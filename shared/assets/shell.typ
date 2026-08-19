// TYPST REPORT SHELL — use for print-oriented, high-density reports.
//
// Choose Typst over HTML when: the document runs to dozens of pages, has many
// financial tables, needs footnotes, running chapter headers, or an auto table of
// contents. HTML can do these but struggles; Typst does them out of the box.
//
// Hierarchy ratio held at 1.95 (20.5pt / 10.5pt) — see SKILL.md.
// Compile: python scripts/render.py typst report.typ --pdf report.pdf

#let accent  = rgb("#17427A")   // CHANGE TO FIT THE REPORT (or apply a styling preset)
#let ink     = rgb("#12161F")
#let muted   = rgb("#5A6474")
#let rule    = rgb("#D9DDE4")   // rule color (avoids clashing with the built-in line())
#let raised  = rgb("#EDEFF3")

#let report(
  title: "Report title",
  kind: "Report type · period",
  summary: "",
  issuer: "",
  body,
) = {
  set document(title: title)
  set page(
    paper: "a4",
    margin: (x: 14mm, top: 18mm, bottom: 20mm),
    footer: context [
      #set text(size: 8.5pt, fill: muted)
      #grid(columns: (1fr, auto), issuer, [#counter(page).display()])
    ],
  )
  set text(font: ("Helvetica Neue", "Arial", "Liberation Sans"),
           size: 10.5pt, lang: "en", fill: rgb("#2C3340"))
  set par(justify: true, leading: 0.68em, spacing: 1.0em)

  // type scale — h2/body ratio = 1.95
  show heading.where(level: 1): it => block(below: 14pt)[
    #set text(size: 26pt, fill: ink, weight: 600)
    #it.body
  ]
  show heading.where(level: 2): it => block(above: 22pt, below: 10pt)[
    #set text(size: 20.5pt, fill: ink, weight: 600)
    #it.body
  ]
  show heading.where(level: 3): it => block(above: 14pt, below: 6pt)[
    #set text(size: 12.5pt, fill: ink, weight: 600)
    #it.body
  ]

  // tables: thin horizontal rules, light header fill, right-aligned numbers
  set table(
    stroke: (x, y) => (bottom: 0.5pt + rule),
    fill: (x, y) => if y == 0 { raised },
    inset: (x: 8pt, y: 6pt),
  )
  show table.cell.where(y: 0): set text(size: 8.5pt, fill: muted, weight: 600)

  // COVER
  block[
    #set text(size: 8.5pt, fill: muted, weight: 600, tracking: 1.2pt)
    #upper(kind)
  ]
  heading(level: 1, title)
  if summary != "" {
    block(width: 100%, below: 16pt)[#set text(size: 12pt); #summary]
  }
  line(length: 100%, stroke: 1.5pt + ink)
  v(6pt)

  body
}

// ── Reusable blocks ─────────────────────────────────────────────────────────

// KPI cell. Use near the top — no report type in the corpus opens with a table.
#let kpi(value, label, note: "") = block(
  width: 100%, inset: 12pt, radius: 2pt, stroke: 0.5pt + rule,
)[
  #text(size: 22pt, fill: ink, weight: 600)[#value] \
  #text(size: 9pt, fill: muted)[#label]
  #if note != "" [ \ #text(size: 8.5pt, fill: accent)[#note] ]
]

#let kpi-row(..cells) = grid(columns: cells.pos().len(), gutter: 10pt, ..cells)

// Callout — conclusion, warning, thing to note
#let callout(content) = block(
  width: 100%, inset: (x: 14pt, y: 12pt), radius: (right: 2pt),
  fill: rgb("#DCE5F1"), stroke: (left: 3pt + accent),
)[#set text(fill: ink); #content]

// Small note under a table or chart
#let note(content) = block(above: 6pt)[
  #set text(size: 8.5pt, fill: muted); #content
]

// ── EXAMPLE USAGE ────────────────────────────────────────────────────────────

#show: report.with(
  title: "Report title",
  kind: "Results report · Q4 2025",
  summary: "One sentence stating the question this report answers and what the reader should do after reading it.",
  issuer: "Issuer",
)

#kpi-row(
  kpi("$131.4M", "Q4 revenue", note: "+9.5% YoY"),
  kpi("110%", "Plan attainment", note: "Plan $120M"),
  kpi("$38.2M", "E-commerce", note: "85% of plan"),
)

== A takeaway title, not just a description

Analysis text. Typst justifies both margins and hyphenates per `lang`, so long prose
blocks read noticeably better than left-aligned HTML.

#callout[
  Put the single most important conclusion here. For a decision report, this block
  belongs BEFORE the data table, not after.
]

== Detailed figures

#table(
  columns: (1fr, auto, auto, auto),
  align: (left, right, right, right),
  [Channel], [Plan], [Actual], [Attain],
  [Pharmacy], [120.0], [131.4], [110%],
  [E-commerce], [45.0], [38.2], [85%],
)
#note[Unit: \$M. Source: sales system, closed 2026-01-05.]
