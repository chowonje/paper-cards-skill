# Korean Paper Section Card Specification

Generate an Obsidian-compatible Markdown card in Korean from a local research paper PDF.

## Frontmatter

Every card starts with YAML frontmatter:

```yaml
---
title: "<exact paper title>"
authors: ["Author One", "Author Two"]
year: 2024
source: "<venue, journal, arXiv, or version information confirmed in the PDF>"
tags: [paper-card, topic-tag]
---
```

Only put source information in `source` when it is confirmed inside the PDF. Put outside publication context in a note callout instead.

## Required Structure

1. `# 논문 전체 요약`
   - One paragraph summarizing the whole paper.
   - End with the physical PDF page reference.
2. Operational blocks:
   - `### TL;DR`
   - `### Why it matters`
   - `### When to cite`
   - `### Do not overclaim`
   - `### Limitations / Failure modes / Not settled by this paper`
3. One `##` section for each top-level paper section.
   - Do not promote subsections such as `2.1` to `##` unless the paper itself has unusual top-level numbering.
   - Keep subsection details inside the parent section card.
4. Final `## 그림·표 커버리지` ledger.

## Section Card Body

Each `##` section must contain:

- `**핵심 주장**`: up to three bullets.
- `**근거·데이터 요약**`: experiments, methods, comparisons, and key numbers.
- Figure/table descriptions when relevant.
- Required formulas in LaTeX.
- `**원문 페이지**: pdf p.X-Y` at the end.

If printed page numbers differ, write:

`**원문 페이지**: pdf p.2-4 (printed p.1189-1191)`

Do not use printed page numbers alone.

## Figure And Table Rules

- Describe all figures and tables that matter to the paper's argument.
- For graphs, include axis meaning, range, trend, and representative values when readable.
- For tables, preserve the comparison structure. Rows may be summarized, but do not remove all competing baselines or comparison columns.
- For multi-panel figures, copy panel labels from the figure itself.
- For diagrams, describe components and connections in order.
- If a figure is qualitative, state that no numeric axis is present and summarize the structure.
- End with a coverage ledger listing source figures/tables and described figures/tables.

## Formula Rules

- Preserve core formulas in LaTeX.
- Include hyperparameters needed to understand the method.
- Do not replace formulas with prose when the equation is central to the paper.

## Claim And Interpretation Separation

Main prose should state the authors' claims and results. Your interpretation, historical context, or external caveat must be separated:

```markdown
> [!note] 해석
> <interpretation; clearly distinguish it from the paper's own claim>
```

Use at most one interpretation callout per section. Do not force a callout when none is needed.

## Public-Export Constraints

- Do not embed paper PDFs, page images, or original figure images.
- Do not paste long source excerpts.
- Prefer paraphrase, compact tables, formulas, and page-grounded citations.
- Mark uncertain OCR or visual readings as uncertain and re-render at higher DPI when possible.
