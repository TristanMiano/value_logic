# Partial reasoning can certify a budget for environmental change

Codex (GPT-6), October23,2026. DEVELOPMENT. A proposed paid-evidence adapter
to established optimal transport and confidence-band machinery. No new
Wasserstein duality, chance-constraint principle or concentration theorem.

## Exact contract

Fix a finite case space Omega with a justified metric c, and a nonempty bad
set B before sampling. Its complement W is the event on which the declared
model-use interface is correct. W need not assert that every statement in
the model is true; it must actually protect every inference the interface
permits. Define the margin

    D(x)=min_(y in B) c(x,y).

The finite metric makes D(x)=0 exactly when x is bad. A deployment change
is a coupling of X~P and Y~Q with E[c(X,Y)]<=rho, or equivalently the
corresponding type-1 Wasserstein bound. This change budget is a separately
warranted premise. The construction does not infer it from training fit.

For every lambda>=0, the pointwise inequality

    1[Y in B] <= lambda*c(X,Y)+(1-lambda*D(X))_+          (1)

holds: on failure c(X,Y)>=D(X), and otherwise its right side is nonnegative.
Therefore

    Q(B) <= inf_(lambda>=0) {lambda*rho+E_P(1-lambda*D)_+}. (2)

For a known discrete margin law, fractional transport of its smallest
margins attains this bound (subject to enough budget to move all mass).
This is the classical continuous-knapsack/Wasserstein chance construction.
In finite Omega a nearest bad point exists for every source point.

## Keep incomplete computations, not guessed margin labels

Take a predeclared iid cohort X_1,...,X_N. Its latent margins D_i are fixed
even if they remain computationally unresolved. Paid sound reasoning gives
lower bounds L_i<=D_i; an uncomputed case may have L_i=0. A solver may
choose which bounds to refine after inspecting all previous receipts.

Suppose a simultaneous upper CDF event for the latent cohort has been
obtained:

    F_D(t) <= min(1,Fhat_D(t)+alpha) for every t>=0.      (3)

A conventional two-sided DKW event supplies this at confidence at least
1-2*exp(-2*N*alpha^2). It is enough to use its upper half. The fixed map D,
iid cohort and sample-size hypotheses are substantive. No optional sample
size or data-chosen bad set is silently admitted.

Because L_i<=D_i, Fhat_D<=Fhat_L. Thus the ONE event(3) simultaneously
covers every truthful subsequent refinement of these same N lower bounds,
however the computation scheduler chooses or stops. Define R_L to have CDF

    F_R(t)=min(1,Fhat_L(t)+alpha), t>=0.

R_L places mass alpha at0, keeps the smallest1-alpha portion of the
empirical L distribution and discards its largest alpha portion. It is
stochastically no larger than D on event(3). Combining with(2) gives the
uniformly valid upper risk

    U_L(rho)=inf_(lambda>=0) {lambda*rho+E_R(1-lambda*R)_+}. (4)

It can be clipped at1. This is a scalar empirical transport problem, not
an optimization over all raw worlds. Increasing any L_i cannot increase
U_L. The same protected event permits later selection of rho, lambda or
an inference within the original common W, provided its change-budget
premise is separately justified. An identical ordinary procedure ties.

## A useful certificate without solving the whole risk curve

For target error epsilon in(alpha,1) and rho>0, sort the current lower
bounds L_(1)<=...<=L_(N), and interpret fractional sums by linear
interpolation. A sufficient certificate for U_L(rho)<=epsilon is

    rho <= (1/N) * sum_(i=1)^((epsilon-alpha)*N) L_(i),  (5)

provided the right side is positive. This is the classical smallest-margin
transport criterion applied to R_L. It is exact for the R_L margin-law
relaxation. It is not asserted to be the exact confidence bound for the
full original case distribution, which may contain additional structure.

At rho=0, check the mass at0 directly; do NOT use(5) alone. A zero
right-hand side cannot certify a small baseline error. Infinite or empty
bad sets would also need conventions not used in this finite contract.

Only the smallest (epsilon-alpha)N bounds enter(5). A partial computation
already known to exceed the current cutoff can be left unresolved above
that cutoff. Exact distances and full classification of all cases are
unnecessary. This is a decision-focused acquisition opportunity, not a
claim that every distance query is cheap or that a greedy scheduler is
optimal. With independent intervals L_i<=D_i<=U_i, the exact range of the
smallest-k sum is between the corresponding sums for L and U; joint
constraints can narrow it further.

## A transparent resource/capability example

Let N=5000 and alpha=1/50. Then the stated DKW failure ceiling is
2*exp(-4)<0.05. At epsilon=1/20, criterion(5) uses the150 smallest bounds.
Suppose4900 acquired certificates supply the stored bound L_i=10, while100 computations
remain wholly unresolved and use0. The right side of(5) is at least
50*10/5000=0.1. Refining50 of those100 cases to a sound lower bound10
increases that certificate to100*10/5000=0.2. Refining the remaining50
increases it to0.3.

Thus50 additional lower-bound certificates double the permitted expected
change from0.1 to0.2 at the SAME declared5% risk and>95% training confidence.
No exact margin need be computed, and50 cases still remain unresolved.
All4900 original certificates, the next50, cohort acquisition, sorting,
calibration and edit-budget provenance are paid. This is a possible
receipt-state calculation, not an observed dataset, measured speedup or
empirical error reduction. It is not a new statistical bound over the
strong ordinary transport/confidence-band combination.

## One concrete source of sound lower margins

If the fixed protected event W is a Boolean CNF and edits flip coordinates
at positive additive prices c_j, then distance to failure is the minimum,
over clauses C, of the sum of c_j for literals currently true in C. To
falsify a clause one must flip precisely those true literals; falsifying
any clause is enough to leave W. A partial raw-case receipt can sum only
the literals proved true and then take the same clause minimum. This is
the exact worst-case margin over its unrestricted Boolean completion box.
Repeated/opposite literals and tautological clauses must first be normalized.

This lower bound can certify that no cheap edit breaks ANY permitted
inference while many coordinates remain unresolved. It is ordinary
certificate/robustness analysis; some CNF interfaces have narrow clauses
and consequently small margins. Richer W can make distance computation
NP-hard. A fallible predictor may propose the most useful literals to
check, but only their sound receipts enter L_i.

## Early rejection conditions

- A binary good/bad rank certificate alone supplies no nonzero continuous
  perturbation margin: an arbitrarily small move can leave a linear subspace.
  In a discrete space its protection depends on the actual edit metric.
- Choosing B to avoid the observed cohort invalidates(3); for instance,
  excluding only sample points can have perfect sample fit and almost no
  population coverage. Retain a fixed protected event, separate data, or a
  separately justified uniform function-class bound.
- The result is unconditional Q(B), not error conditional on a rare release.
  Conditional transport has an additional denominator/mass problem.
- The guarantee concerns every coupling within the declared budget, not a
  learned causal intervention without explicit semantics.

Closest-prior comparison is already strong. Keep this as a useful adapter
candidate; do not build a large benchmark merely to rediscover transport
duality or use a coarse no-drift baseline to claim novelty.

The first drift_probe.py execution passes72 exact transport primal/dual
comparisons,120 positive-radius certificate checks,288 monotone refinements
and108 partial CNF completion boxes. It also checks all three aggregate
receipt states in the example by rational arithmetic. This does not test
population coverage, independence, physical drift or complete economics.
