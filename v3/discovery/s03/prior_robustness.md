# S13R: what a fallible observation model changes

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

## Matching marginals are insufficient

Take two bits with fair marginals, terminal utilities y0=0 and y1=x2, and
query prices q1=1/10, q2=2. Under independent bits, learning x1 cannot change
the preferred action; learning x2 has expected value 1/2 and is too expensive.
The two-action closure upper bound is zero. Under the equally marginally fair
model x1=x2, querying x1 reveals x2 and has expected net gain 1/2-1/10=2/5.

Thus a sound receipt and correct marginal forecasts do not warrant the
independent-bit acquisition certificate. The conditional-independence model
is load-bearing. Merely keeping both models does not supply a calibrated
weight or robust stopping certificate. One can compute separate model bounds,
use explicit credences, or adopt a supported ambiguity set, but must name the
criterion and pay for its evidence. This also reconnects to the earlier finding
that informative probes require correlation information absent from marginals.

## A scoped product-bias extension

Suppose bits are independent with known means mu_i. Center eta_i=x_i-mu_i.
If the utility representation is supplied as

    y_a=c_a+sum_e a_{a,e}*product_{i in e}eta_i,

every term with an unqueried coordinate still has conditional expectation zero.
The common-baseline/tower proof therefore extends. Let [l_e,u_e] be the exact
range of that centered product, computed by successive endpoint products.
For coefficient difference d=a_{a,e}-b_e, its upper completed-term reward is

    r_{a,e}(b)=max(d*l_e,d*u_e)>=0.

The same closure graph gives a valid adaptive upper bound. For nondegenerate
bits l_e<0<u_e. A coordinatewise common baseline minimizing the largest reward
over actions is

    b_e=(a_max*u_e-a_min*l_e)/(u_e-l_e),
    r_e=(a_max-a_min)*(-l_e*u_e)/(u_e-l_e).

This follows by equating the increasing upper branch
(b-a_min)*(-l_e) and decreasing branch (a_max-b)*u_e. Fair-bit endpoints
recover midpoint coefficients and half-ranges. Action-mean gaps can improve
the certificate further; the coordinatewise radius does not solve every
multi-action baseline optimization problem. Degenerate deterministic bits are
substituted before forming the centered basis.

## Representation cost blocks a free generalization

A sparse original parity chi_S=product x_i expands as
product(mu_i+eta_i). If all means are nonzero, its unique centered-product
representation contains all 2^|S| subset terms. Thus changing to the centered
basis can destroy the earlier high-degree sparse representation. Conditional
expectations of the original parity remain cheap:

    E[chi_S|A]=chi_{S intersect A}*product_{i in S minus A}mu_i,

but they now change before the last prerequisite is acquired, so the simple
all-prerequisites completion graph no longer describes their value exactly.
This is a design boundary, not a license to ignore acquisition correlations.

An alternative model decomposition writes a biased bit as a fair bit with
probability 1-|mu_i| and the fixed sign of mu_i otherwise. Conditional on the
independent latent fixed-bit set F, all remaining bits are fair. Revealing F
for free and applying the conditional uniform-model upper bound gives

    V_actual <= E_F[c_star(F)+Gamma_F].

Subtract the original immediate-action value to bound its improvement.
This is an ordinary information relaxation, and can be loose because the free
latent information itself has value. Enumerating F is exponential; truncation
needs an explicit tail bound and a bounded utility remainder. No efficient
or economical implementation is established by this decomposition.

## A conservative distribution-robust transport

For a fixed feasible policy and incumbent action, assume utilities lie in
[0,1] and total query cost is at most C. Their pointwise net gain lies in
[-1-C,1]. If an independently justified relation gives TV(P,Q)<=epsilon,
then its P-expected gain is at most its Q-expected gain+(2+C)*epsilon.
Taking the supremum over the same feasible policy set preserves this upper
bound. Thus Gamma_Q+(2+C)*epsilon is a valid approximate stopping certificate
against that incumbent. It is often weak and does not itself establish a TV
relation. A zero bound under a fallible model does not become a true zero
bound under an unspecified amount of model error.
