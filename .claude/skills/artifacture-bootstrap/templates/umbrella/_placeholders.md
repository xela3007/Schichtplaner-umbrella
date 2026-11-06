# Platzhalter der Umbrella-Templates

Werte, die der Skill in Phase 8 einsetzt. Keine Platzhalter erfinden, keine
weglassen — ein nicht ersetztes `{{...}}` landet sonst sichtbar im Repo des
Nutzers.

## Alle Templates

| Platzhalter | Wert |
|---|---|
| `{{PROJECT_NAME}}` | Projektname aus Phase 3 (Default: Ordnername) |
| `{{TODAY}}` | Datum der Derivation, ISO (`YYYY-MM-DD`) — aus `manifest.json.derived_at` |
| `{{MODE}}` | `fasttrack` oder `advanced` — aus `manifest.json.mode` |
| `{{CATALOG_VERSION}}` | aus `manifest.json.catalog_version` |

## `.claude/settings.json` und `.mcp.json` — nicht anfassen

Beide kommen aus dem ausgelieferten ZIP und sind beim Bootstrap-Lauf schon da:
`settings.json` registriert das Auto-Approval-Hook und die Permission-Defaults,
`.mcp.json` trägt die Artifacture-Anbindung samt Token.

Der Bootstrap **schreibt und überschreibt sie nicht.** Sind sie unerwartet
nicht vorhanden, ist das ZIP unvollständig entpackt — sag es dem Nutzer, statt
sie zu rekonstruieren. Und niemals den Token aus `.mcp.json` lesen, ausgeben
oder in eine Vorschau aufnehmen.

## `gitignore.tpl`

Keine Platzhalter — die Datei ist statisch. `src/*` wird **immer** ignoriert,
unabhängig von `repo_form`.

Grund: **das Umbrella ist immer ein eigenes, code-freies Repo.** Es trägt
`ADR/`, `Docs/`, `CLAUDE.md` und `bootstrap.lock`. Was unter `src/` liegt, ist
in jedem Fall ein *anderes* Repo mit eigener Historie — `repo_form` entscheidet
nur, ob es **ein** Code-Repo ist oder **mehrere** Service-Repos.

Deshalb liegen `package.json` und `tsconfig.json` nie im Umbrella, sondern im
jeweiligen src-Repo. Der Path-Alias `#shared/*` aus dem Sprach-ADR gilt
innerhalb des Code-Repos, nicht über die Umbrella-Grenze hinweg.

## Kein `.mcp.json` mehr

Frühere Versionen (`init-artifacture-umbrella`) schrieben eine `.mcp.json`
mit Bearer-Token und hatten dafür eine Warnung in der `.gitignore`. Beides
ist entfallen: der MCP ist beim Bootstrap-Lauf schon angebunden, der Token
kommt über ein Setup-Script. Falls dir trotzdem ein Token begegnet —
**niemals loggen, niemals zurückspiegeln**, auch nicht in Diffs.
