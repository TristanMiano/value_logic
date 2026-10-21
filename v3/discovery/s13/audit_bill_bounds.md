# Counterfactual bills of a simple auditor: easy lower, hard upper

Codex (GPT-6), s13 DEVELOPMENT, October21,2026. Extends
[implication_audits.md](implication_audits.md) toward S06/S31's question of
learning useful procedures from incomplete feedback. This note supplies
mathematical bounds, not a new bandit algorithm or measured scheduling gain.

## A fixed two-round policy under a positive truth receipt

Fix a2-CNF G, a satisfying predicted world y and a positive certificate C_y.
The policy buys C_y first, then every remaining unit produced by substitution.
Now suppose a separate paid receipt already establishes G(x)=true, possibly
with some coordinate receipts h. The residual source is G AND h. That
positive truth receipt is essential and is not supplied for free by a model.

For i outside C_y, let N_i be its neighbors within C_y in the clause graph.
No non-tautological clause has both coordinates outside C_y, and all units
are inside C_y. Each incident clause has a predicted satisfying literal in
C_y. Its queried literal becomes false exactly when that neighbor's actual
bit differs from y. Since G(x) is true, any such event makes the unqueried
literal a mandatory residual unit. Thus the policy's query bill is exactly

```math
K_y(x)=c(C_y)+\sum_{i\notin C_y}c_i
  \mathbf 1\{N_i\cap E_y(x)\ne\varnothing\},\qquad
E_y(x)=\{j:x_j\ne y_j\}.
```

This is a weighted neighborhood-coverage function of prediction errors.
Knowing G(x) does not usually reveal it: unpurchased coordinates of C_y can
change the counterfactual bill even though the target decision is settled.

## Exact lower bill by ordinary Horn propagation

Set e_i=x_i XOR y_i. Because y satisfies G, each non-tautological binary
clause has at least one literal true at e=0, hence at least one negative
e literal. The transformed formula is Horn. Coordinate receipts remain
units. If it is inconsistent, the premise G AND h is inconsistent. Otherwise
ordinary Horn propagation gives its componentwise least model e_min.

The displayed bill is coordinatewise nondecreasing in e, so its exact
minimum over G AND h is K_y(y XOR e_min). This uses a linear-time Horn
solver and a clause-neighborhood scan, with representation costs explicit.
It does not require enumerating worlds or completing every audit. The same
least-error assignment simultaneously minimizes every nonnegative weighted
sum of errors, and indeed every coordinatewise nondecreasing error penalty.

This also gives a small belief-revision consequence: from any satisfying
assignment of a2-CNF, adding consistent unit observations has a unique
least set of required flips, attaining every such monotone repair penalty.
It is a change to an admissible hypothesis under observations, not a theorem
about physical interventions, changed clauses, or logical counterpossibles.
A new non-unit constraint can destroy it: starting with the unconstrained
source and y=00, adding x1 OR x2 has two incomparable minimal flip sets.

## The exact upper bill can already encode SAT

The upper endpoint is not automatically another cheap replay. Here is a
development reduction showing NP-hardness even for implication G, unit query
prices, a predicted minimum positive certificate, and a nonempty source.

Start with a CNF on n variables whose clauses are each all positive or all
negative, with width at most3. Satisfiability of this form is NP-hard: replace
each negative literal of an arbitrary3-CNF by a new complement variable, and
enforce each variable/complement pair with one positive2-clause and one
negative2-clause. This preserves satisfiability and yields the stated form.
Let m be the number of clauses.

For each variable i introduce queried coordinates p_i,n_i and outside
coordinates r_i,s_i. Include implications

```math
p_i\Rightarrow n_i,\qquad p_i\Rightarrow r_i,\qquad s_i\Rightarrow n_i.
```

Predict p_i=r_i=0 and n_i=s_i=1. The last two implications force every
p_i and n_i into any positive certificate at y. Their2n facts also suffice
for these clauses. For a positive CNF clause C introduce outside t_C and
implications p_i=>t_C for i in C; predict t_C=0. For a negative clause use
t_C=>n_i for i in C; predict t_C=1. All these clauses are covered by
C_y={p_i,n_i:all i}. Thus C_y is a minimum positive certificate, and G has
the displayed satisfying prediction regardless of the CNF's satisfiability.

In an actual G-world, p_i<=n_i prohibits simultaneous errors p_i=1,n_i=0.
A first-round error at p_i requires r_i, and an error at n_i requires s_i;
there are at most n such guard purchases. A clause coordinate t_C is bought
iff its CNF clause contains a corresponding selected error. There are at
most m such purchases. Consequently K_y(x)<=3n+m.

Equality is attainable iff the homogeneous-clause CNF is satisfiable.
An attaining world selects one of the two errors for every variable and
hits every clause, giving a satisfying assignment. Conversely a satisfying
assignment selects p_i=1,n_i=1 for true variables and p_i=0,n_i=0 for false
variables. Set r_i=p_i,s_i=n_i; choose positive t_C=1 and negative t_C=0.
This is a G-world and buys all n guard plus m clause coordinates. Deciding
whether the upper bill reaches3n+m is therefore NP-complete: a world is a
polynomially checkable witness. The lower bill is simply2n at y.

This asymmetry is about exact range computation, not about executing the
auditor on a real world; execution and verification remain polynomial.
Ordinary SAT/MaxSAT, coverage bounds, or further paid receipts can tighten an
upper bill. An interval with an exact cheap lower endpoint and a conservative
upper endpoint is legitimate partial feedback. Treating every unrun policy's
cost as observed merely because one policy proved G would be incorrect.

## Comparison and next screen

Horn least-model inference, weighted coverage and SAT reductions are standard
ingredients. Earlier S06 threshold-policy ranges and S31 receipt replay are
the program lineage. The proposed delta is the exact lower-price service and
an explicit obstruction to equally cheap upper-price replay for this auditor.
No learning speedup, general partial-feedback rate or complete economic gain
is claimed. A tiny next check should compare the lower formula with explicit
completion enumeration and verify the reduction on small homogeneous CNFs.

The first bill_probe.py execution passed35 general2-CNF panels and630 unit
receipt queries (200 inconsistent). The least-error assignment and exact
lower-price formula matched1530 compatible completions. Twelve small
homogeneous-CNF reductions enumerated417792 worlds; seven satisfiable and
five unsatisfiable inputs had exactly the predicted upper-price threshold
behavior. Runtime1.3112576 seconds; same-model finite development only.
The supplied-certificate test here allows general2-CNF; it does not claim
that minimum positive certificates for general2-CNF are cheaply computable.

A close antecedent for the least-flip step is Behrisch, Hermann, Mengel and
Salzer, *Minimal Distance of Propositional Models* (2019), section6.1,
Proposition33 and proof. Its nearest-other-solution construction starts a
forced flip in a satisfying bijunctive assignment and propagates all further
required flips. Our unit-receipt/monotone-bill consequence uses that same
underlying closure behavior. It must not be presented as a new general
nearest-model algorithm.
