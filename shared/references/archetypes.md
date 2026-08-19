# Page archetypes — management set

The eight archetypes management decks and reports actually use, most-frequent first.
Each has a recognition test, the measured grid, and HTML using the shared shell classes
(`.block .two .three .kpis .kpi .tw .card .callout .cover .divider`). Both `deck.html`
and `report.html` define these classes, so the HTML is portable between slide and scroll.

Map each chunk of the user's content to one archetype. When in doubt, pick the one whose
recognition test the content actually passes — the structure should encode something true
about the content, not decorate it.

---

## cover — title page

Grid `full_bleed`/`centered_focal`. Very few words, largest type in the document
(`display_hero`, ≥40pt). Use the shell's `.cover` block: eyebrow (report type · period),
h1, one lede sentence, meta line. One line only in the lede — say what question the
document answers and what the reader should do.

## kpi_grid — headline results (font scale 2.8)

3–12 metric cells in one frame, or 1–3 huge numbers (`big_number_hero`). Numbers
dominate. Place it **early** — no report type opens with a table.

```html
<div class="kpis">
  <div class="kpi"><span class="v">$131.4M</span><span class="l">Q4 revenue</span><span class="d up">+9.5% YoY</span></div>
  <div class="kpi"><span class="v">110%</span><span class="l">Plan attainment</span><span class="d">Plan $120M</span></div>
</div>
```

Numbers must be `tabular-nums` (the `.v`/`.d` classes handle it). Always give a
benchmark — a number with no reference point tells the reader nothing about good or bad.

## chart_text_split — chart beside its reading (font scale 1.8)

A chart next to ≥80 words of explanation. Grid `two_col`. Dominant in `diagnose`.

```html
<div class="block two">
  <figure class="chart"><!-- hand-written SVG --></figure>
  <div>
    <h3>Margin improved three straight quarters on mix shift</h3>
    <p>Explain the cause. Do not restate numbers already on the chart.</p>
  </div>
</div>
```

## chart_multi_grid — 2–6 charts in a grid (font scale 2.24)

Dominant in `monitor`. Use `.two` or `.three`. Keep the **same axis scale** across charts
in a row or the reader compares them wrong.

## comparison_columns — side by side

Before/after, option A/B, plans. Dominant in `decide` and `persuade`. Columns must be
**structurally identical** — same attribute order, same row count. Mismatched structure is
the most common failure here.

```html
<div class="block three">
  <div class="card"><h3>Option A</h3><p>…</p></div>
  <div class="card"><h3>Option B</h3><p>…</p></div>
  <div class="card"><h3>Option C</h3><p>…</p></div>
</div>
```

## takeaway / recommendation block — the decision anchor

Not a corpus archetype but the management workhorse. For `decide`, this leads the page,
before any table. Use the callout.

```html
<div class="callout"><p><strong>Recommendation:</strong> Approve the 40-store expansion; payback is 14 months at the base case.</p></div>
```

## table_dense — detailed figures (font scale 1.69 — lift it)

The number table. Grid `single_col`. Push it to the **appendix**, never the opening. This
archetype measures the lowest hierarchy in the corpus — consciously add header hierarchy.

```html
<div class="tw">
  <table>
    <caption>Unit: $M · Source: sales system, closed 2026-01-05</caption>
    <thead><tr><th>Channel</th><th class="n">Plan</th><th class="n">Actual</th><th class="n">Attain</th></tr></thead>
    <tbody>
      <tr><td>Pharmacy</td><td class="n">120.0</td><td class="n">131.4</td><td class="n hi">110%</td></tr>
      <tr class="total"><td>Total</td><td class="n">165.0</td><td class="n">169.6</td><td class="n">103%</td></tr>
    </tbody>
  </table>
</div>
```

Use `class="n"` on every number cell (turns on tabular-nums, right-align). On slides keep
tables to ~8 rows; longer belongs in an appendix or a scroll report.

## section_divider — chapter break (font scale 2.67)

Under 25 words, centered. Use `.divider` (report) or a full-bleed title slide (deck).

---

## Charts

Hand-write SVG for simple charts (bars, lines, horizontal bars) — no library, no CSP
issues in artifacts, sharp in PDF. Four rules from the corpus:

1. **Label directly on the series**, not via a legend. `direct_label` beats
   `legend_dependent` in every well-designed document.
2. **Drop excess gridlines** — 3–4 faint horizontals max.
3. **Title changes by purpose** — see constants.md §6. Slides take the takeaway.
4. **Show a benchmark** for `monitor` — a target or prior-period line.

Series colors come from `--accent` / `--accent-2`. Don't exceed 2–3 series colors unless
there are genuinely more than 3 series.

## Clever moves that read well (distilled from tagged corpus)

Reusable, brand-agnostic tricks the best decks used — reach for these before defaults:

- **Conclusion as a banner over each chart.** Put the one-line numeric takeaway in a band
  above the chart so the viewer gets the point without reading the axes.
- **Big ordinals instead of bullets.** When five points have no priority order, large
  `01 02 03` anchors let them be read in any order — but only when order is genuinely flat.
- **Mute the context, color the signal.** A map or logo wall recolored to one gray tint,
  with only the labels/one item in accent, reads instantly. Context is gray; signal has color.
- **Repeat the frame, swap the pair.** Reuse the exact 50/50 (or sidebar) layout across
  consecutive pages and change only the color pair — the deck gains a recognizable rhythm.
- **Comparison without cage.** Drop all vertical rules; thin horizontals only; one accent
  tick/mark as the single emphasis. Tables get lighter and more scannable.
- **2×2 with no axes.** A matrix positioned by four corner arrows (no drawn axes) is far
  lighter than a gridded quadrant and reads just as clearly.
- **Big number, source as footnote.** State the evidence at display size; put the source in
  a 10pt caption. Weight goes to the claim, not the citation.
