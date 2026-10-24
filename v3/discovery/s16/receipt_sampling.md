# Use a counterfactual value interval to skip an expensive randomized decision

Codex (GPT-6), October 23, 2026. DEVELOPMENT. Retrospective exact simulation
and bounded-likelihood Metropolis methods are the primary comparators. This
is a potential application of the new receipts, not a new sampling principle.

Suppose a downstream step needs Bernoulli(F), where F in[0,1] is an expensive
revised objective. The old information certifies L<=F<=U. Draw one fresh
uniform V. If V<L return1; if V>U return0; only otherwise buy/refine F.
Under an ideal exact full-value oracle this makes a full call with probability
U-L and returns exactly the required Bernoulli coin. A numerical oracle
instead refines certified intervals until the threshold is excluded; its
termination and bit-cost contract must be supplied.

For the worked matrix receipt, exact certified width is approximately
.07660218. The sharp one-value information permits width greater than
.10004866. Thus this particular one-score interface uses more than23.4%
fewer EXPECTED new full-value calls, conditional on both receipt sets
already being paid. This is an analytic component count, not observed audit
fees, CPU time, or an end-to-end service saving. The identical ordinary
interval sampler ties, and richer information was acquired.

If each full call costs C_F, the additional per-step receipt cost plus
amortized startup must be less than .02344648*C_F for this illustrative
comparison to pay. Counting only skipped calls while ignoring the target
basis, matrix receipt, edit warrant, random bits and interval comparisons
would not establish a saving.

## A natural nonlinear duty: exact acceptance based on an objective change

For an accept/reject step with required probability

    alpha(F)=min(1, exp(-beta*(F-s))), beta>0,

the old exact objective s and new interval[L,U] give

    alpha_lower=min(1,exp(-beta*(U-s))),
    alpha_upper=min(1,exp(-beta*(L-s))).

The full-value call probability is alpha_upper-alpha_lower. For the
worked example L<s=.5<U, it is1-exp(-beta*(U-.5)); the lower bound
does not affect this particular acceptance ambiguity. Coupling the same
uniform V to the exact accept/reject rule preserves the exact decisions.
For Metropolis-Hastings, include all other proposal/density terms correctly;
an arbitrary exponential of a utility is not automatically a valid target
distribution or transition rule.

If an accepted state's objective was not fully evaluated, it remains an
interval for the next step. Do not silently promote it to an exact old s.
One can propagate two objective intervals and refine either as necessary,
but the cheap one-step formula above no longer describes the whole chain.
Unverified floating comparisons or approximate bounds can bias transitions.

## A strong control when only a mean is wanted

If all cases share a known interval[L,U] and the task is merely estimating
their mean, directly evaluating fewer cases can use that narrower range
in its concentration bound. A fixed-range Hoeffding argument then scales
with(U-L)^2, while a naive Bernoulli simulation has range1. Consequently
the23.4% per-score call reduction is NOT automatically a mean-estimation
advantage. Residual/control-variate estimation and variance-aware bounds
are stronger controls. The adapter needs an actual randomized decision
or a justified interface constraint, not an artificially weak estimator.

The next cheap screen is closest retrospective-simulation literature and
a natural objective whose old compressed receipt is already available.
No new large experiment is justified by this calculation alone.
