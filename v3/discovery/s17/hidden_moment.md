# Why N16's scalar parameter has a cap

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; an interpretation of the
core proof through the separate second-block construction. It is not an
alternative claim that every minimax interchange is valid.

Write Q=W^T S^2 W. The only restrictions imposed by C alone are C^2<=Q<C.
When Q is retained, second_block.md gives lower families

    ell_t(Q)=c^T C[(1+t)C-dQ]^(-1)Cc, d=t-E-E/t,

valid for every t>0. If d>=0, this expression increases with Q, so its
smallest value occurs at Q=C^2 and is N16's lower family. If d<0, it
decreases with Q; letting Q approach C gives the infimum

    s/(1+E+E/t), s=c^T Cc.

For t<h this is smaller than the cap value s/(1+h), where
h=(E+sqrt(E^2+4E))/2. Thus parameters below h cannot improve the uniform
lower guarantee obtained by this family when Q is unknown.

For the upper family use eta>0, a=1+eta, b0=1+E+E/eta and kappa=b0-a.
Its matrix denominator is

    D_eta=a(I-C)+kappa(C-Q),
    g_eta(Q)=a-a^2 c^T(I-C)D_eta^(-1)(I-C)c.

If kappa>=0, the expression decreases with Q, so its largest value is
at Q=C^2, giving N16's upper family after reparameterization. If
kappa<0, it increases with Q; the supremum at Q approaching C is a*s.
For eta>h, this exceeds the cap value (1+h)*s, so those parameters cannot
improve this uniform upper guarantee either.

These order arguments explain the parameter restriction and its connection
to information that was discarded. They only establish the best uniform
members of these families. Exchanging optimization over Q and the parameter
without hypotheses would still be a gap. The core finite cap/interior
witnesses establish sharpness directly and avoid that exchange.

This interpretation cuts both ways in the contribution assessment. It makes
the endpoint construction more transparent and exposes exactly what the
hidden second moment does. It also shows why the result should be described
as a particular explicit solution built from conventional robust least
squares, matrix order and dilation, rather than a new general theory of
uncertainty or completion. The separate retained-Q extension has its own
attainment and prior-comparison duties and is not silently included in N16.
