# Primary-source comparison for the s08 redirection

**Codex (GPT-6), October 13, 2026 UTC. DEVELOPMENT literature record.**
These are inspected primary sources, with exact import boundaries. Search
results about unrelated meanings of "backbone" were discarded.

- Biere, Froleyks and Wang, [CadiBack: Extracting Backbones with CaDiCaL](https://drops.dagstuhl.de/opus/volltexte/2023/18465/pdf/LIPIcs-SAT-2023-3.pdf),
  SAT 2023, sections 2–4, Algorithm 1 on printed p. 3:4. A backbone literal
  holds in every satisfying assignment. Candidate filtering, model rotation
  and chunked complement queries already acquire many such facts. Therefore
  proving several mandatory coordinates with one grouped query is not a new
  extraction principle. A value-directed stopping target still needs a paid
  comparison with these partial extraction capabilities.
- Francia-Carramiñana et al., [Backbones in Pseudo-Boolean Optimization: Extraction and Analysis](https://hochbaum.ieor.berkeley.edu/html/pub/Native_Backbone_Extraction_for_Pseudo_Boolean_Optimization.pdf),
  inspected author-hosted manuscript, sections 2.1 and 3, Algorithm 1.
  The optimization backbone concerns all optimal solutions at the specified
  objective. Their extraction first fixes the attained optimal value and then
  performs backbone queries. This is not a certificate that the same facts
  hold for all original feasible models or after arbitrary weight changes.
  No publication-date or current benchmark-superiority claim is inferred from
  the search engine's displayed date.
- Niskanen, Berg and Järvisalo, [Enabling Incrementality in the Implicit Hitting Set Approach to MaxSAT Under Changing Weights](https://drops.dagstuhl.de/storage/00lipics/lipics-vol210-cp2021/LIPIcs.CP.2021.44/LIPIcs.CP.2021.44.pdf),
  CP 2021. The abstract and section-5 passage inspected here support retained
  objective-independent cores and changing objectives as established solver
  territory; the repository's [earlier detailed source reading](../s07/s29_affine.md)
  identifies sections 4.1–4.3 and the fixed-feature versus weight-dependent
  hardening distinction. A newly proved value-quotient rule must be compared
  with ordinary simplification and safe objective-dependent fixing.
- Bogaerts et al., [Certified Symmetry and Dominance Breaking for Combinatorial Optimisation](https://ojs.aaai.org/index.php/AAAI/article/download/20283/20042),
  AAAI 2022, section 3, equation (5), Proposition 3. Redundance-based
  strengthening uses a witness substitution that preserves feasibility and
  does not worsen the objective. It can retain an optimum without preserving
  every feasible solution. This is the direct antecedent of the improving-map
  construction below; the witness principle is imported, not claimed new.
  The [current official VeriPB overview](https://veripb.org/overview.html)
  distinguishes derivable and equioptimal outputs and documents the separate
  objective proof obligation. This session does not claim to run VeriPB.

## Constructive inference

An additional direct antecedent was identified during development:
Shekhovtsov, [Maximum Persistency in Energy Minimization](https://cmp.felk.cvut.cz/~shekhovt/publications/shekhovtsov-2014-improving-mappings-CVPR-final-copy.pdf),
CVPR 2014, sections 3–5, especially the relaxed improving condition and
equations (12)–(14). Improving-map verification is treated through a marginal
polytope relaxation; the map can preserve an optimum while removing labels.
The [later author manuscript](https://cmp.felk.cvut.cz/~shekhovt/publications/2017-maximum-persistency-IRI.pdf)
describes incremental verification with progressively relaxed requirements on
the dual solver. These are stronger comparisons than nominal Boolean backbone
extraction. The present star example does not establish novelty over this
framework. The current cost-region, tolerance and paid-observation extension
needs its own useful consequence rather than credit for the imported map idea.

The full source may have no nontrivial affine equalities even when a checked
cost-nonincreasing map sends every feasible model into a lower-dimensional
representative set. A quotient of that representative set can preserve the
optimum. This is a different premise from falsely treating an optimal-solution
backbone as a fact about every feasible model.

The proposed repository extension attaches a public cost region to the map's
objective guard, keeps that guard valid under observation refinement, and
allows an explicitly bounded cost increase to consume regret tolerance. The
useful question is whether these typed guards enable a smaller paid
observation target while retaining all source and checking costs. Established
dominance preprocessing and robust optimization receive the same map and
guard in the comparison. Neither the inference nor these source readings
establish novelty or a material complete-cost win.

## Action-audit graph comparison (October 14)

Halldorsson and de Lima, [Query-Competitive Sorting with Uncertainty](https://arxiv.org/pdf/2012.09475),
v2, sections 1–4, especially Definition 1, Lemma 2, Facts 5–6 and Theorem 7,
already use dependency edges and minimum-cost vertex covers to characterize
sufficient query sets. Their interval sorting duty differs from our doubled
binary edge actions, and one queried endpoint need not resolve their edge.
The connection between observation certificates and graph covers is therefore
established prior art. Our residual maximum-cut equality is a development
derivation for the stated regret source, not a general first use of covers
for decision-relevant queries. This source also distinguishes offline
verification sets from oblivious and adaptive online queries; our result's
outcome-independent sufficient-set cost should not erase those distinctions.

The search identified a directly relevant weighted partial vertex-cover
manuscript at [OSTI](https://www.osti.gov/servlets/purl/1427211), but the PDF
request returned HTTP 502. Its search excerpt is a lead, not an inspected
theorem. The ordinary tree-knapsack recurrence here has a direct induction
proof and is not attributed as a new graph algorithm. No favorable comparison
against a cost-axis implementation establishes superiority over the equally
available residual-axis ordinary dynamic program.

Bampis et al., [Orienting (Hyper)graphs Under Explorable Stochastic Uncertainty](https://arxiv.org/pdf/2107.00572),
2021 manuscript, section 1 and Appendix C.1 (Lemma C.1), studies minimum-value
identification in overlapping uncertain sets. Its star analysis compares
center-first and leaves-first vertex-cover algorithms with an offline optimum
and explicitly uses independence of mandatory events. Our three-level star
is a restricted instance with ties and a different exact adaptive expected-fee
formula. The general task and graph-cover comparison are already established.
The formula's leaf order is also the standard AND evaluation order already
derived and sourced in [S21](../s03/failed_queries.md). Neither that ordering
nor using stochastic source knowledge to reduce query cost is claimed new.

Chaplick et al., [Query Minimization under Stochastic Uncertainty](https://www.ime.usp.br/~mslima/latin-stochastic-queries.pdf),
author-hosted conference manuscript, sections 1 and 2.1, is a closer exact
planning comparison. It assumes independent uncertain values and computable
interval probabilities, decomposes sorting into proper interval-graph
subproblems and constructs an optimal adaptive query tree by dynamic
programming. The manuscript's complexity differs from the later journal
abstract; no version-mixed complexity claim is used here. Our three-level
path recurrence uses a more restricted source and only ordinary/forced
endpoint interval states. It does not establish first use of interval
decomposition or adaptive DP for cost queries.

Shafer, Shen, Vereshchagin and Vovk,
[Test Martingales, Bayes Factors, and p-Values](https://probabilityandfinance.com/articles/33.pdf),
sections 2, 3.1 (maximal inequality (2)) and 8.2 (mixture likelihood example),
supplies the likelihood-ratio martingale and time-uniform testing principles.
The finite-model set in this session applies those ordinary principles to
the conditional likelihood of adaptively selected physical receipts. Query
choice must be predictable from already observed information and its law
must be common across the compared source models. The particular Markov
forward numerator and typed acquisition-policy integration are the local
construction; the probability coverage principle is imported. Model-family
membership remains a premise, not a conclusion of a large relative likelihood.

Javdani et al., [Near Optimal Bayesian Active Learning for Decision Making](https://www.ri.cmu.edu/pub_files/2014/4/javdani14hec_extended.pdf),
extended AISTATS 2014 paper, section 2 equations (1)–(2) and section 3,
already formulates overlapping decision regions and stopping when every
remaining hypothesis lies in one acceptable region. Their tests have
deterministic outcomes given a hypothesis and their theorem concerns a
Bayesian query policy. The local construction substitutes an all-time
confidence set from stochastic compulsory receipts and exact expected-fee
policy regions. No first discovery of decision-region stopping, nor transfer
of their HEC approximation guarantee to this service, is claimed.

Titi and Garloff, [Matrix methods for the tensorial Bernstein form](https://www-home.htwg-konstanz.de/~garloff/AMC-2.pdf),
Applied Mathematics and Computation 346 (2019), introduction, section 3 and
section 5.1, supplies established coefficient range enclosure and subdivision
context. The next continuum construction uses elementary univariate
Bernstein nonnegativity/partition of unity and exact de Casteljau subdivision.
Neither these polynomial tools nor parametric expected-reward verification
is claimed novel. No multidimensional complexity benefit from that paper is
imported into the one-parameter path service.

Degenne, Garcelon and Perchet,
[Bandits with Side Observations: Bounded vs. Logarithmic Regret](https://www.auai.org/uai2018/proceedings/papers/182.pdf),
UAI 2018, sections 1–2 (especially the passive side-observation model), already
establishes bounded stochastic regret from informative extra observations.
Our compulsory-pair statistic is inferred from an already required action
audit and estimates a shared Markov parameter, rather than directly observing
another arm's reward. The elementary plug-in calculation in passive_regret.md
is therefore a source-specific application of known passive-feedback behavior.
The paper does not supply the logical mandatory-query lemma or pay this
repository's polynomial preparation and statistical-maintenance costs.

Dudik, Langford and Li, [Doubly Robust Policy Evaluation and Learning](https://icml.cc/2011/papers/554_icmlpaper.pdf),
ICML 2011, section 2.2 equation (1) and sections 3–4, supplies the standard
baseline-plus-inverse-probability-residual construction and its bias/variance
analysis. The proposed randomized completion estimator uses a proved invoice
interval midpoint and an exactly known, deliberately chosen completion
probability. It is a particular control-variate construction, not a new
doubly robust estimator. The repository's earlier selective-feedback and
observable-performance derivations already contain related probability tools.

Auer, Cesa-Bianchi and Fischer, [Finite-time Analysis of the Multiarmed Bandit Problem](https://people.eecs.berkeley.edu/~russell/classes/cs294/s11/readings/Auer%2Bal:2002.pdf),
Machine Learning 47 (2002), section 2, Theorem 1 and Figure 1, gives the
ordinary bounded-reward UCB1 comparator and logarithmic regret guarantee.
Acquisition invoices can be normalized and sign-flipped into that setting.
The present all-time confidence-intersection cost index is a modified
implementation, so the paper's exact constants are not claimed for it.
The source-free invoice learning experiment tests a necessary ordinary
control; it does not introduce bandit learning as a new research mechanism.

Bahar et al., [Algebraic Decision Diagrams and their Applications](https://www.researchgate.net/publication/226732263_Algebric_Decision_Diagrams_and_Their_Applications),
Formal Methods in System Design 10 (1997), author-uploaded full text,
sections 2.1–2.2 and 2.5 (ITE, Apply and abstraction), supplies the existing
finite-terminal ordered representation, unique-table reduction and arithmetic
operations. The 1993 conference PDF mirror returned 403; no inaccessible
section was treated as read. Our source-bound invoice recurrence and paid
contrast service use this ordinary representation; they do not introduce
ADDs, canonical reduction or min/max abstraction.

Glasserman and Yao, [Some Guidelines and Guarantees for Common Random Numbers](https://pubsonline.informs.org/doi/10.1287/mnsc.38.6.884),
Management Science 38 (1992), publisher abstract, identifies established
variance reduction through coupled system comparisons and emphasizes that
benefit needs conditions. The attempted PDF redirected to the abstract;
no particular theorem is imported. The local paired invoice interval is
proved pointwise from shared compatible worlds, rather than inferred from
this literature lead or an assumed favorable covariance.

Ciardo and Siminiceanu, [Using Edge-Valued Decision Diagrams for Symbolic Generation of Shortest Paths](https://www.researchgate.net/publication/2570901_Using_Edge-Valued_Decision_Diagrams_for_Symbolic_Generation_of_Shortest_Paths),
FMCAD 2002, author-uploaded full text, section 2.5 Definition 1, explicitly
describes ordinary integer EVBDDs with zero low-edge weight, signed high-edge
weight, one zero terminal and a root offset. Section 3 introduces a different
normalization for their shortest-path application. We use the prior ordinary
normalization from section 2.5, not their reachability algorithm or infinity
extension. The primary Pedram chapter timed out and the CiteSeer copy failed;
these failures are not read evidence. This ordinary offset factoring is the
representation repair after ia01, not a claim of newly invented quotient
decision diagrams.

Halldorsson and de Lima,
[Query-Competitive Sorting with Uncertainty](https://arxiv.org/html/2012.09475),
section 7, Algorithm 3, Theorem 26 and the following arbitrary-graph extension,
already provide an ordinary local-ratio factor two for resolving edges by
one or both endpoint queries, including arbitrary fees and repeated queries.
The s08 ternary graph construction is a restricted application, with a
source-bound dual/mandatory-set certificate. Its ratio is not new.

Erlebach et al.,
[Sorting and Hypergraph Orientation under Uncertainty with Predictions](https://www.ijcai.org/proceedings/2023/0619.pdf),
introduction and section 2, gives existing learning-augmented consistency and
robustness guarantees and distinguishes tractable sorting from harder graph
orientation. No theorem from that paper is transferred to the paid service
without checking its assumptions or paying for its computations.

Hellerstein, Kletenik and Parthasarathy,
[A Tight Bound for Stochastic Submodular Cover](https://arxiv.org/html/2102.01149),
sections 1–3 and Assumptions 1–4, supplies the corrected harmonic/logarithmic
expected-fee bound with independent item states. The author-hosted PDF timed
out; the full arXiv HTML was read instead. Al-Thani, Cui and Nagarajan,
[Minimum Cost Adaptive Submodular Cover](https://arxiv.org/html/2208.08351),
sections 1.1–1.4 and Theorems 1.5–1.6, has a different correlated-state
framework and constants. The graph tolerance mapping uses observable capped
edge scores and proves its assumptions explicitly. The prior-free pointwise
bound uses ordinary deterministic approximate-greedy charging instead; it is
not inferred from independent marginals in the correlated paid streams.

Kasperski and Zielinski,
[Robust discrete optimization under discrete and interval uncertainty: a survey](https://ki.pwr.edu.pl/zielinski/publications/papers/survey16.pdf),
section 2.2.2, pages 11–12, distinguishes possibly optimal actions under
independent Cartesian item intervals from the failure of that property under
discrete correlated scenarios. This directly prevents misattributing the
shared-cost nominal-bank counterexample as a contradiction or a new general
robust optimization principle. The original cs.pwr host timed out; the ki.pwr
author-hosted full PDF was read. The individual original theorem paper was
not successfully retrieved, so the local derivation does not depend on it.

Mastin, Jaillet and Chin,
[Randomized Minmax Regret for Combinatorial Optimization Under Uncertainty](https://arxiv.org/html/1401.7043),
sections 1–3 and Lemmas 1–2, separates deterministic robust choices from
randomized distributions over choices and their convex-hull formulation.
An expected guarantee for a mixture does not give the uniform per-action
guarantee required by these services. No randomized theorem is imported as a
deterministic service certificate.
