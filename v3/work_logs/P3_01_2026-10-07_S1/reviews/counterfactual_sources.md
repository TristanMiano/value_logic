# P3-01 delegated source and counterfactual reconstruction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, same-model internal delegated reviewer.
Date: October 7, 2026 UTC. Scope: questions/comparison contract only. This is
not execution of P3-04/05, an adopted counterfactual semantics, or a gate decision.

## 1. Exact primary interfaces

The following are deliberately restricted imports. The separating constructions
below are our own elementary examples; no newness is asserted for them.

### Halpern: structural intervention and its existence condition

Joseph Y. Halpern, *Axiomatizing Causal Reasoning*, JAIR 12 (2000), 317–337.
[Primary paper](https://arxiv.org/pdf/cs/0005030), retrieved v1.
Read §2.1, printed pp. 318–319, and §§2.2–2.3, pp. 320–321.

A finite signature specifies exogenous/endogenous variables and their ranges.
A structural function for each endogenous variable determines its value from
the other variables. Intervention fixes selected endogenous variables, removes
their equations, and substitutes their assigned values into the remaining
functions, with the exogenous context fixed. Acyclicity guarantees a unique
solution. General cyclic models can have zero, one, or multiple solutions.
The universal intervention modality quantifies over solutions; it is vacuously
true if there are none. Its existential dual can express solution existence.

**Import boundary:** this supplies a precise ordinary comparator when equations
are given. For an action warrant, value_logic must retain its additional
nonempty-context guard. Acyclicity is sufficient, not necessary, for uniqueness.
No result here identifies the correct equations from a cost table.

### FDT: a dependency interface is supplied, not inferred by the value

Eliezer Yudkowsky and Nate Soares, *Functional Decision Theory: A New Theory
of Instrumental Rationality*, [arXiv:1710.05060](https://arxiv.org/pdf/1710.05060),
retrieved v2. Read §3's type/token and alternative-function discussion, and
§5, equations (2)–(4), especially equation (4) and footnote 9.

The paper distinguishes changing an action token, counterpossibly changing the
output of the existing decision function, and implementing another decision
function. Its Newcomb discussion explains why a predictor of the original
function need not track the replacement function. Its graphical formulation
assumes a graph specifying how the relevant logical-variable intervention
affects other variables, then uses intervention on that supplied graph. The
authors do not give a general construction of a logical-truth intervention
operator and explicitly supply the dependency structure as input.

**Import boundary:** use this as a dependency-sensitive decision comparator.
Program replacement is a meaningful restricted operation, but it does not
automatically implement FDT's fixed-function counterpossible. The paper's
2018 open-problem assessment is historical; this reading makes no claim that
it settles the state of the entire field in 2026.

### Spohn: numeric ranks revise disbelieved possibilities

Wolfgang Spohn, *Ordinal Conditional Functions: A Dynamic Theory of Epistemic
States* (1988). [Primary scan](https://d-nb.info/110069062X/34).
Read §§4–5, Definitions 4–6, printed pp. 115–117.

An ordinal conditional function assigns grades of disbelief to worlds, with
at least one world at grade zero, and is constant within the atoms of the
specified proposition field. A nonempty event's grade is the minimum grade
of its worlds. Event conditionalization shifts its part down to zero and
shifts the complementary part to the chosen firmness; internal rank
differences are preserved. Definition 6 requires both event and complement
nonempty. These ranks are not probability masses: event aggregation uses a
minimum, not summation.

**Import boundary:** graded revision and adjustable firmness already exist.
The definition can accommodate an event formerly disbelieved, but not an
empty impossible event in its world space. Real-valued repair scores are not
automatically this ordinal update rule; an exact translation would need proof.

### Berto et al.: impossible worlds need specified selection and evaluation

Francesco Berto, Rohan French, Graham Priest and David Ripley,
*Williamson on Counterpossibles*, JPL 47 (2018), 693–713; published online
2017. [Primary article](https://link.springer.com/article/10.1007/s10992-017-9446-x).
Read §§2.1–2.3, especially §2.3's interpretation and accessibility conditions.

The sample semantics includes possible and impossible worlds, with formula
truth assigned directly at impossible worlds. An antecedent-indexed relation
selects worlds for the conditional. Discussed constraints include selecting
antecedent worlds, weak centering, and using possible worlds when the antecedent
is possible. The framework permits nonvacuous counterpossibles without making
ordinary propositional reasoning nonclassical at possible worlds.

**Import boundary:** merely adding impossible worlds does not choose relevant
ones or force a nonempty selected family for every antecedent. To derive a
particular numerical counterfactual, we must supply selection, consequent/cost
evaluation, and existence conditions. This is a comparison interface, not a
complete ready-made semantics for arbitrary arithmetic hypotheticals.

### Revision versus update: retained reading limitation

The available publisher introduction to Katsuno and Mendelzon's
[*On the Difference between Updating a Knowledge Base and Revising It*](https://www.cambridge.org/core/books/abs/belief-revision/on-the-difference-between-updating-a-knowledge-base-and-revising-it/8ADFFF65FA776C21E8646D6F4D2434AB)
distinguishes information about a static world from a change in the described
world. A targeted second-engine and then first-engine search did not produce
the full primary chapter: a PDF-looking Cambridge result still delivered its
access/summary page; a separate result was a 2008 seminar deck and was not
treated as the original paper. No full AGM/KM theorem has been imported here.

## 2. Four different operations on the same actual state

Fix the complete input/history `h`. Let the existing function satisfy
`f0(h) = 0`, and write

```
Z = f0(h)
A = Z
B = Z
L(A,B) = 2 + A - 2*B,       A,B in {0,1}.
```

The actual state is `(A,B,L) = (0,0,2)`. `A` is an actor output; `B` is another
use associated with the original function. The loss is nonnegative over all
four binary assignments. The phrase “if A were 1” leaves these alternatives:

| Operation | Exact retained/changed structure | A | B | Loss |
|---|---|---:|---:|---:|
| Evidence conditioning | Retain every equation and add `A=1` | No state | No state | Undefined |
| Token override | Replace only the equation for `A` by `A=1` | 1 | 0 | 3 |
| Shared-function replacement | Install `f1(h)=1` and explicitly route both uses to it | 1 | 1 | 1 |
| Actor-only replacement | Route `A` to `f1`; `B` continues to use `f0` | 1 | 0 | 3 |

Conditioning yields no state because `Z=0`, `A=Z`, and `A=1` are incompatible.
It does not yield a free favorable loss. Token override and actor-only
replacement happen to agree here, but their program identities, runtime and
behavior at other histories can differ. Shared replacement improves the loss
by one; actor-only replacement worsens it by one.

The shared-replacement row **stipulates a propagation map**. It does not prove
that an independent predictor of the old function will switch to the new one.
Nor does it hold `f0` fixed while supposing that its mathematically determined
output changes. It therefore illustrates a program-replacement counterfactual,
not a solved general counterpossible operator.

The author's nearest-agent idea fits the last two rows after the candidate
program family and propagation map are specified: choose `A'` satisfying
`A'(h)=1`, preserve the required history, and charge the search and execution.
“Same history” alone does not decide which external uses or predictions follow
the replacement. A syntactic edit distance is also representation-sensitive:
inlining, wrappers and duplicated source code can change edit counts while
preserving the old behavior. P3-04/05 must choose an invariance target or
declare the representation part of the task.

## 3. Stronger separation: even the full observational law can be identical

Let an exogenous binary variable `U` have any fixed distribution. Consider two
finite acyclic models:

```
M_direct: A = U; B = A; L = 2 + A - 2*B.
M_common: A = U; B = U; L = 2 + A - 2*B.
```

For every `U`, both yield exactly `(A,B,L)=(U,U,2-U)`. They consequently agree
on the entire observational distribution and every expected function of the
observed variables, under the same law for `U`. Nevertheless, in the fixed
context `U=0`, intervening to set `A=1` gives:

```
M_direct: (A,B,L) = (1,1,1)
M_common: (A,B,L) = (1,0,3).
```

Therefore an algorithm given only this common observational information must
return the same output for both models, although the correct intervention
losses differ. A point estimate cannot be exact for both. Indeed, for any
estimate `v`, at least one of `abs(v-1)` and `abs(v-3)` is at least one, since
their sum is at least two. A set-valued answer `{1,3}` or interval `[1,3]`
can preserve the structural ambiguity. Additional structural information or
interventions can resolve it.

This is an elementary identification counterexample, not a claim that arbitrary
values can never encode structure. A value representation may encode a graph
if that information is supplied. The precise negative statement concerns
values computed solely from the indistinguishable observational information.

## 4. Counterpossible arithmetic: what exactly is relaxed?

For the intended usual integers, suppose `sqrt(2)=p/q` with nonzero `q` and
coprime integers `p,q`. Squaring yields `p^2=2q^2`. The parity fact that an even
square has an even base makes `p=2k`; substitution makes `q` even as well,
contradicting coprimality. This short reconstruction identifies some of the
dependencies that cannot all be retained with the added premise.

There are at least three different research objects here:

1. **Unresolved mathematical belief.** A bounded agent does not yet possess
   the proof, and may assign provisional estimates to the statement while
   the intended meanings and underlying truth remain fixed.
2. **Theory or interpretation repair.** Change specified background axioms,
   operations or domains. For example, replacing “ratio of usual integers”
   by “ratio of elements of the ring containing sqrt(2)” changes the predicate
   and can make a related statement true. It must be labeled a different
   interpretation, with an explicit translation back to the original question.
3. **Genuine counterpossible reasoning.** Keep the intended premise as the
   impossible antecedent and specify a nonclassical evaluation/selection rule
   that permits discussing its consequences without arbitrary explosion.

Preference-weighted weakening can be useful in object 2 by making the author
state which aspects matter and which changes are tolerable. It does not turn
object 2 into object 3 merely because its repair has a small cost. For object
3, a formal contract must state which inferences and arithmetic evaluations
survive, what happens when they conflict, and why the selected interpretation
supports the requested consequence.

The even smaller premise `P and not P` exposes the same boundary. A union of
one consistent `P` case and one consistent `not P` case represents uncertainty
between alternatives; it does not make their conjunction true in either case.
An empty classical source gives no action warrant. Adding a nonexplosive
inference rule or impossible state is a genuine extension needing its own
soundness/meaning contract.

## 5. Minimum contract for a future repair or replacement operator

This is a proposed P3-01 requirements list, not a selected carrier or algorithm.

| Required field | Concrete purpose / failure witness |
|---|---|
| Typed target and fixed history | Distinguish belief about `A(h)`, action token, function output and replacement program |
| Hard constraints and permitted relaxations | Expose whether the hypothetical is feasible and which meanings can change |
| Source identity and propagation map | Decide which other uses, predictors and cached evidence follow the change |
| Candidate universe and search budget | Separate a global nearest repair from the best repair found so far |
| Ranking, announced before the outcome comparison | Prevent selecting the desired consequence and then defining “closest” to justify it |
| All minimizers or an announced tie rule | Prevent hiding equally close unfavorable cases |
| Nonempty-selection/existence record | Prevent vacuous favorable bounds when no admissible case exists |
| Consequent and loss evaluator | Make every returned cost reconstructable under the changed interpretation |
| Scope/translation and proof dependencies | Prevent reuse of certificates whose source or mathematical assumptions changed |
| Costs for discovery, translation, search and checking | Prevent a free structural oracle on the proposed method's side |

If the loss ranking intentionally uses desirability, name the result a
preference-guided revision/planning policy. That may be useful, but is not an
independent discovery of which counterfactual would obtain. For explanatory
counterfactuals, varying the declared repair weights and reporting sensitivity
is informative; favorable weights chosen after reading outcomes are not.

For a finite nonempty candidate family with a declared ranking, returning all
minimal candidates is well-defined. If they give different costs, report the
set, interval or an explicitly justified distribution. A scalar minimum loss
over ties answers an optimistic planning question; a maximum answers a robust
one. Neither is an unstated uniquely identified counterfactual truth.

## 6. Relation to the existing value_logic interface and comparison gate

Read `v2/foundations/03_provisional_core.md` §§2–5, and the paper's source and
withdrawal interfaces. Repeated source keys mean the same quantity; a changed
program, population or evaluator changes scope. Nonempty modeled contexts
support loss comparisons. Withdrawn used premises incur explicit proof
penalties under the proved transport conditions. These are useful ingredients
for preserving dependencies and explaining a repair's consequences.

They do not already specify the counterfactual candidate family or discover its
dependency graph. The credible ordinary comparator should receive the same
structure and include structural intervention, ranked/weighted repair,
dependency tracking, probabilistic or interval evaluation, and paid search.

**Improvement target:** an exact restricted result, a better checked
cost/retention tradeoff, or a useful combination with explicit scope under
matched information and resources. **Equivalence result:** the same candidates,
ranking and evaluation can reproduce every answer by the ordinary comparator;
any residual contribution would need to lie in the interface, proof or task.
**Failure witness:** ambiguity hidden by a point answer; an impossible source
used as a warrant; an outcome-selected repair; uncharged structural discovery;
or a purported same-meaning counterpossible solved by changing the terms.

## 7. Finite check, retrieval and resource record

A CPython standard-library development check enumerated all eight triples
`(Z,A,B)` for conditioning, evaluated the other three rows, and checked both
binary `U` values in the observational pair. It passed. The values were:

```json
{
  "status": "finite_development_check_pass",
  "operation_losses": [null, 3, 1, 3],
  "observations_at_U0": [0, 0, 2],
  "observations_at_U1": [1, 1, 1],
  "intervention_losses_at_U0": {"direct": 1, "common": 3}
}
```

The finite arithmetic is independently reconstructable from the displayed
equations. This is neither held-out evaluation nor a general counterfactual
theorem. No experimental population was generated.

First observed reviewer UTC: `2026-10-07 00:42:49 UTC`. The tiny check observed
start `2026-10-07T00:45:02.645914+00:00`, monotonic `27071953053670`, and end
`2026-10-07T00:45:02.645938+00:00`, monotonic `27071953067561` in one runtime.
Its measured inner interval is 13,891 ns, not the reviewer research duration.
Reviewer engaged research time, inference-token cost and monetary cost were
not separately metered and are **unknown**. No reviewer duration is added to
the principal research clock.

Retrieval: four direct primary source openings, targeted in-document location
checks, then two literature searches for the original revision/update chapter.
The search coverage limitation is recorded above. Full theorem proofs beyond
the named inspected sections were not reviewed. No frozen phase-two files,
canonical phase-three documents or ledger entries were edited by this reviewer.
