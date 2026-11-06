---
title: "Backend-Skeleton ({language})"
---
## Intent
Lauffähiger API-Prozess mit Health-Endpoint — der Beweis, dass die
Wertschöpfungskette bis "läuft" durchgängig ist.

## Spec
- Projektgerüst {language} nach Haus-Konvention, im Code-Repo unter `src/`
  des Umbrellas (das Umbrella selbst bleibt code-frei)
- Ordnerstruktur im Code-Repo: `src/api`, `src/shared` (Zod-Schemas),
  `src/web`
- `package.json` und `tsconfig.json` im Code-Repo, nicht im Umbrella
- tsconfig-Path-Alias `#shared/*` -> `src/shared/*`
- GET /health -> 200 mit Build-Info
- Konfigurations-Handling: env via Zod-Schema validiert (fehlende
  Variable = Startabbruch mit klarer Meldung, nicht undefined)
- Strukturiertes Logging
- Keine fachlichen Endpoints

## Out of Scope
Domänenlogik, Datenmodell (-> st-090), Auth (-> st-050).
