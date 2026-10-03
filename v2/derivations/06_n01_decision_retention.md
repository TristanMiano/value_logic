# N01 derivation notebook: preserving loss decisions under revision

Contributor: **Codex (GPT-6)**. October 2, 2026, America/Los_Angeles.
Status: N01 derivations complete at the stated planning scope; same-agent
proofs and self-review, not a novelty claim or F11 implementation.

## D1. A concrete scientific loss family

Consider numerical integration over [0,1] for the declared polynomial family

    f(t) = a + d*t + b*t^2 + c*t^4.

The constant and linear parts are integrated exactly by every composite
trapezoidal rule T_n below. Summing powers, or subtracting the exact integrals
1/3 and 1/5, gives

    T_n(t^2) - 1/3 = 1/(6*n^2),
    T_n(t^4) - 1/5 = 1/(3*n^2) - 1/(30*n^4).

Define beta=b/6+c/3 and gamma=-c/30. Then

    e_n := T_n(f) - integral(f) = beta/n^2 + gamma/n^4.       (1)

Conversely c=-30*gamma and b=6*beta+60*gamma, so every real beta,gamma
corresponds to a member of this family; the two coordinates are not fictitious
independent errors assigned to different algorithms. Richardson extrapolation
R=(4*T_2-T_1)/3 has

    e_R = (4*(beta/4+gamma/16)-(beta+gamma))/3 = -gamma/4.     (2)

T_1, T_2 and R use respectively 2, 3 and 3 unique function evaluations;
R reuses T_1's nodes inside T_2. The fallback T_4 uses 5. Let the declared
evaluation price be rho=1/32 in the same cost unit as absolute integration
error, and define

    L_a(beta,gamma) = abs(e_a(beta,gamma)) + rho*N_a.

This price is an explicit task preference, not a measured execution time.
Verification/construction time is a separate evaluation metric. Loss is
relative to the exact integral of the declared polynomial model, not a claim
that that model is empirically adequate for arbitrary physical functions.
Evidence supplied as coefficient constraints needs its own external warrant.
Remainders, noisy fitting and adaptive quadrature are outside this first family.

The three initial queries compare a in {T_1,T_2,R} to F=T_4:

    q_a: L_a - L_F <= 0 for every admitted (beta,gamma).     (3)

The operative decision is the first certified action in the fixed order
T_1, T_2, R, F; F is always an available self-comparison. Preserving all three
threshold answers preserves this decision, although it is a stronger contract
than preserving only the selected action. We select the stronger finite
threshold-vector contract prospectively; recovering sharp bounds is only a
reference calculation, not the chosen retention objective.

## D2. Evidence and a finite revision contract

All coordinates, row budgets and prices use a single numerical unit in this
first study. Thus full source and target-unit reduct coincide; a reachability
restriction cannot manufacture a baseline disadvantage. Permanent rows are

    -1 <= beta <= 1,       -1 <= gamma <= 1.

Two revisable joint rows are

    beta + gamma <= r_plus,
    -(beta + gamma) <= r_minus.

The first attempted grid used only these two rows, with budgets
{0,1/4,1/2,1,2} or absent. **That candidate was rejected during N01:** the
line beta=-gamma remains in every source; at |gamma|=1 both T_2 and R fail
their comparisons, while the coarse grid mostly leaves T_1 useful only at
the zero-width joint strip. This is too impoverished to test the intended
alternative-support and multi-action behavior. The failure is a design finding,
not experimental evidence for a retention advantage.

The revised contract uses r_plus,r_minus in G={0,1/16,1/4,1,2} or absent,
and two additional independently withdrawable evidence bundles:

    B: -b_cap <= beta <= b_cap,
    H: -g_cap <= gamma <= g_cap,

where each cap belongs to H={0,1/64,1/4,1}, or the entire two-row bundle is
absent. Bundle H and the numerical set H are distinguished by context below;
implementation should name them `gamma_band` and `cap_grid` respectively.
There are 6^2*5^2=900 evidence configurations, including intentionally
redundant constraints with different provenance. Not all describe distinct
geometric sets. All are feasible: the origin witnesses them. The four
permanent rows keep them bounded. The first F11 slice can use the 16 states
in which each of the four bundles is at budget zero or absent; the full 900
is the declared finite extension for differential checks, not already executed.
Strengthening, weakening and withdrawal change supplied evidence only; changed
coefficients, algorithms, units or loss prices create a new compiled family.

Order is not part of an isolated logical answer, but affects online search and
cache cost. Later evaluation must distinguish the 900-state correctness universe
from declared update sequences and from their selection/training distribution.
Repeated enumeration of the same states is not extra independent evidence.

The stronger contract for future work may include more rows and rational
budgets. No conclusion from this finite grid silently covers their continuum.

## D3. Ordinary optimization has the same joint information

Write u=e_a(x), v=e_F(x), k=rho*(N_a-N_F). The query difference is

    abs(u)-abs(v)+k
      = max(min(u-v+k,u+v+k), min(-u-v+k,-u+v+k)).          (4)

This has two outer clauses, each a minimum of two affine forms. For each
clause i, with leaves a_ij*x+c_ij, source A*x<=r, and nonempty source, solve

    maximize z subject to A*x<=r, z<=a_ij*x+c_ij for j=1,2.

Its dual is

    lambda>=0, alpha>=0,
    A^T*lambda = sum_j alpha_j*a_ij, sum_j alpha_j=1,
    objective lambda^T*r + sum_j alpha_j*c_ij.             (5)

The query's sharp robust difference B_q is the maximum of the two optimal
clause values. Fixed row directions make this an ordinary parametric LP
problem. A row withdrawn from the source requires lambda_row=0 in any reused
certificate. Keeping a dependency mask with the dual vector therefore gives
the ordinary baseline exactly the same support-eligibility test as a native
proof portfolio. Native checking adds a typed reception contract, not extra
mathematical information or an automatic speed advantage.

Every dual vertex has at most three positive components: (5) is a nonnegative
system with two balance equations plus one sum equation. More precisely the
supported columns must be independent, so degeneracy can reduce that number.
Enumerating independent column sets of size at most three is a bounded exact
producer option for this two-coordinate family, not a general solver claim.
The native producer must separately compile and check the corresponding
weighted-min/source argument; numerical dual feasibility alone is not a
received native certificate. A separate semantic reference can instead split
the signs of u,v and optimize an affine expression on each resulting polygon.

## D4. Finite threshold retention is a coverage problem

Fix the finite query/state universe, a complete finite dual catalogue P for
each clause, and an exact semantic reference. Let Good contain (state,q)
pairs with B_q(state)<=0. For a candidate proof p, let its coverage contain
(state,q,i) when (state,q) is Good, p proves clause i for q, its support is
present, and its replayed upper bound is <=0. Only accepted query pairs enter
the required universe U={(state,q,i):(state,q) in Good, i in {1,2}}.

**Finite coverage criterion.** A retained subcatalogue preserves every true
threshold answer through max-of-clause replay iff its coverage union is U.

Proof: if the union covers U, every required clause has an eligible <=0
certificate, so their maximum is <=0 and the native combination can certify
q. Conversely, a replayed max bound <=0 requires both clause minima <=0;
each is attained in the finite eligible retained set, hence supplies a covering
proof. Soundness prevents any false positive regardless of coverage. Empty
eligible sets mean unavailable, not a proof that the threshold is false.

For indivisible proof costs, minimum-cost retention is a weighted set-cover
formulation of this fixed finite catalogue. This is an established optimization
formulation, not a novelty claim or a hardness proof for this restricted family.
Shared native DAG nodes make actual storage cost non-additive; charge real
serialized bytes and checking work rather than silently summing root costs.
Computing Good and the full candidate catalogue can itself be expensive and
must be charged. A fitted cover cannot count its training states as held-out
application evidence. A lazy ordinary solver can choose not to pay this cost.

## D5. What this does and does not propose

The potential application result is a measured, checked tradeoff among small
threshold-preserving joint-evidence portfolios, selective recomputation and
complete parametric envelopes on this loss family and stated extensions.
The coverage lemma, quadrature identities and dual replay are building blocks.
They are not, separately or merely combined in notation, a supported novelty
claim. A fair ordinary portfolio can implement the same coverage criterion.
The implementation study must be allowed to find no favorable operating region.

## D6. Check that the revised family changes actual decisions

Four exact cases prevent an all-fallback or one-action benchmark:

* beta=gamma=0: the three differences are -3/32, -1/16, -1/16;
  the order selects T_1.
* beta=0, with only the permanent gamma bound: T_2's worst difference is
  15/256-1/16=-1/256. T_1 and R fail at gamma=1. The order selects T_2.
* gamma=0, with only the permanent beta bound: T_1 and T_2 fail at beta=1,
  while R's difference is -abs(beta)/16-1/16. The order selects R.
* only permanent rows: T_1 and T_2 fail at (1,1); R fails at
  (-1/16,1), where e_F=0 and its difference is 3/16. Select F.

The second case is not dependent on a zero-width assumption: if
abs(beta)<=1/64 and abs(gamma)<=1, then the reverse triangle inequality gives

    abs(e_2)-abs(e_F) <= abs(e_2-e_F)
                       <= 3/(16*64)+15/256 = 63/1024,

so its total loss difference is <=-1/1024. Likewise a joint strip
abs(beta+gamma)<=1/16 gives T_1 difference <=1/16-3/32=-1/32.
These are sufficient margins, not assertions that these simple bounds are
sharp throughout the family.

There are real alternative supports. With the joint strip at zero, T_1 is
certified without the beta/gamma bands. With both coordinate bands at zero,
T_1 is certified without either joint row. Starting with both supports present,
withdraw the two joint rows: the threshold stays true even though a proof
that used them is no longer eligible. Dependency checking plus new search can
recover it too. That ordinary strategy must be included in the comparison.

## D7. One complete ordinary catalogue covers every withdrawal mask

In the full dual polyhedron D_i of (5), a withdrawn row j imposes
lambda_j=0. Because all lambda_j are nonnegative, their simultaneous zero
conditions define a face F_S of D_i. Every vertex of that face is a vertex
of D_i: if v in F_S is a nontrivial convex combination of points in D_i,
nonnegativity forces every withdrawn coordinate of both points to be zero,
contradicting extremality in F_S. Conversely any vertex of D_i in F_S
remains extreme in the face. The dual vertices for an eligible mask are
therefore exactly the eligible full-catalogue vertices.

The permanent box ensures finite clause optima for every mask. Elementary LP
duality and the independent-support argument in F08 consequently imply that
filtering a single full catalogue gives the sharp value for every admitted
RHS and mask. No separate full vertex enumeration per mask is necessary.
This is an ordinary polyhedral fact applied here, not a new theorem claim.

With all optional bundles, there are at most ten source rows and two clause
leaves. A vertex has at most three positive coordinates, at least one of them
an alpha. There are at most

    2 + (2*10+1) + (2*choose(10,2)+10) = 123

eligible column supports to inspect per clause, before linear dependence,
infeasibility and duplicate elimination. Six clauses give at most 738 such
candidate supports. These are enumeration bounds, not measured run times or
counts of actual distinct vertices, native proof nodes or serialized bytes.

## D8. An even stronger preprocessing baseline

The coordinate-band rows duplicate permanent row directions. An ordinary
solver may replace each pair by its tightest present bound:

    beta_bound=min(1,b_cap) if beta_band present, otherwise 1;
    gamma_bound=min(1,g_cap) if gamma_band present, otherwise 1.

It retains the winning support (and can rescan the short group after withdrawal).
For an absent joint row, the permanent box supplies beta+gamma<=2 or its
negative. The resulting six-direction system has exactly the same feasible
set as the original source. Derived fallback rows must carry their small
source proof if results pass through the native receiver.

This permits a six-direction parametric baseline with replayed effective RHS,
even though original evidence identities differ. At most

    2 + (2*6+1) + (2*choose(6,2)+6) = 51

column supports per clause need inspection. Both systems may use this reduction;
forbidding it to the ordinary baseline would create an artificial advantage.
The mathematical catalogue is small enough that a generic cache-size novelty
claim is particularly implausible here. This family is a feasibility experiment;
an eventual contribution needs a meaningful application finding or a broader
supported limitation beyond these established constructions.

## D9. Two further ordinary baselines challenge the scope

**A finite answer table.** For exactly 900 configurations and three Boolean
answers, an offline table has only 2,700 answer bits before keys and evidence.
The initial solving cost and the current-state identification cost still count.
If proof reception is required, attach proof-root references or use the table
to select currently checked witnesses; count those payloads too. A hash alone
is not a proof, but excluding a table altogether would handicap the baseline.
Thus this finite universe is suitable for development correctness, not by
itself a compelling unknown-update retention workload.

**A fixed ReLU verification problem.** For each comparison write

    N_q(x)=ReLU(e_a(x))+ReLU(-e_a(x))
           -ReLU(e_F(x))-ReLU(-e_F(x))+k.

This is a two-input, four-hidden-unit ReLU network with an affine output;
N_q equals the loss difference pointwise. All three comparisons can share
eight signed-error hidden units. Verifying N_q<=0 on the current polytope
is exactly an input-domain verification problem. This is a constructed
representation, not evidence that ordinary training learns these quantities.
The source checks N1/N3 therefore apply to the problem structure, not merely
by analogy. The native proof interface may add useful checking contracts,
but a claim of new numerical expressive power for this family would be false.

The response is to keep the finite grid as development fixtures and propose
bounded **rational RHS continua** as the actual extension: r_plus,r_minus in
[0,2], b_cap,g_cap in [0,1], with the same finite row/withdrawal schema and
queries. All hypotheses of the fixed-catalogue result remain satisfied.
This is a prospective scope refinement before any empirical result, not a
switch from threshold preservation to sharp-bound optimization. It does not
evade the ordinary parametric baseline or establish novelty. N01 continuation
must settle and document this refinement before implementation is selected.

## D10. A finite exact test for uniform threshold preservation

The following is an optional paper construction, unimplemented. Fix one
withdrawal mask and a nonempty rational compact parameter polytope Theta.
For each query q, let the complete eligible finite certificate set P_i for
clause i have affine replay functions ell_p(theta). Let S_i be the retained
subset. The reference threshold region is

    T = {theta in Theta: for every i, some p in P_i has ell_p(theta)<=tau}.

The retained family preserves the threshold exactly iff every theta in T has
the same existential witness in each S_i. Soundness already prevents positives
outside T. It is not necessary to preserve optimal values inside T.

For each clause j whose retained family might fail and each tuple
(p_i)_i selecting one complete proof per clause, form this rational LP:

    maximize delta
    theta in Theta;  0<=delta<=1;
    ell_(p_i)(theta)<=tau for every i;
    ell_s(theta)>=tau+delta for every s in S_j.             (6)

**Criterion.** Uniform preservation fails iff at least one such LP has a
strictly positive optimum. Infeasible LPs are harmless. Empty S_j leaves no
last constraints and correctly detects any nonempty reference-positive region.

Forward proof: choose a missed theta in T and a failing clause j. Select
one full-catalogue witness p_i for each clause. Every retained bound in S_j
is strictly above tau. Finiteness gives a positive minimum gap; its minimum
with 1 is a feasible positive delta in (6). Reverse proof: a feasible positive
delta makes the full witnesses certify all clauses while every retained bound
for j exceeds tau. Hence that theta is a missed true threshold answer.
Compactness ensures an optimum when the LP is feasible; rational coefficients
allow a rational missed parameter and exact LP certificates.

Apply (6) separately to every admitted mask and query. This is a finite
disjunctive-linear coverage decision procedure, not a claim of a new general
polyhedral algorithm or a cheap practical method. For two clauses of at most
51 candidates each, a crude bound is 2*51^2 LPs per query/mask; the 3-query,
16-mask bound is 249,696 before pruning. The bound makes indiscriminate full
coverage checking an unattractive first-hour implementation requirement.
No LP in that count has been run here, and no catalogue cardinality is measured.

Unlike separate clause-wide preservation, this criterion permits omission of
proofs useful only at parameter points where another clause already makes the
whole query false. Give the ordinary baseline the same query-specific freedom.

## D11. Vertex checks and threshold margins have limits

Take 0<=t<=1 and 0<=x<=min(2*t,t+3/4). Query x<=1. Full replay gives
B(t)=min(2*t,t+3/4); retaining only the second proof gives U(t)=t+3/4.
At t=0 the true answer is preserved; at t=1 the reference answer is false,
so there is no positive answer to retain. Checking only those two parameter
vertices would pass. At t=3/8, however, B=3/4<=1 while U=9/8>1.
This countermodel uses only affine source rows and one scalar query.

Even if *all* vertices have true answers, an arbitrary correlated revision
polytope can defeat vertex-only checking. On 0<=x<=min(2*t,2-2*t), query
min(x,1/2)<=1/2. The source-free cap certifies it for every t. Retain only
the two source-row proofs: their minimum is zero at both endpoints, but 1
at t=1/2. Discarding the cap loses that interior answer.

There is a useful special case: for a coordinatewise RHS box, nonnegative
dual multipliers make each replay bound monotone. If the entire query is
certified at the box's largest RHS, retaining one successful witness per
clause there certifies the whole box. This does not apply to the preceding
correlated line or to preserving only the reference-positive subset of a box.

If an approximate portfolio has B<=U<=B+epsilon, it preserves every answer
with B<=tau-epsilon, but need not preserve answers in (tau-epsilon,tau].
In particular, equality B=tau cannot be dismissed as negligible. A measured
small value error does not meet the chosen exact threshold contract. Useful
approximate variants must declare that changed contract separately.

## D12. Even losses collapse the asymmetric revision family

This is a further hostile derivation, obtained before implementing any retention
experiment. Write B and G for the effective coordinate caps from D8, and give
an absent joint row its valid box-implied budget 2. Put R=max(r_plus,r_minus).
Every comparison h_a=abs(e_a)-abs(e_F) is even: h_a(-x)=h_a(x).
If P is the original source polytope, then

    P union (-P) = S(B,G,R)
      := {abs(beta)<=B, abs(gamma)<=G, abs(beta+gamma)<=R}.       (7)

Indeed the coordinate box is symmetric, and the two allowed intervals for
beta+gamma are [-r_minus,r_plus] and [-r_plus,r_minus]. They overlap at zero;
their union is [-R,R]. Every point in the right-hand set is in at least one
of the two original sets. Consequently sup_P h_a = sup_S h_a, even though
P and S need not be equal. This is a loss-specific semantic reduction, not
permission to erase source identities from the reception contract.

One withdrawn joint row therefore removes the semantic benefit of the other
for these particular even queries: R=2 and the permanent box implies the strip.
Two distinct asymmetric RHS pairs with the same maximum have the same answers.
The 900 development configurations yield at most 5*4*4=80 effective parameter
triples, often fewer distinct feasible sets; an answer-only table then needs
at most 240 bits before keys. Native source receipts can still differ.

For certificate production, both original joint inequalities can be weakened
to R; an absent one is derived from the permanent box. Compile that source
transformation and both max branches explicitly. An ordinary solver may exploit
evenness and solve just one branch. Such preprocessing is allowed on both
sides, with native compilation/checking costs disclosed. This reduction is
specific to fixed homogeneous signed errors and symmetric coordinate bands.

## D13. Closed-form sharp bounds defeat an expensive solver-only baseline

Scale the unpriced comparative errors by 256. The three functions are

    H_1(x) = 256*abs(beta+gamma) - abs(16*beta+gamma),
    H_2(x) = 16*abs(4*beta+gamma) - abs(16*beta+gamma),
    H_R(x) = 64*abs(gamma) - abs(16*beta+gamma).

All maxima below are over S(B,G,R), with B,G,R nonnegative. These formulas
are exact for the whole bounded rational continuum, including zero-width sets.
They are reconstructed elementary optimization, not claimed new quadrature
results. Their main purpose is to strengthen and cheapen the baseline.

**T_1.** By symmetry take s=beta+gamma>=0. Its largest feasible value is
S=min(R,B+G). At fixed s, beta lies in
[max(-B,s-G), min(B,s+G)]. Minimizing abs(15*beta+s) chooses the point nearest
beta=-s/15. That point never exceeds the upper endpoint. Its distance from
the lower endpoint gives the minimum residual

    d_1(s)=max(0, s-15*B, 16*s-15*G).

Thus the best value at s is 256*s-d_1(s), the minimum of three affine
functions whose slopes are 256,255,240. It is increasing, so

    M_1 = min(256*S, 255*S+15*B, 240*S+15*G).                  (8)

**R.** By symmetry take y=gamma>=0. Its largest feasible value is
Y=min(G,B+R). At fixed y, beta lies in
[max(-B,-R-y), min(B,R-y)]. The nearest point to -y/16 gives

    d_R(y)=max(0, y-16*B, 15*y-16*R).

The two positive residual expressions cannot both be positive on a feasible
slice: that would imply y>B+R. The best value 64*y-d_R(y) is increasing,
with possible slopes 64,63,49. Hence

    M_R = min(64*Y, 63*Y+16*B, 49*Y+16*R).                  (9)

**T_2.** By symmetry take u=4*beta+gamma>=0. The largest feasible u is

    U=min(4*B+G, 3*B+R, 4*R+3*G).

For example, if B<=G+R, beta=B is feasible and the best gamma is
min(G,R-B); otherwise beta=G+R and gamma=-G. This proves the stated maximum.
At fixed u, the feasible gamma interval has lower endpoint
max(-G,u-4*B,(-4*R-u)/3) and upper endpoint
min(G,u+4*B,(4*R-u)/3). The target gamma=4*u/3 is never below the lower
endpoint. Minimizing abs(4*u-3*gamma) therefore gives

    d_2(u)=max(0, 4*u-3*G, u-12*B, 5*u-4*R).

The best value 16*u-d_2(u) is increasing, with slopes 16,12,15,11. Thus

    M_2=min(16*U, 12*U+3*G, 15*U+12*B, 11*U+4*R).         (10)

Feasibility of every intermediate slice follows from convexity and the origin:
the projection on each selected nonnegative coordinate is the full interval
from zero to its maximum. Compactness supplies all endpoint optimizers.
Equations (8)-(10) therefore attain the sharp maxima, not merely upper bounds.
The actual sharp loss differences are

    B_q1=(M_1-24)/256, B_q2=(M_2-16)/256, B_qR=(M_R-16)/256. (11)

These are constant-size rational formulas. They remove the need for a general
LP to answer this family's threshold queries. The independent sign-cell
reference and native proof producer remain useful as cross-checks, but an
empirical speed comparison that omits (8)-(11) would now be misleading.

The result changes the ambition forecast: this family can establish a checked
producer/reception path and expose retention overhead, but offers little reason
to expect a meaningful arithmetic speed advantage from proof caching. A useful
later contribution must survive a richer family and these simplified controls,
or establish a supported limitation/contract result. Do not promote the toy
closed forms themselves to a novelty claim.

## D14. Small explicit envelopes, not merely small formulas

Expanding the nested minima in (8)-(10) and removing dominated affine forms
gives an even simpler ordinary reference:

    M_1=min(256*R, 255*R+15*B, 240*R+15*G, 240*B+255*G),
    M_2=min(48*B+15*G, 33*B+15*R, 48*R+33*G),
    M_R=min(64*G, 63*G+16*B, 49*G+16*R,
            79*B+63*R, 49*B+65*R).                         (12)

For T_2, the two non-obviously dominated expanded forms are
36*B+12*R+3*G and 44*B+4*R+11*G. They are respectively the 1/5–4/5 and
11/15–4/15 convex combinations of 48*B+15*G and 33*B+15*R, so cannot
lower their minimum. For R, the omitted 64*B+64*R is no smaller than
min(79*B+63*R,49*B+65*R): separate R>=15*B and R<=15*B. The other
omissions follow coefficientwise nonnegative domination.

These envelopes have direct source arguments. For the positive outer branch
of each scaled query, use the following two leaves, writing s=beta+gamma:

| Query | First leaf | Second leaf |
|---|---|---|
| T_1 | 255*s-15*beta = 240*s+15*gamma | 257*s+15*beta |
| T_2 | 48*beta+15*gamma = 33*beta+15*s = 48*s-33*gamma | 80*beta+17*gamma |
| R | -16*beta+63*gamma = -79*beta+63*s | 16*s+49*gamma = 65*s-49*beta |

The minimum of the two leaves is no larger than either leaf or their average.
For T_1, their average is 256*s; the other three bounds come from the first
leaf and the indicated source constraints. For T_2, its first leaf alone
gives all three bounds. For R, the average is 64*gamma and either leaf gives
the remaining four. Substituting (-beta,-gamma) gives the other outer branch
and exchanges positive/negative source rows. All coefficients used to combine
source bounds are nonnegative. Scaling by 1/256 and adding the price difference
recovers native-style upper-bound arguments without a general optimizer.

Thus twelve affine expressions suffice to recover all three sharp semantic
bounds for the canonical symmetric family. This is not a measured minimum
native DAG size: symmetry, effective-row receipt and both branches still need
their explicit proofs, source references and current budgets. A symbolic
producer can generate those using the same small templates. Retaining every
one of these templates is a mandatory cheap control before studying selective
retention; it may already make selection overhead pointless in this family.

## D15. Threshold-only retention saves nothing uniformly in this first envelope

There is a stronger negative result than merely observing that the formulas
are small. On the canonical parameter box

    Theta = {0<=B<=1, 0<=G<=1, 0<=R<=2},

**all twelve affine expressions in (12) are needed for uniform exact threshold
preservation within the model of a minimum of fixed affine upper bounds.**
The comparison is per query, with thresholds 24,16,16 respectively. This is
a representation-specific result, not a lower bound for arbitrary programs,
conditional templates, shared DAGs or a solver allowed to produce new proofs.

Here are interior parameter points (B,G,R). At each point the named expression
is exactly its threshold and every other expression for that query is strictly
larger. The points are rational so these strict comparisons are checkable.

| Query / expression | B | G | R |
|---|---:|---:|---:|
| T_1: 256R | 1/2 | 1/2 | 3/32 |
| T_1: 255R+15B | 1/320 | 1/2 | 511/5440 |
| T_1: 240R+15G | 1/2 | 1/20 | 31/320 |
| T_1: 240B+255G | 1/32 | 11/170 | 1 |
| T_2: 48B+15G | 17/96 | 1/2 | 1 |
| T_2: 33B+15R | 113/264 | 3/4 | 1/8 |
| T_2: 48R+33G | 3/4 | 10/33 | 1/8 |
| R: 64G | 1/2 | 1/4 | 1 |
| R: 63G+16B | 1/128 | 127/504 | 1 |
| R: 49G+16R | 1/2 | 15/49 | 1/16 |
| R: 79B+63R | 1/128 | 1/2 | 1969/8064 |
| R: 49B+65R | 191/784 | 1/2 | 1/16 |

For a proof of necessity that also permits new affine candidates, take any
row's point theta_0 and denote its unique active affine expression by ell.
The strict gaps and interior location imply M=ell on an open neighborhood of
theta_0. Any uniformly sound affine upper bound p satisfies p>=M there.
If it preserves the true threshold at theta_0, then p(theta_0)<=tau=M(theta_0),
so p-ell is affine, nonnegative on a neighborhood, and zero at its center.
Every directional derivative must be zero (test both signs); thus p=ell
identically. No different affine upper bound can serve this point. The twelve
listed expressions are also sufficient by (12), proving the restricted minimum.
This uses exact equality decisions essentially; a margin-only contract differs.

By contrast, within the displayed catalogue the 900-state development grid
needs only eight expressions:
T_1's first and fourth, all three of T_2's, and R's first, fourth and fifth.
The omitted T_1 expressions can be <=24 only when R is 0 or 1/16, where its
first expression already certifies. The omitted R expressions can be <=16
only when G<=1/4 on this grid, where 64G already certifies. Each of the eight
remaining expressions has a grid point where it alone certifies: for T_1 use
(B,G,R)=(1,1,0),(0,0,2); for T_2 use (0,1,2),(1/4,1,0),(1,1/4,0);
for R use (1,1/4,2),(0,1,1/4),(1/4,1,0).

An eight-template portfolio optimal within that grid catalogue misses admitted
continuum decisions, for example T_1 at (0,1,8/85) or (1,0,1/10), and R at
(0,16/63,2) or (1,16/49,0). These are losses of true answers, not unsound
positive answers. An ordinary lazy solver can recover them on demand.

This displaces a concrete hoped-for advantage in the seed family: replacing
sharp-bound preservation by exact threshold preservation does **not** reduce
the number of affine replay expressions required uniformly here. The apparent
grid reduction is an artifact of the tested revision set. This is useful
negative planning evidence; a toy polyhedral fact is not by itself a supported
project-level novelty claim. A retention study should not spend further chunks
trying to recover this already-refuted advantage under the same contract.

## D16. A general scaling obstruction to threshold compression

The seed result suggests a broader check before choosing a harder family.
Let C be closed under positive rational scaling. Let M(theta)>=0 be a finite
sharp unpriced loss bound and U(theta)>=M(theta) a finite retained upper bound.
Assume both are positively homogeneous on C. Fix a threshold tau>0.
Then

    [for every theta in C, M(theta)<=tau implies U(theta)<=tau]
        if and only if U=M everywhere on C.                 (13)

The reverse direction is immediate. For necessity, suppose b=U(theta)>a=M(theta).
If a>0, choose a positive rational t in (tau/b,tau/a]; the interval is nonempty.
Then M(t*theta)<=tau<U(t*theta), a missed true answer. If a=0, choose rational
t>tau/b and obtain the same contradiction. Thus b=a. An infinite retained
bound also fails whenever a finite reference bound can be scaled into the
acceptance region. Rational scaling suffices; no irrational test input is needed.

This is a positive-homogeneity/level-set fact reconstructed here, not a claim
of a new general theorem. It is relevant because a fixed min/max family of
linear RHS replay expressions is positively homogeneous. Across unrestricted
rescaling, an exact positive-threshold contract can already require sharp
bound preservation. Merely asking for a Boolean answer does not guarantee a
smaller retained bound representation.

The assumptions matter. Our actual admitted parameter set is **bounded** and
not closed under arbitrary scaling. Permanent box constraints, fixed offsets,
changes to loss prices and arbitrary conditional decision programs can break
the needed homogeneity or domain closure. Do not apply (13) to them silently.
Within one bounded ray {t*v:0<=t<=T}, write a=M(v), b=U(v), with b>=a>=0.
Exact preservation on that ray holds iff either b=a or T*b<=tau. If b>a and
T*b>tau, the interval (tau/b,min(T,tau/a)] is nonempty (use T when a=0),
giving a missed answer. Conversely T*b<=tau makes all retained answers true.
This characterizes exactly where bounded revision can permit coarser bounds.

An alternative margin contract has different consequences. On a scale-closed
domain, for 0<epsilon<tau, preserving only M<=tau-epsilon is equivalent to

    U <= [tau/(tau-epsilon)]*M                               (14)

under the same homogeneity hypotheses. Sufficiency is substitution; necessity
uses scaling to the smaller threshold, or density of rational scalings.
When M=0 it still requires U=0. This is a relative bound guarantee, not a
license to replace an exact contract with an arbitrary small absolute error.
N01 keeps exact threshold preservation; (14) is a separately identified option.

For the next family, therefore test three questions before expensive selection:
which rays cross the threshold, whether apparent savings only exploit the
bounded revision range, and whether an ordinary symbolic formula already
represents the same level set cheaply. These are structural checks that a
larger random benchmark alone would not settle.

## D17. A second negative control: many proof roots, little retained structure

The provenance comparison in literature N10–N11 motivates a deliberately
unfavorable test for a flat portfolio. Let x_0=0, with real x_1,...,x_k.
At each stage i there are two independently withdrawable premises

    a_i: x_i-x_(i-1) <= r_i^a,
    b_i: x_i-x_(i-1) <= r_i^b.

Whenever at least one premise remains at each stage, put m_i equal to the
smallest remaining budget. The exact upper bound on x_k is sum_i m_i:
summing the selected inequalities proves the upper bound, and the assignment
x_i=sum_(j<=i) m_j attains it. If both premises disappear at any stage, the
increments at that stage are unconstrained and x_k has no finite upper bound.
The other increments can still attain their individual bounds. Every source
is feasible. No hidden bounds on intermediate x_i may be added to this test.

Set every budget to zero and ask x_k<=0. Consider the 2^k masks that retain
exactly one of a_i,b_i at each stage. A fixed, sound proof of this query must
use some premise at every stage: otherwise the missing-stage construction
above is a countermodel to its support. To remain eligible in one of these
masks, its support can contain only that mask's chosen premises. Consequently
one fixed root cannot cover two different such masks. A portfolio whose only
operation is selecting an already complete eligible proof needs at least
2^k roots. Retaining one summed proof per mask attains that count.

This is a lower bound for **fixed roots with conjunctive support eligibility**.
It does not apply to a program that constructs a new root, a circuit with
explicit alternatives, or a different reception contract. The alternatives
have the factorized description

    (a_1 OR b_1) AND ... AND (a_k OR b_k),

or the corresponding product of sums in positive provenance. That circuit
has O(k) size. An ordinary producer can scan the stages, pick a surviving
premise of minimum budget, and emit one sum proof in O(k) arithmetic and
reference operations. This produces the sharp bound, so threshold preservation
requires no additional insight. Counting expanded roots while ignoring this
ordinary construction would manufacture an exponential advantage.

There is also a straightforward dynamic baseline. Keep the two budgets and
availability bits at each stage and a balanced binary tree of the m_i sums.
An absent stage has m_i=+infinity as a bookkeeping value, not a native real
term. One premise change updates a leaf and O(log k) ancestors. Storage is
O(k); a cached semantic threshold query is O(1), using unit-cost arithmetic.
Bit complexity depends on rational encoding sizes and must be reported
separately. This is an ordinary data structure, not a novel algorithm.

For fresh explicit certificates, a positive root still needs a surviving
source reference at each stage, giving Omega(k) references under this
particular serialization contract. With a receiver that keeps previously
checked subproofs, a single revision may need only O(log k) new proof nodes
plus receipt of the changed leaf, provided unchanged node/source versions are
actually reusable. Both routes must be given that same receiver cache. The
untrusted producer cannot simply declare an old subtree checked. Thus future
experiments must distinguish semantic query time, fresh-certificate cost and
incremental receipt, rather than using one timing to stand for all three.

This family is a useful baseline sanity check, not a proposed new scientific
application or a project novelty claim. It rules out replacing the small
quartic family with an equally misleading combinatorial proof-count example.

## D18. Exact threshold compression is possible on a bounded revision domain

The preceding negative results do not make the research question vacuous.
Here is a small positive control, stated at the semantic affine-bound level.
For revision parameters 0<=x<=3 and 0<=y<=1, let the source constrain a
real loss variable z by

    0<=z,  z<=x,  z<=2+y.

It is always feasible and its sharp upper bound is M(x,y)=min(x,2+y).
For threshold tau=1, the retained bound U(x,y)=x preserves the exact answer:
since 2+y>=2>1, M<=1 iff x<=1 iff U<=1. Nevertheless at (x,y)=(3,0),
M=2 while U=3. Both pieces are needed for sharp-bound recovery, but only
the first is needed for this threshold contract. This is not a saving
obtained by quietly dropping equality cases.

The saving depends on the admitted revisions and threshold. If the second
budget were permitted below 1, or the query threshold rose to 5/2, its
removal could lose true answers. The fixed offset and bounded parameter
range prevent the scale-closed hypotheses of D16. An ordinary symbolic
preprocessor detects the same simplification immediately. Native proofs
give no semantic advantage, and selection overhead could exceed the saving.

A slightly broader criterion explains the example. Suppose a complete
envelope is M=min_i ell_i and P is a retained subset. Exact threshold
preservation is equivalent to

    union_all_i {theta: ell_i(theta)<=tau}
        = union_i_in_P {theta: ell_i(theta)<=tau}

within the declared revision domain. Soundness gives one inclusion; the
other is precisely absence of missed true answers. A piece always above
tau is removable for that query even if it is sometimes sharp. Conversely
the interior, uniquely active threshold points of D15 obstruct removal,
even when new uniformly sound affine pieces are allowed. This is a
specialization of ordinary coverage, not an additional general novelty claim.

The positive control gives a concrete requirement for a richer application:
identify scientifically justified parameter ranges, prices or margins that
make some distinctions irrelevant to its actual decisions, then show a
useful total-cost consequence against symbolic preprocessing and reconstruction.
Merely increasing polynomial degree or enumerating more evidence masks is
not enough. The range restrictions must be defended as part of the application,
and any claimed benefit must be tested outside the development grid while
remaining inside those restrictions.

## D19. The action set is another scientific falsifier

The seed's comparison is deliberately within four fixed grid rules. It must
not be presented as an optimal general-purpose integration policy. If all
sample locations have the same declared evaluation price and Gaussian rules
are allowed, an ordinary method changes the problem substantially.

For the three-point Gauss rule on [0,1], use nodes

    1/2-sqrt(15)/10, 1/2, 1/2+sqrt(15)/10

with weights 5/18,4/9,5/18. In the centered coordinate u=t-1/2, the rule's
zeroth, second and fourth moments are 1,1/12,1/80, respectively; all odd
moments through degree five vanish by symmetry. These equal the exact
integrals of the centered monomials. Thus the rule integrates every
polynomial of degree at most five exactly, including every seed function.
With the declared cost convention its loss is exactly 3*rho. It pointwise
dominates both T_2 and R, which have the same three-evaluation price and
nonnegative error, and dominates F=T_4 strictly by at least 2*rho.

The two-point Gauss rule has nodes 1/2±sqrt(3)/6 and equal weights 1/2.
Its second centered moment is exact and its fourth-moment error is
1/144-1/80=-1/180. Its seed error is therefore -c/180=gamma/6.
It also pointwise dominates R: it costs one fewer evaluation and has
absolute error |gamma|/6 rather than |gamma|/4.

For example, replacing the fallback by three-point Gauss and including
two-point Gauss gives the comparisons

    T_1: sup |beta+gamma| <= rho = 1/32,
    G_2: sup |gamma| <= 6*rho = 3/16.

On the canonical source S of D12,

    sup_S |beta+gamma| = min(R,B+G),
    sup_S |gamma| = min(G,B+R).

The upper bounds follow directly from the strip and coordinate bounds.
They are attained: for the first, split min(R,B+G) into nonnegative beta,
gamma within their respective caps; for the second, take gamma=min(G,B+R)
and beta=-min(B,gamma), giving |beta+gamma|<=R. Both assignments lie in S.
Hence the expanded-action problem has still cheaper exact ordinary formulas.
This is a derived ablation, not a new implementation or a replacement of
N01's fixed threshold-vector contract.

Gaussian nodes are irrational. That is not an excuse to omit this comparison
from a claim about mathematical quadrature with ideal exact evaluations;
the original loss model already uses ideal evaluations and ignores rounding.
If practical floating-point evaluation, permitted node locations, acquisition
costs or nested reuse are meant to exclude it, those restrictions and their
cost consequences need an explicit application justification. With already
acquired samples, total distinct-node counts are not automatically the right
incremental prices either. No such empirical justification is supplied here.

Consequently F11 may use the four-rule family as a controlled native-interface
fixture and negative control. A later scientific-utility claim must either
defend a restricted action set or include competitive ordinary quadrature
actions. It cannot rely on the weakness of the chosen fallback. This is a
second reason, independent of retention, to avoid predicting a novel practical
integration method from this seed. The Gaussian formulas above are classical;
the centered-moment calculation records their exact relevance to this model.

## D20. Current answers and sufficiency for future edits are different contracts

A second route beyond the seed concerns what a revision request supplies.
Let S be source states, Q a fixed query set, d(s) its exact answer vector,
and T a declared set of total deterministic edit operations. Suppose a retained
encoding h is the only old state available: a reader computes d(s) from h(s),
and an updater computes h(t(s)) from h(s) and the edit t. Then

    h(s)=h(s') implies d(w(s))=d(w(s')) for every finite edit word w. (15)

Proof: equal encodings stay equal after one deterministic update; induction
extends this to a word; the common reader then gives equal answers. Conversely,
the equivalence defined by agreement under every edit word is a sufficient
semantic encoding: one edit maps equivalent states to equivalent states by
prefixing that edit to every future word. Reading the empty word gives the
current answer. This describes a quotient, not an efficient finite algorithm;
it may have infinitely many classes. It is the ordinary future-observation
principle behind state minimization and query-preserving abstractions, not a
claimed new theorem. The needed query family includes compositions with edits,
not only the original current-state predicates.

Even one threshold can require much more than one bit under this contract.
Take x in the rationals in [0,1], d(x)=[x<=1/2], and edits
t_delta(x)=min(1,max(0,x+delta)) for rational delta in [-1/2,1/2].
For x<x', choose delta=1/2-x. The updated x equals the threshold, whereas
the updated x' is strictly greater. Hence every two distinct rational x
have different future behavior: no finite-state encoding supports all these
edits exactly without recovering information elsewhere. On the finite grid
{0,1/N,...,1}, with even N and edits in multiples of 1/N, the same argument
gives N+1 distinguishable states and a lower bound of ceil(log2(N+1)) bits
for fixed-length encodings. Storing x's grid index attains that state count.

By contrast, if the only edits supply an absolute new value x:=v, one current
answer bit is sufficient: the updater computes [v<=1/2] directly. With no
updates, one bit is sufficient as well. Thus an apparent retention advantage
or impossibility can be caused by the update interface rather than the logic.

There is a corresponding example inside the seed family. Fix B=0,G=1 and
both joint budgets equal to r in [0,8/85]. For this range the three scaled
sharp bounds are 255r,15r,63r, respectively, so all current threshold answers
are true. For r<r', weaken both joint budgets by delta=8/85-r. At the first
state T_1 remains true at equality, whereas at the second it becomes false.
All revised budgets remain inside the admitted range; the other two answers
remain true. Merely retaining the three old answers cannot process this delta
edit without the old numerical source information or an equivalent encoding.

This does not invalidate an answer table indexed by a newly supplied complete
source, nor does it prove a lower bound on a system allowed to read that source.
N01's selected comparison **does supply the complete current source to every
route**. Its key construction, source reading and stored source registry must
be accounted for. The stronger no-reread/delta-edit contract is a separately
identified research option, not a condition silently imposed on the baseline.

For a later scientific/self-assessment comparison, record whether a revision
is an absolute replacement, a delta, a withdrawal by identifier, or a new
query/price; what old data remains accessible; and whether cached checked
subproofs survive. This can generate useful cross-case findings about where
the cost moves. A generic future-equivalence lemma alone does not support
novelty, but a real application that forces a different retention/receipt
tradeoff could justify a bounded recurrence rather than more flat enumeration.

## D21. More query prices can force recovery of more numerical information

Fix a source state with finite nonnegative sharp bound a and retained bound
b>=a, independent of the query threshold. Requiring exact answers for every
positive rational threshold forces a=b: if b>a, a rational threshold between
them gives a true reference answer and a false retained answer. This does not
need the source-scaling assumption of D16. It changes the query language instead.

For all rational thresholds in a closed rational interval [l,u], 0<=l<=u,
the exact condition is

    b=a OR b<=l OR a>u.                                    (16)

If none holds, b>a, b>l and a<=u; the threshold max(a,l) witnesses failure
when a is rational, as in this family. For general real a, choose a rational
threshold in the same nonempty interval, except that an irrational isolated
upper endpoint needs separate treatment. The stated rational setting avoids
that issue. Conversely each of the three cases preserves all admitted answers.
Equality at u matters: a=u<b is a failure, not part of the always-false case.

For a finite ordered threshold list tau_1<...<tau_K, a current scalar bound
has at most K+1 answer patterns, identified by the first accepted threshold
or by none. If every region is realizable, ceil(log2(K+1)) bits suffice and
are necessary for a fixed-length semantic encoding. This count excludes keys,
source updates and proof evidence. It is not a certificate-memory lower bound.

In the seed, changing rho changes the unpriced thresholds to
768*rho for T_1 and 512*rho for T_2,R. Allowing all positive prices while
retaining a price-independent upper-bound representation therefore recovers
each query's sharp bound if the **whole answer vector** must remain exact.
The original fixed-price contract does not include this extension. A future
budget package that adds prices or queries must state this extra obligation;
the effort need not scale simply with the number of test cases.

## D22. Optional result: preserving the chosen action needs nine expressions

Keep the same source, actions, price and order T_1,T_2,R,F, but ask only for
the action selected by the exact reference. This is a **different and weaker
contract** from N01's selected three-answer vector. Within the same model of
fixed uniformly sound affine upper bounds per query, the exact minimum is
now nine expressions: all four for T_1, all three for T_2, and only

    J=64G,  L=49G+16R

for R. The three omitted R expressions are K=63G+16B, M=79B+63R and
N=49B+65R. They may prove additional R comparisons, but those comparisons
cannot change the selected action when J and L both fail.

For sufficiency, write tau=16, the common scaled threshold for T_2 and R.
If K<=tau and J>tau, then G>tau/64 and

    48B+15G = 3K-174G < (9/32)*tau < tau.

Thus T_2 is already certified. If M<=tau, then

    33B+15R <= (33/79)*M <= (33/79)*tau < tau;

if N<=tau, the same T_2 expression is <=(33/49)*N<tau. Therefore whenever
an omitted expression certifies R, either a retained R expression or the
earlier action T_2 suffices. Since T_1 and T_2 answers remain exact and
every retained bound is sound, the selected action is preserved everywhere.
This argument works for any common positive T_2/R threshold and any
nonnegative B,G,R. In particular it also preserves the action for every
positive rho, despite not preserving R's full threshold-answer function.
There is no conflict with D21: the observation being preserved has changed.

For necessity, D15's four T_1 witness points still require their respective
affine expressions: losing a T_1 answer changes the first selected action.
Its three T_2 witness points have T_1 strictly false, so they still require
the three respective T_2 expressions. The interior R witness
(B,G,R)=(1/2,1/4,1) has both earlier queries strictly false and J uniquely
active at 16. A second such point is

    (B,G,R)=(1/2,13/50,163/800).

There L=16, while J=416/25=16.64 and the other R expressions are strictly
greater. T_1's minimum is 1304/25=52.16>24 and T_2's minimum is
459/25=18.36>16. Both points have neighborhoods with the same strict earlier
failures. The local affine-touching argument of D15 therefore forces J and L
even if new uniformly sound affine candidates are permitted. This establishes
the restricted minimum 4+3+2=9.

On the 900-state grid, J alone suffices for R whenever R could affect the
action: L<=16 implies G<=1/4 on that grid, so J already holds. T_1 needs its
first/fourth expressions; T_2 still needs all three, with sole-success witnesses
(B,G,R)=(0,1,2),(1/4,1,1/4),(1,1/64,1/4), where T_1 is false. The J witness
(1,1/4,2) has both earlier queries false. Hence the grid's minimum for this
displayed catalogue is six, versus nine uniformly on the continuum. These
grid witnesses establish minimality within that catalogue; do not use them
alone as a lower bound for all newly constructed affine candidates.

This is a concrete application-level distinction to investigate, not a runtime
or native-DAG saving already measured, and not a priority claim for a new
general decision-compression theorem. Removing three arithmetic expressions
from a tiny ordinary formula may save nothing after selection and checking.
Both ordinary and native routes can use this policy-aware simplification.
N01 keeps full-vector preservation as the primary contract; policy-only
preservation is an explicitly labeled ablation or proposed later recurrence.

## D23. Observed estimates can collapse a much larger scientific source

Another proposed extension would fit polynomial coefficients to noisy fixed
measurements. Before choosing it, distinguish prospective method choice from
comparison of outputs already computed. Suppose all candidate estimates u_a
are known numbers, and the only uncertain target is the same scalar integral
I. Let the source be a nonempty bounded polytope in coefficients theta,
possibly obtained from measurement constraints |A*theta-y|<=eta, and let
I=c^T*theta. Its image is the attained interval [I_low,I_high], computable
with two ordinary linear optimizations.

For two known estimates u<v, the comparative absolute error is

    |u-I|-|v-I| = u-v          if I<=u,
                  2I-u-v      if u<=I<=v,
                  v-u         if I>=v.

It is nondecreasing in I. Thus its sharp maximum is its value at I_high;
if u>v the maximum is at I_low, and if u=v it is zero. Adding the known
evaluation-price difference changes none of these conclusions. Consequently
the same two numerical endpoints suffice for every pairwise absolute-loss
comparison among arbitrarily many observed estimates. A sharp witness for
the appropriate endpoint is also a comparative-error witness. For squared
error the difference u^2-v^2+2*(v-u)*I is affine, giving the same endpoint rule.

This is a per-current-source result. It does not say two fixed dual witnesses
remain sharp after every change to measurement tolerances; parametric endpoint
envelopes may have many pieces. It does show that an ordinary baseline should
share the two optimization objectives across all action comparisons, instead
of solving separately for each pair and each absolute-value branch. More
actions alone need not create proportionally more evidence work.

Nor does this collapse apply to the seed's prospective comparison: there the
quadrature outputs depend on unknown coefficients and have not all been
observed when the action is selected. With vector targets, state-dependent
action costs, uncertain observations or additional output-specific losses,
the scalar interval may also cease to suffice. Each extension must state
exactly which quantities have been observed, which costs are sunk, and which
remain decision-dependent. Adding many measurement rows while overlooking
this projection would create another artificially difficult baseline.

This elementary projection result is a further application-design control,
not a new general inference method. It favors a next research chunk that
examines a real information/acquisition protocol and its ordinary reduction
before investing in a larger synthetic source or additional benchmark loops.

## D24. The optional saving depends on a defensible policy order

The nine-expression result is not an intrinsic saving for every action policy.
If the order is changed to T_1,R,T_2,F, the same representation class needs
all twelve expressions for uniform action preservation at rho=1/32.

For the lower bound, T_1's four interior witnesses are unchanged. R's J,K,M
witnesses in D15 have T_1 strictly false. Use D22's L witness, and for N use
(B,G,R)=(9/56,1/2,1/8). At this last point N=16 is uniquely active among
R's expressions, and T_1's minimum is 32>24. Thus all five R expressions
are required by the same local affine-touching argument. Finally, at each
of D15's three T_2 witnesses both T_1 and R are strictly false. The R minima
there exceed 16; for its third witness the smallest is 556/33>16. Therefore
all three T_2 expressions are required too. The full twelve are sufficient
because they recover every sharp bound.

The two policies have the same actions, same evidence and same promise that
the chosen non-fallback action is no worse than F throughout the source.
They expose different subsets of the comparisons as operationally relevant.
Neither is claimed to choose the minimax-optimal action. This makes the
policy-only result useful for calibrating ambition, while also limiting its
application claim: the priority policy needs an independent justification.
One cannot select an order only because it produces a nicer compression
number, then advertise that number as a generally useful decision advantage.

Together D15, D22 and this result distinguish sharp bounds, all threshold
answers, and the action selected under a particular priority order. A next
comparison should name its observation contract before selecting evidence,
and report the others as labeled ablations. The elementary reductions here
are planning results, not external novelty claims or measured system gains.
