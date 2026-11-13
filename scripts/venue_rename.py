#!/usr/bin/env python3
"""Venue rename (Pentalpha Masonic Temple), contact attribution, and copy
cleanup. Every replacement is exact-match and asserted."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

R = {
    "_data/organization.yml": [
        ('lodge: "Pentalpha Lodge #194"', 'lodge: "Pentalpha Masonic Temple"'),
        ("(Pentalpha Lodge #194)", "(Pentalpha Masonic Temple)"),
    ],
    "_includes/seo-jsonld.html": [
        ("meeting at Pentalpha Lodge #194 in Germantown, Maryland.",
         "meeting at Pentalpha Masonic Temple in Germantown, Maryland."),
        ('"name": "Pentalpha Lodge #194",', '"name": "Pentalpha Masonic Temple",'),
    ],
    "_includes/meeting-info.html": [
        ("Map showing Pentalpha Lodge #194, 20516 Boland Farm Road",
         "Map showing Pentalpha Masonic Temple, 20516 Boland Farm Road"),
    ],
    "_includes/footer.html": [
        ("""<address class="site-footer__address">
          {{ site.data.organization.meeting_location.lodge }}<br>""",
         """<address class="site-footer__address">
          {{ site.title }}<br>
          {{ site.data.organization.meeting_location.lodge }}<br>"""),
    ],
    "contact/index.md": [
        ("The bodies meet at Pentalpha Lodge #194, 20516 Boland Farm Road",
         "The bodies meet at Pentalpha Masonic Temple, 20516 Boland Farm Road"),
        ("{{ site.data.organization.meeting_location.lodge }}. The lodge is located at",
         "{{ site.data.organization.meeting_location.lodge }}. The temple is located at"),
    ],
    "index.md": [
        ("meeting at Pentalpha Lodge #194, Germantown.",
         "meeting at Pentalpha Masonic Temple, Germantown."),
        ("In Montgomery County, the three bodies meet together at Pentalpha\n        Lodge #194 in Germantown, sharing in ritual, fellowship, and support",
         "In Montgomery County, the three bodies meet together at Pentalpha\n        Masonic Temple in Germantown, sharing in ritual, fellowship, and support"),
        ("The Montgomery County York Rite is a collection of Appendant Bodies",
         "The Montgomery County York Rite is a collection of appendant bodies"),
        ("If you are a Master Mason in good standing from a regular Jurisdiction,",
         "If you are a Master Mason in good standing from a regular jurisdiction,"),
    ],
    "about/index.md": [
        ("The Montgomery County York Rite is a collection of Appendant Bodies that",
         "The Montgomery County York Rite is a collection of appendant bodies that"),
        ("If you are a Master Mason in good standing from a regular Jurisdiction, you",
         "If you are a Master Mason in good standing from a regular jurisdiction, you"),
        ("first part of the York Rite system of the Masonic degrees.",
         "first part of the York Rite system of Masonic degrees."),
    ],
    "events/index.md": [
        ("at Pentalpha Lodge #194, Germantown, Maryland.",
         "at Pentalpha Masonic Temple, Germantown, Maryland."),
    ],
    "about/chapter.md": [
        ("the York Rite system of the Masonic degrees, with four conferring degrees.",
         "the York Rite system of Masonic degrees, with four conferring degrees."),
        ("Royal Arch Masonry is the first part of the York Rite system of the Masonic\n",
         "Royal Arch Masonry is the first part of the York Rite system of Masonic\n"),
    ],
    "_data/bodies.yml": [
        ("Royal Arch Masonry is the first part of the York Rite system of the\n      Masonic degrees.",
         "Royal Arch Masonry is the first part of the York Rite system of\n      Masonic degrees."),
    ],
    "_config.yml": [
        ("meeting at Pentalpha Lodge #194 in Germantown, Maryland.",
         "meeting at Pentalpha Masonic Temple in Germantown, Maryland."),
    ],
    "README.md": [
        ("meeting at Pentalpha Lodge #194 in", "meeting at Pentalpha Masonic Temple in"),
    ],
    "scripts/generate_brand_assets.py": [
        ("Meeting at Pentalpha Lodge #194 · Germantown, Maryland",
         "Meeting at Pentalpha Masonic Temple · Germantown, Maryland"),
    ],
    "tests/validate_site.py": [
        ('"Pentalpha Lodge #194",', '"Pentalpha Masonic Temple",'),
        ('"collection of Appendant Bodies",', '"collection of appendant bodies",'),
        ('"first part of the York Rite system of the Masonic degrees",',
         '"first part of the York Rite system of Masonic degrees",'),
    ],
}

applied, failed = 0, []
for rel, pairs in R.items():
    p = ROOT / rel
    if not p.exists():
        failed.append(f"MISSING FILE {rel}")
        continue
    t = p.read_text(encoding="utf-8")
    for before, after in pairs:
        n = t.count(before)
        if n == 0 and after in t:
            continue  # idempotent
        if n != 1:
            failed.append(f"[{rel}] count={n}: {before[:60]!r}")
            continue
        t = t.replace(before, after)
        applied += 1
    p.write_text(t, encoding="utf-8")

print(f"Applied {applied} replacements")
if failed:
    print("FAILURES:")
    [print(" ", f) for f in failed]
    sys.exit(1)

# assert no stray old name remains in shipped sources
for pat in ("*.md", "*.yml", "*.html"):
    for f in list(ROOT.rglob(pat)):
        s = str(f)
        if any(x in s for x in ("migration-archive", "_site", "qa-tmp", "staging")):
            continue
        if "Pentalpha Lodge #194" in f.read_text(encoding="utf-8", errors="ignore"):
            print("OLD NAME REMAINS:", s)
            sys.exit(1)
print("Verified: no 'Pentalpha Lodge #194' remains in shipped sources")
