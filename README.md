# Value Logic

Value Logic is a research project about reasoning with useful but fallible models under open-ended theory succession. It begins with a practical and philosophical question:

> If we cannot know that our models give us final metaphysical truth, what should reasoning preserve, and what justifies using one model rather than another?

The project's proposed starting point is **value**: how a model, theory, representation, or course of action serves an intended purpose, at a tolerable error and resource cost. The ambition is not just to attach usefulness scores to otherwise conventional judgments. It is to investigate a calculus in which semantic objects and inference rules make pragmatic value central, with familiar truth-based reasoning potentially recovered within a suitable fragment.

**Phase one is complete. Phase two is building the value-based calculus first. F01, F02 and F03 are complete at their task scopes; the next task is F04, hostile examples and candidate discrimination.** The motivation below is the continuing research program. The particular constructions developed so far are realizations of it, not permanent foundations.

## Motivation: useful does not mean final

Newtonian physics is the guiding example. Relativity and quantum theory expose limits to an unrestricted Newtonian description, but that does not make a Newtonian calculation worthless. On an appropriate domain it may provide the accuracy a task needs, with less computational work, fewer measurements, or a more transparent explanation than a more elaborate model. A successor can restrict a predecessor's scope without eliminating its practical value.

We also expect our present physical theories to be extended or superseded. The project takes seriously the possibility that this process has no knowable endpoint: an agent may never be entitled to announce that it finally possesses the ultimate theory. That is a motivation for the research, not a theorem that every theory must have a successor. The [phase-one paper](paper.md) develops the physics example and its sources in detail.

Mathematics raises a related question at another level. A proof operates within stated axioms and inference rules; choosing an axiomatic framework is a different question from deriving a theorem within it. Choices such as accepting the axiom of choice need not be treated as a universally compulsory foundation for every purpose. Value Logic does not assume access to a uniquely privileged axiomatic system. It asks how expressive power, useful deductions, tractability, and the intended task can bear on the use of a framework, while keeping its actual mathematical assumptions explicit.

The common problem is **how to reason and act before finality**. Lack of access to absolute truth is not a reason to stop modeling. Nor does usefulness settle whether a model is metaphysically true or false. We can instead ask where it works, what error we can tolerate, what it costs, what alternatives exist, and what evidence would make us revise our reliance on it.

## Why value is the proposed primitive

The foundational proposal is to begin with value-related distinctions rather than require an unqualified true/false verdict as the operational primitive. A model may be better for one task and worse for another. It may be good enough without being the best available model, or cease to be the preferred choice while remaining worth retaining for a different domain or budget.

Here “value” is broader than a probability, a truth degree, money, or one universally correct utility function. A scalar reward or loss is one possibility. A context-dependent function, an ordered structure, or an attainable set of guarantees may preserve distinctions that a single evaluated score loses. Conversely, more structure is not automatically better: the representation should retain what the intended reasoning needs, rather than copy every detail of the original object.

Unbounded values remain an explicit part of the investigation. The project does not assume that all useful semantic quantities must lie in a fixed interval such as `[0,1]`. Bounded encodings are also allowed, but their operations and precision must preserve the intended conclusions; applying a squashing function is not by itself an equivalence of calculi.

Three linked questions therefore guide the foundations work:

1. **What carries meaning?** What value objects represent the task-relevant content of an expression or model use?
2. **What follows from what?** Which conclusions about value, adequacy, or possible use are justified by which premises?
3. **How does meaning compose?** What information must survive joint use, sequential use, changes of task, and revision?

Ordinary mathematical proofs remain available in an explicitly stated metatheory. Treating value as the proposed operational primitive does not require abandoning rigorous derivation, and the philosophical motivation does not uniquely force one algebra.

## The original practical questions remain

The scientific-model motivation leads to more than ranking whole theories. An older model and a successor can have overlapping useful domains. A task may require a composition of models, a translation between their outputs, a router choosing where to use each, or a fallback when no available option meets the requirements. The reasoning needs to account for error propagation, resource use, and the evidence supporting each step.

The project consequently distinguishes empirical adequacy, permission to rely, comparative preference, current selection, and archival retention. It asks how these can change when evidence is revised or a better model becomes available, and how a local change should affect downstream conclusions without needlessly discarding unaffected work. A named fallback has its own consequences; doing nothing is not automatically a cost-free or adequate alternative.

A further original goal is to make this reasoning representable and learnable. Phase one used a basic ReLU multilayer perceptron as a reference architecture and tested structured numerical proposals against direct classification. That engineering direction remains part of the broader project, but ReLU, cross-entropy, and any particular network architecture are not axioms of Value Logic.

The earlier writing also explores relationships among values, beliefs, task judgments, and black-box behavior. One longer-term hope is that a value-based view could help explain an agent's policy, rather than merely reproduce its outputs. The [original essays and exploratory notes](posts/) and [conversation records](llm_convos/) preserve those origins. These are research motivations and possible later branches, not claims that behavioral reconstruction already establishes interpretability or recovers a uniquely true utility.

## Current emphasis: loss-grounded, reflective, and interpretable

The active direction connects pragmatic value to losses and rewards used in
machine learning, treated as revisable proxies rather than final utility.
Rational Lawvere-style arithmetic is a starting comparison, with cost/value
meaning beyond degrees of truth. Modest self-assessment and uncertainty about
evaluators are active capability targets. Neural interpretation seeks structure
learned by ordinary networks, not only architectures built to implement a logic.
[DIR01](v2/decisions/DIR01_loss_grounded_reflective_direction.md) specifies this
direction, its scope and its open choices; the [opportunity register](v2/opportunities.md)
guides bounded agent initiative. F03 remains complete; F04 is next, not yet run.

## What phase one established

The completed paper, [*Value Logic: Scoped Reliance on Fallible Models Under Open-Ended Succession*](paper.md), developed one finite-stage, evidence-relative calculus of licensed reliance. A request identifies a use plan, context, epistemic state, and requirement profile. Malformed requests are separated from meaningful requirements assessed as supported, open, or refuted; their combination yields `Granted`, `Withheld`, or `Refused`, with `Undefined` reserved for failed well-formedness.

Its results address profile refinement, open-ended succession, revision locality, model composition, domain transport, and what an implementation must preserve. It separates learned numerical proposals from the exact evidence, provenance, and selection checks required by that realization. The [formalism](formalism/), [verification suite](verification/), and [code guide](CODE_GUIDE.md) retain the details.

The [synthetic experiment](experiments/02_results.md) had mixed results: the structured pipeline transferred better when tolerances changed, but lost other registered comparisons and sent almost all target-weighted cases to fallback. Representational success was therefore not treated as evidence of general operational usefulness. The completed research and its negative results remain intact.

Phase one is a completed realization, **not an immutable definition of the project**. Its results may be reused with their assumptions, adapted, or compared against a different foundation. The [original task history](TODO.md), [detailed phase-one README](README_phase1_archive.md), and [public-facing adaptation](substack_post.txt) remain available.

## Phase two: build the value-based calculus first

The current phase asks:

> What semantic objects and inference rules let an agent draw conclusions justified by preservation of pragmatic value, rather than merely attach scores to conventional judgments?

**F01 — requirements and separating examples — is complete.** Eight worked examples and a reconstruction audit examine cost versus accuracy, task changes, hidden dependence, joint and sequential composition, incomplete or conflicting evaluation, toy axiomatic systems, unbounded values, and information-dependent decisions. A central lesson is that a summary can be insufficient for an exact answer yet sufficient for the guarantee or tolerance actually requested. See the [examples](v2/foundations/01_requirements_and_separating_examples.md) and [reconstruction](v2/foundations/01a_reconstruction_and_information_contracts.md).

**F02 — competing semantic candidates — is complete at its comparison scope.** It develops four concrete alternatives rather than selecting a permanent core:

| Candidate | What carries the meaning | Main question it helps expose |
|---|---|---|
| Evaluated scalars | A numerical evaluation for a fixed task | When is a compressed score sufficient? |
| Aligned value profiles | Values across shared scenarios | Which joint distinctions must composition preserve? |
| Continuation-value transformers | How a step maps downstream goals to present value | How should value propagate through sequential use? |
| Achievable guarantee sets | Combinations of requirements an available use can satisfy | What is achievable without forcing all constraints into one tradeoff score? |

The [candidate comparison](v2/foundations/02_candidate_semantics.md) and [continuation audit](v2/foundations/02a_candidate_reconstruction.md) give operations, worked examples, restrictions, and connections among these alternatives. Their 124 dedicated checks are development evidence for the stated examples, not a soundness proof for an adopted calculus. The [F02 completion record](v2/work_logs/F02_2026-09-22_S2.md) preserves the research and timing evidence.

**F03 — external foundations audit — is complete.** The [source-use register](v2/literature/F03_import_contracts.json), [theorem agenda](v2/literature/01i_calculus_desiderata_and_theorem_agenda.md), and [phase-one comparison](v2/literature/01j_phase_one_literature_and_novelty.md) distinguish established ingredients, scoped imports and future contribution opportunities. The [completion record](v2/work_logs/F03_2026-09-24_S10.md) retains evidence and measured review time.

**Next: F04 — hostile examples and candidate discrimination.** No permanent calculus has been chosen and no readiness gate has passed. Later work must still develop operational semantics, nontrivial inference rules, soundness and characterization results, and an executable reasoner with evidence of useful composition. The authoritative status and continuation pointer are in [TODO_v2.md](TODO_v2.md).

The former contract-semantics and inverse-task-recovery plan is preserved in [TODO_v2_contracts_archive.md](TODO_v2_contracts_archive.md). It remains a possible future direction, alongside model substitution, inquiry and self-revision, learning, and policy interpretability. There is no fixed limit on later phases.

## Working method and validation

Follow [TODO_v2.md](TODO_v2.md) and the [research protocol](v2/RESEARCH_PROTOCOL.md), not an archived queue. One selected task or gate attempt is the scope of a session unless a batch is explicitly requested. Derivations and worked equations, external literature checks, and executable tests remain distinct evidence streams. Forecast effort before work, record actual clocks, respect protected research minimums, and allocate time to both reliable gains and difficult, uncertain ideas.

Readiness gates can send the project back to an earlier definition, proof, or experiment. A failed candidate is recorded rather than hidden, completed history is preserved, and passing tests or spending time does not substitute for a missing argument. Commit validated work with its task ID; publish repository changes when authorized. The present F02 publication and README restoration were explicitly requested by the author.

The existing full repository command is:

```text
python -m verification
```

For the F02 fixtures alone, using the Python standard library:

```text
python -m unittest discover -s verification -p 'test_v2_f02*.py'
```

The dedicated result is 124 tests. Full-suite dependencies and the distinction between fixture checks and the future reasoner are described in [v2/README.md](v2/README.md), [CODE_GUIDE.md](CODE_GUIDE.md), and the [CI workflow](.github/workflows/verify.yml). The exact commit's GitHub Actions result is the publication validation record.

## Repository guide

- [TODO_v2.md](TODO_v2.md), [v2/project_spec.md](v2/project_spec.md), [v2/claim_ledger.md](v2/claim_ledger.md), and [v2/notation.md](v2/notation.md): current plan, scope, evidence, and terminology.
- [v2/foundations/](v2/foundations/), [v2/checks/](v2/checks/), and [v2/work_logs/](v2/work_logs/): phase-two theory, executable examples, and session records.
- [paper.md](paper.md), [formalism/](formalism/), [ml/](ml/), [experiments/](experiments/), and [notes/](notes/): completed phase-one results and supporting material.
- [posts/](posts/), [llm_convos/](llm_convos/), and [substack_post.txt](substack_post.txt): intellectual origins, exploratory discussions, and public exposition.

The project continues from the original motivation: **reasoning should remain useful, compositional, and revisable even when final truth is unavailable.** Each phase is an attempt to make that idea mathematically and operationally concrete.
