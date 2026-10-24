# N16-C/v1: the bounded contribution event assessed in s17

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; prospective assessment scope.
This pins the [s16 target](../s16/verification_targets.md), rather than adding
all adjacent extensions to its verification event.

## Mathematical object and information contract

Let k be a positive integer, C a real symmetric k by k matrix with
0 < C < I, c a real unit vector, and e > 0. A compatible source is any
finite real n by p matrix M and n by k isometry W satisfying

    S = (I + M M^T)^(-1),  W^T W = I,  W^T S W = C.

Both n >= k and p are unrestricted finite dimensions. For any N of the
same shape as its M, with ||N-M||op <= e, define

    F(N; Wc) = min_x { ||Wc - N x||^2 + ||x||^2 }
             = c^T W^T (I + N N^T)^(-1) W c.

The information available for the bound is C, c and e; M and its full
resolvent or solution vectors need not be retained. W is already specified
or supplied as part of the target interface. Its storage/acquisition is not
silently free. Quantification is over compatible sources AND edits, followed
by reoptimization of x. This is distinct from choosing one robust x before
an edit and from bounds for one completely known M.

Put E=e^2, t0=(E+sqrt(E^2+4E))/2. For t >= t0, define

    a = 1+t,  d = t-E-E/t,
    L_t(C) = C (a I-d C)^(-1),
    U_t(C) = a C (I+d C)^(-1).

The proposed theorem is that the infimum and supremum of F over precisely
this compatibility class equal

    lower(C,c,e) = max_{t >= t0} c^T L_t(C)c,
    upper(C,c,e) = inf_{t >= t0} c^T U_t(C)c,

where t=infinity supplies upper limit 1. Each endpoint is attained by a
finite compatible source and edit (sources may differ between endpoints),
with a proposed witness using n=p <= 2k. The sharpness is scalar for a
declared c. This is not a simultaneous greatest/least matrix envelope.

## Usable consequence and contribution event

The same pointwise inequalities yield sound strict-threshold certificates
from truthful rational brackets 0 < C_minus <= C <= C_plus < I and rational
E,t. Review the existing dimension-1-to-16 exact rational checker under its
actual acceptance contract. The checker does not establish the external
source identity, bracket truth, target isometry or edit warrant. It does not
need to solve the scalar optimization or certify sharpness to be sound.

One exact decision example must exhibit a threshold at which the retained
block certifies a choice that a single old target value cannot certify over
its larger compatibility class. Count the block's extra scalar observations
and precision requirements; include checking and acquisition in any economic
interpretation. This example establishes an information-dependent decision
capability, not an empirical speedup or a universal advantage over ordinary
methods using the same block.

The contribution event is: a rigorous reconstruction supports this exact
sharp-information theorem and its rational decision certificate, and a
close prior-art comparison supports a useful, moderately novel guarantee or
synthesis with an explicit delta beyond a routine restatement of a theorem
already supplying the same information, quantifiers and endpoints. Numerical
readiness must include that novelty/usefulness uncertainty, proof risk and
the relevant checker/interface risk. It is not conditioned on those passing.

Ordinary Young inequalities, inverse compression, rank-one worst residuals,
matrix completion and exact rational linear algebra are credited machinery.
An identical conventional implementation ties. A weak scalar-only comparator
cannot by itself establish a contribution against stronger existing results.

## Separate, nonessential extensions

Fixed n or p; eigenvalues at 0 or 1; sharp average or simultaneous matrix
endpoints; Frobenius/shared edit allocation; randomized threshold economics;
task-directed query refinement; quadratic/nonquadratic solution reuse; and
empirical complete-cost gains are separate targets. None is a prerequisite
or borrowed success metric for this event. If the bounded core is already
routine prior art, revise/park it and use the remaining session on the
strongest alternative. Preserve the original claim and that disposition.
