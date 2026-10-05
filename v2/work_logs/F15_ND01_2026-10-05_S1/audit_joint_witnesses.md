# F15-ND01 independent joint-witness audit

Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
Concurrent review adds zero separate root-clock minutes. This is not F16.

**Verdict: PASS; 452 checks, 0 failures.**

The artifact contains **13 witness pairs, comprising 26 stored projector
matrices**. Their model/method identities match exactly the feasible cases in
the independently audited rational classification: original 2, exhaustive
binary 4, rounded 3, and fractional 4. The seven infeasible cases have no
witness pair. All source, input and preparation hashes agree; the previously
audited joint-feasibility derivation snapshot remains unchanged.

## Matrix checks

Using independent compensated scalar sums, this audit recalculated every
matrix square, both cross-product orders, all native-head products and all
coefficient dot products. It verified symmetry, idempotence, mutual
orthogonality, the rank-one formula and unit trace, the projector sphere
equation, and agreement with the selected mask's output coefficient outside
the exact inactive-coordinate nullspace. The saved coefficient null components
also lie on the stated spheres. Recorded errors agree up to float64 summation
differences; every independent residual is below 1e-12.

| Independent quantity | Maximum absolute error |
|---|---:|
| symmetry_max_abs | 0.000e+00 |
| idempotence_max_abs | 1.110e-16 |
| head_binding_max_abs | 1.110e-16 |
| observable_binding_max_abs | 1.110e-16 |
| constructed_coefficient_observable_max_abs | 0.000e+00 |
| sphere_equality_abs | 1.110e-16 |
| rank_one_formula_max_abs | 5.551e-17 |
| trace_one_abs | 1.110e-16 |
| cross01_max_abs | 1.897e-17 |
| cross10_max_abs | 1.897e-17 |
| coefficient_orthogonality_abs | 1.171e-17 |

The constructor was read but not imported or rerun. Its central-branch choice
places the first null component at the proved minimizing norm; the second is
chosen on its sphere to cancel the observable overlap. The saved matrices
directly verify the resulting identities, so this audit does not depend on
repeating that choice algorithm.

## Scope

These are numerical witnesses for a separately proved exact **existing-output-
effect** feasibility condition in the stored native Euclidean metric. They
exploit inactive-coordinate freedom. Their matrix algebra supplies compatible
idempotent/commuting interventions, while the observable coefficients preserve
the original masks' single-role output effects on the declared input box.

They are post-outcome algebraic constructions, not newly learned semantic
features, a new confirmation of F15 support, or a demonstrated joint cost-
adequacy result. No populations, model forwards, fits, optimizers, witness
construction reruns, or new validation scores were performed by this audit.
Native-metric feasibility is not gauge invariant. ND02 and F16 remain unstarted
by this work.

Machine-readable details: [audit_joint_witnesses.json](audit_joint_witnesses.json).
