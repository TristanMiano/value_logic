# Selective-feedback §§8–9: semantic boundary review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Review: separate same-model, nonblind semantic assignment; **zero principal
clock credit**. No experiment, source survey, rate-proof rerun, implementation,
plan or ledger change was performed.

**Disposition: PASS at the stated semantic scope.** The final inspected
sections distinguish fallible forecasts from coherent truth laws, expected
loss from pathwise caps, and the standalone learner from the larger hard-state
interface. The three wording qualifications raised during review are now
present: prospective-only forecast override, conversion of resource units
through prices, and source-relative probability nonidentification.

The governing duties are [U04, V01 and V04](../../../../foundations/01_desiderata.md).
The earlier probability-information contract is
[P3-02 §§1–3](../../../../derivations/02_probability_information.md): supplied
laws, known loss semantics and admissible-source fibers must be distinguished
from fallible estimates, realized scores and source-independent impossibility
claims. This review does not change the historical P3-B duty overlay.

## 1. Source-known comparator bound and admission costs

The library's constant-zero and constant-one experts have losses summing to
T on every binary tape. Therefore `L_*<=T/2` is a structural upper bound
available without private evaluation. It does not identify which expert is
better, imply truth probability one-half, or establish a calibrated forecast.
Substituting an evaluator's smaller realized comparator loss into a retrospective
analysis remains distinct from a live admission certificate. Section 8 says
so explicitly.

For V04, the section now writes the cap in common units: `cG+lambda C_funded`
for a common primitive price, or `cG+max_j(lambda_j) C_funded` as a safe bound
under arbitrary nonnegative category prices. A priced categorywise envelope
may be tighter. Raw operation units are not added to task-loss units.
The pathwise task cap uses `c(T−m)`, while `cG` is an expectation bound.
Thus a hard resource guarantee is not misrepresented as a pathwise task-loss
guarantee, and the private complete invoice table is not a free deployed input.

## 2. Hard-information override and U04

Section 8.2 explicitly states that the cache-free standalone learner is **not
a complete implementation of U04**. This is the correct boundary. Its update
of fallible expert weights is not the hard truth-coordinate update required
after a sound, version-matched answer is admitted by the larger reasoner.

The composition claim is suitably restricted: keep the purchase/update process
and raw forecasts unchanged; a paid sound mechanism may override an action
with the correct answer. A 0/1 forecast override uses an answer already
available **before that forecast is issued**. Earlier issued forecasts remain
immutable and retain their original scores. Pointwise loss improvement does
not erase the additional mechanism's invoice.

The section also prohibits silently skipping or reallocating purchases,
changing weights, or changing the objective/tape under the same proof.
Complete U04 integration still needs the received-answer coordinate and the
dependent-record recomputation/staleness rules, including current version
binding. The output-dominance observation does not implement those rules by
itself. That remaining integration is correctly identified as P3-08 work.

## 3. Fixed precision is an algorithm boundary, not a truth-law theorem

Section 9.1's repeated-true-query construction concerns the positive-weight,
downward-rounded randomized action policy. Its retained wrong-expert mass and
finite action grid impose the stated expected-error floor on unbought actions.
It does not assert that a known true proposition remains uncertain in a
sound hard-information state, or that every finite-state reasoner must make
that error. The text explicitly permits precision changes or the sound
known-answer override to change the conclusion.

The implementation's finite admitted horizon remains separate from the
hypothetical family of longer horizons used to explain an asymptotic failure.
Likewise, fixed weight-state size does not imply constant total memory:
request, random-bit and emitted-record storage remain horizon-dependent.
These distinctions satisfy V01/V04 without transferring a rate or memory
claim to a different algorithm.

## 4. Action-lottery value and source-relative identification

Section 9.2 supplies a coherent subjective law as an **additional premise**;
it does not infer one from the learner's action probability. With the lottery,
correction and cost terms held in the same information context, the relevant
scalar has the form

```math
v=b+c(1-\pi)q+c(1-\pi)(1-2q)p,
```

where `b` is a known additional expected resource cost. The coefficient of
`p` is nonzero exactly when that scalar separates arbitrary distinct admitted
probabilities. At zero coefficient, any two distinct admitted `p` values
collide. If hard evidence already restricts the source to one `p`, it still
identifies that value; the constant lottery value supplies no additional
identification. The final section now includes this source qualification,
matching P3-02's fiber principle.

Unknown or outcome-dependent costs cannot simply be subtracted as a known
`b`, and a realized all-in bill is not this expectation. Independence and the
specified payoff model remain premises. The section correctly distinguishes
action probability, issued Brier score, regret envelope and checked answer.
There is no accidental claim that a fallible `q` is a coherent joint law over
mathematical truths.

## 5. Signed prices do not give coordinatewise dominance

The [saved price audit](../../development/price_and_precision_audit.json),
`reference.derived_v1_2_delta`, uses the sign convention **learner minus
table**. Its cache coordinate is `−11408`, although its total resource
difference is positive. The saved separator assigns cache price one and all
other prices, including terminal-error price, zero; the resulting difference
is `−11408`. Some B=16 rows additionally have negative solve coordinates.

Accordingly, arbitrary nonnegative category-price dominance is false.
For the reference fixed traces, the correct priced comparison is
`1702c+sum_j lambda_j Delta_j`; new prices require that signed product.
The main note's cost discussion explicitly confines its universal deployment
obstruction to a **common nonnegative primitive-unit price** with nonnegative
terminal-error price. This is consistent with the audit and V04.

The separator is a scope check, not a favorable new application or a claim
that the learner beats all ordinary controls. Repricing these fixed traces
also does not simulate a changed price-dependent acquisition policy. No
hardware-price or new-run conclusion is imported from the category vectors.

## 6. Bound inspected sources

The reviewed main sections run from the `## 8.` heading up to, excluding,
`## 10.`. Their UTF-8 content is **9,671 bytes**, SHA-256
`79bd67efb5e79c2f882fe4981c6287fa8ab881f727368fc0a83aac85bfbd8072`.
This sectional binding remains meaningful if unrelated later sections change.

| Inspected input | SHA-256 |
| --- | --- |
| `v3/derivations/07_selective_feedback.md`, full file at final semantic read | `c62cc840cf35af4419a64234ab49c5ed651400b1bd7f1023003fa77cb1b5e401` |
| `development/price_and_precision_audit.json` | `f5efd46fd83cbf0a416a451d1c3aadfecb58dc81b758f35abd6b8c0c2cdf9b97` |
| `v3/foundations/01_desiderata.md` | `0c1b250e1e22640c1a965015e009ed18a2661415af83f5086b893f0182376774` |
| `v3/derivations/02_probability_information.md` | `faee4cd48d6f9477933e08af371ff95718f1468389ee11f61c38ffde0fd6f3af` |
| `v3/checkpoints/B_1.v1.json`, historical scope only | `f91918d661b0ae74068b46d2103822adfe9a5d507666885571e94c2a89ea2a8f` |

The `development/` path is relative to
`v3/work_logs/R_P3_B_A_2026-10-09_S1/`. The rate proof and any exact
binary-potential refinement remain owned by their separate mathematical review.
