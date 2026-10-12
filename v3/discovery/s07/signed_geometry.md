# Paid original-source signed geometry

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT construction. Helper overlap adds no principal-clock credit.
[Implementation](signed_geometry.py), [actual receipts and invoices](signed_geometry_results.json).

The construction completed with **three actual transformed-source negative
proof calls and one physical coordinate audit**. The checked geometry proves
`z3=1` and `z1+z2=1` for the original source. After the audit, checked model 13
has **uniform regret bound zero** while the mandatory feature's cost remains
either 1 or 100. This is a paid geometry-to-certificate bridge, not evidence of
an advantage over an ordinary reasoner with the same geometry.

## Exact extension, projection and signed objective

Let original soft clause C_j contain literals l. Introduce a fresh Boolean
variable v_j, after all original variable IDs, and add the hard clauses

`[v_j] + C_j`, and `[-v_j, -l]` for every literal l in C_j.

Together they say exactly that v_j is true iff every literal of C_j is false.
Every original feasible assignment therefore has exactly one extension to
these variables, with `v_j=z_j`, its ordered original soft-violation vector.
Conversely, projecting any extended feasible assignment onto the original
variables satisfies the unchanged original hard CNF and the same violation
identity. Empty, repeated or complementary clause literals preserve this
logical equivalence; this particular execution uses unit soft clauses.

For an integral signed row c, let `K=sum_{c_j<0}(-c_j)`. Put nonnegative
weight c_j on soft unit `[-v_j]` when c_j is nonnegative, and weight -c_j on
soft unit `[v_j]` otherwise. Zero-weight units are retained here. Its objective
is exactly

`sum_{c_j>=0} c_j*z_j + sum_{c_j<0} (-c_j)*(1-z_j) = K+c dot z`.

A raw proof of no feasible extended assignment at objective budget
`K+b-1` proves `c dot z>=b` for every original feasible repair, because both
the transformed objective and b are integral. The threshold is meaningful even
when b is negative. Two checked inequalities `c dot z>=b` and
`(-c) dot z>=-b` prove equality. An original Boolean coordinate's upper bound
can supply the other side when the checked lower is 1.

The implementation re-creates the whole definitional query during admission,
including the original source identity, fresh variable IDs, ordered original
soft clauses, sign choices, weights, offset and extended checked incumbent. It
compares the new receipt's complete query identity and budget, checks the raw
negative tree again, and compares its compiled leaves and integral lower.
Only then does it emit an inequality bound to the original source. Compact
transformed tree masks are not mistaken for original violation masks, and an
old original-source proof is not reused as a free transformed-source proof.

This is conventional exact CNF definition and weighted-objective
complementation. The useful local addition is an explicit paid admission chain
from that construction to the original-source geometric receipt. It is not a
new satisfiability theorem or a production general-purpose proof interface.

## Frozen source and actual purchases

The original source has four variables and hard clauses

```text
[-1,3], [1,-3], [-2,-3], [2,3], [3,4], [-3,4]
```

Its ordered soft clauses are `[-1],[-2],[-4]`, each originally weighted 1.
The two original checked models are 13 with violation mask 5, and 10 with mask
6. The source has no explicit `[4]` clause or original exact-one pair clauses.
Its implications entail `x1=x3`, `x2=not x3`, and `x4=1`; hence the desired
violation identities can also be derived by ordinary resolution.

The program writes its own implementation hash, full committed logical/cost
source and fixed targets before any acquisition. It then prepares and saves
all three extended queries before the first call. Before each purchase it
saves the active query or fixed audit; the returned raw receipt is saved before
projection/checking. Exceptions retain the cumulative failed prefix. The first
execution completed without a failed or repeated acquisition.

| Original inequality purchased | K | Transformed budget | Actual provider plus wrapper units |
|---|---:|---:|---:|
| z3 >= 1 | 0 | 0 | 1,316 |
| z1+z2 >= 1 | 0 | 0 | 1,050 |
| -z1-z2 >= -1 | 2 | 0 | 1,052 |
| **Total** | | | **3,418** |

Each transformed source has seven variables. Every call returns an actual raw
UNSAT proof, checked inside the complete wrapper and checked again by the
signed projection adapter. The pair receipts establish an equality available
for a later quotient construction; this tiny action gate needs only the paid
mandatory-coordinate receipt. The cost of all three is still included.

## One audit and the final fixed action

One fixed physical cost row has public possibilities

```text
(0,4,1), (0,4,100), (4,0,1), (4,0,100).
```

Hidden mode index 1, audit `(row=0, coordinate=0)`, price 105 and tolerance 0
are all committed before proof or audit outcomes. The gate receives public
possibilities and checked receipts, not the hidden index.

From `z3>=1` and nonnegative weights, every feasible repair costs at least w3.
For a checked repair mask u, the gate uses

`max(0, max_w(w dot u-w3), max_w(w dot u-105))`.

The maximum is over the admitted possibilities. It is a uniform bound on
regret against the better of replacement and the true optimal repair. Before
the audit the best checked fixed repair has bound 4. The actual audit returns
zero and leaves modes `(0,1)` compatible. Model 13 then has mask `(1,0,1)`, so
its cost is exactly w3 in both remaining modes. The bound becomes zero even
though w3 remains in `{1,100}`. The final model, original source, cost source
and mandatory-proof receipt are recorded together.

## Complete named bill and comparison limits

| Named component | Units |
|---|---:|
| Local bridge-code/source admission, definitions, repeated raw checks, storage and gates | 3,698 |
| Three complete provider/wrapper calls | 3,418 |
| Actual audit-provider software | 4 |
| Complete-provider code admission | 6,725 |
| **Total named units** | **13,845** |

The local invoice itemizes the transformation, fresh incumbent checks,
projection checks and all three receipts. Recorded process/wall times are
143,147,440 ns and 15,290,002 ns. These are separate resource observations,
not conversions into the declared software tariff. Actual external proof and
audit prices, storage duration, final export/host overhead and their rates
remain unassigned; the named bill is not a full monetary cost.

Ordinary source reasoning can derive the same mandatory coordinate and pair
equality. In particular, resolution of `[3,4]` with `[-3,4]` yields `[4]`.
A direct original-source query with objective `(0,0,1)` would avoid the fresh
definition variables, and is a strong potentially cheaper conventional route.
It was not executed here, so no measured price advantage over that route is
claimed. An ordinary policy with the same admitted mandatory proof and the
same coordinate audit attains the same zero bound. Full mode identification
would require a further informative audit such as coordinate 2, but that
second policy was not executed or invoiced and supplies no measured comparator.

The positive result is that paid derived original-source geometry can make a
large unresolved mandatory cost irrelevant to action regret. It does not show
that generic definition compilation is the cheapest way to acquire that
geometry, nor that choosing three proof targets was economically necessary for
this one gate.

## Reproduction and immutable bindings

```sh
python v3/discovery/s07/signed_geometry.py NEW_OUTPUT.json
```

This command performs **new acquisitions** and refuses an existing output.
The preserved results already contain the actual raw evidence; do not rerun
merely to obtain another bill.

Implementation SHA-256:
`d1e2278d517b07926fc4caa15b2591c16bbe5c5ec15accb698358675475aa739`.

Results SHA-256:
`edf2cd6386dee1b3725f2ba462d2315d8562bb5cb0aa67ecfa699bb9202e78fb`.
