# Prediction-guided audits of an implication warrant

Codex (GPT-6), s13 DEVELOPMENT, October21,2026. S02/S35 extension. Paid
facts x_i are deterministic Boolean answers with positive query fees c_i;
each can be purchased once and retained. There are no hard source relations
between unqueried facts. A known condition G is a conjunction of implications
x_i=>x_j and units, with self-implications removed. A fallible prediction
y satisfies G; checking that syntactic condition is paid. Correctness never
requires y=x. The output is the exact truth of G(x), useful for checking an
action warrant or a proposed scope of model reliance.

## Cheapest positive certificate at the proposed world

A positive certificate is a set C of queried coordinates whose values at y
force G for every completion. Every non-tautological clause must have an
observed satisfying literal: otherwise that clause has a falsifying completion.
Units and binary clauses with one satisfying literal force their supporting
coordinate into C. For a clause with two satisfying literals, at least one
of its two coordinates must be chosen.

For implications, the two-satisfied-literal case is y_i=0,y_j=1. These
remaining covering edges form a bipartite graph between predicted zeros and
ones. After including forced coordinates and removing covered edges, minimum
weighted vertex cover gives an exact cheapest certificate in polynomial time.
Use the ordinary source-to-left/right-to-sink capacities c_i and infinite
left-to-right edge capacities (any finite value greater than total c suffices).
The source-side/right plus sink-side/left cut vertices give the cover. A max
flow and its matching cut can supply an independently checked optimality
certificate, at an additional charged cost. This is established optimization.

For a generic2-CNF, the cover graph need not be bipartite: the all-positive
clauses of a triangle at y=111 already give ordinary weighted vertex cover.
The exact polynomial certificate claim is therefore restricted to implications
and units, or another checked bipartite residual covering graph. A common
polarity transformation of variables preserves the audit interpretation.

## Two rounds and a positive-instance cost bound

1. Compute a minimum certificate C_y at y and purchase all its facts.
2. Substitute the actual receipts in G. Every original clause already touched
   a predicted satisfying literal, so the residual formula contains only units,
   true clauses, or a witnessed contradiction. In the contradiction case,
   return false. Otherwise query its remaining unit coordinates R and evaluate
   their conjunction, stopping early on a failed unit if desired.

This is exact for every actual x. Both rounds and all checking/flow work must
be charged; the following bound concerns only the fact-query fees.

Let E={i:x_i!=y_i}, and let N[E] be E plus all variables sharing a clause
with any member of E. Write c(S)=sum_(i in S)c_i. If G(x)=true, let OPT_1(x)
be its cheapest positive-certificate fee. Then

```math
\mathrm{queries}(x,y)\le
\min\{c([n]),\ \mathrm{OPT}_1(x)+c(N[E])\}.
```

Proof. Any actual positive certificate C_x can be turned into a certificate
at y by adding N[E]: clauses whose old witness changed lie entirely within
that neighborhood, and y satisfies them. Hence
c(C_y)<=c(C_x union N[E])=c(C_x outside N[E])+c(N[E]).
Every residual unit coordinate r belongs to N[E]: its clause's queried
predicted witness became false. Moreover r belongs to *every* positive
certificate at x, since its literal is now the sole true literal of that
clause. Thus R is a subset of C_x intersect N[E]. Adding c(R) to the previous
bound proves the stated single-neighborhood penalty. No fact is purchased
twice, giving the total-fee cap. With E empty, the protocol buys an optimal
positive certificate exactly. A rough unweighted degree bound is
c(N[E])<=sum_(i in E)sum_(j in N[i])c_j; raw Hamming error omits this geometry.

The important sharpening is that repair units are mandatory even for an
omniscient positive certificate. A first looser argument counted the error
neighborhood twice; that is unnecessary for binary clauses. For wider CNF,
the residual need not be units and this proof does not give the same result.

## Early exclusions and ordinary comparisons

One prediction error can be very expensive. For G=AND_j(e=>z_j), take unit
query prices, actual e=0 and all z_j=1, but predict e=1 and the same z_j.
The predicted minimum certificate queries every z_j, whereas the actual
minimum is the single fact e=0. The neighborhood term scales with this gap.

The positive-instance comparison does not extend to false inputs. Take many
disjoint implications and a prediction satisfying them all. Flip one endpoint
to violate just one implication. A whole predicted positive certificate can
cost proportional to the number of clauses although a negative certificate
has two facts. Sequential negative discovery and an ordinary Boolean-function
evaluation policy are therefore mandatory practical controls. The protocol
does not promise constant competitive ratio on both output classes.

Computing an optimal certificate at a prediction and repairing failed checks
is established learning-augmented explorable uncertainty. Diwan et al.,
*Optimal Verification of a Minimum-Weight Basis in an Uncertainty Matroid*
(STACS2026), use bipartite certificate optimization and explicitly give a
prediction-certificate-then-fallback method (section5.2.1). Their smooth bound
for basis predictions is a distinct circuit/error analysis (section5.2.2).
Here the restricted Boolean adapter supplies a binary-clause local repair
and a query-cost bound on positive inputs. Its closest direct antecedent
still needs checking; no novelty or empirical superiority is established.
The identical ordinary certificate/audit implementation ties.

This may help acquire a task warrant without acquiring an entire predicted
world. It is not a proof that the predictor is globally correct, a learner of
unresolved mathematical truth, or a complete-computation improvement.

The first audit_probe.py run passed30 implication formulas with84 satisfying
predictions, checking4216 actual worlds. It compared minimum-cut certificates
with15528 subset/completion tests, checked588 positive-instance cost bounds,
and found312 nonempty mandatory repairs. In192 positive cases the prediction
was globally wrong but the first purchased certificate already sufficed.
Those counts describe this generated panel, not a population success rate.
Four star examples retained the one-error/large-cost counterexample. Combined
runtime0.0429548 seconds is not a separate arm comparison. No scientific
execution failed and no complete-cost advantage was measured.
