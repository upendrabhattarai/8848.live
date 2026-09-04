#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Open-Graph share images + standalone share pages for the site's
evergreen, non-date-based sections: the two Visual Nepal maps and the Date
Converter. Unlike generate_share_images.py (which runs once per day for
that day's digest), this script produces static assets that don't change
day to day, so it's run once (or re-run only when the target page's copy
changes) rather than as part of the daily pipeline.

Produces:
  assets/shares/visual-nepal/flash-flood.png
  assets/shares/visual-nepal/waters.png
  assets/shares/date-converter.png
  share/visual-nepal/flash-flood/index.html
  share/visual-nepal/waters/index.html
  share/date-converter/index.html

Usage: python3 generate_static_shares.py <repo_root>
"""
import html
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

SITE_URL = "https://8848.live"
W, H = 1200, 630

RED = '#dc143c'
RED_DARK = '#a50e2d'
BLUE = '#003893'
TEAL = '#0d9488'
INK = '#111827'
INK_2 = '#374151'
INK_3 = '#6b7280'
BG = '#ffffff'
BORDER = '#f0d7db'


def font(font_dir, name, size, weight=None):
    f = ImageFont.truetype(os.path.join(font_dir, name), size)
    try:
        axes = f.get_variation_axes()
        names = [a['name'] for a in axes]
        if weight and b'Weight' in names:
            vals = []
            for a in axes:
                vals.append(weight if a['name'] == b'Weight' else a['default'])
            f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f


def wrap_to_width(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wordmark(draw, font_dir, x, y):
    f = font(font_dir, 'Inter.ttf', 30, 800)
    draw.text((x, y), '8848.live', font=f, fill=RED)


def draw_footer_tag(draw, font_dir, text, x, y, color=INK_3):
    f = font(font_dir, 'Inter.ttf', 22, 600)
    draw.text((x, y), text, font=f, fill=color)


def generate_map_card(font_dir, out_path, accent, eyebrow, title_lines, subtitle, tag_text):
    canvas = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, W, 10], fill=accent)

    pad = 64
    draw_wordmark(draw, font_dir, pad, 40)

    eyebrow_f = font(font_dir, 'Inter.ttf', 22, 700)
    draw.text((pad, 108), eyebrow.upper(), font=eyebrow_f, fill=accent)

    title_f = font(font_dir, 'Inter.ttf', 68, 800)
    y = 150
    for line in title_lines:
        draw.text((pad, y), line, font=title_f, fill=INK)
        y += 82

    draw.line([(pad, y + 10), (W - pad, y + 10)], fill=BORDER, width=2)

    sub_f = font(font_dir, 'Inter.ttf', 30, 500)
    sub_lines = wrap_to_width(draw, subtitle, sub_f, W - pad * 2)
    sy = y + 44
    for line in sub_lines[:3]:
        draw.text((pad, sy), line, font=sub_f, fill=INK_2)
        sy += 42

    draw_footer_tag(draw, font_dir, tag_text, pad, H - 60)
    canvas.save(out_path, 'PNG')


def generate_date_converter_card(font_dir, out_path):
    canvas = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, W, 10], fill=RED)

    pad = 64
    draw_wordmark(draw, font_dir, pad, 40)

    eyebrow_f = font(font_dir, 'Inter.ttf', 22, 700)
    draw.text((pad, 108), 'AD ↔ BS CALENDAR TOOL', font=eyebrow_f, fill=RED)

    title_f = font(font_dir, 'Inter.ttf', 68, 800)
    draw.text((pad, 150), 'Date Converter', font=title_f, fill=INK)

    # Example conversion, styled like two chips joined by the swap arrow --
    # mirrors the actual on-page converter's look and feel.
    chip_f = font(font_dir, 'Inter.ttf', 34, 700)
    label_f = font(font_dir, 'Inter.ttf', 20, 700)
    cy = 300
    chip_h = 92
    chip_w = 430

    def chip(x, label, value, color):
        draw.rounded_rectangle([x, cy, x + chip_w, cy + chip_h], radius=16, outline=color, width=2)
        draw.text((x + 24, cy + 14), label.upper(), font=label_f, fill=color)
        draw.text((x + 24, cy + 44), value, font=chip_f, fill=INK)

    chip(pad, 'English (AD)', 'September 1, 2026', BLUE)

    # Drawn by hand rather than a Unicode arrow glyph -- some fonts render
    # U+21C4 (⇄) as tofu/garbled at this size, a plain line+triangle pair
    # always renders correctly regardless of font glyph coverage.
    ax = pad + chip_w + 30
    aw = 60
    amidy = cy + chip_h // 2
    draw.line([(ax, amidy - 8), (ax + aw, amidy - 8)], fill=INK_3, width=4)
    draw.polygon([(ax + aw, amidy - 16), (ax + aw + 14, amidy - 8), (ax + aw, amidy)], fill=INK_3)
    draw.line([(ax + aw + 14, amidy + 8), (ax, amidy + 8)], fill=INK_3, width=4)
    draw.polygon([(ax, amidy), (ax - 14, amidy + 8), (ax, amidy + 16)], fill=INK_3)

    chip(pad + chip_w + 90, 'Bikram Sambat', 'Bhadra 16, 2083', RED)

    sub_f = font(font_dir, 'Inter.ttf', 28, 500)
    draw.text((pad, cy + chip_h + 40),
               'Convert any date between the English and Nepali calendars, instantly.',
               font=sub_f, fill=INK_2)

    draw_footer_tag(draw, font_dir, 'Free tool · 8848.live', pad, H - 60)
    canvas.save(out_path, 'PNG')


SHARE_PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{image}">
<meta property="og:image:secure_url" content="{image}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{page_url}">
<meta property="og:site_name" content="8848.live">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">
<link rel="canonical" href="{redirect}">
</head>
<body>
<p>Redirecting to <a href="{redirect}">8848.live</a>&hellip;</p>
<script>setTimeout(function () {{ location.replace({redirect_js}); }}, 300);</script>
</body>
</html>
"""


def write_share_page(out_path, title, description, image_url, page_url, redirect_url):
    content = SHARE_PAGE_TMPL.format(
        redirect=html.escape(redirect_url, quote=True),
        title=html.escape(title, quote=True),
        description=html.escape(description, quote=True),
        image=html.escape(image_url, quote=True),
        page_url=html.escape(page_url, quote=True),
        redirect_js=json.dumps(redirect_url),
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    repo_root = sys.argv[1]
    font_dir = os.path.join(repo_root, 'assets', 'fonts')

    img_dir = os.path.join(repo_root, 'assets', 'shares', 'visual-nepal')
    os.makedirs(img_dir, exist_ok=True)

    # --- Flash flood card ---
    generate_map_card(
        font_dir,
        os.path.join(img_dir, 'flash-flood.png'),
        accent=RED,
        eyebrow='Visual Nepal · Interactive Map',
        title_lines=['Rasuwa–Bhotekoshi', 'Flash Flood, Aug 2026'],
        subtitle='Flow path, modelled inundation extent, and infrastructure damage — mapped on satellite imagery.',
        tag_text='8848.live/visual-nepal',
    )
    write_share_page(
        os.path.join(repo_root, 'share', 'visual-nepal', 'flash-flood', 'index.html'),
        title='Rasuwa–Bhotekoshi Flash Flood, Aug 2026 — Visual Nepal',
        description="The flood's flow path, modelled inundation extent, and infrastructure damage, mapped on satellite imagery, via 8848.live.",
        image_url=f'{SITE_URL}/assets/shares/visual-nepal/flash-flood.png',
        page_url=f'{SITE_URL}/share/visual-nepal/flash-flood/',
        redirect_url=f'{SITE_URL}/visual-nepal/rasuwa-bhotekoshi-flash-flood/',
    )

    # --- Waters of Nepal card ---
    generate_map_card(
        font_dir,
        os.path.join(img_dir, 'waters.png'),
        accent=BLUE,
        eyebrow='Visual Nepal · Interactive Map',
        title_lines=['The Waters of Nepal'],
        subtitle="A live satellite basemap of Nepal's glaciers, lakes, and rivers.",
        tag_text='8848.live/visual-nepal',
    )
    write_share_page(
        os.path.join(repo_root, 'share', 'visual-nepal', 'waters', 'index.html'),
        title='The Waters of Nepal — Visual Nepal',
        description="A live satellite basemap of Nepal's glaciers, lakes, and rivers, via 8848.live.",
        image_url=f'{SITE_URL}/assets/shares/visual-nepal/waters.png',
        page_url=f'{SITE_URL}/share/visual-nepal/waters/',
        redirect_url=f'{SITE_URL}/visual-nepal/waters-of-nepal-map/',
    )

    # --- Nepal in Relief card ---
    generate_map_card(
        font_dir,
        os.path.join(img_dir, 'nepal-in-relief.png'),
        accent=TEAL,
        eyebrow='Visual Nepal · Elevation Atlas',
        title_lines=['Nepal in Relief'],
        subtitle='A province-by-province elevation atlas — hillshaded relief and terrain for all seven provinces.',
        tag_text='8848.live/visual-nepal',
    )
    write_share_page(
        os.path.join(repo_root, 'share', 'visual-nepal', 'nepal-in-relief', 'index.html'),
        title='Nepal in Relief — Visual Nepal',
        description='Nepal: A Province-by-Province Elevation Atlas — hillshaded relief maps, elevation profiles, and terrain for all seven provinces, via 8848.live.',
        image_url=f'{SITE_URL}/assets/shares/visual-nepal/nepal-in-relief.png',
        page_url=f'{SITE_URL}/share/visual-nepal/nepal-in-relief/',
        redirect_url=f'{SITE_URL}/visual-nepal/nepal-in-relief/',
    )

    # --- Date converter card ---
    generate_date_converter_card(font_dir, os.path.join(repo_root, 'assets', 'shares', 'date-converter.png'))
    write_share_page(
        os.path.join(repo_root, 'share', 'date-converter', 'index.html'),
        title='Date Converter (AD ↔ BS) — 8848.live',
        description='Convert between the English (AD) and Nepali Bikram Sambat (BS) calendars, and browse both side by side.',
        image_url=f'{SITE_URL}/assets/shares/date-converter.png',
        page_url=f'{SITE_URL}/share/date-converter/',
        redirect_url=f'{SITE_URL}/date-converter/',
    )

    print('Done. Wrote:')
    print(' ', os.path.join(img_dir, 'flash-flood.png'))
    print(' ', os.path.join(img_dir, 'waters.png'))
    print(' ', os.path.join(img_dir, 'nepal-in-relief.png'))
    print(' ', os.path.join(repo_root, 'assets', 'shares', 'date-converter.png'))
    print('  share/visual-nepal/flash-flood/index.html')
    print('  share/visual-nepal/waters/index.html')
    print('  share/visual-nepal/nepal-in-relief/index.html')
    print('  share/date-converter/index.html')


if __name__ == '__main__':
    main()
