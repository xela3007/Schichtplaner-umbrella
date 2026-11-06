---
title: "Umbrella-Repo & ADR-Grundgerüst anlegen"
---
## Intent
Projektstruktur nach Haus-Standard: Umbrella-Repo mit ADR/,
Bootstrap-ADRs (aus dem Intake) eingecheckt, bootstrap.lock mit
Katalog-Version gepinnt, README-Skeleton.

## Spec
- Repo-Layout nach Umbrella-Konvention: /ADR, /Docs, /src
- Das Umbrella ist ein EIGENES, code-freies Repo. `src/*` ist gitignored —
  was dort liegt, hat eigene Git-Historie.
- Alle Bootstrap-ADRs unter ADR/ ablegen (bereits generiert, `001-*.md`)
- bootstrap.lock: catalog_version={catalog_version}
- Sprache Kern-Code: {language}
- Repo-Form: {repo_form} — bei `single` (Default) EIN Code-Repo unter
  `src/`, mit eigenem package.json. Bei `multi` mehrere Service-Repos,
  siehe st-015. Bei `n/a` (CLI/Script) ein Code-Repo.
- Registrierung im Artifacture-Setup-Manifest, damit `get_setup_script`
  den Arbeitsbaum rekonstruieren kann

## Out of Scope
Jeglicher fachlicher Inhalt. Purpose-Fragen -> Backlog.
