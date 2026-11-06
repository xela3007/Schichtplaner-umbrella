# ADR-004: Persistenz

- Datum: 2026-11-06
- Entscheidung: **Ja — Postgres (Neon)** (Haus-Default, unverändert übernommen)

## Festlegungen
- Postgres auf Neon, EU-Region
- Drizzle als ORM, Schema als TS-Code in `src/shared/db/schema.ts`
- Migrationen via drizzle-kit, im Repo eingecheckt, **nur vorwärts** — keine
  Down-Migrations
- Kein manueller Eingriff auf der DB. Was nicht als Migration im Repo steht,
  existiert nicht — sonst driftet Prod gegen das Schema und niemand merkt es
- Primärschlüssel: UUID v7 (zeitsortiert), aus der Anwendung. Keine
  Auto-Increment-IDs — sie verraten Datensatzzahlen und kollidieren beim
  Zusammenführen
- Jede Tabelle hat `created_at` und `updated_at` (timestamptz, UTC)
- Zeiten immer `timestamptz` in UTC, Umrechnung erst im Frontend
- Geldbeträge als Integer in kleinster Einheit (Cent) — nie Float
- Kein Soft-Delete im Default. Wo Historie gebraucht wird, ist das eine
  fachliche Entscheidung mit eigener Tabelle, kein `deleted_at`-Flag überall
- Fremdschlüssel sind echte FK-Constraints, nicht nur Konvention
- Connection-Pooling über den Neon-Pooler; die App hält keinen eigenen Pool
- Kein Raw-SQL in Endpoints — Queries liegen in einer Repository-/Query-Schicht
- Der Health-Endpoint prüft die DB-Erreichbarkeit mit
- **Der Neon-HTTP-Treiber kennt keine Transaktionen.** Atomarität über mehrere
  Statements geht nur über den Batch (`sql.transaction([...])`), und der
  verlangt alle Statements vorab — deshalb kommen IDs aus der Anwendung

## Konsequenzen
- Ein ORM-Wechsel ändert dieses ADR, statt ein zweites daneben zu stellen
