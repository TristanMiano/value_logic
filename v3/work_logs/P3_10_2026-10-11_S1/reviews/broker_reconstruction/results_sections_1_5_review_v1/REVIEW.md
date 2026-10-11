# Review of results.md sections 1–5

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, agent **`/root/freeze_review`**. Task: **P3-10**. Principal Research90 time added: **0 minutes**.

## Disposition

**PASS for numerical reconciliation, with two concrete exposition corrections and one terminology clarification.** The saved prose/table checker compared **189 displayed values, counts, classifications, and supplemental-result fields**, with **zero numerical mismatches**. Manual review covers the remaining inline fractions, first-key and transfer values, mathematical identities, interpretation boundaries, and cross-arm summary claims. No scientific stage, paid method, principal observer, or independent observer was run again. `results.md` was not edited.

Reviewed snapshot: `sections_1_5.observed.md`, observed **2026-10-11T16:00:34.400000+00:00**, SHA-256 **`9f81d6b84a7c7c4c3ece203d29129b44db34666c8c23447a4aed0b9fee66a839`**. At that observation the document ended with section 5.3, so the saved whole-file and sections-1–5 hashes coincide. Later draft sections and subsequent principal edits are outside this version's snapshot. The companion attestation binds every source consulted.

## Concrete corrections

### C1 — section 5.2: the displayed gaps are already divided by H

The sentence reporting that the new deterministic width is wider by “0.00136358/H” for F/V and “0.04004628/H” for Z appends a second division to already normalized values. The saved source field is `means_per_scheduled_horizon.frozen_width_minus_end_key_width`. For live uniform gate the exact **new minus delivered normalized width** is:

| Quantity | Exact difference after division by H | Decimal |
| --- | --- | --- |
| F and V | 562227883/412316860416 | 0.0013635820820733595 |
| Z | 1375979821/34359738368 | 0.04004628342227079 |

**Suggested replacement:** “For the live uniform gate path, after dividing widths by H, the new deterministic width is wider than the frozen delivered width by about 0.00136358 for F/V and 0.04004628 for Z.”

The underlying arithmetic, sign, and adverse interpretation are correct. Only the unit notation needs correction. The literal `/H` reading would divide by the gate horizon 128 a second time. No result or observer change is needed.

### C2 — section 4.3: state the subtraction direction explicitly

“Its difference from each candidate is a positive intercept” makes “its” refer to the ordinary witness and can read as ordinary-minus-candidate. The positive coefficients are **candidate minus ordinary**. The following paragraph gets this right; the opening explanation should use the same orientation.

**Suggested replacement:** “Each candidate's objective minus that witness's objective has a positive intercept and a positive slope in lambda.”

All twelve saved intercepts and slopes are positive, so the claimed strict candidate inferiority for every nonnegative price is correct. No numerical correction is required.

### C3 — section 3.3: separate the two meanings of variance

Immediately after section 3.2 uses the within-slice temporal variance `Var(p)`, section 3.3 calls the `p(1-p)` term a “forecast-variance difference.” This risks identifying two different quantities.

**Suggested clarification:** “Here p(1−p) is a Bernoulli-parameter variance term, distinct from the within-slice temporal variance of forecasts used in section 3.2.”

The identity and the pointwise-versus-averaged sign explanation are correct. The clarification is terminology only, consistent with the independent mechanism review.

## Checks that passed

| Section | Checked content and result |
| --- | --- |
| 1 | Original 336 broker + 104 certificate seals, 440 reused records, 60 amended conformance records, 500 scores, and preserved incomplete unamended lineage are accurately described. The unknown original prefix is not converted to zero or used as the sole reason for negative comparisons. A0–A5 dispositions match the exact reconstruction. B0–B2/C0 headline counts and qualifications agree with the signed certificate and conformance reviews; this review does not independently rerun their semantic reconstruction. |
| 2 | 12 groups/500 public units; six broker populations; 336 episodes/28,160 positions; 18 mirrors/1,536 positions; 126 numerical paths/10,752 positions/2,688 blocks all agree. The prescribed mean hierarchy, deterministic analytic weight, 0.01 and 5% conventions, common-stakes comparison, native-price distinction, and non-IID limitations are correct. Certificate and conformance roster/count summaries agree with their arm reviews and protocol. |
| 3.1 | All six rounded equal/base/A2 rows and practical decisions match exact fractions. Three of six distinct selector/family means pass, or six of twelve explicitly duplicated cold/cached candidate cells. All six inline first-key effects and the 8,946 numerical first-key positions agree. The first-key count is correctly not presented as distinct mathematics. Constant-half and stronger-expert cautions are sound. |
| 3.2 | Prefix/suffix A2 values, 31/64 truth fraction in each gate suffix, the three signed uniform moment contributions, mean forecasts 0.73748418/0.61910605, suffix Brier means, and approximately 0.727 incoming weight on three constant-one advice coordinates agree with the saved moment result and independent transfer review. The moment identity uses finite-slice moments before hierarchy, and the text correctly rejects causal acquisition attribution and counterfactual policy claims. |
| 3.3 | The binary Brier identity, same pointwise signs/different possible averaged signs, final projection bound 5/196608, residual lower bound 49027/4915200, and exclusion of accumulated weight rounding are correct. Numeric/independent mechanism records confirm 526 changed forecasts, 162 changed prospective actions, and 98 terminal corrections. Current receipt timing is distinguished from prior hardening and immutable forecasts. |
| 4.1–4.2 | Every exact/rounded action improvement and threshold decision matches. Common-stakes effects 19/384, −37/1152, 1/128, and −13/1152 are correct. All six per-request cold/cached bills and ratios agree; all 36 paired cached bills are larger. Zero-price cold/cache ties and all-price mirror ties are correctly qualified. |
| 4.3 | All three ordinary W and cold/T witnesses match. The 12 positive coefficient pairs and 12 empty weak/strict/practical regions are confirmed by the saved independent tables and supplemental continuous result. No witness tie at zero, the subthreshold 7/768 gate-uniform action gap, five native/fixed catalogue differences, and the inferior Brier of all selected ordinary witnesses are stated correctly. The source excludes an equal-report-service claim and retains the end-to-end economic gate. C2 clarifies the first subtraction direction. |
| 5.1 | All report table values, 126/21/63 denominators, four practical Z cells with identity duplication, 118/8/2 F/V and 95/31/25 Z individual counts, and 65,407,686 total fee with its three family totals agree. Successful delivery is not substituted for useful narrowing or confidence coverage. F, V, Z remain distinct targets; V's expected-action interpretation remains conditional. |
| 5.2 | The affine unknown-key construction is a sharp marginal bound over the relaxed one-bit-per-key cube, not over all realizable CNF worlds. Nonnegative later-receipt/cancellation gains against the deterministic envelope and possible deterioration versus the delivered sampling interval are correctly distinguished. Saved source and public/private timestamps preserve the bounds-before-truth-validation order; investigator exposure and exploratory/unbilled status remain explicit. C1 corrects only the displayed normalization. |
| 5.3 | The public F−V identity follows directly from selected labels and cancellation of the shared unselected affine coefficients. The binary-image convex hull is exactly the translated Minkowski sum of segments. Saved geometry confirms all 126 dimensions equal two, four incompatible marginal corners in every region, 126 successful containment checks, and every displayed area ratio. The ratios use per-report areas followed by the fixed hierarchy. Relaxed worlds, convex mixtures, non-probability interpretation, and conditional sampling-intersection limits are correctly retained. |

The section 5.3 identity and geometry are understood within its **126 complete reporting episodes**. If the phrase “each complete saved episode” is later reused outside this reporting context, make that denominator explicit rather than extending V or the optional-report geometry to the 210 ordinary executions without this report interface.

## Frozen and supplemental boundaries

The primary A0–A5 values remain the frozen endpoints. The moment, final-quantization/mechanism, continuous fixed-record price, retrospective bound, and joint-geometry constructions are separate explanatory analyses over saved paths. The prose does not replace the original scores, rerun a native-price controller, claim free paid reports, infer fair bits from MT paths, or turn observed containment into a confidence-coverage estimate. The ongoing status at the document's start avoids claiming that Research90 or publication has already closed.

The strongest-ordinary statements are properly restricted to the terminal scalar objective and the declared finite catalogue. They do not become forecast domination, universal algorithmic impossibility, same-report-service superiority, or physical-runtime claims. The unknown original public prefix continues to block end-to-end positive economics even where completed-path inequalities are known. No P3-11 contribution or author gate is started by this review.

**Signed: ChatGPT (GPT-6 Astra Pro), `/root/freeze_review`.** Exact signing UTC and source/output hashes are recorded in `review_signature.json`. The two requested prose corrections and the variance clarification require no scientific rerun.
