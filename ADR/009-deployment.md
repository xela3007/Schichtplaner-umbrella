# ADR-009: Deployment-Verfahren

- Datum: 2026-11-06
- Entscheidung: **Railway (Haus-Default)** (Haus-Default, unverändert übernommen)

## Festlegungen
- Zwei Services aus einem Repo: API und statisches Frontend, jeweils mit
  **eigenem Dockerfile** und eigener Service-Konfiguration
- **Docker statt impliziter Buildpacks.** Buildpack-Builds sind undurchsichtig
  und brechen an Kleinigkeiten (gemountete Cache-Verzeichnisse, fehlende
  devDependencies im Build-Image). Ein Dockerfile macht Build- und
  Runtime-Schritt explizit und ist lokal identisch reproduzierbar
- Multi-Stage-Builds: devDependencies bleiben im Build-Stage. Die API läuft als
  unprivilegierter User, das Frontend als statisches Bundle hinter einem
  Webserver
- **Frontend-Konfiguration zur Laufzeit, nicht zur Build-Zeit.** Vite kompiliert
  `VITE_*` fest ins Bundle; ein Image wäre damit umgebungsspezifisch.
  Stattdessen schreibt der Container-Entrypoint eine `config.js` aus den
  Umgebungsvariablen. Geschrieben werden **nur** namentlich genannte Variablen
  — niemals die ganze Umgebung, sonst landen Secrets im Browser
- Zwei Environments: **Staging** und **Production**. Staging deployt automatisch
  aus `main`, Production nur auf ausdrückliche Freigabe
- **CORS als Allowlist**, nie als Wildcard: die Auth-Schicht sendet Cookies, und
  mit `credentials` lehnt der Browser `*` ab. Liegen Frontend und API auf
  verschiedenen Domains, scheitert ohne CORS jeder Browser-Request — auch wenn
  `curl` erfolgreich ist
- SPA-Fallback im Webserver: Client-Routen sind keine Dateien und lieferten
  sonst 404 beim Reload
- Cache-Header getrennt: gehashte Assets `immutable`, `index.html` und
  `config.js` `no-cache` — sonst zeigt der Browser nach einem Deploy auf alte
  Asset-Hashes
- **Secrets ausschließlich als Plattform-Variablen.** Nie im Repo, nie in der
  CI-Konfiguration, nie in einer eingecheckten `.env`
- Jede env-Variable wird beim Start Zod-validiert — fehlende Variable heißt
  Startabbruch mit klarer Meldung, nicht `undefined` drei Schichten später
- Migrationen laufen **vor** dem Start der neuen Version, nicht beim ersten
  Request. Schlägt die Migration fehl, startet die neue Version nicht
- **Migrationen müssen mit der vorherigen App-Version kompatibel bleiben.**
  Vorwärts-only (Persistenz-ADR) heißt: Ein App-Rollback nimmt ein
  Schema-Change nicht zurück — eine inkompatible Migration macht Rollback
  unmöglich
- Health-Check ist Deployment-Gate: unhealthy → kein Traffic
- Rollback = Redeploy des vorherigen Commits. Kein Hotfix direkt auf dem
  Server, weil er beim nächsten Deploy spurlos verschwindet
- **Kein Deploy ohne grüne CI**, und kein Deploy vom Laptop

## Konsequenzen
- Die anbieterspezifische Umsetzung (Konfigurationsdateien, CI-Gate-Einstellung,
  TLS-Terminierung, Zugangswege) gehört in ein eigenes ADR — dieses hier gilt
  unabhängig vom Anbieter
- Ein Wechsel des Verfahrens ändert dieses ADR, statt ein zweites daneben zu
  stellen
