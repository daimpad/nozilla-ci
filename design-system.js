/* ============================================================================
   nozilla Design System — optional behaviours (vanilla, zero dependencies)

   Progressive enhancement: every component degrades gracefully without this
   file. Accordions, dropdowns and popovers already work natively via
   <details>; this only adds tabs, dialogs, toasts, chip-removal, copy, and
   optional single-open accordions.

   Usage: <script src="design-system.js" defer></script>
   Namespaced on window.nz — currently exposes nz.toast(...).
============================================================================ */
(function () {
  "use strict";
  var nz = (window.nz = window.nz || {});

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  /* ── Tabs ──────────────────────────────────────────────────────────────
     <div class="nz-tabs"><button role="tab" aria-controls="panel-id">…</button></div>
     <div id="panel-id" role="tabpanel" data-nz-panel>…</div>                    */
  function initTabs(root) {
    root.querySelectorAll(".nz-tabs").forEach(function (bar) {
      var tabs = Array.prototype.slice.call(bar.querySelectorAll('[role="tab"]'));
      if (!tabs.length) return;
      function select(tab) {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute("aria-selected", on ? "true" : "false");
          t.tabIndex = on ? 0 : -1;
          var id = t.getAttribute("aria-controls");
          if (id) {
            var panel = document.getElementById(id);
            if (panel) panel.hidden = !on;
          }
        });
      }
      tabs.forEach(function (tab, i) {
        tab.addEventListener("click", function () { select(tab); });
        tab.addEventListener("keydown", function (e) {
          var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
          if (!d) return;
          e.preventDefault();
          var next = tabs[(i + d + tabs.length) % tabs.length];
          next.focus(); select(next);
        });
      });
      var current = bar.querySelector('[aria-selected="true"]') || tabs[0];
      select(current);
    });
  }

  /* ── Dialog / modal ────────────────────────────────────────────────────
     Trigger: <button data-nz-open="dialogId">
     Close:   any [data-nz-close] inside, or the backdrop click             */
  function initDialogs(root) {
    root.querySelectorAll("[data-nz-open]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var dlg = document.getElementById(btn.getAttribute("data-nz-open"));
        if (dlg && typeof dlg.showModal === "function") dlg.showModal();
      });
    });
    root.querySelectorAll("dialog.nz-modal").forEach(function (dlg) {
      dlg.addEventListener("click", function (e) {
        if (e.target && e.target.hasAttribute("data-nz-close")) { dlg.close(); return; }
        // click on the backdrop (outside the dialog's content box) closes it
        var r = dlg.getBoundingClientRect();
        var inside = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
        if (!inside) dlg.close();
      });
    });
  }

  /* ── Toasts ────────────────────────────────────────────────────────────
     nz.toast({ title, body, variant: 'signal'|'warn'|'danger', timeout })   */
  function toastRegion() {
    var r = document.querySelector(".nz-toast-region");
    if (!r) {
      r = document.createElement("div");
      r.className = "nz-toast-region";
      r.setAttribute("role", "region");
      r.setAttribute("aria-live", "polite");
      r.setAttribute("aria-label", "Benachrichtigungen");
      document.body.appendChild(r);
    }
    return r;
  }
  nz.toast = function (opts) {
    opts = opts || {};
    var el = document.createElement("div");
    el.className = "nz-toast" + (opts.variant ? " nz-toast--" + opts.variant : " nz-toast--signal");
    var t = document.createElement("div");
    if (opts.title) { var h = document.createElement("div"); h.className = "nz-toast__title"; h.textContent = opts.title; t.appendChild(h); }
    if (opts.body)  { var b = document.createElement("div"); b.className = "nz-toast__body";  b.textContent = opts.body;  t.appendChild(b); }
    el.appendChild(t);
    toastRegion().appendChild(el);
    var ms = typeof opts.timeout === "number" ? opts.timeout : 4000;
    if (ms > 0) setTimeout(function () { el.remove(); }, ms);
    return el;
  };

  /* ── Removable chips ───────────────────────────────────────────────────
     <span class="nz-chip">…<button class="nz-chip__x" data-nz-chip-remove>×</button></span> */
  function initChips(root) {
    root.addEventListener("click", function (e) {
      var x = e.target.closest ? e.target.closest("[data-nz-chip-remove]") : null;
      if (x) { var chip = x.closest(".nz-chip"); if (chip) chip.remove(); }
    });
  }

  /* ── Copy to clipboard ─────────────────────────────────────────────────
     <button data-nz-copy="text to copy">  (or data-nz-copy-target="#id")    */
  function initCopy(root) {
    root.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest("[data-nz-copy],[data-nz-copy-target]") : null;
      if (!btn) return;
      var text = btn.getAttribute("data-nz-copy");
      if (!text) {
        var sel = btn.getAttribute("data-nz-copy-target");
        var node = sel && document.querySelector(sel);
        text = node ? (node.textContent || node.value || "") : "";
      }
      if (!text) return;
      var done = function () { nz.toast({ title: "Kopiert", variant: "signal", timeout: 1600 }); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () {});
    });
  }

  /* ── Single-open accordions ────────────────────────────────────────────
     <div class="nz-accordion" data-nz-single> closes siblings on open        */
  function initAccordions(root) {
    root.querySelectorAll(".nz-accordion[data-nz-single]").forEach(function (acc) {
      var items = acc.querySelectorAll("details.nz-accordion__item");
      items.forEach(function (d) {
        d.addEventListener("toggle", function () {
          if (d.open) items.forEach(function (o) { if (o !== d) o.open = false; });
        });
      });
    });
  }

  ready(function () {
    var root = document;
    initTabs(root);
    initDialogs(root);
    initChips(root);
    initCopy(root);
    initAccordions(root);
  });
})();
