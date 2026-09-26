# F04 S4 — Small proofs, reusable proof families, and precision

Status: **candidate-discrimination work; F04 remains partial**.
Source revision: `115216e15496ffeb29065e4adb503d6c918ab99a`.
Prior note: [S3 compressed revision](01b_compressed_revision_certificates.md).
No permanent calculus, Gate A decision, or later-task implementation is made here.
[Source-use boundaries](F04_S4_sources.md) and the
[session record](../work_logs/F04_2026-09-26_S4.md) accompany this note.

This pass separates four resource questions that the last pass left open:
(1) how many premises one quantitative proof needs, (2) how much numerical
precision those premises need, (3) how many proof alternatives must be retained
for future evidence, and (4) whether an uncertain collection of premises can
be safely summarized before an inference. The same evidence is supplied to the
arithmetic-certificate and value-functional routes throughout.

## 1. Fixed context and the inherited finite-linear interface

Fix a versioned policy family with expected task cost

    J_theta(p) = b_theta + g_theta^T p.

The same theta governs the compared policies. The offset b_theta can be
unbounded. A change v=p_new-p_old has cost change g_theta^T v. Current justified
source inequalities enclose possible slopes in

    P(eta) = {g in R^d : A g <= eta},

where m,d are positive integers and A has m rows a_i^T. All matrix entries, right-hand sides and query
coordinates are finite. P(eta) must be nonempty; its feasibility is not proof
that the actual target obeys the source inequalities. Scope, units, versions,
source identities and evidence modes remain separate side conditions.

S3-C19 established the following ordinary finite-linear fact, including its
nonempty-set hypothesis:

    h_eta(v) = sup_{g in P(eta)} v^T g <= delta

iff there is a supplied certificate

    lambda >= 0,    A^T lambda = v,    eta^T lambda <= delta.       (1)

When the support value is finite, its exact value has an attaining certificate.
When v is outside the cone of A's rows, no finite bound exists on a nonempty
P(eta). These statements are about this fragment, not general completeness of
Rational Lawvere Logic or any proposed Value Logic.

## 2. F04-C23 — sparse optimal certificates and exact update libraries

### 2.1 A tight proof needs at most rank(A) active source rows

Assume P(eta) is nonempty and h_eta(v) finite. Then an optimal certificate in
(1) exists with linearly independent positive-support rows. In particular it
uses at most rank(A) <= d premises. For v=0, the empty certificate suffices and
the exact bound is zero.

**Proof.** Choose an optimal certificate with the fewest positive entries;
existence of an optimum is inherited from (1), and the possible support sizes
are finite. Let I be its positive support. If the rows indexed by I are
linearly dependent, choose a nonzero vector c supported on I with A^T c=0.
For sufficiently small t of either sign, lambda+t c remains nonnegative and
has the same query vector. Optimality then implies eta^T c=0: otherwise one
of the two signs strictly improves the objective.

Choose the sign of c so some c_i>0 and set

    t0 = min_{i:c_i>0} lambda_i/c_i.

The certificate lambda-t0 c is nonnegative, has the same query and objective,
and has fewer positive entries. This contradicts the choice of lambda. Thus
its support rows are independent. For v=0, feasibility of P implies every
certificate has eta^T lambda>=0; lambda=0 attains zero. QED.

This is a sparse **arithmetic witness**, not a claim that the empirical evidence
underlying a row has a short proof, or that the row's provenance can be omitted.
It also is not a sparsity claim for disjunctive reasoning developed below.

### 2.2 A finite reusable library answers every feasible RHS update exactly

For fixed A and v define B(A,v) to be all nonnegative solutions A^T lambda=v
whose positive-support rows are independent, including zero when v=0. There
is at most one such solution for each independent support set. Consequently

    |B(A,v)| <= sum_{k=0}^{rank(A)} binomial(m,k).                  (2)

Whenever P(eta) is nonempty and v belongs to the row cone,

    h_eta(v) = min_{lambda in B(A,v)} eta^T lambda.                 (3)

**Proof.** Every member supplies an upper bound by (1). Section 2.1 supplies an
optimal member for each feasible eta; the set depends only on A and v. Fixed
independent support determines its coefficient vector uniquely. Counting the
possible support subsets proves (2). QED.

Thus exact updating under arbitrary changes of the bounds eta is possible with
a finite library for this fixed-template fragment. This is a positive counterpart
to S3's failure of exact updating from only three compressed scalar answers.
The price is retaining a sufficient family of proofs, not recovering all hidden
target values. Adding a source direction, changing A, or changing v is outside
this fixed-library result. An old lambda can be reused only after checking its
new query identity or adding the residual correction from S3-C22.

### 2.3 Certificate count is not coefficient size

For rational inputs an independent-support certificate is rational. Select k
independent coordinate equations for its k active unknowns. If each input
numerator/denominator has at most L bits, clearing at most k+1 denominators per
selected equation produces an integer square system whose entries have
O(k L) bits. Cramer's rule and the Leibniz determinant bound k! H^k then give
O(k^2 L + k log(k+1)) bits for each numerator and denominator. Row identifiers
also cost O(k log(m+1)) bits. This is a generous bound, not a sharp encoding
claim. Exact verification uses rational arithmetic on the selected rows.

There is no constant-precision conclusion. There also is no claim that enumerating
(2) is the best way to solve a linear program: proof existence, proof checking,
search, and memory are distinct costs. The larger Lawvere language has additional
operations and case structure; its complexity theorems are not complexity results
for a single conjunction of finite linear inequalities.

## 3. F04-C24 — numerical robustness is not sparsity

Suppose a current, justified envelope permits row upper bounds eta+u with
0<=u<=tau componentwise, where tau>=0. For a fixed certificate lambda,

    v^T g <= eta^T lambda + tau^T lambda.                          (4)

The upper-corner envelope P(eta+tau) contains every source allowed by any such
u. If that whole rectangular family is the intended model, its exact worst-case
query is the support of P(eta+tau), so (3) gives

    h_{eta+tau}(v) = min_{lambda in B(A,v)} (eta+tau)^T lambda.      (5)

The nominally best certificate need not be the best at the revised precision.
Formula (4) is a property of the chosen proof; (5) is best inference from the
changed premises. Neither formula establishes the empirical envelope itself.

**Proof.** Multiply each current row bound by lambda_i>=0 and sum. Every allowed
source is in the upper-corner polyhedron; conversely that corner is itself
allowed. It is feasible whenever some weaker corner is feasible. Apply (3).
QED.

### A two-premise proof can amplify small uncertainty arbitrarily

Let epsilon>0 and use

    g1 + epsilon*g2 <= 0,
   -g1 + epsilon*g2 <= 0.

The query g2<=0 has the unique certificate with

    lambda1=lambda2=1/(2 epsilon).

Relax each right-hand side to tau>=0. Adding the inequalities proves

    g2 <= tau/epsilon,                                          (6)

and g=(0,tau/epsilon) attains this bound. Both row normals have length close to
one when epsilon is small; this is not an artifact of multiplying a whole row
by a small number. At epsilon=2^-k, the certificate has two entries of magnitude
2^(k-1), only O(k) bits each, yet its sensitivity is exponential in k.

An independently justified additional row g2<=c, with c>=0, changes the exact
revised bound to min(tau/epsilon,c). Before revision the two-row proof was tighter
when c>0; after enough revision the one-row alternative is tighter. Keeping a
proof portfolio can therefore recover a conclusion when a nominally optimal
proof exceeds its tolerance. The additional row needs evidence; it is not
introduced just because it gives the desired conclusion.

### Row units must transform the uncertainty too

For a positive diagonal rescaling S of the source rows, replace

    A' = S A, eta'=S eta, tau'=S tau, lambda'=S^-1 lambda.

The query identity and both products eta^T lambda, tau^T lambda are unchanged.
A bare multiplier norm is therefore not an intrinsic uncertainty cost; the
weighted quantity tau^T lambda is. This is also why a neural-coordinate or unit
change must transport the certificates and error envelopes, not merely their
numerical labels. Approximate equality A^T lambda≈v is not sufficient on an
unbounded source set; S3's residual-support term remains necessary.

## 4. F04-C25 — sparse data-chosen proofs do not inherit marginal coverage

In the elementary stochastic construction below the target g is fixed at zero.
For m independent records use the location model U_i=g-B_i with B_i Bernoulli(alpha).
At g=0 this is U_i=-1 with probability alpha and U_i=0 otherwise. The procedure
uses the observed U_i, not access to the unknown g; each fixed row g<=U_i has
coverage 1-alpha for every value of the location parameter. A procedure selecting the smallest
U_i emits a one-row arithmetic proof, but its target failure probability is

    Pr[g>min_i U_i] = 1-(1-alpha)^m.                              (7)

At m=3 and alpha=1/10 this is 271/1000, not 1/10. Every formal source polyhedron
is nonempty even on the failure event. Thus neither a feasible source model nor
one selected premise detects the failed empirical premise.

**Proof.** The selected claim holds exactly when all m independent records are
zero. This event has probability (1-alpha)^m. The certificate is the unit vector
at a minimizing index. QED.

A valid repair is simultaneous coverage: on one event E of probability at least
1-alpha_total, every row bounds the same target g. Then *every* data-dependent
choice of valid coefficients and query within the declared source model is
arithmetically sound on E. The proof is pointwise and needs no independence.
A union bound over prespecified row failure allowances is one way to obtain E;
a stronger calibrated joint procedure may be better. A growing or repeatedly
queried evidence store needs its own simultaneous/anytime evidence contract.

This is a probability-of-error example inside a declared sampling model, not
an appeal to knowable metaphysical truth. It states what an empirical evidence
mode would have to warrant. Sparsifying the final proof does not retroactively
reduce the number of data-dependent opportunities for an erroneous certificate.

## 5. F04-C26 — a library can be large even though every proof is small

Let g have d coordinates. For each i supply two independent row *addresses*
with the same left-hand side:

    g_i <= eta_(i,0),    g_i <= eta_(i,1).

These are possibly different evidence records, not probabilistically independent
samples by assumption. Take the query v=(1,...,1). The source set is nonempty
for all finite eta, and

    sup sum_i g_i = sum_i min(eta_(i,0), eta_(i,1)).                (8)

The upper bound follows coordinatewise and is attained by setting each g_i to
its coordinate's smaller upper bound. The dual coefficients have constraints

    lambda_(i,0)+lambda_(i,1)=1, lambda>=0.

At any fixed eta a tight proof needs only d rows. But a **flat, fixed list of
linear certificates** that must return the exact optimum for every eta needs
at least 2^d entries.

**Lower-bound proof.** For each bit string s of length d choose
eta_(i,s_i)=0 and eta_(i,1-s_i)=1. The optimum in (8) is zero. A certificate
attains zero only when every multiplier on a value-one row vanishes. The pair
sum constraints then uniquely force lambda_(i,s_i)=1 for all i. Distinct s
require distinct entries. There are 2^d such settings, all with feasible sources.
Listing those 2^d certificates is also sufficient, since every current set of
pairwise minima selects one of them. QED.

This is emphatically **not** a lower bound on all proof languages, representations,
or neural networks. A factored expression for (8) uses only d minimum operations
and d-1 additions. It evaluates the optimum and emits the chosen d-row certificate
in O(d) comparisons and arithmetic operations, without enumerating the flat list.
It needs the two current bounds for each coordinate, not the whole hidden model.
Ties can use a declared stable row-identity ordering for reproducible provenance.

For real x,y,

    min(x,y)=x-ReLU(x-y).

Thus (8) has an exact one-hidden-layer ReLU realization with at most 3d units
when arbitrary signed eta are allowed: two units carry each signed x as
ReLU(x)-ReLU(-x), and one carries ReLU(x-y). With nonnegative eta, 2d suffice.
The final output is affine. This is a constructed representation and a useful
control, not evidence that training discovered these computations. No new
training target or architecture is mandated for the existing neural experiment.

**Candidate consequence.** An explicit proof route and a value-functional route
can use the same factored expression. Comparing an exponentially expanded proof
list against a compact functional circuit would compare different permitted
operations, not prove that one kind of number has intrinsically greater power.
The opportunity is to retain useful compositional structure and proof emission,
not to advertise familiar min-plus distributivity as a new logic.

## 6. F04-C27 — unknown evidence modes require the right quantifier order

Suppose current evidence says the source belongs to one of K nonempty polyhedra
with the same template matrix:

    P_k = {g : A g <= eta^k},       k=1,...,K.

The current target and compared policies are fixed. The unknown mode is not an
observable input on which the policy may silently condition. The source-cover
assertion itself needs an accepted evidence mode. Write

    Lambda = {lambda>=0 : A^T lambda=v}.

For a finite query bound there are three different operations:

    H_case = max_k min_{lambda in Lambda} (eta^k)^T lambda,
    H_one  = min_{lambda in Lambda} max_k (eta^k)^T lambda,
    H_box  = min_{lambda in Lambda} (max_k eta^k)^T lambda.        (9)

The coordinatewise maximum in H_box discards correlation between premise bounds.
H_case is exact on the disjunction of original source sets. H_one requires one
coefficient vector to work before the mode is known. Generally

    H_case <= H_one <= H_box.

### Exact geometry of the common-proof relaxation

Let B have columns eta^k and define

    P_mix = {g : exists pi>=0, sum pi=1, A g <= B pi}.

Then H_one=h_(P_mix)(v) whenever this support is finite, with an attaining
common certificate. In particular H_one is not automatically the support of
the original union, or even of its convex hull.

**Proof.** Every lambda in Lambda bounds a point in P_mix by
lambda^T A g <= lambda^T B pi <= max_k lambda^T eta^k. For the converse apply
S3's finite Farkas result to the variables (g,pi) and inequalities

    A g - B pi <=0, -pi<=0, sum pi<=1, -sum pi<=-1.

If v^T g<=delta is valid on that nonempty set, its multipliers can be denoted
lambda>=0, mu>=0 and s,t>=0. Equality of query coefficients requires

    A^T lambda=v,
    -B^T lambda-mu+(s-t)1=0,
    s-t<=delta.

Hence (eta^k)^T lambda<=s-t<=delta for every k. At the finite support value this
proves equality and attainment. QED.

A consequence is easy to miss: if eta actually ranges over the convex hull of
the displayed modes, checking the individually optimized *vertex values* need
not suffice. The optimized support is a concave function of eta and can have
its worst value at an interior eta. In contrast, maximization of an affine
quantity at a fixed controller report in earlier notes legitimately checks
vertices. Optimizing the proof first has changed the function being maximized.

### A strict three-level example

Let g=x be a one-dimensional paired loss change. Supply two copies of x as row
left-hand sides and two possible upper-bound records:

    eta^1=(-1,1),     eta^2=(1,-1).

Either mode establishes x<=-1. Thus H_case=-1. A common certificate has
lambda1+lambda2=1 and worst bound |lambda1-lambda2|, minimized at (1/2,1/2),
so H_one=0. Coordinatewise maxima give H_box=1. Convexly mixing the original
bounds by pi=(1/2,1/2) permits the spurious source x=0; taking row maxima permits
x=1. The union and its convex hull both remain {x<=-1}.

The conclusions differ operationally: strict improvement, no deterioration, and
a possible increase. This example also works with nonnegative losses unbounded
above. Add the common row -x<=2, and use J_old=3+z, J_new=3+z+x with z>=0.
The original models have x in [-2,-1]. The added lower bound does not change
any of the three stated upper optima.

### Different proofs need not mean different actions

A finite case certificate supplies a possibly different lambda^k for each
admitted mode, checking the *same query and same proposed policy* in all cases.
The agent does not need to observe the actual mode to use that policy. The
checker verifies every branch and the coverage of the mode set. This is not
the invalid inference from 'each mode admits some action' to 'one currently
available action works for every mode'. Here only the justification varies.
Dropping a possible mode, or proving different action identities in different
branches, changes the conclusion and is not allowed by this rule.

There is an easy positive case where all three bounds agree: if one supplied
eta^k dominates all others componentwise, its source polyhedron contains every
other mode and already realizes the coordinatewise upper envelope. The three
source operations then coincide. The strict example above lacks that premise.

## 7. F04-C28 — optimizing a proof portfolio can encode set cover

This is a statement about a restricted certificate format, not every logical
proof language. Suppose the delivered proof is a flat list of nonnegative linear
combinations, with a table showing which combination establishes the common
bound in each of the finitely listed source modes.

Given a finite universe U of modes and a family of subsets S_1,...,S_m whose
union is U, make a scalar query x<=0 and m identical left-hand-side rows x.
In mode k set

    eta_i^k = 0 if k in S_i, and 1 otherwise.

Every mode's source is nonempty and implies x<=0. Every linear certificate has
lambda>=0 and sum lambda=1. Such a certificate proves bound zero in mode k iff
all its positive-support row indices contain k. Thus its mode coverage is

    coverage(lambda) = intersection_{i:lambda_i>0} S_i.           (10)

Replacing a multirow certificate by any one supported row can only enlarge its
coverage. Therefore the least number of entries in a valid portfolio equals
the least number of sets needed to cover U. This is an explicit reduction,
not a claim that merely deciding the known-valid inequality requires solving
an optimization problem. A nonminimal portfolio is perfectly sound.

For U={1,2,3,4,5,6}, let

    S1={1,2,3,4}, S2={1,2,5}, S3={3,4,6}.

Two entries, S2 and S3, cover every mode. A largest-uncovered-set greedy rule
selects S1 first and then needs both others, using three entries. A single common
linear combination cannot prove zero for all modes. Its best worst-case bound
is 1/2: modes 5 and 6 force a maximum at least (1+lambda1)/2, and
lambda=(0,1/2,1/2) achieves 1/2.

The result helps avoid a misleading performance claim: individual proofs can
be sparse while choosing the smallest reusable collection is combinatorial.
It does not preclude a compact factored algorithm such as section 5, a richer
logical rule, or retaining a larger sound proof list. The set-cover reduction
is a standard complexity-pattern specialization; no literature-priority claim
is made for the construction.

## 8. F04-C29 — a useful compositional subfragment has short path proofs

A more structured source matrix avoids expanding all proof alternatives. Let a
finite directed graph have vertices representing scalar model-cost coordinates
x_i. An edge i->j supplies the same-context inequality

    x_j-x_i <= w_(i,j),

with finite signed weights. The actual costs can share an unrestricted offset;
only differences are constrained. Consider the query x_t-x_s.

Assume the source inequalities are jointly feasible. They then have no directed
cycle of negative total weight, since summing such a cycle would give 0<0.
Conversely, absence of a negative cycle guarantees feasibility: add a temporary
source with zero-weight edges to every vertex and take its shortest-path distances
as potentials. Each distance is finite; deleting nonnegative cycles leaves a
simple path, and edge relaxation gives the required inequalities.

If t is reachable from s, the exact implied upper bound is the shortest-path
weight dist(s,t); a simple path gives a certificate with at most n-1 edges.
If t is not reachable, the query is unbounded above.

**Proof of the upper bound.** Sum the edge premises on any s-to-t path. All
intermediate costs cancel. The smallest path sum is the strongest such bound.

**Attainment.** Let R be the vertices reachable from s. There is no edge from R
to its complement. For j in R set x_j=dist(s,j), so x_s=0 and x_t=dist(s,t).
For j outside R take any feasible potential x_j^0+C. Choose C large enough for
all edges entering R; this is possible because there are finitely many. Edges
within either part preserve feasibility, and none leaves R for its complement.
The resulting potential attains the bound.

**Unbounded case.** Start with any feasible potential. Add the same C>=0 to
all coordinates outside R and leave R fixed. Entering edges only become easier,
internal differences do not change, and no edge leaves R. If t is outside R,
x_t-x_s tends to infinity. QED.

This is the established difference-constraint/shortest-path structure, derived
here to establish a concrete equal-information baseline. Repeated relaxation
computes best path weights with at most n-1 edges in O(n*m) arithmetic operations;
this is not a bit-complexity statement for arbitrary real inputs. The graph's
scope checks, empirical evidence and feasibility must still be supplied.

For three models take edges 0->1 with bound 2, 1->2 with bound -3, and 0->2
with bound 0. Their best implied change is min(0,2-3)=-1. Increasing the first
bound by 1/2 leaves a strict-improvement proof of -1/2. Increasing it by 2 makes
the direct zero bound preferable to the now-positive indirect bound. One proof
has ceased to give the best conclusion, but a retained alternative remains valid.
The tight bound has the ReLU expression

    min(c,a+b) = c-ReLU(c-a-b).

This provides another concrete loss/residual computation, not evidence of an
emergent neural mechanism. A learned proposal would still need its interpretation
and error checked. Adding arbitrary graph vertices or changing the task units
is not an unchanged fixed-input-network inference.

A numerical zero cycle is not a grounded empirical certificate. Graph algebra
operates on supplied valid premises; it does not authorize generating its own
premises from a circular endorsement. An inconsistent negative cycle should
produce a source-conflict diagnostic in the intended empirical interface, not
an operational license obtained by classical explosion.

## 9. F04-C30 — precision needs can defeat a fixed finite template family

Consider a possible-slope disk G={g in R^2: ||g||_2<=1}. Its exact support is
h_G(v)=||v||_2. These are local slope units; an arbitrary shared cost offset can
still make the absolute values unbounded. The radius is not a universal bound
on every value in the research program.

Retain finitely many exact directional premises u_i^T g<=1 with ||u_i||_2=1.
They form an outer enclosure P. No such finite family is exact for every query
direction. Indeed choose a unit q different from all u_i. Then u_i^T q<1 for
every i. Since there are finitely many, some t>1 still has t u_i^T q<=1 for all i.
Thus tq lies in P but q^T(tq)=t>h_G(q)=1. If the family does not surround the disk,
some support values may even be infinite.

For m>=3 directions evenly spaced around the circle, consecutive tangents meet
on their angular bisector at radius sec(pi/m). Their polygon satisfies

    ||v||_2 <= h_P(v) <= sec(pi/m)*||v||_2.                       (11)

At a vertex-bisector query this factor is attained. For any surrounding family
of at most m unit directions, some consecutive angular gap is at least 2*pi/m.
If a gap is at least pi the enclosure is unbounded. Otherwise its tangent
intersection is feasible for all the other directional constraints and has
radius sec(gap/2), giving a factor at least sec(pi/m). Equal spacing is therefore
optimal for this particular worst-direction, finite-tangent-template problem.

For queries ||v||<=R, R>0, a worst-direction additive error at most epsilon>0
requires and, for equal spacing, is achieved by

    R*(sec(pi/m)-1) <= epsilon,
    m >= pi / arccos(1/(1+epsilon/R)).                           (12)

Take the integer ceiling and at least three directions. The small-epsilon
scaling is order sqrt(R/epsilon). This is not a lower bound for arbitrary
representations: the original quadratic inequality defines the disk compactly.
Nor does an ideal evenly spaced real construction by itself specify a finite
rational encoding of its normals. The concrete fixture below uses exact rational
unit directions and rational certificates instead.

### A compact nonlinear premise can avoid those missing directions

In two dimensions the polynomial identity

    (v^T g)^2 + (v1*g2-v2*g1)^2 = (v1^2+v2^2)*(g1^2+g2^2)

proves v^T g<=delta whenever ||g||^2<=1, delta>=0 and delta^2>=||v||^2.
All quantities can be finite signed reals, with the prior guarded translations
used if an RLL encoding is wanted. This is an ordinary sum-of-squares identity,
not a newly implemented RLL proof or a proof that the source disk is empirically
correct. A rational delta above an irrational norm can be certified by squaring;
finite precision need not be confused with exact recovery of an irrational value.

For v=(1/10,1/10), coordinate bounds alone give 1/5. Add the two rational unit
normals (3/5,4/5) and (4/5,3/5). Multipliers 1/14 on each give the sharper bound
1/7. At tolerance 3/20 the coordinate certificate fails while this two-row proof
passes. The quadratic premise also certifies that tolerance, since
(3/20)^2=9/400 >= 1/50=||v||^2. The exact support is sqrt(2)/10.

### Global additive accuracy differs from relative accuracy

No fixed finite tangent family achieves a finite *uniform additive* error for
all v: scale a direction with a strict gap by t and the gap grows linearly.
Relative error (11), or an additive tolerance on a bounded query family, is
possible. This bounds the size of proposed changes, not all absolute values.
The same distinction constrains finite ReLU representations of the Euclidean
norm: exact equality is impossible in dimension two because its restriction to
(1,t) is strictly curved rather than finitely piecewise affine. A global uniform
additive approximation by a finite ReLU network would force its zero-bias ray
function to equal the norm, contradicting the same obstruction. The bounded-bias
ray argument is the one already proved in F04 S2, not a new blanket claim about
all neural architectures or all forms of approximation.

## 10. F04-C31 — when a ReLU value function is a portfolio of valid proofs

This is a structural specialization, not a claim of novelty in convex duality.
It connects the two shortlisted routes without changing the supplied evidence.
Fix finite A and v, and a finite real-valued function f of the m row bounds eta.
Say it is A-translation compatible for v when

    f(eta+A z) = f(eta)+v^T z  for every eta,z.                    (13)

This is a concrete covariance law: shifting a possible slope vector by z shifts
its row bounds by A z and its queried value by v^T z. It is not a metaphysical
axiom and does not mean that all empirical contexts are interchangeable.

### Soundness without exact representation

If f is coordinatewise nondecreasing, satisfies (13), and f(0)>=0, then

    f(eta) >= h_eta(v)

on every nonempty P(eta).

**Proof.** For any feasible g, A g<=eta. Monotonicity gives
f(eta)>=f(A g)=f(0)+v^T g>=v^T g. Take a supremum. QED.

This direction needs neither concavity nor homogeneity. For A=(1,1)^T and v=1,
f(eta)=max(eta1,eta2) is a sound but sometimes loose bound. Rejecting it merely
because it is not concave would reject a valid conservative summary.

### Exact finite-portfolio characterization

Suppose additionally that f is continuous finite piecewise affine on all R^m.
The following are equivalent:

1. f is concave, positively homogeneous, coordinatewise nondecreasing, and
   A-translation compatible for v;
2. there is a nonempty finite collection lambda^1,...,lambda^N with
   lambda^j>=0, A^T lambda^j=v, such that

       f(eta)=min_j (lambda^j)^T eta.                            (14)

Each piece in (14) is a valid arithmetic certificate. The theorem does not say
that the portfolio contains *every* optimal certificate, so f need not equal the
exact h_eta on every feasible eta. The complete library of section 2 does.

**Proof of 2=>1.** Each linear form has nonnegative coefficients. Their minimum
is coordinatewise nondecreasing, concave, continuous and positively homogeneous.
Adding A z to eta adds the same v^T z to every term, giving (13).

**Proof of 1=>2.** Take the finitely many essential affine pieces, those with
nonempty full-dimensional interiors. On one such interior write f= lambda^T eta+c.
A small change in any coordinate stays in that interior; monotonicity forces
lambda>=0. For each z a sufficiently small displacement t A z stays there;
(13) forces lambda^T A z=v^T z, hence A^T lambda=v. Choose a nonzero interior
point eta and vary it to (1+t)eta for sufficiently small t. Homogeneity and the
affine expression imply c=0. The constant-zero piece is covered by the same
argument; no special derivative at the origin is assumed.

Each essential linear form is a global upper support for f. To see this, take
an interior point eta and any y. For sufficiently small t>0, eta+t(y-eta) stays
in that piece. Concavity gives

    f(eta)+t lambda^T(y-eta)
       >= (1-t)f(eta)+t f(y),

so f(y)<=lambda^T y. At any y, continuity and the finite cell decomposition
supply an adjacent essential piece with f(y)=lambda^T y. Taking the minimum
of the finitely many pieces therefore reproduces f everywhere. QED.

**Why the hypotheses matter.** With A=(1,0)^T and v=1, the linear map
f(eta)=eta1-eta2 satisfies homogeneity, concavity and (13) but is not monotone.
At eta=(1,1), its value zero is below the source support one. The constant-zero
map drops translation compatibility and is unsound for A=(1), v=1, eta=1.
The map f(eta)=eta-1 is monotone and translation compatible but lacks the required
normalization, and similarly underestimates. Conversely the max example above
shows that concavity is needed for the *portfolio characterization*, not for
basic soundness.

### A check at one neural input needs less than global structural verification

For an ordinary finite ReLU MLP, fixing the activation masks at the observed
input produces an exact affine expression

    f(eta)=lambda^T eta+c.

Masks at exactly zero can use a fixed convention; the expression still equals
the actual output at that input. They need not describe an open reachable cell
for the following implication. If exact arithmetic verifies

    lambda>=0, A^T lambda=v, c>=0,

the network's scalar output at this input is a valid upper bound on the query.
This follows directly from the same source inequalities. No global concavity
or proof of all activation patterns is needed for that *one emitted certificate*.
If the check fails, the output is not certified by this method; it is not thereby
proved false. A different certificate may still establish it.

If that lambda is retained for later eta', it remains a valid standalone bound
lambda^T eta'+c under unchanged A,v and valid new premises. It need not equal the
network's later output, since the activation masks may change. The network must
be rechecked if its new output is being used as the bound.

This suggests a falsifiable interpretability question: after ordinary training,
does a predeclared meaningful input abstraction and queried cost admit these
certificate fingerprints, and do the proposed mechanisms survive interventions
and reparameterization controls? Selecting A after seeing a convenient gradient
would not answer that question. No network was trained here, and the hand-built
ReLU realizations are positive controls, not evidence of naturally learned logic.

A uniform approximate version of the simple soundness proof is possible: if the
relevant monotonicity comparisons have deficit at most e_m, (13) has deficit at
most e_t on the actually admitted source shifts, and f(0)>=-e_0, then

    f(eta)+e_m+e_t+e_0 >= h_eta(v).

This requires genuine uniform/source-scoped bounds on the defects; average
errors on samples do not establish them, especially on unbounded directions.

## 11. F04-C32 — smoothing proof choice is not free extra evidence

Let x_j=eta^T lambda^j be N valid finite same-query certificate bounds and let
pi_j>0 with sum pi_j=1. For tau>0 define the normalized soft minimum

    S_tau(x) = -tau*log(sum_j pi_j*exp(-x_j/tau)).                 (15)

Then, writing x_min=min_j x_j,

    x_min <= S_tau(x) <= x_min-tau*log(pi_j*)

for any minimizing j*. Thus S_tau is still a conservative bound. Uniform pi
gives the familiar maximum excess tau*log N. These are analytic inequalities;
certifying a numerical log/exp evaluation requires its own error enclosure.
They are not native arithmetic rules of the finite RLL audit checker.

**Proof.** Every exponential in the weighted sum is at most exp(-x_min/tau),
while the minimizing term alone contributes pi_j* exp(-x_min/tau). Taking
negative logarithms gives the two inequalities.

For completeness, set w_j=pi_j exp(-x_j/tau)/Z with Z the sum in (15). Then
for any probability vector q,

    sum_j q_j x_j + tau KL(q||pi)
       = S_tau(x) + tau KL(q||w).

The identity follows by expanding the logarithm of q_j/w_j. Nonnegativity of
KL yields the variational minimum at q=w. The averaged coefficients
lambda_bar=sum_j w_j lambda^j also form a valid certificate and give the bound
sum_j w_j x_j, which is no larger than S_tau because the latter adds tau KL(w||pi).
The KL term here is a regularizer for proof selection; it is not the probability
that an empirical source is true and supplies no additional coverage guarantee.

The *unnormalized* expression -tau log(sum_j exp(-x_j/tau)) need not be an upper
bound at all. Two duplicate exact bounds x1=x2=0 yield -tau log 2 below the
actual zero quantity. Even clamping to nonnegative values does not generally
repair it: duplicate exact bounds of one with tau=1 give 1-log 2, still below one.
A lower-looking smooth objective can therefore fabricate improvement from
duplicating a proof. Normalizing and splitting a prior mass when a proof is
copied preserves (15); silently changing the prior is a different operation.

Minimum over alternative valid proofs and maximum over unresolved source modes
play different roles. A proof portfolio may take a minimum because every entry
bounds the *same* quantity under the same current premises. A possible-world
family requires the appropriate universal/worst-case operation, as in section 6.
Neither minimization nor a neural activation has a fixed pragmatic meaning
without that scope and quantifier information.

### Supergradient certificates beyond finite piecewise-affine functions

There is a useful intermediate statement between the simple soundness rule and
the finite-portfolio characterization. Let f be finite, concave, monotone and
A-translation compatible on all R^m, with f(0)>=0. At eta take any supergradient
lambda, meaning

    f(y)<=f(eta)+lambda^T(y-eta) for all y.

Then lambda>=0, A^T lambda=v, and c=f(eta)-lambda^T eta>=0. Monotonicity rules
out a negative coordinate by setting y=eta+t e_i. Applying translation in both
z and -z forces A^T lambda=v. Taking y=0 gives c>=f(0)>=0. Hence
f(eta)=lambda^T eta+c is again a valid same-query certificate at eta. This
conditional statement uses a genuine global supergradient, not any convenient
fitted local slope. Ordinary finite concavity on the open domain supplies such
supporting hyperplanes; the finite-CPWL proof above constructs them explicitly.

For the normalized soft minimum in (15), differentiating gives

    gradient_eta S = sum_j w_j lambda^j,
    S - eta^T gradient_eta S = tau KL(w||pi) >=0.

So its gradient and tangent intercept are exactly of the certified form. This
also explains why its smooth value can be more conservative than its averaged
linear certificate. Scaling all cost units by alpha>0 must scale tau as well:
S_(alpha*tau)(alpha*x)=alpha S_tau(x). The regularization coefficient has cost
units; its presence does not create uncertainty calibration or metaphysical
truth. The general result is an ordinary convex-analysis specialization, with
verification/learning of the structural assumptions still open for real networks.

## 12. Candidate comparison, adversarial review, and next evidence

The two viable routes now have a more precise common benchmark. Route A retains
scoped linear premises and emits arithmetic certificates. Route B retains an
upper-value/support functional. On the same feasible P(eta), a complete finite
certificate library and its value envelope agree exactly. A flat library can
be a poor implementation: factoring independent choices or using path structure
can avoid exponential expansion. A learned scalar merely fitted to that envelope
is neither an exact optimizer nor a valid certificate until the relevant checks
or sound approximation bounds are supplied.

Neither route wins simply by receiving more informative source constraints.
A quadratic norm premise beats finitely many tangent bounds for some queries,
but this changes the retained information/available operations. Both routes can
use the quadratic identity if their rule interfaces admit it. Conversely, two
short conditional proofs can be stronger than one uniform coefficient vector
on the *same* listed source modes. A proof language must distinguish that case
split from choosing a hidden-world-dependent policy.

The following same-agent reconstruction checks were performed before code:

1. Sparse certificates minimize support among already attaining optima. Without
   feasibility, the zero-query and negative-cycle cases can invalidate the intended
   empirical reading. No empty-set inference authorizes an action.
2. In the sparse perturbation proof both signs are initially feasible, so a
   nonzero objective slope really would contradict optimality. Coefficient
   reduction preserves the exact query identity, not an approximate equality.
3. In the bit-string family every zero-valued optimal proof is unique. The
   exponential lower bound is only for a flat fixed list, not the factored min-plus
   circuit that immediately defeats a broader claim.
4. In the mode example the convex hull of source sets is still x<=-1. It is
   averaging *right-hand sides before intersecting rows* that creates x=0.
   The mode-dependent proofs establish one common policy/query, unlike the
   impermissible swap of an action-existence quantifier.
5. The augmented Farkas proof uses both signs of sum pi=1. Its last multiplier
   difference s-t can be negative; forbidding that would break signed improvements.
6. A path potential on unreachable vertices must be shifted upward, not downward,
   because only edges entering the reachable set can cross the partition.
7. The disk lower bound concerns fixed directional halfspaces. A single quadratic
   premise and its sum-of-squares certificate avoid that representation constraint.
8. Concavity is needed for the finite minimum-of-certificates description, not
   for soundness itself. A rejected local neural certificate is not a refutation
   of the scalar output. No interpretation is manufactured by choosing A after
   observing a convenient activation or gradient.
9. A probability prior over proof choices is not a coverage guarantee. The
   normalized soft minimum is conservative because its inputs are already valid
   bounds. Raw unnormalized log-sum-exp can undercut even duplicate exact bounds.

The most promising next test is not another catalogue of independent toy cases.
It is to apply a *predeclared* scope and coefficient-check interface to the
already-planned neural experiment or to an equally specified source-revision
workload, comparing tightness, proof size, and verification cost against the
same-information baseline. F04 still owes its remaining protected derivation
and hostile-review time. No core, gate, general completeness theorem, training
run, or new external novelty claim is completed by this note.

## 13. End-to-end check on the existing reflective controller

The mode distinction is not confined to a free scalar unrelated to F04's actual
model. Retain the same two-branch controller

    H_(a,b)(r)=a r+b(1-r),   a,b in [0,1].

Fix old report r0=3/4 and proposed report r1=19/20. Let the declared cost be
J_(a,b,z)(r)=5 H_(a,b)(r)+z with arbitrary shared z>=0. The actual cost change
is exactly a-b, because 5*(r1-r0)=1. Absolute costs are nonnegative and can be
unbounded; this comparison is finite.

The source packet includes the four physical box rows and the valid report rows

    (3/4)a+(1/4)b <= 3/4,
    (19/20)a+(1/20)b <= 19/20.

It also gives two same-query evaluator rows with left-hand side a-b. One of the
two modes has bounds (-1/2,1/4); the other has (1/4,-1/2). The mode cover is a
premise, not an observation on which the proposed policy depends.

| Source handling | Paired-cost upper bound | Certificate | Attaining source or relaxation witness |
|---|---:|---|---|
| Preserve both cases | -1/2 | select the -1/2 row in each branch | (a,b)=(0,1/2) in both actual modes |
| One coefficient vector for all modes | -1/8 | weight each evaluator row by 1/2 | (a,b)=(0,1/8) at the midpoint RHS |
| Independent row maxima | 1/4 | either weakened evaluator row | (a,b)=(1/4,0) in the rowwise enclosure |

Each listed point satisfies all six common physical/report rows. Their paired
query values attain the displayed bounds, so those relaxations cannot prove a
stronger result. Both actual-mode sources enforce a-b<=-1/2. Indeed for either
report r in {3/4,19/20}, failure is at most (r/2)+(1-r)=1-r/2<=r; hence the
explicit report rows are compatible and do not hide an assumption of an
infallible branch. Nonempty source witnesses and the arithmetic certificates
can be checked without estimating z.

Preserving the cases certifies an improvement of at least 1/2 in expected cost.
A uniform proof retains only an improvement of 1/8, while rowwise forgetting
cannot certify any improvement. The policy is the same in all three calculations.
The difference is how the evidence is represented and combined, not whether the
agent can observe the hidden source or whether the absolute value is bounded.
This is a source-discrimination result in the declared controller model, not an
empirical reliability claim or an unrestricted self-reflection theorem.

### Supplementary temperature check for the smooth bound

For fixed finite x and strictly positive pi, the normalized bound in (15) is
nondecreasing in tau. Direct differentiation gives

    dS_tau/dtau = (S_tau-sum_j w_j x_j)/tau = KL(w||pi) >=0.

It approaches min x as tau decreases to zero, by the already proved error bound,
and approaches sum_j pi_j x_j as tau increases without bound, by expansion of the
finite exponential sum at zero inverse temperature. Thus temperature controls a
conservative smoothing gap, not empirical certainty. This interpretation and
its limits are specific to normalized same-query proof bounds.

### Exact numerical reconstruction used for the precision fixture

At epsilon=1/16 and tau=1/64, the two near-opposite rows use multipliers (8,8)
and give the sharp bound 1/4, attained at g=(0,1/4). Rescale the first row by 2
and the second by 1/4. The multipliers become (4,32), the uncertainty widths
become (1/32,1/256), and their weighted sum is still 1/4. A separately certified
row g2<=1/8 instead gives the sharp combined bound 1/8, attained at (0,1/8).
This checks the numerical units and the improved alternative without relying
on floating-point arithmetic or a solver's optimality report.

## 14. Boundary reconstruction prompted by the first executable check

The first new-suite run exposed an implementation-level distinction: at a zero
ReLU preactivation, independently choosing every derivative to be zero need
not recover a genuine neighboring affine piece of the *composed function*.
For

    f(x,y)=ReLU(x)-ReLU(-x)-ReLU(x-y)=min(x,y),

at (x,y)=(0,-2), the all-inactive-zero convention gives formal slope (-1,1),
even though f is locally y with true slope (0,1). The output -2 is correct.
The certificate checker rightly rejects the negative coefficient. This is not
an invalid scalar prediction or a counterexample to section 10; it refutes the
fixture's initial assumption that independent zero masks always select a
certificate-carrying affine region. The failed run is retained.

For the one-hidden-layer implementation, use the coherent approach

    eta(epsilon)=eta+(epsilon,epsilon^2,...,epsilon^m), epsilon>0.

At a zero preactivation, select its mask by the sign of the first nonzero input
weight. At a nonzero preactivation retain its current sign. Each zero expression
is a finite polynomial in epsilon; its leading nonzero coefficient determines
its sign for sufficiently small positive epsilon. A finite collection has a
common such neighborhood. Identically zero units contribute nothing. Thus the
selected masks occur at actual nearby inputs, and their affine expression still
agrees at eta by continuity. This gives slope (0,1) in the example.

The fixture keeps the old inactive convention as an explicit negative control
and defaults to this coherent one-sided convention. For a deeper network the
same idea requires propagating the affine coefficient vectors through selected
layers; that broader implementation is not included here. Ordinary autodiff's
per-node convention must not simply be identified with a global supergradient,
especially after introducing cancelling or redundant units. Pointwise arithmetic
certification remains sound whenever its coefficient and intercept checks pass.
