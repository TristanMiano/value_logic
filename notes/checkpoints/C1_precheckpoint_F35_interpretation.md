# Pre-Checkpoint C1: interpreting the mixed `F35` result

Date: 2026-07-16  
Status: required input to Checkpoint C1; not itself an adjudication checkpoint  
Primary readers: project author, Fable 5, later paper authors, and human reviewers

## Durable summary

`F35` tested one proposed neural implementation default, not the value logic as a whole. It compared a structured ReLU learner that predicts numerical centers and uncertainty radii, followed by held-out calibration and an exact `K_3` decoder, with a matched ReLU learner that directly predicts `Refuted`, `Open`, or `Supported` by cross-entropy. The registered positive claim required the structured arm to beat direct classification on tolerance transfer and boundary fidelity while remaining noninferior on ordinary in-regime cases.

The result is **scientifically mixed but statistically clear**. Structured learning wins tolerance transfer by `+0.1866`, loses boundary fidelity by `-0.2612`, and loses the in-regime guard by `-0.1009`. Every one of the eight paired fit seeds has those same three directions. “Mixed/inconclusive” therefore must not be paraphrased as “the experiment could not tell.” It means that the experiment found a stable trade-off in opposing directions.

The upstream effect is asymmetric. The result strengthens the motivation for retaining the quantitative information from which an adequacy judgment is derived: that information transfers extremely well when the tolerance changes. It seriously weakens the further claim that the selected center–radius loss, calibration, and conservative decoder form a generally preferable operational classifier. It does not damage the architecture-neutral license calculus, the origin of task/domain-relative tolerances, the atlas and update semantics, the exact `WF + K_3` decoder, or the ReLU representation/existence theorems.

Checkpoint C1 should treat this as a central limitation and design discovery, not a footnote and not a failed project. It should consider splitting the broad empirical story into a supported information-retention/transfer result and a negative operational-conservatism result, while retaining the frozen aggregate disposition and prohibiting any outcome-selected confirmation rerun.

## 1. What `F35` asked

Suppose a system must decide whether a model is adequate relative to a current loss tolerance. There are two broad neural strategies.

The **structured strategy** predicts something like:

> The relevant loss is centered near `0.18`, with an accepted uncertainty interval from `0.15` to `0.21`.

An exact external rule then compares that interval with the requested tolerance and emits `Supported`, `Open`, or `Refuted`. The learned output remains a proposal until the held-out calibration record and exact checker accept it.

The **direct cross-entropy strategy** predicts the three-way state itself:

> For this request, the state is probably `Supported`.

This comparison was not made unfairly. Both arms used matched ReLU MLP capacity, the same data, paired initialization, matched training/tuning budgets, the same permitted pre-outcome inputs—including the requested tolerance—and the same exact evidence, polarity, well-formedness, profile, mask, and fallback machinery. Cross-entropy was therefore allowed to learn tolerance dependence; it was not merely forced to reuse one old label.

The structured representation nevertheless has a special information advantage. It is trained to retain an estimate of the underlying statistic and uncertainty region. The same output can be compared with a newly requested threshold. A single already-collapsed status label does not generally retain enough information to reconstruct every changed-threshold answer. The representation theorems establish this separator as a possibility; they do not establish that the structured learner will be the better classifier in practice.

The registered `F35` prediction went beyond the information separator. It required structured learning to:

1. outperform direct `K_3` cross-entropy by at least five points on the 16 realizable tolerance-transfer cells;
2. outperform it by at least five points on the exact four-query boundary panel; and
3. remain within two points on ordinary in-regime fidelity.

All three conditions were required for support. A separately frozen reverse rule would label the practical preference falsified only if the competing direction won sufficiently across the registered components. This is why the aggregate disposition can be mixed even though parts of the original positive conjunction clearly failed.

## 2. What happened

The inferential unit was one of 5,000 independent final world roots. The eight fixed paired fit seeds were averaged inside each world before the 10,000-replicate paired world bootstrap.

| registered component | structured | direct CE | structured minus CE | 95% paired interval | outcome |
|---|---:|---:|---:|---:|---|
| tolerance transfer | 0.9436 | 0.7570 | +0.1866 | [0.1860, 0.1873] | structured superiority passes |
| boundary panel | 0.5196 | 0.7808 | -0.2612 | [-0.2636, -0.2587] | structured superiority fails badly |
| in-regime guard | 0.7764 | 0.8773 | -0.1009 | [-0.1022, -0.0997] | noninferiority fails badly |

These intervals are narrow and far from zero. The mixed label is about the direction of the scientific findings, not sampling ambiguity. The seed-level results tell the same story:

- transfer differences range from `+0.0969` to `+0.2468`;
- boundary differences range from `-0.3046` to `-0.2349`; and
- in-regime differences range from `-0.1413` to `-0.0647`.

The structured arm was not simply producing meaningless intervals. The separate `F36` test supports nominal marginal target-in-proposal coverage in both registered statistic groups: `0.9098` for `J` and `0.9044` for `T`, both above the registered lower-bound rule. This is narrow marginal coverage, not a whole-profile or system guarantee, but it matters to the interpretation of `F35`: the structured system's operational deficit coexists with successful registered proposal coverage.

## 3. The behavioral explanation: safety through withholding

The unweighted trace companions show why the structured arm behaves this way.

| unweighted probe behavior | structured | direct CE |
|---|---:|---:|
| false support | 0.0087 | 0.0988 |
| false refutation | 0.0146 | 0.1624 |
| missed support | 0.4611 | 0.0640 |
| missed refutation | 0.3248 | 0.0627 |
| accuracy on `Open`, group `J` | 0.9910 | 0.8120 |

The structured system almost never makes the wrong positive assertion, but often refuses to make a correct one. Its target-weighted downstream fallback mass is `0.9962`, compared with `0.9139` for direct CE. The logic is behaving conservatively: uncertainty intervals that do not sit wholly on one permitted side of a boundary yield `Open`, and an open required atom prevents a full license.

This is not a defect in the meaning of `Open`; `Open` is doing exactly the epistemic work assigned to it. The practical problem is frequency. A reliance logic that nearly always falls back may be safe in one sense while failing to provide useful discrimination or action guidance. Sound withholding and useful coverage are separate objectives.

The likely lesson is not that numerical regions are pointless. It is that the chosen objective and calibration/decoder combination strongly favors avoiding false assertions over recovering supported and refuted cases. The experiment did not separately identify how much of that trade-off comes from the center/radius loss, model fitting, residual expansion, exact conservative decision band, synthetic distribution, or their interaction. Any causal decomposition would require a new prospectively designed study.

## 4. How the result changes the upstream motivational chain

The project’s earlier motivational chain can be separated into four claims:

1. **Finite-stage reliance:** because theories may be superseded indefinitely, a bounded agent needs revisable, domain- and task-relative warrants rather than a claim of final truth.
2. **Tolerance-sensitive information:** adequacy depends on a loss, domain, task, fallback, and tolerance; the tolerance can change with context or a new status quo.
3. **Representational possibility:** a neural system can preserve the relevant numerical quantities and pass them to an exact external license decoder.
4. **Learning-method preference:** the selected structured center–radius objective is a generally preferable way to learn that interface.

`F35` has almost no negative bearing on claim 1. The formal logic does not depend on either learned arm winning.

It positively bears on claim 2. The large tolerance-transfer advantage is precisely what should occur if preserving the underlying statistic matters when standards change. This is unusually well aligned with the motivating example of scientific theories remaining useful under changing domains, purposes, and tolerances.

It is compatible with claim 3. The structured ReLU arm learned transferable numerical information, `F36` supports its registered marginal proposal coverage, and the exact representation theorems remain intact. This does not establish semantic alignment or interpretability, but it demonstrates more than bare function-class existence.

It seriously weakens claim 4. The paper can no longer say or imply that the value logic naturally selects center–radius training as a broadly superior operational objective. That objective is a design choice downstream of the main question, not something forced by `Pi(M,D,epsilon)` or the ReLU construction.

The clean pre-result narrative was:

> Value logic requires retained quantitative adequacy information; therefore structured learning should generally outperform direct state classification.

The defensible post-result narrative is:

> Value logic identifies information that a revisable adequacy judgment may need. Structured learning preserves that information and transfers strongly across changed tolerances, but the tested conservative implementation pays a large price in current-threshold fidelity and usable coverage. Information preservation and operational decision quality are different objectives.

## 5. Damage assessment by project layer

| project layer or ambition | effect of the mixed result |
|---|---|
| philosophical motivation: useful but fallible theories | no material damage |
| task/domain/fallback-relative origin of `epsilon` | no damage |
| finite-stage license calculus and four public outcomes | no material damage |
| overlapping domains, atlases, bridges, updates, and retention | no damage |
| exact `WF + K_3` evidence/profile/mask/fallback boundary | no damage |
| ReLU/CPWL representation and finite-plan existence theorems | no damage; they never promised learnability or superiority |
| information-retention motivation for numerical statistics | strengthened on tolerance transfer |
| selected center–radius loss/calibration as the preferred default | seriously damaged |
| usefulness of the present learned operational system | seriously limited by near-universal fallback |
| ReLU as the uniquely or generally best architecture | unaffected because the project already rejected that claim |
| transparency and interpretability ambition | unresolved; F35 supplies neither internal-alignment nor human-interpretability evidence |
| final paper’s simple positive empirical story | moderately damaged and must be replaced by the observed trade-off |

The overall project is therefore not refuted or hollowed out. Its formal core, motivating question, and representation theory survive. But the damage is not cosmetic: the particular empirical bridge that was supposed to make the logic look naturally useful when learned by a basic ReLU MLP did not succeed as a general operational comparison. The final paper must not hide that fact behind the word “mixed.”

For the interpretability goal, the result is neutral but cautionary. Structured outputs may be more legible because they name centers, radii, margins, and exact state transitions. Yet a transparent system that almost always abstains is not automatically a useful explanation of a high-performing policy. Behavioral fidelity, internal alignment, causal faithfulness, and human inspectability remain separate future tests.

## 6. Questions and recommendations for Checkpoint C1

Checkpoint C1 should explicitly decide the following.

1. **Aggregate versus component dispositions.** Preserve the frozen aggregate `F35/I1` mixed disposition, but consider recording a supported tolerance-transfer component and negatively resolved boundary/noninferiority components. Do not let the aggregate label erase the decisive component results.
2. **Terminology.** Prefer “mixed with decisive opposing effects” over bare “inconclusive,” which readers may mistake for insufficient power or wide uncertainty.
3. **Paper position.** Treat the transfer/conservatism trade-off as a central empirical result and limitation. Do not retain center–radius training as an unqualified default.
4. **Theorem/experiment boundary.** Keep Proposition 2 and the representation theorems: they show information separation and realizability, not practical dominance. State this distinction near the first presentation of the neural motivation.
5. **Safety/usefulness boundary.** Explain that low false-assertion rates and calibrated marginal proposals do not imply useful licensed coverage. Fallback mass and missed support/refutation must accompany any safety language.
6. **No retrospective rescue.** Do not tune thresholds, losses, intervals, endpoints, or rerun confirmation to improve `F35`. A study of the conservatism mechanism or an alternative objective must be separately versioned, prospectively specified, and presented as future work or a new experiment.
7. **Architecture breadth.** Do not infer that direct CE is universally superior, that structured learning is universally inferior, or that another architecture would solve the problem. The result concerns the exact matched arms and synthetic distribution tested.
8. **Interpretability claims.** Do not convert named structured channels into an interpretability result. Their semantics are more explicit at the interface, but mechanistic transparency and policy/value reconstruction remain untested.

Fable 5 and human reviewers are specifically invited to challenge whether the current aggregate status vocabulary communicates this result honestly, whether the proposed component split is legitimate without altering the preregistration, and whether downstream tasks or the final paper outline still silently assume general structured-objective superiority.

## 7. Evidence trail

- The complete reader-facing numerical record is [`experiments/02_results.md`](../../experiments/02_results.md).
- The frozen machine-readable analysis is [`experiments/analysis_v1_1.json`](../../experiments/analysis_v1_1.json).
- The current `F35/F36` ledger rows are in [`notes/claim_ledger.md`](../claim_ledger.md).
- The pre-experiment neural blueprint is [`notes/checkpoints/C_neural_blueprint.md`](C_neural_blueprint.md).
- The representation results whose scope must remain separate are in [`ml/03_representation_theorems.md`](../../ml/03_representation_theorems.md).
- Checkpoint C1 is controlled by [`TODO.md`](../../TODO.md), and this note is required input rather than a substitute for `C1_empirical_adjudication.md`.
