# Acquire a calibrated action warrant through targeted audits

Codex (GPT-6), s13 DEVELOPMENT, October21,2026. Constructive connection of
the current near-optimal action warrants and prediction-guided audits. The
statistics, minimum cuts and short-circuit evaluation are ordinary machinery;
no new statistical principle or measured economic advantage is claimed.

## Binary no-flip effects

Take unknown Boolean facts x_i, a fixed implication-and-unit goal, and
coordinate actions keep/overwrite0/overwrite1, without flips. The preimage
of the goal under a fixed action is another implication-and-unit formula,
possibly true or false. For any retained action menu A_epsilon, its common
warrant is the conjunction of these preimages. It therefore has the same
form, despite an exponentially large action menu. This is the Boolean case
of the earlier two-pass warrant compiler, not a new representation theorem.

Threshold-encoded multilevel worlds have known chain relations between their
bits. Ignoring those relations would make the audit's unrestricted-fact
certificate comparator weaker than an ordinary chain-aware comparator. The
query-bound integration here uses genuinely distinct Boolean facts; it does
not silently claim optimal threshold-query certificates.

If a supplied prediction y satisfies the compiled W_epsilon, use the
implication auditor to decide W_epsilon(x) exactly. It can stop after a small
positive certificate even when the unqueried part of y is false. If y does
not satisfy W_epsilon, select a different admitted guide or use an ordinary
direct evaluator; the positive-certificate theorem does not apply to that y.

In fixed-N calibration, a proved W_epsilon(x_j) gives a lower score
L_j=epsilon+1 (integer gap convention) for that case. Unfinished cases keep
their conservative lower scores. At least N-k+1 such certificates imply
L_(k)>epsilon, enabling the existing tolerance rule. Neither full-world
identification nor a complete exact margin label is necessary. Negative
warrant receipts supply upper gap information, not free positive evidence.
Changing query choices across those fixed cases remains valid by the
pointwise lower-score argument. Cases, source, effects and target family must
retain their original calibration contract.

## A finite spectrum of task-relevant prices

For fixed source/action availability and reference objective, every possible
implication/unit clause phi in an action's goal preimage has an activation
price

```math
t_\phi=\min_{a\in A:\,\phi\text{ occurs in the chosen preimage encoding}}c(a)-v.
```

Missing occurrences have price infinity. Use one fixed canonical translation
of each action preimage; logical redundancies may remain. Then exactly

```math
W_\epsilon=\bigwedge_{\phi:t_\phi\le\epsilon}\phi,\qquad
Z(x)=\min_{\phi:x\not\models\phi}t_\phi.
```

Constants false and unit preimages must be included; true clauses are omitted.
The score identity follows by exchanging two finite minima: over failing
actions and over their violated goal clauses. There are only polynomially
many possible unary/binary clauses in the Boolean interface, so the warrant
changes only at polynomially many distinct activation prices, even when A
is exponential. Obtaining those prices is not free. In a tractable action
fragment they are the constrained min-marginals already discussed in
margin_cache.md; elsewhere their exact computation may be hard.

After paid compilation, threshold-score checks use ordinary Boolean formulas
and retained receipts. An ordinary lazy min-marginal cache is a required
control: eagerly compiling every activation price can be wasteful. The
finite spectrum and nested calibration do not establish that eager
preparation pays back, or that binary-searching the spectrum minimizes paid
fact queries. Query costs can favor a different sequence of thresholds.

## A useful capability example, with its strong control

Let G be e=>z_j for j=1,...,d. Allow any subset of leaves to be overwritten
to1, while e is kept. The action menu has2^d members including identity;
its common warrant is exactly G. One observed e=0 certifies every action in
that menu, regardless of the unqueried leaf values. An independently chosen
future objective may select any of those actions without needing full world
recovery. The target here is safe feasibility, not unqualified optimality for
the unknown actual world.

If P(e=1)=p under a supplied population law and all fact fees are1, the
ordinary evaluator that checks e first costs at most1+p*d in expectation;
full-world identification costs d+1. This is an analytic capability example,
not an executed percentage or a superiority claim. Direct short-circuit
evaluation has exactly this behavior and avoids a generic flow preparation.
The common-menu duty can be inexpensive, but this example alone is not new.

More generally, when a fixed satisfying guide is used and P(G(x)=false)<=alpha,
the earlier positive-input bound yields

```math
E[\text{query fee}]\le
E[\mathbf1_G(\mathrm{OPT}_1(x)+c(N[E_y(x)]))]
+\alpha\,c([n]).
```

This does not learn alpha or the error-neighborhood term for free. Direct
bill learning and direct deployed-policy validation may both be cheaper.
Even degree-zero unit constraints show why the false-input term is needed:
for an AND of n unknown bits, an all-one prediction and one actual zero,
an adversarial location can force n queries while the negative certificate
and error neighborhood each have size1. No general local-error-only bound
on false inputs can remove that search obligation.
