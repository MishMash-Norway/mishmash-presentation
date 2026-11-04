#!/usr/bin/env python3
"""The "AI is not one thing" figure, as three stacked SVG layers for click builds.

    python3 tools/make_ai_kinds.py

Layer 1 is five kinds of system side by side, layer 2 marks the generative ones, and layer 3 adds an
agent below that uses several of them as tools. Writes images/fig-ai-kinds-{1,2,3}.svg, all on the
same canvas so they stack in a .layers div.
"""
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1600, 760
INK, GREEN, PURPLE, GREEN_T, PURPLE_T = "#231f20", "#b3e297", "#9a90cf", "#f0f8e9", "#f0eef9"
FONT = "font-family:'Roboto Condensed','Arial Narrow',Arial,sans-serif;font-weight:700"
# label, generative?
KINDS = [("Rules", False), ("Search", False), ("Language\nmodels", True), ("Image\nmodels", True),
         ("Sound\nmodels", True)]
BW, BH, GAP, TOP = 250, 150, 40, 150
X0 = (W - (len(KINDS) * BW + (len(KINDS) - 1) * GAP)) / 2
AGENT = (W / 2, 600, 420, 120)       # centre x, centre y, width, height


def text(x, y, s, size=40, anchor="middle", fill=INK):
    lines = s.split("\n")
    y0 = y - (len(lines) - 1) * size * 0.55
    return "".join(f'<text x="{x:.0f}" y="{y0 + i * size * 1.1:.0f}" text-anchor="{anchor}" dominant-baseline="middle" '
                   f'font-size="{size}" fill="{fill}" style="{FONT}">{line}</text>' for i, line in enumerate(lines))


def boxes():
    out = []
    for i, (label, gen) in enumerate(KINDS):
        x = X0 + i * (BW + GAP)
        out.append(f'<rect x="{x:.0f}" y="{TOP}" width="{BW}" height="{BH}" rx="18" fill="{GREEN_T if gen else PURPLE_T}" '
                   f'stroke="{GREEN if gen else PURPLE}" stroke-width="5"/>' + text(x + BW / 2, TOP + BH / 2, label))
    return "".join(out)


def generative():
    gen = [i for i, (_, g) in enumerate(KINDS) if g]
    x1, x2 = X0 + gen[0] * (BW + GAP), X0 + gen[-1] * (BW + GAP) + BW
    y = TOP - 40
    return (f'<path d="M{x1:.0f} {y + 20} V{y} H{x2:.0f} V{y + 20}" fill="none" stroke="{INK}" stroke-width="4"/>'
            + text((x1 + x2) / 2, y - 40, "Generative AI", 40))


def agent():
    cx, cy, w, h = AGENT
    out = []
    for i in range(len(KINDS)):
        x = X0 + i * (BW + GAP) + BW / 2
        out.append(f'<line x1="{cx:.0f}" y1="{cy - h / 2:.0f}" x2="{x:.0f}" y2="{TOP + BH + 12}" stroke="{INK}" '
                   f'stroke-width="4" stroke-dasharray="10 10"/>')
    out.append(f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="60" fill="{INK}"/>'
               + text(cx, cy, "Agent", 48, fill="#ffffff"))
    out.append(text(cx + w / 2 + 30, cy, "uses several as tools", 34, anchor="start"))
    return "".join(out)


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{body}</svg>'


def main():
    for k, body in enumerate([boxes(), generative(), agent()], 1):
        path = os.path.join(HERE, "images", f"fig-ai-kinds-{k}.svg")
        open(path, "w", encoding="utf-8").write(svg(body))
        print("wrote", os.path.relpath(path, HERE))


if __name__ == "__main__":
    main()
