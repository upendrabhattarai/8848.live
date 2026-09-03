#!/usr/bin/env python3
"""
Generate Open-Graph share images + standalone share pages for one digest post.

Usage:
    python3 generate_share_images.py <repo_root> <YYYY-MM-DD>

Produces, for a post at _posts/<date>-nepal-news-digest.md:
  assets/shares/<date>/wordcloud.png
  assets/shares/<date>/<outlet-slug>.png   (one per outlet-box)
  share/<date>/wordcloud/index.html
  share/<date>/<outlet-slug>/index.html

Each share/<date>/<target>/index.html is a standalone HTML page (no Jekyll
layout) carrying correct Open Graph / Twitter Card meta tags pointing at the
matching static PNG, plus an instant redirect to the real digest page for
human visitors. Facebook/Twitter/LinkedIn crawlers read the <head> tags
directly (they do not execute JS or follow the redirect), so the generated
image shows up automatically as the shared link's preview image.
"""
import html
import os
import re
import sys
import textwrap
import yaml
from PIL import Image, ImageDraw, ImageFont

SITE_URL = "https://8848.live"
W, H = 1200, 630
FONT_DIR = None  # set in main()

PALETTE = ['#dc143c', '#a50e2d', '#003893', '#0d9488', '#374151', '#b45309']
RED = '#dc143c'
RED_DARK = '#a50e2d'
INK = '#111827'
INK_2 = '#374151'
INK_3 = '#6b7280'
BG = '#ffffff'
BG_SOFT = '#fff5f6'
BORDER = '#f0d7db'


def slugify(s):
    s = (s or 'outlet').strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-') or 'outlet'


def has_devanagari(text):
    return any('ऀ' <= ch <= 'ॿ' for ch in text)


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    try:
        axes = f.get_variation_axes()
        names = [a['name'] for a in axes]
        if weight and b'Weight' in names:
            # keep other axes at default, set Weight
            vals = []
            for a in axes:
                if a['name'] == b'Weight':
                    vals.append(weight)
                else:
                    vals.append(a['default'])
            f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f


def pick_font(text, size, weight=700):
    path = os.path.join(FONT_DIR, 'NotoSansDevanagari.ttf') if has_devanagari(text) else os.path.join(FONT_DIR, 'Inter.ttf')
    return font(path, size, weight)


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


def draw_wordmark(draw, x, y):
    f = font(os.path.join(FONT_DIR, 'Inter.ttf'), 30, 800)
    draw.text((x, y), '8848.live', font=f, fill=RED)


def draw_footer_tag(draw, text, x, y):
    f = font(os.path.join(FONT_DIR, 'Inter.ttf'), 22, 600)
    draw.text((x, y), text, font=f, fill=INK_3)


# ---------------------------------------------------------------------------

def generate_wordcloud_image(words, out_path, date_label):
    from wordcloud import WordCloud
    import random

    if not words:
        words = [('8848.live', 10)]
    freqs = {w['word']: w['count'] for w in words[:60]}

    font_path = os.path.join(FONT_DIR, 'NotoSansDevanagari.ttf')

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(PALETTE)

    wc = WordCloud(
        width=W, height=420,
        background_color=BG,
        font_path=font_path,
        color_func=color_func,
        prefer_horizontal=0.92,
        margin=4,
        max_words=60,
        relative_scaling=0.55,
    ).generate_from_frequencies(freqs)

    cloud_img = wc.to_image().convert('RGB')

    canvas = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, W, 8], fill=RED)

    draw_wordmark(draw, 44, 34)
    hf = font(os.path.join(FONT_DIR, 'Inter.ttf'), 26, 600)
    draw.text((44, 82), "Today's buzzwords from Nepal's headlines", font=hf, fill=INK_2)

    canvas.paste(cloud_img, (0, 150))

    draw_footer_tag(draw, date_label, 44, H - 56)
    canvas.save(out_path, 'PNG')


def generate_outlet_card(outlet_name, headlines, out_path, date_label):
    canvas = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # top accent bar
    draw.rectangle([0, 0, W, 10], fill=RED)

    pad = 56
    draw_wordmark(draw, pad, 36)
    tagf = font(os.path.join(FONT_DIR, 'Inter.ttf'), 22, 600)
    draw.text((W - pad - draw.textlength("TOP HEADLINES TODAY", font=tagf), 42),
               "TOP HEADLINES TODAY", font=tagf, fill=INK_3)

    # outlet name
    name_font = pick_font(outlet_name, 52, 800)
    draw.text((pad, 96), outlet_name, font=name_font, fill=INK)
    draw.line([(pad, 168), (W - pad, 168)], fill=BORDER, width=2)

    y = 196
    max_w = W - pad * 2 - 40
    item_font_size = 30
    for i, headline in enumerate(headlines[:4]):
        headline = headline.strip()
        if not headline:
            continue
        hfnt = pick_font(headline, item_font_size, 600)
        num_f = font(os.path.join(FONT_DIR, 'Inter.ttf'), item_font_size, 800)
        num = f"{i+1}"
        draw.text((pad, y), num, font=num_f, fill=RED)
        lines = wrap_to_width(draw, headline, hfnt, max_w)[:2]
        for j, line in enumerate(lines):
            if j == 1 and len(lines) == 2 and line != lines[-1]:
                pass
            draw.text((pad + 46, y + j * 40), line, font=hfnt, fill=INK)
        y += max(1, len(lines)) * 40 + 20
        if y > H - 90:
            break

    draw_footer_tag(draw, f"Daily digest · {date_label}", pad, H - 56)
    canvas.save(out_path, 'PNG')


# ---------------------------------------------------------------------------

def parse_post(md_path):
    raw = open(md_path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.DOTALL)
    if not m:
        raise SystemExit(f'No front matter found in {md_path}')
    front = yaml.safe_load(m.group(1))
    body = m.group(2)

    words = front.get('wordcloud') or []

    outlets = []
    for box_html in re.split(r'(?=<div class="outlet-box)', body):
        if '<div class="outlet-box' not in box_html:
            continue
        # New (category-digest) format nests bilingual spans inside outlet-name,
        # e.g. <span class="outlet-name"><span data-lang-en>X</span><span data-lang-np>Y</span></span>
        # -- prefer the English variant for the slug/title. Old (outlet-digest)
        # format has plain text directly inside outlet-name -- still supported.
        name_m = re.search(r'<span class="outlet-name">\s*<span data-lang-en>([^<]+)</span>', box_html, re.DOTALL)
        if not name_m:
            name_m = re.search(r'<span class="outlet-name">([^<]+)</span>', box_html)
        if not name_m:
            continue
        name = html.unescape(name_m.group(1).strip())
        heads = re.findall(r'<strong>(.*?)</strong>', box_html, re.DOTALL)
        heads = [html.unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in heads]
        outlets.append({'name': name, 'headlines': heads})

    return front, words, outlets


SHARE_PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta property="og:type" content="article">
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
<p>Redirecting to <a href="{redirect}">the full digest</a>&hellip;</p>
<script>setTimeout(function () {{ location.replace({redirect_js}); }}, 300);</script>
</body>
</html>
"""


def write_share_page(out_path, title, description, image_url, page_url, redirect_url):
    import json
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
    global FONT_DIR
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    repo_root, date = sys.argv[1], sys.argv[2]
    FONT_DIR = os.path.join(repo_root, 'assets', 'fonts')

    md_path = os.path.join(repo_root, '_posts', f'{date}-nepal-news-digest.md')
    front, words, outlets = parse_post(md_path)
    title_full = front.get('title', 'Nepal News Digest')
    date_label = title_full.split(':', 1)[-1].strip() if ':' in title_full else date
    post_url = f"{SITE_URL}/{date[0:4]}/{date[5:7]}/{date[8:10]}/nepal-news-digest/"

    img_dir = os.path.join(repo_root, 'assets', 'shares', date)
    share_dir = os.path.join(repo_root, 'share', date)
    os.makedirs(img_dir, exist_ok=True)

    # --- word cloud ---
    wc_img_path = os.path.join(img_dir, 'wordcloud.png')
    generate_wordcloud_image(words, wc_img_path, date_label)
    wc_image_url = f"{SITE_URL}/assets/shares/{date}/wordcloud.png"
    write_share_page(
        os.path.join(share_dir, 'wordcloud', 'index.html'),
        title=f"Today's buzzwords — {title_full}",
        description="See what words defined today's Nepali news headlines, via 8848.live.",
        image_url=wc_image_url,
        page_url=f"{SITE_URL}/share/{date}/wordcloud/",
        redirect_url=post_url + '#wordcloud',
    )
    print(f"wrote {wc_img_path}")

    # --- outlet cards ---
    for outlet in outlets:
        slug = slugify(outlet['name'])
        card_path = os.path.join(img_dir, f'{slug}.png')
        generate_outlet_card(outlet['name'], outlet['headlines'], card_path, date_label)
        card_image_url = f"{SITE_URL}/assets/shares/{date}/{slug}.png"
        write_share_page(
            os.path.join(share_dir, slug, 'index.html'),
            title=f"{outlet['name']} — top headlines, {date_label}",
            description=f"Today's top headlines from {outlet['name']}, via 8848.live.",
            image_url=card_image_url,
            page_url=f"{SITE_URL}/share/{date}/{slug}/",
            redirect_url=post_url + f'#outlet-{slug}',
        )
        print(f"wrote {card_path}")


if __name__ == '__main__':
    main()
