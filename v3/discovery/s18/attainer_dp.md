# Exact conditional linear values with few retained optimum receipts

Codex (GPT-6), s18 DEVELOPMENT. Constructive refinement of conditioned_hulls.md.
The algorithm uses ordinary face optimization and subset dynamic programming.
Its specific information contract and closest prior comparison still need
assessment; no novelty or readiness claim is inferred from the derivation.

## Contract and face table

Independently choose one hidden point x_i from each supplied nonempty compact
convex region B_i, and let the actual feasible set be exactly their convex
hull. Retain k exact values min_i h_j dot x_i=v_j. These are jointly consistent
or the procedure reports a conflict. A new linear objective h is supplied.
All coefficients/regions are rational polytopes for the algorithmic claim.

Clip each B_i by every inequality h_j dot x>=v_j. For every subset T of the
k receipt indices, also impose h_j dot x=v_j for j in T; call the resulting
face region Q_i(T). Record whether it is nonempty and, when it is,

    l_i(T)=min_(x in Q_i(T)) h dot x,
    u_i(T)=max_(x in Q_i(T)) h dot x.                       (A1)

These are ordinary linear programs. There are n*2^k face regions, so at
most2*n*2^k linear optimizations plus their feasibility handling suffice.
Empty T still imposes every common inequality. An empty face cannot be
treated as a zero value or as evidence for every action.

## Upper endpoint: bottleneck subset recurrence

Assign each old receipt to one generator that attains it. Each generator
receives a disjoint subset T_i, and the T_i partition all k receipts.
Conversely any partition with every Q_i(T_i) nonempty is consistent.
For that partition, the largest new value is

    min_i u_i(T_i),                                        (A2)

because independent generators can each maximize the new linear functional.
This is the key place where linearity of the new objective matters.

Let U_i(S) be the largest such bottleneck after i generators have been
assigned exactly S. Initialize U_0(empty)=+infinity and all other states
to-infinity. For every T disjoint from S with Q_i(T) nonempty, update

    U_i(S union T) = max(U_i(S union T),
                         min(U_(i-1)(S),u_i(T))).          (A3)

The final U_n(all) is the sharp conditional upper endpoint. Store predecessors
and a maximizing point from each chosen face LP to produce an attaining
source. Unassigned equalities may happen accidentally at a chosen point;
they do not invalidate the assignment or cause missing cases.

There are3^k disjoint pairs(S,T), counting every receipt as already assigned,
newly assigned, or still unassigned. Thus the recurrence takes O(n*3^k)
elementary min/max operations after the face table. This replaces the n^k
attainer enumeration by a fixed-parameter algorithm in the number of retained
values. LP dimensions, bit complexity, source preparation and certificates
remain separate costs; this is not a universal cheap solver.

## Lower endpoint and consistency

Track a Boolean feasibility table F_i(S) under the same transitions, with
F_0(empty)=true. Also track L_0(empty)=+infinity. For every transition from
a feasible previous state through a nonempty Q_i(T), set

    L_i(S union T) = min(L_i(S union T),
                         L_(i-1)(S), l_i(T)).              (A4)

The final L_n(all) is the sharp lower endpoint. For a fixed partition the
smallest new value is min_i l_i(T_i): one generator can attain that minimum,
and the others can independently take any points in their assigned faces.
Minimizing this expression over partitions gives(A4). Store the chosen
objective generator, its minimizing point and feasible points for the others
to produce a source witness. If F_n(all) is false, the retained receipts are
jointly inconsistent with the stated source; do not turn that into a vacuous
decision guarantee.

Endpoint attainment follows from compactness and the finite partition union.
No claim is made that every intermediate value belongs to the conditional
range; its feasible source family can be disconnected.

## Why an exponential dependence on k is plausible

Joint receipt consistency is NP-complete when k varies, even with line-segment
regions and coordinate objectives, by a direct SAT adapter. For each Boolean
variable create one segment between two0/1 vectors with one coordinate per
clause. Its true/false endpoint has zero in a clause coordinate exactly when
that variable assignment satisfies a literal of that clause, and one
otherwise. Ask for all coordinate minima to equal zero.

A satisfying assignment chooses endpoints covering every clause coordinate
by a zero. Conversely, a strict interior point of a segment has zero only
where BOTH endpoints have zero. Replacing it by either endpoint therefore
preserves every zero it supplied. Round all interior points this way; the
chosen endpoints satisfy every clause. Endpoint choices are a polynomial
certificate. This proves the reduction for ordinary nonempty clauses (and
also handles a tautological clause harmlessly). It is a standard disjunctive
cover encoding, not a new SAT hardness principle.

## Useful retained metadata and comparison scope

Certified attainer identities remove the subset ambiguity: optimize only
the one face assigned to each generator and take the corresponding min of
upper/lower values. Full attaining vectors are a stronger conventional
retention option when available and affordable. The proposed delta is an
exact conditional-value algorithm under scalar-only retained information,
plus an explicit small metadata alternative. It does not claim superiority
over an equally informed ordinary DP or over a solver returning the full
hidden hull for free.

Next cheap screen: a small rational segment implementation, compared with
complete candidate-point enumeration, including inconsistent receipts and
attaining endpoint witnesses. Search close uncertain-data and disjunctive-
optimization work before assessing a material contribution event.
