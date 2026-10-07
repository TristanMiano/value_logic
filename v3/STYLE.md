# Mathematical Markdown

Use GitHub's code-protected math notation in phase-three Markdown. It keeps
Markdown's own handling of backslashes, braces, underscores and asterisks
from changing the TeX passed to the mathematical renderer.

- Inline: write `$` followed by a backtick, the expression, a backtick and `$`.
  For example, the source ``$`x_i\le y_i`$`` renders as $`x_i\le y_i`$.
- Display: use a fenced block with language `math`, without dollar delimiters
  inside that fence. Matrix row separators and escaped set braces then remain
  literal TeX input.
- For named mathematical labels, use `\mathrm{Label}`. Where operator spacing
  or limits matter, use `\mathop{\mathrm{Label}}` and an explicit `\limits`
  when appropriate. Avoid the renderer-rejected `\operatorname` macro.
- Keep source-code examples in ordinary code fences. An example that explains
  unsupported syntax should remain literal code, so readers can see it.

GitHub documents both protected forms in
[Writing mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions).
The project's earlier [compatibility audit](../notes/gist_compatibility_audit.md)
records why source parsing and live browser rendering require separate checks.

Run from the repository root:

```bash
python v3/checks/math_markdown.py
```

The lightweight GitHub Actions workflow runs this guard for Markdown changes.
It rejects rendered uses of the known unsupported macro, paired legacy math
delimiters, and unprotected phase-three mathematics. It preserves inline code
and non-math fences. It is a deliberately limited source-convention check:
it neither proves the mathematics nor emulates GitHub's complete renderer.
Inspect the live page after material formatting changes, including matrix
rows, set braces, operator labels and formula errors.

`--fix` applies the documented notation substitutions. An optional fresh
`--receipt PATH` saves the paths and before/after hashes; it refuses to
overwrite an existing receipt. Historical scientific manifests retain the
hashes of the exact files originally used. A later presentation repair must
not rewrite those snapshots or any measured time record.

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
