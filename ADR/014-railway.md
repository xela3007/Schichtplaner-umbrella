# ADR-014: Railway-Umsetzung des Deployments

- Datum: 2026-11-07
- Entscheidung: **Railway, ein Projekt, Staging + Production, Frontend als
  einzige öffentliche Adresse**
- Gilt zusammen mit ADR-009 (anbieterunabhängiges Verfahren)
- Status: accepted, geändert 2026-11-07 (Infrastructure as Code statt
  Config as Code, fester API-Port)

## Festlegungen
- Ein Railway-Projekt `schichtplaner`, Region EU (nahe Neon Frankfurt), zwei
  Environments: `staging` und `production`
- **Railway Infrastructure as Code** in `.railway/railway.ts` im Code-Repo
  hält Builder, Dockerfile-Pfad, Watch-Paths, Pre-Deploy, Health-Checks,
  Branch und Region. Übernommen pro Umgebung mit `railway config plan` →
  `railway config apply`. Variablen verwaltet die Datei **nicht** — Secrets
  bleiben ausschließlich in Railway
  - Grund: Railways „Config as Code“ (`railway.json`) ist abgekündigt; neue
    Services können es nicht mehr aktivieren, ab 2026-12-01 wird es gar nicht
    mehr gelesen
  - Einstellungen nicht parallel in der Oberfläche ändern — die Datei ist die
    Quelle der Wahrheit
- Zwei Services aus dem Code-Repo, jeweils mit eigenem Dockerfile:
  - `api`: Node-Container, **nur im privaten Railway-Netz erreichbar**, keine
    öffentliche Domain
  - `web`: nginx mit dem statischen Bundle, **einzige öffentliche Adresse**
- Getrennte Deploys über **Watch-Paths**, nicht über Root-Directories (ein
  `package.json`, ADR-002). Änderungen an `src/shared/` deployen beide Services
- **Same-Origin über den Web-Container:** nginx reicht genau die API-Endpunkte
  (`/health`, `/me`, `/reference`, `/auth/…`) intern an `api` weiter. Für den
  Browser gibt es eine einzige Adresse
  - Grund: Bei zwei Railway-Adressen wären Frontend und API verschiedene
    Sites; Safari und Firefox blockieren das Refresh-Cookie dann, und jeder
    Reload meldet ab
  - Das ist **keine** TLS-Terminierung und kein vorgeschalteter Proxy — TLS und
    öffentliches Routing macht weiter Railway
  - Dieselbe Weiche wie im Dev-Proxy (ADR-007): `/auth/verify-email` mit
    `Accept: text/html` liefert die App, sonst die API
- Folge für Cookies (ADR-005): gleiche Origin → `SameSite=Lax` + `Secure`.
  CORS bleibt eine leere Allowlist — fremde Origins sind nicht erlaubt
- Die API lauscht auf `::` — das private Railway-Netz ist IPv6 — und hat einen
  **fest gesetzten `PORT=3000`**. Railways zur Laufzeit vergebenes `PORT` lässt
  sich aus `web` nicht referenzieren; die Weiterleitungsadresse wäre sonst leer
- **CI-Gate über Railways „Wait for CI“**: Railway deployt aus GitHub, aber erst
  nach grünem Check `CI`. Kein Railway-Token in GitHub
- **Staging** deployt automatisch aus `main`. **Production** deployt aus dem
  Branch `production`; freigeben heißt, `production` per Fast-Forward auf einen
  Commit von `main` zu setzen — nur auf ausdrückliche Anweisung
- Migrationen laufen als **Pre-Deploy-Command** des `api`-Service mit dem
  drizzle-Migrator zur Laufzeit (`drizzle-kit` ist devDependency und nicht im
  Image). Schlägt die Migration fehl, wird nicht deployt
- Health-Checks: `api` → `/health` (503 bei nicht erreichbarer DB stoppt den
  Deploy), `web` → statische Datei
- Jede Umgebung bekommt ihren eigenen Neon-Branch (`staging`, `production`)
  und ein eigenes `JWT_SECRET`. Secrets nur als Railway-Variablen
- Nur die GitHub-Verbindung (Railway-GitHub-App, „Connect Repo“, „Wait for
  CI“) wird einmalig in der Oberfläche gesetzt und in `DEPLOYMENT.md` im
  Code-Repo beschrieben

## Konsequenzen
- Eine eigene Domain ersetzt später nur die Railway-Adresse des `web`-Service;
  die Same-Origin-Architektur bleibt
- Ein Anbieterwechsel ändert dieses ADR, nicht ADR-009
