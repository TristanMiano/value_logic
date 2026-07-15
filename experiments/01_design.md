# Preregistration: the decisive value-logic experiment

Status: **Task 19 prose preregistration and Task 19A generator-only pilot are
complete.** The versioned machine-readable protocol is
[`protocol_v1.json`](protocol_v1.json). No learner or production-role world was
materialized, and final confirmation remains embargoed. Task 19A made two
prospective amendments before production generation: paired-difference
certificates now carry the later-dominance claim, and conservative
design-alternative variance bounds replace an impossible pre-learner estimate
of learned-arm paired variance. Any later substantive change requires a dated
versioned amendment.

This document preregisters one minimum publishable comparison and separates two
optional extensions. It is a design for a synthetic semantics experiment, not
an empirical model of physics. Its Newtonian-like fixture is a narrative aid:
an older local plan, a broader successor, and a later specialist can overlap,
remain useful, lapse, be rebutted, leave a gap, or be dominated in a declared
finite library.

## 1. Questions, claims, and evidential grades

The minimum core asks two questions.

1. At matched inputs and exact output semantics, does structured
   center--radius statistic learning with accepted held-out expansion improve
   tolerance-transfer and boundary-state fidelity over direct independent
   `K_3` cross-entropy? This is `F35/H18.1`.
2. Does the checker-accepted held-out expansion procedure attain its registered
   marginal target-in-proposal coverage in each declared exchangeable
   statistic group? This is `F36/H18.2`.

The experiment can answer those questions only for the frozen synthetic
distribution and implementation family. It cannot show that a plan is true,
that conformal marginal coverage is conditional or selected coverage, that a
class probability is calibrated, or that an entire deployed system is
adequate. The exact logic, the deterministic `F18` sign witness, and the
empirical comparisons retain different evidential grades.

The minimum core contains no architecture-level comparator. A hard
mixture-of-experts (MoE) seam study and a certificate-carrying system study are
optional, separately gated extensions in Sections 16--17. Activation alignment
is exploratory only.

## 2. Independent synthetic succession generator

### 2.1 Independent unit and lineage blocking

The statistical unit is a generated world/trajectory root `w`. Each root owns
all of its stages, candidates, atom probes, request profiles, observations, and
provenance descendants. Rows within a root are clustered observations. Model
initialization seeds are repeated fits, not additional worlds.

Every root also has a unique latent plan-family lineage. The displayed names
`O`, `S`, `N`, and `F` below are reusable *roles* (old, successor, later
specialist, fallback), not shared plan-family identifiers. No world root,
trajectory root, provenance ancestor, or latent plan-family identifier may
appear in more than one evidential role. The roles share only this frozen
generator law.

Each request trajectory within a world contains a context coordinate
`x in [-1,1]`, a declared complexity coordinate `c in [0,1]`, and a
pre-outcome difficulty coordinate `h in [0,1]`. The target law is uniform in
`x`, `c`, and `h`. The design stratifies `x` to expose overlap and gaps while
sampling `c,h ~ Uniform[0,1]` independently:

| stage-0 context cell | target mass | design mass |
|---|---:|---:|
| `O` only, `[-1,-.35)` | .325 | .20 |
| `O/S` overlap, `[-.35,.35]` | .35 | .30 |
| `S` only, `(.35,.85]` | .25 | .25 |
| gap, `(.85,1]` | .075 | .25 |

Within a cell, `x` is uniform. The fixed 40-trajectory panel therefore assigns
8, 12, 10, and 10 trajectories to these cells and uses the exact
target/design ratio for target-law metrics. Cell, public-outcome, focal-atom,
and update schedules are combined by a seeded balanced permutation so no one
factor deterministically identifies another. The core plan scopes are

```text
O: [-1.00, 0.35]       older, locally useful plan
S: [-0.35, 0.85]       broader successor
N: [ 0.15, 1.00]       later specialist, absent before stage 3
F: [-1.00, 1.00]       outside option/fallback
```

Thus `O` and `S` overlap, `S` and the later `N` overlap, and before stage 3 the
interval `(0.85,1]` is an intentional gap. Domains are declared before learned
outputs and are never defined from a fitted network's preferred regions.

### 2.2 Frozen latent laws

The core uses continuous piecewise-linear conditional means. With
`R(u)=max(0,u)`, the smaller-is-better task loss means are

```text
mu_J(F) = .32 + .05 c + .02 |x|
mu_J(O) = .10 + .03 c + .04 |x+.55| + .22 R(x-.20) + b_J(O)
mu_J(S) = .12 + .05 c + .035|x|     + .08 R(x-.75) + b_J(S)
mu_J(N) = .09 + .04 c + .025|x-.55| + .06 R(.10-x) + b_J(N)
```

and latency means in milliseconds are

```text
mu_T(O) = 35 + 8 c + 5|x+.50| + b_T(O)
mu_T(S) = 42 + 6 c + 4|x|     + b_T(S)
mu_T(N) = 38 + 7 c + 3|x-.50| + b_T(N).
```

At world creation, the hidden intercepts are sampled independently as
`b_J(e) ~ Normal(0,.006^2)` and `b_T(e) ~ Normal(0,.8^2)`. They are known to the
oracle but are not scorer inputs. Conditional outcome scales are

```text
sigma_J = .006 + .006 h + .002 c
sigma_T = .60  + 1.00 h + .40 c.
```

For each required target instance, the oracle samples

```text
t_J = mu_J(e) + sigma_J xi_J,
t_T = mu_T(e) + sigma_T xi_T,
xi_J,xi_T independently ~ Normal(0,1).
```

The authoritative reference region is the exact central 90% conditional
region

```text
U_J* = [mu_J(e)-k sigma_J, mu_J(e)+k sigma_J]
U_T* = [mu_T(e)-k sigma_T, mu_T(e)+k sigma_T]
k = 1.6448536269514722.
```

The sampled targets train and test the statistic learners. `U*`, not a learned
arm, supplies reference atom labels. The generator retains exact unrounded
values; displayed decimals are not computational tolerances. Task 19A must
test the formulas and distributions directly rather than re-estimate them from
pilot outcomes.

The generator may use an independently drawn stratum controller to place a
request threshold relative to `U*`; this is how it creates positive-density
boundary cases. That controller, its oracle endpoints, and its decoded state
are forbidden scorer inputs. Both learned arms see the resulting declared
threshold, as a real request would, but never how the generator selected it.

### 2.3 Evidence mode, polarity, and exact atom strata

For a smaller-is-better atom with threshold `epsilon`, scale `sigma>0`, and
reference interval `U*=[l*,u*]`, the oracle uses

```text
m_support* = epsilon-u*
m_refute*  = l*-epsilon.
```

Subject to exact validity and polarity:

```text
Supported iff can_support and m_support* >= 0
Refuted   iff can_refute  and m_refute*  > 0
Open      otherwise.
```

The stratum constructor chooses one of the following before a target draw is
revealed to a learner:

```text
strict support:   epsilon = u* + d sigma,  d ~ Uniform(.25,1.50)
boundary support: epsilon = u*
crossing/open:    epsilon ~ Uniform(l*+.10(u*-l*), u*-.10(u*-l*))
strict refute:    epsilon = l* - d sigma,  d ~ Uniform(.25,1.50)
missing:          no evidence record; atom is Open
invalid:          rejected/expired/mismatched record; atom is Open
```

Support strata use a two-sided or upper-bound mode; refutation strata use a
two-sided or lower-bound mode. Open strata also include polarity-blocked cases
and empirical-proposal-only records. The checker handles these modes exactly.
Missing and invalid are diagnostics for `Open`, not numerical zero values.

The standalone atom-probe panel contains 40 `J` probes and 40 `T` probes per
world. Within each schema its exact counts are 10, 8, 8, 4, 4, and 6 in the
displayed design-stratum order. Probe strata are paired with context cells by a
seeded balanced permutation. Every reported target-distribution atom metric
uses the fixed importance weight `Q_target/Q_design`; unweighted
design-distribution and stratum-specific metrics are also reported.

| atom stratum | target mass | design mass |
|---|---:|---:|
| strict supported | .40 | .25 |
| boundary supported | .05 | .20 |
| crossing/polarity open | .20 | .20 |
| missing-open | .05 | .10 |
| invalid-open | .05 | .10 |
| refuted | .25 | .15 |

Thus boundary equality has 20% design mass and 5% target mass. This deliberate
oversampling cannot be hidden by reporting only the easier target-weighted
average.

### 2.4 Requests and all four public outcomes

The canonical required profile is

```text
P = A and I and C
A: J(e) <= epsilon_A
I: J(e) <= J(F)-Delta
C: T(e) <= epsilon_C.
```

`A` and `I` reuse one loss statistic region; they are different atoms because
their thresholds and roles differ. The oracle first checks well-formedness and
then aggregates required `K_3` values:

```text
WF=0                                  -> Undefined
WF=1 and at least one required Refuted -> Refused
WF=1, none Refuted, at least one Open  -> Withheld
WF=1 and every required atom Supported -> Granted.
```

Each world emits a fixed 40-trajectory core request panel: 12 constructed
`Granted`, 12 `Withheld`, 12 `Refused`, and 4 `Undefined` requests. Within each
meaningful outcome block, focal atoms rotate evenly through `A`, `I`, and `C`;
open cases rotate through crossing, polarity-blocked, missing, and invalid
diagnostics; refutations rotate through loss and latency. Ordered `A/I`
combinations must respect their shared loss interval. At least 20% of
well-formed requests contain a boundary-equality focal atom. Task 19A must
reject the generator if these exact quotas or the ordered-atom constraints do
not hold.

The declared target request distribution is

| public outcome | target mass | design mass |
|---|---:|---:|
| Granted | .35 | .30 |
| Withheld | .30 | .30 |
| Refused | .30 | .30 |
| Undefined | .05 | .10 |

Query metrics use the fixed target/design ratio. `Undefined` is produced by
wrong units, an unbound plan/domain, or a malformed profile before atom
aggregation. It is never a fourth learned atom class.

### 2.5 Succession trajectory and updates

Every world additionally instantiates this frozen event sequence.

| stage | event | required behavior |
|---|---|---|
| 0 | `O` and `S` are available | overlaps may license both; the extreme interval has no eligible plan and invokes `F` |
| 1 | the current `O` certificate expires | its affected atom becomes Open: a lapse, not evidence of violation |
| 1i | an update writes only outside a chosen request footprint | that request's complete diagnostic and outcome are unchanged |
| 2 | accepted new two-sided `O` evidence lies strictly beyond a threshold | the affected atom is Refuted: a rebuttal, not a lapse |
| 2t | the same accepted region is queried at a changed tolerance | state is recomputed without retraining either arm |
| 3 | `N` and its checked comparisons enter the finite library | `N` fills the earlier gap and can dominate `O/S` on a declared overlap |

Relevant updates are determined by the frozen typed read/write footprint, not
by whether an output happened to change. The irrelevant-update assertion is
exact invariance of the full requested diagnostic. The later dominance claim
is only relative to the displayed finite evaluated set and requires valid
pairwise loss and latency evidence; it is not universal optimality. Old plans
remain in the atlas even when unselected.

## 3. Reusable Newtonian-like narrative fixture

The paper-level fixture reuses Task 16's exact numbers. It is called
Newtonian-like only because an older local method and a newer broader method
can both remain usable; it makes no assertion about real Newtonian,
Lagrangian, Hamiltonian, relativistic, or quantum prediction error.

For one overlap request, set

```text
A: J(e) <= .20
I: J(e) <= J(F)-Delta = .35-.05 = .30
C: T(e) <= 50 ms
sigma_J=.01, sigma_T=1 ms.
```

At stage 0, let

```text
O: U_J=[.14,.18], U_T=[43,47]
S: U_J=[.11,.16], U_T=[45,49].
```

Both plans are `Granted`. For `O`, the normalized support-surplus vector is
`z=(2,12,3)` for `(A,I,C)`. This is simultaneous licensing, not a tie in truth
and not forced simultaneous selection. On the extreme interval, `O` is
refuted or out of scope while `S` remains open/out of scope, so the exact
active set is empty and the fallback is used. A wrong-unit request is
`Undefined`; a missing latency record is `Withheld`.

At stage 1, expiry of `O`'s loss certificate makes its relevant atoms `Open`
and its request `Withheld`: the previous warrant lapsed. An unrelated update
outside another request's footprint leaves that request unchanged. At stage 2,
new valid two-sided evidence `U_J(O)=[.23,.25]` refutes `A`, so the request is
`Refused`: this is a rebuttal. Separately, changing the adequacy tolerance from
`.20` to `.16` leaves `O`'s original `[.14,.18]` open while `S`'s `[.11,.16]`
is supported at equality. No learner is retrained.

At stage 3, let `N` have `U_J=[.08,.12]`, `U_T=[40,44]` on the registered
overlap/high region. Those marginal intervals overlap the displayed `O/S`
intervals and therefore do **not** alone prove strict componentwise dominance.
Task 19A amendment `19A-A1` supplies checked paired-difference certificates

```text
J(N)-J(O) in [-.10,-.02],   T(N)-T(O) in [-7,-.5] ms,
J(N)-J(S) in [-.08,-.005],  T(N)-T(S) in [-8,-.5] ms.
```

Their upper endpoints are strictly negative, so they certify dominance over
the exact displayed finite set while permitting correlated marginal evidence.
`N`'s scope fills the earlier extreme gap. `O` and `S` remain recorded;
dominance changes comparative use, not their historical identity or every
basic reliance judgment.

## 4. Scorer input firewall

The whitelist is closed: a field not listed here is forbidden until a
prospective amendment.

### 4.1 Permitted pre-outcome inputs to both learned arms

- exact typed atom address and its frozen Task 14B dependency projection;
- plan role/template and declared pre-outcome plan features, but not a latent
  family lineage identifier;
- `x`, `c`, `h`, declared scope/domain coordinates, and stage prefix already
  available before the target observation;
- statistic schema, units, normalization identity, evidence-mode request, and
  polarity flags;
- profile slot/role, `epsilon_A`, `Delta`, fallback threshold inputs,
  `epsilon_C`, and other declared request tolerances;
- candidate-library and evaluated-set membership known before outcomes, with
  no target-derived ranking, route, or cell label; and
- evidence-collection design variables such as planned sample size or sensor
  class, but no observed target summary.

Exact `WF`, missingness, validity, expiry, scope, checker, and polarity records
are common nonlearned inputs to the decoder. They may be embedded for ordinary
feature computation only if their exact identities also remain available to
the symbolic path; a learned embedding cannot override them.

### 4.2 Forbidden inputs and proxies

- sampled targets `t_J,t_T`, latent means/intercepts, noise draws, or `U*`;
- oracle endpoints, state/outcome stratum, `K_3` label, public outcome, grant
  bit, active mask, selected route, seam-conformance label, or dominator label;
- accepted learned envelopes from the target case before the arm emits its own
  proposal;
- target-derived certificate region, calibration residual, audit judgment, or
  final-confirmation statistic;
- future stages/events or a hash/identifier from which any forbidden field can
  be recovered; and
- statistics computed jointly across evidential roles.

Task 19A must implement a schema-level firewall and negative tests for direct,
aliased, nested, and hash-based disclosure. A scorer-firewall failure invalidates
the run; it is not repaired by dropping a suspicious metric afterward.

## 5. Immutable proposal/calibration/checker binding

Every usable structured interval is bound to one immutable record containing
at least:

```text
record_id, atom_address, statistic_schema, target_constructor_version,
plan_template, plan_family_scope, candidate_registry_version,
units, normalization_id, scorer_architecture_id, scorer_parameter_hash,
learned_head_factorization_id, training_manifest_hash,
calibration_procedure_id, calibration_manifest_hash,
calibration_group, alpha_cal, finite_quantile_rule, eta_cal_or_infinity,
certificate_mode, can_support, can_refute, domain/scope, validity_window,
checker_id, checker_version, checker_result, provenance_root, created_stage.
```

The checker rejects a missing field, mismatched scorer/calibration pair,
changed normalization, wrong group/scope, expired record, invalid polarity,
nonfinite endpoint, reversed interval, insufficient calibration group, or
unregistered version. Rejection and the infinity sentinel yield `Open`; they
cannot support or refute. No field may be rebound in place. A revised component
creates a new record and provenance node.

## 6. Five blocked evidential roles

| role | allowed use | forbidden use |
|---|---|---|
| train | fit normalizers, trunks, centers, radii, CE logits, and declared auxiliaries | calibration quantiles, router thresholds, system claims, final reporting |
| envelope calibration | compute `eta_cal` for a frozen structured scorer | refit scorer, choose groups after labels, tune router, report final performance |
| reject/router validation | tune conservative reject and post-license selection rules | alter scorer/envelope, construct system evidence, test headline claims |
| system audit | evaluate frozen components and construct lower-ranked system evidence | refit/tune, serve as untouched confirmation |
| final confirmation | one frozen evaluation of all registered core endpoints and eligible extensions | any fitting, threshold choice, rerun choice, or amendment based on its outcomes |

Assignment happens at root creation. A manifest auditor rejects overlap in
world/trajectory root, provenance ancestry, or latent plan-family lineage even
when row IDs differ. Train-derived normalization is versioned and may flow
forward; outcome-bearing records may flow only in the displayed direction.

## 7. Arms, learned heads, and exact semantic channels

### 7.1 Structured reference arm

The reference is a shared ReLU trunk plus **one vector-valued learned statistic
head** emitting

```text
(center_J, proposed_radius_J, center_T, proposed_radius_T)
```

for schemas present in the request. The center is fit first; the radius is fit
with the center mapping frozen, using Task 18's schema-balanced squared-center
plus central-interval-score objective. The calibration role supplies the
registered additive residual expansion at `alpha_cal=.10`; the external
checker either accepts the bound proposal as `U_safe` or leaves the atom open.
`A` and `I` share the same `J` center/radius coordinates.

After the learned head, fixed decoder operations derive separate signed
support/refutation margins, paired ReLU values, exact `K_3`, public outcomes,
and masks. These are semantic **channels**, not additional learned heads. In
particular, `z_support=ReLU(m_support/sigma)` and
`z_refute=ReLU(m_refute/sigma)` do not imply two parameterized heads.

### 7.2 Direct cross-entropy arm

The baseline has the same permitted inputs and matched shared-trunk family but
emits three logits per meaningful atom slot and minimizes independent `K_3`
cross-entropy against oracle-derived labels. It predicts `K_3` directly; it
does not emit a statistic region. `WF`, missing/invalid/expiry/scope handling,
and polarity are exact common postprocessing: impossible support under a
lower-only mode and impossible refutation under an upper-only mode become
`Open`, and unusable evidence is exactly `Open` regardless of logits.

Both arms use the same exact profile aggregation, active mask, and query/public
decoder. Both see the same tolerances, including changed tolerances. Neither
sees the reference label except as a train-role target.

### 7.3 Fairness and factorization

The arms use identical worlds, minibatch/update counts, optimizer family,
normalization, early-stopping information, hyperparameter-trial budget, and
paired initialization schedule. Trunk width is adjusted so total trainable
parameters differ by at most 2%; parameters, active parameters, FLOPs, wall
time, and tuning count are all reported.

A separate-head structured variant (distinct `J` and `T` learned heads) may be
reported descriptively if implemented without reducing core power. It is not a
logical necessity and cannot become a confirmatory claim after results are
seen. The frozen primary factorization is the single vector head above.

## 8. Reference labels and tolerance transfer

All atom and query labels are computed once by the generator oracle from `U*`,
exact evidence mode/polarity, exact `WF`, and the frozen profile. A learned
interval, class probability, router score, or self-confidence value never
creates a reference label.

In-regime tolerances are those produced by normalized oracle-endpoint offsets
`d in [-1,1]`, including equality. Transfer queries reuse the same world,
plan, target law, reference interval, and evidence record but change the
declared threshold to offsets

```text
d in {-2.0,-1.5,1.5,2.0}
```

and separately scale the evidence-width design variable by `.5` and `1.5`.
The generator constructs these requests before learner evaluation; the scorer
sees only the resulting allowed inputs. No parameter, calibrator, class head,
or threshold is refit for transfer. Changed tolerance is a new logical query,
not distribution-free proof of extrapolation.

## 9. Minimum-core endpoints

Every metric is first computed within world, averaged over the eight paired
fit seeds, and then compared across independent worlds. Target-weighted metrics
use the exact design ratios in Section 2; unweighted design and stratum metrics
are mandatory companions.

### 9.1 Confirmatory `F35/H18.1` endpoints

Let `Delta_e` be structured-arm fidelity minus CE fidelity in percentage-point
units.

1. **Tolerance-transfer macro `K_3` fidelity (`E_transfer`).** Target-weighted
   accuracy across changed-tolerance atom queries, macro-averaged over `J/T`,
   `Supported/Open/Refuted`, and the four transfer offsets.
2. **Boundary/status macro `K_3` fidelity (`E_boundary`).** Macro accuracy on
   strict-near-support, exact-boundary-support, crossing-open, and
   strict-near-refutation cases with the nearest normalized oracle endpoint at
   distance at most `.25`.
3. **In-regime guard (`E_in`).** Target-weighted macro `K_3` fidelity on the
   ordinary in-regime panel.

The registered superiority margin is **5 percentage points** for each primary
endpoint:

```text
H0_transfer: Delta_transfer <= .05
H0_boundary: Delta_boundary <= .05.
```

The in-regime noninferiority margin is **-2 percentage points**:

```text
H0_in: Delta_in <= -.02.
```

`F35/H18.1` is supported only if both superiority nulls are rejected after the
registered multiplicity correction and the noninferiority guard passes. It is
falsified at the stated practical preference if CE is itself noninferior to the
structured arm within 2 points on both primary endpoints and is not worse on
the guard under the corresponding one-sided intervals. Other patterns are
mixed/inconclusive and must be reported as such.

### 9.2 Registered key secondary endpoints

- false-support rate: reference not Supported among predicted Supported;
- false-refutation rate: reference not Refuted among predicted Refuted;
- class-conditional support/refutation miss rates;
- atom `K_3` fidelity by schema, state, polarity, mode, and diagnostic;
- query-quotient and four-way public-outcome fidelity after the same exact
  profile aggregation;
- simultaneous-license, empty-active-set, lapse/rebuttal,
  relevant/irrelevant-update, changed-tolerance, and later-dominator fidelity;
- proposed/accepted region width and infinity/rejection rate;
- inactive selection rate (required to be exactly zero in production),
  selected loss, deployed loss, fallback mass, and misroute severity; and
- CE probability calibration, explicitly labeled class-probability calibration
  and never compared to region coverage as if they were the same quantity.

These endpoints receive target-weighted estimates and 95% intervals but no
unregistered confirmatory claim. A favorable secondary cannot rescue a failed
primary family.

### 9.3 Registered `F36/H18.2` coverage endpoint

The two calibration groups are fixed as statistic schema `J` and statistic
schema `T`, pooling the preregistered plan templates and target contexts within
each group. The calibration/checker accepts the *mode and binding* before
confirmation targets are inspected. For every confirmation target eligible by
pre-outcome scope--target present, correct statistic group, frozen
scorer/binding, and no pre-outcome scope violation--record

```text
C_i = 1{t_i in U_prop_i}.
```

Here an infinite proposal contains every finite target under the registered
extended-real convention. If the mode/binding checker itself rejects the
procedure, `F36` is invalid/inconclusive rather than rescued by a conditional
subset. This is marginal target-in-proposal coverage. It is not oracle-region
containment, finite-interval-only coverage, conditional coverage, profile
coverage, coverage after selection, or system adequacy. Nominal coverage is
`.90`. For each group, success requires

```text
Holm-adjusted one-sided world-clustered 95% lower bound >= .88.
```

The 2-point gap is an estimation tolerance, not permission to rename 88% as
90%; the point estimate and its distance from `.90` are always reported. Both
schema claims must pass for `F36` to receive experiment-level support. Finite
width, infinity rate, pre-outcome rejection, and finite-usable-region coverage
are mandatory companions. The last quantity is explicitly
selected/descriptive and carries no marginal guarantee. Silently excluding a
difficult but eligible infinite proposal is a protocol failure. An individual
atom still treats an infinite or checker-rejected proposal as Open; counting
infinity for the calibration theorem does not turn it into usable evidence.

## 10. Multiplicity and paired inference

`E_transfer` and `E_boundary` form one one-sided family controlled by Holm at
familywise `alpha=.05`. The in-regime noninferiority test is an intersection
gate at one-sided `.05`; it cannot create success when either superiority test
fails. The `J/T` coverage tests form a separate Holm-controlled one-sided
family at `.05` because `F36` is a distinct absolute claim. There is no omnibus
"experiment succeeded" declaration across `F35` and `F36`.

The estimand is the paired mean of per-world arm differences after averaging
the fixed eight fit seeds. Primary confidence intervals and p-values use
10,000 paired world-cluster bootstrap replicates with a frozen analysis seed;
the centered bootstrap is shifted to the relevant registered null margin
(`.05`, `-.02`, or `.88`) for one-sided p-values, and percentile intervals are
reported as a robustness display. A secondary two-way world-by-fit-seed
bootstrap shows optimization variability without pretending seeds are target
worlds. If the bootstrap procedure fails its Task 19A numerical coverage check,
a prospective amendment must replace it before final manifests exist.

## 11. Power and sample-size rule

Task 19 fixes the rule before the numerical `N`. For each paired mean endpoint
`e`, let `s_e,U` be the registered planning upper bound for the standard
deviation of per-world paired differences. With target power `.90`, use

```text
N_e = ceil(1.15 (z_(1-alpha_e)+z_.90)^2 s_e,U^2 / delta_e^2),
```

where the 15% factor protects against pilot variance error,
`alpha_e=.025` is the conservative two-endpoint superiority allocation and
`delta_e=.05` is the distance from the `.05` null margin to the design
alternative `.10`; for the in-regime noninferiority gate use `alpha_e=.05`
and `delta_e=.02`, the distance from `-.02` to the design alternative `0`.
Power is computed on target-weighted world scores.

Task 19A amendment `19A-A2` records that a generator-only pilot cannot observe
paired differences from learners that Task 20 has not implemented. It would be
misleading to manufacture proxy-arm results and call their SD a pilot estimate.
The frozen protocol instead uses the largest Bernoulli-pair SD compatible with
the registered design alternatives: `sqrt(.29)=.538516` for structured `.90`
versus CE `.80` on the superiority endpoints, and `sqrt(.20)=.447214` for
`.90` versus `.90` on the noninferiority guard. Coverage uses the more
conservative of the observed oracle-balance pilot SD bound and worst complete
within-world clustering at `p=.90`, namely `.30`. These are power-planning
assumptions, not observed learner effects.

For each `F36` group, compute the one-sample world-clustered coverage size for
90% power against `H0:p<=.88` at design `p=.90`, one-sided `.025`, and also the
size required for a 95% interval half-width at most `.02`. The pilot intraworld
correlation and fixed per-world panel determine the effective variance; atom
rows are never inserted as independent Bernoulli trials.

The resulting endpoint counts are 1,402 worlds for each superiority endpoint,
4,925 for the in-regime guard, and 2,719 for each coverage group. Let `N_final`
be the maximum of all core requirements, rounded up to a whole block, with a
floor of **400 independent final worlds** and a cap of **5,000**.
If the rule exceeds 5,000, Task 19A declares the core infeasible and records a
versioned redesign; it may not shrink the effect margin or claim adequate power
after looking at final outcomes.

Rounding 4,925 to the frozen 100-world block gives `N_final=5,000`. Role sizes
are therefore frozen as

```text
train worlds       = 20,000 (16,000 fit; 4,000 internal selection)
calibration worlds = 5,000, with >=200 worlds per J/T group
validation worlds  = 5,000
system-audit worlds= 5,000
confirmation worlds=5,000.
```

Eight paired fit seeds are used for every trained arm and required ablation.
Optional extensions must add their own required independent units; they may not
consume or reduce minimum-core power.

## 12. Seeds, stopping, failures, and final embargo

Generator master seeds are role-specific and derive disjoint world,
trajectory, provenance, plan-lineage, observation, and event substreams. Pilot
seeds can never be promoted to a final role. Fit seeds are paired across arms;
data-order and initialization coupling is recorded, with head-specific random
draws isolated after the shared prefix.

The training-role roots are prospectively divided 80/20 into fitting and
internal model selection. Scorer hyperparameters use only that internal
selection partition; reject/router validation remains reserved for rejection
and routing and cannot alter the scorer or envelope. The frozen grid is 18
trials: learning rate in `{.0003,.001,.003}`, weight decay in
`{0,.0001,.001}`, and trainable-parameter budget in `{12,000,20,000}` under
AdamW, batch size 512, maximum 200 epochs, patience 20, minimum validation
improvement `1e-5`, and gradient-norm clip 1.0. Calibration labels cannot
choose a scorer; system-audit outcomes cannot tune a component. No optional
stopping uses a confirmatory metric.

Task 19A creates and hashes the final role manifests without generating a
readable result summary. Task 21 runs the fully frozen confirmation entry point
once. Infrastructure failures may be rerun only with the identical seed and
configuration, before any metric is read, with the failure logged. A numerical
or unfavorable result is not an infrastructure failure. Missing final worlds
are retained as missing under a prespecified failure indicator; replacement
worlds are forbidden.

## 13. Required arms and ablations

All conditions use the common input firewall, reference labels, exact `WF`,
polarity, profile aggregation, active mask, data/update budget, and reporting
interface.

1. **Structured reference:** center plus learned radius, disjoint accepted
   held-out expansion, exact region decoder.
2. **Ablation 1 / CE baseline:** direct independent atom `K_3`
   cross-entropy.
3. **Ablation 2 / center only:** point center with zero proposed radius before
   the common checker/calibration convention.
4. **Ablation 3 / unaccepted uncertainty:** predicted radius with no accepted
   held-out expansion; its outputs are proposals and cannot license. For fit
   comparison only, decode them in a clearly labeled nonproduction shadow
   path.
5. **Ablation 5 / self-confidence grant:** a learned confidence score is
   incorrectly treated as authorization. This intentionally invalid condition
   measures the failure mode and never supplies an active production mask.

The invalid ablations cannot be made semantically valid by good predictive
performance. They test why the checker and exact mask exist.

## 14. Deterministic `F18` sign and masking witness

This witness runs as an exact regression before any powered analysis and is not
an empirical endpoint. For the fixture `O` at stage 0,

```text
s_support/sigma = (2,12,3)
z_support       = (2,12,3)
exact states    = (Supported,Supported,Supported)
g = ReLU(WF+b_A+b_I+b_C-3) = 1.
```

It must distinguish four levels:

1. an arbitrary positive hidden activation means only positive preactivation;
2. `ReLU(epsilon-J_hat)>0` is predicted positive slack and may be wrong;
3. `ReLU((epsilon-upper(U_safe))/sigma)>0` is strict normalized
   certificate-relative surplus for one accepted atom; and
4. the full license requires `WF=1` and every required exact state Supported.

For accepted `U_J=[.17,.20]` at `epsilon=.20`, the atom is Supported at
equality although its support surplus is zero. For accepted `[.18,.22]`, both
support/refutation ReLUs are zero and the atom is Open. Missing and invalid
records also store masked zeros, so zero has no unique logical meaning.

The implementation must also reproduce

```text
y = 3 ReLU(-10) + 2 + 5 = 7.
```

Zero in one unit therefore does not quarantine a bias or bypass. In the toy
ranking calculation, loss surpluses may still make a raw score positive when
`C` is missing; exact `g=0` must remove the candidate before routing. Passing
requires a positive raw score and exactly zero inactive-selection probability.

## 15. Trace and audit record

Every prediction produces a machine-readable trace containing, at minimum:

```text
protocol/version and all manifest hashes
world/trajectory/provenance/plan-family root IDs and role
allowed input-field names and firewall result (not forbidden values)
request, profile slots, units, thresholds, scope, stage, and event prefix
arm, parameter hash, learned-head factorization, fit seed, capacity/compute
raw center/radius or logits
proposal-binding/checker record and exact evidence polarity/validity
signed margins, paired ReLUs, exact K3, WF, public outcome, active mask
router/fallback result and dependency/read-write footprint
oracle fields in a separately access-controlled evaluation namespace
target/design weights, stratum, metric contributions, and failure flags.
```

Learner code cannot import the oracle namespace. Evaluation joins it only after
predictions and hashes are frozen. Traces preserve full precision and include a
human-readable rendering for the narrative fixture.

## 16. Optional routing/seam extension: hard MoE

**Task 19A gate result: prospectively omitted.** The pilot contains no
independent conforming/mismatched seam generator or defensible paired
interaction-variance estimate, and adding one would displace the minimum core.
No absence or negative result is inferred; this remains a future study against
the frozen interface.

This extension is omitted prospectively unless Task 19A shows 90% power for a
paired architecture-by-seam interaction with at least 100 independent
conforming seams and 100 independent mismatched seams in each evaluated role.
The registered effect is a reduction of at least `.05` in 95th-percentile
normalized near-seam error for hard MoE relative to the ordinary ReLU model on
mismatched seams, together with conforming-seam noninferiority within `.02`.
Holm controls the two one-sided conditions at `.05`.

If activated, both architectures receive identical nonleaking inputs and emit
the same center/radius, payload, and grade schemas. They share worlds, update
counts, normalization, objective, tuning budget, decoder, mask, router, and
seed schedule; total parameters match within 2%, while active parameters,
FLOPs, wall time, and tuning trials are separately reported. Each has its own
identically specified calibration record. The learned gate never receives an
oracle regime or seam-conformance label. An oracle gate is only a labeled
expressivity upper bound.

The endpoint panel includes near-seam extrapolation, 95th-percentile and
maximum normalized error, transition width, and the prespecified interaction.
A finite sample cannot prove the exact continuity impossibility theorem. If the
power/runtime gate fails or the extension would reduce core resources, hard
MoE is omitted rather than run underpowered.

## 17. Optional certificate-carrying system extension

**Task 19A gate result: deterministic integration witness only.** The
root-count condition passes, but no Task 20 learned-grade adapter or empirical
false-grant variance yet exists. The powered empirical comparison is therefore
not activated. Existing and Task 20 regressions may exercise proof erasure,
adapter/checker acceptance, invalid local certificates, cycle rejection, and
audit/confirmation separation without marketing them as a powered result.

This extension uses finite acyclic plan graphs only. Learned nodes may emit a
typed payload and quantitative grade proposal. A registered adapter converts
the learned grade envelope plus primitive checked evidence into the input
schema of the exact composite-certificate transformer. The checker verifies
local rules, interfaces, provenance union, and the grounded rank order. A
learned grade, confidence score, or system's judgment about itself is never its
own certificate.

The system-audit role is lower-ranked evidence: it builds a frozen audit record
about the fitted system. The untouched confirmation role then evaluates that
already-audited system. Audit and confirmation roots, plan families, and
provenance are disjoint. The comparison with self-confidence-only
pseudo-licensing is an intentionally invalid ablation.

Task 19A may activate a powered empirical system claim only if there are at
least 200 independent plan-family roots per audit/confirmation role and 90%
power for a prespecified 2-point reduction in false grants relative to the
invalid self-confidence condition. Otherwise the extension is a deterministic
integration witness: proof erasure, valid composite acceptance, invalid local
certificate rejection, cycle rejection, and audit/confirmation separation.
Neither grade is described as whole-system truth.

## 18. Exploratory activation alignment

Named activation/state agreement, intervention stability, channel identity
across seeds, and surplus use by a downstream consumer may be plotted. These
analyses are exploratory, receive no confirmatory p-values, and cannot establish
that arbitrary hidden units have adequacy semantics or that the reference
factorization is uniquely interpretable.

## 19. Prospective amendment and adjudication rule

Task 19A may fill the sample size, seed list, architecture widths, optimizer
grid, epoch/stopping constants, and machine-readable hashes using pilot-only
information. It may repair an impossible quota, coding ambiguity, invalid
bootstrap, or failed optional-extension power gate. Every repair must be dated,
justified without final outcomes, and reflected in a new protocol version.

After any final manifest is generated, changes to hypotheses, margins,
endpoints, weights, strata, oracle, allowed inputs, split roles, checker,
head factorization, inference, or stopping are deviations. Task 21 reports them;
Checkpoint C1 adjudicates `F35`, `F36`, optional extensions, and their project
impacts separately. No post-hoc result may be relabeled preregistered.

## 20. Task 19A acceptance checklist

Status: **passed on 256 pilot-only roots**; see
[`00_pilot.md`](00_pilot.md) and
[`pilot_results_v1.json`](pilot_results_v1.json). Production manifests contain
only deterministic identifiers and hashes; their world payloads remain
unmaterialized.

Before Task 20 may implement learners, Task 19A must show on pilot-only roots
that:

- all formulas, scopes, quotas, four public outcomes, three `K_3` states,
  missing/invalid modes, overlaps, gap, simultaneous grants, lapse/rebuttal,
  updates, tolerance transfer, and later finite-set dominator are realized;
- the scorer firewall rejects every direct and proxy leakage test;
- proposal bindings reject every registered mismatch and preserve infinity;
- the five manifests are lineage-disjoint and role flow is one-way;
- target weights, boundary density, paired world variance, runtime, and the
  numerical sample-size rule are frozen;
- the reference and CE arms can be capacity/update matched under the declared
  head factorization without implementing or inspecting final performance;
- every deterministic `F18` witness passes; and
- each optional extension is prospectively activated, demoted to illustration,
  or omitted according to its own gate.

Only then is the machine-readable protocol frozen and Task 20 allowed to begin.
