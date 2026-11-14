#!/usr/bin/env python3
"""The "art influences far more than art" figure, as stacked SVG layers for click builds.

    python3 tools/make_arts_impacts.py

The arts on the left and a fan of arrows out to a column of the areas they influence, from the
body outwards, one per layer. No numbers. Adapted from the music figure in the deck for the Musikk
i skolen conference, 30 October 2026, with the arts in place of music. Writes
images/fig-arts-impacts-0..8.svg, all on the same canvas so they stack in a .layers div.
"""
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# From the body outwards: body, feelings and thinking, expression, community and culture.
EFFECTS = ["Motor", "Health", "Emotional", "Cognitive", "Linguistic", "Aesthetic", "Social", "Cultural"]
COLOURS = ["#9a90cf", "#a5cbed", "#efadb2", "#b3e297"]
W, H = 1920, 1000
INK = "#231f20"
FONT = "font-family:'Roboto Condensed','Arial Narrow',Arial,sans-serif;font-weight:700"
ARROW = (f'<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
         f'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker>')


def svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<defs>{defs}</defs>{body}</svg>')


def word(x, y, s, size):
    return (f'<text x="{x:.0f}" y="{y + size * 0.35:.0f}" text-anchor="middle" font-size="{size}" '
            f'fill="{INK}" style="{FONT}">{s}</text>')


def write(n, text):
    with open(os.path.join(HERE, "images", f"fig-arts-impacts-{n}.svg"), "w", encoding="utf-8") as f:
        f.write(text)


def main():
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
    main()
