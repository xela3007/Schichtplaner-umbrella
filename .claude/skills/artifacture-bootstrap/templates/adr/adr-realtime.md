# ADR-{n}: Server-Push / Realtime

- Datum: {date}
- Entscheidung: **{answer_label}** {default_note}

## Festlegungen
- Default: Nein
- SSE für unidirektionales Streaming
- SignalR für bidirektional, mit Redis-Backplane als Haus-Pattern
- **Web-Push ist hiervon nicht berührt.** Es hält keine offene Verbindung und
  liefert gerade dann, wenn die App zu ist — eine andere Frage als Realtime

## Konsequenzen
- Bei SSE/SignalR: Realtime-Story mit entsprechendem Modus
