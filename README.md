# nozilla — Corporate Identity Guidelines

**Gute digitale Dienste.**

Ein Leitfaden für Design, Code und Kommunikation bei nozilla.

---

## 📖 Dokumentation

- **Visuelle Version** (mit Farbmustern, Typographie-Beispiele, Icons): [`index.html`](./index.html)
- **Schnell-Referenz für Claude**: [`CLAUDE.md`](./CLAUDE.md)
- **Diese Datei**: Praktische Richtlinien für Menschen

---

## 🎨 Farben

Unsere Palette hat **genau drei Rollen** — mehr nicht.

| Rolle | Name | Farbe | Hex | Verwendung |
|-------|------|-------|-----|-----------|
| **Signal** | nz-green | `#00FF9C` | `#00FF9C` | Buttons, CTAs, grüne Marker, Highlights |
| **Signal** | nz-green-strong | `#00E88D` | `#00E88D` | Hover & Active States |
| **Signal** | nz-green-soft | `#B7FFE0` | `#B7FFE0` | Tints (sehr sparsam) |
| **Papier** | nz-paper | `#FFFEE5` | `#FFFEE5` | Globaler Hintergrund |
| **Papier** | nz-paper-alt | `#FAF8D4` | `#FAF8D4` | Karten-Tönung |
| **Papier** | nz-paper-deep | `#F4F1C4` | `#F4F1C4` | Sektions-Hintergründe |
| **Kontur** | nz-ink | `#000000` | `#000000` | Text, Linien, Rahmen |
| **Kontur** | nz-ink/70 | `rgba(0,0,0,0.72)` | — | Sekundärtext |
| **Kontur** | nz-ink/50 | `rgba(0,0,0,0.50)` | — | Gedämpfter Text |
| **Kontur** | nz-ink/20 | `rgba(0,0,0,0.18)` | — | Haarlinien, Borders |

**Farbverteilung:**
- 60% **Papier-Gelb** — globaler Untergrund
- 35% **Tinte-Schwarz** — Typografie & Linien
- 5% **Signal-Grün** — echte Handlungsaufforderungen

**Was wir nie tun:**
- ❌ Verläufe
- ❌ Farbton-Spielereien
- ❌ Akzent-Paletten mit 5 Blautönen
- ❌ Weichzeichner oder Glas-Effekte

---

## 🔤 Typografie

Drei Schriften. Klare Rollen.

### Display: Zilla Slab Bold

```
Wir bauen wartbare Plattformen.
```

- **Font**: Zilla Slab Bold (700)
- **Größen**: 56 px, 72 px, 88 px, 128 px
- **Line-height**: 0.95
- **Letter-spacing**: -0.02em
- **Einsatz**: H1, Headlines, Kampagnen-Sätze

### Body: Inter Regular/SemiBold

```
Eine Boutique-Agentur für Digitalberatung, Plattformentwicklung 
und User Experience. Wir schreiben Sätze, die etwas behaupten, 
und belegen sie mit Software, die funktioniert.
```

- **Font**: Inter Regular (400) / SemiBold (600)
- **Body**: 17 px, line-height 1.55
- **Lead**: 22 px, line-height 1.4
- **Small**: 14 px
- **Einsatz**: Fließtext, Unterzeilen

### Mono: Space Mono Regular/Bold

```
// nozilla.config.ts
export const brand = {
  name: 'nozilla',
  motto: 'Gute digitale Dienste',
};
```

- **Font**: Space Mono (400 / 700)
- **Größe**: 11–14 px
- **Letter-spacing**: 0.12em (bei Labels)
- **Einsatz**: Labels, Code, Mono-Kommentare
- **Style**: ALL-CAPS für Labels

### Hierarchie

| Element | Font | Größe | Line-height | Einsatz |
|---------|------|-------|-------------|---------|
| **H1** | Zilla Slab Bold | 56 px | — | Main Headlines |
| **H2** | Zilla Slab Bold | 40 px | — | Section Headlines |
| **H3** | Zilla Slab Bold | 28 px | — | Subsections |
| **H4** | Zilla Slab Bold | 22 px | — | Small headlines |
| **Body** | Inter Regular | 17 px | 1.55 | Fließtext |
| **Small** | Inter Regular | 14 px | 1.55 | Captions, Hints |
| **Label** | Space Mono Bold | 11–12 px | 1.0 | Tags, ALL-CAPS |

---

## 🟫 Form Language

### Eckenradius: Immer 0

- Alle Buttons, Karten, Badges, Inputs, Avatare — **scharfe Kanten**
- Abgerundete Ecken brechen unseren neo-brutalistischen Vertrag
- **Keine Ausnahmen.**

```css
border-radius: 0;
```

### Schatten: Hart, kein Blur

Nur **harter Offset**, nie Weichzeichner.

| Größe | Offset | CSS |
|-------|--------|-----|
| **sm** | 3 px | `box-shadow: 3px 3px 0 0 #000;` |
| **md** (Standard) | 6 px | `box-shadow: 6px 6px 0 0 #000;` |
| **lg** | 10 px | `box-shadow: 10px 10px 0 0 #000;` |

**Keine:**
- `filter: blur()`
- `filter: drop-shadow()`
- `backdrop-filter`
- Glas-Effekte

### Liniendicken: 4 Optionen

| Typ | Größe | Einsatz |
|-----|-------|---------|
| **Hair** | 1.5 px | Feine Unterteilungen |
| **Rule** | 2 px | Standard-Borders, Divider |
| **Strong** | 3 px | Hervorhebung |
| **Heavy** | 4 px | Icons & Illustrationen |

---

## 🎯 Green Marker Element

Unser Signature-Stil: 1–3 Schlüsselwörter pro Absatz auf Signal-Grün.

### ✅ Richtig

```html
<p>Wir bauen <mark class="g">ehrliche</mark> Plattformen.</p>

<p>Unsere Marke trägt zwei <mark class="g">Gesichter</mark>, 
die sich gegenseitig stützen.</p>
```

### ❌ Falsch

```html
<!-- Ganzer Satz grün -->
<p><mark class="g">Wir bauen ehrliche Plattformen für Menschen.</mark></p>

<!-- Mehrere Marker in Folge -->
<p>Wir bauen <mark class="g">ehrliche</mark> und <mark class="g">wartbare</mark> 
<mark class="g">Plattformen</mark>.</p>

<!-- Auf nicht-Text-Flächen -->
<div class="card" style="background: #00FF9C;">Card</div>
```

**Regel:** Semantisch, nie dekorativ. 1–3 pro Absatz. Nur auf Schlüsselwörtern.

---

## 🎨 Ikonografie

Zwei Dialekte, eine Familie.

### Dialekt A: Heavy-Stroke

- **Strichstärke**: 4 px
- **Linien-Ende**: square caps
- **Joins**: miter joins
- **Farbe**: Tinte-Schwarz + optional Signal-Grün-Fill
- **Format**: SVG, 64 × 64 Grundraster
- **Größen**: skalierbar 48–160 px

### Dialekt B: Pixel-Art

- 8-Bit-Reminiszenzen
- Beispiele: Pixel-Gurke, Pixel-Herz
- **Einsatz**: Sparsam, als retro-digitale Interpunktion

**Was wir nicht verwenden:**
- ❌ Emoji
- ❌ Icon-Fonts (wie Font Awesome)
- ❌ Icon-Sets von anderen (Lucide, Heroicons, Tabler)

Alle Icons sind **Custom SVGs** von nozilla.

---

## 💬 Sprache & Ton

### Grundsätze

- **Direkt** — Ohne Umweg, kein Marketing-Nebel
- **Ehrlich** — Was funktioniert, was nicht. Auch in der Präsentation.
- **Deutsch** — Deutsche Sprache, deutsche Substantive groß
- **Technisch** — Mono-Kommentare, Code-Metaphorik, Präzision

### Wortwahl

**Kurze Verben schlagen lange Substantivketten:**
- ✅ bauen, entwickeln, messen, entfernen, ablösen
- ❌ „Implementierung von Synergien", „Enablement von Solutions"

**Buzzwords sind verbrannt:**
- ❌ „seamless", „disruptive", „synergy", „innovative", „cutting-edge"
- ❌ „empowern", „orchestrieren", „next level"

### Format

| Element | Regel |
|---------|-------|
| **Headlines** | Satzanfang, Satzpunkt. Deutsche Substantive groß. |
| **ALL-CAPS** | Nur in Mono-Labels mit `tracking: 0.12em` |
| **Emoji** | Nie. |
| **Symbole** | Nur wenn verdient: `→ ↗ ✓ ✕ · —` |
| **Slogan** | „Gute digitale Dienste." — immer mit Punkt. |

### Beispiele

#### ✅ Richtig

```
Wir bauen ehrliche Plattformen für komplexe Probleme.
```
Kurz. Konkret. Ein Marker. Prüfbar.

```
Altsysteme ablösen, ohne das Tagesgeschäft zu stoppen. 
Inkrementell, mit Messpunkten.
```
Technisch, ehrlich über Einschränkungen.

#### ❌ Falsch

```
Als innovativer Digital-Partner empowern wir Sie dabei, 
disruptive Synergien nahtlos zu orchestrieren.
```
Buzzword-Salat. Nicht prüfbar.

```
Let's take your digital journey to the next level!
```
Englisch, hohl. (Und würde Emoji brauchen, die wir nicht verwenden.)

---

## 📋 Design Tokens (CSS)

```css
:root {
  /* Colors */
  --nz-green: #00FF9C;
  --nz-green-strong: #00E88D;
  --nz-green-soft: #B7FFE0;
  --nz-paper: #FFFEE5;
  --nz-paper-alt: #FAF8D4;
  --nz-paper-deep: #F4F1C4;
  --nz-ink: #000000;
  --nz-ink-70: rgba(0, 0, 0, 0.72);
  --nz-ink-50: rgba(0, 0, 0, 0.50);
  --nz-ink-20: rgba(0, 0, 0, 0.18);

  /* Typography */
  --nz-font-display: "Zilla Slab", serif;
  --nz-font-body: "Inter", sans-serif;
  --nz-font-mono: "Space Mono", monospace;

  /* Layout */
  --nz-radius: 0;
  --nz-container: 1200px;

  /* Strokes */
  --nz-stroke-hair: 1.5px;
  --nz-stroke-rule: 2px;
  --nz-stroke-strong: 3px;
  --nz-stroke-heavy: 4px;

  /* Shadows */
  --nz-shadow-sm: 3px 3px 0 0 var(--nz-ink);
  --nz-shadow-md: 6px 6px 0 0 var(--nz-ink);
  --nz-shadow-lg: 10px 10px 0 0 var(--nz-ink);

  /* Animation */
  --nz-dur: 160ms;
  --nz-ease: cubic-bezier(0.2, 0, 0, 1);
}
```

---

## 🎯 Die 10 Regeln

### Immer ✓

1. **Papier** als Hintergrund, **Tinte** als Linie, **Signal-Grün** nur für echte Aktionen
2. **Ecken bei 0 Radius** — scharf, immer
3. **Schatten als harter Offset** — `6px 6px 0 0 #000`
4. **Zilla Slab** für Display · **Inter** für Body · **Space Mono** für Labels
5. **Max. 3 grüne Marker** pro Absatz, nur auf Schlüsselwörtern

### Niemals ✕

6. **Keine Verläufe**, keine Weichzeichner, kein Glas
7. **Keine Emoji**, keine Icon-Fonts, keine fremden Icon-Sets
8. **Keine runden Ecken** — auch nicht „nur ein bisschen"
9. **Kein Stock-Foto** — wenn Fotografie, dann schwarzweiß mit Korn
10. **Kein Buzzword** — nie „seamless", „disruptive", „synergy"

---

## Logo

### Die Wortmarke

**nozilla** ist unser einziges Logo. Keine Bildmarke, kein Claim im Logo-Lockup.

- **Freiraum**: Höhe des „n" in alle Richtungen
- **Mindestgröße**: Digital 96 px / Print 24 mm Wortmarkenbreite
- **Format**: SVG (digital), EPS (print)
- **Aussprache**: „no-SI-la"

### Zugelassene Untergründe

| Hintergrund | Farbe | Notes |
|---|---|---|
| **Papier-Gelb** | #FFFEE5 | Standard |
| **Signal-Grün** | #00FF9C | Auffällig, selten |
| **Tinte-Schwarz** | #000 | Logo mit `filter: invert(1);` |

### Was wir nie tun

- ❌ Drehen
- ❌ Umfärben (Hue-Rotate)
- ❌ Verzerren (Scale/Skew)
- ❌ Schatten hinzufügen

---

## 🛠️ Praktische Tipps

### Im Web (HTML/CSS)

```html
<!-- Marker-Text -->
<p>Wir bauen <mark class="g">ehrliche</mark> Software.</p>

<!-- Button -->
<button class="btn" style="
  background: var(--nz-green);
  border-radius: 0;
  box-shadow: 6px 6px 0 0 #000;
  font-family: var(--nz-font-body);
  color: #000;
">
  Lass uns bauen
</button>

<!-- Card -->
<div style="
  background: var(--nz-paper);
  border: 2px solid var(--nz-ink);
  border-radius: 0;
  box-shadow: 6px 6px 0 0 var(--nz-ink);
">
  Content
</div>
```

### Im Print (Figma/InDesign)

- Papier-Farbe: `#FFFEE5` (CMYK: 0/0/8/0)
- Schwarz: `#000000` (100% K)
- Signal-Grün: `#00FF9C` (CMYK: 75/0/39/0)
- Schriften: Zilla Slab, Inter, Space Mono (lokale Dateien notwendig)
- Eckenradius: **0** überall



