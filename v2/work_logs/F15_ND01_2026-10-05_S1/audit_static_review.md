# F15-ND01 independent execution and interpretation review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, `nd01_protocol_audit` sub-agent.
The principal agent owns the research clock. This parallel review adds **zero**
additional credited engaged minutes.

## Baseline integrity

[The independently measured baseline](audit_baseline.json) verifies all 34
frozen files against F14-v1 and the supplied manifest SHA256
`b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c`.
The source revision is `9f42a047126618b0364cf334002f846e5839d726`.
The existing ledger contains 949 data rows and 217,776 bytes, with SHA256
`44c93cc930fdea2d588f663688e71615a84b32f98517eadd4bab3943efa154bd`.
POST-B-1 therefore starts this recurrence at 701.64299296445 engaged minutes,
with 258.35700703555 remaining to the 960-minute checkpoint.

The fresh forecast records a protected **D+L+E90**, central D10/L10/E70/O10
(100 engaged), high D15/L15/E90/O15 (135 engaged), and waits separately.
F15's original E60 is already complete and is not reused as recurrence time.
F16 and Gates C/D remain outside this authorized diagnostic chunk.

## Constructed complete-endpoint calibration: static review

Reviewed the draft `calibration_endpoint.py` and accompanying design against
the unchanged `neural.py`, `calibration.py`, `analysis.py` and F14 protocol.
No preparation or evaluation was run by this reviewer.

The calibration uses the actual frozen search, evaluator and assessment. All
five declared evaluation seeds, all original counts, all four hypotheses and
five search/control types are checked. The statistical assessment retains the
complete **560-row** family. `development=True` prevents a new pilot-support
claim; the separately named diagnostic field describes only endpoint behavior
on the five constructed layouts.

The five networks are positive rescalings/permutations of one compiled
function. They are explicitly **not independent ordinary-training replicates**.
The untrained controls come from the frozen initializer, without invented
training steps. The custom validator checks this provenance honestly; it does
not pretend that the ordinary-training validator accepted zero training.

Known subsets do not enter candidate search. Oracle accuracy is reported
separately on hash-identical regenerated evaluation arrays, with that repeated
computation charged separately. The known-subset oracle does not inherit
searched control advantages or receive a complete-endpoint classification.

**Component assessment:** no static blocker found. The root runner must still
establish global readiness: save, hash, reload and validate all five models and
all their selected alignments before writing an exclusive exposure marker and
generating any evaluation population. A one-model helper cannot establish that
cross-model ordering obligation by itself.

## Interpretation boundary

Successful task learning constrains the total output function. The tested
intervention requires the stronger property that a binary eight-coordinate
subset of fixed contributions `v_i h_i` approximately implements a signed
log-cost replacement. An arbitrary observational decoder can use different
coefficients and therefore does not establish this property.

Mixed or non-coordinate-aligned features are a plausible explanation of a
negative coordinate search. These experiments do not, by themselves,
diagnose superposition in the particular trained networks. Likewise, optimized
random/permuted searches can recover useful structure; failure to beat them by
a prescribed margin is distinct from failure of absolute intervention accuracy.

## Fixed-model search: static review

The stable draft contains **five** proposal families: cost correlation,
uniform proposals, permuted-cost correlation, log-cost correlation, and
positive output-contribution covariance. The last family is a substantively
head-aware proposal: absolute correlation with a nonzero output-scaled hidden
unit would cancel that weight's magnitude and sign. Its nonnegative covariance
weights, 25% uniform mixture, and all-zero fallback are explicit.

Each family/role produces one 1,024-candidate pool. The 128-candidate comparison
is its literal prefix; duplicates consume budget. Both selectors share scored
discovery rows and pools. Frozen-MSE selection invokes the existing rule;
robust selection minimizes the maximum of five normalized stratum MAEs and
the normalized near/far disagreements, then MSE and equal-target effect RMS
with the same numerical tie band. Both ordinary controls receive each budget
and selector. Actual reused work and counterfactual unshared logical work are
reported separately.

The original five model weights are loaded with source/config/artifact hashes,
without training. New discovery and validation seeds are distinct from the
original F14/F15 streams. Validation uses the same fresh rows for every
prespecified method and reports all methods; it neither selects a new subset
nor fits a decoder. Paired improvements retain their sign convention and
equal-stratum sufficient moments. The threshold summaries are explicitly
point-estimate diagnostics, not confidence-qualified F15 support.

**Component assessment:** no substantive statistical or comparison blocker
found. The global runner must bind the effective five-family configuration,
all five source models and durable selections before validation exposure.

The first independent syntax check found a missing closing bracket in the
draft's seed list. The owning implementation agent fixed it before any
scientific run. The corrected calibration, search and independent-auditor
files parse successfully. This pre-execution drafting failure and correction
are preserved in [audit_failures.jsonl](audit_failures.jsonl) and
[audit_syntax_check.json](audit_syntax_check.json).

## Remaining review before full run readiness

- Root protocol/configuration, stage orchestration, bounded failure/retry
  contract, preservation of completed units, and global exposure gate.
- Any optional relaxation's scope and interpretation before its execution.
- After execution: a minimal independent saved-statistics reconstruction,
  source-freeze preservation, and append-only ledger/clock arithmetic.

This was the partial static-review record. The subsequent
[final readiness audit](audit_readiness.md) completed runner, binary-extension
and frozen-dependency verification before any study population was generated.
Post-execution statistical and accounting checks remain separate obligations.
