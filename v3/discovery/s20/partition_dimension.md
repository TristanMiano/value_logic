# Dimension of the complete partition-incidence family

Codex (GPT-6), October 28, 2026. Separate DEVELOPMENT. This is a structural
corollary of [the face-chain argument](face_chain.md), not an addition to the
frozen V19 event. Its novelty has not been assessed.

Let K have k items and let a configuration be an ordered partition
(T_1,...,T_n) of K, with empty blocks allowed. Its incidence vector has one
coordinate for each pair (i,T), i in {1,...,n}, T subset K. It puts a one
at exactly the n selected pairs. Let P be the convex hull of all such vectors.

For n>=3,

    dim P = n*2^k - n - k.

To prove that there are no additional affine equations, suppose coefficients
a_i(T) satisfy sum_i a_i(T_i)=C for every ordered partition. Put b_i=a_i(empty),
h_i(T)=a_i(T)-b_i, and B=C-sum_i b_i. All h_i(empty)=0.
For distinct i,j,l and disjoint A,B' with S=A union B', compare the two
partitions putting S at i and K\S at l, or A at i, B' at j and K\S at l.
They imply

    h_i(S) = h_i(A) + h_j(B').

Take A empty to obtain h_i(S)=h_j(S). There is a third block for every pair,
so all h_i agree with one h. The displayed identity then says h is additive
on disjoint subsets. Thus h(T)=sum_(j in T) lambda_j for singleton weights.
Every affine equation therefore comes from block sums and receipt sums:

    sum_T z_(i,T)=1;
    sum_(i,T: j in T) z_(i,T)=1.

These n+k equations are independent: a linear combination with zero
coefficient vector first has every block coefficient zero by looking at
(i,empty), and then every receipt coefficient zero by looking at (i,{j}).
The relation space has dimension n+k, giving the asserted affine dimension.
This proof also covers k=0; there is one configuration and dimension zero.

For n=2, each T determines the unique complementary configuration (T,K\T).
Their first-block coordinates are distinct unit vectors, so all 2^k
configuration vectors are affinely independent. The dimension is 2^k-1.
For n=1 there is a single configuration and dimension zero.

Consequently, the interval bottleneck output has at most

    1                         if n=1;
    2^k                       if n=2;
    n*2^k - n - k + 1         if n>=3

components when all formal slices are considered as independent interval
labels. Removing infeasible configurations cannot increase the affine
dimension of their convex hull, so these remain upper bounds with missing
slices. An instance-specific dimension may be much smaller. The bound is
not claimed sharp for all partition families or realizable V19 local data:
nested slices constrain their endpoints, and overlapping source cells can
join images. In particular the independent source-component bound from
multinomial_components.md can be substantially stronger. This calculation
explains the incidence structure; it is not a new general-purpose algorithm.
