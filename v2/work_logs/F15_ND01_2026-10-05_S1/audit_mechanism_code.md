# F15-ND01 independent supplementary mechanism-code audit

Reviewer: ChatGPT (GPT-6 Astra Pro), representation-analysis subagent.
Date: 2026-10-05. Concurrent review adds zero separate root-clock minutes.
Scope: static review before launch of the supplementary analysis; not F16.

Reviewed [`mechanism_analysis.py`](../../experiments/F15_ND01_analysis/mechanism_analysis.py).
Final source snapshot: **20,415 bytes**, SHA256
`4e181fdd7a1b95c9be9e76fb36f7be032e2cbf823fa95e8e34e892a9de8150c1`.
Also inspected relevant interfaces in `neural.py`, the ND01 runner,
`search_methods.py`, `soft_mask.py`, and `binary_global.py`.

**Launch verdict: no substantive mathematical, indexing, hash-binding, or
scope blocker found.** The root may run this supplementary analysis once.
This is not a claim that its numerical output has already passed validation:
the reviewer did not execute it, run models, or generate populations.

## Exact box geometry and null direction

The declared four-input box matches the task domain. For each affine
preactivation, taking the appropriate endpoint according to each weight's
sign gives its exact real minimum and maximum. `Fraction.from_float` treats
the stored binary64 parameters as exact rationals, rather than treating their
decimal display as exact.

The classification at zero is correct: an upper bound at zero means the ReLU
is identically zero; a nonnegative lower bound means the activation equals
its affine preactivation throughout the box. Always-active **differences**
depend on weights alone, so excluding biases from the four-row RREF matrix
is correct.

The RREF implementation normalizes exact pivot rows and eliminates their
columns from every other row. Setting one free variable to one and pivot
variables to the negatives of the corresponding RREF entries produces a
null vector of the active weight matrix. The exact matrix-vector assertion
checks that construction. An inactive-coordinate null vector is also valid.

The hidden-difference rank bound `number_variable + rank_active_weights`
is sound: variable coordinates contribute at most their count, active
coordinates at most the rank of their weight block, and inactive coordinates
zero. It is an upper bound, not a claim that every variable neuron supplies
an independent feature. Scaling the rational vector before floating conversion
avoids unnecessary large intermediate magnitudes. The output correctly
distinguishes the analytic null direction from its numerical execution check.

## Stable projector construction

Let `a=m*v`, `delta=sum m*(1-m)*v^2`, and let `u` be a unit null direction.
For `q=a+t*u`, the sphere equation becomes

\[
t^2+b t-\delta=0,\qquad b=(2a-v)^T u.
\]

The implemented small-magnitude root is

\[
t=\operatorname{sgn}_{+}(b)
  \frac{2\delta}{\sqrt{b^2+4\delta}+|b|},
\]

where the sign is positive at zero. This is correct: it is the positive root
when `b>=0` and the negative root when `b<0`. It avoids subtracting nearly
equal large terms. At zero deficit, zero shift is a valid choice.

The rank-one matrix `q*q.T/(q.q)` has the intended symmetry, idempotence,
and head coefficient when the sphere condition holds. The zero-vector branch
is appropriate. Numerical checks use the actual computed `P@v`, so they do
not silently substitute the ideal coefficient for the implemented one.
The exact null-vector proof and float64 residual records appropriately
separate real-function equivalence from floating arithmetic.

This is an algebraic per-role output equivalence. The code explicitly avoids
claiming DAS execution, a new native representation, or jointly orthogonal
role projectors. A wording issue in the no-null branch—calling the new
geometry construction “registered”—was reported before launch and changed
to supplementary/declared wording in the hashed snapshot above.

## Population and objective binding

The initial runner verification requires all 15 prepared units and all 15
evaluations, with their manifest and freeze bindings. The script then
regenerates the exact existing discovery and validation arrays using the
same seeds, sizes, streams, and stratum order. Pair hashes are compared
against both the saved search and soft-mask records.

The regenerated least-squares matrix and target are also checked against
the soft-mask matrix hash. Symmetric Gram matrix, linear term, and constant
are checked against the exhaustive binary solver's quadratic hash. These
operations match the original implementations, including the base logit in
the target. A mismatch stops the analysis.

Rescoring every saved candidate on that same logit quadratic resolves the
earlier objective ambiguity. The arithmetic decomposition is

\[
f(\text{selected})-f(\text{global})
=[f(\text{selected})-\min_{\text{pool}}f]
 +[\min_{\text{pool}}f-f(\text{global})].
\]

These are, respectively, selection-objective and candidate-coverage gaps
for the finite discovery logit objective. The new analysis-only pool winner
is neither adopted nor evaluated as a new validation method. Quadratic
scores and the saved direct residual optimum use float64; tiny differences
near the recorded tolerance are not substantive coverage findings.

## Error terms and two-donor signs

The code uses `+log J0` for role zero and `-log J1` for role one. Its
baseline error, residual change, total error, and cross moment agree with
`total=e(base)+r(donor)-r(base)`. Coordinate second moments are explicitly
marked as ignoring cancellation; their participation count is an energy
description, not a count of semantic features.

`h01` applies role zero followed by role one; `h10` applies the reverse.
The difference is correctly checked against
`(h1-h0) @ (v*m0*m1)`. The joint high-level target correctly combines
`J0(donor0)` with `J1(donor1)`.

This secondary panel combines already existing role-specific donors. It
is explicitly not a frozen joint stratum, an independent newly drawn
population, or another confirmatory condition. No trained weights,
registered masks, study outputs, or claim endpoints are modified.

## Review limits and administrative record

This was a static audit; runtime hashes and numerical identity residuals
remain the root execution's responsibility. Existing-output refusal and
exclusive writes preserve prior supplementary results. One read-only source
lookup initially used the nonexistent name `search.py`; the lookup was
corrected to `search_methods.py`. It did not launch an analysis or affect
any artifact, model, or population.
