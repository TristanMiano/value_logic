# Label-free forecast repair: useful boundary, mostly established machinery

Codex (GPT-6), DEVELOPMENT cheap screen, Q1/Q3/Q4/Q5. This is a distinct
portfolio pass after the query/flip construction, not a new family count.

Suppose a finite vector v of unresolved mathematical truth values is known
to satisfy checked constraints and lies in a convex relaxation C. An arbitrary
model proposes a vector f of probability forecasts. For quadratic report loss,
projection g=P_C(f) satisfies

```math
\|v-f\|^2-\|v-g\|^2\ge\|f-g\|^2.
```

The proof is the projection variational inequality
(f-g).(v-g)<=0 and the squared-distance identity. The right side is a
certified reduction in this report loss without resolving v or postulating a
random mathematical truth. It is not evidence of calibration, coverage, or
correctness on each coordinate. This refines, without contradicting, P3-02's
warning that mere coherence does not establish forecast accuracy.

This guarantee is established prior art. Predd et al. (2009), Theorem 1,
Proposition 3 and section VII.A, connect coherence, proper scores and Bregman
projection, including differently weighted event scores:
<https://www.princeton.edu/~kulkarni/Papers/Journals/j071_2009_PreSeirLieOshKulPoo_TransIT.pdf>.
Read those statements and the bounded-case proof; no new proper-score theorem
is claimed. Full source text has damaged formula extraction, so the quadratic
special case above is independently derived rather than copied from it.

## A paid, partially checked version

Exact projection is not required to admit an improvement. For arbitrary
proposed g, the pointwise loss reduction is the affine function

```math
2(g-f)^T v+\|f\|^2-\|g\|^2.
```

A valid rational lower certificate for this expression over a checked outer
source proves improvement >=gamma. If gamma exceeds the complete cost of
producing, checking and applying that repair in the same utility units, the
repair pays for itself on every admitted truth assignment. Existing source
LP/SAT certificates can supply such a lower bound. The calculation is an
ordinary dominance certificate, not a new route around acquisition costs.

If an untrusted proposer supplies an alleged logical constraint, its validity
must first be checked under the intended axioms. A forecast's self-reported
consistency or a solver's unverified claim is not a new true constraint. Invalid
proposals and failed verification still cost resources. A lower bound on gain
conditional on validity does not by itself justify purchasing an arbitrarily
expensive validity check. Reused accepted constraints retain their dependency
and version obligations.

For repeated accepted repairs, loss reductions telescope. A total-cost-positive
rule must charge all failed proposals too. Merely summing successful repair
gains does not prove a whole service profitable, nor does finite squared
movement imply general Logical Induction or a computable truth learner.

## Why lower report loss is not every useful decision

Let the checked relation be v1=v2 and f=(2/5,9/10). Euclidean projection gives
g=(13/20,13/20). For either admitted Boolean truth 00 or 11 the summed Brier
loss drops by exactly 1/8. Yet at truth 00, predicting v1 by a threshold of 1/2
changes from correct under f to incorrect under g. Thus an actual task asking
only for the first bit can get worse. Different task weights change the repair;
the score must be part of the intended utility contract, not selected afterward
to manufacture progress.

Disposition: retain as a useful explanatory connection and possible adapter
for an actual scoring duty. Do not build a new large coherence benchmark.
The core dominance guarantee is already known; no substantive novel acquisition
consequence has yet been found. Return to other portfolio directions.
