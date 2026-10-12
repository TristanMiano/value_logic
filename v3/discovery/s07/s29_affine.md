# S29: source-proved affine cost invariance

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**

This is a separate generative construction linked to
[S28's bundle derivation](bundle_theory.md). It supplies a source-sensitive
alternative to bounding objective changes over every Boolean violation mask.
It does not alter S28-B1, its executed service, its forecast event, or any
earlier frozen evidence. Helper work earns no additional principal-clock credit.

The concrete result is a small checker-backed example: one actual paid
negative proof at a nominal objective, a checked feasible witness, and an
exactly-one constraint read from the original logical source yield a
zero-regret repair across two unknown cost modes without an audit. Generic
scalar transport certifies regret two on that example. **The same paid proof
tree also certifies zero**, and ordinary source simplification can solve the
tiny instance directly. This establishes a scoped construction and a weakness
of the cheap generic margins; no comparative resource benefit is established.
The actual receipt and all comparisons are in
[s29_affine_results.json](s29_affine_results.json).

## 1. A scalar lower can use feasible-source geometry

Let $`F\subseteq\{0,1\}^m`$ be the nonempty set of violation vectors of
repairs satisfying the original hard source. For nonnegative objective
weights $`w`$, define:

```math
C^*(w)=\min_{z\in F}w^\top z.
```

Suppose a separately checked source certificate proves
$`F\subseteq Z`$ for a nonempty compact relaxation Z, and an admitted logical receipt gives
$`L_q\leq C^*(q)`$. For any nonnegative target $`v`$, let:

```math
s_Z(d)=\min_{z\in Z}d^\top z,\qquad
\ell(v)=\max\{0,L_q+s_Z(v-q)\}.
```

Then $`\ell(v)\leq C^*(v)`$. Indeed, every actual feasible
$`z`$ satisfies both $`q^\top z\geq L_q`$ and
$`(v-q)^\top z\geq s_Z(v-q)`$. Add these inequalities and minimize
over actual repairs. The final zero clamp uses nonnegative target weights,
not concavity of the clamped surrogate. The signed displacement can have
either sign in every coordinate.

An exact support minimum is unnecessary. Any independently checked lower
bound on $`s_Z(d)`$ gives a valid, possibly weaker transport. Conversely,
a feasible point of a support-minimization LP gives an upper bound on its
minimum and cannot be substituted as lower evidence.

For simple, source-proved coordinate groups, the support minimum is cheap:

| Source constraint on a disjoint coordinate group | Contribution to the signed support minimum |
|---|---|
| Exactly one violation in group G | $`\min_{j\in G}d_j`$ |
| At most one violation in group G | $`\min(0,\min_{j\in G}d_j)`$ |
| Coordinate fixed to zero | Zero |
| Coordinate fixed to one | $`d_j`$ |
| Unconstrained binary coordinate | $`\min(0,d_j)`$ |

Sum these contributions only for a disjoint decomposition of the coordinates.
Overlapping exclusions or general inequalities need a valid joint relaxation
and a charged support calculation; adding overlapping group minima can double
count a coordinate. The compact implementation below supports one
exactly-one group only. It does not claim a general constraint extractor or
an uncharged LP oracle.

If $`Z\subseteq[0,1]^m`$, its support minimum is at least the minimum
over the full Boolean cube. This provides a constructive way to strengthen
the generic signed scalar lower. A coarse relaxation can still lose much
of the actual logical structure.

### The proof boundary is different from the old leaf evaluator

An abstract leaf's forced-violation mask need not be a feasible complete
repair. A source constraint such as exactly one violation therefore does
not imply that every retained leaf mask satisfies that constraint. Applying
a feasible-only equality directly to those masks is not justified.

The theorem instead combines **two separate admitted facts**: the old
proof establishes its scalar lower at the original query; the original
source establishes the feasible geometry. A new typed scalar receipt binds
both and proves the target lower. A future `RepairEvaluator` can take the
maximum of this lower and its existing checked lower methods. Its old
leaf-mask calculation remains a separate certificate.

The earlier [s05 repricing bridge](../s05/reprice_sources.md) already proposes
globally checked core constraints, separate lower optimization, and
intersection with each leaf's upward closure. S29 specializes the
source-support part to cheap signed support and affine invariance. It does
not introduce the general idea of retaining logical structure under changed
weights.

## 2. Preserve the common cost change instead of adding two margins

Suppose the original source proves $`Az=b`$ for every feasible repair,
and every compatible objective satisfies:

```math
w-q=A^\top\lambda(w),\qquad
\kappa(w)=b^\top\lambda(w).
```

Then every repair has the same cost displacement, so:

```math
w^\top z=q^\top z+\kappa(w),\qquad
C^*(w)=C^*(q)+\kappa(w).
```

The ranking of repairs is unchanged. In an exactly-one group, a common
coordinate shift is such a displacement because $`\sum_jz_j=1`$.
Changes to source-proved mandatory violation costs are another example.
Those costs still affect the choice between repair and replacement.

Let $`u\in F`$ be a checked retained repair, with its **unclipped**
nominal cost $`U_q=q^\top u`$, and let $`p\geq0`$ be the fixed
replacement price. Suppose valid source bounds give
$`\kappa_{\min}\leq\kappa(w)\leq\kappa_{\max}`$. The following
uniform regret bounds are sound:

```math
B_{\mathrm{repair}}=
\max\{0,\ U_q-L_q,\ U_q+\kappa_{\max}-p\},
```

```math
B_{\mathrm{replace}}=
\max\{0,\ p-\max(0,L_q+\kappa_{\min})\}.
```

For repair, its excess over the best repair is at most
$`U_q-L_q`$ because the common shift cancels; its excess over replacement
is at most $`U_q+\kappa_{\max}-p`$. Taking the larger comparison gives
the bound against their minimum. For replacement, the checked target lower
is $`\max(0,L_q+\kappa(w))`$, whose worst value is bounded using
$`\kappa_{\min}`$. Select whichever fixed action has the smaller
certificate. This is uniform source uncertainty, not an expectation.

For independent finite cost rows, take reference vectors with
$`q=\sum_i r_i`$. If each compatible row displacement has a checked
representation
$`m_{ih}-r_i=A^\top\lambda_{ih}`$, then:

```math
\kappa_{\min}=\sum_i\min_{h\in Q_i}b^\top\lambda_{ih},
\qquad
\kappa_{\max}=\sum_i\max_{h\in Q_i}b^\top\lambda_{ih}.
```

These extrema also cover the convex hull of the compatible row configurations.
No configuration product or Boolean model enumeration is required. If rows
have additional joint restrictions, the product calculation is a sound outer
bound but may be loose. Discovering a useful equality basis and finding these
representations is paid work; the tiny implementation only compares
coordinates for a common shift.

### A further direction when invariance is imperfect

Source geometry also supports a candidate-specific contrast bound.
For the same row decomposition and a fixed checked repair $`u`$, define:

```math
d_{ih}=m_{ih}-r_i,\qquad
\Gamma_i(u)=
\max_{h\in Q_i}\bigl[d_{ih}^\top u-s_Z(d_{ih})\bigr].
```

Each term is nonnegative because $`u\in Z`$. For any compatible
source and any feasible competitor, add the query lower and the rowwise
support inequalities to obtain:

```math
w^\top u-C^*(w)\leq
U_q-L_q+\sum_i\Gamma_i(u).
```

Let $`H_W(u)=\sum_i\max_{h\in Q_i}m_{ih}^\top u`$, the exact
upper cost over the row product. Then a valid repair certificate is:

```math
\max\{0,\ U_q-L_q+\sum_i\Gamma_i(u),\ H_W(u)-p\}.
```

This keeps each row's signed change attached to the chosen repair. If a
displacement is constant over the source relaxation, its contribution is
zero automatically. Separate positive upper and lower margins cannot
preserve that cancellation. The formula is a derived next mechanism;
it is not implemented or evaluated in the current S29 script. Multiple
reference decompositions can be compared, but no optimal-decomposition
claim is made.

## 3. Replacement prevents unconditional cancellation

A mandatory repair cost cancels between two repairs but does not shift the
fixed replacement price. Using signed changes on an already clipped query
upper can therefore be wrong.

Consider an exactly-one source with nominal weights $`q=(1,100)`$,
a proved nominal lower $`L_q=1`$, only the second repair retained
($`U_q=100`$), and replacement price $`p=50`$. At the nominal
objective, replacement has regret 49. Under the common shift
$`\kappa=-1`$, the target weights are $`(0,99)`$. The optimum
repair now costs zero, so replacement has regret **50**.

The clipped nominal upper is 50. Shifting that number to 49 would pretend
that replacement became cheaper and could falsely report regret 49.
The formulas above use the actual repair cost 100 and the unchanged price
50; they give a repair bound 99 and a replacement bound 50.

The nonnegative-margin reserve in S28 does not make this signed substitution
and remains unaffected. The S29 interface must retain the original query
witness cost and the signed source displacement before clipping.

## 4. A family that Boolean and row-correlation margins miss

Take one exactly-one group of $`m\geq2`$ violations. Let nominal weights
be $`q_j=a+j`$ for zero-based indices, with $`a\geq T>0`$.
The cost source has two modes:

```math
q-T\mathbf 1,\qquad q+T\mathbf 1.
```

Every feasible repair changes by only $`-T`$ or $`T`$.
With a checked exact nominal optimum and a retained optimal repair,
repair-versus-repair uncertainty is zero. If the price exceeds the greatest
possible cost of that repair, its uniform regret is zero without learning
the mode.

For the centered one-row decomposition, the generic Boolean and
[row-correlation margins](row_margins.py) are each $`mT`$, because
they allow all m coordinates to be violated at once. Even source-simplex
positive margins remain $`\alpha=\delta=T`$. The affine comparison
cancels the shift exactly. This gap scales with the number of coordinates;
it is not obtained by selecting a special query budget in the old fixture.

The source may include additional hard constraints that restrict the
exactly-one simplex. An externally checked nominal lower can exploit those
constraints even when the cheap geometry checker retains only the simplex.

### The actual compact acquisition

[s29_affine.py](s29_affine.py) instantiates four violation literals
`[1,-2,3,-4]`, with soft unit clauses of opposite polarity. Hard clauses
require exactly one violation, and an additional hard unit forbids the first,
cheapest violation. The nominal weights are `[3,4,5,6]`; the public
incumbent violates the second soft clause and costs four.

The program actually:

1. Admits the complete provider code contract and checks the original source.
2. Checks the public incumbent against the original hard clauses and weights.
3. Calls the complete branching provider at budget three and independently
   checks its returned UNSAT tree, obtaining $`L_q=4=U_q`$.
4. Reconstructs each transported scalar lower from that raw proof and the
   source geometry. It uses the two declared modes `[1,2,3,4]` and
   `[5,6,7,8]`; it makes no cost audit.
5. Computes ordinary generic-anchor and same-paid-tree comparisons and
   checks three invalid-input controls.

| Recorded quantity | Result |
|---|---:|
| Nominal checked lower / witness cost | 4 / 4 |
| Lower from the exactly-one simplex alone at the nominal query | 3 |
| Generic Boolean transport lowers at the two modes | 0, 4 |
| New source-feasible transport lowers | 2, 6 |
| Revaluation of the same paid negative tree | 2, 6 |
| Row-correlation upper / lower margins | 8 / 8 |
| Exactly-one positive upper / lower margins | 2 / 2 |
| Affine repair-versus-repair uncertainty | 0 |
| Actual complete logical purchases | 1 |
| Actual cost observations | 0 |
| New LP / native optimization calls | 0 |
| New full logical-model enumerations | 0 |

The checked provider may branch internally; the last row does not describe
proof production as free or prohibit its ordinary search.

| Fixed replacement price | Generic-anchor best bound | Source-feasible best bound | Source-feasible action |
|---|---:|---:|---|
| 7 | 2 | 0 | Retained repair |
| 5 | 2 | 1 | Retained repair |
| 1 | 1 | 0 | Replacement |

The middle row is the material clipping check: the repair can cost six
while replacement costs five. Affine invariance alone does not certify
zero regret there. The source-feasible replacement bound is three, so the
repair's bound one is the useful choice.

The declared invoice is **8,731 operation units**: 1,567 local checks and
comparisons, 439 for the actual complete wrapper, and 6,725 for provider-code
admission. Rechecking the raw proof for the two transport receipts is included.
These are named operations, not money, and the local subtotal includes the
comparison and invalid-input work. CPU, retained storage, serialization,
source preparation and any economic conversions are not fully priced by
that subtotal. The cost modes form a declared synthetic source contract;
they were not learned from a population.

## 5. Concrete admission and future integration

The compact source checker requires distinct variables and atomic soft
clauses. A soft unit `[literal]` is violated by `-literal`.
It verifies the at-least-one clause over those **violation literals** and
every pairwise exclusion of those literals in the original hard clauses.
Extra hard constraints are allowed. This uses the explicit source encoding;
a solver's informal assertion of exactly-one structure is not accepted.

The geometry receipt records the original source identity, an identity for
the ordered hard/soft structure, the ordered violation polarities, and the
raw hard-clause indices. Scalar transport rechecks the negative receipt
identity, its source binding and the actual raw branching proof. Its new
receipt identifies the original query, target weights, signed displacement,
support minimum, resulting scalar lower, geometry receipt and raw proof
receipt. Nonnegative target weights are enforced.

The executed negative controls reject wrong atomic polarity, a missing pair
exclusion, and a nonaffine change submitted as a common shift. Source edits,
soft-clause reordering or changed assumptions require a compatible new
certificate and identity; a checksum alone does not prove a semantic
relationship between two different sources.

This remains a compact constructor, not a production interface. To expose
its bound in the shared service, a new version needs a scalar-receipt
admission branch with the above dependencies, exact arithmetic, retention
and repricing charges. It can then feed admitted target-anchor lowers into
the existing source-anchor method. A direct affine certificate can instead
use the original query lower, witness and shift range without constructing
all anchors. Neither branch is present in the already executed S28 service.

For less explicit sources, learning or proving the equality may require
new SAT/core/proof work. That acquisition, unsuccessful attempts, original
source admission, support computation, witness checking, any cost audit,
retention and reconstruction all belong in the comparison. General derived
equalities are a future scope, not a capability supplied by the small
atomic checker.

## 6. Strong conventional comparisons and limitations

An ordinary robust optimizer supplied the same source constraints can
minimize a signed objective over the same simplex, perform the same affine
elimination, and use the same worst-case comparison with replacement.
These are ordinary linear-algebra and robust-optimization constructions.
The useful local question is whether their checked compact form changes
the cost of repeated acquisition decisions.

The actual retained-tree control **ties** the new lower in both modes.
There is no measured speed advantage. Moreover, an ordinary method that
also propagates the extra hard unit can remove the forbidden simplex
vertex and obtain the nominal optimum four directly. Thus the purchased
point proof demonstrates the scalar receipt path; it is not shown to be
the minimum evidence acquisition for this tiny source.

Two primary methods provide stronger solver comparisons:

- **Niskanen, Berg and Järvisalo, CP 2021,**
  [Enabling Incrementality in the Implicit Hitting Set Approach to MaxSAT Under Changing Weights](https://doi.org/10.4230/LIPIcs.CP.2021.44),
  Sections 4.1–4.3, especially Algorithm 3, printed pp. 44:7–44:11.
  Their method retains weight-independent cores and reprices previous models.
  Its original-clause mapping explicitly distinguishes fixed satisfied and
  fixed violated soft clauses; mandatory costs are tracked in `baseCost`
  and updated when weights change. It performs hard-unit and equality
  simplification. Weight-based hardening and reduced-cost fixing cannot be
  retained indiscriminately. Fixed-feature cost factoring and persistent
  structural reuse are therefore established comparisons.
- **The same authors, SAT 2022,**
  [Incremental Maximum Satisfiability](https://doi.org/10.4230/LIPIcs.SAT.2022.14),
  Section 4 and Figure 1, and Sections 5.2–5.3, printed pp. 14:4–14:12.
  IPAMIR supports objective updates; iMaxHS retains conditional cores with
  their assumption dependencies and extends the incremental handling of
  simplification and fixed values. Its exposed optimum/status interface is
  distinct from this repository's independent raw-proof receipt requirement.

The repository already has a [persistent native IHS adapter](../s06/native_findings.md).
A useful future control retains its native SAT state, valid core rows,
objective updates and starts; it should receive the same structural
information and output tolerance. A cold restart alone is insufficient.
No complete native branch-and-bound retention or independent native-proof
export is inferred here.

The remaining limitations are concrete: useful source geometry may be
expensive to acquire; a coarse geometry may provide little transfer;
nonaffine changes need residual bounds; arbitrary references can weaken
those bounds; uncertainty along invariant directions still matters when
replacement is competitive; and admission overhead can exceed repricing
savings. A future advantage must survive those costs and the stronger
ordinary controls. This small DEVELOPMENT construction does not support
promotion or empirical transfer by itself.

## Reproduce and preserve the acquired bytes

Run from the repository root with a new output path; the script refuses to
overwrite an existing receipt. Reproduction buys a new complete proof and
is not a zero-acquisition replay:

```bash
python v3/discovery/s07/s29_affine.py /tmp/s29_affine_new.json
```

The recorded implementation SHA-256 is
`7125114f72063cc9706500555783958e31ec113a4f466af162014a906ddab673`.
The recorded result SHA-256 is
`a4c4d5157776614efb37ddf8275c2a8f8b5ba24312046373668d56c780c980c1`.
Its JSON also records dependency hashes, original source bytes, raw paid
proof, witness, geometry and scalar receipts, source modes, invalid-input
outcomes and invoice categories.
