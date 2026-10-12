# Closed-form tariff for the quotient audit frontier

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**

The principal proposed this simplification of
[the count-state quotient audit tree](quotient_audits.md); the helper
independently reconstructed the proof and the scope limitations below.
The earlier dynamic-programming derivation remains unchanged. The helper's
proof review adds no principal-clock credit. The principal's arithmetic checks
are recorded below; none purchases new source information or logical evidence.

## Executed arithmetic and representation change

The principal's [closed-form implementation](quotient_closed_form.py) and
[saved results](quotient_closed_form_results.json) agree with all 135 prior
independent literal audit-tree comparisons and nine larger saved count-DP
cases. These checks purchase no observations. In the 128-row middle example,
the same complete observation quote of 128 replaces 4,224 compiled count
states with one scalar plan record. This is constant many rational arithmetic
operations, not constant bit cost or a measured full-service speedup. The
separate trillion-row example checks parameter arithmetic only; no physical
trillion-row source was materialized or admitted.

The [random-order extension](random_order.md) keeps the realized cap while
giving a smaller expected tariff under internal randomization and a fixed
source, without a cost prior. That is a separate objective and not a claim
that the worst-realized optimum below can be improved.

## Contract and thresholds

Use the mandatory-cost family and its already admitted logical evidence:
the fixed auxiliary repair optimum is C; n independent mandatory costs
are a or 2a; a is positive; and an independent decision bit selects the
zero-cost member of an exactly-one pair whose other member costs H.
The price p and tolerance tau are fixed, with
$`0\leq\tau<H`$. The only informative observation channels are
a mandatory-row audit of constant tariff A and a decision-bit audit of
constant tariff D. A and D are positive and contain exactly the
resource components declared in their pricing contract.

After h high outcomes and l low outcomes, the mandatory total lies in:

```math
T\in[na+ah,\ na+a(n-l)].
```

Replacement is certified exactly when the lower endpoint plus C is
at least p minus tau. A decision audit can supply a certified optimal
repair exactly when the upper endpoint plus C is at most p plus tau.
Therefore define the integer thresholds:

```math
R=\left\lceil\frac{p-\tau-C-na}{a}\right\rceil,
\qquad
L=n-\left\lfloor\frac{p+\tau-C-na}{a}\right\rfloor.
```

Replacement is ready when $`h\geq R`$. Repair is ready when
$`l\geq L`$, after which the decision audit selects its actual
fixed repair. Because $`\tau<H`$, a repair cannot be chosen
uniformly over both decision-bit values without that observation.

The conditions are exact in this family because the admitted point
proof and witness establish the optimum C, the source product includes
both endpoints for each remaining row, and the equalities establish
that the common mandatory cost is the entire remaining scalar.

## Exact worst realized tariff

The minimum worst realized observation tariff is:

```math
J=
\begin{cases}
0,&R\leq0,\\
D,&R>0\text{ and }L\leq0,\\
(R+L-1)A+D,&R>0\text{ and }L>0.
\end{cases}
```

The first case is immediate replacement. In the second case, buy the
decision audit immediately. The all-low source never reaches replacement,
because R is positive, so any complete policy must eventually learn the
decision bit on that source. Its worst tariff is at least D.

For positive R and L, let $`K=R+L-1`$. These thresholds satisfy
$`K\leq n`$. To see this, put
$`x=(p-C-na)/a`$ and $`t=\tau/a\geq0`$:

```math
K=n+\lceil x-t\rceil-\lfloor x+t\rfloor-1\leq n.
```

Also, R can exceed n only when L is nonpositive; L can exceed n only
when R is nonpositive. No omitted positive-threshold case requires
more rows than are available.

**Upper bound.** Audit mandatory rows until R highs or L lows appear.
One threshold is reached by the Kth mandatory observation. A
replacement leaf pays at most KA; a repair leaf adds D. Thus every
compatible path costs at most $`KA+D`$.

**Lower bound.** Against any correct deterministic policy, answer its
successive new mandatory-row audits with R minus one highs followed
by L lows, then lows for every remaining row. The product source
admits the resulting fixed assignment. Before the Kth mandatory
observation, neither stopping condition holds. On this continuation,
replacement never becomes adequate because the total high count stays
below R. A repair must eventually be returned, and the independent
decision bit must therefore be observed. The policy pays at least
$`KA+D`$.

The argument also covers a policy that observes the decision bit early:
it still needs K mandatory observations on this continuation. If a state
is repair-ready but not replacement-ready, further mandatory observations
cannot reduce its worst remaining tariff below D; the all-low continuation
still forces a repair. Positive observation charges make the immediate
decision audit optimal there.

This yields the same minimax value as the earlier count-state Bellman
recursion for this contract, using a constant number of exact arithmetic
operations after its parameters and receipts have been admitted.
Integer bit complexity, input reading and proof checking are not constant
time. Actual execution still performs and checks the purchased observations.

## Where the closed form does not apply

The theorem is about deterministic minimax or **worst realized cost**
over all supported observation paths, including any internal random
choices. It is not an optimality result for worst-source expected cost
under randomized audit order.

For a concrete distinction, take n=3 and R=L=2, obtained for example
with a=1, tau=0 and $`p-C-na=3/2`$. The worst realized tariff is
$`3A+D`$. With one high row and two low rows, a uniformly random
row order reaches the repair threshold after two observations with
probability one third and after three with probability two thirds.
Its expected tariff is $`(8/3)A+D`$. The other fixed source types
do not have larger expected cost, so random ordering improves the
worst-source expectation while retaining a realized path costing
$`3A+D`$.

The decision-bit necessity also uses $`\tau<H`$. If tau is at
least H and replacement is sufficiently expensive, one fixed repair
can already meet tolerance across the two decision modes, so adding
D need not be necessary.

Unequal row tariffs, correlated modes, additional contrast or aggregate
sensors, uncertain C, or different available actions need a new argument.
If A and D price only external observations, separately retain all
source admission, equality and point-proof acquisition, quote arithmetic,
receipt checking, updates, CPU, storage and output charges. The closed
form does not turn those unpriced resources into an economic deadline
or establish superiority over the equally informed ordinary threshold
decision tree.
