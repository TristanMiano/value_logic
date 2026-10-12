"""Tests for the repository-local Markdown link checker."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from verification.check_links import check_links, github_slug


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


class LinkParserTests(unittest.TestCase):
    def test_github_heading_spaces_and_custom_anchors(self) -> None:
        self.assertEqual(github_slug("OPP-02 — Is it useful?"), "opp-02--is-it-useful")
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.md").write_text(
                "# OPP-02 — Is it useful?\n<a id=\"ref-proof\"></a>\n"
                "<a name='LegacyAnchor'></a>\n## Repeat\n## Repeat\n## Repeat-1\n",
                encoding="utf-8",
            )
            (root / "source.md").write_text(
                "[heading](target.md#opp-02--is-it-useful)\n"
                "[reference](target.md#ref-proof) [named](target.md#LegacyAnchor)\n"
                "[duplicate](target.md#repeat-1) [collision](target.md#repeat-1-1)\n",
                encoding="utf-8",
            )
            self.assertEqual(check_links(root), [])

    def test_code_math_and_escaped_brackets_are_not_links(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_text(
                "`[inline](missing.md)`\n\n```text\n[fence](missing.md)\n```\n"
                "\n$$\nh+[I-(I-M)^k](d-h)\n$$\n"
                "\\[escaped](missing.md)\n[real](absent.md)\n",
                encoding="utf-8",
            )
            broken = check_links(root)
            self.assertEqual([(x.target, x.line) for x in broken], [("absent.md", 11)])

    def test_hidden_headings_and_anchor_markup_do_not_create_targets(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_text(
                "```md\n# Hidden\n<a id='hidden-id'></a>\n```\n"
                "`<a id='inline-id'></a>`\n"
                "[bad](#hidden) [bad](#hidden-id) [bad](#inline-id)\n",
                encoding="utf-8",
            )
            self.assertEqual(len(check_links(root)), 3)

    def test_custom_fragment_case_and_empty_links(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_text(
                "<a id='MixedCase'></a>\n[good](#MixedCase) [bad](#mixedcase) []()\n",
                encoding="utf-8",
            )
            self.assertEqual([x.target for x in check_links(root)], ["#mixedcase"])


if __name__ == "__main__":
    unittest.main()
