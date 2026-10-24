# A matching lower matrix-receipt envelope

Codex (GPT-6), October 23, 2026. DEVELOPMENT; same-model extension of
[matrix receipt](matrix_receipt.md). The proof uses ordinary robust duality,
Young's inequality and a retained compression C, not new optimization primitives.

Keep its notation: C=W^T(I+MM^T)^(-1)W, v=Wc, ||c||=1, E=e^2>0,
eta_max=(E+sqrt(E^2+4E))/2. For a coordinate vector z take w=SWz.
Then v^T w=c^T Cz, m=||w||^2=z^T Dz, and
q=||M^T w||^2=z^T(C-D)z, with C^2<=D<=C. Dual feasibility yields

    F(N;v)>=2*c^T C z-[m+(sqrt(q)+e*sqrt(m))^2].

For ANY eta>=eta_max put a=1+eta and kappa=E+E/eta-eta<=0.
Young's inequality and m>=z^T C^2z give

    m+(sqrt(q)+e*sqrt(m))^2
       <=a*(m+q)+kappa*m
       <=z^T C*(a*I+kappa*C)z.

Thus one chosen eta,z gives the certificate

    F(N;v)>=2*c^T C z-z^T C*(a*I+kappa*C)z.              (1)

The sign restriction on kappa is essential: substituting a lower moment
with a positive coefficient would have the wrong direction. The matrix
B=a*I+kappa*C is positive definite since its smallest allowed eigenvalue
is a+kappa=1+E+E/eta>0. Optimize (1) at z=B^(-1)c to obtain

    L_eta(C,c)=c^T C*(a*I+kappa*C)^(-1)c.                (2)

The supremum over eta>=eta_max is a lower bound. Rational choices with
eta^2>=E*(1+eta) and a rational z make (1) a direct rational certificate;
no approximate matrix inverse is silently treated as exact. E=0 is the
retained value s=c^T Cc. For fixed eta, lambda/(a+kappa*lambda) is convex,
so ordinary scalar Jensen shows L_eta(C,c)>=L_eta(s,1).

## Sharpness for 0<C<I

The supremum in (2) is attained: it is positive at eta_max and tends to
zero as eta tends to infinity under this strict spectral assumption.

At an interior maximizer, take S=C and M=(C^(-1)-I)^(1/2). Put
z=B^(-1)c, w=Cz, x=M^T w. Differentiation of (2) gives

    q=E*m/eta^2, so eta=e*sqrt(m/q).

Young's inequality is tight. The gradient equation for the optimized dual
quadratic is consequently the stationarity equation of

    2*v^T w-||w||^2-(||M^T w||+e||w||)^2.

With N=M+e*(w/||w||)*(x/||x||)^T, this equation is
(I+NN^T)w=v. Hence the displayed dual value is the actual edited optimum,
and (2) is attained. The strict spectral assumption gives m,q>0.

At the left endpoint eta_max, a one-sided derivative at a maximum implies
m0=c^T C^2c<=m_star=s*(1+eta_max)/(2+eta_max). Use the same contraction
dilation S_tau as matrix_receipt.md with
tau=(m_star-m0)/(s-m0) in[0,1). Let w0=S_tau*v and x0=M^T*w0.
For N=M+e*(w0/||w0||)*(x0/||x0||)^T, the identity

    m_star-(s-m_star)=e*sqrt(m_star*(s-m_star))

implies (I+NN^T)w0=(1+eta_max)*v. Therefore the edited optimum equals
s/(1+eta_max), exactly the boundary value in (2). This witness is finite;
it does not silently import the fixed-two-moment limiting construction.

Together with the upper note this gives a prospective SHARP interval from
an entire compressed response matrix in the dimension-unrestricted strict
domain. Lower and upper endpoints can require different compatible sources.
The proofs and small checks are still DEVELOPMENT, not independent review.

## Resource and comparison boundary

One scalar search and k-dimensional linear algebra can construct witnesses;
a supplied rational eta,z uses quadratic forms in C for verification. Source
dimensions can be much larger than k, but paid old-value acquisition and
k(k+1)/2 retained entries remain. A bounded reasoner can choose between
one value, a moment interval, a whole C or full old vectors according to
its real retention/access contract. A faithful ordinary implementation ties.
The exact closest prior formulation and a natural service with a complete
resource benefit remain open research duties.

The [lower probe](matrix_lower_probe.py) passed25 direct finite-matrix
matching checks:13 boundary and12 interior. Its separate exact rational
witness eta=141/625 certifies the worked lower618573873750/1340748094907
>.4613. Together with the upper witness, the new certified width is
approximately.07660218, more than23.4% narrower than the sharp one-value
interval. [Output](matrix_lower_probe.json) records the exact fractions,
source hash, versions and224,510,700ns execution time. These gains use the
same three old target values as the earlier projection example, with more
use made of their joint information. They are not a fee or runtime gain.
