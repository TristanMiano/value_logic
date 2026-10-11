# Regret tolerance under explicit source expansion

Codex (GPT-6), October 11, 2026. DEVELOPMENT, S04/S07.

The first [encoder source](tolerance_probe.py) failed its small construction
check; [failure output](tolerance01.json) and a minimal
[fixture](tolerance_failure.json) are preserved. For weights x1+3*not-x2 and
threshold 1, input (0,0) was incorrectly rejected. Python's `1 == True` caused
a literal node to be merged with a Boolean constant. The separate
[v2 source](tolerance_v2.py) requires matching types before that simplification.
No failed source/output was overwritten.

The repaired [run](tolerance02.json) matched 756 small threshold-encoding
assignments and all 64 source-expansion tolerance decisions against the earlier
exact MaxSAT values. Sixty decisions accepted the old proposed action's
tolerance; four produced real violating models. This is implementation
development by the principal, not independent confirmation.

| Service | Warm aggregate ms | SAT calls | Encoded clauses |
|---|---:|---:|---:|
| Full new-source tolerance SAT | 96.949 | 70 | 109,416 |
| Edit-aware guard, then delta tolerance SAT | 31.315 | 19 | 25,953 |

The edit-aware route handled 24 same-source cases with structural checks, 24
with the affine box guard, and 16 with SAT search. The guard therefore saved
search beyond recognizing an unchanged source. However, both services rebuilt
threshold encodings, and the unary weighted construction is pseudo-polynomial.
The previous full MaxSAT service can be a stronger practical control than a
needlessly expensive SAT encoding, despite answering a stronger question.

The next matched control must cache threshold encodings and native solver
state across repeated counterfactual edits with the same action/tolerance.
Precompute each affine contrast's unconstrained maximum; substituting a
deleted clause's d fixed bits then updates its bound in O(m*d) rational
operations instead of recomputing O(m*n) coefficients. Give that precomputation
to all controllers and include its cost. This addresses a concrete artificial
overhead before any performance interpretation is promoted.

These timings exclude common package startup and harness construction, and
assume an already warranted old action/source bound. The cost of obtaining it
must be included when it was bought only for this edit workload. Bounds that
fall back on SAT still trust local MiniSat22 UNSAT; no external proof object is
checked. The identical ordinary edit-aware kernel is always an allowed control.

## Stronger reusable control reverses the first timing result

[prepared_probe.py](prepared_probe.py) caches threshold encodings and native
solver state across all single-clause deletions from each of sixteen parent
sources. [The run](prepared01.json) matched 1,376 answer evaluations.
For 688 requests per controller, the guarded method reduced SAT calls from
1,026 to 738, but both built 42 solver objects and 39,316 encoded clauses.
The guarded method took 61.731 ms against 47.272 ms for the ordinary prepared
control. It was slower in each tested n group. Fewer oracle calls therefore
did **not** establish a resource improvement against the stronger control.

The next targeted repair is compiled integer bounds and guard dispatch before
an appropriate solver is prepared. Once native state is warm, repeatedly
paying for rational guard arithmetic can cost more than another native query.
This is an implementation hypothesis, not a claimed rescue. If it remains
unfavorable, retain the negative result and change the mechanism/application.

The [integer-compiled repair](prepared_v2.py) matched 2,064 answer evaluations.
In [its run](prepared02.json), ordinary prepared queries took 46.303 ms,
always-on guards 48.213 ms, and cold-only dispatch 45.307 ms. All three built
the same 42 solvers/39,316 encoded clauses. The roughly 2% aggregate difference
for cold-only dispatch is too small for these two short timing passes to
establish a material advantage. Integer compilation removed most guard
overhead, but has not rescued the positive economic claim at this workload.

**Portfolio disposition:** keep the sound source-difference/transport mechanism
and the useful explicit-edit witness service, but deprioritize further tuning
of tolerance guards on already prepared tiny native solvers. Do not turn the
near tie into a positive result by dropping the strongest control. Next return
to S05's missing constructive value-measurement service and explore statistically
valid, priced residual acquisition with a fallible predictor.
