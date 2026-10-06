# F16 price-family reconstruction: initial derivation

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, delegated separate reviewer. Date: 2026-10-05. Baseline supplied by principal: `6ef27f20e3ac0920953a27dd84d6c91a021ba58f`. This is separate review effort and contributes **zero principal D60 time**. No ledger, clock, frozen-stage, neural, ND02, F17, or Gate C/D work is performed here.

## Reading provenance and limits of independence

This reconstruction was written before reading the proof sections or verification program in full. It is **not a completely blind reconstruction**. A heading search inadvertently exposed the first lines of proof paragraphs at `v2/derivations/09_c4_price_revision.md:75,259,443`. A statement excerpt also exposed lines 338–343 (the k=3 kernel form, exchangeability observation, and first inversion equation). The finite-family excerpt included the coordinate commentary at lines 114–122. Definitions and statements read were lines 1–33, 65–74, 102–124, 139–143, 181–187, 207–222, 234–258, 321–343, 407–442, and 626–650. The last two ranges include some explanatory derivation already embedded in the statement setup. No `06_case_studies.md` argument or verification code has yet been read. The general induction, rank accounting, witnesses, and minimax derivation below were reconstructed directly from the model, with that limited exposure acknowledged.

## 1. Exact model and tangent space

Write `K={1,...,k}`. A world is a failed-procedure subset `F⊆K`; `p_F≥0` and `Σ_F p_F=1`. Define `m_A=Σ_{F⊇A}p_F`, including `m_∅=1`. The cost of a complete order `π` is

`C_π(c,M)=Σ_{r=0}^{k−1} c_{π_(r+1)}m_{P_r}+M m_K`,

where `P_r` is its first `r` procedures. The reset interpretation must make one joint outcome vector valid for all allowed orders on the same request. In particular, executing a preceding procedure cannot change the potential outcome or price of a later one.

The world-law tangent is `{δp:Σδp_F=0}`, of dimension `n=2^k−1`. Boolean inversion gives

`δp_F=Σ_{A⊇F}(−1)^(|A|−|F|)v_A`,

where `v_A=δm_A` and `v_∅=0`. Consequently all nonempty moment directions are independent coordinates. On the full simplex, a sufficiently small positive and negative multiple of every tangent direction is feasible around the uniform law.

For a **linear** summary `T(p)` and a linear target family `L(p)`, arbitrary decoding does not improve the rank lower bound: if `Tv=0`, the two nearby laws `p±tv` have the same summary, so exact decoding forces `Lv=0`. Thus `ker T⊆ker L`, and the minimum summary rank is the rank of `L` restricted to the sum-zero tangent. Constants, including the first attempt price, do not count. A minimum-rank exact summary has precisely the target row space on that tangent.

## 2. One-profile order-difference kernel

Consider an adjacent swap of `i,j` after a prefix `A` disjoint from them. All later terms cancel. Its directional cost difference is

`(c_i−c_j)v_A+c_j v_(A∪{i})−c_i v_(A∪{j})`.

Every such prefix and pair occurs in an allowed order. Adjacent swaps connect all permutations, so their vanishing is necessary and sufficient for all within-profile differences to vanish.

Assume first that every `c_i≠0`. For `A=∅`, the equations say `v_i=t_1 c_i`. Inductively, after subtracting the lower-degree terms, the size-r residuals satisfy

`c_j u_(A∪{i})=c_i u_(A∪{j})` for `|A|=r−1`.

Divide by the product of the prices in each subset. The quotients agree across adjacent vertices of the connected graph of r-subsets that differ by one element. There is therefore one new scalar `t_r`, and

`v_A=Σ_(r=1)^|A| t_r e_r(c_A)` for every proper nonempty `A`.

Conversely this formula solves every swap equation, since `e_r(c_(A∪{i}))=e_r(c_A)+c_i e_(r−1)(c_A)`. The parameters are independent: at each size `r`, the new diagonal coefficient is the nonzero product of its `r` prices. The top moment `z=v_K` is unrestricted by order differences. The kernel dimension is thus `k`, and the within-profile rank is `n−k`.

For a direction in this kernel, every order has the same directional numeric cost

`S_c(t)+Mz`, where `S_c(t)=Σ_(r=1)^(k−1) e_(r+1)(c_K)t_r`.

The identity follows because every `(r+1)`-subset is counted exactly once, when its last element is attempted. The functional `S_c` is nonzero: its final coefficient is `e_k(c_K)=∏c_i≠0`. One numeric profile imposes one additional constraint, even if `M=0`. Its numeric rank is `n−k+1=2^k−k`.

## 3. Two profiles and a finite price family

Let `c,d` be nonproportional and have no zero coordinate. A common within-profile kernel direction has `t_1c_i=u_1d_i`, forcing both scalar coefficients to vanish. Inductively, at size `r`, it has

`v_A=t_r∏_(i∈A)c_i=u_r∏_(i∈A)d_i`.

The two vectors of r-subset products cannot be proportional for `1≤r≤k−1`: taking two subsets with a common `(r−1)`-subset would force `c_i/d_i=c_j/d_j` for every pair. All proper directions therefore vanish. Only `z=v_K` remains.

This gives the following common ranks:

| Consumer | Rank |
|---|---:|
| All within-profile order differences | `n−1` |
| All numeric means | `n` if any penalty is nonzero, otherwise `n−1` |
| All differences, including across profiles | `n` if penalties are not all equal, otherwise `n−1` |

Under the source's nonnegative-penalty assumption, “nonzero” is exactly “positive.” The same conclusions hold for any finite family containing such a pair.

If all price vectors are proportional, write `c^a=λ_a c`. The within-profile kernel is the same, and profile `a` has common value `λ_a S_c(t)+M_a z`. Since `(t,z)↦(S_c(t),z)` is onto `R²`, let `h=rank{(λ_a,M_a)}` and `h_Δ=rank{(λ_a−λ_0,M_a−M_0)}`. The ranks are respectively `n−k+h`, `n−k`, and `n−k+h_Δ` for numeric, within, and all differences. This distinguishes an absolute numeric consumer from a difference consumer.

**Positivity is sufficient but stronger than the exact algebra requires:** coordinatewise nonzero prices suffice for these results. The sign restrictions still give the stated physical cost interpretation.

## 4. One-coordinate repair and lower-order side information

Take an old minimum-rank numeric summary with `M>0`. Its null directions have arbitrary `t_1,...,t_(k−1)` and `z=−S_c(t)/M`. Change only `c_j` by nonzero `ε`, retaining nonzero prices. The new cost for an order differs by `ε m_A`, where `A` precedes `j`. Choose nested subsets `A_r⊆K\{j}` of sizes `r=1,...,k−1` and an actual order with exactly `A_r` before `j`. On the old kernel, these new rows are

`εv_(A_r)=εΣ_(ℓ=1)^r t_ℓ e_ℓ(c_(A_r))`.

This is triangular with nonzero diagonal `ε∏_(i∈A_r)c_i`. The selected `k−1` real order means identify all old null directions and hence the whole law. Necessity follows from the old rank deficit `k−1`; the statement needs the old summary to be minimum-rank. This also explains why placing the edited procedure first supplies no repair information.

If moments through size `s` are fixed and the fiber contains a full-support law, its tangent is exactly `v_A=0` for `|A|≤s`, of dimension `N_s=Σ_(r=s+1)^k binom(k,r)`. The kernel induction forces `t_1=...=t_s=0`. The within rank is `N_s−k+s`. For `s≤k−2`, a numeric profile adds one because the restricted `S_c` still has nonzero final coefficient, giving `N_s−k+s+1`. For `s=k−1`, the only unknown direction is the top moment, observable exactly when `M≠0`. A nonproportional pair eliminates all remaining proper directions, giving the two-profile formulas with `n` replaced by `N_s`.

## 5. Minimal countermodels when assumptions are removed

1. **Zero prices break the two-profile theorem at k=3.** Let `c=(1,0,0)`, `d=(0,1,0)`, and `M=N=1`. The first profile's means involve only `1,m_2,m_3,m_23,m_123`; the second involves only `1,m_1,m_3,m_13,m_123`. Neither sees `m_12`. Let `p` put half its mass on `∅` and half on `{1,2}`, and let `q` put half on `{1}` and half on `{2}`. Both profiles agree for every order, but `m_12(p)=1/2` and `m_12(q)=0`. Combined numeric rank is 6, not 7. The failure is genuinely about allowing zeros; merely allowing negative nonzero prices does not destroy the rank proof.

2. **A restricted law family can remove the repair need.** For `k=2`, restrict to `p=(1−q)δ_∅+qδ_{12}`, use `c=(1,1), M=1`, and allow both orders. Every old mean is `1+2q`, which already recovers the law. A one-coordinate revision needs zero additional observations, contrary to the full-simplex lower bound `k−1=1` if misapplied to this family.

3. **A boundary fiber can have smaller dimension.** For `k=2,s=1`, fix `m_1=m_2=0`. Only the all-success law is feasible, so the actual incremental numeric rank is zero, even with positive `M`; blindly using the nominal `N_s=1` would give one. The source's full-support condition excludes this case.

4. **All-order coverage is essential.** For `k=3`, if the only revised orders requested put the edited procedure last, every revised-minus-old mean uses the single moment `m_(K\{j})`. One new query suffices for those requested answers. The two-query conclusion pertains to all new orders or full-law recovery, not this narrower consumer.

5. **Positive terminal penalty is essential to full-law recovery.** If every available penalty is zero, `m_K` is absent from all cost expressions. Even arbitrarily many nonproportional attempt-price profiles cannot identify this direction on the full simplex.

6. **One common law is essential.** If preceding executions alter later success outcomes, `m_A` need not mean the same event across orders. For example, procedure 2 may always fail when first but always succeed after procedure 1 fails. Treating its first-position marginal as the conditional behavior after procedure 1 gives the wrong order cost. No rank computation on the stated Boolean-law simplex establishes conclusions for that model.

7. **Linear summary restriction is essential.** On unrestricted real encodings, an injective nonregular scalar code of the law defeats a dimension count. The source expressly excludes such encodings. The nonlinear decoder allowed here does not have that effect because its input summary remains linear.

## 6. Approximation reconstructed from level geometry

Take old prices all one and `M≥0`. The kernel formula makes every proper moment difference depend only on subset size. Boolean inversion then makes every world-probability difference constant on a Hamming-weight level, including the top coordinate. Thus differences within an old numeric-summary fiber are exchangeable, even though either underlying law need not be exchangeable.

For an exchangeable law, let `x_h` be its total mass on worlds with `h` failures. A specified r-subset fails with probability `Σ_h f_r(h)x_h`, where `f_r(h)=binom(h,r)/binom(k,r)`. The common old mean is `Σ_h g_hx_h`, with

`g_h=Σ_(r=0)^h binom(h,r)/binom(k,r)=(k+1)/(k−h+1)` for `h<k`, and `g_k=k+M`.

Symmetrizing both members of any indistinguishable pair preserves their difference and feasibility. Hence the global diameter of an r-prefix probability reduces exactly to two distributions `x,y` on `{0,...,k}` with equal `g` expectation. The linear program on `(x,y)` has three equalities: their two normalizations and equality of `g` means. A nonzero maximizing extreme point uses at most three positive entries, with one distribution supported at a middle `g_j` and the other on endpoints `g_i,g_ℓ`. Since `g` is strictly increasing, its diameter is

`D_r=max_(i<j<ℓ) | f_r(j)−[(g_ℓ−g_j)f_r(i)+(g_j−g_i)f_r(ℓ)]/(g_ℓ−g_i) |`.

For each observed old summary, an arbitrary real prediction vector can use the midpoint of each target coordinate's feasible interval. Its worst `ℓ∞` error is half the largest coordinate diameter; every decoder has at least that much error on an endpoint pair. A single price edit gives `C'_π=C_π+εm_A`, so the global minimum uniform error is `(|ε|/2)max_r D_r`. The interchange of the finite maximum over prefixes and the supremum over fibers is valid. This is a global worst-fiber radius, not necessarily the radius of the fiber actually observed, and it does not require one coherent law to realize all predictions.

### k=3 closed form and attaining pair

Here `g=(1,4/3,2,3+M)`, `f_1=(0,1/3,2/3,1)`, and `f_2=(0,0,1/3,1)`. The four triple residual magnitudes for `r=1` are

`1/9, (M+1)/[3(M+2)], (2M+1)/[3(M+2)], (3M+1)/[3(3M+5)]`.

For `r=2` they are

`1/9, 1/[3(M+2)], |M−1|/[3(M+2)], |3M−1|/[3(3M+5)]`.

For `M≥0`, the largest of all eight is `(2M+1)/[3(M+2)]`. Thus the proposed A1 error is `|ε|(2M+1)/[6(M+2)]`.

An extremal pair is: `p` uniform on the three worlds with exactly two failures; `q` with masses `(M+1)/(M+2)` on the all-success world and `1/(M+2)` on the all-failure world. Both give old mean exactly 2 for every order. Their singleton failure probabilities differ by `(2M+1)/[3(M+2)]`. At `M=4`, this difference is `1/2`, producing unavoidable error `|ε|/4` for an order placing the edited procedure after a singleton prefix.

### Coherence and population assumptions

Coordinatewise interval midpoints minimize unconstrained vector error. In three or more effective moment coordinates, their simultaneous feasibility is a separate question: the general simplex `{x≥0:Σx_i=1}` in `R³` has coordinate widths 1, unconstrained radius `1/2`, and radius `2/3` if the center must be in that simplex. This generic example is not yet a counterexample inside the specified price model. A consumer asking for a reusable joint law needs that additional analysis.

The exact old equal-price summary determines `m_S−m_(P_r)` whenever `|S|=r`, because that linear difference vanishes on its kernel. For a fixed canonical chain, the observed initial-failure count `J` satisfies `1{J≥r}=1{all P_r fail}`. With i.i.d. requests from the same population, add these exact offsets to the empirical tail probabilities. Every error at size `r` is the same empirical-tail error. A uniform empirical-distribution bound therefore controls every proper moment, and multiplying by `|ε|` controls every revised mean. This argument requires neither exchangeability of the population nor independence among procedures within one request.

The statistical step does require the exact old summary for the same population, a fixed observation scheme, independent draws from that population, and an appropriate fixed-sample concentration statement. An old summary from another population gives biased offsets; a noisy old summary requires a separate error term. Estimates formed by adding offsets can be outside the feasible joint-law polytope. Their validity as approximate numeric answers does not itself establish a coherent decoded law or an unconditional deterministic proof.

## Initial disposition

The reconstructed exact ranks, minimal repair count, side-information ranks, k=3 error, and general equal-price diameter formula agree with the statements read. Their mathematical ingredients are finite-dimensional linear algebra, Boolean moment inversion, convex geometry, and an established empirical-distribution inequality. The claimed application contribution can reasonably be the explicit kernel/rank calculation, its price-revision interpretation, and the exact residual approximation calculation for this consumer. It is not a new information theory or a result for arbitrary reset/search models. Full proof/code comparison and any model-specific coherence witness remain for `price_review.md`.
