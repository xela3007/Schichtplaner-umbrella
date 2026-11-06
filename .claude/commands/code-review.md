# Review & Fix Command

Du bist im "Review & Fix" Modus. Ziel: Die Codebase nach einer Vibe-Coding-Session wieder solide machen. Kein Anzeigenhauptmeister - pragmatische Fixes, keine Grundsatzdiskussionen.

## Phase 1: Stack erkennen

Analysiere kurz:
- Package.json(s) finden → Framework, Test-Runner, Linter erkennen
- tsconfig.json → TypeScript Setup
- Vorhandene Config-Files (eslint, prettier, etc.)

Keine Ausgabe nötig, nur mental notieren für kontextgerechte Fixes.

## Phase 2: Quick Health Checks

Führe diese Checks aus und sammle Ergebnisse:

### 2.1 TypeScript/Build
```bash
npx tsc --noEmit 2>&1 | head -50
```
Bei Fehlern: Direkt fixen oder konkreten Fix vorschlagen.

### 2.2 Linting
```bash
npm run lint 2>&1 | head -50
```
Falls kein lint script: `npx eslint . --ext .ts,.tsx 2>&1 | head -50`

Bei auto-fixable issues: `npm run lint -- --fix` vorschlagen.

### 2.3 Tests
```bash
npm test 2>&1 | tail -30
```
Bei Failures: Ursache identifizieren, Fix vorschlagen.

### 2.4 Security Audit
```bash
npm audit --audit-level=high 2>&1 | head -30
```
Bei kritischen Vulnerabilities: Upgrade-Befehle vorschlagen.

## Phase 3: Code Smell Scan

Suche nach typischen Vibe-Coding-Überbleibseln:

### 3.1 Debug-Reste
```bash
grep -rn "console\.log\|console\.debug\|debugger" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | grep -v "node_modules" | head -20
```
→ Entfernen oder durch proper logging ersetzen.

### 3.2 TODOs & FIXMEs
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -15
```
→ Auflisten, bei offensichtlichen Quick-Wins direkt fixen.

### 3.3 Hardcoded Secrets (kritisch!)
```bash
grep -rn "password\|secret\|api_key\|apikey\|bearer" --include="*.ts" --include="*.tsx" -i src/ 2>/dev/null | grep -v "node_modules\|\.d\.ts" | head -10
```
→ Bei Treffern: Sofort auf env vars umstellen.

### 3.4 Any-Types (TypeScript)
```bash
grep -rn ": any\|as any" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -15
```
→ Bei offensichtlichen Fällen proper typen vorschlagen.


### 3.5 Allgemeine Beispiele
- Sind alle Endpunkte abgesichert?
- Gibt es Code Duplikate?
- Gibt es Monster Dateien? (größer 500 Zeilen)
- Gibt es auffällige Abweichungen im Datenmodell?
- Gibt es ungenutzte Komponenten, Klassen, Daten?
- Ist irgendwo etwas "gemockt"?

## Phase 4: Stack-spezifische Checks

### Falls React/Next.js Frontend:
- `dangerouslySetInnerHTML` ohne Sanitization?
- Fehlende `key` props in Listen?
- useEffect ohne/mit falschem Dependency Array?
- Missing Error Boundaries an kritischen Stellen?

### Falls Express/Fastify/Hono API:
- Routes ohne Auth-Middleware? (Protected routes identifizieren)
- Missing input validation? (Zod/Yup schemas vorhanden?)
- Unhandled async errors? (try/catch oder error middleware?)
- CORS zu offen? (`origin: '*'` in production?)

### Falls Prisma/Drizzle:
- Raw queries ohne Parameter? (SQL Injection)
- Missing indexes bei häufigen Queries?
- N+1 Query Patterns?

## Phase 5: Zusammenfassung & Fixes

Erstelle eine kurze Zusammenfassung:

```
## Review Ergebnis

### ✅ Alles gut
- [Was passt]

### 🔧 Gefixt
- [Was du direkt gefixt hast]

### ⚠️ Sollte gemacht werden
- [Konkrete Fixes mit Code-Snippets, die Review brauchen]

### 📋 Backlog (nice-to-have)
- [Nicht kritisch, aber irgendwann mal]
```

## Wichtige Regeln

1. **Fix first, ask later**: Offensichtliche Fixes (unused imports, console.logs, typos) direkt machen.
2. **Keine Refactoring-Orgien**: Bestehende Patterns beibehalten, auch wenn du es anders machen würdest.
3. **Kontext beachten**: `console.log` in einem CLI-Tool ist okay, in einer React-Komponente nicht.
4. **Pragmatismus**: 80/20 Regel. Die wichtigsten 20% der Issues fixen, nicht jeden Edge Case.
5. **Keine Breaking Changes**: Fixes dürfen nichts kaputt machen. Im Zweifel nur vorschlagen.
