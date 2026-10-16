# From a proposed-policy certificate to a robust policy mixture

Codex (GPT-6), DEVELOPMENT derivation. This extends `robust_flip.md` rather
than starting a fresh candidate family. Conventional minimax-regret planning
and double-oracle/constraint-generation methods supply the general machinery.

## Fixed source interface and randomization order

Keep known query-cell masses p_z, independent conditional-mean intervals,
fixed query and flip fees, and at most H operations on each policy path.
A reasoner chooses a distribution alpha over admissible deterministic policies,
privately draws a policy before execution, and follows it. The source is fixed
before that draw and cannot depend on its realized private randomness.
The target is

```math
\min_\alpha\max_{\mu\in[l,u]}
 \left\{\sum_\pi\alpha_\pi V_\pi(\mu)-V^*(\mu)\right\}.
```

This is expected regret over the policy draw and source outcomes. It is not
a pathwise guarantee for every selected policy. If nature sees the draw before
choosing the source, the quantifier order changes and randomization need not
help. The comparator V* uses the true mean table under the same paid menu and
operation cap; its extra knowledge is part of this retrospective benchmark.

## Two inexpensive best-response oracles

For each full query cell, a policy is summarized by a fee and terminal sign
coefficients. Mixing policies simply mixes these rows. Coefficients can now
be any values in [-1,1], and expected fees are nonnegative. The fixed-policy
regret derivation never required its proposed coefficients to be extremal:
the endpoint support calculation and comparator recursion remain exact for
these averaged rows. Thus the existing robust oracle returns an attaining
single mean table against any finite policy mixture. Its comparator remains
deterministic, since at a fixed source randomization cannot improve an expected
cost minimum.

Conversely, let nature mix over mean tables mu^k with weights beta_k. For
any deterministic policy, expected cost is affine in those means because
query-cell masses are the same in every table. Therefore

```math
\sum_k\beta_k\{V_\pi(\mu^k)-V^*(\mu^k)\}
 =V_\pi\left(\sum_k\beta_k\mu^k\right)
  -\sum_k\beta_k V^*(\mu^k).
```

The best policy response is ordinary compact query/flip planning at the
averaged mean table. It need not enumerate policies or a full hidden-state law.
This identity would need modification if query-cell masses also varied: one
must average unnormalized cell moments and masses together, not average
conditional means independently. It fails if operation semantics or prices
vary in a way omitted from the source.

## A checked gap, even with an untrusted matrix-game solver

Maintain finite banks of policies and source scenarios. Their regret-payoff
matrix gives a small zero-sum game. A numerical LP proposes mixed strategies.
Convert each to a valid rational probability vector, preserving all original
numerical output separately when relevant. Then compute

```math
U=\max_\mu\{V_\alpha(\mu)-V^*(\mu)\},
\qquad
L=\min_\pi\sum_k\beta_k\{V_\pi(\mu^k)-V^*(\mu^k)\}.
```

The two oracles compute these quantities exactly under the declared contract.
Weak duality gives L<=optimal minimax regret<=U. This certificate does not
require trusting the numerical LP's optimality report. Add the returned source
and policy to their banks and repeat. Stop only when the exact gap U-L is
within the declared tolerance, or retain an unfinished gap at a resource cap.
Clipping/normalizing numerical weights must be disclosed; it creates valid
strategies whose actual gap is checked, not an assertion that the LP was exact.

The finite policy and endpoint-source sets imply finite termination for exact
restricted-game solutions with fresh best responses. This does not give a
polynomial iteration bound. An approximate LP can stall at an existing response;
report that rather than inferring convergence. The cost includes every oracle,
matrix entry, LP solve and retained policy, not just final execution.

## Useful scope and comparison

Regan and Boutilier's minimax-regret and constraint-generation constructions
already establish the general program. Our possible delta is a concrete pair
of compact exact oracles for paid informative queries plus cardinality-bounded
counterfactual flips, including arbitrary within-cell dependence and fallible
conditional means. The dependence on the number r of queryable coordinates is
exponential; the many unqueryable coordinates enter by sums and ranked gains.
This is a tractable parameterized specialization, not universal superiority
over ordinary robust planning or a new decision criterion. Source acquisition,
valid interval coverage and useful application remain open.

Prospective screen: three small structured/random instances and one moderately
larger source, at most 40 iterations, exact oracle gaps, and a tiny case whose
minimax mixture can also be enumerated directly. Preserve nonconvergence and
compare with ordinary midpoint planning and immediate terminal action 0.

## Initial capped implementation

`robust_game.py` and `rg01` preserve all four first attempts; none failed.
The one-bit analytic case gives exact minimax regret 1/2 versus 1 for either
pure action. The three-bit case already has a zero-regret midpoint policy.
The five-bit/two-query case reaches equal rational lower and upper values
26055/44608 in three iterations, versus midpoint regret 135/136.
These are exact oracle certificates within the supplied interval model.

The 31-bit/three-query case reaches the prospective 40-iteration cap rather
than the requested 1/100000 gap. Its final upper is about 5.402505 and lower
about 5.041044; midpoint regret is 239/30, about 7.966667. The feasible mixed
policy therefore reduces certified worst-case regret by about 32.19% against
this named midpoint control, with a remaining optimization gap about 0.361462.
It is not an exact solved optimum and not a comparison against every ordinary
robust method. The final restricted game has 41 policies and 42 scenarios;
the cap record includes additional newly proposed bank entries after its last
strategy, so use the recorded per-iteration bank lengths when reconstructing.

The first probability conversion approximates each numerical LP weight by its
own rational and then normalizes. This is valid but creates denominators as
large as 308 bits in the last mixture, despite the original million-denominator
per-entry approximation. A common probability grid can avoid this avoidable
representation cost. Any amended implementation must preserve the first run,
recompute its own exact gap, and report precision-induced stalling if present.

The closer Gilbert-Spanjaard comparison makes the ordinary ancestry explicit:
their Observation 4 is the same mean-source best response, and their section 4
is the same double-oracle skeleton. Their binary independent-cost adversary is
a strong specialized antecedent. Here signed terminal coefficients and the
shared terminal-zero option couple a binary expansion's costs; the direct
query/flip oracle treats that structure explicitly. Whether this restricted
extension is a worthwhile moderate novelty needs further source comparison.

The explicit `robust_game_grid.py` amendment uses largest-remainder rounding
on a common denominator 2^20. All four repeated duties finish on their first
attempts (`rg02`). The final 31-bit mixture uses at most 21-bit numerators and
denominators, with exact upper 45319457/8388608 and lower
422872649/83886080. The remaining gap is 30321921/83886080. It still reaches
the 40-iteration cap; bounded representation does not imply solved optimization.
The small game cases retain the declared gap tolerance. Compare their newly
checked gaps, not the original solver's exact rational optimum label.
