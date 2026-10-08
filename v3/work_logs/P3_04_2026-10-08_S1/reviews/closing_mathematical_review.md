# P3-04 closing mathematical self-review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
This is self-review, not an independent or blind reconstruction.
The reviewed objects are the finite selector, its paired/signed-Horn adapters,
and the main C04 and companion CE04 statements. No P3-05 transport task or
contribution gate is attempted.

## 1. Selection, coverage and nonemptiness

C04-1 uses strictly positive weights: deleting a satisfied extra soft constraint
strictly worsens its tier and cannot be a minimum deletion repair. A zero weight
would invalidate that exact minimal-deletion correspondence, although the
ordinary numerical optimum can still exist. Constraint identities determine
which penalties are distinct; equal formula text is not sufficient reason to
merge them. C04-7's complete iff gates preserve each original formula's value
and charge one soft root per identity, so they preserve the objective, not just
satisfiability. Treating each clause of a split conjunction as a separately
weighted preference fails the shown two-state comparison.

The branch-and-bound invariant concerns the full feasible family of the fixed
request. Hard-discharge bounds cannot remove a feasible singleton. Rank pruning
uses a feasible incumbent and strict `lower > incumbent`, never equality.
The retained frontier plus all currently best witnesses therefore covers every
true minimizer. If an incumbent later improves, cases previously pruned were
already strictly worse than an older, no-better bound and remain safely excluded.
A seeded witness does not remove any frontier. Rediscovery is deduplicated.

A rank-exact report requires every remaining eligible lower bound to reach the
incumbent rank. This certifies that all recorded best witnesses are optimal,
not that unseen ties are absent. An identity-complete report requires no eligible
frontier, including cells discharged during reporting itself. A feasible
witness proves existence of some global minimum only because the declared
family is finite; the infinite `1/n` example defeats the analogous attainment
claim without that premise or another finite-rank/compactness argument.

C04-6's exact-value and common-action shortcuts require a nonempty target and
sound bounds on the whole minimizer cover. An unknown or empty feasible family
has no action warrant. A constant outer value can be exact before optimum rank
is known. An endpoint seen only in an unproved-optimal incumbent cannot certify
that endpoint is in the selected image. Exact interval hull, exact finite image,
all identities and optimum rank are deliberately different output services.

## 2. Hypothetical truth rules and genuine scope

The ordinary interpretation of `p and not p` remains inconsistent, independently
of the actual factual reference. Its paired-support witness changes the
hypothetical consequence relation explicitly; it is not an ordinary model of
that sentence, a bit-flipped report, or a renamed antecedent. Frame preservation
of the unrelated q coordinate is a declared relevance commitment. Removing the
frame widens consequences; the favorable framed cost is not learned from a
numeric value or claimed to be uniquely philosophically correct.

CE04-4's gap-exclusion proof uses monotonicity of **both support components**
in the information bits. Turning a permitted neither-pair into a true-only pair
preserves every positive-support formula and improves the isolated first
normality tier. Ordinary hard frame atoms cannot have been gaps. Competing
first-tier penalties or arbitrary meta-level negative bit constraints defeat
the argument. Later lexicographic tiers do not. CE04-5 then uses the separate
fact that gap-free formulas cannot have both support bits zero. Failure of
universal negative support supplies the old minimizing witness needed to keep
the old rank attainable. Without that condition, its displayed gap separator
applies. All these consequence laws require fixed permissions, background,
frame and ranking across the compared antecedents.

Material implication is not an executable inference rule. Gap-free paired
states can support every ordinary tautology, yet support A and A implies B
without supporting B. The signed-Horn adapter instead makes a specifically
chosen implication between ordinary support bits a hard primitive. Its least
closure contains every closed admissible support state by induction on rule
firings. The retained ordinary reference bit at every atom precludes gaps.
Every additional bit beyond the least closure creates a new abnormal atom,
so a positive isolated normality penalty makes the feasible least closure the
unique minimum. A forced conflict outside the permission set certifies
infeasibility of that policy, not impossibility of all hypothetical semantics.

The arithmetic quotations `2=3`, `2+2=3+3` and `0=1` retain the usual integer
reference. Their reference truth and the choice of addition/cancellation rules
are exposed inputs. The code checks the finite closure, not arbitrary arithmetic
or the relevance of an inference schema. Keeping cancellation propagates an
additional conflict rather than magically preserving ordinary equality.
This supports a finite genuine counterpossible, not every counterpossible.
The fixed falsity constant remains unsupported in every admitted paired case;
that is an explicit limit of this compositional semantics.

## 3. Source uncertainty, payoff interpretation and policy uncertainty

CE04-6 keeps each unresolved source's minimum repair family before unioning.
Joint minimization over a source and a repair can silently select a convenient
source. Numerical union nonemptiness does not establish a defined hypothetical
for every source, and per-source existence does not produce an executable
common replacement under hidden source information. Unknown source branches
remain in the outer report even when only other branches have witnesses.

CE04-12 is a ranked-selection statement, not merely P3-03 source nesting:
restricting the feasible family preserves old selected cases exactly when an
old minimum survives. Otherwise the new optimum can have wholly different
costs. The result here is a boundary on a fresh selection request; it is not
the later general proof-reuse theorem.

The ordinary-compatible payoff decoders t and 1-f disagree on a both-pair.
Ordinary payoff observations alone cannot identify that extension. A normal
query subfragment is the positive exception **when the hypothetical decoder
is required to depend on that same subfragment**: its truth-functional payoff
then has no such conflict ambiguity. Ordinary-data dependence alone does not
force that hypothetical locality. This premise was made explicit during review. A task loss explicitly defined on support labels
is also evaluable, but it is a different, declared interpretation. Rank units,
task-loss units and resource units are not implicitly interchangeable.

CE04-14/16 require independent scalar rank intervals for their sharp converses.
For heterogeneous bounds, `l_x <= min_y u_y` is necessary and sufficient for
possible optimality, and setting all such candidates to the minimum upper
endpoint makes exactly that family tied in one admissible table. Correlated
weights can block this completion. Lexicographic vector uncertainty also need
not admit a simultaneous tie. If the payoff uses the uncertain rank itself,
its selection coupling must remain: intervals [0,0] and [0,10] yield selected
rank 0, not an attainable selected-rank interval [0,10].

The exact-weight kernel does not implement error-aware pruning or arbitrary
weight-space linear programming. In particular, it discards visited non-best
candidates, whereas a possible-true-minimizer service would need near-best ones.
A fixed rational rank table can be integer-scaled; continuously variable rank
differences need not have a positive gap allowing one uniform scalarization.

## 4. Term language versus source language

The bounded Boolean gate uses only known rational coefficients and min, but
needs both the interval and discrete bit domain. The term-level unbounded
obstruction follows from a finite global Lipschitz bound on each finite CPWA
expression. It is not a claim that Value Logic values must be bounded.

The source-level graph lift has two explicit affine branches and witnesses.
It handles unbounded w without putting a product into the arithmetic syntax.
A newly named g is not enough: the branch equalities and interpretation are the
essential data. Intersections with a general source can make branches empty;
native admission still requires witnessed live cases and justified removals.
Neither this construction nor the bounded gate was run through the native
proof checker. Unknown weights remain source information, not free repair
choices to optimize away.

## 5. Implementation and comparison boundaries

Current scientific use assumes trusted in-process Search objects, ordinary
library implementations and the declared immutable request. It is not an
external report authenticator. An arbitrary Python caller can replace mutable
search state; no theorem endorses that altered object. The finite paired helper
compiles a baseline into constraints only when a frame or distance term uses
it; a caller needing the original unused reference for audit must retain it in
the full base record. The signed-Horn and table-graph adapters expose their
more detailed reference/routing metadata. The generic kernel is not the whole
front-end semantic contract.

The executable grammar, finite caps, fixed rational weights and counters are
narrower than the mathematical source-level extensions. Reporting and seed
checking perform real counted work. Frontier-pop budgets are not total CPU,
memory, bit-operation or monetary budgets. Ordinary competitors may use the
same algorithms and shortcuts. The support reduction, weighted repair and
interval arithmetic have strong ordinary antecedents; the paper records them.
The candidate contribution is the particular typed integration and its boundary
results, not a new invention of those components. P3-N01 remains NOT YET SUPPORTED.

Disposition: no unresolved mathematical blocker identified for the declared
finite P3-04 scope. This self-review is fallible and does not establish a full
formalization, independently verified implementation or unrestricted logic.
