---
name: graph-to-target
description: |
  Entwickelt aus einem IST-Graph (aus `transcript-graph`) und einem internen
  Lösungsgespräch das **Zielbild** — als zweite Ebene im selben Obsidian-Vault.
  Jede Lösung zeigt auf die IST-Probleme, die sie adressiert; die Abdeckungs-
  lücke wird sichtbar statt behauptet. Antwortet auf die Frage, die der
  IST-Graph offen lässt: „Was machen wir jetzt damit?"

  Aktiviert bei:
  - "Wir haben den Graph durchgesprochen, jetzt brauchen wir ein Zielbild"
  - "Zielbild entwickeln" / "Lösungsbild bauen"
  - "Wie lösen wir das?" mit vorliegendem IST-Graph
  - Wenn ein zweites Transkript vorliegt, in dem intern über die Lösung
    geredet wurde
  - Wenn der Vault nur IST-Knoten enthält und Items entstehen sollen —
    dann ist dieser Schritt der fehlende davor

  NICHT aktivieren:
  - Wenn der IST-Graph erst noch entstehen muss — das ist `transcript-graph`.
  - Wenn das Zielbild steht und Items entstehen sollen — das ist
    `graph-to-asdd`.
---

# Graph to Target

Du entwickelst die **SOLL-Ebene** über einem bestehenden IST-Graph. Sie lebt im
selben Vault, damit Obsidian beide zusammen zeichnet — die Graph-View zeigt
dann unmittelbar, welche Problemcluster abgedeckt sind und welche nackt
dastehen.

## Warum dieser Schritt eigen ist

`transcript-graph` durfte nicht denken — er nimmt auf, was gesagt wurde.
Genau deshalb steht im IST-Graph nirgends, was gebaut werden soll: Der Kunde
hat seinen Zustand beschrieben, die Lösung entsteht bei euch.

Der Fehler, den dieser Schritt verhindert: aus `idee`-Knoten direkt Items
machen. Diese Knoten sind Vorschläge, die im IST-Gespräch gefallen sind —
teils vom Kunden, teils von euch, meist ohne Zustimmung der anderen Seite.
Ein Backlog daraus wäre eine Sammlung von Gesprächsfetzen, kein Zielbild.

**Du entscheidest hier nicht allein.** Das Zielbild kommt aus dem internen
Gespräch. Du strukturierst es, verlinkst es gegen den IST-Graph und machst
sichtbar, was es nicht abdeckt.

## Die SOLL-Ebene

Neue Knotentypen, im selben Vault, mit eigenem ID-Präfix `L` (Lösung):

| `typ` | Was | ID |
|---|---|---|
| `zielbild` | Das übergreifende Bild in wenigen Sätzen. Genau einer. | `L0` |
| `loesung` | Ein Lösungsbaustein. Wird später ein Item oder Epic. | `L1`, `L2`, … |
| `baustein` | Teil einer Lösung, nicht eigenständig lieferbar | `L1.1`, `L1.2` |
| `phase` | Zeitliche Staffelung, gruppiert Lösungen | `P1`, `P2`, … |
| `nicht-loesen` | Bewusst nicht angefasst — **mit Begründung** | `N1`, `N2`, … |
| `annahme` | Wovon das Zielbild ausgeht, ungeprüft | `A1`, `A2`, … |
| `entscheidung` | Im Gespräch getroffen, mit Alternative und Grund | `E1`, `E2`, … |

### Knotenformat

```markdown
---
id: L3
typ: loesung
quelle: ["Z:00:41:20"]
loest: [T1.11, T1.12, T1.13]
phase: P1
status: draft
---
# Preisfindung aus Historie mit Margenvorgabe

> "…wir bauen ihm eine Preisfindung, die aus den letzten Aufträgen im
> gleichen Markt einen Korridor vorschlägt." — 00:41:20

Was entsteht: …

Löst [[T1.11-keine-preisliste]]
Löst [[T1.12-vorkalkulation-ohne-margenvorgabe]]
Löst [[T1.13-preisrecherche-aus-historie]]
Teil von [[P1-phase-eins]]
Setzt voraus [[L1-stammdaten]]
```

**`loest` ist Pflicht** bei `typ: loesung` — als Frontmatter-Liste *und* als
`Löst [[…]]`-Wikilink, damit Obsidian die Kante zeichnet. Eine Lösung ohne
`loest` ist entweder ein Feature ohne Anlass oder es fehlt ein IST-Knoten;
beides muss auffallen.

Bei `nicht-loesen` ist die Begründung Pflicht und `loest` zeigt auf die
Probleme, die damit **offen bleiben**.

## Der Kern: beide Richtungen prüfen

Das ist der eigentliche Wert dieses Schritts, und er muss in beide Richtungen
laufen:

**Vorwärts — jede Lösung braucht einen Anlass.** Eine `loesung` ohne `loest`
zeigt auf nichts. Entweder fehlt der IST-Knoten (dann anlegen, `typ: eigen`,
weil er nicht aus dem Transkript stammt) oder es ist ein Feature, das niemand
gebraucht hat.

**Rückwärts — welches Problem bleibt offen?** Jeder `problem`-Knoten im
IST-Graph, auf den keine `loesung` und kein `nicht-loesen` zeigt, ist eine
Lücke. Nicht als Vorwurf — vieles wird bewusst nicht gelöst. Aber *bewusst*
heißt: es steht als `nicht-loesen` mit Begründung im Vault, nicht im Kopf von
einem, der beim Meeting dabei war.

Diese Liste ist das, was im Kundentermin zählt. Sie gehört in den Bericht und
in `_zielbild.md`.

## Ablauf

### 1. IST-Graph lesen

Vault vollständig lesen. Zählen: Knoten je Typ, Themen, bestehende
Widersprüche (`Widerspricht`-Links).

**Ungelöste Widersprüche zuerst melden.** Wenn der IST-Graph interne
Positionen enthält, die sich widersprechen, ist das die erste Frage ans
Meeting — ein Zielbild auf zwei unvereinbaren Prämissen wird später teuer.
Ebenso: Widersprüche zwischen eurer Bewertung (`typ: eigen`) und belegten
Kundenaussagen.

### 2. Zielbild aufnehmen

Zwei Wege, der Nutzer entscheidet:

**Transkript** — ein zweites Gespräch liegt vor. Lies es wie
`transcript-graph`: in Abschnitten, mit Belegstellen, ohne zu interpretieren.
Zeitstempel bekommen das Präfix `Z:`, damit sie von den IST-Quellen
unterscheidbar bleiben.

**Live im Dialog** — ihr redet, du baust mit. Nach jedem Lösungsbaustein
sofort `loest` klären: *„Welche Probleme aus dem Graph löst das?"* Die
Abdeckungslücke wächst sichtbar mit, und ihr könnt im Meeting gegensteuern.
Aufwendiger im Termin, aber ihr geht mit einem fertigen Zielbild raus statt
mit einer weiteren Datei.

In beiden Fällen gilt weiter: **du erfindest keine Lösungen.** Fällt dir etwas
auf, was fehlt, meldest du es — als Frage, nicht als Knoten.

### 3. Entscheidungen festhalten

Wo im Gespräch eine Richtung gewählt wurde, entsteht ein `entscheidung`-Knoten
mit **Alternative und Grund**. Nicht nur das Ergebnis.

```markdown
---
id: E2
typ: entscheidung
quelle: ["Z:01:12:40"]
status: draft
---
# Lager selbst bauen statt Standardsoftware

Alternative war: CMMS-Standardlösung zukaufen.
Grund: …

Widerspricht [[T16.3-eigen-hybrid-empfehlung]]
```

Löst eine Entscheidung einen bestehenden Widerspruch im IST-Graph auf, verlinke
sie dorthin. Dann ist später nachvollziehbar, wann und warum die Spannung
aufgelöst wurde.

### 4. Abdeckung prüfen

Nach dem Aufnehmen systematisch durchgehen:

- Jedes `problem` im IST-Graph: gelöst, bewusst nicht gelöst, oder offen?
- Jede `loesung`: hat sie `loest`?
- Jeder `zwang`: verletzt das Zielbild ihn irgendwo?
- Jedes `ziel` und jeder `mehrwert`: zahlt mindestens eine Lösung darauf ein?

Das Ergebnis ist eine Tabelle, keine Prosa.

### 5. `_zielbild.md` schreiben

```markdown
---
typ: zielbild
basiert_auf: <vault-name>
quelle_transkript: <datei>
datum: <datum>
status: draft
---
# Zielbild <Kunde>

## Das Bild in drei Sätzen
…

## Phasen
- [[P1-phase-eins]] — …
- [[P2-phase-zwei]] — …

## Abdeckung
| IST-Problem | Lösung | Phase |
|---|---|---|
| [[T1.11-keine-preisliste]] | [[L3-preisfindung]] | P1 |

## Bewusst nicht gelöst
| IST-Problem | Begründung |
|---|---|
| [[T9.4-…]] | [[N2-…]] — Prozessthema, keine Software |

## Offen — weder gelöst noch bewusst ausgeschlossen
- [[T5.12-…]]

## Getroffene Entscheidungen
- [[E2-lager-selbst-bauen]]

## Annahmen
- [[A1-…]] — ungeprüft
```

Die Sektion **„Offen"** ist die wichtigste. Ist sie leer, ist das Zielbild
vollständig. Ist sie es nicht, steht dort schwarz auf weiß, worüber im
Kundentermin noch geredet werden muss.

### 6. Bericht

- Lösungen, Phasen, Entscheidungen, Annahmen — jeweils Anzahl
- **Abdeckung**: X von Y Problemen gelöst, Z bewusst ausgeschlossen, N offen
- Lösungen ohne `loest`
- Zwänge, die das Zielbild verletzt
- Widersprüche: aufgelöst / weiterhin offen
- deine eigenen Anmerkungen, getrennt

Dann der Hinweis: Vault in Obsidian öffnen. In der Graph-View liegen die
IST-Knoten ohne eingehende `Löst`-Kante sichtbar am Rand — das ist die
Abdeckungslücke, ohne dass jemand eine Tabelle lesen muss.

Nächster Schritt: `graph-to-asdd`, das die `loesung`-Knoten im Loop bis zu
ASDD-fähigen Items führt und die IST-Knoten als Kontext und Beleg mitgibt.

## Regeln

- **Du erfindest keine Lösungen.** Das Zielbild kommt aus dem Gespräch.
- **Jede `loesung` hat `loest`.** Ohne Anlass kein Baustein.
- **`nicht-loesen` braucht eine Begründung.** Sonst ist es keine Entscheidung,
  sondern Vergessen.
- **Die IST-Ebene wird nicht verändert.** Keine Knoten löschen, keine
  umschreiben. Fehlt ein IST-Knoten, wird er als `typ: eigen` ergänzt und als
  solcher erkennbar.
- **Widersprüche zuerst.** Ungelöste Spannungen im IST-Graph werden gemeldet,
  bevor das Zielbild darauf gebaut wird.
- **Entscheidungen mit Alternative und Grund.** Ein Ergebnis ohne Grund ist in
  drei Monaten wertlos.
- **Keine Items anlegen.** Dieser Skill schreibt Dateien.
- **Nicht schätzen, nicht kalkulieren.** Phasen sind Reihenfolge, nicht Termine.

## Interaktionsstil

- Deutsch als Default.
- Im Live-Modus: nach jedem Baustein `loest` klären, nicht am Ende sammeln.
- Abdeckungslücke immer als Liste zeigen, nie zusammenfassen.
- Knapp. Die Arbeit steht im Vault.
