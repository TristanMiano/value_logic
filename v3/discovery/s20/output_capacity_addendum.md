# Output capacity: simplex realization and established matrix bounds

Codex (GPT-6), October 28, 2026. Separate DEVELOPMENT. No new readiness
event or claim of a new matrix invariant is introduced.

## Arbitrary local labels are realizable, at a dimension cost

Fix nonnegative capacities r_i summing to k. For block i let V_i be all
r_i-subsets of K and put its source in the probability simplex on V_i.
For a source vector p_i define g_ji=sum_(S contains j) p_i(S). Require
max_i g_ji=1 for every item j. Each g_ji lies in[0,1], and

    sum_(i,j) g_ji = sum_i r_i = k.

Every column must therefore have exactly one entry1 and all other entries0.
The resulting allocation has exactly r_i items assigned to block i.
A distribution p_i whose inclusion probabilities are the Boolean vector
of T_i is concentrated on T_i: any other r_i-subset disagrees at some
coordinate and could not have positive mass. Thus the compatible sources
are precisely the capacity-respecting labelled partitions.

Any prescribed rational weight w_i(S) is the affine local readout
f_i(p_i)=sum_S w_i(S)*p_i(S). The future minimum takes exactly the
bottleneck values of these partitions. This realizes the arbitrary-label
configuration problem from [triangular capacity](triangular_capacity.md)
inside the original affine-source semantics. It charges |V_i|-1 source
dimensions, after eliminating one simplex coordinate; a singleton V_i can
instead use an irrelevant bounded coordinate to meet positive-dimension
conventions. This is not a small-dimensional or fixed-noise realization.

For capacities(1,1,k-2), k>=3, there is a simple constructive lower bound
binomial(k,2)+k-1 on distinct future minima. Label the first two blocks'
singletons a_j,b_j and the last block's complements c_{jl}, j<l. Choose
one distinguished item0. Give every c_{jl} with j,l!=0 a different low
weight. Give all a_j,b_j with j!=0 different intermediate weights, and
give a_0,b_0 and c_{0j} high weights. Every low c_{jl} is the minimum
of either corresponding ordered allocation. For each j!=0, the two
allocations involving0,j have distinct minima a_j and b_j. No other
configuration exists. The count is binomial(k-1,2)+2*(k-1), as stated.
This is a derived lower bound, not a claim of optimality here.

## Coordinate-face chains and why rank alone need not be sharp

For a nonempty family of nonempty configurations A, let P be the convex
hull of its incidence vectors. Deleting an element e from the available
ground set replaces P by its face P intersect {x_e=0}. Distinct bottleneck
values correspond to successive strict nonempty-to-smaller faces, ending
with the empty set. Conversely, any such sequence gives a triangular
incidence minor by selecting one removed configuration at each step.
Thus the earlier output-capacity parameter equals the longest such
coordinate-zero face chain. It is at most dim(P)+1.

If P equals an affine subspace intersected with the nonnegative orthant
and is bounded, every proper facet is induced by a coordinate zero.
Choose a facet successively until a vertex remains, then set one positive
coordinate of that nonzero vertex to zero. This yields dim(P)+1 strict
steps and makes the bound exact. The premise concerns the *actual*
configuration polytope, not merely a fractional relaxation.

The premise matters. For all r-subsets of an m-set, with1<=r<=m,
the maximum number of distinct minima is m-r+1: after sorting distinct
weights, only the first m-r+1 can be the least of r selected elements,
and each can be attained. For1<r<m this is less than the algebraic
incidence rank m. The hypersimplex also has upper-coordinate facets;
its zero-coordinate faces need not form a full dimension-by-dimension flag.

## Close prior results and disposition

[Alrabiah--Guruswami (2021)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol207-approx-random2021/LIPIcs.APPROX-RANDOM.2021.57/LIPIcs.APPROX-RANDOM.2021.57.pdf),
sections1.5 and2.2--2.4, defines visible rank, proves the triangular
characterization, and connects it to uniquely restricted matchings.
Their Theorem14 also identifies its complement with the rank of an
associated symmetric inference system. Those identities are established
antecedents; this note only applies the parameter to possible bottleneck
outputs. The proof of Theorem14 and the triangular characterization were
read; later coding-theory results are not imported.

[Fang et al. (2016)](https://dml.cz/bitstream/handle/10338.dmlcz/145878/CzechMathJ_66-2016-3_24.pdf),
Theorem2.9 and its proof on pages904--905, gives a triangular submatrix
of size d+1 in the nonincidence pattern of vertices and facets of a
d-polytope. Under the nonnegative-standard-form premise above, coordinate
columns include the facet pattern, so the sharp rank consequence has a
direct published antecedent. The face-chain proof here is a reconstruction,
not a new polytope theorem.

Keep the simplex realization and resource translation as explanatory
extensions. Park standalone novelty claims about the matrix parameter,
rank bound or coordinate-facet sharpness. No computational campaign is
needed to rediscover those established statements.
