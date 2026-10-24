# A stronger comparator: retain the old solution vectors

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. This strengthens the
decision comparison without changing [the contribution event](claim.md).

An ordinary ridge solver often returns the coefficient x and residual w,
not just s=v^T w and m=||w||^2. Charging an extra solve merely to acquire
m would then be unfair. The [preferred decision](two_scalar_control.md)
does not rely on that charge. Here its ambiguity survives retention of the
entire two vectors, provided the full source or edit direction is not also
used as additional information.

For any valid old v,w,x with ||v||=1 and q^2=||x||^2=s-m>0, set

    M0=(v-w)x^T/q^2.

Then M0 x=v-w and M0^T w=x, so this rank-one source has exactly the
same old optimizer and residual. Restricting its coefficients to alpha*x
loses nothing. The rank-one adversarial edit from the two-scalar upper proof
also acts only on span(x), so the same one-dimensional robust objective
remains attainable while preserving those vectors. The exceptional
zero-residual kink needs an available transverse output direction; the
explicit example below has that direction. This is a reconstruction, not
a new novelty claim for the general upper theorem.

## Exact same-vector pair for the preferred decision

In the original coordinates take

    v=(1,1)/sqrt(2),
    M=diag(3,1/3),
    M0=[[3/2,3/2],[1/6,1/6]],
    Delta=[[-1/100,-1/100],[-7/100,-7/100]], N0=M0+Delta.

Both old sources have

    w=(1/10,9/10)/sqrt(2), x=(3/10,3/10)/sqrt(2),
    s=1/2, m=41/100.

The edit has operator norm exactly 1/10, and

    F(N0;v)=229/425 > 1077/2000 = 0.5385.

Thus even retaining the full old optimizer and residual cannot certify the
threshold uniformly from this information and a norm-only edit warrant.
The retained block C=diag(1/10,9/10) excludes M0 and supplies the stronger
certificate already checked. This is an information comparison, not a claim
that an algorithm possessing M or the actual Delta must abstain: it can
use those additional objects, pay for fresh operator applications, or solve
the fixed-source robust problem. Likewise an ordinary implementation given
C performs exactly the same successful certificate calculation.

The vector storage is n+p scalars per target; C uses k(k+1)/2 entries plus
the target-basis interface. This does not by itself establish a memory win:
W and its acquisition can dominate, and the example has n=k=2. Its point is
that the successful decision is not an artifact of discarding a scalar that
the ordinary solver would already provide for free.

[vector_check.py](vector_check.py) and [vector_result.json](vector_result.json)
verify the exact two-by-two pair, both identical vectors, the edit Gram
eigenvalues and edited value. The focused check passed in 218,600 ns on
Python 3.12.14; that duration is only a local check measurement.

## The ambiguity also survives a full-rank prior

The first M0 has rank one. To keep both sources full rank and both full
resolvents strictly below I, add

    H=(1/100)[[9,-9],[-1,1]]

to M0 and use the same Delta. Since Hx=0 and H^T w=0, both complete old
vectors are still identical. The alternative old source has determinant
3/50, and its edited value is

    41503750/77027579 = 0.538816752893... > 0.5385.

The [exact check](vector_strict_check.py) and
[record](vector_strict_result.json) establish the rank, vector equalities,
norm budget and strict margin. The check passed in 285,300 ns. Thus the
comparison does not need a rank-deficient source. Additional quantitative
spectral information could narrow the baseline class further; it is not
part of the declared C-only versus vector-only comparison.
