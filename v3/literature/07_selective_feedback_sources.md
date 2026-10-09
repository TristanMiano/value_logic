# Sources and comparison contracts for paid selective feedback

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Task: **R-P3-B-A**. The associated [derivation](../derivations/07_selective_feedback.md)
is DEVELOPMENT. Literature inspection supports attribution and comparison;
it is not a claim of exhaustive search or worldwide priority.

## 1. Product weights: the imported inequality

Nicolò Cesa-Bianchi, Yishay Mansour and Gilles Stoltz, *Improved second-order
bounds for prediction with expert advice*, **Machine Learning 66**, 321–352
(2007). [Author-hosted paper](https://cesa-bianchi.di.unimi.it/Pubblicazioni/J28.pdf),
§3, printed pp. 327–328, Lemmas 1–2. DOI: 10.1007/s10994-006-5001-7.

The paper's `prod` uses the linear multiplicative update and bounds cumulative
mixture gains by a fixed comparator, a logarithmic initial-weight penalty and
a second-order comparator term. Replacing gains by negative losses gives the
pathwise inequality used here. The finite loss convention and scalar logarithm
bounds are reconstructed in derivation §3.1. Neither the algorithm nor that
potential argument is new. The block sampling identity, paid current-action
correction, finite-state allowance and implementation invoice are separate
adaptation steps that must be justified in this project.

## 2. Label-efficient prediction: chronology and quantifiers

Nicolò Cesa-Bianchi, Gábor Lugosi and Gilles Stoltz, *Minimizing regret with
label efficient prediction*, **IEEE Transactions on Information Theory 51(6)**,
2152–2162 (2005). [Author-hosted manuscript](https://stoltz.perso.math.cnrs.fr/Publications/CBLS-LabelEff.pdf),
§III, Theorem 1, manuscript p. 3. Prediction incurs loss before purchased
feedback is used; unqueried outcomes remain unobserved. Its Bernoulli querying
scheme has an expected query count. The displayed theorem places the hindsight
minimum inside expectation and the surrounding setup permits past-dependent
outcomes. We do not silently replace that printed setup with an oblivious one.

Gilles Stoltz's [2005 thesis](https://stoltz.perso.math.cnrs.fr/Publications/TheseStoltz.pdf),
*Information incomplète et regret interne en prédiction de suites individuelles*,
chapter 5, §§2–3, printed pp. 86–92, provides another primary version of this
line of work. Its Theorem 5.1, p. 89, instead places the fixed-expert maximum
outside expectation. Its Theorem 5.2 provides a probability-qualified query
budget. These different printed comparator orders are recorded in the
[source scope supplement](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/source_scope_supplement.md).

For this project's **deterministic exogenous loss table**, those two comparator
orders coincide. That restricted consequence is sufficient. The general
identity is `max_i E[L−L_i] = E[L]−min_i E[L_i]`, which can be strictly smaller
than `E[L−min_i L_i]`. No broader adaptive-hindsight theorem is imported, and
a probability-qualified or expected count is not relabelled an exact quota.

## 3. Purchased best actions: the closest correction-aware source

Matteo Russo, Andrea Celli, Riccardo Colini-Baldeschi, Federico Fusco, Daniel
Haimovich, Dima Karamshuk, Stefano Leonardi and Niek Tax, *Online Learning with
Sublinear Best-Action Queries*, **NeurIPS 2024**.
[Published paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/47795c4ae2f7d07ea2fb0d11fa2c3c90-Paper-Conference.pdf),
§1.1, pp. 2–3, and §2.2, pp. 6–7, Theorem 2.4 and Lemma 2.5.

The model has an oblivious bounded loss matrix. A query identifies a current
best action before acting; limited-feedback play reveals the full loss column
only on queried rounds. The method analyzes capped Bernoulli proposals. Thus
current-action correction and the improvement it can create over ordinary
post-prediction feedback are established antecedents. Its published theorem,
including its budget range, is preserved in the
[initial source review](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/source_contracts.md).
We reconstruct the exact-quota block proof independently rather than importing
its constants. Source query counts do not price local computation or checking.

A fixed contextual expert is representable as a virtual fixed action index:
`M[i,t]=loss(a_i(q_t),y_t)` is a deterministic matrix on a fixed tape. Buying a
binary answer reveals that column after paid evaluation of the experts. Our
answer service can even correct a round on which all experts are wrong; a
matched ordinary control receives that same ability. General-game lower bounds
need a separate reduction to this restricted public mathematical family.

## 4. Adaptive selective sampling: disagreement is an established guide

Rui M. Castro, Fredrik Hellström and Tim van Erven, *Adaptive Selective Sampling
for Online Prediction with Experts*, **NeurIPS 2023**.
[Published paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/00b67df24009747e8bbed4c2c6f9c825-Paper-Conference.pdf),
§2, pp. 2–3; §4, Theorem 2 and Lemma 2, pp. 5–6; §5.

The method queries labels using weighted expert disagreement, and updates
exponential weights with importance-weighted observed losses. A sufficient
Bernoulli query probability is the minimum of one and weighted binary
variance times four plus one third of the learning rate. The stated regret
bound matches its full-feedback counterpart; reduced expected query complexity
uses an additional conditional gap premise. Every issued prediction incurs
its loss even when its label is bought.

This is the relevant ordinary antecedent for our adaptive selector. The local
extension changes the contract to one purchase per publicly visible block,
current-action correction, finite tickets and a positive propensity floor.
Its proof is independently reconstructed; a count or regret guarantee alone
would not cover the new hard resource bill. We do not claim invention of
disagreement sampling, importance weighting or learning-dependent purchases.

## 5. Recent best-action bandits have a different feedback service

Francesco Bacchiocchi, Matteo Castiglioni, Alberto Marchesi and Francesco
Emanuele Stradi, *Multi-Armed Bandits With Best-Action Queries*,
[arXiv:2605.08287v1](https://arxiv.org/abs/2605.08287), submitted May 8, 2026.
[PDF](https://arxiv.org/pdf/2605.08287), §2, pp. 5–6, Protocol 1.
No publication venue is asserted here.

Its query reveals a best-arm identifier before acting under a deterministic
query cap, while the chosen arm's reward is observed on every round. Our
unpurchased mathematical labels reveal no expert's loss, and a purchased
binary answer can reveal the full fixed-expert column. Those are different
information contracts. This source is a recent scope comparison, with no
bandit theorem or numerical constant imported into this recurrence.

## 6. What is compared, and what the adaptation adds

| Component | Established antecedent or ordinary comparator | Local obligation and evidence |
|---|---|---|
| Online learning | Linear product weights and label-efficient learning | Reconstruct the selected-loss potential inequality and prove its all-unbought block identity. |
| Current correction | Published best-action queries | Give the same correct current action to matched ordinary methods; keep pre-issued forecast scoring separate. |
| Adaptive acquisition | Disagreement sampling and importance weighting | Prove the `1/pi−1` remaining-action objective, require the actual propensity in each update, and pay for public lookahead. |
| Finite implementation | Ordinary integer arithmetic and fixed precision | Bound weights **and intermediates**, prove an explicit normalization error, debit bits, checking, buffering and outputs. |
| Mathematical computation | Binary modular exponentiation, caching and residue tables | Retain the strongest cheap public shortcut, actual construction costs and equivalent terminal answers. |
| Significance | Author's broad adaptation/synthesis criterion | Assess the precise completed interface and useful boundaries independently from algorithmic novelty and performance superiority. |

A restricted upper bound transfers from an ordinary matrix model to each
admitted mathematical loss table. A lower bound over all matrices does not
transfer without a reduction preserving public advice, query feedback and
corrected actions. Fixed exact experts or ordinary exact computations can
make a particular family easy even when its general feedback game is hard.

The local outcome is judged against the **ordinary combination**, not a weak
post-prediction baseline deprived of purchased corrections. An ordinary
implementation can use this entire construction unchanged. On the selected
finite family, the analytic table is a stronger economic control and its
unfavorable result is retained. A bounded formal adaptation can still be useful
by establishing exactly when learning, acquisition, forecasting and price
claims can be composed—and supplying concrete failures when they cannot.

## 7. Inspection and evidence trail

Primary PDFs were opened by the principal; the load-bearing displays in the
2005 versions were also inspected visually. A separate same-model, nonblind
review reconstructed the source interfaces and the block/propensity arguments.
See [source contracts](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/source_contracts.md),
[version and comparison supplement](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/source_scope_supplement.md),
and [adaptive reconstruction](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/adaptive_quota_review.md).
An earlier thesis URL under `normalesup.org` was unavailable; the author-hosted
version above was inspected successfully. Review time is not added to the
principal's research clock. Third-party PDFs are linked, not redistributed.

## 8. Observable performance: bounded moment inequality

Wassily Hoeffding, *Probability Inequalities for Sums of Bounded Random
Variables*, **Journal of the American Statistical Association 58(301)**,
13–30 (1963). DOI: 10.1080/01621459.1963.10500830.
[Original scanned paper](https://www.csee.umbc.edu/~lomonaco/f08/643/hwk643/Hoeffding.pdf),
§4, Lemma1 on printed p21 and equations4.12–4.16 on p22.

The centered single-variable exponential moment is bounded using the interval
width squared divided by eight. We apply that lemma conditionally and iterate
conditional expectations; the local filtration, purchased-label estimators,
shared binary-loss residual and public predictable widths are reconstructed
in the [observable-performance note](../derivations/07_observable_performance.md).
The original independent-sum theorem is not invoked as if the adaptive block
increments were independent. The exponential argument and concentration
method are established mathematics; the local contribution is the explicit
interface and its finite, paid-feedback application.

Text extraction from the scan produced no readable source text. The principal
inspected locally rendered printed pp19–22, including the stated formulas.
The [inspection receipt](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/hoeffding_source_inspection.json)
records the PDF hash; the paper and page images are linked rather than
redistributed in this repository.

## 9. Sampling inference and the fixed-rate boundary are established tools

D.G.Horvitz and D.J.Thompson, *A Generalization of Sampling Without
Replacement From a Finite Universe*, **JASA47(260)**,663–685(1952),
[original paper](https://www.stat.cmu.edu/~brian/905-2008/papers/Horvitz-Thompson-1952-jasa.pdf),
printedpp665–669, especially equation6,p669. The inverse-inclusion-probability
estimator reconstructs a finite population total; its stated uniqueness is
within a specified unbiased linear subclass. It does not establish globally
optimal sampling or the merit of our disagreement/cost heuristic. In this
project, learned forecast losses change with earlier selected labels, so the
argument is applied conditionally to each one-draw block and then iterated.
Per-draw conditional probabilities are not substituted for whole-sample
inclusion probabilities in a different sampling design.

StevenR.Howard, AadityaRamdas, JonMcAuliffe and JasjeetSekhon, *Time-uniform
Chernoff bounds via nonnegative supermartingales*, **ProbabilitySurveys17**,
257–317(2020), DOI10.1214/18-PS321. Inspected
[arXiv1808.03204v8](https://arxiv.org/pdf/1808.03204v8), datedDecember17,2025:
§2.1, Definition1 and conditional moment discussion, manuscriptpp8–10;
§2.3, Lemma1 and equation2.12,p14. These are version8 locators, not an
assertion about the journal pagination. The fixed-rate exponential crossing
bound used here is an elementary instance of that established framework.
Our finite first-crossing proof is supplied directly; no concentration-method
priority or unrestricted optimized variance bound is claimed.

The [inspection record](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/sampling_sources_inspection.json)
records the scanned source, actual inspected versions and access limits.
Together these sources support the interpretation as design-based inference:
the fixed mathematical answers need no IID population law. Selection and
action randomness, correct propensities and the unchanged policy chronology
remain essential. These probabilities concern sampling error, not a supplied
coherent distribution over mathematical truth.
