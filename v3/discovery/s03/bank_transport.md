# S12T: reusing the policy-bank source for changed costs

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT, not confirmation.
This is an elementary consequence of the common event in [S12](policy_bank.md),
not a new PAC-Bayes principle. Its intended use is retained value information
under repricing and model mixtures; complete acquisition economics remain open.

## Known repricing and affine transport

If a new context-independent price d_theta is known, the mean net utility of
Q is E_Q mu_theta−E_Q d_theta. The existing simultaneous lower certificate
L(Q) therefore transports to L(Q)−E_Q d_theta, even if Q and the new prices
are selected after the evidence. For a fixed lambda, exponential-weight advice
can use scores sum_j z_theta,j−t*d_theta. The evidence event and prior remain
unchanged; the utility source's semantics are not redefined retroactively.
Context-dependent unknown prices need their own warranted relation or source.

More generally, suppose a checked version relation supplies
mu'_theta>=a_theta+b_theta*mu_theta with known b_theta>=0. Put
B=sum_theta Q_theta*b_theta. If B>0, let R_theta=Q_theta*b_theta/B. Then

    E_Q mu'_theta >= E_Q a_theta + B*L(R).

If B=0, only the known a term remains. This works because the original event
already covers every posterior R, including a data-dependent one. Negative
multipliers would need upper information or a more conservative bound. A
fallible forecast alone cannot supply this checked transport relation.

## A cheap certificate for any weighted query

The original means also obey 0<=mu_theta<=1. For arbitrary requested weights
w_theta, any B>=0 and any rational posterior Q, pointwise algebra gives

    sum_theta w_theta*mu_theta
      >= B*E_Q mu_theta + sum_theta min(w_theta−B*Q_theta,0)
      >= B*L(Q) + sum_theta min(w_theta−B*Q_theta,0).

Every numerical proposal (B,Q) therefore yields a checkable lower bound for
the query; negate weights for an upper bound. No numerical optimum or inferred
probability vector is trusted. Taking B=0 gives the trivial box bound. Taking
B=sum w and Q=w/B recovers the direct nonnegative-weight certificate. Trying
other proposals can improve it by exploiting the known coordinate bounds.
This is a certificate for a requested weighted value, not a claim of optimal
acquisition or an automatic replacement for all policy planning.

The confidence event is equivalent, before intersecting hard information, to

    mu in [0,1]^K,
    sum_theta P_theta*exp(lambda*S_theta−lambda*t*mu_theta)
       <= exp(lambda^2*t/8)/alpha,

where S_theta is the current lower-receipt sum. This is a convex set. Minimum
weighted values can be proposed by conventional convex optimization. For
strictly positive weights and an active constraint, its scalar multiplier nu
gives the water-filling form

    mu_theta(nu)=clip(log(nu*lambda*t*a_theta/w_theta)/(lambda*t),0,1),
    a_theta=P_theta*exp(lambda*S_theta).

Choose nu so the constraint is tight; zero/negative-weight coordinates take
their favorable upper endpoint when deriving this particular lower optimum.
This formula is only proposed numerical advice until the resulting support
certificate is checked. At an interior optimum B*Q_theta=w_theta; clipped
coordinates account for the min correction in the certificate. Source
construction, proposal work, log checks and query retention must all be priced.

No without-replacement substitution, arbitrary semantic change, data-selected
prior or unregistered new policy is licensed by this algebra. The common
source supports changed consumer weights because it covers the original mean
vector simultaneously. A meaningful positive result still needs a useful
application and a comparison with these same conventional constructions.
