# Prefix guarantees from marginal score laws without independence

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

The learned/uniform product convolution is not justified for correlated costs.
For an alternative with identical known marginal score probabilities p0,p1,p2,
allow arbitrary dependence across queried coordinates. For a prefix length k,
symmetrizing its joint law preserves each marginal and the event S_k<Q. Describe
the symmetric law by counts (n1,n2), n1,n2>=0, n1+n2<=k. Every count distribution
with E[n1]=kp1 and E[n2]=kp2 realizes such a law by uniformly permuting positions.
Thus the exact worst-case prefix survival is the finite linear program

```math
U_k=\max_w\sum_{n_1,n_2}w_{n_1,n_2}
\mathbf 1\{n_1+2n_2<Q\},\qquad
\sum w=1,\quad\sum n_1w=kp_1,\quad\sum n_2w=kp_2,\quad w\ge0.
```

An optimal basic solution has at most three count states. An affine plane
alpha+beta*n1+gamma*n2 lying above every event indicator is a dual upper bound;
matching primal and dual objectives certifies exactness by elementary weak
duality. No external optimizer is required for the small exact screen.

For a fixed ordered prefix and nonnegative query fees, expected acquisition fee
is at most sum_j c_j U_{j-1} + C U_k. Each U_j is individually sharp; their sum
need not be jointly attainable by a single full joint law. Do not call this an
exact worst-case invoice. Immediate fallback gives C, so minimizing these upper
bounds guarantees expected physical fee <= C under known identical marginals,
without independence. Source correctness and the separate pathwise reserve
remain distinct guarantees. Within-request adaptive selective observations do
not automatically estimate these marginals without selection bias.

Prospective dep01: quota6, marginal counts9000/9000/6001 out of24001, prefix
lengths0..12. Enumerate finite count bases using exact integer determinants;
save a nonnegative primal mixture and a globally checked dual plane. Compare
the product-convolution predictions, the perfectly correlated coupling, and the
robust upper invoice for three fee schedules: all1, alternating1/2, and sorted
1/2/3 repeated four times, with fallback C=12,24,48. These are analytical screens,
not paid service streams or new source-admission comparisons. Count compilation
work; do not treat the table as free. Signed integer products are range checked.
