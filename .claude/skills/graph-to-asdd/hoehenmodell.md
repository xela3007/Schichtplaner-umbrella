# Höhenmodell

Das gemeinsame Vokabular für die Frage: **Wie weit ist ein Item noch von der
Umsetzung entfernt — und was genau fehlt?**

Skills, Workflows und Menschen müssen dieselbe Sprache dafür sprechen. Ohne
dieses Dokument reden sie über verschiedene Dinge und nennen es gleich.

---

## Das Problem, das es löst

Zwei echte Sätze aus einem Projekt:

> „Wir brauchen eine Plattform für Wirtschaftsförderer."

> „Der Save-Button auf Seite XY unten rechts muss von grün zu blau."

Beides sind gültige Anforderungen. Beide landen im selben Backlog. Der
Unterschied zwischen ihnen ist **nicht Größe** — er ist, wie weit der
Lösungsraum noch offen steht.

Das ist die Achse, um die es geht, und Menschen denken nicht in ihr. Sie
reden über Probleme und über mögliche Lösungsansätze, kreuz und quer über
alle Höhen hinweg. Der Graph dedupliziert und destilliert das; danach muss
jedes Detail einsortiert werden.

**Ein erfahrener Entwickler macht das intuitiv.** Er sieht ein Item und weiß,
ob er anfangen kann. Was er dabei tut, ist die Höhe zu erkennen — und genau
das muss der Mechanismus leisten, damit die Plattform auch für jemanden
funktioniert, der diese Intuition nicht hat.

---

## Die Höhenachse

| Stufe | Name | Beispiel | Was fehlt zur Umsetzung |
|---|---|---|---|
| **H4** | Domäne | „Plattform für Wirtschaftsförderer" | Alles. Niemand weiß, was gebaut wird. |
| **H3** | Fähigkeit | „Förderanträge digital bearbeiten" | Welche Schritte, welche Rollen, welche Daten |
| **H2** | Vorgang | „Antrag einreichen mit Anlagen" | Feldliste, Validierung, Fehlerfälle |
| **H1** | Arbeitspaket | „Upload-Feld für PDF-Anlagen, max 10 MB" | Nichts Fachliches — ASDD kann laufen |
| **H0** | Anweisung | „Save-Button grün → blau" | Nichts. Es ist bereits die Lösung. |

**H1 ist das Ziel.** Nicht H0: Eine Anweisung nimmt ASDD die Spec-Arbeit weg,
für die es gebaut ist. Wer auf H0 formuliert, hat die Lösung selbst
entschieden — manchmal richtig (ein Bugfix, eine Farbänderung), meistens zu
früh.

---

## Die zweite Achse: Breite

Höhe allein reicht nicht, weil sie eine zweite Frage nicht beantwortet:
*Wie viele gleichartige Dinge stehen hier nebeneinander?*

„Alle 47 Buttons im Altsystem auf das neue Farbschema umstellen" ist **H0 und
sehr breit**. Es ist riesig an Aufwand und trotzdem nichts zu entscheiden.

Das ist der Grund für zwei Achsen statt einer:

- **Höhe erzeugt Ebenen.** Absenken heißt, den Lösungsraum einzuschränken —
  und dabei entstehen neue, tiefere Items.
- **Breite erzeugt Geschwister.** Aufteilen heißt, gleichartige Dinge
  nebeneinanderzustellen — die Höhe ändert sich dabei nicht.

Sie zu vermischen ist der häufigste Fehler. „Das Item ist zu groß" kann beides
bedeuten und verlangt verschiedene Antworten: Bei Höhe muss jemand
**entscheiden**, bei Breite reicht **zerlegen**.

**Beides erzeugt Items.** Der Unterschied ist nicht, *ob* etwas entsteht,
sondern ob dabei jemand **gewählt** hat. Absenken schließt Möglichkeiten aus,
die vorher offen standen — deshalb braucht es einen Menschen. Aufteilen
sortiert nur, was ohnehin drin war.

---

## Die Matrix

|  | **schmal** | **breit** |
|---|---|---|
| **H4–H3** *(hoch)* | **Entscheiden** — erzeugt die nächste Ebene | **Entscheiden, dann gruppieren** — sonst 20 Geschwister auf einmal |
| **H2** *(mittel)* | **Klären** — offene Fragen, keine neue Ebene | **Klären, dann aufteilen** |
| **H1–H0** *(niedrig)* | **Durchreichen** → ASDD | **Bündeln** → ein ASDD-Item, N-mal ausgeführt |

Nur die **obere Zeile schränkt den Lösungsraum ein** — und nur sie braucht
deshalb einen Menschen. Das ist der Grund, warum niemand die Tiefe vorher
kennt, und warum das kein Problem ist:

**Vorher weiß es niemand. Nach jedem Schritt weiß man es für diesen Ast.**

Der Mechanismus muss die Tiefe nicht vorhersagen. Er muss pro Item *eine*
Frage beantworten können — immer wieder dieselbe.

### Die Bewegung ist ein Kreisel, keine Treppe

Es wäre bequem, sich das als Abstieg vorzustellen: H4 → H3 → H2 → H1, fertig.
So läuft es nicht. Jedes Item geht nach *jeder* Operation erneut in die
Prüffrage, und alle diese Wege kommen vor:

- Eine **Klärung** deckt auf, dass die Anforderung sehr breit ist → aufteilen
- Ein **aufgeteiltes Stück** wirft eine Frage auf, die am Ganzen unsichtbar
  war → klären
- Eine **Klärung** zeigt, dass zwischen zwei Wegen nie jemand gewählt hat →
  absenken
- Nach einer **Absenkung** ist ein Kind sofort fertig, ein anderes braucht
  drei weitere Runden

Der Vorgang endet trotzdem, weil jede Operation entweder etwas Offenes
schließt oder das Item verkleinert — nicht, weil er in eine Richtung läuft.

---

## Die Höhe messen: die ASDD-Frage

Es gibt genau eine Prüffrage, und sie ist für jeden prüfbar, ohne die
Höhenstufen zu kennen:

> **Könnte ASDD daraus ohne Rückfrage eine Spec schreiben?**

- **Ja** → H1. Durchreichen.
- **Nein** → *Was genau fehlt?* Und die Antwort **ist** der nächste Schritt.

Die Antwort fällt immer in eine von drei Kategorien:

| Was fehlt | Höhe | Was zu tun ist |
|---|---|---|
| Eine **Entscheidung** — mehrere Wege sind offen, keiner ist gewählt | hoch (H4–H3) | **Absenken**: entscheiden, erzeugt neue Ebene |
| Eine **Information** — der Weg ist klar, Details fehlen | mittel (H2) | **Klären**: Frage beantworten, gleiche Ebene |
| **Nichts** — es sind nur zu viele auf einmal | niedrig | **Aufteilen**: Geschwister, gleiche Ebene |

Diese Zuordnung ist der ganze Mechanismus. Sie braucht keine Erfahrung, nur
die Fähigkeit zu sagen, was fehlt.

### Warum diese Frage und nicht eine Höhenskala

Eine Skala müsste man lernen und für jedes Projekt neu eichen. Die ASDD-Frage
ist **konkret und überprüfbar**: Sie fragt nach einem Ereignis, das später
tatsächlich eintritt. Wer sie falsch beantwortet, merkt es spätestens, wenn
ASDD zurückfragt — und das ist ein Feedback, das eine Skala nicht hat.

Der Preis: Sie gibt **keine Vorschau**, wie tief es noch geht. Man sieht immer
nur eine Stufe weit. Das ist verkraftbar, weil die Alternative — Tiefe
schätzen — ohnehin nicht funktioniert.

---

## Absenken ist eine menschliche Entscheidung

Der wichtigste Satz dieses Dokuments:

**Wo eine Entscheidung fehlt, entscheidet ein Mensch — nicht der Skill.**

Beim Absenken wird der Lösungsraum eingeschränkt. Das ist Produktarbeit: Aus
„Förderanträge digital bearbeiten" wird ein bestimmter Zuschnitt, und andere
mögliche Zuschnitte fallen damit weg. Eine KI, die das selbst entscheidet,
trifft Produktentscheidungen unter der Tarnung von Aufbereitung — und niemand
sieht es, weil das Ergebnis aussieht wie alles andere im Backlog.

**Klären und Aufteilen** sind dagegen Ausführung: Die Frage ist gestellt, der
Weg steht fest. Das läuft autonom.

Daraus folgt die Eingriffsregel:

| Schritt | Wer |
|---|---|
| Höhe bestimmen (ASDD-Frage) | KI schlägt vor |
| **Absenken** (entscheiden) | **Mensch** |
| Klären (Information beschaffen) | KI |
| Aufteilen (Geschwister bilden) | KI |
| Durchreichen an ASDD | KI |

---

## Wie viele Ebenen entstehen?

Unbekannt, und das ist in Ordnung. Anhaltspunkte aus der Struktur:

- Ein Item aus dem **Zielbild** (`loesung`-Knoten) startet meist auf H3–H2.
  Das Zielbild-Gespräch hat H4 bereits abgesenkt.
- Ein Item aus **`vision-capture`** startet oft auf H4–H3 — dort wurde noch
  nicht entschieden.
- Ein **Bug** oder eine Änderungsanweisung startet auf H1–H0 und geht direkt
  durch.

Ein Ast, der mehr als drei Absenkungen braucht, ist ein Warnsignal: Entweder
wurde zu klein abgesenkt (jede Ebene bringt zu wenig Einschränkung), oder das
Item war in Wahrheit ein Thema und kein Item.
