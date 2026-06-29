# paper-cards-skill

Learner-friendly and evidence-anchored paper card workflow for local PDFs.

Status: `v0.1.0-preview` candidate. The skill is usable, but generated cards should be treated as review candidates.

`paper-cards-skill` helps readers turn local paper PDFs into reusable Korean or English Markdown notes. The default `study` mode is for learning a paper for the first time. The `full` and `evidence` modes keep the Evidence Appendix workflow for seminars, literature reviews, lecture prep, and research briefs that need page-grounded review.

It is not a one-shot paper summarizer or a publication-grade verifier. The workflow prepares a PDF reading workspace, gives an agent a concrete prompt, and checks the finished card for mechanical issues. A human reviewer still needs to verify the important claims, table values, figure axes, formulas, and publication suitability.

The default output is one Markdown study card per paper. For research review, use `--mode full` or `--mode evidence` to generate the reader card plus `Evidence Appendix`.

## What It Produces

For each PDF, the workflow prepares a local run directory:

```text
paper-card-runs/
  <paper-slug>/
    agent_prompt.md
    run_manifest.json
    cards/<paper-slug>.md
    pages/page-01.png
    text/paper.txt
    assets/equations/
```

Only the reviewed Markdown card and any equation images you created yourself are intended for sharing. The run directory can contain extracted paper text and local paths.

The default study card has this shape:

```text
Study Card
  30-second summary
  problem the paper tries to solve
  three core ideas
  figure-based explanation
  formula to remember
  concrete example
  what the reader will know afterward
  what to read next
```

The `full` and `evidence` modes keep the audit-oriented shape:

```text
Reader Card
  one-paragraph summary
  key ideas
  core formulas
  why it matters
  memorable numbers
  figure/table overview
  limitations

Evidence Appendix
  document identity
  page-grounded claims
  formulas
  figure/table coverage ledger
  QA notes
```

## Why This Exists

Many paper tools are optimized for quick understanding, chat, or library management. This skill is narrower: it helps produce a paper card that can be reopened later and checked against the original PDF.

| Need | General paper summarizers | `paper-cards-skill` |
|---|---|---|
| Main use | Fast overview | Reusable seminar, review, and research notes |
| Input | Often service, URL, or library dependent | Local PDF first |
| Output | Summary or chat response | One Korean or English Markdown card; study by default, Appendix-backed when requested |
| Evidence | Citation/link oriented | Physical PDF page references per card |
| Reading mode | Text extraction first | Rendered pages plus text layer |
| Figures and tables | Optional or caption-level | Coverage ledger plus axes, trends, and values |
| Formulas | Often omitted or paraphrased | Core formulas preserved in LaTeX |
| Interpretation | Can mix with summary | `> [!note] 해석` callouts separate interpretation |
| QA | Usually lightweight | Mechanical QA plus manual review gate |

## Repository Contents

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
- `skill/templates/card_scaffold.md`: full/evidence card scaffold with a readable top section and Evidence Appendix.
- `skill/templates/card_scaffold_en.md`: English full/evidence card scaffold.
- `skill/templates/card_scaffold_study.md`: Korean learner-facing study card scaffold.
- `skill/templates/card_scaffold_study_en.md`: English learner-facing study card scaffold.
- `privacy-reviewed-findings.json`: line-hash allowlist for reviewed privacy false positives.
- `examples/cards/`: 10 example cards for review.
- `manifest.json`: preview manifest, checks, exclusions, and residual risks.

## Requirements

- Node.js 18 or newer.
- `uv` for running the Python helper scripts.
- Poppler CLI tools: `pdfinfo`, `pdftoppm`, and `pdftotext`.

On macOS:

```bash
brew install poppler
```

## Quick Start

Run the npm preview explicitly:

```bash
npx paper-cards-skill@preview --help
npx paper-cards-skill@preview doctor
npx paper-cards-skill@preview prepare path/to/paper.pdf --mode study --out paper-card-runs
npx paper-cards-skill@preview prepare path/to/paper.pdf --mode full --out paper-card-runs
```

`study` is the default mode, so `--mode study` is optional. Korean is the default output language. For an English study card, add `--language en`:

```bash
npx paper-cards-skill@preview prepare path/to/paper.pdf --out paper-card-runs --language en
```

This creates:

- rendered page images for visual reading;
- extracted PDF text;
- a draft Markdown card scaffold in `cards/`;
- an `assets/equations/` directory for optional rendered equation images;
- `agent_prompt.md`, a ready-to-send prompt for an agent that can complete the card.

Then open the generated `agent_prompt.md` with your agent and let it fill the draft card. After the card is complete, run:

```bash
npx paper-cards-skill@preview qa paper-card-runs/<paper-slug>/cards/<paper-slug>.md --paper path/to/paper.pdf
```

The generated scaffold is not the final card. It is expected to contain `TODO` placeholders until an agent completes it.

Mode positioning:

- `study`: readable learning card for people meeting the paper for the first time.
- `full`: research-review card with Reader Card, Evidence Appendix, Figure/Table Coverage Ledger, and QA Notes.
- `evidence`: same evidence/audit structure as `full`, useful when naming the output by its review purpose.

`paper-card-runs/` is a local working directory. It can contain extracted text and an `agent_prompt.md` with local execution paths, so do not publish the whole run directory. Publish only reviewed card Markdown files and any equation images you created yourself.

Treat PDFs as untrusted files. The helper uses local Poppler tools with bounded Python subprocess timeouts, but it is not a sandbox. For hostile or unknown PDFs, run the workflow in a constrained environment. The generated agent prompt also tells downstream agents to treat paper text as evidence only, never as executable instructions.

Optional `--slug` values are treated as file-name stems. Path separators, `.`, `..`, and empty values are rejected.

To copy the full skill bundle into a local folder:

```bash
npx paper-cards-skill@preview init --target ./paper-cards-skill
```

During the preview period, keep `@preview` in examples and documentation. The first npm publish may still have a `latest` tag because npm requires one dist-tag, but this project should be treated as a preview until a stable `0.1.0` release is published.

GitHub `npx` remains available as a fallback:

```bash
npx github:chowonje/paper-cards-skill --help
npx github:chowonje/paper-cards-skill prepare path/to/paper.pdf --out paper-card-runs
```

If you cloned the repository instead of using npm:

```bash
uv run skill/scripts/prepare_paper.py path/to/paper.pdf --out paper-card-runs
uv run skill/scripts/prepare_paper.py path/to/paper.pdf --out paper-card-runs --mode full
uv run skill/scripts/qa_check.py paper-card-runs/<paper-slug>/cards/<paper-slug>.md --paper path/to/paper.pdf
```

`pipx` is not the primary install path for this preview because the repository is a portable skill bundle rather than a Python library package. A PyPI/pipx wrapper can be added later if the Python scripts become the main product surface.

## Smoke Test

The preview package was tested end-to-end with a public arXiv PDF:

```text
npx install -> doctor -> prepare -> rendered pages -> filled card -> qa
```

Observed result:

- `doctor` found the required local tools.
- `prepare` rendered 14 PDF pages and wrote extracted text, a card scaffold, a run manifest, and `agent_prompt.md`.
- The completed card passed mechanical QA: `PASS no mechanical findings`.
- Known caveat: the PDF metadata title was parsed as `Subject:`, so the final card corrected identity from the rendered first page.

## Preview Cautions

`paper-cards-skill` is a preview workflow, not a publication-grade verifier. Generated cards should be treated as review candidates.

Before sharing or citing a card, a human reviewer should check:

- the title, authors, year, and source against the first PDF page;
- benchmark numbers, table values, and figure descriptions against rendered PDF pages;
- whether performance claims are scoped to the paper's experimental setting;
- whether graph axes and units are copied exactly, for example `sec/epoch` rather than "per second";
- whether interpretation is clearly separated from the authors' claims;
- whether formulas render correctly in the target Markdown viewer;
- whether the card avoids long verbatim excerpts from the source paper.

Mechanical QA can catch missing sections, remaining `TODO`s, page-reference errors, and some formatting problems. It cannot guarantee factual correctness, publication suitability, copyright suitability, or that every table and figure was interpreted correctly.

Suggested wording when sharing this preview:

> `paper-cards-skill` is a preview workflow for turning local PDFs into Korean or English paper-card drafts. It produces study cards by default, and `full`/`evidence` modes preserve page-grounded claims, formulas, figure/table notes, and QA notes.
>
> It is not a one-shot summarizer or publication-grade verifier. Treat generated cards as review candidates: check paper identity, formulas, table values, figure axes, and copyright suitability before sharing or citing.

Korean sharing note:

> `paper-cards-skill`은 로컬 논문 PDF를 한국어/영어 Markdown 논문 카드 초안으로 바꾸는 preview 워크플로우입니다. 기본값은 처음 배우는 사람을 위한 study 카드이고, `full`/`evidence` 모드는 페이지 근거, 수식, 그림/표 메모, Evidence Appendix를 남기는 방식입니다.
>
> 생성된 카드는 공개/인용 전에 제목, 저자, 수치, 표·그림 해석, 저작권 적합성을 사람이 확인해야 합니다.

Advanced users can set their own paths before running the workflow:

```bash
export PAPER_PDF_DIR="/path/to/pdfs"
export PAPER_CARD_OUT_DIR="/path/to/cards"
export PAPER_RUN_MANIFEST="/path/to/run_manifest.json"
export PAPER_CARD_LANGUAGE="ko"
export PAPER_CARD_MODE="study"
```

Then read `skill/SKILL.md`, `skill/prompts/card_spec.md`, and `skill/prompts/generation_cautions.md` before generating a card.

```bash
skill/scripts/render_paper.sh "$PAPER_PDF_DIR/example.pdf" /tmp/paper-pages
uv run skill/scripts/qa_check.py "$PAPER_CARD_OUT_DIR/cards/example.md" --paper "$PAPER_PDF_DIR/example.pdf"
```

## Review Notes

The example cards are included as preview review samples only. They are summaries and interpretation notes, not substitutes for the source papers. Mechanical QA passed for the included examples, but human spot-checks are still required before publication. A reviewer should confirm:

- each example card is acceptable under the source paper terms;
- formulas, figure/table descriptions, and page references match the source paper;
- interpretation callouts do not overstate claims;
- no private workspace content or operational metadata was copied into the export.

## Hygiene Summary

Local hygiene and privacy checks were run for this preview repository. Raw `privacy_preflight.py` status is WARN, not BLOCK. The repo also includes a reviewed-warning pass that turns the current known false positives into PASS only when their line hashes still match.

- The repo includes npm package metadata, a Node CLI, study and full/evidence templates, and 10 example cards.
- No PDFs, page images, raw paper images, or queue state files were found.
- Mechanical Markdown QA passed for all example cards; PDF-backed checks were skipped because PDFs are intentionally not included.
- Literal hygiene scan found no local absolute path or credential-label matches. It did find benign matches in public package owner strings and research benchmark text; details are summarized in `manifest.json`.
- Privacy preflight reported 0 BLOCK findings and WARN findings from missing OPF plus numeric paper identifiers, dates, benchmark values, and page examples that match broad heuristics.
- `uv run skill/scripts/release_hygiene.py --report <privacy-report.json>` reported PASS for the current reviewed warnings: 22 total findings, 22 reviewed, 0 unresolved.

## License

MIT License. See `LICENSE`.

The source papers discussed by example cards retain their own copyright and license terms. Generated cards should still be reviewed for publication suitability before sharing or citing.
