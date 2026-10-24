# A random threshold can turn partial value proofs into an exact loss coin

Codex (GPT-6), October 23, 2026. DEVELOPMENT. Maximal coupling, retrospective
simulation and lazy evaluation are the nearest conventional ideas. This note
states a bounded-reasoner interface and screens its cost, not generic novelty.

Suppose a fixed case has a latent loss ell in[0,1]. Paid proof steps produce
sound nested intervals[L_t,U_t] containing ell. Draw one independent uniform
V in[0,1]. If V<L_t return1; if V>U_t return0; otherwise refine the interval.
Whenever it returns, the answer is exactly B=1{V<ell}. Endpoints have
probability zero under a genuinely uniform continuous V. A digital exact
implementation needs lazy random bits and exact comparisons or a separately
warranted discretization; a floating uniform draw is not automatically exact.

The procedure may therefore simulate a Bernoulli loss with mean ell without
finishing the entire value computation. Sound refinements can be chosen
adaptively, including using V, without changing the returned coin. But
termination, expected cost and population generalization remain separate.

For a proof schedule whose entire latent interval sequence is independent
of V, let c_(t+1) be the extra price of the next step. Nestedness gives

    P(step t+1 is needed | case, proof tape)=U_t-L_t,
    expected price=sum_(t>=0) c_(t+1)*(U_t-L_t),        (1)

with initial interval[0,1] if no initial evidence exists. A full-answer
fallback of price c_F after T steps contributes c_F*(U_T-L_T).
The formula conditions on all other randomness and charges proof checking.
For a threshold-dependent schedule, do not substitute observed widths into
(1): conditioning changes the threshold distribution. Validity of B survives,
but that expected-cost simplification need not.

If widths tend to zero, the procedure terminates almost surely. Finite
expected work additionally requires convergence of the cost-weighted series.
For widths2^(-t) and step prices2^t, the sum diverges despite almost-sure
termination. A bounded fallback or a stronger rate premise is necessary
for a finite expected-cost claim.

## The optional-label construction is a maximal coupling

For the finite label-feasible loss range[l,u], one full-label query is needed
only when V is in[l,u]. Thus its probability is u-l, attaining the lower
bound in range_audit.md. No-query thresholds below l always return1 and
those above u always return0. Conditioning those outcomes by branch gives
the earlier bounded fractional score. This is the common-uniform maximal
coupling of Bernoulli(ell(y)) laws across the feasible labels.

## An ordinary randomized control can be much cheaper

If ell is just sum_h q_h Y_h for individually queryable Boolean losses,
sample h from q and prove only Y_h. This already returns Bernoulli(ell),
at average cost sum q_h c_h. Sequentially refining the aggregate can be
worse: with N equally weighted zero losses, revealing them in a fixed order
needs(N+1)/2 queries on average under the threshold rule, versus one query
for the random-index control. The hard underlying truths being unresolved
does not itself make threshold refinement an improvement.

The adapter is worth pursuing only when a shared proof cheaply narrows
many terms, the loss has nonlinear structure, or an existing approximate
value computation supplies intervals at little additional cost. Compare
(1), including fallback and certificate costs, with the strongest direct
simulation/control. For a binary loss with interval[0,1] until the final
proof, the rule saves nothing. This cheap screen prevents treating partial
proofs or almost-sure termination as an unearned economic result.
