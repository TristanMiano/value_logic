# Source scope supplement: comparator order and ordinary comparisons

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Task: **R-P3-B-A**, base `6ce7391b6a41c6c19397b00ce7b6a2d9b228b9a4`.
Same-model, nonblind source follow-up; **zero principal research-clock credit**.
This supplement preserves `source_contracts.md`, `block_reconstruction.md` and
their original `manifest.json` byte for byte. Their hashes are recorded in
`supplement_manifest.json`. It makes no claim-status or later-task change.

## 1. The journal and thesis display different comparator orders

| Inspected primary version | Exact displayed left side | Locator |
| --- | --- | --- |
| Cesa-Bianchi, Lugosi and Stoltz, *Minimizing regret with label efficient prediction*, author-hosted journal manuscript, 2005 | `E[Lhat_n − min_i L_i,n]` | [PDF](https://stoltz.perso.math.cnrs.fr/Publications/CBLS-LabelEff.pdf), §III, Theorem 1, printed manuscript p. 3 / PDF index 2 |
| Stoltz, *Information incomplète et regret interne en prédiction de suites individuelles*, thesis, defended May 27, 2005 | `max_i E[Lhat_n − L_i,n]` | [PDF](https://stoltz.perso.math.cnrs.fr/Publications/TheseStoltz.pdf), chapter 5, Theorem 5.1, printed p. 89 / PDF index 88 |

Both displays use the same stated expected-count parameterization and upper
bound reported in the original review. The journal manuscript explicitly
permits outcomes to depend on past learner choices (§III, p. 3, text preceding
Theorem 1); its §II discussion on p. 2 already allows random comparator totals.
Thus an unprinted oblivious-only hypothesis should not be attributed to its
Theorem 1. Its proof's equation (4), p. 3, is indexed by each fixed expert.
The thesis display places the maximum outside expectation.

**Interpretation for this project, derived here.** For random comparator totals,

```math
\max_i\mathbb E[\widehat L-L_i]
=\mathbb E[\widehat L]-\min_i\mathbb E[L_i]
\le\mathbb E[\widehat L-\min_iL_i].
```

The inequality can be strict: take `L_1=Z`, `L_2=1−Z`, with `Z` a fair bit,
and `Lhat=1/2`. The two sides are respectively 0 and 1/2. This is a witness to
the quantifier distinction, not a claimed protocol counterexample to a source.

When the exogenous expert loss table is deterministic, every `L_i` is fixed
and the two expressions agree. That is the scope of the current imported
consequence and block reconstruction. No broader adaptive/random-hindsight
interpretation is needed or imported. The original review's journal-lineage
statement must not be read as claiming identical comparator quantifiers.
This note records the version difference without adjudicating the broader
source theorem.

## 2. Fixed contextual experts can be represented by fixed action indices

The relevant published comparator is Russo et al., *Online Learning with
Sublinear Best-Action Queries*, NeurIPS 2024:
[published PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/47795c4ae2f7d07ea2fb0d11fa2c3c90-Paper-Conference.pdf),
§1.1, pp. 2–3, and §2.2, pp. 6–7. It uses fixed action indices, an oblivious
bounded loss table, pre-action best-action queries and, in the limited-feedback
model, full-vector feedback only on queried rounds.

**Mapping derived here.** For a finite fixed library of policies `a_h`, fixed
mathematical queries `q_t`, deterministic answers `y(q_t)`, and a known loss
function, define the virtual-action table

```math
M_{h,t}=\ell(a_h(q_t),y(q_t)).
```

The source's action index is `h`; it need not denote one constant physical
binary guess. For a fixed deterministic table this is a direct representation,
so a separate theorem extending the source to predictable expert advice is
unnecessary. A purchased binary answer reveals the whole expert loss column
when all expert predictions and the loss function are computable from public
information; the required computation must receive its stated price.

If the current answer permits an action whose loss is even lower than every
expert's, the paid service can dominate a best-expert identifier. The local
upper bound still applies when corrected loss is at most the expert minimum,
but an ordinary control must receive the same correction capability. This is
especially relevant when all experts give the wrong binary guess.

If the query stream or expert states depend on learner history, the induced
loss table can be random. Calling the advice merely predictable does not
establish the block-selector independence used here, or import an oblivious
source theorem. Such an extension needs its own information structure and
proof. Fixed policies on a fixed query tape avoid that extension.

## 3. The published general-game lower bound does not transfer automatically

Russo et al.'s published §3, pp. 8–10, especially Lemma 3.1 and Theorem 3.4,
uses two stochastic environments over two action losses to establish
worst-case lower bounds in its label-efficient game. The hard distribution
assigns mass to `(1,1)`, `(0,0)`, `(0,1)` and `(1,0)`; vectors are independent
across rounds within each environment. Queried rounds reveal the vector;
unqueried rounds do not. The comparison here does not import its numerical
constants or independently validate all endpoint regimes.

**Restriction argument derived here.** A universal upper bound on loss tables
applies to each table induced by a fixed mathematical service. A worst-case
lower bound over all loss tables does not, by itself, apply to a restricted
mathematical family. For example, two constantly opposed binary guessers with
zero-one loss have complementary losses; they cannot realize the source's
agreement rows. Contextual experts could allow agreement, but a valid lower
bound reduction must also preserve what their public advice reveals. Simply
renaming actions as experts does not supply that reduction.

An exact-answer service that can choose outside the expert library introduces
a second issue: it may achieve zero current loss on a row where every source
action loses one. That stronger service must be reflected in any claimed
hardness reduction. We may compare the general-game rates and ordinary
algorithms, but should not claim minimax optimality or an impossibility for
the selected arithmetic family from this source alone.

## 4. One targeted recent follow-up is relevant, with a different service

**Francesco Bacchiocchi, Matteo Castiglioni, Alberto Marchesi and Francesco
Emanuele Stradi, *Multi-Armed Bandits With Best-Action Queries*,
[arXiv:2605.08287v1](https://arxiv.org/abs/2605.08287), submitted May 8, 2026;
[PDF](https://arxiv.org/pdf/2605.08287), front-page date May 12, 2026.**
No publication venue was verified. Section 2, printed pp. 5–6, Protocol 1,
imposes a deterministic query cap and reveals a best-arm identifier before
action, but reveals the chosen arm's reward on **every** round. Its regret
definition has the best expected fixed arm outside expectation. Its two
stochastic settings distinguish independence across arms and rounds from
joint reward vectors with correlated arms.

**Consequence derived here.** This does not replace the matching ordinary
control: our unpurchased labels do not reveal even the chosen expert's loss,
while a purchased answer can reveal all counterfactual expert losses. The
information advantages go in different directions. Its bandit-feedback
results require a separate reduction before use here. It is a useful recent
scope citation, not a reason to enlarge this recurrence or import a new bound.

The search was targeted to best-action queries and hard-budget label-efficient
prediction in 2025–2026. It establishes no exhaustive literature coverage or
novelty claim. No complete third-party PDF is included in this review folder.
