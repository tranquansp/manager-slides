#!/usr/bin/env python3
"""Turn an HTML deck (JS-driven slides) into a PDF by screenshotting each slide
exactly as it renders, then stitching the shots together.

  python deck_to_pdf.py deck.html --pdf deck.pdf [--width 1600] [--slide-selector ".slide"]

WHY NOT @media print
────────────────────
Decks like this are usually built from nested flex, slides stacked with
position:absolute + transform, and an inner scroll container. Forcing pagination
with print CSS fails one layer at a time: first only one page prints, then blocks
overlap because Chrome fragments the flex, then content is clipped because an inner
container scrolls. Every patch exposes a new layer.

Screenshotting has no layers: what is on screen is what lands in the PDF. The one
trade-off is that text in the PDF is not selectable/searchable. That is acceptable
for a pre-read handout; if selectable text is required, rebuild the document as a
vertical scroll instead of patching the deck.

The script auto-detects how to advance slides: it calls `go(i)` if the page defines
it, else clicks a next button, else strips the transform per slide manually.
"""
import argparse, io, os, sys


def build(src, pdf, width=1600, selector=".slide", settle=420):
    from playwright.sync_api import sync_playwright
    from PIL import Image

    url = "file://" + os.path.abspath(src)
    shots = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width,
                                          "height": round(width * 9 / 16)})
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(600)

        # Kill every transition/animation before capturing. Decks often slide
        # horizontally over 400-600ms; capturing sooner catches the old slide
        # mid-transit (typically a color band on the left edge). Waiting longer
        # also works but means guessing the duration -- disabling is certain.
        page.add_style_tag(content="*,*::before,*::after{"
                                   "transition:none !important;"
                                   "animation:none !important}")

        n = page.evaluate(f"document.querySelectorAll('{selector}').length")
        if not n:
            browser.close()
            sys.exit(f"no slides match selector {selector!r}")

        mode = page.evaluate("typeof window.go === 'function' ? 'go' : "
                             "(document.querySelector('.navarrow.right,#nextBtn') ? 'click' : 'manual')")
        print(f"  {n} slides · advancing via: {mode}", file=sys.stderr)

        for i in range(n):
            if mode == "go":
                page.evaluate(f"window.go({i})")
            elif mode == "click":
                if i:
                    page.click(".navarrow.right, #nextBtn")
            else:
                page.evaluate(f"""(() => {{
                    document.querySelectorAll({selector!r}).forEach((el, k) => {{
                        el.style.setProperty('opacity', k === {i} ? '1' : '0', 'important');
                        el.style.setProperty('visibility', k === {i} ? 'visible' : 'hidden', 'important');
                        el.style.setProperty('transform', k === {i} ? 'none' : 'translateX(200%)', 'important');
                    }});
                }})()""")
            page.wait_for_timeout(settle)          # let the transition finish
            shots.append(page.screenshot(type="png"))
            print(f"\r  captured {i+1}/{n}", end="", file=sys.stderr)

        browser.close()

    print(file=sys.stderr)
    ims = [Image.open(io.BytesIO(b)).convert("RGB") for b in shots]
    ims[0].save(pdf, "PDF", save_all=True, append_images=ims[1:],
                resolution=150.0)
    return len(ims)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--pdf", default=None)
    ap.add_argument("--width", type=int, default=1600,
                    help="capture width; 1600 is ~150dpi at 16:9")
    ap.add_argument("--slide-selector", default=".slide")
    ap.add_argument("--settle", type=int, default=420,
                    help="ms to wait for the transition between slides")
    a = ap.parse_args()

    if not os.path.exists(a.src):
        sys.exit(f"file not found: {a.src}")
    pdf = a.pdf or os.path.splitext(a.src)[0] + ".pdf"

    n = build(a.src, pdf, a.width, a.slide_selector, a.settle)
    size = os.path.getsize(pdf) / 1048576
    print(f"✓ {pdf} · {n} pages · {size:.1f} MB")
    print("  Note: image PDF — text is not selectable/searchable.")


if __name__ == "__main__":
    main()
