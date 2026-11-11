# Deployment & Domain Guide

## Hosting model

- The site is served by **GitHub Pages** from the repository
  `Montgomery-County-York-Rite/mcyorkrite.com`.
- Builds run in **GitHub Actions** (`.github/workflows/pages.yml`) using
  the modern *build-with-Actions* flow: the workflow builds `_site`,
  validates it, uploads it as a Pages artifact, and deploys it with
  `actions/deploy-pages@v4`.
- Deployments occur only on pushes to `main` (plus manual `workflow_dispatch`).
  Pull requests build and validate but never deploy.
- Workflow permissions are least-privilege: `contents: read`,
  `pages: write`, `id-token: write`; concurrent deploys are serialized via a
  `pages` concurrency group.

## One-time administrative configuration

These settings live in the GitHub repository and cannot be set from code.
**They require a repository administrator** — verify or set each:

1. **Settings → Pages → Build and deployment → Source**: choose
   **GitHub Actions** (not "Deploy from a branch").
2. **Settings → Pages → Custom domain**: enter `mcyorkrite.com`.
   The committed `CNAME` file keeps this setting anchored across builds.
3. **Settings → Pages → Enforce HTTPS**: enable once the first certificate
   has been issued (GitHub provisions it automatically after the custom
   domain is saved; this can take a few minutes to 24 hours).

A `CNAME` file containing exactly `mcyorkrite.com` is committed at the
repository root; GitHub Pages uses it as the publishing source of record.

## DNS requirements (registrar / DNS provider)

Point the domain at GitHub Pages using either method:

**Option A — apex + www (recommended by GitHub):**

```
mcyorkrite.com.        A     185.199.108.153
mcyorkrite.com.        A     185.199.109.153
mcyorkrite.com.        A     185.199.110.153
mcyorkrite.com.        A     185.199.111.153
www.mcyorkrite.com.    CNAME mcyorkrite.com.
```

**Option B — ALIAS/ANAME (if the provider supports apex ALIAS):**

```
mcyorkrite.com.        ALIAS mcyorkrite.com.github.io
www.mcyorkrite.com.    CNAME mcyorkrite.com.github.io
```

Verification: `dig mcyorkrite.com +short` should return the Pages
addresses; `curl -sI https://mcyorkrite.com` should return `200` with a
`server: GitHub.com` header once both DNS and the Pages settings are live.

> **Important cutover note:** the current live site is served from the
> previous hosting arrangement (it is a Hugo site and this repository was
> empty before the migration). DNS changes and Pages enablement are the
> go-live switches and are deliberately left to the organization: nothing
> in this repository alters the running production site until an
> administrator completes the two steps above.

## Canonical URLs and HTTPS

- `_config.yml` sets `url: "https://mcyorkrite.com"`; every page emits
  `<link rel="canonical">` from that value, so search engines consolidate
  on the production domain regardless of how a visitor arrives.
- GitHub Pages serves HTTPS with a certificate for the custom domain once
  "Enforce HTTPS" is on. The site loads no third-party scripts, so mixed
  content cannot occur; the only embedded third parties are the Google
  Calendar and Maps iframes, both served over HTTPS.
- `www.mcyorkrite.com` is redirected to the configured domain by GitHub
  Pages automatically when both records exist.

## Redirects

Legacy URLs are preserved:

| Legacy path | Behavior |
|---|---|
| `/history/` | Static redirect page → `/about/` (meta refresh + canonical) |
| `/pages/` | Static redirect page → `/` |

GitHub Pages cannot emit server-side 301s, so these are HTML redirects —
the standard static-hosting pattern. All other original URLs resolve
naturally to the same paths in the new site.

## Security notes

- No secrets, tokens, or keys exist anywhere in the repository; the
  workflows only need the built-in `GITHUB_TOKEN`.
- A meta **Content-Security-Policy** is embedded on every page
  (`default-src 'self'`; the only remote frames allowed are
  `calendar.google.com` and `www.google.com`). The inline structured-data
  block is whitelisted by hash. GitHub Pages cannot set HTTP response
  headers, so a meta policy is the strongest available enforcement point;
  header-based additions (HSTS, `frame-ancestors`) remain unavailable and
  are documented here rather than claimed.
- The migration archive and all development tooling are excluded from the
  published output (enforced in `_config.yml` and verified by the
  validator in CI).

## Third-party dependencies (complete list)

| Service | Where | Purpose | Fail-open behavior |
|---|---|---|---|
| Google Calendar embed | `/events/` | Public events display | Always-visible direct link + `noscript` fallback + stated-meetings table |
| Google Maps embed | `/contact/` | Meeting-location map | Address text and a directions link never depend on it |

Nothing else is loaded from outside the site: fonts, styles, scripts, and
images are all self-hosted.
