# MishMash — a reusable presentation

A generic introduction to MishMash, the Norwegian Centre for AI and Creativity.
One deck that scales from a three-minute pitch to a thirty-minute talk, built
with [reveal.js](https://revealjs.com) and styled in the 2026 MishMash visual
identity.

Open `index.html` in a browser, or serve the folder (`python3 -m http.server`)
so the embedded live pages work.

## Talk length

The deck is one stack per question. The question page heads the stack and its
slides hang below it, so how long the talk runs is decided by how far down you
go — in the room, not in advance.

- **→** skips to the next question
- **↓** works through the one you are on
- **Space** walks everything, down then right

Each stack is ordered by priority rather than by narrative, so the first **↓**
is always the slide worth keeping at three minutes. Roughly: one down per
question is three minutes, two or three is ten, all the way down is thirty.

The readout in the top right names the question and how far down it you are
("What? 3/9"). Press **Esc** for the overview — one column per question.

Every slide has speaker notes, and they carry the sentences that are
deliberately not on the screen. Press **S** for the speaker view.

## Structure

Six questions, each opening on a full-bleed page in one of the identity's
surface colours, cycling so that no two consecutive ones match:

1. **Why?** — the mishmash of opinions about AI, the name, the definitions
2. **What?** — create, explore, reflect; the seven work packages; the cube
3. **Who?** — the consortium, the people network, how disciplines meet
4. **Where?** — the map, the rhythm of a distributed centre
5. **When?** — a five-year centre, caught near its start
6. **Join** — MeshUp, membership, conferences

## Adapting it for a particular talk

Nothing needs editing in the HTML for a normal reuse — the deck is generic by
default and takes what is local to a given talk from the URL.

| Parameter | Effect |
| --- | --- |
| `?venue=Kristiansand&date=15 September 2026` | Adds the occasion to the title slide |
| `?place=uia` | Swaps the generic "where you are" slide for the host institution, and marks that city in red on the map |
| `?static=1` | Replaces the two live embeds with stills, for a room with no working network |

Combine them freely: `index.html?place=uia&venue=Kristiansand`.

To make the deck local to a new place, add an entry to the `LOCAL` table near
the foot of `index.html`:

```js
ntnu: {
  city: 'trondheim',                 // must match a data-city key on the map
  heading: 'MishMash in Trondheim',
  lead: 'NTNU is a MishMash partner …',
  points: ['…', '…'],
  people: [{ img: 'images/portraits/…jpg', name: '…', role: '…' }],
  notes: 'Speaker notes for this version of the slide.'
}
```

Adding a city to the map needs a dot as well. Positions come from longitude and
latitude against the outline in `images/mm-norway-map.png`:

```
x = (lon - 4.5) * 22.4903
y = (71.2 - lat) / 0.0183867
```

## Live content

Two slides load from the network:

- the people network, framed from `mishmash.no/people/network/`
- the *Strings On-Line* video, from YouTube

Both are preloaded when the deck opens, so they are ready when you reach them.
If the room has no usable network, add `&static=1`.

## Design

The deck follows `BRAND.md` in
[mishmash-web](https://github.com/MishMash-Norway/mishmash-web): flat surfaces,
hard edges, 2 px ink rules, and no gradients, shadows or rounded corners.
Display type is Roboto Condensed 700, body text is Inter, both self-hosted in
`fonts/`. Colour tokens are copied from `site/assets/css/brand.css` into the
stylesheet at the top of `index.html`.

Each question page is one flat surface colour with nothing on it but the
question. The six cycle through the four surfaces — purple, blue, pink, green,
purple, blue — so no two consecutive pages match. That departs from the
website's section-to-surface table in `BRAND.md`, which governs mishmash.no
rather than a deck. Each question page also sets the accent colour for the
slides under it, which shows as the rule beneath every heading.

The figures carried over from earlier decks were recoloured from the superseded
palette (`#A7A1F4`, `#C1F7AE`, `#363644`) to the 2026 tokens.

## Title slide

The wordmark is inlined (not linked) so that it works over `file://` and so
CSS and script can reach inside it. `js/wordmark.js` is ported from
mishmash.no: it rolls the I/A, S and H columns at random intervals like a
split-flap board. Hovering the mark rolls all three and steps the slide to the
next identity pairing — green/black, purple/green, blue/yellow, pink/red — so
the surface and the wordmark always stay a legal pair. Anyone who has asked
for reduced motion gets the mark held still.

## PDF

```
python3 tools/build_pdf.py                 # the whole deck
python3 tools/build_pdf.py --place uia     # with the local slide filled in
python3 tools/build_pdf.py --static        # with the offline stills
```

It screenshots each slide with headless Chrome and assembles the pages with
Pillow. Requires `google-chrome` and `pillow`.

## Sources

Content is drawn from [mishmash.no](https://mishmash.no) — the centre
description, work package pages, organisation pages and FAQ — and from an
earlier talk on AI and creativity. Figures and photographs come from that deck
and from the website.

## Licence

MIT (see `LICENSE`). Note that the photographs, logos and figures are not
covered by it; they belong to MishMash and its partners.
