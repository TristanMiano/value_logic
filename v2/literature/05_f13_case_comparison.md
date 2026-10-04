# F13: focused comparison for scientific and staged reasoning cases

Contributor: **Codex (GPT-6)**. Accessed October 4, 2026 UTC.
Status: focused comparison for the F13 application and retention arguments.
This is a scoped primary-source check, not an exhaustive novelty search.

## 1. Quadrature: the invisible residual is established methodology

Pedro Gonnet, *A Review of Error Estimation in Adaptive Quadrature*,
[arXiv:1003.4629v1, March 24, 2010](https://arxiv.org/html/1003.4629v1).
Inspected section 6, equations (81)–(82), the following null-space analysis,
and the distinction between finite experimental reliability and general
failure classes. Published survey identity: ACM Computing Surveys 44(4), 2012.
The actual version inspected here is the 2010 manuscript.

Differences between quadrature outputs can vanish without establishing small
integration error. The paper analyzes failure subspaces and stronger
interpolant-based diagnostics. F13's degree-six polynomial is a concrete
conditional information example, not a newly discovered quadrature defect.
An extra-node repair must be compared with ordinary interpolation, Gaussian
quadrature where nodes are free, and appropriate error enclosures. A finite
sampled success corpus cannot certify the integrand model itself.

## 2. Computation selection already has a joint probabilistic semantics

Nicholas Hay, Stuart Russell, David Tolpin and Solomon Eyal Shimony,
*Selecting Computations: Theory and Applications*, UAI 2012,
[author-hosted paper](https://aima.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf).
Inspected definition 1 (joint utilities/computation outcomes), section 2's
metalevel process, theorem 4's computation-cost value, theorem 5 and example 3.

The model already treats computation outcomes jointly and chooses further
computation for its effect on a later decision. Positive computation cost
supports an expected stopping bound under the paper's assumptions, while a
uniform finite path bound need not follow. F13's fixed finite cascade and
explicit unresolved terminal state use a simpler contract. Staging avoids
an infinite feedback question; it does not introduce a new general theory of
self-assessment. The native receipt guarantee is an additional implementation
obligation, not evidence of statistical calibration.

## 3. Algorithm portfolios already use per-instance execution evidence

Matthew Streeter and Stephen F. Smith, *New Techniques for Algorithm Portfolio
Design*, UAI 2008,
[author-hosted paper](https://mattstreeter.org/Research/mstreeter_uai_2008.pdf).
Inspected section 1.1's schedule/restart/resume and portfolio definitions,
section 2.1's offline formulation/theorem 1, section 2.2's partial online
feedback, section 4.2's censored runtime comparison, and section 5's
anytime-objective extension. The arXiv upload is 2012, not the publication year.

Per-instance solver outcomes, schedules and the value of combining heuristics
are established. Online execution reveals only attempted runs; missing later
outcomes are not automatically available for a revised schedule. The stated
approximation result has its own objective and scheduling assumptions and is
not imported as a theorem about F13's bounded unresolved-penalty objective.
Ordinary joint execution tables, schedule optimization and source-aware checked
receipts form the appropriate combined control. Pairwise summaries are only a
deliberately lossy diagnostic, not the strongest ordinary competitor.

## 4. Sequential testing and strong ordinary scheduling controls

Blake Harris, Viswanath Nagarajan and Rayen Tan, *Sequential Testing with
Subadditive Costs*, [arXiv:2501.18010v1 (2025)](https://arxiv.org/html/2501.18010v1),
sections 1–1.1. Independent additive testing has an established cost/probability
ordering rule; the paper studies a substantially richer batching cost model.
F13's independent reset-procedure ratio rule is an ordinary control. Its
robust interval extension retains rectangular independence, which must not
be inferred from observed singleton frequencies. The paper's batching and
approximation guarantees are not claimed for F13's correlated source.

Uriel Feige, László Lovász and Prasad Tetali, *Approximating Min Sum Set Cover*,
Algorithmica 40 (2004), [author manuscript](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf),
definition, theorem 1 and section 2. Correlated first-success scheduling already
contains the familiar task of ordering sets to cover weighted instances early.
Its greedy approximation and hardness results make a small greedy failure
an adverse control, not a new optimization problem or novelty evidence.

Amol Deshpande, Lisa Hellerstein and Devorah Kletenik, *Approximation
Algorithms for Stochastic Boolean Function Evaluation and Stochastic
Submodular Set Cover*, SODA 2014,
[author-hosted manuscript](https://www.cs.umd.edu/projects/reucaar/approx.pdf),
sections 1–2. The discussion distinguishes discovering a Boolean value from
obtaining a certificate for it, and distinguishes independent from general
distributions. F13 similarly must state whether inspection of the source,
a checked object proof, or an attempted strategy is the deliverable. Requiring
a weak search strategy when ordinary source inspection yields a cheap checked
proof would manufacture an advantage. A certificate requirement is legitimate
only when applied to both routes.

## 5. The ordering framework and the rank antecedent

Felix Happach, Lisa Hellerstein and Thomas Lidbetter, *A General Framework for
Approximating Min Sum Ordering Problems*,
[arXiv:2004.05954v2 (July 2020)](https://arxiv.org/html/2004.05954v2),
section 2, equations (1)–(2), and section 2.4; published in INFORMS Journal on
Computing in 2022. Their chain formulation already joins cumulative cost with
increments of a subset weight function. For F13, take cumulative attempt cost
and probability of success within a subset, with the final unresolved mass
handled explicitly. This is an application mapping, not a claim that their
stated approximation assumptions automatically hold for every F13 extension.
It removes generic chain-based cost composition from the novelty candidates.

Oleksandra Gasanova and Lisa Nicklasson, *Chain algebras of finite distributive
lattices*, Journal of Algebraic Combinatorics 59 (2024), 473–494,
[publisher's open text](https://link.springer.com/article/10.1007/s10801-023-01294-8),
theorem 3.4 and its three-step proof. The theorem gives dimension |L|-|P|;
the proof identifies this with the rational span rank of maximal-chain
incidence vectors. For a k-element antichain, L is the Boolean lattice, giving
2^k-k. Its adjacent exchanges and connected rank layers are the direct
antecedent of F13's equal-cost argument. Removing the empty/full coordinates
does not lower the proper-chain span for k>=2: vanishing proper coordinates
forces the sum of row coefficients to vanish. Thus the equal-cost numeric
rank is a specialization, not a new theorem. The checked text does not state
F13's unequal-cost elementary-symmetric kernel, zero-cost exceptions, or its
consumer-revision example. Their omission here is not evidence of priority
elsewhere, or of a useful project-level contribution.

## 6. Statistical coverage and risk remain imported tools

R. Tyrrell Rockafellar and Stanislav Uryasev, *Conditional Value-at-Risk for
General Loss Distributions*, Journal of Banking & Finance 26(7), 2002;
[author manuscript, November 28, 2001](https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf).
Rechecked definition 3, proposition 6, theorem 10 and corollary 12: boundary
atoms are split, the threshold minimization formula applies to general loss
distributions, and monotonicity/translation govern pathwise perturbations.
These support the ordinary tail control and cost-rounding argument. F13's
cheap-fallback reduction is a specialized consequence of the finite-tail
definition. It is not claimed as a new risk measure. The paper's convexity in
decision-dependent losses assumes a fixed underlying probability law; it is
not a blanket convexity claim for simultaneously revised probabilities and
policy choices.

Wassily Hoeffding, *Probability Inequalities for Sums of Bounded Random
Variables*, JASA 58(301), 1963, 13–30,
[publisher record](https://www.tandfonline.com/doi/abs/10.1080/01621459.1963.10500830).
The publisher abstract confirms the independent bounded-summand scope.
The [primary scanned copy](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf)
returned no extractable body and the browser screenshot requests failed.
No fresh theorem-body inspection is claimed. The elementary exponential-moment
proof used for F13's exact bound is therefore written in the case notebook;
the name and formula are established, not novelty evidence. No inference of
iid sampling or calibrated source bounds comes from the synthetic corpus.

## Implication for ambition

None of these checked sources supports a claim that the generic shared-source,
metareasoning or information-loss idea is new. A useful F13 contribution would
need an application result whose significance survives their combination,
or a clearly identified gap with evidence worth pursuing. Developing a new
worked family remains valuable technical progress even if novelty stays
unsupported. More time should buy a materially richer question and its defense,
not only more examples of a known dependence phenomenon.

The weighted retention calculation is worth recording as a precise local
result and a check on assumptions. It saves only k-1 linear coordinates over
the full joint law, disappears for richer consumers, and has a close rank
antecedent. This combination lowers its expected value as the sole novelty
target. A further chunk should choose a substantive application question or
a better-supported limitation, with an explicit discriminator against the
combined ordinary methods above. It should not merely enlarge the same rank
matrix or relabel known metareasoning.
