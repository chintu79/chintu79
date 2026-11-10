#!/usr/bin/env python3
"""Generate assets/avatar.svg — Patch v2: orange robot on charcoal.

32x32 pixel grid scaled to a 512px canvas. Charcoal bg, orange visor
(highlight/main/shade), headphone band, LED eyes, spark marks.
    python scripts/make_avatar.py
"""
import os

W = H = 32

def row(*segs):
    total = sum(w for _, w in segs)
    left = (W - total) // 2
    assert total <= W, segs
    return ("." * left + "".join(c * w for c, w in segs)).ljust(W, ".")

GRID = [
    "." * 32,
    "." * 32,
    row(("T", 2)), row(("T", 2)),                                   # antenna tip
    row(("A", 2)), row(("A", 2)), row(("A", 2)),                    # antenna stem
    row(("H", 12)),                                                 # head top
    row(("H", 17)),
    row(("O", 21)),                                                 # headphone band
    row(("H", 22)),
    row(("C", 4), ("H", 16), ("C", 4)),                             # ear cups
    row(("C", 4), ("H", 1), ("L", 16), ("H", 1), ("C", 4)),          # visor highlight
    row(("C", 4), ("H", 1), ("P", 3), ("k", 3), ("P", 4), ("k", 3), ("P", 3), ("H", 1), ("C", 4)),
    row(("C", 4), ("H", 1), ("P", 3), ("k", 3), ("P", 4), ("k", 3), ("P", 3), ("H", 1), ("C", 4)),
    row(("C", 4), ("H", 1), ("P", 5), ("k", 6), ("P", 5), ("H", 1), ("C", 4)),  # smile
    row(("C", 4), ("H", 1), ("D", 16), ("H", 1), ("C", 4)),          # visor shade
    row(("H", 22)),
    row(("H", 17)),
    row(("H", 12)),
    row(("b", 10)),                                                 # neck shade
    row(("B", 20)),                                                 # shoulders
    row(("B", 26)),
    row(("B", 28)),
    row(("B", 10), ("o", 2), ("B", 4), ("o", 2), ("B", 10)),         # chest LEDs
    row(("B", 30)),
    row(("d", 30)),                                                # bottom shade
    "." * 32,
    "." * 32,
]
for i, r in enumerate(GRID):
    assert len(r) == 32, (i, r)

COLORS = {
    "T": "#E87536",   # antenna tip — orange
    "A": "#2A2926",   # antenna stem — charcoal
    "H": "#2E2C29",   # head — warm charcoal
    "O": "#D9622B",   # headphone band
    "C": "#E87536",   # ear cups — orange
    "L": "#F6A35F",   # visor highlight
    "P": "#E87536",   # visor main
    "D": "#C85A22",   # visor shade
    "k": "#171817",   # slits / smile — charcoal-black
    "b": "#201F1C",   # neck shade
    "B": "#211F1D",   # shoulders
    "d": "#1A1917",  # bottom shade
    "o": "#E87536",   # chest LEDs
}

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Patch v2 — orange pixel-art robot developer avatar on charcoal">',
    '<rect width="512" height="512" fill="#171817"/>',
]
# faint dot grid
for y in range(16, 512, 32):
    for x in range(16, 512, 32):
        parts.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#211F1D"/>')

P = 16
for y, line in enumerate(GRID):
    for x, ch in enumerate(line):
        if ch != ".":
            parts.append(f'<rect x="{x * P}" y="{y * P}" width="{P}" height="{P}" fill="{COLORS[ch]}"/>')

# spark marks (plus-shapes)
def spark(cx, cy, c="#E87536"):
    return (f'<rect x="{cx - 1}" y="{cy - 4}" width="2" height="10" fill="{c}"/>'
            f'<rect x="{cx - 4}" y="{cy - 1}" width="10" height="2" fill="{c}"/>')
parts.append(spark(452, 88))
parts.append(spark(62, 300, "#D9622B"))
parts.append('</svg>')

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "avatar.svg")
with open(OUT, "w") as f:
    f.write("".join(parts))
print("wrote", OUT)
