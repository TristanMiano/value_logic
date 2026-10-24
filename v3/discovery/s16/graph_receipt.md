# A graph projection joins mean, residual and covariance receipts

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass42.
Graph subspaces, perturbation angles and robust Gaussian decisions are
conventional machinery. No generic novelty claim is made.

For M:R^m->R^n let G_M={(u,Mu)} and P_M be its orthogonal projector.
For observed y and ridge posterior mean mu_M=(I+MM^T)^(-1)My,

    P_M(y,0)=((I+M^TM)^(-1)y, mu_M).

Its squared norm is r_M=y^T(I+M^TM)^(-1)y, the optimized ridge objective.
For nonzero y and a unit target v, compress P_M onto the orthonormal
vectors (y/||y||,0),(0,v). The retained two-by-two matrix is

    C_graph = [[r_M/||y||^2, v^T mu_M/||y||],
               [v^T mu_M/||y||, 1-v^T S_M v]],
    0<=C_graph<=I.                                  (1)

Thus feasible scalar receipts obey, with s=v^T S_M v,

    (v^T mu_M)^2 <= min(r_M*(1-s), (||y||^2-r_M)*s).

These relations can detect inconsistent mean/variance/residual receipts.
They do not establish model calibration or recover the whole posterior.

## A sharp uniform graph-angle modulus

If ||N-M||op<=e, then

    ||P_N-P_M||op <= delta(e),
    delta(e)=e/(1+e^2/4) for0<=e<=2, and1 for e>=2.   (2)

The equal-dimensional graph gap is

    ||(I+NN^T)^(-1/2)(N-M)(I+M^TM)^(-1/2)||op.

For any nonzero test vectors, normalize their underlying input/output
vectors x,y to unit norm, set alpha=y^TMx,beta=y^TNx, and d=|beta-alpha|.
The corresponding bilinear quotient is at most

    d/sqrt((1+alpha^2)(1+beta^2)),      d<=e.

Since (1+alpha^2)(1+beta^2)=(1+alpha*beta)^2+d^2 and
alpha*beta>=-d^2/4, this quotient is at most d/(1+d^2/4) for d<=2,
and at most1 generally. The former increases up to d=2. Scalar sources
M=-e/2,N=e/2 attain(2) for e<=2; M=-1,N=1 attain1 when e>=2.
This is a same-model derivation of a graph-gap fact, not a novelty finding.

In particular every later compression satisfies ||C_graph,new-C_graph||
<=delta(e). This can bound joint functionals of retained mean and covariance,
but is often weaker than the task-specific formulas already obtained.
An operator-norm bound on this two-by-two difference is not an arbitrary
independent interval for each entry, and realizability by graph projectors
imposes further restrictions. No exact joint-compression envelope is claimed.

## A directly useful posterior decision, with a narrower scope

The posterior-reuse identity from posterior_reuse.md gives

    |v^T(mu_N-mu_M)| <= a*sqrt(v^T S_N v),
    a=e*sqrt(r_M).

If a retained certificate gives v^T S_N v<=U and v^T mu_M>0, then under
the declared common Gaussian prior/noise model,

    P_N(v^T theta<=0 | y)
       <= Phi(a-(v^T mu_M)/sqrt(U)).                (3)

This follows by standardizing the normal posterior and keeping the
mean/variance coupling in the first inequality. It also holds for any
posterior mixture over admitted N, since every component satisfies the same
bound. Unknown mixture weights need not be learned to certify this one
decision. If y=0 the means vanish and the sign probability is1/2.

This is model-conditional sign risk, not a distribution-free guarantee
about the actual world. It differs from simply bounding a mixture covariance,
which must include between-model mean variation. Strong conventional robust
Bayesian calculations given these same receipts tie. The remaining question
is a real deployment where the retained joint quantities justify avoiding
an expensive recomputation; this note supplies no observed savings.
