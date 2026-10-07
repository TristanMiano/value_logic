# P3-01 counterfactual response-status stress test

Contributor: **ChatGPT (GPT-6 Astra Pro)**, same-model internal delegated reviewer.
Date: October 7, 2026 UTC. Scope: operational adequacy of the P3-01 interface.
This note does not select a counterpossible semantics or implement a P3-04
calculus. It inspects the revised problem contract §7 and duties C01–C04/I01.

## 1. A response needs a typed product with consistency conditions

The request already states what is being asked. The answer must say what was
actually established. A suitable abstract product is

```
Response = (request/version identity,
            scope and operation,
            search/feasibility status,
            selection identity and coverage,
            numerical form and meaning,
            evidence and resource account).
```

The fields are separately reported but are not arbitrary independent choices:
some combinations are invalid. This is a requirements schema, not a permanent
carrier or software API.

### 1.1 Scope and operation

Retain the request ID, base and target scope versions, history, antecedent,
retained semantics, and operation tag. The tags include set/probability
conditioning, state intervention, specified program replacement, model repair,
and mathematical counterpossible evaluation. A repaired interpretation needs
an explicit translation and cannot masquerade as the original fixed-meaning
counterpossible.

An infeasibility certificate names its domain. Proving that no classical model
satisfies an impossible antecedent does not prove that a separately proposed
impossible-world semantics has no selected cases. Conversely, if that latter
semantics has not been supplied, the response is undefined because semantics
are missing; the solver must not silently substitute its classical search space.

### 1.2 Search and feasibility

| Search state | Exact minimal meaning | Required evidence |
|---|---|---|
| `unknown` | No verified admissible candidate and no infeasibility certificate have been obtained | Reason such as budget exhaustion, incomplete validation, absent semantics or execution failure; no negative-existence inference |
| `certified_infeasible` | No admissible candidate exists in the named domain | Complete finite coverage or a valid impossibility certificate, with dependencies |
| `candidate` | At least one admissible candidate is verified; global optimality is not established | Candidate witness and validation; searched region and remaining budget |
| `optimal` | At least one admissible candidate attains the globally minimum declared rank | Feasible witness plus a global lower-bound/optimality certificate |

For a request with no genuine ranking, use a declared constant rank, so the
same interface can represent feasibility without pretending that a substantive
optimization occurred. An open-ended search that merely has not found a
better candidate remains `candidate`.

**Optimality is not complete tie coverage.** A rank-zero candidate with a
known universal nonnegative rank bound is optimal immediately, even if other
rank-zero candidates have not been inspected. Their consequences can differ.

### 1.3 Selection identity and coverage

| Selection state | Meaning |
|---|---|
| `unique_consequence` | All relevant optimal candidates have the same requested consequence; this can hold even with multiple candidate identities |
| `set_of_tied_consequences` | The response characterizes the consequences of all equally selected candidates, with non-singleton support |
| `policy_selected` | A named policy selected a candidate, subset or distribution; its domain and tie rule are given |
| `unresolved` | Candidate consequences may be known, but the requested global consequence family or its selection is not established |
| `not_applicable` | No defined selected family exists, for example after certified infeasibility or a missing interpretation |

Also report coverage of the relevant family: `complete_by_enumeration`,
`complete_by_certificate`, `partial`, or `not_defined`. A complete enumeration
of repairs is unnecessary if a proof establishes consequence invariance over
all of them. A global optimum witness alone does not establish that invariance.

A policy must say whether it acts over **all global minimizers** or just the
validated candidates found within budget. Both can define useful bounded
behavior, but they are different policies. Choosing one branch of a tie does
not establish that the other branch is impossible or less preferred under the
original ranking.

### 1.4 Numerical shape and meaning

| Numeric form | What it means and what remains explicit |
|---|---|
| `point` | One number in a declared unit, labeled as an exact unique consequence, policy value, candidate value, or fallible forecast |
| `interval_hull` | The hull of a stated consequence set; retain whether it is the exact hull or only a certified outer enclosure, and which endpoints/interior values are attainable |
| `unbounded` | A nonempty relevant consequence family is unbounded in a specified direction; infinity is a range marker, not automatically a pointwise realized cost |
| `undefined` | No numerical answer of the requested kind is supplied; reason distinguishes infeasible domain, missing semantics, no result within budget, and evaluation failure |

For strict naming, an enclosure that is not known sharp is an **outer interval
bound**, rather than an exact interval hull. An empirical forecast interval
must carry its forecast/coverage status; it does not become a certified hull.
Finite support such as `{1,3}` may be preserved in the selection field and
summarized numerically by its hull `[1,3]`.

Evidence labels distinguish conditional mathematical certification from an
empirical estimate and its optional calibration/coverage claim. A confidence
number may accompany a well-defined forecast, but must name its target. It does
not identify the scope, replace a witness, or certify complete search.

### 1.5 Essential cross-field rules

1. `certified_infeasible` has no nonempty selected cost family: its requested
   counterfactual cost is `undefined`, even if an internal optimizer uses an
   infinity sentinel. The certificate remains useful information.
2. `optimal` plus one computed cost does not license `unique_consequence`.
   Require complete tie coverage or a consequence-invariance certificate.
3. `policy_selected` plus an exact point is permitted when the policy and its
   selected domain are defined; this does not imply structural identification.
4. An outer bound over every admissible case can coexist with unknown
   feasibility. Its existence premise remains unresolved, so it supplies no
   nonvacuous action warrant by itself.
5. A change from state intervention to mathematical counterpossible changes
   the scope/operation even if the displayed numerical value happens to agree.

These rules permit acting under an explicitly uncertain bounded policy. They
restrict the **claims attached to its output**, rather than requiring complete
counterfactual knowledge before every action.

## 2. Four compact stress examples

The objection is semantic, not a cardinality theorem. Two real numbers could
encode an entire record by an agreed coding scheme. If one number is presented
as task loss and the other as confidence in that loss, however, their numerical
interpretation does not supply the missing claims below. Encoding the flags
inside them would still require the same explicit decoding contract.

### ST01 — no candidate found versus certified infeasibility

A finite catalogue has two entries. With budget one, the solver checks the
first and rejects it. In catalogue `K_good`, the second is admissible and has
loss zero; in `K_empty`, the second is inadmissible too. The first observed
search result is identical. Neither a default loss zero nor confidence zero
establishes infeasibility. The budget-one result is `unknown`; complete
inspection of `K_empty` can yield `certified_infeasible`. That certificate
still does not produce a numerical cost for a selected case.

This is also why no-result and evaluation failure need reasons: a failure of
the checker to run is not a proof that the candidate violated a constraint.

### ST02 — an exact policy value is not a unique consequence

Use the tied-deletion fixture from `counterfactual_contract_review.md`.
Both minimum repairs have rank two and yield losses one and three. A declared
optimistic tie policy returns the exact value one. A different request whose
every minimum repair has loss one also returns exact value one. The scalar can
be fully verified in both cases, yet the first response is `policy_selected`
with identified support `{1,3}`, and the second can be `unique_consequence`.

Even `optimal` is insufficient: a first inspected candidate with rank zero
and loss one is globally optimal under a known nonnegative rank bound, but an
uninspected rank-zero candidate may have loss three. The optimum certificate
and all-minimizer consequence certificate answer different questions.

### ST03 — setting a state bit does not evaluate impossible arithmetic

In a Boolean state model, overriding an output register from zero to one and
charging loss equal to its new value has exact cost one. In a mathematical
request, let that bit instead report “sqrt(2) is a ratio of usual integers.”
Overwriting the report bit still produces the integer one, but does not define
the consequences of that fixed-meaning mathematical counterpossible. It has
changed a report state, not supplied an impossible-state evaluation rule.

The arithmetic evaluation of the register can be perfectly verified while
the requested counterpossible answer remains `undefined: missing_semantics`.
The operation/scope tag prevents this substitution.

### ST04 — unbounded possibilities versus no defined possibilities

Let the admissible family be all integers `n>=0`, every candidate have rank
zero, and the requested cost be `L(n)=n`. The consequence family is nonempty
and unbounded above: for any proposed finite upper bound, a larger integer
is a witness. Every individual cost is nevertheless finite.

An empty selected family, an unsearched catalogue, and a cost evaluator that
failed do not have that property. A single infinity/sentinel value with a
confidence field would hide the difference. The appropriate responses retain
`unbounded_above` with its witness argument, or `undefined` with the relevant
reason. This example concerns a range property; it does not add infinite
pointwise costs to phase two's finite-valued term language.

## 3. Simplest fully specified successful finite request

This is a state-intervention request with a constant ranking. It succeeds
without claiming any general mathematical-counterpossible capability.

### Request

| Field | Specification |
|---|---|
| Request/version | `P3-01-CF-SUCCESS-v1`; all referenced records have this version |
| Language/interpretation | Boolean `U,A,B`; ordinary integer arithmetic for a rationally priced loss account |
| Base scope | `E_A: A=U`; `E_B: B=A`; `E_L: L=2+A-2*B` |
| History | The observed exogenous input is `U=0`; `A` is the action and `B` a later dependent output, so no previously observed `B` value is overwritten |
| Antecedent/operation | State intervention `A<-1` |
| Retained hard constraints | `U=0`, Boolean domains, `E_B`, `E_L` |
| Admissible changes | Replace only `E_A` by `A=1`; no other repairs, function changes or interpretation changes |
| Propagation | Recompute `B`, then `L`; history `U=0` stays fixed |
| Candidate universe/order | After fixing `A=1`, audit `B=0`, then `B=1` |
| Ranking | Constant zero for every admissible candidate; no substantive preference among solutions |
| Tie rule | Return all solution consequences, with no outcome-based tie selection |
| Loss query | Modeled task loss `L`, in declared task-loss units; report computation charges separately |
| Evidence | Supplied equation IDs `E_A,E_B,E_L`, history ID `H_U0`, intervention transformation, and the complete two-entry audit |
| Kernel budget | At most two candidate audits and three integer arithmetic operations for the one accepted assignment; at most one accepted assignment retained |
| Kernel prices | `1/10` task-loss unit per candidate audit; `1/100` per integer arithmetic operation |

These are explicit **toy kernel units**: one audit checks `B=A`; cost evaluation
uses multiplication, addition and subtraction. Fixed request decoding, recording
and presentation are common unpriced overhead outside this toy kernel account.
This is an interface example, not a claim about total hardware cost or an
efficiency advantage. A real challenge must extend the resource model to its
material implementation costs.

### Complete derivation and response

`B=0` fails the retained equation `B=A` when `A=1`; `B=1` satisfies it. There
are no other Boolean candidates. The unique assignment is `(A,B)=(1,1)`, its
rank is zero, and its task loss is one. This establishes both feasibility and
complete consequence coverage.

```json
{
  "request_id": "P3-01-CF-SUCCESS-v1",
  "scope_type": "state_intervention",
  "operation": "replace_E_A_by_A_equals_1",
  "history_retained": {"U": 0},
  "search": {
    "state": "optimal",
    "minimum_rank": 0,
    "witness": {"A": 1, "B": 1},
    "certificate": "all_B_in_0_1_audited"
  },
  "selection": {
    "state": "unique_consequence",
    "target": "all_global_minimizers",
    "coverage": "complete_by_enumeration",
    "consequences": [1],
    "policy_selected": false
  },
  "numeric": {
    "kind": "point",
    "value": 1,
    "meaning": "exact_unique_modeled_task_loss",
    "unit": "task_loss",
    "validity": "conditional_on_H_U0_E_B_E_L_and_declared_intervention"
  },
  "evidence_ids": ["E_A", "E_B", "E_L", "H_U0", "complete_two_entry_audit"],
  "resources": {
    "candidate_audits": 2,
    "integer_arithmetic_operations": 3,
    "priced_kernel_resource_cost": "23/100",
    "task_plus_priced_kernel_cost": "123/100",
    "unpriced_common_overhead": "outside_toy_kernel_account"
  }
}
```

The response's confidence is not a substitute for its conditional premise
record. Empirical adequacy of the supplied structural equations is a different
question from the exact calculation under them.

## 4. Check and resource record

A CPython **3.12.14** standard-library enumeration checked the two candidates,
the unique result and exact `Fraction` charges. It passed with audit results
`B=0:false`, `B=1:true`, task loss `1`, priced kernel cost `23/100`, total
`123/100`. This is P3-01 development arithmetic, not final evaluation.

Inner check start UTC: `2026-10-07T01:08:21.417975+00:00`, monotonic
`28470725140286`; end UTC: `2026-10-07T01:08:21.418044+00:00`, monotonic
`28470725173536`. The matched inner interval is 33,250 ns. Reviewer engaged
research duration, inference-token usage and monetary cost are **unknown**;
no concurrent reviewer time is added to the principal clock. No canonical
document, ledger or experiment marker was changed by this reviewer.
