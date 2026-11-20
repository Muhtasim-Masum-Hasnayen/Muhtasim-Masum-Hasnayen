"""Headings, divider, roles ticker, about terminal + radar, skills marquee, footer."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

GLOW = '<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'


# ---------------------------------------------------------------------------
def heading(slug, text, sub, color=ORANGE):
    W, H = 1200, 76
    tw = len(text) * 20 + 10
    defs = f"""
<linearGradient id="t" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{color}"/></linearGradient>
<linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>
{GLOW}"""
    b = f'<rect width="{W}" height="{H}" fill="none"/>'
    b += (
        f'<rect x="8" y="14" width="6" height="40" rx="3" fill="{color}" filter="url(#glow)">'
        f'<animate attributeName="height" values="14;40;40;14" keyTimes="0;.15;.9;1" dur="6s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="27;14;14;27" keyTimes="0;.15;.9;1" dur="6s" repeatCount="indefinite"/></rect>'
        f'<text x="30" y="42" font-family="{SANS}" font-size="30" font-weight="900" letter-spacing="4" fill="url(#t)">{esc(text)}</text>'
        f'<text x="32" y="64" font-family="{MONO}" font-size="12" fill="#64748B" letter-spacing="2.5">{esc(sub)}</text>'
        f'<rect x="{tw+60}" y="34" width="{W-tw-70}" height="2" fill="url(#l)" opacity=".7"/>'
        f'<circle cy="35" r="4" fill="#fff" filter="url(#glow)"><animate attributeName="cx" values="{tw+60};{W-20}" dur="3.6s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" dur="3.6s" repeatCount="indefinite"/></circle>'
    )
    return svg(W, H, b, defs, title=text)


# ---------------------------------------------------------------------------
def divider():
    W, H = 1200, 30
    defs = f"""
<linearGradient id="d" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0"/><stop offset=".5" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient>
{GLOW}"""
    b = f'<rect x="60" y="14" width="1080" height="2" fill="url(#d)" opacity=".6"/>'
    b += (
        f'<circle cy="15" r="3.4" fill="#fff" filter="url(#glow)"><animate attributeName="cx" values="60;1140;60" dur="7s" repeatCount="indefinite"/></circle>'
        f'<g transform="translate(600,15)"><rect x="-7" y="-7" width="14" height="14" fill="#05080D" stroke="{ORANGE}" stroke-width="2" transform="rotate(45)" filter="url(#glow)">'
        f'<animateTransform attributeName="transform" type="rotate" values="45;225;405" dur="8s" repeatCount="indefinite"/></rect></g>'
    )
    return svg(W, H, b, defs)


# ---------------------------------------------------------------------------
def roles():
    W, H = 900, 64
    items = [
        ("CSE Engineer", AMBER),
        ("Data Science  •  NLP", "#38BDF8"),
        ("Software Testing  &  QA Automation", GREEN),
        ("Web Developer  •  Problem Solver", "#A78BFA"),
        ("Always Learning. Always Building.", ORANGE),
    ]
    n = len(items)
    cyc = 3.2 * n
    b = f'<text x="{W/2}" y="14" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#475569" letter-spacing="4">I AM A</text>'
    defs = GLOW
    for i, (t, col) in enumerate(items):
        w = len(t) * 15.5
        x0 = W / 2 - w / 2
        s = i / n
        e = (i + 1) / n
        kt = f"0;{f(s,4)};{f(s+0.45/n,4)};{f(e-0.1/n,4)};{f(e,4)};1"
        defs += (
            f'<clipPath id="rc{i}"><rect x="{f(x0)}" y="20" width="{f(w+4)}" height="40">'
            f'<animate attributeName="width" values="0;0;{f(w+4)};{f(w+4)};0;0" keyTimes="{kt}" dur="{cyc}s" repeatCount="indefinite"/></rect></clipPath>'
        )
        b += (
            f'<text x="{f(x0)}" y="50" font-family="{MONO}" font-size="26" font-weight="800" fill="{col}" xml:space="preserve" style="white-space:pre" textLength="{f(w)}" lengthAdjust="spacingAndGlyphs" clip-path="url(#rc{i})">{esc(t)}</text>'
            f'<rect y="26" width="3" height="28" fill="{col}" opacity="0">'
            f'<animate attributeName="x" values="{f(x0)};{f(x0)};{f(x0+w+4)};{f(x0+w+4)};{f(x0)};{f(x0)}" keyTimes="{kt}" dur="{cyc}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;1;0;0" keyTimes="{kt}" dur="{cyc}s" repeatCount="indefinite"/></rect>'
        )
    return svg(W, H, b, defs, title="Roles")


# ---------------------------------------------------------------------------
def about():
    W, H = 1200, 360
    LINES = [
        [("$ ", GREEN), ("whoami", "#F1F5F9")],
        [("muhtasim-masum-hasnayen", AMBER)],
        [("$ ", GREEN), ("cat profile.json", "#F1F5F9")],
        [("{", "#94A3B8")],
        [('  "role"', "#7DD3FC"), (": ", "#94A3B8"), ('"CSE Engineer"', "#A7F3D0"), (",", "#94A3B8")],
        [('  "major"', "#7DD3FC"), (": ", "#94A3B8"), ('"Data Science (NLP Domain)"', "#A7F3D0"), (",", "#94A3B8")],
        [('  "university"', "#7DD3FC"), (": ", "#94A3B8"), ('"United International University"', "#A7F3D0"), (",", "#94A3B8")],
        [('  "location"', "#7DD3FC"), (": ", "#94A3B8"), ('"Dhaka, Bangladesh"', "#A7F3D0"), (",", "#94A3B8")],
        [('  "focus"', "#7DD3FC"), (": ", "#94A3B8"), ('["NLP", "ML", "QA Automation", "Web"]', "#FDBA74"), (",", "#94A3B8")],
        [('  "status"', "#7DD3FC"), (": ", "#94A3B8"), ('"open to collaborate"', "#A7F3D0")],
        [("}", "#94A3B8")],
        [("$ ", GREEN), ("_", ORANGE)],
    ]
    cw = 8.45
    cyc = 15.0
    x0, y0, lh = 56, 98, 20.5
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060A12"/><stop offset="1" stop-color="#0B101A"/></linearGradient>
<linearGradient id="rad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".55"/><stop offset="1" stop-color="{ORANGE}" stop-opacity=".12"/></linearGradient>
<clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>
{GLOW}"""
    b = '<g clip-path="url(#round)">'
    b += f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    # terminal window
    b += f'<rect x="24" y="24" width="712" height="{H-48}" rx="14" fill="#070B13" stroke="#1E293B"/>'
    b += f'<rect x="24" y="24" width="712" height="34" rx="14" fill="#0E1624"/><rect x="24" y="44" width="712" height="14" fill="#0E1624"/>'
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b += f'<circle cx="{46+i*20}" cy="41" r="6" fill="{col}"/>'
    b += f'<text x="380" y="46" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#64748B">masum@dhaka: ~/about</text>'
    for i, toks in enumerate(LINES):
        text = "".join(t for t, _ in toks)
        wpx = len(text) * cw
        s = 0.03 + i * 0.062
        e = s + 0.045
        kt = f"0;{f(s,3)};{f(e,3)};0.94;1"
        vals = f"0;0;{f(wpx+6,1)};{f(wpx+6,1)};0"
        ly = y0 + i * lh
        tsp = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in toks)
        defs += (
            f'<clipPath id="al{i}"><rect x="{x0}" y="{ly-15}" width="{f(wpx+6,1)}" height="{lh}">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{cyc}s" repeatCount="indefinite"/></rect></clipPath>'
        )
        b += f'<text x="{x0}" y="{ly}" font-family="{MONO}" font-size="14" xml:space="preserve" style="white-space:pre" textLength="{f(wpx,1)}" lengthAdjust="spacingAndGlyphs" clip-path="url(#al{i})">{tsp}</text>'
    # radar
    cx, cy, R = 960, 204, 100
    axes = [("WEB DEV", 90), ("SOFTWARE TESTING", 90), ("TEST AUTOMATION", 80), ("API TESTING", 80), ("AI / ML", 60)]
    b += f'<text x="{cx}" y="44" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#64748B" letter-spacing="4">FOCUS RADAR</text>'
    for ring in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(
            f"{f(cx+R*ring*math.sin(2*math.pi*k/5),1)},{f(cy-R*ring*math.cos(2*math.pi*k/5),1)}" for k in range(5)
        )
        b += f'<polygon points="{pts}" fill="none" stroke="#fff" stroke-opacity="{.05 if ring<1 else .12}"/>'
    final, start = [], []
    for k, (lab, v) in enumerate(axes):
        a = 2 * math.pi * k / 5
        ex, ey = cx + R * math.sin(a), cy - R * math.cos(a)
        b += f'<line x1="{cx}" y1="{cy}" x2="{f(ex,1)}" y2="{f(ey,1)}" stroke="#fff" stroke-opacity=".08"/>'
        px, py = cx + R * v / 100 * math.sin(a), cy - R * v / 100 * math.cos(a)
        final.append(f"{f(px,1)},{f(py,1)}")
        start.append(f"{cx},{cy}")
        lx, ly_ = cx + (R + 24) * math.sin(a), cy - (R + 24) * math.cos(a)
        anc = "middle" if abs(math.sin(a)) < 0.2 else ("start" if math.sin(a) > 0 else "end")
        b += f'<text x="{f(lx,1)}" y="{f(ly_+4,1)}" text-anchor="{anc}" font-family="{MONO}" font-size="10" fill="#94A3B8" letter-spacing="1">{lab}</text>'
        b += f'<text x="{f(lx,1)}" y="{f(ly_+17,1)}" text-anchor="{anc}" font-family="{SANS}" font-size="11" font-weight="800" fill="{AMBER}">{v}%</text>'
    fp, sp = " ".join(final), " ".join(start)
    b += (
        f'<polygon points="{fp}" fill="url(#rad)" stroke="{ORANGE}" stroke-width="2.2" stroke-linejoin="round" filter="url(#glow)">'
        f'<animate attributeName="points" values="{sp};{fp};{fp};{sp}" keyTimes="0;.14;.92;1" dur="{cyc}s" repeatCount="indefinite"/></polygon>'
    )
    for k, p in enumerate(final):
        px, py = p.split(",")
        b += (
            f'<circle cx="{px}" cy="{py}" r="4" fill="#fff" stroke="{ORANGE}" stroke-width="2">'
            f'<animate attributeName="r" values="3;5.5;3" dur="{2+k*.3}s" repeatCount="indefinite"/></circle>'
        )
    b += (
        f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-R}" stroke="{ORANGE}" stroke-width="1.5" stroke-opacity=".7">'
        f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="6s" repeatCount="indefinite"/></line>'
    )
    b += "</g>"
    b += f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="#fff" stroke-opacity=".08"/>'
    return svg(W, H, b, defs, title="About Muhtasim Masum Hasnayen")


# ---------------------------------------------------------------------------
def marquee_row(items, y, direction, dur, h=38):
    chips, x = [], 0
    for name, col in items:
        w = len(name) * 8.2 + 44
        chips.append((x, w, name, col))
        x += w + 14
    total = x
    def row(offset):
        s = ""
        for cx_, w, name, col in chips:
            s += (
                f'<g transform="translate({f(cx_+offset)},{y})">'
                f'<rect width="{f(w)}" height="{h}" rx="{h/2}" fill="#0C1320" stroke="{col}" stroke-opacity=".6"/>'
                f'<circle cx="20" cy="{h/2}" r="5" fill="{col}"/>'
                f'<text x="34" y="{h/2+5}" font-family="{MONO}" font-size="13.5" font-weight="700" fill="#E2E8F0">{esc(name)}</text></g>'
            )
        return s
    a, b_ = (0, -total) if direction < 0 else (-total, 0)
    return (
        f'<g><animateTransform attributeName="transform" type="translate" values="{f(a)} 0;{f(b_)} 0" dur="{dur}s" repeatCount="indefinite"/>'
        + row(0) + row(total) + row(total * 2) + "</g>"
    )


def skills():
    W, H = 1200, 150
    r1 = [("Python", "#FFD43B"), ("Java", "#F89820"), ("C++", "#659AD2"), ("PHP", "#8892BF"), ("JavaScript", "#F7DF1E"), ("TypeScript", "#3178C6"), ("SQL / MySQL", "#00A8E8"), ("HTML5", "#E34F26"), ("CSS3", "#1572B6"), ("Next.js", "#FFFFFF")]
    r2 = [("NLP", "#38BDF8"), ("Machine Learning", ORANGE), ("TensorFlow", "#FF6F00"), ("PyTorch", "#EE4C2C"), ("scikit-learn", "#F7931E"), ("Pandas", "#8B5CF6"), ("NumPy", "#4DABCF"), ("Playwright", "#2EAD33"), ("Postman", "#FF6C37"), ("Jira", "#2684FF"), ("Git & GitHub", "#F1F5F9")]
    defs = f"""
<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#05080D"/><stop offset=".07" stop-color="#05080D" stop-opacity="0"/><stop offset=".93" stop-color="#05080D" stop-opacity="0"/><stop offset="1" stop-color="#05080D"/></linearGradient>
<clipPath id="round"><rect width="{W}" height="{H}" rx="18"/></clipPath>"""
    b = '<g clip-path="url(#round)">'
    b += f'<rect width="{W}" height="{H}" fill="#05080D"/>'
    b += marquee_row(r1, 24, -1, 38) + marquee_row(r2, 88, 1, 46)
    b += f'<rect width="{W}" height="{H}" fill="url(#edge)"/>'
    b += "</g>"
    b += f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="#fff" stroke-opacity=".08"/>'
    return svg(W, H, b, defs, title="Skills")


# ---------------------------------------------------------------------------
def footer():
    W, H = 1200, 220
    defs = f"""
<linearGradient id="w1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".55"/><stop offset="1" stop-color="{ORANGE}" stop-opacity=".05"/></linearGradient>
<linearGradient id="w2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB347" stop-opacity=".35"/><stop offset="1" stop-color="#FFB347" stop-opacity=".03"/></linearGradient>
<linearGradient id="w3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B1208"/><stop offset="1" stop-color="#05080D"/></linearGradient>
<linearGradient id="tt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
<clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>{GLOW}"""

    def wave(y, amp, wl, fill, dur, direction=1):
        d = f"M0,{y}"
        n = int(W / wl) + 3
        for i in range(n):
            x = i * wl
            d += f" q{wl/4},{-amp} {wl/2},0 t{wl/2},0"
        d += f" V{H} H0 Z"
        a, c = (0, -wl) if direction > 0 else (-wl, 0)
        return (
            f'<path d="{d}" fill="{fill}"><animateTransform attributeName="transform" type="translate" values="{a} 0;{c} 0" dur="{dur}s" repeatCount="indefinite"/></path>'
        )

    b = '<g clip-path="url(#round)">'
    b += f'<rect width="{W}" height="{H}" fill="#05080D"/>'
    r = rng(2)
    for i in range(40):
        b += f'<circle cx="{r.randint(10,W-10)}" cy="{r.randint(8,110)}" r="{f(r.uniform(.6,1.6))}" fill="#fff"><animate attributeName="opacity" values=".1;.9;.1" dur="{f(r.uniform(2,6))}s" begin="-{f(r.uniform(0,5))}s" repeatCount="indefinite"/></circle>'
    b += wave(140, 26, 300, "url(#w2)", 14, -1)
    b += wave(156, 20, 240, "url(#w1)", 10, 1)
    b += wave(176, 14, 200, "url(#w3)", 8, -1)
    b += (
        f'<text x="{W/2}" y="86" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="900" letter-spacing="5" fill="url(#tt)">THANKS FOR VISITING</text>'
        f'<text x="{W/2}" y="114" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#94A3B8" letter-spacing="3">Keep Learning  •  Keep Building  •  Keep Testing</text>'
        f'<text x="{W/2}" y="204" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#64748B" letter-spacing="2">Made with ♥ in Bangladesh by Muhtasim Masum Hasnayen</text>'
    )
    b += "</g>"
    return svg(W, H, b, defs, title="Footer")


if __name__ == "__main__":
    write("heading-about.svg", heading("about", "ABOUT ME", "WHO I AM  //  WHAT I DO", ORANGE))
    write("heading-stack.svg", heading("stack", "TECH ARSENAL", "LANGUAGES  //  FRAMEWORKS  //  TOOLS", "#38BDF8"))
    write("heading-projects.svg", heading("projects", "PROJECTS", "THINGS I HAVE BUILT, TESTED AND SHIPPED", "#A78BFA"))
    write("heading-contrib.svg", heading("contrib", "CONTRIBUTION JUNGLE", "A ROYAL BENGAL TIGER PATROLS MY COMMITS", ORANGE))
    write("heading-work.svg", heading("work", "ENGINEER AT WORK", "CODE  //  COFFEE  //  REPEAT", "#F59E0B"))
    write("heading-stats.svg", heading("stats", "GITHUB STATS", "NUMBERS THAT KEEP ME HONEST", GREEN))
    write("heading-connect.svg", heading("connect", "LET'S CONNECT", "FIND ME EVERYWHERE  //  TAP AN ICON", "#F43F5E"))
    write("divider.svg", divider())
    write("roles.svg", roles())
    write("about.svg", about())
    write("skills.svg", skills())
    write("footer.svg", footer())
