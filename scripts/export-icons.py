#!/usr/bin/env python3
"""nozilla CI — Kern-Icons aus der einen Quelle nach project/assets/ exportieren.

templates/google-slides/build/icons.py definiert jedes Kern-Icon genau einmal
und rendert es wahlweise als PPTX-Form (Deck) oder als SVG (Web). Bis hierher
gab es fuer den SVG-Zweig aber keinen Export — die Dateien in project/assets/
waren von Hand abgelegt und konnten still von der Quelle abweichen.

Dieses Skript schliesst die Luecke:

    python3 scripts/export-icons.py            schreibt project/assets/icon-*.svg
    python3 scripts/export-icons.py --check    prueft nur, schreibt nichts

Exit 0 = sauber - Exit 1 = Abweichung (im Check-Modus) bzw. Fehler.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "templates", "google-slides", "build"))
import icons as ICONS  # noqa: E402

ASSETS = os.path.join(ROOT, "project", "assets")
CHECK = "--check" in sys.argv


def main():
    stale, written = [], 0
    for slug, _label, _fn in ICONS.ALL:
        path = os.path.join(ASSETS, "icon-%s.svg" % slug)
        want = ICONS.to_svg(slug)

        have = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                have = fh.read()

        if have == want:
            continue
        if CHECK:
            stale.append("fehlt" if have is None else "veraltet")
            stale[-1] = "  - project/assets/icon-%s.svg (%s)" % (slug, stale[-1])
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(want)
        written += 1

    # Jedes Icon muss die Signatur tragen — sonst stimmt etwas an der Quelle nicht.
    x, y, w, h = ICONS.SIGNATURE
    mark = 'x="%s" y="%s" width="%s" height="%s"' % (x, y, w, h)
    missing = [s for s, _, _ in ICONS.ALL if mark not in ICONS.to_svg(s)]
    if missing:
        print("x Signatur fehlt bei: %s" % ", ".join(missing), file=sys.stderr)
        return 1

    if CHECK and stale:
        print("x Kern-Icons nicht aktuell — 'python3 scripts/export-icons.py' "
              "ausfuehren und committen:\n%s" % "\n".join(stale), file=sys.stderr)
        return 1

    print("+ Kern-Icons: %d aus icons.py exportiert, alle mit Signatur%s"
          % (len(ICONS.ALL), " (%d geschrieben)" % written if written else " (unveraendert)"))
    if CHECK:
        print("  (--check: nichts geschrieben)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
