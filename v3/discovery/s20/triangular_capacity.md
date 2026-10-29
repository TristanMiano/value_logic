# Exact abstract bottleneck capacity and an existing matrix parameter

Codex (GPT-6), October 28, 2026. Separate DEVELOPMENT; no novelty verdict.
This supplements the frozen face-chain note without changing its evidence.

Let A be a finite nonempty family of nonempty subsets of E. Its incidence
matrix H has rows indexed by configurations and columns indexed by elements.
Define tau(H) as the largest size of a square submatrix that can be reordered
to be upper triangular with diagonal entries one. Then

    max_(real weights u) |{min_(e in A) u_e : A in the family}| = tau(H).

For the upper bound, sort the distinct attained minima v_1<...<v_s. Choose
a configuration A_j attaining v_j and one element e_j in A_j of weight v_j.
The e_j are distinct. For h>j, A_h cannot contain e_j, because its minimum
exceeds u_(e_j). Hence the selected row/column submatrix has ones on its
diagonal and zeros below it. Thus s<=tau(H), with no assumption of distinct
weights on the entire ground set.

Conversely, take a triangular submatrix with rows A_1,...,A_s and columns
e_1,...,e_s. Put u_(e_j)=j and give every unselected element weight s+1.
Row A_j has no earlier selected element and contains e_j, so its minimum
is exactly j. There are at least s attained minima. Apply the upper bound
with s=tau(H) to obtain equality. This construction also shows that integer
weights suffice; no optimization over arbitrary precision real inputs is
needed to witness the maximum.

The same tau(H) is the exact maximum number of connected components of the
union of independent closed-interval bottleneck images over this abstract
configuration family. The upper bound follows from the distinct right
endpoints of components. For sharpness replace each constructed point
weight by [u_e-delta,u_e+delta], with0<delta<1/2. A branch image is the
interval around its point minimum, and distinct integer minima stay apart.
These are positive-width intervals. This is an abstract interval-label
realization; it does not assert that arbitrary labels obey V19's nested
local-slice constraints or arise from small-dimensional affine sources.

## Credit and independent reconstruction of the matrix equivalence

The triangular-submatrix parameter is established, not new. I read
Section3.1, Theorem3.1 and its proof in Bouillaguet, Delaplace and Voge's
[2017 author manuscript](https://perso.lip6.fr/Charles.Bouillaguet/static/publis/PASCO17.pdf).
They explicitly credit earlier work for its equivalence with maximum uniquely
restricted matching. I also read the introduction and matrix motivation in
the author-uploaded [Golumbic, Hirst and Lewenstein2001 manuscript](https://www.researchgate.net/publication/225671808_Uniquely_Restricted_Matchings).
Their later algorithmic and hardness proofs were not reconstructed here.

Here is the equivalence in the present notation. Form the bipartite graph
with an edge (A,e) iff H_(A,e)=1. A triangular submatrix's diagonal matching
is its unique perfect matching: the last row has only its diagonal column,
and induction removes that row and column. Conversely, suppose a matching
on selected rows and columns is the unique perfect matching of their
induced subgraph. Label its pairs (A_j,e_j). In a directed graph on pair
indices, draw j->h for an OFF-DIAGONAL entry H_(A_j,e_h)=1. A directed cycle
would switch matching edges to produce another perfect matching. There is
no such cycle. A topological ordering therefore gives an upper-triangular
submatrix with diagonal ones. The explicit exclusion of diagonal loops
matters when stating this directed-graph argument.

As a consequence, tau(H)<=rank_F(H) over every field F: the selected
triangular minor has determinant one. Over the reals, rank(H)<=dim(P)+1,
recovering the earlier face-chain bound and sometimes improving it for
nonuniform configuration sizes. This does not give a cheap exact formula
for tau or a new matching algorithm. The incidence graph itself may have
exponentially many configuration vertices.

For fixed-cardinality configurations such as receipt partitions, the rank
bound equals affine dimension plus one over the reals. Their row vectors
all have the same positive coordinate sum, so their affine hull excludes
zero and has linear-span dimension one larger. For complete perfect
matchings, the earlier construction shows tau=(n-1)^2+1. For general
partition families the rank upper bound may be strict.

The useful inference here is a translation: the capacity to produce distinct
bottleneck answers is an existing structural-pivot parameter. Its matching
characterization and rank comparison must be credited; the translation to
this output question has not received a novelty assessment. It is a guide
to representation costs, not evidence that V19 beats its ordinary equivalent.
