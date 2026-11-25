#!/usr/bin/env python3
"""Draw the front page for the make.fun news-image-20261125 entry.

One image, 1024x1024 PNG, summing up Wednesday 25 November 2026 in the
style of a newspaper front page: masthead, one lead story (Houthi drone
strike on Riyadh's PIF Tower) with a large drawn visual, and four
secondary stories with small drawn icons. All five stories and every
fact below were verified against news sources on 25 Nov 2026 (see
../../cuan-team/research/news-image-20261125-story-lock.md).

Deterministic: no randomness, no timestamps, no network. Running this
script twice produces byte-identical output.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)      # warm newsprint
INK = (17, 17, 17)
RED = (179, 38, 30)
GRAY = (90, 90, 90)
BLUE = (28, 68, 110)
TEAL = (31, 120, 110)
GREEN = (27, 120, 60)
GOLD = (176, 132, 30)
LIGHT = (238, 232, 218)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_tower(draw, cx, cy, w, h):
    """The PIF Tower: a tall twisting skyscraper, hit near the top.

    A dark tower with a twisted top, pale window bands, a small drone
    above it and a red impact burst on its upper floors.
    """
    top_w, bot_w = w * 0.62, w
    top_y, bot_y = cy - h / 2, cy + h / 2
    # twisted body: top shifted right, base shifted left
    draw.polygon([
        (cx - top_w / 2 + w * 0.16, top_y),
        (cx + top_w / 2 + w * 0.16, top_y),
        (cx + bot_w / 2 - w * 0.10, bot_y),
        (cx - bot_w / 2 - w * 0.10, bot_y),
    ], fill=INK)
    # pale window bands
    for i in range(1, 7):
        yy = top_y + (bot_y - top_y) * i / 7
        frac = i / 7
        half = (top_w / 2 + (bot_w - top_w) / 2 * frac)
        xoff = w * 0.16 - (w * 0.26) * frac
        draw.line([(cx - half + xoff, yy), (cx + half + xoff, yy)],
                  fill=(150, 150, 150), width=2)
    # impact burst near the top
    bx, by = cx + w * 0.28, top_y + h * 0.22
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        r1, r2 = w * 0.06, w * 0.17
        draw.line([(bx + r1 * math.cos(a), by + r1 * math.sin(a)),
                   (bx + r2 * math.cos(a), by + r2 * math.sin(a))],
                  fill=RED, width=4)
    draw.ellipse([bx - w * 0.06, by - w * 0.06, bx + w * 0.06, by + w * 0.06],
                 fill=RED)
    # drone above the tower
    dx, dy = cx + w * 0.42, top_y - h * 0.10
    draw.ellipse([dx - w * 0.07, dy - w * 0.07, dx + w * 0.07, dy + w * 0.07],
                 fill=INK)
    for sx in (-1, 1):
        draw.line([(dx + sx * w * 0.10, dy), (dx + sx * w * 0.24, dy)],
                  fill=INK, width=4)


def icon_cargo(draw, x, y, s):
    """Cargo ship (Sparta II) with containers and a drone above."""
    # drone
    draw.ellipse([x + s * 0.62, y + s * 0.04, x + s * 0.76, y + s * 0.18], fill=INK)
    for dx in (0.50, 0.82):
        draw.line([(x + s * dx, y + s * 0.11), (x + s * dx + s * 0.13, y + s * 0.11)],
                  fill=INK, width=4)
    # container stacks
    draw.rectangle([x + s * 0.16, y + s * 0.30, x + s * 0.38, y + s * 0.44], fill=BLUE)
    draw.rectangle([x + s * 0.16, y + s * 0.45, x + s * 0.38, y + s * 0.52], fill=TEAL)
    draw.rectangle([x + s * 0.40, y + s * 0.38, x + s * 0.60, y + s * 0.52], fill=TEAL)
    draw.rectangle([x + s * 0.62, y + s * 0.38, x + s * 0.76, y + s * 0.52], fill=GOLD)
    # bridge
    draw.rectangle([x + s * 0.78, y + s * 0.30, x + s * 0.88, y + s * 0.52], fill=INK)
    # hull
    draw.polygon([(x + s * 0.06, y + s * 0.52), (x + s * 0.94, y + s * 0.52),
                  (x + s * 0.80, y + s * 0.72), (x + s * 0.20, y + s * 0.72)],
                 fill=INK)
    # waves
    for wy in (0.80, 0.90):
        draw.arc([x + s * 0.05, y + s * wy, x + s * 0.48, y + s * (wy + 0.14)],
                 180, 360, fill=BLUE, width=3)
        draw.arc([x + s * 0.52, y + s * wy, x + s * 0.95, y + s * (wy + 0.14)],
                 180, 360, fill=BLUE, width=3)


def icon_gavel(draw, x, y, s):
    """Judge's gavel over a sound block, with a 10/12 verdict badge."""
    # sound block
    draw.rectangle([x + s * 0.18, y + s * 0.78, x + s * 0.62, y + s * 0.88], fill=INK)
    # handle (diagonal)
    draw.line([(x + s * 0.30, y + s * 0.74), (x + s * 0.62, y + s * 0.34)],
              fill=INK, width=9)
    # gavel head
    draw.rectangle([x + s * 0.52, y + s * 0.20, x + s * 0.82, y + s * 0.40],
                   fill=INK)
    draw.rectangle([x + s * 0.48, y + s * 0.16, x + s * 0.56, y + s * 0.44],
                   fill=INK)
    draw.rectangle([x + s * 0.78, y + s * 0.16, x + s * 0.86, y + s * 0.44],
                   fill=INK)
    # verdict badge: 10/12 (bottom-right, clear of the gavel head)
    draw.ellipse([x + s * 0.68, y + s * 0.60, x + s * 0.99, y + s * 0.91],
                 fill=RED, outline=PAPER, width=2)
    f = font(SANS_B, int(s * 0.11))
    label = "10/12"
    tw = draw.textlength(label, font=f)
    draw.text((x + s * 0.835 - tw / 2, y + s * 0.695), label, font=f,
              fill=(255, 255, 255))


def icon_breach(draw, x, y, s):
    """Padlock with a crack: the CIA/ODNI breach."""
    # shackle
    draw.arc([x + s * 0.30, y + s * 0.06, x + s * 0.70, y + s * 0.46],
             180, 360, fill=INK, width=7)
    # body
    draw.rectangle([x + s * 0.20, y + s * 0.40, x + s * 0.80, y + s * 0.88],
                   fill=INK)
    # keyhole
    draw.ellipse([x + s * 0.45, y + s * 0.52, x + s * 0.55, y + s * 0.62],
                 fill=PAPER)
    draw.polygon([(x + s * 0.47, y + s * 0.60), (x + s * 0.53, y + s * 0.60),
                  (x + s * 0.56, y + s * 0.74), (x + s * 0.44, y + s * 0.74)],
                 fill=PAPER)
    # red crack across the body
    crack = [(x + s * 0.24, y + s * 0.44), (x + s * 0.38, y + s * 0.58),
             (x + s * 0.30, y + s * 0.66), (x + s * 0.48, y + s * 0.76),
             (x + s * 0.40, y + s * 0.86)]
    draw.line(crack, fill=RED, width=4, joint="curve")
    # radiating alarm lines
    for ang in (200, 250, 290, 340):
        a = math.radians(ang)
        cx, cy = x + s * 0.50, y + s * 0.30
        draw.line([(cx + s * 0.22 * math.cos(a), cy + s * 0.22 * math.sin(a)),
                   (cx + s * 0.32 * math.cos(a), cy + s * 0.32 * math.sin(a))],
                  fill=RED, width=3)


def icon_medal(draw, x, y, s):
    """A medal on its ribbon: the Medal of Freedom."""
    # ribbon (two bands)
    draw.polygon([(x + s * 0.36, y + s * 0.02), (x + s * 0.48, y + s * 0.02),
                  (x + s * 0.42, y + s * 0.42), (x + s * 0.30, y + s * 0.42)],
                 fill=RED)
    draw.polygon([(x + s * 0.52, y + s * 0.02), (x + s * 0.64, y + s * 0.02),
                  (x + s * 0.70, y + s * 0.42), (x + s * 0.58, y + s * 0.42)],
                 fill=BLUE)
    # medal disc
    cx, cy = x + s * 0.50, y + s * 0.66
    draw.ellipse([cx - s * 0.26, cy - s * 0.26, cx + s * 0.26, cy + s * 0.26],
                 fill=GOLD, outline=INK, width=2)
    draw.polygon(star_points(cx, cy, s * 0.18, s * 0.08), fill=PAPER)


def secondary(draw, x, y, w, icon, kicker, headline, deck):
    """One secondary story cell: icon left, text right."""
    s = 120
    icon(draw, x, y + 8, s)
    tx = x + s + 16
    tw = w - s - 16
    f_kick = font(SANS_B, 17)
    draw.text((tx, y + 4), kicker, font=f_kick, fill=RED)
    f_head = font(SERIF_B, 26)
    lines = wrap(draw, headline, f_head, tw)
    y2 = draw_lines(draw, lines[:2], tx, y + 28, f_head, leading=31)
    f_deck = font(SANS, 17)
    lines = wrap(draw, deck, f_deck, tw)
    draw_lines(draw, lines[:2], tx, y2 + 4, f_deck, fill=GRAY, leading=22)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 40  # margin
    RX = W - MX

    # ---- masthead ----
    rule(d, MX, 26, RX, 3)
    f_mast = font(SERIF_B, 82)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 36), title, font=f_mast, fill=INK)
    rule(d, MX, 138, RX, 5)
    rule(d, MX, 146, RX, 1)
    f_date = font(SANS_B, 20)
    d.text((MX, 158), "WEDNESDAY, 25 NOVEMBER 2026", font=f_date, fill=INK)
    right = "WORLD NEWS  ·  ONE PAGE"
    tw = d.textlength(right, font=f_date)
    d.text((RX - tw, 158), right, font=f_date, fill=INK)

    # ---- lead story: Houthi drone hits Riyadh's PIF Tower ----
    y = 196
    f_kick = font(SANS_B, 20)
    d.text((MX, y), "CONFLICT  —  RIYADH, SAUDI ARABIA", font=f_kick, fill=RED)
    y += 30
    f_head = font(SERIF_B, 60)
    d.text((MX, y), "DRONE STRIKES", font=f_head, fill=INK)
    y += 68
    d.text((MX, y), "RIYADH TOWER", font=f_head, fill=INK)
    y += 78
    # left column: deck + body; right column: tower visual
    text_w = 560
    f_deck = font(SERIF, 25)
    deck = ("A Houthi drone hit the kingdom's tallest tower — the "
            "Public Investment Fund Tower in Riyadh — wounding 11 "
            "in a second strike in under a week.")
    y2 = draw_lines(d, wrap(d, deck, f_deck, text_w), MX, y, f_deck, leading=32)
    f_body = font(SERIF, 19)
    body = ("The coalition vowed a decisive response after the "
            "attack on the King Abdullah Financial District.")
    draw_lines(d, wrap(d, body, f_body, text_w), MX, y2 + 14, f_body,
               fill=GRAY, leading=25)
    draw_tower(d, 800, y + 108, 150, 228)

    # ---- divider ----
    rule(d, MX, 600, RX, 3)

    # ---- secondary stories, 2 x 2 ----
    cell_w = (W - 2 * MX - 24) // 2
    cell_h = 158
    gx, gy = MX, 624
    secondary(d, gx, gy, cell_w, icon_cargo,
              "CONFLICT — GULF OF FINLAND",
              "Zelenskiy confirms Sparta II strike",
              "Ukraine says the ship carried weapons; Norway urges caution.")
    secondary(d, gx + cell_w + 24, gy, cell_w, icon_gavel,
              "COURTS — NEW YORK",
              "Huawei guilty on 10 of 12 counts",
              "Fraud and trade-secret theft proven; racketeering charge fails.")
    secondary(d, gx, gy + cell_h + 14, cell_w, icon_breach,
              "SECURITY — WASHINGTON",
              "CIA and ODNI hit by cyber breach",
              "Unclassified data exposed; classified systems said untouched.")
    secondary(d, gx + cell_w + 24, gy + cell_h + 14, cell_w, icon_medal,
              "POLITICS — WASHINGTON",
              "Trump gives Giuliani the Medal of Freedom",
              "The 82-year-old is the third to get the top honor this term.")

    # ---- footer ----
    rule(d, MX, 972, RX, 1)
    f_foot = font(SANS, 15)
    foot = "THE WORLD TODAY  ·  ALL FIVE STORIES FROM WEDNESDAY 25 NOVEMBER 2026  ·  DRAWN ENTIRELY IN CODE"
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, 982), foot, font=f_foot, fill=GRAY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
