# F17 independent postappend accounting review

**Disposition: PASS for numeric reconciliation, byte preservation, and source integrity.**

Contributor: **ChatGPT (GPT-6 Astra Pro)**, same-model internal reviewer. This is an independent reconstruction within the same assistant team, not an external review. All audit work occurred after the principal clock stopped and receives **zero additional credited minutes**. The audit neither imported nor executed the serializer, clock, experimental modules, scientific runners, or scientific tests. It did not alter the ledger.

## What reconciles

The saved append is exactly the suffix of the current ledger. Its prefix equals both the recorded baseline and the Git blob at F17 entry commit `2e44ed1b711508d7ad451e1ca6272ff989deef81` byte for byte. The prior **1,105 rows / 269,074 bytes** are unchanged; **12 rows / 4,317 bytes** were appended once, giving **1,117 rows / 273,391 bytes**.

| Artifact | SHA256 |
|---|---|
| Preserved prior ledger bytes | `94c1b965f9ec1b9245ea65419c9d521e7c2712dc2eb4387125119426a508992d` |
| Saved F17 append | `b11afc6a5c06937bbf0055a09d1edc705d3ac46806a167811c52d166265a717b` |
| Final ledger | `ac1bdbb521f4ffe09843850dfadcab509a0f6c20f35db20202a79e5efb8ec36c` |
| Corrected serializer reviewed before its execution | `355577bdcc20cb2d3c727b0ace1246ce1a6ace4baa05c74da682e19ca7cc7766` |

A fresh state-machine reconstruction from **23 clock events** exactly matches the **12 raw segments**, their notes, modes, lanes, and observed endpoints. Subtracting the one explicit exclusion and the separate recovery pause gives the exact effective partition below. The CSV reproduces each interval in integer nanoseconds, with no overlap, duplicated credit, or gap.

| Category | Exact nanoseconds |
|---|---:|
| D | 558,253,824,183 |
| L | 48,120,582,312 |
| E | 260,551,700,996 |
| O | 1,248,531,123,530 |
| Engaged D/L/E/O | 2,115,457,231,021 |
| Excluded uncertain segment | 346,381,322,894 |
| Excluded recovery pause | 25,850,110,568 |
| Tool wait | 0 |
| Total excluded | 372,231,433,462 |
| Total observed elapsed | 2,487,688,664,483 |

Research is **866,926,107,491 ns**, exactly the sum of **R = 699,152,744,436 ns** and **X = 167,773,363,055 ns**. The principal therefore records **35.257620517016666… engaged minutes**, including **14.448768458183333… research minutes**, while excluding **6.203857224366666… minutes**. Ellipses shorten display only; the JSON and integer-nanosecond table preserve the full accounting.

The accounting cutoff is **2026-10-06 17:43:46.802576 UTC**, monotonic **4,696,326,980,644**. The final credited research endpoint remains **17:31:52.451959 UTC**, monotonic **3,981,976,363,952**. Later administrative publication and audit work is explicitly uncredited. The largest credited observation gap is **259,691,860,611 ns**, below the stated 900-second maximum.

The original central forecasts appear exactly once: **O 3,000 s**, **D 2,700 s**, **E 600 s**, and **L 900 s**, on their first engaged row. They are absent from recovery rows and subsequent rows of the same mode. Mode residuals are computed from integer nanoseconds before decimal conversion; the pre-execution precision correction is preserved. Original central/high forecasts remain **120/240 engaged minutes**. F17 has **no protected minimum** and no additional concurrent-agent credit. Gate D remains unattempted.

All **eight `actuals.json` input hashes** match the actual closed-clock files and corrected serializer. The saved ledger-integrity record also matches the independently reconstructed values in full.

## Sixteen-hour checkpoint and later close

The declared complete report-content boundary is the actual `check` at **17:41:06.396478 UTC**, monotonic **4,535,920,882,592**. Clipping the reconstructed effective intervals at that tick yields **1,955,051,132,969 engaged ns**, or **32.584185549483333… F17 minutes**, and **965.049326974800… cumulative POST-B-1 minutes**. The checkpoint's event-prefix hash and the reviewed/delivered report hash both match.

The later close adds exactly **160,406,098,052 ns**, or **2.673434967533333… O minutes**, with no additional research or excluded time. Adding only F17's exact engaged interval to the inherited **932.465141425316666…** entry gives **967.722761942333333… cumulative minutes**. The inherited historical CSV rounding residual of **0.000073995 seconds** is retained, and no recurrence clock is reset.

**Timing-label qualification:** the earlier `check` at **17:37:08.018195 UTC** was already at **961.076355596266666… cumulative minutes**. The checkpoint is therefore the declared complete report-content boundary, not the first observed clock event above 960. TODO requires review at the first *chunk boundary*; a clock observation does not by itself prove a completed content chunk. The saved notes distinguish the earlier work-log/contribution preparation check from the later completed report/review/source-map boundary. This audit establishes the arithmetic and preserves both observations; it does not independently establish cognitive engagement or the semantic completion of a chunk.

## Audit attempts and decimal-display qualification

The first audit invocation exited **1** after the substantive byte and interval checks because its comparison oracle directly rounded the exact rational `960 - close` to 80 significant digits. The serializer instead subtracts the already rounded, 80-significant-digit declared cumulative close. The difference is only approximately **3.33 × 10⁻⁷⁸ minutes**, representing propagation of the declared decimal display's rounding; no integer nanoseconds or inherited carry were changed. The checkpoint overshoot has the same expected property.

The first source is retained as [check_postappend_attempt1.py](check_postappend_attempt1.py), and its actual command, exit status, traceback, and **77,639,229 ns** elapsed time are preserved in [postappend_command.json](postappend_command.json). The correction changed only the audit oracle: it verifies exact rational carry separately, compares derived displays with arithmetic on their documented rounded parent, and requires the resulting discrepancy to stay below one unit of that parent's 80-digit display.

The corrected invocation exited **0**, with **396 administrative checks passing**, in **69,496,057 ns**. Its command and outputs are retained in [postappend_attempt2_command.json](postappend_attempt2_command.json). These are accounting checks, not new scientific tests or an F15 retry. No serializer rerun or ledger repair was needed.

## Reproducible evidence

The read-only audit logic is [check_postappend.py](check_postappend.py); the complete results and exact source hashes are in [postappend_result.json](postappend_result.json). The script creates its result exclusively and refuses to overwrite it. Do not rerun it over the preserved result as though it were a scientific stage. Its recorded invocation used the current primary CPython runtime with `PYTHONDONTWRITEBYTECODE=1` and no experimental module imports.
