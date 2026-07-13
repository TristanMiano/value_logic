# Core-Related Literature Supplement

Status: Task 12A primary-source audit

Date: 2026-07-12

Bibliography: [`references.bib`](../references.bib)

## Durable result summary

This audit verifies the seven literature clusters requested before the compact calculus is frozen. The Fable 5 audit's `L1–L5` entries were treated only as search leads. Every included item was checked against an original paper, official proceedings page, publisher record, author-hosted paper, or journal record.

The nearest structural precedents are now clear:

1. **Input/output logic** is the closest precedent for producing authorized outputs from conditions without treating the output operation as ordinary truth-preserving detachment.
2. **Prioritized defaults and reasons** show how defeasible rules, reliability orderings, undercutting, and conflict can be formalized, but empirical certificates and hard safety constraints are not defaults merely because they can be defeated.
3. **Justification and labelled deductive logics** support explicit evidence terms and structured formula labels. They do not make this project's empirical provenance terms factive proof objects.
4. **Awareness/unawareness logics** distinguish what is currently represented from what is implicit or outside an agent's language. They clarify the finite-library/conceivable-alternative distinction without establishing library completeness or the Task 12 continuation theorem.
5. **Strong Kleene and partial-function logics** support the algebraic use of three meaningful values. The project gives those values an evidential, not truth-functional, interpretation. Its separate `WF` failure is not a fourth Strong-Kleene value.
6. **Conformal prediction** supplies finite-sample prediction-set validity under exchangeability. Its error level is not the same parameter as a task-risk tolerance, and conformal validity does not by itself prove `Risk(e,q)<=epsilon`.
7. **High-confidence and safe policy improvement** is the strongest precedent for improvement over a fallback or status quo under uncertainty. Its guarantees do not transfer outside their MDP, data, return, uncertainty-set, and policy-class hypotheses.

The audit therefore supports a synthesis claim but not a novelty theorem: these literatures cover important components, while none of the verified results directly yields the project's `WF + K_3`, profile-indexed license, update, and open-library semantics. Task 13 may cite structural similarities; Task 14 must prove the project's metatheory independently.

## 1. Audit method and transfer rule

### 1.1 Source rule

A source enters [`references.bib`](../references.bib) only after bibliographic identity and the relevant technical scope were checked at a primary location. Search summaries, encyclopedia entries, and the Fable audit were discovery aids, not evidentiary endpoints.

For books, the publisher page was used. For conference papers, official proceedings or the paper itself was used. For journal papers, the publisher record, DOI record, journal page, or author-hosted journal PDF was used.

### 1.2 Four levels of relationship

Each comparison uses one of four levels:

- **algebraic identity:** the same finite operation occurs after an explicit relabeling;
- **structural analogy:** the same role is played by a differently interpreted object;
- **possible elaboration template:** a neighboring calculus could guide a later extension after a translation is defined;
- **no theorem transfer:** similar vocabulary does not satisfy the source theorem's hypotheses.

Only the first level permits a direct mathematical import. Even then, the imported result is limited to the identified algebraic fragment.

### 1.3 No negative novelty inference

This focused audit cannot prove that no earlier system combines all of the project's elements. It establishes only that the verified sources do not already supply the proposed calculus. A publication-level novelty claim still requires the broader related-work synthesis and final citation audit in Tasks 30–31.

## 2. Input/output logic: output production without truth detachment

### 2.1 Verified source

`MakinsonVanDerTorre2000` develops propositional input/output operations. Its motivating examples include obligations, goals, ideals, preferences, actions, and beliefs. Inputs need not reappear among outputs, contraposition can be inappropriate, and the paper distinguishes systems in which outputs can or cannot be reused as later inputs. It gives semantic operations and corresponding derivation rules.

Primary locations:

- [author-hosted journal paper](https://icr.uni.lu/leonvandertorre/papers/jpl00.pdf)
- [DOI record](https://doi.org/10.1023/A:1004748624537)

### 2.2 Exact similarity

The project's licensed consequence has the shape

```text
condition + valid license record  ->  permitted scoped output,
```

not

```text
condition + theorem about model truth  |-  unrestricted truth.
```

This is structurally close to an input/output operation. The output may be an authorized prediction, equation use, action, or labelled conclusion. The input need not itself be an output, and output reuse should be a declared rule rather than assumed through ordinary transitivity.

The match is strongest for the Task 9 `MayRely` layer. It is weaker for the full `Lic_P` assessment, which is an evidence-state judgment rather than a conditional norm.

### 2.3 Exact mismatch

Input/output logic in the verified paper does not supply:

- empirical loss or risk;
- uncertainty certificates;
- domains, model libraries, fallbacks, or provenance DAGs;
- `WF + K_3` status aggregation;
- the distinction between lapse, rebuttal, comparison defeat, and archive retention; or
- open-ended continuation semantics.

Its semantic and syntactic characterizations apply to its own input/output operations. The project cannot cite those characterizations as soundness or completeness results for `MayRely` until Task 13 gives a translation preserving language, operations, and derivations.

### 2.4 Task 13 disposition

Use input/output logic as the principal related-work comparison for **output-producing consequence without truth detachment**. Do not rebuild the core as an input/output logic unless a translation makes the evidence and profile machinery visible. The minimal calculus may expose a map from granted labelled premises to permitted outputs and then compare its structural rules with the four input/output families.

## 3. Prioritized defaults and reasons

### 3.1 Verified sources

`Brewka1989` constructs preferred maximal consistent subtheories. It introduces reliability layers and then a strict partial ordering over premises, defining weak and strong provability through preferred subtheories. The official IJCAI paper explicitly motivates priorities between conflicting defaults.

`Horty2012` develops reasons using default logic, including conflicts, reason strength, undercutting defeaters, exclusionary reasons, and conclusions supported by multiple reason sets.

Primary locations:

- [Brewka, IJCAI proceedings PDF](https://www.ijcai.org/Proceedings/89-2/Papers/031.pdf)
- [Horty, Oxford University Press](https://doi.org/10.1093/acprof:oso/9780199744077.001.0001)

### 3.2 Exact similarity

The project has potentially conflicting considerations: adequacy evidence, fallback advantage, costs, hard constraints, bridge obligations, and comparison evidence. Default/reason systems demonstrate that defeat can depend on the source and priority of support rather than on Boolean inconsistency alone. Horty's treatment also confirms that “reason,” “defeater,” and “undercutter” can be given proof-theoretic roles rather than serving as informal diagnostic prose.

These systems are plausible templates for an optional extension in which:

- certificate modes have an explicit reliability ordering;
- later corrections undercut a certificate without proving its target false;
- hard constraints defeat otherwise favorable reasons; or
- multiple profiles impose different priority policies.

### 3.3 Exact mismatch

The current `P_rely` core does not resolve arbitrary inconsistent premise sets by selecting preferred classical subtheories. Its required atoms are independently assessed and combined by finite meet. A hard safety countercertificate is not merely a lower- or higher-priority default, and a calibrated risk interval is not a default rule.

Similarly, Task 12's lapse/rebuttal distinction is provenance-sensitive:

```text
invalidated support without counterevidence -> open;
valid countercertificate                     -> refuted.
```

That distinction is not obtained merely by placing premises in a reliability ordering.

No preferred-subtheory, default-logic, or reason-theoretic representation theorem transfers to the project. The source languages, consequence definitions, conflict policies, and semantic targets differ.

### 3.4 Task 13 disposition

Keep priorities out of the smallest core unless Task 13 needs them to resolve actual conflicting diagnostics. Preserve a typed diagnostic and update interface that allows a later priority/defeater extension. Cite Brewka and Horty to show that conflict-sensitive, strength-sensitive reason calculi exist; do not describe the project itself as a prioritized default logic.

## 4. Explicit evidence and labelled deduction

### 4.1 Verified sources

`Artemov2008` presents justification logic as propositional logic augmented with assertions

```text
t : F,
```

read as “`t` is a justification for `F`.” The earlier Logic of Proofs develops operations on proof terms; the 2008 article gives the broader justification-logical framework and a correspondence program relating justification systems to epistemic modal logics.

`Gabbay1996` develops labelled deductive systems as structured families of labelled formulas with algebraic structure on labels.

Primary locations:

- [Artemov, Cambridge/Review of Symbolic Logic](https://doi.org/10.1017/S1755020308090060)
- [Gabbay, Oxford University Press](https://doi.org/10.1093/oso/9780198538332.001.0001)

### 4.2 Exact similarity

The project's diagnostic object has an explicitly indexed shape:

```text
atom address : witness / counterwitness / obstacle / provenance.
```

Likewise, labelled consequence has the shape

```text
[chi] phi,
```

where the label records the model, domain, task, profile, stage, and evidence interface under which `phi` may be used. Justification and labelled systems establish that such indices can be part of the formal language and proof theory rather than annotations discarded after derivation.

This is a strong **elaboration-template** match. Term operations could eventually model certificate composition, and label algebras could eventually model domain restriction or provenance transport.

### 4.3 The factivity boundary

The match stops before factivity. In proof-oriented justification logic, systems may validate principles such as

```text
t:F -> F
```

under their stated semantics. A project certificate is not automatically such a proof object. For example:

- a frequentist confidence procedure can issue a valid certificate on a sample path whose realized interval misses the fixed target;
- a conformal prediction set has a coverage guarantee, not a proof that a particular future label lies inside it;
- an evaluation can later be corrected for leakage; and
- a certificate can support adequacy relative to `epsilon` without proving an object-level physical statement true.

Therefore the project must not import reflection, realization, correspondence, soundness, or completeness theorems from justification logic. A project-specific evidence semantics must state what each term certifies and with what mode of validity.

### 4.4 Provenance is more than a label and less than a proof

A provenance DAG records dependency and history. It can show which data, procedure, certificate, correction, and request produced a status. That makes it richer than an opaque label. But provenance can faithfully record an invalid or defeated argument, so its presence is weaker than proof correctness.

Task 13 should use an abstract evidence/provenance index, not the full DAG, and should avoid calling every evidence term a “proof term.” Task 14 may establish a mode-scoped soundness theorem only after defining the interpretation of each certificate mode.

## 5. Awareness and unawareness

### 5.1 Verified sources

`FaginHalpern1988` develops logics for limited reasoning, including explicit awareness. Its core motivation is that an agent's beliefs need not contain every valid formula and that awareness of a concept can be required before explicit belief about it.

`HeifetzMeierSchipper2006` develops generalized state spaces supporting non-trivial interactive unawareness, rather than forcing all agents into one standard state space whose complete event algebra is already available to them.

Primary locations:

- [Fagin and Halpern, author-hosted journal PDF](https://www.cs.cornell.edu/info/people/halpern/papers/awareness.pdf)
- [Fagin and Halpern, DOI](https://doi.org/10.1016/0004-3702(87)90003-8)
- [Heifetz, Meier, and Schipper, DOI](https://doi.org/10.1016/j.jet.2005.02.007)

### 5.2 Exact similarity

The project must distinguish at least:

```text
evaluated library
known but unevaluated candidates
expressible but currently unconsidered candidates
candidates not representable in the current language/library
metaphysically or mathematically possible candidates, if that notion is supplied externally.
```

Awareness formalisms show why these layers should not be collapsed into one universal candidate set. In particular, “no certified dominator in the evaluated set” is not “the agent knows there is no dominator,” and not “there exists no conceivable dominator.”

The connection to Task 12 is precise but limited: a live `AddModel` continuation can enlarge the represented/evaluated candidate space. Awareness language helps describe why the prior finite library was not complete.

### 5.3 Exact mismatch

Neither verified awareness framework defines empirical model adequacy, risk certificates, profile-indexed licenses, or the Task 12 `AddDom` condition. Task 12's impossibility theorem follows from its continuation property and stage-indistinguishability, not from a theorem in awareness logic.

The project also does not need a completed universal set of “all conceivable theories.” Open-library semantics can be stated operationally:

```text
every current finite state has an admissible history-preserving AddModel continuation.
```

This avoids converting an intended limitation of awareness into a hidden omniscient universe inside the model.

### 5.4 Task 13 disposition

Represent the evaluated library and search scope as state data. Treat unrepresented alternatives through continuation quantification, not a primitive `Unaware(e)` atom in the minimal core. Cite awareness/unawareness logic as the established neighboring field for bounded languages and non-omniscience.

## 6. Strong Kleene, Bochvar, and partial functions

### 6.1 Verified sources

`Kleene1952` is the primary book source for the strong three-valued connectives used in reasoning about partial recursive predicates/functions. Under the order

```text
false < undefined < true,
```

strong conjunction is minimum and strong disjunction is maximum.

`BochvarBergmann1981` is the English translation of Bochvar's 1937 system. Its internal third value is read as nonsense/meaninglessness, and internal compounds are infectious when a component is meaningless; the system also adds external means for speaking about meaningfulness.

`GavilanesFrancoLucioCarrasco1990` gives a first-order, three-valued logic for partial functions and proves results for its own model theory and calculus.

Primary locations:

- [Kleene bibliographic record](https://books.google.com/books/about/Introduction_to_Metamathematics.html?id=gFgPAQAAMAAJ)
- [Bochvar translation and DOI](https://doi.org/10.1080/01445348108837023)
- [Gavilanes-Franco and Lucio-Carrasco DOI](https://doi.org/10.1016/0304-3975(90)90005-3)

### 6.2 Exact algebraic identity

For a well-formed project request, map

```text
refuted   -> false
open      -> undefined
supported -> true.
```

Then finite aggregation of required atoms is exactly strong-Kleene conjunction/minimum on the three-element chain. This imports the following algebraic facts directly:

- commutativity;
- associativity;
- idempotence;
- monotonicity in every coordinate; and
- `supported` iff every required atom is supported, while `refuted` iff at least one required atom is refuted.

This identity concerns the finite algebra only. The interpretation is different: project `open` means that the current record does not support or refute the requirement, not that an object-language proposition has an undefined truth value.

### 6.3 Why `Undefined` is not Bochvar infection in the compact kernel

The historical Task 8/11A four-chain aggregated

```text
Undefined > Refused > Withheld > Granted
```

and therefore resembled a Bochvar-infectious extra error element: one ill-formed component could dominate the displayed result. That presentation was superseded after Checkpoint A1 because it could mask a certified safety refusal at top level.

The compact kernel instead evaluates:

```text
WF first;
K_3 atoms only after WF succeeds.
```

Consequently:

- `Undefined` is a request-level typing/denotation/interface failure;
- no meaningful atom has value `Undefined`;
- `Refused`, `Withheld`, and `Granted` arise from Strong-Kleene meet; and
- safety projections preserve refuted/open safety atoms without relying on a global reason code.

Bochvar remains an illuminating comparison to the superseded design, not the semantics adopted for the compact core.

### 6.4 Partial-function boundary

Partial-function logics demonstrate principled ways to interpret terms whose denotation can fail. The project currently makes a different design choice: missing or ill-typed model execution is handled by `WF`, while lack of evidence on a typed executable scope yields an open atom.

No partial-function soundness/completeness result transfers because the project's syntax, term interpretation, quantifiers, designated values, and consequence relation have not been translated into the source calculus. Task 13 can cite partial logic to justify taking definedness seriously without adopting its entire first-order apparatus.

## 7. Conformal prediction

### 7.1 Verified sources

`VovkGammermanShafer2005` is the primary monograph on conformal prediction. `ShaferVovk2008` supplies a self-contained journal tutorial. Under exchangeability, conformal procedures produce prediction sets with marginal validity at a user-chosen error level; efficiency depends on the conformity score and data-generating structure.

Primary locations:

- [Vovk, Gammerman, and Shafer, Springer](https://doi.org/10.1007/b106715)
- [Shafer and Vovk, JMLR](https://www.jmlr.org/papers/v9/shafer08a.html)

### 7.2 Three parameters that must remain distinct

Use separate notation:

```text
epsilon_task   task-risk tolerance in q
alpha_cert     certificate failure/confidence parameter
eta_CP         conformal miscoverage level
```

The literature often writes conformal miscoverage as `epsilon`; the project already uses `epsilon` for acceptable task risk. Reusing one symbol would falsely suggest that prediction-set miscoverage and expected task loss are the same quantity.

### 7.3 Exact similarity

Conformal prediction is a concrete `CertSpec` mode. It shows how a finite sample and a declared symmetry assumption can produce an operationally checkable prediction set with a finite-sample validity statement. A project use plan may consume that set, route when it is small enough, or defer when it is too broad.

It also supports the general design principle that **validity and efficiency are separate**. A conformal set can be valid but uninformative, much as a project certificate can be procedurally valid while failing to support a useful license.

### 7.4 Exact mismatch

Standard conformal coverage does not directly imply

```text
Risk_L(e,D) <= epsilon_task.
```

It concerns inclusion of future labels/outcomes in prediction sets under exchangeability, typically as a marginal statement. To support an adequacy atom, the project needs an additional theorem translating set coverage/size and the downstream loss into the named risk functional. Conditional coverage, distribution shift, adaptive domain choice, and repeated model selection require further assumptions or adjusted procedures.

Conformal validity is also not a posterior probability that a theory is true. No Bayesian interpretation is imported by the conformal guarantee.

### 7.5 Task 13 disposition

Keep certificate mode abstract in the core. Use conformal prediction as one worked certificate mode and state exchangeability, coverage target, conformity score, calibration sample, and downstream risk translation separately. Task 18 or 19 must choose the operational procedure before empirical claims are made.

## 8. High-confidence and safe policy improvement over a baseline

### 8.1 Verified sources

`ThomasTheocharousGhavamzadeh2015` gives a batch RL algorithm in which the user supplies a performance lower bound and confidence level; the algorithm controls the probability of returning a policy below that bound under its assumptions.

`GhavamzadehPetrikChow2016` formulates robust baseline regret under an inaccurate dynamics model with accuracy guarantees, seeking policies that perform at least as well as a baseline across an uncertainty set and falling back where appropriate.

`LarocheTrichelairTachetDesCombes2019` develops SPIBB: in poorly sampled state-action regions, the learned policy follows the behavioral baseline, while changing behavior where improvement can be evaluated with the stated guarantee.

Primary locations:

- [High Confidence Policy Improvement, PMLR](https://proceedings.mlr.press/v37/thomas15.html)
- [Robust Baseline Regret, NeurIPS](https://proceedings.neurips.cc/paper/2016/hash/9a3d458322d70046f63dfd8b0153ece4-Abstract.html)
- [SPIBB, PMLR](https://proceedings.mlr.press/v97/laroche19a.html)

### 8.2 Exact similarity to the fallback atom

These sources give strong precedent for a decision of the form

```text
adopt candidate only when evidence supports
J(candidate) <= J(baseline) - Delta
at the declared confidence/robustness level;
otherwise retain or execute the baseline.
```

This directly supports the user's status-quo motivation for a contextual threshold. It also supports keeping three objects separate:

- the candidate's absolute hard constraints;
- improvement over the baseline; and
- uncertainty about that improvement.

SPIBB provides a particularly close operational analogy to a stitched atlas: change behavior in sufficiently supported regions and follow the baseline in uncertain regions.

### 8.3 Exact mismatch

The source guarantees are defined for policies, expected discounted return or regret, specified MDP/policy classes, offline trajectories, and particular statistical or model-uncertainty constructions. The project also covers predictors, simulators, scientific approximations, and non-policy use plans. It may use losses rather than rewards and can require noncompensable hard constraints.

Therefore safe policy improvement does not automatically establish:

- hard adequacy under `epsilon_task`;
- truth or empirical correctness of the model;
- safety under unmodeled distribution shift;
- validity for a changed baseline, reward, discount, domain, or policy class;
- a dominance relation over the whole model library; or
- profile-independent authorization.

The project must instantiate and prove its own `ImproveReq` certificate. The source theorems become applicable only if a use plan and context are translated into their policy/MDP objects with every assumption preserved.

### 8.4 Task 13 disposition

Retain fallback improvement as an independent parameterized atom. Cite HCPI, robust baseline regret, and SPIBB as operational precedents. Do not place their algorithms or MDP types in the minimal logic. Later ML experiments should include a baseline-relative comparator because it is both directly motivated and well connected to established operational methods.

## 9. Source-to-core boundary table

| source family | safe import | project-specific work still required | theorem transfer now? |
|---|---|---|---|
| input/output logic | distinction between output production and truth detachment; explicit reuse choice | evidence/status semantics, labels, update, fallback | no |
| prioritized defaults/reasons | conflict, priority, undercutting as formal roles | certificate validity, hard constraints, profile aggregation | no |
| justification logic | explicit term-indexed support pattern | non-factive empirical evidence semantics and provenance validity | no |
| labelled deduction | structured labelled-formula methodology | exact label algebra and consequence rules | no |
| awareness/unawareness | represented versus unrepresented possibility distinction | library/search/continuation semantics | no |
| Strong Kleene | finite meet algebra on three meaningful values | evidential interpretation and `WF` interface | **yes, algebra only** |
| Bochvar | comparison for infectious meaninglessness | none in adopted kernel; historical-design explanation only | no |
| partial-function logic | definedness as a first-class semantic issue | translation of project interfaces/terms | no |
| conformal prediction | certificate mode with exchangeability-based marginal validity | downstream risk translation and domain/model-selection control | no |
| safe policy improvement | baseline-relative improvement under uncertainty | general use-plan translation and independent hard constraints | no |

## 10. Core design consequences

Task 13 should inherit the following literature-constrained choices:

1. Describe licensed consequence as **output-producing and labelled**, while proving its rules independently.
2. Keep reason priority optional; the compact `WF + K_3` core does not need preferred-subtheory machinery.
3. Represent evidence/provenance explicitly but do not assume factivity or call every witness a proof.
4. Keep the evaluated library finite and represent unconsidered alternatives through continuation semantics, not an omniscient candidate universe.
5. Identify meaningful aggregation with the Strong-Kleene meet algebra, while stating that the values are evidential statuses.
6. Keep `WF` failure outside `K_3`; cite Bochvar only to explain why the earlier infectious four-chain was rejected.
7. Parameterize certificate mode. Conformal, confidence-bound, robust-set, and deterministic proof modes have different guarantees.
8. Keep `ImproveReq` distinct from `AdeqReq` and hard constraints. A status quo can induce a decision threshold without becoming the definition of all adequacy.
9. Import no source soundness, completeness, representation, calibration, or policy-improvement theorem without an explicit hypothesis-preserving translation.

## 11. Claim-ledger effects

This audit supports scoped literature dispositions rather than new universal claims:

- `A08`: baseline-relative thresholds now have strong operational precedents, while the project's algebra and empirical usefulness remain separately testable.
- `E02`: conformal prediction is verified as one certificate mode, but the inherited posterior-looking formula remains ambiguous and is not made “conformal” by citation.
- `E09–E10`: awareness literature supports the bounded-language distinction, but Task 12's non-certifiability results remain project theorems rather than imported awareness results.
- the compact status algebra receives a verified Strong-Kleene precedent; the infectious-Bochvar description applies only to the superseded historical four-chain.

No inherited empirical or formal claim is newly falsified in Task 12A. The main corrections are theorem-transfer restrictions and clearer parameter semantics.

## 12. Verified bibliography additions

The following keys were added to [`references.bib`](../references.bib):

```text
MakinsonVanDerTorre2000
Brewka1989
Horty2012
Artemov2008
Gabbay1996
FaginHalpern1988
HeifetzMeierSchipper2006
Kleene1952
BochvarBergmann1981
GavilanesFrancoLucioCarrasco1990
VovkGammermanShafer2005
ShaferVovk2008
ThomasTheocharousGhavamzadeh2015
GhavamzadehPetrikChow2016
LarocheTrichelairTachetDesCombes2019
```

## Task conclusion

The compact calculus now has a defensible related-work perimeter before it is frozen. Its consequence layer is closest to input/output and labelled deduction; its diagnostics resemble explicit evidence terms without inheriting proof factivity; its finite library is naturally compared with awareness formalisms; its meaningful status aggregation is exactly the Strong-Kleene meet algebra; and its fallback-improvement atom has concrete precedents in safe policy improvement. Conformal prediction supplies one valuable certificate mode but not a general adequacy theorem.

The result is not that the project has rediscovered one existing logic. It is that each mature neighboring field supplies a sharply bounded component, and each boundary identifies what Tasks 13–14 must still define and prove.
