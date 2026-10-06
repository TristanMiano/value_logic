# F17 final report: bounded navigation and structure check

**Disposition: PASS_SCOPED. No actual defect found within this check.**

Reviewer: ChatGPT (GPT-6 Astra Pro), same-model internal review. Principal concurrent credit: **0 minutes**. No scientific execution or Gate D assessment occurred.

## Fixed inputs

| File | Bytes | SHA256 |
|---|---:|---|
| `paper_v2.md` | 90,361 | `18c45d7df537c6e8a076793c9e38412e5c8d887995ba041d2ee9cbf51971bc8d` |
| `v2/reporting/F17_v1/claim_map.json` | 92,113 | `53b1fe17adf46aaf4c6443efffe7bcad1f6d9f4451c0e3eed30556584ae28218` |
| `v2/reporting/F17_v1/references.bib` | 11,423 | `4c2fd6cac269d0c27fa8e30ca71fed94bc808481dfc2b36194b2db8628c700e4` |

## Findings

The check parsed all 104 inline Markdown links in the report's observed syntax: **47 local file links**, **31 same-document citation links**, and **26 external URLs**. Every local file or directory exists. The three local file fragments resolve to the corresponding plain-text ATX headings in the soundness acceptance record, F16 recovery derivation and case-study derivation. Those heading slugs are determinable under GFM. There are no duplicate report anchor IDs.

All **24 explicit reference anchors** are cited at least once; the report contains **31 citation uses**. The bibliography has the prescribed **24 unique keys in the expected order**, and its braces balance. This is a structural crosscheck against the previously reviewed reference mapping; it does not repeat the earlier primary-source metadata review.

The report has one balanced fenced code block and ten balanced inline code spans. All **311 inline math spans** and **37 display math spans** close. Their unescaped braces and the one explicit math environment balance. The report's numbered main sections run from 1 through 14, its equation tags from 1 through 25, and its theorem numbers from 1 through 5. The explicit editorial-marker scan found no `TODO`, `TBD`, `FIXME`, `XXX`, `PLACEHOLDER`, `TK`, `citation needed`, `INSERT HERE`, `draft note`, `editorial note` or `???` marker.

The claim map has **42 unique claim groups**, distributed as **19 mathematical, 14 empirical and 9 literature/contribution groups**. Group IDs agree with their three source fragments in order. Every group has evidence, and its report section, equation and theorem locators refer to existing numbered elements. Every path/SHA256 binding directly contained in the map matches: **145 binding occurrences across 83 unique files**. Supplied byte counts also match. These bindings include the canonical report, bibliography, tables, builder, fragment files, fixed reviews and per-claim evidence. The principal's existing map builder independently reproduced the saved map byte for byte with `--check`.

## Reproduction and records

Executed successfully using CPython **3.12.14**, from the repository root:

```bash
python v2/work_logs/F17_2026-10-06_S1/reviews/navigation/check_report_navigation.py
python -m v2.reporting.build_f17_claim_map --check
```

The [check script](check_report_navigation.py) uses only the Python standard library. Its [machine-readable result](result.json) includes all parsed links, code/math spans, reference mappings and individual evidence-binding checks. [Command records](commands.json) preserve the observed completion results. Both commands completed with exit code 0; no failed attempt or report edit occurred.

Check-script SHA256: `1a70e696732bd64a61a0e94101cc673925cf04b6d803594e9bd905bc85aa450d`.

Result SHA256: `00da6a58270924edf68444b325f3f57379e8195935069e81d5689ef4dcd0baeb`.

## Bounds of the disposition

This is a source-level navigation and structural check. It does **not** claim rendered GitHub, Markdown or PDF inspection; complete GFM/TeX parsing; external URL liveness; new source-content verification; renewed scientific tests; proof-assistant checking; or scientific/contribution acceptance. The math checks establish delimiter and environment balance, not successful KaTeX rendering or mathematical validity. The placeholder scan covers explicit markers and does not certify the absence of every possible editorial issue. The hash checks bind saved files; they do not re-establish the substantive claims made in those files. Root-owned current status pointers were left to the principal's separate reconciliation.
