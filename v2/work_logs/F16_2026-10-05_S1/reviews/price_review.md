# F16 price-family review: final disposition

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, delegated separate reviewer. Date: 2026-10-05. Reviewed baseline: `6ef27f20e3ac0920953a27dd84d6c91a021ba58f`. This separate review contributes **zero principal D60 time**. It does not execute a frozen stage, a neural experiment, a native producer, ND02, F17, or Gate C/D, and does not edit the ledger or clock.

## Disposition

**Retain T1–T3 and A1–A3 at their declared mathematical scope. No counterexample or proof defect was found under the stated assumptions. Retain C4-S only as a worked price-revision application with small explicit consequences.** The rank, repair, approximation, and sampling claims do not establish a new general information theory, a native inference rule, a stable numerical inverse, an empirical calibration result, or an advantage over an ordinary method with the same information.

A later bounded [coherent-center review](price_coherent_center_review.md) identifies one local prose correction: in A1's specific `k=3` setting, all proper-moment midpoint predictions can in fact be realized by one law in the old-summary fiber. Thus §10's warning that those midpoint outputs may be incoherent is overbroad there. The radius theorem is unchanged. General coherent-center existence remains unresolved in this review; a single predeclared 735-fiber exact search found no gap.

The principal should not label this particular contribution a completely blind reconstruction. The statement-extraction process exposed small proof fragments before the initial derivation. The exact exposure is recorded in [price_initial.md](price_initial.md). The initial derivation was saved before the complete existing proofs or verification program were read. The separate reviewer then compared that saved derivation with `09_c4_price_revision.md`, the relevant F13 argument in `06_case_studies.md`, `c4_price_revision.py`, `case_retention.py`, and the existing test source. This is a partially exposed reconstruction plus a full scoped mathematical audit.

## What survives, and its earliest dependency

| Claim or consequence | Review result | Earliest necessary dependency |
|---|---|---|
| One-price numeric rank `2^k−k` and within-profile rank `2^k−k−1` | Reconstructed | One fixed Boolean outcome law, all full orders, sum-zero simplex tangent; then the F13 weighted adjacent-swap kernel (`06_case_studies.md` §5.1; repeated in `09_c4_price_revision.md` §2). |
| T1: two nonproportional positive price profiles | Reconstructed | The weighted kernel. Nonproportionality forces all proper-layer coefficients to zero; nonzero terminal penalties detect the remaining all-fail moment. |
| Finite-family numeric/within/cross classification | Reconstructed | Consumer identity must be fixed. In the proportional case, the only extra rows are the two coordinates `(scale, penalty)`; row differences, rather than row rank, govern the cross-comparison consumer. |
| T2: exactly `k−1` added linear queries for full-law repair | Reconstructed, including deterministic adaptive-query lower bound | Minimum-rank old **linear** summary on the full simplex; same law at both profiles; `M>0`; the triangular chain probes have diagonal `ε∏c_i≠0`. |
| T3: known lower moments | Reconstructed | The fiber must contain a full-support law, so its actual affine tangent has the advertised `N_s` dimension. Known low-order coordinates are external information, not newly free memory. |
| A1: `|ε|(2M+1)/[6(M+2)]` | Reconstructed by a different route; later shown attainable coherently at k=3 | Equal old prices, exact old numeric summary, and full law simplex. The matching pair is a uniform two-failure law versus an all-success/all-failure mixture. The planar argument in the follow-up shows that restricting to a compatible coherent law does not increase this radius. |
| A2: finite triple formula and conditional intervals | Reconstructed | Equal-price kernel implies symmetric **differences**, not symmetric populations. Boolean inversion reduces the global question to two level distributions with one common cost expectation; ordinary three-equality LP geometry gives the triple formula. |
| A3: one stopped chain controls all proper moments | Reconstructed | Exact same-population offsets `m_S−m_(P_|S|)` from the old summary; a fixed chain; independent requests drawn from that population; an established fixed-sample empirical-distribution bound. |
| Statistical bounds entering native proofs | No new rule supplied by C4 | Nonempty current source, rational admitted premises or justified rational enclosures, correct context/loss/request binding, and the existing F08 admission/completeness result. Sampling truth and source stability are external assumptions. |

The initial reconstruction contains the actual derivations. The essential kernel is

`v_A=Σ_(r=1)^|A| t_r e_r(c_A)` for proper nonempty `A`,

with a free top direction `v_K`. Its common numeric value is

`Σ_(r=1)^(k−1) e_(r+1)(c_K)t_r+M v_K`.

The sum-zero tangent matters: known first-attempt constants and normalization are free, so taking the rank of unadjusted world-cost rows can overcount. Arbitrary decoding after a linear measurement does not evade the lower bound, because opposite small feasible perturbations along a summary-null direction remain indistinguishable.

## Exact assumption-removal witnesses

These witnesses identify where an enlarged claim would fail. They are **not** counterexamples to the stated theorems, which exclude the relevant cases.

### 1. Allowing zero prices destroys T1 as written

At `k=3`, take `c=(1,0,0)`, `d=(0,1,0)`, and `M=N=1`. They are nonproportional, but no order in either profile observes `m_12`. The first family uses only `1,m_2,m_3,m_23,m_123`; the second only `1,m_1,m_3,m_13,m_123`.

Let `p` assign mass `1/2` to each of `∅,{1,2}`, and let `q` assign mass `1/2` to each of `{1},{2}`. Every old and revised order mean agrees, but their `m_12` values are `1/2` and `0`. The direct numeric rank is 6 instead of 7, and the within/cross ranks are 5 instead of 6. This is a minimal `k` for a nonproportional zero-price pair to break the two-profile conclusion: at `k=2`, nonproportionality already makes the two proper-moment equations independent.

Strict positivity is stronger than the algebra itself needs. The same proof works if every attempt price is merely nonzero, including mixed signs: divide by subset products, and use the final coefficient `e_k(c)=∏c_i≠0` to prove that the common-value functional is nonzero. Thus the relevant degeneracy is zero coordinates, while positive costs retain the intended operational interpretation. The implementation correctly rejects zero or negative attempts under its declared narrower contract.

### 2. Restricted or boundary sources can eliminate the alleged need for repair

For `k=2`, restrict the law to `(1−q)δ_∅+qδ_{12}`, with old `c=(1,1), M=1`. Every old order mean is `1+2q`; one scalar already determines the full law. A single-price edit needs zero extra information, while the unrestricted-simplex calculation would say one. The lower bound must be taken on the actual source.

For T3, set `k=2,s=1,m_1=m_2=0`. The actual fiber is a singleton, so its incremental rank is zero even when `M>0`. The nominal `N_s=1` is not its affine dimension. This is why the full-support hypothesis is substantive. The existing proof and text already state this boundary limitation.

### 3. Query and penalty coverage determine the information target

If `k=3` and only revised orders putting the edited procedure last are requested, every revised-minus-old mean is the same `εm_(K\{j})`. One extra scalar handles those requests; the two-query conclusion is for all new orders or full-law recovery.

If all available penalties are zero, `m_K` is absent from every mean at every attempt-price vector. No amount of price variation recovers the whole law. Conversely, proportional price families can add some information without satisfying T1: their exact count is the rank of the two-column `(scale, penalty)` matrix. Nonproportionality is a clean sufficient condition for full proper-moment recovery, not a substitute for the finite-family classification.

### 4. Feasibility does not establish model or metadata coherence

The cost identity itself is the earliest failure if previous executions change later procedure outcomes. A single order-independent Boolean failure vector then need not exist. A procedure that fails when attempted first but succeeds after another failure cannot be represented by reusing its first-position marginal in every order.

There is also a concrete metadata ambiguity. At `k=2`, let the true law be uniform on all four worlds, the old prices be `(1,1)`, and the true penalty be 1. Both old means are `7/4`; after changing the second price to 2, the chain probe is `9/4`. The distinct feasible law with masses

`p_00=p_11=1/8`, `p_01=p_10=3/8`

has exactly those same observations if the supplied penalty is instead 2. A repair computation with that wrong penalty produces `m_1=m_2=1/2,m_12=1/8`, rather than the true top moment `1/4`. Nonnegativity and normalization cannot expose the mismatch.

Accordingly, `repair_from_chain` is a valid-input mathematical control, not an independent validator of the old profile or unchanged population. The source text's separate request/source-binding requirements must remain attached if these routines enter an operational interface.

## Approximation, coherent laws, and sampling

For equal prices, two laws sharing the exact numeric profile differ by a constant within each Hamming level. Symmetrizing both laws preserves their difference. The global diameter therefore reduces to probability vectors on levels `h=0,...,k` with the same mean of `g_h`. With the two normalizations and one common-mean equation, a maximizing extreme pair uses at most three nonzero masses. This proves A2's triple formula without assuming that the actual population is exchangeable.

At `k=3`, the four triple residuals for singleton moments and the four for pair moments give A1 directly. At `M=4`, the singleton diameter is `1/2`; the pair diameter is `11/51`; the revised numeric minimax radius is `|ε|/4`. The extremal laws have equal old mean 2. They witness a numeric-information lower bound, but do **not** force different optimal order labels. The existing note correctly preserves that distinction.

### Coherence warning is real, but does not refute A2

The existing `k=4,M=1/10,B=9/8` example is exact. With zero within-level contrasts, the individual proper-prefix interval midpoints are

`m_1=41/496`, `m_2=1/48`, `m_3=5/248`.

The old mean then forces `m_4=5/372`, and inclusion-exclusion assigns mass `−3/496` to each specified world with exactly two failures. These coordinatewise optimal answers are not one law.

The later correction in the source is also exact: its displayed coherent level law attains the same largest error `21/496` as the unconstrained decoder. Therefore this example proves that all coordinatewise midpoint optima need not be compatible; it does **not** prove an increased optimal common maximum tolerance. No universal coherent-center theorem, nor a universal positive coherence penalty, follows from the finite searches reported there. The final text makes exactly this limited claim.

### A3 is conditional on the retained offsets and the sampling model

The deterministic identity is `hat_m_S−m_S=hat_P(J≥|S|)−P(J≥|S|)`. The concentration theorem acts only on the one-dimensional stopped-count sample. This legitimately covers all orders, edited indices, and data-selected price queries under the declared total edit bound. It is not dimension-free acquisition of an unrestricted law: the exact old summary has already fixed exponentially many contrasts.

Population mismatch gives an immediate countermodel. Suppose the old population is the deterministic `k=2` world where procedure 1 fails and procedure 2 succeeds. Its stored offset is `m_2−m_1=−1`. If the new population is all-success, every canonical observation gives `J=0`, yet the offset decoder returns `hat_m_2=−1` regardless of sample size. Increasing `n` does not remove this bias. Even with the same population, raw estimates plus exact offsets can fall outside the probability-law polytope; that is compatible with valid coordinate error bounds.

The source already excludes drift, dependence across requests, arbitrary stopping, and free acquisition of old guarantees. It also properly distinguishes a probability bound over fresh samples from a probability bound conditional on acceptance. A reused receipt, feasible fitted source, or native derivation cannot establish those sampling premises by itself.

## Practical discriminator limitation

Independently of the sharp geometry, a one-coordinate edit has pathwise increment between `min(0,ε)` and `max(0,ε)`. An exact old mean plus the midpoint of this interval has error at most `|ε|/2`; an old optimal policy in the same policy family has revised regret at most `|ε|`. These ordinary controls also apply to the stated fixed-level tail/robust objectives via monotonicity and translation equivariance.

For the parameters reported to this reviewer by the F16 contribution audit, `|ε|=1/40`, `M=4`, and `τ=1/20`, the sharp radius is `1/160`, the generic midpoint error is `1/80`, and old-policy regret is at most `1/40`. All are below the reported tolerance. Such a tolerance does not separate the sharp A1 decoder from the generic control, and it cannot show that full-law repair is necessary for that consumer. This arithmetic does not independently certify the experiment's inputs or its native acceptance margin; those belong to the principal's separate F15 audit.

## Fresh arithmetic and code comparison

The supplemental [reconstruct_checks.py](price/reconstruct_checks.py) builds path costs directly from Boolean worlds, implements independent exact rational elimination, and imports **no** existing control module. Its [output](price/reconstruct_checks_output.json) records:

- 48 direct rank-family checks, including positive and mixed-sign nonzero prices;
- 18 known-lower-moment rank checks;
- the explicit zero-price rank/collision witness;
- six `k=3` diameter and attaining-pair cases, including `M=0` as an additional boundary check;
- the incompatible midpoint mass `−3/496` and the coherent common-radius value `21/496`;
- the penalty-metadata ambiguity above.

All exact assertions passed. These finite checks corroborate the written derivations; they do not replace the proofs or establish statistical calibration.

The existing `c4_price_revision.py` matches the declared formulas. Its summary retention is linear even though the subsequent minimum-subtracted residue representation is nonlinear; this does not evade the rank theorem. Its conditional interval enumeration is correct, including single-level and zero-remainder cases, for valid generated summaries. The raw reach-estimate routine explicitly declines to create a confidence claim or a coherent law. Validation and request-binding responsibilities should not be inferred beyond those stated interfaces. No old source edit is needed to repair T1–T3 or A1–A3.

## Contribution boundary for the principal

The defensible application delta is the explicit structure of the price-generated matrix, the two-profile collapse of its proper kernel, the triangular minimum repair, the low-order-information counts, the equal-price exact diameter calculation, and the stopped-chain offset application. Their foundations are established linear algebra, Boolean inversion, partial identification/optimal recovery, finite moment geometry, and empirical-distribution concentration. This review supplies no worldwide-priority evidence and no advantage over an ordinary implementation allowed the same source, probes, and checks.

No failure found here forces abandonment of the narrow mathematical package. Equally, passing this review does not discharge independent novelty, operational-coherence, calibration, or experiment-discriminator obligations.

## Bounded follow-up clarification

[price_assumption_clarification.md](price_assumption_clarification.md) supplies the principal's requested complete mixed-sign algebra, explicitly handles zero or negative sums of attempt prices and vanishing lower symmetric coefficients, and proves which regret/coherence conditions remain necessary. It also derives A1 directly from the stated kernel using an affine residual bound and confirms the exact global specialization `1/160` for the reported `M=4, |ε|=1/40`. This follow-up changes no theorem, runs no new experiment, and makes no priority claim.
