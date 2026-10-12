# One admitted repair-service evaluator

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; same-model construction and focused semantic probe. Concurrent
helper work adds no time to the principal's research clock.

## Construction and admission boundary

[repair_interface.py](repair_interface.py) gives both proposed and conventional
controllers one callable interface over a live s06 `CompactBank` and
`CostState`. Its default menu combines the existing joint tree certificate
with full-cohort scalar-anchor transport. Raw-checked rational cut duals and
capped grouped-hull certificates are optional methods, with their actual
construction and query costs charged. No evaluator starts a solver or performs
logical-model or Boolean-mask enumeration.

The source consists of fixed hard/soft clauses, their ordered violation
features, a fixed finite cohort, public nonnegative integral cost modes and
the currently possible modes of each identified cost row. The evaluator
checks source bindings, rejects empty or foreign cost states, and **actually
checks each newly encountered candidate assignment** against its logical
instance. Replacement is another fixed action with public nonnegative price.

Compact tree masks require actual upstream raw-proof checking, such as
`native_stream.admit_existing_cache()` followed by checked complete-call
retention. The interface cannot recheck missing raw trees from their masks;
its declared internal admission boundary does not treat a receipt ID or
`checked=True` as proof. It rejects a previously bound tree ID whose masks
change. New duals have a stronger local entry point: `admit_cut_dual` checks
the supplied original RUP exports and reconstructs the nonnegative rational
combination itself. A saved LP status, scalar optimum or dual dictionary is
not accepted as an alternative entry point.

## Why the combined bound is valid

Write `C*(w)` for the minimum repair cost on the fixed logical source. A
checked tree supplies `min_z w·z <= C*(w)` over its covering leaf supports.
For each public mode `m_k`, the evaluator computes the strongest available
scalar lower `ell_k <= C*(N m_k)` from this profile's own admitted trees and
any actually admitted duals. These values are compiled once per evidence
state, with their selected proof IDs and exact objective vectors retained.
They are not borrowed from another policy's completed run.

For compatible row modes `h_1,...,h_N`, the cohort weight is
`w = (1/N) sum_i N m_(h_i)`. Concavity of the **true minimum** `C*` yields
`C*(w) >= sum_i ell_(h_i)/N`. For a fixed checked repair mask `u`, its regret
against repair-or-replacement therefore has the uniform bound

```text
max(0,
    sum_i max_(k in Q_i) [u·m_k - ell_k/N],
    sum_i max_(k in Q_i) u·m_k - p).
```

For replacement the bound is
`max(0, p - sum_i min_(k in Q_i) ell_k/N)`. These are the existing
[scalar-anchor formulas](../s06/source_anchor.py), now integrated with the
same source, feasible-action bank and meter as the tree evaluator. Taking
the smallest valid method/action bound selects one fixed action for the
surviving source; it does not choose that action after seeing an unobserved
outcome.

The optional dual-box path evaluates an independently admitted dual over a
warranted coordinate enclosure. The optional hull path constructs the exact
grouped cohort hull when its declared generator cap permits; each generator
gets a valid scalar lower, possibly using a different checked proof. A fixed
action's **true regret** is convex in weights, so its maximum at those
generators bounds the hull. Neither argument assumes the clamped dual
surrogate is concave. The nonnegative domain and integral-only ceiling
restriction in the [binding s06 review](../s06/source_anchor_review.md) are
enforced.

Default tree and scalar-anchor queries are monotone under mode-set refinement
with fixed evidence. A newly compiled hull query can be weaker than an older
hull certificate on its subsource because different pointwise lower proofs
need not interpolate tightly. A controller requiring monotone retention of
optional hull results should keep a previous fixed-action certificate when
its covered source contains the new one. This module makes no monotonicity
promise for a newly recomputed hull certificate.

## API

```python
from repair_interface import RepairEvaluator

service = RepairEvaluator(instances, compact_bank, cost_state, meter)
answer = service.evaluate(row, price, tolerance,
                          costs=outcome_branch_or_current_state,
                          methods=('tree', 'scalar_anchor'), hull_cap=256)
lowers = service.mode_anchor_lowers(row, costs=cost_state)
dual = service.admit_cut_dual(row, raw_exports, exact_multipliers)
```

`service(...)` aliases `evaluate(...)`. Every branch must retain the same
cost source, cohort, ordered modes and meter. The answer includes the chosen
action/model/mask/witness, its uniform `bound`, source and receipt IDs,
per-method answers and bounds, explicit optional-method unavailability, and
incremental/cumulative operation units. `status='unresolved'` means the valid
bound exceeds the requested tolerance; it does not invalidate the bound.
No available method is silently substituted by an unsupported zero lower or
zero regret. If every requested method is unavailable, the call raises.
Exact fractions need the caller's normal lossless serializer.

Each controller pays its own source/witness admission, evidence projection
checks, scalar compilation, support queries, optional hull/dual work and
method selection. Initial raw-tree checking remains a separately reported
upstream charge. Named operation units are not a conversion for native
CPU/wall time, memory, external observations or complete economic cost.

## Focused check

Command: `python v3/discovery/s07/repair_interface_check.py`.
The [saved result](repair_interface_results.json) preserves its source,
hand-constructed raw proofs, raw RUP export, code hashes and both invoices.
It checks a new two-variable source requiring at least one violated feature,
two public cost modes and two distinct cost rows. Across all **18** declared
price/refinement cases, **72** tree/scalar/dual/hull bounds contain the selected
action's exact worst regret. The diagnostic enumerations run after evaluator
selection and never feed its gate.

The probe also verifies seven source/domain/admission rejections, capped-hull
fallback, scalar compilation reuse, and cache invalidation after a second
independently checked tree enters the live bank. It uses **11,102** named
interface/checking units plus **1,837** separately invoiced diagnostic units,
with **zero new LP, SAT, IHS, proof-search or audit calls**. This establishes
the enumerated integration semantics and boundary behavior. It supplies no
transfer result, economic superiority claim or independent confirmation.
