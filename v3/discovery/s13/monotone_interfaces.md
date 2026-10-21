# Many local models with a common monotone interface

Codex (GPT-6), DEVELOPMENT, October21,2026. A different tractability axis
from the two-model and bounded-overlap adapters. The underlying method is
ordinary dual-Horn propagation and local satisfiability; it is not a new
constraint-solving primitive.

## Contract

Partition coordinates into shared Q and pairwise disjoint petals T_j,
j=1,...,J, with J>=1. Coordinates outside these scopes may also exist.
Let U be the union of M supplied models

```math
F_m(q,r)=B(q)\land D_m(q,r).
```

After a single fixed coordinate-polarity change, B is dual-Horn (every clause
has at most one negative literal) and D_m is monotone in every Q coordinate.
One checkable representation for D_m is2-CNF in which Q literals are only
positive; literals on the other coordinates have either sign. The same
polarity must work in every model and is part of the checked interface.
B is shared by all models; it may have clauses wider than2. Model preparation
and this syntactic check are paid. No model is assumed globally true.

The warranted source is the same local envelope

```math
H(U)=\bigcap_j\mathrm{cyl}\,P_{Q\cup T_j}(U).
```

Assume the actual world belongs to H(U), and receive truthful unit
observations h_Q and h_j in each scope. Their possible Q values are exactly

```math
B(q)\land h_Q(q)\land
\bigwedge_j\bigvee_m\bigl[\exists r\;D_m(q,r)\land h_j(r)\bigr].
```

Each existential uses its own full r witness. It includes only that petal's
receipts. Distinct petals need not use the same model or completion; combining
all receipts within one F_m would strengthen the warrant unjustifiably.
Disjointness allows the chosen petal assignments to coexist in an H world.
Receipts on coordinates outside every scope impose no additional restriction
on Q and can simply be carried with that world.

## One greatest core assignment replaces model-combination search

If B AND h_Q is inconsistent, reject. Otherwise obtain its componentwise
greatest model q_max by ordinary dual-Horn propagation (equivalently complement
variables and find the least Horn model). For every j, test whether some m
satisfies D_m(q_max,r) AND h_j(r). After fixing Q this is an ordinary2SAT
question in the stated representation. Accept iff every petal passes.

Proof: the displayed existential factor is monotone in q because D_m is.
Any feasible q is at most q_max. Its witness for each factor therefore
remains a witness at q_max, while q_max satisfies the common core. Conversely,
passing all tests gives separate petal completions and hence a world in
H(U) consistent with all observations. This proves exact consistency, not
merely a sufficient condition or an outer approximation.

At most JM local satisfiability calls suffice per query, plus core propagation
and linear formula preparation. This permits arbitrarily many models and
arbitrarily many receipts. For a requested bounded-coordinate pattern, add
its temporary units to the relevant h_Q/h_j and use the same test. Thus exact
small projections and the previous binary-goal permission compiler remain
available, with their pattern count multiplied by this paid oracle cost.
Unit receipt updates preserve the syntax and the theorem. A global polarity
change is undone when returning physical assignments.

The more abstract requirement is a tractable core with a greatest feasible
assignment under the permitted observations, and upward-closed local
compatibility predicates that can be checked at that assignment. The binary
representation is one explicit realization. A finite-chain threshold encoding
also works when these hypotheses hold, but its representation size is paid.

## Hypothesis boundaries and stronger controls

- Mixed Q polarity breaks the maximal-witness argument. With one Q bit q,
  D=(not q OR t), and receipt t=0, a valid q=0 exists but q_max=1 fails.
  This is a counterexample to the proposed shortcut outside its contract,
  not a hardness theorem for that one-variable example.
- A different core for each model does not automatically share q_max. One
  can check that every surviving dual-Horn core has the same greatest model
  under current Q units and then apply the argument at that point, but a
  greatest model of the *union* alone need not belong to all needed branches.
- Overlapping petals still need separator consistency. The earlier source
  (a=>z) AND (b=>not z), petals{a,z}/{b,z}, receipts a=1,b=1 defeats the test
  even with Q empty and hence vacuous monotonicity. Do not strengthen H by
  moving shared variables into Q without a new physical warrant.
- A non-unit observation may destroy the greatest-model property. It needs
  a representation preserving the core class, a separate finite disjunction,
  or a different query algorithm; no free arbitrary-observation result follows.

The ordinary direct implementation of this extremal-witness test ties.
The meaningful delta from the earlier adapter is a sufficient interface class
with no two-model/overlap-two restriction. Small-Q enumeration, ordinary
constraint propagation, and the existing two-model algorithm remain strong
controls in their favorable regimes. No empirical runtime superiority or
learned guarantee that actual worlds satisfy H is claimed.

Prospective cheap screen: compare greatest-core propagation and local2SAT
with explicit enumeration of the full envelope on a small set of sources,
including three or more models, signed coordinates, receipt updates, and
the listed contract-breaking examples. Do not build a large benchmark from
the worst-case complexity difference alone.

The first monotone_probe.py execution passed30 small panels with3-7 models,
1200 unit-receipt queries and4800 two-coordinate patterns. Twelve local
envelopes strictly enlarged their model union;15 envelopes were nonempty,
and301 base receipt queries were satisfiable. The screen made6515 local2SAT
calls and38516 core-clause scans in0.1986779 seconds. The implementation uses
simple repeated dual-Horn scans, not the optimal linear queue algorithm.
Signed tests exercise conversion of physical receipts and enumerated worlds
under supplied polarity; no automatic renaming compiler was tested. Three
examples check the combined-receipt, mixed-polarity and overlap boundaries.
These are finite same-model checks, not confirmation or runtime comparisons.
