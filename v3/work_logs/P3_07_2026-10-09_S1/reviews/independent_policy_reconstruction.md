# P3-07 — independent reconstruction of finite paid-policy certificates

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal subagent**.  
Date: October 9, 2026 UTC. Base commit:
`c7386f115bf60a9eb3a419515c844b81fc6ba073`.  
Resource cost of agent research: **unmeasured; zero principal-clock credit**.

**Independence boundary.** The initial complete-policy reconstruction and the
sunk-assessment obstruction below were formed without seeing the root's proof.
The task prompt was nonblind: it suggested the finite complete-policy principle
and named failure modes. After the initial reconstruction was communicated,
the root described a paired-feature repricing extension and a two-stage own
procedure audit. Those portions are targeted, nonblind review. This is an
independent same-model derivation within those limits, not external validation.
No main artifact, clock, ledger, task plan, gate, or publication was edited.

## 1. Contract inherited, without reopening completed tasks

The target is the outstanding P3-07 item in
[TODO_v3.md](../../../../TODO_v3.md). Its resource and information contract is
[problem contract §§5–6 and §8](../../../foundations/01_problem_contract.md).
The load-bearing inherited restrictions are:

- [CB01/03](../../../foundations/01_composition_boundaries.md): equal access
  permits different purchased histories; selected comparisons need jointly
  applicable uncertainty bounds.
- [CB05](../../../foundations/01_composition_boundaries.md): a common joint-law
  constraint cannot be silently replaced by independent conditional choices.
- [Representation boundaries §2](../../../foundations/01_representation_boundaries.md):
  mathematical determination by program text does not grant cheap computation
  of its output or its metalevel conditional law.
- [Acquisition/profile review §1](../../P3_01_2026-10-07_S1/reviews/acquisition_and_profile_boundary.md):
  performance profiles need a population, readable conditioning variables,
  acquisition and checking costs, version and reuse conditions.
- [Resource review RI01/04/06/07](../../P3_01_2026-10-07_S1/reviews/resource_information_stress.md):
  machine permissions, setup costs, selected feedback and model identification
  remain separate obligations.

The results below discharge a finite composition question under explicit
hypotheses. They do not repeat the learning, counterfactual, or transport tasks
already completed in P3-01–06, and do not claim a new learning theorem by
renaming the quantities as values.

## 2. The object to compare is a complete bounded policy

Fix a deployment episode specification before profiling. An episode can be one
query or a finite block of queries. A complete policy fixes its behavior after
**every** admitted observation history: which computation to request, what to
do after a checked answer, timeout, unresolved result or checking failure, and
which terminal action to take. Its internal choices may be adaptive. Fix its
code/dependency closure, initial state, readable inputs, stopping horizon,
tie rules, and failure behavior. Internal learning is allowed if its complete
update procedure is fixed and is evaluated as part of the episode.

Let `Pi={pi_1,...,pi_M}` be a finite catalogue, and let `pi_0` be a declared stop
or fallback policy. In the basic empirical theorem, this catalogue and baseline
are fixed before the profile sample. The baseline may inspect the same initial
readable input by its declared procedure. It is not selected afterward using
an uncovered noisy comparison.

Each candidate must satisfy the hard resource contract on every admitted
execution path. This can follow from an explicit finite-tree bound or a
budget monitor with bounded abort/fallback behavior. Profile means of resource
use do not establish a hard bound. Reserve the resources needed for checking,
dispatch and fallback; include timeout and failure paths. Peak memory and other
nonadditive hard constraints require their own monitors; they cannot silently
be treated as an additive expected resource account.

Let `Z` denote a fresh episode drawn from a specified stable law `P`. It includes
the sampled deterministic query, declared environmental randomness and any
policy seeds. `P` is used in the theorem; it is **not** supplied to the reasoner
as a free oracle. A profile obtains information by charged executions and
observations. Hidden truth labels used to measure task loss must be obtained by
the declared mechanism. Unresolved or censored labels cannot be scored as zero
loss, and an evaluator-only label is not a free agent feature.

This is a population claim about a fresh episode. It is not a pointwise claim
about the gain on an already fixed unresolved deterministic mathematical query.
Conditioning on a particular query afterward needs conditional/stratified
coverage or an explicit structural transport premise. Randomizing the query
index does not make its fixed mathematical answer stochastic.

Define the gain, initially at a root **after common assessment has been paid**,
by

```math
g_\pi(Z)=J_0(Z)-J_\pi(Z),\qquad \mu_\pi=E_P[g_\pi(Z)],\qquad g_0=0.
```

`J_pi` includes terminal task loss and all resources remaining to execute that
complete policy: forecasting, feature access, proof/evaluation, acquisition,
storage/access, checking, dependency construction, repair search, failure
handling and terminal action costs where relevant. The distinction between
this post-assessment root and an earlier immediate-stop comparison is essential
and is quantified in §7.

## 3. Abstract finite root certificate

**Theorem R1 — conditional root safety.** Suppose the procedure obtains lower
certificates `L_pi(D)` satisfying, on one event `E`,

```math
L_\pi(D)\le\mu_\pi\quad\hbox{for every }\pi\in\Pi.
```

Include `L_0=0`; choose any maximizer of `L_pi` over `Pi` and `pi_0`, with an
announced tie rule favoring stop at zero. Then, on `E`,

```math
\mu_{\widehat\pi}\ge L_{\widehat\pi}
   =\max(0,\max_{\pi\in\Pi}L_\pi)\ge0.
```

**Proof.** The event controls all candidate policies simultaneously, hence also
the data-selected candidate. The selected certificate is at least the zero
certificate. These two inequalities give the result. There is no claim that
each realized deployment improves, or that every individual query improves.

If `Pr(E)>=1-delta`, the conclusion is a `1-delta` statement over profile data
about expected fresh-episode gain. It is not an unconditional assertion that
the randomized profile-then-select procedure has nonnegative expected gain.
For example, if every continuation gain is at least `-A`, its expected gain
over profiling randomness is bounded below by `-delta*A`; profile costs still
need to be subtracted.

**Credal construction.** A sufficient way to obtain the common event is a
nonempty set `Q_D` of admissible **joint** deployment laws with
`Pr(P in Q_D)>=1-delta`, and a checked number satisfying

```math
L_\pi\le\inf_{Q\in Q_D}E_Q[g_\pi].
```

The certificate must lower-bound the infimum. A found feasible law provides
an upper bound on a minimization problem and cannot certify this lower bound.
An exact finite enumeration, a valid dual lower certificate, or a sound outer
enclosure with accounted numerical error may suffice. An empty uncertainty
set returns conflict/infeasibility; it never licenses a favorable vacuous
bound. Search and validation consume their announced resources.

Joint-law uncertainty may be nonrectangular. Evaluating complete policies at
the original root does not require rectangularity. Replacing their prescribed
continuations after observing a branch gives a different policy, which needs
its own certificate. A loose independent outer approximation remains safe if
it really contains the original joint family, but can lose useful decisions.

## 4. A finite acquired-profile construction

Suppose the execution record has a fixed feature vector `z_pi(Z)` in `R^K`.
For example, coordinates can be error indicators for declared task types and
separate resource counts. Retain the **paired differences**

```math
d_{\pi j}(Z)=z_{0j}(Z)-z_{\pi j}(Z),\qquad
m_{\pi j}=E_P[d_{\pi j}(Z)].
```

For every policy and feature, require a known finite range
`a_pi,j <= d_pi,j <= b_pi,j`, of width `R_pi,j=b_pi,j-a_pi,j`. Profile `n`
fresh IID episodes from the same law and acquire the required paired feature
records. Executing the policies on one common task row is allowed; results
within that row may be dependent. Policies need appropriate resets or isolated
state. The cost of running every policy, obtaining task labels, storing the
records and checking them belongs to the profile account.

For integers `M,K,n>=1`, `0<delta<1`, and exact sample means `mhat_pi,j`, let

```math
e_{\pi j}=R_{\pi j}
\sqrt{\frac{\log(2MK/\delta)}{2n}}.
```

If `R_pi,j=0`, its known constant coordinate needs no sampling. The following
derivation covers the conservative choice of keeping it in `MK` anyway.

**Theorem R2 — simultaneous finite profile box.** With probability at least
`1-delta`, all `MK` inequalities

```math
|\widehat m_{\pi j}-m_{\pi j}|\le e_{\pi j}
```

hold simultaneously.

**Proof, including the bounded-variable concentration step.** For a bounded
scalar `X` with range width `R`, let
`psi(t)=log E exp(t(X-E X))`. Under exponential tilting,
`psi''(t)` is a variance. Any variable supported on an interval of width `R`
has variance at most `R^2/4`, since its mean minimizes expected squared
distance and the midpoint gives squared distance at most `R^2/4`.
As `psi(0)=psi'(0)=0`, integrating twice gives
`psi(t)<=t^2 R^2/8`. For `n` independent copies, multiplication of the
exponential moments and Markov's inequality give

```math
\Pr(\widehat m-m\ge u)
 \le\inf_{t>0}\exp(-ntu+nt^2R^2/8)
 =\exp(-2nu^2/R^2).
```

The negative tail follows by replacing `X` with `-X`. Taking both tails and
union bounding over `MK` coordinates gives R2. Independence between policies
or between feature coordinates is unnecessary. The argument is a
self-contained bounded-variable proof, not a source theorem imported with
unstated hypotheses.

### 4.1 Repricing all fixed linear objectives on the same event

For a request-specific coefficient vector `lambda`, let

```math
\mu_\pi(\lambda)=\lambda\cdot m_\pi,\qquad
B_\pi(\lambda)=\sum_j|\lambda_j|e_{\pi j},\qquad
L_\pi(\lambda)=\lambda\cdot\widehat m_\pi-B_\pi(\lambda).
```

On the event in R2,

```math
L_\pi(\lambda)\le\mu_\pi(\lambda)
 \le\lambda\cdot\widehat m_\pi+B_\pi(\lambda)
\quad\hbox{for every }\pi\hbox{ and every }\lambda.
```

**Proof.** Expand `lambda dot (m_pi-mhat_pi)` and bound each summand in
absolute value by `|lambda_j|e_pi,j`. This is a deterministic implication of
one finite simultaneous event. It therefore permits even a data-chosen
coefficient vector, without union bounding over the uncountable price space.
Signed coefficients are allowed algebraically; operational resource prices
still obey the task's pricing rules.

**Additional bounded catalogue guarantee.** Let `pi_star` maximize the true
mean gain, including zero for stop, and let the selector maximize `L_pi`.
On the same event,

```math
0\le\mu_{\pi^*}(\lambda)-\mu_{\widehat\pi}(\lambda)
 \le 2B_{\pi^*}(\lambda).
```

Indeed, `mu_hatpi >= L_hatpi >= L_pistar >= mu_pistar-2B_pistar`.
This statement compares the fixed catalogue at the post-assessment root.
It does not compare all possible programs. A generic sound credal lower bound
need not have the width control needed for this regret bound.

**Repricing restrictions.** Every policy's actual action map, primitive
semantics, population and feature interpretation must remain fixed. If the
controller changes its branches when prices change, then `d_pi(Z;lambda)` is
a different function; one may instead cover every induced complete policy in
the finite catalogue. A changed baseline likewise requires covered comparison
pairs. A changed query distribution is not a price change. Per-query weights
`lambda(X)` cannot be multiplied by an unconditional feature mean; retain
the relevant weighted/contextual features, use justified stratified coverage,
or obtain new data. The model must also preserve any report-induced effects.

For the native representation, each actual requested coefficient may be a
known rational. The all-coefficient mathematical statement does not install
variable multiplication, arbitrary exact real literals, or free arithmetic
inside the inherited finite piecewise-affine kernel.

### 4.2 Numerical and observation errors

If the stored mean is `mtilde_pi,j` and a checked acquisition/arithmetic bound
gives `|mtilde_pi,j-mhat_pi,j|<=eta_pi,j`, replace each radius by
`e_pi,j+eta_pi,j`. If a sample outcome remains unresolved, an admitted interval
for its true feature gives a corresponding observation-error allowance;
discarding unresolved cases generally changes the sampled population.

Use certified upper approximations for radii and adverse cost terms, and a
lower approximation for the final dot product. Subtract an explicit bound for
any remaining final-evaluation error. A positive floating-point number with no
error contract is not a certificate. The logarithm/square-root formula is a
mathematical specification; a bounded implementation can use rational outer
enclosures and a capped, charged verifier. The verification cap must include
its final check and dispatch, so accounting does not recur indefinitely.

## 5. Adaptive profiling needs prefix-valid sampling

The fixed-`n` theorem does not cover looking repeatedly and stopping when a
certificate becomes positive. For a deterministic profile cap `Nmax`, a
sufficient replacement is

```math
e_{\pi j,n}=R_{\pi j}
\sqrt{\frac{\log(2MKN_{\max}/\delta)}{2n}},
\qquad 1\le n\le N_{\max}.
```

Union bounding over all policies, coordinates and prefixes gives a common
event valid for every stopping rule within this cap. Zero observed samples
require a previously justified range, not a fabricated empirical mean.

Adaptive choice of which policy to profile also needs a sampling premise.
One sufficient protocol chooses the policy before drawing a fresh episode
whose conditional feature mean remains the fixed `m_pi`. Independent sample
stacks for each fixed policy give this directly. More generally the same
exponential-moment proof applies to bounded increments with that fixed
conditional mean. Each policy's random final sample count can then use the
uniform prefix event. Choosing only favorable tasks after inspecting their
features, changing the policy while profiling it, or keeping only successful
runs does not satisfy this premise. Importance weighting, conditional models
or other corrections would require separate assumptions and error bounds.

**Finite optional-stopping failure witness.** Let `X_i` be IID fair signs,
with true mean zero, and `S_n=sum_i X_i`. At every fixed `n`, the event

```math
S_n>0,\qquad S_n^2>6n
```

has probability at most `exp(-3)<1/20`. The strict inequality is certified
arithmetically by the finite series lower bound
`sum_{k=0}^8 3^k/k! > 20`. Thus the corresponding fixed-time lower confidence
test is individually better than 95 percent.

Nevertheless, stop at the first such event by `n=2000`. An exact integer
dynamic program counting all `2^2000` sign sequences gives false-positive
probability **0.1128366373085338**, exceeding five percent. This is an exact
finite count, not a simulation or an appeal to an asymptotic stopping result.
The script and exact rational probability are preserved in
[the check result](proof_agent/policy_proof_checks_result.json).

## 6. Two-stage bounded assessment of the reasoner's own procedure

A clean own-program audit has two stages:

1. Use development information to construct a bounded procedure and its
   initial state. Freeze the complete version before audit data are seen.
2. Acquire fresh independent audit episodes from the stated deployment law,
   execute reset/isolated copies of that frozen procedure and the baseline,
   and measure their paired task/resource features by the announced mechanism.

Conditioning on the development stage leaves a fixed procedure, so R2 applies
to the audit stage. A whole finite learning episode may be the unit of
observation: the frozen program is allowed to update internally within it.
If the live state instead changes across nominally IID audit cases, the
simple fixed-function proof no longer applies. Reset the assessed state,
evaluate independent complete episodes, or supply an appropriate sequential
replacement theorem.

The identity covers code, dependencies, parameters, initial caches, budget,
schedule, loss interpretation, observable metadata and report/environment
interaction. A source-code hash alone does not fix those components. Audit
instrumentation must not change the target law invisibly. A finite audit
certifies only the specified population-mean property; it is not unrestricted
self-trust, universal correctness, or a proof of the evaluator's soundness.

Selecting between the audited complete program and stop using its lower
certificate is covered, after charging the wrapper and gate. Modifying the
program in response to audit failures and reusing the same uncorrected audit
does not inherit the statement. A finite predeclared family, new independent
audit data, a prefix/version allocation of failure probability, or a proved
transport bound can restore an appropriate claim. For example, a proved
gain change of at most `rho` transports an old lower bound as `L_old-rho`;
merely assigning a new version identifier does not prove that premise.

## 7. Assessment is itself paid: the earlier-root obstruction

Suppose `C(D)` is the actual paid profile plus selector/checking setup cost
relative to **immediate stop before assessment**. It includes assessment of
all inspected candidates, not just the one selected. Consider `H` actual fresh
deployment episodes of the selected complete policy under the stated law.
On R2's event, the exact accounting identity and its certificate are

```math
E[\text{total gain}\mid D]
   =H\mu_{\widehat\pi}-C(D)
   \ge H L_{\widehat\pi}-C(D).
```

For the maximizer including stop, this becomes

```math
E[\text{total gain}\mid D]
 \ge H\max(0,\max_\pi L_\pi)-C(D).
```

Future policy-specific overhead belongs in `J_pi`; bounded future selector
overhead must be added to `C` or subtracted by an explicit upper allowance.
If `H` is an amortization assumption, report it and do not pretend it has
already been realized. Shared preparation can instead be common to both
comparators, with that conditional scope stated explicitly.

**Obstruction.** If assessment costs something and returns no positive
certificate, choosing fallback has gain `-C(D)` relative to immediate stop.
Calling that branch's gain zero silently moves the comparison root. Requiring
`H L_pi>C(D)` before accepting a candidate protects each accepted branch's
all-in conditional expectation, but the assessed-and-stopped branch still
loses its assessment cost. The same issue applies to online certificate
evaluation as to initial training. There is no general theorem that purchasing
the information needed to test a computation is itself profitable.

A valid finite alternative is a capped exploration statement. If
`C(D)<=Cmax` and every continuation gain is at least `-A`, then the rule has
unconditional total expected gain at least `-Cmax-delta*H*A`. A stronger
positive all-in conclusion needs sufficient certified deployment benefit,
shared/sunk setup, or a separately justified selection among complete
profile-then-select meta-policies. The latter must include its own assessment
costs; it does not create a free recursive oracle for the value of assessment.

## 8. Finite witnesses and what each one establishes

The planned check is
[policy_proof_checks.py](proof_agent/policy_proof_checks.py), with
[saved exact results](proof_agent/policy_proof_checks_result.json) and
[prospective review plan](proof_agent/review_plan.json). It uses standard-library
rational/integer arithmetic and preserves its first attempt. All output is
**DEVELOPMENT**, with no final challenge exposure.

| Witness | Exact result | Consequence |
|---|---|---|
| Complete policies and complementary computation | Two independent fair bits, XOR target, wrong-answer loss 1, each read costs 1/10. Exhaustive enumeration contains 74 deterministic policies. Stop costs 1/2; every forced one-read optimum costs 3/5; the best complete two-read policy costs 1/5 and gains 3/10. | Extends the inherited XOR diagnostic to every complete adaptive policy in this small catalogue. A one-step stopping rule misses the profitable two-computation plan. It does not prove global search efficiency. |
| Success rate omits relevance to the current decision | Baseline guesses zero, wrong cost 10, computation costs 1 and succeeds on half of fair-bit cases, with accuracy 1 conditional on success. Success exactly on baseline errors gives gain 4; success exactly on baseline-correct cases gives gain -1 for the same declared continuation. | Success rate, successful-answer accuracy and runtime alone do not identify decision value. The dependence between success and avoided loss matters. |
| Equal accuracy under unequal stakes | Two equally weighted contexts have stakes 1 and 9; the solver removes one baseline error indicator on average 1/2 and costs 2. Removing the low-stakes errors gives gain -3/2; removing the high-stakes errors gives gain 5/2. Both unweighted feature means and accuracies agree. | A marginal profile cannot support arbitrary context-dependent repricing. Mean stake times mean error reduction incorrectly returns 1/2 in both cases. |
| Shared-law root commitment and replanning | `X` is fair and `E[Y|X=0]=1-theta`, `E[Y|X=1]=theta`. Acquiring `X` costs 1/10; a complete policy incurs loss `Y`; fallback costs 3/4. Its root worst-case gain is 3/20. After either branch, a fresh conditional worst-case selector switches to fallback, giving total gain -1/10. | Shared uncertainty gives a valid root certificate; replacing its continuation with conditional choices invalidates that certificate. |
| Same accuracy, stale own procedure | Old exact solver costs 1/5 against stop task loss 1/2, so gain is 3/10. A revised exact solver costs 7/10, so gain is -1/5. Both have accuracy 1. | Old accuracy or old cost certificates do not assess the new procedure. Version identity includes resource behavior. |
| Mean resource use | Resource use is 0 or 4 with equal probability; mean 2 meets a nominal limit of 2 but violates that hard limit with probability 1/2. | Statistical average cost does not establish pathwise feasibility. |
| Paying before stop | Assessment cost 1/20 and subsequent fallback yield total gain -1/20. A positive deployment gain 3/100 still yields total -1/50 after that assessment cost. | Positive continuation value is insufficient for positive cold-start value. |
| Adaptively stopping the profile | Every fixed-time false-positive bound is below 1/20, but the exact chance of at least one crossing by 2000 is 0.1128366373085338. | Coverage must include the profile stopping rule. |

Four signed-price examples also enumerate all eight vertices of a
three-coordinate box and match the support-function formula exactly. These
checks illustrate §4.1; the algebraic proof, not that small grid, establishes
the all-prices result.

Improved forecasts need not change an action: under symmetric wrong-answer
loss, moving a probability report from 0.6 to 0.7 still selects the same label.
They can change a task decision when they cross its relevant threshold: with
fallback cost 0.2 and risky-action expected loss `1-p`, moving `p` from 0.55
to 0.85 switches from fallback to the risky action. These are threshold
calculations, not empirical learning results; actual decision improvement
still requires a valid bridge to the true priced loss.

## 9. Assessment of the candidate

**Supported as a conditional finite construction:** complete-policy selection
using a common lower certificate; a charged IID paired-feature profile giving
simultaneous bounds; price selection within the retained linear family;
finite prefix correction for adaptive sample size; and a bounded own-version
audit with a fresh independent audit stage.

**Required qualifications:** the profile law and current query scope must
match, label acquisition and resets must be genuine, policies and action maps
must be covered before selection, numerical lower bounds and hard budgets
must be enforced, joint constraints and root commitment must survive, and all
assessment costs must appear at their actual comparison root.

**Not established:** a profitable initial profile purchase in all cases;
pointwise correctness on unresolved mathematics; a cheap optimal search over
all complete policies; unrestricted self-assessment; arbitrary population or
version transport; a universal induction theorem; or advantage over a strong
ordinary metareasoning controller. An ordinary method can use exactly this
catalogue, joint uncertainty set, profile data and certificate rule. The
surviving result is an explicit finite composition guarantee and a set of
testable boundaries; any contribution claim needs a separately supported
delta and comparison scope.
