# Fixed-path economic robustness audit plan

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Independent same-model, nonblind, retrospective DEVELOPMENT observer review.
Zero principal-clock credit; no worker, analyzer or previous evidence edits.

Use the sealed `development/primary_v5` records and the published
`development/primary_analysis_v1` outputs. Reconstruct costs directly from
each invoice's stage/category counts. Do not import or execute the parent
analyzer, producer, receiver or common service. Verify existing seals and the
correspondence of published category, per-request and total summaries to the
raw records. Preserve an input hash inventory and before/after equality.

## Declared comparisons

There are four fixed families, two recipient modes, six methods and six
requests per method/stream: 288 successful primary deliveries. Keep the eight
family/recipient groups and the forty-eight paired ENUM/P-REUSE requests
distinct. Neither count is a statistical sample of independent trials.

For each complete six-request group, sum the tariff counts for each category
across stages and requests. Compare `O-ENUM-RECEIVER` with `P-REUSE` in every
coordinate. Repeat the comparison separately for all forty-eight paired
requests, preserving any exceptions, exact differences and scalar unit-price
totals. A componentwise weak inequality supports all nonnegative common
category prices on these fixed count vectors. Strictness requires positive
weight on a coordinate with a strict difference; the zero tariff only ties.

## Price parameter and exact envelope

Let $`c_m`$ be the sum of the six recorded `consumer_units`, using exactly the
published consumer-stage definition. Let $`a_m`$ be `total_units` minus that
sum. This fixed nonconsumer intercept includes producer, request-encoding and
coordination work; it is not silently identified with `producer_*` stages
alone. At nonnegative receiver-price multiplier $`\rho`$, compare the lines

```math
L_m(\rho)=a_m+\rho c_m,\qquad\rho\ge0.
```

Keep all six declared methods, including the four ordinary methods, eligible
only if their six receiving services completed. Construct each line's exact
closed minimizing interval by intersecting all pairwise affine half-lines,
using `Fraction` throughout. Preserve identical-line ties and isolated endpoint
ties. Check the resulting envelope independently by direct minimization at
every nonnegative pairwise intersection, every intervening interval and an
unbounded-tail sample. Determine whether `P-REUSE` has any minimizing interval
or even an isolated tie in any group.

Report the full exact boundaries and identify which ordinary comparator, or
combination of comparators, excludes `P-REUSE`. Do not assume that pooling
categories and multiplying only consumer-stage prices are the same operation:
the latter distinguishes where each category was spent.

This is arithmetic on frozen execution paths. Repricing does not rerun a
producer, change its search, reallocate its budget, trigger the governor or
validate successful execution at a new account. In particular, observed bills
and bills plus the separately protected terminal reserve remain distinct from
actual low-budget executions. No conclusion about alternative unexecuted
algorithms, physical CPU/heap prices, population performance or infinite
request horizons follows.

Save one observer script and its hash before running it. Write all new results
and the focused review only here. Stop after exact reconciliation, the bounded
eight-envelope calculation and focused Markdown source verification.
