# P3-03 internal review — development harness and attempt 1

Contributor: **ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction
reviewer**. October 7, 2026 UTC. Same-model, nonblind review; no additional
concurrent time credit. This is a static harness and saved-record audit.
**No scientific rerun was performed.**

## 1. Bound records and observed result

Read the entire [harness](../../../checks/03_bounded_logic_check.py), its
[prospective plan](../development/plan.md), and the saved
[summary](../development/attempt_1/summary.json) and
[manifest](../development/attempt_1/manifest.json). Inspected the saved input
catalogue and selected trace records without executing the method.

| Artifact | SHA-256 checked |
|---|---|
| Executed kernel | `ae757bee58089b1229cdd2e123e4650be704f04729b2fff081238c988a916247` |
| Executed harness | `2eacd06f8280a12ffa9143e869ac310445ea8c1246136888736400c16f0caaee` |
| Saved input catalogue | `a508f02ee891eb1d207de1bc92d20e9938de3afd1bbca3cb7ed5d050c7370c01` |
| Saved traces | `85941862074534b1537e8111d68ed8e119390dffe371cbf873cc2c3fd8833b0b` |
| Saved summary | `3c6eeb87ba87c68283d2492094526f7d6af51780dc4f32c72b253c1491abaa4e` |
| Saved manifest | `b5cded9523243028e6ed95ac7050d4dd21a5e7a99770d05c0609be60ec4554fa` |

The current method/harness bytes match both the manifest and summary. The
input and trace hashes match their declared bindings. The sum of per-suite
assertion counts equals **10,840**; all **twelve suites** record PASS. The
manifest's creation observation equals the summary's start observation, and
the recorded monotonic difference agrees with its host elapsed duration.

The executed method also contains the two final minor corrections from the
[implementation review](implementation_review.md): the initial committed-cell
peak is one, and repeated-container traversal is described accurately.

The harness writes the input catalogue and manifest before importing the
method or executing any suite. A new numbered directory and exclusive file
creation prevent overwriting an earlier attempt. A failed suite records its
failure and traceback and makes the summary fail; the implementation does
not silently delete failed assertions or select only passing suites.

## 2. Independence and information access

The Boolean reference uses ordinary two-valued recursion and does not call
the kernel's Strong-Kleene evaluator. The scalar loss reference independently
evaluates each exact Boolean assignment using rational arithmetic. The VM
reference is a separately written direct interpreter, without the method's
VM state constructor, transition function, or receipt helpers. These are
useful implementation comparisons, although both sides share Python and its
standard exact-rational library.

The full small-domain assignment enumeration and the VM reference answers
remain on the evaluator side of the tested API. They are not passed as
kernel configuration data, hard premises, query labels, or feedback. The
evaluator reads internal state to check it; the direction of that access does
not give the method the evaluator's computed tables. Fault injection into
pending candidates is explicitly labeled as an internal diagnostic rather
than an implemented public receipt-import API.

Some IDs are descriptive, such as `true-immediate` and `bounded-loop-false`.
Those visible names make these fixtures unsuitable for a blind anticipation
or learned-performance claim. They do not undermine the present code-path
correctness diagnostic: the kernel does not branch on the descriptive meaning
of an ID, and no anticipation advantage is claimed. Everything is development
data already exposed to the designers and reviewers.

The ordinary comparison is deliberately different from the independent
evaluators. It runs the **same engine** with an ordinary interpretation and
the same commands. The summary explicitly records `separate_algorithm=false`
and identity reconstruction. This supports operational equivalence of the
chosen interpretation, not independent replication or superiority over an
ordinary competitor.

## 3. What the assertion count covers

| Suite group | Concrete saved coverage | Supported reading |
|---|---|---|
| Cover prefixes | 22 supplied sources with one, two or three atoms; ten loss expressions; 162 checked source/report prefixes; 7,324 assertions | Disjointness, containment, loss enclosures, same-source nesting, witnesses and exact-filtering claims on these finite prefixes. |
| Partial evaluator | 306 cube visits across the repeated source catalogue; 3,256 assertions | Definite partial Boolean results hold on every completion and loss intervals enclose every enumerated completion for the supplied expressions. |
| Bounded VM | Nine supplied programs/requests; 174 assertions | True and false outputs, horizon zero and endpoint cases, a bounded loop, both requested output bits, preserved one-transaction progress and separate production/acceptance. |
| Identity, capacity and revision attacks | Equal-epoch divergent sources, one-cell XOR, source withdrawal, objective/unit change and independent receipt retention | The specifically repaired binding/reopening/retention interfaces behave as recorded. |
| Receipt and limit attacks | Seven candidate corruptions, three changed query cases, evidence-capacity retry, eight rejected rational forms, five input-shape cases and one intermediate arithmetic limit | These fault/refusal paths do not turn the tested inputs into unsupported hard answers or numeric bounds. |
| Ordinary identity and restart | Eight common commands; restarted allowance twelve versus retained allowance ten | Same-engine interpretation has identical reports/state/work on that transcript; discarded computation can defeat completion despite larger summed allowances. |

These are **assertions over reused small fixtures**, not 10,840 independent
research discoveries, arbitrary programs, random trials, or held-out examples.
The catalogue is adequate for the named development risks when combined with
the separate mathematical proof and code review. Its size does not establish
unrestricted correctness or a convergence rate.

## 4. Important oracle scope

The generic `exact_source` reference evaluates `kernel.constraints`, and the
generic loss checks evaluate `kernel.losses`. The evaluators are independent
of the partial-evaluation algorithm, but their semantic inputs are the active
records *after admission*. Therefore this generic comparison alone would not
catch every hypothetical bug that silently replaced an original caller
constraint or loss with a different one during admission.

The current static admission review checks the actual copying/validation
route, and targeted tests also use hard-coded expected bounds, explicit source
identities, changed query fields and conditional/checked-status distinctions.
Those supplement the generic oracle. The appropriate claim is independent
evaluation of the declared active finite source and supplied expressions,
with separately reviewed input binding. Do not describe the generic oracle
as an independent end-to-end proof of every caller-meaning transformation.

Likewise, the independent VM comparisons check answer, executed count, halted
status and output on nine cases. They do not enumerate every allowed register
machine or independently reconstruct every intermediate terminal-state hash.
The general semantic bridge rests on the transition definition and its
reasoning, supported by these diagnostic executions.

## 5. Selected trace checks

The one-cell XOR trace retains interval `[0,2]`, unresolved feasibility and
incomplete filtering after its allowed work. With sufficient cells, the source
is exactly filtered, has a checked finite witness and gives loss `[1,1]`,
while both opaque truth coordinates remain unresolved. This directly supports
the task-specific refinement claim.

The revision trace moves from `[2,2]` under two dependent premises to `[0,2]`
after withdrawing their root. Changing the objective subsequently gives
`[-6,0]` in its new units while preserving the source. The evidence-capacity
trace moves from unresolved truth with process phase `capacity` to checked
truth with phase `done` after space is freed. The arithmetic-limit trace has
no numeric bound and preserves its source cover.

These saved examples address concrete scientific obligations. Their meanings
remain conditional on the admitted source and the fixed finite VM/loss
semantics. They are not calibrated forecasts or measurements of learning
before an individual query is resolved.

## 6. Disposition

The saved PASS result is internally consistent and supports the stated finite
development examples. The independent evaluators, input/access declarations,
fault cases and identity-comparison labeling are appropriate for this scope.
No broad rerun is needed merely to increase the count. The principal should
retain the proof-level conditions, the active-record oracle qualification and
the absence of a blind performance claim when summarizing these results.
