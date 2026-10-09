# P3-07 companion — four paid decisions from one mathematical forecast

**Status: verified bounded companion result with finite DEVELOPMENT evidence.**
The sharp regularization and finite-bit rounding allowances, the enlarged-feature
regret readout, and the restricted numeric-state extension have been reconstructed.
The frozen v2 implementation passes focused failure-boundary review and exact
recomputation of its three saved 32-query cases. The evidence and its limitations
are recorded below; this status makes no P3-07 Research90 completion claim.

The [principal paid-profile result](07_paid_reasoning.md) concerns fixed
procedure performance over a request population. This companion asks what
the completed [P3-06 potential argument](06_cost_forecast_refinement.md)
can say directly about choosing among more than two priced actions on an
arbitrary binary mathematical-answer stream. It does not rerun or replace
P3-06's completed evidence.

## 1. Where a computation can be an affine action

At issuance $`t`$, the answer $`y_t\in\{0,1\}`$ is unresolved by the
reasoner. There are $`A\geq2`$ fixed action identities and known rows
$`c_{t,a}(y)=b_{t,a}+d_{t,a}y`$. The rows and a positive smoothing parameter
$`\eta_t`$, together with a nonnegative finite weight $`w_t`$, are available
before issuing the forecast and receiving its checked answer. They may change with
the announced objective or resource prices; the identities and positive
feature scales $`\gamma_a`$ remain fixed. All compared actions must be
feasible under their hard resource contracts.

The motivating four roles are:

| Role | Binary-outcome cost row |
|---|---|
| Act 0 | False-negative price times $`y`$ |
| Act 1 | False-positive price times $`1-y`$ |
| Fallback | Declared fallback loss |
| Buy exact | Known charged service cost, followed by a checked correct action |

The last row requires a specified procedure with guaranteed resolving and
checking behavior within the admitted budget. A known advertised service fee
is one possible contract. If a resource cap is merely an upper bound on its
actual cost, the row is an upper envelope: comparison with the *actual*
cheaper fixed-buy policy needs the corresponding envelope-gap correction.
The forecast does not conjure a resolving algorithm or its cost model.

A partially successful computation generally has another unresolved outcome,
such as whether it finishes and which error it repairs. Its decision value
need not be affine in the mathematical answer alone with coefficients known
at issuance. The principal paired-profile construction covers such complete
policies under its separate sampling assumptions. A single successful-answer
accuracy or completion frequency cannot replace the required joint evidence.

## 2. A continuous, implementable action mixture

For a proposed scalar forecast $`p`$, let $`c_t(p)=b_t+d_t p`$ and choose

```math
q_t(p)=\mathop{\mathrm{argmin}}_{q\in\Delta_A}
\left[q\mathbin{\cdot}c_t(p)+\frac{\eta_t}{2}\|q\|_2^2\right].
```

The positive quadratic term gives a unique minimizer. It is the Euclidean
projection of $`-c_t(p)/\eta_t`$ onto the probability simplex. Sorting that
finite vector, finding its active threshold, and subtracting the threshold
gives a finite rational implementation for rational inputs. For fixed cost
rows it is continuous and piecewise affine in $`p`$.

### Sharp predicted-loss allowance

For every comparator identity $`a`$, the first-order condition against the
simplex vertex $`e_a`$ gives

```math
q\mathbin{\cdot}c-c_a
\leq\eta(q_a-\|q\|_2^2)
\leq\eta\frac{A-1}{4A}.
```

To prove the second inequality, fix $`q_a=x`$ and minimize the sum of the
other squares at $`q_b=(1-x)/(A-1)`$. The resulting quadratic is maximized
at $`x=(A+1)/(2A)`$. Equality occurs when
$`q_a=(A+1)/(2A)`$, all other coordinates are $`1/(2A)`$, and their costs
exceed $`c_a`$ by $`\eta/2`$. Thus the two-action allowance is the inherited
$`\eta/8`$, while four actions require the sharp allowance $`3\eta/16`$
for this particular mixture. This is a regularized finite-decision
calculation, not a new general optimality principle.

### Bounds needed by the scalar root search

Put $`D_t=\max_a d_{t,a}-\min_a d_{t,a}`$ and
$`V_t=\sum_a(d_{t,a}-\bar d_t)^2`$, where
$`\bar d_t=A^{-1}\sum_a d_{t,a}`$ is the arithmetic mean slope.
Projection is nonexpansive in
Euclidean norm, and adding a common constant to every pre-projection
coordinate does not change the simplex projection. Consequently

```math
g_{t,a}(p)=\sum_b q_{t,b}(p)d_{t,b}-d_{t,a},\qquad
|g_{t,a}(p)|\leq D_t,\qquad
\mathrm{Lip}(g_{t,a})\leq V_t/\eta_t.
```

These are computable rational bounds. The looser inequality
$`V_t\leq A D_t^2/4`$ is also available. The ordinary forecaster gets the
same sorting, bound construction, and numerical allowance; none is free.

The action-feature block also has the useful sharp magnitude bound

```math
\sum_a\gamma_a^2w_t^2 g_{t,a}(p)^2
\le w_t^2D_t^2
\left(\sum_a\gamma_a^2-\min_a\gamma_a^2\right).
```

For fixed slopes, the left side is convex in the mixed slope, whose value
lies between the extreme slopes. At either extreme at least one difference
vanishes and every other difference has magnitude at most $`D_t`$. Equality
is feasible by concentrating the mixture on an extreme-slope action of
minimum scale and placing every other slope at the opposite extreme. With
a common scale this is $`(A-1)\gamma^2w_t^2D_t^2`$. Other feature blocks
and their numerical allowances still contribute to the complete potential.

## 3. The paid-action regret bridge

Append the $`A`$ continuous features

```math
\Phi_{t,a}(p)=\gamma_a w_t g_{t,a}(p)
```

to any other declared P3-06 feature blocks. Run the scalar potential method
on this **enlarged feature map**, with all coordinates present from the start
and their meanings and scales fixed. In the single-copy protocol, the previous
issued answer is admitted before another forecast is issued. Its residual and
bound on the scored chronological rounds are

```math
R_T=\sum_{t\leq T}(y_t-p_t)\Phi_t(p_t),\qquad
\|R_T\|_2^2\leq B_T
=\sum_{t\leq T}p_t(1-p_t)\|\Phi_t(p_t)\|_2^2
+\sum_{t\leq T}\mathcal A_t.
```

The actual nonnegative allowance $`\mathcal A_t`$ is the inherited
outcome-uniform allowance computed at the issued root approximation. A cap
exhaustion may enlarge it; it does not justify silently recording zero.
An old bound from the two-action run is not a certificate for this new run.

Concretely, for the complete feature map let

```math
S_t(p)=R_{t-1}\mathbin{\cdot}\Phi_t(p)
+\frac{1-2p}{2}\|\Phi_t(p)\|_2^2,\qquad
\mathcal A_t=2\max\{0,(1-p_t)S_t(p_t),-p_tS_t(p_t)\}.
```

At zero, a nonpositive score gives zero allowance; at one, a nonnegative
score does the same. If neither endpoint qualifies, continuity supplies a
root between opposite endpoint signs. The endpoint action mixture itself
need not be pure. Paid rational bisection may return an approximation with
the actual displayed allowance when its cap is reached. These are the
existing P3-06 endpoint and potential rules applied to new continuous features.
They hold for arbitrary deterministic binary-answer sequences once the correct
version-matched labels have been admitted; no IID truth law or accurate expert
is required.

For every fixed action identity,

```math
\sum_{t\leq T}w_t
\left[\sum_b q_{t,b}(p_t)c_{t,b}(y_t)-c_{t,a}(y_t)\right]
\leq
\sum_{t\leq T}w_t\eta_t\frac{A-1}{4A}
+\frac{\sqrt{B_T}}{\gamma_a}.
```

Indeed, each bracket equals its value at $`p_t`$ plus
$`(y_t-p_t)g_{t,a}(p_t)`$. The first sum is bounded by the preceding sharp
allowance and the second is one residual coordinate divided by its fixed
scale. This imports the existing potential identity and proves the new
multi-action readout; it adds no independent source of mathematical labels.

The comparator is the same role on every scored round, with that round's
announced costs. It is not the clairvoyant best role per round or an arbitrary
adaptive ordinary controller. A negative predicted gap can make a refined
retained-gap bound smaller, but the displayed generic envelope stays
nonnegative. In fact, with the retained predicted gap

```math
G_{T,a}=\sum_{t\le T}w_t
\left[\sum_bq_{t,b}(p_t)c_{t,b}(p_t)-c_{t,a}(p_t)\right],
```

the exact regret decomposition is $`G_{T,a}+R_{T,a}/\gamma_a`$, giving the
refined upper bound $`G_{T,a}+\sqrt{B_T}/\gamma_a`$. All fixed identities
are covered simultaneously, so their best one can be named after scoring.
If choosing a different role would alter later queries, caches or announced
tables, this comparison still uses the actual announced trajectory; a full
counterfactual policy comparison needs its own contract.

Forecasting, feature construction, selection and new feedback
acquisition costs add to the appropriate all-in comparison when they are not
common to the comparator. A sublinear displayed envelope does not imply a
sublinear total after those additions. For normalization by growing positive scored weight
$`W_T=\sum_tw_t`$, the displayed terms vanish only under the additional
conditions $`\sum_tw_t\eta_t=o(W_T)`$ and $`\sqrt{B_T}=o(W_T)`$.

## 4. A finite random-bit budget needs a correction

An exact rational mixture is not necessarily implementable using a fixed
finite number of fair bits. Three equal-cost actions produce probability
one-third each. Every event determined by at most $`b`$ fair bits has dyadic
probability with denominator dividing $`2^b`$, so exact thirds are impossible
under that primitive. An unbounded rejection sampler, a declared categorical
primitive, and a bounded approximation are different resource contracts.

One bounded choice is largest-remainder rounding. Let $`N=2^b`$, initially
assign each action $`\lfloor Nq_a\rfloor`$ slots, then give the remaining
$`r`$ slots to the largest fractional parts. If $`\nu`$ is the resulting
mixture, its total-variation distance satisfies

```math
\mathrm{TV}(\nu,q)
\leq
\max_{0\leq r\leq\min(A-1,N)}\frac{r(A-r)}{AN}.
```

Writing $`r_* = \min(N,\lfloor A/2\rfloor)`$, denote this exact worst-case
constant by $`\kappa(A,N)=r_*(A-r_*)/(AN)`$.

The bound equals $`\lfloor A^2/4\rfloor/(AN)`$ when
$`N\geq\lfloor A/2\rfloor`$, and equals $`1-N/A`$ when
$`N<\lfloor A/2\rfloor`$. To see this, the sum of the $`r`$ largest
fractional parts is at least $`r^2/A`$, whereas the positive rounding mass
is $`(r-\sum_{\mathrm{top}\ r}f_a)/N`$. Equality is feasible by taking
all fractional parts $`r/A`$ and nonnegative integer parts summing to
$`N-r`$. The maximum must respect $`r\leq N`$.

If the current outcome's action-cost range is at most $`C_t`$, rounding adds
at most $`w_t C_t\mathrm{TV}(\nu_t,q_t)`$ to its weighted mixed cost.
Keep the *continuous ideal mixture* in the defensive feature map, then add
this correction. Substituting the discontinuous rounded mixture into an
intermediate-value root proof is not justified by the same argument.

The rounded mixture can be sampled with exactly $`b`$ fair bits and a bounded
cumulative-table lookup, with the bit draw funded before its generation and
lookup work paid separately. For a fixed finite horizon $`T`$ and
$`\delta\in(0,1)`$, assume the draw is conditionally uniform given the
pre-draw history and conditionally independent of the current mathematical
answer. With deterministic bounds $`w_t C_t\leq M_t`$, the actual sampled-action cost
exceeds its conditional rounded-mixture cost by at most

```math
\sqrt{\frac12\left(\sum_{t\leq T}M_t^2\right)\log(1/\delta)}
```

with probability at least $`1-\delta`$ over the action draws. One centered
sampling process serves every fixed comparator, so an extra union over
action identities is unnecessary for this step. This statement needs the
full chronological horizon and the declared conditional independence;
inserting a random observed variance into a fixed deterministic bound is
another theorem.

Consequently the ideal-mixture bound extends to sampled execution by adding
$`\sum_tw_tC_t\kappa(A,2^{b_t})`$ and the displayed sampling term. Here
$`C_t`$ must bound the action-cost range for the actual outcome; taking the
maximum range over both announced binary endpoint rows is a predictable
choice. The fixed deterministic $`M_t`$ must dominate that choice along every
allowed history. This combines a pathwise rounding correction with a separate
probability statement over action draws, while retaining the ideal mixture
inside the continuous feature map.

## 5. Buying labels changes the guarantee and the bill

The potential inequality concerns labels actually settled under its protocol.
If only buying produces a label, the unbought rounds do not become scored
for free. An idle-copy delayed construction can retain unscored predictions,
but it does not give all-round regret without a valid eventual feedback
condition and the corresponding acquisition cost.

Moreover, filtering a random-action sequence to the rounds that bought a
label can destroy the centered sampling argument. In a two-action example,
fallback costs zero, buy costs one, and $`\eta=2`$. The ideal mixture buys
with probability one-quarter. If only buys settle, every settled action
costs one while its issued mixed cost was one-quarter: the settled sampling
difference is always three-quarters. That filtered process is not the
zero-mean martingale used above.

A revealing fully paid development protocol resolves every mathematical
query after its decision, reusing an already bought result when available.
If the same exact service costs $`f_t`$ whether bought before the decision
or for later feedback, the learner pays $`f_t`$ on every round either way.
It additionally suffers the task loss of any mistaken or fallback decision,
plus its forecasting and control overhead. With $`L_t^{\mathrm{nonBUY}}`$
equal to zero on BUY and to the chosen task loss otherwise, the identity is

```math
C_T^{\mathrm{learner}}
=\sum_tw_tf_t+\sum_tw_tL_t^{\mathrm{nonBUY}}
+\sum_tw_tO_t^{\mathrm{learner}},
```

before one-time setup is added. The explicit always-BUY service-fee comparator
used in the development evidence costs $`\sum_tw_tf_t`$: its fee covers the
same solve, check, acquisition and storage service before the decision.
It weakly dominates the displayed learner total, path by path, when the
additional task losses and controller charges are nonnegative. If a separately
implemented ordinary buyer is assigned additional controller or setup charges,
those must be included too: the difference contains
$`O_t^{\mathrm{learner}}-O_t^{\mathrm{BUY}}`$, and the setup difference,
with the common service fees cancelling. The recorded fee-comparator identity
does not estimate an unmeasured buyer implementation's overhead. Conditional
action regret remains valid under the same hypotheses and does not remove
this procurement obstruction.

Amortized information shared across future queries, cheaper external
feedback, or a different required output service can change that comparison.
Each needs its own acquisition and reuse contract. No such advantage is
assumed here.

## 6. Restricted numeric representation

The [independent bit-growth addendum](../work_logs/P3_07_2026-10-09_S1/reviews/proof_agent/multi_action_bit_extension.md)
extends P3-06's [restricted finite numeric-state result](06_cost_forecast_refinement.md#cf-11-restricted-finite-numeric-state)
to the simplex action features. The hypotheses are essential: fix the action
count, total feature dimension $`d`$, tent resolution, feature scales and a
positive rational $`\eta_0`$. All admitted action coefficients, weights and
supplied expert values have one fixed common denominator for the whole family,
and numerators bounded by fixed polynomials in $`t+1`$. Use

```math
\eta_t=\eta_0 2^{-h_t},\qquad h_t=\lceil\log_2(t+1)\rceil,
```

endpoint or dyadic-bisection reports, and a positive requested score tolerance
with $`O(\log(t+1))`$ encoding size and an inverse-polynomial lower bound.
Rationals are reduced or normalized to the stated common denominator; the
work required for normalization belongs in arithmetic cost.

### Root depth without circular state assumptions

The magnitude and Lipschitz bounds for each feature are polynomial under
these premises, since $`1/\eta_t=O(t+1)`$. If $`M_{t,j}`$ bounds feature
coordinate magnitude, the elementary estimate

```math
|R_{t-1,j}|\le\sum_{s<t}M_{s,j}
```

is already polynomial and does not assume earlier root searches met their
tolerances. Substitution in the inherited score Lipschitz bound

```math
L_{S,t}\le\sum_j
\left(|R_{t-1,j}|L_{t,j}+M_{t,j}^2+M_{t,j}L_{t,j}\right)
```

therefore yields a polynomial bound. When the endpoint rules do not apply,
a sufficiently short dyadic bracket attains the requested tolerance in
$`O(\log(t+1))`$ bisections. This is a sufficient arithmetic budget; an
actual hard cap can still terminate earlier and requires its recorded allowance.

### Fixed support divisors do not accumulate through time

For a dyadic candidate $`p=s/2^k`$ and active support $`S`$ of size
$`m\le A`$, projection gives

```math
q_i(p)=\frac1m+
\frac{\sum_{j\in S}c_j(p)-m c_i(p)}{m\eta_t}
\quad(i\in S),
```

and zero elsewhere. The denominator contribution from $`m`$ divides the
fixed integer $`\mathrm{lcm}(1,\ldots,A)`$. Division by
$`\eta_0 2^{-h_t}`$ adds only a fixed numerator factor from $`\eta_0`$
and multiplies by a power of two. Thus fixed integers $`C_q,C_\Phi`$
exist such that

```math
\mathrm{denom}(q_i(p))\mid C_q2^k,\qquad
\mathrm{denom}(\Phi_{t,j}(p))\mid C_\Phi2^k,\qquad
\mathrm{denom}((y-p)\Phi_{t,j}(p))\mid C_\Phi2^{2k}.
```

If $`K_T`$ is the largest candidate dyadic exponent through time $`T`$,
residual denominators divide $`C_\Phi2^{2K_T}`$. A fixed factor times
$`2^{4K_T+O(1)}`$ covers the variance and allowance statistics. Active
supports of size three introduce no repeated odd-denominator multiplication:
all increments already share the fixed support factor. The prior residual
affects the next feature coefficients only through the dyadic forecast; its
arbitrary rational ratios are not fed back as coefficients. The smoothing
sum has a fixed factor times the nested dyadic denominator $`2^{h_T}`$.

Together with polynomial magnitudes and $`K_T=O(\log(T+1))`$, these
facts give $`O(d\log(T+1))`$ bits for the current numeric statistics and
$`O(dT\log(T+1))`$ for one retained copy of each numeric issue/settlement
record. A sampler with $`b_t=O(\log(t+1))`$ has comparably sized numeric
counts; an arbitrarily larger chosen bit budget is a separate parameter.

This theorem concerns the specified numeric statistics. New odd denominators
in experts or coefficients, varying smoothing numerators, non-dyadic exact
roots, residual-dependent ratios, or unreduced fraction syntax can invalidate
its premises. An empirical frequency with a changing observation denominator
does not qualify automatically. Query identifiers, proofs, external expert
production, checked computation, copies of exports, storage accesses and a
delayed pool's multiple live states retain their own costs. Compact numeric
state alone establishes neither a physical CPU bound nor adequate feedback,
sublinear regret under increasing stakes, or positive all-in value.

## 7. Frozen implementation and finite development results

### Contract, source identities and chronology

The [v2 forecaster](../checks/07_multi_action_forecasting.py) is a bounded
single-pending-issue prototype. It admits 2 through 8 actions, at most 128
settlements, at most 64 requested root steps, 0 through 32 sampling bits,
and 8192-bit rational components, with a prepaid bounded-operation meter.
Its operation bundles are a declared rational-primitive resource model;
they are not measurements of Python CPU instructions. The
[development harness](../checks/07_multi_action_development.py) pays for
controller initialization, projection/features/root search, rounding,
random bits, selection and settlement under its stated tariff.

| Frozen source | SHA-256 |
|---|---|
| Forecaster v2 | `9605a0fa3483358bd6f0f98770b154888cbc37a37c4a746bfbf3e9f3f62453a7` |
| Development harness v2 | `cb5e191150905d9c1615277ab7b5dac0811e8646d2a76924499226dfa0fd7291` |
| Checked computation adapter | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |

The [saved run manifest and source copies](../work_logs/P3_07_2026-10-09_S1/development/multi_action_run_v2/manifest.json)
identify these exact versions. The v2 plan's inherited v1 source/date fields
are explicitly described in a
[non-overwriting disposition](../work_logs/P3_07_2026-10-09_S1/development/multi_action_plan_v2_disposition.json).
The appended v2 revision and new seeds precede the run; the actual run manifest
freezes the v2 sources before its rows are produced. The clarification preserves
the original plan bytes rather than silently changing them after the results.

The queries come from the declared 248-element population
$`a^{(p-1)/2}\bmod p=1`$, with $`p\in\{17,31,47,61,97\}`$ and
$`1\le a<p`$. Query seed 307113 and action seed 307127 define the new
development streams. Each of the three settings has 32 queries, expert
one-half, a tent grid of resolution four with five coordinates, common action
scale $`1/100`$, smoothing
$`8/2^{\lceil\log_2(t+1)\rceil}`$, the fixed four-round weight cycle
$`(1,4,1,2)`$, and the prospectively specified six-round price cycle.
These supplied interfaces and prices are available to ordinary comparators.

Every action record is written and flushed before the harness executes the
real bounded modular solver and checker. All 32 labels are then admitted in
each setting, with an early BUY result reused and the same known flat service
fee charged for later feedback on non-BUY rounds. That tariff covers the
provider's solve, check, acquisition and storage work. Raw adapter operations
are also retained for scope; they are not charged a second time. Controller
work is separately priced at $`1/100000`$ loss units per declared primitive,
then multiplied by the round's weight. Private frequency diagnostics and audit
serialization are explicitly harness work outside the policy account.

### Three settings on the new 32-query stream

The [saved aggregate result](../work_logs/P3_07_2026-10-09_S1/development/multi_action_run_v2/result.json)
and [focused v2 review](../work_logs/P3_07_2026-10-09_S1/reviews/proof_agent/multi_action_code_v2_review.md)
give these exact totals. All-in values exclude the separately recorded one-time
setup fee $`2/3125`$; the always-BUY service-fee comparator is 368 in every case.

| Setting | Root-tolerance misses | Ideal mixed action cost | Sampled action cost | All-in learner cost |
|---|---:|---:|---:|---:|
| Full root, eight bits | 0 | `7096737/25600` | `1367/5` | `32020931/50000` |
| Root cap zero, eight bits | 26 | `55239/200` | `1369/5` | `15969017/25000` |
| Full root, one bit | 0 | `7096737/25600` | `277` | `32100707/50000` |

The ideal mixed costs are approximately 277.216, 276.195 and 277.216.
The all-in costs are approximately 640.419, 638.761 and 642.014. Thus the
favorable mixed action totals coexist with a substantially larger total
than the 368 fee comparator once every feedback label and controller operation
is paid. These finite cases directly exhibit the full-feedback procurement
limitation in Section 5.

Full-root settings allow 32 further bisection steps. Root cap zero still
evaluates the endpoints and, where needed, the initial midpoint; it permits
no further bisections. Its 26 tolerance misses retain their actual nonzero
allowances. All three cases satisfy every stored potential and regret check.
The final generic action bound is `431014299797/536870912` in the full-root
cases, about 802.827, and `2160809239919/1073741824` in the capped case,
about 2012.410. These valid bounds are loose in this run; all four final
ideal mixed regrets are negative. No claim of predictive or computational
superiority follows from passing the inequalities.

The eight-bit certified rounding correction is `2029/128` in either
root setting. The one-bit correction is 2029; its actual signed correction
is only `22623/25600`. Recording both prevents the small realized effect
from being substituted for the worst-case finite-bit guarantee. The observed
controller totals are 140290, 46788 and 140066 primitive units respectively,
with peak retained component sizes 84, 46 and 84 bits. They are finite run
measurements under the declared meter, separate from Section 6's conditional
asymptotic representation theorem.

### Preserved failures and checked repairs

The [frozen v1 review](../work_logs/P3_07_2026-10-09_S1/reviews/proof_agent/multi_action_code_v1_review.md)
found three concrete boundary issues: a derived numeric-cap error after
settlement had committed, direct categorical lookup accepting a 33-bit
request despite the 32-bit contract, and random bits generated before their
charge could fail. The v1 sources and ordinary-size evidence remain preserved
under their original hashes.

The v2 review verified the repairs against the original witnesses. With two
zero-cost actions and weight $`2^{4093}`$, the sixteenth proposed settlement
would make a combined potential bound exceed 8192 bits. V2 validates its full
report before committing: it rejects with 15 settlements and the same pending
issue retained, while keeping the 312 paid failed-settlement units. The
retained state remains exportable. Direct lookup now validates both bit and
action counts before traversal, then prepays bounded slot inspection. Denying
funds at the actual harness's fair-bit charge produces zero action draws and
an unchanged RNG state. Denying the later lookup retains an already-paid
eight-bit draw. Neither focused denial probe calls the truth service.

All 96 saved v2 rows were independently recomputed without rerunning the
solver experiment: issuance fields, exact projection conditions, enlarged
potential and gap identities, dyadic transport, categorical choice, service
resources and weighted all-in cost sums agree. Both declared seed streams
also reconstruct the saved records. This is focused evidence about the
implemented scope, not a proof for all malformed inputs or all possible
program failures. A rejected settlement keeps its pending issue; the component
does not supply a cancellation/fallback wrapper for permanently unfunded or
over-cap feedback.

## 8. Attribution and verified scope

The [independent algebra and boundary reconstruction](../work_logs/P3_07_2026-10-09_S1/reviews/multi_action_reconstruction.md)
was written before inspecting the root's multi-action manuscript or code,
after the root supplied candidate regularization and rounding formulas.
It is same-model, nonblind internal reconstruction. The bit-growth addendum
and v2 code review are targeted same-model reviews; no external independence,
priority or exclusive advantage is claimed. Their agent time is unmeasured
and earns zero principal-clock credit.

The verified contribution is a sharp finite-action regularization allowance,
the enlarged-feature fixed-comparator readout inherited from P3-06, an exact
bounded-bit rounding correction with the stated sampled-execution extension,
and a restricted numeric-state theorem. The preserved negative evidence
establishes concrete limits: unknown partial-success work needs a separate
joint performance model, missing labels restrict the scored population,
action-selected feedback invalidates the stated sampling argument, and the
fully paid feedback protocol can make an always-BUY fee comparator cheaper
despite favorable conditional action regret.

P3-06 source and evidence are unchanged. The principal P3-07 artifact and its
clock/readiness records determine task completion and Research90 status
separately; this companion does not advance them or authorize a later phase.
