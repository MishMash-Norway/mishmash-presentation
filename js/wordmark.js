/* Rolling wordmark on the title slide.
 *
 * Ported from mishmash.no (site/assets/js/wordmark.js). The inline MISH/MASH
 * mark has its I/A, S and H columns built as vertical strips of repeated
 * glyphs behind a clip; this rolls one to three of them at random intervals,
 * in random directions, like a split-flap board that never quite settles.
 *
 * Added here: hovering the mark rolls all three columns *and* advances the
 * slide to the next identity pairing — green/ink, purple/green, blue/yellow,
 * pink/red — so the surface and the wordmark always stay a legal pair.
 *
 * Anyone who prefers reduced motion gets the static mark and an instant
 * colour change. Geometry: mishmash-web/scripts/build_identity_logo.py.
 */
(function () {
  'use strict';

  var mark = document.querySelector('.mm-wordmark .mm-wordmark-svg');
  if (!mark || !window.matchMedia) { return; }
  var holder = mark.closest('.mm-wordmark');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  var P = 129.66;                 // pitch between repeated S and H glyphs
  var IA = [127.104, 132.216];    // I→A and A→I steps (sum = 2P)
  var EASE = 'cubic-bezier(.7, 0, .3, 1)';

  var cols = {
    s:  { el: mark.querySelector('.mm-col-s'),  off: 0, busy: false, period: P },
    h:  { el: mark.querySelector('.mm-col-h'),  off: 0, busy: false, period: P },
    ia: { el: mark.querySelector('.mm-col-ia'), off: 0, busy: false, period: 2 * P, parity: 0 }
  };
  if (!cols.s.el || !cols.h.el || !cols.ia.el) { return; }

  function rand(a, b) { return a + Math.random() * (b - a); }
  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function set(c, off, ms) {
    c.el.style.transition = ms ? 'transform ' + ms + 'ms ' + EASE : 'none';
    c.el.style.transform = 'translateY(' + off.toFixed(3) + 'px)';
    c.off = off;
  }

  /* Roll one column by one glyph in direction dir (-1 up, +1 down). */
  function roll(key, dir, ms) {
    var c = cols[key];
    if (c.busy) { return; }
    c.busy = true;
    var step = P;
    if (key === 'ia') {
      /* From "I on top" an upward roll brings A up by 127.1; from "A on top"
         it brings I up by 132.2 — and the other way round going down. */
      step = ((dir < 0) === (c.parity === 0)) ? IA[0] : IA[1];
      c.parity ^= 1;
    }
    set(c, c.off + dir * step, ms);
    window.setTimeout(function () {
      /* A whole period is the same picture: jump back silently so the strip
         never runs out of glyphs. */
      if (Math.abs(Math.abs(c.off) - c.period) < 0.5) {
        set(c, 0, 0);
        void c.el.getBoundingClientRect();
      }
      c.busy = false;
    }, ms + 40);
  }

  /* One gesture: n columns, staggered, each in a random direction (half the
     time they share one direction, like a real board). */
  function gesture(n) {
    var keys = ['s', 'h', 'ia'].sort(function () { return Math.random() - 0.5; }).slice(0, n);
    var shared = Math.random() < 0.5 ? pick([-1, 1]) : 0;
    var delay = 0;
    keys.forEach(function (key) {
      var dir = shared || pick([-1, 1]);
      var ms = Math.round(rand(650, 1100));
      window.setTimeout(function () { roll(key, dir, ms); }, delay);
      delay += Math.round(rand(90, 280));
    });
  }

  /* Only fidget while the title slide is the one on screen. */
  function onTitleSlide() {
    var slide = holder.closest('section');
    return slide && slide.classList.contains('present');
  }

  function loop() {
    if (!reduce.matches && !document.hidden && onTitleSlide()) {
      gesture(pick([1, 1, 2, 2, 3]));
    }
    window.setTimeout(loop, Math.round(rand(2500, 8000)));
  }
  window.setTimeout(loop, Math.round(rand(700, 1500)));

  /* ---- Hover: roll everything, and step to the next identity pairing ----
     The four surfaces of the identity with the wordmark colour each one takes.
     Never any other combination — see BRAND.md. */
  var PAIRS = [
    { surface: '#b3e297', ink: '#231f20' },   // green  → black
    { surface: '#9a90cf', ink: '#b3e297' },   // purple → green
    { surface: '#a5cbed', ink: '#d1e422' },   // blue   → yellow
    { surface: '#efadb2', ink: '#ee5648' }    // pink   → red
  ];
  var at = 0;

  function background() {
    if (!window.Reveal || !Reveal.isReady || !Reveal.isReady()) { return null; }
    var slide = holder.closest('section');
    return slide ? Reveal.getSlideBackground(slide) : null;
  }

  function advance() {
    at = (at + 1) % PAIRS.length;
    var pair = PAIRS[at];
    holder.style.color = pair.ink;
    var bg = background();
    if (bg) {
      bg.style.transition = reduce.matches ? 'none' : 'background-color 420ms ease';
      bg.style.backgroundColor = pair.surface;
    }
  }

  /* The funder credit belongs to the title slide only. */
  var funder = document.getElementById('funder');
  function syncFunder() { if (funder) { funder.hidden = !onTitleSlide(); } }
  if (window.Reveal) {
    Reveal.on('ready', syncFunder);
    Reveal.on('slidechanged', syncFunder);
  }
  syncFunder();

  holder.addEventListener('mouseenter', function () {
    if (!reduce.matches) { gesture(3); }
    advance();
  });
  holder.addEventListener('click', advance);
  holder.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); advance(); }
  });
})();
