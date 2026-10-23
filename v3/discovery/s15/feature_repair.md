# Learn the input map as well as the output error space

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 38.

Assume the true error has a declared finite feature representation
F(x)=E phi(x), phi(x) in K^M, and a previously certified common event
warrants image(E) subset U, where U is an n by d full-column-rank matrix.
For total-degree-D polynomials in m variables, M=binomial(m+D,D). The
feature representation, field, degree promise and old probability event are
paid premises. Keep all previously acquired feature/error pairs, written
Phi=[phi(x_1),...,phi(x_s)] and Y=[F(x_1),...,F(x_s)].

If a new phi lies in column_span(Phi), solve Phi alpha=phi and return
F=Y alpha. No new exact output is needed. Otherwise select independent
rows J of U, acquire the d exact-minus-model anchors F_J, and return

    F=U (U_J)^(-1) F_J.

Append this new complete pair to the retained feature map. Its feature rank
increases by one. Starting at rank k, at most M-k such new acquisitions,
each of d exact coordinates, determine the whole error map. Thereafter all
future errors can be evaluated by interpolation/factorization, without
new true-output queries. Fresh sampling is unnecessary for these sound
algebraic updates: they preserve the original common event.

One may deliberately choose the missing feature directions from a known
unisolvent set. For the full total-degree basis, a lower-set interpolation
grid built from D+1 distinct field elements is an ordinary option. Since
its feature vectors span K^M, greedy rank completion supplies M-k directions.
Finding the set, evaluating features, factoring matrices, storing coefficients
and exact bit complexity all have costs. Ordinary interpolation and low-rank
cross approximation are direct controls.

## An exact one-case anchor lower bound under this information contract

Suppose phi is outside the old feature span and the only retained coefficient
constraints are E Phi=Y and image(E) subset U. There is a linear functional
lambda with lambda(Phi)=0 and lambda(phi)=1. Hence every alternative

    E'=E+U z lambda

preserves the retained information while changing the new error by U z.
After fewer than d independent coordinate queries, some nonzero z lies in
the kernel of all queried rows of U. Those alternatives have the same
transcript but different full answers. Thus d independent anchors are
necessary for an exact answer under this contract, and sufficient as above.
This applies to deterministic/every-tape exactness, and to zero-error
randomized policies over a finite field (finite feasible-world support).
It does not claim a lower bound for approximate answers, additional retained
coefficient constraints, or a richer oracle that returns whole vectors.

With fixed unequal coordinate prices, the cheapest exact anchor set is a
minimum-weight basis of the row matroid of U. Sorting by price and greedily
adding independent rows solves this familiar linear-matroid problem. Adaptive
queries cannot evade the requirement that every exact terminal set spans U.

## Acquisition example and what it rules out

Take n=128, m=3, D=4, hence M=35; certified error rank d=4; and seven
initial full-output samples with observed feature rank k=7. The initial
samples cost 896 true-coordinate outputs. Completing the feature map costs
at most 4*(35-7)=112 more, for 1008 total. Direct full-output interpolation
at 35 points costs 4480 such outputs: a 77.5% reduction in THIS oracle
component under these premises. The final low-rank correction has n*d+d*M=652
scalar factor entries before compression, versus n*M=4480 for a dense error
coefficient matrix. These are representation/query counts, not CPU savings.

The original model B must still be evaluated, and a public symbolic matrix
may permit direct factoring more cheaply. Training feature rank must be
observed rather than assumed seven. Statistical range certification retains
its failure budget; interpolation does not turn it into a zero-error theorem.
An ordinary identical two-sided interpolation method ties. Generic novelty
is rejected; the proposed synthesis is its integration with acquired error
scope and paid partial evidence.

This is also a stronger baseline for the earlier per-case correction invoice.
It would be unfair to charge an ordinary method d anchors forever after it
has accumulated enough feature information to eliminate those queries.
Finite DEVELOPMENT screen: [feature_probe.py](feature_probe.py) verifies all
729 coefficient maps K^3 to K^2 over F3, with 19,683 repaired output vectors.
Every map needs four additional exact coordinate queries after the first
feature direction; twelve one-query fibers retain three distinct full answers.
The minimum-price two-row basis is checked explicitly. Runtime167,271,600 ns,
Python3.12.14, with source hash in [result](feature_probe.json). This does not
verify a real-world acquisition tariff or the polynomial degree premise.
