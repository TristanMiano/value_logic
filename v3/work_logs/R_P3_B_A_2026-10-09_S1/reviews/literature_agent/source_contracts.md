# Selective-feedback source contracts

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Review type: independent task assignment, same-model, nonblind source review.
Task: **R-P3-B-A**; published base: `6ce7391b6a41c6c19397b00ce7b6a2d9b228b9a4`.
Reviewer time adds **zero** to principal clocks. This review selects no later task,
changes no claim status, and does not review the eventual implementation.

## 1. Standard label-efficient prediction: imported source contract

**Gilles Stoltz, _Information incomplète et regret interne en prédiction de
suites individuelles_, thesis defended May 27, 2005.**
[Primary thesis](https://stoltz.perso.math.cnrs.fr/Publications/TheseStoltz.pdf),
chapter 5 §§2–3, printed pp. 86–92; Figures 1–3; Theorems 5.1–5.2;
Remark 5.1. PDF page indices are one less than printed pages.

Finite N>1; losses in [0,1]; fixed horizon n. Predict first, purchase feedback
second; an unqueried outcome remains unavailable. Expert advice is expressly
allowed. Figure 2 uses independent Bernoulli query indicators Z_t with rate
ε and updates exponential weights with estimated losses Z_t ℓ(i,y_t)/ε.

Theorem 5.1 sets ε=m/n and η=√(2m ln N)/n. It gives E[M]=m and

```math
\max_i\mathbb E[\widehat L_n-L_{i,n}]
\le n\sqrt{2\ln N/m}.
```

Theorem 5.2 sets ε=max{0,(m−√(2m ln(4/δ)))/n} and
η=√(2ε ln N/n). With probability at least 1−δ, M≤m and, simultaneously
for t≤n,

```math
\widehat L_t-\min_iL_{i,t}
\le 2n\sqrt{\ln N/m}+6n\sqrt{\ln(4N/\delta)/m}.
```

The environment may depend on past random choices, not current hidden coins.
Theorem 5.1's maximum lies **outside** expectation. Theorem 5.2's budget
statement is probabilistic. Neither establishes a sure quota by silently
clipping queries. Current-action correction is outside Figure 1's chronology.

Chapter 5 credits joint work with Cesa-Bianchi and Lugosi and a COLT 2004
extended abstract. The authors' [publication list](https://cesa-bianchi.di.unimi.it/papers.html)
confirms the journal version: **N. Cesa-Bianchi, G. Lugosi and G. Stoltz,
_Minimizing regret with label efficient prediction_, IEEE Transactions on
Information Theory 51(6), 2152–2162 (2005)**. An
[author-hosted manuscript](https://stoltz.perso.math.cnrs.fr/Publications/CBLS-LabelEff.pdf)
was inspected. This is the same research lineage, not independent corroboration.

## 2. Rational multiplicative updates: primary theorem available for import

**N. Cesa-Bianchi, Y. Mansour and G. Stoltz, _Improved second-order bounds for
prediction with expert advice_, Machine Learning 66, 321–352 (2007);
published online October 27, 2006.**
[Author-hosted journal paper](https://cesa-bianchi.di.unimi.it/Pubblicazioni/J28.pdf),
§3, printed pp. 327–328, Lemmas 1–2; DOI 10.1007/s10994-006-5001-7.

The source defines `prod(η)` with uniform initial weights and update
w_i←w_i(1+ηx_i). For gains x_i≥−M and 0<η≤1/(2M), Lemma 2 gives,
for every fixed comparator k and every realized gain table,

```math
\sum_t\langle p_t,x_t\rangle
\ge\sum_t x_{k,t}-\frac{\ln N}{\eta}-\eta\sum_t x_{k,t}^2.
```

Substituting x=−z with z∈[0,1] gives the loss update w_i←w_i(1−ηz_i)
and the upper loss bound used in the companion reconstruction. Rational
inputs and rational η preserve rational weights exactly. The source theorem
supplies the potential inequality; unbiased block sampling, current-action
correction and all-in computation prices remain separate adaptation steps.
Its second-order comparator term can be sharper than replacing z² by z.

A secondary cross-check is **Arora, Hazan and Kale (2012)**,
[The Multiplicative Weights Update Method](https://theoryofcomputing.org/articles/v008a006/v008a006.pdf),
§2, Figure 1 and Theorem 2.1, pp. 126–128. It gives the same linear update and
a first-order bound. That survey explicitly points back to `prod` and the
preceding Lemma 2; it is not an independent algorithmic antecedent.

## 3. Buying the current answer: closest published comparison

**M. Russo, A. Celli, R. Colini-Baldeschi, F. Fusco, D. Haimovich,
D. Karamshuk, S. Leonardi and N. Tax, _Online Learning with Sublinear
Best-Action Queries_, NeurIPS 2024.**
[Published paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/47795c4ae2f7d07ea2fb0d11fa2c3c90-Paper-Conference.pdf),
§1.1 pp. 2–3; §2.2 pp. 6–7, Theorem 2.4 and Lemma 2.5;
[official record](https://proceedings.neurips.cc/paper_files/paper/2024/hash/47795c4ae2f7d07ea2fb0d11fa2c3c90-Abstract-Conference.html).

An oblivious table assigns losses in [0,1] to N actions over T rounds.
A query reveals the current best action before selection. In the limited-feedback
setting, full loss feedback arrives only on queried rounds. Section 2.2 uses
Bernoulli proposals, stops querying at cap k, and compares against an uncapped
process. Its stated Theorem 2.4 bound is

```math
R_T\le 2\min\{T\sqrt{2\ln N/k},\ T^2\ln N/k^2\},
\qquad k\ge\sqrt{T\ln T/2}-1.
```

**Status here:** nearest ordinary comparison, not an imported constant-level
proof. The independent block derivation supplies this project's guarantee.
Current-action query correction, the hard-budget issue and the improved large-k
regret rate already have published treatment. This source does not price
implementation, checking, storage or setup. Earlier arXiv v1 numbering (§3.2,
Theorem 3.4) is superseded here by the published numbering.

## 4. Adaptive ordinary comparison for a broader future scope

**R. M. Castro, F. Hellström and T. van Erven, _Adaptive Selective Sampling for
Online Prediction with Experts_, NeurIPS 2023.**
[Published paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/00b67df24009747e8bbed4c2c6f9c825-Paper-Conference.pdf),
§§2, 4–5, Theorem 2, Lemma 2 and Theorem 3.

For binary expert predictions and zero-one loss, query probability can depend
on weighted disagreement while preserving an exponential-weights regret bound.
The displayed sufficient choice is
q_t=min{4A_t(1−A_t)+η/3,1}. Its theorem gives expected regret at most
ln N/η+nη/8. A separate conditional positive-gap assumption gives reduced
expected label complexity. It does not impose a selected exact query quota
or allow retroactive replacement of the issued prediction. **Status:**
comparison candidate if adaptive acquisition becomes an endpoint; no theorem
is imported into the fixed-block implementation.

## 5. Blocking is ordinary; the precise interface still matters

The inspected sources did not supply the exact one-uniform-position-per-block,
frozen-mixture, rational-update construction proposed here. That bounded search
establishes **no novelty**. The construction is a direct ordinary use of
stratified sampling and multiplicative weights, reconstructed in
[block_reconstruction.md](block_reconstruction.md).

As a scope cross-check, **Kanade, Liu and Radunovic, _Distributed Non-Stochastic
Experts_, NIPS 2012**, [§3.1, Figure 1 and §4](https://papers.nips.cc/paper_files/paper/2012/file/1385974ed5904a438616ff7bdb3f7439-Paper.pdf),
uses block-level FPL and discusses label-efficient prediction. Its distributed
communication model can transmit a cumulative block payoff. That is more
information than one paid label, so its block theorem is not substituted here.

## 6. Consequence for this recurrence

The strongest matched ordinary implementation should receive the same purchased
labels, pre-action correction, quota, deterministic query tape, price vector and
permitted exact computations. An ordinary block-`prod` implementation is already
a close control, including the stronger correction-aware learning rate. The
published capped-query best-action method is an additional algorithmic comparison
when implemented under matching costs. Bernoulli post-action feedback alone
would be a weaker service and cannot support an exclusive improvement claim.

Exact arithmetic, analytic shortcuts, caches and cheap fixed experts remain
legitimate controls. A negative cost comparison is informative. An accepted
result can be a modest checked adaptation or a clear limitation; neither the
classical learning method nor purchase-before-action capability becomes novel
by entering this repository.
