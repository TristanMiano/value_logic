# Asymmetric harness v1.1 amendment

DEVELOPMENT only; zero principal-clock credit. Saved after the first public
execution and before the replacement execution or private scoring.

The initial frozen matrix produced all 57 complete successful policy episodes.
The public comparison then failed because fresh in-memory receipts retained
tuple claim keys while reused reference receipts had JSON list claim keys.
The completed saved JSON records pass all three planned public check groups,
including every raw/normalized path comparison. This is a harness representation
mismatch, with no changed policy action or inference from private scoring.

Retain the initial directory `development/asymmetric_v1` and preserved harness
`reviews/source_revisions/asymmetric_development_run_v1.py`. The original
harness hash is
`715436a0cb77c3d60fde8e51986468033299c80e851e75688040568ea4ee1649`.
The archived 57 public records hash is
`4c56983e46fc93094b2c2035894a9e519821787bf42a77e236956a870c003a88`.
The public-only failure/replay record hash is
`796311dbd781673acb8e06787747888ac195caf8d15a5abb7994166c9971fe3b`.
No private reference answers were read and no private score was produced for
that attempt.

The v1.1 harness compares each record after parsing its exact saved JSON
representation. It also versions itself and retains this amendment in the
public seal. It changes no policy source, procurement tariff, public input,
price, seed, action, scoring formula, or matrix member. Execute the original
57-record matrix again in a new `development/asymmetric_v1_1` directory, with
45 fresh policy executions and the same 12 provenance-bound symmetric reuses.
The new public records must seal before separate private scoring.
