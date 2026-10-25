# Decisions from overlapping value reports with uncertain calibration

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; broad constructive branch.
This extends P3-02's single common scale/offset interface. Blind calibration,
homogeneous lifting, set identification and ordinary linear programming are
the relevant existing machinery; a novelty assessment is still required.

## Information contract and exact lift

One fixed probability vector p lies in a supplied rational polytope P inside
the n-state simplex. It may be a subjective law over unresolved cases; it is
not thereby a learned law of mathematical truth. In report batch g, known
loss rows l_gj have expected values l_gj p. The instrument reports them in
unknown common units and with an unknown common offset:

    v_gj = s_g l_gj p + b_g,  s_g>0.

Different batches may have different s_g,b_g. A truthful simultaneous receipt
places every v_gj in[a_gj,z_gj]. The interval event, loss semantics, common
within-batch calibration and persistence of p are external premises. This
does not infer them from the fact that a linear program is feasible.

Set t_g=1/s_g>0 and u_g=b_g/s_g. Then the information class has the exact
linear lift

    p in P,
    a_gj*t_g <= l_gj p+u_g <= z_gj*t_g for every g,j.          (C1)

Known scale limits0<slo_g<=s_g<=shi_g<infinity become
1/shi_g<=t_g<=1/slo_g. Known offset limits blo_g<=b_g<=bhi_g
become blo_g*t_g<=u_g<=bhi_g*t_g. An absent offset is u_g=0.

Necessity follows by multiplication by positive t_g. Conversely, any point
of(C1) with every t_g>0 defines s_g=1/t_g, b_g=u_g/t_g and admissible
reported values v_gj=(l_gj p+u_g)/t_g. Thus projecting this polyhedron onto
p gives exactly the compatible probability laws. Bounds on a new expected
loss c p and on action contrasts are linear optimization over(C1), without
first selecting a calibration or a point probability estimate. Independent
report noise is not needed once the simultaneous interval premise holds.

The additional storage/computation includes all retained loss rows, bounds,
source versions and calibration constraints. The LP is an ordinary strong
comparator, not a proposed advantage over ordinary probabilistic inference.

## Strict positivity, consistency and unattained limits

If no upper scale bound is supplied, t_g>0 must not silently become t_g>=0
when testing consistency. A finite LP can test the former: introduce
0<=lambda<=1, require t_g>=lambda for every g, and maximize lambda.
An optimum greater than0 is equivalent to actual consistency. A feasible
point with only lambda=0 does not justify any probability conclusion.

After one strictly positive feasible point exists, the nonnegative closed
lift has the same infima and suprema for linear targets as the strict lift.
Indeed, mix any point of the closed lift with the strictly positive point;
the mixtures have all t_g>0 and approach the original point. Projection
therefore gives the same sharp limiting bounds, although endpoint attainment
may fail. A strict decision at a boundary should be checked as infeasibility
of its opposite with t_g>0, rather than inferred from a non-strict optimum.
With finite positive scale bounds, the projected feasible set is compact
and its finite target extrema are attained.

## Complementary batches can identify what neither does alone

Take n=3 with no offsets. Batch1 reports(s1*p1,s1*p2)=(2,3).
Batch2 reports(s2*p2,s2*p3)=(6,10). Each scale is arbitrary and positive.
Together the ratios and normalization force

    p=(1/5,3/10,1/2), s1=10, s2=20.

Neither batch's loss-row span contains the normalization row, so P3-02's
single-scale global criterion supplies no nonconstant globally identified
linear expectation from that batch alone. The overlap supplies a calibration
bridge when the common coordinate has positive probability.

That condition matters. Reports(2,0) and(0,10) force p2=0 but allow every
p1 in(0,1), p3=1-p1, with s1=2/p1 and s2=10/p3. The observation graph is
connected through state2, yet the zero-probability bridge transmits no ratio.
The sharp contrast bounds for p1-p3 are(-1,1), with neither endpoint attained.
Connecting a report graph syntactically is not enough.

## Exact positive-support graph characterization

For coordinate reports v_gj=s_g p_j with known absent offsets, consider the
bipartite graph of batch nodes and state nodes. Assume every observed value
is strictly positive and every state has at least one observation. Each
connected component determines all its p_j ratios by alternating divisions
along paths. Products around cycles must agree; inconsistent cycles refute
the stipulated exact calibration interface.

Normalize the recovered state ratios within component k to rho_k. Every
compatible law, and no other one, has

    p_j = m_k*rho_kj for j in component k,
    m_k>0, sum_k m_k=1.

To prove sufficiency, pick arbitrary such component masses and rescale all
batch scales inversely within each component. This preserves every observed
product. Necessity follows by propagating ratios along the connected graph.
Full p is identified iff there is one state-containing component. For a
new contrast c, put d_k=sum_j c_j*rho_kj. Then c p=sum_k m_k*d_k.
Its sharp limiting interval is[min_k d_k,max_k d_k], with the usual strict
endpoint qualification when all component masses must be positive. A contrast
is numerically identified precisely when all d_k agree. Its sign may be
identified even when they differ: all d_k<0 implies c p<0 for every law.

Thus multiple useful value reports can settle an action without identifying
component masses, global probabilities, or individual batch scales. This is
an ordinary partial-identification consequence, not new probability semantics.

## Unknown offsets leave a different gauge

When each coordinate-report batch also has an arbitrary offset, mere graph
connectivity is weaker still. Even a complete report matrix admits the
global transformation, for a>0 sufficiently near1,

    p' = a*p+(1-a)*1/n,
    s'_g=s_g/a,
    b'_g=b_g-s_g*(1-a)/(a*n).

It preserves all reports and normalization while changing a nonuniform
interior p. Therefore complete coordinate reports with arbitrary offsets
need not identify the law. A known zero-payoff anchor in a batch supplies
its offset; further overlaps or anchors must then justify the remaining
calibration transport. Equation(C1) handles these constraints directly,
including degenerate overlaps; a connectivity slogan does not.

Next useful development: exact small rational examples with interval reports,
then a close blind-calibration comparison and a paid-query consequence. Do
not count another single-common-scale example as a new result.

## Bounded scale information compresses to component-mass intervals

In the positive coordinate-report case with absent offsets, write
kappa_g=v_gj/rho_kj for a batch g in component k. Cycle consistency makes
this independent of its observed state j. Then s_g=kappa_g/m_k. Consequently
scale bounds imply exactly

    max_(g in k) kappa_g/shi_g <= m_k
      <= min_(g in k) kappa_g/slo_g.

Together with sum m_k=1, these intervals characterize the compatible laws.
Bounds on a new contrast are a bounded-simplex linear program with one
variable per component. To maximize, start with all lower masses and fill
remaining mass in descending d_k order up to their upper capacities; reverse
the order to minimize. The exchange proof moves mass from a lower coefficient
to a higher coefficient whenever both capacities permit it. The cost includes
constructing ratios, checking cycles and sorting; this is ordinary continuous
knapsack optimization after the calibration reduction.

## A priced calibration-only interface

Suppose existing reports are fixed, scales are unbounded positive, offsets
are absent, and the only new purchase is an exact unit-payoff report in a
chosen batch. It reveals s_g, hence the mass m_k of that component. Let
c_k>0 be the cheapest fee for such a report within component k. This is an
explicit restricted menu, not a ban on cheaper direct task queries when
those are actually available. An arbitrary-loss report plus a constant
anchor can otherwise settle a single target directly and must be compared.

Consider choosing between two actions by whether sum_k m_k*d_k<=tau.
If tau lies strictly between min d and max d, the exact deterministic
worst-case calibration fee for a sound action is

    sum_k c_k - max_d sum_(k:d_k=d)c_k.                       (C2)

To attain(C2), leave one most expensive equal-coefficient class unqueried
and buy all other component masses. Normalization gives the total mass of
the remaining class, which suffices for the contrast. Full probability
recovery is unnecessary when that class has multiple components.

For necessity, choose a strictly positive component-mass vector with
sum m_k*d_k=tau; one exists because tau is interior to the coefficient
range. At the transcript generated by that vector, if two unqueried
components have different d values, a small transfer of mass between them
preserves every answer and moves the contrast to either side of tau.
Neither action can then be certified. All unqueried components must belong
to a single equal-coefficient class, giving(C2). This covers adaptive
deterministic choices; the worst input is fixed before that deterministic
algorithm's execution. Randomized expected fees require a separate analysis.
If tau is outside or at an endpoint of the coefficient range, positivity
can already settle the action without any query; do not apply(C2) there.

## Interval reports: a reconstructable decision example

Use three states and the two batches above, with absent offsets and reports

    batch1: v_11 in[19/10,21/10], v_12 in[29/10,31/10],
    batch2: v_22 in[59/10,61/10], v_23 in[99/10,101/10].

Allow s1 in[9,11] and s2 in[19,21]. Put r=p1/p2 and q=p3/p2.
Their extreme ratios give r in[19/31,21/29] and q in[99/61,101/59].
The contrast p3-p1=(q-r)/(1+r+q) decreases with r and increases with q.
The sharp bounds are therefore

    1590/5921 <= p3-p1 <= 670/2027.                           (C3)

At each ratio corner, normalization determines p, and the endpoint reports
determine scales lying within the supplied scale limits; hence both bounds
are attained. In particular p3-p1>1/4 is certified while p remains an interval
family. This is a hand-constructed arithmetic case, not a measured audit or
CPU saving. The general lifted LP should reproduce these bounds exactly.

The persistence premise is essential. Reports from models with unrelated
subjective laws p_g cannot be merged as if they came from one p. Different
populations, changed beliefs or different statewise loss semantics can also
break the bridge. The interval/source warrant must cover the intended common
object. A known cheap currency conversion or a direct task query is a strong
control, not information to hide from the comparison.

### Short certificate for the interval decision

Let L=1590/5921, R=21/29 and Q=99/61. Normalization gives the identity

    (p3-p1)-L = (1+L)*(R*p2-p1)+(1-L)*(p3-Q*p2).

Both coefficients are positive. The first parenthesis is the sum of the
upper bound21*t1/10-p1 and R times the lower bound p2-29*t1/10.
The second is the lower bound p3-99*t2/10 plus Q times the upper bound
61*t2/10-p2. Hence four original interval inequalities and normalization
certify the lower endpoint. No recovered scale, point law or numerical
solver result is needed to check this implication.

For U=670/2027, R0=19/31 and Q0=101/59, the upper certificate is

    U-(p3-p1) = (1+U)*(p1-R0*p2)+(1-U)*(Q0*p2-p3),

using the other four report inequalities. These are ordinary nonnegative
LP-dual combinations. Scale bounds are only needed to confirm the stated
attaining witnesses belong to the narrower input contract, not to establish
these universal inequalities.

The independently enumerated lifted-polytope probe
[calibration_check.py](calibration_check.py) considered all1,365 candidate
bases of its15 inequalities, found16 vertices, checked every vertex against
the original nonlinear report equations and obtained exactly(C3).
[Result](calibration_result.json): Python3.13.14,68,835,700ns measured probe
runtime, one execution. It also checks the offset gauge at two batches with
different nonzero offsets. These are finite development checks, not a full
general checker audit or an economic comparison.

### Close-prior disposition

Ling–Strohmer's self-calibration work explicitly uses inverse gains to turn
bilinear measurements into a linear system. Positive rank-one completion
already uses a connected bipartite observation graph and ratio propagation;
Hendrickx–Olshevsky–Saligrama also study noise and the fragility of small
entries. Credit those mechanisms. Our additional work specifies the common-
probability/interval/offset information class, sharp partial decisions and
the calibration-only fee consequence(C2). Those are a scoped synthesis and
elementary consequences; their moderate novelty/usefulness remains unassessed.
Do not promote merely because the formulas and finite checks pass.
