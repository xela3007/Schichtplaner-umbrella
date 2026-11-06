# ADR-{n}: Authentifizierung

- Datum: {date}
- Entscheidung: **{answer_label}** {default_note}

## Festlegungen
- Eigene Auth-Implementierung — kein externer IdP (Auth0, Clerk, Cognito)
- JWT als Access-Token, kurzlebig (15 min), im `Authorization: Bearer`-Header
- Refresh-Token als httpOnly-/Secure-/SameSite-Cookie — für JS nicht lesbar
- Refresh-Token serverseitig widerrufbar (Tabelle); Logout widerruft sofort
- Passwort-Hashing Argon2id — kein MD5, SHA, bcrypt ohne Anlass
- Password-Reset: signierter Einmal-Link, 1 h gültig, bei Nutzung invalidiert
- Token-Claims tragen Rechte, nicht Rollen (siehe RBAC-ADR)
- **Registrierung ist offen**: Self-Signup mit E-Mail-Verifikation. Ein offener
  Signup-Endpoint ist Teil der Angriffsfläche und braucht Rate-Limiting
- Frisch registrierte Nutzer bekommen eine Default-Rolle mit minimalen Rechten
  — nie implizit mehr, weil sie eingeloggt sind
- Einladungen existieren zusätzlich, sind aber keine Alternative zum Self-Signup
- **Mail-Versand hinter einem `Mailer`-Interface.** Ohne API-Key fällt er auf
  einen `ConsoleMailer` zurück, der den Link ins Log schreibt — das hält
  lokale Entwicklung ohne Provider-Konto lauffähig
- Ein fehlender Mail-API-Key bricht den Start **nicht** ab, meldet sich in
  `production` aber unübersehbar auf stderr. Sonst können neu registrierte
  Nutzer sich nie anmelden, ohne dass es jemand merkt
- **Refresh-Cookie bei getrennten Domains:** `SameSite=None` + `Secure` in
  Produktion, `Lax` lokal. Liegen Frontend und API auf verschiedenen Domains,
  schickt der Browser ein `Lax`-Cookie cross-site nicht mit und jeder Refresh
  scheitert. `None` verlangt zwingend `Secure`
- Löschen des Cookies muss dieselben Attribute tragen wie das Setzen — sonst
  ignoriert der Browser die Anweisung
- **Produktion braucht eine verifizierte Absender-Domain.** Test-Absender der
  Mail-Provider funktionieren nur für Tests — echte Mails kommen nicht an oder
  landen im Spam

## Konsequenzen
- Ein Wechsel auf einen externen IdP ändert dieses ADR, statt ein zweites
  daneben zu stellen
