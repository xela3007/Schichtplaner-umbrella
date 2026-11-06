---
title: "Realtime-Kanal ({mode})"
---
## Intent
Server-Push funktioniert Ende-zu-Ende mit einem Heartbeat-Event.

## Spec
- Modus: {mode}
- sse: Streaming-Endpoint + Client-Subscription, Heartbeat alle 30s
- signalr: Hub + Redis-Backplane nach Haus-Pattern, Heartbeat-Broadcast
- Frontend (falls vorhanden) zeigt letzten Heartbeat an

## Out of Scope
Fachliche Events (-> Backlog).
