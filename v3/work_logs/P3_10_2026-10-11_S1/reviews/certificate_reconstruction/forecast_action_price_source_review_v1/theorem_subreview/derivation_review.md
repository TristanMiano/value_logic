# Source/math review: forecast and action price sensitivity

Reviewer: **ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction/decision_rank_information**, 2026-10-11.
Reviewed draft: `v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_derivation.md`, SHA-256 `c4055022904b258beccd3b1e71259d807bd72604cbaea464431ddd8ccb4fa266`.
Scope: source-only mathematical review before observer execution. No saved-summary data were read, and no scientific code, paid method, scorer, analyzer, generator, or truth evaluator was run.

**Disposition: fixed-record algebra and weak-feasibility method pass; strict feasibility requires an additional exact step if a catalogue-wide strict conclusion is intended.**

## 1. Scalarization and half-planes

The comparison `K_c-K_o=a+lambda*d-mu*g` is correct for the defined positive gaps. Strict improvement against that one witness is exactly `mu>(a+lambda*d)/g`; equality is a tie. The full-catalogue weak inequalities have the correct signs:

`(C_c-C_o)*lambda+(B_c-B_o)*mu <= W_o-W_c`.

These are conditional statements about exact, consistently normalized, fixed saved records and the declared comparator roster. This source review does not verify empirical gap signs, denominators, completeness, or the roster's contents.

## 2. Weak feasibility and vertices

A nonempty closed finite half-plane intersection inside the nonnegative quadrant has a vertex. Given any feasible point, restricting to a no-larger `lambda+mu` sublevel gives a nonempty compact set and hence an attained minimum. Its minimizing face is compact; an extreme point of that face is extreme in the full feasible set. In two dimensions a vertex has two linearly independent active boundary normals, including axes where necessary. Pairwise boundary intersections followed by all-constraint checking therefore suffice for weak feasibility.

Zero normal vectors are constant constraints, not lines. Parallel and coincident boundary pairs have zero determinant and must not be divided by; their inequalities still participate in feasibility. A point, segment, ray, or unbounded polygon is admissible. Nonemptiness is not the same as a positive-area region.

## 3. Exact elimination and certificates

Write a row as `A*lambda+B*mu <= b`. A positive `B` gives the upper bound `(b-A*lambda)/B`; a negative `B` gives that expression as a lower bound. Include `mu>=0` among the lower bounds and `lambda>=0` among the retained one-variable constraints. For a lower row `i` and upper row `j`, the exact eliminated row is

`(B_j*A_i-B_i*A_j)*lambda <= B_j*b_i-B_i*b_j`.

It is the sum of row `i` multiplied by `B_j>0` and row `j` multiplied by `-B_i>0`. Thus it carries a nonnegative-multiplier contradiction certificate. Retain these multipliers and original row identities if the output claims an independently checkable certificate.

For a resulting row `k*lambda<=h`, positive `k` gives an upper bound, negative `k` a lower bound, and `k=0` is either a tautology (`h>=0`) or an immediate contradiction (`h<0`). After rejecting constant contradictions, feasibility is exactly `L<=U`, allowing an unbounded upper endpoint. If there is no upper bound on `mu`, choose it at least as large as the finite maximum of its lower bounds. Therefore “empty endpoints” should explicitly include constant contradictions and unbounded endpoints.

## 4. Strict improvement is not decided by weak vertices alone

**S1 qualification:** inspecting slacks only at the enumerated weak vertices cannot establish that strict improvement is impossible or that only ties exist. For example, the weak region `1<=lambda<=2, mu>=0` has vertices `(1,0)` and `(2,0)`, each tied with one defining ordinary inequality, while `(3/2,0)` is strict against both. This is a symbolic counterexample to a proposed inference, not a new empirical fixture or executed experiment.

If a returned point has positive slack against every ordinary row, it is a valid strict witness. Failure of that check at all returned weak vertices is inconclusive. A complete strict test can introduce a common margin:

`A_o*lambda+B_o*mu+epsilon <= b_o` for every ordinary row, with `lambda,mu>=0` and `epsilon>0`.

An optional cap `epsilon<=1` preserves existence of a positive margin. Alternatively, exact Fourier–Motzkin elimination can retain strict inequalities and open endpoints. Either method must distinguish a proved lack of strict feasibility from “no strict witness found among weak vertices.” Axes remain weak inequalities: zero prices are permitted even for a strict comparison against every ordinary method.

## 5. Scope and gates

The draft correctly treats the extra Brier weight as post-outcome descriptive sensitivity, keeps the executed frozen objective and practical flags unchanged, and acknowledges that changed acquisition prices could produce different trajectories. Excluding optional reporting fees is an explicit service choice; it does not create a comparison of equal paid reporting services. The unknown-prefix accounting restriction and identical-ordinary-kernel boundary remain in force.

Principal Research90 credit: **0 seconds**. No P3-11, recurrence, or contribution/novelty assessment is made. Any later observer-source review will be preserved as an additive artifact.
