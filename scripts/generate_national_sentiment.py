#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the "National Sentiment Quantified" gauge shown on the homepage,
next to the Latest digest card.

Method: AFINN 2-gram (bigram, negation-aware) sentiment scoring, per Chapter 8.3
of "Text Mining for Social and Behavioral Research Using R"
(https://books.psychstat.org/textmining/sentiment-analysis.html), applied to
that day's national-category headlines from three English-language outlets
(The Kathmandu Post, The Annapurna Express, myRepublica).

INPUT (produced upstream, once per day, by classifying that day's national
headlines from the three outlets into the unified national categories):
  <repo_root>/data/national-sentiment/<date>.csv
  columns: outlet, unified_category, headline

OUTPUT:
  data/national-sentiment/history.csv                             (running day-over-day log)
  assets/shares/<date>/national-sentiment-today-light.png         (on-page gauge, light theme, transparent bg)
  assets/shares/<date>/national-sentiment-today-dark.png          (on-page gauge, dark theme, transparent bg)
  assets/shares/<date>/national-sentiment.png                     (1200x630 share/OG image, framed, unchanged)
  share/<date>/national-sentiment/index.html                      (share page w/ OG tags)

Usage: python3 generate_national_sentiment.py <repo_root> <YYYY-MM-DD>
"""
import csv
import html
import os
import re
import sys
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

try:
    from afinn import Afinn
except ImportError:
    print("Missing dependency: pip install afinn --break-system-packages")
    sys.exit(1)

SITE_URL = "https://8848.live"

NATIONAL_CATS = {
    "Opinion & Editorial", "Business & Economy", "Entertainment, Lifestyle & Culture",
    "Environment & Weather", "National & Society", "Health",
    "Interviews & Features", "Diaspora",
}

NEGATIVE_WORDS = {
    "no", "not", "never", "dont", "don't", "cannot", "can't", "won't",
    "wouldn't", "shouldn't", "aren't", "isn't", "wasn't", "weren't",
    "haven't", "hasn't", "hadn't", "doesn't", "didn't", "mightn't", "mustn't",
}
TOKEN_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


def headline_sentiment_2gram(headline, afinn_dict):
    tokens = tokenize(headline)
    total = 0
    for word1, word2 in zip(tokens, tokens[1:]):
        if word2 in afinn_dict:
            score = afinn_dict[word2]
            total += -score if word1 in NEGATIVE_WORDS else score
    return total


# ---------------------------------------------------------------------------
# Gauge rendering (design: gold-framed card, red->grey->green translucent
# band, tapered needle that vanishes under a small "NET SCORE" box)
# ---------------------------------------------------------------------------
GAUGE_MIN, GAUGE_MAX = -3, 3
MONO = "monospace"
INK = "#1f2933"
GOLD = "#b45309"
CRIMSON = "#dc143c"
PAPER = "#fffaf4"
CMAP = LinearSegmentedColormap.from_list("sentiment", ["#e5484d", "#ffffff", "#2fbf71"], N=256)


def curved_text(ax, text, start_angle_deg, direction, radius, fontsize, deg_per_char, color, weight="bold"):
    for i, ch in enumerate(text):
        theta = start_angle_deg + direction * i * deg_per_char
        rad = np.radians(theta)
        x, y = radius * np.cos(rad), radius * np.sin(rad)
        ax.text(x, y, ch, fontsize=fontsize, fontfamily=MONO, fontweight=weight,
                 color=color, ha="center", va="center", rotation=theta - 90,
                 rotation_mode="anchor")


def draw_gauge(ax, value, caption=None, no_data=False, theme="light", frame=True, score_box=True):
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-0.55, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")

    # Theme-aware ink: the outer frame + cream background used to make these
    # legible against *any* surface, but that baked-in whitish card is what
    # we're removing (the gauge now renders transparent so the surrounding
    # page/card supplies the background) -- so the fine text needs its own
    # light/dark variant to stay readable against a light or dark card.
    if theme == "dark":
        ink = "#e5e7eb"
        neg_c, neu_c, pos_c = "#ff8a8a", "#c3c9d4", "#5ee69a"
        score_pos, score_neg, score_neu = "#5ee69a", "#ff8a8a", "#c3c9d4"
        nodata_ink = "#c3c9d4"
    else:
        ink = INK
        neg_c, neu_c, pos_c = "#a5303a", "#5b6472", "#1e7a4c"
        score_pos, score_neg, score_neu = "#2fbf71", "#e5484d", "#5b6472"
        nodata_ink = "#6b7280"

    if frame:
        gauge_frame = mpatches.FancyBboxPatch(
            (-1.28, -0.5), 2.56, 1.9, boxstyle="round,pad=0.02,rounding_size=0.06",
            linewidth=1.4, edgecolor=GOLD, facecolor=PAPER, alpha=(0.55 if no_data else 0.9), zorder=0
        )
        ax.add_patch(gauge_frame)

    n_seg, thickness, r_outer = 180, 0.30, 1.0
    band_alpha = 0.25 if no_data else 0.72
    for i in range(n_seg):
        t0, t1 = i / n_seg, (i + 1) / n_seg
        theta0, theta1 = 180 - t0 * 180, 180 - t1 * 180
        color = CMAP(0.5 * (t0 + t1))
        ax.add_patch(mpatches.Wedge((0, 0), r_outer, theta1, theta0, width=thickness,
                                     facecolor=color, edgecolor="none", alpha=band_alpha, zorder=1))
    for r in (r_outer + 0.012, r_outer - thickness - 0.012):
        ax.add_patch(mpatches.Arc((0, 0), 2 * r, 2 * r, angle=0, theta1=0, theta2=180,
                                   edgecolor=GOLD, linewidth=1.1, alpha=0.4 if no_data else 0.55, zorder=2))
    for tick_deg in range(0, 181, 30):
        rad = np.radians(tick_deg)
        x0, y0 = (r_outer - thickness - 0.03) * np.cos(rad), (r_outer - thickness - 0.03) * np.sin(rad)
        x1, y1 = (r_outer + 0.05) * np.cos(rad), (r_outer + 0.05) * np.sin(rad)
        ax.plot([x0, x1], [y0, y1], color=GOLD, linewidth=1.0, alpha=0.35 if no_data else 0.6, zorder=2)

    curved_text(ax, "NEGATIVE", 176, -1, 1.16, 9.5, 3.3, neg_c)
    curved_text(ax, "NEUTRAL", 99.9, -1, 1.16, 9.5, 3.3, neu_c)
    curved_text(ax, "POSITIVE", 27.1, -1, 1.16, 9.5, 3.3, pos_c)
    ax.text(-1.09, 0.05, "-3", fontsize=10.5, fontfamily=MONO, fontweight="bold", color=neg_c, ha="center", va="center", zorder=6)
    ax.text(0, 1.10, "0", fontsize=10.5, fontfamily=MONO, fontweight="bold", color=neu_c, ha="center", va="center", zorder=6)
    ax.text(1.09, 0.05, "+3", fontsize=10.5, fontfamily=MONO, fontweight="bold", color=pos_c, ha="center", va="center", zorder=6)

    if no_data:
        ax.add_patch(plt.Circle((0, 0), 0.09, facecolor="#9aa5b1", edgecolor=GOLD, linewidth=1.2, zorder=4))
        ax.add_patch(plt.Circle((0, 0), 0.035, facecolor=GOLD, zorder=4))
        if score_box:
            box = mpatches.FancyBboxPatch((-0.5, 0.19), 1.0, 0.21, boxstyle="round,pad=0.0,rounding_size=0.045",
                                           linewidth=1.1, edgecolor="#9aa5b1", facecolor="white", alpha=0.7, zorder=5)
            ax.add_patch(box)
        ax.text(0, 0.295, "NO DATA YET", fontsize=9, fontfamily=MONO, fontweight="bold", color=nodata_ink, ha="center", va="center", zorder=6)
        if caption:
            ax.text(0, -0.42, caption, fontsize=15, fontfamily=MONO, fontweight="bold", color="#9aa5b1", ha="center", va="center", zorder=6)
        return

    value_c = max(GAUGE_MIN, min(GAUGE_MAX, value))
    frac = (value_c - GAUGE_MIN) / (GAUGE_MAX - GAUGE_MIN)
    angle = np.radians(180 - frac * 180)
    cosA, sinA = np.cos(angle), np.sin(angle)

    box_half_w, box_bottom, box_top = 0.27, 0.19, 0.40
    r_enter = (box_bottom / sinA) if sinA > 1e-6 else np.inf
    r_exit_top = (box_top / sinA) if sinA > 1e-6 else np.inf
    r_exit_side = (box_half_w / abs(cosA)) if abs(cosA) > 1e-6 else np.inf
    r_exit = min(r_exit_top, r_exit_side)
    intersects = r_enter <= r_exit_side and np.isfinite(r_enter)

    tip_r, tail_r = 0.92, 0.16
    perp = angle + np.pi / 2
    w_base, w_tip = 0.045, 0.006

    def width_at(r):
        t = max(0.0, min(1.0, r / tip_r))
        return w_base + (w_tip - w_base) * t

    def needle_segment(r0, r1):
        w0, w1 = width_at(r0), width_at(r1)
        x0, y0 = r0 * cosA, r0 * sinA
        x1, y1 = r1 * cosA, r1 * sinA
        p0x, p0y = w0 * np.cos(perp), w0 * np.sin(perp)
        p1x, p1y = w1 * np.cos(perp), w1 * np.sin(perp)
        return mpatches.Polygon(
            [(x0 + p0x, y0 + p0y), (x1 + p1x, y1 + p1y), (x1 - p1x, y1 - p1y), (x0 - p0x, y0 - p0y)],
            closed=True, facecolor=CRIMSON, edgecolor="#7a0f22", linewidth=0.6, zorder=3
        )

    if intersects:
        ax.add_patch(needle_segment(0.0, r_enter))
        ax.add_patch(needle_segment(r_exit, tip_r))
    else:
        ax.add_patch(needle_segment(0.0, tip_r))

    px, py = w_base * np.cos(perp), w_base * np.sin(perp)
    tailx, taily = -tail_r * cosA, -tail_r * sinA
    ax.add_patch(mpatches.Polygon(
        [(tailx + px, taily + py), (0, 0), (tailx - px, taily - py)],
        closed=True, facecolor=CRIMSON, edgecolor="#7a0f22", linewidth=0.6, zorder=3
    ))
    ax.add_patch(plt.Circle((0, 0), 0.09, facecolor="#3a3f4b", edgecolor=GOLD, linewidth=1.2, zorder=4))
    ax.add_patch(plt.Circle((0, 0), 0.035, facecolor=GOLD, zorder=4))

    box_color = score_pos if value_c > 0.08 else (score_neg if value_c < -0.08 else score_neu)
    if score_box:
        box = mpatches.FancyBboxPatch((-box_half_w, box_bottom), 2 * box_half_w, box_top - box_bottom,
                                       boxstyle="round,pad=0.0,rounding_size=0.045",
                                       linewidth=1.1, edgecolor=box_color, facecolor="white", alpha=0.62, zorder=5)
        ax.add_patch(box)
    mid_y = (box_top + box_bottom) / 2
    ax.text(0, mid_y + 0.06, "NET SCORE", fontsize=8.5, fontfamily=MONO, fontweight="bold", color=ink, ha="center", va="center", alpha=0.85, zorder=6)
    ax.text(0, mid_y - 0.06, f"{value:+.2f}", fontsize=8.5, fontfamily=MONO, fontweight="bold", color=box_color, ha="center", va="center", zorder=6)
    if caption:
        ax.text(0, -0.42, caption, fontsize=15, fontfamily=MONO, fontweight="bold", color=ink, ha="center", va="center", zorder=6)


def save_single_gauge(value, out_path, no_data=False, theme="light"):
    """On-page gauge: frameless/transparent, theme-matched text, no caption
    (only one gauge shows on the page now, so "Today"/"Yesterday" would be
    redundant). No baked-in copyright here -- the page renders a single
    "\u00a9 8848.live" line below the box in HTML (shared .box-copyright class,
    same font/centering as the word cloud box) instead of drawing one into
    the image pixels."""
    fig, ax = plt.subplots(figsize=(5.6, 3.7))
    fig.patch.set_alpha(0)
    draw_gauge(ax, value, caption=None, no_data=no_data, theme=theme, frame=False, score_box=False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, transparent=True, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def save_share_card(today_val, yesterday_val, yesterday_no_data, out_path):
    """1200x630 composite for the OG share image: label + Today (big) + red
    divider + Yesterday (small), matching the on-page card."""
    fig = plt.figure(figsize=(12, 6.3))
    fig.patch.set_facecolor(PAPER)
    fig.suptitle("NEPAL\nNATIONAL SENTIMENT QUANTIFIED", fontsize=15, fontfamily=MONO,
                 fontweight="bold", color=CRIMSON, y=0.99, linespacing=1.4)
    ax_today = fig.add_axes([0.06, 0.30, 0.88, 0.60])
    ax_yesterday = fig.add_axes([0.30, 0.03, 0.40, 0.26])
    draw_gauge(ax_today, today_val, "Today")
    draw_gauge(ax_yesterday, yesterday_val, "Yesterday", no_data=yesterday_no_data)
    fig.text(0.99, 0.015, "\u00a9 8848.live", fontsize=10, fontfamily=MONO, fontweight="bold",
              color="#8a93a3", alpha=0.65, ha="right", va="bottom")
    fig.savefig(out_path, dpi=100, facecolor=PAPER)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Share page (same pattern as generate_share_images.py)
# ---------------------------------------------------------------------------
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
<p>Redirecting to <a href="{redirect}">8848.live</a>&hellip;</p>
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
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    repo_root, date = sys.argv[1], sys.argv[2]

    in_csv = os.path.join(repo_root, "data", "national-sentiment", f"{date}.csv")
    if not os.path.exists(in_csv):
        print(f"No national-sentiment input CSV for {date} at {in_csv} -- skipping.")
        return

    afinn = Afinn()
    afinn_dict = dict(afinn._dict)

    with open(in_csv, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    rows = [r for r in rows if r.get("unified_category") in NATIONAL_CATS]
    if not rows:
        print(f"No national-category rows in {in_csv} -- skipping.")
        return

    scores = [headline_sentiment_2gram(r["headline"], afinn_dict) for r in rows]
    today_mean = float(np.mean(scores))
    today_n = len(scores)
    print(f"[{date}] National sentiment mean={today_mean:+.3f}  n={today_n}")

    # --- history log (day-over-day) ---
    history_path = os.path.join(repo_root, "data", "national-sentiment", "history.csv")
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    history = {}
    if os.path.exists(history_path):
        with open(history_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                history[r["date"]] = {"mean": float(r["mean"]), "n": int(r["n"])}
    history[date] = {"mean": today_mean, "n": today_n}
    with open(history_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "mean", "n"])
        w.writeheader()
        for d in sorted(history):
            w.writerow({"date": d, "mean": f"{history[d]['mean']:.6f}", "n": history[d]["n"]})

    prev_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    if prev_date in history:
        yesterday_mean = history[prev_date]["mean"]
        yesterday_no_data = False
    else:
        yesterday_mean = 0.0
        yesterday_no_data = True

    # --- images ---
    img_dir = os.path.join(repo_root, "assets", "shares", date)
    os.makedirs(img_dir, exist_ok=True)
    save_single_gauge(today_mean, os.path.join(img_dir, "national-sentiment-today-light.png"), theme="light")
    save_single_gauge(today_mean, os.path.join(img_dir, "national-sentiment-today-dark.png"), theme="dark")
    save_share_card(today_mean, yesterday_mean, yesterday_no_data, os.path.join(img_dir, "national-sentiment.png"))
    print(f"Saved gauge images -> {img_dir}")

    # --- share page ---
    share_dir = os.path.join(repo_root, "share", date, "national-sentiment")
    image_url = f"{SITE_URL}/assets/shares/{date}/national-sentiment.png"
    write_share_page(
        os.path.join(share_dir, "index.html"),
        title=f"Nepal National Sentiment Quantified — {date}",
        description=f"Today's net sentiment score: {today_mean:+.2f} (AFINN 2-gram analysis of national headlines), via 8848.live.",
        image_url=image_url,
        page_url=f"{SITE_URL}/share/{date}/national-sentiment/",
        redirect_url=f"{SITE_URL}/#national-sentiment",
    )
    print(f"wrote {share_dir}/index.html")


if __name__ == "__main__":
    main()
