# nozilla — Vorlagen für Google Docs & Slides

CI-konforme Vorlagen: Papier-Gelb, Tinte-Schwarz, Signal-Grün, Zilla Slab · Inter · Space Mono,
scharfe Kanten, harte Schatten. Platzhalter stehen durchgängig in `[ECKIGEN KLAMMERN]`.

---

## 📄 Google Docs — 12 Vorlagen

Liegen im Google Drive unter **nozilla — CI Vorlagen › 01 — Dokumente**:

| # | Vorlage | Wofür |
|---|---------|-------|
| 01 | Anschreiben | Angebots- und Bewerbungsanschreiben |
| 02 | Geschäftsbrief | Formeller Brief, DIN-5008-nah, mit Fußzeile |
| 03 | Konzeptpapier | Ausgangslage → Ziel → Ansatz → Phasen → Risiken |
| 04 | Angebot | Leistungstabelle mit Summen, Rahmenbedingungen |
| 05 | Projekt-Briefing | Problem, Zielgruppe, Erfolgskriterien, Grenzen |
| 06 | Meeting-Protokoll | Entscheidungen, Aufgaben (wer/bis wann) |
| 07 | Statusbericht | Ampel, Fortschritt, Blocker, nächste Woche |
| 08 | Pressemitteilung | Schlagzeile, Lead, Zitat, Boilerplate |
| 09 | Workshop-Agenda | Ablauf, Vorbereitung, Spielregeln |
| 10 | Rechnung | Positionen, USt., Bankverbindung, Pflichtangaben |
| 11 | Projektsteckbrief | One-Pager: Aufgabe → Lösung → Ergebnis |
| 12 | Onboarding | Willkommen, erste Tage, Zugänge, Arbeitsweise |

**Tipp:** Für den vollen Papier-Look in Docs die Seitenfarbe auf `#FFFEE5` setzen —
*Datei › Seiteneinrichtung › Seitenfarbe*. Die Vorlagen selbst nutzen Papier-Gelb
für Akzentboxen, damit sie auch auf Weiß sauber drucken.

Neues Dokument daraus: *Datei › Kopie erstellen*.

---

## 📊 Google Slides — 2 Decks

| Datei | Inhalt |
|-------|--------|
| [`google-slides/nozilla-slides-master.pptx`](./google-slides/nozilla-slides-master.pptx) | **19 Folien** Präsentations-Master |
| [`google-slides/nozilla-slides-icons.pptx`](./google-slides/nozilla-slides-icons.pptx) | **11 Folien** Icon-Bibliothek |
| [`google-slides/nozilla-slides-pitch.pptx`](./google-slides/nozilla-slides-pitch.pptx) | **12 Folien** Pitch-Deck |

Alle Decks laufen auf **weißem Grund** (Papier-Gelb bleibt der Palette vorbehalten);
dunkle Folien für Titel, Kapitel und Kontakt sind eingebaut.

**Import:** Datei in Google Drive ziehen → Rechtsklick → *Öffnen mit › Google Präsentationen*.
Alternativ in Slides: *Datei › Importieren › Hochladen*.

### Master — Layouts
Titel (hell + dunkel) · Agenda · Kapiteltrenner (grün + Tinte) · Fließtext · Zwei Spalten ·
Drei Karten mit Icons · Statement · Zitat · Kennzahlen · Vorgehen/Stepper · Tabelle ·
Bild + Bildunterschrift · Leistungsraster · Team · Nächste Schritte · Kontakt (dunkel) ·
Stil-Referenz.

### Pitch-Deck — Aufbau
Titel · Problem · Warum jetzt · Lösung · So funktioniert es · Produkt · Nutzen ·
Warum nozilla · Referenz · Team · Investition · Nächster Schritt.

### Icon-Bibliothek
Alle **61 Icons** (33 Heavy-Stroke, 4 Pixel-Art, 24 Konzept) in allen Dialekten, hell **und** invertiert, plus die Wortmarke auf Weiß / Signal-Grün / Tinte-Schwarz.

> Die Icons sind **native Vektor-Shapes**, keine Bilder — in Slides direkt umfärbbar,
> skalierbar und ohne Qualitätsverlust. Einfach anklicken, kopieren, in die eigene Folie
> einfügen.

---

## 🔧 Decks neu bauen

```bash
pip install python-pptx
cd templates/google-slides/build
SCRATCH=. python3 mkdeck.py          # erzeugt beide .pptx
SCRATCH=. python3 preview.py nozilla-slides-master.pptx preview.html   # HTML-Vorschau
```

`icons.py` ist die **einzige Quelle** für alle Icons: dieselben Definitionen erzeugen die
Vektor-Shapes im Deck *und* die SVGs in `project/assets/` (64er-Raster, 4 px Umriss,
square caps, miter joins). Web und Slides können damit nicht auseinanderlaufen.

```bash
python3 -c "import sys; sys.path.insert(0,'.'); import icons; \
  [open(f'../../../project/assets/icon-{s}.svg','w').write(icons.to_svg(s)) for s,_,_ in icons.ALL]"
```

`preview.py` liest die **erzeugte Datei** zurück und rendert sie als HTML — so lassen sich
Layout, Farben und Textlängen prüfen, ohne PowerPoint oder LibreOffice.

---

**nozilla CI — v1.0** · Fragen? contact@nozilla.de · _Gute digitale Dienste._
