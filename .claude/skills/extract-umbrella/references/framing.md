# Why ADRs are the foundation for AI-First development

## The problem with conventional codebases for AI workflows

When an AI agent reads a codebase to write a new feature, it sees the *code*
but not the *decisions* behind it. That gap creates predictable failure modes:

- The agent introduces a new pattern that contradicts an existing convention,
  because nobody told it the convention is intentional.
- The agent picks a "reasonable default" (e.g. fetching data with a fresh
  HTTP client) when the codebase has a deliberate pattern (a typed, retried
  client wrapper) that wasn't visible from the immediate task scope.
- The agent suggests a refactor that violates a constraint nobody wrote down
  (e.g. "we don't use Mediator in the frontend service because it adds latency
  to user-perceived flows").
- Two AI sessions on the same project make incompatible decisions because
  neither has access to the implicit shared context.

In a human team, this is solved by tribal knowledge — informal hallway
conversations, code-review feedback, "ask Senior X before doing Y." AI
agents have no access to tribal knowledge. They need it to be written down.

## What ADRs solve

An Architecture Decision Record names:

1. The **decision** (what the system does, as a fact)
2. The **context** (why this was chosen over alternatives)
3. The **consequences** (what follows from this — both good and bad)

For an AI agent, the value is not historical archaeology. It's a binding
constraint: "if you change this, you violate ADR-N — flag it instead of
silently doing it."

## The Spec-First / AI-First workflow this enables

1. Engineer writes a **spec** for a new feature.
2. Spec is checked against **all accepted ADRs** — does it violate any
   architectural constraint? If yes: either revise the spec, or write a new
   ADR explicitly superseding the old one.
3. Implementation proceeds against the spec, with ADRs as guardrails.
4. AI agents can review specs and code with the same constraint set as humans.

This only works if the ADRs exist. For greenfield projects, you write them
as you go. For brownfield projects, you have to **reverse-engineer** them
from the existing code — that's what this skill does.

## What "reverse-engineered" honestly means

When extracting ADRs from a codebase, we are inferring decisions from
artifacts. Some inferences are highly reliable:

- A `package.json` with `"dependencies": { "@angular/core": ... }` reliably
  indicates "Angular is the frontend framework."
- A consistent `MediatR` usage across all command handlers reliably indicates
  "Mediator pattern is the application boundary."

Other inferences are softer:

- Two services use Repository-pattern, two don't. Is that a decision, an
  inconsistency, or an in-progress migration?
- Some tests use mocks, some hit a real DB. Is that an explicit testing
  strategy, or just "whatever each developer felt like"?

The skill should **mark confidence honestly** in the ADR draft. Soft
inferences become discussion-starters, not facts. The goal is to surface
all the candidate decisions so the team can confirm, refine, or reject them.

## What ADRs are NOT

- They are not implementation details. "We use a 5-second HTTP timeout" is
  config, not an ADR. "We standardize on a single HTTP client wrapper" is.
- They are not a complete documentation. They cover decisions, not all knowledge.
- They are not eternal. ADRs get superseded. Mark old ones as Superseded
  with a pointer to the new ADR — don't delete them.

## The minimum viable ADR set for an AI-First project

Roughly: any decision an AI agent would otherwise have to guess about.
That typically includes (non-exhaustive):

- Primary language and runtime version
- Repo form (mono / multi / hybrid) and tooling
- Frontend framework + state management
- Backend framework + application architecture pattern
- Persistence (database choice + ORM/access pattern)
- API style and contracts
- Auth/identity provider
- Test strategy (units of testing, what's mocked, what's real)
- Deployment target and process
- Observability stack

`references/adr-domains.md` has a longer checklist.
