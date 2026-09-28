# F07 — consolidated soundness and acceptance record

Research author: **ChatGPT (GPT-6 Astra Pro)**. September 28, 2026 UTC.
Status: **F07 complete at finite-fragment soundness scope**; F08 is unstarted.
Source baseline: `aad293c8ffa885605a39455bed61532cca18bc9a`.
This is written mathematical reconstruction and source/code correspondence by
the same assistant, not an external review or proof-assistant verification.

## 1. The precise combined result

Fix an admitted context C and a request J before inspecting the candidate output.
An admitted context has a fixed, finite signature of named source coordinates,
unit tags and positive rational conversions, and a nonempty finite family of
rational-polyhedral cases. Each case has a checked rational feasible witness.
A source assignment has finite real coordinates; the domain need not be bounded.
Terms are closed, typed, finite expressions built from rational literals,
addition, rational scaling, min/max, `res(a,b)=max(b-a,0)`, lexical nonrecursive
binding and the declared conversions. Literal infinity arithmetic is not native.

Write `Delta(x)=eval(t,x)-eval(s,x)`. Independently of any proof, a local judgment
`C;h |= t <=[b] s` means `Delta(x)<=b` for every x in **that case** D_h. A global
judgment quantifies over the union of the live cases. Negative b is modeled
improvement, zero non-deterioration, and positive b an allowed deterioration.
This semantics is not defined by checker acceptance.

**Combined acceptance theorem.** On finite, immutable, supported standard data
and exact rational arithmetic, if the native checker accepts a finite proof and
a receiving check binds its actual root to J's current context, domain, unit,
expression pair and adequate budget, then J holds in its declared finite-real
semantics. For each advertised producer field used by the caller, additionally
require the corresponding producer input contract and proved transformation,
or an independent receiving check of that field. Empirical source applicability,
physical program identity, available observations, proxy alignment and a
probability interpretation are separate premises, not consequences of a trace.

This is successful-return correctness. It does not assert proof-search
completeness, optimal bounds, guaranteed availability, runtime/space performance,
robustness to arbitrary mutable or adversarial Python objects, or correctness of
the Python runtime. The current audit utilities are not the F11 integrated
reasoner. Named expansion limits reject certain sizes; they do not certify
whole-process resource use or every possible payload allocation.

## 2. Proof: normalization, rules, derivations and requests

The complete rule proof is [03_soundness.md](03_soundness.md), with its
[function-space reconstruction](03c_function_space_reconstruction.md). The
additional [S3 reconstruction](03e_public_pipeline_reconstruction.md) and
[S4 working derivations](../work_logs/F07_2026-09-28_S4/reconstruction_notes.md)
check correspondence with the actual implementation. The essential induction
is included here to make the dependency path explicit.

A collected form is a finite rational affine combination of source atoms and
min/max atoms whose children are previously constructed forms. Valuing these
atoms at x and extending affinely gives exactly the recursive term denotation.
Prove this by structural induction, strengthened to a captured local environment.
At a let, collect the right side in the **old** environment and only then extend
it for the body. Source and local names remain distinct. Type-check the whole
original term before erasing zero coefficients. Residuals unfold their actual
definition, and a conversion multiplies by its named rational factor. Therefore
equal collected forms imply equal denotations everywhere, including on unbounded
domains. This is not completeness of equality recognition or a contextual rewrite
oracle; all intermediate values at a point are finite.

Every stored instruction is checked, not only the root's ancestors. Parent
indices are strictly backward, and parents of a non-case rule have the same
local/global scope. For a fixed x in that scope, the sixteen rules are justified
as follows:

| Native tag(s) | Preservation argument |
|---|---|
| constant; row | Exact collected constant; or an actual affine source inequality with its intercept removed and budget retained. |
| rewrite | The normalized difference is unchanged, hence so is its denotation. |
| trans; add | Add the two inequalities; transitivity also checks the common middle expression. |
| scale; convert | Multiply by a nonnegative rational, or the fixed positive conversion factor. |
| negate | Reverse and negate the expression pair; its difference and budget are unchanged. |
| slack | Add only a fixed nonnegative allowance. |
| meet_proofs | The **same** difference is bounded by both budgets, hence their minimum. |
| max_common; min_common | A common old/new expression gives a maximum of the two signed budgets. |
| congruence | Min and max are monotone and preserve a common additive shift, including a negative shift; use the maximum parent budget. |
| res_congruence | The new-minus-old preactivation is bounded by the sum of the two correctly polarized parent bounds; the unchanged zero branch requires its positive part. |
| lattice | The four scalar min projections and max injections have budget zero. |
| all_cases | Every live case appears once, with the literal same expression pair; use the maximum local budget. |

The final normalized-difference check transfers each constructor's result to its
recorded pair. Induction over the finite instruction sequence proves every node
and the designated root. Evaluation at a case witness also shows nonvacuity:
no accepted proof can establish the false constant comparison `0 <=[-1] 0`.
A witness certifies mathematical nonemptiness, not empirical truth.

The request receiver then compares the actual root with the independently
supplied J. A root budget b_out<=B implies the inclusive requested budget B.
A strict request is discharged only by b_out<B. An attaining equality example
prevents silently interpreting an inclusive bound as strict improvement.
Fingerprint and version checks guard against stale data; the argument still
uses the actual checked context and does not treat hashing as physical provenance.

## 3. Producer contracts and the interface repair

[03d](03d_producer_contract_audit.md) proves the producer contracts;
[03e](03e_public_pipeline_reconstruction.md) reconstructs their receiving
boundaries. The complete producer modules, not S3's source slices, were used
in S4's execution. The native checker and original producers are unchanged.

Pruning checks the original proof, retains ancestors in order and renumbers
backward references. Localization selects the requested parent at each
all_cases node and recomputes every other bound. Source transport uses one
closed, unit-correct substitution and current proofs of the required substituted
row **directions**; it recomputes budgets and covers all current cases. It does
not copy an old budget or require an invented whole-old-context inclusion
premise. Substitution preserves ambient identities, not an old domain-restricted
inequality without a domain bridge or new leaves. Observation identifiers alone
are not evidence of deployability.

Primitive expansion preserves the current snapshot's result. Discarding a
currently inferior proof-minimum branch need not preserve later evidence-update
precision. Finite support labels likewise describe their declared fixed-snapshot
reconstruction grammar, not arbitrary proof search or every case-local strategy.

For a localized proof, let B_P be its monotone bound program in row allowances.
A row `a_i<=eta_i` withdrawn from the source contributes
`eta_i + max(a_i-eta_i,0)`. Retained rows contribute eta_i. Reconstruct the native
budget operations to obtain E_P. On the retained local domain,

```
Delta <= E_P = b_h + R_P,    R_P = E_P-b_h >= 0.
```

The penalty is zero whenever the **used** withdrawn rows hold. This is a
proof-relative allowance, not a minimal, small or observable error. The
independent softening receiver reconstructs the revised context, selected rows,
localized baseline, allowance and penalty from old inputs before checking the
requested literal root. A valid proof beside a field called `penalty` is not
enough. Globalizing local allowances requires domain validity for the chosen
combination; an arbitrary maximum need not preserve the local zero-penalty claim.

Supplied affine sign cases compile through this discharge and the native
identity `min(alpha*max(g,0), beta*max(-g,0))=0` for nonnegative gains. Strict
empty-branch rays need exact coefficients and a negative margin. Positive-weight
coverage uses its explicit positive divisors and checked weighted guard bound.
An aggregate-information sharp scalar bound is not necessarily the strongest
bound on a more constrained source domain. CaseResult branch budgets may record
the original live branches rather than a stronger current exclusion result.

### Near-exclusion: exact postcondition versus attached metadata

S3 reproduced the raw `almost_exclusion` boundary: its returned K-valid root
does not by itself authenticate `baseline` or the advertised `new` field. This
is not a counterexample to native soundness or to the valid-input mathematical
transformation. The new **request-bound receiving adapter** checks the fields
against the input proof and the independently supplied request.

For the actual checked allowance `Delta<=A+k*max(g,0)`, k>=0, and a checked
`g<=eta`, monotonicity proves

```
Delta <= A + k*max(eta,0) = M.
```

The adapter uses real native rewrites to bind the input presentation and the
returned literal pair. It checks a candidate's actual budget b_out<=M, permits
a stronger valid candidate, then checks b_out against the requested inclusive
or strict threshold. It validates numerical consistency, not a claim that a
particular historical discharge call created the record. Zero gain and a
nonpositive guard ceiling do not establish strict branch infeasibility.

The prior narrowed contracts remain valid; no earlier native theorem or Gate A
readiness premise is invalidated. The active repair queue is empty. The corrected
receiver boundary is now explicit in the current specification, rather than
being inferred from an unchecked dataclass field.

## 4. A constructive assumption-to-expectation and drift bridge

The new [acceptance audit](../checks/f07_acceptance_audit.py) computes a
sufficient global coordinatewise Lipschitz vector L for the **normalized paired
difference** Delta, not separate envelopes for both absolute objectives.
For a source atom use its coordinate basis vector. For a min/max atom take the
coordinatewise maximum of its children's vectors. For an affine form
`c+sum a_i A_i`, take `sum |a_i| L(A_i)`.

For d_j=|x_j-y_j|, scalar min/max nonexpansiveness and
`max(sum L_1j d_j, sum L_2j d_j)<=sum max(L_1j,L_2j)d_j`
prove the recursion by finite structural induction. Thus

```
|Delta(x)-Delta(y)| <= sum_j L_j |x_j-y_j|,
|Delta(x)| <= |Delta(0)| + sum_j L_j |x_j|.
```

Zero is an ambient assignment, not a presumed feasible point. Closed lexical
normalization precedes memoization. Converted source coordinates retain their
declared numerical unit conventions. The vector need not be minimal: some
semantically cancellable structure is not simplified by this normalizer.

If sources are measurable and the coordinates with L_j>0 have finite first
absolute moments bounded by m_j, then Delta is integrable and
`E|Delta| <= |Delta(0)|+sum L_j m_j`. Together with almost-sure validity of the
requested source domain, a checked pointwise bound gives `E Delta<=b`.
No independence or second moments are required. A canceled common baseline
needs no moment bound. Two absolute objectives can have infinite means while
the paired difference is integrable; never subtract those infinite means.
A one-sided upper bound alone need only give an **extended**, not finite,
expectation. Moment bounds and domain applicability remain external premises.

For fixed program meanings, certified coordinate errors `|x_j-y_j|<=d_j` give
`Delta(y)<=b+sum L_j d_j` when the certificate applies at x. Historical change
instead equals `Delta(y)+J_old(y)-J_old(x)` and needs the additional drift term.
The helper recomputes its envelope from the requested terms; it does not
validate arbitrary caller-provided moment claims or a forged envelope object.

## 5. An independent loss and bounded-reflection model

Let a fixed report r select the second branch with probability r. Component
failure probabilities are p,s, their event price is the declared conversion
factor one, and the second branch's additional use cost is r/4. With common
finite baseline z, `J(r)=(1-r)p+rs+r/4+z`. Compare r0=1/2 and r1=3/4, with a
separately assumed paired proxy-to-intended discrepancy e<=beta. Put
`g=s-p+1/2`. Directly from the program law, independently of proof syntax,

```
Delta = J(3/4)+e-J(1/2) = g/4-1/16+e
      <= beta-1/16 + (1/4)*max(g,0).
```

With beta=1/32 and g<=eta=1/16, Delta<=-1/64. The point
`p=7/16,s=0,e=1/32` attains the bound: old cost is `11/32+z`, new cost
`21/64+z`. All declared probability rows and the guard hold; z is unrestricted.
The difference envelope has weights 1/4,1/4,1,0 on p,s,e,z. Equal p/s coordinate
errors epsilon preserve strict improvement for epsilon<1/32; at equality the
attaining perturbation gives only non-deterioration. This is a modeled
conditional guarantee, not learned calibration or an empirical measurement.

Report validity is a separate numerical question. From p<=1,s<=1/4,
`h(3/4)=p/4+3s/4<=7/16`. **Issuing that old upper bound as the new report changes
the policy.** At the feasible point p=1,s=1/4, `h(7/16)=43/64`, exceeding the
new report by 15/64, and the modeled cost increases by 5/32. A separately
reconstructed fixed report 4/7 has `h(4/7)<=4/7`, with equality attainable.
The new tests check these current requests, their probability unit and their
attaining witnesses using ordinary native instructions.

This example permits staged self-assessment without endorsing its own report.
It does not implement a cyclic theorem/proof system. Calibration and value also
need not coincide: an explicitly added calibration cost changes the criterion,
as worked out in the S4 derivation record. A discrepancy bound for one program
pair or criterion does not automatically apply after that change.

## 6. Acceptance, validation and scope

| F07 obligation | Current evidence and disposition |
|---|---|
| Explicit independent semantics and admitted numeric domain | F05 core; native theorem sections 1–3; sections 1–2 above. Met. |
| Every native rule and finite derivation sound | Complete sixteen-tag source reconstruction, lexical proof and ordered-function cross-check. Met. |
| A model of assumptions | Checked feasible cases; the independently calculated attaining policy point above. Met. |
| Nontrivial example independent of syntax | Direct branch-law, resource-cost and discrepancy calculation, then native proof/receiver agreement. Met. |
| Known countermodels handled | Local versus union validity; nonlinear means; inaccessible observations; source drift; strict equality; producer metadata; report update. Assumptions or receiving checks exclude the overclaims. Met. |
| Current producer postconditions | S2/S3/S4 reconstruction and complete-module regressions. Method-specific metadata is not equated with K validity. Met. |
| Measured derivation floor | S4 D30 and cumulative F07 D90 satisfied in the linked actuals and appended ledger. Met. |

Final targeted counts: **186 F07, 171 F06, 90 F05, 202 F04, 256 F03, 124 F02,
17 Gate A: 1,046 tests**. F07 contains 108 published, 47 S3 and 31 S4 tests.
Finite enumerations supplement the written universal arguments; they do not
prove them by sampling. Initial fixture errors, corrections, commands and
outputs are retained in [S4](../work_logs/F07_2026-09-28_S4.md).

The working source is a public-version-verified **overlay**, not a full clone.
The full `python -m verification` command and new GitHub CI are not claimed.
F07 completion is the scoped mathematical task decision, not a Gate B pass or
completion of F11/F16. Gate A retains its foundation-readiness-only PASS; B/C/D
are unattempted. The core stays provisional. **Next: F08, unstarted.**
