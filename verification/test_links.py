"""Tests for the repository-local Markdown link checker."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from verification.check_links import check_links


class LinkCheckerTests(unittest.TestCase):
    def test_repository_links_are_valid(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(check_links(root), [])

    def test_missing_file_and_anchor_are_reported(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.md").write_text("# Real heading\n", encoding="utf-8")
            (root / "source.md").write_text(
                "[missing](absent.md) [bad anchor](target.md#not-real)\n",
                encoding="utf-8",
            )
            broken = check_links(root)
            self.assertEqual(len(broken), 2)
            self.assertEqual(
                {item.detail for item in broken},
                {"target does not exist", "heading anchor does not exist"},
            )


if __name__ == "__main__":
    unittest.main()
