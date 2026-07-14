# Replication with Language Models — Workshop Slides

A talk on LLM-based replication in social science, synthesizing two papers: a
diagnostic tool for prompt stability, and an empirical audit of LLM
replication fragility over time. Closes with an appendix on the real
[`promptstability`](https://github.com/cjbarrie/promptstability) package
behind the diagnostic.

## View the slides

**[Open the slides](https://cjbarrie.github.io/llm_workshop_slides/)**
(served via GitHub Pages).

Press `S` to open speaker notes in a separate window. Use arrow keys or
click to advance through fragments.

**[Open the annotated version](https://cjbarrie.github.io/llm_workshop_slides/llm_workshop_slides_annotated.html)**
for a read-along layout — the deck on the left, that slide's speaker notes
permanently visible on the right, in the style of
[Arvind Narayanan's annotated-slides talks](https://www.cs.princeton.edu/~arvindn/talks/).
Same deck, same content; a separate file, not a replacement for the primary
one above.

## Re-rendering locally

Requires [Quarto](https://quarto.org):

```bash
quarto render llm_workshop_slides.qmd
python3 build_annotated.py   # regenerates the annotated variant from the rendered HTML
```

This regenerates `llm_workshop_slides.html`, which is self-contained
(`self-contained: true`) — all figures and styles are embedded, so it can be
opened directly or served as a static file with no other dependencies.
`build_annotated.py` then derives `llm_workshop_slides_annotated.html` from
it — a post-processing step (adds a narration sidebar via CSS/JS reusing the
existing `::: {.notes}` content), not a second content source, so re-run it
any time the primary deck changes.

## Files

- `llm_workshop_slides.qmd` — Quarto revealjs source
- `llm_workshop_slides.html` — rendered, self-contained slides (what GitHub Pages serves)
- `build_annotated.py` — generates the annotated (notes-sidebar) variant below
- `llm_workshop_slides_annotated.html` — generated; the deck with a persistent read-along notes panel
- `theme-template.scss` — NYU-branded slide theme
- `references.bib` — citations for both papers
- `figures/` — source images (real figure crops from both papers, the NYU logo, and a real `promptstability` output plot used in the appendix)
- `llmreplication.pdf`, `promptstability.pdf` — the two source papers
- `index.html` — redirects the repo's Pages root to the slides

## Appendix: the `promptstability` package

The closing slides walk through the actual package behind Paper 1's
diagnostic — installation, core API (`intra_pss`, `inter_pss`,
`manual_inter_pss`), and a real example run. See
[github.com/cjbarrie/promptstability](https://github.com/cjbarrie/promptstability)
and the [docs](https://promptstability.readthedocs.io) for full detail.
