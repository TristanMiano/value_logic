# Shared-source contrast: sharpness need not mean finite attainment

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; separate extension of
[the exact relative diameter](pair_radius.md), not N16-C/v1's event.
This also explains why finite attainment in the original claim is a
substantive duty beyond an exact closed SDP formulation.

Fix e>0 and its scalar extremizer a and coefficient g(e) from pair_radius.md.
Put lambda_star=1/(1+a^2). Suppose

    0<C<lambda_star I, W^T W=I, W^T S_M W=C.

For every unit c, the exact supremum over compatible finite sources M
and two edits of norm at most e is

    sup [F(N_0;Wc)-F(N_1;Wc)] = g(e)c^T Cc.           (B1)

No finite compatible source/edit pair attains it. The same finite sequence
approaches the whole matrix g(e)C, so this is also a sharp common matrix
upper bound in this regime. It does not assert the formula for arbitrary C.

## Explicit finite sequence preserving every entry of C

Choose 0<delta<lambda_min(C), let

    A_delta=(C-delta I)/(lambda_star-delta),
    P_delta=[[A_delta,sqrt(A_delta(I-A_delta))],
             [sqrt(A_delta(I-A_delta)),I-A_delta]],
    S_delta=delta I+(lambda_star-delta)P_delta,
    W=[I;0].

Since 0<A_delta<I, direct multiplication gives P_delta^2=P_delta.
The spectrum of S_delta is exactly {delta,lambda_star}, both strictly
between zero and one. Its compression is C. Define

    L_delta=sqrt(1/delta-1),
    M_delta=a P_delta+L_delta(I-P_delta),
    N_0=M_delta-e P_delta, N_1=M_delta+e P_delta.

These are finite 2k-by-2k matrices. Each edit has norm e, and M_delta
has resolvent S_delta. On range(I-P_delta) the two edited matrices
coincide, whereas on range(P_delta) their values differ by
lambda_star*g(e). Consequently the exact compressed contrast is

    W^T(S_N0-S_N1)W
       =lambda_star*g(e)(C-delta I)/(lambda_star-delta).

It increases to g(e)C in matrix order as delta decreases to zero.
For a unit target with s=c^T Cc its positive gap is exactly

    g(e)s-contrast
      =g(e)delta(lambda_star-s)/(lambda_star-delta).   (B2)

This proves sharpness using genuine finite sources, while displaying the
unbounded source norm required by this particular approaching sequence.
The universal upper bound follows from pair_radius.md. No Gram closure or
minimax assertion is required for B1.

## Why equality is impossible in this regime

In the proof of the universal bound, R(lambda) has its unique maximum g(e)
at lambda_star. Thus

    g(e)S_M-[U_t(S_M)-L_u(S_M)]

is positive semidefinite, with kernel exactly the lambda_star eigenspace
of S_M, since S_M is strictly positive for every finite M. If the final
scalar contrast equalled g(e)s, equality throughout the bounding chain
would force S_M Wc=lambda_star Wc. Compressing gives
C c=lambda_star c, contradicting C<lambda_star I.

For C<=lambda_star I the construction also works with eigenvalues at
lambda_star. Equality for a particular c can occur only on its
lambda_star eigenspace, and the canonical scalar action there attains it.
The strict regime above avoids needing any claim about other directions.

At e=1, lambda_star is about0.287. Thus the existing C=0.1 scalar screen
and C=diag(0.1,0.2) block screen are in this regime. Their exact suprema
are g(1) times the old target value, explaining the numerical SDP results
and their near-attaining finite witnesses. This is a statement about their
information class, not a numerical solver's ability to prove attainment.

## Broader condition screened but not included in B1

An attempted extension replaces C<=lambda_star I by the directional
condition

    c^T C(I-C)^(-1)c <= (c^T Cc)/(1-lambda_star).       (B3)

The derivation considers a limiting spectral measure supported, on the
target, at zero and lambda_star. With s=c^T Cc<lambda_star, its minimum
possible compressed weights are

    A_1=(Cc)(Cc)^T/(lambda_star*s),
    A_0=(lambda_star*c-Cc)(lambda_star*c-Cc)^T
          /[lambda_star*(lambda_star-s)].

Both are forced lower bounds by the PSD Cauchy-Schwarz inequality. To
complete the remaining measure in [0,1], one needs

    0<=C-lambda_star*A_1<=I-A_0-A_1.

A two-by-two Schur reduction suggests its upper inequality is equivalent
to B3; it also implies c^T C^2c<=lambda_star*s. This is a promising
moment-completion route, but its complete necessity/limiting realization
argument has not been reconstructed here. It is not part of the proven
development claim B1, no readiness estimate is attached, and no numerical
success is substituted for that missing argument.

Later s17 development: [pair_criterion.md](pair_criterion.md) supplies the
missing necessity and finite limiting construction for B3, using a
second-moment obstruction and one added output. This supersedes the
screened-only status above while preserving the earlier partial argument.
It remains a separate DEVELOPMENT result with novelty unassessed.
