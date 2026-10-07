# P3-02 independent review: probability information, retention and repair

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent subagent review,
October 7, 2026 UTC. This review is development reasoning for P3-02. Its
overlapping effort receives no separate research-time credit. It does not
change a phase-two claim, gate, ledger or experimental result.

## 1. Finding and recommended disposition

The finite-loss observation model is a direct general reconstruction of the
linear-information machinery already used by phase two. Its useful P3 role
is to make the **requested service** explicit: a law, selected expectations,
intervals, preferences or one action. Full-law retention and repair are only
one case. A generic kernel theorem, matrix rank or relabelling of expectations
as values is not an additional contribution by itself.

A defensible adaptation is a typed, source-qualified interface that says
which new loss queries are exactly recoverable, which need an uncertainty
set or additional observations, and which unit/criterion changes preserve
that interface. The mathematics below is ordinary linear reconstruction;
the proposed project use is its careful connection to the existing retention,
repair and native-certificate contracts. This review alone does not change
**P3-N01: NOT YET SUPPORTED**.

## 2. Load-bearing repository records inspected

| Record | Relevant content |
|---|---|
| `v3/work_logs/P3_02_2026-10-07_S1.md` | Current task contract, strong ordinary comparator, no duplicate agent time. |
| `v3/foundations/01_representation_boundaries.md` §1 | Known rational coefficients; exact bilinear obstruction; valid outer-enclosure interface. |
| `paper_v2.md` §§7.1–7.4, Theorems 3–5 | Reset loss matrix, exact summary ranks, actual new-mean repair, decision stability, compatible recovery. |
| `v2/derivations/09_c4_price_revision.md` §§1–8 | Full model assumptions; nonproportional and proportional price families; adaptive-query lower bound; known-marginal restriction. |
| `v2/derivations/09_c4_price_revision.md` §§11–13, 15 | Exact old-summary fibers; interval/threshold services; ordinary capacity formulation; statistical repair and native admission. |
| `v2/derivations/10_f16_coherent_recovery.md` §§1–2, 10 | Exact statement of compatible common-radius recovery and explicit additional-source counterexample. The detailed envelope proof is inherited and was not rerun. |
| `v2/derivations/06_n01_decision_retention.md` D20–D21 | Current answers versus future-edit sufficiency; revision access changes the information problem; more thresholds can recover more numerical information. |
| `v2/foundations/03_provisional_core.md` §§2–3 | Source identities, directed conversion table, valuation bridges and rational CPWA grammar. |
| `paper_v2.md` §5.2, Theorem 2; §11.2 | Target-unit-reduct completeness and the explicit ordinary-reconstruction/novelty boundary. |

These are exact repository locators, not claims to have reread the historical
archive. The older empirical challenge is not reopened.

## 3. General finite-loss reconstruction and its repair corollary

Let the finite world law be `p` in a declared admissible set
`D ⊆ Δ_n`. The semantic loss rows in `L ∈ R^{m×n}` are known, and the
retained observations are exact expectations `y=Lp`. A specified target
family has rows `Q ∈ R^{r×n}` and requests `Qp`.

For **every** source set, a decoder from `y` exists exactly when

\[
Lp=Lp'\quad\Longrightarrow\quad Qp=Qp'
\qquad(p,p'\in D).
\]

This is constancy on observation fibers, with no computational-efficiency
claim. It is the same indistinguishability principle as
`09_c4_price_revision.md` §3 and `06_n01_decision_retention.md` D20.

For a nonempty **convex** source, let `V=span(D−D)` be its actual affine
direction space. Then the condition is equivalently

\[
K:=V\cap\ker L\ \subseteq\ \ker Q.
\tag{R1}
\]

Necessity uses a relative-interior law: sufficiently small opposite
perturbations along any `v∈K` remain admissible and have the same retained
data. Sufficiency follows because every admissible difference lies in `V`.
In this case the decoder can be affine. Fix `p₀∈D`; the relation
`F(Lv)=Qv` defines a linear map on `L(V)` precisely when (R1) holds, giving
`Qp=Qp₀+F(Lp−Lp₀)`.

On the unrestricted normalized simplex this becomes

\[
\operatorname{row}Q\subseteq
\operatorname{row}\begin{bmatrix}\mathbf1^\top\\L\end{bmatrix},
\]

and full-law recovery is the special case `Q=I_n`, or rank `n` of the
displayed augmented matrix. Normalization is side information; it must not
be omitted or charged as another unknown measurement.

**Source qualification is essential.** If `D={e₁,e₂,e₃}` contains only three
Dirac laws, `L=(0,1,2)` identifies which allowed law holds, although the
normalization-augmented matrix has rank two. The fiber condition remains
correct; a rank test on the entire affine hull would overstate necessity.
The native language allows finite unions of polyhedra, so convex-source
necessity is not automatically a theorem for every admitted context.

### Target-specific repair

For a convex source, put

\[
d_Q=\dim Q(K)
=\operatorname{rank}([L;Q]|_V)-\operatorname{rank}(L|_V).
\tag{R2}
\]

Exactly `d_Q` further unrestricted exact linear measurements suffice and
are necessary in the worst case to recover the target expectations.
Choose `d_Q` rows of `Q` whose restrictions to `K` span all such restricted
rows. These measurements annihilate every remaining direction that could
change `Qp`. Conversely, fewer rows cannot reduce `K` to a subspace of
`ker Q`: their common kernel in `K` has dimension greater than
`dim K−d_Q`. Small opposite perturbations at a relative-interior law give
the obstruction. The transcript argument in C4 §5 also covers deterministic
adaptive selection of exact linear probes: fix the central-law transcript
and choose a direction preserving all its answers.

This is a worst-case count across the declared source and its possible old
summaries. For one already observed `y`, recompute the actual affine hull of
`D∩{Lp=y}`. A boundary observation can collapse that fiber to a lower face
or even a single law, reducing its conditional repair requirement.

This reconstructs the existing phase-two repair principle for an explicit
target. It does not say that every permitted physical query interface can
attain (R2). If target rows themselves are available, a basis of target rows
does attain it. With a restricted query menu, target rank is only a lower
bound. For example, let `(x,y)` range over `x,y≥0, x+y≤1`, retain nothing,
and target `x`. If the only probes are `x+y` and `y`, target rank is one but
both probes are necessary. Neither available single answer determines `x`.

For an available repair matrix `R`, the exact feasibility test is
`V∩ker L∩ker R ⊆ ker Q`. Selecting a cheap sufficient subset of its rows is
a further query-design problem. Rank alone supplies neither observation
prices nor minimum execution cost.

## 4. Exact reset-family specialization already established in phase two

For `k` reset procedures, worlds record which procedures fail. Let
`m_S=P(S all fail)` and retain all old order means

\[
C_\pi(c,M)=\sum_{j=1}^k c_{\pi_j}
m_{\{\pi_1,\ldots,\pi_{j-1}\}}+M m_{[k]}.
\]

This is a finite known loss matrix in the joint world law, equivalently a
linear map of its invertible Boolean moment coordinates. The fixed-law,
all-orders, strictly positive attempt-price assumptions are substantive.

* One profile has exact numerical rank `2^k−k`, versus law dimension
  `2^k−1`. It therefore loses `k−1` law directions, even when `M>0`.
* Two nonproportional positive price profiles determine the full law when
  at least one terminal penalty is positive. If all penalties vanish,
  the all-failure moment is unseen and full-law recovery is impossible.
* Starting from a minimum old numerical summary with `M>0`, one nonzero
  admissible attempt-price edit admits exactly `k−1` actual new-order mean
  probes attaining full recovery. For nested prefixes `P_r` before the
  edited procedure `j`,
  `C_{π_r}(c+εe_j,M)−C_{π_r}(c,M)=εm_{P_r}`.
* With known moments through order `s` and an interior compatible law,
  the incremental number is `k−s−1`; without positive penalty, only the
  proper moments can be recovered and the count is `max(k−s−2,0)`.

These are inherited results, not new P3 theorems. Their constructive
achievement goes beyond a generic rank slogan by realizing missing
coordinates as actual allowed new order means. Their exact scope is
`09_c4_price_revision.md` §§3–5, 8 and `paper_v2.md` Theorems 3–4.

There is no universal principle that repricing forces the full joint law.
For two binary events, a loss family `aX+bY` at every known price `(a,b)`
needs just `E[X]` and `E[Y]`; no price in that family can recover
`P(X=Y=1)`. A correlation-sensitive target must add another loss row.
Conversely a one-action or tolerance-qualified request can need less than
all those marginals. The reset-family result concerns its particular rich
order/price family.

## 5. Known recoding, criterion change and unknown stakes

### Known numerical recoding

If a stored vector is replaced by `y'=Ty+b`, with known `T,b` and `T`
injective on the relevant observation image, the observation fibers and
every recoverable service are unchanged. In particular a known invertible
matrix `T` gives `L'=TL+b1ᵀ` and preserves normalization-augmented rank.
The same statement holds for a known positive rescaling of each separate
measurement when its inverse and semantic labels are retained.

This is an **information** statement. An arbitrary invertible row mixing or
separate scaling of action losses need not preserve their preference order.
A common positive affine transformation of all action losses preserves
expected-loss rankings; more generally adding the same state-contingent
loss to each action also cancels from pairwise expected differences. Which
recoding preserves information and which preserves a specified criterion
are distinct questions.

### Known repricing

New semantic weights define new query rows `Q`; their answers are available
from the old data precisely under the relevant fiber/span condition.
Knowing the new payoff matrix does not provide its expectations for free.
In the reset family, jointly scaling all attempt prices **and** the terminal
penalty simply scales old costs and adds no information. Scaling only
attempt prices while holding a nonzero terminal penalty fixed is a criterion
change and can add one independent direction. The proportional-family
classification uses the rank of rows `(λ_a,M_a)`; see C4 §4. Thus the word
“proportional” must specify exactly which quantities are scaled.

### Unknown stakes: obstruction and calibration cases

A lone loss `v=c(1−p)` with unknown positive stake does not determine `p`:
the same `v=1/5` arises from `(c,p)=(1,4/5)` and `(2,9/10)`. Unknown
independent stakes in several channels similarly cannot be treated as
known loss rows.

Unknown **shared** calibration can nevertheless be identifiable. If an
exhaustive event partition is observed as `v_i=c p_i`, with one shared
unknown `c>0`, then `c=Σ_i v_i` and `p_i=v_i/Σ_j v_j`. Two observed known
payoff anchors can likewise identify an otherwise unknown common affine
recoding. The obstruction is lack of sufficient calibration, not the
mere presence of an unknown stake parameter. At `c=0` the partition vector
collapses and normalization cannot recover the law.

Randomness in stakes is also different from uncertainty in the payoff
interpretation. If each world's stake `c(ω)` is known, then
`E[c(ω)1_E(ω)]` is an ordinary fixed loss row in a law over those worlds,
even when stakes and the event are correlated. If instead only separate
stake and event summaries are kept, missing joint information matters. One
cannot replace `E[c1_E]` by `E[c]P(E)` without the necessary relationship.

## 6. Approximation and coherence must survive reuse

For a closed convex source, retain the complete compatible set

\[
\mathcal P_y=\{p\in D:Lp=y\},
\]

or its justified noisy analogue. Each target's exact identification interval
is obtained by minimizing/maximizing that row on this set. With rational
polyhedral data these are ordinary linear programs; endpoint witnesses and
dual bounds can be checked. A narrower set needs justified extra evidence,
not merely a chosen estimate.

Separate interval midpoint answers need not equal `Qp*` for one compatible
law. For example take `D=Δ₃`, no informative old measurements (`L=0`) and
target `Q=I₃`. Every coordinate ranges over `[0,1]`. Unrestricted vector
predictions attain common maximum absolute error `1/2` at
`(1/2,1/2,1/2)`, which is not normalized. Every compatible prediction law
has a coordinate at most `1/3`, so its error against the corresponding
vertex is at least `2/3`. The uniform law attains `2/3` for all coordinates.
Thus a compatible center can cost strictly more even on a full observation
fiber. “Full fiber” alone does not imply F16's result.

`10_f16_coherent_recovery.md` proves a stronger positive result for the
**specific full exact equal-old-price reset fibers**. Its residue/level-law
decomposition produces one compatible law at the unrestricted common
proper-prefix radius, hence at the optimal revised-mean radius for each
separately applied single-price edit. The equality requires its envelope
proof, not generic convexity. Extra source restrictions, noisy old means,
arbitrary new linear combinations, changed penalty and simultaneous price
edits are outside that theorem. Section 10 gives a rational convex-source
triangle with unrestricted radius `1/400` and compatible radius `1/300`.

An estimated compatible law is still an estimate. Its exact numerical
expectations cannot be installed as new authoritative source equalities.
Carry the query-family error bound, or certify subsequent conclusions over
the whole remaining source. In particular, a good bound for each separately
applied price edit does not automatically certify arbitrary compositions
of edits or linear combinations of the predictions.

The exact-rank discontinuity also differs from decision instability. C4 §6
already proves that an old optimum has new-price regret at most `|ε|` for
one attempt-price edit in the stated objective families, even when the edit
changes the exact information rank. C4 §12 provides the corresponding
interval/threshold/refusal contract. These are constructive examples of
useful service without full recovery.

### Error amplification is part of the bridge

An affine recovery identity `q=α1ᵀ+βᵀL` gives
`q p=α+βᵀy`. If justified measurement errors satisfy
`|ŷ_i−(Lp)_i|≤η_i`, then

\[
|\alpha+\beta^\top\hat y-qp|
\le\sum_i|\beta_i|\eta_i.
\]

Algebraic recoverability need not be stable. The reset repair divides by
`ε`, so two separately perturbed means with errors at most `η` can incur
`2η/|ε|` reach-probability error. Paired retained world traces instead give
an observed reach indicator after division and avoid this intrinsic
statistical factor. Those traces are additional information and have their
own access/storage cost; C4 §6 and §15 explicitly make this distinction.

## 7. Exact native-admission boundary

The finite-law theorem is mathematical and permits real coefficients and
real population expectations. The existing native grammar permits fixed
**rational** coefficients and finite rational polyhedral source cases.
For known rational `L,Q`, rational exact observations or justified rational
intervals can define a native source, provided a feasible witness is supplied
and source identity/population assumptions match the current request. An
irrational population expectation is not an exact rational literal merely
because the abstract theorem allows it.

When both payoff parameters and probabilities vary independently as source
coordinates, products such as `c(1−p)` are generally not finite CPWA terms.
The same warning applies to the unknown-common-scale normalization formula
above: division by a variable sum is generally outside the grammar. A fixed
concrete rational request can be normalized during charged construction;
that does not create one exact native term for arbitrary varying inputs.
Other valid routes include fixed parameter cases, a justified enclosure,
or a proved language extension. Introducing a fresh coordinate `z` does
not by itself prove `z=c(1−p)`; P3-01's representation-boundary proof already
establishes that limitation.

There is also a **unit-access boundary**, beyond ordinary matrix algebra.
Core §2 distinguishes true coordinate conversions from valuation bridges.
Theorem 2 in `paper_v2.md` makes native proof existence equivalent to
validity on the **target-unit reduct**, which retains only rows whose units
can reach the requested target unit by declared directed conversions.
Numerical invertibility of a known loss/probability factor does not invent
a reverse conversion. If only a probability-to-loss bridge is declared,
loss-unit observations may determine a probability numerically while
remaining unavailable to a probability-unit native query. Supply a justified
reciprocal conversion, or formulate the source and query in a reachable unit.
Reciprocal factors, transformed premise rows and budgets must all agree.

For a justified rational polyhedral source and a reachable rational target,
the inherited completeness theorem supplies finite proofs of valid finite
bounds. It does not certify that learned estimates equal expectations, that
samples are iid, that the population stayed fixed, or that a changed evaluator
shares the old quantity identity. C4 §15 describes this conditional admission
for empirical repair, including simultaneous coverage and nonempty-source
requirements. No new checker rule or empirical guarantee follows from the
probability-recovery theorem alone.

## 8. Integration recommendation

The principal P3-02 artifact should state the fiber theorem first, then the
normalized finite-matrix result and service-specific consequences. Use the
reset theorem as an inherited constructive example of exact repair, and
the F16 theorem as an inherited specialized positive coherence case. The
generic repair corollary, calibrated unknown-scale example, restricted-probe
counterexample and native-unit qualification clarify how the probability
interface may be used. Label them **reconstructed** or **adapted**, with the
source and target services explicit.

The strongest ordinary comparator retains the same `L`, source constraints,
payoff semantics, query menu and budget, then uses normalized probabilities,
a credal polytope, linear reconstruction or interval optimization as needed.
It can reproduce every general calculation in this review. A separate P3
contribution claim would need additional concrete content under a named
comparison scope; this review supplies no reason to award it automatically.
