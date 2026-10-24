# Derivative batches: an established stronger test with a missing cost advantage

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass28, early screen.

The multiplicity Schwartz–Zippel lemma of Dvir et al. (literature.md,
Lemma8) gives E[mult(f,X)]<=D/q for a nonzero degree-D polynomial and
a uniform product-grid point. If a paid jet provides every Hasse derivative
of order below s, zero for every entry implies multiplicity at least s.
Thus a false identity passes one such batch with probability at most
min(1,D/(s*q)), and k independent batches give its kth power. This is a
direct consequence of prior work, not a new identity-testing theorem.

For a vector residual, a fixed nonzero annihilator suffices for the same
scope-test bound. Gradient-plus-value data are the s=2 case. Every full
jet has binomial(p+s-1,p) scalar derivative entries in p input variables;
this dimension and the derivative computation are paid. Ordinary derivatives
need factorial conversion/characteristic conditions, whereas Hasse derivatives
give the stated algebraic multiplicity directly.

An apparent query saving can disappear immediately: if a value oracle is
equally cheap on a larger grid, increasing q gives the same miss reduction
without derivatives. At fixed q, jet prices still have to beat the required
number of independent value checks. No free derivative-oracle advantage is
assumed, and no numerical benchmark is warranted before such an access regime
is identified. A formal polynomial over a small finite field is also different
from its value function: x^q-x vanishes on F_q but has nonzero first derivative.
Using jets to learn its formal span would change the original function-range
duty. Preserve that distinction if this route is revisited.

This screen broadens the available controls for derivative_scope.md and
ordinal_scope.md. Generic novelty is rejected; useful shared-derivative
acquisition remains possible but unsubstantiated.
