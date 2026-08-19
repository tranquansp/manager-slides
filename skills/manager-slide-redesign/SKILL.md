---
name: manager-slide-redesign
description: Redesign an existing slide deck or report so it looks far better, while keeping the same content. Use when the user hands over slides/a deck (HTML, PPTX, or pasted content) and wants to "make it beautiful", "redesign this", "clean it up", "present this properly", or "fix the design" — for a management audience. Preserves the wording and numbers; rebuilds hierarchy, layout, archetype fit, and color. Every design choice is measured from a corpus of 236 real reports.
---

# Manager Slide — Redesign

Take an existing deck or report and produce a better-looking version **without changing
what it says**. You re-tier, re-lay-out, and re-color; you do not rewrite the content or
invent numbers.

Read shared files from the plugin's `shared/` directory: `${CLAUDE_PLUGIN_ROOT}/shared/…`,
or `../../shared/…` relative to this skill.

## The most important lever

Most decks look bad for one measurable reason: everything is the same size
(**font_scale_ratio** ~1.16) so the eye has no entry point. The fix is almost always to
lift the heading/body ratio to **≥1.9** and let the content tier — not to cut words. This
alone rescues most redesigns. (Detail: `shared/references/constants.md`.)

## Flow

### 1. Ingest the source and extract content verbatim
- **HTML**: read the file; pull out every heading, paragraph, number, table, and chart
  data point.
- **PPTX**: use the `pptx` skill to read the slides' text and tables.
- **Pasted content**: use as given.

Keep the extracted content **exactly** — same wording, same figures. This is the contract
of a redesign.

### 2. Audit what's wrong
Note the concrete design failures before rebuilding:
- flat hierarchy (ratio < 1.9), everything one size;
- opens with a big table instead of a takeaway or headline KPIs;
- wrong archetype for the content (e.g. prose where a comparison belongs);
- no color discipline (many hues, or decorative semantic colors);
- emoji bullets, arbitrary numbering, mismatched comparison columns.

### 3. Design Read + elicit only the gaps
State the one-line Design Read (audience · purpose · format · preset). If the target look
or audience is unknown, ask **one** `AskUserQuestion` round (see `shared/styling.md`). If
the source and the user's ask already make it clear, ask nothing.

### 4. Re-map each chunk to the right archetype and rebuild
For each piece of the original, choose the correct archetype from
`shared/references/archetypes.md` and rebuild it in the matching shell
(`shared/assets/deck.html` for slides, `report.html` for a scroll report, `shell.typ` for
print). Apply the styling preset or the user's brand per `shared/styling.md`. Reorder to
the sequence grammar: details to the appendix, a takeaway or KPI block up front.

### 5. Preserve content; upgrade form only
- Do **not** rewrite sentences or change any number.
- You **may** promote a descriptive chart title to a takeaway title (e.g. "Margin by
  quarter" → "Margin improved three quarters running") **only** when the source data
  supports the claim — and note that you did.
- If the original is missing something structural (a `decide` deck with no recommendation),
  flag it; don't invent it.

### 6. Render and LOOK — before and after
```bash
python ${CLAUDE_PLUGIN_ROOT}/shared/scripts/deck_to_pdf.py new-deck.html --pdf new-deck.pdf   # decks
python ${CLAUDE_PLUGIN_ROOT}/shared/scripts/render.py html new-report.html --pdf out.pdf --shots  # reports
```
Open the output with Read and check the four classic failures (theme-on-theme text, table
overflow, orphan titles, empty blocks). Fix and re-render.

### 7. Deliver and list what changed
Publish the HTML as an artifact / send the file, then give a short before→after list:
what hierarchy, archetype, ordering, and color changes you made, and why. This lets the
user trust that the content is intact and see the design reasoning.

## Guardrails
- Content is the user's; wording and numbers are preserved.
- Don't invent data to fill a chart the source lacked — drop it or ask.
- No emoji bullets; no `01/02/03` unless the content is genuinely ordered.
- Check both themes; declare any new color at the token layer (all three theme states).

## Reference map
| File | Read when |
|---|---|
| `shared/references/constants.md` | Always — the measured lookup tables and the 1.9 lever |
| `shared/references/archetypes.md` | Re-mapping each chunk — 8 archetypes + HTML + moves |
| `shared/styling.md` | The elicitation, style presets, brand override, anti-default rules |
| `shared/references/deck.md` | Slides — HTML deck mechanics and PPTX |
| `shared/scripts/render.py` · `deck_to_pdf.py` | Step 6 — render and self-inspect |

## Dependencies
`render.py` needs `playwright`, `typst`, `pymupdf`; `deck_to_pdf.py` needs `playwright`
and `pillow`. Playwright uses the system Chrome. `pip install playwright typst pymupdf
pillow` if missing.
