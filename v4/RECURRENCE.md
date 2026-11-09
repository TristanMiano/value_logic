# Phase-four recurrence procedure

November 8, 2026. **Codex (GPT-6)**, implementing the
[author's direction](decisions/2026-11-08_approval.md).
Governed by the [charter](CHARTER.md) and [aim-balance policy](AIM_BALANCE.md).
This is a small execution contract for [TODO_v4.md](../TODO_v4.md), not a new
scientific contribution or a reopening of phase three.

## Modules, cycles and sessions

A **module** is a continuing subject-level question, P4-R1 through P4-R8.
A **cycle** is a selected recurrence within it, for example P4-R1-C001.
A **session** is a continuous stretch of work; several sessions or context
windows may contribute to one unfinished cycle. Stable IDs distinguish these.

**Every selected research cycle has a floor of 240 engaged research minutes.**
This includes the integration module. An explicit author override applies only
to the recurrence it names. A new cycle earns no credit from an earlier cycle's
surplus. All current modules are unstarted; listing a module does not start its
clock or commit to executing every module immediately.

Preparation, approval records, routine reviews of the plan, report formatting
and publication have no artificial research floor. Substantive reconstruction,
proof or experiment work inside a selected cycle does count. Describe work by
what was actually done; do not turn an administrative task into research by
renaming it. This plan-revision task receives zero recurrence credit.

## Start or resume

Use the actual checkout and preserve unrelated work. Read the charter's Drift
section, the aim-balance policy, the selected module and any unfinished record.
Before substantive work, make one compact record in `notebook/` containing:

- Module/cycle ID, actual contributor/model, authorization and running example.
- Thesis, kernel hypothesis and candidate readings; why the chosen reading
  preserves the intuition and has a credible path to proof.
- Declared inputs, quantifiers and comparison, with constructive attempts and
  limiting cases/repair attempts given equal seriousness.
- The 240-minute floor or explicit override, a rough research/overhead forecast,
  and a few useful directions for the cycle. No result is promised in advance.
- Previous completed time, remaining floor, open arguments and next move if
  resuming. Set the single active-cycle pointer in TODO_v4.md.

The work plan inside a cycle is revisable. Generate several faithful readings
and mechanisms, test them cheaply, and develop promising ones. A failed
construction prompts a repair or another faithful reading; a successful one
prompts consequential extensions and boundary checks. Avoid spending an entire
cycle repeatedly auditing a weak example, or treating one successful toy as the
whole thesis.

## Minimal observed timing

Use one small append-only observation file per cycle, alongside its notebook
record. At active boundaries and at least every fifteen minutes record UTC,
`time.monotonic_ns()`, runtime identity and mode: **D** (definitions/proofs),
**L** (literature), **E** (implementation/experiment analysis), or **O**
(administration). Pair boundaries only within the same live runtime. Research
credit is observed active D+L+E after exclusions; O, waiting, idle, recovery and
unobserved intervals are excluded. Keep integer nanoseconds and compute minutes
from them; rounded displays never determine whether the floor is met.

Pause before unattended waits or handoffs. A crashed clock's unclosed or
unobserved interval earns zero until supported by actual same-runtime boundary
observations; never infer it from elapsed wall time, output length or effort
claimed in prose. Resume unfinished cycles with the verified balance. A context
refresh neither closes the module nor starts another four-hour commitment.
Concurrent work, if separately authorized, must not double-count the principal's
time. This procedure does not authorize delegation.

Keep evidence proportionate: the compact cycle record, raw timing observations,
result/proof/source links and small reproducible checks suffice. Do not copy
repositories or large run traces into each cycle. Preserve raw failed attempts
where scientifically material, but place bulk outputs outside git history as
the charter requires.

## Assess, recur and hand off

A floor is a minimum commitment, not proof of completion or a command to stop.
Continue useful work to a substantive boundary. If interrupted below the floor,
leave the same cycle unfinished with its remaining obligation. A pause does not
reduce the minimum; an author amendment can.

At a cycle boundary, start with charter alignment, then assess correctness and
the explicit contribution. State the strongest supported faithful reading,
the conditions separating successful and failing cases, and what remains open.
Complete the aim-balance end-of-task self-review and closing de-biasing paragraph.
Use one of these module dispositions:

- **Continue:** important questions remain and the next constructive or limiting
  investigation is identified. Select another four-hour cycle when continued
  work is authorized; finishing one cycle never checks off the whole module.
- **Advance at stated scope; available to recur:** a supported result or
  informative repaired thesis is sufficient for the milestone. Preserve the
  broader gap and return when new evidence or a dependent module warrants it.
- **Redirect with repair:** current readings lack a promising route. Record
  attempts in both directions, the most faithful surviving reading and a
  concrete alternative. Seek the author's direction for a substantial change
  of aim; do not silently retire a thesis.

An authorization for one recurrence does not automatically authorize another
four-hour block. Within an author-authorized continuing program, repeat the
relevant module while useful unresolved questions remain. Neither exhausting
one candidate nor reaching a milestone creates a claim that all its questions
are solved. Conversely, general philosophical questions need not be settled to
advance a well-supported restricted contribution.

If two checkpoints show no movement on C1--C5, follow the charter's re-alignment
rule: select work that moves one of those theses. Consider a different faithful
construction as explicitly as stronger scrutiny of the current one.

## Results and completion

Record each completed cycle in a short table in TODO_v4.md: ID, scope, research
time, thesis movement, outcome, next unresolved question and record link. Do
not accumulate several competing progress tables. Use `results/` for statements
with explicit evidence levels, assumptions, proofs/checks, closest established
work and the gap to the thesis. Notes may remain exploratory without becoming
claimed results.

Milestones organize the modules; they do not replace their floors. Administrative
report assembly has no separate floor, while genuinely new integration arguments
belong to P4-R8. The final report and alignment review give a reasoned completion
recommendation; the author retains the final phase-completion decision.
