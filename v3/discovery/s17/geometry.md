# A conventional geometric interpretation that constrains novelty

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; our derivation.
This is a comparison route, not an extra contribution claim or an enlargement
of [N16-C/v1](claim.md).

For a source M, consider its graph subspace G_M=range([M;I]) in the direct
sum of output and parameter spaces. The ridge objective is

    F(M;v)=distance(([v;0]),G_M)^2.

An edit Delta sends G_M to G_(M+Delta) by the invertible shear

    T_Delta=[[I,Delta],[0,I]].

This shear fixes [v;0]. Therefore both T_Delta and its inverse compare the
old and new distances. Singular-value decomposition of Delta reduces the
nontrivial singular values of T_Delta to those of [[1,sigma],[0,1]]. If
||Delta||op<=e and r=(sqrt(e^2+4)+e)/2, these lie between 1/r and r.
Consequently

    F(M;v)/r^2 <= F(M+Delta;v) <= r^2 F(M;v).

Since r^2=1+t0, these are exactly the t=t0 endpoint members of N16's
families. Their universal multiplicative constant is thus an elementary
shear-distortion constant. It should not be advertised as a new principle
of uncertainty or a separate discovery in matrix perturbation theory.

The retained matrix C records inner products of the projections of k target
vectors into the orthogonal complement of G_M. It leaves other graph
coordinates unresolved. N16's more detailed result uses this finite block
to strengthen the distance bounds and proves that no tighter scalar bound
is uniformly valid for the declared information class. A sharp partial-
graph-information theorem in the subspace/gap literature could supply the
same result under different notation. This is another concrete prior-art
comparison duty, not evidence of novelty from a change of vocabulary.

This interpretation also explains usefulness without excluding conventional
methods from value logic: a bounded reasoner retains selected response
information and obtains a warranted future decision after a model edit.
The mathematical mechanism is conventional geometry and optimization.
The candidate contribution, if it survives comparison, is the precise
information-dependent guarantee and its usable finite certificate.
