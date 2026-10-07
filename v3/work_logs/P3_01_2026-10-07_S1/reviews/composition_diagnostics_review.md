# P3-01 composition diagnostics: bounded reconstruction review

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal review, not external validation.
Resource time is unmeasured and contributes no principal-clock credit.
Scope: `v3/foundations/01_composition_boundaries.md`, chiefly CB01–03.
No canonical edits, duplicate test suite, new experiment or gate decision.

## Finding

The three finite/arithmetic arguments are correct at their stated scope. The
most useful strengthening is to make CB03's simultaneous and selection scope
explicit. CB01's replay accounting and CB02's stakes recoding also admit short
clarifications that prevent plausible misreadings. None requires a new learner,
an experiment or a downstream proof task.

## Primary source boundary

Reopened Zhao et al., [Calibrating Predictions to Decisions: A Novel Approach
to Multi-Class Calibration](https://proceedings.neurips.cc/paper_files/paper/2021/file/bbc92a647199b832ec90d7cf57074e9e-Paper.pdf),
NeurIPS 2021, the inherited R6 and planned S19 comparator.

Sections 2.2–2.3 fix losses on label/action pairs and decision functions of
the probability report. Definition 1 gives the Bayes rule; Definition 2
compares simulated and actual population losses; Definition 3 restricts the
action count; Definition 4 normalizes approximate discrepancy by loss magnitude.
The caution after Definition 2 and Proposition 1 delimit individual-input
and competing-rule claims. The paragraph after Theorem 2 explicitly recognizes
calibrated constant predictors. Sections 4.2–4.4 separate sample control from
inner optimization and introduce a computational relaxation.

These are inspected source definitions and stated boundaries. No statistical,
optimization or finite logical-learning theorem is imported into the diagnostics.

## CB01: charges and policy comparison

The expected-cost reconstruction is direct:

| Policy and information contract | Acquisition | Expected guessing loss | Total |
|---|---:|---:|---:|
| A buys its reveal | 1 | 0 | 1 |
| B receives no reveal and guesses zero | 0 | 10/2 | 5 |
| B is additionally handed A's answer without a charge | 0 | 0 | 0 |

The third row has different observations from the second; it is not evidence
that the second policy is better. An ordinary controller with the stipulated
law also buys. The diagnostic assumes the reveal is feasible before the decision
deadline and treats other overhead as common/omitted under its toy cost model;
it makes no wall-clock or proof-hardness claim.

**Clarification recommended:** in replay, either charge the same historical
information cost to both modules or exclude acquisition from both sides and
label the objective conditional on the supplied history. Do not preserve A's
acquisition bill while supplying its result to B free and present that as a
full-policy comparison. Conversely, do not claim B actually selected an
acquisition merely because a replay attaches a common input cost. The canonical
wording is consistent with this, but “charge common information as a common
input” could state the two permitted accounting conventions explicitly.

## CB02: exact calibration and the stakes boundary

### Elementary reconstruction of the constant-report case

Fix a deterministic consumer and put `a0 = delta(1/2)`. For any fixed finite
loss table, both simulated and actual loss equal

`(ell(0,a0) + ell(1,a0))/2`.

This follows because the actual answer marginal and the report's simulated
answer distribution are both fair. Indeed `E[Y | p]=1/2`: the fixture is
distribution calibrated as well as decision calibrated for the indicated
consumers. That does not make `p` equal to `E[Y | X]`, which is `X` here.
An independent randomized mixture of these constant consumers preserves the
equality, provided the expectations exist. A tie-break or random seed that
conveys the missing feature is outside that report-only consumer contract.

The zero-one losses `1/2` and `0` are therefore correct. The feature-using
rule belongs to the stronger information contract. The result is an elementary
specialization of the inspected definition, consistent with the source's own
constant-predictor discussion, not a newly discovered failure of decision
calibration. The distinction is already made accurately in the draft.

### Why the stakes calculation is valid despite `Y=X`

For the *specified feature-dependent simulated loss*, the averages are
`E[kappa(X)p]=5/2` and `E[kappa(X)Y]=9/2`, so the discrepancy is two.
The displayed arithmetic is correct. A constant guessing action isolates
the altered loss contract; feature-dependent action selection is unnecessary
to create this discrepancy.

There is one subtle recoding objection worth heading off. Because `Y=X`,
`kappa(X)Y` equals `9Y` **on the actual population support**. But replacing
the loss by the fixed table `ell'(Y,0)=9Y` changes its evaluation for simulated
labels. In particular, the simulated pair `(X=0, Yhat=1)` has loss one under
`kappa(X)Yhat` and nine under `9Yhat`. The fixed table therefore predicts
`9/2` and agrees with its actual average. It has no calibration violation.

Thus equality of two losses on observed support does not license interchanging
their simulated-loss extensions. The example correctly identifies an additional
conditioning/weighting requirement; it does not refute the fixed-loss result.
Making this explicit would strengthen the draft. Stakes one and nine also
identify the feature, so any consumer allowed those stakes has more information
than the earlier consumer receiving only `p`.

## CB03: signed error bridge and its quantifiers

The identity

`L(A)-L(B) = [L(A)-Lhat(A)] + [Lhat(A)-Lhat(B)] + [Lhat(B)-L(B)]`

gives the stated upper bound by bounding the first and last terms by
`epsilon_A` and `epsilon_B`. No probabilistic independence is needed. The
order certificate alone yields at most the error-sum regret bound; to warrant
`L(A)<=L(B)` the estimated margin must cover that sum. The draft's requirement
that the full right-hand side be nonpositive correctly captures this.

**Clarification recommended:** replace or qualify “independently justified”
with “separately justified and jointly applicable to the compared pair.” If
the two error events have probabilities at least `1-delta_A` and
`1-delta_B`, the joint comparison is valid with probability at least
`1-delta_A-delta_B` by the union bound; independence is unnecessary. If A or B
was selected after examining noisy estimates, pointwise bounds for each fixed
candidate need not apply to that selected pair. Require a uniform event or an
appropriate selection-valid bound.

Population-average error premises yield a correspondingly averaged inequality;
they do not warrant a realized pointwise comparison. The population, program,
source, versions and units must coincide across the estimates, targets and
bounds. The current warning about retaining quantifiers is correct; the added
joint/selection sentence would close the principal concrete risk identified here.

## Evidential classification

| Item | Status established by this review |
|---|---|
| CB01 costs and information distinction | Elementary finite metalevel reconstruction under supplied law/access/cost assumptions |
| CB02 two-case losses and constant-report equality | Elementary reconstruction mapped to the inspected decision-calibration definition |
| Zhao definitions, consumer restrictions and search boundary | Primary source interface imported with its stated scope; no theorem implementation or proof audit |
| CB03 signed-error inequality and event accounting | Elementary algebra and ordinary union-bound reasoning, not a new uncertainty theorem |
| CB04 step-preserving translation | Read as a conditional finite-history simulation argument, not an implemented compiler or exhaustive equivalence test |

The earlier eleven-group `finite_checks_1.json` run does not validate these
new diagnostics. This review uses direct reconstruction and source inspection;
it did not rerun that suite or add its assertion count to the evidence here.
No contribution-support or task-completion disposition changes.
