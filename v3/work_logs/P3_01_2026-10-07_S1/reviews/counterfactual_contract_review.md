# P3-01 adversarial counterfactual contract review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, same-model internal delegated reviewer.
Date: October 7, 2026 UTC. Scope: P3-01 requirements and separating examples;
not P3-04/05 execution or a gate recommendation.

Reviewed working versions of `v3/foundations/01_problem_contract.md` and
`01_desiderata.md`, with special attention to the counterfactual request,
C01–C04 and I01. The referenced separating-examples file did not yet exist
when this review tried to open it. That is an in-progress dependency, not an
assertion that the completed deliverable is missing.

## 1. Review disposition

The central distinctions are sound: conditioning is separated from intervention,
replacement has explicit propagation, genuine counterpossible reasoning is
not silently supplied by interpretation repair, and an empty selected family
does not warrant a favorable action. No redesign is needed. The following
local clarifications would make the contract harder to misapply.

| Issue | Why it matters | Suggested contract change |
|---|---|---|
| CF-R01: “nonempty conditional event” is insufficient for ordinary probability conditioning | A nonempty event can have probability zero, so division by its probability is undefined | Distinguish nonempty set restriction from positive-probability ordinary conditioning; an alternative zero-probability convention must be specified |
| CF-R02: bounded search needs its own unresolved statuses | Finding no repair within a budget does not prove that no admissible repair exists, and best-found need not be globally minimal | Distinguish certified infeasible, none found within budget, candidate found/minimality unproved, and certified optimum |
| CF-R03: inconsistency with factual assumptions is not automatically logical impossibility | A theory containing a contingent fact `P` is inconsistent with `not P`, although `not P` can be possible | Name the retained mathematical/semantic background defining the counterpossible; distinguish conflict with actual-state facts and theory-relative exclusion |
| CF-R04: the operation table omits an explicit actor-only row | C01 requires distinguishing it, while the table says the request selects among the listed kinds | Add actor-only replacement or rename the replacement row to cover an explicit propagation mask and identify the actor-only case |
| CF-R05: an announced tie policy supplies an operational answer, not identified structure | A deterministic tie policy can return one cost even when equally preferred admissible models disagree | Label “selected by policy” separately from “uniquely implied by structural information”; uniqueness of cost also need not imply uniqueness of the underlying repair |

CF-R03 is primarily a terminology/scope clarification. If the intended convention
is explicitly “counterpossible relative to retained mathematical background,”
that is a workable local target. The definition must not accidentally treat
every intervention contrary to the actual facts as a genuine counterpossible.

The [Berto et al. source](https://link.springer.com/article/10.1007/s10992-017-9446-x),
§§1–2, defines counterpossibles by impossible antecedents and permits classical
evaluation at possible worlds in its sample nonvacuist semantics. Thus the
contract's new evaluation rule need not imply abandoning classical reasoning
globally. The earlier delegated source note provides the exact import boundary.

## 2. Exact equal-cost minimal-deletion fixture

### 2.1 Syntax and admissible operation

Let `A,B` be Boolean. The antecedent `A=1` is a **hard** added constraint.
The original soft constraints are three identified records:

```
r1: A=0
r2: B=0
r3: A=B
```

The original conjunction has the single assignment `(A,B)=(0,0)`. A repair
may delete any subset `D` of these three records. It may not rewrite a
constraint, delete the antecedent, change Boolean meanings, or introduce
another variable. It is admissible exactly when the remaining constraints
plus `A=1` have a Boolean solution. Rank admissible repairs by `d(D)=|D|`.
This defines edit cost, independently of the task loss

```
L(A,B)=2+A-2*B.
```

### 2.2 Exhaustive reasoning

Every admissible repair must delete `r1`, because it directly conflicts with
the hard antecedent. Keeping both `r2` and `r3` would force `A=B=0`, also
incompatible with `A=1`. Therefore every admissible repair deletes `r1` and
at least one of `r2,r3`. Exactly three deletion sets are admissible:

| Deleted records | Edit cost | Retained soft constraints | Solutions under `A=1` | Task loss |
|---|---:|---|---|---|
| `{r1,r2}` | 2 | `A=B` | `(1,1)` | 1 |
| `{r1,r3}` | 2 | `B=0` | `(1,0)` | 3 |
| `{r1,r2,r3}` | 3 | None | `(1,0),(1,1)` | `{3,1}` |

Thus the first two are **all** globally minimum-cost repairs, both with cost
two. The optimum does not determine a unique task loss. The exact retained
loss set is `{1,3}`; its interval hull is `[1,3]`. There is no intermediate
realized cost in this fixture, although an expectation under a supplied mixing
law could lie between the two values.

The distinction between an interval hull and actual attainable costs matters:
using `[1,3]` as a robust numerical bound is legitimate, while claiming every
point is an available repair would alter the candidate family.

### 2.3 What stronger ranking or structure would need to add

Give the three records strictly positive deletion weights `w1,w2,w3`.
The two relevant repair costs become

```
delete {r1,r2}: w1+w2, yielding loss 1
delete {r1,r3}: w1+w3, yielding loss 3.
```

If `w2<w3`, preserving equality is cheaper and loss one is selected. If
`w3<w2`, preserving `B=0` is cheaper and loss three is selected. Equality of
those weights preserves the tie. Positivity ensures deleting all three cannot
improve the ranking. Marking `A=B` hard selects the first branch; marking
`B=0` hard selects the second; marking `A=0` hard makes this repair language
infeasible for the hard antecedent.

These are **additional commitments**, not facts obtained from the original
equal-weight fixture. A causal/functional certificate might justify preserving
one equation. A declared source-reliability or relevance preference might
justify weights. A preannounced tie rule might choose one branch. A separate
mixing model might justify an expected loss. Each answers a more specified
question. The symbols `A=B` alone do not certify causal dependence.

Choosing lower task loss as a secondary objective is permitted as optimistic
planning if announced. It must not be presented as discovering the unique
counterfactual consequence. Robust planning instead uses the worst retained
loss. Neither policy erases the underlying tie.

## 3. Exact refactoring failure of raw edit distance

This fixture also supplies a small representation test. Treat the displayed
soft records as a list, so deleting each syntactic occurrence costs one. Copying
an existing assertion below is a **presentation-only duplication of the same
evidence identity**, not a new independent observation.

### 3.1 Duplicate the equality

Replace the original list by

```
A=0; B=0; A=B; A=B.
```

The unmodified conjunction has exactly the same models as before. After adding
hard `A=1`, retaining equality and deleting `A=0,B=0` still costs two and
yields `(1,1)`, loss one. Retaining `B=0` requires deleting `A=0` and **both**
equality occurrences, costing three. The minimum is now unique and selects
loss one.

### 3.2 Duplicate the fixed B value instead

Alternatively present

```
A=0; B=0; A=B; B=0.
```

Again the original models are unchanged. Deleting `A=0,A=B` costs two and
yields `(1,0)`, loss three. The branch preserving equality must now delete
`A=0` and both `B=0` occurrences, costing three. The unique selected loss
becomes three.

| Presentation of the same original constraints | Minimum edit cost | Losses from all minimizers |
|---|---:|---|
| One occurrence of each | 2 | `{1,3}` |
| Duplicate `A=B` | 2 | `{1}` |
| Duplicate `B=0` | 2 | `{3}` |

This proves that raw per-occurrence deletion distance is not invariant under
redundant assertion duplication. It is not a universal impossibility theorem
about program similarity, nor does it establish a canonical repair metric.
It also does not refute a representation equivalence that transports edit
operations and weights: the raw per-occurrence rule fails to perform that
transport, which is exactly the problem the fixture exposes.
Deduplicating by evidence identity would resolve this particular fixture.
Whether a broader representation contract should preserve invariance under
inlining, factoring or semantic equivalence belongs to P3-05. If the syntax
itself is intentionally part of the task, the measured dependence should be
declared instead of calling it an invariant notion of nearness.

## 4. Verification and resources

A CPython **3.12.14**, standard-library-only development enumeration checked
every deletion subset of the three presentations and all four Boolean
assignments. For each subset it required hard `A=1` and all retained records,
then selected every globally minimum cardinality subset. The checks passed:

```json
{
  "status": "pass",
  "base": {"feasible_deletion_sets": 3, "optimum": 2,
           "minimum_losses": [1, 3]},
  "duplicate_EQ": {"feasible_deletion_sets": 5, "optimum": 2,
                   "minimum_losses": [1]},
  "duplicate_B0": {"feasible_deletion_sets": 5, "optimum": 2,
                   "minimum_losses": [3]}
}
```

The algorithm was exhaustive over `2^3 + 2^4 + 2^4 = 40` deletion subsets
and four assignments per subset, not a statistical experiment. The logical
arguments above independently reconstruct the same result. This is P3-01
development data; no final evaluation population was generated.

The inner check recorded start UTC `2026-10-07T00:53:53.610310+00:00`,
monotonic `27602917452731`, and end UTC
`2026-10-07T00:53:53.610436+00:00`, monotonic `27602917565902` in one runtime.
The inner interval is 113,171 ns; it is not a reviewer engaged-time estimate.
Reviewer research time, inference-token usage and monetary cost are **unknown**
and are not added to the principal's clock. The attempt to read the not-yet-created
examples file returned “No such file or directory”; no frozen attempt or retry
contract was involved. Only this reviewer note was written.
