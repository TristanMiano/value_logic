> **Portable display copy — notation only.**
>
> Original: [v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/hard_hash_cap_review.md](../../../reviews/reporting_independent/hard_hash_cap_review.md)  
> Original SHA-256: `5f9527bbebde4270302ec872e9319edf3cbd6ab66a3b02470b74a7ace17c1ea3`.
>
> Generated with the unchanged math guard's `transform(protect=True)`,
> plus relocation of relative links to their original destinations.
> The original scientific document remains unchanged. This is a source-notation
> check, with no live-render or new mathematical validation claim.

# Independent source-bound review of the optional hard hash index

Disposition: **PASS; no semantic or funding-cap blocker found in the reviewed source.** This is a same-model, nonblind static reconstruction, separate from the implementation agent's nine execution probes. It adds no principal time credit. It does not claim a physical CPU or heap bound.

The reviewed broker is `v3/experiments/p308_broker.py`, version `p308-broker-v1.2`, SHA-256 `248642e00333f0939f2e0e41020c69879b2d5bcedacf7979f980583630ba3653` (32,569 bytes). The new direct dependency is `v3/experiments/p308_hashcache.py`, SHA-256 `a668abfff6c4dd6c7d18cb186ed99bbb9c794713ce9f93e8a27470320b07a914` (11,957 bytes). The implementation agent preserved its closure and design in `../hard_hash_index/source_manifest.json`, `source_before`, and `design_and_cap.md`.

## Exact-answer semantics

The optional index has 128 fixed bucket heads. Newest-first immutable linked nodes contain entry slots and predecessor heads; the authoritative entry list is retained for audit. The bucket key includes the complete semantic query key. It excludes epoch and generation deliberately: old occurrences of the same key must remain reachable so a lookup can distinguish stale evidence from absence. Every candidate still receives a full key comparison followed by scope and generation checks. A digest or bucket collision alone never authorizes a checked answer.

For any query, its bucket traversal is the reverse-chronological subsequence of the original linear traversal containing all possible exact-key matches. Entries omitted from that subsequence cannot have the same key. Returning to an older scope does not restore its old generation. Conflict membership uses stable, never-reused integer slots in the hashed branch and is checked only after the current scope and generation match. A newly found conflict, stale return, or denied admission retains the existing warrant rules.

Admission reuses the bucket produced by its lookup. The linked-node/head update is included in the same admitted bundle as the new entry, so failure before that charge cannot append an unindexed entry or publish an index pointing to a missing entry. No hidden growing-list copy is needed. The old linear mode remains the default; its intentional common change is an eight-unit metadata-output obligation and the declared configuration fields.

## Independent cost reconstruction

Let $`Q`$ be the declared maximum complete query-key word count and $`K`$ the maximum retained entries in a successful fixed-epoch episode. The helper's key-digest and bucket work is bounded by

```math
H(Q)=3Q+\left\lfloor\frac{8Q+72}{64}\right\rfloor+12\leq4Q+16.
```

This includes the bounded query type check, key-word reads, encoding and temporary retention, digest words and compression blocks, scratch release, bucket validation and extraction. The finite encoder uses fixed-width signed/integer words and length-prefixed source/version strings; full key checks remain necessary even for a collision of the full digest.

There are at most three full-key hashes per issued position: the issuance lookup, selected-answer admission lookup when selected, and post-close lookup. Insertion reuses its existing bucket. The funding expression allows four hashes, costing at most $`16Q+64`$, leaving 192 units within the declared per-position increment $`16Q+256`$ for fixed reads and index updates. Initialization adds 133 units (128 heads plus configuration/count work), below the declared 256-unit increment. This initialization cost is covered even when hard reuse is disabled.

In the all-collision case, each candidate traversal costs at most $`2Q+10`$: five chain/slot units, four scope units, at most $`2Q`$ full-key comparison words, and one collision/conflict unit. Three full scans therefore cost at most $`3K(2Q+10)`$. The retained preexisting scan allowance satisfies

```math
12(K+1)(Q+32)-3K$2Q+10$
=6KQ+354K+12Q+384>0.
```

It covers the candidate cost even when every retained entry occupies the same bucket. The remaining fixed heads, scope reads, checked-answer reads and insertion work fit in the above 192-unit remainder. The common output increment is eight units. Thus adding eight to the old cap, plus 256 initialization and $`T(16Q+256)`$ when hashed hard reuse is active, is conservative for the declared finite episode. This reconstruction does not extend the successful-episode cap to arbitrary historical direct calls on a `HardState` after unbounded invalidations.

## Source and claim boundaries

The source procurement closure must include the new helper even for default linear mode because the broker imports it. The examined source manifest includes it. The hash is a paid routing accelerator, not an independent source of truth, a probabilistic exactness claim, or a hidden replacement for scope/version checks. Integer conflict tokens are bounded under the finite key/entry contract. The implementation agent's `../hard_hash_index/results.json` reports nine passing probes at the unchanged broker hash; those are supporting executions by its author, not executions performed by this reviewer.
