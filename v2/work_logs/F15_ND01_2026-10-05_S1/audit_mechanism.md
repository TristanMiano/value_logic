# F15-ND01 independent mechanism-derivation audit

Reviewer: ChatGPT (GPT-6 Astra Pro), representation-analysis subagent.
Date: 2026-10-05. Scope: ND01 mathematical and interpretation review, not F16.
Root timing applies; this concurrent review adds zero separate minutes.

Reviewed document:
[`mechanism_derivation.md`](../../experiments/F15_ND01_analysis/mechanism_derivation.md),
12,202 bytes, SHA256
`5ce3a37df7c92007e4934ef9d97cb2e785b07c8546e2157c697e8251926a029f`.
This records the snapshot inspected; subsequent revisions should be identified
as responses to this review. No trained models, discoveries, or evaluation
populations were run or regenerated. No frozen component was edited.

## Disposition

**No algebraic or sign error found in the displayed derivations.** One
interpretation correction is recommended in the final decision table:
exhaustive logit optimization versus a probability-selected bounded method
does not by itself isolate candidate-search coverage. An additional
clarification about activation-difference nullspaces would strengthen the
already qualified full-coefficient comparison.

| Item | Independent check | Disposition |
|---|---|---|
| Weighted cross-entropy optimum | Strict convexity and `p*=J0/(J0+J1)`; the signed logit decomposition follows. | Correct. |
| Base-error decomposition | Direct substitution gives `zswap-zH=e(base)+r(donor)-r(base)`, for both binary and fractional masks. | Correct, including role-1 sign. |
| Error cross term | Expanding `(e+delta_r)^2` yields both square terms and `2 E[e delta_r]`. | Correct; RMS values alone cannot attribute the total. |
| Quadratic objective and gradient | `Q=A.T A/n`, `c=A.T t/n`, gradient `2(Qm-c)` with `t=zH-z(base)`. | Correct and includes the ordinary base error. |
| Fractional first-order bound | Linear minimization selects eight smallest gradient entries; convexity yields `f(m)-gap <= f* <= f(m)`. | Correct in real arithmetic; numerical records are not interval certificates. |
| Convex hull | Perturbing two interior coordinates excludes fractional vertices; the integer mass excludes exactly one interior coordinate. | Correct. |
| Fractional logit averaging | Affinity in `m` and mixture weights summing to one give a mixture of intervention logits. | Correct; not generally a mixture of probabilities. |
| Projector sphere condition | `a=Pv` implies `a.v=||a||^2`; conversely `P=aa.T/||a||^2` works for nonzero `a`. | Necessary and sufficient for an unrestricted orthogonal projector's full effective coefficient. |
| Fractional sphere deficit | For `a=m*v`, the difference is `sum m_i(1-m_i)v_i^2`. | Correct, and strictly positive with any fractional nonzero-weight coordinate. |
| Gauge caveat | `GPG^-1` is generally not Euclidean-orthogonal after positive diagonal rescaling. | Correct. |
| Two-donor composition | Explicit affine expansion gives `M0 M1 (d1-d0)` in the stated subtraction order. | Correct. |

## I01: match the selection objective before attributing a search failure

The final table currently says that an exhaustive binary improvement over a
bounded search establishes a search limitation on the logit objective. This
isolates candidate coverage only if the bounded candidate pool is also
selected or rescored by the **same discovery logit objective**.

A bounded pool could contain the global logit minimizer and nevertheless
select another mask because its prespecified criterion is probability MSE
or a worst-stratum probability criterion. An exhaustive logit improvement in
that situation is an objective/selection difference, not evidence that the
best logit mask was absent from the pool.

Suggested disposition:

> The bounded procedure left better performance on this logit objective
> unrecovered. Candidate coverage is isolated as the cause only after matching
> the pool's selection objective; otherwise search and objective choice remain
> combined explanations.

The exhaustive-binary versus fractional comparison already uses the same
quadratic and therefore does not have this ambiguity. Its limits concerning
probability error and validation generalization are correctly stated.

## I02: identical observed effects do not require identical full coefficients

Let `D` be the span of the activation differences on a specified pair support.
Two effective coefficient vectors `a` and `q` produce identical logit changes
on that support exactly when

\[
q-a\in D^\perp.
\]

An observationally equivalent orthogonal-projector intervention exists
precisely when the affine set `a+D^perp` intersects

\[
\{q:q^T v=\|q\|^2\}
=\{q:\|q-v/2\|^2=\|v\|^2/4\}.
\]

There is a useful stronger corollary. Every fractional effective vector lies
inside or on this sphere. If `D` is a proper subspace, select a nonzero
`u in D^perp`. The line `a+t*u` starts inside the sphere and eventually leaves
the bounded ball, so it intersects the sphere. At an intersection `q`, the
rank-one construction supplies a projector with identical output effects on
`D`. Thus a strict fractional deficit rules out the *same full coefficient*
but does not exclude projector equivalence on a rank-deficient observed span.

This is a per-role, scalar-output statement. It supplies neither a native
semantic interpretation nor a pair of mutually compatible projectors for
both cost roles. Numerical estimates of an observed span also require a rank
tolerance; finite observations need not span every activation difference that
could occur later. Four raw inputs do not imply hidden-difference rank at most
four, because different ReLU activation patterns can supply additional
linearly independent hidden functions.

The source document already acknowledges the restricted-span issue. Making
the affine-set criterion explicit would prevent a later conclusion that
“fractional succeeds, therefore all orthogonal subspaces fail.”

## Gauge and composition details

After `h'=G h`, the transported projector is `P'=G P G^-1`. It is
self-adjoint under the transported metric `H=G^-T G^-1`, since
`P'.T H=H P'`, even when it is not self-adjoint in the new Euclidean metric.
The document's instruction to declare normalization/metric and transport
rules is therefore justified. Coordinate-mask invariance alone would not
validate the proposed subspace experiment.

For donor composition, expanding the two orders gives

\[
T_1T_0(h)=(I-M_1)(I-M_0)h+(I-M_1)M_0d_0+M_1d_1,
\]

\[
T_0T_1(h)=(I-M_0)(I-M_1)h+(I-M_0)M_1d_1+M_0d_0.
\]

Diagonal matrices commute, so the linear terms cancel. The remaining terms
are `-M0 M1 d0 + M0 M1 d1`. The reported positive coefficient of `d1-d0`
is correct. Overlap permits order effects; it does not force them for every
donor pair or every scalar head.

## Additional static solver review

At the relaxation agent's request, `project_capped_simplex` and `fit_mask` in
[`soft_mask.py`](../../experiments/neural_diagnostic_v1/soft_mask.py) were read.
The bisection direction and bracketing, gradient step with
`L=2*lambda_max(Q)`, direct residual objective, first-order gap, lower-bound
direction, and final feasibility checks agree with the derivation. The
explicit `certified_interval_arithmetic=False` and false probability/validation
lower-bound flags correctly limit the numerical claim. This was a static
review, not execution or an independent numerical verification of outcomes.
