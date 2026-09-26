# Value Logic Phase Two: Build the Value-Based Calculus First

Last updated: September 26, 2026 (UTC).
Status: F01–F03 complete at their task scopes; F04 continuation partial; no permanent calculus selected or readiness gate passed.

## Resume here

This is the active project-control document. Read it together with
[v2/RESEARCH_PROTOCOL.md](v2/RESEARCH_PROTOCOL.md), [v2/README.md](v2/README.md),
the latest applicable gate record, and the selected task's prior sessions.
Read relevant phase-one material as needed; do not spend every session rereading
the entire original paper or its completed task history.

**Next task: F04 — hostile examples and candidate discrimination.**

**Active repair queue: empty.**

**Gate state: A not attempted; B not attempted; C not attempted; D not attempted.**

Select the pointer, not mechanically the first unchecked task. A failed or
invalidated gate can put an earlier repair ahead of later numbered tasks.
One selected task, repair, or gate attempt is the scope of a prompt unless the
user explicitly requests a batch. A task may span multiple sessions. Stop
with a durable partial record when necessary; do not mark a time floor or
proof obligation satisfied without its evidence.

Historical reference: [TODO_v2_contracts_archive.md](TODO_v2_contracts_archive.md)
is the superseded contract-and-inverse roadmap, not an alternate execution
queue. [TODO.md](TODO.md) remains the completed phase-one history.

## Project question

> What semantic objects and inference rules let an agent reason from pragmatic
> value, without requiring possession of final metaphysical truth?

The aim is a small calculus that derives justified conclusions about uses and
compositions from premises, not merely an algorithm that attaches a number to
a proposition and thresholds it. Candidate semantics must earn their place
through separating examples, proofs, explicit comparisons, and executable
checks. Scientific model succession supplies motivating examples, not an
obligation to undertake a second full model-comparison research program here.

### Fixed commitments and revisable choices

The philosophical commitments are lack of direct access to final metaphysical
truth, pragmatic reliance on revisable models with tolerable error or reward
and resource costs, and investigation of value as the primary semantic object.
These motivate the research; they do not uniquely derive a mathematical system
or prove that absolute truth does not exist.

Everything more specific is provisional: scalar versus structured value,
bounded versus unbounded ranges, orders and operations, evidence states,
contexts, contracts, probability, inference syntax, revision rules, and neural
architecture. Ordinary mathematical proofs are permitted in an explicitly
stated metatheory; their use is not a claim of metaphysical access.

The phase-one calculus is a completed realization, not an immutable core. Its
results may be reused with their hypotheses, adapted, compared, or not imported.
Do not rewrite their historical claims to make the new design appear inevitable.

## Active direction after F03

[DIR01](v2/decisions/DIR01_loss_grounded_reflective_direction.md) adopts a
loss-grounded, utility-oriented research direction. Treat RLL-like mechanisms
as a serious starting comparison; require more than numerical truth degrees.
Modest reflection and an exploratory connection to normally trained networks
are active aims, not indefinitely deferred branches. The
[opportunity register](v2/opportunities.md) supports bounded agent initiative.
At the DIR01 amendment checkpoint F03 stayed complete and F04 was unstarted;
its current work status is recorded below.

## Required research distinctions

Keep separate (1) a value object, (2) its evaluation or summary, and (3) a
justified inference involving it. The separation itself should be tested, not
inflated into gratuitous data structures. Test what information composition
needs and which distinctions an actual consumer uses.

Do not assume that a scalar summary determines a composite operation. One
required starting test is the equally weighted two-scenario comparison
`X=(3,-1), Y=(-1,3)` versus `X=(3,-1), Y=X`: the individual means coincide
across the two cases, while the means of their pointwise minima differ. F01
must work out the calculation and its exact implication; it is a diagnostic
example, not a decision to make pointwise minimum a logical connective.

Explore unbounded values explicitly. A bounded implementation example is
allowed, but a monotone squashing map is not automatically an algebra- or
inference-preserving equivalence. Similarly, operational choice, joint use,
sequential use, and rejection need not coincide with Boolean and/or/not.

## Research execution and timing

The [research protocol](v2/RESEARCH_PROTOCOL.md) is binding for this queue.
Its essential rules are:

- Separate **D: derivations and worked theory**, **L: external literature**, and
  **E: empirical/computational tests**. Keep durable evidence for each. The
  provisional cycle allocation is 60/15/25; D is normally the largest share.
  Code is permitted inside a derivation task when it is likely to be useful,
  but its execution time is E, not a substitute for a protected D minimum.
- Before each attempt forecast central/high effort by D/L/E/O and expected tool
  waiting. Record real UTC and monotonic clocks, check at least every 15 active
  minutes and at transitions, and report actuals and forecast error. Do not
  count idle or unknown time, or fabricate retrospective durations.
- Protect selected 60- or 90-minute research blocks. They may span sessions.
  Both the minimum and substantive evidence are required for completion. Early
  success leads to assumption testing or an alternative derivation, not
  artificial waiting. Budget exhaustion leads to replanning, not a false pass.
- Allocate both reliable gains and difficult/uncertain gains. Start at 60% R /
  40% X of research time, an axis independent of D/L/E; audit actual allocation
  at gates and preserve concrete work in both lanes.

Use [v2/templates/work_item.md](v2/templates/work_item.md) for forecasts, clock
segments, research notes, result evidence, and gate decisions. O denotes
administration/formatting overhead and does not satisfy research minimums.

### Initial effort allocations

Minutes below are provisional engaged-work allocations, **not measured time or
promised wall-clock completion**. `Review at` means stop to reforecast or
reshape the attempt, not a deadline that makes an unproved claim complete.
`D60` means at least 60 measured engaged derivation minutes across that task;
analogously for L/E. `None` means no floor beyond adequate evidence, not no
forecast or clock recording.

| ID | Initial minutes | Review at | Protected minimum |
|---|---:|---:|---|
| F01 | 90 | 180 | D60 |
| F02 | 120 | 240 | D60 |
| F03 | 120 | 240 | L60 |
| F04 | 120 | 240 | D60 |
| Gate A | 60 | 120 | None |
| F05 | 120 | 240 | D60 |
| F06 | 150 | 300 | D90 |
| F07 | 180 | 360 | D90 |
| F08 | 180 | 360 | D90 |
| F09 | 120 | 240 | D60 |
| F10 | 90 | 180 | L45 |
| Gate B | 60 | 120 | None |
| F11 | 120 | 240 | E60 |
| F12 | 90 | 180 | E45 |
| F13 | 120 | 240 | D60 |
| F14 | 60 | 120 | None |
| F15 | 120 | 240 | E60 |
| F16 | 120 | 240 | D60 |
| Gate C | 60 | 120 | None |
| F17 | 120 | 240 | None |
| Gate D | 60 | 120 | None |
| **Initial traversal** | **2,280 (38 hours)** | **Reforecast per item** | **Not a phase-wide timebox** |

Initially reserve a further 570 engaged minutes (9.5 hours, 25%) for repair and
reconsideration. The resulting 47.5-hour planning envelope is a starting
allocation, not a phase limit, guaranteed duration, or demand to consume time.
The source of a failed gate determines how that reserve is used. Forecasts
must be revised using measured progress; there is no fixed lifetime limit on
phases or recurrence cycles.

## Evidence gates and recurrence

The overall route is:

```text
F01-F04 -> A -> F05-F10 -> B -> F11-F16 -> C -> F17 -> D
              ^ failure anywhere can return to an earlier dependency
```

A gate is a hypothesis about readiness, not a ceremonial checkpoint. PASS
requires the specific evidence listed below, with no unresolved blocking issue
in a result it authorizes. Its note records exact artifact versions, evidence,
clock totals, research-mode and R/X allocation, and the selected next task.
Passing a gate is relative to the declared fragment and evidence, never a
certificate of metaphysical truth.

On failure, record the criterion, smallest witness or gap, earliest affected
dependency, and stale downstream claims. Create a repair item such as
`R-B-1-01` with a fresh forecast and acceptance evidence; place it in the active
queue and move the pointer to it. A completed review can record BLOCKED while
the gate checkbox remains unchecked. Retain completed historical tasks and old
passes; add revisions and invalidations instead of erasing history.

| Failure found | Default return target |
|---|---|
| Examples are underspecified or do not distinguish candidates | F01/F04 |
| Representation loses information needed by an operation | F02/F05 |
| Inference rule is false or its scope is unclear | F05/F06, then affected proofs |
| Soundness/completeness proof has a gap | F07/F08; F05/F06 if structural |
| External result was misapplied or contribution misunderstood | F03/F10 and dependent claims |
| Executable semantics differ from declared semantics | F11/F12; reopen B if the specification changes |
| Demonstrator is vacuous or evidence does not support usefulness | F13/F14, or F01/F06 if no meaningful inference exists |
| Reporting drifts from checked claims | F17 or the affected earlier gate |
| Timing or independent-review evidence is missing | Resume the relevant obligation; do not invent it |

After two unsuccessful cycles on the same blocker, compare at least two
strategies and choose a discriminating next test. Change a rule, carrier, or
fragment when warranted. A restricted positive result can survive a failed
ambitious conjecture; failure alone does not authorize claiming the original
result. Continue, narrow, or suspend that candidate explicitly. Do not proceed
to publication with an unsound core simply because the planned queue ended.

## Numbered task queue

### Preserved history

- [x] **Historical Task 0 — map the first-paper inheritance boundary.**
  Completed August 1, 2026 under the archived follow-up plan. The original note
  is preserved in [v2/inheritance_contracts_archive.md](v2/inheritance_contracts_archive.md).
  Its content remains historical evidence; its inheritance choices are not
  requirements of the new phase.

- [x] **R0 — authorize and install the calculus-first roadmap.**
  September 19, 2026. Replaced the prospective queue, added evidence-driven
  recurrence and measured-effort rules, and archived the prior control files
  without changing the completed research. See
  [decision record](v2/decisions/2026-09-19_calculus_first.md).
  This is roadmap administration, not completion of F01 or satisfaction of a
  foundational research minimum.

### Cycle I — requirements, candidates, and separating evidence

- [x] **F01 — requirements and separating examples.**

  Principal artifact: `v2/foundations/01_requirements_and_separating_examples.md`.
  Derive at least six small examples spanning cheap versus accurate model use,
  task changes, joint/sequential composition, dependence hidden by scalar
  summaries, conflicting or incomplete evaluation, and alternative toy axiom
  systems. Include at least one unbounded-value example. Distinguish desired
  expressive/inferential capability from a preferred representation. State
  what cannot be concluded in each example and calculate the starting
  two-scenario witness explicitly.

  Bootstrap concise `v2/project_spec.md`, `v2/claim_ledger.md`, `v2/notation.md`,
  and `v2/time_ledger.csv`; keep research claims unproved unless demonstrated.
  These supporting records do not replace the principal derivation artifact.

  **Done when:** examples have explicit inputs, operational questions, expected
  distinctions and assumptions; fixed commitments and optional choices are
  separated; timing and claim tracking work; D60 is recorded.

  **Partial session — September 20, 2026.** Created the
  [principal derivation note](v2/foundations/01_requirements_and_separating_examples.md)
  with eight worked examples, query-specific positive controls, and additional
  dependence countermodels. Bootstrapped the project specification, claim and
  notation records, and [time ledger](v2/time_ledger.csv); 26 exact-arithmetic
  fixture tests passed locally. Recorded 15.97 engaged D minutes, leaving 44.03
  minutes of the D60 floor. This is not task completion, independent review, a
  selected calculus, or a passed gate. See the
  [session record](v2/work_logs/F01_2026-09-20_S1.md) for exact clocks,
  evidence, validation limits, and its then-pending review obligations. At the
  end of that session F01 remained unchecked; F02 had not begun.

  **Completed — September 21, 2026.** Reconstructed the eight examples and
  added [worked information-contract and assumption audits](v2/foundations/01a_reconstruction_and_information_contracts.md),
  including sharp covariance-based bounds, tolerated common-model fitting,
  finite-precision and tail conditions, and useful decisions without exact
  value recovery. Added 50 reconstruction checks; the combined F01 discovery
  command passes 76 tests. Updated the claim ledger, notation, and specification.
  Session S2 credits 44.274346 derivation minutes; cumulative F01 D time is
  60.243613 minutes, satisfying D60 without counting unmeasured gaps or tool waits.
  The [completion record](v2/work_logs/F01_2026-09-21_S2.md) links the raw clocks,
  proof/test evidence, and validation boundaries. F02 is selected but not begun;
  all gates remain unattempted. No core, independent review, or novelty is claimed.

- [x] **F02 — derive competing semantic candidates.**

  Principal artifact: `v2/foundations/02_candidate_semantics.md`.
  Compare at least three substantially different candidates, including a
  scalar/summary baseline and richer context-indexed or ordered alternatives.
  Give each concrete carriers, operations, units/context treatment, and at
  least two worked examples. Analyze what each preserves and discards and how
  bounded/unbounded variants differ. Do not choose a winner on familiarity or
  encode the whole original object without explaining useful structure.

  **Done when:** a common example table separates at least two candidates;
  simplifying assumptions and unproved claims are explicit; D60 is recorded.
  Protect exploratory time for a candidate that is not the easiest extension
  of the phase-one design.

  **Partial session — September 21, 2026.** Compared four concrete candidates
  in the [candidate note](v2/foundations/02_candidate_semantics.md): evaluated
  scalars, aligned profiles, continuation-value transformers, and achievable
  guarantee fronts. Each has explicit operations, multiple worked examples,
  scope/units, and bounded/unbounded analysis; the common table distinguishes
  their admitted information and composition questions. Added 53 passing exact
  checks and recorded candidate-level proofs, counterexamples, and open issues.
  Credited D time is 17.095003 minutes; 42.904997 minutes of D60 remain.
  See the [session record](v2/work_logs/F02_2026-09-21_S1.md) and
  [claim entries](v2/claim_ledger.md). At the end of S1, F02 remained unchecked;
  no core or gate was selected and F03 had not begun. S1 was delivered as a local
  patch because its then-available connected tools exposed no repository writes.

  **Completed — September 22, 2026.** Added the
  [candidate reconstruction](v2/foundations/02a_candidate_reconstruction.md):
  exact scalar/convex-budget boundaries, observation-sensitive choices,
  continuation and budget composition, finite-transformer characterization,
  quantitative guarantee-set substitution, nonlinear-test countermodels, and
  bounded-coordinate precision repairs. The original common example table is
  retained and a shared signal/cost example interprets all four candidates.
  Added 71 checks, bringing dedicated F02 discovery to 124 passing tests.
  Updated notation, claims, and the project specification. Session S2 credits
  44.023292 D minutes; cumulative F02 D is 61.118295 minutes, meeting D60.
  The [completion record](v2/work_logs/F02_2026-09-22_S2.md) contains measured
  actuals, source-use limits, same-agent review, and validation boundaries.
  F03 is selected but not begun. All gates remain unattempted; no final core,
  unrestricted calculus soundness result, independent review, or novelty is claimed.
  The downloadable completion package is cumulative from the F01 main snapshot
  and also contains a delta for an exactly applied, committed S1 package.

- [x] **F03 — external foundations audit.**

  Principal artifact: `v2/literature/01_foundations.md`, with
  `v2/references.bib` as a supporting bibliography.
  Verify roughly 5-8 load-bearing primary sources relevant to the actual
  candidates: quantitative/equational or ordered calculi, decision/value
  semantics, and uncertainty or compositional reasoning as needed. Derive the
  mappings to this project's definitions; do not perform an indiscriminate
  survey. Check which proposed laws/results are known and their hypotheses.

  **Done when:** every imported result has an exact usable statement and
  locator, candidates have a literature comparison, and L60 is recorded.
  Unverified sources remain leads; novelty is not inferred from a small search.

  **Partial session — September 22, 2026.** Created the
  [foundations audit](v2/literature/01_foundations.md), a versioned
  [source manifest](v2/literature/F03_sources.json), the
  [bibliography](v2/references.bib), and
  [worked import-boundary mappings](v2/literature/01a_import_boundaries.md).
  Eight core primary sources and three targeted supplementary checks identify
  precise antecedents and hypothesis mismatches; 31 finite checks pass locally.
  Credited L time is 6.030494 minutes, leaving 53.969506 minutes of L60.
  F03 remains unchecked and selected. See the
  [session record](v2/work_logs/F03_2026-09-22_S1.md) for scope, actual clocks,
  source-access limits, and remaining proof-system review. No F04 or gate started.

  **Continuation — September 22, 2026, S2.** Rechecked proof-system and solver
  assumptions; added the targeted 2026 Rational Lawvere Logic source and
  [worked source-adapter checks](v2/literature/01b_proof_system_audit.md).
  The new suite passes 39 tests; both F03 suites pass 70 together. Source IDs
  S01-S11 and the S1 history remain intact. This session credits 17.200387 L
  minutes; cumulative F03 L is 23.230881, leaving 36.769119 of L60.
  Three mixed intervals were conservatively excluded from L credit. See the
  [S2 record](v2/work_logs/F03_2026-09-22_S2.md) for the amendments and exact clocks.
  F03 remains unchecked and selected; F04 and all readiness gates remain unstarted.

  **Continuation — September 23, 2026, S3.** Resumed from the last published
  S2 checkpoint after interrupted attempts. The author's proposed Lawvere/value
  bridge is examined in [a scoped translation audit](v2/literature/01c_lawvere_value_bridge.md):
  nonnegative costs, finite signed pairs, a restricted bridge to Abelian logic,
  and signed values with nonnegative directional replacement loss. Added one
  targeted signed-algebra source (S13), preserving all prior source identities.
  The new 32 tests and combined 102 F03 checks pass locally. Credited L is
  4.298997 minutes; cumulative L is 27.529878, leaving 32.470122 of L60.
  The [S3 record](v2/work_logs/F03_2026-09-23_S3.md) preserves source-text issues,
  exact timing, initial test failure and repair, and the local-only delivery.
  F03 remains unchecked and selected; no F04, core choice, or gate is advanced.

  **Resumed September 23,2026 (S4R1).** Incorporated the saved S3 bridge and
  added a [belief/KL source audit](v2/literature/01d_belief_kl_objectives.md)
  with finite probability, normalization, loss-combination and continuation
  mappings. Five targeted sources join the earlier audit;33 new numeric checks
  bring F03 discovery to135 passing checks. Cumulative credited L is
  30.831357 minutes; 29.168643 remain. The recovered unclosed attempt adds no
  credit. [The work record](v2/work_logs/F03_2026-09-23_S4R1.md) preserves proof/source
  limits and actual clocks. F03 stays unchecked and selected; no F04 or gate.

  **Continuation — September 24, 2026, S5.** Verified the author's local push
  at `f9d5ef6`. The [context/source audit](v2/literature/01e_belief_value_import_contracts.md)
  distinguishes value-summary equality from stability under belief updates,
  gives an exact counterexample and repair for S16's parameter-convexity claim,
  and supplies rational logarithm/KL certificates at the RLL import boundary.
  Forty new tests and 175 combined F03 checks pass locally. No source is added;
  the S16 disposition is corrected with its earlier record retained.
  Credited L is 2.090113 minutes; cumulative L is 32.921469, leaving 27.078531.
  Three mixed blocks receive no L credit. See [S5](v2/work_logs/F03_2026-09-24_S5.md).
  F03 remains partial and selected. This is a local package, not a pushed commit
  or a passed readiness gate; no F04 work is started.

  **Continuation — September 24, 2026, S6.** Verified the author's S5 push at
  `9ba491f`. The [consolidated handoff](v2/literature/01f_consolidated_source_handoff.md)
  and [import register](v2/literature/F03_import_contracts.json) state the usable
  interfaces and guards for the existing 18 sources, without adding references.
  Two finite adapters address directed profile gains and pointwise arithmetic
  versus uniform witnesses/belief types. Fourteen new tests and 189 combined
  F03 checks pass locally. Credited L is 5.615791 minutes; cumulative L is
  38.537260, leaving 21.462740. Mixed, interrupted and retrieval intervals are
  not credited. See [S6](v2/work_logs/F03_2026-09-24_S6.md). This is a local package;
  F03 remains partial and selected, with no F04 or gate started.

  **Continuation — September 24, 2026, S7.** Verified the author's S6 push at
  `e1454a8`. The [source-rule audit](v2/literature/01g_checked_source_derivations.md)
  provides explicit residual and finite signed-coordinate derivations, checked
  by a deliberately small source-rule validator. It lists the exact finiteness,
  multiplicity and substitution obligations rather than borrowing completeness
  for a different language. Eighteen new checks and 207 combined F03 tests pass.
  Credited L is 3.138728 minutes; cumulative L is 41.675988, leaving 18.324012.
  See [S7](v2/work_logs/F03_2026-09-24_S7.md). This is a local incremental package;
  F03 remains partial and selected, with no F04, core choice or gate advanced.

  **Continuation — September 24, 2026, S8.** Verified the author's S7 push at
  `bbd5431`. The [context/witness audit](v2/literature/01h_context_and_witness_audit.md)
  records an extension condition for related-variable elimination and a finite-
  potential optimality-certificate existence boundary. Positive finite cases
  are retained; no additional bibliography entries or core selection. Fifteen
  new tests and 222 combined F03 checks pass. Credited L is 4.577898 minutes,
  cumulative 46.253886, leaving 13.746114. See
  [S8](v2/work_logs/F03_2026-09-24_S8.md). This is an incremental local package;
  F03 stays partial and selected, with F04 and all gates unattempted.

  **Continuation — September 24, 2026, S9.** Verified the author's S8 push at
  `b722b22607ce3d051a84aaa08f00f073e9a99cc2`. In response to the request for
  desirable calculus attributes, the [theorem agenda](v2/literature/01i_calculus_desiderata_and_theorem_agenda.md)
  distinguishes operational composition, contextual characterization, adequate
  information, faithful fragment interfaces and effective certificates. It
  ranks theorem targets without choosing a core or treating them as proved.
  Three targeted primary sources address contextual distance, variational
  preferences and local abstraction repair; the source register now has 21
  entries (8 core, 13 supplements). Fourteen new checks and 236 combined F03
  tests pass. Credited L is 4.804352 minutes; cumulative L is 51.058238, leaving
  8.941762 of L60. See [S9](v2/work_logs/F03_2026-09-24_S9.md). F03 remains partial and
  selected; F04 and all gates remain unattempted. Delivery is an incremental
  local package, not a pushed commit or an amendment selecting the calculus.

  **Completed — September 24, 2026, S10 (UTC September 25).** The
  [phase-one comparison](v2/literature/01j_phase_one_literature_and_novelty.md)
  maps value-as-primitive, licensing, open-ended succession, composition,
  revision and learning to primary literature. It distinguishes standard
  ingredients, concrete integration results, and unproved novelty opportunities.
  Seven targeted comparisons extend the eight-core-source audit to 28 total
  sources; their exact statements and import limits are recorded. Twenty new
  checks bring F03 discovery to 256 passing tests. The source-review minimum is
  met: **60.216954 cumulative L minutes**, including **9.158716** in S10.
  [The completion record](v2/work_logs/F03_2026-09-24_S10.md) retains both runtime logs,
  the excluded interrupted interval, forecasts, evidence and validation limits.
  F03 is complete; **F04 is selected but not started**. No core or gate is chosen.
  The source use register is not a proof engine or a proof of global novelty.

- [ ] **F04 — hostile examples and candidate discrimination.**

  Principal artifact: `v2/derivations/01_candidate_countermodels.md`.
  Try to break the candidates using dependence, composition, rescaling,
  unit/context changes, evidence updates, and information compression. Prove
  the hand-checkable cases. Use finite code probes when high-value, preserving
  the distinction between D and E. Add durable regression fixtures and a
  comparison matrix that records failures as well as positive capabilities.

  **DIR01 scope:** include (i) improvement of a proxy loss without improvement
  of the intended criterion, (ii) a versioned self-evaluator with uncertainty,
  including a feedback-dependent hostile case, and (iii) a hypothesis about
  value/loss computation in an ordinary ReLU MLP. For (iii), specify a causal
  discrimination test and a function-preserving reparameterization control;
  do not train the final challenge here. Compare at least one RLL-like route
  with an alternative and identify the smallest viable reflective fragment.
  Select one high-value opportunity; do not require every candidate to support
  all ambitious extensions immediately.

  **Done when:** at least two tempting but invalid inferences have explicit
  witnesses or scoped explanations; viable candidates have discriminating
  evidence, not just scores; D60 is recorded.

  **Partial first pass — September 25, 2026.** The
  [candidate countermodels](v2/derivations/01_candidate_countermodels.md) give a
  calibrated-proxy ranking reversal; an exact criterion for bounded comparisons
  despite unrestricted shared nuisance values; a versioned uncertain self-bound
  whose report changes its own policy; and rescaling/intervention controls for
  neural interpretations. The [neural design](v2/experiments/F04_neural_probe_design.md)
  is unexecuted, not a frozen F14/F15 challenge. The S/P/T/G comparison retains
  two viable routes without selecting one. All **29 new F04 checks**, **256 F03
  checks** and **124 F02 checks** pass in the source overlay.
  [S1](v2/work_logs/F04_2026-09-25_S1.md) records **4.065999 measured D minutes**;
  **55.934001 minutes of D60 remain**. F04 remains unchecked and selected.
  Next: reconstruct the cases, challenge nonlinear/source-elimination boundaries
  and check comparable information across candidates. No Gate A or F05 work.

  **Partial continuation — September 26, 2026.** The
  [nonlinear/reflective reconstruction](v2/derivations/01a_nonlinear_and_reflective_reconstruction.md)
  gives an exact finite-ReLU uncontrolled-direction criterion, a sharp uniformly
  improving nonlinear comparison, correlated two-branch self-report feasibility,
  and a finite optimizer with a paired deterioration budget. Counterexamples
  distinguish tighter robust scores from true-model expected-cost improvement,
  and observational cost recoding from interchange predictions. No neural training.
  **38 new / 67 combined F04 checks**, **256 F03** and **124 F02** regressions pass.
  [S2](v2/work_logs/F04_2026-09-26_S2.md) credits 3.526176 D minutes; cumulative
  **7.592175 D minutes**, with **52.407825** of D60 remaining. F04 stays selected;
  the shortlist, Gate A and F05 have not been advanced.

  **Partial S3 continuation — September 26, 2026.** The
  [compressed revision derivation](v2/derivations/01b_compressed_revision_certificates.md) proves an exact three-scalar
  check interface for the fixed two-branch model, its failure under certain
  future evidence/weight changes, and selective directional-certificate repair.
  Finite linear proofs connect common-source comparisons, uncertain self-reports,
  proxy-error bounds and reparameterization-aware neural intervention controls.
  No neural training or general proof search. **27 new / 94 combined F04 tests**,
  **256 F03** and **124 F02** regressions pass in the reconstructed overlay.
  [S3](v2/work_logs/F04_2026-09-26_S3.md) records **10.166645 D minutes** this session,
  **17.758820 cumulative D minutes**, and **42.241180 remaining** against D60.
  This meets the requested ten-minute session aim without reclassifying code,
  retrieval or packaging as derivation. F04 remains selected; no Gate A or F05.


  **Partial S4 continuation — September 26, 2026.** The
  [certificate-portfolio derivation](v2/derivations/01c_certificate_portfolios.md)
  distinguishes sparse proofs, coefficient precision, reusable proof families and
  uncertain evidence modes. It gives finite-library and factored-circuit bounds,
  a same-policy case-versus-uniform-proof separation, and a structural
  characterization of certificate-valued ReLU functions. A zero-mask counterexample
  is retained with a coherent one-sided reconstruction. No neural training.
  **34 new / 128 F04 checks**, **256 F03** and **124 F02** regressions pass.
  [S4](v2/work_logs/F04_2026-09-26_S4.md) records **15.692405 measured D minutes**, meeting
  the requested 15-minute session floor. Cumulative F04 D is **33.451225 minutes**,
  leaving **26.548775** against D60. F04 remains selected; no Gate A or F05.

- [ ] **Gate A — foundation-selection readiness.**

  Record `v2/checkpoints/A_1.md` (increase the attempt suffix on retries).
  Require explicit operational questions, at least six worked separating
  examples, two genuinely distinct viable candidate formulations or a proved
  reason to eliminate one, and checked literature relevant to the shortlist.
  Audit clocks and the allocation to both research lanes. Identify which
  assumptions would most threaten the preferred candidate.

  **DIR01 check:** state how the shortlist connects loss proxies to value,
  supports a scoped self-assessment question, and permits a test of naturally
  learned neural structure. Compare the leading opportunity with its closest
  antecedent. Do not pass by permanently deferring these aims without a named
  scoped alternative and an explicit direction decision.

  **PASS:** a justified shortlist and one bounded next development question;
  no need to pretend the final calculus is fixed. Select F05.
  **BLOCKED:** return to F01-F04 through a named repair, not to more polished
  prose or an unsupported carrier choice.

### Cycle II — operational semantics, rules, and metatheory

- [ ] **F05 — choose a provisional core and give operational semantics.**

  Principal artifact: `v2/foundations/03_provisional_core.md`.
  Choose a candidate from Gate A, retain an explicit alternative, and define
  syntax, types/contexts, semantic objects, evaluations, and the consequence
  relation. Explain what an inference licenses the consumer to conclude and
  what constitutes a countermodel. Give a nonempty model/interpretation and
  show the assumptions are jointly satisfiable in the chosen fragment.

  Include the selected loss/proxy semantics and a typed, bounded self-assessment
  interpretation. State where confidence, provenance and metalogical premises
  live; do not conflate a self-prediction with proof of its correctness.

  **Done when:** notation and project spec match; at least three examples have
  complete interpretations; the choice and rejection conditions are explicit;
  D60 is recorded. Existing phase-one objects are imported only by argument.

- [ ] **F06 — develop the first nontrivial inference rules.**

  Principal artifact: `v2/derivations/02_inference_rules.md`.
  Derive a small rule set from the declared semantics. Investigate context
  change, dominance/substitution, composition, resource or error accounting,
  and justified weakening as applicable. Do not add a rule merely to resemble
  classical syntax. Show at least three multistep worked derivations, including
  a composition whose conclusion was not supplied as a premise or directly
  looked up as a final score.

  **Done when:** rules have exact premises, conclusions, and side conditions;
  operational meaning is visible; invalid generalizations have witnesses;
  D90 is recorded.

- [ ] **F07 — prove soundness for an explicit fragment.**

  Principal artifact: `v2/derivations/03_soundness.md`.
  State the fragment and semantic preservation property precisely. Prove each
  rule sound and then the derivation-level theorem, including assumptions
  about contexts, composition, and numeric domains. Work through at least one
  nontrivial example independently of the syntactic proof. Do not define
  semantic validity as derivability and call the resulting identity soundness.

  **Done when:** there is a complete checkable proof, its assumptions have a
  model, known counterexamples are excluded for stated reasons, and D90 is
  recorded. A partial proof remains partial and triggers the repair procedure.

- [ ] **F08 — pursue a harder characterization result.**

  Principal artifact: `v2/derivations/04_characterization.md`.
  Protect exploratory time for a completeness, representation, or information-
  preservation result for the chosen fragment. Start with an exact conjecture
  and an explicit failure test. A genuine obstruction may motivate a restricted
  completeness/representation theorem or a characterization of missing
  structure. A tautological quotient or lossless serialization by itself does
  not establish a useful calculus.

  Use the opportunity register to prioritize a scoped proxy-to-task regret
  relationship, contextual substitutability/representation result, or warranted
  self-assessment result. A known surrogate bound or the ReLU/residual identity
  alone is a baseline, not the new characterization contribution.

  **Done when:** a nontrivial theorem is proved, or an obstruction plus a
  constructive restricted result is established and the specification is
  narrowed accordingly; D90 is recorded. Budget expiry alone does not complete
  this task. Preserve rigorous partial gains while scheduling the next attempt.

- [ ] **F09 — Boolean, phase-one, and scaling comparisons.**

  Principal artifact: `v2/derivations/05_fragments_and_comparisons.md`.
  Establish precisely which Boolean fragment, if any, is recovered; distinguish
  interpretation from a superficial numerical resemblance. Relate the old
  license calculus to the candidate by embedding, abstraction, or explicit
  obstruction. Analyze affine/monotone transformations and bounded/unbounded
  domains for the operations actually adopted. Do not insist on a full
  phase-one embedding when it would distort the candidate.

  **Done when:** at least one exact fragment relationship and one failed
  overgeneralization are proved; remaining incompatibilities are explicit;
  D60 is recorded.

- [ ] **F10 — external theorem and contribution audit.**

  Principal artifact: `v2/literature/02_core_audit.md`.
  Recheck the now-specific theorem claims against primary sources, including
  their assumption strength. Identify what is imported, adapted, independently
  derived, or plausibly new. Look for a simpler known formulation and record
  whether it replaces the candidate. Focus on roughly 4-6 load-bearing checks,
  rather than treating source count as success.

  **Done when:** the claims and contribution boundary reflect the checked
  literature; any misapplication has a repair; L45 is recorded.

- [ ] **Gate B — mathematical core readiness.**

  Record `v2/checkpoints/B_1.md`, with versioned retries.
  Require nonempty operational semantics; three meaningful multistep
  derivations including composition; a soundness proof; the nontrivial result
  or constructive restricted alternative from F08; exact fragment comparisons;
  and an honest literature-based contribution statement. Include a nonempty
  bounded self-assessment example with explicit uncertainty and update rules;
  preserve scope distinctions from full proof reflection. Attempt a fresh
  reconstruction of the load-bearing proof steps. Label self-review honestly
  when another reviewer/agent is unavailable.

  **PASS:** every downstream premise has checked support and no blocking gap;
  select F11. **BLOCKED:** repair F02/F05-F10 as indicated by evidence, and
  invalidate dependent claims. A stack of passing numerical examples cannot
  substitute for the soundness obligation.

### Cycle III — executable reasoning and adversarial evaluation

- [ ] **F11 — implement a minimal reasoner and semantic reference.**

  Principal artifact: `v2/verification/` with a documented entry point.
  Implement the declared fragment, inference steps, proof traces, and a small
  semantic evaluator/reference check. Keep the rule engine and reference
  evaluation sufficiently distinct to catch discrepancies. Avoid unnecessary
  neural architectures, infrastructure, or global optimization systems.

  **Done when:** `python -m v2.verification` exists and runs deterministic
  fixtures; both implementations match the notation; E60 is recorded. Update
  the validation section of `v2/README.md`.

- [ ] **F12 — differential tests and counterexample regression.**

  Principal artifact: `v2/verification/` test suite and test-design note.
  Translate the earlier positive and negative witnesses into tests. Generate
  bounded cases for semantic-versus-syntactic comparison; declare exhaustivity
  bounds and random seeds. Check invalid compositions, units/context changes,
  boundaries, and the exact transformation laws proved in F09. Do not share a
  bug-prone output decoder between an implementation and its supposed oracle.

  **Done when:** known bad rules fail the suite, good fixtures pass, uncovered
  assumptions are logged, and E45 is recorded. General theorems remain proof-
  supported rather than inferred from test counts.

- [ ] **F13 — work two motivating case studies end to end.**

  Principal artifact: `v2/derivations/06_case_studies.md`.
  Use one small scientific approximation/loss/resource example and one bounded
  self-assessment example, which may use a toy axiomatic or proof-checking
  system. The latter must concern the evaluator's own versioned behavior and
  influence later reasoning while admitting unresolved outcomes. For each,
  state the operational task, assumptions, value
  objects, premises, intermediate inferences, comparison baseline, and result.
  Compute a composite conclusion not handed to the reasoner as an input score.
  A more detailed numerical reference is still a declared model, not final
  truth. In the reflective/axiomatic example, distinguish theoremhood inside
  a system from the pragmatic decision to rely on it. A staged fragment is
  acceptable; document what a genuinely cyclic extension would still require.

  **Done when:** the examples explain why the calculus's structure is needed,
  show its limits, and are executable where appropriate; D60 is recorded.

- [ ] **F14 — freeze the empirical challenge and baselines.**

  Principal artifact: `v2/experiments/protocol.md` plus frozen configuration.
  Separate development fixtures from a prospective evaluation population.
  Freeze task generator, constraints, baseline(s), held-out seeds/cases,
  inference-correctness checks, useful-derivation criterion, resource measures,
  and interpretation of failures before final execution. Prefer a transparent
  scalar-summary baseline and a direct semantic reference over an elaborate
  weak competitor. Exact numeric performance thresholds must be justified
  prospectively, not selected after results.

  **Done when:** F15 can execute without inventing its success criteria; any
  already-seen cases are labeled development rather than held out.

  **DIR01 neural probe:** freeze a small ordinary-training ReLU MLP comparison,
  a hypothesized internal loss/value computation, relevant interventions and
  reparameterization controls. No loss term or architecture may secretly force
  the proposed logical structure in the unconstrained baseline. A deliberately
  compiled or constrained network is a separately labeled positive control.
  Select one feasible probe, not a second large research program; prospectively
  revise effort allocations if needed and preserve the existing time floors.

- [ ] **F15 — run and interpret the frozen challenge.**

  Principal artifact: `v2/experiments/results.md`, with code/configuration and
  machine-readable outputs. Run F14 unchanged and report correct derivations,
  failures, retained information, and measured resources. Report negative and
  null comparisons, not only attractive examples. Distinguish an invalid rule,
  an implementation bug, and lack of performance advantage.

  **Done when:** results are reproducible and claim dispositions are recorded;
  E60 is recorded. A failed challenge can complete this reporting task but may
  block Gate C and require a new, explicitly versioned repair/evaluation cycle.
  Do not repeatedly tune against an allegedly untouched test set.

- [ ] **F16 — fresh adversarial reconstruction.**

  Principal artifact: `v2/derivations/07_adversarial_review.md`.
  Reconstruct the load-bearing definitions and proof steps, preferably with a
  separate reviewer/agent, otherwise a labeled fresh self-review. Search for
  circular definitions, vacuity, hidden truth/utility assumptions, lost joint
  information, bad composition, and disagreement between proof and code.
  Protect the review block even when preliminary checks look favorable.

  **Done when:** objections have exact dispositions or named repairs;
  independent-review claims accurately describe the process; a fresh D60 is
  recorded, not borrowed from the original proof task.

- [ ] **Gate C — evidence of a sufficiently solid and useful calculus.**

  Record `v2/checkpoints/C_1.md`, with versioned retries.
  Require a non-stale Gate B; no unresolved flaw in the sound core; successful
  differential/regression checks; worked scientific and self-assessment examples;
  transparent frozen results, including the bounded neural-interpretation
  probe; and resolved dispositions from F16. A negative probe may complete the
  investigation but must not be reported as successful causal interpretation.
  Require
  evidence of genuine compositional inference, not only score thresholding.
  Apply F14's prospective useful-derivation criterion. A speed advantage is
  required only if the specification actually promised one; a null benchmark
  must narrow that claim rather than be concealed.

  **PASS:** sufficient scoped evidence to assemble the report; select F17.
  **BLOCKED:** classify the failure and return to the relevant derivation,
  implementation, or evaluation task. If the core changes, reopen Gate B;
  if the final challenge changes, version and freeze a new protocol before
  execution. A polished report cannot repair an unmet research criterion.

### Cycle IV — consolidation, not automatic publication

- [ ] **F17 — assemble the research report.**

  Principal artifact: `paper_v2.md`.
  Present the question, candidate-selection evidence, chosen semantics, rules,
  worked derivations, theorem statements/proofs, relation to Boolean and
  phase-one reasoning, literature, implementation, empirical findings, and
  remaining questions. Link detailed derivation notes rather than replacing
  them with polished summaries. Explain which claims are mathematical,
  empirical, design choices, or philosophical motivation.

  **Done when:** all claims trace to current evidence, no stronger result is
  introduced during writing, and unresolved directions become later research
  rather than falsely completed contributions.

- [ ] **Gate D — final audit and phase disposition.**

  Record `v2/checkpoints/D_1.md`, with versioned retries.
  Check the report against non-stale Gates A-C, the claim ledger, exact
  implementation/configuration versions, citations, clock/minimum records,
  and actual validation outputs. Audit whether the difficult lane received
  real time and whether easier gains were retained. Confirm that all
  required artifacts exist and active blocking repairs are closed.

  **PASS:** mark this scoped phase complete and set the pointer to external
  review/publication or the next author-selected phase. **BLOCKED:** create
  a targeted repair and do not call the phase complete. No fixed number of
  later phases is implied by this disposition.

## Definition of done

This phase succeeds when it has a justified, explicit value-based semantic
core; operationally meaningful inference rules; nonvacuous worked derivations;
a checkable soundness theorem and a further nontrivial characterization or
constructive restricted result; honest fragment/literature comparisons; a
small executable reasoner; and evidence meeting the frozen usefulness question.
All protected task minima must be actually recorded, not inferred from output
length. Gates A-D must be current and passed, with no hidden blocking repair.

A useful partial theory, a refuted candidate, or a suspension can be a valuable
research outcome without satisfying this definition. Record that status
accurately and retain the evidence for the next cycle or phase.

## Deferred follow-up branches

Contract semantics and inverse task recovery, large-scale model substitution,
general reflective agents, large-network interpretability, and broad physical-
theory hierarchies remain possible later phases. DIR01 explicitly promotes a
bounded self-assessment capability and a small ordinary-network probe into the
current phase. Wider versions still require an explicit roadmap decision rather
than unnoticed scope expansion. There is no fixed lifetime limit on phases.
