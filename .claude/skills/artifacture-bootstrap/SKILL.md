---
name: artifacture-bootstrap
description: |
  Bootstrap-Skill für neue Projekte: erzeugt aus einem leeren Ordner ein
  vollständiges Artifacture-Umbrella — Struktur (CLAUDE.md, .gitignore,
  WELCOME.md, ADR/, Docs/, src/), die Bootstrap-ADRs
  aus einem strukturellen Intake und die Skeleton-Stories direkt auf dem
  Artifacture-Board.

  Aktiviert bei:
  - "Neues Projekt" / "Projekt aufsetzen" / "bootstrap" / "greenfield"
  - "Artifacture Umbrella initialisieren" / "Setup Artifacture für mich"
  - "Lass uns X bauen", wenn noch kein Repo existiert
  - Wenn ein leerer Ordner mit Verweis auf eine Artifacture-Einladung
    geöffnet wird
  - Wenn gefragt wird, welche Stack-/Setup-Entscheidungen ein neues Projekt
    braucht — die Antwort ist dieser Katalog, keine freie Diskussion

  Ersetzt `init-artifacture-umbrella`: dieser Skill legt die Struktur an UND
  füllt `ADR/`, statt den Ordner leer zu lassen.

  Idempotent: vorhandene Dateien werden NIE ohne explizite Rückfrage
  überschrieben.
---

# Artifacture Bootstrap

Du führst die Genese eines neuen Projekts durch — von leerem Ordner bis zu
Stories auf dem Board. Das Wichtigste zuerst: **deine Aufgabe ist, Struktur
und Purpose getrennt zu halten.** Der historische Fehlermodus, den dieser
Skill verhindert: Setup-Fragen und schwammige Produkt-Vision-Fragen
vermischen sich zu einem Vier-Stunden-Sumpf und produzieren verwirrte
Stories, mit denen niemand arbeiten kann.

Deine Rolle ist absichtlich schmal: du führst einen festen strukturellen
Fragebogen (den Katalog-DAG), und alles Kreative oder Fachliche wird **an
das Board vertagt**. Du erfindest keine Stories. Stories kommen aus
`derive.py` — deterministisch, tabellengesteuert, ohne Modell-Urteil. Wenn
du den Impuls hast, eine Story hinzuzufügen, die das Mapping nicht erzeugt
hat: tu es nicht. Schlage sie nach dem Bootstrap als reguläre Backlog-Card
vor.

## Die eiserne Regel

Jede Katalogfrage ist strukturell ("braucht es eine Datenbank?"), niemals
fachlich ("worum geht es in der App?"). Wenn der Nutzer mitten im Intake
anfängt, seine Produktvision zu erklären — und das wird passieren —
antworte freundlich, merk dir **einen** Satz davon für die Purpose-Story,
und lenke zurück:

> "Das klären wir gleich sauber im Produkt-Gespräch — hier brauche ich
> nur die strukturelle Antwort."

Lass Vision-Antworten nicht beeinflussen, welche Katalog-Optionen du
wählst, über das hinaus, was der Nutzer strukturell bestätigt hat.

## Die Zielgruppe bestimmt jede Entscheidung

Dieser Skill richtet sich an Menschen, die **nicht programmieren können**
und mit Artifacture und Claude einen kompletten Stack aufsetzen und
deployen wollen. Daraus folgt die Leitregel für alles, was dieser Skill und
sein Katalog tun:

> **Komplexität, die Fehler verhindert, ist gut. Jede andere Komplexität
> gehört in den Advanced-Modus.**

Konkret: Zod-Validierung an jeder Systemgrenze ist gut, weil ein Fehler
dort mit lesbarer Meldung auffällt statt drei Schichten später als
korrupter Datensatz. Ein pnpm-Workspace mit Contract-Framework ist es
nicht — er kauft Refactoring-Sicherheit für Teams und kostet mehrere
`package.json`, die niemand pflegen kann, der nicht weiß, was ein Workspace
ist. Wende diese Regel an, wenn du je überlegst, den Katalog zu erweitern.

## Modus (Erfahrungslevel)

**Erste Frage, vor allem anderen.** Sie hängt nicht an Können, sondern
daran, wie viel der Katalog für den Nutzer entscheidet:

| Modus | Was passiert | Für wen |
|---|---|---|
| **Fasttrack** | 5 strukturelle Fragen, alles andere ist Hausmeinung | Default. Empfehlen. Intake unter 2 Minuten. |
| **Advanced** | Alle sichtbaren Nodes werden gefragt, inkl. Sprache, Repo-Form, Frontend, Realtime, Deployment | Setzt Entwicklungserfahrung voraus |
| **Nightmare** | Keine Derivation. Du zeigst die Katalogfragen als Liste zum Selbstdurchdenken und beendest den Skill | Der Witz. Wer das wählt, braucht diesen Skill nicht. |

Stelle die Frage neutral und markiere Fasttrack als Empfehlung. Wähle
**nicht** anhand deiner Einschätzung des Nutzers — er entscheidet.

Bei **Nightmare**: keine Dateien schreiben, kein `derive.py`, kein Push.
Zeige die Nodes aus `data/catalog.yaml` als Checkliste ("das sind die
Entscheidungen, die ein Projekt braucht"), verweise auf `extract-umbrella`
für den Fall, dass später doch ADRs aus dem Code entstehen sollen, und
beende freundlich.

Der gewählte Modus wandert in die `CLAUDE.md` des Umbrellas — nicht nur in
`bootstrap.lock`. Grund: `vision-capture` und die Workflow-Schritte sollen ihn
auch sehen, damit die ganze Kette gleich viel nachfragt. Der Modus ist
**kein Katalog-Node**: er produziert kein ADR, weil "ich habe Fasttrack
gewählt" nichts über die Architektur des Projekts aussagt.

## Ablauf

### Phase 1 — Modus wählen

Wie oben. Bei Nightmare: hier endet der Skill.

### Phase 2 — Brownfield-Check

Bevor irgendetwas geschrieben wird: liegt schon Code da?

```bash
ls -A                     # Ordner leer? Was ist da?
ls src/ 2>/dev/null       # Sub-Repos oder Quellcode?
```

Wenn `src/` Quellcode enthält oder das Repo eine gewachsene Codebase ist,
ist **dieser Skill der falsche**. Sag es klar und leite weiter:

> "Hier liegt bereits Code. Dann brauchst du `extract-umbrella` — der
> rekonstruiert ADRs aus dem Bestand, statt sie aus einem Fragebogen zu
> erzeugen. Sonst bekommst du ADRs, die zur Realität nicht passen."

Nicht überschreiben, nicht "beides ein bisschen". Die beiden Skills haben
disjunkte Aufgaben.

### Phase 3 — Projekt-Metadaten

Knapp, nacheinander:

1. **Projektname** — Default: Ordnername.
2. **Bestätigung des Zielordners** — *"Soll ich in `<cwd>` initialisieren?"*

**Kein Token-Handling.** Der Artifacture-MCP ist zum Zeitpunkt des
Bootstraps bereits angebunden: `.mcp.json` und `.claude/` kommen aus dem
ausgelieferten ZIP, das der Nutzer per `curl` geholt hat. Es gibt also
nichts zu schreiben und kein Token zu erfragen. Falls dir irgendwo ein
Token begegnet: **niemals loggen, niemals zurückspiegeln** — auch nicht in
Vorschauen oder Diffs.

Prüfe stattdessen, dass der MCP erreichbar ist **und auf welches Projekt er
zeigt**:

```
list_workflows()          → welche Workflows gibt es?
get_project_setup()       → welches Projekt trägt der Token?
```

Schlägt das fehl, brich mit einer verständlichen Meldung ab, statt bis Phase 8
weiterzulaufen und dort zu scheitern.

**Keine Workflows → stopp.** Liefert `list_workflows()` `count: 0`, gibt es
in diesem Projekt keinen Workflow, in den die Stories gehen könnten. Neue
Arbeitsbereiche starten ohne Workflows (ADR-020). Brich ab — vor jeder
Dateiänderung — mit genau diesem Hinweis:

> Im Arbeitsbereich gibt es noch keine Workflows. Ein TenantAdmin übernimmt
> sie unter Workflows → Store und aktiviert sie im Projekt.

Danach den Skill einfach erneut starten. Lege keinen Workflow selbst an und
rate keinen Namen — Workflows zu ändern ist App-exklusiv (ADR-034 §3).

**Wichtig:** `get_project_setup()` liefert `projectName`. Ist das ein anderes,
bereits bestehendes Projekt als das, das hier gebootstrappt wird, **stopp und
frag nach**. Der Token ist projekt-gescoped; ein Push würde sonst acht
Skeleton-Stories in ein fremdes, laufendes Board schreiben. Zeige dem Nutzer
den Projektnamen und lass ihn bestätigen, bevor irgendetwas angelegt wird.

### Phase 4 — Konflikt-Auflösung (Idempotenz)

Für jede Datei, die es schon gibt, **einzeln** fragen:

```
<datei> existiert bereits. Was soll passieren?
  (k) behalten / nicht anfassen
  (o) überschreiben mit Template
  (m) zeig mir den Diff, dann entscheide ich
```

Relevante Pfade: `CLAUDE.md`, `.gitignore`, `WELCOME.md`, `ADR/`, `Docs/`,
`src/`, `bootstrap.lock`.

**Nicht** in dieser Liste: `.claude/` und `.mcp.json`. Die kommen aus dem
ausgelieferten ZIP und sind tabu — weder überschreiben noch danach fragen.

Bei `CLAUDE.md` besonders vorsichtig: **niemals ohne explizites `o`
überschreiben.** Diff-Vorschau via `Read` und Inline-Vergleich mit dem
gerenderten Template.

Ein bereits gefülltes `ADR/` ist ein starkes Signal, dass hier schon ein
Bootstrap oder `extract-umbrella` gelaufen ist — dann zurück zu Phase 2 und
nachfragen, statt ADRs zu vermischen.

### Phase 5 — Intake entlang des DAG

Lies `data/catalog.yaml`. Stelle die Fragen in topologischer Ordnung, aber
**nur für Nodes, deren Sichtbarkeitsbedingungen die bisherigen Antworten
erfüllen** (`visible_if`, AND-Semantik). Zeige die Optionen mit markiertem
Haus-Default:

> Braucht die Anwendung eine Datenbank?
> 1. **Ja — Postgres (Neon)** ← Haus-Default
> 2. Nein — zustandslos

Akzeptiere Kurzformen ("default", "ja", "2"). Halte es knapp — das ist eine
Checkliste, keine Beratung.

Im Fasttrack-Modus werden `advanced: true`-Nodes **nicht gefragt** und
dürfen auch nicht in den Antworten auftauchen (derive.py weist das ab).
Antworte nie für unsichtbare Nodes.

Schreib die Antworten in den **Scratchpad**, nicht ins Projekt:

```json
{ "mode": "fasttrack",
  "answers": { "delivery": "web_app", "auth": "no" } }
```

Nimm nur Antworten auf, die der Nutzer tatsächlich gegeben hat — fehlende
sichtbare Nodes fallen in derive.py auf ihren Default zurück. Es landet
**kein `answers.json` im Projekt**; die Datei ist ein temporäres
Übergabeformat an das Script, kein Artefakt.

### Phase 6 — Derivation

```bash
python3 scripts/derive.py --answers <scratchpad>/answers.json --out <scratchpad>/out
```

Weist derive.py den Antwortsatz zurück, korrigiere die Antworten **mit dem
Nutzer** — arbeite nicht um die Validierung herum.

`--plan` zeigt vorab, welche Nodes sichtbar sind und welche im gewählten
Modus tatsächlich gefragt werden (`asked`). Nützlich, wenn unklar ist,
warum eine Frage nicht kommt.

### Phase 7 — Spec Review (Entscheidungen zuerst)

Das ist das Spec Review über die Architektur — der eine Moment, in dem
Purpose legitim hereinkommt. Präsentiere komprimiert:

1. **Die ADR-Entscheidungen** als kurze Liste (aus `manifest.json`),
   Abweichungen vom Default markiert.
2. **Die abgeleiteten Stories** darunter, nur Titel, in Sortier-Reihenfolge.

Rahme Zweifel richtig: fragt der Nutzer eine Story an, lautet die Antwort
immer **"welches ADR ist falsch?"** — nie Story-Prosa direkt editieren.
Antwort ändern, `derive.py` neu laufen lassen. Re-Derivation ist billig,
genau das ist der Punkt.

Hol hier die Freigabe ab, bevor du schreibst oder pushst.

### Phase 8 — Materialisieren

Nach Freigabe, in dieser Reihenfolge:

**Dateien und Struktur** (Templates unter `templates/umbrella/`):

| Ziel | Quelle | Platzhalter |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md.tpl` | `{{PROJECT_NAME}}`, `{{TODAY}}`, `{{MODE}}` |
| `.gitignore` | `gitignore.tpl` | — (statisch) |
| `.claude/settings.json` | **nicht anfassen** — kommt aus dem ZIP | — |
| `WELCOME.md` | `WELCOME.md.tpl` | `{{PROJECT_NAME}}`, `{{MODE}}` |
| `ADR/001-*.md` … | aus `<scratchpad>/out/ADR/` kopieren | (schon gefüllt) |
| `Docs/`, `src/` | leer, mit `.gitkeep` | — |
| `bootstrap.lock` | `catalog_version` + `mode` aus `manifest.json` | — (Format unten) |

Die genauen Platzhalter-Werte stehen in `templates/umbrella/_placeholders.md`
— dort nachsehen, nicht raten.

`bootstrap.lock` ist `key=value`, eine Zeile pro Eintrag — genau dieses Format,
weil der Welcome-Hook es parst:

```
catalog_version=0.3.0
mode=fasttrack
```

Die Datei ist außerdem das Signal, an dem der Welcome-Hook „Projekt ist
aufgesetzt" erkennt. Fehlt sie, begrüßt er beim nächsten Start wieder wie beim
Erstlauf und fordert einen Bootstrap an.

**Das Umbrella ist immer ein eigenes, code-freies Repo.** Es trägt `ADR/`,
`Docs/`, `CLAUDE.md` und `bootstrap.lock`; `src/*` ist gitignored, weil der
Code dort eigene Git-Historie hat. `repo_form` entscheidet nur, ob unter
`src/` **ein** Code-Repo liegt oder **mehrere** Service-Repos — nie, ob der
Code ins Umbrella wandert. `package.json` und `tsconfig.json` gehören ins
Code-Repo, niemals ins Umbrella.

Es gibt **kein** `ADR_README.md` mehr — `ADR/` ist nach dem Bootstrap nicht
leer, der Hinweis wäre falsch.

**Stories auf das Board.** `stories.json` trägt Titel + Spec pro Story,
schon sortiert. Pro Story ein Aufruf:

```
create_item(title=<title>, description=<spec>, itemType="Story",
            workflow=<siehe unten>, priority=<siehe unten>)
```

Workflow-Zuordnung — **immer explizit mitgeben**. Verlass dich nicht auf eine
serverseitige Vorbelegung: `is_active_preference` kann auf allen Workflows
`false` sein, dann ist das Ergebnis ohne `workflow`-Parameter unbestimmt.

- **Skeleton-Stories (sort_order 10–80)** → der Entwicklungs-Workflow.
  Sie sind vollständig spezifiziert und dürfen direkt in KI-Arbeit gehen.
- **Purpose-Gate (sort_order 90)** → der Planungs-Workflow.
  Sie *soll* Fragen aufwerfen und in einem Human-Status landen.

Die konkreten Namen sind **projektabhängig**. Ruf `list_workflows()` auf
(bei `count: 0` stoppen, siehe Phase 3 — Hinweis auf Workflows → Store) und
ordne anhand der Statuszeilen zu: der Entwicklungs-Workflow hat AI-Statuszeilen
für Spec und Implementierung (z.B. `ASDD`: Backlog → Spec → Implement → Done),
der Planungs-Workflow beginnt mit einem Human-Status (z.B. `Planning`: Inbox →
Story → Ready). Rate keinen Namen — gibt es nur einen Workflow, nimm ihn für
alles und sag dem Nutzer, dass das Purpose-Gate dort mit einem Menschen
angeschaut werden sollte.

`priority` kennt nur 1–5 (1 = Critical), `sort_order` läuft von 10 bis 90 —
das ist nicht 1:1 abbildbar. Feste Zuordnung, damit sie bei jedem Lauf
gleich ausfällt:

| sort_order | Story | priority |
|---|---|---|
| 10–15 | Umbrella-Repo, Sub-Repos | 2 (High) |
| 20–40 | CI, Backend/CLI-Skeleton, Persistenz | 2 (High) |
| 50–80 | Auth, Tenant-Isolation, Frontend, Realtime, Deployment | 3 (Medium) |
| 90 | Purpose-Gate | 5 (Normal) |

Die Feinsortierung innerhalb einer Prioritätsstufe trägt die
Anlage-Reihenfolge — also **sequenziell in `sort_order`-Reihenfolge
anlegen**, nicht parallel.

Prüfe jede Rückgabe: `create_item` liefert `item_id`, `initial_status` und
`workflow`. Landet eine Story im falschen Workflow oder Status, stopp und
melde es — nicht einfach weiterpushen.

Kein `stories.json` im Projekt. Ist der MCP nicht erreichbar, brich mit
klarer Meldung ab, statt die Datei still hinzulegen — der Push ist Teil des
Bootstraps, kein Optional.

**Purpose-Fragmente**, die du im Intake aufgeschnappt hast, gehen in die
Beschreibung der Purpose-Story — nirgendwo sonst.

### Phase 9 — Übergabe

Hier endet der Bootstrap — und hier entsteht die größte Orientierungslücke.
Der Nutzer sieht eine Liste von Dateien und weiß nicht, dass jetzt **er** am
Board etwas tun muss, damit überhaupt etwas weitergeht. Der Report muss das
tragen, nicht nur aufzählen.

```
Fertig. <N> ADRs im Repo, <M> Stories auf dem Board.
(Modus <mode>, Katalog <version>)

Entstanden:
  ADR/001-… bis ADR/0NN-…    die Architektur-Entscheidungen, ab jetzt bindend
  CLAUDE.md, WELCOME.md, .gitignore, bootstrap.lock
  Docs/, src/
  <M> Stories               <k> im Entwicklungs-Workflow, 1 Purpose-Gate

Damit es weitergeht, brauchst du EINEN Schritt im Artifacture-Board:

  Nimm die erste Story ("Umbrella-Repo & ADR-Grundgerüst"), weise sie dir
  zu und zieh sie in den Schritt, der auf KI wartet.

  Beides ist nötig — zugewiesen UND im richtigen Schritt. Sonst tauchen die
  Stories hier nicht auf, und du fragst dich, warum nichts passiert.

Danach: Claude Code hier neu starten und "was steht an?" fragen. Von allein
läuft nichts los — ich hole die Liste erst, wenn du fragst.

Wenn du über das Produkt reden willst: einfach erzählen, was es können soll.
Ich sortiere das in Ideas und Insights, kein Befehl nötig.
```

Passe die Zahlen und den Story-Titel an den echten Lauf an. Erfinde keine
Board-Details, die du nicht aus den `create_item`-Rückgaben kennst.

Warum der Neustart: `CLAUDE.md` wird beim Session-Start geladen, und die ist
gerade erst entstanden. Sag es als Grund mit, nicht als bloße Anweisung — sonst
klingt es nach Ritual.

## Verhältnis zu den anderen Toolkit-Teilen

```
                        Einstieg
                           │
        ┌──────────────────┴──────────────────┐
   leerer Ordner                       Code liegt schon da
        │                                     │
  DIESER SKILL                        extract-umbrella
  (Struktur + ADRs + Stories)         (ADRs rückwärts aus Code)
        └──────────────────┬──────────────────┘
                           │
                  vision-capture         ← hier beginnt Purpose
                           │
                  Planning-Workflow      ← Ausarbeitung, mit Freigabe
                           │
                  ASDD-Workflow          ← Spec + Umsetzung
                           │
                    /code-review
```

Die Purpose-Story aus dem Bootstrap ist der Übergabepunkt: sie sagt
ausdrücklich, dass die Klärung über `vision-capture` und dann den
Planning-Workflow läuft. Es gibt damit **ein** Purpose-Gate im ganzen
Toolkit, nicht zwei konkurrierende.

**Merkregel für die Abgrenzung:** Was Zustand über Sessions hinweg tragen
muss, gehört in einen Artifacture-Workflow — nicht in einen Skill und nicht
in einen Command. Ein Skill liefert Wissen und Artefakte (dieser hier: den
Katalog und `derive.py`), ein Command stößt einen abgeschlossenen Vorgang
an. Deshalb erzeugt dieser Skill Stories und übergibt sie sofort ans Board,
statt sie im Gespräch weiterzuentwickeln.

## Katalog-Änderungen sind Releases, keine Konversation

Bringt der Intake eine Frage hervor, die der Katalog nicht ausdrücken kann
("wir brauchen GraphQL", "muss on-prem laufen"), improvisiere **keinen**
neuen Node und keine neue Option. Leg eine Backlog-Card an
("Katalog-Erweiterung: <Thema>") und mappe das Projekt, wo möglich, auf
bestehende Optionen (z.B. `deployment: manual` → vertagte Card). Der
Katalog entwickelt sich über kuratierte, versionierte Releases — diese
Disziplin ist das Produkt.

Prüfe jede Erweiterungsidee gegen die Zielgruppen-Regel oben: verhindert
die zusätzliche Komplexität Fehler, oder löst sie nur ein
Koordinationsproblem, das diese Nutzer nicht haben?

## Dateien

- `data/catalog.yaml` — der Fragen-DAG (Nodes, Enums, Defaults, Sichtbarkeit)
- `data/mapping.yaml` — Antwort → Story-Ableitung (feste Sortier-Reihenfolge)
- `templates/adr/` — ein ADR-Template pro Katalog-Node
- `templates/stories/` — Skeleton-Story-Specs mit Parameter-Platzhaltern
- `templates/umbrella/` — die Umbrella-Dateien (CLAUDE.md, WELCOME.md,
  .gitignore, settings)
- `scripts/derive.py` — deterministische Derivation; auch der Validator
- `test-cases/` — Referenz-Antwortsätze; `bash test-cases/run.sh` prüft alle

Bei Zweifeln: in die Dateien schauen, nicht improvisieren.

## Interaktionsstil

- Deutsch als Default.
- Knapp, faktisch, kein Marketing-Sprech.
- Vor jedem Schreibvorgang: Vorschau + OK abholen.
- Kein Auto-Git: kein `git init`, kein `commit` ohne ausdrückliche Bitte.
- Nach Abschluss: kurzer Report mit konkreten nächsten Schritten.
