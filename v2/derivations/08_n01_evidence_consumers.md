# N01 recurrence: optional evidence and consumer extensions

Contributor: **Codex (GPT-6)**. October 3, 2026 UTC.
R-N01-01/C3, closed with its protected floor satisfied. C1–C26 are optional
extensions of [the target notebook](07_n01_recurrence.md), not completed
F11/F13 implementation or a novelty claim. Imported methods are compared in
[the source audit](../literature/04_n01_recurrence_comparison.md).

## C1. A coverage event can support adaptive logical queries

Fix the true parameter theta for a declared program/distribution version.
Suppose audit data produce random source sets P_t satisfying

    Pr(for every t, theta belongs to P_t) >= 1-delta.

A sound receiver at time t accepts only when its certificate establishes
Q_t(theta') for every theta' in P_t. The query and its proof may depend on
all data available at t. On the simultaneous coverage event, every accepted
Q_t is true of theta. Therefore

    Pr(for every t, accepted_t implies Q_t(theta)) >= 1-delta.

This is event inclusion, not a new statistical theorem. No independence of
query and source is needed once the *whole source* has simultaneous coverage.
Repeatedly querying the same covered source does not itself spend delta again.
The logical checker cannot establish the external coverage premise by checking
linear inequalities or a source-version identifier.

For multiple program versions, use a simultaneous guarantee for their entire
family, or conditionally valid per-version audits with a justified error
allocation. Training a version on a dataset and merely attaching a new ID
does not make an audit on those same data valid. Frozen-policy holdout,
uniform function-class guarantees and suitable sequential methods are ordinary
ways to obtain the premise; their actual assumptions and costs must be stated.

Time-uniform inference does not automatically protect against distribution
drift. In R11's general bounded-observation theorem the estimand is the
average of past conditional expectations. A claim about the next deployment
needs a stationarity, transport, or explicitly bounded-drift premise connecting
that estimand to the deployment distribution.

## C2. Adaptive withdrawal does not justify a smaller error charge by itself

If fixed source rows H_j each have failure probability at most delta_j, the
union bound supplies coverage of their joint intersection with error at most
sum_j delta_j. Independence is unnecessary. For a *fixed* subset, summing
only its indices is also valid. Selecting a subset after examining evidence
does not in general permit this smaller post-selection charge.

For a concrete counterexample let theta be in [0,1], draw independent uniform
U_1,...,U_m, and let confidence set C_j be [0,1] when U_j>delta, otherwise
the singleton {1}. Each procedure has coverage at least 1-delta for every
theta. Select the index with smallest U_j, retaining just that one set. At
theta=0 the retained set fails with probability

    1-(1-delta)^m,

which exceeds delta for m>1. The generator is deliberately simple and usually
uninformative; it is a valid counterexample to the generic accounting rule.

Thus deleting premises for logical relevance and deleting their statistical
selection history are different operations. A proof can remain logically
sound from its current rows while an attached confidence claim becomes
invalid. A future empirical receiver should bind the claimed coverage event
or auditing procedure as well as the arithmetic premises. This is an evidence
contract requirement, not a new multiple-testing method.

## C3. Expected-loss guarantees are not per-execution guarantees

Suppose the C1 event implies that the selected policy's conditional expected
deployment loss is at most epsilon, and every execution loss lies in [0,H].
Outside that event its conditional expected loss is at most H. Averaging over
audit data gives

    E[loss] <= (1-delta)*epsilon + delta*H,

provided the accepted query concerns the actual conditional deployment law.
For a positive threshold a, Markov's inequality additionally gives
Pr(loss>a)<=delta+(1-delta)*min(1,epsilon/a). Neither statement says that
every execution incurs loss at most epsilon, or that delta is its tail risk.

Signed regret D=L_A-L_B needs further care. A bound on E[D] does not control
E[max(D,0)] or Pr(D>a) sharply: beneficial outcomes can cancel harmful ones.
For example D is +1 or -1 with equal probability, so E[D]=0 while half the
executions have regret 1. A positive-regret or tail consumer must declare that
different observable and receive enough evidence to evaluate it.

This distinction is relevant to B18's stochastic budget realization. Its
proof concerns conditional expected loss and effort. It does not become a
pathwise performance guarantee merely because the mean inequality has an
exact rational certificate.

## C4. One elementary route from paired experiments to joint source rows

For a fixed context and frozen budget programs, observe independent, identically
distributed audit
vectors X_1,...,X_n, with one coordinate per budget's loss on the same sampled
input. Coordinates within a vector need not be independent. For each of m
predeclared affine contrasts g_l, suppose its range has known width W_l.
The usual bounded-sample inequality and a union bound give simultaneous rows

    |E[g_l(X)] - mean_i g_l(X_i)|
        <= W_l*sqrt(log(2*m/delta)/(2*n)), for all l,

with probability at least 1-delta. This is an ordinary fixed-sample construction.
Data-dependent sample sizes or repeatedly inspected bounds require an
appropriate sequential construction such as R11, or a valid fixed-stage
error allocation. Merely rerunning the same pointwise formula is insufficient.

The contrasts can include paired calibration differences. Known report
differences minus measured loss differences estimate e_j-e_i, yielding graph
rows of the kind in B22. A common-input experiment may have much smaller
contrast variation than separate marginal experiments. That advantage comes
from the experimental design and statistical method; both competitors receive
the same paired data and valid rows.

If all losses lie in [0,H], a generic two-budget contrast has width at most 2H.
Making the simultaneous error radius at most gamma requires

    n >= (2*H^2/gamma^2)*log(2*m/delta).

This radius condition alone does not guarantee certification when the *true*
margin is gamma: the empirical estimate can err toward the threshold. On the
coverage event, radius at most gamma/2 suffices for that guarantee, costing
four times the displayed sample bound. An actual certificate must still
compare its observed contrast plus its radius with the decision threshold.
Small decision margins can therefore make premise acquisition far more costly
than checking the eventual arithmetic proof. A tighter justified paired range
or variance-adaptive method may help. No sample count or empirical calibration
claim is inferred from the synthetic table examples.

A finite set of contexts can be included in the simultaneous family. Uniform
claims over an unseen continuum require additional structure; the observation
of a few contexts cannot certify an arbitrary response function between them.

## C5. Finite tail-loss comparisons fit ordinary affine optimization

Fix rational loss outcomes a_j in [0,H], a rational tail level alpha in (0,1),
and uncertain scenario probabilities p in a bounded rational polytope inside
the probability simplex. The general-distribution CVaR formula in R12 gives

    CVaR_alpha(A;p) = min_t [t + sum_j p_j*max(a_j-t,0)/(1-alpha)].

An optimum t can be chosen among the finitely many loss values a_j: between
successive values the expression is affine in t, and outside the support its
slopes point toward the support. Denote those affine functions of p by A_i(p).
For another fixed-outcome policy B write its corresponding functions B_k(p).
Then the exact robust comparative value is

    max_(p in P) [min_i A_i(p)-min_k B_k(p)]
       = max_k max_(p in P) [min_i A_i(p)-B_k(p)].

For each k the inner maximum is the linear program

    maximize z-B_k(p), subject to p in P, 0<=z<=H, z<=A_i(p) for every i.

For each p its maximizing z is exactly CVaR_alpha(A;p). Thus finitely many
ordinary LPs suffice; introducing the auxiliary variable does not lose the
joint probability constraints. The result is also a finite continuous
piecewise-affine comparison, within the core's stated representation scope.
No general nonlinear optimizer or new risk calculus is needed for this case.

This claim fixes outcome values and the finite scenario interpretation.
Uncertain probabilities multiplied by independently uncertain outcome values
produce additional products and are not covered by the reduction. Adding a
new atom for each product without its joint semantics would repeat the
observable-recoding error already rejected in the core work.

**Atom regression.** If loss is 0 with probability 4/5 and 1 with probability
1/5, then CVaR_(3/4)=4/5. The upper quarter includes all the unit-loss mass
and 1/20 zero-loss mass. Conditioning on loss strictly above its zero quantile
would instead give 1; including the whole quantile atom would give 1/5.
Neither is the stated CVaR. Its mean 1/5 is smaller than a constant loss 3/10,
while its CVaR is larger. Mean-based certification cannot silently serve this
different consumer.

## C6. Paired-regret risk requires a different observation contract

CVaR(A)-CVaR(B) and CVaR(A-B) are not interchangeable. Let both marginal
losses be Bernoulli(1/2). Every joint coupling can be parameterized as

    p_10=p_01=t, p_00=p_11=1/2-t, with 0<=t<=1/2.

Both marginal means and both marginal CVaRs remain unchanged as t varies.
Their difference of means and difference of CVaRs are both zero. The paired
regret has masses t,1-2*t,t at -1,0,+1, respectively. At alpha=1/2,

    CVaR_(1/2)(A-B)=2*t.

More generally for alpha>=1/2 it equals min(1,t/(1-alpha)). At t=0 the
two policies agree on every outcome; at t=1/2 they disagree maximally, despite
identical marginal performance. A bound on disagreement probability
p_10+p_01<=gamma proves the paired-regret CVaR is at most gamma at alpha=1/2.
Withdrawing that row restores a possible value of 1.

This is a small evidence-revision discriminator with an exact one-dimensional
ordinary reference. It supplies additional breadth in the *consumer* dimension,
not new probability theory. A native producer must not infer the paired row
from separate marginal evaluations. Paired executions on a shared input,
an explicit coupling model, or a worst-coupling analysis are different evidence
contracts and must be declared. The means in B18 need no such coupling claim.

If nonnegative primitive losses are required, shift paired regret by 1 before
applying CVaR and shift the query budget by 1. The shift changes neither the
information requirement nor the distinction between these two risk consumers.

## C7. A quantile threshold can be simpler than a quantile-valued observable

For fixed finite loss outcomes and alpha in (0,1), define the lower quantile
VaR_alpha=inf{x:Pr(loss<=x)>=alpha}. For a fixed threshold h,

    VaR_alpha<=h iff sum_(j:a_j<=h) p_j>=alpha.

The threshold query is affine in probabilities even though the numeric
quantile is generally discontinuous. For a Bernoulli loss with probability p
of zero and alpha=1/2, VaR is 0 for p>=1/2 and 1 for p<1/2. No continuous
piecewise-affine primitive equals that function on the whole interval.

This permits a precisely scoped query adapter; it does not prove that the
quantile value has been represented, or that every comparison of quantiles
can use the same adapter. The reverse event VaR>=1 in the example is the
open condition p<1/2, which cannot be the non-strict sublevel set of a
continuous function over this source. Equality conventions matter.

The methodological lesson is the same one that motivated N01: specify the
consumer's observation before judging information sufficiency. Here the
ordinary cumulative-probability identity supplies the reduction. A future
risk application must justify its threshold or tail criterion rather than
count this familiar reduction as novelty.

## C8. Scalar damping does not extend automatically to coupled self-assessment

Consider two effort coordinates q_1,q_2 in [0,1] with reported residual losses

    r_1(q)=max(1-q_1/2-2*q_2,0),
    r_2(q)=max(1-2*q_1-q_2/2,0),
    q_next=r(q).

The reports lie in [0,1]. This is a bounded example of two internal effort
loops responding to their own reported residuals, with declared cross-effects.
It is an execution-semantics stress case, not a recommended compute policy.

There are exactly three fixed points. If both coordinates are positive, the
linear equations are (3/2)*q_1+2*q_2=1 and 2*q_1+(3/2)*q_2=1, giving
(2/7,2/7). If one is zero, the other is 2/3 and the inactive report is zero.
Both zero is impossible. Thus the remaining points are (2/3,0) and (0,2/3).

Nevertheless simultaneous iteration from (0,0) cycles through (1,1) and back.
For task value r_1+r_2+lambda*(q_1+q_2), all fixed-point values are at most
(2/3)*(1+lambda). With lambda=1/4 that bound is 5/6, whereas the cycle's
values are 2 and 1/2, with long-run average 5/4. An equilibrium certificate
therefore fails to describe both the pathwise and average executed value.

For damped iteration q_next=(1-eta)*q+eta*r(q), perturb the interior point
in direction (1,-1). In a sufficiently small neighborhood the report map
multiplies that perturbation by 3/2, so the damped map multiplies it by
1+eta/2>1 for every eta>0. The scalar damping argument in B3 does not extend
to this coupled system. Exact symmetry can hide the instability: at eta=2/7,
the symmetric initial zero state reaches (2/7,2/7) immediately. That does not
establish stability against asymmetric uncertainty or finite-precision error.

Sequential coordinate updates give another behavior. Starting at zero and
updating q_1 first leaves q_2=0 and iterates q_1 <- 1-q_1/2, converging to
2/3; reversing the order selects the other boundary equilibrium. The update
order is therefore part of the program being assessed. A current symmetric
observation is not automatically an invariant of every permitted execution.

All fixed-point cases here are finite affine pieces and can be described by
the provisional core. That expressibility supplies neither a convergence
theorem nor permission to select a favorable equilibrium. The actual request
must distinguish all-equilibrium, designated-equilibrium and executed-policy
claims, with separate justifications for any selection rule.

## C9. A positive coupled class reduces to convex quadratic optimization

Let C=[0,1]^n, let B be a fixed symmetric positive-semidefinite matrix, and
let the report-driven fixed-point equation be q=projection_C(a-B*q).
Projection onto the box is coordinatewise clipping. Its characterization is

    <(I+B)*q-a, x-q> >= 0 for every x in C.

This is exactly the optimality condition for minimizing

    Phi(q)=(1/2)*q^T*(I+B)*q-a^T*q over C.

The Hessian I+B is positive definite, so the minimizer and fixed point are
unique. Compactness gives existence. This is an ordinary strongly convex
quadratic program, not a new reflection principle.

There is a convergent execution with that same fixed point:

    q_next=projection_C(q-eta*((I+B)*q-a)).

This projected-gradient update is a different program from damping outside
the clipping operation. If eigenvalues of I+B lie in [mu,L], projection's
nonexpansiveness gives a Euclidean contraction factor

    max(abs(1-eta*mu),abs(1-eta*L)).

Choosing eta=2/(mu+L) makes it (L-mu)/(L+mu)<1. The proof compares the two
pre-projection points and diagonalizes the symmetric matrix I-eta*(I+B).
The optimum obeys the projected fixed-point equation for every eta>0 by the
same variational inequality, so the comparison is to the desired q*.

For B=[[1,1/2],[1/2,1]] and a=(1,1), the unique point is (2/5,2/5).
Undamped report iteration still cycles between zero and one. Projected
gradient with eta=1/2 has contraction factor 1/4 because mu=3/2,L=5/2.
Thus uniqueness, representability and convergence remain distinct even in
this well-behaved class; an established optimizer provides the positive repair.

For fixed rational B and a varying over a rational polytope, each active-set pattern
gives affine equations and inequalities in (a,q). Principal submatrices of
I+B are positive definite, so the free coordinates have unique affine
solutions within that pattern. The full response is a finite piecewise-affine
map, admitting an ordinary active-set/QP baseline and a finite case encoding.
Continuously uncertain B would multiply unknown q and is a different contract.

These results broaden the bounded self-assessment test design. They do not
establish empirical adequacy of a quadratic model, optimality for an external
task loss, or a generic benefit from a native encoding of an existing QP.

## C10. Revision and finite execution admit cheap ordinary residual checks

For C9, compare old parameters (a,B) and new parameters (a',B'), with
M'=I+B' having smallest eigenvalue at least mu'>0. Let q,q' be the respective
box-constrained optima. Their variational inequalities imply, for d=q'-q,

    <M'*d+(B'-B)*q-(a'-a), d> <= 0.

Therefore

    ||q'-q||_2 <= ||(a'-a)-(B'-B)*q||_2 / mu'.

For d=0 the conclusion is immediate; otherwise divide the strong-monotonicity
bound by ||d||. This is an ordinary sensitivity certificate using the old
solution and new model discrepancy. Keeping a warm start or reconstructing
the new QP must be allowed to the ordinary comparator.

If the selected execution map T is a contraction with factor c<1, an arbitrary
state q also satisfies the a posteriori bound

    ||q-q*|| <= ||q-T(q)||/(1-c),

by adding and subtracting T(q) and using T(q*)=q*. Computing a small update
residual can thus certify proximity without completing another solve. This
requires the *new* contraction and source contract after a revision.

The actual executed task value still needs its own transfer bound. For
v(q)=w^T*r(q)+lambda*d^T*q, where r(q)=projection_C(a-B*q), one sufficient
Euclidean Lipschitz constant is ||w||_2*||B||_2+lambda*||d||_2. It converts
a state-error bound to a value-error bound. The simpler equilibrium identity
v(q*)=(w+lambda*d)^T*q* cannot be used at a non-equilibrium state.

In C9's two-dimensional example with lambda=1/4,w=d=(1,1), start projected
gradient at zero with eta=1/2. Symmetry gives q_k=(t_k,t_k), where

    t_k=(2/5)*(1-(-1/4)^k),
    v(q*)=1, v(q_k)-1=(-1/4)^k.

All iterates stay in the active linear report region. The exact error is
4^(-k). A triangle-inequality Lipschitz estimate instead gives (7/5)*4^(-k),
which is safe but can require an extra iteration at a tight stopping budget.
An ordinary direct calculation retaining the shared report/effort dependence
recovers the exact bound. This is a meaningful finite-execution discriminator,
but not evidence that the native route alone can exploit the dependence.

These sensitivity, residual and contraction checks are promising reusable
components for a bounded reflective case study. Their connection to a measured
external task loss and their total construction/checking cost remain open.

## C11. Symmetry is sufficient, but not necessary for a positive feedback class

Let M=I+B be fixed, possibly nonsymmetric. Suppose its symmetric part is at
least mu*I with mu>0, and ||M||_2<=L. For F(q)=M*q-a, projected iteration
T_eta(q)=projection_C(q-eta*F(q)) satisfies

    ||T_eta(q)-T_eta(p)||^2
       <= (1-2*eta*mu+eta^2*L^2)*||q-p||^2.

Expand the pre-projection squared distance, use strong monotonicity for the
cross term and Lipschitz continuity for the last term. Any
0<eta<2*mu/L^2 gives a contraction. Banach's theorem on the closed box gives
one fixed point; the projection variational inequality makes it the solution
of q=projection_C(a-B*q). This is an ordinary strongly monotone variational
inequality, generally not the minimizer of a scalar quadratic potential.

For example, B=[[0,-1],[1,0]], a=(0,1) gives the raw report map
(q_1,q_2)->(q_2,1-q_1). It has the unique fixed point (1/2,1/2), but raw
updates cycle around the four corners. Here mu=1,L=sqrt(2), and eta=1/2
gives contraction factor 1/sqrt(2). No clipping is active in the averaged
update, so this factor is attained by every difference vector.

For fixed rational M, active-set response pieces remain affine: every free
principal submatrix is invertible, because its symmetric part retains the
same positive lower bound. This supplies a broader positive control than C9,
while the three-equilibrium C8 example fails the strong-monotonicity premise.
The interpretation, execution and empirical calibration obligations remain.

## C12. A finite execution certificate need not assert convergence

Let S be a finite, closed set of reachable execution states, with allowed
edges s->s' and rational per-step loss g(s,s'). Fix a proposed long-run bound
beta. A potential h:S->Q satisfying

    g(s,s')-beta <= h(s)-h(s')

on every edge gives, for every length-T execution,

    sum_{t<T} g(s_t,s_{t+1}) <= T*beta+h(s_0)-h(s_T).

This follows by telescoping, with no convergence premise. Such a potential
exists exactly when every directed cycle has mean loss at most beta. Necessity
follows by summing around a cycle. For sufficiency, assign edge weight g-beta
and define h(s) as the largest weight of a finite path starting at s, including
the empty path. A repeated-vertex cycle has nonpositive weight and can be
removed without decreasing the path weight. Hence a simple path attains a
finite maximum. Concatenating an edge and a maximizing suffix proves the
required inequality. All quantities are rational for rational input.

For C8's reachable synchronous two-cycle, take states 0=(0,0) and 1=(1,1),
outgoing losses 2 and 1/2, beta=5/4, and h(0)=3/4,h(1)=0. Both inequalities
are equalities. Thus its average execution loss is 5/4, even though all three
fixed points have value at most 5/6. A fixed-point certificate cannot replace
this execution certificate. A finite-horizon dynamic program can give sharper
prefix bounds and must be admitted as an ordinary comparator.

This is the familiar potential/difference-constraint and maximum-cycle-mean
method, not a new graph theorem. A finite sample of a continuous trajectory
does not establish a closed execution graph. A finite-state program, exact
reachable-state argument, or sound abstraction is needed before applying it.

## C13. Static model uncertainty cannot be resampled at every transition

Consider states A,B and one parameter theta in {0,1}, fixed throughout a run:

| Fixed model | From A | From B |
|---|---|---|
| theta=0 | Go to B, loss 1 | Stay at B, loss 0 |
| theta=1 | Stay at A, loss 0 | Go to A, loss 1 |

Every actual run incurs total loss at most one and asymptotic average zero.
If an abstraction forgets theta and independently admits the union of outgoing
edges at each step, it admits A->B->A->B forever, with loss one on every step.
There is then no common beta=0 potential: the two changing-state edges require
h(A)>=1+h(B) and h(B)>=1+h(A) simultaneously.

Keeping theta as a latent, unchanging state component repairs the issue.
Use h_0(A)=1,h_0(B)=0 and h_1(A)=0,h_1(B)=1 on the lifted states (s,theta).
C12 certifies total loss at most one in both cases. The receiver need not know
which theta is actual to check both conditional cases. An ordinary product-
state construction or case split obtains exactly the same result.

This is a temporal instance of losing joint dependence. It can matter for a
reflective program whose assessment model remains fixed between revisions,
but it is not by itself a new principle of reflection. The all-edge abstraction
would instead be appropriate if the environment really could change theta
arbitrarily every step. The source contract must distinguish these cases.

## C14. Actual switching has a separate, chargeable transient cost

Suppose the actual version v_t used for step t has a potential h_{v_t} and
bound beta_{v_t}. Summing its edge inequality gives

    sum_{t<T} g_t <= sum_{t<T} beta_{v_t}
       + h_{v_0}(s_0)-h_{v_{T-1}}(s_T)
       + sum_{t=1}^{T-1} [h_{v_t}(s_t)-h_{v_{t-1}}(s_t)].

Unchanged versions contribute zero in the final sum. The positive potential
jumps therefore provide an explicit switching allowance; any physical cost
of installing or auditing a new version is additional. In C13, each actual
theta switch can introduce at most one additional unit of loss, so total
loss is bounded by one plus the number of switches. Alternating the target
after each successful move attains that rate.

Potential offsets are arbitrary. Adding a constant to each h_v changes the
individual jump terms, but the *complete displayed expression* is invariant:
the offset jumps telescope against the endpoint offsets. For the coarse
"one plus switches" bound, normalize both potentials to minimum zero. An
unqualified sum of positive jumps without endpoint normalization is not an
intrinsic cost measure.

Withdrawing an evidence row about a single fixed theta is not a physical
theta switch. It changes the admitted cases, and previously excluded cases
may need validation, but it does not justify charging a fictitious physical
switch at each logical update. Conversely, installing a different controller
really may change execution dynamics. Proof-maintenance cost, source audit
cost, and executed-task switching cost belong in separate reported accounts.

## C15. Expected drift and sample-path guarantees are different consumers

For a stochastic transition, suppose the current history F_t determines s_t
and a fixed potential h, and the true conditional law satisfies

    E[g_t+h(s_{t+1}) | F_t] <= beta+h(s_t).

Taking expectations and telescoping gives the expected version of C12. For
a fixed deterministic horizon T, if 0<=g_t<=G and the potential has span H,
the centered variables

    Z_t = g_t+h(s_{t+1})-E[g_t+h(s_{t+1}) | F_t]

are martingale differences with conditional range width at most G+H. The
conditional Hoeffding bound and exponential Markov inequality give, with
probability at least 1-delta,

    sum_{t<T} g_t <= T*beta+h(s_0)-h(s_T)
                    +(G+H)*sqrt(T*log(1/delta)/2).

The range is G+H, not G+2H: h(s_t) is known before the transition and does
not add a random range term. Replacing -h(s_T) by -min_s h(s) gives a fully
precomputable upper bound. A bounded stopping time is not automatically
covered by this fixed-T statement. One elementary simultaneous alternative
allocates delta_T=6*delta/(pi^2*T^2) and takes a union bound over T>=1;
sharper time-uniform methods are an ordinary baseline (R11).

A statistical source-coverage event does not license conditioning the entire
martingale proof on that event: it may depend on future outcomes. One valid
composition, when the true parameter is fixed and P_t is F_t-measurable, is
to stop the proof process immediately before the first t with theta not in
P_t. Up to that stopping time the certified drift premise holds under the
true conditional law. Apply the bounded-increment argument to this stopped
process, then intersect with the simultaneous source-coverage event. The
total failure probability is at most delta_source+delta_execution. On the
coverage event the process was never stopped. This requires predictable
source sets and valid conditional transition semantics, not just a version ID.

These are standard supermartingale tools. A useful implementation would have
to check the drift inequalities, preserve the transition-law assumptions and
account for the source's empirical coverage; a local arithmetic certificate
cannot establish those external assumptions.

## C16. A finite computation-selection program with an actual task loss

The fixed-point examples above are primarily semantic stress tests. Here is a
separate finite program family with explicit inputs, computations and output
loss. An input consists of two inaccessible bits X,Y. The required answer is
their parity Z=X xor Y. Reading either bit costs c=3/20 in task-loss units;
each bit may be read at most once. After zero, one or two reads the program
outputs a bit. Loss is the zero-one error of that answer plus the read costs.
Reading a bit reveals its actual value; it is not a free sample of a different
input. The distribution p=(p00,p01,p10,p11) is external evidence.

After reading both bits, answering parity exactly weakly dominates an error.
The remaining deterministic policies number twenty: two immediate answers,
nine policies that read X first, and nine that read Y first. Each observed
first-bit branch can answer 0, answer 1, or read the other bit and answer
exactly. Each policy therefore has an explicit four-coordinate loss vector
l_pi, and expected loss l_pi dot p. Duplicate loss vectors may be merged,
but their execution descriptions and receipt costs need not be identical.

For a known p, direct backward induction gives the least expected loss

    min(p01+p10, p00+p11,
        c + sum_x min(p_x0, p_x1, c*(p_x0+p_x1)),
        c + sum_y min(p_0y, p_1y, c*(p_0y+p_1y))).

This uses unnormalized branch masses and remains well-defined for a zero-
probability branch. It is an ordinary metalevel dynamic program (R18).
For an uncertain convex polytope P of priors, a *fixed* deterministic policy
has robust value max_{p in P} l_pi dot p, an ordinary support LP. Choosing a
different optimal policy separately at every unknown p swaps the quantifiers
and is not generally implementable. If private randomization over the twenty
policies is allowed, its weights form another finite simplex; the resulting
minimax expected-loss problem is a finite zero-sum LP. Both ordinary methods
must be permitted to a comparator, with their actual construction cost.

At p=(9/20,1/20,1/4,1/4), policy A reads X, answers 0 if X=0, and otherwise
reads Y and answers parity. Its loss distribution is

| Executed loss | Probability |
|---|---|
| 3/20 | 9/20 |
| 3/10 | 1/2 |
| 23/20 | 1/20 |

Its mean is 11/40. Immediate answer 0 and full evaluation both have mean
3/10. No policy using exactly one read on every input improves on them.
The adaptive stopping policy does improve: it uses 3/2 reads in expectation
and makes an error with probability 1/20. This avoids B24's zero-effort
dominance and has a directly executed meaning. It is still a small synthetic
task, not a demonstrated scientific workload or a novelty claim.

## C17. Source withdrawal and risk preference select different programs

Give C16 the following *joint* source family:

    p00=1/2-e, p01=e, p10=u, p11=1/2-u,
    0<=e<=1/20, 1/5<=u<=3/10.

The bit-reading semantics and row masses are permanent structural premises.
The upper bound on e is a separately identified calibration premise. All
these sources are nonempty. Policy A's distribution depends on e but not u;
increasing e transfers probability from loss 3/20 to loss 23/20. Therefore its
worst mean and every upper-tail CVaR occur at e=1/20. Full evaluation F has
constant loss 3/10 on every input.

At the admitted witness p*=(9/20,1/20,1/4,1/4), the best policies in each
category, other than A, have the following expected-loss lower bounds:

| Policy category | Least mean at p* |
|---|---|
| Immediate answer | 3/10 |
| X first, stop in both branches | 9/20 |
| X first, read again only when X=0 | 19/40 |
| X first, read again only when X=1, wrong first-branch answer | 27/40 |
| Read both in every branch | 3/10 |
| Y first, stop in both branches | 9/20 |
| Y first, read again only when Y=0 | 61/200 |
| Y first, read again only when Y=1 | 89/200 |

The exact planning probe will enumerate all twenty policies; the inequality
needed here is that every competitor except A has mean at least 3/10.

CVaR_alpha(A), for 0<=alpha<=9/20, is

    (11/40-(3/20)*alpha)/(1-alpha).

It is below 3/10 exactly when alpha<1/6, equal at 1/6, and above afterwards.
CVaR is nondecreasing in alpha and at least the mean. Thus the table proves
that A is optimal among all twenty policies at p* for alpha<=1/6, and F is
optimal there for alpha>=1/6. Since A's robust risk is attained at p* and F
has constant loss, these are also robust optima over the whole source family.

Private randomization does not defeat this witness argument. For a *fixed*
input law p*, CVaR as a function of a lottery's outcome distribution is the
minimum of affine threshold expressions, hence concave in mixture weights.
A mixture's CVaR is at least the mixture of the component CVaRs, and therefore
at least their minimum. This is a statement about independently drawing a
policy lottery, not about pointwise averaging two output losses. Those are
different operations. It does not assert that randomization never helps a
general robust-risk problem over multiple possible p.

Withdraw the e<=1/20 premise, retaining 0<=e<=1/2 and the u range. The uniform
four-world law e=u=1/4 becomes admissible. At that law, backward induction
gives least expected loss 3/10, attained by F, since an unread parity bit
leaves error probability 1/2 and another read costs only 3/20. Hence F is a
robust optimum for every alpha, while A's robust mean rises to 29/40. This
is an actual task-level decision change under evidence withdrawal.

All claims here are exactly soluble by the ordinary twenty-policy reference.
At each fixed rational alpha, C5 translates the relevant finite-outcome CVaR
queries into finite LPs or CPWA expressions. No nonlinear source atom, free
calibration oracle, or native expressive advantage is assumed. The example
is a candidate bounded self-assessment *control* for F13, subject to its own
fresh protected derivation and implementation, not an extra F11 requirement.

## C18. A changed consumer may need more information, unless structure supplies it

For C16's fixed policy A at price c in (0,1), let m=Pr(X=1) and
e=Pr(X=0,Y=1). Its three loss atoms have probabilities

    loss c: 1-m-e; loss 2*c: m; loss 1+c: e,
    expected loss = c+c*m+e.

Thus its whole risk curve depends on two probability coordinates, whereas
its mean depends on one affine combination. At c=3/20, the C17 witness has
(m,e)=(1/2,1/20) and mean 11/40. A second distribution with
(m,e)=(5/6,0), for example p=(1/6,0,5/12,5/12), has the same mean.
At alpha=1/5 the first CVaR is 49/160>3/10, while the second is 3/10.
A mean-only receipt cannot decide this new tail query over the unrestricted
prior simplex. At alpha=9/10 the values are 29/40 and 3/10 respectively.

But C17 permanently knows m=1/2. There, the mean identifies e exactly, and
therefore identifies the entire risk curve. The mean-only obstruction above
does **not** apply when that structural premise is retained. Its removal is
a separate source-contract revision, not the removal of C17's calibration
upper bound. A truthful experiment must report all information available to
its reconstruction baseline, including such permanent equalities.

For the full twenty-policy mean-query family, retaining all four probabilities
is sufficient, and only three are independent. Policy A and its branch/answer
variants give several independent affine directions. Any stronger minimality
claim must specify whether it preserves every bound, threshold answers, only
the selected policy, or a risk curve. Different observations define different
summary requirements; neither the number of raw atoms nor an example of a
failed scalar summary establishes an unrestricted storage lower bound.

## C19. A finite grid of risk levels is not a universal exact risk summary

Consider the unrestricted three-atom distribution for A from C18, with fixed
rational c in (0,1). Fix any
finite list of retained levels alpha in [0,1), possibly including zero.
Choose rational delta>0 smaller than every positive retained level and
smaller than one. If there are no positive levels, any small delta suffices.
Let P put mass (1-c)*delta at loss c and the remaining mass at loss 1+c.
Let Q put mass delta at loss 2*c and the remaining mass at loss 1+c.
Both are realizable by two-bit input distributions and have mean

    1+c-(1-c)*delta.

At every retained positive level their CVaR equals 1+c: enough probability
already sits at the largest atom to fill the requested tail. Their alpha=0
values also agree. Nevertheless choose a rational new level
(1-c)*delta < alpha_new < delta. Then CVaR_P=1+c, while

    CVaR_Q = 1+c-(1-c)*(delta-alpha_new)/(1-alpha_new) < 1+c.

A rational threshold between these values distinguishes the new query.
Therefore no fixed finite grid of exact CVaR values is universally sufficient
for all later rational levels on this source class. This lower bound is on
that *particular summary format*. Two probability coordinates, or the actual
three-atom distribution, already suffice at constant size. It does not apply
to C17 with its known branch mass, where even the mean can suffice.

There is also a simple controlled approximation. For losses in [L,H] and
0<=a<b<1, tail-quantile integration gives

    0 <= CVaR_b-CVaR_a <= (H-L)*(b-a)/(1-a).

Indeed the alpha=a tail is the weighted average of the removed quantiles
over [a,b] and the alpha=b tail. Their difference is at most H-L. This
bound extends across atoms because it uses the quantile integral, with the
usual partial mass at an atom. An upper risk bound at the next retained level
therefore incurs at most this error; a decision with adequate margin can
still be certified. For levels up to a fixed alpha_max<1, a uniform grid of
spacing h gives error at most (H-L)*h/(1-alpha_max). This is a conservative
ordinary interpolation control, not a new risk approximation rate.

This supplies both an exact failure mode and a margin-aware baseline for a
future consumer-revision experiment. The existing F11 slice remains finite;
no all-risk-level completeness claim is added to its acceptance criteria.

## C20. Policy pruning must preserve the consumer and its quantifiers

The value-vector pruning in R21 preserves a pointwise optimal expected value.
It does not automatically preserve deterministic robust policy selection.
For two hidden states, consider losses

    A=(0,2), B=(2,0), C=(11/10,11/10).

For every prior p on these states, min(E_p A,E_p B)<=1<11/10.
Thus C is unnecessary for the pointwise lower envelope. But if one must
choose a deterministic policy before an adversary chooses p, A and B both
have worst loss 2, while C has worst loss 11/10. Deleting C changes that
decision. The distinction is min_policy max_p versus max_p min_policy,
not a failure of the published pruning algorithm under its own contract.

If private policy randomization is allowed and the objective is mean loss,
the half-A/half-B lottery has expected loss 1 at every p. More generally,
for a convex compact source P and finitely many loss vectors v_i, pointwise
domination of v_C by their lower envelope means

    max_(p in P) min_i p.(v_i-v_C) <= 0.

Finite-dimensional minimax/LP duality then supplies a *single* mixture sigma
with max_p sum_i sigma_i*p.(v_i-v_C)<=0. That mixture uniformly dominates C
in mean. The mixture and its randomization semantics are part of the repair;
there need not be a single deterministic replacement.

Changing to CVaR defeats a second shortcut. At the equal prior and any
alpha>=1/2, both A and B have CVaR 2, whereas C has CVaR 11/10. A private
lottery over A and B still has the same 0/2 distribution at that prior, so
it does not improve the tail. Pointwise averaging their numerical losses
would give constant 1, but describes a different executable action.

The actual two-bit task already exhibits a cleaner source-specific example:
on C17's source, A has mean at most 11/40 and the full-read policy F costs
3/10. F can therefore be deleted for the current mean objective. After the
risk level exceeds 1/6, F is optimal and A is not. A receipt for expected
dominance cannot be relabeled as risk dominance. Retaining all structurally
possible policies, or rebuilding correctly after the objective changes, is
an ordinary control; charge its cost rather than silently forbidding it.

## C21. All risk-level comparisons have a stronger finite ordinary receipt

C19 rules out one summary format, not finite exact comparison methods.
Let U,V have known fixed finite loss supports and probabilities affine in a
common uncertain parameter p in a polytope P. For a fixed rational allowance
epsilon, put W=V+epsilon and define the stop-loss transform

    S_U(t)=E[(U-t)_+], S_W(t)=E[(W-t)_+].

For each fixed p, the following statements are equivalent:

    CVaR_alpha(U) <= CVaR_alpha(V)+epsilon for every 0<=alpha<1;
    S_U(t) <= S_W(t) for every real t.

Here is a finite-distribution derivation. Write u=1-alpha and let H_U(u)
be the largest total loss in a subdistribution of mass u, allowing partial
mass at an atom. Then H_U(u)=u*CVaR_(1-u)(U) for u>0 and H_U(0)=0.
Selecting precisely the positive terms proves

    S_U(t)=max_(0<=u<=1) [H_U(u)-u*t].

Hence all-CVaR ordering implies all-stop-loss ordering. In the other
direction use CVaR_alpha(U)=min_t[t+S_U(t)/(1-alpha)] and the same formula
for W; pointwise ordered objectives have ordered minima. Translation by
epsilon gives the displayed comparison with V.

The difference S_U-S_W is continuous piecewise affine in t, with breakpoints
only at the union of the two fixed supports. Left of the smallest atom it
is the constant E[U]-E[W]; right of the largest it is zero. Checking every
support breakpoint therefore suffices. At each fixed breakpoint, the
inequality is affine in p. Thus the *uniform* claim over every p in P and
every alpha needs only finitely many ordinary support LPs, each with an
ordinary dual receipt. The universal quantifiers commute; no optimization
over an unknown risk level or nonlinear source atom is necessary.

This does not reconstruct the entire numerical risk curve, does not make a
fixed grid of CVaR values sufficient, and does not preserve every possible
epsilon without new work. Supports and epsilon are fixed receiving inputs.
If a program revision changes an atom, the old knot/row catalogue must be
rechecked. For C16 at epsilon=0 the common support is contained in
{0,c,2*c,1,1+c}; the all-level comparison has a small exact ordinary control.
In C17, A and F are not ordered for all risk levels: A wins in mean and F
wins in the tail. A declared risk preference remains consequential.

This is a direct application of the classical stop-loss/increasing-convex
ordering idea, not a proposed new mechanism; R24–R25 audit the close sources.

**Stronger reference-knot control.** R24's Proposition 3.2 improves the
union-of-supports construction: only W's support knots are needed. Between
successive such knots S_W is affine and S_U is convex, so endpoint ordering
implies ordering throughout. Above max W, the knot inequality forces
S_U(max W)=0, hence U<=max W almost surely and both transforms vanish.
Below min W, S_U(t)+t=E[max(U,t)] is nondecreasing in t, while S_W(t)+t=E[W].
The inequality at min W therefore implies every lower-threshold inequality.
This proof even permits integrable U without finite support; our finite U
restriction supplies the explicit affine probability rows for the core.

For C17's constant fallback F=3/10 and allowance zero, only t=3/10 is
needed. Its stop-loss contrast is (17/20)*e. Therefore A has no greater CVaR
than F at *every* level precisely when e=0. Any positive chance of the
1+c loss defeats that universal contract as alpha approaches one, despite
A's lower mean. A finite preferred risk range and all-risk-level dominance
are different ambitions and should not be substituted for one another.

## C22. Even the old program's entire loss law can omit revision information

Return to the actual two-bit program, with c=3/20 and policy A from C16.
Fix m=1/2 and e=1/20, and vary the remaining input distinction u:

    p=(9/20, 1/20, u, 1/2-u), 0<=u<=1/2.

For every such input law A has exactly the same loss distribution: masses
9/20, 1/2, 1/20 at c,2*c,1+c. Consequently every statistic determined by
that distribution, including its full CVaR curve, is unchanged. Yet the
zero-computation program S that immediately answers parity zero has mean
loss 1/20+u. Its mean contrast to A is

    E[S]-E[A] = u-9/40.

At u=1/5 the replacement improves mean loss by 1/40; at u=3/10 it worsens
mean loss by 3/40. The old program's full loss law therefore cannot decide
this revision. The omitted direction is (0,0,1,-1) in the input simplex:
A groups the two X=1 inputs together because it always reads the second bit
and answers exactly; S's errors distinguish them.

For a concrete withdrawal test, permanently allow 0<=u<=3/10 and initially
add u<=1/5. A current receipt proves E[S]-E[A]<=-1/40. Removing the extra
row admits a real counterexample with contrast 3/40, while A's entire loss
law remains fixed. An old-loss-only cache cannot decide the current request.
An ordinary source-aware affine query does so immediately. Both methods must
receive the same current source and pay to bind the row/version they use.

This is a *retention* limitation, not an impossibility of observing u. A's
execution actually reads Y whenever X=1; retaining its input/branch counts
would preserve the missing distinction. Such logs or sufficient counts are
allowed to the ordinary comparator. Their acquisition is already partly
paid by execution, while their storage and receipt checking are additional.
An experiment that gives native code those counts but an ordinary method
only the old mean or loss histogram would not establish the project claim.

There is a small exact full-mean reference. Let A' reverse A's answer on
the X=0 branch, retaining the full read when X=1. At c=3/20, the three means
mu_A, mu_A', mu_S determine all four input probabilities:

    r = (mu_A+mu_A'-4*c)/(1-2*c) = p00+p01,
    d = mu_A-mu_A' = p01-p00,
    p00=(r-d)/2, p01=(r+d)/2,
    p10=mu_S-p01, p11=1-p00-p01-p10.

Thus three independent probability coordinates suffice for every mean query
over all twenty policies. Conversely, on the full simplex these three affine
mean observations are independent on its direction space. A linear summary
preserving all of them (or their answers at every rational threshold) must
have rank at least three there. This relative-rank statement does not apply
to a smaller permanent source, a fixed threshold family, or arbitrary encodings.
It is an explicit application of A2's ordinary sufficiency argument.

The useful distinction is now concrete: an old policy's complete performance
description can be insufficient for a program edit, while a tiny structural
input summary suffices. C22 is a candidate consumer-revision control for F13,
not a native advantage, an empirical finding, or an additional F11 obligation.

## C23. Robust randomization can help despite concavity in the lottery law

C17's no-randomization-improvement proof used a particular worst-case prior.
It cannot be generalized merely from CVaR's concavity in a mixed law. For
C20's A=(0,2), B=(2,0), allow every prior on the two hidden states. Every
pure policy has worst CVaR 2. A fair private lottery between A and B has
loss 0 or 2 with equal probability at every prior, so its worst CVaR is

    min(2, 1/(1-alpha)).

For alpha<1/2 this strictly improves on both pure policies. The equal prior
makes the same 0/2 law for *every* private mixture of A and B, proving the
displayed value is the robust optimum over their mixtures. This is a direct
quantifier effect: max over p of concave functions of the lottery weights
need not itself be concave.

If C=(11/10,11/10) is also available, the exact robust mixed-policy optimum is

    min(11/10, 1/(1-alpha)).

To prove the lower bound, let the weight of C be w. At the equal prior the
loss law is w mass at 11/10 and (1-w)/2 at each of 0 and 2. CVaR is concave
in this mixture law, so its value is at least the smaller endpoint value
11/10 or min(2,1/(1-alpha)). The better endpoint is attained uniformly over
priors by C or by the fair A/B lottery, respectively. The optimal choice
switches at alpha=1/11. This also explains why mean-envelope pruning that
removes C is invalid for the larger risk family.

No actual averaging of outputs or losses was permitted. A receiver and its
ordinary control must agree on whether a policy lottery, an averaged output,
or a deterministic choice is executable. These simple finite examples are
semantic regression controls, not a new minimax or risk theorem.

## C24. An all-risk predicate need not represent an all-risk numeric value

Let U be Bernoulli(p) loss, V the constant 3/10, and allow 0<=p<=1.
For p>0, choosing alpha>=1-p gives CVaR_alpha(U)=1; at p=0 every tail
average is zero. Therefore

    sup_(0<=alpha<1) [CVaR_alpha(U)-CVaR_alpha(V)]
        = 7/10 if p>0, and -3/10 if p=0.

This numeric observable is discontinuous and cannot equal one finite
continuous piecewise-affine expression on the whole source interval. But
at any fixed allowance 0<=epsilon<7/10, its universal threshold claim is
simply p=0, equivalently p<=0 under the permanent probability bounds.
For epsilon>=7/10 it is always true. C21's single reference-knot test gives
the same predicate: E[(U-(3/10+epsilon))_+]<=0.

Thus a finite affine receipt for every fixed member of a query family does
not imply a single native numeric expression for the family's supremum.
Conversely, the numeric obstruction does not prevent the useful threshold
query. Any future all-risk experiment must state which of these observations
it asks the system to preserve. This is another application of the existing
query-versus-observable distinction, with no claim of a new representation
principle or a requirement to extend F11's declared language.

## C25. Why the independent all-level finite-distribution probe is exact

The risk-revision probe does not sample a uniform grid of risk levels. For
each *fixed* pair of finite distributions it collects both cumulative-mass
breakpoint sets, includes alpha=0, and separately evaluates the limit at one.
Between consecutive breakpoints, upper-tail integration has the form

    CVaR_alpha(U)=(a_U-b_U*alpha)/(1-alpha),

with fixed constants on that interval; the same holds for V. Their difference
therefore has derivative of constant sign (or zero), since its derivative
is a constant divided by (1-alpha)^2. Its extremum on that cell occurs at an
endpoint. CVaR is continuous at the interior breakpoints, including split
atoms. Above the last positive-mass breakpoint, each risk is its largest
positive-probability loss. The limit is their difference.

Thus the probe's knot-and-limit maximum covers every alpha for that fixed
distribution pair. Zero-probability atoms are omitted when computing support
and the limit; otherwise C24's p=0 case would be wrong. This supplies a
separate mathematical justification for the CDF-based reference against
which C21's stop-loss certificates were tested.

The 1,568 tests still enumerate only a finite probability grid and two
allowances. They do not establish the theorem for every uncertain source;
C21's proof and R24's published finite-reference reduction supply that
argument. The distinction prevents an exhaustive risk-level check inside
each fixture from being misreported as exhaustive source-model coverage.

## C26. The old-loss-law obstruction has a simple structural boundary

For a deterministic program on n finite inputs, let B_1,...,B_k be the
partition of inputs having identical old terminal loss. Its full loss law
retains exactly the bin masses s_j=sum_(i in B_j) p_i. A new program's mean
sum_i v_i*p_i is determined by those masses on the full probability simplex
if and only if v_i is constant within each B_j. Sufficiency is direct:
sum_i v_i*p_i=sum_j v_(B_j)*s_j. For necessity, two point-mass input laws
on differently valued members of one bin have identical old loss laws and
different new means. A threshold strictly between them separates decisions.
C22 instantiates this obstruction inside a smaller, nondegenerate source.

The criterion preserves exact means, or all threshold answers, not necessarily
one fixed threshold or an action already determined by permanent evidence.
For a restricted convex source use the relative-kernel condition of A2.
For several retained observations write their bin-indicator matrix S; a
new mean is recoverable exactly when its direction annihilates ker S on
the admitted source direction space. This is ordinary linear sufficiency,
consistent with the decision-compression methods in R20–R22.

Separate old loss histograms need not equal a joint histogram. For two bits,
the input laws assigning half mass each to 00/11 and to 01/10 have the same
marginal bit distributions, but opposite parity. Retaining the joint bit
histogram distinguishes them. This can use C16's actual task: reading X and
answering X incurs loss c+Y, while reading Y and answering Y incurs c+X.
Their separate loss laws agree under those two sources, while the immediate
zero-answer program has error zero in one and one in the other.
More generally p(t)=(t,1/2-t,1/2-t,t), 0<=t<=1/2, fixes both old
histograms, whereas the new mean is 1-2*t. The omitted direction
(1,-1,-1,1) preserves normalization and both bit marginals. This is an
affine one-coordinate repair, not an optimization barrier; these particular
old policies are diagnostic controls rather than recommended optimal choices.
When uncertain probability models are summarized
by a set of histogram vectors, preserve that *joint feasible set*; independent
coordinate ranges need not preserve its support queries.

These facts give a family of deliberately lossy controls and exact structural
repairs. They do not justify granting one method extra source information,
requiring a dense n-state representation when a factored method suffices, or
claiming new generic information theory. The pending empirical question is
the total cost of deriving, retaining and checking the required distinctions
for declared edits and consumers, under matched access to these repairs.
