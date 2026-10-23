# A paid directional upgrade to a scalar receipt

Codex (GPT-6), DEVELOPMENT, October22,2026. Compare the scalar-only theorem
in finite_transport.md with a richer receipt. The generic primal/dual reuse
mechanism is already screened against reduced-basis literature in
../s12/search.md, third pass; do not claim it as a new library principle.

Let ||v||=1 and g(M)=v^T(I+MM^T)^(-1)v. The identity regularizer remains
fixed. Write w=(I+MM^T)^(-1)v and z=M^T w. An exact witness satisfies
w+Mz=v and M^T w=z. Checking both equations costs two applications of the
actual source operator (one transposed). The witness is not trusted merely
because a fallible model supplied it. Store w,z and g=v^T w; storage is
linear in the two matrix dimensions.

For a known edit H, the directional derivative is d=-2*w^T H z. This is
additional information that a scalar receipt alone does not provide. With
||H||op<=e, the following finite bounds hold:

    g(M)+d-e^2 <= g(M+H) <= g(M)+d+e^2/4.          (1)

Clip to[0,1] and intersect with any scalar-only L/U band. This does not claim
that the quadratic bounds are the sharp finite envelopes given all witness
data. Their two global curvature constants are individually sharp.

## One-sided curvature proof

The variational identity is g(M)=min_z(||v-Mz||^2+||z||^2).
Let T=I+M^T M. Differentiating the optimality condition gives

    D^2g(M)[H,H]=2||Hz||^2
       -2||T^(-1/2)(H^T w-M^T H z)||^2.

The block operator T^(-1/2)[I,-M^T] has norm one because its product with
its transpose is I. Hence the squared norm in the negative term is at most
||H^T w||^2+||Hz||^2, and the second derivative is at least
-2||H^T w||^2>=-2||H||op^2, since||w||<=1.
Conversely, discarding the negative term bounds it above by2||Hz||^2.
The singular-value function sigma/(1+sigma^2)<=1/2 gives||z||<=1/2,
so this is at most||H||op^2/2. Along M+tH these inequalities hold uniformly.
Taylor's integral remainder yields(1). Scalar M=0 and M=1 with H=1 attain
the lower and upper second-derivative constants, respectively.

## Partial witnesses and large protected edits

Exact optimality is unnecessary for useful bounds. Any primal trial z and
dual trial w give, with r=v-Mz and s=M^T w,

    l=2v^T w-||w||^2-||s||^2 <= g(M)
       <= u=||r||^2+||z||^2.

The gap is exactly ||r-w||^2+||z-s||^2. Thus independently proposed trial
vectors can be checked against one actual matrix. Under an arbitrary known
factor edit H, their transported certificates are

    l'=l-2*s^T(H^T w)-||H^T w||^2,
    u'=u-2*r^T(Hz)+||Hz||^2.

No small-edit or new coercivity assumption is needed: I+(M+H)(M+H)^T
remains SPD. These are ordinary variational bounds, often stronger than
using the norm of H. Computing Hz and H^T w is charged; structured low-rank
edits may make it cheap, while arbitrary dense edits may not.

If Hz=0 the old upper certificate remains valid. If H^T w=0 the old lower
certificate remains valid. If both vanish, the entire old interval persists;
for an exact witness g(M+H)=g(M) even for arbitrarily large H. With nonzero
w,z, this protected linear edit space has dimension(n-1)(r-1) for n-by-r
matrices: in bases aligned with w and z, the first row and column of H vanish.
This is task-relative value preservation, not a claim the models are equal.

For example M=diag(2,3), v=(1,0), w=(1/5,0), z=(2/5,0) gives g=1/5.
Every H=diag(0,h) preserves that value. The scalar-only norm contract must
permit a much wider band as |h| grows because it lacks this direction data.
The comparison therefore prices a richer receipt, not a free improvement.

Multiple trial pairs may be retained: maximize their lower bounds and minimize
their upper bounds, while charging all source products, storage, edit products
and selection. A source-bound witness can be useful even when its proposing
model is inaccurate. The existing ordinary primal/dual method implements the
same certificate. A new empirical library is not justified by this observation
alone; the narrower new work here is the explicit scalar-factor curvature and
comparison of receipt capabilities.
