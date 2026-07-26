"""Regression checks for GitHub-compatible paper mathematics."""

from __future__ import annotations

from pathlib import Path
import unittest


class PaperMarkdownCompatibilityTests(unittest.TestCase):
    def test_github_rejected_operatorname_macro_is_absent(self) -> None:
        root = Path(__file__).resolve().parents[1]
        paper = (root / "paper.md").read_text(encoding="utf-8")
        self.assertNotIn(
            r"\operatorname",
            paper,
            "GitHub's browser-side math renderer rejects \\operatorname; "
            r"use \mathop{\text{...}} instead",
        )


if __name__ == "__main__":
    unittest.main()
