# Value Logic

Value Logic is a research project about reasoning with useful but fallible models under indefinitely extendable theory succession.

The motivating example comes from physics: a successor theory can show that an older theory is not universally correct while leaving it reliable, efficient, or otherwise useful on a restricted domain. If this process can continue indefinitely—and a bounded agent cannot know that it has reached a final theory—what kind of logic should govern present model use?

The project asks whether a finite-stage, domain-relative logic of licensed reliance can represent:

- empirical adequacy without a claim of final truth;
- explicit task, loss, tolerance, evidence, and fallback conditions;
- overlapping model domains, gaps, routing, and bridge conditions;
- simultaneous usability, comparative preference, current selection, and archival retention;
- revision after new evidence or the addition of a better model; and
- a learnable implementation using a basic ReLU multilayer perceptron as the reference architecture, structured losses, and narrowly motivated alternatives where useful.

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
- [`ml/`](ml/) contains the architecture-neutral encoding contract and, in later tasks, the reference neural architecture, representation results, and loss design.
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

Tasks 0–18, Checkpoints A–C, and the unscheduled external-audit Checkpoint A1 are complete. The finite-stage licensing interface, consequence and update rules, dominance and retention distinctions, overlapping scientific-model cover, bridge taxonomy, and a repaired integrated finite witness have been developed. The compact `WF + K_3` semantics and the complete finite witness are executable and tested with `python -m verification`. Continuation semantics separates current grants, eventual stability, certified stability, semantic finality, and optional truth. The compact core fixes `(s,e,q,P)` and has profile, diagnostic, soundness, update, and composition metatheory. Its quantitative extension characterizes subdomain restriction, decomposes hard-router risk, bounds bridge/blend task risk, propagates finite plan-DAG errors, and audits exact bridge cycles.

Task 14B closed Checkpoint B's focused repair gate. It proved every frozen atom evaluator local to a finite typed read footprint, including negative collection-index reads, and made the canonical event/write graph change-complete. [`Task 14C`](formalism/08c_proof_carrying_plans.md) then proved that finite typed plan DAGs can jointly compute payloads, propagate quantitative grades, and construct checked composite certificates whose erasure is the ordinary computation. It also established grounded finite-DAG provenance and unique finite-rank assessment of a frozen value-logic implementation, while showing that self-endorsement alone is not target-world evidence.

[`Task 15`](ml/01_encodings.md) now fixes the architecture-neutral boundary: an atom input is its exact address plus dependency-scoped record projection; a learned module may propose continuous statistics and envelopes; exact validity, checker/certificate/provenance identity, `WF`, diagnostic decoding, aggregation, masking, and fallback remain external. It also distinguishes a status-minimal query quotient from an audit-preserving code, fixed indexed from candidate-conditioned libraries, and flat from typed-DAG plan encodings while keeping payload, grade, and evidence separate.

[`Task 16`](ml/02_relu_architecture.md) now instantiates that contract as a hybrid ReLU reference architecture. Learned center/region, uncertainty, validity, payload, and grade proposals remain distinct from accepted calibration/checker evidence; the symbolic layer derives inclusive-boundary diagnostics, profiles, active masks, and fallback. Named normalized hypothesis channels may use positive ReLU slack downstream, while separate content/grade channels remain the general default. ReLU zero alone is not treated as authorization or quarantine.

[`Task 17`](ml/03_representation_theorems.md) now supplies the representation theorem spine: exact status/audit factorization, conservative robust decoding, finite CPWL/ReLU realization, the hard-seam characterization and discontinuity obstruction, fixed-versus-expandable library limits, a named dual-use channel construction with scale and boundary counterexamples, and exact proof-erased finite-plan payload/grade computation. Its minimality statement is explicitly relative to a coordinate-complete consumer family, not an information-theoretic optimum. These results preserve the external evidence, decoder, certificate, mask, and fallback boundary and do not claim learnability or semantic alignment.

[`Task 18`](ml/04_losses.md) now fixes the learning contract: standardized schema-balanced center–radius statistic regression plus interval scoring, disjoint held-out calibration, exact polarity-aware symbolic decoding, conservative learned rejection, independent atom cross-entropy as a nonauthorizing baseline, and separate exact-mask router ranking with risk–coverage/fallback accounting.

[`Checkpoint C`](notes/checkpoints/C_neural_blueprint.md) confirms that the formal, neural, and objective layers form one implementable hybrid pipeline, while adding a scorer-input firewall, proposal-bound calibration records, five blocked evidential roles, and separate system-audit/confirmation roles. It narrows the minimum publishable experiment to the structured-versus-cross-entropy and marginal-calibration claims plus core failure ablations. No alternative architecture enters that minimum core; hard MoE is the only optional comparator and must pass a separate seam-power gate. The checkpoint also freezes a provisional reader-facing answer to why this value-logic design plausibly fits ReLU while repairing the stale idea that a positive activation grants or zero quarantines by itself.

The current next step is **Task 19: preregister the decisive experiment**. ReLU remains a reference witness rather than a unique or presumptively optimal architecture.

See [`TODO.md`](TODO.md) for the authoritative and most current status.
