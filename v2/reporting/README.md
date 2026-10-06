# Report evidence versions

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 6, 2026 UTC.

The canonical research report is [`paper_v2.md`](../../paper_v2.md).
Its current evidence map is [`D_1/claim_map.json`](D_1/claim_map.json), created
for the reviewed rendering, attribution and statement-precision revision.
From the repository root, verify it with:

```bash
python v2/reporting/build_gate_d_report.py --check
```

The data tables and bibliography remain the unchanged F17 exports:
[`F17_v1/tables.json`](F17_v1/tables.json) and
[`F17_v1/references.bib`](F17_v1/references.bib). Their table check is:

```bash
python v2/reporting/build_f17_tables.py --check
```

## Historical F17 binding

`F17_v1/claim_map.json`, its builder, manifest and reviews describe the report
at commit `f7aa0bef07cb21da9336429426244f6e944644a4`, with report SHA256
`18c45d7df537c6e8a076793c9e38412e5c8d887995ba041d2ee9cbf51971bc8d`.
An identical [saved snapshot](../work_logs/F17_2026-10-06_S1/drafts/report_v2.md)
remains in the repository. The F17 builder intentionally refuses a changed
canonical report: run that historical builder in a checkout of its pinned
commit when reproducing the original assembly.

The D builder instead verifies all 145 original evidence bindings, resolving
the historical canonical report pointer to the saved F17 snapshot, and binds
the revised report to its new reviews. Of the 42 claim groups, one has an
explicit hypothesis clarification; the other 41 and all original supporting
evidence transfer unchanged. No old review or manifest is silently rewritten.

These checks read saved material. They never train a model, generate a
population, refit an alignment or rerun the frozen experimental stages.
