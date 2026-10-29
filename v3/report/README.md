# Phase-three paper: sources and build

The delivered editions are [paper_v3.md](../../paper_v3.md) and
[paper_v3.pdf](../../paper_v3.pdf). The editable scientific source is
[content.md](content.md); the complete editable LaTeX project is
[tex/main.tex](tex/main.tex), [tex/references.bib](tex/references.bib), and
[tex/arxiv.sty](tex/arxiv.sty). Edit the canonical source and regenerate to keep
both editions synchronized. Direct TeX edits are possible for experimentation,
but must be incorporated into the source/template before publication.

## Build

Use Python 3.13, Pandoc 3.13, and Tectonic 0.17.0. The latter two portable Windows
release URLs and verified SHA256 digests are in [build_tools.json](build_tools.json).
Install them outside the repository and put their executables on PATH, or pass
their paths explicitly. From the checkout root:

```powershell
python -X utf8 v3/report/build.py --pdf
# Alternatively:
python -X utf8 v3/report/build.py --pandoc C:/tools/pandoc.exe --tectonic C:/tools/tectonic.exe --pdf
```

The first Tectonic invocation needs network access to acquire its TeX bundle;
subsequent builds use its cache. The build reads `content.md`, expands tables
generated from preserved records, emits GitHub Markdown with explicit anchors
and numbered MathJax equations, emits equivalent TeX with real theorem/proof
environments and cross-references, generates BibTeX from `references.json`,
and compiles/copies the PDF to the repository root. It checks every result and
equation label and citation key. [consistency.json](consistency.json) records
the common source hashes, citation order, and delivered artifact hashes.

For an existing TeX installation, build `tex/main.tex` with pdfLaTeX or XeLaTeX,
BibTeX, and two further LaTeX passes from `v3/report/tex`. Tectonic and the Codex
desktop compiler were actually used for this delivery; another TeX distribution
has not been tested here. PDF metadata or toolchain changes can change PDF bytes
without changing the science. The generated Markdown and TeX are deterministic
for the pinned Pandoc version.

## Evidence and verification

```powershell
python -X utf8 v3/report/tables.py
python -X utf8 v3/report/episode_check.py
python -X utf8 v3/report/verify.py
python tools/evidence_paths.py verify
# After staging the intended publication files:
python tools/check_repo_paths.py
```

`tables.py` reconstructs all displayed measured table cells and savings from
saved JSON, including the sixteen raw historical cost records. It writes
[tables/data.json](tables/data.json) with source hashes and exact fractions.
It does not rerun the historical experiments. The 77.5% coordinate example is
separately labelled analytic arithmetic. `episode_check.py` is a narrow
reconstruction on the exposed worked example plus the existing N16 rational
threshold, writing [episode_result.json](episode_result.json); it is not another
confirmation attempt. `verify.py` checks local links, shared-source labels,
artifact/source hashes, preserved V19 seals, upstream copied bytes, and table
claims. These checks do not prove the truth of external mathematical premises.

[claims.md](claims.md) maps paper claims to proofs, code, tests, and literature
read scopes. [portfolio.md](portfolio.md) preserves secondary directions and
adverse comparisons. [review.md](review.md) records the final editorial and
rendered-page inspection. Administrative timing and publication records are
under [log/](log/session.md), outside the paper narrative.

## Upstream guidance, template, and licenses

The vendored Academic Paper Skills guidance is MIT-licensed, revision
`827e13e2299c0a15d397ce095bc548817a2cf3cb` from
[DELONG-L/Academic-Paper-Skills](https://github.com/DELONG-L/Academic-Paper-Skills).
Its paper-writing, figures/tables, review, policy, scripts, and supporting docs
retain their relative directory structure under `guide/`. See
[LICENSE](guide/LICENSE) and [THIRD_PARTY_NOTICES.md](guide/THIRD_PARTY_NOTICES.md).
The guidance was adapted to a mathematical synthesis and remains subordinate
to this project's research protocol and the author's scope.

The presentation starts from the MIT-licensed
[kourgeorge/arxiv-style](https://github.com/kourgeorge/arxiv-style), revision
`920514696f6e7270cab0558fd97c44515c63b4c4`. Unmodified `template.tex` and
`arxiv.sty`, its README, and license are in `upstream/`. The adapted template
is [template.tex](template.tex); the runtime style and license are in `tex/`.
Placeholder authors, affiliations, text, and references were not reused.
[upstream.json](upstream.json) records copied-file hashes and the GitHub math
documentation source. No third-party research-paper PDF is redistributed.
