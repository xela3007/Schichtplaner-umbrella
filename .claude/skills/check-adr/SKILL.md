---
name: check-adr
description: |
  Prüft die ADRs eines Umbrella-Repos gegen ein festes Regelset, **verdichtet
  sie** auf das, was tatsächlich gilt, und meldet, was nicht trivial
  entscheidbar ist.

  Kein reiner Linter: Der Skill repariert Formverstöße selbst, wirft
  Prosa und Nachschlag-Gründe raus, und legt nur die Fälle vor, die eine
  Entscheidung brauchen.

  Aktiviert bei:
  - "ADRs prüfen" / "check-adr" / "ADR-Review"
  - "sind die ADRs sauber?" / "ADRs komprimieren"
  - "ADRs verdichten" / "Token sparen bei den ADRs"
  - "gibt es Widersprüche in den ADRs?"
  - Nach einem Bootstrap, bevor die ersten Stories laufen
  - Wenn ein ADR geändert wurde und der Rest gegengeprüft werden soll

  NICHT aktivieren für Drift gegen den Code ("tut der Code, was das ADR
  sagt?") — das ist ein eigener Skill.
---

# check-adr

## Wofür das hier gut ist

Zwei Probleme, ein Skill:

**1. ADRs entstehen zu lang und zu weich.** Generiert oder handgeschrieben —
sie enthalten Prosa, Begründungen, die niemand braucht, offengelassene
Optionen und Statuszeilen, die Nichtgeltung behaupten. Danach räumt jemand
händisch auf.

**2. Jedes Wort im ADR-Ordner kostet Kontext.** ADRs sind bindend, also
werden sie gelesen — bei jeder Story, in jeder Session. Ein ADR-Ordner mit
2000 Wörtern belastet jedes Kontextfenster des Projekts.

> **Ziel: die wichtigen Informationen parat, den Kontext so wenig belastet wie
> möglich.**

Die Regeln sind das Werkzeug dafür, nicht der Zweck. Ein ADR, das kürzer
wird, ohne eine Festlegung zu verlieren, ist der Erfolgsfall.

Die Prüfgrundlage steht in **`RULES.md`** — lies sie, bevor du prüfst. Sie
beginnt mit Regel 0, und ohne Regel 0 prüfst du Symptome ohne Maßstab.

## Was der Skill tut — in dieser Reihenfolge

```
1. Lesen        alle ADRs + Regelset
2. Prüfen       jedes ADR gegen A–D
3. Verdichten   C-Verstöße reparieren, B6-Inhalt umsiedeln
4. Melden       A, B, D als Findings
5. Vorlegen     was Entscheidung braucht, mit Vorschlag
```

### Wo die Ersparnis wirklich herkommt

Gemessen am BOCK-Repo (10 ADRs, ~2970 Token):

| Quelle | Anteil |
|---|---|
| `compile_adr.py` — mechanisch (Metazeilen, Floskeln) | **~3 %** |
| Inhaltliche Arbeit des Skills (C3, A7, B5, B6, Konsequenzen) | **der ganze Rest** |

**Erwarte nichts vom Skript.** Es ist Messgerät und Sicherheitsnetz, kein
Minifier — bei ADRs, die schon in Stichpunktform vorliegen, findet es fast
nichts. Die Arbeit liegt bei dir, und sie besteht aus Entscheidungen: Ist
dieser Grund eine Absperrung oder Nachschlagwerk? Ist diese Zeile eine
Festlegung oder Projektkontext? Hat dieser Inhalt überhaupt
Bindungswirkung?

---

## Schritt 1: Lesen

```
ADR/*.md
```

Liegt kein `ADR/` vor, ist das kein Fehler dieses Skills — sag es und höre
auf. Prüfe **nicht** `Docs/adr-archiv/`: Was dort liegt, gilt bewusst nicht
(A3), und es zu lesen würde es zurück in den Kontext holen.

Miss vorher den Umfang, damit die Verdichtung am Ende belegbar ist:

```bash
wc -w ADR/*.md
```

## Schritt 2: Prüfen

Jedes ADR gegen `RULES.md`, in der Reihenfolge A → D. Notiere pro Verstoß:
Datei, Zeile, Regel, was konkret dort steht.

**Wichtig bei A2/A6:** Suche nach der Bedeutung, nicht nach Stichwörtern.
"gilt bis wir mehr wissen" verstößt gegen A6, auch ohne das Wort
"vorläufig". Umgekehrt ist "vorläufige Zahlen im Report" eine fachliche
Festlegung und kein Verstoß — das Wort steht dort in anderer Funktion.

## Schritt 3: Verdichten

Diese Änderungen führst du selbst aus:

| Regel | Was du tust |
|---|---|
| **C1** | Fließtext-Absatz → Stichpunkte. Eine Festlegung pro Punkt |
| **C2** | Stichpunkt über zwei Zeilen → kürzen, außer er ist ein Absperr-Grund |
| **C3** | **Nachschlag-Gründe streichen.** Absperr-Gründe behalten |
| **C4** | Lehrbuch-Absätze streichen |
| **C5** | Über 12 Festlegungen → melden, nicht kürzen (das ist inhaltlich) |
| **B5** | Festlegung, die nur den Kopf wiederholt → streichen |
| **B6** | Inhalt ohne Bindungswirkung → **umsiedeln**, nicht löschen |

### Umsiedeln statt löschen (B6)

Bedienwissen, Zugangswege, Kontodaten, Präferenzen ohne Folge — das ist nicht
wertlos, nur am falschen Ort. Es gehört nach `Docs/` oder in `CLAUDE.md`.

**Nie stillschweigend wegwerfen.** Nenne im Bericht, was du wohin verschoben
hast. Wer sein Bedienwissen unkommentiert verliert, vertraut dem Skill beim
nächsten Lauf nicht mehr.

### Die C3-Entscheidung ist die wichtigste

Prüffrage für **jeden** Grund im ADR:

> *Würde jemand diese Festlegung für einen Fehler halten und "reparieren"?*

**Ja** → Grund bleibt, auch zwei Zeilen lang. **Nein** → weg.

Bei Unsicherheit: **behalten und in den Bericht als Frage aufnehmen.** Ein zu
viel behaltener Grund kostet ein paar Token. Ein zu viel gestrichener kostet
jemandem einen halben Tag Fehlersuche.

### Was du beim Verdichten NIE tust

- **Keine Festlegung entfernen.** Auch keine, die dir überflüssig vorkommt —
  das ist eine inhaltliche Entscheidung (Schritt 5)
- **Keine Festlegung umformulieren**, sodass sich ihre Bedeutung ändert
- **Keine A- oder B-Verstöße "reparieren".** Dort würdest du Entscheidungen
  treffen, die dem Team gehören
- **Nichts zusammenführen** über ADR-Grenzen hinweg (D2 ist ein Finding, keine
  Aktion)

Nach dem Verdichten: `wc -w ADR/*.md` erneut, und die Ersparnis im Bericht
nennen. Zahlen sind der Beweis, dass es sich gelohnt hat.

## Schritt 4: Melden

A-, B- und D-Verstöße als Findings, blockierende zuerst. Je Finding:

- **Datei und Zeile**
- **Regel** (A6, D1, …)
- **Was dort steht** — wörtlich, kurz
- **Warum das bricht** — bei A-Regeln immer der Durchgriff auf Regel 0
- **Was zu tun ist** — konkret, nicht "überarbeiten"

Ein Finding ohne konkreten Vorschlag ist halbe Arbeit.

## Schritt 5: Vorlegen, was Entscheidung braucht

Alles, was nicht trivial entscheidbar ist, kommt hierher — mit **Vorschlag**,
nicht als offene Frage:

- **A7-Auflösung** (siehe unten) — der häufigste Fall
- **D1-Widersprüche**: Welches ADR ist falsch? Nie beide "irgendwie"
  anpassen
- **D2-Doppelzuständigkeit**: Wo gehört es hin?
- **C5-Überschreitung**: ADR aufteilen oder Festlegungen streichen?
- **C3-Zweifelsfälle**: Grund behalten oder raus?

Formuliere jeden Punkt so, dass eine Ein-Wort-Antwort genügt. "Soll X nach
ADR-004 oder ADR-006?" ist beantwortbar. "Wie wollen wir mit X umgehen?"
nicht.

---

## A7-Auflösung: der häufigste Fall

Ein "Offen"-Block enthält fast immer **zwei verschiedene Dinge**. Trenne sie,
bevor du meldest:

| Was es wirklich ist | Erkennungsmerkmal | Wohin |
|---|---|---|
| **Festlegung im falschen Abschnitt** | Steht schon eine Aussage drin, die gilt | Nach oben zu den Festlegungen — **das kannst du selbst** |
| **Echte offene Frage** | Es ist nichts entschieden | Ins Board, und **raus aus dem ADR** — das legst du vor |
| **Verweis ohne Inhalt** | "→ Planning", "→ Backlog" | Raus. Der Verweis trägt keine Information, die im ADR wirken darf |

**Beispiel aus der Praxis** (ADR-005 in diesem Repo):

```markdown
## Offen (nicht hier entschieden)
- Ausgestaltung des Einladungssystems → Planning          ← Verweis, raus
- Welche Rechte die Default-Rolle trägt → fachlich        ← Verweis, raus
- MFA, SSO/SAML, Session-Dauer im Fachbetrieb             ← echte Frage → Board
- **Verifizierte Absender-Domain bei Resend.** Der Default
  `onboarding@resend.dev` funktioniert nur für Tests      ← FESTLEGUNG!
```

Der letzte Punkt ist keine offene Frage, sondern eine Festlegung mit
Absperr-Grund im falschen Abschnitt. Er gehört nach oben — und genau das
leistet die Regel: Sie zwingt zur Trennung.

**Die dritte Zeile ist der gefährliche Fall.** "MFA, SSO/SAML" im Kontext
kann ein LLM als "hier ist Spielraum" lesen. Deshalb raus, nicht umsortieren.

---

## Ausgabeform

Zuerst die **Verdichtung**, weil sie das Ergebnis ist:

```
## Verdichtet

| ADR | vorher | nachher | gestrichen |
|---|---|---|---|
| 005-auth | 465 W | 380 W | 3 Nachschlag-Gründe, 1 Lehrbuch-Absatz |
| 009-deployment | 545 W | 470 W | 2 Prosa-Absätze → Stichpunkte |

Gesamt: 2291 → 1980 Wörter (−14 %)
Keine Festlegung entfernt.
```

Dann die Findings, blockierende zuerst. Dann die Entscheidungen.

Zum Schluss ein Satz, der die Lage zusammenfasst — nicht "4 Findings
gefunden", sondern was das bedeutet: *"Ein A7-Verstoß in 005 und ein
Widerspruch zwischen 005 und dem Konzept. Beides muss weg, bevor die
Auth-Story läuft."*

## Das Skript

```bash
scripts/compile_adr.py --check ADR/    # messen, nichts ändern
scripts/compile_adr.py --diff  ADR/    # zeigen, was passieren würde
scripts/compile_adr.py         ADR/    # schreiben (in-place)
scripts/compile_adr.py --check ADR/005-auth.md   # einzelnes ADR
```

**In-place, kein Kompilat.** Zwei Fassungen derselben Entscheidung wären zwei
Dinge im Kontext, und welches gewinnt, ist Zufall — Regel 0. Genau dieser
Fehler steckte im BOCK-Repo: ADR-002 wurde auf `#shared/*` korrigiert,
ADR-003 und ADR-007 nannten weiter `@shared/*`.

**Es bricht ab, wenn Inhalt verloren geht.** Das ist seine wichtigste
Funktion, nicht die Verdichtung. Bricht es ab, ist die Verdichtungsregel
falsch — nicht das ADR.

Vor Änderungen am Skript: `scripts/test_compile_adr.py`. Jeder Test dort hält
einen Fehler fest, der beim ersten Lauf gegen echte ADRs aufgetreten ist
(zerstörte Code-Blöcke, verlorene Einrückung, stille Löschung ganzer
Abschnitte, blinde Verifikation).

## Grenzen

- **Ändere `ADR/` nur, wenn der Nutzer den Skill ausdrücklich gestartet hat.**
  ADRs sind eine geteilte Ressource; ungefragte Änderungen sind hier
  besonders teuer
- **Kein Commit.** Änderungen bleiben im Working Directory
- **Kein Drift gegen Code** — eigener Skill
- **Keine neuen ADRs anlegen.** Fehlt eine Entscheidung, ist das ein Finding
- Läuft der Skill zum zweiten Mal, sind C-Verstöße meist weg. Melde dann
  ausdrücklich, dass nichts zu verdichten war — Stille sieht wie ein Fehler aus
