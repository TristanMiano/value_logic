# What the disagreement/fee heuristic would need to optimize

Contributor: ChatGPT (GPT-6 Astra Pro), October9,2026 UTC.
R-P3-B-A, additional D/R interpretation of the executed adaptive selector.
This is a conditional mathematical illustration, not a new policy or experiment.

## Immediate correction, information value and the quota

For one last block with frozen prospective-action error probabilities d_t,
known fees f_t, task-error price c and primitive price lambda, expected
terminal loss plus purchase fees is

sum_t c*d_t + sum_t pi_t*(lambda*f_t-c*d_t).

Under one required purchase and a common floor pi_t>=epsilon, the linear
objective assigns every remaining probability mass to a position maximizing
c*d_t-lambda*f_t. With B positions, pi_t=epsilon for all but the maximizer,
which receives1-(B-1)epsilon. This is the ordinary simplex linear programme;
it is not an implementable free oracle when d_t or fees remain unknown.
It also omits the effect of a paid label on later blocks' learner state.

If an external coherent belief p_t about y_t is supplied, the lottery q_t
has expected error dbar_t=q_t+(1-2q_t)p_t. Only with the additional equality
p_t=q_t does this become2q_t(1-q_t), twice weighted disagreement. The
executed mixture q_t was not established as a coherent calibrated truth law.
Thus disagreement's use as expected immediate value already needs an
extra model premise. It may instead guide learning, but that future benefit
is another quantity, not supplied by the quota-regret proof.

Even under p=q and exact known fees, maximizing disagreement/fee need not
minimize the fixed-quota net objective. Take B=2, c=1, lambda=1/10,
q=p=(1/2,1/4), f=(2,1), and floor epsilon=1/4. These are supplied model
parameters, not measured fees or an empirical mathematical truth law.
The variance/fee ratios are1/8 and3/16, so the ratio favors position2.
The net correction values are3/10 and11/40, so the true last-block objective
favors position1. Assigning probability3/4 rather than1/4 to the better
position improves the model's expected objective by exactly1/80.
No labels, rates or seeds were run to obtain this arithmetic witness.

A benefit/cost ratio can arise in a different fractional-budget allocation
problem. It is not interchangeable with this exactly-one-query constraint,
which has a price-weighted net objective. The implemented adaptive rule
also uses source-informed fee proxies rather than exact future invoices.
Its proof guarantees controlled feedback and regret, not the optimality
of this acquisition heuristic. The existing negative table/null comparisons
remain the actual service evidence.

## Consequence for the next integration

Keep a policy's acquisition purpose and objective explicit: immediate action
correction, information for later forecasts and narrower self-performance
intervals are different goals. Retain the same ordinary computations and
prices when comparing them. Do not rename disagreement as learned value of
computation without evidence for the required truth/fee/future-state model.
P3-08 may integrate the existing bounded rule without claiming such optimality;
no new policy or recurrence is selected by this note.
