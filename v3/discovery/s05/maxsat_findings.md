# Weighted repair receipts that certify useful actions

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. [Implementation](maxsat_repair.py),
[complete source, certificates and results](maxsat_repair_results.json).
This is a finite direct weighted-budget service. It does not implement the
production incremental MaxSAT/proof baseline identified in
[next workloads](next_workloads.md).

## A source whose numerical value comes from checked repairs

Fix hard clauses A, soft clauses C_j and positive integer violation weights
w_j. Define J(x)=sum_j w_j 1[x violates C_j] and

```text
C* = min_(x satisfies A) J(x).
W  = sum_j w_j.
```

The source supplies a feasible public incumbent, checked and charged equally
to every controller, so C* is finite and lies in [0,W]. A budget query asks
whether some hard-feasible x has J(x)<=b.

A returned assignment is checked against the hard clauses, then its actual
objective v=J(x) is evaluated in one paid pass over the soft clauses. This
supplies C*<=v and certifies feasibility for **every** budget b>=v. It can
improve the upper frontier well beyond the budget originally queried.
Failure of that assignment at a lower budget does not prove infeasibility.
Hard-witness checking and the provider's own work remain separately charged.

A checked infeasible integer budget b supplies C*>=b+1, transporting to all
smaller budgets. The retained objective interval [L,U] consequently contains
C*. The positive side retains a usable repair assignment, not only a number.
The negative side retains its proof and source/budget identity. No exact
optimum, distribution, or solve-cost law is supplied free.

The direct provider branches on variables. A negative proof leaf cites either
a hard clause false under the branch assignment, or distinct soft clauses
already forced false whose weights exceed b. An internal node covers both
values of one previously unassigned variable. A separate checker validates
those leaves and the split structure without invoking the search provider.
These are explicit weighted branch certificates, not a claim to implement
DRUP/IDRUP or a new proof calculus.

## Beyond repeated SAT: value intervals and feasible action regret

Let replacement cost p be a nonnegative integer. The best achievable saving
from having the repair option is

```text
V_p = max(0,p-C*).
max(0,p-U) <= V_p <= max(0,p-L).
width = min(U,p)-min(L,p).
```

The lower value is achievable now: use the retained repair when U<p and
otherwise replace. Its objective cost is min(U,p); the best feasible
repair-or-replace action has objective cost min(C*,p). Therefore

```text
actual action regret <= min(U,p)-min(L,p) = value-interval width.
```

A width-tau value receipt thus supplies a **feasible action within tau
objective-cost units of optimal**, without requiring exact optimization.
This gives the interface a concrete output beyond a budget's Boolean status.
Querying a new price reuses the same receipts; achieving a newly requested
precision can still require more proof work.

A simple conventional controller stops when width<=tau. Otherwise it queries

```text
b = min(U,p)-tau-1.
```

For integer tau>=0, b lies inside the unresolved interval. UNSAT raises L to
b+1 and immediately supplies the requested precision. SAT lowers U to the
checked actual cost, at most b, and the controller repeats. Each successful
SAT query decreases the relevant upper endpoint by at least tau+1; a completed
negative query ends that price's refinement. This is ordinary incumbent
improvement adjusted to the requested value, not a claim of optimal paid
query allocation. A second controller uses the midpoint of the relevant
interval. Full exact optimization uses b=U-1 until L=U.

## Actual finite workload and comparison

The saved source has 16 eight-variable repair instances. Soft clauses prefer
the all-zero configuration, with weights (1,2,3,1,2,3,1,2), so W=15. Each
instance has 18 or 24 hard clauses generated around a **public** feasible
assignment. Generation never evaluates or filters by C*. This is an explicitly
planted finite source, not a claim about a natural application distribution.

All source rows are retained. Prices 3, 6 and 9 arrive in that order; the
requested absolute value tolerance is one. Each arm starts from the same
checked public incumbents, owns its paid cache, uses the identical stateless
provider and receives the same objective-saturation opportunities. The exact
optimization arm supplies more precision and information than requested.

| Method | Price | Cumulative provider calls | Cumulative service units | Optima still unresolved |
|---|---:|---:|---:|---:|
| Conventional requested value | 3 | 16 | 40,439 | 16 |
| Conventional requested value | 6 | 29 | 69,327 | 12 |
| Conventional requested value | 9 | 31 | 77,646 | 11 |
| Requested-value midpoint | 3 | 16 | 40,439 | 16 |
| Requested-value midpoint | 6 | 31 | 81,323 | 11 |
| Requested-value midpoint | 9 | 33 | 89,642 | 10 |
| Full exact optimization | 3 | 34 | 92,074 | 0 |
| Full exact optimization | 6 | 34 | 92,730 | 0 |
| Full exact optimization | 9 | 34 | 93,386 | 0 |

Every requested value interval has width at most one and contains the value
from the final arm's checked exact optimum. The conventional requested-value
rule is the strongest tested controller by paid cost; midpoint refinement has
no advantage here. At price 3, its objective intervals still have widths up
to ten, so useful action precision substantially precedes identification.
At price 6, two intervals still have widths four and two. At price 9, every
unresolved optimum has only a **one-integer gap** left. The final stage nearly
identifies the optima; the stronger developmental opportunity is early
action precision and its reuse across later requests.

There were ten strict witness-saturation jumps in the conventional arm. For
example, row 0 was known only to have C* in [2,7]. A SAT query at budget 4
returned a checked repair costing 2, closing the interval to [2,2] and settling
every budget at least 2. All controls get this same improvement.

The tariff charges named source/receipt words, literal inspections, arithmetic
updates, proof-node and controller operations at one unit each. It includes
setup, storage, checking, objective scoring and reporting. It is an explicit
service model, not a complete hardware-instruction count. Final process times
were approximately 21.1, 25.8 and 28.5 milliseconds in a warm Python process;
these tiny runs are not production speed measurements. The final conventional
bill comprises 64,838 provider units and 12,808 adapter units.
Even among eight-variable, eighteen-hard-clause rows with C*=2, proving budget
1 infeasible costs 2,746, 2,346 and 1,786 provider units for rows 0, 6 and 12.
The optimum-cost distribution does not determine the proof-cost distribution.

Command: `python v3/discovery/s05/maxsat_repair.py` (the script refuses to
overwrite an existing result). A compile-only preflight preceded source
execution. Targeted fixture checks covered an unresolved capped purchase,
unchanged bounds after that cap, a checked negative frontier, objective
saturation, cache reuse, and rejection of an invalid negative proof. The main
run saved all proof trees and checked witnesses; no cohort call exhausted its
cap. This is same-model development with separately checkable certificates,
not independent adversarial confirmation.

## Objective costs and proof-service costs have distinct units

For the conventional controller, the following totals count one final action
per source row at the stated price, using the receipts acquired through that
stage. They do not assume earlier quoted actions were executed as well.

| Price | Public-incumbent/replacement cost | Retained-action cost | Exact best cost | Actual regret |
|---:|---:|---:|---:|---:|
| 3 | 46 | 42 | 36 | 6 |
| 6 | 86 | 45 | 42 | 3 |
| 9 | 107 | 45 | 42 | 3 |

Let lambda be the externally chosen conversion from one service unit to one
repair objective-cost unit. At price 9, the retained feasible actions improve
on the public-incumbent/replacement actions by 62 objective units. Charging
the **entire** 77,646-unit acquisition bill, while granting the initial-action
comparator zero service cost, gives the conservative positive-net region

```text
lambda < 62/77646 = approximately 0.00079850.
```

This is a retrospective tariff calculation, not a measured economic price or
a claim about unseen instances. Against exact optimization, the conventional
controller saves 15,740 service units but loses three objective units on the
final actions. Their exact crossover within these invoices is
`lambda=3/15740`, approximately .00019060. Above that rate the selective arm
has lower total final-action-plus-acquisition cost; below it exact optimization
is preferable. This comparison credits exact optimization's better actions.
No expected value of the additional retained information is assumed.

## Common value-source interface and next development

At each stage the result exports all [L_i,U_i] and, for k=0,...,15,

```text
F_lower(k) = #{i: U_i<=k}/16.
F_upper(k) = #{i: L_i<=k}/16.
```

These bound the CDF of C* for the **entire fixed cohort** deterministically;
no sampling margin is needed for this estimand. A larger task population
requires the earlier sampling/calibration warrant. The familiar identity
`E[(p-C*)_+]=sum_(k=0)^(p-1) F(k)` lets this source feed the common value layer.
Its price-9 mean-value interval is [99/16,110/16], enclosing the exact 102/16.
More general bounded g(C*) queries can use the same feasible-CDF interface.
Row-dependent prices or losses need the retained row/conditional information,
not the marginal CDF alone.

The constructive addition is a paid, source-bound service whose witnesses
simultaneously provide feasible actions, budget coverage and numeric value
bounds, with variable proof costs preserved. Established MaxSAT incumbent
reasoning and value identities remain established. The next application step
must include warm incremental solving and assumption-scoped certification,
and compare actual acquisition plus action costs with those stronger controls.
The present small source does not establish P3-POS01 readiness.
