# Replacement-aware witnesses can change the required audit target

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

For a fixed repair x, let R(x) be its uniform regret against optimal repair,
and U(x) its uniform absolute repair cost. Against the better of repair and
fixed-price replacement rho, the exact uniform regret is

```math
\max\{R(x),U(x)-\rho\}.
```

This is the maximum of two suprema, not a claim that their worst cases occur
at the same world. Replacement itself has bound max(0,rho-L), where L is the
minimum compatible optimal-repair cost. A repair minimizing R alone need not
minimize this combined gate. Retain the ordinary Pareto frontier (R,U).

A small boundary: two exactly-one components choose between a known center
cost 1 and a leaf in {0,1,2}. A mandatory feature adds common A in {0,100}.
Replacement costs 100, tolerance is 2. Choosing each endpoint once has R=1
but U=103, so its combined bound is 3. Choosing the center twice has R=2,
U=102 and combined bound 2. Replacement's bound is 100. The latter repair
is therefore warranted without learning the common anchor or the leaf, while
the repair-only minimax witness fails the duty. The known center must be an
admitted public constant or a paid receipt; it is not silently free evidence.

For a star whose center has an acquired M value, give edge i integral weight
w_i and two components. Let W be the total weight of still-unknown leaves,
and C the known optimum cost of resolved edges. Each unknown edge either
balances its two choices (R contribution w_i, U contribution 3w_i) or chooses
the center twice (2w_i,2w_i). Choosing the unknown leaf twice is dominated.
Because leaves vary independently in the compatible set, these worst-case
regrets add exactly. If q is the total weight of biased edges, then

```math
R=W+q,\qquad U=A_{\rm high}+C+3W-q.
```

For a tolerated repair regret tau>=W, maximize attainable subset sum q subject
to q<=tau-W. This minimizes the absolute upper cost among all repair-regret
admissible witnesses. The remaining anchor target becomes

```math
A_{\rm high}\leq\rho+\tau-C-3W+q.
```

For unit edges, q=min(W,floor(tau-W)) and the frontier has W+1 points. For
general integral weights this is an ordinary subset-sum computation. The
source's unknown-cost coordinates and clause weights must not be confused
with physical audit fees. The chosen witness is checked against the original
clauses; an abstract count vector alone is not an output repair.

First finite rf01: n=1..6 leaves, unit weights and one seeded vector of weights
1..5 per n (seed 8141600); every subset of observed leaves and each observed
value in {0,1,2}, with center known M. Enumerate all 3^k count choices on k
unknown edges to verify the (R,U) frontier and every integral tolerance from
0 through 2W. Compare the subset-sum choice with full action enumeration.
Verify the explicit anchor boundary against every original feasible assignment
and every compatible cost world. No physical acquisitions in this first
mathematical screen. A paid continuation must acquire the center receipt and
the mandatory-feature proof, bind the source, and give the same frontier to
an ordinary controller. No unique advantage or F01 benefit is assumed.
