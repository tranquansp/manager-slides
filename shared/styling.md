# Styling — composite style + presets + elicitation

## Style is a composite, not a dropdown

The corpus research is explicit: **"give me a McKinsey-style report" is too ambiguous.**
A good style is *composed*, and most of it is already fixed the moment you know the
Design Read:

> **Style = Audience + Purpose + Format + Reasoning + Tone + Density + Visual**

You derive six of the seven from the brief (`constants.md` gives the measured density,
hierarchy, archetypes, and title style per audience/purpose). The only genuinely free
choice left is the **visual preset** — surface color and type character. So don't open
with "what style do you want?"; declare what you already know, then ask only the gap.

## The elicitation (one round, not five screens)

The research designed a five-step builder (do-what → for-whom → about-what → consume-how
→ reason-how). Collapse it: **infer everything you can from the prompt and any brand
files, state a one-line Design Read, then ask at most one `AskUserQuestion` round for
only the unknowns.** If the user already gave audience, purpose, format, and a brand/style,
ask nothing — just declare the read and build.

**Design Read (always state it, one line):**
> "Reading this as: a `<format>` for `<audience>`, purpose `<purpose>`, `<preset>` look."

**Ask only the gaps.** Typical questions when unknown:
- **Audience + purpose** — Board / C-level / BU-head / Functional-leader × monitor /
  diagnose / decide / align / persuade. (Drives density, hierarchy, archetypes, titles.)
- **Format** — Slide deck (HTML/PPTX) · Report (HTML scroll) · Print (Typst).
- **Look** — Editorial / Keynote / Consulting, and light or dark.

Never ask more than one round. If the user pushes back or is vague, pick the recommended
default and say what you chose so they can correct it.

## Three visual presets

Presets are token overrides pasted into the shell's `:root` (and mirrored into the two
dark blocks — see the shell header). They change surface color and type character only;
the measured layout rules never change. `Consulting` is the shell default, so it needs no
override.

### Consulting (default) — tight grid, navy accent, tabular
Best for `monitor` / `diagnose` / `decide` and any data-dense management report. Already
in the shell:
```css
--accent:#17427A; --accent-soft:#DCE5F1; --accent-2:#8A5D0E; --accent-2-soft:#F0E6D0;
/* headings serif; sans body; paper #F6F7F9 */
```

### Editorial — serif headers, warm neutral, single accent
Best for `align` and narrative reports for functional leaders.
```css
--paper:#F7F4EE; --surface:#FFFFFF; --raised:#EFEAE0;
--ink:#1E1B16; --body:#33302A; --muted:#6B6459; --line:#E2DACC;
--accent:#8A5A2B; --accent-soft:#F0E7DA; --accent-2:#3A5A78; --accent-2-soft:#DEE7EF;
/* dark accent: --accent:#D9A45E --accent-soft:#33261410 */
```
Optional font upgrade (artifact only): `--serif:"Source Serif 4",Georgia,serif` via a
Google Fonts link; keep the system fallback for offline render.

### Keynote — big type, high contrast, dark-capable
Best for `persuade` and board pitches; pairs well with dark mode.
```css
--paper:#FFFFFF; --surface:#FFFFFF; --raised:#F0F2F6;
--ink:#0B0D12; --body:#20242E; --muted:#5A6170; --line:#DCE0E8;
--accent:#1E63D6; --accent-soft:#DCE7FB; --accent-2:#0FA37F; --accent-2-soft:#D6F1E8;
/* headings use the sans stack, not serif: */
h1,h2,h3{font-family:var(--sans); letter-spacing:-.02em}
```
On a deck, Keynote is the natural fit for the larger 16:9 type scale (`deck.html` runs a
higher headline ratio than the report shell — corpus landscape reports measure up to 3.1).

## Brand override

If the user supplies a brand guideline (colors, fonts, logo), it **overrides the preset
tokens**: map their primary to `--accent`, their secondary to `--accent-2`, set the
heading/body font stacks, and drop the logo into the cover/title. Keep the measured layout
and the 1.9 hierarchy floor regardless of what the brand doc says about type sizes — a
brand palette is an input, not a redesign of the tiering.

## Anti-default discipline

Most machine-made decks look generic because the model reaches for the same defaults.
Do not, unless the brief specifically calls for them:

- AI-purple/indigo gradients; a centered hero over a dark mesh.
- Three identical feature cards as the answer to every "list of things".
- Glassmorphism on everything; drop shadows on flat content.
- Emoji as bullet markers; `01/02/03` numbering when the content has no real order.
- A rainbow of series colors when there are only two series.

Reach past these deliberately, guided by the archetype's measured constants and the
"clever moves" in `archetypes.md`.
