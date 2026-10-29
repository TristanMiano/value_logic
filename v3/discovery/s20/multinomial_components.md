# A sharp component bound with any number of source blocks

Codex (GPT-6), October 28, 2026. DEVELOPMENT; new extension, not borrowed
evidence for the unchanged V19-R/v1 contribution event. This extends the
two-block argument and strengthens s19's k! bound.

## Candidate theorem

Let k labelled observations be assigned to n>=1 labelled source blocks.
For block i, let F_i be a hereditary family of feasible observation subsets:
if T is feasible, every subset of T is feasible. Consider the graph of
feasible labelled partitions (T_1,...,T_n) of K, with an edge for moving
one observation from one block to another while preserving feasibility.
Put k=n*q+r with 0<=r<n. The number of graph components is at most

    M(k,n) = k! / ((q+1)!)^r / (q!)^(n-r).

The bound is sharp. For the compact convex receipt-source contract, this
is also a sharp bound on source components and therefore on interval
components of any continuous scalar image. This does not make arbitrary
nonlinear endpoint optimization tractable.

## Weighted counting argument

Choose one terminal partition tau from each graph component, terminal
under feasible moves to a lower-index block. Such a partition exists:
each such move decreases the nonnegative integer sum of assigned block
indices. Write s_i=|T_i(tau)|.

Every permutation of the observations that lists T_1 first, then T_2,
and so forth, reconstructs tau under ordinary first fit. When an item
of T_c is processed, every lower block has its complete terminal set and
cannot accept this item. Block c can accept it by heredity. This is the
same greedy-normalization argument credited in s19/fiber_components.md;
the additional step here counts all within-block orders, not just one.

Exactly product_i s_i! permutations have this block-contiguous order.
Permutation families belonging to distinct selected terminal partitions
are disjoint: first fit is deterministic for a given order, and cannot
return two different partitions. Thus

    sum_(selected components tau) product_i |T_i(tau)|! <= k!,

or equivalently the sum of reciprocal multinomial coefficients is at
most one. Among nonnegative s_i summing to k, the factorial product is
smallest when sizes differ by at most one. Indeed, if a>=b+2, replacing
(a,b) by (a-1,b+1) multiplies the product by (b+1)/a<1. Its minimum is
((q+1)!)^r*(q!)^(n-r). Dividing the counting inequality proves the claim.
Empty blocks contribute 0!=1. At k=0 the unique partition gives M=1;
an infeasible system has zero components. When n>=k this recovers k!.

## Sharpness and continuous sources

For arbitrary capacities r_i>=0 summing to k, take F_i={T:|T|<=r_i}.
Every feasible partition has exactly those sizes. No item can move to a
different block, since every receiving block is full. Hence there are
exactly k!/product_i r_i! isolated graph vertices. Balanced capacities
attain M(k,n).

Realize them with y_i in the hypersimplex

    B_i={y in [0,1]^k : sum_j y_j=r_i}

and observations max_i y_ij=1 for each j. Total sum is k, whereas every
column sum is at least one. Therefore every column contains exactly one
entry equal to one and all others zero. The compatible source consists
of the same isolated labelled allocations. Max observations are the
original min contract after negating each affine form.

For general convex slices the assignment-cell intersection graph and the
one-item-move graph have the same components, as proved in s19. Each
cell is compact convex; each graph component gives a compact path-connected
union, and different graph components give disjoint compact unions.
Consequently every continuous real readout maps each source component to
a closed interval. A weighted affine sum with different powers of two
for all (i,j) coordinates separates the Boolean sharpness points.

This sharpness statement concerns general continuous/affine scalar
readouts. A future minimum over local affine forms also has AR1's
n*2^k bound; it need not distinguish all source components. The correct
combined bound for that specific readout is min(M(k,n),n*2^k).

## Nonzero tolerance and full-dimensional sharpness

For k>=1, replace each sum equality by a band of half-width eta and use
max observations in [1-epsilon,1]. Choose positive eta,epsilon so
eta+(k+1)*epsilon<1. A witness partition has

    |T_i|*(1-epsilon) <= r_i+eta,

which forces |T_i|<=r_i: otherwise r_i+1<=|T_i|<=k would give
1<=eta+(r_i+1)*epsilon<1. Since the sizes sum to k, every size equals its
capacity. On its cell, assigned coordinates are >=1-epsilon and each
unassigned coordinate is <=eta+r_i*epsilon, by subtracting the assigned
coordinates from the sum upper bound. This latter value is strictly less
than 1-epsilon. Two distinct assignment cells are therefore disjoint.

Every cell has nonempty interior in the full n*k coordinate space. Put
delta=min(epsilon/2,eta/(2*k)), use 1-delta for an assigned coordinate and
delta for an unassigned coordinate. The sum differs from r_i by
(k-2*r_i)*delta, of absolute value at most eta/2. All box, sum-band and
assigned-receipt inequalities are strict. This also handles r_i=0 or k;
the small band makes the corresponding source polytope full dimensional.
There are precisely k!/product_i r_i! nonempty disjoint compact convex
cells and hence that many source components.

Number the n*k coordinates by h=0,...,n*k-1 and use the affine scalar
readout F(y)=sum_h 2^h*y_h. Choose

    eta=epsilon=1/[16*(k+1)*2^(n*k)].

Each coordinate is within eta+k*epsilon of its Boolean allocation value.
Consequently the error in F is less than

    (2^(n*k)-1)*(eta+k*epsilon) < 1/16.

Distinct Boolean allocations have distinct integer readouts, so the image
intervals are separated by gaps greater than 7/8. Full dimensionality and
the nonconstant affine F give every interval positive width. All constants
have O(n*k+log(k+1)) bits. This is not a fixed-noise asymptotic claim:
the tolerance decreases with n*k, and rescaling F to a bounded numerical
range also rescales the gaps. Balanced capacities prove the claimed sharp
bound with full-dimensional rational priors and nonzero observation widths.

## Primary comparison to complete

The factorial expression is the classical balanced multinomial maximum;
it is not a new extremal coefficient. The weighted inequality resembles
Meshalkin--Hochberg--Hirsch and their LYM-style permutation counting.
Their componentwise-antichain hypotheses must not be silently assumed
for arbitrary component representatives. The direct deterministic
first-fit fiber argument above establishes the needed disjointness.
The proposed adaptation is a component theorem for heterogeneous
hereditary partition constraints and its convex-source consequence.
Novelty and useful scope require further comparison before promotion.

[Beck and Zaslavsky (2002)](https://people.math.binghamton.edu/zaslav/Tpapers/mhh.pdf),
pages 197--199, theorem and full proof, supplies the classical multinomial
and weighted bounds when each of the first n-1 coordinate families is
chain-free. Their proof combines a maximal-chain count with induction on
the number of parts. Our terminal-partition argument uses deterministic
first-fit fibers instead of asserting that component representatives have
those coordinate-family hypotheses. It in fact bounds the number of ALL
lower-move terminal partitions, which can exceed the number of components.
The numerical coefficient and the factorial-counting method are established
antecedents; the reconfiguration-to-convex-source application is the
remaining proposed synthesis. This is not a claim to have discovered a
new multinomial inequality.

As in s19, [Bonamy and Bousquet's arXiv manuscript](https://arxiv.org/pdf/1403.6386)
contains the coloring-to-greedy normalization inside its Lemma 6 proof.
The current argument generalizes bin feasibility to different hereditary
families, but does not claim the normalization mechanism as new. A first
screen of coloring, Grundy/first-fit and hereditary-reconfiguration work
did not locate this sharp component-count contract. Search absence is
limited evidence and does not establish historical priority.
