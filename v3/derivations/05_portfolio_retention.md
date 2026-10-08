# P3-05 — What a retained proof portfolio must cover

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
S3 finite retention analysis. Future requests and costs are supplied here;
this is not a learned computation-purchase or stopping policy.

## 1. The exact finite retention service

Fix a finite declared family of possible future receiving requests j. Each
has a nonempty incumbent sublevel Qj, a fixed loss difference dj, and a target
bound Bj. Every retained certificate i has its recorded domain Gi and bound
bi. For each request/certificate pair, permitted maps and positive scales are
fixed in advance; no subsequent search over a more powerful map library is
silently included. Some pairs can be excluded by units or source types.

Let U be the tagged union of pairs (j,y) with y in Qj. Define Ui as those pairs
for which certificate i has at least one permitted map satisfying the CT05-6
old-domain and corrected receiving-loss obligations. Computing or checking Ui
is part of the input cost. It is not a free complete-model oracle.

**CT05-19 — finite portfolio-retention reduction.** With fresh direct proof
disallowed and the fixed choices above, a retained library I has a pointwise
portfolio certificate for every requested bound exactly when

```math
\bigcup_{i\in I} U_i=U.
```

Necessity is the witnessing certificate required at every receiving point.
For sufficiency, select a witnessing admitted certificate at each point and
use the finite singleton cover from CT05-8. This is a mathematical existence
statement within the finite fragment; a capped implementation may still reject
an oversized expanded expression or witness tree.

With additive nonnegative supplied retention costs ci, minimum-cost retention
therefore reduces exactly to **weighted set cover on these incidence sets**.
This is an application of an ordinary combinatorial problem, not a new set-cover
algorithm or general complexity theorem. A certificate whose coverage is a
subset of another's and whose cost is no smaller can be omitted in this exact
model. The criterion concerns the *future receiving service*, not just the
current smallest numerical bound.

The cost model assumes independently admitted reusable records. If records
share bootstrap evidence, require dependency-closure replay, or have different
per-query checking costs, simple additive ci need not describe actual cost.
Include those relationships explicitly or retain a weaker conditional claim.
The theorem is not a license to discard the proof dependencies required by a
later untrusted consumer.

## 2. More covered cases need not mean more completed decisions

The number (or fixed nonnegative weighted measure) of covered tagged points is
monotone and submodular in I: adding Ui covers only points not already in the
union, so its marginal gain decreases as that union grows. This familiar
coverage property does **not** transfer to the number of wholly certified tasks.

Let

```math
 H(I)=\sum_j w_j\,\mathbf{1}\!
       \left[Q_j\subseteq\bigcup_{i\in I}U_i^{(j)}\right],
 \qquad w_j\ge0.
```

A task needing two complementary certificates has H({A})=H({B})=0 but
H({A,B}) positive. Thus H is not generally submodular. A ranking by current
marginal task gain per storage unit can miss useful combinations completely.
This is a precise limitation of that selection rule, not of every budgeted
reasoning strategy.

### Arbitrarily poor singleton-gain greedy retention

Take a main request of weight one that requires A and B together, and a second
request of weight epsilon in (0,1) served by D alone. Each certificate costs
one, and the storage budget is two. A and B have zero initial task gain; D has
epsilon. Greedy immediate task gain selects D. Its remaining slot cannot finish
the main request, whereas choosing A and B would give value one. The ratio is
epsilon, arbitrarily small. This proof needs neither probability forecasts nor
a hidden optimum value oracle.

An actual receiver fixture realizes this cover using two conditional U-unit
certificates on x=0 and x=1 for the main U-unit comparison; a V-unit certificate
serves the other query. No conversion between U and V is declared. Each query
has a fixed action difference, identity proof maps only, and direct proof is
disabled for this diagnostic. All eight libraries can be checked explicitly.
Fresh symbolic proof happens to be cheap in this small fixture, so the example
is **not** an adverse example against the strongest unrestricted ordinary
reasoner. It isolates complementarity in the specified retained-proof service.

## 3. Relevance to the remaining programme

This connects the joined-domain receiver to the practical retention question:
which old arguments still support the future comparisons that matter? It
explains why a currently weak or locally useless support can remain valuable
alongside another support, and why counting individually improved bounds is
an incomplete progress measure. The exact query family, admissible maps,
units and resource accounting determine the result.

P3-07 can later investigate learned acquisition and retention choices under an
explicit feedback model. This note does not begin that task, estimate future
request frequencies from missing data, or claim an efficient policy for the
set-cover instance. The contribution here is the scoped reduction and witnessed
failure of a tempting local proxy within the current finite interface.
