# Maintenance Guide

This site is built so that routine updates never require touching HTML,
CSS, or JavaScript. Almost everything lives in Markdown and two YAML files.

## Previewing the site locally

```sh
bundle install          # first time only
bundle exec rake serve  # http://127.0.0.1:4000
```

## Editing site text

Ordinary page copy is Markdown in these files:

| Page | File |
|---|---|
| Home | `index.md` |
| About | `about/index.md` |
| Chapter | `about/chapter.md` |
| Council | `about/council.md` |
| Commandery | `about/commandery.md` |
| Events | `events/index.md` |
| Contact | `contact/index.md` |
| 404 | `404.html` |

Edit the Markdown like any document; keep headings in order (`##` under the
page title). Front matter at the top carries each page's `title`,
`description` (the search-engine snippet — keep it under ~160 words of one
sentence or two), and `breadcrumbs`.

After editing, run `bundle exec rake test` — it verifies every page still
has unique titles/descriptions, working links, and preserved substantive
content (the validator fails if key sentences from the original site are
removed).

## Updating meeting information

All meeting facts live in **`_data/organization.yml`**:

- `meetings:` — the schedule table (day/time pairs). Add or edit a line and
  the homepage, events, and contact pages all update together.
- `meeting_location:` — lodge name, street, city, postal code, directions
  note.
- `email:` — the public contact address.
- `calendar:` — the Google Calendar embed. `id` is the Calendar ID; if the
  bodies move to a new calendar, replace the ID here (and update
  `web_link`, the fallback link). Everything else about the embed stays
  the same.

## Adding a new page

1. Create a directory with an `index.md`, or a single `.md` file — with
   `permalink: pretty` the URL is derived from the file path
   (`about/chapter.md` → `/about/chapter/`).
2. Front matter:

   ```yaml
   ---
   layout: page
   title: "New Page Title"
   description: "One-sentence search description."
   breadcrumbs:
     - label: "New Page Title"
   ---
   ```

3. Write Markdown below the front matter.
4. To add it to navigation, append an item in `_data/navigation.yml`.
5. Run `bundle exec rake test`.

A page whose `layout` is `body` additionally needs `body_key` matching a
key in `_data/bodies.yml` (that is how the Chapter/Council/Commandery pages
share their band and CTA treatment).

## Adding or replacing an image

1. Put the file in `assets/images/` (use descriptive names, prefer PNG for
   emblems/graphics; keep files under ~100 KB).
2. Reference it with Markdown:

   ```markdown
   ![Descriptive alt text for screen readers](/assets/images/example.png)
   ```

3. Regenerating the favicon/social image is only needed after changing
   brand colors: `python3 scripts/generate_brand_assets.py` (requires
   Pillow and the OFL fonts in `scripts/fonts-tmp/`; the script fetches
   them itself — see the file header).

## Updating navigation

`_data/navigation.yml` drives the desktop header, the mobile drawer, and
footer link targets are in `_includes/footer.html`. Items can carry
`children:` (shown in the mobile drawer under their parent, as "About"
does today). `active_on:` controls highlight matching for section pages.

## Maintaining the calendar

- The embed configuration lives in `_data/organization.yml` under
  `calendar:`. The `id` is the Calendar ID (preferred over the legacy
  e-mail address), `timezone` is the IANA zone shown with the embed, and
  `web_link` is the fallback link.
- To change what appears on the calendar, edit the Google Calendar itself
  (the same calendar the ID points to). The website needs no changes.
- If Google's embed ever fails, visitors still see the always-present
  direct link below the frame and the stated-meetings table.

## Deployment

Pushes to `main` build and deploy automatically via GitHub Actions
(`.github/workflows/pages.yml`). Pull requests are built and validated
without deploying (`validate.yml`). See
[deployment.md](deployment.md) for the one-time configuration and DNS.

## Troubleshooting a failed deploy

1. Open the **Actions** tab in GitHub and read the failing step.
2. Most failures are validator failures — run `bundle exec rake test`
   locally; it reproduces the same checks the CI runs.
3. If `bundle install` fails, confirm `.ruby-version` matches the version
   configured in the workflows (3.3) and that `Gemfile.lock` is committed.
4. If Pages shows a 404 after a green deploy, check
   **Settings → Pages** — the source must be *GitHub Actions*, and the
   custom domain must still be set (see deployment.md).
