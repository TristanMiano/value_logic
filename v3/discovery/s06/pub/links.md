# Published CI link failure: inherited baseline

**The 2,214 failing local links are inherited from the pre-s06 base.** Exact
Git-object reconstructions found zero new failures, zero failures on changed
lines, and zero failures originating in the 17 new s06 Markdown documents.
This diagnoses the failed gate; it does not turn the repository-wide workflow
into a pass.

Prepared by **ChatGPT (GPT-6 Astra Pro)** as publication administration.
The s06 research clock remains closed. This check adds **zero research
minutes** and makes **zero solver, proof-provider, LP or cost-audit calls**.
No scientific output, frozen archive, registered checker or workflow changed.

## CI evidence and gate scope

The principal inspected the complete
[first-publication GitHub job log](https://github.com/TristanMiano/value_logic/actions/runs/38288364621/job/114942091817)
for commit `f28d760e16950b5417aa85b315fea61ab9bb1e1b`; the relevant original
failure block is retained losslessly, including original whitespace, in
[the saved JSON excerpt](verify_log.json). Its hashes bind both the excerpt and
the earlier local text representation. Dependency installation
passed. The summary reported `Ran 1689 tests in 261.283s` and
`FAILED (failures=1)`. The sole failure was
`test_links.LinkCheckerTests.test_repository_links_are_valid`, reporting
2,214 broken local links. A later status observation of `6211f8f` found the checkout-portability workflow
completed successfully and both mathematical-Markdown and finite-witness
workflows completed with failure. The detailed test summary above is bound to
the first-publication job; no all-green CI claim is made here.

The unchanged [workflow](../../../../.github/workflows/verify.yml) installs
NumPy 2.2.5, Matplotlib 3.10.8 and CPU PyTorch 2.8.0 on Python 3.13, then runs
`python -m verification`. Its [entrypoint](../../../../verification/__main__.py)
discovers `verification/test_*.py`. It does not execute the new s06 research
entrypoints or require their PySAT, HiGHS or SciPy dependencies.

The new-document-sensitive gate is the
[repository link test](../../../../verification/test_links.py), which scans
physical Markdown files recursively using the
[existing checker](../../../../verification/check_links.py). It is not
restricted to tracked files. The suite's
[paper mathematics test](../../../../verification/test_paper_markdown.py)
checks only `paper.md`; the separate repository-wide math diagnostic reported
elsewhere is not this failed test. The relocation tests separately preserve
the existing evidence manifest and object identities.

## Exact baseline comparison

[The reconstructed receipt](links.json) records these three Git revisions:

| Revision | Markdown sources | Broken links | Affected source documents |
|---|---:|---:|---:|
| Base `13bca720c5e978928eee3cf155bd335fa4a099a1` | 1,224 | 2,214 | 164 |
| First publication `f28d760e16950b5417aa85b315fea61ab9bb1e1b` | 1,241 | 2,214 | 164 |
| Published head `6211f8fbe37a7f34a27354250be9b0d099bf7bb4` | 1,241 | 2,214 | 164 |

Every revision has **2,005 missing-target failures and 209 missing-anchor
failures**. The comparison maps exact unchanged source-line blocks from the
later revision back to the base, then matches each source, mapped line,
target and failure detail against a baseline occurrence. All 2,214 failures
match; no baseline failure disappears and no new failure appears.

The only failure originating in any of the six modified existing Markdown
documents is in `v3/README.md`, line 462 at the published head, corresponding
to unchanged base line 458. Its target is
`claim_ledger.md#p3-10-scientific-dispositions--october-11-2026` and its detail
is `heading anchor does not exist`. The link itself was not edited. There
are **zero failing links on changed lines** and **zero failing links in the
17 newly added s06 documents**.

The first-publication and later-head normalized failure inventories have the
same SHA256:
`1786d1c47dd1aa04c5f0c70906536530819a0106f77b64da82594d3d23006e80`.
The base inventory hash differs because the preserved README failure moves
four lines. The actual working checkout's link inventory also matched the
published head at the time of this check.

## Reproduce this limited check

[The publication helper](links.py) runs only the unchanged link checker.
From the checkout root, choose a new output path:

```sh
python v3/discovery/s06/pub/links.py /tmp/s06_links_again.json
```

The command refuses to overwrite an earlier report. It resolves the three
explicit Git revisions, verifies unchanged checker and relocation-admission
source bytes, and creates isolated temporary filesystem views. Markdown,
the relocation manifest, and referenced relocation objects contain their
exact Git blob bytes; other tracked regular files preserve existence only.
The trees contain no symlinks or submodules. This reproduces every content
and existence fact read by this particular checker without duplicating the
approximately 722–740 MB full trees. It does not substitute for executing a
semantic test against those placeholder files.

The helper preserves full normalized failure lists in the reported temporary
directory, while the portable receipt retains their hashes, counts, precise
changed-document failures and line mappings. The newly written publication
note is outside the three frozen revisions; a later working-tree scan may
therefore count an additional Markdown document while retaining the same
failure inventory. No historical link or archive was repaired during this
diagnosis, and the complete semantic suite was not rerun locally.
