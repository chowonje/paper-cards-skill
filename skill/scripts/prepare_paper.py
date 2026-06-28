#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run prepare_paper.py path/to/paper.pdf [--out paper-card-runs]
# 3. Or make executable and run:
#      chmod +x prepare_paper.py && ./prepare_paper.py path/to/paper.pdf [--out paper-card-runs]
# ──────────────────

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Mapping
from typing import Final, Sequence

DEFAULT_OUT_DIR: Final = Path("paper-card-runs")
DEFAULT_DPI: Final = 110
DEFAULT_MAX_PAGES: Final = 50
SKILL_DIR: Final = Path(__file__).resolve().parents[1]
SLUG_PATTERN: Final = re.compile(r"[^a-z0-9]+")
YEAR_PATTERN: Final = re.compile(r"\b(?:19|20)\d{2}\b")
PAGES_PATTERN: Final = re.compile(r"Pages:\s+(\d+)")
TITLE_PATTERN: Final = re.compile(r"Title:\s+(.+)")


@dataclass(frozen=True, slots=True)
class CliArgs:
    pdf_path: Path
    out_dir: Path
    dpi: int
    max_pages: int
    slug: str | None


@dataclass(frozen=True, slots=True)
class PreparedPaths:
    run_dir: Path
    pages_dir: Path
    text_dir: Path
    card_path: Path
    prompt_path: Path
    manifest_path: Path


@dataclass(frozen=True, slots=True)
class PaperMetadata:
    title: str
    year: int
    page_count: int | None


class UsageError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def parse_positive_int(raw: str, label: str) -> int:
    try:
        value = int(raw)
    except ValueError as error:
        raise UsageError(f"{label} must be an integer: {raw}") from error
    if value < 1:
        raise UsageError(f"{label} must be >= 1: {raw}")
    return value


def usage() -> str:
    return (
        "usage: prepare_paper.py <paper.pdf> "
        "[--out DIR] [--dpi N] [--max-pages N] [--slug NAME]"
    )


def parse_args(argv: list[str]) -> CliArgs:
    if len(argv) < 2:
        raise UsageError(usage())

    pdf_path = Path(argv[1])
    out_dir = DEFAULT_OUT_DIR
    dpi = DEFAULT_DPI
    max_pages = DEFAULT_MAX_PAGES
    slug: str | None = None
    index = 2

    while index < len(argv):
        option_name = argv[index]
        if index + 1 >= len(argv):
            raise UsageError(f"missing argument for {option_name}")
        option_arg = argv[index + 1]
        match option_name:
            case "--out":
                out_dir = Path(option_arg)
            case "--dpi":
                dpi = parse_positive_int(option_arg, "--dpi")
            case "--max-pages":
                max_pages = parse_positive_int(option_arg, "--max-pages")
            case "--slug":
                slug = option_arg
            case unexpected:
                raise UsageError(f"unknown option: {unexpected}")
        index += 2

    return CliArgs(
        pdf_path=pdf_path,
        out_dir=out_dir,
        dpi=dpi,
        max_pages=max_pages,
        slug=slug,
    )


def require_tool(name: str) -> str:
    tool = shutil.which(name)
    if tool is None:
        raise UsageError(f"required tool not found on PATH: {name}")
    return tool


def run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, check=False, text=True)


def read_pdf_header(pdf_path: Path) -> None:
    if not pdf_path.exists():
        raise UsageError(f"PDF not found: {pdf_path}")
    with pdf_path.open("rb") as handle:
        header = handle.read(5)
    if header != b"%PDF-":
        raise UsageError(f"input does not look like a PDF: {pdf_path}")


def slugify(value: str) -> str:
    slug = SLUG_PATTERN.sub("-", value.lower()).strip("-")
    if slug:
        return slug[:80].strip("-")
    return "paper-card"


def first_page_text(pdf_path: Path, pdftotext: str) -> str:
    completed = run_command([pdftotext, "-f", "1", "-l", "1", "-layout", str(pdf_path), "-"])
    if completed.returncode != 0:
        return ""
    return completed.stdout


def pdfinfo_metadata(pdf_path: Path, pdfinfo: str, pdftotext: str) -> PaperMetadata:
    completed = run_command([pdfinfo, str(pdf_path)])
    if completed.returncode != 0:
        return PaperMetadata(title=pdf_path.stem, year=0, page_count=None)
    title_match = TITLE_PATTERN.search(completed.stdout)
    pages_match = PAGES_PATTERN.search(completed.stdout)
    title = title_match.group(1).strip() if title_match is not None else pdf_path.stem
    metadata_or_page_text = completed.stdout + "\n" + first_page_text(pdf_path, pdftotext)
    years = [int(match.group(0)) for match in YEAR_PATTERN.finditer(metadata_or_page_text)]
    year = max(years) if years else 0
    pages = int(pages_match.group(1)) if pages_match is not None else None
    return PaperMetadata(title=title, year=year, page_count=pages)


def make_paths(out_dir: Path, slug: str) -> PreparedPaths:
    run_dir = out_dir / slug
    return PreparedPaths(
        run_dir=run_dir,
        pages_dir=run_dir / "pages",
        text_dir=run_dir / "text",
        card_path=run_dir / f"{slug}.md",
        prompt_path=run_dir / "agent_prompt.md",
        manifest_path=run_dir / "run_manifest.json",
    )


def render_pages(args: CliArgs, paths: PreparedPaths, pdftoppm: str, page_count: int | None) -> int:
    render_count = min(page_count, args.max_pages) if page_count is not None else args.max_pages
    command = [
        pdftoppm,
        "-png",
        "-r",
        str(args.dpi),
        "-f",
        "1",
        "-l",
        str(render_count),
        str(args.pdf_path),
        str(paths.pages_dir / "page"),
    ]
    completed = run_command(command)
    if completed.returncode != 0:
        raise UsageError(completed.stderr.strip() or "pdftoppm failed")
    return render_count


def extract_text(pdf_path: Path, paths: PreparedPaths, pdftotext: str) -> None:
    text_path = paths.text_dir / "paper.txt"
    first_page_path = paths.text_dir / "page-1.txt"
    full_text = run_command([pdftotext, "-layout", str(pdf_path), str(text_path)])
    if full_text.returncode != 0:
        raise UsageError(full_text.stderr.strip() or "pdftotext failed")
    first_page = first_page_text(pdf_path, pdftotext)
    if not first_page:
        raise UsageError("pdftotext first page extraction failed")
    first_page_path.write_text(first_page, encoding="utf-8")


def render_template(template_name: str, values: Mapping[str, str]) -> str:
    text = (SKILL_DIR / "templates" / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text + "\n"


def card_scaffold(metadata: PaperMetadata) -> str:
    return render_template("card_scaffold.md", {"title": metadata.title, "year": str(metadata.year)})


def agent_prompt(args: CliArgs, paths: PreparedPaths, metadata: PaperMetadata, rendered_pages: int) -> str:
    return render_template(
        "agent_prompt.md",
        {
            "pdf_path": str(args.pdf_path),
            "run_dir": str(paths.run_dir),
            "paper_text_path": str(paths.text_dir / "paper.txt"),
            "first_page_text_path": str(paths.text_dir / "page-1.txt"),
            "pages_dir": str(paths.pages_dir),
            "rendered_pages": str(rendered_pages),
            "card_path": str(paths.card_path),
            "title": metadata.title,
            "year": str(metadata.year),
            "page_count": str(metadata.page_count),
        },
    )


def write_manifest(args: CliArgs, paths: PreparedPaths, metadata: PaperMetadata, rendered_pages: int) -> None:
    payload = {
        "source_pdf_name": args.pdf_path.name,
        "run_dir_name": paths.run_dir.name,
        "files": {
            "card": paths.card_path.name,
            "agent_prompt": paths.prompt_path.name,
            "pages_dir": paths.pages_dir.name,
            "text_dir": paths.text_dir.name,
        },
        "title": metadata.title,
        "year": metadata.year,
        "page_count": metadata.page_count,
        "rendered_pages": rendered_pages,
        "status": "prepared",
        "next_step": "Open agent_prompt.md with an agent that can read the PDF and complete the card.",
        "privacy_note": "This manifest avoids absolute source PDF paths. agent_prompt.md may contain local execution paths.",
    }
    paths.manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare(args: CliArgs) -> PreparedPaths:
    read_pdf_header(args.pdf_path)
    pdfinfo = require_tool("pdfinfo")
    pdftoppm = require_tool("pdftoppm")
    pdftotext = require_tool("pdftotext")
    metadata = pdfinfo_metadata(args.pdf_path, pdfinfo, pdftotext)
    slug = args.slug if args.slug is not None else slugify(metadata.title)
    paths = make_paths(args.out_dir, slug)
    paths.pages_dir.mkdir(parents=True, exist_ok=True)
    paths.text_dir.mkdir(parents=True, exist_ok=True)
    rendered_pages = render_pages(args, paths, pdftoppm, metadata.page_count)
    extract_text(args.pdf_path, paths, pdftotext)
    paths.card_path.write_text(card_scaffold(metadata), encoding="utf-8")
    paths.prompt_path.write_text(agent_prompt(args, paths, metadata, rendered_pages), encoding="utf-8")
    write_manifest(args, paths, metadata, rendered_pages)
    return paths


def main() -> int:
    try:
        args = parse_args(sys.argv)
        paths = prepare(args)
    except UsageError as error:
        print(error.message, file=sys.stderr)
        return 2
    print(f"prepared: {paths.run_dir}")
    print(f"draft card: {paths.card_path}")
    print(f"agent prompt: {paths.prompt_path}")
    print(f"manifest: {paths.manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
