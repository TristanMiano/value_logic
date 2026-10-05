# F15-ND01 independent joint-feasibility audit

Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
Concurrent review adds zero separate root-clock minutes. This is not F16.

**Verdict: PASS; 3,625 checks, 0 failures.**

The saved output, source, mechanism result, preparation manifest, five source
networks and five soft-mask preparations have matching hashes and bindings.
The audit uses exact rational arithmetic on saved binary64 parameters and masks.
No model forwards, input populations, fits, projection searches, or numerical
optimizers were run.

## Independent prerequisites and arithmetic

The affine extrema were computed by a sign-based formula independently of the
source's corner enumeration. All 160 unit classifications agree. All
**2,003 pairs of interior variable-unit kink hyperplanes** are
distinct, verified via their rational 2-by-2 minors rather than the source's
canonical normalization. Exact active-weight ranks have full column rank.
The complete activation-difference ranks are
**[30, 30, 29, 29, 29]** and their
nullspace dimensions are **[2, 2, 3, 3, 3]**.
Each nullspace is exactly the coordinate subspace of the inactive units, with
dimension at least two. These establish the stated two-sphere prerequisites.

All twenty masks fall in the exact rational central branch. Independent
computation of `c.v - c.c`, observable role overlap, inactive head energy,
the branch discriminant, cancellation capacity and margin agrees exactly with
every saved rational value. Float display values and all dispositions agree.
No square-root enclosure helper was needed.

| Existing mask method | Feasible | Infeasible |
|---|---:|---:|
| frozen_original | 2 | 3 |
| binary_global | 4 | 1 |
| rounded_top8 | 3 | 2 |
| fractional_mask | 4 | 1 |

For the fractional masks specifically:

| Model index | Disposition | Exact-margin decimal display |
|---|---|---:|
| 0 | feasible | 0.006254956891 |
| 1 | infeasible | -0.039148074608 |
| 2 | feasible | 0.019951334173 |
| 3 | feasible | 0.017598436914 |
| 4 | feasible | 0.039063649874 |

## Meaning and limits

The kink argument is applicable because each variable affine hyperplane crosses
the box interior and can be locally crossed away from all other distinct
hyperplanes. A constant linear combination of activations therefore has zero
coefficient on every variable unit. Full active-weight rank leaves only inactive
coordinates in the difference nullspace.

For the compatible-projector question, the sphere-dot-product minimum yields
the saved central capacity `(delta0 + delta1 + t_squared)/2`. The admissible
dot-product range is connected in nullspace dimension at least two, and its
upper endpoint is nonnegative. Thus comparing that capacity to the nonnegative
observable overlap decides the exact existing-effect feasibility question.

These are exact statements about the real-valued ReLU function with stored
binary64 coefficients treated as rationals, over the entire declared input box,
in the **stored native Euclidean hidden metric**. Positive rescaling changes
that metric and can change feasibility while preserving ordinary network outputs
and transported coordinate interventions. The numerical dispositions should
therefore not be presented as gauge-invariant facts about semantic features.

A feasible pair establishes existence of compatible output-effect coefficients
for these particular masks. It does not establish semantic joint cost adequacy,
an identified native representation, a successful future approximate alignment,
DAS/ND02 execution, or new F15 support. The infeasible fractional model rules out
exact matching of those two particular effects in this metric/domain, not every
approximate or differently parameterized joint representation.

Machine-readable evidence: [audit_joint_feasibility.json](audit_joint_feasibility.json).
