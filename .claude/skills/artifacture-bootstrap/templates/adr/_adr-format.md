# ADR-Template-Format

## Platzhalter (von derive.py gefüllt)

```
{n}              laufende ADR-Nummer (001, 002, ...)
{date}           ISO-Datum der Ableitung
{answer_value}   gewählter Options-Wert
{answer_label}   gewähltes Options-Label
{default_note}   "(Haus-Default, unverändert übernommen)" wenn der Default
                 blieb, sonst "(bewusste Abweichung vom Default)"
```

## Aufbau eines Templates

```markdown
# ADR-{n}: <Thema>

- Datum: {date}
- Entscheidung: **{answer_label}** {default_note}

## Festlegungen
- <Stichpunkt>
- <Stichpunkt>

## Konsequenzen
- <was daraus folgt>
```

## Regeln

Die verbindlichen Regeln stehen im `check-adr`-Skill (`RULES.md`). Für
Template-Autoren die drei, an denen es am häufigsten scheitert:

**Keine `Status`-Zeile.** Ein ADR in `ADR/` gilt — es gibt keinen zweiten
Zustand. Ein Status, der Nichtgeltung behauptet, ist eine Bitte an das LLM,
den Text zu ignorieren, und die ist probabilistisch.

**Kein `## Kontext`-Abschnitt.** Er produziert Prosa, die nichts festlegt.
Was erklärt werden muss, gehört als Halbsatz an die Festlegung — und nur
dann, wenn die Festlegung ohne den Grund falsch aussieht und jemand sie
„reparieren" würde.

**Keine offenen Punkte.** Kein „TBD", kein „noch zu klären". Was nicht
entschieden ist, kann nicht gelten und gehört ins Board.

Prüfen mit:

```bash
python3 .claude/skills/check-adr/scripts/compile_adr.py --check <ordner>/
```

## Absperr-Gründe

Ein Grund gehört ins Template, wenn die Festlegung ohne ihn falsch aussieht.
Beispiele aus dem Bestand — alle vier haben die Signatur „sieht falsch aus,
ist aber richtig":

| Festlegung | Ohne Grund passiert |
|---|---|
| `#shared/*` statt `@shared/*` | Der Nächste nimmt `@` → `ERR_MODULE_NOT_FOUND` |
| `SameSite=None` | Sieht nach Lücke aus → jemand stellt auf `Lax` → Refresh scheitert |
| Fehlender Mail-Key bricht Start nicht ab | Sieht nach Schlamperei aus → jemand baut `throw` ein |
| Dev-Proxy prüft `Accept`-Header | Sieht überflüssig aus → Reload liefert rohes JSON |

Nicht ins Template gehören Werkzeug-Marketing („leichtgewichtig", „gute DX"),
Lehrbuchwissen und Abwägungen gegen nicht gewählte Alternativen.
