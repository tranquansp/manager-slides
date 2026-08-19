# Design constants — management lookup

Every number here is measured from a corpus of 236 real reports (17,947 pages,
3,392 tagged). This file is trimmed to the **management slice** — four audiences and
five purposes. The full corpus covers nine of each; the rest (investor IR, regulator,
customer/employee comms) are out of scope for this skill.

## The one lever that matters most

Across the whole corpus, a single metric separates the well-designed reports from the
rest:

> **font_scale_ratio** = heading size ÷ body size
> Design-award group: **1.94** · S&P 500 annual reports: **1.16**
> A 5.9-sigma gap — the most robust finding in the corpus.

Most corporate reports look bad **not because they have too much text** but because
everything is the same size and the eye has no entry point. The well-designed group did
*not* use less text (339 vs 309 words/page). So don't cut the user's content to make a
page feel airy. **Tier it.** Floor the h2/body ratio at **1.9×**. This is the cheapest,
highest-leverage move available. Every shell in `assets/` already bakes in 1.95.

## 1. By audience (management only)

| audience | docs | measured hierarchy | words/pg | dominant archetype |
|---|---:|---:|---:|---|
| `functional_leader` | 7 | 2.53 | 222 | narrative_prose · chart_text_split |
| `bu_head` | 6 | 2.15 | 170 | table_dense · dashboard_composite |
| `c_level` | 14 | 1.80 → lift to ≥1.9 | 252 | table_dense · chart_multi_grid |
| `board` | 18 | 1.20 → lift to ≥1.9 | 244 | table_dense (31%) |

**How to read this.** The "words/pg" and "dominant archetype" columns reflect the
reader's **real need** — follow them. The "measured hierarchy" column reflects the
**status quo**, and for `board` / `c_level` the status quo is poor. For those two, keep
the density but lift the hierarchy to ≥1.9. Boards get the rawest documents in the
corpus; deliberately do better than the measured norm.

## 2. By purpose (management only)

| purpose | docs | hierarchy | density | words/pg | dominant archetype |
|---|---:|---:|---|---:|---|
| `align` | 84 | 2.67 | sparse | 138 | infographic_illustrated · section_divider |
| `monitor` | 129 | 2.29 | light | 165 | chart_multi_grid · table_dense |
| `persuade` | 168 | 2.00 | sparse | 96 | photo_text_split · cover |
| `diagnose` | 67 | 1.81 | medium | 207 | chart_text_split · chart_multi_grid |
| `decide` | 19 | 1.71 | dense | 202 | table_dense · toc_agenda |

**The through-line** (r = −0.56): the more accountability a report carries, the flatter
and denser its type gets. `decide` is the surprise — it sits low on hierarchy with 202
words/page and a table-dense body, against the popular image of a one-page
"conclusion-first" memo. Decision-makers actually want the comparison data. So for
`decide`: keep the comparison table, but put **one strongly-tiered takeaway block first**,
then the table.

### Density thresholds (words/page)

`sparse` < 40 · `light` 40–140 · `medium` 140–350 · `dense` 350–800 · `extreme` > 800

## 3. Per-archetype font scale (measured medians)

The 1.9 floor is a floor — several archetypes run higher, and one runs below and needs a
conscious lift:

| archetype | measured font scale | note |
|---|---:|---|
| `kpi_grid` | 2.8 | numbers dominate; biggest contrast |
| `section_divider` | 2.67 | display type, almost no body |
| `dashboard_composite` | 2.67 | |
| `toc_agenda` | 2.45 | |
| `chart_multi_grid` | 2.24 | |
| `big_number_hero` | 1.85 | one or three huge numbers |
| `chart_text_split` | 1.80 | |
| `table_dense` | 1.69 | **lift this** — add real header hierarchy |
| `cover` | display_hero (≥40pt) | different regime; largest type in the doc |

## 4. Sequence grammar

The management formats share one rule: **detailed numbers go last; the body is for
synthesis charts and argument. No report type in the corpus opens with a table.** If the
user's content starts with a big table, move it down and open with a takeaway block or
headline KPIs instead.

Typical management flow (executive deck / MBR):
`cover` → `kpi_grid` (headline result) → `chart_multi_grid` / `chart_text_split` (drivers)
→ `comparison_columns` or takeaway block (for `decide`) → `table_dense` (appendix).

## 5. Color

Corpus distribution of color roles: `single_accent` 33% · `mono_neutral` 28% ·
`brand_spectrum` 12% · `dual_accent` 11% · `dark_mode` 9% · rest ≤3%.

Nearly two-thirds of pages use **one accent or none**. A many-hue palette
(`brand_spectrum`) appears mostly when several data series must be told apart in a chart.
Use `semantic_status` (green/amber/red) **only** when the report genuinely has a
met/not-met/at-risk status — it carries meaning, it is not decoration, and it stays
separate from the brand accent. Pick the accent from content or a styling preset; do not
default. See `styling.md`.

## 6. Chart titles: takeaway vs descriptive

The second-largest measured difference, and the one most often gotten wrong.

- `takeaway_title` = "Margin improved for three straight quarters"
- `descriptive_title` = "Margin by quarter"

Rule for management: **slides almost always take the takeaway title** — the viewer has a
few seconds per slide and reads the title first. Persuasive/aligning reports (`persuade`,
`align`) lean takeaway; the exceptions are appendix and reference slides, where a
descriptive title is correct because the reader is looking up a number, not being told
what it means.
