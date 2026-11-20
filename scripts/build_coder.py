"""Animated scene: a CSE engineer coding at a dual-monitor desk, late at night."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

W, H = 1200, 420
CW = 6.62  # monospace advance at 11px (textLength keeps it exact)

CODE = [
    [("import", "#C084FC"), (" torch", "#E2E8F0")],
    [("from", "#C084FC"), (" transformers ", "#E2E8F0"), ("import", "#C084FC"), (" AutoTokenizer", "#7DD3FC")],
    [],
    [("class", "#C084FC"), (" BanglaNLP", "#FCD34D"), ("(nn.Module):", "#E2E8F0")],
    [("    def", "#C084FC"), (" forward", "#60A5FA"), ("(self, x):", "#E2E8F0")],
    [("        h = self.encoder(x)", "#E2E8F0")],
    [("        return", "#C084FC"), (" self.head(h)", "#E2E8F0")],
    [],
    [("for", "#C084FC"), (" epoch ", "#E2E8F0"), ("in", "#C084FC"), (" range(", "#E2E8F0"), ("30", "#FB923C"), ("):", "#E2E8F0")],
    [("    loss = model.step(batch)  ", "#E2E8F0"), ("# learning...", "#64748B")],
]


def typed_lines(x, y0, lh, cycle=16.0):
    out = ""
    n = len(CODE)
    for i, toks in enumerate(CODE):
        if not toks:
            continue
        text = "".join(t for t, _ in toks)
        wpx = len(text) * CW
        s = 0.03 + i * 0.065
        e = s + 0.05
        kt = f"0;{f(s,3)};{f(e,3)};0.93;1"
        vals = f"0;0;{f(wpx+4,1)};{f(wpx+4,1)};0"
        tsp = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in toks)
        ly = y0 + i * lh
        out += (
            f'<clipPath id="cl{i}"><rect x="{x}" y="{ly-12}" width="{f(wpx+4,1)}" height="{lh}">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/></rect></clipPath>'
            f'<text x="{x}" y="{ly}" font-family="{MONO}" font-size="11" xml:space="preserve" style="white-space:pre" textLength="{f(wpx,1)}" lengthAdjust="spacingAndGlyphs" clip-path="url(#cl{i})">{tsp}</text>'
            f'<text x="{x-28}" y="{ly}" font-family="{MONO}" font-size="10" fill="#475569" text-anchor="end">{i+1}</text>'
        )
    return out


def monitor_frame(x, y, w, h):
    return (
        f'<rect x="{x-6}" y="{y-6}" width="{w+12}" height="{h+12}" rx="10" fill="#0A0F18" stroke="#1E293B" stroke-width="2"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#070B12"/>'
        f'<rect x="{x+w/2-34}" y="{y+h+6}" width="68" height="26" fill="#111827"/>'
        f'<rect x="{x+w/2-58}" y="{y+h+30}" width="116" height="7" rx="3.5" fill="#1F2937"/>'
    )


def editor(x, y, w, h):
    s = monitor_frame(x, y, w, h)
    s += f'<clipPath id="edclip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/></clipPath><g clip-path="url(#edclip)">'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="20" fill="#0F172A"/>'
    s += f'<rect x="{x}" y="{y+20}" width="30" height="{h-20-16}" fill="#0B1220"/>'
    for i in range(5):
        s += f'<rect x="{x+9}" y="{y+32+i*26}" width="12" height="12" rx="3" fill="#1E293B"><animate attributeName="fill" values="#1E293B;{ORANGE if i==1 else "#334155"};#1E293B" dur="{4+i}s" repeatCount="indefinite"/></rect>'
    s += f'<rect x="{x+34}" y="{y}" width="124" height="20" fill="#070B12"/><rect x="{x+34}" y="{y+18}" width="124" height="2" fill="{ORANGE}"/>'
    s += f'<text x="{x+44}" y="{y+14}" font-family="{MONO}" font-size="10" fill="#CBD5E1">bangla_nlp.py</text>'
    s += f'<circle cx="{x+146}" cy="{y+10}" r="2.6" fill="{AMBER}"/>'
    s += f'<text x="{x+w-10}" y="{y+14}" text-anchor="end" font-family="{MONO}" font-size="9" fill="#64748B">● ● ●</text>'
    s += typed_lines(x + 58, y + 38, 14)
    # blinking cursor
    s += f'<rect x="{x+58}" y="{y+38+9*14-10}" width="6" height="12" fill="#E2E8F0"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'
    # status bar
    s += f'<rect x="{x}" y="{y+h-16}" width="{w}" height="16" fill="#1D4ED8"/>'
    s += f'<text x="{x+8}" y="{y+h-5}" font-family="{MONO}" font-size="9" fill="#DBEAFE">⎇ main   ✓ 0 errors   Python 3.12</text>'
    s += f'<text x="{x+w-8}" y="{y+h-5}" text-anchor="end" font-family="{MONO}" font-size="9" fill="#DBEAFE">Ln 10, Col 29</text>'
    s += "</g>"
    return s


def dashboard(x, y, w, h):
    s = monitor_frame(x, y, w, h)
    s += f'<clipPath id="dbclip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/></clipPath><g clip-path="url(#dbclip)">'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#08101C"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="22" fill="#0F172A"/>'
    s += f'<circle cx="{x+12}" cy="{y+11}" r="3.4" fill="#22C55E"><animate attributeName="opacity" values="1;.2;1" dur="1.2s" repeatCount="indefinite"/></circle>'
    s += f'<text x="{x+22}" y="{y+15}" font-family="{MONO}" font-size="10" fill="#CBD5E1">training · bn-sentiment-v3</text>'
    s += f'<text x="{x+w-10}" y="{y+15}" text-anchor="end" font-family="{MONO}" font-size="9" fill="#64748B">GPU 87%</text>'
    # chart
    cx0, cy0, cw_, ch_ = x + 14, y + 32, w - 28, 78
    s += f'<rect x="{cx0}" y="{cy0}" width="{cw_}" height="{ch_}" rx="4" fill="#0B1424" stroke="#1E293B"/>'
    for g in range(1, 4):
        s += f'<line x1="{cx0}" y1="{cy0+g*ch_/4}" x2="{cx0+cw_}" y2="{cy0+g*ch_/4}" stroke="#1E293B" stroke-dasharray="3 4"/>'
    r = rng(5)
    pts_loss, pts_acc = [], []
    N = 30
    for i in range(N):
        t = i / (N - 1)
        loss = 0.9 * math.exp(-3.2 * t) + 0.12 + r.uniform(-0.025, 0.025)
        acc = 0.55 + 0.4 * (1 - math.exp(-3.4 * t)) + r.uniform(-0.015, 0.015)
        px = cx0 + 8 + t * (cw_ - 16)
        pts_loss.append((px, cy0 + 8 + (1 - min(loss, 1.0)) * 0 + (loss / 1.05) * (ch_ - 16)))
        pts_acc.append((px, cy0 + ch_ - 8 - (acc - 0.5) / 0.5 * (ch_ - 16)))
    dl = "M" + " L".join(f"{f(a,1)},{f(b,1)}" for a, b in pts_loss)
    da = "M" + " L".join(f"{f(a,1)},{f(b,1)}" for a, b in pts_acc)
    for d, col, begin in ((dl, "#F87171", "0"), (da, ORANGE, "0.4")):
        s += (
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.55;.93;1" dur="9s" begin="{begin}s" repeatCount="indefinite"/></path>'
        )
    s += f'<text x="{cx0+8}" y="{cy0+14}" font-family="{MONO}" font-size="9" fill="#F87171">● loss</text><text x="{cx0+52}" y="{cy0+14}" font-family="{MONO}" font-size="9" fill="{ORANGE}">● acc</text>'
    # tiles
    tiles = [("LOSS", "0.114", "#F87171"), ("ACC", "94.7%", ORANGE), ("TESTS", "128 ✓", "#22C55E")]
    tw = (w - 28 - 16) / 3
    for i, (a, b, c) in enumerate(tiles):
        tx = x + 14 + i * (tw + 8)
        s += (
            f'<rect x="{f(tx)}" y="{y+120}" width="{f(tw)}" height="32" rx="5" fill="#0B1424" stroke="#1E293B"/>'
            f'<text x="{f(tx+8)}" y="{y+132}" font-family="{MONO}" font-size="8" fill="#64748B" letter-spacing="1">{a}</text>'
            f'<text x="{f(tx+8)}" y="{y+147}" font-family="{SANS}" font-size="13" font-weight="800" fill="{c}">{b}'
            f'<animate attributeName="opacity" values="1;.55;1" dur="{3+i}s" repeatCount="indefinite"/></text>'
        )
    # progress
    s += (
        f'<rect x="{x+14}" y="{y+h-16}" width="{w-28}" height="6" rx="3" fill="#1E293B"/>'
        f'<rect x="{x+14}" y="{y+h-16}" width="{w-28}" height="6" rx="3" fill="url(#prog)">'
        f'<animate attributeName="width" values="0;{w-28};{w-28};0" keyTimes="0;.7;.95;1" dur="9s" repeatCount="indefinite"/></rect>'
    )
    s += f'<text x="{x+14}" y="{y+h-22-6}" font-family="{MONO}" font-size="8" fill="#94A3B8">epoch 18/30 · bn-sentiment · eta 02:14</text>'
    s += "</g>"
    return s


def person(cx=600, by=420):
    skin = "#C68B59"
    hood = "#1B2433"
    s = ""
    # rim light glow on person
    s += f'<ellipse cx="{cx}" cy="{by-70}" rx="170" ry="90" fill="url(#rim)"/>'
    # hoodie body
    s += f'<path d="M{cx-98},{by} C{cx-98},{by-52} {cx-66},{by-86} {cx-24},{by-90} L{cx+24},{by-90} C{cx+66},{by-86} {cx+98},{by-52} {cx+98},{by} Z" fill="url(#hoodie)"/>'
    s += f'<path d="M{cx-98},{by} C{cx-98},{by-52} {cx-66},{by-86} {cx-24},{by-90}" fill="none" stroke="#5EA8FF" stroke-opacity=".55" stroke-width="2"/>'
    s += f'<path d="M{cx+98},{by} C{cx+98},{by-52} {cx+66},{by-86} {cx+24},{by-90}" fill="none" stroke="{ORANGE}" stroke-opacity=".5" stroke-width="2"/>'
    # hood + neck
    s += f'<ellipse cx="{cx}" cy="{by-92}" rx="46" ry="15" fill="#141C29"/>'
    s += f'<rect x="{cx-12}" y="{by-124}" width="24" height="34" rx="9" fill="{skin}"/>'
    # arms to keyboard
    for sgn in (-1, 1):
        sx = cx + sgn * 80
        ex = cx + sgn * 92
        hx = cx + sgn * 44
        s += (
            f'<path d="M{sx},{by-62} L{ex},{by-26} L{hx},{by-92}" fill="none" stroke="{hood}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M{sx},{by-62} L{ex},{by-26} L{hx},{by-92}" fill="none" stroke="#fff" stroke-opacity=".04" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<ellipse cx="{hx}" cy="{by-96}" rx="14" ry="8" fill="{skin}">'
            f'<animate attributeName="cy" values="{by-96};{by-100};{by-96};{by-98};{by-96}" dur="{0.55 if sgn<0 else 0.7}s" repeatCount="indefinite"/></ellipse>'
        )
    # head (back view) with hair
    s += f'<ellipse cx="{cx}" cy="{by-158}" rx="38" ry="42" fill="#0C111B"/>'
    s += f'<path d="M{cx-38},{by-158} C{cx-38},{by-198} {cx+38},{by-198} {cx+38},{by-158}" fill="none" stroke="#7CC4FF" stroke-opacity=".45" stroke-width="2.4"/>'
    s += f'<path d="M{cx-30},{by-176} Q{cx},{by-198} {cx+30},{by-176}" fill="none" stroke="#1F2A3D" stroke-width="3" stroke-linecap="round"/>'
    # ears
    s += f'<ellipse cx="{cx-39}" cy="{by-152}" rx="6" ry="10" fill="{skin}"/><ellipse cx="{cx+39}" cy="{by-152}" rx="6" ry="10" fill="{skin}"/>'
    # headphones
    s += f'<path d="M{cx-44},{by-150} C{cx-48},{by-214} {cx+48},{by-214} {cx+44},{by-150}" fill="none" stroke="#111827" stroke-width="8" stroke-linecap="round"/>'
    s += f'<path d="M{cx-44},{by-150} C{cx-48},{by-214} {cx+48},{by-214} {cx+44},{by-150}" fill="none" stroke="{ORANGE}" stroke-width="2.6" stroke-linecap="round" stroke-opacity=".9"/>'
    for sgn in (-1, 1):
        s += (
            f'<rect x="{cx+sgn*44-10 if sgn>0 else cx-44-10}" y="{by-166}" width="20" height="34" rx="9" fill="#141B28" stroke="{ORANGE}" stroke-width="2.2" filter="url(#glow)">'
            f'<animate attributeName="stroke-opacity" values="1;.35;1" dur="1.1s" repeatCount="indefinite"/></rect>'
        )
    # music notes
    for i, (nx, col) in enumerate(((cx - 70, "#38BDF8"), (cx + 74, ORANGE), (cx - 84, "#A78BFA"))):
        s += (
            f'<text x="{nx}" y="{by-170}" font-family="{SANS}" font-size="16" font-weight="700" fill="{col}" opacity="0">♪'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{-8 if nx<cx else 8} -42" dur="3.2s" begin="{i*1.0}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.9;0" dur="3.2s" begin="{i*1.0}s" repeatCount="indefinite"/></text>'
        )
    return s


def window(x, y, w, h):
    r = rng(21)
    s = f'<clipPath id="winclip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/></clipPath>'
    s += f'<rect x="{x-8}" y="{y-8}" width="{w+16}" height="{h+16}" rx="10" fill="#0E1624" stroke="#1E293B" stroke-width="2"/>'
    s += f'<g clip-path="url(#winclip)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#night)"/>'
    for i in range(26):
        sx, sy = x + r.uniform(4, w - 4), y + r.uniform(4, h * 0.6)
        s += f'<circle cx="{f(sx,1)}" cy="{f(sy,1)}" r="{f(r.uniform(.5,1.4))}" fill="#fff"><animate attributeName="opacity" values=".2;1;.2" dur="{f(r.uniform(2,5))}s" begin="-{f(r.uniform(0,4))}s" repeatCount="indefinite"/></circle>'
    s += f'<circle cx="{x+w*0.74}" cy="{y+h*0.24}" r="17" fill="#FFF4D6"/><circle cx="{x+w*0.74+6}" cy="{y+h*0.24-3}" r="15" fill="#0B1226"/>'
    # skyline
    bx = x
    while bx < x + w:
        bw = r.randint(14, 26)
        bh = r.randint(24, 78)
        s += f'<rect x="{bx}" y="{y+h-bh}" width="{bw}" height="{bh}" fill="#0A1020"/>'
        for wy in range(int(y + h - bh + 5), int(y + h - 4), 9):
            for wx in range(bx + 3, bx + bw - 3, 6):
                if r.random() < 0.35:
                    s += f'<rect x="{wx}" y="{wy}" width="3" height="4" fill="#FFD27A"><animate attributeName="opacity" values="1;.2;1" dur="{f(r.uniform(3,8))}s" begin="-{f(r.uniform(0,5))}s" repeatCount="indefinite"/></rect>'
        bx += bw + 2
    s += "</g>"
    s += f'<line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+h}" stroke="#0E1624" stroke-width="4"/><line x1="{x}" y1="{y+h*0.55}" x2="{x+w}" y2="{y+h*0.55}" stroke="#0E1624" stroke-width="4"/>'
    return s


def mug(x, y):
    s = f'<rect x="{x}" y="{y-26}" width="26" height="26" rx="5" fill="#E8EDF5"/><path d="M{x+26},{y-20} q12,2 0,16" fill="none" stroke="#E8EDF5" stroke-width="4"/>'
    s += f'<rect x="{x+3}" y="{y-23}" width="20" height="6" rx="3" fill="#6B3E1E"/>'
    s += f'<text x="{x+13}" y="{y-5}" text-anchor="middle" font-family="{MONO}" font-size="8" font-weight="700" fill="{ORANGE}">&lt;/&gt;</text>'
    for i in range(3):
        s += (
            f'<path d="M{x+7+i*6},{y-28} q-6,-10 0,-20 q6,-10 0,-20" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2" stroke-linecap="round">'
            f'<animate attributeName="opacity" values="0;.6;0" dur="2.6s" begin="{i*0.7}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -10" dur="2.6s" begin="{i*0.7}s" repeatCount="indefinite"/></path>'
        )
    return s


def lamp(x, y):
    s = f'<path d="M{x-120},{y-40} L{x-170},{y+90} L{x+0},{y+90} Z" fill="url(#cone)"/>'
    s += f'<rect x="{x-6}" y="{y+90-76}" width="12" height="76" fill="#1F2937"/>'
    s += f'<path d="M{x},{y+14} L{x-30},{y-40}" stroke="#334155" stroke-width="5" stroke-linecap="round"/>'
    s += f'<path d="M{x-44},{y-36} l30,-14 l12,26 l-30,12 z" fill="#111827" stroke="{ORANGE}" stroke-width="1.6"/>'
    s += f'<ellipse cx="{x}" cy="{y+94}" rx="36" ry="6" fill="#0A0F18"/>'
    return s


def toast(x, y, title, sub, col, begin, cycle=12):
    t0 = begin / cycle
    kt = f"0;{f(t0,3)};{f(t0+0.04,3)};{f(t0+0.18,3)};{f(t0+0.22,3)};1"
    return (
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="translate" values="30 0;30 0;0 0;0 0;0 0;0 0" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>'
        f'<rect x="{x}" y="{y}" width="196" height="46" rx="10" fill="#0B1220" stroke="{col}" stroke-opacity=".7"/>'
        f'<rect x="{x}" y="{y}" width="5" height="46" rx="2.5" fill="{col}"/>'
        f'<text x="{x+16}" y="{y+20}" font-family="{SANS}" font-weight="700" font-size="12.5" fill="#F1F5F9">{esc(title)}</text>'
        f'<text x="{x+16}" y="{y+35}" font-family="{MONO}" font-size="10" fill="#94A3B8">{esc(sub)}</text></g>'
    )


def build():
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060A12"/><stop offset="1" stop-color="#0A0F1A"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050816"/><stop offset="1" stop-color="#16213E"/></linearGradient>
<linearGradient id="hoodie" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#243049"/><stop offset="1" stop-color="#101827"/></linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A2018"/><stop offset="1" stop-color="#120C08"/></linearGradient>
<linearGradient id="prog" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
<radialGradient id="rim"><stop offset="0" stop-color="#3B82F6" stop-opacity=".25"/><stop offset="1" stop-color="#3B82F6" stop-opacity="0"/></radialGradient>
<radialGradient id="mon"><stop offset="0" stop-color="#3B82F6" stop-opacity=".30"/><stop offset="1" stop-color="#3B82F6" stop-opacity="0"/></radialGradient>
<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB347" stop-opacity=".22"/><stop offset="1" stop-color="#FFB347" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>
"""
    mx1, mx2, my, mw, mh = 262, 620, 40, 322, 190
    b = '<g clip-path="url(#round)">'
    b += f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    # wall light spill from monitors
    b += f'<ellipse cx="600" cy="150" rx="470" ry="190" fill="url(#mon)"><animate attributeName="opacity" values=".8;1;.8" dur="5s" repeatCount="indefinite"/></ellipse>'
    b += window(56, 62, 150, 150)
    # shelf
    b += f'<rect x="1000" y="116" width="150" height="6" rx="3" fill="#2A2018"/>'
    for i, (cx_, hh, col) in enumerate(((1008, 38, "#38BDF8"), (1022, 30, ORANGE), (1034, 42, "#A78BFA"), (1048, 34, GREEN), (1060, 40, "#F43F5E"))):
        b += f'<rect x="{cx_}" y="{116-hh}" width="11" height="{hh}" rx="1.5" fill="{col}" opacity=".85"/>'
    b += f'<path d="M1098,116 v-16 h24 v16 z" fill="#C8A24A"/><circle cx="1110" cy="92" r="9" fill="#E8C766"/><text x="1110" y="96" text-anchor="middle" font-family="{SANS}" font-size="10" font-weight="900" fill="#7A5A10">1</text>'
    b += f'<text x="1075" y="150" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#475569">// shipped it ✓</text>'

    b += lamp(1040, 188)
    b += editor(mx1, my, mw, mh)
    b += dashboard(mx2, my, mw, mh)
    # desk
    b += f'<path d="M110,300 L1090,300 L1150,350 L50,350 Z" fill="url(#desk)"/><rect x="50" y="350" width="1100" height="70" fill="#0D0907"/>'
    b += f'<line x1="110" y1="300" x2="1090" y2="300" stroke="#4B3825" stroke-width="2"/>'
    # desk glow
    b += f'<ellipse cx="600" cy="316" rx="320" ry="14" fill="#3B82F6" opacity=".16"/>'
    # keyboard + mouse
    b += f'<rect x="528" y="312" width="144" height="20" rx="5" fill="#0F1623" stroke="#1F2937"/>'
    colors = [ORANGE, "#38BDF8", GREEN, "#A78BFA", "#F43F5E", AMBER]
    for i in range(24):
        kx = 534 + i * 5.7
        b += f'<rect x="{f(kx,1)}" y="317" width="3.6" height="3" rx=".8" fill="{colors[i%6]}"><animate attributeName="opacity" values=".25;1;.25" dur="{f(1.2+(i%5)*.3)}s" begin="-{f((i%7)*.2)}s" repeatCount="indefinite"/></rect>'
        if i < 22:
            b += f'<rect x="{f(kx,1)}" y="323" width="3.6" height="3" rx=".8" fill="#334155"/>'
    b += f'<rect x="700" y="314" width="22" height="14" rx="7" fill="#0F1623" stroke="#1F2937"/><rect x="709" y="316" width="3" height="5" rx="1.5" fill="{ORANGE}"/>'
    b += mug(790, 316)
    # plant
    b += f'<path d="M330,318 h28 l-4,24 h-20 z" fill="#B45309"/>'
    for ang, ln in ((-30, 30), (0, 36), (30, 30), (-55, 22), (55, 22)):
        b += f'<path d="M344,318 Q{344+math.sin(math.radians(ang))*ln*0.6},{318-ln*0.8} {344+math.sin(math.radians(ang))*ln},{318-math.cos(math.radians(ang))*ln}" fill="none" stroke="#22A06B" stroke-width="5" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" values="-2 344 318;2 344 318;-2 344 318" dur="{f(4+abs(ang)/30)}s" repeatCount="indefinite"/></path>'
    # person on top
    b += person(600, 420)
    # toasts
    b += toast(958, 56, "All 128 tests passed", "pytest · 0.8s", "#22C55E", 1.5)
    b += toast(958, 56, "Pull request merged", "feat/nlp-pipeline → main", "#A78BFA", 5.0)
    b += toast(958, 56, "Deployed to production", "vercel · build ok", ORANGE, 8.5)

    # status ticker (bottom-left) — rotates
    msgs = [("// currently: fine-tuning NLP models", "#38BDF8"), ("// currently: automating QA with Playwright", ORANGE), ("// currently: shipping web apps", GREEN)]
    for i, (m, col) in enumerate(msgs):
        t0 = i / 3
        kt = f"0;{f(t0,3)};{f(t0+0.04,3)};{f(t0+0.29,3)};{f(t0+0.33,3)};1"
        b += (
            f'<text x="58" y="394" font-family="{MONO}" font-size="13" fill="{col}" opacity="{1 if i==0 else 0}">{esc(m)}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/></text>'
        )
    b += f'<text x="1142" y="394" text-anchor="end" font-family="{MONO}" font-size="12" fill="#64748B">uptime: ∞  ·  coffee: ☕ ×3</text>'
    # frame
    b += f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="#fff" stroke-opacity=".08"/>'
    b += (
        f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="{ORANGE}" stroke-width="2" pathLength="1" stroke-dasharray=".12 .88" opacity=".8">'
        f'<animate attributeName="stroke-dashoffset" values="0;-1" dur="10s" repeatCount="indefinite"/></rect>'
    )
    b += "</g>"
    return svg(W, H, b, defs, title="Engineer coding at night", desc="Animated scene of an engineer writing NLP code on a dual-monitor desk.")


if __name__ == "__main__":
    write("coder.svg", build())
