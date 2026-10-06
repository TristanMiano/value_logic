# F16 coherent-recovery extension: separate lower-proof audit

**Reviewer:** ChatGPT (GPT-6 Astra Pro), separate proof-audit instance
`/root/f16_coherent_lower_audit`.

**Date:** October 5, 2026. **Principal clock credit:** zero.

**Artifact audited:** `v2/derivations/10_f16_coherent_recovery.md`, the draft headed
“F16 optional extension: a coherent optimal decoder at equal old prices.”
Assigned scope: §§1–2, §§6–7, and §9. The upper inequality in §§3–5 is under a
different review; this report does not certify that part by implication.

## Disposition

**Pass within the assigned scope.** I found no false inequality, missing
lower-proof boundary case, or invalid interpolation step. In particular,
§§6–7 establish the proposed lower inequality for every integer
`k>=2`, `1<=r<=k-1`, every interior node, and every `M>=0`, under the stated
exact full-law-fiber model. The candidate reduction and the displayed `k=4`
witness are correct. The universal coherent-decoder theorem additionally
requires the upper inequality to pass its separate audit.

There is one nonblocking scope clarification in §1: the same law is optimal
for **each individually applied price edit**. For a collection of such edits,
the unnormalized absolute-error radius is multiplied by the supremum of
their absolute magnitudes. That supremum must be finite for a finite common
radius when the underlying residual radius is positive. The revised price
should explicitly preserve the inherited C4 assumption `1+epsilon>0`.
Neither point changes the proof for a fixed admissible edit.

A minor presentation improvement is to introduce the normalized `q` display
with “For `R>0`,” before displaying `B_rem/R`. The next paragraph already
handles `R=0` correctly, so this is not a mathematical gap.

## 1. Exposure, independence, and work discipline

This is a non-blinded, separate same-model proof audit, not an external human
review or formal verification. I read the full new draft, so the proposed
construction and arguments were visible before checking them. I also read:

- `v2/derivations/09_c4_price_revision.md`, §§1–2, §11, and §14, for the reset
  model, exact kernel, canonical residues, and original midpoint example.
- `v2/work_logs/F16_2026-10-05_S1.md`, for the review/evidence constraints.
- The parent assignment and agent-status output. The latter included the
  previous candidate/proof summary and the stated finite-search result. I
  did not open the finite-search source or records, use finite success as a
  premise, or treat the previous lower derivation as an established lemma.

I rederived the assigned identities and inequalities symbolically by hand.
The rational witness was checked by hand. No arithmetic script, CAS, LP,
experiment, search over parameter cases, external search, or rerun was used.
Tool use was confined to local file reads/path inspection and writing this
review. No frozen file, derivation, source, or main document was edited.
One attempted review-only patch failed to match its context and changed no
file; the subsequent review edit succeeded. This was not a scientific run.

A narrow child reviewer, `/root/f16_coherent_lower_audit/reduction_witness_check`,
independently cross-checked §§1–2 and §9 with the same no-experiment/no-search
restriction and reported agreement without arithmetic tool use. Its check is
additional same-model scrutiny, not an external independence claim.

## 2. Exact fiber and decoder reduction (§§1–2)

The C4 canonical summary fixes every within-level contrast and the averaged
old mean `B`. Subtracting the minimum contrast on each level yields fixed
nonnegative `rho_w`, with at least one zero residue on every level. For any
compatible law, the remainder is constant across the worlds of a level, so

    p_w = rho_w + z_(|w|)/binomial(k,|w|).

Nonnegativity is exactly `z_h>=0`; normalization and the old averaged mean
give the two displayed linear constraints on `z`. Conversely, those
constraints reproduce both the contrasts and `B`, hence the complete old
numeric profile by the kernel characterization. The parametrization is
therefore an exact equality of fibers. It imposes no exchangeability
assumption on the original law: only its variable remainder is exchangeable.

For a nonempty fiber, `0<=R<=1`. If `R=0`, the law is the fixed residue vector
and its conditional radius is zero. If `R>0`, normalizing by `R` gives exactly
`X_mu`, and nonemptiness implies `1<=mu<=b`. Since

    g_0=1 < ... < g_(k-1)=(k+1)/2 < k<=b,

the level abscissae are distinct for every allowed `k,M`. No division by zero
or coincident terminal level occurs at `M=0`.

For the singleton curve, its interior segment slopes are

    (k-h)(k-h+1)/(k(k+1)),

and the final slope is `2/[k(k+2M-1)]`. The former decrease, and the final one
is no larger than the preceding slope because

    k+1 <= 3(k+2M-1)

for `k>=2,M>=0`. Thus the curve is concave. Its endpoint chord is a pointwise
minorant, and the adjacent-level interpolation is its concave upper boundary.
Consequently `L_1=p=(mu-1)/(b-1)`, `U_1=B_1`, and the two stated laws attain
these values. This includes `k=2,M=0`, where the singleton curve is entirely
linear and its width is zero, although the full law can remain nonunique.

Both laws lie in `X_mu`, so their average does also. For every proper size,
`E_(q^-) f_r=p`; hence the proposed center coordinate is `(p+B_r)/2`.
The two inequalities (1) imply directly

    U_r-(p+B_r)/2 <= (U_1-p)/2,
    (p+B_r)/2-L_r <= (U_1-p)/2.

Conversely, the endpoints of a singleton interval force every numerical
decoder, and therefore every law-valued decoder, to incur at least half its
width. Since a compatible law achieves that bound, the law constraint causes
no increase once both halves of (1) are established. Subtracting the bounds
also gives `U_r-L_r<=U_1-p`, which justifies singleton width dominance.

For a particular proper subset `S`, its moment is a known residue offset plus
`R E_q f_(|S|)`. Thus all residual intervals of the same size have the same
width, including in nonexchangeable fibers. Under a single edit of attempt
`i`, each revised mean is its known old mean plus `epsilon*m_A`, where `A`
is the prefix preceding `i`. For every size `1,...,k-1`, such an order exists,
and at least one singleton is included because `k>=2`. The empty prefix is
known exactly. Therefore the lower bound is a target-coordinate lower bound
for every edited index, and multiplication by `R|epsilon|` is exact.

### Edit-family clarification

For any bounded collection `E` of separately applied edits, with all orders
included for each edit, the common radius is

    (sup_(epsilon in E) |epsilon|) * R*(U_1-p)/2.

The same candidate is minimax for every individual edit, so it attains this
joint bound as well. If magnitudes are unbounded and the residual radius is
positive, the unnormalized common radius is infinite. A radius normalized
by `|epsilon|` remains the stated finite proper-moment radius. This is the
precise reading recommended for §1's collection statement. A zero edit is
trivial, and a zero residual radius stays zero regardless of edit magnitude.

## 3. Interpolation and endpoint audit (§2)

For fixed `k,M,r`, the feasible pairs
`(E_q g,E_q f_r)` form the convex hull of the finitely many points
`(g_h,f_r(h))`. Its lower and upper boundaries are polygonal, and every
boundary vertex has an abscissa among the `g_h`. Hence the **actual**
`L_r,U_r` are affine on each interval between consecutive levels, even when
the relevant hull edge skips some levels. `B_r` is affine there by its
adjacent-level definition, `U_1=B_1`, and `p` is globally affine. Therefore
both differences in (1) are affine on every such interval and are determined
in sign by the endpoints. The proof correctly interpolates the actual
envelopes; it does not need the auxiliary lower bound `ell_r` to have only
level knots.

At `mu=g_0` and `mu=g_k`, the feasible level law is respectively `e_0` and
`e_k`, and both inequalities are equalities. For `r=1`, they are the defining
equalities of the singleton extrema throughout the domain. Therefore the
remaining argument legitimately assumes `r>=2`, which entails `k>=3`.

## 4. Convexity in the moment index and affine lower bound (§6)

Extend the binomial definition to `f_0(h)=1` and
`f_k(h)=1{h=k}`. The monotonicity follows from the successive ratio up to the
last nonzero term, with all subsequent terms zero. For forward second
differences `0<=s<=k-2`, the stated identity is correct:

    f_(s+2)(h)-2f_(s+1)(h)+f_s(h)
      = f_s(h)*(k-h)(k-h-1)/[(k-s)(k-s-1)].

The denominator is positive in that range. Zero terms, `h=k-1` (linear
sequence), and `h=k` (constant sequence) cause no exception. Convexity puts
indices `0,...,r-1` below the chord from `(0,1)` to `(r,f_r(h))`; monotonicity
bounds indices `r,...,k-1` by `f_r(h)`. Summing gives

    sum_(s=0..k-1) f_s(h)
      <= (r+1)/2 + [k-(r+1)/2]*f_r(h).

The terminal term is handled using
`M*1{h=k}<=M*f_r(h)`, valid because `M>=0`, `f_r(k)=1`, and all moments are
nonnegative. Together with the identity for `g_h`, this proves the stated
pointwise affine majorant of `g_h`. Averaging and rearranging proves (3),
because `2b-r-1>=k>0` in the nontrivial range. This is a rigorous lower bound
on the true minimum; it is not being asserted to be the exact lower envelope.

### Monotonicity of the deficit in `M`

On the positive branch, direct subtraction gives

    p-ell_r(mu)
      = (r-1)(b-mu)/[(b-1)(2b-r-1)].

Differentiation has the stated numerator

    N(b)=-2b^2+4mu*b-(r+3)mu+r+1.

For an interior node, `1<=mu<=(k+1)/2`, so
`b>=k>=2mu-1>=mu`. Therefore `N'(b)=4(mu-b)<=0`, and

    N(2mu-1)=-(r-1)(mu-1)<=0.

All removed denominator factors are positive. The rational deficit is thus
nonincreasing on the required domain. On the zero branch the deficit is
`(mu-1)/(b-1)`, also nonincreasing. Equivalently it is the minimum of those
two nonincreasing expressions. The reduction to `M=0` is valid at every
interior node. Values of `mu` above `(k+1)/2` are covered later by interpolation
and the terminal endpoint; no unjustified derivative claim is needed there.

## 5. Exact lower-node comparison (§7)

Put `m=j`, `s=k-m`, and `n=r-1`. At `M=0`, twice the deficit in §6 is exactly
the right side of (4). Its denominator satisfies `2k-n-2>=k>0`. Using

    g_m-1=m/(s+1),
    k-g_m=(ks-1)/(s+1),

comparison of the two branches reduces to

    2m <= n(s+1).

Thus the threshold `n_0=2m/(s+1)` and both branch orientations are correct;
at equality the two values coincide.

If `m<r`, then `a=0`, `s>=2`, and `k>=3`, so
`(s+1)(k-1)>=3(k-1)>=2k`. This gives `p<=t/2`; the target lower bound is
nonpositive and is covered by nonnegativity. This includes the otherwise
small `k=3,s=2` case.

In the remaining domain, `m>=2` and `1<=n<=m-1`. All product factors in the
bound for `P` are defined and nonnegative. Bounding its first `n-1` factors
by the corresponding `s=1` factors gives `(k-n)/(k-1)` by telescoping;
multiplication by the last factor yields `(m-n)/(k-1)`. The empty product
when `n=1` is one, so that endpoint is included. Substitution proves (5).

### `s>=3`

On the first branch, the displayed bound

    (n+s-1)(s+1)>=2m+s^2-1>=2(m+s)

holds because `s^2-2s-1>=0` for every integer `s>=3`.

On the second branch, substitution and multiplication by positive factors
give exactly the stated `F(n)`. Its quadratic coefficient is `-m(s+1)<0`.
When `n_0>=1`, nonnegativity on the full real interval `[1,n_0]` follows
from its two endpoints; this is sufficient even if some of that real interval
lies beyond the allowed integer range. When `n_0<1`, this branch is empty.

Both endpoint expansions are correct:

    F(n_0)=2m(ks-1)(s^2-2s-1)/(s+1),
    F(1)=2s^2*m^2+(2s^3-5s^2-3s+2)*m-2s^3+2s.

The derivative of the second expression in `m` is at least
`2s^3+3s^2-3s+2>0` for `m>=2`. At `m=2`, it equals
`2(s-1)(s^2-2)>=0`. The proof covers both branches without a rounding or
endpoint gap.

### `s=2`

The exact expression

    d=n(2k-n-3)/[k(k-1)]

follows by canceling the binomial ratio, with `1<=n<=k-3`. For the first
branch, `3n(2k-n-3)` is increasing throughout the allowed interval, and its
excess at `n_0=2(k-2)/3` is exactly
`2(k-2)(k-5)/3`. A first-branch integer can occur only when `k>=5`, consistent
with the stated bound.

For the second branch, `(2k-n-3)(2k-n-2)` decreases over the relevant real
interval. Its excess at `n_0` is exactly `2(2k-1)(k-5)/9`. For `k>=5` the
argument is valid, including equality at `k=5,n=2`. The only remaining case
under `m>=r` is `k=4,n=1`, and the explicit comparison `20>=56/3` is correct.
For `k=3`, `m<r` has already disposed of the case.

### `s=1`

The exact difference is `d=n/k`. Here `n<=k-2<n_0=k-1`, so only the second
branch is relevant. Its value is `n/(2k-n-2)<=n/k`, with equality possible
at `n=k-2`. This also covers the `k=3,r=2` boundary.

The complete case split therefore proves the lower inequality at `M=0`.
The deficit monotonicity proves it at every `M>=0` interior node; the
endpoint/interpolation argument then proves it for every feasible `mu`.

## 6. Exact `k=4` witness (§9)

At `k=4,M=1/10,mu=9/8`, one has `b=41/10`, `p=5/124`, and
`q^+=(e_0+e_1)/2`. Averaging it with
`q^-=(119/124)e_0+(5/124)e_4` gives exactly

    q_c=(181/248,1/4,0,0,5/248).

The masses sum to one. Its proper moments are

    (41/496,5/248,5/248),

and its terminal moment is `5/248`. Thus its old mean is

    1+41/496+5/248+5/248+(1/10)*(5/248)=9/8.

The conditional proper-moment intervals are

    r=1: [5/124,1/8],
    r=2: [0,1/24],
    r=3: [0,5/124].

These can be verified directly at this fixed witness from the four secants
from `(g_0,0)`: the pair maximum uses level 3, the triple maximum uses the
terminal level, and the adjacent-level mixture gives zero for both lower
endpoints. No parameter search is involved.

The singleton half-width is `21/496`, attained by the candidate. Its pair
moment differs from the pair midpoint by

    5/248-1/48=-1/1488,

as stated. Its pair and triple errors are within the common singleton
tolerance. The old coordinate-midpoint construction would instead force
`m_4=5/372`, assigning `1/48-2*(5/248)+5/372=-3/496` to a specified
exactly-two-failure world. Hence the new coherent center and the old
incompatible midpoint example are consistent, distinct claims.

## 7. Recommended disposition to the principal

No repair is required for the lower proof, interpolation, or numerical
witness. Make the edit-family scaling/positivity clarification if retaining
the collection language, and place the `R>0` condition before the normalized
display. Explicitly writing `f_0=1` and `f_k=1{h=k}` before
§6 would also make the endpoint notation self-contained, but the binomial
extension is already unambiguous and this is editorial only.

Promote the universal theorem only after the separate upper-envelope audit
passes; preserve the distinction between a feasible minimax center and
simultaneous attainment of every coordinate's individual interval midpoint.

**Signed:** ChatGPT (GPT-6 Astra Pro),
`/root/f16_coherent_lower_audit`, October 5, 2026.
