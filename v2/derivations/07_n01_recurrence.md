# N01 recurrence notebook: justified consumers and endogenous assessment

Contributor: **Codex (GPT-6)**. October 2 local / October 3 UTC, 2026.
Attempt R-N01-01/C3, closed at target-refinement scope. A1–A4 and B1–B29
received [same-assistant reconstruction](../work_logs/N01R_2026-10-02_S1/self_review.md);
this is not external or mechanized review. This notebook does not declare
F11 or F13 complete or establish project novelty.

## A1. A scientifically meaningful priority rule

Let actions have distinct, prospectively incurred deployment costs c_i.
For a declared tolerance epsilon and source P, choose the least-cost action
whose task regret is at most epsilon throughout P, otherwise the fallback.
This is a meaningful consumer contract. Equal-cost ties need a separately
declared rule. Costs already paid to obtain estimates are sunk and cannot
be counted again as deployment savings. Source construction and proof costs
are accounted separately. A fixed arbitrary ordering of numerical formulas
does not establish this consumer's scientific relevance.

This repairs a motivation gap in the original priority fixture, but supplies
no novelty by itself. It is a robust constrained choice/early-stopping rule.
The question becomes what source distinctions this consumer actually needs.

## A2. Vector squared loss still has a small ordinary reduction

Known outputs y_i in R^d share uncertain truth theta in a bounded polytope P
and a fixed positive-semidefinite quadratic loss matrix H. Let

    L_i(theta) = (y_i-theta)^T H (y_i-theta) + c_i.

Subtracting the fallback b cancels theta^T H theta:

    L_i-L_b = d_i^T theta + k_i,
    d_i = 2 H (y_b-y_i),
    k_i = y_i^T H y_i-y_b^T H y_b+c_i-c_b.

Thus the robust query is h_P(d_i)+k_i <= epsilon, where h_P is the support
function. All pair comparisons use differences of these same directions.
The truth is needed only through its projection on span{d_i}, of rank at
most min(d, number_of_actions-1). Adding many output coordinates or actions
does not force high-dimensional decision information if this rank stays low.
The scalar two-endpoint result from the first N01 is the rank-one case.

For *all budgets* and singleton sources in a truth domain with nonempty
interior, the row space of a linear summary S must contain every d_i to
recover all comparisons: if d_i is outside that space, choose v in ker S
with d_i^T v != 0. Choose theta in the interior and small nonzero t, so both
theta and theta+t*v remain admissible. Their singleton sources have the same
summary and different query values. A budget between them separates them.
For a lower-dimensional domain, use its direction space T=span(P-P): the
correct condition is ker(S) intersect T contained in every ker(d_i^T).
Coordinates fixed by the permanent domain need not be stored. This is a
linear-summary bound, not a lower bound on arbitrary encodings, and fixed-
budget/action-only consumers may need less.

Two non-collinear directions genuinely escape scalar endpoint sufficiency,
but ordinary projected robust optimization remains the mandatory competitor.
Unknown affine model outputs introduce uncancelled quadratic terms unless
the corresponding Gram matrices agree. That enlarges the mathematics and
can leave the finite-CPWA fragment; it is not free additional breadth.

## A3. Fixed samples do not alone rescue the quadrature seed

An acquisition constraint can make arbitrary Gaussian nodes unavailable.
However, with five equally spaced samples, quartic interpolation/Boole's
rule integrates the original quartic family exactly. A comparison retaining
T_4 as if it were the strongest same-data fallback would be artificially weak.
With three equally spaced samples Richardson/Simpson is the natural classical
control. A scientific extension would have to defend a richer function class,
actual sample restrictions, numerical enclosures and cost accounting together.
Merely excluding Gaussian quadrature by fiat is insufficient.

## A4. What a scientific route would need next

A credible application can use least-cost safe deployment, joint uncertainty
and more than one consequential truth direction. It must exhibit a result
that survives projected robust optimization, policy-aware short-circuiting,
parametric LP and ordinary checked witness reuse. An audited application
finding could suffice; a claim of a new generic query-compression mechanism
does not follow. No such application benefit has been established here yet.

## B1. Candidate reflective family (under development)

Name the system's own versioned router. Its reported loss affects deployment
frequency q in [0,1], and deployment changes the loss being assessed. A small
candidate response family is r=a+b*q with explicitly supplied evidence for
(a,b). Distinguish a static fixed-point interpretation, convergence of an
update procedure, and empirical calibration of that response law. None implies
the others. A report is not evidence for its own response equation.

For known rational a,b and a continuous clipped-affine controller, the
fixed-point graph is finite piecewise affine and fits the provisional core.
For continuously uncertain b, the product b*q is bilinear and cannot silently
be treated as an affine source row. Finite scenario uncertainty and sound
outer approximation are separate possible bounded contracts.

## B2. A concrete versioned effort controller

Refine B1 to a nonnegative residual task loss r=a-b*q, with
0 <= b <= a <= 1, effort q in [0,1], fixed tolerance tau in [0,1], and
versioned gain k>0. More effort reduces residual loss; its resource price
lambda>=0 is declared separately. The controller responds to its own assessed
residual loss:

    q = clip(k*(r-tau), 0, 1),       V = r + lambda*q.

This is a deliberately small conditional self-model, not a learned empirical
response law. Evidence about (a,b) must come from outside the report being
certified, and must identify the same computation version and operating regime.
V is a task-loss/resource proxy, not ultimate utility. The interpretation as
the system's *own* computation, and the feedback dependency, are both explicit.

Set F(q)=clip(k*(a-b*q-tau),0,1). F is continuous and nonincreasing;
F(q)-q is strictly decreasing, nonnegative at 0 and nonpositive at 1.
There is exactly one fixed point. Its three closed regimes are:

    a <= tau:                  q*=0, r*=a;
    a-b >= tau+1/k:            q*=1, r*=a-b;
    otherwise: q*=k*(a-tau)/(1+k*b), r*=(a+k*b*tau)/(1+k*b).

The interior conditions can be written a>=tau and a-b<=tau+1/k.
Adjacent formulas agree at equality, so overlapping closed cases are harmless.
The denominator is >=1. These facts establish existence and uniqueness only.

## B3. A fixed-point certificate is not a convergence certificate

For k=2,a=b=1,tau=0, the unique fixed point is q*=2/3 and r*=1/3.
The raw update from q_0=0 alternates 0,1,0,1,... . With lambda=1/4,
V*=1/2, whereas the observed values alternate 1 and 1/4. Certifying the
equilibrium bound V*<=1/2 does not certify the actual undamped trajectory.

There is a cheap established control. If b<=B, use

    q_(n+1)=(1-eta)*q_n+eta*F(q_n), eta=1/(1+k*B).

The inactive slope is 1-eta=k*B/(1+k*B); the active slope is
1-eta*(1+k*b)=k*(B-b)/(1+k*B). Thus the continuous piecewise-affine update
maps [0,1] to itself and is a contraction with factor c=k*B/(1+k*B)<1.
For B=0 it reaches the constant F in one update. For B>0,

    |q_n-q*| <= c^n |q_0-q*|,
    V(q_n) <= V* + max(lambda,abs(lambda-B))*c^n.

The second inequality uses |lambda-b|<=max(lambda,abs(lambda-B)) and
|q_0-q*|<=1. It gives a finite-horizon allowance, not exact finite-time
equilibrium or empirical calibration. A later proof/implementation must name
which of the equilibrium, raw-update, or damped-update claims it receives.

## B4. One feedback denominator admits an ordinary exact LP reduction

In the interior regime define s=1/(1+k*b), alpha=s*a, beta=s*b. Then

    s+k*beta=1, q*=k*(alpha-tau*s), r*=alpha+k*tau*beta.

A source inequality A*a+B*b<=c becomes A*alpha+B*beta<=c*s.
The inverse is a=alpha/s,b=beta/s. A permanent finite b<=B gives
s>=1/(1+k*B)>0, excluding spurious points at infinity. Regime inequalities
transform the same way. Hence the transformed source is a bounded rational
polytope and q*,r*,V* are affine there. The two saturation cases are already
affine. All affine loss queries on this *one* controller have an exact
finite-polyhedral realization. This is the classical Charnes-Cooper idea;
the source audit must check its positivity and boundedness hypotheses.

Equivalently, for an interior threshold V*<=ell,

    (1+k*lambda)*a + k*(tau-ell)*b <= ell+k*lambda*tau.

That shortcut is query-specific. It does not make the graph in the original
(a,b,q,r) coordinates polyhedral. A rational coordinate change with a supplied
source translation is different from blindly applying a nonlinear numerical
presentation to the native loss operations (the F09 obstruction).

Consequence: uncertainty plus one feedback loop is not enough to justify
developing a new generic nonlinear reasoner. A strong baseline solves these
small LP cases and can emit the same receiving certificates.

## B5. Competing controllers: first simplify the comparison

Two versions k_1<k_2 act on the *same* (a,b), with the same tau and price
lambda. In every regime q* increases with k. Since V=a+(lambda-b)*q*,
the more aggressive version is better exactly where extra effort is useful
(b>lambda), apart from equal-effort/zero-loss ties. In the common interior,

    V_1-V_2 = (a-tau)*(k_2-k_1)*(b-lambda)
                / ((1+k_1*b)*(1+k_2*b)).

At zero regret budget the sign has an elementary reduction. A nonzero
declared regret allowance asks about magnitude and can defeat vertex-only
checking. This is not a generic computational-hardness claim.

Concrete fixture: a=1, b in [1/2,1], tau=0, k_1=1, k_2=2,
lambda=1/16. Both versions are interior (with a matching saturation boundary
at b=1/2 for k_2). Set

    D(b)=(b-1/16)/((1+b)*(1+2*b)).

Endpoint values are D(1/2)=7/48 and D(1)=5/32. Both are <=157/1000.
The rational interior witness b=13/16 gives D=32/203>157/1000.
Thus a vertex-only check on the original source returns the wrong answer.

Differentiate: the numerator of D' is 1+3*lambda+4*lambda*b-2*b^2.
The unique positive stationary point is

    b*=(1+sqrt(153))/16,
    max D=(13-sqrt(153))/4.

It lies strictly inside [1/2,1]. These are simple algebraic quantities;
ordinary quadratic sign analysis is a stronger reference than generic LP.
The fixture is a discriminating control, not novelty or an empirical result.

## B6. Totality and calibration obligations before cyclic certification

Let theta be an admissible external model and X(theta) the set of states
satisfying the proposed cyclic self-description. Checking a loss bound on
the union of nonempty fibers alone can silently discard models with
X(theta)=empty. Overall source nonemptiness does not establish

    for every admissible theta, there exists x in X(theta).

For B2 this obligation is discharged by the fixed-point proof for every
0<=b<=a<=1. A discontinuous deterministic threshold controller need not have
that property. For example r=q, q=1 if r<1/2 and q=0 otherwise has no solution.
Mix it with a separate safe scenario and the total source can be nonempty
while the difficult scenario disappears. This is familiar nonblocking/
non-miraculous contract reasoning, to be compared with that literature.

A native conditional proof on the reduced source remains a conditional proof;
the error is promoting it to a guarantee for all original admissible models.
Likewise, a self-reported low loss cannot supply the external premise that
its report is calibrated. Neither issue requires changing the sound core.

## B7. Separate exact models need not compose into an exact joint profile

Retain a=1,tau=0,b in [1/2,1] and gains 1,2. In equilibrium,

    r_1=1/(1+b), q_1=r_1,
    r_2=1/(1+2*b), q_2=2*r_2.

Write x=r_1 in [1/2,2/3]. Their *joint* loss curve is

    r_2=g(x)=x/(2-x),
    g'(x)=2/(2-x)^2, g''(x)=4/(2-x)^3>0.

An exact finite-CPWA source realization of the joint atom values cannot exist:
on a common finite cell partition, each affine image of a source polyhedron
is a polyhedron. If the total image equals the bounded graph, each nonempty
piece is bounded and hence a polytope, even with unbounded auxiliary source
coordinates. The total image is a finite union of these polytopes.
Every convex subset of this strictly convex graph has at most one point,
whereas the graph contains infinitely many points. Auxiliary affine variables
and projection do not evade this obstruction. Each controller separately has
the projective representation B4; their correlation is the obstruction.

Even preserving only *all affine upper-bound observations* of the joint losses
requires their closed convex hull. This hull is not a polytope: every point
on the strictly convex arc is exposed from below. A bounded finite polyhedral
image has a polytopal convex hull. Distinct compact convex sets are separated
by a strict affine inequality, which can be rationally approximated while
retaining a strict gap. Thus rational affine observations already distinguish
them. This is a representation-class bound, not a prohibition on a nonlinear
external solver or query-specific certificates.

## B8. A natural resource-price family already detects the curvature

Let lambda vary in [0,1/7], with the same two controllers and the same source.
The comparison is

    D_lambda=(1+lambda)*r_1-(1+2*lambda)*r_2.

Its sharp upper bound is

    M(lambda)=3+4*lambda-2*sqrt(4*lambda^2+6*lambda+2).

To reconstruct: maximize (b-lambda)/(1+3*b+2*b^2). The stationary point is
b=lambda+sqrt((1+lambda)*(1+2*lambda)/2), which moves from 1/sqrt(2)
to 1 as lambda moves from 0 to 1/7. Substitution gives the formula above;
the derivative is positive then negative around that point. At the upper
price endpoint it matches the right source boundary.

Writing f=sqrt(4*lambda^2+6*lambda+2) gives
f'=(4*lambda+3)/f, f''=-1/f^3, hence

    M''(lambda)=2/f^3 >= 343/864 > 0 on [0,1/7].

A fixed finite polyhedral value profile would make the sharp bound a maximum
of finitely many affine functions of lambda, hence piecewise affine. It cannot
equal this strictly convex M. Requiring exact answers for every rational
nonnegative regret budget determines M by rational cuts, so it fails too.
This uses a meaningful family of effort prices, not every imaginable affine
query. It does *not* establish failure for one fixed price/budget, nor a lower
bound on arbitrary symbolic programs: the displayed radical is already a
small ordinary exact reference.

## B9. A bounded approximation question with a quantitative target

For g on [1/2,2/3], g''<=27/16. Take N equal subintervals and the N+1
rational tangent lines at their endpoints. Their maximum t_N is below g.
Taylor's remainder around the nearest knot, at distance <=1/(12*N), gives

    0 <= g(x)-t_N(x) <= (27/16)/(8*36*N^2).

The polygon with y>=each tangent, y<=the endpoint chord and
1/2<=x<=2/3 is an outer approximation of the convex hull of the curve.
For the price queries above, its upper bound U_N satisfies

    0 <= U_N(lambda)-M(lambda) <= 27/(3584*N^2).

Indeed the y coefficient has magnitude 1+2*lambda<=9/7; maximizing over the
outer polygon chooses its lower envelope and incurs at most this coefficient
times the vertical tangent error. The chord only bounds the unused upper side.

There is also a representation-specific converse. If an affine piece of any
uniform upper bound U occupies a price interval of length h and 0<=U-M<=delta,
strong convexity yields U(mid)-M(mid)>= (343/864)*h^2/8. Therefore a
piecewise-affine upper bound with n pieces over the entire price interval needs

    n >= sqrt(7/(6912*delta)).

This is a lower bound on pieces of the *bound as a function of price*, not on
bytes, source facets or arbitrary algorithms. Together these estimates support
an order delta^(-1/2) finite-polyhedral approximation target, up to constants.
Classical convex approximation is the necessary comparison; the rate itself
must not be advertised as a newly discovered general theorem.

The candidate experiment is now concrete: checked joint-loss outer profiles,
their actual decision misses and total cost under price/source revision, versus
the exact algebraic ordinary reference and an ordinary implementation of the
same tangent construction. It can fail as a useful contribution even when all
certificates are sound. No advantage over that matched baseline is assumed.

## B10. Tangent and chord evidence can have exact rational receipts

At rational t<2 the tangent to g is ell_t(x)=(2*x-t^2)/(2-t)^2. Directly
clearing positive denominators gives

    g(x)-ell_t(x) = 2*(x-t)^2 / ((2-x)*(2-t)^2).

For rational u<v<2 the chord is c_uv(x)=(2*x-u*v)/((2-u)*(2-v)), with

    c_uv(x)-g(x) = 2*(x-u)*(v-x) / ((2-x)*(2-u)*(2-v)).

The first is valid on the permanent x<2 domain, whereas the chord uses the
current interval u<=x<=v. Widening an interval can invalidate the old chord
without invalidating its tangents. These algebraic receipts are external
source-adapter obligations; a native proof from a supplied tangent row does
not itself establish the physical response law or this identity.

Write ell_j=m_j*x+d_j, and let c_1=1+lambda,c_2=1+2*lambda. If adjacent
tangent slopes bracket c_1/c_2, solve

    w_j+w_(j+1)=c_2,
    w_j*m_j+w_(j+1)*m_(j+1)=c_1.

Both weights are nonnegative rational numbers. Combining the rows
m_j*x-y<=-d_j gives the checked bound
c_1*x-c_2*y <= -w_j*d_j-w_(j+1)*d_(j+1). If the maximizing intersection
lies outside the current interval, combine one tangent with the relevant
endpoint row instead. This is ordinary LP duality and is available equally
to the ordinary checked producer and the native producer.

Adjacent tangent intersection:

    x_j = 2*(t_j+t_(j+1)-t_j*t_(j+1))/(4-t_j-t_(j+1)).

It lies between its two knots. The formula follows by equating the two
tangents and factoring the difference of squares. Domain endpoints and these
intersections form a separate exact polygon reference for the outer profile.

## B11. Do not identify a report with actual loss

B2-B9 are exact-calibration controls. A more modest self-assessment fixture
distinguishes report z, actual task loss r, and an externally bounded bias e:

    z=A-b*q, r=z-e, q=clip(k*z,0,1), V=r+lambda*q.

Take A=1, b in [1/2,9/10], e in [-1/20,1/20], gains 1 and 2, and
lambda in [0,1/16]. The report is produced by the named versioned evaluator;
it drives the controller. The bias bound must be supplied/calibrated externally,
not inferred from that report. For every q in [0,1], r>=1-9/10-1/20>0.
The two versions are assumed to share the same response law and bias; that
is a counterfactual coupling assumption requiring its own provenance.

Equilibrium reports retain the B7 curve. Their task-loss pair is
(r_1,r_2)=(z_1-e,z_2-e), and the resource costs use q_1=z_1,q_2=2*z_2.
The shared bias cancels in V_1-V_2, but *does not* cancel in either absolute
loss or a comparison using different biases. Independent biases in the same
interval add a worst-case 1/10 to the regret. A later evidence withdrawal
that breaks shared-bias coupling must therefore invalidate the cancellation.

For an independently bounded bias, each single-controller profile is still
polyhedral after B4, by adjoining e as an independent interval variable.
The joint observation includes reports/effort as well as task losses; its
projection on (z_1,z_2) is still the curved graph. The effort-price comparison
still has the strictly convex M(lambda) on [0,1/16]; its stationary b stays
inside [1/2,9/10]. Hence the representation obstruction survives genuine
uncertainty about report accuracy.

Updated endpoint trap for this smaller interval: lambda=1/16 and regret
budget 63/400. D(1/2)=7/48 and D(9/10)=335/2128 are below that budget,
while D(13/16)=32/203 is above. There is no probabilistic calibration theorem
here; all claims are conditional on the declared source and coupling.

## B12. One observed self-assessment does not identify a revision's value

As a separate identifiability control, suppose perfect calibration, tau=0,
old gain 1, and an observed old equilibrium q=r=1/2. Then a=(1+b)/2.
With lambda=1/4, b=0,a=1/2 and b=1,a=1 both match the observation, yet
changing to gain 2 changes value in opposite directions. The old value is
5/8 in both worlds; the new values are respectively 3/4 and 1/2.

Thus the old report alone cannot justify the controller change. Two exact
observations at distinct imposed effort levels identify an affine response:
b=(r_1-r_2)/(q_2-q_1), a=r_1+b*q_1. Bounded observation errors give strips
and a slope uncertainty of at most (epsilon_1+epsilon_2)/abs(q_2-q_1).
This is ordinary experimental identification, not a new learning theorem.
The imposed effort/measurement protocol and its cost must be supplied.

This control also warns against a false complexity claim: under the single
exact old observation, regret becomes (b-lambda)/(2*(1+2*b)), which is
monotone in b for lambda>=0. Endpoint checking then *is* sufficient. The
harder B11 interval cannot be justified by silently mixing observation regimes.

## B13. Stronger ordinary control: an exact conic profile

The primary-source audit found a substantially broader simultaneous-fraction
convexification result (He, Liu and Tawarmalani, section 5.1). For this tiny
fixture a direct reconstruction suffices. On u<=x<=v<2,

    y>=g(x) iff [[4-2*x, 2], [2, 1+y]] is positive semidefinite.

Indeed its first diagonal is positive; its determinant condition is
2*(2-x)*(1+y)-4>=0, equivalent to y>=x/(2-x). Together with
y<=c_uv(x) and the x interval, this describes the convex hull of the curve.
For each fixed x the hull is the vertical interval between g and its chord:
convexity gives containment one way, and convex combinations of the graph
point and the chord point give the other way.

Thus one rational 2-by-2 positive-semidefinite constraint, two interval rows
and one chord represent *all affine observations exactly*. This can also be
expressed as a rotated second-order cone. The B7/B8 impossibility is strictly
about finite polyhedral value profiles. The price function's radical and this
conic profile are both mandatory ordinary controls. No claimed novelty or
need for a more powerful global optimizer survives merely adding this curve.

## B14. Replace constant shared bias with a stated calibration relation

In B11 let the evaluator's calibration discrepancy be an unknown function
e(q), satisfying |e(q)|<=eta and |e(q)-e(q')|<=K*|q-q'| on [0,1].
Its report law still drives the controller, while true loss is z-e(q).
This avoids identifying shared evaluator version with a constant bias.
Both uniform hypotheses require external evidence; finite calibration data
alone does not establish them without additional assumptions.

The algebra below describes the declared discrepancy class. To interpret
every member as a nonnegative primitive task loss, also require eta no
larger than the minimum report on the admitted effort/context domain (or
separately enforce nonnegativity and recheck attainability). The concrete
eta=1/20 example satisfies this sufficient condition. A larger formal bias
class is not automatically an admissible task-loss source.

For fixed b, define d=q_2-q_1=1/((1+b)*(1+2*b))>0. Then

    V_1-V_2 = D_lambda(b)+e(q_2)-e(q_1),
    worst calibration contribution = min(2*eta,K*d).

The upper bound follows from the two assumptions. It is attained: assign
values -h/2,+h/2 at q_1,q_2, where h=min(2*eta,K*d), interpolate linearly
between them and extend constantly outside. This function is bounded by eta
and has slope at most K. The adversary may choose this function separately
for each admissible b; the robust supremum quantifies both unknowns jointly.

Hence the exact worst-case regret is

    max_b min(D_lambda(b)+2*eta, D_(lambda-K)(b)).

The zero-Lipschitz case recovers common-bias cancellation. With no continuity
bound, only the amplitude term remains. If the term changes branch, the switch
solves (1+b)*(1+2*b)=K/(2*eta). An ordinary exact reference checks endpoints,
admitted stationary points of both branches, and admitted switching points.
This is a finite univariate algebraic calculation, not an inference from grid
samples. Degenerate eta=0 or K=0 is handled before division.

The calibration constraints themselves are linear in the joint report/effort
profile. Introduce t=e(q_2)-e(q_1) and impose

    -2*eta<=t<=2*eta, -K*(2*y-x)<=t<=K*(2*y-x), 2*y-x>=0.

The requested affine query is D_lambda(x,y)+t<=epsilon. The conic profile
plus these rows is a sound outer relaxation; exactness after this intersection
needs a separate argument (B16). An outer polyhedral profile also gives a sound
bound conditional on the adapter receipts. The same constructions are
available to the ordinary producer.

## B15. A concrete evidence-withdrawal decision, with unresolved self-assessment

Use B11's b interval, eta=1/20, lambda=1/16, K=1/8 and budget epsilon=1/5.
Since d<=1/3, K*d<=1/24<1/10, the Lipschitz branch is active everywhere.
The sharp bound is therefore M(-1/16)=(11-sqrt(105))/4<1/5;
its maximizing b=(-1+sqrt(105))/16 lies inside [1/2,9/10].
The inequality follows by sqrt(105)>51/5, since 105>2601/25.

Withdraw the Lipschitz evidence while retaining the amplitude bounds and
report response evidence. Now b=13/16 and e(q_1)=-1/20,e(q_2)=1/20 give

    V_1-V_2=32/203+1/10 > 1/5.

The comparison changes even though both absolute bias bounds remain the same.
An old certificate using the Lipschitz premise must not survive withdrawal.
An interval-only baseline fails to exploit the original relational evidence;
it is a diagnostic ablation, not the main matched-information competitor.

The system remains uncertain about each actual loss throughout. Its permitted
conclusion is a conditional bound on changing its effort controller, not a
claim that its predictions are correct or that the new controller is globally
optimal. A raw-update or transient execution claim additionally needs B3's
dynamic contract. This is a candidate task-level discriminator to challenge
against decision-calibration and performative-optimization literature.

## B16. Failed completeness shortcut, and the precise pair-query exception

The initial B14 draft treated adding the calibration rows to an exact conic
response hull as automatically exact. That implication is invalid in general:
convexification need not commute with intersection. Preserve this failed step
as a regression target, rather than trusting a second optimizer on the same
relaxation as an independent semantic reference.

For the *specific* pair-regret query there is a direct exactness argument.
Let s=2*eta, c1=1+lambda,c2=1+2*lambda, d=2*y-x. Maximizing over t yields

    F(x,y)=min(c1*x-c2*y+s, (c1-K)*x-(c2-2*K)*y).

If 2*K<=c2, both terms are nonincreasing in y, so the maximum at each x
uses y=g(x). This covers B15. For 2*K>c2, F increases below the switching
line y=(x+s/K)/2 and decreases above it. On that line,

    F=x/2+s*(1-c2/(2*K)),

which increases with x. On our interval g has 2*g'-1>0, as does its chord.
Therefore the switching line's feasible segment between graph and chord ends
on the graph at its largest x. Its best value is attained on the graph.
Where the chord lies below the switch, F is affine along the chord; its best
value is at an endpoint, either a true graph endpoint or a switching point
dominated by the rightmost graph-switch point. If the switching segment is
empty, the same endpoint/lower-graph alternatives apply. Thus the conic
relaxation is exact for this pair query for K>=0 (K=0 is immediate), despite
not representing the full augmented source hull exactly.

**Explicit failure for another affine observation.** Use u=1/2,v=2/3,
K=1,s=1/4. The response chord is y=x-1/6. At its midpoint,

    (x,y,t)=(7/12,5/12,1/4)

satisfies the conic response hull and all calibration rows. To be in the
convex hull of the true augmented graph, a point on this upper chord must
mix only its two endpoints (strict convexity). At the midpoint their largest
average t is ((1/6)+(1/4))/2=5/24<1/4. Hence the displayed point is spurious.

A concrete separating affine objective is T=2*t-x. The relaxed optimum is
-1/12, obtained by adding twice the chord row, once t<=1/4 and once
t<=2*y-x. On the true graph, T=2*min(1/4,x^2/(2-x))-x. Its increasing
and decreasing branches meet at x=(-1+sqrt(33))/8, giving the sharp maximum

    max T=(5-sqrt(33))/8 < -9/100 < -1/12.

This can be written with a nonnegative budget by adding 1/6 to both candidate
bounds. It is a witness about affine source observations; it is not presented
as a newly justified scientific deployment objective. B15's concrete consumer
has the separate exactness proof above.

**Revision consequence.** A retained exact convex summary can remain sound
but become incomplete after adding relational evidence. Its spurious point
is not a countermodel of the original response law. Removing evidence can
instead make an old restricted summary unsound if its dependencies are ignored.
Ordinary abstract interpretation/convex relaxation has the same distinction;
the proposed project experiment must test it and retain the raw-source reference.

## B17. Saturation makes the loss-query completeness failure concrete

The B16 exactness exception does not cover saturation. Use the same report
law z=1-b*q, gains 1 and 2, tau=0, but b in [0,1/2]. Then

    q_1=z_1=1/(1+b), q_2=1, z_2=1-b.

In coordinates x=z_1 in [2/3,1], y=z_2, the graph is now the *concave*
function g_s(x)=2-1/x. Its convex hull is bounded below by the chord
y=(3/2)*x-1/2 and above by g_s. Take actual loss r_i=z_i-e(q_i),
|e|<=eta=1/12, Lipschitz constant K=1, and effort price lambda=1.
The losses are nonnegative even away from equilibrium: z>=1/2>eta.

The actual robust comparative value for each x is

    G(x)=2*x-g_s(x)-1+min(1/6,1-x).

The calibration switch is x=5/6. On each side, G''=2/x^3>0; therefore
its maximum on each closed side is at an endpoint. The three candidates give

    G(2/3)=0, G(5/6)=1/30, G(1)=0.

The exact worst-case regret is 1/30. In contrast, first convexifying the
response graph and then adding calibration rows lets y take the old chord.
Its objective becomes (x-1)/2+min(1/6,1-x), maximized at x=5/6 with value
1/12. The gap is 1/20. A regret budget of 1/20 is genuinely satisfied, but
this summary cannot certify it.

The relaxed point (x,y,t)=(5/6,3/4,1/6) is spurious. The actual report at
x=5/6 is y=4/5. Yet the marginal response hull and calibration rows separately
accept the spurious point. A native certificate from that relaxation is still
sound; using the point as a semantic refutation would be wrong.

This is a meaningful same-loss/same-price comparison of two effort controllers,
not the arbitrary affine observation used to establish the general failure in
B16. Both feedback executions are benign here: gain 1 is contractive with
factor at most 1/2, and gain 2 immediately returns q=1 on the entire domain.
No unstable-iteration assumption explains the gap.

**Small ordinary repair.** Split the original source at x=5/6 *before*
convexification. On each side the active calibration bound is affine, and
the convex hull of that source subarc preserves the affine objective exactly.
The two branch endpoint calculations recover 1/30. This is cheap ordinary
disjunctive optimization; an implementation must include it. A fixed finite
partition cannot be called universally exact for arbitrary future switch
locations without proof. Retaining the simple latent rational response law
is another inexpensive baseline and permits reconstruction when K or eta changes.

## B18. Operational interpretation and a six-level realization

Self-review requires more than calling an external regression model “self”.
Treat b as an admissible *future task context*, observed by the router when
that task arrives. The request certifies all contexts in the current domain.
The router's versioned evaluator predicts its own conditional expected loss
as z(q)=1-b*q. Its controller sets its own refinement effort from this report.
Ordinary competitors see the same program, current domain and evidence; no
hidden internal coefficient or forbidden source inspection creates the gap.

The true loss response can be realized by a finite synthetic computation
budget table. Let j=0,...,6 count refinement levels, with normalized cost j/6.
For requested effort q, stochastically round 6*q to its adjacent integers.
Then expected normalized effort is exactly q, and expected task loss linearly
interpolates the table entries. Use the residual table

    loss_j(b)=1-b*(j/6)-e_j,
    e_j=-1/12 for j=0,...,5; e_6=+1/12.

Thus e(q) is constant -1/12 through q=5/6 and increases with slope 1 to
+1/12 on the last interval. The amplitude and Lipschitz premises hold exactly,
and all losses are nonnegative for b in [0,1/2]. This table is an operational
toy, not an empirical scientific algorithm or a measured resource advantage.

At b=1/5 the two controllers use q_1=5/6,q_2=1. Their actual expected losses
are 11/12 and 43/60. At price lambda=1, their values are 7/4 and 103/60,
whose difference is exactly 1/30. Consequently B17's sharp bound is realized
by one fixed six-level discrepancy function, not only by an adversary choosing
a different function at each context. The unknown function/source class can
still be used to express the receiver's uncertainty about this computation.

The guarantee concerns *conditional expected* loss and effort, not every
random execution. The controller's own calculation/checking overhead is not
included in q; it must be separately measured in an end-to-end study. Known
overhead differences C_1-C_2 shift both compared bounds by that constant.
They do not remove the representation gap, but can change the decision.
The toy does not establish that its table must be expensive to compute.

**Rejected realization shortcut.** If q merely mixes two fixed endpoint
algorithms on a fixed input distribution, actual expected loss is affine in q.
The calibration function is then affine too. Uniform amplitude eta and slope
K imply a comparative discrepancy at most min(2*eta,K)*abs(q_2-q_1), which
is generally sharper than min(2*eta,K*abs(q_2-q_1)). The saturation example's
kink disappears under that additional structure. Such an endpoint mixture
cannot honestly be used as the realization of B17. Adjacent-budget rounding
allows a nonlinear refinement curve and gives the explicit realization above.

This reconstruction supplies an executable bounded self-assessment target;
it supplies no theorem about empirical calibration, learning, ultimate utility
or the novelty of stochastic rounding. A genuinely scientific application
still needs its own measured or mathematically justified loss/effort curve.

## B19. Exact revision curve and a fixed-partition limitation

Keep B17's response law, gains, context interval, K=1 and price lambda=1.
Vary only the calibration amplitude, writing s=2*eta, with 0<=s<=1 for
nonnegative actual losses on the whole effort/context domain. For 0<=s<=1/3,
the calibration switch is x_0=1-s. The two smooth branches of

    G_s(x)=2*x-(2-1/x)-1+min(s,1-x)

are convex. Hence their combined maximum is attained at 2/3, x_0 or 1.
Those values are s-1/6, s^2/(1-s), and 0. Comparing the first two gives

    s^2/(1-s)-(s-1/6)=(12*s^2-7*s+1)/(6*(1-s))
                         = (4*s-1)*(3*s-1)/(6*(1-s)).

Consequently the exact ordinary reference for all amplitude revisions is

    M(s)=s^2/(1-s),       0<=s<=1/4;
         s-1/6,          1/4<=s<=1/3;
         1/6,            1/3<=s<=1.

For 1/3<=s<=1 the Lipschitz bound alone is active, and maximizing x-2+1/x
gives the last branch. The retained unsplit response hull instead returns

    U(s)=min(s/2,1/6).

At the fixed regret budget 1/20 the exact source certifies precisely s<=1/5,
whereas the unsplit hull certifies only s<=1/10. This follows by clearing the
positive denominator: 20*s^2+s-1=(5*s-1)*(4*s+1). Thus an entire nonempty
interval of evidence strengths changes the decision. The maximum U-M on the
first branch occurs at s=1-sqrt(6)/3 and equals 5/2-sqrt(6); B17's rational
example is close to, but not exactly, that largest gap. This is a closed-form
ordinary repair, not a computational advantage for the project machinery.

**Finite partitions cannot precompile every future amplitude exactly.**
Suppose a summary stores the exact convex hull of the response subarc on each
of m fixed intervals partitioning [2/3,1], and subsequently adds the current
calibration rows in each retained hull. Choose x_0 in (3/4,1) inside one
partition interval [a,b], and set s=1-x_0. The actual query has its strict
global maximum at x_0, by the branch comparison above. The retained hull
permits y equal to the chord c_ab(x_0), which is strictly below g_s(x_0).
Its reported upper bound therefore exceeds the true maximum by at least

    g_s(x_0)-c_ab(x_0)=(x_0-a)*(b-x_0)/(a*b*x_0)>0.

The observation concerns this explicit fixed-partition architecture, even if
each subarc hull uses an exact conic representation. It is not a lower bound
on general programs: retaining the rational source law and evaluating M(s)
already solves the whole family at constant description size.

**Quantitative version.** The intersections of the partition cells with
[3/4,1] have total length 1/4, so one has length h>=1/(4*m). At its midpoint,
the chord error for that subinterval is at least h^2/4, because a*b*x<=1.
The original cell's chord is no higher than the subinterval chord. Thus some
future amplitude causes error at least 1/(64*m^2). For rational partition
endpoints the witness is rational; arbitrary endpoints admit rational nearby
witnesses with any strictly smaller lower bound. This qualification avoids
asserting an exactly rational midpoint of irrational endpoints.

Conversely, |g_s''|=2/x^3<=27/4. With m uniformly spaced intervals over
[2/3,1], the chord error is at most (27/4)*(1/(3*m))^2/8=3/(32*m^2).
Calibration's upper bound does not depend on y here, so the same bound applies
to U_m(s)-M(s), uniformly in s. This is the classical quadratic chord-error
rate applied to a revision family; it is not a new approximation theorem.

One adaptive split at the current x_0 recovers exactness. A meaningful study
must therefore compare fixed retained partitions, adaptive reconstruction,
the closed formula, and the original source on equal terms. Increasing m
alone would manufacture an unnecessary hard baseline.

## B20. Why splitting before convexification suffices

Let S be a compact response set, f a linear loss contrast, and let a_1,...,a_p
be affine upper bounds on a scalar calibration contrast t. Assume the remaining
constraints make t=min_i a_i(s) attainable at each s in S. The exact
robust query is max over S of f(s)+min_i a_i(s).

For each i, define S_i={s in S: a_i(s)<=a_j(s) for all j}. On S_i the query
is the affine function f+a_i. Hence

    max_S (f+min_i a_i) = max_i max_conv(S_i) (f+a_i).

Compactness supplies the maxima; affine objectives preserve their maxima under
convexification. Ties may belong to multiple cells without changing the result.
This proves the ordinary branch repair. In contrast, conv(S) intersected with
the active-bound regions need not equal conv(S_i), as B17 demonstrates.
The attainability premise is essential: separately necessary calibration
inequalities cannot silently be treated as jointly sufficient.

This elementary disjunctive-optimization identity explains both the useful
receipt boundary and the strongest simple competitor. The source adapter must
establish the correct restricted source hull; a downstream affine checker
cannot infer that correctness merely from feasibility of received rows.

## B21. A stronger operational baseline collapses the uniform lower bound

B19 concerns the whole class of bounded Lipschitz response discrepancies.
B18 realizes its particular sharp witness with six refinement levels, but
that does **not** realize every future amplitude revision with the same table
architecture. Treating those two source contracts as interchangeable would
overstate the operational result.

Suppose the receiver also knows the actual mechanism is adjacent-budget
rounding on the fixed grid j/N. Write e_j for its table discrepancies, with
|e_j|<=eta and |e_(j+1)-e_j|<=K/N. Since q_2=1, the comparative error is
e_N minus the interpolation of the e_j at q_1=x. Define h_j=min(s,K*(1-j/N)),
where s=2*eta. Every admissible table satisfies e_N-e_j<=h_j. These bounds
are attained simultaneously by the single table

    e_N=eta, e_j=max(-eta, eta-K*(1-j/N)).

It satisfies all amplitude and adjacent-slope constraints. Therefore the
sharp comparative error for every x is the linear interpolant h_N(x) of the
h_j. It is generally smaller than min(s,K*(1-x)): interpolation of that
concave function lies below it unless the relevant kink is a grid point.

For the same loss and price as B17, G_N(x)=2*x-g_s(x)-1+h_N(x) is convex
on each grid interval, since h_N is affine there. Its maximum occurs at a
grid point in [2/3,1] or at a domain endpoint. This gives an exact O(N)
ordinary reference for every s,K>=0 as an algebraic discrepancy model;
the nonnegative task-loss application retains 0<=s<=1. Fixed cuts at the budget grid suffice
for all those revisions; there is no need to track the moving continuous
calibration kink. This does not contradict B19, whose source class is larger.

For N=6,K=1 the three candidate values yield

    M_6(s)=max(0, min(s,1/3)-1/6, min(s,1/6)-2/15).

In particular M_6(s)=0 through s=2/15, whereas B19's larger class has positive
regret for every s>0. Both attain 1/30 at s=1/6, preserving B17's original
operational witness. At budget 1/20 the finite-table contract certifies
s<=13/60, improving even on the generic Lipschitz cutoff 1/5. The unsplit
response hull with only generic calibration rows still stops at s<=1/10.

**Research consequence.** A serious benchmark must disclose whether fixed
finite budget structure is known. The native and ordinary routes receive it
equally. The strongest ordinary baseline is then this finite node formula,
not a generic nonlinear optimizer or an arbitrarily refined partition.
The surviving issue is which justified source contract is retained and how
its changed premises are checked, not an inherent need for complicated
optimization in this tiny own-effort model. This failed generalization is
useful evidence against inflating the novelty claim.

## B22. Heterogeneous calibration evidence has a shortest-path reference

The finite-table route can support more substantive revision than a single
amplitude scalar, without pretending the resulting optimization is new.
Let the bounded table errors satisfy difference constraints e_v-e_u<=w_uv,
including interval bounds through an anchor e_*=0. Assume the graph is
consistent and every node has finite paths to and from the anchor. Let
d(u,v) be its shortest-path distances. Then the sharp upper bound on every
endpoint contrast is simultaneously

    e_N-e_j <= d(j,N).

Path summation proves necessity. For sufficiency choose the one potential
e_j=d(*,N)-d(j,N). Its anchor is zero, and the triangle inequality
d(u,N)<=w_uv+d(v,N) proves every difference constraint. All endpoint contrasts
attain their distances together. Negative cycles instead make the source
inconsistent; they must not be interpreted as a useful calibrated decision.

For adjacent-budget rounding, the sharp comparative discrepancy at x is thus
the interpolation of the distances d(j,N). Each cell's loss contrast remains
convex, so the robust regret is the maximum at budget nodes and domain
endpoints. This extends B21 to heterogeneous intervals, relational audit
evidence, and justified monotonicity constraints encoded as graph edges.
Evidence coupling errors to b changes this contract and requires new analysis.
The present source is one table valid uniformly across the context interval.

**Four-state revision fixture.** Set N=6, eta=1/8, K=1, with the same permanent
context domain and price as B17. Add optional evidence A: e_6-e_4<=1/5,
and B: e_5-e_4<=1/30. The permanent slope edge gives e_6-e_5<=1/6.
If either A or B remains, the two consequential distances satisfy
d(4,6)<=1/5 and d(5,6)<=1/6, giving robust regret exactly 1/30.
Both bounds are attained by e_6=1/8, e_5=-1/24, e_4=-3/40, and e_j=e_4
for j<4. This witness satisfies both optional bundles and all permanent rows.

If both A and B are withdrawn, d(4,6)=1/4 and the sharp regret is 1/12.
A witness is e_6=1/8, e_5=0, and e_j=-1/8 for j<=4. At x=2/3 its value
is 1/4-1/6=1/12. Thus budget 1/20 passes in the first three presence states
and fails in the fourth. All these sources are feasible; inconsistency does
not explain the decision change.

A single retained proof using A becomes unavailable when A is removed, even
though the B path still proves the query. Retaining both alternatives or
reconstructing a path repairs that miss. Both are standard options for the
ordinary baseline. This is a bounded operational source-revision fixture,
not evidence of new shortest-path, provenance, or caching mechanisms.

An affine native checker can check the summed evidence rows. The rational
response-law and convexity reduction still belong to a separately justified
source adapter; checking a path does not prove that the system's real loss
obeys the table or that the adapter correctly relates b and x. An end-to-end
claim must expose and charge those obligations.

## B23. The finite-context empirical route is affine once its own policy is fixed

For a finite audited context set C and finite computation levels j, let
mu_(c,j) be the unknown conditional expected task loss. A frozen version of
the system's evaluator/controller determines its own probabilities
pi_i(j|c), including any learned report and halting decisions. Once these
probabilities are known, the conditional value of policy i is

    V_i(c)=sum_j pi_i(j|c)*mu_(c,j) + lambda*sum_j pi_i(j|c)*cost_j.

Uniform comparison over c and a supplied polyhedral source for mu is a finite
family of affine support queries. Shared data and relational calibration can
produce joint rows, but the operation is ordinary robust policy evaluation.
This is a useful tractable empirical entry point, not a novel optimizer.

The policy may refer to its own anticipated quality without its true quality
being known. Freezing the report program does not certify its accuracy. If
the program changes, its probabilities and request version change; if the
underlying task distribution changes, old calibration evidence may cease to
apply. Those are distinct changes. A native proof only establishes its
conditional query from the declared current source.

**Boundary of the reduction.** Unknown or continuously varying report
coefficients can make policy probabilities uncertain and multiply them by
unknown losses. Postdeployment changes to outcomes add a causal response
model. A finite-context/frozen-policy experiment must not be described as
solving either richer problem. Conversely, a nonlinear model is unnecessary
if all its policy probabilities can simply be computed from the available
versioned program on the declared finite evaluation domain.

This observation challenges the recurrence's own ambition: endogenous
reporting alone does not force a new logic or a hard nonlinear solver.
The plausible project-level result concerns justified loss/evidence contracts,
revision and independently checked conclusions in a substantive application.
The finite reduction is a mandatory ordinary control for such an application.

## B24. The chosen controllers are weak competitors under unrestricted effort

B17 is a correct comparison of two specified controller versions. It is not
yet a persuasive unrestricted algorithm-selection application. For any effort
q and the same actual response, V(q)=1+(1-b)*q-e(q). Relative to q=0,

    V(q)-V(0) >= (1-b)*q-min(1/6,q).

For q_1=1/(1+b), b in [0,1/2], this is at least 1/3-1/6=1/6>0.
For q_2=1 it is at least 1/2-1/6=1/3>0. Thus zero refinement strictly
dominates both controllers under every admitted discrepancy function.
The operational witness does not by itself justify excluding this baseline.

Even imposing a fixed minimum effort q>=2/3 does not rescue the selection
claim. Constant q=2/3 has robust regret against q=1 equal to

    max_b -(1-b)/3+1/6 = 0,

and never uses more effort than controller 1. Restricting attention to two
preexisting versioned programs may still define a legitimate audit, but a
practical claim must say why broader policy edits are unavailable or costly.
The comparison cannot be advertised as an optimal compute-allocation rule.

This resembles the first N01's quadrature-baseline failure in a new setting:
a nontrivial certificate problem is not sufficient to establish a worthwhile
consumer. Preserve the counterexample as an ambition check, not as a reason
to weaken the ordinary baseline.

## B25. A quality constraint gives a use case, but also a stronger cheap policy

One defensible additional requirement is a uniform conditional expected loss
ceiling T, separate from resource price. Retain eta=1/12,K=1,lambda=1,
but restrict future contexts to b in [1/9,1/2] and set T=59/60. Controller 1
has worst actual loss at most 9/10+1/12=59/60; controller 2 also meets it.
Zero effort does not satisfy the robust requirement, since its worst loss is
13/12. The old response-curve obstruction persists: x is now in [2/3,9/10],
and its calibration kink 5/6 is still interior.

However, if arbitrary context-dependent policies are permitted, the least
effort satisfying the same amplitude-based quality certificate is

    q_Q(b)=(1+eta-T)/b=1/(10*b).

It lies in [1/5,9/10] and is no larger than q_1=1/(1+b), because b>=1/9.
The uniform quality claim follows directly from 1-b*q_Q+eta=T. The constant
discrepancy -eta makes this amplitude-based necessity sharp at every context.

Its robust regret against q=1 is also better. For b<=3/25, the Lipschitz
branch applies and the regret is b-1/10. For b>=3/25, the amplitude branch
gives b+1/(10*b)-14/15. The latter is convex, so evaluating its endpoints
and the first branch's endpoint yields the sharp maximum 1/50, below the
original controller's 1/30. The same bounded Lipschitz source supplies an
attaining discrepancy at the switching context.

The quality constraint therefore gives the effort-allocation question a
plausible interpretation without establishing an advantage for the selected
two-controller architecture. The ordinary quality-constrained policy must be
included if the application permits new routing rules. No quality ceiling or
action restriction may be added merely to hide an unfavorable competitor.
For the known six-level table, interpolation can further sharpen the bound;
the generic Lipschitz result here remains a sound, not necessarily sharp,
certificate for that more structured source.

On the narrowed context domain the unsplit response chord is
y=(5/3)*x-11/18. Its relaxed regret is x/3-7/18+min(1/6,1-x), whose
maximum is 1/18 at x=5/6. The true maximum remains 1/30. Thus the same
budget 1/20 still separates the sound incomplete summary from the true source,
even with the quality requirement. The ordinary q_Q policy nevertheless meets
both requirements with less effort, so this gap does not establish a practical
advantage for retaining either of the original controllers.

## B26. Comparative safety can have disconnected effort choices

For a fixed observed context b and general price lambda, put c=lambda-b.
The worst regret of effort q against the saturated fallback is

    H(q)=-c*(1-q)+min(s,K*(1-q)).

For 0<c<K and 0<s<K, this increases and then decreases as the distance
d=1-q moves from 0 to 1. If 0<=epsilon<(K-c)*s/K, the permitted d satisfy

    d<=epsilon/(K-c), or d>=(s-epsilon)/c,

intersected with [0,1]. A quality condition q>=q_Q adds d<=1-q_Q and can
remove one of those intervals. Every division uses the displayed strict
parameter conditions; K=0, c=0 and other sign cases are treated directly.

Thus a policy very close to the fallback and a much cheaper policy may both
be certified, while intermediate efforts are unavailable at the same budget.
This is ordinary robust comparative optimization with shared bounded error.
It warns against assuming that “more effort” monotonically improves a
resource-priced safety certificate. Native and ordinary optimizers should
receive the same disconnected feasible set, with boundary equality retained.

For B25 with epsilon=0, q_Q is certified once

    b >= (14-sqrt(106))/30,

within the stated context domain; below this point only q=1 is certified.
To obtain the threshold, substitute q_Q into the amplitude branch, clear
10*b>0 and solve b^2-(14/15)*b+1/10<=0. The other root lies outside the
domain. At the threshold equality permits the cheaper policy. A least-effort
certified policy therefore jumps even though all source laws are continuous.
For epsilon=1/20, q_Q is certified throughout, as B25 already proved.

This is an optional policy-design consequence, not a new selection theorem
or an assertion that such a discontinuity occurs in a measured application.

## B27. Calibration regularity also matters for finite execution

The B3 value-transfer bound was derived before introducing discrepancy e(q).
With actual value V(q)=a+(lambda-b)*q-e(q) and a K-Lipschitz discrepancy,
its correct extension is

    |V(q_n)-V(q*)| <= (|lambda-b|+K)*|q_n-q*|.

A uniform b in [0,B] permits replacing |lambda-b| by
max(lambda,abs(lambda-B)). Report-controller contraction is unchanged when
the controller uses z=a-b*q, but the *actual-loss* transfer needs the extra
regularity term. B3's earlier coefficient cannot be reused unchanged.

Amplitude alone does not ensure value convergence. Set a=1,b=1/2,k=1,
use damping 1/2 from q_0=1, and put eta=1/20. Then
q_n=2/3+(1/3)*4^(-n)>q*=2/3 at every finite n. Let e(q)=-eta above q*
and +eta at or below q*. This obeys the amplitude bound, and all actual
losses remain nonnegative. At price lambda=1/2, V(q)=1-e(q), so

    V(q*)=19/20, while V(q_n)=21/20 for every finite n.

An equilibrium budget of 1 passes while every finite iterate fails. This
counterexample is excluded by a known continuous interpolation mechanism;
it is admitted by an amplitude-only function class. The distinction must
survive evidence withdrawal and request binding.

For fixed adjacent-budget interpolation on N levels, amplitude eta already
implies the structural Lipschitz constant 2*eta*N. Withdrawing an audited
tighter constant must retain this derived bound. In B18's particular N=6,
eta=1/12 table, the structural constant is already 1, so a separate K=1
premise is redundant. B15's stricter calibration premise and its continuum
source must not be silently identified with that different finite-table case.

## B28. Admission to the existing core is a separate proof obligation

The recurrence compares source contracts without silently enlarging F05's
finite rational CPWA term language or its finite polyhedral source cases.
The following reconstruction makes the boundary explicit.

For a finite deterministic program pi with fixed rational terminal loss
ell_pi(j) on input j and uncertain input probabilities p_j, its expected
loss is the affine expression sum_j p_j*ell_pi(j). A *fixed* rational private
lottery of programs remains affine. The finite two-bit programs in C16/C22
therefore have exact core terms once their execution-to-loss table is checked.
The probability simplex, optional linear audit rows and a rational feasible
witness provide an ordinary source context. The checker does not establish
that those rows cover a real future input distribution.

For fixed rational alpha<1, C5's finitely many CVaR threshold expressions
are affine in p; their minimum and pairwise difference are CPWA. C21's
fixed-allowance all-risk comparison is a finite conjunction of affine
stop-loss queries. These are query adapters with derived semantics, not a
new `CVaR`, `sup` or hidden-distribution oracle in the term grammar. Changing
alpha, the allowance, a terminal loss, or the program changes the requested
term/adapter contract. It is not merely a unit conversion or a source RHS edit.
Optimizing arbitrary lottery weights jointly with uncertain p introduces
products; the fixed-policy statement does not supply a general optimizer.

The feedback equation with continuously uncertain b instead contains b*q.
Neither the product nor its reciprocal solution is an exact CPWA operation
in those original coordinates. B4 can translate one controller into a
polyhedral chart because it explicitly proves a positive-denominator inverse
and transforms every source row. B7/B13 show why the corresponding joint
two-controller chart can require a curved/conic profile. A sound rational
outer polyhedron is admissible as *supplied evidence*, with possible loss of
completeness; its feasibility does not prove correctness of the adapter.
B17's spurious relaxed point is consequently not a full-source countermodel.

A fixed rational visible context b and fixed controller version in B18–B22's
a=1,tau=0 setting give fixed rational equilibrium efforts and interpolation
weights. Losses are then affine in the unknown table entries, so a bounded
finite context family is a possible exact implementation slice. Merely fixing
b while leaving both interpolation locations and table entries unknown would
not suffice: the interpolation can introduce products. A theorem uniform
over a continuum of b is additional mathematical evidence; finitely many
received instances do not establish it. Known budget-grid structure must
survive the translation, since B21/B27 show that it can invalidate a claimed
hardness or withdrawal example.

This distinguishes three next-step options: use the current finite fragment
with honest adapters; investigate a richer algebraic/conic certificate layer
with its own soundness obligations; or retain an ordinary external solver
and compare its checked consequences. The recurrence establishes no reason
to reopen Gates A/B merely because the second option exists. F11's bounded
scientific control uses the first option and needs none of these extensions.

## B29. A positive control for restriction after an exact convex summary

B16/B17 do not say that every new evidence restriction destroys exactness.
Let S be a nonempty compact source set, K=conv(S), and let
beta=max_(s in S) a.s. Restrict to the exposed face F={x:a.x=beta}.
Then

    K intersect F = conv(S intersect F).

One inclusion is immediate. For the other, express any x in K intersect F
as a finite convex combination sum_i w_i*s_i. Every a.s_i<=beta and their
weighted average equals beta. Each positive-weight term must therefore
have a.s_i=beta. The same combination lies in conv(S intersect F).
This elementary argument also works for a nonempty intersection of exposed
faces. Compactness guarantees attainment; the source's nonemptiness must
still be checked when several restrictions are combined.

By contrast, fix an interior x_0 of B7's strictly convex curve interval.
Restricting the exact response hull to x=x_0 leaves a nontrivial vertical
interval between g(x_0) and the old chord. Restricting the actual graph
first leaves the single point (x_0,g(x_0)). The coordinate restriction is
not an exposed face of that hull. It preserves the minimum-y query at this
x but loses the maximum-y query. Thus the correct conclusion is both
restriction-specific and consumer-specific.

These give paired positive/negative controls for a future source adapter.
They are ordinary convex geometry, not a new preservation theorem. A native
proof from the old hull remains sound under a genuine restriction, but an
unavailable proof or a spurious relaxed witness must not be promoted to a
full-source refutation. F08's full-source/reduct distinction already requires
this separation; the recurrence supplies concrete response-law instances.
