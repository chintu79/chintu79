#!/usr/bin/env python3
"""
Render data/contributions.json as a terminal-style stats card SVG
(current/longest streak, yearly total, active days). CSS-animation only.

    python scripts/render_stats_svg.py [data.json] [output.svg]
"""
import datetime
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "stats.svg")

BG = "#0B0D10"
PANEL = "#10141B"
TILE = "#12161F"
FRAME = "#1F2733"
MUTED = "#A1A1AA"
INK = "#E8EAED"
ACCENT = "#7897FF"
GREEN = "#70D6A1"

W, H = 880, 196
PAD = 20
TITLEBAR_H = 38
BAR_W = 5
GAP = 14
TILE_W = (W - PAD * 2 - GAP * 3) / 4
TILE_H = 108
TILES_TOP = TITLEBAR_H + 14

data = json.load(open(SRC))
cur, lng = data["current_streak"], data["longest_streak"]
n_days = len(data["days"])

def span(s):
    if not s["length"]:
        return "—"
    f = lambda d: datetime.date.fromisoformat(d).strftime("%b %-d")
    return f'{f(s["start"])} – {f(s["end"])}'

tiles = [
    ("current streak", str(cur["length"]), "days", span(cur), GREEN),
    ("longest streak", str(lng["length"]), "days", span(lng), INK),
    ("contributions", f'{data["total_contributions"]:,}', "in last 365d", f'best day: {data["best_day"]["count"]} · {datetime.date.fromisoformat(data["best_day"]["date"]).strftime("%b %-d")}', ACCENT),
    ("active days", str(data["active_days"]), f'/ {n_days}', f'{data["avg_per_active_day"]} avg per active day', INK),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" role="img" aria-label="GitHub stats: {cur["length"]}-day current streak, {lng["length"]}-day longest streak, {data["total_contributions"]} contributions in the last year">',
    f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
    parts.append(f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">shreekrishna@github: ~ $ ./stats.sh</text>')

for i, (label, value, unit, caption, accent) in enumerate(tiles):
    x = PAD + i * (TILE_W + GAP)
    parts.append('<g>')
    parts.append(f'<rect x="{x:.1f}" y="{TILES_TOP}" width="{TILE_W:.1f}" height="{TILE_H}" rx="8" fill="{TILE}" stroke="{FRAME}"/>')
    parts.append(f'<rect x="{x:.1f}" y="{TILES_TOP}" width="{BAR_W}" height="{TILE_H}" rx="2.5" fill="{accent}"/>')
    parts.append(f'<text x="{x + 18:.1f}" y="{TILES_TOP + 26}" fill="{MUTED}" font-size="11" letter-spacing="1.5">{label.upper()}</text>')
    parts.append(f'<text x="{x + 18:.1f}" y="{TILES_TOP + 68}" fill="{accent}" font-size="34" font-weight="700">{value}<tspan fill="{MUTED}" font-size="12" font-weight="400" dx="6">{unit}</tspan></text>')
    parts.append(f'<text x="{x + 18:.1f}" y="{TILES_TOP + 92}" fill="{MUTED}" font-size="10">{caption}</text>')
    parts.append('</g>')

parts.append('</svg>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write("".join(parts))
print(f"wrote {OUT}")
