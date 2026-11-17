#!/usr/bin/env python3
"""Build the entry poster for 17 November 2026 world news.

Draws the whole front page in code (Pillow) so every letter is
pixel-perfect: no generated text anywhere. Run: python3 build_poster.py
Writes entry.png (1024x1024) next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 234)      # cream newsprint
INK = (20, 32, 46)           # near-black navy
RED = (179, 39, 30)          # masthead red
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
MUTED = (90, 96, 104)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_DATE = font("DejaVuSans-Bold.ttf", 62)
F_MAST = font("DejaVuSans-Bold.ttf", 26)
F_TAG = font("DejaVuSans.ttf", 21)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
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


def draw_bridge(d, cx, cy, s, col):
    """A bridge with a broken, falling middle span."""
    y = cy + 6 * s
    d.line([(cx - 34 * s, y), (cx - 10 * s, y)], fill=col, width=int(5 * s))
    d.line([(cx + 10 * s, y), (cx + 34 * s, y)], fill=col, width=int(5 * s))
    for tx in (-26 * s, 26 * s):
        d.line([(tx, y), (tx, y - 26 * s)], fill=col, width=int(4 * s))
        d.line([(tx - 8 * s, y - 26 * s), (tx + 8 * s, y - 26 * s)],
               fill=col, width=int(3 * s))
    d.line([(cx - 10 * s, y), (cx - 2 * s, y + 12 * s)], fill=col,
           width=int(4 * s))
    d.line([(cx + 10 * s, y), (cx + 2 * s, y + 12 * s)], fill=col,
           width=int(4 * s))
    for wx in range(-34, 35, 12):
        d.arc([cx + wx * s, y + 16 * s, cx + (wx + 10) * s, y + 24 * s],
              0, 180, fill=col, width=int(2 * s))


def draw_tanker(d, cx, cy, s, col):
    """An oil tanker with a small flame and waves."""
    d.polygon([(cx - 34 * s, cy - 2 * s), (cx + 34 * s, cy - 2 * s),
               (cx + 26 * s, cy + 14 * s), (cx - 26 * s, cy + 14 * s)],
              fill=col)
    d.rectangle([cx + 8 * s, cy - 16 * s, cx + 24 * s, cy - 2 * s], fill=col)
    d.polygon([(cx - 20 * s, cy - 22 * s), (cx - 12 * s, cy - 34 * s),
               (cx - 4 * s, cy - 22 * s)], fill=(230, 120, 30))
    d.polygon([(cx - 16 * s, cy - 22 * s), (cx - 12 * s, cy - 28 * s),
               (cx - 8 * s, cy - 22 * s)], fill=(245, 200, 60))
    for wx in range(-34, 35, 12):
        d.arc([cx + wx * s, cy + 18 * s, cx + (wx + 10) * s, cy + 26 * s],
              0, 180, fill=col, width=int(2 * s))


def draw_flags(d, cx, cy, s, col):
    """Three small summit flags: US, China, Russia (simplified)."""
    for i, (fx, flag) in enumerate([(-26, "us"), (0, "cn"), (26, "ru")]):
        x = cx + fx * s
        d.line([(x, cy - 30 * s), (x, cy + 28 * s)], fill=col,
               width=int(3 * s))
        if flag == "us":
            for j in range(4):
                d.rectangle([x, cy - 30 * s + j * 6 * s,
                             x + 16 * s, cy - 30 * s + (j + 1) * 6 * s],
                            fill=RED if j % 2 == 0 else (255, 255, 255))
            d.rectangle([x, cy - 30 * s, x + 8 * s, cy - 18 * s],
                        fill=(30, 60, 120))
        elif flag == "cn":
            d.rectangle([x, cy - 30 * s, x + 16 * s, cy - 6 * s],
                        fill=(200, 30, 30))
            d.ellipse([x + 3 * s, cy - 27 * s, x + 8 * s, cy - 22 * s],
                      fill=(250, 220, 60))
        else:
            d.rectangle([x, cy - 30 * s, x + 16 * s, cy - 22 * s],
                        fill=(255, 255, 255))
            d.rectangle([x, cy - 22 * s, x + 16 * s, cy - 14 * s],
                        fill=(30, 60, 160))
            d.rectangle([x, cy - 14 * s, x + 16 * s, cy - 6 * s],
                        fill=(200, 30, 30))


def draw_building(d, cx, cy, s, col):
    """A government building with columns and a pediment."""
    d.polygon([(cx - 30 * s, cy - 14 * s), (cx, cy - 30 * s),
               (cx + 30 * s, cy - 14 * s)], fill=col)
    for i in range(-2, 3):
        x = cx + i * 12 * s
        d.rectangle([x - 3 * s, cy - 12 * s, x + 3 * s, cy + 16 * s],
                    fill=col)
    d.rectangle([cx - 34 * s, cy + 16 * s, cx + 34 * s, cy + 22 * s],
                fill=col)
    d.rectangle([cx - 38 * s, cy + 22 * s, cx + 38 * s, cy + 28 * s],
                fill=col)


def draw_jet(d, cx, cy, s, col):
    """A fighter jet seen from above, with an alert mark."""
    d.polygon([(cx, cy - 30 * s), (cx + 6 * s, cy + 6 * s),
               (cx + 4 * s, cy + 26 * s), (cx - 4 * s, cy + 26 * s),
               (cx - 6 * s, cy + 6 * s)], fill=col)
    d.polygon([(cx - 6 * s, cy + 2 * s), (cx - 30 * s, cy + 16 * s),
               (cx - 28 * s, cy + 22 * s), (cx - 4 * s, cy + 12 * s)],
              fill=col)
    d.polygon([(cx + 6 * s, cy + 2 * s), (cx + 30 * s, cy + 16 * s),
               (cx + 28 * s, cy + 22 * s), (cx + 4 * s, cy + 12 * s)],
              fill=col)
    d.polygon([(cx - 4 * s, cy + 22 * s), (cx - 12 * s, cy + 30 * s),
               (cx - 8 * s, cy + 30 * s), (cx - 2 * s, cy + 26 * s)],
              fill=col)
    d.polygon([(cx + 4 * s, cy + 22 * s), (cx + 12 * s, cy + 30 * s),
               (cx + 8 * s, cy + 30 * s), (cx + 2 * s, cy + 26 * s)],
              fill=col)
    d.ellipse([cx + 18 * s, cy - 34 * s, cx + 34 * s, cy - 18 * s],
              fill=RED)
    d.text((cx + 26 * s, cy - 33 * s), "!", font=font("DejaVuSans-Bold.ttf",
           int(14 * s)), fill=(255, 255, 255), anchor="mm")


def draw_scales(d, cx, cy, s, col):
    """Scales of justice for sanctions."""
    d.line([(cx, cy - 28 * s), (cx, cy + 28 * s)], fill=col,
           width=int(4 * s))
    d.line([(cx - 28 * s, cy - 20 * s), (cx + 28 * s, cy - 20 * s)],
           fill=col, width=int(4 * s))
    d.ellipse([cx - 4 * s, cy - 32 * s, cx + 4 * s, cy - 24 * s], fill=col)
    for side in (-1, 1):
        px = cx + side * 28 * s
        d.line([(px, cy - 20 * s), (px - 10 * s, cy + 2 * s)], fill=col,
               width=int(2 * s))
        d.line([(px, cy - 20 * s), (px + 10 * s, cy + 2 * s)], fill=col,
               width=int(2 * s))
        d.arc([px - 12 * s, cy - 2 * s, px + 12 * s, cy + 14 * s], 0, 180,
              fill=col, width=int(3 * s))
    d.rectangle([cx - 16 * s, cy + 26 * s, cx + 16 * s, cy + 30 * s],
                fill=col)


ICONS = {"bridge": draw_bridge, "tanker": draw_tanker,
         "flags": draw_flags, "building": draw_building,
         "jet": draw_jet, "scales": draw_scales}

# Six stories, all events of Tuesday 17 November 2026 as reported that
# day (BBC, Reuters, Associated Press, Al Jazeera).
STORIES = [
    ("bridge", "UKRAINE  ·  WAR", (179, 39, 30),
     "Kerch Bridge span collapses after Ukrainian strike",
     "A road section falls into the sea; Russia hits Kyiv's river bridges in reply."),
    ("tanker", "THE GULF  ·  SHIPPING", (15, 90, 110),
     "Tankers hit mines near the Strait of Hormuz",
     "Two ships catch fire; Iran fires drones at a US base in Bahrain; a third US carrier arrives."),
    ("flags", "ASIA  ·  DIPLOMACY", (122, 90, 18),
     "Trump lands in Manila for ASEAN summit",
     "Xi, Trump and Putin are set to meet in Shenzhen on Thursday for talks on peace and trade."),
    ("building", "MONGOLIA  ·  POLITICS", (46, 107, 52),
     "President says he will resign",
     "Khurelsukh steps down amid claims over a railway deal he denies; he vows to cooperate."),
    ("jet", "JAPAN  ·  SECURITY", (91, 46, 122),
     "Jets scramble as Russian planes enter airspace",
     "Tokyo launches fighters and lodges a strong protest with Moscow."),
    ("scales", "WEST BANK  ·  SANCTIONS", (138, 75, 0),
     "UK sanctions settlement builders",
     "Britain blacklists eight Israeli construction firms building in the occupied West Bank."),
]


def fit_font(name, start, text, max_w, draw):
    """Largest font size at which text fits max_w."""
    size = start
    while size > 10:
        fnt = font(name, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(name, 10)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # page margin

    # --- Masthead -------------------------------------------------------
    d.text((W // 2, 52), "THE WORLD IN ONE DAY", font=F_MAST, fill=INK,
           anchor="mm")
    d.line([(mx, 82), (W - mx, 82)], fill=RED, width=4)
    date_font = fit_font("DejaVuSans-Bold.ttf", 62,
                         "TUESDAY, 17 NOVEMBER 2026", W - 2 * mx - 8, d)
    d.text((W // 2, 128), "TUESDAY, 17 NOVEMBER 2026", font=date_font,
           fill=RED, anchor="mm")
    d.line([(mx, 168), (W - mx, 168)], fill=INK, width=2)
    d.text((W // 2, 196), "Six stories that defined the day",
           font=F_TAG, fill=MUTED, anchor="mm")

    # --- Story grid: 2 columns x 3 rows --------------------------------
    gx, gy = mx, 226
    gw, gh = (W - 2 * mx - 24) // 2, 236
    gap = 24
    for i, (icon, kicker, color, head, body) in enumerate(STORIES):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + 18)
        d.rounded_rectangle([x, y, x + gw, y + gh], radius=10,
                            fill=CARD, outline=BORDER, width=2)
        d.line([(x + 20, y + 14), (x + 20, y + gh - 14)], fill=color,
               width=5)
        # icon badge
        bx, by, br = x + 58, y + 52, 40
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=color)
        ICONS[icon](d, bx, by, 0.85, (255, 255, 255))
        # kicker + headline + body
        tx = x + 116
        d.text((tx, y + 26), kicker, font=F_KICK, fill=color)
        hy = y + 56
        for line in wrap(d, head, F_HEAD, gw - 136):
            d.text((tx, hy), line, font=F_HEAD, fill=INK)
            hy += 32
        by2 = hy + 10
        for line in wrap(d, body, F_BODY, gw - 136):
            d.text((tx, by2), line, font=F_BODY, fill=(60, 66, 74))
            by2 += 24

    # --- Footer ---------------------------------------------------------
    fy = gy + 3 * gh + 2 * 18 + 12
    d.line([(mx, fy), (W - mx, fy)], fill=BORDER, width=2)
    d.text((W // 2, fy + 18),
           "As reported on 17 November 2026  ·  Sources: BBC · Reuters · "
           "Associated Press · Al Jazeera",
           font=F_FOOT, fill=MUTED, anchor="mm")
    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
