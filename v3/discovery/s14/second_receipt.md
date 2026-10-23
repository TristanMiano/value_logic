# One extra scalar gives a sharp lower transport certificate

Codex (GPT-6), DEVELOPMENT, October22,2026. A new derivation within the
numerical-receipt branch; no independent review or novelty verdict.

Use g(M)=v^T(I+MM^T)^(-1)v=s, ||v||=1. Let

    w=(I+MM^T)^(-1)v, z=M^T w,
    m=||w||^2, r=m/s.

Then ||z||^2=s-m, s^2<=m<=s, and s<=r<=1. For actual finite matrices,
m=s<1 is impossible, but closure endpoints are useful for sharp envelopes.
The extra retained scalar r can be computed from a certified solve; it is
not derivable from s alone and is not a free observation.

For ||N-M||op<=e, define

    C_e(r)=1+2*e*sqrt(r*(1-r))+e^2*r.

The following lower bound is sharp as an infimum over arbitrary finite
dimensions with the two old receipts fixed:

    g(N) >= s/C_e(r).                                      (1)

## Proof and sharpness

The standard variational identity is

    g(N)=max_x [2*v^T x-||x||^2-||N^T x||^2].

Restrict x to alpha*w. Since v^T w=s and
||N^T w||<=||z||+e*||w||, optimizing alpha gives

    g(N)>=s^2/[m+(sqrt(s-m)+e*sqrt(m))^2]=s/C_e(r).

No matrix entries are used when applying the final scalar rule. If m=s^2,
a scalar M=sqrt((1-s)/s), N=M+e attains equality. For s^2<m<s, put
q=1/(1+K^2) and, for sufficiently large K,

    x=(m-s*q)/(s-q), p=(s-q)/(x-q),
    M=diag(sqrt((1-x)/x),K),
    N=diag(sqrt((1-x)/x)+e,K),
    v=(sqrt(p),sqrt(1-p)).

Both old moments are exactly s,m: p*x+(1-p)*q=s and
p*x^2+(1-p)*q^2=m. As K tends to infinity, x tends to r and p to s/r.
The new response tends to s/C_e(r). Thus the two-dimensional limiting
construction meets the lower bound. This does not assert a finite minimizer
in every interior case. The e0 case is immediate.

## Recovering the one-receipt theorem and measuring extra information

C_e(r) is concave on[0,1]. Its maximum is a^2 at
r_star=a^2/(1+a^2), where a=(sqrt(e^2+4)+e)/2. Maximizing over the permitted
r in[s,1] recovers exactly L_e(s) in finite_transport.md. The earlier
piecewise bound therefore has a precise missing-information interpretation:
it must allow the most sensitive residual-energy ratio compatible with s.

For example, s1/10, m1/100 and e1/10 give the lower bound
100/1061, approximately0.094251. The one-scalar lower envelope is about
0.090488. This is a stronger lower certificate after acquiring one extra
scalar. It is not a free improvement with unchanged information.

If receipts are intervals s in[l,u], r in[A,B], intersect their ranges with
0<=s<=r<=1. For l>0 and a nonempty source, a sharp lower bound for this
rectangular information source is

    l/C_e(clamp(r_star,max(A,l),B)).

The infimum occurs at s=l: holding any feasible r fixed lowers the numerator
and preserves feasibility when s is decreased to l. Maximizing the concave
denominator then gives the clamped expression. Endpoint closure qualifications
are inherited. This avoids treating a noisy point estimate as an exact moment.

## Acquiring the extra receipt and its limitations

For y(t)=E[1/(1+t*lambda)], the squared-resolvent moment is
y(t)+t*y'(t). Thus r is also a normalized value-and-slope observation.
It does not reveal the spectrum or resolve all underlying mathematical facts.

An approximate primal/dual pair z_hat,w_hat gives a certified gap

    Delta=||v-M*z_hat-w_hat||^2+||z_hat-M^T*w_hat||^2.

The dual gap implies ||w-w_hat||<=sqrt(Delta). Together with a truthful
value interval[l,u], this supplies conservative norm and ratio intervals,
for example r_low=max(0,||w_hat||-sqrt(Delta))^2/u and
r_high=(||w_hat||+sqrt(Delta))^2/l when l>0, clipped to[0,1].
Operator applications, norms, outward arithmetic and storing the extra scalar
are charged. If they erase the savings, retaining the receipt is not useful.

A simple upper bound from the unscaled primal witness is
g(N)<=s+2*e*sqrt(m*(s-m))+e^2*(s-m), clipped to1 and intersected with U_e(s).
This upper bound is sound but no sharpness claim is made. The one-sided
sharp lower theorem does not silently become a sharp two-sided theorem.

Ordinary variational certificates perform the same calculation. The possible
contribution is the explicit optimal information contract and useful paid
reuse; the underlying duality and sensitivity ideas are established.

The small executed second_receipt_probe.py screen passed 240 exact matrix
panels/480 inequalities, 20 scalar equality cases and 12 exact moment-preserving
constructions. Three limiting sequences approach the displayed bound in
floating-point evaluation; their old moments are checked as exact rationals.
Runtime 20,044,500 ns. This is same-model development evidence only.
