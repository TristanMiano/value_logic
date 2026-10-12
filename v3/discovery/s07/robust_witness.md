# Ordinary persistent robust-witness proposals

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. Concurrent helper work adds no principal research-clock credit.

## Purpose and API

[robust_witness.py](robust_witness.py) makes a stronger conventional action
search available alongside the retained-witness evaluators. It searches the
original Boolean logical source for a repair minimizing the scalar-anchor
uniform-regret certificate. Future candidate and conventional controllers can
receive the same proposer, admitted evidence, observations, caps and retained
native state.

```python
engine = RobustWitness(instance, costs, meter)
got = engine.propose(costs, admitted_anchor_lowers, price,
                     seconds=0.1, nodes=1000)
if got['witness'] is not None:
    compact_bank.retain(row, got, purchase_id)
answer = ordinary_evaluator.evaluate(row, price, tolerance)
```

The public cost table, cohort, source identity and ordered objective features
are fixed at construction. Each call takes the current admitted row mode
sets and scalar lowers at the exact full-cohort anchors `N*mode[k]`. The
caller retains responsibility for those lower proofs. Defaults are **0.1
seconds and 1,000 MIP nodes**, with explicit smaller caps supported.

## Exact formulation

Let `x` be the original Boolean assignment and `z_j` its soft-clause violation
indicator. A literal's truth is `x_v` for a positive literal and `1-x_v` for
a negative literal. Hard clauses constrain their truth sums to be at least
one. For every soft clause `C_j`, the following Boolean constraints make its
violation indicator exact:

```text
z_j >= 1 - sum_(literal in C_j) truth(literal)
z_j <= 1 - truth(literal)               for every literal in C_j.
```

For each cost row `i`, introduce real epigraph variables `a_i,b_i`. With
`d_k=ell_k/N`, every currently possible mode gets both inequalities:

```text
a_i >= mode[k] dot z - d_k
b_i >= mode[k] dot z.
```

Minimize `t`, subject also to `t>=0`, `t>=sum_i a_i`, and
`t>=sum_i b_i-p`. For any fixed feasible Boolean assignment, minimizing its
epigraph variables gives **exactly the scalar-anchor fixed-repair bound**.
Consequently the exact mathematical MIP chooses the best bound among every
feasible repair on the source, including repairs absent from the current
bank. Replacement remains a separately available action in the ordinary
evaluator.

The formulation contains `n+m+2N+1` columns and
`|hard| + sum_j(1+|C_j|) + 2NK + 2` rows, where `K` is the public mode count.
It contains one epigraph constraint per row/mode possibility, rather than
enumerating all complete cohort mode assignments.

## Persistence and independent checking

All CNF, exact-violation and row/mode epigraph constraints are installed once.
Cost observations disable eliminated modes by relaxing their row bounds;
changed lower certificates and replacement prices update only right-hand
sides. The native HiGHS object, row/column identities and original Boolean
variables remain the same. Each call constructs and supplies a feasible MIP
start from the previous independently checked assignment, with epigraph
values updated for the current source and lowers. Internal branch-tree or
learned-cut persistence is not assumed.

The native formulation uses floating arithmetic. Its objective, dual bound
and termination status are recorded as guidance. A returned binary proposal
is separately checked against the **original hard clauses**, and its soft
violation mask is recomputed exactly and compared with the native binaries.
Only a passing witness is exportable. There is no exported negative proof or
regret certificate. The unchanged `RepairEvaluator` then supplies the actual
source-wide certificate from its admitted tree/scalar bank.

An incomplete search can still return a checked feasible witness, including
the previous one. `UNRESOLVED` is returned when no valid proposal survives
checking. Every executed call carries its setup/API/checking charges, native
termination details and measured CPU/wall time; a cap or repeated witness
does not erase the attempt's costs or imply progress.

The implementation uses the installed **HiGHS 1.11.0** API already employed
by [native_repair.py](../s06/native_repair.py), supplemented by its installed
method documentation. The saved evidence includes the new implementation,
checker, wrapper and native-module hashes.

## Constructed actual calls

Command: `python v3/discovery/s07/robust_witness_check.py`.
The [saved result](robust_witness_results.json) contains two declared sources,
their raw negative trees, original assignments, cost manifests, the actual
audit receipt, every native response, source states and invoices. Neither
source is the historical sixteen-request cohort.

| Source and stage | Before proposal | After retaining checked proposal | Proposed model | Native outcome |
|---|---:|---:|---:|---|
| Two-variable source, initial modes | 3 | **2** | 2 | Optimal status |
| Same source, zero time/node cap | 2 | 2 | 2, repeated | Time limit |
| Mixed soft clauses, weak admitted anchors | 13 | **8** | 2 | Optimal status |
| Same source, stronger raw-checked anchors | 6 | **4** | 5 | Optimal status |
| Same source, after an actual cost audit | 1 | 1 | 2, already retained | Optimal status |

The stronger raw proof is a separately performed admission: it reduces the
existing bank's bound from 8 to 6 before the next MIP call. The subsequent
call changes the preferred witness from model 2 to model 5 and reduces 6 to
4. The audit later reduces the existing bank to 1 before the final proposal;
that proposal produces no further reduction. These distinctions prevent
crediting proof work or observations to native action search.

The zero-cap call returns the earlier checked assignment while reporting a
time limit. It costs **169 named units** and provides no new bound reduction.
This illustrates the difference between a usable checked incumbent and a
completed optimization claim.

All **five** native proposals pass independent witness checks. Three improve
the then-current ordinary evaluator bound. The proposer setup costs **781
units**, and the five proposal API/checking invoices total **1,289 units**.
The complete constructed examples use **13,235 shared operation units** plus
**4 audit-provider software units** and one externally priced observation.
The post-call finite diagnostics cost a separate **1,813 units**. Native
search time is separately recorded; no operation or economic conversion is
assigned to it.

Only after all actual calls finish does the probe enumerate these tiny
sources. Every proposed repair attains the exact best scalar-anchor bound
in the enumerated cases, and every final action's observed worst regret is
within the ordinary evaluator's bound. Those finite diagnostics do not feed
selection or turn native status into a general optimality certificate.

The final audited case also shows the scope of the optimization target: its
best scalar repair bound is **3**, while the retained full tree certificate
gives the selected action a stronger bound of **1**. The proposer optimizes
the specified scalar surrogate; the ordinary evaluator can exploit additional
admitted structure. This construction strengthens future comparisons and
acquisition menus without supplying a candidate-specific superiority result.
