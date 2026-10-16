# When evidence can and cannot enable a revision

Codex (GPT-6), DEVELOPMENT. A structural screen broadens the
[chain repair construction](safe_revision.md), rather than treating one
successful implication example as universal.

## An exact certificate criterion

Let F be a nonempty finite set of original worlds, G the target set, B a
declared menu of transformations, and J the queryable coordinates. For a
transformation b define Safe_b={x in F: b(x) in G}. At history h, b is
admissible precisely when F_h is a subset of Safe_b. Thus the cheapest
query certificate for b is a weighted certificate problem for this predicate,
restricted to F and J. Buying observations can enable b only by excluding
all violating originals. The cost of computing/checking that exclusion is
separate from the query fee.

For a fully observed query cell z, write F_z={x in F:x_J=z}. Transformation b
can be certified at an original x iff F_(x_J) is contained in Safe_b. Proof:
every history on x contains that full-query cell; querying all J attains it.
Equivalently, x_J is absent from the projection onto J of F minus Safe_b.
Consequently an observational twin y with y_J=x_J but b(y) outside G blocks
that revision forever under this query interface. More affordable queries
cannot fix a missing distinguishing observation.

This criterion is ordinary universal feasibility and certificate complexity,
not a new general theory of knowledge. It identifies a useful cheap screen:
check enableability before building an optimizer or estimating query value.
For example, knowing one member of an implication can enable a flip; knowing
an unrelated independent coordinate cannot exclude an unsafe twin.

## Parity constraints give a negative family

For Boolean vectors and a checked affine parity source F={x:A x=c over GF(2)},
let b be an XOR mask, with target G={y:A y=d}. Then for every x in F,
A(x xor b)=c xor A b. Therefore b is admissible iff A b=c xor d, independently
of every nonempty query history. No paid observation can enlarge this menu.
Queries can still help estimate action cost; they do not buy new feasibility.
This is immediate linear algebra, retained to reject a false generic gain.
Different target matrices or different transformations require a new argument.

## Exact-cardinality constraints give a positive non-chain family

Use F={x in {0,1}^m:sum x=k} and target G={y:sum y=k'}. At a query history,
let O be observed coordinates, U the unobserved coordinates, u=|U|, and
t=k-sum_(i in O) x_i. Consider an XOR mask with selected unknown subset V.

If 0<t<u, uniform validity forces V to be either empty or all of U. If V is
a nonempty proper subset, choose i in V and j outside V. There are two
compatible worlds differing only by exchanging their one/zero at i,j,
because 0<t<u. The number of selected true bits differs by one, and the
revised total differs by two. Both cannot equal the same target k'.

Conversely, for V empty or U, the unknown contribution to the count change
is known: zero or u-2t. A mask is valid exactly when

```math
\sum_{i\in O} b_i(1-2x_i)
 +\mathbf1\{V=U\}(u-2t)=k'-k.
```

When t=0 or t=u, every remaining truth value is logically determined, and
arbitrary unknown subsets are allowed subject to the corresponding balance
equation. The same applies when u=0. These boundary cases cannot be discarded:
they are precisely where observations may reveal a much richer repair menu.

For 0<t<u the menu is the union of two constrained subset choices on the
known coordinates, with either no unknown flips or all of them. Under a cap
H, discard the all-unknown mode when u exceeds the remaining budget. The
known-coordinate choices can be compiled by a dynamic program tracking
position, flip count and net cardinality change. Boundary histories use the
same program with every sign determined. This yields a polynomial-sized
terminal flow representation even though the source cardinality relation is
global rather than a chain of pairwise relations. Its optimization and
regret separation still require their own argument and cost accounting.

Example: m=4,k=k'=2. Before observing anything, only identity and flipping
all four bits preserve the source universally. With a two-flip cap, only
identity is available. After observing one zero and one one, swapping their
truth values by flipping those two known bits preserves the count, while the
two remaining truth values can stay unresolved. Query fees and the total
operation cap determine whether that certificate is worth acquiring.

This is an exact logical effect on the action menu, not a probability model
for the unknown worlds. The prior machinery is symmetry, universal constraint
satisfaction and dynamic programming. A claimed useful contribution would
be the costed decision interface or combined guarantee, not these ingredients
alone. First screen the classifier on small cardinality/parity sources and
all relevant histories before extending the main optimizer.

mg01 passes four declared cases (m=2,4,5,6, first two coordinates queryable)
on first attempts. It compares the cardinality classifier at every original
and target count and every compatible history/mask, and checks five seeded
affine-parity systems per size against direct universal feasibility. Boundary
histories with fully deduced remaining bits are included. Source hashes and
all panel inputs are preserved in the result files.

## Refinement can change the benchmark as well as the uncertainty

With target G fixed, refining F to a nonempty subset F' can only enlarge the
admissible mask menu at compatible histories. Hence optimized worst-case
absolute cost cannot increase: every old policy remains feasible and there
are fewer possible originals. Minimax regret against a newly enlarged
comparator class does NOT have that monotonicity.

For a finite example take F={00,01,11}, fixed target G={00,11}, no queryable
bits, cap two, zero flip fees, and terminal-one cost equal to the sum of the
two signs. Terminal zero costs zero. Under F no XOR mask maps all three
originals into the two-point target, so every policy/comparator must use
terminal zero and minimax regret is zero. After a checked refinement excludes
01, both identity and flipping both bits become valid. Their costs on 00/11
are (-2,2) and (2,-2); each point-source comparator gets -2. The best randomized
controller has worst-case regret two. Worst-case absolute cost remains zero.

The refinement increased capability while increasing this relative metric.
Against the frozen old comparator, regret remains zero. Report changes to
source, admissibility and comparator explicitly; a numerical regret change
across those different duties is not a comparable progress percentage.
