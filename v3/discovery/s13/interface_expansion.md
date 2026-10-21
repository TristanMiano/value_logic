# Reusing a scoped warrant after the interface changes

Codex (GPT-6), DEVELOPMENT, October20,2026. Derivation in progress.
Lineage: s12/task_adequacy.md and union_adequacy.md; ordinary forgetting and
abstract interpretation remain direct antecedents.

## Compile the warranted source, then condition it

Let F be a nonempty Boolean source, Q the original observable coordinates, and
J a fixed family of original target scopes. The previous envelope is

```math
H(F)=\bigcap_{J\in\mathcal J}\mathrm{cyl} P_{Q\cup J}(F).
```

If the supplied warrant is that the actual full world x belongs to H(F),
compile H(F) as the maintained source. Every subsequent truthful coordinate
receipt, including one outside Q, can safely condition that source. For any
new target or action, universal validity over the remaining H(F) warrants
validity at x. No new adequacy probability is spent: the same original
coverage event supports the whole adaptive stream. A contradiction is a
warrant failure signal, not license for vacuous release.

This is stronger operational scope than continuing to condition F while
requiring every future receipt to remain in Q. It does not strengthen the
original warrant or restore correlations already forgotten. In particular,
future targets can become less informative than under F. Conditioning the
weaker source is ordinary sound abstract reasoning, not a new logical rule.

For a 2-CNF source, every existential projection is 2-CNF. H(F) can therefore
be represented by the prime unary/binary consequences of F whose variable
scope is contained in some Q union J. This representation has O(n^2) possible
clauses; preparing them is paid. The old binary unit-receipt reuse algorithm
then applies to arbitrary new unit receipts, with new target-pair preparation
charged when needed. No analogous assertion follows for relational receipts.

Example: F is q=>z=>a, original Q={q}, target scope {a}. Its envelope is q=>a,
with z unrestricted. World(q,z,a)=(0,1,0) is outside F but inside H(F).
After observing a=0, H forces q=0 and can answer this new target cheaply if
observing a is cheaper than observing q. F would also incorrectly force z=0.
After observing z=1 alone, F incorrectly forces a=1 while H declines that
inference. The direct conventional model q=>a ties every sound conclusion.

## A new possible boundary: number of alternative models

For a union U of M binary sources, H(U) need not be binary. The original
branch-aware algorithm was cheap precisely because it kept U, conditioned
only on Q and queried the original target scopes. Widening receipts by
compiling the larger H(U) may trade a weaker physical warrant for harder
inference. This cost must not be omitted from the proposed extension.

Initial reduction, to be screened: put all original problem variables in Q,
add one distinct target coordinate t_j per clause, and use singleton target
scopes. For model m, let F_m be the conjunction over j of (t_j OR l_mj).
Every Q assignment extends to each F_m by setting all targets true. Thus
the envelope of the union has clause j equal to
(t_j OR l_1j OR ... OR l_Mj). New receipts setting every t_j false yield
the arbitrary M-CNF over Q. M=3 already gives NP-hard consistency of this
warranted source after interface expansion. Each original model is simple
2-CNF and can be conditioned and checked cheaply. This is a representation
and interface cost boundary, not a proof that ordinary methods cannot help.

Candidate converse: for M<=2, singleton target scopes, arbitrary unit
receipts and bounded-size projection requests, derive a reduction to a
constant number of 2-SAT instances. The disjunction of branch projections
must retain branch feasibility on Q; dropping that term is unsound. Do not
claim the converse until the decomposition and empty-source cases are checked.

## Two-model derivation

Assume a nonempty family of singleton scopes {t}, with T disjoint from Q.
Coordinates outside Q union T are unrestricted by H. Prepare
B_m=P_Q(F_m) and R_mt=P_(Q union {t})(F_m), using exact 2-CNF forgetting.
For each b in {0,1}, separate R_mt(q,b) into B_m(q) and C_mtb(q), where C
is a conjunction of unary Q literals (or true/false). All q-only clauses can
be put in B_m: every such clause implied by R_mt is implied by B_m, and
conversely. Clauses involving t become unary or constant when t is fixed.

For a set O of target receipts t=b_t, the possible Q values are exactly

```math
\bigvee_{\varnothing\ne B\subseteq\{1,\ldots,M\}}
\left[\bigwedge_{m\in B}B_m(q)\;\wedge\;
\bigwedge_{t\in O}\bigvee_{m\in B}C_{mtb_t}(q)\right].
```

Proof: in a compatible world choose B to be all models whose Q projection
contains q. For each observed t some such model witnesses its value. In the
other direction, any displayed branch gives those witnesses. Unobserved
targets can each be assigned a value supported by any model in B; they are
independent conditional on q in H. The branch need not assert that models
outside B are infeasible. An empty B is forbidden even when O is empty.

For M=1 or2, there are at most3 displayed branches. Each C is a conjunction
of unary literals. Distributing the OR of two such conjunctions gives only
binary clauses: (AND_i l_i) OR (AND_j r_j) equals AND_ij(l_i OR r_j),
with constants handled first. Hence each branch is 2-CNF. Unit receipts on
Q conjoin directly; ignored coordinates only require consistency of their
own recorded values. Bounded-size projections are obtained by enumerating
their patterns and applying this consistency check, including requested target
values among the temporary receipts. This proves a polynomial exact adapter
for fixed projection width, after charged projection preparation.

The adapter may add a quadratic number of clauses per target receipt and
requires satisfiability checks. It is NOT the previous unit-pruning work bound.
With M=3 the corresponding distribution produces ternary clauses; the preceding
reduction realizes all 3-CNF, so the count boundary is substantive.

## Hardness with a supplied consistent witness

Consistency hardness alone could look irrelevant when the physical warrant
promises a nonempty source. Strengthen the reduction. For every input 3-SAT
clause (a OR b OR c), introduce fresh w and replace its guarded version
z=1 => (a OR b OR c) by

```math
(\neg z\lor a\lor w)\;\wedge\;(\neg w\lor b\lor c).
```

This 3-CNF has the known satisfying assignment z=0, all original variables0,
all auxiliary w=0. It has a completion with z=1 iff the original input is
satisfiable. Apply the three-model construction to these clauses and observe
all their new target coordinates false. The displayed witness extends with
those false targets and is in H(U). Deciding whether z is forced false is
coNP-hard even with that witness. The witness is not the actual unknown world;
it simply certifies consistency. Giving the full actual world would trivialize
the intended question and is not part of this contract.

Every F_m in this reduction has an obvious all-targets-true extension and
consists only of clauses (t_j OR a Q-literal). These individual source models
are uncomplicated. The hard step is retaining the weaker joint adequacy
warrant while allowing new observations, rather than strengthening it back
to membership in one full model. This remains a DEVELOPMENT proof pending
small independent-formulation finite checks and closest-prior comparison.

## Linear selector encoding and action use

The quadratic clause distribution above is unnecessary for consistency.
For each fixed target receipt introduce a fresh selector s and encode
(s => AND L_1) AND (not s => AND L_2). Each resulting clause is binary.
Existentially eliminating s gives (AND L_1) OR (AND L_2). A false arm forces
its selector off; an empty true arm adds no clauses for that arm. The two-model
branch therefore needs O(|Q|) literal incidences per receipt, not O(|Q|^2),
after prepared projections. Include its new selector in the 2-SAT variable
count. The singleton model branches remain necessary if the other model's
Q projection is incompatible. This is a standard selector encoding.

With q=|Q| and r observed original targets, at most three 2-SAT instances have
O(q+r) variables and O(q^2+rq) clauses. A bounded-width new projection of width
k requires at most 3*2^k such checks, plus receipt handling and preparation.
This is an upper bound, not a measured improvement or an optimal dynamic
algorithm. Repeated fresh checks can be expensive; no unit-only cache bound
is claimed. Unobserved original target variables are existentially eliminated
using their guaranteed extension in each eligible branch, not encoded this way.

For a new binary-CNF target under coordinatewise toggles, request its required
pair projections from this adapter, then use s12's permission compiler. Each
possible source pair forbids the toggle pattern that would falsify a target
clause. The resulting safe-toggle formula is again 2-CNF. Thus the two-model
adapter supports an entire safe action menu after expanded observations,
even though H itself need not be 2-CNF. For example, F1=(q OR t), F2=(r OR t),
Q={q,r}, T={t} yields H=(q OR r OR t), which is not binary-definable.
It is the fixed-value query adapter that stays tractable, not a nonexistent
binary representation of the full envelope.

The finite [screen](expand_probe.json) checks90 one/two-model panels,
1350 receipt contexts and5400 requested two-coordinate patterns against world
enumeration. It also checks24 three-model CNF reductions. All passed in one
combined0.1462681-second run. The executed version uses distributed clauses;
the selector improvement is presently a derivation only. Neither finite screen
proves the unrestricted claim nor supplies independent confirmation.
