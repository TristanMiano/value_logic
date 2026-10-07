# P3-01 — primary definitions and comparison contracts

Contributor: **ChatGPT (GPT-6 Astra Pro)**, with same-model internal,
nonblind delegated reconstruction. Accessed October 7, 2026 UTC.
This record upgrades selected entries of the [planning orientation](00_orientation.md).
It is not a comprehensive literature or priority review.

The compact source cards and their formulas are preserved in the linked
review notes. This index names the exact imported interface and the reading
boundary without repeating those cards. Our contract and examples are separate
derivations/adaptations; none is a claim to have independently reconstructed
every proof of these papers.

## Source index

| ID | Primary source and inspected version | Exact locators | Reading / import disposition |
|---|---|---|---|
| S01 | Garrabrant, Benson-Tilsen, Critch, Soares and Taylor, [Logical Induction](https://intelligence.org/files/LogicalInduction.pdf), 2016, 131-page author PDF; selected passages compared with [arXiv v5](https://arxiv.org/html/1609.03543v5), December 7, 2020 | Definitions 3.0.1, 3.1.1–3, 3.2.1–4, 3.3.1, 3.4.3–5, 3.5.1; §4 assumptions; Definitions 4.8.1–2; §5.5; §7.4; Appendices G.7–G.8 | Selected definitions/statements reconstructed in [induction note §1](../work_logs/P3_01_2026-10-07_S1/reviews/induction_sources.md), with the [import audit](../work_logs/P3_01_2026-10-07_S1/reviews/li_desiderata_import_audit.md) and S16 correction controlling scope. No full construction-proof import. |
| S02 | Gneiting and Raftery, [Strictly Proper Scoring Rules, Prediction, and Estimation](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf), JASA 102(477), 359–378, 2007 | §1 propriety definition; §§2–3, including quadratic score | Definition reconstructed below. No universal calibration guarantee imported. |
| S03 | Hay, Russell, Tolpin and Shimony, [Selecting Computations: Theory and Applications](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf), UAI 2012 | §2, Definitions 1–3; computation-history state, transition and stopping reward | Metalevel probability/decision model reconstructed below. Specialized sampling theorems not imported. |
| S04 | Yudkowsky and Soares, [Functional Decision Theory](https://arxiv.org/pdf/1710.05060), retrieved arXiv v2, 2018 | §3 alternative-function discussion; §5 equations (2)–(4), footnote 9 | Dependency/operation contract reconstructed in [counterfactual note §1](../work_logs/P3_01_2026-10-07_S1/reviews/counterfactual_sources.md). |
| S05 | Halpern, [Axiomatizing Causal Reasoning](https://arxiv.org/pdf/cs/0005030), JAIR 12, 317–337, 2000; arXiv v1 | §§2.1–2.3, pp. 318–321 | Structural intervention, solution and modality definitions reconstructed in the counterfactual note. |
| S06 | Spohn, [Ordinal Conditional Functions](https://d-nb.info/110069062X/34), 1988 scan | §§4–5, Definitions 4–6, pp. 115–117 | Ordinal rank and nonempty-event update definitions reconstructed in the counterfactual note. |
| S07 | Berto, French, Priest and Ripley, [Williamson on Counterpossibles](https://link.springer.com/article/10.1007/s10992-017-9446-x), online 2017; JPL 47, 693–713, 2018 | §§2.1–2.3, especially interpretation and selection constraints; §3.1, classical-closure objection | Selected semantics reconstructed in the counterfactual note. No universal arithmetic evaluator imported; presentation invariance is not unrestricted classical equivalence of impossible antecedents. |
| S08 | Hoeting, Madigan, Raftery and Volinsky, [Bayesian Model Averaging: A Tutorial](https://sites.stat.washington.edu/www/research/online/hoeting1999.pdf), corrected author version, 1999 | Introduction and model-averaging setup | Selected mixture formula/assumptions inspected; no model-selection performance theorem imported. |
| S09 | de Cooman and Hermans, [Imprecise Probability Trees: Bridging Two Theories of Imprecise Probability](https://arxiv.org/pdf/0801.1196v1), January 8, 2008, 30-page preprint | §§2.1–2.3, P1/P2/C; §3.1, D1–D4; §3.2, equations (4)–(5), Proposition 2; §4, D5' and Theorems 3/6/7; §8–9 discussion | Selected conditional-price, local natural-extension and concatenation interfaces reconstructed in the tree note below. Earlier abstract-only orientation is superseded for these selected passages. No full proof, learning or runtime theorem imported. |
| S10 | Freund and Schapire, [A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting](https://cseweb.ucsd.edu/~yfreund/papers/adaboost.pdf), JCSS 55(1), 119–139, 1997; author manuscript | §2; Figure 1, printed p. 4; Theorem 2/Corollary 3, p. 5 | Hedge/full-feedback card and direct Brier-mixture specialization in [induction note §§1–2](../work_logs/P3_01_2026-10-07_S1/reviews/induction_sources.md). Algorithm/bound visually checked because PDF text encoding is poor. |
| S11 | Fagin and Halpern, [Belief, Awareness, and Limited Reasoning](https://www.cs.cornell.edu/info/people/halpern/papers/awareness.pdf), Artificial Intelligence 34, 39–76, **1988** on printed title page | §5, pp. 52–54; §6 local reasoning; §7, pp. 61–63 | Explicit versus implicit belief/awareness and temporal interface in induction note. DOI's embedded `87` is not the publication-year field. |
| S12 | Halpern and Pucella, [Probabilistic Algorithmic Knowledge](https://www.cs.cornell.edu/home/halpern/papers/probalgk.pdf), LMCS 1(3:1), 2005 | §§2–3, §4 state-access discussion, §5.3 reliability | Procedure/knowledge distinction in induction note. [Publisher record](https://lmcs.episciences.org/2261) supplies the date, not the manuscript's placeholder header. |
| S13 | Halpern and Pucella, [Characterizing and Reasoning about Probabilistic and Non-Probabilistic Expectation](https://www.cs.cornell.edu/home/halpern/papers/expectation.pdf), JACM, 2007 author manuscript | §§2.1–2.4; Theorems 2.2, 2.4, 2.9, 2.13; Example 2.11; §3.2; Theorem 4.1 | Compact functional/representation card in [expectation note §1](../work_logs/P3_01_2026-10-07_S1/reviews/expectation_sources.md). Selected definitions/statements and finite argument inspected; no wholesale axiomatization import. |
| S14 | Joulani, György and Szepesvári, [Online Learning under Delayed Feedback](https://proceedings.mlr.press/v28/joulani13.pdf), ICML/PMLR 28(3), 1453–1461, 2013 | Figure 1; §3.1, Algorithm 1 BOLD and Theorem 1 | Exact selected regret/delay assumptions in induction note. Active paid discovery is a separate problem. |
| S15 | Yao, Vehtari, Simpson and Gelman, [Using Stacking to Average Bayesian Predictive Distributions](https://arxiv.org/pdf/1704.02030), retrieved arXiv v3, September 16, 2017; later journal publication 2018 | §§1.1–1.3; §2.1 equations (2.1)–(2.3); §2.2 read for boundary | Predictive-combination definition inspected; asymptotic results not imported into logical forecasting. |
| S16 | A. M. Berns, [Formalized Agent Foundations](https://github.com/A-M-Berns/Formalized-Agent-Foundations/tree/367d1e42bf104706ff28d8a40492b9ce95c98da0), immutable inspected commit `367d1e42bf104706ff28d8a40492b9ce95c98da0` | `LogicalInduction/notes/paper-errata.md`, PE1–PE9 as source warnings; `Properties/FinitePerturbations.lean`, `FiniteSupportPerturbation`; `Construction/Freeze/Oracle.lean`, `lic_iff_of_finiteSupport`; further exact endpoints in the reviews | Primary correction/code declarations inspected; no Lean build or full formalization audit. The finite-coordinate argument needed here is reconstructed independently. See the correction card below. |
| S17 | Albert, Arenas and Puebla, [An Incremental Approach to Abstraction-Carrying Code](https://cliplab.org/papers/inc-acc-lpar06.pdf), LPAR/LNCS 4246, 377–391, 2006; 15-page author manuscript | §§3.1–3.2, Definitions 1–2; §4; §5 correctness statement and §6 storage discussion | Answer/dependency tables, incremental certificate and checking interfaces inspected; no full correctness proof imported. Already cited in phase two. |
| S18 | Perdomo, Zrnic, Mendler-Dünner and Hardt, [Performative Prediction](https://proceedings.mlr.press/v119/perdomo20a/perdomo20a.pdf), ICML/PMLR 119, 7599–7609, 2020 | §§2.1–2.2, Definitions 2.1/2.3; §1.2 fixed distribution-map scope; §3 assumptions read for boundary | Performative risk and stability definitions inspected. They are different targets; no convergence theorem imported for our versioned self-model. Already an inspected phase-two comparator. |
| S19 | Zhao, Kim, Sahoo, Ma and Ermon, [Calibrating Predictions to Decisions: A Novel Approach to Multi-Class Calibration](https://proceedings.neurips.cc/paper_files/paper/2021/file/bbc92a647199b832ec90d7cf57074e9e-Paper.pdf), NeurIPS 2021 | §§2.1–3.1, Definitions 1–2, Proposition 1; Definitions 3–4; §4.2 Proposition 2; §§4.3–4.4 | Decision-relative, population-average calibration reconstructed below. Sample/computation distinction inspected; no guarantee imported for paid or unresolved logical labels. Already cited in phase two. |
| S20 | Zilberstein and Russell, [Optimal Composition of Real-Time Systems](https://people.eecs.berkeley.edu/~russell/papers/aij-anytime.pdf), Artificial Intelligence 82, 181–213, 1996; 38-page author manuscript | Definitions 2.1–2.6; §§2.2.1–2.2.3; §4 setup; Theorems 4.6–4.7; §§4.3–4.4 | Performance-profile/acquisition interfaces and static composition boundaries inspected. No theorem about arbitrary learned changing controllers imported. Already an inspected phase-two comparator. |
| S21 | Hennig, Osborne and Girolami, [Probabilistic Numerics and Uncertainty in Computations](https://arxiv.org/pdf/1506.01326v1), June 3, 2015 author postprint; Proceedings A 471, 20150142 | PDF §2(a)–(c), equation (2.5); §3(a)–(d); HTML §2.1–2.3, equation (5), §3.1–3.4 | Computation as inference, acquisition and pipeline uncertainty interfaces inspected. No calibration, convergence or runtime guarantee imported. Own scale calculation and a local printed-normalization caveat are in the linked note. |
| S22 | Hutter, Lloyd, Ng and Uther, [Probabilities on Sentences in an Expressive Logic](https://www.hutter1.net/publ/problogic.pdf), 52-page September 12, 2012 preprint, arXiv:1209.2620v1; journal publication 2013 | Definitions 17/20/26, printed pp.9/10/14; Proposition 19, p.9; Proposition 21, p.11; Theorem 27, pp.14–15; §8, pp.43–44 | Selected coherent sentence-probability and conditional-confirmation definitions/statements inspected. Efficient bounded refinement and counterpossible consequences are not supplied by these imports. |

## S01/S16 — exact import and correction boundaries

Definition numbers in this record follow the author PDF. The rendered arXiv
v5 HTML has numbering drift in the early definitions: for example its named
Gamma-complete definition is displayed as 3.2.3, where the author PDF has
3.2.4. Use the definition name and stated formula when crossing versions.
The source's first-order theory convention includes the logical axioms needed
to use its Boolean prime-sentence calculus; do not omit them when declaring
a Gamma-complete proof enumeration.

The original finite-day perturbation claim is not imported. S16 reports a
refutation based on persistent historical-price advice and declares a corrected
finite-coordinate preservation theorem. The inspected commit has tree
`397e61e644547031ee90b58a20849358ed4b48df`, observed October 7, 2026 at
01:26:15 UTC. Its `FreezeOracle.lic_iff_of_finiteSupport` requires two computable
markets, the same deductive process and finitely many changed dated quotes.
No residual sentence-syntax or caller patch-certificate hypothesis appears in
that signature. The pinned prose retains stale references to such a restriction
and to a stronger soundness premise than the counterexample's actual code;
the [scope review](../work_logs/P3_01_2026-10-07_S1/reviews/finite_perturbation_scope.md)
records the discrepancies and inspected declarations.

This is acknowledged prior work, not a P3-01 discovery. The formalization's
verification claims remain attributed to that project. Our one-quote separator
uses the independently reconstructed bounded-cash-difference argument in
[evidence boundaries §3](../foundations/01_evidence_boundaries.md), so does not
depend on a full audit of the refutation or the unrestricted original theorem.

Other selected imports also retain their exact interfaces. Definition 4.8.1
requires a provably existing unique bounded variable; its earlier §2 shorthand
alone is weaker. The finite `E_n` is an average of threshold-sentence prices,
not automatically an exactly linear coherent expectation from a joint law.
Calibration/unbiasedness has explicit sequence, weighting and feedback
conditions; introspection has a representation/quotation contract. S16's
PE2 and PE6–PE9 are relevant correction leads, not blanket declarations that
the corresponding theorems are false. The [desiderata import audit](../work_logs/P3_01_2026-10-07_S1/reviews/li_desiderata_import_audit.md)
gives the precise limits. Appendix G.8's use of G.7 is recorded; no downstream
conditioning-closure theorem is imported here.

Finally, §7.4 already proposes a resource-constrained controller consulting a
partly trained logical inductor and sometimes allocating further training to
it. The paper labels this speculative. Thus the architecture is anticipated,
while a particular useful bounded construction or cross-component guarantee
remains a possible research target. Section 7.4 also gives no guarantee of
satisfactory counterpossible beliefs. These are source-specific statements,
not an assertion about all work published by 2026.

## S02 — fixed-outcome propriety, in loss orientation

For a forecast distribution `P`, outcome `x` and score `S(P,x)`, the source
uses a reward orientation. Its strict propriety condition is
`E_Q S(Q,X) > E_Q S(P,X)` for `P != Q` in the stated distribution class.
Negating the score gives a loss minimized in expectation by reporting `Q`.
The outcome law is held fixed across the reports being compared. This is an
elicitation/forecast-evaluation property, not an algorithm that learns `Q`.
See EX11 for why changing the report-induced outcome law requires another
analysis. The score's sign, outcome availability and distribution class must
travel with any import.

## S03 — a metalevel decision model, in cost orientation

Definitions 1–3 supply jointly modeled action utilities and possible
computation outcomes. A state is a finite history of acquired results. Available
actions are further computations or stopping. A computation incurs its cost
and transitions according to its conditional outcome law; stopping selects the
largest conditional expected utility. Reversing utility signs produces an
expected-cost minimization comparator. The model of future computational
outcomes is an input to this decision problem. Supplying it does not prove
that a practical learner knows or can cheaply construct it. We import this
interface, not every specialized optimality or sampling result in the paper.

## S08/S15 — several useful models already have ordinary treatments

S08's predictive mixture uses model-conditioned predictions and posterior model
weights. S15 instead defines a predictive combination selected by a
cross-validated proper score, with nonnegative weights summing to one. Its
motivation explicitly includes situations where no candidate is the exact
data generator. These are useful comparison interfaces for model plurality;
neither selected definition supplies a bounded learner for arithmetic truth.
For Q3, the ordinary combined method must also be allowed scoped approximations,
task-specific routing and the same model library. Its comparison cannot be
limited to an assumption that exactly one supplied scientific model is true.

## S17/S20 — acquired profiles and reusable certificates are ordinary tools

S17 retains answer and dependency-arc tables to support incremental checking.
Its §3.2 warns that compression useful for one-shot checking can discard
information needed for later checking. Retention, provenance and changes
therefore already have a substantive ordinary comparator.

S20's conditional performance profile maps input quality and allocated time
to an output-quality distribution. Acquisition may be analytic or statistical;
the conditioning features, population, representation and approximation error
matter. Its static functional-composition treatment assumes by-value,
side-effect-free functions with specified profiles; the local optimality result
uses tree structure and input monotonicity. Repeated subexpressions and hidden
output quality require separate treatment. These selected interfaces permit an
ordinary procedure-quality controller, not a free model of the value of thinking.
See the [profile/access review](../work_logs/P3_01_2026-10-07_S1/reviews/acquisition_and_profile_boundary.md).

## S18/S19 — forecast consumers and induced outcomes change the guarantee

S18 defines risk under the outcome distribution induced by deploying a report
or model. Its stability concept instead optimizes the report against a fixed
induced distribution. These are generally different. The source's distribution
map is held fixed; an arbitrary history-dependent self-modifying reasoner needs
another model. EX11 is an inherited finite illustration, not a new principle.

S19's calibration definition equates population-average predicted and actual
loss for a specified loss class and associated report-based decision rules.
Its setup excludes direct feature dependence in the loss and gives the decision
rule access to features through the probability report. The exact/approximate
definitions therefore do not imply individual correctness or correctness after
arbitrary stake/context weighting. Its polynomial sample statement also leaves
an inner optimization problem; practical relaxed search is not an exact free
oracle. [CB02](../foundations/01_composition_boundaries.md#cb02-decision-calibration-has-a-consumer-and-population-scope)
reconstructs the two-case boundary. We import these comparison definitions,
not a statistical guarantee for our future logical-query stream.

## S21/S22 — numerical uncertainty and logical probability are established comparisons

S21 treats uncertainty about a deterministic computation through an explicit
probability model and an acquisition rule; it also discusses uncertainty and
effort allocation across computational pipelines. The
[scale diagnostic](../work_logs/P3_01_2026-10-07_S1/reviews/probabilistic_numerics_boundary.md)
shows, under its stated exact-observation Gaussian assumptions, why matching a
posterior mean need not match posterior variance or the modeled value of another
computation. This is our elementary comparison calculation, not a learned
calibration result. The note records a local normalization discrepancy in an
illustrative equation without relying on it or claiming a published erratum.

S22 already defines coherent degrees of belief in logical sentences and gives
an asymptotic confirmation result with explicit enumeration, prior and
continuity hypotheses. Its illustrative agent includes incomputable operations.
The [source card](../work_logs/P3_01_2026-10-07_S1/reviews/probabilities_on_sentences_boundary.md)
separates that idealized service from a budgeted implementation. Ordinary
positive-probability conditioning does not define contradiction-conditioning.
Neither assigning sentence probabilities nor attaching expected costs alone
supplies a phase-three contribution.

## S09 — local tree models and shared uncertainty

The [tree source note](../work_logs/P3_01_2026-10-07_S1/reviews/imprecise_tree_source.md)
reconstructs the selected interface between lower/upper expectations and
sequential prediction. Conditional prices are defined on nonempty events,
without requiring division by an event probability. This does not give a
semantics for conditioning on an empty logical contradiction. The local
conditional assessments are held at the root, not arbitrary beliefs learned
later by an adaptive program.

The source's concatenation equality is for the natural extension constructed
from its local assessments. Our two-law example shows why applying independent
branchwise extrema can enlarge a richer supplied global model and alter an
ex ante decision. This is a preservation obligation for either ordinary or
value-based implementations, not a counterexample to the source theorem.
The source's conic feasible-gamble assumptions also do not automatically cover
a controller's hard computation budget. A separate bridge is needed before
claiming that its uncertainty semantics supplies an executable bounded policy.

## What the reconstructed comparisons rule out

Our assessment is that the candidate must earn any claimed delta beyond
existing expectation semantics, bounded explicit belief, online prediction,
metareasoning and specified intervention/repair. A full coherent functional,
selected retained cost queries and a learned prediction are different objects.
So are a joint credal set and intervals for its individual events. EX12 turns
that last distinction into a concrete decision test. These observations sharpen
the question; they do not establish that the integration is either novel or
unpromising.

The most useful next comparison work is targeted: P3-02 must confront S13's
finite representation results while identifying what restricted retained queries,
precision, paid access or transport add. P3-06 must specify which exact online
duties it seeks. P3-04/05 must supply the counterfactual selection information
their answer uses.

## Retrieval and reconstruction limits

Broad searches were noisy. An initially guessed Hedge PDF was a different
discussion paper; it was not used after its identity was inspected. The correct
paper was obtained through the author's publication index. PDF extraction of
Hedge was garbled, so page images were used for its formula. The full primary
Katsuno–Mendelzon chapter remained unavailable in the attempted retrievals;
only the publisher introduction was inspected, and no AGM/KM theorem is imported.
S09 initially remained abstract-only; selected passages of its complete
version-pinned preprint were subsequently inspected as recorded above.
A later reopening of the version-suffixed URL returned a retrieval error;
the unsuffixed PDF then succeeded and displayed the same v1/January 8, 2008
identifier. These limits are not evidence of originality.

The principal reopened the primary sources used in the canonical interpretation;
the reviewers reconstructed selected definitions and the finite witnesses
independently within the same model family. This is useful internal checking,
not a blind external replication. The raw review notes retain their original
snapshots and resource observations.
