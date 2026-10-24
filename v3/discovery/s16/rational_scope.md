# Rational response models and a strong structural control

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass33.

The private-repair construction does not require literal polynomial outputs.
Suppose A(x)=a(x)/d(x) and B(x)=b(x)/h(x), with vector numerators and scalar
denominators nonzero on the sampling grid. If their coefficient/degree
contracts imply

    deg(h*a-d*b)<=D,

then any false constant-space claim A-B in U has a nonzero annihilator
numerator of degree at most D. The fixed-claim acceptance probability is at
most(D/q)^k, exactly as before. Denominators need not be recovered by the
checker, but their degree and nonvanishing warrants must be sound. On a
domain with poles, the identity conclusion applies only where defined.
Rejecting singular samples and conditioning on the rest changes the sampling
law and requires its own bound; it cannot be silently substituted here.

## A natural finite-dimensional response family

Let K0 be a fixed positive definite n-by-n matrix, P an n-by-r matrix, and

    K_j(x)=K0+P D_j(x)P^T,       A_j(x)=K_j(x)^(-1)b(x),

where D_j is a polynomial r-by-r matrix of degree at most d, positive
semidefinite on the real sampling grid, and b is polynomial of degree db.
This includes changing a small set of conductances in a grounded resistor
network. The matrix determinant lemma and Woodbury algebra show that every
response has a scalar denominator of degree at most r*d and a vector
numerator of degree at most r*d+db. Thus a difference of two responses has
annihilator numerator degree at most2*r*d+db. Positivity excludes real-grid
poles. The degree depends on the edited rank rather than n.

All response differences lie in the fixed space R=range(K0^(-1)P), because

    K0(A_i-A_j)=P[D_j P^T A_j-D_i P^T A_i].

Hence dim(R)<=r. More generally, a proposed vector model B satisfying the
exact structural residual condition K0 B-b in range(P) has A_i-B in R,
even if its interior/edited-region prediction is inaccurate. This separates
a guaranteed error structure from uncertain parameter values. Numerical
errors outside that residual space need an extra approximate-scope warrant.

The rank/degree contracts connect private correction to an actual family of
counterfactual linear systems, rather than only arbitrary polynomial tables.
They do not make rational arithmetic, model calls or proof of positivity free.

## Cheap rejection of an unfair application claim

If K0 and P are accessible and base solves are allowed, an ordinary method
computes K0^(-1)P with r right-hand-side solves. It then has the whole error
space exactly and can use Woodbury/static condensation directly. A service
buying k private full responses plus up to r public counterexamples cannot
claim fewer large solves against that control merely by counting samples.
Factorization sharing strengthens the structural control further.

The private service remains potentially relevant when only a paid response
API and trustworthy structural metadata are available, or when a response
evaluation is much cheaper than obtaining a new structural solve. That is a
different access contract requiring a real application and complete pricing.
No benchmark is built for the accessible-matrix case, because its elementary
ordinary comparison already removes the proposed advantage. Woodbury and
low-rank response structure themselves are established machinery.
