# Checkpoint A: Finite-Stage Foundations and Revised Roadmap

Status: completed roadmap audit  
Date: 2026-07-11  
Scope: Tasks 7–11 and all unfinished work after Checkpoint A  
Control file: [`TODO.md`](../../TODO.md)

## Executive decision

Tasks 7–11 produced a coherent **family** of finite-stage objects, but not yet one publication-ready core calculus. The shared spine is strong enough to justify continuing:

```text
typed model/domain/task/risk records
-> target, empirical, and certified adequacy
-> four-way operational assessment
-> labeled local reliance rather than truth detachment
-> append-only history with nonmonotone current warrants
-> explicit fallback and gaps
-> overlapping local model scopes
-> explicitly represented comparison, routing, and archival factors.
```

The principal unresolved ambiguity is now precise. Task 8's unqualified full `Lic` includes search-relative comparative admissibility—no certified dominator—while Tasks 10–11 distinguish an older model's continued adequacy, possible use under another purpose/profile/subdomain, nonselection, and archival retention after comparative supersession. If `Lic` means basic permission to rely, discovery of a better model need not erase it. If `Lic` means preferred current use, the existing Task 8 conjunction may be reasonable while a different judgment names residual adequacy/usability. A third option is one parameterized license whose requirement profile states whether comparison is required. The checkpoint does not decide among these.

Therefore the roadmap receives one immediate repair item, **Task 11A**, before open-endedness:

> Compare coherent license/comparison factorizations, choose and justify one canonical interface, and construct an integrated finite witness model that exercises continued old-model use, nonselection, and retention without conflating them.

After this repair, Task 12 may analyze open-endedness. No completed task is marked undone; Task 11A prospectively reconciles their interfaces.

The roadmap is otherwise preserved but narrowed. The minimal core/metatheory will not attempt to contain every certificate mode, Pareto extension, domain-splitting construction, bridge type, atlas operation, or policy/value claim. Those remain typed extensions and case studies. The ReLU work must target the surviving core judgments rather than the entire record system.

## 1. Evidence considered

This checkpoint reviewed the project control/specification and the artifacts accumulated through Task 11:

- [`TODO.md`](../../TODO.md), including the checkpoint protocol, remaining task queue, and decision log;
- [`notes/project_spec.md`](../project_spec.md), including success/failure criteria, terminology, non-goals, and paper architecture;
- [`notes/claim_ledger.md`](../claim_ledger.md), including scoped `S1`, `I1`, and `X1` dispositions and required falsification-impact analysis;
- [`notes/motivation_pi_epsilon.md`](../motivation_pi_epsilon.md), especially the direct versus pragmatic derivation of `M,D,L,epsilon` and fallback-induced thresholds;
- [`notes/representation_layers.md`](../representation_layers.md), especially information-loss and signed-margin constraints;
- [`notes/atlas_questions.md`](../atlas_questions.md), especially the three-geometries distinction;
- [`notes/literature_map.md`](../literature_map.md) and [`references.bib`](../../references.bib), especially AGM/KLM, formal learning, selective prediction, intertheory relations, CPWL/ReLU results, IRL limits, and the Löb/GL warning;
- [`formalism/01_signature.md`](../../formalism/01_signature.md);
- [`formalism/02_license_semantics.md`](../../formalism/02_license_semantics.md);
- [`formalism/03_consequence_update.md`](../../formalism/03_consequence_update.md);
- [`formalism/04_dominance_retention.md`](../../formalism/04_dominance_retention.md);
- [`formalism/05_atlas.md`](../../formalism/05_atlas.md).

The review compared these artifacts with the required final outputs: one formal Gist-compatible paper and one low-LaTeX, non-Markdown Substack adaptation.

## 2. What is coherent and should be retained

### 2.1 Stable type boundary

The many-sorted signature successfully prevents the major category errors inherited from the motivating conversations:

- instantiated models are not theory families;
- domains are not merely sets or neural regions;
- point losses are not domain risks;
- `epsilon` is not probability of falsity;
- evidence estimates are not target risks;
- model libraries are not the model universe;
- provenance is not a scalar confidence score;
- router selection is not model identity.

`EvalSpec(D,L,rho)` and the typed risk/tolerance order should survive into the core, although the minimal calculus should introduce the scalar case first.

### 2.2 Four-way assessment

The distinction

```text
Granted / Refused / Withheld / Undefined
```

is central and should remain. It realizes the user's claim discipline inside the semantics:

- contrary evidence can refuse a claim;
- missing or invalid support withholds it;
- type/interface failure makes it undefined;
- none of these automatically means “the theory is false.”

This four-way output is also a major neural/interpretability target. A binary license label would erase the project's most useful epistemic distinction.

### 2.3 Labeled consequence

Task 9's separation among model-local object consequence, fixed-stage typed consequence, and current defeasible consequence is coherent. Classical reasoning may remain local. The conclusion of applying a current warrant is labeled `MayUse`, `LicensedOutput`, or `MayRely`, not an unindexed truth claim. This gives a clean non-explosion result without pretending that every scientific theory shares one global object language.

### 2.4 Historical heredity and current nonmonotonicity

Raw event history can grow monotonically while admissible evidence, certificates, current warrants, comparative status, and routing change nonmonotonically. Strong rebuttal and evidential lapse are correctly separated. This is both philosophically relevant and operationally implementable through dependency-directed recomputation.

### 2.5 Fallback and gaps

The project now has a precise reason for `epsilon` and for abstention. Basic reliance is assessed against a named fallback/status quo as well as any external hard tolerance. Empty active sets force fallback, deference, information gathering, or abstention. This should remain in the minimal core and the decisive experiment.

### 2.6 Retention and comparison

Task 10 correctly falsified the unrestricted claims that partial domination automatically causes a split and that every retained set is a Pareto frontier. It also supplied the surviving structure:

- target dominance versus certified dominance;
- scalar versus Pareto profiles;
- unknown comparison versus target incomparability;
- archive, hard-adequacy, frontier, and selection retention;
- conditional, distribution-aware splitting.

These are valuable results. The checkpoint does not remove them; it moves most multi-objective and splitting machinery outside the smallest core.

### 2.7 Licensed cover and atlas distinctions

Task 11 gives a coherent extension for overlapping charts, gaps, bridges, seams, and routing. The formal term should be `licensed model cover` in the core paper. `Scientific licensed atlas` is acceptable for the richer structure and motivational prose. Literal differential-geometric atlas language remains conditional on axioms not generally present.

The scientific cover, router partition, and ReLU activation complex must remain separate. The hard-router discontinuity counterexample is especially important for later representation claims.

## 3. Principal integration repair

### 3.1 The current ambiguity

Task 8 fixes:

```text
Lic = CertAdeq
      AND CertImproveOverFallback
      AND ConstraintOK
      AND SearchAdmissible
      AND TraceOK.
```

Task 10 then distinguishes:

```text
HardRetained
FrontierRetained
SelectedNow
ArchiveRetained.
```

Under the Task 8 definition, a newly discovered dominator removes the older model's full `Lic`, even if it remains adequate, beats its fallback, satisfies every hard constraint, and remains useful under a different comparison profile. This makes “license” mean “currently competitively preferred,” not merely “presently warranted for reliance.” Several earlier motivational and atlas passages use “licensed” in the weaker sense.

### 3.2 Candidate interfaces to compare

One natural candidate is a layered hierarchy:

```text
CertAdeq(e;q,epsilon,alpha|R)

UseWarrant(e; q,epsilon,alpha,F,Delta,c,p | R)
  = certified adequacy
    + certified fallback improvement
    + hard constraints
    + trace/provenance

CompareStatus(e;D,g,K,sigma|R)
  = Dominated / UndefeatedRelative / CertifiedUndominated
    / Incomparable / Unknown / Undefined

PreferredUse(e;...)
  = UseWarrant(e;...)
    + the comparison status required by a named selection policy

SelectedNow(e,x,pi)

ArchiveRetained(e).
```

Task 11A must compare at least three options:

1. **Layered:** `Lic`/`UseWarrant` excludes comparative preference, which is a separate `PreferredUse` judgment.
2. **Parameterized profile:** `Lic_P` takes a requirement profile `P`; some profiles require only adequacy/fallback/hard constraints, while stronger profiles also require a comparison condition.
3. **Strong license:** `Lic` means comparatively preferred current use, while residual adequacy, usefulness, availability, or fallback suitability receives a different name.

The choice should be evaluated by semantic clarity, normative interpretation, continued use of older models under changed purposes/profiles/subdomains, update behavior, consequence rules, neural target complexity, and public readability. No option is preferred merely because one earlier artifact used its vocabulary.

### 3.3 Search closure correction

`NoCertifiedDominatorFound` is a finite search report, not positive proof of target undominated status. Task 11A must preserve both:

```text
UndefeatedRelative(E_sigma)
CertifiedUndominated(E_sigma).
```

Unknown pairwise comparisons can coexist with the first but not the second. The core must not use one unqualified predicate `Admissible` for both.

### 3.4 Integrated finite witness

The foundations currently have many separate examples but no one small structure showing that all main layers can coexist. Task 11A must build a finite witness with:

- at least three model/use plans and an explicit fallback;
- overlapping scopes and one certified gap;
- two simultaneously adequate/usable models on an overlap under at least one candidate profile;
- one comparison change whose consequences differ under the candidate interfaces;
- one case where the older model remains actually used under another purpose/profile/subdomain and one where it is only retained;
- one `Withheld` and one `Undefined` request;
- new evidence causing a lapse and separate evidence causing refusal;
- a later model causing comparative supersession;
- one unresolved comparison;
- one conditional split that succeeds and one proposed split that is withheld;
- an exact/approximate bridge plus one unknown or incompatible bridge;
- reconstructible provenance and historical events.

This model should expose contradictions among definitions before the core calculus freezes.

## 4. Minimal core versus extensions

### 4.1 Recommended minimal core

Task 13 should begin from the following smallest plausible publication core:

1. typed `Model`, `Domain`, scalar `EvalSpec`, tolerance, fallback, finite record, and stage;
2. an abstract valid-certificate interface rather than every statistical interpretation internally;
3. four operational statuses;
4. `CertAdeq` and the Task 11A-selected license/use-status interface;
5. labeled `MayRely` consequence with no truth detachment;
6. append-only raw history and current-view update;
7. rebuttal versus lapse;
8. active usable/licensed sets under the selected interface, gaps, and mandatory fallback;
9. explicit finite relative comparison status and its chosen relationship to licensing/use;
10. extendable finite-stage semantics with no built-in finality claim.

### 4.2 Typed extensions

The following remain part of the project but need not appear in the minimal proof calculus:

- vector/partial-order risk and Pareto frontiers;
- near-best, lexicographic, diversity, and exploration policies;
- distribution-aware local splitting;
- branch merge protocols;
- the full bridge taxonomy and gluing/cycle machinery;
- continuous mixtures and bridge models;
- every frequentist/Bayesian/conformal certificate instantiation;
- dynamic/causal domain reconstruction;
- policy-to-value reconstruction and recursive judgment;
- full provenance-DAG implementation details.

The paper can present selected extensions after the core theorem package. This prevents the formal contribution from becoming a catalog of records with no tractable metatheory.

## 5. Missing countermodels and proof obligations

### 5.1 Needed before the core freeze

Task 11A must add or consolidate countermodels for:

1. the different consequences of comparative defeat under each Task 11A candidate interface;
2. `UndefeatedRelative` not implying `CertifiedUndominated`;
3. unknown comparison not implying dominance or non-dominance;
4. one integrated example realizing all four operational statuses without contradiction.

### 5.2 Needed in Task 12

Open-endedness needs continuation countermodels, not rhetoric:

- a finite stage compatible with one continuation that stabilizes and another that later changes;
- an extendable sequence that eventually stabilizes without the agent knowing the stabilization time;
- an extendable sequence that changes infinitely often;
- a finite library whose relative optimum is defeated by an admissible future model.

These show that extendability, convergence, known convergence, and final truth are distinct.

### 5.3 Needed in Task 14

The metatheory must separate genuinely proved results from consequences that hold merely by definition. At minimum it should settle:

- soundness of the explicit core inference rules against the core semantics;
- status functionality/exclusivity;
- non-explosion of differently labeled local disagreement;
- tolerance monotonicity under an inclusion-preserving acceptable region;
- safe fallback on gaps;
- raw-record heredity without current-warrant monotonicity;
- conservative-update persistence;
- the exact effect of purely comparative defeat on every judgment selected by Task 11A;
- failure of unrestricted rational monotony;
- failure of global closure from finite search;
- the strongest non-finality/non-certifiability result justified by Task 12.

The distributional split theorem should remain an extension theorem unless Task 14 can prove something stronger than “if every child certificate and reconstruction condition holds, the child warrant holds.”

### 5.4 Existing countermodels retained

The following completed results remain useful and should be imported rather than reproved informally:

- expected-risk restriction can fail on a subset;
- raw heredity does not imply current-license monotonicity;
- branch-merge licenses are not the union of branch licenses;
- partial domination does not justify total adequacy revocation;
- risk supersession does not imply subdomain or full-vector supersession;
- activation/chart alignment need not be bijective;
- hard routed affine experts need not equal one continuous ReLU output;
- signed indexed margins preserve active sets while argmax does not.

## 6. Literature dependency audit

### 6.1 No blocking new literature task before Task 12

The primary-source map is adequate for the next formal steps. The new core results can be proved from project definitions. No additional literature search is required before Task 11A or Task 12.

### 6.2 AGM/KLM

AGM and KLM remain structural comparisons. The project has not established a representation theorem identifying its record/update system with AGM revision or its current consequence relation with a standard KLM class. The public paper may compare properties but must not inherit representation or completeness theorems without matching hypotheses.

### 6.3 Formal learning

Gold/Kelly-style convergence without known arrival is relevant to Task 12. It does not itself prove the project's non-finality theorem. Task 12 should define its own continuation semantics first and then cite formal learning as precedent.

### 6.4 Provability logic

Löb/GL is not part of the planned core. A stage-local empirical warrant operator has not been shown to satisfy arithmetized derivability or fixed-point conditions. Task 12 should include at most a short rejection/audit unless it independently constructs a genuine provability translation. “Anti-Löbian” should not appear as a theorem name.

### 6.5 Selective prediction

Selective prediction remains the closest precedent for fallback, coverage, and abstention. Exact risk–coverage results should be verified when Task 18 chooses objectives and Task 21 reports metrics.

### 6.6 CPWL/ReLU

Task 17 still needs precise primary-theorem statements and architecture conventions. It must additionally include the completed hard-routing discontinuity limitation, which prevents a blanket identification of the routed atlas with one ordinary ReLU output.

### 6.7 Physics/intertheory example

The low-speed kinetic-energy bridge is mathematically self-contained. Before publication, Task 31 should add an authoritative citation for the physical formulas/context if the example remains. A second historical physics case is not required now; Task 25 should add one only if the final motivational burden cannot be carried by the kinetic-energy example plus a synthetic model.

## 7. Course corrections adopted

### 7.1 Add Task 11A

Add an immediate finite-stage integration task before open-endedness. Its output will be `formalism/05a_integration.md`.

### 7.2 Narrow Task 12

Task 12 will define stage/refinement/continuation semantics and distinguish:

```text
current grant
eventual stability
known/certified stability
semantic finality
truth, if introduced only at the metalanguage.
```

Its main target is a conditional non-certifiability result under explicit live-alternative/indistinguishable-continuation assumptions. It must also show that mere extendability is compatible with both stabilization and endless change. GL is excluded unless a genuine translation is proved.

### 7.3 Narrow Task 13

Task 13 must freeze one small core syntax/semantics/proof system and classify all other machinery as extensions. It must use the Task 11A-selected interface and include a theorem-dependency graph distinguishing definitions, lemmas, and conjectures.

### 7.4 Strengthen Task 14's audit role

Task 14 must prove or refute the actual core rule package, not restate earlier conditional constructions. Invalid goals are to be weakened with countermodels and propagated into the claim ledger with project-impact statements.

### 7.5 Refocus Tasks 15–18

The neural blueprint should encode the minimal core first:

- candidatewise structured inputs and external registry pointers;
- predicted risk/certificate validity and signed component margins;
- four-way status outputs;
- multi-label adequate/usable sets under the selected semantics;
- comparison/use-status outputs in either separate or requirement-profile form, as chosen after Task 11A;
- fallback/abstention;
- reason and provenance references.

Dimensionless log physics coordinates, perturbative omitted-correction vectors, full pairwise bridge matrices, and nested model-building choices become optional extensions, not mandatory architecture inputs.

### 7.6 Refocus Tasks 19–21

The decisive synthetic experiment must generate its semantic domains independently of the trained network and include:

- simultaneous adequate/usable models under the selected interface;
- certified gaps and unknown applicability;
- all four statuses;
- fallback-induced and external thresholds;
- later evidence causing lapse versus refusal;
- later model addition causing comparison/selection change while distinguishing continued use, nonselection, and archival retention under the chosen semantics;
- exact/approximate/incompatible or unknown overlap relations;
- at least one failed split or distribution-shift case;
- separate active-set, routing, calibration, coverage, and activation-alignment metrics.

Activation-region alignment is one empirical question, not the sole success criterion.

### 7.7 Keep policy/value work optional to the core

Tasks 22–23 remain because transparency is an explicit project goal. They are not dependencies of the core logic or ReLU representation theorem. Task 22 must decide whether policy/value material belongs in the formal paper, only in the motivating post, or in a companion/future-work section. Task 23 proceeds as an explicitly conditional case-study design, not evidence for a universal policy–value isomorphism.

### 7.8 Expand limitations and claim freeze

Task 24 must include the resolved license/comparison relationship and rejected alternatives, unknown-comparison scaling, certificate-mode mismatch, pairwise bridge complexity, atlas metaphor limits, and continuous-ReLU versus hard-routing mismatch. Task 25 must freeze a core claim set and a separately labeled extension/case-study set.

## 8. Rejected roadmap changes

### 8.1 Do not discard the finite-stage formalism

The central structure is coherent and has already exposed useful counterexamples. The issue is overbreadth and one unresolved judgment-interface ambiguity, not failure of the project question.

### 8.2 Do not make Pareto dominance the core logic

Pareto analysis is valuable but not forced by the motivating question. A scalar minimal core plus a typed product-order extension gives a cleaner theorem target.

### 8.3 Do not make bridge/gluing machinery mandatory for every chart overlap

Bridge obligations depend on operation. The minimal core only needs typed local scopes and a no-transport-without-witness rule. The richer bridge taxonomy stays as an extension.

### 8.4 Do not adopt GL or an “anti-Löbian” calculus by analogy

No derivability translation has been established. Continuation semantics is sufficient for the non-finality question.

### 8.5 Do not add a second physics case yet

The existing kinetic-energy example is rigorous and appropriately narrow. Additional historical claims would create citation and commensurability work before the core is stable.

### 8.6 Do not begin implementation before Checkpoints B and C

The architecture should follow the proved core and a coherent neural blueprint. Early code would freeze the current judgment ambiguity into labels and output heads.

### 8.7 Do not remove the policy/value work

It remains important to the user's interpretability goal, but it is explicitly decoupled from formal validity of the main calculus.

## 9. New risks

### 9.1 Formalism sprawl

The five foundation files exceed six thousand lines. Without a minimal core, the final paper could become a taxonomy rather than a logic with results. Task 13 owns the compression.

### 9.2 Definitional theorem inflation

Several “theorems” are immediate from definitions. These are useful sanity checks but cannot carry the whole formal contribution. Task 14 must distinguish nontrivial results, representation results, and countermodels from definitional consequences.

### 9.3 Statistical-mode overload

Frequentist, Bayesian, conformal, deterministic, and empirical-only certificates cannot share one unqualified soundness theorem. The core should use an abstract validity interface; instantiations retain their modal interpretations.

### 9.4 Variable-library and pairwise scaling

Model-indexed heads and pairwise dominance/bridge matrices scale with library size, potentially quadratically. Tasks 15–16 must distinguish a fixed finite baseline from a shared candidate scorer plus external registry, sparse retrieval, or on-demand pair comparisons.

### 9.5 Unknown-state calibration

`Withheld` and `Unknown` require missingness, certificate validity, and out-of-scope examples—not just ordinary labels. The synthetic generator must make these states identifiable without data leakage.

### 9.6 Semantic circularity

If domains are defined from the trained score and then score/domain alignment is measured, success is tautological. Experiment domains must be supplied independently from the network.

### 9.7 Interpretability overclaim

Exposed margins and chart labels improve inspectability but do not establish causal/mechanistic alignment. Policy/value reconstruction remains underdetermined without interventions and environment assumptions.

### 9.8 Public-artifact scope

The formal paper and Substack post cannot carry every extension at equal depth. The final outline must distinguish core contribution, formal extensions, empirical demonstration, and speculative interpretive motivation.

## 10. Revised pending roadmap

Every unfinished item was re-evaluated:

| Item | Decision | Revised role/dependency |
|---|---|---|
| Task 11A | **Add; immediate next** | Compare layered, parameterized-profile, and strong-license interfaces; select one by explicit criteria; build an integrated finite witness before long-run semantics. |
| Task 12 | **Narrow** | Continuation/refinement semantics; stabilization versus known stability/finality; conditional non-certifiability; no GL without translation. Depends on 11A. |
| Task 13 | **Narrow** | Freeze the smallest core and classify Pareto/splitting/bridges/statistical modes as extensions. Depends on 11A–12. |
| Task 14 | **Strengthen/audit** | Prove or refute core rules and nontrivial results; include countermodels; avoid presenting definitional consequences as the full metatheory. |
| Checkpoint B | **Keep** | Reassess neural targets against the actually proved core. |
| Task 15 | **Refocus** | Encode minimal records/status/margins and external pointers first; analyze variable-library and pairwise-scaling costs; exotic physics encodings optional. |
| Task 16 | **Refocus** | Candidatewise ReLU scorer with four-way status, usable-set, comparison/use-status, fallback, and trace outputs under the Task 11A design; fixed finite baseline plus expandable-registry design. |
| Task 17 | **Strengthen** | Verify CPWL representation, threshold conventions, and finite constructions; include hard-router discontinuity and external-argmax limitations. |
| Task 18 | **Refocus** | Choose a structured/multitask objective and a comparison baseline; plain softmax remains only a baseline. Include calibration/selective coverage. |
| Checkpoint C | **Keep** | Require one implementable, falsifiable neural blueprint before experiment design. |
| Task 19 | **Strengthen** | Independent semantic generator with four statuses, overlap/gap/unknown, lapse/refusal, comparison-driven status changes, continued-use versus archive-only cases, bridge states, and failed split/shift cases. |
| Task 20 | **Keep, scoped** | Implement only the Checkpoint C blueprint; retain readability, tests, deterministic configuration, and machine-readable traces. |
| Task 21 | **Strengthen** | Measure component/status calibration, active-set set fidelity, risk–coverage, routing, update/retention, failure cases, and activation/domain alignment separately. |
| Task 22 | **Narrow/gate** | Audit policy/value and recursive judgment; explicitly decide main-paper versus post/future-work status. Not a core dependency. |
| Task 23 | **Keep conditionally** | Design interpretability bridge only at the strength surviving Task 22; separate behavioral, representational, causal, and human-facing grades. |
| Task 24 | **Expand** | Consolidate formal and neural counterexamples, including warrant/preference ambiguity, unknown comparisons, certificate modes, scaling, atlas limits, and routing discontinuity. |
| Task 25 | **Strengthen** | Freeze a core claim set plus separately labeled extensions/case studies; include theorem dependency and evidence-grade maps. |
| Checkpoint D | **Keep** | Decide whether the core alone warrants publication and whether optional material should be cut. |
| Task 26 | **Revise emphasis** | Motivation/related work must introduce the repaired judgment hierarchy and use `licensed model cover` as the formal term. |
| Task 27 | **Revise structure** | Present the minimal core first; Pareto, splitting, and bridge/atlas machinery as explicit extensions. |
| Task 28 | **Keep, narrow to settled results** | Include genuine proofs and countermodels only; move routine sanity checks to appendix if needed. |
| Task 29 | **Revise emphasis** | Present structured outputs, external registry, representability/learnability/alignment separation, and optional policy/value case study. |
| Task 30 | **Keep, strengthen failure reporting** | Report four-way/status failures, unknown/gap behavior, retention, calibration, alignment, and limitations. |
| Task 31 | **Keep** | Full symbol/proof/citation audit; enforce claim-ledger project-impact propagation for every falsification. |
| Checkpoint E | **Keep** | Publication gate after the full audit. |
| Task 32 | **Keep** | Gist/Markdown/math compatibility only after claims stabilize. |
| Task 33 | **Keep** | Plain-text Substack adaptation derived from the audited paper. |
| Task 34 | **Keep** | Claim-by-claim cross-format finalization and resume-state update. |

## 11. Claim-ledger impact

No new inherited claim is marked `X1` by this checkpoint. The audit confirms and propagates the two existing falsifications:

- E06's automatic-split clause requires conditional `SplitReady` replacement;
- E07's universal Pareto-retention clause requires archive, adequacy/use status, frontier, and selection to remain distinguishable, whether as separate predicates or fields/profiles of one judgment.

The newly identified `Lic` ambiguity is not itself an inherited empirical/formal claim adjudication. It is an open interface choice among project definitions, so it generates Task 11A rather than an `X1` ledger row. If Task 11A proves that one candidate design cannot satisfy the retained requirements, the affected claim must then receive a scoped disposition and project-impact statement.

## 12. Revised next task

The next task is:

> **Task 11A — Resolve the finite-stage license/comparison interface and build an integrated witness model.**

Checkpoint A stops here and does not begin that task.
