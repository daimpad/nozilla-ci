# Übernahme aus der Webseite

**Gute digitale Dienste.**

Dieses Erscheinungsbild gibt es zweimal: hier als Dokument, und in der Webseite
von nozilla, die unter [nozilla.de](https://nozilla.de) läuft. Beide benutzen
dieselben Markennamen (`--nz-*`), denselben Präfix für Bausteine (`.nz-*`) und
dieselben Dateinamen für Zeichen (`icon-*.svg`).

Das ist ein System an zwei Orten. Diese Datei sagt, welcher der beiden recht
hat, wenn sie auseinandergehen, und wie die eine Seite die andere einholt.

## Wer recht hat

**Die Webseite.** Entschieden vom Auftraggeber am 7. August 2026, für die
Marken und für die Zeichen.

Der Grund ist nicht Geschmack. Die Webseite ist die Stelle, an der die Werte
gegen echten Text laufen, in zwei Sprachen, auf 205 Seiten, bei fünf
Bildschirmbreiten und in zwei Erscheinungsbildern, und wo elf Prüfungen bei
jedem Bauen darüber gehen. Eine Musterseite kann eine Größenleiter schön
aussehen lassen; eine Seite mit 350 Wörtern Fließtext kann sie nicht.

**Eine Ausnahme steht unten**, und sie hat einen Grund, den man nachlesen kann.

## Was am 7. August übernommen wurde

Elf Marken, gemessen und nicht geschätzt:

| Marke | vorher hier | jetzt, wie in der Webseite |
| --- | --- | --- |
| `--nz-c-paper-alt` | `#FAF8D4` | `#FFFEE5` |
| `--nz-c-paper-deep` | `#F4F1C4` | `#FFFEE5` |
| `--nz-text-xs` | 11px | 12px |
| `--nz-text-sm` | 14px | 13px |
| `--nz-text-base` | 17px | 16px |
| `--nz-text-lg` | 22px | 21px |
| `--nz-text-xl` | 28px | 34px |
| `--nz-text-2xl` | 40px | 48px |
| `--nz-text-3xl` | 56px | 68px |
| `--nz-text-4xl` | `clamp(56px, 9vw, 128px)` | `clamp(64px, 10vw, 140px)` |
| `--nz-surface-raised` | `#FFFDF0` | `#FFFFFF` |

Zwei Beobachtungen dazu, die den Ausschlag gaben:

* **Die Größenleiter der Webseite ist unten enger und oben weiter.** Fließtext
  muss lesbar sein, Titel dürfen groß sein. Die Leiter hier war in beide
  Richtungen zahmer.
* **Drei Cremetöne unterscheidet niemand auf einem Bildschirm.** Man sieht,
  dass da drei verschiedene Weiß nebeneinanderstehen, aber nicht, welches
  welches ist. Auf Papier wäre das anders; solange dieses Dokument nicht
  gedruckt wird, ist es ein Unterschied ohne Aussage.

## Die eine Marke, die hier bleibt

`--nz-surface-alt` steht in der Webseite auf `#FFFFFF` und hier auf
`var(--nz-c-paper-alt)`.

**Das bleibt so, und zwar bewusst.** Die Webseite setzt die Marke auf Weiß,
weil sie nur ein Weiß hat; hier trägt sie vier Bausteine, und zwei davon sind
Zustände beim Überfahren mit der Maus:

```
code, .nz-code                        Hintergrund
.nz-panel                             Hintergrund
.nz-table tbody tr:hover              Hintergrund
.nz-accordion__item > summary:hover   Hintergrund
```

Setzte man sie auf `#FFFFFF`, wäre sie identisch mit `--nz-surface`, und die
beiden Hover-Zustände hätten keine sichtbare Wirkung mehr. „Die Webseite gilt"
war eine Entscheidung über das Aussehen, keine Erlaubnis, einem Baustein sein
einziges Zeichen zu nehmen.

Wenn dieser Unterschied fallen soll, dann nicht durch Angleichen des Wertes,
sondern durch Übernahme der Lösung, die die Webseite dafür hat: Ihr Aufklapper
antwortet nicht mit einer Fläche, sondern mit einer grünen Unterstreichung
(`text-decoration-color: var(--nz-signal)`, 3px). Das ist die bessere Lösung,
und sie gehört in einen eigenen Schritt, weil sie den Baustein ändert und nicht
nur eine Zahl.

## Wie die Webseite erfährt, was hier passiert

Sofort und automatisch. Die Webseite spiegelt dieses Repository bei jedem Bauen
und vergleicht es mit ihrem Abbild:

```
node scripts/sync_ci.mjs          holt den Stand von hier
node scripts/sync_ci.mjs --check  vergleicht, gehört zu den elf Prüfungen
```

Der Vergleich läuft über die Blob-Kennungen aus `git ls-tree`, also über
Fingerabdrücke des Inhalts. Ein neu gezeichnetes Zeichen hier fällt drüben beim
nächsten Bauen auf, ohne dass jemand daran denken muss.

## Wie dieses Repository erfährt, was dort passiert

Bis heute: gar nicht. Deshalb diese Datei.

Der Weg zurück ist der schwierigere, weil die Webseite in einem **privaten**
Repository liegt. Dieses hier kann sie nicht lesen, und ein Arbeitsablauf hier
kann es auch nicht. Drei Möglichkeiten, in der Reihenfolge, in der sie zu
empfehlen sind:

1. **Die Webseite schiebt.** Ein Arbeitsablauf dort öffnet hier einen Pull
   Request, sobald sich eine gemeinsame Marke ändert. Braucht einen
   Zugriffsschlüssel als Geheimnis im privaten Repository. Das ist der einzige
   Weg, der ohne Menschen auskommt.
2. **Von Hand, aber gemerkt.** Jemand mit Zugriff auf beide Repositories macht
   es, und die Prüfung drüben sagt, wann es fällig ist. So ist es heute
   gelaufen.
3. **Über einen Prompt.** Unten steht er, für den Fall, dass die beiden ersten
   Wege nicht offenstehen.

## Der Prompt

Alles zwischen den Linien ist zum Kopieren gedacht. Er setzt voraus, dass die
Werte der Webseite bekannt sind; sie stehen in der Tabelle oben und, wenn eine
neuere Fassung nötig ist, im Kopf von `web/src/styles/nozilla.css` im privaten
Repository.

---

Du arbeitest im Repository `daimpad/nozilla-ci`. Es enthält das
Corporate-Identity-Dokument von nozilla: `index.html` mit acht Abschnitten,
`design-system.css` mit rund 97 Bausteinen, 92 Kern-Zeichen unter
`project/assets/icon-*.svg` und einen Katalog von 462 Nachbauten unter
`project/assets/icons/nz-*.svg`.

**Deine Aufgabe:** Übernimm die Marken und Zeichen der Webseite von nozilla,
die im privaten Repository `daimpad/nozilla-net` liegt. Der Auftraggeber hat am
7. August 2026 entschieden, dass bei Unterschieden die Webseite gilt, für Marken
wie für Zeichen.

**Was du wissen musst, bevor du etwas änderst:**

1. **Die Kern-Zeichen sind erzeugt, nicht gelegt.** Sie entstehen aus
   `templates/google-slides/build/icons.py` und werden von
   `scripts/build-core-icons.py` als SVG geschrieben. Legst du eine fertige
   SVG-Datei nach `project/assets/`, meldet die Prüfung „gehoert zu keinem Icon
   mehr". Ein neues Motiv gehört in die Quelle, dann läuft der Generator.
2. **Der Stift kennt keinen Bogen.** Die Zeichenbefehle sind `line`, `rect`,
   `solid`, `circle`, `dot` und `poly`. Das ist kein Mangel: Derselbe Code
   zeichnet auch die Formen im Foliensatz, und das CI sagt zur Formsprache
   „Kanten. Immer." Ein Motiv der Webseite, das einen Bogen benutzt, wird hier
   zu einem Kantenzug.
3. **Jedes Zeichen trägt die Signatur.** Ein grünes Quadrat bei 54,54, 6 × 6.
   Der Generator setzt es selbst; du zeichnest es nicht mit. Dafür muss das
   Motiv aus dieser Ecke herausbleiben, und `build-core-icons.py --check`
   prüft genau das mit einer eigenen Freihaltezone.
4. **Fremde Markenlogos werden nicht nachgebaut.** Steht in `ICONS.md` und gilt
   ohne Ausnahme: Die 495 `brands`-Icons von Font Awesome sind Logos fremder
   Unternehmen, markenrechtlich geschützt, und ein Nachbau im Hausstil wäre eine
   unzulässige Veränderung. Bekommst du ein LinkedIn- oder GitHub-Zeichen zum
   Übernehmen, lehne ab und schlage `icon-external` vor.
5. **Die Tafel im Dokument zeigt alle Zeichen.** `index.html` führt zu jedem
   Kern-Zeichen eine Kachel. Kommt eines dazu, kommt die Kachel dazu, sonst ist
   das Dokument unvollständig, und die Mengenangabe im Text stimmt nicht mehr.

**Wie du prüfst.** Lokal alle Schritte aus `.github/workflows/ci.yml`, in dieser
Reihenfolge:

```
xmllint --noout project/assets/*.svg project/assets/icons/*.svg
node scripts/validate-assets.mjs
python3 scripts/build-core-icons.py --check
node scripts/build-icons.mjs --check
node scripts/build-icons.mjs && git diff --quiet -- project/assets/icons ICONS.md icons.html
```

Dazu die Signaturprüfung über beide Sätze: Jede Datei unter
`project/assets/icon-*.svg` und `project/assets/icons/*.svg` muss die Zeichenkette
`x="54" y="54" width="6" height="6" fill="#00FF9C"` enthalten.

**Sprache.** Antworten, Erklärungen und Pull-Request-Beschreibungen auf Deutsch.
Kommentare im Code auf Deutsch; sie erklären, warum etwas so ist, nicht was die
Zeile darunter tut. Commit-Nachrichten auf Deutsch, wie die bestehende Historie.

**Ton.** Kurze Hauptsätze, konkret vor allgemein. Keine Geviertstriche, im
Fließtext ein Komma, bei Label-Paaren ein Mittelpunkt. Keine Ausrufezeichen.
Die vollständigen Regeln stehen in `HAUSREGELN.md`.

**Was du nicht tust.** Keine Zahl erfinden, die du nicht gemessen hast. Ist ein
Wert nicht bekannt, frag danach, statt zu schätzen. Und ändere keinen Baustein,
nur weil eine Marke sich geändert hat: Erst ansehen, was sonst noch an ihr
hängt.

---

*Ende des Prompts.*

## Was zuletzt übernommen wurde

| Wann | Was | Woher |
| --- | --- | --- |
| 7. August 2026 | elf Marken, siehe Tabelle oben | Entscheidung des Auftraggebers |
| 7. August 2026 | `icon-phone`, `icon-callback`, `icon-form` | neu in der Webseite gezeichnet |
| 7. August 2026 | `HAUSREGELN.md`, die 29 Regeln | standen nur in der Webseite |
