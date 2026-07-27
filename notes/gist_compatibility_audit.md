# Task 32 Gist-Compatibility and Publication Audit

Date: 2026-07-25

Status: complete after a browser-stage macro erratum; the corrected `paper.md`
is ready for post-push live-browser confirmation and the final cross-artifact
publication checks. No Gist was created or published.

## Post-Task33 explanatory-revision addendum

The numerical counts in the original Task 32 record below describe the
publication-format snapshot at commit `c42b2fb`. A reader-approved explanatory
revision on 2026-07-27 subsequently expanded `paper.md`: notation is now
defined at first use, design choices are motivated, every theorem is tied back
to the opening problem, an English request is translated into typed atoms, and
the empirical findings are mapped to the exact layers they affect. No theorem,
frozen endpoint, evidence grade, or policy/value existence boundary changed.

The post-revision source has 1,894 single-dollar delimiters, forming 947
single-line inline expressions, and 212 display-dollar delimiter lines,
forming 106 displays. GitHub's `/markdown` API agrees exactly on 947 inline and
106 display math elements, 73 headings, 16 tables, two images, and one code
block, with no raw dollar residue or relative target. The source still contains
zero `\operatorname`, `\hline`, `\left\{`, and `\!` fragments. Its current
operator inventory is 19 `\mathop{\text{...}}` spellings plus nine explicit
`\mathsf{ReLU}` spellings. Main text now counts 14,720 words under the same
repository regex used for Task 32. These values supersede the old counts only
for the current artifact; the dated Task 32 measurements remain the historical
formatting record.

## Durable result

Task 32 changed presentation and destinations, not the paper's theorem set,
claim grades, frozen numbers, or interpretive boundaries. The public source now
has no repository-relative dependency: its two figures use immutable raw links
to pushed commit
`446f46645defa681ef840850fdec8b5ed47d3f4e`, and Appendix E's reproduction
links use immutable GitHub permalinks to the same package. Repository commands,
hashes, and transport history remain in the reproducibility appendix; no task
IDs, audit banners, claim-ledger labels, or development scaffolding enter the
main narrative.

The five known inline expressions that crossed physical lines were reflowed.
A GitHub-render inspection then found and repaired three additional classes of
formatting defect:

1. a display containing a physical line consisting only of `=` was parsed as a
   setext heading rather than mathematics;
2. adjacent inline expressions containing unprotected `_` or `*` tokens could
   be joined as Markdown emphasis; and
3. a display nested in a numbered list degraded to a code block in the complete
   document.

The repairs use an aligned equality, prose or TeX spellings that do not collide
with emphasis, and a single-line inline probability bound in the list. They do
not alter the mathematical statements.

### Browser-stage macro erratum

After the Task 32 commit was pushed, live GitHub screenshots exposed a stage
that the `/markdown` API check does not exercise. The API had correctly wrapped
the formulas in `<math-renderer>` elements, but GitHub's browser-side MathJax
sanitizer then rejected `\operatorname`. GitHub's own `github/markup` issue
tracker records the same error and gives `\mathop{\text{...}}` as a
spacing-preserving workaround. The paper used `\operatorname` 20 times across
`ReLU`, `diam`, `id`, `pred`, `im`, `diag`, and `Fix`.

All 20 occurrences are now written in the issue-recorded
`\mathop{\text{...}}` workaround form, which preserves operator spacing. This
is a typography-only substitution: the formulas, theorem statements, and
proof steps are unchanged. A source check now requires zero `\operatorname`
occurrences. That repair was subsequently pushed; the next live-browser review
reported no further `\operatorname` example and instead exposed the two
different incompatibilities below.

Two later live-browser screenshots exposed two further isolated compatibility
failures in otherwise ordinary TeX. The running-example array's horizontal
rule was reported as a misplaced `\hline`; the public table does not require
rules, so it now uses an unruled three-column array. Appendix F's Hoeffding
event used `\left\{...\right\}`, which the browser reported as an unrecognized
left delimiter; it now uses the equally standard probability-event brackets
`\left[...\right]`, already rendered elsewhere in the paper. A whole-paper
scan found no second occurrence of either rejected fragment. The existing
paper-math regression now excludes all three known browser failures without
increasing the test count. This second repair is not yet pushed, so live
confirmation of these two formulas remains a post-push observation.

## Source and first-stage GitHub-render checks

The final source scan reports:

- 1,736 single-dollar delimiters, forming 868 closed inline expressions;
- 210 display-dollar delimiter lines, forming 105 display expressions;
- zero inline expression crossing a physical line;
- zero unpaired or raw delimiter;
- 73 headings: one level-1, 18 level-2, and 54 level-3 headings, with no level
  jump or duplicate title;
- 48 Markdown link/image occurrences, including two images, all absolute;
- one fenced `text` command block and no raw HTML dependency;
- NFC Unicode, no replacement character, NUL, tab, or carriage return; and
- 13 public theorem/proposition statements, unchanged.

The exact GitHub `/markdown` API, in `gfm` mode and repository context, produced
868 inline and 105 display `<math-renderer>` elements: exact agreement with the
source counts. The result contains 73 headings, 14 tables, two images, and one
code block; it contains no dollar sign outside a math element, no formula
fragment captured as emphasis, no unintended heading, and no relative
`href`/`src`. This supplies first-stage Markdown parsing, copy/paste, and
delimiter parity. It does not by itself execute the browser-side MathJax macro
allowlist, which is why the original `\operatorname` defect escaped it.

Both figures were visually inspected. Their pinned raw URLs return `200
image/png`, and their local files remain readable RGBA PNGs at 1440×864 and
1080×810. The appendix-only repository links likewise return `200`; they no
longer depend on the Gist's own file namespace.

The established main-text token rule now counts 11,763 words. The 15-token
increase from Task 31B's 11,748 is entirely the source-level effect of replacing
two relative figure paths with long immutable URLs; reader-facing prose did not
grow.

## Live citation and link disposition

The canonical DOI metadata for He, Li, Xu, and Zheng, “ReLU Deep Neural
Networks and Linear Finite Elements,” remains
`10.4208/jcm.1901-m2018-0160`. On 2026-07-25 the DOI resolver redirected to
`https://www.global-sci.com/jcm/article/view/12421`, whose lowercase journal
path returned `404`. The case-correct primary Global Science Press page,
`https://www.global-sci.com/JCM/article/view/12421`, returned `200` and exposed
the title, four authors, *Journal of Computational Mathematics*, volume 38,
issue 3, pages 502–527, year 2020, and the same DOI. `paper.md` and
`references.bib` therefore use the live primary page while retaining the
canonical DOI metadata.

The link sweep also found that the former author-hosted Sutton and Barto book
page presented a self-signed TLS certificate. The paper and bibliography now
use the live MIT Press second-edition page. Across the final paper's 46 unique
external destinations, scripted GET requests returned 30 status `200`, one
status `202`, and 15 access-control `403` responses at recognizable publisher
or DOI destinations; none returned `404`. The Caltech page among the bot-guarded
set was independently opened successfully. The 403 group is recorded as
automated-access protection, not silently counted as a successful HTTP fetch.

## Validation and scope

Workspace validation passed after the browser-macro regression was added:

- `python -m verification`: 178/178;
- `python -m experiments.run_repaired_experiment --preflight`: pass, including
  source hashes and release/debug native equivalence, without final payload;
- `python -m verification.check_links .`: all local links valid;
- `git diff --check`: pass; and
- edited text files are LF-only; and
- the corrected paper contains zero `\operatorname` and 20
  `\mathop{\text{...}}` operator spellings, zero `\hline`, and zero
  `\left\{`.

The original checks were repeated against a clean archive with the exact Task
32 patch before that task commit. The browser-macro erratum, including its new
regression, was likewise applied to a fresh archive and passed 178/178,
preflight, and local-link validation. Public CI and live browser rendering
remain post-push observations. Task 32 did not itself authorize creating a
public Gist, drafting the Substack adaptation, changing a scientific claim, or
rerunning final confirmation. Task 33 subsequently completed the adaptation;
Task 34 is the current final cross-check.
