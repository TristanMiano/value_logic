# F04 S2 — Nonlinear comparisons, joint reflection, and identifiable value

Session: 2026-09-26-S2. Base: `30d2e4702eef4363f9df3ea7d03a0404aa7a4fb5`.
Status: candidate-discrimination continuation; **not a selected calculus or a gate**.
Predecessor: [S1 countermodels](01_candidate_countermodels.md). Source-use limits
are in [the S2 source record](F04_S2_sources.md); observed effort is recorded in
[the session log](../work_logs/F04_2026-09-26_S2.md).

The selected lead remains OPP-01: task-grounded comparison using shared sources.
OPP-03 supplies a bounded reflective reconstruction; OPP-02 receives an analytical
negative control, not training. Everything below concerns explicitly supplied
finite models. A proof conditional on a source identity, loss interpretation, or
uncertainty set does not establish that empirical assumption itself.

## 1. Reconstructing the affine result before extending it

S1 writes target costs as `J = ell + B z + A eps`, with unrestricted finite
`z in R^k` and `eps in [-1,1]^m`. A linear consumer `w^T J` is bounded in both
directions exactly when `B^T w = 0`. Expanding the dot product gives the proof:
a nonzero coefficient of z can be driven to either infinity; otherwise the
remaining box has radius `sum_j |(A^T w)_j|`. Shared source identities are part
of the supplied model. Marginal ranges do not recover them.

Three conclusions should not be confused:

1. **Invariance:** changing the nuisance source changes nothing in the consumer.
2. **Finite bound:** it may change the consumer, but only within a finite range.
3. **Useful bound:** the range is tight enough for the actual margin or tolerance.

For affine consumers over an unrestricted linear subspace, the first two coincide.
They need not coincide for nonlinear consumers. The third is a separate question
even when a proof of finiteness is available.

A direct hostile example is the deterioration from raw cost z to raw cost z+1.
The difference is exactly 1. Applying squared loss produces `2z+1`, unbounded
above even on z>=0. This does not reverse the order under an increasing transform
on that domain; it invalidates reuse of the numerical deterioration bound.
In contrast, `ReLU(z+1)-ReLU(z)` lies in [0,1], despite depending on z between
-1 and 0. Shared-source arithmetic therefore needs an operation-specific rule,
not a universal cancellation slogan.

## 2. A nonlinear finite-bound criterion for finite ReLU networks

### 2.1 Objects and a global bias envelope

Let h be the scalar output of an ordinary finite feedforward ReLU network:

    u_0(x) = x,
    u_l(x) = rho(W_l u_(l-1)(x) + b_l), l=1,...,L,
    h(x) = c^T u_L(x) + d,    rho(t)=max(t,0) coordinatewise.

All dimensions and coefficients are finite. The input x can have arbitrary
finite signed magnitude. Let h_0 be the *same* network with every bias b_l and
the final offset d set to zero. This is a comparison construction, not a claim
that deleting biases preserves the original network's predictions.

Define nonnegative vectors and a scalar by

    e_0 = 0,
    e_l = |W_l| e_(l-1) + |b_l|,
    beta = |c|^T e_L + |d|.

Absolute values on matrices are entrywise. Define also the nonnegative row

    p^T = |c|^T |W_L| ... |W_1|.

**Lemma F04-C09 (bias and input envelopes).** For every finite x,y,

    |h(x)-h_0(x)| <= beta,
    |h_0(x)-h_0(y)| <= p^T |x-y|.

**Proof.** The scalar ReLU satisfies `|rho(a)-rho(b)| <= |a-b|`.
Inductively, the discrepancy between the biased and zero-bias hidden vectors
is bounded coordinatewise by e_l. The affine output gives the first inequality.
For two inputs of the zero-bias network, repeat the argument with initial
bound |x-y| and no bias terms; matrix multiplication gives the second. Both
bounds hold globally, not only within the currently active region. Also
`h_0(t x)=t h_0(x)` for t>=0, by positive homogeneity at every layer. These are
structural baseline properties of ReLU networks, not novelty claims. Square.

The bound is generally conservative: large cancelling paths can make beta and
p large while the actual function is small. Its role is to prove an implication,
not to identify a canonical or minimal semantic description.

### 2.2 Restricting only the uncontrolled directions

Supply a common input-source contract

    x = ell + B z + A eps,
    z in R^k, eps in [-1,1]^m.

Here h can be a difference between two loss outputs: stacking two finite
networks and subtracting their affine outputs is still a finite ReLU network.
This presupposes the same source input is supplied to both outputs.

Let `s = |ell| + |A| 1` and `C = beta + p^T s`. The preceding lemma implies

    |h(ell+Bz+A eps) - h_0(Bz)| <= C                         (1)

for all admitted inputs. Empty bounded-source matrices cause no difficulty:
`|A|1` is then the zero vector. The set of admitted inputs is nonempty.

**Theorem F04-C10 (one-sided and two-sided boundedness).** Under this contract:

    sup_(z,eps) h(ell+Bz+A eps) < infinity
        iff h_0(Bz) <= 0 for every z in R^k;                (2)

    inf_(z,eps) h(ell+Bz+A eps) > -infinity
        iff h_0(Bz) >= 0 for every z in R^k.                (3)

Both endpoints are finite iff h_0 vanishes on the range of B.

**Proof.** If the right side of (2) holds, (1) gives h<=C uniformly. If it fails,
choose z_* with h_0(Bz_*)>0. Along z=t z_*, t>=0, with eps=0, (1) and positive
homogeneity give

    h(ell+t Bz_*) >= t h_0(Bz_*) - C -> infinity.

This proves necessity. Reverse the inequalities for (3). Their conjunction
is precisely h_0(Bz)=0 everywhere. Square.

For a smaller-is-better cost comparison h=J_new-J_old, a finite upper bound is
enough to bound replacement loss `max(h,0)`. Requiring both-sided boundedness
would unnecessarily exclude `h(z)=-|z|`, which has upper bound zero and an
unbounded amount of improvement. Conversely, a finite upper bound C that exceeds
the requested tolerance does not authorize that use.

This is a global theorem about a specified finite ReLU function and specified
linear nuisance space. It is not a theorem for arbitrary nonlinear losses,
uncertified loss proxies, unconstrained changing source identities, or functions
with infinitely many affine regions. The universal test on h_0 can itself require
many region checks. No polynomial-time general verification claim is made.

The uniform O(1) remainder in (1) is essential. A mere vanishing asymptotic
slope is insufficient: `h(z)=sqrt(|z|)` has `h(tz)/t -> 0` for each fixed z as
t tends to infinity, but is unbounded above. This function is not a finite
ReLU network, and its deviation from the zero function has no uniform finite
bound. The positive theorem uses the full network envelope, not just a
pointwise limiting-ray heuristic.

### 2.3 Sharp one-dimensional control

For the narrower scalar family

    h(z)=q z+c+sum_i v_i rho(k_i z+b_i),

define tail slopes

    s_plus = q + sum_(k_i>0) v_i k_i,
    s_minus = q + sum_(k_i<0) v_i k_i.

The right tail increases without bound iff s_plus>0; the left tail increases
without bound iff s_minus<0. Thus the supremum is finite exactly when
`s_plus<=0<=s_minus`. The infimum is finite exactly when
`s_minus<=0<=s_plus`. When finite, the relevant endpoint is the max or min of h
at all breakpoints `-b_i/k_i` with k_i!=0, together with z=0. Zero-slope hidden
units contribute only constants.

**Proof.** The listed breakpoints partition the real line into finitely many
intervals on each of which h is affine. An affine function has no strict interior
extremum. The tail signs are the stated necessary and sufficient conditions at
infinity. Under them a finite extremum is attained at a listed endpoint, or on
a constant segment; including 0 handles the globally constant case. Square.

**Worked losses.** Set `J_old(z)=3+rho(z)` and `J_new(z)=1+rho(z+1)`.
Both are nonnegative and unbounded above. Their difference is

    -2                     when z<=-1,
    z-1                    when -1<=z<=0,
    -1                     when z>=0.

It has sharp range [-2,-1]: replacement improves loss by at least one. Its
zero-bias comparison is zero, so (2)-(3) certify finiteness. The crude beta
bound for this expression is 3, however, and would only enclose it in [-3,3].
The breakpoint calculation establishes the useful negative upper endpoint.
This separates a finiteness certificate from a decision-useful certificate.

**Hostile local observation.** `rho(z-2)` is exactly zero on [-1,1] yet has no
finite upper bound on the whole real line. An observed activation region or a
bounded training sample cannot establish the universal tail condition in (2).
A certified restriction of the use domain *would* change the question.

### 2.4 Exact invariance is stronger

For a continuous finite piecewise-affine h on the whole R^n, exact invariance
under x->x+Bz holds iff every affine slope on a nonempty full-dimensional region
annihilates B. Necessity follows by taking small line displacements inside a
region. For sufficiency, restrict h to any finite line segment parallel to Bz.
There are finitely many affine pieces on that segment. Every slope is zero in
the line direction, and continuity joins the constants. A segment lying on a
face is covered by closures of full-dimensional cells, where the same argument
holds by continuity. Lower-dimensional input domains require a relative-region
version rather than silently applying this whole-space statement.

This condition differs from (2)-(3). `rho(z+1)-rho(z)` is bounded but not invariant.
Its middle-region slope is 1. Its zero-bias function is nevertheless zero.

Nor does invariance of the output require invariant hidden units. For example,

    rho(x1)-rho(-x1)-rho(x2)+rho(-x2) = x1-x2

is invariant under (x1,x2)->(x1+t,x2+t), but none of the four individual hidden
preactivations annihilates that common direction. Imposing invariance neuron by
neuron would discard a valid ordinary network representation. This motivates
looking for an inherited computation, rather than imposing a preferred form.

## 3. Equal-information comparison of the surviving routes

For the worked losses, give *both* routes exactly the same functions, source
identity and domain. Route A carries their joint expression and derives a
piecewise bound by ordinary linear arithmetic on the stated regions. An
RLL-like numerical layer can check translated finite inequalities, but neither
source validity nor ReLU region coverage is certified merely by naming RLL.
This session does not emit an RLL proof for the whole network theorem.

Route B carries the same admitted family and lower-evaluates the gain
`J_old-J_new`. Its infimum is also 1. It therefore reaches the same guarantee;
there is no semantic win for Route A created by withholding information from B.
A Route B implementation still needs an algorithm or certificate for the
infimum, just as Route A needs a sound region or envelope procedure.

A scalar-baseline implementation retaining only individual marginal loss ranges
cannot recover the margin: each marginal is an unbounded half-line, and without
the source relation the two losses can move independently. That is a comparison
of retained information, not proof that scalar output types cannot accompany
relational evidence.

The viable tradeoff is now sharper. A joint expression plus a small certificate
can be compact on structured cases; a general lower-value transformer expresses
more observations but may hide the computational burden in evaluation. Neither
has yet earned a global efficiency or completeness claim. Gate A must consider
which admitted composition and update family it is actually selecting.

## 4. Reflection when neither branch is assumed infallible

### 4.1 A versioned common-policy model

S1's SELF-MIX-v1 had a zero-failure safe branch. Here define a different, named
version, `F04_SELF_TWO_BRANCH_v1`. A report r in [0,1] causes this same controller
to choose a cautious branch with probability r and a stress branch otherwise.
Their unknown conditional failure probabilities are a and b, respectively:

    H_(a,b)(r) = a r + b(1-r).

The word cautious is a label, not an assertion that a<b. A supplied nonempty
uncertainty set K is the convex hull of finitely many points `(a_i,b_i)` in
[0,1]^2. All costs and failure quantities in this section are expectations under the
specified branch randomization; a bound on an expected difference is not a
pathwise bound on a realized single trial. The model fixes one pair during the
assessment; the parameter cannot
be revealed to the controller merely because it occurs in the semantics.

A valid report is an upper bound on failure of *the very policy induced by that
report*, uniformly over K:

    H_(a,b)(r) <= r for every (a,b) in K.                  (4)

The criterion and the policy are linked, but validity of K and the branch model
remain external premises. This is bounded probabilistic self-assessment, not
unrestricted proof reflection or self-authorization.

### 4.2 Exact report feasibility

**Theorem F04-C11 (joint-source self-bound).** Define

    d_i = 1-a_i+b_i,
    R = max({b_i/d_i : d_i>0} union {0}).

The feasible reports in [0,1] are exactly [R,1].

**Proof.** For fixed r the left side of (4) minus r is affine in (a,b), so
checking all supplied vertices is equivalent to checking their convex hull.
For vertex i, (4) is `b_i <= d_i r`. Since a_i,b_i are probabilities,
`d_i>=b_i>=0`. If d_i>0 this is r>=b_i/d_i. If d_i=0, necessarily a_i=1,b_i=0,
and the inequality is 0<=0, not a division by zero. Taking the conjunction gives
[R,1]; each ratio is at most 1. Square.

The formula also shows why a solution always exists: r=1 trivially satisfies
it, even when the cautious branch always fails. Nonempty reflective semantics
is not an adequacy theorem. Requiring the *report itself* to be at most tolerance
t gives feasibility exactly when R<=t. That is only the report-based criterion:
a report greater than t could still induce actual failure below t, which a
separate tighter evaluation could establish.

**Dependence witness.** Let K have two vertices `(9/10,0)` and `(0,9/10)`.
Then R=9/19. At r=1/2 both vertices have failure 9/20, so this report is valid.
Replacing K by its rectangular marginal enclosure [0,9/10]^2 gives R=9/10:
it invents the jointly worst point `(9/10,9/10)`. The rectangle is conservative
but loses the positive half-report conclusion. Neither source format is wrong;
retaining their dependence makes a concrete inference difference.

### 4.3 A valid report and an optimal policy are different objects

Let k>=0 be a declared cost of using the cautious branch, in the same total-cost
units as the unit failure penalty. Among the report-valid policies, minimize

    F_K(r) = max_i { b_i + (a_i-b_i+k) r }, r in [R,1].    (5)

This is a restricted optimization problem over the named report-to-policy
family, not unrestricted optimal control or a definition of ultimate utility.

**Proposition F04-C12 (finite optimal witness).** A minimizer of (5) exists
among R, 1, and every pairwise intersection of the affine lines in (5) that lies
in [R,1]. Evaluate these finitely many candidates and choose a minimizer.

**Proof.** A finite maximum of affine functions is continuous and piecewise
affine on the compact interval [R,1]. It attains a minimum. Between successive
line intersections the active affine formula does not change. A minimum on
such an interval is at an endpoint, or the whole interval is constant and its
endpoints are minimizers too. Duplicate parallel lines add no intersection.
The candidate set includes the domain endpoints and every possible change.
Square.

This construction returns one report executable without the hidden parameter.
At a candidate r, the inequalities (4) and the upper objective bound can be
checked by rational arithmetic over every vertex. Optimality of the finite
search relies on the displayed region argument, not merely on checking the
chosen report's feasibility.

In the two-vertex example above with k=0, `F_K(r)=(9/10)max(r,1-r)`.
Its optimal report is r=1/2 with robust failure 9/20. The *least valid report*
R=9/19 instead has worst-case failure 9/19, which is larger. Thus least report
and best attainable performance differ even under the same supplied model.
Choosing r=0 for the first vertex and r=1 for the second would achieve zero
failure, but it would require learning which vertex holds before acting. The
unavailable per-model optimizer is not an alternative implementation of (5).

### 4.4 Evidence refinement: what improves, and what need not

For fixed branch functions and costs, K' subset K makes every K-valid report
K'-valid and gives `F_K'(r)<=F_K(r)` at every fixed r. Therefore

    min_(r valid for K') F_K'(r) <= min_(r valid for K) F_K(r).  (6)

This is improvement of the *optimized robust objective*. It does not order the
actual costs of the two newly optimized policies at a fixed true parameter.

**Explicit counterexample F04-C13.** Take k=3/10 and initial vertices

    T=(0,1/5), B=(0,4/5), C=(9/10,9/10).

Their total-cost lines are

    J_T(r)=1/5+r/10,
    J_B(r)=4/5-r/2,
    J_C(r)=9/10+3r/10.

The initial report floor is 9/10. C dominates the others there and its line
increases, so the unique initial optimum is r_old=9/10 with robust value 117/100.
Evidence removes C, retaining K'=conv{T,B}. The new floor is 4/9; B dominates
T until r=1, and decreases, so r_new=1 with robust value 3/10 is optimal.
If the true pair is T (retained throughout), actual total cost changes from
29/100 to 3/10: it **increases** by 1/100. All forecasts remain valid.

This is a useful limit on a prospective revision rule. A tighter uncertainty
set plus correct reoptimization licenses (6), not a promise of true-model expected-cost
improvement in every retained model. To require that stronger improvement, add
an explicit paired comparison of the old and new *deployed* policies across
K', or retain the old policy when that paired requirement is unresolved.
For linear branch costs the paired difference has a small vertex certificate;
the existence of that certificate is a separate criterion, not automatic.

### 4.5 What this changes about the candidate comparison

Route A can expose (4) as finite inequalities in a common control/report r and
return the rational witness from (5). Route B can expose the robust transformer
`r -> sup_K H_(a,b)(r)` and the same optimization. Both need the same K, policy
version and cost meaning. Both fail if they replace the common r by a different
r for each hidden parameter and still call the result deployable.

For each fixed r and pair (a,b), terminal values are still evaluated by a
normalized positive linear kernel. The feedback dependence on r is not a
monotonicity claim about a terminal-value argument. This separation retains
S1's distinction between continuation values and the controller parameter.

No global core is selected. The smallest viable reflective scope now includes
correlated uncertainty over two fallible branches, a common executable report,
and finite report-constrained cost optimization. Its uncertainty model is still
supplied, and empirical validity, arbitrary recursion and proof self-reference
remain unestablished.

### 4.6 Positive repair: reoptimization with a paired deterioration budget

The preceding counterexample need not force a choice between blind reoptimization
and never changing the policy. Let r_old already be valid under the current K,
and choose a nonnegative task-loss allowance delta. Demand

    J_(a,b)(r)-J_(a,b)(r_old) <= delta for every (a,b) in K.

For the same policy version and cost k, write `s_i=a_i-b_i+k`. The *same-model*
difference is exactly `s_i(r-r_old)`: the baseline b_i cancels. Thus the new
constraint is not a subtraction of separately optimized worst-case values.

**Proposition F04-C15 (nonempty guarded revision and cumulative bound).** The
report-valid policies meeting the paired allowance form the closed interval

    lower = max({R} union {r_old + delta/s_i : s_i<0}),
    upper = min({1} union {r_old + delta/s_i : s_i>0}).

It contains r_old, and so is nonempty. Minimize F_K over this interval using its
endpoints and the same finite line intersections as in Proposition C12. The
result is a common executable policy meeting the paired allowance, and its
current robust cost is no greater than F_K(r_old).

**Proof.** For s_i<0 the inequality imposes the displayed lower bound; for s_i>0
it imposes the upper bound. A zero slope imposes no condition because delta>=0.
The report-valid interval is [R,1]. Each additional inequality holds at r_old,
so their intersection is nonempty and compact. The continuous piecewise-affine
objective attains a minimum at a candidate point by the same argument as C12.
Since r_old is feasible, the minimizing objective is no worse. Every vertex
inequality is satisfied, hence so is the inequality at every convex combination.
Square.

For the refinement counterexample, current K'=conv{T,B} has slopes 1/10 and -1/2.
With r_old=9/10 and delta=0, the interval is the singleton {9/10}: a universally
non-worsening change is unavailable in this report family. With delta=1/200,
the interval becomes [89/100,19/20]. Its optimum is r=19/20 with robust cost
13/40. The true T-cost is 59/200, exactly 1/200 above its old value 29/100.
The budget therefore has an explicit achievable meaning, rather than a vague
permission to take more risk. With vertices (0,4/5),(0,3/5), k=1/5 and old report
1/2, both slopes are negative, and delta=0 still permits the strict robust
improvement to r=1. The guard is not equivalent to freezing every policy.

For a finite sequence of such updates, let every K_t contain the same actual
parameter pair and retain the same cost and policy-version semantics. At step t,
a paired bound delta_t gives

    J_actual(r_n)-J_actual(r_0) <= sum_(t=1)^n delta_t

by telescoping the per-step differences. For nested evidence sets, validity of
the prior report is preserved; otherwise it must be checked separately. This
is a conditional arithmetic guarantee, not a statistical certificate that all
K_t contain the actual pair. A sampling procedure would need its own joint or
selection-aware validity statement. Changing target costs or branch semantics
also requires a new bridge rather than silent reuse of the telescope.

This finite construction is adjacent to safe/baseline policy improvement and
robust optimization; no priority claim is made. Its role here is to provide a
positive, testable repair to a failed value inference while retaining uncertainty
and a genuinely report-dependent behavior.

## 5. Another neural negative control: absolute costs are not identified by choices

The prospective [neural design](../experiments/F04_neural_probe_design.md) uses
positive action costs J0(x),J1(x). Its pointwise weighted-cross-entropy optimum is

    p(x)=J0(x)/(J0(x)+J1(x)).

For any positive function g(x), define `J0'(x)=g(x)J0(x)` and
`J1'(x)=g(x)J1(x)`. They give exactly the same p(x) for every input. Scaling the
entire conditional loss by positive g(x) leaves its unrestricted pointwise
optimizer unchanged. This is not a claim that a finite-capacity trained network
or its optimization trajectory is invariant to reweighting its training data.

**Proposition F04-C14 (observational equality need not preserve interventions).**
For a donor d and base b, the two hypothetical J0-only interchange predictions are

    H = J0(d)/(J0(d)+J1(b)),
    H' = g(d)J0(d)/(g(d)J0(d)+g(b)J1(b)).

Since costs and scales are positive, H'=H iff g(d)=g(b), by cross-multiplication.
Thus input-dependent common scaling is invisible observationally but can change
the isolated-cost intervention prediction.

Take base costs (1/2,1/2), donor costs (3/4,1/2), g(b)=1 and g(d)=2.
The ordinary outputs are unchanged by the recoding, but H=3/5 and H'=3/4.
A constant scale, unlike this input-dependent scale, preserves both predictions.
These are two candidate high-level explanations, not proof that both have low-level
implementations in a given network. Intervention evidence is exactly what is needed
to decide whether either proposed explanation is useful.

This adds a control distinct from hidden-neuron rescaling. S1's hidden gauge
changes parameterization without changing a *transported* intervention. Here the
high-level semantic decomposition itself changes while observational predictions
stay equal. Absolute action-cost structure should not be inferred from a successful
output fit, nor forced on the hidden layer to make the interpretation pass.
The design remains unexecuted. No alignment, training, or held-out claims are made.

## 6. Status and useful next discriminators

The new work rules out four tempting shortcuts: treating all shared-error
cancellation as linear; proving a global bound from one observed activation cell;
identifying the least valid self-report with the best policy; and inferring an
absolute internal cost decomposition from observational choice alone.

Positive results are correspondingly scoped: a finite-ReLU uncontrolled-direction
criterion; an exact one-dimensional certificate; joint report feasibility and a
finite common-policy optimizer; and an intervention that can separate otherwise
equivalent cost interpretations. These are same-agent finite derivations
using standard mathematical techniques. No broad priority or novelty claim is made.

A useful next F04 reconstruction should challenge the remainder/bias criterion on
multidimensional nuisance subspaces and compare certified precision/cost rather
than simply retaining more raw data. It should also test which weaker or coarser evidence still suffices for the
*paired deployed-policy* revision guard, and whether a nontrivial model class
admits it without storing all parameter vertices. The present guard is already
constructive for the finite vertex representation; its representation cost is
not yet characterized.
The candidate selection belongs to Gate A, and a fully specified rule system to
F05/F06; neither is silently completed by these examples.
