# Private scope checking when the truth oracle supports linear summaries

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 39.

This is a different oracle contract from counting individual exact outputs.
Suppose a trusted truth service can return w^T A(x) for a requested vector w,
as well as selected coordinate outputs. The actual cost of this aggregate
must be measured or warranted; computing all coordinates and summing them
does not make it a cheap query.

Fix d anchor indices J. A proposed constant n by d matrix U must have
invertible U_J, and the proposed polynomial model B must satisfy the proved
degree bound deg(A-B)<=D. Define H_U=U U_J^(-1) R_J. The all-input error
scope is equivalent to the identity Z_U(x)=(I-H_U)(A(x)-B(x))=0.

For each of k private independent checks, draw X uniformly from a product
grid S^m of size q>D and w uniformly from F_q^n. Privately cache A_J(X)
and w^T A(X). Test

    w^T[A(X)-B(X)]
       -(w^T U) U_J^(-1) [A_J(X)-B_J(X)] = 0.              (1)

This uses d+1 cached scalar truth responses per check. Model evaluation,
the dot products, solving with U_J, randomness, storage and privacy all remain
paid. It supports changing U,B with the same anchor set, subject to the
private-transcript and first-rejection retirement rules in private_scope.md.

For any fixed false scope, some component/annihilator of Z_U is a nonzero
degree-at-most-D polynomial. P[Z_U(X)=0]<=D/q. If Z_U(X) is nonzero, a
fresh uniform w annihilates it with probability exactly 1/q. Therefore

    P[(1) passes] <= beta = D/q+(1-D/q)/q,
    P[all k checks pass] <= beta^k.

The bound is sharp for a residual equal to a degree-D polynomial with D
distinct roots times one fixed vector outside U. It has perfect completeness.
The first-false-proposal argument consequently yields the same beta^k lifetime
bound before retirement, without a factor for the number of accepted proposals.
No result survives disclosing w or the checked points to the proposer: for
example a proposed false residual in the known kernel of w evades its check.

At D=4, q=257, beta=1281/66049 and k=2 gives beta^2<.001. With d=4,
the cache uses ten scalar truth responses instead of two full 128-coordinate
vectors. This is an interface/communication comparison only. A scalar
aggregate can cost as much as a full vector evaluation, and conventional
fingerprinting with the same oracle implements exactly this method. The
purpose of the screen is to state when this access model would matter,
not to advertise a computation saving by counting unlike calls equally.

Known randomized linear verification and algebraic fingerprinting are direct
antecedents. The potentially useful adapter is the cached anchor-plus-sketch
scope test for changing models; novelty and a favorable real tariff remain
unassessed. Fixed anchors may also be poorly conditioned over approximate
real arithmetic; the exact finite-field theorem does not address that problem.
