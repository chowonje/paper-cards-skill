#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: render_paper.sh <pdf_path> <outdir> [dpi] [first_page] [last_page]" >&2
}

PDF="${1:-}"
OUTDIR="${2:-}"
DPI="${3:-110}"
FIRST="${4:-}"
LAST="${5:-}"

if [[ -z "$PDF" || -z "$OUTDIR" ]]; then
  usage
  exit 64
fi

if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "ERROR: pdftoppm is required. Install poppler and ensure pdftoppm is on PATH." >&2
  exit 69
fi

if [[ ! -f "$PDF" ]]; then
  echo "ERROR: PDF not found: $PDF" >&2
  exit 66
fi

if ! head -c 5 "$PDF" | grep -q '%PDF'; then
  echo "ERROR: input does not look like a PDF." >&2
  exit 65
fi

mkdir -p "$OUTDIR"

ARGS=(-png -r "$DPI")
if [[ -n "$FIRST" ]]; then
  ARGS+=(-f "$FIRST")
fi
if [[ -n "$LAST" ]]; then
  ARGS+=(-l "$LAST")
fi

pdftoppm "${ARGS[@]}" "$PDF" "$OUTDIR/page"

COUNT=$(find "$OUTDIR" -maxdepth 1 -type f -name 'page-*.png' | wc -l | tr -d ' ')
echo "rendered $COUNT pages at ${DPI}dpi -> $OUTDIR"
