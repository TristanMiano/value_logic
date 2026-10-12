# S21: computation attempts that can fail

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
Extends [S20](graph_values.md). A timeout means no receipt, not a false fact.

## A useful failure of the batch reduction

Two facts have weights 1/2 each. Their parity can be attempted at cost 1/100,
with independent success probability 1/2. One fact can be anchored exactly at
cost 3/8. No other queries are available. On parity success, buy the anchor;
on failure, stop and guess fairly. Relative to the 1/2 guessing baseline,
expected gain is (1/2)(1/2-3/8)-1/100=21/400=0.0525. Every fixed batch has gain
at most zero: the joint batch gains (1/2)(1/2)+(1/2)(1/4)-3/8-1/100=-1/100;
anchor alone gains -1/8 and parity alone -1/100. Adaptation to computational
success matters even when truth labels do not affect the planner's value.
These are specified exact query prices and success laws, not measured runtimes.

## Optional all-or-nothing bundles

If k independent receipt attempts must all succeed to deliver value V, failures
end the bundle and attempt i costs c_i with success chance p_i. For a fixed
order, expected gain is V product p - sum_i c_i product_{j before i} p_j.
An adjacent exchange puts i before j exactly when c_i(1-p_j)<=c_j(1-p_i).
Thus increasing c_i/(1-p_i) minimizes the expected invoice; p_i=1 comes last
(zero-cost ties harmless). Execute the best order only when its gain is positive.
If the full gain is positive, every reached successful-prefix suffix also has
positive continuation gain: the preceding invoice was nonnegative and the
prefix success probability positive. No later elective stopping is needed.
This relies on independence and no partial reward or alternative route.

[Deshpande, Hellerstein and Kletenik](https://arxiv.org/pdf/1303.0726),
sections 1–2, describes the standard product-distribution, paid-bit sequential
testing problem and the known optimal ratio orders for AND/OR evaluation.
Those sections were read; no approximation theorem was imported. Our optional
reward/receipt reading changes the application, not the exchange argument's
priority. Unlike mandatory evaluation, a reasoner may choose not to buy a bundle.

## Robust lower success probabilities, without a truth prior

Let K record successful node/edge observations and R the untried attempts.
Let r(K) be half the total weight of anchored vertices. Each attempt j costs
at most c_j and, conditional on every permitted history and fixed truth world,
has success probability at least l_j. Successful labels are exact and checked;
failure need only disclose that no receipt arrived. Define the ordinary finite
Bellman function

```
V(K,R) = max(r(K), max_j [-c_j + l_j V(K+j,R-j)
                              + (1-l_j) V(K,R-j)]).
```

Here c_j is charged in full even on failure. More successful information cannot
reduce V: the controller can ignore it, with the same remaining attempts.
Consequently success-child V is at least failure-child V. The policy selected
at l_j guarantees at least V under ANY conditional success chances >=l_j,
even if they depend on history or world: backward induction replaces actual
child payoffs by their V lower bounds, then uses this monotonicity. At stopping,
anchored predictions are correct and fair guesses give half credit on every
other fixed fact. This gives baseline+V for every truth assignment. No uniform
epistemic prior or independence across attempts is needed for the lower bound.

It is also exact minimax for this broad conditional-success class: the class
contains independent success coins with probabilities exactly l, fixed costs c,
and every truth assignment. Average any candidate policy under uniform truth
bits and these coins; label outcomes cannot improve the terminal component
value. Its average is bounded by the displayed Bellman optimum, so its worst
world/law cannot do better. An observation interface may disclose extra timing
information, but the lower policy may ignore it; exact minimax uses the allowed
no-extra-information law for its upper bound. A smaller real environment need
not admit that least-favorable law and can have a larger value.

## What must be learned, and what cannot be silently assumed

For the two-fact example with parity success probability p, adaptive gain is
p/8-1/100, profitable iff p>0.08. On a repeated iid task source a lower
confidence bound for a shared p can guide this threshold. Its training invoice
must be amortized across subsequent tasks. An average success estimate across
contexts is NOT a lower bound conditional on every logical instance/history.
It therefore cannot justify the robust theorem above. Source-distribution
guarantees and per-world guarantees are distinct, even when their numerical
policies coincide. Learned model adequacy remains a substantive obligation.

## Prospective cheap check

Use new Node sources and exact scaled integers, seed 81497, 24 small random
trees (2–4 nodes), independent success probabilities on a quarter grid and
nonnegative attempt prices. Compare collapsed success-state Bellman planning
with fixed-batch enumeration; for the first 12 cases also use explicit worlds
and receipt-label outcomes. Re-evaluate the lower-probability optimal policy
against a rectangular adversary choosing interval endpoints after each history.
Preserve all cases, including zero gains. Include the exact two-fact separation
and 12 all-or-nothing bundles against all order permutations. No large-experiment
campaign: this screens algebra and the proposed state compression only.

## Observed screen

[Exact Node result](failure01.json): 24 cases, 9,858 collapsed states and
batch-outcome comparisons, 18,608 explicit-world states on the first 12 cases.
Seventeen cases have positive acquisition value; fourteen strictly improve
over all fixed batches. The endpoint adversary matches every lower-probability
policy value. Twelve bundles, with 84 total tested permutations, match the ratio
order and optional-stopping recursion. This is a small exposed design screen;
the low-order pseudorandom draws do not ensure comprehensive shape coverage.
The two-fact separation is exactly 0.0525, as derived. No learned success law
or external solver economics has been established.

## Regenerative retries change the result again

Suppose each failed attempt leaves the complete decision-relevant state unchanged,
can be retried, costs c, and succeeds with the same independent probability p>0.
At an information state, the retry term is -c+p V_success+(1-p)V_current.
The Bellman inequality is equivalently V_current>=V_success-c/p. Conversely,
repeat until success to realize the effective price c/p. Thus unlimited
regenerative attempts reduce exactly to deterministic successful observations
at expected prices c/p. S20's tree DP applies again. This is ordinary stochastic
shortest-path reasoning; regeneration is a substantive state assumption.

With only conditional success lower bounds l>0 and cost upper bounds c, the
same fixed-batch execution has expected invoice at most sum c/l and terminates
almost surely. The worst-case guarantee holds without independent attempts.
The independent constant-l, fixed-c law attains the least-favorable value,
so the reduction is again exact minimax for that broad environment class.
It is an expected-cost guarantee with an unbounded possible invoice, not a
hard deadline. Restarting deterministic code with the same seed is not a new
independent attempt; cache mutation or informative failures can break regeneration.

For a fixed forest plan, cap query j at k_j fresh attempts. Write
q_j=1-(1-l_j)^k_j and C_j=c_j*q_j/l_j. Conditional on any preceding history,
success probability is at least q_j and expected attempt cost at most C_j.
This follows by summing the geometric upper bound on the no-success tail.
When every selected query is attempted regardless of earlier failures, a node
with a selected anchor-to-node witness path P_v is covered with probability at
least product_{j in P_v} q_j. Its expected acquisition gain is therefore at least
sum_v r_v product_{j in P_v}q_j - sum_j C_j. This bound pays for attempts made
in disconnected components; it does not pretend they were useful.

## A cheaper executable capped policy

Choose one possible anchor as root and orient the physical tree away from it.
Only attempt an edge after its parent vertex has been resolved; on capped
failure, abandon that descendant branch. Let B_v be the best guaranteed
additional prize below an already resolved v. Bottom-up,

```
B_v = sum_{child u} max(0, q_(v,u) * (r_u+B_u) - C_(v,u)).
anchor_gain = max(0, q_anchor * (r_root+B_root) - C_anchor).
```

The policy ignores branches with nonpositive contribution. All continuation
rewards are nonnegative, so the same conditional success/cost bounds give a
worst-world lower guarantee by induction. Under the independent endpoint law
it is exact for this declared rooted, single-anchor policy class. It is not an
optimizer over arbitrary orders, disconnected anchors or fallback routes.
Without caps, q=1 and C=c/l, recovering rooted prize-subtree selection.

For n vertices, messages for both directions of every edge can be computed in
two passes: M_(v->u)=r_v+sum_{z != u} max(0,q_(v,z) M_(z->v)-C_(v,z)).
Each anchor's value then uses its complete incoming sum. Nonnegative terms and
a cached total permit O(n) arithmetic for ALL anchor choices; solving separately
for each root would cost O(n^2). This produces an executable acquisition policy
and bound with supplied prices/caps/probabilities. It still needs a meaningful
source of those probability bounds before it is a useful reasoner.

Exact rational messages can grow large along long paths. A constructive numeric
alternative rounds each nonnegative edge contribution downward/upward to a
grid of width 1/D. Multiplication by q<=1 and positive-part are nonexpansive,
so a directed subtree's interval width is bounded by its number of edges / D;
the final anchor interval has width at most n/D. In two-pass rerooting, subtract
the exact stored child contribution from the cached sum on each side; do not
subtract unrelated interval endpoints, which could enlarge uncertainty.
Choose the root and branches from lower messages. The resulting policy's true
value is at least its lower score, while the largest upper anchor score bounds
the best policy in the declared class. Safe integer/BigInt arithmetic checks
the certificate without floating-point roundoff assumptions.

Prospective implementation: 32 fresh 2–7-node trees, seed 92741, compare every
anchor and rooted connected subtree using exact rational arithmetic. Check
lower/upper inclusion and the n/D width bound; inspect all cases. Then compute
all-root bounds and one policy on 4,096-node path/star/random trees at D=10^9,
separately recording source, planning and policy reconstruction costs. The
ordinary comparator is this same rerooting DP, not an exponential table.

[Capped-policy result](capped01.json): 32 fresh trees and 3,148 exact rooted
subtree evaluations satisfy the intervals, chosen-policy guarantee and n/D
width bound. On 4,096-node path/star/random trees, all-root planning took
8.65/8.46/9.26 ms, with 0.01/0.88/0.42 ms for one policy's reconstruction.
The score interval widths were 5e-9, zero and 1.67e-7 in the input prize units.
Selected policies cover 26/2,311/2,291 vertices **if their required attempts
succeed**; those counts are not expected resolved-fact counts. The lower
scores already discount failures and invoices. These measurements cover the
planning kernel with supplied probability/price bounds, not solver execution.
