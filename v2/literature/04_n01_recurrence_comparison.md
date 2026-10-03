# N01 recurrence: targeted primary-source comparisons

Contributor: **Codex (GPT-6)**. Accessed October 3, 2026 UTC.
R-N01-01/C3, complete at the scope of twenty-five targeted comparisons.
This is a targeted audit, not an absence-of-prior-work
claim. Imported techniques, local applications and unverified novelty are separate.

## R1. Performative prediction

Juan C. Perdomo, Tijana Zrnic, Celestine Mendler-Dünner and Moritz Hardt,
*Performative Prediction*, ICML/PMLR 119 (2020), pp. 7599–7609.
[Primary paper](https://proceedings.mlr.press/v119/perdomo20a/perdomo20a.pdf).
Inspected definitions 2.1/2.3, example 3.4, theorem 3.5 and proposition 3.6.
The paper separates optimal induced-distribution risk from stability of
retraining. Its convergence guarantee uses joint smoothness, strong convexity
and sufficiently small distributional sensitivity; dropping assumptions permits
failure. Its discontinuous example already demonstrates cycling without a
stable point. Our clipped controller is a different conditional scalar model,
not a new principle of self-influencing prediction. Equilibrium, convergence,
optimality and empirical adequacy must be separate obligations. No statistical
or convergence guarantee is imported without checking its hypotheses.

## R2. Decision-focused uncertainty sets

Irina Wang, Cole Becker, Bart Van Parys and Bartolomeo Stellato,
*Learning Decision-Focused Uncertainty Sets in Robust Optimization*,
[arXiv:2305.19225v3](https://arxiv.org/html/2305.19225v3).
Inspected introduction, problem formulation, assumption 3.3, theorems 3.1,
3.2 and 4.1, and the robust reformulation appendix. The method learns source
sets for downstream performance with constraint-satisfaction requirements.
The guarantees have explicit uniqueness, regularity, boundedness, optimization
and statistical conditions. This is a direct warning against claiming that
task-specific uncertainty reduction is new. Our present source sets are
supplied conditional evidence, with no learned-set or finite-sample guarantee.
Future learning must compare to this work instead of a marginal interval alone.

## R3. Feedback, legality and non-miraculous contracts

Viorel Preoteasa, Iulia Dragomir and Stavros Tripakis,
*The Refinement Calculus of Reactive Systems*,
[arXiv:1710.03979v2 (2018)](https://arxiv.org/html/1710.03979v2).
Inspected sections 4.2.2, 4.3, 5.5 and 5.7; definition 19 and theorem 11.
Guarded transformers explicitly require an output for legal inputs, avoiding
the false-relation “magic” of unrestricted demonic updates. Algebraic loops
require care; the stated simplification guarantee covers its specified
deterministic loop-free class, not arbitrary instantaneous feedback equations.
The project must treat per-model fixed-point existence as an ordinary contract
obligation. Global source nonemptiness is insufficient for that stronger claim.
Our finite-loss representation limitation is not a limitation of this much
broader formalism. The linked 2022 journal PDF was located but the detailed
inspection here uses the named arXiv version.

## R4. The single-denominator reduction is classical

A. Charnes and W. W. Cooper, *Programming with Linear Fractional Functionals*,
Naval Research Logistics Quarterly 9 (1962), pp. 181–186.
[Author-archive scan](https://iiif.library.cmu.edu/file/Cooper_box00010_fld00009_bdl0001_doc0001/Cooper_box00010_fld00009_bdl0001_doc0001.pdf),
[publisher identity](https://onlinelibrary.wiley.com/doi/10.1002/nav.3800090303).
Inspected all six pages, especially transformation (2.1)–(3), lemma 1,
theorems 1–2 and remark 2. Scaling variables by a reciprocal denominator
reduces the sign-controlled fractional problem to linear programming; the
paper treats sign/zero cases explicitly. B4 specializes the positive-denominator
case with a permanent finite parameter bound. Its use is required as an ordinary
baseline, not a novelty claim. The source-to-loss coordinate change still needs
an explicit receiving contract.

## R5. Joint fractional profiles have much stronger existing machinery

Taotao He, Siyue Liu and Mohit Tawarmalani,
*Convexification Techniques for Fractional Programs*,
[arXiv:2310.08424v2 (June 15, 2024)](https://arxiv.org/html/2310.08424v2).
Inspected introduction and section 5.1, especially the shifted-reciprocal family,
moment-hull descriptions, lemma 3 and proposition 4; other theorem locators were
checked but the full paper was not audited. The paper simultaneously convexifies
univariate fractions with different nonzero denominators using moment hulls.
The two-controller reciprocal family is a very small special case. Therefore
“multiple denominators require approximation” would be false without specifying
the finite-polyhedral representation restriction. An exact conic/algebraic
ordinary comparator is necessary. The local curvature and approximation examples
are useful controls, not a new generic convexification result.

## R6. Calibration can be relative to decisions

Shengjia Zhao, Michael P. Kim, Roshni Sahoo, Tengyu Ma and Stefano Ermon,
*Calibrating Predictions to Decisions: A Novel Approach to Multi-Class
Calibration*, NeurIPS 2021.
[Primary paper](https://proceedings.neurips.cc/paper_files/paper/2021/file/bbc92a647199b832ec90d7cf57074e9e-Paper.pdf).
Inspected theorem 1, definition 4, theorem 2, proposition 2 and sections 4.2–4.4.
Calibration is relative to downstream decision makers; a bounded number of
actions permits polynomial sample complexity. The verification reduction uses
linear partitions of predicted probabilities. Computational search remains a
separate issue: the practical auditor uses a gradient-based surrogate. This
directly challenges a generic claim that comparative usefulness can require
less information than full predictive accuracy. Our uniform conditional bounds
on a response function are different premises, not consequences of average
decision calibration or replacements for this paper's statistical guarantees.

## R7. Changing loss objectives under performative effects is also established

Michael P. Kim and Juan C. Perdomo, *Making Decisions under Outcome
Performativity*, [arXiv:2210.01745v2](https://arxiv.org/html/2210.01745v2).
The version record says January 7, 2023; the rendered document also displays
a later date, so the version identifier is the citation anchor.
Inspected setup, theorems 1–3, theorem 2.7, definition 5.3, lemma 5.4 and
corollary 5.5.
Under a fixed feature distribution and action-dependent binary outcome model,
a predictor can support many bounded downstream loss objectives. Learning
assumes suitable randomized intervention data and a supervised-learning oracle;
adaptability is scoped to specified reweightings. This rules out presenting
multiple objectives under feedback as the project's distinctive idea. Our
prospective question concerns conditional receipts and revised uncertainty;
that difference still needs substantive evidence, not terminology alone.
The detailed implication combines decision and performative outcome
indistinguishability; the calibration reduction concerns residual averages
on induced action partitions. Neither establishes our pointwise source model.

## R8. Conditional performance profiles and compute allocation

Shlomo Zilberstein and Stuart Russell, *Optimal Composition of Real-Time
Systems*, Artificial Intelligence 82 (1996), pp. 181–213.
[Author PDF](https://people.eecs.berkeley.edu/~russell/papers/aij-anytime.pdf).
Inspected definition 2.5, sections 2.2.3, 4.2–4.4 and theorem 4.6. Conditional
performance profiles describe quality distributions given input quality and
computation time. The paper discusses statistical acquisition, discrete
tables, interpolation, approximation error and closure under composition.
Its local compilation theorem uses tree structure and input monotonicity;
repeated subexpressions require separate treatment. Thus a system using its
own predicted performance to allocate effort, or a finite quality/cost table,
is established metareasoning. B18 is an operational witness for a particular
calibration-revision obstruction, not a new anytime architecture. A measured
application must compare ordinary profile-based allocation on the same data.

## R9. Learned halting is an existing optional empirical route

Andrea Banino, Jan Balaguer and Charles Blundell, *PonderNet: Learning to
Ponder*, [arXiv:2107.05407v2](https://arxiv.org/html/2107.05407v2).
Inspected sections 2.1–2.5 and the ACT comparison. The learned conditional
halting probabilities induce a distribution over computation steps. Training
uses expected task loss plus a divergence from a prior halting distribution;
evaluation samples a halting step, with explicit treatment of truncation.
This supplies an ordinary neural baseline if a later empirical task adopts
adaptive computation. It does not establish our external calibration envelope,
and averaging predictions must not be confused with averaging their losses.
No neural training or representability conclusion is part of this recurrence.

## R10. Difference evidence and sharp potentials are established constraint methods

Rina Dechter, Itay Meiri and Judea Pearl, *Temporal Constraint Networks*,
Artificial Intelligence 49 (1991), pp. 61–95.
[Author-hosted reprint](https://ftp.cs.ucla.edu/pub/stat_ser/r113-L-reprint.pdf).
Inspected section 3, theorem 3.1, corollary 3.2, theorem 3.3 and corollaries
3.4–3.5. Difference inequalities become weighted graph edges; negative cycles
characterize inconsistency. Shortest paths give tight implied differences,
and distance potentials construct attaining scenarios. B22 directly adapts
this established method to calibration discrepancies. Its application cannot
support a claim of new relational inference. The full graph closure and
ordinary path reconstruction are mandatory controls. One mirror timed out;
the author's UCLA reprint supplied readable text. The UCI scan was located
but is not the textual basis for these theorem notes.

## R11. Sequential calibration needs an explicit statistical contract

Steven R. Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon,
*Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences*,
Annals of Statistics 49(2), 2021, pp. 1055–1080.
[Inspected arXiv v9 PDF (2022)](https://arxiv.org/pdf/1810.08240v9).
Inspected equation (1), definition 1, theorem 4, corollary 2 and section 6's
stopping-time discussion. Theorem 4 uses bounded adapted observations,
predictable bounded predictions, and an appropriate sub-exponential uniform
boundary. Its estimand is the average conditional expectation, not necessarily
the next deployment's mean. Corollary 2 additionally specifies randomized
assignment with probabilities bounded away from zero and one. These methods
permit repeated inspection under their conditions; they do not validate
arbitrary drift, unobserved actions or pointwise calibration across unseen
contexts. Reusing a logical certificate does not supply any of those premises.

## R12. Tail-loss objectives have an existing finite optimization route

R. Tyrrell Rockafellar and Stanislav Uryasev, *Conditional Value-at-Risk for
General Loss Distributions*, Journal of Banking & Finance 26(7), 2002,
pp. 1443–1471.
[Author manuscript, November 28, 2001](https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf).
Inspected definition 3, proposition 6, theorem 10 and its finite-support
discussion, and theorem 14. CVaR includes only the required fraction of an
atom at the quantile; naively conditioning on losses above that quantile can
give a different quantity. The auxiliary-threshold minimization formula
and scenario-based linear optimization are established. Any later tail-loss
extension should use these as ordinary controls. Average loss, difference of
two CVaRs, and CVaR of paired regret are distinct consumer contracts; the
last also depends on the coupling between the two outcomes.

## R13. The convergent coupled repair uses established convex optimization

Sébastien Bubeck, *Convex Optimization: Algorithms and Complexity*,
Foundations and Trends in Machine Learning 8(3–4), 2015.
[Primary author monograph](https://arxiv.org/pdf/1405.4980v2).
Inspected proposition 1.3, lemma 3.1, the constrained-gradient discussion in
section 3.2, theorem 3.10, and the scope of theorem 3.12. First-order
optimality and projection supply the standard constrained-optimization
interpretation; smooth strong convexity gives convergence guarantees. Theorem
3.12 states its larger-step result on the whole Euclidean space, so C9 does
not import it unchanged into a box. C9 instead proves the quadratic box case
directly from projection nonexpansiveness and eigenvalue bounds. Neither that
specialization nor C10's contraction-residual argument is claimed as a new
optimization method. The text also distinguishes oracle complexity from total
computational work, relevant to fair baseline comparisons here.

## R14. Explicit piecewise-affine QP controllers are an older application

Alberto Bemporad, Manfred Morari, Vivek Dua and Efstratios N. Pistikopoulos,
*The Explicit Linear Quadratic Regulator for Constrained Systems*, Automatica
38(1), 2002, pp. 3–20.
[Primary publisher record](https://www.sciencedirect.com/science/article/pii/S0005109801001741),
[author corrigendum](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp-corrige.pdf).
The publisher's abstract and introduction describe explicit continuous
piecewise-affine solutions of the relevant multiparametric QPs. The main
author PDF timed out twice; its exact theorem hypotheses were not audited.
The two-page 2003 correction was read: it corrects the terminal-weight
calculation and resulting regions in example 7.1. It is not evidence that
the general piecewise-affine characterization was withdrawn. C9's own small
active-set proof stands separately; a broader MPC claim would require reading
the main theorem. The existing application is already a strong reason not
to promote finite affine controller regions as the project's novelty.

## R15. Cyclic execution bounds and recovery of a witnessing cycle

**Primary sources:** Karp, [Berkeley report, 1977](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1977/Archive/ERL-m-77-47.pdf),
later Discrete Mathematics 1978; Chaturvedi and McConnell,
[author preprint, 2017](https://www.cs.colostate.edu/~rmm/minCycleMean.pdf).
Read Karp's Theorem 1, Lemma 1 and dynamic program; read the correction's
counterexample and Lemma 1. Cycle means and shifted edge potentials are
established tools for C12. Negating weights exchanges minimum and maximum.
The later paper corrects a proposed recovery of a cycle of a specified length,
not Karp's value characterization. A checked cycle must establish its actual
edges and mean; a numeric optimal value alone is not that witness. Our small
direct telescoping proof does not depend on the erroneous recovery procedure.

## R16. Static uncertainty, rectangularity and the horizon must stay explicit

**Primary source:** Nilim and El Ghaoui,
[Operations Research 2005](https://people.eecs.berkeley.edu/~elghaoui/Pubs/RobMDP_OR2005.pdf).
Read section 2.2, Theorems 1, 3, 4 and the approximation discussion in 4.2.
The paper distinguishes fixed transition models from time-varying ones.
Its row-product uncertainty assumption excludes correlations across rows and
actions. Finite-horizon robust dynamic programming solves the time-varying
problem, which can upper-bound the fixed-model problem. Under its assumptions,
stationary and varying models coincide for the infinite discounted problem;
the finite discounted gap vanishes with the horizon. C13's two-model family
couples rows and does not satisfy that premise. Our persistent-parameter
example is a small instance of an established modeling distinction, not a
counterexample to their theorem. This source does not justify replacing a
joint static model with independent choices on successive transitions.

## R17. Quantitative potential certificates already support program costs

**Primary source:** Ngo, Carbonneaux and Hoffmann,
[Bounded Expectations, author technical version](https://www.cs.cmu.edu/~janh/assets/pdf/NgoCH17.tr.pdf)
(work published at PLDI 2018). Read sections 3.2-3.5, 4-7, Theorem 6.1 and
Appendix B's expected-cost transformer. The analysis generates quantitative
derivations using potential templates and LP constraints, with operational
MDP semantics and a prototype covering probabilistic loops and procedures.
Its stated metatheory covers monotone resources; the implementation's
polynomial templates and finite-domain sampling are limits, not universal
impossibility results. C12-C15 do not establish a new cost logic by using
potentials, checking linear inequalities or composing expected-cost bounds.
An eventual comparison must separate task loss, reasoning cost and empirical
source validity, and permit ordinary automated resource analysis where its
program model fits. We did not run Absynth or transfer its reported timings.

## R18. Computation selection and context-dependent stopping are old targets

**Primary source:** Hay, Russell, Tolpin and Shimony,
[Selecting Computations, UAI 2012](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf).
Read Definitions 1 and 3, Theorems 4-10, Example 4, Definitions 13-15,
Theorem 16 and sections 6.1-6.2. The model already charges computations
against improved final decisions. It distinguishes bounded expected effort
from a hard cap on every trajectory, shows context-dependent non-indexability,
and supplies stronger alternatives to myopic stopping. Independence is a
premise of the blinkered decomposition, not of the general metalevel model.
The tree-search discussion explicitly addresses reuse and opportunity cost,
while flagging stationarity and future-value approximation limits. Thus a
two-step lookahead defeating greedy stopping, or a retained result useful to
later decisions, is not sufficient project novelty. A bounded exact metalevel
dynamic program is an ordinary comparator for a finite self-assessment fixture.
No claim about the present state of all later metareasoning research follows.

## R19. Tail bounds with signed costs have more developed existing methods

**Primary source:** Chatterjee, Goharshady, Meggendorfer and Zikelic,
[PACMPL/OOPSLA 2024](https://research-explorer.ista.ac.at/download/17162/17182/2024_ProcACMProgLanguage_Chatterjee.pdf).
Read section 4.2, Definition 5.1, Theorems 5.2, 6.2, 6.7-6.9 and section 7's
constraint synthesis. Their cost is a limsup of cumulative increments.
Expected-cost results for signed increments require termination and a lower
bound on cumulative cost. Tail analysis combines stochastic invariants with
cost supermartingales; additional conditions may hold only on the restricted
program, rather than globally. The synthesis uses established polynomial and
linear positivity methods. This is a substantially stronger existing control
than C15's elementary bounded finite-horizon argument. Neither adding a tail
consumer nor adding the probability of leaving a valid region is by itself
new. We inspected theorem statements and synthesis, not the separate detailed
proof appendix or artifact execution; no unqualified import of their full
soundness theorem is claimed.

## R20. Value-directed compression is a direct prior-art challenge

Pascal Poupart and Craig Boutilier, *Value-directed Compression of POMDPs*
(2002), [author-hosted paper](https://www.cs.toronto.edu/~cebly/Papers/vdib.pdf).
Read sections 2–4, Theorems 1–3 and the preliminary experiment description.
Their lossless construction preserves policy values using a reward-containing
subspace invariant under action/observation transitions; predicting the next
compressed belief can suffice without reconstructing the full belief. A
Krylov construction and structured alternatives already implement this idea.
Their lossy alternating optimization has bilinear constraints and is not
guaranteed to reach a local optimum. Theorem 3's proof is omitted in the
paper; we do not import its constants. This is a close baseline for any claim
about consumer-specific information or recursively useful summaries. A fixed
model and reward contract differs from our proposed revision experiment, but
that difference alone establishes no novelty. Rebuilding the ordinary
compression after a revision must be measured, and its reusable structure
must be retained when the native method is allowed to retain analogous work.

## R21. Finite contingent policies already have exact vector/LP methods

Anthony Cassandra, Michael L. Littman and Nevin L. Zhang, *Incremental
Pruning: A Simple, Fast, Exact Method for Partially Observable Markov Decision
Processes* (UAI 1997), [primary paper](https://arxiv.org/pdf/1302.1525).
Inspected sections 2–4, equations 6–10, Figures 1–3 and the experiment tables.
The dynamic-programming update combines finite value vectors by cross sums
and removes unnecessary vectors using witness-region LPs. Intermediate
pruning preserves the represented value function. C16's small policy-vector
calculation therefore fits a longstanding exact approach; exhaustive policy
enumeration is an initial reference, not the strongest scalable comparator.
For our minimization convention the value envelope is concave rather than
convex. Source restrictions can further prune the relevant belief region,
but later source withdrawal must invalidate that restriction-dependent
pruning. The paper's numerical timings are not forecasts for this system;
we have neither run its implementation nor audited every complexity proof.

## R22. Approximate decision state has explicit performance bounds

Jayakumar Subramanian, Amit Sinha, Raihan Seraj and Aditya Mahajan,
*Approximate Information State for Approximate Planning and Reinforcement
Learning in Partially Observed Systems*, JMLR 23 (2022),
[primary paper](https://jmlr.csail.mit.edu/papers/volume23/20-1165/20-1165.pdf).
Targeted inspection: Definition 7, Theorem 9 and its backward-induction proof,
Remarks 11–12, and Theorem 27's discounted extension statement. Approximate
reward sufficiency and approximate self-prediction yield value and policy
loss bounds; transition error is weighted by the relevant value-function
regularity. A learned representation is not automatically a uniform
certificate: the stated error premises still need evidence. This work rules
out treating approximate decision-sufficient state, or a generic propagated
error allowance, as a distinctive project idea. It provides a stronger
ordinary control if the project later admits lossy temporal summaries.
We did not audit all 83 pages, the learning experiments, or supplementary
code. Current finite fixtures do not need those broader guarantees.

## R23. Risk summaries must respect atoms and the tail convention

Carlo Acerbi and Dirk Tasche, *On the Coherence of Expected Shortfall* (2002),
[primary paper](https://arxiv.org/pdf/cond-mat/0104295).
Inspected Definitions 2.1–2.6, Proposition 3.2, Corollary 3.3, Proposition 3.4,
Proposition 4.2 and Corollary 4.3. Quantile integration handles atoms by taking
the required fraction of boundary mass, avoiding a naive conditional-tail
average. Their lower-tail profit convention translates to our upper-tail
loss convention with profit=-loss and tail mass=1-alpha. The continuity and
quantile representation support C19's elementary interpolation control.
Neither adding a tail consumer nor that approximation bound is a novelty
claim. The separate finite-grid counterexample in C19 is a local limitation
of a specified receipt format, not a limitation of distributional summaries.

Additional access limits: the original Blackwell experiment-comparison PDF
was blocked; the Smallwood–Sondik scan did not yield inspectable text or
images. Neither is counted as a theorem audit. R21 supplies the directly
inspected finite-policy-vector comparison instead.

## R24. The stronger finite stochastic-dominance control is already explicit

Darinka Dentcheva and Andrzej Ruszczynski, *Optimization with Stochastic
Dominance Constraints*, SIAM Journal on Optimization 14(2), 548–566 (2003).
[Repository record](https://doi.org/10.18452/8290),
[inspected author-uploaded text](https://www.researchgate.net/publication/328333254_Optimization_with_stochastic_dominance_constraints).
Read section 2's definition/equivalence, Proposition 2.2, section 3 and
Proposition 3.2 with its proof. For a finite-support reference distribution,
checking its support thresholds suffices for the entire dominance relation.
Their proof uses convexity between reference knots and monotonicity outside;
the finite-scenario formulation is linear. This improves C21's sufficient
union-of-supports construction: the reference knots alone suffice. Negate
their reward convention to obtain our loss convention. The paper therefore
supplies an explicit ordinary method for a comparison valid across an entire
class of risk preferences. We did not audit its later optimality/duality
theory or reproduce the financial illustration; none is needed here.

## R25. Tail-risk comparison is related by established convex duality

Wlodzimierz Ogryczak and Andrzej Ruszczynski, *Dual Stochastic Dominance and
Quantile Risk Measures*, International Transactions in Operational Research
9 (2002), 661–680,
[author-hosted paper](https://www.ia.pw.edu.pl/~wogrycza/publikacje/artykuly/myitor02.pdf).
Read section 3, equations 9–17 and the discrete LP construction in section 4.
Integrated quantiles and shortfall transforms have conjugate representations;
their ordering characterizes stochastic dominance. The paper distinguishes
atom-safe tail averages from a naive conditional expectation, using a
convention that must be translated before comparing formulas. These results
directly cover the principle behind C21's self-contained finite derivation.
Its many-risk-level comparison is a control, not a new value-logic theorem.
The related SIAM paper was located, but its extracted text was corrupted;
its detailed theorem statements are not counted as inspected.

## Leads not promoted into evidence

Hay and Russell's *Metareasoning for Monte Carlo Tree Search* (2011) was located
on the Berkeley institutional site; only the record/abstract was inspected.
It motivates an ordinary value-of-computation comparison if that route is
selected. No theorem from it is used. Broad search also returned robust
performative prediction and compensation-for-calibration papers; these remain
leads until their exact assumptions are inspected.

## Current impact on ambition

Route A still lacks a defended application gain beyond ordinary robust
optimization. Route B provides sharper local test cases, but single-loop LP,
joint fractional convexification, feedback legality and decision-relative
calibration all have strong antecedents. A useful project result must concern
the concrete loss/evidence/revision problem and survive those methods. No
novelty pass is justified by the present source audit.
