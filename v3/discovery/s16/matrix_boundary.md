# Complete the eigenvalue-one boundary of the matrix receipt

Codex (GPT-6), October 23, 2026. DEVELOPMENT; extension of the same-model
matrix-envelope derivation, not independent verification.

Finite old operators imply C>0, but C may have eigenvalue1. Decompose
C=I on E1 and C=C0 on its orthogonal complement, where0<C0<I, and write
c=(c1,c0), r=||c1||^2. A compatible full S must satisfy S*W_E1=W_E1:
the positive operator I-S has zero quadratic form on those directions.
Equivalently M^T W_E1=0. This is genuine information about the old source.

The certificate inequalities already cover this boundary. For sharpness,
the interior upper/lower constructions use the canonical rectangular source
M=(0; (C0^(-1)-I)^(1/2)), with zero columns appended if needed. The map
from z to primal x is invertible on the C0 directions; the null directions
contribute their known residual. The earlier gradient/least-squares
stationarity proof therefore goes through after this restriction.

For the finite boundary parameter t0, use I on E1 and dilate only C0 by
the earlier two-by-two contraction construction. Its target second moment
varies from m0=c^T C^2c to s=c^T Cc as before. This avoids the singular
zero block that would result from blindly dilating the eigenvalue-one part.
The upper trivial-value1 endpoint also works with the same rank-one
cancellation N=M-v*(M^T v)^T whenever ||M^T v||<=e.

## A new lower endpoint at parameter infinity

In the common t parameter from operator_receipt.md,

    lim_(t->infinity) c^T L_t(C)c = r/(1+E), E=e^2>0.

Unlike the strict C<I case, this limit can maximize the lower envelope.
Put H0=c0^T C0*(I-C0)^(-1)c0. The first-order expansion is

    c^T L_t(C)c = r/(1+E)
                 +[H0-r*E/(1+E)^2]/t+O(1/t^2).

If a global maximum lies at infinity, necessarily

    H0<=r*E/(1+E)^2.                                  (1)

Conversely, under(1), a finite source/edit attains the limiting lower
value. Use the canonical M above with an additional zero column. Let
w=(c1/(1+E),0), so M^T w=0. Find a unit vector u satisfying

    M*u=(1+E)*c0/(e*sqrt(r)).

Its minimum-norm solution has squared norm (1+E)^2*H0/(E*r)<=1;
the extra zero column fills the remaining norm. Set
N=M+e*(w/||w||)*u^T. Then

    (I+NN^T)w=v,  ||N-M||op=e,
    F(N;v)=v^T w=r/(1+E).

Thus(1) is sufficient too: no larger universally valid lower bound can
hold, and the limit is attained by a finite matrix. If r=0, the strict
case applies and this infinity endpoint is not maximizing. If c0=0,
the construction uses just a zero source column and yields1/(1+E).

## Exact illustrative boundary witness

Take C=diag(1,1/2), M=diag(0,1), v=(3,1)/sqrt(10), e=1, and

    N=[[sqrt(5)/3, 2/3], [0,1]].

The edit is a unit row, so its operator norm is1. For
w=(3/(2*sqrt(10)),0), direct multiplication gives(I+NN^T)w=v.
Hence the edited value is9/20. Here r=.9,H0=.1 and
r*E/(1+E)^2=.225, so the parameter-infinity lower envelope is exactly.45.
This is a finite matching construction, not a numerical limiting plot.

Together these cases extend the proposed sharp directional envelope to
every finite positive compression0<C<=I, when source/output dimensions
and spare zero columns may vary. Fixed-dimension/source-rank constraints
can exclude witnesses and require a different sharpness claim. The
underlying certificate remains valid in those restricted settings.
