# Source review: expected-loss and repair-rank scope

Reviewer: **ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction/decision_rank_information**.
Scope: §§1 and 3–5 of the preserved decision-service interpretation, SHA-256 `8e9c2766a7ed6f4239139e55befe682aff124db0a229fbdd318dcee3a68738a9`. Source-only review. The parent reviewer owns the saved conformance-table and numerical reconstruction checks.

**Disposition: the mathematical distinctions pass. Two probability-scope clarifications and one rank-type clarification would make the interpretation more precise.** No changed endpoint, new execution, or numerical reconstruction is needed.

## 1. Pure minimax and shared expectation

Conditional on the displayed two-state loss table, fallback is the unique pure minimax action. Its expected loss is 3 under every normalized law, while the smaller of the two specialized expected losses is at most 2. It therefore cannot be Bayes-optimal under any law on this exact retained state set and deterministic action menu. This conclusion is appropriately local to the declared menu and state semantics.

The final paragraph of §1 correctly rejects `(4,4,3)` as a common expected-loss vector in known units. The cited sum-to-4 identity uses the known scale and offset convention. The frozen theorem additionally permits three shared nuisance contracts, all covered by `v=s Lp+b 1`, with `s>0` and unrestricted common `b` when unknown. A compact argument excludes the robust vector under all four:

\[
v_{\mathrm{fallback}}-\frac{v_{\mathrm{take\_p}}+v_{\mathrm{take\_r}}}{2}=s>0,
\]

because the corresponding base-loss contrast is the constant 1 on both states. The robust vector gives `3-(4+4)/2=-1`. **T1 recommendation:** append this contrast, or explicitly limit the existing sum-to-4 argument to known units. The common positive scale premise must remain explicit; unrestricted action-specific transformations are outside the frozen contract.

Source support: frozen `02_probability_information.md`, §§2–5 and §10, PI-1/2/10; frozen `02_finite_information_audit.py`, module contract, `effective_rows`, and `target_certificate`.

## 2. What the observation theorem supplies

The observation premise is required before applying the identification theorem. It does not itself guarantee the requested target is identified. For a nonconstant scalar target `c p`, the global full-simplex criteria for `n>=2` are:

| Calibration | Effective observation | Exact target criterion |
| --- | --- | --- |
| Known scale and offset | `Lp` | `c` belongs to `row([1;L])` |
| Unknown common offset | `Dp` | `c` belongs to `row([1;D])` |
| Unknown positive common scale | `s Lp` | both `1` and `c` belong to `row(L)` |
| Unknown positive common scale and common offset | `s Dp` | both `1` and `c` belong to `row(D)` |

Here `D` consists of differences from one reference loss row; the nuisance offset is unrestricted. Constant targets need no observation. Restricted source families, local fibers, and decision-only sufficiency require their separately stated criteria. The frozen theorem expressly does not classify arbitrary nonlinear value encodings.

**T2 recommendation:** replace §5's “Q5 obtains exact probability information only from its separate shared expected-loss observation map” with: “Q5's finite identification theorem applies to its separately declared shared expected-loss observation map, under the stated calibration assumptions and the requested target's fiber/rank criterion.” This avoids suggesting either automatic full-law recovery or an impossibility theorem about other encodings.

## 3. Loss transformations and difference certificates

Section 3's invariances are correct. A shared positive scale and constant offset commute with maxima and preserve the pure minimax ordering. A common state-dependent offset preserves same-state differences and fixed-law expected-loss ordering, while it can change absolute minimax ordering. A fixed-pair uniform inequality is invariant because the offset cancels pointwise; positive scaling preserves its sign. A positive upper bound supplies no nonpositive difference certificate. These claims match the existing discussion in frozen `02_probability_information.md`, §10; no new policy equivalence is being inferred.

## 4. Sourcewise rank and incumbent domain

Sourcewise argmin is preserved by an order-preserving affine recoding, and the frozen worker retains all tagged source/minimum pairs before choosing one action. Cross-source minimization introduces a comparison absent from that quantifier. The invariance proof therefore passes when the feasible source domains, loss table, action menu, and unresolved-source family are held fixed.

**R1 type clarification:** the general repair rank is a lexicographic vector. State `r_s:X_s -> Q^{k_s}`, and write `r'_s(x)=a_s r_s(x)+b_s` with `a_s>0` a scalar and `b_s` a fixed vector of the same dimension. The first differing coordinate keeps its sign, and equal ranks remain equal. For a one-tier source these are ordinary scalar formulas. If a source is infeasible, recoding does not create a useful-action warrant.

The separately deployed incumbent service is explicitly one-tier scalar. For a **checked feasible** incumbent `w`,

\[
Q_r(w)=\{x\in X:r(x)\le r(w)\}
      =\{x\in X:a r(x)+b\le a r(w)+b\}=Q_{ar+b}(w).
\]

Every rank minimizer is in this sublevel, but nonoptimal points may also be included. Optimality of `w` is unnecessary; its feasibility and the fixed hard domain are necessary. The draft correctly keeps transformed-encoding admission, request identity, paid costs, and fresh binding separate from this mathematical equality. This is not a multi-tier implementation or a transport-cost theorem.

Source support: `04_counterfactual_semantics.md`, §4; `04_selection_extensions.md`, sourcewise families and CE04-6; frozen `p308_structural.py`, `ordinary_rank`, `solve_ordinary`, `solve_candidate`, and `choose_fixed_action`; frozen `05_equal_certificate_delivery.md`, §1; frozen `05_counterfactual_transport.py`, `Frame`; `05_counterfactual_transport.md`, §3 and its lexicographic warning.

## Provenance

`source_bindings.json` binds the reviewed draft and ten preserved sources. `signature.json` binds this signed review and manifest. No generator, scorer, paid method, official analyzer, truth evaluator, or experiment was run. All work was read-only apart from new artifacts inside the assigned review directory. Principal Research90 credit: **0 seconds**. No P3-11 or novelty assessment is made.
