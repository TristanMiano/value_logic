# What retaining a block buys for later targets

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. This is an elementary
information comparison for the assessed N16-C/v1 claim, not a new general
query-complexity result or an economic benchmark.

Fix e>0, E=e^2 and h=(E+sqrt(E^2+4E))/2. Suppose the acquisition interface
returns exact scalar values q(z)=z^T C z, where C is an otherwise unknown
real symmetric matrix with 0<C<I. Query vectors may depend on previous
answers, but acquisition finishes before the later unit target c is declared.
There is no other source information. An answer must give the sharp N16
upper endpoint for every later c, or approximate that endpoint uniformly.
This is stronger than returning any valid upper bound, for which 1 suffices.

## Exact acquisition requires the whole symmetric dimension

Let m<k*(k+1)/2. Follow a deterministic adaptive acquisition algorithm on
C0=gamma*I, where gamma=1/[2*(2+h)], and record its m query vectors z_i.
There is a nonzero real symmetric H satisfying z_i^T H z_i=0 for all i:
these are fewer linear equations than the dimension of the symmetric space.
Normalize ||H||_op=1 and set epsilon=gamma/2. The two sources

    C_plus = gamma*I + epsilon*H,
    C_minus= gamma*I - epsilon*H

are strictly positive and have largest eigenvalue at most
3/[4*(2+h)]<1/(2+h). They give exactly the same adaptive transcript as C0;
induction on the queries justifies this despite adaptivity.

For every such C and every unit c, c^T C^2 c<=c^T C c/(2+h). The upper-cap
case of [the endpoint proof](proof.md) therefore says

    U(C,c,e)=(1+h)*c^T C c.

Choose a unit eigenvector c of H with eigenvalue of absolute value one.
The two sharp upper endpoints differ by

    2*epsilon*(1+h) = (1+h)/[2*(2+h)].

Any common numerical answer has error at least
(1+h)/[4*(2+h)] on one source. In particular, exact later-target recovery
is impossible with these m queries. The midpoint of the two endpoints is
also a later threshold for which the all-compatible-source approval answer
differs. Both C values are realizable, for example by their canonical square
sources M=(C^(-1)-I)^(1/2), so this is not an inconsistent information pair.

Conversely, querying the k basis vectors and their k*(k-1)/2 pairwise sums
recovers C by polarization. Thus k*(k+1)/2 scalar quadratic queries suffice
and are necessary for exact arbitrary-later-target endpoint recovery in this
oracle model. The lower-bound argument is deterministic; it does not assert
a randomized high-probability lower bound under unspecified measurability
or input-distribution assumptions.

## What this comparison does and does not establish

This explains a concrete distinction from the one-query certificate in
[the retention comparison](retention_tradeoff.md). A query selected for one
known target can be sufficient for that decision. A reusable block supplies
the exact information needed for arbitrary later directional decisions.
Full-block reconstruction is information-optimal for this particular exact
scalar oracle, using standard linear-algebra reasoning.

A matrix-vector oracle returns more than one scalar and has a different
lower bound. Cheap structural knowledge, a restricted target family, a
nonzero tolerated error, continued access to the source or a library of
task-directed witnesses can change the preferred acquisition. Knowing a
uniform worst-case subspace bound only needs an extreme eigenvalue, as
already noted in retention_tradeoff.md. None of these costs is measured here.
The argument supports the usefulness of a precise retained-information limit;
it does not establish novelty of the analytic N16 endpoint theorem itself.
