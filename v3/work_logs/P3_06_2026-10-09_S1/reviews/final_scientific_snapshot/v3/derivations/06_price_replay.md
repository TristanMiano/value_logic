# P3-06 — Repricing a forecast history

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
Development evidence and an information contract for
[CF-7](06_cost_forecast_refinement.md). This is a newly reconstructed service;
it is not the missing earlier P3-06 learner or its reported 96-query run.

## 1. Three services with different outputs

A change of prices does not identify a unique operation on a learning system.
The retained scalar, the chosen action and the learning trajectory can each
be held fixed or recomputed. The implemented comparison makes these choices
explicit.

| Service | Retained information | Recomputed output |
|---|---|---|
| Rescore the issued forecasts and old decisions | Old scalar reports, old action mixtures, checked answers | Losses of those historical outputs under the new weights and rows |
| Choose new actions from old forecasts | Old scalar reports, new known rows, announced smoothing rule; admitted answers for scoring | New action mixtures and their retrospective losses |
| Replay the forecast procedure | Original query and admission order, admitted answers, expert policy, learner settings, new weights and rows | New scalar reports, new actions and their own finite certificates |

The first service answers what the old behavior would have cost. The second
answers what a decision rule using the old estimates would now do. The third
answers what this specified learner would have reported on the same query
and evidence schedule with different announced prices. These are useful
counterfactual computations with declared fixed inputs. They do not identify
what an acquisition policy would have discovered under a different policy.

There are also two distinct certificate questions. Changing action rows alone
leaves the original scalar's Brier and tent-calibration certificates applicable
to its original weights. An old action-feature certificate concerns its old
rows and mixture; it does not automatically certify the new decision rule.
Changing the weights changes the Brier and calibration metrics themselves.
An arbitrary new weight schedule is not automatically certified; CF-7's
represented menu and CF-17's coordinated unit scaling are explicit transfer
cases. A replay can instead produce
a new certificate for the new reports and new weights.

## 2. The information retained by this implementation

The [replay program](../checks/06_price_replay.py), version
`p306-price-replay-v2`, reads the immutable first mathematical development
run and projects it onto public issue events and explicit admission events.
An issue supplies its scoped modular query, announced weight and action rows.
An admission supplies only a checked answer and residue actually admitted by
that point. The projection excludes the original forecasts, private pending
answers and exact-baseline reports. Poisoning or deleting those excluded
fields leaves the projected replay tape unchanged.

The program reconstructs the expert values independently from the admitted
residue counts and public shortcut computations. In this adapter the expert
policy depends on query descriptions and admitted evidence, not on past learner
forecasts or prices. Consequently this is a full replay of that policy on the
fixed issue/admission schedule. Merely saving old expert numbers would not
be enough for an expert that depended on the original learner outputs.

The identity profile reproduces every original scalar report, the complete
numeric issue records and the final pool audits. Replay never admits an
unresolved label early. At the delayed cutoff eight original queries remain
pending in every profile. Original files remain unchanged and are hash-bound
in the manifest.

For a finite profile menu, aggregate per-profile expert/learner losses and
tent residuals suffice to reconstruct unnormalized linear scores. Normalized
scores also require the corresponding total weights; conditional-bin errors
require the per-profile bin masses. None of these summaries by itself permits
general policy replay. Arbitrary new per-round weights generally require
more history, as the separating examples in CF-7 demonstrate.

## 3. Bounded development comparison

Before execution, the source fixed three profiles: identity; a cyclic weight
multiplier of 1, 3, 2, 5 indexed by issue tick; and a row change multiplying
action zero's outcome-one loss by three and action one's outcome-zero loss
by two. These choices do not inspect the answer. The comparison covers the
four existing 128-query development cases and both polynomial variants.

The saved [v2 manifest](../work_logs/P3_06_2026-10-09_S1/development/price_replay_v2/manifest.json)
reports PASS on 15,368 checks, including identity reconstruction, private-field
noninterference, admitted-evidence ordering, pending partitions and new
certificate validity. This is a bounded executable check of the documented
service, not a general proof that replay improves performance.

Changing rows leaves the plain variant's scalar forecasts unchanged because
rows are absent from its features. The decision-feature variant changes
112–124 forecasts across the four cases. Changing weights changes 57–126
forecasts. Thus retaining a scalar and retraining a scalar can materially
differ even when the mathematical answers and their arrival times stay fixed.

Two examples show why all three services should remain visible. The numbers
below are signed cumulative mixed-action regret to the better fixed action
identity, evaluated under the changed rows and the original weights.

| Decision-feature case | Old mixture, new prices | New mixture from old scalar | Replayed scalar and mixture |
|---|---:|---:|---:|
| Varying stakes and actions | 167.820081 | 36.277236 | 163.266601 |
| Delayed evidence cutoff | 317.981770 | 18.453982 | 272.141220 |

In the varying-stakes case, replay also raises Brier loss per weight from
0.318507 to 0.361728. Its new certificate remains valid. A valid guarantee and
an empirical improvement are different conclusions; these cases establish
no advantage for retraining over recomputing actions from the retained scalar.

## 4. Preserved correction and revision boundary

The [v1 outputs and source snapshot](../work_logs/P3_06_2026-10-09_S1/development/price_replay_v1/manifest.json)
are preserved. Their single `old_certificate_transferred` flag was too broad:
it said false even for row-only changes that leave the original Brier and
calibration metric intact. Version 2 separates original scalar-certificate
applicability, original action-certificate applicability and the replay's own
certificate. All forecast and score numbers remain unchanged. This corrects
metadata rather than deleting an unfavorable result.

A semantic-version change, evidence withdrawal or contradictory answer is
outside this fixed-answer repricing operation. The implementation rejects
wrong scopes and duplicate admissions; it does not claim a complete live
dependency-revocation system. Such a change requires a new episode or a
proved transport with the affected warrants made stale in the meantime.

P3-07's paid-reasoning policy is not implemented here. All comparisons remain
development evidence; no final challenge was frozen or exposed.

## 5. CF-17: coordinated unit changes preserve the forecast

An arbitrary new price schedule can change the learned trajectory. A pure
change of units with transported settings is a more restricted operation.
Fix positive rational factors $`u,v`$, keep the same expert values and
query/admission tape, and transform every round by

```math
w'_t=uw_t,\qquad c'_{t,i}(y)=v c_{t,i}(y)+g_t(y),
\qquad\eta'_t=v\eta_t,
```

where $`g_t`$ is a known affine row common to both actions. Stable action
identities and the same tie policy are retained. The expert policy must
either be independent of these units, as in the current adapter, or be
transported so that its scalar outputs are the same.

For the polynomial core, also use

```math
\gamma'=\gamma/v,\qquad \delta'_t=u^2\delta_t,
```

while leaving the expert/calibration scales, grid and numerical caps fixed.
The common offset cancels from action-cost differences, and positive cost
scaling with the transformed smoothing width preserves the mixture. The
action slope differences scale by $`v`$, which the transformed $`\gamma`$
cancels. Every feature therefore scales by $`u`$.

Induction on admitted observations gives the exact identities

```math
\Phi'_t(p)=u\Phi_t(p),\quad R'_t=uR_t,\quad
S'_t(p)=u^2S_t(p),\quad A'_t=u^2A_t,\quad B'_t=u^2B_t.
```

Each coordinate magnitude bound, coordinate Lipschitz bound and residual
scales by $`u`$. Thus the actual implemented score Lipschitz estimate
scales by $`u^2`$. The transformed root tolerance gives the same sufficient
bisection budget, the same comparisons and the same returned scalar,
including the same behavior under an explicit finite cap. Copies receive
the same issued and admitted identities, so the argument applies to the
delayed pool too.

Squared losses and calibration residuals scale by $`u`$. Weighted relative
action regret and smoothing slack scale by $`uv`$. The aggregate exact
$`H=\sum_k\sqrt{B_k}`$ scales by $`u`$, but a fixed-bit dyadic upper
enclosure of $`H`$ need not scale exactly: rounding must also be transported
if equality of the displayed rational bounds is required. Validity does not
require that equality.

For the separate capital implementation, set

```math
w'_{\max}=u w_{\max},\qquad D'_{\max}=vD_{\max}.
```

Keep the horizon, priors, grid and dimensionless numerical request/caps fixed.
Its rate rule then gives
$`\kappa'=\kappa/u`$, $`\lambda'=\lambda/u`$ and
$`\rho'=\rho/(uv)`$. Expert loss differences scale by $`u`$,
calibration coefficients by $`u`$, and action coefficients by $`uv`$.
Every log-capital increment is consequently identical for both hypothetical
outcomes. All exponential-enclosure inputs, search branches, issued scalars
and capital allowances are identical. Its Brier and calibration certificates
scale by $`u`$, and its action certificates by $`uv`$.

The [fixed public-prefix probe](../work_logs/P3_06_2026-10-09_S1/development/unit_covariance_v1/result.json)
checks these identities for three prospectively recorded transformations on
16 issue ticks from the existing null and delayed cases: 3,522 checks, PASS.
It covers plain and decision polynomial variants, the capital method, both
counterfactual log updates and admitted per-copy state. It is a check of
representation transport, not a new predictive comparison or parameter sweep.

This theorem does not make arbitrary row or weight changes harmless. In
particular, keeping the old root tolerance or decision scale while changing
units defines a different finite procedure. Actual stored costs acquire the
common offset $`u\sum_t w_tg_t(y_t)`$, and their arithmetic bit sizes can
change even when forecasts and relative regrets agree. The native-cost
power-of-two rule in CF-10 fixes its cost unit explicitly; applying that rule
afresh after an arbitrary unit change is not automatically the coordinated
transformation proved here.
