# Reoptimizing after an edit is a different decision duty

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass21.
An early comparison screen for the numerical receipt family.

For scalar t>=0, edit bound e>=0 and loss (1-N*x)^2+x^2, distinguish

    V = max_{|N-t|<=e} min_x [(1-N*x)^2+x^2],
    W = min_x max_{|N-t|<=e} [(1-N*x)^2+x^2].

V asks for the worst best-attainable value after an edit, allowing a newly
optimized action. W requires one action before learning the edited model.
They are different contracts, even though both use ordinary optimization.

Direct scalar minimization gives V=1/[1+(t-e)_+^2]. For W, negative x
cannot improve on x=0, so write

    W=min_{x>=0} (|1-t*x|+e*x)^2+x^2.

If e>=t then W=V=1. Otherwise set a=t-e>0. On0<=x<=1/t the objective is
(1-a*x)^2+x^2, whose unconstrained minimizer a/(1+a^2) lies in the interval
exactly when a*e<=1. On x>=1/t the objective is((t+e)*x-1)^2+x^2 and is
increasing from that boundary. Consequently

    W = V                         if a*e<=1;
    W = (1+e^2)/t^2              if a*e>1.

In the second case,

    W/V = 1 + ((a*e-1)/(a+e))^2.

For t=3,e=1, V=1/5 while W=2/9. For t=20,e=10, V=1/101 while W=101/400.
The ratio can grow without bound by taking a=e large. This is not a
speedup or a superiority result: W buys robustness of a single precommitted
action, a stronger duty. It would be misleading to compare the scalar
transport envelope to W and call the smaller number a new optimization gain.

The receipt family principally estimates counterfactual optimal values.
It can support a decision about whether an edit is worth exploring without
yet finding the new optimizing action. If the intended application requires
actually deploying that optimizer, its acquisition and solution costs must
be added. Conversely, a one-action robust controller should be assessed
against W, not credited with V by assuming free post-edit reoptimization.

The elementary minimax distinction is established mathematics. This pass
retains a concrete guard against an unfair baseline and keeps the intended
counterfactual use explicit; no new family, novelty or readiness is claimed.
