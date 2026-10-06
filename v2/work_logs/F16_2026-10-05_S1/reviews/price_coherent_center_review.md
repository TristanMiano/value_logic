# F16 optional coherent-center review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, delegated separate reviewer. Date: 2026-10-05. This is an optional F16 mathematical adversarial review, with **zero principal clock credit**. It does not run an F15 stage, use frozen populations, modify an old theorem/control, or make a priority claim. The main review's partial initial proof-exposure disclosure remains in force.

## 1. Exact question and residual reduction

For `k≥2`, `M≥0`, define

`g_h=(k+1)/(k−h+1)` for `h<k`, `g_k=k+M`,

`f_r(h)=binom(h,r)/binom(k,r)` for `r=1,...,k−1`.

At a fixed level mean `μ`, let

`X_μ={x≥0:Σ_h x_h=1, Σ_h g_h x_h=μ}`.

Write `L_r=min_(X_μ) E_x f_r`, `U_r=max_(X_μ) E_x f_r`, and

`R_free=(1/2)max_r(U_r−L_r)`.

The question is whether there always exists `x∈X_μ` satisfying

`U_r−R_free≤E_x f_r≤L_r+R_free` for every `r`.                  (CC)

This means that the predictions come from a single law compatible with the **same exact old summary**. It is stronger than merely assigning feasible numbers to each query separately.

The arbitrary old-summary residual representation reduces to this question. If the retained residues are `ρ`, the remaining mass is `R_0>0`, and the remaining cost is `B_rem`, every compatible law has

`p_w=ρ_w+R_0 x_(|w|)/binom(k,|w|)`, with `x∈X_(B_rem/R_0)`.

Every target moment is a fixed offset plus `R_0 E_x f_r`. Offsets and common positive scaling preserve existence or failure of (CC). When `R_0=0`, the law is already fixed. A zero-residue level-family counterexample would therefore be a genuine counterexample to the general residual family, while a theorem for all `X_μ` would cover the whole residual representation.

## 2. Exact k=3 result and a local correction to the old prose

The principal proposed the planar argument below, and this reviewer independently checked its separation proof and its application to the moment fiber.

**Planar box lemma.** Every nonempty compact convex set `K⊂R²` contains the center of its axis-aligned bounding box. If one coordinate has zero width, this follows from the interval property on the remaining line. Otherwise translate and scale the box to `[-1,1]²`. If the origin were outside `K`, strict separation and reflection of axes would give `a,b≥0`, not both zero, with `ax+by>0` throughout `K`. A point attaining `x=−1` would force `b>a`; a point attaining `y=−1` would force `a>b`. These are incompatible. Thus the origin belongs to `K`.

At `k=3`, for one exact old unit-price numeric profile with `M>0`, take any compatible reference law. The full fiber has moment shifts

`δm_i=u`, `δm_ij=v`, `δm_123=−(u+v)/M`.

Its feasible `(u,v)` image is compact and convex. Every singleton interval is a translation of the `u` interval, and every pair interval is a translation of the `v` interval. The planar box lemma supplies a compatible law realizing **all** these interval midpoints simultaneously. Boolean inversion supplies its full probability vector; feasibility follows from membership in the fiber, not from treating arbitrary midpoint moments as automatically nonnegative.

For one-coordinate price edits, each revised order mean is its exact old mean plus an edit times either a fixed empty-prefix value, a singleton moment, or a pair moment. Hence this one law realizes all A1 midpoint predictions, simultaneously over orders and edited indices. This does not assert that the same law is the midpoint predictor for arbitrary linear combinations arising from unrestricted multiple-price edits.

The output boundary also excludes a demand that the **terminal moment** equal the midpoint of its own sharp interval. Its value at the coherent center is forced by the old mean and the chosen `(u,v)`; the midpoint of the range of `u+v` need not equal the sum of the two coordinate midpoints. A1 needs the proper-prefix moments because the terminal penalty is unchanged.

**Local disposition:** the sentence in `09_c4_price_revision.md` §10 saying the midpoint decoder “may be incoherent across orders” is overbroad in that section's specific `k=3` A1 setting. A1's radius remains correct and is attainable by a coherent law in the original exact-summary fiber. The general warning remains appropriate for higher-dimensional coordinatewise midpoint outputs, including §11's `k=4` counterexample. No old file is edited here.

## 3. Proof attempts recorded before the finite search

The singleton function is concave as a polygonal function of `g`. Thus its minimum is achieved by the endpoint law `q−` on levels `0,k`, with

`L_1=(μ−1)/(k+M−1)`,

and its maximum is achieved by an adjacent-level law `q+` on the two `g` levels bracketing `μ`. Put `B_r=E_(q+) f_r`. A natural candidate is the coherent law

`q_center=(q−+q+)/2`.

It would prove the stronger claim that the singleton width dominates all other conditional widths if the following two inequalities held for every `r`:

`2U_r≤U_1+B_r`,

`2L_r≥2L_1+B_r−U_1`.                                         (NC)

The candidate then has error at most `(U_1−L_1)/2` in every coordinate. Since each `L_r,U_r`, the endpoint law, and the adjacent-law expectations are affine on every open interval between successive `g` levels, checking (NC) at all `μ=g_j` suffices for all intervening `μ`, for one specified `k,M`. This observation does not establish (NC) for all `k,M`.

Two tempting stronger lemmas were rejected before any search:

1. **The adjacent law need not maximize `f_1+f_r`.** At `k=4,M=0,r=3,μ=g_3=5/2`, the adjacent law is pure level 3 and gives `f_1+f_3=1`. The law with level-2 mass `9/14` and level-4 mass `5/14` has the same mean and gives `29/28>1`. Thus concavity of all `f_1±f_r` as functions of `g` is not available.
2. **A simple curvature bound after the M=1 tilt is false.** At `M=1`, set `H_r(h)=(k+1−h)f_r(h)`. The tilted variables `y_h=x_h g_h/μ` have a fixed ordinary mean of `h`. However, `|Δ²H_r|≤2/k` fails: at `k=5,r=2,h=3`, the second difference is `−1/2`, whose magnitude exceeds `2/5`. The subsequent proof must not rely on that bound.

A generic simplex in three coordinates is a counterexample to coherent optimal centers for arbitrary convex sets, but is not a counterexample inside this level family. Likewise, the existing `k=4` incompatible coordinate-midpoint example does not show a strict common-radius gap, because it has a coherent center at the largest half-width.

For an exact obstruction, compact convex separation gives the following missing-lemma formulation. Let `B=∏_r[U_r−R_free,L_r+R_free]`. A failure of (CC) is equivalent to some vector `a` satisfying

`min_(x∈X_μ) Σ_r a_r E_x f_r
 > Σ_(a_r≥0) a_r L_r + Σ_(a_r<0) a_r U_r + R_free Σ_r|a_r|`.

The left side is a finite two-level optimization. Such an exact separator, or a proof that none exists for these binomial coordinates and these costs, would settle the general question.

### Additional reduction obtained before the stop

For the lower node inequality at `μ=g_j`, `j<k`, set `a=μ−1`, `s=k+M−1`, and, for a lower level `i≤j`, set `b=g_i−1`, `f=f_r(i)`. Then `s≥k−1≥2a` and `0≤b≤a`. The deficit of the endpoint chord through levels `i,k` below `p=a/s` is exactly

`D_i(s) = p − [f+(a−b)(1−f)/(s−b)]
        = (s−a)/(s−b) · (b/s−f)`.

It is nonincreasing in `s`. The derivative of its first part `b(s−a)/[s(s−b)]` has numerator `b(−s²+2as−ab)≤0`; its second part `−f(s−a)/(s−b)` is also nonincreasing since `f≥0` and `a≥b`. For chords not using terminal level `k`, the chord value is independent of `M` while `p` decreases. Hence `p−L_r(g_j)` is largest at `M=0`. This reduces the remaining lower node inequality to the zero-penalty binomial case; it does not by itself prove that case.

## 4. One predeclared bounded search design

The following design is recorded **before executing any search**. It is the sole finite search design authorized for this optional target.

- Procedure counts: every integer `k=2,...,8`.
- Penalties: exactly `M∈{0,1/10,1,4,16}`.
- Means: for every adjacent pair `g_j,g_(j+1)`, use `μ=g_j+t(g_(j+1)−g_j)` at `t∈{0,1/4,1/2,3/4}`, plus the last endpoint `g_k`. Duplicates are removed by exact equality. This gives exactly 735 specified fibers.
- Compute every conditional interval by exact rational enumeration of feasible one- and two-level laws. These are mathematical moment-polytope vertices, not frozen experimental populations.
- Check the explicit candidate `(q−+q+)/2` exactly against both the unrestricted radius and the singleton half-width. Preserve every result, including failures.
- If the candidate fails at a specified fiber, solve the coherent-center linear feasibility problem at `R_free` using a numerical LP only to locate a basis. Reconstruct a candidate vertex by rational elimination and accept a no-gap result only after exact verification of every equality, nonnegativity condition, and center inequality.
- If feasibility cannot be certified or a strict gap is suggested, retain the attempt and solve the corresponding minimum-radius LP at that same fiber. Claim a strict gap only with an exactly checked rational primal/dual or separating certificate. Otherwise label the fiber unresolved.
- Do not add `k`, penalty values, means, or a second search design in response to results. Do not infer a universal theorem from this finite grid.
- Stop on the first exactly certified strict gap, if one is found; otherwise complete the specified grid. Any remaining specified fibers are then explicitly unrun.

All source, commands, attempts, and results will be retained under `reviews/price/coherent_center_search/`. Any implementation correction or failed execution will be recorded rather than silently discarded.

## 5. Search and final disposition

The single predeclared search completed on its first execution. Every one of the **735 specified fibers** passed exact rational verification of the candidate law `(q−+q+)/2` at `R_free`. Every candidate also met the singleton half-width `(U_1−L_1)/2`. There were no candidate failures, unresolved cases, or strict gaps. The numerical LP fallback was never invoked. No further parameter choices, second search, or experiment was performed.

All 735 case certificates are retained, including every candidate's rational level masses, mean, conditional intervals, coordinate values, and achieved radius:

- [Search source](price/coherent_center_search/search.py)
- [Attempt 1 source snapshot](price/coherent_center_search/attempt1/source.py)
- [Predesign and source manifest](price/coherent_center_search/attempt1/manifest.json)
- [All 735 exact records](price/coherent_center_search/attempt1/records.jsonl)
- [Attempt 1 summary](price/coherent_center_search/attempt1/summary.json)

This is finite corroboration for the candidate, not a universal coherent-center theorem. It is also distinct from the original 54-fiber evidence, although the predeclared grid includes some of the same parameter values.

**Current disposition:** the `k=3` proper-moment midpoint result is proved, so the A1 prose warning has a local scope correction. For general `k`, this review found no counterexample but leaves universal coherent-center existence **unresolved pending an audited proof**.

The candidate and the precise remaining sufficient inequalities are:

`q−=(1−p)e_0+p e_k`, `p=(μ−1)/(k+M−1)`,

`q+` = the adjacent-level mixture of mean `μ`, `q_center=(q−+q+)/2`,

`B_r=E_(q+)f_r`,

`2U_r≤U_1+B_r`, and `2L_r≥2p+B_r−U_1`.

At the nodes `μ=g_j`, the lower inequality is explicitly

`2 min_(i≤j≤l) chord_(i,l) f_r(g_j)
 ≥ 2j/[(k−j+1)(k+M−1)] + f_r(j) − j/k`.

The minimum includes a single-level law when applicable. A pure-proof delegate proposed arguments toward both inequalities, with a claimed completion arriving at the stopping boundary. Those arguments are **unaudited in this review** and are preserved separately for the principal to assess. They do not change this review's unresolved universal disposition. The search and proof exploration were stopped at the principal's instruction.

The already-obtained proposed argument is saved as [proposed_proof_at_stop.md](price/coherent_lemma/proposed_proof_at_stop.md), explicitly marked **UNAUDITED**. Its presence is a record of the proof attempt, not an endorsement of the universal theorem.
