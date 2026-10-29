# Closest-result comparison for the unchanged V19 event

Codex (GPT-6), October 28, 2026. DEVELOPMENT. This comparison addresses the
algorithmic contract, not a claim that ordinary methods cannot do the task.

## Exact comparison questions

The claimed input is k bounded scalar observations of a minimum over n
independent, individually constrained affine response models. The required
output is the entire next scalar image, including gaps and rational witnesses.
The distinguishing resource statement is 2*n*2^k local LP calls, O(n*3^k)
subset-combination comparisons, and at most n*2^k output intervals. Generic
exact encodability and the usefulness of rejecting inconsistent models are
established facts, not claimed discoveries.

| Primary antecedent | What it supplies | Remaining distinction in this event |
|---|---|---|
| Ahmed and Guan, inverse optimal values (2005; s19 read) | Inference from observed optimum values, with hardness and structured tractability | Several shared interval observations and a complete future scalar image under a product of model-specific polytopes; the receipt-parameter algorithm is the proposed delta. |
| Mostafaee, Hladik and Cerny, inverse interval LP (2016) | A scenario with a prescribed optimal value, using continuity and parametric LP under stated assumptions | The conditioning by several shared receipts may disconnect the parameter set. A path joining unconditioned endpoint scenarios need not respect those receipts. Their interval-data contract and target scenario differ from the conditioned whole-image output. |
| Bemporad, Garulli, Paoletti and Vicino, bounded-error PWA identification (2003) | Select a fitting partition and affine models; retain feasible parameter sets for the selected classification | V19 retains all compatible witness assignments and projects their union. It does not select one fitted partition or infer the number of pieces. |
| Toriello--Vielma (2012) and Teichrib--Schulze Darup (2024) | Exact active-piece mixed-integer formulations of max-affine or broader piecewise regression | The same disjunction is a strong exact control. Their fitted-model formulation does not itself state the n-linear fixed-parameter whole-image algorithm, interval count, or complete local-certificate object. |
| Berger and Sankaranarayanan, template-based PWA regression (2024) | All maximal compatible data subsets, infeasibility-guided search, and optimal covering to select a minimal-piece model | Subset enumeration, covering and LP certificates are already combined in identification. Whole-range reconstruction must additionally preserve the values discarded by choosing only maximally constrained compatible fits; see the counterexample below. |
| Exact PWA set propagation and max-plus state estimation | Maintain or enclose states consistent with measurements; exact set prediction is an established objective | General union propagation does not supply the stated receipt-parameter compression merely by recognizing this as a static-state instance. The distinction is resource structure, not epistemological novelty. |
| Subset partition/covering and bottleneck convolution (credited in s19) | The dynamic-programming combination primitives, including faster variants | The proposed synthesis is the anchored scalar image, with exact coverage, source witnesses, and its output/resource consequences. No new convolution primitive is claimed. |
| Goodman (1999), general semiring outside values | Reverse recurrences for surrounding derivations in any commutative semiring | The outside caps themselves are a direct specialization. The [set-semiring reconstruction](semiring_control.md) makes this strong overlap explicit; the remaining claim is the particular whole-range specialization and its checked resource contract. |
| Mohammadi and Gentili (2021), outcome ranges in interval LP | Extremize an additional linear function over all possibly optimal solutions; special tractable cases and general hardness | Retaining uncertainty for a later readout is already a stated purpose. Their equations (7)--(8) ask for endpoints of another function on the optimizer set; V19 asks for the complete future optimum-value image after several shared observations, with an explicit receipt parameter. |
| Hladik (2026; 2025 preprint), interval absolute-value LP | Best/worst optimal values with interval coefficients, orthant LP reduction and basis-stability cases | General nonconvex uncertain optimization and exact local LP decomposition are established. The read propositions do not give the product-source, receipt-conditioned complete image or its n-linear parameter bound. |
| Pouly, Haenni and Wachter (2007), compiled semiring solutions | Compile all optimizing finite configurations into a Boolean representation for further queries, under a strict-monotonicity hypothesis | Compilation for repeated questions is established. V19's continuous whole scalar image is a different output; it needs neither all source configurations nor strict monotonicity of bottleneck multiplication. |
| Abbas and Swoboda (2019), bottleneck potentials in MRFs | Threshold sweeps for discrete bottleneck-plus-sum inference, exact unary/chain cases and a general graph relaxation | Their threshold-dependent optimum costs and exact discrete graph algorithms are strong antecedents to bottleneck inference. They do not state the conditioned continuous image and receipt-parameter bound here. |

## Why maximal feasible covers alone are not a whole-range answer

This counterexample is our derivation, not attributed to the sources. Take
two independent x_1,x_2 in [0,1], one receipt min(x_1,x_2)=0, and future
V=min(-x_1,-x_2). The true future set is [-1,0]. For each generator the only
maximal feasible receipt subset is {1}, whose local slice is {0} and future
image {0}. Retaining only those maximally constrained slices and then covering
the receipt yields {0}, losing valid values. One unassigned generator must
retain its empty-subset slice. Thus a successful maximal-cover feasibility
method is not automatically an exact prediction-set method. It can be adapted
by retaining the relevant value-bearing slices and combining them; V19's
claim concerns that explicit adaptation and its bounded complete output.

This does not prove that such an adaptation is difficult, that no earlier
paper has it, or that all sparse implementations must enumerate every subset.
It isolates an actual missing step rather than relying on different notation
or calling conventional reasoning 'ordinary' as a criticism.

## Primary-source read scope in this session

- [Bemporad et al., 2003](https://cse.lab.imtlucca.it/~bemporad/publications/papers/sysid-03.pdf):
  introduction, Problem 1, Problem 2 and the initialization description.
  The stated objective chooses a bounded-error PWA fit and classification;
  its uncertainty sets are associated with that classification. This reading
  supports the comparison above, not a survey claim about all later work.
- [Mostafaee et al., author preprint dated February 25, 2015](https://nb.vse.cz/~cernym/invp.pdf):
  introduction/problem statement, Theorems 1--3 and Corollary 1 statements,
  the continuity assumptions, and the parametric-method discussion/conclusion.
  The published article is JCAM 292 (2016), 591--608. The read contract asks
  for a scenario attaining one prescribed value over interval coefficient
  data. Its continuity-based range conclusion cannot be applied to a
  disconnected receipt-conditioned subset without further proof.
- [Cerny and Hladik, 2016 publisher page](https://link.springer.com/article/10.1007/s10100-015-0402-y):
  abstract and bibliographic information only. It explicitly studies the
  optimal parameter set, so claiming that inverse work never considers a
  whole parameter set would be false. Full text remains an access limitation;
  the author-linked rdcu PDF was inaccessible during this session. A later
  browser attempt reached a Human Verification CAPTCHA, not the paper;
  no challenge was solved or bypassed. The author homepage links to the
  same publisher article, and the ResearchGate page offers no full text.
- [Teichrib and Schulze Darup, 2024](https://proceedings.mlr.press/v242/teichrib24a/teichrib24a.pdf):
  sections 1--3, equations (2), (4), (6)--(8), Theorem 1 and proof. Its
  max-affine selector formulation specializes to the same receipt source.
  Fixing observation bands and adding supplied compact coefficient bounds
  gives an exact ordinary MIP comparator; whole-range enumeration and the
  claimed parameter count are additional work.
- [Toriello and Vielma, 2012](https://juan-pablo-vielma.github.io/publications/Fitting-Piecewise-Linear.pdf):
  after an initial failed URL, the author's publication-list link succeeded.
  Read section 3.2, equations (3.6)--(3.12), Proposition 3.2 and proof, and
  the model-size discussion. This directly supplies the active-piece MIP
  comparison. Its symmetry ordering cannot simply be imposed on labelled,
  differently constrained source blocks. Model criticism from a poor fit is
  also explicitly discussed there; that general purpose is not our novelty.
- [Berger and Sankaranarayanan, 2024](https://www.cambridge.org/core/journals/research-directions-cyber-physical-systems/article/templatebased-piecewise-affine-regression/9CC69E94D4F222CA4741ADA0181D5471):
  Problems 1--3, the maximal-compatible-set formulation, Theorem 3 and its
  proof, and Lemma 2's infeasibility-certificate argument. The construction
  already integrates subset search, covering and local LP infeasibility.
  Its target is a minimal-piece fitted model under a region template. The
  maximal-cover counterexample above explains the extra prediction duty.
- [Goodman, 1999](https://aclanthology.org/J99-4004.pdf): section 4's outside
  definitions and Theorems 4--5, with proofs, plus section 5's storage
  discussion. See the explicit specialization in semiring_control.md.
- [Mohammadi and Gentili, 2021, author preprint](https://arxiv.org/pdf/1910.05913):
  section 3's formal outcome-range definition, section 3.1's right-hand-side
  restriction, Theorem 1's hardness argument and Propositions 1--2's tractable
  cases. The paper itself is *The Outcome Range Problem in Interval Linear
  Programming*, distinct from Garajova--Rada--Hladik's 2020 exact-method paper,
  which was located as a bibliographic lead but not read here.
- [Hladik, October 7, 2025 preprint](https://arxiv.org/pdf/2510.04604), published
  in October 2026: problem definition, Proposition 1 and its orthant
  formulation, basis-stability definitions, Proposition 4 and conclusion.
  The target is best/worst optimal values. This comparison does not claim
  to solve that broader uncertain absolute-value programming problem.

Searches for exact max-affine prediction sets, bounded-error identification,
version spaces and parameterized complexity did not locate a directly
matching theorem. That absence is limited evidence. Set-membership and
general disjunctive approaches remain strong conceptual antecedents. A
novelty judgment must rest on the precise surviving synthesis and resource
statement, with the inaccessible-paper limitation left visible.

## Additional compilation and bottleneck comparisons

[Pouly, Haenni and Wachter (2007), author-uploaded full text](https://www.researchgate.net/publication/220887049_Compiling_Solution_Configurations_in_Semiring_Valuation_Systems)
was recovered after the CiteSeer copy failed. Read sections 4.1, 6, 7.1--7.3,
Theorems 2--3 and the stated hypotheses; those theorems' proofs are referred
to another report and were not read here. Their complete optimizer compilation
requires strict monotonicity; section 4.1 explicitly notes the bottleneck
exception. Its absence does not invalidate computing one bottleneck maximizer
or Goodman-style outside values. It does prevent importing that particular
all-optimizer guarantee without checking its hypothesis. The paper's repeated
query motivation is an antecedent, not a V19 novelty claim. Our complete
scalar image is smaller than the full continuous source set and includes
nonoptimal scalar values; the anchoring identity establishes that output.

[Abbas and Swoboda (2019)](https://arxiv.org/pdf/1904.08080), sections 3--4.2,
Definition 1, Propositions 1--2, displayed algorithms and Remarks 1--3:
the finite-label problem combines ordinary summed costs with a bottleneck
penalty. Threshold sweeps retain the best summed cost at each bottleneck
bound; dynamic shortest paths yield their chain algorithm. This is not a
claim that bottleneck inference itself is new or difficult in the unary case.
The read algorithm does not preserve an entire continuous conditioned scalar
image. We do not rely on its introductory semiring terminology: scalar max
and min on a total order are distributive, as the directly checked identities
and the bottleneck example in Pouly et al. establish.
