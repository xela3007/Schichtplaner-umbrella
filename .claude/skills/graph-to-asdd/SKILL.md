---
name: graph-to-asdd
description: |
  Nimmt einen Knowledge-Graph-Vault und führt ihn in einem **rekursiven Loop**
  bis zu ASDD-fähigen Items — stellt überall Fragen, wo etwas fehlt, und legt
  am Ende einen **verketteten Baum** im ASDD-Backlog ab: Epics über Items,
  Reihenfolge, Blockierungen, Prioritäten.

  Der Loop pro Knoten ist immer dieselbe Frage — *„Könnte ASDD daraus ohne
  Rückfrage eine Spec schreiben?"* — und die Antwort bestimmt, was passiert:
  **absenken** (du entscheidest, der Lösungsraum wird enger), **klären**
  (Antwort beschaffen) oder **aufteilen** (zu viele auf einmal).

  Läuft auf jedem Vault: mit Zielbild (aus `graph-to-target`) startet er dort,
  ohne Zielbild ist die erste Absenkung genau diese Frage. Woher der Graph
  kommt — Discovery-Transkript, Notion-Sammlung, KI-Umriss — ist egal.

  Zwischenstand lebt im Vault: bricht die Session ab, liest der nächste Lauf
  den Vault und macht weiter.

  Aktiviert bei:
  - "Der Graph steht, mach Items draus"
  - "Graph nach ASDD" / "vom Graph in die Umsetzung"
  - "Lass uns den Graph durcharbeiten"
  - "Was fehlt noch, damit wir bauen können?" mit vorliegendem Vault
  - Wenn ein Vault mit Knoten vorliegt und Items entstehen sollen

  NICHT aktivieren:
  - Wenn der Graph erst noch entstehen muss — das ist `transcript-graph`.
  - Bei einem Gespräch im Dialog ohne Vault — das ist `vision-capture`.
  - Wenn ein einzelnes Item auf dem Board aufbereitet werden soll und kein
    Vault existiert — dort greift der Board-Workflow.
---

# Graph to ASDD

Du führst einen Vault in einem rekursiven Loop bis zu Items, aus denen ASDD
ohne Rückfrage eine Spec schreiben kann — und legst sie **verkettet** ab.

Das Höhenmodell hinter der Prüffrage steht in `hoehenmodell.md` (neben dieser Datei).

## Warum das auf dem Graph läuft und nicht Item für Item

Der Graph weiß Dinge, die ein einzelnes Item nicht weiß:

- **Dieselbe offene Frage hängt an vier Lösungen.** Einmal fragen statt
  viermal — das sieht nur, wer den Graph vor sich hat.
- **Reihenfolge und Blockierungen stehen als Kanten da** (`Setzt voraus`,
  `Hängt zusammen mit`). Ein Item-für-Item-Verfahren verliert sie.
- **Eine Entscheidung wirkt auf mehrere Äste.** Wer zuerst entscheidet, was
  in Version 1 gehört, spart die Klärung für alles, was rausfällt.

Deshalb bleibt der Graph während des gesamten Loops die Arbeitsfläche. Erst
am Ende entstehen Items — und dann mit allen Kanten, die der Graph kennt.

## Die Prüffrage

Für jeden Knoten, der ein Item werden könnte, und für **jedes** Stück, das
unterwegs entsteht:

> **Könnte ASDD daraus ohne Rückfrage eine Spec schreiben?**

Ja → fertig. Nein → **was genau fehlt?**

| Was fehlt | Operation | Wer |
|---|---|---|
| Eine **Entscheidung** — mehrere Wege offen, keiner gewählt | **Absenken** | **Mensch** |
| Eine **Information** — Weg klar, Details fehlen | **Klären** | KI |
| **Nichts**, nur zu viele auf einmal | **Aufteilen** | KI |
| Nichts | fertig | — |

**Das ist ein Kreisel, keine Treppe.** Jedes Stück läuft nach jeder Operation
wieder hinein:

```
          ┌─────────────────────────┐
          │      Prüffrage          │ ←──────────────┐
          └───────────┬─────────────┘                │
      ┌───────────────┼───────────────┬──────────┐   │
      ▼               ▼               ▼          ▼   │
  Entscheidung   Information    zu viele     nichts  │
      │               │               │          │   │
   Absenken        Klären        Aufteilen    fertig │
   (Mensch)         (KI)           (KI)         │    │
      └───────────────┴───────────────┘         ▼    │
                      │                       ASDD   │
                      └──────────────────────────────┘
```

Alle Wege kommen vor: Klären deckt Breite auf → aufteilen. Ein Stück wirft
eine Frage auf → klären. Eine Klärung zeigt, dass niemand gewählt hat →
absenken.

Der Loop endet, weil jede Operation entweder etwas Offenes schließt oder das
Stück verkleinert — nicht, weil er in eine Richtung läuft.

**Unterscheidung Entscheidung/Information:** *Gibt es mehrere vertretbare
Antworten, zwischen denen jemand wählen muss?* → Entscheidung. *Oder gibt es
eine richtige, die nur niemand herausgesucht hat?* → Information.

Im Zweifel **Entscheidung**. Einen Menschen zu viel gefragt kostet eine
Minute; eine still getroffene Produktentscheidung kostet ein Release.

## Ohne Zielbild: die erste Absenkung

Enthält der Vault nur IST-Knoten (`problem`, `fakt`, `zwang`, …) und keine
`loesung`-Knoten, ist die **erste Absenkung** die Zielbild-Frage:

> Diese Probleme stehen im Graph. Was davon lösen wir, und wie?

Das ist eine Entscheidung, also legst du sie vor und triffst sie nicht. Das
Ergebnis sind `loesung`-Knoten, die du in den Vault schreibst — mit `loest`
auf die Probleme, die sie adressieren.

Danach läuft der Loop normal weiter. **Was nicht gelöst wird, wird als
`nicht-loesen` mit Begründung festgehalten** — sonst ist später nicht
unterscheidbar, was bewusst draußen blieb und was vergessen wurde.

Liegt ein Zielbild vor, überspringst du diesen Schritt und startest bei den
`loesung`-Knoten.

## Absenken — der einzige Schritt mit Mensch

**Hier wird der Lösungsraum eingeschränkt, und das ist Produktarbeit.** Eine
KI, die das selbst entscheidet, trifft Produktentscheidungen unter der Tarnung
von Aufbereitung — und niemand sieht es, weil das Ergebnis aussieht wie jedes
andere Item.

Feste Form beim Vorlegen:

```
ABSENKUNG — L3 "Förderanträge digital bearbeiten"

ASDD kann daraus keine Spec schreiben. Es fehlt eine Entscheidung:
  Welche Antragsarten deckt die erste Version ab?

Warum jetzt:
  Der Zuschnitt bestimmt Datenmodell und Rollen — später geändert
  kostet er beides.

Belege aus dem Graph:
  T2.4  > "…wir haben vierzehn verschiedene Förderprogramme." — 00:41:02
  T2.9  > "…die Investitionsförderung ist das Brot-und-Butter-Geschäft."
  Z2    Zwang: Fristenlauf nach VwVfG gilt für alle Arten gleich

Wege:
  A) Nur Investitionsförderung      → 3–4 Items, Rest später
  B) Alle vierzehn, generisch       → 2 Items, Modellentscheidung mit
                                       langer Wirkung
  C) Investitionsförderung + Modell vorbereiten → 4–5 Items

Betrifft außerdem: L7, L9 (hängen an derselben Entscheidung)

Ich empfehle keinen Weg. Das ist deine Entscheidung.
```

**Wege vorschlagen: ja.** Sie entscheiden nicht, sie machen entscheidbar.
Einen davon wählen oder empfehlen: nein.

Die Zeile **„Betrifft außerdem"** ist der Vorteil des Graph-Laufs: Wenn eine
Entscheidung mehrere Äste betrifft, steht das dabei — und wird einmal
getroffen statt dreimal.

### Wenn nicht entschieden werden kann

Kommt vor: Der Kunde muss gefragt werden, jemand ist im Urlaub. Dann
**markierst du den Ast als blockiert**, hältst die fehlende Entscheidung im
Vault fest und arbeitest an den anderen Ästen weiter.

Ein blockierter Ast hält den Rest nicht auf. Deshalb Ast für Ast, nicht
Ebene für Ebene.

## Klären — autonom

Reihenfolge beim Suchen:

1. **ADRs unter `ADR/`** — eine Frage, die ein ADR beantwortet, ist
   entschieden. Verweisen, weitergehen, nie neu aufmachen.
2. **Der Vault** — `offen`- und `annahme`-Knoten stehen oft schon mit Kontext
   da; `zwang`-Knoten begrenzen die möglichen Antworten.
3. **Den Menschen fragen** — nur, was 1 und 2 nicht hergeben.

**Fragen bündeln.** Bevor du fragst, prüfe, ob dieselbe Frage an mehreren
Knoten hängt. Vier Lösungen mit derselben offenen Frage sind **eine** Frage.

**Klären ist nicht die Lösung neu aufmachen.** Stellt sich heraus, dass eine
frühere Entscheidung falsch war: melden, nicht still korrigieren. Sonst
zerfällt die Nachvollziehbarkeit zwischen Quelle und Backlog.

Nach dem Klären: **Prüffrage erneut.** Eine Klärung kann aufdecken, dass doch
eine Entscheidung fehlt.

## Aufteilen — autonom

Erkennungsmerkmal: Die Stücke unterscheiden sich in **Daten, nicht in
Struktur**. „47 Buttons umfärben" ist ein Ding, 47-mal ausgeführt.

- **Bündeln**, wenn identisch bis auf Daten → *ein* Item mit Liste
- **Trennen**, wenn eigene Akzeptanzkriterien → N Items

Im Zweifel bündeln. Aufteilen schränkt den Lösungsraum nicht ein — es sortiert
nur, was ohnehin drin war. Die Stücke sind **echte Items** und gehen einzeln
wieder in die Prüffrage.

## Die Arbeitsebene im Vault

Der Loop schreibt mit. Bricht die Session ab, liest der nächste Lauf den Vault
und macht weiter — deshalb ist der Zwischenstand kein Nebenprodukt, sondern
Teil der Arbeit.

Neue Knotentypen, ID-Präfix `W` (Work):

| `typ` | Was | ID |
|---|---|---|
| `entscheidung` | Beim Absenken getroffen — mit Alternative und Grund | `W1`, `W2`, … |
| `antwort` | Beim Klären beschafft — mit Quelle | `W1.1`, … |
| `blockiert` | Ast wartet auf eine Entscheidung, die niemand treffen kann | `B1`, … |
| `paket` | Stück, das die Prüffrage besteht — wird ASDD-Item | `P1`, `P2`, … |

### Knotenformat

```markdown
---
id: P3
typ: paket
stand: fertig
pfad: [L3, W1, L3.2]
loest: [T2.4, T2.9]
braucht: [P1]
epic: L3
prio: 2
adrs: [ADR-014, ADR-003]
---
# Anlagen hochladen (PDF, max 10 MB)

Was entsteht: …

Entstanden aus [[L3-foerderantraege]] über [[W1-nur-investitionsfoerderung]]
Löst [[T2.4-vierzehn-programme]]
Setzt voraus [[P1-antrag-anlegen]]
```

**`stand`** trägt den Loop: `offen` → `geklaert` → `fertig` → `angelegt`.
**`pfad`** ist Pflicht — ohne ihn ist nach zwei Ebenen nicht mehr
nachvollziehbar, warum ein Item so zugeschnitten ist.

### `_arbeit.md`

Der Einstiegspunkt für den nächsten Lauf:

```markdown
---
typ: arbeitsstand
vault: <name>
stand: laufend
datum: <datum>
---
# Arbeitsstand

## Erledigt
- [[L3-foerderantraege]] → 5 Pakete, 1 blockiert
- [[L7-datev-export]] → 1 Paket

## Offen
- [[L5-bestandsfuehrung]] — noch nicht angefasst

## Blockiert
- [[B1-signaturverfahren]] — betrifft P4; Kunde muss gefragt werden

## Getroffene Entscheidungen
- [[W1-nur-investitionsfoerderung]] — betraf L3, L7, L9
```

## Ablauf

### 1. Vault lesen

Alle Knoten, Frontmatter und Wikilinks. Feststellen:

- Gibt es `loesung`-Knoten? → Loop startet dort. Sonst: erste Absenkung ist
  die Zielbild-Frage.
- Gibt es `_arbeit.md`? → **Fortsetzung.** Erledigtes nicht neu bearbeiten.
- Status der Knoten: `draft` überall heißt, niemand hat den Graph geprüft —
  **fragen**, ob das Meeting stattgefunden hat. Ungeprüft durchlaufen heißt,
  Extraktionsfehler bis nach ASDD durchzureichen.

**ADRs unter `ADR/` immer lesen.** Sie sind bindend, beantworten Fragen und
begrenzen die Wege, die du beim Absenken vorschlägst.

### 2. Querschnitt vor dem Loop

Bevor du den ersten Ast anfasst, einmal über den ganzen Graph schauen:

- **Welche Fragen hängen an mehreren Knoten?** Die werden gebündelt gestellt.
- **Welche Entscheidungen betreffen mehrere Äste?** Die werden zuerst
  vorgelegt — sie schneiden Arbeit weg.
- **Welche `zwang`-Knoten gelten global?** Die begrenzen jeden Weg.
- **Welche Widersprüche stehen ungelöst im Graph?** Melden, bevor darauf
  gebaut wird.

Das ist der Schritt, der den Graph-Lauf vom Item-Lauf unterscheidet. Wer ihn
überspringt, fragt dieselbe Frage viermal.

### 3. Ast für Ast

Einen Ast bis nach unten führen, dann den nächsten. Blockierte Äste liegen
lassen.

Nach jedem Absenken kurz melden:

```
Ast L3 → Investitionsförderung (Ebene 2)
  ✓ P1  Antrag anlegen mit Stammdaten      fertig
  ✓ P2  Anlagen hochladen                  fertig
  … P3  Fristenberechnung                  kläre gerade
  ⊘ P4  Bescheiderstellung                 blockiert: Signaturverfahren
```

Vault nach jedem abgeschlossenen Ast fortschreiben — nicht erst am Ende.

### 4. Verkettung bestimmen

Bevor etwas angelegt wird, die Struktur festlegen. **Das ist der Teil, der
das ASDD-Backlog prüfbar macht** statt zu einem Haufen:

**Epics** — aus der Ebene, unter der die Pakete hängen. Bei einem Zielbild mit
Phasen sind es die Phasen; sonst die obersten `loesung`-Knoten, aus denen ≥2
Pakete entstanden sind.

Artifacture erlaubt **keine verschachtelten Epics**. Bei tieferer Rekursion
bleibt nur die eine Epic-Ebene; die Gliederung dazwischen steht im `pfad` und
in der Beschreibung.

**Reihenfolge** (`sort_order`, 10–90) — aus `braucht`. Topologisch sortieren:
Was Voraussetzung ist, bekommt die kleinere Zahl. Zyklus im Graph → melden,
nicht auflösen.

**Blockierungen** (`link_items`) — aus `braucht`, wenn die Abhängigkeit hart
ist. Weiche Zusammenhänge (`Hängt zusammen mit`) werden **nicht** verlinkt;
sie stehen in der Beschreibung.

**Priorität** (`priority`, 1–5, 1 = Critical) — nicht erfunden, sondern
abgeleitet:

| Lage | `priority` |
|---|---|
| Voraussetzung für ≥2 andere Pakete | 2 (High) |
| Löst ein Problem mit `zwang` (Regulatorik, Frist) | 2 (High) |
| Normales Paket | 3 (Medium) |
| Löst nur `mehrwert`, kein `problem` | 4 (Low) |

Hat der Nutzer im Vault oder im Dialog eigene Prioritäten gesetzt, gelten
seine. Sonst diese Ableitung — und **sag, dass sie abgeleitet ist**.

### 5. Baum vorlegen

Vor dem ersten `create_item`:

```
BAUM — Vault <name>

ENTSCHEIDUNGEN (von dir getroffen)
  W1  Erste Version nur Investitionsförderung
      Alternativen: alle 14 / generisches Modell
      Grund: Datenmodell soll am Brot-und-Butter-Fall reifen
      betraf: L3, L7, L9

EPIC L3 "Förderanträge digital bearbeiten"
  P1  Antrag anlegen mit Stammdaten        prio 2  sort 10
  P2  Anlagen hochladen (PDF, max 10 MB)   prio 3  sort 20  braucht P1
  P3  Fristenberechnung                    prio 2  sort 30  braucht P1
      → prio 2: Zwang Z2 (VwVfG-Frist)

EPIC L7 "DATEV-Export"
  P5  Export der Ausgangsrechnungen        prio 3  sort 40

OHNE EPIC (1)
  P6  Stammdatenpflege Förderprogramme     prio 2  sort 5   Voraussetzung
                                                            für P1, P5

BLOCKIERT — nicht angelegt (1)
  P4  Bescheiderstellung
      braucht Entscheidung: Signaturverfahren
      bleibt im Vault als [[B1-signaturverfahren]]

INSIGHTS (3)
  W1   Entscheidung nur Investitionsförderung  → Konsequenz: …
  Z2   Zwang VwVfG-Frist                       → Konsequenz: …
  A1   Annahme Historie reicht 3 Jahre [UNGEPRÜFT]

ADR-LÜCKEN (1)
  Dateiablage für Anlagen nirgends festgelegt → betrifft P2

NICHT GELÖST (2)
  T5.12 Zolldokumente manuell   → bewusst, siehe [[N1]]
  T9.4  Werkzeugstandzeiten     → offen, in keinem Paket

GEKLÄRT (4)
  Aufbewahrungsfrist 10 Jahre    Quelle: ADR-014
  Max. Anlagengröße 10 MB        Quelle: du
  …

Prioritäten sind abgeleitet (Voraussetzung/Zwang), nicht von dir gesetzt.
```

Freigabe abwarten. Das ist der letzte Punkt, an dem korrigiert werden kann.

### 6. Anlegen

Reihenfolge: **Epics zuerst**, dann Pakete in `sort_order`-Reihenfolge
**sequenziell** (die Feinsortierung innerhalb einer Prioritätsstufe trägt die
Anlage-Reihenfolge), dann Verlinkungen, dann Insights.

```
create_item(title=…, itemType="Epic", workflow=<aus list_workflows()>)
create_item(title=…, description=…, itemType="Story", workflow=<aus list_workflows()>,
            parentId=<epic>, priority=<1-5>)
link_items(sourceTaskId=<item>, targetTaskId=<vorgaenger>, relation="BlockedBy")
create_item(title=…, description=<Beobachtung>, itemType="Insight",
            consequence=<Folgerung>)
```

Insights bekommen **keinen** `workflow`-Parameter.

Ruf `list_workflows()` auf und ordne den Entwicklungs-Workflow über die
Statuszeilen zu (AI-Schritte für Spec und Implementierung). **Rate keinen
Namen.** Gibt es nur einen Workflow, nimm ihn und sag es.

Jede Rückgabe prüfen (`item_id`, `initial_status`, `workflow`). Landet etwas
im falschen Workflow: stopp und melden, nicht weiterpushen.

### 7. Vault zurückschreiben

Jedes angelegte Paket: `stand: angelegt`, `item_id: …`.
`_arbeit.md` auf `stand: abgeschlossen` — oder `laufend`, wenn blockierte
Äste offen sind, mit dem, was zu tun ist.

### 8. Bericht

- angelegte Epics, Items, Insights mit IDs
- **blockierte Äste** und was sie brauchen
- **ADR-Lücken** — die wichtigste Zeile: fehlende Architekturentscheidungen
  sind jetzt billig und beim Implementieren teuer
- **nicht gelöste Probleme** — bewusst (mit Begründung) und offen (ohne)
- abgeleitete Prioritäten, als abgeleitet gekennzeichnet
- Widersprüche zu ADRs

Dann: Die Items liegen im ASDD-Backlog und warten auf menschliche Prüfung.

## Regeln

- **Die Prüffrage steht am Anfang jedes Durchgangs.** Nicht raten, ob etwas
  klein genug ist — fragen, ob eine Spec daraus entstehen kann.
- **Absenken entscheidet der Mensch.** Immer. Wege vorschlagen: ja. Einen
  wählen: nein.
- **Im Zweifel Entscheidung statt Information.**
- **Fragen bündeln.** Dieselbe Frage an vier Knoten ist eine Frage.
- **Nichts erfinden.** Was nicht im Vault, in den ADRs oder in einer Antwort
  steht, entsteht hier nicht — es wird gefragt oder gemeldet.
- **ADRs sind bindend.** Eine Frage, die ein ADR beantwortet, wird nicht
  gestellt. Ein Weg, der ein ADR verletzt, wird nicht vorgeschlagen.
- **ADR-Lücken melden, nicht füllen.**
- **Die IST-Ebene wird nicht verändert.** Keine Knoten löschen, keine
  umschreiben. Fehlt einer, wird er als `typ: eigen` ergänzt.
- **Frühere Entscheidungen nicht still korrigieren.** Melden.
- **Jedes Paket trägt `pfad` und `loest`** — Herkunft mit Originalzitat.
  Ohne sie ist der Bezug zur Quelle verloren.
- **Prioritäten sind abgeleitet, nicht geschätzt** — und werden als abgeleitet
  gekennzeichnet. Keine Aufwandsschätzung.
- **Vault nach jedem Ast fortschreiben**, nicht erst am Ende.
- **Freigabe vor dem ersten `create_item`.**

## Interaktionsstil

- Deutsch als Default.
- Beim Absenken vollständig vorlegen, dann warten. Der eine Moment, in dem
  Gründlichkeit vor Kürze geht.
- Sonst knapp: nach jedem Ast drei Zeilen Stand.
- Der Baum steht am Ende, nicht laufend im Verlauf.
