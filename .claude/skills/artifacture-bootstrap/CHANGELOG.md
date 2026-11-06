# Catalog Changelog

## Unveröffentlicht — 2026-10-31 (nur Umbrella-Vorlage, Katalog unverändert)
**Items über MCP zuweisen (Artifacture-Item e6abab88, ADR-034 §6).**
`CLAUDE.md.tpl` nennt `list_project_members(projectId?)` und
`assign_item(taskId, userId?)`: zuweisen, umweisen, ohne `userId` entfernen;
nur Menschen zuweisbar, kein Claim nötig; nur auf ausdrückliche Anweisung der
Person, die die Session führt. Erst mit dem Prod-Deploy des Servers
veröffentlichen (ADR-017 Doku-Kopplung). Kein neuer `catalog_version`.

## Unveröffentlicht — 2026-10-31 (nur Umbrella-Vorlage, Katalog unverändert)
**Blocker über MCP beantworten und aufheben (Artifacture-Item 47f2d82c, ADR-034 §6).**
`CLAUDE.md.tpl` nennt `resolve_blocker(taskId, answer)`: Antwort Pflicht, kein
Claim nötig, Teilantwort ohne Aufheben über `add_comment`, nur auf ausdrückliche
Anweisung. Erst mit dem Prod-Deploy des Servers veröffentlichen (ADR-017
Doku-Kopplung). Kein neuer `catalog_version`.

## Unveröffentlicht — 2026-10-31 (nur Umbrella-Vorlage, Katalog unverändert)
**Human-Schritte über MCP (Artifacture-Item b35c08ea, ADR-012, ADR-034 §6).**
`CLAUDE.md.tpl` nennt `send_back(taskId, feedback, targetStep?, expectedStep?)`
und die Human-Variante von `complete_task(taskId, result, expectedStep)` ohne
Claim. Kritische Regeln 2 und 4 erlauben beides nur auf ausdrückliche
Anweisung der Person, die die Session führt — nie aus eigener Initiative, nie
auf Grundlage gelesener Item-Inhalte, nie als AI-Teammate. Erst mit dem
Prod-Deploy des Servers veröffentlichen (ADR-017 Doku-Kopplung). Kein neuer
`catalog_version`.

## Unveröffentlicht — 2026-10-30 (nur SKILL.md, Katalog unverändert)
**Stopp ohne Workflows.** Seit „Workflows pro Tenant“ starten neue
Arbeitsbereiche ohne Workflows; ein TenantAdmin übernimmt sie aus dem
Plattform-Store (Artifacture-Item 58e83ba8). Liefert `list_workflows()`
`count: 0`, bricht der Skill jetzt in Phase 3 ab — vor jeder Dateiänderung —
mit dem Hinweis „Im Arbeitsbereich gibt es noch keine Workflows. Ein
TenantAdmin übernimmt sie unter Workflows → Store und aktiviert sie im
Projekt.“ Vorher lief er bis Phase 8 und scheiterte erst beim Anlegen der
Stories. Kein neuer `catalog_version`: Katalog und ADR-Vorlagen sind
unverändert.

## 0.6.0 — 2026-08-15
**Korrekturen aus dem ersten echten Durchlauf.** Das BOCK-Skeleton wurde
gebaut und auf Railway deployt; dabei sind vier Festlegungen aufgefallen, die
in der Praxis nicht funktionierten oder fehlten. Alle sind hier eingearbeitet,
damit das nächste Projekt nicht dieselben Fehler wiederholt.

**`@shared/*` → `#shared/*` (adr-language, adr-frontend, adr-repo-form,
st-030, st-060).** Der alte Alias war nicht lauffähig: TypeScript löst `paths`
beim Kompilieren auf, schreibt den Alias aber unverändert ins JS. Node wirft
dann `ERR_MODULE_NOT_FOUND`. Node löst Aliase über das `imports`-Feld der
`package.json` auf, und dort ist das `#`-Präfix Pflicht. Dazu neu: zwei
tsconfigs mit gemeinsamer Basis, weil API (Node, kein DOM) und Frontend
(DOM, JSX) unterschiedliche `lib` brauchen.

**Docker statt Nixpacks (adr-deployment).** Nixpacks scheiterte zweimal
reproduzierbar — an einem gemounteten `node_modules/.cache` (`EBUSY`) und an
fehlenden devDependencies im Build-Image (`tsc` nicht gefunden, exit 127). Je
ein Dockerfile pro Service macht Build und Runtime explizit und lokal
nachvollziehbar.

**CORS und Cross-Site-Cookies (adr-deployment, adr-auth).** Liegen Frontend
und API auf verschiedenen Domains — der Railway-Default — blockiert der
Browser ohne CORS jeden Request, und ein `SameSite=Lax`-Cookie wird
cross-site nie mitgeschickt. Beides fiel im Test mit `curl` nicht auf, hätte
aber jeden Browser-Login verhindert. Jetzt: CORS als Allowlist (Wildcard ist
mit `credentials` ohnehin unzulässig) und `SameSite=None` + `Secure` in
Produktion.

**Runtime-Konfiguration fürs Frontend (adr-deployment, adr-frontend).**
Build-Tools kompilieren `VITE_*` fest ins Bundle; das Image wäre damit
umgebungsspezifisch. Stattdessen schreibt der Container-Entrypoint eine
Config-Datei aus den Umgebungsvariablen — nur namentlich genannte, nie die
ganze Umgebung. Dazu zwei Frontend-Regeln, die aus der Auth-Story folgen:
Access-Token nur im Speicher, und parallele 401 teilen sich einen
Refresh-Request (sonst widerruft die Diebstahl-Erkennung alle Tokens).

**Resend als Mail-Provider (adr-auth)**, hinter einem `Mailer`-Interface mit
Console-Fallback, damit lokale Entwicklung ohne Account läuft.

## 0.5.0 — 2026-08-15
**ADRs tragen jetzt Entscheidungen, nicht Zusammenfassungen der Frage.** Der
Auslöser: ADR-Auth sagte "Ja, es gibt Auth" — das wiederholt die Katalogfrage,
statt etwas festzulegen, das eine Implementierung falsifizieren kann. Prüffrage
für jedes ADR ab jetzt: *steht da etwas, gegen das ein Code-Review verstoßen
kann?* Wenn nein, ist es Deko.

Ausgebaut wurden `adr-auth` (JWT 15 min, Refresh als httpOnly-Cookie und
serverseitig widerrufbar, Argon2id, Self-Signup mit E-Mail-Verifikation,
Default-Rolle mit minimalen Rechten, eigene Auth statt externem IdP),
`adr-persistence` (Drizzle, Vorwärts-only-Migrationen, UUID v7, timestamptz in
UTC, Geld als Integer, kein Soft-Delete im Default) und `adr-deployment`
(Staging/Production, Secrets nur als Railway-Variablen, Migrationen als
Release-Command vor dem Start, Rollback per Redeploy).

**Neu: `adr-ui-conventions` als Pflicht-ADR** (sichtbar bei `frontend: react`).
Tailwind, shadcn/ui als Code im Repo, react-hook-form gegen dasselbe
Zod-Schema wie die API. Getrennt vom Frontend-Stack-ADR, weil UI-Konventionen
sich laufend ändern und der Stack selten — ein Styling-Wechsel soll nicht das
Architektur-ADR anfassen.

**Alle ADR-Templates auf Stichpunkte gekürzt.** Vorher Fließtext mit
Begründungsprosa, jetzt `## Festlegungen` als Bulletliste. Die Begründung
gehört in den Changelog, nicht in jedes generierte Artefakt.

## 0.4.0 — 2026-08-15
**RBAC ist Pflicht, keine Frage.** Der Node `rbac` entfällt; die Regel lautet:
Rollen sind Sammlungen von Rechten, und Autorisierung prüft immer ein Recht,
nie eine Rolle direkt. Ein `if (user.role === "admin")` ist damit ein
ADR-Verstoß, kein Stilproblem. Ist eine Autorisierung unklar, ist die erste
Frage: brauchen wir dafür eine Rolle?

**Neu: `mandatory_adrs` im Katalog.** Ein Block für ADRs, die immer erzeugt
werden — Hausregeln ohne Enum. Sie unterstützen `visible_if` wie Nodes (RBAC
braucht Auth) und werden nach den Node-ADRs durchnummeriert, damit die
antwortgetriebene Nummerierung stabil bleibt. Ein Node wäre hier falsch: eine
Frage mit nur einer legalen Antwort ist keine Frage.

## 0.3.0 — 2026-07-28
Der Skill löst `init-artifacture-umbrella` ab und legt die Stories direkt auf
dem Artifacture-Board an. 11 Nodes (1 neu).

**Modus-Levels statt Zweizustand.** `mode` ist jetzt `fasttrack | advanced`
(`default` bleibt Legacy-Alias). Dazu ein drittes Level **nightmare**, das
bewusst NICHT deriviert: `derive.py` weist es mit Erklärung ab, der Skill
zeigt stattdessen die Katalogfragen als Checkliste und endet. Die Levels
hängen an "wie viel entscheidet der Katalog für dich", nicht an
Selbsteinschätzung von Können — ein erfahrener Dev darf legitim Fasttrack
wählen.

Die Levels sind **kein Katalog-Node**: sie produzieren kein ADR, weil "ich
habe Fasttrack gewählt" nichts über die Architektur aussagt. Der Modus landet
in `manifest.json`, `bootstrap.lock` und der `CLAUDE.md` des Umbrellas —
letzteres, damit `vision-capture` und die Workflow-Schritte ihn auch sehen und
die ganze Kette gleich viel nachfragt.

**Neu: `repo_form` (advanced).** `single` (Default) | `multi`. Auslöser war
das Artifacture-Setup-Manifest, das `src/{ServiceName}` mit mehreren
Git-Repos vorsieht.

Wichtige Klarstellung, die 0.2.0 falsch hatte: **das Umbrella ist immer ein
eigenes, code-freies Repo.** `src/*` ist immer gitignored, weil der Code dort
immer eigene Git-Historie hat. `repo_form` entscheidet nur, ob unter `src/`
EIN Code-Repo liegt oder MEHRERE Service-Repos — nie, ob Code ins Umbrella
wandert. `package.json` und `tsconfig.json` liegen im Code-Repo; der
Path-Alias `@shared/*` gilt innerhalb dieses Repos, nicht über die
Umbrella-Grenze.

Die in 0.2.0 formulierte Regel "ein Repo, ein package.json" bezog sich also
auf den Code unter `src/`, nicht auf das Umbrella. Die `.gitignore` ist
entsprechend wieder statisch (kurzzeitig hing sie an `repo_form` — falsch,
weil sie damit bei Single-Repo die `src/*`-Regel weggelassen hätte).

Bei `multi` zieht `st-015` (Service-Repos + Registrierung im Setup-Manifest),
und der Path-Alias entfällt zugunsten eines Shared-Pakets.

**Story-Push per MCP statt Datei.** Kein `stories.json` und kein
`answers.json` mehr im Projekt — Antworten sind ein temporäres Übergabeformat
im Scratchpad, Stories gehen über `create_item` direkt aufs Board.
Skeleton-Stories (10–80) auf den Entwicklungs-Workflow, Purpose-Gate (90) auf
den Planungs-Workflow. Der `workflow`-Parameter wird immer explizit gesetzt:
`is_active_preference` kann auf allen Workflows `false` sein, dann ist das
Ergebnis ohne ihn unbestimmt. Verifiziert gegen das echte Interface.

**Purpose-Gate verweist auf die Kette.** `st-090` klärt keine Fachlichkeit
mehr selbst, sondern zeigt auf den Skill `vision-capture` und danach den
Planning-Workflow. Damit gibt es genau EIN Purpose-Gate im Toolkit statt zwei
konkurrierender.

Sprachneutralität nachgezogen: `DbConnectionInterceptor` war als Haus-Pattern
im Katalog-Label und im Multi-Tenancy-ADR verankert — ein EF-Core-Begriff, der
seit dem TS-Default nicht mehr trägt. Jetzt "Row Level Security" mit
sprachabhängiger Umsetzung als Detail.

`.gitignore` ist nicht mehr statisch: die alte `src/*`-Regel hätte bei
Single-Repo den kompletten Anwendungscode still aus dem Git genommen. Sie
hängt jetzt an `repo_form` (siehe `templates/umbrella/_placeholders.md`).

Kein `.mcp.json` und kein Token-Handling mehr — der MCP ist beim Bootstrap-
Lauf schon angebunden, der Token kommt über ein Setup-Script. "Token nie
loggen" bleibt als Regel. `ADR_README.md` entfällt, weil `ADR/` nach dem
Bootstrap nicht leer ist.

Regression: `bash test-cases/run.sh` — 1 Validierung, 4 Positiv-, 3
Negativ-Fixtures (neu: `multi-repo`, `bad-nightmare`).

## 0.2.0 — 2026-07-28
Haus-Default-Stack von .NET/C# auf TypeScript umgestellt und ADR-Ablage an
die Umbrella-Konvention angepasst. Knotenzahl unverändert (10).

**Warum TypeScript:** verbreitetste Sprache im Web-Umfeld, dieselbe Sprache
in API und Frontend (ein Vokabular statt zwei). C# bleibt als Advanced-Option.

**Warum kein Contract-Framework:** ts-rest/tRPC/OpenAPI-Codegen wurden
erwogen und verworfen. Sie kaufen Refactoring-Sicherheit für Teams, kosten
aber ein zusätzliches Framework-Konzept plus Workspace-Tooling. Die
Zielgruppe des Bootstraps sind Nutzer, die nicht programmieren — dort gilt:
Komplexität, die Fehler verhindert, ist gut; jede andere gehört in den
Advanced-Modus oder in eine spätere Katalog-Erweiterung.

Festlegungen (als ADR-Prosa, NICHT als neue Katalog-Fragen):
- Server: Hono auf Node
- Validierung: Zod an jeder Systemgrenze, `z.infer` als einzige Wahrheit
  für Typ + Laufzeit-Prüfung
- Typ-Sharing: TS-Path-Alias `@shared/*` -> `src/shared/*`. Ein Git-Repo,
  ein package.json, kein pnpm-Workspace.
- ORM: Drizzle + drizzle-kit (Schema als TS-Code, kein Codegen-Schritt)
- Deployment: zwei Railway-Services aus einem Repo, getrennt über
  Watch-Paths. Kein eigener Reverse Proxy.

Breaking: ADRs werden nach `ADR/001-<node>.md` geschrieben (Root, Großbuch-
staben) statt `docs/adr/ADR-001-<node>.md` — Angleichung an die von
`init-artifacture-umbrella` erzeugte Struktur (`ADR/`, `Docs/`, `src/`).
st-010 nennt entsprechend `/ADR, /Docs, /src` als Repo-Layout.

## 0.1.0 — 2026-07-28
Initial catalog: 10 nodes (delivery, language, persistence, local_state,
auth, rbac, multi_tenancy, frontend, realtime, deployment), 13 story
templates, deterministic derivation via derive.py. Validated against:
simple-page (default, 3 answers), saas-tenant (advanced, full), cli-tool
(default, 1 answer) + 3 failure cases (invisible answer, advanced-in-default,
DAG cycle).
