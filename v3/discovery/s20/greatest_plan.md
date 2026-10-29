# Greatest-point shortcut: prospective development panel

Codex (GPT-6), October29,2026 UTC. Separate DEVELOPMENT control.
Freeze proof, implementation, runner, input builder and dependencies before
execution. Use fresh attempt directories and retain all failures.

The panel uses the deterministic inputs built by greatest_inputs.py: seven
feasible cases covering zero receipts, one block, unequal dimensions, ordinary
coupling with max-closed rows, exact observations, constant future response,
and tied outside witnesses; plus one missed-receipt inconsistency and one
empty-block inconsistency. The builder emits rational strings and uses seeds
only to choose small coefficients, not to select favorable results.

Compare the shortcut against a newly generated complete local-mask certificate
checked by the unchanged s19 verifier. Check every shortcut primal/dual proof,
range equality, and rational endpoint/third/midpoint witnesses directly against
the original base constraints, receipts and future readout. Inspect the forced
mask formula against a separate outside-block loop, especially ties and n=1.

Count actual scipy.optimize.linprog calls separately for shortcut and full
local-mask control. Feasible shortcut inputs should use2n calls; an empty LP
may require an extra Farkas proposal. Record producer refusal as failure, not
emptiness. LP counts are not fees or wall-time benefits; both methods include
their certificate work, and the ordinary same shortcut ties.

Negative controls reject a two-positive base row, a positive receipt slope,
a negative future slope, incorrect digest, missing peak/lower proofs, wrong
range, altered primal or dual, false missed-receipt claim and invalid query.
Verify copied-input isolation. Preserve the triangle, negative-observation and
negative-future counterexamples in the derivation; do not silently broaden
the code contract after seeing these outcomes.
