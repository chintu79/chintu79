#!/usr/bin/env python3
"""Generate assets/avatar.svg — Patch, head-and-shoulders pixel mascot.

32x32 pixel grid scaled to a 512px canvas, on the profile's dark grid.
    python scripts/make_avatar.py
"""
import os

W = H = 32

def row(*segs):
    total = sum(w for _, w in segs)
    left = (W - total) // 2
    return ("." * left + "".join(c * w for c, w in segs)).ljust(W, ".")

GRID = [
    "." * 32,
    "." * 32,
    row(("T", 2)), row(("T", 2)),
    row(("A", 2)), row(("A", 2)), row(("A", 2)),
    row(("H", 12)),
    row(("H", 18)),
    row(("H", 22)),
    row(("H", 24)),
    row(("H", 2), ("V", 20), ("H", 2)),
    row(("H", 2), ("V", 4), ("E", 2), ("V", 8), ("E", 2), ("V", 4), ("H", 2)),
    row(("H", 2), ("V", 4), ("E", 2), ("V", 8), ("E", 2), ("V", 4), ("H", 2)),
    row(("H", 2), ("V", 20), ("H", 2)),
    row(("H", 2), ("V", 6), ("G", 8), ("V", 6), ("H", 2)),
    row(("H", 24)),
    row(("H", 22)),
    row(("H", 18)),
    row(("b", 12)),
    row(("B", 22)),
    row(("B", 26)),
    row(("B", 28)),
    row(("B", 10), ("G", 2), ("B", 4), ("G", 2), ("B", 10)),
    row(("B", 30)),
    row(("b", 30)),
    "." * 32,
]
for i, r in enumerate(GRID):
    assert len(r) == 32, (i, len(r))

COLORS = {
    "T": "#70D6A1",   # antenna tip — green LED
    "A": "#5A74D8",   # antenna stem
    "H": "#7897FF",   # head — accent periwinkle
    "V": "#0B0D10",   # visor — background black
    "E": "#70D6A1",   # eyes — green
    "G": "#70D6A1",   # LEDs / smile
    "B": "#5A74D8",   # shoulders — deep accent
    "b": "#46589E",   # body shade
}

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Patch — pixel-art robot developer avatar">',
    '<rect width="512" height="512" fill="#0B0D10"/>',
]
# faint grid, every 32px
for x in range(32, 512, 32):
    parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="512" stroke="#141922" stroke-width="1"/>')
for y in range(32, 512, 32):
    parts.append(f'<line x1="0" y1="{y}" x2="512" y2="{y}" stroke="#141922" stroke-width="1"/>')

P = 16  # px per pixel
for y, line in enumerate(GRID):
    for x, ch in enumerate(line):
        if ch != ".":
            parts.append(f'<rect x="{x * P}" y="{y * P}" width="{P}" height="{P}" fill="{COLORS[ch]}"/>')
parts.append('</svg>')

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "avatar.svg")
with open(OUT, "w") as f:
    f.write("".join(parts))
print("wrote", OUT)
