#!/usr/bin/env python3
"""Capture screenshots of key pages at several viewports for review."""
import http.server
import os
import socketserver
import threading
import functools
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
OUT = ROOT / "tests" / "qa-tmp" / "refine"
OUT.mkdir(parents=True, exist_ok=True)

PORT = 4173


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=str(SITE))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


PAGES = [
    ("home", "/"),
    ("about", "/about/"),
    ("chapter", "/about/chapter/"),
    ("degrees-index", "/about/degrees/"),
    ("degree-mark", "/about/degrees/mark-master-mason/"),
    ("events", "/events/"),
    ("contact", "/contact/"),
    ("404", "/404.html"),
]
VIEWPORTS = [(320, 720), (390, 844), (768, 1024), (1440, 900)]


def main():
    httpd = serve()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for w, h in VIEWPORTS:
                page = browser.new_page(
                    viewport={"width": w, "height": h},
                    device_scale_factor=1,
                )
                for name, path in PAGES:
                    page.goto(f"http://127.0.0.1:{PORT}{path}",
                              wait_until="load", timeout=45000)
                    page.wait_for_timeout(400)
                    page.screenshot(path=str(OUT / f"{name}-{w}.png"),
                                    full_page=True)
                page.close()
            browser.close()
    finally:
        httpd.shutdown()
    files = sorted(os.listdir(OUT))
    print(f"captured {len(files)} screenshots to {OUT}")


if __name__ == "__main__":
    main()
