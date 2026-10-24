# A direct old-solution interpretation of the bounds

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; an alternative derivation
that exposes the ordinary primal/dual machinery behind N16. It complements
[the attainment proof](proof.md), rather than creating another target.

Let R=(I+MM^T)^(-1)W and X=M^T R. Then

    R+MX=W, W^T R=C, R^T R=Q, X^T X=C-Q, Q>=C^2.

The last inequality is the projection inequality for R onto span(W).
These identities hold even when the full resolvent has eigenvalue one.
Although R and X need not be stored, they can be used in a mathematical
certificate whose final expression depends only on C.

## Lower bound from the span of old residuals

Use Rz as a trial vector in the dual quadratic for the edited problem.
Since ||N^T Rz||<=||Xz||+e||Rz||, Young's inequality with t>0 gives

    F(N;Wc)
      >= 2c^T C z-||Rz||^2-(||Xz||+e||Rz||)^2
      >= 2c^T C z-(1+t)z^T C z+d z^T Qz,
    d=t-E-E/t.

For d>=0, Q>=C^2 yields the lower quadratic

    2c^T C z-z^T C[(1+t)I-dC]z.

Maximizing it over z gives exactly c^T L_t(C)c. This recovers the lower
family without first introducing an operator-valued Young/Jensen chain.
The optimizer is z=[(1+t)I-dC]^(-1)c. The common scalar t applies to
the complete vector norm; separate eigenvalue choices cannot be substituted.

## Upper bound from the span of old coefficients

Use Xz as a trial coefficient for the edited problem. Its old residual is

    r_z=Wc-MXz=W(c-z)+Rz.

For eta>0, set a=1+eta, b=1+E+E/eta and kappa=b-a. Young gives

    F(N;Wc) <= (||r_z||+e||Xz||)^2+||Xz||^2
             <= a||r_z||^2+b||Xz||^2.

Expanding the last expression using the old Gram identities gives

    a[||c-z||^2+2(c-z)^T C z]+b z^T C z-kappa z^T Qz.

When kappa>=0, replace Q by its lower bound C^2. With H=I-C the result is

    a(1-2c^T Hz+z^T Hz)+kappa z^T C H z.

Minimizing this positive quadratic yields z=a(aI+kappa C)^(-1)c and
the upper expression g(eta) in proof.md. The condition kappa>=0 is
eta<=h. The change t=E(1+eta)/eta gives the stated U_t family.

## Why the cap and the sharpness step are necessary

Outside these parameter ranges the coefficient of the unknown Q reverses
sign, so its lower bound C^2 no longer justifies the same substitution.
This is the same obstruction seen in the inverse-compression derivation.
At the cap its coefficient vanishes. A suitable hidden second moment can
then make Young's inequality exact without altering C; the direct normal
equations establish that the trial vector is an actual edited optimizer.

Thus the valid inequalities are standard variational reuse optimized over
a hypothetical span of old solutions/residuals. The possible contribution
is the proof that these computable bounds solve the entire specified
information problem, including its cap witnesses, plus a useful certificate.
The formula does not make ordinary variational reasoning obsolete or beat
an identical implementation. This derivation also shows exactly where an
additional retained second-moment matrix Q could improve the information
contract; that extension is separate from N16-C/v1.
