# Focused certificate and prediction audit

Codex (GPT-6), October 28, 2026. DEVELOPMENT, before new execution.

Question: does the unchanged s19 rational verifier implement the reconstructed
contract for mixed local dimensions, affine offsets, degeneracy, empty slices
and the new scalar-measurement duty? Its old polygon panel is not a generic
high-dimensional producer audit. This probe addresses that concrete limitation;
it is not a further random pass rate used as a novelty estimate.

Use a new producer in `lp_witness.py`: floating LP solves propose primal/dual
supports, but exact rational row identities, feasibility and matching bounds
must validate every emitted certificate. Failure to reconstruct is an explicit
producer failure, never evidence of infeasibility. Infeasibility needs a
nonnegative Farkas vector checked against the original rows. The unchanged
s19 verifier imports no optimizer and remains the acceptance authority.

Prepare a fixed small panel with 1--7 dimensional local polytopes, including
mixed dimensions, rational invertible coordinate changes, constant objectives,
lower-dimensional sets, inconsistent observations, and the noisy max-affine
example. Save and hash the input JSON and all executed sources before the
first run. New data and checks remain developmental, even after hashing.

For each case, produce certificates for every indexed local slice. Compare
the returned complete range with an independently written exhaustive assignment
combiner over the certified local extrema. Reconstruct sources at every final
endpoint and midpoint, checking the caller's original rows, observations and
future minimum directly. For the small worked duty, additionally compare with
direct joint band-feasibility LPs. Retain numerical proposals, exact acceptance
counts, production/checking time and certificate bytes. These are machine
measurements of this panel, not a general performance benchmark.

Targeted mutations will challenge input binding, affine offsets, missing
slices, false empty faces, mismatched dimensions, changed primal/dual entries,
and deleted or enlarged range components. Do not treat rejection counts as
statistical reliability. The mathematical soundness proof is load-bearing.

Budget: implementation and interpretation approximately 25--45 E minutes;
expected unattended execution at most a few minutes, excluded from research.
Preserve a failed version and output before any deterministic repair. Retry
an unexplained host failure unchanged at most once, with its reason recorded.
Do not repeat the frozen s19 panel or tune inputs to improve outcomes.
