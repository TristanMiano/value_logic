# Next service: buy the remaining repair-action precision

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT design; no new backend was installed or run for this note.
Start with the [compact profiles and invoices](reprice_compact_results.json),
[action-profile derivation](repair_profiles.md), and
[persistent-MaxSAT source bridge](reprice_sources.md).

**Subsequent development in this increment:** the existing finite provider has
now executed the complete stream, in [the paid stream and corrected replay](repair_stream_v2_findings.md).
Full profile reuse closes 61 requests from accumulated evidence and completes
the other 19 with checked calls; all 80 requested tolerances are met. The
standalone setup sensitivity removes the small common-cache cost lead. This
completes a finite integration step, while the production persistent backend
and its checked receipt path remain open.

The strongest next generative extension is now [calibrated repair](calibrated_repair.md):
choose between paid cost observations and logical search to admit a useful
action. The native adapter below is an engineering route toward that service,
not a requirement to spend the next recurrence solely replaying the old fixture.

## One coherent mechanism

Build a persistent repair-or-replace service which first evaluates its checked
receipt cache under the requested weights, then purchases only the precision
still needed for the requested action. A request specifies source, weights w,
replacement price p, allowed regret tau, and a spending cap. Checked bounds
L<=C*(w)<=U certify the retained action when

```text
min(U,p) - min(L,p) <= tau.
```

This is a concrete useful contract even when the optimum is unknown. Use the
retained repair attaining U when U<p; otherwise replace. Returning an unresolved
interval after the cap is a distinct outcome, with the best available action
and its explicit regret bound. Preserve all paid work across the next request.

The same compact evaluator, receipts, objective passes, subset reductions and
stopping rule must be available to the conventional controls. Therefore cache
hits are a shared service improvement; they do not by themselves establish a
new acquisition-policy advantage.

## A concrete first stream and actual costs to measure

Use the existing sixteen sources and five weight recipes, in their saved order,
with p=6 and tau=1. The current cache already certifies **55 of 80 row-edits**.
The remaining rows, before any new acquisition, are:

| Weight recipe | Rows still requiring precision |
|---|---|
| Identity | None |
| Uniform doubling | 1, 2, 3, 4, 7, 9, 10, 11, 14 |
| Double first half | 1, 2, 3, 4, 7, 10 |
| Zero last half | 13 |
| Rotate right | 1, 2, 3, 4, 7, 8, 10, 14, 15 |

These are zero-based source IDs, derived only from the saved interval profiles.
All 80 requests remain in the ledger; the 25 residual requests are not a sample
selected using new optimum labels. As new evidence accumulates, some later
residual requests may become cache hits. The strengthened scalar cache initially
certifies 51 requests, so merely comparing against that cache would omit useful
proof reuse available to an informed conventional controller.

Charge instance/encoding initialization, objective updates, profile evaluation,
new search, witness passes, negative-proof checking, interrupted work and retained
memory. Measure CPU/wall time alongside explicit service counts; do not convert
the earlier DPLL operation tariff into a supposed production-solver runtime.
The five recipes are an exposed integration fixture, not fresh validation data.

## Persistent IHS/IPAMIR is the starting baseline

Rechecked primary locators: Niskanen, Berg and Jarvisalo, CP 2021,
[Algorithm 2 and Sections 4.1–4.3](https://doi.org/10.4230/LIPIcs.CP.2021.44),
pp. 44:7–44:11. Their IHS method retains cores across weight changes and reprices
the previous model; objective-dependent simplification requires care. Preserve
the solver object and supported internal reuse. The baseline is not a restarted
optimizer for every new weight vector.

Also rechecked the authors' SAT 2022
[Section 4 and Figure 1](https://doi.org/10.4230/LIPIcs.SAT.2022.14), pp. 14:4–14:5.
IPAMIR provides weight updates, assumptions, termination, objective and model
access. The paper's status codes are 0 interrupted without a new model,
10 UNSAT, 20 feasible SAT, 30 optimal, and 40 error/unsupported. Verify the
actual selected implementation; do not substitute IPASIR's numeric meanings.
Figure 1 does not specify independent lower-bound or proof export.

Maintain two strong conventional execution paths: persistent IHS completing
optimization when needed, and the same persistent engine stopping at the
requested action tolerance whenever its supported bound interface permits.
Both first consume identical cache evidence and may avoid solving completely.
Exact optimization also buys evidence valuable to later requests; retain that
benefit in its cumulative bill. A cold run may be informative but is not the
main comparison.

## Adapter contract and the one capability to make concrete

The proposed service boundary is:

```text
request:
  request_id, source_id, weight_id, weights, price, regret_tolerance,
  service_cap, archive_snapshot_id
response:
  status: checked_action | unresolved | source_mismatch
  lower, upper, action_kind, witness_id, certified_action_regret
  receipt_dependencies, archive_snapshot_after, solver_state_id
  invoice: admission, encoding, weights, profile, search, checking, storage
  timings, backend_status, backend_version
```

Keep backend status separate from checked status. Independently validate every
returned repair against the original hard clauses and compute its true objective
once. A feasible backend result can improve U even after interruption. A claimed
optimal status alone does not enter the checked lower-bound bank.

For integer costs, when the action gap exceeds tau, a useful bounded query is
`exists feasible x with cost_w(x) <= b`, where `b=min(U,p)-tau-1`.
A checked negative answer gives L>=b+1 and closes this requested gap; a returned
model improves the relevant upper cost. This is the existing conventional
threshold rule from the repair probe, not a newly named policy. Expose the same
query option to every controller.

A real adapter must now identify its paid certificate path: either a backend
export/checker for the required lower bound, or a separately billed proof-capable
bounded-decision call. Guard changing weighted-budget encodings and bind their
proofs to the exact weight vector and assumptions. A generic UNSAT log or core
does not automatically become the old DPLL source's complete branching tree.
Only a supported checked bridge may add new reusable leaf profiles. Until that
bridge exists, new checked scalar bounds and witnesses remain useful at their
declared scope, and existing tree profiles remain usable under the established
weight-only transport rule.

## Reuse, compilation, and the next hour's deliverable

Every controller starts with the same archive and has unrestricted access to
the same compression/checking code. Its own new purchases are charged and its
own receipts persist. If replaying an additional common receipt bank, disclose
the acquisition cost as common to all arms; do not give one run unbilled future
results from another. No private learned prior or optimum diagnostic is needed
for this first finite request stream.

The cache now exists: consume it directly. If the adapter instead starts with
raw profiles in a fresh epoch, the existing
[compile policy](compile_policy.md) gives an explicit rent-or-buy option.
Its fourth-edit purchase costs 22,271 over the exposed five-edit prefix, versus
19,390 always raw and 17,678 always compact. Do not present the online guarantee
as a short-prefix measured win or force recompilation of an available cache.

The next increment should produce one runnable adapter, its pinned capability
record, the complete 80-request event/invoice trace, and a comparison of total
cost at the same checked regret target. Report requests closed before solving,
additional certificates, actual action costs, unresolved counts and memory.
If the backend lacks a required proof function, keep building the callable
witness/update service and make the missing negative-receipt boundary explicit;
do not rename trusted solver statuses as checked results. Expand to one concrete
repair workload after that boundary works. This keeps the next recurrence on
an executable value service rather than another broad screening campaign.
