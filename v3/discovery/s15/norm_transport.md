# One-receipt transport for norm-based regularized loss

Codex (GPT-6), October 23, 2026. DEVELOPMENT; same-model derivation.
This generalizes the s14 squared-loss contract. Priority and independent
reconstruction remain open. It does not claim a new duality principle.

Let X,Y be finite-dimensional real normed spaces, p in (1,infinity),
q=p/(p-1), and ||v||_Y=1. For a linear map M:X->Y define

    F_p(M;v) = min_x (||v-Mx||_Y^p + ||x||_X^p).

The minimum exists by coercivity and its value s lies in (0,1]. Suppose
||N-M||_(X->Y)<=e. Only s, p and this paid norm warrant are retained.
No inner product or smoothness of the underlying norms is assumed.

For e>0 let t_* be the unique positive solution of

    t_*^(-(q-1)) - (t_*+e)^(-(q-1)) = e.

The left side decreases continuously from infinity to zero. Define

    ell(t) = (1+t^q)^(1-p),
    R = ((1+(t_*+e)^q)/(1+t_*^q))^(p-1) = (t_*+e)/t_*,
    a = ell(t_*), b = ell(t_*+e) = a/R,
    t(s) = (s^(-1/(p-1))-1)^(1/q).

Candidate sharp dimension-unrestricted envelopes are

    L(s) = s/R                         if 0<s<=a,
           ell(t(s)+e)                 if a<=s<=1;

    U(s) = R*s                         if 0<s<=b,
           ell(max(t(s)-e,0))          if b<=s<=1.

For e=0 both equal s. Thus a truthful interval [l,u] transports to
[L(l),U(u)] using monotonicity. Closure handles l=0; no finite M with
unit v has value zero. Norms, normalization and the edit warrant are
premises, not free information inferred from the scalar.

## Lower bound from an old optimality certificate

Choose an old minimizer x, r=v-Mx, alpha=||r||, beta=||x||. Convex
subgradient optimality supplies w in Y* and z in X* satisfying

    M* w=z, ||w||=alpha^(p-1), <w,r>=alpha^p,
    ||z||=beta^(p-1), <z,x>=beta^p.

Factors p cancel. The norm-power subgradient rule also applies at zero.
Here alpha cannot be zero: it would force w=z=x=0 and then v=0.
Consequently

    <w,v>=s=alpha^p+beta^p <= alpha^(p-1),
    k=beta^(p-1)/alpha^(p-1),
    0<=k<=t(s).

For any u and any dual vector w, Holder on the product space gives

    <w,v> <= ||w|| ||v-Nu|| + ||N*w|| ||u||
            <= (||w||^q+||N*w||^q)^(1/q)
               (||v-Nu||^p+||u||^p)^(1/p).

Use the old w and ||N*w||<=beta^(p-1)+e*alpha^(p-1), then minimize u:

    F_p(N;v) >= s * [(1+k^q)/(1+(k+e)^q)]^(p-1).       (1)

The ratio C(t)=[(1+(t+e)^q)/(1+t^q)]^(p-1) increases up to t_* and
decreases thereafter. Its logarithmic derivative has the sign of

    t^(-(q-1))-(t+e)^(-(q-1))-e.

Thus maximize C over [0,t(s)] at min(t_*,t(s)). This gives L(s).
The stationarity equation gives the displayed simpler formula for R.
The joined branches of L are increasing. Exchanging M,N and inverting
L gives U, with the trivial value cap one.

The unconstrained ratio R is also the p-th power of the induced norm of
the two-dimensional shear (a,b)->(a+e*b,b) on l_p. This relates the
construction to ordinary product-space geometry; it is not its novelty.

## Sharpness with explicit small examples

For scalar X=Y=R and M=t>=0, direct minimization gives F_p(M;1)=ell(t).
Consequently the nonlinear lower branch is attained by M=t(s), N=M+e.
The nonlinear upper branch below the cap uses M=t(s), N=M-e; at the cap
use N=0, permitted whenever t(s)<=e.

For 0<s<a use X=Y=l_p^2, M=diag(t_*,K), N=diag(t_*+e,K). Their induced
operator distance is e. Choose

    w_K=(s-ell(K))/(a-ell(K)),
    v=(w_K^(1/p),(1-w_K)^(1/p)).

For sufficiently large K, w_K lies in [0,1], ||v||_p=1 and F_p(M;v)=s
exactly. Separability gives F_p(N;v)->s/R. Reversing this construction
proves sharpness of the linear upper branch. These are limiting witnesses;
no general finite-attainment classification is asserted. The stronger
finite p=2 classification in s14 remains a separate inherited result.

## What this changes and what it does not establish

The receipt service can now address nonsquared residual and regularization
costs, with a matching scalar rule for each declared p and norm contract.
One need not retain the matrix or old minimizer to apply the envelope.
For p=2 and Euclidean norms it recovers the s14 one-scalar formula exactly.
For p=2 with other norms it supplies the same sharp unrestricted envelope,
although individual fixed spaces may allow stronger bounds.

This is a capability/formal-extension claim, not a CPU or acquisition
saving. Norm-duality, graph distances and shear norms are conventional;
the exact receipt-conditioned piecewise envelope needs a close literature
comparison. A general result already covering this contract would absorb
the proposed mathematical delta. Endpoint p=1/infinity, vector-valued
receipts and two-receipt sharpness are not included in the present claim.

Cheap next screen: evaluate scalar equalities and l_p diagonal mixtures
for a few nonquadratic p, then use small nonsymmetric matrices with a
convex primal/dual check. Do not use an uncertified optimizer output as
proof of the envelope or broaden a finite check into general confirmation.

Executed norm_probe.py: PASS for 120 scalar equality checks, 45 diagonal
mixture checks, and 20 nonsymmetric primal-dual cases at p=4/3,3/2,2,3,4.
The largest reported numerical primal-dual gap is below 4.79e-11.
These are floating developmental checks, not outward certificates or
independent verification. Source/output hashes and measured runtime are
stored in norm_probe.json; the original outputs remain unchanged.
