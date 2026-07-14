#!/usr/bin/env node
/* ============================================================================
   nozilla CI — asset integrity check (zero dependencies)

   Guards the class of bug that once left the CI document full of placeholders:
     1. every local href/src/url()/@import in HTML & CSS resolves to a real file
     2. CSS brace balance
     3. required deliverables exist (fonts, favicon, social image, print masters)

   Exit 0 = clean · exit 1 = problems (prints each one).
============================================================================ */
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, dirname, resolve, relative } from "node:path";

const ROOT = process.cwd();
const problems = [];
const isRemote = (u) => /^(https?:)?\/\//i.test(u) || u.startsWith("data:") || u.startsWith("mailto:") || u.startsWith("#");

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === ".git" || name === "node_modules") continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const files = walk(ROOT);
const rel = (p) => relative(ROOT, p);

// ── 1. Reference resolution ────────────────────────────────────────────────
// No whitespace/wildcards in a real path — keeps comment prose from matching.
const ASSET_RE = /["'(]([^"'()\s*]+\.(?:css|js|mjs|svg|png|jpe?g|webp|ico|woff2?|ttf|otf|pdf|eps))["')]/gi;

for (const file of files) {
  if (!/\.(html?|css)$/i.test(file)) continue;
  const src = readFileSync(file, "utf8");
  const base = dirname(file);
  const seen = new Set();
  for (const m of src.matchAll(ASSET_RE)) {
    const ref = m[1].trim();
    if (isRemote(ref) || seen.has(ref)) continue;
    seen.add(ref);
    const target = resolve(base, ref.replace(/[?#].*$/, ""));
    if (!existsSync(target)) problems.push(`${rel(file)} → missing reference: ${ref}`);
  }
}

// ── 2. CSS brace balance ───────────────────────────────────────────────────
for (const file of files) {
  if (!/\.css$/i.test(file)) continue;
  const src = readFileSync(file, "utf8");
  const open = (src.match(/{/g) || []).length;
  const close = (src.match(/}/g) || []).length;
  if (open !== close) problems.push(`${rel(file)} → unbalanced braces: ${open} '{' vs ${close} '}'`);
}

// ── 3. Required deliverables ───────────────────────────────────────────────
const REQUIRED = [
  "index.html", "ci.css", "design-system.css", "design-system.html",
  "design-system.js", "components.html",
  "project/colors_and_type.css", "project/fonts.css",
  "project/fonts/ZillaSlab-Bold.ttf", "project/fonts/Inter-Regular.ttf", "project/fonts/SpaceMono-Regular.ttf",
  "project/assets/nozilla-logo.svg", "project/assets/nozilla-logo.eps", "project/assets/nozilla-logo.pdf",
  "project/assets/favicon.svg", "project/assets/favicon-32.png", "project/assets/favicon-180.png",
  "project/assets/og-image.png",
];
for (const r of REQUIRED) {
  if (!existsSync(join(ROOT, r))) problems.push(`required file missing: ${r}`);
}

// ── Report ─────────────────────────────────────────────────────────────────
if (problems.length) {
  console.error(`✗ asset integrity: ${problems.length} problem(s)\n`);
  for (const p of problems) console.error("  - " + p);
  process.exit(1);
}
console.log("✓ asset integrity: all references resolve, braces balanced, deliverables present");
