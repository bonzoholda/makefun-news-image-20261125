#!/usr/bin/env python3
"""Draw the front page of 'The World Today' for Wednesday 25 November 2026.

A one-page newspaper front page, drawn entirely with PIL primitives:
masthead, a lead story about the Houthi drone strike on Riyadh's PIF
Tower, and four secondary stories (Sparta II, Huawei, the CIA/ODNI
breach, Giuliani's Medal of Freedom). No photos, no stock art, no
network access. The output is deterministic: running this script twice
produces byte-identical PNG files.
"""

import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (24, 24, 24)
RED = (164, 30, 34)
GRAY = (96, 96, 92)
GOLD = (178, 142, 60)
BLUE = (36, 82, 128)
LIGHT = (231, 225, 211)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF = FONT_DIR / "DejaVuSerif.ttf"
SERIF_B = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_B = FONT_DIR / "DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(str(path), size)


def fit_size(draw, lines, path, start_size, max_width):
    """Largest font size (<= start_size) at which every line fits max_width."""
    size = start_size
    while size > 10:
        fnt = ImageFont.truetype(str(path), size)
        if all(draw.textlength(line, font=fnt) <= max_width for line in lines):
            return size
        size -= 1
    return size


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, measured with fnt."""
    lines = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(cx, cy, r_out, r_in, points=5):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        angle = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def burst(cx, cy, r_out, r_in, spikes=8):
    pts = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        angle = -math.pi / 2 + i * math.pi / spikes
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def draw_tower(draw, x0, y0, x1, y1):
    """A dark tower with lit windows, an antenna, a drone and an impact burst."""
    draw.rectangle([x0, y0, x1, y1], fill=INK)
    cx = (x0 + x1) // 2
    draw.line([cx, y0, cx, y0 - 30], fill=INK, width=5)
    draw.ellipse([cx - 6, y0 - 38, cx + 6, y0 - 26], fill=RED)
    for row in range(8):
        wy = y0 + 30 + row * 34
        for col in range(4):
            wx = x0 + 28 + col * 52
            draw.rectangle([wx, wy, wx + 20, wy + 13], fill=LIGHT)
    # drone hovering in the empty band above the tower, left of the antenna
    dx, dy = x0 + 70, y0 - 18
    draw.ellipse([dx - 9, dy - 9, dx + 9, dy + 9], fill=INK)
    draw.line([dx - 32, dy, dx - 10, dy], fill=INK, width=4)
    draw.line([dx + 10, dy, dx + 32, dy], fill=INK, width=4)
    draw.ellipse([dx - 42, dy - 5, dx - 24, dy + 5], fill=INK)
    draw.ellipse([dx + 24, dy - 5, dx + 42, dy + 5], fill=INK)
    # red impact burst on the tower face
    bx, by = x0 + 190, y0 + 96
    draw.polygon(burst(bx, by, 30, 13), fill=RED)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 255, 255))


def draw_ship(draw, x, y):
    """Cargo ship with containers and waves, inside an 88x88 box."""
    draw.rectangle([x + 16, y + 30, x + 36, y + 56], fill=BLUE)
    draw.rectangle([x + 40, y + 36, x + 60, y + 56], fill=RED)
    draw.rectangle([x + 62, y + 26, x + 78, y + 56], fill=INK)
    draw.polygon(
        [(x + 6, y + 56), (x + 82, y + 56), (x + 74, y + 72), (x + 14, y + 72)],
        fill=INK,
    )
    for wx in (x + 4, x + 32, x + 60):
        draw.arc([wx, y + 76, wx + 26, y + 88], 0, 180, fill=BLUE, width=3)


def draw_scales(draw, x, y):
    """Balance scales, inside an 88x88 box."""
    draw.line([x + 14, y + 80, x + 74, y + 80], fill=INK, width=4)
    draw.line([x + 44, y + 20, x + 44, y + 80], fill=INK, width=4)
    draw.line([x + 16, y + 26, x + 72, y + 26], fill=INK, width=4)
    draw.line([x + 16, y + 26, x + 8, y + 52], fill=INK, width=3)
    draw.line([x + 16, y + 26, x + 24, y + 52], fill=INK, width=3)
    draw.line([x + 72, y + 26, x + 64, y + 52], fill=INK, width=3)
    draw.line([x + 72, y + 26, x + 80, y + 52], fill=INK, width=3)
    draw.polygon([(x + 4, y + 52), (x + 28, y + 52), (x + 16, y + 64)], fill=INK)
    draw.polygon([(x + 60, y + 52), (x + 84, y + 52), (x + 72, y + 64)], fill=INK)


def draw_lock(draw, x, y):
    """Padlock with a red crack, inside an 88x88 box."""
    draw.arc([x + 28, y + 8, x + 60, y + 44], 180, 360, fill=INK, width=6)
    draw.rectangle([x + 18, y + 40, x + 70, y + 80], fill=INK)
    draw.ellipse([x + 38, y + 50, x + 50, y + 62], fill=PAPER)
    draw.polygon([(x + 41, y + 60), (x + 47, y + 60), (x + 44, y + 70)], fill=PAPER)
    draw.line(
        [(x + 24, y + 44), (x + 36, y + 54), (x + 30, y + 62), (x + 44, y + 74)],
        fill=RED,
        width=3,
    )


def draw_medal(draw, x, y):
    """Medal on ribbons, inside an 88x88 box."""
    draw.polygon([(x + 30, y + 6), (x + 44, y + 6), (x + 40, y + 34), (x + 28, y + 34)], fill=RED)
    draw.polygon([(x + 44, y + 6), (x + 58, y + 6), (x + 60, y + 34), (x + 48, y + 34)], fill=BLUE)
    draw.ellipse([x + 20, y + 30, x + 68, y + 78], fill=GOLD, outline=INK, width=2)
    draw.polygon(star(x + 44, y + 54, 16, 7), fill=PAPER)


def secondary(draw, x, y, kicker, headline, body, icon):
    """One secondary story cell: icon on the left, text on the right."""
    icon(draw, x, y)
    tx = x + 104
    tw = 344
    draw.text((tx, y), kicker, font=load(SANS_B, 15), fill=RED)
    hy = y + 22
    lines = wrap(draw, headline, load(SERIF_B, 24), tw)
    hy = put_lines(draw, lines, tx, hy, load(SERIF_B, 24), INK, 29)
    by = hy + 6
    blines = wrap(draw, body, load(SANS, 17), tw)
    put_lines(draw, blines, tx, by, load(SANS, 17), INK, 22)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 48

    # top rules + masthead
    d.line([(m, 26), (W - m, 26)], fill=INK, width=3)
    d.line([(m, 33), (W - m, 33)], fill=INK, width=1)
    mast_size = fit_size(d, ["THE WORLD TODAY"], SERIF_B, 92, W - 2 * m)
    d.text((W // 2, 44), "THE WORLD TODAY", font=load(SERIF_B, mast_size), fill=INK, anchor="mt")
    d.line([(m, 158), (W - m, 158)], fill=INK, width=2)
    d.text((m, 170), "WEDNESDAY, 25 NOVEMBER 2026", font=load(SANS_B, 20), fill=INK)
    d.text((W - m, 170), "FIVE STORIES · ONE PAGE", font=load(SANS_B, 20), fill=INK, anchor="ra")
    d.line([(m, 202), (W - m, 202)], fill=INK, width=1)

    # lead kicker + three-line headline (left column)
    d.text((m, 214), "CONFLICT — RIYADH, SAUDI ARABIA", font=load(SANS_B, 21), fill=RED)
    head_lines = ["HOUTHI DRONE HITS", "RIYADH'S TALLEST", "TOWER"]
    head_size = fit_size(d, head_lines, SERIF_B, 54, 592)
    put_lines(d, head_lines, m, 246, load(SERIF_B, head_size), INK, int(head_size * 1.15))

    # lead deck (left column, under the headline)
    deck = (
        "A Houthi drone struck the Public Investment Fund Tower in Riyadh "
        "on Tuesday — the second hit on the same tower in under a week. "
        "Eleven people were wounded."
    )
    put_lines(d, wrap(d, deck, load(SERIF, 24), 592), m, 440, load(SERIF, 24), INK, 32)

    # lead art: tower on the right, spanning the whole lead block
    draw_tower(d, 690, 250, 950, 576)

    # divider
    d.line([(m, 596), (W - m, 596)], fill=INK, width=2)

    # four secondaries in a 2x2 grid
    stories = [
        (
            "CONFLICT — GULF OF FINLAND",
            "Zelenskiy confirms Sparta II strike",
            "Kyiv says the ship carried weapons; one crew member was hurt — "
            "the fourth Russian vessel hit since 11 November.",
            draw_ship,
        ),
        (
            "COURTS — NEW YORK",
            "Huawei guilty on 10 of 12 counts",
            "Fraud and trade-secret theft were proven; the racketeering "
            "charge failed. Sentencing is set for September 2027.",
            draw_scales,
        ),
        (
            "SECURITY — WASHINGTON",
            "CIA and ODNI hit by cyber breach",
            "Some unclassified material was exposed; classified systems "
            "were untouched, officials said. The breach has been fixed.",
            draw_lock,
        ),
        (
            "POLITICS — WASHINGTON",
            "Giuliani gets Medal of Freedom",
            "Trump placed the nation's highest civilian honor on the "
            "82-year-old in a private Oval Office ceremony.",
            draw_medal,
        ),
    ]
    positions = [(48, 616), (528, 616), (48, 792), (528, 792)]
    for (kx, ky), (kicker, headline, body, icon) in zip(positions, stories):
        secondary(d, kx, ky, kicker, headline, body, icon)

    # footer
    d.line([(m, 968), (W - m, 968)], fill=INK, width=1)
    d.text(
        (W // 2, 980),
        "THE WORLD TODAY · WEDNESDAY 25 NOVEMBER 2026 · FIVE STORIES, ONE PAGE",
        font=load(SANS, 15),
        fill=GRAY,
        anchor="mt",
    )

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, format="PNG")
    data = out.read_bytes()
    print(f"wrote {out} ({len(data)} bytes) md5={hashlib.md5(data).hexdigest()}")


if __name__ == "__main__":
    main()
