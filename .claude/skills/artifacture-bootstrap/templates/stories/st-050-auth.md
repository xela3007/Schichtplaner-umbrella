---
title: "Auth-Schicht: Login + geschützte Referenz-Route"
---
## Intent
Login funktioniert Ende-zu-Ende, eine Referenz-Route ist über ein Recht
geschützt.

## Spec
- Login: E-Mail + Passwort gegen Argon2id-Hash
- Access-Token als JWT (15 min) im `Authorization: Bearer`-Header
- Refresh-Token als httpOnly-/Secure-/SameSite-Cookie, serverseitig
  widerrufbar (Tabelle); Logout widerruft
- Token-Claims tragen Rechte, nicht Rollen
- Rollen- und Rechte-Gerüst nach ADR RBAC: eine Rolle ist eine Menge von
  Rechten
- Autorisierung prüft **immer** ein Recht, **niemals** eine Rolle direkt
- Eine geschützte Beispiel-Route, die genau ein Recht prüft
  (401 ohne Login, 403 ohne Recht, 200 mit Recht)
- Self-Signup: Registrierung mit E-Mail-Verifikation, Rate-Limiting auf dem
  Signup-Endpoint
- Default-Rolle für neu registrierte Nutzer, mit minimalen Rechten
- Seed: ein User, eine Rolle, ein Recht — als Referenz, nicht als Fachmodell

## Out of Scope
- Einladungssystem (eigenes Item im Planning — setzt auf dieser Schicht auf)
- Password-Reset, MFA, SSO
- Fachliche Rollen und Rechte, Zuschnitt der Default-Rolle
