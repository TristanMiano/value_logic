# Anytime risk warrants from proofs that finish out of order

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass19.
This adapts ordinary test-supermartingale confidence sequences, not a claim
that unfinished mathematical statements have stochastic truth values.

## Latent cases and the observation contract

Draw iid cases Z_i from a fixed source. Each has a fixed bounded loss
Y_i in[0,1], possibly a deterministic but expensive mathematical property
of Z_i. The risk is p=E Y_i. Under a tested null p>=p0, choose lambda_i
before exposing case i, from past cases, past computations and independent
coins, with0<=lambda_i<=1/(1-p0). Thus

    E_n = product_{i<=n} [1+lambda_i*(p0-Y_i)]

is a nonnegative supermartingale starting at1. No computed value for every
Y_i is needed to define this latent process. Predictability is with respect
to the full case filtration, not merely to which labels the reasoner admits
having computed. A bet chosen from the current case's features is not covered
by an unconditional risk null. Constant predeclared bets avoid that issue.

At any computation step tau, sound, version-matched receipts give
U_i(tau)>=Y_i, with U_i in[0,1]. Initially U_i=1. Proof jobs can be selected,
interrupted and completed in any order, including in light of later arrived
cases. They only refine upper bounds; they do not delete hard cases. Define

    L_n(tau) = product_{i<=n} [1+lambda_i*(p0-U_i(tau))].

All factors are nonnegative, so L_n(tau)<=E_n pointwise. Therefore

    P[there exists tau,n with L_n(tau)>=1/delta] <= delta.       (1)

Indeed that event is contained in {sup_n E_n>=1/delta}, and Ville's
inequality applies. It covers arbitrary proof scheduling and refinements,
selection of a historical prefix, and an unbounded number of fresh cases.
No completion-time independence or per-prefix union allocation is needed.
The source version and truthfulness of receipts remain explicit premises.

The iid premise can be replaced by the conditional null
E[Y_i | complete past] >=p0. The original single marginal-risk meaning
requires iid or a separately justified stationary interpretation.

## An actual upper confidence sequence

Take predeclared theta_i in[0,1), put lambda_i(p0)=theta_i/(1-p0), and let
p0 vary in[0,1). Each factor equals

    1+theta_i*(p0-U_i)/(1-p0),

which is nondecreasing in p0. Mixtures over finitely many predeclared theta
sequences with nonnegative weights summing to1 retain both supermartingale
validity and monotonicity. The infimum p0 at which any retained lower wealth
crosses1/delta defines an upper risk bound (use1 if there is no crossing).
For the actual p, an upper bound below p implies a crossing at p itself;
apply(1) at that single true p. There is no additional union cost for scanning
the confidence endpoint. Continuity of the finite-prefix factors gives the
usual open/closed endpoint convention; a strict crossing is simplest.

For Boolean losses, one proved success changes U_i from1 to0. With constant
theta, g proved successes and u unresolved-or-bad cases in a prefix give

    L_n(p0) = [1+theta*p0/(1-p0)]^g * (1-theta)^u.

Unresolved and proved bad cases have the same pessimistic factor. This loses
power but prevents selective proof completion from pretending to be a new
iid sample. Treating only completed successes as a sample would certify any
small risk eventually even if the true bad probability were1/2.

## Retention and the counted update mechanism

Retain the maximum lower wealth over all arrived prefixes. New cases cannot
erase a previously valid risk warrant. Sound refinements only increase each
affected prefix wealth. For a fixed p0 and bet sequence, a binary tree stores
each interval's product P and maximum prefix product M, including the empty
prefix1. Combine adjacent intervals by

    P = P_left*P_right,
    M = max(M_left, P_left*M_right).

A completed proof changes one leaf and O(log n) tree nodes. Appending cases
can use a doubling tree or a forest. This avoids rescanning every prefix on
every out-of-order proof completion. Exact rational factors are possible;
floating implementations need conservative arithmetic. The numerical bit
length, proof checking, memory and acquisition costs are not erased by the
node-count bound. Mixtures can keep one tree per component, but the maximum
of component wealths is NOT their mixture; use a common prefix or spend
explicit component confidence weights when reporting separate maxima.

This is a potential useful interface extension from fixed-cohort receipts
to continuing case acquisition. Generic anytime-valid inference is ordinary
prior work. Closest delayed-feedback and partial-verification comparisons
must be screened before a novelty claim or large implementation.

The [finite probe](anytime_probe.json) checks4096 equiprobable length12
Bernoulli(.5) null sequences at p0=.5, theta=.5, delta=.25. The valid
arrival-order rule crosses with probability299/2048 (about14.6%); deleting
all unresolved/bad cases and keeping only completed successes crosses with
probability3797/4096 (about92.7%). These are exact finite probabilities,
not estimates from a sampled benchmark. Another6561 partial receipt states
check pointwise domination, and119 out-of-order updates check the tree
against direct prefix multiplication.

At delta=.05, theta=.5, the single-prefix upper bound is about3.160% for
1470 proved successes among1500 retained cases, and2.887% for4900 among5000.
These particular bounds remain valid under the anytime protocol. They are
confidence upper bounds, not observed error rates or proof-cost savings.
