# Task 20 experiment implementation

> **Execution note (2026-07-16):** the scientific v1 implementation below remains frozen, but its high-volume custom-object evaluator failed during Task 21. The versioned execution-only repair, its safeguards, and layperson usage instructions are documented in [`03_execution_repair.md`](03_execution_repair.md). No v1.1 production or final-confirmation data was generated during that repair task.

Status: **implemented and frozen on 2026-07-14 without materializing any
train, calibration, validation, system-audit, or final-confirmation world.**
The machine-readable contract is
[`implementation_v1.json`](implementation_v1.json). The only neural execution
performed during this task was the 16-world pilot-role smoke test recorded in
[`implementation_smoke_v1.json`](implementation_smoke_v1.json). It is an
implementation check, not evidence for `F35` or `F36`.

## 1. Executable boundary

The implementation is split so that the learned module cannot import the
generator or oracle:

- [`learner.py`](learner.py) contains only numeric panel types, matched ReLU
  models, capacity arithmetic, paired initialization, fitting, prediction,
  and joint internal-selection logic;
- [`implementation.py`](implementation.py) is the audited adapter from frozen
  generator records to the closed feature vector and from learned proposals
  back to exact symbolic semantics;
- [`system_witness.py`](system_witness.py) implements only the deterministic
  certificate/system witness; and
- [`run_experiment.py`](run_experiment.py) is the sole preflight, smoke, and
  eventual Task 21 entry point.

The frozen learning runtime is Python 3.13.3, NumPy 2.2.5, and CPU PyTorch
2.8.0. The v1.1 contract did not record the Matplotlib version used to render
the already frozen figures. Checkpoint D prospectively pins Matplotlib 3.10.8
for analysis imports and clean-checkout verification. All three packages are
listed in [`requirements.txt`](requirements.txt); this later analysis-only pin
changes no frozen learner, result, or existing figure artifact.

Both learned arms receive the same ordered 25-coordinate pre-outcome vector.
It includes context, declared threshold/fallback inputs, exact pre-outcome
evidence usability and polarity, plan/schema/mode indicators, and the frozen
evidence-width design variable. Every source field passes the closed Task 19A
firewall before encoding. The vector excludes sampled targets, oracle means or
regions, state/outcome labels, active masks, routes, latent lineage, future
events, and audit/confirmation results. Training targets are passed to the
numeric fitter separately; no oracle record type is imported into that module.

The registered scales are `.1` for loss `J` and `10 ms` for latency `T`.
Target-distribution weights multiply the atom-stratum and context-cell
target/design ratios. This multiplication is important: using only the
stratum ratio would silently leave the deliberately oversampled gap at its
design mass.

## 2. Matched learned arms

The structured arm is a two-hidden-layer ReLU MLP with one affine vector head
ordered

```text
(center_J, raw_radius_J, center_T, raw_radius_T).
```

The two radius coordinates pass through ReLU; this is one four-coordinate
learned head, not separate learned heads for support and refutation. The
support/refutation margins, paired ReLUs, exact state, and evidence channels
are later deterministic channels. The CE baseline uses the same conditioned
input and two-hidden-layer family but emits three logits for the current atom
row. It predicts one `K_3` state directly.

The smallest equal hidden widths meeting each common parameter budget are:

| budget | structured width / parameters | CE width / parameters | mismatch |
|---:|---:|---:|---:|
| 12,000 | 96 / 12,196 | 96 / 12,099 | 0.80% |
| 20,000 | 127 / 20,070 | 128 / 20,227 | 0.78% |

Both are inside the frozen 2% tolerance. For each paired fit seed, the arms
draw a common parent trunk and slice their declared widths. At the 20k budget,
the 127-wide structured trunk is the exact initialized prefix of the 128-wide
CE trunk. The head streams are isolated by arm, so changing head shape does
not perturb the shared initialization prefix.

The center phase updates the trunk and center rows. The radius phase freezes
the trunk and restores the two center rows after every AdamW step, including
against decoupled weight decay. Missing statistic targets are masked rather
than replaced by zero. Both phases and CE use schema-balanced,
target-reweighted losses.

## 3. Prospective implementation clarifications

The frozen protocol fixed the total epochs, grid, patience, batch size, and
capacity rule but left several algorithms underspecified. No production role
had been materialized, so Task 20 freezes the following choices before any
confirmatory observation:

1. The structured 200-epoch maximum is divided into at most 100 center epochs
   and 100 radius epochs. Validation occurs every five epochs; patience is
   still 20 epochs.
2. A training minibatch is 512 independent worlds. Each epoch selects one `J`
   and one `T` probe per world through a deterministic cycle covering all 80
   positions. This avoids calling correlated atom rows independent worlds
   while giving both schemas the same update count.
3. The 18 grid points are fit once per arm with seed 101. The common final
   budget minimizes the sum of the arms' relative regrets from their own best
   internal-selection losses; learning rate and weight decay are selected
   separately within that shared budget. The selected configurations are then
   refit at all eight paired seeds.
4. Calibration uses one eligible probe per schema per calibration world. A
   target-blind hash selects it proportional to the registered joint
   target/design weight. Thus each schema has 5,000 independent calibration
   scores. Pooling 200,000 correlated atom rows would have overstated the
   conformal sample size.
5. The boundary endpoint receives an explicit four-query panel at normalized
   distances `+.25`, equality, crossing midpoint, and `-.25`. The ordinary
   continuously sampled strict strata have probability zero of landing
   exactly at the registered `.25` boundary cutoff.
6. A tolerance-transfer case shifts the original declared threshold by
   `d sigma`, for `d` in `{-2,-1.5,1.5,2}`. Smaller-is-better upper-bound
   semantics make eight cells structurally impossible: a negative threshold
   shift cannot create Supported when the corresponding positive direction is
   required, and a positive shift cannot create Refuted in the opposite
   direction. The primary macro therefore averages the 16 realized
   schema/state/offset cells. This makes the monotonic support explicit and
   changes no effect margin, null, world count, or learned input.

The last two points are not favorable-result edits. They repair endpoint
execution before either learner has seen a production world. The public paper
should state the monotonic structural zeros instead of suggesting a full
24-cell Cartesian design that cannot exist.

## 4. Calibration, binding, and exact states

Each fitted structured model gets two separate calibration bundles: learned
radius plus expansion, and center-only plus its own expansion. A bundle binds
the scorer hash, training/calibration manifests, schema, normalization,
finite-quantile rule, calibration ID, scope, polarity, stages, checker, and
provenance. Missing fields, hash/group/scope mismatch, wrong polarity,
expiration, checker rejection, reversed/nonfinite endpoints, too few
calibration worlds, and infinity all fail usable binding.

Infinity remains in the coverage estimand as an interval containing any finite
target, but it cannot support or refute an atom. This keeps marginal proposal
coverage separate from usable logical evidence.

After either learned arm predicts, the same exact path handles:

```text
WF; evidence presence/validity/currency/checker; polarity;
inclusive support; strict refutation; indexed K3 diagnostics;
profile meet; four public outcomes; active mask; route/fallback.
```

CE logits cannot override missing, invalid, or polarity-blocked evidence.
Every request retains separate diagnostics indexed by `A`, `I`, and `C`.
`Undefined` is derived from failed `WF`, never learned as a fourth atom class.
Simultaneous grants remain simultaneous members of the active set, and an
empty set routes to `F`. Router scores are consulted only after exact masking;
the production inactive-selection probability is identically zero.

## 5. ReLU sign semantics and ablations

The exact `F18` witness is run by every preflight. It reproduces:

```text
strict atom surpluses       (2,12,3)
full fixed-profile grant    1
supported equality surplus 0
crossing-open ReLU pair     (0,0)
bias/bypass output          7
inactive high-score route   O, not the inactive candidate
empty active-set route      F.
```

Accordingly, positive ReLU output means only positive preactivation unless a
particular margin semantics has been externally fixed. Predicted positive
slack may be wrong. Positive surplus from an accepted region is evidence about
one atom, not a whole license. Zero has no unique logical meaning: supported
equality, an open crossing, missing/invalid evidence, and inactive numerical
channels can all have zero.

All required ablations are executable:

- center-only uses zero learned radius and its own accepted held-out expansion;
- unaccepted learned radius is always `Open` in production, with its direct
  decoding reported only as a labeled shadow fit comparison; and
- self-confidence-as-grant is deliberately invalid and carries
  `production_active=false`, regardless of confidence or apparent fidelity.

The full runner records these states on in-regime, boundary, transfer, and
request panels. Good prediction cannot turn either invalid ablation into
evidence.

## 6. Traces and deterministic system witness

Full JSON traces are available for focused narrative cases. The powered run
uses a compact replayable format: 100-world, per-fit-seed compressed NPZ
shards plus the frozen trace schema and implicit role manifest. Row order and
the frozen generator recover all lineage and request identities. The shards
store raw centers/radii and logits; exact/reflexive/ablation states; signed
margins and paired ReLUs; reference states joined only after prediction;
request outcomes; active masks; and routes. The fit marker binds model and
calibration hashes before the final generator is called.

The system extension remains a deterministic integration witness. A
`LearnedGradeEnvelope` carries a typed payload and proposed error grade but is
not an `EvidenceRecord`. A lower-ranked, independently checked audit record
must match its scorer and calibration identities before the adapter can
construct local evidence. The existing finite-DAG transformer then propagates
the checked grade/resources, constructs a composite proof term, and erases to
the ordinary payload computation. Regressions verify:

- learned self-assertion and wrong-role audit rejection;
- valid external adapter and composite-certificate acceptance;
- proof erasure and independent proof checking;
- invalid local-certificate and cycle rejection;
- provenance reaching empirical and formal bases;
- ranks `system audit < checked adapter < final confirmation`; and
- audit/confirmation lineage separation.

This is no empirical system-adequacy result and has no powered comparison.

## 7. Entry point, smoke result, and embargo

The single entry point is:

```text
python -m experiments.run_experiment --preflight
python -m experiments.run_experiment --smoke
python -m experiments.run_experiment --task21-final RUN-VALUE-LOGIC-FINAL-V1
```

Only Task 21 may invoke the last command. It refuses source/config hash drift,
the wrong authorization token, or any existing fit/model/result artifact. Its
order is fixed: verify hashes; materialize train; perform 18 matched trials;
select one common budget; fit eight paired models; materialize calibration;
freeze two calibrators per structured model; serialize models and a hashed fit
marker; only then materialize confirmation worlds. Final outputs cannot affect
fitting, calibration, stopping, routing, or rerun decisions.

No learned reject or learned router threshold is in the minimum core, so the
validation role is not materialized by the frozen run. Routing is the fixed
exact-mask selector. Likewise, the deterministic system witness consumes no
system-audit payload. Their manifests remain blocked and unused rather than
being spent on unpowered optional results. Hard MoE remains prospectively
omitted.

The Task 20 smoke path used 12 pilot worlds for fitting and four for internal
selection, four epochs, and seed 101. Both arms completed, the parameter
counts matched, and an exact repeated structured fit produced identical model
and prediction hashes. The losses are retained in the JSON only as runtime
sanity values. Sixteen worlds and four epochs cannot support, falsify, or
adjudicate `F35`, `F36`, calibration, or architecture preference.

## 8. Task 20 disposition

Task 20 passes its implementation gates:

- matched structured and CE ReLU learners, paired initialization, selection,
  all required ablations, and separate calibration are executable;
- the firewall and learner/oracle import boundary are explicit and tested;
- proposal binding, exact `WF + K_3`, indexed diagnostics, masks,
  simultaneous/empty active sets, routing/fallback, signed/rectified margins,
  and `F18` are executable;
- trace construction freezes predictions before the evaluation join;
- the deterministic system/certificate tier respects grade/evidence and rank
  boundaries;
- hard MoE is absent; and
- preflight and pilot-only smoke pass while every production payload and the
  final embargo remain untouched.

Task 21 must run the frozen command once, report runtime or infrastructure
failure before reading result metrics, and create the registered result
artifacts. Until then, `F35` and `F36` remain untested.
