# F16 coherent recovery: independent upper-proof audit

**Reviewer:** ChatGPT (GPT-6 Astra Pro), agent `/root/f16_coherent_upper_audit`.  
**Date:** October 5, 2026.  
**Assigned scope:** §§1–5 and §8 of `v2/derivations/10_f16_coherent_recovery.md`.  
**Principal credited time:** zero.

## Disposition

**No exact mathematical defect was found in the assigned upper proof.** The one-turn slope lemma, tilted-law argument, terminal attachment, and extension from `M=0` to `M>=0` are valid under the stated assumptions. No additional substantive hypothesis is needed for those arguments.

The reduction from the two inequalities (1) to coherent conditional optimality is valid. The passage to the sharp global radius and the discrete maximizer rule in §8 is also valid **conditional on the lower inequality in (1)**. This report does not independently certify §§6–7; that lower proof was assigned to a separate reviewer. Accordingly this report alone is not an unconditional certificate of the whole proposed theorem.

The proposed changes below are explicit intermediate justifications and scope wording. None changes the displayed radius or proposed decoder.

## Reviewed sources and exposure

The target draft had SHA256 `6ba3eb020a6478c1b9b01522a578ad01c0eb975a93e4e321b50c0d0923759b5b` when hashed during this audit. The definitions source, `v2/derivations/09_c4_price_revision.md`, had SHA256 `e0af9845dddeacc5d7ebdf16f9d8a5584b31fb60e95343dfc80d91e95002fad7`. These identify the inspected draft and definitions, not later principal edits.

I read the target draft and C4 definitions. The full target read also exposed the proposed lower proof and its finite-evidence description; the C4 read exposed its existing finite-evidence statements. A collaboration inventory displayed completed-agent summaries, including the already-reported 735-fiber result and earlier proposed proof summaries. I did not open those search records or use their pass counts as proof. This is an independent derivation audit, not a blind audit.

A nested proof-only reviewer, `/root/f16_coherent_upper_audit/global_radius_check`, independently checked §§1–2 and §8 and agreed with the conclusions below. That reviewer made no file edits and reported no experiment or mathematical search. Its incidental exposure included the C4 §14 finite-evidence sentence and completed-agent summaries. Its signed findings are integrated here and attributed below.

I ran no numerical test, finite-fiber search, experiment, model evaluation, or external/literature search. Local operations were confined to locating and reading the requested files, checking for ancestor instructions, hashing the two sources, and writing this review. The initial local filename inventory used `rg --files`; it was not a search over mathematical instances. The first attempt to add this review was rejected by the patch parser for a missing added-line marker and made no file change; the corrected write followed. No root document, theorem draft, frozen file, or experimental artifact was edited.

## 1. Exact fiber reduction and conditional optimality

### Accepted: the canonical representation is exact

At unit old prices, vanishing adjacent-order differences force the difference of proper moments to depend only on subset size. Boolean inversion then makes the difference of world masses constant on each Hamming level. Conversely, such a level-constant difference makes all old order means change by the same amount, which is their average change. Thus the within-level contrasts plus the average old mean characterize the full numeric profile, not merely its average.

Within a level, subtracting the minimum retained contrast gives residues with minimum zero. Every compatible nonnegative world law therefore has exactly the form

    p_w = rho_w + z_(|w|)/binomial(k,|w|),   z_h>=0.

Normalization and the retained average impose precisely `sum z_h=R` and `sum g_h*z_h=B_rem`. For a nonempty fiber, `0<=R<=1`; if `R>0`, `mu=B_rem/R` lies in `[1,b]`. These facts justify all denominators, the endpoint-mixture weights, and residual scaling. If `R=0`, all `z_h` vanish and the source law is known.

### Accepted: the singleton extrema

For `h=0,...,k-2`, the adjacent slope of `f_1(h)=h/k` against `g_h` is

    (k-h)(k-h+1) / [k(k+1)].

These slopes decrease. The final slope is `2/[k(k+2M-1)]`, no larger than the preceding slope because `k+1 <= 3(k+2M-1)` for `k>=2,M>=0`. Hence the original singleton polygonal curve is concave. Its upper envelope is its adjacent-level interpolation; its lower envelope is the endpoint chord. Consequently

    L_1=p=(mu-1)/(b-1),   U_1=B_1.

The displayed `q^-` and `q^+` attain those extrema, including endpoints and the degenerate singleton-width case `k=2,M=0`.

### Accepted, conditional on both inequalities (1): the center and radius

The candidate belongs to the residual polytope by convexity. Since every proper `f_r` is zero at level zero and one at level `k`, its candidate value is `c_r=(p+B_r)/2`. Inequalities (1) give exactly

    U_r-c_r <= (U_1-p)/2,
    c_r-L_r <= (U_1-p)/2.

Thus the candidate attains that common tolerance. Their difference also gives `U_r-L_r<=U_1-p`, so a singleton is a coordinate of maximum width. The two singleton endpoints force the matching half-width lower bound for every unrestricted numerical decoder, and therefore for every law-valued decoder.

For an edit to a fixed procedure `a`, revised orders expose precisely prefixes `S` avoiding `a`. Every size `0,...,k-1` occurs, and at least one singleton occurs because `k>=2`. Different subsets of the same size may have different residue offsets, but those offsets cancel in candidate-minus-true errors. The maximum revised-order error is therefore exactly

    |epsilon| R max_(1<=r<=k-1) |E_q f_r-E_(q_c) f_r|.

For the matching lower bound, choose an order beginning `i,a` with `i!=a`; its edit term is `epsilon m_{i}` and its interval has width `|epsilon|R(U_1-p)`. This checks the lower bound for one fixed edited index, not just for a collection in which every index is edited. The same compatible candidate works for every separately applied single-price edit.

### Accepted: interpolation reduces the proof to nodes

At fixed mean, the upper and lower objective functions are the upper concave and lower convex polygonal envelopes of the finite points `(g_h,f_r(h))`. Their vertices occur among those points. Both envelopes are therefore affine between any consecutive `g` levels, even when one hull edge skips several levels. The same is true of `B_r`, `U_1`, and `p` on each such interval. Checking each signed slack in (1) at the endpoints proves the inequality throughout the interval. At `mu=g_0,g_k`, the residual polytope is a singleton, and the inequalities hold with equality. The coordinate `r=1` and the entire `k=2` case are immediate from the singleton extrema.

## 2. Generic one-turn slope envelope lemma (§3)

**Accepted.** Write `x_0=0`, and let adjacent slopes be `s_1,...,s_N`. Choose a peak index `m` such that

    s_1<=...<=s_m>=s_(m+1)>=...>=s_N.

For `i>=1`, put `a_i=y_i/x_i`. Each `a_i` is a weighted average of `s_1,...,s_i`, with positive weights `x_j-x_(j-1)`. For `i<m`, `s_(i+1)>=s_i>=a_i`, so `a_(i+1)>=a_i`. A last global maximizing index `t` of the secants therefore satisfies `t>=m`.

If `t<N`, maximality gives `s_(t+1)<=a_t`: otherwise adding that slope to the weighted average would make `a_(t+1)>a_t`. Thus a line of slope `a_t` from the origin to vertex `t`, followed by the original edges after `t`, has nonincreasing slopes. It is concave. The maximal-secant property places every earlier vertex at or below the initial line, so this construction majorizes the original polygonal curve.

Every concave majorant lies above the chord joining its values at the origin and vertex `t`, hence above the displayed initial chord. On each later edge, concavity and the required endpoint majorization put it above the original linear edge. This proves pointwise minimality. The cases `t=N`, a wholly concave curve, flat pieces, negative ordinates, and ties need no new argument. On an equally spaced grid, the second-difference sign pattern is exactly the same adjacent-slope condition.

**Wording:** say the secant maximum ranges over `i=1,...,N`, excluding the undefined quotient at the origin. This is a notation clarification, not a failure of the lemma as used.

## 3. Tilted interior upper inequality (§4)

**Accepted.** Let `x` be supported on `h=0,...,k-1` with `E_x g=g_j`. Then `y_h=x_h g_h/g_j` is nonnegative and sums to one. Since `g_h(k+1-h)=k+1`,

    E_y(k+1-h) = (k+1)/g_j = k+1-j.

So `E_y h=j`. Conversely, if `y` is a probability law with this mean, then `x_h=y_h(k+1-h)/(k+1-j)` sums to one and has `E_x g=g_j`. This proves the claimed bijection, including both normalization constraints. It also gives `E_x f_r=E_y H_r/(k+1-j)` exactly.

Using forward differences, direct subtraction first yields

    Delta^2 H_r(h)
      = [(k-h-1)binomial(h,r-2)-2binomial(h,r-1)]/binomial(k,r).

The identity `(r-1)binomial(h,r-1)=(h-r+2)binomial(h,r-2)` converts this to the draft's formula. After the initial zeros its sign has at most one positive-to-negative turn, as asserted. Since `H_r(0)=0`, §3 applies and its secant maximizer is exactly a maximizer of `C(h)/k`, over `1<=h<=k-1`.

Direct subtraction also gives the draft's formula for `Delta C(h)`. The term

    (k-h)binomial(h-1,n-1)

counts `n`-subsets with exactly one element in the second block of a partition of a `(k-1)`-element universe into block sizes `h-1` and `k-h`. It is at most `binomial(k-1,n)`. Subtracting the nonnegative second numerator term therefore establishes `Delta C(h)<=1`, including initial zero cases. Consequently `F(h)=k+1-h+C(h)` is nonincreasing. Also `P(h)<=1`, so `F(h)>=2C(h)`.

For `j<=h_*`, the envelope gives `E_y H_r<=j C(h_*)/k`; monotonicity gives `2C(h_*)<=F(h_*)<=F(j)`. Substitution gives `2E_x f_r<=t+a`. For `j>=h_*`, the envelope agrees with `H_r` at `j`, so `E_x f_r<=a`; the elementary inequality `a<=t` gives the same conclusion. This proves the interior-supported upper inequality without any finite verification assumption.

## 4. Terminal-level attachment and `M>=0` (§5)

**Accepted.** The adjacent interior slopes and their ratio follow from `binomial(h+1,r)-binomial(h,r)=binomial(h,r-1)` and the differences of `g`. Cross-multiplication gives precisely

    (r-1)(k+1)-(r+1)h-2

as the sign of the ratio minus one. Thus these slopes meet §3's hypothesis. At `M=0`, the terminal slope is `2r/[k(k-1)]`.

For `r<=k/2`, the last edge of the interior concave hull is either its initial chord reaching level `k-1`, or the original last interior edge. Their slopes are respectively

    2(k-r)/[k(k-1)],
    6r(k-r)/[k(k-1)(k+1)].

Both dominate the terminal slope. The first comparison is `k-r>=r`. The second is `3(k-r)>=k+1`, which follows from `r<=k/2,k>=2`. Appending the terminal segment gives a concave majorant of the full curve. Any full-curve concave majorant restricts to a majorant of the interior curve, so it must lie above the old interior hull. This proves that the new hull agrees with the interior hull on the interior domain; it is not just a concavity assertion. Section 4 supplies the desired bound there.

For `r>=k/2`, the nonzero successive ratio of `C` is the one in the draft. Its comparison with one reduces to `(r-1)(k+1)-rh>=0`. On its required range `h<=k-2`, this follows from `3r>=k+1`, itself implied by `r>=k/2,k>=2`. Initial zero values are harmless. Since

    f_r(h)/(g_h-1) = C(h)/k,

the maximum interior secant is `2(k-r)/[k(k-1)]<=1/(k-1)`. All interior points lie below the full endpoint chord, whose attaining endpoint mixture gives `U_r(g_j)=p` at `M=0`.

For `j<=k-2`, `2p<=t` follows from `(k-j+1)(k-1)>=3(k-1)>=2k`; here `r>=2` has already ensured `k>=3`. For `j=k-1`, `2p=1` and `a=(k-r)/k>=1/k`, so `t+a>=1`. These cases cover all proper `r>=2`, including their overlap.

Finally a vertex of the residual probability polytope uses at most two levels: on three or more positive coordinates the two equality constraints have a nonzero null direction, allowing a two-sided feasible perturbation. At a fixed interior mean, an interior-supported vertex stays feasible and unchanged as `M` grows. A pair involving the terminal level has the displayed expectation, whose derivative in `M` is

    -[1-f_r(h)](g_j-g_h)/(k+M-g_h)^2 <= 0.

The feasible pair indices remain the same for all `M>=0`. Thus the maximum for `M>0` is no larger than its `M=0` counterpart. The right side `t+a` is independent of `M`, proving the full upper inequality.

## 5. Global radius and discrete maximization (§8)

**Accepted, conditional on both inequalities (1).** The nested reviewer independently confirmed the following derivation and boundary cases.

Let `delta_r(mu)=U_r(mu)-L_r(mu)`. The conditional width in the original world-law fiber is `R delta_r(mu)`, and the center inequalities imply `delta_r(mu)<=delta_1(mu)` for every `r`.

For the global supremum, it is useful to state explicitly that `0<=R<=1` and every `mu` in `[1,b]` is realized by a fiber with `rho=0,R=1`. Thus the bound from conditional widths is attained in the zero-residue family; no unrealized conditional summary is used. Since `delta_1(mu)=U_1(mu)-(mu-1)/(b-1)` is piecewise affine, its maximum occurs at a `g` node. Endpoints give zero and the interior expression is exactly

    D_1 = max_(1<=j<=k-1)
            [j/k-j/((k+1-j)(k+M-1))].

The global maximum coordinate diameter is therefore `D_1`. A uniform law on Hamming level `j` and the endpoint mixture with the same mean are exchangeable, have the same complete old profile, and attain its singleton gap. This proves the sharp global radius `|epsilon|D_1/2` once the conditional theorem is available. The special case `k=2,M=0` has zero diameter and is included.

With `s=k+1-j` and `C=k+M-1>0`, direct subtraction yields

    F(s+1)-F(s) = -1/k+(k+1)/(C s(s+1)).

This difference strictly decreases with `s`. Before the first integer with `C s(s+1)>=k(k+1)` it is positive; at that integer it is nonpositive. The draft's smallest-`s` rule gives a maximum. Equality gives exactly the adjacent tie when `s+1` is still in `[2,k]`. There are no additional nonadjacent ties. The one-element domain for `k=2` is covered. The fallback to `s=k` is harmless but unreachable under the assumptions, because the predicate holds at `s=k` whenever `C>=1`. Binary search is valid for this monotone predicate in the stated exact-arithmetic model. No bit-complexity or measured-speed claim follows.

## Findings requiring disposition

### Exact defects

None found in the assigned upper proof, reduction, or conditional global calculation.

### Unresolved proof obligations

The lower inequality in (1), proved in the draft's §§6–7, remains outside this review's independent certification. No further upper-half lemma is missing.

### Optional wording and explicitness improvements

1. Specify `i=1,...,N` for the §3 secant maximum.
2. Put “For `R>0`” before the §2 display containing `B_rem/R`.
3. At the conditional-to-global step, explicitly mention `0<=R<=1` and realization of every residual mean with `rho=0,R=1`.
4. Say “uniform law on Hamming level `j`” rather than “pure `j`-level law” if ambiguity with a single Boolean-world point mass is possible.
5. If §1 is intended to stand alone under the C4 model's strictly positive revised attempt prices, say `1+epsilon>0`. The algebraic recovery identity itself permits any real `epsilon` when the stipulated order and stopping rule are retained, but that would be a broader price convention.
6. Interpret “all separately applied single-price edits” as one candidate law furnishing each edit's `|epsilon|`-scaled optimum. A single unweighted supremum over an unbounded set of edit sizes is not a finite-radius claim. For a collection with `E=sup |epsilon|<infinity`, the common optimal radius is `E R(U_1-p)/2` conditionally. This is a quantifier clarification, not a counterexample to the per-edit result.

**Signed:** ChatGPT (GPT-6 Astra Pro), `/root/f16_coherent_upper_audit`, October 5, 2026.  
**Signed nested proof-only check:** ChatGPT (GPT-6 Astra Pro), `/root/f16_coherent_upper_audit/global_radius_check`, §§1–2 and §8.  
**Principal clock credit:** zero.

