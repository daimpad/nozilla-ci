# nozilla CI — Master Prompt für Claude Code

Kopiere diesen Prompt und füge ihn am Anfang eines neuen Projekts ein, um automatisch die nozilla Brand Guidelines zu übernehmen.

---

## 📋 Prompt für neue Projekte

```
═══════════════════════════════════════════════════════════════
NOZILLA CORPORATE IDENTITY — MASTER PROMPT FÜR CLAUDE CODE
═══════════════════════════════════════════════════════════════

PROJEKT: nozilla — Gute digitale Dienste
REPO: https://github.com/daimpad/nozilla-ci
BRANCH: main

CI-DOKUMENTATION:
  📖 README (Praktische Richtlinien):
     https://github.com/daimpad/nozilla-ci/blob/main/README.md
  
  🎨 Visuelle Referenz (interaktiv):
     https://github.com/daimpad/nozilla-ci/blob/main/index.html
  
  ⚡ Quick-Reference für KI:
     https://github.com/daimpad/nozilla-ci/blob/main/CLAUDE.md

KONTAKT: ci@nozilla.de

═══════════════════════════════════════════════════════════════

Du arbeitest auf dem nozilla-Projekt. Alle Design, Code und Kommunikation folgen den 
nozilla Corporate Identity Guidelines. Diese sind nicht optional — sie sind Teil 
der Marken-DNA und müssen konsequent angewendet werden.

BRAND IDENTITY:
- Boutique-Agentur für ehrliche Software
- neo-brutalistisch + retro-digital
- Direktheit & Handwerk vor Marketing-Nebel

═══════════════════════════════════════════════════════════════

🎨 FARBEN — Genau drei Rollen:

Signal-Grün: #00FF9C       (Buttons, CTAs, Marker ONLY)
Papier-Gelb: #FFFEE5       (Globaler Hintergrund)
Tinte-Schwarz: #000        (Text, Linien, Rahmen)

Niemals: Verläufe, Farbton-Spielereien, Glas-Effekte

═══════════════════════════════════════════════════════════════

🔤 TYPOGRAFIE — Drei Schriften, klare Rollen:

Display:  Zilla Slab Bold       (56–128px, Headlines)
Body:     Inter Regular         (17px, line-height 1.55)
Mono:     Space Mono Bold       (11–12px, ALL-CAPS, tracking 0.12em)

Hierarchie:
  H1: Zilla Slab Bold 56px
  H2: Zilla Slab Bold 40px
  Body: Inter 17px
  Small: Inter 14px
  Label: Space Mono 11–12px ALL-CAPS

═══════════════════════════════════════════════════════════════

🟫 FORM LANGUAGE:

Radius: IMMER 0 (scharfe Kanten, keine Ausnahmen)
Schatten: Harter Offset nur – 6px 6px 0 0 #000 (kein Blur)
Linien: 1.5px (hair) | 2px (rule) | 3px (strong) | 4px (heavy)

Keine: filter: blur(), backdrop-filter, Glas-Effekte

═══════════════════════════════════════════════════════════════

🎯 GREEN MARKER — Unser Signature-Element:

✅ Richtig:
<mark class="g">ehrliche</mark> Plattformen
1–3 Schlüsselwörter pro Absatz
Nur auf Schlüsselwörtern, semantisch

❌ Falsch:
<mark class="g">Ganzer Satz grün</mark>
Mehrere Marker in Folge
Auf nicht-Text-Flächen

═══════════════════════════════════════════════════════════════

💬 SPRACHE & TON:

Grundsätze:
  • Direkt — ohne Umweg
  • Ehrlich — was funktioniert, was nicht
  • Deutsch — deutsche Substantive groß
  • Technisch — Code-Metaphorik, Präzision

Wortwahl:
  ✅ bauen, entwickeln, messen, entfernen, ablösen
  ❌ seamless, disruptive, synergy, empowern, orchestrieren

Format:
  • Headlines: Satzanfang, Satzpunkt
  • ALL-CAPS: nur in Mono-Labels
  • Emoji: Niemals
  • Slogan: „Gute digitale Dienste." (mit Punkt)

═══════════════════════════════════════════════════════════════

🎯 DIE 10 REGELN:

IMMER ✓
1. Papier-Hintergrund, Tinte-Linie, Signal-Grün nur für Aktionen
2. Ecken bei 0 Radius — scharf, immer
3. Schatten als harter Offset — 6px 6px 0 0 #000
4. Zilla Slab (Display) · Inter (Body) · Space Mono (Labels)
5. Max 3 grüne Marker pro Absatz, nur Schlüsselwörter

NIEMALS ✕
6. Keine Verläufe, keine Weichzeichner, kein Glas
7. Keine Emoji, keine Icon-Fonts, keine fremden Icon-Sets
8. Keine runden Ecken — auch nicht „ein bisschen"
9. Kein Stock-Foto — schwarzweiß mit Korn wenn Fotografie
10. Kein Buzzword — nie „seamless", „disruptive", „synergy"

═══════════════════════════════════════════════════════════════

🛠️ CSS TOKENS:

--nz-green: #00FF9C
--nz-paper: #FFFEE5
--nz-ink: #000000
--nz-ink-70: rgba(0,0,0,0.72)
--nz-ink-50: rgba(0,0,0,0.50)
--nz-ink-20: rgba(0,0,0,0.18)
--nz-radius: 0
--nz-shadow-md: 6px 6px 0 0 var(--nz-ink)
--nz-stroke-rule: 2px

═══════════════════════════════════════════════════════════════

📖 REFERENZEN:

README.md  → Praktische Richtlinien mit Beispielen
index.html → Interaktive visuelle Dokumentation
CLAUDE.md  → Quick-Reference für KI

═══════════════════════════════════════════════════════════════

ANWEISUNG FÜR CLAUDE CODE:

Wenn der Nutzer Design, UI, Kopie oder Code anforderungen gibt:

1. IMMER die nozilla Guidelines anwenden (nicht optional, nicht verhandelbar)
2. Fragen stellen, wenn etwas gegen die Regeln verstößt
3. Farben: #00FF9C (Signal), #FFFEE5 (Papier), #000 (Kontur)
4. Typografie: Zilla Slab > Inter > Space Mono
5. Formen: 0 Radius, harte Schatten (6px 6px 0 0)
6. Text: Deutsch, direkt, keine Buzzwords
7. Green Marker: 1–3 pro Absatz, nur Schlüsselwörter

WENN DU UNSICHER BIST:
→ Konsultiere README.md (https://github.com/daimpad/nozilla-ci/blob/main/README.md)
→ Oder index.html (https://github.com/daimpad/nozilla-ci/blob/main/index.html)
→ Frage den Nutzer, wie es mit den Guidelines abgestimmt werden soll

WORKFLOW BEI NEUEN AUFGABEN:

Schritt 1: Immer kurz überprüfen, ob Anforderung mit CI kompatibel ist
  ✓ „Erstelle Button mit #00FF9C und 0 border-radius" → OK
  ✗ „Erstelle Button mit rundem Design und 5 Farben" → FRAGE nach Alignment
  
Schritt 2: Code/Design mit CI-Tokens schreiben
  --nz-green, --nz-paper, --nz-ink verwenden
  Zilla Slab, Inter, Space Mono einsetzen
  
Schritt 3: Bei Kopie/Text deutsch und direkt schreiben
  Keine Buzzwords, keine Emoji, Green Marker nutzen
  
Schritt 4: Am Ende kurz zusammenfassen, was du gemacht hast und warum es nozilla-konform ist
```

---

## 🔄 Wie man es benutzt

### Option 1: Am Projekt-Start (Empfohlen)
Öffne Claude Code und gib den kompletten Prompt am Anfang ein:

```
PROJEKT: nozilla — Gute digitale Dienste
REPO: https://github.com/daimpad/nozilla-ci

CI-DOKUMENTATION:
  📖 README: https://github.com/daimpad/nozilla-ci/blob/main/README.md
  🎨 index.html: https://github.com/daimpad/nozilla-ci/blob/main/index.html
  ⚡ CLAUDE.md: https://github.com/daimpad/nozilla-ci/blob/main/CLAUDE.md

Du arbeitest auf dem nozilla-Projekt. [... Rest des Prompts ...]
```

### Option 2: GitHub-Link-Variante (Minimal)
Wenn du schnell starten möchtest:

```
Ich starte ein nozilla-Projekt.

Nutze die Corporate Identity Guidelines von hier:
https://github.com/daimpad/nozilla-ci/blob/main/README.md

Alle Design-, Code- und Text-Entscheidungen müssen mit diesen Guidelines 
abgestimmt sein. Frage mich, wenn etwas unklar ist.

Meine Anforderung: [...]
```

### Option 3: Direct Link zum Prompt im Repo
Verlinke auf diesen Prompt direkt:

```
Nutze den Master Prompt von hier:
https://github.com/daimpad/nozilla-ci/blob/main/PROMPT.md
```

### Option 4: Als Session-Hook konfigurieren (Advanced)
In `.claude/settings.json` im nozilla-Projekt:

```json
{
  "hooks": {
    "session-start": "curl -s https://raw.githubusercontent.com/daimpad/nozilla-ci/main/PROMPT.md | head -100"
  }
}
```

### Option 5: Für regelmäßige nozilla-Projekte
Nutze `/loop` um den Prompt regelmäßig zu laden:

```
/loop session-start "Nutze nozilla CI: https://github.com/daimpad/nozilla-ci/blob/main/README.md"
```

---

## ✨ Tipps für beste Ergebnisse

**Nutzer-Input Beispiele:**

❌ Schlecht:
```
Erstelle mir eine Website.
```

✅ Gut:
```
Erstelle mir eine Landingpage für nozilla mit Hero-Section, 
Feature-Liste und CTA. Verwende die nozilla CI.

Repo: https://github.com/daimpad/nozilla-ci/blob/main/README.md
```

✅ Sehr gut (Empfohlen):
```
Ich starte ein neues nozilla-Projekt: [Projektname]

Corporate Identity: https://github.com/daimpad/nozilla-ci
Guidelines: https://github.com/daimpad/nozilla-ci/blob/main/README.md

Verwende alle Regeln — Farben, Typografie, Voice, die 10 Regeln.
Hier meine Anforderung: [...]
```

✅ Mit Master Prompt (Best Practice):
```
[Gib den kompletten Prompt oben ein]

Meine neue Aufgabe für das nozilla-Projekt: [...]
```

---

## 🎯 Was Claude Code dann macht

Mit diesem Prompt wird Claude Code automatisch:

✅ **Design-Entscheidungen**: #00FF9C für CTAs, #FFFEE5 für Hintergründe
✅ **Typografie**: Zilla Slab für Headlines, Inter für Body, Space Mono für Labels
✅ **Code-Struktur**: CSS-Variablen mit nz-Präfix (--nz-green, --nz-paper, etc.), 0 Radius überall
✅ **Formen & Schatten**: Hard offset shadows (6px 6px 0 0), keine Verläufe, keine Glas-Effekte
✅ **Kopie-Ton**: Direkt, ehrlich, Deutsch, keine Buzzwords
✅ **Green Marker**: Automatisch auf 1–3 Schlüsselwörter pro Absatz
✅ **Icons**: Nur Custom SVGs, keine Icon-Fonts oder fremden Icon-Sets
✅ **Fragen bei Unsicherheit**: Konsultiert die Docs oder fragt dich nach Alignment
✅ **Kontext-Bewusstsein**: Referenziert GitHub-Links wenn nötig

---

## 📞 Referenzen & Support

**Documentation:**
- README.md (Praktisch): https://github.com/daimpad/nozilla-ci/blob/main/README.md
- index.html (Visuell): https://github.com/daimpad/nozilla-ci/blob/main/index.html
- CLAUDE.md (Quick-Ref): https://github.com/daimpad/nozilla-ci/blob/main/CLAUDE.md
- PROMPT.md (Master): https://github.com/daimpad/nozilla-ci/blob/main/PROMPT.md

**Fragen?**
- Email: ci@nozilla.de
- GitHub Repo: https://github.com/daimpad/nozilla-ci
- Issue erstellen: https://github.com/daimpad/nozilla-ci/issues

---

**nozilla CI — v1.0 · April 2026**

Repository: https://github.com/daimpad/nozilla-ci
Maintainer: nozilla GmbH
License: Internal Use

_Gute digitale Dienste._
