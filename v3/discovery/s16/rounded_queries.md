# Rounded scalar values: valid witnesses before optimization has converged

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass59.
This repairs the exact-oracle restriction in value_refinement.md. Ordinary
inexact coordinate descent supplies the optimization idea; no new generic
optimization claim is made.

For q(z)=z^T C z,0<C<=I, let f(z)=q(z)+||c-z||^2/d, d>0,
A=C+I/d, g=Az-c/d and G=f(z)-min f. An oracle returns truthful intervals,
including for adaptively selected vectors. With midpoint errors at most
epsilon on two queries z+h*e_i and z-h*e_i, h>0,

    hat_b_i = [mid q(z+h*e_i)-mid q(z-h*e_i)]/(4*h),
    |hat_b_i-(Cz)_i| <= eta = epsilon/(2*h).

The quadratic identity is exact: there is no finite-difference truncation
error. This does not make large vectors or high-precision values free.
Set hat_g_i=hat_b_i+(z_i-c_i)/d, L=1+1/d and update

    z_new=z-(hat_g_i/L)*e_i.

Because A_ii<=L, writing hat_g_i=g_i+xi, |xi|<=eta,

    f(z_new)-f(z) <= (-g_i^2+xi^2)/L.

For a uniformly random coordinate, even history-dependent errors satisfying
the interval warrants give

    E[G_new | history] <= rho*G + eta^2/L,
    rho=1-1/[k*(d+1)],
    E G_T <= rho^T*G_0 + k*d*eta^2*(1-rho^T).

Here ||g||^2 >= lambda_min(A)*G >= G/d. No unbiasedness of numerical
errors is assumed. With iteration-specific eta_t the noise term is instead
sum_(t<T) rho^(T-1-t)*eta_t^2/L, so decreasing certified errors can remove
the fixed noise floor. The iteration's two directional queries do not
certify q(z_new); acquire that interval separately before reporting a new
upper witness. Thus three scalar queries per reported update, or two per
internal update plus one at each chosen reporting point. Retain the best
reported upper bound, since approximate steps need not decrease it.

If each reporting interval has width at most nu, its upper witness's excess
over the best fixed-t block upper bound is at most a*(G+nu), a=1+t.
This certificate is valid at EVERY finite reporting time. A strict decision
margin gamma gives the separate computational-success bound

    P(no decision by report T)
      <= min(1, a*(rho^T*G_0+k*d*eta^2+nu)/gamma).

The probability is over coordinate selection and concerns resolution speed,
not soundness. The displayed bound can be weak or vacuous; equality and
insufficient precision need not resolve. A randomized interval oracle must
supply its own simultaneous/adaptive coverage rather than borrow this bound.

## A relative-error oracle prevents the large-step loophole

Suppose the midpoint error is warranted by epsilon_abs+epsilon_rel*q(w).
Since C<=I, two directional queries give the conservative bound

    eta(h) <= [epsilon_abs+epsilon_rel*(||z||+h)^2]/(2*h).

For epsilon_rel>0, this expression is minimized at
h=sqrt(epsilon_abs/epsilon_rel+||z||^2) (with the zero case understood as
an infimum), yielding epsilon_rel*||z||+
sqrt(epsilon_rel*epsilon_abs+epsilon_rel^2*||z||^2).
Increasing h indefinitely therefore does not remove relative error. The
actual oracle's vector size, bit precision, per-query work and availability
are part of the access contract. A source that cheaply returns C*z supplies
a stronger ordinary control, and direct solves may be cheaper still.

This is a useful implementation repair to a finite value-logic adapter:
fallible proposals and partial computation affect tightness, while checked
value intervals keep the returned counterfactual bounds valid. A literature
delta or end-to-end economic advantage has not been established.
