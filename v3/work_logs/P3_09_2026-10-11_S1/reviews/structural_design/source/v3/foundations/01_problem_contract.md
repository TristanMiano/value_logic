# P3-01 — a contract for uncertainty, usefulness and counterfactuals

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **completed P3-01 contract, attempt P3-01-1; prospective requirements for later work**.
This document specifies questions and evidence. It does not select a permanent
carrier, establish the later learning theorems, or pass a phase-three gate.

Read with the [desiderata matrix](01_desiderata.md),
[separating examples](01_separating_examples.md),
[evidence boundaries](01_evidence_boundaries.md),
[composition boundaries](01_composition_boundaries.md),
[representation boundaries](01_representation_boundaries.md),
[observation contract](01_observation_contract.md),
[machine-readable index](01_contract.v1.json),
[primary-source contracts](../literature/01_source_contracts.md), and
[observed work record](../work_logs/P3_01_2026-10-07_S1.md).

## 1. The question we can investigate

Can a bounded reasoner improve its decisions about unresolved mathematical
questions by learning task-relative costs, deciding which computations to buy,
and reusing justified comparisons when evidence or assumptions change?

This is a precise development of the author's five questions. A numerical
carrier does not answer them in advance. We must supply a language, an
information interface, an update procedure and an interpretation of the costs.
The motivating attitude—retain useful models without treating them as final—is
compatible with definite conditional proofs. A theorem under an explicit theory
does not assert that the theory is the last word on reality.

The most promising phase-three object is an **interface connecting uncertain
forecasts, paid reasoning and checked revision**. We will compare it with an
ordinary combination that has all three abilities. An exact equivalence is an
informative outcome; merely reproducing expected-cost notation is not a new
scientific contribution.

## 2. What phase two actually supplies

| Inherited interface | Reusable scope | Obligation still missing |
|---|---|---|
| Typed signed loss expressions and shared sources | Finite rational piecewise-affine terms; conditional comparisons over admitted source cases | A procedure learning beliefs about arbitrary unresolved mathematical sentences |
| Checked inference and current-request matching | A conclusion warranted by the checked premises, source identities and interpretation | Automatic empirical adequacy of those premises, or trust in an arbitrary checker |
| Source restriction, withdrawal and transport | Reuse when premises survive or a checked correction covers the change | A rule for discovering new assumptions, counterfactual dependencies or their probabilities |
| Expected-cost retention and coherent recovery | The precise reset-procedure/summary families proved in phase two | A general sufficient representation for changing logical beliefs and objectives |
| Bounded proof-procedure assessment | Later procedure choice on a family of already-true requests | Truth prediction for both true and false unresolved claims |
| Report-dependent behavior | The finite `SELF-MIX-v1(r)` program and its explicitly modeled feedback | Unrestricted reflection, self-trust or fixed-point learning guarantees |

Sources: [paper §§2–8](../../paper_v2.md),
[core §§2–4, 8–11](../../v2/foundations/03_provisional_core.md), and
[observation/revision audit §§23–25](../../v2/foundations/03b_observation_and_revision_audit.md).
The report's staged proof-search example is narrower than the full inherited
reflection interface; both boundaries matter.

Two different uses of classical logic also need separation. The loss calculus
rejects an empty deployment source as an action warrant. Its exact Boolean
fragment nevertheless preserves classical entailment, including explosion,
because Boolean premises occur in a query over a nonempty valuation source
([paper §6.1](../../paper_v2.md#61-a-genuine-boolean-fragment)). Neither fact
already supplies a paraconsistent logic or a counterpossible evaluator.

## 3. Language, interpretation and theory

### 3.1 A common reference language, without an omniscient agent

For the first mathematical comparison, use effectively encoded first-order
arithmetic with equality and a declared representation of finite programs,
their inputs, execution traces and rational quantities. Call it `L_math`.
The reference theory `Gamma_tau` has a versioned, computably enumerable axiom
specification and a concrete proof checker. Axiom admission uses a decidable
schema, an enumeration witness checked within budget, or an explicit unresolved
status; bare computable enumerability is not a free membership decision.
`tau` identifies the theory,
interpretation conventions and checker version. Later tasks may choose a
smaller tractable fragment; they must state its translation into this interface.

For a definite reference instance, take the vocabulary `0, S, +, *` with
equality, variables and the usual first-order connectives/quantifiers. Use
first-order Peano arithmetic as `Gamma_ref`: the successor, addition and
multiplication axioms, plus induction for each formula of this vocabulary.
`I_ref` interprets these symbols over the ordinary natural numbers. A fixed
effective proof encoding and the standard syntactic inference rules determine
which strings are proofs; proof discovery enumerates and checks finite strings
in length order. This is a mathematical reference procedure, not an efficient
implementation supplied for free. PA consistency, its intended soundness and
the correctness of an eventual implemented checker are separate conditional
premises. A smaller executable fragment may replace this reference for a
finite arm, with its scope and bridge stated explicitly.

For the LI comparison, include its specified first-order logical axiom
instances in the presented theory and disclosure stream (S01 §2 and
Definition 3.2.4's footnote). Its Boolean prime-sentence convention does not
obtain quantifier instantiation for free. Either give an explicit translation
from the concrete proof calculus or identify `Gamma` with the enumerated
deductive theory; do not equate a bare list of nonlogical axioms with all
of its derived Boolean constraints without that bridge.

One concrete query family is

```
phi_(p,x,b,v): running program p on input x for at most b specified VM
              steps terminates with output v.
```

Each such bounded claim has a definite truth value in the stipulated operational
interpretation and can be decided by finite execution. The budget `b` appearing
inside the proposition is distinct from the reasoner's available budget `B_t`.
A timeout before deciding that horizon says nothing by itself about whether
the bounded execution condition is true. Completing the full horizon without
the specified terminating output refutes that bounded claim. Unbounded halting, arbitrary
arithmetic and independent sentences remain expressible comparison questions;
the finite implementation does not thereby decide them.

Denote truth in a fixed interpretation by `y_I(phi)` when that interpretation
assigns a truth value. Denote existence of a proof in a theory by
`Gamma_tau |- phi`. Denote a particular procedure's successful receipt of a
checked proof within a budget by `received(A, phi, B, tau)`. These are three
different predicates. A false claim can have no received proof, and a true
claim can have no received proof. Consistency, soundness for the intended
interpretation and a concrete checker's correctness are explicit premises when
an argument needs them; no implementation receives their decision oracles.

### 3.2 Versions and conditional theories

If an axiom is withdrawn, a program changes, or a symbol receives a new meaning,
create a new scope/version. Keep the old proof and its dependency record, but
do not silently treat it as a proof in the new scope. A formal assumption
`Gamma_A |- phi` may coexist with `Gamma_B |- not phi` as two tagged conditional
claims. Their coexistence does not authorize taking the untagged union of the
theories. An empirical application of either theory needs a separate bridge.

For any imported Logical Induction property, a fixed consistent theory and its
specified deductive process remain the comparison contract. A stream with
withdrawals is a different extension. Conditioning on an additional consistent
axiom and replacing the current theory are also different operations; see
S01's precise locators in the source record.

Retaining Newtonian and relativistic models at different application scopes
does not mean that a fixed arithmetic sentence has a partially true proof.
Truth in an interpretation, conditional derivability, predictive adequacy and
usefulness are separate coordinates of the problem. A continuous usefulness
scale provides no logical-uncertainty update rule by itself. Ordinary methods
can also keep several scoped, fallible models; Q3 asks what the proposed
interface adds under matched information and resources.

### 3.3 What “all statements” could mean

Distinguish four increasingly strong services:

1. Effectively enumerate well-formed sentences.
2. Return a default or computed forecast on any requested sentence.
3. Improve forecasts on a specified family under a specified feedback process.
4. Satisfy an unrestricted asymptotic criterion over the language.

The first two do not establish the last two. At any finite stage, explicitly
stored forecasts, certificates and active queries are finite. An implementation
may use a default outside them, but must expose that status. It must not label
unqueried statements “learned” because a total lookup function returns a number.

## 4. Five kinds of uncertainty, plus one decision distinction

| Object | What remains unknown? | Evidence that can change it | Inference that is not licensed |
|---|---|---|---|
| Mathematical truth | The value of `y_I(phi)` for a fixed interpretation | A checked proof/refutation, paid execution, or an explicitly fallible predictor | “No proof returned” means false |
| Proof production | Whether procedure `A` will return an accepted proof within `B` | Actual runs or a justified model of the versioned procedure | High success frequency proves this particular claim |
| Model adequacy | Whether a model's predictions or error bounds apply to the current use | Observations, validated error bounds, model criticism and scope evidence | A feasible mathematical source describes deployment |
| Axiom/interpretation choice | Which conditional framework to rely on, or what a hypothetical preserves | Named assumptions, translations and task-relative comparisons | Rejecting one assumption retracts ordinary metatheoretic validity of all earlier proofs |
| Usefulness estimate | Expected or bounded task loss for an action under present information | Newly resolved questions, a changed loss function, better dependence data or resource prices | A favorable utility estimate is a probability without an identification contract |
| Action availability | Whether a useful action or computation can actually be selected | The observation and resource interface | A pointwise minimum over hidden cases is an executable policy |

The last row is a decision constraint, not another kind of uncertainty. A
shared notation may be convenient, but it must retain these types and their
provenance. The intended-value criterion and a measured proxy can also differ;
the inherited discrepancy bridge remains an explicit additional assumption.

Also label what any probability describes: a reasoner's epistemic forecast
about a fixed mathematical answer, random task selection or randomized
computation, or a measured frequency on a specified cohort. Randomizing which
program is asked about does not make the answer to one fixed deterministic
program question physically random. Conversely, a reliability statistic for a
fallible proof-search predictor is not automatically a posterior probability
that a particular sentence is true. An accepted sound proof has a different
evidence contract from such a predictor's favorable report.

## 5. Information state and update timing

### 5.1 Visible state

A finite state has the interface

```
S_t = (scope IDs, query history, paid observations, checked proof records,
       active constraints, forecast state, model/repair catalogue,
       dependency records, pending feedback, resource account).
```

This specifies what must be identifiable, not how it must be stored. A scalar,
profile, constraint set, program or compressed representation may implement
some of these services. Retained identifiers do not give free access to a
discarded object: dereferencing, decoding and recomputation must be possible
and charged when relevant.

Let `D_t` be the finite set of admitted, version-matched proof conclusions so
far in a fixed-theory episode. It grows when new checked evidence arrives.
It is **not** all logical consequences of those sentences, and the agent does
not receive `models(Gamma_tau)` or a consistency oracle. Derived constraints
must come from computations permitted within the budget. A version-changing
episode starts a newly scoped active set; its historical record remains intact.

The agent may also have fallible learned constraints. Store these separately
from checked premises. A learned interval becomes a statistical guarantee only
under a stated coverage statement and its selection conditions. A forecast
does not become a formal certificate because it is confident or repeatedly used.

A conflict status likewise needs evidence: finding a certified inconsistent
finite subset differs from failing to find a satisfying assignment in budget.
Keeping histories from two different theory versions does not authorize
combining their hard premises. A probability state on an empty admitted source
cannot be normalized; report the conflict and apply a declared revision or
fallback policy rather than treating emptiness as a favorable loss bound.

### 5.2 Round order

For a query issued at round `t`:

1. Admit only feedback already scheduled to arrive. Reveal the query, action
   catalogue, loss interpretation, known stakes, hard requirements and current
   resource prices. Save the information-state version and, for anticipatory
   prediction, a forecast before optional question-resolving computation.
   Forecasting itself is charged; a fast exact solver is an admissible
   computation route, not evidence of learning without computing the answer.
2. Permit an adaptive sequence of paid computations. Each response is one of
   a checked answer/certificate, a declared observation, no result within budget,
   or an execution/checking failure. Update the state after receipt and charge
   the work. A computation that is still running supplies no future answer.
3. Save the post-computation decision report, its status/assumptions, chosen
   action and any justification **before** new outcome/evaluator feedback.
   Record the first accepted resolution time. A report made after paid
   resolution can establish a priced decision result but cannot be counted
   as a forecast anticipating that resolution.
4. Apply the declared feedback schedule. Some answers may arrive later; some
   may never arrive. Match every answer to the original query, interpretation
   and forecast timestamp. Scores use the forecast made before that answer.

An action may be `act`, `abstain/use an available fallback`, or `buy another
computation`. Exact costs, allowed actions and fallback loss are part of the
task, not hidden favors to one method. Output identifiers, serialization order,
proof filenames and task generators must be checked for cheap label shortcuts.
Ordinary competitors may exploit any legitimately visible shortcut too.

Round number is an ordering index, not a claim about constant physical runtime.
Every admitted result has a request identifier, scope, issue/receipt times and
an actual resource charge. A budgeted computation may finish within a round or
remain pending across rounds under the declared scheduler. New exogenous
feedback enters only at its announced boundary. A theorem stated in number of
rounds does not become a wall-clock or VM-step guarantee without a cost bridge.

### 5.3 Feedback regimes must remain separate

| Regime | Label access | Appropriate comparison |
|---|---|---|
| Immediate full feedback | Every expert's realized loss is computable after the round | A finite full-information prediction mixture |
| Exogenous delayed feedback | Answers arrive under an announced schedule independent of the selected prediction, under the imported theorem's conditions | A delayed-feedback wrapper, charging all active copies |
| Selected-action feedback | Only the chosen action's outcome is revealed | A method with the same partial-feedback information; no full-information bound imported |
| Paid/selected proof discovery | The reasoning policy affects which labels are obtained and when | Metareasoning/active acquisition under a declared observation model |
| Unresolved forever within the horizon | No usable answer arrives | Pending coverage and conditional/structural diagnostics, not an invented label |

The final challenge must record label coverage and the selection mechanism.
Accuracy on the resolved subset can be informative, but does not estimate
accuracy on unresolved claims without additional assumptions. A hidden evaluator
can compute labels for later assessment; its answers are not agent features.

## 6. Values, costs and resources

### 6.1 A loss query needs an interpretation

For an action `a`, a task `q` specifies a realized loss `ell_q(a, omega)` in a
declared unit, where `omega` contains the relevant outcome/dependence information.
This is the semantic payoff, distinct from the agent's estimate
`Lhat_t(q,a)` and from the observed realized loss. Where an ordinary probability
model `p_t` is supplied, one possible estimate is

```math
\widehat L_t(q,a)=\sum_{\omega}p_t(\omega)\ell_q(a,\omega).
```

This is a comparison bridge, not a mandatory primary carrier. A source set may
instead determine lower/upper costs; a learned direct forecast can be evaluated
without being called a coherent expectation. Its scope and failure modes must
remain visible. Bounded `[0,1]` forecasts, signed task costs and unbounded cost
families are different domains; a bounded learning theorem cannot silently
cover the last one. Name the consuming decision criterion and timing as well:
an expected-loss decision, a worst-case expected-loss commitment and a fresh
conditional choice are different services. Separate branchwise bounds may
discard a global relation even when every bound is individually correct;
[CB05](01_composition_boundaries.md#cb05-a-tree-recursion-can-discard-shared-constraints)
exhibits the resulting decision change and its ordinary affine reconstruction.

The exact finite sum above uses the supplied coherent law. LI's `E_n` instead
averages threshold-sentence prices and has selected asymptotic properties;
its notation alone supplies none of these exact finite identities (S01
Definition 4.8.2). A deliberately constructed quote `v=1-p` is also not
automatically the market's separate quote for `not phi` at that date.

If `c_true` and `c_false` are known and unequal, a binary expected loss obeys

```math
\widehat L=c_{\mathrm{false}}+
(c_{\mathrm{true}}-c_{\mathrm{false}})p.
```

Probability recovery then has a specific algebraic question. Unknown stakes,
unknown additive charges, an interval rather than an expectation, or a purely
ordinal preference need not identify `p`. P3-02 owns the general finite
characterization; the examples here identify the tests it must pass.

### 6.2 Two accounts, without a hidden exchange rate

Track a hard resource vector `r_t`—for example VM steps, checker operations,
memory bytes and observations—and a declared budget `B_t`. If a task values
these resources in loss units, it also provides prices `lambda_t`. Report
task loss and resource use separately, then the specified total

```math
J_t=\ell_{q_t}(a_t,\omega_t)+\lambda_t\mathbin{\cdot}r_t.
```

Charge forecasting, feature extraction, proof/evaluation, acquisition,
representation construction, model selection, storage/access, checking and
dependency/repair search where they distinguish the methods. Report setup
costs and any amortization horizon. Shared costs can be identical for both
methods, but must be identified before interpreting an advantage. Resource
prices do not create access to an infeasible action or buy violations of hard
constraints unless the task explicitly makes those constraints revisable.

The value of additional computation is itself an estimate. Supplying its
conditional outcome law for free is an idealized diagnostic, not a learned
implementation. P3-07 must specify how that law or useful bounds are acquired.

### 6.3 Resource and information closure

A later comparison is not specified by saying only “same budget.” It must fix
the machine primitives, input-access granularity, variable-size arithmetic and
numeric precision; the exact readable input/metadata; and a registry of
libraries, advice, learned parameters and caches with acquisition/exposure,
reset and reuse rules. Report encoded bits/bytes and decoder costs where a
claim concerns storage. One exact number can contain many labels, so coordinate
count alone does not establish compression in those units.

Both methods may use legitimate visible program shortcuts and ordinary lazy
caches. Common supplied structure, learned structure and oracle structure
remain distinct even when their object-construction costs are equal. A causal
graph or repair catalogue does not become empirically identified merely because
its allocation was charged. Also retain the full query cohort, acquisition
policy and pending/censored labels, so selection cannot masquerade as accuracy.
The [resource review](../work_logs/P3_01_2026-10-07_S1/reviews/resource_information_stress.md)
provides concrete field groups and finite failure witnesses. These are required
specification fields for P3-08/09, not numerical choices frozen in P3-01.

### 6.4 Predictive quality and decision quality

Use a proper prediction score only in its declared outcome setting. Separately
measure realized task loss, resource expense, the chosen comparator's regret,
decision coverage and certificate validity. Equal unweighted accuracy can have
very different consequences when stakes differ. Conversely, better numerical
forecasts may not change any action in the tested decision problem.
Even vanishing probability error need not yield vanishing decision regret
under growing stakes: [criterion probes §5](01_criterion_probes.md#5-vanishing-probability-error-needs-a-stakes-bridge)
give an explicit sequence. A transfer claim needs cost-unit error control,
an appropriate rate or a bounded-stakes assumption, not convergence alone.

Decision calibration is itself an established comparison (S19). Its consumer
information, loss class, population and weighting matter: a report can be
calibrated for report-only consumers while ignoring an informative visible
feature, and unweighted calibration need not survive context-dependent stakes.
The [composition diagnostics](01_composition_boundaries.md) make those limits
explicit. A checked inequality between estimates additionally needs a bridge
to actual target loss. Any statistical error bounds used for that bridge must
apply jointly to the compared actions, including their selection procedure.

If reports influence the outcomes being predicted, version the induced process
and state the response semantics. The inherited `SELF-MIX` Brier example already
shows why fixed-distribution propriety alone does not warrant a self-report.
An uncertain forecast, a checked bound and a strategically chosen report must
not be evaluated as if they were interchangeable.

## 7. A typed counterfactual request

Write a request as

```
CF = (base scope and history, antecedent, operation kind,
      retained interpretation/constraints, admissible changes,
      propagation map, candidate/search budget, ranking and tie rule,
      loss query, consumer decision service, evidence dependencies).
```

For an action/policy recommendation, the consumer decision service names its
criterion, information available at choice, and whether an earlier commitment
is enforced or conditional reoptimization is permitted. A pure value query
can mark this field inapplicable. Timestamps alone do not fix that service.

The request must identify which of the following operations it means:

| Kind | What changes? | What must be supplied? |
|---|---|---|
| Evidence conditioning | Information about the same process | A positive-probability event for the ordinary ratio rule; a nonempty retained set for set restriction; otherwise an explicit alternative rule. S09's conditional-price rule has a nonempty-event requirement and does not supply empty-contradiction semantics. |
| Token intervention | One designated variable/equation occurrence | The structural equations and propagation semantics |
| Shared-function replacement | A versioned function and specified uses | Which calls/copies/predictors track the replacement, and which remain tied to the original |
| Actor-only replacement | Only the acting program/call is redirected | A propagation mask retaining other uses of the original program |
| Theory/model repair | Declared assumptions or model components | Hard constraints, allowed edits, ranking, all minimizing alternatives or an announced tie policy |
| Genuine counterpossible | An antecedent inconsistent with retained mathematical/semantic background and interpretation, beyond a mere change of actual-state facts | An explicit nonclassical evaluation/selection semantics, or a precise explanation of infeasibility and the missing structure |

“Choose the nearest agent with the same history that returns the other action”
is a useful program-replacement target. History alone does not define nearness,
identify the candidate class, or make a predictor of the original program follow
its replacement. Charge the search and construction of the dependency model.
Syntactic edit distance needs a refactoring test; equal input/output behavior
need not preserve internal intervention points or runtime.

If several equally ranked admissible repairs give different costs, return their
set/range, use a prospectively declared tie rule, or report unresolved selection.
Distinguish certified infeasibility from no repair found within budget, and
a certified optimum from a best-found candidate. A declared tie policy yields
a policy-selected answer, not necessarily a uniquely identified consequence.
Even a certified global optimum can coexist with uninspected equally optimal
candidates: **optimality and coverage of all minimizing consequences need
separate evidence**. A zero-ranked candidate under a nonnegative ranking is
already optimal; that alone does not exclude another zero-ranked candidate
with a different loss.
If no admissible case exists and this is established, return an infeasibility status. Do not turn a
universal statement over zero cases into a claim that an action is useful.
A ranking may openly favor desired outcomes as a planning preference; that
does not also make it independent evidence about counterfactual dependence.

A response therefore has separate fields for search status, selection meaning,
selection coverage, numerical form and numerical meaning, with evidence and
resource records. For example, a point may be an exact consequence, an exact
policy-selected value, a candidate value, or a fallible forecast. An exact
interval hull differs from an outer bound; an unbounded nonempty cost family
differs from undefined semantics. A confidence number does not specify these
meanings without an explicit encoding/decoding contract. See the
[finite response stress test](../work_logs/P3_01_2026-10-07_S1/reviews/counterfactual_status_stress.md)
for an entirely specified successful request and incompatible cases.

A nonsingleton outer bound does not itself prove that distinct admissible
consequences exist: the bound may simply be loose. Every nonvacuous value or
uniqueness claim identifies its target family and establishes nonemptiness.
Complete coverage of an empty family supports infeasibility, not usefulness.

A uniquely justified action can require less information than a uniquely
identified counterfactual cost. Suppose two admitted cases have paired action
costs `(1,2)` and `(3,4)`. The first action is cheaper by one in both cases,
although neither action's individual cost is unique. Comparing the separate
ranges `[1,3]` and `[2,4]` discards the paired relation and fails to establish
that dominance. A certificate for the joint difference retains it. This is
the inherited shared-source comparison applied to a stipulated counterfactual
family, not a new identification theorem. Its family must still be defined,
nonempty and covered by the certificate; missing counterpossible semantics
cannot be replaced by the favorable numerical table.

The sqrt(2)-rational question fixes the relevant interpretation explicitly.
Changing what “integer” or “rational” denotes can define a related consistent
problem, but the translation must be reported. It does not answer the original
counterpossible merely by using similar words. P3-04/05 own the candidate
semantics and transport results; the examples here make the distinction testable.

Keep the quoted antecedent and its ordinary interpretation fixed at the
original scope; separately identify every exceptional hypothetical evaluation
or consequence rule. The [GC01 diagnostic](../work_logs/P3_01_2026-10-07_S1/reviews/genuine_counterpossible_target.md)
defines a finite example with such an exception. It is a specified diagnostic,
not a defended counterpossible semantics. Its relevance/frame input is
stipulated in development; document order is not prospective freezing. P3-04
must defend the selected rule or retain an unestablished disposition. Later
confirmatory comparisons freeze their selection procedure before evaluation
exposure. Presentation invariance concerns declared meaning-preserving maps;
it does not require that every classically equivalent impossible antecedent
have identical hypothetical consequences (S07 §3.1).

## 8. Strong ordinary comparisons

**O-COMB** is the principal comparison family: classical proof/program checking,
probability or interval forecasts, task-cost decisions, paid reasoning, multiple
scoped models, and dependency-aware certificate reuse. It starts with the same
information and has access to observations, computations, visible features,
actions and repairs on the same terms and budget. In a paid-acquisition policy
comparison, each method pays for its own purchases and may consequently reach
a different history. A common-history replay is a separately labeled diagnostic,
with historical information costs either common to both or excluded from both.
It may use the same successful algorithm as the candidate. Equality of outputs
is allowed; it narrows the contribution to an interface, proof, implementation
or application that must still have a supported delta.

This names a credible comparator family, not a requirement to outperform every
classical program or a selector given hidden evaluation answers. Concrete
baselines and permitted selection are specified in development and frozen later.
A best-fixed-method regret comparator, an executable portfolio and a
best-per-instance oracle are distinct. Ordinary reuse can charge one acquisition
once, plus its actual retention, lookup and checking; no fictitious repeated
full acquisition is required. See [CB01/CB04](01_composition_boundaries.md).

| Component | Concrete comparison contract |
|---|---|
| O-PROOF | Budgeted proof/evaluation with valid timeout, refutation and fallback statuses; includes cheap visible shortcuts |
| O-FINITE | A declared finite set of prime claims and only the Boolean constraints actually checked; finite assignments/projections are constructed within the charged budget |
| O-PROB | A finite joint probability/credal representation on the same accessible information; evaluates the same task losses and decision rule |
| O-ONLINE | A prespecified finite predictor mixture with bounded scoring losses; the chosen feedback theorem is imported only when its hypotheses hold |
| O-META | A finite metalevel model choosing computations and stopping, with learned or stipulated outcome/performance profile labeled explicitly; S03/S20 supply ordinary interfaces |
| O-CHANGE | Ordinary structural intervention or weighted/ranked repair with the same dependency graph, admissible changes and tie contract |
| O-REUSE | Standard dependency records, caches and checks of changed premises; S17 supplies an established incremental-checking comparator |
| Diagnostics | Charged exact computation and a separately labeled free oracle; neither is confused with a matched deployable baseline |

O-FINITE avoids a common hidden oracle. For `k` chosen prime claims, enumerate
at most `2^k` bit assignments and retain those satisfying the observed Boolean
constraints. This may be expensive, so charge it. It does not require that those
assignments extend to full models of `Gamma_tau`. Treat them as information
states still compatible with the checked fragment, not metaphysically possible
mathematical worlds. Under sound checked constraints the actual finite truth
assignment remains among them. Global consistency and completeness are separate.

Including every prime atom used by `D_t` and the query permits an exact finite
restriction of the Boolean assessment worlds `PC(D_t)`. Keeping fewer
constraints generally gives an outer approximation. Dropping mixed clauses is
not exact variable elimination; a projection claim must identify its source
set and certify the required computation. A finite list of found assignments
is generally an inner sample, not an outer bound on all admissible losses.
The [boundary arguments](01_evidence_boundaries.md) give explicit separators.

The source record also includes awareness semantics, predictive model combination
when no candidate is exact, Logical Induction, scoring, metareasoning and
counterpossible semantics. Their role is to prevent a weak comparison to bare
Boolean syntax. We do not assert that every framework solves every row.
Full semantic conditioning on visible code and the information a bounded
procedure has actually computed are different contracts; see
[representation boundaries §2](01_representation_boundaries.md#2-reading-a-program-is-not-the-same-as-cheaply-knowing-its-answer).
Component guarantees also need a composition check: projecting or replacing an
online predictor's output to satisfy constraints can change its scoring/regret
guarantee. A coherent expert mixture, a separately proved projection rule and
an unanalysed modified predictor must not be assigned the same theorem by name.

## 9. Operational answers to the five questions

| Question | Required target | Strong comparator | Improvement evidence | Equivalence or failure evidence |
|---|---|---|---|---|
| Q1: logical uncertainty | A bounded information/update process over true, false and unresolved claims; identify which estimates and bounds improve | O-PROOF + O-FINITE + O-ONLINE; LI as a theorem-level comparison | A proved restricted refinement/decision result or a matched finite advantage before paid resolution | Explicit translation with identical decisions/costs; or a counterexample to the claimed update/guarantee. Timeout is not falsity. |
| Q2: logical counterfactuals | A specified intervention/replacement/repair service and an honest genuine-counterpossible analysis | O-CHANGE + dependency tracking; selected impossible-world semantics for the last case | Nonvacuous answers/transport under declared structural information, with a useful construction or guarantee | Ordinary solver reconstructs the result; observational twins or tied repairs refute a claimed unique answer from insufficient inputs |
| Q3: useful fallible models | Retain and select scoped models under task loss and compute limits, including decisions about unresolved logical queries | O-COMB, including ordinary conditional model use and predictive combination | A logical-query prediction/decision gain survives equal initial access, model library, resource terms and objective; each policy may buy different evidence. Scientific approximation alone does not establish this | An ordinary construction reproduces the service; any apparent gain disappears once the ordinary method receives the missing scope/data |
| Q4: refinement in value/cost space | A declared set of LI-inspired duties, feedback timing and priced reasoning choices | O-ONLINE + O-META; LI expectation machinery for theoretical coverage | A particular duty has a proof or valid finite result and yields a documented consequence for decisions/resources | An exact expectation recoding supplies the same service; unresolved labels, changing outcomes or an adverse sequence invalidate a stronger claim |
| Q5: probability information in values | Identify the loss queries, known stakes, source restrictions and recovery objective | Finite linear expectation algebra, coherent expectations and proper scoring | A scoped characterization or useful retention/repair result beyond an already known identity | A decoder/translation proves equivalence; two admissible laws/stakes with the same retained values and different requested outputs prove insufficiency |

“Failure” here refers to the particular claim and its assumptions. An
implementation's negative outcome is not automatically a refutation of the
research direction. Nor is a finite positive result an unrestricted theorem.
The [duty matrix](01_desiderata.md) records the exact statuses that later work
must change, rather than awarding all desirable properties at once.

“Refinement” also names its quantifier. Pathwise narrowing of certified ranges,
improvement in expected prediction loss, a lower realized score and a better
paid decision are different services. The [criterion probes §4](01_criterion_probes.md#4-refinement-has-several-non-equivalent-meanings)
give a finite conditioning example in which uncertainty increases on one
branch while expected squared loss decreases. Surprising observations need
not be evidence of a defective update.

## 10. Candidate representations and the contribution target

The candidate shortlist remains open:

| Candidate | Natural service | Main question to test |
|---|---|---|
| A direct cost forecast per query | Compact decision-relevant prediction | What does it retain for a new query, changed stakes or a joint operation? |
| A coherent probability/expectation state | Multiple known loss queries | What coherence and logical relations can be maintained within the budget? |
| A set of possible forecasts/source constraints | Conditional robust bounds and explicit ambiguity | What construction, checking and refinement costs are required? |
| A source-preserving loss profile or continuation object | Composition and later query reuse | Does its additional information earn its storage/acquisition cost? |

A hybrid is permitted if the boundaries remain explicit. Exact probability
recovery, a useful decision and a reusable certificate can require different
information; phase two already motivates that distinction. P3-02 determines
a usable restricted representation. This contract does not freeze one because
it uses real numbers or because it resembles the previous implementation.

Native exact checking retains its grammar boundary: a known rational stake
can be a request-specific coefficient, whereas a product of jointly uncertain
stakes and probabilities generally needs a declared extension or justified
enclosure. A new source coordinate does not prove the nonlinear relation it
is intended to encode. The [carrier argument](01_representation_boundaries.md#1-known-coefficients-and-uncertain-quantities-are-different-inputs)
states that inherited limitation and the available routes without choosing one.

**P3-N01 contribution hypothesis.** A modest formal adaptation or useful
synthesis/application may connect delayed logical evidence, changing task
losses, paid computation and transported warrants in a way whose assumptions
and information requirements can be stated more sharply than by merely listing
the components. Potential evidence includes a restricted preservation or
information obstruction theorem, a constructive interface with a meaningful
cross-component guarantee, and a matched application showing its consequence.
Magnitude and comparison scope must follow the actual result.

The broad LI/controller connection is already proposed in S01 §7.4, which
labels it speculative. Learned performance profiles and incremental certificate
checking also have established ordinary treatments (S20/S17). A contribution
therefore needs a particular supported service or cross-component result;
listing those components or adding cost terminology is insufficient.

Current status is **NOT YET SUPPORTED**. None of the elementary examples,
literature reconstructions or time spent here establishes priority or
performance superiority. P3-01 can complete at contract scope without a
contribution pass; P3-02 is the next scheduled evidence chunk, and P3-C retains
the named recurrence rule if meaningful support is still missing then.
