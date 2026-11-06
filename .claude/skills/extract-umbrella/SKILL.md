---
name: extract-umbrella
description: |
  Migration-Skill: Wandelt eine konventionell entwickelte Codebase in eine
  AI-First-Umbrella-Struktur um, indem implizite Architektur-Entscheidungen
  als ADRs reverse-engineert werden. Hält den Umbrella im Sync-Modus am Leben.

  Aktiviert bei:
  - "Extract Umbrella"
  - "Umbrella aus dem Code bauen"
  - "ADRs aus dem Bestand extrahieren"
  - "Reverse-engineer ADRs"
  - "Umbrella aktualisieren / syncen"
  - "Sync ADRs gegen Code"
  - Wenn ein leerer Umbrella-Ordner aufgemacht wird mit Verweis auf existierenden Source

  Modi (selbsterkennend):
  - Bootstrap: Umbrella ist leer → kompletter Reverse-Engineering-Run
  - Sync: ADR/-Ordner existiert mit Inhalten → drift detection + neue ADR-Vorschläge
---

# Extract Umbrella

Reverse-engineert ADRs aus einer existierenden Codebase und baut/aktualisiert
einen AI-First-Umbrella, damit AI-Agenten in einem Spec-First-Workflow mit
nachvollziehbarer Architektur-Hoheit arbeiten können.

## Warum dieser Skill existiert

Lies bei Bedarf `references/framing.md` — das ist der Kontext, *warum* ADRs
das Fundament für AI-Workflows sind. Wenn der User unsicher ist, was hier
passiert, fasse das knapp zusammen.

Kurzversion: AI-Agenten produzieren guten Code, wenn sie die *Entscheidungen*
hinter dem Code kennen. Bei Bestandscode liegen diese Entscheidungen oft nur
implizit vor. Dieser Skill macht sie explizit — als prüfbare ADRs.

## Modus-Erkennung

Beim Start als ERSTES feststellen, in welchem Modus wir sind:

```
Existiert ./ADR/ mit mindestens einer ADR-Datei (NNN-*.md)?
  ja  → Sync-Modus
  nein → Bootstrap-Modus
```

Den erkannten Modus dem User explizit ankündigen, bevor es losgeht.

## Kritische Regeln

1. **`.gitignore` bei der CODE-ANALYSE bewusst ignorieren.** Die Umbrella-
   `.gitignore` schließt `src/*` aus dem Tracking aus, aber der zu
   analysierende Code liegt genau dort. Beim Lesen mit Glob/Grep/Read NICHT
   auf `.gitignore` verlassen — explizit in `src/` reinlesen.
2. **NIEMALS in den Source-Ordner schreiben.** Nur lesen. Alle Outputs
   landen ausschließlich im Umbrella-Root (`./ADR/`, `./Docs/`, `./CLAUDE.md`).
3. **Kein Auto-Commit.** Weder im Source noch im Umbrella. Der User entscheidet.
4. **Hypothesen markieren.** Reverse-engineerte ADRs bekommen Status
   `Proposed (reverse-engineered)`, bis der User sie bestätigt → `Accepted`.
5. **Reden vor Schreiben.** Vor jedem schreibenden Schritt eine Vorschau
   liefern (welche ADRs würden entstehen / verändert werden) und auf OK warten.

## Bootstrap-Modus

Ziel: Aus Source einen vollständigen Umbrella aufbauen.

### Phase 1: Setup-Check

1. Aktuelles Arbeitsverzeichnis erkennen. Bestätigen, dass das der neue
   Umbrella-Ordner sein soll.
2. Den User nach dem Source-Pfad fragen, falls noch nicht angegeben:
   - Üblicherweise `./src/<repo>/` (Sub-Repo unter `src/`)
   - Oder absoluter Pfad zu einem benachbarten Ordner
3. Verifizieren, dass der Pfad existiert und Code enthält.

### Phase 2: Codebase-Discovery

Das Ziel hier: Tech-Stack-Inventar erstellen. Noch keine ADRs schreiben.

Systematisch scannen (mit Glob/Read, NICHT von `.gitignore` blockieren lassen):

- **Manifeste & Build-Files**:
  `package.json`, `*.csproj`, `*.sln`, `nx.json`, `pom.xml`, `build.gradle`,
  `Cargo.toml`, `pyproject.toml`, `go.mod`, `Dockerfile`, `docker-compose.yml`,
  `*.tf`, `Makefile`
- **Konfiguration**:
  `appsettings*.json`, `tsconfig*.json`, `.eslintrc*`, `nx.json`,
  `angular.json`, `next.config.*`, `vite.config.*`
- **CI/CD**:
  `.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`
- **Repo-Form**: Monorepo? Einzelrepo? Workspaces?
- **Modul-Struktur**: Welche Top-Level-Ordner gibt es? Was deutet auf
  Bounded Contexts / Apps / Libs hin?
- **Stichproben aus dem Code**: 3-5 zentrale Files lesen, um Patterns zu
  erkennen (DI-Container? Mediator-Pattern? Repository-Pattern? State-
  Management?)

Ergebnis: Eine strukturierte Liste an beobachteten Fakten — mit Datei-
Beweisen (`file:line`).

### Phase 3: ADR-Hypothesen generieren

Aus dem Inventar Kandidaten-ADRs ableiten. Lies `references/adr-domains.md`
für eine Checkliste typischer Domänen — gehe diese durch und prüfe pro
Domäne: Gibt es eine erkennbare Entscheidung?

Typische Kandidaten:
- Sprache(n) / Stack
- Repo-Form (Monorepo + Tooling)
- Frontend-Framework + State-Management
- Backend-Framework + Architektur-Pattern (Mediator, CQRS, MVC, ...)
- Datenbank + ORM
- API-Stil (REST/GraphQL/gRPC)
- Auth/Identity
- Test-Strategie (Unit/Integration/E2E-Mix)
- Deployment-Target
- Observability / Logging
- Modul-Grenzen / Boundaries

Pro Hypothese erfassen:
- Beobachtung (was im Code zu sehen ist, mit Belegen)
- Vermutete Entscheidung
- Vermutete Konsequenzen
- Confidence (high / medium / low)

### Phase 4: Vorschau & Bestätigung

Dem User die Liste der Kandidaten-ADRs präsentieren — KOMPAKT, nicht die
vollen ADRs. Eine Tabelle / Liste reicht:

```
Vorschlag: 12 ADRs als Reverse-Engineering-Draft

01. Stack: TypeScript + .NET (high)
02. Monorepo mit Nx (high)
03. Angular als Frontend-Framework (high)
04. NgRx für State-Management (medium — nur in 2 von 4 Apps)
...

Soll ich alle 12 schreiben, oder einzelne weglassen / zusammenfassen?
```

### Phase 5: ADRs schreiben

Erst nach Bestätigung. Pro ADR:
- Datei `ADR/NNN-kebab-case-titel.md`
- Template aus `templates/adr-template.md`
- Status: `Proposed (reverse-engineered)`
- Date: heutiges Datum
- Deciders: leer lassen (User füllt aus)
- "Applies to" wenn relevant
- Belege im Context-Abschnitt mit `file:line`-Referenzen

### Phase 6: Umbrella-Skelett

- `CLAUDE.md` aus `templates/CLAUDE.md.tpl` rendern (Platzhalter ersetzen:
  Projektname, Source-Pfad, Tech-Stack-Zeile)
- `.gitignore` aus `templates/umbrella-gitignore.tpl`
- `Docs/` als leerer Ordner mit `.gitkeep`
- `ADR/000-adr-template.md` mitliefern (Standard-Template)
- `.claude/` und `.mcp.json` **nicht anfassen.** Sie kommen aus dem
  ausgelieferten Artifacture-ZIP (per `curl` geholt) und sind schon da:
  `settings.json` registriert Hook und Permission-Defaults, `.mcp.json` trägt
  die Anbindung samt Token. Fehlen sie, ist das ZIP unvollständig entpackt —
  dem User sagen, nicht rekonstruieren. Den Token niemals lesen oder ausgeben.

### Phase 7: Übergabe

Knapper Report an den User:
- Was entstanden ist (X ADRs, Umbrella-Files)
- Was als Nächstes zu tun ist (ADRs durchgehen, Status auf `Accepted`
  setzen, Deciders eintragen)
- Hinweis auf Sync-Modus für später

## Sync-Modus

Ziel: Existierenden Umbrella mit dem aktuellen Code-Stand abgleichen.

### Phase 1: Bestand einlesen

- Alle ADRs aus `./ADR/` lesen
- Pro ADR extrahieren: Nummer, Titel, Status, Decision (worum geht's
  konkret), "Applies to"
- CLAUDE.md kurz lesen, um den Kontext zu verstehen

### Phase 2: Code-Scan

Wie Bootstrap-Phase 2, aber mit Fokus: Was hat sich verändert / was ist
neu / was widerspricht den ADRs?

### Phase 3: Drift-Analyse

Pro existierendem ADR klassifizieren:
- **`confirmed`**: Code stimmt überein, ADR aktuell
- **`drifted`**: Code weicht ab → konkret beschreiben wie
- **`superseded`**: Entscheidung wurde durch eine neue ersetzt
- **`unknown`**: Nicht eindeutig prüfbar (z.B. abstrakte Patterns)

Plus: Neue Tech / Patterns finden, die in keinem ADR stehen → ADR-Kandidaten.

### Phase 4: Report & Bestätigung

Dem User einen Drift-Report präsentieren:

```
Sync-Report:

Confirmed (kein Handlungsbedarf): 8
Drifted (Update vorgeschlagen): 2
  - ADR-005 Blazor Server: Code zeigt jetzt auch Blazor WASM in /admin
  - ADR-007 Job-Handler: Neue Variante mit Hangfire dazugekommen
Superseded (ersetzt): 1
  - ADR-003 Repository-Pattern: Code nutzt nur noch direktes EF
New ADR-Kandidaten: 3
  - SignalR für Realtime
  - MinIO statt S3 für File-Storage (lokal)
  - OpenTelemetry für Tracing

Welche soll ich anpacken? (Drift updaten / neue ADRs anlegen / nichts)
```

### Phase 5: Anwendung

Erst nach Bestätigung:
- Drift: Bestehendes ADR editieren, ältere Decision in einen
  "History"-Abschnitt verschieben oder Status auf `Superseded` setzen
  und neues ADR mit Verweis anlegen
- Neue ADRs: Wie Bootstrap-Phase 5 anlegen, mit nächster freier Nummer
- Status-Klarheit: Reverse-engineerte Drafts klar markieren

## Templates & Referenzen

- `templates/CLAUDE.md.tpl` — neutrales Umbrella-CLAUDE.md
- `templates/adr-template.md` — ADR-Format (Reverse-Engineering-Variante)
- `templates/umbrella-gitignore.tpl` — `.gitignore` für Umbrella-Repo
- `references/framing.md` — Warum ADRs für AI-First-Development
- `references/adr-domains.md` — Checkliste typischer ADR-Bereiche

Bei Unsicherheit über das Format → in die Templates schauen, nicht raten.

## Interaktionsstil

- Deutsch als Default (außer User wechselt)
- ADR-Inhalte auf Englisch (kunden-internationaler)
- Knapp, faktisch, mit Datei-Belegen
- Vor jedem Schreiben: Vorschau und OK abholen
- Confidence ehrlich kommunizieren — lieber "low confidence, bitte prüfen"
  als überzeugt eine falsche Entscheidung dokumentieren
