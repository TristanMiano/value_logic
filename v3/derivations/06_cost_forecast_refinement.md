# P3-06 — Sequential refinement of cost forecasts

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
Status: **COMPLETE at the declared finite cost-forecast task scope**.
The [continuation record](../work_logs/P3_06_2026-10-09_S1.md) controls timing,
recovery and measured closure. The preserved October 8 addendum and its exact
saved evidence remain in the [recovery archive](../work_logs/P3_06_2026-10-09_S1/recovery/checkpoint_original/README.md).
This manuscript is a new version, not a recovered missing manuscript.

## 1. What is being refined

The object is one **fallible scalar forecast** of a versioned, deterministic
binary mathematical answer. Its number can answer known affine loss queries,
and a finite online procedure updates its state after checked answers arrive.
The forecast is distinct from the P3-03 hard-evidence cover and its conditional
certificates. No forecast, however confident, is admitted as a proof.

This is an explicit finite-feature adaptation of ordinary defensive forecasting.
In particular, the zero-allowance vector potential is Vovk's K29* construction;
expert, calibration and decision features use its direct-sum mechanism. The
[source comparison](../literature/06_forecasting_sources.md) identifies the
exact imported result and adaptation.
Cost notation by itself does not establish a new induction theory.

One episode declares a semantic version, a finite expert library with stable
indices, calibration resolution, feature scales, mathematical query family,
feedback/checking interface and root-search policy. Before its own answer is
received, round $`t`$ supplies:

- an immutable query identity and description;
- expert values $`q_{t,i}\in[0,1]`$ computed from admitted information;
- a known nonnegative finite issue-time weight $`w_t`$;
- optionally, two known affine action-loss rows and a positive smoothing scale.

The prototype's mathematical family is specified with the executable adapter
below. Generic expert numbers alone are not an implementation of arithmetic
learning. Shortcuts supplied inside experts are charged and are available to
ordinary comparators. Nothing here proves discovery of an identity absent
from the supplied computations.

For a checked binary answer $`y_t`$, an affine loss row has values
$`c_t(a,y)=b_t(a)+d_t(a)y`$. Its report is

```math
\widehat c_t(a)=b_t(a)+d_t(a)p_t.
```

This is a learned expected-loss estimate with an explicit binary probability
adapter. If $`d_t(a)\ne0`$, the known row recovers its forecast by
$`p_t=(\widehat c_t(a)-b_t(a))/d_t(a)`$. If the gap is zero, the row carries
no probability information. These are the inherited P3-02 known-payoff
identities; they do not certify the forecast's accuracy. Joint-event actions
need the additional information required by that earlier contract.

## 2. The continuous scalar construction

First consider one learner that receives its outstanding answer before it
issues another forecast. Write its local issuance order as $`t=1,2,\ldots`$.
Let $`\Phi_t:[0,1]\to\mathbb R^d`$ be a continuous feature vector determined
by information available before $`y_t`$. Define

```math
R_{t-1}=\sum_{s<t}(y_s-p_s)\Phi_s(p_s),\qquad
S_t(p)=\langle R_{t-1},\Phi_t(p)\rangle
       +\frac{1-2p}{2}\|\Phi_t(p)\|^2.
```

Choose $`p=0`$ if $`S_t(0)\le0`$; otherwise choose $`p=1`$ if
$`S_t(1)\ge0`$. In the remaining case the endpoints have opposite signs,
so a continuous root exists. Sign-preserving bisection at rational points
finds an approximate root; monotonicity is unnecessary. If its configured
budget expires, the actual residual is retained rather than treated as zero.

Every issued report stores the exact outcome-independent allowance

```math
A_t=2\max\{0,(1-p_t)S_t(p_t),-p_tS_t(p_t)\}.
```

This is the smallest nonnegative allowance bounding the next corrected
potential increment uniformly over the two answers. An accepted endpoint
has $`A_t=0`$, even if its score has large absolute magnitude. An interior
report with $`|S_t(p_t)|\le\delta_t`$ has $`A_t\le2\delta_t`$.

### CF-1: the checked potential inequality

For every binary sequence, with arbitrary predictable features and weights,

```math
\|R_T\|^2\le B_T,
\qquad B_T=\sum_{t\le T}p_t(1-p_t)\|\Phi_t(p_t)\|^2+
                  \sum_{t\le T}A_t.
```

Indeed, for $`e=y-p`$ with $`y\in\{0,1\}`$,

```math
e^2=p(1-p)+(1-2p)e,
```

and therefore

```math
\|R+e\Phi\|^2-\|R\|^2-p(1-p)\|\Phi\|^2
=2eS(p)\le A_t.
```

Telescoping from zero proves the claim. No stochastic truth law, independent
outcomes or correct expert is required. Exact arithmetic verifies a numerical
inequality under this model; it does not verify the semantic correctness of
an arbitrary externally supplied label.

## 3. Expert regret and calibration of the issued scalar

Fix positive scales $`\alpha,\beta`$ and integer $`m\ge1`$. Let

```math
b_j(p)=\max(0,1-|mp-j|),\qquad j=0,\ldots,m.
```

These continuous tents are nonnegative, sum to one, and have squared sum at
most one on $`[0,1]`$. The baseline feature vector is

```math
\Phi_t(p)=w_t\bigl(\alpha(q_{t,1}-p),\ldots,
  \alpha(q_{t,N}-p),\beta b_0(p),\ldots,\beta b_m(p)\bigr).
```

Let $`L_T=\sum_t w_t(p_t-y_t)^2`$ and
$`L_{T,i}=\sum_t w_t(q_{t,i}-y_t)^2`$. Square expansion gives the exact
identity, and hence the one-sided regret bound,

```math
L_T-L_{T,i}=\frac{2R_{T,i}}{\alpha}
            -\sum_t w_t(q_{t,i}-p_t)^2
\le\frac{2\sqrt{B_T}}{\alpha}.
```

The same issued $`p_t`$ simultaneously satisfies, for each declared tent,

```math
\left|\sum_t w_t b_j(p_t)(y_t-p_t)\right|
\le\frac{\sqrt{B_T}}{\beta}.
```

These are **CF-2** (weighted regret to every fixed supplied expert) and
**CF-3** (finite continuous-bin calibration). The regret comparator is not a
free per-round oracle. Negative signed regret is allowed; the conclusion is
an upper bound, not convergence of absolute regret to zero. Conditional-bin
error divides by $`\sum_t w_t b_j(p_t)`$, so rare bins have weaker guarantees.
No arbitrary discontinuous selector, context or changing bin is covered.

For the baseline features,

```math
B_T\le\frac{N\alpha^2+\beta^2}{4}\sum_t w_t^2+\sum_t A_t.
```

With $`W_T=\sum_t w_t>0`$, sufficient conditions for these normalized upper
bounds and signed calibration residuals to vanish are

```math
\sum_t w_t^2=o(W_T^2),\qquad \sum_t A_t=o(W_T^2).
```

The second condition concerns a squared-potential allowance, which is followed
by a square root. It is different from a per-round additive loss error. A
fixed bisection count does not itself ensure bounded score residual as state
grows. The actual recorded allowance determines what the finite result says.

## 4. Decision quality is a separate target

### CF-4: a conditional outcome-oracle bridge

For any finite binary affine loss table, let $`\widehat a_t`$ minimize its
forecast costs with an announced tie rule, and put
$`D_t=\max_a d_t(a)-\min_a d_t(a)`$. If $`a_t^*`$ minimizes the realized
cost, then

```math
0\le c_t(\widehat a_t,y_t)-c_t(a_t^*,y_t)
\le (d_t(\widehat a_t)-d_t(a_t^*))(y_t-p_t)
\le D_t|y_t-p_t|.
```

The first upper bound subtracts the nonpositive difference of the two
forecast costs. Thus

```math
\sum_t\bigl[c_t(\widehat a_t,y_t)-c_t(a_t^*,y_t)\bigr]
\le\sqrt{\left(\sum_t D_t\right)
                 \left(\sum_t D_t(p_t-y_t)^2\right)}.
```

If one supplied expert has vanishing normalized $`D_t`$-weighted squared
loss and the matching expert-regret bound is also sublinear, this yields
vanishing normalized outcome-oracle decision regret. Good predictive
structure is an additional premise. Calibration or small expert regret alone
does not supply it.

### CF-5: a hard-threshold obstruction

For $`n\ge1`$, take $`\epsilon_n=1/(8n)`$ and the two rounds

```math
(p_{2n-1},y_{2n-1})=(1/2-\epsilon_n,1),\qquad
(p_{2n},y_{2n})=(1/2+\epsilon_n,0).
```

For $`m=2`$, the three tent residuals after $`2n`$ rounds are
$`(H_n,0,-H_n)`$, where
$`H_n=\sum_{k=1}^n(\epsilon_k+2\epsilon_k^2)=O(\log n)`$.
Squared-loss regret to the constant expert $`1/2`$ is
$`\sum_{k=1}^n(2\epsilon_k+2\epsilon_k^2)=O(\log n)`$.
Nevertheless the action $`1[p>1/2]`$ is wrong on every round under 0–1 loss,
so its regret to either fixed action is $`n`$. For any fixed continuous test
function the paired residual tends to zero, hence its time average does too.
This is an exact counterexample to an implication, not a claimed trace of
our specific forecaster.

### CF-6: a continuous two-action extension

The implemented extension retains the same scalar forecast and appends
two continuous decision features. For the two announced affine rows write
$`d_0,d_1`$ for their slopes and
$`\Delta_t(p)=c_t(1,p)-c_t(0,p)`$. With $`\eta_t>0`$, let

```math
s_t(p)=\min\left(1,\max\left(0,
       \frac12-\frac{\Delta_t(p)}{2\eta_t}\right)\right),\qquad
\bar d_t(p)=d_0+s_t(p)(d_1-d_0).
```

Here $`s_t(p)`$ is an action-1 mixing weight. Its mixture forecast cost
exceeds the smaller of the two forecast costs by at most $`\eta_t/8`$:
inside the mixing interval the excess is
$`|\Delta|(\eta_t-|\Delta|)/(2\eta_t)`$, maximized at
$`|\Delta|=\eta_t/2`$; outside it the excess is zero.

Append $`w_t\gamma(\bar d_t(p)-d_i)`$ for $`i=0,1`$, with
$`\gamma>0`$. These features are continuous, so CF-1, CF-2 and CF-3 still
apply. Let $`\bar c_t(y)`$ be the loss of the issued mixture and let
$`G_{T,i}`$ be its appended residual coordinate. Then

```math
\sum_t w_t\bigl[\bar c_t(y_t)-c_t(i,y_t)\bigr]
=\sum_t w_t\bigl[\bar c_t(p_t)-c_t(i,p_t)\bigr]
  +\frac{G_{T,i}}{\gamma}
\le\sum_t\frac{w_t\eta_t}{8}+\frac{\sqrt{B_T}}{\gamma}.
```

This compares the mixture with either **fixed action identity**, even when
the announced loss table changes across rounds. It needs no accurate expert.
It does not compare with the outcome-optimal action chosen separately each
round. It is a loss of a fractional/randomized decision, not a bound on every
sampled realization. For mathematical answers independent of sampled actions,
it is the corresponding conditional expected loss; no sampling claim is
silently attached to the deterministic implementation.

Putting $`D_t=|d_1-d_0|`$, the two added squared features sum to at most
$`w_t^2\gamma^2D_t^2`$, since $`s^2+(1-s)^2\le1`$. Consequently

```math
B_T\le\frac14\sum_t w_t^2
 (N\alpha^2+\beta^2+\gamma^2D_t^2)+\sum_t A_t.
```

Bounded $`D_t`$, the preceding stake/allowance conditions, and
$`\sum_t w_t\eta_t=o(W_T)`$ give a vanishing normalized one-sided
fixed-action regret bound. Decreasing $`\eta_t`$ preserves the feature
magnitude bound but raises the Lipschitz constant and root-search work.
This is a rational smoothing adaptation of existing decision-exposure
defensive forecasting, not a new general decision-theoretic result.

## 5. Delayed feedback and unresolved answers

Each new query uses an idle copy; if none is idle, allocate a fresh copy.
A copy holds at most one pending forecast. Each copy's settled observations
therefore form a prefix of its own issuance subsequence. Expert computations
may use globally admitted past information, but no copy receives an unreturned
answer. Query and semantic version must match before settlement.

Let $`B_k`$ and $`R_k`$ be the copy-local quantities for the settled subset
at a cutoff. The sharper aggregate certificate is

```math
\left\|\sum_k R_k\right\|\le H:=\sum_k\sqrt{B_k}
\le\sqrt{K_+\sum_k B_k},
```

where $`K_+`$ counts only copies with positive $`B_k`$. Copies without scored
work contribute zero. Thus all preceding coordinate bounds hold with
$`\sqrt{B_T}`$ replaced by $`H`$; a rational upper enclosure or the last
Cauchy bound can be checked without an exact square-root primitive. This
proof is pathwise and does not import a stochastic delay-independence theorem.

For bounded weights and slopes, uniformly bounded root tolerance, and $`M`$
settled observations, the coarse normalized rate is of order
$`\sqrt{K_+/M}`$ when scored weight is proportional to $`M`$. More generally
the actual condition is $`H/W\to0`$, with the decision smoothing term checked
separately. The number of copies can destroy refinement: if all $`T`$ queries
arrive before any label, each starts a fresh identical state. Later settlement
does not repair those already-issued forecasts.

Pending answers are neither zero nor false and receive no score. An intermediate
bound is explicitly over settled subsequences. It does not estimate the
unresolved population, and an acquisition policy that selects easy answers
may make that population very different. Acquisition choices, a hard-copy
budget and the economic value of further computation remain P3-07 work.

## 6. Repricing: retained information and transferred guarantees

Retaining $`p_t`$ permits new known affine loss estimates for that same binary
answer. Retaining only an old cumulative weighted score generally does not
permit retrospective rescoring. For example, error vectors $`(1,0)`$ and
$`(0,1)`$ have equal unweighted sum and different scores under weights
$`(2,0)`$. Repeating the pair gives a linear discrepancy. This is an
information-loss witness for a proposed summary, not yet a regret witness.

A separate witness refutes unrestricted guarantee transfer. Issue $`p_t=1/2`$
on a balanced alternating binary sequence, with unit original weights and
the three constant experts $`0,1/2,1`$. Over each complete pair the scalar
has zero regret to the best expert and zero residual for every fixed test
of its report. Now rescore only the positions whose answer is one. Its new
loss per selected unit weight is $`1/4`$, while the constant-one expert's is
zero; its selected signed calibration error is $`1/2`$. The original two
guarantees therefore do not imply the reweighted ones. This is a counterexample
to a general implication, not an asserted trajectory of the implemented
forecaster. The retrospective selector was not among its original features.

The general audit record retains immutable query/version, issued forecast,
expert vector, old weight, semantic loss rows, issue order and any checked
answer/receipt. It supports three different operations:

| Operation | Information and conclusion |
|---|---|
| Answer a newly priced affine loss query | Use the retained scalar forecast and new known row; it remains an estimate. |
| Rescore old issued predictions | Use their retained answers and new weights; report exactly that retrospective metric. |
| Rerun the learning procedure under new weights | Replay issue/feedback order, expert-input policy and parameter versions; this may issue different forecasts. |

No rescoring operation retroactively changes the forecasts or their proven
issue-time guarantee. A replay supplied with old expert vectors is only a
fixed-expert-tape replay if those experts originally depended on changed
learner outputs; full-policy replay needs their computations too. A changed
semantic interpretation or withdrawn answer requires a new episode or a
separately proved transport, not silent editing of settled history.

### A restricted positive transfer result

Suppose a finite menu fixes its profile identities and dimension prospectively.
Each nonnegative weight $`w_{t,r}`$ is available before choosing $`p_t`$,
and the feature vector includes expert/calibration blocks
for each profile with positive scales $`\alpha_r,\beta_r`$. The same
potential proof gives each profile its own coordinate regret/calibration
bound. For any retrospectively selected real coefficient vector $`\lambda`$
that stays fixed across rounds, define
$`w_t(\lambda)=\sum_r\lambda_r w_{t,r}`$. The exact identities are

```math
L(\lambda)-L_i(\lambda)
=2\sum_r\frac{\lambda_rR_{r,i}}{\alpha_r}
 -\sum_t w_t(\lambda)(q_{t,i}-p_t)^2,
\qquad E_j(\lambda)=\sum_r\frac{\lambda_rC_{r,j}}{\beta_r}.
```

The coordinates belong to one common residual vector. Cauchy--Schwarz
therefore gives the following simultaneous bounds:

```math
L(\lambda)-L_i(\lambda)
\le2\sqrt{B_T}\sqrt{\sum_r(\lambda_r/\alpha_r)^2},\qquad
|E_j(\lambda)|\le\sqrt{B_T}\sqrt{\sum_r(\lambda_r/\beta_r)^2}.
```

The regret inequality requires each resulting $`w_t(\lambda)\ge0`$ so that
the distance term can be dropped. Nonnegative coefficients suffice, but
signed coefficients are also allowed when their resulting weights meet that
condition. The calibration identity and norm inequality are algebraically
valid even for signed resulting weights; interpreting them as frequencies
still needs nonnegative weights and a positive denominator. A canceling
signed sum of coefficients is not an upper-bound factor.

This is **CF-7**, a finite-menu extension of the general feature theorem.
It covers the represented span intersected with nonnegative resulting
weights for regret; it does not cover arbitrary unrepresented new per-round
weights. For unnormalized scoring alone, retaining per-profile losses and bin
residuals is sufficient for this menu, even if full history is absent.
Normalized scores also need per-profile total weights; conditional-bin errors
need their bin masses. The kernel and
finite-menu information arguments are ordinary linear algebra; whether the
extra features are worth their time, memory and looser norm bound is separate.
The main executable prototype uses one weight profile. The
[independent menu extension](../work_logs/P3_06_2026-10-09_S1/reviews/menu_extension_review.md)
implements the larger feature vector separately and preserves both signed
coefficient and negative-resulting-weight failure witnesses. No retrospective
menu features are silently added to a completed one-profile run.

## 7. Finite numerical work and value range

For a coordinate bounded by $`M_k`$ with Lipschitz constant $`D_k`$, the score
has the computable Lipschitz bound

```math
L_S=\sum_k\bigl(|R_k|D_k+M_k^2+M_kD_k\bigr).
```

It follows from the product rule on each affine piece and continuity at its
breakpoints. Expert coordinates use $`M_k=D_k=\alpha w`$; tent coordinates
use $`M_k=\beta w,D_k=m\beta w`$. Each decision coordinate admits
$`M_k=\gamma wD`$ and $`D_k=\gamma wD^2/(2\eta)`$. After $`k`$ bracket
updates, its midpoint is within $`2^{-k-1}`$ of a root, hence
$`L_S2^{-k-1}\le\delta`$ is a sufficient finite iteration allowance.

### CF-10: an unbounded native-cost extension

Fix the native cost unit. Before choosing $`p_t`$, announce two finite rational
rows $`c_t(i,y)`$, put $`D_t=|d_{t,1}-d_{t,0}|`$, and choose

```math
M_t=2^{\lceil\log_2\max(1,D_t)\rceil},\qquad S_T=\sum_{t\le T}M_t.
```

Exact comparisons with successive powers of two compute this scale without
a logarithm oracle. Feed the existing core weight $`w_t=M_t`$ and table
$`c'_t=c_t/M_t`$. Its mixture has native smoothing width $`M_t\eta_t`$.
Its weighted normalized mixture loss and fixed-action losses equal the
original native losses exactly. Moreover,

```math
M_t\gamma(\bar d'_t-d'_{t,i})=\gamma(\bar d_t-d_{t,i}),\qquad
B_T\le\frac{N\alpha^2+\beta^2+\gamma^2}{4}\sum_tM_t^2+\sum_t A_t.
```

Only the normalized slope **range** is at most one. Individual rows and
slopes may retain arbitrarily large shared components. The native signed
regret to either fixed action obeys

```math
G_{T,i}\le\frac18\sum_t M_t\eta_t+\frac{\sqrt{B_T}}{\gamma}.
```

The same forecast has CF-2 and CF-3 with weights $`M_t`$. These three upper
bounds divided by $`S_T`$ vanish if

```math
\sum_t M_t^2=o(S_T^2),\qquad \sum_t A_t=o(S_T^2),\qquad \eta_t\longrightarrow0.
```

The weighted smoothing term vanishes by splitting it into a fixed finite
prefix and an arbitrarily small tail width. Since $`M_t\ge1`$, a fixed
certified absolute root tolerance makes the allowance condition automatic:
$`\sum_t A_t/S_T^2\le2\delta/T`$. An exhausted fixed root cap still needs
its actual recorded allowance. A delayed pool requires $`H_T/S_T\to0`$
over its settled weight, plus the existing coverage qualification; normalizing
costs does not remove its copy penalty.

Under fixed certified root tolerance, dense schedules $`M_t=\Theta(t^a)`$
with fixed $`a>0`$ qualify and give a
potential contribution $`O(T^{-1/2})`$ after normalization. Dyadic
$`\eta_t=\Theta(1/t)`$ gives smoothing $`O(T^{-1})`$; bounded comparable
stakes give $`O(\log T/T)`$. A polynomial upper envelope alone is inadequate:
let $`D_t=t^2`$ at $`t=2^{2^k}`$ and zero elsewhere. Each new spike dominates
all earlier total stake, and the square-sum ratio tends to one along those
times. These statements concern normalization by total stake, not vanishing
native regret per unweighted round or outcome-oracle loss.

There is also a generic obstruction to an unrestricted unbounded-stake
theorem. For any issued binary reports, set $`w_t=r^t`$ and choose the
answer opposite the report's half-threshold. Every report loses at least
$`w_t/4`$. The better of the constant-zero/one experts loses at most all
stake before the final round, whose fraction of total stake is less than
$`1/r`$. Therefore, for $`r>4`$,

```math
\frac{L_T-\min_iL_{T,i}}{\sum_t w_t}>\frac{r-4}{4r}>0.
```

This is a lower bound in the generic adaptive binary-tape protocol. It is
not an impossibility claim for the declared modular-exponent family or for
a domain supplied with an exact predictive shortcut. The
[independent normalization review and probe](../work_logs/P3_06_2026-10-09_S1/reviews/unbounded_stakes_review.md)
verify the native-loss identities, concentrated-stake witnesses and scope.

Common known outcome-dependent offsets cancel from action regret and features,
but change absolute cost errors and incur their actual parsing/arithmetic
costs. This scheme neither calibrates every absolute cost stream nor selects
a universal bounded numerical carrier. The
[report-transport companion](06_forecast_transport.md) gives that distinction
and the separate CF-8/CF-9 report-mean and output-displacement results.

### CF-11: restricted finite numeric state

Exact rational arithmetic alone does not bound bit cost. The independent
denominator probes preserve cases with new odd denominators whose certificate
state becomes much larger than the dyadic reports. A proposed full-state
$`O(\log t)`$ claim with harmonic smoothing $`\eta_t=c/(t+1)`$ also failed:
the exact cumulative smoothing slack contains harmonic denominators. It is
not enough that the feature calculation itself divides by $`\eta_t`$.

A repaired proposition fixes dimension, feature scales and positive root
tolerance $`\delta`$, assumes uniformly bounded rational expert values,
weights and action-row entries with denominators dividing one fixed integer,
and uses the implemented schedule with a fixed positive rational $`c`$,

```math
\eta_t=c\,2^{-\lceil\log_2(t+1)\rceil},\qquad c>0.
```

In certified root mode, each issue needs $`O(\log(t+1))`$ bisections, and
every numerator and denominator in current numeric state, including smoothing
slack, has $`O(\log(t+1))`$ bits. Current numeric state uses
$`O(d\log(t+1))`$ bits; retaining every numeric issue and settlement record
once through round $`T`$ uses $`O(dT\log(T+1))`$ bits.

The proof first uses previous root success: bounded features and allowances
give $`B_{t-1}=O(t)`$ and $`\|R_{t-1}\|=O(\sqrt t)`$. The action-feature
Lipschitz constants grow only as $`O(t+1)`$, so the next score bound is
$`O((t+1)^{3/2})`$ and its computed bisection budget is logarithmic. This
proves the next root succeeds without assuming the desired bit bound.

Enlarge the fixed common denominator to include fixed scale factors and the
numerator of $`c`$. A feature evaluated at a dyadic candidate with exponent
$`k`$ then has denominator dividing a fixed factor times $`2^k`$; its
residual update uses at most $`2^{2k}`$. Across rounds these powers are
nested. Scores, variance, allowances and losses require only a fixed number
of further products, giving a fixed factor times $`2^{4K_T+O(1)}`$, where
$`K_T`$ is the largest candidate exponent so far. Smoothing sums have another
nested dyadic denominator. Since $`K_T=O(\log(T+1))`$ and magnitudes are
polynomial, numerator and denominator bit lengths are logarithmic. Candidate
exponents include the initial midpoint bit; they are not raw bisection counts.

Power-of-two native-cost normalization introduces no new odd factors. The
same argument extends to polynomially growing native input magnitudes with
fixed original denominators, because all extra scale exponents, state
magnitudes and score Lipschitz bounds remain polynomial. This numeric result
does not establish refinement without stake dispersion.

The [full independent precision proof](../work_logs/P3_06_2026-10-09_S1/reviews/independent_proof_review.md)
retains the rejected harmonic claim and checked dyadic repair. Arbitrary
input bit lengths, query strings, proof bodies, external expert work,
duplicate exported snapshots and a delayed pool's total copy/history size
remain separately charged. No constant-time rational-operation model or
hard end-to-end memory/CPU cap is claimed.

In particular, the mathematical adapter's residue-frequency expert uses
growing observation counts as denominators. It does not meet the fixed-input-
denominator premise merely because its values lie in $`[0,1]`$. Its actual
finite bit measurements remain evidence about those runs; they are not an
application of CF-11's asymptotic bound to that expert.

## 8. Implementation, development evidence and duty map

### A declared mathematical family and feedback interface

The [mathematical adapter](../checks/06_mathematical_forecast_development.py)
asks whether $`a^n\bmod m=r`$, with $`0\le a\le8191`$,
$`0\le n\le192`$, $`2\le m\le97`$ and $`0\le r<m`$ under one fixed
semantic version. A deliberately slow answer producer performs successive
modular multiplications. An independent binary-exponentiation checker
reconstructs the residue, with Python's modular power serving as a separate
development cross-check. The forecast is committed before the private answer
is produced and checked. Learning occurs only at the scheduled admission
event; private pending results are unavailable to expert updates.

The four supplied experts are constant one-half, an admitted residue-frequency
estimate, exact elementary shortcuts for declared bases/exponents, and a
fallible parity heuristic. They are computations available to the ordinary
comparators too. Their finite library and readable information are explicit;
their competence is not inferred from the word "mathematical."

A checked residue is cached by semantic scope and $`(a,n,m)`$, so it can
answer every associated equality query exactly. The planned duplicate query
receives a new request identity but reuses that exact admitted information.
Its old forecast record stays immutable; a separate interpretation record
marks the new checked status. A number from a fallible expert never enters
that cache as hard evidence.

This interface supports anticipation of a late answer when its information
is already available through an expert computation or an admitted equivalent
query. It does not prove an efficient learner discovers every recognizable
arithmetic pattern. Nor does finite-expert regret force low loss when every
expert is poor. The public development generator deliberately balances its
answers using an index-dependent rule; it is not a hardness construction or
a natural query distribution.

There is a further finite-domain limit. With a fixed finite semantic family,
permanent exact caching and eventual admission of every encountered residue,
only finitely many requests can remain fallibly predicted before all
encountered residue keys have been learned exactly. A qualitative eventual
accuracy statement can then follow from exhaustive caching alone. The
meaningful evidence here is the finite forecast/decision certificate before
those admissions and the stated generic sequence theorem. It is not an
asymptotic theorem for an unbounded language of mathematical claims.

### Implemented versions and preserved difficulties

The [polynomial core](../checks/06_defensive_forecasting.py), version
`p306-scalar-v2.1`, implements the exact feature, allowance and delay-copy
identities above using rational arithmetic. Configuration, predictions and
accumulators are immutable snapshots. Public inputs receive strict type,
range, identity and scope checks before mutation. A configured numerical cap
may return a valid forecast with a large actual allowance; the audit never
replaces that allowance by the requested tolerance.

The original addendum remains byte-for-byte intact. Its saved 1,510-check
result was readable and a new rerun reproduced its deterministic evidence.
Independent review found that this mathematical success did not validate its
entire interface: malformed calls could allocate copies, several settings
were insufficiently validated and expert names could mutate. The replacement
also had a v2.0 live-copy ownership defect before v2.1 made pool snapshots
read-only. These failures and exact source versions remain in the
[independent implementation records](../work_logs/P3_06_2026-10-09_S1/reviews/implementation_review_v2.md).

The adapter's current version is `p306-modular-development-v3`. Version 2
corrected the bit counter to inspect retained and pending records at each
committed issue/reveal boundary. Version 3 rejected Boolean/float numeric
aliases and mutable receipt-counter payloads before cache mutation, binding
admission to its registration-time canonical digest. The independent
[chronology and receipt review](../work_logs/P3_06_2026-10-09_S1/reviews/transport_and_harness_review.md)
preserves the failures and verifies the repairs. Hash binding is an integrity
check in this trusted in-process adapter, not cryptographic authentication
of an arbitrary proof producer or an atomic transaction across every external
consumer.

The v1, v2 and v3 runs have identical query populations, forecasts, scores
and core audit numbers. Their instrumentation and receipt encodings differ.
The original v1 result remains the immutable basis for the replay and later
prefix comparisons; each derivative records its input hashes. This is a
versioned evidence chain, not three independent demonstrations of predictive
performance.

### What the four development cases support

The [current saved report](../work_logs/P3_06_2026-10-09_S1/development/mathematical_queries_v3/REPORT.md)
covers four cases of 128 queries. At the delayed cutoff 120 labels are
admitted and eight remain pending; the other cases admit all 128. Metrics
use the same admitted labels and announced weights for every method.

| Case | Plain scalar Brier / weight | Decision scalar | Ordinary Brier AA | Exact arithmetic |
|---|---:|---:|---:|---:|
| Recurring shortcuts | 0.011165 | 0.110599 | 0.004223 | 0 |
| Nonshortcut null | 0.265712 | 0.308615 | 0.250303 | 0 |
| Delayed pending tail | 0.233969 | 0.282883 | 0.192746 | 0 |
| Varying stakes and actions | 0.266031 | 0.318507 | 0.251391 | 0 |

The ordinary Brier aggregator beats both polynomial variants on this score
in every case. Exact arithmetic answers every query correctly. The explicit
decision features supply a different guarantee but show no general empirical
advantage here. The same-core K29-star comparator agrees exactly by
construction; that equality verifies a reduction and does not count as an
independent implementation validation.

All recorded finite core inequalities hold. Their magnitude also matters.
The [bound-usefulness analysis](../work_logs/P3_06_2026-10-09_S1/development/mathematical_bound_usefulness_v1/ANALYSIS.md)
compares them with elementary bounds from the same retained forecasts and
action tables. All eight raw expert bounds improve the coarse unknown-weight
bound, but none improves the elementary envelope for the particular
retrospectively winning expert. Keeping the negative expert-distance term
improves two plain-variant comparisons. Keeping the actual forecast-action
gaps gives a negative certified upper bound of about -78.314 in the shortcut
decision case, whose actual mixed regret is about -97.398. That certifies an
improvement over both fixed action identities on those observations, not
over the adaptive ordinary or exact comparator.

Several bin certificates remain looser than their elementary forecast-range
bounds, especially with delayed copies or varying stakes. The numerical
allowance accounts for only about 0.000093%–0.155103% of the summed polynomial
budgets in these runs; their looseness primarily comes from the feature
variance and copy transfer, not insufficient root precision. For these fixed recorded forecasts, reducing only the allowance term
barely changes the bound. Rerunning at a tighter tolerance can change the
forecasts and variance too; that different trajectory was not tested here.

### Stronger ordinary comparisons change the claim

The [capital companion](06_capital_comparison.md) gives CF-12 and a separate
exact-enclosure implementation. It defends an ordinary finite sum of
exponential forecasting capitals, with constant finite-expert regret at
fixed stake cap and bounded total numerical allowance, plus simultaneous
tent and centered-action bounds. A fixed 32-query prefix comparison improves
both polynomial variants' Brier loss in all four prefixes, remains mixed
against ordinary AA, and still loses on accuracy to exact arithmetic. It
does not certify forecasts made by the earlier algorithm.

The [calibration companion](06_calibration_scope.md) supplies CF-13's
fixed-table readout, CF-14's theorem-only growing-tent extension and CF-15's
stronger established Fermi–Sobolev comparison. Ordinary K29-star already
provides square-root residual control on each fixed bounded Lipschitz ball;
the proposed finite-tent epoch rate is only $`T^{2/3}`$. The conditional
prefix-sum computation is checked algebraically, with no ordered-tree
implementation or runtime superiority claim.

The [primary-source record](../literature/06_forecasting_sources.md) also
reconciles delayed online learning, decision calibration, Logical Induction
and BRIA. BRIA's coverage condition concerns admissible action-matching test
histories and is not implied by the average metrics shown here. The exact
sparse witness and its boundary relative to the stronger capital theorem
are retained. The [stronger CF-16 witness](06_bria_boundary.md) has summable
scalar errors, constant regret, optimal decisions and bounded actual-path
capital monitors, yet fails coverage of an always-kept, always-testable
promise. It establishes a criterion nonimplication, not a production trace
or a counterfactual-outcome allowance certificate. Even summable output
perturbations need not preserve exact BRIA coverage. Neither cost notation
nor combining known forecast components
establishes a new induction theory. The prospect of a modest useful synthesis
still requires a specified contribution beyond these antecedents.

The [repricing companion](06_price_replay.md) verifies all three replay
services, while the [report-transport companion](06_forecast_transport.md)
retains the calibrated-distribution/uncalibrated-mean witness and explicit
output-displacement bounds. These address concrete information and report
semantics, not an assumption that all probabilities are mutually coherent.
The repricing companion also proves CF-17: coordinated weight/cost-unit changes preserve forecast
selection when scales, tolerances and capital envelopes are transported.
Genuine new objectives and representation-only unit changes are distinct.

### Selected duty dispositions

| Duty | Result at this task's scope | Remaining boundary |
|---|---|---|
| U06 — anticipation | Supplied shortcut experts and admitted canonical residues can anticipate scheduled answers; regret transfers the performance of a good supplied expert. | No discovery theorem for every efficient arithmetic pattern, proof process or logical-induction trader. |
| U07 — calibration | Pathwise finite-tent residual bounds for the actual scalar; restricted normalization, report-transport and theorem-only continuous-test extensions. | Rare-bin denominators, unbounded test complexity, discontinuous selection and general LI calibration remain separate. |
| U08 — expert regret | Exact finite supplied-expert Brier bounds; stronger ordinary capital comparison with its own code and allowances. | Comparator class and feedback are fixed by the contract; low regret is not low error without a good expert. |
| U09 — delayed evidence | Idle-copy transfer with explicit settled/pending partitions and actual copy penalty. | No unresolved-population accuracy or effective action-dependent paid-acquisition guarantee. |
| V01 — value meanings | Known affine estimates, issued probability, checked answer, conditional certificate and realized score are separate records. | Shared offsets can alter absolute cost error while leaving relative action regret unchanged. |
| V02 — retained information | Scalar affine query adapter, information-separating repricing witnesses, represented-menu transfer and verified full-policy replay on a fixed schedule. | Arbitrary new prices need sufficient history; changed evidence or semantics needs a new episode or proved transport. |
| V03 — action quality | Conditional outcome-oracle bridge; hard-threshold obstruction; two-action smooth fixed-comparator bound; fixed-table tent readout. | Mixed expected loss is not realized random-action performance, absolute value calibration or an unrestricted outcome-oracle guarantee. |
| V04 — resources | Charged expert, issue, producer, checker and retained-state measurements; restricted dyadic bit theorem and explicit cap-exhaustion cases. | No hard end-to-end CPU/heap guarantee, arbitrary-input bit bound or demonstrated practical advantage. Paid selection belongs to P3-07. |
| R01 — revision | Strict scope/identity checks, immutable old reports and explicit repricing services. | Live evidence withdrawal and general cross-version warrant transport are not implemented by this learner. |
| U03/U04 — coherence | Exact admitted canonical equivalents share checked answers. | Separate fallible scalar calls need not satisfy arbitrary cross-query logical or joint-probability constraints. |

The [readiness audit](../work_logs/P3_06_2026-10-09_S1/readiness_audit.md)
records the task criteria, review disposition and timing separately. No final
challenge has been frozen or exposed. P3-05's finding that cached decision
diagrams were faster than proof reuse in all six tested families remains
unchanged; this task supplies no contrary experiment.

P3-N01 remains **NOT YET SUPPORTED**. P3-07 and later gates are unstarted.
