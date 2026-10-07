# P3-01 acquisition and performance-profile boundary

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal reconstruction, not external validation.
Resource time is unmeasured and contributes no principal-clock credit.
Scope: a question-contract addendum. No canonical edit, new experiment,
downstream task, publication or gate decision is made.

## 1. Primary R8 boundary

Reopened Zilberstein and Russell, [Optimal Composition of Real-Time
Systems](https://people.eecs.berkeley.edu/~russell/papers/aij-anytime.pdf),
Artificial Intelligence 82 (1996), 181–213, the primary source inherited in
`v2/literature/04_n01_recurrence_comparison.md`, R8.

Definition 2.5 maps input quality and time to an output-quality distribution.
Section 2.2.3 covers analytically derived or statistically learned profiles,
deployment-population relevance, discrete tables, interpolation and approximation
error. Section 2.2.1 warns that component expectations need not determine an
expected composite quality. Section 4 assumes by-value, side-effect-free
functional composition with a fixed profile per function. Theorem 4.6 gives
local-compilation optimality for tree structure under input monotonicity;
Theorem 4.7 adds bounded degree and measures complexity against the discrete
time horizon. Section 4.4 handles repeated subexpressions separately, including
one paid evaluation reused within a computation. Section 4.3's `oneof` operator
selects the component result with greatest quality.

Those are selected definition and theorem boundaries, not a complete proof
reconstruction or a theorem about arbitrary evolving learned controllers.
Locators refer to the author PDF's numbered sections; its pagination differs
from the journal pagination.

### Application to this contract — reviewer assessment

An ordinary comparator may learn procedure-specific proof-success or answer-quality
profiles and use them to allocate a reasoning budget. That service alone is not
a distinctive value-logic result. Future work must distinguish the *supplied*
profile diagnostic from a profile acquired with charged data and computation.
Learning a proof-production profile also does not resolve the proposition's
truth: procedure, budget, target and outcome definition remain separate fields.

For this application, require the training population, readable conditioning
features, acquisition/update costs, quality-observation mechanism, precision,
reuse assumptions and change policy. A profile keyed by an unavailable true
quality would hide an oracle. Likewise, an executable selector cannot choose
the actually most accurate logical answer using evaluator-only labels. Shared
caches, report-induced effects and theory/program changes require their own
state/transport contract before applying a static composition theorem.

## 2. Correct the ambiguity in “same evidence”

This explicitly clarifies my earlier
[composition review, §3](composition_and_contribution_boundary.md): “same
available queries, evidence” must not require identical *realized acquired*
histories in the primary policy comparison. The current canonical §8 and Q3
use similarly compressed wording. The intended comparison is:

> Give the methods common initial information and access to observations,
> computations, models and repairs on the same declared terms. Use the same
> resource and decision contract. Each policy pays for its own acquisitions
> and may consequently reach a different information history.

| Regime | Information and costs | Permitted conclusion |
|---|---|---|
| Full acquisition-policy comparison | Start from the common information/access contract. Each policy selects and pays for its own computations, then acts on its own resulting history. | Compare realized task loss plus that policy's charged costs, and coverage/timing under the common objective. |
| Matched-history replay | Supply a specified common history to both methods. Either attach the same historical acquisition cost to both, or explicitly condition on already available information and exclude acquisition from the target. | Isolate representation, forecasting, revision or decision behavior at that history. This does not rank the original acquisition policies end to end. |
| Evaluator-only completion | Generate a common scoring cohort or later labels under a declared evaluation procedure; keep those labels unavailable to policies before their decisions. | Assess earlier outputs without giving either method free resolution or silently selecting only its resolved claims. |

The root's planned loss-10/resolve-1 example is an appropriate diagnostic of
the distinction. It is not executed or reconstructed here. A policy that does
not buy an answer must not receive another policy's paid answer before acting
and then be reported as cheaper because it paid no acquisition cost. Giving
both methods that answer defines a different, conditional comparison.

Within-policy reuse remains legitimate: one acquired answer may serve several
later decisions when its validity and retention are established. Charge the
actual acquisition and subsequent checks/lookups under the declared model,
not a fictitious repeated full acquisition. An openly supplied common initial
artifact is also legitimate under its declared preparation/amortization rule;
it must not be created retrospectively from one policy's private evaluation
trace. Coupling underlying instances or random draws for comparison precision
does not itself authorize sharing observations.

Operational fields to make explicit later are: initial readable state;
available queries and their price law; each policy's requests, results and
arrival times; retention/reuse rights and charges; decision timestamps; training
and initialization amortization; evaluator-only labels; cross-policy information
barriers; common cohort; and the exact estimand for any replay. P3-01 can name
these fields without implementing or freezing the later protocol.

## 3. O-COMB is a credible comparator family

O-COMB should identify ordinary components and runnable candidate baselines,
their assumptions, selection procedure and comparison scope. It is not an
instruction to outperform every possible classical program. An implemented
candidate can itself be expressed as a classical program; that observation
precludes an exclusive-capability claim based only on the formal label, while
leaving implementation, formal-adaptation and application contributions open.

Nor should O-COMB select the best baseline separately for every evaluated
instance using its hidden answer. Declare a finite practical comparator set
and a permitted development-selection rule with accounted resources. A
best-fixed-method comparator in a stated regret theorem has a different role
from an executable controller; a best-per-instance oracle is a labeled bound
or diagnostic. A real portfolio or selector is allowed, but its observations,
selection computation, training and constituent execution costs must follow
the same contract.

This boundary is demanding enough to avoid comparing value logic with bare
Boolean syntax, yet finite enough to be an assessable research obligation.
Equality may support an exact reduction; modest useful synthesis or application
still needs a concrete supported delta. Neither superiority over all ordinary
programs nor mere concatenation of established components is the contribution
test. **P3-N01 remains NOT YET SUPPORTED by this review.**
