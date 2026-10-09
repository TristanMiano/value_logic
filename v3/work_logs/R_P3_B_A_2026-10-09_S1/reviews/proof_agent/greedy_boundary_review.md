# Independent verification of the greedy-action boundary

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Separate same-model, nonblind mathematical review. This checks the argument
in `development/bounded_state_design.md`, SHA-256
`e23fbfd3cc488ce94b43d6ccc9eb2835af2f76a3b8ad2ab40b968ac0998a5a08`,
and adds a corresponding witness for the actual four public experts.
Reviewer time adds zero principal credit; P3-08 is not started.

**Verdict: the design's counterexample is correct.** The forecast-to-action
conversion is a load-bearing part of the theorem. Replacing the proved
randomized action by deterministic minimization of the forecasted two-action
loss does not preserve the expert-relative paid-action guarantee.

## 1. The supplied two-expert witness

Use two constant experts, block size $`b=4`$, $`K=3`$ and eight blocks.
Every answer within a block is identical, and the block answers alternate
$`1,0,1,0,1,0,1,0`$. Resolve a forecast tie as action zero.

At the start of each two-block pair, equal weights give probability one-half
to action one. Greedy loss minimization chooses zero and is wrong on the
three unbought rounds of the label-one block. The purchased label changes
weights from a common multiple of $`(1,1)`$ to that multiple of $`(2,3)`$.
The next probability is $`3/5`$, so greedy chooses one and is wrong on the
three unbought rounds of the label-zero block. The next update gives a common
multiple of $`(6,6)`$, restarting the same pattern.

Consequently, greedy terminal task loss is $`8\cdot3=24`$. Each fixed
expert loses 16 on the full tape; greedy regret is 8. The imported randomized
allowance would be $`9\log2<6.3`$, so it is violated. In contrast, the
ideal randomized policy's expected loss per pair is

```math
3\left(\frac12+\frac35\right)=\frac{33}{10},
```

giving $`66/5`$ over all eight blocks, exactly as the design claims.

Uniform query selection introduces no qualification here: every selected
position in a block reveals the same label. The tape is completely exogenous;
it never reacts to the random choices. Independent modular computation
confirms the proposed realizations $`1^8\bmod17=1`$ and
$`3^8\bmod17=16`$.

The supplied witness uses two experts. The current whole-service executable
uses four public experts, so the original example should not be described as
a failed run of that four-expert program.

## 2. A witness within the current four-expert service

Use the admitted Euler queries $`p=17,a=2`$ and $`p=17,a=6`$.
The evaluator independently finds

```math
2^8\bmod17=1,\qquad 6^8\bmod17=16.
```

Both queries give the same public expert-action row

```math
(0,1,\text{odd-base},\text{lower-half-base})=(0,1,0,1).
```

Thus the four experts form two equal-size groups following the two constant
actions. With exact product weights, the aggregate probabilities again
alternate between $`1/2`$ and $`3/5`$. Use sixteen four-round blocks,
alternating the two queries, with fresh public request identities if desired.
Greedy is wrong on all 48 unbought rounds. Every fixed expert loses 32 on the
full tape. Greedy regret 16 exceeds $`9\log4<12.6`$.

The same exact integer calculation was also carried out with fixed-state
precision $`s=16`$ and action precision $`h=16`$, using the reviewed
normalization map. It still chooses the wrong greedy action on every block.
The admitted normalization and action-rounding allowances are much smaller
than the separation.

| Policy/state comparison | Greedy task loss | Best fixed full-tape loss | Greedy regret | Randomized expected task loss | Safe upper bound being incorrectly imported |
|---|---:|---:|---:|---:|---:|
| Supplied two-expert, exact state, 8 blocks | 24 | 16 | 8 | $`66/5`$ | $`63/10`$ |
| Current four-expert row, exact state, 16 blocks | 48 | 32 | 16 | $`132/5`$ | $`63/5`$ |
| Current four-expert row, $`s=h=16`$, 16 blocks | 48 | 32 | 16 | $`1730145/65536`$ | $`225534771/17895424`$ |

The final upper bound is approximately 12.603 and includes both
$`144/65535`$ of state allowance and $`48/65536`$ of action allowance.
The logarithm bound is rigorous without floating-point evaluation:
$`e^{7/10}>1+7/10+(7/10)^2/2+(7/10)^3/6>2`$, hence
$`\log2<7/10`$ and $`\log4<7/5`$.

[The exact probe](greedy_boundary_probe.py) and its
[saved output](greedy_boundary_probe.stdout.json) retain all probabilities,
greedy actions, modular checks and inequalities. These are mathematical
policy comparisons, not a new frozen evaluation or a change to the actual
controller, which continues to sample its action as proved.

## 3. Consequence for the next implementation stage

The proved policy samples action one with the issued mixture probability.
Greedy minimization of the forecasted binary losses instead chooses action
one only when that probability exceeds one-half. This nonlinear conversion
changes the sequential policy and invalidates the particular averaging and
potential readout used by the guarantee.

For P3-08, the existing theorem therefore attaches to the specified stochastic
policy. A greedy value optimizer can be a separate method, but its guarantee
must be proved for that policy or its results must retain their empirical
scope. Encoding the same forecast as expected losses does not automatically
transport every guarantee through the subsequent optimizer.

This is not evidence that greedy reasoning is generally inferior. The
counterexample is directed at a universal theorem transfer. Ordinary exact
computation and semantic caching can solve these repetitive finite queries
cheaply, and those controls remain available. A valid pointwise probability
model would also pose a different decision problem from the adversarial
fixed-tape expert comparison used here. The useful result is the precise
policy boundary to preserve during integration, not a recommendation to
exclude alternative policies or a decision to begin their implementation.
