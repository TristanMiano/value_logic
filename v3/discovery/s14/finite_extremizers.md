# Finite rank-one extremizers remove an unnecessary limiting construction

Codex (GPT-6), DEVELOPMENT, October 22, 2026. This strengthens the attainment
statement in finite_transport.md and decision_radius.md. Their formulas and
inequalities remain unchanged; the earlier diagonal limiting examples remain
valid but were unnecessarily restrictive for the one-scalar contract.

For any 0<t<s<1 with s+t<=1, take a unit vector v and a vector w satisfying

    v^T*w=s, ||w||^2=s^2/(s+t).

Dimension two suffices because s^2<=s^2/(s+t). Put

    q=sqrt(s*t/(s+t)),
    M=(v-w)/q, N=(v-(t/s)*w)/q,

where M,N are one-column matrices. Direct multiplication gives

    M^T*w=q, w+M*(M^T*w)=v;
    N^T*((t/s)*w)=q, (t/s)*w+N*(N^T*((t/s)*w))=v.

Consequently g(M)=s, g(N)=t, and

    ||N-M|| = (s-t)/sqrt(s*t).

This attains the lower-region distance in decision_radius.md with finite
rank-one matrices. The upper region s+t>=1 already has scalar extremizers.
Thus for every strictly positive pair the stated level-set distance is a
minimum, not merely an infimum. Zero response still requires a closure limit
when matrices are finite.

Equivalently, for e>0 and a-1/a=e, every point of the linear lower branch
t=s/a^2 with s<=a^2/(1+a^2) has this finite construction, since s+t<=1.
Reversing M,N gives finite attainment of the linear upper branch. The
nonlinear branches retain the earlier scalar examples. Therefore both
one-scalar envelopes are actually attained for all positive feasible old
values (with the cap one handled as before).

One concrete exact example, using unnormalized column entries divided by
q=sqrt(2)/5, is

    v=(1,0), M=(9/10,-1/10)/q, N=(3/5,-2/5)/q.

It has g(M)=1/10, g(N)=2/5 and distance3/2. The upper ratio is exactly4,
matching a=2. This example changes the column direction; diagonal examples
with a fixed shared eigenbasis did not exhibit its finite attainment.

The two-scalar lower theorem has a different scope. Its lower bound need
not be attained at arbitrary fixed second moments. Finite attainment above
uses the special moment m=s^2/(s+t), or m=s*r_star for the lower-envelope
linear branch. Do not promote this stronger one-scalar attainment statement
to all two-scalar cases.

The nonmetric counterexample remains valid: the closest matrices for two
successive scalar transitions need not share the same intermediate matrix.
Finite attainment does not restore a triangle inequality between level sets.
This is a useful correction to the information geometry, not a measured
cost gain or a proof of novelty relative to operator perturbation theory.
