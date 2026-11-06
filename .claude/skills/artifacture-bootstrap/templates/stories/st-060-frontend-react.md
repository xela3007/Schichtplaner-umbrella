---
title: "Frontend-Skeleton: React SPA gegen API"
---
## Intent
React-App läuft, spricht mit der API, zeigt Health-Status. Bei Auth:
Login-Maske gegen die Auth-Schicht.

## Spec
- Vite/React-Gerüst in src/web, im selben package.json wie die API
- Typen kommen per `#shared/*`-Alias aus den Zod-Schemas — keine
  handgeschriebenen API-Typen im Frontend (sie würden driften)
- Eine Seite: Health-Status der API sichtbar
- API-Basis-URL via env (Zod-validiert)
- Bei vorhandener Auth-Story: Login-Flow angebunden
- Keine fachlichen Views

## Out of Scope
Design, Seitenstruktur, Inhalte — alles Purpose (-> Backlog).
