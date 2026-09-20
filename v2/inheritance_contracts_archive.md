# Follow-Up Paper Workspace: Inheritance Boundary

Completed for Task 0: 2026-08-01

This directory develops the contract-semantics and inverse-task-recovery
follow-up controlled by [`TODO_v2.md`](../TODO_v2.md). The follow-up starts
from the published finite-stage license calculus in [`paper.md`](../paper.md);
it does not rebuild that calculus or silently replace its evidence and
provenance discipline with one scalar.

## Authoritative inheritance table

| status | object or result | first-paper source | follow-up treatment |
|---|---|---|---|
| Imported unchanged | Versioned evaluated plans $e\in E$, reliance contexts $q\in Q$, finite epistemic states $s\in S$, world indices $w\in W$, and finite profiles $P$ | [§3.1](../paper.md#31-three-operational-carriers-and-a-profile) | Retain their roles and the request base $(s,e,q,P)$. Contracts add a semantic view of selected numerical requirements; they do not replace plan, context, state, or profile identity. |
| Imported unchanged | Context fields: domain $D_q$, task and frame, target loss, aggregation, acceptable region, fallback $F_q$, advantage $\Delta_q$, constraints, units, and certificate modes | [§3.1](../paper.md#31-three-operational-carriers-and-a-profile), [Appendix A.1](../paper.md#a1-carriers-and-dependent-fields) | Keep these fields typed. A scalar payoff is meaningful only after the relevant criterion, aggregation, units, and fallback have been fixed. |
| Imported unchanged | The separation of failed well-formedness from meaningful evidence, $K_3=\{\mathsf{Refuted},\mathsf{Open},\mathsf{Supported}\}$, indexed diagnostics, and the four public outcomes | [§3.2](../paper.md#32-profiles-typed-atoms-and-assessment), [Appendix A.2](../paper.md#a2-well-formedness-diagnostics-and-assessment) | `Undefined` remains outside the contract sign abstraction. Meaningful contract atoms retain witnesses, obstacles or counterwitnesses, and provenance rather than becoming bare labels. |
| Imported unchanged | Licensing before selection, exact active-set masking, explicit fallback on gaps, and the distinction among current authorization, finite comparison, selection, and archival retention | [§3.3](../paper.md#33-licensed-consequence-selection-and-revision), [§6.3](../paper.md#63-from-a-positive-number-to-a-licensed-feature) | Contract value cannot reactivate an unlicensed plan or certify the fallback as safe. Selection continues to consume the exact licensed active set. |
| Reinterpreted through contracts | Absolute adequacy $J(e,D_q)\leq\epsilon_q$ | [§2.1](../paper.md#21-from-local-usefulness-to-a-reliance-threshold), [§3.2](../paper.md#32-profiles-typed-atoms-and-assessment) | Use the favorable-payoff contract $A_{e,q}(w)=\epsilon_q-J(e,D_q;w)$. Task 10 must prove the exact evidential embedding; this row records the intended interface only. |
| Reinterpreted through contracts | Improvement over the named fallback | [§2.1](../paper.md#21-from-local-usefulness-to-a-reliance-threshold), [§3.2](../paper.md#32-profiles-typed-atoms-and-assessment) | Use $X_{e,q}(w)=J(F_q,D_q;w)-J(e,D_q;w)-\Delta_q$. Positive payoff favors $e$; absolute adequacy remains a separate requirement. |
| Reinterpreted through contracts | Accepted certificate regions and conservative numerical margins | [§6.2](../paper.md#62-error-bands-and-the-finite-relu-witness), [Appendix D.2](../paper.md#d2-conservative-boundary-recovery) | Study lower and upper valuations $[\underline V_s(X),\overline V_s(X)]$. An old loss interval is not automatically such a valuation interval; the representation assumptions must be stated. |
| Reinterpreted through contracts | Profile atoms and Boolean-looking conjunction | [§3.2](../paper.md#32-profiles-typed-atoms-and-assessment) | A profile remains a finite typed family followed by conservative meet. Indicator contracts will embed a Boolean fragment, while `min` and `max` on arbitrary real payoffs will not be called logical conjunction and disjunction without qualification. |
| Used as a premise | Consumer-relative exact factorization: an exact code must preserve every distinction required by its declared observation family | [§6.1, Theorem 10](../paper.md#61-what-an-implementation-must-preserve), [Appendix D.1](../paper.md#d1-exact-inputs-public-quotients-and-audit-codes) | Adapt this result to response families of priced contract queries. The response image, not a hidden mechanism or uniquely true utility, is the candidate coarsest exact task code. |
| Used as a premise | Exact-state and side-packet discipline: payload, grade, evidence, units, identity, validity, provenance, mask, and fallback can require separate channels | [§6.1](../paper.md#61-what-an-implementation-must-preserve), [§6.3](../paper.md#63-from-a-positive-number-to-a-licensed-feature) | The primary contract carrier must be paired with whatever exact side information its declared consumers need. Task 1 will decide the final carrier presentation. |
| Outside this follow-up | Continuation stability, typed update locality, proof-carrying plan composition, routed-risk and path-sensitivity theorems | [§§4–5](../paper.md#4-open-succession-and-local-revision) | Available background, but not theorem targets for the contract/inverse paper. They may be cited only when an interface boundary requires them. |
| Outside this follow-up | ReLU exact-representation, seam and learning claims; the completed structured-versus-cross-entropy experiment | [§§6–7](../paper.md#6-architecture-neutral-representation-and-a-relu-reference) | Do not rerun, extend, or reinterpret the first experiment. The follow-up implementation is a small architecture-neutral contract/oracle reference plus a separately frozen active-query experiment. |
| Outside this follow-up | Policy/value behavioral reconstruction, recursive-judgment information, mechanistic interpretation, and true-utility recovery | [§8](../paper.md#8-optional-policyvalue-and-recursive-judgment-bridge), [Conclusion](../paper.md#11-conclusion) | The observational-quotient lesson survives, but these results are not premises for identifying a task from contract judgments. Mechanistic and true-utility readings remain excluded. |

## Exact inherited formulas and boundaries

The first paper defines domain risk by

$$
R_{D,L}(e)=\rho_D\left(z\mapsto\ell_L(e,z)\right),
\qquad R_{D,L}(e)\leq\epsilon
$$

for adequacy after the loss and aggregation are declared. With smaller-is-
better combined task loss and use cost $J$, its fallback formulas are

$$
s_B(e,D)=J(B,D)-J(e,D)-\Delta,
\qquad
\epsilon_B(D)=J(B,D)-\Delta.
$$

For certified loss regions $U_e,U_F$, fallback improvement is Supported when

$$
\sup U_e+\Delta\leq\inf U_F,
$$

Refuted when $\inf U_e+\Delta>\sup U_F$, and Open under missing or overlapping
comparison evidence. The common region rule is

$$
U_{\mathrm{cert}}\subseteq A\Rightarrow\mathsf{Supported},
\qquad
U_{\mathrm{cert}}\cap A=\varnothing\Rightarrow\mathsf{Refuted},
$$

with missing, conflicted, expired, or boundary-crossing evidence Open. Thus
favorable equality is inclusive, while refutation requires strict separation
onto the unfavorable side.

For a nonempty required address set, the inherited profile rule is

$$
\mathsf{ReqVal}(s,e,q,P)
=\bigwedge_{a\in\mathsf{Req}(P)}\nu_s(e,q,a),
$$

where the meet is the minimum under
$\mathsf{Refuted}<\mathsf{Open}<\mathsf{Supported}$. Failed $WF$ gives
`Undefined`; otherwise the three meet values give `Refused`, `Withheld`, and
`Granted`.

Finally, for a declared observation $N$ and code $c$, the inherited
consumer-factorization theorem is

$$
\ker(c)\subseteq\ker(N)
\quad\Longleftrightarrow\quad
\exists d:\ d\circ c=N.
$$

Here kernels are equality relations induced by arbitrary maps. The image of
$N$ is the coarsest exact code up to relabeling. The inverse paper will apply
this only after fixing whether $N$ exposes public states or finer audit
responses.

## Unresolved interface questions

1. Is the paper's primary object a bounded real contract plus an exact side
   packet, or a typed bundle of several contracts and exact predicates?
2. When does an accepted first-paper certificate region induce lower and upper
   valuations, and when is it merely an external interval interface without a
   credal-set representation?
3. Does $J(e,D_q;w)$ already include the context's domain aggregation in world
   $w$, or must contracts be case-indexed before aggregation? The follow-up
   must choose one level and avoid double aggregation.
4. Which hard constraints and provenance obligations remain exact predicates
   because scalarization would erase units, priority, or authorization data?
5. Is the inverse oracle's observation family public-state only, or can a
   separately declared audit oracle reveal diagnostics? These induce different
   observational quotients.
6. Which contract and price queries are admissible for an actual judge, and
   which normalizations are required before any finite-dimensional recovery
   claim is meaningful?

## Validation command

Until Task 24 creates the follow-up verification package, validate every v2
work item from the repository root with:

```text
python -m verification
```

Task 24 is expected to add `python -m v2.verification` and update this section.
