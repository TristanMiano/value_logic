# Small-dimensional representatives for joint numerical receipts

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. A proposed elementary
span-compression lemma. Operator interpolation and performance-estimation
methods are close conventional antecedents; novelty is unassessed.

For any finite matrices M,N with the same shape and unit vector v, write

    w=(I+MM^T)^(-1)*v, z=M^T*w,
    u=(I+NN^T)^(-1)*v, p=N^T*u.

Let P project the row space onto span{v,w,u}, and Q project the column
space onto span{z,p}. Restrict PMQ and PNQ to these subspaces, calling
them M',N'. They have at most three rows and two columns. The identities

    M'^T*w=z, M'*z=v-w,
    N'^T*u=p, N'*p=v-u

still hold. Consequently w,u remain the unique resolvent responses, with
their original inner products and norms. Both value receipts, both
squared-resolvent moments, and every Gram entry of v,w,u,z,p within its
respective space are preserved. Moreover

    ||M'||<=||M||, ||N'||<=||N||, ||N'-M'||<=||N-M||.

Thus existence under UPPER norm and edit bounds is exactly equivalent to
existence in shape 3 by 2 (pad zeros if necessary). Exact norm equalities
or lower bounds are not preserved and are outside this statement.

If ||M||<=K and ||N-M||<=e, the compressed matrices lie in a bounded
finite-dimensional set. Include v on its unit sphere and impose exact
closed receipt constraints. Resolvents are continuous because I+MM^T
is uniformly positive definite. The attainable receipt set is compact,
so both response endpoints are attained whenever the source is nonempty.
For generic interior(s,m) outside attainment_class.md's special curve,
the capped lower minimum is therefore strictly above the uncapped
infimum. This proves a strict improvement without yet calculating its size.

For k matrices and p right-hand sides, projecting onto all response
vectors plus the p right-hand sides uses at most (k+1)*p rows; projecting
onto all primal vectors uses at most k*p columns. The same argument
preserves all response Gram data and pairwise UPPER edit bounds.

This can make a later exact semialgebraic or interval screen independent
of the hidden matrix dimension. It is not yet a cheap global optimizer:
the remaining constraints are nonlinear, and numerical optimization alone
would not certify their extrema. No such solver or large screen is run here.
