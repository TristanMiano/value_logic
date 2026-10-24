# Sealed validation can use a learning mistake budget

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass47.
The private ideal-path argument is from private_repairs.md; this note
replaces a linear error-rank potential by a conventional online-learning
mistake potential. It does not claim a new online-learning theorem.

Let a fixed truth function A:X->{0,1} belong to a known class H. Suppose
an exact counterexample learner proposes functions B_t and has the following
deterministic guarantee: every public witness (x,A(x)) with B_t(x)!=A(x)
reduces a nonnegative integer potential, initially at most d. At potential0,
its proposed function equals A everywhere. The learner may retain all its
public witnesses and perform paid computation between proposals.

Fix a distribution D, independent of a hidden validation batch S of k iid
draws. Query A on S once, retain those labels privately, and accept a proposed
B if it agrees on S. Assume EVERY possible incorrect proposal has
P_D(B(x)!=A(x))>=gamma>0. Then a fixed incorrect proposal passes with
probability at most(1-gamma)^k; a correct proposal ALWAYS passes.
On rejection, find a counterexample using NEW independent D draws and
release that public witness to the learner. Never release the hidden
failing sample or use it to select the public repair.

    P(any incorrect acceptance, for the whole lifetime)
       <= d*(1-gamma)^k.                             (1)
    E[number of truth queries] <= k+d/gamma.          (2)

The number of correct proposals/acceptances does not enter(1), although
evaluating them on the private batch still costs work. For(1), condition on
the independent public randomness and follow the ideal path that rejects
every incorrect proposal. At most d such proposals occur. Up to the first
incorrect acceptance, the real path agrees with this seed-independent ideal
path, so the union bound has d terms. Perfect completeness is essential.
For(2), every actual rejection certifies an incorrect proposal and consumes
one unit of potential; its public search has mean at most1/gamma. These
bounds do not charge source evaluation, model evaluation and learner algebra
equally unless a stated tariff does so.

## Littlestone dimension supplies one such potential

For a realizable binary class with finite Littlestone dimension d, maintain
the version class V. At x, the standard optimal algorithm predicts the label
whose restricted class V_(x,label) has larger Littlestone dimension (fixed
tie rule). An error moves to the other nonempty subclass, whose dimension
is strictly less than dim(V): otherwise both children could have dimension
dim(V), forming a shattered tree one level deeper. At dimension0 all
remaining functions agree pointwise. This gives exactly the required
counterexample learner. Its proposal can be improper, and evaluating it
or computing the dimensions may be expensive; no efficient oracle is free.

For a finite class, d<=floor(log2|H|), but the margin gamma must cover all
these possibly improper proposals, not merely every pair in H. A finite
uniform domain gives gamma>=1/|X| for every incorrect binary function,
which may make(1)–(2) economically useless. A claimed larger gamma needs
its own structural proof. A polynomial identity tester does not automatically
check a majority/SOA function: that function need not retain low degree.

VC dimension alone cannot replace this mistake budget. Threshold functions
on an unbounded ordered domain have VC dimension1, while binary search
can build arbitrarily deep shattered mistake trees. This refutes a tempting
constant-budget extension before any implementation.

## Comparison and meaning

A single uniform-convergence batch protecting every possible proposed
function may require a much larger class-union allowance. Here the sealed
interface and a bounded FALSE-proposal path justify(1). Fresh validation,
version-space reasoning and exact equivalence-query learning are mandatory
ordinary controls. They may be cheaper when many proposals are rejected
early, or when gamma is small. This supplies a candidate adapter from
finite learning structure to lifetime checking of mathematical computations;
it supplies no general logical-uncertainty learner and no measured savings.
