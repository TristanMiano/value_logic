# Project Specification: A Finite-Stage License Logic for Fallible Models

Status: living specification, version 2.6 after Task 22A judgment-information theorem
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
Checkpoint B proof-carrying/system-adequacy amendment: 2026-07-12
Task 14B theorem-spine repair: 2026-07-14
Task 14C proof-carrying plans and stratified assessment: 2026-07-14
Tasks 15–18 neural interface, representation, and objective: 2026-07-14
Checkpoint C neural/empirical/publication review: 2026-07-14
Checkpoint C ReLU-sign interpretation clarification: 2026-07-14
Canonical ReLU-semantics toy example: 2026-07-14
ReLU learned-head versus semantic-channel clarification: 2026-07-14
Task 19 decisive-experiment preregistration: 2026-07-14
Task 19A generator pilot and protocol freeze: 2026-07-14
Task 20 frozen experiment implementation: 2026-07-14
Task 20R execution-only repair: 2026-07-16
Task 21 frozen confirmation and analysis: 2026-07-16
Checkpoint C1 empirical adjudication: 2026-07-18
Task 22 policy/value and recursive-judgment audit: 2026-07-18
Task 22 policy/value isomorphism scope correction: 2026-07-18
Task 22A conditional judgment-information theorem: 2026-07-18

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
3. **Repeated evaluation reveals scoped information only under an auditable prediction model.** Task 22A proves that positive population improvement under a strictly proper loss over the true nuisance-conditioned Bayes baseline implies positive conditional outcome information. Under log loss, a `delta`-nat improvement lower-bounds `I(J;Y|N)` by `delta`; explicit non-leakage/mediation transfers the bound to the outcome-identifiable task quotient. Instability and recursive copying still block deployment and incremental-evidence claims.
4. **Scientific theories exhibit local retention under succession.** A successor may dominate an older theory in one regime while the older theory remains accurate enough, cheaper, more interpretable, or more robust in another.
5. **Environment-relative policy evaluation is a smaller companion problem with a broader interpretability motivation.** The project author treats policy as a deliberately general bounded black box and value as a particularly high-level candidate model-of-that-model; even incomplete value surrogates may contain interpretable behavioral information without exposing the full mechanism. Operationally, a policy plus a declared environment, reward/return, state, horizon/discount, perspective, and evaluation distribution induces `V^pi`, `Q^pi`, and occupancy objects. Full state–action occupancy recovers behavior only on its support, while greedy value use is generally policy improvement and equals the original policy only under greediness/tie conditions. Task 23 must test partial surrogate usefulness and interpretability rather than infer mechanism from agreement.
6. **A neural implementation forces representational questions.** The project must say where model identity, domain information, evidence, error, comparative advantage, abstention, and provenance live. A positive ReLU value has no intrinsic license meaning: it becomes predicted slack only when its preactivation is a named learned margin and certificate-relative atom surplus only when that margin is conservatively constructed from accepted evidence. It is never the entire information state or a full license by itself.

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

Within those levels, the word **theorem** must be qualified. A labelled object-model result `[e,q]phi`, an internal derivation `Gamma;s |-VL J`, an externally proved metatheorem about the calculus, and an accepted empirical certificate are different objects. Curry–Howard or proof-term semantics applies directly only to formal derivations or proof objects checked in a named formal system. An empirical confidence region or neural margin can support an operational atom under its certificate mode without becoming an unconditional proof of a target-world fact.

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

For finite recursive composition, the preferred annotated executor returns `(payload, quantitative grade/bound, certificate/provenance)`. The payload performs the task; the grade may include prediction error, risk-to-go, computational resources, or a vector of these; the certificate records why that grade may be used under a named verifier/mode/scope. Plan constructors may transform all three. This is stronger than reifying a DAG but weaker than claiming that every empirical bound is a deductive proof.

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

There is an explicit finite ReLU network, or a controlled approximation result, mapping permitted encoded records/cases to declared quantitative statistics, signed margins, payloads, grades, or utilities. Exact evidence validity, inclusive boundary state, direct `K_3`, active masks, and fallback normally remain in the external decoder rather than being counted as ReLU outputs. A representation result must state its domain, error, network size/depth, boundary convention, and whether inputs such as model identities and tolerances are fixed or variable.

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
    -> proposal-bound accepted evidence envelope
    -> exact atom state and active mask
    -> positive ReLU surplus for named consumers
    -> masked router or fallback
```

The signed preactivation remains semantically primary. After the exact evidence gate and decoder establish support, `ReLU(s)>0` may expose positive slack to a named consumer when `s` is the registered conservative atom margin, but it does not grant or quarantine by itself and all nonpositive values collapse to zero. Where boundary, degree, or cause matters, the system must retain `s`, separate component margins, the exact atom state, and evidence handles, or use paired channels `(ReLU(s), ReLU(-s))`. Exact profile evaluation and active masking supply authorization safety.

A rectified channel may also be consumed as a downstream feature when it has a declared hypothesis index and its preactivation is a commensurate, certificate-valid adequacy grade—or a certified approximation with sufficient boundary separation. In that scoped score-as-content construction, a larger activation means larger positive normalized certificate-relative surplus, not automatically higher probability, world-level adequacy, lower unnormalized risk, or global superiority. General payloads and full diagnostics require separate channels. Exact joint use is permitted only when the representation is sufficient for both the declared license queries and the downstream computation; any use of margin magnitude must state units, normalization, or covariance under allowed rescaling.

The neural component may propose a quantitative grade or certificate statistic. It does not prove its own adequacy. Formal proof terms are checked by a named checker, and empirical certificates require independently defined outcomes, calibration/audit evidence, mode, version, and provenance. A frozen neural-symbolic pipeline can itself be assessed as an ordinary plan under a higher-ranked context, but its self-confidence is not its sole warrant.

Task 18 selects standardized center–radius atom-statistic regression with squared center error and an interval score as the primary objective, followed by disjoint held-out residual calibration. Independent per-atom three-way cross-entropy is the simple baseline; it can represent simultaneous and empty granted-plan sets only because it is applied independently and aggregated symbolically, never as one library softmax. Direct state and aggregate-status heads do not authorize use.

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
- **DR-L18 — Proof-carrying composition:** A certified finite recursive plan separates computational payload, quantitative grade/bound, and evidence/provenance. Every admitted constructor states its output, grade, and certificate transformers plus interface, scope, frame, termination, and validity assumptions. Composite authorization uses a direct or constructed composite certificate, never the meet of component grants alone.
- **DR-L19 — Theorem and reflection stratification:** Labelled object results, internal value-logic derivations, external metatheorems, and empirical certificate judgments remain distinct. Assessment of a value-logic implementation is an ordinary higher-order request grounded in typed base evidence or lower-ranked verifiers; self-endorsement and ungrounded support cycles cannot authorize themselves in the finite core.

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
- **DR-N11 — Consistency by construction:** Externally defined meaningful-atom sufficient statistics are supervised, while exact missingness/obstacles remain side-packet facts; atom state is decoded symbolically and may receive only auxiliary direct supervision. Static well-formedness is checked separately; top-level four-way status is derived through `WF + K_3`, with indexed diagnostics and safety projections preserved.
- **DR-N12 — Architecture neutrality:** The semantic input/output contract is stated independently of ReLU. ReLU-specific CPWL and activation results are labeled as reference-architecture results; any alternative is chosen for a stated structural hypothesis and compared under matched semantic outputs with capacity and compute reported.
- **DR-N13 — Quantitative routing interface:** A learned router exposes or permits auditing of selected-scope local risk, coverage, misroute and fallback mass/severity, and any bridge/sensitivity certificate used by the deployed-risk bound. Route-label accuracy alone is not treated as a risk guarantee.
- **DR-N14 — Consumer-relative code claims:** Neural targets state the query family and distinguish a status-minimal quotient from a diagnostic/audit-preserving interface. Finite discrete-code cardinality or bit bounds are not presented as real-valued neural-width bounds without additional precision, robustness, noise, or decoder restrictions.
- **DR-N15 — Joint computation/license sufficiency:** A dual-use representation is claimed only for a declared license-query family and downstream computation, with proof that equal codes imply equal required query answers and computational outputs. Equal adequacy margins with different payloads are an explicit failure case.
- **DR-N16 — Typed dual-use margins:** Hypothesis-indexed ReLU channels may serve as positive certificate-relative adequacy surplus and downstream features only with an explicit channel map, common/normalized units, calibration, certificate validity or verified error envelope, domain, boundary convention, and scale transformation rule. Signed/open/missing status and proof/certificate data are not silently compressed into the positive activation.

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
5. a proved or sharply countermodeled certificate-carrying finite-plan construction, explicit theorem-level taxonomy, and grounded/stratified system-assessment result;
6. an architecture-neutral realization contract plus an explicit ReLU reference representation or approximation result for a nontrivial finite fragment, including the conditions for dual-use adequacy features;
7. an information audit showing what each neural quantity preserves and loses;
8. a reproducible synthetic experiment involving overlap, gaps, supersession, routing, and a bounded system-adequacy audit;
9. an interpretability analysis connected carefully to the policy/value reconstruction project;
10. an audited, LaTeX-heavy Gist-compatible paper;
11. a plain-text, low-equation Substack adaptation making the same qualified claims.

The minimal publishable mathematical core is items 1–7 plus clear counterexamples and limitations. Definitions, deterministic aggregation facts, standard set partitions, and one-line order lemmas do not count toward the three-result theorem spine, although they may support it. A failed target can count when replaced by a precise countertheorem with project-impact propagation. The experimental claims are publishable only to the strength actually supported by items 8–9.

## 12. Non-goals

This project does **not** need to establish any of the following:

1. that truth is identical to utility, value, predictive accuracy, usefulness, survival, consensus, or current license;
2. that objective truth does not exist, is inaccessible in principle, or is meaningless;
3. that every present physical theory is false, or that scientific succession must literally continue forever;
4. a resolution of scientific realism, instrumentalism, structural realism, or the pessimistic meta-induction;
5. that a licensed model is approximately true in any metaphysically loaded sense beyond its stated performance relation;
6. that all good judgments, values, or policies uniquely recover factual structure;
7. a unique, canonical, or standard-return policy–value isomorphism, or recovery of reward/return value from a policy without environment, return, state, and distribution assumptions;
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
20. that every ReLU hidden activation is an adequacy value, posterior probability, proposition, proof, or semantically identifiable feature.
21. that a system's predicted confidence or self-issued license is sufficient evidence of its own adequacy.
22. an unrestricted reflection principle, consistency proof, or uniquely determined cyclic self-license for value logic.

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

The proposal succeeds formally if the compact signature and `<W,S>` semantics are typed, the detailed schema has a semantics-preserving elaboration into that core, and at least three paper-carrying results survive across distinct theorem clusters. The strict pre-neural tally now counts Task 14's instantiation-fiber profile result, Task 12's repaired and classically positioned stability package, and Tasks 14/14B's calculus-specific typed-locality/update cluster. Task 14C additionally proves the finite proof-carrying-plan construction and sharply delimits theorem levels, grounded provenance, stratified system assessment, and self-endorsement; its structural inductions are classified as established machinery, while their `WF + K_3` integration is the project result. The query quotient and Task 14A are supporting bridges/integration. A positive/negative neural representation cluster remains required and should include the joint-sufficiency boundary for dual-use activations. Standard facts and definitional checks remain useful but do not clear the contribution bar. The proposal fails if “logic” remains only scalar-loss comparison, if recursive composition is only a record schema, or if self-confidence is presented as self-certification.

### 14.2 Neural success

The proposal now succeeds representationally at the Task 17 scope: an explicit finite ReLU reference construction or justified approximation implements global finite CPWL statistics and proof-erased plans while preserving required payload, grade, status, and audit distinctions. Joint sufficiency, boundary handling, and scale semantics are proved for the named coordinate-complete dual-use family; certificate verification remains symbolic. This proves existence for one model class, not architectural uniqueness. The frozen empirical result is deliberately nonbinary: the statistic-output arm generalizes strongly to changed tolerances without retraining and its accepted proposals attain registered marginal coverage, but the tested conservative pipeline is refuted at its registered boundary-superiority and in-regime-noninferiority margins and falls back at rate `0.9962`. No powered system-audit or architecture claim was tested. Empirical success must therefore be stated component by component rather than as an end-to-end neural-logic victory. The proposal fails if argmax is the entire calculus, rectified zeros conceal failure information, arbitrary hidden activations are renamed adequacy, or self-confidence is used as the system certificate.

### 14.3 Atlas success

The proposal succeeds if the scientific licensed cover, router partition, and activation complex are separately measured and their alignment is characterized. It fails if polygonal activation regions are simply renamed “theories” without evidence.

### 14.4 Interpretability success

The strongest interpretability claim supported must match the evidence grade. The companion supplies environment-relative policy evaluation and a conditional greedy-agreement case study, not evidence that its learned standard-return surrogate is a unique, natural, or identifiable policy inverse. This empirical boundary does not refute the separate finite representation-existence construction. Behavioral reconstruction is useful but insufficient for mechanistic claims. Representational or causal transparency requires stable probes, shared or mapped features, interventions/ablations, and explicit domain limits.

### 14.5 Expository success

Both public artifacts must open with the design questions: why `M` and `D` arise directly; why error and `epsilon` enter only after a risk/task and reliance rule are introduced; how a fallback can induce a threshold; where one model ends when a use plan is recursively composed; how a target loss differs from a fallible model of loss; and when an adequacy margin can also be downstream computational content. They must explain object results, internal derivations, metatheorems, and empirical certificates before discussing self/system adequacy, then separate the structured judgment from its neural representation and the two atlas notions.

## 15. Proposed paper architecture

The motivating order should be:

1. bounded action and theory succession;
2. what is and is not forced by `Pi(M,D,epsilon)`, including external and fallback-derived tolerance;
3. finite-stage licenses, open evidence, overlap, gaps, and revision through one running example;
4. relative model granularity, finite recursive composition, and modeled loss;
5. proof-carrying computation, theorem levels, and grounded system assessment;
6. the location and preservation of information, including the classifier/dual-use margin intuition;
7. overlapping scientific model covers versus ReLU activation complexes;
8. the compact finite-stage license language and semantics;
9. update, dominance, retention, and abstention results;
10. architecture-neutral realization, the ReLU reference construction, justified alternatives, and learning objectives;
11. synthetic experiments and counterexamples;
12. the optional environment-relative policy/value case study and interpretability bridge, only at the evidence grade surviving Tasks 22–23;
13. philosophical interpretation, limitations, and open problems.

This preserves the posts' motivational direction—value and comparison before certainty, recursive evaluation recovering useful structure—while making the paper's actual claims depend only on explicit definitions, proofs, audited sources, and experiments.

## 16. Terminology contract

Task 11A selected profile-indexed licensing. Layered terms remain readable aliases for named profiles rather than independent semantic primitives.

| Term | Meaning in this project | Does not mean |
|---|---|---|
| adequacy | performance meets a stated risk condition on a domain | truth simpliciter |
| certified adequacy | evidence supports adequacy at a stated calibration/confidence level | infallible proof |
| quantitative grade/bound | typed error, risk-to-go, resource, or other value propagated with a computation | the certificate proving that the bound is valid |
| proof/certificate term | checked formal evidence or mode-relative empirical evidence with scope, assumptions, version, and provenance | an arbitrary neural score or unconditional world truth |
| object-model result | a labelled result of a named model, equation system, or object prover, possibly carrying a proof term in its own formal theory | automatically an internal value-logic derivation or unlabelled world truth |
| internal value-logic theorem | a value-logic judgment derivable under stated premises, state, rules, and checked evidence | automatically an external metatheorem, object-theory proof, or unlabelled truth |
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
30. ReLU is the canonical reference construction because it makes signed margins, threshold gates, CPWL representation, and activation geometry explicit. The license semantics and diagnostic interface are architecture-neutral; neither universal approximation nor a successful ReLU construction establishes uniqueness or optimality. Checkpoint C selects no alternative for the minimum empirical core and permits only a separately powered hard-MoE seam extension.
31. Update invariance is indexed by both an allowed update class and an observable. Impact-path absence is sufficient under change-completeness and necessary only with path realizability; diagnostic, atom-value, public-status, and grant invariance are not interchangeable.
32. The typed atom refinements are support-sound. Profile refinement is sound generally and relatively complete within finite independently realizable instantiation fibers; unrepresented conjunctive interactions and schema-uniform completeness are outside that theorem.
33. The minimal status representation is the quotient of the realizable atom-vector set by the supported profile queries. Singleton profiles make this quotient equality on `V`; `3^n` and `ceil(n log_2 3)` require full ternary independence, and exact public decoding must distinguish the `WF` branch from meaningful status without requiring a literal internal tag.
34. Operational support is not world-factive. Every target-adequacy or safety conclusion names a certificate-mode bridge and its admissible `<w,s>` class; likewise, gap fallback prevents unlicensed expert use but does not make the fallback target-safe without evidence.
35. Finite acyclic component graphs can be reified as core plans, but component grants do not compose without direct composite evaluation or a proved error/cost/interface propagation certificate. Cyclic evaluator/license dependence remains an explicit fixed-point extension.
36. Expected-risk adequacy transports to every positive-measure measurable subdomain exactly under an almost-sure loss bound. Parent-average, prespecified-cell, selected-subset, pointwise, and uniform certificates are not interchangeable.
37. A deployed hard router is a new use plan whose risk decomposes into correct-route, misroute, and fallback integrals under a measurable covering partition. Selected-subset risk needs its own certificate; whole-cell means give only a conservative integral bound, and mistake frequency needs a severity bound.
38. Prediction bridges control task risk only through a typed regularity bridge. Under `K`-Lipschitz task loss, mean prediction disagreement `delta` yields at most `K delta` risk disagreement; discontinuous decisions and unbounded-sensitivity losses block the unqualified claim.
39. Finite plan-DAG error budgets weight intrinsic errors by sums of downstream path-sensitivity products and require validity on the reachable perturbation tube. Latency, memory, caching, contention, and scalar cost retain separate aggregation rules.
40. Exact invertible group-valued pairwise bridges admit global frame potentials exactly when all cycle products are identity. Approximate, partial, or scope-varying bridges retain defect bounds and path provenance instead.
41. Current provenance-node dependencies do not by themselves characterize future influence. Task 14B derives atom query/read footprints over typed keys, negative reads, and validity/correction relations, pairs them with event write footprints, proves complete-diagnostic locality by cases, and proves the canonical event-to-key-to-slot graph change-complete. The update cluster therefore counts as a theorem of this calculus; necessity of path absence remains conditional on observable-specific path realizability.
42. The default neural factorization learns continuous atom sufficient statistics and calibrated uncertainty; exact metadata, mechanically decidable `WF`, profile roles, `K_3` aggregation, active-set masking, fallback, evaluated-set identity, and provenance remain symbolic or external unless a task explicitly makes one of them a learned evidence model.
43. The query quotient is consumer-relative. Status-only codes need to refine `V/~_F` plus the required well-formedness observations, while diagnostic-preserving clients require a finer code. Discrete bit bounds do not imply real neural output width, and the `Ill/Well` presentation is a canonical decoded normal form rather than a mandatory internal representation.
44. Task 17 proves architecture-neutral exact factorization, margin-robust decoding with the explicit conservative decision band, an exact finite ReLU construction for global finite CPWL statistics with an external decoder, a conforming-polyhedral seam characterization/obstruction, and the finite-output versus expandable-library limitation. Universal approximation alone satisfies none of these results.
45. Checkpoint C authorizes no alternative architecture in the minimum empirical core. Hard mixture-of-experts is the sole eligible optional comparator because it directly tests discontinuous seam mismatch; it proceeds only after a separate power gate and otherwise remains a follow-up against the frozen generator. Monotone/lattice is deferred because tolerance monotonicity already belongs to the exact decoder, and the graph/set `F33` comparison is deferred until many independent structural separators can power it.
46. The minimum publishable experiment is core succession/status plus `F35/H18.1`, registered marginal calibration `F36/H18.2`, an in-regime noninferiority guard, and Task 18 ablations 1–3 and 5. Routing/seams and certificate/system assessment are separately gated extensions; deterministic integration witnesses are not renamed powered empirical results. Activation-region alignment remains exploratory rather than a confirmatory success criterion.
47. A finite recursively structured model is represented by a certificate-carrying executor whose output separates payload, quantitative grade/bound, and evidence/provenance. Task 14C proves by topological induction that locally certified typed constructors produce a checked root bundle whose proof erasure is the ordinary computation; Task 14A's path-sensitivity recurrence is a concrete grade/certificate transformer. The composite receives a new certificate rather than inheriting the conjunction of component grants.
48. “Theorem” is level-indexed. Labelled object results, internal value-logic derivations, external metatheorems, and empirical certificate judgments are not interchangeable. Curry–Howard applies only to formal derivations/proof terms under a named checker; empirical support requires a certificate-mode world bridge. Task 14C's primary-source audit classifies proof/program correspondence, Hoare composition, refinement/quantitative typing, PCC, and certifying algorithms as prior machinery.
49. ReLU sign has inherited rather than intrinsic semantics. For `z=ReLU(s)`, `z>0` unconditionally says only `s>0`; a named learned margin gives predicted slack, while a conservative margin tied to accepted evidence can give certificate-relative surplus for one atom. Such a surplus may also be downstream content when its channel, statistic, units, calibration, certificate validity or verified error envelope, domain, boundary, and consumer are declared and the code is jointly sufficient. None of these alone is a full profile license. Arbitrary hidden units and unnormalized cross-channel magnitudes receive no adequacy interpretation.
50. Joint positive rescaling can preserve a license boundary while changing margin magnitude. Any downstream use of the magnitude must transform covariantly or use a fixed normalization; multiplying a payload by a margin defines a new plan requiring evaluation.
51. A frozen value-logic implementation may be assessed as a plan under an independently specified meta-context. Task 14C proves that finite acyclic support reaches typed bases when every zero-premise support is an accepted base, and that strict finite-rank dependencies with total deterministic local evaluators have a unique assessment. Its own assertion is not its certificate or a target-world fact, and direct self-license cycles require explicit fixed-point semantics.
52. Tasks 14C–21 and Checkpoints C/C1 are complete. Task 18 selected the structured statistic/uncertainty objective, held-out calibration path, independent atom-classification baseline, and separate router loss; Tasks 19–21 froze and ran their comparison once. Checkpoint C1 keeps the hybrid interface but rejects a general structured-objective preference: aggregate `F35=I1`, transfer `F35a=S1`, boundary and in-regime components `F35b/F35c=X1`, and marginal proposal coverage `F36=S1` at exact scope.
53. Missing evidence is an open atom diagnostic, whereas a missing required or report diagnostic makes a purported well-formed core state invalid. Diagnostic payloads form a disjoint sum, and comparison atoms without a valid exact-set search are open unless a valid dominator already refutes them.
54. The architecture-neutral atom input is its exact typed address plus the canonical projection of its Task 14B address-local read footprint. Profile slots form addresses and assign required/report/safety roles; two slots instantiating the same address consume the same atom record. Exact metadata and handles may have learned embeddings but cannot survive only as anonymous latent coordinates when the decoder or audit depends on their identity.
55. The neural interface is query-family-specific. A status-only client may use the required `WF` observations plus `V/~_F`; an audit client retains unquotiented address-indexed diagnostics, safety roles, statistics/envelopes, and exact evidence references over a declared future address horizon. No finite code is claimed sufficient for arbitrary future profiles.
56. A fixed model-indexed output is restricted to its declared finite registry. A candidate-conditioned shared scorer supports a growing external registry and permutation-equivariant evaluation, but it does not guarantee cold-start accuracy or injectively compress unbounded independent records. Sparse pair evaluation costs `Theta(n+|E_K|)` but supplies only the queried evidence; supporting certified non-domination for every candidate can still require quadratic pair resolution.
57. Every encoded annotated-plan node keeps payload, quantitative grade/envelope, certificate/checker/version/assumptions, provenance/rank, and loss-estimator identity distinguishable. Typed plan encodings are invariant only under root-, port-, interface-, grade-, checker-, and incidence-preserving DAG isomorphism; equal final payload does not erase cost, sharing, robustness, or evidential differences.
58. Joint license/computation sufficiency is indexed by independently declared consumer families `F` and `C`: the code kernel must refine their joint observational equivalence. Task 17 proves the general equal-code obstruction and, for the coordinate-complete named-channel family, proves that exact atom states plus normalized positive ReLU margins form the minimal quotient. Equal adequacy with unequal payload, inclusive equality at zero, invalid evidence, and unnormalized rescaling block stronger scalar interpretations.
59. The ReLU reference predicts scalar center/region, nonnegative spread, uncertainty and conservative-validity proposals, plus separately typed payload and grade heads. A named external calibration procedure supplies the accepted error radius, and exact checker/version/polarity records determine whether the resulting conservative region may support or refute. A learned uncertainty or validity score is never its own certificate.
60. Scalar adequacy uses `m_support=epsilon-upper(U_safe)` and `m_refute=lower(U_safe)-epsilon`, with inclusive support, strict refutation, and open boundary crossing. The architecture retains signed and paired-ReLU channels plus the exact diagnostic; supported equality has zero positive activation and is therefore not recoverable from the rectified scalar alone.
61. Learned validity is conservative-only: it may turn otherwise usable evidence open under a declared reject rule, but it cannot validate absent, expired, conflicted, uncalibrated, or checker-rejected evidence. One-sided modes cannot manufacture the unsupported polarity.
62. Named dual-use channels declare exact hypothesis/address, domain, normalization semantics and scale, calibration/checker versions, and downstream consumers. Their positive normalized ReLU surplus may enter the declared downstream plan alongside an exact support bit and any required content; separate payload/grade channels remain the general default, and margin-times-variable-payload computation is a new plan requiring evaluation.
63. Licensing precedes routing. The production selector ranges only over the exact active set for its named profile, returns the exact fallback on a gap, and requires an explicit tie rule. Aggregate-status, flat-reason, self-grant, unmasked-argmax/softmax, and predicted-certificate heads are disconnected ablations rather than authorization paths.
64. ReLU zero does not by itself quarantine downstream computation: bias or bypass paths can remain nonzero. Exact active-set masking supplies the supported quarantine property. ReLU remains useful for positive slack and CPWL analysis, not as an intrinsic non-explosion theorem.
65. The monotone/lattice variant is restricted to learned coordinates with proved monotonic targets; tolerance monotonicity already lives in the exact decoder. The hard-MoE variant keeps the same active mask/evidence interface and is motivated only by discontinuous seams, with route, fallback, selected-scope, and severity certificates still required. Graph/set structure remains an optional matched plan-DAG hypothesis.
66. Exact public realization is consumer-relative: a code is sufficient exactly when equal codes preserve the required `WF` observation and `V/~_F` class. Diagnostic/audit clients require the corresponding finer quotient. `Ill/Well` is a canonical decoded form, and finite discrete-code bits do not imply a real-output-width bound without precision or robustness assumptions.
67. If learned statistics have accepted coordinate errors `delta_j`, an affine boundary has raw propagated radius `r=sum_j |alpha_j|delta_j`. Conservative interval decoding is sound everywhere the envelope holds and uniformly recovers the ideal decision outside the `2r` ideal-margin band. The factor two is retained in training and experimental boundary metrics.
68. A fixed-dimensional global finite CPWL statistic map has an exact finite ReLU realization with affine output. Under the audited convention the scalar hidden-depth upper bound is `ceil(log_2(d+1))`; vector maps are realized coordinatewise and size is finite but can be enormous. A restricted-domain claim must name a global CPWL extension.
69. A finite conforming hard assembly of affine experts is continuous exactly when their traces agree on every relevant common face. Agreement across a codimension-one hyperplane forces a rank-at-most-one Jacobian change; disagreement at a two-sided accumulation face cannot be one ordinary continuous ReLU output and motivates only an external hard router or MoE.
70. Candidate-conditioned shared scoring is permutation-equivariant over any finite external registry in its input domain, but neither it nor sparse evaluation certifies global non-domination. Two registry extensions can agree on all evaluated records while an unseen candidate dominates the current one.
71. The named dual-use code consists of the exact mode-relative state vector plus normalized positive margins. It is minimal up to relabeling for any consumer family containing all state and surplus coordinate projections; CPWL margins make its numerical half exactly ReLU-realizable. Other consumer families may admit coarser quotients, and general payloads remain separate.
72. Under `m_i'=lambda_i m_i`, license status is invariant but raw positive surplus scales. Production downstream use must either rescale `sigma_i` with `lambda_i`, transform the consumer covariantly, or declare a homogeneous unit-bearing output. Independent unnormalized scaling invalidates cross-channel magnitude and argmax comparisons.
73. A fixed finite proof-erased annotated plan with CPWL primitives, CPWL grade transformers, and conforming hard branches has a joint CPWL payload/grade map and exact finite ReLU realization. Proof terms, accepted certificates, checker results, assumptions, and provenance remain external. Bilinear margin-times-payload gates, non-CPWL primitives, unbounded recursion, and discontinuous seams require a different construction or a verified approximation envelope.
74. The reference learning target is an externally defined atom-sufficient statistic. Its standardized schema-balanced objective combines squared center error with a central interval score; missing targets are masked rather than zero-imputed, and payload, grade, and conservative reject auxiliaries retain separate typed terms.
75. The trained center/radius is only a proposal. A disjoint held-out calibration split supplies a finite residual-expansion proposal, including an unbounded result when data are insufficient; a versioned mode/checker must accept its assumptions, scope, polarity, and downstream-risk bridge before the region can support or refute.
76. Production states remain symbolic. Exact `WF`, evidence state, certificate polarity, inclusive support, strict refutation, `K_3` meet, active mask, and fallback derive the result. Independent three-way atom cross-entropy is the simple baseline; direct atom, aggregate status, reason, and self-grant heads are nonauthorizing auxiliaries or ablations.
77. Router learning is separate from licensing. Pairwise ranking uses only exact-active, externally resolved comparable pairs; inactive, missing, unknown, and tied pairs are masked. Selective risk is reported jointly with coverage and fallback-inclusive deployed risk, and a fallback-induced threshold is distinct from a fixed adequacy tolerance unless the policy explicitly identifies them.
78. Unit-bearing statistic losses and dual-use surplus channels use registered scales. Positive joint rescaling leaves the standardized objective, exact boundary state, and normalized surplus unchanged; regularization occurs in normalized coordinates and supplies no semantic-alignment guarantee.
79. An accepted calibration envelope is an immutable bound record tying atom/statistic schema, candidate, units, scorer hash, split manifest, calibration procedure and parameters, scope/group, polarity, checker/version, validity interval, and provenance. The decoder rejects cross-record substitution.
80. The experiment separates train, envelope calibration, reject/router validation, system audit, and final confirmation by latent generator world/trajectory, provenance root, and plan family. Atom rows, candidates, time variants, and training seeds are not independent target-world replicates.
81. Structured and atom-cross-entropy arms share the permitted pre-outcome input and exact `WF`/missingness/validity/polarity machinery. Common endpoints are tolerance-transfer and boundary/status behavior; interval coverage and class-probability calibration remain different objects.
82. Atomwise marginal coverage does not entail profile-conjunction, selected-subset, routed, or system guarantees. A frozen system's candidate certificate is built from lower-ranked audit data and its status is tested on untouched confirmation data; self-confidence-only pseudo-evidence is invalid by construction.
83. The public narrative order is physics succession, reliance before final truth, fallback/status quo and the origin of `epsilon`, finite-stage licenses/overlap/revision, then the classifier and dual-use ReLU intuition followed immediately by its sign-semantics correction. The neural fit was deliberately engineered at a typed boundary and mathematically delimited; the project does not claim that every continuous target is CPWL.
84. Task 17's named state-plus-surplus code is minimal only for a consumer family containing all of its coordinate projections. It is a coordinate-separation result, not information-theoretic optimality for arbitrary external consumers, and it is not a headline contribution.
85. The public artifacts must present the ReLU-sign correction as a semantic ladder: arbitrary positivity, predicted positive slack, accepted certificate-relative atom surplus, and full exact profile licensing are distinct. Supported equality is a required zero-activation counterexample, and bias/bypass behavior is the required counterexample to zero-as-quarantine. This is an author-intuition repair, not a minor implementation caveat.
86. The canonical neural-semantics example is the three-required-atom profile `A and I and C`: loss adequacy, fallback improvement, and a latency constraint. It retains signed support/refutation margins, exact `K_3` one-hots, evidence validity/missingness, normalized surplus, and `WF`; a fixed ReLU conjunction over exact support bits may encode the grant answer for the fixed request, while a separate ReLU may consume surplus only after the exact active mask. Tasks 19, 29, and the public adaptations reuse this example rather than silently changing the meanings of zero, slack, surplus, adequacy, license, or selection.
87. Learned heads, scalar coordinates, and fixed decoder channels are distinct. Two rectified channels `z_support,z_refute` may be deterministic functions of one shared learned interval rather than separately parameterized heads, but their pair is not sufficient for `K_3`: boundary support, open, missing, and invalid cases can all map to `(0,0)`. Multiple semantic channels per atom are therefore generally required by the selected audit-preserving interface, including exact state and evidence diagnostics, while the number and sharing pattern of learned heads remains an empirical architecture choice. This is not a lower bound on arbitrary real encodings of finitely many labels. One accepted statistic interval may serve several atoms with different thresholds.
88. The preregistered synthetic succession study uses independent world/trajectory and plan-lineage roots, overlapping old/successor/later-specialist scopes, an intentional pre-successor gap, exact oracle evidence, positive-density boundary cases, all four public outcomes, lapse versus rebuttal, footprint-relevant versus irrelevant updates, tolerance change without retraining, and finite-set dominance. It is a semantic stress distribution and Newtonian-like narrative fixture, not a physical error model.
89. `F35/H18.1` requires structured-arm superiority of at least five percentage points on both target-weighted tolerance-transfer and boundary-state macro fidelity, Holm-controlled at one-sided familywise `.05`, plus in-regime noninferiority within two points. Independent worlds are paired units; rows are clustered and eight fit seeds are repeated fits. Because a generator-only pilot cannot observe variance from unimplemented learners, Task 19A prospectively replaces that impossible estimate with disclosed worst-coupling bounds at the registered design alternatives; these are planning assumptions, not learner evidence.
90. `F36/H18.2` concerns 90% marginal target-in-proposal coverage for the checker-accepted held-out expansion procedure in separately registered `J/T` exchangeable groups. Every pre-outcome-eligible confirmation target enters, and support requires each Holm-adjusted one-sided world-clustered lower bound to reach `.88`; point estimates and distance from `.90` are still reported. An infinite proposal counts as containing a finite target for the coverage theorem but is unusable evidence and makes the atom Open. Finite-only, selected, profile, routed, and system coverage remain different descriptive or separately certified quantities.
91. The primary structured factorization is one shared ReLU trunk and one vector-valued learned statistic head emitting loss/latency center-radius coordinates. `A` and `I` reuse the loss coordinates. Signed margins, paired ReLUs, `K_3`, `WF`, aggregation, and masks are deterministic semantic channels, not learned heads. A separate-head variant is descriptive and any performance difference is empirical rather than logically required.
92. The final confirmation role remained embargoed until the one authorized Task 21 v1.1 confirmation command after disjoint manifests, power, seeds, stopping, model, calibration, and stage hashes were frozen. No further confirmation run is authorized. Hard MoE failed its separate seam feasibility/power gate and was prospectively omitted. The system extension remains deterministic-witness-only because no powered empirical system claim was activated; activation alignment remains untested.
93. Each frozen generator world contains 40 loss probes, 40 latency probes, and 40 request trajectories with exact atom, context, outcome, focal-atom, and boundary quotas. The 256-world pilot validated those quotas, all semantic/update/fixture cases, and oracle balance at `.896875` for `J` and `.896387` for `T`; these are generator checks, not `F35/F36` results.
94. Marginal intervals for the narrative `N` plan overlap `O/S` and do not prove strict dominance. The finite-set claim is now carried by registered paired-difference certificates for loss and latency whose upper endpoints are all negative. Correlated paired evidence can certify those comparisons without converting the marginal table into a proof.
95. The binding power requirement is the 2-point in-regime guard at 4,925 independent worlds, rounded to a 100-world block and the 5,000-world cap. Frozen roles contain 20,000 train roots and 5,000 roots each for calibration, reject/router validation, system audit, and final confirmation. Train roots split 80/20 for fitting/internal selection; scorer tuning cannot use reject/router validation.
96. The frozen learner boundary is a closed 25-coordinate pre-outcome vector with fixed `J/T` normalization. The structured arm has one vector head `(center_J,radius_J,center_T,radius_T)` and the direct baseline one three-logit atom-conditioned head; both have two ReLU hidden layers, a common selected budget, at most 0.8% parameter mismatch, and a shared-prefix paired initialization whose head streams are isolated. The learner module imports no generator/oracle records.
97. The structured 200-epoch cap is prospectively divided 100/100 between center and radius phases; the radius phase freezes the trunk and restores center rows after every AdamW step. A batch contains 512 worlds and one cycling `J/T` pair per world. All 18 grid points run once per arm at selection seed 101; one common budget minimizes summed within-arm relative regret, followed by the eight registered paired final fits.
98. Held-out expansion uses one target-blind hash-selected eligible probe per schema per calibration world, sampled proportional to the joint stratum/context target weight. This produces 5,000 independent scores per schema and avoids treating correlated atom rows as exchangeable. The structured and center-only variants have distinct immutable calibration bindings; infinity counts covered for the marginal proposal estimand but forces exact `Open` for evidence use.
99. The boundary endpoint uses an explicit four-query panel at normalized near-support `.25`, supported equality, midpoint crossing, and near-refutation `.25`. Tolerance-transfer shifts the original threshold by `d sigma`; monotonic smaller-is-better semantics realize 16 schema/state/offset cells and structurally exclude eight Cartesian cells. Macro fidelity averages realized cells and reports the exclusions; it does not invent impossible states or alter registered margins.
100. Task 20 supplied the source-hashed v1 entry point; Task 20R supplied the separately versioned, differentially checked v1.1 staged path after the original high-volume evaluator failed. Task 21 ran selection, fitting, calibration, and confirmation once, producing 5,000 independent final worlds and 40,000 world/seed rows. Hard MoE remained omitted, the router remained fixed post-license masking/fallback, and system/certificate evidence remained a deterministic checked-adapter witness without a powered claim.
101. Aggregate `F35/H18.1` remains `I1` under its frozen conjunction and reverse rule, but “inconclusive” must be glossed as decisive opposing effects. The registered components receive separate evidential rows without changing the aggregate: tolerance-transfer superiority is `F35a/S1`; boundary superiority and in-regime noninferiority are `F35b/F35c/X1` at their registered margins. Direct CE's observed superiority on the latter metrics is descriptive, not a newly registered confirmatory claim.
102. `F35a` establishes no-retraining changed-tolerance generalization by the structured statistic-output interface on the frozen synthetic panel. Because the tolerance is a scorer input and the scorer is re-evaluated per query, it does not establish literal reuse of one invariant numerical region, semantic alignment, mechanistic transparency, or universal structured-learning superiority.
103. `F36/S1` concerns marginal target-in-proposal coverage only. Its success coexists with structured false-support/refutation rates near zero, support/refutation miss rates `0.4611/0.3248`, and `0.9962` target-weighted fallback mass. Marginal calibration, cautious withholding, and useful licensed coverage are distinct objectives and must be reported together.
104. Conservative dead-band geometry is the leading explanation for the boundary/in-regime deficit but is not an identified causal decomposition. `F36` does not imply pointwise proposal-endpoint overshoot; the declared threshold carries information about the oracle-relative generator construction; and an idealized hidden-intercept excess half-width ranges across the frozen scale rather than uniformly exceeding `.25 sigma`. Future protocols derive directional alternatives against generator constants and applicable theorems before freeze.
105. Checkpoint C's matched-coverage comparison requirement did not survive into Task 19's raw boundary macro-accuracy primary. The frozen endpoint remains governing, but any future conservatism study must preregister matched coverage or full risk--coverage curves. Such a study is a new versioned experiment, never a repair or rescue of v1/v1.1.
106. Deviation `21-D3` leaves target-weighted trace false assertions/misses, polarity/mode/diagnostic breakdowns, selected/deployed loss, and misroute severity unavailable. They cannot rescue or overturn the registered core. Future compact traces retain target/design weights, polarity, evidence mode, and sufficient diagnostics prospectively.
107. The seven frozen JSON artifacts whose consumers recorded CRLF raw-byte hashes are byte-preserved with `.gitattributes`; other experiment JSON retains its existing bytes. The event is an execution-environment artifact-transport erratum with no identified scientific impact. Historical source-hashed writers remain frozen, while future versions use an explicit LF or separately declared canonical serialization. Local checks are required at completion; after an authorized push, public CI must be green or explicitly explained.
108. The finite representational existence form of policy–value isomorphism survives. With a fixed injective scalar action code, deterministic policies are in bijection with code-valued functions on the same state domain; with fixed action-score encoding and decoder, the policy is likewise recovered exactly. What is refuted is the stronger claim that standard `V^pi`, `Q^pi`, or occupancy supplies a unique, natural, policy-only, or observationally identified inverse. The operational companion term is **environment-relative policy evaluation with conditional behavioral reconstruction**; it supplements rather than replaces the qualified existence result.
109. A fully declared decision process and policy induce unique standard `V^pi/Q^pi` objects under the usual finite-horizon or discounted assumptions. Greedy use of `Q^pi` (or deterministic successor `V^pi` with the correct reward/perspective bookkeeping) is generally policy improvement, not an inverse. It reconstructs the original policy only where that policy is already greedy with compatible tie-breaking.
110. State–action occupancy is a behavior distribution depending on dynamics, initial distribution, and horizon/discount. It can recover a Markov policy by conditionalization only on positive-occupancy states under the applicable regularity assumptions. State occupancy alone loses actions; neither occupancy is cardinal utility. Expected return becomes an occupancy–reward pairing only after reward is independently supplied.
111. The companion `policy_value_isomorph` evidence is pinned to remote commit `097ea8897fb203b9b3a6ceafcb29e11bdc6cdd6c`. It is an implementation witness for rollout policy evaluation, separate value/Q fitting, and conditional greedy-agreement metrics in declared games. Task 22 did not run or modify its newline-dirty local checkout, and the case study supplies no reward uniqueness, arbitrary-policy inversion, or mechanism evidence.
112. The unqualified claims that value representation must be at least as complex as policy and that improvement requires value change are refuted. Complexity can reside in dynamics, a policy, or tie-breaking while value remains constant; a fixed-objective agent can improve its model, estimator, search, or policy. Neither optional claim belongs in the public artifacts without a new scoped theorem.
113. Recursive-judgment claim `B01` is supported at a precise scope. For latent task `Z`, held-out outcome `Y`, report `J`, and nuisance context `N`, positive population improvement under a strictly proper loss over the true `N`-conditioned Bayes baseline implies `I(J;Y|N)>0`. Under log loss, improvement `delta` gives `I(J;Y|N)>=delta`; the gap equals mutual information minus the judge's expected conditional KL regret.
114. Let `K=k_N(Z)` merge latent task labels with identical `P(Y|Z,N)`. If `J` is independent of `Y` conditional on `(Z,N)`, quotient mediation and data processing give `I(J;K|N)>=I(J;Y|N)`. The theorem identifies only this outcome-relevant quotient. Non-Bayes comparators, omitted nuisance, leakage, duplicated types, or instability defeat stronger claims.
115. Calibration, repeated agreement, and recursion alone do not establish factual measurement. At recursive level `m`, the relevant increment is `I(J_m;Y|N,J_0,...,J_(m-1))`; copying supplies zero. Any empirical recursive claim requires a positive proper-score gain over the full prior-report baseline, stable task-conditioned outcomes, disjoint held-out lineage, level-specific mediation, independent evidence, and shift replication. `B02` remains future empirical work.
116. Policy/value material is not a dependency of the finite-stage calculus, representation theorems, or frozen experiment. The formal paper may state the finite representation-existence proposition and the scoped Task 22A information theorem, then use the identifiability counterexamples and conditional forward map to delimit their semantics and practical force. The author's intended bridge asks whether a value surrogate can be an informative, interpretable model-of-a-black-box policy without claiming complete transparency or a uniquely true internal utility. The companion belongs in an optional case-study section only if Task 23 supplies a useful bridge.

## 18. Specification gates after Task 22A

Tasks 7–11 resolved the broad signature, semantics, consequence/update, dominance/retention, and bridge/atlas questions. Task 11A selected mandatory profile-indexed `Lic_P`; Checkpoint A1 repaired the witness and identified theorem/executability risks; Task 11B supplied the executable kernel. Tasks 12–14A supplied continuation, compact-core, metatheory, and quantitative transport results. Task 14B then closed Checkpoint B's focused gate by proving typed locality/change-completeness and repairing the statements, citations, and executable kernel. Task 14C closed the recursive-plan gate with proof erasure, a concrete path-sensitivity certificate, root-license lifting, grounded provenance, finite-rank system assessment, and the exact Curry--Howard/self-endorsement boundaries. Tasks 15–18 fixed the query-family-specific encoding, hybrid ReLU reference realization, representation results, and structured learning/calibration proposal. Checkpoint C selected the minimum empirical core and trust boundaries. Tasks 19–20R preregistered, froze, implemented, and execution-hardened that core; Task 21 ran it once; Checkpoint C1 propagated the component-level result and public-verification erratum without reopening confirmation; Task 22 separated the supported finite policy/value representation-existence result from the refuted standard-return/identifiability strengthening; and Task 22A proved the scoped proper-score/log-loss information result with its quotient and countermodel boundaries.

Remaining gates are:

- the strongest optional transparency claim that survives the now-settled policy/value nonidentifiability, partial-information, and causal boundaries (Task 23);
- whether the limitation matrix and frozen outline turn the formal and mixed empirical record into a coherent three-to-five-contribution paper rather than an inventory (Tasks 24–25 and Checkpoint D); and
- the technical and reader audits before public formatting (Tasks 31/31A and Checkpoint E).

These are open research questions and construction targets rather than known defects in the completed core. A later task may revise a default, but it must record what evidence or formal obstacle caused the revision.

## Task conclusion

The project target is now fixed as a finite-stage logic of scoped, defeasible reliance on models under open-ended succession. The logic must formalize licenses, local consequence, revision, overlap, fallback, and abstention; the neural work must distinguish representation, learning, and transparency; and the philosophical discussion must remain neutral on whether truth is reducible to usefulness. This scope is strong enough to yield formal theorems, counterexamples, neural constructions, and experiments without requiring a final theory of truth or an infinitely capacious MLP.
