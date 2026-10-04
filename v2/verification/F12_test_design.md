# F12 development design

Contributor: **Codex (GPT-6)**. October 3 local / October 4 UTC, 2026.
Prospective design recorded before F12 comparison collection. This is a
development study; no held-out performance or novelty claim is implied.

## Differential population

Scientific sources use the F11 contract and unchanged native kernel. Enumerate
the Cartesian product of joint bounds {0,1/16,1/4,1,2,absent} twice and coordinate
caps {0,1/64,1/4,1,absent} twice: **900 sources × three actions**. Also test
**257 rational sources**, seed **20261003**, denominator 997, the generator in
`workloads.py`; **nine** threshold/perturbation sources (±1/1024); and **four**
off-grid witnesses where a grid-selected formula subset previously failed.
Total **1,170 sources / 3,510 queries**. These are declared finite families,
not exhaustive coverage of rational or real inputs. Absent evidence differs
from an explicit zero or redundant upper bound.

Each query compares the native bound, independent geometric/direct polynomial
execution, and the ordinary analytic formula. It verifies the reference
attainer against the complete source and direct losses, receives the proof at
the exact threshold, rejects a threshold tighter by 1/1,000,003, and round-trips
the receipt at its actual bound. The reference imports no native AST, solver,
formula or receipt decoder. The reference and implementation share a human
specification/input model; this is not independent authorship.

For host-failure containment, execution units are fixed contiguous shards of
100 sources (final shard may be shorter), with at most three attempts each.
A shard counts only after an entire attempt exits zero with a valid matching
report; partial attempts never combine into a pass. Preserve commands, all
logs, return codes, timestamps, source hashes and incomplete coverage. Emit
the current source index before each check to localize failures. These retries
address known host instability, not indefinite attempts to obtain a favorable
result. Deterministic disagreements require diagnosis and a recorded correction.

## Revisions and hostile controls

Twenty-four declared old/new pairs × three actions cover unchanged-versioned
evidence, strengthening, relaxation, withdrawal of a coordinate bound, total
withdrawal, and alternative joint support. Check source-set monotonicity where
specified, reject stale receipts, reconstruct with current rows, compare exact
fresh/reference answers, and preserve gaps and genuine refusals. Parameterize
the F11 missed-threshold witness. Test changed consumer, scope, units and
composition separately. F09's common positive-scale proof transformation and
affine-offset denotation corrections receive current-producer regressions;
invalid naive scaling/recoding must not gain acceptance.

## Sequence cost contract

Every strategy gets the same complete current source and query. The request
is a zero-budget comparison against F, with **a checked current bound receipt**
and certification only when it meets that request. An insufficient bound is
unavailable, not a negative certificate. Ground-truth/reference assessment runs
outside timed answer production and is unavailable to the strategy.

Compare fresh generation, ordinary coefficient preprocessing, selected-proof
reconstruction, and reconstruction with explicit fresh fallback. Charge initial
generation/build, every update, serialization, final receiver verification,
and retained source/proof/catalogue bytes. Each update may keep at most one
receipt per action; catalogue storage is reported separately. A numeric-only
ordinary formula is a separately labeled guarantee, never a free certificate.

Three fixed sequences are specified in `workloads.py`: fixed directions with
changing bounds, row withdrawals/returns, and identical bounds with version
changes. Each has six revisions × three actions. Initial events count toward
total cost. Report per-event/cumulative time, achieved guarantees, fresh fallback
count, setup, source/request bytes and peak retained serialized bytes. Serialized
size is not resident Python memory. Repeated cache/schema keys must be charged
when built and counted in storage. A fresh search may still benefit from native
internal caches; do not call it a cold process.

Run each strategy/sequence in its own fresh process with three declared
repetitions. Rotate strategy order across repetitions; no competing timed
workers run concurrently. Separate process/import startup from operation
timings; report naturally warmed within-sequence caches. Do not clear unknown
kernel caches or credit one strategy free preprocessing. Preserve each failed
attempt; retry at most three times per fixed repetition and label timing
summaries conditional on completed executions. Finite single-host results
provide descriptive cost evidence, not statistical generalization.

Compare cumulative prefix costs at equal decision quality, identifying the
first observed setup-repayment point only if the advantage persists through
the measured sequence. A missing break-even point is not infinity. F12's close
must say what these observations justify trying next; passing tests alone does
not establish distinctive contribution or discharge R-N01-01.

## Optional second comparison, declared before its collection

After the required study was available at 02:52:26 UTC, the remaining E60
block selected two stronger controls. Preserve v1 reports and implementation
snapshots. The optional study repeats the same three sequences and three
fresh-process repetitions, comparing fresh/catalogue controls with:

- **Fixed-origin reconstruction:** retain the initial receipt per action and
  always reconstruct from it. Count the new transmitted output separately
  from the retained seed. This tests whether repeatedly reconstructed traces
  explain the first study's growth; it is not an optimal retention policy.
- **Selected coefficients plus fresh fallback:** retain only the two chosen
  coefficient templates per action, screening their new budgets. A successful
  screen must emit and receive a fresh native proof. A schema change or
  insufficient candidate falls back to fully charged fresh generation and
  updates the stored coefficients. The screen supplies no unchecked certificate.
  This ordinary method has equal access and no oracle/future-sequence knowledge.

Also enumerate **60 program sources × seven consumers = 420 queries**:
error caps {0,1/997,1/100,1/43,1/21,1/20}, second-input caps
{1/5,2/9,9/40,2/7,3/10}, foreign-unit control false/true; mean edit and risk
levels {0,1/6,1/3,1/2,9/10,999/1000}. Compare native/reduct, independent
execution/full source, and ordinary formulas; receive exact thresholds and
reject slightly tighter ones. Keep full-source and reduct attainers distinct.
This is native differential breadth, not a new motivating case or F13 completion.

## Optional horizon extension

After observing small and batch-sensitive catalogue effects at 18 queries,
repeat the optional four-strategy comparison for **four cycles / 72 queries**
on each sequence, three fresh-process repetitions. Setup remains charged once
per actual schema build, and all current-source/receipt checks remain charged
at every event. No strategy receives a future sequence or reference answers.
The extension asks whether longer reuse of a catalogue changes the practical
conclusion, rather than selecting a favorable prefix after seeing results.
Initial allowance **15 engaged E minutes**, reviewed at the protected floor.
All 36 units and failed attempts are retained, including a null result.

Report both prefix comparisons: equal current-receipt availability and requested
decisions; and the stricter comparison additionally matching exact-bound quality.
A smaller valid bound and a weaker sufficient bound must not be presented as
identical outputs, although either can meet the original zero-budget request.

## Optional counterexample simplification

After the cost/coverage studies, use a bounded eight-E-minute challenge to
search gamma caps in [0,1], reduced denominator then numerator order, through
denominator 32. Fix the old all-zero source, new beta cap zero, and action T1.
Screen semantically false requests with the independent exact reference;
reconstruct every surviving true request until the first miss. Verify that
witness using fresh generation and a current receipt at the reconstructed
bound. Keep the full inspected prefix. This is a finite counterexample search,
not an oracle-assisted production strategy or a global minimality proof.

The saved corpus is also audited for duplicate/missing execution units,
exact witness/digest consistency, source-bound and source-geometry duplication,
and cost-report accounting. Report both record counts and distinct bounded
planar regions; source contexts with different syntax or revisions can share
the same geometric feasible set.
