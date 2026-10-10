# Optional paid hard-key indexing: design and prospective bound

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration-review sub-agent,
October 10, 2026 UTC. **P3-08 DEVELOPMENT**. Implementation/self-check work;
separate same-model structural review requested. Agent cost/time unmeasured,
principal-clock credit zero. This note precedes the new executable probe.

## Source and compatibility contract

The captured broker is `p308-program-broker-v1.2`, SHA-256
`248642e00333f0939f2e0e41020c69879b2d5bcedacf7979f980583630ba3653`.
Its shared hash helper source is `p308-hashed-exact-cache-v1`, SHA-256
`a668abfff6c4dd6c7d18cb186ed99bbb9c794713ce9f93e8a27470320b07a914`.
The complete pre-change source and post-change closure are retained in
`source_before/` and `source_snapshot/`, with prospective `plan.json` and
`source_manifest.json`. Earlier broker failures and all older development
closures remain untouched.

`Contract.hard_index` is its last field, defaults to `"linear"`, and admits
exact strings `"linear"` or `"hashed"`. Existing positional contract calls
retain their meanings. The episode additionally exports `hard_enabled` and
`index_kind`; the contract and hard-state records expose their matching
index configuration. Both modes pay eight new output words for these
configuration records. The default linear operations otherwise retain
their previous order and tariff; this explicit eight-unit record charge is
the intended cost difference from the old broker source.

The hash implementation is specific to the admitted immutable CNF Query
format. The broker's generic linear service boundary remains available.
The new source dependency must be included in registry procurement; it is
not an unpriced optional import.

## Representation and semantic equivalence

There are 128 bucket heads. Each inserted hard entry also creates an
immutable two-word node `(entry_slot, previous_head)` and updates one head.
The append-only entry array remains the authoritative retained history.
Prepending a bucket node copies no existing chain. There is no eviction,
scope reset of bucket contents, digest equality shortcut, or shrinking of
historical capacity.

The helper hashes the canonical complete key: semantic/source versions,
variable count and all clauses/literals. It excludes request ID, scope epoch
and hard generation. Equal complete keys therefore receive the same bucket,
regardless of their requested identity or receipt chronology. Different keys
may collide arbitrarily, including at the complete digest. Every candidate
still pays for full-key equality and the original scope/generation binding;
only a current complete match supplies an answer.

Inductively, a bucket chain is exactly the reverse-chronological subsequence
of retained entries having that bucket number. The linear search visits all
retained entries in reverse chronology; its omitted entries in the hashed
search cannot have an equal complete key. Thus both searches encounter the
same matching entries in the same order and return the same checked,
conflicted, stale or unresolved state. This argument does not assume hash
collision resistance or a favorable bucket distribution.

On successful duplicate admission, no entry/node is appended. A conflicting
current receipt sets a conflict token for the active entry. Hashed mode uses
the bounded integer entry slot rather than another unpriced semantic-key
hash. Slots are never reused. After withdrawal, the old slot is stale before
its conflict token is examined. A newly admitted current-generation receipt
gets a fresh slot, so old conflicts do not silently revive or contaminate a
new current warrant. The existing linear conflict representation is retained.

Withdrawal keeps the existing epoch/generation semantics and fail-closed
broker ordering. Historical same-key entries remain discoverable as stale
because epoch/generation are outside the index hash. Returning to a prior
scope label does not restore its old generation. Newly admitted current
answers precede all historical matches in both search modes.

The key retention, new node words, entry-slot record and bucket-head update
are prepaid in one bundle before either the entry array or index changes.
A denied commit therefore cannot leave an entry without its bucket link,
or a bucket link naming an absent entry. A purchased receipt can still be
retained as paid evidence when admission fails, exactly as before.

Base expert computation, frozen weights, selected ticket, propensity, action
bit schedule, selected purchase and block update code are unchanged. On a
completed paired run the selected provider invoices, base coordinates and
live hard-corrected outputs should be identical across the two index kinds.
The hard lookup bill may differ and can change which restricted budgets
complete; no equality of completion at arbitrary small budgets is claimed.

## Paid operations

The shared helper charges exact query-type preflight, full canonical key
reads, canonical word encoding, scratch-buffer retention/release, digest
storage, SHA-256 padded input blocks, bounded bucket argument checks and
index extraction. HardState additionally charges:

* 4 configuration-validation units, 128 allocated bucket-head words and one
  retained bucket-count word at hashed initialization;
* one bucket-head read per lookup and five node/chain/slot units per visited
  candidate;
* the inherited scope comparison and complete semantic-key comparison for
  each candidate, with an additional one-unit collision continuation when
  the full key differs;
* one bounded conflict-slot read on a current full-key match;
* six extra commit units for a new node, its head, its retained slot and
  constant-size prepend control; the full key remains priced by the original
  `16+key_words` entry-retention charge;
* eight output units once per broker for the explicit configuration fields.

The abstract word tariff is not a claim about Python CPU or heap costs.
Bucket/entry reference manipulation is represented by the charged bounded
word operations; no growing chain is copied during insertion. Audit JSON
and source-bound test hashes remain separately identified harness work.

## Explicit all-path cap increment

Let Q be the largest complete public key size and K the maximum retained
entries in one successful epoch. The original cap uses

```text
12*(K+1)*(Q+32)
```

per position for the worst-case full-key search, in addition to the separate
service, numeric, advice and fixed-control allowances. A hashed lookup
visiting K entries costs at most K*(2Q+10) in candidate comparisons,
node steps and collision/flag handling, with bounded head/answer work.
There are at most three such lookups per position: before issue, selected
admission, and after close. Thus even total bucket collisions fit within
the retained scan allowance. No expected bucket occupancy is used in the
funding theorem.

The helper's fee for a Q-word key is

```math
H(Q)=3Q+\left\lfloor(8Q+72)/64\right\rfloor+12
\le4Q+16.
```

The code uses at most three hashes per position; allow four conservatively.
The added per-position allowance `16*Q+256` dominates four helper calls
and leaves 192 units for bounded head, slot, node and related control work.
The original search allowance covers all candidate-dependent extra work.
The fixed hashed initialization costs 133 units and is covered by an
additional 256 units, including when the hard override is disabled and its
allocated index is unused.

Therefore the new cap is the old expression plus eight configuration-output
units and, for `hard_index="hashed"`,

```text
256 + (T*(16*Q+256) if hard is enabled else 0).
```

The eight configuration units are added to both the actual bill and the cap
for linear mode too. Source procurement and reporting remain separate
funding obligations. The old sufficient `capacity>=quota` condition and the
provider-limit exclusion from all-path eligibility remain unchanged.

This cap is deliberately a worst-case guarantee; it may increase even when
actual hashed lookup is cheaper. The development probes will check paired
outputs/invoices, true bucket collisions, stale/conflict/capacity behavior,
denied commit integrity and exact-cap completion. They cannot replace this
shape-based argument with a selected cheap seed.
