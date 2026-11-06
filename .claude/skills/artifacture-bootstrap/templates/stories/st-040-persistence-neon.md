---
title: "Persistenz: Neon Postgres + Migrations-Grundgerüst"
---
## Intent
Datenbank angebunden, Migrationen laufen, Schema ist leer — bereit für
die erste Domain-Slice.

## Spec
- Neon-Projekt (eu-central-1), Connection via env (Zod-validiert)
- Bei TypeScript: Drizzle + drizzle-kit, Schema als TS-Code in
  src/shared/db/schema.ts. Sonst Migrations-Tooling der Haus-Konvention
  der jeweiligen Sprache.
- Migration 0001 = leer/init
- Health-Endpoint prüft DB-Erreichbarkeit mit

## Out of Scope
Jede fachliche Tabelle. Das Datenmodell ist Purpose (-> st-090).
