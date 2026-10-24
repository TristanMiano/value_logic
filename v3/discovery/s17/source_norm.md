# A source-norm warrant makes the lower gap quantitative

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; separate second-block
extension. This is a valid explicit improvement, not a sharpness claim.

Use the C,Q information and notation in second_block.md. In addition,
suppose the old source has a truthful warrant ||M||op<=K. For any t>0,
let a=1+t, d=t-E-E/t, A=a C-d Q, alpha=A^(-1)Cc and ell=c^T C alpha.
For the source's old responses R,X put w=R alpha and b_old=X alpha.
Let r,x be the new residual and optimizer, and u=(N-M)x. Set

    h=W(c-a alpha)+d R alpha,
    epsilon_r=r-w,
    epsilon_x=x-a b_old,
    epsilon_u=u-(aE/t)w.

The old and new normal equations give

    h=epsilon_r+M epsilon_x+epsilon_u.

The lower square identity, now using the known Q, gives

    F(N;Wc)-ell >= ||epsilon_r||^2+||epsilon_x||^2/a
                         +t||epsilon_u||^2/(aE).

Apply Cauchy--Schwarz to the block linear map
[I,sqrt(a)M,sqrt(aE/t)I]. Its squared norm is at most
1+a K^2+aE/t. Therefore

    F(N;Wc) >= ell + H/(1+a K^2+aE/t),
    H=||h||^2
     =||c-a alpha||^2+2d(c-a alpha)^T C alpha+d^2 alpha^T Q alpha.

Every quantity on the right is retained or warranted. H is nonnegative
because the C,Q class has a realizing W,R. Equivalently, since Cc=A alpha,

    H=d^2 alpha^T(Q C^(-2)Q-Q)alpha >= 0.

The first expression avoids interpreting products of noncommuting matrices
as scalar functions. Q>=C^2 also directly proves positivity of the second
expression by inversion and congruence. The formula works for every t>0;
it does not require the unbounded-source endpoint optimizer.

When H>0 the new warrant gives a strict quantitative improvement over that
particular second-block certificate. The 1/K^2 scale accords with the
limiting-source construction. It does not prove this is the optimal bound
for a given K: a conventional operator-interpolation SDP can retain the
source norm directly and is the appropriate stronger exact comparison.

This supplies a concrete reason to retain an easily available source-norm
warrant rather than erase it in a compressed-information service. It also
keeps the scientific claims distinct: N16 has finite endpoint witnesses;
the extra-Q lower endpoint may be only an infimum; a finite norm cap can
then rule out its near-extremizing sequence. Acquisition and verification
of C,Q,K are still actual duties.

## Observed exact decision

[norm_check.py](norm_check.py) uses the saved L=4 noncommuting second-block
source and its trace as a conservative squared operator-norm warrant.
[norm_result.json](norm_result.json) records the exact improvement

    640/6401 < 1/10 < 4811357/48001099 = 0.100234309218... .

The improved lower certificate remains below that source/edit pair's actual
value. Thus this additional warrant settles a lower threshold that the sharp
unbounded-source C,Q infimum cannot settle. The check passed in 368,200 ns.
The construction and inequalities establish the general statement; one case
does not establish sharpness, practical pricing or novelty.

## Exact conventional comparison with the same norm warrant

In gram_sdp.md fix R^T R=Q and use its two vector lists to form

    A=[X,x], B_old=[W-R,Wc-r-u],
    D=[R,r], F_old=[X,x-z].

Bounded two-sided operator interpolation supplies a source of norm at most K
exactly when the existing cross equality D^T B_old=F_old^T A holds and

    K^2 A^T A-B_old^T B_old >= 0,
    K^2 D^T D-F_old^T F_old >= 0.

Every block here is linear in the two Gram matrices. Unlike the unbounded
kernel-compatibility projection, these two inequalities directly include
the kernels through their zero directions. Together with the separate edit
interpolation constraints, they are a finite exact SDP for the same C,Q,K
source class. This is a direct import of the already inspected bounded
operator-interpolation theorem, not a new general SDP result. It is the
strong control against which an explicit inexpensive correction should be
described. A numerical comparison remains approximate and is not a proof
of the SDP's optimum or of the correction's sharpness.

[norm_sdp.py](norm_sdp.py) and [norm_sdp_result.json](norm_sdp_result.json)
passed the one-case comparison. The approximate unbounded lower/upper values
were 0.09998437733 and 0.60874775733; with the norm warrant they were
0.10026341732 and 0.60874775519. The largest discrepancy from the separate
unbounded formulas was 1.299e-9, within the stated 1e-6 screen tolerance.
The explicit lower certificate 0.10023430922 is slightly weaker than this
approximate exact-SDP lower value. No solver timing advantage is claimed.

## Feasibility and an upper/lower asymmetry

For fixed C,Q the smallest possible squared source norm is

    K_min^2=lambda_max(T^(-1/2) B T^(-1/2)),
    T=C-Q, B=I-2C+Q.

Necessity follows from MX=W-R and X^T X=T: every source has restriction
(W-R)T^(-1/2) on the orthonormalized old coefficient subspace. Its squared
Gram is T^(-1/2) B T^(-1/2). Sufficiency is the realizing M0 from
second_block.md, whose entire domain is that subspace. Thus a norm warrant
is feasible exactly when B<=K^2 T, equivalently

    Q <= (1+beta)C-beta I, beta=1/(1+K^2).

The upper endpoint in second_block.md is attained by this minimum-norm M0,
with at most an appended zero output row. Consequently **every feasible
source-norm upper bound leaves that sharp C,Q upper endpoint unchanged**.
The lower endpoint can improve because its approaching sequence may need
unbounded source norm. The numerical upper tie above has this analytic
explanation; it is not inferred from agreement of decimals.

If the source norm is disclosed as equality rather than an upper bound,
one can append a decoupled coordinate of norm K while keeping W zero there.
This preserves C,Q and the target/edit construction. This observation uses
unrestricted compatible dimensions; a fixed-shape service must be assessed
separately.
