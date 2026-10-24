# Pool logical information across betting strategies: useful but dominated here

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass60, early screen.

Let E_j(t,Y) be nonnegative test supermartingales for the same null, with
fixed nonnegative weights pi summing to one. Their weighted sum is a test
supermartingale. A sound, possibly adaptively acquired constraint set K_t
containing the actual unresolved truth vector yields the computable lower
certificate

    L_t = inf_(y in K_t) sum_j pi_j E_j(t,y).

Pointwise L_t<=sum_j pi_j E_j(t,Y), so crossing 1/alpha at any time retains
the mixture's Ville bound. L_t need not itself be a supermartingale. Any
solver used for the infimum must return a certified LOWER bound, not just
a feasible minimizer. Constraints may come from late proofs; they must be
sound, and the betting strategies must satisfy their own predictability
contracts. A scheduler does not retroactively license bets based on their
current outcome or outcome-revealing partial computations.

This can improve on summing separately minimized certificates because
the worst truth assignments for different strategies may conflict.
Consider two independently uniform-with-replacement catalogue draws per
round, with fixed catalogue error fraction p. Each stream has iid binary
errors Y_jt. Under H0:p>=4/5, each factor 9/5-Y_jt has conditional mean
at most one. Use E_j=product_t(9/5-Y_jt), pi=(1/2,1/2).

Suppose proofs certify Y_1t+Y_2t=1 in each of 18 sampled rounds but do not
identify which member is wrong. If stream1 has s errors,

    (E_1+E_2)/2
      =[(9/5)^(18-s)*(4/5)^s+(9/5)^s*(4/5)^(18-s)]/2
      >= (36/25)^9 = (6/5)^18 > 26.6 > 20.

Thus a joint logical lower certificate rejects at alpha=.05, whereas
separate minimization yields only (4/5)^18<1. Neither individual outcome
needs to be resolved. This is an exact finite example, not a claim that
the required proofs are cheap or commonly available.

## Early rejection of an efficiency claim

A stronger ordinary control uses the paired observable
Z_t=(Y_1t+Y_2t)/2. It is in[0,1] with conditional mean p. Consequently
1+5*(4/5-Z_t) is a valid nonnegative factor under the same null.
The same proof makes Z_t=1/2, giving factor 5/2 per round; just four
such paired proofs give (5/2)^4=39.0625>20. It needs no individual
outcomes either, and uses the identical paired truth information.

Therefore the proposed pooled-strategy construction is sound but loses
badly to a direct paired test in its motivating example. Do not promote
its 18-pair result as a cost gain. General coupled logical constraints may
still justify certificate optimization, but that requires an application
where an equally informed direct statistic does not already extract more
evidence. The positive lesson is that unresolved individual mathematics
can suffice for a task; the efficient mechanism here is conventional
aggregation of the proved quantity, not the mixture wrapper.
