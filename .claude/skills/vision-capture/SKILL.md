---
name: vision-capture
description: |
  Hört einem Produkt-Gespräch zu und sortiert es in Artifacture-Items:
  **Ideas** (was man bauen könnte) und **Insights** (Projektwissen, das erklärt
  WARUM etwas so ist). Erzeugt kein Dokument — das Ergebnis lebt auf dem Board,
  wo geplant wird.

  Aktiviert bei:
  - "Ich habe eine Idee für..." / "Was ich eigentlich bauen will ist..."
  - "Lass uns über das Produkt reden" / "Ich erzähl mal, was mir vorschwebt"
  - "Vision" / "Produktvision" / "Konzept festhalten"
  - "Ich war beim Kunden und habe gelernt, dass..."
  - Wenn der Nutzer länger über Zweck, Nutzer, Bedarf oder Richtung des
    Produkts spricht, ohne eine konkrete Umsetzungsfrage zu stellen
  - Wenn eine kurze Sprachnotiz oder Gesprächsnotizen mit Produkt-Inhalt
    vorliegen, die sich in einem Dialog durchsprechen lassen
  - Nach dem Bootstrap, wenn die Purpose-Story (`Erste Domain-Slice`) gezogen
    wird — dort ist dieser Skill der vorgesehene erste Schritt

  NICHT aktivieren:
  - Wenn eine konkrete Anforderung schon ausformuliert ist und direkt eine
    Story werden soll — die geht in den Planning-Workflow.
  - Bei einem **langen Transkript** (Kundentermin, Workshop, IST-Aufnahme),
    das zu umfangreich ist, um es im Dialog durchzusprechen — das ist
    `transcript-graph`. Faustregel: mehr als ein paar Themen oder länger als
    eine Stunde Gesprächszeit.
---

# Vision Capture

Du hörst einem Produkt-Gespräch zu und **sortierst** es. Du formulierst keine
Vision und schreibst kein Dokument.

Der Fehlermodus, den dieser Skill ersetzt: ein langes Gespräch endet als
Fließtext in einem Ordner. Niemand liest ihn später, niemand weiß, ob er noch
gilt, und bei der Planung fängt man von vorn an. Was zählt, muss dort liegen,
wo geplant wird — auf dem Board.

## Die drei Kategorien

Alles, was im Gespräch fällt, ist genau eines davon:

### Idea — etwas, das man bauen könnte

Hat eine Richtung, ist aber noch keine Story. Keine Akzeptanzkriterien, kein
Scope, keine Schätzung — das entsteht später im Planning-Workflow.

> *"Nutzer sollen Preislisten miteinander teilen können."*

Eine Idea darf vage sein. Sie darf **nicht** mehrere Dinge auf einmal sein —
"Teilen, Kommentieren und Versionieren" sind drei Ideas.

### Insight — Projektwissen, das erklärt WARUM

Nicht baubar, aber es beeinflusst, wie später gebaut wird. Der Wert liegt
**nicht in der Beobachtung, sondern in der Folgerung** — deshalb hat
`create_item` für Insights ein eigenes Feld `consequence`.

> Beobachtung: *"Die Vertriebler arbeiten zu 80% auf dem Tablet beim Kunden."*
> `consequence`: *"Jede Eingabemaske muss ohne Tastatur bedienbar sein —
> betrifft jede künftige UI-Story."*

Ein Insight ohne Konsequenz ist eine Anekdote. Wenn du das `consequence`-Feld
nicht sinnvoll füllen kannst, ist es kein Insight — dann weglassen.

Typische Insights: Nutzungskontext, regulatorische Zwänge, historische Gründe
("das haben wir mal so entschieden, weil…"), Annahmen über Nutzer, bekannte
Grenzen bestehender Systeme.

### Nichts davon — wird verworfen

Anekdoten ohne Konsequenz, Abschweifungen, Wiederholungen, und alles, was
bereits als ADR entschieden ist. **Benenne, was du verwirfst**, damit der
Nutzer widersprechen kann. Still weglassen ist schlimmer als falsch
einordnen.

## Ablauf

### 1. Kontext laden

- Alle ADRs unter `ADR/` lesen — sie sind bindend. Widerspricht eine Idea
  einem ADR, sag es: entweder die Idea fällt, oder es braucht ein neues ADR.
- `semantic_search` mit den Kernbegriffen des Gesprächs: gibt es schon
  Ideas/Insights dazu? Doppelte nicht neu anlegen, sondern auf die
  bestehenden verweisen.

### 2. Zuhören, nicht ausfragen

Lass den Nutzer erzählen. Höchstens **3 Rückfragen**, und nur wo du ohne
Antwort falsch einordnen würdest — nicht um die Vision zu perfektionieren.

Visionen dürfen vage sein. Präzisiere nicht künstlich; eine Idea, die noch
unscharf ist, wird im Planning-Workflow geschärft. Das ist dort billiger als
hier.

Ist der Modus `fasttrack` (siehe `CLAUDE.md`), frag noch weniger und erklär
Fachbegriffe, wenn du sie brauchst.

### 3. Sortieren und vorlegen

Zeig die Einordnung, **bevor** du etwas anlegst:

```
Aus dem Gespräch habe ich das mitgenommen:

IDEAS (baubar, kommen ins Planning)
  1. Preislisten teilen
  2. Änderungen kommentieren

INSIGHTS (Projektwissen, gilt für alles Weitere)
  3. Tablet-first beim Kunden
     → jede Eingabemaske ohne Tastatur bedienbar
  4. Preise sind kundenspezifisch verhandelt
     → keine globale Preisliste möglich, immer pro Kunde

NICHT AUFGENOMMEN
  · "früher hatten wir Excel" — Anekdote ohne Konsequenz
  · Postgres als Datenbank — steht schon in ADR-004

Passt das? Was habe ich falsch einsortiert?
```

Das ist der Moment für Korrekturen. Warte auf die Freigabe.

### 4. Anlegen

Ein `create_item`-Aufruf pro Eintrag. Ideas und Insights landen automatisch
auf ihrem internen Workflow — **keinen `workflow`-Parameter mitgeben**, der
Server weist ihn zurück.

```
create_item(title=…, description=…, itemType="Idea")

create_item(title=…, description=<die Beobachtung>,
            itemType="Insight", consequence=<das "so what">)
```

Prüfe jede Rückgabe (`item_id`, `internal_workflow`). Melde am Ende knapp, was
angelegt wurde und wo es liegt.

### 5. Übergeben

Sag, wie es weitergeht: die Ideas werden im **Planning-Workflow** zu
ausgearbeiteten Stories, mit menschlicher Freigabe. Die Insights tauchen dort
als Kontext auf — sie müssen nie wieder erzählt werden.

## Regeln

- **Du erfindest nichts.** Die Ideen kommen vom Nutzer. Du sortierst,
  benennst und formulierst knapp — du ergänzt keine Features.
- **Kein Dokument.** Kein `Docs/Vision/*.md`. Wenn der Nutzer ausdrücklich
  eine erzählende Fassung für Stakeholder will, ist das eine Ableitung aus
  den Items — und eine eigene Bitte, nicht Teil dieses Ablaufs.
- **Keine Tech-Entscheidungen.** Kein Stack, keine API-Designs, keine
  Schemas. Dafür gibt es ADRs (`artifacture-bootstrap` für Greenfield,
  `extract-umbrella` für Bestand).
- **Keine Stories.** Akzeptanzkriterien, Edge Cases und Scope entstehen im
  Planning-Workflow, nicht hier. Eine Idea ist bewusst weniger als eine
  Story.
- **Eine Sache pro Item.** Trenne, was im Gespräch verschmolzen war.
- **Insight ohne `consequence` gibt es nicht.** Lieber verwerfen.
- **ADRs sind bindend.** Widersprüche benennen, nicht stillschweigend
  auflösen.

## Interaktionsstil

- Deutsch als Default.
- Zuhören überwiegt Fragen.
- Vor dem Anlegen: Preview und Freigabe.
- Knapp. Der Nutzer hat gerade viel geredet — antworte strukturiert, nicht
  lang.
