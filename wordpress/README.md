# nozilla — WordPress

Custom CSS für **Divi**, **Gravity Forms** und **Thrive Quiz Builder** in der nozilla Formsprache.

| Datei | Zweck |
|-------|-------|
| [`nozilla-wordpress.css`](./nozilla-wordpress.css) | Das komplette Stylesheet — Tokens, Typo, Divi, Gravity Forms, Thrive Quiz |

---

## Einbinden

**Weg 1 — Child-Theme (empfohlen).** Datei nach `wp-content/themes/divi-child/nozilla-wordpress.css` legen und in der `functions.php` einreihen:

```php
add_action( 'wp_enqueue_scripts', function () {
    wp_enqueue_style(
        'nozilla-wordpress',
        get_stylesheet_directory_uri() . '/nozilla-wordpress.css',
        [ 'divi-style' ],
        '1.0'
    );
}, 20 );
```

**Weg 2 — Divi.** Inhalt der Datei nach *Divi → Theme-Optionen → Allgemein → Custom CSS* kopieren.

### Schriften

Zilla Slab · Inter · Space Mono, alle SIL OFL 1.1. Die Dateien liegen im Repo unter `project/fonts`.

**Selbst hosten, kein Google-Fonts-CDN** — das ist Markenvorgabe und in Deutschland auch die sichere Variante. Die Schriften auf den Server legen, z. B. nach `wp-content/uploads/nozilla/fonts`, und die `@font-face`-Regeln ins Child-Theme schreiben. Das Stylesheet selbst enthält bewusst keine Pfade, damit es sich unverändert in jedes Projekt kopieren lässt.

Vorlage: [`project/fonts.css`](../project/fonts.css) — nur die `url()`-Pfade anpassen.

Ohne die Schriften greifen die Fallbacks (Georgia · system-ui · ui-monospace). Das Layout hält, die Marke nicht.

---

## Was sich ändert

### Farbe

Vorher standen acht Akzentfarben nebeneinander. Jetzt gelten drei Rollen.

| Vorher | Nachher | Rolle |
|--------|---------|-------|
| `#52f8ac` · `#1ec448` · `#3edf04` (drei Grüntöne) | `#00FF9C` Signal-Grün | Handlung |
| `#ee0000` · `#e00` (roter Absenden-Button) | `#00FF9C` auf Tinte-Schwarz | Handlung |
| `#2f00db` (blauer Weiter-Button) | `#00FF9C` auf Tinte-Schwarz | Handlung |
| `#3b8be5` (PDF-Download) | `#00FF9C` auf Tinte-Schwarz | Handlung |
| `#666666` (Rahmen, Labels, Hover) | `#000000` Tinte-Schwarz | Text, Linien |
| `#d1f3e5` · `#fff9f9` · `#ffc` (Flächentöne) | Papier-Töne + farbige Kante links | Rückmeldung |

Signal-Grün liegt jetzt nur noch auf echten Handlungsflächen: Buttons, gewählte Antworten, aktiver Schritt, Fortschrittsbalken. Der grüne Grund auf **jedem geschlossenen Divi-Toggle** ist weg — flächig auf jeder Zeile wird die Handlungsfarbe zur Dekoration. Stattdessen: Papier-Ton geschlossen, Weiss offen, Plus/Minus-Zeichen in Grün.

### Form

- **Radius 0 überall.** Die elf `border-radius: 8/10/20px` sind raus. Ein Radius-Guard erzwingt das auch gegen künftige Plugin-Updates. Einzige Ausnahme: `input[type="radio"]` — Radios lesen sich per Konvention als Kreis.
- **Harte Offset-Schatten** statt Weichzeichner. Der geknickte Papier-Schatten der Bestätigungsseiten (`box-shadow: 0 15px 10px rgba(0,0,0,.2)` plus `transform: rotate(-3deg)`) ist ersatzlos gestrichen.
- **Keine Verläufe.** `gf_confirmation_yellow_gradient` und `gf_confirmation_green_gradient` behalten ihre Klassennamen — bestehende Formulare brechen nicht — bekommen aber eine Fläche, einen Rahmen und einen harten Schatten.
- **Keine Text-Schatten.** Die sechs `text-shadow`-Regeln der Hinweisblöcke sind raus.
- **Buttons drücken sich.** Ruhe: 4 px Schatten. Hover: hebt 2 px nach oben/links, Schatten wächst auf 6 px. Klick: fällt auf null. Nur `transform` und `box-shadow`, hinter `prefers-reduced-motion`.

### Typografie

Fehlte im Bestand komplett — es gab nur Größen, keine Schriften. Ergänzt:

| Rolle | Schrift | Einsatz |
|-------|---------|---------|
| Display | Zilla Slab Bold, `-0.02em` | h1–h6, Divi-Modul-Header, Toggle-Titel, Formular- und Sektionstitel, Quiz-Frage, Bestätigungen |
| Body | Inter Regular 17 px / 1.55 | Fließtext, Eingabefelder, Choices, Antworten |
| Labels | Space Mono Bold 11 px, VERSAL, `0.12em` | Feld-Labels, Schritt-Labels, Buttons, Tabellenköpfe, Fortschritts-Prozente |

Dazu: grüner Marker (`mark`), Links mit 2 px Unterstrich und grünem Hover, Zitate mit grüner Kante, `::selection` in Signal-Grün.

### Nebenbei behoben

Vier Fehler aus dem Bestand, alle bei der Übersetzung mitgenommen:

1. `input[type="checkbox"]:hover` als Hover-Regel für buttonized Choices zielte auf den per `left: -9999px` ausgeblendeten Input — der Hover konnte nie greifen. Jetzt am Label.
2. `.gform_previous_button.button, .gform_save_link.button:hover` — das `:hover` galt nur für den letzten Selektor der Liste. Beide Zustände sind jetzt sauber getrennt.
3. `input:hover { cursor: pointer }` galt global, also auch für Textfelder. Cursor jetzt nur auf Bedienelementen, Textfelder behalten den Text-Cursor.
4. `.gfield_description` war dreimal mit widersprüchlichen Werten definiert (`#fff`, `#fff9f9`, zwei Paddings), `.gf_page_steps` und vier weitere Regeln doppelt. Zusammengeführt.

Sichtbarer Fokus (`:focus-visible`, 3 px Signal-Grün) ist neu — im Bestand gab es keinen.

### Unverändert übernommen

Layout-Eingriffe aus dem Bestand, die nichts mit Design zu tun haben:

- `.et_non_fixed_nav … #main-header .container { display: none }`
- Der absolut positionierte Footer von `#gform_wrapper_1` (Button neben dem Feld). Neu ist nur ein Rückfall in den Textfluss unter 720 px.
- `margin-bottom: -26px` am filterbaren Portfolio
- `gf_hide_ampm` · `gf_hide_charleft` · `gf_invisible` · `gf_list_inline` · `gf_scroll_text`
- Die Glyph-Korrektur `content: "\e04f"` am offenen Divi-Toggle

---

## Eigene Klassen

Im Divi-Modul unter *Erweitert → CSS-ID & Klassen* vergeben:

| Klasse | Wirkung |
|--------|---------|
| `nz-btn-secondary` | Button in Weiss statt Signal-Grün — für die zweite Handlung im Bild |

---

## Kein Dark Mode

Das Design System kann Dark ([`design-system.css`](../design-system.css)), diese Datei nicht. Divi und Gravity Forms bringen hunderte fest verdrahtete Farbwerte mit, die keine Tokens lesen — ein Theme-Wechsel würde die halbe Seite hell lassen. Lieber ehrlich hell als halb dunkel.

---

Fragen? ci@nozilla.de
