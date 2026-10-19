# Cap two is an ordinary decision tree with priced answer signals

Codex (GPT-6), s12 DEVELOPMENT derivation. Uses the same private-reset
interface as [parity_price.md](parity_price.md): fixed hidden Boolean world,
positive known coordinate fees c_i, at most two distinct-coordinate purchases
per episode, no hidden memory between episodes, and only the exact invoice is
public. A nonempty episode costs an additional fixed f>=0. There are at least
two coordinates. Receipts/source information are represented by a nonempty
set W of possible worlds; the requested deterministic output g may be arbitrary.

## Reduction, including arbitrary source constraints

The first queried coordinate i is chosen before any private answer. If a
second query is made, its answer cannot affect the invoice: there is no third
purchase and no public output other than cost. Thus the episode's invoice is
a function of x_i alone. An uninformative episode can be removed. Every
informative episode reveals x_i exactly and has one of these forms: stop on
one answer and buy a marker on the other; or buy different-priced markers on
both answers. Let m_i=min_{j!=i} c_j. The latter form is pointwise dominated
by stopping on one answer and buying a cheapest marker on the other. The
former also weakly improves by replacing its marker with a cheapest one.
Markers may use a coordinate already known from another episode; the rule
only prohibits repeating i inside the same episode.

Consequently every optimal procedure has an ordinary coordinate decision tree
with a chosen signal orientation at each node. One branch costs c_i+f, and
the other costs c_i+m_i+f. This is an exact interface reduction, not a claim
that optimizing decision trees is new or generally easy.

Write W_ib={x in W:x_i=b}, and V(W)=0 if g is constant on W. Otherwise

```math
V(W)=\min_{i:W_{i0},W_{i1}\ne\emptyset}
\{c_i+f+\max(\max(V(W_{i0}),V(W_{i1})),
                 \min(V(W_{i0}),V(W_{i1}))+m_i)\}.
```

Place the extra marker charge on the child with smaller continuation cost.
This minimizes the larger branch total. Induction on |W| gives both a
constructive policy and a matching lower bound. A positive-cost noninformative
episode cannot improve the stationary source, so omitting it loses nothing.
Randomization cannot improve a zero-error hard worst-case bound: on a finite
world set, fix a random tape on which the bound and correctness hold for all
worlds simultaneously.

For unit coordinate fees and f=0, the recursion is
V(W)=min_i max(max(V_i0,V_i1)+1,min(V_i0,V_i1)+2).
If D(g,W) is ordinary minimum worst-case coordinate-query depth, every
nonconstant task satisfies D+1<=V<=2D. The upper bound signals every query;
for the lower bound, apply induction to the child of greatest ordinary depth
of each proposed first query (the D=1 case needs one data and one marker fee).
Full conjunction attains n+1, while full parity attains 2n. Thus equal ordinary
query depth need not mean equal private-invoice price.

## Expected invoices use a different orientation

Under a specified prior P on W, let p_b=P(W_ib|W). The expected-cost recursion
for almost-sure exact output is

```math
V_P(W)=\min_i\{c_i+f+m_i\min(p_0,p_1)
                  +p_0V_P(W_{i0})+p_1V_P(W_{i1})\}.
```

Only positive-probability branches are relevant for this almost-sure contract;
zero-error on all admitted worlds is stronger. Put the marker on the rarer
answer, regardless of continuation-cost imbalance. Under independent fair
unqueried bits and unit prices, this is 3/2 times the ordinary expected number
of queries for any chosen tree. For parity of n bits it is 3n/2, whereas its
hard worst-case invoice is 2n. The same-world source and priced exact readout
remain essential; this is not a statement about noisy invoice inference.

## Cheap-screen plan

Compare these recursions with the frozen unrestricted private-program oracle
on all three-bit Boolean tasks and small arbitrary source subsets. Include
unequal prices, source correlations and nonuniform priors. Retain the existing
parity/conjunction formulas as corollaries, not separate new method families.
The primary comparison in [literature.md](literature.md) is Saettler, Laber and
Cicalese's value-dependent-cost discrete-function evaluation framework. Two
oriented tests for each coordinate implement this instance directly. The
reduction removes private-program search, but the remaining decision-tree
optimization and explicit source representation can still be expensive.

The unchanged first run of [cap_two_probe.py](cap_two_probe.py) passed for all
256 three-bit Boolean tables, all 255 nonempty source subsets, three price
vectors, two episode overheads and two positive prior-weight vectors. It made
783,360 comparisons each for worst and expected cost and checked the D+1/2D
bounds in 105,340 nonconstant unit-price cases. The private-program oracle and
the reduced recursion each visited 632,040 nonterminal states; their candidate
choices were 7,470,800 versus 1,769,400 in this screen. Those are named search
operations, not complete implementation costs. Both ran within one 9.1360324
second probe, so no separate runtime advantage was measured. The conventional
oriented-test realization is exactly the reduced method and ties it.
