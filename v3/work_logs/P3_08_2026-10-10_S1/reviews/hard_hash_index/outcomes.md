# Hashed hard-key index: outcomes and ownership handoff

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration-review sub-agent,
October 10, 2026 UTC. **P3-08 DEVELOPMENT**.

**Completed:** optional paid hashed indexing is implemented in broker v1.2,
the default linear behavior is preserved, all nine focused case groups pass,
and a separate same-model structural reconstruction found no cap or semantic
blocker. Broker ownership has been returned to the principal. No further
broker edits are planned. No commit, push, P3-09 or final evaluation was
performed.

Implementation and executable verification here are **self-check** of the
delegated author's changes. The structural agent's cap and semantic review
is **independent, same-model and nonblind**. Agent resource/time costs are
unmeasured and principal-clock credit is zero. The principal's common_v2
run remains a separate prospectively frozen development stage.

## 1. Final source and evidence binding

| Artifact | SHA-256 |
|---|---|
| Broker v1.1 before indexing | `399080c950a48c1cd935efbee8ed7769a7af54b7afa14859b5671397638e2e4d` |
| Broker v1.2 implemented/tested source | `248642e00333f0939f2e0e41020c69879b2d5bcedacf7979f980583630ba3653` |
| Shared `p308_hashcache.py` v1 helper source | `a668abfff6c4dd6c7d18cb186ed99bbb9c794713ce9f93e8a27470320b07a914` |
| `check_hard_index.py` | `0ae981065737707be8614536828e09a59c8dfb1f38b1dee2247773b269242819` |
| `results.json` | `659d4ee300b1b6b1615aecaf55b13277c911546974462a1c5afd725a6141b83e` |

The source closures are retained in `source_before/` and `source_snapshot/`.
`plan.json`, `design_and_cap.md`, `source_manifest.json` and
`script_before_execution.json` precede execution. The sole new script run
started at 2026-10-10 16:55:43.558718 UTC and ended at
16:55:43.700448 UTC, with **9 pass, 0 fail**:

```text
python v3/work_logs/P3_08_2026-10-10_S1/reviews/hard_hash_index/check_hard_index.py
```

All earlier broker sources, failed runs and repair dispositions remain
unchanged. The new source closure includes the new hash dependency; source
procurement must include it when the implementation is deployed.

## 2. Public API and unchanged decisions

`Contract.hard_index` is appended after `hard_capacity`, accepts `linear`
or `hashed`, and defaults to `linear`. Seven-field positional calls preserve
their old meaning; an eighth positional field can select hashing. Invalid
types and unsupported labels reject. The episode records `hard_enabled`
and `index_kind`, and its contract/hard-state records expose matching
configuration.

Both modes pay eight explicit output units for these configuration fields.
The comparison with the captured old broker verifies that linear mode's
forecasts, selections, full traces, provider invoices, weights, bit count,
hard state and all prior meter operations are identical. Only that declared
eight-unit metadata bill/cap addition and the new configuration fields differ:

| Selector, eight-query check | Old paid total | New linear paid total | Old cap | New linear cap |
|---|---:|---:|---:|---:|
| Uniform | 7258 | 7266 | 190488 | 190496 |
| Tickets | 7972 | 7980 | 190508 | 190516 |

The hashed mode uses 128 paid bucket heads and constant-size linked nodes
naming append-only entry slots. Every candidate retains a full-key,
scope and generation check. Hash equality alone never authorizes an answer.
The helper is shared with the ordinary hashed exact cache; no hidden Python
semantic-key hash is used to choose hard buckets. The full canonical CNF key
includes semantic/source versions, variables and clauses, and excludes request
identity, hard epoch and generation.

## 3. Paired paths and mixed actual cost effects

Paired linear/hashed runs preserve **identical complete traces and selected
provider invoices**, for both uniform and ticket selection, on repeated and
varied tapes. This equality includes base and emitted forecasts, prospective
and terminal actions, hard-before/hard-after states, purchased labels,
actual propensity records, block weights and bit consumption.

The 32-query checks show the expected workload dependence of indexing cost:

| Selector | Tape | Retained keys | Linear units | Hashed units | Hashed minus linear |
|---|---|---:|---:|---:|---:|
| Uniform | Varied | 6 | 28362 | 27596 | -766 |
| Uniform | Repeated | 1 | 22256 | 26043 | +3787 |
| Tickets | Varied | 3 | 29245 | 29832 | +587 |
| Tickets | Repeated | 1 | 24416 | 28215 | +3799 |

These are declared finite development witnesses, not a population advantage
or tuning decision. Paid hashing can cost more than a short linear scan.
No method or seed was changed after seeing these bills. The main comparison
can retain both index kinds as prospectively specified alternatives.

When hard overrides are disabled, hashed configuration still pays its fixed
133-unit allocation but performs no live hash operations. In the checked
eight-query run, totals are 6538 linear and 6671 hashed. This configuration
and its initialization charge are explicit; default disabled controls can
continue to use the default linear index.

## 4. Collision, identity, conflict and generation probes

A bounded public-shape search found a real bucket collision after 24 helper
calls. With four variables, the false key containing an empty clause and
unit clause `(-2)` and the true key containing the single clause `(-4,1)`
both map to bucket 10. The fixture was saved before obtaining real checked
receipts; those receipts independently returned 0 and 1.

Admitting the false key did not authorize the other key. After both were
admitted, both correct answers remained retrievable. Reissuing the false
complete key with a different request ID reused the coordinate without
appending another entry. The hash implementation charged the actual bucket
collision continuation and the complete-key comparisons.

A test-only contradictory claimed receipt passed directly to HardState
exercised its conflict path; the real source did not generate a contradictory
answer. The conflict invalidated only that current coordinate and did not
affect the different key in the same bucket. Both modes then:

* retained the old entries as stale after changing epoch;
* kept them stale after returning to the old epoch label, because the
  generation had advanced;
* admitted fresh current answers into new slots;
* retained four total entries, two active entries, the historical conflict,
  two withdrawals and generation 2;
* rejected a further insertion at capacity without discarding historical
  entries or corrupting the index.

The hashed representation retained exactly four reachable nodes for its
four entries, with no missing, dangling or duplicated slot. This checks the
full collision/version behavior without assuming collision resistance or
monkeypatching the production hash function.

## 5. Atomic insertion and budget/withdrawal failure

An empty hashed store needed 230 total units through its first full insert.
At limit 229, it spent 198 units on initialization and lookup, then denied
the entire 32-unit commit bundle. Both the entry array and all bucket heads
remained empty. Thus a denied debit cannot leave an unindexed hard entry or
a node naming an absent entry.

Uniform and ticket provider-limit-zero failures preserve the failed provider
invoice and suppress the quota theorem. Hard-capacity-zero failures preserve
the one already purchased checked receipt and its acquisition bill while
failing hard admission. Low parent funding remains a recorded failed path.

After a completed hashed broker episode, an explicit test-only spend
exhausted the parent budget. A subsequent withdrawal failed at its paid
invalidation operation, but the broker had already entered its prepaid
failed epoch state. Its current record no longer asserted success, a new
issue rejected, and the retained historical index remained structurally
valid. This preserves the earlier fail-closed repair.

## 6. Funding results and independent structural reconstruction

The new cap adds eight configuration-output units to all modes. Hashed mode
adds 256 fixed initialization units and, when hard overrides are enabled,
`T*(16*key_max+256)`. It retains the old worst-case full-key scan allowance;
there is no all-path assumption of balanced buckets.

| Selector, sixteen-query check | Hashed all-path cap | Actual paid | Restricted successful limit | Restricted theorem eligible? |
|---|---:|---:|---:|---|
| Uniform | 403128 | 14485 | 21509 | No |
| Tickets | 403168 | 15500 | 22524 | No |

Execution at each exact advertised cap completed with all-path eligibility.
The lower limits include provider reservation headroom and complete those
particular realizations, but correctly withhold the theorem flag. The
maximum-key probe uses 343 key words, 12 variables, 64 width-four clauses,
a 128-character source label and action/state precision 32. It completes
at its declared cap 851032754 with actual total 37558, peak numerical width
68 bits and 220 paid hash input-block units. It uses an easy SAT instance
so this bounded-shape check does not create an expensive truth population.

The separate structural agent reviewed the final source hash and the
prospective bound. Its independent reconstruction confirmed:

* `_locate` is called at most three times per broker position and reuses the
  admission bucket during insertion;
* each bucket candidate costs at most `2Q+10` before bounded return work;
* the old `12(K+1)(Q+32)` scan allowance exceeds `3K(2Q+10)` by
  `6KQ+354K+12Q+384`;
* the shared helper satisfies `H(Q)<=4Q+16`, so the added `16Q+256`
  allowance covers four calls with at least 192 units of fixed-work slack;
* fixed index initialization is 133 units, covered by 256, and the extra
  eight output units are matched in the cap;
* complete-key chronology, nonreused conflict slots and prepaid atomic
  mutation preserve the declared semantics.

That review reported no blocker. Source procurement of `p308_hashcache.py`
remains required. The cap is a statement about the declared abstract word
tariff and owned finite service, not arbitrary hardware/runtime failures.

## 7. Reporting interface and final disposition

The current reporter accepts the explicit index configuration. A paired
ticket check using the prospectively specified `basis="base", radius="fixed"`
produces identical reference/live centers, corrections, widths, rates,
radii, unresolved counts, deterministic envelopes, intervals and confidence
eligibility for both indices. Both reporting calculations cost 8448 units.
This is a test of index invariance; the new snapshot/grid mathematical
extensions are under their own separate review.

The requested indexing improvement is complete. No new source defect or
failed case occurred in this nine-group probe. Previous failures remain
preserved in their original review directories. The principal can freeze
the complete common_v2 dependency closure with both index kinds, while
retaining all existing funding, receipt-soundness, fair-bit and fixed-end
performance boundaries.
