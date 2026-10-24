# The exact relative diameter has an elementary ordinary certificate

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; a stronger comparison
discovered after [the rational SDP certificate](relative_pair.md). This
removes its apparent coefficient advantage over ordinary methods. It is
separate from the N16-C/v1 contribution event.

For every finite real M, any v, and two edits N_i=M+Delta_i satisfying
||Delta_i||op<=1, the exact best universal coefficient in

    |F(N_0;v)-F(N_1;v)| <= g F(M;v)

is

    g = 4 r (1+r^2)/(r^4+4),
    r=sqrt(q),  q^3+3q^2-12q-4=0,  9/4<q<5/2.       (X1)

The root in that interval is unique. A one-dimensional source M=[r],
edits Delta_0=[-1], Delta_1=[1], and v=1 attain the coefficient. Thus
there is no need for a limiting source, Gram optimization or numerical
duality assumption. The following proof supplies an exact ordinary
comparison to the earlier near-optimal SDP result.

## Two established inequalities on the same full resolvent

Let S=(I+MM^T)^(-1), so 0<S<=I. For any u>0, Young's inequality on
N_1=M+Delta_1, followed by order-reversing inversion, gives

    (I+N_1 N_1^T)^(-1) >= S[(1+u)I-d_u S]^(-1),
    d_u=u-1-1/u.                                    (X2)

The denominator is positive even when d_u<0. In the reverse direction,
Young applied to M=N_0-Delta_0 gives

    (I+N_0 N_0^T)^(-1) <= (1+t)S[I+d_t S]^(-1)       (X3)

whenever t>0 and I+d_t S>0. These are precisely the conventional
fixed-source families in [fixed_source.md](fixed_source.md). Compression
is not being performed here, so the lower u need not exceed the N16 cap.

Choose u=1/r and t=1/(r-1). Write

    k=1+r-r^2,  l=r^2+r-1.

The cubic in X1 is negative at 9/4 and positive at 5/2. Its derivative
3q^2+6q-12 is positive on this interval, and its single positive turning
point precedes it; there is only one positive root. In particular
3/2<r<sqrt(5/2)<(1+sqrt(5))/2, so 0<k<l and d_t=k/(r-1)>0.
Thus both X2 and X3 apply for every source, including S with eigenvalue one.

Subtract X2 from X3. In their common spectral basis the difference is
lambda R(lambda), where

    R(lambda)=r/[r-1+k lambda]-r/[r+1+l lambda].        (X4)

All denominators are positive for 0<=lambda<=1. It remains to maximize
this scalar function; no commutation between either edited matrix and M
is assumed or needed for the preceding Loewner inequalities.

## Exact spectral maximum

Put lambda_star=1/(1+r^2). Differentiation gives

    R'(lambda)=r{l/[r+1+l lambda]^2
                   -k/[r-1+k lambda]^2}.

Its sign is that of

    sqrt(l)(r-1)-sqrt(k)(r+1)
      +[k sqrt(l)-l sqrt(k)]lambda.                  (X5)

The coefficient of lambda is negative. At lambda_star the two denominators
in X4 are respectively r[(r-1)^2+1]/(1+r^2) and
r[(r+1)^2+1]/(1+r^2). Direct expansion gives

    l[(r-1)^2+1]^2-k[(r+1)^2+1]^2
       =2(r^6+3r^4-12r^2-4)=0.                     (X6)

Hence X5 vanishes at lambda_star, is positive before it and negative
after it. This proves the global maximum of R on [0,1] occurs there.
Substitution gives R(lambda_star)=g in X1. Functional calculus now gives

    (I+N_0 N_0^T)^(-1)-(I+N_1 N_1^T)^(-1) <= g S.

Interchanging the edits proves the opposite inequality and the stated
absolute-value bound. The scalar source in X1 attains both X2 and X3
at lambda_star and gives exactly g. This proves optimality in every finite
dimension simultaneously, with a scalar extremizer.

## Disposition of the earlier comparison

The earlier rational coefficient 2.1596506315 remains a valid exact
certificate. Its reported 0.33156% improvement was relative to the
particular primal/dual-reuse comparison then available. X1 is a stronger
ordinary analytic comparison and is exact. Therefore there is **no
remaining positive coefficient advantage over this strongest control**;
the earlier coefficient is slightly looser. Preserve the earlier evidence
and its chronology, but do not carry its percentage forward as the final
headline.

The exact diameter may itself be a useful small mathematical synthesis.
The proof is a short combination of established inequalities and a scalar
maximum, so its moderate novelty is unassessed and should not be presumed.
Park N17-P/v0 as a competing algorithmic-improvement claim; retain X1 as
a useful analytic result and comparison tool. It does not change the
N16-C/v1 readiness probability.
