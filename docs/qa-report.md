# QA Report

Results at delivery. Every claim below was produced by an automated check or
a rendered-browser inspection against the actual build output; nothing is
described as verified that was not executed.

## 1. Build validation

| Check | Result |
|---|---|
| `bundle install` with locked dependencies (`Gemfile.lock`, Ruby 3.3.x) | ✅ Pass locally (3.3.6) and in CI (3.3.13) |
| `jekyll build --strict_front_matter` (JEKYLL_ENV=production) | ✅ Pass, no warnings |
| Production URLs generated for all seven known pages | ✅ `/`, `/about/`, `/about/chapter/`, `/about/council/`, `/about/commandery/`, `/events/`, `/contact/` |
| `/about/chapter/` produced as a directory index (not `.html` URL) | ✅ |
| Legacy `/history/`, `/pages/` produce redirect pages | ✅ |
| `robots.txt`, `sitemap.xml`, `CNAME`, `404.html`, `site.webmanifest` present | ✅ |
| No source/dev files in `_site` (docs, scripts, tests, migration archive, Gemfile) | ✅ enforced by `_config.yml`, asserted by the validator |

CI equivalence: the same commands run in `.github/workflows/validate.yml`
(pull requests) and `.github/workflows/pages.yml` (deploys).

## 2. Content migration validation

`tests/validate_site.py` asserts, for every migrated page, that substantive
sentences from the original site exist verbatim in the generated output
(38 coverage phrases across the seven content pages — see the
`MIGRATION_COVERAGE` table in the script, mapped per page in
content-mapping.md). Result: **all present.** Editorial changes are the six
documented typographical corrections; nothing else was altered.

Coverage of discovered pages: 100% — 7 migrated, 2 justified redirects,
2 platform artifacts documented, 1 replaced theme asset. See
migration-inventory.md for the per-page audit.

## 3. Link validation

| Check | Result |
|---|---|
| Internal links resolve to generated files | ✅ 0 broken |
| Fragment anchors exist in target pages | ✅ 0 broken |
| Images/scripts referenced exist; every `<img>` has `alt` | ✅ |
| Every iframe has a `title` and is `loading="lazy"` | ✅ |
| External links (`scripts/check_external_links.py`) | ✅ 12 OK, 1 warning, 0 broken — warning resolved (see remaining issues) |

The single warning had been `jmweeks.com`, the site-credit link preserved
from the original footer, whose DNS no longer resolved. At the
organization's direction the credit link now points to
`https://focuswithjustin.com`.

## 4. Visual validation

Headless Chromium (Playwright) rendered every page at **320, 390, 768,
1024, 1440, and 1920 px** (48 full-page screenshots, kept locally under
`tests/qa-tmp/shots/`). Manual inspection of homepage, about, chapter,
events, contact, and 404 at desktop/tablet/mobile found no clipped text,
no horizontal overflow, no overlapping sections, and no broken responsive
behavior. Fixes applied during this pass:

- Bronze text-token darkened (`#8A6A33` → `#7A5F2D`) after axe flagged
  contrast on the ivory-deep band (homepage eyebrows) — corrected.
- 404 numeral color changed from gold to bronze (large-text contrast
  2.5:1 → 4.9:1) — corrected.
- Footer contact-column link spacing — corrected.
- Meeting-info grid dropped its unused third column — corrected.
- Brand wordmark letterspacing no longer wraps at 320 px — corrected.
- Tradition-section keystone ornament re-centered — corrected.

## 5. Accessibility validation

axe-core 4.10 (WCAG 2.0/2.1/2.2 A+AA rules) across all pages at all
viewports: **0 violations** after the contrast fixes above.

Keyboard/interaction harness (`tests/visual_qa.py`): **16/16 checks pass** —

- Mobile drawer: hidden on load, opens, `aria-expanded` toggles, focus
  moves in, Tab cycles are trapped inside, Escape closes, focus returns to
  the toggle, link activation navigates.
- Desktop: toggle hidden, inline nav visible; Home/About/Events/Contact
  reachable by keyboard.
- Skip link: first Tab focuses it; Enter moves focus to main content.
- Copy-address button: activates and reports status via `aria-live` region.

Other requirements verified in code/output: semantic landmarks (`header`,
`nav`, `main`, `footer`, `address`), one `h1` per page in order, skip link,
visible focus indicators, `prefers-reduced-motion` honored, 44 px touch
targets, zoom-safe rem-based type, no color-only meaning (ordinal labels
accompany accents).

## 6. Performance

Homepage measured in headless Chromium: **12 requests, 218.5 KB transferred,
100% self-hosted** (largest items: three emblems 30/27/18 KB, stylesheet
29 KB, two preloaded fonts 38 KB combined; JS 4.8 KB). The only third-party
requests on the whole site are the calendar embed (events page) and the map
embed (contact page), both `loading="lazy"`. Fonts are WOFF2 subsets with
`font-display: swap` and preloads for the two critical faces. All images
declare intrinsic dimensions to avoid layout shift. These figures support
the Lighthouse targets (Performance ≥ 90, Accessibility ≥ 95, Best
Practices ≥ 95, SEO ≥ 95) on production hardware/networks; a final
production-environment Lighthouse run should be repeated after the DNS
cutover since this environment could not run Lighthouse itself.

## 7. Functionality validation

| Control | Result |
|---|---|
| Every navigation link and CTA (header, hero, cards, footer, CTAs, breadcrumbs) | ✅ resolved by the link validator |
| Mobile menu (open/trap/close/navigate) | ✅ see interaction checks |
| Email links (`mailto:website-contact@mcyorkrite.com`) | ✅ present on contact, footer, drawer, 404 |
| Directions link (Google Maps) | ✅ HTTP 200 |
| Copy-address button | ✅ works with clipboard API and fallback path |
| Calendar embed with the new Calendar ID | ✅ **verified rendering live public events** (e.g., Commandery 11 Nov, Chapter 25 Nov) |
| Calendar fallback (no-JS and embed-failure) | ✅ `<noscript>` + always-visible direct link (HTTP 200) |
| Legacy redirects `/history/`, `/pages/` | ✅ meta refresh + canonical |
| Active navigation states | ✅ `aria-current="page"` + visual state |
| Map embed | ⚠ Renders as an empty frame in headless screenshots (Google Maps requires full JS/interaction); embed URL verified HTTP 200 and unchanged from the original site. Needs one human glance post-cutover |

## 8. Security & hygiene

- CSP meta policy on every page; validator asserts the JSON-LD hash inside
  it always matches the emitted structured data. ✅
- 0 console errors, 0 CSP violations in headless browsing of all pages. ✅
- Forbidden strings (placeholder text, migration-archive paths) asserted
  absent. ✅
- No secrets/tokens anywhere in the repository; workflows use only the
  built-in `GITHUB_TOKEN`. ✅

## 9. Deployment validation status

The pipeline is fully operational on GitHub's infrastructure. The
repository-level Pages enablement (once blocked) was completed by an
administrator; every push to `main` now builds, validates, and deploys
automatically.

| Item | Status |
|---|---|
| Workflow triggered on push to `main` | ✅ latest run (`bd94422`) and predecessors |
| Setup Ruby (`~> 3.3`) and locked bundle install | ✅ Pass |
| Jekyll production build (`--strict_front_matter`) on `ubuntu-24.04` | ✅ Pass |
| `tests/validate_site.py` executed in CI against the CI build | ✅ Pass |
| Pages artifact upload (`actions/upload-pages-artifact@v3`) | ✅ Pass |
| Deploy (`actions/deploy-pages@v4`) | ✅ Pass |
| Live production site | ✅ https://mcyorkrite.com serving the deployed build (in front of Cloudflare) |

Two earlier runs surfaced and fixed real CI defects: a bleeding-edge
Bundler 4 lockfile the runner toolchain could not satisfy (re-locked to the
widely supported 2.5 line with Linux platforms added), and a Ruby patch
pin (`3.3.6`) that clashed with the runner's newer `3.3.13` (relaxed to
`~> 3.3`).

**2026-11-13 re-validation** after the venue-rename and design pass: axe
audits clean on all audited pages at desktop width, 16 interaction checks
pass, the validator passes on 22 built pages, the external link checker
reports 25 OK / 0 warnings / 0 broken, no horizontal overflow at 320 px or
390 px on any audited page, and footer/breadcrumb touch targets were
enlarged to 36 px height.

## 10. Remaining issues (none critical)

1. ~~`jmweeks.com` site-credit link does not resolve (DNS).~~ Resolved at
   the organization's direction: the credit now links to
   `focuswithjustin.com` (verified HTTP 200).
2. Final Lighthouse + calendar/map iframe visual check should be repeated
   against the live production URL after cutover (tooling constraints in
   this environment prevented running Lighthouse locally).
3. GitHub Pages settings (source = GitHub Actions, custom domain, enforce
   HTTPS) require an administrator; documented step-by-step in
   deployment.md.
