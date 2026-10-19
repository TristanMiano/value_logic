# Priced graphic recovery with exact and fallible answers

Codex (GPT-6), s12 DEVELOPMENT derivation; not yet independently probed.
Connects Q1/Q3/Q4/Q5 through the earlier graphic invoice adapter. The
optimization ingredients are ordinary minimum cuts, LP duality and risk budgets.

## Fixed-instance interface and a distributional error contract

Let hidden edge bits satisfy a checked graphic equation A*x=b over GF(2),
where A is vertex-edge incidence. For a non-loop target edge t=(u,v), any
u-v cut U gives the exact identity

    x_t = b(U) XOR parity_(e in delta(U) without t) x_e.

Each other edge e has an exact acquisition routine with a justified expected
fee bound w_e, valid for every fixed input. It may also have supplied fallible
predictors j, with evaluation fee a_(e,j)>=0 and valid marginal error bound
epsilon_(e,j). Predictor failures need not be independent. Calibration and
source validation are additional preparation costs; supplied numerical bounds
are not obtained for free by calling a model confident.

Before seeing this instance's predictor outputs or errors, choose a cut and,
for each of its non-target edges, either the exact routine or one predictor.
XOR those answers with the known offset. Its mean acquisition/evaluation bill
is bounded by the sum C of chosen fees, and its error probability is at most
the sum R of the chosen predictor error bounds. R is deliberately an uncapped
union-bound certificate. This guarantee is marginal over the stated task
population and procedure randomness, not conditional on observed model values.

The exact expected routine can use the earlier cap-two invoice construction:
query e and orient its cheapest marker by a fair bit. Then
w_e=c_e+(1/2)*min_(i!=e)c_i, excluding explicitly separate episode/coin costs.
For a predetermined set of edge acquisitions, one shared orientation coin
suffices for these mean fees. Its price, if nonzero, is a method-level charge.
Hard-worst prices instead yield a different resource objective and must not
silently be substituted for these expected prices.

## A global certificate from one ordinary minimum cut

Fix lambda>=0 and assign each non-target edge the capacity

    k_e(lambda)=min(w_e, min_j[a_(e,j)+lambda*epsilon_(e,j)]).

The minimum u-v cut in G without t minimizes C+lambda*R over every declared
cut method and every per-edge exact/predictor choice. Direct exact target
acquisition, supplied direct target predictors and a fair random guess can
be included as additional methods with their own (C,R) pairs. A fair guess
has R=1/2 for every fixed truth and costs its random-bit/implementation fee.

Let z(lambda) be the minimum of the cut value and those additional methods.
Every mixture of these methods with average certified risk at most alpha has

    average certified fee >= z(lambda)-lambda*alpha.

Indeed each method obeys C+lambda*R>=z, and averaging preserves the inequality.
A minimum-cut/max-flow certificate plus the listed direct comparisons thus
certifies the lower bound without enumerating all cuts. If one feasible method,
or a mixture of two tied methods, attains it, that construction is optimal for
this **certificate-accounting class**. It need not minimize actual worst-case
error risk: union bounds and averaging separately valid risks can be loose.

For a finite set of methods, the fee/risk LP has an optimum supported on at
most two methods, except for immaterial ties. Column generation can alternate
the small mixture LP with the minimum-cut separator. It terminates in the
finite class, but no strongly polynomial iteration bound is claimed. A useful
stopping certificate can be much smaller than the entire class.

## Worked instance with a checkable resource/risk tradeoff

Take target edge t plus three internally disjoint length-two u-v paths
(a_i,b_i), i=1,2,3, with b=0. Acquisition prices are c_(a1)=c_(a2)=1 and
all other prices 100. Cap two and a shared fair marker orientation give
w_(a1)=w_(a2)=3/2 and every other w=201/2. For each a_i, offer a predictor
costing one fee unit, with marginal errors (2/5,2/5,1/100). The b_i have only
exact routines; target t has its exact routine plus the fair-guess option.
Take zero episode/coin price for this declared example.

Acquire a1,a2 exactly and use the a3 predictor. Its fee bound is C=4 and
certified risk R=1/100. At lambda=10 the three selected cut capacities are
3/2,3/2,11/10; all alternatives on the paths cost 201/2. The minimum cut and
a three-path flow both have value 41/10. Direct acquisition costs 201/2 and
guessing has penalized value 5. Hence z=41/10, and at alpha=1/100 the dual
lower bound is 41/10-10/100=4, attained by the construction.

For alpha=1/10, mix that method with a fair guess, using the method with
probability 40/49 and the guess with probability 9/49. Certified fee is
160/49 and risk is 1/10. At lambda=400/49 the two methods tie at 200/49;
the same cut choices remain minimizing. The resulting dual lower bound is
200/49-(400/49)/10=160/49, again attained. The coin used to choose the mixture
and the guess must be priced if it is not negligible; zero price is an explicit
assumption here, not a general free-computation claim.

The direct exact baseline's fee is 201/2. Comparing it to fee four also changes
the allowed error from zero to 1%, so this is not an accuracy-matched speedup.
The risk-matched mixture of direct exact answering and a fair guess costs
(201/2)*(1-2/100)=9849/100 at 1% risk; the constructed method improves its
declared acquisition/evaluation bill, using the additional calibrated model
information. A conventional controller with that information obtains the same
minimum-cut construction. The closest useful comparison is established
risk-constrained inference/experimental design, not an ordinary reasoner denied
the models or the graph relations.

## Boundaries before any larger screen

Precommit the cut/method mixture from valid fees and error contracts. Choosing
a cheap-risk cut after inspecting current predictions does not inherit these
marginal guarantees. Context-dependent prices require corresponding valid
conditional error contracts or an independently justified selection argument.
Model evaluation, calibration, graph checking, cut/flow computation, storage
and randomization must be included in any eventual complete-cost claim.

This is a prospective adapter with an explicit certificate and worked delta,
not a new min-cut theorem, a calibrated learner, or a promoted result.

The unchanged first [risk_cut_probe.py](risk_cut_probe.py) execution passed
the 29-method example at seven risk levels, checking 2,842 pairs of methods,
the explicit dual/cut-flow certificates, and 128 private-invoice executions.
It ran in 0.0076669 seconds. These checks establish the constructed finite
example only. Sources and outputs are frozen.

The separator assumes additive declared edge-offer fees. A nonzero shared
coin charge, joint model setup fee or other method-level cost needs a justified
additional case split or a richer separator; it cannot automatically be
absorbed into the displayed edge capacities.
