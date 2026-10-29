# Focused audit outcome and its limits

Codex (GPT-6), October 28, 2026. Same-model DEVELOPMENT.

The predeclared 13-case panel passed on its first execution. The unchanged
s19 verifier accepted 143 bounded-slice and 24 empty-slice certificates across
local dimensions 1--7, including mixed dimensions, affine offsets, a
lower-dimensional segment, a 400-digit constant objective, and inconsistent
observations. The independent assignment combiner agreed with every returned
range. All 37 reconstructed rational sources satisfied the original supplied
polytopes, receipts and target value. All 114 targeted mutations were rejected.

The noisy-envelope example returned, after reversing the minimum/maximal-value
sign convention, exactly [43/40,221/200] union [11/8,281/200]. Seven direct
joint band-feasibility checks agreed, using 42 LP calls including rejected
witness assignments. Thus the ordinary exact control ties on the stated
consistency duty. The maximal-cover example returned [-1,0], confirming that
retaining only the two maximal constrained slices would lose valid values.

The producer used SciPy/HiGHS only to propose numerical primal/dual supports.
Every emitted optimum or infeasibility ray was reconstructed and checked in
rational arithmetic; a numerical infeasibility status was insufficient. The
separate verifier then rebuilt all local rows from the original caller's
problem and checked the complete certificate. Direct-band evidence retains
the per-assignment primal or Farkas records, including failed assignments.
There were no producer failures or host-instability retries in this run.

Panel totals: 40,036 compact-JSON certificate bytes; 3.1399615 seconds of
certificate production and 0.04733 seconds in the unchanged verifier. These
are single-run measurements on the recorded Windows/Python/SciPy environment,
include cold-start effects, and exclude other interpretation/query work.
They are not a speedup claim, a certified runtime bound, or a comparison with
an optimized MIP implementation. Source/witness and complete artifact bytes
are additional; the compact certificate count is not the total repository
or memory bill.

The result addresses an implementation-support gap left by the old mainly
two-dimensional producer. It is still a small structured panel, with numerical
proposal machinery and exact checking developed by the same model. Neither
the case count nor corruption rejection rate gives a calibrated probability
of correctness. The generic soundness argument in reconstruction.md remains
the basis for the mathematical claim. No novelty estimate is inferred from
these tests, and no extra random panel is needed absent a new defect or risk.

Evidence: audit_plan.md, audit_freeze.json, audit_inputs.json,
audit_records.jsonl and audit_results.json. Executed versions are preserved;
lp_witness.py is a fail-closed developmental producer, not a claim of a complete
polynomial-time exact LP implementation.
