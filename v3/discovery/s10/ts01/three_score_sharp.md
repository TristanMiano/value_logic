# Sharp three-score marginal bound by explicit mass allocation

Codex (GPT-6), 2026-10-14. DEVELOPMENT derivation; a finite moment-problem
specialization, not an assessed novelty claim. This strengthens the valid-bound
statement in cheap_dependence.md without changing its executed evidence.

Let k>=1, 1<=Q<=2k, h=Q-1, r=floor(h/2). All k scores have common probabilities
p0,p1,p2 on0,1,2; their dependence is unrestricted. Put x=kp1, y=kp2. Then the
maximum failure probability Pr(sum scores<Q) is exactly

```math
w=\min\left\{1,\frac{2k-x-2y}{2k-h},
\frac{k-y}{k-r},
\frac{k-x-y}{k-h}\ \text{if }h<k\right\}.
```

The bounds in cheap_dependence.md prove the upper inequality. The following
construction proves attainability, including arbitrary real marginal laws.

The integer count states are (n1,n2)>=0 with n1+n2<=k. The convex hull P of the
failure states is exactly

```math
P=\{(a,b):a,b\ge0,\ a+b\le k,\ a+2b\le h,\ b\le r\}.
```

Every failure count satisfies these inequalities. Conversely all vertices of
this polygon are integral: intersections with the axes use integer k,h,r;
the sum and weighted-sum lines intersect at (2k-h,h-k), the horizontal bound
with the weighted-sum line at (h-2r,r), and with the sum line at (k-r,r).
Retain only feasible intersections. Thus P is the convex hull of its integer
failure vertices; it has no additional fractional vertices.

Allocate total mass w to failure. Its unnormalized count means can be chosen as

```math
s=\max\{0,x+y-(1-w)k\},\qquad
f_2=\max\{0,s-x\},\qquad f_1=s-f_2.
```

These satisfy 0<=f1<=x, 0<=f2<=y, s<=wk, and the remaining count means
(x-f1,y-f2) have nonnegative coordinates and sum at most (1-w)k. Also
f2=max(0,y-(1-w)k); the chosen bound w<=(k-y)/(k-r) implies f2<=wr.
Finally

```math
f_1+2f_2=\max\{0,\ x+y-(1-w)k,\ x+2y-2(1-w)k\}\le wh.
```

The last inequality follows from the other two candidate bounds. When h>=k,
x+y<=k already makes the middle expression <=wk<=wh, so that bound is omitted.
Therefore f/w belongs to P whenever w>0. Mix its integer failure vertices to
realize the failure mass and means. The residual means divided by1-w lie in the
full count triangle, so mix its three integer vertices for the residual mass.
For w=0 or1 omit the zero-mass component and use the same limiting construction.
The resulting count law has at least w failure probability and exact required
means. The upper bound proves it cannot have more. Uniform random permutation
of positions realizes identical coordinate marginals and attains w.

For Q<=0 failure is impossible; for Q>2k it is certain. These are separate
trivial cases. This result is sharp for ONE prefix. It does not make the sum of
prefix survival bounds a jointly sharp acquisition invoice, does not cover
nonidentical marginals, and does not establish unbiased learning from adaptively
selected correlated observations. It does supply a constant-size exact marginal
survival certificate for the ordinary robust-prefix construction.
