#!/usr/bin/env python3
"""Two figures with the arts at the centre, as stacked SVG layers for click builds.

    python3 tools/make_arts_figures.py

images/fig-arts-subjects-0..8.svg: the arts in the middle, one school subject per layer on a ring
around it, joined by a plain line (the arts connect the subjects); music is one of them.
images/fig-arts-impacts-0..8.svg: the arts on the left and a fan of arrows out to a column of the areas they influence, from the
body outwards, one per layer. No numbers.
Both are adapted from the music figures in the deck for the Musikk i skolen conference, 30 October
2026, with the arts in place of music. All layers of a figure share one canvas, so they stack in a
.layers div.
"""
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# From the body outwards: body, feelings and thinking, expression, community and culture.
SUBJECTS = [["Mathematics"], ["Science"], ["Programming"], ["Norwegian"], ["Languages"],
            ["Social", "studies"], ["Music"], ["Physical", "education"]]
EFFECTS = ["Motor", "Health", "Emotional", "Cognitive", "Linguistic", "Aesthetic", "Social", "Cultural"]
COLOURS = ["#9a90cf", "#a5cbed", "#efadb2", "#b3e297"]
W, H = 1920, 1000
INK = "#231f20"
FONT = "font-family:'Roboto Condensed','Arial Narrow',Arial,sans-serif;font-weight:700"
ARROW = (f'<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
         f'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker>')


def svg(body, defs="", box=(0, 0, W, H)):
    x, y, w, h = box
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.0f} {y:.0f} {w} {h}" width="{w}" height="{h}">'
            f'<defs>{defs}</defs>{body}</svg>')


def word(x, y, s, size):
    lines = s if isinstance(s, list) else [s]
    return "".join(f'<text x="{x:.0f}" y="{y + size * 0.35 + (i - (len(lines) - 1) / 2) * size * 1.05:.0f}" '
                   f'text-anchor="middle" font-size="{size}" fill="{INK}" style="{FONT}">{w}</text>'
                   for i, w in enumerate(lines))


def write(n, text, name="impacts"):
    with open(os.path.join(HERE, "images", f"fig-arts-{name}-{n}.svg"), "w", encoding="utf-8") as f:
        f.write(text)


def ring():
    cx, cy, rad, r_item, r_mid = W / 2, H / 2, 370, 122, 170
    box = (cx - 500, cy - 500, 1000, 1000)    # cropped to the ring, so it can be shown large
    write(0, svg(f'<circle cx="{cx}" cy="{cy}" r="{r_mid}" fill="#b3e297" stroke="{INK}" stroke-width="5"/>'
                 + word(cx, cy, "The arts", 56), box=box), "subjects")
    for i, lines in enumerate(SUBJECTS):
        a = math.radians(90 - 360 * i / len(SUBJECTS))
        ux, uy = math.cos(a), -math.sin(a)
        x, y = cx + rad * ux, cy + rad * uy
        size = 30 if max(len(w) for w in lines) > 10 else 36
        body = (f'<line x1="{cx + (r_mid + 6) * ux:.0f}" y1="{cy + (r_mid + 6) * uy:.0f}" '
                f'x2="{cx + (rad - r_item) * ux:.0f}" y2="{cy + (rad - r_item) * uy:.0f}" stroke="{INK}" stroke-width="6"/>'
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_item}" fill="{COLOURS[i % 4]}" stroke="{INK}" stroke-width="4"/>'
                + word(x, y, lines, size))
        write(i + 1, svg(body, box=box), "subjects")
    print(f"wrote images/fig-arts-subjects-0..{len(SUBJECTS)}.svg")


def fan():
    mx, my, mr = 470, H / 2, 200
    px, pw, ph = 1180, 400, 86
    ys = [H / 2 + (i - (len(EFFECTS) - 1) / 2) * 112 for i in range(len(EFFECTS))]
    write(0, svg(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#b3e297" stroke="{INK}" stroke-width="5"/>'
                 + word(mx, my, "The arts", 60)))
    for i, (label, y) in enumerate(zip(EFFECTS, ys)):
        a = math.atan2(y - my, px - mx)
        x0, y0 = mx + (mr + 8) * math.cos(a), my + (mr + 8) * math.sin(a)
        x1 = px - 18
        c = x0 + (x1 - x0) * 0.55
        body = (f'<path d="M{x0:.0f} {y0:.0f} C{c:.0f} {y0:.0f} {c:.0f} {y:.0f} {x1:.0f} {y:.0f}" fill="none" '
                f'stroke="{INK}" stroke-width="5" marker-end="url(#ar)"/>'
                f'<rect x="{px}" y="{y - ph / 2:.0f}" width="{pw}" height="{ph}" rx="{ph / 2:.0f}" '
                f'fill="{COLOURS[i % 4]}" stroke="{INK}" stroke-width="4"/>'
                + word(px + pw / 2, y, label, 40))
        write(i + 1, svg(body, ARROW))
    print(f"wrote images/fig-arts-impacts-0..{len(EFFECTS)}.svg")


if __name__ == "__main__":
    ring()
    fan()
