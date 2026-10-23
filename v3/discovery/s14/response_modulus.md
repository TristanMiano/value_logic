# Exact global inverse-response modulus

Codex (GPT-6), DEVELOPMENT, October22,2026. Corollary of finite_transport.md.
This concerns the operator norm of a regularized inverse, with a rectangular
factor perturbation. It is not a bound on a general matrix function without
the stated factor structure, nor a closest-prior novelty conclusion.

For e>0 put

    q=e^2/4,
    z=[q-1+2*sqrt(q^2+q+1)]/3,
    t=sqrt(z), x=t-e/2.

Then x>0 and the exact dimension-independent modulus is

    omega(e)=1/(1+x^2)-1/(1+(x+e)^2)
            =2*e*t / [(1+(t-e/2)^2)*(1+(t+e/2)^2)].

For all same-shape real matrices M,N with ||M-N||op<=e,

    ||(I+MM^T)^(-1)-(I+NN^T)^(-1)||op<=omega(e).

A scalar pair M=x,N=x+e attains equality. Set omega(0)=0. The limit of
omega(e)/e as e decreases to zero is3*sqrt(3)/8, agreeing with the earlier
sharp differential constant. The modulus tends to one for large e.

## Derivation

For every unit v the scalar theorem bounds g(M)-g(N) by s-L_e(s), where
s=g(M). Swapping M,N bounds the other sign. On the linear branch of L,
s-L_e(s) increases up to s_plus. On the nonlinear branch, write
s=1/(1+x^2), so0<=x<=1/a, with a=(sqrt(e^2+4)+e)/2. The difference is

    f_e(x)=1/(1+x^2)-1/(1+(x+e)^2).

In the centered variable t=x+e/2 its denominator is
t^4+2(1-q)t^2+(1+q)^2. Setting the derivative to zero yields

    3*t^4+2*(1-q)*t^2-(1+q)^2=0.

There is exactly one positive root for t^2, the z displayed above. Since
4(q^2+q+1)>(2q+1)^2, z>q and x>0. The derivative at x=0 is positive;
at x=1/a it is negative because the two derivative magnitudes are in ratio
a^2>1. Therefore the unique maximizer lies inside[0,1/a], and dominates
the linear branch's endpoint. Taking the supremum over unit v proves the
operator claim, with the scalar pair proving attainment.

The earlier additive band s plus/minus(3*sqrt(3)/8)*e can therefore be
replaced by s plus/minus omega(e), clipped to[0,1]. The conditional L/U band
is at least as informative when the old scalar receipt is known. The global
modulus is mainly useful when transporting a whole family of right-hand sides
under one norm guarantee; its cost advantage remains an application question.

Searches for Tikhonov residual-operator perturbation, regularized projection
and rational operator moduli did not establish an exact prior match in the
displayed results. This is incomplete search evidence, not evidence of
absence. Do not raise readiness from that absence alone.
