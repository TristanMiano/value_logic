# Learn a correlation model from paid partial observations

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
Prospective constructive redirection from the independent-source learner.
Likelihood-ratio confidence, finite model selection, Markov inference and
robust policy evaluation are imported ordinary tools. The proposed work
connects them to an actually paid repair-acquisition service and explicitly
accounts for the observation policy, rather than treating selected marginal
frequencies as an adequate source model.

## Why the preceding source contract matters

The [finite correlation screen](correlation_counterexample.json) considers
all equal-probability complementary extreme/middle pairs on paths n=2..7,
with unit query fees. On n=5, the pair (0,0,0,1,0) and (1,1,1,0,1), each with
probability one-half, has the same one-half extreme marginal at every vertex
as the independent source. Here 0 means an extreme cost value and 1 means
middle. The policy compiled for the independent source predicts fee 15/4,
but its actual mean under this pair source is 4. Analogous n=6 and n=7
examples give 37/8 versus 5 and 87/16 versus 6. Marginal calibration alone
does not supply the conditional probabilities required by the invoice proof.
These are conditional computations; they bought zero physical audits.

The cost receipt still determines a correct repair. This failure concerns
the **resource forecast** used to select purchases, not logical output validity.
A useful bounded reasoner should learn this distinction from relevant joint
observations, and pay for retaining and evaluating that joint information.

## Finite correlated source menu

Let the extreme/middle indicators along a path be a stationary symmetric
two-state Markov chain. The initial indicator is fair; a neighbor repeats the
previous indicator with probability rho. Given an extreme indicator, the
actual cost is 0 or 2 with equal probability, independently of the other
extreme labels. A middle indicator gives cost 1. Every new request draws a
fresh chain under one fixed but unknown parameter from a prospectively
declared finite menu, initially rho in {1/10,3/10,1/2,7/10,9/10}.

All menu members have identical marginal extreme frequencies, but different
joint behavior. The cost-source family and truthful sensor are admitted
premises, not facts learned merely by fitting the menu. The possibility that
the actual law lies outside the menu remains an explicit limitation.

The zero-regret action duty and original exactly-one CNF remain unchanged.
All ternary values have positive support at every vertex for these parameters.
Query selection may depend on earlier requests and current paid receipts.
The likelihood must therefore use each queried coordinate's conditional law
given the earlier observed coordinates under each candidate model. Multiplying
unconditional marginal frequencies would erase the very correlation being
learned and is invalid for this adaptive observation process.

## A common model confidence set under adaptive acquisition

For each model k let L_k(t) be the likelihood of the actual observed receipt
sequence through time t, conditional on the predictable query choices. The
query policy's own randomization law is shared across models and cancels.
Fix positive prior weights pi_k before acquisition and define

```math
M_t=\sum_k\pi_k L_k(t),\qquad
\mathcal C_t=\{k:L_k(t)\geq\alpha M_t\}.
```

If model k is the actual source, M_t/L_k(t) is a nonnegative mean-one
likelihood-ratio martingale (or supermartingale for a subprobability mixture).
Ville's inequality gives probability at most alpha that k ever leaves the
set. There is no extra union over k: exactly one fixed true model is being
covered, and the guarantee is valid for each possible true member. Taking
intersections of past sets is also safe on the same event. This is standard
mixture likelihood inference, not a new confidence theorem.

Parameters and likelihoods can be exact here. With rho numerators over ten,
a partial indicator pattern on a length-n row has likelihood Z_k divided by
2*10^(n-1), where Z_k is an integer obtained by two-state forward summation.
The denominator is shared by every candidate. Across completed rows, retain
integer relative likelihood weights, normalize by their common gcd, and
multiply by the next row's Z_k. Within a row, use the **previous rows'**
weights times the current partial Z_k, rather than multiplying nested partial
likelihoods repeatedly. Uniform pi gives the exact membership comparison
K*L_k >= alpha*sum_j L_j. Bit growth and inference work must be billed.

## Policy evaluation must retain boundary information

Under a known Markov model, conditioning on an observed interior indicator
separates left and right unobserved intervals. A remaining interval's law
depends on its observed boundary indicators, not just its length or marginal
probabilities. A forced middle boundary and an extreme boundary generally
give different conditional predictions. A proposed policy can therefore use
states (a,b,left boundary,right boundary), with absent boundaries at physical
path ends. Conditional probabilities come from forward/backward Markov
messages or exact matrix powers. This inference is part of the bill.

A fixed policy can be evaluated separately under every retained model and
receive the maximum expected-fee upper bound. For a first implementation,
freeze the selected policy/model set at the start of each request and update
the cross-request model evidence after the checked output. This avoids
claiming a free within-request replanning guarantee. The action still adapts
to actual extreme/middle receipts along its fixed conditional policy.

Current model uncertainty couples subintervals through the unknown parameter;
do not pretend a mixture over Markov models is itself the same first-order
chain. Either retain the model identity in evaluation and take a common worst
bound, or explicitly maintain the updated mixture state. A per-subinterval
maximum is a conservative rectangular relaxation, not generally the exact
worst fixed-model invoice.

## Prospective work and expected evidence

Derive and check exact partial-pattern likelihoods and boundary-conditioned
policy values against full source enumeration for small paths. Preserve the
independence counterexample. Then execute a short paid repeated-source service
with a fixed true menu member, actual receipt prefixes, one common model
confidence set, and independently checked actions. Compare marginal-only
forecasting, a known-model oracle diagnostic, an equally informed ordinary
likelihood controller and a conservative source-agnostic policy. Include
model/inference/retention costs and negative source-membership controls.

This is a new constructive direction within discovery, linking S12/S16/S21
and the current paid source work. No positive contribution, calibration record,
new family count or promotion event is awarded prospectively. F01 remains its
existing distinct finite-row event.
