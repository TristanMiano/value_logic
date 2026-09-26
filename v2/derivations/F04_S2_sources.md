# F04 S2 — targeted primary-source comparison

Accessed September 26, 2026. Continuation of [the S1 source record](F04_sources.md).
This is not a reopened F03 audit. Source descriptions below are scoped to inspected
passages; no whole-paper independent verification or priority claim is made.
The [derivation note](01a_nonlinear_and_reflective_reconstruction.md) supplies
standalone proofs of the finite constructions used in this session.

## N1 — finite ReLU geometry and behavior along unbounded rays

Matthias Hein, Maksym Andriushchenko, Julian Bitterwolf, *Why ReLU Networks Yield
High-Confidence Predictions Far Away From the Training Data and How to Mitigate
the Problem*, CVPR 2019, pp. 41–50.

- Identity: <https://openaccess.thecvf.com/content_CVPR_2019/html/Hein_Why_ReLU_Networks_Yield_High-Confidence_Predictions_Far_Away_From_the_CVPR_2019_paper.html>
- Inspected text: <https://arxiv.org/html/1812.05720v2>, section 2, Lemma 3.1,
  Theorem 3.1, and Appendix A's lemma argument.

The source explicitly represents a finite ReLU network by affine formulas on
polyhedral activation regions. Lemma 3.1 shows that a fixed ray eventually
remains in one such region. The softmax-confidence theorem has additional slope
conditions. Our bounded-difference argument for the all-zero-bias network is
proved separately; the source's confidence theorem is not imported as a theorem
about utility or the adequacy of an extrapolated loss. The counterexample to
using a single observed activation region agrees with this geometric baseline.
The paper's confidence result is not a claim about all bounded input domains.

The CVF PDF fetch failed. Legible primary arXiv HTML, not a search snippet,
supports the statements used here. No figure or PDF image from this paper was
needed or treated as inspected. Search phrases included zero-bias bounded
ReLU differences and asymptotic ReLU behavior. This limited search establishes
neither novelty nor absence of a closer expression of our elementary criterion.

## N2 — feedback-aware prediction, stability and optimization

Juan Perdomo, Tijana Zrnic, Celestine Mendler-Dünner, Moritz Hardt,
*Performative Prediction*, ICML 2020, PMLR 119, pp. 7599–7609.

- Primary record: <https://proceedings.mlr.press/v119/perdomo20a.html>
- Inspected paper: <https://proceedings.mlr.press/v119/perdomo20a/perdomo20a.pdf>
- Locators: sections 2.1–2.2, Definition 2.1, Definition 2.3 and Remark 2.4;
  Example 3.4 and Theorem 3.5 were read to delimit the convergence comparison.
  PDF pages indexed 2 and 3 were successfully viewed.

This is a closer baseline for the report-induced outcome distribution than
unrestricted logical reflection alone. The source distinguishes minimizing
loss under the distribution caused by deployment from minimizing against a
frozen deployment-induced distribution. The latter fixed-point condition need
not be optimal for the former objective. Its retraining convergence theorem
requires stated regularity, curvature and sensitivity conditions.

Our inequality `H(r)<=r` is a uniform report constraint, not automatically the
source's performative-stability equation. We add explicit uncertainty over
branch failure rates, a common deployable report and a finite constrained
optimizer, all proved in the note. No retraining theorem, learned distribution
map, empirical calibration, or unrestricted reflective ability is claimed.

## N3 — causal rather than observational explanation

Atticus Geiger, Hanson Lu, Thomas Icard, Christopher Potts,
*Causal Abstractions of Neural Networks*, NeurIPS 2021, arXiv:2106.02997v2.

- Primary text: <https://arxiv.org/html/2106.02997v2>
- Reinspected: section 3, particularly equations (1)–(3) and the distinction
  between an alignment hypothesis and its interchange-intervention test.

The source tests aligned high- and low-level counterfactual behavior rather
than treating probe accuracy as causal evidence. Our common-scale cost example
is a new finite design control, not a result about the networks in that paper.
It differentiates competing high-level factorizations with identical ordinary
outputs. No training, alignment search or high-/low-level abstraction has been
executed here. The proposed control does not establish either factorization in
an unconstrained MLP.

## Disposition

Retain all three as baselines and interpretation constraints. N2 strengthens the
nearest-antecedent entry for OPP-03. Source facts are distinct from the proofs of
F04-C09–C15 and their finite tests. None of these checks selects a calculus,
imports unrestricted completeness, or justifies a claim of a newly discovered
neural mechanism. All source windows mixed with retrieval are separately
identified in session accounting rather than treated as measured derivation.
