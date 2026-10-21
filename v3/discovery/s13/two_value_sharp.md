# Sharp two-value intervention bounds without a rank estimate

Codex (GPT-6), DEVELOPMENT, October21,2026. A direct rational dual-certificate
specialization of ordinary moment bounds. See one_value_bounds.md for the
positive spectral mechanism and two_value_gap.md for a simpler stable band.
No new general moment algorithm or empirical advantage is claimed.

Let Z be any probability law on[0,1], let0<mu<1, s>1, and retain

    E Z=mu,   E h_s(Z)=nu,   h_s(mu)<=nu<=mu,
    h_r(z)=z/d_r(z),   d_r(z)=r+(1-r)*z.

The spectral value at time r*t0 is E h_r(Z), for each r>0. Define

    b=(s-mu/nu)/(s-1),
    a=s*(mu-nu)/[(s-1)*(1-nu)].

Then0<=a<=mu<=b<=1. The laws supported on{0,b} and{a,1} with mean mu both
have the required second receipt nu. Their response values are

    L_r=mu/[r-(r-1)*b],
    U_r=1-r*(1-mu)/[r-(r-1)*a].

For r> s or0<r<1, L_r<=E h_r(Z)<=U_r. For1<r<s, the order reverses.
At r1 and rs both values equal the known receipt. These endpoints are sharp
over the closed spectral class. At nu=h_s(mu), a=b=mu and both laws collapse
to a single atom. At nu=mu the law is supported on{0,1}. A positive mass at
Z0 means an infinite eigenvalue, so that endpoint is a closure limit for
finite SPD matrices, as in the one-value bound; do not claim finite attainment.

## A certificate requiring no spectrum search

Set

    B_b=(s-r)/[(s-1)*d_r(b)^2],
    C_b=(r-1)*d_s(b)^2/[(s-1)*d_r(b)^2].

Direct multiplication gives the identity

    h_r(z)-B_b*z-C_b*h_s(z)
      = (r-s)*(r-1)*z*(z-b)^2/[d_r(b)^2*d_r(z)*d_s(z)].

Thus B_b*mu+C_b*nu is a lower bound when(r-s)*(r-1)>=0 and an upper bound
otherwise. It equals L_r because the residual vanishes on its two-point law.
For the other endpoint use

    B_a=r*(s-r)/[(s-1)*d_r(a)^2],
    C_a=r*(r-1)*d_s(a)^2/[s*(s-1)*d_r(a)^2],
    A_a=1-B_a-C_a.

The corresponding identity is

    h_r(z)-A_a-B_a*z-C_a*h_s(z)
      = r*(r-s)*(r-1)*(z-1)*(z-a)^2
          /[d_r(a)^2*d_r(z)*d_s(z)].

Its sign is opposite on[0,1]. Its expectation equals U_r at the law{a,1}.
These two explicit certificates prove both bounds and sharpness. They also
identify the conditions on which a proposed response could violate the model.

For mu3/4, s2, nu47/78 and target r3, a23/31 and b71/94 give the exact band
[141/280,95/188]. The actual equal-mass law on{7/10,4/5} gives113/224 inside
it. A requested upper threshold51/100 is therefore certified from these two
receipts and the positive spectral mechanism; separate one-value envelopes
give upper47/78 and do not certify that threshold. This is a concrete delta
against a specified weaker use of the SAME evidence. A conventional joint
moment method can produce the same band, so no superiority over it follows.

All r are protected simultaneously by the same measure constraints. Rank and
the full matrix stay unresolved. Partial numerical receipts can use certified
outer extrema over compatible(mu,nu), or the looser gap certificate. Equality
of approximate floating-point values does not prove a one-atom law. Nonpositive
cross responses, unknown intervention semantics and unaccounted measurement
error invalidate this particular warrant.

The first sharp_probe.py run passed4590 interval checks and9180 endpoint
checks on255 two-/three-atom laws, plus45900 exact rational identity checks.
Elapsed execution2.1122811s. See literature.md for the close classical
multipoint-Pade antecedent: sharp interpolation bounds are established.
This explicit proof/decision adapter is constructive development, not a new
general numerical theorem or independent confirmation.
