# paper-cards-skill

Local PDF to reusable Korean research cards.

Status: `v0.1.0-preview` candidate. The skill is usable, but the included example cards still need human publication review.

`paper-cards-skill` is an agent skill for professors, researchers, and graduate students who want to turn paper PDFs into reusable Korean Markdown research cards for seminars, literature reviews, lecture prep, and research briefs.

It is not a one-shot paper summarizer. The workflow asks the agent to read a local PDF page by page, preserve source-page references, describe figures and tables, keep important formulas in LaTeX, and separate the paper authors' claims from the agent's own interpretation notes.

## Why This Exists

Many paper tools are optimized for quick understanding, chat, or library management. This skill is narrower: it helps produce a paper card that can be reopened later and checked against the original PDF.

| Need | General paper summarizers | `paper-cards-skill` |
|---|---|---|
| Main use | Fast overview | Reusable seminar, review, and research notes |
| Input | Often service, URL, or library dependent | Local PDF first |
| Output | Summary or chat response | Section-level Korean Markdown paper card |
| Evidence | Citation/link oriented | Physical PDF page references per card |
| Reading mode | Text extraction first | Rendered pages plus text layer |
| Figures and tables | Optional or caption-level | Coverage ledger plus axes, trends, and values |
| Formulas | Often omitted or paraphrased | Core formulas preserved in LaTeX |
| Interpretation | Can mix with summary | `> [!note] 해석` callouts separate interpretation |
| QA | Usually lightweight | Mechanical QA plus manual review gate |

## Contents

- `skill/SKILL.md`: standalone workflow for generating paper cards.
- `skill/prompts/card_spec.md`: output contract for section cards.
- `skill/prompts/generation_cautions.md`: known quality pitfalls and review cautions.
- `skill/scripts/qa_check.py`: mechanical Markdown card QA.
- `skill/scripts/render_paper.sh`: PDF-to-page-image helper.
- `examples/cards/`: 10 copied example cards for review.
- `manifest.json`: preview manifest, checks, exclusions, and residual risks.

## Basic Use

Set your own paths before running the workflow:

```bash
export PAPER_PDF_DIR="/path/to/pdfs"
export PAPER_CARD_OUT_DIR="/path/to/cards"
export PAPER_RUN_MANIFEST="/path/to/run_manifest.json"
```

Then read `skill/SKILL.md`, `skill/prompts/card_spec.md`, and `skill/prompts/generation_cautions.md` before generating a card.

```bash
skill/scripts/render_paper.sh "$PAPER_PDF_DIR/example.pdf" /tmp/paper-pages
uv run skill/scripts/qa_check.py "$PAPER_CARD_OUT_DIR/example-card.md" --paper "$PAPER_PDF_DIR/example.pdf"
```

## Review Notes

The example cards are included as review samples only. They are summaries and interpretation notes, not substitutes for the source papers. Before publication, a human reviewer should confirm:

- each example card is acceptable under the source paper terms;
- formulas, figure/table descriptions, and page references match the source paper;
- interpretation callouts do not overstate claims;
- no private workspace content or operational metadata was copied into the export.

## Hygiene Summary

Local hygiene and privacy checks were run before the initial GitHub publish. Current status is WARN, not BLOCK:

- 19 files in the repo, including 10 example cards.
- No PDFs, page images, raw paper images, or queue state files were found.
- Mechanical Markdown QA passed for all example cards; PDF-backed checks were skipped because PDFs are intentionally not included.
- Literal hygiene scan found no local path or credential-label matches. It did find benign research-term matches in example card text; details are summarized in `manifest.json`.
- Privacy preflight reported 0 BLOCK findings and WARN findings from missing OPF plus numeric paper identifiers, dates, benchmark values, and page examples that match broad heuristics.

## License

No open-source license has been selected yet. Treat this preview repository as visible source, not as a grant of reuse rights, until a license is added.
