#!/usr/bin/env python3
"""Build a flat PDF of the MishMash deck.

Screenshots every slide with headless Chrome at 1920x1080 and assembles the
pages with Pillow. Run from anywhere:

    python3 tools/build_pdf.py                 # the full 30-minute deck
    python3 tools/build_pdf.py --level 2       # just the 10-minute deck
    python3 tools/build_pdf.py --place uia     # with the local slide filled in

The deck is served over HTTP rather than opened as file:// so that the
self-hosted fonts and the embedded live pages behave the same as they do in a
talk.
"""
import argparse
import http.server
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
from urllib.parse import urlencode

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PRES = os.path.dirname(HERE)
INDEX = os.path.join(PRES, "index.html")

CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser")
               if shutil.which(c)), None)


def slide_count(level):
    """How many slides survive the level filter — mirrors the deck's own rule."""
    html = open(INDEX, encoding="utf8").read()
    body = html.split('<div class="slides">', 1)[1]
    levels = re.findall(r'<section[^>]*data-level="(\d)"', body)
    return sum(1 for l in levels if int(l) <= level)


def serve(directory):
    """Serve the deck on a free port; returns (port, shutdown)."""
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=directory, **kw)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1], httpd.shutdown


def shoot(url, out, budget):
    subprocess.run(
        [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
         "--hide-scrollbars", "--window-size=1920,1080",
         # Cross-origin iframes do not paint reliably under virtual time with
         # site isolation on, which leaves the live embeds blank.
         "--disable-features=IsolateOrigins,site-per-process",
         "--disable-site-isolation-trials",
         f"--virtual-time-budget={budget}", f"--screenshot={out}", url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", type=int, default=3, choices=(1, 2, 3),
                    help="talk length: 1=3min, 2=10min, 3=30min (default 3)")
    ap.add_argument("--place", default=None, help="a key from the LOCAL table")
    ap.add_argument("--static", action="store_true",
                    help="use the offline stills instead of the live embeds")
    ap.add_argument("--budget", type=int, default=9000,
                    help="milliseconds of virtual time per slide")
    ap.add_argument("-o", "--out", default=None, help="output PDF path")
    args = ap.parse_args()

    if CHROME is None:
        sys.exit("No Chrome or Chromium found on PATH.")

    total = slide_count(args.level)
    out = args.out or os.path.join(PRES, f"mishmash-level{args.level}.pdf")

    query = {"level": args.level}
    if args.place:
        query["place"] = args.place
    if args.static:
        query["static"] = "1"

    port, shutdown = serve(PRES)
    base = f"http://127.0.0.1:{port}/index.html?{urlencode(query)}"

    pages = []
    with tempfile.TemporaryDirectory() as tmp:
        try:
            for i in range(total):
                png = os.path.join(tmp, f"s{i:03d}.png")
                print(f"  slide {i + 1}/{total}", end="\r", flush=True)
                shoot(f"{base}&print=1#/{i}", png, args.budget)
                if os.path.exists(png):
                    pages.append(Image.open(png).convert("RGB"))
                else:
                    print(f"\n  ! slide {i + 1} did not render; skipped")
        finally:
            shutdown()

        if not pages:
            sys.exit("Nothing rendered.")
        pages[0].save(out, save_all=True, append_images=pages[1:],
                      resolution=150.0)

    print(f"\nWrote {out} — {len(pages)} page(s)")


if __name__ == "__main__":
    main()
