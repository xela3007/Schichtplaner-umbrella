# Willkommen bei Schichtplaner

Dieses Repo wurde via `artifacture-bootstrap` aufgesetzt. Du arbeitest hier
nicht klassisch mit Issues und Tickets, sondern mit **Items**, die durch
konfigurierbare **Workflows** laufen — gesteuert über den Artifacture
MCP-Server, der direkt in Claude Code eingehängt ist.

**Modus:** fasttrack · **Katalog-Version:** 0.6.0

Was das heißt, steht in `CLAUDE.md`. Kurzfassung: bei `fasttrack` entscheidet
Claude entlang der ADRs und fragt wenig; bei `advanced` sind technische
Rückfragen normal.

---

## So fängst du an

### 1. Claude Code neu starten

Damit Skills und MCP-Server in diesem Ordner geladen werden, schließe die
Session und öffne sie wieder im Repo-Root.

### 2. Eine Story im Board freigeben

Das ist der Schritt, der am leichtesten übersehen wird — und ohne ihn passiert
hier nichts.

Eine Story wird für KI-Arbeit erst sichtbar, wenn **beides** stimmt:

1. Sie ist **dir zugewiesen**
2. Sie steht in einem Schritt, der **auf KI wartet** — nicht in einem
   Human-Review-Schritt

Beides stellst du im Artifacture-Board ein. Fang mit `Umbrella-Repo &
ADR-Grundgerüst` an; die anderen Stories bauen darauf auf.

### 3. Erste Frage an Claude

> *"Was steht an?"*

Claude ruft dann `list_actionable_items()` auf. **Von allein läuft nichts** —
du musst fragen.

Kommt nichts zurück, liegt es fast immer an Schritt 2: nicht zugewiesen, oder
im falschen Schritt. Claude sagt dir dann, was es im Board sieht und woran es
hängt.

### 4. Wenn du über das Produkt reden willst

Der Bootstrap hat bewusst **keine** fachlichen Entscheidungen getroffen. Er
hat nur die Struktur gebaut.

Fang einfach an zu erzählen, was das Produkt können soll — du musst keinen
Befehl kennen. Claude erkennt das Produkt-Gespräch und sortiert mit:

- **Ideas** — Dinge, die man bauen könnte. Werden im Planning-Workflow zu
  ausgearbeiteten Stories.
- **Insights** — Projektwissen, das erklärt *warum* etwas so sein muss
  ("die Vertriebler arbeiten auf dem Tablet beim Kunden" → jede Maske muss
  ohne Tastatur bedienbar sein). Das musst du nie wieder erzählen; es taucht
  bei jeder Planung als Kontext auf.

Bevor etwas angelegt wird, siehst du die Einordnung und kannst widersprechen.

---

## Was Artifacture für dich tut

Artifacture ist kein Ticket-System, sondern eine **Workflow-Engine**. Jedes
Item hat einen aktuellen Schritt, und jeder Schritt enthält klare Anweisungen
— für dich, für Claude, oder für beide.

Welche Workflows in **diesem** Projekt aktiv sind, fragst du direkt:

> *"Welche Workflows gibt es hier?"* (→ `list_workflows`)

Die Bootstrap-Stories liegen auf zwei Workflows: die Struktur-Stories dort,
wo KI sie direkt spezifizieren und umsetzen kann, und das Purpose-Gate dort,
wo zuerst ein Mensch draufschaut.

---

## Ordnerstruktur

```
Schichtplaner/
  ADR/             Architecture Decision Records — bindend
  Docs/            Diagramme, Notizen, Vision-Dokumente
  src/             Code-Repo(s) — eigene Git-Historie, hier gitignored
  CLAUDE.md        Anweisungen an Claude Code
  WELCOME.md       Diese Datei
  bootstrap.lock   Katalog-Version + Modus
```

Dieses Repo ist das **Umbrella**: es trägt Entscheidungen und Dokumentation,
keinen Anwendungscode. Der Code liegt in einem eigenen Repo unter `src/` und
wird separat geklont — `get_setup_script` stellt den Baum idempotent her.

`ADR/` ist **nicht leer** — dort liegen die Architektur-Entscheidungen aus
dem Bootstrap-Intake. Sie sind bindend: jede Spec und jede Implementierung
muss dazu passen. Willst du eine davon ändern, ändere das ADR selbst und
vermerke die Änderung mit Datum (z. B. `Status: accepted, geändert
JJJJ-MM-TT`); was nicht mehr gilt, raus aus `ADR/` (siehe check-adr RULES
A4).

`Docs/` ist für Diagramme, Notizen und Transkripte — alles, was Menschen
lesen. Produkt-Erkenntnisse gehören **nicht** hierher, sondern als Ideas und
Insights aufs Board: dort werden sie bei der Planung tatsächlich gefunden.

---

## Wichtige Spielregeln

1. **Workflow zuerst.** Bevor irgendwas gebaut wird, beansprucht Claude das
   Item mit `claim_task` und ruft dann `get_current_task` dafür auf
   (`list_actionable_items` → `claim_task` → `get_current_task` →
   `complete_task`). Die Anweisung dort ist die Quelle der Wahrheit.
   Solange eine Session ein Item beansprucht hat, arbeitet keine andere
   daran; im Board kannst du einen Claim lösen.
2. **Items wandern automatisch.** Niemand verschiebt Items manuell;
   `complete_task` rückt den Workflow vor.
3. **Blockaden melden.** Geht etwas nicht weiter → `report_blocker`, statt
   still im Sand zu verlaufen.
4. **ADRs sind verbindlich.** Sie sind harte Constraints für jede Spec und
   jeden Code-Change.
5. **Kein Auto-Commit.** Claude lässt Änderungen liegen, du entscheidest,
   was committet wird.

---

## Hilfreiche Einstiegsfragen an Claude

- *"Was kann ich tun?"* → Liste offener Items
- *"Welche Workflows gibt es hier?"* → Workflow-Übersicht
- *"Was ist Item X?"* → Details + aktueller Schritt
- *"Suche nach Items zum Thema Y"* → Volltext-Suche
- *"Welche ADRs gelten hier?"* → die Bootstrap-Entscheidungen

---

## Wenn was nicht klappt

- **Claude kennt `artifacture` nicht?** → Claude Code wurde nicht neu
  gestartet, oder die MCP-Anbindung fehlt.
- **MCP-Server antwortet mit 401/403?** → Zugang ungültig oder abgelaufen;
  beim Projekt-Owner neu anfordern.
- **`get_current_task` meldet `instruction: "This step requires human
  action…"` oder `error: not_assigned…`?** → Das Item wartet auf einen
  Menschen (z.B. Human Review oder Zuweisung). Anderes Item nehmen.
- **`claim_task` meldet `already_claimed`?** → Eine andere Session arbeitet
  gerade an dem Item. Anderes Item nehmen.

Viel Erfolg.
