# Fixed-path economic robustness: independent reconstruction

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Same-model independent, nonblind, retrospective DEVELOPMENT observer review.
Zero principal-clock credit. No worker, parent analyzer or prior evidence edits.

## Findings

The source-bound reconstruction confirms four distinct statements:

- Across each complete six-request stream, `O-ENUM-RECEIVER` uses no more of
  any pooled tariff category than `P-REUSE`: **eight of eight groups**.
- Requestwise componentwise dominance holds in **forty-five of forty-eight**
  paired comparisons. The three native-call exceptions are preserved below.
  At the original unit tariff, ENUM nevertheless has lower total cost in
  **all forty-eight** requestwise comparisons.
- Repricing consumer work by any nonnegative multiplier leaves ENUM as the
  sole cheapest recorded method in seven groups. The larger complementary
  resident group switches from ENUM to `O-ADD-WARM` at the exact boundary
  $`2556095/1236394`$, with both methods tied there.
- `P-REUSE` never enters that six-method, ordinary-inclusive envelope,
  **including isolated ties**. An ordinary method strictly dominates its
  fixed nonconsumer and consumer cost coordinates in every group.

These are exact statements about fixed recorded execution paths. They do not
execute a new price, allocate a new account, change the resource governor,
or imply a statistical population result. The two repricing operations used
above have different meanings and are distinguished explicitly below.

## Evidence reconciliation and scope

The observer reads the immutable [primary v5 records](../../../development/primary_v5/completed_units.jsonl)
and [primary analysis](../../../development/primary_analysis_v1/analysis.json).
It imports neither the parent analyzer nor any worker. Source and artifact
seals are checked before reconstructing each total directly from
`invoice.by_stage`.

All 288 successful primary delivery rows, 9,397 stage/category CSV rows,
48 complete method-stream totals and eight published unit-price comparison
cells agree exactly with the independent reconstruction. Every field in the
published per-request and total CSVs agrees, including the separate observed
bill and bill-plus-reserve threshold fields. The successful output strings
agree across methods and recipient modes for each of the 24 logical input
cases. This is record reconciliation; proof correctness was not rerun and
proof blobs were not independently rechecked in this economic task.
[Reconciliation receipt](run/results.json)

The eight groups are four fixed families times two recipient modes. Each
contains six methods with six successive requests. The forty-eight paired
ENUM/P-REUSE request comparisons are eight groups times six requests. These
counts describe the finite experiment; they are not independent statistical
trials. All methods completed every service used in these comparisons.

Twenty-five inventoried input/source files remained unchanged. The observer
source was saved before its single run. The parent owns the original worker
executions and the separate interpretation of those experiments.

## Pooled category comparison

For each group and method, form a vector by summing every named tariff
category across stages and all six requests. Let $`v_E`$ and $`v_P`$ denote
the ENUM and portfolio vectors. The recorded comparisons satisfy

```math
v_{E,j}\le v_{P,j}
\quad\text{for every category }j
\quad\text{in each of the eight groups}.
```

Consequently, for any nonnegative price vector that assigns a common price
to each category wherever that category occurs,

```math
\sum_j\lambda_jv_{E,j}\le\sum_j\lambda_jv_{P,j},
\qquad\lambda_j\ge0.
```

Strict savings require a positive price on at least one strict coordinate.
Pricing only equal coordinates, or assigning every category price zero,
can produce a tie. Thus the claim is that portfolio reuse cannot strictly
beat ENUM under such pooled common-category prices on these recorded streams.
It is not a claim that every nonnegative tariff gives a unique ENUM winner.

ENUM has strictly fewer observed Python opcodes, native calls, current-request
bytes, current proof input/output bytes and serialized live-state byte-periods
in every pooled group. On the six nonconstant groups it also avoids the old
request and old-proof input/output costs. The program/hash/length-probe/source
record fees, current receipt output bytes, delivery events and publication
events are equal. The full vectors, including every coordinate and exact
difference, are saved in [pooled_category_comparisons.json](run/pooled_category_comparisons.json).

At the original unit prices the complete costs are:

| Family | Recipient | ENUM units | P-REUSE units | ENUM saving |
| --- | --- | ---: | ---: | ---: |
| Constant, 3 bits | Fresh | 842,657 | 1,370,865 | 528,208 |
| Constant, 3 bits | Resident | 842,669 | 1,370,613 | 527,944 |
| Parity reassociation, 6 bits | Fresh | 2,177,683 | 9,698,866 | 7,521,183 |
| Parity reassociation, 6 bits | Resident | 2,177,695 | 5,551,884 | 3,374,189 |
| Complementary, 3 parity bits / 5 total | Fresh | 1,981,733 | 8,541,209 | 6,559,476 |
| Complementary, 3 parity bits / 5 total | Resident | 1,981,745 | 6,324,992 | 4,343,247 |
| Complementary, 5 parity bits / 7 total | Fresh | 5,017,653 | 15,357,085 | 10,339,432 |
| Complementary, 5 parity bits / 7 total | Resident | 5,017,665 | 9,903,248 | 4,885,583 |

These sums include each method's recorded setup and source enrollment as well
as subsequent requests. They do not provide method-specific minimum program
sizes or physical resource costs.

## All requestwise comparisons and the three exceptions

The [complete forty-eight-row comparison](run/request_category_comparisons.json)
preserves both vectors and their signed differences for every request. The
only failures of requestwise componentwise ENUM dominance occur in the
resident parity-reassociation group:

| Request index / input edit | ENUM native calls | P-REUSE native calls | ENUM total | P-REUSE total |
| --- | ---: | ---: | ---: | ---: |
| 2 / `edit/01` | 8,456 | 8,149 | 280,419 | 381,390 |
| 4 / `edit/03` | 8,583 | 8,576 | 286,226 | 391,880 |
| 6 / `edit/05` | 9,283 | 8,797 | 302,689 | 402,535 |

ENUM spends respectively 307, 7 and 486 additional native-call events on these
individual requests. Every other compared category is no larger. Its total
unit-price savings remain 100,971, 105,654 and 99,846 units. The full-stream
native-call sum still favors ENUM once all six requests and setup are included.

Therefore the correct requestwise statement is 45/48 componentwise comparisons
and 48/48 unit-price total comparisons. A sufficiently different single-request
native-call price can matter on the three exceptions; the full-stream vector
result does not erase them.

## Consumer-price envelope

For method $`m`$ in a complete group, define $`c_m`$ as its six-request sum of
`consumer_units`, using exactly the service's consumer stages:
`receiver_*`, `terminal`, `failure_terminal` and `common_source`. Define
$`a_m`$ as total units minus those consumer units. The latter is fixed
**nonconsumer** work, including producer, request-encoding and coordination
work. It must not be reported as only the `producer_*` stages.

The frozen-path repricing is

```math
L_m(\rho)=a_m+\rho c_m,
\qquad\rho\ge0.
```

All six successfully completed methods remain eligible. The observer derives
the exact minimizing domain of each line by intersecting, for every other
method $`n`$,

```math
\rho(c_m-c_n)\le a_n-a_m.
```

A positive coefficient gives an upper bound on the multiplier; a negative
coefficient gives a lower bound; an equal slope either imposes no restriction
or rules out the more expensive intercept. Intersect these with the
nonnegative half-line. All divisions use `Fraction`, all finite endpoints
are closed, and identical-line or isolated-point ties are retained.

A second check directly minimizes the six exact lines at every nonnegative
pairwise crossing, between consecutive crossings and on the final unbounded
interval. All 68 such checks agree with the half-line intersections. The
complete coordinates, constraints, exact domains and check points are saved
in [price_envelopes.json](run/price_envelopes.json).

ENUM is the unique minimizer for all nonnegative multipliers in the constant,
parity and smaller complementary families under both recipient modes, and
in the larger complementary family with fresh recipients. In those seven
groups it has both a strictly smaller intercept and a strictly smaller
consumer coordinate than every other recorded method.

The only switching group is `complementary_k5_n7`, resident:

```math
L_E(\rho)=345252+4672413\rho,
\qquad
L_W(\rho)=2901347+3436019\rho.
```

Here $`W`$ denotes `O-ADD-WARM`. Their difference is

```math
L_W(\rho)-L_E(\rho)=2556095-1236394\rho.
```

Thus the exact envelope is:

| Multiplier range | Minimizing method |
| --- | --- |
| $`0\le\rho<2556095/1236394`$ | `O-ENUM-RECEIVER` |
| $`\rho=2556095/1236394`$ | `O-ENUM-RECEIVER` and `O-ADD-WARM`, tied |
| $`\rho>2556095/1236394`$ | `O-ADD-WARM` |

The first boundary is between two ordinary controls. The envelope contains
nine nonempty closed method intervals across the eight groups, and no
`P-REUSE` interval or isolated tie.

## Why P-REUSE cannot enter this envelope

In seven groups, ENUM's intercept and consumer coordinate are both strictly
smaller than P-REUSE's. In the remaining larger complementary resident group,
the portfolio line is

```math
L_P(\rho)=5960247+3943001\rho.
```

Warm ordinary ADD strictly dominates both coordinates:

```math
L_P(\rho)-L_W(\rho)=3058900+506982\rho>0
\quad\text{for every }\rho\ge0.
```

This supplies a direct exclusion certificate, including multiplier zero.
No fine endpoint rounding or omitted tied minimum is responsible for the
portfolio's absence.

The distinction from pooled category prices is material. In this last group,
portfolio reuse would beat ENUM alone when
$`\rho>5614995/729412`$, because ENUM assigns more of its smaller overall work
to consumer stages. Warm ordinary ADD already beats both at those prices.
Pooled category dominance remains correct: giving receiver stages a special
multiplier prices the same category differently depending on where it occurs,
which is a different transformation from the pooled common-category price
vector. The no-entry conclusion is specifically for the declared two-coordinate
envelope with nonconsumer prices fixed at one.

## Interpretation and reproducibility

The counts and execution paths remain fixed throughout this analysis. A new
price could change whether a resource governor lets those paths finish, or
motivate a different search or certificate protocol. Neither effect is
simulated here. The unspent 1,024-unit protected terminal reserve is an
admission constraint, not an extra consumed-cost term silently added to these
lines. Existing observed bill and bill-plus-reserve fields remain separately
identified; no successful execution at a new threshold or multiplier is
inferred.

The calculations concern six-request DEVELOPMENT streams under the named
event/byte tariff. They retain all setup, source, input, proof, checking and
live-state costs already present in the records. They do not establish a
physical CPU/heap ordering, an infinite-horizon result, a minimum ordinary
implementation cost or a stronger affirmative Q3 superiority claim.

To reproduce the observer without running a worker, use a fresh output path
from the repository root:

```bash
python v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/economic_robustness_v1/source/observer_v1.py \
  --repository . \
  --inputs v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/economic_robustness_v1/input_manifest.json \
  --out /tmp/rp3bb_economic_robustness_reproduction
```

| Artifact | SHA-256 |
| --- | --- |
| Sealed primary record stream | `555d0af18e958053f06b14940e6a725d28514877191a0982d976c91eb210254e` |
| Input/source inventory | `7bd5c7850accc29b405a5171de1da4ca4ca5fcd897ab95bfd012565df4e14369` |
| Independent observer | `292c52b4bf9fca0337cd6c2bd66b452f176c0a5f26f226aa4606f8cdb1b0ffb0` |
| Complete results | `9830007bfcf9109b535d2777b3e861251ede549911f5779577b3f962037304f1` |
| Pooled vectors | `1fb94e7cff839f367e0f4bff1f767bb411cbaa32a31142d8de012dca2237f506` |
| Requestwise vectors | `73b5f496e85bfbe692fb6a9e49bbfdc0388df57d5797daaaa59163a7baef9571` |
| Exact price envelopes | `ba3fc03948f19e1d3cefb20f6f9683bffb4db3ba9ea25812909b636d2ae4be94` |

The focused presentation receipt checks only the listed new Markdown sources
and their links. No global historical-style or live-rendering claim is made.
