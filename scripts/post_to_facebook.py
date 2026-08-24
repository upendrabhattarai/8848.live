#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-post today's word cloud image, National Sentiment gauge image, and a
link to the full digest, to the 8848.live Facebook Page -- via the Facebook
Graph API (Pages API), no browser/manual clicking involved.

Runs from GitHub Actions (see .github/workflows/facebook-post.yml), which has
unrestricted outbound internet access to graph.facebook.com. Reads the Page
ID and a long-lived Page Access Token from environment variables (populated
from GitHub repo secrets -- never committed to the repo).

Posts made:
  1. Photo post: assets/shares/<date>/wordcloud.png
  2. Photo post: assets/shares/<date>/national-sentiment.png (skipped if the
     day has no National Sentiment data yet)
  3. Link post: the full digest article (Facebook renders its own preview
     card from that page's og:image/og:title/og:description)

Idempotent: writes a marker file at _data/fb-posted/<date>.json after a
successful run; if that marker already exists, the script exits immediately
without posting again (so re-running the workflow, e.g. after a manual
re-trigger, never double-posts).

Usage: python3 post_to_facebook.py <repo_root> <YYYY-MM-DD|latest>
  "latest" auto-detects the most recent _posts/YYYY-MM-DD-nepal-news-digest.md
  file by filename, so the GitHub Actions workflow never has to guess/compute
  "today" itself (avoids timezone drift between UTC and Nepal time).
Required env vars: FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN
"""
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH_VERSION = "v21.0"
SITE_URL = "https://8848.live"


def graph_post(path, params, access_token):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{path}"
    params = dict(params)
    params["access_token"] = access_token
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Graph API error ({e.code}) posting to {path}:\n{body}", file=sys.stderr)
        raise


def read_front_matter(post_path):
    with open(post_path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise RuntimeError(f"No front matter found in {post_path}")
    fm = m.group(1)

    def field(name):
        fm_m = re.search(rf'^{name}:\s*"(.*)"\s*$', fm, re.M)
        return fm_m.group(1) if fm_m else None

    return {
        "title": field("title"),
        "summary_en": field("summary_en"),
    }


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    repo_root, date = sys.argv[1], sys.argv[2]

    if date == "latest":
        candidates = sorted(glob.glob(os.path.join(repo_root, "_posts", "*-nepal-news-digest.md")))
        if not candidates:
            print("No _posts/*-nepal-news-digest.md files found -- nothing to post.", file=sys.stderr)
            sys.exit(1)
        latest_file = os.path.basename(candidates[-1])
        date = latest_file[: len("YYYY-MM-DD")]
        print(f"Auto-detected latest digest date: {date}")

    page_id = os.environ.get("FB_PAGE_ID")
    access_token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    if not page_id or not access_token:
        print("Missing FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN env vars -- skipping Facebook post.", file=sys.stderr)
        sys.exit(1)

    marker_path = os.path.join(repo_root, "_data", "fb-posted", f"{date}.json")
    if os.path.exists(marker_path):
        print(f"Already posted for {date} (marker exists at {marker_path}) -- skipping.")
        return

    post_path = os.path.join(repo_root, "_posts", f"{date}-nepal-news-digest.md")
    if not os.path.exists(post_path):
        print(f"No digest post found for {date} at {post_path} -- nothing to post.")
        return
    fm = read_front_matter(post_path)

    y, m, d = date.split("-")
    digest_url = f"{SITE_URL}/{y}/{m}/{d}/nepal-news-digest/"

    wordcloud_img = f"{SITE_URL}/assets/shares/{date}/wordcloud.png"
    sentiment_img = f"{SITE_URL}/assets/shares/{date}/national-sentiment.png"
    wordcloud_img_local = os.path.join(repo_root, "assets", "shares", date, "wordcloud.png")
    sentiment_img_local = os.path.join(repo_root, "assets", "shares", date, "national-sentiment.png")

    results = {}

    # 1. Word cloud photo
    if os.path.exists(wordcloud_img_local):
        caption = f"Today's buzzwords from Nepal's headlines — {fm['title']}.\n\n{fm['summary_en']}\n\nFull digest: {digest_url}"
        resp = graph_post(f"{page_id}/photos", {"url": wordcloud_img, "caption": caption}, access_token)
        print("Posted word cloud photo:", resp)
        results["wordcloud_post"] = resp
    else:
        print(f"No word cloud image at {wordcloud_img_local} -- skipping that post.")

    # 2. National Sentiment gauge photo
    if os.path.exists(sentiment_img_local):
        caption = f"Nepal National Sentiment Quantified — {date}. AFINN 2-gram sentiment analysis of today's national headlines.\n\nFull digest: {digest_url}"
        resp = graph_post(f"{page_id}/photos", {"url": sentiment_img, "caption": caption}, access_token)
        print("Posted National Sentiment photo:", resp)
        results["sentiment_post"] = resp
    else:
        print(f"No National Sentiment image at {sentiment_img_local} -- skipping that post (normal on day one).")

    # 3. Link post to the full digest
    message = f"{fm['title']}\n\n{fm['summary_en']}"
    resp = graph_post(f"{page_id}/feed", {"message": message, "link": digest_url}, access_token)
    print("Posted digest link:", resp)
    results["digest_post"] = resp

    os.makedirs(os.path.dirname(marker_path), exist_ok=True)
    with open(marker_path, "w", encoding="utf-8") as f:
        json.dump({"date": date, "posted": results}, f, indent=2)
    print(f"Wrote marker -> {marker_path}")


if __name__ == "__main__":
    main()
