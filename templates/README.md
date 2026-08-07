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
| [`google-slides/nozilla-slides-icons.pptx`](./google-slides/nozilla-slides-icons.pptx) | **5 Folien** Icon-Bibliothek |

**Import:** Datei in Google Drive ziehen → Rechtsklick → *Öffnen mit › Google Präsentationen*.
Alternativ in Slides: *Datei › Importieren › Hochladen*.

### Master — Layouts
Titel (hell + dunkel) · Agenda · Kapiteltrenner (grün + Tinte) · Fließtext · Zwei Spalten ·
Drei Karten mit Icons · Statement · Zitat · Kennzahlen · Vorgehen/Stepper · Tabelle ·
Bild + Bildunterschrift · Leistungsraster · Team · Nächste Schritte · Kontakt (dunkel) ·
Stil-Referenz.

### Icon-Bibliothek
Alle **14 Icons** in beiden Dialekten, hell **und** invertiert, plus die Wortmarke auf
Papier / Signal-Grün / Tinte-Schwarz.

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

`icons.py` zeichnet die Icons als Vektor-Shapes im 64er-Raster (4 px Umriss, square caps,
miter joins) — dieselbe Geometrie wie die SVGs in `project/assets/`.

`preview.py` liest die **erzeugte Datei** zurück und rendert sie als HTML — so lassen sich
Layout, Farben und Textlängen prüfen, ohne PowerPoint oder LibreOffice.

---

**nozilla CI — v1.0** · Fragen? ci@nozilla.de · _Gute digitale Dienste._
