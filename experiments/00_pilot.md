# Task 19A pilot and protocol freeze

Status: **completed on 2026-07-14 using only 256 pilot-role worlds.** No train,
calibration, reject/router-validation, system-audit, or final-confirmation
world payload was materialized. The frozen machine-readable contract is
[`protocol_v1.json`](protocol_v1.json); the compact implicit split manifests
are in [`manifests_v1.json`](manifests_v1.json), and raw pilot aggregates are in
[`pilot_results_v1.json`](pilot_results_v1.json).

## 1. What was built

[`protocol.py`](protocol.py) is a standard-library executable specification of
the Task 19 generator and trust boundary. It implements:

- deterministic role/world/trajectory/provenance/plan-family identities;
- the frozen CPWL loss and latency laws, hidden world effects, conditional
  Normal targets, and exact 90% oracle reference regions;
- 80 atom probes and 40 request trajectories per world with exact design
  quotas, target weights, overlaps, stage-0 gap, and later `N` scope;
- exact evidence presence, validity, expiry, polarity, inclusive support,
  strict refutation, `K_3` aggregation, and all four public outcomes;
- the reusable `A and I and C` succession fixture, including simultaneous
  grants, fallback, lapse, rebuttal, relevant/irrelevant updates, tolerance
  change, and finite-set dominance;
- a closed scorer whitelist with explicit provenance-taint checks for direct,
  aliased, nested, and hash-based leakage;
- an immutable proposal/calibration/checker record with mismatch, expiry,
  polarity, sample-size, infinity, and endpoint checks;
- role-manifest construction and lineage-disjointness auditing;
- common fidelity, false-support/refutation, marginal-coverage, bootstrap-SD,
  and power-calculation primitives; and
- the deterministic `F18` sign, equality, bias/bypass, and exact-mask witness.

[`run_pilot.py`](run_pilot.py) can materialize only `Role.PILOT`. It generates
compact production manifests from deterministic identities but never calls the
world generator for a production role. The generator also refuses final-world
materialization by default; Task 21 will need an explicit `allow_final` action
under the frozen entry point. Once `protocol_v1.json` exists, the pilot CLI
refuses to overwrite frozen artifacts unless a prospective repair explicitly
uses `--force-refreeze`; any such repair must receive a new protocol version
before production generation.

## 2. Pilot bank and balance

The pilot used 256 roots under seed label `pilot-7b9d41c6`. Each root contains
40 `J` probes, 40 `T` probes, and 40 request trajectories. Every world passed
the following exact checks:

- each statistic schema has atom-stratum counts `(10,8,8,4,4,6)` for strict
  support, boundary support, crossing/polarity open, missing open, invalid
  open, and refuted;
- each schema and the request panel have context counts `(8,12,10,10)` for
  old-only, overlap, successor-only, and the stage-0 gap;
- request outcomes are 12 Granted, 12 Withheld, 12 Refused, and 4 Undefined;
- each meaningful outcome rotates its focal atom exactly four times through
  `A`, `I`, and `C`;
- exactly eight well-formed requests contain a supported equality boundary;
- `A` and `I` share the same loss region while retaining distinct thresholds;
  and
- every fallback-improvement request has a positive `Delta`.

Across the pilot this yields 20,480 atom probes and 10,240 requests. The atom
states were 9,216 Supported, 8,192 Open, and 3,072 Refuted. There were 4,096
boundary atom probes, 2,048 boundary requests, and 2,048 deliberately missing
learning targets. The quotas are construction checks, not favorable empirical
findings.

The independently sampled target fell inside its exact generator reference
region at rates:

| schema | observed oracle-region coverage | bootstrap upper 95% bound for world-level SD |
|---|---:|---:|
| loss `J` | 0.896875 | 0.0573002 |
| latency `T` | 0.8963867 | 0.0515448 |

Both lie in the pilot acceptance band `[.885,.915]` around the exact `.90`
conditional law. These numbers validate the oracle sampler and balance only.
They are not coverage results for the unimplemented structured learner and do
not adjudicate `F36`.

The generator produced 256 worlds in about 0.28 seconds on the recorded Python
3.13.3 runtime, roughly 900 worlds per second. This validates generator and
manifest feasibility, not neural-training runtime.

## 3. Two prospective amendments

### 3.1 `19A-A1`: dominance needs paired evidence

Task 19's later-plan marginal intervals overlap the older-plan intervals.
Consequently they cannot alone establish strict componentwise dominance.
The fixture now binds four paired-difference certificates:

```text
J(N)-J(O) in [-.10,-.02],   T(N)-T(O) in [-7,-.5] ms,
J(N)-J(S) in [-.08,-.005],  T(N)-T(S) in [-8,-.5] ms.
```

Every upper endpoint is negative. These records can be valid when marginal
measurements overlap because paired outcomes may be correlated. The finite-set
dominator test now checks these certificates; it does not infer dominance from
the marginal table or globalize the result beyond `{O,S,N}`.

### 3.2 `19A-A2`: pre-learner variance cannot be observed

Task 19 asked the generator pilot for an upper confidence bound on the paired
world-level fidelity difference. That quantity does not exist until Task 20
implements and fits both arms. Inventing pilot-only proxy learners would both
begin Task 20 early and risk designing the sample size around a prejudicial
effect. The power freeze therefore uses explicit conservative planning bounds,
not purported observed learner variance.

For superiority, the design alternative is structured accuracy `.90` versus
CE `.80`, ten points above the five-point null margin. The largest paired
Bernoulli SD compatible with those marginals is

```text
sqrt(.30-.10^2) = sqrt(.29) = .538516.
```

For the in-regime guard, both design accuracies are `.90`; worst compatible
discordance is `.20`, giving SD `sqrt(.20)=.447214`. For coverage the planning
bound is `.30`, corresponding to complete within-world clustering at `p=.90`
and exceeding the observed oracle-balance SD bounds. These are assumptions of
the power design, not evidence that either learner will attain `.90`.

## 4. Frozen power and sample sizes

Applying Task 19's 15% inflation and one-sided normal planning rule gives:

| endpoint | null/design separation | SD bound | required independent worlds |
|---|---:|---:|---:|
| tolerance-transfer superiority | .05 | .538516 | 1,402 |
| boundary/status superiority | .05 | .538516 | 1,402 |
| in-regime noninferiority | .02 | .447214 | 4,925 |
| marginal coverage `J` | .02 | .30 | 2,719 |
| marginal coverage `T` | .02 | .30 | 2,719 |

The in-regime guard binds. Rounding 4,925 to the frozen 100-world block gives
the preregistered cap of 5,000 confirmation worlds. Production-role sizes are:

```text
train                       20,000
envelope calibration         5,000
reject/router validation     5,000
system audit                 5,000
final confirmation           5,000
```

The train role is prospectively divided by root: indices `0..15999` are the
16,000 fitting worlds and indices `16000..19999` are the 4,000
internal-selection worlds. This repairs a role ambiguity in the prose:
ordinary scorer selection cannot use reject/router validation, whose outcomes
are reserved for conservative rejection and post-license routing.

The sample size reaches but does not exceed the Task 19 cap. If actual
Task 20 fitting is much noisier than the registered planning alternative, the
proper eventual disposition may be underpowered/inconclusive; sample size will
not be enlarged after final outcomes are inspected.

## 5. Frozen learning and analysis controls

The protocol preserves the primary learned factorization rather than
implementing it:

```text
structured: shared ReLU trunk -> one vector head
            (center_J,radius_J,center_T,radius_T)
CE baseline: matched shared-trunk family -> three logits per atom slot
decoder:     fixed margins/ReLUs/K3/WF/profile/mask, not learned heads
```

Both use two hidden ReLU layers. A deterministic capacity rule chooses the
smallest integer widths meeting the selected parameter budget and at most 2%
between-arm mismatch, with lower inference FLOPs as the tie-breaker. The 18
train-internal selection trials cross learning rates
`{.0003,.001,.003}`, weight decays `{0,.0001,.001}`, and parameter budgets
`{12000,20000}` under AdamW, batch size 512, maximum 200 epochs, patience 20,
minimum improvement `1e-5`, and gradient-norm clip 1.0. Eight fit seeds and the
10,000-replicate world-cluster bootstrap seed are frozen in the JSON protocol.

Task 20 may implement this deterministic rule; it may not choose a new
factorization or grid from audit/final performance. Calibration remains
`alpha_cal=.10` in separate `J/T` groups, with at least 200 calibration worlds
per group. Infinite proposals count in the marginal proposal-coverage
estimand, but are unusable and force exact `Open`.

## 6. Optional-extension decisions

- **Hard MoE: prospectively omitted.** No independent conforming/mismatched
  seam generator or paired interaction-variance estimate exists, and building
  a separately powered study would displace the minimum core. This is not a
  negative or inconclusive architecture result.
- **Certificate/system extension: deterministic witness only.** The root-count
  gate passes, but the learned-grade adapter and its false-grant variance do
  not exist before Task 20. The project may test proof erasure, adapter/checker
  acceptance, invalid local certificates, cycles, and audit/confirmation
  separation, but cannot report a powered empirical system claim.
- **Activation alignment: exploratory only.** No confirmatory inference is
  assigned.

## 7. Frozen manifests and embargo

The compact manifests store each role's seed label, count, first/last root,
ordered SHA-256 digests for world, trajectory, provenance, and plan-family
identities, and a combined manifest hash. Exact membership is regenerated from
the public deterministic rule, avoiding a multi-megabyte list while binding
every root. A full cross-role audit found no overlap in any of the four lineage
dimensions.

The final-confirmation manifest hash is
`28f8fd31125d2019db52e002b9f7f38e0b14411cdb7b597cd726a191339e6ff2`.
Only identifiers and digests exist; `payloads_generated=false` is asserted in
the manifest, protocol, pilot result, and regression suite. The generator's
default final-role call raises `FinalEmbargoError`.

The frozen protocol binds the design, generator source, pilot runner, pilot
result, and manifest file by SHA-256. The repository tests recompute the
source/result/manifest hashes and reject drift.

## 8. Acceptance disposition and handoff

All Task 19A generator, semantic, firewall, binding, split, metric, power,
fixture, and embargo gates pass. Eighteen new focused regressions cover the
new machinery; the existing proof-plan tests continue to carry the detailed
finite-DAG certificate/cycle witnesses.

Task 20 may now implement the matched learners and deterministic system
integration against `protocol_v1.json`. It must not generate final worlds,
change registered margins or weights, reactivate hard MoE, upgrade the system
witness to a powered claim, or tune from system-audit/final outcomes.
