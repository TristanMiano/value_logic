# F16 final independent accounting audit

**PASS — October 6, 2026.** Reviewer: ChatGPT (GPT-6 Astra Pro), separate
accounting agent. This review supersedes the pending final-ledger portion of
the [earlier audit](accounting_review.md) while preserving that audit and its
snapshot. The principal supplied expected totals; the reviewer derived the
results independently from raw integer clocks before comparing them with
[actuals](actuals.json), the [appended rows](ledger_append.csv), and the
[integrity record](ledger_integrity.json).

No scientific checks were rerun. No accounting input, script, clock, ledger or
experiment output was modified. Only the two final audit files were created.
Concurrent reviewer time contributes **zero** to principal engaged time.

## Exact clock reconstruction and exclusions

The final observed stop is **2026-10-06T00:11:03.848448+00:00**, monotonic
**32070088200858**. Clock state is null and the last event is `stop`.
Reconstructed all **87 raw segments from 110 events**, matching mode, lane,
notes, runtime and both endpoint representations. Every saved elapsed-seconds
value equals the corresponding integer nanosecond difference exactly.

Independent interval partitioning produces **90 effective intervals**: the
original segments plus three splits at existing observed clock events. All
intervals are positive, contiguous and non-overlapping. Every clock event uses
`linux-F16-S1`; the largest adjacent observation gap is 599.356840314 seconds,
below the fifteen-minute requirement.

The first two transfers remove reporting/administrative intervals from E/X and
D/R and retain them as O. The final partial recovery transfer divides the
administrative segment at the observed check:

| Administrative interval | Exact seconds | Disposition |
|---|---:|---|
| Research close to the 00:07:27.579973 check | 849.154030137 | Engaged O |
| That check to the 00:09:57.271157 recovery pause | 149.691184051 | Recovery/unobserved; excluded |
| Recovery pause to the 00:10:26.766520 resume | 29.495362231 | Paused recovery; excluded |
| Resume to the final stop | 37.081928120 | Engaged O |

Each transfer is contained in one raw segment, matches its original mode and
lane, and overlaps no other transfer or whole-segment exclusion. The three
earlier whole-segment recovery exclusions are preserved. All four paused
recovery inspections are separated from actual tool waits. Research remains
closed at monotonic **31004665696319**, and there is no D/L/E credit afterward.

## Independently derived totals

| Category | Exact nanoseconds | Minutes, shown to 12 decimals |
|---|---:|---:|
| D | 4,049,009,098,156 | 67.483484969267 |
| L | 810,626,919,554 | 13.510448659233 |
| E | 555,314,650,319 | 9.255244171983 |
| O | 1,358,933,293,402 | 22.648888223367 |
| Research D + L + E | 5,414,950,668,029 | **90.249177800483** |
| Engaged D + L + E + O | 6,773,883,961,431 | **112.898066023850** |
| Tool waiting | 39,841,696,576 | 0.664028276267 |
| Recovery/unobserved | 936,298,279,399 | 15.604971323317 |
| Paused recovery inspection | 117,848,987,044 | 1.964149784067 |
| All excluded time | 1,093,988,963,019 | **18.233149383650** |
| Observed elapsed time | 7,867,872,924,450 | **131.131215407500** |

The exact identity `elapsed = engaged + excluded` holds. Research is unchanged
from the first independent audit. **D60 and Research90 pass**, with exact
margins of 449.009098156 and **14.950668029 seconds**, respectively. Display
rounding is not used to decide either floor.

Research lanes remain R **42.122955587833… minutes** and X
**48.126222212650 minutes**, or 46.6740602% / 53.3259398%. Their nanosecond totals
sum exactly to all research time. O, recovery, waits and concurrent-agent work
contribute to neither lane nor research floors.

The original central/high forecasts are preserved. Relative to central, D is
2.516515 minutes lower, L 1.489551 lower, E 10.744756 lower, and O 7.648888
higher. Research is 14.750822 minutes lower and total engaged work
**7.10193397615 minutes lower** than the 120-minute central forecast. Those
forecast differences do not change the protected floors.

## Ledger and actuals verification

The entire original **237,548-byte / 1,006-row** CSV prefix is byte-identical to
source commit `6ef27f20e3ac0920953a27dd84d6c91a021ba58f` and retains SHA256
`708b045b4e2432a28dc5cff1e897ab9cb1946ff0a3283d33064548aee5c532e1`.

All **90 appended rows** match the independently derived effective intervals:
task/attempt/session IDs, mode/lane, observed UTC endpoints, exact elapsed,
engaged, waiting, idle and unmeasured amounts, artifact path and transparent
status descriptions. Each row partitions its own elapsed time correctly.
The file is exactly `original prefix + saved append`; it contains **1,096 data
rows / 265,648 bytes**, with SHA256:

`2ddbbff7ccbc4c76bd15f3c26a58273be562ba21f6967b9d1d87feab7958c8fa`

Every effective row and integer total in `actuals.json` matches this independent
reconstruction. All input hashes recorded there match current bytes. The
integrity record's counts and hashes also match. The first audit's raw clock,
segment and transfer prefixes are preserved; its unchanged exclusion,
baseline and forecast hashes still match.

The 80-significant-digit decimal-minute fields match recomputation under their
declared Decimal context. Repeating decimal strings are finite representations;
**integer nanoseconds are authoritative** for new elapsed and credited time.
No accounting or final administrative work after the stopped clock is credited.

## POST-B-1 carry and checkpoint

The authorized inherited entry is preserved exactly as recorded:

- Entry: **801.13038837636666666666666666666666666666666666667 minutes**.
- F16 addition: **112.89806602385 minutes**.
- Close: **914.02845440021666666666666666666666666666666666667 minutes**.
- Remaining to 960 minutes: **45.97154559978333333333333333333333333333333333333 minutes**.

There is **no reset and no sixteen-hour checkpoint crossing**. The earlier
audit's disclosed **73.995-microsecond** difference between the authorized
historical carry and a direct sum of historical CSV seconds remains an
inherited reconciliation difference. Neither prior rows nor the authorized
carry were rewritten to hide or remove it.

This is a pass of the recorded accounting and its consistency. It does not
independently observe every instant of engagement, establish mathematical or
contribution claims, or pass an evidence gate. The companion
[machine-readable final audit](accounting_postappend_review.json) preserves
exact totals, checks and reviewed-file hashes.
