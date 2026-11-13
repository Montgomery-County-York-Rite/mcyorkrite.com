#!/usr/bin/env python3
"""
Static-site validator for mcyorkrite.com.

Run against the generated _site directory:

    python3 tests/validate_site.py _site

Checks (see DESIGN notes in docs/qa-report.md for the mapping to the QA plan):

  1. Build      — every required page exists at its production URL.
  2. Metadata   — unique, non-empty <title> and meta description on every
                  page; canonical URLs; Open Graph basics.
  3. Migration  — substantive content from every original page is present
                  in the generated output (coverage strings).
  4. Links      — internal links, images, scripts, and fragment anchors
                  resolve to generated files; no references to excluded
                  source directories (migration archive, docs, scripts).
  5. Security   — the CSP meta tag contains the sha256 hash of the page's
                  inline JSON-LD (guards against breaking the policy by
                  editing the structured-data block).
  6. Hygiene    — no placeholder text, no accidental TODOs, system files
                  (robots.txt, sitemap.xml, CNAME, 404.html) present.
  7. Redirects  — legacy URLs redirect with canonical links.

Exit code 0 means all checks passed.
"""

import base64
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SITE_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
SITE_URL = "https://mcyorkrite.com"

REQUIRED_PAGES = [
    "index.html",
    "about/index.html",
    "about/chapter/index.html",
    "about/council/index.html",
    "about/commandery/index.html",
    "about/degrees/index.html",
    "about/degrees/mark-master-mason/index.html",
    "about/degrees/past-master/index.html",
    "about/degrees/most-excellent-master/index.html",
    "about/degrees/royal-arch-mason/index.html",
    "about/degrees/royal-master/index.html",
    "about/degrees/select-master/index.html",
    "about/degrees/super-excellent-master/index.html",
    "about/degrees/illustrious-order-of-the-red-cross/index.html",
    "about/degrees/order-of-st-paul/index.html",
    "about/degrees/order-of-malta/index.html",
    "about/degrees/order-of-the-temple/index.html",
    "events/index.html",
    "contact/index.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "CNAME",
]

REDIRECT_PAGES = {
    "history/index.html": "/about/",
    "pages/index.html": "/",
}

# Substantive content that must survive migration. Each tuple is
# (page, list of phrases from the original site).
MIGRATION_COVERAGE = {
    "index.html": [
        "collection of appendant bodies",
        "Master Mason in good standing",
        "don\u2019t hesitate to contact us",
    ],
    "about/index.html": [
        "operate independently of each other",
        "Chapter of Royal Arch Masons",
        "Council of Cryptic Masons",
        "Commandery of Knights Templar",
        "first part of the York Rite",
        "second part of the York Rite",
        "final order joined in the York Rite",
    ],
    "about/chapter/index.html": [
        "first part of the York Rite system of Masonic degrees",
        "Mark Master Mason",
        "Past Master",
        "Most Excellent Master",
        "Royal Arch Mason",
        "Grand Chapter of the Northern States",
        "General Grand Chapter, Royal Arch Masons International",
        "10 November 2004",
        "pure, antient Masonry",
    ],
    "about/council/index.html": [
        "second part of the York Rite system of Masonic degrees",
        "Hiramic Legend",
        "Second Temple Legend",
        "Council of Royal & Select Masters",
    ],
    "about/commandery/index.html": [
        "final order joined in the York Rite",
        "protect and defend the Christian faith",
        "Grand Encampment of the United States",
        "The Illustrious Order of the Red Cross",
        "Order of St. Paul",
        "Order of the Knights of Malta",
        "The Order of the Temple",
        "state level Grand Commandery",
    ],
    "events/index.html": [
        "calendar.google.com/calendar",
        "606ca60259602d624c2334646cedc5b31f1272bf88aa9dbcdbe70d9416de858e",
        "America/New_York",
        "Second Wednesday",
        "Fourth Wednesday",
    ],
    "contact/index.html": [
        "website-contact@mcyorkrite.com",
        "Pentalpha Masonic Temple",
        "20516 Boland Farm Road",
        "Germantown",
        "20876",
        "Observation Drive",
        "I-270 at Exit 15 (Maryland 118)",
        "Second Wednesday",
        "7:30 p.m.",
        "google.com/maps",
    ],
    "about/degrees/index.html": [
        "Mark Master Mason",
        "Royal Master",
        "Select Master",
        "The Order of the Temple",
    ],
    "about/degrees/mark-master-mason/index.html": [
        "operative masons",
        "eighteenth century",
    ],
    "about/degrees/past-master/index.html": [
        "Virtual Past Master",
    ],
    "about/degrees/most-excellent-master/index.html": [
        "completion of King Solomon",
    ],
    "about/degrees/royal-arch-mason/index.html": [
        "pure, antient Masonry",
        "10 November 2004",
    ],
    "about/degrees/royal-master/index.html": [
        "early nineteenth century",
    ],
    "about/degrees/select-master/index.html": [
        "Councils of Royal and Select Masters",
    ],
    "about/degrees/super-excellent-master/index.html": [
        "honorary degree",
        "Babylon",
    ],
    "about/degrees/illustrious-order-of-the-red-cross/index.html": [
        "Zerubbabel",
        "Truth",
    ],
    "about/degrees/order-of-st-paul/index.html": [
        "Mediterranean Pass",
    ],
    "about/degrees/order-of-malta/index.html": [
        "Hospitaller",
        "Rhodes",
    ],
    "about/degrees/order-of-the-temple/index.html": [
        "1119",
        "Council of Vienne in 1312",
        "1826",
        "no proof to justify them",
    ],
    "404.html": ["Page not found"],
}

FORBIDDEN_STRINGS = [
    "lorem ipsum",
    "TODO:",
    "FIXME",
    "placeholder text",
    "migration-archive",
    "Free Consultation",  # leftover Hugo theme placeholder must not appear
    "Certified Accountants",
    "Tax Compliance",
]

FORBIDDEN_PATH_PARTS = ["migration-archive", "/docs/", "/scripts/", "staging"]

# Escaped block-level HTML in rendered output — the signature of Markdown
# text glued to raw HTML by Liquid whitespace-stripping (kramdown then
# escapes the tags and they become visible text on the page).
ESCAPED_TAG_PATTERN = re.compile(
    r"&lt;(?:h[1-6]|p|ol|ul|li|div|span|a|table|section|nav|article)\b"
)

# Markdown heading syntax stranded inside rendered paragraph text.
INLINE_HEADING_PATTERN = re.compile(r"[^\n#]#{1,6} [A-Z]")


class PageParser(HTMLParser):
    """Collects metadata, links, images, and inline JSON-LD from a page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.descriptions = []
        self.canonical = None
        self.og_tags = {}
        self.jsonld_blocks = []
        self._in_jsonld = False
        self._jsonld_buf = []
        self.csp = None
        self.links = []      # (href, text)
        self.images = []     # (src, alt_present)
        self.scripts = []
        self.iframes = []
        self.ids = set()
        self._text_parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "head"):
            self.skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            if a.get("name") == "description":
                self.descriptions.append(a.get("content", ""))
            if a.get("property"):
                self.og_tags[a["property"]] = a.get("content", "")
            if a.get("http-equiv", "").lower() == "content-security-policy":
                self.csp = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buf = []
        if tag == "a" and a.get("href") is not None:
            self.links.append((a["href"], ""))
        if tag == "img":
            self.images.append((a.get("src", ""), "alt" in a))
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if tag == "iframe":
            self.iframes.append((a.get("src", ""), a.get("title"), a.get("loading")))
        if a.get("id"):
            self.ids.add(a["id"])

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self.skip_depth = max(0, self.skip_depth - 1)
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld_blocks.append("".join(self._jsonld_buf))

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld:
            self._jsonld_buf.append(data)
        if self.skip_depth == 0:
            self._text_parts.append(data)

    @property
    def text(self):
        parts = (re.sub(r"\s+", " ", p) for p in self._text_parts)
        return " ".join(p.strip() for p in parts if p.strip())


def norm_url(url):
    """Strip fragment for file resolution; return (path, fragment)."""
    url = url.split("#", 1)
    return url[0], (url[1] if len(url) > 1 else None)


def resolve_internal(page_rel, url):
    """Resolve an internal URL to a file inside _site. Returns Path or None."""
    if url.startswith("http"):
        return None  # external
    if url.startswith(("mailto:", "tel:")):
        return None
    path, _ = norm_url(url)
    if path.startswith("//"):
        return None
    path = path.split("?", 1)[0]
    if path.startswith("/"):
        rel = path.lstrip("/")
    else:
        rel = str(
            (SITE_ROOT / page_rel.parent / path)
            .resolve()
            .relative_to(SITE_ROOT.resolve())
        )
    if rel == "":
        rel = "index.html"
    candidates = [
        SITE_ROOT / rel,
        SITE_ROOT / rel / "index.html",
        SITE_ROOT / (rel + ".html"),
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def main():
    errors = []
    warnings = []

    for required in REQUIRED_PAGES:
        if not (SITE_ROOT / required).is_file():
            errors.append(f"missing required file: {required}")

    html_pages = sorted(
        (p.relative_to(SITE_ROOT) for p in SITE_ROOT.rglob("*.html")),
        key=str,
    )
    parsed = {}
    titles = {}
    descriptions = {}

    for rel in html_pages:
        path = SITE_ROOT / rel
        raw = path.read_text(encoding="utf-8")
        parser = PageParser()
        try:
            parser.feed(raw)
        except Exception as exc:  # malformed HTML
            errors.append(f"{rel}: HTML parse error: {exc}")
            continue
        parsed[rel] = parser

        page_url = "/" + str(rel).replace("index.html", "")

        # -- Redirect pages -------------------------------------------------
        if str(rel) in REDIRECT_PAGES:
            target = REDIRECT_PAGES[str(rel)]
            if f"url={SITE_URL}{target}" not in raw:
                errors.append(f"{rel}: missing meta refresh to {target}")
            if f'<link rel="canonical" href="{SITE_URL}{target}">' not in raw:
                errors.append(f"{rel}: missing canonical to {target}")
            continue

        # -- Titles and descriptions ----------------------------------------
        title = parser.title.strip()
        if not title:
            errors.append(f"{rel}: missing <title>")
        elif title in titles:
            errors.append(f"{rel}: duplicate page title: {title!r}")
        titles[title] = rel

        if not parser.descriptions or not parser.descriptions[0].strip():
            errors.append(f"{rel}: missing meta description")
        else:
            desc = parser.descriptions[0].strip()
            if desc in descriptions:
                errors.append(f"{rel}: duplicate meta description")
            descriptions[desc] = rel
            if len(desc) > 320:
                warnings.append(f"{rel}: meta description is long ({len(desc)} chars)")

        # -- Canonical and Open Graph ----------------------------------------
        if not parser.canonical:
            errors.append(f"{rel}: missing canonical link")
        else:
            expected = SITE_URL + page_url
            if parser.canonical != expected:
                errors.append(f"{rel}: canonical {parser.canonical} != expected {expected}")

        for prop in ("og:title", "og:description", "og:url", "og:type", "og:image"):
            if not parser.og_tags.get(prop):
                errors.append(f"{rel}: missing {prop}")

        # -- CSP / JSON-LD hash ----------------------------------------------
        if parser.csp and parser.jsonld_blocks:
            block = parser.jsonld_blocks[0]
            digest = base64.b64encode(
                hashlib.sha256(block.encode("utf-8")).digest()
            ).decode()
            if f"'sha256-{digest}'" not in parser.csp:
                errors.append(
                    f"{rel}: CSP meta tag does not contain the sha256 hash of "
                    "its JSON-LD block; regenerate the hash after editing "
                    "_includes/seo-jsonld.html"
                )

        # -- Images ------------------------------------------------------------
        for src, has_alt in parser.images:
            if not has_alt:
                errors.append(f"{rel}: image without alt attribute: {src}")
            if src.startswith("/"):
                if not (SITE_ROOT / src.lstrip("/")).is_file():
                    errors.append(f"{rel}: missing image file: {src}")

        # -- Scripts, iframes ---------------------------------------------------
        for src in parser.scripts:
            if src.startswith("/"):
                if not (SITE_ROOT / src.lstrip("/")).is_file():
                    errors.append(f"{rel}: missing script file: {src}")

        for src, title_attr, loading in parser.iframes:
            if not title_attr:
                errors.append(f"{rel}: iframe without title attribute: {src}")
            if loading != "lazy":
                warnings.append(f"{rel}: iframe not lazy-loaded: {src}")

        # -- Internal links ------------------------------------------------------
        for href, _text in parser.links:
            if href.startswith(("mailto:", "tel:")):
                continue
            path_part, frag = norm_url(href)
            if path_part.startswith(("http://", "https://", "//")):
                continue  # external links checked separately
            target = resolve_internal(rel, href)
            if target is None:
                errors.append(f"{rel}: broken internal link: {href}")
                continue
            if frag:
                target_html = target.read_text(encoding="utf-8")
                frag_parser = PageParser()
                frag_parser.feed(target_html)
                if frag not in frag_parser.ids:
                    errors.append(f"{rel}: missing anchor #{frag} in {href}")

        # -- Hygiene --------------------------------------------------------------
        low = parser.text.lower()
        for phrase in FORBIDDEN_STRINGS:
            if phrase.lower() in low:
                errors.append(f"{rel}: forbidden placeholder string: {phrase!r}")
        for part in FORBIDDEN_PATH_PARTS:
            if part in raw:
                errors.append(f"{rel}: references excluded source path: {part}")
        if ESCAPED_TAG_PATTERN.search(raw):
            errors.append(
                f"{rel}: escaped HTML tags visible in output — a Liquid tag in "
                "the Markdown source is stripping the blank lines that separate "
                "text from raw HTML blocks"
            )
        if INLINE_HEADING_PATTERN.search(parser.text):
            errors.append(
                f"{rel}: Markdown heading syntax leaked into rendered text — "
                "a Liquid block is gluing a heading to the preceding paragraph"
            )

        # -- Migration coverage -----------------------------------------------------
        phrases = MIGRATION_COVERAGE.get(str(rel), [])
        for phrase in phrases:
            if phrase not in parser.text and phrase not in raw:
                errors.append(f"{rel}: migration coverage missing: {phrase!r}")

    # -- System files ----------------------------------------------------------
    cname = (SITE_ROOT / "CNAME").read_text(encoding="utf-8").strip() if (SITE_ROOT / "CNAME").is_file() else ""
    if cname != "mcyorkrite.com":
        errors.append(f"CNAME is {cname!r}, expected 'mcyorkrite.com'")

    robots = (SITE_ROOT / "robots.txt").read_text(encoding="utf-8") if (SITE_ROOT / "robots.txt").is_file() else ""
    if SITE_URL + "/sitemap.xml" not in robots:
        errors.append("robots.txt does not reference the sitemap")

    sitemap = (SITE_ROOT / "sitemap.xml").read_text(encoding="utf-8") if (SITE_ROOT / "sitemap.xml").is_file() else ""
    for url in ["/", "/about/", "/about/chapter/", "/about/council/", "/about/commandery/", "/events/", "/contact/"]:
        if f"<loc>{SITE_URL}{url}</loc>" not in sitemap:
            errors.append(f"sitemap.xml missing {url}")

    # -- Excluded directories must not leak into _site --------------------------
    for part in ("migration-archive", "docs", "scripts", "tests", "staging"):
        if (SITE_ROOT / part).exists():
            errors.append(f"excluded directory leaked into _site: {part}/")

    # -- Report ------------------------------------------------------------------
    print(f"Validating {SITE_ROOT} — {len(html_pages)} HTML pages")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  ⚠ {w}")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        print("\nFAIL")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
