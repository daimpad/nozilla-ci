#!/usr/bin/env python3
"""Baut das CI-Portal unter /ci aus den echten Repo-Artefakten.

Icons, Bilder und Downloads werden aus dem Dateisystem bzw. aus icons.py
gelesen — die Galerie kann damit nicht veralten. Aufruf:

    python3 scripts/build-ci-site.py
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "templates", "google-slides", "build"))
import icons as ICONS  # noqa: E402

OUT = os.path.join(ROOT, "ci")
ASSETS = os.path.join(ROOT, "project", "assets")
MAIL = "contact@nozilla.de"

NAV = [
    ("Marke", [
        ("index.html", "Übersicht", ""),
        ("grundlagen.html", "Grundlagen", ""),
        ("logo.html", "Logo", "3"),
        ("sprache.html", "Sprache", ""),
    ]),
    ("Gestaltung", [
        ("farbe.html", "Farbe", "10"),
        ("typografie.html", "Typografie", "3"),
        ("icons.html", "Icons", str(len(ICONS.ALL))),
        ("bilder.html", "Bilder", ""),
        ("komponenten.html", "Komponenten", ""),
    ]),
    ("Anwendung", [
        ("vorlagen.html", "Vorlagen", ""),
        ("downloads.html", "Downloads", ""),
    ]),
]

COLORS = [
    ("Signal-Grün", "--nz-green", "#00FF9C", "Buttons, CTAs, Marker — nur für Aktion", "signal"),
    ("Signal Hover", "--nz-green-strong", "#00E88D", "Hover- und Active-Zustände", "signal"),
    ("Signal Tint", "--nz-green-soft", "#B7FFE0", "Flächige Tönung, sehr sparsam", "signal"),
    ("Papier-Gelb", "--nz-paper", "#FFFEE5", "Globaler Hintergrund (Print, CI-Dokument)", "papier"),
    ("Papier Alt", "--nz-paper-alt", "#FAF8D4", "Karten-Tönung", "papier"),
    ("Papier Deep", "--nz-paper-deep", "#F4F1C4", "Sektions-Hintergründe", "papier"),
    ("Tinte-Schwarz", "--nz-ink", "#000000", "Schrift, Linien, Rahmen, harte Schatten", "kontur"),
    ("Ink 900", "--nz-c-ink-900", "#0C0C0A", "Warmes Near-Black — Canvas im Dark Theme", "kontur"),
    ("Ink 800", "--nz-c-ink-800", "#17160F", "Flächen im Dark Theme", "kontur"),
    ("Warnung", "--nz-c-warn", "#FF5F1F", "Nur für Fehler- und Verbotsmarkierung", "status"),
]

TYPE_SCALE = [
    ("Display", "Zilla Slab", "700", "56 – 128 px", "0.92", "Headlines, Kampagnen-Sätze"),
    ("H1", "Zilla Slab", "700", "56 px", "1.02", "Seitentitel"),
    ("H2", "Zilla Slab", "700", "40 px", "1.02", "Abschnitte"),
    ("H3", "Zilla Slab", "700", "28 px", "1.05", "Unterabschnitte"),
    ("Lead", "Zilla Slab", "500", "22 px", "1.25", "Einleitungen"),
    ("Body", "Inter", "400", "17 px", "1.55", "Fließtext"),
    ("Small", "Inter", "400", "14 px", "1.55", "Hinweise, Bildunterschriften"),
    ("Label", "Space Mono", "700", "11 – 12 px", "1.0", "ALL-CAPS, tracking 0.12em"),
]


def esc(s):
    return html.escape(str(s), quote=True)


def layout(slug, title, kicker, lede, body, index_js):
    nav = []
    for group, items in NAV:
        nav.append(f'<div class="nav__group">{group}</div>')
        for href, label, count in items:
            cur = ' aria-current="page"' if href == slug else ""
            c = f'<span class="nav__count">{count}</span>' if count else ""
            nav.append(f'<a class="nav__link" href="{href}"{cur}>{label}{c}</a>')
    navhtml = "\n        ".join(nav)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)} — nozilla CI</title>
<meta name="description" content="{esc(lede)}"/>
<meta name="color-scheme" content="light dark"/>
<link rel="icon" href="../project/assets/favicon.svg" type="image/svg+xml"/>
<link rel="alternate icon" href="../project/assets/favicon-32.png" type="image/png"/>
<meta property="og:title" content="{esc(title)} — nozilla CI"/>
<meta property="og:description" content="{esc(lede)}"/>
<meta property="og:image" content="../project/assets/og-image.png"/>
<link rel="stylesheet" href="../project/fonts.css"/>
<link rel="stylesheet" href="../design-system.css"/>
<link rel="stylesheet" href="ci-site.css"/>
<script>(function(){{try{{var t=localStorage.getItem('nz-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
</head>
<body>
<div class="shell">
  <aside class="side">
    <a class="side__brand" href="index.html">nozilla<span>.</span></a>
    <div class="side__tag">Corporate Identity</div>
    <button class="nz-btn nz-btn--sm nz-btn--secondary side__toggle" id="navToggle" aria-expanded="false">Navigation</button>
    <nav class="side__nav" id="sideNav" aria-label="CI-Bereiche">
        {navhtml}
    </nav>
  </aside>

  <div class="main">
    <header class="topbar">
      <div class="search">
        <input id="q" type="search" placeholder="Alles durchsuchen — Icons, Farben, Regeln …"
               autocomplete="off" aria-label="CI durchsuchen" aria-controls="results"/>
        <div class="results" id="results" hidden role="listbox"></div>
      </div>
      <label class="nz-switch" title="Theme umschalten">
        <input type="checkbox" id="themeSwitch" role="switch" aria-label="Dark Theme"/>
        <span class="nz-switch__track"><span class="nz-switch__thumb"></span></span>
      </label>
    </header>

    <div class="wrap">
      <div class="page-head">
        <div class="nz-label">{esc(kicker)}</div>
        <h1>{title}</h1>
        <p>{lede}</p>
      </div>
      {body}
      <footer class="foot">
        <span class="nz-label">nozilla CI · v1.1</span>
        <span class="nz-label">// Gute digitale Dienste.</span>
        <a class="nz-label" href="mailto:{MAIL}">{MAIL}</a>
      </footer>
    </div>
  </div>
</div>
<script>window.NZ_INDEX = {index_js};</script>
<script src="ci-site.js"></script>
</body>
</html>
"""


# ── Suchindex ─────────────────────────────────────────────────────────────
def build_index():
    idx = []
    for _, items in NAV:
        for href, label, _ in items:
            idx.append({"t": label, "c": "Seite", "u": href, "k": label.lower()})
    for slug, label, _ in ICONS.ALL:
        dial = "Pixel-Art" if slug.startswith("pixel") or slug == "cucumber" else "Heavy-Stroke"
        idx.append({"t": label, "c": "Icon", "u": f"icons.html#icon-{slug}",
                    "k": f"{label} {slug} icon {dial}".lower()})
    for name, token, hexv, note, group in COLORS:
        idx.append({"t": f"{name} · {hexv}", "c": "Farbe", "u": f"farbe.html#{token.strip('-')}",
                    "k": f"{name} {token} {hexv} {note} {group}".lower()})
    for name, fam, *_ in TYPE_SCALE:
        idx.append({"t": f"{name} · {fam}", "c": "Typo", "u": "typografie.html",
                    "k": f"{name} {fam} schrift typografie".lower()})
    for t, u, k in [
        ("Wortmarke — Standard", "logo.html", "logo wortmarke svg punkt grün"),
        ("Wortmarke — einfarbig", "logo.html", "logo mono einfarbig grün untergrund"),
        ("Wortmarke — invers", "logo.html", "logo invers dunkel papier"),
        ("Briefpapier", "vorlagen.html#print", "briefpapier letterhead a4 print"),
        ("Visitenkarte", "vorlagen.html#print", "visitenkarte business card 85x55"),
        ("Präsentations-Master", "vorlagen.html#slides", "slides deck master präsentation"),
        ("Icon-Bibliothek (Slides)", "vorlagen.html#slides", "slides icons bibliothek"),
        ("Pitch-Deck", "vorlagen.html#slides", "slides pitch deck"),
        ("Google Docs Vorlagen", "vorlagen.html#docs", "docs vorlagen brief angebot rechnung vertrag"),
        ("Favicon", "bilder.html", "favicon icon browser tab"),
        ("Social Preview", "bilder.html", "og image social preview twitter"),
        ("Die 10 Regeln", "grundlagen.html#regeln", "regeln kanon do dont"),
        ("Green Marker", "grundlagen.html#marker", "marker grün hervorhebung mark"),
        ("Schreibweise nozilla", "grundlagen.html#schreibweise", "nozilla klein punkt schreibweise"),
        ("Buzzword-Verbot", "sprache.html", "buzzword seamless disruptive synergy verboten"),
        ("Web-Elemente", "komponenten.html", "akkordeon modal toast dropdown komponenten"),
        ("Design Tokens", "farbe.html#tokens", "token css variablen nz"),
    ]:
        idx.append({"t": t, "c": "Artefakt", "u": u, "k": k})
    import json
    return json.dumps(idx, ensure_ascii=False, separators=(",", ":"))


IDX = build_index()


def write(slug, title, kicker, lede, body):
    path = os.path.join(OUT, slug)
    with open(path, "w") as f:
        f.write(layout(slug, title, kicker, lede, body, IDX))
    return path


# ── Seiten ────────────────────────────────────────────────────────────────
def p_index():
    tiles = [
        ("grundlagen.html", "Grundlagen", "Haltung, Prinzipien, Schreibweise und die 10 Regeln."),
        ("logo.html", "Logo", "Wortmarke, drei Varianten, Freiraum, Mindestgrößen, Verbote."),
        ("farbe.html", "Farbe", f"{len(COLORS)} Werte in drei Rollen — plus alle Design Tokens."),
        ("typografie.html", "Typografie", "Zilla Slab, Inter, Space Mono — Skala und Einsatz."),
        ("icons.html", "Icons", f"{len(ICONS.ALL)} Icons in zwei Dialekten, kopier- und ladbar."),
        ("bilder.html", "Bilder", "Favicon, Social Preview und alle Marken-Grafiken."),
        ("komponenten.html", "Komponenten", "Design System und Web-Elemente für Oberflächen."),
        ("sprache.html", "Sprache", "Tonalität, Wortwahl, richtig gegen falsch."),
        ("vorlagen.html", "Vorlagen", "Briefpapier, Visitenkarte, Google Docs und Slides."),
        ("downloads.html", "Downloads", "Alle Dateien gebündelt — Web, Print, Fonts."),
    ]
    cards = "\n".join(
        f'<a class="card-link" href="{h}"><div class="nz-label">{i + 1:02d}</div>'
        f'<h3>{t}</h3><p>{d}</p></a>' for i, (h, t, d) in enumerate(tiles))
    stats = [(str(len(ICONS.ALL)), "Icons"), ("3", "Logo-Varianten"), (str(len(COLORS)), "Farbwerte"),
             ("3", "Schriften"), ("21", "Web-Elemente"), ("14", "Dokument-Vorlagen")]
    statrow = "\n".join(
        f'<div class="nz-stat nz-stat--raised"><div class="nz-stat__label">{l}</div>'
        f'<div class="nz-stat__value">{v}</div></div>' for v, l in stats)
    body = f"""
      <div class="nz-alert nz-alert--signal" style="margin-bottom:var(--nz-space-6)">
        <div><div class="nz-alert__title">Alles an einem Ort.</div>
        <div class="nz-alert__body">Oben suchen — die Suche findet Icons, Farbwerte, Regeln und Dateien
        über alle Seiten hinweg. Tastatur: <kbd class="nz-kbd">/</kbd> fokussiert das Feld.</div></div>
      </div>
      <div class="nz-grid nz-grid--3" style="margin-bottom:var(--nz-space-7)">{statrow}</div>
      <section class="sec" style="margin-top:0"><h2>Bereiche.</h2>
        <p class="lede">Zehn Kapitel — von der Haltung bis zur fertigen Datei.</p>
        <div class="cards">{cards}</div>
      </section>"""
    write("index.html", "Corporate<br/>Identity.", "nozilla · Markenportal",
          "Jedes Artefakt der Marke — geordnet, durchsuchbar und direkt verwendbar.", body)


def p_grundlagen():
    principles = [("Direkt", "Wir schreiben und gestalten ohne Umweg. Kein Marketing-Nebel."),
                  ("Ehrlich", "Wir zeigen, was funktioniert — und was nicht. Auch in der Präsentation."),
                  ("Handwerklich", "Linien werden gezogen, nicht gefiltert. Schatten sind hart."),
                  ("Technisch", "Mono-Kommentare, Pixel-Ikonografie und Code-Metaphorik gehören zu uns.")]
    pr = "\n".join(f'<div class="nz-card nz-card--raised"><h3 class="nz-card__title">{t}</h3>'
                   f'<p class="nz-small nz-muted">{d}</p></div>' for t, d in principles)
    do = ["Papier oder Weiß als Grund, Tinte als Linie, Signal-Grün nur für echte Aktionen.",
          "Ecken bei 0 Radius. Scharf. Immer.",
          "Schatten als harter Offset — <code>6px 6px 0 0</code>.",
          "Zilla Slab für Display · Inter für Body · Space Mono für Labels.",
          "Maximal drei grüne Marker pro Absatz, nur auf Schlüsselwörtern."]
    no = ["Keine Verläufe, keine Weichzeichner, kein Glas.",
          "Keine Emoji, keine Icon-Fonts, keine fremden Icon-Sets.",
          "Keine runden Ecken — auch nicht „nur ein bisschen“.",
          "Kein Stock-Foto. Wenn Fotografie, dann schwarzweiß mit Korn.",
          "Kein Buzzword. Nie „seamless“, „disruptive“, „synergy“."]
    rules = "".join(f'<div class="rule rule--do"><h4>{i + 1:02d} · Immer</h4><p>{t}</p></div>'
                    for i, t in enumerate(do))
    rules += "".join(f'<div class="rule rule--no"><h4>{i + 6:02d} · Niemals</h4><p>{t}</p></div>'
                     for i, t in enumerate(no))
    body = f"""
      <section class="sec" style="margin-top:0"><h2>Wer wir sind.</h2>
        <p class="lede">nozilla ist eine Boutique-Agentur für <mark>ehrliche</mark> Software. Wir bauen
        digitale Plattformen, Prototypen und Interfaces für Menschen, die Komplexität ernst nehmen.</p>
        <p class="nz-muted" style="max-width:68ch">Die Marke trägt zwei Gesichter: ein handwerkliches,
        neo-brutalistisches Äußeres — klare Kanten, schwere Typografie, Tinte-Schwarz — und ein
        augenzwinkerndes, retro-digitales Inneres aus Pixel-Gemüse, Mono-Kommentaren und grünem
        Leucht-Marker. Seriös da, wo es zählt; verspielt, wo es gut tut.</p>
      </section>
      <section class="sec"><h2>Prinzipien.</h2><div class="nz-grid nz-grid--4">{pr}</div></section>
      <section class="sec" id="schreibweise"><h2>Schreibweise.</h2>
        <p class="lede">Die Marke heißt <b>nozilla</b> — immer klein, immer mit grünem Punkt.</p>
        <table class="tbl">
          <thead><tr><th>Richtig</th><th>Falsch</th><th>Warum</th></tr></thead>
          <tbody>
            <tr><td><b>nozilla</b><span style="color:#00FF9C">.</span></td><td>Nozilla</td><td>Nie am Satzanfang großschreiben — die Marke bleibt klein.</td></tr>
            <tr><td><b>nozilla</b></td><td>NOZILLA</td><td>Auch in Versal-Labels bleibt der Name klein.</td></tr>
            <tr><td><b>nozilla</b></td><td>nozilla GmbH</td><td>Kein Rechtsformzusatz im Marken­auftritt.</td></tr>
            <tr><td>{MAIL}</td><td>ci@nozilla.de</td><td>Eine Adresse, überall gleich.</td></tr>
          </tbody></table>
      </section>
      <section class="sec" id="marker"><h2>Der grüne Marker.</h2>
        <p class="lede">Unser Signature-Element: 1–3 Schlüsselwörter pro Absatz auf Signal-Grün.</p>
        <div class="rules">
          <div class="rule rule--do"><h4>So</h4><p>Wir bauen <mark>ehrliche</mark> Plattformen für komplexe Probleme.</p></div>
          <div class="rule rule--no"><h4>Nicht so</h4><p><mark>Wir bauen ehrliche Plattformen für komplexe Probleme.</mark></p></div>
        </div>
      </section>
      <section class="sec" id="regeln"><h2>Die 10 Regeln.</h2>
        <p class="lede">Für den schnellen Blick — der Kanon in zehn Sätzen.</p>
        <div class="rules">{rules}</div>
      </section>"""
    write("grundlagen.html", "Grundlagen.", "Marke", "Haltung, Prinzipien, Schreibweise und der Kanon.", body)


def p_logo():
    variants = [
        ("nozilla-logo.svg", "Standard", "Tinte + Signal-grüner Punkt. Erste Wahl auf hellen Gründen.", "paper"),
        ("nozilla-logo-mono.svg", "Einfarbig", "Ohne grünen Punkt — für den Signal-grünen Untergrund.", "green"),
        ("nozilla-logo-invers.svg", "Invers", "Papier + grüner Punkt. Für dunkle Gründe.", "ink"),
    ]
    cards = "\n".join(
        f'<div class="asset"><div class="asset__art asset__art--{bg}">'
        f'<img src="../project/assets/{f}" alt="{n}"/></div>'
        f'<div class="asset__meta"><div class="asset__name">{n}</div>'
        f'<div class="asset__note">{d}</div>'
        f'<div class="asset__links"><a href="../project/assets/{f}" download>SVG laden</a>'
        f'<button class="copy" data-copy="project/assets/{f}">Pfad kopieren</button></div></div></div>'
        for f, n, d, bg in variants)
    body = f"""
      <section class="sec" style="margin-top:0"><h2>Varianten.</h2>
        <p class="lede">Ein Glyph, drei Fassungen. Die Wortmarke ist unser einziges Logo —
        ohne Bildmarke, ohne Claim im Lockup.</p>
        <div class="assets">{cards}</div>
      </section>
      <section class="sec"><h2>Regeln.</h2>
        <table class="tbl">
          <tbody>
            <tr><td><b>Freiraum</b></td><td>Höhe des „n“ in alle Richtungen.</td></tr>
            <tr><td><b>Mindestgröße</b></td><td>Digital 96 px, Print 24 mm Wortmarkenbreite.</td></tr>
            <tr><td><b>Punkt</b></td><td>Immer Signal-Grün — außer auf Signal-Grün, dort einfarbig.</td></tr>
            <tr><td><b>Schreibweise</b></td><td>Immer klein. Nie „Nozilla“, nie Versalien.</td></tr>
            <tr><td><b>Dateiformat</b></td><td>SVG digital · EPS und PDF für Print (echte Konturen).</td></tr>
            <tr><td><b>Aussprache</b></td><td>„no-SI-la“.</td></tr>
          </tbody></table>
      </section>
      <section class="sec"><h2>Was wir nie tun.</h2>
        <div class="rules">
          <div class="rule rule--no"><h4>Nicht drehen</h4><p>Die Marke steht waagerecht. Immer.</p></div>
          <div class="rule rule--no"><h4>Nicht umfärben</h4><p>Nur Tinte, Papier und der grüne Punkt.</p></div>
          <div class="rule rule--no"><h4>Nicht verzerren</h4><p>Skalieren nur proportional.</p></div>
          <div class="rule rule--no"><h4>Kein Schatten</h4><p>Keine Weichzeichner, kein Glow, kein Relief.</p></div>
        </div>
      </section>
      <section class="sec"><h2>Print-Dateien.</h2>
        <p class="lede">Beide enthalten echte Zilla-Slab-Konturen — keine Schriftabhängigkeit.</p>
        <div class="nz-row">
          <a class="nz-btn nz-btn--primary" href="../project/assets/nozilla-logo.eps" download>EPS laden</a>
          <a class="nz-btn nz-btn--secondary" href="../project/assets/nozilla-logo.pdf" download>PDF laden</a>
        </div>
      </section>"""
    write("logo.html", "Logo.", "Marke", "Die Wortmarke, ihre Varianten und die Regeln dazu.", body)


def p_farbe():
    rows = "\n".join(
        f'<tr id="{t.strip("-")}" data-k="{esc((n + " " + t + " " + h + " " + note).lower())}">'
        f'<td><span class="chip" style="background:{h}"></span><b>{n}</b></td>'
        f'<td><code>{t}</code></td><td><code>{h}</code></td><td>{note}</td>'
        f'<td><button class="copy" data-copy="{h}">Hex</button> '
        f'<button class="copy" data-copy="var({t})">Token</button></td></tr>'
        for n, t, h, note, _ in COLORS)
    body = f"""
      <section class="sec" style="margin-top:0"><h2>Rollen.</h2>
        <p class="lede">Die Palette kennt drei Rollen — und weigert sich, mehr zu tragen.</p>
        <div class="nz-grid nz-grid--3">
          <div class="nz-card nz-card--raised"><h3 class="nz-card__title">Signal · 5 %</h3>
            <p class="nz-small nz-muted">Die einzige Aktionsfarbe. Buttons, Marker, Hervorhebungen, die zählen.</p></div>
          <div class="nz-card nz-card--raised"><h3 class="nz-card__title">Grund · 60 %</h3>
            <p class="nz-small nz-muted">Papier-Gelb im Print und CI-Dokument, Weiß in Präsentationen.</p></div>
          <div class="nz-card nz-card--raised"><h3 class="nz-card__title">Kontur · 35 %</h3>
            <p class="nz-small nz-muted">Tinte-Schwarz für Schrift, Linien, Rahmen und harte Schatten.</p></div>
        </div>
      </section>
      <section class="sec"><h2>Alle Werte.</h2>
        <div class="filter-bar"><span class="hit-count" id="colorCount"></span></div>
        <table class="tbl" id="colorTable">
          <thead><tr><th>Farbe</th><th>Token</th><th>Hex</th><th>Rolle</th><th>Kopieren</th></tr></thead>
          <tbody>{rows}</tbody></table>
      </section>
      <section class="sec" id="tokens"><h2>Design Tokens.</h2>
        <p class="lede">Komponenten nutzen ausschließlich semantische Tokens — ein Theme-Wechsel
        tauscht die Zuordnung, nicht die Komponenten.</p>
        <table class="tbl">
          <thead><tr><th>Token</th><th>Rolle</th><th>Light</th><th>Dark</th></tr></thead>
          <tbody>
            <tr><td><code>--nz-bg</code></td><td>Canvas</td><td>#FFFEE5</td><td>#0C0C0A</td></tr>
            <tr><td><code>--nz-surface</code></td><td>Karten, Panels</td><td>#FFFFFF</td><td>#17160F</td></tr>
            <tr><td><code>--nz-text</code></td><td>Primärtext</td><td>#000000</td><td>#FFFEE5</td></tr>
            <tr><td><code>--nz-line</code></td><td>Rahmen, Linien</td><td>#000000</td><td>#FFFEE5</td></tr>
            <tr><td><code>--nz-signal</code></td><td>Aktionsfarbe</td><td>#00FF9C</td><td>#00FF9C</td></tr>
            <tr><td><code>--nz-shadow-color</code></td><td>Harte Schatten</td><td>#000000</td><td>#FFFEE5</td></tr>
            <tr><td><code>--nz-radius</code></td><td>Eckenradius</td><td colspan="2">0 — ausnahmslos</td></tr>
          </tbody></table>
      </section>"""
    write("farbe.html", "Farbe.", "Gestaltung", "Drei Rollen, zehn Werte, ein Token-Vokabular.", body)


def p_typografie():
    rows = "\n".join(
        f'<tr><td><b>{n}</b></td><td>{fam}</td><td><code>{w}</code></td><td>{sz}</td>'
        f'<td>{lh}</td><td class="nz-muted">{use}</td></tr>'
        for n, fam, w, sz, lh, use in TYPE_SCALE)
    body = f"""
      <section class="sec" style="margin-top:0"><h2>Drei Schriften.</h2>
        <p class="lede">Klare Rollen, keine Überschneidung.</p>
        <div class="nz-stack">
          <div class="nz-card nz-card--raised">
            <div class="nz-label">Display — Zilla Slab Bold</div>
            <p style="font-family:var(--nz-font-display);font-weight:700;font-size:52px;line-height:1;margin:10px 0 0">
              Wir bauen <mark>wartbare</mark> Plattformen.</p>
          </div>
          <div class="nz-card nz-card--raised">
            <div class="nz-label">Body — Inter Regular</div>
            <p style="font-size:17px;line-height:1.55;margin:10px 0 0;max-width:60ch">
              Eine Boutique-Agentur für Digitalberatung, Plattformentwicklung und User Experience.
              Wir schreiben Sätze, die etwas behaupten, und belegen sie mit Software, die funktioniert.</p>
          </div>
          <div class="nz-card nz-card--raised">
            <div class="nz-label">Mono — Space Mono</div>
            <pre class="nz-codeblock" style="margin-top:10px">// nozilla.config.ts
export const brand = {{
  name: 'nozilla',
  motto: 'Gute digitale Dienste',
}};</pre>
          </div>
        </div>
      </section>
      <section class="sec"><h2>Skala.</h2>
        <table class="tbl">
          <thead><tr><th>Stufe</th><th>Schrift</th><th>Schnitt</th><th>Größe</th><th>Zeilenhöhe</th><th>Einsatz</th></tr></thead>
          <tbody>{rows}</tbody></table>
      </section>
      <section class="sec"><h2>Dateien.</h2>
        <p class="lede">Alle drei Familien liegen selbst gehostet im Repo — SIL Open Font License.</p>
        <div class="nz-row">
          <a class="nz-btn nz-btn--secondary" href="../project/fonts/ZillaSlab-Bold.ttf" download>Zilla Slab Bold</a>
          <a class="nz-btn nz-btn--secondary" href="../project/fonts/Inter-Regular.ttf" download>Inter Regular</a>
          <a class="nz-btn nz-btn--secondary" href="../project/fonts/SpaceMono-Regular.ttf" download>Space Mono</a>
          <a class="nz-btn nz-btn--ghost" href="../project/fonts/OFL.txt">Lizenz</a>
        </div>
      </section>"""
    write("typografie.html", "Typografie.", "Gestaltung", "Zilla Slab, Inter und Space Mono — mit klarer Hierarchie.", body)


def p_icons():
    cells = []
    for slug, label, _ in ICONS.ALL:
        dial = "pixel" if slug.startswith("pixel") or slug == "cucumber" else "heavy"
        svg = ICONS.to_svg(slug)
        cells.append(
            f'<figure class="icon-cell" id="icon-{slug}" data-dial="{dial}" '
            f'data-k="{esc((label + " " + slug).lower())}">'
            f'<div class="icon-cell__art" role="img" aria-label="{label}">{svg}</div>'
            f'<figcaption class="icon-cell__name">{label}</figcaption>'
            f'<div class="icon-cell__bar">'
            f'<button class="copy-svg" data-svg="{esc(svg)}" title="SVG-Quelltext kopieren">SVG</button>'
            f'<a href="../project/assets/icon-{slug}.svg" download>Laden</a>'
            f'</div></figure>')
    grid = "\n".join(cells)
    heavy, pixel = len(ICONS.HEAVY), len(ICONS.PIXEL)
    body = f"""
      <section class="sec" style="margin-top:0">
        <div class="filter-bar">
          <div class="nz-segmented" role="radiogroup" aria-label="Dialekt">
            <label><input type="radio" name="dial" value="all" checked/><span>Alle</span></label>
            <label><input type="radio" name="dial" value="heavy"/><span>Heavy-Stroke</span></label>
            <label><input type="radio" name="dial" value="pixel"/><span>Pixel-Art</span></label>
          </div>
          <input class="nz-input" id="iconFilter" type="search" placeholder="Icon filtern …"
                 style="max-width:240px" aria-label="Icons filtern"/>
          <span class="hit-count" id="iconCount"></span>
        </div>
        <div class="icon-grid" id="iconGrid">{grid}</div>
      </section>
      <section class="sec"><h2>Zwei Dialekte.</h2>
        <div class="nz-grid nz-grid--2">
          <div class="nz-card nz-card--raised"><h3 class="nz-card__title">Heavy-Stroke · {heavy}</h3>
            <p class="nz-small nz-muted">4-px-Umriss auf 64er-Raster, rechtwinklige Enden, Gehrungsecken.
            Tinte-Schwarz, optional mit Signal-grünem Fill. Zielgröße 48–160 px.</p></div>
          <div class="nz-card nz-card--raised"><h3 class="nz-card__title">Pixel-Art · {pixel}</h3>
            <p class="nz-small nz-muted">8-Bit-Reminiszenzen als retro-digitale Interpunktion.
            Sparsam einsetzen — ein Augenzwinkern pro Seite genügt.</p></div>
        </div>
      </section>
      <section class="sec"><h2>Verwendung.</h2>
        <table class="tbl"><tbody>
          <tr><td><b>Web</b></td><td><code>&lt;img src="project/assets/icon-grid.svg" alt="Grid"/&gt;</code></td></tr>
          <tr><td><b>Slides</b></td><td>Icon-Bibliothek öffnen, Form anklicken, kopieren — native Vektoren, direkt umfärbbar.</td></tr>
          <tr><td><b>Farbe</b></td><td>Tinte auf hell, Papier auf dunkel. Grün nur als Akzentfüllung.</td></tr>
          <tr><td><b>Verboten</b></td><td>Keine Emoji, keine Icon-Fonts, keine fremden Sets.</td></tr>
        </tbody></table>
      </section>"""
    write("icons.html", "Icons.", "Gestaltung",
          f"{len(ICONS.ALL)} Icons in zwei Dialekten — filtern, Quelltext kopieren, laden.", body)


def p_bilder():
    imgs = [
        ("og-image.png", "Social Preview", "1200 × 630 — Open Graph und Twitter Card.", ""),
        ("favicon.svg", "Favicon", "Browser-Tab, skalierbar.", "paper"),
        ("favicon-180.png", "Apple Touch Icon", "180 × 180 für iOS-Homescreen.", "paper"),
        ("favicon-32.png", "Favicon PNG", "32 × 32 Fallback.", "paper"),
        ("nozilla-logo.svg", "Wortmarke", "Standard mit grünem Punkt.", "paper"),
        ("nozilla-logo-invers.svg", "Wortmarke invers", "Für dunkle Gründe.", "ink"),
    ]
    cards = "\n".join(
        f'<div class="asset"><div class="asset__art{" asset__art--" + bg if bg else ""}">'
        f'<img src="../project/assets/{f}" alt="{n}" loading="lazy"/></div>'
        f'<div class="asset__meta"><div class="asset__name">{n}</div>'
        f'<div class="asset__note">{d}</div>'
        f'<div class="asset__links"><a href="../project/assets/{f}" download>Laden</a>'
        f'<a href="../project/assets/{f}" target="_blank" rel="noopener">Öffnen</a></div></div></div>'
        for f, n, d, bg in imgs)
    body = f"""
      <section class="sec" style="margin-top:0"><h2>Marken-Grafiken.</h2>
        <p class="lede">Alle Bilddateien der Marke — jeweils in der Fassung, die im Einsatz ist.</p>
        <div class="assets">{cards}</div>
      </section>
      <section class="sec"><h2>Fotografie.</h2>
        <div class="rules">
          <div class="rule rule--do"><h4>Wenn Fotografie</h4>
            <p>Schwarzweiß mit sichtbarem Korn. Echte Situationen, echte Menschen, kein Posieren.</p></div>
          <div class="rule rule--no"><h4>Niemals</h4>
            <p>Kein Stock-Foto, keine Farbfilter, keine Verläufe oder Weichzeichner darüber.</p></div>
        </div>
      </section>"""
    write("bilder.html", "Bilder.", "Gestaltung", "Favicon, Social Preview und alle Marken-Grafiken.", body)


def p_komponenten():
    body = """
      <section class="sec" style="margin-top:0"><h2>Zwei Bibliotheken.</h2>
        <div class="cards">
          <a class="card-link" href="../design-system.html"><div class="nz-label">Design System</div>
            <h3>Foundations &amp; Kern.</h3><p>Buttons, Cards, Formulare, Alerts, Tabellen — mit Light- und Dark-Theme.</p></a>
          <a class="card-link" href="../components.html"><div class="nz-label">Web-Elemente</div>
            <h3>21 Bausteine.</h3><p>Akkordeon, Modal, Toast, Dropdown, Stepper, Timeline und mehr.</p></a>
          <a class="card-link" href="../index.html"><div class="nz-label">CI-Dokument</div>
            <h3>Das Original.</h3><p>Die vollständige Fassung als durchgehendes Dokument.</p></a>
        </div>
      </section>
      <section class="sec"><h2>Einbinden.</h2>
        <pre class="nz-codeblock">&lt;link rel="stylesheet" href="project/fonts.css"/&gt;
&lt;link rel="stylesheet" href="design-system.css"/&gt;
&lt;script src="design-system.js" defer&gt;&lt;/script&gt;</pre>
        <p class="nz-muted" style="margin-top:var(--nz-space-3);max-width:68ch">Die meisten Elemente
        laufen ohne JavaScript — Akkordeon, Dropdown und Popover nutzen natives
        <code>&lt;details&gt;</code>, das Modal ein natives <code>&lt;dialog&gt;</code>.</p>
      </section>
      <section class="sec"><h2>Formensprache.</h2>
        <table class="tbl"><tbody>
          <tr><td><b>Radius</b></td><td><code>0</code> — ausnahmslos.</td></tr>
          <tr><td><b>Schatten</b></td><td>Harter Offset: <code>3px</code> · <code>6px</code> (Standard) · <code>10px</code>. Nie Blur.</td></tr>
          <tr><td><b>Linien</b></td><td>1.5 px Haar · 2 px Regel · 3 px stark · 4 px schwer (Icons).</td></tr>
          <tr><td><b>Bewegung</b></td><td>160 ms, <code>cubic-bezier(.2,0,0,1)</code> — hinter <code>prefers-reduced-motion</code>.</td></tr>
        </tbody></table>
      </section>"""
    write("komponenten.html", "Komponenten.", "Gestaltung", "Design System und Web-Elemente für Oberflächen.", body)


def p_sprache():
    good = [("Wir bauen <mark>ehrliche</mark> Plattformen für komplexe Probleme.", "Kurz. Konkret. Ein Marker auf dem tragenden Wort."),
            ("Altsysteme ablösen, ohne das Tagesgeschäft zu stoppen. Inkrementell, mit Messpunkten.", "Technisch, prüfbar, ehrlich über die Einschränkung.")]
    bad = [("Als innovativer Digital-Partner empowern wir Sie dabei, disruptive Synergien nahtlos zu orchestrieren.", "Buzzword-Salat. Keine Behauptung, die man prüfen könnte."),
           ("Let’s take your digital journey to the next level!", "Englisch, hohl — und ohne jede Aussage.")]
    g = "".join(f'<div class="rule rule--do"><h4>So</h4><p style="font-family:var(--nz-font-display);font-size:19px;line-height:1.3;color:var(--nz-text)">{t}</p><p style="margin-top:6px">{w}</p></div>' for t, w in good)
    b = "".join(f'<div class="rule rule--no"><h4>Nicht so</h4><p style="font-family:var(--nz-font-display);font-size:19px;line-height:1.3;text-decoration:line-through;color:var(--nz-text-muted)">{t}</p><p style="margin-top:6px">{w}</p></div>' for t, w in bad)
    body = f"""
      <section class="sec" style="margin-top:0"><h2>Grundsätze.</h2>
        <p class="lede">Wir sprechen deutsch, technisch und ohne Zucker. „Sie“ nach außen, „wir“ als Agentur.</p>
        <table class="tbl"><tbody>
          <tr><td><b>Headlines</b></td><td>Satzanfang, Satzpunkt. Deutsche Substantive groß — <b>nozilla</b> bleibt klein.</td></tr>
          <tr><td><b>Verben</b></td><td>Kurze Verben schlagen lange Substantivketten: bauen, messen, ablösen.</td></tr>
          <tr><td><b>ALL-CAPS</b></td><td>Nur in Mono-Labels mit <code>tracking 0.12em</code>.</td></tr>
          <tr><td><b>Emoji</b></td><td>Nie.</td></tr>
          <tr><td><b>Symbole</b></td><td>Nur wenn sie sich verdienen: → ↗ ✓ ✕ · —</td></tr>
          <tr><td><b>Slogan</b></td><td>„Gute digitale Dienste.“ — immer mit Punkt.</td></tr>
        </tbody></table>
      </section>
      <section class="sec"><h2>Verbrannte Wörter.</h2>
        <p class="lede">Diese Begriffe benutzen wir nicht — sie behaupten etwas, das man nicht prüfen kann.</p>
        <div class="nz-row">
          {"".join(f'<span class="nz-badge">{w}</span>' for w in ["seamless", "disruptive", "synergy", "innovativ", "cutting-edge", "empowern", "orchestrieren", "next level", "ganzheitlich", "State of the Art"])}
        </div>
      </section>
      <section class="sec"><h2>Richtig gegen falsch.</h2><div class="rules">{g}{b}</div></section>"""
    write("sprache.html", "Sprache.", "Marke", "Tonalität, Wortwahl und Beispiele — direkt, ehrlich, deutsch.", body)


def p_vorlagen():
    body = f"""
      <section class="sec" style="margin-top:0" id="print"><h2>Print.</h2>
        <p class="lede">Beide Vorlagen sind druckfertiges HTML — im Browser öffnen und über
        „Drucken → Als PDF sichern“ ausgeben. Die PDF-Fassung liegt daneben.</p>
        <div class="cards">
          <a class="card-link" href="briefpapier.html"><div class="nz-label">DIN A4</div>
            <h3>Briefpapier.</h3><p>Kopf mit Wortmarke, Falzmarken, Fußzeile mit Pflichtangaben.</p></a>
          <a class="card-link" href="visitenkarte.html"><div class="nz-label">85 × 55 mm</div>
            <h3>Visitenkarte.</h3><p>Vorder- und Rückseite, mit 3 mm Beschnitt.</p></a>
        </div>
        <div class="nz-row" style="margin-top:var(--nz-space-4)">
          <a class="nz-btn nz-btn--secondary" href="../project/assets/print/briefpapier.pdf" download>Briefpapier · PDF</a>
          <a class="nz-btn nz-btn--secondary" href="../project/assets/print/visitenkarte.pdf" download>Visitenkarte · PDF</a>
        </div>
      </section>
      <section class="sec" id="slides"><h2>Präsentationen.</h2>
        <p class="lede">In Drive ziehen → Rechtsklick → „Öffnen mit &rsaquo; Google Präsentationen“.</p>
        <div class="cards">
          <a class="card-link" href="../templates/google-slides/nozilla-slides-master.pptx" download>
            <div class="nz-label">19 Folien</div><h3>Master.</h3><p>Titel, Agenda, Kapitel, Inhalte, Kennzahlen, Team, Kontakt.</p></a>
          <a class="card-link" href="../templates/google-slides/nozilla-slides-icons.pptx" download>
            <div class="nz-label">7 Folien</div><h3>Icon-Bibliothek.</h3><p>Alle {len(ICONS.ALL)} Icons als native Vektoren, hell und invertiert.</p></a>
          <a class="card-link" href="../templates/google-slides/nozilla-slides-pitch.pptx" download>
            <div class="nz-label">12 Folien</div><h3>Pitch-Deck.</h3><p>Problem, Lösung, Nutzen, Referenz, Investition.</p></a>
        </div>
      </section>
      <section class="sec" id="docs"><h2>Dokumente.</h2>
        <p class="lede">14 Google-Docs-Vorlagen — Kopie erstellen und Platzhalter füllen.</p>
        <table class="tbl">
          <thead><tr><th>Vorlage</th><th>Wofür</th></tr></thead>
          <tbody>
            <tr><td><b>Anschreiben</b></td><td>Angebots- und Bewerbungsanschreiben</td></tr>
            <tr><td><b>Geschäftsbrief</b></td><td>Formeller Brief mit Pflichtangaben</td></tr>
            <tr><td><b>Konzeptpapier</b></td><td>Ausgangslage → Ziel → Ansatz → Phasen</td></tr>
            <tr><td><b>Angebot</b></td><td>Leistungstabelle mit Summen</td></tr>
            <tr><td><b>Projekt-Briefing</b></td><td>Problem, Zielgruppe, Erfolgskriterien</td></tr>
            <tr><td><b>Meeting-Protokoll</b></td><td>Entscheidungen und Aufgaben</td></tr>
            <tr><td><b>Statusbericht</b></td><td>Ampel, Fortschritt, Blocker</td></tr>
            <tr><td><b>Pressemitteilung</b></td><td>Schlagzeile, Lead, Zitat, Boilerplate</td></tr>
            <tr><td><b>Workshop-Agenda</b></td><td>Ablauf, Vorbereitung, Spielregeln</td></tr>
            <tr><td><b>Rechnung</b></td><td>Positionen, USt., Bankverbindung</td></tr>
            <tr><td><b>Projektsteckbrief</b></td><td>One-Pager: Aufgabe → Lösung → Ergebnis</td></tr>
            <tr><td><b>Onboarding</b></td><td>Willkommen, erste Tage, Zugänge</td></tr>
            <tr><td><b>Vertrag</b></td><td>Dienstleistungsvertrag als Gerüst</td></tr>
            <tr><td><b>Retrospektive</b></td><td>Was lief, was nicht, welche Maßnahmen</td></tr>
          </tbody></table>
      </section>"""
    write("vorlagen.html", "Vorlagen.", "Anwendung", "Briefpapier, Visitenkarte, Präsentationen und Dokumente.", body)


def p_downloads():
    groups = [
        ("Logo", [("nozilla-logo.svg", "Wortmarke · SVG"), ("nozilla-logo-mono.svg", "Einfarbig · SVG"),
                  ("nozilla-logo-invers.svg", "Invers · SVG"), ("nozilla-logo.eps", "Print · EPS"),
                  ("nozilla-logo.pdf", "Print · PDF")], "../project/assets/"),
        ("Bilder", [("og-image.png", "Social Preview"), ("favicon.svg", "Favicon · SVG"),
                    ("favicon-180.png", "Apple Touch"), ("favicon-32.png", "Favicon · PNG")], "../project/assets/"),
        ("Schriften", [("ZillaSlab-Bold.ttf", "Zilla Slab Bold"), ("ZillaSlab-SemiBold.ttf", "Zilla Slab SemiBold"),
                       ("Inter-Regular.ttf", "Inter Regular"), ("Inter-Bold.ttf", "Inter Bold"),
                       ("SpaceMono-Regular.ttf", "Space Mono"), ("SpaceMono-Bold.ttf", "Space Mono Bold"),
                       ("OFL.txt", "Lizenz")], "../project/fonts/"),
        ("Präsentationen", [("nozilla-slides-master.pptx", "Master · 19 Folien"),
                            ("nozilla-slides-icons.pptx", "Icon-Bibliothek · 7 Folien"),
                            ("nozilla-slides-pitch.pptx", "Pitch-Deck · 12 Folien")],
         "../templates/google-slides/"),
        ("Code", [("design-system.css", "Design System · CSS"), ("design-system.js", "Verhalten · JS"),
                  ("ci.css", "CI-Dokument · CSS")], "../"),
    ]
    secs = []
    for name, files, base in groups:
        rows = "\n".join(f'<tr><td><b>{lbl}</b></td><td><code>{f}</code></td>'
                         f'<td><a class="nz-btn nz-btn--sm nz-btn--secondary" href="{base}{f}" download>Laden</a></td></tr>'
                         for f, lbl in files)
        secs.append(f'<section class="sec"><h2>{name}.</h2><table class="tbl"><tbody>{rows}</tbody></table></section>')
    body = f"""<p class="nz-muted" style="max-width:68ch">Alle Icons einzeln gibt es auf der
      <a href="icons.html">Icon-Seite</a> — dort auch der SVG-Quelltext zum Kopieren.</p>
      {"".join(secs)}"""
    write("downloads.html", "Downloads.", "Anwendung", "Jede Datei der Marke — gebündelt und benannt.", body)


# ── Print-Vorlagen ────────────────────────────────────────────────────────
PRINT_BASE = """
  @page { size: %(size)s; margin: 0; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: #9a9a9a; }
  body { font-family: 'Inter', system-ui, sans-serif; color: #000; }
  .sheet { background: #fff; position: relative; overflow: hidden; margin: 16px auto;
           box-shadow: 0 0 0 1px rgba(0,0,0,.25); }
  .mono { font-family: 'Space Mono', monospace; letter-spacing: .1em; text-transform: uppercase; }
  .wm { font-family: 'Zilla Slab', serif; font-weight: 700; letter-spacing: -.02em; }
  .wm i { color: #00FF9C; font-style: normal; }
  @media print {
    html, body { background: #fff; }
    .sheet { margin: 0; box-shadow: none; page-break-after: always; }
    .no-print { display: none !important; }
  }
"""


def p_briefpapier():
    css = PRINT_BASE % {"size": "A4"} + """
  .sheet { width: 210mm; height: 297mm; padding: 20mm 20mm 16mm; }
  .head { display: flex; justify-content: space-between; align-items: flex-start;
          border-bottom: 2px solid #000; padding-bottom: 6mm; }
  .head .wm { font-size: 30pt; line-height: 1; }
  .head .meta { text-align: right; font-size: 7pt; line-height: 1.7; color: #555; }
  .fold { position: absolute; left: 0; width: 6mm; height: 0; border-top: .4pt solid #999; }
  .fold--1 { top: 105mm; } .fold--2 { top: 210mm; } .fold--punch { top: 148.5mm; width: 10mm; border-top-width: .6pt; }
  .addr { margin-top: 18mm; font-size: 10pt; line-height: 1.5; min-height: 30mm; }
  .addr .from { font-size: 6.5pt; color: #555; border-bottom: .4pt solid #999;
                padding-bottom: 1mm; margin-bottom: 3mm; }
  .date { margin-top: 6mm; }
  .subject { font-family: 'Zilla Slab', serif; font-weight: 700; font-size: 15pt;
             line-height: 1.2; margin: 10mm 0 6mm; }
  .body { font-size: 10pt; line-height: 1.6; }
  .body p { margin: 0 0 4mm; }
  mark { background: #00FF9C; padding: 0 .12em; }
  .foot { position: absolute; left: 20mm; right: 20mm; bottom: 12mm;
          border-top: 2px solid #000; padding-top: 3mm;
          display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm;
          font-size: 6.5pt; line-height: 1.6; color: #555; }
"""
    html_doc = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"/>
<title>nozilla — Briefpapier</title>
<link rel="stylesheet" href="../project/fonts.css"/>
<style>{css}</style></head>
<body>
<div class="sheet">
  <div class="fold fold--1"></div><div class="fold fold--punch"></div><div class="fold fold--2"></div>
  <header class="head">
    <div class="wm">nozilla<i>.</i></div>
    <div class="meta mono">nozilla<br/>[STRASSE NR.]<br/>[PLZ ORT]<br/>{MAIL}</div>
  </header>
  <div class="addr">
    <div class="from mono">nozilla · [STRASSE NR.] · [PLZ ORT]</div>
    [FIRMA]<br/>[ANSPRECHPARTNER:IN]<br/>[STRASSE NR.]<br/>[PLZ ORT]
  </div>
  <div class="mono date" style="font-size:7.5pt;color:#555">[ORT], [TT.MM.JJJJ]</div>
  <div class="subject">[BETREFF IN EINEM SATZ.]</div>
  <div class="body">
    <p>Sehr geehrte:r [NAME],</p>
    <p>[EINSTIEG: Was ist der Anlass? Ein Satz, keine Floskel.]</p>
    <p>[KERN: Was schlagen wir vor? <mark>Eine Behauptung</mark>, die man prüfen kann.]</p>
    <p>[ABSCHLUSS: Der nächste konkrete Schritt. Wer macht was bis wann?]</p>
    <p style="margin-top:8mm">Mit freundlichen Grüßen<br/><br/><br/>[NAME] · [ROLLE]</p>
  </div>
  <footer class="foot mono">
    <div>nozilla<br/>[STRASSE NR.]<br/>[PLZ ORT]</div>
    <div>{MAIL}<br/>nozilla.de<br/>[TELEFON]</div>
    <div>[INHABER:IN / GF]<br/>[REGISTER-NR.]<br/>USt-ID: [DE…]</div>
    <div>[BANK]<br/>IBAN [DE…]<br/>BIC [—]</div>
  </footer>
</div>
<p class="no-print mono" style="text-align:center;font-size:9pt;color:#fff;padding:8px 0 24px">
  Drucken → „Als PDF sichern“ · Ränder: keine · Hintergrundgrafiken: an
  &nbsp;·&nbsp; <a href="vorlagen.html" style="color:#00FF9C">zurück zum CI-Portal</a></p>
</body></html>
"""
    with open(os.path.join(OUT, "briefpapier.html"), "w") as f:
        f.write(html_doc)


def p_visitenkarte():
    css = PRINT_BASE % {"size": "91mm 61mm"} + """
  .sheet { width: 91mm; height: 61mm; padding: 3mm; }          /* 85×55 + 3mm Beschnitt */
  .card { width: 85mm; height: 55mm; margin: 0 auto; position: relative;
          outline: .25pt dashed rgba(0,0,0,.18); padding: 7mm; }
  @media print { .card { outline: none; } }
  /* Vollflächige Motive müssen bis in den Beschnitt laufen. */
  .sheet--ink { background: #0C0C0A; }
  .card--back { background: #0C0C0A; color: #FFFEE5; }
  .name { font-family: 'Zilla Slab', serif; font-weight: 700; font-size: 15pt; line-height: 1.1; }
  .role { font-size: 8pt; color: #555; margin-top: 1mm; }
  .contact { position: absolute; left: 7mm; bottom: 7mm; font-size: 7.5pt; line-height: 1.7; }
  .mark { position: absolute; right: 7mm; bottom: 6mm; font-size: 17pt; }
  .back-center { position: absolute; inset: 0; display: flex; flex-direction: column;
                 align-items: center; justify-content: center; gap: 3mm; }
  .claim { font-family: 'Zilla Slab', serif; font-size: 11pt; }
  /* Randabfallend: 3 mm in den Beschnitt hinein, 4 mm sichtbar. */
  .bar { position: absolute; left: -3mm; top: -3mm; bottom: -3mm; width: 7mm; background: #00FF9C; }
"""
    html_doc = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"/>
<title>nozilla — Visitenkarte</title>
<link rel="stylesheet" href="../project/fonts.css"/>
<style>{css}</style></head>
<body>
<div class="sheet"><div class="card">
  <div class="bar"></div>
  <div style="margin-left:4mm">
    <div class="name">[VORNAME<br/>NACHNAME]</div>
    <div class="role mono">[ROLLE]</div>
  </div>
  <div class="contact mono" style="margin-left:4mm">
    {MAIL}<br/>[+49 …]<br/>nozilla.de
  </div>
  <div class="mark wm">nozilla<i>.</i></div>
</div></div>

<div class="sheet sheet--ink"><div class="card card--back">
  <div class="back-center">
    <div class="wm" style="font-size:26pt">nozilla<i>.</i></div>
    <div class="claim">Gute <span style="background:#00FF9C;color:#000;padding:0 .12em">digitale</span> Dienste.</div>
  </div>
</div></div>

<p class="no-print mono" style="text-align:center;font-size:9pt;color:#fff;padding:8px 0 24px">
  85 × 55 mm + 3 mm Beschnitt · Drucken → „Als PDF sichern“, Ränder: keine
  &nbsp;·&nbsp; <a href="vorlagen.html" style="color:#00FF9C">zurück zum CI-Portal</a></p>
</body></html>
"""
    with open(os.path.join(OUT, "visitenkarte.html"), "w") as f:
        f.write(html_doc)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    p_index(); p_grundlagen(); p_logo(); p_farbe(); p_typografie()
    p_icons(); p_bilder(); p_komponenten(); p_sprache(); p_vorlagen(); p_downloads()
    p_briefpapier(); p_visitenkarte()
    pages = sorted(f for f in os.listdir(OUT) if f.endswith(".html"))
    print(f"{len(pages)} Seiten gebaut: {', '.join(pages)}")
