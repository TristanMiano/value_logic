# Counterexamples and Limitations: Paper-Selection Matrix

Created: 2026-07-18
Task: TODO Task 24
Status: publication-facing boundary synthesis after Tasks 22--23 and Checkpoint C1

## Executive selection

This note selects the limitations that materially shape the paper. It is not a
list of every caveat in the repository and it is not a table assigning final
truth values to broad research ideas. A counterexample here has a constructive
job: it identifies an inference that the current premises do not support, then
points to the additional condition or narrower object for which a useful result
is available.

The public paper should foreground seven boundary families:

1. a finite-stage grant concerns one versioned request; it does not settle
   permanent stability, global search closure, or semantic finality;
2. a checked record supports a target-world conclusion only through its named
   mode, checker, version, scope, and soundness bridge;
3. finite recursive composition is constructive when evidence is grounded and
   dependencies are ranked; unrestricted cycles require a separately defined
   semantics;
4. exact ReLU representability is distinct from learnability, semantic
   alignment, and the conditional dual use of named activations;
5. calibrated proposals can be operationally unhelpful when withholding and
   fallback dominate;
6. routed and shifted performance requires coverage, severity, fallback, and
   trace information in addition to local accuracy; and
7. policy/value results provide scoped representations and environment-relative
   evaluations. The project makes no claim about the existence of a policy's
   true utility or its recovery.

Rows marked **main** should be stated where the corresponding positive result
is introduced. Rows marked **appendix** preserve exact constructions and
assumptions without interrupting the argument. Rows marked **future** describe
work whose positive evidence is not in the present repository. Equivalent
caveats appear once below and are cross-referenced rather than renamed.

## 1. How to read a boundary row

The phrase “assumption exposed” names the premise required by a stronger
inference. The witness column records a theorem hypothesis, finite
counterexample, executable regression, or empirical result showing why that
premise matters. Three kinds of conclusion must remain linguistically distinct:

- **established at scope:** the stated hypotheses construct or imply the
  conclusion;
- **not established here:** the project has supplied no result about the
  neighboring proposition, which remains open at this scope; and
- **separated by a witness:** the displayed premises can hold while the proposed
  conclusion fails, so that particular implication needs repair.

Publication prose should avoid compressing the first two into “X, not Y.” A
clearer form is: “The construction establishes X. The project makes no claim
about Y,” or “The current experiment did not measure Y.” A witness against one
formal strengthening also should not be narrated as a universal negative about
every possible formalization.

The **project impact** column answers whether the boundary changes the core
calculus, its neural realization, the empirical interpretation, or an optional
motivation. “Core-bounding” means that the condition belongs beside the
positive theorem; it does not mean that the project goal has failed.

## 2. Finite scope and search

| ID | assumption exposed | constructive witness | surviving result | project impact | paper placement |
|---|---|---|---|---|---|
| `L24-F1` | A current grant is sometimes read as a certificate of permanent stability or finality. Such a reading needs frozen dependencies or restrictions on compatible continuations. | [`06_open_endedness.md`](../formalism/06_open_endedness.md), Theorems 1--5 and Countermodels 9.1--9.5: one finite state can have a grant-preserving continuation and a later-changing continuation; a frozen proof-backed request can nevertheless be certified stable. | `Assess(s,e,q,P)` is a complete finite-stage assessment. Deterministic stability is constructible under a checked freeze invariant, and statistical stabilization is available under simultaneous coverage, shrinkage, and nonzero margin. | Core-bounding. It preserves the reliance-before-finality thesis while preventing a stage result from becoming a metaphysical conclusion. | **Main**, scope paragraph beside continuation semantics; exact witnesses in **appendix**. |
| `L24-F2` | “No evaluated candidate dominates `e`” implies global or future undominatedness only if the search universe is closed or a stronger certificate covers it. | [`08_metatheory.md`](../formalism/08_metatheory.md), Theorem 23 and Countertheorems 24--25, and [`03_representation_theorems.md`](../ml/03_representation_theorems.md), Theorem 5: two continuations agree on finite `K`, while one adds a certified dominator. | `RelUndom` is relative to the exact evaluated set and search trace; `CertUndom` records the stronger finite certificate required by its profile. Shared candidate scoring can query variable finite registries without implying global closure. | Core-bounding and neural-interface-bounding. Exact library/search identity remains part of the diagnostic. | **Main**, one countermodel beside finite comparison; implementation details in **appendix**. |
| `L24-F3` | Component grants compose automatically. A composite conclusion additionally needs interface compatibility and a grade/certificate transformer valid for the whole plan. | [`08c_proof_carrying_plans.md`](../formalism/08c_proof_carrying_plans.md), Theorem 1, Corollaries 2--3, and Countertheorem 4: two components each have error `0.06` at tolerance `0.10`, while their same-direction composite error is `0.12`. | Finite typed plan DAGs construct payload, grade, certificate, and provenance together; a checked root certificate can then support the composite request. | Core-bounding. The positive proof-carrying construction survives and component status remains useful explanatory data. | **Main**, compact counterexample beside composition theorem; path arithmetic in **appendix**. |
| `L24-F4` | A fixed finite neural interface covers an open-ended library or an arbitrary future query family. | [`03_representation_theorems.md`](../ml/03_representation_theorems.md), Propositions 5--6: a fixed indexed output has no coordinate for a new candidate; a shared scorer is equivariant over externally supplied finite registries. | The architecture supports fixed finite query families and candidate-conditioned scoring over each supplied finite registry. An expandable exact registry remains external. | Neural-interface boundary. It motivates the hybrid registry/scorer design and does not constrain every possible growing system. | **Appendix** with one sentence in the neural scope paragraph. |

## 3. Evidence, calibration, and trusted bases

| ID | assumption exposed | constructive witness | surviving result | project impact | paper placement |
|---|---|---|---|---|---|
| `L24-E1` | An accepted stage record entails its target-world claim without an explicit evidence-to-world relation. | [`08_metatheory.md`](../formalism/08_metatheory.md), Theorem 15 and Countertheorem 16: the same finite state is paired with two worlds in which the target adequacy fact differs. | Soundness is a mode-scoped schema over `<W,S>`. A grant remains a usable operational conclusion when the named bridge assumptions hold. | Central philosophical and formal boundary. It protects the pragmatic interpretation from both truth inflation and blanket skepticism. | **Main**, immediately after the central judgment; formal schema in **appendix**. |
| `L24-E2` | The task loss, a learned model of that loss, and the optimizer's training objective are interchangeable; alternatively, every evaluator must terminate in one universal unmodeled loss. | [`07_core_calculus.md`](../formalism/07_core_calculus.md), §2.1, [`08_metatheory.md`](../formalism/08_metatheory.md), Proposition 29, and the finite plan construction: `L_q` is fixed by the request while an estimator `e_L` can receive a higher-order request. | Any finite well-founded tower of loss/consequence estimators is typed constructively. Its target criteria, learned estimates, training losses, and supporting evidence remain distinct. The project does not propose a universal terminal loss. | Core-bounding, with direct relevance to recursive models. It replaces a regress slogan with a finite construction and an explicit boundary for cycles. | **Main**, one paragraph in definitions/recursion; worked typing in **appendix**. |
| `L24-E3` | Certificate acceptance is invariant under checker, schema, implementation, or artifact-version changes. | The immutable record contract in [`02_relu_architecture.md`](../ml/02_relu_architecture.md), §§3--4, requires checker/version/polarity binding. Checkpoint C1's [`artifact-transport erratum`](checkpoints/C1_empirical_adjudication.md#2-artifact-transport-erratum-and-verification-contract) showed that public verification can fail when frozen bytes and recorded hashes are transported under a different newline convention. | A certificate is usable only with its exact claim schema, candidate, units, scorer, split, scope, polarity, checker, version, validity interval, and provenance. The CRLF artifacts now retain their registered bytes; prospective artifacts have an explicit LF writer. | Trust-boundary and reproducibility repair. The scientific result remains unchanged, while “the checker accepted it” becomes explicitly versioned. | **Main** reproducibility sentence; full record and erratum in **appendix/repository**. |
| `L24-E4` | Marginal calibration, low false-assertion rates, or narrow selective risk alone establish useful licensed coverage. | **Calibrated but nearly non-granting:** [`02_results.md`](../experiments/02_results.md), §§2--3. `F36` passed with target-in-proposal coverage `0.9098/0.9044`, while the structured arm had unweighted trace miss rates `0.4611/0.3248` for support/refutation and target-weighted fallback mass `0.9962`. | `F36` supports marginal target-in-proposal coverage under the frozen exchangeable generator. The same run constructively demonstrates that information retention, calibrated proposal coverage, cautious withholding, and operational usefulness are separate quantities. | Central empirical limitation and paper narrative. It weakens one implementation default; the architecture-neutral calculus and representation theorems remain intact. | **Main**, physically adjacent to every calibration or safety-usefulness discussion. |
| `L24-E5` | The frozen compact traces can reconstruct all target-weighted error, routing, and deployed-risk secondaries after the run. | [`02_results.md`](../experiments/02_results.md), deviation `21-D3`: target/design weights, polarity, evidence mode, and diagnostic labels were absent from compact traces; selected/deployed loss and misroute severity cannot be reconstructed. | The registered minimum core remains interpretable from sealed metric rows. The unavailable secondaries are recorded as unavailable and cannot be used to strengthen or rescue that result. | Reporting limitation and prospective design obligation. No rerun of the sealed confirmation is authorized. | **Main** limitations sentence for the experiment; exact unavailable list and future trace schema in **appendix**. |

## 4. Recursion and self-reference

| ID | assumption exposed | constructive witness | surviving result | project impact | paper placement |
|---|---|---|---|---|---|
| `L24-R1` | Finiteness and acyclicity alone ground a support derivation. Every zero-premise success must also be a declared accepted base. | [`08c_proof_carrying_plans.md`](../formalism/08c_proof_carrying_plans.md), Theorem 5, Corollary 6, and Counterexample 7: a one-node acyclic graph marked supported has no evidential source. | A finite acyclic derivation in which each zero-premise node is a typed base and each rule preserves provenance gives a constructive path from every supported requirement to accepted evidence. | Core provenance boundary. It distinguishes audit grounding from target-world soundness, which still uses `L24-E1`. | **Main**, one sentence with the positive grounded-DAG theorem; details in **appendix**. |
| `L24-R2` | A system's same-run grant supplies its own evidence, or the ordinary finite decoder already determines the meaning of an unranked cycle. | [`08c_proof_carrying_plans.md`](../formalism/08c_proof_carrying_plans.md), Theorem 8, Countertheorem 10, and Counterexample 11: finite ranks yield a unique assessment; `g=g` has multiple Boolean solutions and `g=not g` has none. | A frozen implementation can be assessed at a higher evidential rank from independent records. A cyclic extension would need a declared state space, operator, existence conditions, selected fixed point, and soundness bridge. The project makes no universal claim about what every future cyclic semantics could yield. | Central recursion boundary. It permits bounded self-assessment while excluding circular warrant from the core. | **Main**, adjacent to system assessment; fixed-point checklist in **appendix/future**. |
| `L24-R3` | Repeated agreement or recursion automatically contributes new evidence about outcomes or task structure. | [`09_judgment_information.md`](../formalism/09_judgment_information.md), Theorem 7, Corollary 8, and Countermodel 6.6: `J_m=J_0` gives perfect agreement and zero conditional increment after `J_0`. | Recursive level `m` is evaluated against the full prior-report Bayes baseline. A positive held-out proper-score increment with new evidence gives conditional outcome information and, under mediation, task-quotient information. | Bounds an optional motivation while retaining a precise constructive experiment design. It is independent of proof-carrying plan recursion. | **Main or compact sidebar** if recursive judgment is retained; full derivation in **appendix**. |

## 5. Representation, scale, and boundaries

| ID | assumption exposed | constructive witness | surviving result | project impact | paper placement |
|---|---|---|---|---|---|
| `L24-P1` | ReLU positivity or zero alone encodes the full three-valued atom state and provides authorization or quarantine. | [`03_representation_theorems.md`](../ml/03_representation_theorems.md), Theorems 1--2, and the canonical witness in [`02_relu_architecture.md`](../ml/02_relu_architecture.md), §8.4: supported equality, open, negative-side, missing, and invalid cases can share zero; downstream biases bypass a zeroed unit. | A named positive ReLU margin can expose predicted slack or, after accepted conservative construction, certificate-relative surplus for one atom. Exact state, evidence validity, polarity, `WF`, profile meet, and active mask supply authorization. | Central neural-semantics correction. It strengthens the hybrid design while withdrawing no architecture-neutral theorem. | **Main**, immediately after the ReLU intuition, with one zero-boundary and one bypass example. |
| `L24-P2` | Any useful hidden activation can be relabeled as a jointly sufficient adequacy/value feature. | [`03_representation_theorems.md`](../ml/03_representation_theorems.md), Theorems 6--7: equal adequacy codes can hide different payloads; the positive construction requires named addresses, state coordinates, normalized surplus, valid evidence, and declared consumers. | Dual use is constructible for the named coordinate-complete state-plus-surplus family. General payloads and unregistered consumers retain separate channels or require a new sufficiency proof. | Neural-interpretability boundary. It preserves the author's dual-use insight at an exact typed scope. | **Main**, concise conditional construction; minimality and separator in **appendix**. |
| `L24-P3` | Exact representability, training success, calibration, and semantic alignment are one achievement. | [`03_representation_theorems.md`](../ml/03_representation_theorems.md), Executive Result and §9: finite CPWL maps have exact ReLU realizations, while SGD recovery, shift validity, hidden-feature alignment, and architectural efficiency require separate evidence. | The repository proves exact hybrid representation theorems and reports one frozen learning experiment. Semantic alignment remains an empirical question with probe/intervention designs in [`policy_value_interpretability.md`](policy_value_interpretability.md). | Core publication distinction. It prevents a theorem about functions from being narrated as a learned-mechanism result. | **Main**, contribution and limitation paragraphs; experimental designs in **future**. |
| `L24-P4` | An unnormalized scalar margin has invariant semantic magnitude across units, or one adequacy scalar is sufficient for arbitrary downstream computation. | [`03_representation_theorems.md`](../ml/03_representation_theorems.md), Theorems 6--7 and §7.5: independent rescaling can change cross-channel rankings; equal margins can hide different predictions, costs, and traces. | Positive rescaling preserves status. Registered normalization makes surplus invariant, and a covariant consumer can preserve a declared computation. Sufficiency remains relative to the named consumer family. | Representation boundary with practical trace implications. It keeps units and normalization visible without denying scalar use where justified. | **Appendix**, with one sentence beside dual-use channels. |
| `L24-P5` | One ordinary continuous ReLU output exactly realizes arbitrary discontinuous hard seams, nonlinear primitives, unbounded recursion, or dynamically growing plans. | [`03_representation_theorems.md`](../ml/03_representation_theorems.md), Theorems 4 and 8, §8.3: affine traces glue continuously exactly under face agreement; bilinear gates and discontinuous seams leave the exact CPWL class. | Fixed finite CPWL plans with conforming branches have exact ReLU realizations. Other primitives can use an external hard router, a different architecture, or verified approximation envelopes on declared compact domains. | Architecture-scope boundary. It motivates comparators without claiming that ReLU is uniquely suitable. | **Appendix** theorem statement; brief **main** architecture-neutrality sentence. |

## 6. Atlas, routing, and shift

| ID | assumption exposed | constructive witness | surviving result | project impact | paper placement |
|---|---|---|---|---|---|
| `L24-A1` | Adequacy in parent expectation transports automatically to every learned or selected subdomain. | [`08a_transport_routing.md`](../formalism/08a_transport_routing.md), Theorem 1 and Counterexample 3: a loss of `1` on ten percent of the domain has parent mean `0.1` but conditional loss `1` on that subdomain. | Free restriction to every positive-measure subdomain is equivalent to an almost-sure pointwise bound. Otherwise certificates remain indexed to their evaluated scope or use selection-aware re-evaluation. | Core domain boundary. It explains why learned regions cannot inherit aggregate evidence silently. | **Main**, one counterexample beside domain restriction; proof in **appendix**. |
| `L24-A2` | Local expert accuracy or correct masking alone controls deployed routed risk; fallback is harmless whenever no expert is licensed. | [`08a_transport_routing.md`](../formalism/08a_transport_routing.md), Theorems 5--6, and [`08_metatheory.md`](../formalism/08_metatheory.md), Theorem 20/Countermodel 21: routed risk contains correct, misroute, and fallback integrals, and a status-quo fallback can have catastrophic target loss. | The hard-router decomposition gives constructive bounds when selected-scope risks, misroute/fallback mass and severity, and the fallback policy are evaluated. Gap fallback prevents unlicensed expert use; fallback safety is its own requirement. | Core routing and safety boundary. It prevents abstention from being counted as cost-free success. | **Main**, adjacent to routing and empirical fallback numbers; formulas in **appendix**. |
| `L24-A3` | Pairwise usable bridges imply one path-independent global coordinate system. | [`08a_transport_routing.md`](../formalism/08a_transport_routing.md), Theorem 20 and Counterexample 21: three invertible translation bridges with cycle sum `1` admit no global potential. | Exact group-valued bridges have global frame potentials exactly when all declared cycle products are identity. Partial or approximate bridges can remain useful with path-specific provenance and defect bounds. | Optional atlas boundary. It preserves local translation without manufacturing global ontology. | **Appendix** unless a bridge appears in the running example. |
| `L24-A4` | A certificate, calibration result, judge-information bound, or semantic alignment transfers unchanged across population or temporal shift. | [`09_judgment_information.md`](../formalism/09_judgment_information.md), Countermodel 6.5, and the validity/shift contract in [`04_losses.md`](../ml/04_losses.md), §§5 and 12: training outcome information can vanish when `P(Y|Z,N)` changes. | Every result remains population-, scope-, and version-relative. Transfer requires a replicated shift panel, an accepted transport model, or renewed evidence; expired or off-scope records become open rather than silently retained. | Empirical and deployment boundary. It motivates prospective shift panels and versioned evidence validity. | **Main** generalization sentence; stress-test design in **future**. |
| `L24-A5` | Raw accuracy under different abstention policies identifies representation or architecture quality, and an omitted comparator receives an empirical ranking. | [`C1_empirical_adjudication.md`](checkpoints/C1_empirical_adjudication.md), §4.3: Checkpoint C requested matched coverage, while the frozen boundary primary used raw macro accuracy with fallback masses `0.9962` versus `0.9139`. Hard MoE failed its prospective feasibility/power gate and was omitted. | The registered raw endpoints retain their exact evidential status. Future architecture comparisons should match capacity/compute where meaningful and make matched coverage or full risk--coverage curves primary. No result ranks hard MoE or establishes general CE/structured superiority. | Central empirical fairness boundary. It affects comparative narrative, not the validity of the frozen endpoints. | **Main**, beside the empirical comparison; follow-up comparator study in **future**. |
| `L24-A6` | Neural activation cells, router cells, and scientific-model domains align by sharing an atlas metaphor. | [`05_atlas.md`](../formalism/05_atlas.md), §§4--8, and [`03_representation_theorems.md`](../ml/03_representation_theorems.md), §5.2 distinguish the three partitions. Checkpoint C1 ran no activation-alignment experiment. | The scientific cover and CPWL activation complex are separately well-defined; typed probes, shared/independent encoder comparisons, and interventions can test correspondence. | Interpretability boundary. The atlas formalism survives, while neural/scientific alignment remains unmeasured. | **Main**, one sentence guarding the atlas analogy; evidence program in **future**. |

## 7. Policy, value, interpretability, and truth

| ID | assumption exposed | constructive witness | surviving result | project impact | paper placement |
|---|---|---|---|---|---|
| `L24-V1` | A lossless real-valued policy encoding automatically has standard-return, natural, unique, or identified utility semantics. | [`policy_value_judgment.md`](policy_value_judgment.md), §§2--3: injective finite action codes give inverse maps on their image, while the same policy under two reward functions has different `V^pi`. | Finite representational existence is retained with its encoder, decoder, image, and preserved structure declared. Standard `V^pi/Q^pi` is a separate environment-relative construction. | Clarifies the policy/value proposition without withdrawing its existence content. | **Main**, proposition followed immediately by the same-policy/different-return witness. |
| `L24-V2` | Standard policy evaluation followed by greedy decoding inverts any policy, or occupancy is utility everywhere. | [`policy_value_judgment.md`](policy_value_judgment.md), §§2.2--3.4: a suboptimal policy chooses the lower-return action, so greedy `Q^pi` improves it; occupancy is driven by starts and dynamics and is silent off support. | Greedy reconstruction agrees under stated greediness and tie conditions. Full state--action occupancy can recover Markov behavior on positive-occupancy states; expected return additionally needs reward. | Bounds the companion case study. Disagreement can be informative policy improvement rather than reconstruction error. | **Main or companion sidebar**; extended examples in **appendix**. |
| `L24-V3` | Proper-score improvement against any convenient comparator establishes task information; outcome prediction alone identifies the latent task ontology. | [`09_judgment_information.md`](../formalism/09_judgment_information.md), Theorems 2, 3, and 6, Lemma 5, and Countermodels 6.1--6.4: a weak baseline, omitted nuisance, or leaked outcome can create an apparent gain without task information; duplicated labels are invisible to the outcome kernel. | Improvement over the true nuisance-conditioned Bayes baseline gives outcome information. Explicit mediation transfers it to the outcome-identifiable task quotient, which intentionally merges outcome-equivalent labels. | Bounds the recursive-judgment and semantic-surrogate motivation while preserving the exact information theorem. | **Main or compact sidebar**, with one omitted-nuisance/leakage witness; remaining countermodels in **appendix**. |
| `L24-V4` | Behavioral agreement with an independently trained value surrogate identifies the policy's internal computation or makes the representation human-readable. | [`policy_value_judgment.md`](policy_value_judgment.md), §4, and [`policy_value_interpretability.md`](policy_value_interpretability.md), §§3--5: separate policy/value models can agree without shared representation; causal and human axes remain unmeasured. | Behavioral and value fidelity can support a scoped semantic surrogate. Mechanism and human-use claims have their own constructive probe, intervention, and comparative-user-study requirements. | Optional interpretability boundary. It places positive mechanism/human results in companion or future work. | **Main limitation** if the case study is mentioned; experiments in **future**. |
| `L24-V5` | The project answers whether arbitrary policies possess true utility, recovers such utility, establishes value's metaphysical priority over belief, or reduces truth to usefulness. | The author clarifications recorded in [`policy_value_judgment.md`](policy_value_judgment.md), §1A, together with the two-sorted semantics and [`06_open_endedness.md`](../formalism/06_open_endedness.md), §12. These are scope declarations rather than negative theorems. | The project studies approximate environment-relative value-function representations as a promising first semantic foothold and a pragmatic logic of finite-stage reliance. It remains neutral on the neighboring metaphysical questions. | Protects the philosophical narrative from implying denials that the project has not argued for. | **Main**, motivation and conclusion; no “true utility is false” or “truth is only usefulness” language. |

## 8. Cross-matrix paper allocation

The main paper should use a small number of adjacent positive-result/boundary
pairs rather than collect every row in one late limitations section:

| positive result | adjacent main-text boundary | appendix/future handoff |
|---|---|---|
| finite-stage `WF + K_3` assessment | `L24-F1`, `L24-E1` | continuation countermodels and mode-scoped soundness schema |
| finite comparison, composition, and routing | `L24-F2`, `L24-F3`, `L24-A2` | search obstruction, path-sensitivity budget, full routed-risk decomposition |
| ReLU reference realization | `L24-P1`, `L24-P3` | dual-use, scale, hard-seam, and finite-library details `L24-P2/P4/P5/F4` |
| frozen empirical result | `L24-E4`, `L24-A5`, with `L24-E5` disclosed | future matched-coverage/deployed-risk study using the trace contract below |
| policy/value and recursive-judgment motivation | `L24-V1`, `L24-V3`, `L24-V4/V5` | companion reconstruction, probes/interventions, and human studies |

The atlas cycle row `L24-A3`, typed-base row `L24-R1`, and detailed scale row
`L24-P4` are appendix material unless the final running example depends on
them. `L24-R2` belongs in the main formal section because it states the exact
boundary of the project's constructive treatment of self-assessment.

## 9. Prospective trace contract

Deviation `21-D3` cannot be repaired retrospectively. Any separately versioned
future study of routing, conservative decoding, policy/value usefulness, or
matched coverage should retain a compact per-decision record sufficient to
reconstruct the declared estimands:

```text
FutureTrace = {
  study/protocol/implementation versions,
  world root, split role, lineage root, fit seed,
  candidate, request, profile, atom/schema, domain/cell,
  target weight, design/sampling weight,
  target state and prediction,
  polarity and accepted evidence mode,
  compact diagnostic and reason code,
  statistic/region, threshold, signed margins, checker record,
  active set, selected route, fallback event,
  task loss for candidate/selected/fallback/deployed behavior,
  misroute type and severity
}.
```

The minimum prospective obligation named by Task 24 is explicit retention of
**target and design weights, polarity, evidence mode, and compact diagnostics**.
Selected/deployed loss and misroute severity are also required whenever a study
makes routing, usefulness, or safety claims. The trace schema must be frozen
before outcomes are inspected, validated against the aggregate metric rows, and
bound to the same protocol/checker versions. Compactness is an engineering
constraint; it is not permission to omit the fields defining the estimand.

## 10. Constructive conclusion

The limitations do not reduce to a verdict that the ambitious neighboring
ideas are false. They show where the present constructions stop and which
extra data or hypotheses would extend them. The finite core becomes stronger,
not weaker, when it states its continuation class, evidence bridge, search set,
grounding discipline, and composition rule. The neural story becomes more
informative when representation, learned fidelity, calibration, alignment, and
usefulness are measured separately. The policy/value bridge remains promising
because it now has explicit semantic targets and evidence grades; its mechanism
and human-use evidence awaits the proposed studies.

This matrix is the source for Task 25's claim freeze and outline. Public prose
should select the rows above by argumentative role, keep each boundary adjacent
to the positive result it qualifies, and reserve the full matrix for an
appendix or repository reference.
