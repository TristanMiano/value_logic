# A probability interpretation with known losses and fixed model identities

Codex (GPT-6), October26,2026. DEVELOPMENT. This connects the scalar-receipt
construction to the author's probability-information and fallible-model
questions. It supplies an interpretation, not a new imprecise-probability
principle or an empirical application.

Suppose a service uses n fixed probability models p_i on a finite outcome
space, but the client only knows model-specific rational polytopes B_i
inside the probability simplex. For a declared loss vector ell_j it reports
the conservative risk R_j=max_i ell_j dot p_i. Interval reports impose

    a_j <= max_i ell_j dot p_i <= b_j.

Negate each affine response and reverse the interval endpoints. These are
exactly AR1 minimum receipts. Consequently the entire possible risk of a
new declared loss is available, including gaps, without identifying all
model probabilities. Here values contain probability information because
losses, scaling, the maximization rule and model identities are fixed and
known. Unknown stakes or a changing aggregation rule destroy this reading.

The result is a constraint on the *service's collection of distributions*.
It is not a probability that any one model is correct. A guarantee about
actual expected loss additionally needs a warranted relation between the
true distribution and this collection, such as membership in its convex
hull. Agreement between quoted risks does not establish that premise.

## A three-outcome risk gap with positive probabilities

Embed the positive two-coordinate source vectors in robust_gap.md as

    p_i=(x_i1/30, x_i2/30, 1-(x_i1+x_i2)/30).

Use that example's a=b=10, delta=epsilon=1/10 and its two distinct
full-dimensional coordinate regions. All probabilities are positive and
sum to one; the source remains an independent product of compact rational
polytopes in the simplex. For the first two losses take the indicators of
outcomes{2,3} and{1,3}. Retain each conservative risk in
[199/300,2/3], equivalent to the original coordinate-minimum reports in
[10,10.1]. For the new loss take the indicator of outcome3. Its risk is

    max_i p_i3 = 1 - min_i(x_i1+x_i2)/30,

so the exact possible risks are

    [13/50,27/100] union [22/75,3/10].

A reported risk17/60 lies in the interval hull but in neither component.
Thus it contradicts the joint fixed-model/risk-report contract. It does
not tell the client which reported value, source region or stability
premise to withdraw. The construction is analytic; no deployed risk
service or sampled calibration outcome is claimed.

The ordinary comparison receives the same model polytopes, losses and
reports, and therefore computes the same answer. Standard robust
expectation is the support function of the convex hull of the probability
models. This familiar representation explains both the information and
its limits. The possible contribution is the structured inference and
certificate for a finite retained history under an explicit cost model,
not privileged access to probabilities from the word 'value'.

Known full models permit direct evaluation. Warranted maximizing-model
labels fix old witnesses and simplify inference. With many identical
model regions, homogeneous_receipts.md can remove the general subset
algorithm. For one new reported risk, direct consistency is a serious
alternative to retaining its complete predictive set.

The gap also depends on the finite, model-specific source contract. If the
service is instead allowed an arbitrary risk envelope inside a common
region, the inference problem changes: its convex hull and coherent-risk
extension are the natural ordinary objects. In particular, sufficiently
many interchangeable models fall under the homogeneous shortcut and have
an interval of possible next risks. The example does not establish that
nonconvex predictive risk sets are intrinsic to coherent risk measures.
Convexifying each fixed collection preserves its support-function values;
allowing arbitrary new collections or dropping their model-specific priors
is the information change that can erase the example's gap.
