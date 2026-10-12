# Checking links in preserved research documents

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026.
Repository maintenance only; no research-clock credit.

The repository keeps reviewed manuscripts, partial draft excerpts and earlier
versions as evidence. Their bytes and scientific manifests remain preserved.
The link checker now distinguishes their **document source namespace** from
their later storage directory, using explicit content-bound provenance in
[document_origins.json](../tools/document_origins.json). It still checks every
local destination and Markdown fragment that it extracts.

Run the focused gate from the checkout root:

```bash
python -m unittest verification.test_links verification.test_archive_origins -v
```

For the standalone repository link report:

```bash
python -m verification.check_links
```

## What was repaired

The initial run reported 2,214 broken links: 2,005 missing paths and 209 missing
heading anchors. Most were valid references copied into partial evidence
directories without the referenced sibling files. The parser also missed
custom HTML anchors, collapsed the multiple hyphens in GitHub heading slugs,
and mistook three code or mathematical expressions for links. These were
checker and archive-context problems; they did not require rewriting the
research records.

The parser now recognizes the repository's automatic headings and explicit
HTML `id`/anchor `name` attributes, including case-sensitive custom identifiers
and heading-name collisions. It masks code and mathematical spans before
extracting prose links, while preserving offsets for useful line numbers.
These behaviors are covered by focused regression tests. The relevant primary
references are GitHub's
[link and custom-anchor documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
and the original [GitHub slugger project](https://github.com/Flet/github-slugger).
The checker is a repository Markdown checker, not a full browser renderer or
an external-URL availability service.

## How an archived namespace is admitted

[archive_origins.py](../verification/archive_origins.py) loads the explicit
registry. There is no fallback that searches for a similarly named file, no
rule that ignores `work_logs` or `source` directories, and no accepted list of
broken targets. An unregistered copy uses its physical path and can fail the
gate normally.

Each entry binds the stored file's current SHA-256 and its original
repository-relative document path. The loader verifies the bytes of every
provenance record before following its JSON selectors. Most entries use a
capture manifest that directly associates the original path with the exact
archived digest. Other entries need their more specific historical contract:

| Evidence form | What it establishes |
| --- | --- |
| Exact capture record | The original path and archived bytes were recorded together. |
| Separate fields in one capture record | The original path, named snapshot and digest retain their documented association. |
| Reviewed excerpt context | Recorded source and excerpt identities, together with the pinned review passage, identify the excerpt's source document. This is not whole-file equality. |
| Historical presentation transformation | The original capture digest reaches the current archived digest through every recorded before/after step. |
| Individually captured source-tree document | The inventory binds the complete stored path and digest, and the pinned review identifies the named file as a captured live-source document. This does not authorize a directory-wide inference. |

The registry has 136 document entries. Its source-context entries retain an
explicit interpretive boundary: hashes establish the identity of the reviewed
passage, while the passage supplies the relationship between the excerpt and
its source. A checksum alone cannot establish that relationship. The current
registrations were reviewed against their existing capture, assembly and
review records. None asserts that the latest live source must still equal its
earlier copy.

The five older paper drafts illustrate why both identities matter. Their
entry hashes precede two historical mathematical-presentation transformations.
The existing `portable_math_repair.json` and `protected_math_repair.json`
records connect those hashes to the current files. The loader checks the
complete chains instead of treating an old receipt as a match for different
bytes.

## Relative paths, fragments and historical checkout links

For an admitted copy, a relative file reference uses the original document's
parent directory. The target must actually exist, or resolve through the
separately verified [evidence relocation manifest](../v3/evidence/relocations.v1.json).
A target fragment must exist in the resolved Markdown content. A missing or
tampered relocated object still fails.

A self-fragment normally belongs to the archived content itself. The registry
contains one explicit assembly exception: the partial `core_v1.md` paper draft
references bibliography entry `ref-chain` in its documented complete paper.
Only that fragment uses the assembled paper; all its other self-fragments
remain checked against the archived draft. The complete paper must contain
the actual bibliography anchor.

Nine exact saved review files contain absolute `sandbox:` links from an old
checkout. Their accepted prefix comes from a hash-bound command-start receipt's
observed `cwd`. Compatibility is restricted to those nine source digests and
that recorded prefix. The checker strips the admitted checkout prefix, then
checks the real repository target and fragment. It does not treat arbitrary
`sandbox:` URLs as external links to skip.

One preserved `observable_before.md` review copy contains a heading fragment
that its existing prose-correction receipt already replaced. The live
literature file is also bound by scientific and preservation receipts, so
neither raw file was edited. A single source/target-specific correction uses
the receipt's exact old-to-new fragment substitution. It requires the exact
before-copy digest and the correct original source path, cannot redirect the
file path, and still checks that the replacement anchor exists.

## Source validation and portable navigation

Checking an immutable copy in its original source namespace does **not**
rewrite the links physically rendered by GitHub in that copy. The same is true
of the one preserved old fragment and the historical checkout links. The
registry is an explicit interpretation of archived references, not a claim
that those raw storage locations are standalone navigable documents.

The portable mathematical views use the same verified namespaces and
corrections when producing actual links at their new locations. Their separate
view identity and deterministic-transformation checks preserve the raw-source
admission chain. Consumers should use those views when available, the original
source namespace, or the evidence relocation resolver when reading a preserved
archive directly.

Focused tests reject changed source bytes, changed provenance bytes,
unrelated but rehashed source records, unsafe or duplicate paths, incomplete
transformation chains, missing review passages, unregistered copies, unknown
historical checkout scopes, nonexistent target anchors and attempted path
redirection through an anchor correction. Repository-wide link validation
remains part of the normal `python -m verification` gate.
