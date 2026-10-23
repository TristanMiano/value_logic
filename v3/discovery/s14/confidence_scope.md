# Confidence does not turn into a posterior or survive selective forgetting

Codex (GPT-6), October23,2026. Same-model scientific screen.

The latent-span results bound the probability, over the whole iid training
experiment, that a procedure reports an unsafe certificate. They do not
assign a95% posterior probability to the particular learned model or its
population risk after the observed receipt. This distinction remains even
when the bound is a function of the observed complexity.

An elementary example makes the issue explicit. Let z in F2 be Bernoulli
with P(z=1)=0.1 and take N200. Conditional on seeing J_N=0, every sample
is zero, and the true missing mass is exactly0.1. A rank-zero bound below
0.1 is then wrong with conditional probability ONE. That observation has
unconditional probability(9/10)^200, so it is entirely compatible with a
95%-valid confidence procedure. A prior would be extra information.
The close scenario literature gives a broader version of this distinction;
see the Garatti/Campi2023 example logged in literature.md.

Repeated independent fresh cohorts create another danger. Keep only an
all-zero200-case cohort and retry otherwise. Its positive probability
(9/10)^200 implies that eventually such a cohort appears with probability
one. Reporting only that certificate can therefore produce a false
nontrivial learned rule almost surely. It is not the same experiment as
the single-stream anytime theorem. Budget confidence across restarts, or
retain the original cohort as that theorem requires. Large expected waiting
time does not repair the invalid inference.

Selective expensive audits within ONE iid latent stream are permitted:
unaudited cases remain represented by truthful broad feasible sets. Deleting
those cases and pretending the selectively audited subsequence is iid is
not justified. Similarly, a rule may be withdrawn after new evidence; the
common guarantee applies only to rules still certified on the retained
latent span. Storing the raw vectors is not necessary if a faithful
certificate preserves the required containment.

These tests support the contract, not a promotion. They also identify the
price of safe reuse: evidence provenance, cohort retention, and a fixed
population/feature interpretation are substantive resources.

## Paid distribution-shift warrants

If an independently warranted new law Q satisfies TV(P,Q)<=rho, then on
the original good training event every retained model has Q-risk at most
min(1,epsilon+rho). If dQ/dP<=w is warranted instead, the bound is
min(1,w*epsilon). These elementary inequalities apply to the same protected
set S_tau and can cover a whole family of future laws whose respective
shift bounds are established. They do not infer a shift bound from good
training fit. Ordinary robust probability gives the identical rules;
this is a scope adapter, not a new distribution-shift method.
