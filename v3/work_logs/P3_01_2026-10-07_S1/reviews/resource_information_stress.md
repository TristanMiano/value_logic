# P3-01 resource and information stress review

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal review; not external validation.
Resource time is unmeasured and supplies no additional research-floor credit.
Scope: the current P3-01 contract and finite development check, not a P3-03 or
P3-08 implementation. No canonical file, saved attempt or freeze was changed.

## 1. Overall assessment

The current contract names the right resource and information obligations. It
charges source inspection, prediction, checking, storage, representation
construction and repair search; permits ordinary methods to use visible
shortcuts; separates selected feedback from full feedback; and now distinguishes
forecasts before resolution from reports after paid resolution. The draft also
warns that projection can change an online learner's guarantee.

These principles need several concrete fields before a later comparison can
be audited. In particular, “one VM step,” “one value,” “the same library” and
“the revealed loss” are not sufficiently specific measures on their own. The
examples below show finite ways that each phrase can hide an advantage. They
do not establish that the current, still prospective implementation has
committed those errors.

## 2. Finite separating examples

### RI01 — a richer primitive changes the computational task

An input consists of sixteen accessible Boolean positions, and the target is
their parity. In a deterministic bit-query interface, suppose an exact method
stops after inspecting at most fifteen distinct positions. At least one position
was not read. Changing only that bit preserves every response the method saw
and reverses parity. Therefore the method cannot be correct on both inputs.

This is a finite exact lower bound for the stated bit-query interface. If another
method receives a `PARITY16` primitive charged as one operation, it can answer in
one operation. The two operation counts describe different machines. Likewise,
a word-level machine that reads all sixteen bits at once is a different declared
interface; it is not invalid, but its primitive must be available symmetrically.

**Protocol consequence:** identify the primitive instruction set, input-access
granularity, word size, arithmetic semantics, overflow behavior and native
library calls. Count variable-size operations by a specified rule or report
measured resource use for them. A checker node, a Python call and one VM bit
read cannot be exchanged at unit cost without an explicit model.

### RI02 — one exact coordinate can contain a whole finite label table

For labels `y_0,...,y_15`, the integer

```math
M=\sum_{i=0}^{15}2^i y_i
```

stores all sixteen labels. Reading bit `i` recovers `y_i`. This is one integer
coordinate but up to sixteen bits of information. There are `2^16` possible
tables and the same number of possible values of `M`. An exact dyadic rational
encoding gives the same issue in the interval `[0,1]`.

A coordinate-count comparison may be mathematically appropriate for an exact
linear representation theorem. It is not a byte, precision or access-cost
comparison. Allowing arbitrary exact reals with uncharged digit extraction is
more powerful still and has no finite executable representation contract.

**Protocol consequence:** report encoded bit/byte length, integer and rational
numerator/denominator sizes, working precision, rounding rules, access costs and
whether a representation is explicit or implicit. Include decoder/program size
and external referenced data. A discarded table cannot be recovered for free
through a short identifier or a decoder containing that table as advice.

### RI03 — a visible program shortcut is legitimate information

Consider a program schema that performs a fixed sequence of no-op instructions
and then returns a literal bit. A bounded-execution question asks whether its
output is one before a horizon large enough for those instructions. The literal
and schema can make the answer easy to prove by reading the program, without
performing every simulated instruction. A method restricted to black-box
simulation is a weaker comparator if another method sees that syntax.

By contrast, a file named `answer_true_17` can leak a label that was never meant
to be an agent observation. An explicit label-table index can do the same if
the table is accessible. These two cases need different dispositions: permit
and charge legitimate semantic shortcuts for both methods; remove unintended
evaluation metadata from both interfaces before the final challenge.

**Protocol consequence:** specify the exact input bytes and metadata each method
can read, including program text, identifiers, serialization order, generator
parameters, lengths, hashes, filenames and cached results. “No label column”
is not a complete information restriction. Conversely, do not prohibit a
valid static proof merely to make the benchmark look difficult.

### RI04 — precomputation can move the whole cost outside the measured round

Suppose a declared finite library has 256 entries and computing each answer
costs sixteen units under its stipulated access model. A full table then costs
4,096 units to build. If each lookup costs one, its total over `N` uses is
`4096+N`. Recomputing each answer at sixteen units costs `16N`. Under these
simplified assumptions, precomputation first wins at the integer horizon
`N=274`, not on the first query. The table's storage also has a cost.

This illustration is not a recommended baseline that repeatedly ignores its
own discoveries. A strong ordinary method may cache lazily and reuse repeated
answers too. The point is that a cold-start comparison, a warm-cache comparison
and an amortized lifetime comparison are different services.

**Protocol consequence:** provide a registry of admitted libraries, model
parameters, proofs, calibration data, advice strings and caches, with hashes,
creation/exposure stage, acquisition cost and permissible reuse. State cache
reset boundaries and amortization horizon. Distinguish common supplied advice,
method-specific learned artifacts and an oracle diagnostic. Pretraining that
contains the evaluation answers is not ordinary generalization simply because
its bytes appear in a parameter vector rather than a table.

### RI05 — a helpful projection for one score can harm another score

For a claim and its negation, let the raw forecasts be `(9/10,9/10)` and the
actual labels be `(1,0)`. Euclidean projection onto the coherence constraint
`p(phi)+p(not phi)=1` gives `(1/2,1/2)`.

| Score | Raw forecasts | Projected forecasts |
|---|---:|---:|
| Squared loss for currently queried `phi` | `1/100` | `1/4` |
| Sum of squared losses for both coordinates | `41/50` | `1/2` |

Thus projection improves the full-vector score but worsens the currently scored
coordinate. Repeating this scoring schedule produces a linear cumulative
difference. A guarantee for total-vector squared loss cannot simply be imported
as a per-query regret guarantee. A projection using the relevant coordinate
weights can behave differently; for example `(9/10,1/10)` is coherent and keeps
the current claim's forecast unchanged.

There are positive composition rules too. A common convex mixture of coherent
expert vectors preserves linear coherence constraints. But choosing one expert
for `phi` and a different expert for `not phi` can destroy coherence: experts
`(1,0)` and `(0,1)` are each coherent, whereas choosing their favorable first
and second coordinates produces `(1,1)`.

**Protocol consequence:** retain raw and postprocessed forecasts, the active
constraint set, projection/normalization method, metric/weights, update timing,
solver budget and certified versus approximate status. State which score and
which comparator receive the claimed guarantee. Arbitrary “coherence repair”
is neither computationally free nor a theorem-preserving wrapper by default.

### RI06 — selective proof discovery can make a resolved subset look perfect

Take 100 unresolved Boolean claims, with fifty eventually true and fifty false.
A forecast always reports probability one. Suppose the acquisition mechanism
only returns proofs of true claims and never returns refutations. On the fifty
resolved claims, accuracy is one and Brier loss zero. On the full cohort,
accuracy is one half and mean Brier loss one half. The unobserved false labels
were not made true by the absence of returned proofs.

The result on the resolved subset is a correct conditional description. It is
not performance on the original cohort. Comparisons can also become unfair if
one method is scored on its easy selected subset and another on a harder
selected subset. Charging the acquisition cost alone does not remove this
selection problem.

**Protocol consequence:** retain the full issued-query cohort, eligibility,
pre-acquisition forecast, discovery policy, query costs, first resolution time,
label source, delayed/pending/censored status and scoring rule. Report common
cohort results where available, plus method-specific coverage and conditional
results. Any statistical correction for selection needs its own assumptions;
unresolved labels are not zero losses. A hidden evaluator may compute later
cohort scores, but must not provide those labels to either agent early.

### RI07 — paying to construct a model does not make its unidentifiable parts known

The already specified observational-twin example has two models with identical
observed `A=B=U` but different outcomes under intervention on `A`. In one,
`B` tracks `A`; in the other, `B` tracks the common source `U`. With `U=0` and
the declared loss `2+A-2B`, intervention `A=1` gives losses one and three.

Giving only one method the correct causal graph supplies extra information.
Counting its graph object as one cheap construction does not recover fairness.
Nor can paying more observational search identify a distinction that all
permitted observations leave identical. Additional intervention evidence or
an explicit structural assumption is needed.

Similarly, a supplied catalogue containing exactly the favorable repair may
already encode the answer. Exhaustively searching that tiny catalogue says
little about the cost or epistemic justification of discovering it.

**Protocol consequence:** classify every graph, repair catalogue, ranking,
similarity metric and propagation rule as stipulated common input, learned
from identified evidence, discovery-selected, or oracle information. Record
construction/search costs and semantic assumptions separately. Enumerated,
best-found and certified-optimal candidate sets need distinct statuses. Both
methods must have access to the same permitted alternative space and evidence.

## 3. Recommended protocol fields

These are future implementation/freeze obligations. P3-01 need not choose the
final numeric values, instruction set or learning algorithm now.

| Record group | Minimum fields or choices needed |
|---|---|
| Machine and primitive model | VM/version, instruction semantics, input-access granularity, word size, integer/rational arithmetic, native calls, operation charging rule, overflow/rounding, timeout behavior. |
| Resource account | Per-round and cumulative hard limits; CPU/wall distinction if measured; persistent state, peak memory and read/write volumes; storage duration unit; setup cost; amortization horizon; priced versus unpriced components. |
| Information interface | Exact readable fields/bytes, query/program identity, permitted static inspection, generator metadata, hidden evaluator fields, shortcut audit and common permissions. |
| Artifact/advice registry | Content hash, authoring/acquisition stage, permitted label exposure, construction/training cost, library/model/cache contents, access path, reset and invalidation policy. |
| Numeric representation | Explicit/implicit status, encoded byte size, number of coordinates, precision, rational bit lengths, decoder size/cost, referenced data and approximation error. |
| Forecast and postprocessing | Pre-resolution and final report timestamps; raw/coherent output; selected constraints; projection metric/weights; algorithm and budget; solver status; forecast and comparator score definitions. |
| Feedback and cohort | All issued queries, earlier known status, acquisition choices/costs, first accepted resolution, label source, full/partial feedback, delay/censoring, common and method-specific scoring cohorts. |
| Structural/repair input | Stipulated versus learned versus oracle status; candidate grammar/catalogue; construction evidence and cost; semantic propagation; hard constraints; ranking/tie rule; best-found/complete/optimal certificate status. |
| Comparison scope | Same information/action/primitive permissions, own algorithmic costs, common supplied costs, reused artifacts, expected versus realized costs, exactness/tolerance and comparator class. |

“Same budget” need not mean the same algorithm or the same number of operations.
Different algorithms are the point of a comparison. It means their permissions,
primitive costs, resource limits and accounting conventions are specified so
that an advantage cannot be introduced through an unreported oracle or a cost
moved outside the horizon.

## 4. Review of the actual finite check and saved result

### 4.1 What was inspected

- Source: `v3/development/p301_contract_checks.py`.
- Saved result: `v3/work_logs/P3_01_2026-10-07_S1/finite_checks_1.json`.
- Its original start marker was read and retained. The development attempt was
  not rerun or overwritten for this review.
- The result's source SHA256 matches the current script:
  `23ddbfc0a324fa27947e152d889b617be6ab3a2884106547d57812b51f411aba`.
- The record reports CPython 3.12.14 on Linux, `data_class=development`,
  `frozen_evaluation=false`, status PASS, eleven completed groups and no failure.
- Group assertion counts sum to the recorded **3,449 assertions**. Of these,
  **3,375** enumerate a grid for the `2 epsilon` decision-cost bridge. These are
  not 3,449 independent experiments, benchmarks or different theorems.
- Recorded process CPU is `36,083,111 ns`; the monotonic measured section is
  `37,932,447 ns`. These are the check script's local costs, not a reasoner's
  task cost or a method comparison. The final record write/print occurs after
  the end samples, so these numbers are not the entire command's end-to-end cost.

### 4.2 Actual tested scope

| Group | What it checks | What it does not check |
|---|---|---|
| `finite_fragment` | Three-bit enumeration, complementary relation, successive selected constraints, a conflict, and an omitted-row bound witness. | A VM, proof production, checker soundness, a scheduler, calibrated weights or budget enforcement. Status strings are reported fixture labels, not a tested state-machine implementation. |
| `binary_bridge`, `joint_decision` | Exact rational arithmetic for known-stakes inversion and two stipulated joint laws. | Learning unknown probabilities, identification for arbitrary loss matrices, empirical calibration or resource advantage. |
| `fallible_models` | Two endpoint calculations and the reversal at two declared domain radii/prices. | The whole-interval inequality without its written monotonicity argument; model discovery; a logical-query performance improvement. |
| `operation_cases` | Explicit assigned observation and intervention values in the small examples. | A general structural-equation interpreter, causal-graph learning or a method discovering the propagation rule. The two observational tuples use the same explicit values by construction. |
| `repairs` | All forty deletion subsets of the three supplied presentations, each with four Boolean assignments; exact minima and tied loss sets. | General repair completeness, catalogue construction, a principled representation-invariant ranking, or logical counterpossible semantics. |
| `paid_reasoning` | Stated high/low-stakes costs and the four supplied XOR observation subsets. | A learned value-of-computation model or general metareasoning policy. The JSON correctly says best catalogue loss; arbitrary adaptive policy optimality is not established by enumerating four fixed subsets alone. |
| `predictions_and_decisions` | Fixed score contrasts and 3,375 rational-grid cases of the decision lemma, including an attaining case. | Training an online learner, calibration, arbitrary continuous cases without the written proof, delayed feedback, or projection composition. |
| `withdrawal_and_prices`, `report_feedback` | Fixed numerical revision and inherited report-dependent Brier calculations. | A live dependency cache, source-drift estimator, general feedback learner or a newly established causal self-model. |
| `event_intervals_and_costs` | Eight event indicators and one nonbinary cost across explicitly supplied vertices; the robust decision separation. | Learning a credal set, general recovery of lower expectations, or an experimental advantage. Its validity for the specified convex hulls uses linear extrema at supplied vertices. |

The script is appropriately small and exact for its advertised development
purpose. It uses `Fraction`, preserves completed group results after each
group, records a failure if an ordinary exception occurs, and refuses an
existing output or start marker. Those implementation properties were inspected
in code, not tested by injecting crashes or competing runs. Atomic replacement
is useful for normal process failure; absence of an explicit disk flush means
the review does not certify durability against a machine/power failure.

No change to the completed finite check is required merely to cover the new
resource examples. Its report should continue to say **exact finite development
checks**, not an implemented bounded reasoner, a frozen evaluation or validation
of every interface duty.

## 5. Recommended disposition

Add a compact resource/information closure requirement to the main contract and
use the fields above at the implementation and freeze stages. Carry RI01,
RI02, RI05 and RI06 as particularly useful finite stress cases: they separate
machine primitives, precision, score composition and feedback selection without
requiring a new research program.

The current numerical examples remain sound at their stated small scope. The
strong ordinary comparator is a good design; the remaining work is to make its
shared access and charging conventions inspectable. None of these observations
is evidence that value logic is unable to improve a matched task. They specify
what a claimed improvement would have to survive.
