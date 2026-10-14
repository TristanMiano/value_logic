# External-source paid service: development findings

**Codex (GPT-6), October 14, 2026. Not confirmation.**

All 96 ds01 stream/arm executions completed on the first attempt: 12,288
outputs, 12,526 purchased receipts, 96 actual source-diagram compilations.
Each arm has 2,048 outputs over eight SATLIB sources and two tolerances.
The synthetic paired-cost law, source-informed tolerances, exact action search,
relevant-coordinate fallback and complete accounting scope are in ds01.md.

| Arm | Audit fees | Counted units incl. setup | Setup units | Fallbacks |
| --- | ---: | ---: | ---: | ---: |
| Marginal / ordinary mirror (each) | 7,660 | 18,907,750 | 11,702,248 | 750 |
| Response-by-response scan | 7,660 | 46,671,972 | 11,702,248 | 750 |
| Fixed threshold order | 3,721 | 15,824,323 | 11,723,568 | 180 |
| Relevance-aware audit | 16,128 | 14,006,516 | 9,913,076 | 2,048 |
| Reoptimize action after every audit | 6,804 | 206,911,004 | 11,702,248 | 640 |

The marginal calculation exactly matches all 4,096 ordinary-mirror/response-scan
outputs, queries and costs. It saves 59.49% counted units versus separate
response scans. The ordinary mirror ties it. The cheaper threshold policy has
both lower fees and lower counts than that candidate. Threshold saves 76.93%
fees versus relevant full auditing but costs 12.98% more named computation.
Global action reselection often lowers fees but its naive exhaustive repeated
implementation is expensive. These results support further reuse and planning;
they do not establish a win over strong ordinary methods.

The first three read-only check attempts failed at different proof hash checks.
A fourth with Node --jitless exited -1073741819. The instrumented fifth passed
all checks, including exhaustive 2^20 truth-table reconstruction of each source,
direct interval-regret verification, 336 negative controls and receipt replay.
Independent Python then verified all proof body and 12,526 receipt bindings.
One proof file was written under an incorrect hash-derived filename although its
body and internal binding match an otherwise identical correctly named object.
Preserve both and resolve the original references using
ds01/bindings_manifest.json. Do not silently rename/rewrite executed evidence.
The cause of the transient failures is unproven; host instability is possible.
Failed diagnostic work has unknown full bills and is not hidden by the passing
attempt. None of these retries purchased additional physical information.
