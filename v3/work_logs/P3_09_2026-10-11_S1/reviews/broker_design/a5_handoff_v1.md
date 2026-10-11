# P3-09 A5 observer amendment handoff

Contributor: **ChatGPT (GPT-6 Astra Pro)**. **DEVELOPMENT observer only**,
October 11, 2026. Principal clock credit: **zero**.

## Current source and preserved evidence

The amended `v3/experiments/p309_broker.py` is 60,086 bytes, SHA-256
`6dbe26a870416ae54a206d258472ab710a2d78d9705cfde68ebd56cf491b9787`.
It adds one observer function and two score-field calls. An AST comparison
confirmed every other original function and class, including `run`,
`generate`, configuration, method selection and selfcheck, is unchanged.
The original `_report_widths` interface also remains unchanged.

The previous 56,461-byte adapter and its paid records remain immutable in
`development_v1`. The new complete closure, observer and plan are copied in
`a5_observer_v1`; its manifest has SHA-256
`7c3cee7f15d9e415edf29a1f01506f40475cbf0670c2f3d8ca24388a6f4a663e`.
The observer result has SHA-256
`6ac07c9920c79e68b6357d7f9366932134c259c8509bdb780f3f50ce5c022c78`.

The focused check passed **975 assertions**, using the 30 saved v1 public
development records and four fixed synthetic interval/status cases. It made
**zero policy, provider, reporter, private-truth or final-generator calls**.
There was no method rerun, random stream, final population or winner/threshold
selection. All source and input hashes still matched after the check.

## New score field

`paid_report_comparison` is available on regular and completed-invalid score
records. It records the complete already-paid optional fee, scheduled horizon,
existing reference basis and radius rule, and an explicit top-level status:
`not_requested`, `failed`, `success` or `confidence_conflict`. No-report and
failed-report cases have an empty endpoint mapping. The empirical-coverage
flag is always false.

Each `endpoints.V`, `endpoints.F` and `endpoints.Z` record retains:

- Delivered lower and upper bounds, usable width and width per horizon.
- The paid deterministic envelope's lower/upper bounds and width, also per
  horizon.
- `normalized_width_reduction`: deterministic width minus delivered width,
  divided by scheduled horizon.
- Signed raw and normalized `lower_endpoint_gain` and `upper_endpoint_gain`.
  The first is delivered lower minus deterministic lower; the second is
  deterministic upper minus delivered upper.
- `practical_width_reduction`, using the prospectively fixed inclusive
  threshold `1/100`, plus same-threshold side indicators.

The two signed endpoint gains sum to the width reduction before normalization.
The independent checker uses that identity to reconstruct the reduction from
the endpoints. A wider delivered interval preserves a negative reduction and
negative side gains; no value is clamped to zero. A conflict retains the raw
bounds and signed span but has no usable width or width reduction and no
positive practical indicator. It therefore cannot become a reporting winner
because its endpoints cross. The original `paid_report_endpoint_widths` field
retains its previous schema and values.

These are observer comparisons against the same report's already-computed
deterministic envelope. No extra reference policy or reporting procedure is
computed or claimed for free. Invalid parent scientific output remains
invalid even when its raw report arithmetic can be displayed. Report widths
are not estimates of empirical seed coverage.

All 21 quantity records from the seven successful preserved toy reports have
exactly zero normalized width reduction against their deterministic envelope;
none meets the practical threshold. This no-improvement observation remains
visible with the original paid fees. It is a result on the already exposed
fixed toy, not evidence about ungenerated final populations and not a reason
to change the report construction or threshold.

## Accounting boundary

The new adapter bytes increase the prospective common source charge from
65,114 to **66,076** word units, a difference of 962. This is a byte-only
calculation under the unchanged source tariff; it is not a newly executed
policy invoice. The 30 preserved paid development records retain their
original 65,114-unit source bills, and their optional-report invoices are
copied exactly. Old records must not be labelled as execution of the amended
source. Root's copied-source preparation gate will exercise the current full
closure prospectively.

## Reproduction and handoff

The completed observer invocation was:

```bash
python v3/work_logs/P3_09_2026-10-11_S1/reviews/broker_design/a5_observer_v1/a5_observer_check_v1.py v3/work_logs/P3_09_2026-10-11_S1/reviews/broker_design/a5_observer_v1
```

The observer refuses to overwrite the completed `run` directory. Its manifest
binds the preserved v1 input and adapter by exact paths and hashes. A future
observer reproduction needs a new destination with the same closure and
inputs, and must retain any failure as a new record. No full selfcheck or
method rerun was performed for this observer amendment. Canonical ownership
is returned to root at the current source hash above.
