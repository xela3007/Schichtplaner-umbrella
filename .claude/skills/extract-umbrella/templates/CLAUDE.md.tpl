# CLAUDE.md — {{PROJECT_NAME}} Umbrella

## What this repo is

This is an **umbrella repository** for {{PROJECT_NAME}}. It contains shared
documentation, ADRs, and diagrams. Application code lives in sub-repos cloned
into `src/`, each with its own git history. Sub-repos are gitignored by the
umbrella.

```
{{PROJECT_NAME}}/
  ADR/        Architecture Decision Records (binding)
  Docs/       Diagrams, transcripts, decision log, discussion notes
  src/        Sub-repos (own git, not tracked by umbrella)
              {{SOURCE_LAYOUT_HINT}}
```

## ADRs are binding

The `ADR/` folder contains Architecture Decision Records. These are
**mandatory constraints** — every spec you write and every implementation
you produce must comply with all accepted ADRs.

ADRs in this repo were **partially reverse-engineered** from the existing
codebase. They are accurate but may need refinement as the team confirms
each decision. Status `Proposed (reverse-engineered)` means: derived from
code, awaiting human confirmation. Status `Accepted` means: confirmed and binding.

Before starting any work:
1. Read all ADRs in `ADR/`
2. Treat `Accepted` ADRs as binding constraints
3. If your task touches a domain that has no ADR (e.g. no decision on a
   relevant pattern), **flag it** — do not guess

## Tech stack snapshot

{{TECH_STACK_SUMMARY}}

For details, see the ADRs.

## Source code

The actual application code lives under `src/`. To work on it:

```bash
# Clone the sub-repo into src/
cd src/
git clone <repo-url> <name>
```

Sub-repos are intentionally gitignored by the umbrella so each project can
keep its own history. The umbrella only tracks documentation and decisions.

## Git rules (umbrella only)

- **Do not commit automatically.** Leave changes for the operator to review.
- **Do not modify files in sub-repos** (`src/`) from this umbrella context
  unless explicitly requested. Sub-repo changes belong in the sub-repo.
- When working in a sub-repo, change directory into it and follow that
  repo's own conventions.

## Keeping the umbrella alive

When the codebase evolves and new architectural decisions are made
informally, run the `extract-umbrella` skill in **sync mode** to detect
drift and surface ADR candidates:

```
/extract-umbrella
```

It will read existing ADRs, scan the source, and report what changed —
without writing anything until you confirm.
