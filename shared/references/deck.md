# Slides — HTML deck and PPTX

Read this when the output is a slide deck. Two engines:

- **HTML deck** (default for slides) — build from `assets/deck.html`, a 16:9 shell with
  `.slide` sections and a `window.go(i)` navigator. Publish as an artifact for viewing;
  export to PDF with `scripts/deck_to_pdf.py` (it screenshots each slide, so what renders
  is what prints). Use `render.py` only for scroll reports, not decks.
- **PPTX** — when the manager needs an editable PowerPoint file. Use the `pptx` skill; the
  sizing and layout rules below come from the corpus.

## Deck vs read-report

| | presentation deck | read report |
|---|---|---|
| density | sparse→light (40–140 words/slide) | medium→dense (140–800) |
| shape | 16:9 landscape | A4 portrait |
| body archetypes | chart_multi_grid, comparison_columns, kpi_grid | narrative_prose, table_dense |

If the user says "slides" but the content is report-dense, say so and offer a choice: a
deck to **present** must cut to ~100 words/slide; a deck to **pre-read** can stay dense,
but then an HTML scroll report usually serves better.

## Slide sequence

Executive / earnings-style flow measured in the corpus:
`cover` → (disclaimer if any) → `kpi_grid` (headline) → `chart_multi_grid` (drivers) →
`table_dense` → appendix. No deck opens with a table.

## Slide typography

The hierarchy ratio still applies but landscape allows more: well-designed portrait
reports measure 1.94, landscape brand decks up to 3.11. Sizing for 13.33 × 7.5 in (16:9):

| role | size |
|---|---|
| slide title | 30–36pt |
| body | 16–18pt |
| caption / source | 10–11pt |
| KPI number | 54–72pt |

Title/body at 32/17 ≈ **1.9** — the floor. `deck.html` bakes this in.

## Slide titles state the conclusion

The single biggest gap between good and average decks: pitch decks use a conclusion-title
on 63% of chart slides, annual reports 4%. On a slide, almost always use the takeaway
title — the viewer reads it first and may read nothing else. Exception: appendix/lookup
slides take a descriptive title.

## When building with the pptx skill

- 16:9 (13.333 × 7.5 in); safe margins ≥0.5 in — projectors crop edges.
- ≤ ~8 rows per table; longer splits to another slide or the appendix.
- One idea per slide. If the title needs "and" to join two ideas, that's two slides.
- Source line at the foot in 10pt muted — a consistent habit in the investor-deck corpus.
