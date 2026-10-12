# S11: counterfactual diagnostics that change the target

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; S04 lineage, Q2/Q3/Q4.
This is a constructive boundary case and proposed state-aware repair, not a
new POMDP principle or a positive-objective promotion.

## Pure information is an additional premise

The earlier decision-region construction assumes each diagnostic reveals a
fixed function of the latent model and leaves its terminal action-loss vector
unchanged. That is appropriate for paid computation about a fixed object.
It is not automatic for an actual intervention on a stateful program. Restoring
a function binding need not restore caches, copied references or other state.
Such a diagnostic has both information and intervention effects.

Consider a black-box predictor with one of three stipulated mechanisms:

- live: calls the currently bound actor function each time;
- cached: caches its first returned actor value and then reuses that value;
- frozen: retains an original function that always returns zero.

The actor action a is either 0 or 1. A terminal call to the predictor returns
p, with loss c(a,p)=10*p−a. Initially the cached predictor is empty. The initial
loss vectors for actions (0,1) are (0,9) for live and cached, and (0,−1) for
frozen. Under a stipulated uniform prior over these three mechanisms, immediate
action 0 has expected loss 0; action 1 has expected loss 17/3.

A diagnostic binds the actor to 1, calls the predictor once, records the result,
then restores the actor binding to 0. Assume zero computation price solely to
isolate the state effect. Result 0 identifies frozen; result 1 leaves live or
cached. A pure-information planner would then choose action 1 after result 0
and action 0 after result 1, forecasting expected terminal loss −1/3.

Actually the diagnostic leaves cached with stored value 1. Following that
policy gives losses −1 for frozen, 0 for live, and 10 for cached: expected loss
3. Even an additional zero-price observation at restored actor 0, which
distinguishes live from cached, only permits losses −1,0,9, with mean 8/3.
More identification did not undo the intervention's harm. The optimal choice
in this small menu remains immediate action 0 with loss 0. If a reliable cache
snapshot/restore operation is actually available, priced and included in the
diagnostic, the pure-information calculation can become appropriate again.

Live and cached have identical initial action values, yet cannot be merged
for diagnostic planning: their post-intervention states differ. A representation
sufficient for the current value query need not be sufficient for choosing
future computations. This gives an explicit programming counterpart to the
problem contract's propagation-mask and operation-kind requirements.

## A criterion-specific preservation certificate

Let a covered finite model h have current state s and terminal action costs
c_h(s,a). A diagnostic e yields observation o and successor state T_h(s,e).
If the checked model gives

    c_h(T_h(s,e),a) = c_h(s,a) + b_h(s,e,o) for every terminal action a,

then that diagnostic preserves each model's *regret vector*: subtracting the
model's best terminal cost cancels b_h. Decision-region intersection for a
fixed regret tolerance can therefore use the same regions after restricting
to models consistent with o. Its complete utility bill must still include the
state-change offset, as well as computation/reset costs. Equal regret regions
alone do not certify that buying the diagnostic is beneficial.

For expected loss under a fixed updated prior, the additive offset is also
independent of the terminal action and cancels when comparing those actions,
but must be charged in the earlier choice of diagnostic. For worst-case loss,
a model-dependent offset can even change the preferred terminal action:
costs (0,1) and (2,0) favor action 1 before offsets; adding 100 to both costs
of the first model makes action 0 minimax. Thus a preservation certificate must
name the consumer criterion, not merely say that values share a shift.

When this condition fails, retain successor states and solve the finite
belief-state control problem. The diagnostic may be useful, harmful or
unaffordable; it is not a pure partition of a fixed loss table. A finite
state/transition table and a conditional model-coverage premise make this
repair executable. They do not learn real counterfactual semantics for free,
justify a chosen prior, or define a genuine mathematical counterpossible.

Next cheap screen: implement the three mechanisms, compare pure-information
and state-aware policies, and verify that a paid snapshot/restore variant has
the advertised different behavior. Compare ordinary finite-horizon POMDP
planning; no broad empirical learning claim is intended by this example.

## Executed toy and stronger continuation error

[stateful_probe.py](stateful_probe.py) executes actual mutable bindings/cache
state and enumerates all observation-to-action policies, using exact rational
priors. [stateful01.json](stateful01.json) reproduces the uniform-prior forecasts
and actual costs above. The initial prose mistakenly gave 7/3 rather than
(9+9−1)/3=17/3 for immediate action 1; this arithmetic error is corrected here
and does not change the immediate optimal action or any diagnostic comparison.

With prior (live,cached,frozen)=(1,38,1)/40, the pure-information one-probe
policy still chooses action 0 on observation 1, predicting −1/40 overall.
Its actual expected cost is 379/40. The state-aware continuation chooses action
1 on that observation and costs 35/4 overall. Both are worse than immediately
choosing action 0. This separates a wrong purchase decision from a wrong
terminal continuation; the uniform case only exhibited the former.

A complete snapshot/restore probe costs −Pr(frozen)+its price in these two
priors. Thus its purchase is favorable exactly when its price is below 1/3
or 1/40, respectively. The prototype explicitly restores the cache as well as
the binding; no real-world ability to discover or restore all state is inferred.

## Approximate preservation

Write d_h(a)=c_h(T(s,e),a)−c_h(s,a) and let omega_h=max_a d_h(a)−min_a d_h(a).
The change in the best action's cost lies between min d_h and max d_h: apply
each bound pointwise before minimizing. Therefore each action's regret changes
in absolute value by at most omega_h. The same argument applies to mixtures
of terminal actions, whose expected d_h lies in that interval. An old robust
epsilon-regret certificate transfers to epsilon+max_h omega_h over the retained
models. A common offset has omega=0; bounding absolute cost change alone can
be unnecessarily pessimistic. Computing a useful omega bound is an additional
paid semantic analysis, not a free oracle supplied by this inequality.

## Primary comparison scope

Cassandra, Kaelbling and Littman, [AAAI 1994, pp. 1023–1025](https://cdn.aaai.org/AAAI/1994/AAAI94-157.pdf),
explicitly model both environmental effects and information, with transition
and observation functions, Bayesian belief updates and expected rewards in the
belief-state process. This is the direct conventional repair. The 1998 journal
article's author PDF failed retrieval because it exceeded the tool size limit;
only its abstract was accessible, so no detailed 1998-section comparison is
claimed. The next [continuation construction](continuation.md) is an adaptation
within ordinary finite belief-state planning, not an alternative to probability.
