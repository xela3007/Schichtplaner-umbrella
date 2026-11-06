# ADR domain checklist

A checklist of architectural domains to consider during reverse-engineering.
For each domain, ask: "Is there an observable decision in the codebase here?"
If yes → ADR candidate. If no → flag as "no decision found, may need one."

Not every project needs an ADR for every domain. Use judgement. The goal is
to surface the decisions that exist, not to force decisions that don't.

## Stack & runtime

- [ ] Primary language(s) per layer (frontend, backend, scripts, infra)
- [ ] Runtime version(s) (Node, .NET, JVM, Python, Go)
- [ ] Package managers / dependency tooling
- [ ] Compilation / transpilation strategy

## Repo form

- [ ] Single repo, multi-repo, monorepo
- [ ] Monorepo tooling (Nx, Turbo, Lerna, Pants, Bazel, npm/pnpm/yarn workspaces)
- [ ] Sub-project boundaries and naming conventions
- [ ] Shared code / libraries strategy

## Frontend

- [ ] Framework (React, Angular, Vue, Svelte, Blazor, server-rendered, ...)
- [ ] Routing (file-based, declarative, SSR, SPA, hybrid)
- [ ] State management (Redux, NgRx, Zustand, Pinia, Signals, MobX, ...)
- [ ] Styling (CSS Modules, Tailwind, styled-components, design system)
- [ ] Component library / design system
- [ ] Forms strategy
- [ ] Data-fetching pattern (REST client, SWR/React Query, Apollo, RTK Query)

## Backend

- [ ] Framework / web stack (ASP.NET, Spring, Express/Nest, Django, Rails, FastAPI, ...)
- [ ] Application architecture (MVC, Clean / Onion / Hexagonal, CQRS, vertical slices)
- [ ] Mediation / dispatch (MediatR, custom pipeline, controllers-only)
- [ ] Dependency injection style (built-in container, Autofac, ...)
- [ ] Background jobs / scheduling (Hangfire, Quartz, BullMQ, Sidekiq, custom)
- [ ] Validation pattern (FluentValidation, decorators, manual)

## Persistence

- [ ] Primary database (Postgres, SQL Server, MySQL, MongoDB, ...)
- [ ] ORM / data-access (EF Core, Dapper, Prisma, TypeORM, raw SQL, repositories)
- [ ] Migration strategy
- [ ] Caching layer (Redis, in-memory, none)
- [ ] File / blob storage (S3, MinIO, Azure Blob, local)
- [ ] Search / indexing (Elastic, Postgres FTS, Algolia, Meilisearch)

## API & contracts

- [ ] Style (REST, GraphQL, gRPC, RPC, mixed)
- [ ] Versioning strategy
- [ ] Contract / schema definition (OpenAPI, GraphQL SDL, protobuf)
- [ ] Client generation strategy
- [ ] Real-time (WebSockets, SignalR, SSE, polling, none)

## Auth & identity

- [ ] Identity provider (Auth0, Keycloak, Cognito, custom, none)
- [ ] Auth flow (OIDC, SAML, JWT, session, API keys)
- [ ] Authorization model (RBAC, ABAC, claims-based, custom rules)
- [ ] Multi-tenancy approach (silo, pool, hybrid)

## Testing

- [ ] Test framework(s) per layer
- [ ] What is mocked vs real (DB, HTTP, time, filesystem)
- [ ] Integration vs unit balance
- [ ] E2E framework and scope
- [ ] Test data strategy (fixtures, factories, snapshots)

## Deployment & infrastructure

- [ ] Target platform (Railway, AWS, Azure, GCP, on-prem, hybrid)
- [ ] Deployment unit (container, function, VM, monolith)
- [ ] CI/CD platform and pipeline shape
- [ ] Environment strategy (dev / staging / prod / per-PR)
- [ ] Infrastructure-as-code (Terraform, Pulumi, CloudFormation, Bicep, none)

## Observability

- [ ] Logging (structured, format, sink — Seq, ELK, Datadog, ...)
- [ ] Metrics (Prometheus, OpenTelemetry, custom, none)
- [ ] Tracing (OpenTelemetry, vendor-specific, none)
- [ ] Error tracking (Sentry, Raygun, custom)

## Cross-cutting concerns

- [ ] Configuration management (env vars, config files, secret manager)
- [ ] Feature flags (LaunchDarkly, GrowthBook, custom, none)
- [ ] Internationalization
- [ ] Accessibility commitments
- [ ] Performance budgets / SLOs

## Modularity & boundaries

- [ ] Bounded contexts / domains (if DDD-influenced)
- [ ] Module / service boundaries and ownership
- [ ] What can call what (layering rules)
- [ ] Public / internal API distinction

## Source of truth questions to ask

When uncertain, look for:

- A `README` or `ARCHITECTURE.md` already in the source — sometimes the team
  documented enough that you can lift content directly
- A consistent code pattern across N similar locations — that's a decision
- Outliers from the dominant pattern — those are either bugs, in-progress
  migrations, or unstated exceptions worth flagging
- Test code — testing strategy is often more revealing than production code
