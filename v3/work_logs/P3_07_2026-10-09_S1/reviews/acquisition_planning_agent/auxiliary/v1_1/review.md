# Frozen acquisition-planning v1.1: narrow follow-up

## Verdict and scope

**PASS.** All 24 newly saved canonical core identities verify. The resource bills derived independently from the saved source byte sizes and declared operation charges match every saved plan. All 1,128 saved Bellman-table states, root actions and values, and conditional-law results are unchanged from frozen v1. In total, 9,763 exact comparisons produced zero mismatches.

The reviewed v1.1 source and its saved copy both have SHA-256 `88c73b82ac2809da8f31a8dcb93237e732f93b73665a42f5ec180d6355c782b7`. The run is `development/acquisition_planning_run_v1_1`; the comparison baseline is the preserved `development/acquisition_planning_run_v1`. The saved v1 source hash remains `94fb8efcbb924470d883733f3c317fc0a79c4047089104ee4ee1c03ca5141f37`.

This is a same-model, nonblind follow-up. The assignment disclosed the frozen v1.1 hash, expected construction totals, and expected cost delta. The checker was independently authored; it did not import or execute the planner, rerun previous checks, recompute the DP, or restate a new theorem verification. It compares the new saved mathematical results directly with the independently checked frozen v1 evidence. The only adapter information used beyond its byte size and hash is its literal category order, read through Python's syntax tree without execution.

All work is unmeasured auxiliary work with zero principal credit. All new files are confined to this `auxiliary/v1_1` directory; v1 artifacts and earlier evidence are preserved.

## Canonical identities

For every plan, the checker re-encodes the saved `core` as sorted-key compact ASCII JSON and computes its SHA-256. Each hash matches both the plan envelope's `identity` and the result row's `plan_id`. The encoded byte length matches `core_bytes`, the full canonical envelope plus one newline matches the saved file bytes, and each core fits its declared word envelope. All 24 identities are distinct.

Each new core has the expected version and source hashes. After removing only `version`, `source_hashes`, and `construction_resources`, every new core is exactly equal to its corresponding v1 core. The full 24 new identities, byte counts, and evidence hashes are recorded in `verification.json`.

## Independently derived resource bill

The saved adapter is unchanged at 22,795 bytes. The planner grows from 9,047 bytes in v1 to 9,515 bytes in v1.1. The charged source-read/hash formula is twice the sum of each file's size rounded up to eight-byte words:

    v1:   2 * (ceil(22795/8) + ceil(9047/8)) = 7,962 units
    v1.1: 2 * (ceil(22795/8) + ceil(9515/8)) = 8,080 units

That is an increase of 118 units. The newly declared two-file stat operation adds 2 units, producing an exact per-plan increase of 120 units.

Let C=(N+1)(N+2)/2 be the number of table states and W=1024+64C the word envelope. The independently reconstructed operation bill is:

| Operation | Formula | Cap 1 | Cap 12 |
|---|---:|---:|---:|
| Model admission | 96 | 96 | 96 |
| Two source-file stats | 2 | 2 | 2 |
| Source reading and hashing | 8,080 | 8,080 | 8,080 |
| Bellman state bundles | 128C | 384 | 11,648 |
| State child reading and retention | 64C | 192 | 5,824 |
| Planner freeze, validation, hashing | 2W | 2,432 | 13,696 |
| Core retention | W | 1,216 | 6,848 |
| **Total** | **11,250 + 384C** | **12,402** | **46,194** |

These values match the saved operation dictionaries, category totals, core construction-resource vectors, construction-unit totals, meter totals, and remaining balances. There are twelve plans per cap, so the complete 24-plan construction total is `12*(12402+46194)=703152`, up from 700272 by exactly 2880 units.

## Preserved mathematical results and price effects

Every saved state field is identical to v1, including action, Bellman value, posterior, predictive probability, deployment value, and continuation value. Root actions, the root Bellman value, prior gain excluding construction, and every conditional-law record are also identical. This is evidence equality against v1, not a recomputation of the mathematical experiment.

The changed construction bill is the only change to the final gain calculation. All 24 saved construction costs and all-in gains satisfy the exact identities

    new construction cost - old construction cost = 120*price
    new all-in prior gain - old all-in prior gain = -120*price.

| Unit price | Construction-cost increase | All-in prior-gain change |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1/10,000 | 3/250 = 0.012 | -3/250 = -0.012 |
| 1/1,000 | 3/25 = 0.120 | -3/25 = -0.120 |

The original finite-model and sunk-cost interpretation continues to apply unchanged. This follow-up does not review preflight ordering, denial behavior, oversized-price behavior, the DP theorem, optional stopping, or whether declared units adequately represent CPU or human development effort. Those remain outside this assignment and, where applicable, with the parent reviewer.

## Artifacts and reproduction

- `check_frozen_v1_1.py`: the independent bounded checker.
- `verification.json`: exact comparison counts, zero-mismatch result, byte-derived tariffs, all 24 identities, cost deltas, and evidence hashes.
- `review.md`: this scoped account.

The bounded command was `python v3/work_logs/P3_07_2026-10-09_S1/reviews/acquisition_planning_agent/auxiliary/v1_1/check_frozen_v1_1.py`, run from the repository root. It exited successfully.
