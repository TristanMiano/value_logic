# Task 23: Policy-to-Value Interpretability Bridge

Date: 2026-07-18

Checkpoint D motivation, comparator, and companion-gate amendment: 2026-07-21

Status: design complete; empirical bridge remains companion/future work

Depends on: [`policy_value_judgment.md`](policy_value_judgment.md),
[`formalism/09_judgment_information.md`](../formalism/09_judgment_information.md),
the canonical profile interface in
[`formalism/07_core_calculus.md`](../formalism/07_core_calculus.md), and the
Checkpoint C1 component dispositions in
[`checkpoints/C1_empirical_adjudication.md`](checkpoints/C1_empirical_adjudication.md)

Companion scope: [`policy_value_isomorph`](https://github.com/TristanMiano/policy_value_isomorph/tree/097ea8897fb203b9b3a6ceafcb29e11bdc6cdd6c)
at inspected commit `097ea8897fb203b9b3a6ceafcb29e11bdc6cdd6c`

## Durable design decisions

1. **The bridge does not ask whether an arbitrary agent has a true utility
   function.** Its target is an approximate, environment-relative value
   representation of a bounded black-box policy. It does not claim that a true
   utility exists, that the surrogate recovers it, or that unlimited compute
   would make the surrogate the uniquely truest recoverable object.
2. **Value is the project's first semantic foothold.** The author was led from policy reconstruction to pragmatic logic
   because value-like rankings were the first tractable semantic object he saw
   how to recover from behavior; beliefs were not recovered first and their
   extraction was less direct. This records research motivation. The project
   makes no claim that value is universally prior, that belief extraction is
   impossible, or that every policy has an internal utility module.
3. **Three correspondence questions remain separate.** A finite lossless
   action-code or action-score representation proves abstract existence. A
   standard `V^pi` or `Q^pi` is instead fixed by a declared decision process and
   return. A learned surrogate is an empirical approximation to that second
   object. None of these facts identifies a unique natural utility or the
   policy's internal mechanism.
4. **Semantic abstraction can trade detail for meaning.** A categorical action
   code can preserve the policy exactly while carrying only conventional label
   meaning. An environment-relative value surrogate can lose action-level detail
   while exposing return estimates, counterfactual rankings, and failure
   regions. Whether that trade is useful is an empirical question; neither a
   real codomain nor exact behavioral agreement is interpretability by itself.
5. **Interpretability is represented as a profile.** Behavioral fidelity,
   value fidelity, outcome/task information, domain validity, representational
   alignment, causal faithfulness, and human inspectability are separate axes.
   The project does not combine them into a single interpretability score, and
   evidence on one axis must not be silently promoted to another.
6. **The value-logic bridge is an auditable reliance wrapper.** A reconstructed
   `V/Q` becomes an evaluated use plan under a context that fixes its target,
   domain, loss, fallback, tolerance, constraints, and evidence mode. Named
   profiles can require value/ranking fidelity, support, improvement, and trace
   while reporting the other interpretability axes. Bare `LicInterp` remains
   undefined.
7. **Task 22A applies only when an outcome-information claim is made.** A
   valid evaluation certificate that lower-bounds the population log-loss gain
   over the true nuisance-conditioned Bayes baseline also lower-bounds
   `I(J;Y|N)`. Only explicit
   mediation transfers that result to the outcome-identifiable task quotient.
   A merely nuisance-conditioned comparator instead uses the lower bound
   `delta_b-Regret_N(b)` for the population gap; empirical use needs an
   accepted lower bound on `delta_b` and upper bound on comparator regret.
   The theorem does not establish readability, mechanism, causality, or a full
   latent ontology.
8. **The companion is a conditional case study.** Its current separate policy,
   value, and Q models support an implementation-level policy-evaluation and
   greedy-agreement study. They supply no present representational, causal, or
   human evidence. Greedy disagreement can be policy improvement rather than a
   failed inversion.
9. **Coverage and fallback usefulness are feasibility gates.** `F35a` supports
   changed-tolerance reuse of a numerical statistic in this repository's
   synthetic experiment. Neither `F36` nor named channels establishes
   interpretability, and `0.9962` fallback mass bars a claim that the tested
   structured pipeline was a useful transparent default.
10. **Publication placement is therefore bounded.** The author motivation and
    seven-axis design may appear briefly in the paper, but a positive
    policy-to-value interpretability result belongs in a companion case-study or
    future-work section unless the relevant experiments are run. It is not a
    core contribution of the present repository.
11. **Output semantics is a starting point for an inward research program.**
    The author's further motivation is to ask whether a certified value-like
    output semantics can guide recovery of stable semantic structure deeper in
    a network. Tracing that meaning into an independently trained value
    surrogate concerns the surrogate itself. A claim about the original policy
    additionally needs an explicit alignment/readout link to policy hidden
    states and policy-side interventions; representational alignment and causal
    faithfulness remain independent gates.

## 1. Author objective and controlling non-claim

The source posts establish the historical arc.
[*Is Utility All You Need?*](../posts/utility_all_you_need.txt) starts from
agents as black-box input/output mappings and asks whether behavior can be
re-expressed through value.
[*Judgment, Value, and the Recovery of Fact*](../posts/judgement_value_fact_recovery.txt)
then presents policy-to-value reconstruction as a miniature of a larger
pragmatic sequence: repeated action reveals value-like direction; repeated
evaluation can reveal stable structure; contact with outcomes constrains which
structures survive.
[*Condensed Response to Hidden Complexity of Wishes*](../posts/condensed-response-hidden-complexity.txt)
uses stronger “isomorphism” and utility language. The two founding transcripts,
[`chatgpt.txt`](../llm_convos/chatgpt.txt) and
[`claude.txt`](../llm_convos/claude.txt), supply the adequacy-margin,
finite-license, and abstaining-atlas side of the bridge. These files are
provenance and motivation, not controlling evidence. The later survey
[*Utility- and Preference-Based Logics*](../posts/utility_preference_logic_nn.md)
supplies the explicit semantic-design distinction among scalar, vector,
ordered-world, and uncertainty/aggregation values; Task 23 does not infer from
that taxonomy that a trained network has one of those meanings internally.

The project author's 2026-07-18 clarification controls their interpretation.
The question “does this arbitrary policy have a true utility function?” is out
of scope. The proposed object is a **semantic surrogate**: a model-of-a-model
that summarizes what the policy does in value-like terms to an empirically
specified fidelity. It may be useful whether or not the policy contains a
utility representation internally. No claim is made that the surrogate is the
agent's true utility, that such a utility exists, or that the infinite-compute
limit would settle either question.

The author also identifies an important order of discovery. Value was the first
semantic object that seemed straightforward to reconstruct from the model:
observed choices induce candidate comparisons among reachable prospects, and a
declared environment supplies outcome and return tests. Beliefs were not the
first extracted object, and it was less clear how to identify them from the
same black-box behavior. This motivated the turn toward pragmatic concepts of
logic. The project's narrower restatement is that value is a promising first
**semantic foothold** for this program. It does not assert an ontological
reduction of belief to value or a universal theorem of semantic priority.

The project author further proposes a future **semantics-backward** program:
once the final value-like output has a declared and empirically licensed
meaning, test whether that semantics can be traced inward through stable
mappings, probes, and interventions on earlier layers. If those are the
independently trained surrogate's layers, the result describes that surrogate.
Transferring the interpretation to the original policy requires an explicit
alignment or readout relation to policy hidden states plus policy-side
interventions. This is recorded as motivation rather than a result. A semantic
label on an output does not by itself identify hidden coordinates or show that
the policy causally uses the surrogate's features; the representational-
alignment and causal-faithfulness axes below are the gates for any such
inference.

## 2. The object being reconstructed

Fix a versioned policy `pi` and a declared decision-process contract

```text
M = (S,A,P,r,gamma,mu,perspective,horizon,legal-actions,state-convention).
```

Under the usual scoped assumptions, this pair induces environment-relative
objects `V^(pi,M)` and `Q^(pi,M)`. A learned surrogate `V_hat` or `Q_hat` is
trained against rollout, dynamic-programming, or other versioned estimates of
those targets. The superscript `M` is conceptually load-bearing even when
omitted for readability. Changing reward, perspective, horizon, state/history,
or evaluation distribution changes the interpretation target rather than merely
adding more samples to the same claim.

If no return is independently declared, behavior may still support a
revealed-choice surrogate under known feasible sets and consistency assumptions.
That object should expose local ordinal inequalities, not be relabeled a
standard cardinal value function. Likewise, the finite encoder from Task 22 is
a lossless representation of actions but receives no return semantics merely
because its codomain is real-valued.

A useful surrogate record should expose at least:

```text
ValueView = {
  policy/environment/surrogate versions,
  state-or-history and declared domain,
  legal alternatives and transition summaries,
  V/Q estimates, uncertainty regions, and pairwise rankings,
  margin to the fidelity/tolerance and fallback requirements,
  active local rule or chart, when one is actually identified,
  selected action, original-policy action, and disagreement type,
  grant/withhold/refuse/undefined or explicit abstention,
  diagnostic witnesses, obstacles, and provenance trace
}.
```

“Local rule” means a rule of the surrogate—such as a local affine piece,
decision path, sparse feature summary, or value decomposition—whose validity
region is checked. It is not automatically a rule used internally by the
original policy.

## 3. Seven non-collapsible evidence axes

| axis | operational question | suitable evidence | what it does not establish |
|---|---|---|---|
| behavioral fidelity | Does value-guided decoding reproduce the frozen policy's action distribution on the declared population? | held-out agreement, action-distribution KL/log loss, tie-aware top-set coverage, on-/off-policy strata | return fidelity, unique preference, mechanism, or beneficial behavior |
| value fidelity | Does the surrogate predict the declared `V^(pi,M)`/`Q^(pi,M)` target or its rankings? | held-out return error, calibrated intervals, pairwise ranking loss, regret of decoded choices | inversion of a suboptimal policy or a true internal utility |
| outcome/task information | Does a report derived from the surrogate contain conditional information about held-out outcomes or their identifiable task quotient? | Task 22A log-loss gap against the true `P(Y|N)` Bayes baseline; mediation audit for quotient transfer | full task identity, human-readable semantics, or licensing |
| domain validity | Where is the preceding evidence valid and operationally useful? | support tests, lineage-separated shift panels, risk--coverage curves, fallback rate/severity, abstention calibration | fidelity outside the evaluated population |
| representational alignment | Are policy and surrogate representations stably related beyond output agreement? | cross-validated probes/mappings, subspace similarity, shared-versus-independent encoder comparisons, cross-seed and symmetry controls | causal use of the aligned features or uniquely named coordinates |
| causal faithfulness | Do interventions on the proposed value-relevant variables change policy behavior as predicted? | targeted interventions/ablations, matched control ablations, state counterfactuals, mediation of action changes | human usability or a uniquely true utility |
| human inspectability | Does the exposed view help people understand, predict, or audit the policy? | blinded user tasks measuring accuracy, time, calibration, error detection, and reliance/abstention quality against baselines | mechanistic identity or correctness outside the tested task |

These axes form a vector or partially ordered evidence profile. Averaging them
would allow, for example, excellent action imitation to conceal zero causal
evidence or attractive traces to conceal unusable coverage. The report should
therefore retain every axis and mark unmeasured entries explicitly.

Task 22A's information criterion is deliberately conditional. Let `J` be a
pre-outcome report computed from the surrogate, `Y` a held-out outcome, and `N`
the declared nuisance context. If `J` is a deterministic function of everything
already placed in `N`, then it cannot add conditional information; the baseline
design must reflect the claim actually being tested. A finite game with an exact
outcome law may permit the true nuisance Bayes comparator. A merely flexible
learned comparator does not become Bayes-optimal by name, so any empirical
application must use the correction
`I(J;Y|N)>=delta_b-Regret_N(b)` for the population gap. Before reporting a
positive numerical information bound, it must certify a lower bound on
`delta_b` and an upper bound on comparator regret under a stated joint
coverage rule.

## 4. Feeding `V/Q` into the profile-indexed license interface

Treat the versioned surrogate plus its renderer/decoder as an evaluated use plan
`e_V`. Its context `q_V` declares:

- policy, environment, return, state/history, perspective, and horizon versions;
- the deployment and counterfactual state distributions;
- whether the primary task is value prediction, action ranking, behavior
  reconstruction, or human audit support;
- its target loss/risk aggregation and acceptable region;
- the original policy, direct rollout, a simpler surrogate, or abstention as the
  explicit fallback;
- the required improvement margin, coverage floor, and resource/safety limits;
- certificate, calibration, and trace modes; and
- the comparator library and finite evaluation scope when relative preference is
  requested.

The open atom family in the core permits named, typed constraints. Three profile
shapes are useful without inventing a universal interpretability predicate:

```text
P_surrogate-rely = required {
  Adeq(value-or-ranking fidelity),
  Improve(named fallback,Delta),
  Constraint(domain/support coverage),
  Constraint(counterfactual validity when action use is authorized),
  Trace
}
report {behavior, outcome-information, representation, causal, human axes}

P_surrogate-mechanism = P_surrogate-rely plus required {
  Constraint(representational alignment),
  Constraint(causal faithfulness)
}

P_surrogate-human = P_surrogate-rely plus required {
  Constraint(human inspectability)
}.
```

The latter two are not linearly ordered: a human-useful abstraction need not
identify mechanism, and a causally faithful internal description need not be
readable. A comparison profile can separately extend any shape with
`RelUndom` or `CertUndom` over a finite set containing direct imitation, lookup
or rollout summaries, simple heuristics, and the value/Q candidates. No profile
claims global bestness.

The complete diagnostic vector supplies the proposed transparency interface.
It shows the exact domain, value/ranking error region, margin to threshold and
fallback, support and shift flags, local rule and alternative transitions,
active/selected plan, abstention, and trace. `Withheld` must remain distinct from
`Refused`, and failed well-formedness from both. If no surrogate is active, the
selector uses the declared fallback or requests more information; it does not
force an explanatory value label.

## 5. Test program and repository allocation

| test | design and controls | allocation |
|---|---|---|
| interface/countermodel suite | Check exact profile typing, version binding, margins, four-way outcomes, traces, and abstention on same-policy/different-return, same-value/different-policy, off-support, state-aliasing, tie, and suboptimal-policy fixtures. | this repository, as any future adapter to the canonical calculus |
| held-out value and behavior fidelity | Split by trajectory/provenance root and policy seed; evaluate on-policy, reachable counterfactual, and deliberately off-policy states. Report value error/ranking separately from action agreement and task return. | companion repository |
| fair surrogate baselines | Compare `V`, `Q`, direct policy imitation, lookup/rollout summaries, occupancy statistics, and simple low-dimensional heuristics under matched data/compute where applicable. Include intentionally suboptimal and stochastic policies so greedy improvement is visible. | companion repository |
| counterfactual ranking | Query every legal alternative where feasible; compare predicted successor/action rankings with the declared return target, including tie and perspective changes. Treat reward/perspective changes as new contexts. | companion repository |
| outcome-information audit | Freeze `J,Y,N`, lineage, score, and population; use an exact Bayes nuisance baseline where the finite game permits it, otherwise certify an upper bound on comparator regret and apply the corrected bound. Audit mediation before claiming task-quotient information. | theorem and synthetic countermodels here; empirical application in the companion |
| support, shift, and usefulness | Produce full risk--coverage curves and fallback mass/severity over held-out games or layouts, policy seeds, reachable/off-policy states, stochasticity, and history-dependent cases. Predeclare minimum useful coverage. | companion repository; broader domains in future work |
| representation probes | Compare separate encoders with a shared-encoder policy/value variant. Cross-validate linear/orthogonal mappings, probes, and subspace similarity; include random, label-permuted, cross-seed, and function-preserving symmetry controls. | companion repository if architecture is instrumented |
| causal tests | Intervene on or ablate proposed value-relevant policy features and test predicted changes in rankings/actions against matched nonsemantic ablations. Manipulating only the separate surrogate tests that surrogate, not the policy. | companion for instrumentable models; larger-agent studies are future work |
| human readability | Blind participants to condition; compare the licensed value view with raw policy outputs, direct imitation explanations, and rollout tables on action prediction, failure detection, appropriate abstention, time, and calibration. | future work after nontrivial domain coverage is achieved |

Any future companion experiment waits until its open PyTorch-migration Tasks
23--29 are complete, records a fresh exact commit pin, and freezes thresholds
and evidence roles before reading outcomes. The current pin remains a
code-inspection reference; it is not a standing authorization to run or extend
the companion study.

All empirical thresholds should be frozen before the corresponding outcomes are
inspected. Agreement should be tie-aware. Return, policy fidelity, and task
performance should remain separate because a greedy decoder can improve the
task while disagreeing with the original policy. Shift panels must preserve
target/design weights and the diagnostics needed to explain fallback and misses.

## 6. What the frozen value-logic experiment contributes

The Task 21 experiment is an analogy and feasibility constraint, not a
policy/value result. `F35a` shows that retaining a reusable numerical statistic
helped under a changed tolerance without retraining. `F35b` and `F35c` show that
the tested conservative pipeline had worse boundary and ordinary in-regime
fidelity at the registered margins. This illustrates why numerical content,
categorical decision fidelity, calibrated caution, and operational usefulness
must be separated: a thresholded category discards magnitude, while a numerical
surrogate plus conservative decoder can retain magnitude yet abstain too often
to be useful.

`F36` establishes marginal target-in-proposal coverage only. It does not show
that named channels align with semantic features, that a human can understand
the trace, or that the system makes useful licensed predictions. The structured
arm's `0.9962` fallback mass is incompatible with presenting that configuration
as a practically useful transparent surrogate. Any future bridge must
preregister minimum licensed coverage or risk--coverage performance, not merely
proposal validity.

## 7. Claim and publication disposition

`G04` remains supported as a separation result: behavior can be reproduced
without shared mechanism. `G06` is now an operational seven-axis design; its
representational, causal, and human measurements remain unexecuted. `G05` is a
specified test program. The current artifacts supply no positive transparency
measurement for that program.

A positive **partial semantic-surrogate** claim would require declared
environment/return semantics, held-out value or counterfactual-ranking fidelity,
nontrivial domain coverage/usefulness, and auditable scope/traces. A mechanism
claim additionally requires representational and causal evidence. A human
interpretability claim requires comparative human-task evidence. If a study
misses its preregistered fidelity, usefulness, or human-task margin, that study
does not support the corresponding grade at its tested scope. Inadequate power
or coverage leaves the grade unresolved. Either outcome should guide a revised
surrogate, domain, or evidence requirement rather than be promoted to a
universal verdict about value-based interpretation.

The formal paper may retain the finite representation-existence proposition,
the environment-relative evaluation map, the Task 22A partial-information
criterion, and this evidence-grade separation. It should state plainly that the
policy/value interpretability bridge has a design and that its proposed
empirical measurements have not been run. The blog may use the author's “value
as the first semantic foothold” motivation while stating explicitly that the
project makes no claim about the existence or recovery of true utility. The
current companion can be cited as a scoped implementation witness; any positive
bridge result awaits its own preregistered tests.

## Task conclusion

Task 23 supplies a concrete route from a reconstructed `V/Q` to the canonical
value-logic interface without turning an existence encoding, standard policy
evaluation, behavioral agreement, or a named neural channel into
interpretability by stipulation. The strongest present conclusion is a design:
an environment-relative value surrogate can be assessed as a scoped semantic
model-of-a-model along seven separate evidence axes, with explicit fallback and
trace behavior. The empirical bridge remains companion/future work and is not a
core result of this repository.
