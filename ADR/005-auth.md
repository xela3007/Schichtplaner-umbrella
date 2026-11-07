# ADR-005: Authentifizierung

- Datum: 2026-11-06
- Entscheidung: **Ja** (Haus-Default, unverändert übernommen)
- Status: accepted, geändert 2026-11-07 (Rate-Limit-Speicher, Login erst nach
  Verifikation, Mail-Anbieter vertagt)

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
- **Rate-Limit-Zähler liegen in der Datenbank**, nicht im Arbeitsspeicher: sie
  überstehen Deploys und gelten über mehrere Instanzen hinweg. Ein Zähler wird
  mit einem einzigen atomaren Upsert erhöht — der HTTP-Treiber kennt keine
  Transaktionen (Persistenz-ADR)
- **Login erst nach bestätigter E-Mail-Adresse.** Vorher antwortet der Login
  mit einem eindeutigen Hinweis, statt eingeschränkt zu funktionieren
- Ein echter Mail-Anbieter wird erst mit einer verifizierten Absender-Domain
  angebunden; bis dahin gilt der `ConsoleMailer`
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
