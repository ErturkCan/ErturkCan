"""Hand-drawn, self-drawing SVG doodles for the profile README (light and dark).

Same sketch method as erturks.com: polylines are resampled, pushed off-line with smooth noise,
drawn as Catmull-Rom curves and doubled with a faint second pass. Each stroke draws itself in
with a CSS animation, which GitHub keeps when it renders the SVG as an image.

Run: python3 scripts/build_doodles.py
"""
from math import sin, cos, pi, hypot, atan2
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
THEMES = {
    "light": dict(ink="#3F5233", accent="#23A84E", warn="#C8922A", marker="rgba(75,227,122,.24)", text="#18181B", muted="#57606A", sky="rgba(150,196,240,.4)", pink="rgba(232,92,92,.6)"),
    "dark": dict(ink="#CDEBD3", accent="#8CF2A6", warn="#F2D06B", marker="rgba(75,227,122,.18)", text="#E6EDF3", muted="#9DA7B3", sky="rgba(150,196,240,.3)", pink="rgba(232,92,92,.7)"),
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def rng(seed):
    state = [seed & 0xFFFFFFFF]

    def next_():
        state[0] = (state[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = state[0]
        t = ((t ^ (t >> 15)) * (1 | t)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF) ^ t) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return next_


def sketch(points, closed=False, seed=1, amp=0.7, step=5.0):
    r = rng(seed)
    p1, p2 = r() * 6.28, r() * 6.28
    src = points + [points[0]] if closed else points
    pts = []
    for (ax, ay), (bx, by) in zip(src, src[1:]):
        n = max(1, round(hypot(bx - ax, by - ay) / step))
        pts += [(ax + (bx - ax) * k / n, ay + (by - ay) * k / n) for k in range(n)]
    pts.append(src[-1])
    out = []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = hypot(dx, dy) or 1
        n = (sin(i * .55 + p1) * .6 + sin(i * 1.7 + p2) * .4) * amp
        out.append((x - dy / l * n, y + dx / l * n))
    if closed and len(out) > 2:
        out.append((out[1][0] + (out[2][0] - out[1][0]) * .4, out[1][1] + (out[2][1] - out[1][1]) * .4))
    d = f"M{out[0][0]:.2f} {out[0][1]:.2f}"
    for i in range(len(out) - 1):
        a, b, c, e = out[max(0, i - 1)], out[i], out[i + 1], out[min(len(out) - 1, i + 2)]
        d += (f" C{b[0] + (c[0] - a[0]) / 6:.2f} {b[1] + (c[1] - a[1]) / 6:.2f}"
              f" {c[0] - (e[0] - b[0]) / 6:.2f} {c[1] - (e[1] - b[1]) / 6:.2f} {c[0]:.2f} {c[1]:.2f}")
    return d


def ring(cx, cy, r, n=26):
    return [(cx + cos(-1.9 + i / n * 2 * pi) * r, cy + sin(-1.9 + i / n * 2 * pi) * r) for i in range(n)]


def ngon(n, cx, cy, r, rot=0):
    return [(cx + r * cos(rot + i * 2 * pi / n - pi / 2), cy + r * sin(rot + i * 2 * pi / n - pi / 2)) for i in range(n)]


class Doodle:
    """Collects strokes; `at` advances so strokes draw in the order they were added."""

    def __init__(self, w, h, label):
        self.w, self.h, self.label, self.parts, self.at, self.seed = w, h, label, [], 0.0, 7

    def ink(self, points, cls="", closed=False, amp=.7, step=5, dur=.55, delay=None):
        delay = self.at if delay is None else delay
        self.at = delay + dur * .55
        self.seed += 13
        for s, a, extra in ((self.seed, amp, ""), (self.seed + 31, amp * 1.6, " g")):
            d = sketch(points, closed, s, a, step)
            self.parts.append(f'<path class="i {cls}{extra}" pathLength="1" d="{d}" style="animation-delay:{delay:.2f}s;animation-duration:{dur:.2f}s"/>')
        return self

    def marker(self, points, kind="m"):
        self.seed += 7
        self.parts.append(f'<path class="{kind}" d="{sketch(points, True, self.seed, 2.2, 7)}" style="animation-delay:{self.at:.2f}s"/>')

    def raw(self, svg):
        self.parts.append(svg)

    def render(self, theme, defs=""):
        t = THEMES[theme]
        css = (f".i{{fill:none;stroke:{t['ink']};stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;"
               "stroke-dasharray:1;stroke-dashoffset:1;animation:draw .6s cubic-bezier(.65,0,.35,1) both}"
               ".g{stroke-width:.9;opacity:.32}"
               f".a{{stroke:{t['accent']}}}.w{{stroke:{t['warn']}}}.f{{opacity:.45}}"
               f".m,.sky,.pk{{fill:{t['marker']};opacity:0;animation:fade .8s ease both}}.sky{{fill:{t['sky']}}}.pk{{fill:{t['pink']}}}"
               f".dot{{fill:{t['ink']};opacity:0;animation:fade .4s ease both}}"
               f".t{{fill:{t['text']};font-family:{FONT}}}.mu{{fill:{t['muted']};font-family:{FONT}}}"
               f".ac{{fill:{t['accent']}}}"
               "@keyframes draw{to{stroke-dashoffset:0}}@keyframes fade{to{opacity:1}}"
               "@media (prefers-reduced-motion:reduce){.i,.m,.sky,.pk,.dot{animation:none;stroke-dashoffset:0;opacity:1}.g{opacity:.32}}")
        body = "".join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'role="img" aria-label="{self.label}"><style>{css}{defs}</style>{body}</svg>')


def write(name, doodle, defs=""):
    for theme in THEMES:
        (OUT / f"doodle-{name}-{theme}.svg").write_text(doodle.render(theme, defs))


def dot(d, x, y, r=2.2, delay=None):
    d.raw(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{r}" style="animation-delay:{(d.at if delay is None else delay):.2f}s"/>')


# ---------------------------------------------------------------- hero
def hero():
    d = Doodle(560, 132, "Can Erturk. Software for problems that live outside the screen.")
    d.raw('<defs><radialGradient id="chrome" cx=".32" cy=".28" r=".8"><stop offset="0" stop-color="#F3FFEE"/>'
          '<stop offset=".28" stop-color="#8CF2A6"/><stop offset=".6" stop-color="#23A84E"/><stop offset="1" stop-color="#0B3D1A"/></radialGradient></defs>')
    # The chrome full stop follows the text, whatever font the viewer has.
    d.raw('<text class="t" x="0" y="58" font-size="54" font-weight="600" letter-spacing="-2">Can Erturk<tspan class="ac" dx="3" font-size="20">●</tspan></text>')
    d.raw('<text class="mu" x="2" y="104" font-size="22" letter-spacing="-.3">Software for problems that live outside the screen.</text>')
    d.at = .3
    d.ink([(4, 120), (180, 116), (360, 118), (538, 113)], "a", amp=.8, step=8, dur=1.1)
    return d


# ---------------------------------------------------------------- Fiat Stellantis line
def vision():
    w, belt, cam, slot = 760, 70, 380, 64
    d = Doodle(w, 96, "Sketch of parts on an assembly line passing a camera that marks faults")
    d.ink([(20, belt), (740, belt)], amp=.5, step=7, dur=.9)
    d.ink([(20, belt + 13), (740, belt + 13)], amp=.5, step=7, dur=.9)
    d.ink(ring(20, belt + 6.5, 6.5, 12), closed=True, amp=.25)
    d.ink(ring(740, belt + 6.5, 6.5, 12), closed=True, amp=.25)
    d.ink([(cam - 14, 4), (cam + 14, 4), (cam + 14, 17), (cam - 14, 17), (cam - 14, 4)], amp=.3, step=3)
    d.ink(ring(cam, 21, 4, 10), closed=True, amp=.15)
    for x2 in (cam - 24, cam + 24):
        for i in range(4):
            t0, t1 = i / 4, i / 4 + .12
            d.ink([(cam + (x2 - cam) * t0, 26 + 22 * t0), (cam + (x2 - cam) * t1, 26 + 22 * t1)], "f", amp=.05, dur=.15)
    states = [True, True, False, True]
    parts, marks = [], []
    start = d.at
    for i in range(16):
        x, ok = -60 + i * slot, states[i % 4]
        sub = Doodle(0, 0, "")
        sub.seed = 90 + i % 4
        sub.at = start
        sub.ink([(x - 14, belt - 18), (x + 14, belt - 18), (x + 14, belt - 1), (x - 14, belt - 1), (x - 14, belt - 18)], amp=.35, step=3)
        sub.ink(ring(x - 5, belt - 9.5, 3, 8), closed=True, amp=.15, dur=.3)
        if ok:
            sub.ink(ring(x + 5, belt - 9.5, 3, 8), closed=True, amp=.15, dur=.3)
        else:
            sub.ink([(x + 3, belt - 18), (x + 6, belt - 12), (x + 2, belt - 7), (x + 5, belt - 1)], amp=.2, step=2, dur=.3)
        parts += sub.parts
        m = Doodle(0, 0, "")
        m.seed, m.at = 120 + i % 4, start + .4
        if ok:
            m.ink([(x + 8, belt - 32), (x + 12, belt - 28), (x + 20, belt - 37)], "a", amp=.2, step=2, dur=.35)
        else:
            m.ink([(x + 9, belt - 37), (x + 18, belt - 28)], "w", amp=.15, step=2, dur=.3)
            m.ink([(x + 18, belt - 37), (x + 9, belt - 28)], "w", amp=.15, step=2, dur=.3)
        marks += m.parts
    d.raw('<defs><clipPath id="belt"><rect x="12" y="0" width="736" height="96"/></clipPath>'
          f'<clipPath id="seen"><rect x="{cam + 6}" y="0" width="{w}" height="96"/></clipPath></defs>')
    d.raw(f'<g clip-path="url(#belt)"><g class="run">{"".join(parts)}</g></g>')
    d.raw(f'<g clip-path="url(#seen)"><g clip-path="url(#belt)"><g class="run">{"".join(marks)}</g></g></g>')
    return d, f".run{{animation:run 7s linear 2.4s infinite}}@keyframes run{{to{{transform:translateX({4 * slot}px)}}}}@media (prefers-reduced-motion:reduce){{.run{{animation:none}}}}"


# ---------------------------------------------------------------- Parmestore flow
def parmestore():
    d = Doodle(760, 128, "Sketch of the Parmestore flow: source, price, ship")
    # Source: boxes and a magnifier with a check.
    d.marker([(48, 82), (104, 80), (106, 116), (46, 116)])
    d.ink([(30, 116), (196, 116)], amp=.5)
    d.ink([(50, 116), (50, 82), (102, 82), (102, 116)], amp=.45, step=4)
    d.ink([(50, 94), (102, 94)], amp=.3)
    d.ink([(108, 116), (108, 90), (148, 90), (148, 116)], amp=.45, step=4)
    d.ink([(62, 82), (62, 54), (94, 54), (94, 82)], amp=.45, step=4)
    d.ink([(70, 70), (76, 75), (86, 65)], "a", amp=.2, step=2, dur=.4)
    d.ink(ring(168, 56, 13), closed=True, amp=.4)
    d.ink([(177, 66), (190, 80)], amp=.25)
    # Arrow.
    d.ink([(214, 76), (232, 70), (250, 75), (268, 71)], amp=.4, step=4)
    d.ink([(261, 66), (268, 71), (262, 78)], amp=.2, step=2, dur=.3)
    # Price: a tag and a rising, repriced line.
    d.marker([(292, 58), (340, 58), (352, 74), (340, 90), (292, 90)])
    d.ink([(292, 58), (340, 58), (352, 74), (340, 90), (292, 90), (292, 58)], amp=.45, step=4)
    d.ink(ring(300, 74, 3.5, 10), closed=True, amp=.15, dur=.3)
    d.ink([(312, 68), (336, 68)], amp=.2, dur=.3)
    d.ink([(312, 76), (330, 76)], amp=.2, dur=.3)
    d.ink([(370, 30), (370, 116), (448, 116)], amp=.4)
    d.ink([(374, 98), (388, 86), (400, 92), (414, 68), (428, 74), (440, 46)], "a", amp=.35, step=4, dur=.8)
    d.ink([(432, 46), (440, 46), (440, 54)], "a", amp=.15, step=2, dur=.3)
    # Arrow.
    d.ink([(470, 76), (488, 70), (506, 75), (524, 71)], amp=.4, step=4)
    d.ink([(517, 66), (524, 71), (518, 78)], amp=.2, step=2, dur=.3)
    # Ship: parcel, dotted route, globe.
    d.marker(ring(690, 70, 30, 16))
    d.ink(ring(690, 70, 34), closed=True, amp=.55, dur=.8)
    d.ink([(656, 70), (724, 70)], amp=.35)
    d.ink([(690, 36), (678, 54), (676, 70), (678, 86), (690, 104)], amp=.3)
    d.ink([(690, 36), (702, 54), (704, 70), (702, 86), (690, 104)], amp=.3)
    route = [(560 + (k / 20) * 120, 98 - sin(k / 20 * pi) * 66 - k * 1.2) for k in range(21)]
    for k in range(0, 20, 2):
        d.ink([route[k], route[k + 1]], "f", amp=.05, dur=.12)
    d.ink([(546, 92), (574, 92), (574, 114), (546, 114), (546, 92)], amp=.35, step=3)
    d.ink([(560, 92), (560, 114)], amp=.2, dur=.2)
    d.ink(ring(680, 52, 4, 10), "a", closed=True, amp=.15, dur=.3)
    labels = [(110, "Source"), (370, "Price"), (690, "Ship")]
    for x, text in labels:
        d.raw(f'<text class="mu" x="{x}" y="14" font-size="12" text-anchor="middle" letter-spacing=".8">{text.upper()}</text>')
    return d


# ---------------------------------------------------------------- Where it started
def started():
    d = Doodle(760, 120, "Sketches of a 3D printer, two intersecting polygons, a rocket, clustered points and the NFT character")
    # 3D printer printing a vase.
    d.ink([(14, 112), (14, 22), (118, 22), (118, 112)], amp=.45, step=4, dur=.7)
    d.ink([(6, 110), (126, 110)], amp=.5)
    d.ink([(14, 40), (118, 40)], amp=.5)
    widths = [14 + 22 * sin(pi * (i + .7) / 11.6) for i in range(11)]
    d.marker([(66 - widths[5] - 4, 64), (66 + widths[5] + 4, 62), (66 + widths[0] + 6, 108), (66 - widths[0] - 6, 108)])
    for i, wd in enumerate(widths):
        d.ink([(66 - wd, 104 - i * 4), (66 + wd, 104 - i * 4)], amp=.45, step=4, dur=.25)
    d.ink([(60, 32), (72, 32), (69, 40), (63, 40), (60, 32)], amp=.4, step=3, dur=.3)
    # Polygons with a hatched overlap.
    pa, pb = ngon(5, 196, 70, 32, .2), ngon(6, 224, 64, 29, -.1)
    d.raw('<defs><clipPath id="ov"><polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pb) + '"/></clipPath></defs>')
    d.ink(pa, closed=True, amp=.6, dur=.7)
    d.ink(pb, closed=True, amp=.6, dur=.7)
    hatch = Doodle(0, 0, "")
    hatch.at = d.at
    for x in range(150, 270, 6):
        hatch.ink([(x, 110), (x + 50, 20)], "a", amp=.3, step=6, dur=.2)
    d.raw('<g clip-path="url(#ov)"><g clip-path="url(#pa)">' + "".join(hatch.parts) + "</g></g>")
    d.raw('<defs><clipPath id="pa"><polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pa) + '"/></clipPath></defs>')
    d.at = hatch.at
    # Rocket on its arc.
    d.ink([(296, 112), (444, 112)], amp=.45)
    arc = [(318 + 120 * k / 24, 98 - sin(k / 24 * pi * .82) * 82) for k in range(25)]
    for k in range(0, 24, 2):
        d.ink([arc[k], arc[k + 1]], "f", amp=.05, dur=.1)
    tip = arc[16]
    ang = atan2(arc[17][1] - arc[15][1], arc[17][0] - arc[15][0]) + pi / 2
    def rot(px, py):
        return (tip[0] + px * cos(ang) - py * sin(ang), tip[1] + px * sin(ang) + py * cos(ang))
    d.ink([rot(0, -14), rot(4, -7), rot(4, 7), rot(-4, 7), rot(-4, -7), rot(0, -14)], amp=.3, step=2, dur=.4)
    d.ink([rot(-4, 2), rot(-8, 9), rot(-4, 7)], amp=.2, step=2, dur=.2)
    d.ink([rot(4, 2), rot(8, 9), rot(4, 7)], amp=.2, step=2, dur=.2)
    d.ink([rot(-2.5, 8), rot(0, 16), rot(2.5, 8)], "w", amp=.2, step=2, dur=.25)
    # k-means: three lassoed clusters.
    r = rng(5)
    for k, (cx, cy) in enumerate([(486, 78), (532, 54), (576, 86)]):
        for _ in range(7):
            a, m = r() * 6.28, 3 + r() * 8
            dot(d, cx + cos(a) * m, cy + sin(a) * m * .8, 2.1 if k == 1 else 1.8)
        d.ink(ring(cx, cy, 15 + k % 2 * 2), "a" if k == 1 else "", closed=True, amp=1.1, dur=.5)
    # NFT character.
    d.raw(f'<path class="sky" d="{sketch(ring(684, 66, 40, 16), True, 81, 2.2, 7)}" style="animation-delay:{d.at:.2f}s"/>')
    d.ink(ring(684, 66, 42), closed=True, amp=.55, dur=.6)
    body = [(662, 104), (661, 78), (664, 60), (658, 46), (666, 50), (665, 37), (672, 46), (678, 42), (684, 42), (690, 42), (696, 46), (703, 37), (702, 50), (710, 46), (704, 60), (707, 78), (706, 104)]
    d.raw(f'<path class="m" d="{sketch(body[:1] + body[3:-3] + body[-1:], True, 83, 1.5, 6)}" style="animation-delay:{d.at:.2f}s"/>')
    d.ink(body, amp=.35, step=3, dur=.9)
    for x in (677, 691):
        dot(d, x, 64, 3.6)
    d.raw(f'<path class="pk" d="{sketch([(678, 72), (690, 72), (684, 79)], True, 85, .4, 2)}" style="animation-delay:{d.at:.2f}s"/>')
    d.ink([(678, 72), (690, 72), (684, 79), (678, 72)], amp=.15, step=2, dur=.25)
    for y in (86, 91):
        d.ink([(667, y), (671, y + 3)], amp=.1, dur=.15)
        d.ink([(701, y), (697, y + 3)], amp=.1, dur=.15)
    return d


# ---------------------------------------------------------------- contact
def plane():
    d = Doodle(760, 70, "Sketch of a paper plane on a looping trail")
    trail = [(30 + k * 6.0, 38 - 16 * sin(k / 109 * 2 * pi) - 6 * sin(k / 109 * 5 * pi)) for k in range(110)]
    for k in range(0, 106, 3):
        d.ink([trail[k], trail[k + 1]], "f", amp=.05, dur=.06)
    x, y = trail[-1]
    k = 1.7
    pl = [(-14, -9), (14, -1), (-14, 7), (-8, -1), (-14, -9)]
    d.ink([(x + px * k, y + py * k) for px, py in pl], "a", amp=.3, step=2, dur=.5)
    d.ink([(x - 8 * k, y - k), (x + 14 * k, y - k)], "a", amp=.1, dur=.2)
    return d


if __name__ == "__main__":
    write("hero", hero())
    v, css = vision()
    write("vision", v, css)
    write("parmestore", parmestore())
    write("started", started())
    write("plane", plane())
    print("written:", sorted(p.name for p in OUT.glob("doodle-*.svg")))
