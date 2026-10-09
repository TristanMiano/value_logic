# R-P3-B-A service implementation and focused verification

Contributor: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-09 UTC.
Separate same-model, nonblind implementation assignment.
Stage: **DEVELOPMENT**. Reviewer work contributes zero principal clock credit.

## Current source and interface

The implemented source is
[`07_selective_feedback_service.py`](../../../../checks/07_selective_feedback_service.py),
version `r-p3ba-euler-services-v1.2`, SHA-256
`68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32`.
It implements the prospective [contract v1](../../development/contract_v1.json)
and the existing 248-query mathematical family. It contains no learner and no
evaluator-provided answer table.

| API | Returned service |
|---|---|
| `make_query(p, a, query_id)` | Immutable public `A.Query`, with the complete modular claim and source/semantics identity. It computes no answer. |
| `expert_predictions(query, meter)` | Four stateless binary predictions: constant zero, constant one, odd base, and base below half the modulus. Uses only public inputs and charges the supplied compatible meter. |
| `checked_purchase(query)` | Cold old-adapter solve/check/acquisition. A successful result has `status="success"`, `checked=True`, and binds both the full claim key and request identity. |
| `direct_exact(query)` | Efficient ordinary binary modular exponentiation and terminal action. No mandatory second checker; `checked=False`. |
| `ExactCache(capacity=248)` | Empty bounded semantic-residue cache. Misses use direct computation; warm hits reuse the same mathematical key under a fresh request identifier. Capacity 0–248 is explicit, with FIFO replacement. |
| `QuadraticResidueTable()` | Paid prime checks and 124 square/reduce evaluations construct exact membership tables. Uses six separate 64-bit bitset words. Lookup returns an ordinary exact action. |
| `registry_setup(source_paths=...)` | Charges one explicit list/tuple of actual dependency files for path admission, source reading, hashing and retained identities. It is separate from object/answer costs. |

Results and resource records are frozen dataclasses with immutable tuple fields.
`ResourceRecord.record()` exposes total, category totals and named operations
as ordinary JSON-compatible data. Its construction and serialization are
external instrumentation. Direct, cached and table answers are exact local
computations, but are not falsely labelled as independently checked purchase
receipts.

The caller can reserve these conservative successful-call caps:

| Operation | Admitted cap | Largest observed actual debit over all 248 keys |
|---|---:|---:|
| Family admission | 64 | 31 |
| Four expert predictions including admission | 73 | 40 |
| Cold checked purchase | 1,088 | 300 |
| Direct exact answer | 512 | 91 |

The checked cap is 64 family-admission units plus the existing source-bound
1,024-unit cold core cap. Separate local meters preserve the old core boundary.
The caller absorbs actual debits, not the reserved maximum. Non-successful
answer calls expose no answer or residue and retain already spent costs.
Failed registry/object construction raises `ServiceSetupError` carrying those
resources. No pending cold state is reused after a failed purchase.

## Verification and exact resource findings

The final [run 003](service_probe_run_003/result.json) passes the new-service
correctness checks on every admitted mathematical key. Checked purchase,
direct computation, cold cache and table agree with an external private
Python modular-power check. A second cache pass changes request identifiers
and verifies reuse without direct arithmetic. The probe also checks request
and claim binding, source/family rejection, denied spending, FIFO replacement,
zero cache capacity, immutable results, 64-bit table words and registry sums.

No previous experiment was rerun. These three saved runs are successive
source/tariff revisions of this one new correctness probe, not independent
learning populations. Private diagnostic labels in `domain_checks.json` are
not inputs to the service or to the proposed learner.

| Operation across all 248 distinct keys | Actual abstract units, excluding standalone registry/setup |
|---|---:|
| Checked cold purchases | 70,096 |
| Direct exact answers | 21,446 |
| Exact table lookups | 9,862 |
| Cache misses/direct computations | 25,166 |
| Warm cache lookups, fresh request IDs | 9,366 |
| Four expert predictions | 9,614 |

Table construction adds **1,611** units; empty full-capacity cache setup adds
**503**. For example, at a common unit price, table construction plus one
complete 248-query pass uses 11,473 units, compared with 21,446 for direct
computation. This is a statement about the implemented source-bound tariff.
Different category prices use the retained category vectors; physical runtime
and the cheapest conceivable implementation are not inferred from these
counts. The caller must add each method's actual source closure once and its
own remaining policy work. The table constructor's mathematical proof and
source selection remain supplied research, just as the learner's algorithm
and proof are supplied.

The table and warm cache comparisons matter because computing the four cheap
experts already costs almost as much as an exact table lookup. Weighting,
sampling, updates and paid feedback add further costs to the learner. This
does not decide the principal's full comparison before its actual scope and
prices are applied, but prevents treating avoided checked purchases alone as
net learning value.

## Revision disposition

- **v1 / run 001:** all mathematical and binding checks passed. The table's
  inferred negative residue subtraction needed its own explicit tariff entry.
- **v1.1 / run 002:** added that subtraction charge and required an explicit
  bounded source list/tuple. It adds exactly one table unit per query.
- **v1.2 / run 003:** adds the caller-visible `EXPERT_EVALUATION_CAP=73` and
  its exhaustive admitted-domain check. Mathematical outputs and per-answer
  tariffs are unchanged from v1.1.

The earlier new-service source versions and probe sources are preserved in
`service_v1_snapshot` and `service_v1_1_snapshot`. Their result files retain
their own exact hashes. The old P3-06/P3-07 source files remain unchanged.
The current manifest is [implementation_bindings.json](implementation_bindings.json).
