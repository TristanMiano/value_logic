# Independent reconstruction before source inspection

Reviewer: ChatGPT, GPT-6 Astra Pro, same-model internal subagent. The root supplied the candidate recurrence, cost constants and the optional-stopping candidate. This is a nonblind reconstruction from that prompt, written before reading the planning source or companion. All activity is DEVELOPMENT, unmeasured, with zero principal-clock credit.

## Supplied finite-law decision model

Let the fixed latent service law have completion probability theta in {9/20,11/20}, with supplied prior good-law mass pi. Conditional on the law, paid profile completions are IID Bernoulli and future deployment uses the same stated law. A completed attempt yields a checked correct answer and zero task loss, a failed attempt uses fallback loss one, and every attempt costs one-half. Relative to immediate fallback, one deployed future query therefore has expected gain theta-1/2, namely plus or minus 1/20. There are H future queries. The allowed terminal choices are fallback on them all, or the declared deployment on them all; no extra future policy class is silently included. Profile probes have no task reward beyond information about this law.

At count state (s,f), prior half gives posterior

```math
pi(s,f)=11^s9^f/(11^s9^f+9^s11^f).
```

The posterior is sufficient because order carries no additional information under this model and the remaining acquisition cap is determined by s+f. The predictive success probability is q=9/20+pi/10. Immediate deployment gain is D(pi)=H(2pi-1)/20 and optimal terminal gain is M(pi)=max(0,D(pi)).

## Bounded dynamic program and precise cost placement

Let ell be the charge to consult a decision state, g the other charged controller work per purchased profile observation, and b=1/2 its service bill. Define J at a state before its lookup and W=J+ell after that lookup has already been paid. With remaining cap zero, W=M. Otherwise

```math
W(s,f)=max{0,D(pi),-b-g-ell+q W(s+1,f)+(1-q)W(s,f+1)}.
```

The next lookup belongs in the purchase branch because either child must consult its next decision. Thus if the root's combined per-observation controller charge is 16u and ell=8u, the root continuation coefficient should be c'=1/2+16u and initial full value J(0,0)=W(0,0)-8u. Source inspection must verify how the two 8u parts are assigned; it must not count a child lookup twice or omit it. A separately paid table-building cost C_build gives cold-start value W(0,0)-8u-C_build.

Backward induction proves the recurrence over all history-dependent and randomized bounded profile-then-terminal-decision policies permitted by this fixed model and cost interface: condition on the next observation, use the optimal child continuation values, and maximize over the finite available actions. Mixing current actions cannot exceed their maximum. State sufficiency then removes irrelevant order dependence. A declared stopping tie rule does not change the optimal value. This is ordinary finite Bayesian planning for a supplied prior/law, rather than a frequentist guarantee under each law.

For the frozen selected policy, a separate conditional-law forward enumeration must keep its Bayesian policy decisions fixed while using theta=9/20 or11/20 for branch probabilities. The prior-weighted average of conditional-law terminal gains minus profile and per-visit control bills must equal J(0,0). Conditional good/low-law values need not each be nonnegative. Table construction remains a separate actual setup charge.

## Arbitrary-prior adaptive profiling obstruction

For any posterior pi, weighted child terminal gains simplify without a posterior denominator:

```math
E[M(pi_next)|pi]
 = H/20 * [(pi-9/20)_+ + (pi-11/20)_+].
```

Subtracting M(pi) gives a tent: zero outside [9/20,11/20], equal to H(pi-9/20)/20 on [9/20,1/2], and H(11/20-pi)/20 on [1/2,11/20]. Its supremum is H/400, attained at prior/posterior half.

Hence if every observation costs at least c' >= H/400, Z_n=M(pi_n)-c'n is a supermartingale under every supplied initial prior. For bounded stopping N, optional sampling yields E[M(pi_N)-c'N] <= M(pi_0). For E[N]<infinity, truncate N by k: the bounded M term converges and c'(N-min(N,k)) has expectation tending to zero, giving the same conclusion. If E[N]=infinity and c'>=1/2, the bounded terminal reward and positive linear bill give extended expected gain minus infinity; an infinite probe sequence cannot improve the objective.

With a strict gap the stronger inequality is E[M(pi_N)-c'N] <= M(pi_0)-(c'-H/400)E[N] whenever the expectation is finite. For H=128, H/400=8/25=.32 and c'>=1/2, so each expected probe loses at least9/50=.18 relative to immediate optimal stopping, before other setup or initial lookup charges.

This statement permits arbitrary adaptive numbers of these pure information probes. It keeps the two fixed completion laws, their Bayesian update, H, terminal action class and cost lower bound. It is not a lower bound for arbitrary computation programs, task-reward-producing observations, changing service laws, or a larger adaptive deployment policy class. It makes no empirical service-performance or CPU claim and does not supply the human work needed to construct the model.
