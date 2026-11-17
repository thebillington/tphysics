#!/usr/bin/env python3
"""Capture the game frame that og/card.html shows.

Runs `examples/games/flappy_bird.py` in the browser editor from this repository,
flies it with a small controller (see fly.py) and screenshots the canvas. The
image on the card is the engine's own output.

    python3 og/capture.py

Requires Playwright with a Chromium (`playwright install chromium`), or pass
`--browser /path/to/chrome`.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import shutil
import socketserver
import tempfile
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from fly import fly

REPO = Path(__file__).resolve().parent.parent
WEB = REPO / "web"
ASSETS = REPO / "og" / "assets"
EXAMPLE = REPO / "examples" / "games" / "flappy_bird.py"
SEED = 7


class Handler(http.server.SimpleHTTPRequestHandler):
    """Serve the repository, but let the page under /web/ reach the engine.

    web/tphysics.py is a symlink to the author's machine, and web/examples is a
    local convenience link, so the editor's fetches are mapped onto the real
    files in the repository instead of relying on either.
    """

    def translate_path(self, path: str) -> str:
        if path.startswith("/web/tphysics.py"):
            path = "/tphysics.py"
        elif path.startswith("/web/examples/"):
            path = "/examples/" + path[len("/web/examples/"):]
        return super().translate_path(path)


def serve() -> tuple[socketserver.TCPServer, int]:
    # threaded: Pyodide is fetched in parallel with the app's own files, and a
    # single-threaded server lets one request block the runtime download
    handler = functools.partial(Handler, directory=str(REPO))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--browser", help="path to a Chrome or Chromium binary")
    args = ap.parse_args()

    # the page is served from /web/, so the editor's relative fetches resolve
    httpd, port = serve()
    try:
        with sync_playwright() as p:
            launch = {"args": ["--no-sandbox"]}
            if args.browser:
                launch["executable_path"] = args.browser
            browser = p.chromium.launch(**launch)
            page = browser.new_page(viewport={"width": 1440, "height": 900},
                                    device_scale_factor=2)
            page.goto(f"http://127.0.0.1:{port}/web/", wait_until="domcontentloaded")
            page.wait_for_function("!document.querySelector('#run-btn').disabled",
                                   timeout=180_000)
            page.evaluate("(code) => editor.setValue(code)",
                          f"import random\nrandom.seed({SEED})\n" + EXAMPLE.read_text())
            page.click("#run-btn")
            page.wait_for_timeout(150)
            page.click("#game-canvas")

            box = page.locator("#game-canvas").bounding_box()
            inset = 1.5          # leave the editor's own green border out of frame
            clip = {"x": box["x"] + inset, "y": box["y"] + inset,
                    "width": box["width"] - 2 * inset,
                    "height": box["height"] - 2 * inset}

            with tempfile.TemporaryDirectory() as tmp:
                best = fly(page, clip, Path(tmp))
                ASSETS.mkdir(parents=True, exist_ok=True)
                shutil.copy(best, ASSETS / "flappy.png")
            browser.close()
    finally:
        httpd.shutdown()
    print(f"og: captured {ASSETS / 'flappy.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
