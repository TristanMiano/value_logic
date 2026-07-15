# Semantic verification

This directory is a compact, standard-library Python reference for the finite witness in [`formalism/05a_integration.md`](../formalism/05a_integration.md). It is verification infrastructure, not a neural implementation or a proof-assistant formalization.

The implementation separates request well-formedness (`WF`) from meaningful three-valued atom assessment (`K_3 = {refuted, open, supported}`). Finite meet plus `WF` derives the four public outcomes. Indexed diagnostics are a disjoint sum retaining exactly the applicable witness, obstacle, or counterwitness plus safety flags and provenance; there is intentionally no closed reason-code enumeration. Missing evidence is an open diagnostic, while an omitted diagnostic record makes a purported well-formed fixture invalid.

From the repository root, run:

```powershell
python -m verification
```

The command exercises the three-stage integrated witness, the finite Task 14 separation/cardinality countermodels, the Task 14A transport/routing bounds, the Task 14B typed-footprint and audit-repair witnesses, the Task 14C proof-carrying-plan and stratified-assessment witnesses, the Task 15 encoding-contract regressions, and all local Markdown links. It uses only the Python standard library. The Task 14C suite checks payload erasure, path-sensitivity grade propagation, typed energy/latency aggregation, independently registered certificates, actual root-license lifting through the kernel, grounded base sources, cycle rejection, and unique strict-rank evaluation. The Task 15 suite checks dependency-scoped projection and explicit missingness, shared-scorer candidate equivariance, sparse/dense comparison counts, checker-sensitive typed-DAG isomorphism, and joint-sufficiency counterexamples. These finite theorem/interface tests are regression witnesses, not a proof-assistant formalization; the proofs and contracts are in [`formalism/08_metatheory.md`](../formalism/08_metatheory.md), [`formalism/08a_transport_routing.md`](../formalism/08a_transport_routing.md), [`formalism/08b_audit_repairs.md`](../formalism/08b_audit_repairs.md), [`formalism/08c_proof_carrying_plans.md`](../formalism/08c_proof_carrying_plans.md), and [`ml/01_encodings.md`](../ml/01_encodings.md).
