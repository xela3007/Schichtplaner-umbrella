---
title: "CI-Basics: Build + Checks auf jedem Push"
---
## Intent
Jeder Push wird gebaut und geprüft, bevor irgendetwas Fachliches existiert.

## Spec
- Pipeline: restore/build/test (leerer Testlauf zählt als grün)
- Lint/Format-Check nach Haus-Konvention
- Läuft auf dem Umbrella-Repo (setzt st-010 voraus)

## Out of Scope
Deployment (eigene Story), Coverage-Ziele, fachliche Tests.
