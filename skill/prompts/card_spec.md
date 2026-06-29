# Paper Card Specification

Generate one Obsidian-compatible Markdown card from a local research paper PDF.

The prepared run selects one output mode:

- `study`: a learner-facing card for people meeting the paper for the first time.
- `full`: a readable reader card plus Evidence Appendix for research review.
- `evidence`: the same Appendix-backed review structure as `full`, named for audit-oriented workflows.

## Output Language

The card language is selected during preparation:

- `ko`: Korean reader card and Korean appendix labels.
- `en`: English reader card and English appendix labels.

Use the selected language consistently. Keep paper titles, author names, venues, formulas, model names, dataset names, and quoted labels in their original language when that is more accurate.

## Output Mode

`study` is the default. Use it when the reader needs to understand the paper before auditing every claim. It should be easier to read than a research review card and should not include an Evidence Appendix.

Use `full` or `evidence` when the card must support review, seminar prep, or citation decisions with page-grounded evidence, figure/table coverage, formulas, and QA notes.

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

## Required Study Structure

Korean study card:

1. `# <paper title>`
2. `## 30초 요약`
3. `## 이 논문이 풀려는 문제`
4. `## 핵심 아이디어 3개`
5. `## 그림으로 이해하기`
6. `## 꼭 기억할 수식`
7. `## 예시로 이해하기`
8. `## 이 논문을 읽고 나면 알게 되는 것`
9. `## 다음에 읽으면 좋은 것`

English study card:

1. `# <paper title>`
2. `## 30-Second Summary`
3. `## Problem This Paper Tries To Solve`
4. `## Three Core Ideas`
5. `## Understand It With Figures`
6. `## Formula To Remember`
7. `## Understand It By Example`
8. `## What You Will Know After Reading`
9. `## What To Read Next`

## Required Full/Evidence Structure

Korean card:

1. `# <paper title>`
2. Reader Card marker text
3. `## 한 문단 요약`
4. `## 핵심 아이디어`
5. `## 수식으로 보는 핵심`
6. `## 왜 중요한가`
7. `## 기억할 수치`
8. `## 그림·표 한눈에 보기`
9. `## 한계와 조심할 점`
10. `# Evidence Appendix`
11. `## 문서 신원`
12. `## 핵심 주장별 근거`
13. `## 수식 근거`
14. `## 그림·표 근거`
15. `## QA 메모`

English card:

1. `# <paper title>`
2. Reader Card marker text
3. `## One-Paragraph Summary`
4. `## Key Ideas`
5. `## Core Formula`
6. `## Why It Matters`
7. `## Memorable Numbers`
8. `## Figure/Table At a Glance`
9. `## Limitations And Cautions`
10. `# Evidence Appendix`
11. `## Document Identity`
12. `## Evidence By Claim`
13. `## Formula Evidence`
14. `## Figure/Table Evidence`
15. `## QA Notes`

## Study Mode Rules

- Explain the problem before the method.
- Prefer concrete examples, analogies, and compact bullets over section-by-section audit notes.
- Before a central formula, define the few technical terms a first-time reader needs.
- Limit figure/table discussion to what helps the learner understand the idea.
- Include only the formulas a learner must remember. If formulas are not central, say that clearly.
- Do not add `# Evidence Appendix` in `study` mode.
- Do not paste long source excerpts.

## Readable Top Section Rules For Full/Evidence Modes

- Prefer compact prose and bullets over long section-by-section reports.
- Keep figure/table notes to the reader-facing point: what the visual shows and why it matters.
- Do not paste long raw LaTeX inside prose.
- If a formula is central and visually hard to read inline, use block math or a small self-created equation image.
- Do not include full PDF pages, original paper figures, or long source excerpts.

## Evidence Appendix Rules For Full/Evidence Modes

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
