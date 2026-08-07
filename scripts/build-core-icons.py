#!/usr/bin/env python3
"""Kern-Icons nach project/assets/ schreiben — und pruefen, dass es stimmt.

Die Icons entstehen aus einer einzigen Quelle (templates/google-slides/build/
icons.py). Dieses Skript exportiert sie als SVG und stellt sicher, dass

  1. jedes Icon die Signal-gruene Signatur unten rechts traegt,
  2. kein Motiv in die dafuer reservierte Ecke ragt,
  3. die committeten Dateien dem Stand der Quelle entsprechen.

    python3 scripts/build-core-icons.py            # schreiben
    python3 scripts/build-core-icons.py --check    # nur pruefen (CI)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "templates", "google-slides", "build"))
import icons as ICONS  # noqa: E402

OUT = os.path.join(ROOT, "project", "assets")
SIGNATURE_MARK = 'fill="#00FF9C" stroke="none"'


def main(check_only):
    problems = []

    # 1 · Freihaltezone um die Signatur
    for slug, label in ICONS.clearance_violations():
        problems.append(f"{slug} ({label}) ragt in die fuer die Signatur reservierte Ecke")

    written = stale = 0
    for slug, label, _ in ICONS.ALL:
        svg = ICONS.to_svg(slug)

        # 2 · Signatur vorhanden?
        if SIGNATURE_MARK not in svg:
            problems.append(f"{slug} traegt keine Signatur")

        path = os.path.join(OUT, f"icon-{slug}.svg")
        current = open(path).read() if os.path.exists(path) else None
        if current == svg:
            continue
        if check_only:
            stale += 1
            problems.append(f"icon-{slug}.svg ist nicht auf dem Stand der Quelle")
        else:
            with open(path, "w") as f:
                f.write(svg)
            written += 1

    # 3 · Icon-Matrix und Mengenangabe im CI-Dokument mitziehen
    doc_path = os.path.join(ROOT, "index.html")
    doc = open(doc_path).read()
    tiles = "\n".join(
        f'      <div class="icon-tile" role="listitem">'
        f'<img src="project/assets/icon-{slug}.svg" alt="{label}"/></div>'
        for slug, label, _ in ICONS.ALL)
    matrix = ('<div class="icon-matrix" role="list" aria-label="Icon-Set">\n'
              + tiles + '\n    </div>')
    umfang = (f'<li><b>Umfang</b><span>{len(ICONS.HEAVY)} Heavy-Stroke, '
              f'{len(ICONS.PIXEL)} Pixel und {len(ICONS.CONCEPT)} Konzept-Icons.</span></li>')
    updated = re.sub(r'<div class="icon-matrix" role="list" aria-label="Icon-Set">.*?</div>\s*</section>',
                     matrix + '\n  </section>', doc, flags=re.S)
    updated = re.sub(r'<li><b>Umfang</b><span>[^<]*</span></li>', umfang, updated)
    if updated != doc:
        if check_only:
            problems.append("index.html: Icon-Matrix oder Mengenangabe nicht auf dem Stand")
        else:
            open(doc_path, "w").write(updated)

    # 4 · verwaiste Dateien melden (Icon wurde umbenannt oder entfernt)
    known = {f"icon-{s}.svg" for s, _, _ in ICONS.ALL}
    core_prefixes = tuple(f"icon-{s}." for s, _, _ in ICONS.ALL)
    for name in sorted(os.listdir(OUT)):
        if name.startswith("icon-") and name.endswith(".svg") and name not in known:
            problems.append(f"{name} gehoert zu keinem Icon mehr — entfernen")

    if problems:
        print(f"✗ Kern-Icons: {len(problems)} Problem(e)\n")
        for p in problems:
            print("  - " + p)
        if stale:
            print("\n  'python3 scripts/build-core-icons.py' ausfuehren und committen.")
        return 1

    n, h, px, c = len(ICONS.ALL), len(ICONS.HEAVY), len(ICONS.PIXEL), len(ICONS.CONCEPT)
    action = "geprueft" if check_only else f"geschrieben ({written} geaendert)"
    print(f"✓ Kern-Icons {action}: {n} Motive "
          f"({h} Heavy-Stroke, {px} Pixel-Art, {c} Konzept), alle mit Signatur")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
