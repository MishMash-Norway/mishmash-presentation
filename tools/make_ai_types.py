#!/usr/bin/env python3
"""Six kinds of AI system by complexity and autonomy, as stacked SVG layers for click builds.

    python3 tools/make_ai_types.py

Splits images/ai-types-autonomy.svg into images/fig-ai-types-0.svg (the two axes) and
fig-ai-types-1..6.svg, one system type per layer: its dashed link from the previous type, its dot
and its label. Then draws fig-ai-types-hitl.svg, a person with an arrow out to the line of types
and one back, so the two make a loop: the human in the loop. Adapted from the Norwegian figure in
the deck for Musikk i skolen, 30 October 2026; edit the base SVG's labels, not the layers.
"""
import math
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(HERE, "images")
INK, FILL = "#1a202c", "#efadb2"
LINE = (252, 649), (1330, 162)     # from Bots to Autonomous systems in the base SVG
CX, CY = 400, 260                  # the person, in the empty upper left


def shorten(path, gap=30):
    """Trim a dashed link so it stops at the dots instead of crossing them."""
    x1, y1, x2, y2 = map(float, re.search(r"d='M(\S+) (\S+) L(\S+) (\S+)'", path).groups())
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    new = f"d='M{x1 + gap * ux:.0f} {y1 + gap * uy:.0f} L{x2 - gap * ux:.0f} {y2 - gap * uy:.0f}'"
    return re.sub(r"d='M[^']*'", new, path)


def split():
    src = open(os.path.join(IMG, "ai-types-autonomy.svg"), encoding="utf-8").read()
    head = src[:src.index("</defs>") + len("</defs>")]
    body = src[len(head):src.rindex("</svg>")].strip()
    elements = re.findall(r"<(?:path|circle)[^>]*/>|<text[^>]*>[^<]*</text>", body)
    assert sum(len(e) for e in elements) == len(re.sub(r"\s+$", "", body)), "unparsed content in the SVG"
    groups, pending = [[]], []
    for e in elements:
        if e.startswith("<circle"):
            groups.append(pending + [e])
            pending = []
        elif "stroke-dasharray" in e:
            pending.append(shorten(e))
        elif len(groups) == 1:
            groups[0].append(e)
        else:
            groups[-1].append(e)
    for i, g in enumerate(groups):
        with open(os.path.join(IMG, f"fig-ai-types-{i}.svg"), "w", encoding="utf-8") as f:
            f.write(head + "".join(g) + "</svg>")
    print(f"wrote images/fig-ai-types-0..{len(groups) - 1}.svg")


def on_line(x):
    (x0, y0), (x1, y1) = LINE
    return x, y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def curve(p, c, q):
    return (f"<path d='M{p[0]:.0f} {p[1]:.0f} Q{c[0]:.0f} {c[1]:.0f} {q[0]:.0f} {q[1]:.0f}' fill='none' "
            f"stroke='{INK}' stroke-width='9' marker-end='url(#hl)'/>")


def hitl():
    tx, ty = on_line(760)       # out: over the top to the line between Assistants and Agents
    out = curve((CX + 70, CY - 40), (720, 170), (tx, ty - 30))
    bx, by = on_line(560)       # back: from between Chatbots and Assistants round to the person
    back = curve((bx - 10, by + 25), (CX + 10, by + 40), (CX, CY + 125))
    r = 48
    person = (f"<circle cx='{CX}' cy='{CY - 62}' r='38' fill='{FILL}' stroke='{INK}' stroke-width='5'/>"
              f"<path d='M{CX - r} {CY + 95} L{CX - r} {CY - 2 + r} A{r} {r} 0 0 1 {CX + r} {CY - 2 + r} "
              f"L{CX + r} {CY + 95} Z' fill='{FILL}' stroke='{INK}' stroke-width='5'/>")
    label = (f"<text x='{CX}' y='{CY - 130}' text-anchor='middle' font-size='40' fill='{INK}' "
             f"font-weight='bold'>Human in the loop</text>")
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 800' "
           "font-family='Inter, Helvetica Neue, Helvetica, Arial, sans-serif'>"
           f"<defs><marker id='hl' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='4' markerHeight='4' "
           f"orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='{INK}'/></marker></defs>"
           + out + back + person + label + "</svg>")
    with open(os.path.join(IMG, "fig-ai-types-hitl.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote images/fig-ai-types-hitl.svg")


if __name__ == "__main__":
    split()
    hitl()
