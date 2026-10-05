# F14 design arguments and adverse cases

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 4, 2026.
Status: development reasoning; the final protocol/configuration determines
the prospective evaluation contract. No final evaluation data are used here.

## 1. Numeric information and a useful decision are different consumers

Let P be the nonempty probability-law fiber compatible with the information
actually retained by a method. For an order a, its revised mean cost C_a(p)
is affine in p. The exact ordinary reference returns

    l_a = min_{p in P} C_a(p),  u_a = max_{p in P} C_a(p).

A point answer is exact only when l_a=u_a. Without that equality, the midpoint
has the optimal worst absolute error for that scalar query, (u_a-l_a)/2:
every answer must be at least half the endpoint distance from one endpoint,
and the midpoint attains that bound. Thus tolerance tau admits a midpoint iff
u_a-l_a <= 2 tau. Numerical closeness on the generating law alone does not
justify an answer for all laws compatible with the method's information.

These independently sharp intervals do not imply that their midpoint vector
comes from a single joint law (C4 already supplies a counterexample). Decisions
must consequently use a common law fiber, not compose convenient endpoints.
For finite action set A, including a declared constant-cost fallback f,

    R_P(a) = max_{p in P} [C_a(p)-min_{b in A} C_b(p)]
           = max_{b in A} max_{p in P} [C_a(p)-C_b(p)].

The second equality follows by commuting two finite/compact maxima. Each
inner problem is an ordinary linear program over the SAME P. Minimize R_P(a)
with the frozen lexicographic tie rule; accept a regret claim only if its exact
bound is at most epsilon. A certified fallback choice is distinct from refusal
followed by executing the fallback. The latter still incurs its realized loss
and regret and is never relabeled a successful certified choice.

For old unit attempt cost 1, tau=epsilon=1/20 means five percent of one attempt,
and two percent of the stipulated fallback cost 5/2. This is a transparent task
preference, not an empirically discovered threshold. A single price edit of
1/40 leaves any old-optimal action within 1/40 regret under each compatible law
when the complete old mean vector is known: each action's cost changes in an
interval of width 1/40, so old optimality bounds its new disadvantage by that
width. This is a useful sufficient-information regime even when numeric exact
recovery fails. A unit price edit tests the different regime where refusal or
paid acquisition may be necessary. Both signs of an edit keep prices positive.

The final generated cases must include sufficient and insufficient regimes;
the prior C4 examples remain development diagnostics. A passing exact theorem
fixture cannot by itself establish application frequency or performance.

## 2. Information, storage, and an acquisition oracle

An algorithm which can inspect the original law has retained that information
somewhere, even if its named summary is small. The experiment must expose a
restricted method only to its serialized retention payload, current request,
and authorized acquisition interface. Reference truth is for scoring outside
that interface. Resident bytes, archive bytes, source-schema bytes, proof bytes,
and source/measurement counts are reported separately. An archive available
to fresh solving is charged; an external archive is not free compression.

Acquiring an exact mean is a stipulated oracle operation, not a sampled
population estimate. Its charge and transcript belong to the result. C4's
two-new-means reconstruction uses substantial exact old information and does
not demonstrate cheap real-world data acquisition. Source drift invalidates
old-law reuse unless the current context explicitly supplies a valid relation.
Fresh current acquisition may restore an answer; paying for it is part of the
comparison. Synthetic generation cost and the price of an empirical query are
different quantities.

Measured CPU time, serialized bytes, query counts, and action-loss units form
a resource vector. Add them only after declaring a conversion. A break-even
update count can compare setup plus repeated update times on a fixed frozen
revision schedule; it is not a speed claim outside the measured implementation,
and an eventual strict win requires a positive per-update saving, or equal
update cost with a strictly cheaper setup. With a negative saving, a cheaper
setup can still win at small horizons before losing later; report those
horizon values and do not call them eventual amortization. The F14
implementation projects one measured event rather than measuring a
repeated-update schedule.
Acquisition-price sensitivity is reported in the declared task units separately.

## 3. A scalar-output ReLU network imposes a specific causal hypothesis

Write h(x)=ReLU(Wx+b) and logit z(x)=v^T h(x)+b_out. Replacing a hidden subset S
of base b with donor d gives

    z_I(b,d) = z(b) + A_S(d)-A_S(b),
    A_S(x) = sum_{j in S} v_j h_j(x).

For the F04 task, the independent high-level model has

    z_H(x) = log J0(x)-log J1(x).

If the unperturbed network fits this model exactly, exact J0-only interchange
for every base/donor pair requires

    A_S(d)-A_S(b) = log J0(d)-log J0(b).

Fixing b shows A_S(x)=log J0(x)+constant. The analogous J1 subset contributes
-log J1(x)+constant. Thus affine decodability of raw J0/J1 is not the sufficient
mechanistic condition. The intervention test measures the output contribution;
the expected-cost decoder is only a separately reported diagnostic. A finite
ReLU representation is piecewise affine, so exact equality to these logarithms
on an open domain is unavailable in general. The bounded probe must have an
explicit approximate criterion, with learning error reported separately.

Probability-level interchange error includes base prediction error. Also
report the error of the observed change relative to the predicted change:
(p_I-p_base) - (p_H-p_star_base). This prevents a good-looking effect from hiding
poor task learning, or poor task learning from being mislabeled evidence that
one particular internal explanation is false. It does not remove the required
absolute-interchange criterion.

## 4. Two different scale freedoms

Positive neuron rescaling multiplies a hidden activation by s_j>0, its incoming
weights and bias by s_j, and its outgoing weight by 1/s_j. A permutation carries
the neuron index, subset membership and decoder coefficient together. The
network and TRANSPORTED intervention are algebraically unchanged. The test
must transport a fitted explanation with no refit; numerical discrepancies
are subject to an independently frozen floating-point tolerance.

By contrast a positive input-dependent g produces J0'=gJ0 and J1'=gJ1 with
the same observational p*. J0-only interchange changes to

    g(d)J0(d) / [g(d)J0(d)+g(b)J1(b)].

This equals the original prediction iff g(d)=g(b). Constant g=2 is an invariant
high-level control; g=1/eta and g=1/(1-eta) are serious competing factorizations
because they assign the shared outcome-probability dependence differently.
Each receives equal alignment capacity and search effort. Merely fitting the
observational task cannot establish absolute expected-cost scale. If competing
predictions are too close on the frozen pairs, the correct outcome is unresolved
discrimination, rather than choosing the explanation with a favorable label.

The fourth frozen hypothesis is `g=1/(J0+J1)`, giving `(p*,1-p*)`. For role zero
its counterfactual is `p*(d)/(p*(d)+1-p*(b))`; it is the direct competing
normalized-probability interpretation of ordinary classifier computation.
It replaces the development draft's illustrative `exp((x1+x2)/2)` scale
before freezing, on conceptual grounds rather than trained-model comparisons.
The latter's general cancellation issue remains: with unrestricted,
network-dependent `g=exp(A_S)/J0`, a subset can be named as a scaled cost
tautologically. The four fixed network-independent functions bound that
interpretation problem without claiming to exhaust every scale.

Equal coordinate capacity need not mean equal approximation difficulty:
normalized log-costs include a coupled `log(J0+J1)` term. Failure to find a
normalized alignment cannot by itself select the absolute-cost description.
The primary scale contrast therefore uses the **same identity-selected
intervention** against each rival prediction; separately searched rival
alignments are additional evidence with their full budget disclosed.

## 5. Search, evaluation, and statistical scope

Network training labels are sampled outcomes Y only; expected costs are used
after training for interpretation development. Candidate pools, scores, selected
subsets, affine decoders and competing-scale selection must be serialized and
hashed before generating evaluation pairs. A held-out test examines the one
frozen candidate per declared hypothesis. It does not need a multiplicity
factor for every candidate tried only on development, but simultaneous claims
about roles, strata, models, scales and controls need an explicit family.

Independent donor/base draws are the sampling units. Reusing every pair from a
small input batch does not create quadratically many independent observations.
Fixed trained seeds are replications of this bounded pilot, not a sufficient
sample for general claims about all training runs. Conditional-on-frozen-model
error bounds concern the stipulated pair generator only. Negative results can
mean task underlearning, failure of this coordinate-subset explanation,
insufficient discrimination among explanations, or numerical/protocol failure;
these must receive different dispositions.

Exact numeric thresholds, finite claim families and generator details are
finalized in the protocol after development validation, before any evaluation.

## 6. A matched-capacity positive calibration is analytically feasible

For `f(t)=log(t)` on a positive interval `[a,b]`, its linear secant `l(t)`
underestimates `f`, and the interpolation remainder gives

    0 <= f(t)-l(t) <= (b-a)^2/(8 a^2).

Use four geometrically spaced intervals for each of `log(cFN)`, `log(eta)`,
`log(cFP)` and `log(1-eta)`. A continuous four-piece secant function has one
positive linear-input ReLU and three hinges. Two log functions per role thus
need eight coordinates, with sixteen active coordinates in the allowed
32-unit network. The remaining output weights are zero. Constant offsets live
in the output bias and cancel correctly when a role's varying contribution
is substituted from a donor.

Write `B=((sqrt(2)-1)^2+(3^(1/4)-1)^2)/8`, the sum of the two conservative
log-interpolation errors for a role. Both role log-cost approximations
underestimate their targets by values in `[0,B]`. The full or intervened
logit error is their **difference**, hence has magnitude at most `B`, not
`2B`. Since sigmoid has derivative at most `1/4`, its probability error is
uniformly at most `B/4`, which is less than .01. The executable calibration
adds `1e-12` numerical slack and tests its known subsets on all five strata,
gauge transport and two-donor composition.

This establishes representational feasibility for a deliberately compiled
positive control at the selected width and subset capacity. It does not show
that ordinary outcome training discovers those units, that a 128-proposal
search finds them, or that the competing controls will lose. Those remain
separate prospective questions.

## 7. Unknown law plus known mean is not enough for the application example

A multiple-vertex law fiber can still determine a particular current mean
exactly. For example, increasing the price of the first attempted procedure
adds a known constant to its known old mean. Counting that alone as the
uncertain-information use case would miss the numerical approximation
question. The final useful-application criterion therefore requires at least
one useful selective/no-reacquisition row whose **selected cost interval is
non-singleton and admitted as an approximation**.

Here is an analytic feasibility witness, permanently development. Under the
uniform three-bit law, all old unit-price order costs are `9/4`. The compatible
old-profile fiber contains the following exchangeable perturbation of the
lexicographic eight-world probability vector:

    p(t) = (1/8,...,1/8) + t*(6,-3,-3,1,-3,1,1,0),
    -1/48 < t < 1/24.

Every coordinate remains positive. Marginal, pair and triple failure moments
are respectively `1/2-t`, `1/4+t` and `1/8`. Their combination
`1 + marginal + pair + 4*triple` stays `9/4` for every order. With a positive
procedure-2 price change `delta=1/40`, putting that procedure last changes
its mean by `delta*(1/4+t)`, which varies on this fiber.

More generally, equality of the six old means forces all marginal failure
moments to agree and all pair moments to agree. Pair reach probability is at
most marginal reach probability, which is at most one. Thus a last-position
procedure-2 order minimizes the new mean for every compatible law: its robust
regret is zero. Its interval has nonzero width at most `delta`, and its upper
cost is at most `9/4+delta`, comfortably below fallback minus `1/20`.
Meaningful approximation and a useful revised decision can therefore coexist
without exact recovery. This is a sufficient construction, not a promised
evaluation frequency or a new generic policy-regret result.

## 8. Limits of interpreting intervention agreement

The [focused source analysis](../literature/07_f14_protocol_sources.md)
constructs a two-unit cancelling pair with exact one-role cost interchange
and no net ordinary contribution. Its purpose is to distinguish the frozen
partial intervention relation from a stronger ordinary-necessity claim.
It is not the original F14 training population, not a learned result, and not
a demonstration that the full matched-control statistical gate would pass.
It supplements the unused-zero-output-weight witness without adopting a
blanket rule that every nullspace component invalidates an explanation.
