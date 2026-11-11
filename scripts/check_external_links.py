#!/usr/bin/env python3
"""
External link checker for mcyorkrite.com.

Scans the generated _site output for outbound http(s) links and verifies each
responds. Distinguishes:

  OK         2xx/3xx
  WARN       temporary-looking failures (timeouts, DNS hiccups, 429, 5xx)
  BROKEN     definitive failures (404/410 and unreachable after one retry)

Network access is required; run manually or from a scheduled job, not from
the deployment pipeline (transient failures must not block deploys).

Usage:  python3 scripts/check_external_links.py [_site]
"""

import re
import sys
import time
import urllib.request
import urllib.error
import socket
from html.parser import HTMLParser
from pathlib import Path


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        href = a.get("href") or a.get("src")
        if href and href.startswith(("http://", "https://")):
            self.links.add(href)


def collect(site_root: Path):
    found = {}
    for page in sorted(site_root.rglob("*.html")):
        parser = LinkCollector()
        parser.feed(page.read_text(encoding="utf-8"))
        for link in parser.links:
            found.setdefault(link, []).append(str(page.relative_to(site_root)))
    return found


def check(url: str, timeout: float = 12.0) -> str:
    headers = {
        "User-Agent": (
            "mcyorkrite-link-checker/1.0 "
            "(static site validation; contact: website-contact@mcyorkrite.com)"
        )
    }
    for attempt in (1, 2):
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if response.status < 400:
                    return "OK"
                if response.status in (429, 500, 502, 503, 504):
                    status = f"WARN http {response.status}"
                else:
                    status = f"BROKEN http {response.status}"
        except urllib.error.HTTPError as exc:
            code = exc.code
            if code in (429, 500, 502, 503, 504):
                status = f"WARN http {code}"
            elif code in (401, 403):
                # Common for bot-protected sites (e.g. Google properties);
                # not evidence of a broken link.
                status = "WARN http 403/401 (bot protection)"
            else:
                status = f"BROKEN http {code}"
        except (urllib.error.URLError, socket.timeout, ConnectionError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            status = f"WARN {type(reason).__name__}: {reason}"
        if attempt == 1 and status.startswith("WARN"):
            time.sleep(2)  # one retry for transient errors
    return status


def main() -> int:
    site_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
    links = collect(site_root)
    print(f"Found {len(links)} unique external link(s)\n")

    results = {}
    for url in sorted(links):
        status = check(url)
        results[url] = status
        print(f"  {status:<40} {url}")

    broken = {u: s for u, s in results.items() if s.startswith("BROKEN")}
    warned = {u: s for u, s in results.items() if s.startswith("WARN")}

    print(f"\nOK: {len(results) - len(broken) - len(warned)}  "
          f"WARN: {len(warned)}  BROKEN: {len(broken)}")
    if broken:
        print("\nConfirmed broken links:")
        for url in sorted(broken):
            print(f"  ✗ {url}")
    if warned:
        print("\nWarnings (retry or verify manually):")
        for url in sorted(warned):
            print(f"  ⚠ {url}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
