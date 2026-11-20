"""Animated GitHub stats + top languages card."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

W, H = 1200, 310

DEMO = dict(
    followers=46, following=17, repos=22, stars=38, commits=None, prs=None, issues=None,
    contributions=None,
    langs=[("TypeScript", "#3178C6", 41), ("PHP", "#4F5D95", 22), ("Java", "#B07219", 20),
           ("JavaScript", "#F1E05A", 9), ("Python", "#3572A5", 5), ("CSS", "#563D7C", 3)],
)


def icon(kind, x, y, col):
    if kind == "repo":
        return f'<g transform="translate({x},{y})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="-8" y="-10" width="16" height="20" rx="2.5"/><path d="M-8,4 h16"/></g>'
    if kind == "star":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = 11 if i % 2 == 0 else 4.6
            pts.append(f"{f(x+math.cos(a)*rr,1)},{f(y+math.sin(a)*rr,1)}")
        return f'<polygon points="{" ".join(pts)}" fill="{col}" fill-opacity=".25" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>'
    if kind == "users":
        return f'<g transform="translate({x},{y})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"><circle cx="-4" cy="-4" r="4.6"/><path d="M-12,9 c0,-6 16,-6 16,0"/><circle cx="8" cy="-2" r="3.4"/><path d="M5,8 c1,-3 9,-3 9,1"/></g>'
    if kind == "commit":
        return f'<g transform="translate({x},{y})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"><circle r="5"/><path d="M-13,0 h8 M5,0 h8"/></g>'
    if kind == "pr":
        return f'<g transform="translate({x},{y})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"><circle cx="-6" cy="-7" r="3"/><circle cx="-6" cy="8" r="3"/><circle cx="8" cy="8" r="3"/><path d="M-6,-4 v9 M8,5 v-8 q0,-4 -4,-4 h-3"/></g>'
    if kind == "issue":
        return f'<g transform="translate({x},{y})" fill="none" stroke="{col}" stroke-width="2"><circle r="9"/><circle r="2.2" fill="{col}"/></g>'
    return ""


def num(v):
    return "—" if v is None else f"{v:,}"


def build(data=None, demo=True, login="Muhtasim-Masum-Hasnayen"):
    d = data or DEMO
    tiles = [
        ("repo", "REPOSITORIES", d["repos"], "#38BDF8"),
        ("star", "STARS EARNED", d["stars"], AMBER),
        ("users", "FOLLOWERS", d["followers"], "#A78BFA"),
        ("commit", "COMMITS · 12M", d["commits"], ORANGE),
        ("pr", "PULL REQUESTS", d["prs"], GREEN),
        ("issue", "ISSUES", d["issues"], "#F43F5E"),
    ]
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070B12"/><stop offset="1" stop-color="#0C0F14"/></linearGradient>
<linearGradient id="tt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
<clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>"""
    b = '<g clip-path="url(#round)">'
    b += f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    b += f'<circle cx="120" cy="260" r="240" fill="{ORANGE}" opacity=".06"/><circle cx="1100" cy="40" r="220" fill="#38BDF8" opacity=".05"/>'
    # tiles (3x2)
    tw, th, gx, gy = 178, 112, 16, 16
    for i, (ic, lab, val, col) in enumerate(tiles):
        r_, c_ = divmod(i, 3)
        x = 34 + c_ * (tw + gx)
        y = 34 + r_ * (th + gy)
        frac = 0 if val is None else min(1.0, math.log10(val + 1) / 3.2)
        circ = 2 * math.pi * 24
        b += (
            f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="#0B111B" stroke="#fff" stroke-opacity=".07"/>'
            f'<circle cx="{x+40}" cy="{y+40}" r="24" fill="none" stroke="#1E293B" stroke-width="4"/>'
            f'<circle cx="{x+40}" cy="{y+40}" r="24" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-dasharray="{f(circ*frac,1)} {f(circ,1)}" transform="rotate(-90 {x+40} {y+40})" filter="url(#glow)">'
            f'<animate attributeName="stroke-dasharray" values="0 {f(circ,1)};{f(circ*frac,1)} {f(circ,1)};{f(circ*frac,1)} {f(circ,1)}" keyTimes="0;.3;1" dur="6s" repeatCount="indefinite"/></circle>'
            + icon(ic, x + 40, y + 40, col)
            + f'<text x="{x+16}" y="{y+88}" font-family="{SANS}" font-size="26" font-weight="900" fill="#F8FAFC">{num(val)}'
            f'<animate attributeName="opacity" values=".75;1;.75" dur="{3+i%3}s" repeatCount="indefinite"/></text>'
            f'<text x="{x+16}" y="{y+104}" font-family="{MONO}" font-size="9.5" fill="#64748B" letter-spacing="1.6">{lab}</text>'
        )
    # languages
    lx = 640
    b += f'<text x="{lx}" y="48" font-family="{SANS}" font-size="20" font-weight="900" letter-spacing="3" fill="url(#tt)">TOP LANGUAGES</text>'
    sub = "SAMPLE DATA · syncs automatically" if demo else f"@{esc(login)} · by code size"
    b += f'<text x="{lx}" y="66" font-family="{MONO}" font-size="10.5" fill="#64748B" letter-spacing="1.5">{esc(sub)}</text>'
    langs = d["langs"][:6]
    top = max((p for _, _, p in langs), default=1) or 1
    for i, (name, col, pct) in enumerate(langs):
        y = 96 + i * 34
        bw = 330
        fw = bw * pct / top
        b += (
            f'<circle cx="{lx+6}" cy="{y}" r="5" fill="{col}"/>'
            f'<text x="{lx+22}" y="{y+4}" font-family="{MONO}" font-size="13" font-weight="700" fill="#E2E8F0">{esc(name)}</text>'
            f'<rect x="{lx+138}" y="{y-5}" width="{bw}" height="10" rx="5" fill="#111827"/>'
            f'<rect x="{lx+138}" y="{y-5}" width="{f(fw,1)}" height="10" rx="5" fill="{col}">'
            f'<animate attributeName="width" values="0;{f(fw,1)};{f(fw,1)}" keyTimes="0;.35;1" dur="6s" repeatCount="indefinite"/></rect>'
            f'<text x="{lx+138+bw+14}" y="{y+4}" font-family="{MONO}" font-size="12" fill="{AMBER}">{pct:.1f}%</text>'
        )
    b += "</g>"
    b += f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="#fff" stroke-opacity=".08"/>'
    b += (
        f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="{ORANGE}" stroke-width="2" pathLength="1" stroke-dasharray=".12 .88" opacity=".8">'
        f'<animate attributeName="stroke-dashoffset" values="0;-1" dur="11s" repeatCount="indefinite"/></rect>'
    )
    return svg(W, H, b, defs, title="GitHub stats", desc="Animated GitHub statistics and top languages.")


if __name__ == "__main__":
    write("stats.svg", build())
