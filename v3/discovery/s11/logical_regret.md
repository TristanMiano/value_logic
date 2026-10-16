# Paid queries and output revision under checked logical constraints

Codex (GPT-6), DEVELOPMENT. A distinct source extension of S01/S11, connecting
the P3-03 outer-source interpretation to the paid query/revision construction.
The proposed delta is a compact exact regret planner for structured logical
uncertainty, without supplying probabilities for unresolved facts. It uses
ordinary cost-network optimization; novelty and practical usefulness remain
to be assessed against that literature.

## Explicit source and operation contract

Let the unresolved signs x_i belong to {-1,+1}. Checked or explicitly assumed
local relations define a nonempty finite set F of admissible answer vectors.
The actual intended vector must belong to F for the conditional guarantee to
apply. F need not consist of complete models of arithmetic; it is the finite
outer source warranted by received premises. A fallible model's agreement is
not a checked relation. Finding or checking these relations has a separate cost.

The allowed source laws are ALL probability laws supported on F. This is a
worst-case decision criterion, not a claim that unknown mathematical truth is
random or that a uniform law is justified. A controller may privately randomize,
purchase at most r designated original signs, and revise individual output
signs. Query/flip fees are fixed and nonnegative; at most H operations occur on
each path. Terminal zero costs zero, terminal one costs the sum of the revised
weighted signs plus paid fees. Revisions change the specified output only:
they do not rewrite the original logical source or infer a causal intervention.

The comparator is the same menu of feasible procedures chosen with knowledge
of the source law, as in the preceding regret construction. It does not see
the controller's private random seed. For a point-mass source at x, it already
knows x through the law and buys no queries: every query can be removed from
its realized path without increasing cost or using more operations. Its best
cost is therefore

```math
B(x)=\min\left\{0,\ \min_{F'\subseteq[m],\ |F'|\le H}
 \left[\sum_i w_i x_i-2\sum_{i\in F'}w_i x_i
       +\sum_{i\in F'} f_i\right]\right\}.
```

For any fixed controller pi, its worst-source regret is exactly

```math
\max_{\mu:\mathrm{supp}\mu\subseteq F}
 \left[C_\pi(\mu)-\min_\tau C_\tau(\mu)\right]
=\max_{x\in F}\{C_\pi(x)-B(x)\}.
```

Proof: for every law, its best fixed procedure has expected cost at least
the expectation of B(x), so regret is at most the maximum displayed pointwise
regret. A point mass at any maximizing x attains equality with its tailored
query-free comparator. This does not permit the adversary to select a new
truth after each observation. One fixed x is enough for the worst case.
Known moment or mass constraints can remove point masses and invalidate this
reduction; that is a different, harder source model.

## Structured separation for a fixed controller

The existing private-reach flow represents a controller exactly. Conditional
on a full cell z of the r queryable signs, its expected cost has the form
C_pi(z)+sum_i w_i*s_zi*x_i, with s_zi in [-1,1]. These are private-mixture
expectations, not truth probabilities. They are affine in the flow variables.

Enumerate the at most 2^r cells. Clamp queried signs to z and maximize either
the terminal-zero regret expression, or

```math
C_\pi(z)+\sum_i w_i(s_{zi}-1+2b_i)x_i-\sum_i f_i b_i,
\qquad b_i\in\{0,1\},\quad \sum_i b_i\le H,
```

subject to the checked logical relations on x. Each added flip bit b_i has
only a local interaction with its truth bit x_i; the global operation count
is carried as a dynamic-program state. A supplied bounded-width tree
decomposition of the relation graph yields an ordinary max-sum elimination
with a count index. For a chain of binary relations the states are simply
(position, last sign, number of flips), and each step has at most four local
sign/flip extensions. This gives O(2^r*m*H) arithmetic for separation, with
exact rational values and an attaining truth/flip witness. Terminal zero is
a separate O(2^r*m) chain problem. An empty clamped source is skipped.

For a general bounded-width tree decomposition, combine count profiles at
joins; a straightforward bound is O(2^r*N*H^2*2^(w+1)), up to decomposition
degree and local relation-table factors, where N is decomposition size and
w+1 the largest truth bag. This is a structural claim, not an implemented
general-tree solver. Width, decomposition discovery and relation checking
are not free. A chain admits arbitrary allowed pairs, including implications,
exclusions, equalities and sign reversals; it is more general than aliases.

## Compact minimax formulation and certificate route

For every cell, comparator terminal mode and dynamic-program state, introduce
an upper value variable. Each feasible local transition supplies a linear
inequality: parent upper value >= local affine regret score + child value.
Root inequalities bound total regret. Minimize that bound jointly with the
private-reach controller flow. Backward induction shows every feasible value
assignment dominates every complete adversarial path; setting values to the
exact dynamic program attains equality. Thus the compact LP optimizes the
full randomized controller class represented by that flow.

The chain's adversary block has O(2^r*m*H) size in addition to the O((m+r)*3^r)
controller flow, before accounting for explicit affine incidence. Sparse
coefficient maps must be retained rather than blindly substituted if claiming
that compact storage. Exact rational checking of a feasible controller plus
the adversary DP supplies an upper certificate. A rational LP dual with
explicit residual/bound correction can supply a lower certificate, as in
the preceding independent-mean prototype. This LP extension is currently
derived only; the next cheap screen targets the fixed-controller separator.

## Closest literature and what is inherited

[Boutilier, Patrascu, Poupart and Schuurmans](https://www.cs.toronto.edu/~cebly/Papers/minimax-CP.pdf),
sections 2.3 and 4.2, already formulate constraint-based minimax regret and use
cost-network variable elimination to replace exponentially many adversarial
inequalities by local epigraph inequalities. Their stated source is incomplete
factored utilities and their decision is a configuration. Our proposed
adapter has paid adaptive observations, private-mixture flow and output
revisions, with logical constraints on the unknown original answers.
Do not attribute the cost-network LP construction itself to this session.

[Unifying Tree-Decomposition Schemes for Automated Reasoning](https://ics.uci.edu/~dechter/publications/r92a.pdf),
sections 2–3, Definition 3.1 and Theorems 3.2–3.3, give the general
cluster-tree decomposition framework, its correctness and width-dependent
complexity. The truth/flip count messages here instantiate that ordinary
machinery. A conventional planner with the same source and reduction ties.

Compared with the existing finite outer-cover service, the prospective gain
is exact structured regret and paid-query planning without enumerating all
truth vectors, for a declared low-width class. It is not a general learner
of mathematical uncertainty or evidence that arbitrary mathematical tasks
have low width. A source with no useful checked structure may still be hard.

Prospective screen: a few small chains with varied relations, signed/zero
weights, mixed policies, zero/positive fees and H boundary cases; compare
against explicit truth/flip enumeration. Include one longer chain solely
to record state counts. Do not undertake a broad benchmark before deciding
whether the literature leaves a useful adapter-level contribution.

## First screen and its limits

The [six declared cases](lc01/attempts.jsonl) passed on their first attempts.
The executed [chain separator](logical_chain.py) has SHA256
`57b9296e48d488c314691ef9a97b20e7c05f1cdcec56dbee7835ab4f644ff7c1`.
The small cases compare exact rational answers with all feasible truth/flip
pairs; the larger case has 257 original signs and four queryable signs. Full
inputs, three-policy private mixtures, witness assignments and operation
counts are retained. These are fixed-controller results, not an executed
minimax LP, a learned source or an empirical deployment comparison.

Low width of the logical source does not by itself make arbitrary adaptive
query planning cheap. The present flow retains up to 3^r histories and the
separator enumerates 2^r query cells. An unrestricted r=m query menu can
therefore defeat this compactness even when source relations form a chain.
For a fixed H, the reachable partial-history count is at most
sum_{k=0}^{min(H,r)} binomial(r,k)*2^k, but a controller's many conditional
response terms can still couple distant truth variables. Do not remove the
query-cell factor merely because each execution sees at most H answers.

The next constructive implementation will encode that chain LP with explicit
cell coefficient variables, retaining sparse feature equalities. Its declared
first panel reuses the five small lc01 inputs and truncates the large source
to m=31,r=3,H=4. Compare the compact program with a truth-enumerated LP on the
small sources, reconstruct rational upper/lower certificates, and compare
with the same controller class prohibited from buying queries. The ordinary
cost-network implementation is the relevant equal-information counterpart.
This is developmental construction, not a promotion or empirical confirmation.

Executed [ll01](ll01/attempts.jsonl): all six compact LPs and six no-query
controls completed on first attempts; ten small truth-enumerated LPs matched
the numerical optima, and exact fixed-controller truth/flip enumeration
matched each repaired policy's upper bound. Executed source
[logical_lp.py](logical_lp.py), SHA256
`0f51a5b3eb13a6f6c45b8747995c2a896ef759e0eaa8816e084c62b86414ce63`.
All outputs retain exact rational lower/upper certificates and dependency
hashes. Query fees and flip fees are included in the objective; planning,
relation acquisition and checking still have no common monetary price.

| Case | m / r / H | Optimized regret with queries, approximate interval | Optimized regret without queries, approximate interval |
|---|---|---|---|
| 0 | 4 / 0 / 0 | 6 exactly | 6 exactly |
| 1 | 5 / 1 / 1 | [2.933035, 2.933037] | 5.25 exactly |
| 2 | 6 / 2 / 3 | [7.101562, 7.101563] | [9.028645, 9.028649] |
| 3 | 7 / 2 / 8 | [9.011111, 9.011119] | [10.164062, 10.164063] |
| 4 | 6 / 0 / 2 | 7 exactly | 7 exactly |
| 5 | 31 / 3 / 4 | [17.713541, 17.713550] | [21.218749, 21.218756] |

The decimal intervals are presentation summaries; the rational output is the
certificate. The 31-sign program uses 2351 variables, 3868 inequalities and
13,941 nonzero coefficients. Paid queries reduce its certified worst-case
regret by at least 16.519% against the optimized no-query class. This is
a different capability comparison from an economic gain against an ordinary
equivalent with the SAME query access. Such an ordinary planner ties. The
case is exposed development, and no independent mathematical review or broad
empirical transfer evidence is supplied.

A more general fixed-controller separator can factor its expected cost over
the scopes of its actual response terms and run elimination on the UNION of
those scopes and the source-relation graph. It is that augmented width which
controls complexity. A one-query rule whose answer changes every output adds
a star of interactions; many such query alternatives can create a large
bipartite interaction graph even when every source relation is unary.
This is a useful guard against silently treating paid information as a local
change to an otherwise tractable source.
