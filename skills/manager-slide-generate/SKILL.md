---
name: manager-slide-generate
description: Generate a beautiful slide deck or report for a management audience from a prompt, plus any attached files (content, data, a brand guideline). Use when the user wants to "make slides", "build a deck", "put together a board/exec presentation", "create a management report", or "turn this into a deck" — for board, C-level, BU-head, or functional-leader audiences. Produces an HTML deck (16:9), an HTML/Typst report, or a PPTX. Every design choice is measured from a corpus of 236 real reports.
---

# Manager Slide — Generate

Turn a prompt (and any files the user attaches) into a designed deck or report for
managers. What makes this different from "write some nice HTML" is that every choice —
type hierarchy, density, archetype, color, chart title — is looked up from measured
corpus constants, not guessed.

Read shared files from the plugin's `shared/` directory: `${CLAUDE_PLUGIN_ROOT}/shared/…`,
or `../../shared/…` relative to this skill.

## The most important lever

One metric separates well-designed reports from the rest: **font_scale_ratio** (heading ÷
body) — 1.94 in the design-award group vs 1.16 in typical annual reports. Floor it at
**1.9×**. Every shell already bakes this in. Don't cut the user's content to make a page
feel airy; **tier it**. (Full detail: `shared/references/constants.md`.)

## Flow

### 1. Read the input, classify, state a Design Read
Read the prompt and every attached file. Separate **content/data** (what goes in) from a
**brand guideline** (how it looks). Then state a one-line Design Read:

> Reading this as: a `<deck|report>` for `<audience>`, purpose `<purpose>`, `<preset>` look.

Audiences (management only): `board` · `c_level` · `bu_head` · `functional_leader`.
Purposes: `monitor` · `diagnose` · `decide` · `align` · `persuade`.

### 2. Elicit only the gaps — one round
Infer everything you can. If audience, purpose, format, or look is genuinely unknown, ask
**one** `AskUserQuestion` round covering only the unknowns (see `shared/styling.md` — style
is a composite, not a dropdown; most of it follows from the Design Read). If the user gave
a brand file and a clear brief, ask nothing.

### 3. Look up the constants
Read `shared/references/constants.md`: the density, hierarchy, dominant archetypes, and
title style for this audience/purpose. **Density follows the measured norm** (it reflects
the reader's real need); **hierarchy is always lifted to ≥1.9**.

### 4. Outline by sequence grammar, map to archetypes
Build the outline using the sequence grammar (no deck/report opens with a table; details
go last). Map each content chunk to an archetype from `shared/references/archetypes.md`,
which has the HTML and the "clever moves" that read well.

### 5. Pick the engine and build
| Output | Start from | When |
|---|---|---|
| **HTML deck** | `shared/assets/deck.html` | Slides to present or pre-read. Publish as an artifact. |
| **HTML report** | `shared/assets/report.html` | On-screen report, charts, shareable link, under ~20 pages. |
| **Typst** | `shared/assets/shell.typ` | Print-oriented, dense, many tables, footnotes, TOC. |
| **PPTX** | `shared/references/deck.md` | Editable PowerPoint. Use the `pptx` skill. |

Apply a styling preset (or the user's brand) by overriding the accent/font tokens per
`shared/styling.md`. Keep the layout and the 1.9 floor regardless of the brand.

### 6. Render and LOOK before delivering
The most-skipped, highest-catch step. You cannot tell if a page overflows, a table breaks,
or a theme color is wrong without seeing it.

```bash
# scroll report → PDF + light/dark screenshots
python ${CLAUDE_PLUGIN_ROOT}/shared/scripts/render.py html report.html --pdf report.pdf --shots
# HTML deck → PDF (screenshots each slide)
python ${CLAUDE_PLUGIN_ROOT}/shared/scripts/deck_to_pdf.py deck.html --pdf deck.pdf
```

Open the PNGs (or deck PDF) with Read and actually look. Fix the four classic failures —
theme-on-theme text, table overflow, orphan titles, empty blocks — then re-render.

### 7. Deliver and say what you chose
Publish HTML as an artifact and give the link; send PDF/PPTX. Add 2–3 lines on how you
classified the audience/purpose and which engine and preset you chose, so the user can
correct a wrong guess.

## Guardrails
- **Don't invent numbers.** If a chart needs data the user didn't give, ask or drop it.
- **Don't add sections the user didn't provide.** Present their content; if a needed part
  is missing (e.g. a `decide` deck with no recommendation), say so — don't fill it in.
- No emoji bullets; no `01/02/03` unless the content is genuinely ordered.
- Check both themes; declare any new color at the token layer (all three theme states).

## Reference map
| File | Read when |
|---|---|
| `shared/references/constants.md` | Always, step 3 — the measured lookup tables |
| `shared/references/archetypes.md` | Building each block — 8 archetypes + HTML + moves |
| `shared/styling.md` | The elicitation, style presets, brand override, anti-default rules |
| `shared/references/deck.md` | Slides — HTML deck mechanics and PPTX |
| `shared/scripts/render.py` · `deck_to_pdf.py` | Step 6 — render and self-inspect |

## Dependencies
`render.py` needs `playwright`, `typst`, `pymupdf`; `deck_to_pdf.py` needs `playwright`
and `pillow`. Playwright uses the system Chrome — no `playwright install` needed unless
Chrome is absent. `pip install playwright typst pymupdf pillow` if missing.
