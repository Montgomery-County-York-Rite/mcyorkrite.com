/*
 * Montgomery County York Rite — site behaviour
 * Vanilla JavaScript, no dependencies. Loaded with `defer`.
 *
 * 1. Accessible mobile navigation drawer
 * 2. Copy-address button on the contact page
 */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
   * 1. Mobile navigation drawer
   * ------------------------------------------------------------------ */
  var DESKTOP_QUERY = "(min-width: 900px)";
  var mq = window.matchMedia(DESKTOP_QUERY);

  var toggle = document.querySelector("[data-nav-toggle]");
  var drawer = document.getElementById("mobile-nav");
  var panel = drawer ? drawer.querySelector("[data-nav-panel]") : null;
  var label = toggle ? toggle.querySelector("[data-nav-label]") : null;

  function isOpen() {
    return toggle && toggle.getAttribute("aria-expanded") === "true";
  }

  function focusables() {
    if (!panel) return [];
    return panel.querySelectorAll(
      "a[href], button:not([disabled]), [tabindex]:not([tabindex='-1'])"
    );
  }

  function openDrawer() {
    if (!drawer || !toggle) return;
    drawer.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    if (label) label.textContent = "Close";
    document.body.style.overflow = "hidden";
    var links = focusables();
    if (links.length > 0) links[0].focus();
  }

  function closeDrawer(returnFocus) {
    if (!drawer || !toggle) return;
    drawer.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    if (label) label.textContent = "Menu";
    document.body.style.overflow = "";
    if (returnFocus) toggle.focus();
  }

  if (toggle && drawer && panel) {
    toggle.addEventListener("click", function () {
      if (isOpen()) {
        closeDrawer(false);
      } else {
        openDrawer();
      }
    });

    /* Close when the scrim or a navigation link is activated */
    drawer.addEventListener("click", function (event) {
      var target = event.target;
      if (
        target.hasAttribute("data-nav-close") ||
        target.closest("[data-nav-close]")
      ) {
        closeDrawer(false);
        return;
      }
      if (target.closest("a[href]")) {
        closeDrawer(false);
      }
    });

    /* Keyboard support: Escape closes and restores focus; Tab is trapped */
    document.addEventListener("keydown", function (event) {
      if (!isOpen()) return;
      if (event.key === "Escape") {
        event.preventDefault();
        closeDrawer(true);
        return;
      }
      if (event.key === "Tab") {
        var items = focusables();
        if (items.length === 0) return;
        var first = items[0];
        var last = items[items.length - 1];
        /* Shift+Tab from the first link returns to the menu toggle. */
  if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          toggle.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          /* Tab from the last link wraps to the first link inside the
             panel so focus never escapes the open drawer. */
          event.preventDefault();
          first.focus();
        }
      }
    });

    /* Reset when crossing into the desktop layout */
    mq.addEventListener("change", function (event) {
      if (event.matches && isOpen()) closeDrawer(false);
    });
  }

  /* ------------------------------------------------------------------
   * 2. Copy-address button
   * ------------------------------------------------------------------ */
  var copyBtn = document.querySelector("[data-copy-address]");

  function fallbackCopy(text) {
    var field = document.createElement("textarea");
    field.value = text;
    field.setAttribute("readonly", "");
    field.style.position = "fixed";
    field.style.opacity = "0";
    document.body.appendChild(field);
    field.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (err) {
      ok = false;
    }
    document.body.removeChild(field);
    return ok;
  }

  if (copyBtn) {
    var status = document.querySelector("[data-copy-status]");
    var statusTimer = null;

    copyBtn.addEventListener("click", function () {
      var text = copyBtn.getAttribute("data-copy-address") || "";

      function report(ok) {
        if (!status) return;
        status.textContent = ok
          ? "Address copied."
          : "Copy failed — please select the address manually.";
        if (statusTimer) window.clearTimeout(statusTimer);
        statusTimer = window.setTimeout(function () {
          status.textContent = "";
        }, 3000);
      }

      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard
          .writeText(text)
          .then(function () {
            report(true);
          })
          .catch(function () {
            report(fallbackCopy(text));
          });
      } else {
        report(fallbackCopy(text));
      }
    });
  }
})();
