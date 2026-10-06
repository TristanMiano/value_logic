
## Recovery at 2026-10-05 22:16 UTC

The current D interval from 22:12:07.795006 to 22:16:28.222283 UTC was conservatively excluded in full (260.427277521 seconds) because it crossed automatic context compaction and reconstruction of working state. Existing artifacts, clocks and agent reports were preserved; no F16 clock was restarted. A read-only inspection initially used the nonexistent name `clock_events.jsonl`; the actual append-only clock file is `clocks.jsonl`. No source or experiment was affected.

- Recovery at 2026-10-05T23:32:53.988871+00:00: excluded the entire unobserved L interval from 2026-10-05T23:27:54.524048+00:00 (299.464823491 seconds). Closed work remains credited; concurrent reviewers add no time.

## Final administrative recovery at 2026-10-06 00:09 UTC

The recorded O interval was split at its actual 00:07:27.579973 check. The following 149.691184051 seconds through the observed 00:09:57.271157 recovery pause are excluded as unobserved recovery, using an append-only O-to-recovery transfer. Measured administrative work before the check is preserved. The subsequent paused recovery inspection is excluded separately. `close_accounting.py` now accepts this observed partial recovery transfer and records it as unmeasured recovery, not tool wait. No research time, raw timestamp, scientific attempt, prior ledger entry or frozen artifact was changed.
