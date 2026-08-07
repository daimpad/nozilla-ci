/* ============================================================================
   nozilla CI-Portal — Verhalten (Vanilla, keine Abhängigkeiten)
   Globale Suche über window.NZ_INDEX, lokale Filter, Kopier-Buttons, Theme.
============================================================================ */
(function () {
  "use strict";

  /* ── Theme ─────────────────────────────────────────────────────────────── */
  var root = document.documentElement;
  var sw = document.getElementById("themeSwitch");
  function currentTheme() {
    return root.getAttribute("data-theme") ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  if (sw) {
    sw.checked = currentTheme() === "dark";
    sw.addEventListener("change", function () {
      var t = sw.checked ? "dark" : "light";
      root.setAttribute("data-theme", t);
      try { localStorage.setItem("nz-theme", t); } catch (e) {}
    });
  }

  /* ── Navigation (mobil) ────────────────────────────────────────────────── */
  var navBtn = document.getElementById("navToggle");
  var nav = document.getElementById("sideNav");
  if (navBtn && nav) {
    navBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      navBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ── Globale Suche ─────────────────────────────────────────────────────── */
  var q = document.getElementById("q");
  var box = document.getElementById("results");
  var idx = window.NZ_INDEX || [];
  var active = -1;

  function norm(s) {
    return (s || "").toLowerCase()
      .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");
  }

  function search(term) {
    var t = norm(term.trim());
    if (!t) return [];
    var words = t.split(/\s+/);
    var hits = [];
    for (var i = 0; i < idx.length; i++) {
      var hay = norm(idx[i].t + " " + idx[i].k + " " + idx[i].c);
      var ok = true, score = 0;
      for (var w = 0; w < words.length; w++) {
        var pos = hay.indexOf(words[w]);
        if (pos < 0) { ok = false; break; }
        score += pos === 0 ? 0 : 1;
      }
      if (ok) hits.push({ item: idx[i], score: score });
    }
    hits.sort(function (a, b) { return a.score - b.score; });
    return hits.slice(0, 12).map(function (h) { return h.item; });
  }

  function render(list) {
    if (!list.length) {
      box.innerHTML = '<div class="results__empty">Nichts gefunden. Andere Schreibweise probieren?</div>';
      box.hidden = false;
      return;
    }
    box.innerHTML = list.map(function (it) {
      return '<a href="' + it.u + '" role="option"><span>' + it.t +
        '</span><span class="cat">' + it.c + "</span></a>";
    }).join("");
    box.hidden = false;
    active = -1;
  }

  if (q && box) {
    q.addEventListener("input", function () {
      var v = q.value;
      if (!v.trim()) { box.hidden = true; return; }
      render(search(v));
    });
    q.addEventListener("keydown", function (e) {
      var links = box.querySelectorAll("a");
      if (e.key === "Escape") { box.hidden = true; q.blur(); return; }
      if (!links.length) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        active += e.key === "ArrowDown" ? 1 : -1;
        if (active < 0) active = links.length - 1;
        if (active >= links.length) active = 0;
        for (var i = 0; i < links.length; i++) links[i].classList.toggle("is-active", i === active);
        links[active].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter" && active >= 0) {
        e.preventDefault();
        links[active].click();
      }
    });
    document.addEventListener("click", function (e) {
      if (!box.contains(e.target) && e.target !== q) box.hidden = true;
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== q &&
          !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
        e.preventDefault(); q.focus();
      }
    });
  }

  /* ── Kopieren ──────────────────────────────────────────────────────────── */
  function flash(btn, label) {
    var old = btn.textContent;
    btn.textContent = label;
    setTimeout(function () { btn.textContent = old; }, 1200);
  }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("[data-copy],[data-svg]");
    if (!btn) return;
    var text = btn.getAttribute("data-copy") || btn.getAttribute("data-svg");
    if (!text || !navigator.clipboard) return;
    navigator.clipboard.writeText(text).then(function () { flash(btn, "Kopiert"); }, function () {});
  });

  /* ── Icon-Filter ───────────────────────────────────────────────────────── */
  var grid = document.getElementById("iconGrid");
  if (grid) {
    var cells = Array.prototype.slice.call(grid.children);
    var f = document.getElementById("iconFilter");
    var count = document.getElementById("iconCount");
    var dial = "all";

    function apply() {
      var t = norm(f ? f.value.trim() : "");
      var shown = 0;
      cells.forEach(function (c) {
        var okDial = dial === "all" || c.getAttribute("data-dial") === dial;
        var okText = !t || norm(c.getAttribute("data-k")).indexOf(t) >= 0;
        var vis = okDial && okText;
        c.hidden = !vis;
        if (vis) shown++;
      });
      if (count) count.textContent = shown + " von " + cells.length;
    }
    if (f) f.addEventListener("input", apply);
    document.querySelectorAll('input[name="dial"]').forEach(function (r) {
      r.addEventListener("change", function () { dial = r.value; apply(); });
    });
    apply();
  }

  /* ── Farbtabelle: Trefferzahl ──────────────────────────────────────────── */
  var ct = document.getElementById("colorTable");
  var cc = document.getElementById("colorCount");
  if (ct && cc) cc.textContent = ct.tBodies[0].rows.length + " Werte";
})();
