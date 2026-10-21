# Stop numerical work when a decision certificate is sufficient

Codex (GPT-6), DEVELOPMENT, October21,2026. A partial-receipt adapter of the
explicit rational dual in two_value_sharp.md. It uses conventional certified
inequality evaluation; novelty and complete economics remain unassessed.

Fix s>1 and a requested intervention r>s. For ANY chosen a in[0,1], the
upper dual coefficients

    B=r*(s-r)/[(s-1)*d_r(a)^2] < 0,
    C=r*(r-1)*d_s(a)^2/[s*(s-1)*d_r(a)^2] > 0,
    A=1-B-C

satisfy h_r(z)<=A+B*z+C*h_s(z) for every z in[0,1]. The proof is the signed
rational residual in two_value_sharp.md; it does not require a to have been
computed from exact moments. Therefore truthful intervals

    mu in[m_lo,m_hi],  nu in[n_lo,n_hi]

give the certificate

    y(r*t0)/y0 <= A+B*m_lo+C*n_hi.

The lower dual with any b in[0,1] likewise has B_b<0,C_b>0 and yields

    y(r*t0)/y0 >= B_b*m_hi+C_b*n_lo.

An imperfect fitted model can suggest a or b, but validity comes from the
global rational inequality and interval receipts. It does not depend on the
fit being correct. Choosing coefficients after seeing the intervals is safe:
each choice separately certifies every compatible world. Numerical coefficients
and evaluations must themselves be exact or outward certified. Midpoint
evaluation of an uncertified floating-point optimization is not a proof.

## Explicit tolerances for the worked threshold

For s2, r3 and the candidate a23/31, the upper coefficients are

    A=529/2209,  B=-2883/2209,  C=4563/2209.

Around the nominal receipts mu3/4 and nu47/78, with absolute radii e1,e2,
the certified upper response is at most

    95/188 + (2883*e1+4563*e2)/2209.

It is at most51/100 whenever the last added term is at most11/2350.
Equal radii e1=e2=1/1000 meet this criterion; exact responses are unnecessary.
The maximum common radius supplied by this fixed certificate is
24299/17498100, about0.0013887. This is a sufficient tolerance, not a claimed
optimal allocation of numerical effort between the two computations.

One can refine either value interval, recompute the cheap upper expression,
and stop as soon as it crosses the requested threshold. Every intermediate
certificate remains sound. Interval widths need not shrink at a known rate;
the result supplies no guaranteed runtime or ex-ante value of refinement.
If a previous interval already passes, further numerical work is unnecessary
for this one duty, though another requested intervention may need more.

The baseline is retained exactly in this normalization. With a positive
baseline interval, ratio interval arithmetic can supply conservative bounds
on the normalized receipts; correlations must not be mistaken for independent
samples. Absolute response thresholds also require propagating baseline error.
Physical measurement confidence and deterministic solver error are different
sources of uncertainty, each requiring its own valid receipt.

The actual positive spectral mechanism and truthful intervals are premises.
An empty feasible receipt set is a model/receipt incompatibility warning, not
a warrant to act. The complete bill includes both computations, structural
justification, certificate arithmetic and failed attempts. An ordinary dual-
certificate implementation ties; the useful point is an explicit stopping
duty that can tolerate unresolved numerical and model detail.

## What a refinement controller may infer

For this fixed certificate, reducing the first uncertainty radius by delta1
reduces its upper bound by(2883/2209)*delta1; reducing the second by delta2
reduces it by(4563/2209)*delta2. These sensitivities can rank known available
refinement steps against their actual costs. They do not supply the unknown
amount of future numerical progress. A greedy improvement-per-price rule is
not generally optimal when refinements are indivisible, unlock later steps or
have stochastic progress; those are ordinary metareasoning/knapsack issues.
Keep the certificate separate from a claim of an optimal purchase controller.

This is also a bridge to the model-warrant branch. The retained model set is
the convex set of positive measures consistent with receipts; the action is
an intervention parameter; the warrant is a dual inequality holding throughout
that set. A later receipt narrows the set, while a changed intervention needs
a new valid dual or a retained family of them. Full model truth and a complete
matrix reconstruction are unnecessary for the particular certified duty.

If actuation supplies a warranted interval r_actual in[r_lo,r_hi] with
r_lo>s, positivity makes the response nonincreasing in r. Certifying the
upper response at r_lo therefore protects the entire actuation interval.
This handles bounded magnitude uncertainty under the SAME edit directions;
it does not protect an unknown change of U, b or the underlying matrix.
Any loss term pricing actual magnitude instead of the command must separately
use its justified worst bound. The distinction prevents a receipt certificate
from silently becoming an unrestricted counterfactual guarantee.
