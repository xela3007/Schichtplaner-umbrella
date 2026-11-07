# ADR-013: Logging

- Datum: 2026-11-07
- Entscheidung: **pino, JSON auf stdout**

## Festlegungen
- **pino** als Logger in der API. Kein `console.log` im Anwendungscode — er hat
  kein Level, keine Struktur und landet ungefiltert in den Plattform-Logs
- Ausgabe als **eine JSON-Zeile pro Eintrag auf stdout**. Die Plattform
  (Railway) sammelt stdout ein; die App schreibt keine Log-Dateien
- Lokal (`NODE_ENV=development`) lesbare Ausgabe über `pino-pretty`; in allen
  anderen Umgebungen JSON. `pino-pretty` ist nur devDependency
- Log-Level über die env-Variable `LOG_LEVEL` (Zod-validiert, Default `info`)
- **Jede Anfrage bekommt eine Request-ID**: ein eingehender `X-Request-Id`
  wird übernommen, sonst erzeugt. Sie steht in jedem Log-Eintrag der Anfrage
  und im Response-Header — damit lässt sich eine Fehlermeldung des Nutzers
  einem Log-Eintrag zuordnen
- Pro Anfrage ein Abschluss-Eintrag mit Methode, Pfad, Status und Dauer
- **Geschwärzt werden immer**: `authorization`- und `cookie`-Header,
  `set-cookie` sowie Felder namens `password`, `token`, `refreshToken`,
  `accessToken`, `secret`. Über pino-`redact`, nicht per Hand an der
  Fundstelle — eine vergessene Stelle darf kein Leck sein
- Keine Request-Bodies im Log. Was fachlich nachvollziehbar sein muss, wird
  gezielt geloggt
- Unerwartete Fehler werden mit Stacktrace auf Level `error` geloggt; der
  Client bekommt nur eine generische Meldung plus Request-ID

## Konsequenzen
- Ein Wechsel des Loggers ändert dieses ADR, statt ein zweites daneben zu
  stellen
- Log-Aggregation, Alerting und Tracing sind hier bewusst nicht festgelegt
