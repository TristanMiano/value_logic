# P3-07 frozen multi-action code v2: focused independent review

## Disposition

**PASS for the three requested repairs and all 96 saved v2 rows.** No further
defect was found in this focused scope. The v1 evidence and its boundary-failure
witnesses remain preserved under their original source identities; this report
does not retroactively relabel them as v2.

This is a same-model independent source review and exact verification after a
nonblind repair prompt. The saved-row audit reuses the explicit equations from
the reviewer's v1 audit, adds checks relevant to the changed source and fresh
streams, and does not rerun any truth solver or old development experiment.
The targeted plan was saved before the new probes. All activity is DEVELOPMENT,
unmeasured, with **zero principal-clock credit**.

## Frozen source and provenance

| File | SHA-256 |
|---|---|
| `07_multi_action_forecasting.py` | `9605a0fa3483358bd6f0f98770b154888cbc37a37c4a746bfbf3e9f3f62453a7` |
| `07_multi_action_development.py` | `cb5e191150905d9c1615277ab7b5dac0811e8646d2a76924499226dfa0fd7291` |
| Saved computation adapter | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |

The first two hashes match both the current frozen sources and the saved run's
source copies. Reviewer snapshots preserve their exact bytes. All three run
source hashes agree among the saved run manifest, saved result, source copies,
and the v2 plan's explicit disposition record.

The v2 plan retained v1 values in `schema`, `recorded_utc`, `source_sha256`, and
`prior_scope`. The appended v2 revision, freeze time, repair rationale, and new
seeds are visible in the original bytes. The non-overwriting
`multi_action_plan_v2_disposition.json` explicitly identifies the inherited
fields and gives the actual v2 hashes. It is a subsequent clerical clarification,
not a new prospective numerical plan. The actual run manifest freezes the v2
source hashes before its exercise calls produce rows; its recorded start precedes
all 96 issuance timestamps, which precede the saved finish. The appended plan
freeze time precedes the run start.

The exact query stream with seed 307113 and action-bit stream with seed 307127
were reconstructed from the stored records. All 32 query positions differ from
the corresponding v1 case, for each of the three settings. This verifies the
declared fresh deterministic streams; it does not turn seeded data into evidence
for the separate independent-randomness theorem.

## 1. Numeric-cap settlement is transactional

The changed settlement path constructs `_report_for(...)` from local proposed
values before assigning any residual, cumulative costs, potential components,
pending state, or settled count. That construction validates the combined bound,
scaled square-root readout, action regrets, generic bound, and retained-gap bounds.
The final observation validates the retained and derived components, and the
prepared report's work record is refreshed before the semantic commitment.

The exact original failure fixture was repeated against frozen v2: two zero-cost
actions, eta 1, bins 4, input weight `1 << 4093`, root cap zero, and sixteen
synthetic binary unit-level outcomes equal to one. No mathematical truth service
was called. Every issued forecast is one-half. The sixteenth proposed settlement
again exceeds the 8192-bit cap through its combined bound, but it now raises
`Rejected` **before** consuming the forecast.

| State component | Before rejection | After rejection |
|---|---:|---:|
| Settled rounds | 15 | 15 |
| Pending forecast | Same sixteenth issue | Same sixteenth issue |
| Used identities | 16 | 16 |
| Retained bound bits | 8192 | 8192 |
| Paid work | 16488 | 16800 |

Exact comparison confirms that all semantic state fields are unchanged. The
312-unit failed-settlement bundle remains charged. Exporting the retained state
after rejection succeeds and reports 15 settled rounds with pending feedback.

This repair gives atomic semantic failure under the tested numeric-cap path;
it does not provide a cancellation or fallback controller for a forecast whose
settlement cannot fit the configured cap. Resource-account history is intentionally
not rolled back.

## 2. Direct lookup enforces bounded admission

`choose_slots` now rejects non-exact-integer or out-of-range bit counts before
shifting, and rejects action counts outside 2 through 8 before traversing the
slots. It then prepays the bounded cumulative-selection bundle before inspecting
individual slot values. The random draw is an explicitly admitted input; the
caller is responsible for funding its generation separately.

The focused probes rejected bit counts -1, 33, `True`, an exact Fraction equal to
8, the string `"8"`, and 100000; all were rejected before paying a lookup bundle.
Action counts 0, 1, and 9 also rejected before traversal. Valid boundary cases at
0 and 32 bits and the two sides of a categorical boundary at 8 bits returned the
expected action. Each valid two-action lookup paid six cumulative-selection units.

A malformed final slot with a zero work budget raised `Exhausted` before cell
validation. The same malformed slot with six funded units raised `Rejected`
after those six units were charged. Thus the public bit/action guards and the
prepaid bounded cell-validation contract both hold on these probes.

## 3. The actual harness funds random bits before drawing

The frozen v2 harness pays `fair_random_bits` immediately before `getrandbits`,
then calls the separately paid lookup. Focused instrumentation exercised this
actual harness order and denied funds at each of the two payment boundaries.
It only restricted a fresh test object's remaining budget at the chosen boundary.
It did not run a truth computation or create a labeled evidence row.

| Denied payment | Observed order | Action draws | Paid bit units |
|---|---|---:|---:|
| Fair bits | Pay attempt; `Exhausted` | 0 | 0 |
| Cumulative selection | Pay bits; draw; lookup pay attempt; `Exhausted` | 1 | 8 |

In the first case the action RNG state is unchanged. In the second case the
already-performed eight-bit draw is funded and retained. Both cases stop before
emitting an action or calling the truth service. The ordinary funded source
still flushes the issued action record before label acquisition, as in v1.

## 4. Saved v2 evidence

All 96 stored rows pass exact recomputation of the expert/tent/action feature
vector, score allowance, residual, variance, accumulated allowances, enlarged
potential inequality, predicted-gap decomposition, and smoothing slack. The
verification also checks projection KKT conditions, each row's fixed-action
regrets and square-root certificate, largest-remainder slots, exact dyadic mass,
sharp four-action TV cap, cost transport correction, and selected categorical
action. These are calculations on stored records, not repeated experiments.

The issued record fields exactly match the corresponding completed row and
contain no label. The full-feedback accounting correctly reuses a purchased
label for BUY and charges later label acquisition on every other action. Each
case's service-category totals, controller operations, round weights, fee
conversions, and final aggregates agree. The new ledger splits random bits from
cumulative selection: 32 times the bit count is charged to `fair_random_bits`,
and 320 units to cumulative selection. No old combined category remains.

| Setting | Root-tolerance misses | All-in cost excluding setup | Always-BUY service-fee cost |
|---|---:|---:|---:|
| Full root, eight bits | 0 | `32020931/50000` | 368 |
| Capped root, eight bits | 26 | `15969017/25000` | 368 |
| Full root, one bit | 0 | `32100707/50000` | 368 |

Setup is separately `2/3125` in each case. The exact pathwise identity is

```math
C_{\rm allin}=\sum_t w_t f_t+
\sum_t w_t L_t^{\rm nonBUY}+\sum_t w_t C_t^{\rm controller}.
```

The latter two terms are nonnegative for these action tables. Consequently all
three recorded totals exceed the always-BUY fee-cost comparator. The ideal
mixed action cost is a different quantity and does not include all mandatory
feedback and controller costs. Any additional overhead assigned to an independently
implemented always-BUY controller needs its own accounting; the displayed identity
uses the explicitly declared fee-cost comparator.

## Evidence and remaining scope

- [Prospective focused plan](multi_action_code_v2_targeted_plan.json)
- [Targeted probe source](multi_action_code_v2_targeted_probe.py)
- [Probe attempt and source identities](multi_action_code_v2_probe_attempt.json)
- [Exact result](multi_action_code_v2_targeted_result.json)
- [Forecaster snapshot](multi_action_code_v2_07_multi_action_forecasting.py)
- [Development harness snapshot](multi_action_code_v2_07_multi_action_development.py)
- [Original v1 review](multi_action_code_v1_review.md)

The resource model remains the declared bounded rational-operation bundle model
plus stipulated checked-service tariffs. The saved runs do not prove a physical
runtime bound, a hardware lower bound, an independent-fair-bits assumption, or a
guarantee with unpurchased feedback. Audit serialization and private categorical
frequency diagnostics retain their explicit harness scope. The unchanged adapter
was not rerun by this review. No root source, plan, clock, ledger, gate, or
publication file was modified.
