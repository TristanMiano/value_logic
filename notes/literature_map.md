# Literature Map and Citation Audit

Status: Task 6 research map  
Date: 2026-07-10  
Bibliography: [`references.bib`](../references.bib)

## Executive result

The project's exact combination appears to be novel enough to require a synthesis rather than the adoption of one existing logic. The nearest fields each solve a different part of the problem:

| Field | What it supplies | What it does not supply |
|---|---|---|
| belief revision/nonmonotonic logic | defeasible consequence, contraction/revision, defaults, preference orderings over beliefs | empirical loss, domain coverage, calibrated abstention, neural realization |
| formal learning theory | convergence with finitely many mind changes and no requirement that the learner know when convergence occurred | task-relative usefulness of theories that remain false; finite-sample calibration |
| truthlikeness/verisimilitude | formal comparison of false theories relative to a truth target | a truth-neutral reliance license; generally requires a privileged target/world metric |
| scientific structuralism/intertheory reduction | theories as structured families with applications; bridge/limit relations between theories | a trainable operational license predicate or routing architecture |
| preference/decision logic | ordered worlds/options, partial preferences, thresholds, dominance, update | evidence-based model adequacy unless coupled to statistics and tasks |
| selective prediction | explicit abstention and the risk–coverage tradeoff | retention of multiple theories, bridge relations, logical consequence |
| mixture-of-experts | learned gating and local expert specialization | guarantees that experts are adequate, interpretable, or scientifically meaningful |
| ReLU CPWL theory | finite piecewise-affine regions and exact representation results | SGD learnability, semantic alignment, infinite memory, scientific correspondence |
| differentiable/neural-symbolic logic | techniques for compiling constraints or fuzzy/probabilistic logic into differentiable computation | the proposed theory-succession semantics unless it is separately defined |
| IRL/reward identifiability | precise limits on recovering value from behavior and conditions that reduce ambiguity | universal policy–value isomorphism or mechanistic explanation from output agreement |
| provability logic | exact results about formal provability and self-reference | a ready-made semantics for empirical adequacy, open-ended inquiry, or model selection |

The most defensible positioning is therefore:

> The project combines nonmonotonic finite-stage licenses, selective risk/abstention, overlapping expert routing, and ReLU representability. Formal learning theory supplies a model of eventual stabilization without known arrival; intertheory-reduction literature supplies bridge types; IRL supplies interpretability limitations. None of these neighboring results by itself establishes the proposed calculus.

## 1. Audit method

### 1.1 Inclusion rule

An entry was added to `references.bib` only after its bibliographic identity was checked against at least one primary location: a publisher page, journal/proceedings page, author publication page, or archival record containing the original paper. DOI metadata was preferred. Search-result summaries and encyclopedias were used only to locate primary works, not as the evidentiary endpoint for technical claims.

### 1.2 Strength labels

This map uses:

- **Core:** directly constrains or supplies a formal component of this project.
- **Bridge:** supplies a useful analogy, representation, or neighboring formalism, but transfer requires an additional theorem or definition.
- **Background:** orients terminology or history; it should not carry a central technical claim.
- **Caution:** establishes an impossibility, underdetermination, or scope restriction that the project must respect.

### 1.3 Verification limits

Bibliographic verification is not theorem verification. Several inherited notes attribute stronger theorem packages than could be confirmed from metadata or abstracts alone. Such claims remain open even when the cited work is real. Later proof tasks should quote exact definitions/theorem numbers from full texts before relying on them.

## 2. Belief revision and nonmonotonic logic

### Core sources

- `AlchourronGardenforsMakinson1985` — AGM partial-meet contraction and revision. **Core** for distinguishing revision, contraction, and retained background records.
- `Reiter1980` — default logic and extensions. **Core/bridge** for defeasible conclusions whose support can be withdrawn.
- `KrausLehmannMagidor1990` — preferential models and cumulative consequence relations. **Core** for studying which weaker-than-monotonic inference properties are worth preserving.
- `GardenforsMakinson1994` — relates expectation orderings, nonmonotonic inference, and belief revision. **Bridge** to the project's comparative model orderings.
- `McCarthy1980` — circumscription. **Background/bridge** for formalizing minimal/default commitments.

### Transfer to this project

The useful inheritance is structural:

1. consequence can be defeasible without becoming arbitrary;
2. different update operations should be distinguished;
3. ordered or preferential semantics can generate nonmonotonic consequence;
4. representation theorems should connect postulates to semantic constructions.

The project should not simply identify a license with an AGM belief set. AGM operates on deductively closed theories and gives postulates for revision/contraction; the proposed system also carries empirical risk, domains, costs, evidence, libraries, and abstention. A model can be retained in the registry while its current license is defeated, so archival heredity differs from belief-set inclusion.

### Formal questions inherited

- Which KLM-style properties should finite-stage license consequence satisfy: reflexivity, left logical equivalence, right weakening, cautious monotony, cut, rational monotony?
- Does adding evidence behave like revision, while discovering a competitor behaves like preference/order revision?
- Can domain restriction be modeled as labeled consequence rather than contraction of the object-level theory?

## 3. Formal learning, convergence, and truth approximation

### Core and contrasting sources

- `Putnam1965` — trial-and-error predicates permit finitely many changes of mind. **Core** historical precursor.
- `Gold1967` — identification in the limit. **Core** for convergence in which a learner can stabilize without a finite certificate that it has stabilized.
- `Kelly1996` — logical reliability and formal inquiry. **Core/bridge** for finite stages judged by their role in an indefinitely extensible process.
- `Valiant1984` — computational learning with approximation and confidence parameters. **Bridge** to finite-sample learnability, but not a theory-succession logic.
- `Niiniluoto1987` and `Oddie1986` — formal truthlikeness. **Background/contrast** because they compare false theories relative to a truth target or world similarity.

### Central distinction

Identification-in-the-limit is the closest formal match to “the learner need not know it has reached the end.” It supports a sequence of conjectures that eventually stabilizes under stated learnability conditions. It does **not** imply that an old conjecture remains pragmatically useful on a subdomain, nor does it provide an operational `epsilon`-license.

Truthlikeness is closer to the motivating claim that false theories can be better or worse. It is not truth-neutral: it normally evaluates closeness to a true theory, actual world, or privileged state description. The present project may compare task performance without assuming that its model library contains the truth or that its loss is a metric on theories' truth content.

### Recommended use

- Use Gold/Kelly to define a meta-level sequence and distinguish eventual stability from certifiable finality.
- Use PAC-style `epsilon,delta` notation only after carefully distinguishing approximation error/confidence from the project's task tolerance `epsilon`.
- Present truthlikeness as an alternative stronger semantic project, not as a synonym for adequacy.

## 4. Scientific theories, structure, and intertheory relations

### Core and bridge sources

- `Nagel1961` — classical theory reduction. **Background** for deductive reduction and bridge principles.
- `Sneed1971` — mathematical theories as structured families with intended applications, identity/equivalence/reduction, and dynamics. **Core/bridge** for typing “theory,” “model,” and “application domain.”
- `Nickles1973` — distinguishes concepts of intertheoretic reduction. **Core/bridge** against treating every successor relation as deduction.
- `Batterman1995` — asymptotic limiting relations between physical theories. **Core/bridge** for overlap/limit relations such as relativistic-to-Newtonian regimes.
- `Butterfield2011` — separates emergence, reduction, and supervenience. **Background/bridge** warning that neighboring intertheory notions do not collapse.

### Transfer to this project

This literature strongly supports treating a theory as more than a single proposition and treating applications as part of theory use. It also supports the Task 4 decision that bridges are typed: deductive reduction, limiting relations, approximation, and empirical correspondence are not interchangeable.

It does not establish that scientific theories literally form a differential-geometric atlas, or that their applicability regions correspond to ReLU activation cells. The paper should call the scientific object an **overlapping licensed model cover** unless it later defines enough structure to justify stronger atlas terminology.

### Candidate worked examples

The literature repeatedly uses special relativity/Newtonian mechanics, wave/geometrical optics, and quantum/classical limits. Later examples must state the parameter, limiting operation, observable, norm/loss, and range over which the approximation is controlled. “Theory A reduces to theory B” is too compressed for the license calculus.

## 5. Preference and decision logic

### Core sources

- `VanDalen1974` — Rescher-style measure semantics and completeness results. **Core/bridge** for a logic with an ordered evaluative layer alongside propositional structure.
- `BoutilierEtAl2004` — CP-nets for conditional ceteris paribus preferences. **Bridge** for compact partial preferences and dominance reasoning.
- `VanBenthemGirardRoy2009` — modal ceteris paribus preference logic. **Bridge** for ordered-world semantics and interaction with Boolean structure.
- `VanBenthemLiu2007` — dynamic preference upgrade. **Bridge** for explicit changes to preference orderings.
- `VonNeumannMorgenstern1944` — expected-utility representation under lottery axioms. **Background** for when cardinal arithmetic is justified.
- `GilboaSchmeidler1989` — maxmin expected utility under non-unique priors. **Core/bridge** for robust criteria under ambiguity.
- `SeidenfeldSchervishKadane1995` — representation of partially ordered preferences by sets of expected utilities/probability-utility pairs under stated axioms. **Core** support for refusing premature scalarization.

### Audit conclusion on inherited taxonomy

The inherited post's scalar/vector/ordered-world/uncertainty taxonomy is a useful **project taxonomy**, not a canonical four-way partition established by one cited source. Different literatures place values on formulas, worlds, acts, or outcomes and define comparison differently. The paper should define each family independently and avoid saying that one consequence relation “naturally” or uniquely follows unless it proves the pairing.

The inherited claim that Van Dalen supplies a simple “soundness/completeness ladder” was not verified at theorem-level in this task. The paper exists with the stated title and metadata, but later use requires the full language, semantic classes, calculi, and exact theorem statements.

### Transfer rule

Preference formalisms can order candidate models or actions, but they do not turn performance into evidential warrant automatically. The license semantics must specify how evidence generates admissible comparisons. Conversely, the project should preserve partial order/incomparability when no justified scalarization is available.

## 6. Selective prediction and abstention

### Core sources

- `Chow1957` and `Chow1970` — decision-theoretic reject options and optimal error/reject tradeoffs in classical recognition settings. **Core** for a fallback/reject action whose cost induces a threshold.
- `ElYanivWiener2010` — selective classification and risk–coverage curves. **Core** for separating coverage from risk.
- `GeifmanElYaniv2019` — an integrated neural reject option. **Core/bridge** for jointly learned prediction and selection.

### Direct relevance to `epsilon`

This field provides the cleanest literature support for the user's status-quo intuition. If accepting a prediction and rejecting/deferring have different costs, the reject action supplies a comparison point. The resulting threshold is decision-relative, not a probability that a theory is false.

For the project, define a selective predictor as `(f,g)` where `f` predicts/routes and `g` accepts or abstains. Report at least:

- coverage `P(g(X)=accept)`;
- selective risk conditional on acceptance;
- fallback/reject cost or regret;
- calibration or coverage guarantees;
- performance under distribution shift.

### Limitation

Selective classification usually returns one label or rejects. The proposed system must additionally retain all adequate models, record overlapping licenses, and distinguish active set from selected model. Selective prediction supplies the gap behavior, not the entire atlas logic.

## 7. Mixture-of-experts and model routing

### Core sources

- `JacobsEtAl1991` — trainable gating that partitions cases among local experts. **Core/bridge** for learned specialization.
- `JordanJacobs1994` — hierarchical mixtures and EM. **Bridge** for nested routing and probabilistic gates.
- `ShazeerEtAl2017` — sparsely gated neural experts. **Background/bridge** for conditional computation and large expert libraries.
- `FedusZophShazeer2022` — simplified top-one sparse routing and training issues. **Background/caution** for load balance, capacity, and instability.

### Transfer to this project

MoE architectures demonstrate that learned gating and expert specialization are feasible. They do not make router weights epistemic licenses. Ordinary MoE routing can:

- route every input even when no expert is adequate;
- choose one expert even when several are adequate;
- specialize for optimization reasons unrelated to scientific domains;
- suffer expert collapse or load-balancing artifacts;
- hide the risk/provenance that justified the choice.

The intended architecture therefore needs an explicit null/fallback expert or accept gate, multi-license output before selection, risk calibration, and separate evaluation of routing efficiency versus license correctness.

## 8. ReLU continuous piecewise-affine geometry

### Core sources

- `MontufarEtAl2014` — linear-region complexity and depth. **Core/background** for expressivity, with architecture-dependent bounds.
- `AroraEtAl2018` — ReLU networks and piecewise-linear representation results. **Core** for finite representability.
- `HeEtAl2020` — explicit representation of general scalar CPWL functions in `R^d` by ReLU DNNs and depth/size bounds. **Core** for inherited claim F14.
- `Ovchinnikov2002` — max–min representation of piecewise-linear functions. **Core/bridge** for constructive lattice formulas.
- `ZhangNaitzatLim2018` — equivalence of feedforward ReLU networks and tropical rational maps under the paper's conventions. **Bridge** for algebraic analysis.

### Verified finite result

For ordinary finite feed-forward ReLU networks, the computed map is continuous and piecewise affine on a finite polyhedral decomposition. Conversely, cited representation results establish exact finite ReLU realizations for finite CPWL functions under their stated scalar/vector, domain, and architecture conventions. `HeEtAl2020` gives a detailed construction and an upper bound of `ceil(log2(d+1))` hidden layers for a general scalar CPWL function on `R^d` under its counting convention.

This supports a **finite representability theorem**, not the claims that:

- SGD discovers the construction;
- activation regions correspond one-to-one with scientific domains;
- the representation is parameter-efficient for every target;
- a fixed network stores an open-ended library;
- tropical paths are logical proofs.

Vector-valued CPWL maps can be handled coordinatewise, but any shared-width/depth claim must state how coordinate networks are combined.

### Tropical qualification

`ZhangNaitzatLim2018` verifies an algebraic tropical-rational-map correspondence. The inherited “best-margin proof path” interpretation remains a project hypothesis. It requires a syntax of derivations and a soundness/completeness correspondence; max-plus evaluation alone does not provide one.

## 9. Differentiable and neural-symbolic logic

### Core sources

- `XuEtAl2018` — semantic loss for Boolean constraints over neural outputs. **Core/bridge** for compiling a satisfaction target into loss.
- `BachEtAl2017` — hinge-loss MRFs and Probabilistic Soft Logic. **Core/bridge** for weighted soft constraints and convex MAP inference.
- `BadreddineEtAl2022` — Logic Tensor Networks/Real Logic. **Bridge** for differentiable many-valued first-order grounding.
- `RiegelEtAl2020` — Logical Neural Networks. **Bridge**, but cited here as a preprint and not treated as a settled theorem package.
- `RocktaschelRiedel2017` — differentiable proving via soft unification. **Background/bridge**.
- `EvansGrefenstette2018` — differentiable inductive logic programming. **Background/bridge**.
- `ManhaeveEtAl2018` — neural predicates inside probabilistic logic programming. **Bridge** for keeping symbolic and neural components distinct.
- `YangYangCohen2017` — Neural LP; the inherited author list and title were incorrect and are corrected in `references.bib`. **Background/bridge**.

### Transfer to this project

These systems establish that logical constraints, fuzzy semantics, probabilistic programs, and proof-like computations can interact with gradient learning. They do not show that minimizing any loss is itself a logic. The Task 5 minimum remains: syntax, semantics, consequence, update, metatheory, and a stated neural correspondence.

The most relevant construction patterns are:

1. keep a symbolic/typed layer and compile only specified judgments into differentiable objectives;
2. treat formula satisfaction and empirical prediction as separate loss components;
3. expose which logical semantics (Boolean, fuzzy, probabilistic, interval) a numeric output uses;
4. test constraint satisfaction separately from task accuracy.

## 10. Inverse reinforcement learning and value identifiability

### Core and caution sources

- `NgRussell2000` — foundational algorithms and the ambiguity of reward recovery from optimal behavior. **Core/caution**.
- `ArmstrongMindermann2018` — policy decomposition into reward plus planner is not uniquely inferable under unknown rationality, even with a simplicity prior. **Caution**.
- `CaoCohenSzpruch2021` — characterizes reward equivalence for entropy-regularized settings and gives conditions under which multiple discounts/environments improve identification. **Core/caution**.
- `KimEtAl2021` — necessary/sufficient reward-identification conditions in scoped MaxEnt settings. **Core/caution**.
- `SkalseEtAl2023` — invariances and partial identifiability across reward-learning data sources. **Core/caution**.
- `SmallwoodSondik1973` and `KaelblingLittmanCassandra1998` — belief-state formulations under partial observability. **Core** support for enlarging state/history when the visible state is not sufficient.

### Consequences for the companion project

The literature supports the existing caution that a policy alone does not uniquely determine a standard return-based value or reward. The companion repository avoids the most basic ill-posedness by supplying game dynamics, terminal utility, perspective, rollout convention, and a state distribution. Even then:

- multiple values/rewards can preserve the same action ordering;
- reward shaping or other transformations can preserve policies;
- output agreement does not imply shared hidden mechanisms;
- a coarse observation may need history or a belief state;
- extra environments, discount factors, interventions, or structural assumptions can improve identifiability.

Thus the strongest near-term target is a **licensed transparent surrogate**, not unique recovery of the policy's true internal value function.

## 11. Provability logic and the Löbian discussion

### Primary sources

- `Lob1955` — Löb's theorem under arithmetized provability conditions. **Core only if the project introduces an actual formal provability predicate with the required derivability conditions.**
- `Solovay1976` — arithmetical completeness of GL-style provability logic. **Background/core only for a genuine provability interpretation.**

### Audit conclusion

The inherited LLM discussion moves too quickly from finite-stage “certification” to Löbian behavior. A modal operator meaning “the current evidence licenses model M” is not automatically a formal provability predicate. Löb's theorem depends on strong self-reference and derivability conditions; Solovay's theorem concerns arithmetical interpretations of modal formulas.

Later tasks should use neutral stage modalities first. GL should be imported only if the formal license operator satisfies an explicit translation into formal provability or analogous fixed-point machinery. “Anti-Löbian open-ended refinement” is not an established named dual theorem in the cited primary literature.

## 12. Łukasiewicz and clipped-ReLU correspondences

### Verified sources

- `CastroTrillas1998` — equivalence claims between multilayer feed-forward networks with a squashing/truncated-linear setting and linear combinations of Łukasiewicz propositions. **Bridge**.
- `AmatoDiNolaGerla2002` — correspondence between rational Łukasiewicz formulas and neural networks with truncated-identity activation and rational weights. **Core/bridge** for inherited F17.

### Required qualification

The relevant activation is the clipped/truncated identity `min(1,max(0,x))`, not ordinary unbounded ReLU. Coefficient restrictions matter: integer/rational McNaughton functions correspond to particular logical languages. Therefore this literature cannot be cited as a bidirectional equivalence between arbitrary real-weight ReLU MLPs and Łukasiewicz formulas.

## 13. Inherited bibliography audit

The only pre-existing numbered bibliography was in `posts/utility_preference_logic_nn.md`. Its entries were handled as follows.

| Old no. | Disposition | Audit result |
|---:|---|---|
| 1 | omitted | SEP survey; useful orientation, but Task 6 prefers primary sources. |
| 2 | omitted | SEP survey; replaced by primary decision-theory works. |
| 3 | included | Van Dalen metadata/DOI verified; strong theorem-ladder paraphrase remains unverified. |
| 4 | omitted | Packard entry was not needed for the core map and lacked a verified DOI in this audit. |
| 5 | included | van Benthem, Girard, Roy metadata and DOI verified. |
| 6 | included | van Benthem and Liu metadata and DOI verified. |
| 7 | omitted | Real paper, but dominance-complexity details are downstream of current scope. |
| 8 | included | CP-nets metadata and DOI verified. |
| 9–10 | omitted | Real adjacent qualitative-decision papers; not needed for the minimal verified map. |
| 11–14 | partly included | Wald omitted; Gilboa–Schmeidler and Seidenfeld–Schervish–Kadane included. The inherited DOI for the latter was wrong; corrected to `10.1214/aos/1034713653`. |
| 15–21 | omitted | Adjacent preference-change, robust-optimization, elicitation, planning, and likelihood sources; none is needed to support a core Task 6 conclusion. |
| 22 | included/corrected | Logic Tensor Networks cited by its 2022 journal version and DOI, not only the 2020 arXiv version. |
| 23 | included with caveat | Logical Neural Networks retained as a 2020 preprint; do not cite it as a journal theorem. |
| 24 | included/corrected | End-to-End Differentiable Proving cited to NeurIPS 2017. |
| 25 | included/corrected | Evans–Grefenstette cited to JAIR 61 (2018), DOI `10.1613/jair.5714`. |
| 26 | included/corrected | Inherited authors/title were wrong. Correct work: Fan Yang, Zhilin Yang, William W. Cohen, “Differentiable Learning of Logical Rules for Knowledge Base Reasoning.” |
| 27 | included/corrected | DeepProbLog cited to NeurIPS 2018 with complete author list. |
| 28–29 | omitted | LDL and t-norm-learning entries were not needed; inherited metadata/title/author presentation was too uncertain for inclusion without a deeper full-text audit. |
| 30 | included/corrected | Hinge-Loss MRF/PSL cited to the 2017 JMLR version, not only arXiv 2015. |
| 31 | included/corrected | Semantic Loss cited to ICML 2018 with correct full author list and title. |
| 32 | omitted | The 2025 categorical-neural-architecture preprint is not needed for the core project and was not used to support a claim. |

The omitted items are not declared false. They are simply not carried into the verified bibliography.

## 14. Claim-ledger dispositions from Task 6

### Supported within scope (`S1`)

- **C07:** Belief states/history summaries can restore a Markov decision representation when they are sufficient statistics under the assumed POMDP model (`SmallwoodSondik1973`; `KaelblingLittmanCassandra1998`). This does not imply that every compressed history representation is sufficient.
- **D01:** There exist genuine preference-logical families using ordered worlds, conditional preference statements, or evaluative measures. The broad family resemblance is supported, but no single universal “preference consequence” is established.
- **F14:** Finite scalar CPWL maps admit exact finite ReLU representations under stated conventions; `HeEtAl2020` supplies a constructive general result and bound. The inherited conversation's unspecified architecture conventions still need normalization before a theorem is quoted.
- **F17:** A bidirectional logical/network correspondence is supported for truncated-identity networks with rational/integer coefficient restrictions, not arbitrary ordinary ReLU networks (`CastroTrillas1998`; `AmatoDiNolaGerla2002`).

### Checked but still inconclusive (`I1`)

- **D02:** The four-way semantics/consequence pairing is a useful synthesis, but “naturally pair” is not a verified theorem and should be restated as a design taxonomy.
- **D03:** The Van Dalen paper and its completeness focus are verified bibliographically, but the inherited “ladder” formulation needs full theorem-level verification.
- **F16:** The tropical rational-map correspondence is supported (`ZhangNaitzatLim2018`); the proof/license-path interpretation is not.
- **E09:** Löb and Solovay results are real and precise, but they do not transfer to empirical license modalities without derivability/fixed-point assumptions.

## 15. Priority reading order for later tasks

### Before Tasks 7–11 (signature, semantics, consequence, update)

1. `AlchourronGardenforsMakinson1985`
2. `KrausLehmannMagidor1990`
3. `GardenforsMakinson1994`
4. `VanDalen1974`
5. `ElYanivWiener2010`
6. `Sneed1971`, especially theory identity, applications, reduction, and theory dynamics

### Before Tasks 12–14 (limits, reflection, atlases)

1. `Gold1967`
2. `Kelly1996`
3. `Batterman1995`
4. `Nickles1973`
5. `Lob1955` and `Solovay1976` only if a genuine provability operator survives formalization

### Before Tasks 15–18 (neural representation and objectives)

1. `HeEtAl2020`
2. `Ovchinnikov2002`
3. `MontufarEtAl2014`
4. `XuEtAl2018`
5. `BachEtAl2017`
6. `GeifmanElYaniv2019`
7. `AmatoDiNolaGerla2002` for the clipped-ReLU contrast

### Before Tasks 22–23 (policy/value interpretability)

1. `NgRussell2000`
2. `CaoCohenSzpruch2021`
3. `SkalseEtAl2023`
4. `ArmstrongMindermann2018`
5. `KaelblingLittmanCassandra1998`

## 16. Research gaps and likely contribution boundary

No audited source combines all of the following in one formal object:

- an evidence- and task-indexed adequacy license;
- a fallback-induced or externally imposed tolerance;
- an overlapping, possibly incomplete cover of model domains;
- simultaneous retention of all adequate models before selection;
- defeat by both new evidence and new competitors;
- an extendable finite-stage registry without finality certification;
- an information-preserving ReLU realization with abstention and provenance;
- graded interpretability tests tied to policy/value reconstruction.

That conjunction is the plausible contribution. Novelty must be stated carefully: each component has close precedents, and the project must contribute a precise composition, theorem, or empirical result—not merely new names for existing pieces.

## Task conclusion

Task 6 establishes a verified primary-source bibliography and a division of intellectual labor among neighboring fields. The strongest immediate foundations are AGM/KLM for revision and defeasible consequence, Gold/Kelly for convergence without known arrival, selective prediction for fallback and abstention, MoE for routing, CPWL theory for finite ReLU representation, intertheory-reduction work for bridge types, and IRL for nonidentifiability constraints. Preference and differentiable logics supply design patterns, while truthlikeness and provability logic are optional stronger frameworks whose assumptions must not be imported silently.
