# Die 29 Hausregeln

**Gute digitale Dienste.**

Dieses Dokument beschreibt in [`index.html`](index.html) die Haltung, die
Wortmarke, die Farbzonen, die Schriften, die Formsprache, die Zeichen, die
Sprache und die zehn Regeln. Was hier steht, ist die Ebene darunter: 29 Sätze,
die beim Bauen von Seiten entschieden werden mussten, jeder aus einem Fall, in
dem etwas schiefging.

Sie stammen aus der Webseite von nozilla und gelten dort. Sie stehen hier,
damit sie auch jemand liest, der etwas anderes in diesem Erscheinungsbild
gestaltet: eine Vorlage, eine Präsentation, ein Plakat.

**Sie ersetzen die zehn Regeln des CI nicht.** Die zehn sagen, wie das
Erscheinungsbild aussieht. Diese 29 sagen, was man mit ihm nicht tun darf,
und das ist die Angabe, die auf einer Musterseite fehlt.

Jede Regel, die neu dazukommt, wird an beiden Stellen nachgetragen. Steht sie
nur an einer, gilt in einem halben Jahr die falsche.

---

Sie stehen im Kopf des Stylesheets der Webseite und hier. Wer eine ändert, ändert beide.

1. **Fließtext steht immer auf einer weißen Fläche** (`.nz-sheet` bzw. `--nz-surface`), niemals direkt auf dem Papierton.
2. Auf dem Papierton (`--nz-bg`) stehen nur **Überschriften, Labels und Navigationselemente**.
3. **Signalgrün ist ausschließlich Aktionsfarbe**: Buttons, Links, Hover-Zustände, kleine Marker. Keine Flächen, keine Container, keine Textblöcke auf Grün.
4. Im dunklen Modus übernimmt `--nz-surface` die Rolle der weißen Fläche.
5. **Es gibt genau einen Gelbton** (`--nz-c-paper`). Abgetönte Gelbvarianten sind als Hintergrund nicht zulässig.
6. **Vollflächige Bänder sind weiß.** Schwarz ist die Ausnahme für genau eine besonders hervorgehobene Stelle je Seite (`.nz-band--ink`).
7. **Weiß ist die dominierende Fläche**, Gelb bleibt der ruhige Grund dahinter.
8. **Überschriften in Zilla Slab** dürfen groß auftreten, der Fließtext bleibt eine Spur kleiner.
9. **Navigationspunkte** stehen ebenfalls in Zilla Slab und werden im Hover zur Schaltfläche.
10. **Keine Trennlinien** unter Überschriften oder Hero-Bereichen.
11. **Kein Rahmen**, wenn sich die Fläche ohnehin vom Hintergrund abhebt. Ausnahme: anklickbare Flächen.
12. **Unter jedem Seitentitel steht eine Subline**: ein bis drei Sätze in Zilla Slab, groß, auf dem Papierton, mit deutlichem Abstand nach unten. Fehlt sie, wird der erste Satz des Fließtexts verwendet.
13. **In Sammlungen** steht die Kategorieüberschrift auf dem Papierton, die Bausteine darunter auf Weiß.
14. **Mobil ist die Navigation ein eigenes Blatt** über der Seite: Hauptpunkte bleiben Links, das Aufklappen liegt daneben, und es ist immer nur ein Zweig offen. Im Blatt gibt es keine Trennlinien, weder waagerecht noch senkrecht.
15. **Mobil steht unten rechts eine schwebende Schaltfläche** mit Termin, Anruf und E-Mail. Sie ersetzt dort den Termin-Knopf der Kopfleiste.
16. **Es gibt genau zwei Linien:** durchgezogen 2px in der Textfarbe, wo etwas wirklich getrennt ist, und gestrichelt 2px in derselben Farbe, wo eine Grenze nur angedeutet wird. **Schwache graue Linien gibt es nicht** — eine Linie, die man kaum sieht, hat keine Aufgabe. Als Token: `--nz-rule` und `--nz-rule-dashed`.
17. **Schaltflächen und Tag-Links sind nie durchsichtig.** Die laute ist grün, die normale weiß, die leise weiß mit gestrichelter Linie. Auf dem schwarzen Band ist die leise cremefarben.
18. **Jedes Zeichen des Hauses** (`assets/icon-*`) **trägt genau eine grüne Stelle**, am liebsten eine Fläche: ein gefülltes Quadrat, einen Kreis, einen Körper. Sie markiert im Bild den Punkt, um den es geht. Das ist die einzige Ausnahme von Regel 3. **Illustrationsreihen gehören nicht dazu**, sie folgen der Reihe, zu der sie gehören. Die 48 Figuren des Ausreden-Kompasses sind schwarze Strichzeichnungen mit einer Stelle im Grün der Pinnwand (`#53f9ac`), nicht im Signalgrün des Hauses. Ihr Requisit liegt im Körper (44 × 50 im Rahmen 100 × 120), nicht daneben: Links und rechts bleiben 26 Bildpunkte, und alles Größere läuft aus dem Bild.
19. **Die Bedienelemente der Kopfleiste haben denselben Umriss:** ein Quadrat in der Höhe der Leiste, weiße Fläche, durchgezogene Linie, harter Schatten. Suche, Sprache und Erscheinungsbild stehen als drei gleiche Quadrate nebeneinander. Der Umschalter **zeigt das Ziel, nicht den Zustand** (Mond führt ins Dunkle, Sonne zurück) und trägt kein Wort.
20. **Überschriften brechen um, weil der Satz es verlangt**, nicht weil die Spalte zu eng gesetzt ist. Automatische Silbentrennung greift nur auf schmalen Bildschirmen.
21. **Vor dem Abschlussbaustein steht ein Abstand, nicht drei.** Der letzte Baustein einer Seite nimmt sich keinen eigenen mehr.
22. **Karten einer Übersicht führen ihr Bild über dem Titel**, dann den Titel, dann einen Satz zur Ausrichtung. Eckdaten wie Personenzahl und Dauer gehören auf die Seite dahinter, nicht auf die Karte.
23. **Es gibt genau einen Aufklapper** (`.nz-accordion`): weiße Fläche, durchgezogene Linie, Frage in Zilla Slab, rechts ein Pluszeichen, das sich beim Öffnen zum Kreuz dreht. Die häufigen Fragen, die Fragen auf den Säulenseiten und die Musterbibliothek benutzen dieselbe Bauform. Einzige Ausnahme sind die Karten des Ausreden-Kompasses; sie liegen auf einer Insel mit eigener Palette.
24. **Die breite Kante links ist kein Schmuck.** Sie markiert ausschließlich Hinweisfelder: Sprachhinweis, Datenschutz-Nachtrag, ausstehende Einwilligung, Hinweis zum Honorar. Aufforderungen tragen sie nicht — der Weg weiter steht in einer Zeile auf Weiß, die Betonung liegt im Knopf. Ausgenommen bleiben schmale Marken, die auszeichnen statt zu rahmen: das Zitat im Fließtext und die aktuelle Seite in der Seitenspalte.
25. **Ein Zeichen steht für genau eine Sache.** Eine Menüspalte und die Seite, auf die sie führt, tragen dasselbe; zwei verschiedene Sachen tragen nie dasselbe. Erlaubt ist allein, dass eine Sammelüberschrift aussieht wie das, was sie sammelt: Die Spalte Toolkits trägt die Karten des KI-Toolkits, das in ihr steht. Die Glühbirne gehört den Ideen, nichts sonst.
26. **Der Störer heißt Blase und schiebt sich dazwischen** (`components/Blase.astro`). Er schwebt nicht über dem Text, sondern fährt aus Höhe null auf seine eigene, und der Abschnitt darunter rückt nach. Zwei Fassungen: die Gegenfarbe des Signalgrüns (`#ff0063`) und Schwarz. Beide sind Ausnahmen von Regel 3, und sie sind es nur, weil eine Blase keine Aktion ist und nicht bleibt: Sie lässt sich schließen, und die Entscheidung hält für einen Besuch. Das Grün bleibt dem Knopf. Für Dauerhinweise ist sie nicht gedacht; wer sie auf jede Seite setzt, hat sie abgeschafft.
27. **Eine Zahl in einem Ablauf steht schwarz mit weißer Schrift.** Grün ist die Aktionsfarbe und sagt „hier kann man klicken"; eine Schrittzahl kann man nicht klicken. Das gilt überall, wo Schritte gezählt werden: auf der Startseite, auf den Säulenseiten, in jeder künftigen Abfolge.
28. **Ein Zeichen trägt, wer sammelt.** Übersichtsseiten haben eines rechts vom Titelblock, Einzelseiten nicht; dort steht, wenn überhaupt, ein Bild der Sache selbst. Das Zeichen ist damit eine Ortsangabe und keine Verzierung: Wo eines steht, geht es weiter nach unten. `check_icons.mjs` hält die Regel für die Seitenarten `hub`, `list`, `collection`, `partners` und `service` (Pflicht) sowie `format`, `kompass` und `tool` (verboten). Nur `deep` bleibt offen: Fünf der 29 Seiten dieser Art sind Sammlungen, die nur technisch als Detailseite geführt werden.

29. **Beim Zeigen reagiert nur, was ein Ziel ist.** Ein Schatten, der unter dem Mauszeiger erscheint, sagt „hier kann man klicken". Ein Absatz Fließtext kann man nicht klicken, und wer ihn antworten sieht, sucht ein Ziel und findet keins. Verweise, Schaltflächen, Karten und Aufklapper dürfen sich melden; Textflächen, Kästen und Streifen nicht. `check_browser.mjs` misst es, indem es die Maus darüberfährt.
