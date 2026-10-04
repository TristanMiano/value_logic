# F13: scientific aliasing and staged reasoning cascades

Contributor: **Codex (GPT-6)**. Started October 4, 2026.
Status: complete at F13 case-study scope; project novelty NOT YET SUPPORTED.
Work record: [F13](../work_logs/F13_2026-10-04_S1.md).

## 1. Common question and declared scope

What evidence must survive a change of consumer or executable policy? A
scientific approximation and a reasoning policy both have modeled losses,
observation-dependent execution and resource costs. A small old performance
summary can omit directions used by the revised consumer. That general fact
is established in C3; this task must supply richer actual families, useful
scoped consequences, and a stronger comparison, not rename it as novelty.

All scientific quantities below refer to an explicit polynomial model, not
final truth. All proof claims are conditional on a fixed context and checker.
Performance assertions about a versioned evaluator require separately supplied
evidence about its actual executions. Native proof validity, empirical adequacy
of a source model, and usefulness of running a proof procedure are distinct.

## 2. Scientific family: an invisible degree-six residual

On 0 <= x <= 1 define

    g(x) = 30 x^2 (1-x)^2,
    h(x) = -2688 (x-1/2)^2 ((x-1/2)^2-1/16) ((x-1/2)^2-1/4),
    f(x) = a + b x + u g(x) + v h(x).

The four coefficients are real, with rational evidence bounds where supplied.
The integral of g is 1. Writing t=x-1/2, the unscaled h has integral

    1/448 - 1/256 + 1/768 = -1/2688,

so the integral of h is also 1. Thus I(f)=a+b/2+u+v. This is an ordinary
four-dimensional subspace of degree-six polynomials, with no stochastic or
empirical adequacy guarantee built into the choice of basis.

At all five dyadic nodes 0,1/4,1/2,3/4,1, h vanishes. Consequently the
trapezoid T, Simpson S and five-node Boole B outputs are

    T = a+b/2,
    S = a+b/2 + 5u/4,
    B = a+b/2 + u.

Their signed errors (output minus integral) are -u-v, u/4-v, and -v.
The complete five-node observation determines a,b,u but says nothing about v.
Any rule claiming an absolute error bound from those observations alone is
invalid on this unbounded-v family: arbitrarily large v preserves every
sample and changes the integral. With |v|<=V supplied externally, the
minimax absolute error of any deterministic estimate from the five samples
is at least V, attained by B. Indeed the two indistinguishable integrals
a+b/2+u +/- V are 2V apart. This lower bound also holds for randomized
estimates under worst-case expected absolute error, by the triangle inequality.
It is a standard information limitation specialized to the declared family.

### 2.1 One additional location, and the strong ordinary control

At x=1/8, g=735/2048 and h=6615/2048. Endpoints identify a,b;
the midpoint gives u=(8/15)(f(1/2)-a-b/2). Let
r=f(1/8)-a-b/8. Then

    v=(2048r-735u)/6615,
    Q=a+b/2+u+v=I(f).

Q uses four distinct samples (0,1/2,1,1/8). It is an ordinary exact linear
interpolation/integration rule for this family. A workflow which already paid
for five samples needs one *additional* sample; a fresh deployment of Q needs
four. Neither those sunk observations nor this rule's algebra can be priced
as five additional evaluations. If arbitrary new nodes are allowed, ordinary
four-point Gaussian quadrature is also exact for every degree-six polynomial;
we do not exclude that stronger general alternative to create an advantage.
Fixed sensor locations are a possible declared restriction, not an inherent
limitation of ordinary numerical methods.

### 2.2 Loss and consumer revisions

With per-evaluation deployment price c>=0, use

    L_T=|u+v|+2c, L_S=|u/4-v|+3c, L_B=|v|+5c, L_Q=4c.

These are loss proxies, not truth degrees. Q is exact only within the stated
model and exact-arithmetic sampling assumptions. B is dominated by Q for this
fresh-deployment comparison, so it cannot be the strongest fallback.

Relative replacement and absolute adequacy ask different questions. If u is
known, the triangle inequality gives |u/4-v|-|v|<=|u|/4, with equality for an
appropriate sign of v. On a symmetric interval [-V,V], including V=0, the
bound is attained. Hence S versus B has exact worst excess |u|/4-2c,
independent of V, while the absolute error of S has exact worst |u|/4+V.
A favorable relative certificate may coexist with arbitrarily bad absolute
accuracy. Revision from a relative comparator to an absolute tolerance is a
change of query; it must not inherit an irrelevant old guarantee.

For a nonempty joint source P in (u,v), S versus Q has exact bound

    max(h_P(1/4,-1), h_P(-1/4,1)) - c,

where h_P is the ordinary support function. A source strip
|u/4-v|<=d gives bound d-c whenever the strip extremes are feasible.
Replacing P by independent u/v intervals can destroy this cancellation.
No advantage over ordinary projected robust optimization follows: it computes
these same two directions and can retain their coefficients.

### 2.3 Sampling noise and a better placement of the fourth node

Expanding the four-node rule at 1/8 gives the weights, in node order
0,1/2,1,1/8,

    (-1/126, 64/135, 989/4410, 2048/6615).

They sum to one. If each observed function value has an independently bounded
adversarial additive error of magnitude <=delta, this rule's sharp noise
amplification is its coefficient l1 norm, 64/63. The bound is attained by
choosing each noise sign to match its coefficient. Exactness on the noiseless
family does not mean exactness on measured values.

For any fourth node z where h(z)!=0, an exact rule on this family has

    w_z=1/h(z), w_m=(8/15)(1-g(z)/h(z)),
    w_1=1/2-w_m/2-z*w_z,
    w_0=1/2-w_m/2-(1-z)*w_z.

At z=1/12, g=605/3456, h=1925/486, and g/h=99/2240. Therefore
w_z=486/1925, w_m=2141/4200, and both endpoint weights are positive.
All four weights are positive and sum to one, so the sharp noise factor is
1, the smallest possible for any linear rule exact on constants. This is a
concrete ordinary repair if the measurement location is free. It is not a new
quadrature construction method. The 1/8 rule remains relevant when that is
the available additional sensor location.

Suppose instead the actual integrand is f+r with |r(x)|<=R, independently of
the polynomial parameters. For a rule Q with weights w exact on f,

    |Q(observations)-I(f+r)| <= (sum |w|)*delta + (1+sum |w|)*R.

This follows by separating measurement noise, the finite sum of r at nodes,
and its integral. For unrestricted bounded r the two terms have the stated
worst-case constants; for continuous r the discrepancy constant is a supremum
approached by narrow spikes at the finite nodes. Under the positive 1/12 rule
the bound is delta+2R. Extra smoothness can improve it, but must be a premise.
The four-node model repair is not a guarantee against arbitrary discrepancy.

In fact delta+2R is the minimax absolute-error value for any estimator from
these fixed finite sample locations on this discrepancy class with unbounded
constant term. For a zero observation vector, choose f=-(R+delta), residual
r=-R away from the sample locations but r=+R at them, and measurement errors
+delta. The integral is -2R-delta. Negating everything gives identical
observations and integral +2R+delta. No estimate can have smaller worst
absolute error on both worlds; randomized output also obeys this lower bound
by the triangle inequality. Continuous residuals approach the same integrals
with narrow node hats. The positive exact 1/12 rule attains the upper bound,
so nonlinear estimation from those same observations cannot improve it on
this class. This does not cover randomized new sampling locations, stronger
smoothness or a bounded constant term.

### 2.4 A sharper relative bound from sharing the same model discrepancy

The preceding absolute-error enclosure need not be the best replacement
guarantee. Let S and Q use the same observed values at their shared nodes,
with node errors bounded by delta, and let the actual integrand be f+r with
|r|<=R. Extend both weight vectors to their union of nodes and put w=S-Q.
Their common target integral cancels inside the reverse triangle inequality:

    |S-I|-|Q-I| <= |S-Q|
                <= |u/4-v| + (R+delta) sum_j |w_j|.

Thus the excess priced loss is at most the right side minus c. This controls
relative replacement even when Q itself is not absolutely accurate. The bound
does not assume independent errors: it uses the same r and the same noise
at shared nodes. A model which gives the two methods unrelated copies of those
measurements loses this particular guarantee.

For Q at 1/12 the endpoint weights are 253/18480 and 4141/18480, and

    sum |S-Q| = 28633/46200 < 1.

For Q at 1/8 the corresponding norm is 694/945. Both are smaller than the
absolute discrepancy coefficient 2 (or 127/63 for the 1/8 rule). With delta=0
the displayed relative discrepancy constant is sharp on the unrestricted
bounded-residual class for either of these two rules. Choose the node values
of r to maximize the signed S-Q difference, aligned with u/4-v. For these
specific weights the resulting Q(r) lies within [-R,R], so choose the integral
of r to equal Q(r), leaving Q's error zero and attaining the comparison bound.
Finite node values and the integral can be set independently for bounded
measurable r. Here continuous r can also attain the bound when delta=0:
for R>0 the required Q(r) is strictly inside (-R,R). Use disjoint continuous
node hats with the prescribed signs and choose the common interior baseline
to make their integral exactly Q(r). Sufficiently narrow hats keep that
baseline inside (-R,R). For R=0 attainment is immediate. The general noisy
physical source has additional distinctions described in 2.8.

The bound is ordinary linear error propagation plus a shared-target
inequality. Its application relevance is that a tolerable relative decision
can survive discrepancy which defeats an absolute-accuracy claim. Its
limitations are explicit: the noise-coupling convention, admissible residual
class, sample acquisition timing, and the chosen comparator all matter.

### 2.5 Native derivation with individually unbounded losses

The relative guarantee can be reconstructed using the existing rules, without
assuming a finite bound on the target integral. Let r_j and e_j be the shared
node discrepancy and measurement error, with |r_j|<=R and |e_j|<=delta. Let J
be an unbounded common error coordinate. Set d=u/4-v and

    E_Q = J + sum Q_j(r_j+e_j),
    E_S = J + d + sum S_j(r_j+e_j).

In the physical discrepancy model J=-I(r); leaving it unrestricted is a sound
relaxation. The source still has the previously stated joint constraints on
u,v and separate bounds on each r_j,e_j. It contains no primitive conclusion
about |E_S|-|E_Q|. Both absolute errors can be unbounded through J.

First derive, by scaling and adding the appropriate signed source rows,

    +(E_S-E_Q) <= D,  -(E_S-E_Q) <= D,
    D=min(U/4+V,d_cap)+(R+delta) sum |S_j-Q_j|,

where an absent joint cap means the first minimum is U/4+V. The cancellation
of J is an exact algebraic rewrite. For each sign sigma, the native lattice
rule gives sigma E_Q<=|E_Q|. Add the corresponding difference bound, then
rewrite to obtain sigma E_S<=|E_Q| with budget D. The maximum-common rule
combines these into |E_S|<=|E_Q| with budget D. Finally add the constant price
difference 3c-4c=-c. The derived replacement budget is D-c.

This proof uses shared source identity, signed affine evidence, an unbounded
common coordinate and ordinary lattice/addition rules. It does not infer
absolute adequacy. It also does not assume J is final metaphysical truth:
the guarantee quantifies over every J in the explicitly admitted model. The
bound is sharp on this enlarged native source: choose node signs and a
feasible d to attain D, then choose J large with the matching sign so the
two absolute errors have that difference. Physical constraints relating J to
r can only narrow the source; sharpness there needs the separate argument in
2.4 and is not asserted for arbitrary noisy variants.

This also identifies the operational timing: prior evidence selects a fresh
deployment rule before its samples are paid for. After samples have already
been collected, their acquisition cost is sunk. A nested policy which has
already paid for endpoints and midpoint compares stopping at S with *one more*
measurement and Q; its incremental sample charge is c. Deriving or checking
that decision is a separate reasoning cost.

### 2.6 An optimal extra observation under a different, explicit noise contract

Suppose the old five measurements are exact and already paid for. They identify
a,b,u. The remaining interval for v is [l,r], for example the intersection of
[-V,V] with [u/4-d,u/4+d]. Write W=(r-l)/2. A new observation at z has error
|e|<=delta and, after subtracting the known nuisance polynomial, equals

    y=h(z)v+e.

For h(z)!=0 the posterior is [l,r] intersected with the interval centered at
y/h(z) of radius delta/|h(z)|. Its midpoint minimizes worst absolute integral
error. The worst posterior radius, over possible observations, is exactly

    min(W, delta/|h(z)|).

The upper bound is intersection of two intervals; equality follows by centering
the observation interval at (l+r)/2. A minimax choice between stopping and buying
that one sample at price c therefore has modeled cost

    min(W, c+min(W,delta/|h(z)|)).

This is a sequential acquisition statement, not the all-samples-noisy contract
in 2.3. It uses a bounded interval or an explicitly unbounded prior, calibrated
noise and a fixed family. With unbounded v the new radius is still delta/|h(z)|,
whereas the old minimax absolute error is infinite. Model discrepancy requires
its own additional bounds; it is not removed by this calculation.

If the location is freely chosen with the same price, maximize |h(z)|. Put
t=(z-1/2)^2. Then

    h=-2688(t^3-5t^2/16+t/64),
    h'(t)=0 iff 192t^2-40t+1=0,
    t_+/-=(5+/-sqrt(13))/48.

Checking both stationary points and the interval endpoints gives

    H=max_[0,1]|h|=(245+91 sqrt(13))/144,
    z=1/2 +/- sqrt((5+sqrt(13))/48).

These two locations minimize the worst new error. The rational node 1/12 has
h=1925/486 > (199/200)H, so its radius is less than 200/199 times the optimum.
The exact optimum uses irrational locations and constants; this analytic design
result is not silently introduced as a rational native atom. The rational
alternative and its evidence coefficients are admitted by the existing fragment.
An ordinary experimental-design calculation obtains the same result.

### 2.7 Retention and the next experiment must be specified together

Keeping only B=a+b/2+u prevents the preceding one-observation repair on the
unbounded nuisance family. For h(z)!=0, choose changes u=0, a=-b/2 and
v=(1/2-z)b/h(z). They keep B and the new value f(z) at zero, while the integral
v varies without bound. At nodes where h vanishes, the unobserved v itself
already supplies the obstruction. Thus an old scalar integral estimate plus
one new sample has no finite uniform absolute-error guarantee on this family.

The repair is consumer-specific and available to ordinary methods. If the
future location z is fixed before discarding the old measurements, retain

    R_z = (a+b/2+u) - (a+bz+u g(z))/h(z).

One retained scalar now suffices: I=R_z+f(z)/h(z), with new-noise radius
delta/|h(z)|. If the old B must also remain answerable, two independent retained
linear functionals are necessary and sufficient. R_z is not proportional to B:
that would require z=1/2 from the constant and linear coefficients, but h(1/2)=0.

If every later z with h(z)!=0 must remain available, three retained independent
linear functionals of (a,b,u) are necessary and sufficient. For necessity,
a direction annihilating every R_z obeys

    (a+b/2+u) h(z) = a+bz+u g(z)

on an open set. This is a polynomial identity. The degree-six coefficient first
forces a+b/2+u=0, and then the right polynomial vanishes identically, forcing
a=b=u=0. Hence the family of R_z spans all three nuisance coordinates. Retaining
(a,b,u) attains the bound. These are linear-summary ranks on an unbounded model,
not lower bounds for arbitrary real encodings or bounded approximate summaries.

The consequential distinction is one scalar tailored to a frozen experiment,
two when the old output must coexist with it, or three for arbitrary later
location revisions. The number of stored scalars alone does not determine
usefulness. This specializes the earlier preservation criterion to an actual
acquisition family; it is not claimed as a new general information principle.

### 2.8 Sharper physical comparison when the common discrepancy is bounded

The unbounded J relaxation in 2.5 is intentional. If the physical premise
|r|<=R is retained, it also gives |J|=|I(r)|<=R. Put A=R+delta and denote
the Simpson and Q weight vectors on their common four-node support by s,q.
For any -1<=lambda<=1,

    |E_S|-|E_Q| <= |E_S-lambda E_Q|
      <= d_max + A ||s-lambda q||_1 + R |1-lambda|,

where d_max=min(U/4+V,d_cap). The first inequality follows from
|lambda E_Q|<=|E_Q|. Minimizing the last two terms over lambda gives the exact
worst error increment on the rectangular source for the shared node values
and J. To see exactness, use sign symmetry to reduce the problem to
max_{|x_j|<=A,|J|<=R} [s.x+J-|q.x+J|]. Introducing a variable below both
affine branches gives a finite linear program. Its dual chooses the convex
combination of those branches, equivalently lambda in [-1,1], with the stated
box support function. Primal feasibility and boundedness give equality.
The d coordinate is independent of these errors and attains d_max.

For the 1/12 rule the minimum is lambda=1 for every R,delta>=0; its value
is A*28633/46200. Indeed q.sign(s-q)=2167/46200>0, so the convex objective's
left derivative at 1 is negative (unless A=R=0). For the 1/8 rule,
q.sign(s-q)=-64/945. The only relevant interior kink is
lambda_*=735/989, where the endpoint-1 coefficient changes sign. The exact
error increment beyond d_max is

    A*694/945                              if delta<=881R/64,
    A*6382/8901 + R*254/989                 if delta>=881R/64.

Both expressions agree at the boundary. This refines the earlier sufficient
bound when measurement noise is large relative to model discrepancy. For
R=0,delta=1, set errors at 0,1/2,z to +1,+1,-1 and choose the endpoint-1 error
to make q.x=0. It lies in [-1,1], and s.x=6382/8901 attains the sharper value.

The rectangular node/integral source is physically attainable by bounded
measurable residuals: finite node values do not constrain their integral.
Continuous residuals approximate every such choice with narrow node hats.
For the 1/12 rule the sharp bound can in fact be attained continuously: choose
the indicated node signs, choose integral zero, and interpolate continuously
within [-R,R]. The Q error is then nonnegative, so the reverse-triangle step
is equality. For the 1/8 high-noise branch, the extremal integral can lie on
the boundary +/-R while nodes have the opposite sign; continuous attainment
is not generally available, although the supremum is the same.

All of this is ordinary finite robust optimization and error propagation.
It also exposes the exact native obligation: lambda!=1 requires bounds on J.
An unbounded-common-error receipt cannot silently use the sharper physical
source. The existing lambda=1 native proof remains valid on its larger source.

### 2.9 A complete scientific decision, and what would reverse it

Take U=V=1, the joint strip |u/4-v|<=1/64, fresh sample price c=1/32,
node discrepancy R=1/100 and measurement error delta=1/200. Compare using
three-node S with four-node Q at 1/12 under priced absolute error. The supplied
source rows contain the strip and separate node-error bounds; they contain
neither a relative loss score nor a bound on the common J. The native steps
in 2.5 derive

    L_S-L_Q <= 1/64 + (3/200)(28633/46200) - 1/32
              = -4873/770000 < 0.

This conditionally licenses the cheaper three-sample deployment. It does not
certify either method's absolute accuracy under the unbounded-J source.
An absolute-tolerance request must use the stronger physical model and its
own bound, or acquire more evidence. Withdrawing the joint strip admits a
larger error direction and invalidates this replacement conclusion. Changing
the reference rule, measurement coupling, source revision or price similarly
requires a current request and new calculation.

The ordinary baseline solves the same two signed support directions and
obtains the identical number. The native structure's role here is to expose
the assumptions, cancel the shared target, compose the priced loss and produce
a request-bound receipt. The case demonstrates why those relationships matter;
it does not establish that this calculus is the only way to express them.

## 3. Staged self-assessment candidate: versioned bounded-search cascades

For a fixed finite development task population, let B_i in {0,1} indicate
whether bounded search version i produces a receipt accepted against the
independently supplied current request. A zero means unresolved by that
procedure, not false in the semantics. A rejected malformed/stale receipt is
not a successful proof. Each B_i must be obtained by actual execution or
independently justified behavior evidence, never by the evaluator asserting
its own reliability.

A staged evaluator measures its own versioned behavior, selects an ordered
cascade, and on later tasks runs versions until the first accepted receipt or
exhaustion. The selection changes its later reasoning and its unresolved rate.
This is finite and acyclic; there is no self-certifying fixed point. The
scientific query's theoremhood is independent of which search budget is chosen.

Let F_i=1-B_i, let order pi contain k distinct versions, charge fixed nonnegative
reasoning costs c_i per attempted version and unresolved loss M>=0. A declared
finite joint execution law p determines

    C_pi = sum_(j=1..k) c_(pi_j) E[prod_(r<j) F_(pi_r)]
           + M E[prod_(r<=k) F_(pi_r)].

This composite is derived from execution paths; it is not a supplied input
score. Costs represent measured or explicitly modeled reasoning costs, not
scientific sample price c. Audit and fallback costs need separate accounting.
Future execution evidence must match the version and task population.

### 3.1 Higher-order information can matter after every pair is retained

For k>=3, consider the two uniform laws on even versus odd parity bit strings
(F_1,...,F_k). Every proper-subset joint marginal agrees: it is uniform. To
see this, fixing m<k bits leaves 2^(k-m-1) completions of each parity. Yet the
all-failure event has probability 2^(1-k) in the parity class containing the
all-ones string and zero in the other class. For any full cascade, all
attempted-cost terms use proper-subset moments
and agree. The unresolved-loss difference is exactly M*2^(1-k).

For k=3 this gives equal individual and pairwise success records with a
composite unresolved-rate difference of 1/4. This extends the old two-bit
program-edit witness to an executable staged reasoning question. It is still
an ordinary dependence phenomenon, not a new information-theoretic principle.
Actual realizations, query revisions and adverse instances remain to construct.

### 3.2 Candidate preservation boundary (to audit)

For one fixed order, its k nonempty prefix-failure probabilities determine
cost and unresolved loss for every fixed vector of costs and penalties. If
every subset/order edit and every nonnegative cost/penalty is permitted, all
nonempty subset-failure moments suffice. They are an invertible Boolean
moment representation of the full joint execution law, by inclusion-exclusion.
On the full probability simplex, a linear summary preserving all such queries
must have rank 2^k-1 on its direction space. Restricting the allowed edits or
the source can reduce that requirement; arbitrary encodings and fixed-threshold
decisions are not covered by this linear rank claim.

The shared scientific/program contract is: retain the admitted source and
the directions used by the specified future consumer family, and recheck on
revision. The substantive application question is how much that family grows
when a scientific consumer or a reasoning cascade is edited. Ordinary support
queries and execution-trace summaries are the mandatory exact controls.

### 3.3 Proof of the rank boundary and its precise restrictions

Write m_A=E[prod_(i in A) F_i], including m_empty=1. If a cascade may contain
exactly any nonempty subset A and its unresolved penalty is allowed to vary,
preserving all of its costs preserves m_A: subtract two cost queries with
identical attempted costs and different penalties. Thus every nonempty moment
is necessary for exact recovery over the full query family. Zero attempt
costs are not required for this subtraction argument.

For each exact failure set Z, inclusion-exclusion gives

    p(F_i=1 iff i in Z) = sum_(A containing Z) (-1)^(|A|-|Z|) m_A.

Proof: expand prod_(i notin Z)(1-F_i) and multiply by prod_(i in Z)F_i.
Consequently the 2^k moments, including normalization, are linearly independent
functions on the Boolean cube. If a linear summary has rank less than 2^k-1
on the simplex's direction space, it has a nonzero invisible probability
direction. An interior law plus/minus a sufficiently small multiple of that
direction gives valid laws with the same summary and a different required
moment. Suitable penalties and a threshold separate a cascade decision.
This is an application of the existing relative-kernel criterion, with the
newly declared executable query family providing the rank.

For a fixed order and fixed length, only its k prefixes are needed. Allowing
independent costs c_2,...,c_k and M varies their k coefficients, so the k
prefix moments are necessary on the full simplex for *all those numeric
queries*. A fixed cost vector needs just one linear cost statistic; a fixed
decision threshold may need less. If all k! full orders are permitted but
only one cost vector is fixed, the previous 2^k-1 necessity does not follow
without further analysis. Do not silently broaden the proven family.

### 3.4 Exact ambiguity after all proper marginals

When every proper-subset marginal of F is uniform, the only free Fourier
coefficient is its full parity interaction. The admitted laws are

    p_theta(f)=2^(-k) [1+theta*(-1)^(sum f_i)], -1<=theta<=1.

This also follows directly from the moment inversion above, fixing every
proper moment m_A=2^(-|A|). Nonnegativity gives exactly the stated interval.
The all-failure bit string has parity (-1)^k, hence

    m_all=2^(-k) [1+theta*(-1)^k] in [0,2^(1-k)].

The orientation of the parameter depends on k; the even/odd populations in
3.1 were defined using failure bits. For odd k it is the *odd*, not even,
population that contains the all-failure string. The invariant conclusion is
the interval and the absolute unresolved-loss gap M*2^(1-k).

This restricted family has only one unknown parameter. Given its exact proper
marginals, ordinary retention of q=m_all suffices for every reset cascade's
loss distribution. The full-simplex exponential rank bound does not apply to
this one-dimensional source. At fixed M>0 even one full-order mean already
determines q. A richer information-loss claim must explicitly broaden the
source rather than silently borrowing that rank from another model.

For three unit-cost attempts and M=4, the attempted-cost expectation is
1+1/2+1/4=7/4 in both populations, while total cost is 7/4 or 11/4.
Against a fixed complete fallback with modeled cost 9/4, one population
favors the cascade by 1/2 and the other disfavors it by 1/2. Pairwise evidence
alone gives robust bound 11/4 and cannot license that replacement. This is a
cost-model example, not measured Python performance or a claim the fallback
must cost 9/4.

### 3.5 Quantitative preservation and choice regret

Suppose retained estimates of the needed prefix moments have errors <=e_A.
For a fixed cascade with nonnegative costs and penalty,

    |C_pi - C_hat_pi| <= sum_(j=2..k) c_(pi_j)*e_(prefix(j-1))
                        + M*e_(prefix(k)).

The first attempted cost has no uncertainty because m_empty=1. This is an
application-specific error budget from the path formula, not an assumption of
independent outcomes. If every candidate policy's cost error is <=eta, choosing
a minimizer of the approximate costs has true regret <=2eta, by inserting
the approximate minimizer between the true minimizer's two error bounds.
If the approximate best-versus-second-best margin exceeds 2eta, the same
unique choice is certified. Correlated moment constraints can improve these
triangle-inequality bounds by ordinary linear optimization; do not call them
always sharp.

Source revision matters twice: changed probability evidence needs new moment
bounds, while a changed executable version needs new behavior coordinates or
a proved cross-version relation. Reusing an old behavior column by its display
name is not an evidence update. The same distinction applies when scientific
model discrepancy or a new numerical consumer adds a previously invisible
direction.

### 3.6 One joint feasible law, not independently maximized moments

For uncertain p in a nonempty rational polytope P of joint laws, the robust
cascade bound is the support query max_(p in P) C_pi(p). Each candidate law
interprets *all* prefix moments. Independently maximizing the moments gives
a sound outer bound for nonnegative costs, but can be strictly weaker.

For two attempts, let P be the convex hull of p_A concentrated on F=(1,0)
and p_B placing half mass on (0,0) and half on (1,1). With both attempt costs
one and M=1, the two endpoint costs are both 2:

    C=1+m_{1}+m_{1,2};
    (m_{1},m_{1,2})=(1,0) or (1/2,1/2).

Every mixture therefore also costs 2. Keeping just separate moment intervals
admits the impossible pair (1,1/2) and yields 5/2. A comparison allowance
strictly between 2 and 5/2 is lost by this rectangular summary. Ordinary
two-variable linear programming or the exact relation m_1+m_12=1 repairs it.
The case is a limitation of the summary, not of ordinary optimization.

### 3.7 Histories, shared caches, and the limits of the static trace table

The Boolean trace model assumes each version is a deterministic bounded
procedure on the same request, starting from its declared fixed state. Random
seeds can be included in the joint source, with a declared coupling. Running
one procedure must not change another's potential outcome. If restart versus
resume, lemma sharing or a cache alters behavior, the static table is invalid.

Counterexample: the current source contains x<=y and y<=0. Procedure A copies
a checked proof of x<=y into a cache but leaves the requested x<=0 unresolved.
Procedure B only combines that cached lemma with y<=0, and is unresolved when
the cache is empty. Both standalone success bits are zero. Yet A then B
resolves the query, whereas B then A does not resolve it within two calls.
All receipts remain subject to the independent current-context receiver.
On a source revision, a cached lemma from the old context must be rejected or
explicitly reconstructed; its mere presence cannot make B succeed soundly.

The repair is ordinary finite execution semantics: use history-indexed
outcomes/costs and include cache state and version identities in the source
contract. For a bounded history graph, each policy has a derived terminal-loss
vector over possible worlds, so ordinary joint-law support queries remain
exact. The k-bit subset-moment theorem applies only to the reset model; it is
not a theorem about arbitrary program edits, stateful cascades, or truly cyclic
self-improvement. An actual stateful implementation must be tested as such.

### 3.8 Native admission and theoremhood versus reliance

In the scientific fixed-action comparisons, u,v are source coordinates and
each loss is finite rational CPWA, so the existing F05 syntax applies directly.
A changed polynomial model or criterion changes the declared scope. Evidence
strips are premises, not primitive composite loss scores.

In a finite reset cascade, enumerate execution worlds f and derive each
policy's rational terminal loss ell_pi(f) by running the path. Its expected
loss is sum_f p_f ell_pi(f), affine in source probabilities. Simplex and moment
evidence is affine; a declared probability-to-loss valuation bridge gives
the native target unit. Products of the *fixed Boolean world labels* have
already been evaluated in the table. This does not admit multiplication of
uncertain source probabilities or uncertain cost coefficients into F05.
Changing costs can construct a new query with new rational constants; making
costs continuously uncertain needs a larger joint source or an explicit
sound approximation.

The finite table model can therefore express the metalevel expected-loss
comparison in the existing core, conditional on separately justified execution
and population evidence. This is distinct from each underlying native proof
search's object-level receipt. Accepting the latter proves its requested
comparison within the declared model; it does not prove that the evaluator
should spend resources seeking more receipts or trust its own success forecast.
An unavailable search outcome proves neither the negation nor a false theorem.

## 4. Actual bounded native procedures and later reasoning

The executable reset family has source coordinates x,y_1,...,y_k,z_0,z_1,z_2.
For each i the source supplies x<=y_i and y_i<=b_i, with b_i in {0,1}; it
also supplies x<=z_0<=z_1<=z_2<=0. The request is x<=0. Every source is
nonempty (the zero assignment witnesses it), and every request is a theorem
via the four-row chain, even when every short search leaves it unresolved.

Version i@1 attempts only its two-row chain. It derives x<=b_i by addition,
rewriting and the all-case rule; a current F07 receiver accepts it for x<=0
exactly when b_i=0. The code records outcomes from these actual checked
derivations, rather than treating the Boolean pattern as a success assertion.
The generic four-row version always resolves the request. A later query
x<=1 makes every short version successful; old performance coordinates must
not be reused as though the requested guarantee were unchanged.

This family deliberately makes all Boolean traces realizable through real
bounded native proof searches. It is a small diagnostic family, not a hard
theorem-proving benchmark. The longer chain is a complete fallback only for
this source schema. No claim of general proof-search completeness follows.

### 4.1 A staged update computed from the evaluator's own runs

Stage 0 executes each version on the declared finite calibration population,
with independent reset state and current checking. Stage 1 derives joint
prefix moments and chooses among all ordered subsets (including doing no
search) and the complete fallback. Stage 2 uses that selected policy on later
instances from the *declared same population model*. The latter match is an
assumption; the evaluator's report does not establish it.

For the present code, a short native trace has five proof nodes and the
fallback nine. Use one unit per emitted proof node as an **audit-work proxy**,
so c_i=5 and fallback cost H=9. This is neither measured runtime nor the full
cost of source inspection, proof construction, repeated checking or acquiring
the calibration traces. An unresolved outcome has declared penalty M=20 in
that proxy unit. The two three-bit parity populations give:

| Population | All-three cascade cost | Unresolved probability | Selected among all ordered subsets and fallback |
|---|---:|---:|---|
| Even failure parity (no 111 world) | 35/4 | 0 | Three-version cascade, cost 35/4 |
| Odd failure parity (includes 111) | 55/4 | 1/4 | Complete fallback, cost 9 |

Every individual and pairwise execution record agrees across these populations.
Empty, one-version and two-version policies cost 20,15,25/2 respectively.
Thus the choice above is checked against partial cascades as well, not forced
by offering only a weak single-procedure competitor. Equal costs are resolved
by smaller unresolved probability, then fewer attempts, then lexicographic
order. The mean result changes actual later search behavior; it does not
change theoremhood of x<=0.

### 4.2 The strongest ordinary control exposes this family's limit

The input source already displays each b_i. An ordinary solver may inspect
them, directly construct an available two-row proof, and use the long chain
only when all b_i=1. It emits a current checked receipt in every instance.
Its expected emitted-node counts are 5 (even population) and 6 (odd), below
both selected policies. Pointwise it emits five nodes if any short route
works and nine otherwise, avoiding the cascade's repeated unsuccessful or
unnecessary proof attempts. Its inspection and production cost still needs
charging before a *total-time* dominance claim; no such timing claim is made.

This is a specific negative application finding. It prevents a hidden-input
information argument from being misapplied to a source-visible proof problem.
The trace-summary separation remains true, but the ordinary solver can bypass
that prediction task. A genuine resource-use study would need consequential
search whose outcome is not cheaply exposed in the premises, with both
procedures charged for obtaining and checking that information. Merely making
the Boolean table larger would not meet this requirement.

### 4.3 Native metalevel comparison, derived from prefix evidence

For the full three-version order, retain m_1=1/2, m_12=1/4 and
0<=m_123<=q<=1/4. Its loss is

    C=5+5m_1+5m_12+20m_123;
    C-9 <= -1/4+20q.

The intermediate steps are the constant difference 5-9=-4, adding the
weighted prefix bounds 5/2 and 5/4, then the unresolved bound 20q. With a
declared probability-to-audit-loss valuation bridge these are native row,
scaling, addition, rewrite and all-case inferences. No composite C score is a
premise. The replacement is justified exactly when q<=1/80 in this source
family. Pairwise evidence alone admits q=1/4 and gives excess 19/4; the
complete even-parity trace gives q=0 and excess -1/4. The same arithmetic is
available to the ordinary coefficient baseline.

All q in [0,1/4] have a consistent joint law with the fixed proper marginals,
by the parity mixture in section 3.4. Treating the prefix coordinates as
independent [0,1] quantities would throw away useful constraints. Conversely,
their consistency is a mathematical source obligation, not something a
receiver infers from the evaluator's claim of calibration.

### 4.4 A risk revision reverses even the favorable mean conclusion

Under the even population, the cascade's audit-plus-unresolved loss has law
5 with mass 1/2, 10 with mass 1/4, and 15 with mass 1/4. The fallback is 9.
For upper-tail CVaR at confidence alpha in [0,1), direct tail integration gives

    (35/4-5alpha)/(1-alpha)      for 0<=alpha<=1/2,
    (45/4-10alpha)/(1-alpha)     for 1/2<=alpha<=3/4,
    15                         for 3/4<=alpha<1.

The cascade's favorable comparison survives precisely for alpha<=1/16.
For alpha>1/16 the complete fallback wins this comparison, despite the mean
improvement. Under uncertain q, mass q moves from loss 15 to loss 35 while
the first two atoms stay fixed. Every upper-tail risk therefore increases
with q, and the worst source is its upper endpoint. A fixed alpha is an
ordinary finite-law tail query; it can use the existing min-of-affine
representation. This does not import uncertain source multiplication.

The source-aware ordinary method has losses 5 throughout the even population,
and 5/9 in the odd population, so this risk revision does not create a hidden
native advantage. It instead shows why the consumer identity must accompany
a retained guarantee.

### 4.5 What sampling, instead of a declared complete population, would cost

The executed finite calibration population is exhaustive development evidence;
it is not an iid deployment sample or a generalization result. If an unknown
deployment law supplies iid trials, the *predeclared* 17-policy family has
losses in [0,35]. Hoeffding plus a union bound gives uniform mean error

    eta = 35 sqrt(log(34/delta)/(2n))

with confidence at least 1-delta. Uniformity permits choosing the policy from
that same sample, with regret <=2eta. A tiny 1/4 mean gap therefore requires
a large conservative sample bound. Changing the executable policy family
after inspecting the data requires fresh validation or a justified broader
uniform bound. Distribution shift or dependent samples do not satisfy the
stated iid argument.

Under the much stronger *externally justified exact proper-marginal model*,
only q is unknown. After n independent trials with zero all-failure events,
the one-sided binomial bound is q<=1-delta^(1/n). Certifying q<=1/80 then
requires (79/80)^n<=delta. This smaller problem illustrates how assumptions
and evidence acquisition, not just logical arithmetic, determine effort.
Neither confidence argument is evidence supplied by self-assertion, and
neither has been claimed for the present synthetic development corpus.

The common loss range can be sharpened from [0,35] to [5,35] for these 17
policies at M=20, replacing 35 by 30 in the uniform bound. This is still a
large conservative acquisition requirement for a quarter-unit advantage.
Under the exact-proper-marginal assumption and delta=1/20, zero failures in
239 iid trials suffice for q<=1/80; 238 do not. That cap only proves a tie
against the fallback. A cap q<=1/160, giving a guaranteed 1/8 improvement,
needs 478 zero-failure trials; 477 do not. Executing all three short versions
on each such trial costs 7,170 emitted nodes before other acquisition costs.
Amortizing that charge from the guaranteed 1/8 margin would require more
than 57,360 subsequent uses. These are conditional planning calculations,
not measured sample complexity, evidence of iid deployment, or a benefit
over the source-aware ordinary control.

For completeness, the uniform concentration calculation can be reconstructed
without relying on the inaccessible scanned theorem text. If Y lies in [a,b]
and psi(s)=log E exp(sY), then psi''(s) is the variance under the exponentially
tilted distribution. Under any distribution on [a,b],
E[(Y-a)(b-Y)]>=0 gives Var(Y)<=(E[Y]-a)(b-E[Y])<=(b-a)^2/4.
Integrating twice yields log E exp(s(Y-E[Y]))<=s^2(b-a)^2/8.
Independence multiplies moment-generating functions; Markov's inequality,
optimized at s=4eta/(b-a)^2, gives each upper-tail probability at most
exp(-2n eta^2/(b-a)^2). Apply the same bound to -Y and union over 17 policies.
The policies may be correlated on the same task; independence is required
across sampled tasks. Their counterfactual losses must actually be observed
or otherwise justified. Censored on-policy observations do not supply them
for free. Here the confidence failure probability delta is unrelated to
section 2's measurement-noise amplitude.

The zero-failure binomial statement has a similarly direct coverage proof.
For a fixed predeclared n, a false certificate q<=q_0 when q>q_0 can occur on
the zero-event outcome with probability (1-q)^n<(1-q_0)^n<=delta. This is a
frequentist error guarantee, not a posterior probability for q after seeing
the data. Repeating fresh batches until one has zero failures would invalidate
it: for any q<1 an all-zero batch eventually occurs with probability one.
An explicit sequence of error allowances whose sum is at most delta, or an
appropriate time-uniform method, is needed for such repeated testing.

On one valid coverage event q<=q_cap, all consequences for the fixed behavior
family hold together. In particular every alpha satisfying 20q_cap+4alpha<=1/4
is licensed at that confidence, even if alpha is selected after seeing the
cap. No separate error allocation is needed for every member of this consumer
family. A new executable version, population or object request changes the
behavior parameter and requires fresh evidence; receipt identity alone does
not establish statistical transfer.

### 4.6 Acquisition, amortization and the value of learning the population

Executing all three five-node short procedures on all eight development
contexts produces 120 proof nodes before any control/fallback/audit overhead.
Against the generic nine-node fallback, the favorable parity population saves
only 1/4 node unit per deployment. Charging just those 120 acquisition units
requires more than 480 later deployments for strict expected amortization.
This calculation grants a stable population and ignores other costs, so it is
an optimistic condition, not a measured break-even result. Against the stronger
source-aware method there is no positive emitted-node saving to amortize.

For one fixed cascade, gathering its prefix moments does not require executing
every counterfactual version after success: early-stopped traces already reveal
all its prefix-failure indicators. Reordering or adding a version is different;
unattempted outcomes can then be needed. A full counterfactual table is an
optional acquisition choice that supports more edits, not free evidence or
a minimum-cost requirement for every fixed consumer.

For a further metalevel calculation, suppose an externally declared prior puts
probability pi on the even population and 1-pi on the odd population, with one
fixed but unknown population governing future tasks. Restrict the available
deployment choices here to the full cascade and generic fallback. Without
learning the population, the best expected cost is

    min(9, 55/4-5pi).

Perfect knowledge of the population would reduce it to 9-pi/4. The value of
perfect information is therefore

    pi/4                  if pi<=19/20,
    (19/4)(1-pi)          if pi>=19/20,

with maximum 19/80 per future deployment. Any actual observation channel has
no greater value for these choices, since perfect information can reproduce
its policy. An acquisition costing K cannot be justified for N future uses
by this objective if K>N*19/80. This is a classical value-of-information
calculation, conditional on the prior and fixed population; the evaluator
cannot create either premise by reporting them.

Under a minimax criterion over the two populations, perfect identification
does not lower worst-case deployment cost below 9, because the unfavorable
population still uses the fallback. A positive acquisition cost therefore
does not improve that minimax objective. Switching between a Bayesian mean,
a tail-risk criterion and minimax is a substantive consumer change. It cannot
be obscured by saying simply that better self-assessment is valuable.

These limits affect research ambition: a larger data collection or a more
intricate native certificate is not justified by a tiny benchmark margin
alone. A stronger application needs either consequential decisions, cheaper
useful evidence, a defensible source-access restriction, or a different
benefit. The present results do not establish such a benefit over the strongest
ordinary combination.

The 17-policy calibration bound above applies to its declared menu: every
ordered subset with unresolved termination, plus a standalone fallback.
It is not an optimality claim over all adaptive strategies. Allowing a fallback
after a failed prefix adds legitimate hybrid policies. At M=20, replacing a
terminal unresolved charge by the nine-node fallback can only improve a fixed
prefix policy. Exhausting the three short procedures still wins on the even
population, and the immediate fallback still wins on the odd population;
the source-aware ordinary control remains stronger than either. Revised
menus require revised uniform statistical bounds.

Behavior evidence also needs an external provenance contract: executable
version, object request, population, reset/history convention and cost model.
The receiver binds a proof to the *supplied* current context. It cannot infer
that its probability rows actually describe those executions. In particular,
the weaker x<=1 request changes observed failures to zero; one must rebuild
the metalevel source, not reuse the old m_1=1/2, m_12=1/4 premises merely
because their arithmetic receipt is still well formed. The demonstrations
recollect outcomes and reselect the later policy after that request revision.

### 4.7 Population drift: why retaining only the unresolved cap can be unsafe

Start from the favorable even-parity population, with full-cascade loss law
5/10/15 of masses 1/2,1/4,1/4. Suppose the deployment law may differ by total
variation at most rho, using TV=(1/2)sum|p-p_old|. On the full Boolean source,
the cascade's loss ranges from 5 to 35. Therefore its mean can increase by at
most 30rho. For 0<=rho<=1/2 this is exact: transfer mass rho from a cost-5
world to the all-failure cost-35 world. The replacement against 9 remains
robustly justified exactly for rho<=1/120 in this range.

Merely changing the unresolved bound from q=0 to q<=rho while continuing to
use old prefix moments would instead report 35/4+20rho. At rho=1/100 that
incorrect calculation is below 9, while the valid shifted law costs
35/4+30/100=181/20=9.05. Its first two prefix moments both increase by rho.
This is a concrete unsafe transfer, not just a conservative summary failure.

If the drift is additionally required to preserve *every proper-subset
marginal*, the parity-mixture family applies. A mixture of weight t toward
the odd population has TV=t and q=t/4; mean cost increases by 5t. The exact
robust radius is then rho<=1/20, six times the unrestricted value. This larger
radius is purchased by a substantive joint invariance assumption, not by
renaming the evidence revision. There is no empirical claim that deployment
preserves those marginals.

This pairs with section 2.4: shared scientific discrepancy and constrained
population drift can support sharper replacement guarantees, but only while
the relevant joint relationships survive the revision. Ordinary coefficient
and support-function methods attain the same bounds. The novelty question
is the usefulness and distinctiveness of the combined application contract,
not priority for these standard inequalities.

### 4.8 A stronger ordinary control: cheap fallback collapses the risk decision

The information gap in section 5 does not automatically matter to the actual
replacement decision. Let a finite-mean loss X have support in {a} union
[b,infinity), with a<b, and compare it with a deterministic fallback h satisfying
a<=h<b. For 0<=alpha<1, upper-tail CVaR obeys the exact equivalence

    CVaR_alpha(X)<=h  iff  E[X]<=alpha*a+(1-alpha)*h.       (H)

Proof. Write p=P(X=a). If alpha<p, removing the lowest alpha mass removes
only loss a, so CVaR=(E[X]-alpha*a)/(1-alpha). If alpha>=p, the entire remaining
tail has loss at least b, and cannot beat h. In that case the mean condition
also fails: E[X]>=p*a+(1-p)*b, and subtracting its proposed bound leaves
(alpha-p)(b-a)+(1-alpha)(b-h)>0. This includes atoms and ties at alpha=p.
No inference from mean to a complete loss distribution was used.

In the actual full three-attempt family, a=5, b=10 and h=9. Therefore every
risk replacement query against that fallback is answered exactly by

    E[C_pi]-9 <= -4 alpha.

With the proper-prefix evidence in 4.3 and unresolved cap q, the sharp robust
condition is simply

    20q+4 alpha <= 1/4.

At q=0 this recovers alpha<=1/16; at q=1/160 the frontier is alpha<=1/32;
at q=1/80 only alpha=0 remains. Existing native mean receipts can be checked
against the stronger rational request budget -4 alpha. The interpretation as
a CVaR request relies on the proved support-gap lemma; no new nonlinear CVaR
atom or unrestricted statistical premise is inserted into the kernel.

The same equivalence holds uniformly over a source of laws sharing a,b,h.
It needs only the worst mean, even if all other tail details vary. Thus the
full-mean-profile collisions in section 5 do **not** show that the strong
ordinary route needs additional joint information to answer this actual
fallback comparison. A more expensive fallback h>=b, a random fallback, or
different path charges requires a fresh analysis. This adverse result is
particularly relevant to target selection: an information lower bound for
an unrestricted consumer family may be irrelevant to the useful consumer.

These arguments also combine statistical evidence, consumer revision and
population drift without keeping stale prefix premises. Suppose the nominal
law has exactly uniform proper marginals and q<=q_cap, and a later law is at
TV distance at most rho. For 0<=rho<=1/2 the worst fixed-order mean is exactly
35/4+20q_cap+30rho: choose q=q_cap and transfer mass rho from first-success
worlds to all failure. The same support gap holds after drift. Thus the exact
robust fallback frontier is

    20q_cap + 30rho + 4alpha <= 1/4.

If q_cap is a valid statistical upper bound, this consequence inherits its
coverage conditional on the drift assumption. For alpha=1/32,q_cap=0, the
drift allowance drops from 1/120 to 1/240. No extra confidence factor is
needed merely to choose a point on this frontier; the source-coverage event
already supports it uniformly. This is a conditional robust application,
not an empirical certification that a future population stays within rho.

## 5. Optional extension: exact information dimension for fixed-price order edits

This section sharpens the declared consumer family, rather than claiming that
every cascade needs the full execution law. The equal-cost rank is a
specialization of Gasanova and Nicklasson's maximal-chain theorem (theorem 3.4,
2024); see the [focused comparison](../literature/05_f13_case_comparison.md).
The weighted kernel and consumer extensions below are locally derived, with
priority and useful distinctiveness still unestablished.

### 5.1 Fixed positive attempt costs and full orders

Let k>=2, c_i>0 be fixed rational attempt costs, M>=0 a fixed unresolved
penalty, and permit every permutation pi of *all k* reset procedures. Known
constants are free; summary rank is measured on the simplex's direction space,
with arbitrary decoding allowed after the linear measurement. The
consumer asks for every exact mean cost C_pi, equivalently all its rational
threshold answers. On the full joint-law simplex, the minimum rank of a
linear summary preserving those numeric queries is

    2^k-k.

Preserving every pairwise mean-cost difference among full orders needs rank
2^k-k-1. This second statement concerns numeric comparisons; it is not a
minimal representation theorem for the single optimal-order label. Neither
claim covers stateful procedures, a smaller source, arbitrary encodings, or
varying prices. For k=1 the numeric rank is one if M>0 and zero if M=0.

These lower bounds assume later answers come from the retained summary and
public model parameters alone. If full source data or execution traces remain
retrievable, ordinary reacquisition/recomputation is an available repair whose
cost must be charged. A receipt containing that extra data changes the retention
contract; a source fingerprint binds identity but does not by itself reconstruct
discarded values. Exact real-coordinate rank also says nothing by itself about
serialized byte size, coefficient conditioning or computation time.

Proof. Use all nonempty subset moments as coordinates, an invertible linear
coordinate system on the simplex's direction space. Write v_A for a direction
in those coordinates and v_empty=0. Interchanging adjacent procedures a,b
after prefix S changes the directional cost by

    (c_a-c_b)v_S + c_b v_(S+a) - c_a v_(S+b).                 (E)

All full orders are connected by adjacent interchanges. Thus all directional
costs agree iff (E)=0 for every proper S and distinct a,b outside it.

Let e_r(c_A) denote the r-th elementary symmetric polynomial in the costs
indexed by A. On all nonempty proper subsets, exactly the following directions
satisfy those equations:

    v_A = sum_(r=1..|A|) t_r e_r(c_A),                       (F)

with k-1 free coefficients t_1,...,t_(k-1); v_all is separately free. For
sufficiency use e_r(c_(S+a))=e_r(c_S)+c_a e_(r-1)(c_S) in (E).
For necessity start with S empty, obtaining v_i/c_i constant. Inductively
subtract already determined terms of (F). At subset size j the residual
vanishes on smaller sets and (E) says

    residual(S+a)/prod_(i in S+a)c_i
      = residual(S+b)/prod_(i in S+b)c_i.

The graph of j-subsets connected by one-element exchanges is connected, and
the costs are positive. Thus this ratio is a single coefficient t_j. This
proves the induction and shows that the common-cost subspace has dimension k.
Consequently the span of cost differences has rank (2^k-1)-k.

For a direction (F), the common contribution to any full-order mean is

    sum_(r=1..k-1) t_r e_(r+1)(c_all) + M v_all.             (G)

Each monomial of size r+1 is counted once when its last element is appended.
Requiring that common contribution also vanish imposes one nonzero linear
condition: if M=0, e_2(c_all)>0 since k>=2 and all costs are positive.
The numeric-query kernel therefore has dimension k-1, proving rank 2^k-k.
An interior probability law admits small perturbations along every such
direction, so these are actual simplex-relative lower bounds, not merely
formal polynomial dimensions.

For equal costs this reduces to a simpler argument: adjacent swaps isolate
differences of moments within one subset-size layer. Each proper layer loses
one common offset, and one base cost retains the combination of layer offsets
and the full-failure moment. The weighted proof above is needed for unequal
costs; simply repeating the equal-cost layer argument would be incorrect.

### 5.2 An ordinary summary attaining the bound

Fix reference order (1,...,k), with chain P_j={1,...,j}. Fit t_j recursively
to the observed chain moments by

    t_j = [m_(P_j)-sum_(r<j)t_r e_r(c_(P_j))] / prod_(i<=j)c_i.

For every other proper nonempty A retain

    r_A = m_A-sum_(r<=|A|)t_r e_r(c_A),

and retain B=C_(1,...,k). Chain residuals are zero by construction. These
are 2^k-k-1 residuals plus one base cost, all linear functions of the original
moments with known constant coefficients. Recover every full-order cost as

    C_pi = B + c_(pi_1)-c_1
             + sum_(j=2..k)c_(pi_j) r_(prefix(j-1)).

The removed elementary-symmetric contribution is common to all orders and
cancels by (G). This gives an explicit ordinary coefficient summary, not only
an existence result from matrix rank. It is permitted to the baseline with
the same source and checking requirements. Computing/storing it may cost
more than the small number k-1 of coordinates it saves versus a full law;
no performance improvement is implied.

### 5.3 Exactly which extensions restore the missing directions

With the same fixed c_i and **M>0**, permitting every ordered subset already
requires rank 2^k-1, without varying any prices. Singleton-policy costs reveal
m_i through c_i+M m_i. Inductively, the cost of an order ending at subset A
reveals M m_A after subtracting its known proper-prefix contributions. Thus
all subset moments are recovered. This strengthens the sufficient hypothesis
used in section 3.3: varying penalties is not necessary for this larger
policy family. If M=0 and all c_i>0, all ordered subsets recover every proper
moment but no full-failure moment, giving rank 2^k-2 instead.

For full orders alone, allowing arbitrary positive attempt-price revisions
isolates every proper prefix moment by differencing prices. If M>0, one full
cost then recovers m_all, again giving rank 2^k-1. If only M may change,
adding the single moment m_all to the fixed-price summary is sufficient;
for k>=2 it is an independent additional direction. The exact consumer
revision determines the additional information requirement.

Full loss distributions for every full order also recover all prefix-failure
moments when c_i>0 and M>0: the stopping positions have distinct cumulative
costs, and unresolved cost is strictly above the final successful cost. Every
subset appears as a prefix of some order. Thus all fixed-order mean costs
can be preserved more cheaply than all these distributions or all tail
consumers. When M=0, last success and exhaustion have the same cost, so their
separation cannot be inferred from that distribution; retain this exception.

### 5.4 A full mean-profile collision with a consequential risk revision

Take k=3, c_i=1, M=4. The following two exchangeable laws specify the mass
of *each* world with the given number of failure bits:

| Number of failures | Population P+ | Population P- |
|---|---:|---:|
| 0 | 29/128 | 3/128 |
| 1 (each of three worlds) | 7/128 | 25/128 |
| 2 (each of three worlds) | 21/128 | 11/128 |
| 3 | 15/128 | 17/128 |

Both are normalized and nonnegative. Single moments are 1/2 in both;
pair moments are 1/4 +/- 1/32 and the full moment is 1/8 -/+ 1/128.
Every full-order mean is therefore

    1+1/2+(1/4 +/- 1/32)+4(1/8 -/+ 1/128) = 9/4.

Keeping the exact mean of every one of the six full orders cannot distinguish
these populations. Yet an unresolved-rate cap of 1/8 is satisfied only by P+.
At CVaR confidence alpha=7/8, the worst 16/128 probability mass has average
27/4 under P+ (15 parts at loss 7 and one at loss 3), versus 7 under P-.
A risk allowance strictly between those values separates the consumers.
This is a collision of complete *mean profiles*, not complete loss laws.

These two populations are outside the exact-uniform-proper-marginal submodel
of 3.4: their pair moments differ from 1/4. The collision therefore does not
contradict that submodel's one-parameter sufficiency. The eight actual native
task contexts realize both laws, but the old fixed-prefix metalevel premises
must be changed before drawing a native performance conclusion about them.

The perturbation follows the kernel of 5.1 and scales to a family about any
interior law for sufficiently small changes. Its relevance is to revision of
retained guarantees; its generic tools are ordinary Boolean moments, finite
path semantics and linear sufficiency. Priority, useful distinctiveness and
an empirical application advantage remain separate questions.

### 5.5 Assumption challenge: free procedures change the rank

The positive-cost hypothesis matters when some work is treated as already
paid for. Let r procedures have positive attempt costs and z=k-r have zero
cost, still with reset behavior and all full orders available. For r>=1 the
rank of the numeric mean profile is

    2^k-2^z-r+1       if M>0 or r>=2,
    2^z-1            if M=0 and r=1.

If r=0, it is one for M>0 and zero for M=0. The rank of all order differences
is 2^k-2^z-r for r>=1 and zero for r=0. These are source-relative linear
information ranks, not lower bounds on computational time or on policy labels.

Proof from the same exchange equations. If a has positive cost and b has
zero cost, (E) reduces to v_(S+b)=v_S whenever S excludes a,b. Therefore for
every subset missing a positive-cost procedure, its common-profile kernel
coordinate depends only on the positive-cost members: remove zero-cost
members one at a time while retaining a missing positive index. A set of only
zero-cost indices has v_S=v_empty=0. On proper subsets of the r positive
indices, the previous elementary-symmetric induction leaves r-1 parameters.

Moments of subsets containing *every* positive index, apart from the full
set, never appear in an attempted-cost term: only zero-cost procedures remain
to be attempted. They contribute 2^z-1 invisible coordinates. The full moment
contributes one further coordinate before the common-cost condition. Hence
the order-difference kernel has dimension (r-1)+(2^z-1)+1, giving its stated
rank on the 2^k-1 dimensional simplex. A numeric base cost adds one condition
iff M>0 or there are at least two positive costs. If r=1,M=0, an order placing
that sole costly procedure first has constant cost, so it adds no direction.
The r=0 case is immediate from C_pi=M m_all.

For example, with three procedures, costs (0,0,1) and M>0, the mean-profile
rank is four, rather than the positive-cost value five. The costly procedure's
position exposes exactly the failure moments of the free procedures preceding
it, plus the terminal full-failure moment. This does not license treating
current receipt checking as free: that is a cost-model assumption to justify,
especially after source revisions. Sunk acquisition and fresh audit remain
separate.

### 5.6 Strong ordinary control under an independence assumption

The full-simplex rank bounds are inapplicable if the execution law is
independently factored. With independent failure probabilities f_i, all subset
moments are products of the k marginals. A fixed mean cost is computed from
those products. For positive costs and positive success probabilities,
an adjacent exchange after a prefix changes cost by the prefix-failure
probability times

    c_a(1-f_b)-c_b(1-f_a).

Thus sorting by increasing c_i/(1-f_i) gives an optimal full order; procedures
with no chance of success go last. M does not affect that order, because
full-exhaustion probability is order-independent. If stopping unresolved is
allowed, adding a final procedure changes cost by the preceding failure
probability times c_i-M(1-f_i). An optimal policy uses the sorted procedures
with c_i/(1-f_i)<M; equality can stop earlier. This statement allows zero
prefix probability and ties to make multiple policies optimal. It does not
claim every optimal policy has this form.

If each f_i independently ranges over a known interval, the worst case for
every fixed policy is simultaneously its upper-endpoint vector: every term
in the path-cost expression is monotone in failure probabilities. The same
ordinary sorting calculation therefore solves this rectangular independent
robust policy problem. Treating continuously uncertain probabilities as
native multiplicative terms would still exceed the adopted CPWA fragment;
this ordinary solution is not denied to the baseline because of that syntax.

Dependence invalidates the context-free sorting rule. With equal unit costs,
consider four task types, where the listed procedures succeed:

    {A,B}: mass 3/10; {B}: mass 1/5;
    {A,C}: mass 3/10; {C}: mass 1/5.

A has the largest marginal success probability 3/5, versus 1/2 each for B,C.
Running A first, then the better remaining procedure, costs 8/5 on average.
Running B then C costs 3/2 and resolves every task. A greedy marginal rule is
therefore inferior even in this small actual-trace family. With dependence,
the adjacent-exchange comparison instead uses success probabilities
conditional on the whole failed prefix; those can change with the prefix.
An exact finite policy search using the joint table remains the strong
ordinary control. The example diagnoses the independence/greediness
restriction, not a defect in all ordinary scheduling methods.

### 5.7 Exact uncertainty remaining behind a complete mean profile

The collision in 5.4 extends to an exact identified interval. Suppose k=3,
c_i=1, M>=0, every full-order mean is B, and the known singleton moments all
equal x. Equality of means for orders beginning with the same index forces
their pair moments to agree. Hence every pair moment is y, the full moment
is t, and, writing b=B-1, y=b-x-Mt. Moment inversion gives the mass of each
world with zero, one, two and three failures respectively as

    1-6x+3b-(3M+1)t,
    3x-2b+(2M+1)t,
    b-x-(M+1)t,
    t.

These constraints characterize the entire fiber, rather than a guessed
exchangeable subclass: equal singleton and pair moments and one full moment
determine the joint law. Nonnegativity gives its sharp interval

    max(0,(2b-3x)/(2M+1)) <= t
      <= min((b-x)/(M+1),(1-6x+3b)/(3M+1)).

An empty interval refutes the supposed summary. Every point of a nonempty
interval yields a normalized law with exactly that retained information.
For B=9/4, x=1/2, M=4 this is [1/9,7/52]. The best scalar reconstruction of
the unresolved rate has worst absolute error 11/936, half the interval width.
A cap below 1/9 fails for every law; one at least 7/52 holds for every law;
strictly between them, compatible laws give opposite answers.

Changing only M to M+Delta changes every full-order mean to B+Delta*t.
The sharp new mean interval follows by multiplying the displayed t interval
and respecting the sign of Delta. Its minimax reconstruction error is
|Delta|*11/936. With unbounded price revisions this error is unbounded despite
perfect preservation of every old mean. A declared bounded revision range
gives the corresponding finite guarantee.

For the numerical fiber above, each order has loss probabilities

    loss 1: 1/2; loss 2: 4t-1/4;
    loss 3: 3/4-5t; loss 7: t.

Increasing t replaces five units of mass at loss 3 by four at loss 2 and one
at loss 7. This is a mean-preserving spread, so every convex loss functional
increases. Direct tail integration gives, for alpha>1/2,

    CVaR_alpha = min(2+3/[4(1-alpha)], 3+4t/(1-alpha), 7).

For alpha<=1/2 it is (9/4-alpha)/(1-alpha). In particular, every compatible
law has the same CVaR through alpha=25/36. At alpha=7/8 the sharp range is
[59/9,7], so reconstructing that risk value has minimax absolute error 2/9.
These are exact finite uncertainty ranges computed by an ordinary joint-law
control. They are not a claim of a deployment advantage: section 4.8 explains
why the cheap actual fallback makes these high-risk distinctions irrelevant
to its replacement test.

### 5.8 Loss distributions with zero-cost procedures

For r>=1 positive-cost procedures and z=k-r zero-cost procedures, retaining
all full-order loss distributions requires linear rank

    2^k-2^z       if M>0,
    2^k-2^z-1     if M=0.

Here a distribution is retained as its finite probability vector on the known
cost levels; this is a linear observation of the execution law. If r=0, the
rank is one for M>0 and zero for M=0.

To prove necessity, take any nonempty subset A missing a positive-cost index.
Choose an order with prefix A and a positive-cost procedure immediately next.
The probability of a total loss strictly above the cumulative cost of A is
exactly m_A. All successes up to that point cost at most that amount; all
later paths incur the next positive charge. For M>0 the separately highest
unresolved cost also reveals m_all. These moments are independent simplex
coordinates. There are 2^k-2^z-1 such nonempty A, plus m_all when M>0.

For sufficiency, path probabilities at distinct cost levels are differences
of those same prefix moments. Once every positive-cost procedure has run,
subsequent zero-cost successes have the same cumulative charge; their timing
cannot be distinguished by the loss. Only the full unresolved event can be
separated when M>0. No other moments are needed.

Compared with 5.5, upgrading all fixed-order means to all loss distributions
adds r-1 independent directions when M>0. With M=0 it adds r-2 when r>=2,
and zero when r=1. In particular, with just one charged procedure the full
mean profile already determines every full-order loss distribution. A claim
that tail revisions necessarily demand more information must preserve its
cost assumptions; treating most work as free can remove that gap entirely.

### 5.9 Approximate costs, policy dominance and a smaller useful question

Exact rank can be a poor proxy for the effort needed for a useful decision.
Let Z be a set of low-cost reset procedures and let s=sum_(i in Z)c_i. Round
their attempt costs down to zero, leaving outcomes, positive costs and M
unchanged. On every world, for every fixed order, original loss minus rounded
loss lies in [0,s]. Thus every mean and every CVaR at 0<=alpha<1 differs by
at most s, without a factor 1/(1-alpha). This follows from pointwise order and
translation: X_zero<=X_true<=X_zero+s. The conclusion is uniform over any
source of joint laws sharing those pathwise semantics.

In the rounded problem, moving a free procedure ahead of a paid one can only
reduce loss on each world: it can stop earlier without a charge. Therefore
an optimal full-order policy puts all Z first. Their internal order is
irrelevant at zero cost. After they all fail, only the remaining r procedures
need ordering. Their joint conditional law together with P(all Z fail) is
represented by the 2^r unnormalized world masses on that event. If this event
has probability zero, all such policies have zero loss. There are at most r!
paid orders to compare. Retaining every policy's original full mean profile,
whose exact rank can still be exponential in k, solves a much larger question.

Choose an optimal rounded policy pi_0, and let pi_* be optimal for the true
costs in the same full-order family. For any fixed mean or CVaR objective V,

    V_true(pi_0) <= V_zero(pi_0)+s
                 <= V_zero(pi_*)+s <= V_true(pi_*)+s.

The approximation regret is s, rather than the generic 2s, because rounding
was one-sided. Supremizing each objective over a common uncertainty source
preserves these inequalities. This is an ordinary control and applies only
when costs change without changing successes or history effects. Free source
inspection, fresh receipt checking, extra fallback permissions and experimental
acquisition cannot be hidden in the rounding assumption. The constant is sharp
as a supremum even for a mean: one cheap procedure costs s and succeeds with
probability p, and a paid procedure always succeeds at cost C. Rounding the
first cost to zero strictly prefers it first when p>0. If s>pC, the true best
order instead starts with the certain procedure, and the regret is s-pC,
which approaches s as p tends to zero. This does not require a bad tie rule.

At the actual three-search prices c_i=5 and a quarter-unit improvement margin,
rounding even one attempt cost to zero is not an admissibly small perturbation.
The approximation result is a possible control for a more heterogeneous
future family, not a saving demonstrated by the current fixture.

For arbitrary cost edits Delta_i at fixed outcomes and a full order pi, a
sharp uniform absolute path bound is the maximum of the absolute cumulative
prefix edits and |sum_i Delta_i+Delta_M| for exhaustion. Across all full
orders it is max(P,N,|P-N+Delta_M|), where P sums positive attempt edits and
N sums magnitudes of negative ones. Every possible successful prefix and
the unresolved path is realizable on the full Boolean source. The same
bound controls means and all CVaRs under the shared-world coupling. It is
not a guarantee for changed outcome laws or changed executable behavior.

Changing only M leaves all pairwise full-order mean differences unchanged:
the common term Delta_M*m_all cancels. The full mean values still need m_all
for that revision (5.3). Consequently preservation of numeric values and
preservation of the best-order label must not be conflated, even before
allowing approximation.

This identifies a more useful discriminator for later research: do information
retention and revision guarantees change the best attainable decision at a
meaningful margin, once cheap approximations and dominated policies are
removed? The present exact dimension result alone does not establish that.

## 6. Shared result, evidence boundaries and contribution assessment

The cases share a prospective contract: identify the retained information,
the next permitted experiment or program edit, the consumer to be answered,
the current source/version identity, and the costs of obtaining and checking
evidence. A guarantee is transferable only when compatible worlds cannot
disagree on that consumer beyond the allowed error. That criterion is inherited
from C3; the case-specific calculations above supply its consequences.

| Question | Scientific family | Staged reasoning family |
|---|---|---|
| What is computed from premises? | Signed residual bounds, shared-target cancellation and sample-priced replacement; optional posterior error after a new sample. | Prefix-dependent expected work and unresolved cost, followed by actual policy selection and later native proof attempts. |
| What old information can fail? | Five old nodes miss v; retaining only the old integral estimate also loses nuisance directions needed by a later sample. | Proper marginals miss full failure dependence; every old mean can still miss a changed tail consumer. |
| What strong ordinary method suffices? | Interpolation, source support functions and a summary designed for the next measurement. | Joint execution data, source inspection, exact finite policy selection and the cheap-fallback risk reduction. |
| What extra premise improves a guarantee? | A calibrated discrepancy/noise bound, shared measurements, or a frozen future sample location. | Reset behavior, a valid population model, constrained drift, or a uniform gap below the fallback cost. |
| What cannot be inferred? | Absolute adequacy from a relative certificate, or model validity from finite samples. | Theoremhood from a failed search, calibration from self-report, cyclic stability from staging, or total runtime from emitted nodes. |

The resulting findings are substantive at case-study scope: exact acquisition
and retention tradeoffs, weighted cost-profile dimensions and their zero-cost
exceptions, a sharp risk-information fiber, and ordinary simplifications that
remove apparent information requirements for useful decisions. They extend
the old isolated two-bit witness. However, quadrature failure subspaces,
metareasoning, portfolio scheduling, Boolean moments and linear sufficiency
are established. The equal-cost rank has a direct maximal-chain antecedent.
The additional weighted and revision-specific calculations have neither an
exhaustive priority review nor demonstrated practical distinctiveness.

**Project-level novelty remains NOT YET SUPPORTED.** A/B's scoped readiness
passes remain intact; these case results do not pass C/D. The next selected
step should be the reserved C4 reconsideration before F14, with a concrete
application margin and the strongest ordinary combination as its discriminator.
More fixtures of the same easy proof-search source or a held-out test of its
already displaced speed claim would not resolve that question.

The [focused comparison](../literature/05_f13_case_comparison.md) records the
checked antecedents. Executable evidence and its failures are reported in the
[work record](../work_logs/F13_2026-10-04_S1.md). These are development cases,
not the frozen empirical challenge, a generalization result, or an independent
proof-assistant verification.
