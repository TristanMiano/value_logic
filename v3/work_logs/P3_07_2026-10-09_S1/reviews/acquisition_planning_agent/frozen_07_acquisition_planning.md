# P3-07 — bounded acquisition and the cost of planning it

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
**Exact stipulated-law DEVELOPMENT diagnostic.** This companion sharpens the
[acquisition boundary](07_paid_reasoning.md#42-a-precise-acquisition-identification-obstruction).
A fixed-size sign-identification duty and an adaptive prior-expected-loss
policy are different services. This file analyzes both the useful distinction
and an additional obstruction that covers adaptive observation under the
particular supplied laws. It does not learn those laws or the prior.

## 1. A fully stated ordinary metalevel model

A service has one persistent completion parameter
$`\theta\in\{9/20,11/20\}`$, with prior probability one-half for each.
Conditional on that parameter, all profile and future completion observations
are independent Bernoulli trials. Each future attempted computation costs
one-half; success returns a checked correct answer, while failure incurs
fallback loss one. The saving against immediate fallback is therefore
$`\theta-1/2`$ per attempted future request. At a stopping decision, the
controller either uses fallback on all $`H`$ future requests or attempts the
service on all of them. It does not adapt those future choices or learn from
future outcomes in this particular policy class.

A profile trial costs one-half and yields one correctly observed completion
bit. This is a stipulated service contract, not a numerical claim about the
modular adapter. Profile observations have no separate object-level payoff.
The model's conditional independence and two-point prior are premises. They
are not an uncharged estimate of the expected value of thought: that value
is computed by the bounded planner below, and the planner's resource bill is
reported separately. Justifying or acquiring the model itself remains an
additional task.

The ordinary interpretation is direct. Computations are actions, observations
update a sufficient state, and stopping receives the best available expected
terminal utility. The [primary-source comparison](../literature/07_paid_reasoning_sources.md#pr07-1--s03--the-supplied-law-metalevel-decision-problem)
identifies Hay et al.'s metalevel MDP and its two-point-prior example. The
finite Bellman method here is an instance of that established approach.
No priority claim attaches to solving this tiny model.

## 2. Exact posterior and finite Bellman rule

After $`n`$ profile observations with $`s`$ successes, the posterior good-law
probability and predictive success probability are

```math
\pi_{n,s}=\frac{11^s9^{n-s}}{11^s9^{n-s}+9^s11^{n-s}},\qquad
q_{n,s}=\frac9{20}+\frac{\pi_{n,s}}{10}.
```

The best terminal gross expected gain is
$`M(\pi)=\max\{0,H(2\pi-1)/20\}`$. Let $`u`$ price one declared
resource unit. An initial table lookup costs $`8u`$. Each acquired
observation costs one-half, eight control units and the next state's eight
lookup units, so its total incremental cost is $`c'=1/2+16u`$.
The complete table's construction bill is $`h`$, paid before execution.

For a hard profile cap $`N`$, define

```math
W_{N,s}=M(\pi_{N,s}),\qquad
W_{n,s}=\max\left\{
M(\pi_{n,s}),
-c'+q_{n,s}W_{n+1,s+1}+(1-q_{n,s})W_{n+1,s}
\right\}.
```

Stop on a tie, and use fallback on a zero terminal-gain tie. Backward
induction proves that $`W_{n,s}`$ is the largest conditional expected future
gain within this finite profile-then-commit policy class, after the current
lookup has been paid. Every available observation leads to one of the two
child states; both continuation values are already computed. No further
benefit oracle appears in the recurrence. The root execution value is
$`W_{0,0}-8u`$, and the all-in value is $`W_{0,0}-8u-h`$.
The acquisition choice after paying $`h`$ uses the former continuation
problem; it does not try to recover that sunk bill by changing its decision.
A claim that constructing the table was initially worthwhile must retain
$`h`$ and the still-unquantified model-acquisition cost.

## 3. When even adaptive acquisition cannot help

There is a useful analytic bound beyond a twelve-observation computation.
For any prior good-law probability $`\pi\in[0,1]`$, one observation's
expected increase in the best terminal gross value is exactly

```math
\mathbb E[M(\pi')\mid\pi]-M(\pi)
=\frac H{20}\left[
(\pi-9/20)_+ +(\pi-11/20)_+ -(2\pi-1)_+
\right]\leq\frac H{400}.
```

To derive the identity, multiply each next-state posterior gain by its
predictive branch probability. On success, that weighted positive part is
$`(H/20)(\pi-9/20)_+`$; on failure it is
$`(H/20)(\pi-11/20)_+`$. Subtract the present gain. The expression vanishes
outside $`[9/20,11/20]`$, rises linearly to its maximum at one-half, and
then falls linearly. Thus the constant $`H/400`$ is attained.

If $`c'\geq H/400`$, the process
$`M(\pi_n)-c'n`$ is a supermartingale. For any bounded stopping rule,
conditional expected net improvement from acquiring observations is no
larger than immediate stopping. The same conclusion holds when the expected
stopping count is finite: apply the bounded result to $`N\wedge k`$,
use boundedness of $`M`$ for its terminal limit, and use monotone convergence
for the nonnegative cost. If the expected count is infinite, the expected
observation cost is infinite while terminal gain remains bounded, yielding
negative infinite expected net value. A nonterminating path supplies no
new finite terminal payoff.

For $`H=128`$, $`H/400=0.32<0.5\leq c'`$. **No adaptive profile-sampling
policy can improve prior expected value in this supplied model**, for any
initial prior, even before paying to construct its planning table. This
includes a larger class than the implemented twelve-observation cap. The
claim remains conditional on the fixed laws, observation contract, constant
cost and profile-then-commit terminal service. It is not an impossibility of
useful acquisition with other laws, extra free observations, a different
terminal action space or a longer deployment horizon.

## 4. Implementation and exact results

The [planner v1](../checks/07_acquisition_planning.py) evaluates both one- and
twelve-observation caps at four fixed horizons and three resource prices,
for 24 prospectively declared tables. It uses exact rational arithmetic,
checks 256-bit numeric bounds and binds its source, adapter tariff source,
model, policy table and procurement resources in a bounded numerical core.
Each state has a prepaid 128-unit arithmetic bundle and 64-unit read/retention
allowance. Source reading/hashing, admission and final table validation and
retention are charged before the corresponding work. These are explicit
bounded arithmetic/service allowances, not a measured Python CPU bound or
a machine-verified instruction count.

At the ordinary resource price $`u=1/1000`$, the one-observation table costs
12,282 units and the twelve-observation table 46,074. The construction cost
is charged per separately built table; amortizing it across later uses would
be a new declared sharing contract. Exact conditional-law forward propagation
uses only the selected actions and branch laws to reconstruct buying
probabilities, expected profile lengths and gains. It never consults the
Bellman values during that reconstruction. This is external validation,
not a free observation channel supplied to the controller.

| Profile cap | Future horizon | Root continuation | Prior gain after acquisition/control, before table cost | All-in prior gain including table cost |
|---:|---:|---|---:|---:|
| 1 | 128 | fallback | -0.008 | -12.290 |
| 12 | 128 | fallback | -0.008 | -46.082 |
| 1 | 512 | acquire | 0.756 | -11.526 |
| 12 | 512 | acquire | 0.756 | -45.318 |
| 1 | 4,096 | acquire | 9.716 | -2.566 |
| 12 | 4,096 | acquire | 22.612282 | -23.461718 |
| 1 | 16,384 | acquire | 40.436 | 28.154 |
| 12 | 16,384 | acquire | 104.286367 | 58.212367 |

The [saved result](../work_logs/P3_07_2026-10-09_S1/development/acquisition_planning_run_v1/result.json)
retains exact fractions and all 24 rows. At horizon 512, the larger planner
pays to compute many states but its executed policy still takes one sample.
At 4,096 it improves execution value but loses more after construction than
the smaller planner. At 16,384 it has positive prior expected all-in value
under the stated model and tariff. None of those future deployments was
actually run; these are exact conditional-law calculations.

For the twelve-observation, 16,384-request case, the expected profile length
is approximately 9.224131 under each law. It buys the future service with
probability about 0.366877 under the bad law and 0.633123 under the good law.
Its operating gains before table construction are approximately **-305.313633**
and **513.886367**, respectively. Their prior average is positive, but this
is neither three-quarter sign identification under each law nor a guarantee
of positive gain in each state. These figures make the difference from the
fixed-size identification duty explicit. The 45-sample threshold and the new
128-horizon adaptive obstruction remain true alongside the long-horizon
positive prior-value example.

## 5. Scope and review

This is a bounded ordinary expected-cost control using a supplied uncertain
model, not a free expected-benefit oracle. It does not prove that the prior is
correct, make the complete table cheap in a large problem, establish the
initial worth of model acquisition, or infer a general self-trust theorem.
The separate P3-07 whole-procedure audit addresses an actual versioned
mathematical adapter under its own empirical-law assumptions.

The source and 24 tables were frozen before their independent targeted
review. Review evidence is in
[reviews/acquisition_planning_agent](../work_logs/P3_07_2026-10-09_S1/reviews/acquisition_planning_agent).
Same-model, nonblind review and an exact stipulated-law diagnostic are not a
final empirical challenge. No earlier task source or evidence is replaced;
P3-B and P3-08 remain unattempted.
