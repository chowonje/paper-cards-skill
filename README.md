# paper-cards-skill

Turn a local paper PDF into a Korean or English Markdown paper card.

`paper-cards-skill` is a preview workflow for people who read papers and want notes they can review later. It is not a one-click truth machine. It prepares a local PDF workspace, asks an agent to write the card with a clear contract, then checks the finished Markdown for common mechanical problems.

Default output is a **study card** for learning a paper. Use `full` or `evidence` mode when you want a more detailed card with page-grounded evidence.

## Quick Start

Requirements:

- Node.js 18+
- `uv`
- Poppler tools: `pdfinfo`, `pdftoppm`, `pdftotext`

On macOS:

```bash
brew install poppler
```

Check your setup:

```bash
npx paper-cards-skill@preview doctor
```

Prepare a paper:

```bash
npx paper-cards-skill@preview prepare path/to/paper.pdf --out paper-card-runs
```

This creates a local run folder:

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

Open `agent_prompt.md` with an agent that can read local files, then let it complete the draft card in `cards/`.

After the card is complete:

```bash
npx paper-cards-skill@preview qa paper-card-runs/<paper-slug>/cards/<paper-slug>.md --paper path/to/paper.pdf
```

## Output Modes

### Study Mode

Default mode:

```bash
npx paper-cards-skill@preview prepare path/to/paper.pdf --out paper-card-runs
```

Best for:

- first-time learning
- Obsidian notes
- study groups
- quick review before reading the full paper

Card shape:

```text
30-second summary
problem the paper tries to solve
three core ideas
figure-based explanation
formula to remember
concrete example
what you will know after reading
what to read next
```

### Full / Evidence Mode

For review-heavy notes:

```bash
npx paper-cards-skill@preview prepare path/to/paper.pdf --mode full --out paper-card-runs
```

Best for:

- seminar prep
- literature review
- lecture prep
- checking claims against the PDF later

Card shape:

```text
Reader Card
Evidence Appendix
page-grounded claims
formulas
figure/table coverage ledger
QA notes
```

## Language

Korean is the default.

For English:

```bash
npx paper-cards-skill@preview prepare path/to/paper.pdf --language en --out paper-card-runs
```

You can combine language and mode:

```bash
npx paper-cards-skill@preview prepare path/to/paper.pdf --language en --mode full --out paper-card-runs
```

## What Makes It Different

Most paper tools focus on fast summaries. This workflow focuses on notes that remain checkable.

- Local PDF first
- Markdown output
- Korean or English cards
- PDF page references
- rendered page images for visual checking
- formulas preserved in LaTeX
- figure/table notes in evidence mode
- interpretation separated from author claims
- mechanical QA before sharing

## What Not To Publish

Do not publish the whole `paper-card-runs/` folder. It can contain extracted paper text, rendered pages, and local paths.

Publish only:

- reviewed Markdown cards
- equation images you created yourself, if any

Do not publish:

- source PDFs
- rendered page images
- raw paper figures or tables
- queue files
- local run manifests with private paths
- unreviewed generated cards

## Preview Warning

This is a preview package. Generated cards are **review candidates**.

Before sharing or citing a card, check:

- title, authors, year, and source
- important numbers and table values
- figure axes and units
- formulas
- whether claims are scoped to the paper's experiment
- whether interpretation is separate from the paper's claims
- copyright/publication suitability

Mechanical QA can catch missing sections, remaining `TODO`s, some page-reference problems, and formatting issues. It cannot prove that a card is factually correct or legally safe to publish.

## Claude Code / Codex Use

The npm CLI works from Claude Code, Codex, or any local terminal:

```bash
npx paper-cards-skill@preview prepare path/to/paper.pdf --out paper-card-runs
```

The actual skill instructions live in:

```text
skill/SKILL.md
skill/prompts/card_spec.md
skill/prompts/generation_cautions.md
```

If your agent supports custom skills, copy the `skill/` folder into that agent's skill location.

## Local Install

Copy the skill bundle into a folder:

```bash
npx paper-cards-skill@preview init --target ./paper-cards-skill
```

Or clone this repository and run the scripts directly:

```bash
uv run skill/scripts/prepare_paper.py path/to/paper.pdf --out paper-card-runs
uv run skill/scripts/qa_check.py paper-card-runs/<paper-slug>/cards/<paper-slug>.md --paper path/to/paper.pdf
```

## Repository Contents

- `bin/paper-cards-skill.js`: npm/npx CLI
- `skill/SKILL.md`: paper-card workflow
- `skill/prompts/`: card rules and generation cautions
- `skill/scripts/`: prepare, render, QA, and release hygiene helpers
- `skill/templates/`: Korean and English card scaffolds
- `examples/cards/`: public preview example cards
- `manifest.json`: preview export manifest and residual risks
- `privacy-reviewed-findings.json`: reviewed privacy false-positive records

## Security And Privacy Status

Current preview checks found no blocking security or privacy issue for GitHub/npm sharing.

Known WARN items:

- OPF was not installed, so model-based PII scanning was not run.
- Some paper years, page numbers, and table values can look like phone numbers to simple heuristics.
- Example cards still need human review before being treated as final public examples.
- Untrusted PDFs should be processed in a constrained local environment because Poppler parses the file.

## License

MIT License. See `LICENSE`.

The source papers discussed by example cards keep their own copyright and license terms.
