# Native bounded-call proof export: concrete available capability

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**
Capability reconnaissance for a second separately paid negative-proof bridge.
The stable executed `native_repair.py` and its stream results are unchanged.
This note records **one additional native SAT solve**, separately from that
stream. No generic independent checker or lower-bank admission was performed
by this probe.

## Recommended first path

The installed **python-sat 1.8.dev24** exposes `Glucose3`, corresponding to
**Glucose 3.0**, with proof logging. A fresh `Glucose3(with_proof=True)` object,
followed by `append_formula(full_cnf)`, `conf_budget(cap)` and
`solve_limited(assumptions=[])`, can return ASCII proof lines through
`get_proof()`. The actual constructor and exporter source are saved in
`proof_cap_results.json`.

The [official PySAT API](https://pysathq.github.io/docs/html/api/solvers.html)
describes the proof logging and assumption interfaces. The installed wrapper
is more specific about this combination: both Glucose3 and Glucose4 explicitly
reject simultaneous `incr=True` and `with_proof=True`. Instantiate proof logging
**before loading any clauses**, use a fresh object for the bounded call, and
put every premise—including bound restrictions—into the checker-visible CNF.
The proposed proof call uses no assumptions, external propagators or native
cardinality objects. Resident native IHS reuse remains a separate service path.

| Installed wrapper inspected | Version indicated by installed source | Export / relevant constraint |
|---|---|---|
| `Glucose3` | Glucose 3.0 | ASCII proof lines; bounded conflict calls; only backend actually probed here |
| `Glucose4` | Glucose 4.1 | ASCII proof lines; same incrementality/proof incompatibility; not executed here |
| `Lingeling` | Lingeling, exact native revision not independently queried | ASCII proof lines; installed `conf_budget` raises `NotImplementedError`; not executed |
| `Cadical153` | CaDiCaL 1.5.3 | Wrapper converts binary proof stream to textual steps; not executed |
| `Cadical195` | CaDiCaL 1.9.5 | Wrapper converts binary proof stream to textual steps; not executed |

These are selected installed wrappers and source capabilities, not a claim to
have exercised every backend or established pure-RUP output for all formulas.
`pysat.pb` is present but its `pypblib` dependency is absent. `pysat.card` is
present. A small explicit CNF encoder avoids adding that missing dependency
and exposes the weighted-bound translation for separate checking.

Installed source hashes:

```text
pysat/solvers.py
d3463ac8a357bc938b03b9786880e0b9e15b34cf65b773e4993d8ec41e37690f

pysolvers native binary
e8b25021797356ae56e2a76aeae01e3b25305ecd75c1e62b4133c2cccb9ed089
```

## One actual bounded-objective export

The example has hard clauses `(x1 OR x2)` and `(x3 OR x4)`. Its four soft
clauses are `NOT xi`, each with penalty 2, and the queried budget is 3.
Thus the objective bound is exactly `2 sum(xi) <= 3`, equivalent to at most
one true variable. The independently understandable CNF is the two original
hard clauses plus all six pairwise clauses `NOT xi OR NOT xj`, for i<j.
There are eight clauses, sixteen literal occurrences and no auxiliary variables.

One fresh, proof-enabled Glucose3 call with a conflict cap of 10,000 returned
UNSAT and the seven-byte ASCII proof:

```text
-3 0
0
```

The native counters were two conflicts, two decisions, one propagation and
one restart. The measured call including setup and export used 323,200 ns
of process time and 322,248 ns of wall time. These are a capability observation,
not a runtime benchmark. The complete source, encoding, proof bytes, installed
hashes, caps and counters are saved in `proof_cap_results.json`; the producing
code is `proof_cap_probe.py`. No exact-optimum diagnostic was called.

The two proof steps can also be checked directly. Negating the proposed
clause `NOT x3` sets x3 true. The pairwise clauses force x1 and x2 false,
contradicting the first hard clause. After adding `NOT x3`, the second hard
clause forces x4 true, which again forces x1 and x2 false. Therefore the empty
clause follows by unit propagation. This is a transparent instance of reverse
unit propagation; it is not a claim that the probe implemented a general checker.

## Admission contract for the constructive follow-up

The [DRUP format description](https://www.cs.utexas.edu/~marijn/drup/) explains
clause additions and deletion hints. A strict first checker can require each
addition to pass reverse unit propagation against its admitted CNF and prior
checked additions, and require a checked empty clause. Ignoring deletion hints
retains more clauses and is sound for this addition-only entailment check;
unsupported proof steps should remain unresolved instead of being accepted
from backend status. A larger general proof format is unnecessary for this
first capability.

Independent RUP checking establishes inconsistency of the **encoded CNF**.
Using it as a weighted-repair lower receipt also needs the source/objective
mapping and exact bound encoding justified and bound to the receipt. Include
original clauses, violation-indicator semantics, auxiliary-variable allocation,
weights, budget and complete CNF/proof identities. Charge encoding, native
search, proof export, checking, retained bytes and incomplete attempts.

The immediate admitted conclusion is a scalar weighted statement
`q dot z >= b+1`, with its source and weight dependencies. A proof at a
coordinatewise lower objective also gives that scalar lower throughout a
nonnegative weight box. DRUP output does not automatically yield the old
branching proof's reusable leaf masks. Any compiled Boolean-mask relaxation
of multiple checked cuts is an additional, separately justified and paid
representation step.
