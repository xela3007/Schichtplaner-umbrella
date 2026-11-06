---
title: "Erste Domain-Slice (Purpose-Gate)"
---
## Intent
DIES ist die Stelle, an der Purpose in das Projekt einfließt —
kontrolliert, nach laufendem Skeleton, mit einem Menschen im Loop. Der
Bootstrap hat bewusst KEINE fachliche Entscheidung getroffen.

## Spec
- Purpose-Klärung läuft NICHT in dieser Story, sondern:
  1. Produkt-Gespräch (Skill `vision-capture`) — sortiert die Vision in
     Ideas und Insights auf dem Board
  2. Planning-Workflow in Artifacture — Vision-Punkte werden dort zu
     ausgearbeiteten Items, mit menschlicher Freigabe
- Diese Story ist der **Durchstich des ersten Items aus dem Planning**:
  eine Entität, ein Weg von "anlegen" bis "sichtbar".
- Umsetzung: Entität + Migration + Endpoint(s) + minimale View
- Bewusst klein: EINE Entität, EIN Durchstich

## Out of Scope
Alles Weitere. Jede zusätzliche Idee aus dem Vision-Gespräch wird ein
eigenes Item im Planning-Workflow — nicht in diese Story gezogen.

Auch out of scope: die Vision selbst formulieren. Das passiert in
einem Produkt-Gespräch (`vision-capture`), mit dem Nutzer, nicht hier.
