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

## Precision floors and hard evidence: additional derived boundary

On a tape of true queries and a library containing a constantly wrong zero
expert, all product/fixed-state weights remain positive. Therefore the raw
mixture p_t<1 on every finite round. Downward dyadic rounding forces
q_t<=1−2^(−h), so every unbought randomized action has conditional error at
least 2^(−h). Fixed h alone therefore permits at least (T−m)2^(−h) expected
terminal mistakes even when L*=0. With fixed-mass weights, the wrong constant
expert has at least mass 1/M, so the lower bound improves to
(T−m)*max(1/M,2^(−h)). It applies for every selector path on this repeated
true-query tape. It is an asymptotic construction for growing admitted
horizons, not a claim that the current executable accepts T>8192.

The restricted service realizes a true repeated input with p=17,a=1. Its
public experts are (0,1,1,1); no empirical error search is needed. This shows
why constant-in-horizon ideal-regret language cannot describe a fixed h,s
implementation indefinitely, even though the finite allowance is small.
A sound retained-answer override removes this specific repeated-known-answer
problem while preserving the raw learner's purchased-label update theorem.
Actually integrating such a hard state remains P3-08.

## Forecast and action objectives have different trivial baselines

For every binary answer, the fixed forecast q=1/2 has Brier loss 1/4. Thus its
all-issued score is exactly T/4 without any label knowledge. A selective
learner's Brier theorem against fixed binary experts need not beat this
fractional constant. This analytic baseline was identified during analysis;
it is a post-run diagnostic, not a prospectively deployed comparison arm.
For the same selector positions, fair-coin unbought actions have conditional
expected terminal loss (T−m)/2. Any performance difference from this null
must retain the proper action versus forecast objective and paid-bill scope.

If one additionally posits an external coherent subjective truth probability
p, an independent action lottery with Pr(action=1)=q has expected 0–1 loss
q+(1−2q)p. That scalar identifies p only when q!=1/2 and the loss/stake model
is known. At q=1/2 it is identically one-half and carries no truth-probability
information. Under independent correction probability pi, known c>0 and
known other fees, the variable part is c(1−pi)[q+(1−2q)p]. The same
nonidentification holds at pi=1 or q=1/2. This is an explicitly conditional
valuation identity, not a new subjective probability law for the mathematical
inputs and not a way to interpret a regret upper bound as a probability.
