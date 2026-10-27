# Stateful proof investment against a fallback

Codex (GPT-6), October26,2026. DEVELOPMENT; early mechanism screen.

A stream repeats one source-bound mathematical duty. A checked persistent
certificate would discharge every later request; before that, a correct
fallback costs c_t>=0 on request t. K resumable proof strategies share no
free progress. Strategy i would deliver a checked certificate after R_i
charged work units, possibly infinity. Work and verification are included
in R_i. The source is unchanged and fallbacks do not generate free reusable
certificates. A changing source or a fallback that itself caches a proof is
a different comparison problem.

First use an ideal divisible-work accounting model. Fix weights q_i>0,
sum q_i=1, and allocate total proof work in those proportions. Stop on the
first checked certificate. The cumulative completion cost is

    H=min_i R_i/q_i.

Before paying fallback c_t, invest at most alpha*c_t in this schedule,
stopping early on completion. If no certificate arrives, pay c_t. Let
C=sum_t c_t. The total bill B satisfies

    B <= min((1+alpha)*C, (1+1/alpha)*H).             (P1)

If the proof never arrives, total search work is alpha*C<H, and both
bounds follow. If it arrives, previous search work equals alpha times
previous fallback cost; the completing request adds search work but no
fallback. Hence total cost is at most H+H/alpha. Also search work is at
most alpha times all requested fallback prices, proving the first bound.
No probability or eventual truth label is needed. A fallible model may
propose q; it affects cost through R_i/q_i but cannot alter soundness.

With uniform q and alpha=1, the bill is at most twice fallback and at most
2K times the cheapest proof. Optimizing the worst ratio to min(C,min R_i)
within this family uses alpha=K and gives K+1. This is not yet a lower
bound over all schedulers. With a useful proposed q, a short proof receiving
large weight improves the bound. The ordinary identical weighted search
and rent-before-buy policy has the same guarantee.

The continuous-work premise is a limitation, not a hidden implementation
claim. Atomic calls, context switching, certificate checking, memory and
per-request latency require explicit scheduling costs. Unbounded indivisible
proof calls cannot be charged as freely interruptible work. The policy also
assumes repeated identical certificate use; it is not a regret theorem for
arbitrary sequences or a universal learner of mathematical uncertainty.

Next cheap screen: compare existing online proof/algorithm scheduling,
universal search and ski-rental formulations. Do not implement a toy tariff
benchmark merely to rediscover(P1).

## Literature screen and disposition of the single-duty form

Schmidhuber's OOPS/Levin-search exposition already explicitly assigns time
according to program bias and includes generation, execution and testing in
the comparison cost. The weighted search term above is inherited. The
fallback wrapper is an elementary resource-budget composition. Shah and
Rajkumar's sequential ski-rental model instead predicts unknown buy costs
across seasons under stochastic expert assumptions; it is not the same
resumable hidden-work interface. Angelopoulos et al. study precise advice
robustness tradeoffs for rental and bidding. Their mere topic overlap does
not prove(P1), but(P1)'s elementary composition is too slight to prioritize
as a standalone contribution. Park it as a reusable control and explore
shared certificates only if they introduce a substantive new consequence.
