"""Animated hero banner: Bangladesh flag + map | name + bio | UIU building."""
import base64
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

W, H = 1200, 470
CX = 588

# --------------------------------------------------------------------------
# Bangladesh flag (waving, slice based) -------------------------------------
# --------------------------------------------------------------------------

def flag(x, y, w=220, h=132, slices=24):
    sw = w / slices
    defs = (
        f'<g id="flagart"><rect width="{w}" height="{h}" fill="{BD_GREEN}"/>'
        f'<circle cx="{f(w*0.45)}" cy="{f(h/2)}" r="{f(w*0.2)}" fill="{BD_RED}"/></g>'
    )
    clips = ""
    body = f'<g transform="translate({x},{y})">'
    for i in range(slices):
        clips += (
            f'<clipPath id="fc{i}"><rect x="{f(i*sw)}" y="-30" width="{f(sw+0.7)}" height="{h+60}"/></clipPath>'
        )
        amp = 1.5 + 6.5 * (i / (slices - 1))
        steps = 8
        ys = ";".join(
            f"0 {f(amp*math.sin(2*math.pi*k/steps - i*0.55))}" for k in range(steps + 1)
        )
        shade = ";".join(
            f"{f(0.16 + 0.16*math.cos(2*math.pi*k/steps - i*0.55 ))}" for k in range(steps + 1)
        )
        body += (
            f'<g><animateTransform attributeName="transform" type="translate" values="{ys}" dur="1.9s" repeatCount="indefinite"/>'
            f'<use href="#flagart" clip-path="url(#fc{i})"/>'
            f'<rect x="{f(i*sw)}" y="-30" width="{f(sw+0.7)}" height="{h+60}" fill="#000" opacity="0.2" clip-path="url(#fcs{i})">'
            f'<animate attributeName="opacity" values="{shade}" dur="1.9s" repeatCount="indefinite"/></rect></g>'
        )
        clips += (
            f'<clipPath id="fcs{i}"><rect x="{f(i*sw)}" y="0" width="{f(sw+0.7)}" height="{h}"/></clipPath>'
        )
    body += "</g>"
    return defs + clips, body


# --------------------------------------------------------------------------
# Bangladesh map -------------------------------------------------------------
# --------------------------------------------------------------------------
BD_OUTLINE = [
    (88.45, 26.55), (88.62, 26.62), (88.78, 26.42), (88.95, 26.30), (89.10, 26.20),
    (89.45, 26.05), (89.80, 25.95), (89.85, 25.50), (89.82, 25.30), (90.25, 25.17),
    (90.65, 25.15), (91.20, 25.17), (91.65, 25.10), (92.05, 25.14), (92.28, 24.90),
    (92.20, 24.55), (92.25, 24.30), (92.10, 24.10), (91.85, 24.12), (91.62, 23.88),
    (91.58, 23.55), (91.35, 23.35), (91.40, 23.10), (91.60, 23.00), (91.80, 23.30),
    (92.00, 23.68), (92.30, 23.30), (92.45, 22.85), (92.55, 22.40), (92.62, 21.95),
    (92.50, 21.55), (92.35, 21.20), (92.30, 20.85), (92.34, 20.60), (92.12, 20.95),
    (91.98, 21.35), (91.92, 21.80), (91.82, 22.25), (91.55, 22.55), (91.30, 22.80),
    (91.00, 22.45), (90.75, 22.05), (90.40, 21.85), (90.00, 21.82), (89.62, 21.78),
    (89.25, 21.75), (89.08, 22.05), (89.10, 22.45), (88.92, 22.95), (88.76, 23.30),
    (88.62, 23.60), (88.78, 23.95), (88.50, 24.10), (88.20, 24.35), (88.03, 24.65),
    (88.20, 24.95), (88.50, 25.20), (88.40, 25.55), (88.22, 25.90), (88.15, 26.10),
    (88.38, 26.25),
]
DHAKA = (90.41, 23.81)


def project(lon, lat, ox, oy, k):
    x = ox + (lon - 88.0) * math.cos(math.radians(23.5)) * k
    y = oy + (26.7 - lat) * k
    return x, y


def bd_map(ox, oy, k=44):
    pts = [project(lo, la, ox, oy, k) for lo, la in BD_OUTLINE]
    d = "M" + " L".join(f"{f(x,1)},{f(y,1)}" for x, y in pts) + " Z"
    dx, dy = project(*DHAKA, ox, oy, k)
    body = (
        f'<path d="{d}" fill="url(#mapfill)" stroke="{GREEN}" stroke-opacity=".55" stroke-width="1.4" stroke-linejoin="round"/>'
        f'<path d="{d}" fill="none" stroke="#9FFFD9" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round" '
        f'pathLength="1" stroke-dasharray=".12 .88" filter="url(#glow)">'
        f'<animate attributeName="stroke-dashoffset" values="1;0" dur="6s" repeatCount="indefinite"/></path>'
        f'<circle cx="{f(dx,1)}" cy="{f(dy,1)}" r="3.4" fill="{BD_RED}"/>'
        f'<circle cx="{f(dx,1)}" cy="{f(dy,1)}" r="3.4" fill="none" stroke="{BD_RED}" stroke-width="1.5">'
        f'<animate attributeName="r" values="3;16" dur="2.2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0" dur="2.2s" repeatCount="indefinite"/></circle>'
        f'<text x="{f(dx+9,1)}" y="{f(dy+4,1)}" font-family="{SANS}" font-size="10" fill="#E7FFF6" letter-spacing="1">DHAKA</text>'
    )
    return body


# --------------------------------------------------------------------------
# UIU building -----------------------------------------------------------------
# --------------------------------------------------------------------------

def uiu_logo(cx, cy, r, logo_path=None):
    """Official logo if assets/uiu-logo.png exists, otherwise a clean emblem."""
    if logo_path and os.path.exists(logo_path):
        ext = os.path.splitext(logo_path)[1].lower().strip(".")
        mime = "image/png" if ext == "png" else "image/jpeg" if ext in ("jpg", "jpeg") else "image/svg+xml"
        data = base64.b64encode(open(logo_path, "rb").read()).decode()
        return (
            f'<circle cx="{cx}" cy="{cy}" r="{r+2}" fill="#fff"/>'
            f'<image href="data:{mime};base64,{data}" x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" preserveAspectRatio="xMidYMid meet"/>'
        )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0E2A52" stroke="{AMBER}" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r-5}" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1"/>'
        f'<path d="M{cx-r*0.42},{cy-r*0.45} v{r*0.55} a{r*0.42},{r*0.42} 0 0 0 {r*0.84},0 v-{r*0.55}" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>'
        f'<path d="M{cx},{cy-r*0.62} L{cx+r*0.18},{cy-r*0.2} L{cx-r*0.18},{cy-r*0.2} Z" fill="{AMBER}"/>'
    )


def building(logo_path=None):
    r = rng(7)
    body = ""
    gx = 992  # main tower left
    WL, WR = 92, 34  # wing widths
    top, base = 140, 400
    tw = 150
    # sky glow behind building
    body += f'<ellipse cx="1060" cy="300" rx="180" ry="170" fill="url(#bglow)"/>'

    # --- outline blueprint (draws itself) -----------------------------------
    def outline(d, delay):
        return (
            f'<path d="{d}" fill="none" stroke="#7DD3FC" stroke-width="1.6" stroke-linejoin="round" '
            f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="1;0;0;0;1" keyTimes="0;{delay};0.82;0.96;1" dur="12s" repeatCount="indefinite"/></path>'
        )

    # fills first (fade in after the blueprint has been drawn)
    fills = (
        f'<g><animate attributeName="opacity" values="0.15;1;1;0.15" keyTimes="0;0.32;0.92;1" dur="12s" repeatCount="indefinite"/>'
        f'<rect x="{gx}" y="{top}" width="{tw}" height="{base-top}" fill="url(#tower)"/>'
        f'<rect x="{gx-WL}" y="{top+70}" width="{WL}" height="{base-top-70}" fill="url(#wing)"/>'
        f'<rect x="{gx+tw}" y="{top+115}" width="{WR}" height="{base-top-115}" fill="url(#wing)"/>'
        f'<rect x="{gx-WL-8}" y="{base-34}" width="{tw+WL+WR+16}" height="34" fill="#101A2B"/></g>'
    )
    body += fills

    # structural grid: columns and floor beams
    cols = 7
    cw, cg = 14, 5
    wx0 = gx + (tw - (cols * cw + (cols - 1) * cg)) / 2
    rows_y = [top + 78 + i * 25 for i in range(9)]  # window rows on main tower
    beams = ""
    for ry in rows_y:
        beams += f'<rect x="{gx}" y="{ry+17}" width="{tw}" height="3" fill="#CBD5E1" opacity=".22"/>'
    body += f'<g>{beams}</g>'

    # windows (twinkle)
    wins = ""
    for ri, ry in enumerate(rows_y):
        if ry + 16 > base - 40:
            continue
        for c in range(cols):
            wx = wx0 + c * (cw + cg)
            lit = r.random() < 0.55
            col = r.choice(["#FFD27A", "#FFE9B0", "#9AD7FF"]) if lit else "#1B2A44"
            dur = r.uniform(3, 7)
            begin = r.uniform(0, 5)
            anim = ""
            if lit:
                anim = (
                    f'<animate attributeName="opacity" values="1;.35;1" dur="{f(dur)}s" begin="-{f(begin)}s" repeatCount="indefinite"/>'
                )
            else:
                if r.random() < 0.2:
                    anim = (
                        f'<animate attributeName="fill" values="#1B2A44;#FFD27A;#1B2A44" dur="{f(dur+3)}s" begin="-{f(begin)}s" repeatCount="indefinite"/>'
                    )
            wins += f'<rect x="{f(wx)}" y="{ry}" width="{cw}" height="16" rx="1.5" fill="{col}">{anim}</rect>'
    # left wing windows
    for ri in range(6):
        ry = top + 100 + ri * 25
        if ry + 16 > base - 40:
            continue
        for c in range(3):
            wx = gx - 84 + c * 26
            lit = r.random() < 0.5
            col = r.choice(["#FFD27A", "#9AD7FF"]) if lit else "#1B2A44"
            wins += (
                f'<rect x="{wx}" y="{ry}" width="16" height="16" rx="1.5" fill="{col}">'
                + (f'<animate attributeName="opacity" values="1;.3;1" dur="{f(r.uniform(3,6))}s" begin="-{f(r.uniform(0,4))}s" repeatCount="indefinite"/>' if lit else "")
                + "</rect>"
            )
    # right wing windows
    for ri in range(4):
        ry = top + 140 + ri * 25
        if ry + 16 > base - 40:
            continue
        for c in range(1):
            wx = gx + tw + 10
            lit = r.random() < 0.5
            col = "#FFD27A" if lit else "#1B2A44"
            wins += f'<rect x="{wx}" y="{ry}" width="14" height="16" rx="1.5" fill="{col}"/>'
    body += f"<g>{wins}</g>"

    # outlines
    body += outline(f"M{gx},{base-34} V{top} H{gx+tw} V{base-34}", 0.08)
    body += outline(f"M{gx-WL},{base-34} V{top+70} H{gx}", 0.14)
    body += outline(f"M{gx+tw},{top+115} H{gx+tw+WR} V{base-34}", 0.2)
    body += outline(f"M{gx-WL-8},{base-34} H{gx+tw+WR+8} V{base} H{gx-WL-8} Z", 0.26)
    for c in range(1, 4):
        xx = gx + c * tw / 4
        body += f'<line x1="{f(xx)}" y1="{top}" x2="{f(xx)}" y2="{base-34}" stroke="#E2E8F0" stroke-opacity=".10" stroke-width="2"/>'

    # roof truss + antenna
    tr = ""
    for i in range(8):
        x1 = gx + i * tw / 8
        tr += f'<path d="M{f(x1)},{top} l{f(tw/16)},-14 l{f(tw/16)},14" fill="none" stroke="#94A3B8" stroke-width="1.2" stroke-opacity=".7"/>'
    body += tr
    body += f'<line x1="{gx+tw-22}" y1="{top}" x2="{gx+tw-22}" y2="{top-36}" stroke="#94A3B8" stroke-width="2"/>'
    body += (
        f'<circle cx="{gx+tw-22}" cy="{top-38}" r="3.4" fill="#FF4D4D">'
        f'<animate attributeName="opacity" values="1;.1;1" dur="1.4s" repeatCount="indefinite"/></circle>'
    )

    # sign board with logo + UIU lettering
    sx, sy, sw_, sh = gx + 8, top + 14, tw - 16, 52
    body += (
        f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh}" rx="8" fill="#060B14" stroke="{ORANGE}" stroke-width="1.6" filter="url(#glow)">'
        f'<animate attributeName="stroke-opacity" values="1;.45;1" dur="3.2s" repeatCount="indefinite"/></rect>'
    )
    body += uiu_logo(sx + 28, sy + sh / 2, 19, logo_path)
    body += (
        f'<text x="{sx+54}" y="{sy+35}" font-family="{SANS}" font-weight="900" font-size="28" fill="#fff" '
        f'textLength="{sw_-62}" lengthAdjust="spacingAndGlyphs">UIU</text>'
    )

    # entrance + trees
    body += f'<rect x="{gx+tw/2-22}" y="{base-34}" width="44" height="34" fill="#0B1220" stroke="{AMBER}" stroke-opacity=".6"/>'
    for tx in (gx - WL - 2, gx - WL + 22, gx + tw + WR - 8):
        body += f'<circle cx="{tx}" cy="{base-44}" r="10" fill="#0F5132" opacity=".9"/><rect x="{tx-1.5}" y="{base-36}" width="3" height="10" fill="#3B2A1A"/>'
    # label
    body += (
        f'<text x="1040" y="{base+34}" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="11.5" fill="#E2E8F0" letter-spacing="1.6">UNITED INTERNATIONAL UNIVERSITY</text>'
        f'<text x="1040" y="{base+52}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{AMBER}" letter-spacing="3">DHAKA • BANGLADESH</text>'
    )
    return body


# --------------------------------------------------------------------------
# Neural net background ----------------------------------------------------
# --------------------------------------------------------------------------

def neural_net():
    layers = [(380, 4), (480, 5), (600, 6), (720, 5), (820, 4)]
    nodes = []
    for lx, n in layers:
        ys = [60 + (i + 0.5) * (350 / n) for i in range(n)]
        nodes.append([(lx, y) for y in ys])
    body = '<g opacity=".5">'
    r = rng(11)
    for a, b in zip(nodes, nodes[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                if r.random() < 0.55:
                    body += f'<line x1="{x1}" y1="{f(y1)}" x2="{x2}" y2="{f(y2)}" stroke="#38BDF8" stroke-opacity=".10"/>'
                    if r.random() < 0.12:
                        body += (
                            f'<line x1="{x1}" y1="{f(y1)}" x2="{x2}" y2="{f(y2)}" stroke="{ORANGE}" stroke-width="1.4" pathLength="1" stroke-dasharray=".18 .82">'
                            f'<animate attributeName="stroke-dashoffset" values="1;0" dur="{f(r.uniform(2.4,4.5))}s" begin="-{f(r.uniform(0,3))}s" repeatCount="indefinite"/></line>'
                        )
    for layer in nodes:
        for (x, y) in layer:
            d = r.uniform(2, 4)
            body += (
                f'<circle cx="{x}" cy="{f(y)}" r="3" fill="#0B111B" stroke="#38BDF8" stroke-opacity=".5">'
                f'<animate attributeName="r" values="2.5;4;2.5" dur="{f(d)}s" begin="-{f(r.uniform(0,3))}s" repeatCount="indefinite"/></circle>'
            )
    return body + "</g>"


# --------------------------------------------------------------------------
# Floating code glyphs -------------------------------------------------------
# --------------------------------------------------------------------------

def particles():
    glyphs = ["</>", "{ }", "01", "λ", "def", "NLP", "BERT", "∑", "git", "#!", "=>", "tf", "[ ]", "∇", "SQL", "bn→en"]
    r = rng(3)
    body = ""
    for i in range(22):
        x = r.randint(30, W - 30)
        y0 = r.randint(380, 450)
        dur = r.uniform(9, 16)
        col = r.choice(["#38BDF8", ORANGE, GREEN, "#A78BFA"])
        g = r.choice(glyphs)
        size = r.randint(11, 17)
        body += (
            f'<text x="{x}" y="{y0}" font-family="{MONO}" font-size="{size}" fill="{col}" opacity="0">{esc(g)}'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -{r.randint(260,380)}" dur="{f(dur)}s" begin="-{f(r.uniform(0,dur))}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.55;.55;0" keyTimes="0;.15;.8;1" dur="{f(dur)}s" begin="-{f(r.uniform(0,dur))}s" repeatCount="indefinite"/></text>'
        )
    return body


# --------------------------------------------------------------------------
# Assemble --------------------------------------------------------------------

def build(logo_path=None):
    flag_defs, flag_body = flag(56, 66)

    bio = "CSE Engineer | Major Data Science (NLP Domain)"
    bio_w = 470
    bx = CX - bio_w / 2
    steps = len(bio)
    kt = ";".join(f(i / steps * 0.62, 4) for i in range(steps + 1)) + ";0.92;1"
    widths = ";".join(f(i * bio_w / steps, 1) for i in range(steps + 1)) + f";{bio_w};0"
    curs = ";".join(f(bx + i * bio_w / steps, 1) for i in range(steps + 1)) + f";{f(bx+bio_w,1)};{f(bx,1)}"
    bio_cycle = "13s"

    name = "Muhtasim Masum Hasnayen"
    name_w = 500
    nx = CX - name_w / 2

    chips = ["NLP", "MACHINE LEARNING", "SQA & AUTOMATION", "WEB DEV"]
    chip_svg = ""
    cx0 = 0
    widths_c = [48, 138, 146, 84]
    total = sum(widths_c) + 14 * (len(chips) - 1)
    cx0 = CX - total / 2
    for i, (c, cw_) in enumerate(zip(chips, widths_c)):
        col = [ "#38BDF8", ORANGE, GREEN, "#A78BFA"][i]
        chip_svg += (
            f'<g opacity="1"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(0.06+i*0.04,3)};{f(0.12+i*0.04,3)};.92;1" dur="{bio_cycle}" repeatCount="indefinite"/>'
            f'<rect x="{f(cx0)}" y="344" width="{cw_}" height="24" rx="12" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".7"/>'
            f'<text x="{f(cx0+cw_/2)}" y="360" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{col}" letter-spacing="1.2">{esc(c)}</text></g>'
        )
        cx0 += cw_ + 14

    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03060B"/><stop offset=".6" stop-color="#08101D"/><stop offset="1" stop-color="#0B0A08"/></linearGradient>
<radialGradient id="gG"><stop offset="0" stop-color="#00A878" stop-opacity=".30"/><stop offset="1" stop-color="#00A878" stop-opacity="0"/></radialGradient>
<radialGradient id="gO"><stop offset="0" stop-color="#FF7A18" stop-opacity=".28"/><stop offset="1" stop-color="#FF7A18" stop-opacity="0"/></radialGradient>
<radialGradient id="gB"><stop offset="0" stop-color="#3B82F6" stop-opacity=".18"/><stop offset="1" stop-color="#3B82F6" stop-opacity="0"/></radialGradient>
<radialGradient id="bglow"><stop offset="0" stop-color="#FF7A18" stop-opacity=".22"/><stop offset="1" stop-color="#FF7A18" stop-opacity="0"/></radialGradient>
<linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#FFE3C2"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="ul" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{ORANGE}"/><stop offset="1" stop-color="{BD_RED}"/></linearGradient>
<linearGradient id="tower" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#16243C"/><stop offset="1" stop-color="#0A1222"/></linearGradient>
<linearGradient id="wing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1A2B47"/><stop offset="1" stop-color="#0C1627"/></linearGradient>
<linearGradient id="mapfill" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A7A5A" stop-opacity=".55"/><stop offset="1" stop-color="#033D2D" stop-opacity=".85"/></linearGradient>
<linearGradient id="border" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{ORANGE}"/><stop offset="1" stop-color="#38BDF8"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="nameclip"><text x="{nx}" y="232" font-family="{SANS}" font-weight="900" font-size="44" textLength="{name_w}" lengthAdjust="spacingAndGlyphs">{name}</text></clipPath>
<clipPath id="bioclip"><rect x="{f(bx,1)}" y="262" width="{bio_w}" height="34">
<animate attributeName="width" values="{widths}" keyTimes="{kt}" calcMode="discrete" dur="{bio_cycle}" repeatCount="indefinite"/></rect></clipPath>
<clipPath id="round"><rect x="0" y="0" width="{W}" height="{H}" rx="22"/></clipPath>
{flag_defs}
"""

    body = f'<g clip-path="url(#round)">'
    body += f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>'
    # aurora blobs
    body += (
        f'<circle cx="150" cy="300" r="280" fill="url(#gG)"><animateTransform attributeName="transform" type="translate" values="0 0;40 -20;0 0" dur="14s" repeatCount="indefinite"/></circle>'
        f'<circle cx="1060" cy="260" r="320" fill="url(#gO)"><animateTransform attributeName="transform" type="translate" values="0 0;-40 20;0 0" dur="16s" repeatCount="indefinite"/></circle>'
        f'<circle cx="600" cy="90" r="300" fill="url(#gB)"><animateTransform attributeName="transform" type="translate" values="0 0;30 20;0 0" dur="18s" repeatCount="indefinite"/></circle>'
    )
    body += neural_net()
    body += particles()

    # ---- left zone: flag + pole + map
    body += (
        f'<rect x="48" y="58" width="6" height="250" rx="3" fill="#B8C2D0"/><circle cx="51" cy="56" r="6" fill="{AMBER}"/>'
        f'<ellipse cx="51" cy="310" rx="14" ry="4" fill="#000" opacity=".5"/>'
    )
    body += flag_body
    body += bd_map(108, 226, k=29)
    body += (
        f'<text x="166" y="424" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="14" fill="#E7FFF6" letter-spacing="5">BANGLADESH</text>'
        f'<text x="166" y="442" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GREEN}" letter-spacing="3">MADE IN THE DELTA</text>'
    )

    # ---- centre: intro, name, bio
    body += (
        f'<text x="{CX}" y="148" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{ORANGE}" letter-spacing="6">'
        f'◆ HELLO WORLD, I\'M ◆<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.06;.92;1" dur="{bio_cycle}" repeatCount="indefinite"/></text>'
    )
    # name: soft shadow, outline draw, gradient fill, shimmer
    body += (
        f'<text x="{nx}" y="236" font-family="{SANS}" font-weight="900" font-size="44" textLength="{name_w}" lengthAdjust="spacingAndGlyphs" fill="{ORANGE}" opacity=".35" filter="url(#glow)">{name}</text>'
        f'<text x="{nx}" y="232" font-family="{SANS}" font-weight="900" font-size="44" textLength="{name_w}" lengthAdjust="spacingAndGlyphs" fill="url(#nameGrad)">{name}'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.92;1" dur="{bio_cycle}" repeatCount="indefinite"/></text>'
        f'<g clip-path="url(#nameclip)"><rect x="{nx-120}" y="180" width="110" height="70" fill="url(#sweep)" transform="skewX(-18)">'
        f'<animate attributeName="x" values="{nx-200};{nx+name_w+60}" dur="3.6s" repeatCount="indefinite"/></rect></g>'
    )
    # underline
    body += (
        f'<rect x="{CX-250}" y="248" width="500" height="3" rx="1.5" fill="url(#ul)" opacity=".95">'
        f'<animate attributeName="width" values="0;500;500;0" keyTimes="0;.12;.92;1" dur="{bio_cycle}" repeatCount="indefinite"/>'
        f'<animate attributeName="x" values="{CX};{CX-250};{CX-250};{CX}" keyTimes="0;.12;.92;1" dur="{bio_cycle}" repeatCount="indefinite"/></rect>'
        f'<circle cx="{CX-250}" cy="249.5" r="4" fill="#fff" filter="url(#glow)"><animate attributeName="cx" values="{CX-250};{CX+250}" dur="2.8s" repeatCount="indefinite"/></circle>'
    )
    # bio typing (mono-ish via textLength)
    body += (
        f'<g clip-path="url(#bioclip)"><text x="{f(bx,1)}" y="286" font-family="{MONO}" font-size="20" font-weight="600" fill="#E2E8F0" '
        f'textLength="{bio_w}" lengthAdjust="spacingAndGlyphs"><tspan fill="{AMBER}">CSE Engineer</tspan> <tspan fill="#64748B">|</tspan> <tspan fill="#fff">Major Data Science</tspan> <tspan fill="#38BDF8">(NLP Domain)</tspan></text></g>'
        f'<rect x="{f(bx,1)}" y="266" width="2.4" height="24" fill="{ORANGE}"><animate attributeName="x" values="{curs}" keyTimes="{kt}" calcMode="discrete" dur="{bio_cycle}" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0;1" dur=".9s" repeatCount="indefinite"/></rect>'
    )
    body += f'<text x="{CX}" y="326" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#94A3B8" letter-spacing="2">B.Sc. in CSE  ·  United International University</text>'
    body += chip_svg
    # tiny terminal line
    body += (
        f'<text x="{CX}" y="418" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#64748B">'
        f'<tspan fill="{GREEN}">~/masum</tspan> <tspan fill="#64748B">$</tspan> <tspan fill="#E2E8F0">python train.py --task nlp --lang bn</tspan>'
        f'<animate attributeName="opacity" values=".55;1;.55" dur="3s" repeatCount="indefinite"/></text>'
    )

    # ---- right zone: building
    body += building(logo_path)

    # frame
    body += (
        f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="url(#border)" stroke-width="2" pathLength="1" stroke-dasharray=".22 .78" opacity=".9">'
        f'<animate attributeName="stroke-dashoffset" values="1;0" dur="9s" repeatCount="indefinite"/></rect>'
        f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="#fff" stroke-opacity=".07"/>'
    )
    body += "</g>"
    return svg(W, H, body, defs, title="Muhtasim Masum Hasnayen — CSE Engineer | Data Science (NLP)", desc="Animated banner with the Bangladesh flag and map, name and bio, and the UIU building.")


if __name__ == "__main__":
    logo = os.path.join(ASSETS, "uiu-logo.png")
    write("banner.svg", build(logo))
