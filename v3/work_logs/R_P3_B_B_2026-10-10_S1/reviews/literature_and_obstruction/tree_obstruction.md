# Option B: a precise parity obstruction for the inherited tree receiver

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration reviewer, October 10,
2026 UTC. **R-P3-B-B DEVELOPMENT; same-model, nonblind reconstruction.**
Principal-clock credit: **zero**. This is a mathematical and source inspection,
not a new empirical run. [Source hashes](source_manifest.json) bind the code.

## 1. Statement that is actually supported

For the family below, the inherited `BandProof` and a **fresh** `PortfolioProof`
with `choices=()` require exactly $`2^n`$ leaves and $`2^{n+1}-1`$ visited tree
nodes. This holds for every valid split order. In the portfolio case it holds
for every admissible tuple of nonnegative current-row multipliers, not merely
for the supplied producer's search heuristic.

The hypotheses include the concrete interval and feature-collection rules,
absence of hard/soft premises, no admitted old choices, and a requested bound
of zero. This is **not** a lower bound on arbitrary certificates, arbitrary
algebraic proof trees, or portfolios with useful admitted history. The old
finite implementation admits at most ten bits; the asymptotic statement is
about the explicitly uncapped rule schema. Its instances with $`2\le n\le10`$
fit the source's bit and 2,047-node caps.

## 2. Family and requested service

Let $`x_0,\ldots,x_{n-1}`$ be Boolean inputs, with $`n\ge2`$. Define XOR using
the actual grammar by $`u\mathbin{\oplus}v=\neg\mathrm{eq}(u,v)`$. Let

```math
P_n=((x_0\mathbin{\oplus}x_1)\mathbin{\oplus}\cdots)
       \mathbin{\oplus}x_{n-1},\qquad
Q_n=((x_{n-1}\mathbin{\oplus}x_{n-2})\mathbin{\oplus}\cdots)
       \mathbin{\oplus}x_0,
\qquad d_n=P_n-Q_n.
```

The frame has no hard constraints and no soft rows. Its rank is identically
zero. Supply the all-zero feasible incumbent, cutoff zero, and desired upper
bound zero. The current incumbent sublevel is the full Boolean cube. Every
assignment has $`P_n=Q_n`$, by associativity and commutativity of parity, so the
requested statement $`d_n\le0`$ is true everywhere and nonvacuous.

This is the same expression pattern as `parity` and the parity family in
[`05_resource_comparison_check.py`](../../../../checks/05_resource_comparison_check.py),
but **with the unedited full-cube frame**. It is not a claim that every old
edited benchmark still needs a complete tree: hard and rank exclusions can
shorten those trees. The expression tree itself has linear size in $`n`$;
writing explicit binary variable indices adds their ordinary encoding cost.

## 3. Interval fact for every partial cell

A cell fixes some bits and leaves the others unspecified. In
[`04_counterfactual_repair.py`](../../../../checks/04_counterfactual_repair.py),
`interval` gives an unspecified bit $`[0,1]`$, complements endpoints for `not`,
and gives an `eq` node $`[0,1]`$ whenever one operand is $`[0,1]`$ and the other
is either $`[0,1]`$ or a Boolean singleton.

Induction through either XOR fold gives two facts:

- if every bit in that fold has been assigned, its interval is its exact
  Boolean value;
- if at least one bit in that fold is unspecified, its interval is $`[0,1]`$.

Each complete fold contains every input. Therefore on every non-singleton
cell both $`P_n`$ and $`Q_n`$ receive $`[0,1]`$. On a singleton both receive the
same exact parity bit. This is a claim about this interval interpreter, not
about the true range of the difference, which is always $`\{0\}`$.

## 4. BandProof lower bound

The relevant source is
[`05_counterfactual_transport.py`](../../../../checks/05_counterfactual_transport.py),
`collect`, `enclosure`, `build_band` and `verify_band`.

`collect` flattens addition and scaling but treats Boolean `not` subexpressions
as opaque atoms. The two parity expressions have different serialized syntax
for every $`n\ge2`$. Thus their coefficients cannot cancel in this collector.
On a non-singleton cell, `enclosure(d_n, cell)` is $`[-1,1]`$, and a loss leaf
cannot discharge the requested bound zero. A hard leaf cannot apply because
the hard list is empty. A rank leaf cannot apply because its strict test is
$`0>0`$.

The only remaining accepted instruction splits one previously unspecified bit
and checks both assignments. No bit can be split twice on a path. Every
accepted leaf must therefore fix all $`n`$ bits. Exhaustive disjoint splitting
partitions the full cube into its $`2^n`$ singletons. A finite full binary tree
with $`L`$ leaves has $`L-1`$ internal nodes, giving

```math
L=2^n,\qquad I=2^n-1,\qquad N=L+I=2^{n+1}-1.
```

Conversely, splitting all bits and using loss leaves is accepted: on every
singleton the interval difference is exactly zero. The bound is exact for
this proof system, regardless of the producer's chosen variable order.

An in-process repeated tuple pointer would not change the receiver's traversal:
`verify_band` visits both children with distinct current cells. The declared
nested tree serialization has no reference instruction that would make a
single residual proof stand for both contexts.

## 5. Fresh PortfolioProof: arbitrary multipliers do not defeat this witness

The stronger local receiver is
[`05_portfolio_transport.py`](../../../../checks/05_portfolio_transport.py),
particularly `form`, `context_rows`, `conditional_upper` and
`PortfolioCache.verify`. Its `form` does linearize Boolean `not`, so the
BandProof argument cannot simply be copied.

Write the outer equality nodes as $`E_P`$ and $`E_Q`$, so
$`P_n=1-E_P`$ and $`Q_n=1-E_Q`$. They are distinct syntactic `eq` features.
The collected target is therefore $`E_Q-E_P`$. Both features still have
interval $`[0,1]`$ on every non-singleton cell by the preceding induction.

With no hard or soft rows, `context_rows` derives only:

```math
0\le0,\qquad x_i-b_i\le0,\qquad b_i-x_i\le0
\quad\text{for the bits assigned }x_i=b_i\text{ in the current cell}.
```

There are no clauses or hidden producer-supplied premises. Arbitrary admitted
nonnegative multipliers can change only the constant and assigned-bit
coefficients. They cannot change either opaque feature coefficient in
$`E_Q-E_P`$. Every added assigned-bit expression is exactly zero on the cell;
its collected interval is therefore exactly zero there, including after any
linear combination. The conditional upper bound remains **exactly one** on
every non-singleton cell. This argument covers every syntactically valid
multiplier tuple, within the implementation's rational/row caps.

When `choices=()`, no reuse leaf is available. The hard and rank alternatives
remain unavailable, and a direct leaf cannot prove zero before a singleton.
The same exact $`2^n`$-leaf bound follows. At every singleton the empty
multiplier tuple suffices, so this is also attainable.

**Why the qualification matters.** A previously admitted certificate for this
same full-domain zero bound admits a one-leaf reuse proof with identity map
and positive scale one: the old hard obligations are empty, old rank is zero,
and the receiving correction is literally zero. Constructing, checking,
retaining and restoring that old warrant must still be charged, but a new
request's tree does not have the above lower bound. Additional hard equalities
or a richer algebraic checker may also discharge the target earlier. We prove
no obstruction for those services.

## 6. The ordinary shared representation and possible checked bridge

A fixed-order diagram for parity stores only the parity accumulated so far.
After the first decision there are at most two residual parity states at each
remaining level. A reduced diagram without complemented edges has
$`2n-1`$ internal nodes and two terminals, hence $`2n+1`$ nodes. Reversing the
syntactic fold leaves the represented function unchanged. The difference has
the constant-zero diagram.

This elementary residual-state construction is consistent with the ordinary
BDD and knowledge-compilation antecedents in
[source cards B-B-L1 and B-B-L3](source_map.md). It does not show that a forged
zero root is a certificate: the receiver still needs a checked connection from
the independent request to those shared functions.

One constructive route records acyclic exact-Apply obligations and the
expression compilation graph. Each local obligation checks both Shannon
branches and exact terminal arithmetic, referencing only validated children.
For this family, each intermediate XOR fold has linear-size parity diagrams;
a constant number of Apply operations per added bit with memoization gives a
polynomial total trace (a simple quadratic upper bound in node-pair work
suffices). This is a proposed constructive argument, not a claim about code
that has yet to be inspected. Bit encodings, checker lookup strategy, exporter
copies and retained storage determine the actual charged bound.

Generic inputs can have exponential diagrams or intermediate Apply work.
Neither a linear parity diagram nor a final zero root implies a polynomial
compiler on arbitrary expressions. The new DAG service is a separate accepted
proof format; comparison against the old tree format must say when that format
change is available equally to ordinary and portfolio methods.

## 7. A second representation-only check and the inference boundary

An ordinary bit-query decision tree computing parity also needs $`2^n`$
leaves: if a leaf leaves any bit unqueried, flipping it preserves the path but
changes parity. This lower bound concerns the function representation.
Likewise, any implicant cube for odd parity must fix every bit, so a DNF over
only the original variables needs $`2^{n-1}`$ satisfying cubes; the dual CNF
count is the same. Extension variables or shared subproofs change this syntax.

None of these arguments lower-bounds all Boolean formulas or algebraic proof
trees. A balanced Boolean formula for XOR can already avoid the complete
bit-query decision tree, and a proof calculus may admit algebraic parity
identities directly. The source's representation separation must not be
renamed as a general proof-complexity result.

For Option B, the supported conclusion is therefore constructive and scoped:
there is a precise exponential expansion in the inherited empty-history local
interval-tree interface, while established ordinary shared proof techniques
motivate a compact checked alternative. Which implementation meets an actual
receiver budget remains an end-to-end development comparison.
