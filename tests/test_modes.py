from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_script(relative_path: str, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load script: {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


prepare_paper = load_script("skill/scripts/prepare_paper.py", "prepare_paper_for_tests")
qa_check = load_script("skill/scripts/qa_check.py", "qa_check_for_tests")


class PrepareModeTests(unittest.TestCase):
    def test_defaults_to_study_mode_when_mode_is_omitted(self) -> None:
        args = prepare_paper.parse_args(["prepare_paper.py", "paper.pdf"])

        self.assertEqual(args.mode, "study")
        self.assertEqual(prepare_paper.scaffold_template_name(args.language, args.mode), "card_scaffold_study.md")

    def test_mode_can_default_from_environment(self) -> None:
        previous = os.environ.get("PAPER_CARD_MODE")
        os.environ["PAPER_CARD_MODE"] = "evidence"
        try:
            args = prepare_paper.parse_args(["prepare_paper.py", "paper.pdf"])
        finally:
            if previous is None:
                del os.environ["PAPER_CARD_MODE"]
            else:
                os.environ["PAPER_CARD_MODE"] = previous

        self.assertEqual(args.mode, "evidence")

    def test_accepts_full_and_evidence_modes(self) -> None:
        full_args = prepare_paper.parse_args(["prepare_paper.py", "paper.pdf", "--mode", "full"])
        evidence_args = prepare_paper.parse_args(["prepare_paper.py", "paper.pdf", "--mode", "evidence"])

        self.assertEqual(full_args.mode, "full")
        self.assertEqual(evidence_args.mode, "evidence")
        self.assertEqual(
            prepare_paper.scaffold_template_name(full_args.language, full_args.mode),
            "card_scaffold.md",
        )
        self.assertEqual(
            prepare_paper.scaffold_template_name(evidence_args.language, evidence_args.mode),
            "card_scaffold.md",
        )


class QaModeTests(unittest.TestCase):
    def test_study_card_uses_study_headings_without_evidence_appendix(self) -> None:
        card = "\n".join(
            [
                "---",
                'title: "Example"',
                "authors: []",
                "year: 2024",
                'source: "arXiv"',
                "tags: [paper-card, study]",
                "---",
                "",
                "# Example",
                "",
                "## 30초 요약",
                "짧은 요약.",
                "",
                "## 이 논문이 풀려는 문제",
                "문제 설명.",
                "",
                "## 핵심 아이디어 3개",
                "- 하나",
                "- 둘",
                "- 셋",
                "",
                "## 그림으로 이해하기",
                "그림 설명.",
                "",
                "## 꼭 기억할 수식",
                "없음.",
                "",
                "## 예시로 이해하기",
                "예시 설명.",
                "",
                "## 이 논문을 읽고 나면 알게 되는 것",
                "알게 되는 점.",
                "",
                "## 다음에 읽으면 좋은 것",
                "다음 논문.",
                "",
            ],
        )

        result = qa_check.check_card_text(card, paper_path=None)

        self.assertEqual(result.hard, ())


if __name__ == "__main__":
    unittest.main()
