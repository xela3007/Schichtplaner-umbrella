#!/usr/bin/env python3
"""
Verdichtet ADRs in-place — die Quelle IST das Ergebnis.

Kein Kompilat, keine zweite Datei. Begruendung: Zwei Fassungen derselben
Entscheidung sind zwei Dinge im Kontext, und welches gewinnt, ist Zufall
(Regel 0, RULES.md). Genau dieser Fehler steckt im BOCK-Repo: ADR-002 wurde
auf `#shared/*` korrigiert, ADR-003 und ADR-007 nennen weiter `@shared/*` —
der falsche Alias steht oefter im Kontext als die Korrektur.

Was dieses Skript tut, ist **deterministisch und mechanisch**. Es trifft keine
inhaltliche Entscheidung. Alles, was Urteilsvermoegen braucht — ist dieser
Grund ein Absperr-Grund oder Nachschlag? ist das eine Festlegung oder ein
Verweis? — macht der Skill, und zwar VOR diesem Skript.

Arbeitsteilung:
    Skill  entscheidet inhaltlich, bearbeitet die Quelle
    Script verdichtet mechanisch, zaehlt, verifiziert

Verifikation ist der wichtigste Teil: Ein verdichtetes ADR, das eine
Festlegung verliert, ist schlimmer als ein langes. Das Skript bricht ab,
wenn eine Festlegung verschwindet.

Aufruf:
    compile_adr.py --check   ADR/       nur messen, nichts aendern
    compile_adr.py           ADR/       verdichten (schreibt in-place)
    compile_adr.py --diff    ADR/       zeigen, was passieren wuerde
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Token-Zaehlung
#
# Ohne echte Zaehlung ist jede Ersparnis-Angabe geraten. tiktoken ist nicht
# Anthropics Tokenizer, liegt aber nah genug fuer eine Relativaussage
# ("38 % weniger"), und genau darum geht es hier. Fehlt es, faellt das Skript
# auf eine Wortzaehlung zurueck und sagt das auch.
# ---------------------------------------------------------------------------

try:
    import tiktoken

    _ENC = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str) -> int:
        return len(_ENC.encode(text))

    TOKENIZER = "tiktoken/cl100k_base (Näherung)"
except Exception:  # pragma: no cover - haengt an der Umgebung

    def count_tokens(text: str) -> int:
        # ~1.3 Token pro Wort ist fuer deutschen Prosatext eine brauchbare
        # Naeherung. Nur fuer die Relativaussage gedacht.
        return int(len(text.split()) * 1.3)

    TOKENIZER = "Schätzung (tiktoken nicht installiert)"


# ---------------------------------------------------------------------------
# Was mechanisch weg kann
# ---------------------------------------------------------------------------

# Abschnitte, die das Skript NICHT eigenmaechtig entfernt.
#
# Erster Entwurf loeschte "Konsequenzen" automatisch. Der Testlauf gegen
# ADR-003 zeigte, warum das falsch ist: Dort standen im Konsequenzen-Abschnitt
# zwei Verzeichnisbaeume und die Zeile "Path-Alias `@shared/*` gilt innerhalb
# dieses Repos" — Inhalt, teils veraltet, aber nicht mechanisch entbehrlich.
# Und die Verifikation schwieg, weil sie nur geschuetzte Abschnitte zaehlt.
#
# Daraus die Regel: Das Skript entfernt keine Abschnitte. Es MELDET
# entfernbare Kandidaten, und der Skill entscheidet je Zeile — Festlegung
# hochziehen, Verweis streichen. Genau die Trennung, die dieses Werkzeug
# braucht: mechanisch verdichten, inhaltlich entscheiden lassen.
REPORTABLE_SECTIONS = {
    "konsequenzen",
    "consequences",
    "folgen",
}

# Abschnitte, die niemals automatisch fallen: Hier stehen Festlegungen.
PROTECTED_SECTIONS = {
    "festlegungen",
    "entscheidung",
    "decision",
    "regeln",
}

# Metazeilen im Kopf. `Status` faellt, weil A1 nur einen Zustand kennt:
# Was in ADR/ liegt, gilt. Eine Zeile "Status: accepted" ist damit reine
# Wiederholung. `Datum` bleibt — es ordnet Korrekturen zeitlich ein.
DROPPABLE_META = re.compile(
    r"^\s*[-*]\s*(Status|Autor|Author|Owner|Verantwortlich)\s*:", re.IGNORECASE
)

# Fuellwendungen ohne Informationsgehalt. Nur solche, die den Satz nicht
# aendern — dieses Skript formuliert nicht um.
NOISE_PHRASES = [
    (r"\(Haus-Default, unverändert übernommen\)", ""),
    (r"\(Haus-Default\)", ""),
    (r"\(Bootstrap\)", ""),
    (r"\s+—\s+siehe unten", ""),
]


@dataclass
class Stats:
    path: Path
    tokens_before: int = 0
    tokens_after: int = 0
    reportable_sections: list[str] = field(default_factory=list)
    dropped_meta: int = 0
    facts_before: int = 0
    facts_after: int = 0

    @property
    def saved(self) -> int:
        return self.tokens_before - self.tokens_after

    @property
    def saved_pct(self) -> float:
        if not self.tokens_before:
            return 0.0
        return 100.0 * self.saved / self.tokens_before


# ---------------------------------------------------------------------------
# Festlegungen erkennen — Grundlage der Verifikation
# ---------------------------------------------------------------------------


def extract_facts(text: str) -> list[str]:
    """
    Jede inhaltstragende Zeile eines ADR, normalisiert.

    Absichtlich NICHT auf "Festlegungen"-Abschnitte beschraenkt: Der erste
    Entwurf tat das und uebersah dadurch, dass beim Entfernen des
    Konsequenzen-Abschnitts Inhalt verschwand — die Pruefung meldete "88 -> 88
    OK", waehrend zwei Verzeichnisbaeume weg waren.

    Gezaehlt wird deshalb alles ausser Struktur: Ueberschriften, Leerzeilen und
    Code-Fence-Marker. Normalisiert auf Kleinschreibung ohne Markdown-Deko,
    damit reines Umformatieren nicht als Verlust gilt.
    """
    facts: list[str] = []
    in_fence = False

    for line in text.splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            continue

        if not stripped or (not in_fence and stripped.startswith("#")):
            continue

        fact = re.sub(r"^\s*[-*]\s+", "", line)
        fact = re.sub(r"[*`_|]", "", fact)
        fact = re.sub(r"\s+", " ", fact).strip().lower()
        if fact:
            facts.append(fact)

    return facts


def fact_key(fact: str) -> str:
    """
    Wiedererkennungs-Schluessel einer Festlegung.

    Nur Buchstaben und Ziffern, damit Umformatierung (Bindestriche,
    Klammern, Deko) die Wiedererkennung nicht bricht.
    """
    return re.sub(r"[^a-z0-9äöüß]", "", fact)[:60]


# ---------------------------------------------------------------------------
# Verdichten
# ---------------------------------------------------------------------------


def compact(text: str, stats: Stats) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False

    for line in lines:
        # Code-Bloecke bleiben unangetastet. Der erste Entwurf normalisierte
        # auch dort Whitespace und machte aus einem Verzeichnisbaum in ADR-003
        # eine unlesbare Liste. Formatierung IST dort die Information.
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        heading = re.match(r"^(#{2,})\s*(.+?)\s*$", line)

        if heading:
            name = heading.group(2).lower()
            base = re.sub(r"\s*\(.*?\)\s*", "", name).strip()

            # Nur vormerken — entfernt wird hier nichts (siehe
            # REPORTABLE_SECTIONS). Der Skill sieht sich den Abschnitt an und
            # entscheidet je Zeile.
            if base in REPORTABLE_SECTIONS:
                stats.reportable_sections.append(heading.group(2))

            out.append(line)
            continue

        if DROPPABLE_META.match(line):
            stats.dropped_meta += 1
            continue

        cleaned = line
        for pattern, repl in NOISE_PHRASES:
            cleaned = re.sub(pattern, repl, cleaned)

        # Nur INNERHALB der Zeile aufraeumen — die fuehrende Einrueckung
        # bleibt. Sie markiert Fortsetzungszeilen von Stichpunkten; ohne sie
        # verliert die Liste ihre Struktur.
        if cleaned.strip():
            indent = re.match(r"^[ \t]*", cleaned).group(0)
            body = cleaned[len(indent) :]
            body = re.sub(r"[ \t]{2,}", " ", body)
            cleaned = (indent + body).rstrip()

        out.append(cleaned)

    # Mehr als eine Leerzeile am Stueck bringt nichts
    result: list[str] = []
    blank = 0
    for line in out:
        if not line.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        result.append(line)

    while result and not result[-1].strip():
        result.pop()

    return "\n".join(result) + "\n"


def verify(before: str, after: str) -> list[str]:
    """
    Ist Inhalt verloren gegangen, der nicht verloren gehen durfte?

    Das ist die Abbruchbedingung des Skripts: Verdichtung, die eine Festlegung
    kostet, ist Datenverlust und kein Gewinn.

    Zwei Arten von Wegfall sind gewollt und duerfen die Pruefung nicht
    ausloesen:

    1. Metazeilen, die DROPPABLE_META absichtlich entfernt (`Status:` faellt
       nach A1 — was in ADR/ liegt, gilt; die Zeile wiederholt das nur).
    2. Zeilen, die durch NOISE_PHRASES gekuerzt wurden. Die Entscheidungszeile
       verliert "(Haus-Default, unveraendert uebernommen)" und traegt danach
       einen anderen Schluessel — die Aussage steht aber unveraendert da.

    Fuer Fall 2 wird der Vergleich auf beiden Seiten mit denselben Regeln
    normalisiert, statt eine Ausnahmeliste zu pflegen: Was das Skript
    absichtlich entfernt, entfernt es auch aus dem Vergleichstext.
    """

    def normalize(text: str) -> str:
        """Wendet dieselben Streichungen an, die `compact` vornimmt."""
        for pattern, repl in NOISE_PHRASES:
            text = re.sub(pattern, repl, text)
        # Absichtlich entfernte Metazeilen zaehlen nicht als Verlust.
        return "\n".join(
            line for line in text.splitlines() if not DROPPABLE_META.match(line)
        )

    # WICHTIG: erst normalisieren, dann extrahieren. Umgekehrt greifen die
    # Muster nicht mehr, weil `extract_facts` die Markdown-Marker schon
    # entfernt hat — und `fact_key` schneidet auf 60 Zeichen, sodass der
    # Unterschied unsichtbar wird.
    keys_after = {fact_key(f) for f in extract_facts(normalize(after))}

    return [
        fact
        for fact in extract_facts(normalize(before))
        if fact_key(fact) not in keys_after
    ]


# ---------------------------------------------------------------------------
# Ablauf
# ---------------------------------------------------------------------------


def process(path: Path, write: bool, show_diff: bool) -> Stats:
    original = path.read_text(encoding="utf-8")
    stats = Stats(path=path)
    stats.tokens_before = count_tokens(original)
    # Ohne die absichtlich entfernten Metazeilen — sonst meldet der Zaehler
    # einen Verlust, den `verify` gerade als gewollt durchgewinkt hat.
    stats.facts_before = len(
        extract_facts(
            "\n".join(
                l for l in original.splitlines() if not DROPPABLE_META.match(l)
            )
        )
    )

    compacted = compact(original, stats)
    stats.tokens_after = count_tokens(compacted)
    stats.facts_after = len(extract_facts(compacted))

    lost = verify(original, compacted)
    if lost:
        print(f"\nABBRUCH — {path.name}: Festlegung verloren", file=sys.stderr)
        for fact in lost:
            print(f"    {fact[:90]}", file=sys.stderr)
        raise SystemExit(2)

    if show_diff and compacted != original:
        import difflib

        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            compacted.splitlines(keepends=True),
            fromfile=f"{path.name} (jetzt)",
            tofile=f"{path.name} (verdichtet)",
        )
        sys.stdout.writelines(diff)

    if write and compacted != original:
        path.write_text(compacted, encoding="utf-8")

    return stats


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Verdichtet ADRs in-place. Die Quelle ist das Ergebnis."
    )
    ap.add_argument("adr_dir", type=Path, help="Pfad zum ADR-Ordner")
    ap.add_argument(
        "--check", action="store_true", help="nur messen, nichts schreiben"
    )
    ap.add_argument(
        "--diff", action="store_true", help="zeigen, was passieren würde"
    )
    args = ap.parse_args()

    # Ordner oder Einzeldatei — beim Nachziehen einer Korrektur will man ein
    # ADR einzeln pruefen, nicht den ganzen Ordner.
    target = args.adr_dir
    if target.is_dir():
        files = sorted(p for p in target.glob("*.md") if not p.name.startswith("_"))
    elif target.is_file() and target.suffix == ".md":
        files = [target]
    else:
        print(f"Kein ADR-Ordner und keine .md-Datei: {target}", file=sys.stderr)
        return 1

    if not files:
        print(f"Keine ADRs in {target}", file=sys.stderr)
        return 1

    write = not (args.check or args.diff)
    all_stats = [process(p, write, args.diff) for p in files]

    tb = sum(s.tokens_before for s in all_stats)
    ta = sum(s.tokens_after for s in all_stats)
    fb = sum(s.facts_before for s in all_stats)
    fa = sum(s.facts_after for s in all_stats)

    print(f"\nTokenizer: {TOKENIZER}")
    print(f"{'ADR':<26} {'vorher':>8} {'nachher':>8} {'gespart':>9}")
    print("-" * 55)
    for s in all_stats:
        mark = "" if s.saved else "  (unverändert)"
        print(
            f"{s.path.name:<26} {s.tokens_before:>8} {s.tokens_after:>8} "
            f"{s.saved_pct:>8.0f}%{mark}"
        )

    print("-" * 55)
    pct = 100.0 * (tb - ta) / tb if tb else 0.0
    print(f"{'Gesamt':<26} {tb:>8} {ta:>8} {pct:>8.0f}%")
    print(f"\nFestlegungen: {fb} → {fa}  " + ("OK" if fb == fa else "PRUEFEN"))

    # Kandidaten, die der Skill inhaltlich pruefen muss — nicht entfernt.
    candidates = [
        (s.path.name, sec) for s in all_stats for sec in s.reportable_sections
    ]
    if candidates:
        print("\nZu prüfen (nicht entfernt — Festlegung hochziehen oder streichen):")
        for name, sec in candidates:
            print(f"    {name}: Abschnitt '{sec}'")
    meta = sum(s.dropped_meta for s in all_stats)
    if meta:
        print(f"Entfernte Metazeilen: {meta}")

    if args.check:
        print("\n--check: nichts geschrieben")
    elif args.diff:
        print("\n--diff: nichts geschrieben")
    else:
        print(f"\n{len(files)} ADRs verdichtet (in-place)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
