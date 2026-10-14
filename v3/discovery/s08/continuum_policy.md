# Continuum fee guarantees without a five-point model premise

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
Prospective construction following [compulsory-pair learning](pair_findings.md).
The new source keeps fresh stationary symmetric homogeneous Markov rows but
allows every repeat probability rho in [0,1]. The current-row action duty and
exact receipt checker remain separate from the statistical fee guarantee.

## A fixed policy has a low-degree fee polynomial

Let a deterministic receipt policy pi, fixed before the current request,
terminate after at most n distinct audits on an n-vertex path. Let C_pi(x)
be its total physical fee in complete indicator world x. The policy may
adapt to observed indicators but does not inspect hidden values or rho.
The extreme label 0 versus 2 does not affect its query choices. For a world
with s repeated adjacent indicators and d=n-1 transitions,

```math
P_\rho(x)=\tfrac12\rho^s(1-\rho)^{d-s}.
```

Consequently its expected fee is a polynomial of degree at most d:

```math
V_\pi(\rho)=\sum_{s=0}^d b_{\pi,s}{d\choose s}
\rho^s(1-\rho)^{d-s},\qquad
b_{\pi,s}=\frac{\sum_{x:s(x)=s} C_\pi(x)}{2{d\choose s}}.
```

This is an identity, not a Bernstein approximation to another function.
The coefficients are conditional mean fees given the number of repeated
transitions. They are bounded between zero and the sum of all audit fees.
Whole-world enumeration produces them directly but is exponential.

For the prepared interval policies, exact boundary-conditioned evaluation
at **n distinct interior rational rho values** determines this polynomial
uniquely. Each supplied-policy value has an O(n^2) Bellman equality certificate;
the checker uses independent matrix products for its bridge probabilities.
Interpolate exactly, convert to the Bernstein basis, then verify the supplied
coefficient vector against all n independently checked values. The degree
bound plus n equalities establishes the identity on the whole continuum,
including endpoints even though no zero-probability bridge is evaluated
there. Do not replace this with floating-point regression through n samples.
Arithmetic operation counts are polynomial; rational bit growth is separately
relevant and must be retained in resource reporting.

## A checked fee-regret region

For a finite, fixed policy bank, each difference V_pi-V_j has a coefficient
vector. Restrict this vector to a rational interval I=[l,u] with exact
de Casteljau subdivision. Nonnegative Bernstein basis weights sum to one,
so its largest coefficient bounds the difference throughout I. If, for every
bank policy j, the largest restricted coefficient is at most epsilon, then

```math
\sup_{\rho\in I}\big[V_\pi(\rho)-\min_j V_j(\rho)\big]
\le\epsilon.
```

This is a sufficient certificate, not always the sharp polynomial range.
Subdividing I can sharpen it; every subinterval must be covered and checked.
An exact zero certificate can fail at a true policy crossing even with
arbitrarily narrow nonzero confidence intervals. A positive prospectively
chosen epsilon avoids pretending that exact model/decision identification
is always possible at a boundary. The comparator is the prepared bank, not
all possible adaptive policies on the continuum.

The single-parameter time-uniform Hoeffding interval from compulsory pairs
covers the true rho at every sample count. Intersect it cumulatively and
test a checked fee-regret region at sparse confidence epochs. On the common
coverage event, stopping and freezing the chosen policy preserves the epsilon
expected-fee guarantee for all later fresh requests under the same source,
fees and bank. The current-row action certificate remains exact on every
request, including the statistical failure event. No inference is permitted
from unqueried labels; all learning samples must reference actual receipts.

## Development checks before a repeated service

Build a standalone parametric value producer and independent matrix checker.
Check polynomial identities against full world enumeration for n=2..8,
including rho endpoints and off-menu rational values. Check restrictions
against exact evaluation and reject changed coefficients, substituted roots,
changed fees and incomplete interval covers. Compare all preparation costs
with direct known-model planning and retain ordinary polynomial verification
as the identical-capability control. Then specify actual repeated-source
experiments separately, using off-menu parameters and a declared epsilon;
these are new DEVELOPMENT observations, not a rigorous confirmation stage.

The imported tools are ordinary interpolation, parametric expected-reward
verification, Bernstein range enclosure and sequential confidence sets.
The local synthesis is the source-bound chain from required action receipts
to a checked region of sufficient acquisition policies, with preparation and
statistical maintenance explicitly charged.
