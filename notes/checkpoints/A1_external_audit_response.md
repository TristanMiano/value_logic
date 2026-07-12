# Unscheduled Checkpoint A1: Response to the Fable 5 External Audit

Date: 2026-07-11

Trigger: [`llm_convos/claude_audit_2026-07-11.md`](../../llm_convos/claude_audit_2026-07-11.md)

Scope audited: Tasks 0–11A and Checkpoint A

Status: completed; no subsequent formal task begun

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
4. **Status algebra with diagnostic safety.** Task 13 will analyze the four statuses algebraically. Until then, `Diag` is mandatory for action consumers because aggregate `Undefined` can otherwise mask a certified safety refusal in presentation.
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
5. **Task 14 strengthened:** update-persistence characterization and at least one nontrivial theorem/countertheorem; KLM premise postulates no longer treated as the natural primary target.
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

1. The core still lacks a genuinely nontrivial theorem; Tasks 12–14 now own explicit candidates.
2. The finite semantics is not yet executable; Task 11B is now a gate.
3. The neural contribution remains entirely prospective; Checkpoints B and C still gate implementation.
4. The profile preorder remains too weak until Task 13 replaces literal parameterized-atom inclusion with entailment/refinement.
5. The original recursive-judgment narrative remains unsupported until Task 22A.
6. The corpus remains large; durable summaries and canonical consolidation are now required, but no historical artifact was destructively shortened.

## Revised next task

> **Task 11B — Mechanize and test the integrated finite witness.**

This checkpoint stops here and does not begin Task 11B.
