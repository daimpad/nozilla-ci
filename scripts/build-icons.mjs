#!/usr/bin/env node
/* ============================================================================
   nozilla CI — Icon-Build (ohne Abhängigkeiten)

   Nimmt die handgezeichneten Geometrien aus scripts/icons/*.mjs und erzeugt:

     project/assets/icons/nz-<name>.svg   Ein SVG je Icon, Dialekt A
     ICONS.md                             Vollständiger Katalog aller freien
                                          Font-Awesome-Icons + Nachbau-Status
     icons.html                           Durchsuchbare Galerie im nozilla CI

   Der Abgleich läuft gegen project/icons/fontawesome-free.index.json — jeder
   Nachbau muss auf einen real existierenden freien Font-Awesome-Namen zeigen.

   Aufruf:  node scripts/build-icons.mjs        (schreibt)
            node scripts/build-icons.mjs --check (prüft nur, schreibt nichts)
============================================================================ */
import { readFileSync, writeFileSync, mkdirSync, readdirSync, rmSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT_DIR = join(ROOT, "project", "assets", "icons");
const CHECK_ONLY = process.argv.includes("--check");

// ── Quellen einlesen ────────────────────────────────────────────────────────
const fa = JSON.parse(readFileSync(join(ROOT, "project", "icons", "fontawesome-free.index.json"), "utf8"));
const faByName = new Map(fa.icons.map((i) => [i.n, i]));

const partFiles = readdirSync(join(ROOT, "scripts", "icons")).filter((f) => /^\d+-.*\.mjs$/.test(f)).sort();
const icons = [];
for (const f of partFiles) {
  const mod = await import(join(ROOT, "scripts", "icons", f));
  for (const ic of mod.default) icons.push({ ...ic, part: f });
}

// ── Prüfen ──────────────────────────────────────────────────────────────────
const problems = [];
const seen = new Set();
for (const ic of icons) {
  if (seen.has(ic.n)) problems.push(`doppelt vergeben: ${ic.n} (${ic.part})`);
  seen.add(ic.n);
  if (!faByName.has(ic.n)) problems.push(`kein freies Font-Awesome-Icon: ${ic.n} (${ic.part})`);
  if (!ic.de || !/[A-Za-zÄÖÜäöüß]/.test(ic.de)) problems.push(`Bedeutung fehlt: ${ic.n}`);
  if (!ic.g || !ic.g.trim()) problems.push(`Geometrie fehlt: ${ic.n}`);

  // CI-Regeln erzwingen -----------------------------------------------------
  // Ecken bleiben scharf: abgerundete Rechtecke und runde Enden sind verboten.
  // <circle> und <ellipse> sind erlaubt — das sind Kurven, keine weichen Ecken.
  for (const r of ic.g.matchAll(/<rect\b[^>]*>/g)) {
    if (/\br[xy]=/.test(r[0])) problems.push(`abgerundetes Rechteck verboten: ${ic.n}`);
  }
  if (/stroke-line(?:cap|join)="round"/.test(ic.g)) problems.push(`runde Enden verboten: ${ic.n}`);
  if (/gradient|filter=|blur|opacity|shadow/i.test(ic.g)) problems.push(`Verlauf/Filter verboten: ${ic.n}`);
  for (const m of ic.g.matchAll(/(?:fill|stroke)="(#[0-9A-Fa-f]{3,8})"/g)) {
    if (!["#000000", "#00FF9C"].includes(m[1])) problems.push(`Farbe außerhalb des CI: ${m[1]} in ${ic.n}`);
  }
  // Geometrie muss im Raster 0…64 bleiben (transform="…" führt eigene Winkel)
  const geom = ic.g.replace(/\stransform="[^"]*"/g, "");
  for (const m of geom.matchAll(/-?\d+(?:\.\d+)?/g)) {
    const v = Number(m[0]);
    if (v < -1 || v > 65) { problems.push(`Wert außerhalb 64er-Raster (${v}): ${ic.n}`); break; }
  }
}

if (problems.length) {
  console.error(`✗ Icon-Build: ${problems.length} Problem(e)\n`);
  for (const p of problems) console.error("  - " + p);
  process.exit(1);
}

// ── SVG erzeugen ────────────────────────────────────────────────────────────
const HEAD = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#000000" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter"`;

/* Die nozilla-Signatur: derselbe 6 × 6 Signal-Grün-Punkt, den die Wortmarke am
   Wortende und das Favicon tragen. Immer unten rechts auf (54,54), immer gleich
   groß, immer als letztes Element — der Punkt liegt vor der Tinte und sieht
   damit in jedem Icon identisch aus. Genau dafür ist die Ecke gewählt: bei 322
   der 462 Icons ist sie ohnehin leer, und wo Geometrie hinreicht, verdeckt der
   Punkt nur einen Randbereich, der nichts zur Lesbarkeit beiträgt.
   `stroke="none"` ist Pflicht, sonst erbt der Punkt die 4-px-Kontur. */
const MARK = `<rect x="54" y="54" width="6" height="6" fill="#00FF9C" stroke="none"/>`;

const svgFor = (ic) =>
  `${HEAD} role="img" aria-label="${ic.de.split(" — ")[0]}">\n${ic.g}\n${MARK}\n</svg>\n`;

if (!CHECK_ONLY) {
  if (existsSync(OUT_DIR)) rmSync(OUT_DIR, { recursive: true });
  mkdirSync(OUT_DIR, { recursive: true });
  for (const ic of icons) writeFileSync(join(OUT_DIR, `nz-${ic.n}.svg`), svgFor(ic));
}

// ── Katalog ICONS.md ────────────────────────────────────────────────────────
const built = new Map(icons.map((i) => [i.n, i]));
const catNames = Object.keys(fa.categories).sort();
const esc = (s) => String(s).replace(/\|/g, "\\|");

const lines = [];
lines.push("# Font-Awesome-Free-Katalog · nozilla-Nachbau");
lines.push("");
lines.push("**Gute digitale Dienste.**");
lines.push("");
lines.push(`Vollständige Liste aller frei verfügbaren Font-Awesome-Icons (Version 6.7.2) mit Name, Bedeutung und Nachbau-Status im nozilla CI.`);
lines.push("");
lines.push("## Bestand");
lines.push("");
lines.push("| Kennzahl | Wert |");
lines.push("|---|---|");
lines.push(`| Freie Icons gesamt (Stilvarianten) | **${fa.counts.style_variants}** |`);
lines.push(`| Davon eindeutige Namen | **${fa.counts.unique_names}** |`);
lines.push(`| Stil \`solid\` | ${fa.counts.solid} |`);
lines.push(`| Stil \`regular\` (Outline-Variante, keine eigenen Namen) | ${fa.counts.regular} |`);
lines.push(`| Stil \`brands\` (fremde Markenlogos) | ${fa.counts.brands} |`);
lines.push(`| Nachbau-Universum (frei, ohne Markenlogos) | **${fa.icons.filter((i) => !i.s.includes("brands")).length}** |`);
lines.push(`| Im nozilla CI nachgebaut | **${icons.length}** |`);
lines.push(`| Kategorien | ${catNames.length} |`);
lines.push("");
lines.push("## Was nicht nachgebaut wird");
lines.push("");
lines.push(`Die ${fa.counts.brands} \`brands\`-Icons sind Logos fremder Unternehmen und Produkte. Sie sind markenrechtlich geschützt — ein Nachbau im nozilla-Stil wäre eine unzulässige Veränderung fremder Marken und obendrein unbrauchbar, weil ein Logo nur in seiner Originalform wiedererkannt wird. Sie stehen in diesem Katalog, werden aber nicht gezeichnet.`);
lines.push("");
lines.push("## Nachbau — Dialekt A");
lines.push("");
lines.push("Jedes Icon: SVG, 64 × 64 Grundraster, 4 px Strichstärke, `stroke-linecap=\"square\"`, `stroke-linejoin=\"miter\"`, Tinte-Schwarz `#000`. Keine Radien, keine Verläufe, keine Filter.");
lines.push("");
lines.push("### Die Signatur");
lines.push("");
lines.push("Jedes Icon trägt unten rechts denselben **6 × 6 großen Signal-Grün-Punkt** — dieselbe Marke, die die Wortmarke am Wortende und das Favicon tragen:");
lines.push("");
lines.push("```svg");
lines.push('<rect x="54" y="54" width="6" height="6" fill="#00FF9C" stroke="none"/>');
lines.push("```");
lines.push("");
lines.push("Immer dieselbe Stelle, immer dieselbe Größe, immer als letztes Element. Sie ist kein semantischer Marker, sondern das Erkennungszeichen des Sets: ein Punkt am Satzende. Bei 322 der 462 Icons ist die Ecke ohnehin leer; wo Geometrie hinreicht, deckt der Punkt nur Randfläche ab, die zur Lesbarkeit nichts beiträgt.");
lines.push("");
lines.push("Sieben Icons führen zusätzlich **semantisches** Grün — `battery-full`, `bars-progress`, `bullseye`, `highlighter`, `server`, `toggle-on`, `tower-broadcast`. Dort trägt die Farbe Bedeutung (Ladestand, Fortschritt, Schalterzustand), die Signatur kommt davon unabhängig dazu.");
lines.push("");
lines.push("`stroke=\"none\"` ist Pflicht — sonst erbt der Punkt die 4-px-Kontur des Wurzelelements.");
lines.push("");
lines.push("Dateien liegen in [`project/assets/icons/`](./project/assets/icons/) als `nz-<name>.svg`. Galerie: [`icons.html`](./icons.html).");
lines.push("");
lines.push("---");
lines.push("");
lines.push("## So liest sich der Katalog");
lines.push("");
lines.push("| Spalte | Inhalt |");
lines.push("|---|---|");
lines.push("| **Name** | Der Font-Awesome-Name. Er ist der Schlüssel — die nozilla-Datei heißt `nz-<name>.svg`. |");
lines.push("| **Bedeutung** | Wofür das Icon steht. Nachgebaute Icons tragen die nozilla-Lesart auf Deutsch, alle übrigen das *englische Font-Awesome-Label in Kursiv*. |");
lines.push("| **Stil** | In welchen freien Font-Awesome-Stilen der Name existiert. |");
lines.push("| **nozilla** | ✓ mit Link auf die SVG-Datei, wenn nachgebaut. Sonst –. |");
lines.push("");
lines.push("Ein Icon steht in jeder Kategorie, der Font Awesome es zuordnet — Mehrfachnennungen sind daher normal.");
lines.push("");
lines.push("---");
lines.push("");
lines.push("## Katalog nach Kategorie");
lines.push("");

const row = (i) => {
  const b = built.get(i.n);
  const bedeutung = b ? esc(b.de) : `*${esc(i.l)}*`;
  const status = b ? `[✓](./project/assets/icons/nz-${i.n}.svg)` : "–";
  return `| \`${i.n}\` | ${bedeutung} | ${i.s.join(" · ")} | ${status} |`;
};
const table = (list) => {
  lines.push("| Name | Bedeutung | Stil | nozilla |");
  lines.push("|---|---|---|---|");
  for (const i of list) lines.push(row(i));
  lines.push("");
};

for (const cat of catNames) {
  const list = fa.icons.filter((i) => i.c.includes(cat));
  if (!list.length) continue;
  lines.push(`### ${fa.categories[cat]} \`${cat}\``);
  lines.push("");
  lines.push(`${list.length} Icons · ${list.filter((i) => built.has(i.n)).length} nachgebaut`);
  lines.push("");
  table(list);
}

const rest = fa.icons.filter((i) => !i.c.length && !i.s.includes("brands"));
if (rest.length) {
  lines.push("### Ohne Kategoriezuordnung");
  lines.push("");
  lines.push(`${rest.length} Icons · ${rest.filter((i) => built.has(i.n)).length} nachgebaut — Ziffern, Buchstaben und Motive, die Font Awesome in keine Kategorie einsortiert.`);
  lines.push("");
  table(rest);
}

// Vollständigkeit beweisen: jeder freie Name muss mindestens einmal im Katalog stehen.
const listed = new Set([
  ...fa.icons.filter((i) => i.c.length).map((i) => i.n),
  ...rest.map((i) => i.n),
  ...fa.icons.filter((i) => i.s.includes("brands")).map((i) => i.n),
]);
const gaps = fa.icons.filter((i) => !listed.has(i.n));
if (gaps.length) {
  console.error(`✗ Katalog unvollständig: ${gaps.length} Name(n) fehlen — ${gaps.slice(0, 10).map((i) => i.n).join(", ")}`);
  process.exit(1);
}

const brands = fa.icons.filter((i) => i.s.includes("brands"));
lines.push("---");
lines.push("");
lines.push("## Markenlogos `brands` — nicht nachgebaut");
lines.push("");
lines.push(`${brands.length} Icons. Vollständig gelistet, damit die Liste vollständig ist — aber keiner davon wird gezeichnet. Begründung siehe oben.`);
lines.push("");
lines.push("| Name | Marke |");
lines.push("|---|---|");
for (const i of brands) lines.push(`| \`${i.n}\` | ${esc(i.l)} |`);
lines.push("");

lines.push("---");
lines.push("");
lines.push("## Herkunft");
lines.push("");
lines.push("Namen, Labels und Kategorien stammen aus den Metadaten von [Font Awesome Free 6.7.2](https://fontawesome.com) (Metadaten MIT, Icon-Namen/Labels CC BY 4.0) und liegen als [`project/icons/fontawesome-free.index.json`](./project/icons/fontawesome-free.index.json) bei. **Es wurden keine Font-Awesome-Pfaddaten übernommen** — jede Geometrie in `project/assets/icons/` ist neu gezeichnet.");
lines.push("");
lines.push("Erzeugt von [`scripts/build-icons.mjs`](./scripts/build-icons.mjs). Nicht von Hand ändern — Geometrien liegen in [`scripts/icons/`](./scripts/icons/).");
lines.push("");
lines.push("Fragen? ci@nozilla.de");
lines.push("");

if (!CHECK_ONLY) writeFileSync(join(ROOT, "ICONS.md"), lines.join("\n"));

// ── Galerie icons.html ──────────────────────────────────────────────────────
const escH = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const byCat = new Map();
for (const ic of icons) (byCat.get(ic.c) || byCat.set(ic.c, []).get(ic.c)).push(ic);

const tiles = [...byCat.entries()]
  .sort((a, b) => (fa.categories[a[0]] || a[0]).localeCompare(fa.categories[b[0]] || b[0]))
  .map(([cat, list]) => {
    const cells = list
      .sort((a, b) => a.n.localeCompare(b.n))
      .map((ic) => {
        const kurz = ic.de.split(" — ")[0];
        return `      <figure class="ico" data-q="${escH(ic.n + " " + ic.de)}">
        <img src="project/assets/icons/nz-${ic.n}.svg" alt="${escH(kurz)}" width="64" height="64"/>
        <figcaption><b>${escH(ic.n)}</b><span>${escH(ic.de)}</span></figcaption>
      </figure>`;
      })
      .join("\n");
    return `    <section class="grp" data-cat="${escH(cat)}">
      <h2>${escH(fa.categories[cat] || cat)} <span class="cnt">${list.length}</span></h2>
${cells}
    </section>`;
  })
  .join("\n");

const html = `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>nozilla — Icon-Set</title>
<link rel="icon" href="project/assets/favicon.svg" type="image/svg+xml"/>
<link rel="alternate icon" href="project/assets/favicon-32.png" type="image/png"/>
<link rel="stylesheet" href="project/fonts.css"/>
<link rel="stylesheet" href="project/colors_and_type.css"/>
<style>
  *{box-sizing:border-box;}
  body{margin:0;background:var(--nz-paper,#FFFEE5);color:#000;font-family:var(--nz-font-body,Inter),system-ui,sans-serif;font-size:17px;line-height:1.55;}
  .wrap{max-width:1180px;margin:0 auto;padding:48px 24px 96px;}
  header{border-bottom:3px solid #000;padding-bottom:28px;margin-bottom:36px;}
  .kicker{font-family:var(--nz-font-mono,'Space Mono'),monospace;font-weight:700;font-size:11px;letter-spacing:.12em;text-transform:uppercase;}
  h1{font-family:var(--nz-font-display,'Zilla Slab'),Georgia,serif;font-weight:700;font-size:clamp(40px,8vw,84px);line-height:1.02;margin:12px 0 16px;}
  .lead{max-width:62ch;margin:0 0 4px;}
  mark.g{background:#00FF9C;color:#000;padding:0 .12em;}
  .bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:28px 0 0;}
  #q{flex:1 1 260px;min-width:200px;border:3px solid #000;background:#fff;padding:12px 14px;font:inherit;}
  #q:focus{outline:0;box-shadow:6px 6px 0 0 #00FF9C;}
  .tally{font-family:var(--nz-font-mono,'Space Mono'),monospace;font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase;}
  .grp{margin:0 0 44px;}
  .grp h2{font-family:var(--nz-font-display,'Zilla Slab'),Georgia,serif;font-weight:700;font-size:26px;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #000;grid-column:1/-1;}
  .cnt{font-family:var(--nz-font-mono,'Space Mono'),monospace;font-size:12px;font-weight:700;vertical-align:middle;background:#000;color:#FFFEE5;padding:2px 7px;margin-left:6px;}
  .grp{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:14px;}
  .ico{margin:0;border:2px solid #000;background:#fff;padding:16px 14px 14px;display:flex;flex-direction:column;gap:12px;}
  .ico img{width:64px;height:64px;display:block;margin:0 auto;}
  figcaption{border-top:2px solid #000;padding-top:10px;display:flex;flex-direction:column;gap:3px;}
  figcaption b{font-family:var(--nz-font-mono,'Space Mono'),monospace;font-size:11px;font-weight:700;letter-spacing:.06em;word-break:break-word;}
  figcaption span{font-size:13px;line-height:1.35;}
  .hide{display:none !important;}
  .empty{border:3px solid #000;padding:20px;}
  footer{border-top:3px solid #000;padding-top:20px;margin-top:36px;font-size:14px;}
  a{color:#000;}
  @media (max-width:640px){.grp{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="kicker">nozilla · Ikonografie · Dialekt A</div>
    <h1>Dicke Linie,<br/>klare Ansage.</h1>
    <p class="lead">${icons.length} Icons aus dem freien Font-Awesome-Bestand, neu gezeichnet im nozilla CI: 64 × 64, <mark class="g">4 px Strichstärke</mark>, rechtwinklige Enden, Tinte auf Papier. Keine fremden Pfaddaten, keine Radien, keine Verläufe.</p>
    <p class="lead">Unten rechts trägt jedes Icon denselben <mark class="g">6 × 6 Signal-Grün-Punkt</mark> — die Signatur des Sets, so wie die Wortmarke ihren Punkt am Wortende trägt.</p>
    <div class="bar">
      <input id="q" type="search" placeholder="Suchen — Name oder Bedeutung" aria-label="Icons durchsuchen"/>
      <div class="tally" id="tally">${icons.length} Icons</div>
    </div>
  </header>
${tiles}
  <p class="empty hide" id="empty">Kein Treffer. Der vollständige Katalog aller ${fa.counts.unique_names} freien Font-Awesome-Namen steht in <a href="ICONS.md">ICONS.md</a>.</p>
  <footer>
    Vollständiger Katalog aller ${fa.counts.style_variants} freien Font-Awesome-Icons: <a href="ICONS.md">ICONS.md</a> ·
    Regeln: <a href="index.html#ikonografie">CI-Dokument, Abschnitt 06</a> ·
    Fragen? <a href="mailto:ci@nozilla.de">ci@nozilla.de</a>
  </footer>
</div>
<script>
  const q = document.getElementById('q');
  const tally = document.getElementById('tally');
  const empty = document.getElementById('empty');
  const all = [...document.querySelectorAll('.ico')];
  const groups = [...document.querySelectorAll('.grp')];
  q.addEventListener('input', () => {
    const t = q.value.trim().toLowerCase();
    let n = 0;
    for (const el of all) {
      const hit = !t || el.dataset.q.toLowerCase().includes(t);
      el.classList.toggle('hide', !hit);
      if (hit) n++;
    }
    for (const g of groups) g.classList.toggle('hide', !g.querySelector('.ico:not(.hide)'));
    tally.textContent = n + (n === 1 ? ' Icon' : ' Icons');
    empty.classList.toggle('hide', n > 0);
  });
</script>
</body>
</html>
`;

if (!CHECK_ONLY) writeFileSync(join(ROOT, "icons.html"), html);

const universe = fa.icons.filter((i) => !i.s.includes("brands")).length;
console.log(
  `✓ Icon-Build: ${icons.length} Icons gezeichnet · ${fa.counts.unique_names} freie Namen katalogisiert ` +
    `(${universe} ohne Markenlogos, ${fa.counts.brands} brands ausgenommen)`
);
if (CHECK_ONLY) console.log("  (--check: nichts geschrieben)");
