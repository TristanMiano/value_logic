# Snapshot/grid mathematical review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
P3-08 **DEVELOPMENT**, independent delegated reconstruction; no added
principal-clock credit. Source hashes and finite checks are retained in
[`run_v1`](run_v1/manifest_before.json).

## Disposition

**The mathematical composition is valid under the stated owned-source,
predictability, fair-bit, and all-path completion assumptions.** Two review
points were sent to the principal and addressed: hard-disabled episodes must
have both masks zero even though the report can read past purchased receipts;
and a coverage-bearing choice of basis/radius rule must precede inspection
of episode outcomes, not merely precede the retrospective report call. The
updated note explicitly labels the same-sealed-trace comparison retrospective
DEVELOPMENT with no prospective coverage claim.

## Shared residual and monotone masks

For fixed block-entry information, let a=(1-H0)/2,
r=(1-H0)(d-1/2), and v=(1-H0)q(1-q). The snapshot loss probability is a+r
and its Brier loss is a+r-v. Subtracting the declared centers gives, directly,

```math
V_s-U_s=F_s-A_s
=\sum_k\left(\sum_t r_{kt}-r_{kJ_k}/\pi_{kJ_k}\right).
```

The selected position appears in the all-round Brier public term but is
excluded from the terminal-error public term. In particular, the first
term of U_s is the actual sum of a over unselected positions; replacing it
by an unconditional expected number of unknown positions would be wrong.

Conditional on the past, q, H0, and the actual pi are fixed. The answers are
mathematically fixed by the exogenous source, whether or not purchased.
Therefore the pi-weighted mean of each displayed block residual is zero.
Each r/pi lies in [-C_s/2,C_s/2], with
C_s=max((1-H0)|1-2q|/pi), so the residual range width is at most C_s.
Coordinatewise masking proves C_s<=C_base and hence Q_s<=Q_base for the
same executed policy and actual probabilities. This does not order centers
or complete interval endpoints.

The owned successful hard epoch starts empty, has no eviction, admits sound
matching receipts, and stops on withdrawal/conflict/capacity failure. Thus a
hard answer at block entry remains available at each later issuance in that
block: H0<=H1. H0 must use only earlier-block receipts; a current-block
receipt can justify H1 only at subsequent positions. Hard-off policy mode
sets both masks zero. Final-cache knowledge alone cannot be used as H0.

On H0=H1 the snapshot/live outputs agree. On H0=0,H1=1, the removed Brier
loss is (q-y)^2 and the removed unselected error mean is d. Summation proves
F_live=F_s-Delta_new_F and V_live=V_s-Delta_new_V. Translating both centers
by these exact observable differences preserves precisely the same residual.
No conditional-mean argument is applied to the live mask.

## Rate-grid allocation and terminal event

The finite rate family depends only on B, m, and selector type. Deduplication
of the original fixed rate is performed before setting J. For each sign and
each fixed R, the inherited conditional exponential process gives failure
at most exp(-c) for radius Q_s/R+cR/8, with lambda=8/R.

Because c=ceil(log2(80J)), one has 2^c>=80J; e>2 then yields
exp(-c)<=1/(80J). A union bound over the two signs and all J rates costs at
most 1/40. On that one event every rate works, so the minimum radius is
valid even though the minimizing rate depends on observed Q_s. F and V
share the residual and need no extra allocation between them. The grid does
not allocate error across base/snapshot bases, fixed/grid constructions,
several policies, or a post hoc favorable choice among those objects.

Conditional on the full action-independent selection and hard history,
only n_live unselected, still-unknown draws can err. For
r_action=ceil(sqrt(ceil(5*n_live/2))), each sign has probability at most
exp(-2*r_action^2/n_live)<=exp(-5)<1/80 when n_live>0. Their sum is at most
1/40; when n_live=0 the action statement is exact. Integrating over history
and combining with the common sampling event gives the stated fixed-end
19/20 joint event for F, V, and Z. No action anytime statement is supplied.
If n_live=0, all issued Brier losses are also observable and the exact-point
exception remains valid.

## Finite arithmetic bound

Every admitted public contract was checked: **16,368** (T,B,selector)
combinations, with D=2^32 providing the monotone maximum in precision. The
maximum grid size is **9**, c is at most **10**, and the maximum grid rate
is **8192**. These counts are finite contract bounds, not coverage tests.

A symbolic bound also suffices. Since T=mB<=8192 and S<=2B,

```math
R_*<2\sqrt{2TB}+2B\le10240.
```

The largest geometric rate is less than 2R_*, hence below 2^15. With
W=D^2 M^2<2^86, the width numerator is below 2^54 and Q's numerator below
2^121 using the note's loose m<2^13. A candidate radius pair has numerator
N_R=8Q_num+cR^2W<2^125 and denominator D_R=8RW<2^104. Comparing two such
pairs by cross multiplication therefore has a pre-operation bit bound at
most **229**, below 256. The exhaustive public-contract upper-bound scan
improves the maximum to **215 bits**. Masking cannot increase these bounds.
Other center/correction operations remain within the earlier coarse envelope.

The implementation still needs to price grid creation, exact comparisons,
snapshot reconstruction, retained state, and output; the mathematical bound
alone does not certify a code-specific tariff. The large existing completion
cap looks sufficient, but the implemented source/cost review remains separate.

## Finite algebra evidence and limits

The independent checker used supplied hypothetical B=2 binary vectors and
q in {0,1/4,1/2,3/4,1}. All **5,400** monotone-mask translation cases and
**1,200** fixed-H0 conditional-mean/range cases passed exactly with Fraction
arithmetic. It imported no production calculator or truth service and read
no main private score. The symbolic argument above supplies generality;
these finite checks only verify the enumerated algebra.

The extension is a finite paid composition of the accepted sampling and
hard-answer interfaces. It establishes no universal endpoint improvement,
new generic concentration method, or economic advantage over an ordinary
implementation of the same report.
