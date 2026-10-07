# P3-03 internal review — bounded reconstruction and hostile cases

Contributor: **ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction
reviewer**. October 7, 2026 UTC. Same-model, nonblind review; no additional
concurrent time credit. Status: **mathematical proposal reviewed; executable
implementation not yet reviewed**.

This report reconstructs the principal's proposed finite cube process and
tests its assumptions. It does not claim that the proposal has already been
implemented, experimentally verified, or independently replicated. No
scientific execution was performed for this review.

## 1. Reviewed scope and inherited obligations

The starting published commit is
`c573b58165826b30ccbb78107ea752169531c45a`, source tree
`a0e5782e554cac6946ef2de23106bae092e551d2`. The current P3-03 task requires a
bounded information state for deterministic unresolved claims, an increasing
computation process without a free consequence/consistency oracle, sound
evidence updates and reopening, both true and false cases, and an explicit
undecided policy. It does not require a full logical-induction result.

Read selectively: [P3-A](../../../checkpoints/A_1.md),
[P3-01 problem contract §§3, 5 and 8](../../../foundations/01_problem_contract.md),
[observation contract](../../../foundations/01_observation_contract.md),
[representation boundaries](../../../foundations/01_representation_boundaries.md),
[EX01](../../../foundations/01_separating_examples.md#ex01--unresolved-truth-failed-search-and-finite-coherence),
and [U01–U06/R01](../../../foundations/01_desiderata.md). These artifacts are
source contracts, not evidence that the future process satisfies them.

The principal subsequently specified disjoint Boolean cubes; atomic splits;
pruning only after Strong-Kleene falsity of a received constraint; interval
evaluation of known rational affine/min/max losses; immediate stale marking
and rebuilding after withdrawal; and a bounded kernel-operation account
separate from measured host time. The conclusions below address that proposal.

## 2. Precise finite construction

Fix an active finite list of distinct, versioned Boolean claims of length
$n$. Their actual interpreted answer vector, when the stated semantic bridge
applies, is $x^*\in\{0,1\}^n$. The algorithm does not receive this vector.
It receives only permitted program text, observations, computations and
version-matched checked receipts.

Let $C$ be the finite collection of accepted Boolean constraints. Define the
mathematical assessment set

$$
S(C)=\{x\in\{0,1\}^n:\ c(x)=1\text{ for every }c\in C\}.
$$

This definition does not compute its members and does not require that they
extend to complete models of arithmetic. A hard-evidence bridge states that
every accepted constraint holds of $x^*$. It is a conditional soundness
premise, not a global consistency oracle supplied to the program.

A cube is a length-$n$ word in `0`, `1`, and `*`; its concretization contains
every Boolean vector agreeing with its specified positions. A finite frontier
$P$ denotes the union of its cube concretizations, written $G(P)$. Initially
$P$ contains the all-star cube. The essential invariant is

$$
S(C)\subseteq G(P).
$$

The frontier can be a disjoint partition of the retained region, though
disjointness is needed for efficient accounting rather than sound interval
bounds alone. The following transitions preserve the invariant.

1. **Split:** replace a cube with its two children fixing one star to zero
   and one. Their union is exactly the original cube.
2. **Prune:** delete a cube only when a sound partial evaluator proves that
   every completion violates an accepted constraint. Strong-Kleene value
   false is a sufficient condition for ordinary Boolean syntax.
3. **Add evidence:** add an accepted constraint to $C$. Its compatible set
   becomes a subset of the old one. Leaving the frontier temporarily unchanged
   is a sound outer approximation, although it does not yet enforce every
   accepted constraint on every covered assignment.
4. **Add a fresh query:** extend every old cube by a star. This projects back
   exactly to the old frontier, and covers both possible answers to the newly
   represented claim.

For Strong-Kleene evaluation, the needed claim follows by structural induction:
when a partial evaluation returns a Boolean constant, every Boolean completion
has that value. An unknown result is permission to retain the cube, not an
instruction to assign the claim either truth value or a particular probability.

### Soundness theorem

Assume the initial cover, transition checks, and hard-evidence bridge above.
Then after every committed transition, $x^*\in S(C)\subseteq G(P)$. If a
computed interval encloses the loss at every point of $G(P)$, it therefore
encloses the actual loss at $x^*$. The proof is induction over committed
transitions followed by one application of set containment.

The theorem needs no complete arithmetic models, no full-theory entailment
test, and no arbitrary probability weights. Its content is a restricted
information/update construction with conditional warrants.

## 3. Interruptions are part of the proof

The invariant must hold at every point from which a report or saved state can
be recovered, not only after a successful unlimited run. A split implemented
as “remove parent; compute left; compute right” is unsafe if the process stops
after the first operation or before saving the right branch. The same applies
to sequential output-file replacement or replay of a partially saved mutation.

A valid implementation can prepare both children before committing the
replacement, retain the parent as a pending obligation until the split is
committed, or roll back incomplete changes. Its declared resource model must
cover the chosen mechanism. Budget failure returns the prior sound state or an
explicit pending state whose residual work remains covered.

**Interruption witness.** For one unknown bit $x$ and loss $x$, suppose an
enumerator has visited only assignment zero. Returning the visited minimum and
maximum gives `[0,0]`, which fails if the actual answer is one. Keeping the
unvisited branch, or retaining the parent cube, gives the warranted interval
`[0,1]`. A sample of visited assignments is an inner set; it is not an outer
uncertainty bound.

The same witness applies to memory pressure: silently dropping a queued cube
to meet a capacity limit can delete the actual answer. Refusing a split,
returning an unfinished status, or widening to a sound ancestor is permitted;
deleting unexplored alternatives is not.

## 4. Loss bounds, monotonicity and exact endpoints

Map a cube to coordinate intervals: zero becomes `[0,0]`, one becomes `[1,1]`,
and a star becomes `[0,1]`. For a known rational affine term

$$
f(x)=a_0+\sum_{i=1}^{n}a_i x_i,
$$

the lower endpoint selects the lower coordinate endpoint for $a_i\geq0$ and
the upper endpoint for $a_i<0$; the upper endpoint makes the opposite choices.
These are exact extrema over the Boolean cube and over its real box.

Interval extensions for addition, known rational scaling, minimum and maximum
are sound and inclusion-isotone. For example, the interval for the minimum of
two terms is the minimum of their lower endpoints through the minimum of
their upper endpoints. The actual pair of term values need not vary
independently, so this extension can be loose. Soundness does not require
independence.

For a nonempty finite frontier, take the minimum of the per-cube lower bounds
and the maximum of the per-cube upper bounds. Splitting or pruning only
restricts the represented set. Inclusion isotonicity therefore makes the
computed global lower bound nondecreasing and upper bound nonincreasing,
provided the loss, units, evidence dependencies and scope stay fixed.

**The missing assumption in a broader claim.** An arbitrary sound enclosure
routine need not be inclusion-isotone: a routine may return `[0,1]` on a large
source and `[-100,100]` on a smaller one while remaining sound. Thus source
narrowing alone does not establish monotonicity of arbitrary reported
intervals. The proposed compositional kernel supplies the missing property.
Alternatively, separately warranted bounds may be intersected under unchanged
dependencies; this requires recording the justification for the intersection.

On a singleton cube, every coordinate interval is exact. Induction over the
term syntax then shows that affine/min/max evaluation returns the exact
rational loss. Consequently, if a fixed finite frontier is eventually split
into singletons and every singleton is checked against every accepted
constraint, the retained source is exactly $S(C)$ and the loss extrema are
exact on that assessment set. There are at most $2^n-1$ binary splits in a full
tree, but checking constraints and evaluating terms have their own nonzero
costs. This is a finite termination bound, not a claim of efficiency.

### Native source bridge

Replacing Boolean stars by real intervals embeds the frontier in a finite
union of rational boxes, inside the inherited native source language. Its
relationship to the Boolean source is containment. For a general admitted
piecewise-affine loss it is not exact equivalence of extrema. The term
$\min(x,1-x)$ equals zero at both Boolean assignments but reaches $1/2$ on
the real interval `[0,1]`. A native certificate over the real boxes can still
transfer to the actual Boolean answer through containment. A relaxation-only
counterexample need not refute the Boolean target.

The interval `[0,1]` in this bridge is an enclosure of an unresolved Boolean
coordinate. It does not assert that the coordinate is itself a probability.

## 5. Nonemptiness and coherence require distinct evidence

A nonempty frontier need not certify $S(C)$ nonempty. It can retain cubes
whose incompatibility has not yet been discovered. For example, constraints
`x` and `not x` make $S(C)$ empty, but the initial all-star cube can remain
while processing is incomplete. The proper status is an outer cover with
pending constraint processing, not “a consistent logical model found.”

Conversely, an empty frontier obtained from a complete initial cover by valid
splits and justified prunes proves $S(C)$ empty. The transition record, or a
separate checked finite unsatisfiability certificate, supplies the proof.
An empty frontier supplied without this history is not by itself a conflict
certificate. Under the stated bridge to a single actual vector, a certified
conflict means that at least one of the bridge or admission premises cannot
hold jointly; it must not be converted into a favorable vacuous loss warrant.

There is also a coherence distinction. An arbitrary normalized distribution
on an incompletely pruned frontier can put mass on assignments violating an
accepted constraint. Conditional containment bounds are therefore available
earlier than a claim that arbitrary frontier weights satisfy every accepted
Boolean relation. To assert the latter, finish filtering the represented set
or retain the accepted constraints explicitly in the admissible probability
source. Do not report unrestricted U03 coherence from an outer cover alone.

Neither an unverified candidate assignment nor a partial solver's failure to
find one proves nonemptiness or emptiness of the accepted finite source.
These are positive witness and exhaustive exclusion services, respectively.

## 6. Hard evidence and dependent current reports

U04 requires accepted, version-matched Boolean resolution at the next eligible
update. Merely putting the receipt at the back of a pruning queue is
insufficient if the system continues to advertise a contradictory current
estimate. A direct literal overlay can resolve the query while other
dependent intervals are recomputed, or affected reports can become explicitly
stale/pending. Old reports remain immutable historical observations.

In particular, receipt discovery, syntactic checking, semantic applicability,
acceptance, and incorporation are separate events. The cost and timing of the
accepted result must not be moved backward to the start of an unfinished proof
or simulation. If the checker fails or runs out of budget, the candidate
receipt does not become a hard constraint merely because its producer expects
it to be valid.

An unconditional semantic statement is stronger than a proof in a tagged
alternative theory. The bridge from the latter must remain explicit. A proof
of `Gamma_A implies x` and a proof of `Gamma_B implies not x` can be stored
together without asserting that both antecedents hold in the current source.

## 7. Source revision forces either repair or widening

Take one unknown Boolean coordinate and loss equal to that coordinate. With
accepted hard premise `x=1`, pruning can leave only the singleton one and a
loss interval `[1,1]`. Withdraw that premise. The new compatible source is
`{0,1}`. Keeping the old frontier is an inner restriction and no longer covers
the newly admitted zero case. The current warrant must be reopened to `[0,1]`
unless some retained independent support still excludes zero.

A full rebuild from the top cube is a sound constructive policy. More efficient
repair may retain valid exclusions and reactivate those depending on withdrawn
premises. That optimization must also retain or reconstruct excluded branches;
a list of final survivors alone cannot recover the lost alternatives.
Dependency references without accessible exclusion data do not supply this
repair for free.

A version change can invalidate the query coordinate itself, even when its
displayed sentence is unchanged. A program that returns zero in one version
and one in the next provides the smallest example. New objective units can
instead preserve the answer vector while invalidating loss bounds and action
ordering. These require different dependency edges, not an indiscriminate
truth-value reset.

### Memory tradeoff

A fixed frontier cap can preserve soundness by refusing further splits or by
joining cells into a coarser covering cube. It cannot guarantee all finite
fragments will reach exact assessment extrema under that policy. For example,
a cap of one cube cannot represent the exact XOR set `{01,10}` as a single
ordinary cube. Its smallest enclosing cube also contains `00` and `11`.
Keeping the XOR constraint intensionally is an alternative representation,
but its solver and evaluation costs must be declared.

Previously proved actual-loss bounds can sometimes be retained even after
representation widening if their semantic dependencies remain valid. Such a
bound is then supported by the retained proof, not by the claim that it holds
over every point of the widened frontier. A report must identify which source
and certificate it is using. Forgetting the proof as well as the detailed
frontier removes that particular cheap reuse route.

## 8. A scoped eventual-resolution theorem

For a fixed versioned query, suppose a correct answer or refutation has a
finite admissible computation/receipt; its checker completes after finite
work; the scheduler eventually supplies every required finite prefix of that
work; the accepted result is retained or otherwise remains available for every
later report; and the query's semantic scope eventually stays fixed. Then
there is a finite report event after which every eligible report resolves that
query correctly. This follows by completion of the finite receipt and checker
work, hard-evidence incorporation, and retention. Both Boolean answers are
covered by the same argument.

For the explicit bounded-execution family in P3-01, the bound *inside the
proposition* is part of its meaning. Fully simulating that horizon can establish
the requested output or its absence. A reasoner stopped before that horizon
has not refuted the bounded claim. For an unbounded halting claim, failure to
halt during a finite simulation is not a general refutation rule.

For a general arithmetic theory, proof enumeration can eventually resolve a
fixed sentence only when an appropriate proof or refutation exists and its
checking prerequisites are effectively available. Semantic decidability of a
selected external query family should instead be connected to a supplied
total decision procedure. “The statement has a truth value” alone supplies
neither form of effective resolution.

### Fairness must be stated in work, not just in round names

Unbounded cumulative budget is insufficient if every fixed query receives
only a bounded share, or if the verifier restarts each time. A job requiring
two indivisible units never completes when every visit gives one unit and
discards progress, even though its lifetime assigned budget diverges. Either
the required operation eventually receives enough budget at once or its
computation must be resumable with retained progress. Heterogeneous verification,
arithmetic and receipt costs belong to this condition.

Similarly, repeatedly evicting accepted receipts can make a fixed query
alternate between resolved and unknown. Fair discovery alone proves repeated
resolution, not eventual correctness of every later report. Persistent relevant
information, or an explicit service guaranteeing its timely reacquisition, is
an additional assumption.

## 9. Enumeration and defaults do not establish anticipation

An effective sentence enumerator and an unresolved default such as `[0,1]`
make a finite interface extendible to arbitrary requested syntax. A midpoint
`1/2`, if separately offered, is merely a point-forecast policy. Neither
operation proves useful refinement on a growing cohort.

Consider a fair search process where each fixed query will eventually receive
its checked answer, but the requested query at round $t$ is a newly introduced
one beyond the completed search frontier. Every initial report can remain
unresolved. If a point-default policy returns `1/2` and all these selected
queries happen to be true, its squared loss is $1/4$ on every initial report.
Pointwise eventual resolution of old queries remains possible. The two
statements have different quantifiers.

This is a construction about the stipulated process and feedback schedule,
not a computational lower bound against every ordinary method. A competitor
with a valid cheap shortcut may do better, and the comparison contract gives
both methods access to that shortcut. Claims of anticipation, calibration or
efficient pattern learning require their own update and feedback argument.

## 10. Exact ordinary reconstruction

The same state is an ordinary partial-assignment frontier with checked
constraints, sound interval evaluation, receipt scheduling, and dependency
tracking. Define the translation as identity on query keys, evidence bytes,
cube cells, loss terms, resource prices and pending work. Map a candidate
split, prune, receipt check or report to the identical operation in O-COMB.
By induction over the common event transcript, both executions have the same
frontier, statuses, interval endpoints, actions under the same tie rule, and
declared resource charges. If the implementations are literally shared, no
extra decoder cost is hidden by the translation.

An optional probability reconstruction, after fixing a nonempty assessment
source, admits all normalized distributions supported on it. For any supplied
finite loss table, the minimum and maximum expected losses over this credal
set equal the minimum and maximum table entries. The inequality follows
because an expectation is a convex combination; equality follows by assigning
all mass to an attaining state. This is an ordinary mathematical adapter,
not a justification for any particular subjective weighting. Its explicit
enumeration or compact inference implementation still has costs.

The bounded construction therefore does not establish an advantage over the
strong ordinary comparator. Its possible contribution is a precise, verified
application to the project's value/query and revision interfaces, with a
clearly named scope. P3-N01 cannot be upgraded from the construction's notation
or from this review alone.

## 11. Implementation questions to check when code exists

| Obligation | Concrete failure to look for |
|---|---|
| Budget-safe cover | A split removes a parent before preserving both children; a rejected operation mutates state. |
| Closed resource claim | Large input parsing, integer arithmetic, receipt copying, or report production falls outside a claimed hard budget without disclosure. |
| Arithmetic limits | Oversize rationals yield truncated bounds or partial commits rather than a typed limit/pending status. |
| Nonemptiness evidence | Nonempty frontier is advertised as satisfiable, or empty work queue is advertised as a certified contradiction. |
| Complete filtering | A probability/Boolean-coherence claim uses still-unchecked outer-cover assignments. |
| Literal uptake | An accepted resolution leaves contradictory dependent current bounds without stale marking. |
| Semantic scope | Correct bytes for the wrong program, horizon, input, checker or theory are accepted for a different query. |
| Receipt binding | A self-consistent supplied receipt is checked without matching the actual original request and active source. |
| Revision | Withdrawing a premise leaves its exclusions active; changing a loss keeps an old-unit bound current. |
| Retention | The theorem promises permanent resolution while the implemented cap may discard the only supporting evidence. |
| Finite coverage | A small instruction language is described as deciding arbitrary PA or unbounded halting. |
| Historical reports | Later evidence edits the originally issued forecast, or unreceived labels enter current features. |

The principal's bounded kernel-operation account should be labeled as that
account. Input-size and bit-length limits can make its operations finite and
auditable; they do not make one rational operation equal to one physical CPU
step. Host wall/CPU observations and modeled task-loss prices answer different
questions. A hard memory claim additionally needs checks before unsafe large
allocations; recording size failure only afterward is a different guarantee.

## 12. Present assessment

The proposed construction has a sound restricted mathematical route to U01,
U02, hard-evidence uptake under U04, conditional fixed-query resolution under
U05, and a concrete rebuilding policy for R01. U03 is exact only for the
fully represented/filtered finite constraint service; intermediate covers
supply containment rather than arbitrary-weight coherence. U06 anticipation
is not established. The singletons, interruption, source revision, memory,
and fairness examples identify useful acceptance checks without turning the
ordinary reconstruction into a weaker comparator.

No conceptual blocker remains **provided the implementation and principal
theorems include these hypotheses and typed failure modes**. This report
does not award executable correctness before inspecting the actual code and
its specifically authorized development evidence.
