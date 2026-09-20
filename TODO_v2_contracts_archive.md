# Value Logic Follow-Up Paper: Contract Semantics and Inverse Task Recovery — TODO

Last updated: 2026-08-01

Intended repository filename: `TODO_v2.md`

## Resume here

This file is the project control document for the follow-up paper. On a fresh chat:

1. read `paper.md`, the original `TODO.md`, this file, and the latest completed checkpoint note;
2. complete **exactly the first unchecked work item** unless the user explicitly selects another;
3. treat one numbered task or one checkpoint as the entire scope of one prompt; and
4. stop after validating and recording that item.

Each work item is designed for approximately **30 minutes of GPT-5.6 Sol work at Extra High effort**. The initial roadmap contains **36 numbered tasks and 4 checkpoints: 40 work items, approximately 20 hours total**.

When finishing a work item:

1. mark it `[x]`;
2. add the completion date and a 2–5 sentence result note beneath it;
3. link every file created or materially changed;
4. update `v2/claim_ledger.md` when a claim was added, sharpened, supported, refuted, or deferred;
5. run the validation command currently recorded in `v2/README.md`;
6. make one local commit containing only that work item when working in a Git checkout, using the task/checkpoint ID in the commit message; and
7. do not begin the next item.

Do not automatically push.

### Thirty-minute scope discipline

The timebox is a design constraint, not merely an estimate.

- A prose task should normally create or revise **one principal artifact**, add roughly 600–1,200 polished words, and handle at most one main theorem plus one short corollary or counterexample.
- A literature task should verify roughly 4–6 load-bearing primary sources, not attempt an exhaustive survey.
- A proof task should prefer a sharply scoped finite theorem over a broad conjectural framework.
- A code task should implement one cohesive module or experiment stage plus focused tests.
- If a task exposes a larger problem, record the exact issue in the claim ledger or checkpoint note rather than silently expanding the task.
- If the allotted scope cannot be completed, preserve the strongest checked partial result, state the blocker precisely, and stop.

### Checkpoint protocol

A checkpoint is itself one 30-minute work item. At each checkpoint:

1. read all artifacts produced since the preceding checkpoint, plus `v2/project_spec.md`, `v2/claim_ledger.md`, and `v2/notation.md`;
2. test whether the remaining roadmap still fits the paper question and the remaining time budget;
3. inspect every unfinished item after the checkpoint for necessity, order, dependencies, and realistic half-hour scope;
4. split, merge, reorder, narrow, add, or remove future items when justified;
5. preserve completed history and prefer suffixed task IDs over renumbering already referenced tasks;
6. create the named checkpoint note recording evidence considered, accepted changes, rejected changes, risks, and the revised pending roadmap;
7. update the `Next task` pointer; and
8. stop before beginning the selected next task.

**Next task: Task 1 — Freeze the follow-up question, contribution boundary, and paper shape.**

## Estimated schedule

| phase | work items | estimated time |
|---|---:|---:|
| Scope, inheritance, and literature | Tasks 0–5 + Checkpoint A | 3.5 hours |
| Contract semantics and qualitative abstraction | Tasks 6–14 + Checkpoint B | 5 hours |
| Inverse task recovery | Tasks 15–23 + Checkpoint C | 5 hours |
| Reference implementation and synthetic experiment | Tasks 24–29 + Checkpoint D | 3.5 hours |
| Paper assembly and final audit | Tasks 30–35 | 3 hours |
| **Total** | **40 work items** | **20 hours** |

## Project question

The first paper formalized present permission to rely on a fallible model as a finite-stage, evidence-relative license. Its atom states were Supported, Open, and Refuted, and its public outcomes separated malformed requests, counterindication, unresolved evidence, and grants.

The follow-up asks:

> Can these scoped reliance judgments be understood as qualitative abstractions of values assigned to world-indexed contracts, and what task or value structure can be recovered from a sufficiently rich family of such judgments?

The main intended construction begins with a use contract

\[
X_{e,q}(w)
=
J(F_q,D_q;w)-J(e,D_q;w)-\Delta_q,
\]

whose payoff is positive when using plan \(e\) improves on the named fallback by the required margin in world \(w\). An epistemic state supplies lower and upper valuations

\[
\underline V_s(X),\qquad \overline V_s(X).
\]

The qualitative state is then obtained by the sign position of the valuation interval:

\[
\underline V_s(X)\ge 0
\Rightarrow \mathsf{Supported},
\qquad
\overline V_s(X)<0
\Rightarrow \mathsf{Refuted},
\]

with the remaining meaningful cases Open.

The inverse problem treats contract-and-price queries as observations of a latent task or valuation. The target is not a uniquely true utility function. It is the **observational quotient**: exactly the task distinctions that the declared query family can identify.

## Provisional paper thesis

The intended thesis has two connected parts:

1. **Forward semantics.** The finite-stage license calculus is a sound qualitative sign abstraction of lower and upper valuations of scoped model-use contracts. Boolean logic embeds as the indicator-contract special case, while general real-valued contracts support richer operations that should not automatically be called logical conjunction or disjunction.
2. **Inverse semantics.** A family of priced contract judgments identifies a latent task only up to observational equivalence. Threshold sweeps recover lower and upper values of queried contracts; finite-dimensional linear fragments are identifiable under explicit spanning and normalization conditions; outside those conditions, non-identifiability is structural rather than a failure of optimization.

A small synthetic experiment should test whether an active contract-query strategy recovers a finite latent-task version space more efficiently than random querying.

## Main theorem and result targets

The roadmap should aim for the following scoped results, revising them at checkpoints when necessary:

1. **Contract-abstraction theorem:** sign abstraction of a valid lower/upper valuation interval is sound for favorable and unfavorable contract value and reproduces the relevant finite-stage license atoms.
2. **Indicator embedding theorem:** Boolean events embed into bounded contracts through indicator functions, with `not`, `and`, and `or` recovered by \(1-x\), `min`, and `max`; precise expectation recovers ordinary probability.
3. **Observational quotient theorem:** every exact representation of a declared judgment family factors through its response quotient, and the quotient is the coarsest exact task code up to relabeling.
4. **Threshold-recovery theorem:** under translation-invariant valuation, judgments of \(X-p\) locate \(\underline V(X)\) and \(\overline V(X)\); a finite binary-search procedure recovers them to declared resolution.
5. **Finite linear identifiability theorem:** a normalized finite-dimensional linear valuation is recoverable from values of a spanning contract family, while incomplete span or omitted normalization yields explicit equivalence classes.
6. **Synthetic active-query result:** on one frozen finite version-space generator and metric, a balanced-split query strategy is compared prospectively with random querying.

The first five are mathematical targets. The sixth is an empirical result whose disposition must follow the frozen experiment rather than be assumed.

## Required final artifacts

1. `paper_v2.md` — the complete follow-up paper in rigorous Markdown with LaTeX.
2. `v2/claim_ledger.md` — claim roles, scopes, dependencies, evidence states, and project impacts.
3. `v2/notation.md` — the authoritative glossary and symbol table.
4. `v2/verification/` — executable finite semantics, inverse-query routines, and tests.
5. `v2/experiments/results.md` — frozen experiment design, results, and limitations.

Supporting notes may live under `v2/formalism/`, `v2/inverse/`, `v2/literature/`, and `v2/checkpoints/`.

## Inherited objects and intended changes

The follow-up should inherit rather than rebuild:

- versioned evaluated plans, contexts, finite epistemic states, profiles, and provenance;
- the separation of `Undefined` from meaningful evidential states;
- `K_3 = {Refuted, Open, Supported}`;
- explicit fallback, absolute adequacy, and profile aggregation;
- the distinction among evidence, target-world claims, current authorization, selection, and final truth;
- the architecture-neutral factorization and exact active-mask discipline.

The follow-up may reinterpret or extend:

- adequacy and fallback margins as contract payoffs;
- interval certificates as lower/upper contract valuations;
- license queries as observations from which a task quotient can be reconstructed;
- Boolean propositions as a restricted indicator-valued fragment of a larger contract algebra.

## Non-goals

This paper does not need to:

- identify truth with utility or probability;
- recover a uniquely true reward, preference, or ontology;
- claim that every coherent judgment system is representable by one probability distribution;
- solve cyclic self-authorization or unrestricted recursive judgment;
- develop a full sheaf, topos, or differential-geometric semantics for model domains;
- establish mechanistic interpretability of a neural policy;
- perform a realistic physics case study;
- prove that ReLU networks learn the proposed semantics;
- replace the first paper’s evidence and provenance discipline with numerical contract values; or
- treat `min` and `max` of arbitrary real contracts as ordinary logical conjunction and disjunction without qualification.

Those are possible later projects. The present follow-up should remain a compact contract-semantics and inverse-identification paper.

## Main risks

1. **Expectation collapse:** assuming one precise probability measure when the Open state is motivated by imprecise or incomplete valuation.
2. **Probability–utility confounding:** interpreting a value functional as belief alone when the contract payoff already contains task loss or utility.
3. **Logical overreach:** treating operations on arbitrary payoffs as if they inherited every law and interpretation of Boolean connectives.
4. **Query unrealism:** proving identification only by allowing contracts or prices that an actual judge could not evaluate.
5. **Boundary ambiguity:** mishandling inclusive support, strict refutation, and an Open valuation interval.
6. **Inherited-semantics drift:** changing the first paper’s fallback, profile, or evidence meanings while claiming an embedding.
7. **Identification overclaim:** inferring a unique latent task where only an observational equivalence class is determined.
8. **Experiment leakage:** selecting the active-query metric, task population, or stopping rule after inspecting results.
9. **Proof/implementation mismatch:** proving results for one oracle or normalization while implementing another.
10. **Scope expansion:** allowing recursive evidence, real physics, or mechanistic interpretability to consume the 20-hour paper budget.

## Definition of done

The project is complete when:

- the contract carrier, use-contract construction, valuation assumptions, and sign convention are explicit;
- the qualitative abstraction reproduces the relevant first-paper atom semantics under a stated embedding;
- indicator contracts recover the Boolean fragment with correct boundaries;
- arbitrary contract operations are carefully distinguished from Boolean logic;
- observational equivalence and the recoverable task quotient are defined;
- at least one positive identifiability theorem and at least two explicit non-identifiability countermodels are included;
- threshold recovery is given as both a theorem and executable algorithm;
- the active-query experiment is frozen before execution and reported without outcome-selected replacement;
- every main claim has a ledger entry and every citation is checked against a primary source;
- the executable semantics agree with the paper’s formulas on deterministic fixtures; and
- `paper_v2.md` passes the final notation, proof, citation, link, and claim-boundary audit.

## Numbered task queue

### Phase I — Scope, inheritance, and literature

- [x] **Task 0 — Map the inheritance boundary from the first paper.**

  Create `v2/README.md`. Read the abstract, Sections 2–4, Sections 6–8, and the conclusion of `paper.md`, plus the current original `TODO.md`. Record a compact table of: objects imported unchanged; objects reinterpreted through contracts; results used as premises; and results explicitly outside the follow-up. Identify the exact first-paper formulas for adequacy, fallback improvement, interval assessment, profile meet, and consumer-relative factorization. Do not summarize the entire paper.

  **Done when:** the note gives one authoritative inheritance table, links every inherited definition to its source section, records unresolved interface questions, and states the validation command placeholder.

  Completed 2026-08-01. Created [`v2/README.md`](v2/README.md) with the
  authoritative import/reinterpretation/premise/exclusion table and the exact
  inherited adequacy, fallback, interval-assessment, profile-meet, and
  consumer-factorization formulas. The note fixes the current validation
  command, records six unresolved contract/side-packet/valuation/oracle
  interfaces for Task 1 onward, and keeps ReLU, the original experiment,
  policy/value reconstruction, and recursive judgment outside the follow-up's
  theorem spine. Updated this [`TODO_v2.md`](TODO_v2.md) pointer to Task 1;
  repository validation passes.

- [ ] **Task 1 — Freeze the follow-up question, contribution boundary, and paper shape.**

  Create `v2/project_spec.md`. Turn the provisional thesis into a one-page specification containing the central question, 4–6 intended contributions, mathematical assumptions, final artifact list, non-goals, and a proposed 7–9 section paper outline. Decide whether the paper’s primary semantic object is a bounded real contract, a typed contract bundle, or a contract plus exact side packet. Preserve hard constraints and provenance outside any scalar that cannot carry them.

  **Done when:** every intended theorem target has a stated role in the paper and every attractive but out-of-scope direction is explicitly deferred.

- [ ] **Task 2 — Initialize the follow-up claim ledger.**

  Create `v2/claim_ledger.md` with approximately 15–20 scoped claims covering contract semantics, lower/upper valuation, Boolean embedding, abstraction, task quotients, threshold recovery, linear identifiability, non-identifiability, active querying, and the experiment. For each claim record: ID; exact statement; role; assumptions; proof/test route; support and falsification conditions; current evidence state; dependencies; and project impact if narrowed or refuted.

  **Done when:** every main theorem/result target has a ledger row and no row is labeled supported merely because it is planned.

- [ ] **Task 3 — Audit the contract-valuation literature needed by the core.**

  Create `v2/literature/contracts.md` and update or create `v2/references.bib`. Verify roughly 4–6 primary sources spanning bets/contracts, coherent previsions or lower previsions, sets of probabilities, desirability, and coherent risk/value functionals. Extract only the definitions or representation results actually needed. Distinguish a generic interval-valued functional from one represented by a credal set.

  **Done when:** each imported concept has a precise hypothesis-preserving use or is labeled analogy only; no secondary-source theorem is carried forward unverified.

- [ ] **Task 4 — Audit inverse-value and elicitation literature needed by the recovery problem.**

  Create `v2/literature/inverse.md` and update `v2/references.bib`. Verify roughly 4–6 primary sources on revealed preference, preference/value elicitation, active comparison queries, inverse decision problems, or reward/utility identifiability. Focus on observational equivalence, normalization, query richness, and active experiment design rather than surveying entire fields.

  **Done when:** the note states what is standard, what the follow-up adapts, and which stronger recovery claims are blocked by known equivalences.

- [ ] **Task 5 — Freeze notation and the theorem-dependency map.**

  Create `v2/notation.md`. Define the authoritative meanings of \(\Omega\), \(w\), \(e\), \(q\), \(F_q\), \(J\), \(X\), \(\underline V\), \(\overline V\), \(K_3\), the abstraction map, query price \(p\), oracle response, latent parameter \(\theta\), feature map \(\phi\), query family, and observational equivalence. Add a dependency graph from definitions to theorem targets and final paper sections.

  **Done when:** every symbol planned for Tasks 6–23 has one meaning, units/sign conventions are fixed, and later files are instructed to link rather than redefine notation.

- [ ] **Checkpoint A — Freeze the paper scope before formal development.**

  Create `v2/checkpoints/A_scope_freeze.md` and apply the checkpoint protocol. Decide, using Tasks 0–5, whether the main semantics will be stated through a credal set of linear expectations, a more general lower/upper valuation interface, or both with one as the representation example. Confirm that the five mathematical targets can fit the remaining 16.5 hours. Narrow or remove any target that would require a full monograph on imprecise probability, preference theory, or recursive logic.

  **Done when:** the semantic assumptions, theorem spine, paper outline, and next task are frozen prospectively.

### Phase II — Contract semantics and qualitative abstraction

- [ ] **Task 6 — Define worlds, typed use contracts, and the payoff convention.**

  Create `v2/formalism/01_contracts.md`. Define a finite or otherwise explicitly bounded world space, bounded real contracts, typed units, plan loss, fallback loss, switching margin, and

  \[
  X_{e,q}(w)=J(F_q,D_q;w)-J(e,D_q;w)-\Delta_q.
  \]

  Explain why positive payoff favors use of \(e\), how absolute adequacy remains a separate contract or requirement, and how malformed units remain `Undefined` rather than zero-valued. Include one numerical succession example.

  **Done when:** the contract is well typed, its sign convention is tested on at least three cases, and scalarization limits are recorded.

- [ ] **Task 7 — Define precise and imprecise valuation interfaces.**

  Create `v2/formalism/02_valuations.md`. Define precise expectation \(V_P(X)\), lower and upper valuation from a nonempty set of admissible linear previsions, and the minimal properties used later: monotonicity, translation by constants, and lower/upper order. State separately what follows only under positive homogeneity, convexity, or full coherence. Permit an accepted external interval interface without asserting that every such interface has a credal-set representation.

  **Done when:** every later proof can cite an explicit assumption list and probability, utility, loss, and evidential uncertainty are not collapsed.

- [ ] **Task 8 — Define the qualitative sign abstraction and public outcome interface.**

  Create `v2/formalism/03_abstraction.md`. For a meaningful contract with accepted interval \([\underline V(X),\overline V(X)]\), define Supported, Open, and Refuted using inclusive favorable equality and strict unfavorable separation. Define the malformed-request branch separately. Show how component states enter a required profile meet and recover Granted, Withheld, Refused, and Undefined.

  **Done when:** the complete boundary table covers positive, negative, crossing, equality, missing, invalid, and conflicted evidence without representing all of them by the same diagnostic.

- [ ] **Task 9 — Prove the contract-abstraction theorem.**

  Create `v2/formalism/04_abstraction_theorem.md`. Prove one compact theorem: under valid lower/upper bounds, Supported implies nonnegative value for every admissible valuation; Refuted implies strictly negative value for every admissible valuation; Open is exactly the unresolved sign region for the declared interval interface. Add one monotonicity corollary for interval refinement and one counterexample showing why a point estimate alone is insufficient.

  **Done when:** the theorem’s quantifiers and boundary conventions match Task 8 and its ledger row has an evidence disposition.

- [ ] **Task 10 — Embed the first paper’s adequacy and fallback atoms.**

  Create `v2/formalism/05_license_embedding.md`. Map first-paper adequacy \(J(e)\le\epsilon\) to the contract \(\epsilon-J(e)\), and fallback improvement to \(J(F)-J(e)-\Delta\). Show clause by clause that the interval-containment rules induce the same `K_3` state under the inherited evidence mode. State and prove a finite-profile assessment-preservation proposition, or record the smallest counterexample and repair.

  **Done when:** the follow-up has an exact documented relationship to the original calculus rather than a metaphorical similarity.

- [ ] **Task 11 — Define the algebra of bounded contracts.**

  Create `v2/formalism/06_contract_algebra.md`. Define addition, scalar multiplication, constants, order, `min`, `max`, positive/negative parts, and price translation on bounded contracts. Record unit constraints and distinguish algebraic closure from epistemic authorization. Explain which valuation properties preserve which operations or inequalities.

  **Done when:** every operation used later is typed and at least two tempting but invalid valuation identities are counterexampled.

- [ ] **Task 12 — Embed Boolean events as indicator contracts.**

  Create `v2/formalism/07_boolean_embedding.md`. For events \(A\subseteq\Omega\), use \(\mathbf 1_A\) and prove the finite Boolean embedding:

  \[
  \neg A\mapsto 1-\mathbf 1_A,\quad
  A\wedge B\mapsto\min(\mathbf 1_A,\mathbf 1_B),\quad
  A\vee B\mapsto\max(\mathbf 1_A,\mathbf 1_B).
  \]

  Show that precise expectation gives ordinary probability and that lower/upper expectation gives lower/upper event probability under the declared credal representation.

  **Done when:** the result is stated as an embedding of the indicator fragment, not as an identification of arbitrary contract value with probability.

- [ ] **Task 13 — Delimit conjunction and disjunction for general contracts.**

  Create `v2/formalism/08_general_contract_connectives.md`. Analyze `min(X,Y)` and `max(X,Y)` as worst/best payoff combinations. State sufficient conditions under which support for both component contracts supports `min(X,Y)`, and give counterexamples to invalid converse or distributive inferences under lower valuation. Explain why these operations extend the indicator fragment but do not automatically inherit ordinary propositional interpretation.

  **Done when:** the paper can answer “can we do and/or/not directly on contract values?” with exact positive constructions and exact limits.

- [ ] **Task 14 — Reconstruct multi-requirement profiles from contract atoms.**

  Create `v2/formalism/09_profiles.md`. Represent absolute adequacy, fallback improvement, latency/resource constraints, and optional comparison obligations as a finite typed family of contracts or exact predicates. Define component abstraction followed by conservative profile meet. Explain when vector/Pareto structure must remain explicit rather than scalarized.

  **Done when:** a worked profile reproduces the first paper’s running example and the root authorization cannot be manufactured from an unrelated aggregate payoff.

- [ ] **Checkpoint B — Audit and freeze the forward contract semantics.**

  Create `v2/checkpoints/B_contract_core.md` and apply the checkpoint protocol. Check every formula in Tasks 6–14 against the inherited calculus, the literature assumptions, and at least one numerical fixture. Decide which results are paper-carrying and which belong in an appendix. Specifically audit the treatment of equality, translation invariance, arbitrary interval interfaces, Boolean embedding, and general-contract `min`/`max`.

  **Done when:** the forward semantics are internally consistent, the inverse query language can be defined without changing them, and any failed theorem target has a scoped replacement.

### Phase III — Inverse task recovery

- [ ] **Task 15 — Define the priced-contract judgment oracle.**

  Create `v2/inverse/01_oracle.md`. Define a query as a typed contract \(X\) and price \(p\), evaluated through the translated contract \(X-p\). Specify the three meaningful oracle responses and the malformed branch. State which contracts and prices are admissible, whether the oracle exposes diagnostics or only public state, and how repeated equivalent queries are normalized.

  **Done when:** the oracle is deterministic relative to a latent valuation state and its response boundaries follow directly from Tasks 7–9.

- [ ] **Task 16 — Define observational equivalence and the recoverable task quotient.**

  Create `v2/inverse/02_observational_quotient.md`. Let latent task/valuation models be equivalent when they produce the same responses for every query in a declared family. Define finite-family and universal-family quotients, explain why the quotient—not a uniquely true utility—is the inverse target, and give two distinct latent models that are observationally equivalent under a weak query family.

  **Done when:** identifiability claims can be stated as singleton quotient classes rather than informal “recovery.”

- [ ] **Task 17 — Prove the observational quotient factorization theorem.**

  Create `v2/inverse/03_quotient_theorem.md`. Adapt the first paper’s consumer-relative factorization result to the inverse setting. Prove that an exact task code for the declared response family must separate every pair separated by the response map, and that the response image is the coarsest exact code up to relabeling. State clearly that this is a structural quotient theorem, not recovery of hidden mechanism.

  **Done when:** the theorem is proved in a page or less and one example distinguishes public-response and audit-response quotients.

- [ ] **Task 18 — Prove interval recovery by threshold sweep.**

  Create `v2/inverse/04_threshold_recovery.md`. Under translation invariance, prove that responses to \(X-p\) locate the lower and upper values of \(X\): support below the lower boundary, refutation above the upper boundary, and Open between them with the chosen equality convention. Give the exact set-theoretic formulas for recovering both boundaries from an ideal continuum of price queries.

  **Done when:** the formulas handle degenerate precise value, nonzero imprecision interval, and boundary equality correctly.

- [ ] **Task 19 — Give a finite-resolution recovery algorithm.**

  Create `v2/inverse/05_finite_recovery.md`. Specify a bounded price interval and a binary-search or grid algorithm that recovers each valuation boundary to resolution \(\delta\). Prove a query bound such as \(O(\log((b-a)/\delta))\) under the stated oracle and show how three-way responses alter the search. Include deterministic pseudocode suitable for direct implementation.

  **Done when:** the algorithm has a termination condition, an error guarantee, and one manually checked trace.

- [ ] **Task 20 — Define the finite-dimensional linear task fragment.**

  Create `v2/inverse/06_linear_fragment.md`. Define contract features \(\phi(X)\in\mathbb R^d\), a normalized parameter set \(\Theta\), and precise valuation \(V_\theta(X)=\theta^\top\phi(X)\). Explain what \(\theta\) represents and does not represent, why normalization or an anchored constant is necessary, and how price queries become half-space observations and version-space constraints.

  **Done when:** the fragment is expressive enough for the experiment but narrow enough for an elementary identifiability theorem.

- [ ] **Task 21 — Prove a finite linear identifiability theorem.**

  Create `v2/inverse/07_linear_identifiability.md`. Prove a theorem of the following scale: if values of a spanning feature family are recoverable through priced queries and the normalization is fixed, then \(\theta\) is uniquely determined; conversely, a nontrivial null direction in the queried feature span yields observationally equivalent parameters. Use a matrix-rank formulation and one concrete \(d=2\) example.

  **Done when:** both directions are proved, assumptions match Task 20, and no stronger preference-identification claim is implied.

- [ ] **Task 22 — Build the non-identifiability countermodel suite.**

  Create `v2/inverse/08_nonidentifiability.md`. Give at least three finite countermodels: insufficient contract span; omitted scale or affine normalization; and probability–utility/task-payoff confounding. Optionally add a fourth showing that public `K_3` responses identify less than exact price boundaries. For each, state exactly which stronger claim fails and which quotient-level claim survives.

  **Done when:** every countermodel is small enough to verify by hand and its project impact is propagated to the claim ledger.

- [ ] **Task 23 — Design the active query rule and frozen comparison metric.**

  Create `v2/inverse/09_active_queries.md`. For a finite candidate version space, define a query rule that maximizes a prospective balanced split, entropy reduction, or worst-case elimination across Supported/Open/Refuted responses. Give deterministic tie-breaking, pseudocode, stopping rules, and a random-query baseline. Predefine the experiment’s primary metric and any secondary metrics; do not run the final comparison yet.

  **Done when:** the active policy can be implemented without additional design choices and the primary endpoint is frozen before data generation.

- [ ] **Checkpoint C — Audit inverse claims and freeze the experiment.**

  Create `v2/checkpoints/C_inverse_and_experiment_freeze.md` and apply the checkpoint protocol. Verify the quotient, threshold-recovery, finite algorithm, linear-identifiability, and countermodel results against the exact oracle. Freeze the candidate-task generator, admissible query pool, seeds, stopping rule, primary endpoint, baseline, and result table schema. Remove any empirical hypothesis that cannot be tested in the remaining 3.5 experiment hours.

  **Done when:** the experiment can be executed mechanically from the checkpoint note and no outcome-dependent redesign remains available.

### Phase IV — Reference implementation and synthetic experiment

- [ ] **Task 24 — Scaffold the `v2` verification package and validation command.**

  Create `v2/verification/` with a small package entry point, deterministic test runner, and README section recording the single validation command. Add typed dataclasses or equivalent minimal structures for finite worlds, contracts, valuation states, queries, and responses. Do not implement active querying yet.

  **Done when:** `python -m v2.verification` runs a smoke test from the repository root and the package layout matches the notation.

- [ ] **Task 25 — Implement contract algebra and valuation semantics.**

  Implement bounded finite-world contracts, algebraic operations, precise expectation, credal-set lower/upper expectation, and price translation. Add focused tests for order, constants, indicator contracts, and at least two invalid-operation guards involving units or malformed dimensions.

  **Done when:** the implementation reproduces the formulas in Tasks 6, 7, 11, and 12 on deterministic fixtures.

- [ ] **Task 26 — Implement qualitative abstraction and first-paper embedding fixtures.**

  Implement `K_3`, malformed/public outcomes, sign abstraction, component profile meet, and diagnostic payloads. Add tests for favorable equality, strict refutation, crossing intervals, missing/invalid evidence, and the adequacy/fallback examples from Task 10.

  **Done when:** every boundary row in Task 8 has one executable regression and the embedding fixture produces the same assessment on both representations.

- [ ] **Task 27 — Implement finite latent tasks, the oracle, and version-space filtering.**

  Implement the linear fragment from Task 20, a finite candidate set, priced-contract oracle responses, and exact filtering of candidates by observed responses. Add tests for observational equivalence, singleton identification, and a non-identifiable null-space example.

  **Done when:** a fixed hand-built sequence of queries shrinks the version space exactly as predicted in Tasks 16–22.

- [ ] **Task 28 — Implement active querying and the random baseline.**

  Implement the frozen query-selection rule, deterministic tie-breaking, random baseline, stopping condition, and metrics from Task 23/Checkpoint C. Add tests showing that the selected query has the declared split score and that no hidden access to the true task enters query choice.

  **Done when:** both policies can run on the same frozen candidate/query pool and emit a complete trace.

- [ ] **Task 29 — Execute and report the frozen synthetic experiment.**

  Run the exact experiment frozen at Checkpoint C. Save machine-readable configuration and results, plus `v2/experiments/results.md` containing the primary comparison, uncertainty or seed variation, failure cases, and a trace example. Generate at most one figure if it materially clarifies query efficiency. Do not replace the endpoint or rerun with outcome-selected settings unless a documented implementation bug invalidates the run.

  **Done when:** raw and summarized outputs are linked, reproducible, and the claim ledger records supported, refuted, or inconclusive dispositions.

- [ ] **Checkpoint D — Audit the empirical result and freeze publication claims.**

  Create `v2/checkpoints/D_experiment_audit.md` and apply the checkpoint protocol. Inspect code, tests, frozen configuration, raw outputs, and summaries. Determine exactly what the experiment supports about active querying, what it does not establish about human judgment or natural tasks, and whether any implementation bug requires a prospectively documented rerun. Freeze the result language for the paper.

  **Done when:** Tasks 30–35 can assemble the paper without inventing new analyses or changing the experiment claim.

### Phase V — Paper assembly and final audit

- [ ] **Task 30 — Create the paper skeleton, abstract, and introduction.**

  Create `paper_v2.md` with the final section structure. Write a complete abstract and introduction explaining the transition from scoped reliance licenses to contract values and inverse task recovery. State contributions with their exact mathematical or empirical status, explain the relationship to the first paper, and include a compact running example.

  **Done when:** the opening makes the central idea legible without requiring the reader to know the repository and does not promise results absent from completed artifacts.

- [ ] **Task 31 — Assemble the forward contract-semantics sections.**

  Integrate Tasks 6–14 into the paper’s formal core. Include the use-contract definition, valuation interface, qualitative abstraction, embedding of the old license atoms, Boolean indicator fragment, and limits for arbitrary contract operations. Move long proof details to an appendix rather than rewriting them.

  **Done when:** every forward theorem statement links to a completed proof artifact, notation matches `v2/notation.md`, and the first-paper relationship is explicit.

- [ ] **Task 32 — Assemble the inverse recovery sections.**

  Integrate Tasks 15–23 into the paper. Present the oracle, observational quotient, threshold recovery, finite algorithm, linear fragment, identifiability theorem, non-identifiability countermodels, and active-query design in dependency order.

  **Done when:** “task recovery” is consistently stated at quotient or theorem-supported scope and every stronger unavailable interpretation is excluded nearby.

- [ ] **Task 33 — Write the experiment, discussion, and limitations sections.**

  Integrate Checkpoint C, Task 29, and Checkpoint D. Report the frozen generator, query policies, endpoint, results, and trace. Discuss query realism, public-state information loss, probability–utility confounding, finite-dimensional assumptions, and the distinction between synthetic identification and human or scientific task recovery.

  **Done when:** every numerical statement is traceable to a result artifact and negative or null findings are reported with the same precision as positive ones.

- [ ] **Task 34 — Complete related work, conclusion, and proof appendices.**

  Write the related-work section from the two verified literature notes, emphasizing structural overlap and claim boundaries. Add a conclusion, concise future-work section, and appendices containing proof details or countermodel tables omitted from the main line. Future work may mention real physical model hierarchies, recursive evidence bridges, local-to-global semantics, and policy interpretability without presenting them as completed results.

  **Done when:** all citations resolve, novelty language is conservative, and the main text remains readable.

- [ ] **Task 35 — Cross-check, validate, and freeze the follow-up paper.**

  Read `paper_v2.md` end to end against `v2/project_spec.md`, `v2/notation.md`, `v2/claim_ledger.md`, all checkpoint notes, and executable results. Audit definitions, quantifiers, boundary conventions, proof references, citations, numerical claims, links, and inherited first-paper terminology. Run the full validation command, repair only genuine inconsistencies, mark this task complete, and set `Next task` to publication or external review.

  **Done when:** the repository validation is green, every main claim has a final ledger state, all required artifacts exist, and no TODO placeholder remains in `paper_v2.md`.

## Deferred follow-up branches

These are intentionally outside the initial 20-hour roadmap. A checkpoint may promote one only by removing equivalent work elsewhere.

1. A real numerical-physics hierarchy with cheap approximations, validated error estimators, expensive reference solvers, routing, and fallback cost.
2. A local-to-global or sheaf-like semantics for domain restriction, overlap, transport, and gluing of licensed models.
3. First-class evidence bridges whose own licenses may expire or be revised.
4. Monotone fixed-point semantics for carefully controlled cyclic or recursive judgment.
5. Policy/value interpretability experiments measuring behavioral, representational, causal, and human-use evidence separately.
6. Sequential task recovery when the queried agent changes the future state distribution.
