---
name: paper-section-cards
description: Generate Korean section-level paper cards from user-supplied local PDFs, with document identity checks, page-grounded evidence, formula preservation, figure/table coverage, separated interpretation callouts, and a QA gate.
---

# Paper Section Cards

This skill converts a local paper PDF into a Korean Markdown card split by the paper's top-level sections. It is designed for reviewable research-note generation, not for canonical citation without human review.

## Inputs

The caller supplies all paths:

- `PAPER_PDF_DIR`: directory containing source PDFs.
- `PAPER_CARD_OUT_DIR`: directory where Markdown cards will be written.
- `PAPER_RUN_MANIFEST`: JSON or Markdown run record for selected papers, generated cards, QA status, and reviewer notes.
- Optional `PAPER_QUEUE_FILE`: a caller-owned queue file if batch processing is needed.

Do not assume any fixed home directory, workspace name, queue location, or output path.

## Non-Scope

- Do not download papers unless the caller explicitly makes that a separate task.
- Do not modify source PDFs.
- Do not include PDFs, rendered page images, raw paper figures, or long source excerpts in generated cards.
- Do not write into private note stores or unrelated workspace roots.
- Do not mark a card ready until the QA gate and manual review notes are recorded.

## Workflow

### 1. Read the Contracts

Before each batch, read:

- `prompts/card_spec.md`
- `prompts/generation_cautions.md`

For long batches, reread both files every five cards.

### 2. Select a Paper

Choose a PDF from the caller-provided manifest or queue. Record:

- PDF filename or stable identifier;
- expected title and authors, if known;
- intended output card filename;
- whether this is a first pass or a regeneration.

### 3. Render for Visual Reading

```bash
skill/scripts/render_paper.sh "$PAPER_PDF_DIR/<paper>.pdf" /tmp/paper-pages
```

Use a higher DPI for unclear tables or figures:

```bash
skill/scripts/render_paper.sh "$PAPER_PDF_DIR/<paper>.pdf" /tmp/paper-pages-hi 300 5 6
```

The rendered images are temporary reading aids. Do not copy them into the card export.

### 4. Verify Document Identity

Read the first page image and the first text page. Confirm that the title and authors match the target paper. Edition differences are acceptable when the same work is clearly identified.

If identity does not match, stop without writing a card and record `identity_mismatch` in the run manifest.

### 5. Read the Paper

- For papers up to 50 pages, read the relevant main text pages and all figure/table pages.
- For longer papers, read the full main text plus appendix or supplement pages that contain figures, tables, safety notes, system cards, or methods referenced by the main text.
- Use physical PDF page numbers for `원문 페이지`. If printed page numbers differ, write both.
- Cross-check hard-to-read table values with text extraction or higher-DPI rendering.

### 6. Write the Card

Follow `prompts/card_spec.md`.

Required qualities:

- frontmatter title, authors, year, source, tags;
- one whole-paper summary;
- one card per top-level paper section;
- source-page references at the end of each section card;
- all important formulas preserved in LaTeX;
- all figures and tables inventoried and described in text;
- interpretation only inside `> [!note] 해석` callouts;
- no long verbatim excerpts from the paper.

For long papers, write incrementally so partial work survives interruptions.

### 7. Run Mechanical QA

```bash
uv run skill/scripts/qa_check.py "$PAPER_CARD_OUT_DIR/<card>.md" --paper "$PAPER_PDF_DIR/<paper>.pdf"
```

If the PDF is not available during public review, run the Markdown-only subset:

```bash
uv run skill/scripts/qa_check.py "$PAPER_CARD_OUT_DIR/<card>.md"
```

Fix `FAIL` findings before treating a card as a candidate. `WARN` findings require a reviewer note.

### 8. Manual Review Gate

Before marking a card ready for sharing, check:

- identity was verified against the PDF;
- figure/table coverage is meaningful, not only a number list;
- formulas required to reconstruct the method are present;
- page references use PDF pages and are within range;
- interpretation callouts do not mix with author claims;
- the card does not reproduce long source passages.

Record PASS/WARN/BLOCK in `PAPER_RUN_MANIFEST`.

## Output

Report each card with:

- source identifier;
- output card path;
- page range read;
- QA command and result;
- manual review status;
- residual risks.
