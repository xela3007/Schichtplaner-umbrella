---
name: transcript-graph
description: |
  Wandelt lange Gesprächs-Transkripte (Kundentermine, Workshops, IST-Aufnahmen)
  in einen **Knowledge Graph als Obsidian-Vault** — eine Datei pro Knoten,
  verlinkt über Wikilinks. Fasst zusammen und ordnet ein, **interpretiert nicht**.
  Das Ergebnis ist ein Zwischenstand zum gemeinsamen Durchgehen im Meeting,
  kein fertiges Backlog.

  Aktiviert bei:
  - "Wir haben ein Transkript von einem Kundentermin"
  - "Hier sind 4 Stunden Gespräch, arbeite das durch"
  - "Themengebiete aus dem Gespräch aufnehmen"
  - "Knowledge Graph aus dem Transkript bauen"
  - "IST-Aufnahme auswerten"
  - Wenn eine Transkript-Datei (txt/md/vtt/srt) mit Gesprächsinhalt vorliegt,
    die zu lang ist, um sie im Dialog durchzusprechen

  NICHT aktivieren:
  - Bei einem laufenden Produktgespräch im Dialog — das ist `vision-capture`.
  - Wenn der Graph schon existiert und Items entstehen sollen — das ist
    `graph-to-asdd`.
---

# Transcript Graph

Du liest ein Transkript vollständig und legst für jede darin enthaltene Sache
einen Knoten an. Das Ergebnis ist ein Ordner, der sich als Obsidian-Vault
öffnen lässt.

**Du denkst nicht mit.** Das ist die zentrale Regel dieses Skills, und sie ist
schwerer einzuhalten, als sie klingt.

## Warum dieser Skill so streng ist

Bei vier Stunden Transkript ist die Versuchung groß, zu interpretieren: aus
drei Bemerkungen ein Thema zu machen, eine naheliegende Lösung zu ergänzen,
eine Aussage „aufzuräumen". Jede solche Interpretation ist eine Entscheidung,
die niemand getroffen hat — und sie ist im Meeting nicht mehr erkennbar,
weil sie aussieht wie alles andere im Graph.

Der Graph wird gemeinsam durchgegangen und korrigiert. Das funktioniert nur,
wenn jeder Knoten auf eine Stelle im Transkript zeigt. Was nicht belegt ist,
kann nicht geprüft werden.

Geklärt wird später (in `graph-to-asdd`), geschnitten auch. Hier wird nur
aufgenommen.

## Der Vault

Zielordner: `Docs/start-vision/` (oder was der Nutzer nennt). Eine Datei pro
Knoten, Dateiname `<id>-<slug>.md`.

```
Docs/start-vision/
  _index.md
  T1-auftragsabwicklung.md
  T1.1-angebot-dauert-zu-lang.md
  T1.2-freigabe-durch-zweite-person.md
  T2-lagerverwaltung.md
```

### Knotenformat

```markdown
---
id: T1.1
typ: problem
quelle: ["01:47:20", "02:03:05"]
sprecher: Kunde
status: draft
---
# Angebotserstellung dauert zwei Tage

> "…bis das Angebot raus ist, vergehen zwei Tage, weil der Meier das
> noch gegenlesen muss." — 01:47:20

Teil von [[T1-auftragsabwicklung]]
Hängt zusammen mit [[T4.1-freigabeprozesse]]
```

**Frontmatter-Felder:**

| Feld | Bedeutung |
|---|---|
| `id` | Stabil, hierarchisch (`T1`, `T1.1`, `T1.1.2`). `graph-to-asdd` referenziert sie. |
| `typ` | Siehe Knotentypen unten. |
| `quelle` | Zeitstempel oder Zeilennummern. **Pflicht** außer bei `typ: eigen`. |
| `sprecher` | Wer hat es gesagt (`Kunde`, `Norman`, Name/Rolle). Optional, aber hilfreich. |
| `status` | `draft` (von dir) / `bestaetigt` / `verworfen` (im Meeting gesetzt). |

Der Body ist: Überschrift, **wörtliches Zitat**, dann eine knappe Zusammenfassung
in *neutraler* Sprache, dann die Links. Zitate immer als Blockquote mit
Zeitstempel — sie sind der Prüfanker.

### Knotentypen

| `typ` | Was | Wird später… |
|---|---|---|
| `thema` | Themengebiet, gliedernd | …nie ein Item, evtl. ein Epic |
| `ziel` | Was der Kunde erreichen will | …nie ein Item, wird Kontext |
| `problem` | Was heute nicht funktioniert | …oft ein Item |
| `idee` | Vorgeschlagene Lösung | …fast immer ein Item |
| `mehrwert` | Erwarteter Nutzen | …nie ein Item, begründet Priorität |
| `detail` | Konkretisierung eines anderen Knotens | …Teil eines Items |
| `fakt` | IST-Zustand, Systeme, Zahlen, Mengen | …wird Insight |
| `zwang` | Regulatorik, Termine, Vorgaben | …wird Insight mit Konsequenz |
| `offen` | Im Gespräch aufgeworfen, nicht beantwortet | …wird Frage im Refinement |
| `eigen` | **Nicht aus dem Transkript** — im Meeting ergänzt | …wie sein Inhalt |

`eigen` ist der einzige Typ ohne `quelle`. Wenn *du* etwas ergänzen willst,
was nicht im Transkript steht: nicht in den Graph schreiben, sondern am Ende
als Anmerkung melden. Der Nutzer entscheidet, ob daraus ein `eigen`-Knoten wird.

### `_index.md`

Einstiegspunkt: Metadaten des Gesprächs (Datum, Teilnehmer, Dauer, Quelldatei),
die Themengebiete als Wikilink-Liste, und der Verarbeitungsstand.

```markdown
---
quelle_datei: transkript-2026-09-09.txt
datum: 2026-09-09
dauer: 4h
teilnehmer: [Norman, ...]
status: draft
---
# IST-Aufnahme <Kunde>

## Themengebiete
- [[T1-auftragsabwicklung]] — 12 Knoten
- [[T2-lagerverwaltung]] — 8 Knoten

## Verarbeitungsstand
Abschnitt 1–4 von 8 verarbeitet.
```

## Ablauf

### 1. Vorbereiten

- Transkript-Datei finden (Pfad vom Nutzer, sonst fragen). Länge feststellen.
- Zielordner klären. Existiert er schon mit Knoten: **nicht überschreiben** —
  fragen, ob ergänzt oder neu angelegt wird.
- ADRs unter `ADR/` lesen, falls vorhanden. Nicht um zu filtern, sondern um
  Widersprüche später benennen zu können.

### 2. In Abschnitten lesen

Ein 4h-Transkript passt nicht in einen sinnvollen Arbeitsschritt. Teile es in
Abschnitte von etwa 20–30 Minuten Gesprächszeit und arbeite sie **der Reihe
nach** ab. Nach jedem Abschnitt:

- Knoten des Abschnitts schreiben
- `_index.md` unter „Verarbeitungsstand" fortschreiben
- knapp melden, was dazukam

So geht bei Abbruch nichts verloren, und der Nutzer kann früh gegensteuern,
wenn die Extraktion in die falsche Richtung läuft.

**Überflieg nichts.** Nebensätze enthalten oft die `zwang`- und `fakt`-Knoten,
die später am meisten wert sind.

### 3. Knoten anlegen

Für jede Sache im Transkript genau einen Knoten. Ein Knoten ist **eine** Sache:
Werden im selben Satz drei Probleme genannt, sind das drei Knoten.

Hierarchie über `id` und Wikilinks — `Teil von [[…]]` nach oben,
`Hängt zusammen mit [[…]]` quer. Querverbindungen sind wertvoll: wenn dasselbe
Thema an drei Stellen auftaucht, verlinke alle drei, statt zu entscheiden,
wo es „hingehört".

Bei Wiederholung: **kein neuer Knoten**, sondern zusätzlicher Eintrag in
`quelle` beim bestehenden. Dass etwas dreimal gesagt wurde, ist Information.

### 4. Widersprüche markieren, nicht auflösen

Sagt der Kunde an zwei Stellen Unterschiedliches, lege **beide** Knoten an und
verlinke sie mit `Widerspricht [[…]]`. Nicht entscheiden, welche Aussage gilt —
das ist eine fachliche Entscheidung und gehört ins Meeting.

Dasselbe bei Widerspruch zu einem ADR: im Knoten vermerken, nicht weglassen.

### 5. Übergeben

Am Ende meldest du:

- Anzahl Knoten je Typ
- die Themengebiete
- **was du nicht einordnen konntest** (wörtlich, mit Zeitstempel)
- Widersprüche
- deine eigenen Anmerkungen — klar getrennt, als Vorschlag für `eigen`-Knoten

Dann der Hinweis: Ordner in Obsidian als Vault öffnen, Graph-View nutzen.
Sieht der Graph aus wie eine flache Liste, hat die Extraktion keine Struktur
getroffen — dann lieber nachbessern als weitergeben.

Nächster Schritt nach dem Meeting: `graph-to-target` für das Zielbild, oder
direkt `graph-to-asdd` — das entwickelt das Zielbild bei Bedarf im Loop mit.

## Regeln

- **Du erfindest nichts.** Keine Lösung ergänzen, kein Thema konstruieren,
  keine Aussage „vervollständigen".
- **Jeder Knoten hat eine Quelle** — außer `typ: eigen`.
- **Zitate sind wörtlich.** Kürzen mit `…` ist erlaubt, umformulieren nicht.
- **Eine Sache pro Knoten.**
- **Nichts still weglassen.** Was du nicht einordnen kannst, wird gemeldet.
- **Nicht klären, nicht schneiden, nicht priorisieren.** Das sind die nächsten
  Schritte und sie haben ihre eigenen Regeln.
- **Keine Items anlegen.** Dieser Skill schreibt ausschließlich Dateien.
- **Kein Fließtext-Dokument.** Kein „Zusammenfassung.md" neben dem Graph.

## Interaktionsstil

- Deutsch als Default.
- Nach jedem Abschnitt kurz melden, nicht erst am Ende.
- Knapp. Die Arbeit steht im Vault, nicht in der Antwort.
