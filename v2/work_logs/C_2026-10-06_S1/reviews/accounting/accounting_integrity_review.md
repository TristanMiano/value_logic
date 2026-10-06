# Gate C entry accounting and scientific-integrity review

**PASS for the reviewed historical accounting and saved-byte continuity.**
The final Gate C clock close and ledger append remain pending in this entry
snapshot. This is supporting evidence for the principal's Gate C
recommendation; the author retains the final continue/recurse decision.

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, separate accounting/integrity agent,
October 6, 2026. The principal supplied expected ledger and carry values. This
review independently recomputed the task and cycle totals from the preserved
CSV, checked its recorded monotonic endpoints, and directly hashed the saved
scientific files. Concurrent reviewer work contributes **zero** principal
engaged minutes. No experiment was prepared, evaluated, retrained or rerun.

## Source and method

Entry commit: `de7b456d08f383e72dfcabd278c183db324fdf16`.
The complete entry ledger is **265,648 bytes / 1,096 data rows**, identical to
that commit and SHA256:

`2ddbbff7ccbc4c76bd15f3c26a58273be562ba21f6967b9d1d87feab7958c8fa`.

The [historical timing report](historical_timing.json) uses exact decimal CSV
seconds and an 80-digit context for displayed minute ratios. It preserves
blank historic credits as unmeasured rather than treating a blank as evidence
of no work. No gate or planning time is back-credited to a numbered task.

All **358 post-B research-package rows** match the corresponding recorded
same-runtime monotonic endpoints and frequencies. Every row partitions its
elapsed amount exactly into engaged, waiting, idle and unmeasured amounts;
there were no serialization differences or invalid credits. The **262 rows
with positive engaged credit** have no overlapping UTC intervals. Every
historical session's largest adjacent recorded-clock gap is under 15 minutes;
the largest is F14's **773.904950483 seconds**. This checks recorded timing,
not continuous independent observation of historical cognition.

Six F14 rows share three recovery boundaries that a top-level-clock-only
reader misses. Two boundaries are explicitly nested inside its existing
`recovery_exclusion` events. The third is an existing same-runtime segment
boundary, corroborated by the recovery event's UTC label and exact excluded
duration. The report preserves this provenance for each endpoint rather than
pretending all were standalone events. No boundary was invented and no old
clock file was edited.

Gate A's **78,295-byte** source prefix retains SHA256
`baa3852d0e063ad6fa580d8be73236a5ec8575fbb8945956336faf204bf7a458`;
Gate B's **154,563-byte** source prefix retains SHA256
`3c2726ff685ef15c82817a0f9fac32fc99fc59fdd143f056304f9b71bcf741a5`.
This review recomputes their cycle mode/lane sums while retaining the existing
historical endpoint audits. It does not rerun their scientific checks or
rewrite their signed snapshots.

## Required floors and recurrence identity

Each floor is tested on its own task/attempt rows, with no pooled credit from
another task, recurrence, administration or concurrent agent. Recorded minute
values below are rounded for display; exact seconds determine the result.

| Work group | Protected requirement | Independently measured minutes | Finding |
|---|---|---:|---|
| N01, `N01-A1` | D+L60, evidence in both modes | 60.229666322 | Satisfied |
| N01 recurrence, `R-N01-01-C3` | Fresh D+L120 author exception | 120.540527580 | Satisfied |
| F11, `R-N01-01-C1` | E60 | 60.162454620 | Satisfied |
| F12, `R-N01-01-C2` | Selected fresh E60 | 60.919965818 | Satisfied |
| F13, `R-N01-01-F13-A` | D60 within Research90 | D60.496926722; Research90.192406988 | Both satisfied |
| C4, `R-N01-01-C4-A` | Research60 | 60.336816673 | Satisfied |
| F14, `F14-A` | Prospectively amended Research90 | 90.564634074 | Satisfied |
| F15, `F15-A` | E60 | 60.090886268 | Satisfied |
| F15-ND01, `F15-ND01-A1` | Fresh Research90 | 90.797983823 | Satisfied |
| F16, `F16-A1` | Fresh D60 and selected Research90 | D67.483484969; Research90.249177800 | Both satisfied |

F12 is checked against its selected **E60**, which is stronger than the original
roadmap's E45. F13 and F16 retain their additional selected Research90
obligations. N01's initial target selection, its C3 recurrence, and C4's
contribution reconsideration are distinct groups. ND01 is separate diagnostic
development, and contributes nothing to F15's E60 or F16's fresh review floor.
The historically named C1/C2/C3/C4 recurrence chunks are not Gate C attempts.

Older `actuals.json` mode values were rounded independently to six decimals.
Every mode total agrees within half of the displayed final decimal place;
summing those rounded values can differ slightly from first summing exact
CSV seconds. These display differences change no floor. In particular,
F16's exact **14.950668029-second** Research90 margin agrees with its final
independent audit and integer-nanosecond actuals.

## Cycle allocation, with scope stated explicitly

The binding prospective Cycle III allocation is **D35/L10/E55**, with R60/X40.
The required numbered sequence and the broader package answer different
accounting questions. Both are reported to avoid obscuring the cost of
recurrence and optional diagnostics.

| Scope, before Gate C work | Research minutes | D / L / E | R / X |
|---|---:|---|---|
| Cycle I, F01–F04 | 318.338391 | 64.802% / 18.959% / 16.239% | 62.995% / 37.005% |
| Cycle II, F05–F10 | 516.451560 | 80.113% / 8.714% / 11.174% | 60.955% / 39.045% |
| Required Cycle III, F11–F16 | **452.179526** | **36.764% / 7.436% / 55.800%** | **51.460% / 48.540%** |
| Broader post-B package: N01, C3, F11–F16, C4 and ND01 | **800.576702** | **46.333% / 11.057% / 42.610%** | **50.000896% / 49.999104%** |

Required F11–F16 modes are D166.240339546, L33.624708156 and E252.314477867
minutes. Their O credit is 64.778669729 minutes, giving 516.958195298 engaged
minutes. The broader package modes are D370.930779657, L88.523068869 and
E341.122853308, with O113.451751333 minutes. Gate C's own work is excluded
from these entry totals and must be appended separately.

The required implementation/evaluation sequence is close to the prospectively
deliberate E-heavy allocation. The broader package contains the substantial
author-selected target reconsideration and the later diagnostic and proof
work, so its higher D share is explained by concrete work rather than corrected
by retrospective relabeling. Literature credit concerns new comparison work;
reusing already checked sources did not earn it again. There is no reason to
add low-value computation or literature solely to hit the old percentages.

### Two-cycle reliable/exploratory requirement

| Consecutive-cycle interpretation | R / X combined | At least 25% each? |
|---|---|---|
| I + II | 61.732% / 38.268% | Yes |
| II + required III | 56.522% / 43.478% | Yes |
| II + broader III | 54.296% / 45.704% | Yes |

Both interpretations of Cycle III satisfy the rule without an emergency
exception. Reliable implementation, exact reconstruction and regression work
coexist with uncertain retention/compression, target selection, neural
extraction and stronger coherent-recovery attempts. Exploratory failures retain
their exploratory credit; a later null is not grounds to relabel them.

## Cumulative POST-B-1 clock

The authorized inherited Gate C entry is preserved:

- **914.02845440021666666666666666666666666666666666667 minutes**.
- Remaining to 960: **45.97154559978333333333333333333333333333333333333 minutes**.

The direct historical CSV sum is 54,841.707190018 seconds, or
914.0284531669666… minutes. The declared carry exceeds it by the already
disclosed **0.000073995 second (73.995 microseconds)**. This predates F16's
increment, has no floor significance, and is retained as a reconciliation
difference. Neither historical rows nor the authorized carry were reset.

If Gate C's credited D/L/E/O increment reaches the remaining 45.9715456 minutes,
the sixteen-hour checkpoint is due at this chunk boundary, with exact overshoot
reported. It is not triggered merely by wall time or parallel-agent work. If the
increment remains below it, preserve the remaining amount for the author's
next selected chunk.

## Frozen scientific evidence

The [direct hash-check report](scientific_hash_checks.json) independently reads
and hashes each registered file. No experiment module is imported, and no
stage or broad scientific suite is executed by this audit.

| Evidence | Finding |
|---|---|
| F14-v1 manifest | SHA256 `b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c`; all **34** registered files match |
| ND01 manifest | SHA256 `9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c`; all **47** registered files match |
| F16 scientific inventory | All **973** saved files match size and SHA256 |
| F15 run sidecars | **180/181** match; the known zero-byte primary retention aggregate is the sole exception |
| ND01 run sidecars | **103/103** match |
| Run attempt directories | Each retains only `preparation_attempt_1` and `evaluation_attempt_1` |

The separately saved F15 recovery has **15,833,616 bytes** and original
aggregate SHA256
`0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691`.
The damaged original and its sidecar remain unchanged under the existing
F15-ART-01 disposition. This review does not turn that exception into a clean
181/181 primary-file pass or regenerate any episode.

The F15 report retains SHA256
`333ef2b80b9108d288529d9bc0c7925c8c76471eb1a1ae4fc055d5d475341d74`;
the final ND01 report retains
`e1aff33a3b59c9dc0c53e530e3b1c6305969a1c073814069e2ab824e6880ac6a`.
The two older ND01 report-audit hashes continue to denote intermediate report
snapshots, as F16 already documented. Their mismatch with the final report is
not a newly changed scientific artifact.

## Gate C clock source and remaining closure check

Read the new principal `clock.py`, `baseline.json` and `forecast.json` without
operating that clock. Its mode/lane rules separate D/L/E from O, waiting and
recovery. It records integer nanoseconds, keeps an explicit open state, and
reports closed intervals separately. Gate C has **no protected floor**; its
central/high 60/120 engaged-minute forecasts are estimates, not completion
conditions. A final report should use integer totals rather than its float
minute display.

At closure, require a null state and final `stop`; reconstruct every raw
segment from observed events; validate positive, ordered and non-overlapping
exclusions contained in their claimed segments; split partial exclusions
without double-counting; preserve the exact entry ledger prefix; and compare
the appended rows and actuals with that reconstruction. The current convenience
`report` command alone does not check mutually overlapping exclusions or all
these closure invariants. The final audit will check them independently.

This audit finds no historical timing or saved-byte reason to block Gate C.
Scientific readiness and contribution support still require the principal's
criterion-by-criterion arguments. The author has explicitly reserved the final
decision, so this supporting PASS neither selects F17 nor constitutes an
author-accepted Gate C pass.

## Review execution and failures

The first audit-reader attempt stopped before writing report outputs because
it assumed every observed F14 boundary was a top-level clock event. The exact
source is retained as `audit_historical_accounting_integrity_attempt1.py`, with
`attempt1_diagnostics.json`. The corrected reader handles the existing explicit
recovery/segment schemas and completed on attempt two. It changes no source
clock, duration, credit, scientific file or assertion about engagement. Two
nonexistent guessed inspection paths (`integrity_audit.md` and F14's standalone
`recovery_exclusions.jsonl`) were also read unsuccessfully; the existing
integrity JSON and embedded recovery events supplied the intended evidence.

These are reporting/inspection failures, not experimental retries. The
machine-readable reports preserve exact totals, endpoint provenance, individual
file hashes and audit execution timestamps. No measurement of this delegated
process is added to the principal's ledger.

Signed: **ChatGPT (GPT-6 Astra Pro)**, separate Gate C accounting/integrity
reviewer. Same-model collaboration, not external human replication.
