# Paper Card Specification

Generate one Obsidian-compatible Markdown card from a local research paper PDF.

The card has two layers in one file:

- readable top sections for study, seminars, and literature review;
- `# Evidence Appendix` for page-grounded verification, figures, tables, formulas, uncertainty notes, and QA.

## Output Language

The card language is selected during preparation:

- `ko`: Korean reader card and Korean appendix labels.
- `en`: English reader card and English appendix labels.

Use the selected language consistently. Keep paper titles, author names, venues, formulas, model names, dataset names, and quoted labels in their original language when that is more accurate.

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

Korean card:

1. `# <paper title>`
2. `## 한 문단 요약`
3. `## 핵심 아이디어`
4. `## 수식으로 보는 핵심`
5. `## 왜 중요한가`
6. `## 기억할 수치`
7. `## 그림·표 한눈에 보기`
8. `## 한계와 조심할 점`
9. `# Evidence Appendix`
10. `## 문서 신원`
11. `## 핵심 주장별 근거`
12. `## 수식 근거`
13. `## 그림·표 근거`
14. `## QA 메모`

English card:

1. `# <paper title>`
2. `## One-Paragraph Summary`
3. `## Key Ideas`
4. `## Core Formula`
5. `## Why It Matters`
6. `## Memorable Numbers`
7. `## Figure/Table At a Glance`
8. `## Limitations And Cautions`
9. `# Evidence Appendix`
10. `## Document Identity`
11. `## Evidence By Claim`
12. `## Formula Evidence`
13. `## Figure/Table Evidence`
14. `## QA Notes`

## Readable Top Section Rules

- Prefer compact prose and bullets over long section-by-section reports.
- Keep figure/table notes to the reader-facing point: what the visual shows and why it matters.
- Do not paste long raw LaTeX inside prose.
- If a formula is central and visually hard to read inline, use block math or a small self-created equation image.
- Do not include full PDF pages, original paper figures, or long source excerpts.

## Evidence Appendix Rules

- Use physical PDF page numbers for every claim group.
- If printed page numbers differ, write both:

Korean:

`**원문 페이지**: pdf p.2-4 (printed p.1189-1191)`

English:

`**Source pages**: pdf p.2-4 (printed p.1189-1191)`

- Do not use printed page numbers alone.
- Preserve core formulas in LaTeX.
- Put interpretation only inside `> [!note] 해석` callouts.
- Mark OCR, table, or visual-reading uncertainty explicitly.

## Figure And Table Rules

In the readable top section:

- Mention only important figures/tables.
- Use one or two short sentences per item.
- Avoid table-value dumps.

In `# Evidence Appendix`:

- Describe all figures and tables that matter to the paper's argument.
- Keep a coverage ledger listing source figures/tables, PDF pages, whether they appear in the top section, and evidence status.
- For graphs, include axis meaning, range, trend, and representative values when readable.
- For tables, preserve the comparison structure. Rows may be summarized, but do not remove all competing baselines or comparison columns.
- For multi-panel figures, copy panel labels from the figure itself.
- For diagrams, describe components and connections in order.
- If a figure is qualitative, state that no numeric axis is present and summarize the structure.

## Formula Rules

- Preserve core formulas in LaTeX in `# Evidence Appendix`.
- Include hyperparameters needed to understand the method.
- Do not replace formulas with prose when the equation is central to the paper.
- In the readable top section, avoid long inline math. Use block math or a self-created equation image when readability is better.
- Do not copy original paper equation images. If an image is needed, create a fresh rendering from the LaTeX you wrote.

## Claim And Interpretation Separation

Main prose should state the authors' claims and results. Your interpretation, historical context, or external caveat must be separated:

```markdown
> [!note] 해석
> <interpretation; clearly distinguish it from the paper's own claim>
```

English cards may use:

```markdown
> [!note] Interpretation
> <interpretation; clearly distinguish it from the paper's own claim>
```

Use interpretation callouts mainly in `# Evidence Appendix`. Do not force a callout when none is needed.

## Public-Export Constraints

- Do not embed paper PDFs, page images, or original figure images.
- Do not paste long source excerpts.
- Prefer paraphrase, compact tables, formulas, and page-grounded citations.
- Mark uncertain OCR or visual readings as uncertain and re-render at higher DPI when possible.
- Mark generated cards as review candidates until a human has spot-checked identity, key table values, figure axes/units, and performance-claim scope.
- Mechanical QA is required, but it does not prove factual correctness, publication suitability, copyright suitability, or visual interpretation quality.
