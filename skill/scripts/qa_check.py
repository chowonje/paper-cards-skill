#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run qa_check.py path/to/card.md [--paper path/to/paper.pdf]
# 3. Or make executable and run:
#      chmod +x qa_check.py && ./qa_check.py path/to/card.md [--paper path/to/paper.pdf]
# ──────────────────

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

PAGE_REF_PATTERN: Final = re.compile(r"(?<!printed )(?<!인쇄 )p\.(\d{1,4})")
FRONTMATTER_PATTERN: Final = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
SUBSECTION_PATTERN: Final = re.compile(r"^## (\d+\.\d+[ .].*)$", re.MULTILINE)
FIGURE_PATTERN: Final = re.compile(r"(?:Figure|Fig\.)\s+(\d{1,2})\b")
TABLE_PATTERN: Final = re.compile(r"Table\s+(\d{1,2})\b")


@dataclass(frozen=True, slots=True)
class CheckResult:
    hard: tuple[str, ...]
    warn: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CliArgs:
    card_path: Path
    paper_path: Path | None


def parse_args(argv: list[str]) -> CliArgs:
    if len(argv) not in {2, 4}:
        print("usage: qa_check.py <card.md> [--paper <paper.pdf>]", file=sys.stderr)
        raise SystemExit(64)
    card_path = Path(argv[1])
    paper_path: Path | None = None
    if len(argv) == 4:
        if argv[2] != "--paper":
            print("usage: qa_check.py <card.md> [--paper <paper.pdf>]", file=sys.stderr)
            raise SystemExit(64)
        paper_path = Path(argv[3])
    return CliArgs(card_path=card_path, paper_path=paper_path)


def contiguous(numbers: set[int]) -> set[int]:
    found: set[int] = set()
    current = 1
    while current in numbers:
        found.add(current)
        current += 1
    return found


def run_text_command(command: list[str]) -> str | None:
    try:
        completed = subprocess.run(command, capture_output=True, check=False, text=True)
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def pdf_pages(pdf_path: Path) -> int | None:
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        return None
    output = run_text_command([pdfinfo, str(pdf_path)])
    if output is None:
        return None
    match = re.search(r"Pages:\s+(\d+)", output)
    if match is None:
        return None
    return int(match.group(1))


def pdf_fig_table_inventory(pdf_path: Path) -> tuple[set[int], set[int]] | None:
    pdftotext = shutil.which("pdftotext")
    if pdftotext is None:
        return None
    output = run_text_command([pdftotext, str(pdf_path), "-"])
    if output is None:
        return None
    figures = {int(match) for match in FIGURE_PATTERN.findall(output)}
    tables = {int(match) for match in TABLE_PATTERN.findall(output)}
    return contiguous(figures), contiguous(tables)


def check_frontmatter(text: str) -> tuple[str, ...]:
    failures: list[str] = []
    frontmatter = FRONTMATTER_PATTERN.match(text)
    if frontmatter is None:
        return ("H1 frontmatter missing",)
    for field in ("title:", "authors:", "year:", "source:", "tags:"):
        if field not in frontmatter.group(1):
            failures.append(f"H1 frontmatter field missing: {field}")
    return tuple(failures)


def check_sections(text: str) -> tuple[str, ...]:
    failures: list[str] = []
    if "# 논문 전체 요약" not in text:
        failures.append("H2 missing '# 논문 전체 요약'")
    for promoted in SUBSECTION_PATTERN.findall(text):
        failures.append(f"H3 subsection promoted to top-level card: ## {promoted[:40]}")
    sections = re.split(r"^## ", text, flags=re.MULTILINE)[1:]
    for section in sections:
        name = section.splitlines()[0][:40]
        if name.startswith("그림·표 커버리지"):
            continue
        if "원문 페이지" not in section:
            failures.append(f"H4 source page missing: ## {name}")
    if "그림·표 커버리지" not in text:
        failures.append("H6 missing figure/table coverage ledger")
    return tuple(failures)


def check_pdf_backed_rules(text: str, paper_path: Path | None) -> CheckResult:
    if paper_path is None:
        return CheckResult(hard=(), warn=("W0 PDF-backed checks skipped; no --paper supplied",))
    if not paper_path.exists():
        return CheckResult(hard=(f"H0 paper file missing: {paper_path}",), warn=())

    hard: list[str] = []
    warn: list[str] = []
    page_count = pdf_pages(paper_path)
    if page_count is None:
        warn.append("W0 pdfinfo unavailable or could not read page count")
    else:
        page_refs = [int(match) for match in PAGE_REF_PATTERN.findall(text)]
        over = sorted({page for page in page_refs if page > page_count})
        if over and "printed" not in text:
            hard.append(f"H5 page reference exceeds PDF page count {page_count}: {over[:5]}")
        elif over:
            warn.append(f"W2 page references exceed PDF count despite printed-page note: {over[:5]}")

    inventory = pdf_fig_table_inventory(paper_path)
    if inventory is None:
        warn.append("W0 pdftotext unavailable or could not read figure/table inventory")
    else:
        figures, tables = inventory
        missing_figures = [
            number for number in sorted(figures)
            if re.search(rf"(?:그림|Figure|Fig\.)\s*{number}\b", text) is None
        ]
        missing_tables = [
            number for number in sorted(tables)
            if re.search(rf"(?:표|Table)\s*{number}\b", text) is None
        ]
        if missing_figures:
            warn.append(f"W1 source figures not visible in card: {missing_figures}")
        if missing_tables:
            warn.append(f"W1 source tables not visible in card: {missing_tables}")
    return CheckResult(hard=tuple(hard), warn=tuple(warn))


def check_card(card_path: Path, paper_path: Path | None) -> CheckResult:
    if not card_path.exists():
        return CheckResult(hard=(f"H0 card file missing: {card_path}",), warn=())
    text = card_path.read_text(encoding="utf-8")
    hard = [
        *check_frontmatter(text),
        *check_sections(text),
    ]
    pdf_result = check_pdf_backed_rules(text, paper_path)
    return CheckResult(hard=tuple(hard + list(pdf_result.hard)), warn=pdf_result.warn)


def main() -> int:
    args = parse_args(sys.argv)
    result = check_card(args.card_path, args.paper_path)
    for finding in result.hard:
        print(f"FAIL  {finding}")
    for finding in result.warn:
        print(f"WARN  {finding}")
    if result.hard:
        return 1
    if result.warn:
        print("PASS  warning review required")
        return 0
    print("PASS  no mechanical findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
