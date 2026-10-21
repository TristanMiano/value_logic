# Recover joint matrix-edit values from observable one- and two-port probes

Codex (GPT-6), DEVELOPMENT, October21,2026. A restricted counterfactual-value
identification adapter, using Woodbury and low-degree algebra. This is not
general causal identification or a new matrix inverse identity. Its closest
principal-minor/network-identification comparison remains to be checked.

## Known edit semantics and a sufficient observation contract

Let A be an unknown symmetric positive definite matrix, b a fixed vector,
and U a known full-column-rank edit matrix with r columns. The task value is

    y(D)=b^T(A+U D U^T)^(-1)b,

for arbitrary nonnegative diagonal D. Set y0=b^T A^(-1)b,
g=U^T A^(-1)b and V=U^T A^(-1)U. Then V is positive definite and

    y0-y(D)=g^T(D^(-1)+V)^(-1)g

on the positive support of D, with zero coordinates omitted. Suppose every
g_i is nonzero. Simultaneously changing the signs of g_i and row/column i
of V leaves every response invariant because diagonal D commutes with that
sign matrix. Work in the gauge g_i>0 without needing to know physical signs.

For each port i, two distinct positive singleton strengths give

    d_i(t)=y0-y(t e_i e_i^T)=t*g_i^2/(1+t*V_ii).

The reciprocals are affine in1/t, so the two nonzero values identify g_i^2
and V_ii. These are exact-value operations; finite precision is a separate
question. Now each remaining unknown is one off-diagonal v=V_ij, with
|v|<sqrt(V_ii V_jj) by positive definiteness.

Choose a positive common pair strength t small enough that

    t*sqrt(V_ii V_jj) < min(g_i/g_j,g_j/g_i).

A readily checked upper bound on the square root can replace it. For all
admissible v, the vector

    z = [[1/t+V_ii,v],[v,1/t+V_jj]]^(-1) (g_i,g_j)^T

has both entries positive. The pair reduction d_ij(t)=g_pair^T z therefore
has derivative -2*z_i*z_j<0 with respect to v. One exact pair value uniquely
identifies v in its admissible interval; solving its quadratic equation
and selecting the unique admissible root is sufficient.

Thus baseline y0,2r singleton values and r(r-1)/2 pair values identify the
entire multivariate response y(D) for every nonnegative diagonal edit. This
matches the number r+r(r+1)/2 of continuous(g,V) parameters after fixing
the discrete sign gauge, but no general oracle lower bound is inferred just
from that count. Later evaluation uses an r-dimensional linear solve; the
original system dimension need not appear after paid identification.

This differs from numeric_edits.md's2r samples for a *single common-strength*
curve. Independent edit strengths require more information. It also explains
why joint_edit_gap.md used dormant ports: its g has zero entries, so that
construction falls outside this sufficient observation contract.

## Exact observability does not imply an economical noisy measurement

Use the three-port cycle matrices V_plus,V_minus from joint_edit_gap.md,
with diagonal2 and off-diagonal magnitudes1/2. Flip only the2-3 edge in
V_minus. Set g=(1,epsilon,epsilon),epsilon>0, and y0=10; for sufficiently
small epsilon the full inverse block [[y0,g^T],[g,V]] is positive definite.

All singleton responses and the1-2/1-3 pair responses agree between the two
models. For the2-3 pair at common strength t, the difference in reductions
has magnitude

    2*epsilon^2*t * |1/(1+2.5t)-1/(1+1.5t)|
      <= (8/15)*epsilon^2.

At epsilon0, the full three-port t1 reductions differ by1/140, and continuity
preserves a nonzero separation for sufficiently small positive epsilon.
Consequently exact pairwise identification can become arbitrarily ill-
conditioned even though all ports are technically observable. A fixed-noise
value service may fail to distinguish every pair experiment while the joint
counterfactual remains materially different. This is a measurement-precision
obligation, not an excuse to count exact reals as free data.

For inverse M-matrix/electrical-network subclasses, positivity imposes
additional relations between g and V. The near-dormant construction above
need not satisfy them. A quantitative stable boundary for that natural
subclass is a separate promising question, not proved by this adapter.

The positive subclass is developed in weak_ports.md. First ports_probe.py
execution:20 exact rational recovery panels,140 singleton values,100 pair
values and1800 multivariate predictions all matched direct full-system
solves. Sixteen near-dormant pair comparisons obeyed the stated quadratic
bound. At epsilon1/10000 the pair difference is at most1/187500000 while
the unit-strength joint difference is24970009/3500000000, about0.00713.
These are constructed precision requirements, not measured hardware accuracy.

[Brunel/Urschel2024](https://arxiv.org/html/2404.06302v2), introduction,
§5.1 and§5.3, is a close principal-minor recovery comparison, including
quadratic query counts and quantitative separation conditions. Our oracle
returns a scalar resolvent response under diagonal edits, not a freely
chosen principal minor. That interface distinction requires its own exact
reduction; the generic matrix-recovery idea and sign gauge are established.
