# Growing program proposals, delayed receipts and an anytime risk bound

Codex (GPT-6), October23,2026. DEVELOPMENT; pass19 extension.
This is a synthesis of open_model_receipts.md and anytime_receipts.md.
It is a candidate operational interface, not a new generic PAC-Bayes bound.

Fix a countable universe of complete bounded-loss policies h, prior
subprobability pi_h>0 with sum<=1, and eta>0 before the iid case stream.
The program may enumerate only finitely many of these policies. Their risks
p_h=E Y_hi and latent losses Y_hi in[0,1] exist regardless of computation.
Set a=1-exp(-eta). For every fixed h,

    E_n^h = exp(-eta*sum_{i<=n}Y_hi) / (1-a*p_h)^n

is a nonnegative supermartingale. This follows from the chord inequality
E exp(-eta*Y_hi)<=1-a*p_h. The prior-weighted sum is a supermartingale
with initial wealth<=1. Ville therefore gives one event of probability
at least1-delta on which, simultaneously for all n and finite posteriors q,

    sum_h q_h log E_n^h <= KL(q||pi)+log(1/delta).

Use the variational inequality for the finite support of q and then
convexity of -log(1-a*p). With sound partial upper losses U_hi>=Y_hi,
u_n(q)=sum_h q_h sum_{i<=n}U_hi/n, this yields

    R(q) <= [1-exp(-eta*u_n(q)
                     -(KL(q||pi)+log(1/delta))/n)] / a,          (1)

clipped at1. It holds at every arrival time, after arbitrary later proof
refinements, and for any selected historical prefix and posterior. A fixed
eta incurs no additional union penalty over n. This strengthens the local
fixed-N interface, not the underlying established theorem.

For a finite enumerated set A, let

    w_h=pi_h*exp(-eta*sum_{i<=n}U_hi), Z=sum_{h in A}w_h.

The minimizing finite posterior is q_h=w_h/Z and bound(1) becomes
[1-(delta*Z)^(1/n)]/a. A bounded reasoner can present a finite certificate
consisting of a prefix, finite program list, prior weights, loss receipts
and exact or outward-rounded arithmetic. No global program enumeration or
normalization is required. The risk is for drawing h from q afresh per
future case; a single persistent draw or a context-dependent selector needs
its own specified guarantee.

The prior and whole policy semantics must precede the cases, even if a
particular description is found later. Retrofitting cheap codes to the
sample invalidates the statement. Data-dependent selection of eta also
needs a predeclared mixture or explicit confidence allocation. Increasing
n can worsen the current bound when new losses are unresolved, but retaining
past prefix certificates avoids losing earlier justified decisions.

## Fallible receipt checking and counterfactual transfer

Suppose a separate validation mechanism has a lifetime probability<=beta
of ever accepting a false upper receipt before retirement. On its good
event, all the preceding pointwise inequalities hold. A claimed risk
certificate can fail only if either that validation event fails or the
latent statistical Ville event fails. The total is at most beta+delta;
no independence is needed and no conditional-on-release guarantee follows.
Only a validator with that actual receipt semantics can instantiate this
composition; a numerical residual checker does not automatically check
arbitrary mathematical proofs.

A changed policy h' can reuse a bound for h without a new statistical test
when a separately warranted population relation p_h'<=p_h+c is available,
for example from a uniform pointwise loss bound valid for every case.
Checking that relation only on the same finite cohort is insufficient.
If new candidate policies instead enter the prior universe, their own
weights and partial losses are charged in(1). Adaptive choices of semantic
counterfactuals cannot bypass either route.

The primary-source screen identifies Chugg, Wang and Ramdas(2023),
Theorem4, as a direct strong antecedent: mixtures, dominated processes,
variational inequalities and time-uniform posterior choice are already
explicit there. Retain the partial-proof and finite-enumeration interface,
but reject a claim of new generic anytime PAC-Bayes machinery. A complete
cost example would need to establish a useful operational difference.
