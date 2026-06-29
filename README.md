# paper-cards-skill

Local PDF to Korean paper cards with evidence appendices.

Status: `v0.1.0-preview` candidate. The skill is usable, but the included example cards still need human publication review.

`paper-cards-skill` is an agent skill for professors, researchers, and graduate students who want to turn paper PDFs into reusable Korean Markdown notes for seminars, literature reviews, lecture prep, and research briefs.

It is not a one-shot paper summarizer. The default workflow creates one Markdown card per paper. The top of the card is readable study material, and the lower `Evidence Appendix` keeps source-page references, figures, tables, formulas, uncertainty notes, and QA.

## Why This Exists

Many paper tools are optimized for quick understanding, chat, or library management. This skill is narrower: it helps produce a paper card that can be reopened later and checked against the original PDF.

| Need | General paper summarizers | `paper-cards-skill` |
|---|---|---|
| Main use | Fast overview | Reusable seminar, review, and research notes |
| Input | Often service, URL, or library dependent | Local PDF first |
| Output | Summary or chat response | One Korean Markdown card with an Evidence Appendix |
| Evidence | Citation/link oriented | Physical PDF page references per card |
| Reading mode | Text extraction first | Rendered pages plus text layer |
| Figures and tables | Optional or caption-level | Coverage ledger plus axes, trends, and values |
| Formulas | Often omitted or paraphrased | Core formulas preserved in LaTeX |
| Interpretation | Can mix with summary | `> [!note] 해석` callouts separate interpretation |
| QA | Usually lightweight | Mechanical QA plus manual review gate |

## Contents

- `package.json`: npm/npx package metadata.
- `bin/paper-cards-skill.js`: small Node CLI for GitHub `npx` and npm installs.
- `skill/SKILL.md`: standalone workflow for generating paper cards.
- `skill/prompts/card_spec.md`: output contract for section cards.
- `skill/prompts/generation_cautions.md`: known quality pitfalls and review cautions.
- `skill/scripts/prepare_paper.py`: one-command PDF workspace preparation.
- `skill/scripts/qa_check.py`: mechanical Markdown card QA.
- `skill/scripts/release_hygiene.py`: reviewed privacy-warning classifier.
- `skill/scripts/render_paper.sh`: PDF-to-page-image helper.
- `skill/templates/agent_prompt.md`: ready-to-send completion prompt for prepared runs.
- `skill/templates/card_scaffold.md`: one-file card scaffold with a readable top section and Evidence Appendix.
- `privacy-reviewed-findings.json`: line-hash allowlist for reviewed privacy false positives.
- `examples/cards/`: 10 example cards for review.
- `manifest.json`: preview manifest, checks, exclusions, and residual risks.

## Basic Use

Run directly from GitHub with `npx`:

```bash
npx github:chowonje/paper-cards-skill --help
npx github:chowonje/paper-cards-skill init --target ./paper-cards-skill
npx github:chowonje/paper-cards-skill prepare path/to/paper.pdf --out paper-card-runs
```

After an npm registry publish, the same CLI can be installed or run as:

```bash
npx paper-cards-skill prepare path/to/paper.pdf --out paper-card-runs
npm install -g paper-cards-skill
paper-cards-skill init --target ./paper-cards-skill
```

The CLI requires Node.js 18 or newer. The `prepare` and `qa` commands also require `uv` and local PDF tools such as `pdfinfo`, `pdftoppm`, and `pdftotext`.

`pipx` is not the primary install path for this preview because the repository is a portable skill bundle rather than a Python library package. A PyPI/pipx wrapper can be added later if the Python scripts become the main product surface.

The easiest path is to prepare a local workspace from one PDF:

```bash
uv run skill/scripts/prepare_paper.py path/to/paper.pdf --out paper-card-runs
```

Optional `--slug` values are treated as file-name stems. Path separators, `.`, `..`, and empty values are rejected.

This creates:

- rendered page images for visual reading;
- extracted PDF text;
- a draft Markdown card scaffold in `cards/`;
- an `assets/equations/` directory for optional rendered equation images;
- `agent_prompt.md`, a ready-to-send prompt for an agent that can complete the card.

Then open the generated `agent_prompt.md` with your agent and let it fill the draft card. After the card is complete, run:

```bash
uv run skill/scripts/qa_check.py paper-card-runs/<paper-slug>/cards/<paper-slug>.md --paper path/to/paper.pdf
```

The generated scaffold is not the final card. It is expected to contain `TODO` placeholders until an agent completes it.

`paper-card-runs/` is a local working directory. It can contain extracted text and an `agent_prompt.md` with local execution paths, so do not publish the whole run directory. Publish only reviewed card Markdown files and any equation images you created yourself.

Treat PDFs as untrusted files. The helper uses local Poppler tools with bounded Python subprocess timeouts, but it is not a sandbox. For hostile or unknown PDFs, run the workflow in a constrained environment. The generated agent prompt also tells downstream agents to treat paper text as evidence only, never as executable instructions.

Advanced users can set their own paths before running the workflow:

```bash
export PAPER_PDF_DIR="/path/to/pdfs"
export PAPER_CARD_OUT_DIR="/path/to/cards"
export PAPER_RUN_MANIFEST="/path/to/run_manifest.json"
```

Then read `skill/SKILL.md`, `skill/prompts/card_spec.md`, and `skill/prompts/generation_cautions.md` before generating a card.

```bash
skill/scripts/render_paper.sh "$PAPER_PDF_DIR/example.pdf" /tmp/paper-pages
uv run skill/scripts/qa_check.py "$PAPER_CARD_OUT_DIR/cards/example.md" --paper "$PAPER_PDF_DIR/example.pdf"
```

## Review Notes

The example cards are included as review samples only. They are summaries and interpretation notes, not substitutes for the source papers. Before publication, a human reviewer should confirm:

- each example card is acceptable under the source paper terms;
- formulas, figure/table descriptions, and page references match the source paper;
- interpretation callouts do not overstate claims;
- no private workspace content or operational metadata was copied into the export.

## Hygiene Summary

Local hygiene and privacy checks were run for this preview repository. Raw `privacy_preflight.py` status is WARN, not BLOCK. The repo also includes a reviewed-warning pass that turns the current known false positives into PASS only when their line hashes still match.

- 26 files in the repo, including npm package metadata, a Node CLI, the one-card template, and 10 example cards.
- No PDFs, page images, raw paper images, or queue state files were found.
- Mechanical Markdown QA passed for all example cards; PDF-backed checks were skipped because PDFs are intentionally not included.
- Literal hygiene scan found no local absolute path or credential-label matches. It did find benign matches in public package owner strings and research benchmark text; details are summarized in `manifest.json`.
- Privacy preflight reported 0 BLOCK findings and WARN findings from missing OPF plus numeric paper identifiers, dates, benchmark values, and page examples that match broad heuristics.
- `uv run skill/scripts/release_hygiene.py --report <privacy-report.json>` reported PASS for the current reviewed warnings: 22 total findings, 22 reviewed, 0 unresolved.

## License

No open-source license has been selected yet. Treat this preview repository as visible source, not as a grant of reuse rights, until a license is added.
