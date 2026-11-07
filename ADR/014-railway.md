# ADR-014: Railway-Umsetzung des Deployments

- Datum: 2026-11-07
- Entscheidung: **Railway, ein Projekt, Staging + Production, Frontend als
  einzige öffentliche Adresse**
- Gilt zusammen mit ADR-009 (anbieterunabhängiges Verfahren)

## Festlegungen
- Ein Railway-Projekt `schichtplaner`, Region EU (nahe Neon Frankfurt), zwei
  Environments: `staging` und `production`
- Zwei Services aus dem Code-Repo, jeweils mit eigenem Dockerfile und eigener
  Config-as-Code-Datei (`railway.api.json`, `railway.web.json`):
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
- Die API lauscht auf `::` — das private Railway-Netz ist IPv6
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
- Einstellungen, die die Railway-CLI nicht setzen kann (GitHub-Verbindung,
  Branch je Environment, „Wait for CI“, Config-Datei-Pfad), werden einmalig in
  der Oberfläche gesetzt und in `DEPLOYMENT.md` im Code-Repo beschrieben

## Konsequenzen
- Eine eigene Domain ersetzt später nur die Railway-Adresse des `web`-Service;
  die Same-Origin-Architektur bleibt
- Ein Anbieterwechsel ändert dieses ADR, nicht ADR-009
