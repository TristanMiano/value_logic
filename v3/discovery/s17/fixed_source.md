# A strong conventional reduction for the fully known source

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; our algebraic specialization.
This strengthens the comparison in [reduction.md](reduction.md). The
[matrix S-lemma](https://arxiv.org/pdf/2006.00870), Theorem 9, supplies the
equivalence used below under strict matrix Slater. The primary-source scope
is recorded in [literature.md](literature.md). The derivation below is ours;
it is not a claim that the source states N16-C verbatim.

## Exact worst reoptimized value from a known M

Fix a finite M, unit v and E=e^2>0. For lambda>0, Schur complementation gives

    F(M+Delta;v)<=lambda
    iff lambda[I+(M+Delta)(M+Delta)^T]-vv^T >= 0.

Put Z=Delta^T. The norm ball is the matrix quadratic constraint

    [I;Z]^T diag(E I,-I) [I;Z] >= 0.

It has a strict feasible point Z=0. Applying the matrix S-lemma to the
displayed performance inequality gives an exact equivalence with existence
of alpha>=0 such that

    [[lambda(I+MM^T)-vv^T-alpha E I, lambda M],
     [lambda M^T,                         (lambda+alpha) I]] >= 0.

The lower diagonal block is positive definite. Set rho=alpha/lambda and
take its Schur complement. The condition becomes

    lambda A(rho) >= vv^T,
    A(rho)=(1-rho E)I+[rho/(1+rho)]MM^T, rho>=0.        (1)

For A(rho)>0 the least lambda is v^T A(rho)^(-1)v. Singular admissible
A does not create a lower infimum missed by positive definite A: for
0<=theta<1, concavity of rho/(1+rho) gives
A(theta rho)>=(1-theta)I+theta A(rho)>0. If (1) holds at singular A,
then v lies in its range, and approaching it this way recovers the
pseudoinverse quadratic value. This also follows directly by simultaneous
diagonalization with MM^T. Include rho=0, whose value is one.

Let S=(I+MM^T)^(-1), t=1/rho for rho>0, and
d(t)=t-E-E/t. Since

    A(rho)=[S^(-1)+d(t)I]/(1+t),

the exact fixed-source endpoint is

    sup_{||Delta||op<=e} F(M+Delta;v)
      = inf { (1+t)v^T S[I+d(t)S]^(-1)v :
              t>0, I+d(t)S>0 },                       (2)

with the value one included as t=infinity. Thus the rational upper family
and a scalar optimization already follow from a standard exact robust
certificate. Merely changing from a robust common action to reoptimized
value does not distinguish N16 from this strongest comparison.

## Why the retained compression still requires work

For N16 only C=W^T S W is known, and hidden coordinates of S are allowed.
When d>=0, the rational map in (2) is operator concave, so compression gives
the uniform upper bound U_t(C). This restricts the allowed common parameter
to t>=t0. For d<0 the compression inequality reverses; substituting C in
(2) is no longer a valid universal upper bound for the enlarged class.

This difference is numerically real. For M=3, v=1 and e=1, the known-source
maximum is 1/5. Equation (2) attains it at t=1/2, where d=-5/2. If only
C=1/10 is retained and extra output coordinates are permitted, N16's
endpoint is (3+sqrt(5))/20, attained at t0=(1+sqrt(5))/2. This is larger
than 1/5. The cap is therefore not a harmless reparametrization of the
fully known-source result.

The additional task is to show that the uniformly valid compressed envelope
is EXACT for the compatibility class. The [direct proof](proof.md) supplies
canonical witnesses at interior optima and moment-adjusting dilations at the
cap. A prior theorem could still make that step routine; this explicit
reduction narrows rather than eliminates the novelty uncertainty.

## Fully known-source lower endpoint

When 0<S<I, the lower family is valid for every t>0 before compression,
including d<0. The scalar value tends to zero at both ends of this open
parameter interval. At a maximizer, its derivative yields the rank-one
edit in proof.md section 4, whose normal equation proves attainment.
Thus for a canonical full-row-rank source

    inf_{||Delta||op<=e} F(M+Delta;v)
      = max_{t>0} v^T S[(1+t)I-d(t)S]^(-1)v.           (3)

This is a direct elementary derivation, not an imported novelty claim.
Compression needs d>=0 for its lower bound too. For M=3 and e=1, the
known-source minimum is 1/17, attained by t=1/3 and N=4; the larger
information class permits the smaller value (3-sqrt(5))/20.

The critical candidate delta is consequently the complete sharp
information contract, not the fractional families, scalar optimization,
rank-one perturbations, or the general idea of a conditional certificate.
