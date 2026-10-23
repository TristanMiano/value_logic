# A fallible completion forecast can buy cheaper certification

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 29.
Uses the polynomial-range contract and its miss bound zeta=D/q<1.
No correctness or calibration assumption is imposed on the forecast.

At each probe freeze the current certified span, then draw a fresh point.
Let B_i indicate that the new true residual belongs to that frozen span.
While the span is incomplete, P(B_i=1|past)<=zeta. Fully resolved probes
either add a rank or are redundant. Let j be rank increments and h be
redundancies. A safe baseline with theta in (zeta,1) has wealth

    W_t = a^h*b^j, a=theta/zeta, b=(1-theta)/(1-zeta).

It declares completion when W_t>=1/delta. Stop the latent process when
the true span first becomes complete; its pre-completion wealth is a
nonnegative supermartingale. Thus a false completion has probability at
most delta, even if its declaration time is chosen adaptively.

## Disposable forecast component

A fallible model proposes a time t0 at which the span is likely complete.
It need not supply a proof or a rank upper bound. Set V_t=1 through t0;
after t0 multiply by B_i/zeta at every probe. An outside-span result kills
this component permanently. With fresh probes and the same stopped-null
argument, V is another valid testing process. A fixed mixture

    M_t = (W_t+V_t)/2

may declare completion at M_t>=1/delta. The mixture retains the same
overall false-completion bound. A bad forecast costs power, not validity.
An adaptively chosen t0 is also permitted when the start decision precedes
its first bet; silently selecting the best start retrospectively is not.

Partial receipts replace B_i by sound lower bits L_i<=B_i, initially zero.
Both products are increasing in each bit, so their computed mixture remains
below the latent mixture before completion. Later proof refinements may
restore a provisionally zero forecast component; a genuinely nonredundant
result kills it. Always use the span frozen for that probe. The finite
probe cap below requires each probe to be resolved before drawing the next.

## A concrete guarantee, including a wrong-forecast fallback

Set zeta=4/257, delta=1/1000, theta=1/2, t0=4. For true residual rank r,
the mixture always stops by

    N(r)=r+ceil((log(2/delta)+r*log(1/b))/log(a)).           (1)

Indeed, at that many probes j<=r makes W_t at least 2/delta. Compared
with the baseline's analogous cap, halving its wealth adds at most one
probe here since log(2)/log(a)<1. This cap includes rare false returns;
correctness remains the separate 1-delta event. It is not an exact rank
certificate in the zero-error sense.

If the actual rank is four, (1) is seven. The probability that the first
four probes all increase rank is at least (1-zeta)^4. On that event the
span is complete at four; two subsequent redundant probes make
V_6=zeta^-2>2/delta, so the mixture returns by six. Consequently

    E[T_mixture] <= 7-(253/257)^4, approximately 6.061.

For this same rank, the baseline returns at exactly seven on every correct
return and never before two. Since its error probability is at most .001,
E[T_baseline]>=7-5*.001=6.995. These statements imply a reduction of more
than thirteen percent in expected full-vector probe count against this
specific fixed-theta baseline. They are analytic resource bounds, not a
measured workload gain or superiority over all ordinary stopping rules.

Both schemes use the same residual oracle, degree premise and confidence.
The forecast computation and mixture bookkeeping must cost less than the
saved probes to yield a complete-cost improvement. A conventional forecast-
assisted test implements exactly this mechanism and ties. Proposal/check
and rank-adaptive mixture methods are required strong comparators. In
particular, other theta mixtures can be better for large true ranks; the
fixed-theta comparison is not a universal recommendation.

## Why this serves the broader task

The model contributes a prediction about when mathematical evidence will
be sufficient. Exact receipts and a common statistical event determine
whether that prediction earns useful knowledge. The forecast can be wrong
without changing the guarantee, and its contribution is priced in saved
verification calls. This connects fallible models, unresolved computations,
and reasoning costs without requiring a general learner of mathematical
uncertainty. Mixtures and prediction-adapted betting are established;
the proposed synthesis is this explicit range/correction interface.

The source screen found a particularly close generic antecedent:
Cullen, Montague and Rubinstein, [Halt Fast!](https://arxiv.org/html/2606.27694v1),
Section 4, already combines learned certification mixtures with a fixed
safety component. Therefore reject novelty of that general combination.
The remaining local question is whether the algebraic range/partial-receipt
adaptation, its finite-probe bounds and its correction service form a useful
moderately novel contribution. Neither a different application name nor
the same-model probe alone resolves that question.

## Rank-triggered starts and tunable insurance

The forecast may instead predict rank r_hat. Start V only when that many
independent residuals have actually been acquired. This start is a stopping
time chosen before its first validation bet, so the same proof applies.
If the prediction equals the true rank r, the start's expected time is at
most r/(1-zeta). After that, h_f redundant probes suffice, where

    h_f=ceil(log(1/((1-gamma)*delta))/log(1/zeta)),

for mixture gamma*W+(1-gamma)*V with fixed 0<gamma<1. The baseline guarantees
the fallback cap obtained by replacing log(2/delta) in (1) with
log(1/(gamma*delta)). Thus a correct rank forecast gives expected probes
at most r/(1-zeta)+h_f, whereas its accuracy is never a premise for the
error guarantee. Predictions above the true rank never trigger; the safe
component still terminates. A prediction below it gets just one disposable
attempt. Restarting that component for free after a genuine failure would
invalidate the claim.

For a chosen rank, write h_b for the original baseline's redundancy cap.
Keeping that same cap while funding a faster h_f-step forecast is feasible
whenever

    1/(delta*a^h_b*b^r) + zeta^h_f/delta <= 1.

This inequality states the resource tradeoff between fallback protection
and forecast power. It does not optimize the complete algorithm portfolio.
If the observed rank reaches the known ambient dimension, exact completion
is already proved and every sensible control should stop immediately;
large-rank illustrative bounds with r equal to ambient dimension must not
be advertised as improvements over that elementary shortcut.

## Finite screen

`forecast_probe.py` passed exact rational propagation of 19 true ranks
(0 through 16, 32 and 128), each at three forecast times, plus 19 baseline
cases. The synthetic process has conditional miss probability exactly
4/257 before completion; it checks the bound interface and is not claimed
to be a realized polynomial workload. Its rank-four bound arithmetic is
6.060818365653365 versus 6.995, a guaranteed 13.35499% probe reduction for
the specified comparison. A retrospective best-start counterexample under
a Bernoulli(1/2) null crosses the nominal .1 threshold with probability
0.89703 over 64 draws, demonstrating why choosing starts after seeing
their future is prohibited.

Source SHA-256:
`9a307f1806c8e64eae3f1cde03a1f9e6a7e8950e2dde542ef9ce0591bd609ee3`.
The measured probe runtime is 60,786,700 ns. This is developmental evidence;
the same model supplied both the argument and the executable checks.
