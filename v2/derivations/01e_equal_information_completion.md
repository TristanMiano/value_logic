# F04 S6 — equal-information reconstruction and candidate disposition

Date: September 26, 2026, UTC. Base: `50f2400267818a48ff0e4eca5d619f7bf9c2d136`.
Scope: complete the *candidate-discrimination task*, not select the core or pass
Gate A. This note reconstructs a common finite fragment before deciding what the
previous counterexamples actually discriminate. A candidate's ability to name an
optimization is not a proof-search algorithm or evidence of learned reasoning.

Prior objects and limits are in [S1](01_candidate_countermodels.md),
[S3](01b_compressed_revision_certificates.md),
[S4](01c_certificate_portfolios.md), and
[S5](01d_source_transport_and_identifiability.md).

## 1. One operational question, the same evidence for both routes

A **plan** here is a fixed available computation or policy, not a choice that may
silently depend on an unobserved model. A **context** fixes the loss/proxy,
resource units, allowed input/domain, source meanings, evaluator versions and
any admissible randomization. Change any of these and a reuse theorem needs an
explicit bridge. The comparisons below are conditional on the supplied evidence,
not assertions that the evidence or loss is metaphysically privileged.

Let the evidence be a finite nonempty family of nonempty polyhedra

    Gamma_k = {x in R^n : A_k x <= eta_k},  k in K.

A coordinate of x is a shared unknown, not an independently resampled variable
at every occurrence. A mode k may remain unknown. Retain a feasible witness for
each admitted mode; it prevents an inconsistent set of premises from being
mistaken for an actionable guarantee. Impossible modes may be removed only with
an explicit contradiction witness; removing every mode leaves no deployment
warrant in this operational interpretation.

Within this comparison fragment, a fixed plan p has a finite-valued affine
loss proxy

    L_p(x) = c_p + w_p^T x.

The family of values may be unbounded in either direction; pointwise arithmetic
uses finite reals. Nonnegative losses can instead be stipulated on Gamma. No
universal magnitude cap, privileged probability distribution or exact utility is
required. This fragment does not cover arbitrary nonlinear losses by fiat.

For the proposed replacement p -> q write

    d(x) = L_q(x) - L_p(x) = c + v^T x.

The operational question is: can the *same available q* replace p with loss
increase at most b on every admitted mode and source assignment? A negative b
certifies uniform improvement. The signed comparison should not be confused with
a nonnegative confidence level or statistical error probability.

Two routes receive precisely Gamma_k, c, v and b:

**A, proof-carrying arithmetic.** For each mode supply nonnegative multipliers
lambda_k with

    A_k^T lambda_k = v,
    c + lambda_k^T eta_k <= b.                         (A)

The product is a small arithmetic certificate, plus its source, scope and mode
identities. Signed finite expressions can be translated using the guarded
nonnegative-pair adapter from F03. This is an RLL-*like comparison fragment*, not
the claim that the existing small checker implements every RLL rule.

**B, lower-value evaluation.** Form the gain L_p-L_q and evaluate

    lower_gain(p,q) = inf_(k,x in Gamma_k) (L_p(x)-L_q(x)).  (B)

Accept an improvement margin m when lower_gain >= m. Equivalently define the
upper deterioration U(c,v)=sup_(k,x in Gamma_k) (c+v^T x) and ask U<=b.
This is the scoped lower-value/desirable-difference route, not an assertion that
all versions of strict desirability accept a zero gamble.

Route B must retain the *shared family* or an adequate representation of it.
Replacing it by unrelated marginal extrema is a change of semantics, not an
implementation of the same query. Conversely, route A must not receive hidden
joint premises unavailable to B.

## 2. C40 — exact agreement on the finite affine comparison fragment

### Statement

Under section 1's assumptions, a finite b bounds d on all admitted models iff
certificates (A) exist for every mode. The strongest common numerical bound, when
finite, is

    U(c,v) = max_k min_{lambda>=0, A_k^T lambda=v}
                         (c + lambda^T eta_k).         (1)

A mode with unbounded-above query has no finite certificate. A feasible mode
whose query is bounded above has a tight certificate. Different modes may use
different lambda, but they all certify the same q, p and b.

This is a finite-linear consequence/duality reconstruction, not a novelty claim.
It restates the precise overlap that the two candidate routes must respect.

### Direct proof of the certificate direction

For any x in Gamma_k, nonnegativity gives

    v^T x = lambda_k^T A_k x <= lambda_k^T eta_k.

Add c and use the final inequality in (A). Every admitted mode is covered, so
one operational guarantee follows. No independence assumption enters this step.

### Fresh finite-cone proof of the converse

Fix one mode and put t=b-c. In R^(n+1) form the finitely generated cone

    C = cone({(a_i,eta_i): source rows i} union {(0,1)}).

Membership (v,t) in C says exactly that there are lambda>=0 and s>=0 with
v=A^T lambda and t=lambda^T eta+s, which is (A).

For clarity, the closed-cone fact needed here can be verified in finite dimension.
Every conic combination can be reduced to an independent support: if its active
generators are dependent, choose a nonzero coefficient dependence, orient it to
have a positive coordinate, and subtract the largest feasible multiple until an
active coefficient becomes zero. Iterate. For a convergent sequence in C, take
a subsequence with the same independent support (there are finitely many such
supports). The inverse linear map on that support is continuous; its nonnegative
coefficients converge to nonnegative coefficients. The limit is in C. Thus C is
closed, as well as convex.

If z=(v,t) is outside C, let p be a nearest point in C and h=p-z. A nearest point
exists because the distance minimization can be restricted to a closed bounded
ball. The projection inequality gives h^T(y-p)>=0 for y in C. Since C is a cone,
testing y=0 and y=2p gives h^T p=0. Hence

    h^T y >= 0 for y in C,       h^T z = -||h||^2 < 0.

Write h=(u,s). The generator (0,1) gives s>=0 and each source row gives

    a_i^T u + eta_i s >= 0,
    v^T u + t s < 0.                                  (2)

If s>0, x=-u/s satisfies A x<=eta while v^T x>t. It is a countermodel to the
alleged consequence.

If s=0, use the required feasible x_0. Equations (2) imply A u>=0 and v^T u<0.
All x_T=x_0-Tu, T>=0, remain feasible, while v^T x_T tends to +infinity. Again the
bound fails. This is the exact point where nonempty evidence is used.

Consequently, validity of v^T x<=t forces membership in C and supplies a
certificate. If the supremum h=sup_Gamma v^T x is finite, the inequality v^T x<=h
is valid; applying the same argument at t=h supplies a tight certificate.
Repeating this for finitely many nonempty modes proves (1). The proof does not
confuse an unbounded feasible source set with an unbounded *particular query*.

### What this does and does not discriminate

On this fragment, neither route can validly claim a stronger exact numerical
answer while using the same source information. Differences are in representation,
certificate production/checking, source updates, supported operations and cost.
A source-indexed lower evaluator can call a certificate-producing linear solver;
a proof-carrying front end can use a lower evaluator to suggest useful goals.
These are implementation possibilities, not a proof that the two full systems
have identical languages or computational costs.

Full RLL affine consequence includes piecewise operations and is not reduced
here to just checking one supplied linear multiplier vector. RLL's broader
complexity statements cannot be read as the complexity of verifying (A).

### Signed improvement versus nonnegative residual

For a fixed threshold b, d<=b iff ReLU(d-b)=0. This supplies an explicit
nonnegative residual query without calling its magnitude a truth degree.
A *single unshifted* residual loses improvement information: d=-1/2 and d=0 both
produce ReLU(d)=0. A family of thresholded residual queries can distinguish them;
the threshold and units belong to the query. We should not discard the signed
comparison and later infer an improvement margin from an unshifted zero alone.

## 3. C41 — when reducing components separately loses nothing

For a nonempty source set Gamma and finite affine differences d_1,...,d_m, define

    U_joint = sup_x sum_j d_j(x),
    U_separate = sum_j sup_x d_j(x).

When the displayed individual suprema are finite, U_joint<=U_separate. The right
side permits each occurrence of x to be chosen independently at its worst value;
it is a valid upper bound, not automatically the original coupled semantics.

Assume the individual and joint maxima are attained. This holds, in particular,
for compact Gamma, or the nonempty finite-union polyhedral setting when these
linear query maxima are finite. Then

    U_joint = U_separate
    iff intersection_j Argmax_Gamma d_j is nonempty.   (3)

Indeed, a common maximizer attains every summand. Conversely take a joint
maximizer x*. Each slack sup d_j-d_j(x*) is nonnegative. Equality of the sums
forces every slack to be zero. This proves both directions. Without attainment,
replace a common exact maximizer by a sequence simultaneously approaching every
supremum; equality alone need not produce an attained witness.

This identifies precisely one limitation of early scalarization. A scalar
summary is fine for its already-reduced query, but it need not support tight
composition. The original transformer candidate is not disqualified: it can
keep x as a shared state parameter or retain an adequate relation. It is the
independent lower/upper reduction before composition that loses information.

### Two-stage hand reconstruction with genuinely nonnegative, unbounded losses

Let theta in [0,1] and z>=0. The old and new stage losses are

    old_1 = 2+z,          new_1 = 5/4+z+theta,
    old_2 = 2+z,          new_2 = 9/4+z-theta.

Every loss is nonnegative; the family is unbounded above. The proposed new
composite is fixed and uses both new stages. Its differences are

    d_1 = theta-3/4,      d_2 = 1/4-theta.

Each separate worst-case bound is +1/4, but the coupled sum is exactly -1/2.
The first maximum requires theta=1; the second requires theta=0. Equation (3)
explains the strict gap. Neither z nor a complete absolute-loss estimate is
needed for the paired comparison.

Route A preserves the signed expressions and cancels theta before reducing the
combined goal. Its resulting source multiplier is zero for the constant -1/2
query; the source identity is still essential to justify that cancellation.
Route B composes the two source-indexed maps first, then takes the upper envelope,
obtaining the same -1/2. Independently reducing either representation first gives
+1/2 and loses the improvement. Adding already-truncated nonnegative residuals
also loses it. The example distinguishes order of operations, not brand names.

As a positive control, take d_1=theta-3/4 and d_2=theta-1/4. Both attain their
maximum at theta=1, and both evaluation orders give 1. If stage two legitimately
uses an independent new source phi in [0,1], the original opposite-slope example
has joint worst case +1/2. One cannot retain the sharper -1/2 by pretending that
two separately uncertain sources are equal.

## 4. C42 — equality of current affine observations need not survive evidence

Let

    K = {(0,0),(1,0),(0,1)},        H = convex_hull(K).

Every affine query has the same supremum over K and H: an affine value at a
convex combination is the same combination of vertex values and cannot exceed
the largest one. Thus even a complete oracle for current affine upper values
cannot distinguish these two evidence models.

Now add the *same* admissible source relation E={x:y=x}. Both restrictions are
nonempty, but

    K intersect E = {(0,0)},
    H intersect E = {(t,t): 0<=t<=1/2}.

The query x+y has revised upper value 0 in the first model and 1 in the second.
The distinction is not caused by inconsistent evidence or an oracle-informed
choice of action. It is caused by convexification before a contextual update.

Both routes face the same boundary. Route A must retain the disjunctive modes
(or an adequate update-aware abstraction) rather than blindly conjoin their
convex-hull inequalities. Route B must retain enough structure beyond current
affine evaluations when this update is allowed. A current-value equivalence is
not automatically a congruence for every future operation.

A useful positive case is retained: if E contains all of K, it contains H when
E is convex, and nothing changes; more generally exactness for an allowed E
requires comparing convex_hull(K intersect E) with H intersect E for the declared
linear observations. This is a criterion to check, not a blanket requirement to
store every original observation forever. S3 and F03 already develop related
update-sensitive counterexamples; this construction aligns them with the two
routes now being compared.

## 5. C43 — a real closure difference, with a quantitative repair

It would be misleading to present the two dual descriptions in section 2 as
two different numerical answers. To distinguish the broader routes, specify an
operation that belongs naturally to the transformer candidate rather than just
changing the name of the certificate.

### A source-preserving finite continuation operator

For a finite observable state space S, let e have immediate cost c_e(theta,s)
and transition kernel K_e(theta,s,s'). A cost continuation h retains the same
hidden parameter theta. Define

    (T_e h)(theta,s)
      = c_e(theta,s) + sum_{s'} K_e(theta,s,s') h(theta,s').   (4)

The policy chooses from its allowed observations; indexing the mathematical
semantics by theta does not grant the policy access to theta. For two fixed
stages use T_e(T_f h), preserving the source identity. An outer supremum over
admitted theta then evaluates the complete policy. Unless a suitable uncertainty
pasting condition holds, taking unrelated inner suprema at each stage can give
a conservative relaxation rather than this exact evaluation. Section 3 already
exhibits that failure with a one-state, two-stage additive example.

This operator formulation is materially different in its native objects and
composition interface from an affine certificate language, even though they
agree on the affine comparison subfragment. Equation (4) supplies semantics;
it is not an unrestricted algorithm for performing every resulting optimization.

### A same-information nonlinear closure witness

Let theta in [0,1]. Stage one produces Y=1 with probability theta and Y=0 with
probability 1-theta. The downstream cost is h(theta,1)=theta and h(theta,0)=0.
Then the exact composite expected cost is

    (T h)(theta) = theta*theta + (1-theta)*0 = theta^2.     (5)

Only the specified one-step random experiment and its conditional costs are
used. The repeated theta is a fixed shared parameter, not a claim of independence
between uncertain parameters. Add any common finite z>=0 to both competing
plans to keep absolute cost unbounded without changing the approximation issue.

A finite affine/ReLU expression is continuous piecewise affine in theta. It
cannot equal theta^2 on all of [0,1]. Any finite affine partition contains an
interval [a,b] with a<b on which the expression is affine. Its midpoint value
is the mean of its endpoint values, whereas

    (a^2+b^2)/2 - ((a+b)/2)^2 = (b-a)^2/4 > 0.

Thus exact equality on that interval is impossible. This is a closure obstruction
for the **restricted affine/ReLU route**, not for full RLL, which includes
multiplication, nor for every possible certificate representation.

This also does not mean that the affine route cannot prove useful *inequalities*
about theta^2. With a suitable multiplication/interval rule it can prove, for
example, theta^2<=theta on this domain. The obstruction is to representing the
exact whole return function with a fixed finite piecewise-affine expression.

### Sharp conservative affine repair on a declared tolerance

Partition [0,1] into k intervals of length 1/k. On [a,b] the chord

    C(theta) = (a+b)theta - ab

satisfies the exact identity

    C(theta) - theta^2 = (theta-a)(b-theta).

Hence the continuous piecewise-affine chord function C_k is an upper bound with

    0 <= C_k(theta)-theta^2 <= 1/(4k^2).                 (6)

For uniform knots it has an explicit ReLU expression

    C_k(theta) = theta/k
                  + (2/k) sum_{j=1}^{k-1} ReLU(theta-j/k),
                  for theta in [0,1].                  (7)

To verify (7), the initial slope is 1/k, and each knot raises the slope by 2/k;
on the j-th interval the slope is (2j+1)/k, exactly its chord slope. The value at
zero and continuity fix all intercepts.

The conservative error in (6) is minimax-sharp among piecewise-affine upper
bounds with at most k intervals. One interval must have length at least 1/k.
Let an affine upper bound on [a,b] have endpoint excesses e_a,e_b>=0. At the
midpoint its excess is

    (e_a+e_b)/2 + (b-a)^2/4 >= (b-a)^2/4.

So its uniform excess is at least 1/(4k^2). Equal-width chords attain this. This
is a bound on *number of affine intervals*, not a neuron-count lower bound for
an arbitrary deep network. Do not confuse representation accuracy with the
strength of one isolated bound query.

At k=4 the envelope error is at most 1/64. A certified affine comparison using
C_4 can spend this explicit uncertainty budget; it does not pretend to have
computed the exact nonlinear cost. A transformer representation retaining the
polynomial can keep (5) exact on this example, but general polynomial source
optimization is an additional problem, not free from the function notation.

### Candidate consequences

The surviving alternatives are now precise:

* A: source-indexed arithmetic expressions, regional affine certificates, and
  explicit approximation budgets; extend to multiplication only by an admitted
  rule/semantic fragment.
* B: source-preserving finite continuation operators / desirable differences,
  with explicit operational state, information and uncertainty. It can generate
  nonlinear value functions even from simple input pieces; proof certificates
  or certified optimization must still be supplied for actual conclusions.

A hybrid can use B for semantics and A for checkable approximations. That is an
option for Gate A, not a decision taken by F04. A simpler restricted arithmetic
core is attractive only if its approximation budget leaves useful conclusions
on the intended demonstrations. The nonlinear case is a test of that condition.

## 6. C44 — reconstruct the reflective fragment and an end-to-end warrant

Use a *versioned controller* whose report r in [0,1] sets the probability of
choosing its second branch. The branch failure probabilities p,s are uncertain
but lie in [0,1]. The failure expectation is

    H_(p,s)(r) = (1-r)p + r s.

Thus the report concerns the very behavior it helps determine. It is not merely
an unrelated prediction supplied with a SELF label. An upper report is valid
when r>=H_(p,s)(r) for all retained models, equivalently

    p <= r(1+p-s).                                     (8)

When 1+p-s>0 the required threshold is p/(1+p-s). The exceptional case p=0,s=1
has zero denominator and H(r)=r, so every r is valid; it contributes threshold
zero, not a division-by-zero computation. The intersection of all valid-report
intervals is [t,1], where t is the supremum of these thresholds. Report 1 is
always feasible, though often uninformative and not necessarily useful.

If (p,s) ranges over a finite convex hull, the threshold equals the largest
vertex threshold. To verify this, p and 1+p-s are affine in the convex weights.
Terms with zero denominator have p=0 and contribute nothing. The ratio for a
positive-denominator mixture is a denominator-weighted average of the vertex
ratios; it cannot exceed their maximum. Conversely each vertex is admitted.
This supplies a finite constructive report-validity calculation. It is not
unrestricted proof reflection, and no statement says the uncertain probabilities
are calibrated merely because the algebra is correct.

For a fixed known branch-use cost kappa, the expected task cost is

    J_(p,s)(r) = z + p + (s-p+kappa)r,

where z is an arbitrary common finite baseline. A change r0->r1 has paired cost

    J(r1)-J(r0) = (r1-r0)(s-p+kappa).                   (9)

A report can be selected by an ordinary algorithm and then substituted as a
fixed number in the affine certificate. Treating r as an additional unknown
symbol makes (8) bilinear; the purely affine fragment does not silently gain
that operation. A parameterized theorem about all r is a metatheorem or requires
a larger object language. This is an important limit for the preferred route.

### Nontrivial two-fallible-branch instance

Let theta in [0,1], p=1/2+theta/4, s=theta/4, kappa=1/4. Both branches are fallible
at theta=1. Their difference s-p=-1/2 is known despite the unknown theta. Now

    H_theta(r)=1/2+theta/4-r/2,
    t = (3/4)/(3/2)=1/2.

Both r0=1/2 and r1=3/4 are common valid reports. Their paired cost change is

    (3/4-1/2)(-1/2+1/4) = -1/16.

The actual failure of the new policy lies in [1/8,3/8], below its report 3/4.
The report is deliberately an upper bound, not necessarily an exact prediction
or the least valid report. The old policy's failure lies in [1/4,1/2]. Increasing
the numerical report here makes the bound looser while improving actual expected
cost: report quality and policy quality remain distinct.

Both A and B obtain these conclusions from the same p,s relations and versioned
controller. A checks (8) at the proposed reports and (9) using source rows; B
evaluates the fixed report-dependent policy over the same parameter family.
Neither is permitted to select a different hidden-world report without an
observation policy that makes it available.

### Common proof witnesses versus available policy witnesses

For finitely many model cases k and a finite observation map o(k), suppose the
admissible report set at case k is F_k. An observation-respecting report policy
exists iff

    intersection_{k:o(k)=y} F_k is nonempty

for every reachable observation y. Necessity follows because one report pi(y)
must work for all cases with that observation. Sufficiency follows by choosing
one element of each nonempty finite family intersection. This is elementary
uniformization, not a new reflection theorem.

In the upper-report model F_k=[t_k,1], so the intersection is [max t_k,1]. Extra
paired-cost or resource requirements may shrink F_k, and then an empty
intersection is a genuine operational obstruction. For example F_1={0},F_2={1}
are separately satisfiable but not under a single uninformative observation.
Proof certificates lambda_k can still vary by case: they are justification
witnesses for one statement, not the action selected by the agent.

### Comparison is useful before absolute adequacy is known

Return to section 3's two-stage proxy comparison, whose change is exactly -1/2.
Let the intended task loss be L_p+E_p, where E denotes the difference between
proxy and intended criterion. Assume the paired alignment premise

    E_new(x)-E_old(x) <= 1/8

on the same admitted models. Then the intended-loss change is at most

    -1/2 + 1/8 = -3/8.                                (10)

The absolute discrepancies may be unbounded; the paired relation is enough.
If that premise is absent, choose E_new-E_old=1 to reverse the conclusion.
If the criterion, weights or source alignment changes, the old relation cannot
be reused without another bridge.

Equation (10) justifies improvement over the named old plan. It does not justify
an absolute target tolerance when the common baseline z is unbounded. A separate
old-plan bound U0 would yield a new-plan bound U0-3/8 by composition. This recovers
phase one's useful distinction between fallback improvement and absolute
adequacy rather than collapsing every favorable number to a generic license.

A probabilistic source certificate adds its own sampling-law premise. Simultaneous
validity of the source and alignment premises gives simultaneous validity of the
deduced bound. Two merely marginal confidence statements need an appropriate
joint coverage argument (a union bound is one conservative option). The arithmetic
proof neither creates such coverage nor equates its failure probability with
3/8 cost units. Earlier F04 selection counterexamples remain in force.

## 7. A boundary that matters for both neural and symbolic representations

### Varying the query is not the fixed-query portfolio theorem

S4's finite-portfolio characterization fixed A and the queried vector v while
varying the source bounds eta. Do not read it as a statement about one finite
ReLU network simultaneously computing every exact bound for every query vector.

Even in one dimension, let

    Gamma_eta = {x: 0<=x<=eta},   eta in [0,1],
    query = v*x,                v in [0,1].

The exact upper value is

    U(eta,v)=v*eta.

Restricted to the diagonal eta=v=theta this is theta^2; section 5 rules out an
exact finite piecewise-affine representation on the whole square. Each fixed-v
slice is nevertheless affine in eta. Thus *every individual slice is ReLU
representable* does not imply *one finite ReLU represents the whole joint map*.

There is a positive certificate representation: retain the source x<=eta and
propose its multiplier lambda=v. The coefficient itself is a simple affine/ReLU
function on this domain and satisfies the query coefficient identity exactly.
The checker evaluates lambda*eta to obtain the numerical bound. The product
occurs in the evaluator, not magically in a finite affine output map. The second
source -x<=0 can have multiplier zero. This is not an asymptotic speed theorem,
but it separates what must be represented from what is computed after decoding.

For a neural study, outputs, coefficient proposals, retained source quantities
and the arithmetic evaluator must be distinguished. Observing a useful internal
coefficient would not require finding a neuron whose activation equals the
entire final cost. Conversely, a correct numerical output need not identify a
unique coefficient or a causal derivation; S5's nonidentifiability cases remain.

### A representation obstruction need not obstruct the requested decision

For the two-step cost theta^2, compare against the old cost theta on
[1/4,3/4]. The exact worst-case change is -3/16. Although C_4 is not theta^2,
its four-interval chord enclosure satisfies

    sup_{theta in [1/4,3/4]} (C_4(theta)-theta) = -3/16.

This follows by checking the affine differences at the relevant knots 1/4,
1/2,3/4: the values are -3/16,-1/4,-3/16. Thus the finite approximate
representation answers this particular worst-case question *exactly*.

The two-interval chord C_2 instead yields -1/8 on this restricted domain: the
endpoints 1/4,3/4 are not its knots. It remains a useful improvement certificate,
but it does not meet the stronger requested margin 3/16. This is a concrete
precision-versus-task comparison, not a preference for maximal detail everywhere.

The polynomial identity

    theta^2-theta+3/16 = (theta-1/4)(theta-3/4) <= 0

also proves the same bound directly on the stated interval. A full arithmetic
route admitting multiplication could use that short proof without approximating
the entire value function. In contrast a minimal affine route needs the nonlinear
interval fact as an explicitly verified premise, not as a rule it never supplied.

### Avoiding a vacuous neural interpretation

For any finite scalar computation F(z), the invented source premise g<=F(z)
would make F a trivial certified upper bound on g. This says nothing about the
network's task or mechanisms. The empirical source semantics, queried quantity
and permitted source transformations must therefore be obtained independently
of the held-out evaluation; exploratory alignment can be developed on training
or development data and then frozen before that evaluation.

Two already-proposed neural hypotheses should remain distinct:

1. hidden action-cost variables in the ordinary weighted-label learner predict
   donor/base interventions; and
2. a declared scalar subcomputation or coefficient proposal admits useful,
   source-grounded numerical certificates on a stated domain.

Neither implies the other. The classifier's logit or probability is not an
upper-bound output just because a different proof-selection function can be
represented by ReLUs. The normal-training baseline must not be given hidden
logical labels, certificate regularizers, or a special architecture that inserts
the hoped-for result. No ordinary network was trained in F04.

## 8. Final same-information discrimination matrix

The purpose of this table is to finish F04, not to perform Gate A. The aliases
refer to the explicit A/B constructions above; the original S/P/T/G formulations
remain available through their F02 definitions.

| Operational question | A: source-aware arithmetic/certificates | B: source-preserving lower-value/continuation maps | Actual discriminator |
|---|---|---|---|
| Fixed affine paired loss, nonempty finite polyhedral modes | Tight modewise multiplier certificates exist when finite | Same exact upper/lower value | Exact answers coincide by C40; compare production/checking/storage costs, not unequal data |
| Shared unbounded baseline | Cancellation before bounding; free-source guard is explicit | Difference evaluated on the same source before extrema | Separate absolute extrema or independent copies can lose the useful answer |
| Additive stages | Preserve expressions and combine/reoptimize their certificate | Compose theta-indexed operators before reducing | C41 identifies when separate reductions happen to be tight |
| Stochastic sequential composition | Minimal affine/ReLU fragment is not exactly closed; retain an enclosure or explicitly extend it | Native composition can produce theta^2 | C43 proves closure loss and a sharp conservative piecewise-affine repair |
| Changing the query and evidence together | Coefficient proposals can be simpler than the final numerical bound | Joint value map can be nonlinear | Fixed-query CPWL results cannot be reused as joint-query representability |
| New hard evidence | Preserve disjunctive modes/context or use a certified relaxation | Current lower affine values alone may not support exact updating | C42; both routes need update-relevant information |
| Correlated reflective policy with fixed report | Check the report inequality and paired change under declared source/evaluator | Evaluate the same report-dependent kernel family | Both support the finite two-fallible-branch fragment; unknown-model optimizers are not deployable |
| Symbolic report parameter and self-reference | Bilinear terms require a broader object language or a fixed-report theorem family | Feedback fixed-point constraints still need an existence/selection semantics | No unrestricted reflection theorem is claimed by either route |
| Proxy-to-task bridge | Explicit paired-alignment premise plus arithmetic consequence | Same premise in the gain family | Neither can infer alignment from lower proxy loss alone |
| Neural interpretation | Check coefficients/regions with independent source and scope data | Test retained source/value transitions under actual interventions | Mathematical validity is not causal use or learned emergence |

The scalar S baseline remains useful for a fixed answered query and tolerance,
but is inadequate as the unrestricted composition/update carrier. The guarantee
front G remains useful for attainable joint budgets and policy witnesses, but
it cannot recover hidden correlation once reduced to unrelated marginal bounds.
These are scoped findings, not declarations that all scalars or fronts are
universally inadequate. P and T continue to provide genuinely different native
expression/continuation organizations. Dualizing their affine overlap is not
by itself a new calculus.

## 9. Reconstructed failures and positive alternatives

This section records a fresh mathematical check against the original obligations.
It is same-agent self-review, not independent verification.

**Proxy ranking.** At label probability 3/5, prediction 1 has Brier loss 2/5
and classification error 2/5. Prediction 49/100 has Brier loss 2521/10000 and
classification error 3/5. The intended error increases by 1/5 despite proxy
improvement 1479/10000. The excess-risk bound compares each predictor with its
Bayes optimum and does not imply pairwise ordering. C44's paired-alignment
premise repairs the desired *kind* of inference without denying this witness.

**Common uncertainty.** In the original source pair
3+z+epsilon/4 and 1+z-epsilon/4, subtracting gives -2-epsilon/2. The uncontrolled
z cancels only because it is shared and its multiplicity is equal. With unrelated
z_new,z_old the difference is unbounded, and using the new component twice leaves
one uncancelled z. The final two-stage example retains this discipline and tests
composition rather than another change of notation.

**Self-reference.** Reconstruct (8) directly from branch probabilities, including
the p=0,s=1 corner. Verify both common reports and the actual failure range in
C44. A lower or exact self-report is not its own evidence; r=1 feasibility alone
is not useful adequacy. Distinguish fixed-point existence, uniqueness, convergence,
report validity, utility and available observation policies. Earlier contrary
examples stay active regressions.

**Certificate directions.** The finite-cone separator gives x=-u/s, not u/s.
Its s=0 case uses x0-Tu, not x0+Tu. In the domain-lift reconstruction from S5,
stacking source A g-B z<=eta0 and domain D z<=d gives

    A^T lambda=v,
    B^T lambda-D^T nu=alpha,
    eta0^T lambda+d^T nu<=c.

The minus sign before D^T nu is essential. Nonempty joint evidence/domain data
is also essential to an operational conclusion. Regional certificate validity
can accommodate negative observed slopes; it does not make an arbitrary
negative source multiplier admissible.

**Neural controls.** Positive hidden-unit rescaling and permutation preserve the
function when outgoing weights and intervention coordinates are transported.
An unused duplicate can be perfectly decodable without causal effect. At a kink,
separately assembled partial derivatives can fail to be one coherent affine
piece. Even a valid piece certificate can have many lifts on a constrained input
manifold. None of these obstructions is removed by naming activations 'values'.
The prospective experiment keeps function-preserving gauges, donor controls,
held-out evaluation and ordinary training distinct from a hand-compiled example.

**Attainment and emptiness.** Nonempty polyhedral source sets with finite linear
support attain the support: projecting the polyhedron onto the objective axis
by finite linear elimination gives a closed one-dimensional polyhedron with a
finite included endpoint. This does not generalize to arbitrary nonclosed source
sets. In the absence of attainment, equality in C41 gives a simultaneous
approximation sequence, not a common exact maximizer. Inconsistent premises can
formally entail arbitrary bounds but do not produce an operationally available
solution under our candidate comparison convention.

No contradiction requiring retraction of a completed phase-one/F03 result was
found in this pass. The new comparisons explicitly preserve the earlier scope
restrictions; they do not turn a test count into a whole-calculus theorem.

## 10. F04 disposition for the next review

The task now has far more than two invalid-inference witnesses, their positive
restricted alternatives, and same-information discrimination across its viable
routes. DIR01's proxy, feedback-sensitive self-evaluation and prospective neural
requirements have concrete artifacts. Completion also depends on the recorded
remaining derivation floor and validation, which are adjudicated in the session
record rather than presumed from this note's existence.

**Recommendation for Gate A to assess:** pursue a source-aware loss-comparison
language with small checked arithmetic certificates as the first implementation
candidate, while retaining source-preserving continuation semantics as the
explicit alternative/reference. Require a nonvacuous paired-improvement result,
a feasible reflective policy witness and an uncertainty budget for non-affine
composition. Do not count the finite-linear duality alone as a new contribution.

The most threatening assumption is that the chosen source variables and their
joint constraints actually express the task-relevant dependencies. Certifying
consequences of post-hoc or inaccurate source semantics is not interpretability
or empirical adequacy. A second threat is restricting the object language until
all interesting composition or self-evaluation is done by an external oracle.
The bounded next question should expose, rather than hide, those boundaries.

A proposed bounded development question is: can a small source-indexed language
express a complete paired replacement argument, transport its certificate through
one declared evidence change, and evaluate a fixed report-dependent policy while
showing exactly which arithmetic and semantic premises it uses? Gate A decides
whether that is the right scope for F05. Neither Gate A nor F05 is performed here.

## 11. Fully explicit shared-source certificate for the reflective replacement

To ensure the proposed arithmetic route is not just an optimizer with a new name,
write the entire C44 example as source rows. Use x=(p,s,e), with one unit of cost
per failure. The third coordinate is the *difference* between intended and proxy
loss errors for the two proposed policies, not a failure probability. Let

    A = [ 1 -1  0 ]     eta = [  1/2 ]
        [-1  1  0 ]           [ -1/2 ]
        [ 0  1  0 ]           [  1/4 ]
        [ 0 -1  0 ]           [    0 ]
        [ 0  0  1 ]           [ 1/32 ].

Thus p-s=1/2, 0<=s<=1/4, and e<=1/32. In particular both probabilities lie in
[0,1]. The evidence set is nonempty and is unbounded below in e. An arbitrary
common finite cost baseline z need not be stored in A because it cancels from
all the queried differences. Absolute error baselines may also be unbounded.
The source packet still records what e and the eliminated baseline mean.

### Report validity, with explicit nonnegative multipliers

For a fixed r, the report shortfall is

    H(r)-r = (1-r)p + rs - r.

Choose lambda=(1-r,0,1,0,0). For r in [0,1] this is nonnegative, and

    A^T lambda=(1-r,r,0),
    -r+lambda^T eta = 3/4-3r/2.

At r0=1/2 the bound is zero; at r1=3/4 it is -3/8. The point p=3/4,s=1/4 attains
both, so these are tight bounds, not just accepted inequality manipulations.
The uncertainty in e is irrelevant to report validity and receives zero weight.

### Intended paired cost, rather than report quality

With branch-use cost kappa=1/4 and displacement r1-r0=1/4, the intended-loss
change is

    d(x)=1/16 -(1/4)p +(1/4)s + e.

Its certificate is lambda=(0,1/4,0,0,1). The coefficient identity is exact and

    1/16+lambda^T eta
      = 1/16-1/8+1/32 = -1/32.                         (11)

A feasible point with e=1/32 attains the bound. Route B's direct lower-value
evaluation obtains the same guaranteed improvement 1/32. The proxy alone improves
by 1/16; the explicitly budgeted proxy discrepancy reduces, rather than invents,
the intended-value conclusion. For e=1/8 instead, the intended change is +1/16;
omitting the alignment premise would permit reversal.

No part of this argument infers source validity from the controller's own report.
The report, branch model, intended criterion and evidence verifier are separate
versioned objects. This is a complete *conditional example*, not an unqualified
claim about every evaluator capable of describing itself.

### Selective evidence revision with an exact loss margin

Now weaken the second bound to -1/2+delta and the fifth to 1/32+epsilon, where
0<=delta<=1/2 and epsilon>=0. Keep the other source rows and their interpretations.
Probability constraints remain valid: p>=s+1/2-delta>=0 and p<=s+1/2<=3/4.
The old feasible points remain available, so feasibility is not assumed without
a witness. The old common reports remain valid because their certificates use
rows one and three, which did not change.

The same paired-cost certificate gives

    d <= -1/32 + delta/4 + epsilon.                    (12)

This bound is tight: choose s=0, p=1/2-delta and e=1/32+epsilon. Therefore the
fixed replacement remains uniformly non-worsening exactly when

    delta/4 + epsilon <= 1/32,

within this revised model family. For a requested improvement m>=0, require
m+delta/4+epsilon<=1/32. At delta=1/8,epsilon=0 the old improvement margin is
exhausted and zero is attained. At delta=1/4,epsilon=0 deterioration 1/32 is
actually possible; no alternative proof can recover non-worsening from these
same premises because the displayed countermodel is feasible.

This example connects report validity, proxy alignment, loss-grounded comparison,
nonnegative arithmetic proof weights and selective revision in one packet. The
scope and update rules are doing real work: unchanged report validity does not
mean the value of deploying the new policy is unchanged. It also gives a direct
counterpart to phase one's distinction between dependency-local status stability
and substantive task adequacy.

## 12. Final reconstruction qualifications

1. The theta^2 continuation can be realized by two Bernoulli trials with common
   fixed parameter theta and conditional independence of their random draws:
   charge a unit cost only if both succeed. Shared *parameter* identity and
   conditional independence of the *draws* are different assumptions. The latter
   is required for this physical realization; equation (5) already stipulates
   the relevant conditional kernel.
2. A bounded return-function approximation is neither necessary nor sufficient
   by itself for every operational claim. Sections 5 and 7 give a precision
   bound and a decision-specific positive control. The criteria involve the
   intended query, retained source meaning, and tolerance together.
3. The finite-cone certificate verifies implications of the declared source
   rows, not the sampling process that supplied them. Declaring a nonempty
   mathematical model and establishing empirical source adequacy are different.
4. Finite tests below check exact examples, malformed certificates and boundary
   calculations. The cone proof, nonlinear closure obstruction and interpolation
   lower bound are analytical statements, not conclusions extrapolated from a
   test grid. Completion of F04 does not constitute their independent review.
5. The final candidate comparison keeps the competing representations alive.
   Exact agreement in one fragment, strict closure differences in another and
   shared update failures are evidence for Gate A. They do not silently install
   a final syntax, permanent architecture or general reflection principle.

## 13. C45 — exact self-report optimization has a fragile corner

The post-fixture reconstruction exposes a substantive condition on the smallest
reflective fragment. Define the least exact upper report for one model by

    t(p,s)=p/(1+p-s)  if 1+p-s>0, and t(0,1)=0.

At (p,s)=(0,1), every r is self-consistent and the least report is zero. At
(p,s)=(epsilon,1) for any epsilon>0, the least report is one. Thus arbitrarily
small changes of a source probability can cause a unit jump in the *chosen least
report*. Nevertheless H_epsilon(r)-H_0(r)=epsilon(1-r) for each fixed r, a small
change. This is not an error in C44: feasibility and an attained optimum do not
establish robustness of the optimizing report.

### Positive alternative 1: quantify a nondegenerate source region

On the convex region 1+p-s>=alpha>0, the derivatives of t are

    partial_p t = (1-s)/(1+p-s)^2,
    partial_s t = p/(1+p-s)^2.

They are nonnegative and their sum is 1/(1+p-s)<=1/alpha. Integrating along a
line segment in that region gives

    |t(p,s)-t(p',s')| <= ||(p,s)-(p',s')||_infinity / alpha.

For 0<alpha<=1, the constant is sharp in the limit at (p,s)=(alpha,1) when s is
decreased slightly. A denominator lower bound is a real additional source
hypothesis, not a reason to relabel every poorly conditioned case undefined.

### Positive alternative 2: retain a declared self-prediction error allowance

Permit an estimate r to drive the original policy while the published failure
upper bound is min(1,r+xi), for a declared xi>0. Do not change the policy to use
r+xi without a new analysis. The acceptance condition is

    H_(p,s)(r) <= r+xi,

not the former exact-upper-report condition. Its least feasible r is

    t_xi(p,s)=max(0,(p-xi)/(1+p-s))  when 1+p-s>0,
    t_xi(0,1)=0.

On the active region p>xi the denominator is at least p>xi. Its derivatives are

    partial_p t_xi=(1-s+xi)/(1+p-s)^2,
    partial_s t_xi=(p-xi)/(1+p-s)^2.

Their sum is again 1/(1+p-s), at most 1/xi. On p<=xi the function is zero. It is
continuous across p=xi; near the degenerate corner it is identically zero. A
line segment crosses the active/inactive interface at most once, so integrating
the derivative on its pieces proves the global bound

    |t_xi(p,s)-t_xi(p',s')|
      <= ||(p,s)-(p',s')||_infinity / xi.               (13)

For 0<xi<1 the constant 1/xi is sharp: compare (p,s)=(xi,1) with
(xi+epsilon,1), obtaining t_xi=epsilon/(xi+epsilon). At xi=1 the function is
identically zero, so the displayed general bound is valid but not sharp.

For any nonempty compact uncertainty family Gamma, the least common report is
sup_Gamma t_xi. If Gamma and Gamma' are within Hausdorff infinity-distance delta,
(13) gives a difference of at most delta/xi between their least common reports.
Proof: approximate any point in either set by a point in the other, apply (13),
then take the two suprema. Matched finite vertices within delta give the same
Hausdorff bound for their convex hulls by using the same convex weights.

This is a deliberately explicit uncertainty tradeoff: allowing a small stated
prediction error removes the degenerate jump, but the conditioning constant
worsens as that allowance approaches zero. It does not certify source accuracy,
turn an approximate estimate into an exact report, or guarantee improved cost
of the newly chosen policy. The paired-cost guard from earlier F04 remains a
separate requirement. Both routes can represent this restricted alternative;
Gate A must decide which version of reflection the first core should express.

### Source error and finite precision in that same reflective example

The positive slack result remains conditional, but its remaining numerical
obligations can be stated directly. Suppose each true (p,s) is within infinity
distance delta of an admitted approximate pair (p_hat,s_hat). For any *fixed*
r in [0,1],

    |H_(p,s)(r)-H_(p_hat,s_hat)(r)|
      <= (1-r)|p-p_hat| + r|s-s_hat| <= delta.

Thus an approximate-source certificate H_hat(r)<=r+xi implies the true bound
H(r)<=r+xi+delta. This does not need independence of the two errors; it uses a
uniform joint approximation premise. It does not establish that premise.

For report rounding, F_(p,s)(r)=H_(p,s)(r)-r=p-(1+p-s)r has slope in [-2,0].
If an exact r is accepted and the implemented report r_tilde in [0,1] satisfies
r_tilde>=r-epsilon_r, then

    F_(p,s)(r_tilde) <= xi+2 epsilon_r.

Combining source and rounding errors yields the published failure upper bound

    min(1, r_tilde + xi + delta + 2 epsilon_r).

Rounding upward is safe for the same-source report inequality without that
extra term; this says nothing about whether upward rounding improves task cost.
The kernel still uses r_tilde, not the published envelope as a branch probability.
The distinction prevents a circular change of controller semantics while certifying it.

If kappa is fixed and the source probabilities change by at most delta, a
change from exact least slack-report r to r' satisfies

    |J_(p,s)(r)-J_(p',s')(r')|
      <= delta + (1+kappa)|r-r'|,

after cancelling a common baseline. Under the matched-family hypothesis of
(13), this is at most delta+(1+kappa)delta/xi. For a *fixed actual model* the
first delta term is absent. This bounds deterioration in magnitude, not its
sign; a paired improvement condition is still needed for a non-worsening promise.

An unknown admissible slack is a different problem: robust acceptance across
xi in [xi_min,xi_max] uses xi_min. If xi_min=0, the corner obstruction can return.
A chosen positive approximation budget must not be silently substituted for a
hard zero-error requirement, a confidence probability, or a preference weight.
This final check ties numerical modesty to an explicit operational contract.

Two final hand checks delimit the constants. For 0<xi<=1, t_xi<=1-xi:
if p>xi then (p-xi)/(1+p-s)<=(p-xi)/p<=1-xi because p<=1;
otherwise t_xi=0. The upper endpoint is attained at p=s=1. The published bound
there is still one, so the algebra has not turned certain failure into safety.

The report-rounding factor two can be attained: p=1,s=0,xi=1/4 gives least
r=3/8. Rounding downward by epsilon_r=1/16 yields r_tilde=5/16 and

    H(r_tilde)-r_tilde = 1-2(5/16) = 3/8
                         = xi+2 epsilon_r.

The source-error and rounding constants are separate sharp controls; no claim
is made that every combination of their worst cases is jointly attained. These
checks leave the original exact-report results intact while identifying the
extra condition required for a robust practical implementation.

Final post-test self-review rederived the reflection bounds from the branch
expectation rather than the code: (i) the report residual slope is -(1+p-s),
(ii) the two active slack-threshold derivatives sum to 1/(1+p-s), not 2/(1+p-s),
(iii) one-sided source matching suffices for an upper risk envelope, whereas
symmetric Hausdorff matching gives two-sided threshold stability, and (iv) the
paired-cost witness remains feasible at both the zero-margin and adverse-update
boundaries. No change to the original exact-report theorem was needed. The
additional slack is explicitly a changed report contract, not a silent repair
of an earlier false statement.
