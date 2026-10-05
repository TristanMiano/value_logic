# F15-ND01 independent intervention-algebra audit

Reviewer: ChatGPT (GPT-6 Astra Pro), representation-analysis subagent.
Date: 2026-10-05. Concurrent review adds zero separate root-clock minutes.
Scope: static mathematical review of a post-outcome supplementary derivation,
not another F15/ND01 criterion or an F16 attempt.

Reviewed [`intervention_algebra.md`](../../experiments/F15_ND01_analysis/intervention_algebra.md),
8,464 bytes, SHA256
`36768de5ebaa92f4bdb979178529764021507a50d65540b744601bccbf16a79a`.
No model computations, fitting, or population generation were performed.

**Disposition: all displayed formulas and compatibility signs are correct.**
Three interpretation clarifications are recommended below; none requires a
change to the frozen experiment or any result.

## Repeated masks and overwrite algebra

Writing `T(h)-d=(I-M)(h-d)` immediately gives

\[
T^k(h)=d+(I-M)^k(h-d)
      =h+[I-(I-M)^k](d-h).
\]

At `k=2`, subtracting one application gives exactly
`M(I-M)(d-h)`. For diagonal `m_j in [0,1]`, the effective replacement
fraction is `1-(1-m_j)^k`. The stated limit is correct: coordinates with
positive mask value converge to the donor, while zero-mask coordinates retain
the base. The nominal mass need not remain eight after repeated application.

The logit drift is `v.T M(I-M)(d-h)`. With the defined discovery matrix
`A_ij=v_j(d_ij-h_ij)`, setting `b=m*(1-m)` makes that drift `A b`.
Therefore its mean square is exactly `b.T Q b` for `Q=A.T A/n` in real
arithmetic. This is a drift calculation, so no ideal-target or baseline-error
term needs to be added.

The more general overwrite law has the same obstruction:

\[
T_{M,d_2}T_{M,d_1}(h)-T_{M,d_2}(h)
=M(I-M)(d_1-h).
\]

Thus a binary mask or projector supplies the full-state overwrite law for
arbitrary donors. For fractional masks, cancellation in one scalar output
can make this relation hold on a particular support without full-state
equality. Checking one/two applications only on natural base states does not
automatically establish the law on all states reachable by intervention.

The two-role commutator sign is also correct:
`T1 T0-T0 T1=M0 M1(d1-d0)` for diagonal masks. The corresponding head
effect is its inner product with `v`; nonzero overlap alone need not yield
nonzero observed drift.

## Compatibility in the observable and null components

For mutually orthogonal projectors, `q_r=P_r v` obeys
`q_r.T v=||q_r||^2` and `q0.T q1=0`. Conversely, the stated rank-one
construction gives mutually orthogonal projectors when both nonzero
coefficients satisfy these equations. Zero coefficients can use zero
projectors.

For a declared difference span `D`, write `v=v_D+v_N` and
`q_r=c_r+n_r`, where `c_r=projection_D(a_r)` and `n_r in D^perp`.
Orthogonality of the two component spaces gives

\[
q_r^T v-\|q_r\|^2
=c_r^T v_D+n_r^T v_N-\|c_r\|^2-\|n_r\|^2.
\]

Setting this to zero yields precisely the document's first equation.
Likewise `q0.T q1=c0.T c1+n0.T n1` gives the stated negative sign in
`n0.T n1=-c0.T c1`. Individual feasible null shifts need not solve the
coupled pair condition. Failure of one particular pair of constructed shifts
therefore does not establish infeasibility.

This is exact effective-coefficient feasibility for the declared domain and
geometry. If each role has a different allowed difference domain, using a
common larger `D` is a stronger requirement than matching each role only on
its own support. A discovered null direction is a certified part of the
complement; it need not characterize the complete complement.

## Interpretation clarifications

1. **Distinguish three levels of equality.** Full hidden-state idempotence
   and commutation imply the corresponding algebraic identities after any
   abstraction map, but they are stronger than necessary. A causal
   abstraction requires the appropriate identities *under its intended
   abstraction* on the declared domain. Equality of one scalar output is
   weaker still and need not recover the two abstract cost values. Conversely,
   projector algebra alone does not establish the semantic cost mapping.
   Adding this explicit hierarchy would make the already present output-null
   qualification harder to misread.
2. **Qualify higher-rank extensions.** To preserve both effective coefficients
   and mutual orthogonality, added directions should lie in the common
   orthogonal complement of `v`, `q0`, and `q1`, with mutually orthogonal
   allocations to the two ranges. Orthogonality to the head alone does not
   suffice for an arbitrary enlargement. For example, with `v=(1,1)` and
   `q=(1,0)`, adding the head-orthogonal direction `(1,-1)` expands the
   rank-one range to the whole plane and changes its projection of `v`.
3. **Keep status and outcome wording precise.** Replace “registered
   supplementary reconstruction” with “declared supplementary
   reconstruction.” Specify the metric and comparator in the statement that
   all ten roles improve, and link the saved result record. The numerical
   outcome sentences were not independently checked by this static review.

The proposed later joint-abstraction question is appropriately distinct from
changing F15's 0/5 outcome. Any later experiment still needs semantic target
accuracy, allowed-domain specification, controls, and prospective validation;
the algebra does not supply those empirical conclusions by itself.

Administrative check: an initial naive link regex treated the displayed
factor `[I-(I-M)^k](d-h)` as a Markdown link and raised an assertion. A
math-aware recheck found no missing local links or trailing whitespace.
The mathematical expression and source derivation were not changed.
