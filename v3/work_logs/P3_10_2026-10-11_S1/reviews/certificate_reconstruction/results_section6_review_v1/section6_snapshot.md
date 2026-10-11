## 6. Current-bound certificates: valid delivery, costly reuse and cap failures

### 6.1 The checked object is the whole current incumbent sublevel

Of **416 scheduled delivery attempts**, 356 deliver valid current warrants
and 60 return `NO_CURRENT_CERTIFICATE` with `ResourceExhausted`. No delivered
warrant has a false bound, stale/current identity confusion, wrong source or
request scope, or missing required sublevel member. All 104 history scores pass
validity, while only **70 histories** deliver all four requests. In particular,
all 52 full-budget histories deliver all 208 requests. Capped histories deliver
148 of 208 requests, and 18 of their 52 histories achieve full service.

Both construction families reduce pointwise to the signed loss difference
`D = 2z-1`; the final edit gives `D = 2z-1/2`. The independent reference checks
those identities at every Boolean assignment rather than trusting the ADD
representation. The old complementary domains are disjoint halves, each of
size 8 or 64, with exact old bounds −1 and +1. The current request can change
hard information, rank, supplied incumbent or loss, so an old bound does not
become a current warrant merely because its mathematical expression is familiar.

| Edit slot | Hard-feasible states, n=4 / n=7 | Current sublevel | Minimizers | Incumbent rank | Exact D range | Current upper bound |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 16 / 128 | 16 / 128 | 16 / 128 | 0 | [−1,1] | 1 |
| Hard/rank edit | 12 / 96 | 6 / 48 | 6 / 48 | 0 | [−1,1] | 1 |
| Nonoptimal incumbent | 12 / 96 | 12 / 96 | 6 / 48 | 1 | [−1,1] | 1 |
| Weight/loss scope edit | 12 / 96 | 6 / 48 | 6 / 48 | 0 | [−1/2,3/2] | 3/2 |

The third slot deliberately includes nonminimal assignments at or below the supplied
cutoff: the certificate is over the entire incumbent sublevel, not merely an
arbitrarily chosen optimum. All minimizing ties remain included. The positive
upper bounds are attained and valid; they do not certify action improvement or
non-deterioration. The service is given its incumbent and bound as task inputs,
so this experiment does not price an algorithm for acquiring an optimal action
or incumbent. Those are distinct obligations.

Evidence: [independent scalar and invoice reconstruction](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_observation_v4/results.json) and
[certificate interpretation with all 104 history bills](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_review_v1/review.md).

### 6.2 Direct ordinary checking wins complete service

`O-ENUM-RECEIVER` is the unique cheapest complete ordinary method in all eight
full group/recipient cells and all four corresponding family/recipient
aggregates. The next table sums the two sizes within each family: two histories
and eight requests per method, all delivered. Units are the separate declared
`rp3bb-cpython31214-observed-events-plus-live-byte-periods-v1` certificate tariff.

| Family | Recipient | P-REUSE units | Direct ordinary units | Reuse/direct ratio | P-FRESH rebuild units |
| --- | --- | --- | --- | --- | --- |
| Majority DNF/CNF | Fresh | 15,294,823 | 4,330,174 | 3.532150 | 19,814,051 |
| Majority DNF/CNF | Resident | 11,029,502 | 4,330,190 | 2.547117 | 19,814,025 |
| Selector mux/sum | Fresh | 17,103,740 | 4,492,110 | 3.807507 | 21,198,524 |
| Selector mux/sum | Resident | 12,058,878 | 4,492,126 | 2.684448 | 21,198,498 |

At individual full-history granularity, reuse costs 2.356317–3.864761 times
direct enumeration at the same complete request-ID coverage. Resident receipt
delivery reduces reuse's bill relative to fresh delivery but leaves the direct
ordinary advantage intact. Narrower favorable reuse comparisons are preserved:
it meets the completed-path 5% convention against P-FRESH for the n=7 streams,
and against the ordinary ADD portfolio for the n=4 streams. They do not establish
advantage over the cheapest complete ordinary service. Even a visually favorable
aggregate can miss the threshold: majority fresh reuse costs 15,294,823 against
portfolio 16,081,726, a ratio greater than 0.95.

The full-service ordinary advantage also has a price-robust interpretation on
the recorded primitive counts. Direct enumeration has no greater count in any
category in all eight complete group/recipient cells. Therefore any common
nonnegative prices on those primitive counts leave it no more expensive. A
price vector assigning zero to every differing coordinate can produce a tie;
strict saving at every possible price is not claimed. The statement holds the
actual full paths fixed. It neither changes their budgets nor supplies a
complete economic claim across the original failed experiment.

Evidence: [all 156 certificate aggregate records and 864 directed comparisons](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_observation_v4/results.json),
[complete comparison interpretation](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_review_v1/review.md), and
[exact summary and primitive-price cells](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_review_v1/summary.json).

### 6.3 Actual caps reveal a stateful coverage deficit

The consumer cap is **1,048,576 units per attempt** within the common total
per-attempt service budget of **134,217,728 units**. These are different scopes:
a whole attempt's producer, enrollment and delivery bill is not identical to
its consumer-cap subtotal. Each capped history starts separately and evolves
through its actual successful or failed transitions.

| Budget | Recipient | Method | Delivered request IDs /16 | Full histories /4 | All-attempt units |
| --- | --- | --- | --- | --- | --- |
| Full | Fresh | P-REUSE | 16/16 | 4/4 | 32,398,563 |
| Full | Fresh | Direct ordinary | 16/16 | 4/4 | 8,822,284 |
| Full | Resident | P-REUSE | 16/16 | 4/4 | 23,088,380 |
| Full | Resident | Direct ordinary | 16/16 | 4/4 | 8,822,316 |
| Capped | Fresh | P-REUSE | 6/16 | 0/4 | 40,700,598 |
| Capped | Fresh | Direct ordinary | 14/16 | 2/4 | 8,322,314 |
| Capped | Resident | P-REUSE | 6/16 | 0/4 | 39,242,612 |
| Capped | Resident | Direct ordinary | 14/16 | 2/4 | 8,322,342 |

At n=4, capped reuse loses the first request and delivers requests 2–4. At n=7
it delivers none. Direct enumeration delivers every n=4 request and requests
2–4 at n=7. Thus reuse has a strictly smaller covered set in every capped
group/recipient cell. It fails the frozen coverage-superset condition
independently of any resource price. No zero-cost assumption or allocation of
unknown overhead could turn those same sealed missing request IDs into service.

All 60 certificate denials are budget outcomes with complete internal invoices,
not unexpected program failures. Their stages are **24 receiver checks,
22 old-receipt checks, two old-input admissions and 12 receiver-storage steps**.
Their retained paid fees sum to **168,462,843 units**, within the complete known
certificate all-attempt total of **625,860,229 units**. Every history pays the
common 561,239-unit source enrollment once, followed by three zero source
charges. Source installation persists after failure; the scientific producer
and receiver caches are evicted and the current receipt is withdrawn.

There are 52 scheduled attempts following a failure: 28 subsequently deliver
and 24 fail again. Four resident n=7 histories expose why retrospective cap
filtering is invalid. Both P-REUSE and the ordinary ADD portfolio, in both
families, have full-trace requests 2–4 whose consumer subtotals fit the cap.
Their actual capped histories nevertheless deliver none because the successful
bootstrap and retained evidence were never acquired. Filtering the full traces
would invent **12 deliveries** across those four histories. They are the only
coverage-set discrepancies among the 52 full-versus-actual-cap pairs, and the
actual capped runs are authoritative.

Full-service primitive dominance must not be copied into the capped setting.
Direct enumeration publishes more successful receipts there, so some of its
output counts are larger because its service coverage is larger. The capped
conclusion follows from exact coverage and all-attempt bills, with every failed
attempt retained, rather than from a claim of componentwise capped dominance
or a cost average conditioned only on successful deliveries.

Evidence: [request-level costs, failure stages and state transitions](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_observation_v4/results.json) and
[failure census and the four cap counterexamples](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_review_v1/review.md).
