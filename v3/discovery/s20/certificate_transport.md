# Reusing a range certificate after a bounded model change

Codex (GPT-6), October 28, 2026. Separate DEVELOPMENT extension, outside
the frozen V19-R/v1 contribution event and its P3-11-A1 assessment.

The local ingredient is established safe LP bounding from dual residuals,
not a new sensitivity theorem. The proposed use is to retain a sound union
of intervals, and therefore a useful excluded report band, after changing
the premises. It deliberately gives up exact attainment until the changed
problem is solved again. This is different from the exact receipt repair
radius already derived in [s19](../s19/repair_radius.md).

## One changed local slice

Write the new slice as A'x <= b', with readout c'x+d'. Require a known
finite box l <= x <= u for every feasible new point. The box must follow
from the new premises; a guessed old solution bound is insufficient.
For any nonnegative vectors y and z of the appropriate row dimension,
define box extrema m(r)=sum_j min(r_j*l_j,r_j*u_j) and
M(r)=sum_j max(r_j*l_j,r_j*u_j). Then every feasible new point satisfies

    d' - y*b' + m(c'+A'^T*y) <= c'*x+d'
                               <= d' + z*b' + M(c'-A'^T*z).       (T1)

Proof: insert and subtract y*A'*x on the left, use y*A'*x<=y*b',
and bound the residual linear form on the box. The upper inequality
uses z*A'*x<=z*b'. Neither vector must be dual feasible for the new
objective; all residual terms are retained. Taking maxima of lower bounds
and minima of upper bounds from a retained bank is also sound.

A nonnegative vector w proves new infeasibility whenever

    m(A'^T*w) > w*b'.                                           (T2)

Indeed every feasible point would satisfy both the reverse weak inequality
and w*A'*x<=w*b'. Failure of this test is inconclusive. In particular, an
old empty slice must not remain omitted merely because it used to be empty.
If its old Farkas vector no longer proves emptiness, retain the entire
new box readout interval, or solve it again. An interval produced by (T1)
also need not be nonempty in reality. Lower > upper proves emptiness;
lower <= upper establishes only an outer enclosure.

## Uniform changes and a report-band persistence radius

For a compact, easily checked perturbation contract, require the same
indexed rows and fixed symmetric coordinate bounds |x_j|<=R_j. Suppose

    |A'-A| <= t*D_A, |b'-b| <= t*D_b,
    |c'-c| <= t*D_c, |d'-d| <= t*D_d, t>=0,

entrywise, with nonnegative declared D's. Fixed physical box constraints
are part of every changed model. Receipt rows include all lower conditions
and the selected upper conditions, just as in the original construction.
An exact old lower/upper certificate y/z gives, uniformly over these edits,

    L(t)=ell - t*beta_y, U(t)=u + t*beta_z,
    beta_y=D_d+y*D_b+sum_j R_j*(D_c[j]+(D_A^T*y)[j]),           (T3)

and similarly for beta_z. This follows directly from (T1), or by bounding
the changed residual coefficient and right-hand side separately. It is
conservative: different perturbations attaining its component bounds need
not occur together.

An old Farkas vector w has w*A=0 and w*b<0. Put

    gamma=w*D_b+sum_j R_j*(D_A^T*w)[j],
    alpha=(-w*b)/gamma, with alpha=+infinity if gamma=0.         (T4)

The slice is still empty for t<alpha. At t=alpha the proof may cease to
exclude it, so include it at that closed boundary. Its fallback enclosure
is [d-sum_j |c_j|R_j-t*sigma, d+sum_j |c_j|R_j+t*sigma], where
sigma=D_d+sum_j R_j*D_c[j]. Thus every slice has one activation time a_s
and one expanding outer interval [l_s-t*p_s,u_s+t*q_s]. Old bounded
slices have a_s=0; old empty slices use (T4) and the box fallback.

For a proposed report band [h,H], define

    up_s = inf{t>=0 : u_s+t*q_s >= h},
    down_s = inf{t>=0 : l_s-t*p_s <= H},
    ordinary_s=max(a_s,up_s), anchor_s=max(ordinary_s,down_s).  (T5)

Each infimum is an exact rational nonnegative quotient, zero if already
satisfied, and infinity if a positive deficit has zero slope. For any
fixed witness partition, its artificial product intervals permit a minimum
in [h,H] iff every upper endpoint reaches h and at least one lower
endpoint reaches H. Therefore its first admission time is the minimum,
over its anchor blocks, of the maximum of anchor_s and every other
ordinary_s. Min-max prefix/suffix subset recurrences give

    t_cert = min_(i,T) max(anchor_(i,T),
                 min_(outside partition of K\T) max_j ordinary_(j,T_j)). (T6)

This takes O(n*3^k) scalar comparisons and O(n*2^k) entries after the
certificate dot products; it needs no new LP. Empty outside collections
have maximum zero. The interval construction and the threshold calculation
are ordinary bottleneck partitioning. All changed models within every
t<t_cert reject [h,H]. At t_cert the *outer approximation* admits the band;
that is not a source witness, proof of achievable model repair, or claim
that the exact changed source became feasible. The guarantee remains
conditional on the supplied coefficient bounds and fixed physical box.

## Relation to existing methods and earlier work

[Guilbeau et al. (2016), sections 1--3.3 and 3.7](https://interval.louisiana.edu/preprints/reformulations-for-rigorous.pdf)
give safe bounds using dual residuals and explicit variable bounds, crediting
Neumaier--Shcherbina (2004). Their cautions about nonexistent optima and
unjustified variable bounds apply directly here. T1/T2 use that established
idea with exact rational arithmetic and our inequality sign convention.
No local LP novelty is claimed.

The repository's earlier exact repair-radius construction pays for new
local LPs and can provide an attaining changed source. This extension
reuses an already paid-for certificate bank and returns only a sufficient
radius. Its possible gain is avoiding new optimization for some questions,
with reduced precision explicitly charged. A conventional implementation
of the same safe bounds and subset recurrence ties it. No measured speedup
or standalone novelty readiness is assigned before a specific check.
