# Design Decisions — the "Keystone & Arch" design system

The rebuild replaces the previous generic Hugo-theme design (white cards on
a grey body, default theme icons, placeholder content) with an original
design language: **historic Masonic heritage meets refined contemporary
institutional design.**

## Design direction

Dignified, timeless, welcoming. The visual program is built from three
ingredients:

1. **The palette** — midnight navy and warm ivory grounds with antique-gold
   detailing; burgundy and two kindred accents give each York Rite body its
   own wayfinding color.
2. **The architecture of the arch** — every hero sits on concentric
   arch linework rising from the section's base; a keystone mark serves as
   the site's signature ornament and favicon.
3. **Editorial typography** — an elegant serif (EB Garamond) for headings
   and ceremonial voice, a workhorse humanist sans (Source Sans 3) for
   reading and navigation.

What was deliberately avoided: gradients-as-decoration, metallic/gold
texture effects, busy backgrounds, drop-shadow stacking, animation without
purpose, and icon soup. Decorative SVGs are thin-line architecture, not
illustration.

## Color tokens

| Token | Hex | Usage |
|---|---|---|
| `--navy` | `#101E35` | Header, footer, hero and CTA bands |
| `--navy-deep` | `#0B1526` | Footer ground, breadcrumbs, drawer |
| `--navy-soft` | `#1B2A47` | Reserved (hover surfaces) |
| `--gold` | `#BA9555` | Accents, hairlines, buttons on dark grounds, medallion rings. **Never body-size text on light grounds** |
| `--gold-bright` | `#D9BC85` | Gold text on navy (passes AA) |
| `--bronze` | `#7A5F2D` | The gold family darkened to pass contrast as text on ivory/white (eyebrow labels, keystone divider) |
| `--burgundy` | `#7A2632` | Primary buttons, links, Chapter accent |
| `--cryptic` | `#4A3B6B` | Council accent |
| `--templar` | `#1E3357` | Commandery accent |
| `--ivory` | `#F8F4E9` | Page background |
| `--ivory-deep` | `#EFE8D6` | Alternate section bands |
| `--slate` | `#283446` | Body text |
| `--slate-soft` | `#46536B` | Secondary text |

### Contrast policy (WCAG 2.2 AA)

- Body text `--slate` on `--ivory`/white: ≥ 10:1.
- `--gold` is reserved for large decorative strokes and for text on navy
  (≈ 5.9:1); on light grounds the darker `--bronze` (≥ 4.9:1) is used
  instead — this was corrected during QA when the original bronze value
  fell below 4.5:1 on the `--ivory-deep` band.
- Buttons: burgundy/white ≈ 9.8:1; gold/navy ≈ 5.9:1; outline-light ivory on
  navy ≈ 15:1.
- Body accents (`--burgundy`, `--cryptic`, `--templar`) are used on borders
  and large type only; meaning is never carried by color alone (cards also
  carry ordinal labels — "First of the three bodies", etc.).

## Typography

| Role | Font | Notes |
|---|---|---|
| Display/headings | EB Garamond 600 | Self-hosted WOFF2, `font-display: swap`, preloaded 600 |
| Body/UI | Source Sans 3 400/600/700 | Self-hosted WOFF2, preloaded 400 |
| Ceremonial labels | Source Sans 3 600, uppercase, `0.16em` tracking | The "eyebrow" component |

System fallbacks: Garamond/Georgia serif stack and the standard sans stack.
No third-party font service is contacted at runtime. Total font payload for
a first visit is ~66 KB (the two preloaded faces); italic and 700 load only
on pages that use them.

## Layout conventions

- `.container`: 1080 px max width, fluid gutters (`clamp(1.25rem, 5vw, 2rem)`).
- Section rhythm: `clamp(3.5rem, 8vw, 6rem)` vertical padding; alternating
  ivory / ivory-deep bands bordered by 1 px hairlines.
- The mobile layout is designed, not merely stacked: the homepage intro
  card moves below the prose, body cards become centered full-width
  medallions, and the navigation collapses into a full-height drawer with a
  scrim.
- Breakpoints: base (≥ 320 px), 700 px (3-col card grids), 760 px (body
  hero becomes two-column), 900 px (inline nav replaces drawer; two-column
  meeting info), 1000 px (four-column footer).

## Reusable components

| Component | Include / class | Purpose |
|---|---|---|
| Header + brand | `_includes/header.html`, `.site-header` | Sticky navy masthead, keystone mark, stacked wordmark |
| Navigation | `_includes/navigation.html` (desktop / mobile / footer variants) | Active states via `aria-current="page"` |
| Mobile drawer | `_includes/mobile-nav.html` + `assets/js/main.js` | Disclosure pattern: `aria-expanded`, focus trap, Escape, scrim click |
| Breadcrumbs | `_includes/breadcrumbs.html` | On sub-pages, `aria-label="Breadcrumb"` |
| Hero | `_includes/hero.html` | Home hero with arch linework |
| Body hero | `_layouts/body.html` | Per-body band with medallion and accent |
| Body card | `_includes/body-card.html` | Emblem medallion, ordinal, name, tagline, summary, link |
| Info card | `.info-card` | Meeting summary on the homepage |
| Meeting info | `_includes/meeting-info.html` | Schedule table + location (+ map on contact) |
| Calendar | `_includes/calendar.html` | Lazy iframe, `noscript` and always-visible fallback link, timezone note |
| Contact actions | `_includes/contact-actions.html` | Email button, copy-address button with live status, directions link |
| Keystone divider | `_includes/keystone-divider.html` | Section ornament (decorative, `aria-hidden`) |
| Buttons | `.btn--primary/-gold/-outline/-outline-light` | 44 px minimum target height |
| Progression | `.progression-steps`, `.rite-progression` | The Chapter → Council → Commandery sequence |
| Page band / 404 | `.page-band`, `.error-section` | Title bands and the 404 screen |

## Image conventions

- The three authentic emblems are presented in circular white medallions
  with gold rings, which both unifies their differing styles (two
  transparent PNGs, one opaque GIF) and frames them as seals.
- All raster images carry intrinsic `width`/`height` to prevent layout
  shift, `decoding="async"`, and `loading="lazy"` except the hero medallion.
- The OG/social image (1200×630 PNG, 24 KB) is generated from the same
  tokens by `scripts/generate_brand_assets.py`.

## Motion

One transition family only: 150 ms color/transform feedback on links,
buttons, and the drawer. `prefers-reduced-motion` collapses all of it to
zero. No scroll effects, parallax, or entrance animations.

## Print

Headers, navigation, calendar/map iframes, and footers are excluded from
print; text prints black-on-white.
