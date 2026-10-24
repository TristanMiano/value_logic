# Explicit certificates for the ordinary Gram SDP

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; direct derivation.
These identities connect the proposed scalar solution to the strongest
[ordinary comparison](gram_sdp.md). They certify its closed relaxation
directly, without using the nondegenerate-source approximation argument.
They are a reconstruction of the bounded contribution, not a new target.

Use the Gram program's vectors W,R,r,u and X,x,z, with v=Wc,
f=v^T r=||r||^2+||x||^2, Q=R^T R, and P=Q-C^2>=0. The last order
follows from the PSD Gram matrix and W^T W=I, W^T R=C. Equivalently,
alpha^T P alpha=||R alpha-WC alpha||^2. The edit constraints are

    ||u||^2 <= E||x||^2,  ||z||^2 <= E||r||^2.

All formulas below are identities in Gram entries. Auxiliary coefficient
vectors alpha and all parameters depend only on the given C,c,E.

## Lower certificate

Take t>=h, a=1+t, d=t-E-E/t>=0, B=aI-dC,
alpha=B^(-1)c, w=R alpha and b=X alpha. Constraint (G2) gives

    c^T C alpha = r^T w+x^T b+u^T w.

Using ||w||^2+||b||^2=alpha^T C alpha, direct square expansion yields

    f-c^T L_t(C)c
      = ||r-w||^2
        + ||x-a b||^2/a
        + t ||u-(aE/t)w||^2/(aE)
        + (t/a)(||x||^2-||u||^2/E)
        + d alpha^T P alpha.                         (D1)

To check the constants before optimizing alpha, the first four terms equal

    f-2c^T C alpha
      + a alpha^T C alpha-d alpha^T Q alpha.

Adding the last term replaces Q by C^2. Since B alpha=c,
alpha^T C B alpha=c^T C alpha=c^T L_t(C)c, establishing (D1).
Every term on its right is nonnegative for every feasible Gram pair.

## Upper certificate

Take 0<eta<=h, a=1+eta, b0=1+E+E/eta,
kappa=b0-a>=0, B=aI+kappa C, alpha=a B^(-1)c. Put

    b=X alpha, q=W(c-alpha)+R alpha.

Here q is the old residual of the hypothetical coefficient b; it is not
the program's z=Delta^T r. Constraint (G3) gives

    f=r^T q+x^T b-z^T b.

The upper scalar expression g(eta) in proof.md satisfies

    g(eta)-f
      = ||x-b||^2
        + ||r-a q||^2/a
        + eta ||z+(aE/eta)b||^2/(aE)
        + (eta/a)(||r||^2-||z||^2/E)
        + kappa alpha^T P alpha.                     (D2)

Indeed, the first four terms expand to a||q||^2+b0||b||^2-f.
Adding the final term gives the compressed upper quadratic evaluated at
its minimizing alpha, hence g(eta)-f. Again every term is nonnegative.
At eta=0 the universal bound f<=1 follows from
f=||r||^2+||x||^2=v^T r<=||r||<=sqrt(f).

These are explicit feasible dual certificates: each squared norm is a
positive semidefinite quadratic form in one of the two Gram matrices;
the two scalar norm slacks have nonnegative multipliers; and the used
normal-equation identities are linear equality constraints. Writing the
matrices of multipliers separately is optional bookkeeping, not another
mathematical assumption.

## Equality and the candidate's remaining delta

For the lower certificate, equality requires r=w, x=a b,
u=(aE/t)w, saturation of the u norm constraint, and d alpha^T P alpha=0.
For the upper one, equality requires x=b, r=a q,
z=-(aE/eta)b, saturation of the z norm constraint, and
kappa alpha^T P alpha=0. The canonical interior sources and the cap
dilations in [proof.md](proof.md) realize precisely these conditions.
At either cap the coefficient of P vanishes, permitting hidden second
moments without a compression penalty. Cancellation handles the eta=0 case.

Consequently the closed Gram SDP has the stated exact optimum values,
with finite genuine source/edit witnesses, by (D1), (D2) and those explicit
primal constructions. No numerical duality gap assumption, Slater argument,
or interchange of minimization and maximization is required for this claim.
The general interpolation framework remains prior machinery. The possible
increment is its explicit solution for this specified retained-information
problem, including a transparent primal/dual equality mechanism.

## Focused exact check

[dual_check.py](dual_check.py) and [dual_result.json](dual_result.json)
check both identities on a rational 3-by-2 source with a dense two-dimensional
compression, a non-eigenvector target and a rank-one edit. Two parameter
cases exercise positive compression penalties and zero cap penalties.
All four identities and the signs of every displayed term passed in exact
fraction arithmetic (982,800 ns for the check). The independent target value
uses an adjugate inverse. This is a focused algebra screen, not a general
proof or independent confirmation. The normal-equation derivation above
supplies the universal argument.
