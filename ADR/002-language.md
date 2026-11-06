# ADR-002: Backend-/Kern-Sprache

- Datum: 2026-11-06
- Entscheidung: **TypeScript (Node, Hono)** (Haus-Default, unverändert übernommen)

## Festlegungen
- TypeScript auf Node, Hono als Server
- Zod an jeder Systemgrenze (Request-Body, Query, externe Antworten)
- `z.infer` als einzige Typquelle — kein separates Typ-Modell
- Kein Contract-Framework (ts-rest, tRPC, OpenAPI-Codegen)
- Kein pnpm-Workspace — ein `package.json` im Code-Repo
- **Typ-Sharing via Subpath-Import `#shared/*`** → `src/shared/*`, deklariert
  im `imports`-Feld der `package.json` **und** in `tsconfig.paths`. Das
  `#`-Präfix ist Pflicht: TypeScript löst `paths` nur beim Kompilieren auf und
  schreibt den Alias unverändert ins JS. Node löst ihn über `imports` auf, und
  dort ist `@` nicht erlaubt — `@shared/*` scheitert zur Laufzeit mit
  `ERR_MODULE_NOT_FOUND`. Vite bekommt denselben Alias über `resolve.alias`
- Zwei tsconfigs mit gemeinsamer Basis: `tsconfig.json` (Node, kein DOM),
  `tsconfig.web.json` (DOM, JSX). Zusammenlegen erzwingt die
  `lib`-Schnittmenge und bricht eine der beiden Seiten
- **Biome** für Linting und Formatierung, nicht ESLint+Prettier
- Regeln werden **gezielt an der Fundstelle** unterdrückt (`biome-ignore` mit
  Begründung), nie global abgeschaltet. Eine global deaktivierte Regel verliert
  ihren Wert für alle künftigen Fälle

## Konsequenzen
- Ein Sprachwechsel ändert dieses ADR, statt ein zweites daneben zu stellen
