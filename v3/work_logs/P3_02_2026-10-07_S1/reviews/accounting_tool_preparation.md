# P3-02 accounting-tool preparation

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated administrative work,
October 7, 2026 UTC. **PREPARED; not a task close, clock stop, ledger append,
actuals record, gate or additional research-time credit.**

Read the P3-01 `accounting.py` and `verify_close.py`, the current P3-02
baseline, forecast, raw clock/dispositions and progress records, and
`v3/RESEARCH_PROTOCOL.md`. P3-01 is retained rather than re-executed.

## Prepared files and exact boundary

The only executable additions are this session's `accounting.py` and
`verify_close.py`. They use the standard library and set
`sys.dont_write_bytecode=True`. Preparation used CPython **3.12.14** and
`python3 -B`. No old script or phase-two module is imported by the closing
verifier. One read-only preparation check imported the current P3-02 clock
module and called only its `effective_segments()` function.

At the last preparation check, these file versions were present:

| File | Bytes | SHA-256 |
|---|---:|---|
| `accounting.py` | 33,266 | `17d8d8b3f1273dfe42da2ac3de2cd416663f67d8ef7f93b72f7af140db73cbca` |
| `verify_close.py` | 20,653 | `9283345440e49640b4d503f23f122f139714b03c1e52abfeb984ae3bdb291cdc` |

These are preparation-version hashes, not a scientific freeze. The eventual
actuals will bind the versions that the principal actually reviews and uses.

## Accounting behavior

`preview` and its alias `snapshot` read stable file snapshots and return
JSON to stdout. They never modify a clock, ledger or result. Open intervals
receive zero credit, even when they contain recent check events. The saved
closed segments are reconstructed from the raw events; their exact equality
and the saved open/closed state are required. The current clock's effective
split semantics are reproduced with stronger checks on disposition IDs,
runtime, original mode, overlap and observed UTC/monotonic boundaries.

Raw clock events, raw segments, all raw dispositions, effective segments and
input hashes remain in the proposed/final accounting payload. Corrections
are applied once without editing their sources. No concurrent-agent duration,
progress snapshot, remaining forecast or executable run time is added to the
principal's intervals. Wait, idle, recovery and unmeasured modes are excluded
from research and total engaged time; O is included only in total engaged.

Integer nanoseconds are authoritative. CSV seconds are exact to nine decimal
places; minute and fraction displays are explicitly rounded to twelve places.
Signed forecast errors use a separate correct signed formatter. Forecasts are
compared with actual D/L/E/O and waits, with central/high research and engaged
sums reported separately. The original forecast and remaining-forecast history
are preserved. Historical progress is checked against the presently effective
intervals and never credited separately.

The protected test is actual task D+L+E of at least **90 minutes**. There are
no separate mode floors. Prior task credit, if any, is derived from the
immutable prefix and checked against the baseline. Phase cumulative research,
engaged time, the remaining **960-minute research floor**, and 240/480/960
checkpoint crossings and overshoots are calculated separately.

R/X totals and fractions are exact. A last-two-research-attempt window is
also reported against the 25% diagnostic. The script does not invent a new
definition of the protocol's cycles or fabricate an exception. It checks
that consecutive saved observations contain no more than fifteen closed
engaged minutes. Excluded portions are not counted as active time in this
cadence calculation.

Preservation checks require the prior v3 ledger prefix's exact byte count
and SHA-256 and its equality with the ledger in the recorded source commit.
Every old v3 file other than the four declared mutable control/ledger files
is checked against that source Git blob. The ledger gets its separate prefix
check; README/plan/claims are the current phase-three controls. Baseline
phase-two ledger, paper, TODO, accepted Gate D and root README hashes are
checked, and a tracked phase-two diff must be empty. New engaged UTC intervals
must not overlap prior ledger credit; their durations still come only from
matched same-runtime monotonic clocks.

## Finalization is explicit and was not invoked

The principal can inspect the current state with:

```text
python3 -B v3/work_logs/P3_02_2026-10-07_S1/accounting.py preview --summary
```

Only after completing the real protected research, stopping the principal
clock and reviewing the resulting snapshot can the principal invoke:

```text
python3 -B v3/work_logs/P3_02_2026-10-07_S1/accounting.py finalize
```

`finalize` refuses an open clock, an unmet floor, a cadence violation,
unaccounted stop/resume gaps, any existing suffix, existing actuals/append,
or a previous finalization attempt. It creates a durable exclusive lock and
prepared record, rechecks inputs/preservation, writes an append record, and
opens the ledger **for append only**. Size and byte checks surround the
append; the exact resulting bytes must match. On POSIX it also takes an
advisory ledger lock. It writes `actuals.json` only after the append and
postappend checks succeed. Existing files are never overwritten.

If finalization fails, the lock, prepared records and any written bytes stay
available for inspection. There is no automatic retry, truncation, replacement
or guessed recovery. Multiple runtimes or a stopped-clock gap require an
explicit separate disposition/accounting decision; they are not filled in as
research. The helper does not make a scientific-completion or gate decision.

The current accounting inputs include the closing tools themselves. Review
their final versions before finalization. A later edit to a bound input will
be exposed by closing verification rather than silently attributed to the
old actuals. Post-stop bookkeeping is explicitly uncredited.

## Read-only closing verifier

Preparation/snapshot command:

```text
python3 -B v3/work_logs/P3_02_2026-10-07_S1/verify_close.py preview --summary
```

After finalized accounting and synchronized records:

```text
python3 -B v3/work_logs/P3_02_2026-10-07_S1/verify_close.py close
```

The close mode verifies the exact current replay against both prepared and
final actuals; the single append, hashes, row count and finalization receipt;
and no remaining failure/lock marker. It requires P3-01 to stay complete,
P3-02 to be marked complete with its exact actuals pointer and research total,
the plan's cumulative/remaining totals to agree, and its last completed session
to point here. P3-A must remain an unattempted next pointer; later chunks/report
must remain unstarted, and no final freeze or exposure may be claimed. The
dedicated P3-N01 disposition must agree with the plan; the script does not
choose whether contribution support is warranted. It also requires the
P3-02 TODO checkbox, completed work-log header and `readiness_audit.md`.

The verifier parses new JSON, checks local linked inputs, and checks saved
development script/dependency hashes without rerunning the science. It accepts
the existing result formats and the announced companion format with
`stage="development"`, passed/failed outcome, explicit script path/hash and
dependency hashes. Prospective `constructive_audit_plan.json` remains a plan,
not an execution. Development progress JSONL is parsed and hashed as provenance,
with zero separate principal credit.

`final_validation.json` and `artifact_hashes.json` are generated outputs,
excluded from their own input scan. Their possible pending links are explicit;
the principal's final publication/manifest check must validate the eventual
files. Unicode/special heading anchors and the interpretation of lane cycles
remain explicit review boundaries. At preparation the sole conservative
anchor warning was the existing `S02 — Proper scoring rules` heading in
`v3/literature/00_orientation.md`; the exact heading was inspected, and no
source file was changed.

## What actually ran during preparation

The accounting preview passed. An initial verifier preview failed its
development-classification predicate because the just-added constructive
**plan** had been scanned as an executed result. The classifier was corrected
to distinguish that plan; it was not relabeled or edited. Subsequent verifier
previews returned **SNAPSHOT_VALID**, including the final prepared version.

Nine narrow in-memory checks passed for the accounting core: equality with
the actual clock's effective output; rejection of a raw elapsed mutation,
duplicate interval, duplicate disposition ID, unobserved correction anchor,
mixed runtime and subnanosecond quantity; correct signed-second rendering;
and comparison of the floor flag with the actual integer task total. Inputs
remained identical through that check. Later CLI/metadata/control checks were
inspected and the final versions parsed; no append/close branch was executed.

The last closed-record snapshot used in preparation contained
**3,330,104,741,032 research ns = 55.501745683867 display minutes**, with
**2,069,895,258,968 ns still required**. This was a read-only snapshot, not
extra ledger credit; the principal's live work can subsequently change it.
Its only finalization blockers were the open clock and unmet Research90.
The two-attempt R/X diagnostic passed, and no fifteen-minute cadence violation
was found in closed work.

At the last preservation check, the v3 ledger remained exactly its original
19,845-byte prefix with SHA-256
`4d871385e36f95dd35927f1ec70dd9d06164855bbf75b4b44c0344314351884d`.
`actuals.json`, `ledger_append.csv`, `accounting.finalize.lock`, and
`accounting_attempts/` were all absent. No clock stop, finalization, ledger
append, new completion record or scientific probe was performed here.
