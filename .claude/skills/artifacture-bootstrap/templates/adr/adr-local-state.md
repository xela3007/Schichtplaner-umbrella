# ADR-{n}: Lokaler Zustand (CLI/Script)

- Datum: {date}
- Entscheidung: **{answer_label}** {default_note}

## Festlegungen
- Zustand liegt lokal (SQLite oder Dateien), nicht in einer Server-Datenbank
- Der Pfad kommt aus einer env-Variable mit Default, nie hart verdrahtet —
  sonst ist das Werkzeug nicht mehrfach parallel nutzbar
- Migrationen gelten auch hier: Schema-Änderungen sind versioniert und laufen
  beim Start, nicht auf Zuruf

## Konsequenzen
- Ein Wechsel auf eine Server-Datenbank ändert dieses ADR, statt ein zweites
  daneben zu stellen
