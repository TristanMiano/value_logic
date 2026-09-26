# F04 S3 — Compressed evidence for paired revision

Status: candidate discrimination, not a selected calculus, gate, or general
reflection theorem. Session 2026-09-26-S3. Source revision:
`e66c1aed6a700e1c59455140f4a6e046d0736b95`.
Prior construction: [S2](01a_nonlinear_and_reflective_reconstruction.md).

The question in this continuation is deliberately narrower than choosing the
whole calculus: **what information is sufficient to check a useful change of
policy, and what information is lost when we retain only that check interface?**
We use the already-defined reflective controller rather than starting a new
model. Costs below are expectations with an explicitly fixed interpretation.
No empirical evidence that this interpretation is correct is supplied by the
algebra. All scalars are finite unless expressly stated otherwise.

## 1. Reconstruct the common-source semantics

A single report r in [0,1] makes the versioned controller choose branch A with
probability r and branch B otherwise. Conditional failure rates are a,b in [0,1].
The source uncertainty set K is nonempty and is the convex hull of a finite list
of such pairs. One actual pair, unknown to the controller, governs both the old
and the proposed policy. The expected failure and declared total cost are

    H_(a,b)(r) = a r + b(1-r),
    J_(a,b)(r) = H_(a,b)(r) + k r = b + (a-b+k)r,

where k>=0 is a fixed branch-A resource cost in unit-failure-cost units.
A report is valid when H_(a,b)(r)<=r for every (a,b) in K. This is feedback:
the bound being reported controls the behavior it bounds. It is not unrestricted
logical reflection. A valid report can still exceed the task's tolerance.

Write d=a-b. At a supplied vertex i, report validity is

    b_i <= (1-d_i)r.

When 1-d_i=0, a_i=1 and b_i=0, and the inequality is automatic. Otherwise its
threshold is b_i/(1-d_i). Thus define

    R_K = max({b_i/(1-d_i) : 1-d_i>0} union {0}),
    l_K = min_i(d_i+k),      u_K = max_i(d_i+k).

Every threshold lies in [0,1]. Checking vertices suffices because, at fixed r,
H(r)-r is affine in (a,b). The exact valid-report set is [R_K,1]. This restates
S2-C11 to make the following compression argument reproducible.

## 2. A three-scalar exact check interface

### F04-C16 — fixed-context report and paired-loss summary

Define the signed paired change

    B_K(r0,r1) = sup_(a,b in K) [J_(a,b)(r1)-J_(a,b)(r0)].

The common b cancels **inside each source model**, before taking a supremum.
For t=r1-r0,

    B_K(r0,r1) = u_K t  if t>=0,
                l_K t  if t<=0.                              (1)

Both formulas give zero at t=0. Hence (R_K,l_K,u_K) answers every report-validity
query and every signed paired-change query in this fixed policy family.

For a deterioration allowance delta>=0 we can retain even less information:

    c_plus  = max(u_K,0),
    c_minus = max(-l_K,0),
    D_K(r0,r1) = max(B_K(r0,r1),0)
               = c_plus ReLU(r1-r0) + c_minus ReLU(r0-r1).     (2)

Thus **(R_K,c_plus,c_minus) is sufficient for every report-validity and
nonnegative paired-deterioration test**, over a fixed K, controller version,
branch-cost convention, and units. These three numbers are a mathematical
summary; source identity and evidence provenance remain required metadata.

**Proof.** Subtract the two costs at the same (a,b) to obtain (d+k)t. Multiplying
by positive t selects the largest slope; multiplying by negative t selects the
smallest. The extrema of d over a finite convex hull occur at supplied vertices.
Taking the positive part yields (2). The report threshold was derived above.
This proves sufficiency, not an assertion that three physical memory words are
necessary. An unconstrained real number can encode multiple values. Square.

The exact deterioration is a directed pseudometric on reports: it is zero on
the diagonal, nonnegative, and satisfies

    D_K(r0,r2) <= D_K(r0,r1) + D_K(r1,r2).

Indeed ReLU(x+y)<=ReLU(x)+ReLU(y), and both coefficients in (2) are nonnegative.
It need not be symmetric or separate two reports in both directions. This is
a law for worst expected deterioration, not a metric on metaphysical truth.
A nonnegative inference-loss quantity can coexist with signed task values.

If R_K<1, the exact numerical query family recovers c_plus and c_minus by
querying (R_K,1) and (1,R_K) and dividing by 1-R_K. Valid-report answers recover
R_K. This makes the summary observationally exact for that declared family.
If R_K=1, only the report 1 is valid, so all valid-to-valid changes are zero:
claiming that the two rates must still be recoverable would be false. Similarly,
nonnegative-loss queries do not recover negative surplus discarded by clipping.
The richer signed interface can recover l_K,u_K when R_K<1.

### The summary does not determine the absolute cost optimizer

Let k=0 and compare

    K_A = conv{(1/4,3/4), (1/2,0)},
    K_B = conv{(1/4,3/4), (3/4,1/4)}.

Both have R=1/2, l=-1/2, u=1/2, hence the same two deterioration rates 1/2.
But their robust cost envelopes on the valid reports are

    F_A(r)=max(3/4-r/2, r/2),
    F_B(r)=max(3/4-r/2, 1/4+r/2).

The unique optimizer for A is r=3/4 with cost 3/8. For B it is r=1/2 with
cost 1/2. At r=1 the costs are 1/2 and 3/4. The derivation is just the
intersection of each pair of lines, followed by their slopes on either side.

Therefore the exact check summary does **not** determine absolute evaluation,
the robust optimizer, or all neural intervention interpretations. An optimizer
may use a separate richer objective representation and submit a proposed report
to the compact check interface. This is useful division of work, not proof that
the richer representation is unnecessary for every consumer.

## 3. Conservative summaries that still admit the old policy

### F04-C17 — approximate-rate guard with a retained baseline witness

Suppose independently accepted numerical certificates give

    R_K <= R_bar <= 1,
    c_plus <= C_plus,      c_minus <= C_minus,

with C_plus,C_minus>=0, and a retained certificate establishes that r0 is
K-valid. Let

    R_tilde = min(R_bar,r0).

Since both entries bound R_K from above, R_tilde also bounds it. A sufficient
feasible interval for a proposed report, under allowance delta>=0, is

    lower = max(R_tilde, r0-delta/C_minus) if C_minus>0,
            R_tilde                         otherwise;
    upper = min(1, r0+delta/C_plus)       if C_plus>0,
            1                               otherwise.      (3)

Every report in this interval is K-valid and has D_K(r0,r)<=delta. The interval
contains r0, so it is nonempty. If the inputs are the exact R_K and rates, (3)
is the exact admissible interval, not merely sufficient.

**Proof.** The rate expression C_plus ReLU(t)+C_minus ReLU(-t) dominates (2).
For t>=0 its inequality is the displayed upper constraint; for t<=0 it is the
lower constraint. Zero rates impose no constraint on their direction. Taking
[ R_tilde,1 ] ensures report validity. At r0 the deterioration expression is
zero and R_tilde<=r0. With exact quantities these implications are equivalences.
Square.

The baseline witness is material. A coarse R_bar can exceed r0 even though r0
is genuinely valid. Discarding that known validity and requiring r>=R_bar can
make the approximate guard empty at delta=0 when both rates are positive. For
K_A above, r0=1/2, R_bar=9/10 and rates 1/2 demonstrate this failure; retaining
the old certificate recovers the nonempty interval {1/2}. This does not justify
lowering R_bar without a valid same-context certificate for r0.

Rate uncertainty scales with the **size of the policy change**, rather than a
fixed charge for every check. For example let the nonempty slope range be
[-2/5,3/5], report floor 2/5, r0=3/5, and delta=3/50. The exact interval is
[9/20,7/10]. A coarser pair C_minus=1/2, C_plus=4/5 gives [12/25,27/40]. Both
contain r0; the latter is narrower but still permits changes. This slope range
and floor are realized by vertices (4/25,14/25) and (7/10,1/10) with k=0.

## 4. What an evidence restriction does to the summary

### F04-C18 — sound reuse is easier than exact updating

If valid new evidence supplies a nonempty K' subset K under the same policy and
cost semantics, then

    R_(K') <= R_K,  c_plus(K') <= c_plus(K),
    c_minus(K') <= c_minus(K).                              (4)

The old three-scalar certificate remains sound. It can fail to exploit new
information, but it cannot become optimistic merely because possible models
were removed. An evidence correction that expands or otherwise replaces K does
not have this guarantee. In particular, including (a,b)=(1,1) changes the valid
report floor to 1; an old floor 1/2 cannot authorize report 3/4 for that model.

**Proof of (4).** Every K-valid report is K'-valid. Each slope supremum over the
smaller nonempty set is no larger, including the supremum of the negated slope.
Positive-part clipping preserves these orders. No step presumes that the
selected robust optimizer stays the same or improves at each retained model.
Square.

**Exact updating is impossible from these scalars for arbitrary affine evidence.**
Use K_A and K_B from section 2, which have identical original summaries. Receive
the same evidence E={b>=1/8}. Exact intersection with the convex sets gives

    K_A' = conv{(1/4,3/4),(11/24,1/8)},
    K_B' = K_B.

For A, the original segment has parameterization
(a,b)=(1/4+t/4, 3/4-3t/4). The constraint says t<=5/6, yielding the new endpoint
(11/24,1/8). This endpoint must be created: deleting infeasible listed vertices
and taking their convex hull would not compute K_A intersect E correctly.

Both updated floors remain 1/2, but their maximum slopes are 1/3 and 1/2.
For the valid common reports r0=1/2, r1=3/4,

    D_(K_A')(r0,r1)=1/12,
    D_(K_B')(r0,r1)=1/8.

At allowance 1/10, A permits the change and B does not. Thus a deterministic
update procedure receiving only the old summary and this same evidence cannot
return the exact answers for both. The lost source correlation matters later.
This is a constructive obstruction, not a claim that all compression is bad.
Keeping the old certificate is sound; reopening only the needed maximum-slope
query would recover A's useful permission.

**A positive exact-update subfragment.** If the new evidence constrains only
the slope s=a-b+k to lie in [L,U], the slope image of convex K is already the
entire interval [l_K,u_K]. Provided the intersection is nonempty, the new image
is exactly

    [max(l_K,L), min(u_K,U)].                               (5)

Every value in this intersection has a preimage in K by convexity; that preimage
also satisfies the slope evidence. Thus paired-change rates update exactly from
l_K,u_K and the new interval. This needs untruncated signed endpoints; clipping
can discard which negative slopes were present. It does not need the whole K.

However, the report floor still need not update exactly. For K_A,K_B and the
same evidence a-b>=0, parameterizing by d yields

    A: b=3/8-3d/4,   d in [0,1/2],
    B: b=(1-d)/2,    d in [0,1/2].

The maximum of b/(1-d) is 3/8 for A and 1/2 for B. For A its derivative is
-3/[8(1-d)^2]<0, so the maximum is at d=0; for B the ratio is constant. Both
updated slope intervals are [0,1/2], but a report r=2/5 is valid only for A.
One update can therefore be exact for a paired-loss consumer while remaining
inexact for a report-validity consumer. Such capabilities need typed scope.

## 5. Generalize the check, not the whole object representation

The two-branch case has a one-dimensional policy coordinate. A broader finite
fragment lets a policy/control vector p in R^d have cost

    J_theta(p)=b_theta+g_theta^T p,                          (6)

where the same hidden theta is used when comparing policies. b_theta can range
without a finite bound. Supply a nonempty possible-slope set G containing all
g_theta allowed by the evidence. For a change v=p1-p0,

    sup_theta [J_theta(p1)-J_theta(p0)] <= h_G(v),
    h_G(v)=sup_(g in G) g^T v.                             (7)

Equality holds when G is exactly the image of the admitted source models.
Taking max(0,h_G(v)) gives a nonnegative deterioration allowance. If G is a
compact convex hull, every h_G(v) is finite and attained; this is not an
assumption that absolute costs have finite maxima.

### F04-C19 — finite directional premises and complete linear certificates

Instead of storing all G, retain finitely many verified directional bounds

    v_j^T g <= eta_j, j=1,...,m, for every admitted g.

They define the possible-slope enclosure

    P = {g in R^d : A g <= eta},  row j of A is v_j^T.

Require P nonempty. If the original source G is nonempty and every bound really
holds on it, this requirement follows; a witness of P's feasibility does not
establish empirical truth of those source bounds.

A sufficient certificate for the new query v^T g<=delta consists of

    lambda_j >= 0,
    A^T lambda = v,
    eta^T lambda <= delta.                                (8)

A checker needs only linear arithmetic, not a fresh evaluation of all source
models. Under the stated finite linear premises and nonempty P, (8) is also
**necessary** for the inequality to hold on every g in P. This is the classical
valid-inequality/Farkas certificate fact, proved below for clarity. It is not a
new completeness theorem for arbitrary Value Logic, RLL, or neural networks.

**Sufficiency.** Multiply each premise by its nonnegative lambda_j and sum.
Then v^T g=lambda^T A g<=lambda^T eta<=delta. Negative multipliers cannot be
used without separately supplied reversed inequalities. Square.

**Necessity, including the unbounded case.** Form the finitely generated cone

    C=cone{(v_1,eta_1),...,(v_m,eta_m),(0,1)} in R^(d+1).

Its members are precisely pairs (A^T lambda,eta^T lambda+t) with lambda,t>=0.
The cone is closed. One elementary justification: a conic combination can have
its active generators reduced to a linearly independent subset by subtracting
a suitably scaled linear dependence while retaining nonnegative coefficients.
For each independent subset, its generated cone is a closed orthant under an
injective linear map into a closed subspace. There are only finitely many such
subsets, so their union is closed. This argument permits redundant and zero
generators.

If z=(v,delta) is outside C, choose a closest point c in C. A nearest point
exists because C is closed in finite-dimensional Euclidean space (restrict the
minimization to a sufficiently large closed ball). Convexity of C gives
(c-z)^T(w-c)>=0 for every w in C. Using w=0 and w=2c yields (c-z)^T c=0.
Consequently y=c-z satisfies

    y^T w>=0 for all w in C,       y^T z=-||c-z||^2<0.

Write y=(x,t). The generator (0,1) ensures t>=0; the others imply
x^T v_j+t eta_j>=0. If t>0, g=-x/t satisfies A g<=eta, but v^T g>delta.
If t=0, A x>=0 and v^T x<0. Choose any g0 in nonempty P. Then g0-alpha x
lies in P for all alpha>=0 and v^T(g0-alpha x) tends to +infinity. Both cases
contradict validity of v^T g<=delta on P. Thus z belongs to C, giving (8).
Square.

The retained information determines a **best sound** bound through

    inf {eta^T lambda : lambda>=0, A^T lambda=v}.

When h_P(v) is finite, the preceding equivalence at delta=h_P(v) supplies a
minimizing certificate and equality with h_P(v). If no such lambda exists,
the nonempty enclosure has h_P(v)=+infinity. No efficiency theorem or solver
implementation follows just from this existence result. With rational input
data, rational feasible certificates can be obtained from a rational polyhedron;
our executable checks validate supplied rational certificates, not search them.

### A one-premise repair of a lost relation

Let G=conv{(1,-1),(-1,1)}. Marginal premises +/-g1<=1 and +/-g2<=1 enclose G
in the square [-1,1]^2. For v=(1,1), their best implied bound is 2, attained
at the spurious point (1,1). The actual h_G(v) is zero.

One extra valid relational premise, g1+g2<=0, gives the exact zero bound using
lambda=1 on that premise and zero elsewhere. There is no need to recover the
whole line segment for this query. Before repair, a certificate for bound zero
cannot exist: the feasible square witness (1,1) disproves it. This is an
example of genuinely inferential reuse of numerical premises, not merely
thresholding an independently evaluated composite.

The price is that the extra premise must itself be justified. Setting eta=0
because it would authorize the desired policy is not evidence. Independence
assumptions or a new model can invalidate the common-source relation even when
the old marginal bounds survive.

## 6. Composition, precision and neural reparameterization

### F04-C20 — directional certificates through a finite ReLU suffix

Let f be a continuous finite piecewise-affine scalar function on a convex
full-dimensional domain. Consider an admissible segment x+t v, 0<=t<=1. Suppose
a certified possible-gradient set G includes the affine gradients of every
region met by this segment (using adjacent regions for a segment lying on a
face). Then

    f(x+v)-f(x) <= h_G(v).                                 (9)

**Proof.** Partition [0,1] at the finitely many changes of the affine formula
along the segment. On subinterval i of length t_i, the change is t_i g_i^T v.
Continuity prevents a jump term at a boundary; tangential derivatives agree
across any face containing a segment piece. Summing gives a convex combination
of the numbers g_i^T v, each bounded by h_G(v). Their lengths sum to one.
This proves (9). A finer tube partition can use different sets G_i and bounds
sum_i h_(G_i)(t_i v). Square.

For a finite ReLU network with affine scalar output, the function has this
form. A softmax, log loss, squared error or true downstream utility need not.
Their composition needs an additional justified operation/gradient bound;
one must not infer an improvement in practical value from a change in a logit.
The neural calculation yields a cost-proxy guarantee only if f has that declared
interpretation. No learned interpretation or trained network is supplied here.

A single current activation pattern does not certify G for a perturbation.
For f(r)=ReLU(r-1/2), r0=1/4, r1=3/4, the current derivative is zero, but the
actual change is 1/4. The full gradient set {0,1} yields a valid bound 1/2.
Splitting at 1/2 yields the exact bound 0*(1/4)+1*(1/4)=1/4. Thus a sound
conservative certificate can be refined only where its margin is too loose.
Discovering all reachable regions may still be computationally expensive.
The mathematical bound is not an efficient general region-enumeration result.

For a function-preserving positive-rescaling/permutation matrix M on a hidden
representation, transport the suffix and displacement as

    x'=M x,   v'=M v,   f'(x')=f(M^(-1)x'),
    G'=M^(-T)G.

Then h_(G')(v')=h_G(v), by the pairing identity
(M^(-T)g)^T(Mv)=g^T v. Direction templates transform v_j'=Mv_j and keep eta_j.
A multiplier certificate lambda is unchanged:

    sum_j lambda_j v_j'=M(sum_j lambda_j v_j)=Mv=v'.

Hence its bound eta^T lambda is invariant. This extends the earlier neural
scale/permutation controls to a **certificate-bearing interpretation**, rather
than requiring that a particular neuron amplitude itself mean a cost. Keeping
v fixed while rescaling G would change the physical intervention and is not
this control. Neither observational invariance nor this algebraic transport
establishes that an ordinary trained network implements the proposed semantics.

### Finite-precision bounds belong to the certificate

If the true bound for template j is no more than eta_hat_j+e_j, where e_j>=0,
use those upper endpoints in (8). The certified cost is

    sum_j lambda_j eta_hat_j + sum_j lambda_j e_j.         (10)

The second term is not optional numerical formatting; it is the price of the
uncertain premises. A proof with many large multipliers can amplify a tiny
premise error. For one premise g<=1, a query 10g<=10 needs multiplier 10;
using an uncertified estimate 99/100 in place of 1 would falsely claim 99/10.
A radius 1/100 restores the correct bound 10. Conversely, not every certificate
needs the same uniform rounding penalty. The actual nonnegative coefficients
provide an explicit bound on the precision needed for that inference.

This is compatible with exact rational checking of supplied certificates.
With rational v, eta and delta, feasibility of the certificate constraints
admits a rational witness whenever it admits a real one: retain the tight
rational equalities at a feasible point, express their affine solution space
with a rational basis, then approximate the remaining free coordinates by
rationals closely enough to preserve all strictly slack inequalities. This
argument is an existence fact, not a certificate-search algorithm.

## 7. A proxy need only be aligned for the proposed change

### F04-C21 — directional proxy-error bridge

Let J_theta(p)=L_theta(p)+E_theta(p), where L is the measured or learned loss
proxy, J the intended task criterion, and E their unknown discrepancy. Suppose
on the named source set, for the same pair (p0,p1),

    L_theta(p1)-L_theta(p0) <= B_L(p0,p1),
    E_theta(p1)-E_theta(p0) <= B_E(p0,p1).

Then, pointwise in theta and hence uniformly,

    J_theta(p1)-J_theta(p0) <= B_L(p0,p1)+B_E(p0,p1).      (11)

The conclusion requires **no** bound on E_theta(p0) itself. It permits an
arbitrarily large common evaluation offset, provided changes in that error are
bounded as stated. Both premises require evidence; neither follows just from
using a conventional ML training loss or from the proxy being well calibrated
in some different task.

For the one-dimensional policy family, suppose the proxy slope lies in
[l_hat,u_hat] and the discrepancy has directional increments bounded by

    E_theta(r1)-E_theta(r0)
       <= e_plus ReLU(r1-r0)+e_minus ReLU(r0-r1),

with nonnegative e_plus,e_minus. Sound target deterioration rates are

    C_plus=max(u_hat+e_plus,0),
    C_minus=max(-l_hat+e_minus,0).                         (12)

Use (3) with these corrected rates and an independently certified report floor.
This is a scoped difference-error bridge; it is not a surrogate-risk calibration
theorem for every classifier or a definition of final utility.

**Worked nonnegative-loss example.** Let r in [0,1], z>=0 arbitrary, and

    L_z(r)=1+z-(2/5)r,
    E_(z,t)(r)=z+t r,  t in [-1/10,1/10],
    J_(z,t)(r)=1+2z+(-2/5+t)r.

All L and J are nonnegative and unbounded above as z varies; E has no uniform
absolute upper bound. Yet the change r0=1/2 to r1=3/4 has

    J(r1)-J(r0) in [-1/8,-3/40].

Thus it improves the intended criterion by at least 3/40 under the declared
proxy-error family. This is not evidence that such a family holds for real
neural predictions. It demonstrates the kind of relational certificate we
would need and why absolute loss prediction can be a stronger demand than the
practical comparison calls for.

Absolute-error certificates also work, but can be less informative: bounds
|E(p)|<=epsilon at both points imply B_E<=2epsilon, which need not vanish as
p1 approaches p0. A directional certificate can preserve an already valid
baseline with a tighter, displacement-sensitive penalty. It is an additional
assumption about error structure, not a free consequence of the pointwise bound.

## 8. Equal-information candidate comparison

Route A retains shared cost expressions and finite directional inequalities.
For the affine fragment, it checks a proposed update by (8), optionally with
precision correction (10). Finite signed-pair translations and RLL-like
residuals remain possible arithmetic encodings; this session does not emit a
full RLL proof of each certificate or adopt a universal signature.

Route B retains a joint lower-value functional, or equivalently a support
functional for the paired slopes. It answers the same query with h_G(v).
If it receives only the finite directional facts, its justified model set is
also P, and the best implied bound is the same h_P(v). If it receives all G
while Route A receives only coordinatewise bounds, a sharper answer demonstrates
unequal information, not an intrinsic superiority of its numeric carrier.

Both routes can use the three-scalar report/check interface in the fixed
one-dimensional model. Both must reopen information when an update falls outside
the supported exact-update fragment. Both can preserve old sound certificates
under genuine source restriction. Neither obtains empirical coverage, an
operational optimizer, or internal neural causal meaning merely by a change
of notation.

The concrete discrimination is therefore between **admitted operations and
retained evidence**, not a competition to store more unspecified structure:

| Question | Three-scalar checks | Finite template enclosure | Full joint source/function |
|---|---|---|---|
| Same-family report and deterioration | exact with named metadata | expressible with needed facts | exact in specified finite model |
| Absolute robust optimization | not determined | requires added objective facts | available via S2 finite search |
| Arbitrary affine evidence restriction | conservative reuse only | conservative reuse; selective new facts | exact intersection possible |
| Slope-interval restriction | exact paired rates with signed endpoints | exact when its constraints are represented | exact |
| Multi-coordinate policy change | outside the three-scalar interface | checked linear certificate, tight for enclosure | potentially tighter if more dependence retained |
| Nonlinear neural proxy intervention | needs further tube information | conditional gradient/tube certificate | still requires verification and causal grounding |

## 9. Reconstruction questions and scope

A fresh same-agent pass should check the cone proof's separation sign, the
nonempty-enclosure condition, clipped versus signed observables, the degenerate
R=1 case, and exact convex intersection rather than vertex filtering. The
paired quantities use the same hidden model; they are not differences of
separately optimized robust scores. The empirical validity of that common-source
premise and of a proxy-error family remains an explicit obligation.

The finite-template certificate fact and support-function arithmetic are standard
convex/linear-optimization constructions. The two-branch calculation is an
application of elementary affine geometry. Their purpose in F04 is to narrow
the candidate comparison and expose a useful tractable subfragment, not claim
priority for safe improvement, Farkas certificates, or neural Lipschitz bounds.
No permanent core, readiness gate, F05 work, or trained neural result is introduced.

## 10. Selective quantitative certificate repair

### F04-C22 — tolerate changed premises when their weighted effect fits the margin

Keep a fixed query v, template matrix A, source-variable meaning, and a checked
lambda>=0 with A^T lambda=v. At one stage its premise bounds eta give
b=lambda^T eta<=delta. If the currently justified bounds change to finite eta',
the very same arithmetic proof yields

    b' = lambda^T eta' = b + lambda^T(eta'-eta).            (13)

It remains sufficient at the old tolerance precisely when b'<=delta. Thus a
sufficient local reuse condition is

    lambda^T(eta'-eta) <= delta-b.

This permits some premises to change; it is stronger than the merely sufficient
rule that none of the read premises change. Bounds with zero multiplier do not
participate in this certificate. A revoked premise with positive multiplier
requires a new bound or a different proof, not silently keeping its old number.
The condition is necessary only for **this fixed certificate's numerical test**,
not for the semantic conclusion or existence of a different certificate.

For example a relation g1+g2<=0 certifies v=(1,1) at tolerance 1/10. Replacing
its justified upper bound by 1/20 preserves the guarantee. Revoking unrelated
coordinate bounds has no effect on that proof. Conversely, if the relation is
revoked but separate facts g1<=0 and g2<=0 remain, a new two-premise certificate
still proves the zero bound. This is why 'a used premise was invalidated' should
reopen a proof obligation rather than automatically assert the target false.

**Proof.** The equality A^T lambda=v is unchanged, and every retained premise
is justified in the current source interpretation. Multiplying and summing is
still sound; expansion of the dot product gives (13). Other certificates are
not constrained to have the same support. Square.

The contrast with phase one's exact disjoint-read/write locality is useful:
there, disjointness preserves a diagnostic; here a numerical tolerance can
preserve a conclusion despite changes in contributing bounds. This is a
specialized certificate-sensitivity calculation, not an unqualified novelty
claim or a replacement for phase-one provenance and mode checks.

### Changing the template directions is a different kind of revision

If the new justified premises use A' rather than A, the old coefficient vector
need not derive the same query. Let w=v-(A')^T lambda. Then, for an independently
justified current possible-slope enclosure G',

    v^T g <= lambda^T eta' + h_(G')(w).                    (14)

This follows by adding the residual pairing w^T g. If G' has ||g||<=M in a
specified norm, Holder's bound gives h_(G')(w)<=M||w||_*; if it has unrestricted
directions, even a tiny nonzero w can have infinite support. The correction must
not be omitted as a numerical rounding detail. Exact transformed templates in
section 6 have w=0 after transforming the query too, so no penalty appears.

For a simple failure, the sole true premise is g1+epsilon*g2<=0, with
unrestricted g2 and epsilon>0. Reusing its coefficient 1 as a proof of g1<=0
is invalid: (g1,g2)=(1,-1/epsilon) meets the premise. If one also knows |g2|<=B,
the same premise instead proves g1<=epsilon B, a valid finite repair. Both
statements remain true for arbitrarily small positive epsilon.

### Changing the task over time needs an explicit comparison bridge

The per-step paired policy bounds telescope under a fixed cost interpretation,
as in S2. For actual functions J_t that themselves change, the exact identity is

    J_n(p_n)-J_0(p_0)
      = sum_t [J_t(p_t)-J_t(p_(t-1))]
        + sum_t [J_t(p_(t-1))-J_(t-1)(p_(t-1))].           (15)

So policy-change bounds delta_t and separately justified environment/criterion
bridges gamma_t give a total bound sum_t(delta_t+gamma_t). Without the latter,
no cross-time bound follows: a cost that changes from 0 to 100 while the policy
stays fixed has zero policy-change deterioration but a total increase of 100.
This does not prevent a useful within-current-context policy comparison, even
when a common time-varying offset makes the cross-time value unknowable.
All stochastic coverage claims for many stages require their own joint validity;
the finite algebra itself provides no sampling guarantee.

## 11. Fresh same-agent reconstruction record

The derivation was rechecked from the underlying equations before implementation.
The checks below are mathematical self-review, not an independent reviewer:

* The threshold denominator 1-a+b vanishes only at (a,b)=(1,0), where every
  report is valid. A source set with a=1 and b>0 instead forces r=1. These
  different endpoint cases prevent an erroneous unconditional three-coordinate
  minimality claim.
* The clipped paired query reverses the least slope on a negative displacement.
  Multiplying by a positive cost weight changes slopes, not the report floor.
  Changing k is a new context for fixed-rate certificates.
* The illustrative approximate interval has floor 2/5. Its first realization
  vertex was corrected during derivation to (4/25,14/25); the initially proposed
  (1/5,3/5) would have floor 3/7. The interval arithmetic was unaffected, but
  the wrong realization was not left as a premise.
* The b>=1/8 evidence intersects a **convex segment**, producing (11/24,1/8).
  Merely deleting the excluded original vertex would exaggerate what the
  evidence establishes. The exact paired bounds 1/12 and 1/8 have a strict
  separating allowance 1/10.
* In the cone proof, separation uses y=c-z, so a positive last coordinate gives
  feasible g=-x/t. At t=0 the feasible ray is g0-alpha*x, not g0+alpha*x.
  A nonempty starting polyhedron is indispensable. The degenerate query v=0
  has support zero and cannot support a negative bound in a nonempty model.
* Finite support facts concern possible slopes, hence upper enclosures are
  conservative for guarantees. They are not a list of achievable policies.
  An optimizer still has to produce one common available report/policy.
* The tube bound needs all traversed affine pieces; an exact certificate for
  one observed activation cell is not a certificate of its continued validity.
  A neuron rescaling must transport both the gradient and intervention.
* Policy improvements telescope only with a common interpretation, or with the
  explicit drift term in (15). Better current robust scores alone do not
  replace any of these paired bounds.

These checks narrow the candidates and sharpen their tests. They do not complete
F04's protected D60 requirement, select the winner, or begin the later reasoner.

## 12. End-to-end finite certificate example

To ensure that the general certificate interface actually connects back to
reflection, let the only source facts be

    a+b <= 9/10,      -a <= 0,      -b <= 0.

Their nonempty triangle lies in [0,1]^2. The hidden rates need not be estimated
separately, and the triangle includes correlated alternatives. Take k=0,
old report 3/5, new report 1/2, and allowed paired deterioration 9/100.
In the source-coordinate order (a,b), the three queries and multiplier vectors
against the three displayed premises are

| Claim | Query vector v | lambda | Certified upper bound | Required ceiling |
|---|---|---|---|---|
| Old report bounds its own failure | (3/5,2/5) | (3/5,0,1/5) | 27/50 | 3/5 |
| New report bounds its own failure | (1/2,1/2) | (1/2,0,0) | 9/20 | 1/2 |
| New expected cost minus old | (-1/10,1/10) | (1/10,1/5,0) | 9/100 | 9/100 |

Each equality A^T lambda=v can be inspected directly, and all multipliers are
nonnegative. The last row is obtained by subtracting the **same model's** costs,
not subtracting the robust values. At (a,b)=(0,9/10), actual expected failure
increases from 9/25 to 9/20, exactly 9/100. At (9/10,0) it decreases from
27/50 to 9/20. The robust score improves, but the paired guarantee correctly
retains the possible deterioration at the first model.

The current source relation, the report-to-policy version, loss units, and
allowance are still explicit premises. The arithmetic proof does not prove
these empirical premises or authorize unrelated actions. This small example
shows actual reuse: one relation and two sign facts certify the old report,
the new report, and its permitted change without enumerating the possible
sources again or learning their exact values.

### Additional context boundary: changing the resource weight

Clipped rates are sufficient at a **fixed** k, not for arbitrary future changes
of that weight. Consider

    K_C=conv{(1/4,3/4),(1/10,1/2)},
    K_D=conv{(1/4,3/4),(1/10,1/5)}.

At k=0 both have R=1/2 and clipped rates (c_plus,c_minus)=(0,1/2).
Their largest signed slopes are respectively -2/5 and -1/10, information that
clipping discarded. Change only the known resource weight to k=3/10. Now the
largest total-cost slopes are -1/10 and 1/5. Moving r from 1/2 to 3/4 has
upper expected-cost changes -1/40 and 1/20. A zero-deterioration permission
therefore survives only for C. Report validity is unchanged because its failure
probabilities and report-to-policy semantics were not altered.

The explicit checks are: the shared first vertex supplies threshold 1/2 and
least unweighted slope -1/2; the other thresholds are 5/14 and 2/11, respectively.
Thus the stated old summaries genuinely agree. If one retains the *signed*
unweighted endpoints, changing k translates them and recomputes the clipped
rates exactly. A summary must say which future context operations it supports.

Multiplying the entire cost by a known alpha>0 instead multiplies both
comparison rates and all loss allowances by alpha; the probability report floor
does not change. Adding any source-dependent offset that is identical for the
old and new policy cancels within the paired query. That offset is not necessarily
harmless for absolute robust optimization: it can change which source model is
worst, as the different envelopes in section 2 illustrate. 'Common' here means
shared by the two policies within one model, not a universal constant across all
models.

For a multi-term loss with changing weights, the same issue moves from signed
endpoints to directional support of the **joint** vector of component slopes.
Separate marginal slope bounds need not preserve a weighted sum. The opposing
slopes (1,-1) and (-1,1) in section 5 give sum zero but independent marginal
maxima summing to two. This connects the finite certificate question to losses
built from multiple terms without identifying their empirical or normative roles.
