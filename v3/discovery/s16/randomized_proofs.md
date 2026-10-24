# Randomized proof purchase with a fallible control variate

Codex (GPT-6), October 23, 2026. DEVELOPMENT; early synthesis screen.
Prediction-powered inference and active inference are immediate comparators.

The earlier partial-proof rule pessimistically keeps every unknown loss at
one. A different paid acquisition duty can use model predictions for cases
whose proofs were deliberately not purchased, provided the purchase coin
and its probability are retained. This is not permission to omit hard cases.

Let iid cases X_i have fixed losses Y_i in [0,1], with mean p. Y_i may be a
mathematical property of X_i that is expensive to resolve. Before drawing a
purchase coin, compute mu_i in [0,1] and pi_i in [pi_min,1] from the current
features and past information. Draw A_i conditionally Bernoulli(pi_i), using
independent private randomness. The latent score is

    Z_i=mu_i + A_i*(Y_i-mu_i)/pi_i.                         (1)

Conditioning on the entire current case and pre-coin information gives
E[Z_i|X_i,past]=Y_i, even when mu_i is badly wrong. Thus E[Z_i|past]=p.
The paid policy and coin must really have this semantics; post-hoc propensity
replacement and selecting already-observed labels are not covered.

## Validity with proofs that finish later

Put K=1/pi_min. To test p>=p0 choose lambda_i before the current case,
using past information only, with 0<=lambda_i<=1/(K-p0). The factors

    E_n=product_{i<=n} (1+lambda_i*(p0-Z_i))

are nonnegative and have conditional mean at most one. For a purchased
but unfinished proof retain a sound upper loss U_i>=Y_i, initially one.
Set Z_i^+=mu_i+A_i*(U_i-mu_i)/pi_i. Then

    L_n=product_{i<=n} (1+lambda_i*(p0-Z_i^+)) <= E_n.

Ville bounds the probability of any L_n crossing1/delta by delta. The same
pointwise comparison permits arbitrary completion order, selected historical
prefixes and later sound refinements. No completion-time independence is
needed. Unpurchased cases have A_i=0 and an exactly known score mu_i; the
randomized corrections, rather than assumed truth of mu_i, protect validity.
Store original predictions, propensities and coins. Updating a predictor for
future cases is allowed; rewriting past scores with a fitted new predictor
requires a separate argument. A bet depending on the current features is
not justified by this marginal-risk null merely because pi_i may depend on
those features. Constant bets avoid that additional issue.

The interval score can be negative and exceed one. Applying the old bounded
loss factor with its old range, without the propensity adjustment, is false.
This mechanism estimates a population mean of case losses, not a learned
probability that one fixed unresolved theorem is true.

## A fair asymptotic economic screen

For a fixed predictor and constant pi, let V=Var(Y) and r=E[(Y-mu)^2].
Conditional variance in (1) gives

    Var(Z)=V+(1/pi-1)*r.

Suppose acquiring a feature case and its prediction costs c0, resolving its
loss costs c1, and these prices are fixed for this screen. At a fixed target
variance of the sample mean, the leading total-cost factor is

    (c0+pi*c1)*(V-r+r/pi).

When V>r, the interior optimum is

    pi_star=sqrt(c0*r/[c1*(V-r)]),
    cost_factor_star=(sqrt(c0*(V-r))+sqrt(c1*r))^2,

provided pi_star<=1 and above any imposed minimum. Otherwise clip at the
boundary; when V<=r, full purchase minimizes this expression. A strong
direct-label control need not pay for the prediction: its factor is c1*V.
Writing alpha=r/V and k=c0/c1, the interior method beats that control only if

    k < (1-sqrt(alpha))/(1+sqrt(alpha)),     0<=alpha<1.    (2)

This is an asymptotic variance/cost calculation, not a finite confidence
invoice or measured saving. Finite overshoot, inverse-propensity range,
proof delays, accounting, calibration and setup may remove the apparent
benefit. A fallible estimate of r can guide spending without becoming a
validity premise; it cannot be used to assert an unverified fee reduction.

If a purchased proof is never completed, it retains its pessimistic score.
Treating its predicted loss as a proved upper bound would remove the main
protection. If proof price depends on the current case, use the actual
conditional price and residual structure in the allocation calculation;
the constant-price optimum is then not the claimed optimum.

## Initial disposition

The estimator and betting ingredients are conventional. The prospective
value is an explicit computation/refinement interface that can use cheap
fallible forecasts without completing every mathematical case. Compare
the closest active and anytime prediction-powered formulations before
building a benchmark. No novelty or complete-service benefit is assumed.

The [primary screen](literature.md) found direct prior art. Substituting
e_i(y)=1+lambda_i*(p0-y) into Csillag et al.'s prediction-powered factor
gives (1) and our wealth exactly. With a=1-lambda*(1-p0), b=1+lambda*p0,
their floor pi>=1-a/b=lambda/(1+lambda*p0) rearranges to
lambda<=pi/(1-pi*p0), our condition. At the endpoint pi=1 the source's
strict a>0 condition excludes a zero factor; our elementary proof permits
that harmless boundary. Generic novelty is rejected. Zrnic and Candes
already give the AIPW estimator and variance identity. Only a useful
partial-proof service adapter and its explicit economics remain candidates;
these have not yet been demonstrated against a suitably extended ordinary
implementation.
