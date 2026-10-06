# F16 independent accounting review

Reviewer: ChatGPT (GPT-6 Astra Pro), separate accounting agent. The principal
supplied its expected totals; this reviewer reconstructed them from raw integer
monotonic readings instead of assuming the supplied totals. No concurrent
reviewer minutes are added to the principal's accounting.

**Status: research interval verified; final overhead close and appended ledger
verification pending.** This first review is bounded at the observed transition
to O at `2026-10-05T23:53:18.425936+00:00`, monotonic
`31004665696319`. It does not credit the open administrative interval.

## Method and source binding

Read the binding [research protocol](../../RESEARCH_PROTOCOL.md), the relevant
[TODO timing and F16 requirements](../../../TODO_v2.md), the prospective
[forecast](forecast.json), [baseline](ledger_baseline.json), raw events,
segments, recovery exclusions and mode transfers. Neither `adjustments.jsonl`
nor `mode_reclassifications.jsonl` existed in this snapshot. The matching
machine-readable report records the snapshot hashes.

Reconstructed all 84 closed segments from 105 raw clock events, including
their mode, lane, note, runtime, UTC and monotonic endpoints. All reconstructed
fields match. Elapsed seconds in every saved segment agree exactly with its
integer nanosecond difference. Segments partition the measured interval
without gaps or overlaps; every event uses `linux-F16-S1`. The largest adjacent
observation gap is 307.186281373 seconds, below the fifteen-minute requirement.
UTC and monotonic interval differences are at most 0.000209812 second; all
credited arithmetic uses monotonic time.

Whole-segment recovery exclusions remove three intervals in full. The two
mode-transfer records split their original segments at existing observed
clock events. Each transfer lies inside exactly one segment, has the recorded
original mode/lane, overlaps no exclusion or other transfer, and removes
research credit while preserving engaged O. No raw event or segment was
rewritten by this review.

## Recomputed research totals

| Mode or lane | Exact nanoseconds | Minutes, shown to 12 decimals |
|---|---:|---:|
| D | 4,049,009,098,156 | 67.483484969267 |
| L | 810,626,919,554 | 13.510448659233 |
| E | 555,314,650,319 | 9.255244171983 |
| D + L + E | 5,414,950,668,029 | 90.249177800483 |
| R | 2,527,377,335,270 | 42.122955587833 |
| X | 2,887,573,332,759 | 48.126222212650 |

The exact integer totals, rather than displayed decimal rounding, determine
the floors. **Fresh D60 and Research90 both pass.** D exceeds its floor by
449.009098156 seconds; research exceeds its floor by **14.950668029 seconds**.
Neither old F15/ND01 work, O, excluded time nor parallel-agent time contributes.
Research lane shares are R 46.6740602% and X 53.3259398%; they sum to the entire
research interval. This is a deviation from the 60/40 forecast to explain,
not grounds for relabeling work retrospectively.

The two transparent transfers remove 178.633335412 seconds from E/X and
127.455359580 seconds from D/R, adding their combined 306.088694992 seconds to
O. Through research close, closed O is 472.697335145 seconds. The raw wait
bucket is 128.195321389 seconds and wholly excluded. It contains distinct
paused recovery inspections, so it should not all be labeled tool waiting:

| One-based raw segment | Start monotonic ns | End monotonic ns | Paused recovery/inspection seconds |
|---|---:|---:|---:|
| 12 | 25,194,462,035,672 | 25,222,928,559,515 | 28.466523843 |
| 46 | 27,266,802,816,921 | 27,292,575,513,382 | 25.772696461 |
| 74 | 29,780,228,623,458 | 29,814,343,027,967 | 34.114404509 |

These sum to 88.353624813 seconds; the other paused intervals sum to
39.841696576 seconds. The additional three whole-segment recovery exclusions
sum to 786.607095348 seconds. This classification does not affect any engaged
total. The saved bounded math-process record excludes its blocked wait and
does not add background computation or reviewer effort to concurrent principal
work. The audit found no recorded tool wait or identified recovery gap left in
research credit.

The durable derivation, primary-reading and bounded computation/interpretation
records support the recorded mode distinctions. This accounting audit checks
their presence and timing correspondence; it is not another mathematical
acceptance or independent observation of every instant of engagement. No
artifact length or number of checks is converted into minutes.

## Historical prefix and cumulative clock

The original **237,548 bytes / 1,006 CSV data rows** are unchanged and match
both source commit `6ef27f20e3ac0920953a27dd84d6c91a021ba58f` and SHA256
`708b045b4e2432a28dc5cff1e897ab9cb1946ff0a3283d33064548aee5c532e1`.
No F16 rows had yet been appended at the first review.

The authorized inherited POST-B-1 entry is
**801.13038837636666666666666666666666666666666666667 minutes**,
matching the prior ND01 actuals. Preserve that entry and add the exact F16
increment. A direct sum of historical CSV `engaged_seconds` from the first
N01 row yields 801.1303871431166666666666666666666666666666666666666667
minutes. The inherited entry is higher by **0.00000123325 minute, or
0.000073995 second (73.995 microseconds)**. This is a pre-existing reconciliation
difference associated with historical checkpoint carry values, not an F16
increment or a reason to rewrite old rows or reset the cumulative clock.
The principal confirmed that the authorized inherited baseline will remain
unchanged and this difference will be disclosed.

## Remaining final check

After O is closed, independently recompute the complete increment and inspect
the appended ledger. Check exact nanosecond-to-decimal row amounts, preserved
prefix, the two split transfers, excluded recovery and waits, no overlap,
actuals agreement, forecast differences, and POST-B-1 entry plus increment.
Final commit/publication administration after the stopped clock must not be
retrospectively credited.

### Pre-execution accounting-script review

Read `close_accounting.py` without executing or importing it. Its source-prefix
guard, stopped-clock requirement, split transfers at observed events, exact
integer totals, research cutoff, recovery-pause classification, CSV category
partition and inherited POST-B-1 carry agree with the independent reconstruction
for the observed inputs. The reviewer recommended direct Decimal equality to
integer nanoseconds instead of converting through `int`, and explicitly checking
each exclusion's saved end against its segment end. These are stricter input
checks; the already inspected data satisfy both conditions. The script's
80-digit decimal minute strings represent repeating rational values with finite
rounding. Floors and new credited time must continue to use integer nanoseconds.
Its eventual execution and resulting rows still require the final independent
check below; a source review is not an execution result.

One harmless reviewer inspection failure is retained: an `rg` request included
a guessed prior `ledger_audit.json` path that did not exist. The existing prior
`actuals.json` files supplied the needed evidence. No clock, ledger, code,
experiment or source was changed by that failed read. This reviewer ran only
read-only arithmetic and source inspection and created these two audit files.
