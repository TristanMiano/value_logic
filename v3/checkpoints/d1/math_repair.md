# Post-audit GitHub math repair

October 29, 2026. **Codex (GPT-6)**. Presentation repair; zero research credit.
This additive record preserves the pre-decision audit and its artifact hashes.

The author's two errors were reproduced in GitHub's live rendering of the
PR24 main version. Ordinary dollar-delimited display math lost escapes on
braces and norm bars. Switching to GitHub's documented math fences fixed that
problem, but did not alone repair equation 13. Live isolation also reproduced
the error on the standalone sum with literal subscript `s<t`. The final build
uses `\lt` / `\gt`, explicit zero-space aligned-row endings, and protected
math fences. No algebra was changed.

Visual inspection exposed another presentation defect: ungrouped terms in the
numbered MathML cell stacked vertically in the browser. Grouping the expression
keeps it on one row. Equations 13, 14 and 15 were then inspected as readable
aligned or horizontal expressions. The final scan at commit
`56a0244a` found **378 math-renderer elements, 378 rendered MathML elements,
20 displays and zero flash-error elements**. The test used the actual public
GitHub branch page, not a local approximation to GitHub's renderer.

The build's twenty displays are checked against the canonical mathematical
payload, allowing only equation labels/tags, outer grouping, inequality macro
spelling, whitespace and zero-space row breaks. The canonical source, generated
LaTeX and bibliography remain unchanged. A fresh Tectonic compilation had the
same page pixels on all fourteen pages at 1.5x resolution; page 9 was also
visually inspected. The original audited PDF was retained, SHA256
`ec602e98756e247fba63fb750d4eeb9c3c9d0898f12005b4ae8649aca4071b54`.

The portable delimiter checker was never a live rendering test. This repair
does not retroactively claim that its earlier PASS guaranteed GitHub rendering.
The [build guide](../../report/README.md) and
[package check](../../report/verify.py) describe the revised contract. GitHub's
[official math documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)
documents fenced displays; the additional normalizations above are supported
by the recorded live checks, not asserted as general MathJax requirements.
