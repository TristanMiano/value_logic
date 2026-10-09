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

The timing of overhead matters. For a declared future cohort of $`H`$
requests, let $`t_\pi(\lambda)`$ be still-unpaid, policy-specific overhead
absent from the feature vector. After common assessment is already paid, a
conservative continuation chooses

```math
\widehat\pi\in\mathop{\mathrm{argmax}}_{\pi\in\Pi\cup\{b\}}
\{H L_{\pi,b}(\lambda)-t_\pi(\lambda)\},
\qquad L_{b,b}=t_b=0.
```

Its lower future improvement is nonnegative. Shared sunk acquisition and
assessment costs must not make the controller decline a continuation that
now improves expected loss. They remain in the root accounting. If their
actual incurred values are $`S`$ and $`h`$, the all-in lower gain is

```math
H L_{\widehat\pi,b}(\lambda)-t_{\widehat\pi}(\lambda)-S-h.
```

A positive value is a sufficient successful-branch certificate. The branch
that finds no candidate still loses $`S+h`$ relative to never starting the
assessment. Thus neither the rule nor this certificate proves that deciding
to acquire the profile was worthwhile before seeing it.

The deployed prototype includes execution overhead inside each policy's
feature vector, so $`t_\pi=0`$. It selects the largest lower saving, with
fallback winning a zero tie. A paid gross-value screen can first reject this
assessment route when a known upper bound on its possible task saving is no
larger than a still-unpaid mandatory assessment cost. The screen's own cost
remains paid; it does not rule out cheaper unassessed routes.

**Proof.** On the simultaneous event, multiply the lower bound by each
nonnegative coefficient and the upper bound by each negative coefficient,
then sum. The true expected feature saving is at least $`L`$. Multiply by
the fixed future horizon and subtract the relevant overhead. Selecting a comparison after the event is observed does not
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
this statistical inequality does not prove any of them. The [source contract](../literature/07_paid_reasoning_sources.md#pr07-6--the-concentration-inequality-actually-needed) identifies the exact bounded-sum theorem; the
[independent reconstruction](../work_logs/P3_07_2026-10-09_S1/reviews/independent_policy_reconstruction.md) checks its use on paired rows.

### 3.1 An integer-checkable conservative radius

An implementation need not trust rounded logarithms or square roots for a
purchase certificate. Let $`Q`$ be the number of sample sizes fixed before
profiling, and let $`K`$ count nonconstant comparison-coordinate cells.
Choose an integer $`k`$ and a rational $`r\geq0`$ satisfying

```math
2\max(1,K)Q\,2^{-k}\leq\delta,\qquad 2nr^2\geq k.
```

Use $`\epsilon=Rr`$. Because $`e\geq2`$, the union of both tails, all
cells and all declared checkpoints has failure probability at most

```math
2KQ\exp(-2nr^2)\leq2KQ\exp(-k)\leq2KQ\,2^{-k}\leq\delta.
```

Constant coordinates are exact, including the zero baseline. If all cells
are constant, their coverage is deterministic. The implementation uses the
conservative nonzero envelope anyway. Its upward dyadic square-root rounding
and the two displayed conditions are checked exactly with integers. With the
six-policy profile, four checkpoints and $`\delta=1/20`$, $`K=22`$ and
$`k=12`$. The radius calculation, coordinate reads, arithmetic and decision
are paid operations.

The fixed checkpoint qualification matters. An independently reconstructed
fair-sign example has a valid fixed-time false-positive bound below 0.05,
yet checking after every draw through 2,000 raises the exact crossing
probability to approximately 0.11284. The [saved proof diagnostics](../work_logs/P3_07_2026-10-09_S1/reviews/proof_agent/policy_proof_checks_result.json)
preserve that calculation. Repeated testing needs a stated union budget or a
valid confidence sequence; an unmodified fixed-time interval is insufficient.

If $`\pi^*`$ maximizes the true finite-catalogue gain, the selected lower-bound
policy also has the ordinary conservative regret bound

```math
G_{\pi^*,b}(\lambda)-G_{\widehat\pi,b}(\lambda)
\leq 2\sum_j |\lambda_j|\epsilon_{\pi^*,b,j}
```

when policy-specific future overhead is zero. On the simultaneous event,
$`G_{\widehat\pi,b}\geq L_{\widehat\pi,b}\geq L_{\pi^*,b}`$, and
$`G_{\pi^*,b}-L_{\pi^*,b}`$ is at most the right side. Clipping intervals
to their valid ranges can only improve the lower score. This comparison is
with the fixed catalogue, not an unrestricted adaptive planner.

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

### 3.3 A represented context rule or a proved shift bound

There are two explicit ways to extend the constant-price claim. Neither is
implemented by silently reusing the current fourteen-coordinate profile.

First, fix bounded, available context functions $`g_1,\ldots,g_m`$ before
sampling and retain the paired features
$`g_r(X)d_{\pi,b,j}(X)`$. Their simultaneous bounds support every represented
price schedule $`\lambda_j(X)=\sum_r\theta_{jr}g_r(X)`$ by the same signed
linear calculation. The coefficients may be selected from the profile data;
the complete policy maps and the context-feature definitions remain fixed.
Finite stratum indicators are a simple example. Computing the context
features and admitting their bounds has a cost. A new policy that reacts
differently to those prices is a different complete map, requiring catalogue
coverage or its own assessment.

Second, suppose a separately justified deployment law $`\nu`$ satisfies
$`\mathrm{TV}(\nu,\mu)\leq\rho`$ relative to the acquired profile law.
For a coordinate in $`[a_j,b_j]`$, a valid deployed interval is the old
interval expanded by $`\rho(b_j-a_j)`$, then clipped to the analytic range.
Indeed, normalize the coordinate to $`[0,1]`$ and use the layer-cake integral
of its level sets: its expectation changes by at most total variation.
Thus a constant-price lower gain may be reduced by

```math
\rho\sum_j |\lambda_j|(b_j-a_j).
```

The coefficient has no extra factor of two when total variation means the
supremum probability difference over events. A binary indicator attains the
bound. A feature map or computation implementation change is a separate
change; a population-distance bound alone does not cover it. The theorem
requires an independently supported $`\rho`$, not an estimate declared
small because a few observed means agree. No such drift certificate is used
in the present development runs.

## 4. The acquisition and self-assessment boundary

A positive deployment certificate after profiling does not show that
building the profile was worthwhile. Let setup cost $`S`$ include task
generation/access, all policy rollouts and labels, retained data, profile
construction, and the checks that make it usable. For a horizon $`H`$ fixed before deployment and the measured once-per-batch
assessment cost $`h`$, the successful-branch condition is

```math
H L_{\widehat\pi,b}(\lambda)-t_{\widehat\pi}(\lambda)>S+h.
```

It requires fresh future requests from the stated law and the stated initial
state. The profile sample and future requests are independent under that
model; conditioning on the acquired profile fixes the selected policy,
prices and horizon. A selected deterministic query or an outcome-selected
future stopping time does not automatically satisfy this condition. A large
postulated amortization horizon is an assumption, not observed deployment.

The no-certificate branch still incurs setup and assessment. An acquisition
policy needs its own bounded decision model, an explicitly accepted
exploration cost, or an independent assessment of the complete
profile-then-select procedure. A hard depth/budget ends this process without
proving optimality of its last unassessed controller.

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

### 4.1 A frozen-profile audit and a rebuilding audit answer different questions

A warm-profile audit freezes one previously acquired profile and samples
fresh deployment episodes. A rebuilding audit instead makes the *whole*
profile-acquisition, selection and deployment procedure the sampled object.
Each episode then includes all internal profile samples and their costs.
Its initial profile is absent, its algorithm is fixed, and it is bounded even
when the profile fails to produce a useful certificate.

The latter direct audit does not require every internal confidence interval
to cover its target. Those successes and failures are part of the complete
procedure's distribution. Apply the bounded-mean inequality to the actual
all-in episode outcome. No extra union over internal profile error events is
needed for that outer expected-performance statement. A claim that all
internal certificates were simultaneously correct would require its own
error allocation.

The outer audit's procurement bill remains a further setup expense. A fresh
positive lower bound can justify later deployment conditional on the audit
coverage event; it does not retroactively prove that acquiring that audit
was an optimal initial decision. The stage boundary and the absence of a
self-endorsement theorem are substantive parts of this construction.

### 4.2 A precise acquisition-identification obstruction

The [fixed-law diagnostic](../checks/07_acquisition_boundary.py) makes the
uncertainty about benefit explicit. An attempt costs one-half. It either
returns a checked correct answer or fails, in which case fallback costs one.
The unknown population completion rate is either $`9/20`$ or $`11/20`$.
Thus the true per-request saving over immediate fallback is respectively
$`-1/20`$ or $`1/20`$. Outcomes within this diagnostic are stipulated
independent completion observations; they are not results about the modular
adapter's empirical success rate.

Consider fixed-size profile acquisition that must identify the sign with
probability at least three-quarters under **each** law. The likelihood ratio
for $`n`$ observations is monotone in the number of successes. Symmetry makes
majority, with an unbiased tie decision, optimal for this symmetric minimax
criterion. The best accuracy is
$`(1+\mathrm{TV}(P^n,Q^n))/2`$, equivalently the corresponding binomial
majority probability. Exact rational calculation gives the first qualifying
sample size **45**; at 44 the best accuracy is approximately 0.745767, and at
45 it is approximately 0.750561. The
[independent derivation and saved-evidence audit](../work_logs/P3_07_2026-10-09_S1/reviews/proof_agent/acquisition_subreview/independent_derivation.md)
reconstruct the same threshold without reusing the implementation's formula.

A weaker analytic necessary condition follows from
$`\chi^2(P\Vert Q)=4/99`$,
$`1+\chi^2(P^n\Vert Q^n)=(103/99)^n`$, and
$`\mathrm{TV}(P^n,Q^n)\leq\tfrac12\sqrt{\chi^2(P^n\Vert Q^n)}`$:
three-quarter accuracy requires $`(103/99)^n\geq2`$, hence $`n\geq18`$.
This is a lower bound, not the exact 45-sample threshold.

For 128 later requests, the largest possible good-law gross improvement is
$`128/20=32/5`$. The exact identification minimum costs $`45/2`$ before
any assessment overhead, so it cannot repay that bill even under the good
law. At most 12 observations fit below the gross-improvement ceiling; their
best sign accuracy is
$`32415876138437/51200000000000\approx0.633123`$.
This is an obstruction to **that fixed-size, two-sided identification duty**.
Safe abstention can always decline to claim a sign. Adaptive acquisition,
other priors, different success laws and longer horizons are separate
problems; this calculation is not their impossibility theorem.

A separate perfect-diagnostic witness shows why a prior acquisition judgment
needs additional information. Under different laws with completion rates
zero or one, one half-cost probe reveals which service is present. Over four
future requests, its net gain is three-halves in the good state and minus
one-half in the bad state. It has positive prior expected gain exactly when
the prior probability of the good state exceeds one-quarter. The diagnostic
therefore does not license a law-free assertion that investigating the
benefit of thinking must pay.

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

## 6. Bounded implementation and development evidence

The final arithmetic path uses adapter **v1.1**, paired controller **v3**,
and development driver **v3**. The
[source-bound run](../work_logs/P3_07_2026-10-09_S1/development/run_v3/result.json)
and [source snapshots](../work_logs/P3_07_2026-10-09_S1/development/run_v3/sources/07_paid_reasoning.py)
identify the exact bytes. Every observation below is **DEVELOPMENT**. The
seeded runs are reproducible realizations; IID sampling is a mathematical
model assumption, not something demonstrated by a pseudorandom seed.

### 6.1 What is actually bought and charged

A query asks whether $`a^n\bmod m=r`$, with $`a\leq8191`$,
$`n\leq192`$ and $`2\leq m\leq97`$. The public adapter admits bounded
ASCII identities and exact bounded integers. Its right-to-left binary
producer and separately written left-to-right checker must agree before
paid acquisition can return an answer. Every policy can use the same public
cache lookup and elementary identities. The present cohort resets the cache
and all pending jobs for each query.

The catalogue consists of fallback, guess 0, guess 1, six-transaction compute
then fallback, twelve-transaction compute then fallback, and nineteen-
transaction full computation then fallback. Each includes the common paid
half-probability report, public cheap operations, and its terminal emission.
No unacquired answer is exposed in a progress record. A response has 1,024
abstract units, with explicit reserves for cancellation and terminal output;
spent work remains spent after a timeout. A zero budget produces no report
or action. The full computation fits within the proved finite adapter cap
on this input domain; the wrapper's additional operations are included in
its own cap. This is a bounded arithmetic service, not a hardness claim.

The fourteen retained features are false positives, false negatives,
fallbacks, and eleven resource categories. Those categories are admission,
solving, checking, acquisition, storage, cache access, forecasting,
assessment, profiling, dependency compilation and repair search. The last
two are zero in the arithmetic adapter because those operations are absent;
§6.5 measures them in an actual separate dependency/repair example.

The tariff counts declared bounded primitive operations and 64-bit word
accesses. It is not elapsed CPU time, Python memory usage, or a claim that
all real-world administrative work has negligible cost. Source registration,
profile construction and numerical readout are explicitly priced. Raw audit
serialization and diagnostic snapshots are experiment instrumentation and
cannot be read by the deployed selector as a source of otherwise unpaid
information. Human theorem and program development are research activities,
not measured deployment operations under this tariff.

The immutable profile binds the controller, adapter, catalogue, feature
meaning, request generator, reset state and observation schedule. Bounds are
admitted from the declared analytic catalogue, not from favorable observed
extrema. Construction funds validation and hashing before producing the
profile. Assessment pays for identity admission, feature reads, exact
rational bounds and selection; its final arithmetic is prepaid and bounded.
The selector reserves a valid fallback/output path for insufficient budgets.

### 6.2 Stakes, objectives and improved estimates

The fixed development law is uniform over 248 public queries: for primes
17, 31, 47, 61 and 97, take every $`1\leq a<p`$, exponent
$`(p-1)/2`$, and target residue 1. Half the answers are true. The profile
uses paid full-policy rollouts at four prospectively fixed sample sizes:
128, 256, 512 and 1,024. One simultaneous event covers all checkpoints.
The final run checks every acquired interval against a separately acquired
exact population table; all four coverage checks pass on this realization.
This is a development falsification check, not empirical proof of a 95%
coverage frequency.

At 1,024 samples, setup totals **1,692,957 units**. At one-thousandth loss
unit per resource unit, setup costs 1,692.957 and a full assessment costs
3.893. The low-stakes prices are $`(1,1,1/5)`$ in the false-positive,
false-negative and fallback basis; high stakes are $`(100,100,20)`$.
The asymmetric rows replace one error price by 1. Storage-expensive pricing
uses the high task prices, storage at one-tenth and other resources at
one-thousandth. The zero-task row prices all three task features at zero.

| Price case | Selected continuation | Lower saving per fresh query | All-in lower gain, $`H=64`$ | All-in lower gain, $`H=10{,}000`$ |
|---|---|---:|---:|---:|
| Low stakes | fallback | 0 | -1,696.850 | -1,696.850 |
| High stakes | full computation | 16.892187 | -615.750031 | 167,225.020117 |
| False positives expensive | guess 0 | 16.940231 | -612.675195 | 167,705.463232 |
| False negatives expensive | guess 1 | 16.940231 | -612.675195 | 167,705.463232 |
| Zero task prices | fallback after gross screen | 0 | -1,694.254 | -1,694.254 |
| Storage expensive | full computation | 1.869517 | -39,067.807906 | -20,492.286102 |

These are conditional lower bounds for the stipulated future horizon, not
observed savings on 10,000 deployed requests. The setup and once-per-batch
assessment are subtracted exactly once. Storage-expensive setup is
39,117.036 and assessment is 70.421. The zero-task gross screen costs 1.297;
it can reject that assessment route but does not refund the profile.
Exact fractions and all 72 checkpoint/price/horizon rows are retained in
[selections.json](../work_logs/P3_07_2026-10-09_S1/development/run_v3/selections.json).

More observations change **one** continuation in the six-case development
comparison: under expensive storage, the first three checkpoints choose
fallback and 1,024 samples choose full computation. High stakes choose full
computation at every checkpoint, with a stronger lower bound as data accrue.
The two asymmetric cases keep their respective cheap guesses. Those guesses
are conservatively certified but are not the exact best policies: the exact
population table prefers full computation in both cases. Low and zero task
prices retain fallback. Thus improved estimates sometimes change a decision,
but neither more data nor a positive lower bound implies optimal selection
or acquisition payback.

### 6.3 Two bounded assessments of the actual procedure

The warm-profile audit freezes the final 1,024-row profile and controller,
then draws 256 fresh batches of 16 queries. The profile is already acquired;
the audit's future episode contains its paid assessment and selected policy
execution. Its mean episode costs are 7.9654375 for the controller,
307.437296875 for fallback and 4.0724375 for charged full computation. Its
95% lower expected gain over fallback is
$`246661639/1024000\approx240.880507`$ per batch. The controller pays
exactly 3.893 more than simply using the charged full solver on these
batches. Audit procurement plus final checking adds **4,057,527 units**;
that setup is outside the reported future-deployment gain. See the
[frozen closure and audit](../work_logs/P3_07_2026-10-09_S1/development/run_v3/self_audit.json).

The separate **whole-audit v2** starts every sampled episode without a
profile. It pays for 64 profile queries, freezes that profile, assesses it,
and serves 64 fresh requests at the high prices. Its source closure binds
both generator files. The hard whole-episode resource cap is 628,752 units;
the paired scalar saving lies in $`[-5748.752,1280]`$. Profiles and selections
are written before their future query draws. Each episode includes its own
profile expenses, including unhelpful acquisition if that were to occur.
The outer audit is fixed before its 256 fresh development episodes.

| Whole-audit quantity | Exact result | Decimal interpretation |
|---|---:|---:|
| Mean controller all-in episode cost | $`44446187/256000`$ | 173.617918 |
| Mean fallback episode cost | $`78733879/64000`$ | 1,230.216859 |
| Mean charged-exact episode cost | $`4172681/256000`$ | 16.299535 |
| Mean all-in saving over fallback | $`270489329/256000`$ | 1,056.598941 |
| 95% lower all-in saving over fallback | $`1211017049/4096000`$ | 295.658459 |
| Additional outer audit procurement | $`11281921/200`$ | 56,409.605 |

All 256 episodes select full computation. The lower bound is a direct
complete-procedure statement of §4.1, so internal profile success is not a
separately assumed event. The larger outer procurement bill still needs its
own acquisition judgment or amortization assumption. These results show a
bounded self-assessment with useful fallback avoidance. The charged exact
solver remains substantially cheaper. The
[independent v2 review](../work_logs/P3_07_2026-10-09_S1/reviews/whole_audit_agent/review_v2.md)
reconstructs all 256 profiles and selections, 32,768 sample indices, resource
vectors, the 45,598-unit global startup and final bound from saved evidence.
No stronger reflection or universal self-evaluation claim follows.

### 6.4 A stronger ordinary comparator removes much of the acquisition cost

The [analytic companion](07_ordinary_analytic_profile.md) proves a special
property of this population. At a fixed prime, the three classes are base 1,
base minus 1, and all other nonzero bases. Algebra determines the exact
positive/negative count of each class. The current flat-tariff adapter's
execution resources and completion status are constant within each class
and policy. Individual unresolved guess errors are **not** class-constant;
their aggregate counts come from the algebraic lemma.

The ordinary comparator executes one paid representative per class for each
policy, constructs and retains the exact population feature means, and pays
for exact repricing. Its source-bound numerical table is frozen before the
retained exhaustive population is opened for external checking. All 1,488
query-policy resource/completion rows and class feature sums agree.

| Acquisition route | Resource units | Evidence needed before selection |
|---|---:|---|
| Sampled 1,024-row profile | 1,692,957 | Paid paired rollouts and simultaneous statistical bounds |
| Exhaustive finite profile, excluding 248 private `pow` diagnostics | 359,918 | Paid full-policy rows for every query |
| Analytic class profile v2 | 64,581 | Source-specific algebra/path lemmas and 15 paid representative queries |

At ordinary resource prices the analytic setup costs 64.581 and one
assessment costs 0.740. It selects full computation under high or asymmetric
stakes and gives exact expected all-in gain about **1,149.624548** for a
64-query horizon. The sampled route's lower bound is negative at that horizon.
Under expensive storage, analytic setup costs 1,481.469 and assessment 25.688;
its exact all-in gains are approximately **-760.973258** at 64 queries and
**115,084.052677** at 10,000. Low and zero task prices still make acquisition
lose 65.321 relative to going directly to fallback.

These are source-specific consequences of a transparent small arithmetic
population. The hand-proved algebra and program-path lemma are explicit
prerequisites, not an uncharged generic theorem checker. Their human discovery
and program-development costs are unquantified by the deployment tariff.
The result demonstrates a strong ordinary opportunity in this domain; it is
not a physical runtime advantage or an optimality claim over all algorithms.
It also shows why the sampled method should not be evaluated against a
weakened control that is forbidden to exploit the same visible structure.

### 6.5 Actual dependency construction and admissible-repair search

The [dependency probe](../checks/07_dependency_paid_probe.py) invokes the
existing P3-05 dependency compiler and P3-04 admissible-repair search on a
four-bit paired program. It changes the left conjunction to disjunction,
retains the declared source condition and weights, and must account for both
minimum-rank witness worlds. Partial search can find one optimal witness
without proving all selected identities or the comparison interval. The
complete run uses 13 actual frontier pops, retains witnesses 1011 and 1100,
and returns the exact comparison image $`\{0,1\}`$ and hull $`[0,1]`$.
A separately enumerated sixteen-world checker validates the frozen result;
source mutation is rejected by its version binding.

At the saved unit multiplier and fallback fee one, checking plus retention
alone costs 0.61339, suggesting a saving of 0.38661. Adding actual dependency
construction and search makes the total **1.79639**, hence net gain
**-0.79639**. The components are construction 0.085, search 1.098, checking
0.52335 and retention 0.09004. The fifteen saved price cases and corrected
short-circuit accounting are in the
[v2 evidence](../work_logs/P3_07_2026-10-09_S1/development/adapter_agent/dependency_probe_v2/results.json)
and [independent review](../work_logs/P3_07_2026-10-09_S1/reviews/dependency_paid_diagnostic.md).
This is a retrospective operation-tariff diagnostic. It is not a learned
forecast that supplies its own future cost for free, and it does not redo or
alter the completed counterfactual semantics.

### 6.6 Forecast-conditioned actions and the full-feedback limitation

The [multi-action companion](07_multi_action_forecasting.md) extends the
surviving P3-06 defensive-forecasting construction to four explicit roles:
act 0, act 1, fallback and purchase of a guaranteed checked exact answer at a
fixed stated fee. It proves a finite fixed-role regret bound using continuous
quadratic smoothing, a sharp regularization constant, a paid dyadic sampler
and a separate sampling-noise condition. A restricted numerical bit-growth
result specifies the fixed-denominator and precision conditions. These are
conditional adaptations of the existing potential argument; they do not
replace uncertain-completion profiling by a guarantee that every available
computation succeeds.

In all three 32-query v2 development cases, the forecaster's ideal mixture
satisfies the recorded fixed-role inequalities. The controller's actual
all-in costs are approximately 640.419, 638.761 and 642.014, while always
buying the exact answer costs 368 in each case. The protocol acquires exact
feedback on every query to settle the forecast, even when the selected role
did not buy it. Always buying is therefore an especially strong ordinary
control: it pays the same mandatory exact-feedback service, incurs no error
or fallback loss, and avoids forecasting/selection overhead. This pathwise
cost argument explains the unfavorable results. An ideal mixture guarantee
is not a claim of lower charged total cost.

Selective settlement only on purchased queries would change the martingale
and potential accounting. The companion gives a simple selection-bias
witness; it does not declare the unmodified full-feedback guarantee valid
under that cheaper schedule. The current extension is technically checkable,
with a precise negative service comparison, and leaves a selective-feedback
method as an unproved later research question.

## 7. Sources, verification and evidence boundaries

The [primary-source cards](../literature/07_paid_reasoning_sources.md) compare
this construction with ordinary metareasoning, conditional performance
profiles and held-out policy evaluation. Russell and Wefald and Hay et al.
already make computation an action with consequences and costs. Hay et al.'s
finite-stopping conclusions have stated positive-cost and bounded-utility
conditions; they do not provide an acquired omniscient performance law.
Zilberstein and Russell's conditional profiles and Callaway et al.'s learned
metareasoning make profile/model scope and online deliberation expense
material. Callaway et al. charge online metareasoning time in their simulation
budget while excluding offline training from that deadline formula; that is
a deployment/amortization distinction, not grounds to describe the entire
source method as ignoring costs.

The bounded-mean acquisition guarantee uses Hoeffding's inequality. Thomas,
Theocharous and Ghavamzadeh provide a directly relevant held-out policy
evaluation/selection antecedent. Repeated adaptive checks need an allocated
event budget or an appropriate confidence sequence, as in the separately
reviewed off-policy confidence-sequence source. No new priority claim is made
for these ingredients. The comparison with P3-06's defensive forecasting
inherits its verified source contract and preserves its original addendum
and evidence.

The independent reviews are **same-model, targeted and nonblind**. They
reconstruct mathematics and exact saved data but are not outside peer review
or a final challenge. Current versions are source-bound; earlier v1/v2
snapshots and failed probes remain preserved. Found and repaired defects
include unpaid profile identity construction, missing numerical admission,
insufficient-budget use of an unvalidated fallback name, unfinished-job
cleanup, omitted generator scope, unpaid whole-audit startup, settlement
mutation before final size validation, and a random draw before its charge.
Each repaired path has focused checks and, where behavior or closure changed,
separately versioned fresh development evidence. A passing numerical result
under an old source is not silently reassigned to the repaired version.

The strongest supported statement is a bounded, paid complete-policy
comparison under a declared request law, with explicit acquisition and
self-assessment boundaries. It is an ordinary expected-cost construction
that can use cost-oriented features and the earlier mathematical forecast.
The worked examples establish stakes sensitivity, one observed checkpoint
decision change, conditional certificates and several cost reversals.
They do not establish broad resource efficiency, unrestricted mathematical
learning, rationality under every new objective, general self-endorsement,
or a performance advantage over strong ordinary controls.

Task-boundary accounting and the substantive contribution assessment are
recorded separately. P3-N01 remains NOT YET SUPPORTED pending that assessment;
clock time and test counts cannot settle it. P3-B and P3-08 remain unattempted,
and no final challenge is frozen or exposed.
