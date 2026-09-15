# MishMash — a reusable presentation

A generic introduction to MishMash, the Norwegian Centre for AI and Creativity.
One deck that scales from a three-minute pitch to a thirty-minute talk, built
with [reveal.js](https://revealjs.com) and styled in the 2026 MishMash visual
identity.

Open `index.html` in a browser, or serve the folder (`python3 -m http.server`)
so the embedded live pages work.

## Talk length

The deck is progressive: every slide is tagged with a level, and slides above
the chosen level are removed before the deck starts. The spine of the argument
is the same at every length.

| URL | Length | Slides |
| --- | --- | --- |
| `index.html` | ~3 min | 15 |
| `index.html?level=2` | ~10 min | 27 |
| `index.html?level=3` | ~30 min | 39 |

`?level=3min`, `?level=10min` and `?level=30min` work too, as does
`?level=all`. The badge in the top right shows the current length; click it to
cycle. Navigation and slide numbers are always correct for the level you chose,
because the other slides are gone rather than hidden.

## Structure

Six questions, each opening on a full-bleed divider in its own surface colour:

1. **Why?** — the mishmash of opinions about AI, and where the name comes from
2. **What?** — create, explore, reflect; the cube; the seven work packages
3. **Who?** — the consortium, the people network, how disciplines meet
4. **Where?** — the map, the rhythm of a distributed centre
5. **When?** — a five-year centre, caught near its start
6. **Join** — MeshUp, membership, conferences

Every slide has speaker notes. Press **S** for the speaker view.

## Adapting it for a particular talk

Nothing needs editing in the HTML for a normal reuse — the deck is generic by
default and takes what is local to a given talk from the URL.

| Parameter | Effect |
| --- | --- |
| `?venue=Kristiansand&date=15 September 2026` | Adds the occasion to the title slide |
| `?place=uia` | Swaps the generic "where you are" slide for the host institution, and marks that city in red on the map |
| `?static=1` | Replaces the two live embeds with stills, for a room with no working network |

Combine them freely: `index.html?level=2&place=uia&venue=Kristiansand`.

To make the deck local to a new place, add an entry to the `LOCAL` table near
the foot of `index.html`:

```js
ntnu: {
  city: 'trondheim',                 // must match a data-city key on the map
  kicker: 'here',
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

Section dividers use the identity's surface colours with the wordmark in its
paired colour — black on green, green on purple, yellow on blue, red on pink.
Each divider also sets the accent colour for the slides that follow it.

The figures carried over from earlier decks were recoloured from the superseded
palette (`#A7A1F4`, `#C1F7AE`, `#363644`) to the 2026 tokens.

## PDF

```
python3 tools/build_pdf.py            # writes mishmash.pdf
python3 tools/build_pdf.py --level 2  # just the ten-minute deck
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
