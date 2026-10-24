# Nonquadratic reuse: the edit exponent changes

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass54.
This extends the optimization-decision use of an old solution to explicit
ell-p geometry. Generic duality and uniform smoothness are conventional;
the exact formulation and literature delta remain unassessed.

Let1<p<infinity, q=p/(p-1), and

    J_M(x)=||y-M^T x||_p^p+||x||_p^p.

Let x minimize J_M, j=J_M(x)>0, r=y-M^T x, and suppose
||Delta^T||_(p->p)=||Delta||_(q->q)<=e, N=M+Delta. Normalize x,r,y by
j^(1/p), so a=||r||_p,b=||x||_p satisfy a^p+b^p=1. Define
j_p(v)_i=|v_i|^(p-2)*v_i, with value0 at v_i=0. Optimality gives
M*j_p(r)=j_p(x).

The new primal residual at the old solution is w'=(r-Delta^T*x,x).
A feasible dual direction is h=(j_p(r),N*j_p(r)). For EVERY z,

    <h,(y-N^T z,z)> = <j_p(r),y> =1.

Holder therefore gives min J_N>=||h||_q^-p, and

    J_N(x)/min J_N <= [||w'||_p*||h||_q]^p.       (1)

For s>1 put

    R_s(t)=2^(2-s)*t^s,                     1<s<=2,
           s*(s-1)/2*(1+t)^(s-2)*t^2,      2<=s<infinity.

For ||v||_s=1, the scalar Taylor remainder and Holder imply
||v+u||_s^s<=1+s<j_s(v),u>+R_s(||u||_s). For s<=2 use the
coordinate inequality |j_s(v+d)-j_s(v)|<=2^(2-s)*|d|^(s-1) and integrate.
For s>=2 integrate the second derivative and use
sum(|v_i|+|u_i|)^(s-2)*u_i^2 <=(1+||u||_s)^(s-2)*||u||_s^2.

The linear terms in the two factors of(1) have opposite signs:
with t=<j_p(r),Delta^T*x>, their pth/qth powers are bounded by
1-p*t+R_p(e*b) and1+q*t+R_q(e*a^(p-1)). Weighted arithmetic-geometric
mean applied to their ACTUAL nonnegative powers cancels those terms. Thus

    J_N(x)/min J_N
       <= [1+R_p(e*b)/p+R_q(e*a^(p-1))/q]^p.      (2)

The bound uses only the old value, old residual/solution norm split and
the paid edit norm warrant. At p=2 it reduces exactly to
(1+e^2/2)^2, the earlier sharp Hilbert result. For fixed p, the uniform
small-edit order is O(e^min(p,q)). Replacing both a,b by1 gives a looser
source-independent bound if the split is not retained. The norm here is
the induced ell-p norm, not silently the Euclidean operator norm.

## The exponent cannot uniformly be improved

For e>0 let a=2^(-1/p), y=(2a,0),

    M=diag(1,e^(2-q)),
    Delta=e*[[0,1],[-1,0]],
    x_M=(a,0), r_M=(a,0), J_M(x_M)=1.

The signed permutation Delta has induced ell-q norm e. Set B=1+e^q/2.
An exact new minimizer and its residual are

    x_N=(a,-e^(q-1)*a)/B,  r_N=(a,0)/B.

Substitution checks y-N^T*x_N=r_N and N*j_p(r_N)=j_p(x_N).
Strict convexity of the penalty makes this the unique minimizer. Hence

    min J_N=B^(1-p),
    J_N(x_M)=1+e^p/2,
    ratio=(1+e^p/2)*(1+e^q/2)^(p-1).            (3)

For p<2 its leading excess is e^p/2; for p>2 it is(p-1)*e^q/2.
For p=2 it is exactly(1+e^2/2)^2. Thus no uniform O(e^2) relative reuse
guarantee holds for all sources when p differs from2. The source depends
on e; for p<2 its norm diverges as e decreases. A separately bounded source
class is a different claim and may have stronger local properties.

Equation(3) proves the exponent, not a sharp constant for p!=2. Other
scalar configurations can exceed its coefficient, so this witness must
not be promoted to a universal exact envelope.

## Value of computation

If a separate upper bound U_N on min J_N is available, equation(2), with
right side K, gives possible objective improvement at most(K-1)*U_N.
Alternatively an available current objective J_N(x) gives at most
(1-1/K)*J_N(x). Compare the appropriate certified quantity with the cost
of recomputing in common utility units. Acquiring U_N or J_N(x) is paid;
neither is silently supplied by this ratio. This is a conditional receipt
for a computation-purchase decision, not evidence of a measured fee saving.

There is also a bound using only the information already retained:
J_N(x)<=j*((a+e*b)^p+b^p) by the triangle inequality. Thus the possible
improvement is at most

    j*(1-1/K)*((a+e*b)^p+b^p).

This can be conservative, but needs no newly evaluated objective. The
arithmetic and the original receipt acquisition still have their costs.

p_reuse_probe.py passed12 exact rational-family checks at p=3/2,2,3
and200 finite floating primal-dual/smoothness checks at five p values.
Runtime44025600ns, Python3.13.14/NumPy2.2.5; source SHA-256
410cb5d13ddb72feb04b6248f2fcb901ec85d78da90187c27347c3251ed3f117.
These are development checks, not independent confirmation or a sharp-
constant test outside the Hilbert case.
