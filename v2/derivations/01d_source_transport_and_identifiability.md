# F04 S5 — Evidence transport, restricted observations, and identifiable proofs

Status: **candidate discrimination; F04 remains partial**.
Base: `334e106d748ebdc43a8f7ceddb896cdb25135273`.
Predecessor: [S4 certificate portfolios](01c_certificate_portfolios.md).
This note develops finite source-interface results and countermodels. It does not
select a permanent calculus, begin Gate A/F05, train a network, or claim novelty
for linear programming. [Source positioning](F04_S5_sources.md) and the
[measured session record](../work_logs/F04_2026-09-26_S5.md) delimit the work.

## 1. The focused question

S4 showed how a piecewise-linear computation can select valid quantitative
certificates. But the rows supplied to that computation need not be independent
coordinates. Some are derived from other rows; some are observed only together;
some are recoded by a representation change. When does a valid bound survive
such a change, and when does a neural computation identify a particular proof?

Three questions must be distinguished:

1. Does a stored numerical representation still determine the old information?
2. Does the *new interpretation as premises* justify the same conclusion?
3. Do the observations or interventions distinguish the proposed explanations?

A positive answer to one does not imply a positive answer to the others. The
results below give constructive tests and counterexamples, rather than demanding
that every representation store all available information.

### Fixed finite setting

A versioned policy has expected task cost `J_theta(p)=b_theta+g_theta^T p`.
The common baseline `b_theta` can be unknown and unbounded. A fixed policy
change has query `v=p_new-p_old`; its paired change is `v^T g_theta`.
Current, scoped evidence supplies

    P_A(eta) = {g in R^d : A g <= eta}.

All entries of `A`, `eta`, and `v` are finite real numbers. Computational
fixtures use rational entries. Unless stated otherwise, `P_A(eta)` is nonempty.
Its nonemptiness is not empirical evidence that the actual target lies in it.
Source identities, shared-target coupling, units, and certificate modes are
part of the interface, not optional numeric decorations.

The inherited finite-polyhedron result is

    sup_{g in P_A(eta)} v^T g <= delta
      iff exists lambda>=0: A^T lambda=v, eta^T lambda<=delta.   (1)

This implication/duality result, including finite optimal attainment on the
dual side, was reconstructed in S3–S4. It is the ordinary finite linear fragment,
not the full Rational Lawvere language. Both candidate routes below receive the
same `A`, evidence domain, query, and allowed transformations.

## 2. F04-C33 — aggregating premises transports certificates, but may weaken them

Let `R` be a finite `k by m` matrix with nonnegative entries. Replacing the
original inequalities with their nonnegative combinations gives

    A' = R A,    eta'=R eta,
    P_A(eta) subseteq P_(RA)(R eta).                            (2)

If a new certificate `mu>=0` obeys `(RA)^T mu=v`, its pullback

    lambda=R^T mu                                             (3)

is an original certificate, with exactly the same bound:

    eta^T lambda = (R eta)^T mu.

**Proof.** Multiply `Ag<=eta` by the nonnegative matrix `R`. Transposition gives
`A^T R^T mu=v`, and `R^T mu>=0`. The scalar identity is associativity of matrix
multiplication. No new empirical observation is created. QED.

Write `C_R={R^T mu:mu>=0}`. The best aggregate bound is precisely

    min {eta^T lambda : A^T lambda=v, lambda in C_R},           (4)

when the feasible certificate set is nonempty; otherwise the aggregate query
is unbounded above. The original bound minimizes over all nonnegative lambda.
Consequently, when the original support value is finite, aggregation preserves
that value **iff at least one original optimum lies in C_R**. More modestly,
aggregation preserves a particular tolerance claim `<=delta` iff an original
certificate in `C_R` attains that tolerance.

**Proof.** Apply (1) to the nonempty aggregate source in (2). Its feasible
certificates pull back exactly onto the set in (4). A finite aggregate optimum
is attained. Equality to the finite original optimum is therefore equivalent
to that restricted set containing an original minimizer. QED.

A supplied factorization `lambda=R^T mu` is itself a short, checkable transport
witness. If every member of a retained finite portfolio has such a factorization,
the portfolio's numerical answer is preserved for *every* right-hand side:

    min_j (lambda_j)^T eta = min_j (mu_j)^T R eta.              (5)

This statement does not require enumerating all optimal certificates and does
not assert that the retained portfolio is globally tight.

### The same compression preserves one question and destroys another

Take `A=I_2`, `eta=(1,2)`, and `R=(1,1)`. The original premises are
`g1<=1, g2<=2`; the aggregate premise is `g1+g2<=3`.
The query `g1+g2` has exact bound 3 in both representations, witnessed by
`lambda=(1,1)` and `mu=1`. The query `g1` has original bound 1 but no finite
aggregate bound: `g=(t,3-t)` is aggregate-feasible for every real t.

This is a genuine query-specific gain and loss with unbounded signed unknowns.
It does not show that summing evidence is always harmful, or that all utility
values need to be bounded. The policy query must be part of a claim that a
compression is adequate.

## 3. F04-C34 — invertible numerical recoding is not invertible logical weakening

Even an invertible `R` can lose consequences when its output is reinterpreted
as an ordinary independent list of upper-bound premises. For example take

    A=I_2, eta=(1,2), R=((1,1),(0,1)).

Numerically `R eta=(3,2)` determines eta exactly. But the new inequalities are

    g1+g2<=3,    g2<=2.

They do not imply `g1<=1`: `(g1,g2)=(4,-1)` satisfies both, and the earlier
`t` construction is unbounded as `t` grows. Recovering the old bound by
subtracting the second inequality from the first would be invalid: both are
upper bounds, not equalities.

The exact transformed semantics explains the loss. The original slack is
`s=eta-Ag`, with `s>=0`. Put `t=R s`. An invertible recoding is exact if it
retains

    t in R(R_+^m),                                             (6)

rather than weakening (6) to `t>=0`. In the displayed example the correct
cone is `{t:t2>=0 and t1>=t2}`. The latter inequality is precisely the old
`g1<=1` constraint when written in transformed slack coordinates.

There is a sharp elementary limit to a universal remedy within the orthant.
For an invertible square nonnegative matrix R, the following are equivalent:

* `s>=0 iff R s>=0` for every finite real vector s;
* `R^-1>=0`;
* R is a positive diagonal scaling composed with a permutation.

**Proof.** The first equivalence follows by setting `s=R^-1 e_i` and by direct
multiplication. For the second, put `S=R^-1>=0`. If `i!=j`,
`sum_k R_ik S_kj=0`, so each nonnegative summand vanishes. A column k of R
cannot have positive entries in two different rows: then row k of S would
have to vanish in every column, contradicting invertibility. Every column
of R is nonzero, and invertibility forces their single positive entries into
distinct rows. This is a scaled permutation. Conversely such a matrix has a
nonnegative inverse. QED.

This is only a statement about invertible **linear** maps preserving the
standard componentwise order in both directions. It excludes neither more
structured cones, query-specific transformations, nor nonlinear encodings.

### Consequence for value-as-primitive

A signed or bounded encoding of a value can preserve numbers without preserving
the *operations and order used to infer from them*. Here even no numerical
information is lost, yet the weakened premise interpretation loses a useful
model comparison. Both retained quantitative relationships and their intended
logical use matter. No commitment to metaphysical truth is needed for this
finite conditional statement.

## 4. F04-C35 — a complete lift test on a restricted evidence domain

Suppose the actual input coordinates are z, not independent row bounds, with

    eta(z)=eta0+B z,   z in Z={z:D z<=d}.

The relation and domain must be supplied before testing an explanation. They
cannot be invented after seeing a convenient network gradient. Empty D is
allowed and means all finite z. Suppose a proposed bound is affine on Z:

    f(z)=alpha^T z+c.

Assume the *joint* source/domain set

    K={(g,z): A g-B z<=eta0, D z<=d}                            (7)

is nonempty. There is no bound on the magnitudes of g or z unless these actual
constraints impose one. Then the following are equivalent:

1. for every `(g,z) in K`, `v^T g <= f(z)`;
2. there exist finite nonnegative vectors lambda,nu such that

       A^T lambda = v,
       B^T lambda-D^T nu = alpha,
       eta0^T lambda+d^T nu <= c.                             (8)

Here lambda weights source evidence and nu weights domain premises. These have
different provenance and are not interchangeable records.

**Sufficiency.** Multiplying the source and domain premises respectively gives

    v^T g <= eta0^T lambda+lambda^T B z
           = eta0^T lambda+alpha^T z+nu^T D z
           <= alpha^T z+eta0^T lambda+d^T nu
           <= alpha^T z+c.

All coefficient signs, transposes and the intercept inequality are load-bearing.
In particular nu is subtracted, not added, in the second identity of (8).

**Necessity.** Stack the variables as `w=(g,z)` and use the finite nonempty
polyhedron (7). Its matrix and queried linear form are

    M=((A,-B),(0,D)),     b=(eta0,d),     q=(v,-alpha).

Statement 1 is exactly `q^T w<=c` on `Mw<=b`. Apply (1) to this augmented
finite system. The nonnegative certificate splits into lambda and nu. Expanding
`M^T(lambda,nu)=q` and `b^T(lambda,nu)<=c` yields precisely (8). QED.

This is a restricted completeness statement for a concrete linear source
interface, not completeness of a new general calculus. The actual checker
below checks supplied multipliers; it does not search all of them. A feasible
witness for K distinguishes meaningful conditional reasoning from an empty
premise set. An empty K requires a source-conflict/inapplicable-case treatment,
not an operational authorization justified by vacuity.

### No domain constraints: the gradient needs a lift, not a direct interpretation

With empty D, (8) reduces to

    lambda>=0, A^T lambda=v, B^T lambda=alpha,
    eta0^T lambda<=c.                                         (9)

The observed input coefficient alpha need not have the dimension or signs of
a source coefficient. Even when the network is presented with the original
eta coordinates, the reachable evidence manifold can prevent identifying an
ambient gradient with a unique source proof.

Take a single unknown cost g with duplicate left-hand-side rows, `A=(1,1)^T`,
query v=1, and reachable evidence `eta=(z,z)` (`eta0=0, B=(1,1)^T`). The
network function `F(eta)=2 eta1-eta2` equals z on that manifold and is an exact
bound. Its ambient gradient `(2,-1)` is not a nonnegative certificate. Yet
its observed slope alpha=1 has the valid lift lambda=(1,0), as well as (0,1)
and every convex combination of them. Thus rejecting the particular ambient
gradient is not a proof that the bound is wrong on the declared inputs.

Off the manifold the same network can be unsound: at eta=(0,1) it returns -1,
but g=0 satisfies both source rows. A lift on the manifold is not an unrestricted
certificate for all separate evidence changes. This is not the earlier S4
zero-ReLU derivative issue: the function here is globally linear and smooth.

### Domain constraints can justify negative intercepts and unfamiliar slopes

Take `A=B=(1)`, eta0=0, domain `z>=1` (D=-1,d=-1), and `f(z)=2z-1`.
The source says g<=z, so f is a valid bound on that domain. The source-only
slope test would require lambda=1 and alpha=1, not alpha=2; its nonnegative
intercept test would also reject c=-1. But (8) passes with lambda=nu=1:

    1= v,       1-(-1)=2,       0+(-1)=-1=c.

At z=0 the proposed bound -1 is invalid for g=0, so the domain premise cannot
be erased after certification. Conversely `f(z)=1` is a sound bound on z<=1,
with lambda=nu=1, D=1,d=1; it fails without that domain condition.

The appropriate meaning of a neural coefficient therefore depends on the
input chart and its scope, not only on the name of an activation function.

## 5. F04-C36 — finite ReLU bounds have region-scoped linear proof certificates

Let an ordinary finite ReLU network with an affine output compute a scalar
F(z). No sign constraints, logic-labelled training, or special architecture are
assumed. Fix a finite polyhedral cover `{Z_sigma}` of its input domain such that
on every cell

    Z_sigma={z:D_sigma z<=d_sigma},
    F(z)=alpha_sigma^T z+c_sigma.

A consistent activation pattern supplies such an affine description; redundant
cells and shared boundaries are allowed. The affine equality must hold on the
entire claimed cell, not just at one sampled input. Additional application-domain
constraints are appended to D_sigma and d_sigma.

For each cell whose joint source set (7) is nonempty, apply (8). Then

    F(z) >= v^T g for every admissible (g,z)

**iff** every nonempty source/cell pair admits a certificate `(lambda_sigma,
nu_sigma)` satisfying (8). Each cell with an empty joint source set must instead
be identified as empty; it produces no admissible operational use.

**Proof.** The global implication restricts to each cell. C35 gives the
corresponding multipliers. Conversely, every admitted input is in at least one
cell; that cell's supplied inequalities prove the common query bound. The cover
must include the input and the same F is used on shared boundaries. QED.

For finite rational A,B,eta0,cell data and network weights, the feasible linear
certificate system has a rational solution whenever it has a real one. One
way to see this is to eliminate variables by rational row operations and use
a rational point in the relative interior of the resulting nonempty rational
polyhedron (or the independent-support construction of S4). This is an existence
statement, not a practical bit bound or an efficient activation-case search.

This construction specializes finite linear implication to finite ReLU regions.
It is not a novel general neural-verification algorithm. It gives a precise
candidate interface that does not require forcing a trained network to obey
logic rules in its architecture. The potentially exponential case count,
source fidelity, and floating-point evaluation error remain separate obligations.
A rational proof for the ideal real-valued network does not silently bound the
rounding error of the deployed floating-point implementation.

### A positive and negative network with the same simple training-domain behavior

For one source `g<=z`, define

    F_good(z)=z+ReLU(z-1),
    F_bad(z) =z-ReLU(z-1).

Both equal z on z<=1, so observing only that domain cannot distinguish them.
For z>=1 the good network equals 2z-1; C35's certificate with lambda=nu=1
and domain -z<=-1 proves it sound. For z<=1 the identity branch has lambda=1,
nu=0. Thus all cells of the good network have certificates.

For z>=1 the bad network is the constant 1. Its certificate would require
`lambda=1` and `1+nu=0`, impossible for nu>=0. At z=g=2 it returns 1<2,
providing an actual countermodel rather than merely a failed certificate.
The identity term z can itself be represented by `ReLU(z)-ReLU(-z)`, so both
are ordinary finite ReLU MLP functions. These are constructed controls, not
trained systems or evidence of emergent logical reasoning.

### Concavity remains optional for soundness

The good network above is convex, not concave. S4's concavity condition
characterized a *global minimum-of-certificates representation*, not all sound
bounds. Domain-premise certificates let a more general sound piecewise-affine
function be justified region by region. In the concave case, essential affine
pieces are global upper supports. If such a function is globally sound on the
source chart, each global piece itself is sound there and admits a lift (9).
Then a finite minimum of these lifted bounds reconstructs the function. The
local and global proof organizations should not be conflated.

## 6. F04-C37 — validity of an explanation and identifiability are different

For clarity first use eta0=0 and no additional domain rows. Given an observed
linear coefficient alpha, the possible source explanations form the polyhedron

    L_alpha={lambda>=0 : A^T lambda=v, B^T lambda=alpha}.        (10)

A nonempty set supplies possible valid explanations. It does not identify which,
if any, the network causally implements. Even exact observations on every input
in the chart can leave this ambiguity. All conclusions here concern this
predeclared linear explanation family, not every conceivable mechanistic model.

### Exact uniqueness criterion, including boundary cases

Fix lambda0 in (10), and let I0 be its zero coordinates. Then (10) is a singleton
iff the following cone contains only zero:

    {d : A^T d=0, B^T d=0, d_i>=0 for every i in I0}.           (11)

**Proof.** Any other feasible lambda gives a nonzero d=lambda-lambda0 in (11).
Conversely, for a nonzero d in (11), choose a sufficiently small t>0. The
coordinates that start positive remain nonnegative in lambda0+t d; zero
coordinates remain nonnegative by (11). Both equalities are unchanged. This
is a distinct feasible explanation. QED.

If lambda0 is strictly positive, this reduces to a nullspace/rank test: the
stacked matrix `(A^T;B^T)` must have full column rank. That rank condition is
sufficient but not necessary at the boundary. With three source coefficients,
constraints `lambda1+lambda2+lambda3=1` and `lambda1=1` force `(1,0,0)` despite
the nontrivial linear nullspace spanned by `(0,1,-1)`. Its directions fail the
nonnegativity condition at the zero coordinates.

A translated chart with eta0!=0 additionally has the intercept inequality in
(9). Its active inequality must also be included in a uniqueness test. Formula
(11) is not asserted unchanged for that enlarged setting.

### Which interventions can distinguish explanations?

Suppose a meaningful source perturbation u changes the bound of one fixed
linear certificate by `lambda^T u`. Two explanations lambda and mu are
indistinguishable under a declared subspace U of perturbations exactly when

    lambda-mu in U-perp.                                     (12)

This follows directly by subtracting their linear predictions. In particular,
all source shifts u=A z are uninformative about *which certificate* is used:
every valid certificate predicts the same change `v^T z`. Such covariance
checks can test semantic compatibility, but cannot distinguish alternatives
that all satisfy the compatibility law.

There is also a finite measurement-count result. For a nonempty convex
explanation set L, put `T=span(L-L)` and q=dim(T). All explanations can be
distinguished by perturbations chosen from U iff `T intersect U-perp={0}`.
When this holds, q suitably chosen scalar perturbation responses suffice; fewer
than q cannot distinguish every member of L through linear measurements.

**Proof.** Sufficiency follows by choosing q members of U whose restrictions
span the dual of T; the condition on the annihilator guarantees that span.
Necessity is not merely a formal dimension count: choose a relative-interior
point of L. Every sufficiently small movement in T remains in L. If the
measurement map has a nonzero kernel direction in T, two nearby members of L
have the same responses. Fewer than q linear measurements necessarily have
such a direction. QED.

This is not a lower bound for arbitrary nonlinear encodings, nor a promise
that the required interventions are physically meaningful or available.
Those are additional assumptions. In a degenerate singleton q=0.

### Precision can defeat an otherwise identifying intervention

In the duplicate-row example, let lambda=(1-t,t), t in [0,1]. A perturbation
u=(1,1+epsilon) produces response `1+epsilon*t`. It identifies t when epsilon
is nonzero, but an absolute response-error bound rho gives a t-error bound of
rho/abs(epsilon). At epsilon=0 no precision suffices. The perturbation
u=(0,1) instead gives t directly. The meanings, units and magnitudes of the
perturbations must be fixed to make this comparison legitimate.

Thus source-proof checking, observational identification, intervention access,
and numerical conditioning are separate requirements. None is supplied merely
by naming a hidden activation a cost or residual.

### Invisible redundant proof weight can hide arbitrary sensitivity

Take `A=(1,-1)^T`, v=1 and reachable evidence eta=(z,-z). The sources fix g=z.
Every coefficient vector

    lambda_t=(1+t,t), t>=0,

is a valid certificate and gives exactly z on the entire chart. They cannot
be distinguished there, however many noiseless examples are observed. Widening
both source bounds by rho>0 gives the bound

    z+rho+2*t*rho.

All these bounds remain sound, but their excess sensitivity is unbounded as t
grows. The tight source conclusion is only `g<=z+rho`, supplied by t=0.
A minimal-sensitivity representative can be selected by an additional criterion,
but that is a choice by the analyst, not an identification of the network's
internal procedure. A valid numerical explanation is not automatically the
best or uniquely justified explanatory object.

## 7. F04-C38 — coherent weakening probes at a proof-selection boundary

Nonnegative perturbations eta->eta+t u, u>=0, t>=0, preserve every previously
feasible target g. They loosen bounds rather than fabricate stronger evidence.
This gives a natural *candidate* intervention family when the model accepts
such source-bound inputs. It does not guarantee that a corresponding low-level
neural intervention has been found.

For a fixed finite proof portfolio

    f(eta)=min_j lambda_j^T eta,

let I be the indices active at eta0. For each fixed direction u, its right
one-sided derivative is

    d_f(u)=min_{j in I} lambda_j^T u.                          (13)

**Proof.** Inactive entries have a strictly positive gap at eta0. There are
finitely many, so for sufficiently small positive t none undercuts all active
entries along this fixed direction. Active entries have common initial value;
the smallest directional slope determines the minimum. QED.

Independent directional derivatives must not be assembled into one linear
certificate. For `f(eta)=min(eta1,eta2)` at eta0=(0,0), both positive coordinate
derivatives are zero, while `d_f((1,1))=1`. The vector of separate coordinate
derivatives (0,0) fails the source query `lambda1+lambda2=1`. This is a
mathematical behavior of the function, not an autodiff implementation bug:
each coordinate direction selects a different valid proof.

A coherent procedure first moves to a single declared affine cell and probes
there without crossing its boundaries. For example moving to (epsilon,2epsilon)
selects the first source; sufficiently small further perturbations recover
(1,0). At a cell `Dz<=d`, the positive step along u must obey every inequality
`D_i(z+t u)<=d_i`. Its maximal allowed positive size is bounded by
`(d_i-D_i z)/(D_i u)` for each row with D_i u>0. A strict interior point allows
a common positive step for any finite list of directions.

### When source-valid weakening directions can expose the full active proof hull

Let C be the convex hull of the active coefficient vectors at eta0. Suppose
there is a strict feasibility witness g0 with

    s=eta0-A g0 > 0 componentwise.

All active coefficients then have the same inner product with s:

    lambda^T s=f(eta0)-v^T g0=:k.

For any finite direction w, choose t large enough that u=w+t s>=0. Equation
(13) gives

    d_f(w)=d_f(u)-t*k.                                       (14)

Thus exact directional behavior under source-valid weakenings determines the
behavior in *every* direction. In turn it determines C: a point outside the
compact convex hull can be strictly separated by a linear functional, whose
minimum distinguishes it from the actual hull. Equivalently,

    C={lambda : lambda^T w>=d_f(w) for every w}.

Every exposed vertex of this finite hull can also be selected by a weakening
direction: take a direction that uniquely minimizes at that vertex and add t s;
the common added term t k leaves the minimizer unchanged. The local probe uses
a sufficiently small step along that direction, so old inactive entries do not
interfere. A large direction magnitude does not license a large physical step.

This is a positive result with explicit conditions, not a claim that finite
noisy probing recovers every explanation or that all valid certificates are
actually present in the network. The hull is the *active finite portfolio*, not
the whole nonnegative dual feasible set. Strict feasibility matters to the
argument; exact-equality source systems can lack the positive slack vector s.
Attributions to duplicated identical proofs cannot be recovered from scalar
behavior, even when their common coefficient is identified. Provenance and
causal implementation need additional evidence.

## 8. F04-C39 — reusing a proof when the evidence chart changes

A certificate is more useful if it carries explicit conditions for revision.
Let w=(g,z), and write the old stacked source/domain system as `Mw<=b`.
A supplied gamma>=0 proves a desired linear form q through `M^T gamma=q`.
Now the context is explicitly replaced by `M'w<=b'`, and the intended query
is q'. Do not pretend this is the same unchanged request. Retaining gamma gives

    q'^T w <= b'^T gamma+r^T w,
    r=q'-M'^T gamma.                                         (15)

An accepted outer enclosure `W` for w therefore gives the conservative bound

    q'^T w <= b'^T gamma+h_W(r),
    h_W(r)=sup_{w in W} r^T w.                               (16)

This bound can be checked against the new output intercept/tolerance. The
coefficient identity may change, but the change must be paid for rather than
silently treated as zero.

For the explicit shared-source enclosure

    W={w0+N t+C e : t in R^r, |e_i|<=1},

its residual support is finite exactly when `N^T r=0`. In that case

    h_W(r)=r^T w0+sum_i |(C^T r)_i|.                          (17)

**Proof.** If `N^T r` is nonzero, choose t along that vector with arbitrarily
large positive length; the linear form diverges. Otherwise t disappears and
each bounded coordinate independently maximizes at the sign of its coefficient.
Those sign choices attain (17). Combining the new premise inequalities with
this support bound proves (16). QED.

Failure of `N^T r=0` means *this particular outer-enclosure correction* has no
finite value. The intersection with the new source rows might still bound the
query, or another certificate might work; it does not prove the query itself
unbounded in every more informative model.

### Small coefficient errors can have very different meanings

Take `w=(g,z)`, shared direction N=(1,1)^T, and bounded discrepancy
`g-z in [-1,1]`, represented by w0=0 and C=(1,0)^T.
A residual `(epsilon,-epsilon)` has support abs(epsilon), despite g and z
being individually unbounded. A residual `(0,epsilon)` has infinite support
for any nonzero epsilon. Thus a small norm of the coefficient error does not
by itself justify a small correction. Its relation to the uncontrolled source
directions matters.

Similarly the inference from `g<=z` to `g<=(1+epsilon)z+c` cannot be made
uniformly sound for all real z with any finite c when epsilon!=0: set g=z and
send z in the unfavorable direction. Exact matching along that unbounded
direction is a structural obligation, not a replaceable numerical tolerance.

This gives a quantified version of phase one's evidence-locality discipline:
a changed source/interface does not always require discarding a proof, but the
retained proof needs a checked residual and a valid same-source enclosure.
The enclosure and empirical mode are premises; the algebra does not certify
its own statistical applicability. No ungrounded self-endorsement is introduced.

## 9. Same-controller reconstruction: numerical invertibility can hide lost improvement

Use the existing report-dependent controller, not a new decision model:

    H_(a,b)(r)=a r+b(1-r), a,b in [0,1],
    J_(a,b,z)(r)=5 H_(a,b)(r)+z, z>=0.

The report r controls branch selection. Fix r0=3/4 and r1=19/20, with both
reports required to satisfy `H(r)<=r`. Their cost difference is exactly a-b;
the shared, unbounded nonnegative baseline z cancels.

In addition to the physical and report constraints, retain the evaluator rows

    a-b<=-1/2,       -b<=0.                                  (18)

The source is nonempty: (a,b)=(0,1/2) satisfies it and both report requirements.
The first row is already a certificate of an expected-cost improvement of at
least 1/2. Its truth about the actual controller remains an empirical premise.

Apply the invertible R=((1,1),(0,1)) to just these two evaluator rows, but make
the mistaken semantic weakening of keeping only independent upper bounds:

    a-2b<=-1/2,      -b<=0.                                  (19)

All physical and report constraints are otherwise unchanged. The relaxed source
now allows `(a,b)=(11/14,9/14)`. The old report constraint is tight:

    H(r0)=(3/4)(11/14)+(1/4)(9/14)=3/4.

The new one is valid as well: `19a+b=109/7<=19`. The cost increase is now 1/7.
This is the exact best bound in the relaxation: combine

    (4/7)*(a-2b<=-1/2) + (1/7)*(3a+b<=3)

and obtain `a-b<=1/7`, attained by the displayed point. The second premise is
the old report requirement multiplied by four. No estimate of the absolute
baseline is needed anywhere.

Thus an invertible data transformation, incorrectly interpreted, changes what
can be established from improvement `<=-1/2` to possible deterioration `<=1/7`.
It has not changed the actual controller or refuted the original evidence; it
has forgotten an inferential constraint. Retaining the transformed slack cone
from C34 restores (18) and the useful bound exactly. At the relaxation witness,
its transformed slacks are `(t1,t2)=(0,9/14)`, violating the omitted t1>=t2.

This example uses two fallible branches, valid report-dependent behavior, a
single deployed policy pair across all models, and nonnegative absolute costs
unbounded above. It connects the new source-interface tests back to F04's
reflective and loss-grounded question, rather than merely renaming arbitrary
linear algebra a calculus.

## 10. Fresh reconstruction of the linear alternative and its guards

The lift theorem was first derived by reducing to the inherited S3 result. A
separate same-agent reconstruction now checks that its strongest implication
has not smuggled in feasibility, closure, or a missing intercept condition.
This is self-review, not an independent reviewer.

For a finite system `Mx<=b`, form the cone generated by the finitely many
vectors `(M_i,b_i)` and `(0,1)`. Its members are exactly

    (M^T gamma, b^T gamma+t), gamma>=0, t>=0.

This cone is closed: every conic combination can have linearly dependent
positive-support generators eliminated until only independent generators
remain. There are finitely many independent subsets. The cone over each such
subset is closed, because the injective linear map from its coefficient space
has a continuous inverse on its finite-dimensional image. A finite union of
these closed cones is closed. The overall cone is convex by its definition.

If (q,c) is not in it, a separating vector (u,s) has nonnegative inner product
with every generator and negative inner product with (q,c). Thus

    M u+b s>=0,  s>=0,  q^T u+c s<0.

For s>0, x=-u/s is feasible and q^T x>c. For s=0, take any feasible x0;
then x=x0-t u stays feasible for t>=0 and its queried value grows without
bound because q^T u<0. This latter step explains precisely why a nonempty
source set is required. Conversely a cone representation of (q,c) is exactly
a certificate and cannot coexist with a violating feasible x. This recovers
(1), and consequently (8), without a circular definition of validity.

Finite cone separation itself can be seen by projecting (q,c) onto the closed
convex cone. If k* is its nearest point, the vector k*-(q,c) is nonnegative
on the cone, vanishes on k*, and has strictly negative product with (q,c).
Thus no unverified infinite-dimensional separation principle is being used.

### Further source-transform boundary checks

For a rectangular nonnegative R, a universal equivalence

    s>=0 iff R s>=0 for every s

holds exactly when each original coordinate has at least one row of R that
is a positive pure copy of that coordinate. Sufficiency is immediate. For
necessity, if coordinate i has no such row, set s_i=-1 and every other s_j=T.
Every row involving i also has a positive coefficient elsewhere; finitely many
rows allow a common sufficiently large T making R s>=0. Rows not involving i
are already nonnegative. This contradicts the equivalence. Equivalently, there
is a nonnegative S with S R=I. A universal fixed linear orthant rewrite therefore
cannot discard an arbitrary original premise.

This is **not** a lower bound on all adaptive or nonlinear reasoning. For
`g<=eta1, g<=eta2`, the single derived row `g<=min(eta1,eta2)` preserves the
whole current scalar feasible set. Its selected source or case proof must still
be retained, and the one number need not support arbitrary later corrections
without reopening the original evidence. Query-adapted compression remains
possible, as C33 and the earlier F04 examples established.

### A finite piece test for numerical factorization, separate from logical transport

Let R have full row rank, and let f be a finite continuous piecewise-affine
function on all R^m. There is a finite continuous piecewise-affine F with
`f(eta)=F(R eta)` iff every essential affine-piece gradient of f lies in the
range of R^T. Indeed factorization makes each gradient vanish on ker R.
Conversely, that gradient condition makes f constant on each line in a kernel
direction: on ordinary cells its directional slope is zero; boundary-contained
lines follow by continuity from nearby lines. A linear right inverse J of R
then gives F(y)=f(J y), with finite piecewise-affine structure, and
`eta-JR eta in ker R` proves the equality.

This is a useful finite structural test, but finding all relevant pieces can
still be expensive. It does not license testing only observed training cells.
The pulled-back piece coefficients can lie in range(R^T) without lying in
`R^T R_+^k`. Consequently numerical factorization can succeed while positive-
premise certificate transport fails. C34's invertible triangular example is
exactly such a case. For comparison, `min(eta1,eta2)` cannot factor through the
single sum eta1+eta2: (0,2) and (1,1) have the same sum and different minima.

### Cached report validity in the reflective example is not self-endorsement

The original rows (18), together with b<=1, give

    H(r)=b+r(a-b)<=1-r/2<=r for r>=2/3.

Thus both fixed reports in section 9 can be certified from the original source
before any representation change. Keeping those report inequalities in the
relaxation can be understood as retaining already established fixed-stage
facts. Their provenance still depends on the original evidence; a retraction
would require reconsideration. The comparison does not assume that a report
becomes true merely because the controller issues it.

## 11. Candidate implications and what is still not established

The arithmetic-certificate route and a source-set/value-transformer route
produce the same sharp finite-linear conclusions when given the same complete
source context. C35 is a translation between such representations, not evidence
that one is inherently more powerful. The meaningful discrimination is what
happens when each retains a different *summary* or discards a side condition.

| Offered representation/claim | Positive result | Exact limitation |
|---|---|---|
| Nonnegative aggregated upper bounds | Certificates pull back and some queries remain exact | Other original implications can disappear |
| Invertibly recoded numerical data | Old values can be reconstructed | Reinterpreting the image as the old orthant can lose order information |
| Scalar neural value on a known affine chart | A source/domain lift can certify it | Ambient gradients need not be source coefficients |
| Region-scoped ReLU interpretation | Each nonempty cell admits a finite linear proof iff the stated bound is sound | No cheap global case search, empirical source validation, or hidden-mechanism identification follows |
| Observed certificate fingerprint | Compatible explanations form a testable linear family | Correlated observations, boundaries and limited precision can prevent unique identification |
| Retained proof under a context revision | A residual-support correction can keep it useful | Small unmatched errors in an uncontrolled direction need not admit any finite correction |

For the prospective neural experiment, this pass adds three necessary controls:
predeclare the source chart and allowed interventions; distinguish a single
observed coefficient from its set of valid lifts; and use coherent same-region
probes rather than assembling different directional limits into one proof.
A proof checker can establish that a network output is a valid bound relative
to its premises. It cannot establish that those premises are true or that the
network internally follows the analyst's proposed proof. That final claim
needs the planned intervention evidence and competing-explanation controls.

### An important unchanged query restriction

C35–C36 fix v. When the selected policy/query itself changes with input,
`v(z)^T g` can be bilinear rather than affine. The displayed linear alternative
cannot then be applied with a silently frozen v. For example `g<=1, z>=0`
implies `z*g<=z`; the multiplier is now z, not one fixed coefficient for all
inputs. Allowing z<0 destroys that implication when g has no lower bound.
A pointwise certificate can still be checked for each proposed v, or a richer
arithmetic calculus can retain the multiplication and sign premises. Uniform
parameterized certificates require additional derivation. This is a concrete
boundary where RLL's richer arithmetic or another candidate may matter.

A neural layer might propose both a bound and a certificate, but training with
that extra output would be a different empirical question from discovering
proof-like structure in an unconstrained existing network. No such training,
full verification engine, or permanent interface is adopted in F04 here.

The next bounded question is to compare certificate cost and retained information
on the *same* source-changing workload, including parameterized queries, rather
than generating another unrelated catalogue of examples. The source-preserving
and transformer routes both remain viable. Gate A is not attempted in this note.

## 12. Final coordinate and scope reconstruction

A further same-agent pass separates three operations that can otherwise all be
called a 'change of representation'. These corollaries use the same C33–C35
claims, not another proposed calculus.

### Latent-target coordinates versus source-premise coordinates

For an invertible target-coordinate change `g'=Tg`, the source matrix and
query become `A'=A T^-1` and `v'=T^-T v`. The same certificate lambda obeys
`A'^T lambda=v'`; its numerical bound is unchanged. No positivity restriction
on T is needed, because this transforms the unknown coordinates, not the order
of the premise list. Treating this as if it were a nonnegative row aggregation
would conflate two different interfaces.

An arbitrary invertible row change R can also be exact if its *order cone*
travels with it. For `C=R(R_+^m)`, its dual cone is

    C*={mu:R^T mu>=0}=R^-T(R_+^m).

The transformed slack condition is `R eta-R A g in C`. Every old certificate
lambda corresponds to `mu=R^-T lambda in C*`, with

    (RA)^T mu=v,    (R eta)^T mu=eta^T lambda.

The coefficient mu may have negative ordinary coordinates without being an
invalid dual-cone certificate. What is invariant is nonnegativity *on the
specified slack cone*, not a sign convention after forgetting that cone.
C34's failure arose precisely from replacing C by the larger ordinary orthant.
This preserves the phase-one distinction between value space and its declared
comparison preorder.

### Input coordinates and interventions must be transported together

Let `z'=Uz+t`, with U invertible. In C35 replace

    B' = B U^-1,       eta0'=eta0-B U^-1 t,
    D' = D U^-1,       d'=d+D U^-1 t,
    alpha'=U^-T alpha, c'=c-alpha'^T t.

The same lambda,nu satisfy (8) in the new chart. In particular
`B'^T lambda-D'^T nu=alpha'`, and the intercept inequality changes by exactly
`-alpha'^T t` on both sides. A direction u becomes Uu, so its predicted scalar
response is unchanged: `alpha'^T Uu=alpha^T u`.

Even the simple coordinate reversal z'=-z turns the valid source `g<=z` and
bound f(z)=z into `g<=-z'`, f'(z')=-z', with a negative input derivative but
the unchanged nonnegative source certificate lambda=1. This is harmless
recoding, unlike negating an upper-bound premise while retaining its original
inequality direction. Interpretability tests need the declared map, not a rule
that every observed gradient must be positive.

An uncertainty correction is covariant as well. Under eta'=R eta and
`U'=R U`, the corresponding certificate mu=R^-T lambda satisfies

    sup_{u' in U'} mu^T u' = sup_{u in U} lambda^T u.

If a procedure instead replaces U' by a box containing it, it may lose relevant
correlations and inflate the correction. That is a new abstraction step, not
a failure of the exact coordinate transformation.

### Boundary checklist after reconstruction

* C33 assumes nonnegative aggregation and a common target; no coverage level
  is created by deriving or duplicating rows.
* C34 distinguishes data invertibility, order-cone preservation and query-
  specific adequacy; its orthant result is not a theorem against compression.
* C35 uses a nonempty joint source/domain set and the minus sign on D^T nu.
  A region multiplier is not relabelled as empirical source evidence.
* C36 fixes the query v and needs the affine expression to hold on the entire
  stated cell. A fitted gradient at one point does not establish that fact.
* C37 identifies only a specified linear explanation family. Its rank-only
  condition needs an interior coefficient; boundary uniqueness uses (11).
* C38 uses a finite portfolio, coherent directions and, for full hull recovery
  from weakening probes, a strict feasible source witness. A zero derivative
  in each separate direction is not a joint linear explanation.
* C39 bounds the residual on a supplied joint enclosure. An infinite correction
  rejects that proof-reuse method, not every possible proof of the conclusion.

All these checks are conditional mathematics. None establishes a final utility,
a factive empirical self-report, a discovered neural circuit, or unrestricted
reflection. Their purpose is to make a small loss-grounded inference capability
both useful and testable while leaving those larger questions open.

### A failed proof transport can be repaired by a different compatible proof

Combine C33 with C35. A whole affine bound on the chart survives positive
aggregation R exactly when its lift family contains a certificate with
`lambda=R^T mu`, mu>=0 (and the corresponding domain multiplier nu). This is
(8) applied to the aggregated chart `(RA,RB,R eta0)`. It can succeed even
when the currently cached lambda has no such factorization.

For duplicate sources on eta=(z,z), the bound f=z can use either (1,0) or
(0,1). Dropping the first row cannot transport the first proof literally, but
the second proof still establishes the same bound on that chart. If future
inputs allow the two bounds to differ independently, that equivalence no
longer follows. Proof identity, proof-family adequacy, and permitted future
contexts remain separate observations.

### Negative evidence derivatives do not alone refute a valid upper bound

Even on independent evidence coordinates there can be a valid but deliberately
loose bound with a negative local derivative. With duplicate left-hand-side
sources, put t=eta1-eta2 and

    F(eta)=eta2+ReLU(t)-2 ReLU(t-1)+ReLU(t-2).

For t<=0 this is eta2>=min(eta1,eta2). For 0<=t<=1 it is eta1; for
1<=t<=2 it is eta2+2-t>=eta2; and for t>=2 it is eta2. Hence it is always
an upper bound on the source query. On the middle cell its affine expression
has coefficient (-1,2) and intercept 2. The source-only gradient check fails,
but C35 certifies it: use source weight lambda=(0,1) and the domain inequality
`t<=2` with multiplier one. The interval's other boundary is needed to establish
the network's affine expression, but need not have positive proof weight.

The negative derivative reflects a decreasing *slack in a conservative bound*,
not a negative source-evidence weight. This example prevents rejection of a
sound unconstrained network solely because its local gradient is not a global
minimum-of-proofs fingerprint. Conversely, certifying the slack by a region
premise does not demonstrate a specific hidden reasoning mechanism.

The triangular slack has another useful expression:

    ReLU(t)-2 ReLU(t-1)+ReLU(t-2)=ReLU(1-|t-1|)>=0.

Thus the same bound can also be proved globally as the second source bound
plus a nonnegative slack. That is a different proof organization from its local
affine gradients. An algebraically rewritten network with the same output is
not thereby evidence that the original network uses that particular hidden
factorization; the distinction motivates the already-planned causal controls.

Finally, scoped self-reference is not excluded by the input-domain treatment.
An affine feedback equation involving a report, after a ReLU cell is fixed,
becomes linear equalities (two inequalities each) on that cell. Certificates
can reason conditionally over those solutions. For example `r=ReLU(z)` and
`z=(1-r)/2` have the unique feasible positive-cell solution r=z=1/3; the
negative cell would require z=1/2<=0 and is infeasible. This finite example
admits feedback without unrestricted self-certification. A proof about all
solutions does not itself supply existence, selection, iteration convergence,
or empirical correctness of the feedback model. The existing reflective
controller results and those separate obligations remain in force.
For the parameterized equation `z=beta*(1-ReLU(z))`, beta>=0, the same cell
analysis gives the unique solution z=beta/(1+beta). But at beta=1 the iteration
started at zero alternates between zero and one forever. For 0<=beta<1,
`|z_(n+1)-z*|<=beta*|z_n-z*|` instead proves convergence by induction. These
calculations confirm why solving/validating a feedback constraint must not be
reported as validating the algorithm that repeatedly evaluates it. They do not
extend the probabilistic controller model to negative failure probabilities.

### Post-test hostile check: the weakening-hull theorem has real restrictions

Without a strict feasible source at the base, different active proof hulls can
be indistinguishable under *every* feasible evidence change. Let A=(1,-1)^T,
v=1, eta0=(0,0). Compare portfolios `{(1,0)}` and `{(1,0),(2,1)}`. Both
coefficients in the second portfolio are active at eta0. The source is feasible
exactly when eta1+eta2>=0; on that whole domain the extra certificate is no
smaller, so both functions equal eta1. There is no strict feasible source at
eta0. The additional active coefficient cannot be identified from valid-input
behavior, and has no distinctive effect on that declared domain.

The zero-intercept/homogeneous portfolio restriction matters too. Even with a
strict source witness at eta0=(1,1), the two sound affine bounds

    f1(eta)=eta1+2,
    f2(eta)=min(eta1+2, 2 eta1+eta2)

agree after every nonnegative weakening from eta0, but have different active
slope hulls there. The underlying source again has A=(1,-1)^T; g0=0 is now
strictly feasible. Their difference is exposed at the still-feasible input
(1/2,1/2), where f1=5/2 and f2=3/2. Offsets prevent the common-slack shift in
(14) from adding the same constant to every active slope. Hence C38 must not
be transferred to all affine or arbitrary region-certified neural bounds.
Neither counterexample affects the broader soundness/lift test C35–C36.
