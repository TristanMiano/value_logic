# Scalar model correction from a certified derivative image

Codex (GPT-6), October 23, 2026. DEVELOPMENT; same-model derivation.
This is an early constructive screen, not a novelty or performance claim.

Let a true scalar polynomial A and a cheap scalar model B on R^m have
residual h=A-B of total degree at most P>=1. An exact value/gradient oracle
and the degree promise are separately warranted and priced. Let

    V = span{grad h(x): x in R^m},  dim V=d.

The s15 polynomial-range rules apply to grad h, whose degree is at most
D=P-1. Thus random exact gradient differences can certify a retained space
U=V on one common event. For example, a fixed finite grid of q>D scalars
gives conditional membership probability at most D/q while the retained
space is incomplete. The inherited sequential test must keep each question
frozen at its sample time; no later-span relabelling or free rank premise.

## Exact reduction to d input coordinates

Write U also for an m-by-d full-column-rank basis, put W=U^T, and choose
any right inverse Q of W. Then WQ=I_d. For every x,

    z=x-QWx lies in ker W, and grad h(y)^T z=0 for every y.

The function t -> h(QWx+t*z) has derivative zero, so

    h(x)=g(Wx),  g(y)=h(Qy),  deg g<=P.                (1)

The case d=0 means h is a constant, which still needs one value or an
independent normalization. A gradient certificate alone cannot determine it.
The representation does not need an orthonormal basis or unit-cost square
roots: rational U permits rational row elimination for a right inverse Q.

This d is the least possible number of linear input coordinates. If
h(x)=g0(Cx) with rank C=k, the chain rule gives grad h(x) in range C^T,
hence d<=k. Formula (1) attains d. This is an exact ridge/essential-variable
statement; those established subjects are the immediate prior-art screen.

The argument extends algebraically to a field of characteristic zero or
characteristic greater than P. After an invertible linear change of variables,
all derivatives in the inactive coordinates vanish; every coefficient with
a positive inactive exponent must therefore vanish. Merely assuming field
size q>P is insufficient in small characteristic: h(x)=x^p over an extension
of F_p is nonconstant and has zero formal derivative. Do not import the
gradient-to-value implication from the range theorem without this premise.

## Acquisition after the image is known

There are N_d=binomial(d+P,P) coefficients in a general degree-P polynomial
on d variables. Query g on a fixed unisolvent set, such as integer nodes
alpha>=0 with sum alpha<=P, using x=Q*alpha. Newton interpolation determines
g exactly. Every future adaptive value is then A(x)=B(x)+g(Wx), with no
further true-value queries, on the original common event. Matrix products,
interpolation, model evaluation, storage and exact coefficient bit lengths
remain paid. The finite unisolvent set is available over the stated fields;
point/domain restrictions can invalidate this particular acquisition plan.

If s gradient probes were purchased, the oracle component is

    s*c_gradient + N_d*c_value.

The comparison to full ambient polynomial interpolation has N_m=
binomial(m+P,P) value queries, but is not the strongest ordinary comparator:
ordinary essential-variable reduction can perform the same construction.
If a public symbolic expression already exposes h, direct algebra may win.
If only function values are available, exact coordinate differentiation of
a degree-P polynomial can be built from at most m*P+1 evaluations per point;
that cost must replace the gradient-oracle price rather than be hidden.

The possible useful synthesis is an economical correction to a high-dimensional
model whose *residual* has few essential variables. A may depend on every input
even when h does not. The structural role of fallibility is different from
estimating the model's frequency of correct answers, but ordinary reduction
theory expresses it too. The generic ridge mechanism is not presumed novel.

## Changes and limitations

If an edited model changes the residual by a proved ridge term with gradient
image in T, the new image is contained in U+T on the old common event. That
algebraic extension spends no new statistical failure probability. Finding
a smaller new image from fresh random tests does require a valid additional
event or shared process. The true function's edit must have its own warrant.

Approximate gradient membership yields approximate values only with a path
length/domain premise. If ||(I-P_U)grad h||<=epsilon throughout every segment
from P_U x to x, then |h(x)-h(P_U x)|<=epsilon*||(I-P_U)x||. Sparse samples do
not by themselves provide that uniform derivative bound. An unbounded domain
can erase any uniform value guarantee. These simple screens should precede
an expensive numerical harness.

Primary comparison now rejects generic novelty: Carlini's essential-variable
characterization and Constantine et al.'s gradient-nullspace theorem already
supply the core reduction. See [read scopes](literature.md). Applying it to
the model residual and attaching a sequential finite-degree certificate is
a possible service composition, not yet an established moderate contribution.
No large benchmark is warranted before a useful access regime is identified.
