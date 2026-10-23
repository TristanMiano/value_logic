# An exact small SDP for a norm-bounded counterfactual

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. This specializes the
established linear-operator interpolation theorem; it is not a new SDP
principle or a claim of an implemented certified solver.

We seek the possible t=v^T(I+NN^T)^(-1)v given unit v, old receipts
s=v^T(I+MM^T)^(-1)v and m=||(I+MM^T)^(-1)v||^2, and bounds
||M||<=K, ||N-M||<=e. Hidden dimensions are unrestricted.

Use two positive-semidefinite Gram matrices: one for row-space vectors
(v,w,u,a), and one for column-space vectors (z,p,c). All expressions
below are linear in their Gram entries. Impose ||v||^2=1, v^T*w=s,
||w||^2=m. Define the following symbolic lists and linear combinations:

    X=[z,p], Y=[v-w,a], U=[w,u], V=[z,c],
    b=v-u-a, d=p-c.

The old operator constraints are

    X^T*V=Y^T*U,
    Y^T*Y <= K^2*X^T*X,
    V^T*V <= K^2*U^T*U,                              (1)

where matrix inequalities are positive-semidefinite order. The edit
constraints are

    p^T*d=b^T*u, ||b||^2<=e^2*||p||^2,
    ||d||^2<=e^2*||u||^2.                            (2)

Minimizing or maximizing the linear objective v^T*u gives the exact
lower or upper endpoint. Interval receipts replace the corresponding
equalities by linear interval inequalities. Additional new moment data
are constraints on ||u||^2. No rank restriction on the Gram matrices is
needed because the hidden dimensions are unrestricted.

## Why it is exact

For actual matrices, set w=(I+MM^T)^(-1)v, z=M^T*w,
u=(I+NN^T)^(-1)v, p=N^T*u, a=M*p and c=M^T*u. With H=N-M,
b=H*p and d=H^T*u, so (1)-(2) are necessary.

Conversely factor the two Gram matrices into actual vectors. Theorem 3.1
of Bousselmi, Hendrickx and Glineur supplies ONE operator M of norm at
most K with M*z=v-w, M*p=a, M^T*w=z, M^T*u=c. The same theorem applied
to the singleton lists in (2) supplies an operator H of norm at most e
with H*p=b and H^T*u=d, on the SAME realized vector spaces. Define N=M+H.
Then w+MM^T*w=v and u+NN^T*u=v. This proves sufficiency, including
degenerate Gram matrices. Independently interpolating M and N without
binding their difference would not prove this statement.

The ordinary source is *Interpolation Conditions for Linear Operators
and Applications to Performance Estimation Problems*, SIAM J. Optim.
34(3), 3033-3063 (2024), https://arxiv.org/pdf/2302.08781, Theorem 3.1.
The theorem is imported; its full appendix construction has not been
independently reconstructed here. The main-text statement and proof route
were read. Its Theorem 3.6 also supplies an uncapped-operator formulation
with auxiliary block LMIs. We do not implement that extension here.

## Shared counterfactuals

For several alternatives N_i=M+H_i, introduce (u_i,p_i,a_i,c_i), include
all p_i/u_i in M's lists, and apply (2) to each edit. This binds the
alternatives to a common old model. For a single shared edit with
N_i=M+tau_i*H and fixed nonzero tau_i, interpolate ONE H on all pairs
(p_i,(v-u_i-a_i)/tau_i) and (u_i,(p_i-c_i)/tau_i). Its cross-list
equalities and LMIs retain the shared edit information. Separately
bounding the alternatives discards it. Linear combinations of their
value receipts then remain linear SDP objectives.

This is an explicit conventional interpolation adapter for receipt-limited
decisions. It can handle noncommuting edits and partial joint information.
Solving the SDP, checking a dual certificate, acquiring receipts and
certifying the norm bounds are all paid work. Floating-point solver
output alone would not be a rigorous outward bound. No complete-cost
benefit or novelty conclusion is drawn from this formulation.
