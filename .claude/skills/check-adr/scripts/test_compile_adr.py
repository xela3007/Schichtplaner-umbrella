#!/usr/bin/env python3
"""
Regressionstests fuer compile_adr.py.

Jeder Test hier haelt einen Fehler fest, der im ersten Testlauf gegen echte
ADRs tatsaechlich aufgetreten ist. Keine erfundenen Faelle.

Aufruf:
    python3 test_compile_adr.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from compile_adr import Stats, compact, extract_facts, verify  # noqa: E402

FAILED: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}" + (f" — {detail}" if detail else ""))
        FAILED.append(name)


def run(text: str) -> tuple[str, Stats]:
    stats = Stats(path=Path("test.md"))
    return compact(text, stats), stats


# ---------------------------------------------------------------------------
# Bug 1: Code-Bloecke wurden zerstoert
#
# Der erste Entwurf normalisierte Whitespace zeilenweise ueber die ganze
# Datei. Aus dem Verzeichnisbaum in ADR-003 wurde dadurch eine unlesbare
# Liste — Formatierung IST dort die Information.
# ---------------------------------------------------------------------------

print("\nCode-Blöcke bleiben unangetastet")

TREE = """# ADR-003: Repo-Form

- Datum: 2026-08-15

## Festlegungen
- Umbrella ist ein eigenes Repo

## Konsequenzen
```
<Projekt>/                 Umbrella (ADR/, Docs/)
  src/                     gitignored
    <projekt>-app/         eigenes Git-Repo
      package.json
```
"""

out, _ = run(TREE)
check(
    "Einrückung im Code-Block erhalten",
    "  src/                     gitignored" in out,
    "Whitespace im Fence wurde normalisiert",
)
check("Baumstruktur vollständig", out.count("<projekt>-app/") == 1)


# ---------------------------------------------------------------------------
# Bug 2: Fortsetzungszeilen verloren ihre Einrueckung
#
# Ein Stichpunkt, der ueber zwei Zeilen geht, verlor die fuehrenden zwei
# Leerzeichen der Folgezeile. Markdown liest die Zeile dann als neuen
# Absatz — die Liste zerfaellt.
# ---------------------------------------------------------------------------

print("\nFortsetzungszeilen behalten ihre Einrückung")

WRAPPED = """# ADR-009: Test

- Datum: 2026-08-15

## Festlegungen
- Migrationen laufen als Release-Command **vor** dem Start der neuen Version,
  nicht beim ersten Request. Schlägt die Migration fehl, startet die neue
  Version nicht
"""

out, _ = run(WRAPPED)
check(
    "Folgezeile bleibt eingerückt",
    "\n  nicht beim ersten Request" in out,
    "führende Leerzeichen der Fortsetzungszeile entfernt",
)


# ---------------------------------------------------------------------------
# Bug 3: Abschnitte wurden eigenmaechtig geloescht
#
# Der erste Entwurf entfernte "Konsequenzen" automatisch und riss dabei
# Inhalt mit (zwei Verzeichnisbaeume und eine Alias-Festlegung in ADR-003).
# Das Skript darf melden, nicht loeschen.
# ---------------------------------------------------------------------------

print("\nAbschnitte werden gemeldet, nicht gelöscht")

CONSEQ = """# ADR-004: Test

- Datum: 2026-08-15

## Festlegungen
- Postgres auf Neon

## Konsequenzen
- Health-Endpoint prüft DB-Erreichbarkeit
"""

out, stats = run(CONSEQ)
check("Konsequenzen-Abschnitt bleibt erhalten", "## Konsequenzen" in out)
check("Inhalt bleibt erhalten", "Health-Endpoint" in out)
check(
    "Abschnitt wird als Kandidat gemeldet",
    any("Konsequenzen" in s for s in stats.reportable_sections),
)


# ---------------------------------------------------------------------------
# Bug 4: verify() schwieg bei Verlust
#
# extract_facts las nur "Festlegungen"-Abschnitte. Verlor ein anderer
# Abschnitt Inhalt, meldete die Pruefung "88 -> 88 OK".
# ---------------------------------------------------------------------------

print("\nverify() erkennt Verlust in JEDEM Abschnitt")

lost = verify(CONSEQ, CONSEQ.replace("- Health-Endpoint prüft DB-Erreichbarkeit\n", ""))
check("Verlust außerhalb von 'Festlegungen' wird erkannt", len(lost) == 1, str(lost))

lost = verify(CONSEQ, CONSEQ)
check("Kein falscher Alarm bei identischem Text", lost == [])


# ---------------------------------------------------------------------------
# Gewollte Streichungen loesen keinen Alarm aus
#
# `Status:` faellt nach A1 absichtlich, und "(Haus-Default, unveraendert
# uebernommen)" wird aus der Entscheidungszeile entfernt. Beides darf die
# Pruefung nicht als Verlust melden.
# ---------------------------------------------------------------------------

print("\nGewollte Streichungen sind kein Verlust")

HEAD = """# ADR-002: Test

- Status: accepted (Bootstrap)
- Datum: 2026-08-15
- Entscheidung: **TypeScript (Node, Hono)** (Haus-Default, unverändert übernommen)

## Festlegungen
- Zod an jeder Systemgrenze
"""

out, stats = run(HEAD)
check("Status-Zeile entfernt", "Status:" not in out)
check("Floskel entfernt", "Haus-Default" not in out)
check("Entscheidung bleibt lesbar", "**TypeScript (Node, Hono)**" in out)
check("Datum bleibt", "Datum: 2026-08-15" in out)
check("verify meldet keinen Verlust", verify(HEAD, out) == [], str(verify(HEAD, out)))


# ---------------------------------------------------------------------------
# Idempotenz — zweimal laufen darf nichts weiter aendern
# ---------------------------------------------------------------------------

print("\nIdempotenz")

once, _ = run(HEAD)
twice, _ = run(once)
check("zweiter Lauf ändert nichts", once == twice)


# ---------------------------------------------------------------------------
# extract_facts zaehlt Struktur nicht mit
# ---------------------------------------------------------------------------

print("\nextract_facts")

facts = extract_facts(CONSEQ)
check("Überschriften zählen nicht als Inhalt", not any("adr-004" in f for f in facts))
check("Stichpunkte zählen", any("postgres auf neon" in f for f in facts))


# ---------------------------------------------------------------------------

print()
if FAILED:
    print(f"{len(FAILED)} Test(s) fehlgeschlagen: {', '.join(FAILED)}")
    raise SystemExit(1)
print("Alle Tests grün.")
