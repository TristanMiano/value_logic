# Proposed recurrence dashboard patch

Contributor: **ChatGPT (GPT-6 Astra Pro)**. DEVELOPMENT/reporting proposal,
October 12, 2026. No global file, clock or historical row is changed by this
note. Exact research times and the final forecast are supplied by the principal
after closing the hour; the displayed forecast below is the present assessment.

## 1. Main Markdown layout

Keep all **17 existing historical rows and their probabilities unchanged**.
Move their existing complete table, if helpful, under **Historical measured
duties through s06**. Retain its 272-edit and 80-request explanatory tables.
Above that history, add **Current S28-B1 / F01 recurrence dashboard**, with one
new row per hourly recurrence. This keeps useful current measurements visible
without manufacturing old measurements of a mechanism not yet introduced.

Use this exact new-row content after replacing the two time placeholders with
the independently rounded final integer-nanosecond values:

| Recurrence | Research min | Cumulative min | Checked outputs | Complete-plan closures | New audits | Complete / native-IHS calls | Quotation units | Named bill / audit-first | Demonstrated 10% full-cost regions | Promotion forecast |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s07 hourly round | PRINCIPAL_FINAL | PRINCIPAL_FINAL | 16/16; first | 11/11 needing work; first | 14; first | 14 / 0; first | 1,718,749; first | 4.7544 times; first | 0; first assessment | F01: 20–45%, central 30%; first recurrence assessment; −5 pp from its within-hour baseline |

Link the row label to the final s07 checkpoint. Complete-plan closures count
the eleven requests not already closed from initial retained evidence, all
completed after an actually executed supported plan. The operation ratio is
explicitly a **named-unit component**, not a full economic ratio. The zero
region entry means none established with complete relevant prices and evidence;
it does not assert that every possible symbolic price assignment is impossible.

Add a short paragraph next to the table:

> These columns follow one declared source, request schedule, purchase menu
> and cost contract. Actual repeats report changes since the previous comparable
> measurement. When a round works on another construction, carry the latest
> value with its original measurement date and age, clearly marked “carried;
> no new measurement.” The promotion forecast is reassessed numerically each
> recurrence, including unchanged or lower assessments. Family counts, test
> counts and elapsed time are not promotion probabilities.

The **F01** paragraph should link [forecast_design.md](forecast_design.md),
[forecast_update.md](forecast_update.md) and
[verification_review.md](verification_review.md). Replace the obsolete current
“readiness unassessed” prose with the present numerical assessment and its
concrete blocker: material complete-cost benefit against the strongest named
conventional implementation remains unestablished. Do not alter the old cells.

### Supporting table: actual development within s07

These are **three implementation measurements within one recurrence**, not
three new research hours. They explain favorable movement in the new columns:

| Version | Checked | Executed complete-plan closures | Audits / complete calls | Quote units including setup | Named arm units | Named ratio to audit-first |
|---|---:|---:|---:|---:|---:|---:|
| a01 / v1 | 16/16 | 0/11 | 14 / 14 | 2,314,412 | 2,799,250 | 5.7709 |
| a02 / v2 | 16/16 | 11/11 | 14 / 14 | 2,797,711; +20.88% | 3,385,019; +20.93% | 6.9785 |
| a03 / v3 | 16/16 | 11/11 | 14 / 14 | 1,718,749; **−38.57%** | 2,306,193; **−31.87%** | 4.7544 |

Compute exact percentage displays from source integers when applying the patch.
The active row uses the **latest completed a03**, not whichever intermediate
result looks best. The matched audit-first denominator is **485066** named
arm units. A future rerun of that control must retain its own measurement date.

## 2. Additive JSON update

The current [recurrences.json](../recurrences.json) is schema
`c001_recurrence_progress_v2`. No live Python consumer of this schema was found
in the scoped repository search; a maintenance JSON records an older file
hash, which remains historical. Use a descriptive **v3** schema label and keep
every existing row object intact. Add fields; do not replace the old series.

1. Copy the old `current_readiness_assessment` unchanged into
   `readiness_assessment_history` before setting the new current assessment.
2. Preserve the old `metric_policy` under `metric_policy_history`; update the
   current policy prospectively to allow explicitly marked carried values and
   require a numerical assessment each new recurrence. Historical N/A semantics
   remain unchanged.
3. Append one `s07_cp01` row using the existing row keys. The principal fills
   `research_ns`, `cumulative_research_ns`, rounded times and `time_evidence`
   from the final effective actuals. Update top-level current pointers/totals
   from the same exact record. Reporting adds zero research credit.
4. Keep the old metric IDs and definitions. Add the new definitions below and
   `forecast_events.F01`, `forecast_assessments`, `active_metric_ids`, and the
   new comparison scopes. New fields need not be backfilled into old rows.
5. The new row may retain the six old experiment metrics as explicitly carried
   legacy evidence, or omit them from its active view while retaining their
   historical rows. Do not run old workloads merely to populate columns.
   Family count remains a portfolio quantity in JSON; confirm new family IDs
   against the final portfolio rather than using it as readiness evidence.

### New metric IDs and selectors

All JSON paths below are relative to `v3/discovery`, following the existing
record convention. Use scope ID **`s28_b1_joint16_menu1_v1`** for these active
metrics. Keep implementation version `s07-complete-bundle-v3` separately.
The extractor's hash currently called `scope_id` binds the common outer
source/request/admission data; retain it as `source_binding_sha256` under this
full scope. The full scope also binds the menu, caps and policy tariff below.
Do not use equal outer-source hashes alone to merge the expanded witness menu.

| New ID | Value | Unit / denominator | Exact selector / definition |
|---|---:|---|---|
| `joint16_checked_outputs` | 16 | outputs / 16 | `s07/a03/results.json: arms[policy=bundle].requests`, count checked status with bound at most tolerance |
| `joint16_complete_plan_closures` | 11 | requests / 11 initially unclosed | Distinct `plans[].request` with nonnull plan and a checked final request; denominator `16-sum(requests[].closed_from_cache)` |
| `joint16_audits` | 14 | actual audits | Count `events[kind=audit]` |
| `joint16_complete_calls` | 14 | complete logical calls | Count `events[kind=complete]` |
| `joint16_native_ihs_attempts` | 0 | capped native-IHS attempts | Count `events[kind=native]`; keep distinct from complete calls |
| `joint16_quotation_units` | 1718749 | named units | `sum(plans[].quote_units)=1716389` plus `invoice.planner_initialization_units=2360`; full meter deltas across all categories |
| `joint16_named_arm_units` | 2306193 | named units | `invoice.operation_units`; includes quote cost already |
| `joint16_named_ratio_audit_first` | 4.754390124230517 | dimensionless | `2306193 / 485066`; denominator `s07/a01/results.json: arms[policy=audit_first].invoice.operation_units` |
| `f01_demonstrated_cost_regions` | 0 | evidence-supported qualifying regions | Current assessment in `s07/forecast_update.md` / `verification_review.md`; no supported complete-price region yet. Treat as an evidence assessment, not an acquired observation. |

All those measurements are first entries in their recurrence series, so their
`previous_comparable_row` and recurrence `absolute_delta` are **null**. Do not
report the a02-to-a03 percentage change as a change from s06. Store within-hour
measurements in a separate `development_measurements` array, linked to a01,
a02 and a03. The source extractor computes them without new acquisitions.

Use the current derived artifact [progress_results.json](progress_results.json),
SHA-256 `390692c2017f5f072f4689ff18bef7232293f0f7e4e54072a4986a33838d505f`,
with extractor **`s07-progress-extraction-v3`**, SHA-256
`0353a49367b7aaa109af30a711d5c36e9c8c1f3e2758e0eea03f974a3c4c3f70`.
Its active arm selector is
`arms[version=s07-complete-bundle-v3,policy=bundle]`; use `counts`, `quotation`
and `resources` there, and
`comparisons[candidate_version=s07-complete-bundle-v3,control_policy=audit_first]`
for the named ratio and full symbolic cost condition. These are derived
selectors; each entry retains its original raw source/hash/measurement UTC.
The report's creation does not reset any metric's observation age.

Version v3 corrects one reporting assumption, with v2 preserved separately:
the exact archived a01 control code constructs no bundle planner. Their
`resources.additional_quotation_payload_bytes=0` records **source-proven
structural absence** of prepared-quote, enclosure and margin payloads,
with provenance in `resources.quotation_payload_measurement`. It does not
interpret a missing field as zero. Candidate a01/a02 payloads remain unknown;
other host/native memory remains in the explicit unpriced remainder for every
arm. No active count, quotient, forecast or raw acquisition record changes.

### One concrete metric object

This object is ready to place under the new row's `fixed_metrics`; subsequent
objects follow its pattern with their corresponding values and selectors:

```json
{
  "scope_id": "s28_b1_joint16_menu1_v1",
  "variant_id": "s07-complete-bundle-v3",
  "measurement_status": "first measurement",
  "observed_in_row": "s07_cp01",
  "measurement_utc": "2026-10-12T20:22:24.594133+00:00",
  "age_in_recurrences": 0,
  "value": 1718749,
  "units": "named operation units",
  "previous_comparable_row": null,
  "absolute_delta": null,
  "sources": [
    {
      "path": "s07/a03/results.json",
      "sha256": "64687890283a2082bdefe37b760c82bffb9195f7a759b51adfee426e54b2eda9",
      "locator": "arms[policy=bundle]: sum(plans[].quote_units) + invoice.planner_initialization_units"
    }
  ],
  "comparability_note": "Full quotation meter deltas plus constructor work; a subset of the enclosing invoice, never added again to total cost."
}
```

The ratio metric additionally needs `numerator_value=2306193`,
`denominator_value=485066`, each source/measurement UTC, and
`denominator_observed_in_development_run="s07/a01"`. Its scalar is not an
unqualified all-in efficiency metric.

### Forecast object preserving existing conventions

Continue using the existing `confirmation_forecast_percent` key. Its numerical
`value` is the central judgment and the range remains a separate field:

```json
{
  "scope_id": "candidate_specific_confirmation_event",
  "event_id": "F01",
  "candidate_id": "S28",
  "candidate_version": "S28-B1",
  "verification_plan_version": "V1",
  "measurement_status": "new assessment",
  "assessment_status": "assessed; remain in discovery",
  "assessment_utc": "2026-10-12T20:34:42+00:00",
  "value": 30,
  "probability_range_percent": [20, 45],
  "previous_comparable_row": null,
  "previous_comparable_assessment_id": "F01_s07_start",
  "change_since_previous_assessment_percentage_points": -5,
  "range_endpoint_changes_percentage_points": [-5, -5],
  "recurrence_absolute_delta": null,
  "gap_to_80_central_percentage_points": 50,
  "gap_to_90_central_percentage_points": 60,
  "sources": [
    {"path": "s07/forecast_design.md", "locator": "F01 event and prospective baseline"},
    {"path": "s07/forecast_update.md", "locator": "20–45 percent; central 30 percent"},
    {"path": "s07/verification_review.md", "locator": "Full-cost inequality and strongest comparison"}
  ]
}
```

The principal may revise the final assessment after later evidence; retain this
assessment and its UTC in `forecast_assessments` rather than changing its
historical number. The start record is **25–50%, central 35%, at
2026-10-12 20:03:17 UTC**. No preceding recurrence recorded F01, so the −5 pp
belongs to the within-hour assessment series. Future same-event recurrence
deltas use the previous recorded F01 assessment, even if experimental metrics
are carried. A changed event begins a new forecast series.

### Carry-forward example for a later round

For an unremeasured quote value in s08, retain `value=1718749`,
`observed_in_row="s07_cp01"`, the original source hash/UTC and
`variant_id="s07-complete-bundle-v3"`. Set
`measurement_status="carried_forward"`, `age_in_recurrences=1`,
`carried_in_row="s08_cp01"`, a specific reason, and `absolute_delta=null`.
Do not change the old observation date or claim a new zero improvement.
When a genuinely comparable s09 result appears, compare it to the s07 actual
measurement across the carried row. Compute age from recurrence rows, not
elapsed minutes or the number of artifacts produced.

## 3. Scope binding and separation

For **`s28_b1_joint16_menu1_v1`**, record:

- Source identity `8ff4d4165568151a25a530b085c2c27cda9bd77408b1a552d4358008211a33df`;
  source-file SHA-256 `59714c7fc872a06c4df23049d6ea79e3179b4562d50d4c4c7658315f6ad078a0`.
- Ordered `(request,row,price,tolerance)` signature
  `f21f611e311f5e506ede47cc75de486ff6375e6ad89828e6c2c6716ff2c65684`.
  Six nonnegative integer cost modes, eight finite rows, sixteen requests;
  internal price/tolerance **48/4**, cohort means **6/0.5**.
- Initial admitted 29 witnesses and 18 trees; bind the raw admission hashes
  from a03. Current common admission is **99694 named units** and historical
  acquisition **77646**, separately retained. Common evaluator SHA-256
  `1ec100e50c6ab11600d9074fa718b4136d8227192b112676de468979725a6b8a`.
- Purchase menu: supported complete branching plus capped native-IHS path;
  no robust-witness proposer in this executed F01 menu. Limits: **64 audits,
  128 logical purchases, 80 main-loop steps/request**; audit plan depth **1**,
  with each multi-call leaf's separate complete-call reserve. Native caps are
  retained in the bound source: 64 rounds, 0.1 s per MIP call, 10000 SAT
  conflicts/MIP nodes, 1000000 proof/adapter units. These are not a complete
  host deadline or an outcome law.
- Price-policy slice `a/sigma=1000` is a conditional selection parameter,
  not a measured external tariff. Full `U+a*A+rho*T+s*B+R` accounting and
  unmeasured components remain explicit. Same source alone does not make an
  expanded purchase menu or a new source law a comparable recurrence lane.

Use **`joint16_robust_witness_menu2_v1`** for the new expanded-menu screen.
Both schedules use 16 outputs, 14 audits and eight complete calls; native
proposals are **25 versus 11**. Store their respective counts and named bills
under separate policy IDs, not as a 14-to-8 F01 improvement. Both have **six**
strict proposal-induced bound improvements and **three** proposal-caused output
closures. The matched named arm bills are **1142250 versus 658633**, not a
complete-cost result. Whole-arm runtime includes order-dependent repeated
serialization of previously completed arms, so it is unsuitable as a clean
comparative speed claim. The actual independent review belongs with that scope.

S29's affine geometry and S30's population CDF source each get separate scope
IDs. S30's relevant-audit **29 versus 58** and equality to the direct control's
**29** are informative new measurements, but neither replaces F01's fixed
fourteen audits nor supplies a same-event forecast increase.

## 4. New evidence and F01

The expanded witness menu shows a concrete benefit from avoiding repeated
native proposals: audit-before uses **14 fewer** than witness-before, with
equal output and complete-proof counts. It strengthens the next conventional
comparison and suggests a better acquisition route. The menu changed and the
stronger ordinary schedule also receives it; this is not an F01 economic win.
I would **retain 20–45%, central 30%** unless the principal has additional
same-event evidence. Keep the new scope's promising result visible without
turning it into readiness for a different claim.
