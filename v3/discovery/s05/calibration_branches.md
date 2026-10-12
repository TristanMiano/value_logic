# Calibrating relations that decisions actually use

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; constructive support for [s05](session.md). Readiness unassessed.
Concurrent work contributes no additional principal-clock credit.
Parents: [marginal profiles](../s03/robust_tree.md),
[sparse policy contrasts](../s03/value_moments.md), and
[checked edit residuals](../s03/edit_residuals.md).

## Four mechanisms to retain

| Branch | What evidence is acquired | Constructive use | Cheap screen / comparison |
|---|---|---|---|
| Direct paired contrast | The difference of two policy scores, after symbolic cancellation | Avoid paying for common terms or resolving propositions that cancel | Best initial control for a small fixed bank; retain source identity, sharing, score range and unresolved outcomes |
| Parity-block library | Error frequencies of a few products of forecast errors | Preserve useful cancellation and cover many later fixed plans without a joint law | Stronger than singleton bounds when errors cancel; its general planning problem need not retain S25's compact profile |
| Margin-directed allocation | More receipts for the moments that dominate an undecided contrast | Spend precision where a currently useful decision needs it | An allocation formula below is only valid for separately billed streams; shared receipts change the cost problem |
| Observable source strata | Block or contrast bounds conditional on a cheap, fixed context partition | Permit different fixed plans in observably different regimes | Pays guard and stratum-sampling costs; direct stratified policy auditing gets identical access |

The second branch has a useful algebraic relation worth developing now. The
others remain alternatives, rather than a requirement to complete a new
four-part audit. None establishes an advantage over the conventional method
implementing the same relation.

## Parity certificates between singleton and full-law evidence

Fix a source of tasks, a tree and forecast signs before the calibration draws.
An edge's forecast error sign is Z_e=E_e*s_e in {-1,+1}, where E_e is checked
truth and s_e is the declared forecast. The forecasts can be fixed functions
of a task's observable context; their identity cannot be changed while keeping
the old calibration target. For an edge set B write Z_B=product_(e in B) Z_e.

Let a library F have simultaneous warranted bounds

```text
P(Z_B = -1) <= u_B,       B in F.
```

Overlaps between blocks are allowed, and their errors can be arbitrarily
dependent. If U=B_1 symmetric_difference ... symmetric_difference B_k, then

```text
Z_U = product_(j=1..k) Z_(B_j).
P(Z_U = -1) <= min(1, sum_j u_(B_j)).
```

Proof: repeated signs square to one. A negative product has at least one
negative factor. This uses a union bound over **blocks**, preserving any
cancellation already measured within a block. It does not infer independence
or an unobserved joint distribution. Define

```text
b_F(U) = min(1, min_(subsets J of F with XOR J = U) sum_(B in J) u_B).
```

If no decomposition exists, set b_F(U)=1. If the singleton edges are included,
this bound is never weaker than the old singleton union bound. Repeated use
of a block is unnecessary: two copies cancel and nonnegative cost cannot help.
Selecting a decomposition after seeing all its bounds needs no new risk charge
on their common validity event. The same event covers every U at once.

For a fixed purchased set S and rewarded vertex v, the residual error set is
U=path(v) minus S. The score guarantee can therefore replace the old additive
load by

```text
L_F(S) = sum_v r_v * max(0, 1 - 2*b_F(path(v) minus S)) - cost(S).
```

Use the declared forecast if its warranted excess score is nonnegative and
a real independent fair guess otherwise. S may be selected using calibration
evidence, stakes and prices covered by the fixed-source contract. This does
not authorize adapting S to its deployment truth receipts: unconditional
block rates need not survive that selection.

### The endpoint graph is a confidence representation

Let Y_v be the product of edge error signs from the root to v; Y_root=1.
For any pair a,b the path-block product equals Y_a*Y_b. Thus

```text
d(a,b) = P(Y_a != Y_b)
```

is a pseudometric: the event Y_a!=Y_c is contained in the union of
Y_a!=Y_b and Y_b!=Y_c. If calibrated path blocks are graph edges with weights
u_ab, any graph path supplies an upper bound for its endpoint error; shortest
paths give the tightest bound of this form.

More generally, let T be the vertices of odd degree in the residual edge
forest U, retaining the root as a formal endpoint when necessary. Every
subset J of calibrated graph edges with odd-degree set T satisfies

```text
product_(ab in J) (Y_a*Y_b) = product_(v in T) Y_v = Z_U.
```

Hence the least sum of u_ab over such a T-join is a valid bound. The
two-endpoint case is the shortest-path construction. This equation proves
validity of any supplied join; an approximate proposed join can be checked
without trusting an optimization claim. The next section identifies a scope
in which this bound is sharp; general block-mask libraries need not have
that graph structure.

These weights are **error probabilities**, not the monetary or runtime costs
of obtaining receipts. The separately developed forest-boundary cost relation
can make an edge of this confidence graph cheap to measure; the two graphs
must not be conflated.

Triangle relaxations of binary correlations are established machinery. The
abstract of Deza, Laurent and Poljak,
[The cut cone III (1992)](https://link.springer.com/article/10.1007/BF02350631),
explicitly places triangle inequalities within the cut/metric-polytope
relationship. The article's full text was not accessed; no internal theorem
is imported here. The displayed sign/event derivations establish the relation
needed for this application directly. No novelty of the metric machinery is
claimed.

## Sharpness for one parity target under pair upper bounds

The following stronger relation emerged during joint development of the
block construction. Let G=(V,E) be any finite undirected calibration graph,
let T have even cardinality, and let u_e>=0 be the **only** distributional
constraints, P(Y_a!=Y_b)<=u_ab for ab in E. All vertex-sign assignments are
allowed in the ambiguity family. Write tau_T(u) for minimum T-join weight,
with value infinity when no T-join exists. Then

```text
max_(joint laws satisfying these pair upper bounds)
    P(product_(v in T) Y_v = -1)
    = min(1, tau_T(u)).
```

The upper bound was proved above. For attainability, represent a sign
assignment by the subset A of vertices assigned -1. It has target error
exactly when |A intersect T| is odd. Replace probability mass on every
T-even assignment by the all-equal assignment; this preserves the objective
and can only reduce pair-disagreement probabilities. The remaining mass
lambda_A solves the finite packing problem

```text
maximize sum_(T-odd A) lambda_A
subject to sum_(T-odd A with e in delta(A)) lambda_A <= u_e, every e;
           sum_A lambda_A <= 1; lambda_A >= 0.
```

Ignore the normalization constraint temporarily. The LP dual minimizes
sum_e u_e*x_e over x>=0 with x(delta(A))>=1 for every T-odd A. This is the
T-join dominant: the convex hull of T-join incidence vectors plus the
nonnegative orthant. Its minimum for nonnegative weights is tau_T(u).
Finite LP duality therefore supplies a packing of total mass tau_T(u).
If tau<=1, put the remaining mass on all-equal. If tau>1, scale the packing
to total mass one. Scaling only weakens capacity usage, proving attainability.
If no T-join exists, some connected component has odd intersection with T;
flipping that whole component makes the target wrong while every observed
pair still agrees, giving value one directly. T empty gives zero.

The imported polyhedral description was checked in Cornaz, Grappe and Lacroix,
[author manuscript, section 2.1, PDF page 5](https://www-lipn.univ-paris13.fr/~lacroix/research/publications/boxTDIMF.pdf),
which explicitly gives the T-cut inequalities for an arbitrary undirected G
and even T, citing Schrijver Corollary 29.2b. Its later series-parallel
restriction concerns stronger dual-integrality properties. This argument
requires the stated primal dominant description and ordinary fractional LP
duality, not an integral cut packing. [Source notes](sources.md) retain the
original Edmonds-Johnson connection and precise import scope.

This is an adaptation of an established combinatorial min-max relation to
calibrated parity error, not a new T-join theorem. Fixing one root sign to
+1 does not change it: complement a world when its root is negative. Pair
disagreements and an even target product are both unchanged.

### What the sharpness means for acquisition

On an original tree with only its singleton edge upper bounds, the residual
edge set U is the unique T-join. Consequently min(1,sum_(e in U) u_e) is
already the sharp worst-case parity error. Its weakness cannot be repaired
by a better inequality using those same premises. New block information,
lower bounds, a narrower justified source family, or direct target evidence
is needed to obtain a stronger guarantee.

Sharpness is relative to this upper-bound-only ambiguity family. Retaining
nonzero lower bounds, exact moments, incompatible signed pair targets, or
restrictions on which joint assignments a logical source can produce can
change the optimum. Dropping that extra information still gives a valid
upper bound, but no longer establishes its tightness for the smaller family.

### Sharp individual bounds need not share a worst-case law

Take G=K_(2,3), every observed cross-partition pair bound equal to 1/5,
and query all ten vertex pairs. Each cross-partition target has sharp error
1/5; each within-partition target has sharp error 2/5. Their sum is 14/5.

Nevertheless their maximum **joint sum** is only 12/5. For one cut, let a
and b be the selected vertex counts from the parts of sizes two and three.
The number of within-partition cut pairs minus cross-partition cut pairs is

```text
a*(2-a) + b*(3-b) - [a*(3-b) + (2-a)*b]
    = (b-a) - (b-a)^2 <= 0.
```

Therefore total pair disagreement is at most twice cross-partition
disagreement, whose expectation is at most 6/5. Equality is attained by
placing mass 1/5 on each of the three singleton cuts in the larger part and
mass 2/5 on all-equal. This is an explicit simultaneous-target gap, even
though every individual sharp bound is below 1/2. Summing the per-target
score bounds remains safe but can be conservative; neither exact
multi-target minimax planning nor preservation of compact profiles follows.

## A paid example, including the stronger control

Consider a four-edge chain with known root truth, and errors

```text
Z_1=Z_2=A,  Z_3=Z_4=B,  P(A=-1)=P(B=-1)=1/5.
```

The singleton bound for the leaf is max(0,1-2*4/5)=0. In contrast, both blocks
{1,2} and {3,4} have error probability zero, as does the whole path. This
conclusion does not need A and B to be independent.

For a concrete finite calibration illustration, take n=400 independent
source draws, two prespecified block targets, and family error alpha=.05.
If each target has zero observed errors, the rule

```text
u_B = 1 - (alpha/2)^(1/n)
```

gives u_B=0.0091798046 and the two-block leaf excess-score lower bound
1-4*u_B=0.9632807817. For this simple zero-error rule, use upper bound one
when any error occurs. Its validity follows directly from the zero-error
probability (1-p)^n and a two-target union bound; it is not an unrestricted
optional-stopping confidence sequence. Shared rows need not make the two
targets independent. No simulated confidence-level validation is claimed.

Suppose each unknown vertex truth costs one checked evaluation on a row and
the root is known. All four edge marginals need x_1,...,x_4: four truth
evaluations per row. The two block products need only x_2,x_4: two. Directly
auditing the fixed leaf prediction needs only x_4: **one**. At 400 rows, the
three label bills are respectively 1600, 800 and 400, before lookup, forecast,
checking and bound-construction costs. If some truths are cached, charge the
actual missing endpoints instead; do not invoice four separate edge queries
when their truth receipts can be shared.

Thus block evidence improves the singleton representation but does not beat
the strongest fixed-leaf audit. Its possible usefulness is broader reusable
coverage under later plans and prices. A conventional symbolic/paired policy
bank with the same endpoint reuse can also exploit it. A useful comparison
must pay both the preparation and the changing-request costs.

### Retaining compact profiles requires structure

For arbitrary block libraries, b_F(path(v) minus S) is nonadditive and may
couple distant query choices. S25's compact shifted-profile proof does not
automatically extend. A tractable first version can contract adjacent edge
blocks into a smaller tree when there are no rewarded interior vertices and
the allowed query menu buys a block completely or leaves it unresolved.
Its superedge load is 2*u_B and its price is the actual block-query cost, so
S25's recurrence applies directly. This intentionally restricted menu must
be compared with conventional planning on that same contracted tree, and
with the cost of allowing useful partial queries in the original menu.

## Buying precision according to a contrast

For a covered sparse contrast D=d_0+sum_i d_i*mu_i, component intervals of
radius r_i yield a contrast radius at most sum_i |d_i|*r_i. Suppose a
prospective independent sampling design has r_i=a_i/sqrt(n_i) and each new
observation of component i costs c_i>0. Write w_i=|d_i|*a_i. The continuous
allocation minimizing sum_i c_i*n_i subject to radius <=epsilon is

```text
A = sum_i w_i^(2/3)*c_i^(1/3)
n_i = (A/epsilon)^2 * (w_i/c_i)^(2/3)
minimum relaxed observation cost = A^3/epsilon^2.
```

The equations follow by differentiating the Lagrangian; rounding counts up
preserves the width constraint. Zero coefficients require no observations.
The fixed-sample bounded-mean radii can come from
[Hoeffding (1963), Theorem 1 and equation (2.3)](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).
For variables in [-1,1], two-sided radius is sqrt(2*log(2/alpha_i)/n_i).
The theorem's independence is across source draws, not across components.

This is a planning formula, not a license to use fixed-n intervals at arbitrary
stopping times. Choose counts before a fresh batch, or use an existing valid
time-uniform/staged construction. If one checked row reveals multiple
components, c_i*n_i double-counts shared work: optimize actual receipt actions
instead. A paired direct estimate of D retains common-row covariance and may
be considerably sharper than the component box. Keep it as the primary
comparison rather than assuming all moment intervals must be acquired.

Observable source strata offer another targeted extension. If a fixed guard
C(x) has known source masses pi_c and warranted conditional block bounds,
separate fixed plans S_c have aggregate score bound sum_c pi_c*L_c(S_c).
The guard's evaluation cost belongs in the bill. Unknown masses need their
own evidence; post-selected context-dependent predictors need covered target
semantics. This handles known observable regimes without claiming conditional
validity after arbitrary truth-dependent deployment actions.

## Small algebraic screen

One inline Python/Fraction probe enumerated eight laws over four edge errors,
all 16 residual sets, and all subsets of library
F={1,2,4,8,3,12,15} (bit-mask notation). For seven laws, world x has raw weight
1+(((x+3)*(k+5)+x*x) mod 19), k=0,...,6, then weights are normalized.
The eighth law uses the displayed paired errors with independent A,B, each
error probability 1/5. For each target, the probe minimized the sum of exact
block error rates over XOR decompositions and checked

```text
actual target error <= block upper bound <= singleton upper bound.
```

All **128** target checks passed; **48** had a strictly smaller block bound
than the singleton bound. These are supplied finite-law arithmetic checks,
not acquired-source economics or an independent confirmation. The minimal
reconstruction is below; the reported confidence number is a separate
analytic illustration and does not depend on these selected laws.

```python
from fractions import Fraction as F
from itertools import product

worlds = range(16)
blocks = (1, 2, 4, 8, 3, 12, 15)
odd = lambda mask, x: (mask & x).bit_count() % 2
laws = []
for k in range(7):
    raw = [1 + ((x + 3) * (k + 5) + x*x) % 19 for x in worlds]
    laws.append([F(w, sum(raw)) for w in raw])
pair = [F(0) for _ in worlds]
for a, b in product((0, 1), repeat=2):
    pair[(3 if a else 0) | (12 if b else 0)] = (
        (F(1, 5) if a else F(4, 5)) * (F(1, 5) if b else F(4, 5))
    )
laws.append(pair)
checks = strict = 0
for law in laws:
    ps = {b: sum(law[x] * odd(b, x) for x in worlds) for b in blocks}
    bound = {t: F(1) for t in worlds}
    for selected in range(1 << len(blocks)):
        target, total = 0, F(0)
        for j, b in enumerate(blocks):
            if selected >> j & 1:
                target ^= b
                total += ps[b]
        bound[target] = min(bound[target], total)
    for t in worlds:
        actual = sum(law[x] * odd(t, x) for x in worlds)
        single = min(F(1), sum(ps[1 << j] for j in range(4) if t >> j & 1))
        assert actual <= bound[t] <= single
        checks += 1
        strict += bound[t] < single
print(checks, strict)  # 128 48
```

The next useful development is a paid structured receipt source with both
correlated errors and shared boundary truths, serving several changing
requests. Compare singleton closure, a small block library, and direct paired
policy audits under one receipt cache. Permit the result to redirect which
evidence is acquired; do not commit to the block representation in advance.
