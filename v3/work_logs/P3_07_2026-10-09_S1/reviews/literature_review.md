# P3-07 — internal literature and import review

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: October 9, 2026 UTC. Starting base:
`c7386f115bf60a9eb3a419515c844b81fc6ba073`.

Scope: the paid-reasoning question in `TODO_v3.md` and the problem contract's
§6, with the principal's proposed finite catalogue, paired profile and fresh
controller audit. Nonblind internal review; no external validation or
principal Research90 credit. P3-01–06, ledger, clocks, task status and gates
were not edited. No experiment, final-challenge exposure or publication was
performed by this reviewer.

## Findings

The [primary-source comparison](../../../literature/07_paid_reasoning_sources.md)
identifies a strong ordinary method for the proposed task: computation
selection plus acquired procedure profiles, finite statistical coverage and
a fixed-policy assessment. Its source cards give the exact inspected
definitions, assumptions and reading limits. The
[retrieval manifest](../sources/literature_agent/source_manifest.json)
preserves primary URLs, retrieval references and hashes for locally inspected
sources.

The most consequential finding is PR07-2: the 1991 author manuscript already
discusses statistical assessment of an agent's own computational procedures,
the change in the agent caused by learning its controller, and probabilistic
self-modelling. A finite version-pinned audit is therefore a restricted
formal application, and needs an explicit target identity rather than a
generic claim of reflective novelty.

PR07-4 is a useful counterweight to a weak comparison: learned metalevel
selection, charging online selection time and amortizing offline training
are already addressed together. PR07-5 additionally demonstrates prediction
of an anytime algorithm's future quality within an individual run. The
P3-07 claim should concern its particular evidence and transport contract,
and any measured result against matched implementations.

## Load-bearing boundaries to preserve in the principal result

| Review item | Required disposition |
|---|---|
| Scope of Hay et al.'s model | Its supplied joint law can already include uncertain latent profile parameters. The practical acquisition/adequacy question must be stated separately. |
| Stopping and myopia | Preserve almost-sure versus uniformly bounded stopping; one-way myopic continuation is not a converse stopping theorem. Specialized Bernoulli bounds are not generic proof-search bounds. |
| Paired concentration | Apply the bounded-summand theorem to per-task differences; use their actual range width. Correlation inside a row is allowed. The adjacent independent-two-sample corollary is not the paired justification. |
| Repricing | The guarantee can hold for all linear price readouts on one simultaneous event. Keep the raw feature meaning and complete policy maps fixed, or explicitly cover their induced changes. |
| Selection | Profile-based choice among the predeclared finite policies is covered by simultaneous bounds. Arbitrary post hoc query filtering or catalogue expansion is a different statistical target. |
| Frozen controller | Fix trained state and operational dependencies as well as executable text. State episode resets; IID queries alone do not make stateful resource observations IID. |
| Fresh audit | Interpret performance conditionally on the frozen construction history, on the specified population and budget. Retuning on the same audit cohort needs a new validity argument. |
| Costs | Report full profile acquisition and conditional deployment separately; identify the amortization horizon and charge estimator/controller work. Preserve hard feasibility independently of priced means. |
| Labels | Complete paid resolution and censoring are different observations. No bound may silently discard unresolved tasks or substitute prediction confidence for checked truth. |
| Ordinary comparator | Permit the same empirical feature means/intervals or empirical row distribution. Do not burden only the comparator with an unnecessary richer truth model. |

These are requirements and observations for the prospective design. The
reviewer has not independently checked the final principal proof or the
developing adapter against them.

## Verification and exclusions

Primary verification covered Hay et al. 2012; Russell and Wefald 1991;
Zilberstein and Russell 1996; Callaway et al. 2018; Svegliato et al. 2018;
Hoeffding 1963; Thomas et al. 2015; and selected interfaces of
Karampatziakis et al. 2021. The 1989 Russell–Wefald IJCAI paper was also read
as corroborating history; the source note uses the closer 1991 manuscript.

Hoeffding's original scan was rendered locally because the web parser had
no text and web screenshots supplied only placeholders. Printed p. 16,
Theorem 2 and equation (2.6), were visually verified. The author-hosted 1991
PostScript was downloaded and converted for selected-page inspection;
manuscript pp. 20–21 were visually checked after text inspection. The
conversion emitted Type 3 font bounding-box warnings; both retained pages
were legible and their relevant equations and paragraphs matched the text.

S21 retains the existing P3-01 primary audit. Fresh source retrieval failed
in this review, so no additional primary-reading claim was made. No source's
reported empirical results were replicated. The source note's concentration
specialization is an elementary conditional adaptation for the proposed
sampling design; it is not a new theorem attributed to this reviewer.

## Disposition

The selected-source comparison is ready for principal use. It supports
classifying the central machinery as inherited interfaces and standard
statistical adaptations, and identifies the narrow integration that can be
assessed in P3-07. It supplies no gate pass, task-completion decision or
worldwide-priority claim. P3-N01 remains under its existing disposition.
