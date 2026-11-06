# ADR-{n}: Frontend-Stack

- Datum: {date}
- Entscheidung: **{answer_label}** {default_note}

## Festlegungen
- React als SPA gegen die API — kein SSR, kein Next.js
- Vite als Build-Tool und Dev-Server
- React Router fürs Routing
- TanStack Query für Server-State (Fetching, Caching, Invalidierung)
- **Kein Redux/MobX/Zustand für Server-Daten.** Server-State gehört in
  TanStack Query, lokaler UI-State in `useState`. Ein globaler Store, der
  API-Daten spiegelt, ist eine zweite Wahrheit und läuft auseinander
- Typen kommen per `#shared/*` aus den Zod-Schemas — keine handgeschriebenen
  API-Typen im Frontend
- API-Basis-URL via env, Zod-validiert beim Start. Im Container kommt sie zur
  **Laufzeit** aus einer generierten `config.js`, lokal aus `import.meta.env`
  — dasselbe Schema validiert beide Quellen
- Kein eigener API-Client-Generator; ein dünner `fetch`-Wrapper reicht
- Ausgeliefert wird ein statisches Bundle, kein Node-Server
- **Access-Token nur im Speicher**, nie in `localStorage`: dort wäre er per XSS
  auslesbar. Nach einem Reload stellt der Refresh über das httpOnly-Cookie die
  Session wieder her
- **Parallele 401 teilen sich einen Refresh-Request.** Ohne diese
  Deduplizierung benutzt der zweite Request einen bereits rotierten Token, und
  die Diebstahl-Erkennung der API widerruft alle Tokens des Nutzers — er wäre
  grundlos ausgeloggt
- **Der Dev-Proxy entscheidet nach Pfad UND `Accept`-Header.** Eine URL wie
  `/groups/<id>` ist zugleich API-Route und Seiten-URL; kein Pfadmuster kann
  das trennen. Ohne Header-Prüfung liefert ein Reload rohes JSON statt der App

## Konsequenzen
- SSR-Bedarf ändert dieses ADR, statt ein zweites daneben zu stellen
- UI-Konventionen stehen im eigenen ADR
