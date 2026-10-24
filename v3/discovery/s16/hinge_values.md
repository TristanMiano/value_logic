# A value book need not be a probability reconstruction

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass34.
Early screen: generic novelty rejected. Stop-loss transforms, option-price
inversion and convex-payoff representation are established subjects.

For an unknown probability law mu on [0,1], define the value query

    C_mu(t)=E_mu[(X-t)_+].

Its right derivative is -P_mu(X>t), so the full exact value function identifies
the law. This uses specified payoffs and one fixed linear expectation
functional. Arbitrary costs, changing stakes or market prices do not thereby
identify a physical probability law; a pricing measure can be a different
object. This is an elementary reconstruction of a classical fact.

## A finite certificate with an explicit approximation bill

Suppose two candidate laws have |C_mu(j/n)-C_nu(j/n)|<=epsilon at j=0,...,n.
For every1-Lipschitz payoff f, interpolate f linearly on that grid. The
interpolant has form

    g(x)=f(0)+s0*x+sum_(j=1)^(n-1)(s_j-s_(j-1))*(x-j/n)_+,

with |s_j|<=1, and ||f-g||infinity<=1/(2n). Consequently

    |E_mu f-E_nu f| <= (2n-1)*epsilon+1/n.          (1)

The bound holds simultaneously for all such f, hence also bounds their
1-Wasserstein distance. Its best grid size at fixed epsilon is of order
epsilon^(-1/2); buying increasingly many equally noisy values is not
automatically helpful. If each law merely fits an observed value book within
eta, use epsilon=2eta when comparing two compatible laws.

For a particular piecewise-linear action contrast g, the exact relevant
uncertainty bill is instead

    |s0|*epsilon_0 + sum_j |s_j-s_(j-1)|*epsilon_j.  (2)

It depends on the contrast's slope changes, not the number of probability
coordinates. A value model may therefore certify a decision even when a
global probability-recovery bound is too loose. Directly evaluating the
action contrast is a mandatory strong control. Shared value queries need a
reuse or access advantage over that control to justify their acquisition.

For convex f the slopes are monotone, so their total variation is at most2
and the coefficient bill is at most3epsilon. Convexity also makes g-f
nonnegative, giving interpolation contribution at most1/(2n), rather than
1/n, to the difference of the two expectations. These are consequences of
standard payoff spanning, not a newly discovered value semantics.

This screen supports the program's distinction between information adequate
for a decision and information adequate for a complete law. It does not add
a new empirical learner or justify a promotion; a priced repeated-query
application would have to supply the substantive delta.
