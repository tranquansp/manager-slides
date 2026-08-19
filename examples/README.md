# Examples

Two worked examples, one per skill. Both were rendered and visually inspected in light
and dark themes; the exported PDFs are the proof.

## generate — `mbr-deck.html`
A Monthly Business Review deck (`audience=c_level`, `purpose=monitor`+`diagnose`,
**Consulting** preset). Seven slides: takeaway cover → headline KPIs → a hand-written SVG
attainment chart with the miss in a semantic red → root-cause cards → options → detail
table (appendix) → recommendation callout. Exported: `mbr-deck.pdf`.

## redesign — `redesign-before.html` → `redesign-after.html`
`redesign-before.html` is a typical flat deck: everything one size (`font_scale ~1.0`),
opens with a table, emoji bullets, garish heading colors. `redesign-after.html` is the
rebuilt version (**Keynote** preset) — **same content, same numbers** — with a takeaway
cover, the table's data promoted to a headline KPI grid, rationale as cards, the table
moved to the appendix, and the ask as a callout. Compare `redesign-before.pdf` with
`redesign-after.pdf`.

## Regenerate

```bash
python ../shared/scripts/deck_to_pdf.py mbr-deck.html --pdf mbr-deck.pdf
python ../shared/scripts/deck_to_pdf.py redesign-after.html --pdf redesign-after.pdf
python ../shared/scripts/render.py html redesign-before.html --pdf redesign-before.pdf
```

To view a deck live, open the `.html` in a browser (arrow keys navigate) or publish it as
an artifact.
