# Constant-noise reduction: finite evidence

Codex (GPT-6), October29,2026 UTC. Same-model DEVELOPMENT extension.
The mathematical statement is in [the derivation](noise_hardness.md).

The [a02 result](noise_runs/a02/result.json) passes all six prospectively
specified formulas. The three satisfiable formulas have exact image
[0,1/10] union[19/20,1]; the three unsatisfiable ones have[19/20,1].
All1224 local masks were covered by checked rational extrema or Farkas
certificates. The panel checks27 exact boundary/interior source points,
and verifies the supplied old-feasible source's radius1/100 strict ball
for every formula. Satisfiable cases also check a low-gate strict ball.

The control uses the existing numerical-proposal/exact-certificate producer
and unchanged strict verifier; floating solver success is not the acceptance
criterion. Runtime6,362,402,600ns belongs to the probe and was excluded from
engaged research. There is no speed claim. Complete generated inputs,
certificates and checks are in the lossless JSONL gzip evidence.

The [first attempt](noise_runs/a01/failure.txt) passed the empty formula,
then rejected a new builder's integer coefficient instead of its required
rational string. The [versioned repair](noise_amendment.md) changes only the
new probe, preserves its failed source/freeze, and improves intermediate
evidence retention. It does not change V19 or count as independent confirmation.

a02 records SHA256:
`b1075a919d6043951ea85585461af5cc6632b270828e463aecb3fb19170dc82d`.
a02 freeze SHA256:
`240485395f0ed8786c403045834d2fd09ec62a2f519f5086d0f7baebaaa930d1`.

The proof supplies the asymptotic reduction; these finite cases only support
its implementation and boundary formulas. The constant-noise, known-consistent,
two-component contract is the explicit delta. General piecewise-linear
hardness and complementary Boolean coefficient gadgets are established prior
work, and standalone novelty is not assessed here. This extension does not
raise the fixed V19-R/v1 confirmation probability.
