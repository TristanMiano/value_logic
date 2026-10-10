# Balanced recorded-seed price envelope: independent review

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, ordinary-controls reviewer,
2026-10-10. **P3-08 DEVELOPMENT; same-model, nonblind additive verification.**
Principal and agent research-clock credit are both **zero seconds**. This review
imports neither analyzed module and runs no policy, generator, private scorer,
or reporter. It changes no existing scientific source or evidence.

## Disposition

**PASS. The stronger finite-catalogue statement is correct:** among all 90
balanced configuration means, **no broker mean line attains the minimum at any
external price lambda >= 0, including ties at zero**. All 32 records on the mean
frontier are ordinary controls. This comprises 12 records with positive-width
optimal intervals and 20 additional records optimal only at zero; coincident
no-compute controls remain separate records. There is no positive-price
singleton optimum. No arithmetic, membership, endpoint, completeness, or source
binding discrepancy was found.

The already audited individual-seed intermediate-price broker findings remain
correct. They do not imply that one broker configuration attains the lower
envelope after its outcomes are averaged across the three recorded seeds. The
aggregate adverse result removes that stronger interpretation from this finite
catalogue; it does not erase the individual-record result or estimate a
population expectation. Ordinary-kernel equivalence and Q3 non-closure remain.

## Eligibility, denominators, and information held fixed

The independent checker starts from the sealed 234-line upstream result whose
hash is `2bc29b62e9713ba90665605edab95c60e025250c7c8a210276d33fb6f9b147d7`.
That exact result was previously reconstructed from the sealed development
records by the individual-record reviewer. This additional check audits its
aggregation, rather than rerunning those private truth evaluations.

The checker groups structurally by **scenario, source family, and the full
configuration with only seed removed**. Configuration identity retains the
acquisition price, cache/provider kind, proof solver and cap, selector, hard
setting, and every other recorded field. Identifiers are scoped by scenario;
the analyzer's display key alone is not globally unique across scenarios.

There are **102 initial groups**. Of these, 66 stochastic configurations have
exactly one record for each of seeds 11, 29, and 47; 24 deterministic
configurations have one eligible seed-11 record. The latter are the eight
previously justified deterministic control methods on each of three scenarios:
proof enumeration, proof DPLL, full enumeration, exact DPLL, both exact-cache
indexes, and both no-compute constants. Their deterministic reuse is not a new
execution or statistical replication.

Exactly **12 incomplete groups are excluded from both sides of the comparison**:
six cold-mixed and six cheap-structure reuse configurations, each represented
only by seed 11. In each scenario these are the two selectors crossed with the
three providers, with hard mode enabled. No absent seed outcome is imputed,
and no such stochastic record is misclassified as deterministic.

| Scenario | Stochastic configurations | Reused deterministic configurations | Total | Omitted groups |
| --- | ---: | ---: | ---: | ---: |
| cold_mixed | 18 | 8 | 26 | 6 |
| repeat_online | 30 | 8 | 38 | 0 |
| cheap_structure | 18 | 8 | 26 | 6 |
| Total | 66 | 24 | 90 | 12 |

The retained catalogue contains 57 ordinary-control and 33 broker configurations.
It uses 222 of the original physical records, expanded to 270 seed-line
appearances by deterministic reuse. Neither 90 nor 270 is a count of new runs.
All 90 archived mean records and all 12 omission records match the independent
reconstruction exactly, including membership, coefficients, flags, and fixed
acquisition parameters.

For configuration c and recorded seed s, the objective is terminal error count
plus external price times fully charged cold cost:

\[
J_{c,s}(\lambda)=E_{c,s}+\lambda C_{c,s},\qquad
C_{c,s}=L_{c,s}+50{,}115.
\]

Each configuration receives equal weights 1/3 across the three recorded seeds.
The common source bill is preserved in every mean. The upstream transfer of
1,841 source units to older common-v2 records is checked against every input
line; it does not change local work or acquisition choices. Terminal-answer
errors are used here, not Brier loss or an uncorrected probability diagnostic.

## Independent completeness and endpoint construction

The analyzed code intersects affine half-lines. The independent checker instead
generates every nonnegative pairwise crossing of the reconstructed mean lines,
includes zero, and evaluates the exact minimum at every crossing point, at a
rational midpoint of every intervening open cell, and in the unbounded tail.
Affine order cannot change inside a cell. Thus this checks completeness over
the entire nonnegative price axis, rather than checking a few frontier witnesses.

For each line, the checker joins its winning points and cells and requires a
single contiguous closed interval or unbounded tail. It compares the complete
interval and flags with the archived result. It also compares the archived
active set at every point and cell, so endpoint ties and coincident lines are
fully checked. Replacing cold bills with local bills gives identical winners
everywhere checked, as required by cancellation of the common source term.

| Scenario | Distinct nonnegative crossings, including zero | Point/cell/tail evaluations | All frontier records | Positive-width records | Broker frontier records, including zero ties |
| --- | ---: | ---: | ---: | ---: | ---: |
| cold_mixed | 258 | 516 | 10 | 5 | 0 |
| repeat_online | 405 | 810 | 9 | 4 | 0 |
| cheap_structure | 99 | 198 | 13 | 3 | 0 |
| Total | 762 | 1,524 | 32 | 12 | 0 |

The following table gives all positive-width frontier segments. Finite endpoints
are included in both adjacent segments, so the policies tie there. Additional
zero-only ties are retained in `run_v1/details.json`. Acquisition prices shown
for combinations are the frozen parameters that produced their transcripts;
the external price varies only the retrospective objective coefficient.

| Scenario | External lambda interval | Fixed configuration | Mean errors | Mean cold units |
| --- | --- | --- | ---: | ---: |
| cold_mixed | [0, 1/2638686] | exact_dpll | 0 | 2059463 |
| cold_mixed | [1/2638686, 13/920073] | ordinary_combo_hashed, acquisition 1/100000 | 1/3 | 1179901 |
| cold_mixed | [13/920073, 61/2034120] | ordinary_combo_hashed, acquisition 1/10000 | 14/3 | 873210 |
| cold_mixed | [61/2034120, 6/130517] | proof_enumeration, cap 2048 | 25 | 195170 |
| cold_mixed | [6/130517, infinity) | no_compute_1 | 31 | 64653 |
| repeat_online | [0, 44/1587537] | exact_cache_hashed | 0 | 1924600 |
| repeat_online | [44/1587537, 5/64501] | proof_enumeration, cap 2048 | 44 | 337063 |
| repeat_online | [5/64501, infinity) | no_compute_0 and no_compute_1, coincident | 64 | 79059 |
| cheap_structure | [0, 32/15339] | exact_cache, linear | 0 | 74630 |
| cheap_structure | [32/15339, infinity) | no_compute_0 and no_compute_1, coincident | 32 | 59291 |

## Fixed-configuration means versus seedwise hindsight

At lambda = 1/30000, both sides use exactly the same eligible configuration set
within each scenario. Define

\[
A=\min_c\frac13\sum_s J_{c,s},\qquad
B=\frac13\sum_s\min_c J_{c,s}.
\]

The checker reconstructs every configuration's mean directly from its expanded
seed records, confirms equal catalogue membership in all three seeds, and
checks A, all three seed minima, B, and the exact nonnegative difference A-B.

| Scenario | Fixed-configuration winner | A: minimum configuration mean | B: mean seedwise minimum | A-B |
| --- | --- | ---: | ---: | ---: |
| cold_mixed | proof_enumeration | 94517/3000 | 2105099/90000 | **730411/90000** |
| repeat_online | proof_enumeration | 1657063/30000 | 1532963/30000 | **1241/300** |
| cheap_structure | exact_cache, linear | 7463/3000 | 7463/3000 | **0** |

The cold seedwise winners are finite_tickets at seed 11, probability_cost at
seed 29, and finite_uniform at seed 47. On the repeated tape they are the
ticket broker at seed 11, proof_enumeration at seed 29, and the uniform broker
at seed 47; the relevant reused cold-provider records coincide with the broker
records and create no extra independent evidence. The cheap tape uses the same
deterministic linear exact cache for all three seeds. Exact winner records and
per-seed minima are saved in the checker result.

Both A and B still choose configurations retrospectively using observed
outcomes. The gap measures the extra benefit of allowing that retrospective
choice to vary by recorded seed. It is not a benefit available to an implemented
selector, a new native-price controller run, a gain from retraining, or a
fair-bit expectation estimate. Requiring one configuration across three exposed
seeds is a stricter descriptive comparison, not a prospective validation set.
The absent reuse outcomes remain outside this balanced catalogue.

## Source binding and reproduction

The upstream and aggregate manifests verify all their listed byte lengths and
hashes. Both live analyzer files match their archived snapshots. The aggregate
result names the exact audited upstream result hash. All 14 captured input
files were bound before this check ran and reverified afterward. The declared
aggregate contract is bound separately here because the aggregate run manifest
contains its source and result, not the contract. This later review does not
supply a cryptographic proof of the earlier contract's declaration time.

The independent check's **first execution passed**, from
18:01:32.698600 to 18:01:33.411198 UTC on 2026-10-10. These execution times carry
no research credit. A separate same-model static review by integration_review
also found the deterministic rule, complete grouping, and same-catalogue
comparison consistent with the upstream source. No existing policy/evidence
file was changed.

From the repository root, reproduce only this arithmetic review with a fresh
output directory:

```bash
python -B v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/check_mean_envelope.py --out /path/to/fresh-review-output
```

Keep the checker in its review directory with `plan.md`, `input_manifest.json`,
and `inputs/`, since those relative paths are its complete input closure. The
copied checker inside `run_v1/` is a source preservation copy; it needs the same
sibling input layout before direct execution. Fresh execution timestamps vary;
the exact arithmetic, memberships, and intervals should match.

| Artifact | SHA-256 |
| --- | --- |
| Mean analyzer, live and archived | `506de380c5d5db13a5e3275aa8a574e8326ea4c5ff25940847ae4f15bb6bb8b0` |
| Mean contract | `f409b2ab7fe4f2285e452377a3273e787aee00340d22bff096d2ffbcbb2c467c` |
| Mean result | `984987822a2950ee70d8a3d4b17333725921172d3de9809b6cd6c678ddbc46c5` |
| Mean run manifest | `12555bbbbfbc9b6c935151f7c63a289c1ac3ef1d7f3a3c4e2e57bd826010d49d` |
| Upstream result | `2bc29b62e9713ba90665605edab95c60e025250c7c8a210276d33fb6f9b147d7` |
| Review input manifest | `34ea22952aed6619e23f05507f6da784429dc20617105a5859bcc1477434d02c` |
| Independent checker | `ce602eff1f86d02d05c5bc7ee156c9fb9e81c0e68bd4d3eab9e9f75e34a61890` |
| Independent result | `cc0a922cdbe59210695b4df951b2e317c01a722ac7568bc1c160844f109987ec` |
| Full reconstructed means, cells, and intervals | `1ce806a3a0b946bf77a7458e081b1ed250d1452326e05d0037c5af0768503ef1` |
| Independent run manifest | `7a07cf4710f2933c0963d683eb0c1e9d87a50e5909361e76c62ebc0e3f8558b3` |

`source_checks.json` records the final check of original input bytes against
the captured closure and the review output-manifest verification. The complete
deliverable is additive under this review directory.
