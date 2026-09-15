# MishMash - Presentation Slide Deck

A generic introduction to MishMash Centre for AI and Creativity. One deck that scales from a three-minute pitch to a thirty-minute talk, built with [reveal.js](https://revealjs.com) and styled in the 2026 MishMash visual identity.

You can view the presentation at [here](https://mishmash-norway.github.io/mishmash-presentation/), or from the local `index.html` if you download this repo to your own computer.

## Organisation

The deck is organised in two directions. The key chapters (the questions) are laid out horizontally, and their slides hang below them, with progressively more detail below. That means that it is easy to adjust the duration by how far down you go.

## Duration 

Rule of thumb: go one down per question for a 3-minute presentation. Two or three down for a 10-minute presentation, and all down would be 30–45 minutes. 

## Controls

You navigate with **→** between questions and **↓** downwards. You can use **space** to walk through everything, down then right. 

Press **Esc** to get an overview of all the slides. **S** gives you speaker view, and **D** switches between light and dark modes.

## Structure

Seven questions, each opening on a full-bleed page in one of the identity's surface colours, cycling so that no two consecutive ones match:

1. **Why?** — the mishmash of opinions about AI, the name, the definitions
2. **What?** — the objective in one sentence; create, explore, reflect
3. **How?** — the cube, then one slide per work package
4. **Who?** — the consortium, the people network, how disciplines meet
5. **Where?** — the map, the rhythm of a distributed centre
6. **When?** — a five-year centre, caught near its start
7. **Join** — MeshUp, membership, conferences

## Local adaptations

Feel free to fork and edit. There are also some tricks for quick adaptations: 

| Parameter | Effect |
| --- | --- |
| `?venue=Kristiansand&date=15 September 2026` | Adds the occasion to the title slide |
| `?place=uia` | Puts the host institution's people on the local slide instead of the generic institution network |
| `?static=1` | Replaces the two live embeds with stills, for a room with no working network |

Combine them freely: `index.html?place=uia&venue=Kristiansand`.

To make the deck local to a new place, add an entry to the `LOCAL` table near the foot of `index.html`:

```js
ntnu: {
  people: [{ img: 'images/portraits/…jpg', name: '…', role: '…' }],
  notes: 'Speaker notes for this version of the slide.'
}
```

## Design

The deck follows `BRAND.md` in [mishmash-web](https://github.com/MishMash-Norway/mishmash-web). 

## PDF

```
python3 tools/build_pdf.py                 # the whole deck
python3 tools/build_pdf.py --place uia     # with the local slide filled in
python3 tools/build_pdf.py --static        # with the offline stills
```

It screenshots each slide with headless Chrome and assembles the pages with Pillow. Requires `google-chrome` and `pillow`.

## Licence

MIT (see `LICENSE`). Note that the photographs, logos and figures are not covered by it; they belong to MishMash and its partners.
