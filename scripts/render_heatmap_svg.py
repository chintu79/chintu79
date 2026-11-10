#!/usr/bin/env python3
"""
Render data/contributions.json as an animated contribution-graph SVG
(cells cascade in with a short pop animation, SMIL/CSS only -- GitHub runs
animation inside <img> SVGs but never JS).

    python scripts/render_heatmap_svg.py [data.json] [output.svg]
"""
import datetime
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "contrib-heatmap.svg")

BG = "#0B0D10"
PANEL = "#10141B"
FRAME = "#1F2733"
MUTED = "#A1A1AA"
INK = "#E8EAED"
ACCENT = "#E87536"
# level 0..4 -- blue ramp on near-black
LEVELS = ["#1C1917", "#33241A", "#54301F", "#844A28", "#E87536"]

W, H = 880, 172
CELL, GAP = 11, 3.5
PITCH = CELL + GAP
LEFT, TOP = 34, 46

data = json.load(open(SRC))
days = data["days"]
total = data["total_contributions"]

# GitHub weeks run Sunday..Saturday
first_wd = (datetime.date.fromisoformat(days[0]["date"]).weekday() + 1) % 7
n_cols = (len(days) + first_wd + 6) // 7
GRID_W = n_cols * PITCH
OFFSET = (W - GRID_W) / 2 - 10

cells = []
for i, d in enumerate(days):
    idx = i + first_wd
    col, row = idx // 7, idx % 7
    x, y = OFFSET + col * PITCH, TOP + row * PITCH
    lvl = d["level"] if 0 <= d["level"] <= 4 else 4
    cells.append(
        f'<rect class="c" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2" '
        f'fill="{LEVELS[lvl]}"><title>{d["date"]} · {d["count"]} contributions</title></rect>'
    )

legend_x = W - 34 - 5 * (CELL + 4) - 8
legend = [f'<text x="{legend_x - 8}" y="{H - 12}" fill="{MUTED}" font-size="10" text-anchor="end">less</text>']
for i, lv in enumerate(LEVELS):
    legend.append(f'<rect x="{legend_x + i * (CELL + 4)}" y="{H - 20}" width="{CELL}" height="{CELL}" rx="2" fill="{lv}"/>')
legend.append(f'<text x="{legend_x + 5 * (CELL + 4) + 6}" y="{H - 12}" fill="{MUTED}" font-size="10">more</text>')

start = datetime.date.fromisoformat(data["range"]["start"]).strftime("%b %Y")
end = datetime.date.fromisoformat(data["range"]["end"]).strftime("%b %Y")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" role="img" aria-label="GitHub contribution graph for {data["username"]}, {total} contributions in the last year">
<style>
@media (prefers-reduced-motion: reduce){{.c{{opacity:1}}}}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{FRAME}"/>
<text x="28" y="30" fill="{MUTED}" font-size="12">$ <tspan fill="{INK}">./contributions.sh</tspan> --last-year</text>
<text x="{W-28}" y="30" fill="{ACCENT}" font-size="12" text-anchor="end">{total:,} contributions · {start} – {end}</text>
{''.join(cells)}
{''.join(legend)}
</svg>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(cells)} cells)")
