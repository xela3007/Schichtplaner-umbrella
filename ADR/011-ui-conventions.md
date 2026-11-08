# ADR-011: UI-Konventionen

- Datum: 2026-11-06
- Entscheidung: **Tailwind + shadcn/ui, Formulare gegen Zod, visuell im
  Dinexis Design System**
- Status: accepted, geändert 2026-11-08 (Dinexis Design System verbindlich)

## Festlegungen
- Tailwind für Styling — keine CSS-in-JS-Bibliothek, keine parallelen
  `.css`-Dateien pro Komponente
- shadcn/ui als Komponentenbasis: Komponenten liegen als Code im Repo, nicht
  als Paket-Abhängigkeit — anpassbar ohne Fork
- Design-Tokens (Farben, Spacing, Typo) in der Tailwind-Config, nicht als
  Hex-Werte im JSX verstreut
- Formulare: react-hook-form mit Zod-Resolver, gegen **dasselbe** Schema, das
  die API validiert. Client- und Server-Validierung können damit nicht
  auseinanderlaufen
- Client-Validierung ist Komfort, nie Schutz — die API validiert immer erneut
- Ladezustände und Fehler sind sichtbar zu behandeln; kein stiller Leerzustand,
  wenn ein Request fehlschlägt
- Barrierefreiheit als Mindestmaß: Formularfelder haben Labels, interaktive
  Elemente sind per Tastatur erreichbar

### Visuelle Gestaltung: Dinexis Design System (verbindlich)
- **Quelle der Wahrheit** ist das „Dinexis Design System“ der Organisation
  (Claude-Artifact `https://claude.ai/artifact/PJ9eahksQobxufhrrxZRCi`, Dateien
  `project/README.md`, `project/colors_and_type.css`, `project/assets/*.svg`).
  Jede UI-Story gestaltet danach; Abweichungen nur mit Eintrag in diesem ADR
- Die Werte aus `colors_and_type.css` (Farben, Schriftgrößen, Abstände,
  Radien, Schatten, Bewegung) werden **unverändert** als CSS-Variablen in
  `src/web/styles.css` übernommen und auf die shadcn-Token gemappt
  (`--primary`, `--ring`, `--border` …). Keine Hex-Werte im JSX
- Markenkern: weiße Fläche, Anthrazit-Schrift (`--ink`), **Cyan `#0CE8F6`** als
  Akzent (Text/Icons auf Weiß in `--brand-700`), **Magenta** nur sparsam,
  Cyan→Magenta-Verlauf nur für einzelne Akzente; Primär-Buttons als
  anthrazitfarbene Pill (`--graphite-900`), Fokus-Ring `--focus-ring`
- **Logo:** nur die offiziellen SVGs aus dem Designsystem (Wortmarke
  `dinexis.svg`, Monogramm `dx.svg`), als Dateien im Repo — nie nachzeichnen
- **Icons:** Lucide (Linien, Strichstärke 1,75)
- **Schriften:** Schibsted Grotesk (Überschriften), Hanken Grotesk (Text) —
  **selbst gehostet** im Bundle, kein Abruf von Google-Servern zur Laufzeit
  (DSGVO). Sind es noch Ersatzschriften laut Designsystem, werden sie ersetzt,
  sobald die echten Markenschriften vorliegen
- **Nur helles Farbschema.** Ein Dunkelmodus kommt erst, wenn das Designsystem
  ihn definiert — kein selbst erfundenes Dunkelschema
- **Tonalität** nach Designsystem (ruhig, menschlich, kurze Handlungsaufforderungen,
  keine Emojis) — **Ausnahme Anrede: „du“** statt „Sie“, weil der Schichtplaner
  eine interne App für das Empfangsteam ist (Entscheidung 2026-11-08)
- Kontraste mindestens WCAG AA (Text 4,5:1); Cyan `#0CE8F6` ist als Textfarbe
  auf Weiß zu hell

## Konsequenzen
- Prüfmaßstab im Code-Review für jede UI-Story
- Ein Wechsel der Komponentenbasis ändert dieses ADR, nicht den Frontend-Stack
- Ändert sich das Dinexis Design System (z. B. echte Schriften, Dunkelmodus),
  zieht eine eigene Story die Werte in `styles.css` nach
