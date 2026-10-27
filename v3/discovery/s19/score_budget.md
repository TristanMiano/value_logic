# Can guaranteed score improvements fund more reasoning?

Codex (GPT-6), October26,2026. DEVELOPMENT; broad Q1/Q3/Q4 screen.
The projection mechanism is established. This note isolates a modest
budget wrapper and the assumptions under which its interpretation survives.

Fix m mathematical claims, their actual but unresolved truth vector
x in {0,1}^m, positive stakes w_i, and weighted Brier loss

    L(p,x) = sum_i w_i*(p_i-x_i)^2.

A sound checked argument may establish x in a closed convex region C.
Project p onto C in the weighted norm, obtaining q. The projection
inequality gives, for every admitted truth vector,

    L(p,x)-L(q,x) >= g = ||p-q||_w^2.

This is ordinary proper-score coherence correction. Predd et al.2008
already provide successive local projections with stepwise Brier improvement;
their2009 paper gives the broader proper-score/Bregman argument. Partial
constraints and additional iterations are not new ideas here.

For arbitrary proposed p,q, their score difference is affine in x:

    ||p||_w^2-||q||_w^2-2*(p-q)^T W x.

A sound lower bound over the current source can therefore certify a gain
without resolving the actual truth vector. For a compact convex source C,
the largest uniform gain over all q in the unit cube is dist_w(p,C)^2.
Indeed projection achieves it. Conversely evaluate any proposed correction
at the projection point z in C: its gain there is
dist_w(p,C)^2-||q-z||_w^2, at most dist_w(p,C)^2. Affinity extends a
guarantee on Boolean vertices to their convex hull. This is a robust
decision calculation, not evidence that the unknown truth is randomized.

## A conservative spending account

Start with explicit reserve B>=0 in the same utility units as the stakes.
Pay every search, checking, projection and account-update cost from the
available reserve. Whenever a correction is admitted, add its certified
gain g to the reserve. No anticipated gain is credited before its proof
and numerical certificate have passed; abandoned work remains charged.
At every prefix, expenditure C_T<=B+sum_(t<=T)g_t. Telescoping the
actual losses for the same fixed x gives

    L(p_T,x)+C_T <= L(p_0,x)+B.

Thus unresolved truth need not prevent a verifiable computation-spending
limit. This is an elementary potential-account argument, not a new
coherence theorem or a competitive guarantee against the best proof search.
With zero reserve it cannot start a paid computation. It can stop without
finding any useful proof. A gain certificate expressed in Brier units is
not money until an explicit stakes/cost conversion is warranted.

For example, proving two propositions complementary changes forecasts
(4/5,4/5) to (1/2,1/2). Either admissible truth vector incurs loss17/25
before and1/2 after: the gain9/50 can reimburse at most9/50 of total paid
work if there is to be a net improvement. The example contains no measured
proof acquisition or economic result; ordinary projection gives the same gain.

## Two scope failures

1. A proposed mathematical relation is not a sound constraint merely because
   a fallible model predicts it. Crediting its projected gain before checking
   may pay for arbitrary wasted search even when the initial forecast is
   exactly true and has zero loss. The account admits only proved gains.
2. Changing the truth vector or stakes changes the potential. For changing
   Boolean x_t but fixed weights and forecasts in the cube, the added drift
   term is bounded by sum_t sum_i w_i*|x_(t,i)-x_(t-1,i)|. Such a variation
   budget must be warranted and charged. Retracting an old premise does not
   retroactively preserve its gain certificate on a newly admitted world.

**PARK the generic contribution.** The budget identity is useful bookkeeping,
but projection/coherence and telescoping potentials are close established
ingredients. A nontrivial search-selection guarantee or a real total-cost
gain remains absent. Do not expand an experiment campaign just because the
wrapper has a direct connection to unresolved mathematics.
