# A callable persistent native repair service with a paid proof boundary

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**
This implements the useful engineering step left open in
[s05's service direction](../s05/repair_service_next.md). It connects an existing
checked compact witness/proof bank, objective changes, actual persistent native
IHS calls, and independently certified repair actions. It does not establish
material-positive verification, a new optimization method, or a total-cost lead.

## What is now callable

`native_repair.py` exposes `PersistentIHS(instance)` and
`purchase(weights, budget, limits=None, exact=False)`. Importing the module does
not run the fixture. Source IDs bind variable count, original hard clauses,
soft-clause order and meanings; each weighted instance and weight vector also
has its own ID. The current native interface accepts nonnegative integer weights
whose sum is at most `2**50`. The independent checker uses Python integers.

The object keeps one MiniSat 2.2 oracle, one native HiGHS model, stable soft
enforcement literals, and its own growing core bank. The SAT encoding adds
`C_i OR NOT s_i`; an assumption `s_i` enforces the original soft clause. A
native UNSAT core K gives the internal IHS constraint `sum(z_i, i in K) >= 1`.
HiGHS reprices these retained rows through **`changeColsCost` on the same native
object**. Subsequent purchases explicitly supply the previous hitting-set
solution through `setSolution`. The source formula is not rebuilt on each
request. These are conventional IHS operations, following the weight-independent
core reuse described in [the CP 2021 source bridge](../s05/reprice_sources.md).

The executed dependencies are **python-sat 1.8.dev24, MiniSat 2.2, highspy/HiGHS
1.11.0, NumPy 2.3.5**, on the Python/platform recorded in the result. The
official [PySAT API documentation](https://pysathq.github.io/docs/html/api/solvers.html)
describes assumption-based incremental calls, learned-clause reuse and limited
solving; the installed wrapper was inspected for the exact selected methods.
The official [HiGHS Python examples](https://ergo-code.github.io/HiGHS/dev/interfaces/python/example-py/)
and installed native method signatures were read. The live documentation is
newer than the pinned packages, so the record includes the wrapper and native
binary hashes actually used. It does **not** claim HiGHS preserves its complete
branch-and-bound tree when objective coefficients change. Retained native
objects, core rows, explicit starts and SAT accumulated counters are the
observed persistence claim.

## Independent negative evidence is still a purchase

A native optimum status, hitting-set bound or raw core does not enter the
checked lower bank. Native IHS is allowed to propose a useful witness or the
point at which to buy a negative certificate. Every returned repair is checked
against the original hard clauses and has one full original objective pass.
The v2 adapter additionally checks the SAT model's assumptions and that its
checked cost does not exceed the proposed hitting-set cost.

For the requested-tolerance path, the outer service first evaluates identical
checked banks and uses the existing integer threshold
`b = min(U,p) - tau - 1`. A native model at cost at most b improves U. If the
native IHS lower hint exceeds b, the service **separately calls** the existing
weighted-budget branching provider at b, pays its actual invoice, independently
checks the complete returned tree, and only then retains L at least b+1 and
the reusable leaf masks. That call is actual new proof production; it does not
translate a native core into a tree or reuse a historical source invoice.

The exact-completion control has the same initial gate and cache. Where new
work is needed it lets native IHS obtain an optimum candidate with checked
cost C, then buys/checks the separate negative proof at C-1. All 18 such
completions in the repaired run have an independently checked matching lower.
The native exact result is thus useful in the paid controller and is never
used as an unbilled diagnostic label or runtime estimate.

`UNRESOLVED` remains distinct from checked action. The response preserves
partial native events, capped proof attempts and any checked witness already
obtained. A missing or incompletely checked proof supplies no lower receipt.
The outer controller stops if its checked interval does not improve.

## Current cache admission and the 80-request integration

The new consumer did not trust a self-declared checksum. It read the existing
**8,037-byte** `regions_bundle.json`, actually rechecked all **29 witnesses and
18 negative proofs** used by its pointwise projection against the original
raw archive, and matched source IDs, assignment IDs, original budgets, leaf
masks, proof IDs and raw event dependencies. The cell geometry is not used by
this consumer. Its exact pointwise mask evaluator uses one demand-driven LSB
sum DAG for both controllers, including subsequently purchased masks.

This admission cost **92,969 declared units**, including actual file
admission/hash work, source/witness checks, tree checks/compilation and compact
projection binding. It is actual common work performed once in this run.
Earlier source acquisition of **77,646 units** remains historical and common.
These are separate from the two arms' own new work below. The three relevant
entry points are `native_repair.py`, `native_stream.py` and `native_check.py`;
all complete receipts are retained in their JSON results.

The repaired stream uses the existing sixteen sources and five weight recipes,
in their existing order, with replacement price 6 and regret tolerance 1. It
is exposed development; it is not new validation of controller superiority.

| Same 80 requested actions | Native requested tolerance | Native exact completion |
|---|---:|---:|
| Checked at requested tolerance | 80 | 80 |
| Closed using retained checked cache | 61 | 62 |
| New native purchases | 19 | 18 |
| Actual native hitting-set solves | 59 | 75 |
| Actual native SAT solves | 45 | 75 |
| Retained native cores | 40 | 57 |
| Purchases beginning with previously acquired cores | 7 | 6 |
| Separately paid and checked negative-proof calls | 14 | 18 |
| Sum of returned action costs | 223 | 220 |
| Unresolved requests | 0 | 0 |
| Final checked pointwise cache + DAG, serialized bytes | 12,887 | 14,087 |

Each controller retains its own purchases; neither receives the other's new
witnesses or proofs. Exact completion bought stronger evidence, closed one
additional later request from cache, and supplied actions whose total cost
was three units lower while both paths met the same regret tolerance. That
is a useful tradeoff to retain in subsequent acquisition work.

## Full invoice vector, without invented native units

| New declared operations in each arm | Requested tolerance | Exact completion |
|---|---:|---:|
| Separate branching proof provider | 33,895 | 47,973 |
| Native source admission and encoding setup | 3,408 | 3,408 |
| Native adapter, updates, checking and receipt retention | 7,090 | 10,556 |
| Shared compact service/controller operations | 8,198 | 8,564 |
| **Declared subtotal excluding native search** | **52,591** | **70,501** |

Native internal computation is **not included** in that subtotal. The result
also records every native call, SAT decisions/conflicts/propagations/restarts,
MIP nodes, and measured process/wall time. Native-search wall times in this
single ordered execution were approximately **160.694 ms** and **265.310 ms**;
whole-arm wall times were **188.261 ms** and **301.659 ms**. Native-search
process times were **503.441 ms** and **265.215 ms**. Process CPU can include
background native-library work and exceeds wall time in the first arm; the
different startup states and one ordered run do not support a runtime ranking.

The resource cap is an explicit vector: 256 IHS rounds per purchase, 100,000
SAT conflicts per call, 100,000 MIP nodes and 2 seconds per MIP call, 1,000,000
branching-proof units and 1,000,000 adapter units. These are the same for both
arms. They are not a common dollar cap or a claimed conversion among machine
work, proof tariffs and time. Native memory consumption is unmeasured; the
quoted bytes cover only the serialized checked cache/DAG. Final JSON writing
and external delivery are additional to the displayed per-arm measurements.
The [s05 v2 setup sensitivity](../s05/repair_stream_v2_findings.md) continues to
apply to its older comparison; none of these native numbers repairs or
establishes the earlier small total-cost margin.

## Narrow defect found and repaired

The optional PySAT `warm_start=True` mode was initially enabled in addition to
keeping the SAT object resident. Under changed assumptions, one exact-path
call returned an old feasible model whose objective exceeded its hitting-set
proposal; a separately paid proof call found a better model. Independent
checking prevented an incorrect lower from being admitted. The initial outer
loop lacked a no-progress stop and repeated that purchase until its cap.

`native_attempt_02.json` preserves the complete failed trace: the exact path
closed 79 of 80 requests, made 273 purchases and left one request unresolved.
`native_warm_attempt.py` and `native_attempt_runner.py` preserve the code needed
to reconstruct that attempt. `native_attempts.json` also records an earlier
unsaved smoke and first failed run whose receipts were lost because the initial
runner asserted before writing; those runs contribute no reusable evidence or
reported performance result. The correction removes only the optional SAT
warm-start mode, preserves the resident SAT solver/learned clauses, adds explicit
assumption/objective checks and stops a non-improving checked interval. Failed
work is not deleted or folded into the repaired comparison invoice.

The focused follow-up replay independently checked **23 new witnesses and
32 new lower proofs**, plus thirteen native predecessor links, with zero new
search calls. Its 8,057 checker units are additional verification work.
Two separately recorded small cap probes confirm that zero native rounds and
zero proof-production budget return unresolved, and that a native lower hint
cannot become a checked lower when proof production is capped. Their actual
setup/native/proof invoices are in `native_check_results.json`.

## Next constructive use

The outer calibrated-repair service can now call this engine at a justified
lower-corner weight vector, retain a source-bound checked witness or proof,
and reevaluate it throughout an uncertain weight set. The next scientific
question remains how to choose and price cost audits versus logical work for
that output. The separately paid finite proof provider is a precise remaining
scaling limitation: a supported proof-producing native bounded solver or a
checked core/optimization export would be needed to replace that extra search
without weakening the admitted lower-evidence contract.

Reproduce in an environment with the pinned requirements, supplying a new
output path so existing evidence is preserved:

```bash
python -m pip install -r v3/discovery/s06/native_requirements.txt
python v3/discovery/s06/native_stream.py /tmp/native_stream_new.json
python v3/discovery/s06/native_check.py /tmp/native_check_new.json
```

The latter command checks the **saved authoritative repaired stream** and
records new cap probes. It does not silently switch to the optional newly
generated stream. Dependency hashes and native counters make differences
visible; wall-clock numbers are not expected to reproduce bit-for-bit.
