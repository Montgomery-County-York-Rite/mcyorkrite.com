# Montgomery County York Rite: Website

The public website of the Montgomery County York Rite bodies (Maryland):
a Chapter of Royal Arch Masons, a Council of Cryptic Masons, and a
Commandery of Knights Templar, meeting at Pentalpha Masonic Temple in
Germantown, Maryland.

- **Production URL:** <https://mcyorkrite.com>
- **Hosting:** GitHub Pages (built by GitHub Actions from `main`)
- **Generator:** Jekyll 4, static HTML/CSS, no JavaScript framework

## Quick start

Prerequisites: Ruby (see `.ruby-version`), Bundler, and Python 3 for the
validation scripts.

```sh
bundle install            # install Ruby dependencies
bundle exec rake serve    # preview at http://127.0.0.1:4000
```

## Build, test, validate

```sh
bundle exec rake build      # build into _site/
bundle exec rake validate   # run the static output validator
bundle exec rake test       # build + validate
bundle exec rake linkcheck  # check outbound links (needs network)
bundle exec rake serve      # local preview
```

Browser-based QA (screenshots, axe-core accessibility audit, interaction
checks) is available locally:

```sh
python3 -m pip install --user playwright && python3 -m playwright install chromium
python3 tests/visual_qa.py _site
```

## Repository layout

```
├── _config.yml            Site configuration (single source of truth for
│                          site-wide settings; content facts live in _data)
├── _data/
│   ├── navigation.yml     Primary navigation
│   ├── organization.yml   Contact details, meetings, calendar configuration
│   └── bodies.yml         The three York Rite bodies
├── _layouts/              default, home, page, body, redirect
├── _includes/             header, footer, navigation, seo, components…
├── index.md               Home
├── about/                 About, Chapter, Council, Commandery
├── events/                Events (Google Calendar embed)
├── contact/               Contact (email, address, meetings, map)
├── history/ pages/        Legacy-URL redirects
├── assets/                css, js, self-hosted fonts, images
├── docs/                  Migration, design, QA, and maintenance records
├── scripts/               Brand-asset generator and external link checker
├── tests/                 Static output validator and browser QA harness
├── migration-archive/     Snapshots of the original website (excluded from
│                          the build; reference material only)
└── .github/workflows/     pages.yml (deploy), validate.yml (PR checks)
```

## Documentation

| Document | Purpose |
|---|---|
| [docs/maintenance.md](docs/maintenance.md) | How to edit text, meetings, pages, images, navigation |
| [docs/deployment.md](docs/deployment.md) | GitHub Pages, custom domain, DNS, HTTPS |
| [docs/migration-inventory.md](docs/migration-inventory.md) | Every page found on the old site and where it went |
| [docs/content-mapping.md](docs/content-mapping.md) | Old content → new source files, editorial changes |
| [docs/asset-inventory.md](docs/asset-inventory.md) | Original assets, provenance, and treatment |
| [docs/design-decisions.md](docs/design-decisions.md) | The design system: colors, type, components |
| [docs/qa-report.md](docs/qa-report.md) | Validation results at delivery time |

## Content principles

- Organization facts live in `_data/organization.yml`; edit there, not in
  templates.
- Nothing is published about ritual work, membership rosters, or anything
  beyond what the previous public site already published.
- Historical statements carried over from the previous site are preserved
  verbatim except for documented typographical corrections (see
  [docs/content-mapping.md](docs/content-mapping.md)).

## License

Site content © Montgomery County York Rite. Fonts are provided under the
SIL Open Font License (EB Garamond, Source Sans 3). Original decorative
linework was created for this site and is released for the organization's
use. Retained emblems remain the property of their respective bodies.
