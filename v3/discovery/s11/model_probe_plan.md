# One combined-model implementation screen

Codex (GPT-6), DEVELOPMENT; declared before output. Test the joint algorithm
from model_selection.md on three 512-request, six-variable streams: seeded
independent bits with probability 0.4, all-one worlds, and all-zero worlds.
Stop after the first positive bit or after all six queries. Fees are
(1,3,2,4,1,2). The last two streams are boundary mechanisms, not applications.

Use exactly three forecasters, supported only at the first edge: zero; the
optimal baseline IF both first possible queries certify; and half the maximum
fee. All predictions use only known fees and pre-execution probabilities.
They receive no world or unpurchased answer. Do not retune after exposure.
Compare a zero-baseline learner with the same outer gamma/eta and sampling
seed. This is an implementation ablation, not the strong service benchmark.

Check the pathwise small-loss score inequality and signed matching-weight
inequality, enumerate the 13 matchings to check probability normalization and
every 32nd round's conditional estimator mean, and record all truth purchases.
The independent evaluator may read complete generated worlds for these
diagnostics; those are explicitly validation reads, never learner receipts.
Save model weights, fee totals, matrix work, score arithmetic and source hashes.
Use existing Python 3.12 and at most two unchanged retries per case. No inference
of an expected-regret theorem from one realized trajectory is permitted.
