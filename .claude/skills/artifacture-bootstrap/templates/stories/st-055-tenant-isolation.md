---
title: "Tenant Isolation: Row Level Security ab Tag 1"
---
## Intent
Mandantentrennung strukturell verankert, bevor die erste fachliche
Tabelle existiert — nachrüsten ist teuer, jetzt ist es billig.

## Spec
- Postgres RLS: jede Tabelle mit Tenant-Bezug bekommt eine Policy gegen
  eine Session-Variable (`app.tenant_id`)
- Die Variable wird beim Connection-Aufbau gesetzt, nicht pro Query —
  eine vergessene `WHERE tenant_id = ?` darf nicht zum Datenleck werden.
  Bei TypeScript/Drizzle: zentraler Wrapper um den Connection-Bezug.
  Bei .NET: `DbConnectionInterceptor`.
- Membership-Validierung beim Connection-Aufbau (gehört der User zum
  Tenant?)
- RLS-Policy-Vorlage für zukünftige Tabellen dokumentiert (als Anhang zum
  Multi-Tenancy-ADR unter `ADR/`)
- Demo: zwei Seed-Tenants, Isolation per Test nachgewiesen

## Out of Scope
Tenant-Onboarding-Flows, Billing, fachliche Tabellen.
