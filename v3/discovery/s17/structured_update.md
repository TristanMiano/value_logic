# Exact structured transport before an unresolved edit

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; separate synthesis screen.
This is established Schur-complement/Woodbury machinery combined with the
N16 valid bounds. It is not an additional claim of sharpness or novelty
inside the bounded N16-C/v1 event.

Suppose the known part of a source change is M_1=M+UV^T. In addition to
the old response block C=W^T(I+MM^T)^(-1)W, suppose the interface retains
enough information to verify U=WB and MV=WD for known B,D, with W an
isometry. Then

    M_1 M_1^T-MM^T = W H W^T,
    H=D B^T+B D^T+B(V^T V)B^T.                       (S1)

The extra old action MV and factor Gram V^T V are real information and
must be retained, queried or independently warranted. C alone does not
establish them. An equivalent directly warranted factor-product update H
also suffices. H can be indefinite.

Complete W to an orthonormal basis. The inverse of the Schur complement
of the hidden block of I+MM^T is C. Adding WHW^T changes only its visible
block, hence its Schur complement changes by H. Therefore exactly

    C_1=W^T(I+M_1 M_1^T)^(-1)W=(C^(-1)+H)^(-1).      (S2)

This proof covers singular H and avoids requiring H^(-1). It is a
standard inverse-update identity, not a new matrix theorem. Positive
definiteness follows from a truthful factor update. Without that warrant,
an arbitrary numerical H need not describe any allowed source change.

For truthful old bounds C_minus<=C<=C_plus, define

    C1_minus=(C_minus^(-1)+H)^(-1),
    C1_plus =(C_plus ^(-1)+H)^(-1).                   (S3)

If C_plus^(-1)+H>0, inversion of the two ordered positive matrices proves
C1_minus<=C_1<=C1_plus. To feed the current N16 checker, require also
0<C1_minus and C1_plus<I. A failure of the latter check calls for a better
bracket or a different valid bound; clipping individual matrix entries
or eigenvalues is not a warranted repair.

Now let the final source be N=M_1+R, ||R||op<=e. Apply the existing
receipt to C1_minus,C1_plus and E=e^2. This can be far stronger than
discarding the known direction and using ||UV^T||+e as a single budget.
It does not assert that the resulting interval is sharp given *all*
the original structured information. A conventional joint SDP can retain
those extra restrictions too.

## A small noncommuting worked construction

Take W to be the first two coordinate vectors in R^3 and

    M  = [[3,1,0],[1,2,1],[0,1,2]],
    M_1= [[0,1,0],[1,2,1],[0,1,2]],
    H  = [[-9,-3],[-3,0]].

Here U=(-3,0,0)^T, V=(1,0,0)^T and MV=(3,1,0)^T. Direct inversion gives

    C  = [[2,-2],[-2,5]]/13,
    C_1= [[26,-8],[-8,11]]/37.

Use c=(1,1)/sqrt(2), residual budget e=1/10, and threshold 2/5.
The known edit has norm 3. A norm-only combined budget is consequently
31/10. Discarding its direction cannot certify the threshold: with
v=Wc and P=I-(4/5)vv^T, the alternative N_alt=PM has

    ||N_alt-M||op^2=(16/25)*||M^T v||^2=208/25<(31/10)^2,
    v^T(I+N_alt N_alt^T)v=1+13/25=38/25.

The inverse-compression inequality therefore gives
F(N_alt;v)>=25/38>2/5. This alternative uses the actual same old M,
so a norm-only bound fails even with full old-source knowledge.

By contrast, transporting the truthful old bracket C+/-10^(-4)I via S3
and using t=11/100 with E=1/100 provides a candidate upper certificate
well below 2/5. [structured_check.py](structured_check.py) and its
[result](structured_result.json) verify the bracket transport and the
unchanged checker exactly. The certified upper is
23633804669794/74823188731265, about **0.31586204 < 0.4**. Direct inversion
gives **75/98**, about 0.76531, for the norm-only alternative above.
The source/edit identities and certificate passed in 1,129,100 ns.
This is one constructed capability example, not a new benchmark or an
empirical transfer claim.

## Strong ordinary controls and scope

If R=0, S2 already gives the exact target value. For a fully specified
low-rank R, a larger retained update block may give another exact
Woodbury calculation. These are stronger controls than a total-norm
bound and must be credited. N16 becomes relevant to the remaining
directionally unresolved part, when its norm warrant is cheaper than
retaining the full action or solving the new source.

No complete prices have been supplied for producing W, C, B, D, V^T V,
the residual warrant or future targets. The example only establishes a
valid compositional decision capability. Its mechanism is ordinary
numerical linear algebra and robust optimization; calling it value logic
does not create a performance separation from those same methods.
