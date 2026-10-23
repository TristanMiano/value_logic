# Lossy reconstruction is a different acquisition duty

Codex (GPT-6), DEVELOPMENT, October22,2026. Uses the cap-three local
potential from vector_rate.md. This is a proposed consequence, not a new
rate-distortion theory or a completed high-reset optimum.

Same independent fair n-bit source and private-reset cap-three interface,
but the public output is an estimate xhat with expected Hamming error at
most delta*n, where0<=delta<=1/2. Expectation includes source and independent
coins. This differs from a bound on the probability of any output error.

For a terminal source cell W with estimate xhat, every internal cube edge
has exactly one endpoint differing from xhat on that edge's coordinate.
Charge it there. A vertex x receives at most d_H(x,xhat) such charges, so

    E(W)<=sum_(x in W) d_H(x,xhat).

Averaging terminal cells gives expected residual edge potential at most
delta*n. Separately the binary entropy bound gives

    H(X | public transcript, coins)<=n*h2(delta).

One proof bounds each coordinate's conditional entropy by the entropy of
its error bit relative to xhat, uses subadditivity, and applies concavity
of h2 to the n averaged error probabilities. If actual error is smaller
than delta*n, monotonicity on[0,1/2] gives the displayed inequality.

For f>=1/2, set a=(8+2f)/3 and b=(2f-1)/6 as in vector_rate.md. Telescoping
its nonnegative edge/entropy potential proves

    E[fee]>=n*[a*(1/2-delta)+b*(1-h2(delta))].             (1)

For0<=f<=1/2, the existing pure-edge coefficient instead gives

    E[fee]>=gamma*n*(1-2delta), gamma=(7+4f)/6.          (2)

Run the exact full-vector prefix decoder with probability1-2delta and
otherwise output independent fair guesses. The expected error is exactly
delta*n on EVERY fixed world and the expected fee is
(1-2delta)*[gamma*n+O_f(1)]. Thus(2) is asymptotically sharp under the
declared average-fee contract. Coin generation and controller work are
unpriced here; a pathwise budget is a different problem.

For f>1/2, the same upper construction and(1) leave the leading gap

    b*[h2(delta)-2delta]*n.

This gap is real in the bounds, not demonstrated extra achievable value.
Recovering one fixed fraction of bits and guessing the rest has the same
leading fee/error tradeoff as the all-or-nothing mixture. A two-bit parity
observation by itself reduces no marginal Hamming error for fair bits.
A simple two-bit OR message is also dominated by revealing one bit at
cap two: both save1/2 expected bit-error, while OR costs more queries.
These cheap screens reject two tempting proposals before a coding harness.

Conventional rate-distortion coding, zero-delay/causal source coding and
finite-lookahead encoders are mandatory comparisons. The private episode
can acquire only a few coordinates before its answers disappear, so an
ordinary block encoder with all source bits already available cannot be
imported at no acquisition charge. Conversely, restricting an unproven
optimal protocol to revealed prefixes would silently discard correlated
posterior cells. Retain the high-reset gap as an open direction, not a
reason to spend the rest of this recurrence on finite oracle expansion.
