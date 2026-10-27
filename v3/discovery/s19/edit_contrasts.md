# Sharp value contrasts for independent source edits

Codex (GPT-6), s19 DEVELOPMENT. This is a proposed conditional-receipt
algorithm, not a new general sensitivity principle. It gives a bounded
counterfactual comparison without separately forgetting the shared source.

Use the independent generators and old receipts of value_sets.md. Two
specified edits give affine scalar costs f_i(x_i), g_i(x_i) for each old
generator. Their optimized values on the same hidden source are
F=min_i f_i(x_i), G=min_i g_i(x_i). We seek the sharp bounds on F-G over
sources consistent with the old receipts. Both edited action sets are
nonempty; arbitrary coupled edits or new intersection constraints are excluded.

## One anchored generator keeps the shared information

Pointwise,

    F-G = max_a [ min_i f_i(x_i) - g_a(x_a) ].          (C1)

No separate constraint that a is g-optimal is needed: the outer maximum
selects such an a automatically. For a fixed old-receipt partition T_i and
anchor a, independently optimize f_i on every nonanchor face. Put
U=min_(i!=a) max_(Q_i(T_i)) f_i, using U=+infinity if n=1. The largest
value for that anchor and partition is the ordinary linear-program value

    max_(x in Q_a(T_a), z) z-g_a(x)
    subject to z<=f_a(x), z<=U.                       (C2)

When U is infinite omit its constraint. Compactness and face feasibility
ensure attainment. Other generators can independently attain their f upper
values, so C2 is exact, not only a relaxation. Increasing U cannot decrease C2.

## Subset DP eliminates full partitions

Compute upper bottleneck prefix and suffix tables from the f face maxima,
as in s18's attainer DP. For each omitted anchor a and receipt set S, combine

    U^(-a)(S) = max_(R subset S)
                 min(prefix_(a-1)(R), suffix_(a+1)(S-R)). (C3)

Infeasible entries are absent, not numerical infinities confused with
unassigned empty sources. All prefix, suffix and omitted-anchor tables take
O(n*3^k) min/max work. For every feasible face Q_a(T), use
U=U^(-a)([k]-T) in C2 and maximize over a,T. Monotonicity in U justifies
keeping only the best outside bottleneck. This computes the exact upper
contrast. Exchange f,g and negate to obtain the exact lower contrast.

For both endpoints the construction uses at most4*n*2^k linear optimizations
(two face-max tables and two anchor tables), plus feasibility handling and
O(n*3^k) subset work. O(n*2^k) scalar DP storage suffices if prefix/suffix
tables are retained. LP dimensions, rational bit complexity and witness
storage are separate costs. A maximizing source is recovered from the anchor
LP and the attaining outside partition/face maxima. Its actual F-G must be
recomputed; the maximizing anchor then agrees with some g-minimizer.

The ordinary disjunctive optimizer is an exact comparator. A new result, if
any, is the particular structured reduction and source-edit use, subject to
close inverse-value/max-affine literature comparison.

## A small paid-reasoning consequence

One unresolved scalar t lies in [0,1]. There are two available procedures.
The first has original cost2t and edited costt; the other costs1/2 in either
version. Thus G=min(2t,1/2), F=min(t,1/2). The improvement G-F ranges exactly
over [0,1/4], peaking at t=1/4.

Separate sharp ranges F,G in [0,1/2] give improvement [-1/2,1/2]. The
pointwise monotone edit adds the lower bound0, leaving [0,1/2]. The coupled
calculation cuts this width in half to [0,1/4]. Hence an upfront edit/check
fee greater than1/4 cannot be recovered on any compatible source, while the
separate-value bound would not rule out fees up to1/2. The direct ordinary
piecewise calculation ties. This is a decision screen, not a measured
fee saving, learned probability, or general claim about real solver runtimes.

The source contract matters: the same t governs both versions. Allowing an
unrelated t after the edit invalidates the contrast. A fallible model may
propose the relationship, but a source warrant must establish it before the
screen can authorize skipping a computation.

## Bounded developmental check

The frozen edit_contrast_result.json agrees with direct rational
piecewise-linear arrangement enumeration on90 seeded segment instances,
of which3 are inconsistent. There are1962 enumerated arrangement vertices.
On8 of87 consistent cases the exact interval is narrower than the
intersection of separately sharp value bounds and globally sharp pointwise
difference bounds over the same source. Summed widths are53869/180 versus
11207/36; these are artificial-panel interval units, not fee or runtime gains.
The ordinary exact enumeration ties every endpoint. The worked improvement
range [0,1/4] is also recovered. These tests do not prove the general LP/DP
claim or establish novelty.
