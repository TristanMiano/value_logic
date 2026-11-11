# Handoff: P4-R1-C001 (open, unfinished)

**Written by Claude (Fable 5.2), November 10, 2026,** for the next
contributor, expected to be GPT-6 Astra, at the author's direction. This is
an administrative note; it earns no research credit. Attribute your own work
to yourself and leave earlier attributions unchanged.

## State

- Cycle P4-R1-C001 (module W1) is **open**. The 240-minute floor is not met;
  the exact balance is at the end of [record.md](record.md) and is recomputed
  by `python v4/notebook/clock.py v4/notebook/P4-R1-C001/timing.jsonl --sum`.
- Results R1.1 to R1.7 are indexed in [v4/results](../../results/README.md).
  All were written and checked by one model and none is independently
  reviewed. A cold audit of the proofs would be worth more than a further
  result. The ones that carry most weight are Theorem 1 (R1.1), Theorem 5
  (R1.2) and Theorem 13 (R1.6).
- The author's November 10 statements (quoted in R1.6 and R1.7) fix the
  reading: **J is a forecast that what is rated will be seen again**, and
  reappearance is determined by the same agent, another agent, or the
  environment. Earlier files that speak of forecasting a performer's later
  result are the special case described in R1.6, section 3.

## What is established, in one paragraph

Scoring forecasts of reappearance selects conceptualisations, and the ones
it selects are fixed by the world: the minimal sufficient partition (R1.6),
which for performer-and-task worlds is the transfer partition (R1.1).
Without an outcome evaluator, approvals can serve as their own outcomes;
credited judges and delineation form a lattice of fixed points with
self-confirming members (R1.2). What judges' conventions cannot distort is
the transfer geometry; what they can is difficulty (R1.4). Recursive
weighting converges, and keeps all competent judges only when the domain is
connected (R1.5). Diverse judges' picks of "the best" identify an exemplar
set that is a fact about the objects (R1.3). When ratings also cause
recurrence, the environment's share is what selects among self-consistent
ratings (R1.7).

## Open obligations, most useful first

1. **Audit.** Re-derive Theorems 1, 5 and 13 independently; try to break
   them. Check the citations, which were made from memory after session 1.
2. **Couple R1.7 to R1.6:** a selection dynamic in which the kinds
   themselves are chosen, and fitness may depend on what agents do. This is
   the bridge to W7 and to C3.
3. **An explicit bound for Corollary 14** (R1.6) and a stability bound for
   general history length (R1.1, Theorem 2 is for one past performance).
4. **Coupled dynamics** of judge weights and delineation (R1.5 holds the
   delineation fixed).
5. **Unflagged random assignment** (R1.1, Proposition 5) and vindication
   with longer histories (R1.2).
6. **C5 proper:** self-trust and a Löb-type statement are untouched.

## Practical notes

- **Clock.** Record an observation at each change of activity. Run any
  computation that takes more than a few seconds under mode O; waiting is
  not research. Session 2 had to remove 27.9 minutes for this reason.
- **Scripts** are in this folder, import from one another, and run from
  this folder with Python 3 and NumPy only. Saved outputs sit beside them.
- **Checks before committing:** `python tools/check_repo_paths.py` and
  `python v3/checks/math_markdown.py --path FILE` for each changed document.
  Inline mathematics uses the backtick-dollar form.
- **The repository has about 58,000 tracked files.** On a slow or mounted
  filesystem `git status` can take minutes; commit by explicit paths.
- **The plan and policies** are [TODO_v4.md](../../../TODO_v4.md), the
  [charter](../../CHARTER.md), [AIM_BALANCE.md](../../AIM_BALANCE.md) and
  [RECURRENCE.md](../../RECURRENCE.md). Each session's log in record.md ends
  with an alignment note and a self-review; keep that form.
