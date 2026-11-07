# ADR-012: CI & Tests

- Datum: 2026-11-07
- Entscheidung: **GitHub Actions, Vitest, Node 24 LTS, npm**

## Festlegungen
- CI läuft im **Code-Repo** (`src/app`), nicht im Umbrella — das Umbrella
  enthält keinen Code (ADR-003)
- **GitHub Actions** als CI-Plattform, weil die Repos auf GitHub liegen. Kein
  zweiter Dienst mit eigenem Konto und eigenen Secrets
- Trigger: jeder Push auf jeden Branch und jeder Pull Request auf `main`
- **Node 24 (LTS)**, festgelegt in `.nvmrc` und `package.json#engines`; die CI
  liest die Version aus `.nvmrc`. Lokal und CI laufen damit auf derselben
  Version
- **npm** als Paketmanager; `package-lock.json` ist eingecheckt, die CI
  installiert mit `npm ci`. Ein Lockfile-Drift bricht den Build, statt still
  andere Versionen zu ziehen
- Pipeline-Schritte, jeder ein eigener Step mit eigenem Fehlerbild:
  `npm ci` → `npm run check` (Biome: Lint + Format) → `npm run typecheck`
  (`tsc --noEmit`, alle tsconfigs) → `npm test` (Vitest) → `npm run build`
- **Vitest** als Test-Runner für API und Frontend — dieselbe Konfiguration,
  dieselben Assertions, passt nativ zu Vite
- Ein Lauf ohne Tests ist grün (`--passWithNoTests`), solange es noch keine
  fachlichen Tests gibt
- Branch-Schutz auf `main`: Merge nur mit grüner CI. Grundlage für ADR-009
  („kein Deploy ohne grüne CI“)
- Keine Secrets in der CI-Konfiguration (ADR-009). Braucht ein späterer Schritt
  eins, kommt es aus den GitHub-Secrets

## Konsequenzen
- Ein Wechsel von Plattform, Runner oder Paketmanager ändert dieses ADR, statt
  ein zweites daneben zu stellen
- Coverage-Ziele sind hier bewusst nicht festgelegt
