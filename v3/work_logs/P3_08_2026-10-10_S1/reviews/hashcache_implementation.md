# P3-08 stronger ordinary controls: direct fixed action and hashed cache

Stage: **DEVELOPMENT**. Contributor: ChatGPT (GPT-6 Astra Pro), same-model,
nonblind delegated implementer. This extension was authorized after the parent
inspected common_v1 development results. Its tests and input plan are
prospective to this extension, but it is not held out or a final challenge.
No additional principal-clock credit, commit, push, or main-cohort private
scoring was performed by this contributor.

## Source identities and API

| Artifact | Version / SHA256 |
| --- | --- |
| `v3/experiments/p308_ordinary.py` | v1.4; `fc98d9008bbf429e35a4b2fc71806ec006cc4f6fd416051c8fdaea2782f29bff` |
| `v3/experiments/p308_hashcache.py` | v1; `a668abfff6c4dd6c7d18cb186ed99bbb9c794713ce9f93e8a27470320b07a914` |
| Preserved `reviews/source_revisions/p308_ordinary_v1_3.py` | v1.3; `492897ba8eb84921068411c411188bd0057d299668904c31c3bf877d9db9e9af` |
| Unchanged `v3/experiments/p308_cnf.py` | v1.1; `46fd3e82505b9b6af9805836a562f2f78a3436384e0b3476c4f85cec355817a2` |
| `reviews/hashcache_input_plan.json` | `34dbe4c4eda2906f1dba63fd9217c5882131ce68f3b7e6e181efe9d774bc025a` |
| `reviews/hashcache_development_check.py` | `54df772de013637e0a4b08df0159fb1ca06f2bac18b9124f7c4bd4b023242825` |

`run_method(tape, "no_compute", fallback_action=0|1)` emits the supplied fixed
terminal action with unresolved hard knowledge. It calls no provider, experts,
numeric updater, or random selector. The same pre-computation half forecast,
terminal record, retained query key, and common output service are charged.
The explicit fixed action does not claim a checked true answer. Both fallback
values are separately executable; truth does not select one inside the policy.

`run_method(..., "exact_cache"|"ordinary_combo", cache_kind="linear"|"hashed")`
selects its cache prospectively. The default remains linear. Configuration
records the chosen cache and the hashed cache's bucket count. The existing
linear cache was not changed. The focused check establishes identical old
linear local records after removing only the new version/configuration fields.

`p308_hashcache.ExactHashCache(capacity=64, bucket_count=128)` supports
`lookup(query, meter)`, `remember(query, receipt, meter)`, `entries`, and
`retained_words`. Capacities 0 through 64 and fixed bucket arrays of 128 or 256
are admitted. The ordinary controller uses 128 buckets.

## Hash, equality, and receipt contract

The key contains the semantics version, source version, variable count, and
every canonical clause/literal. Request IDs are excluded from the mathematical
key and are rebound on every successful receipt. Each ASCII version label is
encoded with its length word, followed by zero-padded bytes in complete
64-bit words. Counts and signed literals use little-endian 64-bit words.
Clause lengths make the representation injective before hashing. No sorting,
canonical JSON conversion, Python dictionary, or Python object hash supplies
unpaid work.

All actual key words are read, encoded, and retained in the transient buffer
before SHA-256 runs. SHA-256 uses the already declared source-procurement
primitive: one unit per padded 64-byte input block. Its price is an abstract
shared service tariff, not an empirical CPU cost. Four digest words and two
buffer-release operations are also charged. For key size K words,
`paid_key_digest` costs `3K + 8 + floor((8K + 72)/64)` units. Bucket argument
validation and index extraction add four units. Query-format admission by the
cache remains separately charged through the unchanged CNF admission routine.

The shared helpers are:

```python
paid_key_digest(query, meter) -> bytes  # Exactly 32 bytes.
paid_digest_bucket(digest, meter, bucket_count=128) -> int
paid_key_bucket(query, meter, bucket_count=128) -> int
```

They require the bounded, canonical, immutable CNF Query established by the
owned caller's admission protocol. They perform exact-type/bounded-argument
checks and charge every encoding/hash step, without independently repeating
the whole format validation. A broker may reuse the same key-only hash and
then compare its own scope and generation in the bucket. Scope epoch and hard
generation are not in this mathematical hash, so a stale same-key entry stays
discoverable. The helpers import only CNF/common and standard modules; no
broker import creates a cycle.

Every cache lookup first follows its paid bucket chain and compares the full
digest. A digest match then requires a paid full-key equality check. A bucket
or digest collision alone cannot authorize an answer. Successful output is the
same immutable CNF Receipt class with provider
`bounded_cnf_hashed_exact_cache`, the current CNF service version, full claim
key, current request ID, binary checked answer, optional witness, and actual
operation invoice. The hash implementation version is separately bound by the
source closure. This is a trusted local cache of admitted provider receipts,
not an authentication service for externally forged objects.

## Bounded storage, FIFO, and failures

Paid setup creates the fixed bucket-head array, fixed slot array, and eight
header words. Each retained entry uses the same eight common header words as
the linear cache, plus four digest words and three bucket-link/index words,
plus its complete key. A slot cursor supplies FIFO order. Hits and duplicate
admission never refresh the cursor. Bucket chains retain previous/next indices,
so eviction needs no hidden list shift or uncharged hash recomputation.

Eviction pays the slot/header read, unlink plan, affected links, reference
release, retained-size subtraction, new entry, new head/slot/backlink, and
cursor/count/size writes. Releasing references is an explicit bounded metadata
operation; it does not claim a free linear scan or physical zeroing of key
words. The entire mutation bundle is prepaid atomically. A denied insertion
cannot remove an old entry. Earlier paid setup, validation, hashing, and search
costs remain spent. Lookup output and answer binding are charged before a
Receipt is returned; a denied output returns no answer object.

## Focused evidence and initial invoice comparison

The source-copied check passed all **eight groups**: canonical encoding/tariff
and bounds; receipt/content/version/request binding; actual bucket collisions
and test-only paid forced full-digest collisions; FIFO wraparound and duplicate
behavior; setup/hash/eviction/output failures; direct no-computation behavior;
old linear/default identity and controller integration; and the prospective
initial invoice comparison. The forced-collision wrapper still executes and
pays the normal hash before replacing its test digest. Distinct SAT/UNSAT keys
retain their own answers under the forced collision.

The comparison used the predeclared catalogue of 32 distinct three-variable
formulas, with two online passes, without main-cohort scoring or filtering.
Local bills include output, local setup, hashing, storage, and all provider
work. Common installed source procurement is separate and must include the new
hash-cache source equally in the parent's common_v2 closure.

| Method | Local units | Provider units | Provider attempts | Cache hits | Retained cache words |
| --- | ---: | ---: | ---: | ---: | ---: |
| Exact linear cache | 67,553 | 17,479 | 32 | 32 | 772 |
| Exact hashed cache | 46,899 | 17,479 | 32 | 32 | 1,192 |
| Fixed action 0, no computation | 9,160 | 0 | 0 | 0 | 0 |
| Fixed action 1, no computation | 9,160 | 0 | 0 | 0 | 0 |

The exact-cache terminal sequences and purchased-provider bills matched. The
hashed representation saves 20,654 local units on this declared 32-key tape,
while retaining 420 more cache words. This is an implementation/invoice result,
not a guarantee that hashing is always cheaper. On the separate four-request,
two-key integration tape, exact linear caching cost 2,325 units and hashing
2,886; the combined controller likewise increased from 5,696 to 6,257. The
fixed-array/hash overhead costs 561 additional units in both tiny cases.
Those adverse comparisons are retained.

Evidence is in `development/ordinary_hashcache_v1_4/`, including a copied full
transitive source snapshot, starting manifest, public syntax/invoice inputs,
provider test receipts, complete method runs, and source-bound result.
Result SHA256: `355098e40f7f859100e43f659a150763ab2bc100abfa35e3de1abb626a2772cf`.
The focused snapshot intentionally uses the already sealed common_v1 broker
while a separate contributor modifies its optional hard-state indexing. The
parent owns the combined common_v2 source closure, integration, main rerun,
private scoring, and economic interpretation. No executable changes in these
two delegated files remain pending.
