# common_v2: independent score, indexing, price-path, and endpoint review

**Disposition:** the sealed score arithmetic and reported linear/hashed equivalences pass. The specified price example is a real limitation of this concrete ordinary controller: increasing its configured unit price from 0 to 1/100000 increases realized local work by 3,202 units, increases physical provider attempts by 3, and adds one terminal error. Repeated failed capped probes account for the resource reversal. The reporting diagnostic also distinguishes smaller raw sampling radii from actual endpoint gains; the two are not interchangeable.

This is a same-model, nonblind DEVELOPMENT review. The principal supplied the aggregate price witness before this reviewer inspected the traces. The reviewer then wrote independent read-only checks; no policy or reporting service was rerun and no policy, score, or archive was edited. The endpoint executable reads only public artifacts, but the reviewer had already read private scores in the separate score audit. Neither exercise is prospective coverage evidence or an independent random trial. Principal research credit: **0 seconds**; no historical or overlapping credit, no P3-09/final evaluation, no commit or push.

All paths below are relative to `/workspace/scratch/095cdac579b7/value_logic`. The compact binding table at the end identifies the exact sources; `plan.json` contains the full initial manifest.

## 1. What the read-only audit verifies

The sole execution of `check_archive.py` passed from 2026-10-10 17:07:04.506824 to 17:07:06.159977 UTC. Its output is `results.json`, with fuller pair/cost results in `pair_and_catalogue_details.json`.

- Recomputed and matched both public/private seals, source-before/source-after identities, frozen source hashes, all **186** line-level archive hashes, public-index entries, and score entries.
- Recomputed terminal errors, false positives/negatives, base errors, issued/base Brier totals, and live/base lottery diagnostics across **15,872** completed trace positions, using the sealed evaluator truth tape. This is an independent reconstruction of scoring arithmetic, not a second proof of every SAT answer.
- Reconciled all **4,910** physical provider invoices: complete query binding; successful checked answer versus the saved target; failed receipts exposing no purported answer; category and operation totals; and exact absorption of every provider debit into the owning episode. The common installed-source invoice is **48,274** units in every row, and `cold_units = local_units + source_units` throughout.
- Compared **48 ordinary linear/hashed pairs** and **18 candidate linear/hashed pairs** using full trace rows, blocks, provider invoices (including provider costs), weights, selector-bit consumption, purchase counts, and completion status. For ordinary pairs, cost profiles, cache-hit counts, known rounds, successful purchases, provider failures, and feedback-update counts also match. Candidate base/selection/label paths match their finite shadow arms.
- Reconciled **63** optional report bills and the report audit's exact corrections, shared residual, and diagnostic interval membership. This checks saved report/scoring arithmetic, not prospective coverage.
- Independently recomputed **45 native-price catalogue comparisons**, **78 seed-summary groups**, and **36 fixed-path repricing thresholds**. All match `p308_analyze.py` and its saved `analysis_v1/result.json` exactly.

### Indexing interpretation

Full semantic equality holds in these paired completed runs; hashing changes only the charged local implementation work. It does not uniformly save resources.

| Scenario | Ordinary pairs | Ordinary linear minus hashed units, range | Candidate pairs | Candidate linear minus hashed units, range |
|---|---:|---:|---:|---:|
| cheap_structure | 16 | −2,933 to −2,783 | 6 | −3,226 to −2,762 |
| cold_mixed | 16 | 38,005 to 397,577 | 6 | 98,006 to 147,170 |
| repeat_online | 16 | 113,695 to 225,646 | 6 | 301,155 to 484,254 |

The analyzer's `identical_performance` flags originally test aggregate errors, Brier loss, and purchases. The independent audit supplies the stronger trace/invoice/history equality for these particular records. These are representation pairs, not additional independent trials.

### Native-price arithmetic and its scope

Each scenario/seed/price comparison contains **18** eligible records: seven broker arms, the probability-cost arm, the two ordinary-combination indexing implementations at that exact native price, and eight deterministic ordinary baselines. The deterministic baselines are stored only under seed 11; their source policies do not use random selectors, so reusing those fixed records across the three seed comparison groups is appropriate. They must not be counted as three executions.

The analyzer prices each completed core service as `terminal_errors + lambda * cold_units`. Its native-price filter excludes both ordinary-combination arms run at another price. Optional reporting is separately billed and excluded from this core-service comparison, as explicitly declared. The catalogue minimum is retrospective; no deployed oracle or future price-selection guarantee follows. The ordinary mirror is the same executable kernel under an ordinary marginal-cost interpretation, and its equality is not another algorithmic trial.

No arithmetic or eligible-set blocker was found in the bound analyzer.

## 2. Exact explanation of the price reversal

The two run IDs are:

- `repeat_online__ordinary_combo_hashed__seed11__price0`
- `repeat_online__ordinary_combo_hashed__seed11__price1_100000`

They use the same public 128-position input tape, source versions, cache implementation, and selector seed. All selected-position flags and all 64 consumed selector bits agree. The unit-price configuration changes the optional acquisition decisions; purchased/cached feedback then changes subsequent weights and forecasts.

| Quantity | Price 0 | Price 1/100000 | Higher minus lower |
|---|---:|---:|---:|
| Terminal errors | 0 | 1 | +1 |
| Physical provider attempts, including failures | 41 | 44 | +3 |
| Successful checked purchases | 28 | 26 | −2 |
| Failed provider attempts | 13 | 18 | +5 |
| Exact cache hits | 100 | 82 | −18 |
| Paid/retained label updates and known terminal rounds | 128 | 108 | −20 |
| Local resource units | 2,189,022 | 2,192,224 | +3,202 |
| Common source units | 48,274 | 48,274 | 0 |
| Cold resource units | 2,237,296 | 2,240,498 | +3,202 |

### First operational divergence: index 3, before any terminal error differs

At `repeat-online-00003`, both runs have the same immutable forecast `43690/65536`, greedy action 1, and estimated error cost `21846/65536 = 0.333343505859375`. Both lack a cache entry and estimate full-call cost as **60,632** units from the public shape proxy.

Both first purchase a capped DPLL call with cap **4,160**. Both spend **4,159** units and receive `budget_exhausted` with no checked label. At price 0 the estimated fee for a full call is zero, so the controller makes a fresh full purchase, spends **6,775**, learns checked label 1, and caches it. At price 1/100000 the estimated full-call fee is **0.60632**, which exceeds the estimated error cost, so it stops after the failed probe. The first failed probe is affordable under both price tests: `4160/100000 = 0.0416` is below the estimated error.

Both terminal actions at index 3 happen to be correct. Nevertheless, the first block now supplies four label updates in the lower-price run and three in the higher-price run. Its post-block weight vectors are respectively:

- `[20232, 102413, 102413, 102411, 20230, 45517]`
- `[28862, 97402, 97402, 97400, 28860, 43290]`

Consequently base forecasts first diverge at index 4. Across the episode, 121 base forecasts and 42 emitted forecasts differ. This is acquisition-dependent learning, with identical selectors.

### Calls by purpose

| Purpose | Price 0: calls (success/failure) | Price 0 units | Price 1/100000: calls (success/failure) | Price 1/100000 units |
|---|---:|---:|---:|---:|
| optional_capped_probe | 21 (8/13) | 76,571 | 25 (7/18) | 111,714 |
| selected_full | 7 (7/0) | 368,738 | 13 (13/0) | 1,524,182 |
| optional_full | 13 (13/0) | 1,286,140 | 6 (6/0) | 103,745 |
| **Total** | **41 (28/13)** | **1,731,449** | **44 (26/18)** | **1,739,641** |

Every full call succeeds. Every failed call here is a capped probe. Failures have neither a hard answer nor a retained solver continuation. The controller's cost profile records successful full-call costs; failed prefixes are censored, not learned as cheap full completions. Later `selected_full` purchases occur on cache misses independently of the unit-price test.

Several early full purchases are delayed until a later selected repetition: indices **3→35, 14→110, 19→51, 22→86, and 29→61**. The cheap contradiction first bought by a successful capped probe at index **24** is instead first bought by `selected_full` at **88**. The two formulas first seen at **9** and **18** never receive a successful purchase in the higher-price run. The cost of the same successful checked formula is unchanged when moved to a later occurrence.

The higher-price path pays five additional failed capped probes: indices **41, 73, 105** each cost **6,870** for the still-unlearned key first seen at 9, and indices **46, 78** each cost **8,024** for the key first seen at 14. Their sum is exactly **36,658**. Successful provider work falls by exactly **28,466**, the omitted full costs **21,592 + 6,874** of keys 9 and 18. Thus:

`provider increase = 36,658 − 28,466 = 8,192 units`.

Other local work decreases from **457,573** to **452,583**, a **4,990** unit decrease, chiefly reflecting changed cache/feedback work together with extra admission/profile work. Full operation-level deltas are retained in `target_trace_explanation.json`. The net increase is exactly:

`8,192 − 4,990 = 3,202 units`.

### The single added error: index 78

The UNSAT key first seen at 14 repeats at **14, 46, 78, 110**. The lower-price run learned its checked answer 0 at index 14 for **1,060,041** units and serves index 78 from cache. The higher-price run remains unresolved at index 78. It emits `45330/65536`, chooses action 1, pays another failed 8,024-unit probe, and declines the full call: its profile estimate **68,682** implies fee **0.68682**, exceeding `20206/65536`. It therefore makes one false positive. It finally buys the checked answer at selected index 110.

The 68,682 estimate is the already acquired successful full cost of a different formula in the same coarse public shape group, acquired at index 61. This is visible, fallible own-history information. It is not hidden evaluator truth.

### Q4 consequence and limit

For this fixed controller, tape, and seed, the positive price suppresses some early learning/cache acquisition but does not suppress later selected full calls or repeated failed-prefix work. A local marginal fee test therefore does not establish a monotone full-episode resource response to price. The record is a concrete counterexample to such a claim about this implementation. It is not a general theorem that raising prices increases computation, nor a comparison of globally optimal policies.

At a common retrospective evaluation price of 1/100000, the lower-price policy's saved record costs **22.37296**, while the native higher-price policy costs **23.40498**; the difference is **1.03202**. The native-price analyzer correctly excludes the zero-price combination record from the higher-price catalogue. This illustrative repricing must not be substituted for a native run or presented as an implemented tuning rule.

## 3. Do the displayed statistical intervals add information beyond deterministic caps?

The separate `report_endpoints/check_endpoints.py` ran once, successfully, from 2026-10-10 17:10:14.221798 to 17:10:15.308865 UTC. It checks the public archive seals, reconstructs the report's declared deterministic envelopes from issued forecasts and paid/current labels, and recomputes interval clipping exactly with rational arithmetic. It reads no private scores or truth, and invokes no policy/report service. Reviewer blindness is not claimed.

The relevant comparison is strict: an interval adds endpoint information if its lower endpoint exceeds the declared deterministic lower cap or its upper endpoint is below the declared deterministic upper cap. Empty intervals and conflict flags are counted separately, never as improvements. Equality with a deterministic cap is not labeled a statistical failure.

### Actual common_v2 reports

All 63 reports use the snapshot basis and grid rule. There are no empty intervals, confidence conflicts, or all-remaining-known exceptions.

| Target | Strict lower improvements | Strict upper improvements | Either endpoint improves | Both endpoints equal deterministic caps |
|---|---:|---:|---:|---:|
| F | 0 | 6/63 | 6/63 | 57/63 |
| V | 0 | 6/63 | 6/63 | 57/63 |
| Z | 0 | 11/63 | 11/63 | 52/63 |

Exactly **11 of 63 report records** improve at least one target endpoint. The six F/V improvements are the repeat_online finite_uniform and finite_uniform_enumeration arms at each of the three seeds. The candidate's only gain beyond its declared caps is the repeat_online value_uniform seed47 **Z** upper endpoint, from 61 to `31572549251/536870912`, repeated identically by its hashed representation. The remaining three Z-only improvements are cold_mixed finite_uniform and finite_uniform_enumeration seed47, and repeat_online finite_tickets seed11.

Counts are report records. They include duplicated indexing/solver output representations and do not measure independent trials. Most displayed endpoints on these cohorts are determined entirely by the observable deterministic caps; the few strict gains are real exact endpoint gains.

### All 180 reports recomputed on old common_v1 traces

These are 45 fixed public broker traces under four reporting constructions. No reporting computation was rerun for this diagnostic; it only reads the sealed reporting_v2 outputs.

| Construction | Reports | F upper improves cap | V upper improves cap | Z upper improves cap | Reports with any improvement |
|---|---:|---:|---:|---:|---:|
| base/fixed | 45 | 12 | 12 | 20 | 20 |
| snapshot/fixed | 45 | 12 | 12 | 20 | 20 |
| base/grid | 45 | 6 | 6 | 9 | 9 |
| snapshot/grid | 45 | 6 | 6 | 10 | 10 |
| **Total** | **180** | **36** | **36** | **59** | **59** |

All lower endpoints equal their deterministic lower caps; there are **zero empty/conflicted intervals**. F and V each equal both caps in 144/180 records, and Z in 121/180.

### Raw radius changes versus actual endpoint changes

| Paired public comparison | Pairs | Raw sampling radius smaller / equal / larger | Actual F endpoint gains | Actual V endpoint gains | Actual Z endpoint gains |
|---|---:|---:|---:|---:|---:|
| base/grid versus base/fixed | 45 | 6 / 0 / 39 | 0 | 0 | 0 |
| snapshot/grid versus snapshot/fixed | 45 | 15 / 0 / 30 | 0 | 0 | 0 |
| snapshot/fixed versus base/fixed | 45 | 15 / 30 / 0 | 0 | 0 | 3 |
| snapshot/grid versus base/grid | 45 | 15 / 30 / 0 | 0 | 0 | 1 |
| snapshot/grid versus original base/fixed | 45 | 16 / 0 / 29 | 0 | 0 | 0 |

The grid penalty allows a smaller raw radius for some records, but produces **no improved displayed endpoint relative to the corresponding fixed-rule report** in these old-trace comparisons. F/V endpoints instead worsen in 12/45 records and Z endpoints worsen in 20/45 records for each same-basis grid-versus-fixed comparison; the others are equal. This is consistent with the grid's larger union allowance and does not contradict the validity of its separately declared certificate.

Snapshot versus base improves three fixed-rule Z upper endpoints: cold_mixed value_uniform seed47 and repeat_online value_uniform seeds29/47. The cold_mixed improvement has **equal sampling radius**, so it comes from the changed center. Under the grid rule only repeat_online value_uniform seed47 improves its Z endpoint. Neither basis change improves an F/V endpoint on these records.

For the actual 63 common_v2 snapshot/grid reports, a public formula-only comparison to the same-basis fixed radius gives 27 smaller and 36 larger raw radii. There are zero endpoint gains over that virtual fixed rule; F/V endpoints are equal in 51/63 cases and Z in 40/63, with the others worse. This comparison does not create an authorized posthoc minimum of the two report procedures.

## 4. Source and evidence binding

The first plan binds 17 source/data files and records pre-plan source exposure. The endpoint addendum has its own eight-public-file plan and pre-execution binding. All full traces, per-purpose invoices, exact changed-key histories, and endpoint details remain reviewable in the JSON artifacts.

| Source or evidence | SHA-256 |
|---|---|
| `development/common_v2/run/public_records.jsonl.gz` | `afcdac06a9f1803cb0c57f0981bdffd2f7480127d9d7c5cb8c92d0038e5639ba` |
| `development/common_v2/run/private/scores.json` | `4b34e6cf9befd537235950d7bf12c3ea750a568cf6863a0da190787d217e103f` |
| `development/common_v2/run/private/truth.json` | `ad547a9d16e35f226d828a43491460b65395de649a7f36b233cf6dec6058bd84` |
| `development/common_v2/source/v3/experiments/p308_ordinary.py` | `fc98d9008bbf429e35a4b2fc71806ec006cc4f6fd416051c8fdaea2782f29bff` |
| `development/common_v2/source/v3/experiments/p308_cnf.py` | `46fd3e82505b9b6af9805836a562f2f78a3436384e0b3476c4f85cec355817a2` |
| `development/common_v2/source/v3/experiments/p308_run.py` | `01b468abb46cf9f1cb0e9143a9a64e811e18ffecce8de6c4d51d92e7373a4c99` |
| `development/common_v2/source/v3/experiments/p308_reporting.py` | `990f3b417d4ab366a9be7baccb137d4335d90d284354c61d3d8f15dbfeafe0e1` |
| `development/common_v2/analysis_v1/p308_analyze.py` | `cc646aa77ef246341d90539cf0f09e137e47f322a9d8d887a8bea4b8a687df14` |
| `development/reporting_v2/run/public_reports.jsonl.gz` | `bc7bb4970de4abaebdf37dfab01b3fa15b8ec4eae519847916f2d0a62fe39f18` |
| `reviews/common_v2_analysis/check_archive.py` | `00f4018dc693c940ff53a434dc3dc6fe285068f8a2fa55125b5f0dbc2b416fe7` |
| `reviews/common_v2_analysis/results.json` | `96a96e94efe7baa4b6305c92c98c8da7e980395968c1c26289d6fcdf08c4d585` |
| `reviews/common_v2_analysis/target_trace_explanation.json` | `54eab38e737eaa79b8404b785582e15f496b075d8ab7b2834f3003b2db632672` |
| `reviews/common_v2_analysis/pair_and_catalogue_details.json` | `ae1a5d8d6f7c057ee5d68cb9410ed1de6461e308337c262b319dc872c45e800f` |
| `reviews/common_v2_analysis/report_endpoints/check_endpoints.py` | `b4cdb634b9bfe09144cc3525ea4dbf561a9c13c12695ef56262dae00a0abca53` |
| `reviews/common_v2_analysis/report_endpoints/results.json` | `73feed44c5258c6b909615e171a1bc8fab74ec983aabcda6a486655320e274bf` |
| `reviews/common_v2_analysis/report_endpoints/details.json` | `f8c37855a1cfde46c8b57dcfc9f85c4cd9c7e7bc612cd7e7ac5aa1ace6e1765d` |

In this table, `development/` and `reviews/` resolve under `v3/work_logs/P3_08_2026-10-10_S1/`. The analyzer's live source and saved analysis source have the same bound hash. The target record hashes are `914817abf8575c18855c34b46b35585895afe4c3c3fc8b33e431edfae272bd86` (price0) and `a6e40848c0fa1d5750f5f7986112fd6f093058051527dea4aba8a0efa0e4e27e` (price1/100000).
