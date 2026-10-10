# Final preservation audit

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls agent, October 10,
2026 UTC. Administrative observer only; zero principal or agent clock credit.

## Result

**PASS_WITH_DOCUMENTED_EXCEPTION**, observed at
`2026-10-10T21:41:43.265036+00:00`. One read-only observer execution compared
baseline object bytes and verified saved artifacts. It did not import or run
any worker, checker or oracle, change a preexisting file, update status or
accounting, commit, or push.

The base commit is `33c6d6795aac894bd3cf8575e44f1d6f38f6ae56`; Git independently
resolved its tree to `0dbec24dfc68172a31aaa4a524fd5d1f2c199b67`.

## Baseline preservation

The audit compared all **5,659 tracked base blobs**, representing
**393,402,873 bytes**, directly against their working-tree bytes using
`git cat-file --batch`. This was a literal chunk-by-chunk comparison, with
additional per-path SHA-256 records. All **5,654 protected paths are
byte-identical**. There are **no deletions, unexpected modifications or mode
changes**.

The only permitted content changes are `TODO_v3.md`, `v3/plan.v1.json`,
`v3/README.md`, `v3/claim_ledger.md` and `v3/time_ledger.csv`. At this scan, the
changed subset was `TODO_v3.md`, `v3/plan.v1.json` and `v3/time_ledger.csv`;
the other two permitted files still matched the base. This is a point-in-time
preservation result while the parent completes authorized status updates.

The baseline comparison includes **740 paths with the P3-08 session prefix**,
all unchanged. All other earlier source-bound files and experiments outside
the five named exceptions are covered by the same complete baseline scan.
The full 5,659-path evidence is `run/baseline_blobs.json`.

## Completed evidence seals

All four required completed runs have matching manifest and unit-log seals,
the exact declared row count, outcome counts matching their summaries, and
source copies equal to their declared hashes and current bound source bytes.
The audit also verified the worker source-record bytes and every referenced
packet file's digest and length.

| Directory | Records | Outcomes | Declared source copies | Referenced packet files |
|---|---:|---|---:|---:|
| primary_v5 | 317 | 29 references; 288 delivered | 9 | 531 |
| secondary_pruning_v1 | 148 | 144 delivered; 4 intended failures | 12 | 445 |
| actual_consumer_cap_v1 | 288 | 239 delivered; 49 failures | 15 | 458 |
| rational_service_v1_retry1 | 30 | 13 delivered; 17 expected failures | 12 | 30 |

There are 5,894 verified packet references across these directories. The
1,464 packet-file count is the sum across separate archives, not a claim that
all contents are distinct across archives. The scientific meaning of the
intended failures remains in the original contracts; this audit checks
preservation and recorded outcomes without rerunning those tests.

| Directory | Verified completed-unit SHA-256 |
|---|---|
| primary_v5 | `555d0af18e958053f06b14940e6a725d28514877191a0982d976c91eb210254e` |
| secondary_pruning_v1 | `76d3f28bf30edee6e19e5edbdff6a7bb0927032744dd54bf5bd57005c33f90b1` |
| actual_consumer_cap_v1 | `01e88137a200c02385f1039fb146083780bf66a76900dee62f67d655460ccd4f` |
| rational_service_v1_retry1 | `13dd3b33ca4dafbb287f9f2e61d452517eae42a6b5e7014fe855d20352e630e8` |

## Preserved original rational-run exception

The original `development/rational_service_v1` still contains **29 records**
and **143,295 bytes**, with unit-log digest
`df3e500eac31c649b9afa3fc285b3d5428ed157ced94e2a63c462ff6bc92f69f`.
Its unchanged summary declares **30 records** and digest
`82f71da539ad3231764b54e9652635b5c4eded73805b8f2f08a81e6d521d28e4`.
The mismatch therefore remains observable and is not accepted as completed
30-unit evidence.

The saved unit and summary copies under
`reviews/receiver_reconstruction/synthesis_review_v1` are byte-identical to
those originals. Its `rational_integrity_observation_v1.json` retains the
same observed and declared counts and digests. The original manifest and its
12 declared source copies also remain intact. This audit neither repairs the
original directory nor assigns a cause to the mismatch. The separate
`rational_service_v1_retry1` passes its own 30-unit seals as shown above.

## Final ledger prefix

The parent completed the append before this observer ran. The audit fetched
the baseline ledger directly from the base commit and verified that all
**179,501 baseline bytes**, including the header and **426 prior data rows**,
are an exact prefix of the current ledger.

The current ledger has **192,395 bytes** and **461 data rows**. Its **35 new
rows** all have task ID `R-P3-B-B`, preserve the 15-column header width and
follow the unchanged baseline CSV rows. This checks append preservation; it
does not change or independently assign any research time.

| Object | SHA-256 |
|---|---|
| Baseline time ledger | `16941e46242606e37232b2ee1f577a06737f100a5eae9f585afce897353faac2` |
| Current time ledger | `a9e1d458690b7b29790f71a7f86cb2f2987fad311991d160810af07758153e2a` |
| Appended byte suffix | `0b548602b69d1fb1aaf857c9fe9fef432920fba1420e3c79f0c4f91b991909e3` |

The unchanged header is:

```csv
task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status
```

## Audit evidence and reproduction

| File | SHA-256 |
|---|---|
| plan.md | `4abc2888b9218c31eaa0219181ffffa42ad7861e1e8edeabf01939d645b73f22` |
| audit.py | `4ee274d1d79c1df69a2aa3822f2753b62f43f2bcc098df43de0c33d9284dda72` |
| run/audit.json | `f1c22045106205d3c499a461ca3494113f7942dfd477c3ea757d8bf10a525e68` |
| run/baseline_blobs.json | `bec747c610190c312d7c69e51403111b1804d8a0cd8201b5dcd0b5f3356254b3` |
| run/files.sha256.json | `f7e6e7271367916d019b49eb75115c17c9a99c4880f6299906457a9e4234f8f7` |

Run from the repository root; choose a new output directory for a subsequent
observation because the reader refuses to overwrite a completed audit:

```bash
python -B v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/ordinary_bridge/final_preservation_v1/audit.py \
  --out v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/ordinary_bridge/final_preservation_v1/run
```

The optional `--ledger-only` mode can make a new, additive ledger-prefix
receipt without rereading the scientific archives. It was unnecessary for
this execution because the full scan began after the final append.
