# nozilla CI — Master Prompt für Claude Code

Kopiere diesen Prompt und füge ihn am Anfang eines neuen Projekts ein, um automatisch die nozilla Brand Guidelines zu übernehmen.

---

## 📋 Prompt für neue Projekte

```
Du arbeitest auf dem nozilla-Projekt. Alle Design, Code und Kommunikation folgen den 
nozilla Corporate Identity Guidelines. Diese sind nicht optional.

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

1. IMMER die nozilla Guidelines anwenden
2. Fragen stellen, wenn etwas gegen die Regeln verstößt
3. Farben: #00FF9C (Signal), #FFFEE5 (Papier), #000 (Kontur)
4. Typografie: Zilla Slab > Inter > Space Mono
5. Formen: 0 Radius, harte Schatten (6px 6px 0 0)
6. Text: Deutsch, direkt, keine Buzzwords
7. Green Marker: 1–3 pro Absatz, nur Schlüsselwörter

WENN DU UNSICHER BIST:
→ Konsultiere README.md oder index.html
→ Frage den Nutzer, wie es mit den Guidelines abgestimmt werden soll
```

---

## 🔄 Wie man es benutzt

### Option 1: Am Projekt-Start
Öffne Claude Code und gib diesen Prompt am Anfang ein:

```
Du arbeitest auf dem nozilla-Projekt. [... Rest des Prompts ...]
```

### Option 2: /loop für regelmäßige Projekte
Wenn du öfter neue nozilla-Projekte startest:

```
/loop 1h "Du arbeitest auf dem nozilla-Projekt. [...]"
```

### Option 3: Als Session-Hook konfigurieren
In `.claude/settings.json`:

```json
{
  "hooks": {
    "session-start": "echo 'Du arbeitest auf dem nozilla-Projekt...' && source PROMPT.md"
  }
}
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
Erstelle mir eine Landingpage für nozilla mit einer Hero-Section, 
Feature-Liste und CTA. Verwende die nozilla CI (README.md).
```

✅ Sehr gut:
```
Ich starte ein neues nozilla-Projekt: [Projektname]
Verwende alle Guidelines aus README.md — Farben, Typografie, Voice, die 10 Regeln.
Hier meine Anforderung: [...]
```

---

## 🎯 Was Claude Code dann macht

Mit diesem Prompt wird Claude Code automatisch:

✅ **Design-Entscheidungen**: #00FF9C für CTAs, #FFFEE5 für Hintergründe
✅ **Typografie**: Zilla Slab für Headlines, Inter für Body
✅ **Code-Struktur**: CSS-Variablen mit nz-Präfix, 0 Radius überall
✅ **Kopie-Ton**: Direkt, ehrlich, Deutsch, keine Buzzwords
✅ **Green Marker**: Automatisch auf 1–3 Schlüsselwörter pro Absatz
✅ **Fragen bei Unsicherheit**: Statt zu raten

---

## 📞 Fragen zum Prompt?

- Siehe `README.md` für detaillierte Erklärungen
- Siehe `index.html` für visuelle Beispiele
- Email: ci@nozilla.de

---

**nozilla CI — v1.0 · April 2026**

_Gute digitale Dienste._
