# Verification across edits: charge new error directions

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass35.
An extension of private_repairs.md, not a new general counterpossible logic.

## A public rank potential

At version t, all admissible model errors lie in an unknown linear space R_t.
The public learned correction space U_t is a subspace of R_t. On an explicit
program/model change, let T_t be a known linear transport and assume

    T_t R_(t-1) subset R_t,
    dim(R_t)-dim(T_t R_(t-1)) <= p_t.

Transport the learned space to T_t U_(t-1). Rank-nullity gives

    dim(R_t)-dim(T_t U_(t-1))
      <= p_t + dim(R_(t-1))-dim(U_(t-1)).           (1)

Indeed the quotient map from R_(t-1)/U_(t-1) onto
T_t R_(t-1)/T_t U_(t-1) cannot increase dimension. Each independently found
public counterexample adds one dimension and reduces the deficit by one.
Consequently the total number of false scope proposals on the ideal
transcript is at most

    H = dim(R_0)-dim(U_0) + sum_t p_t,              (2)

using a warranted upper bound when the dimensions are not known exactly.
Rank loss under a projection T_t is not itself a fresh-error charge.
Repeatedly throwing U away would lose this benefit. If there is no finite
innovation budget, (2) does not supply a finite lifetime bound.

## Reusing the actual sealed evaluations

A count bound alone does not update the expensive truth data. Require an
explicit exact source edit

    A_t(x)=T_t A_(t-1)(x)+c_t(x),                   (3)

where c_t can be evaluated by the verifier at its hidden points with a
known cost. Then it can update its stored true values using (3), without
new full-source oracle calls. Per-version transport and c_t evaluation still
cost work. If the edit is merely asserted or its effect must itself be
obtained from the full oracle, no such saving follows.

All source/model differences must keep a common proved polynomial degree
bound D (or a rational numerator bound with nonzero denominators). Proposals,
edits and public repairs may depend on earlier Boolean checks, but no hidden
points, residuals, timings or private sketches are disclosed. The ideal-path
argument fixes the whole adaptive sequence independently of the sealed
sample up to its first error. Thus k hidden grid points give

    P(any false all-input scope accepted) <= H*(D/q)^k.       (4)

Fresh independent public counterexamples cost at most H*q/(q-D) full-source
calls in expectation. Those calls concern the appropriate current source;
they are not automatically interchangeable with initial-source calls at the
same price. If inverse transports permit using a cheaper reference oracle,
that must be stated and paid separately.

## Scope and useful distinction

An invertible relabelling or a projection with no new error directions has
p_t=0. Any number of such edits can preserve the same finite rejection budget,
even if the displayed error subspace changes at every version. New model
families can introduce additional directions; their innovation bounds add
to H. This is an executable hypothetical-update semantics with a common
verification event, rather than a claim that arbitrary inconsistent axioms
have a uniquely correct counterfactual truth value.

The mechanism separates three bills: source-value transport, new error-space
learning, and per-proposal checking. It links retained evidence, fallible
models, paid refinement and counterfactual revisions. Linear transport,
rank potentials and one-sided checking are conventional ingredients; the
candidate synthesis needs a real access regime and closest-method comparison.
An ordinary verifier using the same transport contract implements the same
service and ties. No measured runtime or fee improvement is claimed here.
