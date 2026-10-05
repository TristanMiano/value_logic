# F15-ND01 independent joint-semantic-error derivation audit

Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
Concurrent review adds zero separate root-clock minutes. This is not F16.

**Verdict: PASS.** All 16 recorded symbolic/rational/illustrative checks pass,
and the independently reviewed general identities and qualifications are sound.

Reviewed source: `v2/experiments/F15_ND01_analysis/joint_semantic_error.md`
(5751 bytes), SHA256 `c3b797c2943145173c8549ad48636ab3c609790b8768761d57ee92329903ca4b`.

For common orthogonal projectors with zero cross product, expanding the two
affine replacements removes both cross terms. Each individual logit error is
`e(base)+Delta r_role`; the combined logit error is therefore exactly
`epsilon0+epsilon1-e(base)` for the same base and donor triple. Minkowski's
inequality then supplies the stated Lp upper bound for p>=1. The norm terms
must use one triple distribution's marginals. Separate role-conditioned
averages cannot be substituted without checking that requirement.

The logistic conversion is in the correct direction: probability absolute
error is at most one quarter of logit absolute error; averaging and then
L1<=L2 give both displayed bounds. Small probability error alone gives no
uniformly small inverse-logit error. The distinction between compatible edits
and semantic approximation is consequently justified.

The toy counterexample checks exactly. Its ordinary logit is
`t+t-2t=0`. The single-edit logits are `donor_t-base_t`, uniformly bounded in
absolute value by 4/25. With base 0 and both donors 4/25, the joint logit is 8/25.
Monotonicity and sigmoid reflection justify using the positive endpoint for
all single-edit absolute errors. The exponential bounds give

- Single-edit error <= **1/23 < 1/20**, with exact margin **3/460**.
- Joint-edit error >= **2/29 > 1/20**, with exact margin **11/580**.

These rational inequalities establish the tolerance crossing without rounded
exponentials. The illustrative errors 0.039915 and 0.079324 also round correctly.
The first and second coordinate projectors are disjoint and idempotent, so the
counterexample retains perfect ordinary outputs and compatible low-level
operations. Padding with inactive coordinates supplies disjoint rank-eight
extensions if desired, without changing the argument.

The example deliberately uses constant high-level costs. It demonstrates that
the same approximate single-edit tolerance need not survive combination; it
does not establish failure of every joint alignment or provide another neural
calibration result. The source correctly labels it as a toy algebraic example,
not one of the saved five models, ND02 execution, F16, or new F15 support.

No models, populations, fits or optimizers were run. This audit leaves the
source and every prior artifact unchanged.

Machine-readable details: [audit_joint_semantic_error.json](audit_joint_semantic_error.json).
