# Targeted primary-source screen

Codex (GPT-6), October 11, 2026. DEVELOPMENT. Locators below describe inspected
scope; no exhaustive novelty audit or imported confirmation theorem.

- Nielsen, Rohwedder, Schewior, *Non-Adaptive Evaluation of k-of-n Functions:
  Tight Gap and a Unit-Cost PTAS*, [v1](https://arxiv.org/html/2507.05877v1),
  §§1.1 and 2. The inspected text optimizes expected evaluation cost under
  known independent bit probabilities; its two-sided domination uses
  probability-ordered injections, rather than comparing two orders on the
  same truth vector. It supplies a much stronger nonadaptive statistical
  comparator than arbitrary fixed orders. The PTAS proof is not imported here.
  Query-price objectives do not price all learner/preparation computation.
- Zong, Lehtonen, Rintanen, *Cost-Optimal Decision Diagrams for Stochastic
  Boolean Function Evaluation*, [v1](https://arxiv.org/html/2606.24672v1),
  §1 and §3 Definitions 1–3. It considers general formulas, positive query
  costs and conditional probabilities from a joint distribution, with offline
  decision-diagram construction. Logical/probabilistic dependence is therefore
  not by itself a novel extension of ordinary SBFE. Only the definitions and
  stated algorithm scope were screened; complexity and performance claims
  were not independently checked or imported.
- Cicalese and Milanic, *Competitive Evaluation of Threshold Functions and
  Game Trees in the Priced Information Model*, [two-page author abstract](https://rutcor.rutgers.edu/Milanic.pdf),
  p.1 second paragraph and bullet 1; p.2 references 5–6. Outcome-dependent
  evaluation prices and competitive certificate evaluation are established
  directions. This abstract identifies ancestors, but does not give enough
  algorithm/proof detail to identify whether the exact pair-cost range
  construction is already present. Priority remains unassessed.

The quick search did not establish a specialized prior exact algorithm for
the same-request pair range. Search absence is not evidence of novelty. The
new elementary [dominance obstruction](comparison_limits.md) already removes
one proposed application without requiring a prolonged literature audit.

## Incremental SAT branch

- [PySAT solver API](https://pysathq.github.io/docs/html/api/solvers.html), module
  description and assumptions example (accessed October 11): supports related
  SAT calls, retained learned clauses, model extraction and assumption cores.
  This establishes a mandatory ordinary incremental comparison; none of those
  basic capabilities is a new S07 mechanism. The documentation also exposes
  solver-specific restrictions, so an assumption-capable solver must be chosen.
- Een and Sorensson, *An Extensible SAT-solver*, MiniSAT author PDF: direct
  fetch timed out. Search-extracted §2 identifies the incremental API but is a
  lead only; no proof or implementation result was imported from this failed
  retrieval. The accessible PySAT API above supports the immediate comparison.

- [PySAT RC2 API](https://pysathq.github.io/docs/html/api/examples/rc2.html),
  module example, `compute`, and `add_clause`: RC2 accepts weighted soft clauses
  and hard CNF clauses, returns an optimal model or `None` for infeasible hard
  clauses, and reports **unsatisfied soft weight**, not the maximized objective.
  The new separation prototype must retain the affine offset when converting
  this reported cost back into a regret value. Incremental additions are
  documented, but changing an old soft objective is not a free supported
  operation in that interface; initial implementation will reconstruct each
  priced separation call. No MaxSAT optimality proof is imported or checked
  merely by reading the API.

## Prediction-assisted finite-population values

- Angelopoulos, Bates, Fannjiang, Jordan, Zrnic,
  [Prediction-Powered Inference, arXiv v4](https://arxiv.org/pdf/2301.09633),
  §1.3 and Appendix B Corollary B.1 (PDF pp.3 and 23–24). The inspected mean
  construction corrects a prediction average with a confidence interval for
  prediction error; the finite-population corollary already covers fixed
  unlabeled populations. S08 cannot claim that basic rectification as new.
  A priced sequential decision service still needs its own sampling and
  stopping contract; fixed-time asymptotic intervals are not imported.
- Waudby-Smith and Ramdas,
  [Confidence sequences for sampling without replacement](https://proceedings.neurips.cc/paper_files/paper/2020/file/e96c7de8f6390b1e6c71556e4e0a4959-Paper.pdf),
  §2.1 Proposition 2.1, §2.2 Theorem 2.1 and §2.3. This is a stronger ordinary
  sequential comparator than a repeated fixed-time interval: a working
  full-support beta-binomial distribution can yield simultaneous coverage for
  a fixed finite binary population. Its working distribution is not a claim
  that the unknown truth count was sampled from that prior. S08 should use or
  compare this confidence-sequence construction and charge its computation.
  Support-changing boundary cases should be expressed through the sufficient
  nonnegative-supermartingale inequality rather than silently assuming common
  positive likelihood support. No broader statistical theorem is imported.
