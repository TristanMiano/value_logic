# P3-01 accounting helper review

Contributor: **GPT-6 Astra Pro**, `/root/p301_induction_sources`.
Date: **2026-10-07 UTC**. Administrative implementation and same-model internal
review; **zero concurrent principal research or engaged-time credit**.

Created [accounting.py](../accounting.py). SHA256:
`68f9c0d5da0f133d8e276d36fa62e699a6422ff53021bc771d0a82fd3f5f15f6`.
No finalization command or ledger append was executed. Raw clocks, dispositions,
the clock helper, canonical research files and prior ledger bytes were not edited.

## Commands

From the repository root, the preview is read-only and emits JSON to stdout:

```sh
python v3/work_logs/P3_01_2026-10-07_S1/accounting.py preview
```

After the principal uses the existing clock procedure to close the active
segment, and after the protected research floor is met, the final command is:

```sh
python v3/work_logs/P3_01_2026-10-07_S1/accounting.py finalize
```

The final command appends exactly the effective P3-01 rows to
`v3/time_ledger.csv` and writes work-log-local `ledger_append.csv`, `actuals.json`
and `accounting_attempts/attempt0001/` records. It does not declare scientific
completion, contribution support or a gate pass. Later tasks and phase-three
gates remain unattempted. After success, another preview can audit the same
closed inputs and recognize the existing exact append; another finalization is
an error, not a no-op presented as a fresh success.

## Exact mapping and preservation

| Effective category | Ledger mode / lane | Engaged credit | Research credit | Exclusion column |
|---|---|---|---|---|
| D / L / E | Same mode; R or X | Full interval | Full interval | None |
| O | O; blank | Full interval | Zero | None |
| wait | O; blank | Zero | Zero | `tool_wait_seconds` |
| idle | O; blank | Zero | Zero | `idle_seconds` |
| recovery / unmeasured | O; blank | Zero | Zero | `unmeasured_seconds` |

The original effective category remains in each row's status and in actuals.
Each row partitions elapsed time exactly. Central forecast seconds occur once
per genuinely engaged mode; an excluded row mapped to O does not consume O's
forecast. The complete central/high forecasts remain in actuals. Lane totals
must equal D+L+E, and concurrent helper work is never added.

Integer nanoseconds are authoritative. Ledger seconds retain all nine decimal
places without floating arithmetic. Decimal input conversion rejects fractions
of a nanosecond. Display minutes are explicitly rounded to twelve places and
never fed back into the ledger. The actuals include the raw/effective counts,
dispositions, effective segments, category/lane totals, input hashes, forecast,
protected floor and cumulative phase-three research/engaged totals including
the original setup row.

The audit replays saved clock events and requires exact agreement with raw
segments and the saved open/closed state. Dispositions must be nonoverlapping,
fit one closed original-mode segment and use boundaries matching saved clock
observations. No open interval is counted or extrapolated.

The original phase-three ledger's **435 bytes** must match baseline SHA256
`ecd61f0c3fe39d1ca6b670993c11b5e04665dc977590ba5f143b885cba29bcba`.
They remain an exact byte prefix after appending. The baseline-listed phase-two
ledger, paper, TODO and Gate D record must retain their original byte lengths
and hashes; the phase-two ledger must retain **1,125 rows**. The original setup
contributes **876.356952516 engaged seconds and zero research seconds**. No
phase-two time enters the phase-three research floor.

## Verification and limitations

Syntax compilation, a read-only preview and **28 pure/rejection checks passed**:
exact numeric roundtrip, all eight category partitions, invalid categories and
lanes, forecast placement, event/raw-state disagreement, disposition overlap
and original-mode mismatch, open/floor blockers, and exact agreement with
unchanged `clock.py` effective-segment nanosecond totals. Evidence:
[accounting_validation_attempt1.json](accounting_validation_attempt1.json),
SHA256 `4f6d1cf7c4dbd01258c4609f8945a08c390c8ddac69d767816d813971505d54b`.

The observed preview had **60.616045152967 closed research minutes** and
**68.516702072733 closed engaged minutes**. These are a dated partial preview,
not final actuals. Its blockers were `principal_clock_open` and
`protected_research_floor_not_met`. Hashes of the raw/helper/ledger inputs were
unchanged across the preview verification.

The same-model helper `accounting_safety_review` inspected arithmetic,
classification and preservation. Its orphan-attempt retry finding was fixed:
any nonempty `accounting_attempts` directory now blocks automatic finalization.
Existing append/actuals/lock artifacts and any unexpected ledger suffix also
block it. Prior attempts are never overwritten or silently reused.

The append path was source-reviewed but **not executed**, as requested. It uses
exclusive output creation, a lock, prepared records, append-only ledger I/O,
file/directory synchronization on POSIX and before/after checks. This is not a
cross-file atomic transaction. A crash or concurrent edit can leave a preserved
partial append or prepared attempt requiring manual reconciliation. A failure
during directory setup can leave only the lock, without an attempt-local failure
JSON. Do not delete blockers merely to rerun; inspect the preserved bytes and
record an explicit disposition first. The principal must keep the clock and
ledger quiescent while finalizing; an uncooperative external writer is not
prevented by this helper's advisory lock file.

Finally, arithmetic validation cannot establish whether a recorded interval
was substantively engaged. That judgment remains in the observed principal
records and their explicit conservative dispositions. The helper neither
creates research credit from artifact volume nor infers completion from time.
