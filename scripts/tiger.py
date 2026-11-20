"""Royal Bengal Tiger contribution graph (black + orange jungle theme)."""
import datetime as dt
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

W, H = 1200, 410
CELL, GAP = 17, 3
PITCH = CELL + GAP
GX, GY = 92, 92          # grid origin
GROUND = 338             # tiger feet y
CYCLE = 20               # seconds for one crossing

LEVEL_FILL = ["#17120E", "#6B3410", "#B4560F", "#F27A14", "#FFB13B"]
LEVEL_STROKE = ["#2A2018", "#7B3E14", "#C2631A", "#FF8F2E", "#FFCB6B"]


# --------------------------------------------------------------------------- tiger
def leg(hx, hy, color, stripe, begin, flip=1):
    return (
        f'<g transform="translate({hx},{hy})"><g>'
        f'<animateTransform attributeName="transform" type="rotate" values="-27;27;-27" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="1.05s" begin="{begin}s" repeatCount="indefinite"/>'
        f'<rect x="-8" y="-4" width="16" height="31" rx="8" fill="{color}"/>'
        f'<path d="M-8,6 h7 M-8,14 h6" stroke="{stripe}" stroke-width="2.6" stroke-linecap="round"/>'
        f'<g transform="translate(0,24)"><g>'
        f'<animateTransform attributeName="transform" type="rotate" values="2;-48;2" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="1.05s" begin="{f(begin-0.26)}s" repeatCount="indefinite"/>'
        f'<rect x="-6" y="-2" width="12" height="28" rx="6" fill="{color}"/>'
        f'<path d="M-6,8 h6" stroke="{stripe}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<ellipse cx="3" cy="27" rx="10" ry="5.4" fill="{color}"/>'
        f'<path d="M0,24 v6 M5,24 v6" stroke="#1B0C03" stroke-width="1.2" opacity=".55"/>'
        f'</g></g></g></g>'
    )


def tiger():
    stripes = ""
    for i, x in enumerate((30, 40, 50, 60, 70, 80, 90, 100)):
        top = -88 + ((x - 62) / 46) ** 2 * 22
        ln = 24 + (i % 3) * 5
        sk = -4 + (i % 2) * 7
        stripes += f'<path d="M{x},{f(top+1,1)} q{sk-4},{f(ln*0.55,1)} {sk+1},{ln} q{5},{-ln*0.6:.1f} {-sk+3},{-ln} z" fill="#1A0B03"/>'
    s = '<g>'
    s += '<ellipse cx="74" cy="3" rx="66" ry="5.5" fill="#000" opacity=".55"/>'
    # far legs (darker)
    s += leg(50, -46, "#C2570C", "#1A0B03", -0.52) + leg(92, -46, "#C2570C", "#1A0B03", 0)
    # body group (bobs)
    s += (
        '<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -2.6;0 0" dur=".525s" repeatCount="indefinite"/>'
        # tail
        '<g><animateTransform attributeName="transform" type="rotate" values="6 24 -60;-10 24 -60;6 24 -60" dur="1.6s" repeatCount="indefinite"/>'
        '<path d="M24,-60 C4,-60 -8,-76 0,-98" fill="none" stroke="#F97316" stroke-width="8" stroke-linecap="round"/>'
        '<path d="M24,-60 C4,-60 -8,-76 0,-98" fill="none" stroke="#1A0B03" stroke-width="8.2" stroke-dasharray="4 9" stroke-linecap="butt"/>'
        '<circle cx="0" cy="-98" r="4.3" fill="#1A0B03"/></g>'
        # torso
        '<path d="M20,-60 C24,-86 60,-94 92,-86 C114,-80 122,-66 114,-50 C108,-38 96,-34 84,-34 L42,-34 C24,-36 14,-48 20,-60 Z" fill="url(#tBody)"/>'
        '<path d="M30,-38 C52,-28 90,-28 110,-44 C104,-34 96,-30 84,-30 L42,-30 C34,-31 31,-34 30,-38 Z" fill="#FFE2BC" opacity=".9"/>'
        f'<g opacity=".95">{stripes}</g>'
        # neck + head
        '<path d="M100,-84 C116,-90 124,-80 122,-62 C120,-48 112,-42 102,-44 Z" fill="#F97316"/>'
        '<g><animateTransform attributeName="transform" type="rotate" values="-2 116 -64;3 116 -64;-2 116 -64" dur="1.05s" repeatCount="indefinite"/>'
        '<circle cx="124" cy="-88" r="6.4" fill="#EA580C"/><circle cx="124" cy="-88" r="3.2" fill="#1A0B03"/>'
        '<circle cx="141" cy="-88" r="6.4" fill="#EA580C"/><circle cx="141" cy="-88" r="3.2" fill="#1A0B03"/>'
        '<ellipse cx="132" cy="-72" rx="21" ry="18" fill="url(#tHead)"/>'
        '<path d="M118,-60 C124,-48 140,-46 150,-56 C150,-48 144,-42 134,-42 C124,-42 118,-50 118,-60 Z" fill="#FFE9CC"/>'
        '<ellipse cx="146" cy="-64" rx="10.5" ry="8" fill="#FFEBD0"/>'
        '<path d="M149,-71 l8,1 l-4,6 z" fill="#3A1A12"/><path d="M153,-65 v4 q-3,3 -7,2 M153,-61 q3,3 7,2" fill="none" stroke="#3A1A12" stroke-width="1.4" stroke-linecap="round"/>'
        '<path d="M127,-82 l6,5 M133,-86 l3,7 M139,-85 l-1,7" stroke="#1A0B03" stroke-width="2.6" stroke-linecap="round"/>'
        '<path d="M113,-72 l9,3 M113,-65 l10,3 M114,-58 l9,2" stroke="#1A0B03" stroke-width="2.4" stroke-linecap="round"/>'
        '<ellipse cx="140" cy="-75" rx="5" ry="3.4" fill="#FFE066"/><ellipse cx="141" cy="-75" rx="1.4" ry="3" fill="#1A0B03"/>'
        '<circle cx="140" cy="-75" r="9" fill="#FFE066" opacity=".35" filter="url(#tglow)"><animate attributeName="opacity" values=".15;.5;.15" dur="2s" repeatCount="indefinite"/></circle>'
        '<path d="M152,-62 l16,-4 M152,-59 l17,0 M151,-57 l15,5" stroke="#fff" stroke-opacity=".6" stroke-width=".9"/>'
        '</g></g>'
    )
    # near legs
    s += leg(40, -46, "#F97316", "#1A0B03", 0) + leg(98, -46, "#F97316", "#1A0B03", -0.52)
    s += '</g>'
    return s


# --------------------------------------------------------------------------- data
def demo_weeks(n=53, seed=4):
    r = rng(seed)
    today = dt.date(2026, 11, 20)
    start = today - dt.timedelta(days=today.weekday() + 1 + (n - 1) * 7)  # sunday
    weeks = []
    for w in range(n):
        days = []
        for d in range(7):
            date = start + dt.timedelta(days=w * 7 + d)
            if date > today:
                continue
            base = r.random()
            burst = 1.0 + 0.9 * math.sin(w / 4.5)
            wk = 0.45 if d in (0, 6) else 1.0
            val = base * burst * wk
            cnt = 0 if val < 0.42 else int(val * 4.6)
            lvl = 0 if cnt == 0 else 1 if cnt < 3 else 2 if cnt < 5 else 3 if cnt < 8 else 4
            days.append(dict(date=date.isoformat(), count=cnt, level=lvl, weekday=d))
        weeks.append(days)
    return weeks


def streaks(weeks):
    flat = [d for wk in weeks for d in wk]
    best = cur = run = 0
    for d in flat:
        if d["count"] > 0:
            run += 1
            best = max(best, run)
        else:
            run = 0
    # current streak counts back from the latest day (allow today to be empty)
    i = len(flat) - 1
    if i >= 0 and flat[i]["count"] == 0:
        i -= 1
    while i >= 0 and flat[i]["count"] > 0:
        cur += 1
        i -= 1
    return best, cur


# --------------------------------------------------------------------------- scene
def build(weeks, demo=True, login="Muhtasim-Masum-Hasnayen"):
    nweeks = len(weeks)
    gw = nweeks * PITCH
    total = sum(d["count"] for wk in weeks for d in wk)
    best_streak, cur_streak = streaks(weeks)
    best_day = max((d["count"] for wk in weeks for d in wk), default=0)

    tw_start, tw_end = -165, W + 25
    span = tw_end - tw_start

    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04060A"/><stop offset=".62" stop-color="#0A0A0C"/><stop offset="1" stop-color="#1B0E04"/></linearGradient>
<radialGradient id="horizon" cx=".5" cy="1" r=".8"><stop offset="0" stop-color="#FF7A18" stop-opacity=".32"/><stop offset="1" stop-color="#FF7A18" stop-opacity="0"/></radialGradient>
<linearGradient id="tBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9A3C"/><stop offset="1" stop-color="#E8590C"/></linearGradient>
<linearGradient id="tHead" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFA047"/><stop offset="1" stop-color="#F0640F"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF7A18" stop-opacity="0"/><stop offset="1" stop-color="#FFB347" stop-opacity=".42"/></linearGradient>
<linearGradient id="fog" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#FFB98A" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="tt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="tglow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>
<clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>
"""
    b = '<g clip-path="url(#round)">'
    b += f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#horizon)"/>'
    r = rng(8)
    for i in range(46):
        b += f'<circle cx="{r.randint(8,W-8)}" cy="{r.randint(6,230)}" r="{f(r.uniform(.5,1.3))}" fill="#fff"><animate attributeName="opacity" values=".08;.7;.08" dur="{f(r.uniform(2,6))}s" begin="-{f(r.uniform(0,5))}s" repeatCount="indefinite"/></circle>'
    # hills
    b += f'<path d="M0,300 C120,260 220,280 340,262 C470,244 560,282 700,268 C840,254 940,284 1060,262 C1130,252 1170,262 1200,270 V{H} H0 Z" fill="#0B0A09"/>'
    b += f'<path d="M0,326 C160,300 300,318 460,304 C640,290 760,320 940,306 C1060,298 1140,310 1200,314 V{H} H0 Z" fill="#100B07"/>'
    # bamboo
    def bamboo(x, h, sway):
        s = f'<g><animateTransform attributeName="transform" type="rotate" values="-{sway} {x} {GROUND};{sway} {x} {GROUND};-{sway} {x} {GROUND}" dur="{f(5+h/60)}s" repeatCount="indefinite"/>'
        s += f'<rect x="{x-4}" y="{GROUND-h}" width="8" height="{h}" rx="3" fill="#0E1A12"/>'
        for k in range(1, int(h / 44)):
            yy = GROUND - k * 44
            s += f'<rect x="{x-5}" y="{yy}" width="10" height="3" rx="1.5" fill="#1C3326"/>'
            s += f'<path d="M{x+4},{yy} q16,-6 26,-16 q-14,0 -26,10 z" fill="#12261B"/>'
        return s + "</g>"
    for x, h, sw in ((28, 250, 1.2), (52, 200, 1.8), (1172, 260, 1.2), (1148, 210, 1.8), (1124, 160, 2.2)):
        b += bamboo(x, h, sw)
    # fog drift
    for i, (yy, hh, dur) in enumerate(((250, 46, 26), (300, 40, 34))):
        b += f'<rect x="-400" y="{yy}" width="800" height="{hh}" fill="url(#fog)"><animateTransform attributeName="transform" type="translate" values="0 0;1500 0" dur="{dur}s" begin="-{i*9}s" repeatCount="indefinite"/></rect>'

    # --- grid frame
    b += f'<rect x="{GX-48}" y="{GY-34}" width="{gw+60}" height="{7*PITCH+50}" rx="14" fill="#07090D" fill-opacity=".72" stroke="#fff" stroke-opacity=".07"/>'
    # month labels
    last_m = None
    for wi, wk in enumerate(weeks):
        if not wk:
            continue
        m = dt.date.fromisoformat(wk[0]["date"]).month
        if m != last_m and wi < nweeks - 2:
            b += f'<text x="{GX+wi*PITCH}" y="{GY-12}" font-family="{MONO}" font-size="10" fill="#8B7B6B">{dt.date(2000,m,1).strftime("%b").upper()}</text>'
        last_m = m
    for d, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b += f'<text x="{GX-20}" y="{GY+d*PITCH+CELL-3}" text-anchor="end" font-family="{MONO}" font-size="9" fill="#6B5D50">{lab}</text>'

    # --- cells with tiger-triggered light-up
    cells, hot = "", ""
    for wi, wk in enumerate(weeks):
        for d in wk:
            lvl = d["level"]
            x = GX + wi * PITCH
            y = GY + d["weekday"] * PITCH
            xc = x + CELL / 2
            fill, stroke = LEVEL_FILL[lvl], LEVEL_STROKE[lvl]
            tc = (xc - 130 - tw_start) / span
            tc = min(max(tc, 0.0), 0.96)
            if lvl == 0:
                el = f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            else:
                kt = f"0;{f(tc,4)};{f(tc+0.006,4)};{f(tc+0.04,4)};0.965;1"
                vals = f"#17120E;#17120E;#FFF1D6;{fill};{fill};#17120E"
                el = (
                    f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1">'
                    f'<animate attributeName="fill" values="{vals}" keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/></rect>'
                )
            if lvl == 4:
                hot += el
            else:
                cells += el
    b += f"<g>{cells}</g><g filter=\"url(#glow)\">{hot}</g>"

    # --- header stats
    if demo:
        b += (
            f'<text x="{GX-34}" y="40" font-family="{SANS}" font-size="22" font-weight="900" fill="url(#tt)" letter-spacing="2">CONTRIBUTION JUNGLE</text>'
            f'<text x="{GX-34}" y="58" font-family="{MONO}" font-size="11" fill="#8B7B6B" letter-spacing="1.5">SAMPLE DATA  ·  run the “Update profile assets” workflow to sync your real commits</text>'
        )
    else:
        b += (
            f'<text x="{GX-34}" y="40" font-family="{SANS}" font-size="22" font-weight="900" fill="url(#tt)" letter-spacing="2">CONTRIBUTION JUNGLE</text>'
            f'<text x="{GX-34}" y="58" font-family="{MONO}" font-size="11" fill="#8B7B6B" letter-spacing="1.5">@{esc(login)}  ·  last 12 months  ·  synced {dt.date.today().isoformat()}</text>'
        )
        stats = [(f"{total:,}", "CONTRIBUTIONS"), (f"{best_streak}d", "LONGEST STREAK"), (f"{cur_streak}d", "CURRENT STREAK"), (f"{best_day}", "BEST DAY")]
        sx = GX + gw - 8
        for val, lab in reversed(stats):
            b += (
                f'<text x="{sx}" y="42" text-anchor="end" font-family="{SANS}" font-size="22" font-weight="900" fill="{AMBER}">{val}</text>'
                f'<text x="{sx}" y="58" text-anchor="end" font-family="{MONO}" font-size="9" fill="#8B7B6B" letter-spacing="1.5">{lab}</text>'
            )
            sx -= max(len(lab) * 7.2, 80) + 28

    # --- ground
    b += f'<rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="#0B0705"/><rect x="0" y="{GROUND}" width="{W}" height="2" fill="{ORANGE}" opacity=".35"/>'

    # --- light beam following the tiger's head
    b += (
        f'<g><animateTransform attributeName="transform" type="translate" values="{tw_start} 0;{tw_end} 0" dur="{CYCLE}s" repeatCount="indefinite"/>'
        f'<rect x="96" y="{GY-12}" width="80" height="{GROUND-GY+12}" fill="url(#beam)"/></g>'
    )
    # --- paw prints
    nprints = int(W / 70) + 2
    for i in range(nprints):
        px = 40 + i * 70
        tp = (px - 40 - tw_start) / span
        tp = min(max(tp, 0.0), 0.97)
        kt = f"0;{f(tp,4)};{f(tp+0.004,4)};{f(min(tp+0.07,.985),4)};1"
        ph = GROUND + 10 + (i % 2) * 8
        b += (
            f'<g opacity="0"><animate attributeName="opacity" values="0;0;.75;0;0" keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/>'
            f'<ellipse cx="{px}" cy="{ph}" rx="5.2" ry="4" fill="{ORANGE}"/>'
            + "".join(f'<circle cx="{px+dx}" cy="{ph-6.5}" r="1.9" fill="{ORANGE}"/>' for dx in (-5, -1.7, 1.7, 5))
            + "</g>"
        )
    # --- the tiger
    b += (
        f'<g transform="translate(0,{GROUND})"><g>'
        f'<animateTransform attributeName="transform" type="translate" values="{tw_start} 0;{tw_end} 0" dur="{CYCLE}s" repeatCount="indefinite"/>'
        f'<g transform="scale(1.02)">{tiger()}</g></g></g>'
    )
    # --- grass (front)
    for i in range(0, W, 14):
        hh = r.randint(14, 30)
        sway = r.uniform(3, 7)
        b += (
            f'<path d="M{i},{GROUND+4} q{r.randint(-3,3)},-{hh/2} {r.randint(-6,6)},-{hh}" stroke="#241A0F" stroke-width="2.4" fill="none" stroke-linecap="round">'
            f'<animateTransform attributeName="transform" type="rotate" values="-{f(sway)} {i} {GROUND+4};{f(sway)} {i} {GROUND+4};-{f(sway)} {i} {GROUND+4}" dur="{f(r.uniform(2.5,5))}s" begin="-{f(r.uniform(0,4))}s" repeatCount="indefinite"/></path>'
        )
    # --- fireflies
    for i in range(14):
        fx, fy = r.randint(80, W - 80), r.randint(250, 330)
        d = r.uniform(5, 10)
        b += (
            f'<circle cx="{fx}" cy="{fy}" r="1.8" fill="#FFD27A" filter="url(#glow)">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{r.randint(-40,40)} {r.randint(-30,10)};{r.randint(-40,40)} {r.randint(-20,20)};0 0" dur="{f(d)}s" begin="-{f(r.uniform(0,d))}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;.2;1;0" dur="{f(r.uniform(2.5,5))}s" begin="-{f(r.uniform(0,3))}s" repeatCount="indefinite"/></circle>'
        )
    # --- legend
    lx = GX + gw - 5 * 22 - 40
    ly = H - 24
    b += f'<text x="{lx}" y="{ly+10}" text-anchor="end" font-family="{MONO}" font-size="10" fill="#8B7B6B">LESS</text>'
    for i in range(5):
        b += f'<rect x="{lx+10+i*22}" y="{ly}" width="14" height="14" rx="3.5" fill="{LEVEL_FILL[i]}" stroke="{LEVEL_STROKE[i]}"/>'
    b += f'<text x="{lx+10+5*22+4}" y="{ly+10}" font-family="{MONO}" font-size="10" fill="#8B7B6B">MORE</text>'
    b += f'<text x="{GX-34}" y="{ly+10}" font-family="{MONO}" font-size="10" fill="#6B5D50">◆ the Royal Bengal Tiger lights up every commit it passes</text>'
    # frame
    b += f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="#fff" stroke-opacity=".08"/>'
    b += (
        f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20" fill="none" stroke="{ORANGE}" stroke-width="2" pathLength="1" stroke-dasharray=".14 .86" opacity=".85">'
        f'<animate attributeName="stroke-dashoffset" values="0;-1" dur="12s" repeatCount="indefinite"/></rect>'
    )
    b += "</g>"
    return svg(W, H, b, defs, title="Contribution graph with a Royal Bengal Tiger", desc="Contribution calendar lighting up as an animated Bengal tiger walks past.")


if __name__ == "__main__":
    write("tiger-contribution.svg", build(demo_weeks(), demo=True))
