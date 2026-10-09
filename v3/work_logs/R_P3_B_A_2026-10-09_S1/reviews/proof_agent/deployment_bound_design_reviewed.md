# Deployable bounds and finite precision: prospective derivation

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Task R-P3-B-A, DEVELOPMENT, principal D/X work.

## Remaining question

The saved experimental certificates may use the private evaluator's all-tape
best-expert loss L*. That is a valid retrospective theorem evaluation, but a
live learner has not computed L* when it admits the job. Derive a numerical
label-free envelope from source-known expert structure and finite capacities.
This is still the selected selective-feedback service, not P3-08 integration.

## Candidate answer

Because the fixed four-expert library contains constant zero and constant one,
L_zero+L_one=T for every binary tape. Therefore L*<=T/2 without purchasing a
single label. The two-expert argument alone establishes this upper bound; it
is not an evaluator query and does not estimate the actual number of ones.
Substitute T/2 for L* in the uniform and adaptive terminal-loss theorems, then
clip at the deterministic maximum T−m. For uniform B=2, the first-order term
is 3T/8; for B>=4 it is T/2. Add the independently priced source/setup envelope,
controller envelope, development random-source allowance and 1088m query
reservation. This gives a conservative source-known expected all-in cap. The
actual resource cap also gives the pathwise expenditure bound, while terminal
mistakes are bounded pathwise only by T−m.

A finer L* bound from exact labels remains private retrospective evaluation
unless that extra evidence is itself admitted and paid. A posterior forecast
or a trained prediction about L* cannot replace a certified bound silently.

## Precision design before execution

Let A=(B−1)mK in the uniform rule, or A=HmK in the adaptive rule. For a desired
additive state allowance epsilon_s>0, choose integer s>=1 with
2^s>=1+A/epsilon_s. For action allowance epsilon_h>0 choose integer h>=1 with
2^h>=(T−m)/epsilon_h. These choices guarantee A/(2^s−1)<=epsilon_s and
(T−m)/2^h<=epsilon_h, subject to the executable limits s,h<=32.
For the four-expert fixed state, h>=s+2 removes the action-rounding term
entirely. Compare the actual bit and arithmetic tariff before selecting that
alternative: exact dyadic action probabilities do not make the bit source free.

Only the weight state is independent of T at fixed s. The implementation
retains a finite preloaded bit tape and emits every record; those resources
scale with T. Avoid calling it a constant-total-memory algorithm.

## Adaptive pre-issued forecasts

The adaptive update estimates the unbought objective, not the all-issued
forecast objective. The uniform B-factor identity cannot be reused. A safe
simple upper bound follows by adding at most one ideal mixture loss per
purchased position: all-issued ideal mixture loss <= terminal ideal mixture
loss+m for each selection realization. Therefore the adaptive pre-issued
Brier bound is at most
L*+HK log N+HmK/(2^s−1)+m+2T2^(−h), clipped at T.
The proof uses Brier<=ideal mixture loss and the 2-Lipschitz rounding bound.
No action-sampling allowance should be added on top of that same Brier
rounding argument. The actual issued probabilities are recorded before
receipt feedback and their score is never corrected retroactively.

## Intended finite checks

Before any new calculation, record the parameters: all allowed power-of-two B,
T at representative boundaries 2,8,64,992,3968,8192 where divisible, N=4,
state/action precisions 1,2,8,16,32, and epsilon_s=epsilon_h=1 for the
precision-choice calculation. Check the exact integer ceilings rather than
floating-point log decisions. No new random or query experiment is required;
this calculation verifies parameterization and displayed certificate bounds.
