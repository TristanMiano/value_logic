# P3-08 portable display closure

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Administrative presentation work; zero research or principal-clock credit.

The user's preservation instruction takes precedence over applying the style
guard in place. Original scientific Markdown, source snapshots, old analyses,
ledgers, seals, source files, the style guard and workflow remain unchanged.

Read `v3/STYLE.md` and the existing `v3/checks/math_markdown.py`. Inspect the
canonical new main document, four P3-08 derivations, session summaries and
canonical review notes, plus the current structural and mean-price analyses.
Exclude duplicate frozen inputs, run/source/snapshot trees and plan-only notes.
Create a separate display copy only when the existing
`transform(text, protect=True)` changes the original notation. Add a banner
giving its original path and SHA-256, and relocate ordinary relative Markdown
link destinations so that they still address the original targets.

Record every inspected canonical original and any corresponding display copy
with hashes. Verify exact original preservation, declared transform equality,
relative-link destination equality and a focused portable source-convention
check. Run the unchanged global guard read-only and compare its findings with
the same guard rules applied to the base commit's Markdown blobs. Preserve
the global findings, including retained raw/source history; do not call a
failing global check a pass.

This work performs no browser inspection or live-render validation, no policy
execution and no mathematical re-evaluation. Stop after sufficient source and
link verification. The principal may add final packaging metadata separately.
