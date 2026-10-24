# The cancellation decision persists on a parameter region

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; analytic robustness of
the selected decision example, not an empirical transfer population.

The capability separation is not confined to one selected threshold gap.
Consider all real R in [32,99] and squared edit budgets E in [7,9], with

    M_R=diag(R,1/3,R), W=[e1,e2], c=(1,1)/sqrt(2),
    C_R=diag(1/(1+R^2),9/10), delta=1/10000, threshold=3/5.

Retain C_R +/- delta I and use the same rational parameters t_lower=10,
t_upper=100. The brackets are strictly interior throughout the rectangle:
the smallest lower eigenvalue is 1/9802-1/10000>0, and the largest upper
eigenvalue is 9001/10000<1. Both t constraints hold for E<=9.

For fixed t=100, U_t(C) is operator increasing in C and increasing in E
on this domain, because d=t-E(1+1/t) decreases with E. Therefore the
largest upper certificate over the rectangle occurs at R=32,E=9. One
exact rational check at that boundary is enough to establish the whole
region; no parameter grid or extrapolation from floating tests is needed.

The old-vector cancellation alternative also persists. Put

    u=(1,1), w0=(1/(1+R^2),9/10),
    x0=(R/(1+R^2),3/10), q=||x0||^2/2, s=u^T w0/2,
    A0=(u-w0)x0^T/(2q),
    a=(w0_2,-w0_1), b=(x0_2,-x0_1), A=A0+(1/10)ab^T.

The same algebra as cancellation_decision.md gives the identical old
optimizer/residual and det(A)=q/5>0. Its cancelling edit has squared norm

    (1-s)^2/q+(q/100)(w0_2-w0_1)^2
       < 121/18+81/200000 < 7 <= E.

Indeed, s>=9/20, q>=9/200, q<1/20, and
0<w0_2-w0_1<9/10 throughout the region. Also ||A||<18/5<R by the
same elementary norm estimate used in the original example. Appending
the scalar R to A therefore gives the same disclosed source norm R,
the same dimensions and the same full old vectors as M_R. The zero-padded
edit produces new value exactly one. Thus even those stronger old-vector
observations cannot certify the universal threshold 3/5 in this region.

The additional block observations are still paid, and the three-query
adapter's sufficient uniform half-width remains 1/25000. The diagonal form
is not extra public structural information given to the comparison. No
population frequency, fee saving or wall-time advantage follows from this
analytic parameter region. It strengthens the example's robustness while
leaving the contribution's prior-art question separate.

## Observed boundary check

[region_check.py](region_check.py) and [region_result.json](region_result.json)
passed the prospectively specified boundary calculation. Its upper certificate is

    2230354600123100 / 3728020398298921 = 0.598267810213... < 3/5,

with exact margin 32288194281263/18640101991494605. The recorded check took
261,200 ns. This single rational calculation plus the monotonicity proof above
establishes the declared rectangle; it is not a sampled empirical success rate.
