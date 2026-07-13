# Project Specification: A Finite-Stage License Logic for Fallible Models

Status: Task 5 specification, version 1.2 after Checkpoint B
Created: 2026-07-10  
Checkpoint A amendment: 2026-07-11
Task 11A interface resolution: 2026-07-11
External audit checkpoint A1: 2026-07-11
Checkpoint A1 theorem/elegance amendment: 2026-07-12
Task 11B executable verification: 2026-07-12
Task 12 open-endedness analysis: 2026-07-12
Task 12A core-literature audit: 2026-07-12
Task 13 core-calculus selection: 2026-07-12
Recursive-composition amendment: 2026-07-12
Architecture-neutrality amendment: 2026-07-12
Task 14 metatheory audit: 2026-07-12
Task 14A transport/routing theorems: 2026-07-12
Checkpoint B theorem/neural-roadmap review: 2026-07-12

## Executive specification

This project will develop and test a **finite-stage, domain-relative logic of licensed model use**. Its central judgment does not say that a theory is true. It records a bounded agent's present model-use status for a stated domain and purpose under a mandatory finite requirement profile `P`: `Lic_P`. Profiles state whether adequacy, fallback improvement, hard constraints, trace, finite comparison, coverage, bridge, or other typed atoms are required or merely reported.

The semantic models are explicitly two-sorted pairs `<W,S>`: `W` carries target/world facts such as population risk, while `S` carries the bounded agent's finite record, certificates, library, and operational statuses. No soundness claim may treat a stage certificate as an unqualified world fact; it must state the certificate mode and the relation connecting the two sorts.

The public mathematical core must be materially smaller than the typed implementation schema. Its target presentation has three principal carriers—evaluated use plans `E`, reliance/evaluation contexts `Q`, and finite epistemic states `S`—with worlds as a semantic index and profiles as finite requirement families. Tasks, frames, domains, losses, risk spaces, records, libraries, searches, budgets, certificates, reason displays, and provenance remain available as dependent data or elaborations without all becoming primitive paper-level sorts.

The logic must explain several possibilities without conflating them: an older model may remain in actual use under another purpose, profile, subdomain, resource regime, or fallback role; it may remain adequate but unselected; or it may remain only in the archive after a successor is preferred. Several models may also remain simultaneously usable on overlapping domains. A basic ReLU MLP will be studied as the analytically transparent finite-stage reference implementation of selected scoring, status, gating, comparison, and routing parts of this logic, coupled where necessary to an external registry. The semantics are not ReLU-specific, and later tasks may identify or test a more suitable architecture. The project will not assume that a fixed finite network contains an actually infinite sequence of future theories.

The target is therefore neither a replacement for truth nor ordinary multiclass model selection. It is a formally specified and empirically testable calculus of **scoped reliance under fallibility**.

## 1. Motivational spine

The posts in this repository motivate the order of the argument; they are not treated as evidence for its mathematical or empirical claims.

The recurring structure is:

1. **A bounded agent must evaluate and act before it possesses a final theory.** Waiting for certainty is itself a practical policy, often with consequences.
2. **Performance, preference, and value provide comparison signals before final truth is available.** An agent can observe that one model, judge, or policy performs better than another on a task without concluding that the winner is universally or finally correct.
3. **Repeated evaluation can reveal structure.** A judge that must continue to judge its own judgments, survive new cases, and predict which methods will work is pressured to represent stable distinctions in the world. This is a research motivation, not yet a theorem that value uniquely recovers fact.
4. **Scientific theories exhibit local retention under succession.** A successor may dominate an older theory in one regime while the older theory remains accurate enough, cheaper, more interpretable, or more robust in another.
5. **Policy-to-value reconstruction is a smaller companion problem.** Behavior can induce value or preference constraints relative to an environment, return convention, and data distribution. A reconstructed value model may make decisions more inspectable, but behavioral reconstruction alone does not reveal the original policy's mechanism.
6. **A neural implementation forces representational questions.** The project must say where model identity, domain information, evidence, error, comparative advantage, abstention, and provenance live. A positive ReLU value is a plausible license margin, but it cannot be the entire information state.

This yields the intended narrative:

```text
action before certainty
    -> comparative performance and fallback
    -> domain-relative reliance
    -> explicit licenses and revision
    -> overlapping model cover and abstention
    -> finite neural scoring and routing
    -> tests of transparency and failure
```

The paper may argue that value or usefulness is **epistemically prior for a bounded decision maker** in the limited sense that comparison and action can occur before final knowledge. It must not infer the metaphysical identity of truth and usefulness from that practical ordering.

## 2. Target research question

The primary question is:

> Can a finite-stage, evidence-relative logic represent the licensed use, overlap, supersession, retention, and revision of fallible models, and can its operational judgments be represented or learned by an interpretable finite architecture—using a basic ReLU MLP as the reference case—without erasing the information needed to explain those judgments?

Five subsidiary questions organize the project:

1. Which parts of a judgment such as `Pi(M;D,L,epsilon,...)` follow from the motivating problem, and which are optional engineering choices?
2. What formal objects and consequence/update rules make the proposal a logic rather than a relabeling of loss minimization?
3. How should multiple licensed models, overlapping domains, unresolved bridges, gaps, fallbacks, and abstention be represented?
4. Which parts of the calculus are exactly ReLU-representable, which are only approximable or learnable under assumptions, and what information does rectification destroy?
5. Can the resulting representation expose useful, stable, and causally relevant decision structure in a neural model, rather than merely reproduce its outputs?

## 3. The intended meaning of “logic”

For this paper, a logic is not merely a real-valued score, a loss function, or a trained classifier. At minimum it must specify:

- a **typed language** of models, cases, domains, tasks, losses, tolerances, evidence records, agents, stages, libraries, fallbacks, costs, predictions, and license judgments;
- a **semantics** that states when an empirical adequacy claim, certified license, comparative preference, dominance claim, or abstention judgment obtains;
- a **consequence relation** that states what may be inferred from licensed local models, including how domain restrictions prevent unrestricted export of object-level conclusions;
- **update and defeat rules** for new observations, new models, changed tasks, changed tolerances, domain splits, and corrected provenance;
- a **metatheory** establishing at least some consistency, monotonicity, retention, non-retention, representation, or impossibility results;
- a **neural correspondence** saying precisely which semantic quantities a network input, preactivation, activation, and output represent.

The central judgment will provisionally be called a **license**. “Permission,” “warrant,” and `Pi` may be used informally, but `Lic` should name the fully indexed formal record once the signature is fixed. This terminology emphasizes present authorization to rely on a model and does not imply legal permission, deductive proof of truth, or permanent belief.

The logic has three levels:

1. **Object level:** predictions, equations, rules, and inferences made within a model.
2. **License level:** judgments about where and for what purpose those object-level operations may be relied upon.
3. **Meta level:** claims about revision sequences, eventual stability, completeness, or finality.

Local object-level reasoning may remain classical or use whatever mathematics a model requires. Defeasibility enters primarily through licensing, routing, and update. Consequently, contradiction between two unrestricted theories need not produce global explosion: their usable claims remain indexed to domains and records.

## 4. The intended meaning of “theory” and “model”

The final formalism must not use “theory,” “model,” “representation,” and “policy” interchangeably.

For this project:

- A **theory framework** supplies a vocabulary, state variables, structural principles, and a family of possible laws or models.
- An **instantiated model** `M` is an executable or evaluable predictor, decision rule, simulator, equation set, or local approximation with sufficiently fixed parameters and outputs to score on cases.
- A **representation or frame** specifies coordinates, units, idealizations, state encodings, and translations through which a model is used.
- A **router or selection policy** chooses, mixes, ranks, or abstains among candidate models for a case or domain.
- A **library entry** stores the model identity together with version, frame, training or fitting record, known domain evidence, costs, and provenance.

The core license predicate will normally apply to an instantiated model or library entry because empirical risk cannot be assigned to an underspecified theory family without additional choices. The paper may call such an object a “theory” in motivating prose, but formal passages must identify the scored object.

Two models can make similar predictions while differing in ontology, derivation, cost, or robustness. Conversely, two parameterizations may count as the same model for one question and different models for another. Model identity must therefore be a typed, versioned convention rather than something inferred solely from output equality.

## 5. The intended meaning of “domain”

A domain is not just an unlabeled vector or a region drawn after seeing a network's activations. It is a typed specification of the cases over which a risk, guarantee, or decision claim is evaluated.

The formal domain object should be able to carry one or more of:

- a set of admissible cases;
- a probability distribution or sampling process;
- a task family and action space;
- measurement, intervention, or environmental conditions;
- a risk functional, such as expectation, worst case, tail risk, regret, or a vector of criteria;
- evidence and coverage information;
- a representation/frame in which membership and predictions are meaningful.

These components must remain distinguishable. The same set of cases with a different distribution can yield a different expected risk; the same distribution with a different task or loss can yield a different license.

The project must distinguish:

- a **supplied domain**, fixed independently of model performance;
- an **empirically certified domain**, for which a model has adequate evidence;
- an **induced adequacy region**, such as `{x : s_M(x) >= 0}`;
- an **active-set cell**, on which exactly a given subset of models is licensed;
- a **selection region**, on which a router actually chooses a model;
- an **intrinsic ReLU region**, on which the network computes one affine map.

These objects can align, but alignment is an outcome to prove or measure rather than a definition.

## 6. The intended license object

The motivating question directly supplies a model index and domain index. It does not by itself uniquely supply a scalar loss, a threshold, a confidence convention, a fallback, or a library-relative best-model clause.

A provisional structured license is:

```text
Lic(a,t,b; M,D,L,epsilon,alpha,B,Delta,K,c,trace)
```

where, provisionally:

- `a` is the agent or certifier;
- `t` is the stage or time;
- `b` is the computational/search budget;
- `M` is an instantiated model or library entry;
- `D` is the domain;
- `L` is the predictive or decision loss and risk convention;
- `epsilon` is a hard tolerable risk;
- `alpha` specifies statistical confidence, coverage, or calibration;
- `B` is a fallback or status-quo policy/model;
- `Delta` is the improvement required over that fallback;
- `K` is the searched model library;
- `c` collects cost, robustness, and other admissibility criteria;
- `trace` stores the evidence and derivation provenance.

This list is a specification target, not the final signature; Task 7 will type and simplify it.

The full use decision should factor rather than hide its structure in one threshold:

```text
certified hard adequacy
AND improvement over fallback, when required
AND library-relative admissibility, when required
AND resource/safety constraints
```

The distinction matters because a model can beat “do nothing” while remaining unacceptably dangerous, meet a hard accuracy standard while not improving enough to justify switching, or be adequate without being the preferred member of the current library.

`epsilon` may have at least two legitimate sources:

1. an external task, safety, scientific, engineering, or legal tolerance; or
2. a fallback-induced threshold, for example `epsilon_B(D)=J(B,D)-Delta` under compatible loss units.

It is not the probability that the model is false. It is an operational boundary for a specified risk. Scalar `epsilon` is acceptable only when scalarization is justified; otherwise the logic must support vector thresholds, partial orders, Pareto admissibility, or chance constraints.

## 7. The intended meaning of “fit onto a basic ReLU MLP”

“Fits onto an MLP” will be evaluated at four distinct strengths.

ReLU is a reference model class, not a semantic axiom, uniqueness theorem, or prior claim of empirical optimality. It is attractive because signed affine margins, threshold behavior, exact finite CPWL representation results, and activation-region geometry can be analyzed explicitly. Other architectures are compatible when they preserve or approximate the same typed inputs, atom-level sufficient statistics, diagnostics/missingness, and symbolic `WF + K_3` decoder interface. Universal approximation by itself is insufficient: it says nothing by itself about efficient size, learnability, calibration, preservation of provenance, semantic alignment, or interpretability.

### 7.1 Representability

There is an explicit finite ReLU network, or a controlled approximation result, mapping encoded records/cases to the required signed risks, margins, license indicators, active sets, or routing outputs. A representation result must state its domain, error, network size/depth, boundary convention, and whether inputs such as model identities and tolerances are fixed or variable.

### 7.2 Learnability

A specified data-generating process, target, and loss allow the relevant map to be estimated with finite data. Empirical learnability requires held-out tests, calibration/coverage tests, comparisons with baselines, and failure cases. Successful representation does not imply that gradient descent finds the representation.

### 7.3 Semantic alignment and transparency

Internal or exposed quantities correspond stably to the formal objects they are claimed to encode. The strongest preferred interface exposes component signed margins, active licenses, selected models, abstentions, and provenance. Coordinate interpretations require stability, probing, intervention, or identifiability evidence; prediction alone is insufficient.

### 7.4 Open-ended implementation

The system can add, version, and retain model/domain/evidence records through a sequence of finite stages. This may require an external or expandable registry coupled to a finite scorer/router. It does not require one fixed finite parameter vector to store infinitely many future theories.

The minimal neural target for this paper is representability plus a concrete empirical learnability test. Semantic alignment is a major evaluation target. Universal convergence of training and literal infinite storage are not required.

The provisional loss-first computation is:

```text
encoded model/domain/evidence record
    -> predicted risks or regrets
    -> component signed margins
    -> positive ReLU license channels
    -> active-set report and router/abstention decision
```

The signed preactivation remains semantically primary. `ReLU(s)>0` may gate licensed content and expose positive slack, but all nonpositive values collapse to zero. Where degree or cause of failure matters, the network must retain `s`, retain separate component margins, or use paired channels `(ReLU(s), ReLU(-s))`.

Ordinary softmax cross-entropy is a baseline, not a foregone conclusion. It is poorly matched to cases in which several models are simultaneously adequate or no model is adequate unless a suitable multi-label or abstention construction is added. Task 18 will compare objectives.

## 8. The intended meaning of “handles indefinite succession”

The logic handles indefinite succession if it can describe every finite stage of an extendable revision process without containing a rule that licenses the claim “the present theory is final.”

Concretely, at each finite stage it must support:

1. a finite evidence record and searched model library;
2. addition of a new model, version, observation, task, loss, or domain description;
3. defeat or restriction of an old license when new evidence arrives;
4. discovery of a new dominator without pretending the previous search was globally complete;
5. retention of historical models and evidence even when current selection changes;
6. domain restriction, splitting, overlap, nesting, or expansion;
7. multiple simultaneously licensed models and unresolved comparisons;
8. gaps in the licensed cover and an explicit fallback, information-gathering action, or abstention;
9. changed tolerances, costs, or purposes that can make a stored older model relevant again;
10. provenance sufficient to reconstruct why a license was issued or withdrawn.

The project will represent the process as a sequence of finite records and finite scorers/routers. “Indefinite” means **no fixed last stage is presupposed or internally certified**. It does not mean that an actual infinity is simultaneously stored, that revision must improve monotonically, or that every sequence converges.

Two kinds of retention must be separated:

- **record heredity:** previous models, tests, and decisions remain in the archive unless explicitly corrected or removed;
- **belief or selection monotonicity:** once licensed or chosen, a model stays licensed or chosen.

The first is desirable for auditability; the second is generally false in a defeasible system.

## 9. Atlas requirement

The scientific structure will be modeled as an overlapping partial cover, not a perfect tiling.

For a finite library `{M_1,...,M_n}`, each model has a certified licensed domain `D_i` relative to fixed indices. At a case `x`, the active set is:

```text
A(x) = { i : x belongs to D_i and M_i is licensed at x }.
```

The system must support:

- `|A(x)| = 0`: gap; abstain or use an explicit fallback;
- `|A(x)| = 1`: only one currently licensed model;
- `|A(x)| > 1`: overlap; retain all licenses before applying a selection policy.

Two models may have the same licensed domain while one has lower risk. The lower-risk model may be selected without deleting the other. If two domains overlap partially, the overlap is itself a meaningful active-set region and a location for comparison, calibration, bridge testing, or information gathering.

Bridges across models may be exact, approximate, statistical, decision-equivalent, asymptotic, translated, or unresolved. The paper must never infer scientific equivalence merely from smooth numerical interpolation.

The intrinsic activation complex of a ReLU network and the scientific licensed cover are different. A successful neural atlas alignment may be many-to-one: several activation regions can implement one scientific chart, and one activation pattern need not name a scientifically meaningful regime. Alignment must be defined behaviorally and, where interpretability is claimed, structurally or causally.

## 10. Explicit design requirements

The formalism, architecture, experiments, and final exposition must satisfy the following requirements.

### Logical and semantic requirements

- **DR-L1 — Typed scope:** Every license identifies a model, domain, task/loss, tolerance or comparison rule, evidence stage, and certifying context.
- **DR-L2 — Locality:** Object-level conclusions may be exported only within the licensed domain and purpose, subject to bridge rules.
- **DR-L3 — Defeasibility:** New evidence and newly retrieved competitors can revise current licenses without erasing historical records.
- **DR-L4 — No finality rule:** “Best in the searched library” never entails “best possible” or “final theory.”
- **DR-L5 — Factored reliance:** Hard adequacy, improvement over fallback, comparative admissibility, safety, and cost remain separately inspectable.
- **DR-L6 — Abstention:** Empty licensed sets are representable and operationally distinct from choosing the least bad retrieved model.
- **DR-L7 — Overlap:** Simultaneous licenses and coincident or partially overlapping domains are first-class cases.
- **DR-L8 — Nonexclusive adequacy:** Licensing one model does not by itself negate a different licensed model.
- **DR-L9 — Provenance:** A license has an auditable evidence and derivation trace.
- **DR-L10 — Scalarization discipline:** Scalar thresholds are used only with an explicit loss and scale; vector or partial-order alternatives remain available.
- **DR-L11 — World/stage separation:** Target adequacy, finite-stage certification, and mixed claims are explicitly typed; soundness names a class of `<W,S>` pairs and a certificate-mode bridge.
- **DR-L12 — Design/verdict separation:** Replacing a proposed definition is recorded as a superseded design default, not as falsification unless a separate forced-design proposition is stated and countermodeled.
- **DR-L13 — Core economy:** A distinction becomes a primitive carrier or judgment only when a theorem, countermodel, or typing obstruction requires it. The detailed record schema belongs in an elaboration/implementation layer.
- **DR-L14 — Factored status:** `Undefined` arises from failed well-formedness. Meaningful required atoms use `K_3={refuted,open,supported}` and finite meet to derive `Refused`, `Withheld`, or `Granted`; diagnostic reasons are indexed witnesses/obstacles rather than a closed global enum.
- **DR-L15 — Relative atomicity and disciplined recursion:** A use plan may elaborate to a finite typed component DAG, and a loss/consequence estimator may itself be licensed under a higher-order request. The criterion, its estimator, and the training objective remain distinct; component licenses require an explicit composition rule before they authorize the whole; cyclic self-reference requires separately stated fixed-point semantics.
- **DR-L16 — Transport scope:** Every reused adequacy certificate states whether it covers only a parent mean, prespecified cells, router-selected subsets, an almost-sure pointwise bound, or a uniform/worst-case claim. Routing, bridging, blending, and plan composition expose the measure, coverage, regularity, sensitivity, and fallback assumptions used to transport risk.
- **DR-L17 — Auditable dependency locality:** Current provenance dependencies and future update influence are separated. Each operational atom exposes a typed query/read footprint, including relevant negative reads and validity/correction closure; event schemas expose write footprints. A persistence claim must prove read/write locality or use an explicitly conservative impact overapproximation, and an iff explanation additionally requires observable-specific path realizability.

### Representational and neural requirements

- **DR-N1 — Layer separation:** Structured judgments, vector encodings, predicted risks, signed margins, ReLU activations, and routing outputs are not conflated.
- **DR-N2 — Signed information:** Negative margin magnitude and component failure identity are retained whenever explanation or revision needs them.
- **DR-N3 — Point/domain separation:** A pointwise score does not become a domain guarantee without an aggregation, coverage, or certification rule.
- **DR-N4 — Risk-relative domain encodings:** A domain representation is evaluated for sufficiency with respect to the exact risk functional it supports.
- **DR-N5 — Identifiability humility:** Learned embeddings are interpreted up to observational equivalence unless further constraints or interventions identify their coordinates.
- **DR-N6 — Multiple/empty labels:** The objective and output layer can express several adequate models and no adequate model.
- **DR-N7 — Calibrated routing:** Routing quality is assessed separately from risk prediction and includes coverage/abstention behavior.
- **DR-N8 — Finite-stage capacity:** Network capacity and library size are reported; open-endedness is implemented by staged expansion or external memory.
- **DR-N9 — Atlas distinction:** Activation-region geometry, scientific licensed regions, and router selection regions are evaluated separately.
- **DR-N10 — Transparent interface:** The preferred system can return active models, component margins, chosen/fallback action, and provenance rather than only an argmax label.
- **DR-N11 — Consistency by construction:** Meaningful atom state and missingness/obstacles are supervised; static well-formedness is checked separately; top-level four-way status is derived through `WF + K_3`, with indexed diagnostics and safety projections preserved.
- **DR-N12 — Architecture neutrality:** The semantic input/output contract is stated independently of ReLU. ReLU-specific CPWL and activation results are labeled as reference-architecture results; any alternative is chosen for a stated structural hypothesis and compared under matched semantic outputs with capacity and compute reported.
- **DR-N13 — Quantitative routing interface:** A learned router exposes or permits auditing of selected-scope local risk, coverage, misroute and fallback mass/severity, and any bridge/sensitivity certificate used by the deployed-risk bound. Route-label accuracy alone is not treated as a risk guarantee.
- **DR-N14 — Consumer-relative code claims:** Neural targets state the query family and distinguish a status-minimal quotient from a diagnostic/audit-preserving interface. Finite discrete-code cardinality or bit bounds are not presented as real-valued neural-width bounds without additional precision, robustness, noise, or decoder restrictions.

### Empirical and interpretability requirements

- **DR-E1 — Claims precede verdicts:** New claims are classified as falsifiable/testable, formally provable/refutable, or presently underspecified before being called true or false.
- **DR-E2 — Baselines:** Experiments include a status quo, simple threshold/routing baselines, and a comparison between externally fixed and fallback-induced tolerances where relevant.
- **DR-E3 — Stress cases:** Tests include overlaps, gaps, domain shift, a newly introduced superior model, changed tolerances, and model failure outside training support.
- **DR-E4 — Ablation:** The project tests the effect of losing signed margins, provenance, abstention, or componentwise scores.
- **DR-E5 — Graded interpretability:** Behavioral, value, domain, representational, causal, and human-inspectability results are reported separately.
- **DR-E6 — Reproducibility:** Synthetic generators, seeds, trained artifacts, metrics, and failure cases are retained.

## 11. Required project outputs

A successful project should produce:

1. a typed finite-stage license language and semantics;
2. consequence and update rules that keep object-level reasoning local to licensed domains;
3. definitions of dominance, retention, domain splitting, overlap, bridge types, selection, fallback, and abstention;
4. a theorem spine containing at least three paper-carrying results from distinct clusters: open-ended stability/impossibility, profile logic, calculus-specific update locality/persistence, and neural representation/impossibility; domain/router transport bounds remain load-bearing integration unless a genuinely new result is established;
5. an architecture-neutral realization contract plus an explicit ReLU reference representation or approximation result for a nontrivial finite fragment;
6. an information audit showing what each neural quantity preserves and loses;
7. a reproducible synthetic experiment involving overlap, gaps, supersession, and routing;
8. an interpretability analysis connected carefully to the policy/value reconstruction project;
9. an audited, LaTeX-heavy Gist-compatible paper;
10. a plain-text, low-equation Substack adaptation making the same qualified claims.

The minimal publishable mathematical core is items 1–6 plus clear counterexamples and limitations. Definitions, deterministic aggregation facts, standard set partitions, and one-line order lemmas do not count toward the three-result theorem spine, although they may support it. A failed target can count when replaced by a precise countertheorem with project-impact propagation. The experimental claims are publishable only to the strength actually supported by items 7–8.

## 12. Non-goals

This project does **not** need to establish any of the following:

1. that truth is identical to utility, value, predictive accuracy, usefulness, survival, consensus, or current license;
2. that objective truth does not exist, is inaccessible in principle, or is meaningless;
3. that every present physical theory is false, or that scientific succession must literally continue forever;
4. a resolution of scientific realism, instrumentalism, structural realism, or the pessimistic meta-induction;
5. that a licensed model is approximately true in any metaphysically loaded sense beyond its stated performance relation;
6. that all good judgments, values, or policies uniquely recover factual structure;
7. a universal or unique policy–value isomorphism, or recovery of reward/value from a policy without environment, return, state, and distribution assumptions;
8. mechanistic interpretability merely from training a behaviorally faithful surrogate;
9. that individual ReLU neurons are propositions, that every activation region is a scientific theory, or that ReLU output is a truth degree or probability;
10. that continuous neural interpolation establishes a legitimate bridge between incompatible scientific ontologies;
11. that ordinary cross-entropy is the unique or best learning objective;
12. that exact logical rules are automatically learned by SGD because a network can represent them;
13. that one fixed finite MLP stores or anticipates infinitely many future theories;
14. that the model library is complete, the search has found all relevant competitors, or the current router is globally optimal;
15. a single scalar ordering of accuracy, safety, coverage, robustness, interpretability, and computational cost in every application;
16. a complete logic of all scientific reasoning, a complete AGI epistemology, or a general theory of consciousness, agency, and value;
17. a literal differential-geometric atlas structure unless later definitions and results genuinely require it;
18. empirical confirmation of the motivational claims merely because the formalism is coherent or the synthetic experiment succeeds.
19. that ReLU MLPs are uniquely compatible with the calculus, universally preferable, or empirically optimal among neural, symbolic, routing, monotone, graph, set, or hybrid architectures.

The formalism is compatible with realism, anti-realism, and several pragmatic views because its central claim is conditional and operational: **given a bounded record, task, requirement profile, and any comparison policy that profile invokes, this model has this finite-stage use status here for these reasons**. The required and report-only atom assessments remain inspectable. Stronger metaphysical readings are optional interpretations and must not enter proofs as assumptions.

## 13. Claim boundaries

Every important statement in the final paper should be identifiable as one of four kinds:

- **Definition/design decision:** true by stipulation within the proposed calculus, justified by usefulness and coherence rather than empirical confirmation.
- **Formal result:** proved from stated assumptions, with countermodels used to delimit stronger variants.
- **Empirical claim:** supported by a specified dataset or generator, metric, uncertainty analysis, and reproducible test.
- **Interpretive hypothesis:** a proposed connection to scientific practice, value, truth, or transparency that remains open to further philosophical or empirical argument.

The project must not move silently between these kinds. In particular, a formal representation theorem cannot establish learnability, scientific realism, or human interpretability; an experiment on a synthetic atlas cannot establish that physics is organized by the same latent coordinates; and a persuasive motivation cannot substitute for a theorem or measured result.

## 14. Success and failure criteria

### 14.1 Formal success

The proposal succeeds formally if the compact signature and `<W,S>` semantics are typed, the detailed schema has a semantics-preserving elaboration into that core, and at least three paper-carrying results survive across distinct theorem clusters. Checkpoint B's strict tally counts Task 14's independent-fragment profile result; counts Task 12's stability package after its precision and classical-positioning repairs; and counts the update cluster only after Task 14B derives locality/change-completeness from the actual atom clauses and event schemas. The query quotient is a representation bridge, while Task 14A's measure/Lipschitz/perturbation results are load-bearing standard integration rather than a novelty quota. A positive/negative neural representation cluster remains required and is expected to be the most distinctive result. Finite-algebra corollaries, standard bounds, definitional sanity checks, and renamed standard results remain useful but are not made novel by relabeling. It fails if “logic” remains only a name for comparing scalar losses or if mathematical weight is carried by record definitions rather than results.

### 14.2 Neural success

The proposal succeeds representationally if an explicit finite ReLU reference construction or justified approximation implements a meaningful fragment while preserving the margins required by the semantics. This proves existence for one model class, not architectural uniqueness. It succeeds empirically only if the trained system generalizes and calibrates on held-out overlap, gap, and supersession cases; any architecture comparison must use the same semantic output contract and report capacity/compute differences. It fails if an argmax classifier is presented as the entire calculus or if rectified zeros conceal relevant failure information.

### 14.3 Atlas success

The proposal succeeds if the scientific licensed cover, router partition, and activation complex are separately measured and their alignment is characterized. It fails if polygonal activation regions are simply renamed “theories” without evidence.

### 14.4 Interpretability success

The strongest interpretability claim supported must match the evidence grade. Behavioral reconstruction is useful but insufficient for mechanistic claims. Representational or causal transparency requires stable probes, shared or mapped features, interventions/ablations, and explicit domain limits.

### 14.5 Expository success

Both public artifacts must open with the design questions: why `M` and `D` arise directly; why error and `epsilon` enter only after a risk/task and reliance rule are introduced; how a fallback can induce a threshold; where one model ends when a use plan is recursively composed; and how a target loss differs from a fallible model of loss. They must then separate the structured judgment from its neural representation and separate the two atlas notions before presenting results.

## 15. Proposed paper architecture

The motivating order should be:

1. bounded action and theory succession;
2. what is and is not forced by `Pi(M,D,epsilon)`;
3. relative model granularity, finite recursive composition, and modeled loss;
4. fallback/status quo and factored reliance;
5. the location and preservation of information;
6. overlapping scientific model covers versus ReLU activation complexes;
7. the finite-stage license language and semantics;
8. update, dominance, retention, and abstention results;
9. architecture-neutral realization, the ReLU reference construction, justified alternatives, and learning objectives;
10. synthetic experiments and counterexamples;
11. the policy/value interpretability bridge;
12. philosophical interpretation, limitations, and open problems.

This preserves the posts' motivational direction—value and comparison before certainty, recursive evaluation recovering useful structure—while making the paper's actual claims depend only on explicit definitions, proofs, audited sources, and experiments.

## 16. Terminology contract

Task 11A selected profile-indexed licensing. Layered terms remain readable aliases for named profiles rather than independent semantic primitives.

| Term | Meaning in this project | Does not mean |
|---|---|---|
| adequacy | performance meets a stated risk condition on a domain | truth simpliciter |
| certified adequacy | evidence supports adequacy at a stated calibration/confidence level | infallible proof |
| license profile `P` | finite versioned set of required and report-only typed atoms plus validity/provenance | hidden or universal requirement set |
| `Lic_P` | finite-stage grant for one model/use plan, scope, and explicit profile | truth, final belief, legal permission, or a grant under every profile |
| `K_3` atom value | refuted, open, or supported state of one meaningful requirement | a type error or a complete explanation by itself |
| diagnostic reason | atom-indexed counterwitness, obstacle, or support/provenance rendering | a closed primitive enum of every possible failure |
| `P_rely` / use warrant | named profile requiring adequacy, fallback improvement, hard constraints, and trace | necessarily current comparative preference |
| comparison status | dominated, relatively undefeated, certified undominated, incomparable, unknown, or undefined under a named finite profile/scope | basic adequacy or global optimality |
| `P_pref-rel` / relative preferred use | `P_rely` plus no certified dominator in the evaluated set; unknown pairs disclosed | resolved or global optimality |
| `P_pref-cert` / resolved preferred use | `P_rely` plus certified non-domination/ineligibility for every relevant evaluated candidate | optimality over future or unsearched models |
| margin | signed slack in one explicit comparison | probability or truth degree |
| active `P`-license set | all models satisfying the same named profile at a case | necessarily a unique winner or the active set under another profile |
| selection | a policy chooses/ranks/mixes active models or falls back | deletion of unselected models |
| retention | a model/record remains available or licensed somewhere | monotonic belief in every old claim |
| supersession | a new model defeats, restricts, or is selected over an old one somewhere | universal erasure of the old model |
| domain | typed cases/distribution/task conditions supporting a risk claim | automatically a neural linear region |
| bridge | typed relation connecting models on an overlap | necessarily exact equality |
| licensed model cover / scientific atlas | primarily an overlapping partial cover of warranted model charts; the richer atlas also stores bridges, seams, routing, and provenance | a differential atlas or one-to-one neuron/theory map without extra axioms |
| indefinite | every finite stage admits possible extension without certified finality | actually infinite storage in one MLP |
| transparency | a graded property with behavioral, domain, representational, causal, and human-facing levels | output agreement alone |

## 17. Decisions fixed by this specification

The following decisions are now project defaults unless a later theorem, experiment, or verified literature result gives a documented reason to revise them:

1. The central object is the finite-stage scoped judgment `Lic_P`, not a novel truth value. The profile is mandatory; bare `Lic` is undefined.
2. The logic is finite-stage, indexed, defeasible, and compatible with but agnostic about metaphysical truth.
3. An instantiated, versioned model/library entry—not an underspecified theory family—is the normal object of empirical scoring.
4. Domains are typed risk contexts and can overlap, coincide, nest, or leave gaps.
5. Hard adequacy, fallback improvement, hard constraints, provenance, and comparative/library status remain separately inspectable atoms assembled by a finite license profile.
6. ReLU represents a gate and positive slack; the signed and component information remains available.
7. “Fit” is reported separately as representability, learnability, semantic alignment, and open-ended implementation.
8. Indefinite succession is modeled by an extendable sequence of finite records and systems, not one actually infinite fixed network.
9. The scientific cover, network activation complex, and router partition remain distinct.
10. The posts supply the motivational arc; proofs, experiments, and verified literature supply warrants for public factual claims.
11. `Licensed model cover` is the weakest formal cover term; richer atlas, Pareto, splitting, bridge, merge, and policy/value machinery are extensions unless selected for the frozen core.
12. Selectors declare their required profile; continued old-model use, usable-but-unselected status, and archive-only retention are different outcomes.
13. The 28-sort Task 7 inventory is a typed elaboration, not the paper's primitive ontology; the compact core targets `E`, `Q`, and `S`, with `W` as a semantic index.
14. Well-formedness is checked before evidence status. Meaningful atoms use `K_3`; `Undefined` is not another degree of evidential failure.
15. Flat reason codes are presentation/implementation labels derived from atom identity, polarity, witness or obstacle, and provenance.
16. The mathematical contribution is judged by a multi-cluster theorem spine, not by the number of definitions labeled “Theorem.”
17. Stability fixes `(e,q,P)` and is separated into pathwise eventual stability, permanent current stability, and scheme-relative certified stability.
18. Semantic finality and optional target truth remain metalanguage notions; their absence from the base grammar is not itself a non-finality theorem.
19. Deterministic freeze, statistical margin/coverage, and open-library model addition are distinct stability regimes with different assumptions.
20. Open-library non-finality is directional: a supported finite-library non-domination claim is defeasible by a valid dominator extension, while a persistent refutation may be stable.
21. Licensed consequence is compared with input/output and labelled deduction as output-producing rather than truth-detaching; their source theorems are not inherited without translation.
22. Evidence and provenance terms remain explicit but are not automatically factive proof terms.
23. The well-formed meaningful atom meet is algebraically Strong Kleene; `WF` failure stays outside `K_3`, and Bochvar infection describes only the superseded four-chain.
24. Certificate mode and parameters are explicit: task tolerance, confidence/failure level, and conformal miscoverage must not share one ambiguous `epsilon`; fallback improvement remains independent of hard adequacy.
25. The canonical paper-level request is `(s,e,q,P)`: evaluated use plan, complete reliance context, finite epistemic state, and finite requirement profile. Finite separators show that no coordinate can be dropped while preserving assessment in every core model.
26. `E`, `Q`, and `S` are the only principal operational carriers. `W` is a semantic index, profile families are finite syntax, and the Task 7 record inventory is recovered by typed elaboration rather than promoted to primitive ontology.
27. Profile strength is typed and parameter-sensitive: atom refinement requires exact scope/mode side conditions, request-local profile refinement lifts uniformly to schemas, and certified undominated status refines relative undefeated status only on the same evaluated set and valid search view.
28. `NoLicensedModel` and fallback behavior are selector-level consequences of an empty active set; they are not atom reasons. Full atlas, bridge, Pareto, splitting, and policy/value structures remain formal extensions.
29. Model atomicity is relative to the request interface. A core `e` may hide a finite well-founded graph of object, frame, formulation, solver, evaluator, and action choices; `L_q` names the target criterion rather than any fallible model used to estimate it. Cyclic evaluator/license dependence is not part of the ordinary core without explicit fixed-point semantics.
30. ReLU is the canonical reference construction because it makes signed margins, threshold gates, CPWL representation, and activation geometry explicit. The license semantics and diagnostic interface are architecture-neutral; neither universal approximation nor a successful ReLU construction establishes uniqueness or optimality. Checkpoint B nominated only monotone/lattice and hard-MoE hypotheses; Checkpoint C owns any trained comparison.
31. Update invariance is indexed by both an allowed update class and an observable. Impact-path absence is sufficient under change-completeness and necessary only with path realizability; diagnostic, atom-value, public-status, and grant invariance are not interchangeable.
32. The typed atom refinements are support-sound. Profile refinement is sound generally and relatively complete for finite independently realizable atom fragments; unrepresented conjunctive interactions are outside that completeness theorem.
33. The minimal status representation is the quotient of the realizable atom-vector set by the supported profile queries. Singleton profiles make this quotient equality on `V`; `3^n` and `ceil(n log_2 3)` require full ternary independence, and `WF` needs a separate tagged channel.
34. Operational support is not world-factive. Every target-adequacy or safety conclusion names a certificate-mode bridge and its admissible `<w,s>` class; likewise, gap fallback prevents unlicensed expert use but does not make the fallback target-safe without evidence.
35. Finite acyclic component graphs can be reified as core plans, but component grants do not compose without direct composite evaluation or a proved error/cost/interface propagation certificate. Cyclic evaluator/license dependence remains an explicit fixed-point extension.
36. Expected-risk adequacy transports to every positive-measure measurable subdomain exactly under an almost-sure loss bound. Parent-average, prespecified-cell, selected-subset, pointwise, and uniform certificates are not interchangeable.
37. A deployed hard router is a new use plan whose risk decomposes into correct-route, misroute, and fallback integrals under a measurable covering partition. Selected-subset risk needs its own certificate; whole-cell means give only a conservative integral bound, and mistake frequency needs a severity bound.
38. Prediction bridges control task risk only through a typed regularity bridge. Under `K`-Lipschitz task loss, mean prediction disagreement `delta` yields at most `K delta` risk disagreement; discontinuous decisions and unbounded-sensitivity losses block the unqualified claim.
39. Finite plan-DAG error budgets weight intrinsic errors by sums of downstream path-sensitivity products and require validity on the reachable perturbation tube. Latency, memory, caching, contention, and scalar cost retain separate aggregation rules.
40. Exact invertible group-valued pairwise bridges admit global frame potentials exactly when all cycle products are identity. Approximate, partial, or scope-varying bridges retain defect bounds and path provenance instead.
41. Current provenance-node dependencies do not by themselves characterize future influence. Task 14B must derive atom query/read footprints over typed keys, negative reads, and validity/correction relations, pair them with event write footprints, and prove the concrete locality/change-completeness bridge before the update cluster counts as a theorem of this calculus.
42. The default neural factorization learns continuous atom sufficient statistics and calibrated uncertainty; exact metadata, mechanically decidable `WF`, profile roles, `K_3` aggregation, active-set masking, fallback, evaluated-set identity, and provenance remain symbolic or external unless a task explicitly makes one of them a learned evidence model.
43. The query quotient is consumer-relative. Status-only codes need to refine `V/~_F` plus the required well-formedness observations, while diagnostic-preserving clients require a finer code. Discrete bit bounds do not imply real neural output width, and the `Ill/Well` presentation is a canonical decoded normal form rather than a mandatory internal representation.
44. Task 17 targets architecture-neutral exact factorization, margin-robust decoding, an exact finite ReLU construction for CPWL statistics with an external decoder, a conforming-polyhedral seam characterization/obstruction, and the finite-output versus expandable-library limitation. Universal approximation alone satisfies none of these targets.
45. The only nominated architecture alternatives before Checkpoint C are a monotone/lattice model for explicitly proved monotone coordinates and a hard mixture-of-experts router for discontinuous seams. The symbolic decoder is shared infrastructure; graph/set models remain conditional on Task 15 identifying a specific variable-library or plan-composition hypothesis.
46. The experiment is tiered: core succession/status/calibration first, routing/seams second, and composed-plan or fallible-estimator stress tests only when adequately powered. Activation-region alignment remains exploratory rather than a confirmatory success criterion.

## 18. Specification gates after Checkpoint B

Tasks 7–11 resolved the broad signature, semantics, consequence/update, dominance/retention, and bridge/atlas questions. Task 11A resolved the integration ambiguity by selecting mandatory profile-indexed `Lic_P`, defining canonical reliance/relative-preference/resolved-preference profiles, and validating them in one integrated witness. Checkpoint A1 repaired the witness scope, introduced `<W,S>` semantics, corrected the CPWL attribution, and identified the theorem/executability/motivation risks. Task 11B closed the executable-semantics gate with a compact standard-library `WF + K_3` kernel, a machine-checked three-stage witness, lossless indexed diagnostics, local-link validation, and continuous verification. Task 12 supplied continuation semantics, stabilization/impossibility results, and separation countermodels, with statement and classical-positioning repairs now assigned to Task 14B. Task 12A closed the core-literature gate. Task 13 closed the ontology/interface gate with the canonical three-carrier calculus. Task 14 proved the abstract update, profile, and diagnostic results; Checkpoint B found that the update cluster still needs a concrete reads-from/locality theorem before it counts as a theorem of the operational calculus. Task 14A closed the quantitative transport/routing gate with standard mathematics integrated into the typed license interface. Checkpoint B therefore adds exactly one focused repair gate before ML. Remaining gates are:

- the Task 14B canonical atom-locality/change-completeness theorem, statement/citation repairs, and executable-kernel hardening;
- the smallest architecture-neutral semantic interface and ReLU reference fragment that preserve four-way status, signed component margins, active usable sets, comparison/selection information under the Task 11A design, fallback, and external trace pointers, plus whether one narrowly motivated alternative should be trained (Tasks 15–17 and Checkpoint C);
- the appropriate structured objective and simple baseline for multi-warrant, four-status, calibration, and abstention behavior (Task 18);
- an independently defined synthetic generator and separate functional, calibration, retention, routing, and activation-alignment metrics (Tasks 19–21);
- whether the recursive-judgment information promise receives a theorem/countertheorem or is demoted, and the strongest optional transparency claim that survives policy/value nonidentifiability and causal tests (Tasks 22–23, including Task 22A).

These are research questions, not defects in the specification. A later task may revise a default, but it must record what evidence or formal obstacle caused the revision.

## Task conclusion

The project target is now fixed as a finite-stage logic of scoped, defeasible reliance on models under open-ended succession. The logic must formalize licenses, local consequence, revision, overlap, fallback, and abstention; the neural work must distinguish representation, learning, and transparency; and the philosophical discussion must remain neutral on whether truth is reducible to usefulness. This scope is strong enough to yield formal theorems, counterexamples, neural constructions, and experiments without requiring a final theory of truth or an infinitely capacious MLP.
