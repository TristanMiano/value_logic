# Let a fallible model propose an old-value query

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass57.
This uses the established variational inverse identity. The possible useful
adapter is task-directed scalar acquisition, not new duality or a new
generic learned-certificate principle.

Let C=W^T(I+M M^T)^-1 W, W^T W=I, and c be the current target coordinates.
Suppose ||N-M||_op^2<=E. Choose t>0 with t^2>=E*(1+t), put a=1+t and
d=t-E-E/t. First assume d>0. For ANY proposed vector z, acquire a truthful
interval[l_z,u_z] for the old quadratic value q_z=z^T C z. Then

    c^T W^T(I+N N^T)^-1 W c
       <= a*u_z + (a/d)*||c-z||^2,                 (1)
       >= a*l_z - ||c-a*z||^2/d.                  (2)

Intersect the final scalar interval with[0,||c||^2]. Different z and t may
be used for the two sides. No accuracy or structural assumption on the
proposing model is a validity premise. The exact target vector Wz, source
identity, normalization, interval warrant and edit bound are actual inputs.

Proof: operator_receipt.md gives U_t(C)=a*C*(I+d*C)^-1 and
L_t(C)=C*(a*I-d*C)^-1. The inverse variational inequality

    c^T A^-1 c >= 2*c^T z-z^T A z

implies c^T U_t(C)c <= a*q_z+(a/d)*||c-z||^2 and
c^T L_t(C)c >= a*q_z-||c-a*z||^2/d. The signs are opposite because
U_t=(a/d)*(I-(I+d*C)^-1), whereas
L_t=(a/d)*(a*I-d*C)^-1-I/d. The interval endpoints then prove(1)–(2).
When d=0, use the direct old-target bounds q_c/a and a*q_c instead.

## Tightness depends on the proposal, not validity

The upper optimum is z_U=(I+d*C)^-1 c; its exact excess is

    bound_U-c^T U_t(C)c
       =(a/d)*(z-z_U)^T*(I+d*C)*(z-z_U).

The lower optimum is z_L=(a*I-d*C)^-1 c; its exact deficit is

    c^T L_t(C)c-bound_L
       =(a/d)*(z-z_L)^T*(a*I-d*C)*(z-z_L).

These identities concern exact q_z. An interval adds a times the respective
one-sided query error. A fallible approximate block can propose the inverse
directions; if the proposal is poor, the certificate becomes weak and may
return unresolved. At the optimal directions, one old scalar value per side
recovers the corresponding whole-block certificate for THIS target and t.

This makes two selected scalar queries an alternative to learning all
k*(k+1)/2 entries of C when the task and edit budget are already known.
It is a different retention duty: the full block supports every later c,
while these two witnesses need not. Acquiring an additional original-target
value or a library for many tasks must be charged, not omitted from the count.
The proposed z vectors cost O(k) scalars each; an arbitrary dense W still
costs O(nk) unless it is already available or implicitly specified.

## Later use and a fair comparison

A stored pair(z,[l_z,u_z]) can be used at any later valid t and target c
by(1)–(2). A finite library may minimize upper and maximize lower bounds;
all are pointwise consequences of truthful receipts, so this deterministic
selection spends no extra statistical confidence. If value intervals come
from randomized acquisition, their actual joint/adaptive coverage contract
must be supplied separately.

The old source must be queryable at acquisition time. This does not restore
a discarded matrix, make an old solve free, or imply an old query is cheaper
than evaluating the new source. Direct old solves and their retained vectors,
ordinary variational witnesses, full-block batching and direct contrast
evaluation are strong controls. The calculation is a concrete connection
between fallible models, paid mathematical questions and counterfactual
decisions; economics and the exact literature delta remain unassessed.

The exact query_probe.py example uses target(3/5,4/5), true C=diag(.1,.9)
and a deliberately imperfect forecast[[.12,.03],[.03,.85]]. Two old-value
queries with outward error10^-5 certify[.5672462113,.6546098399], hence
strict separation from thresholds.56 and2/3. The corresponding exact-block
interval at the same t is[.5675860497,.6542871386]. Eighty-one arbitrary
proposal vectors and one explicitly edited source also pass exact checks.
Runtime4306400ns on Python3.12.14; source SHA-256
eacfdef0607c893286570f166be28bbf3e685c49742faccb0497facad247e1d3.
These are finite development results, not measured source-query prices.
