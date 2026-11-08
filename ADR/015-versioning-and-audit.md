# ADR-015: Versionsnummer und zentraler Änderungsverlauf

- Datum: 2026-11-08
- Entscheidung: **Optimistische Sperre über Versionsnummer, ein zentraler
  Änderungsverlauf für alle fachlichen Daten**

## Festlegungen

### Versionsnummer (gleichzeitiges Bearbeiten)
- Jeder fachliche Datensatz, den Nutzer bearbeiten, hat eine Spalte
  `version integer not null default 1`
- Der Client schickt bei jeder Änderung die Version mit, die er geladen hat.
  Die Änderung greift nur, wenn sie noch stimmt (`… where id = ? and version = ?`),
  und erhöht die Version um 1
- Passt die Version nicht, antwortet die API mit **409 `version_conflict`** und
  dem aktuellen Stand. Die Oberfläche zeigt einen Hinweis statt still zu
  überschreiben
- Keine Sperren auf Vorrat, kein „gerade in Bearbeitung“-Status

### Zentraler Änderungsverlauf
- Eine gemeinsame Tabelle `audit_events` für alle fachlichen Datenarten:
  `entity_type`, `entity_id`, `action` (z. B. `created`, `updated`,
  `deactivated`, `reactivated`), `actor_user_id`, `occurred_at`,
  `changes` (`jsonb`: je geändertem Feld `{ from, to }`)
- **Nur anhängen** — Einträge werden nie geändert oder gelöscht
- Der Verlaufseintrag entsteht **in derselben atomaren Operation** wie die
  Änderung selbst. Mit dem HTTP-Treiber ohne Transaktionen (ADR-004) heißt
  das: ein einziges Statement mit CTE (`with changed as (update … returning …)
  insert into audit_events … from changed`). So kann es weder eine Änderung
  ohne Verlauf noch einen Verlauf ohne Änderung geben, und eine fehlgeschlagene
  Versionsprüfung schreibt keinen Eintrag
- Keine Secrets, Passwörter oder Tokens im Verlauf (ADR-013)
- Wer einen Verlauf sehen darf, regelt das Recht der jeweiligen Datenart
  (ADR-010)

## Konsequenzen
- Neue fachliche Datenarten bekommen Versionsnummer und Verlauf ohne eigene
  Verlaufstabelle
- Daten, die zusammen geändert werden (z. B. Öffnungszeiten eines Standorts),
  liegen sinnvollerweise in **einer** Zeile (z. B. als validiertes `jsonb`),
  damit Versionsprüfung und Verlauf ein einziges Statement bleiben
- Ein Wechsel des Musters ändert dieses ADR, statt ein zweites daneben zu
  stellen
