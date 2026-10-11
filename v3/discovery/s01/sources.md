# C001 source comparisons

Codex (GPT-6), October 11, 2026. DEVELOPMENT source screening; not exhaustive
priority review. Primary texts were retrieved through the web tool. The first
attempt at the older paper's HTML v4 failed; its PDF v2 was accessible.

| ID | Primary text and locator | Relevant established construction and import boundary |
|---|---|---|
| DS01 | Erlebach, de Lima, Megow, Schlöter, [Learning-Augmented Query Policies](https://arxiv.org/pdf/2011.07385), PDF v2, §§1–2, pp. 1–6 | Untrusted value predictions guide exact queries, with consistency/robustness and structural error measures. Their §2 explicitly leaves time/space unrestricted and measures query count. S02's basic idea is established here; no priority for combining fallible predictions and correct answers. A complete runtime/inference/checking bill needs additional analysis. Their minima/sorting/MST guarantees are not threshold-function theorems. |
| DS02 | Deshpande, Hellerstein, Kletenik, [Approximation Algorithms for Stochastic Boolean Function Evaluation and Stochastic Submodular Set Cover](https://arxiv.org/pdf/1303.0726), abstract and problem definition | Paid bit evaluation under a given product distribution; a 3-approximation for Boolean linear thresholds. This is a strong conventional family for S02/S03. We do not infer a known product distribution for unresolved deterministic mathematics or import an expectation guarantee under model misspecification. Full algorithm proof has not been reconstructed. |
| DS03 | Gkenosis, Grammel, Hellerstein, Kletenik, [The Stochastic Boolean Function Evaluation Problem for Symmetric Boolean Functions](https://arxiv.org/pdf/2111.08793), PDF v3, §3 pp. 4–5 and §7 pp. 10–11 | Describes the classical Salloum–Breuer–Ben-Dov k-of-n rule: intersect the first k coordinates ordered by c/p with the first n-k+1 ordered by c/(1-p), query a member, recurse. It is an optimal expected-cost conventional comparator under the stated independent known probabilities. The paper distinguishes knowing the answer from knowing all bit values in verification. We will implement the rule as a comparison, not claim it as new. |
| DS04 | [CASP: Learning-Augmented Offline Approximation with Verifiable Certificates and Bounded-Loss PAC Guarantees](https://arxiv.org/html/2607.14545v1), §§3, 6–7 | Recent preprint explicitly combines predicted structure, verified certificates and conventional fallbacks. A topical overlap requiring attention before novelty claims. Its offline approximation/solution-quality setting does not by itself establish savings in total mathematical computation. Only relevant definitions and scope were screened; its empirical and theorem claims are not independently verified here. |

Current conclusion: retain S02 as a potential *resource-aware useful
integration/application*, with a substantial comparison obligation. Reject
the broad novelty hypothesis that safe computation guided by fallible
predictions is new. No candidate is promoted by this screening.

For S04, Javdani et al., [Near Optimal Bayesian Active Learning for Decision
Making](https://publications.ri.cmu.edu/storage/publications/pub_files/2014/4/javdani14hec_extended.pdf),
§2 pp. 2–3, specifies a hypothesis-to-test-response map, overlapping acceptable
decision regions, and stopping when all remaining hypotheses belong to one
region. This displaces any novelty claim for the basic decision-only
acquisition target. The present mixed-regret/LP example is a specialization;
the HEC approximation guarantee has not been reconstructed or imported.

The quadratic fixed-order cost-difference algorithm in comparison.md was
derived after these screens. Its closest specialized-algorithm literature
search remains an explicit next obligation. DS03 supplies the threshold
evaluation setting, not an asserted prior proof of that pair-policy result.
