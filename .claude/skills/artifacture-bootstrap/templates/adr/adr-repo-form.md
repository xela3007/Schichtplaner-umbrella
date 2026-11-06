# ADR-{n}: Repo-Form

- Datum: {date}
- Entscheidung: **{answer_label}** {default_note}

## Festlegungen
- Umbrella ist immer ein eigenes, code-freies Repo (`ADR/`, `Docs/`,
  `CLAUDE.md`, `bootstrap.lock`)
- `src/*` ist im Umbrella gitignored — eigener Git-Verlauf
- Diese Entscheidung betrifft nur den Inhalt von `src/`: ein Code-Repo oder
  mehrere Service-Repos
- `single`: ein Checkout, ein `package.json`, ein Commit hält Frontend und
  Backend konsistent
- `multi`: erst sinnvoll, wenn mehrere Teams unabhängig deployen
- Bei `single` gilt der Path-Alias `#shared/*` innerhalb des Code-Repos
  (Sprach-ADR); bei `multi` wandern die Zod-Schemas in ein Shared-Repo und der
  Alias entfällt

## Konsequenzen
- Ein Wechsel `single` → `multi` ändert dieses ADR, statt ein zweites daneben
  zu stellen — zwei ADRs zur Repo-Form wären zwei Wahrheiten im Kontext
