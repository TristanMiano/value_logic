# Cap-three acquisition: output rank changes the optimal fee

Codex (GPT-6), DEVELOPMENT, October 22, 2026. Proposed new consequence for
the exact private-reset invoice interface. Uses and extends the s13 edge
charging argument; not independent confirmation or a complete CPU claim.

## Contract and full-vector result

There are n>=3 independent fair Boolean coordinates. Each private episode
queries at most three coordinates, exposes only its total query count, and
forgets private answers. Each query costs1 and each used episode costs an
additional reset fee f>=0. Public control can adapt to all previous invoices;
independent coins and controller computation remain unpriced. Correctness is
zero error on every world, with almost-sure termination and finite mean fee.

Let gamma=(7+4f)/6. Every protocol recovering the entire vector has expected
fee at least gamma*n. Ordinary prefix recovery attains

    V_n = gamma*n + [2(1+f)/9]*(1-(-1/2)^n).

Thus gamma is the optimal asymptotic rate. For f<=1/2 this follows already
from s13's parity edge bound. The new case is f>=1/2: full recovery has a
strictly higher leading fee than parity when f>1/2. Parity's rate is
beta=(5+2f)/4; the difference gamma-beta=(2f-1)/12.

## A combined edge and entropy potential

For f>=1/2 define

    a=(8+2f)/3, b=(2f-1)/6, gamma=a/2+b.

Both coefficients are nonnegative. For a compatible world set W of size m,
let E(W) count its induced Boolean-cube edges. Define the unnormalized
potential F(W)=a*E(W)+b*m*log2(m), with F(empty)=0.

For one deterministic episode with output cells W_t, let e be the number
of cube edges separated by its invoices, c its total query count summed over
W, and p its output distribution under the uniform law on W. We claim

    a*e + b*m*H(p) <= c+f*m.                         (1)

The entropy here is of public invoice counts, not private leaves. Giving the
public controller the latter would change the problem.

Normalize m to1. At the first query on which an edge's endpoints disagree,
charge that edge to the query node. At any such split the charge is at most
the smaller branch mass. A depth-two query whose two branches both continue
to depth three cannot separate an edge there: both invoices equal3. Such
nodes contribute zero to the refined charge used below, even though s13's
looser relaxation could charge them.

An active subtree with remaining depth at most2 has at most two informative
counts. If one first branch stops and the other continues, with stopped mass
u, its normalized potential decrease minus query bill is at most

    a*min(u,1-u)+b*h2(u)-(2-u) <= a/2+b-3/2 = 2b.

To verify the inequality write u=1/2+d, use h2(u)<=1 and
min(u,1-u)=1/2-|d|; the remainder is -a*|d|+d<=0 because a>=1.
Uninformative subtrees have zero potential decrease and positive bill, and
also obey this bound. A final query's answer cannot affect its own invoice.

Now classify a depth-three tree by the root's children:

1. Both stop. The invoice is constant, so (1) is immediate.
2. Exactly one continues, with mass t. The root's stopped count1 is disjoint
   from the continuing counts2/3. Entropy therefore decomposes as
   h2(t)+t*H(child). After using the depth-two bound, the normalized potential
   decrease minus query bill is at most

       a*min(t,1-t)+b*h2(t)-1+2b*t <= a/2+2b-1 = f.

   The same substitution proves it because a>=2b (indeed a-2b=3).
3. Both continue. All invoices are2 or3; let v be the count3 fraction. The
   root's edge charge is at most1/2. Charges at depth two sum to at most
   min(v,1-v): only opposite stop/continue branches can separate there, and
   their endpoint masses are disjoint portions of the two invoice classes.
   Total query bill is2+v. Consequently the difference is at most

       a/2+a*min(v,1-v)+b*h2(v)-(2+v) <= a+b-5/2 = f.

   Here the deviation term is -a*|v-1/2|-(v-1/2)<=0 since a>=1.

Zero-query episodes are uninformative and obey (1) with their nonnegative
reset fee. The argument applies to arbitrary W, so it survives adaptive
public history and privately observed answers being forgotten.

Telescoping (1) over the public transcript tree, normalized by2^n, gives
the lower bound. Initially E=n*2^(n-1) and log2(m)=n, so expected potential
is gamma*n. Exact full recovery leaves singleton fibers and zero potential.
For finite-mean almost-surely terminating protocols use finite truncations
and bounded convergence for the finite-state potential; condition first on
independent random tapes. Revealing private coins for this lower-bound
argument does not give the implemented controller extra information.

## Matching construction

While at least two unresolved bits remain, query the first, stopping on0.
On1 query the second, stopping on0. If both are1, query a distinct marker and
stop. The invoices1,2,3 reveal one bit with probability1/2 and two bits with
probability1/2. A previously processed or other coordinate may be the marker;
n>=3 guarantees a coordinate distinct from the two in this episode.
At one remaining bit use cap-two readout. Thus

    V_0=0, V_1=3/2+f,
    V_n=7/4+f+(V_(n-1)+V_(n-2))/2, n>=2.

Solving this recurrence gives the display above, with remainder between0 and
(1+f)/3. The same ordinary prefix implementation is an attainer; the advance
is a sharper lower bound and output-duty distinction, not a new faster code.

## Rank-sensitive linear outputs

Suppose the required output is A*x over F2, A has rank k, and every one of
its n columns is nonzero. Every cube edge changes the required output, so
terminal fibers contain no cube edges. Each output fiber has at most
2^(n-k) worlds, so terminal conditional entropy is at most n-k. Applying
the combined potential and the separate s13 parity-style edge bound gives

    E[fee] >= max(beta*n, (a/2)*n+b*k)
           = beta*n+b*max(0,k-n/2).                 (2)

For f>=1/2 this is a universal bound for such linear maps. It is attained
up to a constant depending only on f by explicit maps of every feasible
rank k=1,...,n:

- If k>=n/2, take n-k disjoint two-bit parity outputs and 2k-n individual
  bit outputs. Recover each pair parity with a two-bit prelude and a third
  marker only on one sign, mean bill5/2+f=2beta. Recover the individual
  outputs together by the prefix procedure. The leading total is exactly
  (a/2)*n+b*k; its remainder is at most(1+f)/3.
- If k<=n/2, use k disjoint nonempty parity groups of size at least2, all
  even when n is even, with at most one odd group otherwise. Recover each
  pair inside a group by the same pair-parity episode and combine publicly.
  At most one remaining bit costs an extra constant relative to beta*n.

This characterizes the least achievable leading fee among these rank-k
linear tasks; it does not claim every matrix of that rank attains (2).
Column structure can impose additional constraints. For f<=1/2, the
existing ordinary prefix decoder recovers all n bits at the common leading
rate beta=gamma, so output rank does not improve that leading fee.

At f1, parity rate is7/4 while full-vector rate is11/6: full recovery costs
at least1/12 more fee per input bit asymptotically, or4.7619% relative to the
parity rate. This is a mathematical comparison of distinct required outputs,
not a measured saving on an unchanged task or a CPU improvement.

## Verification and novelty boundary

A cheap world-set/tree screen should test the local potential inequality,
with the depth-two charging distinction explicit. The all-size claim rests
on the argument, not finite enumeration. Entropy, cube adversaries and
prefix coding are established; the proposed delta is their exact cap-three
acquisition/forgetting/reset-fee composition and the rank-sensitive boundary.
Close prior work and useful scope remain to be assessed. No promotion.

The first [screen](vector_probe.json) passed423,060 local inequalities:
all255 nonempty three-bit sources and257 fixed-seed four-bit sources, using
all99/231 distinct legal cap-three count maps and five reset fees. Entropy
was evaluated with floating logarithms (minimum margin about-7.1e-15,
within the declared1e-9 screen tolerance). Runtime0.4769659seconds.
This supports the small cases; the algebra above supplies the proposed proof.
