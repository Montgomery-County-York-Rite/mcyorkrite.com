#!/usr/bin/env python3
"""
Browser-based QA for mcyorkrite.com using headless Chromium (Playwright).

Serves the generated _site directory over a local HTTP server and runs, for
every page:

  - full-page screenshots at 320 / 390 / 768 / 1024 / 1440 / 1920 px
  - console error and CSP-violation capture
  - axe-core accessibility audit (WCAG 2.x AA ruleset)

Interaction checks on the homepage and contact page:

  - mobile drawer opens, traps focus, closes on Escape
  - skip link appears on first Tab press
  - copy-address button updates its status region

Usage:  python3 tests/visual_qa.py [_site] [--screens]
Output: tests/qa-tmp/report.json and screenshots in tests/qa-tmp/shots/
"""

import argparse
import json
import http.server
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "_site")
OUT = ROOT / "tests" / "qa-tmp"
SHOTS = OUT / "shots"
AXE_PATH = OUT / "axe.min.js"

if not AXE_PATH.is_file():
    # axe-core is a QA-time dependency (deque systems, MPL-2.0); fetch it on
    # demand so the repository does not carry a vendored copy.
    import urllib.request

    AXE_PATH.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(
        "https://unpkg.com/axe-core@4.10.2/axe.min.js", AXE_PATH
    )
AXE = AXE_PATH.read_text(encoding="utf-8")

PORT = 4873
PAGES = [
    ("/", "home"),
    ("/about/", "about"),
    ("/about/chapter/", "chapter"),
    ("/about/council/", "council"),
    ("/about/commandery/", "commandery"),
    ("/events/", "events"),
    ("/contact/", "contact"),
    ("/404.html", "notfound"),
]
VIEWPORTS = [(320, 640), (390, 800), (768, 1000), (1024, 720), (1440, 900), (1920, 1000)]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def log_message(self, *args):
        pass


def serve():
    """Start a background HTTP server for _site and keep it alive."""
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.4)
    return httpd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--screens", action="store_true", default=True)
    args = parser.parse_args()

    report = {"pages": {}, "interactions": {}, "errors": []}
    httpd = serve()
    print(f"Serving {SITE} on http://127.0.0.1:{PORT}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        for path, name in PAGES:
            page_report = {"console_errors": [], "csp_violations": [], "axe_violations": []}

            for (w, h) in VIEWPORTS:
                context = browser.new_context(viewport={"width": w, "height": h})
                page = context.new_page()

                console_messages = []
                page.on(
                    "console",
                    lambda msg: (
                        console_messages.append(f"{msg.type}: {msg.text}")
                        if msg.type in ("error",)
                        else None
                    ),
                )
                page.on(
                    "pageerror", lambda exc: console_messages.append(f"pageerror: {exc}")
                )

                page.goto(f"http://127.0.0.1:{PORT}{path}", wait_until="load", timeout=45000)
                page.wait_for_timeout(300)

                if args.screens:
                    SHOTS.mkdir(parents=True, exist_ok=True)
                    page.screenshot(
                        path=str(SHOTS / f"{name}-{w}.png"), full_page=True
                    )

                # record console errors only once per page (largest viewport)
                if (w, h) == (1440, 900):
                    page_report["console_errors"] = console_messages

                    # CSP violations surface as console errors containing
                    # "Content Security Policy" — pull them out explicitly
                    page_report["csp_violations"] = [
                        m for m in console_messages if "Content Security Policy" in m
                    ]

                    # axe audit
                    page.evaluate(AXE)
                    axe_results = page.evaluate(
                        "axe.run(document, {runOnly: {type: 'tag', values: "
                        "['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})"
                    )
                    for violation in axe_results.get("violations", []):
                        nodes = [
                            n.get("target") for n in violation.get("nodes", [])
                        ][:4]
                        page_report["axe_violations"].append(
                            {
                                "id": violation.get("id"),
                                "impact": violation.get("impact"),
                                "summary": violation.get("help"),
                                "nodes": nodes,
                            }
                        )

                context.close()

            report["pages"][path] = page_report
            status = (
                "OK"
                if not page_report["axe_violations"] and not page_report["console_errors"]
                else "ISSUES"
            )
            print(f"  {path:<24} {status}")

        # ---- Interaction checks ------------------------------------------------
        report["interactions"] = interactions(browser)

        browser.close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2))
    print(f"Report written to {OUT / 'report.json'}")

    failing = []
    for path, page_report in report["pages"].items():
        for v in page_report["axe_violations"]:
            failing.append(f"{path}: axe {v['id']} ({v['impact']}): {v['summary']}")
        for e in page_report["console_errors"]:
            failing.append(f"{path}: console {e}")
    for name, ok in report["interactions"].items():
        if not ok:
            failing.append(f"interaction failed: {name}")

    if failing:
        print(f"\n{len(failing)} finding(s):")
        for f in failing:
            print(f"  ✗ {f}")
        return 1
    print("\nAll browser checks passed.")
    return 0


def interactions(browser):
    results = {}

    # Mobile drawer behaviour (375x812)
    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(f"http://127.0.0.1:{PORT}/", wait_until="load", timeout=45000)

    toggle = page.locator("[data-nav-toggle]")
    results["toggle_visible_on_mobile"] = toggle.is_visible()
    results["drawer_hidden_on_load"] = page.evaluate(
        "document.getElementById('mobile-nav').hidden === true"
    )

    def drawer_open():
        return page.evaluate("document.getElementById('mobile-nav').hidden === false")

    # 1. open drawer
    toggle.click()
    results["drawer_opens"] = drawer_open()
    results["aria_expanded_true"] = toggle.get_attribute("aria-expanded") == "true"

    # 2. focus moves into the drawer
    results["focus_in_drawer"] = page.evaluate(
        "document.activeElement.closest('#mobile-nav') !== null"
    )

    # 3. Tab cycles inside the drawer (focus trap) — press Tab many times
    trapped = True
    for _ in range(14):
        page.keyboard.press("Tab")
        if page.evaluate("document.activeElement.closest('#mobile-nav') === null"):
            trapped = False
            break
    results["focus_trapped_in_drawer"] = trapped

    # 4. Escape closes and restores focus
    page.keyboard.press("Escape")
    results["drawer_closes_on_escape"] = page.evaluate(
        "document.getElementById('mobile-nav').hidden === true"
    )
    results["focus_restored_to_toggle"] = page.evaluate(
        "document.activeElement.hasAttribute('data-nav-toggle')"
    )
    results["aria_expanded_false"] = toggle.get_attribute("aria-expanded") == "false"

    # 5. drawer navigates to a page
    toggle.click()
    page.locator("#mobile-nav .nav-link", has_text="About").first.click()
    page.wait_for_load_state("networkidle")
    results["drawer_navigates"] = page.url.endswith("/about/")

    context.close()

    # Desktop header: inline nav shown, toggle hidden
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    page.goto(f"http://127.0.0.1:{PORT}/", wait_until="load", timeout=45000)
    results["toggle_hidden_on_desktop"] = not page.locator(
        "[data-nav-toggle]"
    ).is_visible()
    results["desktop_nav_visible"] = page.locator(".site-nav").is_visible()

    # Skip link behaviour
    page.keyboard.press("Tab")
    results["skip_link_first_tab"] = page.evaluate(
        "document.activeElement.classList.contains('skip-link')"
    )

    # Keyboard-only navigation through the header (before activating skip link)
    focus_chain = []
    for _ in range(6):
        page.keyboard.press("Tab")
        focus_chain.append(page.evaluate("document.activeElement.textContent.trim()"))
    results["keyboard_reaches_all_nav"] = any("Events" in t for t in focus_chain)

    # After activating the skip link, focus lands on main content
    page.goto(f"http://127.0.0.1:{PORT}/", wait_until="load", timeout=45000)
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.wait_for_timeout(200)
    results["skip_link_moves_focus_to_main"] = page.evaluate(
        "document.activeElement.id === 'main-content'"
    )

    # Copy address button (contact page)
    page.goto(f"http://127.0.0.1:{PORT}/contact/", wait_until="load", timeout=45000)
    if page.locator("[data-copy-address]").count():
        page.locator("[data-copy-address]").click()
        page.wait_for_timeout(300)
        results["copy_button_reports_status"] = (
            page.locator("[data-copy-status]").inner_text() != ""
        )
    else:
        results["copy_button_reports_status"] = False

    context.close()
    return results


if __name__ == "__main__":
    sys.exit(main())
