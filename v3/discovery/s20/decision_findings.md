# Final decision consequences and limits

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT after P3-11-A1; none of
these extensions changes the frozen V19-R/v1 contribution event or raises its
readiness estimate. Each panel below passed its first exposure and was not rerun.

## Observation must be compared with the stated current action

The [incumbent derivation](incumbent_value.md) separates pure information value
relative to an ideal constant action from total recoverable improvement relative
to a possibly suboptimal current action. The two-cell counterexample has ideal
information value0 but incumbent improvement1. This matters operationally:
using the former to reject every positive-fee observation would be unjustified.
The frozen ideal-baseline theorem remains valid at its stated scope.

The [first result](incumbent_runs/a01/result.json) checks7,260 support brackets,
930 distinct support controls,5,916 enumerated policy tables and14,520 action
bounds. The exact incumbent bound improves on the sum of separate computation
and information bounds in2,435 cases. The implementation records271,518
cell-action inspections and2,838,159,600ns runtime; this is diagnostic work,
not a deployed speed comparison. Three malformed incumbent requests are rejected.
The maximizing support is a signature witness, not a receipt-source witness.
Acquisition and policy computation fees must both be subtracted. A large upper
bound alone is insufficient reason to acquire information.

## Source evidence changes the decision's status

The [integration result](integration_runs/a01/result.json) connects retained
receipts, partial scalar ranges, computation-gap bounds and incumbent-aware
observation bounds. The initial fallback has possible improvement1 although
ideal information value is0. Two propagation passes exclude the hazardous
band with134 row visits,28 coordinate updates and zero optimizer calls.
The fast action then has computation gap0 and observation improvement upper0.
The range is still incomplete, and nonemptiness is still conditional until a
checked original source is supplied. Revision2 and revision3 carry such source
evidence; revision0 and revision1 explicitly do not.

This demonstrates a useful stopping condition before full range reconstruction.
It does not demonstrate a runtime gain over a tailored ordinary band query.
Three source checks and two rejection controls cover digest mismatch and a
bad second source block; rejected updates leave state and revision unchanged.
Input/output copying and changed request identity are checked. An inconsistent
receipt problem returns INCONSISTENT_SOURCE rather than a vacuous decision.
Runtime is7,078,600ns, with no optimizer calls; copying and general production
costs were not separately measured. Correctness remains conditional on receipt
and model premises. Python isolation is not an adversarial security guarantee.

## Continuous losses require the right candidate points

The [continuous derivation](continuous_gap.md) extends the sharp computation-gap
formula to compact scalar brackets and continuous losses. The rational
piecewise-affine implementation evaluates interval endpoints, loss knots and
crossings with an already witnessed competing maximum. The last category is
necessary even when the individual losses are convex: the worked example's
second action has exact gap13/4 at3/4, while checking the supplied knots alone
would report only1. The first action is already certified optimal despite the
older separate-extrema bound2. Optimality is relative to the fixed loss model;
it is not a certificate of low absolute loss or of true real-world premises.

The [first result](continuous_runs/a01/result.json) uses the worked example and
three prospectively saved seeded tables. All76 independent epigraph LP controls
agree with161 formula candidate evaluations; rational primal/dual evidence is
retained. Three malformed domain/shape controls are rejected. Runtime56,902,200ns
excludes imports and is not a general performance result. This implementation
handles deterministic worst-loss decisions; a regret transformation requires
its own piecewise representation, including any additional crossing knots.

Together these consequences connect retained uncertainty to the value of further
reasoning and observation. Their ordinary robust-optimization derivations are
explicit. They strengthen the usable research program without creating a new
standalone novelty claim or retroactively adding duties to the passed review.

For fallible-model use, the remaining bridge is an upstream simultaneous
coverage guarantee. On that event an absolute loss certificate can be carried
through an adaptive stopping decision. A zero computation gap supplies no such
absolute bound, and fixed-time coverage alone does not survive arbitrary
stopping. Thus the demonstrated stopping service is useful conditional
reasoning; it does not manufacture calibration from its exact arithmetic.
This distinction leaves a concrete future research direction while avoiding
making calibration a retrospective prerequisite for the bounded contribution.
