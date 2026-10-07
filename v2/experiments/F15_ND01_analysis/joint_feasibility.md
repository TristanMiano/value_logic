# Exact joint feasibility of existing intervention effects

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05.
Status: optional supplementary derivation, selected after the ND01 outcomes
within its Research90 allowance. The question concerns existing masks; no new
alignment fit, validation population, scientific endpoint or F16 work is added.
This is a local algebraic specialization, with no worldwide-priority claim.

## Question and domain

Can two existing fractional-mask output effects be reproduced exactly by
orthogonal projectors onto two mutually orthogonal subspaces, for **all base
and donor inputs in the declared input box**? This is stronger than matching
only the observed finite validation pairs. It is also different from asking
whether some other jointly fitted alignment has acceptable approximate
cost-intervention behavior.

The metric is the native Euclidean metric on hidden activations. Exact
statements concern the real-valued ReLU function whose coefficients are the
stored binary64 numbers, interpreted as rational numbers. Floating-point
execution is a separate numerical approximation. Positive coordinate
rescaling changes this metric and can change the feasibility question.

## 1. Certifying the complete activation-difference span

Let `h_j(x)=max(0,w_j^T x+b_j)` on a box with nonempty interior. Classify each
unit by its exact affine minimum and maximum on that box. A variable unit has
strictly negative minimum and strictly positive maximum, so its kink
hyperplane intersects the box interior. Suppose the variable units' affine
hyperplanes are pairwise distinct.

If `sum_j a_j h_j(x)` is constant on the whole box, consider a variable unit
`j`. There is an interior point on its hyperplane lying on none of the other
finitely many distinct hyperplanes. In a sufficiently small neighborhood,
all other units are affine with fixed activation state. Crossing the chosen
hyperplane changes the gradient of the sum by `a_j w_j`. Constancy and
`w_j!=0` force `a_j=0`.

Only always-active affine units and inactive units can therefore participate
in a constant relation. The active coefficients must satisfy
`sum_j a_j w_j=0`; biases affect the constant but not activation differences.
Inactive coefficients are unrestricted. Consequently, for the span `D` of
all vectors `h(d)-h(b)` in the box,

```math
\dim D=\#\{\text{variable units}\}
        +\mathrm{rank}(W_{active}).
```

The previous mechanism analysis only used this expression as an upper bound.
Pairwise distinctness of the interior kink hyperplanes supplies the matching
lower bound. Hyperplane equality is tested by normalizing the rational vector
`(w_j,b_j)` by its first nonzero entry, so opposite orientations of one
hyperplane count as the same hyperplane. If that prerequisite fails, the
present certificate does not claim the rank formula.

For ND01's models there are at most one always-active unit. If its weight is
nonzero, it contributes full rank one. Under the unique-kink condition,
`D` is then precisely the coordinate subspace outside the inactive units.
This last specialization must be checked, not inferred merely from a low
dimensional input space: nonlinear ReLU features can have a high-dimensional
linear span even with four inputs.

## 2. Individual output-equivalent projector coefficients

Write `v=v_D+v_N`, with `N=D^perp`. For a mask `m_r`, the observable
coefficient is `c_r=projection_D(m_r*v)`. An output-equivalent coefficient
is `q_r=c_r+n_r`, where `n_r` lies in `N`.

There exists an orthogonal projector with `P_r v=q_r` exactly when

```math
q_r^T v=\|q_r\|^2.
```

The nonzero case uses `P_r=q_r q_r^T/||q_r||^2`; the zero case can use a zero
projector. Define

```math
\delta_r=c_r^T v_D-\|c_r\|^2,\quad
t=\tfrac12\|v_N\|,\quad
\rho_r=\sqrt{\delta_r+t^2}.
```

For the coordinate-subspace `D` just certified and a fractional mask,
`delta_r=sum_{j in D} m_rj(1-m_rj)v_j^2>=0`. Each admissible null component
lies on the sphere

```math
n_r=\tfrac12v_N+\rho_r u_r,\qquad\|u_r\|=1.
```

The degenerate zero-radius case is interpreted as a point.

## 3. Two spheres give an exact compatibility condition

Mutually orthogonal projectors require `q0^T q1=0`. Set
`C=c0^T c1>=0`, so the remaining condition is `n0^T n1=-C`.
Assume `dim N>=2`, as must be checked for the models.

Let `w=v_N/2`. A point on the first sphere can have every norm

```math
x\in[|\rho_0-t|,\rho_0+t].
```

For fixed `n0`, the smallest dot product with the second sphere is

```math
n_0^T w-\rho_1\|n_0\|
=\tfrac12(x^2+t^2-\rho_0^2)-\rho_1 x.
```

This convex quadratic is minimized at
`x*=clip(rho1,abs(rho0-t),rho0+t)`. The maximum dot product over both spheres
is `(t+rho0)(t+rho1)`, attained when both radial directions agree with `w`
(or any common direction when `w=0`). The product of two spheres in dimension
at least two is connected, and the dot product is continuous. Its attained
values fill the entire interval between the extrema. Thus the pair exists
**if and only if**

```math
\boxed{C\leq\kappa,
\qquad \kappa=-\tfrac12((x^*)^2+t^2-\rho_0^2)+\rho_1 x^*.}
```

Here the upper endpoint is nonnegative, so the only constraint on the
nonpositive target `-C` is the minimum. A point sphere is handled directly;
the same formula remains valid.

Since `delta0,delta1>=0`, each `rho_r>=t`. An equivalent form convenient for
exact classification is

```math
\kappa=\begin{cases}
(\delta_0+\delta_1+t^2)/2,& |\rho_0-\rho_1|\leq t,\\
(\rho_{small}+t)(\rho_{large}-t),& |\rho_0-\rho_1|>t.
\end{cases}
```

The first branch is decided using rational arithmetic:

```math
(\delta_0+\delta_1+t^2)^2
\leq4(\delta_0+t^2)(\delta_1+t^2).
```

In the second branch, square-root enclosures can be obtained with integer
square roots. For rational `r>=0` and integer `Q=10^60`, set
`k=isqrt(floor(r*Q^2))`; then `k/Q<=sqrt(r)<(k+1)/Q`.
Interval arithmetic yields certified rational bounds on `kappa-C`.
If those bounds straddle zero, report unresolved rather than rounding a
verdict. No numerical optimizer is needed.

## 4. Meaning of a result

A feasible pair establishes existence of compatible **output-effect**
coefficients for the two existing masks in this metric and domain. Nonzero
orthogonal coefficients give rank-one projectors. In the 32-dimensional
space, those projectors can be extended to disjoint rank-eight subspaces by
allocating seven additional mutually orthogonal directions to each in the
common complement of `v,q0,q1`, whose dimension is at least 29. The additions
do not alter the effective head coefficients.

This preserves the single-role output effects on the declared input box and
guarantees the low-level idempotence/commutation algebra. It does not prove
that their abstract variables equal the intended costs, that a unique native
representation was recovered, or that a future approximate joint test passes.
The native-metric choice and possible inactive-coordinate participation
remain material interpretation limits.

An infeasible pair rules out exact reproduction of *these two mask effects*
by any such disjoint orthogonal-subspace pair over the whole box. It does not
rule out different effects, approximate correspondence, a different metric,
other nonlinear interventions, or every cost representation. No frozen
success criterion is changed by either result.

## 5. Saved-weight results

The first calculation completed successfully. All five models satisfy the
prerequisites. Their exact activation-difference ranks are **30,30,29,29,29**;
the nullspaces are exactly the **2,2,3,3,3** inactive coordinate directions.
All **2,003** variable-hyperplane pairs are distinct. In every one of the 20
mask-pair calculations the central branch applies, so each feasibility
decision uses rational arithmetic without square-root rounding.

| Existing mask effects | Feasible model indices | Infeasible model indices |
|---|---|---|
| Original F15 | 0, 3 | 1, 2, 4 |
| Exhaustive binary | 0, 1, 3, 4 | 2 |
| Rounded fractional | 0, 3, 4 | 1, 2 |
| Fractional | 0, 2, 3, 4 | 1 |

Fractional feasibility margins `kappa-C`, in index order, are approximately
**0.006255, -0.039148, 0.019951, 0.017598, 0.039064**. The exact rational
inputs and margins are preserved in [joint_feasibility.json](joint_feasibility.json).
The calculation performs zero model forwards, fits, optimizer calls or
population generations. It does not select a replacement model on validation.

Thus the independently applied fractional masks fail to commute, while
compatible projectors reproducing their individual effects exist in four
networks. There is no contradiction: output agreement on ordinary base/donor
states leaves the behavior on already patched intermediate states
underdetermined. This is a concrete reason to distinguish the individual
interchange relation from the whole intervention algebra.

## 6. Native Euclidean feasibility is not gauge invariant

Suppose an inactive coordinate has nonzero head weight. Rescale that ReLU
unit by a positive factor `g`, multiplying its incoming weights and bias by
`g` and dividing its head weight by `g`. Its activation remains zero on the
whole box. Ordinary outputs and transported coordinate-mask effects are
unchanged, but the stored Euclidean head norm in `N` changes. If all inactive
coordinates use the same factor, `t^2` changes to `t^2/g^2`; the observable
`delta0,delta1,C` do not change.

For sufficiently small unrestricted `g`, the central branch holds and
`kappa=(delta0+delta1+t^2/g^2)/2` can exceed any fixed finite `C`. Therefore
the existence of a compatible Euclidean projector pair can change under a
function-preserving inactive-unit gauge. This argument assumes a nonzero
inactive head component and at least two null directions. It does not claim
that every gauge used in F15 has this effect or change any saved network.

Conversely, if interventions are restricted to the noninactive coordinate
space, its certified difference span is full. There is then no hidden-
difference null direction to absorb a coefficient change. A strictly
fractional coefficient with positive sphere deficit cannot be matched exactly
by an orthogonal projector in that restricted space, even for one role.
Approximate performance of a different projector is not determined by this
exact statement.

These two observations strengthen the reason for fixing activation geometry
and the treatment of inactive directions in any subsequent ND02 protocol.
They do not license choosing the metric after validation to obtain a pass.
