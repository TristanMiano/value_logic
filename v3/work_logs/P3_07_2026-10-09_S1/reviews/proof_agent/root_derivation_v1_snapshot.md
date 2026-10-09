# P3-07 — paid reasoning under an uncertain performance profile

**Status: research in progress.** This development artifact continues the
completed [P3-06 forecasting result](06_cost_forecast_refinement.md). Its
question is which *specified computation*, if any, to buy. Forecast accuracy,
a proof of eventual resolution, and a computation's positive expected net
value are separate claims. The [prospective session forecast](../work_logs/P3_07_2026-10-09_S1/forecast.json)
and observed clocks precede this derivation. P3-B and P3-08 are unattempted.

## 1. The service and its finite scope

A request supplies a mathematical query, available terminal actions, an
available fallback, a hard resource budget, and prices in task-loss units.
The mathematical answer is deterministic. A performance profile describes
the behavior of a bounded procedure over a declared population of such
requests; it is not a second semantics for the mathematical answer, nor a
free conditional distribution of everything implied by visible program text.

Fix a finite catalogue of **complete policies**. A policy includes which
computation to call, how far to run it, which checked observations it may use,
and what terminal action it returns on success, timeout, refutation, or an
unusable receipt. A multi-step policy includes every contingent continuation.
All policies obey the same input-access rules and hard limits. A reserved
fallback must remain feasible after an unsuccessful computation. Exhausting
a budget does not erase resources already spent.

The stopping catalogue includes immediate actions and fallback. The ordinary
metareasoning comparator receives the same catalogue, observations, prices,
profiles, caches, and implementation. It can implement the selection rule
below exactly. A charged exact solver is a further concrete comparator; a
free answer oracle, if shown, is a separate diagnostic.

The resource vector distinguishes admission and feature extraction,
forecasting, profile acquisition, assessment/selection, proof or evaluation,
checking, evidence acquisition, storage/access, dependency-model construction,
and admissible-repair search where present. No cost is converted into task
loss without a stated price. Hard resource caps remain constraints even when
the corresponding price is zero. Shared work, one-time setup, and an asserted
amortization horizon must be declared separately.

## 2. A root certificate for a complete policy

Let $`b`$ be a complete stopping policy and $`\pi`$ a complete candidate. On
one request $`X`$, let $`z_b(X),z_\pi(X)\in\mathbb R^d`$ record the same
task-loss basis and resource quantities. Define the paired feature saving

```math
d_{\pi,b}(X)=z_b(X)-z_\pi(X),\qquad
G_{\pi,b}(\lambda)=\lambda\mathbin{\cdot}\mathbb E[d_{\pi,b}(X)].
```

The expectation names a declared request law and initial procedure state.
The computation's outputs may be arbitrarily dependent within an episode.
A single joint law governs the whole policy. Replacing it by independently
chosen conditional worst cases is an additional rectangularity assumption,
not an algebraic simplification of this certificate. Complete-policy
enumeration can be expensive; enumerating or evaluating the catalogue is
itself charged. This result supplies no cheap planning oracle.

Suppose a *paid* procedure produces bounds $`l_{\pi,b,j}\leq
\mathbb E[d_{\pi,b,j}]\leq u_{\pi,b,j}`$ simultaneously for all retained
comparisons and coordinates. For any fixed price vector, including one
chosen after observing those bounds, set

```math
L_{\pi,b}(\lambda)=
\sum_{j:\lambda_j\geq0}\lambda_j l_{\pi,b,j}
+\sum_{j:\lambda_j<0}\lambda_j u_{\pi,b,j}.
```

If online selection and other incremental overhead absent from
$`z_\pi-z_b`$ cost at most $`h(\lambda)`$, then
$`L_{\pi,b}(\lambda)>h(\lambda)`$ certifies lower expected total loss than
the declared stopping policy, conditional on the simultaneous coverage
event. A declared conservative rule buys a feasible candidate only on this
strict inequality; otherwise it uses its selected stopping policy. This is
a sufficient rule, not a claim that uncertified computations are valueless.
The comparison must also account for the assessment cost on the branch that
ultimately stops. A controller which always assesses can lose to immediate
stopping even when it never buys a computation.

**Proof.** On the simultaneous event, multiply the lower bound by each
nonnegative coefficient and the upper bound by each negative coefficient,
then sum. The true expected feature saving is at least $`L`$. Subtract the
overhead bound. Selecting a comparison after the event is observed does not
invalidate an inequality that already holds for every comparison. No
independence between coordinates or policies is used. This is a root
expected-loss comparison, not a pathwise promise about an individual query.

The same calculation applies to an explicitly supplied joint credal set,
using the infimum of complete-policy improvement over that set. Such a set
is an assumption until its acquisition, soundness, and evaluation have an
evidence contract. Independent marginal intervals generally discard useful
dependence; evaluating each branch against a different model can change the
decision problem. The existing [composition boundary](../foundations/01_composition_boundaries.md#cb05-a-tree-recursion-can-discard-shared-constraints)
already establishes that obstruction; this task imports it rather than
repeating that completed work.

## 3. Acquiring simultaneous bounds from permitted observations

Fix the policy catalogue, stopping catalogue, coordinate meanings, and
bounded initial states before drawing profile data. Obtain $`n`$ independent
requests from the declared law. On each request run every retained complete
policy, with the specified state reset, and acquire/check the evidence
needed to record its feature vector. These paired full-information rollouts
can be costly. Shared valid computations may be reused only under an
explicit accounting and information contract; a future result is never
available before its paid acquisition.

Suppose each paired coordinate is known to lie in
$`[a_{\pi,b,j},b_{\pi,b,j}]`$, and write its width as $`R_{\pi,b,j}`$.
For $`K`$ total comparison-coordinate cells, a simultaneous Hoeffding event
has probability at least $`1-\delta`$ when

```math
\epsilon_{\pi,b,j}
=R_{\pi,b,j}\sqrt{\frac{\log(2K/\delta)}{2n}},
\quad
l=\max(a,\widehat d-\epsilon),
\quad
u=\min(b,\widehat d+\epsilon).
```

Apply the scalar bounded-sum inequality to each sequence of *paired
differences*, then union bound over both tails and all cells. The policies'
outcomes on the same request need not be independent. In particular, a
difference in $`[-R,R]`$ has width $`2R`$. Exact labels, correct resource
measurements, fixed policy behavior, and the sampling law are assumptions;
this statistical inequality does not prove any of them. Primary-source
comparison and independent reconstruction are being recorded separately.

### 3.1 An integer-checkable conservative radius

An implementation need not trust rounded logarithms or square roots for a
purchase certificate. Choose an integer $`k`$ with
$`2K\,2^{-k}\leq\delta`$, choose a rational $`r\geq0`$ satisfying
$`2nr^2\geq k`$, and use $`\epsilon=Rr`$. Since $`e\geq2`$,

```math
2K\exp(-2nr^2)\leq2K\exp(-k)\leq2K\,2^{-k}\leq\delta.
```

Both final inequalities can be checked with integers/rationals. This radius
is deliberately looser than the logarithmic radius. Its construction and
verification consume resources; mathematical validity does not make their
runtime free. The implementation must reject invalid dimensions, ranges,
counts, versions, budgets, and nonfinite or malformed quantities before
issuing a certificate.

### 3.2 Exactly what repricing preserves

One simultaneous coordinate event supports every constant price vector for
the same feature distribution and fixed complete-policy maps. This includes
a data-selected price vector, with no further union over a continuum of
prices. If only nonnegative prices are meaningful, that is the declared
domain. Large prices enlarge the uncertainty penalty as well as the
estimated saving; no scale-independent usefulness claim follows.

A new objective outside the retained feature span needs new information.
Changing a policy's internal terminal decision or stopping rule changes its
feature distribution, even if the code file is unchanged. The new complete
map must be covered by the catalogue or separately assessed. A
query-dependent price $`\lambda(X)`$ cannot be pulled outside an
unconditional expectation. Such a service requires covered weighted
features, declared strata with valid conditional sampling, or a fresh audit
of the complete price-reactive controller. A selected individual query is
not automatically a fresh draw from the profile's target law.

## 4. The acquisition and self-assessment boundary

A positive deployment certificate after profiling does not show that
building the profile was worthwhile. Let setup cost $`S`$ include task
generation/access, all policy rollouts and labels, retained data, profile
construction, and the checks that make it usable. For a declared future
horizon $`H`$, the sufficient successful-branch condition is

```math
H\,[L_{\pi,b}(\lambda)-h(\lambda)]>S.
```

This comparison requires the same future deployment law and an actual
accounting convention for $`H`$. It is not evidence that the procedure
knew before profiling that this branch would occur. The no-certificate
branch still incurs setup and assessment costs. An acquisition policy needs
its own bounded decision model, an explicitly tolerated exploration loss,
or an independent assessment of the entire profile-then-select procedure.
A finite depth and budget can terminate this metareasoning process; they do
not establish that the last unassessed controller is optimal.

A bounded self-assessment can be made without self-endorsement. Freeze the
whole procedure closure: controller and computation versions, policy maps,
profiles, feature meanings, prices or covered price rule, initial caches and
other retained state, scheduler, and budget/fallback behavior. Evaluate
this *fixed* program against a stopping comparator on fresh independent
episodes, paying the required execution, checking, and retention costs.
The same paired bounded-mean argument certifies its expected performance
over that episode law. Conditioning on earlier design data is legitimate
because the audit sample is fresh. Updating the frozen procedure during
those audit cases or reusing them for unaccounted selection invalidates
this simple argument. A whole adaptive episode can instead be the sampling
unit if it is fixed and bounded before the audit.

This is a staged empirical self-model of one version. It supplies no
reflection theorem, proof of the code's own correctness, universal model of
future versions, or guarantee for outcomes altered by the report itself.

## 5. Equal prediction accuracy need not give equal computation value

The existing EX07 already distinguishes stakes and complementary
computations. A further finite witness distinguishes the *same expected
proper-score improvement* from the value of buying a signal.

Let a binary answer have prior one-half. Signal A gives posterior 0 or 1
with probability $`2/25`$ each, and posterior one-half otherwise. Signal B
gives posterior $`3/10`$ or $`7/10`$, each with probability one-half. Each
is an explicitly stipulated Bayes-consistent experiment; these probabilities
are a diagnostic joint-law assumption, not acquired performance evidence.
Both have expected Brier loss $`21/100`$, improving the prior's $`1/4`$ by
$`1/25`$.

With false-positive loss 9 and false-negative loss 1, the action threshold
is $`9/10`$. Immediate action 0 has expected task loss one-half. Signal A
improves that loss by $`2/25`$ because its certain-positive branch changes
the action. Signal B never crosses the threshold and improves task loss by
zero. At a signal cost $`1/25`$, A pays and B does not. An accuracy-only
performance profile fails to identify this decision value. Under a changed
objective the comparison must be recomputed from appropriate retained
outcomes, not from the common Brier score alone.

## 6. Development implementation and verification

Pending. The prospective design uses a separately versioned bounded
mathematical computation adapter, a finite complete-policy catalogue,
charged paired profiling, an exact-rational certificate, and a fresh audit
of the frozen selection procedure. All runs are development. Cheap
ordinary shortcuts and exact computation remain available and charged under
the same contract; no speed, hardness, novelty, or final-evaluation claim is
implied by this plan.

## 7. Current evidence boundary

The independent proof reconstruction, primary-source verification, actual
implementation checks, clock accounting, and final scope assessment remain
open. Neither Research90 nor P3-07 completion is asserted here. P3-N01 stays
NOT YET SUPPORTED pending substantive evidence assessment. No later gate or
task has started.
