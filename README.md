# Value Logic

Value Logic is a research project about reasoning with useful but fallible models under indefinitely extendable theory succession.

The motivating example comes from physics: a successor theory can show that an older theory is not universally correct while leaving it reliable, efficient, or otherwise useful on a restricted domain. If this process can continue indefinitely—and a bounded agent cannot know that it has reached a final theory—what kind of logic should govern present model use?

The project asks whether a finite-stage, domain-relative logic of licensed reliance can represent:

- empirical adequacy without a claim of final truth;
- explicit task, loss, tolerance, evidence, and fallback conditions;
- overlapping model domains, gaps, routing, and bridge conditions;
- simultaneous usability, comparative preference, current selection, and archival retention;
- revision after new evidence or the addition of a better model; and
- a learnable implementation using a basic ReLU multilayer perceptron and structured losses.

## Current formal direction

The central judgment is profile-indexed:

```text
Lic_P
```

Here `P` is a finite requirement profile. It states which adequacy, fallback, constraint, provenance, comparison, or related conditions are required and which are merely reported. Bare, unqualified `Lic` is intentionally undefined.

The current canonical profiles distinguish pragmatic reliance from two strengths of finite comparative preference:

- `P_rely`: adequacy, improvement over an explicit fallback, hard constraints, and traceability;
- `P_pref-rel`: reliance plus no certified dominator in the evaluated set, with unresolved comparisons disclosed; and
- `P_pref-cert`: reliance plus resolved non-domination or ineligibility for every relevant evaluated candidate.

None of these judgments claims global optimality, universal truth, or immunity from later revision.

The detailed typed records in the early formalism are now treated as an elaboration/implementation schema. The canonical paper-level core in [`formalism/07_core_calculus.md`](formalism/07_core_calculus.md) uses three principal carriers—evaluated use plans, reliance contexts, and finite epistemic states—with target worlds as a semantic index and profiles as finite parameterized syntax. Its four public outcomes are derived compactly: failed well-formedness gives `Undefined`; otherwise each requirement is refuted, open, or supported, and finite meet gives `Refused`, `Withheld`, or `Granted`. Named reason codes are diagnostic renderings of atom-indexed witnesses or obstacles, not primitive logical types.

## Repository map

- [`TODO.md`](TODO.md) is the resumable project-control document and identifies the next task.
- [`formalism/`](formalism/) contains the developing mathematical semantics, update rules, dominance results, atlas machinery, and integrated witness model.
- [`notes/`](notes/) contains the project specification, claim ledger, literature map, checkpoint records, and focused research notes.
- [`posts/`](posts/) contains earlier motivational writing. It informs the narrative but is not treated as proof or external evidence.
- [`llm_convos/`](llm_convos/) contains the conversations from which several initial ideas were extracted and critically assessed.
- [`verification/`](verification/) contains the standard-library executable semantics, integrated finite witness, tests, and local-link checker.
- [`references.bib`](references.bib) is the working bibliography.

The planned final public artifacts are:

1. `paper.md`, a LaTeX-heavy, GitHub-Gist-compatible paper; and
2. `substack_post.txt`, a low-LaTeX, non-Markdown adaptation for Substack.

## Working method

Work proceeds one numbered task or checkpoint per prompt. To resume the project in a fresh context:

1. read [`TODO.md`](TODO.md);
2. follow its **Next task** pointer unless a different task is explicitly requested;
3. complete exactly that task or checkpoint;
4. update its completion record, affected specifications, and claim dispositions; and
5. stop before beginning the following item.

Claims are classified before being accepted or rejected. A claim is first treated as supported, falsifiable and awaiting a test, or likely unfalsifiable. It is marked falsified only after a counterexample, proof, or sufficiently relevant empirical result is supplied; a replaced definition is instead recorded as a superseded design default. Every falsified inherited claim also records its impact on the overall project.

The historical interfaces in `formalism/01_signature.md` through `formalism/05a_integration.md` are detailed elaborations and provenance records. Their bare `Lic`, four-chain atom statuses, or unindexed current-use notation must be read through the canonical request, profile, and `WF + K_3` calculus in [`formalism/07_core_calculus.md`](formalism/07_core_calculus.md).

## Project status

Tasks 0–13, Checkpoint A, and the unscheduled external-audit Checkpoint A1 are complete. The finite-stage licensing interface, consequence and update rules, dominance and retention distinctions, overlapping scientific-model cover, bridge taxonomy, and a repaired integrated finite witness have been developed. The compact `WF + K_3` semantics and the complete finite witness are executable and tested with `python -m verification`. Continuation semantics separates current grants, eventual stability, certified stability, semantic finality, and optional truth. The core-related literature has been audited against primary sources with explicit theorem-transfer boundaries. The compact core calculus now fixes the canonical request `(s,e,q,P)`, proves each coordinate indispensable by finite separators, and states the metatheory program.

The current next step is Task 14: proving or refuting the compact core's metatheory.

See [`TODO.md`](TODO.md) for the authoritative and most current status.
