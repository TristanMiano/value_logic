# An exact decision from an old value and a norm receipt

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC.

Suppose ||v||=1, old g(M)=1/10, ||M||<=4, and ||N-M||<=1. The task is
to certify g(N)>=9/200=0.045 without evaluating N. Either the old value
alone or the norm bound alone is insufficient. Together they imply

    g(N) >= 40000/885149 > 9/200.                        (1)

This is a deliberately elementary outward certificate for capped_response.md;
it does not require trusting a floating-point minimizer.

Let t denote the new primal solution norm. For t^2>=9/170 the objective
is already at least9/170>9/200. For smaller t, the exact minimum old
residual curve is ||(1,0)-t*(c,d)||, with c^2=153/10,d^2=7/10.
Use the unit supporting vector(4/5,-3/5). Since

    c<=489/125, d>=209/250,
    1+(4*c-3*d)/5 <= 907/250,

the new objective is bounded below by

    [4/5-(907/250)*t]_+^2+t^2.

The minimum over t>=0 is40000/885149. Both square-root comparisons are
checked by rational squaring; no square-root routine is required. Taking
the smaller of this bound and9/170 proves (1).

## Why both old premises matter

Without the norm receipt, the finite rank-one construction from
finite_extremizers.md permits old s=1/10 and new t=1/25, with edit norm
squared9/10<=1. Its old norm squared is61/2, so it is excluded by K=4.
Thus the old scalar value alone cannot certify the threshold.

Without the old value, M=4,N=5 (scalars) obey both norm bounds and have
new value1/26<9/200. The norm cap alone also cannot certify the threshold.

The checker makes zero NEW operator applications after receiving the
truthful old scalar, norm cap and edit bound. Acquiring those premises,
outward arithmetic, storage and the theorem's verification are paid work.
No end-to-end computation saving is inferred. This is ordinary conic-dual
certification in a specialized retained-information service; an identical
ordinary checker ties.
