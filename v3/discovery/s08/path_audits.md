# Exact adaptive acquisition on a three-level path

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
Prospective extension of the [star duty](star_audits.md). A full query-history
Bellman representation grows exponentially even when the cost-source graph
is a path. The construction below retains only intervals and a forced-endpoint
state. It is ordinary stochastic dynamic programming with an explicit source
decomposition, not a claim to have invented that method.

## Model and forced observations

Original feasible actions are the independently checked two-choice edge
factors already declared for the three-level source. The graph is the path
1..n; fees c_i>0 are fixed, and independent fresh values t_i lie in {0,1,2}.
Write p_i for the probability of an extreme value. The requested regret is
zero for every compatible completion. Positive edge cost scales do not
affect this zero-tolerance query duty, but remain in the action cost map.

An audited middle vertex forces each unaudited neighbor: the incident edge
cannot be resolved while that neighbor remains unknown. A forced query can
be made before elective queries without increasing expected cost. It is
unavoidable regardless of the other outcomes, and its observation may make
elective work unnecessary. Once forced observations propagate to extreme
boundary values, the remaining unqueried components are independent paths.
All edges to the observed extreme boundaries are already resolved.

## Three interval tables

Let V(a,b) be the minimum expected future fee for the ordinary remaining
interval [a,b]. Let F_R(a,b) impose that its rightmost vertex must be audited,
because of a middle vertex just outside that endpoint. Define F_L similarly.
Empty intervals have all values zero. An ordinary singleton has V(a,a)=0:
it has no unresolved edge and need not be identified. A forced singleton has
F_R(a,a)=F_L(a,a)=c_a.

The forced-endpoint recurrences are

```math
F_R(a,b)=c_b+p_b V(a,b-1)+(1-p_b)F_R(a,b-1),
```

```math
F_L(a,b)=c_a+p_a V(a+1,b)+(1-p_a)F_L(a+1,b).
```

For b>a, condition on the first elective query i:

```math
V(a,b)=\min_{i=a}^b\left[
c_i+p_i\{V(a,i-1)+V(i+1,b)\}
 +(1-p_i)\{F_R(a,i-1)+F_L(i+1,b)\}\right].
```

If i is extreme, both remaining intervals are ordinary. If middle, their
adjacent endpoints are forced. The two components have independent unobserved
coordinates and disjoint action/fee duties, so their optimal expected fees
add. Any interleaving of their query policies cannot improve on that sum.
Conversely the minimizing root and recursively selected component policies
attain every recurrence. Induction on interval length gives exactness.

Compute by increasing interval length; both F tables depend on shorter
intervals and V's candidates do too. There are O(n^2) stored states and
O(n^3) candidate arithmetic operations, with O(n) actual queries per request.
These are arithmetic counts, not constant-cost rational bit-complexity claims.
Store chosen roots as well as values so execution does not redo planning.

## Conservative source probabilities

Suppose every vertex's conditional extreme probability, before its query,
is at least l_i under the admitted source. Evaluate the tables at l_i and
follow the resulting policy. A forced-endpoint duty contains the ordinary
duty plus a compulsory query, so F_R(a,b)>=V(a,b) and F_L(a,b)>=V(a,b).
Thus each action's middle child costs at least its extreme child in the
bounding recurrence. Replacing the actual conditional probability by l_i
can only raise the expected upper bill. Induction gives the same table value
as a safe bound even if those conditional probabilities are larger.

Care is needed: this last statement uses conditional lower bounds after
every permitted history, not merely marginal extreme frequencies. For a
stationary independent fresh-row source, a simultaneous confidence event for
the p_i provides the required bounds. For correlated source values it does
not. The original-source action checker remains valid without that statistical
claim, but its expected-cost certificate must be withdrawn or re-admitted.

The independent product law at exactly l_i attains the upper bound for the
optimal policy. It also lies in the broad conditional-probability class, so
the table is exact minimax for that declared class, provided the interchange
of mandatory/elective queries remains justified by the conditional model.
**Open proof duty:** history-dependent laws may invalidate the simple
interchange argument. Keep the exact optimality claim restricted to the
independent product law until that extension is resolved; the upper guarantee
for the explicit policy can be checked separately by induction.

## Next developmental check

Compare against an independent full three-value query-history Bellman solver
for n<=7, unequal fees and probability endpoints. Check every output on all
small source realizations, retain a tampered-source control, then measure
table construction and actual query work for longer paths. Use the identical
ordinary interval DP as the strong comparison. This is a proposed compact
integration, not a fresh readiness event or an empirical superiority claim.
