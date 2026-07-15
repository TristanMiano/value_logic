# Task 21 runtime diagnosis

Date: 2026-07-15  
Status: **final run paused; no endpoint adjudicated**

## 1. What happened

Attempt 1 used the frozen Task 20 runtime and failed after approximately 35
minutes with CPython 3.13.3's fatal `Executing a cache` evaluator state. It had
completed fitting and calibration and written 191 of 400 trace shards, but no
raw result. The failure and unread-artifact audit are recorded in
[`task21_failure_attempt1.md`](task21_failure_attempt1.md) and its JSON
companion.

The registered unread-infrastructure-failure exception was then used with the
same seeds, packages, source hashes, and command under CPython 3.13.14. The
replacement runtime passed the frozen preflight and reproduced both Task 20
smoke-model hashes exactly. Attempt 2 was stopped at the project author's
request after approximately 20 minutes because the total turn, including
attempt 1 and diagnosis, had exceeded one hour. At interruption, its model
archive existed, but calibration's fit marker, traces, and raw results did not.
The model archive SHA-256 was
`38a939225b373694c194015b3b18c4e4be1a2a67c30fa8f065408b476894a9e7`,
exactly matching attempt 1. No result metric from either attempt was read.

## 2. The registered workload is intrinsically large

The frozen runner performs all of the following in one process:

1. materialize 20,000 training worlds, containing 1.6 million probe rows;
2. fit 18 hyperparameter configurations for each of two arms, then fit two
   arms for each of eight final seeds: 52 neural fits in total;
3. allow up to 200 epochs per fit, with full validation over 320,000 rows every
   five epochs;
4. materialize 5,000 calibration worlds and run the same 400,000 rows through
   each structured model twice, once for the full and once for the center-only
   calibrator;
5. evaluate 5,000 confirmation worlds for each of eight fit seeds, yielding
   40,000 world-seed evaluations; and
6. compress 400 trace shards. Attempt 1's first 191 shards occupied 0.535 GiB,
   projecting to roughly 1.12 GiB for the complete trace set.

The sample sizes are not themselves a bug. The implementation makes them much
more expensive than necessary.

## 3. The dominant avoidable costs

Each world-seed evaluation reconstructs four panels:

| panel | rows per world |
|---|---:|
| ordinary probes | 80 |
| four-condition boundary panel | 320 |
| four-offset tolerance-transfer panel | 320 |
| three atoms for 40 requests | 120 |
| **total** | **840** |

For every one of the 40,000 world-seed evaluations, the current seed-outer
loop regenerates the world and sends all 840 feature records through the
recursive scorer firewall. This gives 33.6 million complete payload audits,
even though the world, reference values, static features, and firewall answers
are identical for all eight fit seeds.

The ablations also repeat the symbolic boundary at atom granularity. Each row
is decoded under the structured, center-only, and unaccepted-radius variants.
The confirmation therefore requests:

- 100.8 million `decode_structured` calls;
- 33.6 million cross-entropy decodes;
- 33.6 million self-confidence ablation decodes;
- 8 million request aggregations; and
- 320,000 small neural `predict` calls before counting calibration or training.

Most structured calls rebuild a binding record and rerun checks whose bundle,
schema, normalization, scorer hash, and variant are unchanged across many
atoms. Neural prediction is batched only within one world/panel, leaving Python
and object-construction overhead dominant.

## 4. Pilot-role profile

A post-interruption `cProfile` run evaluated 16 pilot world-seed records using
the same evaluation function. It created 16,815,030 calls in 5.37 profiled
seconds. The important cumulative entries were:

| operation | calls | cumulative profiled seconds |
|---|---:|---:|
| `_evaluate_one_world_seed` | 16 | 5.631 |
| `_safe_payload` | 13,440 | 3.153 |
| `validate_scorer_payload` | 13,440 | 3.050 |
| `_contains_forbidden_token` | 376,320 | 1.823 |
| `encode_probe` | 6,400 | 1.687 |
| `tolerance_transfer_cases` | 1,280 | 1.373 |
| `boundary_status_cases` | 1,280 | 1.318 |
| `decode_structured` | 40,320 | 1.302 |
| `_audit_nested` | 403,200 total/362,880 primitive | 1.096 |

The firewall alone consumed about 56% of the total cumulative profiled time.
`_contains_forbidden_token` repeatedly scans the full forbidden-token set for
every key and taint source; its generator expression executed 7,150,080 times
for only 16 world-seed evaluations. This enormous repeated bytecode workload
also makes the location of attempt 1's CPython evaluator failure unsurprising,
although it does not establish the exact upstream trigger.

## 5. Scientifically conservative repair

The registered sample sizes, worlds, seeds, targets, endpoints, ablations,
weights, and trace fields need not change. A versioned execution-only amendment
should instead:

1. checkpoint selection, final fits, and calibration separately, with hashes,
   elapsed times, and an explicit immutable-resume rule;
2. iterate by 100-world block rather than by seed, generate and firewall each
   static world record once, and reuse it for all eight frozen models;
3. batch neural prediction over whole blocks instead of one world at a time;
4. validate static payload schemas and immutable calibration bindings once per
   relevant schema/bundle/variant, retaining per-record dynamic checks only
   where a dynamic field can change the answer;
5. vectorize the scalar `K_3` interval decoder and reuse its one binding result
   across semantically identical ablation work; and
6. reuse the same structured raw prediction for full and center-only
   calibration rather than running the model twice.

Before another confirmation is released, the old and amended implementations
should be compared on pilot-role worlds for exact equality of every metric,
raw prediction, `K_3` value, margin, active mask, route, trace array, model hash,
and calibration record. A timed pilot-scale run should demonstrate a safe
upper bound. Because final payloads have already been generated, this repair
must receive a new implementation version and be disclosed as a protocol
deviation even if the scientific estimand is bit-for-bit unchanged.

## 6. Current disposition

Task 21 is not complete. `F35`, `F36`, calibration, architecture comparison,
and empirical system claims remain unadjudicated. The partial attempt-2 model
archive is retained locally and ignored by Git; it blocks accidental use of the
old guarded entry point. No further run should occur until the project author
chooses between the versioned execution-only repair above and abandoning the
frozen empirical study.
