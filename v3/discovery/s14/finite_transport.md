# Sharp finite-distance transport of a scalar response

Later same-session strengthening: finite_extremizers.md gives finite rank-one
attainment of both linear branches. The diagonal limits below remain valid
examples, but a limit is not necessary for the one-scalar theorem.

Codex (GPT-6), DEVELOPMENT, October22,2026. Derived after the differential
adapter in receipt_transport.md. The proof uses standard Young, inverse
Loewner and scalar Jensen inequalities; closest-prior novelty remains open.

Let v be a unit real vector, M,N rectangular matrices of the same shape,
||N-M||op<=e, and g(M)=v^T(I+MM^T)^(-1)v=s. No access to the entries of M
is needed to USE this rule, but the structural distance warrant is a paid
input. The theorem permits arbitrary finite dimensions; sharpness below is
over that class, with dimension two enough for limiting examples.

Put a=(sqrt(e^2+4)+e)/2, so a-1/a=e, a>=1, and

    s_plus=a^2/(1+a^2), s_minus=1/(1+a^2).

The sharp lower envelope, understood as an infimum where necessary, is

    L_e(s)=s/a^2,                                      0<=s<=s_plus;
           1/[1+(sqrt((1-s)/s)+e)^2],                 s_plus<=s<=1.

Its associated sharp upper envelope is

    U_e(s)=a^2*s,                                      0<=s<=s_minus;
           1/[1+max(0,sqrt((1-s)/s)-e)^2],             s_minus<=s<=1.

Both are increasing and join continuously. At e=0 they equal s. Endpoints
at s=0 use closure; every actual finite M has s>0. The upper envelope becomes
one when s>=1/(1+e^2). Thus a partial truthful receipt [l,u] transports to
[L_e(l),U_e(u)]. Scalar interval information and this distance premise alone
cannot uniformly tighten either endpoint over arbitrary finite dimensions.

## Lower bound

Write R=(I+MM^T)^(-1), and choose h>0. Matrix Young gives

    I+NN^T <= (1+h)(I+MM^T)+d I,
    d=(1+1/h)e^2-h.

This follows by expanding N=M+(N-M), applying
MD^T+DM^T<=h MM^T+D D^T/h, and D D^T<=e^2 I.
Take h>=e*a. Then d<=0, while c=1+h>0 and c+d>0.
Inverse order and the spectral theorem imply

    g(N)>=v^T R(cI+dR)^(-1)v >= s/(c+d*s).

The second inequality is scalar Jensen for x/(c+d*x), convex on[0,1]
when d<=0. The denominator is

    1+h(1-s)+e^2*s+e^2*s/h.

Its minimum on h>=e*a occurs at h=e*a if s<=s_plus, and otherwise at
h=e*sqrt(s/(1-s)). These give the two displayed branches. Cases e=0 and
s=1 follow directly or by limits. In particular s=1 yields1/(1+e^2).

## Sharpness and upper bound

For s>=s_plus use scalar M=sqrt((1-s)/s), N=M+e and v=1.
For 0<s<s_plus, take

    M=diag(1/a,K), N=diag(a,K),
    v=(sqrt(w),sqrt(1-w)),
    w=(s-1/(1+K^2))/(s_plus-1/(1+K^2)).

For sufficiently large K, w lies in[0,1] and g(M)=s exactly. As K grows,
g(N) tends to s/a^2. The matrices differ in operator norm exactly e.
Except at the branch join, this construction establishes an infimum, not
attainment by a finite K. A scalar-only interface has a narrower envelope;
the dimensional quantifier must remain explicit.

The same lower bound with M,N exchanged gives s>=L_e(g(N)). Invert this
increasing function on its range, with cap one, to obtain U_e. The reversed
sharpness examples establish its supremum. If s>=1/(1+e^2), take scalar
M=sqrt((1-s)/s), N=0, whose distance is at most e, to attain the cap one.

## Practical comparison and verification duty

The global ratio bound alone is

    a^(-2)*g(M)<=g(N)<=a^2*g(M),
    |log g(N)-log g(M)|<=2 asinh(e/2).

This is sharper than integrating the uniform log-derivative bound e.
The nonlinear branches use the known scalar value and improve the ratio
bound near one. Compare the exact envelope to the earlier Phi transport,
global additive Lipschitz band and direct recomputation under identical
access. No CPU saving is implied by the formula.

For the original response y_U(t), substitute e=sqrt(t)*epsilon with the
validated ||A^(-1/2)(U'-U)||op bound epsilon. Normalize by the same exact
baseline y0. Uncertainty in y0 requires additional accounting. Directly
bounding an accumulated edit from the receipt origin is preferable when
available; sequential application remains sound but can lose information.

Prospective cheap screen: exact rational inverses for small noncommuting
matrices with independently constructed rank-one norm-bounded edits; scalar
equality cases; limiting two-dimensional sharpness; comparisons with the
earlier sound adapters. This does not replace the dimension-free argument.

Executed transport_probe.py/json: PASS, 1,080 rational matrix panels and
2,160 exactly checked one-sided inequalities,66 exact scalar equalities,
five decreasing limiting-gap sequences, and6,000 floating-point comparisons
with earlier adapters (maximum discrepancy2.23e-16). Runtime150,871,300ns.
Source SHA25693a9c783ed89126a0076f9f505b648307c914fdff3b01e259890f66695385518.
For s=0.1 and e=2, the sharp band is approximately[0.0171573,0.582843],
versus[0.0135335,0.729174] from Phi transport and[0,1] from the additive rule.
This is an information guarantee under the same mathematical premises,
not a measured fee saving or independent confirmation.
