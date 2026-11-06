---
title: "Service-Repos anlegen und im Setup-Manifest registrieren"
---
## Intent
Umbrella und Service-Repos existieren, das Artifacture-Setup-Manifest
beschreibt sie vollständig — ein Worker kann den Arbeitsbaum aus dem
Manifest rekonstruieren, ohne dass jemand Pfade errät.

## Spec
- Je Service ein Git-Repo, geklont nach `src/{ServiceName}`
- Registrierung im Artifacture-Setup-Manifest (`get_project_setup`
  liefert danach umbrella + repos mit `serviceName`, `gitUrl`,
  `targetPath`)
- `get_setup_script` muss den Baum idempotent herstellen können
  (clone-or-ff-pull), ohne Secret im Script
- Shared-Code (Zod-Schemas) als eigenes Repo + konsumierbares Paket —
  der Path-Alias aus dem Sprach-ADR gilt hier NICHT
- Umbrella enthält nur ADR/, Docs/ und die Registrierung, keinen Code

## Out of Scope
Fachlicher Code in den Services, CI pro Repo (-> st-020), Deployment
(-> st-080). Der Repo-Split selbst ist hier der ganze Umfang.
