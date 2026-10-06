# F16 bounded clarification: signed attempt prices and the A1 specialization

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, delegated separate reviewer. Date: 2026-10-05. This is a proof-only follow-up to [price_review.md](price_review.md), at the principal's request. It supplies **zero principal clock credit**, changes no theorem or control implementation, and executes no experiment. The assumption weakening below is an optional algebraic observation, not a new priority claim. The reading-provenance qualification in [price_initial.md](price_initial.md) continues to apply.

## 1. Exact statement of the optional weakening

For the exact rank calculations, replace the requirement that every attempt price be strictly positive by the requirement that every attempt-price coordinate be **nonzero**. The prices may have different signs; their sum may be zero or negative; and some lower elementary symmetric polynomials may vanish. Keep the other hypotheses: `k≥2`, a fixed joint Boolean outcome law, the full probability simplex or the specified full-support affine fiber, all permitted full orders with the original stopping rule, fixed known query coefficients, and linear summaries with arbitrary decoding.

Under that replacement, the one-profile ranks, T1's two-profile ranks, the proportional-family rank classification, and T3's ranks remain correct. With the original nonnegative penalties, “some penalty is positive” remains the correct top-moment condition. If penalties were separately extended to arbitrary real values, that condition would become “some penalty is nonzero.” A negative or zero **sum of attempt prices** does not change any of these statements.

The pathwise `|ε|` regret bound needs no sign or nonzero restriction on attempt prices at all. It instead needs the same outcome coupling, stopping protocol, policy family, and law source at the two price profiles. The proof appears below.

## 2. Complete one-profile kernel argument without positivity

Let `K={1,...,k}`, and let `v_A` be a moment direction, with `v_∅=0`. A swap of `i,j` after prefix `A` gives the directional difference

`(c_i−c_j)v_A+c_j v_(A∪{i})−c_i v_(A∪{j})`.                       (1)

All such swaps occur among the full orders, and adjacent swaps connect all orders. Thus a direction is in the within-profile kernel exactly when (1) vanishes for every admissible `A,i,j`. The terminal term cancels from (1), so `v_K` remains free at this stage.

For `A=∅`, equation (1) says `c_jv_i=c_iv_j`. Since all `c_i≠0`, this gives `v_i=t_1c_i` for one scalar `t_1`; its sign is unrestricted.

Suppose the formula has been established at sizes below `r`. For a size-r subset `B`, subtract the already determined terms:

`u_B=v_B−Σ_(ℓ=1)^(r−1) t_ℓ e_ℓ(c_B)`.

The elementary-symmetric recurrence

`e_ℓ(c_(A∪{i}))=e_ℓ(c_A)+c_i e_(ℓ−1)(c_A)`

shows that these subtracted terms themselves satisfy (1). Therefore, for `|A|=r−1`, the remaining equation is

`c_j u_(A∪{i})=c_i u_(A∪{j})`.

Dividing by the nonzero product `c_i c_j ∏_(a∈A)c_a` gives

`u_(A∪{i}) / ∏_(a∈A∪{i})c_a = u_(A∪{j}) / ∏_(a∈A∪{j})c_a`.

The graph of size-r subsets connected by replacing one element is connected. Every normalized residual is consequently the same scalar `t_r`, whether its denominator is positive or negative. Since `e_r(c_B)=∏_(i∈B)c_i` when `|B|=r`, induction proves

`v_B=Σ_(r=1)^|B| t_r e_r(c_B)`                                  (2)

for every proper nonempty subset `B`. Conversely, substitution of the same recurrence verifies every swap equation. Each `t_r` supplies one independent direction: at size `r` its new coefficient is a nonzero product. The proper kernel therefore has dimension `k−1`; adding `v_K` gives dimension `k`.

On the sum-zero probability tangent, of dimension `n=2^k−1`, the within-profile rank is `n−k`.

For a direction (2), the common numeric value of every order is

`S_c(t)+M v_K`, with `S_c(t)=Σ_(r=1)^(k−1) e_(r+1)(c_K)t_r`.       (3)

To see this identity without using signs, fix `r`. Each monomial consisting of `r+1` distinct prices appears exactly once in the ordered prefix-cost sum, when its last element is appended. This is a polynomial identity, independent of the signs of those monomials.

The required nonvanishing argument is **not** `e_2(c)>0`, which need not survive the weakening. Instead, the coefficient of `t_(k−1)` in (3) is

`e_k(c_K)=∏_(i=1)^k c_i≠0`.

Thus (3) imposes one nonzero linear condition for every value of `M`, including zero. The numeric kernel has dimension `k−1`, and the numeric rank remains `n−k+1=2^k−k`.

This explicitly covers cancellation cases. For `c=(1,−1)`, the sum is zero but `e_2=−1`. For `c=(1,1,−1/2)`, `e_2=0` but `e_3=−1/2`. For an all-negative vector the sum is negative and the same final coefficient remains nonzero. No sum-of-prices sign assumption is used.

## 3. Nonproportional and proportional families with mixed signs

### Nonproportional profiles

There is a direct proof that avoids even dividing by coordinates of the second profile. Let `c` have all coordinates nonzero, and let `d` be nonproportional to `c`. There are indices `i,j` with

`D_ij=c_i d_j−c_j d_i≠0`.

Take a direction in the within-profile kernels of both profiles. Write its proper coordinates in the `c` representation (2). Inductively suppose `t_1,...,t_(r−1)` vanish. Choose any `(r−1)`-subset `A` avoiding `i,j`, possible because `r≤k−1`. Then `v_A=0`, and the `d` swap equation becomes

`d_jv_(A∪{i})−d_iv_(A∪{j})
 = t_r (∏_(a∈A)c_a)(d_jc_i−d_ic_j)=0`.

Both displayed factors multiplying `t_r` are nonzero, so `t_r=0`. This proves the induction through `r=k−1`. All proper directions vanish, leaving only `v_K`.

In particular, the argument handles arbitrary mixed-sign **nonzero** profiles. It also shows a limited further fact: one all-nonzero profile and a nonproportional second profile suffice even if the second has zero entries. That observation does not rescue a general theorem allowing zeros in every profile; the zero-price countermodel in the final review has no all-nonzero profile.

The remaining numeric values are `M_a v_K`. Hence, for a family containing the stated nonproportional pair:

| Consumer | Rank with the original nonnegative penalties |
|---|---:|
| Within-profile differences | `n−1` |
| All numeric means | `n` if any `M_a>0`, otherwise `n−1` |
| All differences, including across profiles | `n` if the penalties are not all equal, otherwise `n−1` |

This calculation uses neither the signs nor the sums of attempt prices.

### Proportional profiles

When all attempt-price vectors have nonzero entries and are proportional, write `c^a=λ_a c` with `λ_a≠0`; the scalars may now be negative. Formula (2) represents the same proper kernel, because the coefficients at profile `a` can be written `t_r/λ_a^r`. Its common value is

`Σ_r (t_r/λ_a^r)e_(r+1)(λ_a c)+M_a v_K
 = λ_a S_c(t)+M_a v_K`.

The map `(t,v_K)↦(S_c(t),v_K)` is onto `R²`, using the nonzero `e_k(c)` coefficient. Therefore the original matrix-rank classification remains unchanged: let `h` be the rank of rows `(λ_a,M_a)`, and let `h_Δ` be the rank of their differences from a reference row. The numeric, within, and cross ranks are respectively

`n−k+h`, `n−k`, and `n−k+h_Δ`.

Negative scale factors do not require an exception. They must simply be retained with their actual signs in this two-column matrix.

## 4. Repair and known-moment fibers

For T2, the old profile's kernel is still (2)–(3). A one-coordinate edit obeys the exact identity

`C'_π−C_π=ε m_A`,

where `A` is the prefix preceding the edited procedure `j`. Choose nested prefixes `A_r⊆K\{j}` of sizes `r=1,...,k−1`. On the old kernel, the new query rows form a triangular system with diagonal

`ε∏_(i∈A_r)c_i`.

Each entry is nonzero when `ε≠0` and the old prices are all nonzero; its sign is irrelevant. With `M≠0`, the old numeric profile plus these `k−1` queries recovers the entire law, and the old rank deficit proves necessity for added linear measurements. Under the original nonnegative-penalty contract, this is the original `M>0` case.

The triangular proof actually allows the **new edited price to equal zero**. It divides by `ε` and products of old prices preceding `j`, not by the new `c_j+ε`. Thus the optional signed-price analysis does not introduce an unnecessary nonzero-endpoint condition for this particular repair construction. This does not assert that an isolated zero-price profile has the original one-profile rank.

For T3, known moments through size `s` force `t_1=...=t_s=0`, by the same nonzero-product induction. If `s≤k−2`, the restricted functional in (3) still contains `t_(k−1)e_k(c)`, so it is nonzero. The advertised single-profile ranks follow. At `s=k−1`, only `M v_K` remains. The nonproportional-pair proof above can start at `r=s+1` and gives the advertised combined ranks as well.

None of this weakens the **probability** conditions. World masses remain nonnegative and sum to one. Full support is still needed to identify the stated affine tangent of a fixed-moment fiber and realize opposite small perturbations. Negative attempt prices do not justify signed probability laws or enlarge the admissible source.

## 5. Regret and coherence: what must stay fixed

For one fixed world and one fixed order, the revised-minus-old realized cost is

`L'_π(F)−L_π(F)=ε 1{all procedures preceding j fail}`.             (4)

This is true for positive, zero, or negative attempt prices. Put `ℓ=min(0,ε)` and `u=max(0,ε)`. Equation (4) gives `L_π+ℓ≤L'_π≤L_π+u` pointwise.

Expectations and fixed-level upper-tail CVaR are monotone and translation equivariant for these finite-valued losses, including signed losses. Taking the worst such objective over the **same nonempty law source** preserves the inequalities. Thus every fixed order's objective satisfies

`J_π+ℓ≤J'_π≤J_π+u`.

If `π_old` minimizes the old objective and `π_new` minimizes the new one over the same finite policy family, then

`J'_(π_old)−J'_(π_new)
 ≤ J_(π_old)+u−J_(π_new)−ℓ
 ≤ u−ℓ=|ε|`.

An old `η`-optimal policy gives `η+|ε|`. Zero sums of prices, negative realized costs, or an edited price crossing zero create no exception to this argument.

The required coherence conditions are instead structural. The procedure outcomes and the event of reaching `j` must have the same meaning at both profiles; the terminal penalty is held fixed; and a fixed policy must execute the same stopping protocol. In particular, the model still mandates stopping at the first success and attempting each listed procedure at most once. Allowing an agent to continue after success to collect a negative-price rebate, or to repeat attempts, changes the policy model and does not inherit (4) automatically.

Nonnegative probability masses, a nonempty admitted source, and correct profile/population metadata remain necessary. A negative coefficient in a cost equality does not itself impair probability-law coherence: the intersection of the simplex with fixed linear observation equalities is still a compact convex set. Separate coordinate midpoints nevertheless need not come from one law, just as in the positive-price example already reviewed. Feasibility alone still cannot establish correct old-profile or unchanged-population binding.

Finally, this weakening concerns the **rank and repair algebra**, not an automatic extension of A1–A3 to arbitrary old mixed-sign prices. Their level reduction and canonical-chain offsets use equal old attempt prices. Under unequal prices, same-size moment differences need not be determined by the old summary. The A1 derivation below therefore retains its stated old unit-price assumption and `M>0`.

## 6. A1 derived directly from its stated kernel

Let `k=3`, old prices be `(1,1,1)`, and `M>0`. For two laws `p,q` with the same complete old numeric profile, the stated kernel gives

`v_i=a`, `v_ij=2a+b`, `v_123=−(3a+b)/M`.

Boolean inversion gives the per-world probability differences `w_h` for a world containing exactly `h` failures:

`M w_0=(3M+3)a+(3M+1)b`,

`M w_1=−(3M+3)a−(2M+1)b`,

`M w_2=(2M+3)a+(M+1)b`,

`M w_3=−3a−b`.

The difference is constant within each level. This does not require `p` and `q` themselves to be exchangeable. Let `U_h` and `V_h` be their total probability masses at level `h`; then `U_h−V_h=binom(3,h)w_h`. The difference of any specified r-prefix moment is

`Σ_(h=0)^3 f_r(h)(U_h−V_h)`.

The relevant values are:

| `h` | Mean old order cost `g_h` | Singleton reach `f_1(h)` | Pair reach `f_2(h)` |
|---:|---:|---:|---:|
| 0 | `1` | `0` | `0` |
| 1 | `4/3` | `1/3` | `0` |
| 2 | `2` | `2/3` | `1/3` |
| 3 | `3+M` | `1` | `1` |

The old mean averaged over all orders is `Σ_h g_h U_h`, and similarly for `V`. Equal old profiles therefore imply `Σ_h g_h U_h=Σ_h g_h V_h`. Since both level distributions also have total mass one, any affine function of `g_h` has equal expectation under them.

Choose the following affine function:

`ℓ_h=(g_h−1)/(M+2)`.

Subtracting it does not change a target difference between compatible laws. For singleton reach the four residuals are

`f_1−ℓ = (0, (M+1)/[3(M+2)], (2M+1)/[3(M+2)], 0)`.

They all lie in the interval `[0,A]`, where

`A=(2M+1)/[3(M+2)]`.

Two probability distributions can differ in their expectation of a function with that range by at most `A`. Therefore every compatible singleton-moment difference has absolute value at most `A`.

For pair reach the residuals are

`f_2−ℓ = (0, −1/[3(M+2)], (M−1)/[3(M+2)], 0)`.

Their range has width

`W_2=max(1,M)/[3(M+2)]≤A`.

This is enough to bound every pair-moment difference by `A`; it does not purport to be the sharp pair-only diameter in every parameter range. The empty prefix has zero uncertainty. Consequently, every revised mean after a one-coordinate edit has width at most `|ε|A` on each old-summary fiber.

Each such fiber is compact, so all these coordinate intervals attain their endpoints. Predicting each interval's midpoint gives an unconstrained real prediction vector with worst absolute error at most `|ε|A/2`.

For the matching lower bound, take `p` uniform on the three worlds with exactly two failures. Let `q` put mass `(M+1)/(M+2)` on all-success and `1/(M+2)` on all-failure. Every old order has mean 2 under both laws. Their singleton reach probabilities are `2/3` and `1/(M+2)`, whose difference is exactly `A`. An order with the edited procedure second therefore has revised means separated by `|ε|A`. The summary is identical, so any one prediction incurs error at least half that separation on one of the two laws.

The upper and lower bounds agree:

`R_A1 = |ε|(2M+1)/[6(M+2)]`.

This argument obtains the exact global radius directly from the stated kernel, a simple affine residual bound, and an attaining pair. It does not need the existing weighted-median calculation or the exact piecewise pair-moment formula.

## 7. Exact specialization of the reported F15 parameters

At `M=4`, `A=1/2`, so `R_A1=|ε|/4`. Inserting the reported `|ε|=1/40` gives

`R_A1=1/160=0.00625`.

For an explicit positive-edit witness, use `ε=1/40` and an order with the edited procedure second. The two laws above have revised means

`2+(1/40)(2/3)=121/60`,

`2+(1/40)(1/6)=481/240`.

Their gap is `1/80`, their midpoint is `193/96`, and their distances from that midpoint are both `1/160`. A negative edit of the same magnitude gives the same absolute radius.

This is the exact **global worst-fiber A1 radius** under its stated summary and population model. It is not a claim that the actual F15 population or its observed summary realizes the extremal fiber, nor an empirical error measurement. The generic midpoint bound remains `1/80`, and the unchanged old-optimum regret bound remains `1/40`; their separate operational preconditions still apply.

The subsequent [coherent-center review](price_coherent_center_review.md) proves that this k=3 A1 radius is also attainable by one compatible law realizing all proper-moment midpoints. It does not require the terminal moment to equal the midpoint of its own interval, and does not establish a universal coherent-center theorem for arbitrary k.
