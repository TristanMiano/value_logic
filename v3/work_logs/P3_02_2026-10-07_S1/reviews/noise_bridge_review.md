# P3-02 hostile review: noisy observations and compatible recovery

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent subagent review,
October 7, 2026 UTC. This is mathematical development review. No additional
agent-clock credit, primary-artifact edit, gate or new executable result is
claimed.

## 1. Disposition and phase-two antecedents

The proposed scalar global-radius identity is correct for the specified
bounded-error observation model. The compatible vector-center formulation
is also correct, with one necessary qualification: it is a **linear program
when the source and error sets are polyhedral**, not for an arbitrary compact
convex source merely because the objective is linear.

The generic recovery ingredients are already established phase-two material:

| Exact repository locator | Previously established scope |
|---|---|
| `v2/work_logs/F16_2026-10-05_S1/root_reconstruction.md` §15 | Coordinate extrema, free sup-norm midpoint radius, compatible-law center LP and factor-two bound. |
| `v2/derivations/07_adversarial_review.md` §6 | The same strongest ordinary combined baseline and explicit source-preserving center LP. |
| `v2/work_logs/F16_2026-10-05_S1/reviews/contribution/ordinary_baseline.md` §§2, 5 | Scalar/vector midpoints, conditional certificates, simultaneous coverage, and replacing exact old observations by intervals in the existing recovery framework. |
| `v2/literature/06_c4_contribution_comparison.md` §4; F16 `reviews/contribution/source_record.md` §C | Checked ordinary optimal-recovery source for bounded observation errors, local/global error and polytope center methods. |
| `v2/derivations/10_f16_coherent_recovery.md` §§1–2, 10 | Specialized full exact equal-price fiber equality, its attaining law and the extra-source triangle counterexample. |
| `v2/work_logs/F16_2026-10-05_S1/source_uncertainty_boundary.md` §§2–5 | An already established three-procedure example where arbitrarily narrow old-mean intervals permit a strict compatible-center premium. |

I did not locate the eliminated pair constraint `|L(p−q)|≤2ε` written in
that exact general form in these inspected records. Deriving it below is a
direct reconstruction of their observation-fiber method, not evidence for
a new recovery principle. The known joint-error-set formulation and the
common-bias/calibration examples below are **illustrative adaptations in
this P3 review**, reproducible by the same ordinary methods. No new
contribution support follows from their inclusion alone.

## 2. Scalar global minimax identity: exact statement and proof

Let `P⊆R^n` be nonempty compact, let `L∈R^{m×n}` and scalar target row `c`
be known, and let `ε∈R^m` have finite nonnegative entries. The observation
model permits exactly

\[
z=Lp+e,\qquad p\in P,\qquad |e_i|\le\epsilon_i.
\]

This is a deterministic joint error-set assumption. It makes no assertion
of stochastic independence, unbiasedness, frequencies or confidence.
For every possible observation define

\[
F_z=\{p\in P:|Lp-z|\le\epsilon\},
\quad a(z)=\min_{F_z}cp,\quad b(z)=\max_{F_z}cp.
\]

Only observations with nonempty `F_z` belong to the task. Compactness makes
the extrema attained. An unrestricted deterministic scalar decoder may
output any real number as a function of z, without a computation, continuity,
precision or memory restriction. Its global worst-case error is minimized by
the per-fiber midpoint `(a(z)+b(z))/2`, giving

\[
R_{\rm free}
=\frac12\sup_z\bigl(b(z)-a(z)\bigr)
=\frac12\max\left\{|c(p-q)|:
 p,q\in P,\ |L(p-q)|\le2\epsilon\right\}.
\tag{B1}
\]

**Local lower and upper bounds.** The two endpoint target values are both
compatible with z. For any output t, the triangle inequality gives
`max(|t−a|,|t−b|)≥(b−a)/2`; their midpoint attains equality for every target
value between them. The same explicitly defined midpoint decoder works at
every possible z, so no unproved interchange of minimization and supremum
is required.

**Eliminate the observation.** If p and q share a feasible z, then
`|L(p−q)|≤|Lp−z|+|Lq−z|≤2ε`. Conversely, if that pair inequality holds,
the single observation `z=(Lp+Lq)/2` is feasible for both. Thus the pair
sets coincide after existentially eliminating z, proving (B1). The pair
domain is nonempty compact, so the displayed supremum is a maximum.

Convexity is **not needed** for this free scalar identity. It becomes
important for a compatible output law: when P is convex, every `F_z` is
convex, and the average of two endpoint laws lies in `F_z` and attains the
scalar midpoint. Hence a law-valued decoder has **no additional error for
one scalar linear target** under these hypotheses. A vector of individually
optimal scalar outputs need not have a common attaining law.

For rational polyhedral P, the global diameter in (B1) can be computed by
one linear program maximizing `c(p−q)`. The feasible pair set is symmetric
under swapping p and q, so a separate negative-orientation solve is not
needed. A feasible maximizing rational pair supplies a lower witness and
its midpoint observation; an ordinary rational dual bound certifies the
matching upper bound. For general compact P this remains an optimization
identity, with no LP or finite-arithmetic claim.

## 3. Vector sup-norm recovery and the exact compatibility criterion

Let C have finitely many target rows `c_i`, and fix a nonempty fiber. Write

\[
a_i=\min_{p\in F_z}c_i p,\qquad
b_i=\max_{p\in F_z}c_i p.
\]

For an unrestricted output vector v,

\[
\sup_{p\in F_z}\|Cp-v\|_\infty
=\max_i\max\{b_i-v_i,v_i-a_i\}.
\]

Each direction follows by bounding every coordinate and then choosing its
attaining endpoint. No independence between target coordinates is used.
Consequently

\[
r_{\rm free}(z)=\tfrac12\max_i(b_i-a_i).
\tag{B2}
\]

A compatible decoder chooses one `q∈F_z` and outputs `Cq`. Its exact
conditional optimization is

\[
\begin{aligned}
\text{minimize }&r\\
\text{over }&q\in F_z,\quad r\ge0,\\
\text{subject to }&b_i-c_iq\le r,\quad c_iq-a_i\le r
\quad\text{for every }i.
\end{aligned}
\tag{B3}
\]

For rational polyhedral P and box errors this is a rational LP, after
computing the coordinate endpoint values. For arbitrary compact convex P
it is a compact convex optimization problem with the stated source-membership
constraint; that membership need not have a finite linear description.

Define the midpoint-tolerance box

\[
B_r=\prod_i[b_i-r,\ a_i+r].
\]

Then the exact equality criterion is

\[
r_{\rm compatible}(z)=r_{\rm free}(z)
\quad\Longleftrightarrow\quad
C(F_z)\cap B_{r_{\rm free}(z)}\ne\varnothing.
\tag{B4}
\]

Indeed (B3) at the free lower bound asks precisely for a compatible target
vector in that box. Coordinates with maximum interval width are fixed to
their own midpoints. Narrower coordinates have room to move. Requiring all
coordinate midpoints simultaneously is a stronger condition than (B4).
This criterion is a restatement of the inherited center LP, not another
new minimax theorem.

For the specified finite vector sup norm, the global free radius also equals
one half the largest `||C(p−q)||∞` over the pair set in (B1). This follows by
the same finite-coordinate maximum and shared-observation argument. No
corresponding pair-only formula is claimed for the compatible global optimum.

## 4. The Δ₃ example: rational endpoints and a dual lower certificate

Take `P=Δ₃`, `L=0`, `ε=0`, `z=0`, `C=I₃`. Thus `F_z=Δ₃`. Every coordinate
has endpoints zero and one, attained by simplex vertices. The unrestricted
midpoint vector `(1/2,1/2,1/2)` has radius `1/2`.

For a compatible law q, (B3) includes `1−q_i≤r` for all three coordinates.
Adding these inequalities and using `Σ_iq_i=1` yields

\[
2\le3r,\qquad r\ge\tfrac23.
\]

This is an explicit rational multiplier certificate. The uniform law
`q=(1/3,1/3,1/3)` attains the lower bound: each coordinate's largest error
is `2/3`. Hence

\[
r_{\rm free}=\tfrac12,\qquad
r_{\rm compatible}=\tfrac23.
\tag{B5}
\]

At the free radius, (B4)'s box is the single vector `(1/2,1/2,1/2)`, whose
sum is `3/2`; it cannot meet the simplex. The example does not say that a
single scalar coordinate suffers this premium. For one coordinate its
midpoint is attained by many compatible laws. The obstruction is simultaneous
performance of one output law across all three target directions.

This generic geometry is already acknowledged in the phase-two review
records and is not a new adverse example against their theorem.

## 5. Exactly why F16 does not extend to general noisy fibers

F16-C1 fixes the complete **exact** old numeric order profile, unit old
attempt prices, unchanged outcome law and terminal penalty, all Boolean
laws compatible with that profile, and the proper-prefix/revised-mean query
family generated by separately applied single-price edits.

Its proof first derives fixed nonexchangeable residues and a remaining
failure-count distribution q satisfying a single exact scalar moment
constraint. It then constructs an endpoint/adjacent-level mixture. Two
specific envelope inequalities place every target coordinate inside the
common optimum tolerance box (B4). That construction proves the required
intersection for that family.

A box of uncertain old observations need not have those fixed residues or
one exact remaining moment constraint. An arbitrary C does not have the
special proper-prefix envelopes. Extra source restrictions may remove the
constructed law. None of these changes preserves the key intersection merely
because the new fiber is compact, convex, or called a full observation fiber.

This is already supported by exact phase-two boundaries:

* `10_f16_coherent_recovery.md` §10 realizes an extra-source triangle with
  free radius `1/400` and compatible radius `1/300` inside the same reset
  model. The additional source changes the permitted output-law set.
* F16 `source_uncertainty_boundary.md` §§2–5 gives a three-procedure known
  support face with arbitrarily narrow old-mean intervals. At its rational
  example, interval width `1/100` and price edit `1/10` give free radius
  `11/2000` and compatible radius `11/1550`. This is inherited, already
  reviewed evidence; it is not rerun or presented as a new P3 construction.

The correct import is that F16 supplies one specialized equality proof and
that ordinary methods can implement its construction. The general noisy
interface should retain (B3)/(B4) and solve or prove its own instance.

## 6. Known joint noise: replace the box by its actual difference set

Let the error belong to a known nonempty compact set `E⊆R^m`, independent
of the unknown law in the sense that every pair `(p,e)∈P×E` is admissible.
This is a product **admissibility** condition, not stochastic independence.
Define

\[
F_z=\{p\in P:z-Lp\in E\}.
\]

Two laws share one observation exactly when

\[
L(p-q)\in E-E.
\tag{B6}
\]

To prove necessity, write the common observation as `Lp+e_p=Lq+e_q`.
Then `L(p−q)=e_q−e_p`. Conversely, any such error pair creates a common
observation. Thus the exact scalar free radius is

\[
\frac12\max\{|c(p-q)|:p,q\in P,\ L(p-q)\in E-E\}.
\tag{B7}
\]

No convexity of E is required for this free scalar identity. Convex P and
convex E give convex fibers, hence a compatible scalar midpoint law.
Polyhedral P and E give finite LP descriptions, possibly retaining two
explicit error vectors in the pair problem instead of projecting `E−E`.

For a symmetric coordinate box, `E−E=[−2ε,2ε]`, recovering (B1). For a
correlated set, replacing E by its coordinate bounds generally enlarges
the ambiguity relation. If admissible errors depend on p, or calibration
changes L, use the actual joint observation relation instead of (B6) with
an unrelated fixed E.

### Rational common-bias example: an exact calibration benefit

Take `P=Δ₂`, `L=I₂`, scalar target `p₁`, and

\[
E=\{(b,b):|b|\le1/4\}.
\]

Every law difference is `(d,−d)`, while `E−E` lies on the diagonal
`(a,a)`. Their intersection is zero, so (B7) gives exact recovery. Directly,

\[
b=\frac{z_1+z_2-1}{2},\qquad
p_1=\frac{1+z_1-z_2}{2},\qquad p_2=1-p_1.
\]

The known normalization calibrates the shared offset. At `z=(1/2,1/2)`
the only compatible law is `(1/2,1/2)`.

If the same per-coordinate error limits are instead treated as the full
box `|e_i|≤1/4`, that observation admits the endpoint laws
`(3/4,1/4)` and `(1/4,3/4)`, with errors `(-1/4,1/4)` and
`(1/4,-1/4)`. The interval for p₁ is `[1/4,3/4]` and the free radius is
`1/4`. The scalar upper certificate is simply the p₁ observation bound;
the endpoint pair proves sharpness. Those errors were impossible in the
shared-bias model. Rectangularizing error summaries discarded useful
calibration information.

This also applies when a common noisy anchor is subtracted from several
measurements: the anchor error occurs in every residual. Differences can
cancel it, so treating residual errors as freely varying coordinates can
be strictly more conservative than the original joint error contract.

## 7. Unknown scale plus additive errors: a rational calibration edge

The fixed-known-L hypothesis matters. Suppose unknown positive common-scale
values are `x_i=s p_i`, `p∈Δ₂`, `s>0`, and the observed vector is
`z=(2,1)` with bounds `|x₁−2|≤1/2`, `|x₂−1|≤1/4`. The calibrated value
source is the box

\[
3/2\le x_1\le5/2,\qquad3/4\le x_2\le5/4.
\]

It proves `s=x₁+x₂≥9/4>0`. The target `p₁=x₁/(x₁+x₂)` has exact interval

\[
\frac6{11}\le p_1\le\frac{10}{13}.
\tag{B8}
\]

For the lower endpoint, the affine certificate is
`6x₂−5x₁≤6(5/4)−5(3/2)=0`. The upper certificate is
`3x₁−10x₂≤3(5/2)−10(3/4)=0`. Positivity turns these signs into the ratio
bounds. The endpoints are attained at `(x₁,x₂)=(3/2,5/4)` and
`(5/2,3/4)`, respectively.

The scalar midpoint is `94/143` and its sharp radius is `16/143`.
Normalizing the noisy observed vector instead gives `2/3`, whose worst
error is `4/33>16/143`. Thus normalization alone need not be the minimax
decoder once the common scale is noisy and unobserved.

If the scale were separately known to equal three, the extra equality
`x₁+x₂=3` would reduce the interval to `[7/12,3/4]`, radius `1/12`.
Using fixed `L=3I` without that calibration premise would silently claim
this smaller uncertainty. The unknown-scale example is a linear-fractional
target over a calibrated value source, not an instance of (B1) with the
same fixed L. Its threshold certificates are affine in the value unit,
as reconstructed in `native_probability_bridge.md` §5.

Even known scales need quantitative conditioning. On `Δ₂`, with known
`L=sI`, `s>0`, and equal box error ε, (B1) gives scalar radius
`min(1/2,ε/s)`. The normalized measurement rank is sufficient for exact
recovery at every `s>0`, but there is no uniform small-noise guarantee over
scales approaching zero. For any positive rational ε, choose `s=2ε`;
the two simplex vertices share observation `(ε,ε)` and force radius
`1/2`. This is a per-family conditioning limit, consistent with (B1).

## 8. Remaining scope checks

* An impossible observation has no fiber and no meaningful midpoint radius.
  For `Δ₂,L=I,z=(9/10,9/10),ε=(1/10,1/10)`, both coordinates would be at
  least `4/5`, contradicting normalization. This source needs inconsistency
  handling, not a vacuous probability certificate.
* A jointly valid deterministic error set is not supplied merely by separate
  fitted standard errors or calibration averages. If a random source covers
  the true law with probability `1−δ`, the inherited simultaneous-source
  argument bounds the event of an accepted false selected conclusion by δ;
  it does not assert the same conditional probability given acceptance.
* A compatible center remains an estimate. Its membership in the current
  source does not authorize replacing that source by the selected singleton
  for future queries.
* All general identities here permit arbitrary decoding and charge no
  computational budget by themselves. Rational endpoint and multiplier
  certificates can enter the inherited native contract only through the
  current source identities and directed unit paths.

No false scalar identity remains under the stated contract. The substantive
corrections are the polyhedral qualification for LP claims, the scalar/vector
compatibility distinction, and preservation of actual joint error and
calibration information. These strengthen the interpretation of P3-02 while
leaving the generic optimal-recovery method classified as inherited.
