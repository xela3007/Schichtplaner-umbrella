# ADR-008: Server-Push / Realtime

- Datum: 2026-11-06
- Entscheidung: **Nein** (Haus-Default, unverändert übernommen)

## Festlegungen
- Default: Nein
- SSE für unidirektionales Streaming
- SignalR für bidirektional, mit Redis-Backplane als Haus-Pattern
- **Web-Push ist hiervon nicht berührt.** Es hält keine offene Verbindung und
  liefert gerade dann, wenn die App zu ist — eine andere Frage als Realtime

## Konsequenzen
- Bei SSE/SignalR: Realtime-Story mit entsprechendem Modus
