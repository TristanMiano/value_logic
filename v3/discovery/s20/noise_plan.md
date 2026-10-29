# Prospective finite reduction check

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT extension, separate from A1.

Check that the constant-noise reduction in noise_hardness.md actually encodes
its claimed complete future image when fed through the existing independent
LP-certificate producer and unchanged exact verifier. Freeze this plan,
derivation, input builder/probe, literal formula inputs, LP producer/helpers,
and verifier before the first optimizer call. Save the complete generated
instances and certificates, compressed losslessly, in a fresh attempt.

Six fixed cases: no old variables/no clauses; one positive unit clause padded
to three literals; contradictory positive/negative units; all four possible
two-variable clauses padded by repeating their last literal; all eight
three-variable clauses; and the same list with one clause removed. Boolean
truth tables are an independent semantic control for the formula, not a
replacement for checking the encoded real source. All masks are included in
the LP certificates, including infeasible masks. Compare exact ranges to H3.

Check the supplied old-consistent source and its radius1/100 ball by rational
row margins and receipt witnesses. On satisfiable cases check explicit source
points at q=0,1/20,1/10; on every case check q=19/20,39/40,1. This tests the
construction and boundary formulas beyond a yes/no floating LP answer.

Budget60 seconds, expected10--35 seconds. Exclude unattended execution from
research. Preserve the first failure; repairs require new versioned attempts.
Do not rerun a passing unchanged panel. This is six finite cases, not a
verification of the complexity theorem or an empirical performance comparison.
