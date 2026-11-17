#!/usr/bin/env python3
"""Render og/card.html to the site's Open Graph image.

The card is ordinary HTML and CSS; this renders it in headless Chromium at
1200x630, at 2x so the type is crisp, then downsamples to the exact size the
social platforms want and flattens it to RGB (an alpha channel is rejected by
some of them).

    python3 og/render.py            # write the image
    python3 og/render.py --check    # fail if the committed image is stale
    python3 og/render.py --out /tmp/x.png

Requires Playwright and Pillow:

    pip install playwright pillow
    playwright install chromium

Pass --browser to use a Chrome/Chromium already on the machine instead.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "web/og-image.png"
WIDTH, HEIGHT = 1200, 630
SCALE = 2


def check_assets() -> list[str]:
    """Every asset the card mentions has to exist, or it renders a blank frame."""
    html = (HERE / "card.html").read_text()
    missing = []
    for attr in html.split('src="')[1:]:
        rel = attr.split('"')[0]
        if rel.startswith(("http://", "https://", "data:")):
            continue
        if not (HERE / rel).is_file():
            missing.append(rel)
    return missing


def render(browser_path: str | None) -> Image.Image:
    with sync_playwright() as p:
        launch = {"args": ["--no-sandbox"]}
        if browser_path:
            launch["executable_path"] = browser_path
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT},
                                device_scale_factor=SCALE)
        page.goto((HERE / "card.html").as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(400)
        shot = HERE / ".render@2x.png"
        page.screenshot(path=str(shot))
        browser.close()
    image = Image.open(shot).convert("RGB")
    shot.unlink()
    return image.resize((WIDTH, HEIGHT), Image.LANCZOS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="where to write the PNG")
    ap.add_argument("--check", action="store_true",
                    help="compare against the committed image instead of writing")
    ap.add_argument("--browser", help="path to a Chrome or Chromium binary")
    args = ap.parse_args()

    missing = check_assets()
    if missing:
        print("og: card.html references files that are not there:", file=sys.stderr)
        for name in missing:
            print(f"  {name}", file=sys.stderr)
        return 1

    image = render(args.browser)
    target = Path(args.out) if args.out else OUT

    if args.check:
        if not target.is_file():
            print(f"og: {target} is missing; run python3 og/render.py", file=sys.stderr)
            return 1
        existing = Image.open(target).convert("RGB")
        if existing.size != image.size:
            print(f"og: {target} is {existing.size}, expected {image.size}", file=sys.stderr)
            return 1
        diff = sum(1 for a, b in zip(existing.getdata(), image.getdata()) if a != b)
        if diff:
            share = diff / (image.size[0] * image.size[1]) * 100
            print(f"og: {target} is stale ({share:.1f}% of pixels differ); "
                  "run python3 og/render.py", file=sys.stderr)
            return 1
        print(f"og: {target} matches the card")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, optimize=True)
    print(f"og: wrote {target} ({image.size[0]}x{image.size[1]}, "
          f"{target.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
