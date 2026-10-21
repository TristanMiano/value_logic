# A complete robust decision from two scalar receipts

Codex (GPT-6), DEVELOPMENT, October21,2026. A worked consequence of
two_value_sharp.md, using ordinary minimax optimization.

Consider normalized loss r/20+y(r*t0)/y0 for an intervention r>=0. All
structural premises of the positive spectral model are independently supplied;
the only numerical receipts initially are y0 and mu=y(t0)/y0=3/4. There is
no finite upper spectral bound. The sharp one-value upper envelope is
3/(r+3) for0<r<=1 and3/4 for r>=1, with value1 at r0. Thus the minimax
choice is r1 and its worst-case loss is4/5. Its derivative is negative up
to1 and the upper envelope plus price is increasing after1.

Now suppose a second paid receipt gives y(2*t0)/y0=47/78. The sharp envelope
of two_value_sharp.md is U_r for r outside[1,2] and L_r inside, with
a23/31 and b71/94. For r>=2 the upper law has probability31/32 at Z23/31
and1/32 at Z1, so

    U_r=1/32 + (31/32)*23/(23+8*r).

Minimizing r/20+U_r yields

    r_star=(sqrt(3565)-23)/8 > 2,
    worst_loss=(sqrt(3565)-9)/80.

This is the global optimum: the worst-case loss is the supremum of convex
functions of r, hence convex; the derivative vanishes at the displayed
interior point of its exact r>=2 branch. The first-order argument and
attaining two-point law certify the result without identifying the actual
matrix. The worst-case loss drops by(73-sqrt(3565))/80, about0.166 loss units.
All numbers are analytical within this specified toy duty, not measured
application performance. A conventional joint-moment minimax optimizer ties.

The receipt cost is deliberately not hidden inside that gain. Once this
receipt has arrived, the tighter decision problem is worth the displayed
amount in a worst-case comparison of the two ambiguity sets. Before buying
it, its value is unknown and may be unhelpful; this does not prove an ex-ante
value-of-information rule or a guaranteed net saving at that purchase price.
The structural certificate, baseline, both evaluations, numerical precision
and decision computation all belong in a complete economic comparison.

This supplies a concrete reason to retain decision-relevant values without
learning a complete model. The numerical ingredients are established, so a
moderately novel contribution would require a useful paid-refinement or
intervention-scope adapter beyond this worked example.

## A uniform regret certificate for the chosen intervention

The same receipts bound regret against the best intervention for the actual
compatible model. For r>=2 the lower envelope is

    L_r=(3/4)/[71/94+(23/94)*r].

Its priced minimum is

    lower_best=sqrt(141/230)-71/460,

at r=(sqrt(345/94)-71/94)/(23/94)>2. For0<r<=1 the lower envelope is L_r
and its priced derivative is negative. For1<=r<=2 it is U_r and its priced
derivative is also negative. Their minimum values at the right endpoints
are4/5 and1/10+47/78, both above lower_best. The r0 value is1. Consequently
every compatible actual model has optimum priced loss at least lower_best.

The robust r_star therefore has regret at most

    (sqrt(3565)-9)/80 - sqrt(141/230) + 71/460 < 0.0053.

For example sqrt(3565)<59.708 and sqrt(141/230)>0.7829 give the last strict
inequality by direct squaring and rational arithmetic. This upper bound need
not be the sharp minimax regret, because its two extremizing models can differ.
It does give a uniform task-level certificate while model identification
remains incomplete. The guarantee concerns intervention loss only; unpriced
receipt and controller costs cannot be credited as a net performance gain.
