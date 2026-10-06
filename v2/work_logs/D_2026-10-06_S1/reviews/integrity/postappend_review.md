# Gate D: final accounting and report-binding audit

**PASS, administrative attempt 1: 1,690 checks, no discrepancies.**
The [independent reconstruction](postappend_attempt1.json) checks the stopped
clock, every new ledger row, the exact historical prefix and carry, and the
current report's evidence bindings. Its [script](audit_postappend.py) does not
import or execute the accounting serializer, operate the clock, write the ledger,
or run scientific code.

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, separately assigned same-model internal
reviewer. This audit ran after the principal's **19:24:44.019801 UTC** accounting
cutoff. **Principal time credited by this review: zero.**

## Exact accounting result

| Mode or category | Observed minutes |
|---|---:|
| D | 0.706795120 |
| L | 1.849459743 |
| E | 0 |
| O | 13.649387557 |
| **Engaged total** | **16.205642420** |
| **Research total, D+L+E** | **2.556254863** |
| Recovery and unobserved, excluded | 4.486273499 |
| Concurrent reviewer credit | 0 |

The acceptance calculations use integer nanoseconds; the table is display
rounding. There are **972,338,545,187 engaged nanoseconds** and
**269,176,409,932 excluded nanoseconds**, partitioning the complete
**1,241,514,955,119-nanosecond** observed interval. All six raw segments and
effective rows agree with the transition events. The exclusion is contained
and nonoverlapping. The maximum credited observation gap is
**396.000520195 seconds**, below fifteen minutes.

The principal stopped research at **19:14:04.951632 UTC** and the full accounting
clock at **19:24:44.019801 UTC**. Administrative tail work after the latter,
including this review, is explicitly uncredited. Zero actual E is consistent
with the forecast's role as an estimate; no gate floor requires it. Forecast
seconds occur once on the first positive row of each actually used mode, and
the displayed forecast errors match exact actuals.

## Ledger and cumulative carry

All **1,117 prior rows / 273,391 bytes** match the entry Git ledger exactly.
The new append contains **six rows / 2,353 bytes**. The final ledger is
**1,123 rows / 275,744 bytes**, exactly the original prefix followed by that
append. The complete hashes are:

| Artifact | SHA256 |
|---|---|
| Historical prefix | `ac1bdbb521f4ffe09843850dfadcab509a0f6c20f35db20202a79e5efb8ec36c` |
| D append | `278884cbd0e2d43af08693b79c6dc3b16ea56708aa5a05059391e3c299df4dfb` |
| Final ledger | `9fa43939dba89818ce8690cec76aaff97a35d82ffa7079ae23e7ecc107a790b7` |

Forecast, baseline and F17 close use the identical inherited entry. The new
POST-B-1 close is:

`983.92840436211666666666666666666666666666666666667000000000000000000000000000000` minutes.

The rational reconstruction differs from that finite decimal only within its
last-place rounding bound. The inherited **0.000073995-second** historical
CSV/carry difference remains unchanged; no prior row or cumulative starting
value was silently adjusted. The sixteen-hour checkpoint remains completed
in F17. There are **936.071595637883333… minutes** to 1920, without automatic
authorization for that later programme.

The broader post-B package including consolidation now contains
**825.764044425133333… research minutes**, with
**R/X 50.729913/49.270087%**. Both lanes remain substantively represented, as
described in the [corrected entry review](entry_review.md). No concurrent time
is added to create those percentages.

## Current paper and preserved science

The current paper and its saved D snapshot both hash to
`c8f490ce94584fc93d27b759f1f524d5eeeb0d3885729d24db413cb4f5205c5d`.
The current D claim map hashes to
`979bd9aa2f1cef2c4ef50d44fabc6ccb1baddcd97ae6fb821145d80148030a08`.
Its **145 bindings** match current files. The original F17 map's **145 bindings**
also match, with its canonical report pointer resolved to the preserved F17
snapshot at the original epoch.

Both maps retain 42 claim groups. **F17-MATH-13 is the only changed claim**,
and it retains the same supporting evidence while clarifying that the strictly
positive attempt-price vectors themselves must be nonproportional. The other
41 claims transfer unchanged. Every one of the **973 accepted scientific
artifacts** and **288 Python files tracked at D entry** still matches its prior
byte count and SHA256. No experiment or scientific test was executed here.

The actuals and current report map retain **Gate D author decision PENDING**.
This review verifies the completed assessment's record; it does not enact the
author's phase decision or initiate further work.

## Attempts and limits

This final audit passed its first execution. The earlier entry audit's decimal
guard correction and review-chronology correction remain separately preserved;
their records are not overwritten by this successful result. The final audit's
own process wall time was **0.891 seconds**, with **53,568 KiB** peak process RSS.
These are audit process costs, not credited research minutes.

Arithmetic and hash checks establish consistency of the saved clocks, sources
and accounting. They do not independently observe historical cognition or
constitute external peer review. The current artifact binding and historical
evidence preservation are complete at this cutoff.

**Signed: ChatGPT (GPT-6 Astra Pro), Gate D integrity/accounting reviewer.**
