# Statistical sources and authoritative receipts

Codex (GPT-6), October 11, 2026. DEVELOPMENT, S08/S08T; no confirmation claim.

The [problem contract](../../foundations/01_problem_contract.md) §4–5 and
[observation contract](../../foundations/01_observation_contract.md) §4 already
distinguish interpreted mathematical truth, proof production, forecasts and
statistical intervals. S08 is a design-based aggregate guarantee over the
verifier's random selection of a fixed population. It is not a posterior on
one mathematical sentence, nor a hard proof of an aggregate proposition.

## An executable conflict policy

Retain a hard receipt map H and a separately typed collection C of statistical
count constraints. Each receipt names source, coordinate, value and checker
bridge. Reject stale identity and unsupported messages before update. Two
contradictory hard receipts indicate a bridge/source error; do not resolve that
by silently selecting one. The following statement assumes hard receipts are
sound and mutually consistent.

On receipt, first fix the truth coordinate in H. Test feasibility of H ∩ C
using the source's actual implemented algorithm. If empty, record a detected
statistical-source conflict, retire all statistical constraints for that source,
and fall back to H alone. Retiring everything is deliberately simple; finding
a smallest conflicting subfamily is a different paid computation. Keep old
reports immutable, with their creation-time information and risk status.

Suppose with probability at least 1−α, the fixed true vector y lies in C at
every acquisition time. On that event, H ∩ C is nonempty after every sound
receipt, every optimization over it bounds y, and all subsequent adaptively
chosen value queries are covered by that same event. No query-wise union bound
is needed. On its complement, a conflict need not appear immediately, so old
statistical warrants can be wrong. Once detected, the H-only fallback is sound.
This policy never licenses a claim that undetected statistical errors are
impossible. Fresh statistical reacquisition needs its own conditional sampling
contract and risk allocation; merely clearing the conflict is not a reset of α.

This realizes U04's hard-evidence priority at the specified finite scope. If
every fixed coordinate eventually receives a sound positive or negative
receipt, all pointwise bounds become exact, even on a failed confidence event.
That conditional observation is not an anticipatory-learning theorem. In the
positive-proof-only service, false coordinates may never resolve, so that U05
premise is absent. Sound negative certificates require an explicit checker;
the native solver's unsupported False is still not one.

## Closest statistical-verification comparison

- Younes and Simmons, [Statistical Probabilistic Model Checking with a Focus
  on Time-Bounded Properties](https://www.cs.cmu.edu/~lorens/papers/tmp/prob_model_checking.pdf),
  inspected §§1–2.2, especially the acceptance-sampling and sequential-test
  equations. Statistical verification and reduced expected sample count are
  established ideas. The paper distinguishes probabilistic error from exact
  correctness and uses an indifference region for its two-sided service. S08
  cannot claim sequential testing itself. Its current output is a one-sided
  finite-population warrant or abstention with arbitrary computation censoring;
  it has no general termination or power guarantee.
- Younes, [Error Control for Probabilistic Model Checking](https://www.cs.cmu.edu/~lorens/papers/tmp/error_control.pdf),
  inspected §§2.3–4.1. False positives, false negatives, undecided outputs and
  termination are separate requirements. This directly constrains S08's
  interpretation: validity of a lower warrant says nothing by itself about
  how often a useful answer is returned. Our bounded-proof examples display
  that gap. No nested temporal-logic theorem is imported here.
- Daca, Henzinger, Křetínský and Petrov,
  [Faster Statistical Model Checking for Unbounded Temporal Properties](https://arxiv.org/abs/1504.05739v2),
  abstract inspected only. Their Markov-chain simulation termination approach
  uses a minimum-transition-probability assumption. It is a relevant lead for
  computation stopping, not an available justification for censoring arbitrary
  deterministic SAT calls. No theorem from it is imported.

The working delta remains a source/version-bound integration of checked
receipts, partial-label confidence sources and cheap revision/value queries.
It still needs a materially useful capability or complete-cost benefit over
specified strong conventional constructions. Readiness remains unassessed.
