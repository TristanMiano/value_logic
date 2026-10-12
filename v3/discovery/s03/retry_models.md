# S22: learning the right restart law

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
Connects S15's model mixtures with S21's failed computation attempts.

## Average task success is not per-instance regeneration

Half the tasks always succeed on one attempt; half never succeed at the chosen
cutoff. The first-attempt success rate is 1/2. Treating that as a fresh Bernoulli
chance at every retry predicts expected cost 2c and almost-sure completion.
Actually, after one failure this task belongs to the hard class and its chance
of success on further identical-cutoff attempts is zero. The observed failure
must update the model of task difficulty. A timeout is still not a refutation
of the underlying mathematical statement.

For a fixed latent per-instance probability P, fresh random restarts are iid
conditional on P, not marginally iid. After k failures the posterior is
proportional to (1-P)^k times its initial law. Write s_k=E[(1-P)^k] and
h_k=E[P(1-P)^k]/s_k when s_k>0. The next success probability is h_k, and

```
h_(k+1) = h_k - Var(P | k failures)/(1-h_k).
```

Thus failure makes this hazard nonincreasing, strictly decreasing when the
remaining mixture has nonzero variance and h_k<1. The expected invoice for
unlimited retries is E[c/P], with infinity when the appropriate integral
diverges, not c/E[P]. Equality requires a degenerate positive P (apart from
trivial zero cost). The arithmetic/geometric replacement can hide infinite cost.

## A constructive stopping rule

For one receipt with fixed value V and cost c>0 per attempt, no partial reward,
no informative side channel except failure, and the supplied mixture above,
the expected net gain from at most n attempts is

```
G(n) = V(1-s_n) - c sum_(k=0..n-1) s_k.
G(n+1)-G(n) = s_n (V h_n-c).
```

Since h_n is nonincreasing, the optimal cutoff is the first n with V h_n<=c,
or unlimited retries if no such n exists. Before that point the marginal gain
is positive; thereafter it is never positive again. Random cutoffs give convex
combinations of these gains, so cannot improve the optimum. With a finite
cap H, take the smaller cutoff. This is ordinary Bayesian optimal stopping,
not a new stochastic-control principle. It gives a compact revisable performance
model rather than treating the initial pooled rate as immutable.

The reward V is the value of receiving the checked result, assumed constant
through failures. If failures also change the best truth prediction or other
query values, V must change with the full belief state; this one-dimensional
rule is then not a complete controller.

## Primary restart comparison

[Luby, Sinclair and Zuckerman (1993)](https://www.cs.utexas.edu/~diz/pubs/speedup.pdf),
sections 1–2 and the statement of Theorem 5 in section 3, were read. The restart
law is for a **fixed input** with independent random bits on each fresh run.
Their known-law analysis minimizes the repeated-cutoff expected runtime; their
universal schedule handles unknown fixed-input distributions with logarithmic
overhead relative to the optimum. No proof of that universal bound is imported
here. The law may place some mass at infinite runtime, but it must have a
positive finite completion chance for the fixed input. It does not turn a pooled
population frequency into a conditional success probability for every task.

Our c/p formula assumes a fixed charge per attempt. For a real cutoff t,
success may stop early, giving mean invoice E[min(T,t)]/Pr(T<=t), the quantity
in their Lemma 1. A cost budget must include the actual execution semantics.

## Useful directions and boundaries

A hierarchical model learned from previous instances can forecast a mixture
over difficulty; per-instance failures update its posterior and chosen cutoff.
This is revisable advice. Validate its **source-expected decision payoff** on
fresh tasks or simultaneously covered policy families (S12/S14/S16); do not
convert that guarantee into the per-world lower-success assumption in S21.
Model revision changes the stopping policy, so retained evaluations need the
same policy, checked off-policy support, or a prior-covered policy class.

Even a universal restart schedule cannot guarantee positive acquisition gain
against every unconstrained runtime law. Any policy with positive expected
spending on an instance that never returns incurs negative gain there. Without
a completion assumption, risk allowance or task-distribution guarantee, the
only universally nonnegative acquisition is to spend nothing. This explains
why learning and openly priced exploration cannot be replaced by notation.

## Values reveal the relevant survival law at a declared horizon

Two performance models can agree on the next attempt yet disagree on all
continuation. A fixed P=1/2 and a half-half mixture of P=0 and P=1 have identical
one-step value V/2-c. After a failure their hazards are 1/2 and zero, respectively.
The first-step value is not a sufficient continuation state.

For at most H identical-cutoff attempts, the sequence s_0,...,s_H suffices for
every capped single-receipt payoff above and every failure-conditioned stopping
choice. It need not identify the full mixture over P. These are the first H
moments of 1-P; infinite-dimensional model recovery is unnecessary for this
bounded decision menu.

Conversely, exact values G(0),...,G(H) at known V>0,c recover that sequence:

```
s_0 = 1
s_(n+1) = (1-c/V)*s_n - (G(n+1)-G(n))/V.
```

The algebra uses the declared payoff and invoice semantics. Unknown stakes or
costs reintroduce nonidentification; querying every exact value is not free.
If each G estimate has absolute error <=epsilon and 0<c<=V, the recurrence's
survival error is at most (2epsilon/c)*(1-(1-c/V)^n), by the geometric sum.
For c=0 the direct identity s_n=1-G(n)/V gives epsilon/V instead. These bounds
are conservative and do not certify that noisy reconstructed numbers form a
valid survival sequence. Recovering h_n=(s_n-s_(n+1))/s_n can be unstable when
s_n is small; late histories are both rare and potentially hard to forecast.

For a menu of caps with value bounds L_n<=G(n)<=U_n, choose the largest L_n.
Then max_n U_n-L_chosen directly bounds regret without reconstructing hazards
or dividing by rare survival. This is a useful distinction between a decision
certificate and a detailed performance model, but is ordinary interval decision
analysis, not evidence of universal superiority.

Prospective finite screen: 24 dyadic latent mixtures on P in {0,1/4,1/2,3/4,1},
seed 53219, cap H=16, compare the hazard cutoff with every cap's exact payoff.
Verify the variance identity, bounded-horizon value reconstruction, and include
the same-initial-rate counterexample. All priors are supplied in this screen;
statistical learning and source generalization remain open.

[Finite result](retry01.json): all 24 mixtures agree with exhaustive cap choice;
384 variance/hazard identities and 408 survival reconstructions hold exactly.
Observed optimal caps range from zero to eight under H=16. The two models
with equal initial value choose caps six (the imposed example limit) and one.
This supports the stated supplied-mixture mechanism, not learned calibration.
