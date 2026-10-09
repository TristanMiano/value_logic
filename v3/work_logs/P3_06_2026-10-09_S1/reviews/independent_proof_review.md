# P3-06 independent reconstruction and decision extension

Contributor: **ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer**.
Date: October 9, 2026 UTC. This is a distinct reconstruction from the principal's
derivation. Subagent research effort is **unmeasured** and contributes **zero**
to the principal's Research90 clock.

## 1. Scope and disposition

I read the phase-three protocol, mathematical style contract, this session's
prospective forecast, the desiderata matrix, and the preserved defensive
forecasting addendum and implementation. I reconstructed the potential and
consequences from the algebra before using executable evidence.

**Disposition:** the preserved scalar-forecast potential, expert-loss identity,
finite continuous-bin calibration statement, endpoint/root allowance, and
per-copy delayed reduction are mathematically sound under their written input
contracts. I found no load-bearing defect in those results. Their limitations
are material: continuous calibration does not justify hard threshold decisions;
fixed-expert predictive regret does not justify outcome-oracle action regret;
and delayed or concentrated stakes can prevent normalized refinement.

This review gives an exact obstruction to the first two careless implications,
and develops a useful additional theorem: two rational continuous action
features give a common scalar report with approximate fixed-action regret for
announced, changing binary affine loss tables. That extension is a new reviewed
derivation here; it is not attributed retroactively to the preserved code.

The inspected immutable source hashes were:

| Preserved file | SHA-256 |
|---|---|
| `06_defensive_forecasting_addendum.md` | `87662fd234e2401da060f00027489ce42bf19be54c28b4595675287c919fa02e` |
| `defensive_forecasting.py` | `cbe6565492f3083c55bc966e1b31ae55f95aa026d87af378b1e2673f7e944be2` |
| `check_defensive_forecasting.py` | `5299bd921e452403df13e95447cbeb9f5c8144146ccbf5c33f4a324df20fc9e5` |
| `development_result.json` | `dead832e91d7327fd826fc9f8b1c11f4cd6a1ae52ae01aefaa1162919f4a9db3` |

The preserved result reports PASS, 1,510 assertions and 32 binary-sequence cases;
its two recorded Python hashes match the inspected files. I did not rerun that
checker or overwrite its output. This review's additional evidence is separate.

## 2. The scalar potential reconstructed

Let the complete predictable continuous feature vector be $`\Phi_t(p)`$, and
let $`R`$ be the sum of earlier settled residuals in the same copy. Define

```math
S_t(p)=\langle R,\Phi_t(p)\rangle+
\frac{1-2p}{2}\|\Phi_t(p)\|^2.
```

For either binary outcome, put $`e=y-p`$. Direct expansion gives

```math
(y-p)^2-p(1-p)=(1-2p)(y-p),
```

and consequently

```math
\|R+e\Phi\|^2-\|R\|^2-p(1-p)\|\Phi\|^2=2eS_t(p).
```

At issue time the two possible corrected-potential increments are exactly
$`2(1-p)S_t(p)`$ and $`-2pS_t(p)`$. Thus

```math
A_t=2\max\{0,(1-p_t)S_t(p_t),-p_tS_t(p_t)\}
```

is a valid predictable allowance. In fact the zero in this maximum is redundant
for $`p\in[0,1]`$, because the other two expressions cannot both be negative.
Keeping it makes nonnegativity explicit. Summing from zero gives

```math
\|R_T\|^2\le B_T,
\qquad
B_T=\sum_{t\le T}p_t(1-p_t)\|\Phi_t(p_t)\|^2+\sum_{t\le T}A_t.
```

No probabilistic outcome assumption appears in this proof. It holds for every
binary path, including one selected adaptively after seeing the report.
Whether an admitted label is the correct interpreted answer is a separate
soundness/execution bridge; the identity cannot establish that bridge.

If $`S(0)\le0`$, the choice $`p=0`$ has nonpositive increments for both
outcomes; if $`S(1)\ge0`$, $`p=1`$ does also. Otherwise continuity supplies a
root between the endpoints. The preserved code's endpoint signs, midpoint
updates and stored allowance agree with this proof.

## 3. The expert and calibration consequences

For the preserved expert coordinate,
$`R_{T,i}=\alpha\sum_t w_t(y_t-p_t)(q_{t,i}-p_t)`$. The square expansion is

```math
\sum_t w_t\bigl((p_t-y_t)^2-(q_{t,i}-y_t)^2\bigr)
=\frac{2R_{T,i}}{\alpha}-\sum_t w_t(q_{t,i}-p_t)^2
\le\frac{2\sqrt{B_T}}{\alpha}.
```

The single power of $`w_t`$ in this identity is correct even though the
potential norm bound contains $`w_t^2`$. Dropping the negative distance term
weakens the bound but does not invalidate it. The comparator is each fixed
supplied expert index; the supplied expert's forecasts may change predictably
over rounds. It is not a per-round hindsight oracle or a universal reasoner.

For $`E_{T,j}=\sum_t w_tb_j(p_t)(y_t-p_t)`$, the calibration block yields

```math
\sum_{j=0}^{m}E_{T,j}^2\le\frac{B_T}{\beta^2}.
```

This slightly stronger joint statement implies each displayed bin bound in
the addendum and, for any fixed coefficient vector $`a`$,

```math
\left|\sum_t w_t\left(\sum_j a_jb_j(p_t)\right)(y_t-p_t)\right|
\le\frac{\|a\|_2\sqrt{B_T}}{\beta}.
```

These are tests of the issued scalar itself. The construction never substitutes
the mean of a randomized forecasting distribution for that distribution's
calibration guarantee. A conditional bin statistic divides by that bin's
actual weighted occupancy. A bound normalized by total stake does not make
a rarely occupied bin conditionally accurate.

The fixed finite tent span is not every continuous test, every context, or a
discontinuous decision-selection family. More features require another declared
feature block, its norm and computation costs, and the same proof conditions.

## 4. Normalization, concentration and delayed feedback

For the preserved feature vector,

```math
B_T\le\frac{N\alpha^2+\beta^2}{4}\sum_t w_t^2+\sum_t A_t.
```

With $`W_T=\sum_t w_t>0`$, the sufficient hypotheses
$`\sum_t w_t^2=o(W_T^2)`$ and $`\sum_t A_t=o(W_T^2)`$ establish normalized
expert regret and finite-test signed-error refinement. Fixed bounded absolute
root residual is compatible with this result for bounded, sufficiently
nonvanishing total weights. A fixed number of bisections alone does not imply
that absolute residual bound as the state grows.

The scale of the allowance is important: it bounds an increment of a squared
vector potential, not an additive loss. Requiring only sublinear cumulative
loss allowance belongs to a different proof. Conversely, an allowance that
grows quadratically in total weight can leave the present certificate vacuous.

A single dominating stake explains why the weight hypothesis matters. In an
abstract binary protocol, after any report $`p`$ an outcome can be chosen with
$`|y-p|\ge1/2`$. Against the two constant experts, the best expert has zero
loss on that one round, and the learner has weighted loss at least $`w/4`$.
Earlier weights cannot rescue a uniform normalized conclusion if the new
stake dominates their total. This is an obstruction under the abstract input
contract, not a claimed arithmetic experimental population.

Each delayed copy has its own settled prefix, so the same proof applies to
each without guessing a missing label. A somewhat sharper aggregation than
the preserved common-$`K`$ bound is

```math
\left\|\sum_kR^{(k)}\right\|\le\sum_k\sqrt{B^{(k)}}=:H,
\qquad
H^2\le K\sum_k B^{(k)}.
```

The parent owns integration and the complete cutoff/pending formulation of
this strengthening. One must use the actually relevant copy-local prefixes;
a settled-subset guarantee does not become a claim about the unresolved
population. A missing-label policy does not acquire a paid-discovery guarantee
merely because its settled algebra remains valid.

The slowdown can be real. If every query is assigned a fresh copy, the
constant experts are zero and one, all unit-weight labels are withheld until
all forecasts are issued, and all eventual outcomes are zero, the preserved
symmetric new-copy calculation issues $`p=1/2`$ on every round. Its expert
regret is $`T/4`$. This is consistent with $`K=T`$ and shows why a useful
copy-growth or eventual-prefix condition is indispensable.

## 5. What the existing terminal decision bridge proves

For binary affine costs $`c(a,y)=b_a+d_ay`$, let $`\widehat a`$ minimize the
announced forecast cost at $`p`$ and let $`a^*`$ minimize realized cost at
$`y`$. Their forecast-cost difference is nonpositive, so

```math
0\le c(\widehat a,y)-c(a^*,y)
\le(d_{\widehat a}-d_{a^*})(y-p)
\le D|y-p|,
\qquad D=\max_a d_a-\min_a d_a.
```

The slope diameter is a useful sharper coefficient than separately bounding
each action error. The subsequent weighted Cauchy--Schwarz bound in the
addendum follows. However, vanishing regret to a good *fixed predictor* does
not imply the squared loss itself vanishes. The outcome-oracle decision
conclusion needs a supplied expert with the required vanishing predictive
loss and an applicable normalized learner regret bound. Common action costs
cancel in the terminal comparison; their computation and acquisition costs
do not vanish from a complete policy budget.

## 6. Exact obstruction: continuous calibration and good squared loss do not justify hard decisions

For $`n=1,2,\ldots`$, let $`\varepsilon_n=1/(8n)`$ and issue the pairs

```math
(p_{2n-1},y_{2n-1})=(1/2-\varepsilon_n,1),
\qquad
(p_{2n},y_{2n})=(1/2+\varepsilon_n,0).
```

Use unit weights and the three tents with $`m=2`$. After $`M`$ pairs, their
exact residual vector is

```math
(E_0,E_1,E_2)=
\left(\sum_{n\le M}(\varepsilon_n+2\varepsilon_n^2),\;0,\;
       -\sum_{n\le M}(\varepsilon_n+2\varepsilon_n^2)\right).
```

It is $`O(\log M)`$. The learner's squared-loss regret to the half predictor is

```math
\sum_{n\le M}(2\varepsilon_n+2\varepsilon_n^2)=O(\log M).
```

The constant zero and one experts are worse than the half expert by a linear
amount. Thus the example has normalized vanishing finite-tent errors and
normalized vanishing regret to the best of the three constant experts.

Under zero-one action loss, the hard rule $`a=1[p>1/2]`$ is nevertheless wrong
on every round. Its loss is $`2M`$, while either fixed action loses $`M`$.
Its external action regret is exactly $`M`$.

The obstruction is not restricted to three tents. For any fixed continuous
function $`f`$, the residual of one pair equals

```math
(1/2+\varepsilon_n)
\bigl(f(1/2-\varepsilon_n)-f(1/2+\varepsilon_n)\bigr),
```

which tends to zero. Its normalized cumulative sum tends to zero by averaging.
Hence even calibration against every fixed continuous test does not rule out
this hard-decision failure. The hard selection switches discontinuously while
the forecast mass accumulates at its threshold.

This is an implication counterexample. It is not asserted to be a trajectory
generated by the preserved algorithm. A theorem for the algorithm's hard
decisions would need additional argument, such as a justified margin condition
or an applicable selection-specific feature construction. One cannot simply
insert a discontinuous indicator into the continuous-root proof.

## 7. A decision consequence available from the existing tents

For one fixed finite affine action table, select an optimal action $`a_j`$ at
each tent center $`c_j=j/m`$. At a forecast $`p`$, score the mixed action that
uses $`a_j`$ with probability $`b_j(p)`$. These are action probabilities; the
forecast remains the one scalar $`p`$.

For any fixed action $`a`$, center optimality gives

```math
c(a_j,p)-c(a,p)\le(d_{a_j}-d_a)(p-c_j)\le D|p-c_j|.
```

On each grid interval, writing its fractional position as $`r\in[0,1]`$,

```math
\sum_j b_j(p)|p-c_j|=\frac{2r(1-r)}{m}\le\frac1{2m}.
```

Adding the exact realized-minus-forecast cost differences and using the joint
calibration bound proves

```math
\sum_t w_t\left(\sum_j b_j(p_t)c(a_j,y_t)-c(a,y_t)\right)
\le\frac{DW_T}{2m}
 +\frac{\|(d_{a_j}-d_a)_{j=0}^{m}\|_2\sqrt{B_T}}{\beta}
\le\frac{DW_T}{2m}+\frac{D\sqrt{(m+1)B_T}}{\beta}.
```

This gives an approximate fixed-action comparator service from the existing
features. It has a fixed discretization term and requires the same table and
center actions over the scored rounds. Changing tables do not preserve the
constant coefficients multiplying the existing residuals. The next extension
handles announced changing tables directly.

## 8. Rational smooth-action extension with changing tables

### 8.1 Contract

On every round, before $`y_t`$, receive two action losses

```math
c_{t,i}(y)=b_{t,i}+d_{t,i}y,\qquad i\in\{0,1\},
```

known rational coefficients, a nonnegative rational weight $`w_t`$, and a
positive rational smoothing width $`\eta_t`$. The action labels are stable
across rounds. A comparison to a fixed action means choosing that same index
on every round, while its announced loss table is allowed to change.

The losses refer to the same binary mathematical outcome. A terminal action
does not change that interpreted outcome. Expert and loss-table computation,
root search, exact arithmetic, storage and feedback acquisition retain their
ordinary costs. Fix a positive scale $`\gamma`$ across the state and copies.

### 8.2 Local rule and sharp approximation constant

For candidate $`p`$, define

```math
\Delta_t(p)=c_{t,1}(p)-c_{t,0}(p),
\qquad
s_t(p)=\min\left(1,\max\left(0,\frac12-\frac{\Delta_t(p)}{2\eta_t}\right)\right).
```

Score the action mixture with action-one probability $`s_t(p)`$. Its slope is

```math
\bar d_t(p)=d_{t,0}+s_t(p)(d_{t,1}-d_{t,0}).
```

The mixture's forecast cost is
$`\bar c_t(p,p)=(1-s_t(p))c_{t,0}(p)+s_t(p)c_{t,1}(p)`$.
Outside $`|\Delta_t(p)|<\eta_t`$, this mixture selects a minimizer exactly.
Inside, with $`u=|\Delta_t(p)|`$, its excess over the minimum equals

```math
\frac u2-\frac{u^2}{2\eta_t}
=\frac{\eta_t}{8}-\frac{(u-\eta_t/2)^2}{2\eta_t}
\le\frac{\eta_t}{8}.
```

The constant is attained at $`u=\eta_t/2`$. Therefore, for both action indices,

```math
\bar c_t(p,p)-c_{t,i}(p)\le\eta_t/8.
```

### 8.3 Add two continuous features

Append to the existing vector the two coordinates

```math
\Phi^{\mathrm{act},i}_t(p)
=w_t\gamma\bigl(\bar d_t(p)-d_{t,i}\bigr),\qquad i=0,1.
```

Every feature is continuous and piecewise linear in candidate $`p`$. The same
score is continuous and piecewise cubic; rational evaluation remains exact.
Use the same endpoint/root rule and actual allowance for this **extended**
vector. Let $`B_T^{\mathrm{ext}}`$ be its resulting potential certificate.

For the scored mixed-action loss
$`\bar c_t(p,y)=(1-s_t(p))c_{t,0}(y)+s_t(p)c_{t,1}(y)`$, define
$`G_{T,i}=\sum_t w_t(\bar c_t(p_t,y_t)-c_{t,i}(y_t))`$. The exact identity is

```math
G_{T,i}
=\sum_t w_t\bigl(\bar c_t(p_t,p_t)-c_{t,i}(p_t)\bigr)
 +\frac{R^{\mathrm{act},i}_T}{\gamma}.
```

Combining local slack with the same vector potential proves, simultaneously
for both fixed action indices,

```math
G_{T,i}\le\frac18\sum_t w_t\eta_t+
\frac{\sqrt{B_T^{\mathrm{ext}}}}{\gamma}.
```

The old expert and continuous-bin statements hold simultaneously with
$`B_T^{\mathrm{ext}}`$. This is a guarantee for the same issued scalar forecast
and its announced smooth decision rule, not for the old code's unextended
forecasts or an unanalysed hard action rule. It compares with the best fixed
action index, not the changing outcome-optimal action on each round.

### 8.4 Norm, rate and computational cost

Put $`D_t=|d_{t,1}-d_{t,0}|`$. The two added coordinates have joint squared norm

```math
w_t^2\gamma^2D_t^2\bigl(s_t(p)^2+(1-s_t(p))^2\bigr)
\le w_t^2\gamma^2D_t^2.
```

Thus the sharper useful total bound is

```math
B_T^{\mathrm{ext}}\le
\frac14\sum_t w_t^2\bigl(N\alpha^2+\beta^2+\gamma^2D_t^2\bigr)
+\sum_t A_t.
```

For example, bounded $`D_t`$, dispersed weights, controlled potential allowance,
and $`\sum_t w_t\eta_t=o(W_T)`$ give normalized vanishing fixed-action mixed
regret. This needs neither a perfect predictor nor vanishing outcome-oracle
loss. If $`W_T\to\infty`$ and $`\eta_t\to0`$ with finite early terms, the
weighted slack condition follows by splitting the sum into a finite prefix
and a tail bounded by an arbitrarily small width.

There is no free precision gain. The slope of $`s_t`$ is bounded in magnitude by
$`D_t/(2\eta_t)`$, so an action feature is bounded by
$`M_t=w_t\gamma D_t`$ and has Lipschitz constant
$`L_t=w_t\gamma D_t^2/(2\eta_t)`$. Small smoothing widths increase the score's
Lipschitz bound and therefore the certified root effort. Unknown or uncontrolled
stakes/slopes require the displayed weighted sums, not an automatic rate.

### 8.5 Sampling and delayed scope

The theorem scores the mixture cost exactly. If an actual action is sampled,
its realized loss additionally contains sampling fluctuation. Equality to the
mixture's expected loss requires that, conditional on pre-action information,
the outcome and scored inclusion rule not be changed in response to that
sample. Fixed mathematical truth satisfies the outcome part; action-dependent
feedback selection can still require care. No pathwise bound for every sampled
action sequence is claimed here.

For a delayed pool, add the same action-feature indices and scales to each
copy. On its admitted settled prefixes, the aggregate action bound replaces
$`\sqrt{B_T^{\mathrm{ext}}}`$ by $`\sum_k\sqrt{B_k^{\mathrm{ext}}}`$. Store the
original $`p_t`$, loss table, smoothing width and mixture weight. Retrospectively
changing the table does not preserve the online feature state or guarantee.

## 9. Root termination and bit complexity

For feature-wise bounds $`|\Phi_k(p)|\le M_k`$ and Lipschitz constants $`L_k`$,
directly subtracting the two scores gives the global bound

```math
|S(p)-S(q)|\le
\sum_k\bigl(|R_k|L_k+M_k^2+M_kL_k\bigr)|p-q|.
```

This argument works across every piece boundary and does not assume a
monotone score. A sign-preserving bisection bracket after $`k`$ halvings has
width $`2^{-k}`$; its midpoint lies within $`2^{-k-1}`$ of some root. A chosen
$`k`$ with $`L_S2^{-k-1}\le\delta`$ therefore certifies the requested absolute
residual. Endpoint success is a different condition and can have a large
absolute score while still having zero allowance.

The preserved implementation's `max_bisections` counts midpoint refinements;
it may additionally evaluate both endpoints and the initial midpoint. Its
recorded score evaluation count reflects that distinction. Budget exhaustion
does not create a false root: the actual allowance is returned.

These are rational-operation statements. Even numbers in the bounded interval
$`[0,1]`$ can be supplied with arbitrarily large denominators. A finite root-step
budget alone does not bound input parsing, integer arithmetic, retained-history
memory or elapsed CPU time. Exact rational arithmetic is a valid executable
finite-prefix model, but a stronger resource claim must include input bit
lengths, numerator/denominator growth and storage. The smoothing extension is
piecewise rational, so it avoids introducing a transcendental evaluation oracle;
it does not eliminate those bit costs.

## 10. Repricing and retention

The preserved issue-time weighted theorem does not imply a new theorem for
arbitrary later weights. The addendum's two-round loss-error contrast is a
valid separating witness for that implication. Retaining only accumulated
regret loses information needed for general rescoring. Retaining the immutable
forecasts, expert values, labels and scoped per-round costs permits rescoring
and counterfactual analysis of the recorded decisions.

Such rescoring is not a replay of the online learner under the new prices:
different earlier weights would change its state and future reports. Changed
loss tables also change the new action features. Recomputed policy trajectories
need an explicitly separate replay and matching available-information contract.

## 11. Independent executable evidence

The review-specific [probe](decision_extension_probe.py) imports no project
forecaster. Its [saved result](decision_extension_probe_result.json) reports
PASS with 2,962 exact assertions, 195 local slack grid cases, and all 32 binary
paths of five rounds. The varying loss tables include negative coefficients,
parallel action slopes, nonunit feature scales and a zero-weight round.

The checks independently cover both-outcome potential increments before label
admission; endpoint and successful-root allowances; the Lipschitz-derived
termination budget; the sharper joint action norm; the existing expert identity;
the changing-table action identity and finite regret bound; the sharp local
$`\eta/8`$ constant; and exact hard-threshold counterexample statistics at 32,
128 and 512 rounds. The maximum rational component observed in these small
cases had 83 bits. This is a finite observation, not a worst-case bound.

Probe SHA-256:
`60fc425554094ed5a2b021fc67b3fcaa510a8a43a9f6a4d2a07fd9a0ef7ad8d9`.
The result records an observed script execution duration of 135,705,034 ns;
this is neither the subagent's total effort nor principal research credit.
All general mathematical conclusions above rest on their written proofs, not
the number of assertions.

## 12. Desiderata and source comparison boundary

| Duty | Reviewed scope |
|---|---|
| U01 | Predictable finite scalar computation, with actual approximation allowance; semantic admission and complete resource accounting remain external interfaces. |
| U06 | Learning relative to supplied predictive structure before each admitted label; supplied identities are not discoveries by the update. |
| U07 | Weighted finite continuous-bin residuals of the scalar report; hard selection and unresolved-population calibration do not follow. |
| U08 | Pathwise weighted squared-loss regret to a fixed finite expert library. |
| U09 | Copy-local settled prefixes and charged copy aggregation; no paid proof-discovery optimality. |
| V03 | Existing conditional outcome-oracle bridge; additionally a proved rational smooth mixed-action bound to either fixed action index under the extended features. |
| V04 | Root arithmetic and bit/memory obligations explicit; no complete value-of-computation policy is established. |
| R01 | Original issue records preserved; repricing or semantic changes require explicitly scoped rescoring or replay. |

No joint logical coherence, general self-trust, universal inexploitability,
arbitrary-language logical induction, or optimal paid reasoning theorem is
obtained here. The action extension fits the same continuous-feature potential
mechanism; it is an adaptation within that framework. It should be compared
with ordinary generalized defensive forecasting and ordinary calibrated
decision methods on identical inputs and resources. This review makes no
priority claim and does not independently award P3-N01 contribution support.
Primary-source attribution and source-specific hypothesis reconciliation belong
in the principal's literature integration.

## 13. Rejected precision claim and repaired finite-bit proposition

### 13.1 Research failure retained: harmonic smoothing slack

The principal proposed a draft refinement with uniformly bounded inputs and a
fixed common input denominator: use $`\eta_t=c/(t+1)`$, a fixed positive root
tolerance, and claim that **all** exact numeric state has $`O(\log t)`$ bits.
The core feature calculation contains $`1/\eta_t=(t+1)/c`$, so its denominators
really do remain a fixed factor times powers of two. But the full state also
stores the exact cumulative smoothing allowance

```math
Q_T=\frac18\sum_{t=1}^{T}w_t\eta_t.
```

For unit weights and $`c=1`$, this is $`(H_{T+1}-1)/8`$. Its denominator is
not controlled by the proposed fixed-factor/dyadic induction. The original
full-state claim was therefore rejected before integration; the narrower
core-state observation was not itself refuted.

There is an elementary asymptotic obstruction as well as finite evidence.
Write $`H_n=a_n/d_n`$ in lowest terms and
$`D_n=\mathrm{lcm}(1,\ldots,n)`$. Every prime $`n/2<p\le n`$ occurs in the
denominator of exactly one summand, so it cannot cancel from $`d_n`$. Hence

```math
\prod_{n/2<p\le n}p\ \mid\ d_n,
\qquad d_n\mid D_n.
```

Applying the prime number theorem to the prime product gives
$`\log d_n\ge(1/2+o(1))n`$, while
$`\log D_n=(1+o(1))n`$. Thus the harmonic denominator has $`\Theta(n)`$
bits. Subtracting one leaves its reduced denominator unchanged, and multiplying
by a fixed rational can remove only a fixed number of those bits. The standard
denominator notation and lcm estimate are recorded in
[P. Shiu, *The denominators of harmonic numbers*, arXiv:1607.02863v2 (2024),
§§1 and 7](https://arxiv.org/pdf/1607.02863); the uncancelled upper-half-prime
argument above is the reconstruction used here. No conjecture concerning exact
equality between $`d_n`$ and $`D_n`$ is needed.

The independent [precision probe](precision_schedule_probe.py) and its
[immutable result](precision_schedule_probe_result.json) retain the concrete
failure. At 256 rounds, the harmonic-schedule core used at most 83-bit rational
components in that trace, while the cumulative smoothing allowance had a
374-bit denominator. Under the dyadic replacement below, the corresponding
core maximum was 82 bits and the slack denominator used 13 bits. These are
finite observations; the preceding proof explains the asymptotic distinction.

### 13.2 Restricted positive theorem

Fix the dimension, expert names, tent count, and positive rational scales
$`\alpha,\beta,\gamma,c,\delta`$. Assume every supplied expert value, weight
and action-table entry has uniformly bounded magnitude and a denominator
dividing one fixed integer $`L`$. Use the certified root mode with absolute
tolerance $`\delta`$, and set

```math
h_t=\lceil\log_2(t+1)\rceil,
\qquad \eta_t=c\,2^{-h_t},\qquad t\ge1.
```

Then the numeric forecasting kernel requires $`O(\log(t+1))`$ bisections per
round; every exact numerator and denominator in its current numeric state,
including cumulative smoothing slack, has $`O(\log(t+1))`$ bits. With dimension
displayed as $`d`$, current numeric accumulators and one current report use
$`O(d\log(t+1))`$ bits, and retaining each numeric issue/settlement record once
through round $`T`$ uses $`O(dT\log(T+1))`$ bits. Constants depend on the fixed
parameters, common denominator and magnitude bounds.

This is a restricted numeric-kernel statement. Query identifiers, proof bodies,
semantic certificates, arbitrary metadata, repeated exported snapshots and
external expert/acquisition computation are outside it. A delayed pool needs
its actual copy and history costs separately. General rational inputs or an
arbitrary fixed root cap do not instantiate this proposition.

### 13.3 Noncircular root-effort argument

The order of the induction matters. Suppose previous rounds used valid
endpoints or met the requested residual. Uniform input bounds imply a uniform
feature norm bound, including both action coordinates, regardless of the
small smoothing width. Their allowances satisfy $`A_s\le2\delta`$. Therefore

```math
B_{t-1}=O(t),\qquad \|R_{t-1}\|=O(\sqrt t).
```

This conclusion uses earlier root success, not an assumed bound on future
bit lengths. Since

```math
\frac{c}{2(t+1)}\le\eta_t\le\frac{c}{t+1},
```

the action-feature Lipschitz constants are $`O(t+1)`$, while other feature
constants remain bounded. The score bound from §9 is consequently
$`L_{S,t}=O((t+1)^{3/2})`$. Its certified root budget is
$`O(\log(t+1))`$. Continuity and bisection prove that the next root succeeds,
closing the induction. The kernel computes the adequate budget from its actual
state; no unknown asymptotic constant must be guessed in advance.

### 13.4 Fixed denominators and bounded numerator sizes

Enlarge the fixed integer $`L`$ to a fixed integer $`H`$ that also includes all
fixed scale denominators, the numerator of $`c`$, and fixed factors such as two.
Use $`K_t`$ for the largest dyadic denominator exponent of a trial/report through
round $`t`$. This exponent is one more than the number of midpoint refinements
for a nonboundary issued report; it is not the raw refinement count.

For a dyadic candidate with denominator dividing $`2^k`$, the rational clipping
formula uses $`1/\eta_t=2^{h_t}/c`$. Therefore every feature denominator divides
$`H^C2^k`$ for one fixed exponent $`C`$ determined by the algebraic template.
Multiplication by $`y-p`$ gives residual-update denominators dividing
$`H^C2^{2k}`$. Because the fixed factor is shared and the powers of two are
nested, summing updates gives a residual denominator dividing
$`H^C2^{2K_t}`$; the factor is not multiplied once per round.

Score, variance and allowance calculations involve only a fixed further
number of products. For example, their denominators can be bounded by a fixed
power of $`H`$ times $`2^{4K_t}`$. The cumulative smoothing slack denominators
divide another fixed factor times $`2^{h_t}`$. Expert losses, mixed-action
losses and forecast action gaps have the same fixed-factor/dyadic form.

The root-effort induction gave $`K_t=O(\log(t+1))`$, and also
$`h_t=O(\log(t+1))`$. Denominators thus need $`O(\log(t+1))`$ bits. Residuals,
potential terms, losses and Lipschitz bounds have at most polynomial magnitude
in $`t`$, so their reduced numerators do also. This proves the claimed bit
bound. It does not prove a constant-time rational operation model or a total
end-to-end wall-clock guarantee.

The precision probe passed 2,821 exact assertions over two 256-round schedules
and five harmonic-denominator witness sizes. Its source hash is
`c7e05ad89d7122c64ccb63ee29fef5e046e8083f8d1d57b28e0671e81d3fe902`.
Observed execution was 406,434,039 ns, recorded separately from research effort.

## 14. Review of the integrated production module

I subsequently inspected `v3/checks/06_defensive_forecasting.py`, version
`p306-scalar-v2.1`, with SHA-256
`b66af7ec64b7e690aaa15c0901b2ccb220f93f97962052607481ddd7ae240e07`.
Its action rows are outcome-contingent costs, so the conversion to an intercept
and slope is exact. The clipped action mixture, feature block, slope diameter,
current-score Lipschitz bound and action accumulators agree with §8. The
`max_bisections=None` mode instantiates the sufficient root-budget condition;
the explicit capped mode honestly retains actual approximation allowance.
Its `dyadic_eta` helper instantiates §13 when combined with the other stated
fixed-input hypotheses.

The distinct [production formula probe](production_action_review_probe.py)
recomputes features and all scoring identities from the announced loss tables
and returned forecasts. It does not call the production feature, score or
accumulator-check functions as its oracle. Its
[saved result](production_action_review_probe_result.json) is PASS with 3,148
exact assertions, all 32 five-label paths under changing tables, a genuinely
exhausted zero-refinement case, 20 dyadic square-root enclosure cases and 256
dyadic-schedule comparisons. The checked production source hash was unchanged
throughout that run. Observed execution was 173,854,648 ns, with zero principal
research-time credit.

I also identified a public API issue in the initial `p306-scalar-v2` draft:
the pool's `copies` property exposed live learner objects, allowing a caller
to bypass pool settlement bookkeeping. The principal's `v2.1` revision exposes
frozen `CopySnapshot` records instead. I inspected that repair; the underlying
mathematical update is unchanged. Preservation and the broader API failure
record are owned by the principal and implementation reviewer.

**Final signed disposition:** the reconstructed mathematics and the inspected
`p306-scalar-v2.1` action-feature implementation support the limited claims in
this review. The precision counterexample, hard-decision obstruction and
sampling/delay qualifications must survive integration. No priority conclusion,
P3-N01 advancement, P3-07 work or later gate execution follows from this review.

**Signed:** ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer.
