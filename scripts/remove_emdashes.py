#!/usr/bin/env python3
"""Replace every em-dash in shipped site content with natural punctuation.

Each replacement is exact-match and asserted to fire exactly once, so a
typo in a pattern fails loudly instead of silently leaving dashes behind.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# file -> list of (before, after)
REPLACEMENTS = {
    "index.md": [
        ("# Homepage — Montgomery County York Rite",
         "# Homepage: Montgomery County York Rite"),
        ('seo_title: "York Rite — Montgomery County, Maryland"',
         'seo_title: "York Rite of Montgomery County, Maryland"'),
        ("Maryland — a Chapter of Royal Arch Masons, a Council of Cryptic Masons, and a Commandery of Knights Templar — meeting at",
         "Maryland: a Chapter of Royal Arch Masons, a Council of Cryptic Masons, and a Commandery of Knights Templar, meeting at"),
        ("bodies — a <strong>Chapter of Royal Arch Masons</strong>, a",
         "bodies: a <strong>Chapter of Royal Arch Masons</strong>, a"),
        ("<strong>Commandery of Knights Templar</strong> — each with its own",
         "<strong>Commandery of Knights Templar</strong>, each with its own"),
        ("Temple, its destruction, and its rebuilding — and on the traditions of",
         "Temple, its destruction, and its rebuilding, and on the traditions of"),
        ('<span class="visually-hidden"> — see the contact page</span>',
         '<span class="visually-hidden">: see the contact page</span>'),
        ('<span class="visually-hidden"> — on the About page</span>',
         '<span class="visually-hidden">: on the About page</span>'),
    ],
    "about/index.md": [
        ("# About the York Rite — Montgomery County",
         "# About the York Rite: Montgomery County"),
        ("family — three appendant bodies, one continuing Masonic story.",
         "family: three appendant bodies, one continuing Masonic story."),
        ('>Learn more<span class="visually-hidden"> — about {{ body.name }}</span>',
         '>Learn more<span class="visually-hidden">: about {{ body.name }}</span>'),
    ],
    "about/council.md": [
        ("adds an honorary degree as well — each with its own history:",
         "adds an honorary degree as well, each with its own history:"),
    ],
    "about/commandery.md": [
        ("Maryland — the final order joined in the York Rite, conferring",
         "Maryland, the final order joined in the York Rite, conferring"),
    ],
    "contact/index.md": [
        ("Germantown, Maryland — second and fourth Wednesdays at 7:30 p.m.",
         "Germantown, Maryland, on the second and fourth Wednesdays at 7:30 p.m."),
        ("There is no public telephone listing — please email us and we will respond",
         "There is no public telephone listing, so please email us and we will respond"),
    ],
    "events/index.md": [
        ("York Rite bodies — Royal Arch Chapter, Cryptic Council, and Knights Templar Commandery — at Pentalpha Lodge #194",
         "York Rite bodies (Royal Arch Chapter, Cryptic Council, and Knights Templar Commandery) at Pentalpha Lodge #194"),
    ],
    "_data/bodies.yml": [
        ("Emblem of the Chapter of Royal Arch Masons — a triple tau within a triangle and circle",
         "Emblem of the Chapter of Royal Arch Masons: a triple tau within a triangle and circle"),
        ("Emblem of the Council of Cryptic Masons — a triangle, trowel, and sword",
         "Emblem of the Council of Cryptic Masons: a triangle, trowel, and sword"),
        ("Emblem of the Knights Templar — a cross and crown with the motto In Hoc Signo Vinces",
         "Emblem of the Knights Templar: a cross and crown with the motto In Hoc Signo Vinces"),
    ],
    "about/degrees/index.md": [
        ("them carries a story — drawn from the building of Solomon&rsquo;s Temple, its",
         "them carries a story drawn from the building of Solomon&rsquo;s Temple, its"),
        ("tradition rather than documented fact — where scholars differ, the pages",
         "tradition rather than documented fact; where scholars differ, the pages"),
    ],
    "about/degrees/mark-master-mason.md": [
        ("operative masons chiseled personal marks into the stones they dressed —",
         "operative masons chiseled personal marks into the stones they dressed,"),
    ],
    "about/degrees/most-excellent-master.md": [
        ("literature of the period — the era of Thomas Smith",
         "literature of the period, the era of Thomas Smith"),
        ("Webb's widely used Masonic monitors — and from there spread through the",
         "Webb's widely used Masonic monitors, and from there spread through the"),
        ("narrative need within the York Rite — it marks the",
         "narrative need within the York Rite: it marks the"),
    ],
    "about/degrees/order-of-malta.md": [
        ("heritage of service — from Jerusalem to Rhodes to Malta.",
         "heritage of service, from Jerusalem to Rhodes to Malta."),
        ("Hospitaller knights — the Order of St. John — whose centuries of care",
         "Hospitaller knights, the Order of St. John, whose centuries of care"),
        ("to the Hospitallers — an",
         "to the Hospitallers, an"),
        ("service — hospitality, mercy, and the",
         "service: hospitality, mercy, and the"),
        ("defense of the faith — drawing on the witness",
         "defense of the faith, drawing on the witness"),
    ],
    "about/degrees/order-of-st-paul.md": [
        ("Also called the Mediterranean Pass — a passing order on the sea-road to Malta.",
         "Also called the Mediterranean Pass: a passing order on the sea-road to Malta."),
        ("The Passing Order of St. Paul — historically also known as the",
         "The Passing Order of St. Paul, historically also known as the"),
        ("Mediterranean Pass — is a *passing* order:",
         "Mediterranean Pass, is a *passing* order:"),
        ("sea-road of the Mediterranean — the",
         "sea-road of the Mediterranean, the"),
        ("The Mediterranean Pass — under the invocation of St. Paul,",
         "The Mediterranean Pass, under the invocation of St. Paul,"),
        ("whose voyages across that same sea the Book of Acts records — served",
         "whose voyages across that same sea the Book of Acts records, served"),
    ],
    "about/degrees/order-of-the-temple.md": [
        ("The crowning order of the York Rite — Christian knighthood in commemoration",
         "The crowning order of the York Rite: Christian knighthood in commemoration"),
        ("medieval Poor Fellow-Soldiers of Christ and of the Temple of Solomon —",
         "medieval Poor Fellow-Soldiers of Christ and of the Temple of Solomon,"),
        ("the Knights Templar — and its ceremony brings",
         "the Knights Templar, and its ceremony brings"),
        ("property to the Hospitallers — the Knights of St. John, whose",
         "property to the Hospitallers, the Knights of St. John, whose"),
        ("that Freemasonry was founded by the Templars — or that fugitive",
         "that Freemasonry was founded by the Templars, or that fugitive"),
        ("Templars took refuge within it — are acknowledged as theories, with no",
         "Templars took refuge within it, are acknowledged as theories, with no"),
    ],
    "about/degrees/past-master.md": [
        ("A degree born of an old constitutional requirement — that only a Master who had presided could be exalted.",
         "A degree born of an old constitutional requirement: that only a Master who had presided could be exalted."),
        ("actually presided over a lodge — an installed Master — was considered",
         "actually presided over a lodge, an installed Master, was considered"),
        ("after the Grand Chapter's 2004 decisions — described on the",
         "after the Grand Chapter's 2004 decisions (described on the"),
        ("[Chapter page](/about/chapter/) — no installed or presiding requirement",
         "[Chapter page](/about/chapter/)), no installed or presiding requirement"),
        ("concern the duties and responsibilities of the chair — presiding,",
         "concern the duties and responsibilities of the chair (presiding,"),
        ("teaching, and serving — which is why it has kept its place rather than",
         "teaching, and serving), which is why it has kept its place rather than"),
    ],
    "about/degrees/royal-arch-mason.md": [
        ("lede: \"The completion of 'pure, antient Masonry' — the recovery of what was lost at the building of the Temple.\"",
         "lede: \"The completion of 'pure, antient Masonry': the recovery of what was lost at the building of the Temple.\""),
        ("foundation of a second — and in clearing the ground, discover what the",
         "foundation of a second, and in clearing the ground, discover what the"),
        ("the same decade — which is one reason the whole system of allied degrees",
         "the same decade, which is one reason the whole system of allied degrees"),
        ("General Grand Chapter — a history told on the",
         "General Grand Chapter, a history told on the"),
        ("consists of the three Craft degrees and the Royal Arch — a statement",
         "consists of the three Craft degrees and the Royal Arch, a statement"),
    ],
    "about/degrees/royal-master.md": [
        ("Conversations at the building of the Temple — the Cryptic story begins before its loss.",
         "Conversations at the building of the Temple: the Cryptic story begins before its loss."),
        ("degrees narrate only after the fact — making plain why what will be",
         "degrees narrate only after the fact, making plain why what will be"),
        ("body — one organized around the Temple's secrets and their safekeeping.",
         "body, one organized around the Temple's secrets and their safekeeping."),
    ],
    "about/degrees/select-master.md": [
        ("is the crypt — the secret vault constructed beneath the Temple — where",
         "is the crypt, the secret vault constructed beneath the Temple, where"),
        ("Traditions of \"Select Masters\" — small, carefully chosen",
         "Traditions of \"Select Masters\" (small, carefully chosen"),
        ("groups concerned with the Temple's secrets — were at work among American",
         "groups concerned with the Temple's secrets) were at work among American"),
        ("the Grand Chapters — part of the same general organization of the York",
         "the Grand Chapters, part of the same general organization of the York"),
        ("preserved against loss, and recovered by another — binding the whole",
         "preserved against loss, and recovered by another, binding the whole"),
    ],
    "about/degrees/super-excellent-master.md": [
        ("An honorary degree of the Council — the fall of Jerusalem and the sorrow of the captivity.",
         "An honorary degree of the Council: the fall of Jerusalem and the sorrow of the captivity."),
        ("Super Excellent Master is an honorary degree — it is not one of the two",
         "Super Excellent Master is an honorary degree; it is not one of the two"),
        ("arc of the Temple story — building, completion, destruction, captivity,",
         "arc of the Temple story: building, completion, destruction, captivity,"),
        ("Judahite exile — the destruction of the city and Temple and the",
         "Judahite exile, the destruction of the city and Temple and the"),
    ],
    "about/degrees/illustrious-order-of-the-red-cross.md": [
        ("Zerubbabel's plea before the court of Darius — an order of truth that completes the Temple story.",
         "Zerubbabel's plea before the court of Darius: an order of truth that completes the Temple story."),
        ("the appeal of Zerubbabel — the prince who led",
         "the appeal of Zerubbabel, the prince who led"),
        ("the return from the Babylonian captivity — for the rebuilding of the",
         "the return from the Babylonian captivity, for the rebuilding of the"),
        ("nineteenth century — the period that produced the Grand Encampment of",
         "nineteenth century, the period that produced the Grand Encampment of"),
        ("the United States — the Red Cross had taken its fixed place as the",
         "the United States, the Red Cross had taken its fixed place as the"),
    ],
    "_includes/footer.html": [
        ("The York Rite Bodies of Montgomery County, Maryland — a Chapter of",
         "The York Rite Bodies of Montgomery County, Maryland: a Chapter of"),
        ('aria-label="Footer — the three bodies"',
         'aria-label="Footer: the three bodies"'),
        ('aria-label="Footer — site links"',
         'aria-label="Footer: site links"'),
        ('aria-label="Footer — contact information"',
         'aria-label="Footer: contact information"'),
    ],
    "_includes/header.html": [
        ('aria-label="{{ site.title }} — home"',
         'aria-label="{{ site.title }}, home"'),
    ],
    "_includes/seo.html": [
        ("Montgomery County York Rite — Royal Arch, Cryptic Masonry, and Knights Templar",
         "Montgomery County York Rite: Royal Arch, Cryptic Masonry, and Knights Templar"),
    ],
    "_includes/body-card.html": [
        ('<span class="visually-hidden"> — read more about {{ include.body.name }}</span>',
         '<span class="visually-hidden">: read more about {{ include.body.name }}</span>'),
    ],
    "_layouts/body.html": [
        ('<span class="visually-hidden"> — {{ other.name }}</span>',
         '<span class="visually-hidden">: {{ other.name }}</span>'),
    ],
    "_layouts/redirect.html": [
        ("<title>{{ page.title }} — {{ site.title }}</title>",
         "<title>{{ page.title }} · {{ site.title }}</title>"),
    ],
    "assets/js/main.js": [
        ("Montgomery County York Rite — site behaviour",
         "Montgomery County York Rite: site behaviour"),
        ('"Copy failed — please select the address manually."',
         '"Copy failed. Please select the address manually."'),
    ],
    "_config.yml": [
        ("# Site configuration — Montgomery County York Rite",
         "# Site configuration: Montgomery County York Rite"),
        ("Maryland — a Chapter of Royal",
         "Maryland: a Chapter of Royal"),
        ("Templar — meeting at Pentalpha Lodge #194",
         "Templar, meeting at Pentalpha Lodge #194"),
    ],
    "_includes/seo-jsonld.html": [
        ("This block is intentionally static — it must",
         "This block is intentionally static; it must"),
        ("No ratings, reviews, or event claims — only verified organization details.",
         "No ratings, reviews, or event claims. Only verified organization details."),
    ],
    "_includes/navigation.html": [
        ('Parameter: variant — "desktop" | "mobile" | "footer".',
         'Parameter "variant": "desktop", "mobile", or "footer".'),
    ],
    "_includes/meeting-info.html": [
        ('Parameter: show_map — "true" renders the preserved Google Maps embed.',
         'Parameter "show_map": "true" renders the preserved Google Maps embed.'),
    ],
    "_includes/contact-actions.html": [
        ('Parameter: show_copy — "true" enables the copy-address button.',
         'Parameter "show_copy": "true" enables the copy-address button.'),
    ],
    "pages/index.html": [
        ("# Legacy URL /pages/ — the original page was an empty theme index",
         "# Legacy URL /pages/: the original page was an empty theme index"),
    ],
    "history/index.html": [
        ("# Legacy URL /history/ — the original page contained only unedited placeholder",
         "# Legacy URL /history/: the original page contained only unedited placeholder"),
    ],
}

# Degree page heading comments: "# Name — degree/order history" -> "# Name: ..."
# (optional pair: each degree page has only one of the two variants;
#  index.md has neither and is skipped)
for p in sorted((ROOT / "about/degrees").glob("*.md")):
    if p.name == "index.md":
        continue
    rel = str(p.relative_to(ROOT))
    text = p.read_text(encoding="utf-8")
    for before, after in ((" — order history", ": order history"),
                          (" — degree history", ": degree history")):
        if before in text:
            text = text.replace(before, after, 1)
            applied += 1
            p.write_text(text, encoding="utf-8")
            break

applied, failed = 0, []
for rel, pairs in REPLACEMENTS.items():
    path = ROOT / rel
    if not path.exists():
        failed.append(f"MISSING FILE: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for before, after in pairs:
        n = text.count(before)
        if n == 0:
            if after in text:
                continue  # already applied on a previous run
            failed.append(f"NO MATCH [{rel}]: {before[:60]}...")
            continue
        if n > 1:
            failed.append(f"MULTI MATCH x{n} [{rel}]: {before[:60]}...")
            continue
        text = text.replace(before, after)
        applied += 1
    path.write_text(text, encoding="utf-8")

print(f"Applied {applied} replacements across {len(REPLACEMENTS)} files")
if failed:
    print("FAILURES:")
    for f in failed:
        print(" ", f)
    raise SystemExit(1)

# Final assertion: no em-dashes remain anywhere that ships
shipped = []
for pat in ("*.md", "*.yml", "*.html", "*.js", "*.json", "*.svg", "*.xml"):
    shipped.extend(ROOT.glob(pat))
    shipped.extend((ROOT / "about").rglob(pat))
    shipped.extend((ROOT / "contact").rglob(pat))
    shipped.extend((ROOT / "events").rglob(pat))
    shipped.extend((ROOT / "history").rglob(pat))
    shipped.extend((ROOT / "pages").rglob(pat))
    shipped.extend((ROOT / "_data").rglob(pat))
    shipped.extend((ROOT / "_includes").rglob(pat))
    shipped.extend((ROOT / "_layouts").rglob(pat))
    shipped.extend((ROOT / "assets").rglob(pat))
left = sorted({str(p.relative_to(ROOT)) for p in shipped
               if p.is_file() and "—" in p.read_text(encoding="utf-8",
                                                      errors="ignore")})
if left:
    print("EM-DASHES REMAIN in:", *left, sep="\n  ")
    raise SystemExit(1)
print("Verified: no em-dashes remain in any shipped source file")
