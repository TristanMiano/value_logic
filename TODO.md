# Value Logic Project: Context and TODO

Last updated: 2026-07-12

## Resume here

This file is the project control document. On a fresh chat, read this file first, then complete **exactly the first unchecked work item**—a numbered task or a named checkpoint—unless the user explicitly selects a different item. One task or checkpoint is the intended scope of one user prompt.

When finishing a task or checkpoint:

1. mark it `[x]`;
2. add its completion date and a short result note beneath it;
3. link every file it produced or materially changed;
4. record unresolved questions in the claim ledger or decision log named by the task;
5. stop before beginning the next work item.

When the workspace is a Git repository, make one local commit per completed task or checkpoint after validation, with the task/checkpoint ID in the message. Do not automatically push unless the user asks. This makes the repository history mirror the project's append-only provenance discipline.

### Artifact discipline

Each new research artifact should begin with a compact durable summary of definitions, decisions, results, and unresolved obligations. Aim for roughly 3,000 words of main-line exposition per task when the mathematics permits; place long proofs, exhaustive examples, or raw audits in clearly linked appendices rather than deleting qualifications. Task 13 must establish a central notation/glossary index so later consolidation does not silently change meanings.

### Checkpoint protocol

Checkpoints are roadmap-review tasks, not ceremonial status updates. At each checkpoint:

1. read the artifacts produced since the previous checkpoint, plus this TODO, the project specification, claim ledger, and decision log;
2. compare the accumulated results, counterexamples, literature findings, and implementation constraints with the project question and required final artifacts;
3. re-evaluate **every still-unfinished work item after the checkpoint** for necessity, order, dependencies, scope, and feasibility;
4. split, merge, reorder, add, narrow, or remove future work when justified, while preserving completed artifacts and their historical completion notes;
5. update stale task references and the `Next task` pointer if the roadmap changes;
6. create the checkpoint note named by the checkpoint, recording evidence considered, course corrections, rejected changes, new risks, and the revised pending roadmap;
7. if no correction is needed, record why the current roadmap remains appropriate;
8. stop without beginning the newly selected next task.

Checkpoint edits apply prospectively. They may add follow-up work for a completed result, but they do not silently mark completed work undone or rewrite its history. Prefer stable checkpoint labels and suffixed new tasks over renumbering tasks that are already referenced elsewhere.

**Next task: Task 13 — Select the smallest publishable logic and state its metatheory goals.**

## Project question

Physics develops through sequences of theories. A successor can show that a predecessor is not universally correct while retaining it as a useful approximation on a restricted domain. The sequence may be indefinitely extendable, and a bounded agent may never be entitled to conclude that its present theory is final.

The project asks:

> What kind of logic can represent theory use under indefinite, domain-sensitive supersession without requiring an agent to claim possession of final truth, and how can that logic be represented or learned by a basic ReLU multilayer perceptron, preferably with cross-entropy or a closely related loss?

## Three opening derivation questions

These questions should appear near the beginning of both final artifacts, before the mature formalism is presented. The reader should see which parts of the formal object are forced by the motivating problem and which parts are later modeling choices.

### 1. Does the main question itself yield `Pi(M,D,epsilon)`?

Not in its exact final form. The main question immediately motivates two indices:

- `M`, because the object under evaluation is a model or theory;
- `D`, because the motivating phenomenon is precisely that a superseded theory can remain usable on a restricted domain.

The pragmatic background then motivates a performance comparison: a bounded agent may be unable to certify that `M` is true, while still being able to compare `M` with observations or with outcomes on a background task. To turn that comparison into a yes/no permission to rely on `M`, one introduces a discrepancy or loss functional `L` and a tolerated upper bound `epsilon`:

```text
Pi(M; D,L,epsilon)  iff  Risk_L(M on D) <= epsilon.
```

Thus `epsilon` is not “the probability that the theory is false.” It is a task- and loss-relative tolerance: the largest measured or estimated discrepancy the application will treat as negligible. The compressed notation `Pi(M,D,epsilon)` suppresses `L` and other indices only after those are fixed by context.

The exact scalar form is not forced. A vector of losses and tolerances, a partial order, a regret bound, or a calibrated chance constraint may be more appropriate. Sampling uncertainty also means that observed risk is an estimate, so a fuller form may require a confidence/calibration level. The paper must present the derivation in stages:

```text
indefinite succession
    -> domain-relative use
    -> observable/task-relative performance
    -> loss or discrepancy
    -> tolerance epsilon
    -> uncertainty/calibration and agent/stage indices.
```

### 2. What is `Pi(M,D,epsilon)` represented as, and where is its information?

The project must not identify four distinct objects without argument:

1. the structured logical judgment `Pi(M;D,L,epsilon,...)`;
2. vector encodings of `M`, cases, and/or `D`;
3. a signed preactivation or predicted adequacy margin;
4. the rectified ReLU output.

A candidate loss-first construction is

```text
s_i(x,epsilon) = log(epsilon) - predicted_log_loss(M_i,x),
ell_i(x,epsilon) = ReLU(s_i(x,epsilon)).
```

Here `s_i` contains both positive and negative adequacy information. `ell_i > 0` is a grant and its magnitude is remaining slack; `ell_i = 0` deliberately quarantines failure but erases how badly the test failed. Therefore ReLU is best treated initially as a gate plus positive margin, not as the complete representation of the judgment.

The vectors should, where possible, be derived backward from operational data rather than stipulated. A model-by-case loss matrix or tensor can be factorized so that model embeddings encode capability profiles and case/domain embeddings encode demand profiles. Physics can add constrained coordinates from dimensionless groups and perturbative correction sizes. These encodings are generally identifiable only up to transformations that preserve predicted loss, so “the network learned the ontology” requires additional evidence.

### 3. In what sense do domains form an atlas and get stitched together?

There are two candidate atlases, and the paper must not conflate them:

- **Scientific-model atlas:** separately meaningful models `M_i` have licensed regions `D_i(epsilon)`. These regions may overlap or leave gaps. Stitching requires an explicit router and bridge conditions that bound predictive or decision disagreement on overlaps. Hard routing can be discontinuous; soft routing or matched bridge models can preserve continuity. Abstention is required where no chart is licensed.
- **Intrinsic ReLU atlas:** a fixed ReLU network partitions its input space by activation pattern into finitely many polyhedral regions, and computes an affine map on each region. Because the network is continuous, adjacent affine pieces agree on their shared boundary, although their Jacobians can differ.

Fable's strongest observation is valid at the structural level: the second atlas is native to the ReLU function class, and depth permits much richer piecewise-linear region maps than a single half-space test. But this does **not** by itself show that the regions correspond to Newtonian, relativistic, or other scientific domains. The central neural question is whether a loss-grounded architecture and training process can align the intrinsic activation atlas with the scientific-model atlas closely enough to implement the intended license logic.

## Required final artifacts

1. `paper.md`: a rigorous, LaTeX-heavy, GitHub-Gist-compatible Markdown paper.
2. `substack_post.txt`: a Substack-compatible version with no Markdown syntax, minimal equations/LaTeX, and the same argument in readable prose.

Research notes, code, data, figures, and verification scripts may be added as supporting artifacts, but these two are the required deliverables.

## Cross-project interpretability goal

The parallel repository [`TristanMiano/policy_value_isomorph`](https://github.com/TristanMiano/policy_value_isomorph) is a concrete companion experiment. Its current scope is deliberately narrower than a universal policy–value isomorphism: it freezes a policy in small deterministic games, estimates policy-induced `V^pi(s)` or `Q^pi(s,a)` from rollouts, trains scalar value models, and measures how well argmax/argmin decisions reconstruct the original policy.

As currently implemented, this is primarily **behavioral reconstruction**. The policy MLP and value/Q MLPs receive raw state encodings and are trained separately. The recovered value network need not share the policy network's hidden representation or causal mechanism. Consequently, high action agreement establishes a faithful surrogate on the evaluated distribution, not yet mechanistic interpretability.

One late-stage goal of this project is to determine whether the license logic supplies a representation that improves transparency into such a policy network. The desired bridge is:

```text
opaque policy behavior
    -> rollout- or preference-induced V/Q constraints
    -> loss-grounded adequacy/license representation
    -> domains/charts, margins, bridges, and decision traces
    -> a transparent surrogate or probe whose limits are explicit.
```

Transparency must be evaluated at several strengths:

1. **behavioral fidelity:** reconstructed actions and outcome distributions match the policy;
2. **value fidelity:** the recovered `V`/`Q` predicts rollout returns and action rankings;
3. **domain fidelity:** the transparent logic states where the reconstruction is licensed and abstains outside supported regions;
4. **representational alignment:** recovered charts/features correspond stably to policy hidden states or directions;
5. **causal faithfulness:** interventions on the proposed value/license features change policy behavior as predicted;
6. **human inspectability:** the representation compresses decisions into understandable margins, comparisons, local rules, or chart transitions.

The paper must not collapse these grades into a single word, “interpretability.” A simple surrogate may satisfy the first two while failing the last three.

The universal target also needs a qualification exposed by the companion code: a policy alone does not determine the usual return-based `V^pi`. Reconstruction requires an environment/transition model, a return or preference convention, a sufficiently Markov state, and a distribution over evaluated states or histories. The companion repository supplies these through game rules, terminal utilities, perspective conventions, and rollout sampling. Task 22 will state the strongest general reconstruction problem that survives these dependencies.

## Current working thesis (provisional)

The most promising object is not a replacement truth value but a **provisional, indexed license**. A bounded agent at stage `t` licenses a model `M` only relative to a domain `D`, loss functional `L`, tolerance `epsilon`, evidential confidence/calibration level, computational cost or budget, and the model library actually searched. A license can be defeated by new observations or by discovery of a model that dominates it. A superseded model can remain licensed on subdomains or because it remains Pareto-optimal in accuracy, coverage, cost, and robustness.

A candidate neural realization is loss-first:

```text
s_i(x, epsilon) = log(epsilon) - predicted_log_loss(M_i, x)
license_margin_i(x, epsilon) = ReLU(s_i(x, epsilon)).
```

Positive margin licenses model `M_i` for case `x`; zero does not assert its negation. The signed preactivation must remain available whenever the degree of failure matters. A domain-level license must then aggregate or certify pointwise claims over a set or distribution `D`. Deep ReLU networks induce continuous piecewise-affine regions, providing one possible finite atlas of local computations; a separate argument is needed to align those regions with a scientific-model atlas. This is a research hypothesis, not yet an established logic or theorem of this project.

The intended logic must keep three levels distinct:

- **object level:** a model's predictions or rules within a stated regime;
- **license level:** an agent's defeasible judgment that a model is adequate for a domain and purpose;
- **limit/meta level:** external claims about eventual stability, finality, or convergence, which a finite-stage agent generally cannot certify.

## Non-negotiable distinctions

The following distinctions must remain explicit throughout the work:

- truth versus empirical or decision-theoretic adequacy;
- a single case `x` versus a domain `D` (a set, distribution, or task family);
- a theory, a fitted model, a representation/frame, and a model-selection policy;
- a policy alone versus a policy coupled to dynamics, returns/preferences, and a state distribution;
- predictive loss versus decision regret versus computational cost;
- a Boolean license versus its real-valued safety margin;
- a signed adequacy score versus the information-erasing zero branch of ReLU;
- a logical judgment versus its vector encoding, scalar preactivation, and gated output;
- “no better retrieved model was found” versus “no better model exists”;
- retention of past records versus monotonic retention of current beliefs;
- representability by a ReLU network versus learnability by gradient descent;
- behavioral surrogate fidelity versus representational alignment and causal/mechanistic explanation;
- the geometry of a network's linear regions versus their interpretation as scientific regimes;
- a scientific-model atlas/router versus the intrinsic activation-region atlas of one ReLU function;
- internal certification/provability versus external eventual stability;
- ordinal preference, scalar utility, and multi-objective/Pareto comparison.

## Source map and inherited ideas

All six pre-existing files were read before this TODO was created.

### `llm_convos/chatgpt.txt`

The most operational recent line of thought. It develops:

- `Adequate(T,D,L,epsilon,alpha)` as a loss-relative, confidence-sensitive predicate;
- nested adequacy for model-building choices, frames, units, idealizations, parameters, solvers, and selection policies;
- error budgets and vertical versus horizontal composition;
- ReLU activations as positive adequacy margins;
- model and domain encodings, bilinear compatibility, tiled adequacy regions, and routing;
- a later correction from hand-labeled vectors to a record-derived loss matrix;
- log dimensionless coordinates, omitted-correction profiles, tied `log(epsilon)` dependence, and abstention when no model is licensed.

### `llm_convos/claude.txt`

The most ambitious formal line. It develops:

- agent-, time-, library-, and search-budget-indexed licenses;
- empirical defeat versus discovery of a dominator;
- Pareto retention of old theories;
- atlases of local theories with seams/bridges;
- a separation between finite internal certificates and external stability;
- Löbian claims for stage-local certification and anti-Löbian claims for open-ended refinement;
- a proposed identification of ReLU linear regions with affine atlas charts;
- depth as nested licensing, tropical and many-valued interpretations, and training as supersession;
- loss-tensor factorization, Buckingham-pi/log coordinates, perturbative correction profiles, calibrated routing, and abstention.

The Fable discussion makes a useful structural case: activation patterns index polyhedral regions; a ReLU network is affine on each region; continuity supplies exact agreement of the network's adjacent affine pieces on shared facets; and depth constructs bounded, disconnected, or combinatorially rich regions unavailable to a single affine threshold. It also proposes interpreting a neuron as an incoming license test plus outgoing licensed content and emphasizes that the positive ReLU value is unused tolerance or margin. The project must qualify this optimism in two ways. First, an intrinsic activation-region decomposition is not automatically a decomposition into human-interpretable scientific models. Second, separately implemented physical models usually require approximate overlap conditions, routing, or bridge models rather than the exact continuity inherited by the affine pieces of one network.

Many theorem names, exact statements, and citations in this conversation have not yet been verified.

### `posts/utility_preference_logic_nn.md`

A survey-style draft connecting preference logic, planning, differentiable logic, score semantics, open-set/Heyting semantics, ReLU min/max constructions, and loss-induced preference orders. It contains a useful bibliography and several strong technical claims that require source and proof audits before reuse.

### `posts/judgement_value_fact_recovery.txt`

Argues that recursively evaluating judges pressures them to recover stable factual structure; introduces “excellence centroids” and the “latent geometry of excellence”; treats truth as a pragmatic limit of increasingly successful theories; and gives a cautious policy-to-value reconstruction argument.

### `posts/utility_all_you_need.txt`

Develops belief/value duality, task delineation `T`, judgment `J`, the informal claim `T = J^2`, recursive valuation, and arguments against simple value-fragility pictures. These are motivating intuitions, not established results.

### `posts/condensed-response-hidden-complexity.txt`

States the strongest policy–utility “isomorphism” and value-complexity claims. These require substantial qualification: occupancy or visitation counts are not generally a utility function, policies do not uniquely identify rewards, and utility-to-policy conversion requires an environment model and decision rule.

### Parallel repository: `TristanMiano/policy_value_isomorph`

The `main` branch was inspected through GitHub on 2026-07-10. The repository has progressed beyond its original tabular slice:

- a heuristic tic-tac-toe policy and trainable one-hidden-layer policy MLP;
- rollout generation for fixed-perspective `V^pi(s)` targets;
- separate state-value and action-value MLP regressors;
- successor-value and direct-Q policy recovery;
- action agreement, top-k, W/D/L, and value-calibration utilities;
- symmetry, sampling, telemetry, checkpointing, tests, and a partial Connect Four port;
- an active plan to migrate manual list-based/tanh training to PyTorch while preserving behavior and artifacts.

The policy model is presently trained by masked cross-entropy imitation; `V` and `Q` are trained by MSE on rollout-derived terminal returns. Tests establish basic loss reduction, sign conventions, legal actions, modest agreement/MAE thresholds, and recovery of simple forced moves. The current code does not inspect policy hidden activations, share a latent space between policy and value models, learn a ReLU atlas, or establish causal correspondence between recovered value features and the policy's internal computation. Those are opportunities for the cross-project interpretability task rather than existing results.

## Main research risks

1. **Relabeling risk:** calling loss minimization a “logic” without defining syntax, semantics, consequence, and proof/update rules.
2. **Conflation risk:** treating `x`, `D`, model descriptions, theory families, and neural embeddings as the same kind of object.
3. **Circularity risk:** hand-encoding “handles strong gravity” and then claiming the embedding discovered adequacy.
4. **Scalarization risk:** hiding coverage, error, robustness, cost, and risk in one arbitrary number.
5. **Finality risk:** covertly reintroducing final truth through a stability, best-model, or complete-library operator.
6. **Neural overclaim risk:** CPWL representability does not show that SGD learns scientifically meaningful charts.
7. **Loss mismatch risk:** ordinary softmax cross-entropy forces a choice even when several models are adequate or none is; multi-label, ranking, selective, or calibration losses may be necessary.
8. **Citation risk:** the LLM conversations contain plausible but unverified attributions, theorem formulations, and complexity claims.
9. **Philosophical overclaim risk:** pragmatic adequacy can guide bounded belief without entailing that truth is identical to usefulness.
10. **Identifiability risk:** behavior and loss matrices generally underdetermine utilities, latent coordinates, mechanisms, and ontologies.
11. **Rectification risk:** `ReLU(s)=0` collapses every negative margin, so the rectified value alone cannot encode the kind or magnitude of inadequacy.
12. **Atlas-equivocation risk:** the CPWL regions of one neural function may be called an atlas in a precise structural sense, but that does not identify them with the domains of a library of scientific theories.
13. **Surrogate-interpretability risk:** an independently trained value network can reproduce actions without identifying the internal computation or reasons implemented by the original policy network.

## Definition of done

The project is complete only when:

- the formal language, semantics, consequence relation, and update dynamics are explicit;
- at least three paper-carrying results from distinct stability, update/profile/diagnostic, transport/routing, or neural representation clusters are proved or replaced by precise countertheorems;
- the precise ReLU representation claim is stated and proved or cited correctly;
- representability, trainability, and empirical interpretation are separated;
- a reproducible toy experiment tests the proposed encoding and at least one failure case;
- the connection to policy-to-value reconstruction is evaluated with separate behavioral, domain, representational, causal, and inspectability criteria;
- cross-entropy is either justified in a precise role or replaced with a documented alternative;
- all technical citations are checked against primary sources;
- counterexamples and limitations are presented alongside positive results;
- both final artifacts agree on claims while matching their respective formatting constraints.

## Claim-status discipline

The project will not assign early truth-likelihood labels merely because a claim is ambitious, unfamiliar, positively framed, or negatively framed. The claim ledger separates three dimensions:

1. **Role:** motivation, definition proposal, mathematical conjecture, empirical hypothesis, interpretive thesis, or known result to verify.
2. **Testability:** formally falsifiable by proof/countermodel, empirically falsifiable after operationalization, addressed by an identifiable literature, currently underspecified but potentially testable, or likely unfalsifiable in its present form.
3. **Evidence state:** uninvestigated, evidence located but not checked, test proposed, test performed and supportive within scope, test performed and falsifying within scope, or inconclusive.

“Likely false,” “refuted,” and comparable negative dispositions may be used only after one of the following:

- a sufficiently similar, precisely stated claim is found in reliable research literature and the relevant falsification/result is verified; or
- this project first gives the claim an explicit falsifiable formal or empirical reading and then supplies a valid proof, countermodel, counterexample, or experiment against it.

The same rule applies to negative claims. Statements such as “no policy can reveal value,” “no ReLU representation can align with scientific domains,” or “the theory sequence never terminates” do not receive a lower evidential burden merely because they deny something. Positive and negative formulations must expose their quantifiers, scope, and possible counterevidence symmetrically.

Whenever a claim receives a falsified/refuted disposition, its ledger row must also state the result's **project impact**: whether it threatens the central goal or only narrows a mechanism/theorem; which definitions, proofs, experiments, neural outputs, roadmap items, and final-publication claims must change; what narrower claim survives; and whether a repair task or checkpoint action is required. A falsification is not fully propagated until this consequence analysis is recorded.

## Numbered task queue

- [x] **Task 0 — Inventory the repository and create the resumable TODO.**

  Completed 2026-07-10. Read all six pre-existing files, synthesized the project question, recorded the source map, identified high-risk inherited claims, and created this control document.

- [x] **Task 1 — Build the inherited-claim ledger.**

  Create `notes/claim_ledger.md`. Extract the major mathematical, logical, philosophical, and ML claims from the six local source files and the inspected `policy_value_isomorph` companion repository. For each claim, record: source; exact quotation location or paraphrase; precise restatement with quantifiers and scope; role; testability class; current evidence state; dependencies; a candidate proof, countermodel, experiment, or literature comparison; and what outcome would count as support, falsification, or inconclusive evidence. Initial testability labels should include `formally falsifiable`, `empirically falsifiable after operationalization`, `literature-addressable`, `underspecified but potentially testable`, and `likely unfalsifiable as stated`. Do not label claims likely false or true, and do not settle them in this task.

  Completed 2026-07-10. Created [`notes/claim_ledger.md`](notes/claim_ledger.md) with 65 scoped claims across theory succession, recursive judgment, policy–value correspondence, preference logic, finite-stage licenses, ReLU semantics/atlases, and the companion implementation. Each row records role, testability, evidence state, and explicit support/falsification/inconclusive conditions. Added cross-claim dependencies, immediate formal sanity checks, urgent operationalization targets, and handoffs to later tasks. No truth-likelihood or final evidence dispositions were assigned.

- [x] **Task 2 — Derive `Pi(M,D,epsilon)` and explain `epsilon`.**

  Create `notes/motivation_pi_epsilon.md`. Begin only from the main theory-succession question and derive which arguments of `Pi` are forced, which are pragmatically motivated, and which are optional refinements. Explain the progression from observations or background tasks to discrepancy, loss, domain risk, tolerance, calibration, and decision regret. Determine when a scalar `epsilon` is justified and when a vector tolerance or partial order is required. This note is intended to become the opening conceptual derivation in both final artifacts.

  Completed 2026-07-10. Created [`notes/motivation_pi_epsilon.md`](notes/motivation_pi_epsilon.md). Derived `M` and `D` directly from domain-sensitive theory succession, then derived loss, domain risk, tolerance, calibration, and library-relative comparison as separate pragmatic steps. Added the fallback/status-quo route `epsilon_B(D)=J(B,D)-Delta`, giving ReLU a positive-surplus interpretation, while proving why baseline improvement must remain distinct from hard adequacy. Recommended factoring `Pi` into certified adequacy, improvement over fallback, and admissibility among retrieved alternatives. Recorded scalar/vector conditions, elementary monotonicity and retention results, the inclusive-threshold/ReLU boundary issue, worked examples, and a draft opening argument. Added claims A08–A09 to the claim ledger.

- [x] **Task 3 — Separate the representations and locate their information content.**

  Create `notes/representation_layers.md`. Distinguish the typed judgment `Pi`, encodings of models/cases/domains, the signed adequacy score, the ReLU output, and the downstream licensed content. Analyze exactly what information is preserved or lost at each map. Develop the loss-first/inverse-utility idea far enough to state the central encoding problem without yet selecting a final architecture.

  Completed 2026-07-10. Created [`notes/representation_layers.md`](notes/representation_layers.md). Separated the structured license, evidence, model/case/domain encodings, predicted risks, component margins, ReLU gates, routing, content, and actions. Defined lossless, task-sufficient, decision-sufficient, approximate, and interpretive preservation; compared model and domain encoding strategies; formulated a loss-tensor-based central encoding problem; separated negative loss from recovered utility; and audited information loss at every layer. Proved elementary results for ReLU non-injectivity, exact paired-ReLU signed encoding, calibration buffers, bilinear non-identifiability, and conjunction compression. Preserved provenance and signed component margins as transparency requirements without choosing a final architecture. Added claims F21–F26 to the claim ledger.

- [x] **Task 4 — Disambiguate and evaluate the two atlas claims.**

  Create `notes/atlas_questions.md`. Closely reconstruct Fable's argument about ReLU activation regions, affine charts, seams, exact bridges, and depth. Separately define the desired scientific-model atlas with overlapping domains, approximate bridges, gaps, routing, and abstention. State the alignment question connecting the two and list the claims that will later need proof or empirical evidence.

  Completed 2026-07-10. Created [`notes/atlas_questions.md`](notes/atlas_questions.md). Distinguished the scientific licensed model cover, the intrinsic ReLU activation complex, and the router's selection partition. Made overlapping, nested, coincident, and uncovered domains first-class; derived active-set cells for every licensed model subset; separated adequacy, dominance, selection, and archival retention; and defined exact, approximate, statistical, decision, asymptotic, translated, and unresolved bridge types. Showed conditionally how continuous overlap weights can blend commensurate predictions without exact seam equality, while warning against interpolating incompatible ontologies. Audited Fable's strongest atlas claims, formulated a many-to-one alignment target, and limited “remember every model/domain” to finite-stage capacity or a hybrid expandable registry. Added claims E11–E14 and F27–F30 to the claim ledger.

- [x] **Task 5 — Fix the project’s target and non-goals.**

  Create `notes/project_spec.md`. Use Tasks 2–4 to turn the working thesis into explicit design requirements. Decide what “logic,” “fit onto an MLP,” “theory,” “domain,” and “handles indefinite succession” must mean for this paper. State non-goals, including any metaphysical thesis about truth the formalism does not need.

  Completed 2026-07-10. Created [`notes/project_spec.md`](notes/project_spec.md). Fixed the target as a finite-stage logic of scoped, defeasible model-use licenses rather than a new truth value. Defined the project meanings of logic, theory/model, domain, neural “fit,” and indefinite succession; made representability, learnability, semantic alignment, and open-ended implementation separate success grades; converted Tasks 2–4 into logical, neural, empirical, and interpretability design requirements; and stated strong non-goals concerning truth, scientific realism, policy–value uniqueness, neuron/proposition identifications, SGD, and infinite fixed-network capacity. Used the posts only to establish the motivational order—action and comparison before certainty, recursive evaluation, and value/policy reconstruction—not as evidence for factual claims.

- [x] **Task 6 — Audit related fields and create a verified bibliography.**

  Create `notes/literature_map.md` and `references.bib`. Research primary sources for belief revision/nonmonotonic logic, formal learning and truth approximation, scientific structuralism and theory reduction, preference/decision logic, selective prediction and abstention, mixture-of-experts/model routing, ReLU CPWL geometry, differentiable logic, inverse reinforcement learning/reward identifiability, and provability/GL where relevant. Verify every inherited citation before including it.

  Completed 2026-07-10. Created [`notes/literature_map.md`](notes/literature_map.md) and [`references.bib`](references.bib), using primary publisher, proceedings, journal, author, or archival records. Mapped the distinct contributions and limits of eleven neighboring fields; identified selective prediction as the closest formal precedent for fallback-induced thresholds and abstention; verified finite CPWL/ReLU representation and qualified tropical and Łukasiewicz correspondences; separated formal-learning convergence from truthlikeness; constrained the policy/value goal with modern reward-identifiability results; and rejected automatic transfer of Löb/GL results to empirical licenses. Audited the inherited numbered bibliography, corrected the Neural LP authors/title and several publication versions, corrected the Seidenfeld–Schervish–Kadane DOI, and omitted unneeded or insufficiently verified entries rather than carrying them forward. Updated claims C07, D01–D03, and F14/F16/F17 in [`notes/claim_ledger.md`](notes/claim_ledger.md) with scoped `S1` or `I1` dispositions.

- [x] **Task 7 — Choose the core formal objects and notation.**

  Create `formalism/01_signature.md`. Define the sorts for agents, stages, records, cases, domains, model/theory objects, predictions, losses, tolerances, costs, libraries, searches, and provenance. Resolve the point/domain distinction and specify whether a domain is a set, probability distribution, task family, or a typed object supporting more than one of these.

  Completed 2026-07-11. Created [`formalism/01_signature.md`](formalism/01_signature.md). Fixed a many-sorted, task-typed finite-stage signature covering agents, stages, budgets, tasks, cases/histories, predictions/outcomes/actions, theory frameworks, versioned models, frames, domains, losses, risk aggregators, tolerances, uncertainty specifications, fallbacks, costs, records, libraries, searches, provenance, selectors, and bridges. Resolved a domain as a typed evaluation scope supporting carrier-set, distribution/sampler, task-family, condition, frame, and provenance views while keeping loss and risk aggregation outside domain identity. Introduced `EvalSpec(D,L,rho)` to type risk and scalar/vector/partially ordered tolerances; distinguished point domains from domain guarantees; made records, libraries, and search scope finite and versioned; stated full license-request well-formedness; and excluded global truth/finality/completeness predicates from the base object language. Deferred truth conditions and update rules to Tasks 8–10.

- [x] **Task 8 — Define finite-stage license semantics.**

  Create `formalism/02_license_semantics.md`. Give a fully typed definition of a license such as `Lic(a,t,b; M,D,L,epsilon,alpha,cost,trace)`. Define empirical adequacy, calibrated adequacy, the closure/search clause, abstention, and the two defeat modes (new evidence and a newly retrieved dominator). Include small examples.

  Completed 2026-07-11. Created [`formalism/02_license_semantics.md`](formalism/02_license_semantics.md). Defined target, empirical, and certificate-relative adequacy; introduced valid typed certificate objects with distinct deterministic, frequentist, Bayesian, conformal/selective, vector, and empirical-only readings; and gave the full factored use-license semantics. Added four operational outcomes—granted, refused by a countercertificate, withheld for insufficient/unresolved evidence, and undefined for ill-typed requests—so failure to certify is not treated as certified failure. Required every full license to name an explicit fallback, formalized conservative fallback improvement, hard constraints, relative versus declared-library search closure, library-relative admissibility, provenance, active sets, selection, mandatory fallback on gaps, coverage/selective risk, evidence rebuttal versus evidential lapse, and defeat by a newly retrieved dominator. Included five examples and six elementary semantic consequences. Recorded open dominance/update questions for Tasks 9–10.

- [x] **Task 9 — Define consequence and update rules.**

  Create `formalism/03_consequence_update.md`. Specify what follows from a set of licenses, which object-level rules remain local/classical, how contradictions are quarantined by domains, how record heredity differs from belief monotonicity, and how revision changes licenses, domains, tolerances, and provenance.

  Completed 2026-07-11. Created [`formalism/03_consequence_update.md`](formalism/03_consequence_update.md). Separated model-local object consequence, monotone typed consequence at a fixed finite stage, and current nonmonotonic consequence derived from active licenses and admissible evidence. Defined labeled reliance rather than truth detachment; component, case-application, active-set, selection, and fallback rules; risk-specific scope transport; and contradiction quarantine across model/version/frame/task/domain/purpose/stage contexts. Established raw-record heredity alongside non-hereditary admissible views, certificates, licenses, and selections. Added dependency-directed, stratified update transactions for evidence, corrections, retractions, models/searches, domains, tolerances, certificate conventions, fallbacks, costs/purposes, expiry, provenance, branches, and merges. Included seven examples and seven elementary results covering status functionality, nonmonotonic current licenses, non-explosion, conservative persistence, tolerance transport, merge behavior, and dominator defeat. Deferred exact dominance and distribution-aware splitting to Task 10.

- [x] **Task 10 — Formalize dominance, Pareto retention, and domain splitting.**

  Create `formalism/04_dominance_retention.md`. Define scalar and multi-objective dominance over loss, coverage, cost, and robustness. Prove a first retention result: a globally superseded model may remain undominated on a subdomain or on the full resource vector. State exact conditions for split, retain, or revoke.

  Completed 2026-07-11. Created [`formalism/04_dominance_retention.md`](formalism/04_dominance_retention.md). Defined eligible model–gate–fallback use plans, typed comparison profiles, task risk, coverage deficit, resource cost, and robustness coordinates; explicit monotone scalar dominance; product-preorder Pareto dominance; mode-correct joint comparison certificates; pairwise comparison statuses; target, undefeated, and certified operational frontiers; and four distinct retention layers. Formalized whole-domain versus cell/local dominance, prespecified relation cells, distribution-aware child carriers, conditional measures/samplers, expected/worst-case/coverage reconstruction, split readiness, and exact retain, supersede, split/withhold, adequacy-revoke, and archive-removal conditions. Proved eight results, including two retention theorems showing that global risk supersession does not imply subdomain or full-resource supersession, a conditional split-retention theorem, and a countermodel to total revocation from partial dominance. Scoped and adjudicated inherited claims A05, E06, and E07.

- [x] **Task 11 — Formalize scientific atlases, charts, seams, and bridges.**

  Create `formalism/05_atlas.md`. Turn the distinctions from Task 4 into definitions for local model charts and compatibility on overlaps without assuming exact equality. Distinguish a router over models from a single CPWL predictor. Provide Newtonian/relativistic and simpler toy examples while avoiding the claim that approximate physical theories literally form a differential-geometric atlas unless the axioms support it.

  Completed 2026-07-11. Created [`formalism/05_atlas.md`](formalism/05_atlas.md). Defined the licensed model cover as the weakest object and a scientific licensed atlas as a finite cover plus typed chart, overlap, bridge, seam, dominance/frontier, router, fallback, and provenance records; reserved literal differential-atlas status for structures satisfying explicit manifold, open-chart, invertible-transition, regularity, and cocycle axioms. Formalized archive/hard/use/frontier chart views, active and generalized status cells, certified gaps versus unknown scope, thick overlaps versus routing seams, directional purpose-specific bridge kinds, compatibility ledgers, bridge obligations by operation, error composition and cycle defects, exact gluing, approximate blending, safe routing, atlas revision, and alignment among the scientific cover, router partition, and ReLU activation complex. Added temperature, overlapping-regressor, gap, same-domain, unresolved-overlap, and narrowly scoped Newtonian/relativistic kinetic-energy examples. Proved nine elementary results, including active-set decomposition, exact gluing, blend continuity/deviation and bridge-composition bounds, gap fallback, a hard-routing/ReLU discontinuity counterexample, non-bijective activation/chart alignment, a low-speed kinetic-energy error bound, and exact signed-margin active-set recovery versus argmax insufficiency. Updated atlas-related claim-ledger dispositions without adding a new falsification.

- [x] **Checkpoint A — Reassess the roadmap after the finite-stage logic and atlas foundations.**

  Create `notes/checkpoints/A_finite_stage_foundations.md` and apply the checkpoint protocol. In particular, determine whether Tasks 8–11 produced a coherent enough finite-stage object to justify the planned open-endedness, core-calculus, and metatheory tasks; identify missing countermodels or literature dependencies; and revise Task 12 onward before further formalization.

  Completed 2026-07-11. Created [`notes/checkpoints/A_finite_stage_foundations.md`](notes/checkpoints/A_finite_stage_foundations.md). Determined that Tasks 7–11 share a coherent typed finite-stage spine but do not yet form one publication-ready calculus. Identified a subtle interface ambiguity: Task 8's full `Lic` includes comparative non-domination, while the retention/atlas results distinguish continued adequacy, possible use, comparison status, current selection, and archival memory after supersession. Added Task 11A to compare alternative judgment factorizations, choose terminology only after testing them in one integrated finite witness, and ensure the chosen design represents both continued old-model use and mere historical retention without conflation. Narrowed Task 12 to continuation-based open-endedness rather than speculative Löb/anti-Löb analogy; narrowed Tasks 13–14 to a small core and genuine proof/countermodel audit; refocused the ML and experiment tasks on four-way status, component factors, active sets, calibration, fallback, comparison-driven status changes, external registry pointers, scaling, and semantic/non-neural alignment distinctions; and made policy/value work optional to the core. Updated [`notes/project_spec.md`](notes/project_spec.md), [`notes/claim_ledger.md`](notes/claim_ledger.md), and a stale Task 8 handoff in [`formalism/02_license_semantics.md`](formalism/02_license_semantics.md). No new claim was marked `X1`.

- [x] **Task 11A — Resolve the finite-stage license/comparison interface and build an integrated witness model.**

  Create `formalism/05a_integration.md`. Treat the relation among `CertAdeq`, pragmatic usability/reliance warrant, finite comparison status, preferred use, `SelectedNow`, and archival retention as an open design question. Compare at least: (A) layered basic warrant plus separate preference; (B) one parameterized `Lic_P` whose requirement profile optionally includes comparison; and (C) a strong preferred-use `Lic` plus a separately named adequacy/usability judgment. Decide the unqualified meaning of `Lic` only after evaluating semantic clarity, continued use of older models under another purpose/profile/subdomain, update behavior, normative interpretation, and neural target complexity. In every design distinguish `UndefeatedRelative` from `CertifiedUndominated` and specify how unknown comparisons behave. Then construct one finite end-to-end witness with at least three model/use plans, an explicit fallback, overlap and gap, simultaneous usable/adequate models, comparison and selection changes without automatic evidence/archive erasure, both continued old-model use and mere retention cases, all four operational statuses, lapse versus rebuttal, model-addition supersession, a successful and withheld split, multiple bridge statuses, and complete provenance. Record the selected design, rejected alternatives, inconsistencies found, and exact repairs Tasks 12–14 must inherit.

  Completed 2026-07-11. Created [`formalism/05a_integration.md`](formalism/05a_integration.md). Compared layered, parameterized-profile, and strong-license interfaces without assuming a winner, then selected mandatory profile-indexed licensing `Lic_P` because it subsumes the other designs as named profiles, supports a provisional literal-inclusion profile order, and lets selectors declare their required authorization level. Defined finite required/report-only atoms; `P_rely`, `P_pref-rel`, and `P_pref-cert`; four-way atom/profile assessment; mandatory profile references; relative-undefeated versus certified-undominated behavior under unknown comparisons; profile-local updates; selector-required profiles; and profile-indexed current/stability views. Built a four-plan, three-stage witness with explicit fallback, overlap, gap, all four statuses, simultaneous usability, continued old-model use on an edge subdomain, usable-but-unselected and archive-only retention, model-addition supersession, unknown comparison, successful and withheld splits, five bridge statuses, lapse, rebuttal, and complete provenance. Proved nine structural results and mapped repairs into Tasks 8–14. The later external audit repaired one comparison-scope certificate gap and clarified E05: universal closure is a superseded design default (`D1`), while the narrower claim that closure is forced is falsified (`X1`); the profile-indexed replacement and project impact remain supported.

- [x] **Unscheduled Checkpoint A1 — Adjudicate the Fable 5 external audit.**

  Read [`llm_convos/claude_audit_2026-07-11.md`](llm_convos/claude_audit_2026-07-11.md) as an independent audit of Tasks 0–11A and apply the checkpoint protocol without beginning the next formal task. Verify each correction against the source files and primary literature; repair accepted local defects; record rejected or deferred recommendations; and revise the pending roadmap where the theorem deficit, executable-semantics risk, literature gaps, motivation debt, or corpus-management risks warrant a change.

  Completed 2026-07-11 and amended 2026-07-12. Created and extended [`notes/checkpoints/A1_external_audit_response.md`](notes/checkpoints/A1_external_audit_response.md). The first pass accepted and repaired C1–C10 with one bibliographic correction to the audit itself; introduced explicit world/stage semantics, substantive versus stage-bound request fields, typed action-authorizing roles, overlap-scope witness certificates, transparent joint-score certificates, `D1` design dispositions, and top-of-file Task 11A interface notices. It corrected F14's attribution and added Tasks 11B, 12A, and 22A. The second pass converted the theorem-light criticism into a paper-carrying theorem spine, reduced the planned mathematical core from 28 nominal sorts to three principal carriers plus semantic indices, replaced flat reason codes with indexed witnesses over a `WF + K_3` kernel, added Task 14A for transport/routing bounds, and strengthened Tasks 11B–19. At checkpoint completion Task 11B was next; it is now complete.

- [x] **Task 11B — Mechanize and test the integrated finite witness.**

  Create a small standard-library Python reference implementation under `verification/` plus tests and a reproducible command. Implement the compact kernel rather than one class per Task 7 sort: use plans `E`, evaluation contexts `Q`, finite epistemic states `S`, finite profiles, a separate `WF` check, meaningful atom values `K_3={refuted,open,supported}`, finite-meet aggregation, and lossless indexed diagnostics containing support/counterwitnesses, obstacles, and provenance. Derive the four public outcomes from `WF + K_3`; do not create a closed `ReasonCode` enum. Encode the three-stage Task 11A witness as fixtures over this kernel, including comparison eligibility on the exact evaluation scope, profile-local update, lapse (`+ -> ?`) versus rebuttal (`+ -> -`), selectors, and provenance links. Assert every table and transition in `formalism/05a_integration.md`, including the legacy-label rendering and the difference between marginal score intervals and tighter joint certificates. Test that well-formed atoms never return `Undefined`, empty active sets are selector-level outcomes rather than atom reasons, and safety/provenance projections are lossless. Add a lightweight repository check for broken local Markdown links and run both checks in a minimal GitHub Actions workflow. This is semantic verification infrastructure, not the neural experiment or proof-assistant formalization.

  Completed 2026-07-12. Added the standard-library [`verification/`](verification/) reference implementation: [`kernel.py`](verification/kernel.py) separates `WF` from meaningful `K_3` atoms and derives all four public outcomes, while [`witness.py`](verification/witness.py) encodes the complete three-stage Task 11A structure without a closed reason-code type. Added 28 executable assertions covering the witness tables, exact-scope eligibility, profile-local comparison updates, routing and retention distinctions, unknown comparisons, split and bridge cases, marginal versus joint certificates, lapse versus rebuttal, selector-level empty active sets, safety projections, and append-only lossless provenance. Added a local Markdown link checker, one-command instructions in [`verification/README.md`](verification/README.md), and the minimal [verification workflow](.github/workflows/verify.yml). `python -m verification` passes. No neural experiment, proof-assistant claim, or new claim-ledger disposition was introduced.

- [x] **Task 12 — Analyze open-endedness and non-finality.**

  Create `formalism/06_open_endedness.md`. Starting from Task 11A's profile-indexed interface and the Task 11B compact executable reference, define stage/refinement DAGs over world/stage pairs, compatible continuations, live alternatives, current `Lic_P` grant, eventual profile-indexed stability, known/certified stability, semantic finality, and optional meta-level truth. Hold `(e,q,P)` fixed when asserting stability; changing one creates a new substantive question. Prove or sharply refute a **stability trichotomy**: (i) deterministic proof-backed atoms can be internally certified stable when every allowed continuation freezes their premises and proof-validity rules; (ii) statistical atoms separated from their tolerance boundary can stabilize under explicit convergence/simultaneous-coverage assumptions while finite-prefix indistinguishability prevents a zero-error announcement of arrival in a rich family; and (iii) open-library comparison atoms cannot receive a sound permanent-stability certificate when every stage admits a history-preserving `AddModel` continuation with a validly evaluated dominator. Also give countermodels showing that extendability permits eventual stabilization and endless change and that different profiles can behave differently. Treat absence of `Final` from the base language as syntactic non-expressibility, not a substantive theorem. Include Löb/GL only if a genuine provability translation with derivability/fixed-point conditions is constructed; otherwise record a concise rejection, and do not use “anti-Löbian” as a theorem name.

  Completed 2026-07-12. Created [`formalism/06_open_endedness.md`](formalism/06_open_endedness.md). Defined compatible refinement DAGs over finite world/stage pairs, fixed queries `(e,q,P)`, stage indistinguishability, live alternatives, current grant, pathwise eventual stability, permanent current stability, scheme-relative certified stability, semantic finality, and optional target truth. Proved a finite-prefix non-certifiability theorem, deterministic freeze theorem, margin-separated statistical stabilization theorem, zero-error finite-announcement impossibility theorem, finite-profile lifting result, and directional open-library dominator theorem. Added countermodels separating stabilization, known arrival, endless change, profile dynamics, and finality. Sharply refuted the polarity-unrestricted comparison-instability target: a persistent dominator can make refutation stably certifiable, while currently supported non-domination remains non-final under valid dominator extensions. Updated [`notes/claim_ledger.md`](notes/claim_ledger.md) with the scoped replacement and full project impact, superseded the unsupported Löb framing, and retained `Final`, `Complete`, and `True` only in the metalanguage. No new literature claims were imported in Task 12; the now-completed Task 12A supplied primary-source positioning.

- [x] **Task 12A — Fill the core-related literature gaps before freezing the calculus.**

  Create `notes/literature_core_supplement.md` and update `references.bib`, `notes/literature_map.md`, and affected ledger rows using verified primary sources. Audit input/output logic for output-producing rather than truth-detaching consequence; prioritized reasons/defaults; justification and labelled deductive logics for explicit evidence/provenance terms; awareness/unawareness logics for library versus conceivable alternatives; strong-Kleene and logic-of-partial-functions precedents for meaningful `K_3` aggregation, with Bochvar-style infectious undefinedness treated as a comparison to the superseded four-chain presentation; conformal prediction's primary sources; and high-confidence/safe policy improvement over a fallback. Determine exact structural similarities and mismatches without importing representation, completeness, or soundness theorems whose hypotheses are absent. Treat the Fable audit's L1–L5 list as search leads, not verified authority.

  Completed 2026-07-12. Created [`notes/literature_core_supplement.md`](notes/literature_core_supplement.md) and verified fifteen primary sources spanning input/output logic, prioritized defaults/reasons, justification and labelled deduction, awareness/unawareness, Strong-Kleene and partial-function logic, conformal prediction, and safe baseline policy improvement. Added their checked metadata to [`references.bib`](references.bib), integrated the results into [`notes/literature_map.md`](notes/literature_map.md), and updated `A08`, `E02`, `E09`, `E10`, and new algebraic row `E16` in [`notes/claim_ledger.md`](notes/claim_ledger.md). Established one direct import—the Strong-Kleene finite-meet algebra after explicit relabeling—and classified every other connection as structural or an elaboration template requiring a hypothesis-preserving translation. Kept empirical evidence terms non-factive, separated task tolerance from confidence and conformal miscoverage, treated Bochvar infection only as a comparison to the superseded four-chain, and found no new falsified inherited claim. Task 13 may now freeze the core without silently inheriting neighboring soundness, completeness, coverage, or safety theorems.

- [ ] **Task 13 — Select the smallest publishable logic and state its metatheory goals.**

  Create `formalism/07_core_calculus.md`. Consolidate Tasks 7–12A into a compact mathematical calculus rather than reproducing the typed implementation inventory. Target three principal carriers: evaluated use plans `E`, reliance/evaluation contexts `Q`, and finite epistemic states `(S,->)`, with target worlds `W` as a semantic index and profiles as finite families of parameterized requirement schemata. Package cases, domains, losses, risk posets/acceptable sets, task interfaces, and frames as dependent data of `q`; package record, library/evaluated set, budget, search, certificate support, dependency, and abstract provenance as data of `s`. Treat theory frameworks, exhaustive event/reason taxonomies, full provenance DAGs, bridges, Pareto/splitting machinery, and policy/value work as elaborations or extensions. Use a compact request `(s,e,q,P)` and prove or countermodel that `e,q,s,P` are independently indispensable.

  Canonical assessment is two-phase: `WF(P,e,q,s)` handles type/denotation/executability and yields `Undefined` on failure; every well-formed required atom has value in `K_3={refuted,open,supported}`, aggregated by meet to yield `Refused`, `Withheld`, or `Granted`. Define `Diag(r)` through atom identity, positive/counterwitness, obstacle, and provenance; flat names such as `HardRiskViolation` are renderings, not primitive constructors, and `NoLicensedModel` is derived from an empty active set. Define safety projections without a global reason enum. Separate profile shape from atom parameters, define typed atom entailment/refinement (including tolerance, fallback margin, constraints, trace, and certified-to-relative comparison), and lift it to a profile preorder. Give syntax, `<W,S>` semantics, consequence rules, update dynamics, a typed-elaboration map back to the detailed records, a central glossary, and a theorem-dependency/novelty table distinguishing definitions, standard lemmas, new characterizations, impossibility results, countermodels, and conjectures.

- [ ] **Task 14 — Prove or refute the core calculus results.**

  Create `formalism/08_metatheory.md`. Prove or refute the actual compact core against the Task 13 `<W,S>` semantics, revising the calculus when necessary. The paper-carrying targets are: (1) **robust update persistence**, seeking necessity and sufficiency for grant/diagnostic invariance over an update class via dependency-complete impact cones plus an explicit path-realizability condition, with a countertheorem showing why path absence is only sufficient without realizability; (2) **profile refinement soundness and relative completeness**, proving semantic antitonicity and constructing a finite separating countermodel for missing syntactic entailments in an independent-atom fragment; and (3) **minimal diagnostic representation**, characterizing the quotient of meaningful atom-state vectors that answers every supported profile query and deriving a `3^n` distinguishable-state / `n log_2(3)`-bit lower bound for well-formed requests when singleton profiles are available, plus a separate channel for `WF` failure and its derivation. Also settle the `WF + K_3` status normal form, algebra, four-outcome minimality, safety projection, typed elaboration invariance, mode-scoped soundness, labeled non-explosion, tolerance monotonicity, safe fallback on gaps, raw heredity without current-status monotonicity, comparative defeat by profile, failure of unrestricted rational monotony, and failure of global closure from finite search. Treat KLM premise postulates only as structural comparisons because nonmonotonicity primarily lives in state transitions. Label definitional consequences and standard algebra separately; they do not satisfy the theorem contribution by themselves. Every refutation must update the claim ledger with project impact.

- [ ] **Task 14A — Prove the domain-transport and routed-cover bounds.**

  Create `formalism/08a_transport_routing.md`. Build a second, cross-layer theorem cluster rather than adding more record definitions. At minimum prove: (1) for nonnegative integrable loss on a probability space, every positive-measure subdomain has conditional expected loss at most `epsilon` iff the loss is at most `epsilon` almost surely, exactly characterizing when expected-risk adequacy restricts freely; (2) a hard-router expected-risk bound decomposing correct-cell local risks plus an explicit misrouting/fallback penalty under bounded loss; and (3) a Lipschitz bridge/blending bound translating prediction disagreement into excess task risk. State measurability, boundedness, coverage, and selection assumptions exactly, and give counterexamples when they fail. Optionally prove the group-valued bridge cocycle characterization—global frame potentials exist iff cycle products are identity—only if it remains concise and relevant. Classify these as extension theorems, but use them to connect the abstract license calculus to the later neural router.

- [ ] **Checkpoint B — Reassess the roadmap after the core calculus and metatheory.**

  Create `notes/checkpoints/B_core_metatheory.md` after Tasks 14 and 14A and apply the checkpoint protocol. Decide whether the proved, refuted, or weakened theorem spine supports the proposed ReLU correspondence; identify which formal objects and theorems actually need neural representation; and revise Task 15 onward so the ML work targets the surviving calculus rather than the earlier aspirations. Require an explicit tally of paper-carrying characterizations/impossibility results versus definitions and standard lemmas; if the core remains theorem-light, add a focused proof repair before ML work.

- [ ] **Task 15 — Specify operational encodings for cases, domains, and models.**

  Create `ml/01_encodings.md`. Encode the surviving core before optional extensions. Specify which request/model/domain/evidence fields are explicit inputs, fixed context, missingness/status indicators, learned embeddings, external registry/provenance pointers, or forbidden compression targets. Compare a fixed finite model-indexed baseline with a shared candidate scorer over a variable library; analyze sparse/on-demand pair comparisons versus quadratic dominance/bridge matrices. Use record-derived loss profiles and learned factorization as main options, with dimensionless log or perturbative physics coordinates only as optional case-specific features. State identifiability/equivalence classes and interpretation tests; do not treat latent coordinates as ontology.

- [ ] **Task 16 — Derive the ReLU license architecture.**

  Create `ml/02_relu_architecture.md`. Define a basic ReLU reference architecture with candidatewise predicted risk/certificate-validity heads, signed hard/fallback/constraint/comparison margins, paired or exposed negative channels, multi-label usable/licensed sets, comparison and selection outputs, routing, and explicit fallback/abstention. Supervise meaningful atom state/margins and derive the top-level four outcomes symbolically through `WF + K_3`; do not train an independent aggregate-status head that can contradict its components. Do not add a flat reason-code classifier: reason displays derive from atom address, polarity, witness/obstacle metadata, and provenance pointers. Preserve `Diag`, safety/open-safety projections, registry references, and missingness outside any scalar margin. Compare separate atom heads with a parameterized profile head rather than assuming factorization in advance. Provide both a fixed finite-library MLP baseline and a shared scorer coupled to expandable external memory. Treat nested model-building choices, full bridge matrices, and mixtures as optional extensions.

- [ ] **Task 17 — State and verify the ReLU/atlas representation results.**

  Create `ml/03_representation_theorems.md`. Prove the required finite constructions or cite precise primary CPWL/ReLU theorems with architecture conventions. Give a positive construction: if finitely many atom margins are CPWL, a finite ReLU network computes them and a fixed external threshold/`WF + K_3` decoder exactly recovers supported profile queries; state size/depth and boundary conventions. Prove the **hard-routing seam characterization** on a finite polyhedral complex: a piecewise affine/CPWL expert assembly is continuous iff adjacent expert traces agree on every common face; seam agreement yields a continuous CPWL map and exact finite ReLU representation, while a seam mismatch forbids exact representation by one ordinary continuous ReLU output. Connect the Task 14 minimal-diagnostic quotient to what outputs must be preserved, and settle fixed finite versus expandable libraries plus external argmax. Keep scientific-cover, router-partition, and activation-complex alignment as a separate empirical claim.

- [ ] **Task 18 — Decide the training objective.**

  Create `ml/04_losses.md`. Analyze risk/log-loss regression, positive/countercertificate prediction, open/missingness obstacles, binary or multi-label atom objectives, derived four-way status, hinge/ranking losses for comparison/selection, calibration/selective-risk objectives, explicit reject options, and plain softmax multiclass cross-entropy. Choose one structured primary objective and one deliberately simpler comparison baseline. The primary objective must supervise atom identity/state and any learnable witness/obstacle features, then compute `Granted/Refused/Withheld/Undefined` symbolically through `WF + K_3`; an independently learned aggregate or flat reason classifier may appear only as an ablation. Explain simultaneous/empty usable sets, comparison-driven changes without conflating them with evidence failure, and risk–coverage calibration.

- [ ] **Checkpoint C — Reassess the roadmap after the neural representation and objective.**

  Create `notes/checkpoints/C_neural_blueprint.md` and apply the checkpoint protocol. Check that the proposed encodings, ReLU architecture, representation results, and training objective form one implementable and falsifiable system; revise the experiment, interpretability, and paper tasks from Task 19 onward; and add any necessary baseline, calibration, capacity, or impossibility work before implementation begins.

- [ ] **Task 19 — Design the decisive toy experiment.**

  Create `experiments/01_design.md`. Specify a synthetic theory-succession generator whose domains and target semantics are fixed independently of the trained network. Generate compact atom states and witness/obstacle families rather than an expanding flat reason-label vocabulary. Include external and fallback-induced thresholds, several simultaneously adequate/usable models, a certified gap, unknown applicability, all four derived outcomes, costs/coverage, later evidence causing lapse versus refusal, and a later-added model that changes comparison/selection while distinguishing continued use, nonselection, and archival retention. Include exact/approximate/incompatible or unknown overlaps and at least one failed split or distribution-shift case. Define datasets, splits, metrics, ablations, expected plots, falsification criteria, and seeds. Measure atom/diagnostic fidelity, active-set routing, calibration, risk–coverage, update/retention, and activation/domain alignment separately.

- [ ] **Task 20 — Implement the experiment.**

  Add a small, readable implementation under `experiments/` with configuration, tests, and a reproducible entry point. Implement only the Checkpoint C blueprint. Include the basic ReLU MLP, structured atom objective, `WF + K_3` symbolic decoder, indexed witness/obstacle diagnostics without a closed reason enum, comparison baselines, simultaneous/empty usable sets, comparison/selection routing, fallback/abstention, signed and rectified margins, registry identifiers, machine-readable update traces, and activation-region inspection.

- [ ] **Task 21 — Run and analyze the experiment.**

  Create `experiments/02_results.md` plus machine-readable results and figures. Report component-risk, atom-state, witness/obstacle, and derived-status calibration; confusion among refuted/open/WF-failure cases; multi-label usable-set fidelity; gap/unknown handling; risk–coverage and fallback cost; comparison/selection routing; model-addition supersession; old-model continued-use versus archive-only outcomes; tolerance monotonicity; subdomain retention; activation/domain alignment; and distribution-shift/identifiability failures. Keep functional fit, calibration, semantic alignment, and interpretability conclusions separate.

- [ ] **Task 22 — Audit the policy–value and recursive-judgment claims.**

  Create `notes/policy_value_judgment.md`. Replace “isomorphism” with the strongest defensible result. Cover reward non-identifiability, occupancy measures, environment dependence, rationalization of policies, recursive evaluation, and conditions under which judgment reveals stable structure. Explicitly decide whether each surviving claim belongs in the formal paper, only the motivating/Substack post, a companion case-study section, or future work. This task is not a dependency of the core calculus.

- [ ] **Task 22A — Prove, refute, or demote the recursive-judgment information claim.**

  Create `formalism/09_judgment_information.md`. Give B01 a precise latent-task prediction model and determine whether above-baseline calibrated transfer judgment entails nonzero mutual information about task structure under explicit non-leakage and identifiability assumptions. Prove the strongest valid information lower bound or construct a countermodel and update B01 with project impact. Use the result to decide whether recursive judgment can remain in the formal paper's motivational contract or must be confined to the Substack post/future work. Keep this result independent of the validity of the core license calculus.

- [ ] **Task 23 — Design the policy-to-value interpretability bridge.**

  Create `notes/policy_value_interpretability.md` only at the strength surviving Task 22. Use `policy_value_isomorph` as a conditional companion case study, not evidence for universal policy–value equivalence. Specify how a reconstructed `V` or `Q` could feed the Task 11A-selected license/comparison interface and expose domains, margins, local rules, transitions, abstentions, and traces. Separate behavioral/value fidelity, domain validity, representational alignment, causal faithfulness, and human inspectability. Propose probes, shared/independent encoder comparisons, counterfactual rankings, interventions/ablations, shift coverage, and readability tests; allocate each test to this repository, the companion repository, or future work.

- [ ] **Task 24 — Build the counterexample and limitations section.**

  Create `notes/limitations.md`. Include underdetermination, arbitrary/scaled rewards and losses, policy/environment/return dependence, basic-warrant versus preferred-use ambiguity, certificate-mode mismatch, unknown and incomparable models, pairwise comparison/bridge scaling, rectification information loss, hard-routing discontinuity, surrogate-without-mechanism, adversarial routing, catastrophic forgetting, unsupported domains, ontology shifts, nonstationarity, atlas-metaphor limits, semantic misalignment of linear regions, and cases where usefulness diverges from truth. Link every falsified/limited claim to its project-impact analysis.

- [ ] **Task 25 — Freeze the paper’s claims and outline.**

  Create `paper_outline.md`. Select only claims supported by completed proofs, verified literature, or experiment results. Freeze a **core contribution set** separately from formal extensions, empirical results, optional policy/value case study, and interpretive motivation. Put the three opening derivation questions near the start and any surviving interpretability bridge after the neural/experimental results. Write a section-level outline with explicit word budgets, theorem/evidence dependency map, notation table cross-checked against the Task 13 glossary, countermodel map, explicit contribution list, and cut list.

- [ ] **Checkpoint D — Reassess the roadmap before drafting the public artifacts.**

  Create `notes/checkpoints/D_predraft.md` and apply the checkpoint protocol. Audit whether the formal, neural, experimental, policy/value, counterexample, and interpretability results support a coherent paper of the intended scope. Revise Task 26 onward, including the paper structure and any missing proof/experiment repair tasks, before prose drafting begins. Treat the frozen claim set as a proposed publication contract, not an obligation to preserve unsupported ambitions.

- [ ] **Task 26 — Draft the formal paper’s motivation and related work.**

  Begin `paper.md` with title, abstract, introduction, the derivation and limits of `Pi(M,D,epsilon)`, the Task 11A judgment design and rejected alternatives, the representation question, licensed model covers versus ReLU activation complexes, motivating examples, contributions, scope, and related work. Preserve whatever distinctions Task 11A shows are necessary among truth, adequacy/usability, finite relative comparison, current use/selection, and retention without pretending the terminology was forced from the outset.

- [ ] **Task 27 — Draft the formal definitions and semantics sections.**

  Extend `paper.md` with the compact `E,Q,S` signature, semantic world index, finite profiles, `WF + K_3` assessment, indexed diagnostics, consequence/update rules, comparison/use relationship, and open-ended stage semantics. Explain the elaboration into detailed typed records in an appendix or compact implementation section. Present Pareto retention, splitting, and licensed-atlas/bridge machinery explicitly as extensions rather than silently enlarging the core.

- [ ] **Task 28 — Draft the theorem and proof sections.**

  Extend `paper.md` with only the settled theorem spine and representation results, including countermodels where stronger desired claims fail. Organize the section around characterizations, impossibility results, quantitative bounds, and exact representation conditions; label imported standard lemmas and definitional corollaries honestly and move them to appendices when they obscure the paper-carrying results.

- [ ] **Task 29 — Draft the neural representation, learning, and interpretability sections.**

  Extend `paper.md` with the minimal-diagnostic quotient, information-preserving/lossy maps, atom-state/margin outputs, symbolic status decoder, external registry and scaling assumptions, ReLU architecture, seam characterization and hard-routing limits, semantic alignment metrics, objective choice, transparency criteria, and exact limitations. Include the policy/value companion case only at the evidence grade and scope frozen by Tasks 22–25.

- [ ] **Task 30 — Draft the experiment, discussion, and conclusion.**

  Complete the substantive draft of `paper.md` with results, ablations, four-way/status and risk–coverage failures, update/retention behavior, alignment results, philosophical interpretation, interpretability implications, limitations, future work, and conclusion. Do not let synthetic success imply scientific realism or mechanistic transparency.

- [ ] **Task 31 — Perform the mathematical and citation audit.**

  Check every symbol, definition, theorem dependency, proof, numerical claim, and citation. Verify the compact/elaborated signature map, ensure no flat reason taxonomy or implementation record is presented as primitive without necessity, and classify each formal result as definitional, standard, new characterization, impossibility/countertheorem, quantitative bound, or conjecture. Confirm that at least three paper-carrying results from distinct theorem clusters survive. Ensure every technical claim is supported by a primary source or by a proof/experiment in the repository. Add an authoritative source for any retained physical context/formulas. Update the claim ledger with final dispositions and verify that every `X1`/refutation includes project-impact propagation into the paper, roadmap, and Substack claims.

- [ ] **Checkpoint E — Reassess publication readiness after the full audit.**

  Create `notes/checkpoints/E_publication_readiness.md` and apply the checkpoint protocol. Decide whether any audited failure requires returning to proof, experiment, interpretation, or drafting work; revise Task 32 onward and add narrowly scoped repair tasks if needed. Proceed to Gist/Substack formatting only if the surviving claim set is mutually consistent and supported.

- [ ] **Task 32 — Make `paper.md` Gist-compatible and publication-ready.**

  Verify GitHub Markdown and math delimiters, links, references, figures, Unicode, heading structure, and copy/paste behavior. Remove repository-only scaffolding from the public artifact.

- [ ] **Task 33 — Produce the Substack adaptation.**

  Create `substack_post.txt` from the audited paper. Use plain prose, Unicode where helpful, very few display equations, no Markdown formatting, and concrete examples. Retain the three opening motivations and all necessary caveats without introducing claims absent from the paper.

- [ ] **Task 34 — Cross-check and finalize both artifacts.**

  Compare `paper.md` and `substack_post.txt` claim by claim, proofread both, verify required formats, ensure the repository resume instructions are current, and record the final completion note here.

## Decision log

- **2026-07-10 — Loss-first rather than vectors-first.** The current preferred neural route derives adequacy targets from observed or simulated loss, then learns embeddings that predict that loss. Hand-labeled capability/demand vectors remain allowed as an interpretable baseline, not as evidence of discovery.
- **2026-07-10 — “License” is provisional terminology.** It usefully emphasizes defeasibility and scope, but Task 5 may rename the calculus if the term conflicts with established usage.
- **2026-07-10 — No commitment to cross-entropy yet.** Cross-entropy remains a requested baseline. The semantics may require multi-label or selective objectives, so Task 18 owns the final choice.
- **2026-07-10 — No commitment that usefulness equals truth.** The project studies bounded, revisable warrants. Any stronger metaphysical conclusion must be separately argued.
- **2026-07-10 — `Pi(M,D,epsilon)` is a derived compression, not an unexplained primitive.** `M` and `D` come directly from domain-sensitive theory succession; loss and `epsilon` enter when pragmatic comparison is turned into an operational reliance threshold. The loss, confidence, purpose, agent, and stage indices may be suppressed only after they are fixed.
- **2026-07-10 — ReLU is a gate and positive margin, not the whole information state.** The signed preactivation records degree of adequacy or inadequacy; rectification licenses the positive branch and deliberately collapses all nonpositive scores to zero.
- **2026-07-10 — Keep two atlas notions separate.** The intrinsic polyhedral atlas of a ReLU function is a structural representation result. A scientific-model atlas additionally requires model identity, domain licensing, routing, approximate bridge conditions, and possibly gaps. Alignment between them is a central theorem/experiment target.
- **2026-07-10 — Policy-to-value reconstruction is environment- and return-relative.** The companion repository correctly reconstructs `V^pi`/`Q^pi` using game dynamics, terminal utilities, perspective conventions, and sampled states. The general target is therefore reconstruction from a policy coupled to this background structure, not from network weights or action outputs alone.
- **2026-07-10 — Behavioral reconstruction is the first interpretability grade, not the last.** Independent value regression can explain decisions extensionally while missing the policy's internal mechanism. Claims of transparency must report behavioral fidelity, domain validity, internal alignment, causal faithfulness, and human inspectability separately.
- **2026-07-10 — The companion implementation is a case study, not yet a shared architecture.** Its current MLPs use `tanh` and separate raw-state encoders; this project studies a ReLU license calculus. Task 23 will design principled cross-project tests before proposing architectural changes to the companion repository.
- **2026-07-10 — Falsifiability precedes truth-likelihood labels.** Task 1 classifies how a claim could be tested, proved, or refuted and whether it is currently operational enough to do so. “Likely false” or “refuted” requires verified prior research on a sufficiently similar claim or a project-supplied proof, countermodel, counterexample, or experiment. Positive and negative claims use the same evidential standard.
- **2026-07-10 — `epsilon` has two principal sources.** A tolerance may be externally imposed by safety, precision, law, or task requirements, or endogenously induced by a fallback/status quo: `epsilon_B(D)=J(B,D)-Delta`. These sources can coexist and must not be conflated.
- **2026-07-10 — Separate adequacy, improvement, and admissibility.** A candidate can beat the fallback while remaining unsafe, or meet a hard adequacy threshold without being worth its cost. Comparative “best known” status is a third, library-relative condition. The provisional full `Pi` is their factored conjunction, not a primitive scalar test.
- **2026-07-10 — Preserve the zero boundary explicitly.** Inclusive adequacy uses signed margin `s>=0`, whereas `ReLU(s)>0` implements a strict inequality and maps equality together with failure to zero. The provisional recommendation is to retain the signed score for the formal comparison and use ReLU only to propagate positive slack.
- **2026-07-10 — Structured semantics precede vectorization.** `Pi` begins as a typed record whose model, domain, loss, tolerance, evidence, fallback, library, and provenance fields need not share a semantic type. Neural encoders may compress these fields, but the project must state which target each encoding is sufficient for.
- **2026-07-10 — Preserve component and signed margins.** A combined minimum can implement conjunctive licensing but loses failure identity; ReLU loses all nonpositive magnitudes. The preferred transparency interface retains `(s_hard,s_base,s_library,...)` and either the signed preactivations or paired channels `(ReLU(s),ReLU(-s))`, while routing content only through licensed positive channels.
- **2026-07-10 — Loss-derived embeddings identify competence profiles, not unique ontology.** Bilinear and neural encodings admit basis transformations and observational equivalence classes. Coordinate-level semantic claims require constraints, probes, stability tests, or causal interventions beyond held-out loss prediction.
- **2026-07-10 — Domain encodings are risk-relative.** A vector sufficient for expected risk can discard tails or geometry required for worst-case and safety claims. The domain representation must be evaluated against the exact risk functional it supports.
- **2026-07-10 — Scientific domains form an overlapping partial cover, not necessarily disjoint tiles.** Multiple models may be simultaneously licensed on a large overlap, may share the same domain, or may leave uncovered gaps. Active-set cells record exactly which model subset is licensed without forcing a single winner.
- **2026-07-10 — Separate three atlas-like geometries.** The scientific licensed cover stores model-indexed domains and evidence; a ReLU network has an intrinsic activation complex of affine restrictions; a router induces a selection partition. Alignment may be many-to-one and must be proved or tested.
- **2026-07-10 — Bridges are typed relations, not universally exact seams.** Scientific overlaps may support exact, approximate, statistical, decision-equivalent, asymptotic, translated, or unresolved bridges. Continuous blending does not require exact equality when outputs are commensurate, but numerical smoothness does not justify mixing incompatible ontologies.
- **2026-07-10 — Retention is broader than selection.** A lower-error model can be selected while the older adequate model and its domain remain stored for fallback, comparison, interpretation, changed tolerances, or future revision.
- **2026-07-10 — Open-ended atlases require expandable memory.** A fixed finite ReLU MLP represents only a finite-stage library. The provisional open-ended implementation is a sequence of finite scorers/routers coupled to an external or expandable model/domain/evidence registry.
- **2026-07-10 — The target is a license logic, not a replacement truth semantics.** The central judgment is a finite-stage, evidence-relative permission to rely on an instantiated model for a typed domain and purpose. The formalism remains neutral on whether truth exists or whether usefulness constitutes truth.
- **2026-07-10 — “Logic” carries a minimum formal burden.** The proposal must define a typed language, semantics, consequence, update/defeat rules, metatheoretic results, and a neural correspondence. A loss function or score by itself is not enough.
- **2026-07-10 — Neural fit has four grades.** Representability, empirical learnability, semantic/interpretive alignment, and open-ended implementation are separate claims and must be reported separately.
- **2026-07-10 — Indefinite succession means extendable finite stages.** Every finite record/library may be revised or extended without an internal finality rule. The project does not require a fixed network to store an actual infinity or require every revision sequence to converge.
- **2026-07-10 — The posts determine motivation, not warrant.** Their recurring progression from action/value before certainty through recursive evaluation to recovered structure and policy/value reconstruction will guide exposition. Public technical claims still require definitions, proofs, experiments, or verified literature.
- **2026-07-10 — The project is a synthesis across fields, not an instance of one existing logic.** Nonmonotonic logic supplies defeasible consequence; selective prediction supplies abstention/risk–coverage; MoE supplies routing; CPWL theory supplies finite ReLU representation; formal learning supplies convergence without known arrival; intertheory work supplies bridge distinctions; and IRL supplies identifiability limits. None supplies the complete license calculus.
- **2026-07-10 — Selective prediction is the main precedent for fallback-induced `epsilon`.** Reject/deferral costs can induce an operational acceptance threshold and require reporting risk jointly with coverage. The license system must extend this with multiple simultaneous models, retention, provenance, and domain bridges.
- **2026-07-10 — Truthlikeness and adequacy remain different projects.** Formal truthlikeness compares theories relative to a truth target or world similarity. The proposed license can compare task performance without assuming that the truth is in the library or that loss measures truth distance.
- **2026-07-10 — GL is conditional, not foundational.** Löb and Solovay results apply to formal provability under strong derivability/self-reference assumptions. A finite-stage empirical license modality is not a provability predicate unless a later formal translation proves that it is.
- **2026-07-10 — ReLU representation claims are finite and typed.** Exact CPWL representation is supported under explicit scalar/vector, domain, architecture, and layer-count conventions. It does not imply SGD learnability, semantic atlas alignment, efficient size, or open-ended storage.
- **2026-07-10 — Reward/value recovery is only partial without extra structure.** Policy behavior generally identifies equivalence classes rather than a unique reward/value or mechanism. Additional environments, discounts, state information, assumptions, and causal tests may narrow the class; behavioral agreement alone remains the weakest transparency grade.
- **2026-07-11 — The core signature is many-sorted and task-typed.** Cases, predictions, outcomes, and actions are dependent on a task; a shared neural vector does not erase those semantic types.
- **2026-07-11 — A domain is a typed evaluation scope with multiple views.** Its carrier set, optional measure/sampler, task family, contextual conditions, frame, coverage evidence, and provenance remain distinguishable. A risk specification declares which views it requires.
- **2026-07-11 — `EvalSpec(D,L,rho)` types risk and tolerance.** Loss is pointwise; `rho` aggregates it over declared domain views. `epsilon` lives in the resulting preordered risk space, allowing scalar, vector, interval, or Pareto thresholds without overloading domain identity.
- **2026-07-11 — Model identity is intensional and versioned.** Two models may be behaviorally equivalent on a domain while remaining different entries because their theory references, frames, derivations, costs, robustness, or provenance differ.
- **2026-07-11 — Records retain corrections rather than overwriting history.** A finite stage record is a versioned event structure; corrections/retractions change admissible evidence views while preserving an audit trail. Record heredity still does not imply license monotonicity.
- **2026-07-11 — Library and search closure are finite and relative.** A stage-local library is not the model universe. Search traces must state scanned/retrieved/evaluated sets, budgets, stopping reasons, and failures before supporting a no-recorded-dominator claim.
- **2026-07-11 — The base object language has no global truth or finality predicate.** Model-local satisfaction is allowed, while `TrueTheory`, `Final`, `Complete`, or `BestPossible` require separately defined meta-level semantics in later tasks.
- **2026-07-11 — Phase checkpoints are first-class work items.** Checkpoints occur after the finite-stage foundations, core metatheory, neural blueprint, claim/outline freeze, and final audit. Each consumes one prompt, reviews all remaining work prospectively, may restructure the unfinished roadmap, records its rationale in `notes/checkpoints/`, and stops before executing the revised next task.
- **2026-07-11 — Finite-stage assessment has four operational outcomes.** A request is granted, refused by valid contrary evidence, withheld because evidence/search/comparison is insufficient, or undefined because it is ill-typed/non-executable. Only grant makes `Lic` obtain; the other outcomes must not collapse into “false theory.”
- **2026-07-11 — Target, empirical, and certified adequacy are separate.** `Adeq` concerns target risk, `EmpAdeq` concerns a recorded finite evaluation, and `CertAdeq` requires a valid certificate connecting evidence to the target under an explicit statistical or deterministic interpretation.
- **2026-07-11 — Certificate semantics is mode-specific.** Frequentist coverage is not a posterior probability; Bayesian posterior support is assumption-relative; conformal coverage certifies only its declared target; and calibration tests do not become risk guarantees without a proved implication.
- **2026-07-11 — Full reliance requires an explicit fallback.** `NoFallback` is permitted for adequacy-only judgments but makes the unqualified full use-license ill formed. Reject, defer, status quo, information gathering, or another model/policy must be represented and compared.
- **2026-07-11 — The full license is a factored grant.** Hard certified adequacy, certified improvement over fallback, hard constraints, search-relative admissibility, and provenance must all pass. Narrower permissions must use an explicit requirement profile or a different judgment name.
- **2026-07-11 — Relative evaluated closure is the default.** A finite search can grant only that no certified dominator was found among validly evaluated candidates in the recorded scope. Declared-library closure is stronger and can be withheld by timeouts or omissions; global closure is unavailable without a completeness theorem.
- **2026-07-11 — Gaps force fallback rather than forced choice.** When the active licensed model set is empty, a safe selector must reject, defer, preserve a stated status quo, gather information, or use a separately licensed fallback. Raw argmax over unlicensed models is forbidden.
- **2026-07-11 — Evidence defeat splits rebuttal from lapse.** A countercertificate can refuse a former license; invalidation, expiry, or scope failure without contrary evidence merely withholds it. Discovery of a dominator defeats admissibility but not automatically hard adequacy or archival retention.
- **2026-07-11 — Consequence has three layers.** Model-local object consequence may be classical within one typed context; fixed-stage license consequence is monotone over explicit premises; current consequence is defeasible because its active-license and admissible-evidence base is recomputed at each stage.
- **2026-07-11 — License application yields labeled reliance, not bare truth.** A current license plus a permitted model derivation supports `MayUse`, `LicensedOutput`, or `MayRely` with the model/version/frame/task/domain/purpose/record context intact. There is no truth-detachment rule that erases this label.
- **2026-07-11 — Contradictions are quarantined by typed context.** Differently labeled contrary outputs produce disagreement or decision conflict, not explosion. Cross-context inference requires a valid restriction, bridge, equivalence, or approximate transport witness with its error retained.
- **2026-07-11 — Domain transport is risk-specific.** Set inclusion alone does not move an expected-risk license to a subset, union, intersection, point domain, or extension. Every required domain view and certificate must be reconstructed; uniform worst-case restriction is a conditional special case.
- **2026-07-11 — Raw heredity is not belief or license monotonicity.** Corrections and retractions append to raw history while changing admissible evidence views. Certificates, current licenses, and selections can lapse or be refused without deleting their historical derivations.
- **2026-07-11 — Updates are dependency-directed and stratified.** Primary events feed admissible views, then certificates/comparisons, licenses, and routing. Impact cones permit conservative persistence outside changed dependencies and widen for library/search changes that may affect many admissibility judgments.
- **2026-07-11 — Request records are immutable and versioned.** Changing a domain, tolerance, confidence convention, fallback, cost/purpose, model, or provenance creates a linked new request. Expiry is derived from explicit validity/review conditions, and branch merges recompute rather than union current licenses.
- **2026-07-11 — Dominance compares eligible use plans under a named profile.** Coverage and fallback behavior belong to a model–gate–fallback plan, not always to the bare model. Hard adequacy and safety filter candidates before scalar or Pareto comparison.
- **2026-07-11 — Scalar and Pareto dominance remain distinct.** Scalar dominance requires an explicit monotone scalarization and policy-chosen units/weights. Pareto dominance is the strict product preorder over typed loss, coverage-deficit, cost, robustness, or other coordinates and allows multiple frontier members.
- **2026-07-11 — Certified dominance requires joint uncertainty treatment.** Every required coordinate must be comparable under a mode-correct joint certificate, with a fixed strict witness for Pareto defeat. Missing or boundary-straddling coordinates yield `Unknown`, not a win for either entity.
- **2026-07-11 — Target and operational frontiers differ.** The default relative `UFront` means no certified dominator was found in the evaluated eligible set; `CFront` additionally resolves every required comparison. Neither implies a global Pareto frontier over unknown future models.
- **2026-07-11 — Retention has four layers.** Archive, hard-adequacy, competitive/frontier, and selected-now retention are different. Competitive retention equals the Pareto frontier only under a complete profile/comparison policy; dominance never entails archive deletion.
- **2026-07-11 — Comparison granularity is explicit.** Whole-domain aggregate dominance, declared-cell dominance, and uniformly certified pointwise dominance are different claims. Aggregate superiority can coexist with reversal on a subdomain.
- **2026-07-11 — Partial domination is not automatically a split.** A local/refinement policy must construct a measurable partition, risk-appropriate child measures/samplers or dynamics, corrected certificates, fallbacks, boundaries, and provenance. Without `SplitReady`, local routing is withheld or the valid aggregate policy remains unchanged.
- **2026-07-11 — Comparative defeat is narrower than adequacy revocation.** A dominator can supersede selection on a whole domain or cell while the incumbent remains adequate elsewhere or archived. Adequacy revocation requires a same-scope countercertificate; archive removal requires explicit authorization.
- **2026-07-11 — Falsifications require project-impact propagation.** Every `X1`/refuted ledger disposition must state its significance for the central goal, affected formal/neural/empirical/public artifacts, surviving narrower claim, and roadmap consequence. This prevents a locally falsified premise from remaining silently embedded elsewhere.
- **2026-07-11 — Licensed model cover is weaker than literal atlas structure.** The base scientific object is a finite partial overlapping cover of typed model/use-plan charts. “Scientific licensed atlas” additionally records bridges, seams, routing, frontiers, and provenance; differential-geometric status requires separate manifold and transition-map axioms.
- **2026-07-11 — Overlaps and seams are different.** An overlap may be a thick region with several active charts; a seam is a hard/soft routing transition. The atlas keeps coincident, nested, overlapping, gap, and unknown regions without forcing a disjoint scientific tiling.
- **2026-07-11 — Bridge obligations are operation-specific.** Exact, approximate, statistical, decision, asymptotic, translation-only, incompatible, unknown, and not-required statuses are distinct. Comparison, transport, blending, and gluing require different evidence; overlap alone does not force a successful bridge.
- **2026-07-11 — Approximate stitching is not exact gluing.** Bridge errors compose, triple-overlap path defects must be audited, and convex blends are new use plans with their own semantic, safety, and certificate obligations. Smooth output does not establish theoretical equivalence or truth.
- **2026-07-11 — The atlas router is not one CPWL predictor.** Scientific chart scopes, router selection regions, and ReLU activation cells are separate geometries. Hard expert routing may be discontinuous even with affine experts, whereas an ordinary finite ReLU output is continuous CPWL; exact identification needs seam agreement or an external discrete decision.
- **2026-07-11 — The physics bridge example is deliberately narrow.** Newtonian and relativistic normalized kinetic-energy predictors admit an explicit low-speed approximation bound on a shared observable. This does not make the full theories diffeomorphic charts, establish ontological equivalence, or certify final truth.
- **2026-07-11 — Checkpoint A identified a license/comparison ambiguity, resolved by Task 11A.** An older model may remain in actual use under another purpose, profile, subdomain, resource regime, or fallback role; it may instead remain merely adequate or archived after a successor is preferred. Task 11A compared layered, parameterized-profile, and strong-license designs without presupposing separate predicates, and selected mandatory profile-indexed `Lic_P` with named reliance and preference profiles.
- **2026-07-11 — Checkpoint A narrows the publishable core.** Four-way assessment, scalar typed risk, explicit fallback, labeled reliance, current-view update, gaps, finite comparison status, and extendable stages form the core candidate. Pareto/splitting, full bridge/atlas machinery, certificate-mode instantiations, merges, and policy/value reconstruction are typed extensions or optional case studies.
- **2026-07-11 — Open-endedness will use continuation semantics, not Löbian analogy.** Task 12 must distinguish extendability, stabilization, known stabilization, and finality with explicit continuation countermodels. GL/Löb enters only through a genuine derivability/fixed-point translation; “anti-Löbian” is not an inherited theorem.
- **2026-07-11 — Neural work targets structured finite-stage outputs.** The reference architecture must preserve signed component margins, derived four operational outcomes, simultaneous/empty usable sets, comparison and selection information according to Task 11A's chosen design, fallback, atom-indexed diagnostics, and registry/provenance pointers. A fixed finite baseline and expandable external-memory design are both required.
- **2026-07-11 — Synthetic domains must be independent of learned regions.** The decisive experiment must generate semantic scopes before training and measure scientific-cover, router-partition, and activation-complex alignment separately, avoiding circular success definitions.
- **2026-07-11 — Licensing is profile-indexed.** The primitive judgment is `Lic_P`; omitting `P` is `Undefined(MissingLicenseProfile)`. Profiles contain finite required and report-only atoms, so common “basic reliance” and “preferred use” language becomes readable aliases rather than competing primitives.
- **2026-07-11 — Comparison strength is explicit rather than universal.** `P_rely` does not require library closure; `P_pref-rel` requires no certified dominator in the evaluated set while disclosing unknown pairs; `P_pref-cert` withholds until every relevant comparison is resolved. Neither establishes global optimality.
- **2026-07-11 — Selectors declare their required license profile.** Actual use of an older model can remain valid under another purpose, subdomain, resource regime, fallback role, or weaker justified profile even when a stronger comparison profile fails. Usable-but-unselected and archive-only retention remain distinct.
- **2026-07-11 — Updates and stability are profile-local.** Evidence changes propagate through every profile requiring the affected atom; comparison changes alter required or report-only comparison atoms without automatically rewriting adequacy or unrelated profiles. Current license sets, active sets, and Task 12 stability claims must carry `P`.
- **2026-07-11 — Universal license closure is a superseded default; forced closure is falsified.** E05 is `D1` when read as a proposed universal definition and `X1` only when read as the formal claim that every coherent action-authorizing interface must include a no-better-model clause. The supported replacement is that profiles authorizing comparative preferred use must name finite search/closure strength. This is an interface and claim-discipline correction, not a threat to the project goal.
- **2026-07-11 — World facts and finite-stage status are separate semantic sorts.** Core models are pairs `<W,S>`: population/target adequacy belongs to `W`, while certificates and operational licenses belong to `S`. Soundness must state a certificate-mode bridge rather than treating an agent's stage structure as an oracle.
- **2026-07-11 — Literal profile inclusion is provisional.** Task 11A's required-atom set inclusion order is too sparse for parameterized real requests. Task 13 must define atom entailment/refinement and lift it to profiles before claiming useful antitonicity.
- **2026-07-11 — Aggregate status is derived, diagnostics remain primary.** Neural work will supervise atom assessments and derive the four-way tag symbolically. `Diag` or a lossless safety projection is mandatory because aggregate precedence can hide a certified safety reason in presentation.
- **2026-07-11 — The integrated witness becomes executable before open-endedness.** Task 11B is a semantic reference implementation and test suite, not early neural experimentation. It must make every Task 11A table, transition, scope, and provenance dependency machine-checkable.
- **2026-07-11 — The original recursive-judgment promise must be cashed or demoted.** Task 22A will prove, refute, or narrow B01 in a latent-task information model before the formal paper can use that motivation as more than speculation.
- **2026-07-12 — The paper core targets three carriers, not 28 primitive sorts.** Use plans `E`, reliance contexts `Q`, and epistemic states `S` form the principal carriers; worlds index target semantics, profiles are finite requirement families, and the detailed Task 7 records become a typed elaboration/implementation layer. Compression may not erase the listed scope, evidence, comparison, transport, or provenance distinctions.
- **2026-07-12 — Status uses `WF + K_3`.** Failed well-formedness yields `Undefined`; meaningful atoms are refuted, open, or supported and aggregate by meet to `Refused`, `Withheld`, or `Granted`. Flat reason codes derive from atom identity and witnesses/obstacles/provenance rather than extending the core syntax.
- **2026-07-12 — Formal weight comes from a theorem spine.** The project now targets distinct stability, update/profile/diagnostic, transport/routing, and neural representation clusters. At least three paper-carrying results from different clusters must survive; definitions and standard lemmas do not count by relabeling.
