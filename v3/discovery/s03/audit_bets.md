# S16: paid audits of revisable value forecasts

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

This branch joins S10's lower-proof censoring with established prediction-powered
e-values. It does not claim a new general statistical method. The target is a
fixed bounded value of an immutable program on iid contexts, not the changing
forecast program's own utility. A forecast may improve while evidence accumulates
about that fixed target; revising the target requires another source contract.

## An elementary specialization

Let X_t be iid and Y_t=g(X_t) in [0,1], with mu=E Y_t. Before X_t is drawn,
choose lambda_t>=0 using only past information. After X_t is seen, a fallible
model supplies b_t in [0,1], and the controller selects audit probability p_t>0.
Draw an independent audit coin R_t with that probability. When audited, obtain
Y_t at its charged computation cost. Define

    Z_t = b_t + R_t (Y_t-b_t)/p_t,
    F_t(m) = 1 + lambda_t (Z_t-m).

Conditional on X_t and the past, E_R Z_t=Y_t. Thus under mu<=m the conditional
mean of F_t is <=1. Nonnegativity is essential: a safe uniform rule is
0<=lambda_t<=p_min when p_t>=p_min>0 and m in [0,1]. A sharper condition for
lambda_t with 1-lambda_t*m>0 is

    p_t >= lambda_t b_t / (1 + lambda_t(b_t-m)).

It follows by checking the smallest audited value Y_t=0; the unaudited factor
is already positive. This forecast-dependent condition can reduce audits where
the forecast is small. The product M_n=product_{t<=n}F_t is a nonnegative test
supermartingale; crossing 1/alpha rejects mu<=m with probability at most alpha.
The betting size must not be selected from current X_t merely because p_t and
b_t can be: weighting the target by current features generally changes its mean.

For p_t>0 the audit-noise variance conditional on X_t is

    Var_R(Z_t | X_t,past) = (1/p_t-1)(Y_t-b_t)^2.

For a fixed forecast/audit rule, total variance is Var(Y)+the expected displayed
term. Accurate forecasts can replace some costly audits with cheap context
processing. Bad forecasts preserve validity but may destroy efficiency. Forecast
and controller costs, all failed audits and the cost of obtaining X remain due.
This variance identity is a design guide, not a finite-sample cost guarantee.

## Checked lower outcomes and delayed refinement

A bounded mathematical evaluator may provide only a checked lower value
0<=L_t<=Y_t, even on an audited context. Set L=0 when unresolved and substitute
it for Y in Z. Every resulting factor is nonnegative and <= its full-outcome
oracle factor. Therefore every partial-evidence product is pathwise <= M_n.
No missing-at-random or truth-independent runtime assumption is needed for this
lower-bound substitution. Never drop a failed audit or change its recorded p.

Later computation may raise an old L_t. Retain the original context, b, p, coin,
betting size and target version; update only its checked lower value. Every
revised prefix product is still <= the corresponding same oracle M_n, so any
threshold crossing remains covered by the original simultaneous event. Refit
future forecasts freely from available past evidence. Do not retrospectively
replace old forecasts or bets with their new fitted values. The full oracle
process uses the actual predictable coefficient history, not a hypothetical
rerun of the controller on complete labels.

The case b=0,p=0 can conservatively skip a context and use Z=0<=Y, instead of
forming 0/0. It no longer gives an unbiased estimator, but retains the one-sided
supermartingale inequality. No such shortcut is valid for arbitrary b>0.

Multiple strategies may share audits using known coins; each must use its actual
inclusion probability. With one shared U_t uniform on [0,1], strategy k can
define R_kt=1[U_t<=p_kt], while the service pays for the union event. Correlation
between wealth processes is harmless for a prospectively weighted mixture.
The actual audit cost is the union probability, not each arm's isolated bill.
Partial lower labels can be shared only when they have the same target meaning.

## Closest primary constructions and scope

Angelopoulos et al., [Prediction-Powered Inference](https://arxiv.org/pdf/2301.09633),
v4 §§1.2-1.4 and Theorem 1, was read for independent model/data requirements and
the prediction-plus-residual decomposition. S08 already recorded the fixed-pool
specialization; repeating it is not a new candidate.

Csillag, Struchiner and Goedert,
[Prediction-Powered E-Values](https://arxiv.org/pdf/2502.04294), v2 §2.1,
Theorem 2.1 and Algorithm 1, directly supplies the corrected-factor construction,
adaptive forecast/collection rules and nonnegative-supermartingale inheritance.
Those are imported ingredients, not claimed here. The working extension is the
explicit connection to checked lower program values and delayed monotone proof
refinement, with immutable target and audit records. Its domination argument
reuses S10/S12 rather than inventing a separate statistical principle.

Next cheap screen: exact finite expectation checks, an adaptive forecast with
truth-dependent censoring, and an explicit cost/quality comparison against full
auditing and the identical ordinary prediction-powered procedure. Do not promote
without a useful actual-evaluator service and a paid model-construction account.

## First executable screen

[audit01.json](audit01.json) preserves 324 exact one-step checks, a five-step
adaptive fair-null tree with 1,024 paths and expected wealth exactly one, and
four delayed refinements of a 96-row frozen history. Partial wealth increases
to the oracle wealth while staying below it. Exact counterexamples show that
choosing the bet after the current label gives null mean factor 5/4, and
retrospectively fitting old predictions only where audits returned labels gives
9/8. An insufficient audit probability allows a negative factor -17/2.

The separate floating developmental simulation uses a supplied 16-context
population with positive fraction 3/4, 32 paths and a 1,024-draw cap. Audit
price is an illustrative unit; each forecast costs .01 units. The direct
control uses lambda=1, the log-optimal bet for Bernoulli(3/4) against 1/2.
Prediction arms use p=lambda=1/4. All capped paths are retained.

| Supplied forecast | Threshold crossings / 32 | Mean capped audits | Mean capped tariff cost |
|---|---:|---:|---:|
| Full audit control | 32 | 29.750 | 29.750 |
| Perfect | 32 | 14.969 | 15.581 |
| Two erroneous contexts | 32 | 28.688 | 29.829 |
| Inverted | 7 | 204.281 | 212.352 |
| Online four-group predictor | 32 | 18.000 | 18.718 |

This illustrates a favorable regime, a near loss and a severe failure. It does
not measure real solver time, paid model construction, empirical coverage or
transfer. The original ordinary prediction-powered method supplies the same
uncensored mechanism. The exact arithmetic screen and floating cost simulation
have different evidential scopes.

## Fallback without a false pathwise promise

A bad model can make the prediction-powered arm fail indefinitely. A direct
full-audit process B and a prediction arm P can be mixed as M=w B+(1-w)P with
fixed w in (0,1). Each process may pause while the other computes, provided its
next context/audit contract remains valid conditional on all shared past data.
Then M is a test supermartingale on the shared operational filtration. A paid
cooperative scheduler can devote at least a fraction rho of computation budget
to B; it reaches any particular B-work budget using at most that budget/rho,
up to a charged indivisible task overshoot. Model inference, checking and
bookkeeping must consume the appropriate worker budget too.

But M>=w B only guarantees crossing when B>=1/(w alpha). It does not guarantee
a constant cost relative to the direct process's earlier 1/alpha crossing on
every sample path. B can cross the lower threshold then collapse or never reach
the higher one. The honest fallback comparison is to the more stringent
baseline, or a separately quantified statistical/power guarantee. Omitting
this significance cost would reproduce a weak-baseline economy claim.

Context-dependent prediction-arm audits cannot automatically be counted as iid
full-audit observations for B. The inclusion rule must remain independent of
the current outcome/context, or B must use its own correct sampling adjustment.
Independent baseline draws may safely train the prediction arm for future
steps. This gives a constructive integration with a real accounting boundary,
not an assumption of free all-policy feedback.

## Which revision is free statistically?

Changing the forecast of a fixed program value is a nuisance-model update;
the predictable correction above already permits it. Changing the program
whose value is being estimated changes Y and its mean. New-program claims need
fresh future samples or an already valid simultaneous source such as S14's
fixed countable family and description prior. A forecast's sophistication need
not itself pay a description penalty in the fixed-target test. Selecting a new
target after inspecting the same outcomes does. This distinction avoids charging
every useful predictive update as a new semantic theory while retaining the
actual post-selection obligation on decisions and program claims.
