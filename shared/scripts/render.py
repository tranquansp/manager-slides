#!/usr/bin/env python3
"""Render a report to PDF plus self-check screenshots.

  # HTML -> PDF + light/dark screenshots for self-inspection
  python render.py html report.html --pdf report.pdf --shots

  # Typst -> PDF (print, high density)
  python render.py typst report.typ --pdf report.pdf

  # screenshots only, no PDF
  python render.py html report.html --shots

Screenshots are written to `<name>-light.png` and `<name>-dark.png` next to the
source file. OPEN both with the Read tool and actually look at them before you hand
the file over -- it is the only way to catch color-token mistakes, text overflow,
broken tables, or overlapping figures.

Playwright uses the Chrome already installed on the machine (channel="chrome") and
does not download a browser. If Chrome is missing, the script falls back to the
bundled chromium and says so -- run `playwright install chromium` once in that case.

This applies to SCROLL documents (reports). For JS-driven slide decks, use
deck_to_pdf.py instead.
"""
import argparse, os, sys


def render_typst(src, pdf):
    import typst
    typst.compile(src, output=pdf)
    return pdf


def render_html(src, pdf=None, shots=False, fmt="A4",
                margin=("16mm", "16mm", "14mm", "14mm")):
    from playwright.sync_api import sync_playwright
    url = "file://" + os.path.abspath(src)
    stem = os.path.splitext(os.path.abspath(src))[0]
    made = []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            print("  (system Chrome unavailable -> using bundled chromium)",
                  file=sys.stderr)
            browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(250)          # let webfonts / canvas finish painting

        if pdf:
            page.emulate_media(media="print")
            page.pdf(path=pdf, format=fmt, print_background=True,
                     margin={"top": margin[0], "bottom": margin[1],
                             "left": margin[2], "right": margin[3]})
            made.append(pdf)

        if shots:
            page.emulate_media(media="screen", color_scheme="light")
            page.wait_for_timeout(120)
            page.screenshot(path=stem + "-light.png", full_page=True)
            page.emulate_media(color_scheme="dark")
            page.wait_for_timeout(120)
            page.screenshot(path=stem + "-dark.png", full_page=True)
            made += [stem + "-light.png", stem + "-dark.png"]

        browser.close()
    return made


def inspect(pdf):
    """Print a few measurements to catch common layout failures early."""
    try:
        import fitz
    except ImportError:
        return
    d = fitz.open(pdf)
    blank = [i + 1 for i in range(d.page_count)
             if len(d.load_page(i).get_text().strip()) < 5
             and not d.load_page(i).get_images()]
    r = d[0].rect
    print(f"  {d.page_count} pages · {r.width:.0f}x{r.height:.0f}pt", end="")
    print(f" · BLANK PAGES: {blank}" if blank else "")
    d.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("engine", choices=["html", "typst"])
    ap.add_argument("src")
    ap.add_argument("--pdf", default=None)
    ap.add_argument("--shots", action="store_true",
                    help="capture light+dark screenshots for self-inspection (html only)")
    ap.add_argument("--format", default="A4", help="A4 · Letter · A3")
    a = ap.parse_args()

    if not os.path.exists(a.src):
        sys.exit(f"file not found: {a.src}")

    if a.engine == "typst":
        if not a.pdf:
            a.pdf = os.path.splitext(a.src)[0] + ".pdf"
        render_typst(a.src, a.pdf)
        print(f"✓ {a.pdf}", end="")
        inspect(a.pdf)
    else:
        if not (a.pdf or a.shots):
            sys.exit("need at least --pdf or --shots")
        made = render_html(a.src, a.pdf, a.shots, a.format)
        for f in made:
            print(f"✓ {f}", end="")
            if f.endswith(".pdf"):
                inspect(f)
            else:
                print()
        if a.shots:
            print("\n→ Open both screenshots with Read and actually look before delivering.")


if __name__ == "__main__":
    main()
