# Targeted review of the observation contract

2026-10-07. Reviewer: **ChatGPT (GPT-6 Astra Pro)**, internal delegated semantic review. Scope: P3-01 requirements only; no new learner, implementation, literature search or gate assessment. This is a fresh review of the observation prose and JSON index against the main contract. The linked counterfactual stress note is this reviewer's earlier work, so that part is self-reconstruction rather than independent authorship.

**Disposition:** the four requested distinctions are substantially consistent. Two local wording corrections and one access-provenance clarification would close the remaining ambiguity. None requires another example family or algorithm.

## 1. Concrete corrections

### OR01 — separate empirical learning evidence from a learning theorem

Observation §2 says: “A learning claim needs a stated training/update history and an appropriate held-out comparison.” The universal wording is stronger than main §9 and JSON Q1/Q4, which permit a proved restricted refinement/decision result. A theorem about a specified update procedure and admissible stream does not require an empirical held-out comparison to establish that theorem. Conversely, an empirical held-out result does not establish the unrestricted theorem.

Suggested replacement: **“An empirical learning claim needs a stated training/update history and an appropriate held-out comparison; a theorem claim needs its specified procedure, admissible information/stream and proof.”** Keep the adjacent shortcut-cost/correctness requirement. This is an evidence-type correction, not a relaxation of empirical validation.

### OR02 — remove the remaining equal-information shorthand in Q3

Main §9 Q3 requires a gain surviving “equal information, model library, computation budget and objective.” Main §8, CB01, observation §2 and JSON `observation_requirements.policy_comparison` correctly distinguish equal initial access from potentially different purchased histories. Read literally, the table's equal-information requirement would exclude an acquisition policy precisely when it buys useful information the competitor elects not to buy.

Replace that table phrase with **“equal initial information/access, model library, resource rules and objective, charging each policy's acquisitions.”** A common-history replay remains a separately named endpoint. The prose and JSON do not need another policy-comparison mechanism.

### OR03 — accessibility needs an actor and indirect-use provenance

Observation §1 correctly says that hidden evaluator generation alone is not agent exposure. However, JSON `resolution` offers an “agent accessibility event or evaluator-only flag.” That binary alone cannot distinguish an evaluator-only answer that stays unavailable to method design from one inspected by a designer and then embedded in the method's parameters, rules, prompt or cache. Neither case requires the deployed method to receive a feedback event.

A concise condition is sufficient: **record whose access occurred (method, designer/tuner, evaluator), and disclose whether evaluator labels influenced method selection or supplied parameters/advice. “Evaluator-only” must not itself certify a held-out comparison.** This is a missing provenance condition for future empirical claims, not evidence that the present development work exposed a final population. Main §7's prospective selection freeze and §6.3's advice/cache accounting already point in this direction.

## 2. Distinctions that survive the review

**Generation versus availability.** The new prose correctly permits prior hidden evaluator computation, detects visible metadata/cache routes, and does not treat creation time as the time the method gained information. The main contract separately charges access/decoding and admits earlier version-matched evidence. There is no need to ban every precomputed answer or legitimate cache.

**Initial accuracy versus learning.** Main §5.2 explicitly admits a charged fast exact solver and rejects calling post-resolution accuracy anticipation of that resolution. Observation §2 correctly treats initial-report quality as a mechanism-neutral endpoint. For clarity, retain the name **initial-report endpoint** in summaries; reserve a claim of anticipating resolution for reports made before the method's relevant resolution. The first endpoint can improve through a faster solver or lawful reuse without supporting learned generalization. This clarification follows existing conditions rather than adding another duty.

**Different acquired histories.** A full policy comparison fixes initial access, available computations, observation rules, prices and hard budgets, then charges each policy's own choices. A replay supplies a common history under a common information-cost convention. Shared exogenous evidence can legitimately arrive to both. The JSON's short policy sentence is consistent when read with main §8/CB01; it is not a complete list of matching conditions by itself.

**Counterfactual response axes.** The request already carries operation, ordinary scope, retained constraints, propagation, ranking/tie policy and evidence dependencies. The response then separates search/feasibility, selection meaning, coverage, numerical form, numerical meaning, evidence and resources. No additional numerical confidence field can replace these. In particular, an optimum witness need not cover tied consequences; a policy point need not identify a structural consequence; a loose outer interval need not contain two attainable values; and certified infeasibility supplies no nonempty selected cost family. Original-scope meaning and exceptional hypothetical evaluation remain distinct under main §7/C04.

The JSON explicitly calls itself an index rather than a validated API. Omitted enumerations, field-level validators or repetition of every cross-field condition are therefore not current implementation defects. Any eventual serialized response must remain bound to its versioned request and target family; otherwise even correctly named status fields would be ambiguous. The present canonical prose supplies that semantic obligation.

## 3. Reviewed state and resources

Read the observation contract, JSON index, relevant main §§5/7/8/9, duty rows U01/U04/U06/U09/C01–C04/I01, CB01, and the earlier counterfactual status note. No numerical rerun was needed for this requirements review. Reviewed SHA256 identifiers:

| File | SHA256 |
| --- | --- |
| `01_observation_contract.md` | `7e16d9eefd01376526ee2b1501271b28a3bd5d6879e263790b00baf049bf857b` |
| `01_contract.v1.json` | `d08bdb5879d7593084af14be7cec9af5d36cfaf7be01c75a2ddf0a932f8d78e5` |
| `01_problem_contract.md` | `ead10134ac0d1ef1756eeea63263d312045eef9b8f8d5841c4c5302a2eb007f6` |
| `01_desiderata.md` | `0c1b250e1e22640c1a965015e009ed18a2661415af83f5086b893f0182376774` |

Only this review note was created for the semantic review. Separately, the parent-requested Def.20/Prop.21 printed-page locator correction was applied to this reviewer's earlier optional Hutter source card; its substance was retained. No canonical, control or clock edits. Own engaged duration, token usage and dollar cost are unmetered/unknown; **zero concurrent principal time credit**.
