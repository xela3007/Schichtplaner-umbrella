#!/usr/bin/env python3
"""
welcome_hook.py -- SessionStart-Hook: Orientierung statt Funkstille.

Das Problem, das dieser Hook loest: nach dem curl-Download sitzt der Nutzer vor
einer leeren Claude-Session und weiss nicht, dass er den Bootstrap ausloesen
muss. Und nachdem der Bootstrap durch ist, weiss er nicht, dass Items im Board
zugewiesen UND in einem AI-Step liegen muessen, damit es weitergeht.

Der Hook kennt den Board-Zustand NICHT (kein MCP-Zugriff). Er unterscheidet
deshalb nur zwei Faelle anhand des Dateisystems:

  bootstrap.lock fehlt  -> Projekt ist noch nicht aufgesetzt
  bootstrap.lock da     -> aufgesetzt, es geht ums Weiterarbeiten

Alles, was den Board-Zustand braucht, steht in der generierten CLAUDE.md --
dort kann Claude list_actionable_items() aufrufen.

ZWEI AUSGABEKANAELE, nicht verwechseln:

  systemMessage                          -> sichtbar im Terminal, fuer den NUTZER
  hookSpecificOutput.additionalContext   -> Modell-Kontext, fuer CLAUDE

SessionStart ist eines der drei Events (neben UserPromptSubmit und
UserPromptExpansion), bei denen reines stdout als Kontext ins Modell wandert.
Wer hier nur Markdown ausgibt, redet also mit Claude statt mit dem Nutzer -- und
der sitzt vor Funkstille, weil Claude keinen Auftrag hat, den Text vorzulesen.
Genau dieser Fehler war in der ersten Fassung drin.

systemMessage ist ein universelles Top-Level-Feld (alle Events),
additionalContext liegt VERSCHACHTELT in hookSpecificOutput. Beide Ebenen sind
verschieden -- additionalContext auf oberster Ebene wird ignoriert.

Fail-safe: jeder Fehler fuehrt zu stiller Ausgabe, nie zu einem Abbruch der
Session. Ein kaputter Welcome-Hook darf niemanden aussperren.
"""

import json
import os
import sys
from pathlib import Path

DOCS_URL = "https://artifacture.ai/docs"
SUPPORT = "support@artifacture.ai"

# Kontext fuer CLAUDE (nicht fuer den Nutzer -- der bekommt systemMessage).
# Knapp halten: Zustandsinformation, keine Wiederholung der Begruessung.
CONTEXT_FRESH = (
    "Dieses Projekt ist noch nicht gebootstrappt (kein bootstrap.lock, kein ADR/). "
    "Der Nutzer hat beim Session-Start den Hinweis auf /artifacture-bootstrap "
    "gesehen -- wiederhole ihn nicht unaufgefordert. Fragt er, was zu tun ist, "
    "oder will er loslegen: den Skill artifacture-bootstrap benutzen."
)
CONTEXT_BOOTSTRAPPED = (
    "Dieses Projekt ist gebootstrappt (bootstrap.lock vorhanden), die ADRs unter "
    "ADR/ sind bindend. Der Nutzer hat beim Start den Hinweis gesehen, dass er "
    "nach offenen Aufgaben fragen muss und dass Items im Board zugewiesen UND in "
    "einem KI-Schritt liegen muessen. Wiederhole das nicht unaufgefordert. "
    "Liefert list_actionable_items() nichts, erklaere woran es haengt -- siehe "
    "CLAUDE.md."
)


def project_dir(payload):
    """cwd aus dem Hook-Input, Fallback CLAUDE_PROJECT_DIR.

    KEIN Fallback auf os.getcwd(): ohne verlaessliche Quelle lieber schweigen.
    Ein falsch geratenes Verzeichnis wuerde in einem fremden Ordner eine
    Bootstrap-Aufforderung zeigen -- schlimmer als keine Nachricht.
    """
    for candidate in (payload.get("cwd"),
                      os.environ.get("CLAUDE_PROJECT_DIR")):
        if not candidate:
            continue
        try:
            path = Path(candidate).resolve()
        except (OSError, ValueError):
            continue
        # resolve() akzeptiert auch nicht existierende Pfade -- ein toter Pfad
        # sieht sonst aus wie ein leeres Projekt und loest die Begruessung aus.
        if path.is_dir():
            return path
    return None


def first_run_message():
    return f"""**Willkommen bei Artifacture.**

Hier liegt noch kein Projekt — es fehlen die Architektur-Entscheidungen (ADRs)
und die ersten Aufgaben auf deinem Board.

**Zum Einrichten:** `/artifacture-bootstrap`

Das ist ein kurzer Fragebogen zur Struktur — keine Produktfragen, die kommen
spaeter und woanders. Im Fasttrack-Modus sind es fuenf Fragen, unter zwei
Minuten. Danach stehen ADRs im Repo und die ersten Stories auf dem Board.

Doku: {DOCS_URL} · Fragen: {SUPPORT}"""


def returning_message(lock_text):
    mode = catalog = None
    for line in (lock_text or "").splitlines():
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip().lower(), value.strip()
        if key in ("mode", "modus"):
            mode = value
        elif key in ("catalog_version", "catalog"):
            catalog = value

    stamp = " · ".join(p for p in (f"Modus {mode}" if mode else None,
                                  f"Katalog {catalog}" if catalog else None) if p)
    stamp = f" ({stamp})" if stamp else ""

    return f"""**Artifacture-Projekt{stamp}**

Frag **"was steht an?"** — dann hole ich die Liste vom Board. Von allein
laeuft nichts los.

Wenn die Liste leer ist, liegt es fast immer an einem von zwei Dingen. Ein Item
wird erst dann fuer KI-Arbeit sichtbar, wenn **beides** stimmt:

1. Es ist **dir zugewiesen**
2. Es steht in einem Schritt, der auf KI wartet (nicht in einem
   Human-Review-Schritt)

Beides stellst du im Artifacture-Board ein, nicht hier. Danach hier einfach
nochmal fragen.

**Ueber das Produkt reden?** Erzaehl einfach, was es koennen soll — ich sortiere
das in Ideas und Insights. Kein Befehl noetig.

Doku: {DOCS_URL} · Fragen: {SUPPORT}"""


def build_message(payload):
    """(nutzer_text, claude_kontext) -- beide None, wenn geschwiegen wird."""
    root = project_dir(payload)
    if root is None:
        return None, None

    lock = root / "bootstrap.lock"
    try:
        if lock.is_file():
            try:
                text = lock.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            return returning_message(text), CONTEXT_BOOTSTRAPPED
        # Kein Lock: nur begruessen, wenn hier auch wirklich nichts steht.
        # Ein fremdes Repo (Code, aber kein Artifacture) soll keine
        # Bootstrap-Aufforderung bekommen -- dafuer ist extract-umbrella da.
        if (root / "ADR").is_dir():
            return None, None
        return first_run_message(), CONTEXT_FRESH
    except OSError:
        return None, None


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            payload = {}
    except (json.JSONDecodeError, ValueError, OSError):
        payload = {}

    try:
        message, context = build_message(payload)
    except Exception:
        message, context = None, None

    if not message:
        return

    # systemMessage  -> sichtbar im Terminal, fuer den NUTZER.
    # additionalContext (in hookSpecificOutput!) -> fuer CLAUDE.
    #
    # Ohne systemMessage landet der Text nur im Modell-Kontext: SessionStart ist
    # eines der drei Events, bei denen stdout als Kontext eingespeist wird. Der
    # Nutzer saehe dann nichts -- genau der Fehler, den diese Trennung behebt.
    payload_out = {"systemMessage": message}
    if context:
        payload_out["hookSpecificOutput"] = {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    print(json.dumps(payload_out))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Ein Welcome-Hook darf niemals eine Session blockieren.
        pass
