# Paying for proof compilation without forecasting recurrence

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT derivation and [exact arithmetic](compile_policy.py), with
[source-bound results](compile_policy_results.json). This applies the
established rent-or-buy principle to the [compact proof profiles](reprice_compact_findings.md).

## The decision that remains after exact compression

The raw and compact tree evaluators return identical lower and upper bounds
for every admitted nonnegative weight vector. The compact representation is
more expensive to build and cheaper to reuse. An arbitrary future sequence
of priorities does not require forecasting how many edits will occur before
choosing between these two representations.

Suppose the raw profile already exists. Let B be the complete additional
compilation cost, c_j the compiled service cost for admitted query j, and
delta_j>=0 the extra raw evaluation cost. These must be known before serving
j, or bounded by a separately justified paid contract. They cannot be taken
from a free forecast of an arbitrary solver's future runtime.

Maintain the excess R already spent on raw evaluation. Before serving a query,
compile if `R+delta_j >= B`. Otherwise use the raw evaluator and add delta_j
to R. After compilation, use the compact evaluator. The archive must remain
valid, the compilation price fixed, and both representations must supply the
same requested output. Work that changes the archive starts a separately
specified epoch; an offline comparator allowed uncharged transfer across
those epochs would need a new analysis.

## A complete elementary guarantee

For a horizon N, any offline strategy that eventually compiles can move its
compilation to the first query and save every earlier nonnegative excess.
Thus its optimal cost, apart from common existing setup, is

```text
OPT_N = sum_j c_j + min(B, sum_j delta_j).
```

If the online strategy never compiles, its accumulated excess is below B
and it equals this optimum. If it compiles, the excess previously rented
is strictly below B, while the horizon's total potential excess is at least
B. Its excess bill is therefore `R+B < 2B`. Including the nonnegative common
evaluation costs gives `ALG_N <= 2 OPT_N` for every finite horizon. The
zero-cost case is immediate. The deterministic argument permits future
queries to depend on previous answers or decisions.

This is a standard online acquisition guarantee, not a new competitive-ratio
theorem. A primary antecedent is Karlin, Manasse, McGeoch and Owicki,
*Competitive Randomized Algorithms for Non-Uniform Problems*, Section 3.1
([author paper](https://courses.csail.mit.edu/6.895/fall03/handouts/papers/karlin.pdf)),
which gives the analogous deterministic spin/block threshold. Our new local
use is the explicit mapping from preserved proof semantics and measured
construction/evaluation invoices to this decision rule.

## What the current paid archive actually implies

The current fixed-format sixteen-row profile request has raw setup 7,975,
additional compilation B=5,943, raw evaluation 2,283, and compact evaluation
752 declared service units. Thus delta=1,531. Building immediately repays its
extra setup on query four. Without knowing the horizon, the threshold rule
rents for three queries and compiles just before the fourth.

On the five already exposed recipes, this online choice costs **22,271**
including shared setup. Always raw costs **19,390** and compilation at the
start costs **17,678**. The online guarantee does not make its short exposed
prefix a measured win. It buys protection against both early termination and
long recurrence, while paying for its uncertainty about the horizon. The
calculation reuses prior invoices; it is not a new experimental workload.

The strengthened scalar profile is cheaper still, but may return weaker
action guarantees. It is therefore a distinct output-quality option, not
one of the two equivalent evaluators in this guarantee. A service can first
ask whether its cheap available certificate already meets the requested
tolerance, and invoke this compilation policy only for requests that require
the stronger profile. Costs of that admission and routing belong in the bill.

This supplies a concrete bounded-reasoning mechanism for the next service:
retain a correct action certificate, compile expensive reusable structure
only when the observed demand justifies it, and leave proof validity
independent of a learned guess about future demand. Better recurrence models
can guide earlier purchases, but need their own evidence and loss account.
