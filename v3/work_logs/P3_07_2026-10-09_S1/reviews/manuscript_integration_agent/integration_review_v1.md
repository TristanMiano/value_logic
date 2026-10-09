# P3-07 manuscript integration review v1

## Disposition and scope

**The reviewed integration is mathematically and numerically consistent with its retained evidence, subject to the two narrow qualifications below.** The first is an accounting label and its resulting rounding; the second makes the validity conditions of a general, unimplemented credal-set extension explicit. Neither finding changes the implemented coordinate-interval certificates, the analytic profile, or the reported ordering against the direct exact-answer control.

This is a **same-model, targeted, nonblind development review**. Reviewer time is unmeasured and contributes **zero principal Research90 credit**. No next phase or gate was started. The reviewer made no changes to root source code, derivations, clocks, plans, ledger, or prior evidence. This review used the frozen manuscripts, retained exact results, and the earlier independent source/reconstruction reviews identified below; it did not run a new broad test suite or any solver population. The additional acquisition-planning study mentioned by the root is outside this review.

The following exact manuscripts were copied before review and remained byte-identical to the root manuscripts at finalization:

| Manuscript | SHA-256 | Reviewed snapshot |
|---|---|---|
| `v3/derivations/07_paid_reasoning.md` | `ba5faf34e10b2030290135296b2d705ee75e7d25884ed07caa655b316b2bb1bd` | [Main snapshot](07_paid_reasoning_reviewed.md) |
| `v3/derivations/07_ordinary_analytic_profile.md` | `46db6cb249c5e0bb0066685c438132a1bfcf7551d834612cc752a8239e90cfb7` | [Analytic snapshot](07_ordinary_analytic_profile_reviewed.md) |

This report releases the manuscript freeze for the root to incorporate the two findings. Any later changed bytes are outside these exact snapshot hashes. The current “research in progress” status is intentional and was not treated as a defect.

## Finding 1: label or include the multi-action setup fee

Main §6.6 calls the three actual controller costs “all-in” and prints approximately 640.419, 638.761, and 642.014. These values agree with the retained results' `all_in_cost_excluding_one_time_setup` fields. Each result also records a separate `initial_setup_fee = 2/3125 = 0.00064`.

Either label the printed values explicitly as excluding the one-time setup fee, or add that fee before describing them as all-in:

| Retained case | Deployment cost excluding setup | Cost including setup | Including setup, three decimals |
|---|---:|---:|---:|
| `full_root_eight_bits` | 32020931/50000 | 32020963/50000 | 640.419 |
| `capped_root_eight_bits` | 15969017/25000 | 15969033/25000 | 638.761 |
| `full_root_one_bit` | 32100707/50000 | 32100739/50000 | **642.015** |

Evidence: the three `*_result.json` files in [multi_action_run_v2](../../development/multi_action_run_v2), whose hashes and exact reconstruction are preserved in [integration_check_results.json](integration_check_results.json). This is a small label/transcription correction. The direct exact-answer control's cost of 368 is still lower in all three cases, and the manuscript's explanation of the mandatory exact-feedback bill remains supported. The multi-action companion contains related wording, but that companion was not one of the two frozen manuscripts assigned here.

## Finding 2: state the credal-set validity and evaluation requirements

The general extension in main §2 should explicitly require a **nonempty joint-law family containing the target law on the stated validity event**. Its present wording says that the joint credal set and its soundness are assumptions until an evidence contract is supplied, but it does not spell out the nonemptiness or computational bound direction. The root independently requested that the earlier proof-review qualification be made explicit here; this reviewer checked the mathematics below.

Let $`\mathcal K`$ be the supplied family and $`Q`$ the target joint law. On the stated event, require $`Q\in\mathcal K`$ and $`\mathcal K\ne\varnothing`$. For complete-policy improvement $`G`$,

```math
\mathbb E_Q G\ \ge\ \inf_{P\in\mathcal K}\mathbb E_P G.
```

An empty or inconsistent family must return an invalid/conflict state; the extended-real convention $`\inf\varnothing=+\infty`$ must not become an improvement certificate. A capped evaluator must produce a sound **lower bound** on this infimum. Evaluating a feasible member of $`\mathcal K`$ instead gives an **upper bound** on the infimum, which is insufficient for safe adoption. For example, a family with attainable improvements $`-1`$ and $`2`$ cannot be certified beneficial merely by finding the feasible model with improvement $`2`$.

These requirements are for the general credal-set extension. They do not reveal a numerical defect in the implemented simultaneous coordinate-box procedure. No generic credal-set optimizer was validated by this review.

## Mathematical integration checks

The signed linear certificate correctly uses the lower coordinate endpoint for a nonnegative coefficient and the upper endpoint for a negative coefficient. Its selection guarantee follows on one simultaneous coverage event; choosing prices or catalogue comparisons after that event is observed does not require independence between coordinates. The manuscript correctly separates a continuation comparison after acquisition has become sunk from an all-in decision that subtracts the acquisition bill. The fixed-checkpoint development protocol and fresh future-cohort conditions are stated at the relevant claims.

Main §3.3 is byte-identical to the previously reviewed section. A fixed bounded context basis must be multiplied by the raw paired features before profiling. Signed linear combinations of those product features then cover the represented query-dependent prices. The total-variation extension uses a population-law bound $`\mathrm{TV}(\nu,\mu)\le\rho`$, with the event-supremum convention, so the expectation penalty is $`\rho`$ times the feature range, without an extra factor of two. The range must be valid on both laws' supports. A separately probabilistic transfer guarantee needs its own failure probability accounted for. This does not supply empirical drift detection or coverage for an unrestricted context-dependent price function. See [whole-audit review v2](../whole_audit_agent/review_v2.md).

The acquisition-identification section correctly restricts its exact sample-size conclusion to the stated fixed-size, two-sided minimax accuracy duty. It does not promote that calculation to a lower bound for arbitrary sequential, abstaining, or differently tasked learners. The perfect diagnostic is a separate experiment with its own prior threshold. The Brier-score witness and asymmetric task-loss comparison are arithmetically consistent with their stated losses.

The whole-procedure audit treats each entire profile-and-deploy episode as the sampled bounded outcome. Internal interval failures are therefore included in that episode distribution; an additional union bound over internal certificates is not needed to certify the outer expected outcome unless simultaneous internal correctness is separately claimed. The manuscript's separation of the controller episode bill from the outer certification bill is appropriate.

## Analytic class-count and resource-path checks

The analytic companion's finite-field proof is valid. Multiplication by a nonzero residue permutes the nonzero elements, giving Fermat's identity after cancelling their product. With $`n=(p-1)/2`$, every nonzero residue is a root of exactly one of $`x^n-1`$ and $`x^n+1`$. Each degree-$`n`$ polynomial has at most $`n`$ roots, and their disjoint root sets cover $`2n`$ elements, so each has exactly $`n`$ roots.

Removing $`a=1`$ and $`a=-1`$ leaves ordinary-class counts

```math
N_+=n-1-\mathbf 1_{n\text{ even}},\qquad
N_-=n-\mathbf 1_{n\text{ odd}}.
```

Their sum is $`2n-2=p-3`$. The final manuscript table uses these correct formulas, including the sometimes easy-to-miss negative count for odd $`n`$:

| Prime | Ordinary class size | Positive | Negative |
|---:|---:|---:|---:|
| 17 | 14 | 6 | 8 |
| 31 | 28 | 14 | 14 |
| 47 | 44 | 22 | 22 |
| 61 | 58 | 28 | 30 |
| 97 | 94 | 46 | 48 |

The ordinary classes contain 238 queries with 116 positive and 122 negative labels. The ten boundary queries contribute eight positive and two negative labels, producing the declared 248-query balanced population. The manuscript explicitly avoids assuming that all ordinary queries share their representative's label.

The resource-path lemma has the needed source-specific restrictions: fixed prime, class and catalogue policy; frozen adapter/controller; cold cache; no pending jobs; default response cap; and the posted flat resource tariff. At a fixed prime, the exponent's length and bit pattern fix the modular-power operation schedule. The relevant same-class admission, solve/check, retention and completion branches are consequently fixed. The theorem concerns charged resource vectors and completion status, not physical CPU cost or common truth labels. It would not automatically extend to a value-sensitive tariff, different implementation, warm cache, changed scheduling, or arbitrary policy catalogue.

The earlier independent analytic review checked the concrete bounded paths, all 90 representative-policy resource vectors, all 1,488 retained population resource/completion rows, all fourteen-coordinate means and all six price selections. This integration review confirms that the companion accurately states that reviewed argument and its limits; it does not claim to have rerun those solvers. See [analytic review v2](../analytic_profile_agent/analytic_review_v2.md) and [class/resource proof review](../analytic_profile_agent/class_resource_review_v2.md).

## Exact evidence and tariff integration

The new [integration checker](integration_checks.py) performed **76 exact-to-displayed-number comparisons**, all passing at the specified precision. Its saved output includes the exact fractions, tolerances, evidence hashes and the separate setup-label finding. Its original numeric-only status names one finding because the credal-set wording qualification was added after that output was saved; the earlier output has been preserved rather than rewritten.

The principal checks were:

- All eighteen decimal cells in main §6.2's six-price table, their selected policies, and one-time setup subtraction. The only saved checkpoint policy change is the storage-expensive sequence fallback/fallback/fallback/full_fallback. This is a claim about that saved realization, not universal monotonicity.
- Sampled, exhaustive and analytic acquisition bills of **1,692,957**, **359,918** and **64,581** posted units. The analytic bill consists of 9,223 representative units plus 55,358 model/identity units; each price readout separately costs 740 units under the ordinary tariff. The exact profile's numerical core is 5,680 bytes and its stated identity matches the retained evidence.
- Warm-profile mean costs of 127447/16000 for the controller, 19675987/64000 for fallback and 65159/16000 for direct exact answers; the extra controller cost versus direct exact is exactly 3.893. The warm certificate lower value and the outer procurement bill also match.
- Whole-audit v2 means of 44446187/256000 for the controller, 78733879/64000 for fallback, and 4172681/256000 for direct exact answers. The mean saving relative to fallback is 270489329/256000, and its all-in lower certificate is 1211017049/4096000. All displayed six-decimal conversions are correct. The outer bill is 56,409,605 units, including the prepaid 45,598-unit startup charge; its ordinary-tariff value is 11281921/200. The episode resource cap 628752 and scalar lower range endpoint $`-718594/125`$ match the reviewed construction.
- The analytic companion's exact six-price, two-horizon table, the main manuscript's corresponding decimal summaries, and the stated source/identity scope. The high-price analytic H64 value is 35638361/31000 and the storage-expensive H64 value is $`-23590171/31000`$; both reflect their own acquisition and readout prices.
- The identification diagnostic's exact n=45 accuracy threshold, its necessary chi-square n=18 lower bound, and the affordable n=12 accuracy; the optional-stopping diagnostic's displayed crossing probability; and the bounded dependency diagnostic's posted-stage arithmetic.

The analytic profile is frozen before the retained exact reference is read. The reference assertions gate development validation, but do not construct or price-select the numerical profile. The manuscript properly leaves external validation instrumentation and human theorem/program development outside the 64,581-unit operational bill, and explicitly leaves the latter unquantified. Its theorem handproof is a prerequisite; no generic paid theorem checker has been demonstrated. The comparisons therefore establish neither a total historical-development cost nor superiority over simply purchasing direct exact answers. These boundaries agree with [analytic review v2](../analytic_profile_agent/analytic_review_v2.md).

Main §7's literature summary is consistent with the inspected retained primary-source cards, including the distinction between online computation costs and separately amortized offline construction. No new literature search was conducted for this integration pass, and no novelty or priority conclusion follows from it. The local Markdown link-target check found no missing targets.

## Final limits

After the two narrow manuscript qualifications, no additional mathematical, rounding, tariff, source-binding, or evidence-leakage defect was identified in this scoped integration review. The supported outcomes remain those of the frozen source versions, declared finite workload, posted tariff, fixed catalogue, and specified evidence protocols. Positive gain against fallback is compatible with the observed lower cost of direct exact answers. The review is development evidence, not a blind replication or independent external-model audit.
