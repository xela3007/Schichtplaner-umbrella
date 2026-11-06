---
title: "Deployment: Railway, deploybar ab Tag 1"
---
## Intent
Das Skeleton läuft öffentlich erreichbar auf Railway — jede weitere
Story landet automatisch dort.

## Spec
- Zwei Railway-Services aus EINEM Repo: API + statisches Frontend,
  getrennt über Root-Directory/Watch-Path (ein API-Commit deployt nicht
  das Frontend)
- KEIN eigener Reverse Proxy — Railway terminiert TLS und routet selbst.
  CORS auf der API explizit konfigurieren.
- Deploy aus CI (setzt st-020 voraus), env-Variablen dokumentiert
- Health-Check als Deployment-Gate

## Out of Scope
Custom Domains, Skalierung, eigene Targets, Reverse-Proxy-Setups.
