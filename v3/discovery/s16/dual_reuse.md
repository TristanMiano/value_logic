# An inexact solver can retain a primal-dual reuse receipt

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass55.
The dual certificate is conventional. This note transports it without
assuming that the old numerical optimization was exact.

Use nonquadratic_reuse.md's objective, conjugate p,q and induced edit norm.
Let x be ANY old primal candidate with j=J_M(x)>0, and normalize its
residual r=y-M^T x and x by j^(1/p). Then ||(r,x)||_p=1. Choose a
nonzero dual direction u0, compute M u0, and normalize

    h=(u,v)=(u0,M u0)/||(u0,M u0)||_q,
    kappa=<h,(r,x)> >0.

Holder gives0<kappa<=1. The old optimum is at least j*kappa^p, so this
also records an ordinary primal-dual gap. Selecting u0 and computing its
image are paid; a fallible forecast does not certify them.

Retain a=||r||_p,b=||x||_p,d=||u||_q and

    eta_r=||u-j_p(r)||_q,
    eta_x=||j_q(v)-x||_p.

For N=M+Delta, the new dual vector h'=(u,N u) still pairs to kappa with
EVERY normalized primal feasible residual(y-N^T z,z), because v=M u.
Let R_s be the elementary smoothness remainder from nonquadratic_reuse.md.
The following entirely scalar receipt bounds reuse:

    T=1+e*(d*eta_x+b*eta_r)
        +R_p(e*b)/p+R_q(e*d)/q,
    J_N(x)/min J_N <= (T/kappa)^p.                (1)

Proof: the pth power of the new primal norm has linear term
-p<j_p(r),Delta^T x>; the qth power of the new dual norm has linear
term q<j_q(v),Delta u>. After weighted arithmetic-geometric mean their
uncancelled sum is

    <j_q(v)-x,Delta u> + <x,Delta(u-j_p(r))>,

which is at most e*(eta_x*d+b*eta_r). The two remainders give T, and
the feasible-dual Holder lower bound gives(1). This argument uses actual
feasible primal and dual vectors; scalar fields copied from an unrelated
solve would not be a certificate.

If the old solve is exact, take h=j_p(r,x). Then kappa=1, both eta terms
vanish, d=a^(p-1), and(1) reduces to the exact-old-solution bound. At e=0,
it reduces to the existing gap ratio kappa^-p. Thus solver error and edit
error appear in the same receipt without treating either as zero.

The current objective obeys J_N(x)<=j*((a+e*b)^p+b^p). A sufficient upper
bound on the objective value of recomputation is consequently

    j*((a+e*b)^p+b^p)*(1-(kappa/T)^p).            (2)

Comparing(2) with a certified lower computation price gives the earlier
robust decision rule. This is a sufficient bound, not the expected value
of an unspecified solver. Verification of the norms, source identity,
duality pairing and edit warrant has its own cost and rounding duties.

For p=2 the earlier specialized approximate-solve theorem can be stronger;
use it as a control. The purpose here is an explicit broadly applicable
certificate for unfinished optimization, not replacing a sharper known
quadratic result or claiming a new generic duality theorem.
