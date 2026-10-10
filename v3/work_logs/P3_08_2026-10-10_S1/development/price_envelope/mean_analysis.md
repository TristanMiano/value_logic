# One configuration across recorded seeds — DEVELOPMENT

Contributor: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10.
This is the final principal interpretation of the declared
`mean_policy_contract.md` analysis of already exposed development records.
It executes no policy, private scorer or reporter. Its input is the sealed
234-line `run_v1` catalogue, whose lines have been independently reconstructed
from the underlying public records and evaluator truth.

## Exact question and eligibility

The individual-record envelope permits a different hindsight winner for each
seed. A separate question requires one entire configuration across seeds 11,
29 and 47. Group by scenario, source family and every configuration field except
seed. This retains the acquisition parameter, cache kind, hard mode, selector
and solver. A stochastic group must have each of the three seeds exactly once.
A declared deterministic common control has one seed-11 record reused with
weight one; it is not three executions or three independent observations.

The resulting catalogue contains **90 means**: 26 cold, 38 repeated and 26 cheap
configurations. All 12 repeated-tape selected-provider configurations have all
three seeds and remain. Twelve incomplete cold/cheap reuse configurations have
only seed 11 and are listed in `mean_run_v1/results.json`; they are omitted from
both sides of the aggregation comparison. None receives imputed seed outcomes.
The output key must be paired with its scenario to identify a mean uniquely.

Every record's cost is local units plus the same 50,115-unit installed-source
charge, using the previously audited 1,841-unit transfer for old records. The
arithmetic means retain rational values instead of rounding errors or bills.
Each acquisition parameter stays fixed as external lambda varies. Three named
seed outcomes do not establish that this mean equals fair-bit expectation.

## Mean-policy frontier

For configuration j and recorded seed s, write
`L_js(lambda)=E_js+lambda C_js`. Its aggregate line is
`M_j(lambda)=(L_j,11+L_j,29+L_j,47)/3`. Exact intersections of all inequalities
`M_j<=M_i`, with lambda nonnegative, retain every optimal closed interval.

**No broker mean line attains the resulting envelope, even at zero-price
endpoints. Every retained frontier line is an explicitly ordinary control.**
There are 32 optimal closed configuration intervals, 12 of positive width;
coincident constants count as distinct supplied configurations. Their ordering
and exact switch prices are:

| Scenario | Increasing-price optimal configurations | Exact switch prices |
|---|---|---|
| Cold mixed | Exact DPLL; hashed combination at acquisition parameter 1/100000; hashed combination at 1/10000; bounded enumeration; supplied action one | `1/2638686`, `13/920073`, `61/2034120`, `6/130517` |
| Repeated tape | Hashed exact cache; bounded enumeration; both constants | `44/1587537`, `5/64501` |
| Cheap structure | Linear exact cache; both constants | `32/15339` |

The table lists positive-width pieces; all zero-price-only ties remain in the
complete output. Every adjacent listed piece includes its shared endpoint.
The same common source term cancels from comparisons but remains in every
displayed objective. This is a finite mean-record claim about the given
catalogue. It is not a universal ordinary dominance theorem or a result for
an acquisition policy newly executed at every external price.

## Why separate hindsight choices look better

Using the **same balanced catalogue** on both sides gives

```math
\frac13\sum_s\min_j L_{js}(\lambda)
\le \min_j\frac13\sum_s L_{js}(\lambda).
```

For any fixed j, each summand on the left is at most its corresponding
`L_js`; average that inequality and then minimize over j. Since the finite
minimum is attained, equality holds exactly when at least one configuration
minimizes every seed's objective. If no common minimizer exists, at least one
of the three nonnegative gaps is positive for each fixed configuration.

At the already displayed price 1/30000, the differences of the right side
minus the left side are exactly `730411/90000` on the cold tape, `1241/300`
on repeats and zero on cheap structure. Bounded enumeration minimizes the
fixed-configuration mean in the first two cases; linear exact caching does so
in the last. These are hindsight configuration-selection gaps. A method that
obtains such choices by solving/evaluating alternatives would need its own
information and computation bill. No such selection service is executed here.

This result sharpens the interpretation of the individual-seed price windows:
the saved finite-feedback records can be useful at intermediate prices, but
their advantage among those records does not survive this balanced aggregate.
Their ordinary-kernel equivalents remain available throughout. Both the
positive individual result and this aggregate negative are preserved in the
principal contribution assessment, with affirmative Q3 still open.
