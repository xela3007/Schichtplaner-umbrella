# Was ein ADR ist — das Regelset

Diese Datei ist die Prüfgrundlage. Sie steht getrennt von `SKILL.md`, damit
man sie zitieren kann, ohne den Ablauf mitzulesen.

---

## Regel 0 — die Wurzel

> **Was im Kontext liegt, wirkt.** Geltung entsteht durch **Anwesenheit**,
> nicht durch Markierung.

Ein LLM liest jedes ADR im Ordner. Eine Metazeile, die sagt "das hier gilt
nicht", ist eine **Bitte**, den folgenden Text zu ignorieren — und diese
Bitte ist probabilistisch. Bei jedem Lesevorgang neu ausgewürfelt, in jedem
Kontextfenster, mit jedem Modell anders.

Der Fehlerfall ist der schlimmstmögliche: Eine verworfene Entscheidung wird
still befolgt, und niemand merkt es, weil das ADR ja "korrekt" dokumentiert
war.

Das ist derselbe Fehler wie `// diese Funktion nicht mehr benutzen` neben
einer exportierten Funktion. Wer sie importiert, importiert sie.

**Determinismus ist kein Stilwunsch, sondern die Kernanforderung von Context
Engineering.** Jede Regel unten ist entweder eine Folge daraus oder eine
Formfrage. Bei Zweifelsfällen ist Regel 0 der Maßstab.

Die verbreitete ADR-Praxis (`Status: superseded by ADR-012`) stammt aus einer
Zeit, in der ADRs von Menschen gelesen wurden, die Metazeilen zuverlässig
beachten. Für LLM-Kontext ist sie kaputt.

---

## A — Geltung (blockierend)

Verstöße gegen A sind **blockierend**: Sie brechen den Determinismus. Ein
Repo mit A-Verstoß hat keine verlässliche Architektur-Grundlage, egal wie
gut die einzelnen Entscheidungen sind.

### A1 — Ein ADR in `ADR/` gilt

Es gibt keinen zweiten Zustand. Kein "vorgeschlagen", kein "teilweise", kein
"veraltet".

### A2 — Kein Status, der Nichtgeltung behauptet

Verboten: `proposed`, `draft`, `rejected`, `superseded by`, `deprecated`,
`obsolet`, "veraltet", "gilt nicht mehr", "überholt".

`Status: accepted` ist erlaubt — es behauptet Geltung und widerspricht A1
nicht. Nötig ist es nicht.

### A3 — Was nicht mehr gilt, liegt nicht mehr in `ADR/`

Gelöscht, oder verschoben nach `Docs/adr-archiv/` — also **außerhalb des
Pfades, den Claude als bindend liest**. Git hält die Historie ohnehin.

### A4 — Änderungen werden im ADR selbst vollzogen

Der alte Text wird **ersetzt**, die Änderung mit Datum vermerkt:

```markdown
- Status: accepted, geändert 2026-08-16

## Korrektur 2026-08-16: `@shared/*` → `#shared/*`
```

**Kein zweites ADR, das das erste ablöst.** Dann lägen beide im Ordner und
beide würden gelesen — genau der Widerspruch, den D1 verbietet.

### A5 — Keine zwei Fassungen derselben Entscheidung nebeneinander

"Früher X, jetzt Y" ist als Korrekturhinweis in Ordnung. "X … Y" ohne
Auflösung ist es nicht: Welche Fassung gewinnt, wird dann Zufall.

### A6 — Keine bedingte Geltung

Verboten: "vorläufig", "bis mehr Bedarf entsteht", "gilt, außer wenn",
"optional", "bewusste Abweichung" als Weichmacher, "flaches Modell, bis…".

**Bedingte Geltung ist im LLM-Kontext keine Geltung.** Was gelten soll, steht
unbedingt da.

### A7 — Ein ADR hat keine offenen Punkte

Ein Abschnitt "Offen", "TBD", "noch zu klären", "Offene Fragen" ist ein
**harter FAIL**.

Begründung aus Regel 0: Ist etwas nicht entschieden, kann es nicht gelten.
Was nicht gelten kann, hat im Ordner nichts zu suchen. Und ein "Offen"-Block
im Kontext signalisiert Spielraum — genau das soll ein ADR nicht.

**Die Klärung passiert vor dem Commit, nicht danach.** Ist eine Frage nicht
entscheidbar, geht sie ins Board, und das ADR wartet.

Häufigster Fall in der Praxis: Im "Offen"-Block stehen **zwei verschiedene
Dinge** gemischt — echte offene Fragen und Festlegungen, die nur im falschen
Abschnitt gelandet sind. Der Prüfer muss das trennen (siehe `SKILL.md`,
Abschnitt A7-Auflösung).

---

## B — Substanz: entscheidet das ADR etwas?

Verstöße gegen B sind **Mängel**, nicht blockierend. Sie machen das ADR
wertlos, aber nicht gefährlich.

### B1 — Die Entscheidung steht im Kopf, in einer Zeile

Nicht erst nach drei Absätzen. Wer scrollen muss, um die Entscheidung zu
finden, liest sie nicht.

### B2 — Jede Festlegung ist verletzbar

Man muss dagegen verstoßen können.

- ✗ "Wir achten auf Qualität" — dagegen kann man nicht verstoßen
- ✓ "Autorisierung prüft immer ein Recht, niemals eine Rolle direkt" —
  `if (user.role === "admin")` ist ein Verstoß

Prüffrage: *Wie sieht der Verstoß aus?* Keine Antwort → keine Festlegung.

### B3 — Keine Optionen

"könnte", "man könnte erwägen", "je nach Bedarf", "denkbar wäre". Ein ADR
**wählt**.

### B4 — Konsequenzen sagen, was zu tun ist

- ✓ "Braucht eine Auth-Story; Rollen-Gerüst ist Teil des Skeletons"
- ✗ "Verbessert die Sicherheit", "erhöht die Wartbarkeit"

### B5 — Keine Wiederholung der Entscheidung als Festlegung

Die Entscheidung steht im Kopf (B1). Eine erste Festlegung, die sie nur
wiederholt, ist Projektkontext und keine Festlegung:

```markdown
- Entscheidung: **Railway**

## Festlegungen
- Railway als Target für die Skeleton- und frühe Produktphase   ← doppelt
- Zwei Services aus einem Repo: API und statisches Frontend     ← Festlegung
```

Prüffrage: *Steht das schon im Kopf?* Dann weg. Was bleibt, sind die
Festlegungen, die **aus** der Entscheidung folgen.

Die Zeile im Beispiel ist zusätzlich ein A6-Verstoß: "für die frühe
Produktphase" befristet die Geltung. Was gilt, gilt unbefristet — oder das
ADR wird geändert (A4).

Typische Formen dieses Verstoßes:

| Muster | Warum es raus muss |
|---|---|
| "X als Target für Phase Y" | Wiederholung + Befristung |
| "Wir setzen auf X" (als erste Festlegung) | Steht im Kopf |
| "X ist für dieses Projekt gesetzt" | Sagt nichts über das Wie |
| "Zunächst X, später evtl. Y" | A6 — bedingte Geltung |

### B6 — Was keine Bindungswirkung hat, ist kein ADR-Inhalt

> Prüffrage: *Wie sieht der Verstoß aus, und was kostet er?*
>
> Keine Antwort → gehört nach `Docs/` oder in `CLAUDE.md`, nicht in `ADR/`.

Das ist die Regel, die die meiste Länge austreibt. Ein ADR-Ordner wird bei
jeder Story mitgelesen; alles darin muss diesen Platz verdienen.

| Gehört ins ADR | Gehört nicht ins ADR |
|---|---|
| "Kein Deploy ohne grüne CI" | "Das Web-UI ist bequemer als die CLI" |
| "Secrets nur als Plattform-Variablen" | Konto- und Workspace-Namen |
| "Migrationen laufen vor dem Start" | Wie man Logs zieht |
| "Service-Zuordnung liegt im Repo" | "MCP ist der Default-Weg, CLI geht auch" |

Der letzte Fall zeigt das Muster: Wer die CLI statt MCP nimmt, verstößt gegen
nichts — das Ergebnis ist identisch. Es ist **Bedienwissen**, keine
Entscheidung. Es veraltet auch anders: Ändert der Anbieter sein Werkzeug, ist
eine Anleitung überholt, ohne dass eine Entscheidung falsch geworden wäre.

Bedienwissen ist nicht wertlos — es ist nur am falschen Ort. Der Prüfer hat
hier eine dritte Aktion neben "reparieren" und "melden": **umsiedeln**, mit
Zielort im Vorschlag.

Grenzfall: "MCP ist der Default" **wird** bindend, sobald daran eine Folge
hängt ("Zugänge werden nur über MCP vergeben, damit kein Token im Umlauf
ist"). Dann steht die Folge im ADR, nicht die Präferenz.

---

## C — Form: Stichpunkte, keine Prosa

C-Verstöße sind **autokorrigierbar**. Hier verdichtet der Skill selbst.

### C1 — Festlegungen sind Stichpunkte

Keine Fließtext-Absätze.

### C2 — Max. zwei Zeilen pro Stichpunkt

**Ausnahme: Absperr-Gründe nach C3.** Die dürfen ausführlich sein, weil ihre
Länge Arbeit spart. C2 ist damit kein Längenlimit, sondern ein Prosa-Limit.

### C3 — Gründe nur, wenn die Festlegung ohne sie falsch aussieht

Das ist die **Bedingung**, nicht das Verbot:

> Prüffrage: *Würde jemand diese Festlegung für einen Fehler halten und
> "reparieren"?*
>
> - **Ja** → Grund ist Pflicht, auch wenn er zwei Zeilen braucht
> - **Nein** → Grund weglassen

**Absperr-Gründe (bleiben):**

| Festlegung | Ohne Grund passiert |
|---|---|
| `#shared/*` statt `@shared/*` | Der Nächste nimmt den vertrauteren `@`-Alias → `ERR_MODULE_NOT_FOUND` |
| `SameSite=None` beim Refresh-Cookie | Sieht nach Lücke aus → jemand stellt auf `Lax` → jeder Refresh scheitert, unsichtbar für curl |
| Fehlender `RESEND_API_KEY` bricht den Start nicht ab | Sieht nach Schlamperei aus → jemand baut ein `throw` ein → lokale Entwicklung tot |
| `sql.transaction([...])` als einzige Atomarität | Jemand will `db.transaction()` "reparieren" — der Treiber kann es nicht |

Gemeinsame Signatur: **Die Festlegung sieht falsch aus, ist aber richtig.**

**Nachschlag-Gründe (raus):**

- Werkzeug-Marketing: "leichtgewichtig", "moderne API", "gute DX",
  "Web-Standard-APIs"
- Lehrbuchwissen: was JWT ist, wie RLS funktioniert
- Abwägungen gegen Alternativen, die nicht gewählt wurden
- Alles, was auch in der Doku des Werkzeugs steht

Beispiel: *"Warum haben wir uns für Hono entschieden?"* — Niemand hält "wir
nehmen Hono" für einen Fehler. Grund raus.

### C4 — Kein Lehrbuch

Ein ADR erklärt nicht, was JWT ist.

### C5 — Max. 12 Festlegungen

Darüber Begründungspflicht. **Keine Zeilengrenze pro Datei** — ein
Deployment-ADR braucht zu Recht mehr Festlegungen als eines über
Tenant-Isolation. Die Grenze gehört auf die Zahl der Festlegungen, nicht auf
Zeilen.

---

## D — Konsistenz über alle ADRs

Das kann nur ein Prüfer über den ganzen Ordner, kein Template.

### D1 — Kein Widerspruch zwischen ADRs (blockierend)

Zwei ADRs im Ordner, die sich widersprechen, sind **beide** im Kontext — und
welches gewinnt, ist Zufall. Das ist Regel 0 in ihrer schädlichsten Form.

### D2 — Eine Frage, ein ADR — und ein ADR, eine Frage

Zwei Richtungen, beide Verstöße:

**Eine Frage in zwei ADRs.** Doppelte Zuständigkeit — `APP_TIMEZONE` gehört in
das Persistenz-ADR **oder** woanders, nicht in beide. Nach Regel 0 liegen dann
zwei Fassungen im Kontext.

**Zwei Fragen in einem ADR.** Fällt leicht durch, weil das ADR ja "eine"
Entscheidung im Kopf trägt — die Festlegungen antworten aber auf zwei
verschiedene Fragen. Erkennungsmerkmal: Ein Teil der Festlegungen bleibt
gültig, wenn die Entscheidung im Kopf sich ändert.

Beispiel: Ein Deployment-ADR, das "Anbieter X" entscheidet und darunter sowohl
anbieterunabhängige Festlegungen (Docker statt implizite Builds, Migrationen
vor dem Start, Secrets nie im Repo) als auch anbieterspezifische
(Konfigurationsdateien, CI-Gate-Einstellung, TLS-Terminierung) führt. Wechselt
der Anbieter, bleibt die erste Hälfte richtig.

**Prüffrage:** *Was, wenn die Entscheidung im Kopf kippt — welche Festlegungen
überleben?* Überleben viele, sind es zwei ADRs.

Das ist ein Finding, keine Aktion: Ein ADR aufzuteilen ist eine
Architekturentscheidung und gehört dem Team.

### D3 — Verweise auf andere ADRs existieren wirklich

Ein toter Verweis ist falsche Sicherheit.

### D4 — Nummer im Dateinamen = Nummer im Titel

Geht beim Umnummerieren kaputt.

### D5 — Nummernlücken: einmal fragen, nicht melden

Eine fehlende Nummer ist meist Absicht (gelöschtes ADR nach A3). **Kein
Finding** — höchstens eine Rückfrage, und nur einmal.

---

## Was ausdrücklich NICHT geprüft wird

| Nicht geprüft | Grund |
|---|---|
| Status-Vokabular jenseits von A2 | A1 macht Status überflüssig |
| `superseded`-Ketten | Nach A4 existieren sie nicht |
| Pflicht-Abschnitt "Alternativen erwogen" | Produziert genau die Prosa, die C3 austreibt |
| Pflicht-Abschnitt "Kontext" | Dito — der Grund gehört in die Entscheidungszeile |
| Zeilenlimit pro Datei | Bestraft ADRs, die zu Recht lang sind |
| **Drift gegen den Code** | Eigener Skill — braucht Zugriff auf `src/` und andere Werkzeuge |

---

## Schweregrade

| Grad | Regeln | Bedeutung |
|---|---|---|
| **blockierend** | A1–A7, D1 | Determinismus verletzt. Muss weg, bevor das ADR verlässlich ist |
| **Mangel** | B1–B4, D2–D4 | ADR ist schwach oder inkonsistent, aber nicht gefährlich |
| **verdichtbar** | C1–C5 | Der Skill räumt selbst auf |
