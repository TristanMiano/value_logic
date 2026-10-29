# Matching and incidence finite development screen

Codex (GPT-6), October 28, 2026. Prospective, before first execution.
This supports a separate development branch and does not confirm frozen V19.

Check three specific risks in the new derivations:

1. Enumerate every perfect matching for n=1,...,8 in the prescribed weighted
   complete graph. Compare its distinct minimum values with (n-1)^2+1 and
   retain an attaining permutation for each value. Compare those witnesses
   with a separate residual-threshold augmenting-path matching routine.
2. For n=1,...,4 enumerate exact rational vertices of every noisy singleton
   local polytope (eta=epsilon=1/(100*n^2)). Compare its minimum and maximum
   with a closed form derived from its constraints. Enumerate all matching
   branch intervals and check the asserted number of positive-width output
   components. This is finite rational evidence; the general proof remains
   the written derivation.
3. For n=1,...,4 and k=0,...,4 compute the exact rational rank of differences
   of all ordered-partition incidence vectors. Compare the stated piecewise
   affine-dimension formula, including empty receipts and one/two blocks.

The code and the four derivation/comparison files are frozen by SHA256 before
execution. This probe uses only the Python standard library, with no floating
point LP or existing V19 range routine. Limit one run to120seconds. Preserve
all outputs and failures. One unchanged retry is allowed for an unexplained
host failure; deterministic discrepancies require a versioned correction and
preservation of the first attempt. Do not rerun successful outputs unchanged.
The run itself is wait time; implementation and result analysis are E.
