# Complementary proof duties through monotone certificate clauses

Codex (GPT-6), October26,2026. DEVELOPMENT; constructive extension of the
unknown-work covering adapter. The optimization machinery is ordinary
primal-dual covering. Novelty and practical costs remain unassessed.

A request may need several lemmas, each provable by alternative procedures.
Let its warranted certificate condition be a supplied monotone CNF phi_t:
each clause C is a set of certificate types, and the request is discharged
exactly when every clause contains a completed type. A singleton clause
is an indispensable proof; several clauses express complementary work.
This is a representation contract. Converting an arbitrary monotone DNF
or an arbitrary proof relation to a small CNF is not free or always possible.

Keep the shared_proofs procedure model, with fixed unknown completion work
R_j, possible nontermination, persistent checked certificates and fallback
c_t. Let d be the maximum clause width, not the union size of all clauses.
On a request that is not yet discharged, select any currently unsatisfied
clause C. Increase its dual variable y_tC while advancing every procedure
in C at unit virtual rate. Stop that increase when a certificate completes
or the request's total dual sum reaches c_t. Recheck the request condition;
if it remains false and budget remains, choose another unsatisfied clause.
At the budget cap pay fallback if still necessary. All other dual variables
remain fixed. A fallible model can choose which clause to work on first;
the bound holds for every such choice.

The ordinary fractional relaxation for an offline proof bank and fallback is

    min sum_j R_j*z_j + sum_t c_t*r_t
    subject to sum_(j in C) z_j+r_t>=1
               for every clause C of every request t;
               z_j,r_t>=0.

Its dual constraints are

    sum_(t,C: j in C) y_tC <= R_j,
    sum_C y_tC <= c_t,
    y_tC>=0.

A completed certificate j lies in no subsequently selected unsatisfied
clause, so cumulative virtual progress cannot exceed R_j. The fallback
budget ensures the second constraint. Consequently Y=sum_t,C y_tC<=OPT,
including an offline comparator that shares every purchased primitive
certificate across all clauses and requests. Total proof work, including
unfinished work, is at most dY; fallback payments are at most Y. Thus

    B <= (d+1)*OPT.                                     (PC1)

The atomic virtual-credit implementation carries over: credits z_j are sums
of selected-clause dual increments; execute a proof instruction whenever
a credit reaches its next integer. All instructions due at a simultaneous
crossing are finished before choosing the next clause. Controller costs,
applicability checks, CNF evaluation and state storage remain additional.
The symbol z in this implementation denotes credit, not the fractional
purchase variable in the displayed relaxation; code should distinguish them.

For K required lemmas with two alternative procedures each, the clause width
is2 and(PC1) gives3, whereas flattening all2K procedures into one crude
search support gives a2K+1 bound and does not express the AND duty correctly.
No completed primitive work is duplicated across bundles. This is an actual
complementarity-aware representation consequence, not evidence of a new
competitive ratio for known-cost covering or a measured application gain.
An ordinary solver implementing the same clause process ties exactly.

A useful prospective experiment would implement actual resumable checked
proofs, preserve their states across several clause-shaped requests, and
compare against complete fallback, independent per-request search, shared
ordinary search, and a small offline oracle with identical proof costs.
Only if that experiment addresses a real retained-proof duty should it
support a contribution claim; artificially withholding reusable witnesses
from the ordinary method would invalidate the comparison.

## A matching deterministic lower-bound candidate

The d+1 factor is not only an artifact of flattening the proof bank. Consider
one repeated request with d alternative proof procedures and unit fallback
price. All instructions have unit cost and finite completion lengths are
positive integers. Suppose a deterministic online method claims ratio rho
to the cheapest proof or all fallbacks, with no source information beyond
completion feedback. Follow its run when every procedure has infinite
completion length. After t completed requests, let S(t) be its total proof
work and p_i(t) the work on procedure i. Competitiveness on that prefix
requires S(t)+t<=rho*t, so S(t)<=(rho-1)*t.

Choose an index i with p_i(t)<=S(t)/d. Change only that procedure's completion
length to R_i=p_i(t)+1; keep all others infinite. The new instance has exactly
the same observed history through t requests. Extend the sequence long
enough that the offline comparator buys this certificate. The online method
has already spent S(t)+t, so its ratio is at least

    (S(t)+t)/(S(t)/d+1).

For rho>1, using S(t)<=(rho-1)*t and letting t grow gives a lower limit
at least d*rho/(rho-1). (For sufficiently large t, the displayed expression
is decreasing in S.) This exceeds rho whenever rho<d+1. If S(t) stays
bounded, the ratio instead diverges. Thus no deterministic method can
achieve a uniform ratio below d+1 in this black-box completion model.
A fixed additive constant can be handled by the same asymptotic argument.
The trivial rho<=1 cases fail directly when proof work is needed.

This is a prospective adversarial proof, not an independent confirmation.
For each deterministic method the adversary fixes a completion vector and
finite horizon consistent with the observed prefix; it is a legitimate
worst-case instance construction. It is not a lower bound for randomized
methods against an oblivious adversary, or for algorithms that inspect
program structure and infer completion costs. Such extra information is
outside the black-box model. Search the hidden-buy-cost literature before
calling this tightness result novel.

## Bounded developmental evidence

The frozen proof_credit_check.py implements hidden completion oracles, not
real theorem provers. It passed1,424 input schedules under two clause orders
(2,848 policy checks), charging9,654 simulated proof instructions in total.
It checks the dual inequalities, rational-credit identity, exact finite
hindsight cover and width-plus-one bill bound. Inputs include fractional
prices, nontermination, complementary clauses, empty conditions and
impossible clauses. The frozen source hash is in proof_credit_plan.json;
no re-run or post-exposure tuning has occurred.

In the worked repeated two-alternative case,40 requests cost20 proof units
plus9 fallback units, total29, against an offline proof cost10. With two
required lemmas, each having two alternatives, the bill is40+19=59 against
20 offline. Ten prices of1/10 carry fractional credit correctly and produce
bill29/10 against1 offline. These are artificial completion/tariff examples,
not fees from an actual prover or comparative application improvements.
The maximum observed ratio4 occurs at width3 in an input with a known empty
clause when the chosen ordering wastes work on another clause first. An
ordinary emptiness precheck would avoid that waste. It is a useful edge case,
not the substantive tightness witness; the nonempty repeated-duty lower
bound above supplies the separate asymptotic argument.

## Counterfactual requests may change without resetting proof identities

The fixed-source restriction is per certificate procedure, not a requirement
that every requested context stay identical. Let j name a proof of a fixed
lemma under an immutable source/version. Success still has one fixed R_j.
An edited request may add or remove j from its applicability clauses after
checking the old-to-new relation. The proof above permits these clauses to
change arbitrarily over time. A completed j is never run again and is usable
whenever its checked applicability returns. Unfinished progress likewise
continues to concern the original immutable lemma.

For the UNSAT-support example, additions to a request clause set can make a
stored refutation applicable; deletions can remove applicability; restoring
the support restores use without reproving it. This is ordinary dependency-
aware proof reuse, now included in the same stateful cost comparator. It
does not violate the dual budget. The warning in shared_proofs concerns a
stronger change: altering the meaning of j itself or requiring a new paid
verification under the same identity. That needs a fresh versioned procedure
and a comparator that pays or transports the corresponding proof explicitly.
Do not confuse temporary inapplicability with destruction of a certificate.
