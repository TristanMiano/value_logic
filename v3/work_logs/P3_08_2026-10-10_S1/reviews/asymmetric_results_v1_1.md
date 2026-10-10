# Normalized asymmetric stakes: DEVELOPMENT result

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-control implementer and
same-model nonblind analyst. Principal-clock credit: **0**. No policy source
was changed. No optional-only controller was added.

## Result and scope

The extension verifies the ordinary known-stakes decision algebra and its
units. All 12 raw `(FP,FN)=(1,3)` executions at twice the normalized resource
price reproduced the corresponding `(1/2,3/2)` actions, acquisitions,
numerical states, invoices, and resource totals. Every raw objective was
**exactly twice** its normalized objective. The asymmetric readout improves
realized weighted cost in one orientation and worsens it in the other.
Correct algebra does not establish accurate probabilities or a realized
decision guarantee. The combined controller also changes later acquisitions
and forecasts when its stakes change. These are scoped Q5/Q4 behavior and
units results, with ordinary expectation algebra as the reference service.
They do not supply a new probability-recovery theorem or broad superiority
claim. [Public checks](../development/asymmetric_v1_1/public_checks.json)
and [sealed scores](../development/asymmetric_v1_1/private/scores.json).

The original plan was saved before the first extension execution. The final
matrix contains 57 complete public records on the already exposed 64-query
`cold_mixed` tape: 45 fresh executions and 12 explicitly reused symmetric
records. The reused records match the source closure, tape, method, exact
invocation settings, source procurement invoice, and original record hashes.
They are not extra trials. The stochastic arms use seeds 11, 29, and 47;
deterministic exact and constant-action controls execute once per stake and
are separately repriced. The scoring table consequently has 54 normalized
economic rows. All 57 episodes completed the full horizon successfully.
[Plan](asymmetric_plan_v1.md), [run contract](../development/asymmetric_v1_1/run_contract.json),
and [public index](../development/asymmetric_v1_1/public_index.json).

All policies use a byte-identical copy of the sealed common_v2 source closure,
including ordinary controller v1.4. The same nine `CORE_SOURCES` are charged
at **48,274 common cold units per record**. Local totals below include the
controller, providers, checking, failed attempts, cache, output, and local
setup under the existing word-operation tariffs. The common source bill is
shown separately and included in every priced objective. This is an explicit
service tariff, not a claim about wall time. The new public seal preceded the
separate scoring process's access to the principal's already sealed reference
answers. No new private truth evaluation was needed.
[Source manifest](../development/asymmetric_v1_1/source_before.json),
[public seal](../development/asymmetric_v1_1/public_seal.json), and
[reference provenance](../development/asymmetric_v1_1/private/reference.json).

## Q5: stakes change the action readout without changing its evidence

For an issued fallible probability `q`, predicting one has modeled loss
`FP*(1-q)` and predicting zero has modeled loss `FN*q`. The ordinary controller
uses action one exactly when

`q > FP / (FP + FN)`.

A tie chooses zero. The two normalized asymmetric thresholds are therefore
`1/4` and `3/4`, against the symmetric `1/2`. These are the **base actions**;
a paid checked answer can subsequently determine the terminal action. Every
row passed the exact threshold check. With known positive stakes, either
appropriate expected-action loss also algebraically recovers `q`, such as
`q = expected_loss(action_zero)/FN`. This extension verifies the use and
normalization of that existing identity, rather than claiming it is novel.
[Frozen ordinary source](../development/asymmetric_v1_1/source/v3/experiments/p308_ordinary.py)
and [public checks](../development/asymmetric_v1_1/public_checks.json).

Within `probability_cost`, each seed has identical selected queries, 16 paid
labels, provider invoices, block updates, numeric weights, and issued
probabilities under all three stake settings and both resource prices. Its
local bill is identical across those settings; the mean is 696,761 units.
This isolates the effect of the changed action readout. The following values
are means over the three named seeds. The final column reprices the already
saved symmetric **terminal actions** at the new stakes; it does not run or
train another policy.

| `(FP,FN)` | Mean terminal FP | Mean terminal FN | Actual weighted task loss | Symmetric actions at these stakes |
|---|---:|---:|---:|---:|
| `(1/2,3/2)` | 14 | 0 | 7 | 23/2 |
| `(1,1)` | 4 | 19/3 | 31/3 | 31/3 |
| `(3/2,1/2)` | 0 | 23 | 23/2 | 55/6 |

The low-FP readout reduces realized task loss by `9/2`. The high-FP readout
increases it by `7/3`. Both conclusions apply at either resource price because
the paired resource totals also agree. The corresponding changes in terminal
actions across seeds are `(13,14,22)` and `(23,23,16)`. Issued Brier is identical
under all stake settings: its three-seed mean is
`45026266891/4294967296`. Thus an unchanged forecast diagnostic accompanies
material, sometimes adverse, changes in the task loss.
[Scores](../development/asymmetric_v1_1/private/scores.json) and
[exact post-score repricing analysis](../development/asymmetric_v1_1/analysis/readout_and_acquisition.json).

The raw scale checks do more than divide a reported final loss. They supply
raw `(1,3)` **and resource price `2*lambda` to the executing policy**. For
fixed resource use `C`, this gives

`J_raw = FP_raw*FP_count + FN_raw*FN_count + 2*lambda*C = 2*J_normalized`.

All 12 observed resource differences were zero, so this equality held exactly.
The plan also specified the general accounting residual
`J_raw - 2*J_normalized = 2*lambda*(C_raw-C_normalized)` if different bounded
arithmetic word costs had arisen. They did not arise in these records.
[Homogeneity checks in scores](../development/asymmetric_v1_1/private/scores.json).

## Q4: changed prices lead to new paid information paths

At resource price zero, the combined controller obtains a checked terminal
answer for every row under all three stake settings. For a given seed its
invoice sequence, numerical path, and terminal actions agree across stakes.
The mean local bill is 2,405,848 units, with `250/3` provider attempts: 56
successful calls, 8 later cache hits, and `82/3` failed capped attempts. The
failed attempts remain charged. Pure exact DPLL obtains the same zero task
loss with 64 successful provider calls and 2,009,348 local units. At zero
resource price both have objective zero. These totals do not equate an
attempt with a purchased label. [Scores](../development/asymmetric_v1_1/private/scores.json)
and [full public records](../development/asymmetric_v1_1/public_records.jsonl.gz).

At resource price `1/10000`, stakes alter the combination's optional
acquisitions. The table again reports means over three seeds; the update
count includes labels reused from the controller's paid cache.

| `(FP,FN)` | Weighted task loss | Provider attempts | Failed attempts | Feedback updates | Local units |
|---|---:|---:|---:|---:|---:|
| `(1/2,3/2)` | 10/3 | 65/3 | 0 | 26 | 2453605/3 |
| `(1,1)` | 14/3 | 68/3 | 1/3 | 26 | 823095 |
| `(3/2,1/2)` | 23/6 | 68/3 | 1 | 76/3 | 825637 |

Equal aggregate attempt counts do not imply equal information. All six
asymmetric-versus-symmetric comparisons at this nonzero resource price have
different provider invoice sequences. The low-FP runs change `(28,24,28)`
later base forecasts across seeds; the high-FP runs change `(24,12,40)`.
The executions therefore include fresh, policy-dependent acquisition and
online updating. They cannot be treated as mere repricing of a fixed
transcript or as an isolated readout experiment.
[Behavior comparisons in scores](../development/asymmetric_v1_1/private/scores.json).

Compared with repricing the symmetric combined transcript, the low-FP
execution raises mean task loss by one, lowers mean local units by `15680/3`,
and raises mean objective by `179/375`. The high-FP execution lowers mean task
loss by `19/6`, raises mean local units by 2,542, and lowers mean objective by
`43687/15000`. These comparisons describe consequences of new paths; they
are not guarantees of improved computation selection. The unchanged controller
still forces a full checked purchase at each selected unknown query. Its
optional choice uses fallible public-shape or own past provider costs and is
not an optimized value-of-computation controller.
[Post-score analysis](../development/asymmetric_v1_1/analysis/readout_and_acquisition.json)
and [frozen source](../development/asymmetric_v1_1/source/v3/experiments/p308_ordinary.py).

## Economic context and limits

At resource price `1/10000`, the complete objective includes each record's
48,274 common source units. The following are recorded means, rounded to six
decimal places only for display. The exact rationals are retained in scores.
Both supplied constant-action endpoints remain visible; no evaluation-selected
endpoint is silently installed as a new policy.

| Method | `(1/2,3/2)` | `(1,1)` | `(3/2,1/2)` |
|---|---:|---:|---:|
| Probability to cost | 81.503500 | 84.836833 | 86.003500 |
| Combined, hashed cache | 89.947567 | 91.803567 | 91.224433 |
| Exact DPLL | 205.762200 | 205.762200 | 205.762200 |
| Supplied constant action 0 | 55.781200 | 39.281200 | 22.781200 |
| Supplied constant action 1 | 21.781200 | 37.281200 | 52.781200 |

At price zero the exact and combined arms have zero task loss in every stake
orientation. At price `1/10000`, a supplied no-compute endpoint has the smallest
recorded objective in each orientation of this declared comparison. The table
does not infer a deployable selector from those minima. Stronger caching
comparisons remain in common_v2; this small extension is not a replacement for
them. [Economic aggregates](../development/asymmetric_v1_1/private/scores.json).

The tape and earlier v1/v2 outcomes were exposed during development before
this extension was planned. Seeds, normalized references, raw scale pairs,
and reused records are not independent evidence for a coverage or population
claim. Fresh runs start with the same source library and their own empty
online state; no offline retraining or cross-run learned-state reuse occurs.
For the combined policy, new supplied stakes can change its own training
history. For fixed controls, subsequent evaluation at another resource price
is explicitly fixed-record repricing. Earlier issued Brier remains distinct
from terminal decisions after paid computation.

## Preserved harness failure and source bindings

The first public attempt completed all 57 policy episodes, then its comparison
of fresh tuple claim keys with reused JSON list claim keys failed. Replaying
the complete saved wire records passed every declared public check. That
attempt, its original source, and its public-only failure record remain under
`development/asymmetric_v1`. No private scoring occurred for that attempt.
The v1.1 amendment normalizes harness comparisons to the exact saved JSON
representation and repeats the original matrix in a new directory. It changes
no policy, price, seed, input, or tariff.
The repeated final public-record archive is byte-identical to the first
attempt's complete archive (SHA-256
`4c56983e46fc93094b2c2035894a9e519821787bf42a77e236956a870c003a88`),
confirming that the harness repair did not change any policy record.
[Amendment](asymmetric_harness_amendment_v1_1.md) and
[failure record](../development/asymmetric_v1/failed_check_record.json).

| Artifact | SHA-256 |
|---|---|
| Original pre-execution plan | `b0f935ad2315acd24ec527dfd351224ebcda93f3899bffc4b3f2ade26019771c` |
| v1.1 harness amendment | `201652d4e7e952d721110219ef88d7c1bfb0e01d9cdbeba6cf1638cad071cfb3` |
| Executed v1.1 harness | `2eb0ac300d87a87721cad8b3b0b6654e754b9e27d5f8b5b333a76ae9b1dc9067` |
| Unchanged ordinary controller v1.4 | `fc98d9008bbf429e35a4b2fc71806ec006cc4f6fd416051c8fdaea2782f29bff` |
| Copied common_v2 runner | `01b468abb46cf9f1cb0e9143a9a64e811e18ffecce8de6c4d51d92e7373a4c99` |
| Final public seal | `0919dec1c5ea9d2a65d2d5cbb68e545aec44aa1e837a59b8cfaf79f38c75ff1e` |
| Sealed scores | `0197241d3df4576303cd226cab56abd015f5217702fa726514e54bbd82b7b454` |
| Private score seal | `8abe1863b82eabdf4bb4ee137c909ae1869c6a641784b7d1c00560dd77ffac72` |
| Derived readout/acquisition analysis | `aad851d09cf3c85e7c5643ee2733ddbca033e1c4e796a677e2277edded249eae` |

The full transitive source hashes are retained in the final public manifest
and seal. All statements here are bound to those records and the stated
development scope.
