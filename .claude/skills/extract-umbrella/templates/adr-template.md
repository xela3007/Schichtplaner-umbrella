# ADR-NNN: {{Decision title in plain English}}

**Status:** Proposed (reverse-engineered) | Accepted | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Deciders:** —
**Applies to:** {{scope, e.g. "all backend services" or "frontend only"}}

## Context

What is the situation in the codebase that this decision addresses? Reference
concrete evidence from the code (`path/to/file.ext:line`).

When reverse-engineering: be honest about confidence. If the decision is
clearly visible (single dependency, single config), say so. If it's inferred
from patterns, say "inferred from N occurrences in …".

## Decision

What was decided. Phrase as a present-tense statement of fact about the system,
not a wish or a proposal.

## Consequences

### Positive
- ...

### Negative
- ...

### Risks
- ...

## Evidence

For reverse-engineered ADRs, list the concrete code locations that prove this
decision is in place:

- `path/to/manifest.json` — declares dependency X
- `path/to/file.cs:42` — uses pattern Y
- `path/to/config.yml` — sets option Z

Remove this section once the ADR is reviewed and confirmed (or fold the most
important evidence into Context).
