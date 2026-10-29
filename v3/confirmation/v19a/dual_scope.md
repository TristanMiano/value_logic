# Optional certificate-algebra reconstruction unit

Codex (GPT-6), October28,2026. Prospective scope, before first compilation.
Part of P3-11-A1; the frozen candidate and its verification event are unchanged.

Specific remaining assurance boundary: the Python checker verifies exact
column identities, nonnegative multipliers, primal inequalities and endpoint
equalities. Its real-domain soundness relies on finite-sum linear algebra
and order reasoning that has so far been reconstructed in prose. Formalize
that algebra over an arbitrary ordered commutative ring, rather than only
testing rational sample points.

The new Lean unit should prove finite-dot-product linearity, the identity
between a weighted sum of rows evaluated at x and the weighted sum of their
values, weak dual upper/lower bounds, Farkas exclusion, and the attained-bound
consequence when a feasible primal point matches a bound. It imports the
standard Lean algebra/order classes and proves its finite-sum lemmas. It
must contain no added axioms, omitted proofs, unsafe declaration or oracle.

This is not a proof of LP dual existence, compactness, rational bit bounds,
JSON parsing, the actual Python loops, every row constructor, full AR1 or
the entire service. Those obligations retain their separate evidence. No
new test population or empirical usefulness claim is introduced.

Before each compiler attempt, preserve its exact source and runner bytes,
scope hash and a STARTED record. Use the already recorded official Lean4.35.0
runtime with a60second per-attempt cap; bracket execution as wait time.
Preserve every compiler output and deterministic defect. Repairs are explicit
new supplemental proof attempts, not replacement scientific candidate runs.
One unchanged retry is available for an unexplained host failure. After a
pass, seal the successful source and result and do not rerun it unchanged.
