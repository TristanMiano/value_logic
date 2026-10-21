# Learn the permission source directly from incomplete worlds

Codex (GPT-6), DEVELOPMENT, October21,2026. Q1/Q3/Q4. This combines ordinary
positive-example conjunction learning with the operation preimage compiler.
It is a constructive counterpart to warrant_learning.md's unfavorable
continuous/large-domain example, not a new PAC-learning algorithm.

## A fixed operational vocabulary

Fix a finite world domain, allowed actions and goal semantics. Suppose every
action's success region G_a is a conjunction of clauses from a known
vocabulary C of size M. Tautology is the empty conjunction; treat an
identically failing action separately. The vocabulary and its semantics
are fixed independently of the sample.

For the no-flip Boolean effects keep/overwrite0/overwrite1 and an implication-
and-unit goal, take C to contain the2n signed units and the goal's g distinct
nontrivial implications. Substitution produces only these clauses, constants
or tautologies, so M<=2n+g, even though there are up to3^n actions. With
arbitrary coordinate flips, a larger fixed binary-clause vocabulary works.
The same count does not hold for unbounded ordered thresholds.

Draw N i.i.d. worlds X_i. Paid truthful observations give sets B_i containing
X_i; their acquisition/refinement can depend on earlier receipts. Let

    F_N = union_i B_i,
    H_N = conjunction{phi in C : every B_i implies phi}.

H_N contains every B_i and is the strongest C-conjunction that does so.
For every allowed action,

    F_N subset G_a  iff  H_N subset G_a.

The forward implication holds because every clause of G_a then belongs to
H_N; the reverse holds because F_N subset H_N. Thus compact H_N retains
*exactly* the actions safe on all observed possibilities. It need not retain
all other assertions about the sampled worlds. For product Boolean boxes,
testing a candidate unit or binary clause uses at most its two coordinates.
All M*N tests, purchased facts, subsequent action compilation and optimization
remain charged. No exponential list of full-world completions is required.

## Common coverage without a held-out sample

For any fixed C-conjunction W with population failure probability greater
than alpha, the probability that all N independent worlds lie in W is at
most(1-alpha)^N. There are at most2^M such conjunctions. Hence

    Pr{some sample-consistent C-conjunction has risk>alpha}
       <= 2^M*(1-alpha)^N.

In particular, if N>=(M*ln2+ln(1/delta))/[-ln(1-alpha)], then with confidence
at least1-delta, every such W has population failure probability at mostalpha.
This includes H_N and every common warrant formed by any subset of its
permitted actions. Choosing a permitted action after inspecting additional
information about a new world cannot leave the common success event. The
guarantee is unconditional over that new world, not conditional on a chosen
release subpopulation.

Partial receipts do not need an independent censoring assumption: B_i
contains the actual X_i pathwise, so H_N is sample-consistent regardless of
how the receipt purchases were chosen. The single uniform event covers
every refinement stage on the same N original cases, and data-dependent
selection of prices/action menus within the fixed vocabulary. Unfinished
cases remain included with their full valid B_i; discarding difficult cases
is not licensed. Changing the vocabulary or its physical effect semantics
after looking at cases needs a new complexity/selection argument.

This permits using the same cases to construct and validate the *restricted*
permission source. It pays M in the sample bound. In contrast, the earlier
independently fixed-source scalar calibration avoids that model-selection
price. Neither rule dominates the other universally. An empty permitted
menu has vacuous common coverage and supplies no useful action. A universal
safe action must actually be available if the application needs a fallback.

## A simpler retained warrant can cost fewer samples

An optional ordinary Occam bound uses a C-conjunction with s clauses. Give
each size s=0,...,M failure budget delta/(M+1), and union-bound over its
binom(M,s) syntactic formulas. Simultaneously for all sizes, every consistent
formula has risk at most

    1-exp(-(ln binom(M,s)+ln((M+1)/delta))/N),

with confidence1-delta. The empty conjunction has exactly zero risk and
can be handled directly. A shorter equivalent formula may be selected
after fitting because the union event already covers every formula.
Dropping clauses widens the warranted world set and can remove useful
permissions; this is a real task tradeoff, not costless compression.

## Quadratic dependence is a real worst-case obstruction

Take n=a+b variables split into L and R and goal G containing every
implication i=>j, i in L,j in R. For each pair(i,j), allow action a_ij that
keeps just those two variables and overwrites other left variables to0 and
other right variables to1. Its success preimage is exactly(x_i=>x_j).
Also allow the constant action setting all left0 and right1, which is safe
everywhere. The action availability here is this explicit finite menu;
do not silently replace it by a more permissive one.

Define ab worlds w_ij: among left variables only i is1; among right
variables only j is0. Each w_ij violates exactly its corresponding cross
implication. For any observed subset S of these worlds, action a_ij is
empirically safe exactly when w_ij was not observed. Consequently the
common warrant of *all* empirically safe actions intersects the grid in
exactly S. Under its uniform distribution, common-warrant failure is

    1 - number_of_distinct_observed_worlds/(ab),

which is at least1-N/(ab). Thus preserving every empirical permission can
require order n^2 examples for even a constant common-coverage target.
All2^(ab) intersections with the grid are realized by conjunctions of the
cross implications, giving a direct shattering witness as well. This is a
lower example for this rich all-permissions service, not a lower bound on
finding one useful action; the universal safe action is already available.

## Comparison and next obligation

The clause-elimination idea is directly anticipated by Valiant's
[A Theory of the Learnable](https://courses.grainger.illinois.edu/ece544na/fa2014/valiant84.pdf),
§5, TheoremA, including partially specified positive examples. Its original
concept-learning contract is not identical to this permission-service
contract; the finite-class proof above states the needed one explicitly.
Double derivation between worlds and action properties is the standard
formal-concept/Galois closure underlying permission_closure.md.

The useful developing connection is: compile a small *operational preimage*
vocabulary, refine only paid sample facts needed by that vocabulary, retain
the exact empirical action menu, and carry a common population-risk bound
through later action selection. Strong ordinary conjunction learning plus
the same action compiler ties. No new sample-saving percentage, empirical
gain, distributional validity of a real source or general learner of
mathematical truth is claimed. A small finite screen of the preimages and
quadratic counterexample is sufficient before seeking a useful acquisition
duty; a broad learning benchmark is premature.

The first learn_probe.py execution passed24 Boolean panels and108 partial-
receipt stages, checking6156 action memberships. In52 stages the compact
source strictly expanded the raw possible-world union without changing its
action menu. Four stages correctly had no available safe action. The grid
construction matched all596 enumerated subsets across four small sizes.
Runtime0.4202005seconds; no sample-saving or statistical-prevalence claim.

## What changes of scope this particular coverage event permits

On the high-confidence training event, P_X{X not in H_N}<=alpha over a
new full world on the declared coordinates. Conditional on X being in H_N,
*every sound consequence* of H_N is correct at X, not only the initial
action menu. Truthful receipts h can be conjoined and new goals may be
proved against H_N and the correct action semantics. The same common
event covers adaptively chosen queries/actions on that same world, including
goals whose preimages are outside C. The exact empirical-menu equality
does not extend to those new preimages; their inference may be conservative
or expensive. Newly introduced coordinates or changed physical semantics
still need their own adequacy evidence.

This differs from a purely task-projection adequacy promise: here a
restricted *global formula* has population coverage, so its sound logical
consequences share the same failure event. A rare receipt can nevertheless
raise conditional risk to as much as min(1,alpha/P(h)); unconditional
coverage is not uniform conditional coverage. Nor does one per-world
guarantee promise perpetual correctness over fresh worlds. For T independent
new worlds, a union bound gives at mostT*alpha failure probability on the
good training event. If the true miss probability is positive, infinitely
many independent deployments eventually encounter a miss almost surely.
