# Sound constraints can choose the next randomized proof query

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass43.
Fixed mathematical truths need no iid interpretation in this construction.
The novelty of the proof interface, rather than the martingale, is open.

Let fixed Y in {0,1}^N mark false claims. Test H0: sum(Y)>=S0.
Before each query, sound proofs and already acquired outcomes describe a
set K_t containing Y. It may be a tractable relaxation of the Boolean set.
Choose a distribution q_t on catalogue indices, then independently sample
I_t from it. The selection and all solver work are paid. Acquire Y_(I_t).
Any certified lower bound

    a_t <= min {q_t^T z : z in K_t, sum(z)>=S0},   0<=a_t<=1

supports the factor

    1 + lambda_t*(a_t-Y_(I_t)),
    0<=lambda_t<=1/(1-a_t),                       (1)

when a_t<1. The product is a nonnegative supermartingale under H0:
conditional on all prior observations and proofs, the newly randomized
index has expected truth q_t^T Y>=a_t. Its crossing of1/alpha has error
probability at most alpha. An empty certified null-feasible set permits
deterministic rejection. If a_t=1, a sampled zero directly contradicts
the null; a sampled one carries no evidence.

Proofs may depend adaptively on the entire computation history and reveal
unsampled truths. They must be sound, and the next index must actually be
drawn from the declared q_t after it is selected. This conditional argument
does not require exchangeability, random truths, a calibrated forecast or
a fixed solver schedule. Approximate optimization needs a certified LOWER
bound on this minimization. A feasible minimization incumbent is an upper
bound and is unsafe in(1). Checker error needs a separate allowance.

For a fallible forecast with predicted query failure rate p<a, maximizing
predicted log growth in(1) gives lambda=(a-p)/(a*(1-a)) and growth
KL(Bernoulli(p)||Bernoulli(a)). This can guide q and computation purchases
per unit cost, without making the guarantee depend on the forecast's
accuracy. It supplies no regret or optimal-allocation theorem. Repeatedly
querying a known truth cannot create actual information: its certified
lower bound never exceeds the already known query expectation.

## A small certificate changes which observations suffice

Two disjoint blocks have1000 fixed claims each. A sound aggregate proof
shows the expensive block has at most10 failures. Test whether the full
catalogue has fewer than100 failures. Under H0, the cheap block has at
least90. Sample only the cheap block without replacement. After t zeros,
the zero-alternative likelihood ratio is

    E_t = (1000)_t/(910)_t.

At t32 it exceeds20, so32 inspected cheap truths suffice on this outcome
path for a5% test. Without the aggregate certificate, observing arbitrarily
many zeros in just the cheap block cannot refute H0: all100 failures can
be in the uninspected expensive block. Uniform sampling of the entire
catalogue would instead use (2000)_t/(1900)_t on its all-zero path.

The certificate's price and the actual failure distribution matter. There
is no empirical saving here, nor a guaranteed32-query stopping time.
Conventional stratified sequential testing given the same certificate is
the strong equal-information control. A useful application would need an
aggregate theorem cheaper than resolving its expensive block individually.

## Counterfactual scope

If a checked program edit proves that at most b catalogue truth values can
change from0 to1, any sound upper confidence sequence U_t for the old total
gives min(N,U_t+b) for the edited total on the SAME coverage event. An edit
selected after seeing the data is allowed when its deterministic change
bound is sound for every selected edit. Reusing an old e-value at an
unchanged null threshold is not generally valid. Unknown semantic changes,
new catalogue entries and out-of-catalogue generalization are not covered.

The partial-proof/stochastic-audit connection advances the intended use of
unresolved mathematics; the probability and decision machinery is ordinary.
It is a candidate formal adapter, not evidence that ordinary methods cannot
express the same mechanism.

The exact all-zero-path calculation in [edit_kernel_probe.json](edit_kernel_probe.json)
gives first crossing32 with the aggregate proof (wealth21.5011), versus58
for uniform sampling of the full catalogue (wealth20.4787). These paths
have different acquisition information and do not establish an expected
cost ratio; the proof's price remains unpaid in this constructed comparison.
