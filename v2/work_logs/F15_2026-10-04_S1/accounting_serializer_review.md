# F15 accounting serializer: static preparation review

Contributor: delegated ChatGPT (GPT-6 Astra Pro), execution audit, with an independent delegated static code review. This administrative work is outside the frozen experiment and adds no minutes to the principal's engaged clock.

Reviewed artifact: `finalize_accounting.py`, final static-review SHA256 `700193fec86846fd730654a10e3017e619092d2fb79d7615b2c64f5ce35ed24f`, 26,519 bytes. The file was prepared and inspected, then parsed with `ast.parse`. It was **not imported, executed, or dry-run**. No clock command was issued. The accounting cutoff and E60 satisfaction remain for the principal to establish.

## Static verdict

No blocking defect was found in the reviewed serializer. The independent reviewer approved the preceding version (`a43d7f1d87d76cb6a91d308f869eb59b2184c3c66dd0d27973af6213ff9dd420`) and suggested binding recovery metadata to its raw segment. The final version adds that check and passes another AST parse. This is source-level review, not a claim that final accounting has run successfully.

The reviewed code:

- Requires `clock_state.json` to contain `null`, reconstructs raw segments from clock transitions, and requires the final transition to be an explicit stop. `check` events do not create segments. Segment boundaries must be contiguous and nonoverlapping in monotonic time, with matching adjacent UTC boundaries.
- Reads the current `adjustments.jsonl`, `recovery_exclusions.jsonl`, and `mode_reclassifications.jsonl` at execution time. The three recovery records present during review include the whole 425.083064484-second segment beginning at monotonic timestamp 26351400554989; no exclusion count is hardcoded.
- Binds exclusions to existing raw segments, binds recovery classification and UTC boundaries to those segments, and applies mode/lane changes before assigning engaged credit. The raw E/X segment conservatively reclassified as O receives no E credit. The explicit artifact-recovery wait segment is classified as recovery.
- Uses integer monotonic nanoseconds for credited durations. Decimal text is normalized only to that observed resolution, with any nonzero normalization delta recorded. The known binary-float serialization excess of 0.00000000000004 seconds in one recovery record is represented explicitly rather than becoming a substantive negative duration.
- Checks exact per-row and aggregate conservation, research lane totals, and **at least 3,600,000,000,000 nanoseconds of adjusted E time**. D, L, O, wait, recovery, parallel agents, and unobserved gaps cannot substitute for the E60 floor.
- Verifies immutable forecast bytes and preserves the original D10/L0/E90/O20 central forecast, D20/L10/E180/O30 high forecast, 5/20-minute waits, R/X 60/40 allocation, source revision `5388a3f9b0f18ad4f4e33d7e0cd04ea38f03e43e`, POST-B-1 entry 636.727190 minutes, inherited eight-hour overshoot 54.976816 minutes, and 960-minute checkpoint.
- Requires the exact historical ledger: 203,501 bytes, SHA256 `7f777f89e0aff82d58752d0b1774c30e015fe9f3dbbf4faa1caae9b35c49988f`. A separate read-only inspection confirmed 906 prior data rows, all with the expected 15 columns, and no F15 rows. Historical mixed line endings are preserved because the prior bytes are never serialized again.
- Writes a durable, exclusive `finalization_intent.json` containing exact append bytes and planned old/new hashes. It then appends one row per raw segment under an advisory file lock and checks the full resulting byte string against the exact old prefix plus the planned append. `actuals.json`, `ledger_integrity.json`, and all SHA256 sidecars are exclusive, flushed, fsynced, and reread. Existing outputs or F15 rows cause refusal.
- Rechecks raw inputs before and after serialization. The raw records remain unchanged. Document synchronization, ledger administration, commit/push handling, and the response after cutoff are expressly uncredited.

## Use after the principal's cutoff

Both commands below require the principal to have explicitly stopped its clock after the adjusted E floor is met. They have not been run by this audit:

```sh
python v2/work_logs/F15_2026-10-04_S1/finalize_accounting.py --dry-run
python v2/work_logs/F15_2026-10-04_S1/finalize_accounting.py
```

The first performs validation without writing. The second is a one-shot append and output operation. If serialization is interrupted after an intent or ledger append exists, preserve that evidence and inspect its exact old/new hashes before recovery; do not delete the intent or blindly rerun. The serializer does not edit reports or declare a scientific/contribution gate pass. F16 and Gates C/D remain outside its scope.
