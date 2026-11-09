# Value Logic Charter

**Status: APPROVED by Tristan Miano on November 8, 2026.** Drafted by
**Claude (Opus 5.5)** on November 7, 2026. Approval and the author's accompanying
recurrence-floor amendment are recorded in the
[dated decision](decisions/2026-11-08_approval.md) by **Codex (GPT-6)**.
Approval adopts the research charter; its theses remain research targets.

This charter sits above every phase plan, protocol, gate and audit. When a
procedure in this repository conflicts with the charter, the charter wins.
When the charter is wrong, the author amends it explicitly. Tasks and audits
never amend it by drifting away from it.

## Why this project exists

For a bounded agent, value comes before truth. "This works better than that"
is available long before "this is finally true." Newton was never simply
false. He was dominated for some purposes and not for others, and we expect
today's best theories to be superseded the same way, with no known endpoint.

The founding intuition is stronger than "use losses instead of truth values."
**When value is applied to itself, it is the engine that produces fact.**
A judge who wants to judge well has to recover the real distinctions between
tasks. Judging judges therefore forces contact with the structure of the
world. Truth is what explains the long-run success of increasingly useful
judgments and theories, and a value score always leaves room for something
better, including a better ontology.

The essays in [`posts/`](../posts/) and the conversations in
[`llm_convos/`](../llm_convos/) are where these ideas originate. Read them
before starting phase work.

## The theses

Each thesis states what the project is trying to show, and what would count
as success. A thesis can be refuted. It cannot be quietly abandoned.

| # | Thesis | What would count as success |
|---|---|---|
| C1 | **Judging judges forces the recovery of factual distinctions.** | An identifiability theorem: recursive judgment recovers latent task structure that first-order judgment cannot. |
| C2 | **Task delineation and judging judgments are two faces of one operation (T = J²).** | A typed fixed-point characterization in which the task partition and the judge weighting determine each other. |
| C3 | **Truth is the limit of value under successful use.** | A limit-truth construction with consistency conditions that recovers classical logic on a fragment. Newton-on-a-regime survives in the limit; unrestricted Newton does not. |
| C4 | **Supersession is local, and no theory need be final; value can rank ontologies.** | Licenses form a sheaf over domain space. "No final theory" is the absence of a global section, and theories with different carriers are compared through bridge maps. |
| C5 | **Self-trust is possible but constrained; values can be assigned to values without chaos.** | A Löb-type theorem for self-licensing, and convergence conditions for recursive value updates. |
| C6 | **Neural networks implement a value logic, and their geometry is an atlas.** | Measured alignment between ReLU linear regions and domain-of-validity boundaries; evidence on whether depth is forced. |
| C7 | **Policy and value are dual; a capable policy's value function is as complex as the policy.** | Identification results separating what behavior determines (decisions) from what it does not (a unique belief/value split), plus a compressibility question that bears on value fragility. |

## How the theses are to be read

The binding [aim-balance policy](AIM_BALANCE.md) governs how every task
interprets and reports on the theses. Its two central rules:

- **Hunt for the kernel of truth.** The theses are intuitions stated
  informally. Given a thesis "X implies Y," the task is to find and prove
  **X′ ⇒ Y′**, where X′ is as close to X and Y′ as close to Y as possible
  while the implication is true and provable: the precise statement that
  seems to generate the intuition. Faithfulness and defensibility are
  optimized together. Proving "X does not always imply Y," or retreating to
  whatever reading is easiest to defend, does not discharge a thesis.
  Refuting the most ambitious reading does not either; it shows which
  condition is missing or which conclusion is too strong, and that is the
  next step toward the most faithful statement that holds. Finding the
  kernel is itself valuable work and is credited as a contribution.
- **Prefer informative statements.** "X does not imply Y" and "it is not
  always the case that X" are the start of an answer, not the end. Ask what
  does imply Y, when X does hold, and which conditions separate the cases.
  Headlines are positive conditional claims followed by their limits.

The search for limits stays real. Constructions and obstructions get equal
effort and equal standards, and neither direction is presumed in advance.

## What counts as a contribution

This is foundational research. A result counts when it does at least one of
these:

1. **Characterizes:** makes a thesis precise and proves it under stated
   conditions.
2. **Unifies:** shows that two founding ideas are the same structure.
3. **Refutes informatively:** shows that a thesis fails *and* states the
   repaired thesis that the failure points to.
4. **Interprets:** finds the kernel of an informal thesis, a precise reading
   that is both faithful to it and credibly provable, making it ready to
   prove.

Obstructions, counterexamples and characterized limits are legitimate
contributions. Constructions, sufficient conditions, successful repairs and
characterized regions where a thesis holds are equally legitimate, and
agents must seek them with equal seriousness.

"Ordinary methods reproduce it" is information to report, not a verdict.
Classical logic can simulate intuitionistic proofs by translation, and that
does not make intuitionistic logic empty. A logic contributes through what it
organizes and makes expressible. Exclusive computational capability is not
required, and full-cost superiority is not the bar.

Results that touch none of the theses can be good mathematics. They belong in
a toolkit appendix, not at the head of a phase.

## Drift: the main risk to this project

**Read this section before starting any phase, task, audit or report.**

Phases one through three became steadily more rigorous and steadily further
from the theses above. The subject moved from a logic of fallible theories,
to a calculus of loss bounds, to a parametric linear-programming range
algorithm. T = J² was demoted as "untyped" and never typed. Excellence
centroids were excluded. Reflection stayed acyclic despite an explicit
statement that this was temporary. Ontology change shrank to adding entries
to a fixed library. No single step was unreasonable. Each one chose the safest
next problem, the one least exposed to critique, and audits, including Claude's, rewarded claims that
survive critique, which means narrower claims. Nothing protected the
ambition.

Drift is the default outcome of careful work under critique. It has to be
actively resisted.

### Warning signs

Stop and re-align when any of these appear:

- The phase's headline result could be published without mentioning value,
  judgment, supersession or self-application.
- A thesis is weakened, renamed, deferred or moved to "motivation only"
  without a proposed repaired version.
- A thesis is "answered" by refuting its most sweeping reading, or by
  proving a reading so weakened that little of the thesis remains, with no
  attempt at the most faithful provable one.
- Headlines and dispositions are mostly negations: "does not imply," "not
  always," "not established," "ordinary methods tie."
- The work is chosen mainly because a measurable computational delta against
  conventional methods is available.
- Bookkeeping (clocks, gates, recurrence ledgers, trace archives) is growing
  faster than the stated mathematics.
- Reports describe what is *not* established more prominently than what is.
- Several consecutive tasks deepen one narrow construction while no thesis
  moves.
- The author's essays and the current paper no longer sound like the same
  project.

Drift has a reciprocal form, and it is also a warning sign:

- A success on a restricted class is announced as the thesis proved in
  general, or a construction's assumptions disappear from its summary.
- An inconvenient but independently motivated obstruction is set aside
  rather than characterized.

### The re-alignment rule

1. **Every task names the thesis it advances,** and says in one sentence how.
   A task that advances none must be explicitly authorized by the author as
   toolkit work.
2. **Every demotion carries a repair.** An audit or task that weakens a
   thesis must propose a typed or otherwise repaired version, or argue that
   none exists. "Untyped," "slogan" or "excluded" are not final dispositions.
3. **Every checkpoint begins with an alignment review** before any
   correctness review. For each thesis, record whether it moved forward,
   stood still or moved back since the last checkpoint, and why. If two
   consecutive checkpoints show no movement on C1–C5, the next task must be
   chosen to move one of them.
4. **Every audit asks two questions:** "Is it correct?" and "Did it preserve
   or recover a thesis?" An audit that answers only the first is incomplete.
5. **Every task ends with the end-of-task review** in
   [AIM_BALANCE.md §6](AIM_BALANCE.md#6-end-of-task-review), recorded in the
   task record or pull request.
6. **When in doubt, re-read the founding essays** and ask whether their
   author would recognize the current work as theirs. If the answer is
   unclear, ask the author.

Narrowing a claim to make it true is often right. Narrowing the *project*
silently is not. The reciprocal also holds: widening a claim beyond its proof
is not right either, and a successful construction keeps its real
assumptions. When a thesis really does fail, say so prominently, keep what
was learned, and state the strongest version that survives. When a thesis
succeeds on a restricted class, say so prominently too, and pursue its
extension.

## Working norms

- **Exploration and record are separate.** Fast, informal exploration goes in
  a notebook with no hedging requirements. Stated, proved and checked results
  go in the record.
- **Ideas first, caveats second.** Every result gets a short plain-language
  statement of what it shows about a thesis before its scope conditions.
- **Light repository.** Run traces and bulk outputs do not belong in git
  history. Use releases or Git LFS, and keep individual commits small.
- **Attribution stays honest.** Record which model or person produced each
  result. Model-generated analysis is not third-party endorsement.
- **Milestones assess progress; recurrence floors protect sustained work.**
  Under the author's November 8 amendment, each selected research recurrence
  has a four-hour engaged-research floor unless explicitly overridden for that
  recurrence. Keep a small observed timing record, with administration and
  waiting excluded. Time alone does not discharge a thesis. The
  [recurrence procedure](RECURRENCE.md) implements this without importing the
  phase-three archive or its accumulated time.

## Amending this charter

Only the author amends the charter, by an explicit dated edit with a short
reason. Phase plans, protocols and audits can propose amendments; they cannot
make them.
