#!/usr/bin/env python3
"""
Generate brand assets (favicons and the social preview image) for the
Montgomery County York Rite website.

Artwork is original linework created for this site: a keystone (the central
stone of a masonic arch) on a midnight navy field, drawn from the same
geometry as assets/images/mark.svg.

Fonts are variable TTFs fetched from the google/fonts repository (both under
the SIL Open Font License) and are only used at generation time; the site
itself serves self-hosted WOFF2 subsets. Font files live in
scripts/fonts-tmp/ (git-ignored) so no font binaries are committed here.

Usage:  python3 scripts/generate_brand_assets.py
Output: assets/images/favicon-32.png
        assets/images/apple-touch-icon.png
        assets/images/og-default.png
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "images"
FONTS = Path(__file__).resolve().parent / "fonts-tmp"

NAVY = (16, 30, 53, 255)        # #101E35
NAVY_DEEP = (11, 21, 38, 255)   # #0B1526
GOLD = (186, 149, 85, 255)      # #BA9555
GOLD_BRIGHT = (217, 188, 133, 255)
IVORY = (248, 244, 233, 255)

SERIF = FONTS / "EBGaramond.ttf"
SANS = FONTS / "SourceSans3.ttf"


def set_weight(font: ImageFont.FreeTypeFont, weight: int) -> None:
    """Select a named weight on a variable font."""
    try:
        font.set_variation_by_axes([weight])
    except Exception:
        pass  # static fallback: default instance is fine


def draw_keystone(draw: ImageDraw.ImageDraw, scale: float, ox: float, oy: float) -> None:
    """Keystone linework matching assets/images/mark.svg."""
    def x(v):
        return ox + v * scale

    def y(v):
        return oy + v * scale

    lw = max(1, round(2.2 * scale))
    # Keystone body: apex width 19-29, base 14-34 at y=33.
    draw.polygon(
        [(x(19), y(15)), (x(29), y(15)), (x(34), y(33)), (x(14), y(33))],
        outline=GOLD,
        width=lw,
    )
    # Vertical joint.
    draw.line([(x(24), y(15.5)), (x(24), y(33))], fill=GOLD, width=max(1, round(1.6 * scale)))
    # Bed line.
    draw.line([(x(12), y(37)), (x(36), y(37))], fill=GOLD, width=lw)


def rounded_square(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    radius = size * 0.15
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=NAVY, outline=GOLD, width=max(2, size // 20))
    draw_keystone(draw, size / 48.0, size * 0.06, size * 0.06)
    return img


def make_favicons() -> None:
    master = rounded_square(512)
    master.resize((32, 32), Image.LANCZOS).save(OUT / "favicon-32.png", optimize=True)
    # Apple touch icons are full-bleed squares; iOS applies its own mask.
    tile = Image.new("RGB", (180, 180), NAVY[:3])
    d = ImageDraw.Draw(tile)
    draw_keystone(d, 180 / 48.0, 180 * 0.06, 180 * 0.06)
    tile.save(OUT / "apple-touch-icon.png", optimize=True)
    print("favicons written")


def make_og_image() -> None:
    img = Image.new("RGBA", (1200, 630), NAVY)
    draw = ImageDraw.Draw(img)

    # Concentric arches rising from the bottom edge.
    cx = 600
    for radius, opacity in ((680, 22), (600, 30), (500, 22), (410, 16), (320, 12)):
        box = [cx - radius, 630 - radius, cx + radius, 630 + radius]
        draw.arc(box, 180, 360, fill=(186, 149, 85, opacity), width=2)
    draw.line([(600, 40), (600, 630)], fill=(186, 149, 85, 20), width=2)

    # Keystone mark, centred above the title.
    mark = rounded_square(96)
    img.alpha_composite(mark, (552, 64))

    serif = ImageFont.truetype(str(SERIF), 64)
    set_weight(serif, 600)
    sans = ImageFont.truetype(str(SANS), 26)
    set_weight(sans, 600)
    sans_small = ImageFont.truetype(str(SANS), 22)
    set_weight(sans_small, 400)

    def center(text, font, fill, y, tracking=0):
        if tracking:
            widths = [draw.textlength(ch, font=font) + tracking for ch in text]
            total = sum(widths) - tracking
            x = (1200 - total) / 2
            for ch, w in zip(text, widths):
                draw.text((x, y), ch, font=font, fill=fill)
                x += w
        else:
            w = draw.textlength(text, font=font)
            draw.text(((1200 - w) / 2, y), text, font=font, fill=fill)

    center("ROYAL ARCH · CRYPTIC MASONRY · KNIGHTS TEMPLAR", sans, GOLD_BRIGHT, 196, tracking=6)
    center("Montgomery County", serif, IVORY, 252)
    center("York Rite", serif, IVORY, 330)

    # Gold rule.
    draw.line([(420, 462), (780, 462)], fill=GOLD, width=2)

    center("The York Rite Bodies of Montgomery County, Maryland", sans_small, (248, 244, 233, 200), 486)
    center("Meeting at Pentalpha Lodge #194 · Germantown, Maryland", sans_small, (248, 244, 233, 170), 524)

    # Flatten onto navy and save optimized.
    out = Image.new("RGB", img.size, NAVY[:3])
    out.paste(img, (0, 0))
    quantized = out.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    quantized.save(OUT / "og-default.png", optimize=True)
    print("og image written")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    make_favicons()
    make_og_image()
    for name in ("favicon-32.png", "apple-touch-icon.png", "og-default.png"):
        p = OUT / name
        print(f"  {name}: {p.stat().st_size / 1024:.1f} KB")
