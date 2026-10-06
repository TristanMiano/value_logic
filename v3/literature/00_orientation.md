# Primary-source orientation for phase three

Contributor: **ChatGPT (GPT-6 Astra Pro)**, with same-model delegated research
reviewers. Accessed October 6, 2026 UTC. **Planning orientation only.**

These inspected sources establish relevant comparison directions. They do not
constitute an exhaustive novelty search or completed theorem-import audit.
P3-01 and later tasks must reconstruct the exact assumptions they use. No full
third-party paper is redistributed. Search failures are not evidence of novelty.

## S01 — Logical Induction

Scott Garrabrant, Tsvi Benson-Tilsen, Andrew Critch, Nate Soares and Jessica
Taylor, *Logical Induction* (2016). [Official full paper](https://intelligence.org/files/LogicalInduction.pdf),
[archival record](https://arxiv.org/abs/1609.03543).
Inspected: introduction and the following definitions/statements, not all proofs.

| Comparison target | Exact locator |
|---|---|
| Trading criterion and computable existence | Definitions 3.0.1 and 3.5.1; Theorem 3.6.1 |
| Convergence and coherence | Theorems 4.1.1–2 |
| Early prediction of provable patterns | Theorem 4.2.1 |
| Calibration and statistical patterns | Theorems 4.3.3, 4.3.8, 4.4.2 |
| Bounded numerical expectations and indicator probabilities | Definitions 4.8.1–2; Theorems 4.8.4, 4.8.6 |
| General convergence-rate boundary | §5.5; Proposition 5.5.1 |

Numerical expectations are already covered. A cost notation alone therefore
needs no new logical-induction theory. Phase three will investigate paid
reasoning, changing objectives and checked revision as possible additional value.

## S02 — Proper scoring rules

Tilmann Gneiting and Adrian E. Raftery, *Strictly Proper Scoring Rules,
Prediction, and Estimation*, JASA 102(477), 359–378 (2007).
[Author-hosted paper](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf),
[DOI](https://doi.org/10.1198/016214506000001437).
Inspected: §§1–3, especially the propriety definition, positive-affine
equivalence and Example 1, the quadratic/Brier score.

Proper scoring supplies an established loss-based bridge to probabilistic
forecasting; strict propriety identifies an optimal reported distribution
under its assumptions. This does not identify an arbitrary utility number
with a probability. Compare loss orientation, observed outcome availability
and known stakes before using the bridge in P3-02/06.

## S03 — Selecting computations

Nicholas Hay, Stuart Russell, David Tolpin and Solomon Eyal Shimony,
*Selecting Computations: Theory and Applications*, UAI 2012.
[Author-hosted paper](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf),
[2012 archival record](https://arxiv.org/abs/1207.5879).
Inspected: abstract, introduction and formal metalevel decision-model setup.

The paper models choosing computations as a decision problem with computation
costs and subsequent object-level choices. This is a necessary ordinary
metareasoning comparator for P3-07. Importing its results requires checking
the information model and assumptions, not merely recognizing the phrase
“value of computation.”

## S04 — Functional counterfactual dependence

Eliezer Yudkowsky and Nate Soares, *Functional Decision Theory: A New Theory
of Instrumental Rationality*, arXiv:1710.05060, retrieved v2 (2018).
[Paper](https://arxiv.org/pdf/1710.05060).
Inspected: §3, pp. 6–7, and §5, pp. 11–14.

The paper distinguishes replacing a decision function from evaluating another
output of it: a predictor of the original need not predict a replacement.
Its graphical formulation supplies the relevant dependency structure as input.
Use this as a counterfactual-dependence comparison, not as an already supplied
general operator for arbitrary false mathematical premises. P3-04/05 must say
what changes, which uses follow it and what extra information supports that choice.

## S05 — Structural-equation counterfactuals

Joseph Y. Halpern, *Axiomatizing Causal Reasoning*, JAIR 12, 317–337 (2000).
[Paper](https://arxiv.org/pdf/cs/0005030).
Inspected: §2.1, pp. 318–320, modified submodels and the acyclic case.

Specified structural equations permit explicit interventions; acyclicity gives
a unique solution in the stated setting. This is a strong finite ordinary
baseline for changing one designated variable. It does not identify an unknown
logical dependency structure from existing cost observations alone.

## S06 — Ranked revision

Wolfgang Spohn, *Ordinal Conditional Functions: A Dynamic Theory of Epistemic
States* (1988). [Primary scan](https://d-nb.info/110069062X/34).
Inspected by the delegated reviewer: §§4–5, Definitions 4–6; principal retrieved
the same source for this handoff.

Graded disbelief and revision strength are established numeric tools distinct
from probability mass. A cost-ranked repair proposal must be compared to them
and to ordinary weighted repair; its numeric ranking is not sufficient novelty.

## S07 — Counterpossibles

Francesco Berto, Rohan French, Graham Priest and David Ripley,
*Williamson on Counterpossibles*. [Primary article](https://link.springer.com/article/10.1007/s10992-017-9446-x).
Inspected: §§1–2, including possible/impossible-world semantics and selection
constraints; principal retrieved the same source as the delegated reviewer.

Nonvacuous treatments of impossible antecedents already exist. They are a
comparison for the part of P3-04 that cannot be answered just by moving to a
consistent alternative theory. The relevance/selection rule still needs a
specific interpretation in a proposed value-based system.

## S08 — Several uncertain models

Jennifer A. Hoeting, David Madigan, Adrian E. Raftery and Chris T. Volinsky,
*Bayesian Model Averaging: A Tutorial*, Statistical Science 14(4), 382–417 (1999).
[Corrected author-hosted version](https://sites.stat.washington.edu/www/research/online/hoeting1999.pdf).
Inspected: introduction and model-averaging setup.

Ordinary statistics already combines uncertainty over models. This supplies
one comparison for simultaneous model use, without assuming that model
averaging, task-dependent routing and approximate-theory revision are identical.

## S09 — Imprecise expectation models

Gert de Cooman and Filip Hermans, *Imprecise Probability Trees: Bridging Two
Theories of Imprecise Probability* (2008).
[Primary archival record](https://arxiv.org/abs/0801.1196).
Inspected: author abstract only. It describes connections between behavioural
imprecise probabilities and game-theoretic probability. Treat it as a lead for
P3-02's lower/upper expectation comparison; no theorem has been imported.

## Further reading and retrieval limits

The delegated reviewer inspected the publisher's available introduction to
Katsuno and Mendelzon's [*On the Difference between Updating a Knowledge Base
and Revising It*](https://www.cambridge.org/core/books/abs/belief-revision/on-the-difference-between-updating-a-knowledge-base-and-revising-it/8ADFFF65FA776C21E8646D6F4D2434AB).
Its full chapter and a full original AGM reading remain
P3-01 literature work if used. Causal versus logical counterfactuals and revision
versus update must be distinguished in the adopted definitions regardless.

An initial broad search returned many irrelevant results; focused exact-title
queries and direct primary URLs resolved the principal orientation sources.
No absence of search results is used as evidence for originality. Author-hosted
and archival versions must be pinned when importing a theorem. Finite online
learning and bounded proof-search baselines still need exact source contracts
during P3-01/06/08.
