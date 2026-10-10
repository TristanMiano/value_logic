# Static converse cutoff-cap assessment

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Independent same-model static prediction only. No execution or clock credit.

The parent proposed a second one-bit scope diagnostic: receiving difference
zero, no hard constraints, two soft rows with **distinct identities**, both
using `bit(0)`, weights $`1/p`$ and $`1/q`$, supplied witness `(0,)`, and bound
zero, where

```math
p=2^{127}-1,\qquad q=2^{127}-3.
```

Both positive weight denominators have 127 bits and satisfy the inherited
128-bit input cap. The odd numbers differ by two, so they are coprime without
needing a primality claim. Their sum is coprime to their product. Thus the
incumbent cutoff

```math
c=\frac{1}{p}+\frac{1}{q}=\frac{p+q}{pq}
```

is already reduced, with a 128-bit numerator and a 254-bit denominator.
The witness is feasible but nonoptimal: `(1,)` has rank zero and is the unique
rank minimizer; both points are in the supplied witness's incumbent sublevel.
The receiving difference zero satisfies the bound on both points.

## Exact native failure path

The [captured portfolio source](source/v3/checks/05_portfolio_transport.py)
does not reject in the bare `PortfolioProof` dataclass constructor. Both
`PortfolioCache.build` and `verify` call `_prepare`, which computes the
cutoff as an exact `Fraction` and then invokes `context_rows`. The latter
constructs a rank premise using `K.lit(cutoff)`. That calls the inherited
`K.rational` validator and applies the **128-bit input** cap to this computed
254-bit cutoff. The expected rejection therefore precedes proof traversal;
even a direct zero-loss leaf cannot bypass it through the public checker.

## ADD and ordinary direct paths

The [recording ADD producer](source/v3/checks/05_add_evidence.py) treats the
cutoff as a computed terminal under its 4,096-bit cap. The
[independent receiver](source/v3/checks/05_add_evidence_check.py) independently
sums the incumbent rank as `Fraction`, reconstructs the checked rank comparison
and requires that same terminal. These values are well inside their component
and wire integer bounds. No 128-bit recast of the cutoff occurs in these
direct ADD evidence paths.

In the inspected service v5, the ordinary direct receiver likewise retains an
exact `Fraction` cutoff. Its zero-loss global interval screen can establish
the requested bound. `common_report` compares the exact cutoff and does not
recast it through `K.rational`. These observations predict logical acceptance
of the ADD and ordinary direct paths if the parent supplies adequate funding;
they do not constitute paid execution or a budget guarantee.

The ADD-to-old-domain adapter has a separate explicit
`K.rational(M.rank_bounds(...)[0])` step and therefore reimposes the 128-bit
cutoff cap. Successful direct ADD evidence would not by itself imply successful
admission of that same 254-bit cutoff into the old portfolio domain adapter.

This candidate would demonstrate a different implementation boundary from
the already executed large-negative-constant witness. The earlier record and
its results remain unchanged. The parent owns any prospective fixture,
funded failure/recovery execution and conclusion drawn from that execution.

Sources inspected are the unchanged closure in [source_manifest.json](source_manifest.json):
old portfolio `9bf64849…`, producer `1e40f1bf…`, receiver `1f396bbb…`, and
service v5 `b96cae82…` as preserved in the separate
[v5 audit](../service_audit_v5/review.md). No source edit or cap relaxation is
proposed here.
