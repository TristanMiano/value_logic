# Aim preservation and balanced research

**Binding companion to the [charter](CHARTER.md).** Read and follow this
document when planning, conducting, reviewing, auditing, summarizing or
handing off any task: research, literature search, code, documentation,
prompts and publication. Explicit author instructions override it. It
supplements mathematical rigor; it never changes the truth or support status
of a result.

Drafted by **Claude (Opus 5.5)** on November 7, 2026, at Tristan Miano's
request. It adapts the aim-balance policy of the author's
[corrigibility-games](https://github.com/TristanMiano/corrigibility-games/blob/main/research/AIM_BALANCE.md)
project to Value Logic and adds a rule about interpretation.

## 1. Three failure patterns this document corrects

**Refuting the most ambitious reading and stopping.** An agent receives an
intuitive thesis, chooses its most sweeping reading ("judgment *always*
recovers fact," "T *equals* J² as functions"), finds a counterexample or a
typing gap, and reports the task finished. That reading was the easiest one
to refute, not the one the author most likely meant. The refutation is often
correct and almost always uninformative about the thesis.

**Retreating to the safest statement.** Asked to prove "X implies Y," an agent
notices that a literal reading may be false and instead proves "X does not
always imply Y," or a reading so weakened that it is trivially true. Each is
easy to defend, and each gives up nearly all of the contribution the thesis
was reaching for. Defensibility alone is not the goal; maximizing it picks
the emptiest statement available.

**Answering with negations.** "It is not always the case that X." "X does not
imply Y." "Ordinary methods reproduce it." "Not established." Each is true,
adds little information, and closes a question that was not actually
answered. A long list of such statements can look like rigorous progress
while the project's positive content shrinks.

The project's history contains these patterns. T = J² was demoted as an
"untyped slogan" and not typed. The recursive-judgment countermodel
J_m = J₀ showed when recursion adds *no* information. The
[phase-one proper-score bridge](../paper.md#f4-proper-score-information-and-the-task-quotient)
also gave a positive conditional connection between predictive judgment and
task information, and characterized incremental information beyond earlier
reports. Full latent-task recovery and a coupled T/J² construction remained
open. Preserve that positive starting point while pursuing the stronger theses.
The neural probe tested a localist reading (clean
eight-neuron cost blocks) that the policy/value intuition does not predict;
the report itself noted that ordinary training gives no reason for such
blocks, but the test of the distributed reading was deferred. Phase contribution
reviews repeatedly closed with "ordinary methods tie." These are not
mistakes of mathematics; they are mistakes of aim.

## 2. Hunt for the kernel of truth: faithful and defensible together

When a task starts from an author's thesis, intuition, essay passage or
informal claim, the first job is interpretive, and it is real work. The goal
is the **kernel of truth**: the precise statement that seems to be generating
the original intuition, and that explains why the intuition looked right.

### The target

Suppose the thesis is "X implies Y," and a literal reading may be false. The
task is **not** to prove "X does not always imply Y," and **not** to pick
whatever reading is easiest to defend. It is to find and prove

> **X′ ⇒ Y′,** where X′ and Y′ are interpretations of X and Y, X′ is as close
> to X as possible, and Y′ is as close to Y as possible, subject to X′ ⇒ Y′
> being true and provable.

Two quantities are optimized **jointly**:

- **Faithfulness:** how much of the thesis's content X′ ⇒ Y′ keeps. Would the
  author say "yes, that is what I meant, made precise"? Does it keep the
  thesis's direction, its central objects and its surprising part?
- **Defensibility:** how good the prospects are that X′ ⇒ Y′ is true and can
  actually be proved.

Neither is maximized at the expense of the other. The most sweeping reading
maximizes faithfulness and usually fails. The trivially true reading
maximizes defensibility and is worthless. Ambition is not disfavored: among
readings that are provable, prefer the most faithful, and push toward the
most faithful reading that can be proved, rather than settling for the first
one that can.

The same shape applies to theses that are not implications. For "A equals
B," seek the closest relation A′ ~ B′ that holds (equality on a quotient, at
a fixed point, in a limit). For "there exists a Z with property P," seek the
closest Z′ and P′. For "truth is the limit of value," seek the closest notion
of limit and of truth under which it holds.

### Moves that weaken the thesis, and their costs

There are two basic ways to make X ⇒ Y provable, and each spends
faithfulness:

- **Strengthen the hypothesis:** add conditions, X′ = X ∧ C.
- **Weaken the conclusion:** Y′ = a bounded, approximate, eventual,
  generic or probabilistic version of Y.

Movement in the other direction is welcome. If a reading with a weaker
hypothesis or a stronger conclusion than the thesis can be proved, that is a
better outcome, not drift, provided it is still a reading of the thesis.

Spend as little as possible. Name every condition C and every weakening of Y
explicitly, say why it was needed, and check whether it can be relaxed. A
condition that the founding intuition itself suggests (for example, temporal
recurrence in "yes means I expect it to reappear") costs less than an
arbitrary one.

**Excluded as endpoints:** replacing the thesis with its negation or with a
non-implication ("X does not always imply Y"); vacuous readings (X′ never
holds, or Y′ always holds); and readings that keep the words but none of the
content. These may appear as lemmas or as boundary markers along the way.
They do not discharge the task.

### Procedure

1. **Locate the kernel.** Ask what mechanism would make the intuition true
   when it is true. The kernel is usually a mechanism, not a slogan: for
   T = J², something like "the task partition and the judge weighting are
   determined by each other at a fixed point."
2. **Collect candidate readings.** Write several precise versions of X′ ⇒ Y′,
   varying the quantifiers ("always," "under C," "generically," "in the
   limit"), the objects (functions, fixed points, partitions,
   distributions), and the sense of key relations ("equals," "is determined
   by," "recovers," "is a limit of").
3. **Place them on the faithfulness–defensibility frontier.** Discard
   readings beaten on both counts. Begin with the most faithful reading that
   has a credible path to proof.
4. **Defend it rigorously.** Try to prove it. Build examples where it holds.
   This is where most of the effort goes.
5. **When it fails, use the failure to move along the frontier, not off
   it.** A counterexample shows which condition was missing or which part of
   Y was too strong. Turn that into the smallest added C or the smallest
   weakening of Y′, and try again. Also check whether the counterexample
   attacks the kernel itself or only an inessential feature of the reading.
6. **Report the most faithful statement proved**, together with the gap
   between it and the thesis: which conditions were added, which parts of Y
   were weakened, and which stronger readings remain open or were refuted.
   The gap is a named obligation, not a reason to stop.
7. **Record the interpretive work.** The candidate readings, the kernel
   hypothesis, the frontier, and the reasons for each move go in the task
   record. Finding the kernel of an intuition is a contribution in its own
   right and is credited as such.

A thesis may be judged false only after its kernel has been sought, the most
faithful credible readings have had a serious attempt, and repairs have been
tried. Then say so prominently, state the most faithful statement that does
hold, and name the obligation that remains.

This is not a license to defend anything. The same rigor applies: a proof is
a proof, a counterexample is a counterexample, and a reading that keeps
nothing of the intuition does not count as defending it.

## 3. Prefer informative statements

A statement adds information when it narrows down what is the case. Replace
negations and non-implications with statements of these kinds:

| Instead of | Look for |
|---|---|
| X does not imply Y. | What *does* imply Y (sufficient conditions)? What does X imply? Under which added conditions does X imply Y? |
| It is not always the case that X. | When is X the case? Characterize the region, class or regime where X holds, and where it fails. |
| No procedure can certify P in general. | Which procedures certify P under which conditions? What is the weakest assumption that makes certification possible? |
| Ordinary methods reproduce the result. | What the result organizes, unifies or makes expressible, and what the equivalence itself shows. |
| Not established. | What *is* established, at which level, and what specific evidence would establish the rest. |

A counterexample is the start of a characterization, not its end. After one
is found, ask what distinguishes it from the cases where the claim holds, and
try to turn that distinction into a theorem.

Headlines, summaries and checkpoint dispositions lead with positive
conditional claims ("Under C, recursive judgment recovers the task
partition") and then state limits. A headline that says only what fails is
incomplete.

## 4. Pair both directions

### The paired formulations

Whenever a goal, instruction or interpretation uses one of these, include
its converse with equal prominence in the same paragraph or paired list:

> It is not always the case that X; sometimes it is Y.
>
> It is not always the case that Y; sometimes it is X.

For this project the central pair is:

- **X:** value judgments carry no factual information; truth must be
  established first and value assigned afterwards.
- **Y:** value, recursively applied and checked against recurrence, recovers
  factual structure, and truth can be reconstructed as its limit.

The charter's theses are mainly about Y. Showing that some judgment fails to
recover fact does not answer whether other judgment does. Showing that one
recursive scheme recovers fact does not show that all do. Both are distinct
achievements and both can be true. X and Y need not exhaust the
possibilities; do not infer one by negating the other unless the model
justifies the dichotomy.

### Local pairing rule

Any instruction to seek counterexamples, obstructions or failure modes is
paired, in the same place, with an equally explicit instruction to seek
constructions, sufficient conditions and successful repairs. Any warning
against overclaiming is paired with a warning against underclaiming,
including treating a local failure as general failure. This applies to
titles, lists, contribution criteria, stopping rules, templates, prompts,
audits and handoffs. A balanced sentence elsewhere in the repository does not
repair an unbalanced active instruction.

This is symmetry of instructions, search effort, evidential standards and
prominence. It is not a quota of conclusions. Do not fabricate a positive
theorem, hide a valid negative result, or force equal counts. Exact theorem
statements keep their exact content; their interpretation must say what they
establish and what constructive or limiting question remains.

### Equal standards

- Apply naturalness, robustness, literature and proof standards to both
  sides. Do not call a favorable construction contrived while treating an
  equally specialized countermodel as representative.
- Do not dismiss an independently motivated obstruction because it is
  inconvenient.
- Counting successes does not establish generality, and neither does
  counting failures.
- State every result at the level actually supported: existence,
  conditional theorem, robustness, generic behavior, or prevalence.

## 5. Keep constructive research operational

Begin each task by restating:

1. the charter thesis it serves, in the author's terms;
2. the kernel hypothesis and the reading X′ ⇒ Y′ being pursued, with why it
   sits where it does on the faithfulness–defensibility frontier (§2);
3. the quantifier and model class;
4. which positive and which limiting possibilities the task can distinguish.

When a construction fails, decide whether the obstacle belongs to this
construction or persists over an explicitly enlarged class. Seriously try
repairs: richer representations, temporal structure, different typing,
weaker or stratified conclusions. When a construction works, test its
consequential perturbations instead of assuming it generalizes. These are
two halves of one investigation.

Literature searches, delegated subtasks, generated prompts and handoffs
inherit these obligations. Search for enabling theorems and successful
mechanisms as explicitly as for impossibility results.

## 6. End-of-task review

**After every task, review the work for aim inversion and missing
counterpart instructions before reporting it complete.** This includes short
edits, literature tasks, audits, reports and revisions of this document.

Read the complete changed material and the active instructions around it.
Check:

1. **Interpretation.** Which readings of the thesis were considered, and what
   kernel was hypothesized? Was the most faithful credible reading pursued,
   or one chosen because it was easiest to refute or easiest to prove? Were
   added conditions and weakenings minimal and named? Is the interpretive
   work recorded?
2. **Quantifiers and target.** Did a conditional or possibility question
   become a demand for a universal claim, or a search only for failure? Did a
   local result become a broad pessimistic or optimistic claim?
3. **Informativeness.** Is each headline and disposition a positive
   conditional statement, with limits after it? Where a non-implication or
   counterexample was found, was the characterizing follow-up attempted?
4. **Pairing.** For each directional caution or search directive, where is
   its equally explicit counterpart?
5. **Actual research choices.** What construction was developed, tested,
   repaired or carried forward? What limiting condition was tested? Did
   omitted structure (time, typing, carrier changes) predetermine the answer?
6. **Comparable standards.** Were naturalness, controls and proof standards
   applied evenly? Was equivalence to conventional methods wrongly treated as
   evidence against a thesis?
7. **Charter alignment.** Which thesis moved, and in which direction? Has
   successive refinement narrowed the active question away from the theses?
8. **Next action.** Does the recommended next step advance a thesis, with
   both directions explicit where used? Correct wording, omissions and
   interpretations now; carry unfinished mathematical repairs forward as
   named obligations rather than claiming them.

Record the review in the task record, report or pull-request description. A
bare "no bias found" is not enough: include the aim and thesis, the paths
reviewed, constructive and limiting work, omissions or inversions found,
corrections made, and remaining obligations.

Every findings report ends with about one paragraph acknowledging this
review: what bias or risk of bias appeared during the work, and what was done
about it. Distinguish identified bias from possible risk, and do not claim
the review guarantees impartiality. Unless an independent review actually
occurred, describe it as a self-review.

A task with an unperformed review or an uncorrected framing defect is not
complete. An honestly scoped open mathematical question is not a framing
defect.
