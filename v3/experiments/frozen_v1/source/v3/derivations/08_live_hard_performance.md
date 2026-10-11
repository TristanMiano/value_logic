# Observable performance after live hard-answer correction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Task **P3-08**, **DEVELOPMENT**. This is a new composition result under
review, not a change to the historical P3-07 or R-P3-B-A experiments.

## 1. Question and inherited boundary

The [accepted selective-feedback service](07_selective_feedback.md#82-previously-proved-answers-and-the-hard-information-interface)
retains a fallible base forecast and improves an action, or a newly issued
forecast, when a current sound answer is already available. Pointwise
domination transfers upper loss bounds. Domination alone does not transfer
lower bounds. Further, a receipt early in a block can change a later live
forecast, so that live vector is not predictable before the block's selector.
The [observable-performance proof](07_observable_performance.md#8-integration-and-value-boundaries)
therefore cannot simply be rerun on the changed vector.

P3-08 retains more information than an inequality: the immutable base
forecast, the same base action draw, the actual selector, and the chronology
of current checked answers. On every corrected position these records reveal
the exact amount of loss removed. This note asks whether that additional
information permits a valid translation of both interval endpoints.

## 2. The unchanged base and the live process

Use the inherited exogenous binary query tape of length T=mB. The base
forecast q_t is fixed within a block given preceding selected feedback.
Exactly one position J_k is selected with the owned positive propensity
pi_kt, and its checked receipt corrects the selected terminal action. The
base learner uses only those selected labels at block boundaries.

Let H_t indicate that, **before the live forecast at t is issued**, the hard
store supplies the sound answer y_t for the complete current semantic key.
It may become one because of a receipt earlier in the same block. The live
forecast is q'_t=y_t on H_t=1 and q_t otherwise. Both prospective actions
use the same supplied uniform draw; draws are consumed even on known
positions. The selected terminal action is correct in both processes.

Hard receipt admission, query selection, weights, resource admission and
the issued forecasts do not depend on sampled terminal actions. Scope
withdrawal ends the current statistical epoch. Only a complete successful
quota episode is reported. Both the expectation theorem and the displayed
unconditional confidence theorem require all-path completion and funding,
including the added reporting service; completion of one budget-limited seed
is not that premise. In particular, there is no 95% coverage assertion
conditional on selectively successful completion. Sound checked receipts
and independent fair bits remain
mathematical assumptions. A public pseudorandom development seed does not
establish coverage.

Write d_t=q_t+(1-2q_t)y_t and g_t=(q_t-y_t)^2. Let F_0 be the sum of base
Brier losses, V_0 the sum of base d_t on unselected positions, and Z_0 the
actual base terminal errors. Define F_1,V_1,Z_1 for the live process. Given
the complete selector history, V_1 is the live terminal-error mean: the
remaining action bits are independent of that history and of hard state.

## 3. Observable exact differences

The following quantities use only retained base records and answers whose
current sound warrants existed before the relevant live issuance:

```math
\Delta_F=\sum_{t:H_t=1}(q_t-y_t)^2,\qquad
\Delta_V=\sum_{t\notin\{J_k\}:H_t=1}d_t,\qquad
\Delta_Z=\sum_{t\notin\{J_k\}:H_t=1}\mathbf1\{a_t^0\ne y_t\}.
```

The selected positions are excluded from the last two sums because both
terminal services already correct those actions. They are not excluded from
the first sum: Brier loss scores the forecast as issued, before a current
purchase. A receipt bought on that position cannot retroactively remove its
earlier forecast loss.

For every admitted complete path,

```math
F_1=F_0-\Delta_F,\qquad V_1=V_0-\Delta_V,\qquad Z_1=Z_0-\Delta_Z. \tag{1}
```

**Proof.** At an uncorrected position the base and live outputs coincide.
At a position with a prior sound answer, the live Brier loss and prospective
error probability are zero. On an unselected such position the common draw
also gives a pathwise reduction of the base error indicator to zero. Both
selected terminal actions have zero error. Summing these exhaustive cases
proves (1). No conditional zero-mean assertion about the live forecast
vector is used. The deltas may depend on the current selector.

As a general consequence, a valid event L<=X<=U and an observable exact
identity X'=X-Delta imply L-Delta<=X'<=U-Delta on the **same event**. Delta
need not be independent of X, L or U. This extra exact identity, rather than
domination alone, is what licenses a lower endpoint.

## 4. Preserve the base sampling residual

Let U_c,A_c,C_k,Q,R and the fixed-rate sampling radius be the **base**
statistics in [the inherited observable-performance result](07_observable_performance.md#3-a-public-identity-links-the-two-unknown-performances).
In particular, with r_t=d_t-1/2,

```math
U_c=\frac{T-m}{2}+\sum_k(\pi_{kJ_k}^{-1}-1)r_{kJ_k},\qquad
A_c=\frac T2-\sum_tq_t(1-q_t)+\sum_k\frac{r_{kJ_k}}{\pi_{kJ_k}},
```

and V_0-U_c=F_0-A_c. Define the live centers

```math
U'_c=U_c-\Delta_V,\qquad A'_c=A_c-\Delta_F.
```

Equation (1) gives the **same exact shared residual**

```math
V_1-U'_c=V_0-U_c=F_0-A_c=F_1-A'_c. \tag{2}
```

The base vector and its base widths are predictable. Therefore their
conditional moment proof continues to bound (2), even when the live vector
is not predictable. The width Q is not recomputed on selection-dependent
live forecasts. This construction does not assert that its widths or final
endpoints are optimal.

## 5. A paid two-sided live report

Use S=B for uniform selection or S=2B for the declared ticket selector,
R=S ceil(sqrt(2m)), and Q=sum_k C_k^2 with
C_k=max_t |1-2q_t|/pi_kt. Fix these rate choices prospectively. The inherited
two-sided sampling radius is

```math
\rho=Q/R+5R/8.
```

Let n_1 be the number of unselected positions with H_t=0. Conditional on
the complete action-independent selector and hard-state history, these are
the only possibly erroneous live terminal draws. For

```math
r_1=\left\lceil\sqrt{\left\lceil5n_1/2\right\rceil}\right\rceil,
```

the same two-tail bounded-moment argument gives conditional action failure
probability at most 1/40 (and zero if n_1=0). Integrating over the selector
history preserves that bound; n_1 need not be constant across histories.
The two base sampling tails together cost at most 1/40. Hence, for this
declared episode at its fixed end,

```math
\Pr\left[
 |V_1-U'_c|\le\rho,\quad
 |F_1-A'_c|\le\rho,\quad
 |Z_1-U'_c|\le\rho+r_1
\right]\ge19/20. \tag{3}
```

The all-path completion premise in section 2 applies to (3); reporting only
successful budget-selected realizations does not turn it into conditional
coverage among those realizations. The implementation withholds its
confidence-eligible flag when the funding premise is absent.

This chosen report uses the live conditional action tail. Alternatively,
one can translate a pre-existing interval for Z_0 by Delta_Z using (1).
The implementation must not silently take a favorable minimum of several
separately budgeted confidence constructions. Delta_Z remains useful as
an exact pathwise audit quantity without invoking that extra interval.

Intersect (3) with deterministic observable envelopes: hard-known live
losses are zero; purchased issued Brier losses are exactly known; other
issued Brier losses lie between min(q^2,(1-q)^2) and its maximum; unselected
unknown conditional errors lie between min(q,1-q) and its maximum; actual
terminal errors lie between zero and n_1. Retain an empty intersection as a
confidence conflict. If n_1=0, V_1 and Z_1 are exactly zero. Since every
other position was purchased, F_1 is then exactly observable as well.

For nonnegative error price c and the same episode's observed paid resource
bill r, the terminal interval maps pathwise to c*[L_Z,U_Z]+r. The report's
own bill must be included. This does not forecast a future bill or justify
a changed purchase policy. Different methods/episodes do not receive joint
coverage from (3) without an additional error allocation.

## 6. Small separator from naive recomputation

Take B=2, one repeated false query, q_1=q_2=1/4, and uniform selection.
Initially there is no hard answer. If J=1, the first checked receipt makes
the second live forecast zero; if J=2, both live forecasts remain 1/4.
The base centers are U_c=1/4 and A_c=1/8, with zero actual sampling residual.

| Selected position | Live forecasts | Delta_V | Delta_F | Live V | Live F |
|---|---|---:|---:|---:|---:|
| 1 | (1/4,0) | 1/4 | 1/16 | 0 | 1/16 |
| 2 | (1/4,1/4) | 0 | 0 | 1/4 | 1/8 |

The translated centers equal both live targets in both cases. By contrast,
naively applying the constant-half-centered formula directly to the live
vector yields U=1/4 in both cases; its mean residual is -1/8. Applying the
hard-mask center to a nonpredictable live mask gives a different failure
(mean residual +1/8). Neither is a martingale-difference proof. These
failures leave the inherited predictable-snapshot construction intact.

## 7. Implementation and limits

The new paid reporter will retain unreduced exact rational pairs and use a
bounded integer tariff. Its main development comparison will be sealed
before private truth scoring. A separate independent Fraction-based audit
will verify all identities and interval formulas; it is evaluator work,
not a free deployment capability. Source and trace reads, validation,
arithmetic, storage and terminal output are deployment costs.

The theorem relies on the extra observable correction records and unchanged
base sampling process. Skipping a selected purchase, changing the update
rule, using stale answers, allowing action-dependent hard selection, or
discarding the base records needs a new argument. It makes no calibration,
coherence, logical-induction or general economic-advantage claim. Its
contribution is a finite paid interface for this hybrid, using established
sampling and concentration tools already attributed in the inherited
[primary-source comparison](../literature/07_selective_feedback_sources.md#9-sampling-inference-and-the-fixed-rate-boundary-are-established-tools).
