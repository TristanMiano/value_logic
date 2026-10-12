# Complete audit/proof bundles without enumerating logical outcomes

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT auxiliary derivation and construction for S28-B1; no auxiliary
time is added to the principal clock. The parent session owns the integrated
controller and its readiness judgment. Existing frozen evidence is unchanged.

The concrete extension is an inexpensive complete-query quotation. It uses
the integer objective lattice, scalar-anchor transport and monotonicity to
decide whether a logical purchase can finish a child state after an audit.
A multi-call reserve handles child states needing more than one complete
logical answer. These are useful implementation consequences of conventional
robust decision planning; no originality of minimax regret, gcd arithmetic,
binary search or decision trees is claimed.

## 1. The admitted information state

Retain the fixed logical source and cost contract in
[source-anchor transport](../s06/source_anchor.md). Feasible violation vectors
are Boolean, costs are nonnegative, and each output is a single checked fixed
repair or replacement. Every row has a nonempty set of public cost modes.
The target is the cohort sum, with no probabilities over modes:

```math
C^*(w)=\min_{z\in F}w\cdot z,\qquad
w\in W=\sum_{i=1}^{N}\mathrm{conv}\{m_h:h\in Q_i\}.
```

Paid checked anchors satisfy $`0\le\ell_h\le C^*(Nm_h)`$. Let B be the best
current source-anchor certificate among retained feasible actions and
replacement at price p. Define the warranted common lower bound and the
coordinate enclosure by

```math
L=\frac1N\sum_i\min_{h\in Q_i}\ell_h,\qquad
\overline w_j=\sum_i\max_{h\in Q_i}m_{hj}.
```

An audit partitions one public row-mode set by its observable value. A
hypothetical partition used to price a plan is not an observation. The source
state changes only after an actual source-bound receipt. Existing independently
checked tree or dual certificates remain usable alongside this representation.

## 2. A cheap improvement: round both logical outcomes to the gcd lattice

For a nonzero nonnegative integer query objective q, let

```math
g=\gcd(q_1,\ldots,q_m)>0,\qquad k=\left\lfloor\frac bg\right\rfloor.
```

Every Boolean objective value is a multiple of g. Consequently a checked
SAT answer at budget b supplies an objective upper bound gk; a checked UNSAT
answer supplies the lower bound g(k+1). This follows directly by writing
every coefficient as g times an integer. It does not require enumerating
objective masks or logical models. For g=1 these are the original b and b+1
endpoints. An identically zero objective has no useful two-outcome purchase
under this interface and is returned as uninformative.

Set

```math
\alpha(q)=\sum_j\max(\overline w_j-q_j,0),\qquad
d_h(q)=\sum_j\max(q_j-Nm_{hj},0).
```

For every possible checked SAT witness u, binary features give
$`w\cdot u\le gk+\alpha(q)`$. The old actions and replacement remain available,
so a valid positive-branch quotation is

```math
B_+(k)=\min\!\left(B,
 \max\{0,\min(p,gk+\alpha)-\min(p,L)\}\right).
```

A checked negative cut gives the new anchor bank

```math
\ell'_h(k)=\max\{\ell_h,0,g(k+1)-d_h(q)\}.
```

Re-evaluate the retained fixed-action certificates using these anchors and
retain the old bound; call the result $`B_-(k)`$. The complete-call bound is
the maximum of its two branch quotations. Both improve weakly on the previous
unit-step quote because the SAT endpoint only decreases and the UNSAT endpoint
only increases. They are exactly equal to the old formula when g=1.

This is conditional on the actual complete provider contract and independent
answer checking. A no-progress or interrupted outcome retains B. Raw native
status, an unchecked negative flag or an anticipated successful solve cannot
justify the anchor update.

## 3. Exact feasible budget interval for this quotation

Suppose the state is unclosed: $`B>\tau`$. Replacement is included in B, so
its bound $`\max(0,p-L)`$ also exceeds tolerance. Therefore
$`L+\tau<p`$. The positive branch closes exactly when

```math
k\le k_{\max}
 =\left\lfloor\frac{L+\tau-\alpha(q)}g\right\rfloor.
```

Meanwhile each new anchor lower is nondecreasing in k; each retained action
bound and their minimum are nonincreasing. Hence $`B_-(k)`$ is nonincreasing.
At k=-1 the negative update adds only zero and leaves every nonnegative old
anchor unchanged, so it cannot close an unclosed state.

**Existence theorem for the implemented quotation.** A nonnegative closing
budget exists if and only if $`k_{\max}\ge0`$ and
$`B_-(k_{\max})\le\tau`$. Thus one evaluation of the negative branch at
the largest SAT-feasible budget decides existence. No search over logical
truths, solver outcomes, hull vertices or objective masks is needed.

The qualifying indices form an interval from the smallest negative-feasible
index to the largest positive-feasible index. If the full interval is useful,
integer bisection between failing index -1 and the successful endpoint finds
its lower end. For successful indices from a through c, the ordinary integer
budgets are exactly

```math
ga\le b\le g(c+1)-1.
```

[lattice_quotes.py](lattice_quotes.py) implements both operations. The default
closing-query function chooses one canonical budget, g times the largest
eligible index. Optional `exact_interval=True` computes the lower end.
An admitted feasible objective upper can additionally restrict the search to
budgets below it. An already closed state needs no purchase.

“Exact” here describes existence within this conservative quotation. Failure
does not prove that no useful query exists: the coordinate enclosure, common
scalar lower and retained action bank can all be loose. The chosen largest
budget also need not minimize regret or CPU cost; it meets the requested
tolerance when the quotation succeeds.

## 4. A whole complementarity family with zero singleton gain

Let H be any integer at least two. The hard source is the clause
$`x_1\lor x_2`$, with soft violations corresponding to true x1 and true x2.
There is one cost row with modes (0,H) and (H,0), replacement price H+1,
and tolerance zero. Initially only the both-true feasible witness is retained.
A paid initial lower proof at objective (H,H), budget zero, does not raise
either mode-anchor lower above zero.

The initial bound is H. A coordinate audit identifies the mode but leaves
the only retained repair costing H, so each audit singleton has zero gain.
Every possible logical purchase also has zero guaranteed gain while the
cost source remains unobserved: the three feasible repairs are (1,0), (0,1)
and (1,1), and each has regret H at at least one mode endpoint. Even complete
logical knowledge cannot select one fixed repair with a smaller worst regret.
This argument covers every logical query, beyond the finite illustrative menu.

After the actual audit, query the identified cost vector q at budget zero.
Its gcd is H. Both checked answers have a terminating certificate:

| Answer | Warrant after the audit | Output and bound |
| --- | --- | --- |
| SAT | New witness has actual cost zero. | Return that checked witness; regret zero. |
| UNSAT | Every feasible repair has actual cost at least H. | Existing both-true witness costs H; regret zero. |

The actual formula makes SAT possible and UNSAT impossible, but the planner
does not need a free solution of the formula to discard a branch. It quotes
both conditional answers and supports both. The audit followed by the complete
logical purchase guarantees zero regret, although each singleton has zero
guaranteed gain. This remains a fixed-action service after each observed outcome;
a randomized expected-regret output would be a different duty.

The previous unit-step quote cannot close this family at zero tolerance.
Within its useful integer budget range its worst branch is
$`\max(b,H-b-1)`$, whose minimum is $`\lfloor H/2\rfloor`$. The lattice
quote closes at zero. This is a strict capability improvement of the quote,
with an explicit scale family rather than a favorable runtime observation.

The initial action bank is part of the example. A strong ordinary controller
may propose and cheaply check one of the obvious single-true assignments after
the audit; it need not purchase this full branching proof. All such capabilities
remain available to a fair comparison. The example establishes complementarity
and a tighter quotation, not economic superiority over direct checking.

## 5. Several complete queries can form one terminating leaf

A one-call leaf can fail even when its cost source is fully known. A compact
multi-call reserve avoids explicitly unfolding every logical outcome tree.
This extension was proposed by the principal after the first broad s07 run;
the following clipping argument checks its guarantee.

Keep q fixed and maintain a checked integer bracket for its clipped point
optimum. Let lower Lq and feasible upper Uq be admitted, and let p be an integer:

```math
l=\min(p,L_q),\qquad u=\min(p,U_q),\qquad G=u-l\ge0.
```

If an admitted lower is rational, its ceiling is still valid for an integer
objective and supplies an integer bracket endpoint. A rational price instead
requires an exact common scaling or a separately derived rounding rule.
When u=p, replacement supplies the clipped upper; no witness of objective p
is required.

For $`l<u`$, query budget $`b=\lfloor(l+u)/2\rfloor<p`$. On SAT update the
upper using the checked witness. On UNSAT update the lower using the checked
negative cut. The resulting gap is at most $`\lfloor G/2\rfloor`$ in either
branch. Gcd rounding can only improve this bound. After at most t such calls,
the gap is at most $`\lfloor G/2^t\rfloor`$.

Suppose the fixed source state warrants transfer margins alpha and delta for
every compatible w and Boolean z:

```math
(w-q)\cdot z\le\alpha,\qquad (q-w)\cdot z\le\delta.
```

The retained q witness or replacement and the point lower then give

```math
B_W\le
\max\{0,\min(p,u+\alpha)-\min(p,\max(0,l-\delta))\}
\le (u-l)+\alpha+\delta.
```

The first inequality remains valid when u=p because replacement costs p.
For the second, the upper is at most u+alpha while the clipped lower is at
least l-delta. Therefore a nonnegative residual
$`r=\tau-\alpha-\delta`$ permits a reserve of t calls whenever
$`\lfloor G/2^t\rfloor\le r`$. Equality of transfer width and tolerance may
require an exact point bracket; its finite reserve still terminates. Stop
earlier whenever the full retained certificate service closes.

Every reserved call needs the same admitted finite completion contract. Its
provider/checker wrapper can be bounded by t times a valid per-call ceiling;
actual receipts and additional local processing remain charged. This is a
guarantee about complete answers and a fixed source state, not a learned native
runtime law or a reason to omit unresolved work.

## 6. Preserve row dependence in the transfer margin

The coordinate-box choice has
$`\alpha+\delta=\sum_j(\overline w_j-\underline w_j)`$ whenever q lies
inside the box. Moving q inside it cannot reduce that sum. This can unnecessarily
force further audits. A cheap row decomposition gives a useful alternative.

Choose public reference vectors r_i summing exactly to q. Their coordinates
may be signed rational numbers. Define

```math
\alpha_r=\sum_i\max_{h\in Q_i}\sum_j\max(m_{hj}-r_{ij},0),\qquad
\delta_r=\sum_i\max_{h\in Q_i}\sum_j\max(r_{ij}-m_{hj},0).
```

For every latent row configuration and every Boolean z,

```math
(w-q)\cdot z
=\sum_i(m_{h_i}-r_i)\cdot z
\le\sum_i\sum_j\max(m_{h_i j}-r_{ij},0)
\le\alpha_r.
```

The reverse difference gives delta_r. Convex combinations preserve the
inequalities. Neither proof needs independence or a product enumeration.
Each margin may be independently minimized with any other valid upper bound.

[row_margins.py](row_margins.py) compares the coordinate box with two simple
reference choices. One uses integer row midpoints and places the residual
between their sum and q in the last unresolved row, preserving already known
rows when possible. The other uses q/N for every row. Supplied exact
decompositions are also supported. There is no optimization claim for these
choices. For the anticorrelated row with modes (0,2) and (2,0), q=(1,1) gives
alpha=delta=1, versus box margins 2 each. Distinct already known rows have
zero row-margin contribution when their reference equals their known vector.

This reduces the source-width term in the multi-call reserve without logical
model, Boolean objective-mask or source-product enumeration in the controller.
Known different rows explain why a uniform q/N split alone is insufficient:
its artificial per-row discrepancy can persist after all costs are known.

## 7. Complete plans and their comparison scope

A finite audit plan chooses a query or a terminating logical reserve in each
observed child. Its guarantee takes a maximum over every compatible audit
answer. A positive local singleton score is unnecessary: the complete child
plans can have positive joint value. Actual logical branches use their proved
quotation/reserve, so they do not require enumeration of source truths.

The appropriate ordinary reference remains robust elicitation with the same
source, action proposals, lower proofs, early stopping and planning menu.
Small AND/OR recursion is conventional decision planning, and full tree
quotation itself must be paid. A symbolic path cost can be retained as
$`n_A A+\sigma K+H_{\mathrm{path}}`$, where A prices an observation, K is
the named operation count, and H contains unpriced CPU, storage, serialization
and other relevant implementation costs. Without bounds or prices for these
terms, an observation-count or provider-unit improvement is not a total
economic guarantee.

The existing [primary-source comparison](../s06/acquisition_sources.md) was
extended by reading these primary PDFs directly during s07:

- **Boutilier, Patrascu, Poupart and Schuurmans (2006)**,
  [Constraint-based Optimization and Utility Elicitation using the Minimax Decision Criterion](https://www.cs.toronto.edu/~cebly/Papers/BPPS-aij06.pdf):
  Section 4.2.2, printed pp. 20–21, already supplies early-stop regret bounds
  and reuse of generated constraints. Sections 5.2–5.4 supply worst-case gap,
  current-solution and both-outcome query evaluation. Footnote 20 on printed
  p. 36 explicitly describes extending lookahead to an optimal finite-stage
  query plan, limited by computation. These are close prior mechanisms; the
  logical receipt/lattice/source-transport interface is the scoped adaptation.
- **Golovin and Krause (2010)**,
  [Adaptive Submodularity: A New Approach to Active Learning and Stochastic Optimization](https://www.cs.cmu.edu/~dgolovin/papers/colt10.pdf):
  Section 2 specifies a known outcome distribution and adaptive policies;
  Section 3, Definitions 1–2, Proposition 3 and equation (5), makes its
  diminishing-return property a condition on conditional expected marginal
  gains. Source containment and monotone retained evidence alone supply neither
  that prior nor a greedy approximation guarantee for this certificate objective.

No result from either source is silently imported as a theorem about the new
acquisition objective. The constructive family explains why a singleton-only
controller can stall; it does not establish a broad failure of those papers'
algorithms or assumptions.

## 8. Actual evidence and exact limits

[bundle_example.py](bundle_example.py) fixes its cost source before acquisition,
executes a new paid initial UNSAT proof and checks its raw tree, admits the
both-true witness, prices both audit outcomes, then obtains one actual source
observation and one actual child SAT response. Its
[saved result](bundle_example_results.json) has initial bound 2, zero singleton
guaranteed gains, complete bundle bound 0 and actual final bound 0. The child
provider/checker costs 117 named wrapper units under its prospective ceiling
269; the initial call costs 146. The finite-provider code admission costs 6,725.
These are components, not an all-in performance comparison.

The same file includes 288 objective-endpoint arithmetic cases, 96 exact
interval comparisons and 192 old/new quotation comparisons. The full retained
invoice is 234,965 named units **including reconstruction**. Reconstruction
quote calls use their normal quotation categories, so the `construction_check`
category alone is not their entire cost. No actual logical optimum or hidden
source outcome is used to choose the acquisition.

[row_margin_check.py](row_margin_check.py) separately reconstructs six small
cases with 68 exact source-configuration/objective-mask comparisons; its
[result](row_margin_results.json) records 2,317 units and zero acquisitions.
Those finite enumerations belong to the reconstruction, not the quotation.
They support the implemented arithmetic; the general guarantees are the
arguments above. The broad integrated controller evidence and current promotion
forecast belong to the principal's s07 findings and recurrence record.

To reproduce into new output locations, preserving the existing evidence:

```sh
python v3/discovery/s07/bundle_example.py /tmp/s07_bundle_example_new.json
python v3/discovery/s07/row_margin_check.py /tmp/s07_row_margin_new.json
```

Both scripts refuse to overwrite an existing result. The first command makes
new paid acquisitions and therefore creates another DEVELOPMENT execution.
The second is only a finite arithmetic reconstruction. The inherited complete
provider guard binds the exact source versions whose finite tariff is used.
