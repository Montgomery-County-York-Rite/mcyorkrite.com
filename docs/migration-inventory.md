# Migration Inventory

Complete inventory of pages discovered on the original production website
(https://mcyorkrite.com, a Hugo 0.68.3 site) and their treatment in the
rebuilt Jekyll site.

Discovery method: the site's own `sitemap.xml`, a per-page crawl of every
URL it listed, inspection of all internal hyperlinks in each page's HTML,
and a check of robots.txt (which returned the HTML homepage — the original
site publishes no robots directives). The crawl was performed politely (one
request per second) and covered all URLs the sitemap disclosed plus the 404
path.

## Page inventory

| # | Original URL | Discovered via | Substantive content? | Destination | Status |
|---|---|---|---|---|---|
| 1 | `/` | sitemap | Yes — welcome text, "What is the York Rite", "Find out More" | `/` | Migrated (`index.md`) |
| 2 | `/about/` | sitemap | Yes — three-body family overview with emblems | `/about/` | Migrated (`about/index.md`) |
| 3 | `/about/chapter/` | sitemap | Yes — full Royal Arch description + history | `/about/chapter/` | Migrated (`about/chapter.md`) |
| 4 | `/about/council/` | sitemap | Yes — full Cryptic Masonry description | `/about/council/` | Migrated (`about/council.md`) |
| 5 | `/about/commandery/` | sitemap | Yes — full Knights Templar description + orders | `/about/commandery/` | Migrated (`about/commandery.md`) |
| 6 | `/events/` | sitemap | Yes — embedded Google Calendar (`mdyorkrite@gmail.com`) | `/events/` | Migrated (`events/index.md`), embed reconfigured to the provided Calendar ID |
| 7 | `/contact/` | sitemap | Yes — email, address, directions, meeting hours, map | `/contact/` | Migrated (`contact/index.md`) |
| 8 | `/history/` | sitemap | **No** — contained only unedited Hugo-theme placeholder text from an accounting-firm demo ("Free Consultation", "Certified Accountants", "Tax Compliance") and unrelated stock SVG icons | `/history/` → redirect to `/about/` | Redirected; justification below |
| 9 | `/pages/` | sitemap | **No** — empty theme index page ("Pages", "About Heading") with no content | `/pages/` → redirect to `/` | Redirected; justification below |
| 10 | `/404/` | sitemap | System page (Hugo-generated 404) | `/404.html` | Replaced with a new 404 page |
| 11 | `/categories/`, `/tags/` | sitemap | System pages (empty Hugo taxonomy indexes, no content) | — | Not migrated; generated artifacts of the previous platform with zero content |
| 12 | `/favicon.png` | page metadata | Asset — generic Hugo-theme default "H" icon, **not** organization identity | — | Replaced with an original keystone mark (see asset-inventory) |

## Acceptance rule audit

"Every discovered original page must have a corresponding migrated page or an
explicitly justified redirect. No source page may disappear silently."

- Pages 1–7: migrated; see content-mapping.md for per-page text mapping.
- Page 8 (`/history/`): justified redirect. The page held no organizational
  content — reproducing it would have published accounting-firm demo copy, and
  inventing replacement history was prohibited by the project ground rules.
  Visitors following old links land on the About page, which carries the
  York Rite overview and links to each body.
- Page 9 (`/pages/`): justified redirect to the homepage (empty index).
- Pages 10–11: platform system artifacts, replaced or documented above.

## Content discovered beyond the known starting inventory

The preliminary inspection listed seven pages. The crawl additionally
discovered `/history/`, `/pages/`, `/404/`, `/categories/`, and `/tags/`
(rows 8–11), plus the assets recorded in asset-inventory.md. No other
public pages, PDFs, downloads, or embedded services were found: the only
third-party embeds on the original site were the Google Calendar (events)
and the Google Maps iframe (contact).
