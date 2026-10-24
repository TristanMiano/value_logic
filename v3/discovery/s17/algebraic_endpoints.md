# Exact univariate algebra for the bounded N16 claim

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT. This is a consequence of
the selected endpoint formulas, not a new root-isolation algorithm.

Assume rational symmetric 0<C<I, rational E>0 and rational rank-one
V>=0 with trace1. The target can be represented by V=cc^T even when an
individual unit c has irrational coordinates. Define polynomial matrices

    D_l(t)=(I-C)t^2+(I+EC)t+EC,
    D_u(t)=Ct^2+(I-EC)t-EC.

For t>=h, where h^2-Eh-E=0 and h>0, both are positive definite:
D_l=t(aI-dC) and D_u=t(I+dC). Thus the two scalar families are

    L(t)=t tr(V C adj(D_l(t)))/det(D_l(t)),
    U(t)=t(t+1) tr(V C adj(D_u(t)))/det(D_u(t)).       (A1)

All coefficients are rational. The determinant degrees are exactly2k
because C and I-C are positive definite; numerator degrees are at most
2k-1 and2k respectively. After any common factors are cancelled, the
derivative numerator has degree at most4k-2 in either case. For U the
putative degree4k-1 terms cancel between N'D and ND'; for L its original
numerator already has one smaller degree. This conclusion needs no
diagonalization or algebraic eigenvector representation.

Each finite interior optimizing parameter is a real root of the appropriate
derivative numerator. That polynomial is not identically zero: L tends to
zero at infinity but is positive on the domain; U is a nonconstant rational
function (it has value0 at t=0, where D_u is invertible, and limit1 at
infinity). A rational function that were constant on the domain would be
constant as a rational identity, contradicting those evaluations.

Consequently each exact endpoint is algebraic of degree at most
max(2,4k-2) over Q. An interior endpoint belongs to Q(t_*), the cap lies
in Q(h) of degree at most2, and the upper infinite endpoint is1. The
lower infinite limit0 cannot be its maximum. This is a degree bound,
not a claim of an elementary radical formula for arbitrary k.

## Strict decisions need only degree2k polynomials

For rational threshold tau, U(t)<tau is equivalent on the admissible
domain to

    tau det(D_u(t))-t(t+1) tr(V C adj(D_u(t))) > 0.   (A2)

Similarly L(t)>tau is equivalent to

    t tr(V C adj(D_l(t)))-tau det(D_l(t)) > 0.        (A3)

These polynomials have degree at most2k. The domain is described by
t>0 and t^2-E(t+1)>=0. Exact univariate real-root isolation and sign
determination therefore decide existence of a strict certificate using
rational coefficients. If a strict inequality holds at the irrational
cap, continuity makes it hold at a nearby admissible rational parameter;
if the upper limiting value1 is strictly below tau, sufficiently large
rational t works. Thus a positive existence answer can supply a rational
witness to the existing checker, subject to its size limits. Equality to
the sharp endpoint remains unresolved under a strict decision contract.

This complements [finite ternary search](search_guarantee.md): it removes
the need to choose a known positive margin in advance. It does not make
bounded input formats complete or authenticate the receipt premises.
Polynomial coefficients and root certificates can be large. An ordinary
floating proposal with an exact check can be much cheaper in practice.

## Computational interpretation

The analytic theorem reduces an optimization over unknown source dimensions
to one variable with explicit degree bounds, while the
[ordinary Gram formulation](gram_sdp.md) already reduces it to an exact SDP.
This is a concrete difference in representation. It is not an observed
CPU advantage or a claim that generic root isolation beats optimized SDPs.
For numerical proposal generation, a one-time eigendecomposition of C
allows each scalar objective to be evaluated as k weighted fractions;
certification can still use rational linear algebra on C. The decomposition
cost, later target rotations, bit precision and receipt acquisition remain
part of a complete computational comparison.

The distinction helps define what an external contribution review should
judge: whether this explicit scalar solution and its finite extremizers
are useful and moderately novel beyond known exact operator interpolation
SDPs. The root-isolation machinery itself is established mathematics.

The [exact two-dimensional screen](algebraic_result.json) checks both
formula identities, irreducible degree-six derivative polynomials, exactly
one admissible critical root per endpoint and the correct extremum signs.
It certifies an upper value below0.539 through a degree-four polynomial.
The [script](algebraic_check.py) used SymPy1.14.0 on Python3.13.14 and
169,230,600ns after imports. These are one-block exact checks, not a
general proof or a performance comparison. See the
[primary comparison](literature.md) for why generic SDP algebraic-degree
results cannot be used as a lower bound for this structured problem.
