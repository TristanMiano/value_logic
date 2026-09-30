# F08 final penalty refinement: source geometry and loss sensitivity

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
This is a bounded refinement of U17, not a new native rule or integrated
optimizer. It reconstructs an elementary polyhedral error bound from the
already derived linear alternative. No novelty is claimed for this classical
type of result; terminology and closest formulations remain for F10's audit.

## 1. Fix the coordinate gauge and the row matrix

Fix the target unit u and its relevant source coordinates as in U1. Encode
their numerical values in unit u using `(1/k_v)*Phi_v(src(x))`. This is a
chosen mathematical coordinate gauge. The resulting distance is not a
canonical utility, probability or physical metric independent of that choice.

In these coordinates, write each converted reduct case as

    P_h(theta_h) = {y : A_h*y <= theta_h}.

The matrices are finite rational and fixed. Each theta under consideration
must make every case nonempty; full context admission supplies such witnesses.
The characteristic violation from U12 is

    V_h(x) = max(0, max_r(A_hr*x-theta_hr)),
    V(x) = min_h V_h(x).

For a row-free case use V_h=0. Fixed positive path factors have already been
included in A and theta. One cannot change those factors while pretending
that the same matrices and coordinate gauge remain fixed.

## 2. A finite affine formula for distance to one case

Define the mathematical distance

    d_h(x) = min_(y in P_h) ||x-y||_1.

The minimum exists. For a rational x, the following rational LP is feasible,
bounded below by zero, and attains its optimum by 04a A3:

    minimize sum_i z_i
    subject to A_h*y<=theta_h,
               y_i-z_i<=x_i,
              -y_i-z_i<=-x_i.

For an arbitrary real x, existence also follows directly by restricting to
the closed ball of radius `||x-y_0||_1+1` around x for any feasible y_0. This
restriction is nonempty and compact, and points outside it cannot improve on
y_0. The continuous norm attains its minimum on the restricted feasible set.

The last two rows imply z_i>=|y_i-x_i|, so a separate z>=0 row is unnecessary.
Both y,z are mathematical free coordinates; they are not new native sources.
At any optimum z_i=|y_i-x_i|, because otherwise reducing that coordinate
strictly reduces the objective without breaking a constraint.

Apply the affine certificate construction to the maximization of -sum z_i.
Let lambda,mu,nu be the nonnegative weights on the three displayed row groups.
Coefficient cancellation gives

    A_h^T*lambda+mu-nu=0,       mu+nu=1.

Thus `||A_h^T*lambda||_infinity<=1`, and the optimal distance is
`lambda^T*(A_h*x-theta_h)`. Conversely, any such lambda can be completed by

    mu=(1-A_h^T*lambda)/2,   nu=(1+A_h^T*lambda)/2,

which are nonnegative and sum to one. Directly, for every feasible y,

    lambda^T*(A_h*x-theta_h)
      <= (A_h^T*lambda)^T*(x-y) <= ||x-y||_1.

Consequently the exact dual domain is

    D_h = {lambda>=0 : ||A_h^T*lambda||_infinity<=1}.   (D)

It depends only on the matrix. It contains zero and is pointed, although it
need not be bounded. Introduce unique nonnegative slacks for its two sets of
inequalities to put it into the standard form used in U11. The minimal-support
optimizer argument then gives a rational vertex optimizer for every finite
objective, and only finitely many vertices exist. Let E_h be their complete
set. For every rational x,

    d_h(x) = max_(lambda in E_h) lambda^T*(A_h*x-theta_h).  (d)

This extends to real x as well. Distance is 1-Lipschitz by the triangle
inequality (taking infima in each direction); the finite affine maximum on
the right is continuous. Approximate x by rational points and use equality
there. Alternatively, the same elimination proof works with real RHS, omitting
only its rational-witness assertion. Thus d_h is a finite rational CPWA function
and can be expressed in the admitted unit-u syntax.

This argument never assumes that P_h is bounded or has a vertex. A line, a
halfspace and a polyhedron with arbitrary nuisance directions are covered.
It also explains why arbitrary dual rays need not be retained in d: feasibility
of P_h gives `r^T*theta_h>=0` for every r>=0 with A_h^T*r=0, so such a recession
direction cannot increase this objective.

## 3. A matrix-uniform finite coefficient

Set

    H_h = max_(lambda in E_h) sum_r lambda_r,
    H = max_h H_h.

These are finite nonnegative rational numbers. Every residual row value is at
most V_h(x), so every affine leaf in d satisfies

    lambda^T*(A_h*x-theta_h) <= H_h*V_h(x).

Take the finite maximum to get `d_h<=H_h*V_h`. Distance to the union
P=union_h P_h is the finite minimum of its case distances. Hence

    d(x,P) = min_h d_h(x) <= H*min_h V_h(x) = H*V(x).  (EB)

There is also an explicit source-row-free native proof of EB. The lattice
injection of each affine residual into V_h, followed by its nonnegative lambda
weights, proves the corresponding distance leaf at gain sum(lambda). Use
V_h>=0 to increase the gain to H_h, then max_common over the vertices. Increase
to H and combine the case comparisons with min congruence. Source-free positive
homogeneity identifies the final min with H*V. All proof budgets are zero;
the old source inequalities were used to establish the meaning of the distance
formula, not smuggled into the unconditional inequality EB.

**Corollary U18 (geometry-controlled transfer).** In this fixed-matrix admitted
family, EB has a finite rational coefficient independent of theta. If a fixed
paired loss difference f=t-s is globally L-Lipschitz in these coordinates for
a rational L>=0, and its native old bound is b, then

    f(x) <= b+L*d(x,P) <= b+L*H*V(x)                 (G)

for every x. Choose a closest point in the appropriate closed case to justify
the first inequality; rational x has a rational closest point by the LP above.
All terms in G are finite rational CPWA, so U1 supplies a row-free native proof
at the displayed rational coefficient. Equivalently its earlier constructive
normal-form route can be used to emit that comparison.

The F07 coordinate envelope `|f(x)-f(y)|<=sum_i L_i*|x_i-y_i|` gives the sufficient
choice L=max_i L_i, with L=0 in zero dimensions. Compute it for the paired
difference, so a canceled common baseline does not create an artificial gain.
Every fixed finite CPWA expression has some finite such envelope; the statement
does not assume that one L bounds the entire unnormalized language.

Under typed source substitution, a current native proof of sigma(V)<=epsilon
therefore transfers the old bound to `b+L*H*epsilon`. One geometry calculation
can serve a family of losses with known sensitivity bounds and admitted RHS
revisions. This explains exactly how a common error tolerance becomes possible
after bounding loss sensitivity. Without that normalization, the M*x example
in U17 still rules out a universal tolerance.

## 4. The one-case coefficient is sharp over arbitrary feasible RHS

For one fixed matrix A, the coefficient H=max_(lambda in E) sum(lambda) is
the least constant working uniformly for all its nonempty rational RHS cases.
This is stronger than sufficiency but does not say H is sharp for every fixed
theta or for every union of cases.

If H=0, EB is exact at zero. Otherwise choose a vertex lambda_* attaining H
and let S be its positive support. The rows A_S are linearly independent:
a nonzero kernel direction supported on S would permit two small opposite
moves preserving lambda>=0 and A^T*lambda, contradicting extremality.

The face D_S obtained by setting all other lambda entries to zero is bounded,
because A_S^T is injective and its image is bounded by the infinity-norm box.
Its vertices are vertices of D. Thus the maximum of sum(lambda) over D_S is
exactly H: lambda_* attains it and no face vertex has larger sum.

Apply the distance formula at x=0 to the nonempty polyhedron
`{y:A_S*y<=-1}`. Nonemptiness follows by solving A_S*y=-1 using the independent
rows. A rational closest point y_* has norm H. Put delta=-y_*. Then

    A_S*delta>=1,       ||delta||_1=H.

The dual inequalities sandwich
`H=sum(lambda_*) <= lambda_*^T*A*delta <= ||delta||_1=H`.
Each positive-support row must therefore have A_r*delta=1.

Now choose theta_r=0 on S and `theta_r=max(0,A_r*delta)` off S. The origin is
a feasible witness. At x=delta, V(x)=1, while lambda_* gives distance at least
H and the feasible origin gives distance at most H. Thus d(delta,P)=H.
All coefficients, RHS and witness values are rational. Any smaller uniform
constant fails on this admitted case. This sharpness concerns freely varying
RHS; additional restrictions on which contexts may be deployed can reduce it.

For a union the maximum of the single-case constants is only asserted as
sufficient. An unrestricted case makes the union the whole space, with exact
distance zero, regardless of other cases' positive constants. For a fixed
theta, redundant scaled rows can likewise improve its exact coefficient.

## 5. A small family with arbitrarily large exact sensitivity

Take two sources x,y in unit u and a fixed rational e>0. The old source is

    x<=0,          -x+e*y<=0.

It is a cone with feasible origin. Its distance dual satisfies

    lambda_1,lambda_2>=0,
    |lambda_1-lambda_2|<=1,       e*lambda_2<=1.

Therefore sum(lambda)<=1+2/e, attained by
`lambda_*=(1+1/e,1/e)`, a vertex. The exact uniform constant is H=1+2/e.
At delta=(1,2/e), both row violations are 1. Every feasible point has x<=0
and y<=x/e<=0, so the origin is nearest in the 1-norm and its distance is H.

The paired loss f=x+y has L=1 and old bound b=0. Relax both source budgets to
R>=0. The same native weighted row combination gives

    x+y <= (1+2/e)*R,

attained at `(x,y)=(R,2*R/e)`. Thus the geometry-based transfer bound is exactly
optimal for this query and every rational R>=0. With e=1/100, even R=1/100
permits loss 201/100. Small numerical row violations do not by themselves imply
small task loss when the constraint geometry is ill-conditioned.

At e=0 the source becomes x=0 with y unconstrained. Its distance constant is
1, but f=x+y is unbounded. The distance dual now has the recession direction
(1,1); taking the supremum of sum(lambda) over *all* dual points would give
infinity even though its vertex-based distance constant is finite. This
separates the finite catalogue from an unjustified bounded-dual assumption,
and shows why changing row directions is outside the RHS-only replay theorem.

No optimizer, empirical constraint validation or new claim about practical
running time follows from this calculation. The optional gain is the explicit
factorization of a transferred guarantee, with a sharp matrix sensitivity
example and a clear boundary when the matrix itself changes.

## 6. Retaining the coordinate sensitivities avoids unnecessary slack

Instead of replacing a known nonnegative rational vector L_i by its maximum,
use the weighted seminorm `||delta||_L=sum_i L_i*|delta_i|`. The distance LP
changes its objective to sum_i L_i*z_i. Its dual domain is

    D_h(L) = {lambda>=0 : |(A_h^T*lambda)_i|<=L_i for every i}.

The same coefficient cancellation gives `mu+nu=L`, with
`mu=(L-A_h^T*lambda)/2` and `nu=(L+A_h^T*lambda)/2`. Its finite rational vertices
therefore represent the exact weighted distance, and

    H_L = max_h max_(lambda in vertices(D_h(L))) sum_r lambda_r

gives `d_L(x,P)<=H_L*V(x)`. The conclusion for a paired loss with this coordinate
envelope is `f<=b+H_L*V`, without an additional scalar L factor. The construction
is still matrix-uniform for fixed coordinate sensitivities, and its one-case
sharpness proof in section 4 works with the weighted LP objective.

Zero entries are permitted. The weighted distance is then a seminorm distance
and need not distinguish every point outside P. One must not use its zero set
in place of U12's characteristic probe for the whole query language. However,
the assumed coordinate envelope makes f independent of each zero-weight
coordinate, so the transfer argument is valid. The weighted LP remains feasible
and bounded below; affine consequence supplies an attaining optimizer even
though a weighted ball need not be compact. At an optimizer, zero-weight z
coordinates may be reduced to absolute differences without changing its cost.
If every L_i is zero, f is constant and H_L=0 suffices.

For the report rectangle `0<=p<=1, 0<=s<=1/4`, the unweighted matrix coefficient
is H=2. At fixed r>=4/7, the paired report gap

    f_r=(1-r)*p+r*s-r

has coordinate envelope `(1-r,r)`, scalar L=r, and old optimum
`b_r=1-7*r/4`. The scalar factorization would give gain 2*r. The weighted dual
instead has exact coefficient H_L=(1-r)+r=1. A direct row-free certificate
makes the latter transparent:

    f_r = b_r+(1-r)*(p-1)+r*(s-1/4) <= b_r+V.

Both upper residuals are at most the rectangular characteristic V; their
weights are nonnegative and sum to one. This gain is least for this request:
at `p=1+epsilon, s=1/4+epsilon`, epsilon>0, V=epsilon and
`f_r=b_r+epsilon`. The lower-row residuals are nonpositive at these points.

For r=3/4, the old strict budget is -5/16. A current certificate of V<=epsilon
preserves a strict native report whenever epsilon<5/16, with explicit budget
`-5/16+epsilon`. This is a conditional statement about the supplied numerical
row-violation allowance. It neither changes the mixture law nor asserts that
violated probability caps still describe an empirically valid probability
model. If additional current physical caps hold, they may give a sharper
fresh bound than this all-assignment transfer envelope.

The zero-denominator report corner remains a distinct obstruction: if the old
source contains (0,1), no negative old strict budget exists to start this
calculation. A small constraint-violation allowance cannot manufacture that
missing margin. Similarly, old b must be justified for the relevant old context;
reusing H across RHS changes does not freeze b at a historical value.

### A current probability cap gives a sharper, attained threshold

Keep r=3/4 and retain the physical caps `0<=p,s<=1`, but replace only the old
cap s<=1/4 by `s<=1/4+eta`, eta>=0. The current exact report-gap optimum is

    B(eta)=min(-5/16+3*eta/4, 1/4).

To prove the first branch, combine the unchanged p cap and the revised s cap
with weights 1/4 and 3/4, then subtract the report 3/4. Combining the two
physical upper caps gives the second branch. Native meet takes their minimum.
The common point `p=1, s=min(1/4+eta,1)` is feasible and attains the displayed
budget, proving sharpness without treating two different comparisons as one.

Consequently strict reporting holds exactly for eta<5/12, inclusive reporting
holds through eta=5/12, and at the boundary the model (1,2/3) gives equality.
The simpler universal transfer from V<=eta only guaranteed strictness for
eta<5/16. Both are correct: the scalar V allowance forgets that the p cap was
retained with zero violation. The vector allowance
`(1/4)*ReLU(p-1)+(3/4)*ReLU(s-1/4)` preserves that information. This gives an
explicit current-source example of U17's warning that a least global scalar
penalty need not give the best bound after a particular revision. It also
exhibits U11's finite min-of-affine replay budget within a physically bounded
probability source, with the report-control law held fixed throughout.
