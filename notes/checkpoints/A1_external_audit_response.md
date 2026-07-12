# Unscheduled Checkpoint A1: Response to the Fable 5 External Audit

Date: 2026-07-11

Trigger: [`llm_convos/claude_audit_2026-07-11.md`](../../llm_convos/claude_audit_2026-07-11.md)

Scope audited: Tasks 0–11A and Checkpoint A

Status: completed and amended 2026-07-12; no subsequent formal task begun

## Executive result

The external audit was useful and materially changed the project. It found one real internal inconsistency in the integrated witness, several underspecified interfaces, one citation misattribution, a claim-disposition mistake, and three strategic risks: a theorem deficit, non-executable semantics, and motivation that currently outruns the formal results.

The local defects have been repaired immediately. The roadmap now inserts an executable semantic reference before Task 12, a focused literature supplement before the core calculus freezes, stronger nontrivial theorem targets, and a later formal test of the recursive-judgment information claim.

The audit's overall positive findings are recorded as external corroboration, not as proof by authority. Its proof/arithmetic report supports confidence in the completed artifacts, but later Tasks 11B, 13, 14, and 31 remain responsible for executable, formal, and citation-grade verification.

## Evidence considered

- the complete Fable 5 audit;
- `formalism/01_signature.md` through `formalism/05a_integration.md`;
- `notes/project_spec.md`, `notes/claim_ledger.md`, `notes/literature_map.md`, and `references.bib`;
- the current TODO and Checkpoint A;
- Arora et al. (2018), Theorem 2.1, checked in the primary paper;
- Crossref metadata for Wang and Sun (2005) and He et al. (2020);
- the He et al. arXiv primary record/abstract describing its construction, neuron-count, and FEM contributions.

## Correction-by-correction adjudication

| Audit item | Decision | Repair |
|---|---|---|
| C1: comparison entities lacked adequacy certificates on the comparison scope | **Accepted; real inconsistency** | Added prespecified `{b,c}` adequacy certificates for `O`, `S`, and later `N`; added provenance nodes; revised the witness audit so it records the discovered and repaired inconsistency rather than claiming none was ever found. |
| C2: tight joint score intervals looked like invalid marginal propagation | **Accepted** | Named `D_cloud` and stated explicitly that the separating intervals are new joint certificates; marginal propagation overlaps and would withhold dominance. |
| C3: conservative update said no request field changes although `Succ_u` rebinds stage fields | **Accepted** | Partitioned request positions into substantive and stage-bound fields in Task 7; conservative update now preserves the former and rebinds only the latter. |
| C4: target risk was evaluated through a stage-only satisfaction symbol | **Accepted; foundational** | Introduced semantic pairs `<W,S>` with world-, stage-, and mixed-level satisfaction in Task 8. Task 13 must annotate every core judgment and state certificate-mode relations before soundness. |
| C5: tolerance proposition repeated an entailed inclusion hypothesis | **Accepted** | Removed the redundant hypothesis for principal down-sets and noted that general application-supplied acceptable sets still require explicit inclusion. |
| C6: CPWL depth bound attributed to He et al. rather than Arora et al. | **Accepted with audit erratum** | F14 and the literature map now credit Arora et al. (2018), Theorem 2.1, for the exact representation/depth statement and He et al. for detailed construction/size and FEM results. Added Wang–Sun (2005). The audit misnamed that paper: the verified title is “Generalization of Hinging Hyperplanes,” not “Representations of Piecewise Linear Functions.” |
| C7: E05 treated a superseded definition as falsified | **Accepted** | Added `D1` for superseded design defaults. E05 is `D1` as a universal definition and `X1` only for the narrower forced-closure proposition. The existing project-impact analysis was retained and sharpened. |
| C8: action-authorizing profile was informal | **Accepted** | Added a typed `UseRole` enumeration and defined `ActionAuthorizing`; ordinary action profiles require a fallback, while emergency/governance exceptions are separately typed and traced. |
| C9: the showcase `Withheld` request might instead be `Undefined` | **Accepted** | Declared `S` executable on `e` with a typed interface but lacking scope evidence. The request is therefore withheld; an absent/ill-typed interface remains undefined. |
| C10: Task 11A retrofit appeared only at file bottoms | **Accepted and broadened** | Added prominent interface notices to Tasks 7–11, not only 8–11, and linked them to Task 11A §16. Added the same warning to the README. |

The minor classification point in Task 9 was accepted: label-preserving right weakening is now identified as a rule schema, not an unrestricted structural closure property.

## Structural recommendations

### Adopted

1. **Executable semantics before more abstraction.** New Task 11B will implement the finite witness and assertions without beginning the neural experiment. This is an exception to the “no implementation before Checkpoint C” rule only for semantic verification infrastructure.
2. **Nontrivial theorem targets.** Task 12 now targets atom-level stability distinctions. Task 14 must seek an exact or near-exact update-persistence characterization and must distinguish definitions/algebraic corollaries from substantive results.
3. **Usable profile refinement.** Task 13 must separate profile shape from parameters, define atom entailment, and lift it to a profile preorder. Literal required-set inclusion remains only the provisional Task 11A relation.
4. **Status algebra with diagnostic safety.** The first pass required `Diag` because aggregate `Undefined` could mask a certified safety refusal in the historical four-chain presentation. The 2026-07-12 amendment below resolves this through separate `WF` plus meaningful `K_3` aggregation while retaining indexed diagnostics.
5. **Symbolic aggregation in the neural design.** Tasks 16 and 18 now supervise atoms and derive aggregate status symbolically. An independent aggregate head is only an ablation.
6. **Motivation debt.** New Task 22A must prove, refute, or demote B01. The formal paper may not promise recursive judgment recovers task structure unless that task supplies a defensible result.
7. **Corpus/provenance discipline.** New artifacts receive compact durable summaries and an advisory main-line length target. A central glossary/notation index is required in Task 13. One local commit per task/checkpoint is now the preferred history discipline; pushing still requires user direction.

### Deferred into explicit tasks

- Input/output logic, justification/labelled systems, awareness logic, logics of partiality, conformal prediction, and safe policy improvement are promising but not yet verified for this project. Task 12A will inspect primary sources and exact hypothesis matches.
- A proof-assistant formalization remains a high-value option, but it is not yet a required task. Checkpoint B should reconsider it after the core syntax and theorem targets are fixed.
- Automated notation extraction is deferred until Task 13 has one canonical grammar. Generating it now from superseded notation would automate inconsistency.

### Rejected or narrowed

- **Do not start the paper outline now.** Task 25 remains the claim-freeze/outline point because Task 14 may refute the proposed core and Tasks 21–22A may change the contribution. Task 25 now includes explicit word budgets and a glossary cross-check.
- **Do not impose a rigid 3,000-word cap on proofs.** The limit is advisory for main-line exposition; necessary proofs and audit trails go to linked appendices rather than being compressed until qualifications disappear.
- **Do not import all audit citations immediately.** Only the CPWL attribution was independently verified here. The remaining leads are assigned to Task 12A.
- **Do not move neural implementation before Checkpoint C.** Task 11B verifies semantics only; it does not train a ReLU model or freeze neural labels.
- **Do not add GL/Löb by analogy.** The continuation approach and the existing Task 12 exclusion remain.

## Roadmap changes

1. **Task 11B added and made next:** executable witness, unit tests, local-link checker, and minimal CI.
2. **Task 12 strengthened:** world/stage continuations plus atom-level stability characterization and open-library `AddModel` countermodels.
3. **Task 12A added:** core-related primary literature supplement before Task 13.
4. **Task 13 strengthened:** `<W,S>` models, judgment-level typing, profile shape/parameter entailment, status algebra, safety diagnostics, central glossary.
5. **Task 14 initially strengthened:** update-persistence characterization replaced KLM premise postulates as the primary target. The 2026-07-12 amendment below upgrades this to a multi-cluster theorem spine and adds Task 14A.
6. **Tasks 16 and 18 strengthened:** learn atoms, derive aggregate status symbolically.
7. **Task 22A added:** formal B01 information claim or narrative demotion.
8. **Task 25 strengthened:** word budgets and Task 13 notation cross-check.

## Claim-ledger consequences

- E05 now distinguishes `D1` from `X1`; its project-impact analysis remains mandatory because the narrower forced-closure proposition is genuinely falsified.
- E06 and E07 remain genuine scoped `X1` results with existing project-impact analyses.
- F14 remains `S1`, with corrected attribution.
- No new inherited substantive claim is marked falsified by this checkpoint.
- The audit's “all proofs correct” statement is external corroboration, not a new evidence status for every row.

## Risks after repair

1. The core still lacks a genuinely nontrivial theorem; Tasks 12–14A and 17 now own an explicit multi-cluster spine.
2. The finite semantics is not yet executable; Task 11B is now a gate.
3. The neural contribution remains entirely prospective; Checkpoints B and C still gate implementation.
4. The profile preorder remains too weak until Task 13 replaces literal parameterized-atom inclusion with entailment/refinement.
5. The original recursive-judgment narrative remains unsupported until Task 22A.
6. The corpus remains large; durable summaries and canonical consolidation are now required, but no historical artifact was destructively shortened.

## 2026-07-12 amendment: theorem weight and mathematical economy

The project author agreed with the audit's theorem-light diagnosis and separately questioned whether the number of nominal sorts and reason codes made the formalism resemble a software schema more than a mathematical paper. A second checkpoint pass therefore audited theorem opportunities, the 28-sort Task 7 inventory, and the reason vocabulary in Task 8.

### Finding 1: the problem is theorem quality, not theorem labels

The existing results remain useful validation lemmas and counterexamples, but most follow from a definition, deterministic aggregation, set inclusion, a standard product-order fact, the law of total expectation, or a triangle inequality. Renaming more such facts “theorems” would worsen the problem. The paper needs a small spine of characterizations, impossibility results, representation results, and quantitative bounds whose conclusions are not stipulated by the records.

The checkpoint adopts the following ranked theorem program:

| Cluster | Primary target | Why it carries mathematical weight | Owner |
|---|---|---|---|
| stability | deterministic/statistical/open-library stability trichotomy and finite-prefix non-certifiability | combines continuation semantics, convergence assumptions, and indistinguishable histories | Task 12 |
| update | robust grant/diagnostic persistence iff a dependency-complete impact cone misses required atoms, under path realizability; countertheorem without realizability | turns a sufficient frame rule into a necessity/sufficiency characterization over an update class | Task 14 |
| profiles | sound and relatively complete atom/profile refinement calculus for an independent realizable fragment | adds a finite separating-countermodel completeness direction absent from literal set inclusion | Task 14 |
| information | minimal sufficient diagnostic quotient for supported profile queries; `3^n` meaningful states or `n log_2(3)` bits for well-formed singleton-profile queries, plus a separate `WF` channel | answers where license information must live and proves what aggregation destroys | Task 14 |
| transport | exact characterization of when expected-risk adequacy restricts to every measurable subdomain | replaces “restriction may fail” with an iff theorem: all conditional means are at most `epsilon` iff loss is at most `epsilon` almost surely | Task 14A |
| routing | hard-router expected-risk decomposition and Lipschitz bridge-to-risk bounds | connects local licenses/bridges to global decision risk with explicit misrouting and disagreement penalties | Task 14A |
| neural | hard-routing seam iff characterization plus positive CPWL/ReLU construction and discontinuity obstruction | supplies both exact representability conditions and an impossibility boundary | Task 17 |
| motivation | conditional mutual-information lower bound for recursive judgment under log loss and non-leakage | can cash B01's promise or expose the exact assumptions it needs | Task 22A |

The optional group-valued bridge cocycle theorem remains an extension: global frame potentials exist exactly when cycle products are identity. It should be attempted only if the core theorem spine is already secure.

Formal success now requires at least three paper-carrying results from distinct clusters. Algebraic normal forms and standard lemmas support that spine but do not count toward it. A failed desired theorem may count only when replaced by a precise countertheorem and propagated through the claim ledger.

### Finding 2: the typed inventory is an elaboration, not the core calculus

The 28 entries in `formalism/01_signature.md` protect real distinctions, but calling all of them “core sorts” is presentationally and mathematically expensive. The compact calculus should have three principal carriers:

```text
E = evaluated alternatives/use plans
Q = substantive reliance/evaluation contexts
(S,->) = finite epistemic states and admissible updates.
```

Target worlds `W` are a semantic index rather than an agent-accessible object-language sort. A profile `P` is a finite family of parameterized requirement schemata. The four public outcomes form a fixed finite codomain, not another domain ontology.

For `q in Q`, dependent data include cases `X_q`, scope `D_q`, any measure/sampler and interface conditions, an ordered risk space `(V_q,preceq_q)`, an acceptable lower set `A_q`, and the target risk map in world `W`. For `s in S`, dependent data include the finite available/evaluated alternatives, certificate/support relation, dependency relation, resource/search bounds, and abstract provenance. A request becomes:

```text
(s,e,q,P)
```

rather than carrying a 14-field record through every theorem.

The former nominal sorts are retained as follows:

- `Agent`, `Stage`, `Budget`, `Record`, `Library`, `Search`, evidence events, and full provenance become indices or fields/elaborations of `S`;
- task, case, prediction, outcome, action, domain, frame, loss, risk, tolerance, and certificate mode become dependent data of `Q` or parameters of requirement atoms;
- fallback, cost, selector, and purpose become fields of a use plan/context or profile parameters;
- theory frameworks, bridges, full event taxonomies, checksums, and audit records remain extensions;
- instantiated model identity survives through a pure-model embedding into `E`; version/genealogy is not quotiented away.

Compression must preserve world versus stage, model/use plan versus theory family, carrier versus distribution, prediction/outcome/action typing, hard adequacy versus fallback improvement versus comparison versus selection, universe versus finite evaluated set, `Refused/Withheld/Undefined`, lapse versus rebuttal, tolerance versus certificate uncertainty, partial transports, profile identity, and dependency-sensitive provenance.

Task 13 must provide an elaboration-invariance theorem: two detailed records with the same compact reduct and atom diagnostics have the same core license status. This lets code retain rich records without forcing the paper to treat every record field as primitive mathematics.

### Finding 3: reason codes should factor through atoms and evidence

The four outcomes remain valuable, but the flat “typical reasons” list is already open-ended and inconsistent as a putative syntax. Some names are unused, downstream files add many more, `BrokenProvenance` legitimately appears at two statuses, and `NoLicensedModel` is actually a selector-level consequence of an empty active set.

The planned core therefore uses two phases:

```text
WF(P,e,q,s)                         -- type/denotation/executability
v_s(r;e,q) in K_3={-,?,+}          -- refuted/open/supported
v_s(P;e,q)=meet_{r in Req(P)} v_s(r;e,q).
```

Then:

```text
not WF                  -> Undefined
WF and meet=+           -> Granted
WF and meet=?           -> Withheld
WF and meet=-           -> Refused.
```

`Undefined` is thus not an evidential severity and cannot mask a simultaneous safety refusal in the semantics: atom assessment begins only after the request is meaningful. A diagnostic is indexed rather than enumerated:

```text
Diag(r)=<atom r, value in K_3,
         positive witness?, counterwitness?, obstacle?, provenance>.
```

Readable displays derive from this structure. For example, `HardRiskViolation` renders a refuted adequacy atom with a countercertificate; `CertificateStraddlesBoundary` renders an open adequacy atom with a boundary obstacle; and `FrameMismatch` renders a failed `WF` derivation. Safety projections select refuted/open atoms from the profile's declared safety subset. A closed global reason enum and a learned reason-classification head are unnecessary.

This compression creates useful supporting theorems: status normal form; commutative/associative/idempotent meet; four-outcome observational minimality; loss of atom identity under aggregate status; and exact safety projections. These results clarify the design but do not replace the paper-carrying theorem spine above.

### Roadmap effects of the amendment

1. Task 11B implements and tests the compact `WF + K_3` kernel while reproducing the legacy witness labels.
2. Task 13 replaces the 28-sort presentation with `E,Q,S`, semantic `W`, finite profiles, dependent data, and an elaboration map.
3. Task 14 owns update/profile/diagnostic characterizations, not a miscellaneous list of elementary consequences.
4. New Task 14A owns expected-risk restriction, routed-risk, and bridge-risk bounds.
5. Tasks 16–19 use atom-indexed state/witness data and derived reasons, not a flat reason vocabulary.
6. Task 17 owns the hard-routing seam characterization and exact ReLU-plus-symbolic-decoder result.
7. Checkpoint B must count characterization/impossibility results separately from definitions and standard lemmas and add a proof repair if the spine remains thin.

No current theorem is claimed proved by this amendment. It chooses targets, simplifies the future core, and prevents the executable reference from freezing the verbose historical schema.

## Revised next task

> **Task 11B — Mechanize and test the integrated finite witness.**

This checkpoint stops here and does not begin Task 11B.
