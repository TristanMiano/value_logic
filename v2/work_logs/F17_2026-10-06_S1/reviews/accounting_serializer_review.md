# F17 accounting serializer and entry integrity — pre-close review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, same-model delegated administrative
review. October 6, 2026. Principal concurrent time credit: **zero**.

**Static disposition: PASS for the corrected serializer below.** The
serializer has not been executed by this reviewer, the principal clock is
still open in O at the integrity snapshot, and no ledger has been appended.
Actual closure and the appended ledger require a separate post-append audit.

Reviewed serializer:
`v2/work_logs/F17_2026-10-06_S1/close_accounting.py`, SHA256
`355577bdcc20cb2d3c727b0ace1246ce1a6ace4baa05c74da682e19ca7cc7766`.

## Static accounting findings

| Obligation | Finding |
|---|---|
| Observed session boundaries | A stopped `clock_state.json`, first `start` and last `stop`, one runtime, strictly increasing monotonic timestamps and the complete transition/segment correspondence are required before writing. Check events do not create duplicate intervals. |
| Exact elapsed arithmetic | Segment differences and every split are integer nanoseconds. CSV seconds have exactly nine decimal places. New rows partition elapsed seconds into engaged, tool wait, idle and unmeasured components without replacing historical rows. |
| Exclusion treatment | Exclusions must use observed event boundaries, be contained in one raw segment and be pairwise nonoverlapping. Interval cuts assign each nanosecond to exactly one category. The whole uncertain O segment is excluded; the following paused recovery is a different excluded interval. |
| Research, overhead and lanes | D/L/E alone form research. O contributes engaged overhead with no R/X lane. Waiting and both recovery categories contribute no engaged time. Only credited D/L/E time enters R/X; research must equal the lane sum. Concurrent reviewer credit is zero. |
| Observation continuity | Credited pieces require observed boundary/check spacing no greater than 900 seconds. The existing excluded compaction segment remains excluded even though some work in it was observed. |
| Research and total cutoffs | The last raw D/L/E endpoint is recorded separately from total stop. In this session the last such segment is credited and ends at 17:31:52.451959 UTC; later O does not become research. |
| Prior ledger | Length, SHA256, row count and absence of previous F17 rows are checked before append. The serializer appends bytes to the existing ledger, then verifies `current == old + append` and the entire prior prefix byte-for-byte. It never reserializes the historical rows. |
| Forecast rows | Each mode receives its prospective forecast once, on its first positive engaged row. Excluded recovery rows labeled O receive no forecast merely for being O. All four modes are already present in the observed session. |
| Protected minimum | Forecast and TODO explicitly specify no F17 protected minimum. The serializer records `protected_minimum: null`; no D/E/research floor is borrowed from another task or manufactured. |
| POST-B-1 | Exact inherited entry is retained and the increment is derived from integer engaged nanoseconds. The remaining balance is `960 - close`; `checkpoint_reached` reports the actual crossing and no recurrence clock is reset. |
| Durable append and interruption visibility | Existing result names and changed ledger prefixes cause refusal before normal execution. The append is flushed/fsynced, reread and checked. A partial administrative failure would leave visible output and must be inspected rather than bypassed. |
| Final tail | The recorded administrative tail excludes later accounting checks, exact-value rendering, final links/status, commit/push/transfer and chat. This is explicit uncredited work, not an inferred elapsed interval. |

### Resolved precision issue

The first inspected serializer computed forecast-error decimals by subtracting
outside its 80-digit local Decimal context. That would have reduced the
precision of these descriptive residuals to Decimal's default 28 digits;
integer nanosecond totals and ledger rows were unaffected.

The principal corrected this before execution to:

```python
minutes(totals[mode] - forecast['central_minutes'][mode] * 60 * NS)
```

The subtraction now occurs exactly in integer nanoseconds before conversion
under `minutes`' 80-digit local context. The corrected line and complete
serializer hash above were verified. No finding remains open for the current
session. The serializer was neither edited nor imported/run by this reviewer.

## Independent current integrity result

The separate read-only checker
`reviews/accounting/check_integrity.py` completed with exit 0 on its corrected
administrative attempt. It does not import experiment code or execute tests,
training, evaluation or the accounting serializer.

| Entry evidence | Current result |
|---|---|
| F16 scientific inventory | **973/973 files** match recorded byte counts and SHA256 digests. |
| Python files tracked at F17 entry | **278/278 files** match entry byte counts and hashes. The entry Python path set also equals `git ls-tree` at `2e44ed1b711508d7ad451e1ca6272ff989deef81`. Newly created F17 scripts are outside this preservation set. |
| F14 freeze | Original manifest hash matches; all **34** registered file bindings match. |
| ND01 freeze | Original manifest hash matches; all **47** registered files and **five source preparations** match. |
| Original attempt directories | F15 and ND01 each still contain exactly `evaluation_attempt_1` and `preparation_attempt_1`, matching the prior integrity record. |
| Ledger before append | **1,105 rows; 269,074 bytes**, SHA256 `94c1b965f9ec1b9245ea65419c9d521e7c2712dc2eb4387125119426a508992d`. No F17 row exists. |
| POST-B-1 entry | `932.46514142531666666666666666666666666666666666667` minutes, exactly equal to Gate C's saved close. Remaining entry balance is `27.53485857468333333333333333333333333333333333333` minutes. |

The integrity result SHA256 is
`afe9427e59fb68bc8a065f44b48c71bca2c8a232dc78e4b7946ff06a8cf4ffb8`.
The successful external command took **534,576,661 observed nanoseconds**.
This process cost is not added to principal engaged minutes.

The clock inspection independently reconstructed the **11 closed segments**
through **17:31:52.451959 UTC**. It found 866,926,107,491 research ns,
534,180,506,838 O ns, 346,381,322,894 excluded uncertain ns and 25,850,110,568
paused-recovery ns. Closed engaged time is 1,401,106,614,329 ns; closed
elapsed time is 1,773,338,047,791 ns. The open O interval is deliberately not
included in this partial audit and cannot be used as the final session total.
R/X research totals are 699,152,744,436 and 167,773,363,055 ns, respectively.

## Administrative reader failures retained

One inline schema/ledger inspection contained an unmatched parenthesis and
failed before execution. The corrected read succeeded.

The first saved integrity-reader attempt then stopped before writing its
result because F14's `files` field is a dictionary while ND01's is a list.
The first source is preserved as `check_integrity_attempt1.py`, with
`attempt1_failure.json`. The corrected reader normalizes those existing
schemas without changing any source, then passes. Its exact command, return
code, outputs, source hash and observed elapsed time are in
`attempt2_command.json`. No scientific retry or artifact repair occurred.

These findings authorize no ledger append by the reviewer. The next review
will check the actual stopped clock, serialized actuals, append bytes and
unchanged historical prefix after the principal closes the session.
