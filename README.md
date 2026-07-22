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
- [`CODE_GUIDE.md`](CODE_GUIDE.md) explains every Python/C++ component, common commands, experiment artifacts, and safety boundaries in plain language.
- [`formalism/`](formalism/) contains the developing mathematical semantics, update rules, dominance results, atlas machinery, and integrated witness model.
- [`notes/`](notes/) contains the project specification, claim ledger, literature map, checkpoint records, and focused research notes.
- [`posts/`](posts/) contains earlier motivational writing. It informs the narrative but is not treated as proof or external evidence.
- [`llm_convos/`](llm_convos/) contains the conversations from which several initial ideas were extracted and critically assessed.
- [`verification/`](verification/) contains the standard-library executable semantics, integrated finite witness, tests, and local-link checker.
- [`ml/`](ml/) contains the architecture-neutral encoding contract and, in later tasks, the reference neural architecture, representation results, and loss design.
- [`experiments/`](experiments/) contains the preregistered synthetic study design, pilot, frozen protocol, implementation, completed run checkpoints, analysis, figures, and results.
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
5. run local verification, and once the commit is pushed confirm public CI is green or record why it is not; then stop before beginning the following item.

Claims are classified before being accepted or rejected. A claim is first treated as supported, falsifiable and awaiting a test, or likely unfalsifiable. It is marked falsified only after a counterexample, proof, or sufficiently relevant empirical result is supplied; a replaced definition is instead recorded as a superseded design default. Every falsified inherited claim also records its impact on the overall project.

The historical interfaces in `formalism/01_signature.md` through `formalism/05a_integration.md` are detailed elaborations and provenance records. Their bare `Lic`, four-chain atom statuses, or unindexed current-use notation must be read through the canonical request, profile, and `WF + K_3` calculus in [`formalism/07_core_calculus.md`](formalism/07_core_calculus.md).

## Project status

All scheduled work through Task 26, including Task 22B and the other completed suffixed tasks, and Checkpoints A, A1, B, C, C1, and D is complete. The finite-stage licensing interface, consequence and update rules, dominance and retention distinctions, overlapping scientific-model cover, bridge taxonomy, and a repaired integrated finite witness have been developed. The compact `WF + K_3` semantics and the complete finite witness are executable and tested with `python -m verification`. Continuation semantics separates current grants, eventual stability, certified stability, semantic finality, and optional truth. The compact core fixes `(s,e,q,P)` and has profile, diagnostic, soundness, update, and composition metatheory. Its quantitative extension characterizes subdomain restriction, decomposes hard-router risk, bounds bridge/blend task risk, propagates finite plan-DAG errors, and audits exact bridge cycles.

Task 14B closed Checkpoint B's focused repair gate. It proved every frozen atom evaluator local to a finite typed read footprint, including negative collection-index reads, and made the canonical event/write graph change-complete. [`Task 14C`](formalism/08c_proof_carrying_plans.md) then proved that finite typed plan DAGs can jointly compute payloads, propagate quantitative grades, and construct checked composite certificates whose erasure is the ordinary computation. It also established grounded finite-DAG provenance and unique finite-rank assessment of a frozen value-logic implementation, while showing that self-endorsement alone is not target-world evidence.

[`Task 15`](ml/01_encodings.md) now fixes the architecture-neutral boundary: an atom input is its exact address plus dependency-scoped record projection; a learned module may propose continuous statistics and envelopes; exact validity, checker/certificate/provenance identity, `WF`, diagnostic decoding, aggregation, masking, and fallback remain external. It also distinguishes a status-minimal query quotient from an audit-preserving code, fixed indexed from candidate-conditioned libraries, and flat from typed-DAG plan encodings while keeping payload, grade, and evidence separate.

[`Task 16`](ml/02_relu_architecture.md) now instantiates that contract as a hybrid ReLU reference architecture. Learned center/region, uncertainty, validity, payload, and grade proposals remain distinct from accepted calibration/checker evidence; the symbolic layer derives inclusive-boundary diagnostics, profiles, active masks, and fallback. Named normalized hypothesis channels may use positive ReLU slack downstream, while separate content/grade channels remain the general default.

The controlling interpretation rule is deliberately strict. For `z=ReLU(s)`, the only unconditional meaning of `z>0` is `s>0`. An arbitrary hidden preactivation supplies no adequacy semantics. If `s` is a named learned margin, `z>0` records **predicted** positive slack. If `s` is instead a conservative support margin constructed from an accepted envelope, `z>0` records strict **certificate-relative surplus for that one atom and scope**. It is still not a full license or a world-truth claim: exact evidence validity, polarity, `WF`, boundary state, every required profile atom, and the active mask remain necessary. Conversely, `z=0` merges supported equality with negative, open, refuted, missing, and invalid cases and does not quarantine biases or bypass paths.

The [canonical worked example](ml/02_relu_architecture.md#84-worked-toy-one-plan-three-requirements) applies this rule to loss adequacy, improvement over a fallback, and a latency constraint. It shows all six boundary/evidence cases, encodes `A and I and C` as an audit-preserving vector, computes its grant bit with a fixed ReLU conjunction over exact state bits, reuses normalized surplus in a later ranking calculation, and explains why neither the surplus nor the ranking score can replace the full license and active mask. It also distinguishes learned heads from output/decoder channels: multiple channels per atom are generally necessary, while `z_support` and `z_refute` may be fixed transformations of one shared learned interval and are still insufficient without exact state and evidence channels.

[`Task 17`](ml/03_representation_theorems.md) now supplies the representation theorem spine: exact status/audit factorization, conservative robust decoding, finite CPWL/ReLU realization, the hard-seam characterization and discontinuity obstruction, fixed-versus-expandable library limits, a named dual-use channel construction with scale and boundary counterexamples, and exact proof-erased finite-plan payload/grade computation. Its minimality statement is explicitly relative to a coordinate-complete consumer family, not an information-theoretic optimum. These results preserve the external evidence, decoder, certificate, mask, and fallback boundary and do not claim learnability or semantic alignment.

[`Task 18`](ml/04_losses.md) now fixes the learning contract: standardized schema-balanced center–radius statistic regression plus interval scoring, disjoint held-out calibration, exact polarity-aware symbolic decoding, conservative learned rejection, independent atom cross-entropy as a nonauthorizing baseline, and separate exact-mask router ranking with risk–coverage/fallback accounting.

[`Checkpoint C`](notes/checkpoints/C_neural_blueprint.md) confirms that the formal, neural, and objective layers form one implementable hybrid pipeline, while adding a scorer-input firewall, proposal-bound calibration records, five blocked evidential roles, and separate system-audit/confirmation roles. It narrows the minimum publishable experiment to the structured-versus-cross-entropy and marginal-calibration claims plus core failure ablations. No alternative architecture enters that minimum core; hard MoE is the only optional comparator and must pass a separate seam-power gate. The checkpoint also freezes a provisional reader-facing answer to why this value-logic design plausibly fits ReLU while repairing the stale idea that a positive activation grants or zero quarantines by itself.

[`Task 19`](experiments/01_design.md) preregisters the decisive experiment before implementation. It freezes an independent synthetic succession/oracle law, the reusable `A and I and C` fixture, nonleaking inputs, immutable calibration binding, five lineage-blocked roles, exact target/design reweighting, numerical superiority/noninferiority margins, world-level paired inference and power, required failure ablations, and a final-test embargo. It also distinguishes marginal target-in-proposal coverage from finite usable evidence: an infinite proposal can preserve the former guarantee while forcing the atom Open. Hard MoE and certificate/system studies remain separately gated extensions.

[`Task 19A`](experiments/00_pilot.md) implements and freezes the generator, exact oracle/decoder, scorer firewall, proposal binding, metric/power skeleton, and lineage manifests after a 256-world pilot. It fixes 5,000 worlds for each confirmatory downstream role and 20,000 train worlds while leaving every production payload ungenerated. The pilot repairs finite dominance with paired-difference certificates and uses disclosed conservative design bounds rather than pretending to observe pre-learner variance. Hard MoE is prospectively omitted; the system tier remains a deterministic integration witness.

[`Task 20`](experiments/02_implementation.md) implements the matched structured and atom-cross-entropy ReLU arms, required ablations, independent-world calibration, proposal binding, exact symbolic states and masks, routing/fallback, trace schema, and deterministic certificate/system witness. Its frozen entry point verifies source/config hashes and cannot materialize confirmation worlds until the explicit Task 21 command. A 16-world pilot-role smoke test passed exactly reproducibly; it is not an empirical result. Every production payload remains ungenerated, and `F35/F36` remain untested.

[`Task 20R`](experiments/03_execution_repair.md) repairs the failed full-scale execution path without changing the frozen scientific design. It replaces millions of repeated Python-object audits with direct NumPy/PyTorch blocks and a small allocation-free C++ decoder, adds exact differential/native tests, and separates the future run into atomic resumable stages. Its pilot preserved discrete outputs exactly and passed the performance gate. It used pilot-role data only: no v1.1 production or final-confirmation payload was generated, and `F35/F36` remain untested.

[`Task 21`](experiments/02_results.md) completed that staged frozen run once. The structured center–radius arm decisively beats direct `K_3` cross-entropy under changed tolerances, but decisively loses the registered boundary and ordinary in-regime comparisons. Registered marginal target-in-proposal coverage passes for both `J` and `T`. The machine-readable analysis, figures, stage hashes, execution deviations, unavailable secondaries, and claims not made are committed; large reproducible raw/model/trace products remain local and ignored by Git.

[`Checkpoint C1`](notes/checkpoints/C1_empirical_adjudication.md) preserves aggregate `F35=I1` as **mixed with decisive opposing effects**, while recording the registered components separately: no-retraining changed-tolerance generalization is `F35a=S1`, and boundary superiority plus in-regime noninferiority are `F35b/F35c=X1` at their registered margins. `F36=S1` remains marginal proposal coverage only. The structured arm's low false-assertion rates coexist with large misses and `0.9962` fallback mass, so calibrated withholding and useful licensed coverage are now explicit separate objectives. Hard MoE has no empirical disposition; the system tier remains a deterministic integration witness; and no confirmation rerun is authorized. Conservative dead-band geometry is a theory-consistent leading explanation, not an identified causal decomposition or proof that one invariant region was reused.

The checkpoint also repaired a public artifact-transport erratum: seven frozen JSON files now retain their registered CRLF bytes under [`.gitattributes`](.gitattributes), while new experiment versions can use the explicit LF writer in [`experiments/artifact_io.py`](experiments/artifact_io.py). Historical source hashes and scientific results were not changed. A later public run reached the repaired artifacts but failed because the workflow did not install the experiment/analysis imports; Checkpoint D added pinned NumPy, Matplotlib, and CPU PyTorch dependencies. After the authorized Task 22B push, [public run 29887626439](https://github.com/TristanMiano/value_logic/actions/runs/29887626439) passed at exact head `2e6c85969fa4e8c5aa54de8c227bf770ab74d5e4`.

[`Task 22`](notes/policy_value_judgment.md) preserves a finite representational policy–value isomorphism/existence result: after fixing a scalar or action-score encoding and decoder, a policy has a lossless value-like representation and the maps are inverse on the encoder image. It separately shows that standard `V^pi`, `Q^pi`, and occupancy are not unique, natural, policy-only inverse representations. The companion's defensible operational scope is **environment-relative policy evaluation with conditional behavioral reconstruction**. The recorded author motivation is to treat a value surrogate as a potentially interpretable high-level model of a deliberately general black-box policy. The project does not ask whether a true utility exists or claim that the surrogate recovers one; behavioral agreement alone still does not establish semantic or mechanistic interpretability.

[`Task 22A`](formalism/09_judgment_information.md) proves a scoped version of the recursive-judgment information claim. Positive population strict-proper-score improvement over the true nuisance-conditioned Bayes baseline implies positive `I(J;Y|N)`; a `delta`-nat log-loss gain gives `I(J;Y|N)>=delta`. Under explicit mediation, the bound transfers to the outcome-identifiable task quotient. Non-Bayes comparators, omitted nuisance, leakage, duplicated task types, instability, calibration alone, and copying delimit the result.

[`Task 23`](notes/policy_value_interpretability.md) designs the optional bridge and records its current empirical status. It treats value as the author's first promising semantic foothold from black-box behavior. The project makes no claim that value is metaphysically primitive or that a recovered surrogate is true utility. A licensed `V/Q` view exposes declared return/ranking content, domain, margins, counterfactual transitions, local surrogate rules, abstentions, and traces. Evidence remains seven-dimensional: behavioral, value, outcome/task-quotient, domain, representational, causal, and human. The pinned companion has not run the proposed representation, intervention, shift/usefulness, or human tests; `F35a` supplies changed-tolerance evidence in the separate synthetic experiment, and `0.9962` fallback mass prevents a usefulness claim for that structured configuration.

[`Task 24`](notes/limitations.md) consolidates the project's paper-facing boundaries into six constructive matrices. Each row identifies the assumption exposed by a theorem, counterexample, regression, or experiment; states the narrower result that remains available; and assigns the material to main text, appendix, or future work. The central empirical row is **calibrated but nearly non-granting**, which places `F36` coverage beside unweighted trace miss rates `0.4611/0.3248` and target-weighted fallback mass `0.9962`. The matrix also records the matched-coverage drift, unavailable `21-D3` secondaries, and a prospective trace contract retaining target/design weights, polarity, evidence mode, diagnostics, and deployed-risk fields.

[`Task 25`](paper_outline.md) freezes the public argument around four formal contribution clusters: the profile-indexed calculus, the open-ended stability package, typed update locality, and an architecture-neutral representation contract with a finite ReLU reference witness. Standard formal integrations, the mixed experiment, the optional policy/value case, and interpretive motivation are kept separate. Its 500-word lead answer and 136-word abstract give the empirical asymmetry equal billing: tolerance transfer and marginal proposal coverage are supported at their registered scopes, the registered boundary-superiority and in-regime noninferiority propositions are refuted at their margins, and usable coverage is poor. One Task 19 succession example derives `epsilon` from fallback before neural notation and carries the argument through overlap, gaps, revision, changed tolerances, and finite retention. The finite policy/value representation-existence claim remains intact; standard-return semantics, identification, practical learning, and true-utility recovery are separate questions. ReLU remains one reference witness, and the project makes no claim of architectural uniqueness or presumptive optimality.

[`Checkpoint D`](notes/checkpoints/D_predraft.md) confirms that this publication contract forms a coherent human argument and inserted one bounded bridge-rigor gate before drafting. [`Task 22B`](formalism/10_policy_value_reconstruction.md) has now discharged that gate. It proves the distribution-scoped raw action-gap bound for approximate policy reconstruction, its accepted-evidence and held-out IID certificate routes, and the separate conservative `4 rho` sufficient condition for recovery plus non-abstention. The exact encoder-image isomorphism/existence proposition remains available; arbitrary scores, return-semantic `Q`, scalar `V` plus a transparent harness, stochastic policies, off-support behavior, and trajectories retain distinct scopes. The finite [verification kernel](verification/policy_value_reconstruction.py) exercises the tight boundaries and countermodels. No companion run, architecture comparison, matched-coverage rescue, or Lean task was added.

[`Task 26`](paper.md) begins the formal paper with its title, abstract, reader-facing introduction, one synthetic succession decision, and related work by claim boundary. It derives `epsilon` from both external requirements and the declared fallback before neural notation, separates plan granularity and modeled loss, states the profile-indexed judgment as a design choice, and places the complete frozen transfer-versus-coverage asymmetry beside the ReLU motivation. The optional policy/value bridge is foreshadowed while retaining the exact finite encoder-image existence claim and true-utility neutrality. **Task 27 is next.**

See [`TODO.md`](TODO.md) for the authoritative and most current status.
