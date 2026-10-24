# Predicted supports can propose probability queries, not justify themselves

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 22.

Let P be an unknown supplied law on a known finite set Omega. A fallible
model proposes S subset Omega of size r. A paid exact value oracle for
bounded functions can return q=E[1_(Omega minus S)]. If q=0, nonnegativity
proves support in S; r-1 further independent indicator values determine P.
The bill is r queries, including validation, versus n-1 for an unrestricted
n-point law. If q>0, the proposal fails. Normalizing predicted weights does
not repair that failure. The query functions must be admitted and priced.

This elementary route is already covered by finite fibers, nonnegative
expectations and sparse recovery. It is not a new contribution.

On a compact real interval, a proposed r-point support S={a_1,...,a_r}
has annihilator g(x)=product_i(x-a_i). A paid q=E[g(X)^2]=0 proves X is
in S almost surely. The first r moments, including normalization, determine
weights through a Vandermonde system. A degree-2r query may instead require
2r separately acquired moments; it is not automatically one unit of work.
Distinct roots and conditioning matter for numerical recovery.

For q<=epsilon, outside the rho-neighborhood of S, |g|>=rho^r. Therefore
P(distance(X,S)>=rho)<=min(1,epsilon/rho^(2r)). For L-Lipschitz loss ell,
interval diameter D and nearest-support projection pi_S,

    |E ell(X)-E ell(pi_S X)| <= L*(rho+D*epsilon/rho^(2r)).

The high-degree penalty is real. This bound supplies no projected weights.
Exact-zero support and approximate concentration are different services.
Adaptive exact queries need no statistical union bound; estimated values
need a justified simultaneous/adaptive validity rule.

Reject generic 'values discover sparse probabilities' novelty. The possible
application is a naturally cheap checked nonnegative value that validates
a fallible source proposal and reduces later task information. No natural
workload or full-cost benefit has been supplied here. A synthetic favorable
oracle would not resolve the missing contribution.
