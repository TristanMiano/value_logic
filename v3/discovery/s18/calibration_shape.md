# Decisions from affine probability shape, with one paid anchor

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; continuation of
[batch calibration](calibration_batches.md), with exact coordinate reports.

## Rank after eliminating batch offsets and gains

A fixed unknown probability vector p in the n-simplex generates reports

    v_gj = s_g*p_j + b_g,  s_g>0,

for the coordinates j exposed in batch g. Each batch has its own unknown
gain and offset; all share the same p. For a nonconstant batch choose indices
j0,j1 with different reported values. Every other j imposes the linear relation

    (v_gj1-v_gj0)*(p_j-p_j0)
      -(v_gj-v_gj0)*(p_j1-p_j0) = 0.                             (A1)

Also require the difference p_j1-p_j0 to have the report's sign. A constant
batch instead requires all its observed coordinates of p to be equal.
These conditions are necessary and sufficient: choose s_g from one nonzero
difference and b_g from one report. Constant batches admit any positive gain
with the corresponding offset. This is ordinary elimination of affine nuisance
parameters, not a new statistical principle.

Collect the equality rows into R. Suppose the reports are consistent, at least
one batch is nonconstant, and rank(R)=n-2. Since R*1=0, choose a mean-zero
nonzero vector q spanning the remaining null direction. Orient it to match
the nonconstant reports. Normalization and positive gains then leave exactly

    p = (1/n)*1 + beta*q,  0<beta<=beta_max,
    beta_max = min_(j:q_j<0) -1/(n*q_j).                        (A2)

All batches' sign requirements must agree with this orientation; otherwise
the assumed consistency fails. Finite gain bounds or additional information
can further restrict beta. Without them, beta=0 is a limit, not an attainable
source when reports are nonconstant.

For every balanced contrast c with sum_j c_j=0,

    c.p = beta*(c.q).

Its sign is completely identified even though its nonzero numerical value
and the probability vector remain unidentified. Thus all comparisons within
a loss family having the same uniform-state mean can be ranked. This does
not identify arbitrary decisions with different constant baselines. Strict
order can be known while the infimum of its margin is zero.

One convenient sufficient rank mechanism is a chain of batches joined by two
overlapping states with distinct values: their relative affine maps align.
It is only sufficient; the actual equality rank and sign constraints are the
general test. Single-state overlaps do not by themselves fix relative gains.

## Why one constant anchor can suffice

For every nonconstant batch, the exact reports determine numbers z_g,k_g with

    v_gj = z_g + k_g*q_j,  k_g=s_g*beta>0,
    z_g=s_g/n+b_g.

Request one value for a known constant loss L in that batch. Its report is
v_gL=s_g*L+b_g, hence

    v_gL-z_g=s_g*(L-1/n).

If L differs from1/n, this single anchor identifies s_g, beta=k_g/s_g, all p,
and then the other observed batch calibrations. Two independent calibration
anchors are not required once the old reports have reduced p to(A2). An
anchor at L=1/n is already predicted and gives no new information.

When any positive-gain anchor of this kind is available at a known fixed fee,
one query is sufficient; zero queries cannot identify a quantity varying with
beta. The cheapest applicable anchor therefore attains the exact query fee
for full identification under this restricted menu. Direct target queries,
previously retained calibration and other menus remain stronger possible
controls. This is a consequence of the information rank, not superiority over
ordinary calibration. If only a decision is requested, even an interval or
one-sided bound on an anchor can suffice.

## Four-state rational example

Batch A reports coordinates1,2,3 as10,14,18. Batch B reports2,3,4 as-3,3,12.
Their independent equations are

    p1-2*p2+p3=0,  3*p2-5*p3+2*p4=0.

The complete compatible family is

    q=(-13,-5,3,15)/8,
    p=(1,1,1,1)/4 + beta*q,  0<beta<=2/13.

For example beta=1/10 gives p=(7,15,23,35)/80, with
s_A=40,b_A=13/2 and s_B=60,b_B=-57/4. Each displayed report is recovered.
All balanced contrasts are ranked by q. In particular p4>p1 always, but
the decision p4>1/3 is unresolved: it holds exactly when beta>2/45.

For batch A, k_A=4 and z_A=33/2. A constant-one anchor has value

    v_A1 = 33/2 + 3/beta.

The exact value93/2 recovers beta=1/10. More weakly, a truthful upper bound
v_A1<=80 gives beta>=6/127 and hence

    p4 >=43/127 >1/3.

The probability vector is still unresolved, but that action is certified.
This is a worked value-information example, not measured acquisition savings.
With an interval anchor and L>1/n, ordinary inversion gives a gain interval
from(v_gL-z_g)/(L-1/n), and then an inverse interval for beta, intersected with
the original simplex constraints. Near L=1/n the inversion is ill-conditioned;
bounded available losses and actual measurement noise must govern anchor choice.

## Scope and comparison

Common-law semantics, known coordinate losses and truthful exact initial
reports are essential. Multiple models with unrelated beliefs cannot be
combined using(A1). These are deterministic identification statements, not
learned calibration guarantees. The inverse-gain linearization and low-rank
completion literature already supply the main tools. The explicit positive
affine gauge, balanced-decision consequence and one-anchor rule are scoped
extensions to evaluate for usefulness, not a new general uncertainty learner.
