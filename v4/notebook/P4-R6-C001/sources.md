# W6 source comparisons

Codex (GPT-6), November 12, 2026. Read scopes are updated as work proceeds.
Retrieval alone does not count as reconstructing a result. No upstream PDF is
copied into the repository. The research claims and their remaining obligations
belong in the result files and [cycle record](record.md).

| Source | Version and read scope so far | Relevance and comparison obligation |
| --- | --- | --- |
| [Bostrom, The Superintelligent Will](https://nickbostrom.com/superintelligentwill.pdf) | 2012; sections 1--2, goal integrity, cognitive enhancement and technology discussion opening | Broad instrumental agreement can coexist with different final goals. The paper already allows reasons for strategic goal change; it does not assert blanket immutability. |
| [Turner et al., Optimal Policies Tend To Seek Power](https://arxiv.org/pdf/1912.01683v10) | v10, January 28, 2023; definitions 5.1--6.5, propositions 6.6/6.9, theorem 6.13 and its appendix proof | The relevant prevalence notion counts permutation-orbit elements. Average attainable value, a majority of goals and one learner's temporal behavior are distinct. Reconstruct the embedding/injection and its assumptions. |
| [Turner and Tadepalli, Parametrically Retargetable Decision-Makers Tend To Seek Power](https://arxiv.org/abs/2206.13477) | Retrieved 36-page PDF; definitions 3.1--3.5, theorem 3.6 and appendix proof | Disjoint retargeting images give a counting bound, including beyond optimal policies. Compare bounded learners and nonuniform actual goal populations without silently importing uniform orbit weights. |
| [Everitt et al., Self-Modification of Policy and Utility Function in Rational Agents](https://arxiv.org/abs/1605.03142) | 19-page technical report, theorem 16 and proof; appendix lemma 19 and theorems 20--21. The 10-page conference version numbers the main result theorem 12. | Initial optimality, modification independence and the on-policy scope matter. R6.6 supplies bounded improvement; R6.10 lets opponents observe the modification, changing the opportunity set. Neither is a counterexample to the stated theorem. |

Downloaded primary-source PDF SHA-256 identifiers, for reproducibility of the
read scope (temporary copies are not research artifacts):

```text
Bostrom: 4bf5ce7c3d974e4ef889b98a89b248861787baa986b8bc13afe401a2346cebaf
Turner v10: 3f0f5ca0e8ff3391ce0e78161db3b846b80bf5a9aa67efe25954f0dbfeaeb748
Retargetability: 5e4e811bd5a8cbf62203f29e9b7e430d0597d123397ab9f2be12ade6878a694e
Self-modification: 1b7a3c091bd2c02b30d9bc9201bf09b5c6f9af839d30240458da917a3f750461
```

The original Blackwell comparison-of-experiments scan was located, but its
Berkeley download returned HTTP 403. No full-source reading of that scan is
claimed. R6.7 independently reconstructs the finite experiment-order proof;
the result is established mathematics, not a priority claim.

## Initial proof reconstruction notes

For the power theorem's copy argument, restrict the swapping involution to the
support of the *matched* pair A and phi(A). That support is invariant; fix its
complement. The other relevant outcome laws have disjoint support and remain
fixed. If A wins for r, the copied family wins or another member of the larger
family wins for the transformed reward. Applying the involution twice pairs
unfavorable and favorable cases injectively. Extra exposed choices support
strictness under the specified reward laws. This reconstructs the mechanism;
it does not transfer the result to arbitrary empirical distributions of goals.

For multiply retargetable choices, each map is injective and the images of
losing inputs are disjoint. Summing their cardinalities proves the stated
ratio of favorable to unfavorable orbit elements; ties are separate. A weighted
version needs a corresponding assumption about the probability mass of those
images. R6.9 supplies the elementary weighted extension and a checked example;
counting alone does not supply an empirical goal distribution.

For safe self-modification, a continuation worse on a positive-probability
percept can be replaced by the initially optimal continuation while retaining
the same current world action. Modification independence permits this splice;
full-support beliefs make its expected improvement strict. Induction preserves
optimal action along the actually generated history. Optimal-policy existence
and allowable policy names are separate premises, treated in appendix results
19--21. Neither bounded computational improvement nor an opponent reacting
to a changed internal objective is established by this proof.

## Judgment, factual recovery and information representation

| Primary source | Actual read scope | Relationship to this cycle |
| --- | --- | --- |
| [Gneiting and Raftery (2007), Strictly Proper Scoring Rules, Prediction, and Estimation](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf) | Focused theorem 1 convex representation and theorem 3 cost-loss comparison, building on W1's reading; not a new full-paper audit | R6.1's proper-score/Bregman geometry is established. Its task is to make goal coverage, shared and pooled information, and costs explicit. |
| [Zhao et al. (2021), Calibrating Predictions to Decisions: A Novel Approach to Multi-Class Calibration](https://arxiv.org/abs/2107.05719) | Definitions 1--2, proposition 1, theorem 2.2; not the complete sample-complexity proof | Decision calibration compares downstream rules in its specified forecast-based class. It must not be silently equated with recovery of every context-level distinction. |
| [Gopalan et al. (2021), Omnipredictors](https://arxiv.org/abs/2109.05389v1) | Theorem 6.3 and lemma 6.4 proof, including covariance control and convex clipping | Strong existing loss-family guarantees. R6.1/R6.5 specify the separating practical uses that turn low decision regret into factual error bounds. No superior general predictor is claimed. |
| [Jin et al. (2020), Reward-Free Exploration for Reinforcement Learning](https://proceedings.mlr.press/v119/jin20d.html) | Introduction and main algorithm/theorem statements, not the complete appendix | Strong sequential exploration before a reward is supplied. “Reward-free exploration” is distinct from evolution of the evaluator or absence of all selection criteria. |
| [Gács and Körner (1973), Common Information is Far Less Than Mutual Information](https://cs-web.bu.edu/faculty/gacs/papers/commoninf.pdf) | Rendered scanned pages 1--2 and common-code definition; not the complete coding theorem | R6.1's common deterministic fact is the common-function object, whereas pooling is a join. Our finite partition proof is given directly. |
| [Charpenay, Le Treust and Roumy (2024), Side Information Design in Zero-Error Coding for Computing](https://www.mdpi.com/1099-4300/26/4/338) | Introduction, section 3.1 definition 4 and part of appendix A.1 | R6.14's context graph is a characteristic graph for a function with decoder side information. The new interpretive work is the practical-regret bridge and the condition for a single coarsest adequate quotient. |
| [Kolchinsky and Wolpert (2018), Semantic information, autonomous agency and non-equilibrium statistical physics](https://doi.org/10.1098/rsfs.2018.0041) | Introduction; section 4's chosen viability measure; section 5.1, equations 5.1--5.8, coarse-graining interventions and preserved viability. Section 5.2 only inspected in excerpts; no full thermodynamic proof review | A strong prior construction of information defined by its contribution to continued viability. R6.1/R6.12 do not originate that idea. Their finite decision and survival mechanisms specify a different adequacy target; the viability criterion remains explicit. |
| [Sugiyama, Krauledat and Müller (2007), Covariate Shift Adaptation by Importance Weighted Cross Validation](https://www.jmlr.org/papers/v8/sugiyama07a.html) | Section 2 assumptions and weighted risk; section 3 lemma 1 and proof opening | R6.16's changed-relevance repair uses conditional invariance, a standard covariate-shift premise. Its factorized plug-in estimator is different from importance-weighted cross-validation and does not inherit its unbiasedness claim. |
| [Poupart and Boutilier (2002), Value-Directed Compression of POMDPs](https://papers.nips.cc/paper_files/paper/2002/file/14ea0d5b0cf49525d1866cb1e95ada5d-Paper.pdf) | Introduction and rendered pages 3--4, equations 2--5 and theorems 1--2; not the lossy-compression analysis | Established decision-directed compression and invariant reward-predictive subspaces. R6.16 adds its own finite observation, cost and cross-agent recovery contract, not the underlying principle. |
| [Li, Walsh and Littman (2006), Towards a Unified Theory of State Abstraction for MDPs](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/camera-ready-9.pdf) | Section 3 definitions and theorems 1--5 with their proof sketches; theorem 6 statement and opening explanation | Preserving actions, values and models are distinct abstraction targets. R6.16 is an iid finite example; it does not import the paper's sequential learning guarantees. |
| [Grimm et al. (2020), The Value Equivalence Principle for Model-Based Reinforcement Learning](https://proceedings.neurips.cc/paper/2020/file/3bb585ea00014b0e3ebe4c6dd165a358-Paper.pdf) | Sections 3--4.1; supplemental A.1.1 through proposition 1, proposition 4 proof and the invariant-subspace example. Known-reward condition retained in the linear comparison | Strong prior account of models distinguished by intended uses. The R6.8 supplement independently derives a rank criterion for identifying dynamics from policy values with known rewards; its argument does not import an unrestricted linear-span claim when rewards differ. |
| [Grimm et al. (2021), Proper Value Equivalence](https://proceedings.neurips.cc/paper_files/paper/2021/file/400e5e6a7ce0c754f281525fae75a873-Paper.pdf) | Section 3 and section 4 opening; supplemental A.2 proposition 2, proposition 3 and corollary 1 proofs; not the MuZero analysis or empirical reproduction | Policy values can suffice for planning while permitting distinct models. The R6.8 supplement states additional conditions for factual identification; the successful compression and separating cases both remain available. |

The judgment results separate three obligations. Practical goals must make
the target distinction useful; feedback must reveal it; and the learner must
use that feedback. A proper-score identity supplies the first, not all three.
R6.5 implements selective payoff decoding, and R6.16 implements partition
selection with purchased exploration. The latter's declared deployment price
does not cover all search and historical storage. This is an implemented
synthesis on a finite vocabulary, not open-ended concept invention.

## Learning internal values and their persistence

| Primary source | Actual read scope | Relationship to this cycle |
| --- | --- | --- |
| [Auer, Cesa-Bianchi, Freund and Schapire (2002), The Nonstochastic Multiarmed Bandit Problem](https://homepages.math.uic.edu/~lreyzin/papers/auer02.pdf) | Exp3 algorithm, theorem 3.1 and potential proof; section 9 adaptive-adversary qualification | R6.5 uses the established method with a nonuniform prior and a reset-task contract. Structured outcome decoding is a genuinely different, stronger learner in the tested payoff model. |
| [Singh, Lewis and Barto (2009), Where Do Rewards Come From?](https://web.eecs.umich.edu/~baveja/Papers/singh-lewis-barto-2009-cogsci.pdf) | Six-page paper, bounded internal reward versus external fitness and example models | Internal rewards can serve an external success criterion without matching it point by point. This is a central enabling comparison for R6.4/R6.6, not a new idea invented here. |
| [Sorg, Singh and Lewis (2010), Reward Design via Online Gradient Ascent](https://proceedings.neurips.cc/paper_files/paper/2010/file/168908dd3227b8358eababa07fcaf091-Paper.pdf) | Model, algorithm, theorems 1--2 and theorem 3's expressivity argument; the paper omits part of its convergence proof | Strong constructive comparison for optimizing internal reward under bounded planning. Our example makes the clamped-goal/plastic-subgoal/J² interpretation transparent. |
| [Ng, Harada and Russell (1999), Policy Invariance Under Reward Transformations](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf) | Rendered pages 3--5: theorem 1 sufficiency, Bellman substitution and corollary 2; not the necessity appendix | R6.6/R6.15 use established potential differences. Optimal-policy invariance and improving a particular myopic controller are separate statements. |
| [Wiewiora (2003), Potential-Based Shaping and Q-Value Initialization are Equivalent](https://arxiv.org/abs/1106.5267) | Four-page paper, rendered pages 2--3 and induction proof; arXiv upload is from 2011 | Exact same-experience Q-update equivalence. This is an identical implementation after recoding, unlike deeper planning or reward-parameter learning. |
| [Altenberg, Liberman and Feldman (2017), Unified reduction principle for the evolution of mutation, migration, and recombination](https://www.zoology.ubc.ca/let/pdfs/AltenbergEtAl2017.pdf) | Introduction, assumptions and discussion; not the complete general proof | R6.4 proves its own two-type reduction statement. It is an elementary instance of existing evolutionary structure, and reversal can favor positive revision. |
| [Birkhoff (1957), Extensions of Jentzsch's Theorem](https://doi.org/10.2307/1992971) | Cached excerpts of sections 1--3 and the positive-matrix example; the AMS PDF was inaccessible | R6.11 gives its full elementary log-odds derivative proof. The reference locates the broader positive-map tradition, not an uninspected theorem imported as support. |
| [Kussell and Leibler (2005), Phenotypic Diversity, Population Growth, and Information in Fluctuating Environments](https://doi.org/10.1126/science.1114383) | Abstract only; inaccessible author PDFs were not bypassed | Relevant precedent for environmental statistics and switching. No source-specific technical formula is used. R6.11 proves its own synchronous/distributed comparison. |
| [Dekel, Ely and Yilankaya (2007), Evolution of Preferences](https://faculty.wcas.northwestern.edu/dekel/papers/Evolution%20of%20Preferences.pdf) | Introduction, definitions 2--3, section 3 propositions, appendix proposition 2 proof; proposition 1 proof skimmed | Arbitrary preference mutants and equilibrium selection make their static stability comparison stronger than our two-type dynamic. Their observability mechanism motivates R6.10's strategic commitment and fallible-certificate boundaries. |
| [Marklund, Infanger and Van Roy (2025), Misalignment from Treating Means as Ends](https://arxiv.org/html/2507.10995v1) | Sections 2--3 and theorem 1; appendix B.1--B.3 including the fragility proof; section 4 theorem 2 and B.4 opening | Strong comparison for confusing immediate reward with continuation value. R6.15 uses a different discounted preparation example and pairs the fixation boundary with a constructive shaping repair. No empirical result was reproduced. |
| [Ramírez-Ruiz et al. (2024), Complex behavior from intrinsic motivation to occupy future action-state path space](https://pmc.ncbi.nlm.nih.gov/articles/PMC11286966/) | Main definitions/equations 1--7, method conditions 1--4, discussion of absolute versus relative entropy and examples; not the supplement's full proof or experimental reproduction | A substantial alternative without an externally specified task reward: intrinsic path occupancy supplies its objective. It is distinct from R6.12's external survival filtering and from a process with no directional asymmetry at all. |

R6.4, R6.11 and R6.13 make three different convergence claims: a uniform
lower bound on retained priority, synchronization along shared changing
experience, and optimality for a fixed survival objective. None makes every
goal converge to one terminal utility. R6.10 provides a positive stable-
diversity construction. These distinctions, and the intervention removing a
priority's benefit, are central to the answer about degrees of terminality.
The origin and selection of the revision mechanism itself remain W7 work.

## Capability, policy reconstruction and survival selection

| Primary source | Actual read scope | Relationship to this cycle |
| --- | --- | --- |
| [Gardner, Kiderlen and Milanfar (2006), Convergence of Algorithms for Reconstructing Convex Bodies and Directional Measures](https://arxiv.org/abs/math/0608011) | Introduction, section 2 definitions and section 6 opening; not the full estimation proof | Established support-function geometry and statistical reconstruction. R6.7 supplies elementary deterministic bounds and an interpretation of capability/value duality. |
| [Dayan (1993), Improving Generalization for Temporal Difference Learning: The Successor Representation](https://www.gatsby.ucl.ac.uk/~dayan/papers/d93b.pdf) | Sections 2--3, occupancy representation and discounted relation | R6.8's invertible conditional rollout matrix is an immediate consequence of the established successor identity. |
| [Barreto et al. (2017), Successor Features for Transfer in Reinforcement Learning](https://me.net.nz/files/publications/barreto2017sf.pdf) | Main theorem 1 and appendix proof; transfer lemma 1 and theorem 2 proof | Generalized policy improvement is a stronger constructive algorithmic alternative to merely identifying capability geometry. |
| [Alegre, Bazzan and da Silva (2022), Optimistic Linear Support and Successor Features as a Basis for Optimal Policy Transfer](https://arxiv.org/abs/2206.11326) | Section 3.3, theorems 3.2/3.5 and appendices A.1--A.3; state-occupancy application in A.5 | Covers a declared linear reward family. R6.7 explicitly proves why nonnegative weights recover signed preferences on a known fixed-total occupancy hyperplane. That repair does not apply to arbitrary feature totals. |
| [Zheng, Jayanth and Eysenbach (2026), Can We Really Learn One Representation to Optimize All Rewards?, v2](https://arxiv.org/abs/2602.11399v2) | Section 3.1 and appendix C.1's necessary rank proof; not the training/empirical claims | Linear factorization rank is a different complexity notion from exact program description. R6.8 keeps those claims separate. |
| [Chetrite and Touchette (2015), Nonequilibrium Markov Processes Conditioned on Large Deviations](https://arxiv.org/html/1405.5157v3) | v3 dated October 9, 2014; introduction, section VI.3 equations 174--186 and appendix E equations 209--216; not the full large-deviation proof | Doob conditioning and the distinction between endpoint and interior laws are established. R6.12 reconstructs the finite killed-chain case. |
| [Chetrite and Touchette (2015), Variational and Optimal Control Representations of Conditioned and Driven Processes](https://arxiv.org/html/1506.05291v2) | v2 June 19, 2015; introduction, section III.4 and finite-Markov appendix C equations 138--151; not the diffusion argument | Established entropy/control interpretation of selected paths. Conditioning is not automatically a physically available action policy. |
| [Todorov (2006), Linearly-Solvable Markov Decision Problems](https://papers.nips.cc/paper_files/paper/2006/file/d806ca13ca3449af72a1ea5aedbed26a-Paper.pdf) | Section 2 derivation and section 2.1 opening; rendered page 3 verifies cost/value signs | Established KL control cost and exponential value transform. R6.12 is an interpretation and finite worked instance. |
| [Štrupl et al. (2022), Reward-Weighted Regression Converges to a Global Optimum](https://arxiv.org/html/2107.09088v3) | Sections 2--4 and variance proof; section 5 global proof through lemma 5.1, lemma 5.2 construction opening and theorem statements; appendix D finite-rate proof and examples. Not every compact-space technical lemma was reconstructed | Same finite-horizon reweighting mechanism as R6.13. Their discounted value convergence does not itself prove the Perron-growth version; the cycle supplies its own finite-state proof. |
| [Cvetković and Protasov (2020/2022), The Greedy Strategy for Optimizing the Perron Eigenvalue](https://doi.org/10.1007/s10107-020-01585-z) | Full primary HTML introduction, row-product formulation, sparse cycling example, theorem 1 and its proof opening; not the full rate analysis | Exactly the same model-based objective as R6.13 over convex hulls of action rows, with a genuinely different greedy method and broader sparse handling. The cycle's own greedy comparator is faster in its declared panels. |
| [Murthy, Moharrami and Srikant (2023), Modified Policy Iteration for Exponential Cost Risk Sensitive MDPs](https://proceedings.mlr.press/v211/murthy23a.html) | Main paper through theorem 6 proof, including pages 7--9; lemma 7 statement. Supporting appendix proofs not all read | A strong risk-sensitive planning comparison. The map $K_a=s_aP_a$, log reward $\log s_a$, relates the objective to survival growth. |
| [Noorani, Baras and Johansson (2023), Risk-Sensitive RL Using Sampling-Based Expectation-Maximization](https://people.kth.se/~kallej/papers/Risk-Sensitive_RLCDC2023_Noorani.pdf) | Sections II--V, proposition 1 and theorem 1 derivation, especially the episode-weighted likelihood in equation 9; no empirical reproduction | Existing sample-based exponential-return policy search. R6.13's sampler is a different, tabular reset construction. Its proof does not import the source's reward-to-go factorization or claim global convergence for the source's parameterized gradient method. |

For the survival branch, the scientific delta is a fully typed route from
external retention to an acquired, revisable policy and a value description,
including the gap between controllable actions and selected lucky outcomes.
The exact and finite-trial convergence proofs are supplied to make that route
sound. They are not evidence that survival-based learning or multiplicative
control is new. The sampling supplement prices its required attempted trials
and keeps its conservative theorem schedule distinct from the smaller run.

## Source qualifications and unused leads

Bibliographic labels identify the linked primary works; the scope column
limits what the comparison uses. No bibliography priority ranking is intended.
Additional search leads included Rothblum's 1984 multiplicative Markov
decision-chain abstract, recent risk-sensitive surveys, and recent
self-generated-data/bandit convergence work. Their full proofs were not
used. An evolutionary periodic-mutation paper and an older reward-weighted
regression PDF were inaccessible; no technical result was reconstructed from
those retrieval failures.

The comparison deliberately distinguishes an exact recoding (shaping and
Q initialization), a different method solving the same objective (greedy
Perron optimization), and a different objective or information contract
(path occupancy, raw survival, discounted rewards, or paid observation).
An empirical tie is not a substitute for this scientific classification.


## Direct judgment-to-model comparisons found during closure

The [closing comparison](comparison.md) states their scientific effect.
These primary sources were checked in the same cycle; discovery order does
not establish priority.

| Primary source | Actual read scope | Use |
| --- | --- | --- |
| [Nayebi (2026), What Capable Agents Must Know](https://arxiv.org/html/2603.02491) | v3, sections 5.1--6; appendix F threshold proof and J.2 recoding proof; not all PSR-operator proofs | Direct predecessor for probability recovery and common minimal representations. |
| [Richens et al. (2025), General agents contain world models](https://arxiv.org/html/2506.01622v5) | Setup, section 2.4, main result and appendix A.5 proof overview; A.6 opening only | Sequential competence-to-model comparison; full proof not audited. |
| [Adamczyk (2025), Inferring Transition Dynamics from Value Functions](https://arxiv.org/html/2501.09081) | Assumptions, proposition 1, separation discussion and appendix error arguments | Direct deterministic inverse-value predecessor. No use of its reverse-Lipschitz sufficient-condition lemma. |
| [Letcher et al. (2026), Inverting the Bellman Equation](https://arxiv.org/abs/2606.21173v1) | Main sections 2--4.1, theorems 1--3 and appendix C.7 construction | Closest stochastic inverse-value comparison. Continuous and empirical claims not reproduced. |
| [Batra (2026), From Optimal Actions to World Models](https://arxiv.org/abs/2608.07301) | Abstract only | Retained lead; no technical claim imported. |
| [Brandfonbrener et al. (2022), When does return-conditioned supervised learning work for offline reinforcement learning?](https://arxiv.org/html/2206.01079v3) | Sections 2.2 and 3, theorem 1 and stochastic counterexamples | Completes the primary-source record for R6.13 section 6. |
