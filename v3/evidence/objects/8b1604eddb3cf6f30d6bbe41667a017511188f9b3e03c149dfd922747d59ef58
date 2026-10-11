# Independent inspection of the rational-service integrity retry

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.

**Disposition: the separate retry is complete and internally consistent. The
original remains a retained 29-row partial record with an inconsistent summary;
the cause is unknown.** This is a same-model, nonblind DEVELOPMENT review after
exposure to the original summary, the integrity finding, and the retry outcomes.
It contributes zero principal research time and executes no worker, proof
checker, experiment runner, policy, or new scientific case.

The new standard-library [artifact reader](inspect_artifacts.py) performed
**2,093 observational checks with no failures**, recorded in
[run/results.json](run/results.json). These are independent file, JSON, hash,
accounting and record-comparison checks. The retry author's **302 assertions**
remain separately attributed to its execution; this review did not rerun them.
All 112 files read by the observer remained byte-identical at its final readback.
The original log's size, modification time, change time and inode also remained
identical during this inspection.

## 1. The two evidence records have different standing

| Item | Original `rational_service_v1` | Separate `rational_service_v1_retry1` |
|---|---|---|
| Present JSONL rows | 29 complete, parseable lines | 30 complete, parseable lines |
| Counted delivered / no-current-certificate outcomes | 12 / 17 | 13 / 17 |
| JSONL bytes | 143,295 | 149,862 |
| JSONL SHA-256 | `df3e500eac31c649b9afa3fc285b3d5428ed157ced94e2a63c462ff6bc92f69f` | `13dd3b33ca4dafbb287f9f2e61d452517eae42a6b5e7014fe855d20352e630e8` |
| Summary's declared rows | 30 | 30 |
| Summary's declared JSONL hash | `82f71da539ad3231764b54e9652635b5c4eded73805b8f2f08a81e6d521d28e4` | `13dd3b33ca4dafbb287f9f2e61d452517eae42a6b5e7014fe855d20352e630e8` |
| Present log agrees with summary | **No** | **Yes** |
| Missing planned key in present log | `O-ADD-PORTFOLIO`, request 5, `recovery_zero` | None |

The [original summary](../../../development/rational_service_v1/summary.json)
and [original log](../../../development/rational_service_v1/completed_units.jsonl)
must both remain preserved. Identifying the absent planned key follows from
the declared six-method, five-case order. It does **not** recover that missing
row's outcome, invoice, timing, state flags or other contents. This review does
not treat the original summary as evidence of the missing row.

The [retry declaration](../../../development/rational_integrity_retry_1.json)
was recorded at `2026-10-10T21:15:03.239383+00:00`, before the retry manifest's
preparation timestamp. It permits one unchanged retry of an evidence-integrity
failure, retains the original bytes, fixes the same algorithm, inputs and caps,
and gives the new run its own destination. The declaration is SHA-256
`d533f019ec4a2cb2d844f1ae6944661e70789984c258d9c8271ae2ec15fd97c3`.
This is the explicit later provenance amendment to the original contract's
instruction to retain unexpected outcomes without repair or retry.

The [retry summary](../../../development/rational_service_v1_retry1/summary.json)
is SHA-256
`a84d87b88f52019af3e57fdc32578d06d411cec0473d6e40ea72a18e2c3d147d`.
Its manifest digest, completed-log digest, 30-unit count, 13 deliveries and
17 failures all agree with the independently read files. Its recorded finish
time is `2026-10-10T21:15:29.099143+00:00`. The elapsed runtime is observer data,
not research-clock credit.

## 2. Source inspection does not explain the original loss

I inspected the frozen and matching current
[runner](../../../development/rational_service_v1_retry1/sources/v3/checks/05_certificate_delivery_run.py),
[scope audit](../../../development/rational_service_v1_retry1/sources/v3/work_logs/R_P3_B_B_2026-10-10_S1/development/rational_service_audit.py),
and service source, plus both saved transcription-reader versions. The following
source facts matter:

1. `Writer.__init__` requires a fresh output directory. `Writer.save` stores
   content-addressed packets, updates its in-memory counts, appends one canonical
   JSON line using `open('a')`, flushes, leaves the context manager, then checks
   source stability. Each append therefore finishes before the later summary
   routine is called on the ordinary successful path.
2. `Writer.finish` derives `units` and outcome counts from the in-memory objects,
   but derives `completed_units_sha256` by reading the current file. It writes
   `summary.json` separately. The rational audit invokes it after the fixed
   30-unit loop and the count assertion. Its exceptional path writes a failure
   summary and re-raises.
3. The audit gives the final hybrid recovery the same `deliver`, record,
   `writer.save`, and assertion sequence as every other case. There is no
   special final-row branch that deletes or omits its saved line.
4. The inspected runner and audit have no truncation, deletion, rename or
   replacement operation for `completed_units.jsonl`. The service opens source
   files for bounded reads during enrollment and does not write the observer
   log. The inspected transcription readers read the original or preserved
   JSONL bytes; their output paths are new review files.

There is no explicit `fsync` or final JSONL line-count readback in this writer.
Consequently, its in-memory count and printed PASS are not an independent
durability certificate for a later reader. The code's separately recorded
digest does expose the mismatch. Neither omission supplies a demonstrated
mechanism for this observed disappearance. I found **no concrete source defect
that explains the missing final row** in the inspected paths.

The original log was observed with modification time
`1791665499040113593` ns, change time `1791665501472080716` ns, inode `534652`,
and size 143,295 bytes. These are file metadata observations; they do not identify
an actor or establish the sequence of writes. The original source histories,
the inconsistent summary, and the structural reviewer's preserved 29-row copy
remain evidence of the discrepancy. The latter copy is byte-identical to the
present original log. The structural reviewer's initial provisional
reader-error interpretation is explicitly superseded by its saved
`rational_integrity_observation_v1.json`; this review adopts the observed
integrity mismatch, not that initial interpretation.

## 3. The retry keeps the declared experiment fixed

The independently checked [retry manifest](../../../development/rational_service_v1_retry1/manifest.json)
is SHA-256
`1111ed0c74b241f1a276a3861c5923c6287933e74c61a224192a488185ea3583`.
Its only field differences from the original manifest are the output argument
at `command[2]` and `prepared_utc`. In particular:

- All **12** declared captured files are present, with exact directory membership.
  Their hashes match the original capture, the retry declaration, the retry
  capture and current repository bytes. This includes the eight worker sources,
  the execution writer, the rational audit, its contract and the previously
  declared rational witness record.
- The installed worker source record has the same **eight** files and
  **197,956** source bytes. Each per-file length and digest matches the captured
  and current source. The service revision remains
  `rp3bb-certificate-service-v5`, SHA-256
  `b96cae82e0fe3f0f734671d57df81ac3a62350746f73228aef63c2f77bb1745f`.
- The exact five-case scope input file is unchanged at 11,022 bytes, SHA-256
  `9d54048d095a0452cffa16dbeb8a1b55a0e63ff5e1acde89347a1c823bc0eb1b`.
  The general fixture declaration also remains byte-identical; it is a separate
  writer artifact and does not substitute for these five audit inputs.
- The methods, fresh-recipient condition, no-old-domain setup, request order,
  request identifiers, normal budget **134,217,728**, denial budget **1,024**,
  failure reserve **1,024**, lack of a separate consumer cap, Python version and
  tariff are unchanged.

All **29** surviving original rows exactly match their corresponding retry
rows after omitting only `observed_wall_ns`. A recursive comparison found that
one timing field different in each pair and no other differences. This includes
the complete output string, status, error, invoice and every category count,
work counters, proof size, packet references, live and retained size fields,
current-receipt availability, stale-receipt list, and scientific-state flags.
This is stronger than matching aggregate totals, while still providing no
missing original row.

Both run directories contain the same **30** content-addressed packet files,
all with correct lengths and SHA-256 filenames. The original's 102 saved packet
references reach 29 distinct files. Its one currently unreferenced file is
`e9845ffd547c52bef93ba0f042c9438c031a84d0f3a277af0a3687b83dd42f95.json`.
The retry's 109 references reach all 30. The presence of that original orphaned
packet is recorded only as an inventory fact. It is not a substitute for a
complete original delivery row and is not used to infer its missing contents.

## 4. Receiving claims, invoices and failure behavior

For every retry row, I independently summed all stage/category counts and the
receiving-account subset defined by `Meter._consumer`: `receiver_*`, `terminal`,
`failure_terminal` and `common_source`. Both sums equal the saved invoice.
Every total stays within its prescribed account. Corresponding observed packet
byte totals agree exactly with their charged invoice categories. Success-output
blobs equal the public output strings, and source blobs equal the declared
installed source record.

The first request of each owned method pays the same **430,041** units in
`common_source`, including 197,956 program bytes, 197,956 hashing bytes, eight
length-probe bytes, and the 1,199-byte source record plus the saved event work.
Later requests do not recharge installed source. Failure eviction concerns the
scientific state; it does not reset the installed source flag in the inspected
service. This is the existing tariff convention, not a new discount introduced
for the retry.

Each delivered public output binds exactly the case's current frame record,
supplied witness, requested bound, current request ID and installed source
record. It states `NONEMPTY` and
`ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS`. All saved stale
receipt lists are empty, and current-receipt availability agrees with delivery.
Every failure records empty owned scientific state, the explicit
`NO_CURRENT_CERTIFICATE` payload, and the same **113**-unit failure footer:
111 output bytes, one delivery event and one state-eviction event.

These are source-supported checks of the recorded observations. They are not
new executions against endpoint state or a proof that arbitrary hidden state is
empty. The audit source shows the state and receipt observations are taken
directly from the owned session before the row is saved.

The complete retry's outcome matrix is:

| Case | P-REUSE | P-FRESH | ADD cold | ADD warm | Direct ordinary receiver | ADD–portfolio |
|---|---|---|---|---|---|---|
| Large negative constant | Delivered | Delivered | Evidence rational cap | Evidence rational cap | Delivered | Delivered |
| Large positive constant | Uncertified | Uncertified | Evidence rational cap | Evidence rational cap | Actual violating point | Uncertified |
| Large incumbent cutoff | Input rational cap | Input rational cap | Delivered | Delivered | Delivered | Input rational cap |
| Zero worker capacity | Paid resource failure | Paid resource failure | Paid resource failure | Paid resource failure | Paid resource failure | Paid resource failure |
| Recovery zero | Delivered | Delivered | Delivered | Delivered | Delivered | Delivered |

“Evidence rational cap” is the recorded `EvidenceLimit` with message
`Evidence rational component cap.` “Input rational cap” is the recorded
`ValueError` with message `Input rational exceeds 128-bit component cap.`
The positive case illustrates why a no-current-certificate result is not
uniformly a falsity diagnosis: two methods stop at their representation cap.
The direct ordinary receiver instead records an actual violating point, while
the native portfolio paths report an uncovered incumbent-sublevel point.

Every zero-capacity row costs exactly **113** total and receiving units, has no
packet references, reports `ResourceExhausted` at `coordination`, leaves no stale
current receipt and records an empty scientific state. The subsequently
delivered recovery rows are all present in the retry. Its final hybrid recovery
has total **71,704** units, receiving cost **40,158**, proof size **434** bytes,
request ID `rational-fragment-service-v1:5`, a current receipt, no stale receipt,
and no error. Those values are claims about this saved retry row only.

## 5. Claim and preservation guidance

The admissible statement is: **one unchanged, prospectively declared integrity
retry supplies a complete 30-unit source-bound DEVELOPMENT scope/failure
diagnostic with the stated acceptance, rejection, withdrawal and recovery
outcomes.** Its evidence is separately attributed to
`rational_service_v1_retry1`. The original remains a 29-unit record whose
summary does not validate against its current log.

This diagnostic does not join the primary or secondary cost-competition
populations, widen the accepted exact-rational fragment, prove generic
failure recovery, or give an economic win. It preserves the backend-specific
limits and the distinction between a true request rejected at a resource or
representation boundary and a false request with an observed counterexample.
No policy tuning, source repair, additional retry, status edit, final evaluation
or research-clock credit is part of this review.

The review source is SHA-256
`fc8d8f44b764a093b3ed8aa8021e054ee8559bb3b28252be1d9ef409c69a9682`
(19,004 bytes). Its complete observational output is SHA-256
`b8eb018ececd1ce0a1c4e6536425e2971f74b2bd80457de2b1552ea105fbb167`
(59,384 bytes). That output includes the complete source/input hash inventory,
all 59 surviving or retry row summaries, exact comparison paths, the unchanged
original metadata and the known integrity mismatch as an explicit retained
condition. Existing evidence was not rewritten.
