# Gate A — fresh mathematical reconstruction

Input revision: `34beaaf2638f2fb6d113cd1695e0df8dbf4fe26a`.

Reviewer: same assistant, new pass from the declared inputs. This is not an
independent reviewer, mechanized metatheorem, or new research contribution.

## R1. Nonempty finite-linear source inference

Write Gamma={x:Ax<=eta}, and d(x)=c+v^T x. Given lambda>=0,
A^T lambda=v and c+lambda^T eta<=b, multiply the individual inequalities
by their nonnegative weights and add. This proves d<=b without requiring x
or the individual plan losses to be bounded. If Gamma is empty the formal
implication is vacuous: a deployment certificate must separately record a
feasible source case. In the converse cone argument, include (0,1) among
the generators. A separating vector (u,s) must have s>=0. For s>0,
x=-u/s is the counterexample. For s=0, use a feasible x0 and x0-tu;
A u>=0 and v.u<0 imply feasibility and unbounded objective increase.
This checks the signs and the point at which nonemptiness is essential.
This is the classical finite linear consequence result, not a novelty claim.

## R2. Shared versus separately maximized losses

Take d1=theta-3/4 and d2=1/4-theta, 0<=theta<=1.
Each separate supremum is 1/4, at opposite endpoints. Their sum is the
constant -1/2. Accordingly, summing already reduced bounds gives +1/2,
a safe but uninformative upper bound, while retaining theta gives -1/2.
Under attained finite maxima, equality of these bounds occurs exactly when
all component maxima have a common maximizer: the nonnegative individual
slacks at a joint maximizer must sum to zero. This does not hold as an
attained-witness statement for arbitrary nonclosed source families.

## R3. Genuine difference between the shortlisted native fragments

A source-preserving one-step kernel with Pr(Y=1|theta)=theta and
continuation h(theta,1)=theta, h(theta,0)=0 returns theta^2. A finite
continuous piecewise-affine expression cannot equal this on [0,1]:
on every nontrivial affine interval the midpoint is the endpoint average,
whereas the quadratic gives a strict gap. This distinguishes the *restricted
CPWA arithmetic candidate*, not full Rational Lawvere Logic (which has
multiplication), from the finite-kernel transformer candidate.

For a mesh interval [a,b], C(theta)=(a+b)theta-ab obeys
C(theta)-theta^2=(theta-a)(b-theta), so the chord is conservative and its
maximum excess is (b-a)^2/4. On [1/4,3/4], the four-cell uniform chord
C4 yields sup(C4(theta)-theta)=-3/16, attained at the interval endpoints.
The exact quadratic-minus-linear has the same supremum there. Thus the
restricted representation loses exact function recovery but need not lose
this task-specific decision. This is a nontrivial viable alternative rather
than two names for primal/dual arithmetic on a single example.

## R4. Reflective policy, proxy alignment, and explicit source certificate

Let p-s=1/2, 0<=s<=1/4, and e<=1/32. A single report r controls the
probability of executing the second branch. The failure is
H(r)=(1-r)p+r s=p-r/2, so H(r)-r=p-3r/2.
Uniform report validity requires r>=1/2; r0=1/2 and r1=3/4 both qualify.
With branch charge kappa=1/4, the paired proxy cost is
(r1-r0)(s-p+kappa)=-1/16. Adding the same-world discrepancy bound e
makes the intended cost change <=-1/32. A common unknown baseline cancels;
no absolute adequacy conclusion follows from this comparison alone.

In the published five-row ordering, report weights
(1-r,0,1,0,0) give the report-shortfall upper bound 3/4-3r/2.
Paired intended-cost weights (0,1/4,0,0,1) give query vector
(-1/4,1/4,1), RHS -3/32 and, after adding kappa/4=1/16,
final bound -1/32. Feasible example: p=1/2,s=0,e=0.
Every proof uses the same fixed r under every source possibility; the
weights are proof witnesses, not hidden-model-dependent policy choices.
Removing e<=1/32 permits e=1 and reverses the intended guarantee.
Thus this is conditional self-assessment, not a circular assertion of trust.

## R5. Source transport versus invertible numerical recoding

Original bounds x<=1,y<=2 imply x+y<=3,y<=2. The row transform
T=((1,1),(0,1)) is invertible, but its inverse is not order-preserving.
The transformed feasible point (x,y)=(3,0) violates x<=1, even if
nonnegative coordinates are separately required. More generally (M,3-M)
shows the lost x bound is unbounded if coordinates are unrestricted.
For query x+y the aggregated first row remains exact. Therefore preservation
is query-relative; an invertible input representation does not imply
reversibility of logical weakening. F05 must retain the source matrix and
its interpretation, not merely the observed numerical RHS.

For the region-lift sign check, let A=B=1, eta0=0, domain D=-1,d=-1.
The source g<=z and z>=1 justify g<=2z-1. Nonnegative source/domain
multipliers lambda=nu=1 satisfy B^T lambda-D^T nu=2 and
eta0^T lambda+d^T nu=-1. Dropping the domain permits z=g=0 and makes
the proposed -1 bound false. This validates the published minus sign and
shows why a negative observed intercept need not be an invalid proof.

## R6. Exact and approximate self-report stability

From H(r)<=r derive p<=(1+p-s)r. For p=0,s=1 every r is valid and
the least is zero; for p=epsilon>0,s=1 the least is one. Thus no uniform
continuity claim for exact least-report choice is licensed.
With a fixed slack xi>0 the least policy parameter is zero for p<=xi
and (p-xi)/(1+p-s) otherwise. On the active region the two partial
derivatives are nonnegative and sum to 1/(1+p-s)<=1/xi. Continuity
across p=xi and piecewise integration along a segment give the global
infinity-norm Lipschitz bound 1/xi. The controller uses r, not r+xi;
its published bound is min(1,r+xi). Changing which quantity controls
behavior invalidates this derivation. A fixed-report source error delta
adds at most delta to H. Downward report rounding epsilon adds at most
2 epsilon to H-r because its derivative is -(1+p-s) in [-2,0].
These results justify a feasible bounded reflective *example*, not
reflection over arbitrary theorem provability, autonomous discovery of
its own probabilities, or target-calibration of its supplied model.

## R7. Certificate-valued ReLU functions: what is and is not established

For fixed A,v, each lambda>=0 with A^T lambda=v yields the valid form
lambda.eta. A finite minimum of such forms is concave, monotone,
positively homogeneous, and obeys f(eta+Az)=f(eta)+v.z.
Conversely, for a finite CPWA f with all four properties, choose a
full-dimensional affine cell f=lambda.eta+c. Small coordinate changes
force lambda>=0; source shifts force A^T lambda=v; small radial changes
force c=0. Concavity makes that cell's linear form a global upper support;
continuity and coverage give equality with some cell at every point.
Their finite minimum is f. This checks the scope of F04-C31.

These hypotheses describe a certificate *portfolio*, not necessarily the
optimal value: omitting a better valid lambda may leave a loose bound.
Basic one-point validity is weaker. If an exact affine expression at an
input has lambda>=0, A^T lambda=v,c>=0, its value bounds the query even
without a global concavity proof. Failure of a particular gradient test
is inconclusive. At kinks separate derivative conventions need not choose
one coherent active expression; on correlated inputs an observed gradient
may need a domain-dependent lift and can have several valid lifts.

This remains adjacent to familiar polyhedral duality/abstract interpretation,
not evidence of a learned inference mechanism. The named causal experiment
must retain independent task semantics and distinguish validation of an
emitted numerical certificate from a claim about the network's actual
internal organization.

## R8. Evidence priorities and the gate's bounded inference

The certificate-first and source-preserving transformer routes are identical
on the finite affine support question by R1. Calling that duality itself a
choice between two theories would fail the gate. R3 instead distinguishes
native operation closure and approximation obligations. Neither candidate
has yet earned an unconditional efficiency advantage, complete core calculus,
or empirical interpretability claim. These unestablished results are targets
of F05 onward, not missing requirements for *foundation-selection readiness*.

The decisive prospective problem is preservation of a task-relevant paired
loss guarantee through composition and one declared evidence update. The
unknown shared baseline, fixed deployed policy, paired proxy discrepancy,
nonempty evidence, and explicit nonlinear approximation budget are all
necessary test dimensions. No external oracle may provide the final paired
conclusion as an opaque premise. Source validity and criterion choice remain
explicit assumptions with an uncertainty mode and scope, not self-ratifying
outputs. Phase-one licensing can consume such a guarantee in a later compared
fragment; it is not silently reinstated as an immutable core.


## Evidence and source relationship

R1–R8 review existing readiness premises; they do not create a provisional core.
The [independent fixture implementation](../checks/gate_a_review.py) imports no
F04 implementation. Its [17-test report](A_1_numerical_review.json) is evidence
for the explicitly sampled examples, not a general proof. The reviewer is still
the same assistant: neither separate code nor a new pass means independent human
or external-agent review.

Relevant published inputs are the [F04 completion](../derivations/01e_equal_information_completion.md),
[source transport](../derivations/01d_source_transport_and_identifiability.md),
[certificate portfolios](../derivations/01c_certificate_portfolios.md), and
[neural experiment design](../experiments/F04_neural_probe_design.md).
The [gate record](A_1.md) states the checked primary-source interfaces and the
limited readiness decision. The [input manifest](A_1_inputs.json) distinguishes
fresh GitHub hash matches from recovered package copies.
