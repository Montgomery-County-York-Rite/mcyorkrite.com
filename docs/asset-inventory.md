# Asset Inventory

Every asset discovered on the original site, its disposition in the rebuild,
and the licensing/provenance position.

## Original site assets (discovered via crawl)

| Asset | Where used originally | Disposition | Provenance / rights position |
|---|---|---|---|
| `/images/chapter.png` (225×225 PNG, 30 KB) | About page card | **Preserved** → `assets/images/chapter.png`; used in the three-bodies cards and the Chapter page hero | Organization-approved Royal Arch emblem (Triple Tau in triangle and circle). Retained as-is; transparent background intact |
| `/images/council.png` (225×224 PNG, 18 KB) | About page card | **Preserved** → `assets/images/council.png` | Organization-approved Cryptic Council emblem. Retained as-is |
| `/images/commandery.gif` (218×225 GIF, 28 KB) | About page card | **Preserved** → `assets/images/commandery.gif` | Knights Templar "In Hoc Signo Vinces" cross-and-crown emblem. Retained as-is; displayed inside a white medallion so its opaque white ground reads as intentional framing |
| `/favicon.png` (256×256 PNG) | Browser icon | **Not carried over** | Verified during migration to be a generic Hugo-theme default (a blue letter "H") — it is not organization identity. Replaced (see below). Original file retained in `migration-archive/assets/` for reference |
| `/features/noun_branding_1885335.svg`, `noun_The%20Process_1885341.svg`, `noun_3d%20modeling_1885342.svg` | `/history/` placeholder page | **Discarded** | Unrelated stock demo icons from the previous theme (accounting-services placeholders). Not organization material |
| Google Calendar embed | `/events/` | **Preserved and reconfigured** | Third-party service (Google); documented in deployment notes |
| Google Maps embed | `/contact/` | **Preserved verbatim** | Third-party service (Google); same embed URL as the original site |
| Stylesheet `/css/style.min.3101f3….css` (Hugo build) | Whole site | **Discarded** | Replaced by the new original design system |

## New assets created for the rebuild

| Asset | Source | License position |
|---|---|---|
| `assets/images/mark.svg`, `favicon.svg` | Original keystone linework drawn for this site (a keystone — the central stone of a masonic arch — on a midnight field). Deliberately generic Masonic geometry: no borrowed seal, no heraldry of any other organization | Created for the organization's use |
| `assets/images/favicon-32.png`, `apple-touch-icon.png`, `og-default.png` | Generated from the same linework by `scripts/generate_brand_assets.py` | Created for the organization's use |
| `assets/fonts/eb-garamond-*.woff2` (400, 400 italic, 600) | EB Garamond, self-hosted latin subsets | SIL Open Font License 1.1 |
| `assets/fonts/source-sans-3-*.woff2` (400, 600, 700) | Source Sans 3, self-hosted latin subsets | SIL Open Font License 1.1 |
| Inline SVG ornaments (hero arch linework, keystone divider, tradition-section arch) | Original linework created for this site | Created for the organization's use |

The identity brief explicitly excluded "generic AI-generated heraldry" and
appropriation of other bodies' seals; the decorative program therefore uses
plain geometric masonic motifs (arches, keystones) plus the three authentic
emblems already published by the organization.

## Rights hygiene

- No third-party photographs were found on the original site, and none were
  added.
- The migration archive (`migration-archive/`) holds the raw snapshots and
  the original assets for provenance; it is excluded from the Jekyll build
  and from the published site.
- No private, ritual, or internal material was encountered or included.
