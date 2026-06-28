Use this repository's paper-cards skill to finish a Korean paper card.

Read these files first:
- {{skill_path}}
- {{card_spec_path}}
- {{generation_cautions_path}}

Input PDF:
{{pdf_path}}

Prepared workspace:
{{run_dir}}

Extracted text:
{{paper_text_path}}

First page text:
{{first_page_text_path}}

Rendered pages:
{{pages_dir}}

Rendered pages: first {{rendered_pages}} page(s). Render more pages manually if the paper is longer.

Draft card to replace:
{{card_path}}

Known metadata from pdfinfo:
- title: {{title}}
- year: {{year}}
- page_count: {{page_count}}

Required final checks:
1. Verify document identity from page 1.
2. Replace all TODOs in the draft card.
3. Use physical PDF page numbers.
4. Describe all important figures and tables with a coverage ledger.
5. Keep formulas in LaTeX.
6. Keep interpretation inside `> [!note] 해석` callouts.
7. Run:
   uv run skill/scripts/qa_check.py "{{card_path}}" --paper "{{pdf_path}}"
