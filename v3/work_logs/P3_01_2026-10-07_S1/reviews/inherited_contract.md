# P3-01 inherited-interface reconstruction

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Review date: 2026-10-07 UTC. This is a **nonblind internal reconstruction**,
not independent external validation. Resource time is unmeasured; this review
does not add research minutes to the parent clock. Scope: source reconstruction
and proposed P3-01 contract checks only. No phase-two file was edited, and no
P3-02 or later research task is being declared complete.

## 1. Most consequential findings

The phase-two system already provides a conditional language for loss comparisons,
shared uncertainty, provisional evidence and proof reuse. It does **not** yet
provide a general logical-uncertainty learner. In particular, its executable
proof-search application samples the behavior of bounded procedures on requests
that are all already theorems. Its uncertainty is about producing a received
proof within a procedure's limits, rather than about arbitrary mathematical truth.

There is also more inherited reflection than a staging-only description suggests.
The foundations model a report that changes its own program's behavior, and
an evidence-responsive finite controller. These are genuine behavioral feedback
examples, but they do not establish unrestricted proof reflection, calibrated
beliefs about arithmetic, or a cyclic logical self-trust theorem.

The central favorable interpretation of fallible model coexistence is operational:
the system can retain several scoped, useful models and reason about reliance
under a named loss and resource criterion. Classical conditional reasoning,
combined with ordinary uncertainty and decision machinery, can do this too.
P3-01 should compare with that complete combination.

## 2. Inheritance matrix

| Question or capability | What phase two actually supplies | What is absent or remains a new obligation | Source pointers |
|---|---|---|---|
| Uncertain quantities and model cases | Finite signed CPWA loss functions over shared finite-real source coordinates; a nonempty finite union of rational polyhedra can retain joint constraints and alternative interpretations. | No privileged probabilities over cases; no automatic empirical coverage; no procedure for generating all logical models of an arbitrary theory. | `paper_v2.md` §§2–3; `v2/foundations/03_provisional_core.md` §§3–4. |
| Classical mathematical consequence | An exact finite Boolean fragment, and conditional finite-fragment soundness under current-request checking. | No arbitrary arithmetic truth evaluator, search completeness, or feasible enumeration of all consequences. | `paper_v2.md` §§5–6.1; `v2/derivations/03f_soundness_acceptance.md` §§1–2. |
| Unresolved proof search | Actual versioned short procedures, a complete fallback for one supplied source schema, observed failure traces and a policy that changes later procedure selection. | The requests are all true under the source; failure is not falsity. A hard logical-uncertainty task needs both true and false claims and a genuinely unresolved outcome policy. | `paper_v2.md` §8.2; `v2/derivations/06_case_studies.md` §§4–4.3. |
| Model adequacy | Shared discrepancy, modeled error and resource prices can justify one approximation over another without proving absolute accuracy. | No inference from low task loss to final truth of a scientific model; no demonstrated Newton/GR application or special mathematical-belief advantage. | `paper_v2.md` §8.1; `v2/derivations/06_case_studies.md` §§2.2, 2.5, 2.9. |
| Axiom or evaluator uncertainty | Alternative source interpretations, discrepancy premises and conditional metatheory; checker or source validity may remain uncertain to the agent. | No operational distribution or revision rule over arbitrary axiom systems; no general consistency oracle or solution to theory selection. | `v2/decisions/DIR01_loss_grounded_reflective_direction.md` §§2, 4–5; core §§8–9. |
| Learning usefulness | Conditional evidence updates can change report choice, loss bounds and the next procedure. Common source coverage can transfer a checked bound to selected use. | No supplied statistical estimator, generic calibration process, asymptotic online-learning guarantee, or automatic marginal-to-conditional coverage. | Core §§9, 11.3; `03b_observation_and_revision_audit.md` §§23, 25.3; case studies §§4.1, 4.5–4.6. |
| Probability information in costs | Declared expectations use ordinary probability laws; reset-cost profiles preserve particular linear information and can lose information needed after revision. | A cost number alone has no fixed probability meaning. Known payoff, normalization, correlations, report meaning and observation semantics are additional requirements. | `paper_v2.md` §§6.2, 7; `v2/experiments/retention_design.md` §§1, 3–4. |
| Counterfactual or counterpossible reasoning | Program identity, interpretation transport, evidence withdrawal and source revision are explicit. | No selected counterfactual operator; no automatic distinction between token intervention and shared-function replacement; no genuine counterpossible semantics merely from rejecting an empty deployment context. | Core §§8, 11.4; `paper_v2.md` §§3.1, 4.2, 6.1. |
| Reflection and feedback | `SELF-MIX-v1(r)` emits its own report and uses it to choose a branch; a finite controller changes the report after visible evidence. Report validity is separately checked. | No implication from self-emission to correctness; no full theory of cyclic reasoning or general self-calibration. | Core §§9.1, 11; `03b_observation_and_revision_audit.md` §§23–24. |

## 3. Three boundaries to make explicit in the new problem contract

### 3.1 Conditional truth, belief, and proof production have different objects

A useful proposed contract can identify a formal language, a theory, a checker,
an intended interpretation where one is used, and the finite record that the
agent has actually obtained. These are different components. A deterministic
sentence can have a fixed interpretation while its truth remains unknown to a
bounded agent. Uncertainty about whether a particular procedure will return a
proof is another prediction, even when the sentence is a theorem.

Do not identify a time-limited search's failure with a refutation. Do not require
every unresolved sentence to converge to a Boolean answer unless the chosen
deduction/evaluation process can resolve the declared class. If a theory does not
decide a sentence, an eventual Boolean label needs a separate semantic or
evaluation assumption. A finite benchmark can arrange such labels, while keeping
them outside the agent's observations until the scheduled reveal.

The supplied polyhedral feasibility witnesses in phase two establish a much
narrower property than the consistency of a complete arithmetic world. Extending
the source to “all models consistent with what is known” must identify who
constructs the models and performs consistency checks, and at what cost. A
finite set of provisional Boolean assignments that has not passed all logical
constraints can be a bounded forecast representation; it should not be called
the set of models of the full theory.

### 3.2 Nonvacuous deployment is not a nonclassical truth theory

Core §4 rejects an empty deployment context because it cannot warrant an action.
However, the Boolean embedding in paper §6.1 deliberately keeps all Boolean
valuations in the source and places premises in the query. Inconsistent premises
then still entail every Boolean conclusion in the classical fragment. Therefore
neither paraconsistency nor a semantics of counterpossibles has already been
obtained. A hypothetical inconsistent with explicitly retained assumptions
needs a new declared treatment; renaming a repaired consistent interpretation
does not settle the original fixed-interpretation counterpossible.

### 3.3 Changing a report can change the distribution being predicted

The inherited program has

\[
H_r=(1-r)p+rs.
\]

Here `r` is both a report and a behavioral parameter. In the existing example
`p=1,s=1/2`, minimizing the report-induced Brier objective gives `r=5/8`, whose
actual failure probability is `11/16`. The self-consistent report is `2/3`.
Their Brier losses are `7/32` and `2/9`, respectively, so the inconsistent report
has the smaller objective by `1/288`. This is a fixed finite calculation already
in `03b_observation_and_revision_audit.md` §24. It does not contradict proper
scoring against an exogenous fixed outcome distribution.

P3-01 should distinguish ordinary logical forecasts, reports about a controller
whose action depends on that report, and claims about a future predictor. Their
information and timing contracts differ. Reusing the same score name does not
make their learning guarantees interchangeable.

## 4. A strong combined ordinary comparator

The comparator should have the same public syntax, query stream, proof checker,
versioned programs, accessible features, budget, observation schedule, action
set and source evidence as the proposed value-logic method. It may combine:

1. Ordinary proof and program checking, including cheap input inspection that
   bypasses an unnecessary prediction problem.
2. Probability or interval forecasts learned from the same available feedback,
   with an explicitly selected finite online learner where appropriate.
3. Expected-cost or robust-cost action choice under the same known losses and
   constraints, including abstention, fallback and paid computation.
4. Joint dependence information rather than artificially independent marginals,
   whenever the candidate receives or retains that information.
5. Dependency records, cached certificates and ordinary recomputation or
   transport checks after an evidence, model, program or objective revision.

This is a comparator specification, not a claim that one implementation already
achieves every item at zero cost. Charge feature extraction, calibration,
proving, checking, consistency tests, counterfactual dependency search, retention,
updates and selection where each is consequential. State whether feedback is
full-information, selected-action only, or delayed; do not give one method
counterfactual losses that the other cannot observe.

An exact translation that preserves decisions and overhead up to a declared
bound is positive equivalence evidence. An improvement in a weak baseline's
accuracy is insufficient if the strong comparator makes the same decisions or
if acquisition costs reverse the result. A useful synthesis may still improve
traceability, current-request correctness or justified reuse, but that must be
tested against an ordinary implementation that is allowed to retain provenance.

The phase-two proof-search example is a concrete warning: visible source bits
already expose which short proof works. The ordinary source-aware solver emits
five or six expected nodes, while the learned cascade selects a policy with
cost `35/4` or fallback `9`. Making the trace table larger would not remove the
shortcut. See case studies §4.2 and paper §8.2.

## 5. Small separating cases suitable for P3-01

These are proposed contract witnesses, not a completed P3-02 characterization or
new empirical evidence.

### E1. Cheap fallible model versus costly exact model

Take a declared target `f(x)=x+x^3` on `|x|<=epsilon`. A cheap approximation
returns `x`; an expensive model returns `f(x)` and incurs additional cost `c`.
Under absolute error plus resource charge, the cheap model's excess cost is
`|x|^3-c`, bounded by `epsilon^3-c`. Thus it is conditionally preferable when
`epsilon^3<=c`, although it is not an exact equation for the target on the whole
domain. Enlarging the domain or lowering the exact model's price can reverse
the decision. Ordinary conditional algebra yields the same conclusion.

This separates usefulness from literal exactness and tests whether a method
properly transports the domain and price conditions. It supplies no automatic
improvement in predicting the truth of a difficult mathematical sentence.

### E2. Equal cost with different beliefs or stakes

For a binary claim, suppose accepting it loses zero if true and `c` if false.
An estimated loss of `3` corresponds to estimated false probability `3/10` if
`c=10`, and `3/100` if `c=100`. Without the payoff convention, the number does
not identify belief. A realized loss of zero also differs from an estimated
expected loss of zero. The method's input types should keep all three meanings
separate.

### E3. Equal marginal costs, different joint decision

Let two Boolean costs `X,Y` each have mean `1/2`. In one source, `Y=X`; in the
other, `Y=1-X`. An action paying `max(X,Y)` has mean `1/2` in the first case and
`1` in the second. A safe action costs `3/4`. The optimal choice reverses while
the pair of marginal means stays the same. A joint probability model and an
aligned value profile can both preserve the distinction. The example is a
failure witness for an insufficient summary, not evidence that values dominate
probabilities. The underlying marginal separation is inherited from paper §2.

### E4. Useful thinking versus unweighted prediction accuracy

Suppose two unresolved binary claims both have current estimated probability
`1/2`. A wrong decision on the first costs `10`, and on the second costs `1`.
A computation reveals either claim exactly at cost `2`. Under these declared
beliefs and losses, revealing the first changes expected total cost from `5`
to `2`; revealing the second changes `1/2` to `2`. Equal accuracy improvement
has different decision value. The expected-cost comparator sees the same
distinction, and the computation's success and price must be actual inputs or
learned estimates rather than free oracle knowledge.

### E5. Logical truth versus bounded proof success

Include two decidable claims with opposite eventual truth labels and an agent
whose initial budget resolves neither. “No proof yet” is the same initial
procedure output for both; it cannot be assigned the same false truth label.
Then reveal checked evidence on a specified schedule. Measure prediction
quality and decision loss separately from the cost and success of producing a
proof. Evaluation can use a slower checker, but its result must not leak into
the earlier feature state. This is the missing extension of the phase-two
already-true request family.

## 6. Concrete error risks for the main contract

| Risk | Required correction or check |
|---|---|
| Calling all real-valued losses truth degrees | Give each coordinate an interpretation and distinguish expected loss, payoff, forecast and evidence status. |
| Treating scalar expected cost as a new form of Logical Induction | Compare with the existing expectation interface and identify a further operational target. |
| Promoting mathematical source feasibility to empirical adequacy | Keep evidence mode and coverage premise separate from exact checking. |
| Claiming a proof-search failure refutes a sentence | Retain “unresolved”; distinguish proof, refutation, eventual label and timeout. |
| Giving a learner a free consistency, truth or model-enumeration oracle | Name the operation, its access permissions and its budget or restrict the task. |
| Assuming all changing estimates must narrow monotonically | Distinguish added valid evidence, withdrawn premises, model change and loss change; reopening can be required. |
| Scoring only claims that become easy enough to reveal | Declare delay/censoring and the target population; do not infer performance on never-resolved claims from the selected subset. |
| Treating model coexistence as an advantage over bare Boolean logic | Compare with classical conditional proofs plus ordinary uncertainty, decision theory, model selection and provenance. |
| Comparing against marginal-only or forced-cascade controls | Give the strong control joint evidence, input inspection and alternative actions when available to the candidate. |
| Calling an empty source a counterpossible answer | Preserve the original antecedent, theory and interpretation; label explicit repair separately. |
| Treating proper scoring as automatic truthful self-report under feedback | Fix the outcome-generation timing or analyze report-dependent outcomes separately. |
| Learning costs after seeing the evaluated outcome | Freeze the current action loss before selection and log subsequent objective changes as new queries. |

## 7. Recommended disposition

The inherited machinery is a useful foundation for P3-01. It contributes exact
conditional comparisons, source dependence, current-request checks and explicit
revision interfaces. The new work should seek a disciplined combination of these
with bounded prediction, paid computation and counterfactual semantics. It should
not attribute a general logical-uncertainty learning capability to the current
calculus or claim an advantage merely because its outputs are numerical.

The most promising distinctive target is the interaction between unresolved
logical evidence, changing decision stakes, computational choice and justified
reuse. That is a research opportunity, not yet support for a new contribution.
