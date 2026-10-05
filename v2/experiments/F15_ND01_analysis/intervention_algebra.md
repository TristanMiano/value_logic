# ND01: what a joint cost-variable interpretation would require

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05.
Status: supplementary derivation after the registered single-intervention
outcomes. This neither changes the frozen assessment nor adds a new acceptance
criterion to F15 or ND01. The elementary identities below explain a concrete
remaining ambition and a possible later diagnostic. No priority claim is made.

## Setting a variable is stronger than making one useful change

The proposed high-level intervention sets one cost to a donor's value:

\[
H_{0,j}(J_0,J_1)=(j,J_1),\qquad
H_{1,k}(J_0,J_1)=(J_0,k).
\]

These assignments have two familiar properties. Repeating the same assignment
does nothing further; assigning two different variables commutes. In symbols,

\[
H_{r,j}H_{r,j}=H_{r,j},\qquad
H_{0,j}H_{1,k}=H_{1,k}H_{0,j}.
\]

More generally the most recent assignment to one variable overwrites the
previous assignment to it. A causal interpretation of the whole intervention
family should say whether, and to what accuracy, its low-level operations obey
these relations after mapping to its intended abstract variables. Exact
hidden-state equality is sufficient and can be stronger than necessary;
equality of the one scalar output is weaker than semantic equality of the two
cost variables. Individual good counterfactual outputs do not establish the
whole abstraction.
Statistical independence of the two naturally occurring costs is not required
for the algebra; the allowed intervention domain is a separate question.

For the diagnostic's hidden-state operation, write

\[
T_{M,d}(h)=(I-M)h+Md,
\]

where `d` is the donor's hidden activation. An eight-coordinate swap has a
diagonal binary `M`; the fractional intervention has diagonal entries in
`[0,1]`. Both use the original affine output head `z=beta+v^T h`.

## 1. Fractional replacement is generally not idempotent

Applying the same operation twice gives

\[
T_{M,d}^2(h)=h+(2M-M^2)(d-h).
\]

The difference from one application is

\[
\boxed{T_{M,d}^2(h)-T_{M,d}(h)=M(I-M)(d-h).}
\]

Thus binary masks and orthogonal projectors have exact hidden-state
idempotence, since `M^2=M`. A strictly fractional coordinate usually keeps
moving toward the donor when patched again. After `k` applications its
effective replacement fraction is `1-(1-m_j)^k`. This converges to full
replacement on every coordinate with positive `m_j`, regardless of the
original nominal mass of eight. It is a partial replacement operation, not
automatically the operation of setting a stable abstract variable.

The corresponding logit drift is

\[
v^TM(I-M)(d-h).
\]

This can vanish on a particular activation-difference domain despite a
nonzero hidden-state difference. Such output cancellation is a weaker
property than hidden idempotence. A fractional mask's failure of matrix
idempotence alone is therefore not a measured failure of every relevant
output assignment. The actual output drift can be checked using existing
discovery moments: if `A_ij=v_j(d_ij-h_ij)` and `Q=A^T A/n`, its mean squared
logit drift is exactly `b^T Q b`, where `b=m*(1-m)`. This calculation does not
fit a new mask, select another intervention, or generate new examples.

## 2. Diagonal matrices commute; donor assignments can still fail to commute

For diagonal `M0,M1`, direct expansion gives

\[
\boxed{T_{M_1,d_1}T_{M_0,d_0}(h)
       -T_{M_0,d_0}T_{M_1,d_1}(h)
       =M_0M_1(d_1-d_0).}
\]

The matrices commute, but the affine operations have different donor terms.
Disjoint masks make the difference zero. Overlapping masks can overwrite a
shared part of the hidden state in different ways. For a scalar head, the
observable order difference is `v^T M0 M1 (d1-d0)`. It may also vanish through
an output-null or activation-null direction, so overlap count alone is not
an adequate output diagnostic.

The declared supplementary reconstruction checks this identity on an
explicitly labeled combination of the already generated validation arrays.
It is a secondary joint panel, not a new frozen stratum or an independent
confirmatory population. Fractional masks lower mean probability MAE over the
five strata in all ten roles relative to each of the other three mask methods,
yet all five paired fractional operations have observable
order dependence on that panel. This limits the claim that those particular
operations already implement two independently replaceable costs. It does
not rule out another alignment or a different faithful abstraction.

## 3. A common orthogonal representation adds compatibility constraints

Two disjoint subspaces of one orthogonal basis have projectors `P0,P1` with
`P0 P1=P1 P0=0`. Each intervention is then idempotent and the two assignments
commute for arbitrary donors. These are sufficient structural guarantees
rather than performance observations from a finite panel. They do not by
themselves supply a semantic mapping to costs or establish accurate
counterfactual outputs.

For the native scalar head, set `q_r=P_r v`. Each effective coefficient obeys

\[
q_r^T v=\|q_r\|^2,
\]

and the pair additionally obeys `q_0^T q_1=0`. Conversely, nonzero orthogonal
`q0,q1` satisfying the two individual equalities produce compatible rank-one
projectors `P_r=q_r q_r^T/||q_r||^2`. The zero case can use a zero projector.
Larger subspaces can add mutually orthogonal directions in the common
complement of `v,q0,q1` without changing these output coefficients or the
pair's orthogonality, so even these constraints do not identify a unique
internal representation.

The earlier mechanism derivation showed how each fractional coefficient can
be shifted along an activation-difference null direction to satisfy its
individual sphere equality. It did **not** show that the two shifted
coefficients can simultaneously be chosen orthogonal. The particular
constructed coefficients in ND01 are not orthogonal. That construction is
therefore a demonstration of individual output underidentification, not an
executed common-basis DAS solution or a proof that no compatible pair exists.

For clarity, an exact feasibility formulation can be written without choosing
a search method. Let `D` be the span of allowed hidden differences and
decompose `v=v_D+v_N` along `D` and `D`'s orthogonal complement. If the
fractional target effect is `a_r`, its observable component is
`c_r=projection_D(a_r)`. An equivalent coefficient has `q_r=c_r+n_r`, with
`n_r` in the complement. Compatibility requires

\[
\|n_r\|^2-n_r^T v_N
  =c_r^T v_D-\|c_r\|^2,\qquad
n_0^T n_1=-c_0^T c_1.
\]

These are requirements on a pair of unobserved components, not two unrelated
one-dimensional fits. The set `D` must refer to a declared intervention domain.
A finite sample's empirical span can be too small. ND01 instead constructs
a guaranteed null direction from the exact real-valued ReLU function with
the stored binary64 weights on the declared input box, and separately checks
floating-point output equivalence. That stronger domain certificate still
does not imply unique causal interpretation.

## 4. A useful future experiment should test the unresolved joint claim

The next neural ambition should be a separately frozen **ND02 Research90**
chunk, if selected. Its target would be: do unchanged ordinary networks admit
a useful *joint* two-cost abstraction under a common, declared intervention
geometry? It would not retry F15 or change the meaning of its 0/5.

Before any new validation population, the protocol should settle the metric
used for hidden distances, treatment of exactly inactive coordinates, the
subspace ranks, finite optimization budget and discovery selection rule. A
common orthogonal basis gives structural idempotence and commutation; its
ordinary prediction weights remain fixed. Positive hidden rescaling changes
Euclidean geometry, so a normalization rule and transport check matter.

The decisive comparison should include the existing binary and fractional
methods, matched search controls, known-structure calibration, single-role
counterfactuals, repeated assignments and two independent donors. Report
absolute adequacy separately from superiority over an optimized control.
Declare whether joint target cost pairs must be realizable by an ordinary
input, and report any deliberately broader intervention domain separately.
Keep all fitted alignments durable before validation and retain every
prespecified model and failed optimizer.

Additional training or architectural separation would answer a different
question about learning dynamics or inductive bias. It could follow if a
fixed-model joint diagnostic fails, but adding auxiliary cost supervision
would no longer test whether the original ordinary objective spontaneously
provides that organization. A successful intervention result would still
need comparison with alternative causal decompositions and the closest
established methods before supporting a distinctive representation claim.
