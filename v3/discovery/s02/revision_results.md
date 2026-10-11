# Explicit-edit SAT: first constructive evidence

Codex (GPT-6), October 11, 2026. DEVELOPMENT; no P3-POS01 promotion.

The [prototype](revision_probe.py) ran nine solver-independent streams of
97 requests each, at n=8,12,20, with two reversed-order timing passes and five
controllers. All 8,730 answers agreed. Six malformed/stale/recycled edit
attempts were rejected without changing semantic state. The
[raw record](revision01.json) binds source, seeds, complete streams, versions,
answers and counts. These are developmental checks by the implementing model.

| Controller | Warm stream time, aggregate ms | Native solves | Clause evaluations |
|---|---:|---:|---:|
| Fresh native solver per version | 148.761 | 1,746 | 79,908 |
| Full-formula witness/support rechecking | 90.475 | 376 | 104,804 |
| Native incremental solver with assumptions | 77.451 | 1,746 | 79,908 |
| Edit-maintained evidence + fresh fallback | 36.807 | 376 | 14,234 |
| Edit-maintained evidence + native incremental fallback | 22.998 | 378 | 14,044 |

The pattern supports further development of local evidence maintenance. Its
gain over full rechecking is visible in clause-work counts, not only timing.
The integrated kernel is also the **identical ordinary comparator**; this is
not an advantage over conventional methods as a class or a priority claim.
Native solve counts can differ across fallback styles because solvers may
return different satisfying witnesses, which affect subsequent reuse.

Timing covers state construction, edit validation, cache maintenance, failed
reuse, all solver calls, independent SAT checks and cleanup. It excludes common
Python/package startup, generation/serialization and research preparation.
The aggregate workloads take milliseconds; two passes cannot establish a
stable hardware performance claim. This is not a cold complete-cost result.
UNSAT fallback trusts local MiniSat22; no independently checked UNSAT proof is
provided by this prototype. The earlier historical evidence contract is not
silently weakened by reusing its result label.

## Constructive questions now worth answering

1. One retained witness forgets other useful models of nearby formula versions.
   Keeping a small library can avoid repeated solving across alternating regions,
   but maintenance grows with library size. Derive and measure that tradeoff.
2. Explicit add/off/on streams grant structural identity. For independently
   supplied full formulas, reconstructing and checking the edit has a real cost.
   Measure or bound that conversion; do not transfer delta economics for free.
3. A trusted-UNSAT answer is insufficient for a future proof-carrying claim.
   Reuse native assumption cores only with their stated trust scope, or attach
   a verified resolution/DRUP proof and charge proof construction/checking.
4. Broad source/version changes need a fresh admission or a separately checked
   translation. The current edit service intentionally covers only fixed CNF
   literal semantics and variable vocabulary.

Next derive a small-library rule and test genuinely alternating constraints,
without requiring a fresh extensive adversarial evaluation at this stage.

## Small-library development

The [lazy prototype](library_probe.py) matched 28,392 answer evaluations against
fresh native solving. It uses activation cursors and one blocking clause for
each requested witness, with LRU capacities 1,2,4,8. The
[record](library01.json) includes a separate, explicitly constructed alternating
two-model family; no hidden truth filtering selected its inputs.

On the nine original streams, capacity two reduced fallback calls from 378 to
240 (two passes) and clause evaluations from 14,044 for eager single-witness
maintenance to 5,890. Capacities four/eight did not reduce solver calls further
and increased clause checking. Capacity one performed approximately the same
clause work as the eager method while adding cursor overhead. Thus more
retention is not automatically useful.

On the declared two-model alternations, capacity two used 18 native calls over
six runs, compared with 1,158 for a one-witness cache; this is the intended
conditional reuse example, not a generic SAT performance result. The family
has visible equality structure and can be solved by a specialized ordinary
graph/2-SAT method. It demonstrates library persistence, not an advantage over
the strongest solver specialized to that family. Larger libraries did no better.

The second run's base native time was 50.121 ms versus 77.451 ms previously,
despite identical counts. This variation confirms that two tiny timing passes
are descriptive only. Counts offer the clearer developmental evidence.

The rebasing branch did not execute in this cohort: at most 232 activations
were generated, below its 256-entry trigger. Test that branch separately before
claiming a bounded-log implementation. Even with a bounded activation log,
the registry and native solver retain previously registered clauses; this is
**not** a proof that total memory is O(active clauses). Future memory claims
need retirement/reconstruction or an explicit finite historical-ID cap.

The targeted [rebase check](rebase01.json) subsequently exercised 132 resets
across nine n=4,8,12/capacity=1,2,4 runs. All 3,465 answers matched fresh native
solving and the activation log stayed below its declared bound. This closes
only that missing developmental branch check; the historical registry/native
solver memory limitation remains.
