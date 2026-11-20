"""Project factory (animated pipeline) and animated project cards."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

# ---------------------------------------------------------------------------
# FACTORY PIPELINE
# ---------------------------------------------------------------------------
W, H = 1200, 330


def gear(cx, cy, r, teeth, color, dur, direction=1, hole=0.35):
    pts = []
    for i in range(teeth * 2):
        ang = math.pi * i / teeth
        rr = r if i % 2 == 0 else r * 0.8
        for da in (-0.5, 0.5):
            a = ang + da * math.pi / teeth * 0.9
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d = "M" + " L".join(f"{f(x,1)},{f(y,1)}" for x, y in pts) + " Z"
    to = 360 * direction
    return (
        f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{to} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<path d="{d}" fill="{color}" stroke="#0B111B" stroke-width="1.5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r*hole}" fill="#0B111B"/></g>'
    )


def station_frame(x, label, num, color):
    return (
        f'<rect x="{x-64}" y="96" width="8" height="114" fill="#1E293B"/><rect x="{x+56}" y="96" width="8" height="114" fill="#1E293B"/>'
        f'<rect x="{x-70}" y="90" width="140" height="10" rx="3" fill="#273449"/>'
        f'<rect x="{x-58}" y="28" width="116" height="26" rx="13" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".8"/>'
        f'<text x="{x}" y="46" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="800" fill="{color}" letter-spacing="2">{num} {label}</text>'
        f'<line x1="{x}" y1="54" x2="{x}" y2="90" stroke="{color}" stroke-opacity=".4" stroke-dasharray="3 4"/>'
    )


def st_design(x):
    s = f'<rect x="{x-44}" y="104" width="88" height="62" rx="5" fill="#0B2340" stroke="#38BDF8" stroke-opacity=".7"/>'
    for i in range(1, 8):
        s += f'<line x1="{x-44+i*11}" y1="104" x2="{x-44+i*11}" y2="166" stroke="#38BDF8" stroke-opacity=".12"/>'
    for j in range(1, 6):
        s += f'<line x1="{x-44}" y1="{104+j*10.3}" x2="{x+44}" y2="{104+j*10.3}" stroke="#38BDF8" stroke-opacity=".12"/>'
    paths = [
        f"M{x-34},{158} V{120} H{x-8} V{158} Z",
        f"M{x+2},{158} V{132} H{x+34} V{158}",
        f"M{x-34},{120} L{x-21},{110} L{x-8},{120}",
    ]
    for i, d in enumerate(paths):
        s += (
            f'<path d="{d}" fill="none" stroke="#7DD3FC" stroke-width="2" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;{f(.25+i*.12,2)};.9;1" dur="6s" repeatCount="indefinite"/></path>'
        )
    s += (
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;30 -18;-6 -6;0 0" dur="6s" repeatCount="indefinite"/>'
        f'<path d="M{x-40},{160} l14,-14 l4,4 l-14,14 z" fill="{AMBER}"/><path d="M{x-40},{160} l-2,6 l6,-2 z" fill="#F1F5F9"/></g>'
    )
    s += f'<text x="{x}" y="186" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#64748B">wireframes · schema · API</text>'
    return s


def st_build(x):
    s = gear(x - 18, 150, 28, 10, "#FF7A18", 6) + gear(x + 22, 130, 18, 8, "#FFB347", 6 * 18 / 28, -1)
    # robot arm
    s += (
        f'<g transform="translate({x+36},206)"><rect x="-10" y="-8" width="20" height="8" fill="#334155"/>'
        f'<g><animateTransform attributeName="transform" type="rotate" values="-28 0 -8;18 0 -8;-28 0 -8" dur="1.6s" repeatCount="indefinite"/>'
        f'<rect x="-4" y="-62" width="8" height="56" rx="3" fill="#94A3B8"/>'
        f'<g transform="translate(0,-62)"><g><animateTransform attributeName="transform" type="rotate" values="30 0 0;-20 0 0;30 0 0" dur="1.6s" repeatCount="indefinite"/>'
        f'<rect x="-3" y="-36" width="6" height="36" rx="3" fill="#CBD5E1"/>'
        f'<circle cx="0" cy="-38" r="4" fill="#FF4D4D"><animate attributeName="r" values="2;6;2" dur=".25s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.3;1" dur=".25s" repeatCount="indefinite"/></circle>'
        f'</g></g></g></g>'
    )
    # sparks
    r = rng(9)
    for i in range(6):
        ang = r.uniform(-2.6, -0.5)
        s += (
            f'<line x1="{x+34}" y1="150" x2="{x+34+math.cos(ang)*8}" y2="{150+math.sin(ang)*8}" stroke="#FFD27A" stroke-width="1.6" stroke-linecap="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;0" dur=".5s" begin="{f(i*.17)}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{f(math.cos(ang)*22)} {f(math.sin(ang)*22)}" dur=".5s" begin="{f(i*.17)}s" repeatCount="indefinite"/></line>'
        )
    s += f'<text x="{x}" y="226" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#64748B">code · commit · iterate</text>'
    return s


def st_test(x):
    s = f'<rect x="{x-44}" y="104" width="88" height="62" rx="5" fill="#0B1F1A" stroke="#22C55E" stroke-opacity=".7"/>'
    for i in range(3):
        ry = 114 + i * 17
        s += f'<rect x="{x-36}" y="{ry}" width="40" height="6" rx="3" fill="#134E3A"/>'
        s += (
            f'<path d="M{x+14},{ry+3} l4,4 l9,-9" fill="none" stroke="#22C55E" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="1;1;0;0;1" keyTimes="0;{f(.1+i*.2,2)};{f(.2+i*.2,2)};.9;1" dur="5s" repeatCount="indefinite"/></path>'
        )
    # bug squashed
    s += (
        f'<g><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.3;.35;.95;1" dur="5s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="translate" values="-40 0;0 0;0 0" keyTimes="0;.3;1" dur="5s" repeatCount="indefinite"/>'
        f'<ellipse cx="{x-6}" cy="176" rx="6" ry="4" fill="#F43F5E"/><circle cx="{x+1}" cy="176" r="2.6" fill="#F43F5E"/></g>'
    )
    s += f'<g><animateTransform attributeName="transform" type="translate" values="-30 0;30 0;-30 0" dur="3s" repeatCount="indefinite"/><circle cx="{x}" cy="190" r="8" fill="none" stroke="#7DD3FC" stroke-width="2"/><line x1="{x+6}" y1="196" x2="{x+12}" y2="202" stroke="#7DD3FC" stroke-width="3" stroke-linecap="round"/></g>'
    s += f'<text x="{x}" y="226" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#64748B">unit · API · E2E · regression</text>'
    return s


def st_ship(x):
    s = f'<rect x="{x-34}" y="198" width="68" height="8" rx="3" fill="#334155"/>'
    s += (
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -130;0 -130" keyTimes="0;.45;.75;1" dur="5s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;1;1;0;0" keyTimes="0;.45;.7;.85;1" dur="5s" repeatCount="indefinite"/>'
        f'<path d="M{x},{120} C{x+14},{136} {x+14},{170} {x+9},{190} H{x-9} C{x-14},{170} {x-14},{136} {x},{120} Z" fill="#E2E8F0"/>'
        f'<circle cx="{x}" cy="150" r="6" fill="#38BDF8" stroke="#0B111B" stroke-width="2"/>'
        f'<path d="M{x-9},{176} l-12,16 l12,-4 z M{x+9},{176} l12,16 l-12,-4 z" fill="{BD_RED}"/>'
        f'<path d="M{x-5},{190} q5,24 10,0 z" fill="{ORANGE}"><animate attributeName="d" values="M{x-5},190 q5,14 10,0 z;M{x-5},190 q5,34 10,0 z;M{x-5},190 q5,14 10,0 z" dur=".3s" repeatCount="indefinite"/></path></g>'
    )
    for i in range(4):
        s += (
            f'<circle cx="{x+(-1)**i*(8+i*4)}" cy="196" r="6" fill="#94A3B8" opacity="0"><animate attributeName="opacity" values="0;0;.5;0" keyTimes="0;.45;.6;1" dur="5s" repeatCount="indefinite"/>'
            f'<animate attributeName="r" values="3;3;16;22" keyTimes="0;.45;.7;1" dur="5s" repeatCount="indefinite"/></circle>'
        )
    s += f'<text x="{x}" y="226" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#64748B">deploy · monitor · improve</text>'
    return s


def pipeline():
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060A12"/><stop offset="1" stop-color="#0C111B"/></linearGradient>
<linearGradient id="belt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B3445"/><stop offset="1" stop-color="#151B26"/></linearGradient>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>
"""
    stations = [(210, "DESIGN", "01", "#38BDF8", st_design), (480, "BUILD", "02", ORANGE, st_build), (750, "TEST", "03", "#22C55E", st_test), (1020, "SHIP", "04", "#A78BFA", st_ship)]
    b = '<g clip-path="url(#round)">'
    b += f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>'
    b += f'<ellipse cx="600" cy="230" rx="560" ry="60" fill="{ORANGE}" opacity=".05"/>'
    # title
    b += (
        f'<text x="40" y="20" font-family="{MONO}" font-size="11" fill="#64748B" letter-spacing="3">PROJECT FACTORY</text>'
        f'<text x="1160" y="20" text-anchor="end" font-family="{MONO}" font-size="11" fill="#64748B" letter-spacing="2">idea → code → test → ship</text>'
    )
    # pipes + steam
    b += f'<path d="M0,64 H1200" stroke="#18212F" stroke-width="10"/><path d="M0,64 H1200" stroke="#fff" stroke-opacity=".04" stroke-width="2"/>'
    for sx, st_, col, fn in [(s[0], s[1], s[3], s[4]) for s in stations]:
        pass
    for x, label, num, col, fn in stations:
        b += station_frame(x, label, num, col)
        b += fn(x)
    # belt
    b += f'<rect x="0" y="240" width="1200" height="26" fill="url(#belt)"/><rect x="0" y="266" width="1200" height="6" fill="#0A0E15"/>'
    b += (
        f'<line x1="0" y1="253" x2="1200" y2="253" stroke="#475569" stroke-width="3" stroke-dasharray="14 12">'
        f'<animate attributeName="stroke-dashoffset" values="0;-26" dur=".8s" repeatCount="indefinite"/></line>'
    )
    for i in range(0, 1200, 60):
        b += f'<circle cx="{i+20}" cy="282" r="9" fill="#18202D" stroke="#334155"><animateTransform attributeName="transform" type="rotate" values="0 {i+20} 282;360 {i+20} 282" dur="2.4s" repeatCount="indefinite"/></circle><line x1="{i+20}" y1="274" x2="{i+20}" y2="290" stroke="#334155"/>'
    # packages
    labels = ["{ }", "</>", "NLP", "API", "QA"]
    fr = [(210 + 80) / 1330, (480 + 80) / 1330, (750 + 80) / 1330, (1020 + 80) / 1330]
    kts = "0;" + ";".join(f(v, 3) for v in fr)
    vals = "#475569;#3B82F6;#F59E0B;#22C55E;#A78BFA"
    dur = 15
    for i in range(5):
        beg = -i * dur / 5
        b += (
            f'<g><animateTransform attributeName="transform" type="translate" values="-80 0;1250 0" dur="{dur}s" begin="{f(beg,2)}s" repeatCount="indefinite"/>'
            f'<rect x="0" y="212" width="54" height="30" rx="6" fill="#475569" stroke="#fff" stroke-opacity=".25">'
            f'<animate attributeName="fill" values="{vals}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" begin="{f(beg,2)}s" repeatCount="indefinite"/></rect>'
            f'<rect x="4" y="216" width="46" height="4" rx="2" fill="#fff" opacity=".35"/>'
            f'<text x="27" y="236" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="800" fill="#fff">{esc(labels[i])}</text></g>'
        )
    # bottom stats strip
    stats = [("22", "REPOSITORIES"), ("46", "FOLLOWERS"), ("∞", "CUPS OF COFFEE"), ("24/7", "LEARNING MODE")]
    for i, (v, l) in enumerate(stats):
        x = 150 + i * 300
        b += (
            f'<text x="{x}" y="312" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="900" fill="{AMBER}">{v}'
            f'<animate attributeName="opacity" values=".7;1;.7" dur="{3+i}s" repeatCount="indefinite"/></text>'
            f'<text x="{x+34}" y="312" font-family="{MONO}" font-size="10" fill="#64748B" letter-spacing="2" text-anchor="start">{l}</text>'
        )
    b += f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="#fff" stroke-opacity=".08"/>'
    b += (
        f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="{ORANGE}" stroke-width="2" pathLength="1" stroke-dasharray=".12 .88" opacity=".8">'
        f'<animate attributeName="stroke-dashoffset" values="0;-1" dur="10s" repeatCount="indefinite"/></rect>'
    )
    b += "</g>"
    return svg(W, H, b, defs, title="Project factory", desc="Animated pipeline showing projects moving through design, build, test and ship stations.")


# ---------------------------------------------------------------------------
# PROJECT CARDS
# ---------------------------------------------------------------------------
CARD_W, CARD_H = 380, 168

PROJECTS = [
    dict(slug="covercraft", name="CoverCraft", tag="WEB APP", color="#38BDF8",
         desc="Assignment cover page generator with professional, customizable templates.",
         tech=["Next.js", "TypeScript"], meta="★ 4"),
    dict(slug="academic-hub", name="Academic-Hub-UIU", tag="DESKTOP", color="#F59E0B",
         desc="Academic hub built around the day-to-day needs of UIU students.",
         tech=["Java", "OOP"], meta="★ 6"),
    dict(slug="ticket", name="Ticket Management System", tag="WEB APP", color="#22C55E",
         desc="Ticketing platform for creating, assigning and tracking support requests end to end.",
         tech=["PHP", "MySQL"], meta="★ 7"),
    dict(slug="portfolio", name="Portfolio", tag="LIVE", color="#A78BFA",
         desc="Personal portfolio: projects, skills and contact, deployed on Vercel.",
         tech=["TypeScript", "Vercel"], meta="★ 7  ⑂ 2"),
    dict(slug="wishora", name="Wishora", tag="WEB APP", color="#F43F5E",
         desc="Full-stack TypeScript web application, built and shipped end to end.",
         tech=["TypeScript", "Web"], meta="★ 5"),
    dict(slug="ecommerce-qa", name="E-Commerce QA Automation", tag="QA", color="#14B8A6",
         desc="End-to-end, API and regression test suites for an e-commerce flow.",
         tech=["Playwright", "API", "Regression"], meta="QA"),
    dict(slug="ai-testgen", name="AI Test Case Generator", tag="AI + QA", color="#FF7A18",
         desc="Generates structured test cases from requirements using AI.",
         tech=["AI", "QA", "Automation"], meta="AI"),
    dict(slug="smartkrishi", name="SmartKrishi", tag="AGRI-TECH", color="#84CC16",
         desc="Smart agriculture web platform for Bangladeshi farmers.",
         tech=["PHP", "MySQL", "Web"], meta="WEB"),
    dict(slug="adaptive-mfa", name="Adaptive MFA", tag="ML + SEC", color="#EC4899",
         desc="Risk-based multi-factor authentication powered by machine learning.",
         tech=["ML", "Security", "Risk Analysis"], meta="ML"),
]


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 <= width:
            cur = f"{cur} {w_}".strip()
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def card(p, idx):
    c = p["color"]
    r = rng(idx * 17 + 3)
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E1522"/><stop offset="1" stop-color="#090D15"/></linearGradient>
<radialGradient id="g"><stop offset="0" stop-color="{c}" stop-opacity=".35"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>
<clipPath id="r"><rect width="{CARD_W}" height="{CARD_H}" rx="16"/></clipPath>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""
    b = '<g clip-path="url(#r)">'
    b += f'<rect width="{CARD_W}" height="{CARD_H}" fill="url(#bg)"/>'
    b += f'<circle cx="{CARD_W-40}" cy="30" r="110" fill="url(#g)"><animateTransform attributeName="transform" type="translate" values="0 0;-30 20;0 0" dur="{6+idx%4}s" repeatCount="indefinite"/></circle>'
    # icon medallion
    b += (
        f'<circle cx="46" cy="50" r="24" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".8"/>'
        f'<circle cx="46" cy="50" r="24" fill="none" stroke="{c}" stroke-width="2" pathLength="1" stroke-dasharray=".25 .75" filter="url(#glow)"><animateTransform attributeName="transform" type="rotate" values="0 46 50;360 46 50" dur="5s" repeatCount="indefinite"/></circle>'
        f'<text x="46" y="57" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="900" fill="{c}">{esc(p["name"][0])}</text>'
    )
    # title + tag
    b += f'<text x="82" y="46" font-family="{SANS}" font-size="16" font-weight="800" fill="#F1F5F9">{esc(p["name"])}</text>'
    b += f'<rect x="82" y="55" width="{len(p["tag"])*7+16}" height="17" rx="8.5" fill="{c}" fill-opacity=".15"/><text x="{82+(len(p["tag"])*7+16)/2}" y="67" text-anchor="middle" font-family="{MONO}" font-size="9.5" font-weight="800" fill="{c}" letter-spacing="1.5">{esc(p["tag"])}</text>'
    b += f'<text x="{CARD_W-18}" y="30" text-anchor="end" font-family="{MONO}" font-size="11" fill="#94A3B8">{esc(p["meta"])}</text>'
    # description
    for i, line in enumerate(wrap(p["desc"], 46)[:3]):
        b += f'<text x="22" y="{98+i*16}" font-family="{SANS}" font-size="12.5" fill="#B6C2D3">{esc(line)}</text>'
    # tech chips
    cx = 22
    for t in p["tech"]:
        wd = len(t) * 6.6 + 18
        b += (
            f'<rect x="{f(cx)}" y="{CARD_H-34}" width="{f(wd)}" height="20" rx="10" fill="none" stroke="{c}" stroke-opacity=".55"/>'
            f'<text x="{f(cx+wd/2)}" y="{CARD_H-20}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{c}">{esc(t)}</text>'
        )
        cx += wd + 8
    # equalizer / activity bars
    for i in range(7):
        bx = CARD_W - 20 - (7 - i) * 8
        hh = r.randint(8, 22)
        b += (
            f'<rect x="{bx}" y="{CARD_H-16-hh}" width="4.5" height="{hh}" rx="2" fill="{c}" opacity=".85">'
            f'<animate attributeName="height" values="{hh};{r.randint(5,26)};{hh}" dur="{f(r.uniform(1.0,2.2))}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{CARD_H-16-hh};{CARD_H-16-r.randint(5,26)};{CARD_H-16-hh}" dur="{f(r.uniform(1.0,2.2))}s" repeatCount="indefinite"/></rect>'
        )
    b += "</g>"
    b += f'<rect x="1.5" y="1.5" width="{CARD_W-3}" height="{CARD_H-3}" rx="15" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="1.5"/>'
    b += (
        f'<rect x="1.5" y="1.5" width="{CARD_W-3}" height="{CARD_H-3}" rx="15" fill="none" stroke="{c}" stroke-width="2" pathLength="1" stroke-dasharray=".2 .8">'
        f'<animate attributeName="stroke-dashoffset" values="1;0" dur="{5+idx%3}s" repeatCount="indefinite"/></rect>'
    )
    return svg(CARD_W, CARD_H, b, defs, title=p["name"], desc=p["desc"])


if __name__ == "__main__":
    write("pipeline.svg", pipeline())
    for i, p in enumerate(PROJECTS):
        write(f"card-{p['slug']}.svg", card(p, i))
