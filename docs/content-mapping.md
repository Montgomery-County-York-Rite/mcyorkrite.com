# Content Mapping

Per-page mapping from the original site's substantive content to the new
Jekyll source files, with the editorial treatment applied to each. The full
original HTML snapshots are preserved in `migration-archive/pages/`.

Editorial ground rules applied throughout:

- Original text is preserved verbatim unless an edit is listed below.
- Only obvious typographical/formatting problems were corrected.
- Meaning, terminology, and historical claims were never altered.
- Nothing new was invented (no dates, names, events, or claims).

---

## 1. `/` (homepage) → `index.md`

| Original element | Treatment |
|---|---|
| Heading "Welcome"; text "Welcome to the website of the York Rite of Montgomery County, Maryland." | Preserved as the hero: "Welcome to the York Rite of Montgomery County" with lede introducing the fellowship |
| Section "What is the York Rite": "The Montgomery County York Rite is a collection of Appendant Bodies that operate independently of each other. If you are a Master Mason in good standing from a regular Jurisdiction, you may be eligible to join." | Preserved in the "One Rite, three venerable bodies" section and in the site description; the eligibility sentence appears verbatim |
| Section "Find out More": "If you want to find out more about the York Rite and their associated appendant bodies, please don't hessitate to contact us." | Preserved in the "Get involved" band. **Editorial change:** corrected the typo "hessitate" → "hesitate" |
| "Contact Us" CTA | Preserved as hero secondary CTA and CTA band buttons |
| Footer: "© 2020 Montgomery County York Rite. Site maintained by Justin Weeks." (link to jmweeks.com) | Credit preserved in the new footer; copyright year now generated dynamically |

**Additions (structural, not factual):** a "Three Bodies" card section driven
by the body pages' own text, a "Tradition & Fellowship" section describing the
Rite's publicly documented background, and a meetings strip reusing the
contact page's verified schedule. No new facts were introduced.

## 2. `/about/` → `about/index.md`

| Original element | Treatment |
|---|---|
| Title "The Montgomery County York Rite Family" | Preserved as the page's framing; lede states "three appendant bodies, one continuing Masonic story" |
| Card: "Chapter of Royal Arch Masons — Royal Arch Masonry is the first part of the York Rite system of the Masonic degrees. Royal Arch Masons meet as a…" | Preserved (full sentence from the Chapter page) |
| Card: "Commandery - Knights Templars — The Knights Templar is the final order joined in the York Rite. Unlike the initial degrees conferred in a regular…" | Preserved (full text on the Commandery page). **Editorial change:** "Knights Templars" → "Knights Templar" (standard form used on the original Commandery page itself) |
| Card: "Council of Cryptic Masons — Cryptic Masonry is the second part of the York Rite system of Masonic degrees, and the last found within the Rite that…" | Preserved |
| Emblems chapter.png / council.png / commandery.gif | Preserved, see asset-inventory.md |

**Additions:** the "How the bodies relate" progression (Chapter → Council →
Commandery) uses only the ordering already stated on the original body pages
("first part", "second part", "final order"). Membership eligibility text is
carried from the original homepage.

## 3. `/about/chapter/` → `about/chapter.md`

All four paragraphs preserved verbatim: the intro, the four degrees (Mark
Master Mason, Past Master, Most Excellent Master, Royal Arch Mason), the 1776/1797
Hartford/Grand Chapter of the Northern States history, and the 10 November 2004
Grand Chapter of the Holy Royal Arch decision.

**Editorial change:** the original ran two sentences together with a missing
space ("…and the Royal Arch.Following this decision…"); corrected to a
paragraph break. No wording changed.

**Additions:** section headings ("Degrees of the Chapter", "Historical
background", "Continuing the journey") and cross-links to the Council and
Commandery pages; CTA band with contact link.

## 4. `/about/council/` → `about/council.md`

Both paragraphs preserved verbatim, including the Hiramic Legend and Second
Temple Legend references and the "Council of Royal & Select Masters or
Council of Cryptic Masons depending on the jurisdiction" sentence.

**Additions:** section headings, a short "Within the Rite" paragraph linking
to the Chapter and Commandery pages, CTA band. The CTA text ("If you are a
Royal Arch Mason…") restates the membership dependency already published on
the Commandery page (membership open to Masons who have completed their
Royal Arch degrees).

## 5. `/about/commandery/` → `about/commandery.md`

All original text preserved verbatim: the Christian-faith membership
requirement, the "modeled on the historical Knights Templar" paragraph with
the Grand Encampment's statement on disputed origin theories, the
Commandery/Grand Commandery/Grand Encampment structure paragraph, and the
orders list (Illustrious Order of the Red Cross; Passing Order of St. Paul
(Mediterranean Pass); Order of the Knights of Malta; Order of the Temple).

**Editorial change:** the two paragraphs of the original first section were
grouped under added headings ("Membership", "A living memorial",
"Organization and orders") for readability; the disputed-origin theories
remain clearly attributed to the Grand Encampment's acknowledgment, as in
the original.

## 6. `/events/` → `events/index.md`

| Original element | Treatment |
|---|---|
| Google Calendar embed: `https://calendar.google.com/calendar/embed?src=mdyorkrite%40gmail.com&ctz=America/New_York&color=%23D50000&showCalendars=1&showTabs=1&showTitle=0` | Preserved parameter-for-parameter except `src`, which now uses the Calendar ID supplied by the organization: `606ca60259602d624c2334646cedc5b31f1272bf88aa9dbcdbe70d9416de858e@group.calendar.google.com` |
| — | **Additions:** a plain-text fallback link (always visible and inside `<noscript>`), timezone note, lazy-loaded iframe, and a stated-meetings section reusing the contact schedule |

The new calendar ID was verified live during QA: the embed renders real
public events (e.g. a Commandery meeting on 11 November and a Chapter
meeting on 25 November), confirming public display permission.

## 7. `/contact/` → `contact/index.md`

| Original element | Treatment |
|---|---|
| "The Montgomery County York Rite bodies meet at Pentalpha Lodge #194. This lodge is located at 20516 Boland Farm Road, next to the medical center on the corner of Boland Farm Road and Observation Drive. Just East of I-270 at Exit 15 (Maryland 118)" | Preserved verbatim under "Where we meet" |
| "Phone: Please e-mail" | Preserved as "There is no public telephone listing — please email us…" |
| Email (Cloudflare-obfuscated link, decoded during migration) | Decoded to `website-contact@mcyorkrite.com`; now a plain clickable `mailto:` link |
| Address: "20516 Boland Farm Rd, Germantown, MD 20876" | Preserved, with a copy-to-clipboard button and a Google Maps directions link |
| Meeting hours table: Second Wednesday 7:30pm; Fourth Wednesday 7:30pm | Preserved verbatim (times normalized typographically to "7:30 p.m.") |
| Google Maps embed (Pentalpha Lodge #194) | Preserved with identical embed URL; added `title`, `loading="lazy"`, responsive frame |

## 8. `/history/` → `history/index.html`

Justified redirect to `/about/`. Original page contained only Hugo-theme
placeholder text (accounting services: "Free Consultation", "Certified
Accountants", "Tax Compliance") and three stock `noun_*.svg` icons. Nothing
organizational was lost — there was no organizational content to lose. No
replacement history was invented, per project ground rules.

## 9. `/pages/` → `pages/index.html`

Justified redirect to `/`. Original page was an empty theme index
("Pages", "About Heading").

## Site-wide elements

| Original | Treatment |
|---|---|
| Navigation: Home, Events, About, Contact | Same four destinations, plus About-page sub-navigation to the three bodies |
| Footer credit "Site maintained by Justin Weeks" (jmweeks.com) | Preserved verbatim. Note: jmweeks.com did not respond during QA (DNS failure) — retained as on the original site |
| Footer copyright © 2020 | © year generated at build time |

## Summary of all editorial changes

1. "hessitate" → "hesitate" (typo).
2. "Knights Templars" → "Knights Templar" (house consistency; the original
   site itself used "Knights Templar" on the Commandery page).
3. Missing space/paragraph break between "…the Royal Arch." and "Following
   this decision…" on the Chapter page.
4. "7:30pm" → "7:30 p.m." (typographic normalization; same time).
5. "Just East of I-270" → sentence-case "just east of I-270" within running
   prose (the all-caps "East" was a formatting quirk of the original).
6. Calendar `src` switched from the Gmail address to the Calendar ID
   provided by the organization (explicitly instructed).
