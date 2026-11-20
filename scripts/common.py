"""Shared helpers for building the profile SVG assets."""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

# Palette
ORANGE = "#FF7A18"
AMBER = "#FFB347"
GREEN = "#00A878"
BD_GREEN = "#006A4E"
BD_RED = "#F42A41"
INK = "#05080D"
PANEL = "#0B111B"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, defs="", title="", desc=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    d = f"<desc>{esc(desc)}</desc>" if desc else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">{t}{d}'
        f"<defs>{defs}</defs>{body}</svg>"
    )


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote {name}  {len(content)/1024:.1f} KB")
    return path


def f(x, n=2):
    """Compact float formatting."""
    s = f"{x:.{n}f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def sine_values(amp, steps=8, phase=0.0, fmt="0 {y}"):
    out = []
    for k in range(steps + 1):
        y = amp * math.sin(2 * math.pi * k / steps - phase)
        out.append(fmt.format(y=f(y)))
    return ";".join(out)


def rng(seed):
    return random.Random(seed)
