# Three-level costs, adaptive star audits and learning from paid receipts

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
Extends [action audits](action_audits.md). The optional AND ordering and its
robust continuation argument are inherited from [S21](../s03/failed_queries.md),
not new discoveries. The present question is whether that existing principle
can use **actually acquired** cost observations in a checked repair service.

## Binary coverage does not transfer unchanged

Keep the independent exactly-one edge-action source, but let each cost value
be in {0,1,2}. An observed endpoint at 0 or 2 determines an optimal choice
against every possible other endpoint. An observed endpoint at 1 does not:
the unobserved neighbor may be 0 or 2. With zero regret tolerance, both
endpoints must then be audited. The one-edge counterexample already invalidates
the binary vertex-cover sufficiency rule for this source.

The exact zero-tolerance stopping condition on a graph is: every edge has an
audited extreme endpoint, or both endpoints have been audited. In particular,
one queried middle vertex forces every still-unqueried neighbor. This is an
instance of graph orientation under explorable uncertainty. The literature
already treats that general problem; our three-level ties and the exact
restricted star formula below need their own hypotheses.

## Exact optimal expected audit fee for an independent star

Consider a star with center audit fee C>0 and leaf fees L_i>0. Fresh vertex
values are mutually independent. Write p_0 for the probability that the center
is extreme and p_i for the corresponding leaf probabilities. The split of
extreme probability between 0 and 2 does not affect query sufficiency. This
probability model optimizes expected acquisition fee; terminal action
correctness still uses a pathwise checker over all compatible source values.

Querying the center first costs

```math
B(S)=C+(1-p_0)\sum_{i\in S}L_i.
```

If a queried leaf is middle, the center becomes mandatory. Query it immediately:
delaying that required query cannot avoid its fee and may buy other leaves
that an extreme center would make unnecessary. Independence means that earlier
leaf outcomes do not change the unqueried center or leaf distributions.
If the center is middle, all remaining leaves are mandatory; if extreme, stop.

Before querying the center, the only continuing histories contain extreme
leaves. Let V(S) be the least expected future fee for the remaining star.
For nonempty S the Bellman recurrence is

```math
V(S)=\min\left\{B(S),\min_{i\in S}
\left[L_i+p_iV(S\setminus\{i\})+(1-p_i)B(S\setminus\{i\})\right]\right\}.
```

Here B(empty)=C but V(empty)=0. Defining D(S)=B(S)-V(S) gives

```math
D(\varnothing)=C,\qquad
D(S)=\max\{0,\max_{i\in S}[p_iD(S\setminus\{i\})-p_0L_i]\}.
```

This is exactly the inherited optional AND-bundle recursion, with reward C,
success probabilities p_i and effective attempt fees p_0*L_i. An optimal
non-center-first policy tests leaves in increasing L_i/(1-p_i) until the
first middle result, then executes the forced center/fallback route. The
comparison with center-first is

```math
D_\pi=C\prod_i p_i-p_0\sum_k L_{\pi_k}\prod_{j<k}p_{\pi_j}.
```

Choose this route iff its maximum D_pi is positive. Positive full-route gain
implies positive continuation gain along every all-extreme prefix, by the same
AND-bundle argument; no profitable route needs an elective center query after
an all-extreme proper prefix. This is an exact expected-fee result under the
stated source, not a bound on every realized invoice. Worst-case all-middle
outcomes still require every vertex, regardless of the prior.

## Learning the required probabilities without full value identification

On independent fresh repeated star rows, deciding to audit an unseen vertex
using only earlier rows and other vertices in the current row does not inspect
that vertex's current value. Its extreme/middle outcome still has mean p_i
conditional on the selection history. Therefore the success observations
collected at each vertex's adaptively selected audit times are valid Bernoulli
samples under this admitted product-source contract. Source independence is
substantive: correlated current-row values can invalidate this conclusion.

The observed extreme indicator is enough for acquisition-fee prediction; the
actual value receipt is still retained for constructing the repair. There is
no need to infer the separate probabilities of 0 and 2 merely to order audits.
No observation is acquired for free: the service pays for every receipt, even
when its statistical reuse adds no further physical query. Computation,
storage and confidence updating remain additional costs.

A common time-uniform confidence event for all vertices and sample counts
can be obtained by allocating failure alpha/(m*n*(n+1)) at sample count n
for each of m vertices and using ordinary two-sided Hoeffding intervals.
The sum over n>=1 is alpha/m. Union over vertices and counts covers later
adaptive choices. A practical implementation may use a conservatively checked
rational radius rather than silently relying on floating-point tail rounding.
This is an imported concentration argument, not a new statistical theorem.

If that event gives p_i>=l_i for leaves and p_0<=u_0, optimize the optional
AND value using l_i and effective fees u_0*L_i. When the resulting lower gain
is positive, the chosen leaf-first route improves expected **physical fee**
over center-first by at least that lower gain for every parameter vector in
the box. This follows from the robust S21 continuation argument, or direct
induction on positive suffix values. It does not yet pay confidence/planning
overhead or prove a complete-cost benefit. If the lower gain is nonpositive,
center-first is an available correct fallback; this is uncertainty about
performance, not uncertainty about the emitted action's validity.

## Prospective development steps

First compare the closed form with a fully enumerated query-history Bellman
solver on small stars, including unequal fees, endpoint probabilities and
all three-value outcomes. Then implement a bounded repeated service with a
durable source declaration, physical query log, receipt-based confidence
updates and checked terminal actions. Compare an oracle law only as a
diagnostic, center-first, full identification, and the identical ordinary
AND-ordering learner. Charge source admission and all learning work. Preserve
source-shift/correlation counterexamples rather than transferring the
independence guarantee without a new admission argument.

This is S21/S29 development. It neither promotes a candidate nor changes F01.
