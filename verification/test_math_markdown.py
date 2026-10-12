"""Focused Markdown grammar and safe math-formatting regressions.

These tests exercise delimiter boundaries and masking contracts used by both
publication guards. They do not render TeX or validate mathematical results.
"""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v3.checks.math_markdown import (
    mask_literals,
    mask_literals_and_math,
    math_spans,
    transform,
)


class MathMarkdownGrammarTests(unittest.TestCase):
    def bodies(self, text):
        return [body for _, _, _, body in math_spans(text)]

    def test_unmatched_backtick_does_not_hide_later_equations(self):
        text = "A literal ` has no mate.\n\nNow \\(x+y\\) must be checked."
        self.assertEqual(["x+y"], self.bodies(text))
        self.assertIn("$`x+y`$", transform(text, protect=True))

    def test_code_span_needs_an_exact_backtick_run(self):
        text = "``literal ` $not_math$ ` literal`` and \\(visible\\)."
        self.assertEqual(["visible"], self.bodies(text))
        self.assertIn("$not_math$", transform(text, protect=True))

    def test_backslashes_inside_code_do_not_escape_its_closing_backtick(self):
        text = "`literal \\` and \\(visible\\)"
        self.assertEqual(["visible"], self.bodies(text))

    def test_short_fence_cannot_close_a_longer_fence(self):
        text = "````python\n```\n\\(literal\\)\n````\n\\(visible\\)\n"
        self.assertEqual(["visible"], self.bodies(text))

    def test_quote_and_list_fences_are_literal(self):
        text = ("> ```text\n> \\(literal\\)\n> ```\n\n"
                "1. ```text\n   \\(also_literal\\)\n   ```\n\n\\(visible\\)\n")
        self.assertEqual(["visible"], self.bodies(text))

    def test_indented_code_and_list_continuation_are_distinct(self):
        code = "An example:\n\n    \\(literal\\)\n\n\\(visible\\)\n"
        self.assertEqual(["visible"], self.bodies(code))
        prose = "1. An item.\n\n    A continuation with \\(visible\\).\n"
        self.assertEqual(["visible"], self.bodies(prose))

    def test_math_fence_is_checked_and_nonmath_fence_is_preserved(self):
        text = ("~~~math\n\\operatorname{rank} A\n~~~\n\n"
                "~~~text\n\\operatorname{literal} \\(x\\)\n~~~\n")
        after = transform(text, protect=True)
        self.assertIn(r"\mathrm{rank} A", after)
        self.assertIn(r"\operatorname{literal} \(x\)", after)

    def test_protected_inline_math_can_contain_a_dollar(self):
        text = "$`\\text{price \\$5} + x`$ then \\(y\\)"
        self.assertEqual([r"`\text{price \$5} + x`", "y"], self.bodies(text))
        after = transform(text, protect=True)
        self.assertEqual(after, transform(after, protect=True))

    def test_currency_and_escaped_dollars_stay_prose(self):
        text = r"The fee is $5 and later $10; escaped \$x\$ stays literal."
        self.assertEqual([], self.bodies(text))
        self.assertEqual(text, transform(text, protect=True))

    def test_math_does_not_pair_delimiters_through_code_blocks(self):
        text = "$open\n\n```text\n$close\n```\n\n\\(visible\\)\n"
        self.assertEqual(["visible"], self.bodies(text))

    def test_masking_keeps_length_lines_and_only_hides_nonprose(self):
        text = ("[real](target.md) and `[literal](missing.md)`\n"
                "$`[x](y)`$ and \\([a](b)\\)\r\n"
                "```math\n[c](d)\n```\n[after](other.md)\n")
        masked = mask_literals_and_math(text)
        self.assertEqual(len(text), len(masked))
        self.assertEqual([i for i, c in enumerate(text) if c in "\r\n"],
                         [i for i, c in enumerate(masked) if c in "\r\n"])
        self.assertIn("[real](target.md)", masked)
        self.assertIn("[after](other.md)", masked)
        for fragment in ["[literal]", "[x]", "[a]", "[c]"]:
            self.assertNotIn(fragment, masked)

    def test_heading_mask_can_retain_inline_code_text_and_inline_math(self):
        text = "# A `name` and $`x`$\n\n```text\n# hidden\n```\n\n```math\n# not-a-heading\n```\n"
        self.assertIn("# A `name` and $`x`$", mask_literals(text, inline=False))
        self.assertNotIn("# hidden", mask_literals(text, inline=False))
        self.assertNotIn("# not-a-heading", mask_literals(text, inline=False))
        self.assertNotIn("`name`", mask_literals(text))
        self.assertIn("$`x`$", mask_literals(text))


if __name__ == "__main__":
    unittest.main()
