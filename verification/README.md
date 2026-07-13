# Semantic verification

This directory is a compact, standard-library Python reference for the finite witness in [`formalism/05a_integration.md`](../formalism/05a_integration.md). It is verification infrastructure, not a neural implementation or a proof-assistant formalization.

The implementation separates request well-formedness (`WF`) from meaningful three-valued atom assessment (`K_3 = {refuted, open, supported}`). Finite meet plus `WF` derives the four public outcomes. Indexed diagnostics retain witnesses, counterwitnesses, obstacles, safety flags, and provenance; there is intentionally no closed reason-code enumeration.

From the repository root, run:

```powershell
python -m verification
```

The command exercises the three-stage integrated witness, the finite Task 14 separation/cardinality countermodels, the Task 14A transport/routing bounds, and all local Markdown links. It uses only the Python standard library. These finite theorem tests are regression witnesses, not a proof-assistant formalization; the proofs are in [`formalism/08_metatheory.md`](../formalism/08_metatheory.md) and [`formalism/08a_transport_routing.md`](../formalism/08a_transport_routing.md).
