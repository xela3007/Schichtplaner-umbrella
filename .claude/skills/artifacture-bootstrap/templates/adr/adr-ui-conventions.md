# ADR-{n}: UI-Konventionen

- Datum: {date}
- Entscheidung: **Tailwind + shadcn/ui, Formulare gegen Zod**

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

## Konsequenzen
- Prüfmaßstab im Code-Review für jede UI-Story
- Ein Wechsel der Komponentenbasis ändert dieses ADR, nicht den Frontend-Stack
