# ADR-006: Tenant Isolation

- Datum: 2026-11-06
- Entscheidung: **Nein — ein gemeinsamer Datenraum** (Haus-Default, unverändert übernommen)

## Festlegungen
- Strukturell entscheidend: nachträgliche Mandantentrennung ist teuer
- Haus-Pattern bei Ja: Postgres Row Level Security gegen `app.tenant_id`
- Session-Variable beim **Connection-Aufbau** setzen, nicht pro Query — eine
  vergessene `WHERE tenant_id = ?` darf kein Datenleck sein können. Die DB
  erzwingt die Trennung, nicht die Anwendung
- Plus Membership-Validierung
- Umsetzung: TypeScript → zentraler Wrapper um den Connection-Bezug;
  .NET → `DbConnectionInterceptor`

## Konsequenzen
- Bei Ja: Tenant-Isolation setzt auf Persistenz und Auth auf
