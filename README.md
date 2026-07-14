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

## Re-rendering locally

Requires [Quarto](https://quarto.org):

```bash
quarto render llm_workshop_slides.qmd
```

This regenerates `llm_workshop_slides.html`, which is self-contained
(`self-contained: true`) — all figures and styles are embedded, so it can be
opened directly or served as a static file with no other dependencies.

## Files

- `llm_workshop_slides.qmd` — Quarto revealjs source
- `llm_workshop_slides.html` — rendered, self-contained slides (what GitHub Pages serves)
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
