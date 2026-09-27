# F05 S2 — observation, relative loss, and revision reconstruction

Status: **completed F05 reconstruction; the semantic core remains provisional**.
Date: September 27, 2026 UTC (September 26 in America/Los_Angeles).
Base: `f96be7af8a6fcb766ec90aae24202c2884129a53`.
This note reconstructs the S1 definitions from ordinary finite real/rational
arithmetic and set semantics. It is same-assistant self-review, not independent
verification, a new priority claim, or the deductive rule system assigned to F06.

## Reading guide and result boundary

Sections 1–5 and 8–17 reconstruct the source/observation interface and what a
relative-cost summary preserves. Sections 18–23 and 33 give complete component-level
interpretations with feasibility witnesses and explicit updates. Sections 6,
24–25 and 31 distinguish report-dependent behavior, loss optimization and
conditional self-assessment. Sections 26 and 30 contrast an update counterexample
with a restricted exact fibre summary. Section 27 connects the native margin
loss to log loss through an analytic enclosure, not a new logarithm connective.

These are semantics, scoped proofs and hostile examples supporting F05. They are
not the F06 deduction rules, a claim of new classical convex-analysis results,
or evidence that a trained neural network has acquired the proposed interpretation.
[The S2 tests](../checks/f05_observation_revision.py) exercise 42 finite cases/test
families; their analytic extent is the written argument, not extrapolation from
sampled values. [The source note](F05_S2_sources.md) records the limited fresh
literature check. The [work log](../work_logs/F05_2026-09-27_S2.md) closes the task.

## 1. A lean reading of the existing semantics

There are three interfaces, not three mandatory new kinds of semantic carrier:

1. A **numerical presentation**: typed source coordinates, a finite union of
   nonempty rational polyhedra, and finite cost terms.
2. A **use interface**: visible observations, available versioned programs, and
   the cost interpretation of the *same* program in each retained case.
3. A **warrant record**: which source assumptions, interpretation versions and
   evidence modes justify applying the conditional numerical conclusion.

For a fixed expression comparison only the first interface and the interpreted
expressions determine mathematical validity. Different provenance records with
identical numerical interpretations give the same conditional inequality. They
need not give equally justified empirical reliance, or support identical later
updates. Conversely a signature/revision fingerprint is a conservative cache
key, not a mathematical claim that equivalent presentations have different values.
No all-purpose scalar replaces these distinctions.

Let a modeled situation be `omega=(o,h,x)`, with finite visible observation `o`,
hidden case `h`, and a feasible source assignment `x`. The observation map returns
`o`, not `h` or `x`. Repeated coordinates denote shared quantities before a cost
is evaluated. An expression interpreter may inspect x in a supplied hypothetical
model; the deployed program cannot inspect x unless its observation interface
provides that information. This distinguishes a semantics from an omniscient
implementation.

For every live observation/case, give a complete cost table `J_(o,h,a)(x)` for the
available program versions a. A rational lottery `p_o` is chosen from the visible
observation only, and its modeled expected cost is

    J_p(o,h,x) = sum_a p_o(a) J_(o,h,a)(x).

The weights are fixed rational numbers within each visible cell. This makes the
cost a native CPWA term. A model-dependent weight would generally be nonlinear
and, when hidden, an illegal decision. A cost table is a declared component-use
model, not evidence of its empirical accuracy or an oracle supplying the final
comparison. Every candidate example retains the component computations.

Pointwise evaluation is total after typing. Universal comparison is a quantified
property of these evaluations. Admissibility of a policy is a property of its
visible table and registry, not inferred from a numerical minimum of costs.

## 2. Relative-cost images: an exact numerical simplification

Fix one visible observation and a finite set A of available programs. Choose a
reference program `a0`. All programs in this comparison have costs in one unit.
At each possible situation define

    d_a(omega) = J_a(omega) - J_a0(omega),   d_a0=0,
    R_o = { (d_a(omega))_(a != a0) : omega compatible with o }.

### Proposition 1 — exact relative evaluation

For any two fixed lotteries p,q over A,

    J_p(omega)-J_q(omega) = sum_a (p(a)-q(a)) d_a(omega).

Consequently R_o preserves every universal bound on this difference, and every
native CPWA expression formed from the retained relative coordinates. A common,
possibly unbounded baseline can be omitted. It does not preserve absolute
adequacy unless an anchor for that baseline is retained.

**Proof.** Substitute `J_a=J_a0+d_a`; the coefficient of J_a0 is
`sum_a p(a)-sum_a q(a)=0`. Evaluation of any expression of d factors through the
image by structural induction. Each image point has a preimage, so the two
universal quantifiers have exactly the same values, not merely an inclusion.
The assignments `J=(z,z+1)` for arbitrary real z have one fixed relative image
but different absolute adequacy. This is the promised counterexample. QED.

Changing the reference from a0 to aj applies the invertible transformation
`d'_a=d_a-d_aj` on the corresponding relative-coordinate spaces. Independently
recentering each action is not that transformation and destroys the comparisons.

### Proposition 2 — native representability of the image

For the selected rational CPWA / finite rational-polyhedral fragment, R_o is a
finite union of rational polyhedra. Each nonempty component has a rational
witness. Thus the simplification has a representation within the source format,
although explicitly computing it can increase size substantially.

**Proof.** Refine source cases by a joint finite partition on which every cost
term is affine. Use closed activation regions; overlaps on equality boundaries
have agreeing values. On one such rational polyhedron P, relative evaluation is
an affine rational map T. Its image is the projection of the rational polyhedron
`{(x,d): x in P, d=T(x)}`. Eliminating coordinates yields a rational polyhedron.
Take the finite union over the nonempty regions. Rational feasibility follows
from the usual rational affine-face construction already reconstructed in S1.
This is a semantic construction, not an implemented projection algorithm. QED.

### Corollary 3 — finite sharp bounds are attained in the selected fragment

For a fixed native term comparison on a nonempty source, a finite supremum is
an attained rational value. If a proposed rational upper bound fails, a rational
countermodel exists. This is stronger than finite testing and weaker than an
implemented validity decider.

**Proof.** On each joint affine region, the set of attained differences is a
nonempty rational polyhedron in the real line, hence a point, closed interval,
closed ray or the whole line. A finite upper endpoint belongs to it and is
rational. Take the maximum of the finitely many finite endpoints; any unbounded
component instead makes the overall supremum infinite. Lift an endpoint through
the rational affine system to obtain a rational source witness. QED.

The argument uses *polyhedral* projection, not the false assertion that every
linear image of every closed set is closed. For example
`{(x,y): x>0, y=1/x}` is closed in R^2 but its x-projection is `(0,infinity)`.
Nonlinear equality sources are not covered by the selected fragment.

## 3. Convex compression is query-relative

Let K_o be the closed convex hull of R_o. Every fixed-lottery comparison is
linear in d, so

    sup_(d in R_o) v.d = sup_(d in K_o) v.d

for its corresponding direction v, including unbounded suprema. Convexification
is exact for these numerical bounds and optimization over a fixed family of
visible lotteries. It does not authorize mixing hidden-world interpretations or
choosing an action after observing a hidden mode.

It is not exact for every native CPWA query. For

    R={(0,2),(2,0)},

`sup_R min(d1,d2)=0`, but `sup_conv(R) min(d1,d2)=1`. Both relative coordinates
can be expressed as costs relative to a zero-cost reference. The nonlinear
expression is a diagnostic quantity, not automatically an executable best-action
selector. Convexification changes its admissible joint interpretations.

This is why the principal core retains finite source cases. The convex hull is
an optional abstraction with a declared query family, not a universal redesign.

## 4. Observations cannot be erased merely because the cost image is retained

For one blind observation, two hidden situations with action costs `(0,2)` and
`(2,0)` give a lottery `(q,1-q)` worst cost `max(2q,2(1-q))`. Its minimum is 1,
attained at q=1/2. When the situation is revealed, choose the cheaper action in
each visible cell and attain 0. The pooled cost image is identical. Only the
permitted policy interface changed.

More generally, suppose several fine visible cells i are merged into one coarse
cell. For a target bound b and a fixed, correctly lifted old policy, put

    K_i(b) = {p in Delta(A): for every omega in cell i,
              J_p(omega)-J_old(omega) <= b}.

Fine-information feasibility means every K_i(b) is nonempty. Coarse-information
feasibility means their intersection is nonempty. This is an exact criterion:
coarse choice is one common p, while fine choice can be p_i. It is neither an
independence assumption nor an expectation over an unspecified prior.

For finite rational cost tables these are rational polytopes inside the compact
simplex. Finite optimum bounds are attained and a rational optimum exists. A
finer observation cannot worsen the *optimal robust value* when the old policy
can ignore it and the source/cost model is unchanged. It does not imply that a
newly optimized policy is no worse at each individual possible situation. That
requires its own paired comparison to the lifted old policy.

The choice sets A must either be common across the merged cells or replaced by
the common available intersection. An apparently beneficial action unavailable
in one retained case cannot be used to certify a coarse policy.

## 5. Precisely when a projected source can absorb an update

Let T:X->Z retain a numerical observation such as the relative-cost vector.
For a source S subset X, its summary is T(S). An evidence update retains E subset X.
Ask whether an updater F_E on summaries alone can satisfy

    F_E(T(S)) = T(S intersection E)

for **every** admissible source subset S, without revisiting its hidden fibers.

### Proposition 4 — exact update criterion

For arbitrary source subsets, such an updater exists iff E is a union of T-fibers:

    T(x)=T(y) implies [x in E iff y in E].

In that case E=T^{-1}(G) for some G subset im(T), and the updater is intersection
with G on the image. This is a statement about a specified update, not a claim
that all future evidence can be accommodated by a fixed small summary.

**Proof.** If E is saturated, `T(S intersection E)=T(S) intersection G` directly.
Conversely take x,y with the same image. Their singleton source sets have identical
summaries. If E retains x but not y, their updated images are respectively a
singleton and empty, contradicting a deterministic updater on summaries alone.
In the finite rational witnesses below all these sources are expressible by the
native closed-polyhedral presentation. QED.

A retained-coordinate inequality is saturated, but a new observation about an
omitted quantity need not be. This identifies which variables may safely be
removed for a *declared update family*. Adding the update's sufficient coordinate
can repair the interface; the entire original object need not always be retained.

Convexification is a separate obstruction, even when the update mentions only
retained coordinates. Let R={0,2}, R'=[0,2], and retain the new evidence d=1.
Both initial convex summaries are [0,2], but the exact updated images are empty
and {1}. Updating the convex summary alone can invent a live case. To avoid an
example depending on empty contexts, take R={0,2}, R'=[0,2], and update d<=1.
Both updated sources are nonempty; their exact attainable ranges are {0} and
[0,1], and their sharp upper bounds differ. The transformation therefore is not
an exact dynamic abstraction merely because it preserved every initial linear
bound. It remains a sound *outer* abstraction if that is the declared contract.

### Example with an omitted coordinate and no empty updated source

C1 contains (d,y)=(0,0),(2,1); C2 contains (0,1),(2,0). The two relative-cost
images are the same {0,2}. Evidence y=0 leaves d=0 in C1 and d=2 in C2.
Both updated contexts have witnesses. Neither the range nor even the complete
initial relative image reveals which result follows. Retaining y jointly with d
is sufficient for this update. Recording only their separate ranges is not.

## 6. Randomizing reports: expected loss is not conditional self-assessment

The S1 self-controller is a versioned program SELF-MIX(r), with

    H_r=(1-r)p+rs,

the modeled failure rate conditional on its emitted report r. At fixed p,s this
is an expectation over its specified fresh execution randomness, not uncertainty
about the mathematical truth of an assertion.

Now let a wrapper draw I with fixed positive weights q_i, emit r_I, and run the
corresponding SELF-MIX(r_I). Two distinct questions are possible:

    mean-report calibration:  sum_i q_i H_i <= sum_i q_i r_i;
    emitted-report validity:  H_i <= r_i for every i with q_i>0.

They are not equivalent. With p=1/2,s=0 and an equal mixture of r=0 and r=1,
mean failure is 1/4 and mean report is 1/2, so the first inequality holds. But
the emitted zero report has failure rate 1/2 and is invalid.

### Proposition 5 — a native expression for conditional report shortfall

Define the nonnegative modeled shortfall

    Q = sum_i q_i res(r_i,H_i),   res(a,b)=max(b-a,0).

For fixed rational reports and weights Q is a native CPWA term. `Q<=0` is
pointwise equivalent to emitted-report validity on the positive support.
The equivalence remains true under universal source quantification.

**Proof.** Every summand is nonnegative, and its positive coefficient can only
contribute zero when its residual is zero. At a zero weight the report is never
emitted by this wrapper, so no conditional obligation follows. Apply the pointwise
argument at every retained model. QED.

In contrast `res(sum q_i r_i, sum q_i H_i)` clips *after* cancellation. It is at
most Q and can be zero when Q is positive. In the example Q=1/4 while this
clipped mean is zero. The order of expectation and residual is operationally
meaningful; it is not a choice of notation for the same truth degree.

A different wrapper that always emits the constant mean report but uses the
same mixture of inner behaviors can have a valid report. That is a different
observable/program version. Expected loss alone does not identify which report
protocol was executed.

### Allowing uncertainty rather than enforcing perfection

A budget `Q<=epsilon` bounds average magnitude of report shortfall. For any
positive threshold tau,

    sum_{i: H_i-r_i>tau} q_i <= epsilon/tau.

This follows because Q dominates tau times the weight of those indices. It is
about selection of a report *at a fixed retained model*, not the frequency of
random binary failures, and remains uniformly valid when its premise holds for
all source models. No informative probability of *any* positive shortfall follows
without a threshold or other margin assumption: every report can miss by an
arbitrarily small positive amount. When all positive weights are at least qmin,
individual shortfalls are bounded by epsilon/qmin.

This is a scoped semantic target for later rules. It does not assert that the
F05 fixture supplies a new statistical calibration method or unrestricted proof
reflection.

## 7. Signed comparisons, scopes, and consistent cycles

For fixed terms over one nonempty source let B(t,s)=sup(t-s). These values are
finite reals or +infinity; no -infinity occurs. For finite budgets, a cycle of
valid comparisons satisfies

    t1-t0<=b1, ..., t0-t_(n-1)<=bn  =>  0<=sum_i bi.

**Proof.** Evaluate all terms at one feasible point of the *same* source. The
left sides telescope exactly to zero; sum the inequalities. QED.

Thus negative budgets cannot certify a negative cycle inside one consistent
interpretation. Mixing source scopes can manufacture one: in x=0, costs A=x
and B=1-x satisfy A-B=-1; in x=1 they satisfy B-A=-1. The two statements cannot
be chained over a common feasible source. Their conjunction has an empty join,
not a two-unit improvement returning to the starting policy.

An open-ended sequence of better models is not a negative cycle. For costs
J_n=z+1/n, consecutive improvements persist for every n although they have a
finite cumulative limit. With no lower bound on allowed signed costs, J_n=z-n
instead has unbounded cumulative improvement. Neither construction certifies
metaphysical finality, or requires a finite current registry to contain its
unrepresented future members.

## 8. What is safe to erase from the numerical evaluator

The numerical evaluator does not read dates, certificate authors, proof histories
or confidence labels. Equality of the typed source relation and the interpreted
query gives equality of its conditional bound regardless of those records.
They can be left outside the arithmetic kernel. They cannot be discarded from a
claim that a particular empirical source is presently warranted or transferable.

A coherent bijective renaming of source keys, local binders, cases and registered
program versions (with their interpretation table transported) changes neither
point evaluations nor quantified bounds. Renaming a source in only one occurrence,
or transporting the record label but not the source relation, is not such an
isomorphism. The earlier dependence and version counterexamples apply.

Named positive linear maps in the conversion table include *valuation bridges*
such as expected failure probability -> expected cost at one unit per failure.
They are not all pure unit-coordinate changes. A pure re-expression in different
units must transport all terms, source rows and budgets coherently; a semantic
change of per-failure cost changes the criterion. If a pair of maps is claimed
as inverse coordinate conversions, its composed scale must be one. The grammar
itself does not supply that identity merely because the unit names match.

A source-domain witness establishes nonemptiness, not observation of the hidden
assignment or empirical validity of the rows. A registry check establishes that
a named program is available, not that its proposed loss model is correct.
These boundaries prevent a minimal arithmetic kernel from silently inheriting
unlicensed authority while avoiding unnecessary metadata inside every number.

## 9. Which future compositions still permit baseline erasure?

Proposition 1 is about the declared programs and query family. It must not be
misread as saying that their relative-cost image supports arbitrary later plan
composition. Consider `J_A=z, J_B=z+1`. The relative image is the singleton {1}
for every z. A newly constructed twice-A plan compared with B costs

    2 J_A - J_B = z-1.

Its sign cannot be recovered from {1}. Even z>=0 leaves both improvement and
worsening possible. The new use has changed the coefficient of the unknown
common cost. This is not a failure of the original fixed-lottery theorem.

### Proposition 6 — a sufficient common-baseline composition discipline

Call an expression t *translation-covariant of weight k* when

    t(J+c*1)=t(J)+k*c

for all finite J and c in one common unit. Constants have weight 0 and cost
coordinates weight 1. Addition adds weights; rational scaling scales them;
minimum/maximum of equally weighted terms retains that weight; and the residual
of equally weighted terms has weight 0. Nonrecursive substitution preserves
these pointwise identities. These are semantic calculations, not an F06 proof
system being installed early.

If t_new and t_old have the same weight, their difference is a function of the
relative-cost coordinates alone. If the allowed grammar does not establish an
equal weight, retain an absolute anchor or check a stronger semantic invariant.

**Proof.** The constructor calculations follow by inserting the common shift.
For equal weights, substitute `J=J_a0*1+(0,d)` and cancel the two k*J_a0 terms.
For a linear expression c.J, invariance is possible iff sum(c)=0, because its
increment under a shift is `shift*sum(c)`. QED.

The syntactic test is sufficient rather than complete: algebraic cancellations
can establish covariance even where two unreduced intermediate subterms have
different provisional weights. It must not reject a proved equality as false.

### A complete functional test for the finite CPWA case

For a continuous finite piecewise-affine t on R^m, t has global translation
weight k iff the gradient on every full-dimensional affine region has coordinate
sum k. The gradient here means the actual affine coefficient, not an arbitrary
subgradient selected separately at each zero ReLU.

**Proof.** Covariance implies the gradient identity in the interior of every
region by differentiating its affine formula along the all-ones direction.
Conversely on a generic line parallel to that direction, the finitely many
successive affine segments all have slope k. Continuity makes their affine
constants agree at their interfaces. For a line lying on region boundaries,
approximate it by generic parallel lines and use continuity at its endpoints.
The shift identity follows. QED.

This provides a mathematical baseline-invariance control for an already-grounded
neural cost interpretation. It does not identify which internal coordinates of a
trained network are costs, and one sampled activation region does not establish
the global hypothesis.

## 10. All relative CPWA queries distinguish more than linear comparisons

Two different closed finite unions of rational polyhedra can have the same convex
hull, and therefore the same fixed-lottery bounds, yet differ for native nonlinear
relative expressions. This is not merely a chosen example.

### Proposition 7 — constructive separation of relative source images

For nonempty closed finite unions R,S of rational polyhedra, the following are
equivalent:

* R=S;
* every native rational CPWA relative expression has the same valid rational
  upper bounds on R and S.

**Proof.** Equality clearly suffices. If x lies in R but not S, closedness of S
provides a positive-radius open neighborhood disjoint from S. Rational points
are dense in the rational polyhedral piece of R containing x, by the active-face
argument of S1. Choose a rational x' in that piece still inside the neighborhood,
and a rational radius r>0 whose closed sup-norm ball misses S. The native term

    f(d)=max(0, r-max_j |d_j-x'_j|)

vanishes on S and equals r at x'. Thus `f<=0` holds on S and fails on R.
Interchange R and S for the other direction. QED.

This is a concrete distinguishing expression, not an assertion that an arbitrary
future consumer is covered by an undefined observational quotient. It makes the
scope of exact simplification precise. Computing a complete relative image may
still cost more than retaining the original source presentation.

For **linear** relative queries, closed convex hull is enough. In the selected
rational-polyhedral family it is also characterized by their valid bounds: if
two rational polyhedral convex hulls differ, a rational supporting/separating
inequality witnesses the difference. Any rational direction v in relative
coordinates can be rewritten as a positive rational multiple of a difference
of two rational lotteries: extend v with coordinate `-sum(v)`, separate positive
and negative parts, and normalize their equal total mass. The zero direction is
trivial. Thus this is an operational comparison family, not an arbitrary test
added solely for a mathematical characterization.

The rational-polyhedral hypothesis matters when tests are restricted to rational
directions. Do not generalize that characterization to every closed convex set
without further argument. These are standard separation constructions applied to
the chosen semantics, not the later F08 contribution claim.

## 11. Conditional loss models and observational averages

A registry interpretation J_a(omega) refers to *executing a under the declared
source model*. Historical conditional averages `E[loss | selected action=a]` do
not automatically supply that function. They can condition on different hidden
subpopulations.

For example take equally likely hidden situations with costs `(0,2)` and `(2,0)`.
A historical selector that observes the situation always chooses the cheap
program. Both observed action-conditioned mean losses are zero. A blind equal
lottery has expected loss one in each situation, not zero. Treating the two
historical zero means as costs for blind use silently changes the source model.
The arithmetic evaluator cannot discover the missing counterfactual assumption.

The reflective examples explicitly specify their fresh random draws and branch
failure probabilities conditional on the source. More general report-induced
changes of the population require report-indexed costs or a declared response
model. They are not licensed by the word 'self' or by a policy-table type check.

## 12. Finite witnesses and open numerical questions

Native comparisons over nonempty rational-polyhedral sources have four distinct
semantic/operational situations that should not be compressed prematurely:

* a universal upper bound holds;
* a supplied feasible point disproves that universal bound;
* all feasible points violate the bound;
* a current proof/countermodel search has not decided the question.

The second need not imply the third, and the fourth is a statement about a
procedure rather than a new mathematical valuation. In the S1 report r=2/5,
`H_r-r=s-1/10` has attainable interval [-1/10,3/20]. There are both satisfying
and violating source points.

In this exact native fragment a finite infimum is attained as well as a finite
supremum (apply Corollary 3 to the negative term). Therefore a universally strict
violation has a positive uniform margin. This is a restriction of the chosen
finite CPWA/closed-polyhedral model. General nonlinear models can be strictly
positive everywhere with infimum zero, such as 1/(1+x) on x>=0. Such distinctions
must remain visible when importing a richer continuation or nonlinear adapter.

No declaration of numerical consistency certifies that the actual environment
belongs to the source. Evidence modes and their joint-coverage conditions remain
explicit premises outside this deterministic interpretation.

## 13. A query-relevant error measure that ignores common cost offsets

For a finite vector e of per-program cost errors, define

    span(e) = max_a e_a - min_a e_a.

This is a seminorm on the full cost space and a norm modulo common additive
offsets. It is invariant under adding c*1, and vanishes exactly on constant
vectors. It is not a probability or a degree of truth.

### Proposition 8 — exact all-lottery contrast error

For two cost vectors J and Jhat at one modeled situation,

    sup_(p,q in Delta(A)) |(p-q).(J-Jhat)| = span(J-Jhat).

Rational lotteries suffice for the maximum, since point-mass choices attain it.
Thus all fixed-policy cost comparisons are accurate to epsilon exactly when the
joint error span is at most epsilon. Neither absolute cost error need be bounded
when their common component is unbounded.

**Proof.** For e=J-Jhat, both p.e and q.e lie between min(e) and max(e). Their
difference has magnitude at most the span. Point masses at its maximizing and
minimizing entries attain the span. QED.

For a particular p,q, the sharper bound is

    |(p-q).e| <= (1/2)||p-q||_1 * span(e).

Write v=p-q, whose coordinates sum to zero. Shift e by its minimum so its
coordinates lie in [0,span(e)]. Its positive-weight contribution is at most
`sum(v_+) * span(e)`; its negative-weight contribution gives the opposite bound.
Both positive and negative coefficient masses equal ||v||_1/2. The coefficient
is attained by errors that are maximal on positive v entries and minimal on
negative ones. This refinement distinguishes nearly identical lotteries from
completely different actions.

### Explicit unbounded common-error example

Take `Jhat=(0,1,2)` and `J=(z+1/4,z+7/8,z+2)`, where z is unrestricted.
The error vector is `z*1+(1/4,-1/8,0)`. Its span is 3/8 regardless of z.
Every pairwise policy comparison is therefore accurate to 3/8 even though no
finite uniform bound exists on any absolute error. The A-versus-B contrast
attains 3/8. This is a relative-error statement, not an absolute adequacy warrant.

### Extending to nonlinear but baseline-respecting use

If F is monotone in each cost coordinate and obeys
`F(J+c*1)=F(J)+c`, then for any e,

    min(e) <= F(J+e)-F(J) <= max(e).

Insert the componentwise sandwich `J+min(e)*1 <= J+e <= J+max(e)*1` and use
monotonicity and the shift law. Hence for two such functions F,G,

    |[F(J+e)-G(J+e)]-[F(J)-G(J)]| <= span(e).

Minima, maxima, and fixed probability mixtures have these properties and are
closed under suitable nesting. This is an approximation theorem about two
cost computations; it does not make a pointwise minimum an executable action,
or say that every strict improvement survives a saturating downstream map.

For a general finite CPWA contrast whose affine gradients v satisfy sum(v)=0,
a global gain `max_regions ||v||_1/2` bounds sensitivity in the span seminorm.
To prove this, restrict to a line segment between the two inputs, integrate the
finitely many affine slopes, and use the previous zero-sum coefficient bound on
each segment. Boundary-contained lines follow by continuity. Domain-relative
variants must check all reached regions, not only the starting derivative.

## 14. Approximate transport still needs one joint model match

Suppose a source comparison uses the same finite available program set and the
same observation-based lottery tables on a new source and an old source.
For every new situation choose an old situation with the corresponding visible
observation and with cost-vector error span at most epsilon. Then every old
paired bound b transfers to a new bound b+epsilon. If the lottery contrast has
coefficient mass at most tau in each visible cell, use b+tau*epsilon instead.

**Proof.** Fix one new situation, use its matched old situation, apply Proposition
8 to the same p_o,q_o, and add the old bound. Universal quantification proves the
claim. Matching may depend on the hidden situation because it is a mathematical
witness, not a deployed action. The policy tables themselves may not. QED.

Separate matches for separate actions do not suffice. Sources with cost vectors
`{(0,0),(2,2)}` and `{(0,2),(2,0)}` give the same marginal range for each action,
but the first has every action contrast zero and the second has contrast bound
two. A joint source-aware match, not independent interval fitting, is needed.

For a numerical abstraction containing the concrete image, universal abstract
validity implies concrete validity. An abstract countermodel can be spurious.
If a reverse approximate match exists as above, its possible loss of precision
is controlled. Without such a match, a certificate for one query does not make
an abstraction exact for every later query or observation.

### A concrete adapter/update test

On theta in [1/4,3/4], the single chord for the squared component is
`U(theta)=theta-3/16`, with `0<=U-theta^2<=1/16`.
It preserves the sharp original old-theta versus new-theta-squared improvement
of 3/16. After the new observation theta=1/2, the exact squared component is 1/4,
but the unreconstructed chord source still permits q=5/16. The exact comparison
with old theta is -1/4; the abstract upper comparison remains -3/16.
A stronger threshold -7/32 is now concrete-valid but abstract-invalid.
The old adapter remains sound; it is simply not exact for the newly sharpened
question. Its witnessed gap is 1/16, consistent with its original error budget.

## 15. Optional point-estimate decision use, with its strong premise exposed

Suppose a cost-vector estimate Jhat(o) is visible and for every modeled situation
compatible with o its joint error span is at most epsilon. Let a_hat minimize
Jhat(o). Then in each such situation,

    J_a_hat - min_a J_a <= epsilon.

**Proof.** Let a_star minimize the actual finite vector in that situation.
Subtract and add the two estimated entries. The estimated difference is <=0;
the difference of their estimation errors is <=epsilon by Proposition 8. QED.

The selected action depends only on visible o. The hidden a_star is a benchmark,
not an input to the policy. The premise is strong: it requires simultaneous
relative accuracy of the entire available action-cost vector. Individual average
prediction losses, independently calibrated intervals, or an accurate robust
score alone do not establish it. The bound provides a possible later loss-to-use
adapter, not a universal claim that minimizing any training loss yields value.

Adding a common input-dependent baseline to all action costs also leaves the
modeled fixed-policy objective's ordering unchanged. For a differentiable
normalized policy family with costs independent of its parameters,

    gradient_theta sum_a pi_theta(a|o) J_a
      = sum_a gradient_theta pi_theta(a|o) (J_a-b(o)),

because `sum_a gradient_theta pi_theta(a|o)=0`. This elementary identity explains
why relative costs are naturally relevant to an ordinary policy-learning loss.
It is a baseline, not a new policy-gradient result, and it does not identify any
particular learned hidden unit as a proof or cost. Parameter-dependent costs or
baselines require their missing derivative terms to be included.

## 16. A second reconstruction of the arithmetic evaluator

For a term t, let FS(t) be its free source keys, FL(t) its free lexical locals,
and CM(t) its used conversion names. Sources and lexical locals are disjoint name
classes. For `let y=e in b`,

    FS = FS(e) union FS(b),
    FL = FL(e) union (FL(b) minus {y}),
    CM = CM(e) union CM(b).

The bound name is absent only from the body's free locals, not from those of its
right-hand side. This handles shadowing without evaluating the right-hand side
in the newly extended environment.

### Proposition 9 — pointed evaluation uses only its explicit support

If two well-typed assignments/environments agree on FS(t), FL(t), and the used
conversion meanings, their evaluations of t agree. A lexical-local renaming
that avoids capture, with its environment transported, also preserves evaluation.

**Proof.** Induct over the finite syntax. Leaves use exactly their named entries.
Each arithmetic operation is a deterministic function of its recursively equal
children. In a let, equal evaluations of e give the same new bound value; outer
locals used by b but not shadowed by y agree, and y agrees by that new value.
The induction hypothesis for b then applies. A conversion uses the same fixed
factor and its equal child value. QED.

This permits an evaluator cache to use the relevant environment projection, not
necessarily an entire environment. Caching by syntax identity alone is unsafe:
`let y=1 in loc(y)` and another evaluation of the same local node under y=2
must return different values. A cache key is an implementation aid, not a new
semantic quantity.

Numerical dead-binding removal is valid when y is not free in b because this
arithmetic language is pure and total after typing. It is not a theorem that
removing an executed real-world stage preserves a plan's behavior or use cost.
Similarly, t+t doubles the modeled numerical contribution even if the evaluator
computes t only once. Arithmetic sharing and counted resource usage are distinct.

For source substitution sigma, the environment map is
`nu_sigma(x)=[[sigma(x)]]_nu'`. Structural induction proves the substitution
identity. Transferring a *source-relative judgment* additionally requires
`nu_sigma` to lie in the old domain. The syntax/evaluation lemma alone neither
validates the old source assumptions nor preserves the policy's observations.

## 17. Removing accidental assumptions from the observation result

The observation feasibility result of section 4 requires the same costs and
available actions after the observation interface changes. It does not make
information free. In the two-action example, blind optimal worst cost is 1.
Revealing the hidden mode reduces action cost to 0, but an unavoidable observation
charge 2 makes total cost 2. If declining the observation remains available, the
old cost-one policy remains a valid option. Each acquisition plan must include
its actual charge in its registered cost; logical access to a case split is not
an information-acquisition primitive.

A proof may use a different mathematical witness in each hidden source case while
certifying one fixed policy. It may not replace that policy by a different action
per case unless the corresponding observation was actually acquired. This is the
same distinction as in the case-specific arithmetic certificate portfolio.

More visible information can refine which cases remain possible, expand which
policies are admissible, or both. These are separate effects:

* Source restriction alone preserves old fixed-policy comparisons.
* Policy-class expansion alone preserves availability of the old policy but
  does not certify the new policy's improvement.
* A new observation that changes the data-generating process, evaluator, or
  acquisition cost changes the relevant interpretation as well.

The finite visible interface is a bounded example specification, not a claim
that all eventual neural inputs must be finite-valued. A fixed deployed network
may be one registered program whose input/output behavior receives a separate
loss model. A more expressive internal policy language needs its own semantics;
its properties are not silently supplied by the present finite table.

## 18. Reconstructing the three principal interpretations from component models

### I — additive use with one shared quantity

There are two stages and one U-valued unknown theta in [0,1], with nonnegative
baselines z1,z2. The old program incurs `(z1+3/4)+(z2+theta)` and the new program
`(z1+theta)+(z2+1/4)`. Subtracting after addition cancels both baselines and theta,
giving -1/2. At theta=1/2,z1=z2=0 the respective totals are 5/4 and 3/4.

If the quantities are instead independent *source coordinates* theta1,theta2
in [0,1], the difference is theta1-theta2-1/2; its attained range is [-3/2,1/2].
This source set says that all coordinate combinations remain possible, not that
a probability law factors. The matching names or equal marginal intervals of
two evaluations cannot restore the missing equality premise.

The old and new plans both have two baseline-bearing stages. The baseline
counterexample of section 9 would apply to a later change in exposure count.
The native source remains nonempty before and after restriction to theta in
[1/4,3/4], and the original comparison is unchanged.

### II — report-dependent controller with explicit proxy alignment

At a fixed report r, P executes with probability 1-r and S with probability r.
Conditional failure rates are p,s. Hence `H_r=(1-r)p+rs`, and the additional
expected S-branch charge is r/4. These are expectations under a specified
kernel, not data-conditioned empirical estimates.

Use `p=s+1/2, 0<=s<=1/4`. Then

    H_(1/2)=s+1/4,       H_(3/4)=s+1/8,
    L_(1/2)=z+s+3/8,     L_(3/4)=z+s+5/16.

The report residuals are `s-1/4` and `s-5/8`, both <=0. The proxy difference is
`5/16-3/8=-1/16`. For named intended costs
`J_old=L_old+w` and `J_new=L_new+w+e`, the paired difference is `-1/16+e`.
The interval `-1/32<=e<=1/32` gives the sharp upper bound -1/32, attained at
s=0,p=1/2,z=w=0,e=1/32. Increasing only its upper endpoint to 3/64 changes the
sharp bound to -1/64 and leaves both report inequalities unchanged.

All these costs are nonnegative in the supplied interpretation. Their absolute
values are nevertheless unbounded as z,w grow. Removing the e premise permits
arbitrary intended-cost deterioration while leaving the proxy computation and
self-report valid. The claim is therefore explicitly conditional on the paired
alignment model, not on a belief that the proxy is ultimate utility.

For r=2/5, `H_r=s+3/10`; at s=0 it is below r, while at s=1/4 it is 11/20>r.
The uncertain report has both a satisfying and a violating rational model.
Changing the code to use P with probability r reverses the proxy comparison's
sign to +1/16; matching report strings are not matching program semantics.

### III — two conditionally independent calls with one unknown parameter

For two Bernoulli calls with shared fixed parameter theta, the joint success
probability is theta^2 only under the declared conditional-independence premise.
A reused random draw would give theta instead. Unknown-parameter sharing and
fresh-execution independence concern different layers of the model.

For theta in [a,b], the chord `(a+b)theta-ab` differs from theta^2 by
`(theta-a)(b-theta)`, lying in [0,(b-a)^2/4]. This is a component-level enclosure.
On [1/4,3/4] a single chord suffices for the old-versus-new comparison:
`U(theta)-theta=-3/16`. The four-cell version reduces component approximation
error to 1/256, but does not improve this particular sharp paired bound.

The abstract q source remains a nonempty finite union of rational polyhedra;
each mesh endpoint with q=theta^2 is a rational witness. The exact squared-cost
model maps inside that source. Its validity therefore implies the concrete bound,
while the stricter post-observation example in section 14 shows why a later
countermodel in the outer source need not refute the concrete computation.

This reconstructs three complete operational interpretations without assuming
a primitive that supplies the final comparison. It is not an F06 derivation
system or F07 derivation-level soundness proof.

## 19. Case-dependent interpretations need not enlarge the numerical kernel

The S1 fixture evaluated one expression pair across all source cases, while the
specification also admitted a different cost interpretation in each hidden case.
These two descriptions are compatible by an explicit definitional elaboration.

### Proposition 10 — finite graph elaboration

Suppose each retained case h has a nonempty rational polyhedron P_h and, for
each fixed registered program a, a rational CPWA cost term J_(h,a)(x). Introduce
one derived source coordinate g_a for each program. Refine P_h by the finite
joint affine regions of these terms; on each nonempty region add the equations

    g_a = J_(h,a)(x)   for every a.

Each equation is a pair of affine inequalities on that region. All resulting
cases are rational polyhedra. Every original model has a unique vector g of
cost values and at least one corresponding refined case. Conversely every
refined model has exactly the original interpreted g values. Hence every common
policy comparison using g has the same value and the same universal bounds as
the case-indexed interpretation table.

**Proof.** On a selected region each defining term is affine, so the graph
constraints express equality exactly. Shared boundary regions give duplicate
presentations but equal cost values, because the terms are continuous. Evaluation
supplies a lift of every original point, and projection of a graph point removes
only values fixed by these equations. A rational source witness evaluates to a
rational graph witness. The finite union gives both directions. QED.

These are *defined* coordinates, not unconstrained primitive final scores. Their
component term graphs and interpretation versions remain recorded. The elaboration
may be expensive, and is not asserted to be the preferred runtime representation.
It is a semantic check that case tables do not require an additional numerical
connective or a hidden-policy oracle. It does not turn a nonlinear term such as
theta^2 into a finite CPWA graph; that still needs the declared adapter.

### A full ML-loss example in two graph regions

Let `y>=3/4, 0<=c<=1/4, z>=0`, with

    J_old=|y|+z,   J_new=|y-1|+c+z.

On `3/4<=y<=1`, their difference is `1-2y+c`, with range [-1,-1/4]. On `y>=1`
it is `c-1`, with range [-1,-3/4]. The complete relative image is [-1,-1/4].
Thus three source coordinates, including unbounded y and z, can be replaced by
one interval for all native queries of this *one fixed relative difference*.
Absolute costs and later y- or c-dependent evidence need the richer presentation.
At y=3/4,c=1/4,z=0 the difference -1/4 is attained. The two graph regions have
explicit affine equality rows for g_old,g_new and rational feasible witnesses.

## 20. A smaller reflective presentation for the declared current questions

For the two principal reports r0=1/2 and r1=3/4, let

    d = J_new-J_old = -1/16+e,
    u = H_(1/2)-1/2 = s-1/4.

Then `H_(3/4)-3/4 = u-3/8`. Under the S1 source the exact image is the rectangle

    -3/32 <= d <= -1/32,   -1/4 <= u <= 0.

Every point in that rectangle has a source lift:

    e=d+1/16, s=u+1/4, p=s+1/2, z=w=0.

The lifted p,s satisfy all probability constraints and the named intended costs
remain nonnegative. Thus this is exact for the current paired-cost and two-report
shortfall queries, not merely a containing box produced by losing correlations.
After weakening e's upper bound to 3/64, only d's upper endpoint changes to -1/64.
The report coordinate u and its warrant are unchanged.

Two coordinates rather than all p,s,e,z,w therefore suffice for these fixed
questions and this specified update. They do not suffice for absolute-cost
questions because z,w were removed. They also do not make every future report
parameter or different controller version part of the same judgment by fiat.
Some further reports can be reconstructed under the same branch model from u,
but new cost/interpretation premises must still be declared for new versions.

This is a concrete example of the exact-update criterion: the e update is
expressible as an inequality on d. An observation on w is not. Scope/provenance
for the two retained coordinates remains necessary for later warranted reuse.

## 21. The self-controller's finite execution law

To check that the preceding probability terms are not arbitrary score labels,
spell out the four execution outcomes of SELF-MIX(r), conditional on p,s:

| Outcome | Probability | Extra cost, excluding common z |
|---|---|---|
| S and failure | r*s | 1+1/4 |
| S and no failure | r*(1-s) | 1/4 |
| P and failure | (1-r)*p | 1 |
| P and no failure | (1-r)*(1-p) | 0 |

For fixed rational r and valid p,s these probabilities are nonnegative and sum
to one. Summing the failure rows gives H_r. Summing the cost rows gives
`H_r+r/4`. The common unknown z contributes z because the probabilities normalize.
This remains an affine native expression even though writing each probability
times z separately would introduce products that cancel. The assertion that
variable-probability composition *can* leave CPWA is not a claim that it always does.

For the random-report wrapper, multiply the four probabilities by each fixed q_i.
They still normalize. Conditional on a positive-probability emitted report r_i,
the failure rate is H_i. A zero-weight report has no such conditional obligation.
The calculation is a fully specified finite execution model; the actual validity
of its branch probabilities and independence assumptions is still conditional.

## 22. Compact semantic contract for the next task

The operative ingredients are now explicit:

* `Sigma` fixes source names, units and registered interpretation maps.
* At every visible o, a finite union of rational-polyhedral live cases supplies
  the modeled uncertainty, with a rational witness in each case.
* Pure finite terms denote pointwise finite signed values; their ranges need
  not be bounded. No runtime observation of an unknown source is introduced.
* A finite registry gives complete, typed component-use interpretations for
  the available versions. A policy binds rational choices to visible o only.
* The primary judgment quantifies the signed difference of the *same two uses*
  over every retained model. Countermodels, inconsistent contexts and undecided
  proof searches are separate things.
* Source changes, observation changes, program changes, and evidence-mode changes
  have separate transport obligations. A fingerprint is a guard, not a proof.
* Enclosures and proxy alignment are scoped assumptions/lemmas, not evidence that
  the physical world or ultimate utility is known. Report protocols specify
  whether a claim is unconditional, averaged, or conditional on the emitted report.

All three principal examples satisfy these clauses with nonempty models. The
continuation formulation remains an alternative when richer native closure is
needed. F06 must next decide a finite deductive presentation and derive useful
multistep rules; it may reuse these semantic lemmas with their assumptions.
Nothing here claims a complete reasoner, full RLL adoption, unrestricted logical
reflection, empirical interpretability, or a new theorem of the eventual calculus.

## 23. An evidence-responsive self-controller, not just two hypothetical constants

The three principal interpretations already meet the specified F05 scope. A
finite visible-policy elaboration makes the self-use interface more explicit.
It is a separate criterion instance: the checking charge here is kappa=3/4,
not the kappa=1/4 of the principal interpretation.

Let the fixed branch gap be d=p-s=1/2, with evidence `0<=s<=b`, where the visible
record b is either 1/4 (coarse) or 1/8 (refined). The program uses

    r(b) = (b+d)/(1+d)

as its report and as its S-branch probability. Thus the finite table chooses
r=1/2 at the coarse observation and r=5/12 at the refined observation. Its
arithmetic parameter calculation reads only the visible bound b, never p or s.
Failure randomness is generated by the environment kernel with rates p,s; the
agent does not need an oracle that reads those rates.

For any fixed b and admitted s,

    H_r = s+d-d*r,
    sup H_r = b+d-d*r,
    H_r<=r for all s<=b  iff r >= (b+d)/(1+d).

This proves the report guarantee and the choice's minimality among exact valid
reports. The denominator is at least one here; none of the singular behavior
near (p,s)=(0,1) from F04 is being ignored.

The declared total cost is

    J_r = z+H_r+kappa*r = z+s+d+(kappa-d)*r.

When kappa>d it increases with r, so the smallest valid report is also the
lowest-cost report satisfying this reporting contract. When kappa<d the cost
instead decreases with r; minimizing the report would then be a different
objective from minimizing use cost. This explains, rather than erases, the
principal example's alternative behavior.

At kappa=3/4 and on the refined source, comparing the new r=5/12 with the old
r=1/2 gives

    Delta r=-1/12,
    Delta failure=+1/24,
    Delta checking charge=-1/16,
    Delta total cost=-1/48.

The new report remains valid even though actual failure increases at each
retained source point. The lower resource expenditure more than offsets it
under the explicitly stated criterion. A paired discrepancy upper bound 1/96
would still leave intended-cost improvement of at least 1/96. No unqualified
claim that more information improves every objective is involved.

At the coarse observation the new visible policy uses exactly the old report,
so its paired change is zero. The observation-indexed guarantees are therefore
0 (coarse) and -1/48 (refined); the global bound across both observations is 0.
A single sharper global claim would be false. Both observation cells have
nonempty rational models. Source validity of the new b is a premise, not a
consequence of the controller emitting a smaller number.

For a known rational d, the formula with an explicit allowance xi is
`max(0,(b+d-xi)/(1+d))`. It is CPWA in b. Only the specified finite visible
instantiations are part of this F05 policy interface; this calculation does not
silently add a general continuous-observation policy language.

## 24. A proper prediction loss need not enforce a self-report under feedback

Use SELF-MIX again, now evaluate the conventional squared binary-prediction loss
for its own reported probability r. If Y has its report-induced failure rate H_r,
then direct expectation gives

    Brier(r) = E[(r-Y)^2] = r^2+(1-2r)*H_r.

For fixed r this is a native affine term in p,s. When examining r as a design
parameter, substitute H_r=s+d-d*r to obtain

    Brier(r)=(1+2d)r^2-[2(s+d)+d]r+s+d.

Its unconstrained minimum on [0,1] for the valid examples occurs at

    r_B = (2s+3d)/(2+4d),

whereas exact self-consistency H_r=r occurs at

    r_eq=(s+d)/(1+d).

Their difference is

    r_B-r_eq = d*(1-2s-d) / [2*(1+2d)*(1+d)].

It can have either sign. At p=1,s=1/2,d=1/2, r_B=5/8, H_(r_B)=11/16 and the
report underestimates its own failure by 1/16. Its Brier loss is 7/32. The valid
self-consistent report r_eq=2/3 has loss 2/9, which is larger by 1/288.
Thus even an ordinary proper prediction loss can prefer the invalid self-report
when changing the report changes the distribution being predicted.

This does not refute propriety for a fixed outcome distribution. For fixed H,
`Brier(r)=(r-H)^2+H*(1-H)` is minimized at r=H. Here H itself varies with r.
Likewise a small prediction loss is not a proof of the source assumptions. The
counterexample separates the *training/use objective* from the *report warrant*,
without declaring either one metaphysically privileged.

There is no quadratic primitive added to the selected core: the two reports are
fixed rational program instances, and their expected losses are affine source
terms. The quadratic parameter calculation is a metalevel explanation of those
instances. No training run or claim about a naturally learned network is made.

### Reconstruction correction

The baseline-gradient identity in section 15 subtracts a baseline inside a
score-weighted sum. Its equality remains valid even for a parameter-dependent
common baseline when that baseline is not differentiated on the right-hand side.
If one differentiates the *centered objective itself*, however, a parameter-
dependent baseline contributes its derivative and must be restored. Parameter-
dependent program costs also contribute `sum pi*gradient J`. This distinction
prevents a semantic invariance from licensing an incorrect training gradient.

## 25. Final interpretation-domain and conditioning checks

### 25.1 Probability units are not probability range proofs

The numeric carrier for a dimensionless source is still R. Calling a source p
'a probability' does not make the arithmetic expression H_r a probability when
its context admits p<0 or p>1. A probability interpretation of SELF-MIX requires
`0<=p,s<=1` throughout the admitted source, together with a normalized nonnegative
policy lottery. One feasible in-range point does not establish that universal
range obligation. The principal contexts give the necessary inequalities explicitly.

A numeric term can remain defined outside these ranges while the proposed
stochastic interpretation is inadmissible. A point violating an explicitly
assumed range is not a countermodel to a theorem whose domain includes that
range. The distinction is between a mathematical expression, a kernel model,
and a justified use of that model.

Graph elaboration in section 19 compiles the named conversion maps along with
the term. Its numerical matrix rows do not license adding unlike units. A
probability-to-loss map such as one U per failure remains a declared valuation
bridge, including when its factor happens to be numerically one.

### 25.2 Observation-indexed guarantees are a finite family of old judgments

A table of rational bounds b(o) abbreviates one primary comparison in each live
visible context C(o). A violating model names o as well as h,x. Combining the
family into one observation-independent bound takes the maximum of the component
bounds, not their unweighted average. A different aggregation requires a declared
law over the observations and its own task meaning.

The adaptive controller's 0 and -1/48 bounds are an example. The second does not
hold before the refined observation merely because it is the better number.
The emitted report in section 6 is a *later* observation of the wrapper's output,
not information available to select that wrapper before its draw. Conditional
report assessment must not reverse that temporal order.

### 25.3 A marginal evidence guarantee is not a guarantee conditional on each output

Let a data procedure observe o=0 with probability 9/10 and o=1 with probability
1/10, while the actual parameter is theta=1. It returns C0=[0,1] and C1={0}.
Overall source coverage is 9/10, but conditional on o=1 it is zero. Both reported
source sets are nonempty. A valid arithmetic conclusion theta<=0 under C1 does
not have conditional 9/10 reliability at that observation.

The S1 coverage-to-use implication remains correct at its stated *marginal*
sampling scope: on the coverage event the selected, conditionally proved statement
holds. It does not silently supply conditional coverage, a posterior probability,
or validity under a new sampling procedure. Source validity and uncertainty about
it remain outside the exact inequality checker.

No new confidence calculus is selected here. This finite counterexample just
checks that future implementations retain the scope of the already specified
mode premise rather than replacing it with one universal confidence label.

### 25.4 Arithmetic equality, action identity, and update identity

Two programs with equal expected costs can have different report protocols or
resource traces. Two contexts with equal relative images can permit different
visible policies. Two sources with identical current comparisons can respond
differently to a later update. These are witnessed above, not asserted as an
unbounded list of metadata requirements. The relevant observation/query/update
contract decides which distinctions must be retained.

The compact arithmetic kernel can therefore remain small while its use record
retains exactly the source, program and criterion versions needed by those
contracts. F05's choice stays provisional; an extension needing unsupported
closure or hidden-case actions must be respecified rather than represented by
an unexplained number.

## 26. One successful update does not prove compositional update correctness

A more stringent check of convex source compression is useful for later
open-ended revision. Let R be the boundary of the unit square, represented by
its four rational line-segment cases, and let K=[0,1]^2 be its convex hull.
All initial linear bounds agree on R and K.

First add evidence x>=1/2. The exact surviving boundary has its top and bottom
half-edges and the right edge. Its convex hull is `[1/2,1] x [0,1]`, exactly the
result of cutting K. Thus this update genuinely preserves all linear bounds.

Next add y>=1/2. The exact source now contains only the top and right half-edges:

    R2 = {(x,1): 1/2<=x<=1} union {(1,y): 1/2<=y<=1}.

Its convex hull is the triangle satisfying x+y>=3/2 inside the upper-right
quarter. Cutting the previous convex summary gives the entire quarter instead.
The two sources remain nonempty and give different bounds:

    sup_R2 [-(x+y)] = -3/2,
    sup_naive [-(x+y)] = -1.

A witness to the latter is (1/2,1/2), which no original boundary case realizes.
The former is attained at (1/2,1) and (1,1/2). For an actual lottery comparison,
use a zero-cost reference versus the equal mixture of costs x and y; the two
bounds become -3/4 and -1/2.

This is not an unsafe *outer* approximation: the naive summary is conservative.
It is a counterexample to claiming exact reuse from one verified update step.
The relevant simulation/update property must hold for the reachable class of
source states, not only the original source.

The effect is not limited to an unlucky first cut. For the boundary of a
full-dimensional compact polygon, every single closed halfspace cut initially
has the same convex hull as cutting the polygon. Every extreme point of the
cut polygon lies on the old boundary: an interior point of the old polygon on
the cut line has a small segment along that line inside the cut, so is not
extreme. Convexity then gives the claim. Two cuts can instead create a new
interior intersection vertex, as above. This explains precisely why repeated
updates expose the lost information.

A repair within the selected semantics is to retain the four original source
cases and apply both cuts before taking an optional linear summary. Bottom and
left cases are removed only after their infeasibility is established; top and
right retain explicit witnesses. A case-specific proof of the same fixed query
then gives -3/2 without requiring the deployed policy to know which edge is real.
No new principal carrier or new numerical primitive is needed.

## 27. A direct margin-loss / log-loss adapter

The selected native grammar should not be confused with a claim that only
piecewise-affine training losses matter. A concrete analytic adapter connects it
to ordinary log loss without adding an exponential or logarithm primitive.

For a binary classification margin m define

    h(m)=max(0,-m),
    ell(m)=log(1+exp(-m)).

Direct factorization gives

    ell(m)=h(m)+log(1+exp(-|m|)),
    0<=ell(m)-h(m)<=log(2).

The remainder is uniformly bounded although both losses are unbounded above.
The margin is relative to the evaluated label; increasing a raw logit is not
assumed to improve that margin without its label/source condition.

A simple exact rational enclosure is log(2)<=3/4: on [1,2], the convex function
1/x lies below its chord, whose integral is 3/4. Equivalently integrate the
nonnegative chord difference. Thus a source coordinate for the remainder may
be constrained to [0,3/4] as an explicitly proved outer model. It is not an
arbitrary learned confidence label.

### A complete paired example with a use cost

Let m<=-1, let the new margin be m+1, and let its extra resource charge be 1/8.
The native margin losses differ by -1. Introduce remainder coordinates r_old,
r_new in [0,3/4], and an unrestricted common finite baseline z. The interpreted
costs are

    J_old=z+h(m)+r_old,
    J_new=z+h(m+1)+r_new+1/8.

Their sharp bound in this outer source is

    J_new-J_old <= -1+3/4+1/8 = -1/8.

The exact log-loss model maps into it by the analytic remainder identity. Hence
the new program improves the declared log-loss-plus-resource criterion by at
least 1/8 on the specified source. Both individual losses can grow without bound.
A feasible outer model is m=-1,z=0,r_old=0,r_new=3/4; it attains -1/8. That
outer extremum need not be attainable by the exact logarithmic remainders,
which is precisely the distinction between sound abstraction and exactness.

This is an analytic proxy-to-task premise, not a claim that log loss is ultimate
utility or that the margin relationship has been empirically established. A
further intended-value claim still requires its own alignment premise.

### Why a global strict improvement can lack a uniform margin outside CPWA

For c>0, `ell(m+c)-ell(m)<0` for every finite m, but its supremum over all real
m is zero as m tends to +infinity. Thus no fixed negative budget works globally.
Its derivative with respect to m is

    1/(1+exp(m)) - 1/(1+exp(m+c)) > 0.

This independently verifies the limiting direction. Adding any positive resource
charge can make the replacement worse for sufficiently large positive margins.
The selected finite CPWA source guarantee is not allowed to hide this nonlinear
boundary under an unjustified 'strictly better therefore uniformly better' rule.

### Multiclass version and neural-coordinate relevance

For K finite logits z_j and evaluated label y,

    ell(z,y)=log(sum_j exp(z_j))-z_y,
    h(z,y)=max_j z_j-z_y=max_j res(z_y,z_j),
    0<=ell(z,y)-h(z,y)<=log(K).

Factor exp(max z) out of the sum to prove the enclosure. The native proxy uses
only maximum and a signed difference. A common logit shift cancels from both.
For a logit perturbation e, monotonicity and shift covariance of log-sum-exp give

    min(e)-e_y <= ell(z+e,y)-ell(z,y) <= max(e)-e_y.

Its absolute change is therefore at most span(e), even if a common logit offset
is unbounded. This is a concrete instance of the comparison metric in section 13.
It supplies a source-aware loss interpretation for future neural tests without
identifying every number as a truth degree or imposing a special neural layout.
It is a standard mathematical relation, not a claim of a new log-loss bound or
an observed mechanism in a trained network.

## 28. Adversarial reconstruction of the abstraction claims

### 28.1 Why the closed convex hull is polyhedral here

For finitely many nonempty rational polyhedra P_i={x:A_i x<=b_i}, introduce
lambda_i>=0, sum lambda_i=1 and vectors u_i satisfying

    A_i u_i <= lambda_i b_i,    x=sum_i u_i.

The projected feasible x set is a closed rational polyhedron. It contains every
P_i and is convex. Conversely choose a fixed witness v_i in each P_i. For any
feasible lifted point and 0<epsilon<1, put

    lambda_i^eps=(1-epsilon)lambda_i+epsilon/k,
    u_i^eps=(1-epsilon)u_i+(epsilon/k)v_i.

These have strictly positive weights, satisfy the lifted constraints, and give
a point in conv(union P_i) tending to x. Thus the lifted set is exactly the
**closed** convex hull. The closure is necessary: a point (0,1) together with
the ray {(x,0):x>=0} has convex hull missing (x,1) for x>0, although those points
belong to its closure. No claim that every convex combination is attained is made.

This supplies the premise used in section 10's rational linear separation. If
two such closed hulls differ, one rational defining inequality of one hull is
violated in the other. Its direction becomes a difference of rational lotteries
by the positive/negative mass construction. The quantitative bound uses a
supremum, so taking closure is exact for that initial linear query even where
actual mixed-model attainment is different.

### 28.2 Normalization is a load-bearing condition, not decoration

The relative comparison uses coefficients summing to zero. If p and q are
subprobability vectors with different total mass, a common error offset is no
longer harmless. For p=(1/2,0), q=(0,1), and e=z*(1,1), span(e)=0 but
`(p-q).e=-z/2`. This is a counterexample to omitting the equal-mass condition.

Equal total masses, even other than one, retain cancellation with the appropriate
coefficient gain. For policy probabilities the declared mass is one. Missing
termination/fallback probability must receive an explicit outcome and cost, or
remain outside the finite-loss interpretation; it cannot be assigned free value
by omission. This does not add infinity-valued execution costs to the core.

### 28.3 An absolute anchor changes what baseline erasure permits

The span calculation concerns errors in a *joint family* of costs. If a fixed
zero-cost reference is included and must remain exactly zero, its error is zero.
A common arbitrary offset is then no longer a permissible error of that anchored
family. Thus the relative-cost result cannot be used to certify absolute adequacy,
probability normalization, or a report bound against a fixed literal by ignoring
the literal's anchored meaning.

The reflective two-coordinate presentation explicitly retains report residuals
relative to the actual reported numbers. It does not quotient probability values
by arbitrary shifts. Its loss coordinate and probability coordinate keep their
different units; the span seminorm is not applied across unlike units.

### 28.4 Observation and policy transport must commute

For the approximate transfer in section 14, use the same visible alphabet and
the same two lottery tables, or supply a map between visible alphabets under
which both tables are transported. The matched old visible observation cannot
vary with the hidden new state while the claimed deployed action remains fixed.
Likewise, the old reference policy in a coarsening test must be coarsely measurable
when claimed available there. A hidden-state-dependent benchmark is permissible
only as a benchmark, not as an available fallback or transported executable policy.

### 28.5 The loss adapter is not a standard unit-margin hinge identity

The binary native proxy h(m)=max(0,-m) in section 27 is a *zero-margin* ReLU loss.
It is not the different function max(0,1-m). The exact log-loss remainder identity
uses the stated zero-margin convention. In its concrete cost example z may be
restricted to z>=0 so the interpreted losses remain nonnegative; the comparison
and unbounded-range argument are unchanged.

## 29. What the chosen value objects are, before taking any summary

For one fixed context and one unit, identify two native terms only when they have
the same value at every admitted source point. The resulting functions form an
ordered rational vector lattice: addition, rational scaling, min and max are
pointwise, and equality on that context is a congruence for those operations.
The positive cone consists of functions nonnegative at every admitted point.
Every function splits as

    t = max(t,0) - max(-t,0).

This is existing ordered-algebra structure, not a new algebra claimed by F05.
There need not be a strong order unit: an unbounded source term cannot be bounded
by any constant multiple of 1. The unit label names the measurement/criterion,
not an axiom bounding all values.

The residual is pointwise positive part,

    res(a,b)=max(b-a,0),
    res(a,b)-res(b,a)=b-a.

So nonnegative internal quantities can jointly represent a signed difference.
But *separately summarized* residuals need not preserve its guaranteed margin.
Differences with possible values {-3,-1} and {-3,0} both have positive-part
supremum 0 and negative-part supremum 3. Only the first guarantees a strict
one-unit improvement. This is a concrete reason to retain the signed source-
relative comparison rather than two independently pooled nonnegative scores.

The source supremum is a summary, not the definition of every value object.
It preserves maximum and translation by constants, but need not preserve
addition, minimum, or negation. For example, with d1=x and d2=1-x on [0,1],
`sup(d1+d2)=1` whereas `sup d1+sup d2=2`. With the two hidden cost cases (0,2)
and (2,0), `sup min=0` whereas `min sup=2`. Negation exchanges supremum with
negative infimum, not with negative supremum. These are why shared-source
composition happens before summary.

For signed comparison budgets, positive scaling scales the bound; negative
scaling swaps the compared terms before using a positive factor. Multiplication
by zero is evaluated as the zero term, not by an unexplained 0*infinity convention
at the summary level. The term values remain finite at every interpretation.
These are semantic calculations that F06 may use to design rules, not a completed
proof system installed by this task.

### A latent algebraic witness is not necessarily a deployable allocation

If 0<=c<=a+b with a,b>=0 pointwise, define

    c1=min(c,a),   c2=c-c1.

Then c1+c2=c, 0<=c1<=a and 0<=c2<=b. If c<=a the second part is zero; otherwise
c1=a and c2=c-a<=b. All these are native value terms.

Yet cases (a,b,c)=(1,0,1) and (0,1,1) admit no common constant nonnegative
allocation c1,c2 with sum one and the same upper limits. Each constant would
have to be zero in one case. The pointwise decomposition uses hidden-source
values. It may be a proof witness or a contingent plan *when the case is visible*,
but is not a blind executable allocation. This additional check confirms why
the policy interface cannot be removed solely because the value algebra is rich.

Changing a source by restriction preserves term equalities. Weakening evidence
can break them: x=y in an old source allows replacing one by the other there;
a new source allowing x!=y does not. Numerical identity on a context, syntactic
identity, and preserved meaning under every update are therefore different notions.

## 30. A constructive middle ground between forgetting a source and keeping it all

The failures of projection do not require keeping every latent coordinate forever.
For a retained value d and one eliminated scalar y, suppose the current source
S is a finite union of rational polyhedra. On each retained d define its fiber
`S_d={y:(d,y) in S}` and, when nonempty, `a(d)=inf S_d`.

For a new upper-threshold observation y<=c,

    projection_d(S intersection {y<=c})
       = {d in projection_d(S): a(d)<=c},

where a(d)=-infinity permits every finite c. This equivalence uses attainment
when a(d) is finite. Each nonempty scalar fiber is a finite union of closed
intervals/rays/points, so its finite infimum is attained. Without that condition,
an infimum equal to c could give a false existence conclusion.

Successive upper-threshold observations on the same y preserve the same lower
endpoint on every surviving fiber. Thus the pair `(retained domain, a)` is enough
for any sequence of those updates, together with updates expressible on d alone.
It is a richer summary than the projected value set, but need not retain the full
fiber. This is a specified source-family contract, not a promise about every
future observation or an implemented efficient projection solver.

### Native example

Take `-2<=d<=2` and `y>=|d|`. Its current d image is [-2,2], and a(d)=|d|.
Observing y<=1 refines the image exactly to [-1,1]. The alternative source
`-2<=d<=2, y>=0` has the same initial image but a(d)=0 and retains [-2,2].
The native CPWA conditional lower function supplies exactly the missing information.
A source witness at any retained d is y=|d| in the first model and y=0 in the second.

The contract does not cover arbitrary interval observations on a nonconvex fiber.
Fibers {0,2} and [0,2] have identical minima and maxima but respond differently
to y=1. Nor do separate summaries for two omitted coordinates preserve a joint
observation: points (y,z)=(0,2),(2,0) each permit y<=1 or z<=1 separately but never
both. Retain a joint conditional relation or a correspondingly narrower update class.

If the source is convex, scalar fibers are intervals, so retaining both endpoints
is enough for successive interval restrictions, with the usual nonemptiness test.
These positive cases identify concrete, potentially compact interfaces instead
of using the negative examples to demand universal lossless storage.

Finally, approximation direction matters. A lower approximation to a(d) retains
an outer set of d possibilities after an upper-threshold update, conservative
for universal cost bounds. Filtering with an upper approximation can discard
real possibilities and is not automatically sound for those bounds. An inner
existence certificate and an outer uncertainty model serve different consumers.

## 31. Final operational reconstruction: evaluation is pure; execution need not be

The numeric evaluator is a structural recursion on a finite term. Every recursive
call is on a strict subterm; a let evaluates its right-hand side under the outer
environment, then its body under the updated lexical environment. Every primitive
operation on finite typed real values is total and deterministic. This gives a
unique result by induction. A left-to-right stack implementation uses continuation
frames that retain the correct lexical environment; frame evaluation agrees with
that recursive result by the same induction. There are no side effects, random
draws, hidden-source observations, or recursive program calls in this interpreter.

That result must not be confused with the semantics of the actual registered
programs. In particular, normalized lottery weights alone do not prove that a
wrapper's expected cost is a weighted sum of *standalone* program expectations.
The declared execution model must preserve those conditional expectations.

Here is a finite counterexample. Let U be a fair bit. Standalone A has cost
`1{U=0}` and standalone B has cost `1{U=1}`, so both mean costs are 1/2. A wrapper
selects A when U=0 and B when U=1, then **reuses that same bit** in the branch.
Its cost is always 1, not the naive weighted mean 1/2. With a fresh independent
bit V used in the branch, the weighted mean 1/2 is correct. Equal branch weights
and correct standalone means did not specify the missing joint execution law.

Fresh independent randomness is a sufficient interface condition, not the only
possible one; equality of the required conditional branch expectations suffices.
The principal SELF-MIX and squared-component interpretations state their relevant
freshness/conditional-independence laws explicitly. This example does not refute
those models, or arithmetic linearity of expectation. It prevents a future
composition rule from replacing a missing execution premise with normalization.

## 32. Reconstruction disposition

The fresh pass found no contradiction in the selected F05 interpretation. It
made several previously implicit boundaries explicit: complete case-indexed cost
tables, fixed visible policy choices, report-conditional versus averaged claims,
valuation bridges versus coordinate conversions, and the exact query/update scope
of numerical simplification. The new examples have nonempty rational models and
retain the original three interpretations rather than replacing them.

The additional loss adapter and evidence-responsive controller are scoped
interpretations of the same chosen objects. No new logical connective, general
policy optimizer, opaque final-score oracle, or richer proof reflection was
required. The continuation alternative remains available where finite CPWA
closure or its enclosure precision is insufficient.

This is completion evidence for a **provisional semantic specification**. The
actual deductive rules, their derivation-level soundness and the later strongest
characterization still belong to F06–F08. Formal representability, a successful
finite check and a naturally learned causal computation remain separate claims.

## 33. Final numeric and nonvacuity reconstruction before implementation

The small fixtures should implement these already-derived targets, rather than
supply the mathematical argument after the fact:

| Witness | Exact reconstructed result |
|---|---|
| Blind equal lottery in the two swapped-cost cases | worst cost 1; revealing the case permits cost 0 |
| Relative errors (1/4,-1/8,0) plus any common baseline | span 3/8; contrast coefficient mass 1/4 gives sharp error 3/32 |
| Equal randomization of reports 0 and 1 at p=1/2,s=0 | mean failure 1/4, mean report 1/2, average positive shortfall 1/4 |
| Performative Brier example p=1,s=1/2 | invalid report 5/8 has loss 7/32; valid report 2/3 has loss 2/9; loss gap 1/288 |
| Evidence-responsive controller, kappa=3/4 | report change -1/12; failure +1/24; resource -1/16; total -1/48 |
| Square-boundary source after two cuts | upper bound on negative coordinate sum -3/2, versus coarse -1 |
| Absolute-error-plus-resource source | complete relative range [-1,-1/4] |
| Binary log-loss outer adapter with charge 1/8 | sharp outer paired bound -1/8; exact model lies inside the source |

Every operational case used for a warrant has an explicit feasible rational
assignment. A filtering operation may produce an empty set, but that cannot be
repackaged as a deployment context with a zero bound. Nonemptiness itself is an
observable that an update-aware representation must preserve or re-establish.

Unboundedness is across modeled assignments, with finite values at each one.
Cancellation is performed before taking separate upper bounds or optional
expectations. For example, if a nonnegative finite-almost-sure random baseline Z
has infinite mean, costs Z+1 and Z still have pointwise difference -1. Expected
*difference* is well defined, while subtracting their two infinite expected costs
is not. The selected core makes the pointwise comparison; it does not introduce
an infinity-minus-infinity operation or claim a finite expected-risk interpretation
for an internally nonintegrable program. The same shared-baseline identity must
be justified before using this argument.

The conditional source mathematics does not impose complete preferences or a
uniquely correct utility function. It supplies scoped comparisons that a consumer
may use alongside other requirements. All new refinement and self-report results
remain relative to their declared source and execution models.

### Scope review of the final comparisons

The source-data simplifications above preserve conditional **numerical** meaning.
A future implementation must still bind them to the same observation interface,
registered programs and evidence scope. The policy examples bind actions before
unknown source values are interpreted. The conditional-report examples bind each
reported probability to the program behavior that emitted it. The loss adapters
bind approximation error to a component function rather than assuming the desired
final comparison. The update examples either retain the needed relation or exhibit
exactly the query family for which a smaller summary suffices.

These four bindings are mutually consistent in the three principal models and the
new finite visible-policy elaboration. They require no access by the program to
hidden p,s,theta or evaluator correctness. Their mathematical witnesses are inputs
to a semantic audit, not observations magically made available to the deployed
policy. This is the operational distinction the finalized F05 specification
must preserve when F06 introduces syntactic inference.

A final geometric check on the comparison-error metric is

    inf_c max_a |e_a-c| = span(e)/2.

For any c, the distances to the largest and smallest entries have maximum at
least half their separation; their midpoint attains equality. Thus the span
bound can equivalently certify closeness *up to one common offset*. That offset
may depend on the hidden model and need not be known or computed by the agent.
The inference concerns the observable cost contrasts; it does not authorize
subtracting a different unknown offset from each action or claiming absolute
calibration. This closes the connection between relative numerical sufficiency
and the unbounded-baseline motivation without assuming recoverable absolute value.
