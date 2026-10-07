# What compatible individual edits imply about joint error

Contributor: ChatGPT (GPT-6 Astra Pro), October 5, 2026.

This is a bounded supplementary interpretation derivation selected after ND01
outcomes within its Research90 allowance. It adds no fitted alignment, saved
network forward, population or validation method score. It does not begin
ND02 or F16. The equations specialize elementary affine-head and norm
identities; no general-method novelty or worldwide-priority claim is made.

## 1. Compatible operations and semantic accuracy are different requirements

Write the ordinary hidden state as `h(x)`, the native logit as
`z(x)=v^T h(x)+beta`, and the desired ordinary logit as
`z*(x)=ell0(x)+ell1(x)`. For the actual task,
`ell0=log J0` and `ell1=-log J1`.

Let `P0,P1` be orthogonal projectors with `P0 P1=0`. Replacing role `r`
with donor `dr` means `h <- h+Pr(h(dr)-h)`. Idempotence makes repeated
replacement by the same donor stable. Mutual orthogonality makes the two
donor assignments commute. Starting at base `b`, their joint result is

```math
h_{01}=h(b)+P_0(h(d_0)-h(b))+P_1(h(d_1)-h(b)).
```

Define `phi_r(x)=v^T Pr h(x)`, `r_r=phi_r-ell_r`, and
`e(b)=z(b)-z*(b)`. Then

```math
\epsilon_{01}=z_{01}-[\ell_0(d_0)+\ell_1(d_1)]
=e(b)+[r_0(d_0)-r_0(b)]+[r_1(d_1)-r_1(b)].
```

If `epsilon0` and `epsilon1` denote the individual intervention errors for
these **same** base and donor choices, the equivalent identity is

```math
\boxed{\epsilon_{01}=\epsilon_0+\epsilon_1-e(b).}
```

This shows exactly what the whole-box output-equivalence witnesses establish
and leave open. Their individual effects agree with existing masks on
ordinary base/donor states; their joint effect combines those two changes
additively. It need not equal either order of the original fractional edits,
whose overlapping fractional replacements also change intermediate states.
Neither individual matching nor low-level commutation alone proves that the
sum agrees closely enough with both intended cost assignments.

## 2. A valid error bound requires the same distribution and the right scale

For any one probability distribution on triples `(b,d0,d1)` and any `p>=1`,
the triangle inequality gives

```math
\|\epsilon_{01}\|_p
\leq\|\epsilon_0\|_p+\|\epsilon_1\|_p+\|e(b)\|_p.
```

All terms must use the triple distribution's actual marginals. Separate
role-conditioned samples are not automatically those marginals. This matters
for ND01's secondary panel, which combines already generated arrays without
claiming a registered joint distribution. Its published per-role averages
cannot simply be inserted as if that assumption had been verified.

Since the logistic function has derivative at most `1/4`, a corresponding
probability-error bound is `E|p01-pH01| <= E|epsilon01|/4`, also at most
`||epsilon01||2/4`. This direction of conversion is valid. Small individual
probability MAEs do not by themselves supply equally small logit norms:
the inverse logistic derivative is large near zero and one. Near-boundary
decision errors also need their own margin/distribution treatment.

A uniform bound on all three logit errors would support a uniform joint
bound by the same identity. Exact individual correspondence on every input
and donor, together with exact ordinary correspondence and common compatible
projectors, would imply exact joint correspondence. The present approximate,
conditional, finite diagnostic has not established those stronger premises.

## 3. Even uniform single-edit probability tolerance need not transfer intact

Consider the deliberately simple algebraic example

```math
t\in[0,4/25],\quad h(t)=(t,t,2t),\quad
v=(1,1,-1),\quad\beta=0.
```

Let both high-level log contributions be zero. Every ordinary logit is
exactly zero, so ordinary probability is the exact target `1/2`. Choose
role projectors onto the first and second coordinates. They are disjoint,
idempotent and mutually commuting. A single edit has logit `td-tb`, hence
absolute logit at most `4/25` **for every base and donor in the interval**.
Both single-role probability errors are therefore at most approximately
`0.039915`, below `.05` uniformly.

Set the base to zero and both donor values to `4/25`. The joint logit becomes
`8/25`, with probability error approximately `0.079324`, above `.05`.
Ordinary error is zero; the two same-signed isolation errors accumulate.

The threshold comparison can be checked without rounded exponentials. For
`0<=x<1`, `exp(x)<=1/(1-x)`, so at `x=4/25` the single-edit error is at most
`1/23 < 1/20`. At `x=8/25`, `exp(x)>=1+x`, so the joint error is at least
`2/29 > 1/20`. The displayed decimal values are illustrative evaluations;
the two rational inequalities prove the tolerance crossing.

This example is **not one of the five F15 networks**, a meaningful new
cost-structure calibration, or a newly evaluated scientific arm. Its constant
high-level costs intentionally isolate the error-budget issue. The inactive
extra coordinates could extend each rank-one projector to rank eight without
changing these effects. It refutes an automatic inheritance of the same
absolute tolerance from individual edits to their combination, even with
perfect ordinary outputs and compatible operations. It does not assert that
every jointly fitted alignment must fail.

## Consequence for the proposed continuation

ND02, if separately selected, needs a declared joint target and population,
an error budget or acceptance rule for combined assignments, and jointly
compatible low-level operations. It should preserve ordinary-error and
single-role diagnostics so a joint negative result can be interpreted.
The whole-box compatibility certificate is useful preparation for asking
that question; it does not replace the question with a geometric pass.
