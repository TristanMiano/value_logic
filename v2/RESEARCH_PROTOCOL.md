# Research Execution Protocol

Effective September 19, 2026. Applies to the calculus-first queue in
[../TODO_v2.md](../TODO_v2.md), including all repair iterations. Historical
half-hour task rules do not apply to this queue.

## 1. One work item, possibly several sessions

The unit of selection is a task or a gate attempt; the unit of timing is an
observed work segment. A task can span multiple prompts or sessions. At each
start read the current pointer, active blockers, dependencies, latest gate
record, and prior sessions for that task. Do not resume by numerical order when
a repair is active. A user-selected task overrides the pointer, but does not
waive its dependencies or gate requirements unless explicitly stated.

Before substantive work, create a record using
[templates/work_item.md](templates/work_item.md). State the exact question,
expected artifact, required evidence, and the task's minimum-duration obligation.
A gate attempt is its own work item; do not quietly perform the whole repair
cycle within the gate review. Small corrections that do not change semantics
can be made and recorded during an audit.

## 2. Separate three kinds of research

**D — derivation.** Write definitions, equations, proofs, worked examples,
failed proof attempts, and explicit countermodels in durable notes. Separate
assumptions from conclusions. Preserve enough intermediate steps that another
session can reconstruct the argument; final theorem statements alone are not
an adequate research record.

**L — literature.** Search external sources, read primary material, verify
hypotheses and exact statements, and distinguish imported results, adaptations,
and analogies. Record title, author, date, locator, access date, relevant
statement, and project impact. Search snippets and unverified recollections
are leads, not evidence. Retain unsuccessful searches when they materially
limit a novelty claim; do not equate failure to find a result with novelty.

**E — empirical or computational.** Implement models, run code, search finite
counterexamples, test invariants, benchmark a reasoner, and analyze results.
Keep code, configuration, seeds or exhaustive bounds, outputs, and failure
cases. Finite tests do not establish an unrestricted theorem. A finite
exhaustive verification can establish only its explicitly enumerated claim.

Use **O — overhead** for project administration, formatting, copying, routine
commit handling, and work that produces no new research evidence. O is reported
but does not satisfy D/L/E minimums. Scientific synthesis belongs to D only to
the extent it develops or checks an argument; paper formatting belongs to O.

The provisional research-time allocation is **60% D, 15% L, 25% E** across a
cycle, not necessarily within every task. At each gate compare planned and
actual shares. Adjust prospectively when evidence warrants it, preserving D as
the largest share by default. Do not manufacture low-value searches or runs to
hit a percentage; explain deviations and rebalance the next cycle.

### Code during derivation is allowed

Use a short computational probe during D work when it is plausibly a high-gain
way to find a counterexample, check an identity, or compare candidates. Before
switching, record the uncertainty it addresses, the expected benefit, and a
small initial budget. Record actual execution and implementation time as E and
the mathematical interpretation as D; never count the same minutes twice.
Stop an unproductive coding detour at its review budget or explicitly replan.
An hour of code does not discharge an hour-long derivation minimum.

## 3. Forecast effort before observing the result

For each task attempt record a central estimate and a plausible high estimate
for engaged working minutes, broken down into D/L/E/O. These are estimates, not
measurements or guaranteed completion times. Also forecast expected tool/run
waiting and any known wall-clock constraints. The roadmap's initial and
review-at allocations are starting priors; refine them for the actual task.
Keep the original forecast when revising a remaining-work forecast.

State one reliable gain and one uncertain gain available to this task or its
current cycle, their rough benefit and uncertainty, and how the allocated time
would reduce uncertainty. Do not invent precise probabilities to decorate a
forecast. A narrow implementation task may be entirely reliable-lane work if
the cycle already protects a concrete exploratory block.

## 4. Measure actual clocks, not perceived effort

Record UTC wall-clock start/end and a monotonic-clock reading for each segment
on the same runtime. A minimal portable reading is:

```python
from datetime import datetime, timezone
import time
print(datetime.now(timezone.utc).isoformat(), time.monotonic_ns())
```

Subtract matched monotonic readings to obtain elapsed segment time. Record the
runtime/session identity; do not subtract readings across restarts or hosts.
Use UTC intervals for audit and total elapsed reporting, not as a substitute
for missing observations of engaged work. Record a clock check at least every
15 minutes of active work, at mode/lane changes, before and after long tool
runs, and before ending the session. If a tool blocks a check, record that fact
and its timestamps afterward; do not invent an intermediate reading.

Separate engaged work, unattended tool waiting, interruption/idle time, and
unmeasured gaps. Pause the segment when work pauses. Awaited computation has
useful wall time but is not unattended derivation effort. Overlapping agents or
jobs get separate resource records; their simultaneous minutes are not added
to the principal agent's wall time. Token counts, word counts, and an agent's
feeling of effort are not clock measurements.

At a session end write actual D/L/E/O minutes, tool-wait and idle minutes,
observed wall elapsed, cumulative task totals, and forecast error. `Unmeasured`
is a valid record; it never satisfies a measured minimum. Historical work done
without a clock is not retroactively assigned a convenient duration.

F01 creates `v2/time_ledger.csv` with columns:

```text
task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status
```

Keep one row per closed segment; use D/L/E/O for mode and R/X for research lane
(leave lane empty for O). Avoid overlapping engaged intervals for one agent.
A missing duration is empty, not zero. Link each segment to its session record
and evidence artifact. Correct a mistaken row transparently with an amendment
record, preserving the original information in version history.

### Minimums are floors, not proof or busywork

The roadmap specifies protected minima for selected tasks, including at least
60 engaged D minutes for several foundational tasks and 90 for major proof
attempts. They may accumulate over multiple sessions of the same task. A
previously successful pass cannot be recycled to satisfy a newly required
independent-review minimum; repair-specific floors are set prospectively.

If the main result appears early, spend the remaining protected block on
alternative derivations, assumption weakening, hostile examples, or an
independent reconstruction. Do not sleep, repeat tool calls, inflate prose,
or leave a timer running to reach a floor. If useful work is genuinely
exhausted, propose a prospective change at the next gate; the current minimum
is not silently waived. If execution must stop early, save a partial record,
leave the task unchecked, and keep its continuation selected. Do not promise
unattended continuation.

Completion requires BOTH evidence and the recorded minimum. Time spent is
never itself evidence that a calculus is sound. At a task's review-at budget,
stop for explicit replanning: narrow the immediate attempt, create a repair
item, or forecast an additional block. Do not silently expand an unbounded
proof search or mark it successful because its budget expired.

## 5. Balance reliable and exploratory gains

This is an axis separate from D/L/E. **R (reliable)** includes checking a finite
lemma, removing an ambiguity, implementing a known construction, or preserving
a proven restricted fragment. **X (exploratory)** includes a stronger
representation theorem, a competing carrier, a possible impossibility result,
or a genuinely uncertain inference principle.

Start with **60% R / 40% X** of research time per cycle. Before the cycle,
identify concrete work in both lanes, not just a percentage. Report actual
shares at gates. Unless a documented repair emergency intervenes, preserve at
least 25% for each lane over two consecutive cycles. Deviations trigger a
prospective reallocation, not cosmetic relabeling. An X result becoming easy
does not erase the exploratory effort already spent. A failed X attempt can
be valuable if it narrows the search and leaves precise evidence.

Reserve roughly 25% of the initial traversal budget for recurrence. This is a
planning reserve, not a global phase limit or a requirement to exhaust it.
Review the benefit of continued work when the reserve is used. Preserve a
restricted sound result while investigating a harder candidate; do not make
all progress depend on the ambitious branch succeeding.

## 6. Evidence, claims, and gates

`v2/claim_ledger.md` records exact statements, assumptions, dependencies,
artifact versions, evidence type, status, counterexamples, and project impact.
Useful statuses include conjectured, proved-in-fragment, independently-checked,
empirically-supported, refuted, narrowed, and deferred. A generated proof is
not independently checked merely because it has been reread without a distinct
reconstruction attempt. Prefer a separate agent or reviewer when available;
otherwise use a fresh pass from definitions and label it self-review.

Every gate records PASS or BLOCKED, artifact revisions/hashes, criteria checked,
timing and lane totals, open objections, decisions, and the exact next pointer.
A failed attempt is still a completed review record, but its gate checkbox
remains unchecked. Passes can later become INVALIDATED; keep the old pass and
add an invalidation note rather than falsifying its history.

A gate does not pass with an unresolved contradiction or proof gap in a result
used downstream. A missing ambitious theorem may be scoped out only when a
stated alternative result meets that gate's criteria and the claim ledger and
specification are revised. An empirical null result is not automatically a
logical inconsistency: distinguish correctness, expressive usefulness, and
benchmark performance when assigning its consequences.

### Mandatory recurrence procedure

1. State the failed criterion and smallest known witness or exact gap.
2. Classify the source: requirements, representation, rule, proof, external
   premise, implementation, test design, or timing/evidence record.
3. Find the earliest affected dependency. Mark downstream claims/gates stale
   without deleting completed historical work.
4. Add a stable repair ID such as `R-B-1-01` to the active queue with a target,
   evidence requirement, fresh forecast, mode/lane allocation, and any minimum.
5. Move **Next task** to that repair. Work only on unaffected prerequisites or
   the repair until the blocked gate is rerun and passes.
6. Keep regression cases. Reopen dependent gates when their assumptions changed.

After two unsuccessful repair cycles on the same blocker, require a comparison
of at least two alternatives: change the rule, change the carrier, narrow the
fragment, or stop pursuing that candidate. Record a discriminating next test
and bounded exploration block; do not repeat the same attempt without new
information. There is no fixed lifetime count of phases or cycles. A suspended
candidate is not a successful calculus and a suspended phase is not completed.

## 7. Completion, commits, and validation

For a completed item, update its checkbox and result note, the claim ledger,
work log, time ledger, affected dependency map, and Next task pointer. Run the
commands in [README.md](README.md) and record actual outputs. In a checkout,
commit only that item with its ID after validation. A partial session may also
be committed with `partial` in the message, without marking the task done.
Do not automatically push unless the user authorized it.

Do not begin the next item merely because the present prompt has capacity.
At an explicit batch request, repeat the same checks at every task boundary.
The final report may claim only what passed the current, non-stale gates.
