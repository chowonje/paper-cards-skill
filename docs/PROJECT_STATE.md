# Project State

## 2026-06-29

- `prepare` now supports `--mode study|evidence|full`.
- Default output mode is `study`, producing a learner-facing card without `# Evidence Appendix`.
- `full` and `evidence` modes preserve the previous review/audit card shape with Reader Card, Evidence Appendix, Figure/Table Coverage Ledger, and QA Notes.
- `PAPER_CARD_MODE` can set the default mode for direct script usage.
- Mechanical QA auto-detects study cards and checks study headings without requiring the Evidence Appendix ledger.
- Full/evidence scaffolds now mark the Reader Card region before the Evidence Appendix.
- Study scaffolds include a short glossary before central formulas to reduce first-reader friction.
- `pro-review/` is ignored because it is a local/private evaluation packet, not a release artifact.
