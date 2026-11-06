# ADR-010: Rollen & Rechte (RBAC)

- Datum: 2026-11-06
- Entscheidung: **RBAC** (Pflicht, keine Option)

## Festlegungen
- Es gibt Rollen, und Rollen haben Rechte
- Eine Rolle ist eine Sammlung von Rechten — nichts weiter
- Autorisierung prüft **immer** ein verknüpftes Recht, **niemals** eine Rolle direkt
- Kein `if (user.role === "admin")` — stattdessen `if (user.can("invoice.approve"))`
- Ist eine Autorisierung unklar, lautet die erste Frage: **brauchen wir dafür eine Rolle?**
- Ein Rechte-Check direkt gegen eine Rolle ist ein **Verstoß** gegen dieses ADR,
  kein Stilproblem

## Konsequenzen
- Rollen- und Rechte-Gerüst ist Teil des Skeletons
- Konkrete Rollen und Rechte sind fachlich, nicht Teil dieses ADR
