# Checked native proof exports and reusable objective cuts

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**
The previously missing native negative-proof path is now executable:
an explicit weighted-budget CNF, a fresh Glucose3 proof export, an independent
strict RUP check, a freshly derived objective cut, and a separately paid
reusable projection of the accumulated checked cuts. The native IHS service
retains its existing resident state while this additional proof-producing
call supplies its own independently admitted evidence. A second construction
uses rational dual certificates to avoid enumerating all objective masks.

These are useful capability and representation developments. The existing
80-request fixture remains exposed, the implementations remain developmental,
and no material-positive verification or total-cost advantage is established.
This note synthesizes the already executed evidence; writing it makes no
additional solver calls and earns no concurrent principal-clock credit.

## 1. The actual admission chain

The implementation is [rup_bridge_v2.py](rup_bridge_v2.py), used by
[native_rup.py](native_rup.py). Its executed hashes and installed dependency
hashes are recorded in [rup_stream_results.json](rup_stream_results.json).

**First establish the objective's meaning.** For each original soft clause
`C_j`, the encoder introduces `z_j` equivalent to the clause being false.
It adds `z_j OR C_j` and, for every literal l in that clause,
`NOT z_j OR NOT l`. The original hard clauses remain premises. Stable source
identities bind variable meanings, hard clauses and ordered soft clauses;
each weight vector and bounded encoding has its own identity.

The budget `sum_j q_j z_j <= b` is encoded with explicit recursive threshold
nodes. For a suffix beginning at i, the node represents

```text
T(i,b) = if z_i then T(i+1,b-q_i) else T(i+1,b).
```

The terminal is false for a negative budget and true when the remaining
weight sum fits. Four CNF clauses implement each node's equivalence, and the
root is asserted. Constants, repeated literals and tautologies are simplified
explicitly. The receipt saves the original and weighted source IDs, ordered
violation variables, every auxiliary node and complete CNF. Current admission
requires nonnegative integer weights within the inherited native integer range.

**Then purchase and inspect a native export.** A fresh
`Glucose3(with_proof=True)` object is created before the full CNF is loaded.
No assumptions, unexported native cardinality constraints or external
propagators enter this proof call. It has separate conflict and propagation
caps. Native SAT supplies a candidate repair for original-source checking;
native UNSAT supplies raw proof bytes for checking. Neither status is itself
an admitted lower certificate. The supported installed configuration is
described in [the capability note](proof_cap_note.md), with the
[official PySAT API](https://pysathq.github.io/docs/html/api/solvers.html) as its
primary interface reference. The installed Glucose wrappers forbid combining
their optional `incr=True` mode with proof tracing.

**Independently check the proof and derive the cut.** `check_export` regenerates
the weighted encoding from the source and requires it to equal the receipt's
complete encoding. `check_rup` admits a clause only if negating that clause
and propagating the current admitted clauses produces a contradiction. It
requires an independently checked empty clause. Parsing, propagation, premise
admission and retained clause work are charged. Deletion instructions are
parsed and charged but ignored: every retained addition is already entailed
by the original CNF, so keeping it is sound for this restricted RUP check.

This is deliberately narrower than general DRAT. Heule's
[The DRAT format and DRAT-trim checker](https://arxiv.org/pdf/1610.06229),
particularly the clause-addition conditions on pp. 2–3, explains how RAT
extends the unit-propagation redundancy condition. The
[official DRAT-trim documentation](https://www.cs.utexas.edu/~marijn/drat-trim/)
also distinguishes the stronger RAT check and lists a RUP-only option.
Our checker rejects an unsupported non-RUP addition rather than treating a
generic DRAT log as an independently verified proof. DRAT-trim itself was not
installed or run for the reported checks.

Given a checked refutation of the justified budget encoding, the newly
constructed conclusion is

```text
q dot z >= b+1
```

for every feasible original-source violation vector. `check_export` constructs
this cut from the rechecked raw encoding/proof; it does not trust a serialized
`checked=True` flag, stored numeric lower or stored receipt ID. A new consumer
must repeat that admission or rely on an explicitly admitted earlier checker
receipt. The small Python encoding/checking kernel remains trusted software,
with finite checks and derivations rather than a formal correctness proof.

## 2. A missing empty line is a checked-completion duty

The v1 probe found a concrete exporter boundary: on a tiny negative budget
query, Glucose detected the contradiction during clause loading and returned
an empty proof list. The v1 checker correctly refused to admit a proof with
no checked empty clause. It did not turn native UNSAT into a trusted lower.
That attempt's four actual calls, including the unresolved capped call, remain
in [rup_check_results.json](rup_check_results.json), with its failure and
revision disposition in [rup_attempt_01.json](rup_attempt_01.json).

V2 preserves the raw export. If it lacks an explicit empty-clause line, the
checker proposes an additional empty clause and independently tests it by
RUP against the original admitted CNF and prior checked additions. It accepts
only if propagation really derives contradiction. The record distinguishes
the raw-proof hash from the admitted-proof hash and marks
`independent_empty_completion`. This is paid proof completion, not a fabricated
native export. The repaired stream uses this path twice in its requested-
tolerance arm and four times in its exact-completion arm.

[The v2 focused checks](rup_check_v2_results.json) cover twelve encoding/budget
configurations and 72 original-assignment extensions, including zero weights,
empty and tautological soft clauses, and threshold terminal cases. They also
recheck the earlier seven-byte native export, reject a non-RUP clause, a missing
empty clause and an unbound proof variable, and execute the four positive,
negative and capped source queries. Those four new calls give `UNSAT`, `SAT`,
`SAT`, `UNRESOLVED`. Altering the stored lower summary to budget 9999 does not
alter the freshly derived budget-1 cut. This is finite implementation evidence
for these obligations, not unrestricted verification.

## 3. Reusable supports are a paid projection of checked cuts

RUP proof lines do not automatically contain the old branching proof's leaf
masks. The new representation instead uses the separately established cuts.
If all feasible source violations satisfy `A z >= k`, define

```text
Z_cut = {z in {0,1}^m : A z >= k}.
L_cut(w) = min_(z in Z_cut) w dot z.
```

Every original feasible violation vector lies in this relaxed set, so
`L_cut(w) <= C*(w)`. For nonnegative w, componentwise dominated masks can be
removed without changing that lower function. `compile_cut_supports` enumerates
objective masks satisfying the admitted cuts and saves their minimal antichain.
This is objective-space relaxation work; it does not enumerate logical source
assignments or call an exact-optimum diagnostic.

The projection has its own operation meter and a default limit of **sixteen
soft features**. Its receipt identifies all the freshly admitted cut
dependencies. If projection is capped or unavailable, the service retains
the checked scalar cut but does not claim to have constructed reusable support.
The helper is an internal consumer of admitted cuts: passing it an arbitrary
saved `checked=True` object is not a substitute for raw admission.

The resulting support record fits the existing compact mask evaluator, which
both conventional controllers receive. The inherited JSON field
`retained_checked_trees` now counts old checked branching profiles **and these
new checked cut projections**; it must not be read as a count of native proofs
exported in the branching-tree format.

## 4. Persistent native integration and the complete stream

`native_rup.PersistentIHS` inherits the frozen resident MiniSat/HiGHS engine
from [native_repair.py](native_repair.py). The same SAT object and learned
clauses, stable enforcement literals, native IHS core rows, direct objective
updates and explicit previous hitting-set starts survive across requests.
The optional SAT `warm_start=True` mode remains disabled after the earlier
preserved assumption-model defect; returned models undergo the repaired
assumption and original-objective checks. No complete MIP branch-tree retention
or equivalence to an optimized iMaxHS implementation is claimed.

The Glucose proof object is fresh for every separately purchased bound. Its
raw proof and derived cuts are reusable evidence; its native search state is
not retained. Thus proof persistence and optimization persistence have distinct
implemented contracts.

Both paths first use the same initially admitted compact bank. When its
checked action gap exceeds tolerance, the requested path buys the existing
threshold `b=min(U,p)-tau-1`. The exact path completes native IHS and buys a
proof below the checked candidate's cost. Both keep their own new purchases.
The source order and five weight recipes are the existing exposed development
fixture, with p=6 and tau=1.

| Repaired RUP-backed stream | Requested tolerance | Exact completion |
|---|---:|---:|
| Checked actions | 80 | 80 |
| Closed from retained checked cache | 60 | 61 |
| New native IHS purchases | 20 | 19 |
| Native hitting-set solves | 60 | 76 |
| Native SAT solves | 45 | 76 |
| New separately paid Glucose proof calls | 15 | 19 |
| Retained native cores | 40 | 57 |
| Sum of returned action costs | 223 | 220 |
| Unresolved requested actions | 0 | 0 |
| Final serialized checked cache and DAG bytes | 13,787 | 15,378 |

The old independently checked branching-proof bridge remains valid. Its
earlier native stream closed 61/62 requests from cache versus this bridge's
60/61. The changed proof representation can lose useful structural information;
a compact export does not imply equally strong weight transport. The positive
result here is the supported native proof-to-service admission path.

## 5. Costs, including the composite adapter invoice

Each arm pays native source initialization, its own original-source witness
checks, native IHS work, weighted proof encoding, export checking, cut retention,
projection, compact evaluation and output work. The pointwise initial bank was
actually readmitted once for this execution, costing **92,969 declared units**.
The older **77,646-unit** source acquisition remains historical and common.

| New declared operations, excluding native search | Requested tolerance | Exact completion |
|---|---:|---:|
| Weighted proof CNF construction | 17,226 | 21,593 |
| Proof checking and repeated encoding admission | 101,453 | 144,808 |
| Native source admission and encoding setup | 3,408 | 3,408 |
| Base native adapter, updates, witnesses and cut references | 3,780 | 5,731 |
| Separately metered objective-cut projection | 82,508 | 101,907 |
| Compact service/controller operations | 9,380 | 10,084 |
| **Declared subtotal excluding native search** | **217,755** | **287,531** |

The response's `adapter_invoice` is composite. Its top-level `by_category`
and `operations` describe the **base** native adapter. The separate nested
`projection` meter is added once to its `total`:

```text
requested: 3,780 + 82,508 = 86,288
exact:     5,731 + 101,907 = 107,638
```

Those totals are the stream's `new_purchase_adapter_units`. The projection
must not be added a second time to the arm total, and the base categories
alone do not reconstruct the composite total. The replay explicitly checks
this accounting identity for every purchase.

Native search is not converted into the declared operation tariff. Actual
IHS native-search wall time was about **177.618 ms / 279.999 ms**, and the
additional proof-call creation/loading/search/export wall time was
**4.043 ms / 4.700 ms**. Whole-arm wall time was **346.323 ms / 469.277 ms**.
Detailed process times, native conflicts/propagations/decisions and MIP nodes
are retained separately. These single ordered executions have different startup
conditions and do not establish a runtime ranking. The short raw exports—692
and 836 bytes summed over the respective proof calls—do not include encoded
CNF, wrapper records or projection costs.

The explicit proof caps cover encoding/checking operations, positive native
conflict/propagation budgets, admitted proof size and objective projection.
The inherited `proof_units` caps each applicable encoding/checking allocation;
it is not a monetary cap on their sum or on native work. Proof-size admission
is checked after export, so it does not promise a hard peak-memory cap.
Native host memory and total economic cost remain unmeasured. Final serialization
and publication are additional work. On this fixture, the new declared subtotal
is higher than the finite branching bridge's subtotal; no net savings claim is
made from replacing that provider.

## 6. A new consumer reconstructed every returned action

[rup_replay_results.json](rup_replay_results.json) reports an actual fresh
admission of the old bank, every used raw weighted encoding/RUP export, every
new witness and each successive projection from that arm's own rederived cuts.
It then reconstructs all 160 action gates, chosen actions and stated costs.

| Independent-of-search replay duty | Requested arm | Exact arm |
|---|---:|---:|
| Raw RUP proofs rechecked and cuts freshly derived | 15 | 19 |
| New witnesses checked | 5 | 19 |
| Resident predecessor links checked | 8 | 7 |
| Requested action gates reconstructed | 80 | 80 |

This replay made **zero new native calls, zero branching-provider calls and
zero cost observations**. Its archive/readmission/projection/gate invoice is
**740,129 units**, additional to its separately recorded **92,969-unit** initial
bank readmission. It supplies checker-relative reconstruction of this stream,
not new source acquisition or formal verification. Historical search invoices
are neither rerun nor counted as new search during that replay.

## 7. Rational dual receipts provide another representation

The projection is exponential in soft-feature count. The further construction
in [cut_dual_derivation.md](cut_dual_derivation.md) and
[cut_dual.py](cut_dual.py) supplies a second route from the same independently
admitted cuts. For any nonnegative rational multiplier vector lambda, let
`a=A^T lambda` and `K=k^T lambda`. Every feasible `0<=z<=1` satisfies

```text
w dot z >= K - sum_j max(a_j-w_j,0).
```

The argument combines `a dot z>=K` with the coordinate bounds on z. An LP may
propose lambda, but the receipt converts it to exact nonnegative rationals
and recomputes a and K. Its validity requires no trusted LP optimum status
or floating-point dual feasibility. For the implemented nonnegative objectives
the bound can also be clipped at zero; integer objectives permit exact upward
rounding. A saved multiplier supports new weight queries without another LP
call when its cut dependencies remain admitted.

For a checked fixed repair mask u and warranted coordinate enclosure
`lo<=w<=hi`, the shared weights in action and lower costs give the uniform
contrast bound

```text
-K + sum_(j:u_j=1) max(hi_j,a_j)
   + sum_(j:u_j=0) max(0,a_j-lo_j).
```

Combine it with the repair's worst-case cost minus replacement price and zero.
The replacement bound is `max(0,p-K+sum_j max(a_j-lo_j,0))`. Evaluation is
linear in the feature count once a multiplier is admitted. It may be weaker
than the Boolean antichain or a method using more dependence information
about W; an insufficient bound leaves the action unresolved.

[cut_dual_results.json](cut_dual_results.json) is a **retrospective query
rehearsal on each completed arm's final own cut bank**, rather than a new
historical controller trace. Each source keeps one continuous HiGHS model
while its five objective recipes change. Raw proof admission, continuous rows,
objective updates, new LP proposals and exact certificate arithmetic are paid.

| Retrospective final-bank duty | Requested arm's bank | Exact arm's bank |
|---|---:|---:|
| Sources with acquired cuts | 9 | 12 |
| New paid LP calls | 45 | 60 |
| Integer dual lower equal to Boolean cut-projection lower | 38/45 | 58/60 |
| Fixed-action tolerance-one certificates obtained | 35/45 | 48/60 |
| Declared rehearsal units | 123,500 | 175,281 |

The rehearsal makes **zero new SAT, IHS or proof calls**, but its **105 LP
calls are new computation**. Its initial bank admission is also separate.
The comparison lower is the exact Boolean **cut relaxation**, not an original
source optimum diagnostic. The executed box evaluations are singleton supplied
weight vectors; the general uniform-box guarantee comes from the displayed
derivation, not from claiming that these queries tested uncertain-source
coverage. No controller rollout or cost-audit policy was executed by this
retrospective rehearsal.

## Next constructive move

The native proof-export capability is now concrete. A useful next integration
can choose among cheap retained dual evaluation, further paid logical evidence,
and paid observations that tighten a justified common weight-confidence set.
It should buy Boolean projection only when the needed precision and anticipated
reuse justify it. Give conventional controllers the same checked cuts,
representations, observations, native warm state and requested action tolerance.
The remaining question is which paid acquisition closes a meaningful calibrated
repair duty—not whether a native solver can merely label its optimum.
