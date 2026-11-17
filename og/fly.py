"""Fly flappy_bird.py so it can be photographed mid-game.

The example has one pipe on screen and the bird falls out of the frame in about
two seconds, so the capture reads the canvas, taps Space to keep the bird inside
the gap, and keeps the frames where the pipe is actually in the playfield.
"""
from __future__ import annotations

import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import Page


def state(frame: Path) -> tuple[float, float, float] | None:
    """(bird y, pipe x, gap centre y), all 0..1, from one screenshot."""
    image = Image.open(frame).convert("RGB").resize((200, 175))
    px = image.load()
    w, h = image.size

    columns: dict[int, list[int]] = {}
    for x in range(w):
        ys = [y for y in range(h)
              if px[x, y][1] > 90 and px[x, y][0] < 70 and px[x, y][2] < 70]
        if len(ys) > h * 0.5:
            columns[x] = ys

    bird = [(x, y) for x in range(w) for y in range(h)
            if px[x, y][0] > 200 and px[x, y][1] > 200 and px[x, y][2] < 90]
    if not bird:
        return None
    bird_y = sum(y for _, y in bird) / len(bird) / h

    pipe_x = gap = None
    if columns:
        xs = sorted(columns)
        pipe_x = (xs[0] + xs[-1]) / 2 / w
        column = columns[xs[len(xs) // 2]]
        missing = [y for y in range(h) if y not in set(column)]
        if missing:
            gap = (missing[0] + missing[-1]) / 2 / h
    if pipe_x is None or gap is None:
        return None
    return bird_y, pipe_x, gap


def fly(page: Page, clip: dict, scratch: Path, seconds: int = 22) -> Path:
    """Keep the bird alive and return the frame where it sits best in the gap."""
    scratch.mkdir(parents=True, exist_ok=True)
    best: tuple[float, Path] | None = None
    probe = scratch / "probe.png"
    started = time.time()

    while time.time() - started < seconds:
        page.screenshot(path=str(probe), clip=clip)
        reading = state(probe)
        if reading:
            bird_y, pipe_x, gap = reading
            if bird_y > gap + 0.02:                 # below the gap: flap
                page.keyboard.down("Space")
                page.wait_for_timeout(60)
                page.keyboard.up("Space")
            if 0.30 < pipe_x < 0.68:
                # prefer a pipe near the middle with the bird level with the gap
                score = abs(pipe_x - 0.5) + 3 * abs(bird_y - gap)
                shot = scratch / f"{len(list(scratch.glob('*.png')))}.png"
                page.screenshot(path=str(shot), clip=clip)
                if best is None or score < best[0]:
                    best = (score, shot)
        page.wait_for_timeout(120)

    if best is None:
        raise SystemExit("og: the bird never lined up with a pipe; run it again")
    return best[1]
