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
  /* Ein Index, beliebig viele Felder: die Kopfzeile auf jeder Seite, auf der
     Startseite zusätzlich der Hero. Jedes Feld zeigt seine Treffer selbst an. */
  var idx = window.NZ_INDEX || [];

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

  function bindSearch(q, box) {
    if (!q || !box) return;
    var active = -1;

    function render(list) {
      active = -1;
      box.hidden = false;
      if (!list.length) {
        box.innerHTML = '<div class="results__empty">Nichts gefunden. Andere Schreibweise probieren?</div>';
        return;
      }
      box.innerHTML = list.map(function (it) {
        return '<a href="' + it.u + '" role="option"><span>' + it.t +
          '</span><span class="cat">' + it.c + "</span></a>";
      }).join("");
    }

    q.addEventListener("input", function () {
      if (!q.value.trim()) { box.hidden = true; return; }
      render(search(q.value));
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
      } else if (e.key === "Enter") {
        e.preventDefault();
        links[active >= 0 ? active : 0].click();
      }
    });
    document.addEventListener("click", function (e) {
      if (!box.contains(e.target) && e.target !== q) box.hidden = true;
    });
    /* Formular abschicken (Knopf „Suchen") öffnet den besten Treffer. Bewusst
       neu gesucht: der Klick auf den Knopf hat die Liste da schon geschlossen. */
    var form = q.form;
    if (form) form.addEventListener("submit", function (e) {
      e.preventDefault();
      var list = search(q.value);
      if (list.length) location.href = list[0].u;
      else if (q.value.trim()) render(list);
      else q.focus();
    });
  }

  var q = document.getElementById("q");
  var hq = document.getElementById("hq");
  bindSearch(q, document.getElementById("results"));
  bindSearch(hq, document.getElementById("hresults"));

  /* „/" springt ins Suchfeld — in den Hero, solange er zu sehen ist */
  var heroSearch = document.querySelector(".hero-search");
  document.addEventListener("keydown", function (e) {
    if (e.key !== "/" || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) return;
    var target = hq && !document.body.classList.contains("hero-out") ? hq : q;
    if (target) { e.preventDefault(); target.focus(); }
  });
  if (heroSearch && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      document.body.classList.toggle("hero-out", !entries[0].isIntersecting);
    }).observe(heroSearch);
  } else if (heroSearch) {
    document.body.classList.add("hero-out");
  }

  /* ── Icon-Mosaik (Startseite) ──────────────────────────────────────────── */
  /* Alle 2,4 s tauscht eine Kachel ihr Motiv mit der Reserve: kurz invertiert,
     dann das neue Icon — harter Schnitt, kein Fade. Pausiert bei Hover, im
     Hintergrund-Tab und bei reduzierter Bewegung. */
  var mosaic = document.querySelector(".mosaic");
  var poolTpl = document.getElementById("mosaic-pool");
  if (mosaic && poolTpl && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var tiles = [].slice.call(mosaic.querySelectorAll(".mosaic__tile"));
    var pool = [].slice.call(poolTpl.content.querySelectorAll(".mosaic__tile"))
      .map(function (t) { return t.innerHTML; });
    var paused = false, turn = 0;
    mosaic.addEventListener("mouseenter", function () { paused = true; });
    mosaic.addEventListener("mouseleave", function () { paused = false; });
    setInterval(function () {
      if (paused || document.hidden || !pool.length) return;
      var visible = tiles.filter(function (t) { return t.offsetParent !== null; });
      var tile = visible[Math.floor(Math.random() * visible.length)];
      if (!tile) return;
      tile.classList.add("is-swap");
      setTimeout(function () {
        var slot = turn++ % pool.length, old = tile.innerHTML;
        tile.innerHTML = pool[slot];
        pool[slot] = old;
        tile.classList.remove("is-swap");
      }, 140);
    }, 2400);
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

  /* ── Icon-Katalog: Kategorie + Volltext ────────────────────────────────── */
  var catRoot = document.getElementById("catRoot");
  if (catRoot) {
    var catCells = Array.prototype.slice.call(catRoot.querySelectorAll(".cat-cell"));
    var catGrps = Array.prototype.slice.call(catRoot.querySelectorAll(".cat-grp"));
    var chips = Array.prototype.slice.call(document.querySelectorAll(".cat-chip"));
    var cq = document.getElementById("catQ");
    var tally = document.getElementById("catTally");
    var empty = document.getElementById("catEmpty");
    var reset = document.getElementById("catReset");
    var cat = "all";

    function applyCat() {
      var t = norm(cq ? cq.value.trim() : "");
      var shown = 0;
      catGrps.forEach(function (g) {
        var inCat = cat === "all" || g.getAttribute("data-cat") === cat;
        var visibleHere = 0;
        Array.prototype.forEach.call(g.querySelectorAll(".cat-cell"), function (c) {
          var ok = inCat && (!t || norm(c.getAttribute("data-k")).indexOf(t) >= 0);
          c.hidden = !ok;
          if (ok) visibleHere++;
        });
        g.hidden = visibleHere === 0;
        shown += visibleHere;
      });
      if (tally) tally.textContent = shown + " von " + catCells.length;
      if (empty) empty.hidden = shown !== 0;
    }

    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        cat = ch.getAttribute("data-cat");
        chips.forEach(function (o) { o.setAttribute("aria-pressed", o === ch ? "true" : "false"); });
        applyCat();
        // Die gewaehlte Gruppe in den Blick holen, ohne den Filterbalken zu verdecken.
        if (cat !== "all") {
          var g = catRoot.querySelector('.cat-grp[data-cat="' + cat + '"]');
          if (g) window.scrollTo({ top: g.offsetTop - 150, behavior: "smooth" });
        }
      });
    });
    if (cq) cq.addEventListener("input", applyCat);
    if (reset) reset.addEventListener("click", function () {
      if (cq) cq.value = "";
      cat = "all";
      chips.forEach(function (o) { o.setAttribute("aria-pressed", o.getAttribute("data-cat") === "all" ? "true" : "false"); });
      applyCat();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    // Direktlink wie katalog.html#business waehlt die Kategorie vor.
    var want = (location.hash || "").replace("#", "");
    if (want) {
      var pre = chips.filter(function (c) { return c.getAttribute("data-cat") === want; })[0];
      if (pre) pre.click();
    }
    applyCat();
  }

  /* ── Farbtabelle: Trefferzahl ──────────────────────────────────────────── */
  var ct = document.getElementById("colorTable");
  var cc = document.getElementById("colorCount");
  if (ct && cc) cc.textContent = ct.tBodies[0].rows.length + " Werte";
})();
