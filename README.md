# Value Logic

**Reasoning with useful, fallible models—and preserving what matters when they change.**

Value Logic investigates how a model, theory, representation or course of action serves an intended purpose, at a tolerable error and resource cost. Its central question is what reasoning should preserve when neither our models nor our criteria for using them can be assumed final.

The project develops mathematical semantics, inference rules, executable checkers and controlled applications. Two research reports present complementary approaches:

- **[Loss Comparisons and Information Retention Under Revision](paper_v2.md)** develops a value-based calculus and studies how much information must survive changes in the costs of correlated procedures.
- **[Scoped Reliance on Fallible Models Under Open-Ended Succession](paper.md)** develops an evidence-relative framework for deciding when a model is licensed for a particular use.

## Motivation: useful does not mean final

Newtonian physics is a guiding example. Relativity and quantum theory expose limits to an unrestricted Newtonian description, but a Newtonian calculation can still deliver the accuracy a task needs, with less computation, fewer measurements or a more transparent explanation. A successor can restrict a predecessor's scope while leaving much of its practical value intact. The [first report](paper.md) develops this example and its sources.

The project takes seriously the possibility that scientific revision has no knowable endpoint. An agent may never be entitled to announce that it possesses the ultimate theory. This motivates the research; it is not a theorem that every theory must have a successor. The practical questions remain available: where does a model work, what error is tolerable, what does its use cost, what alternatives exist, and what evidence would change our reliance on it?

Mathematics raises a related question. Deriving a theorem within stated axioms differs from choosing a framework for a purpose. Choices such as accepting the axiom of choice need not be universally compulsory for every investigation. Expressive power, useful deductions and tractability can inform that choice while its mathematical assumptions remain explicit.

Usefulness does not settle metaphysical truth. It gives us something concrete to reason about while knowledge remains revisable.

## Why begin with value?

The foundational proposal makes task-relative value central to the semantic objects and inference rules themselves. A model can be adequate without being the best available option. It can cease to be preferred for one task while remaining worth retaining for another domain or budget.

Here, value is broader than probability, truth degree, money or a universally correct utility function. A scalar reward or loss is one possible representation. A function of uncertain quantities, an ordered structure or a set of attainable guarantees may preserve distinctions that one evaluated score loses. The appropriate amount of structure depends on the intended reasoning.

Unbounded values are part of the investigation. There is no general requirement that useful quantities lie in a fixed interval such as `[0,1]`. Bounded encodings are possible when their operations and precision preserve the intended conclusions; a squashing function alone does not establish that equivalence.

Three questions guide the work:

1. **Meaning:** what represents the task-relevant content of an expression or model use?
2. **Inference:** which conclusions about value or adequacy follow from which premises?
3. **Composition:** what information must survive joint use, sequential use, changes of task and revision?

Ordinary mathematical proofs remain available in an explicitly stated metatheory. The philosophical motivation leaves room for several possible calculi.

## Loss comparisons and revision

The [second report](paper_v2.md) compares scalar values, aligned profiles, continuation-based descriptions and achievable guarantees. Its working calculus uses finite signed piecewise-affine loss expressions over a shared uncertain source. A proof combines bounds on these expressions, and a receiver checks that the conclusion answers the current request under the current evidence.

This distinction matters when a price, model or observation changes. An old answer may remain useful, require a limited repair or lose its justification. The calculus separates the information retained about the source, the consumer's actual question and the evidence needed to accept the answer.

The main mathematical application studies procedures that share correlated failure outcomes and whose attempt prices can change. It characterizes exact retention requirements, constructs minimal repairs using new expected costs, and gives a compatible probability-law reconstruction with a sharp common error guarantee for a specified family of old summaries. These results distinguish preserving accurate numbers, selecting a good action and retaining a reusable model.

The work is a modest synthesis, formal adaptation and specialized application of established ideas in quantitative reasoning, optimization and information recovery. Ordinary methods remain strong comparators and can reproduce the same numerical services. The [report's contribution comparison](paper_v2.md#11-contribution-and-relation-to-established-work) identifies the precise technical additions and their scope.

## Applications and experiments

| Application | What it investigates |
|---|---|
| [Scientific model replacement](v2/derivations/06_case_studies.md) | Combining error, shared-source and resource premises to justify a cheaper procedure for a bounded task. |
| [Staged self-assessment](v2/derivations/06_case_studies.md#4-actual-bounded-native-procedures-and-later-reasoning) | Using checked outcomes of actual short proof procedures to choose and evaluate a later reasoning policy. |
| [Information retention under revision](v2/experiments/results.md) | Deciding when retained information supports a revised request, when new observations repair it and when refusal is appropriate. |
| [Ordinary-trained neural representations](v2/experiments/F15_ND01_results.md) | Testing whether task-relevant cost computations can be extracted and intervened on inside networks trained for ordinary prediction. |

The frozen retention challenge met its usefulness criterion in 68 of 160 episodes, with ordinary controls reproducing the equal-information results. In the neural probe, all five networks learned the prediction task and none met the complete intervention-support criterion. A follow-up diagnostic improved individual interventions and clarified the limits of the original extraction method.

**Ordinary prediction training gives a network no particular reason to organize each expected cost into one clean eight-neuron block.** Shared or distributed features can make that extraction difficult. The diagnostic motivates further work on joint representations; it does not establish technical superposition or a unique internal utility function. The [report](paper_v2.md#10-the-ordinary-trained-neural-intervention-probe) presents both the negative result and the informative improvements.

## The broader research program

A scientific task may combine models, translate between their outputs, route requests among them or invoke a fallback. Each step has its own error, cost and evidential requirements. Value Logic distinguishes empirical adequacy, permission to rely, comparative preference, current selection and archival retention, so that revision can change one without conflating the others. A fallback has consequences of its own.

The [first report](paper.md) makes licensed reliance relative to a use, context, epistemic state and requirement profile. It studies refinement, succession, local revision, composition and implementation preservation. Its [synthetic experiment](experiments/02_results.md) finds mixed advantages for structured numerical proposals and retains the ordinary comparisons that limit broader claims.

Learning and interpretability remain longer-term goals. A value-based description might help explain an agent's policy as well as predict its outputs. Neither a particular neural architecture nor the recovery of a uniquely true utility is assumed by the mathematical framework. The [original essays](posts/) and [exploratory conversations](llm_convos/) preserve the philosophical and practical origins of these questions.

## Explore the repository

| Material | Location |
|---|---|
| Research reports | [Loss comparisons and retention](paper_v2.md) · [Scoped reliance](paper.md) |
| Definitions and derivations | [Mathematical development](v2/derivations/) |
| Reproducibility | [Saved-result verification](paper_v2.md#133-verifying-saved-results) · [Experiment protocol](v2/experiments/protocol.md) |
| Evidence and comparisons | [Claim ledger](v2/claim_ledger.md) · [Literature studies](v2/literature/) |
| Research directions | [Opportunity register](v2/opportunities.md) |
| Contributor workflow | [Workspace guide](v2/README.md) · [Research protocol](v2/RESEARCH_PROTOCOL.md) · [Task plan](TODO_v2.md) |

The reports present the research; the workspace records preserve its derivations, experiments, decisions and attributed contributions.
