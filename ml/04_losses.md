# Structured learning objectives and symbolic licensing

## Status and decision

This document completes Task 18. It chooses the learning objective for the
hybrid interface fixed by
[`01_encodings.md`](01_encodings.md),
[`02_relu_architecture.md`](02_relu_architecture.md), and
[`03_representation_theorems.md`](03_representation_theorems.md).

The reference decision is:

1. **Primary objective:** learn externally defined, atom-sufficient continuous
   statistics with a standardized center--radius loss. Squared error trains the
   center and a central interval score trains the predicted radius.
2. **Calibration:** on a disjoint held-out split, calibrate additive residual
   expansion of the proposed interval. A versioned external mode/checker must
   accept the calibration record before the expanded region can support or
   refute an atom.
3. **Decoder:** derive atom values and public outcomes exactly through the
   evidence gate, boundary-aware region relations, `WF`, and finite `K_3` meet.
4. **Simple baseline:** train an independent three-way cross-entropy classifier
   for each meaningful atom. It predicts `supported/open/refuted` fidelity but
   never authorizes production use.
5. **Router:** train selection utility with a separate, exact-mask-respecting
   pairwise ranking objective. Router loss cannot create a license.

Direct atom-state logits, aggregate public-status logits, reason classifiers,
and self-license heads are auxiliary diagnostics or ablations. They are absent
from the production authorization path. Optimization success is evidence about
prediction performance, not a proof or certificate of adequacy.

## 1. Four levels that must not collapse

The word “loss” refers to different mathematical objects at four levels.

| level | object | role | example |
|---|---|---|---|
| task | `L_q`, aggregation `rho_q`, and risk `J_q(e)=rho_q(L_q(e))` | says what success means for the use plan | prediction error, decision regret, latency, or a typed risk vector |
| estimator | `f_theta` and its statistic heads | predicts an outcome, sufficient statistic, `J_q`, or a region containing it | risk center `c_hat` and proposed half-width `r_hat` |
| optimization | `\mathcal L_train(theta)` | chooses parameters from external targets | standardized squared error plus interval score |
| certification | `CertMode(record) |- J_q(e) in U` and the exact region decoder | states when an estimate may support/refute an atom | checked held-out envelope, confidence bound, formal proof, or other named mode |

The criterion is not its estimator. The estimator is not its training loss. A
small training loss is not the certificate relation. A certificate for an
estimator is not automatically a certificate that every plan using the
estimator satisfies the target criterion.

This separation is especially important for recursively structured plans. A
loss estimator can be a node inside `e`, can emit a payload and quantitative
grade, and can itself be evaluated by another request. The finite acyclic
construction of
[`formalism/08c_proof_carrying_plans.md`](../formalism/08c_proof_carrying_plans.md)
admits that structure. It does not admit an unqualified cycle in which the
result grants the estimator that generated the result.

### 1.1 Parameters with different meanings

The reference notation reserves distinct names:

```text
epsilon_task   acceptable target risk or other ordered threshold in q
alpha_int      nominal miscoverage used by the interval training score
alpha_cal      miscoverage level of a named held-out calibration mode
eta_cal        additive calibration radius returned by that mode
tau_reject     threshold for the conservative learned-reject proposal
kappa          desired router coverage, if a coverage target is imposed
lambda_*       optimization weights only
```

`epsilon_task`, `alpha_int`, and `alpha_cal` are not interchangeable. In
particular, conformal literature often calls its miscoverage parameter
`epsilon`; this project does not.

## 2. What the estimator learns

Fix an atom address `a`, request context `q`, plan `e`, and dependency-scoped
input `x_a=(a,pi_a)` from Task 15. A schema registry declares an externally
defined statistic

```text
t_a = T_a(source record, e, q)
```

that is sufficient for the atom relation the decoder must evaluate. Examples
include:

- scalar risk `J_q(e)` for an adequacy atom;
- candidate and fallback risks for an improvement atom;
- typed constraint coordinates;
- pairwise loss or resource differences for a comparison proposal; and
- a numerical payload or grade of a proof-erased plan node.

`T_a` is fixed before fitting. In the synthetic experiment it should be
computed from the generator's independently defined ground truth or from a
frozen evaluation record. In an empirical application it should cite the
outcome source, loss implementation, risk aggregation, sampling frame, units,
and version. A network prediction, its own decoded status, or a label produced
from an unaccepted model certificate is not an external target.

For the reference scalar statistic, the network returns

```text
c_hat_a in R,
r_hat_a = ReLU(o_r) >= 0,
U_hat_a = [c_hat_a-r_hat_a, c_hat_a+r_hat_a].
```

The radius is an uncertainty proposal. It is useful even before calibration
because it can rank heterogeneous cases and express conditional width, but it
has no certificate status by itself. Direct endpoints are allowed when an
external check enforces `lower<=upper`. Non-scalar risk schemas use their own
typed region and score rather than an arbitrary scalarization.

### 2.1 Data split contract

After Checkpoint C, the experiment protocol is:

```text
train                       fit theta and training-only normalization constants
envelope calibration        fit eta_cal for the frozen scorer
reject/router validation    fit rejection and selection thresholds
system audit                construct lower-ranked system evidence
final confirmation          evaluate the fully frozen system once
```

The split identifiers, generator version, candidate registry, scopes, and
grouping rules are stored in the appropriate records. The five roles must be
disjoint at the independent generator-world/trajectory, provenance-root, and
plan-family levels registered in Task 19; row-ID disjointness alone is
insufficient. Adaptive domain, group, or model selection performed after
inspecting a held-out role needs another held-out role, simultaneous correction,
or a certificate mode that explicitly covers the adaptation.

## 3. The primary statistic objective

Let `sigma_a>0` be a registered unit scale, preferably fixed by the task. If no
natural scale exists, compute a robust training-split scale with a declared
positive floor, freeze it, and version it. Define standardized quantities

```text
t_tilde = t_a/sigma_a,
c_tilde = c_hat_a/sigma_a,
l_tilde = (c_hat_a-r_hat_a)/sigma_a,
u_tilde = (c_hat_a+r_hat_a)/sigma_a.
```

The point component is

```math
\ell_{\mathrm{ctr}}(a)=(\widetilde c_a-\widetilde t_a)^2.
```

Squared error is chosen because the reference target is the conditional mean
or a directly observed deterministic statistic. If a later task instead
declares a median, quantile, or heavy-tail functional, it must change the
scoring rule and the semantic target together; replacing squared error by
Huber loss without saying what functional is elicited is not neutral.

After fitting the center mapping, freeze it while fitting the radius (or apply
an explicit stop-gradient to `c_hat` in the interval term). This prevents the
width objective from directly moving the statistic center it is supposed to
estimate. If a shared trunk is jointly fine-tuned instead, that is a reported
multi-task ablation because finite shared capacity can trade center and width
accuracy.

For `0<alpha_int<1`, the central interval score is

```math
\begin{aligned}
\operatorname{IS}_{\alpha}(l,u;t)
&=(u-l)
 +\frac{2}{\alpha}(l-t)_+
 +\frac{2}{\alpha}(t-u)_+ .
\end{aligned}
```

It trades width against misses and is closely related to the two endpoint
quantile scores. Proper scoring rules and the interval score are reviewed by
`GneitingRaftery2007`. The project makes the more restricted symmetric
center--radius parameterization for a simple first experiment; asymmetric
endpoint heads are a later option, not an assumption that uncertainty is
actually symmetric.

For schema `s`, let `I_s` be the observed targets of that schema. Missing
targets are not in `I_s`. The schema-balanced loss is

```math
\mathcal L_{\mathrm{stat}}
=\frac{1}{|\mathcal S_{\mathrm{obs}}|}
 \sum_{s\in\mathcal S_{\mathrm{obs}}}
 \frac{1}{\sum_{i\in I_s}w_i}
 \sum_{i\in I_s}w_i
 \left[
  \lambda_c\ell_{\mathrm{ctr}}(i)
  +\lambda_I\operatorname{IS}_{\alpha_{\mathrm{int}}}
     (\widetilde l_i^{\mathrm{sg}},\widetilde u_i^{\mathrm{sg}};
      \widetilde t_i)
 \right].
```

Here `l_tilde^sg=(stopgrad(c_hat)-r_hat)/sigma` and
`u_tilde^sg=(stopgrad(c_hat)+r_hat)/sigma`. The displayed sum specifies the
two head targets and evaluation score; the reference optimization schedule is
center first, radius second with the center mapping frozen.

Balancing at the schema level stops a frequently instantiated atom family from
winning only because it has more rows. `w_i` may correct an externally known
sampling design; it may not be set from the model's confidence in its own
target.

### 3.1 Full structured objective

For the modules actually present, the primary training objective is

```math
\mathcal L_{\mathrm{primary}}
=\mathcal L_{\mathrm{stat}}
 +\lambda_y\mathcal L_{\mathrm{payload}}
 +\lambda_g\mathcal L_{\mathrm{grade}}
 +\lambda_v\mathcal L_{\mathrm{reject}}
 +\lambda_R\Omega(\theta).
```

- `L_payload` is typed to the declared payload: squared error, cross-entropy,
  or another proper task-specific score.
- `L_grade` scores a quantitative bound/resource proposal in its own units.
  An asymmetric underestimation penalty is allowed when the grade semantics
  justify it, but the resulting grade still needs external evidence.
- `L_reject` is the one-way learned-validity auxiliary in Section 6.
- `Omega` is ordinary capacity control applied in normalized coordinates.

Absent heads contribute no term. Resource coordinates such as latency, energy,
and memory are not summed until a declared scalarization supplies common units
and weights. There is no direct public-status or self-license term in the
reference objective.

### 3.2 Optional calibration-score head

The predicted radius is the reference uncertainty score. If a later procedure
adds a distinct nonnegative scale `q_hat_a`, its semantics must be registered.
One admissible construction calibrates normalized residuals

```text
s_a/q_hat_a
```

and expands by `eta_cal q_hat_a`, with a positive floor on `q_hat_a`. A free
“confidence” logit with no external residual target or held-out calibration map
is not part of the primary system.

## 4. Held-out calibration is a proposal until checked

For a calibration example with target `t_i` and trained interval
`[l_hat_i,u_hat_i]`, define additive residual nonconformity

```math
s_i=\max\{\widehat l_i-t_i,\ t_i-\widehat u_i,\ 0\}.
```

With `n` held-out residuals and desired miscoverage `alpha_cal`, the reference
split-conformal-style proposal uses

```math
k=\left\lceil(n+1)(1-\alpha_{\mathrm{cal}})\right\rceil,
\qquad
\eta_{\mathrm{cal}}=s_{(k)},
```

where an infinity sentinel is appended. Thus `eta_cal=+infinity` when `k>n`;
too little data produces an uninformative proposal instead of invented
certainty. The expanded proposal is

```math
U_a^{\mathrm{prop}}
=[\widehat l_a-\eta_{\mathrm{cal}},
  \widehat u_a+\eta_{\mathrm{cal}}].
```

Only after the mode checker accepts the record is `U_prop` registered as the
usable `U_safe`. A rejected, expired, out-of-scope, or unbounded proposal cannot
support or refute.

Under the exact split-conformal exchangeability and split assumptions, this
construction supplies marginal target-in-region coverage at the declared
level; `ShaferVovk2008` is the project's verified primary conformal reference.
That imported guarantee is not yet a project certificate. The mode checker
must also verify at least:

- target/statistic schema and units;
- train/calibration disjointness and frozen scorer version;
- exchangeability or the exact alternative assumption;
- scope, group, candidate registry, and time validity;
- the finite quantile and infinity convention;
- whether adaptive selection or repeated use is covered; and
- a bridge from coverage of `t_a` to the atom's target proposition.

If `t_a` is one future point loss, prediction coverage does not by itself prove
that a domain mean or worst-case risk is below `epsilon_task`. If `t_a` is an
externally constructed domain-risk statistic, the certificate must state its
sampling and estimation guarantee. Conformal risk control
(`AngelopoulosEtAl2024`) is a possible future certificate mode for bounded
monotone loss families; its hypotheses and guarantee would replace, not be
silently inferred from, the simple residual-envelope mode above.

Calibration groups must be declared before inspecting the calibration labels.
An undersized group returning an infinite radius remains open. Pooling it after
seeing that result changes the procedure and requires a new record.

## 5. Symbolic atom and public-state derivation

For a smaller-is-better scalar atom, let

```text
U_safe=[lower(U_safe),upper(U_safe)],
m_support = epsilon_task-upper(U_safe),
m_refute  = lower(U_safe)-epsilon_task.
```

The production decoder applies this order:

```text
1. WF failure
   -> Undefined with the exact WF error.

2. Missing, expired, conflicted, out-of-scope, checker-rejected,
   uncalibrated, or learned-rejected evidence
   -> meaningful atom Open with its indexed obstacle, when the request is WF.

3. usable evidence and can_support and m_support >= 0
   -> Supported with the accepted witness.

4. usable evidence and can_refute and m_refute > 0
   -> Refuted with the accepted counterwitness.

5. otherwise
   -> Open with boundary or polarity obstacle.
```

The inclusive support and strict refutation conventions match Tasks 16--17.
They ensure a point region `{epsilon_task}` supports while its positive ReLU
surplus is zero. `can_support` and `can_refute` are exact certificate-mode
fields, not learned class probabilities.

### 5.1 Positive and countercertificate evidence

Evidence polarity is not the complement of a label:

| accepted mode | may support | may refute | unsupported conclusion |
|---|---:|---:|---|
| checked two-sided region | yes | yes | boundary crossing remains open |
| certified upper bound | yes | no | a bad-looking estimate cannot refute |
| certified lower bound/countercertificate | no | yes | a good-looking estimate cannot support |
| empirical proposal only | no | no | both polarities remain open |

A missing positive certificate is not a countercertificate. A missing
countercertificate is not positive evidence. Training targets for either
polarity are generated by the external evidence constructor and exact decoder;
the model does not manufacture negative examples by complementing its own
support predictions.

### 5.2 Profile aggregation

For a well-formed request with required atom values `v_1,...,v_m`, compute

```text
v_P = meet_K3(v_1,...,v_m)

Supported -> Granted
Open      -> Withheld
Refuted   -> Refused.
```

`WF` failure yields `Undefined` before this meet. Report-only diagnostics and
safety projections remain address-indexed. Multiple plans can independently be
granted, and every plan can fail to be granted. There is no softmax across the
library.

### Proposition 1 — decoder consistency

For a nonempty interval, support and refutation cannot both be decoded.

**Proof.** Support requires `upper(U)<=epsilon_task`. Refutation requires
`lower(U)>epsilon_task`. Since `lower(U)<=upper(U)`, their conjunction would
give `lower(U)<=epsilon_task<lower(U)`, a contradiction. The exact evidence
gate can only remove a polarity, so it cannot create a contradiction. `WF` and
finite `K_3` meet then determine exactly one public outcome. ∎

### Proposition 2 — statistic targets preserve tolerance transport

Fix an accepted region `U` and all request fields except the scalar tolerance.
If support obtains at `epsilon_1` and `epsilon_2>=epsilon_1`, support obtains at
`epsilon_2`. A status code at only one tolerance `epsilon_0` is not sufficient
in general to recover status at another tolerance `epsilon'`.

**Proof.** `upper(U)<=epsilon_1<=epsilon_2` proves the first claim. For the
second, risks `0.1` and `0.2` are both supported at tolerance `0.3`, so a code
retaining only that label may identify them; tolerance `0.15` separates them.
Thus learning the statistic/region preserves a query that the frozen status
label can erase. ∎

This is the main formal reason for preferring statistic regression to direct
classification. It does not prove that the structured objective will train
better; that is the empirical hypothesis in Section 12.

## 6. Exact validity, learned rejection, and missingness

Exact observation state remains in the side packet:

```text
present / missing
current / expired / corrected
conflict / resolved
checker accepted / rejected
scope membership
calibration record accepted / absent
```

A learned validity head predicts only a conservative reject probability
`p_reject`. Its externally defined target `b_reject` comes from a frozen scope,
shift, corruption, or quality audit. The optional asymmetric binary loss is

```math
\ell_{\mathrm{reject}}
=-w_1 b_{\mathrm{reject}}\log p_{\mathrm{reject}}
 -w_0(1-b_{\mathrm{reject}})\log(1-p_{\mathrm{reject}}),
\qquad w_1>w_0
```

when missing a known bad case is more costly than conservatively withholding a
good case. `tau_reject` is selected on held-out data and is versioned. If no
credible external reject labels exist, omit this head.

At inference:

```text
effective evidence usable
= exact evidence usable AND p_reject < tau_reject.
```

A learned rejection can turn would-be support or refutation into open. A
favorable score cannot turn missing, expired, invalid, or checker-rejected
evidence into support. The exact state always dominates.

Missing target values are masked out of statistic loss and counted. They are
not imputed as zero, because zero can be a valid risk, cost, margin, payload, or
grade. Missing input evidence is an exact observation feature and normally
decodes open. An optional model of future evidence availability is a separate
forecast head; it cannot overwrite actual missingness.

`Open` may result from missingness, uncertainty-band crossing, one-sided
evidence, conflict, expiry, learned rejection, or unresolved comparison. The
ternary value is enough for the meet, but the diagnostic obstacle is retained
for audit and update.

## 7. Cross-entropy and atom-state auxiliary heads

The simple baseline has one independent logit triple per meaningful atom:

```text
h_a=(h_a^support,h_a^open,h_a^refute),
p_a=softmax(h_a),
L_CE=-sum_a log p_a[y_a].
```

The target `y_a` is generated by the external ground-truth/evidence record and
the exact boundary decoder. Static `WF` remains external. Public outcome is
still obtained by symbolic `K_3` meet over the predicted atom classes for
fidelity evaluation; there is no aggregate four-way production head.

This is a useful baseline because it is small, standard, contradiction-free
within one atom, and can express multiple or empty granted-plan sets when
applied independently across plans. It is weaker than the primary design:

- the label depends on `epsilon_task`, mode, and evidence state;
- it discards risk magnitude, interval width, and boundary distance;
- it cannot be recalibrated by expanding a quantitative region;
- it does not distinguish different reasons for open without the exact side
  packet; and
- a low cross-entropy does not establish an accepted certificate relation.

Cross-entropy is proper for the externally defined class distribution when its
usual probabilistic assumptions hold. That makes it a sound class-prediction
loss, not a proof that the classes correspond to true adequacy. It is expected
to be competitive on a frozen tolerance and evidence regime and weaker on
tolerance transfer, boundary calibration, and new certificate modes.

An auxiliary atom-state head may be attached to the structured trunk to probe
whether the learned statistic representation exposes the decoder classes. Its
gradient is off by default; if used as a regularizer, the experiment must report
it as a separate condition and verify that production output is unchanged when
the head is removed. A direct public-status head, flat reason classifier, and
self-grant head are ablations only.

## 8. Router and ranking loss are separate

Licensing precedes selection. Let `A_P(x)` be the exact active set under the
selector's named profile. The router receives only candidates in `A_P(x)` and a
separately declared external selection cost `C_i(e)`. For every resolved active
pair `(e,j)` with unequal costs, define

```math
y_{iej}=\operatorname{sign}(C_i(j)-C_i(e))
```

so `y=+1` means `e` is preferred. With router utilities `u_hat`, use

```math
\mathcal L_{\mathrm{rank}}
=\operatorname{mean}_{(i,e,j)\in\mathcal R}
 \log\left(1+\exp\left[-y_{iej}
 (\widehat u_i(e)-\widehat u_i(j))\right]\right).
```

`R` contains only exact-active, externally resolved, comparable pairs. An
inactive candidate, missing comparison, unknown pair, or tie is masked rather
than labeled as a loss. An optional standardized cost-regression term may be
added when calibrated utility magnitude matters. Pairwise ranking alone learns
order, not task-cost scale.

The router is trained in a separate stage or with detached license-statistic
features and a separate optimizer term. Inference applies the exact active mask
again before argmax/soft routing. If `A_P(x)` is empty, return the declared
fallback/information action/abstention. No router score can reactivate an
inactive plan.

The exact profile matters:

- Under `P_rely`, an active plan is warranted for the declared reliance use but
  need not be comparatively preferred. The selector may still choose another
  active plan or the fallback if its policy permits.
- Under `P_pref-rel` or `P_pref-cert`, comparative conditions are already part
  of the exact license profile at their stated finite-set strength.
- A use plan can remain adequate and licensed under one profile while a newer
  plan is selected under another. The router does not rewrite the first fact.

## 9. Selective risk, reject options, and the status quo

Let `g_i=1` when the system selects a licensed plan rather than its fallback,
and let `L_i^sel` and `L_i^F` be target losses. Report jointly

```math
\operatorname{Coverage}=\frac1n\sum_i g_i,
```

```math
R_{\mathrm{sel}}
=\frac{\sum_i g_i L_i^{\mathrm{sel}}}{\sum_i g_i}
\quad\text{when }\sum_i g_i>0,
```

and

```math
R_{\mathrm{deploy}}
=\frac1n\sum_i
\left[g_iL_i^{\mathrm{sel}}+(1-g_i)L_i^F\right].
```

Selective risk without coverage can be made small by rejecting nearly
everything. Coverage without fallback loss treats rejection as free. The
deployed quantity exposes both. Misroute severity, selected-scope shift, and
fallback harm remain additional Task 14A/Task 19 metrics.

Classical reject-option and selective-prediction work (`Chow1957`, `Chow1970`,
`ElYanivWiener2010`, `GeifmanElYaniv2019`) motivates cost- or coverage-aware
selection. The present architecture differs by retaining overlapping licensed
sets and deriving the permission mask before learned selection.

If candidate and fallback share one scalar criterion, the status quo can induce
a contextual threshold. With required advantage `Delta`, candidate use is
supported only when an accepted comparison establishes

```math
J_q(e)+\Delta\le J_q(F_q),
```

equivalently `J_q(e)<=epsilon_F` for

```math
\epsilon_F=J_q(F_q)-\Delta.
```

This explains where an error threshold can come from operationally: it is the
largest loss that still beats the outside option by the required margin. It is
not forced by the original philosophical question alone, is not an amount of
falsity, and does not make the fallback safe. An externally fixed adequacy
tolerance and a fallback-improvement threshold remain distinct atoms unless a
declared policy identifies them.

A selective training objective such as

```math
\widehat R_{\mathrm{sel}}
+\lambda_\kappa(\kappa-\widehat{\operatorname{Coverage}})_+^2
```

may tune the learned reject/router threshold on validation data. It does not
replace `L_stat`, the evidence checker, or the exact active mask. The reference
experiment reports this objective as a router/threshold variant, not as the
logic's loss.

## 10. Score-as-content normalization and regularization

For an accepted adequacy atom, the named dual-use channel is

```math
z_a=\operatorname{ReLU}\left(\frac{m_a^{\mathrm{support}}}{\sigma_a}\right),
```

and is exposed downstream only when the exact symbolic atom state is
`Supported`. The complete record still retains signed support/refutation
margins, state, evidence handles, and normalization identity.

### Proposition 3 — unit covariance

Suppose every unit-bearing target, estimate, radius, tolerance, calibration
radius, and scale in one scalar schema is multiplied by `c>0`. Then the
standardized statistic loss, decoded state, and normalized surplus are
unchanged.

**Proof.** Every standardized quantity divides numerator and denominator by
the same factor. The interval relation is preserved by a positive order
isomorphism, and
`ReLU(cm/(c sigma))=ReLU(m/sigma)`. ∎

The implementation therefore trains normalized outputs, stores the inverse
unit transform, and applies weight decay or other norm regularization in those
normalized coordinates. A task-defined physical scale is preferable. If
models are compared by activation magnitude, their scales must have the same
registered semantics; separate per-model normalizations can otherwise reverse
comparisons.

Norm penalties, sparsity, nonnegativity, and stable calibration are engineering
constraints. None establishes that a hidden unit has the intended scientific
meaning. Semantic alignment remains a test involving channel identity,
held-out behavior, intervention/ablation, stability across seeds, and the
joint-consumer conditions of Task 17. Multiplying an arbitrary payload by `z_a`
defines a new computation plan; it is not licensed merely because `z_a` was.

## 11. Optimization protocol

The first implementation should follow this order:

1. Freeze generator/data version, external target constructors, atom schemas,
   split identifiers, profiles, units, candidate registry, and decoder.
2. Fit normalization constants on train only; version them.
3. Fit the statistic center (and compatible typed payload/grade heads), freeze
   the center mapping, then fit the radius with the interval term. The scalar
   `L_primary` records the component tradeoff for model selection; joint shared-
   trunk fine-tuning is a named ablation. Tune ordinary hyperparameters without
   inspecting the system-audit or final-confirmation roles.
4. Freeze the scorer. Compute calibration residuals and the finite
   `eta_cal` proposal on the calibration split.
5. Run the external calibration/checker procedure and record assumptions,
   mode, polarity, scope, versions, and provenance. Rejected/unbounded records
   remain open.
6. Decode all atom targets symbolically, derive profiles/public outcomes, and
   construct exact active masks.
7. Train or tune rejection thresholds and the router on their separate
   validation role, using active, resolved comparisons only. Freeze them.
8. Evaluate the learned arms and ablations on the lower-ranked system-audit
   role and construct system-level evidence under the separate Task 19 audit
   protocol. Do not reuse the system's own confidence as its certificate.
9. Evaluate the completely frozen system and its audit-derived status once on
   the untouched final-confirmation role. The five roles--train, envelope
   calibration, reject/router validation, system audit, and final
   confirmation--must be blocked by the independent units registered in Task
   19, not merely by row identifiers.

Joint end-to-end training is not forbidden forever, but it must preserve the
same data, gradient, and authorization boundaries. In particular, a router or
state auxiliary must not improve its own training objective by weakening the
exact grant condition.

## 12. Metrics, ablations, and falsifiable claims

### 12.1 Primary measurements

Report by atom schema, domain/cell, candidate, evidence mode, and shift regime:

- standardized statistic RMSE and signed boundary error;
- proposed and accepted interval coverage, width, and unbounded-rate;
- supported/open/refuted fidelity and false-support/false-refutation rates;
- public-outcome and query-quotient fidelity after exact aggregation;
- missingness, expiry, conflict, polarity, and learned-reject behavior;
- simultaneous-license and empty-active-set fidelity;
- tolerance-transfer fidelity without retraining;
- coverage, selective risk, deployed risk, fallback mass/loss, and misroute
  severity;
- inactive-selection rate, which must be exactly zero in the production path;
  and
- payload/grade error separately from certificate acceptance.

Calibration claims are reported only at their mode's scope. A nominal marginal
coverage result is not renamed conditional coverage, selected-subset risk,
worst-case safety, or target-world truth.

### 12.2 Required ablations

The experimental design should include:

1. independent three-way atom cross-entropy baseline;
2. center-only regression without a learned radius;
3. predicted radius without held-out expansion/checker acceptance;
4. direct aggregate public-status head;
5. self-confidence/self-validity treated incorrectly as a grant signal;
6. global plan softmax instead of independent atoms and exact empty-set logic;
7. joint router training without the exact mask;
8. zero-imputed missing targets;
9. unnormalized raw surplus channels; and
10. structured objective with and without the auxiliary atom-state head.

### 12.3 Pre-empirical claim dispositions

The following are testable hypotheses, not current verdicts:

- **H18.1:** under changed tolerances or certificate widths, structured
  statistic/region training will yield better status and boundary fidelity than
  the direct atom cross-entropy baseline at matched capacity/compute.
- **H18.2:** the registered held-out calibration procedure will meet its exact
  marginal coverage target on exchangeable test strata. Under preregistered
  shift stressors, coverage and width are reported without assuming a direction
  because the exchangeable-case guarantee no longer transfers automatically.
- **H18.3:** normalized named surplus channels will be more stable across unit
  rescalings and seeds than raw margins; this does not predict mechanistic
  monosemanticity.
- **H18.4:** separate masked router training will improve the risk--coverage
  tradeoff without nonzero inactive-selection errors; superiority over every
  joint alternative is not assumed.

If H18.1 is falsified in a sufficiently powered matched experiment, the
project's core logic, external certificate boundary, and ReLU representation
theorems survive. The practical case for region regression as the default
would weaken; a scoped direct classifier could become the implementation
default for frozen tolerances while quantitative prediction remains necessary
where tolerance transfer, risk reporting, or calibration-region inspection is
required.

## 13. Executable witnesses

[`verification/losses.py`](../verification/losses.py) and
[`verification/test_losses.py`](../verification/test_losses.py) implement the
small mathematical contract without a neural library. They verify:

- central interval-score behavior;
- explicit missing-target masking and schema-balanced aggregation;
- objective covariance under a positive unit change;
- finite calibration quantiles, including the infinity sentinel;
- inclusive support, strict refutation, one-way evidence validity, and symbolic
  public outcomes;
- independent atom cross-entropy and asymmetric reject loss;
- exact-active/resolved pair masking in router ranking;
- joint selective risk, coverage, and fallback-inclusive deployed risk;
- scale-covariant, symbolically gated dual-use surplus; and
- primitive train/calibration/test ID-overlap rejection (Task 19A must extend
  this to the frozen five-role, group-blocked manifest).

These are regression witnesses, not a proof assistant, trainer, empirical
result, or accepted certificate.

## 14. Literature and project boundary

The chosen objective uses established components but a project-specific
separation:

- proper scoring and interval-score literature motivates honest prediction of
  the declared statistic/interval target;
- conformal prediction supplies one mode-relative held-out coverage procedure;
- conformal risk control is a possible direct bounded-risk mode under its own
  monotonicity and sampling assumptions;
- reject-option/selective-prediction work motivates joint risk--coverage and
  fallback-cost accounting; and
- pairwise ranking supplies an ordinary post-license selector objective.

None of those literatures supplies the project's exact address-indexed
diagnostics, `WF + K_3`, profile-indexed license, open-library semantics,
proof-carrying-plan distinction, or external active mask. Conversely, this
document does not claim a new theorem about the optimality of interval scores,
conformal methods, cross-entropy, or pairwise logistic ranking.

## Task conclusion

The selected learning contract is deliberately quantitative before it is
logical:

```text
external atom-statistic targets
    -> structured center/radius training
    -> held-out calibration proposal
    -> accepted mode-specific envelope
    -> exact evidence/polarity-aware K_3 atoms
    -> exact profile/public outcome and active mask
    -> separate learned selection or explicit fallback.
```

This choice preserves a conditional form of the project's original intuition
without turning a ReLU value into a truth degree or grant. An arbitrary positive
activation means only positive preactivation; a named point margin means
predicted slack. A normalized positive activation can carry strict
certificate-relative surplus for one atom and feed a later computation only
after the accepted envelope and symbolic state establish what that number
means. The full profile and mask still authorize use. Cross-entropy remains a fair
simple baseline; learned validity may only withhold; selective risk is reported
with coverage and fallback harm; and no optimization loss certifies itself.
