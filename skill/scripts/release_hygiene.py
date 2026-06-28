#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run privacy_preflight.py first, then review known false positives:
#      uv run skill/scripts/release_hygiene.py --report /tmp/privacy/report.json
# 3. Use a custom reviewed-findings file:
#      uv run skill/scripts/release_hygiene.py --report /tmp/privacy/report.json --reviewed privacy-reviewed-findings.json
# ──────────────────

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

DEFAULT_REVIEWED_PATH: Final = Path("privacy-reviewed-findings.json")

type JsonValue = str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class CliArgs:
    report_path: Path
    reviewed_path: Path


@dataclass(frozen=True, slots=True)
class Finding:
    severity: str
    kind: str
    file: str
    line: int | None
    message: str

    def key(self) -> str:
        return f"{self.kind}\t{self.file}\t{self.line}"


@dataclass(frozen=True, slots=True)
class ReviewedFinding:
    kind: str
    file: str
    line: int | None
    line_sha256: str | None
    classification: str
    reason: str

    def key(self) -> str:
        return f"{self.kind}\t{self.file}\t{self.line}"


class UsageError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def usage() -> str:
    return "usage: release_hygiene.py --report REPORT_JSON [--reviewed privacy-reviewed-findings.json]"


def parse_args(argv: list[str]) -> CliArgs:
    report_path: Path | None = None
    reviewed_path = DEFAULT_REVIEWED_PATH
    index = 1
    while index < len(argv):
        option_name = argv[index]
        if index + 1 >= len(argv):
            raise UsageError(f"missing argument for {option_name}")
        option_arg = argv[index + 1]
        match option_name:
            case "--report":
                report_path = Path(option_arg)
            case "--reviewed":
                reviewed_path = Path(option_arg)
            case unexpected:
                raise UsageError(f"unknown option: {unexpected}")
        index += 2
    if report_path is None:
        raise UsageError(usage())
    return CliArgs(report_path=report_path, reviewed_path=reviewed_path)


def read_json(path: Path) -> JsonValue:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise UsageError(f"could not read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise UsageError(f"invalid JSON in {path}: {error}") from error


def expect_mapping(value: JsonValue, label: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise UsageError(f"{label} must be a JSON object")
    return value


def expect_list(value: JsonValue, label: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise UsageError(f"{label} must be a JSON array")
    return value


def expect_str(value: JsonValue, label: str) -> str:
    if not isinstance(value, str):
        raise UsageError(f"{label} must be a string")
    return value


def expect_optional_int(value: JsonValue, label: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int):
        raise UsageError(f"{label} must be an integer or null")
    return value


def expect_optional_str(value: JsonValue, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise UsageError(f"{label} must be a string or null")
    return value


def parse_finding(value: JsonValue) -> Finding:
    item = expect_mapping(value, "finding")
    return Finding(
        severity=expect_str(item.get("severity"), "finding.severity"),
        kind=expect_str(item.get("kind"), "finding.kind"),
        file=expect_str(item.get("file"), "finding.file"),
        line=expect_optional_int(item.get("line"), "finding.line"),
        message=expect_str(item.get("message"), "finding.message"),
    )


def parse_reviewed(value: JsonValue) -> ReviewedFinding:
    item = expect_mapping(value, "reviewed finding")
    return ReviewedFinding(
        kind=expect_str(item.get("kind"), "reviewed.kind"),
        file=expect_str(item.get("file"), "reviewed.file"),
        line=expect_optional_int(item.get("line"), "reviewed.line"),
        line_sha256=expect_optional_str(item.get("line_sha256"), "reviewed.line_sha256"),
        classification=expect_str(item.get("classification"), "reviewed.classification"),
        reason=expect_str(item.get("reason"), "reviewed.reason"),
    )


def load_findings(report_path: Path) -> tuple[Finding, ...]:
    report = expect_mapping(read_json(report_path), "privacy report")
    findings = expect_list(report.get("findings"), "privacy report findings")
    return tuple(parse_finding(item) for item in findings)


def load_reviewed(reviewed_path: Path) -> dict[str, ReviewedFinding]:
    payload = expect_mapping(read_json(reviewed_path), "reviewed findings")
    reviewed = expect_list(payload.get("reviewed_findings"), "reviewed_findings")
    entries = tuple(parse_reviewed(item) for item in reviewed)
    return {entry.key(): entry for entry in entries}


def line_sha256(finding: Finding) -> str | None:
    if finding.line is None or finding.file == ".":
        return None
    path = Path(finding.file)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    if finding.line < 1 or finding.line > len(lines):
        return None
    return hashlib.sha256(lines[finding.line - 1].encode("utf-8")).hexdigest()


def is_reviewed(finding: Finding, reviewed: dict[str, ReviewedFinding]) -> bool:
    entry = reviewed.get(finding.key())
    if entry is None:
        return False
    current_hash = line_sha256(finding)
    if entry.line_sha256 is None:
        return current_hash is None
    return current_hash == entry.line_sha256


def decision(unresolved: tuple[Finding, ...]) -> str:
    if any(finding.severity == "block" for finding in unresolved):
        return "BLOCK"
    if unresolved:
        return "WARN"
    return "PASS"


def run(args: CliArgs) -> int:
    findings = load_findings(args.report_path)
    reviewed = load_reviewed(args.reviewed_path)
    unresolved = tuple(finding for finding in findings if not is_reviewed(finding, reviewed))
    release_decision = decision(unresolved)
    print(f"Decision: {release_decision}")
    print(f"Findings: {len(findings)} total / {len(findings) - len(unresolved)} reviewed / {len(unresolved)} unresolved")
    if unresolved:
        print("Unresolved:")
        for finding in unresolved:
            loc = f"{finding.file}:{finding.line}" if finding.line is not None else finding.file
            print(f"- {finding.severity.upper()} {finding.kind} {loc}")
    return 2 if release_decision == "BLOCK" else 1 if release_decision == "WARN" else 0


def main() -> int:
    try:
        args = parse_args(sys.argv)
        return run(args)
    except UsageError as error:
        print(error.message, file=sys.stderr)
        return 64


if __name__ == "__main__":
    raise SystemExit(main())
