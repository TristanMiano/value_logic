# Primary-source comparisons

Codex (GPT-6), DEVELOPMENT. Read during s11; search snippets alone are leads.
No exhaustive novelty review is claimed.

- Poupart and Boutilier, *Value-Directed Compression of POMDPs*, NeurIPS 2002,
  [paper](https://papers.neurips.cc/paper/2192-value-directed-compression-of-pomdps.pdf),
  sections 2.1, 2.3 and 3–3.1, equations 1, 3–5 and Theorems 1–2. Read the
  unnormalized update convention, compressed recursion and smallest invariant
  subspace construction. These already supply linear value-directed compression
  and its Krylov computation. They are the direct ordinary comparator. The
  s11 canonical-baseline inclusion is a proposed combination with potential
  transformations, not a new compression principle.
- Ng, Harada and Russell (1999), *Policy invariance under reward transformations*,
  [paper](https://ai.stanford.edu/~ang/papers/shaping-icml99.pdf). The accessible
  abstract identifies potential-difference reward transformations and their
  policy-invariance role. The PDF text extraction of the theorem pages was
  garbled; those pages have not yet been reliably read. Attribute the shaping
  principle, but do not assert that the paper lacks a particular extension.
- Grimm et al. (2020), *The Value Equivalence Principle for Model-Based
  Reinforcement Learning*, [paper](https://proceedings.neurips.cc/paper/2020/file/3bb585ea00014b0e3ebe4c6dd165a358-Paper.pdf),
  section 4, Proposition 1 and Remark 2. The span of selected functions controls
  model equivalence; feature-relative model matching can suffice for the
  represented value class. Generic task-relative model usefulness is therefore
  prior art, not a new s11 discovery.
- Grimm et al. (2021), *Proper Value Equivalence*,
  [paper](https://arxiv.org/html/2106.10316v2), introduction and the section
  containing Proposition 4 and Corollary 1. Models can preserve planning while
  ignoring environmental distinctions. This directly limits any broad novelty
  claim about several globally imperfect but task-useful models.
- Skalse et al., *Invariance in Policy Optimisation and Partial Identifiability
  in Reward Learning*, [record](https://arxiv.org/abs/2203.07475). Relevant lead
  on reward transformations and policy-order information. Abstract page opened;
  attempted HTML v3 endpoint failed. Full comparison remains pending.

Subsequent reading: the [PDF](https://arxiv.org/pdf/2203.07475) was accessible.
Read Definition 2.5, Lemma B.1, the comparison lattice discussion and section
4.2/Theorem 4.2. Potential shifts preserve advantages; data sufficient under one
transition law can become inadequate under another through successor-reward
redistribution. These are direct antecedents for baseline cancellation and
the warning against automatic counterfactual transport. Our finite stopping
interface includes an explicit terminal residual instead of importing an
infinite-horizon vanishing-potential assumption. No new invariance principle
is claimed.

- Baisero and Amato (2021), *Reconciling Rewards with Predictive State
  Representations*, [paper](https://www.ijcai.org/proceedings/2021/0299.pdf),
  introduction, sections 2.3, 3.1 and 4 through equations 7–11. Predicting
  observations alone need not preserve reward information. Their reward-predictive
  representation adds reward intents and a constant-reward token to include
  observation probabilities. This supplies a strong comparison for s11's
  value-query interpretation. Our narrower relative-policy output may omit that
  token, and must not claim to reproduce the generative observation law.
  Observable rewards can themselves change the information interface; that
  caution supports explicitly including informative invoices in K.

The 2020 reward-predictive-representation article on PMC was blocked by a
browser check. It remains a lead rather than a completed full-text comparison.
# Interval-regret comparison (October 15 session)

- Gilbert and Spanjaard, *A double oracle approach to minmax regret
  optimization problems with interval data*, arXiv:1602.01764v3 (2017),
  <https://arxiv.org/pdf/1602.01764>: read section 3.1, Observation 4,
  Proposition 1, and section 4 Algorithm 1. Mean-scenario agent responses,
  endpoint adversaries for binary interval objectives and the whole double
  oracle framework are established. Our paid-query specialization must be
  compared with these, not just midpoint or always-fallback baselines.
- Xu et al., MIRROR, UAI 2021,
  <https://proceedings.mlr.press/v161/xu21a/xu21a.pdf>: read Algorithm 1,
  section 4 and the agent/nature oracle discussion. Sequential minimax-regret
  policy mixtures via double oracle are already explicit; approximate oracle
  limitations are also explicit. The proposed local delta is exact structured
  oracles for the specified information/revision menu, not the framework.
- *Optimizing Minimax Regret in Uncertain MDPs with Small Sets of Policies*,
  arXiv:2608.02509v1, <https://arxiv.org/html/2608.02509v1>:
  read the deterministic-memoryless restriction and section 5's partition
  formulation. Its prepared-policy-set duty is different from private
  randomization before learning the source. It does not establish that our
  randomized scope is new; retain it as a recent comparison lead.
- Padmanabhan, Ahipasaoglu, Ramachandra and Natarajan, *Extremal Probability
  Bounds in Combinatorial Optimization*, arXiv:2109.01591v1,
  <https://www.arjunramachandra.com/_files/ugd/fca0b4_9e9f1d3e9c6e41bb90335fe4e69d2462.pdf>:
  read section 2.2, Corollary 2.2 and its attaining conditional construction,
  plus section 2.2.2's final-sum weighted probability objective. The stopped
  invoice flow adapts these compact marginal-coupling ideas to intermediate
  costs and saturation. Optimization Online and an attempted HTML version
  were inaccessible; the author-hosted PDF was read.
- Thomas, Theocharous and Ghavamzadeh, *High Confidence Off-Policy Evaluation*
  (2015), <https://people.cs.umass.edu/~pthomas/papers/Thomas2015.pdf>:
  read the importance-weighting discussion, coverage/support restriction and
  concentration-inequality section. Partial-policy evaluation, importance
  weighting and its large-range problem are established. The dual-score
  sampling proposal has different measurements but must face this antecedent.


- Regan and Boutilier, *Robust Policy Computation in Reward-uncertain MDPs
  using Nondominated Policies* (AAAI 2010),
  <https://www.cs.toronto.edu/~cebly/Papers/Regan_Boutilier_aaai10.pdf>:
  read equations (4)-(8), Observation 1, and the constraint-generation
  description. Fixed-policy worst-case regret, its interpretation as an
  adversarial model/policy pair, and use in elicitation are established.
  Our proposed oracle is a special structured evaluation problem, not a new
  regret criterion or a general minimax-regret solver.
- Chassein and Goerigk, *Minmax Regret Combinatorial Optimization Problems with
  Ellipsoidal Uncertainty Sets*,
  <https://eprints.lancs.ac.uk/id/eprint/82586/1/source.pdf>:
  read introductory binary decision model and section 3.1, especially the
  induced interval scenario preceding equation (5). An extremal fixed
  solution admits a single induced scenario followed by ordinary optimization.
  The signed controller has that same shortcut when every cell selects terminal
  action 1. Terminal action 0 has interior coefficients and needs separate
  treatment; this alone does not establish novelty of our dynamic program.
- Osogami, *Robust partially observable Markov decision process* (ICML 2015),
  <https://proceedings.mlr.press/v37/osogami15.pdf>:
  read section 2's state/action uncertainty contract, Bellman equation (1),
  Theorem 1 and Algorithm 2. It supplies a strong robust planning antecedent.
  Our fixed common-source regret benchmark is different from that paper's
  worst-case value objective and transition uncertainty. No general superiority
  or transfer of its theorem is claimed.

- Koller, Megiddo and von Stengel, *Efficient Computation of Equilibria for
  Extensive Two-Person Games* (1996),
  <https://pdfs.semanticscholar.org/5ec2/6550509b747e3b213206b0eb668a25e9d249.pdf>:
  read section 2, equations (2.1)-(2.4): realization constraints, conversion
  to behavior strategies, and LP best responses. The perfect-recall tree
  representation is an explicit antecedent. Our merging of different query
  orders into partial assignments requires its separate source-independent
  proof; the theorem is not imported for arbitrary imperfect-recall games.
  The von Stengel 1996 companion abstract was available at the publisher;
  two attempted LSE-hosted full sources returned errors.
- Gandhi, Khuller, Parthasarathy and Srinivasan, *Dependent Rounding and its
  Applications to Approximation Algorithms* (2006),
  <https://www.cs.umd.edu/~srin/PDF/2006/depround-jou.pdf>:
  read introduction's properties P1/P2 and star-vector case, section 2.1,
  and Theorem 2.3. Marginal-preserving sampling with a hard cardinality
  bound, including a linear-time star case, is established machinery.
  Our subset sampler uses these properties; no novelty is claimed for it.

- Mastin, Jaillet and Chin, *Randomized Minmax Regret for Combinatorial
  Optimization Under Uncertainty* (2015),
  <https://www.mit.edu/~jaillet/general/rand_mmr_final.pdf>:
  read sections 2 and 3.2, Theorem 4, (LPI), and the convex-uncertainty
  limitation. Randomized interval regret can already be polynomial when the
  binary nominal problem is. The finite-response lifting is an adaptation;
  its ternary labels share an uncertain coefficient and must not be replaced
  by independent interval costs on duplicated one-hot variables.
- Gyorgy, Linder, Lugosi and Ottucsak, *The On-Line Shortest Path Problem
  Under Partial Monitoring* (2007),
  <https://www.jmlr.org/papers/volume8/gyoergy07a/gyoergy07a.pdf>:
  read section 4, Theorem 3 and its forward/suffix path-sum implementation,
  plus section 5's paid-feedback estimator. Weighted-path learning and its
  linear-in-edges implementation are established. This is a strong ordinary
  no-extra-query comparison for our stopped-query graph.

## Later primary comparisons and exact locators

These readings occurred during the closed research session; this index merely
collects locators already used in the linked notes. Imported machinery remains
distinct from the proposed specialization. Abstract-only entries are leads.

- [Juba (2016)](https://www.jmlr.org/papers/volume17/13-584/13-584.pdf):
  sections 1.1–1.2, Theorems 8/10, Algorithm 1 and proof pages 22–23.
  Integrated learning and planning is established; its weighted traces,
  typical-state and bounded proof assumptions differ from the all-source-world
  repair contract. [Comparison](repair_prior.md).
- [Rigter, Lacerda and Hawes (2021)](https://www.robots.ox.ac.uk/~nickh/papers/rigter2021aaai.pdf):
  Definition 5, Propositions 1–3 and appendix proof of Proposition 2.
  Distinguish rectangular uncertainty from a fixed dependent model.
  [Repair comparison](repair_prior.md).
- [Kolman and Koutecky (2015)](https://kam.mff.cuni.cz/~kolman/papers/CSP-published_EJC.pdf):
  Theorem 1.1, section 2.2, Lemma 2.1 and join argument. Bounded-treewidth
  CSP extended formulations are prior machinery; the proposed truth/mask
  adapter has separate sampling and resource duties. [Adapter](structured_repair.md).
- [Ignatiev, Morgado and Marques-Silva (2016)](https://arxiv.org/pdf/1604.08229):
  section 2.2 Definition 1 and section 2.3 Algorithm 2;
  [abductive/contrastive explanation analysis](https://arxiv.org/pdf/2012.11067),
  section 3 Propositions 1–2 and Theorem 1; and
  [Marques-Silva, Janota and Lynce (2010)](https://sat.inesc-id.pt/~mikolas/ecai10.pdf),
  sections 2.2 and 3.1–3.3. Generic certificate/hitting-set novelty was parked.
  [Selection note](certificate_selection.md).
- [Rakhlin and Sridharan (2013)](https://proceedings.mlr.press/v30/Rakhlin13.pdf):
  section 4.1 Lemma 6, appendix small-loss argument and section 4.2.1 Lemma 7.
  Optimistic multi-model learning is prior art; the receipt estimator and
  observability conditions are the local adaptation. [Model selection](model_selection.md).
- [Nisan and Szegedy (1994)](https://web.vu.lt/mif/s.jukna/boolean/Nisan-Szegedy.pdf):
  section 1.3.2, Theorem 1.3. Decision-tree degree bounds are established;
  the invoice-event restriction and span construction have their own proof.
  [Information note](invoice_information.md).
- [Coding lecture](https://tdalazard.io/infoTheory/S7.pdf), PDF pages 20–23:
  code-dual orthogonality and coset consequences. The restricted-character
  calculation uses these standard tools. [Invoice information](invoice_information.md).
- [Zong, Lehtonen and Rintanen (2026)](https://arxiv.org/pdf/2606.24672):
  section 3 Definitions 1–3, section 5.2 Theorem 3. Known-joint-law Boolean
  evaluation and decision diagrams differ from fixed-source minimax repair;
  the shared conventional mechanisms must still be credited. [Comparison](repair_prior.md).
- [Albore, Palacios and Geffner (2009)](https://ml.rwth-aachen.de/~hector.geffner/www.dtic.upf.edu/~hgeffner/alex-ijcai09.pdf):
  sections 2–4 on knowledge and sensing; [reconfiguration discussion](https://arxiv.org/html/1404.3801v1),
  introduction and valid-move distinction; [model repair](https://arxiv.org/pdf/0710.3332),
  section 3 Definitions 2–4. These precedents distinguish querying knowledge,
  valid intermediate moves and atomic output repair. [Geometry](repair_geometry.md).

The JAIR regret source at https://www.mit.edu/~jaillet/general/regret-jair-17.pdf
was not successfully opened; no theorem is imported from that failed request.
The Statistics Canada 2024 cost-allocation abstract was a lead only. Later
searches for cost-only Boolean feedback and stopping-time Fourier degree
returned leads rather than a completed priority search. Lack of a found match
does not establish novelty. Further priority comparison remains part of R11-M
and I11-M's unassessed verification targets.
