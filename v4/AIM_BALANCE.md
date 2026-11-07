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

## 1. Two failure patterns this document corrects

**Refuting the most ambitious reading and stopping.** An agent receives an
intuitive thesis, chooses its most sweeping reading ("judgment *always*
recovers fact," "T *equals* J² as functions"), finds a counterexample or a
typing gap, and reports the task finished. That reading was the easiest one
to refute, not the one the author most likely meant. The refutation is often
correct and almost always uninformative about the thesis.

**Answering with negations.** "It is not always the case that X." "X does not
imply Y." "Ordinary methods reproduce it." "Not established." Each is true,
adds little information, and closes a question that was not actually
answered. A long list of such statements can look like rigorous progress
while the project's positive content shrinks.

The project's history contains both patterns. T = J² was demoted as an
"untyped slogan" and not typed. The recursive-judgment countermodel
J_m = J₀ showed when recursion adds *no* information, and the question of when
it *does* was not asked. The neural probe tested a localist reading (clean
eight-neuron cost blocks) that the policy/value intuition does not predict;
the report itself noted that ordinary training gives no reason for such
blocks, but the test of the distributed reading was deferred. Phase contribution
reviews repeatedly closed with "ordinary methods tie." These are not
mistakes of mathematics; they are mistakes of aim.

## 2. Find the most defensible interpretation, then defend it

When a task starts from an author's thesis, intuition, essay passage or
informal claim, the first job is interpretive and it is real work.

1. **Collect candidate readings.** Write down several precise readings of the
   statement, varying the quantifiers ("always," "under conditions C,"
   "generically," "in the limit"), the objects (functions, fixed points,
   partitions, distributions), and the sense of key relations ("equals,"
   "is determined by," "recovers," "is a limit of").
2. **Rank by defensibility, not ambition.** The most defensible reading is
   the one that best combines two things: it keeps the intuition's core
   content (what would make the author say "yes, that's what I meant"), and
   it has the best prospect of being true and provable. A trivially true
   reading fails the first test; the most sweeping reading usually fails the
   second.
3. **Defend it rigorously.** Try to prove it. State the conditions it needs.
   Build examples where it holds. This is where most of the effort goes.
4. **When it fails, repair before reporting.** Find the nearest reading that
   survives the obstacle, and say what the obstacle teaches. A counterexample
   to one reading is evidence about where the true statement lives, not an
   answer to the thesis.
5. **Record the interpretive work.** The candidate readings, the chosen one,
   and the reasons for choosing it go in the task record. Finding the right
   reading of an intuition is a contribution in its own right and is credited
   as such.

A reading may be abandoned only after the most defensible reading has been
given a serious attempt and repairs have been tried. Then say so prominently,
state what survives, and name the obligation that remains.

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
2. the most defensible reading being pursued, and why (§2);
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

1. **Interpretation.** Which readings of the thesis were considered? Was the
   most defensible one pursued, or the easiest to refute? Is the
   interpretive work recorded?
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
