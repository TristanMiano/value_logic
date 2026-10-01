# F10 — research effort and ambition calibration

Research contributor: **Codex (GPT-6)**. September 30, 2026.
Status: **complete at F10 audit/calibration scope; L45 satisfied**. This is a prospective planning assessment informed by
[the core audit](02_core_audit.md), not measured completion of the proposed work.

The author's objective is a useful project-level advance, built with established
tools wherever they help. No component novelty quota is imposed. Forecasts must
say what question could be answered, which work is required, what counts as an
informative stopping point, and what remains uncertain about novelty.

## 1. What the literature changes about the work estimate

The finite arithmetic and certificate foundations are substantially available.
Reuse ordered-group/CPWA reasoning, linear certificates, parametric optimization
and support maintenance. Most remaining uncertainty is in the **combination's
usefulness and cost**, including how much joint evidence a loss judgment needs
after a revision. A new scalar carrier or another representation identity is
unlikely to be the best next investment.

The first integrated reasoner can be small, but a fair evaluation needs a
separate semantic reference, explicit source-access policies, construction and
checking costs, and update sequences that include unfavorable cases. A fast
replay demonstration on hand-selected examples is cheaper than that evaluation.
Published solver performance does not estimate our implementation hours or
predict our speedups. In particular, minimization can reduce checking work
while adding producer work, and conflict reuse only benefits queries with
reusable conflicts. Account for both kinds of cost in the whole workflow.

The ordinary-training neural branch has mature methods to reuse too, but a
different uncertainty: the proposed cost decomposition may not be learned or
identifiable. A successful decoder or output-changing patch is an early
observation. A stronger interpretation needs controlled interventions, matched
alternative explanations and held-out evidence. The short pilot and the
stronger research claim should have different budgets.

## 2. Optional close checks used for calibration

These close checks extend the core audit for planning. They do not turn the
paper into a broad survey of interpretability or statistical learning.
All primary texts below were accessed September 30, 2026.

### C01. Distributed alignment search

Atticus Geiger, Zhengxuan Wu, Christopher Potts, Thomas Icard and Noah D.
Goodman, *Finding Alignments Between Interpretable Causal Variables and
Distributed Neural Representations*, CLeaR 2024, PMLR 236, 160–187.
[Published paper](https://proceedings.mlr.press/v236/geiger24a/geiger24a.pdf).
Read §3, especially Definitions 1 and 3–5, §§4.3–4.4 and Appendices A, D–E.
DAS fits an alignment with both models frozen. Its implemented search uses
rotations; its definition permits general invertible maps. A specified causal
model and counterfactual sampling are required. Tables 1–2 select the best
training-intervention results across three runs, but Appendix A.2 describes
testing splits and Appendix E also reports unseen intervention evaluations.
Held-out evaluation is therefore an established part of the comparison.
Published GPU times do not price our research effort or this host's runtime.

**Project implication.** F04's initial coordinate-subset probe is a reasonable
bounded start. Failure there does not rule out distributed representations.
Use established alignment methods if expansion is warranted. Retain matched
alternative-cost explanations, ordinary training and transported gauge
controls, and budget development selection and held-out evaluation separately.

### C02. Successful patching can be misleading

Aleksandar Makelov, Georg Lange and Neel Nanda, *Is This the Subspace You Are
Looking for? An Interpretability Illusion for Subspace Activation Patching*,
arXiv 2311.17030v2, December 6, 2023.
[Inspected primary version](https://arxiv.org/pdf/2311.17030v2).
Read §§3.2–3.5, §5, §8 and Appendix A.3. A patch can mix a disconnected
information-carrying direction with a dormant output-relevant direction and
produce the desired output effect. The paper also discusses successful
interpretations and the role of representation/component choices; it does
not show that all subspace interventions are invalid. A workshop version has
a different author list; this citation follows the inspected arXiv version.

**Project implication.** The existing unused-neuron control is useful but is
not a complete test of a future distributed intervention. Before expanding
that search, include a disconnected/dormant control and examine the permitted
intervention family. Separate transported changes of hidden coordinates from
changes to the high-level causal question. Budget for diagnosing apparent
success as well as failure. This increases the effort estimate for a defended
neural interpretation, without requiring a new methodology.

### C03. A proxy-risk bound already has a substantial theory

Peter L. Bartlett, Michael I. Jordan and Jon D. McAuliffe, *Convexity,
Classification, and Risk Bounds*, JASA 101(473), 138–156, 2006.
[Published paper, university mirror](https://sites.stat.washington.edu/courses/stat527/s14/readings/Bartlett_etal_JASA_2006.pdf).
Read §2, Definitions 1–2 and Theorems 1–2. The psi-transform relates excess
surrogate risk to excess binary-classification risk, with classification
calibration giving a nontrivial limiting guarantee. The bound is sharp in its
stated setting. This is about population risks and their Bayes infima; finite
data, approximation and optimization errors remain separate issues.

**Project implication.** Import an appropriate calibrated bound as evidence
when its task and distribution assumptions hold. A source-row numerical
inequality is not itself a statistical calibration theorem. The promising
project question is how such evidence composes and survives specified changes,
not a generic promise to improve a mature risk bound in a short session.
The continuous population theorem is not automatically an exact CPWA expression
or an arbitrary-utility result.

### C04. Approximation with a storage/error tradeoff is established too

Colin N. Jones and Manfred Morari, *Polytopic Approximation of Explicit Model
Predictive Controllers*, IEEE Transactions on Automatic Control 55(11),
2542–2553, 2010, DOI 10.1109/TAC.2010.2047437.
[Author manuscript, EPFL repository](https://infoscience.epfl.ch/server/api/core/bitstreams/1cf0c9fe-7adf-4e30-af9b-56ce997d56a1/content).
Read §II, Algorithm 2, and §V.A–D, especially Lemma 19 and Theorem 20.
Implicit double description builds inner/outer approximations of a compact
convex set; the control application relates an approximate cost to a feasible
controller under additional stability conditions. It explicitly trades
complexity against approximation error without requiring the full optimal
explicit solution first. A Hausdorff bound and a control stability guarantee
are different from an arbitrary vertical error bound on our signed judgments.

**Project implication.** Generic certified approximation is not an unexplored
escape from the size of U11's complete catalogue. For a fixed native clause,
negating its concave RHS value gives a convex function; the outer case/clause
combination need not share that convexity. Bounded revision regions, support
eligibility after withdrawals, and native evidence checks must be specified.
Reuse convex approximation where it fits, then measure the application's
benefit. This lowers confidence in a generic pruning novelty claim and favors
a focused revision experiment before a new optimization method.

### C05. Recomputing alternatives is a serious retention baseline

Boris Motik, Yavor Nenov, Robert Piro and Ian Horrocks, *Incremental Update of
Datalog Materialisation: the Backward/Forward Algorithm*, AAAI 2015,
DOI 10.1609/aaai.v29i1.9409.
[Author manuscript](https://www.cs.ox.ac.uk/people/ian.horrocks/Publications/download/2015/MNPH15b.pdf).
Read §§2–5, especially Algorithm 2 and Theorem 1. The method maintains a finite
Datalog materialisation after explicit fact deletion, finding alternate proofs
without storing the full dependency family. Its evaluation compares both work
and runtime, including a crossover to fresh materialisation. This is not a
termination theorem for all native terms and rational budgets.

**Project implication.** Compare selective retention with an ordinary strategy
that checks a cached proof, searches for a replacement when needed, and falls
back to fresh solving. Preserving a requested threshold judgment is weaker
than retaining the globally sharp bound. Choose that objective before pricing
the experiment; a first acceptable proof can settle the former. Existing
incremental methods make an all-cache-versus-no-cache comparison too weak to
support the intended contribution claim. No Datalog implementation is imported.

### C06. The prediction scale is part of a loss interpretation

Mark D. Reid and Robert C. Williamson, *Composite Binary Losses*, JMLR 11,
2387–2422, September 2010.
[Published primary paper](https://www.jmlr.org/papers/volume11/reid10a/reid10a.pdf).
Read §§2–4.1: conditional risk, properness, and the loss/link distinction.
Proper probability estimation and real-valued prediction connected by a link
are separate contracts. Use the stated differentiability and invertibility
conditions when applying their characterizations; this note imports no new
statistical guarantee.

**Project implication.** F04 correctly identifies the weighted-loss optimum
as `q=J0/(J0+J1)`, not the raw outcome probability eta. Evaluate task learning
against that target. Interpretation also depends on the decoder/intervention
scale: a useful log-cost encoding need not admit an accurate affine raw-cost
decoder. Before the F14 freeze, check compatibility between the chosen
decoder family, the affine output logit and the proposed cost intervention.
Treat that as a design diagnostic, not evidence that training learns the costs.
Any comparison of raw-cost and transformed-cost decoders must be declared and
capacity-matched before held-out evaluation.

### C07. Preference-led revision already has close normative accounts

Maomei Wang, *Preference revision and Bayesian updating*, Synthese 207,
article 244, May 28, 2026, DOI 10.1007/s11229-026-05628-4.
[Published primary text](https://link.springer.com/article/10.1007/s11229-026-05628-4).
Read §§4–5, especially the revision axioms and Theorem 5.3. Under its
Anscombe–Aumann prior, event-occurrence input and designated conditional and
constant-act anchors, the framework recovers the Bayes-induced posterior
preference relation. The anchor choice matters; this is not an unconditional
uniqueness result for arbitrary incomplete preferences or changing desires.

**Project implication.** Preference-led belief revision is not by itself a new
project contribution. The present proposal maintains quantitative evidence
after a **supplied** revision; choosing which commitments to revise is a
different normative problem. A v3 proposal to select revisions must compare
such accounts and declare its own trust/priority assumptions. A source version
or directed unit edge does not supply those assumptions automatically. This
comparison narrows the ambition without requiring changes to the finite core.

### C08. Adding expectation is not a new scalar foundation

Robert Furber, Radu Mardare and Matteo Mio, *Probabilistic logics based on
Riesz spaces*, LMCS 16(1), article 6, January 27, 2020,
DOI 10.23638/LMCS-16(1:6)2020.
[Author manuscript](https://www.macs.hw.ac.uk/~rm4023/papers/Riesz20.pdf).
Read Definition 3.1, Proposition 3.6, Theorem 8.1 and its proof-system figure.
Real-valued lattice/vector operations combine with a positive linear
subprobability expectation operator. The stated semantic completeness uses
the Archimedean rule and a specified Markov-process model class; it is not
the finite native certificate contract. The publisher PDF endpoint failed,
so the author's manuscript was inspected.

**Project implication.** Reuse this theory if probabilistic modalities become
useful. A finite known rational transition matrix can already be represented
by fixed linear combinations; uncertain coefficients multiplied by uncertain
losses or genuinely cyclic evaluation raise different questions. Neither a
generic expectation operator nor its renaming as value reasoning establishes
novelty. The next feasibility block should identify an application and the
specific extension of the current evidence contract it actually needs.

### C09. The combined retention aim also has a close proposal

Aevyra, *The Ledger of Will: Evidence, Revaluation, and the Preservation of
Revisable Agency*, research paper v4.0, September 25, 2026.
[Primary project text](https://aevyra.github.io/ledger-of-will/).
The page credits Yue and Anika, Sofia, and Anika for formulation, revision,
and review respectively; independent peer review was not established here.
Read §§3–6, §9 and Appendix A. Its finite factorization and revision-closure
criteria, alternative supports, and budgeted evaluation proposal concern
preserving answers under later changes. The reported finite illustrations
are distinct from its unexecuted agent study. Its broad synthesis is already
close to our motivation; generic revision sufficiency is not a safe novelty
claim.

**Project implication.** A remains worthwhile as a narrower quantitative
certificate experiment. The inspected text does not supply our directed-unit
kernel, fixed-row CPWA portfolio or measured comparison. Those differences
are questions to evaluate, not automatic originality. At the early checkpoint,
state the exact unanswered application question and compare an ordinary
dependency/status-plus-solver construction. Confidence in distinctiveness
should stay low-to-medium until that comparison yields a result. No agent
memory benchmark or external implementation is imported into A's budget.

### C10. Reward transfer already has reusable quantitative structure

André Barreto, Will Dabney, Rémi Munos, Jonathan J. Hunt, Tom Schaul,
Hado van Hasselt and David Silver, *Successor Features for Transfer in
Reinforcement Learning*, NeurIPS 2017.
[Published paper](https://proceedings.neurips.cc/paper/2017/file/350db081a661525235354dd3e19b8c05-Paper.pdf);
[primary manuscript with supplement](https://arxiv.org/pdf/1606.05312).
Read §§2–4, Theorems 1–2 and Appendix A. Fixed dynamics and a shared feature
map permit reward-weight changes. Generalized policy improvement has a
uniform value-approximation penalty; the transfer bound additionally uses
feature bounds, discounting and closeness to stored tasks. The main text also
discusses limiting the retained policy library. This is not a theorem about
arbitrary changing dynamics or source withdrawal. The proceedings supplement
was a ZIP unavailable through the reader; Appendix A was inspected in arXiv.

**Project implication.** Reusable value decompositions and reward-transfer
portfolios are established baselines if v3 pursues that problem. Distinguish
reward weights from source RHS changes. U11 fixes the query as well as row
directions; arbitrary changes to its objective require new work. A's initial
budget therefore covers a finite declared query family and supplied evidence
revisions, not an unrestricted reward-transfer agent.

### C11. Start with an established selection objective when it fits

G. L. Nemhauser, L. A. Wolsey and M. L. Fisher, *An Analysis of
Approximations for Maximizing Submodular Set Functions—I*, Mathematical
Programming 14, 265–294, 1978, DOI 10.1007/BF01588971.
[Original paper, hosted scan](https://thibaut.horel.org/submodularity/papers/nemhauser1978.pdf).
Read §1's sum-of-maxima example, Definition 2.1, Proposition 2.1 and §4,
especially Theorem 4.2 at zero marginal-decrease allowance. Normalized monotone
submodular gain under a cardinality limit k admits the greedy guarantee
`1-(1-1/k)^k`, hence at least `1-1/e`. This requires the stated objective and
constraint, not merely a selection problem bearing the word portfolio.

**Project implication.** Complete independently replayable certificates over
a finite workload give a simple coverage baseline. P4 below states its narrow
adaptation and failure cases. Byte budgets, sharing, worst-case coverage and
complementary proof fragments require separate analysis. This makes a first
implementation more plausible while reducing the rationale for inventing a
new selection heuristic before testing an existing one. No universal pruning
guarantee for U11 follows.

## 3. Prospective research packages

### Current planning rule: grow breadth and evidence together

**Subsequent authorized PLAN01 amendment:** the
[current roadmap](../../TODO_v2.md) now applies this ladder through protected
60/90-minute research chunks, starting with N01's contribution-target comparison.
The illustrative targets and original forecasts below remain estimates. At each
checkpoint, unsupported or displaced novelty requires a named next recurrence/
evidence chunk; Gates C/D cannot advance without a supported scoped project-level
contribution. A/B retain their original readiness scopes. This amendment is a
planning decision, not new literature evidence or a conclusion that novelty has
been established. See [PLAN01](../decisions/2026-09-30_novelty_and_recurrence.md).

**Author amendment, September 30, 2026, after F10 completion.** Increasing
effort should buy both more substantive results to defend and stronger support
for the growing result set, in roughly equal measure. The default is a
**4 / 8 / 16 / 32-hour cumulative ladder**, extensible at later checkpoints.
These are different scope targets, not central/high estimates for the same
deliverable. In particular, 32 hours should not merely repeat the 16-hour
programme with more checking.

Plan roughly half of each additional research block for new scope and half
for establishing or strengthening evidence across the expanded scope. Count
work once even when it serves both purposes; mandatory integration and records
also consume the budget. This is a planning balance, not an assertion that
claims have equal costs. Every new result needs enough support to be reported
honestly when introduced. A collection of unsupported conjectures is not the
intended breadth gain.

The following is an **illustrative project path**, conditional on Gate B and
later task dependencies. Hours are total engaged effort from the start of the
selected package, for one agent familiar with the repository, including
D/L/E/O and excluding unattended computation. Gate work and required reviews
must be explicitly charged when assembling an execution budget; this table
does not price or complete every remaining v2 obligation.

| Cumulative budget | Added substantive scope | Added evidence and challenge | Useful stopping result |
|---|---|---|---|
| **4 h** | One bounded scientific loss comparison and one RHS revision family; attempt the smallest producer/reference path | Check the contract, compare with direct solving, and reconstruct a hostile case | A narrow end-to-end feasibility result, or a precise obstruction and revised implementation estimate |
| **8 h** | Extend that question to withdrawal, stale versions and alternative supports on a small declared workload | Challenge the new revision cases; add current-proof and replacement-search comparisons with explicit cost accounting | An expanded revision result showing which conclusions survive, fail or remain unavailable, with initial comparison evidence |
| **16 h** | Add a bounded self-assessment case concerning the evaluator's own versioned behavior; connect it to the scientific case | Test compositional conclusions against a separate reference; strengthen baselines and reconstruction across both cases | A coherent two-case result and an account of where the shared method works or breaks; later frozen evaluation remains distinct |
| **32 h** | Add one further substantive question, preferably the required ordinary-training neural pilot once its F14 prerequisites are met | Freeze and evaluate that pilot with matched controls; deepen the earlier cases through prospective evaluation, replication or an adversarial reconstruction | A broader body of supported results spanning revision, bounded self-assessment and a scoped learned-representation question, including informative nulls |

The increments are **4, 4, 8 and 16 hours**, not four independent allocations.
These are provisional ambition targets: the original implementation forecast
below already shows that the 16-hour outcome could overrun. At each checkpoint
record separately (1) new questions/results covered, (2) evidence gained,
(3) unresolved limitations, and (4) the next increment's revised central/high
execution forecast. If the producer or a premise fails, retain a supported
obstruction, repair or redirect the next scope addition. Do not label an
unfinished rung achieved or spend the next block entirely polishing the same
result without reporting the deviation from the breadth/evidence balance.

At **64 hours and beyond**, choose the next meaningful extension from the
evidence: for example, another application family, a richer revision contract,
or a second learned task. Pair it with stronger checks of the enlarged claims.
Do not precommit to endless doubling, a new carrier, or a new version merely
to fill a budget. A v3 extension still needs its own feasibility case. More
supported breadth can be valuable even when its components reuse known tools;
novelty remains a project-level, uncertain assessment.

### Original F10 package estimates retained for calibration

The following A/B central/high estimates are the **original narrower package
forecasts**, preserved rather than retroactively fitted to the ladder. They
remain evidence about likely effort and risks, not the preferred policy of
spending all additional effort on a fixed result. In particular, the old
"more thoroughly defended" tier is superseded as the default expansion path
by the balanced ladder above. These judgmental estimates are not confidence
intervals and exclude human independent review, publication, a production
solver and a complete new phase. No package is started by this amendment.

### A. Checked evidence for revisable loss judgments — preferred next investment

**Question.** In a declared finite loss-model workload, when does keeping a
selective, checked portfolio preserve useful decisions after evidence changes
more economically than keeping everything or solving each request afresh?
This joins OPP-01 and OPP-04 and can include OPP-03's bounded self-assessment.
The algorithms can be established ones; the candidate advance is an answered
application question with a precise evidence contract and measured tradeoffs.
C09 makes even the broad combination an antecedent, so the first checkpoint
must test this narrower application delta rather than just restate the aim.
Revisions are supplied inputs. This estimate does not include selecting a
normatively preferred revision policy or inferring a unique utility function.
The scientific model is also supplied: validating its error assumptions against
new domain data is additional work, not included in these hours. A small
joint-error loss comparison from F04 is a development starting point, not a
substitute for the application decision and composite inference required by F13.

**First informative checkpoint: 3 / 6 hours, included in the totals below.**
Choose one scientific loss comparison and its revision family. Establish a
small independent semantic reference and reproduce an adversarial sequence
containing strengthening, relaxation, withdrawal, and a stale source version.
Compare a full portfolio, a current-best proof and fresh solving. Decide
whether the distinctions matter to the task's decision or only to incidental
proof formatting. A failed comparison can stop the proposed optimization work.
Include the cached-proof/replacement-search baseline from C05. Freeze a finite
set of query shapes and say whether the objective is preserving specified
threshold decisions or reproducing sharp bounds; do not slide between them.
Check automated certificate production at this checkpoint. The current
[F08 code](../checks/f08_revision_portfolio.py) replays supplied dual candidates;
it does not enumerate vertices or solve
LPs. If a small search/reference pair cannot be made reliable within this block,
revise the implementation forecast before committing to the full comparison.

**First useful integrated result: 12 / 24 hours total.**

| Work area | Central | Plausible high | Result purchased by that effort |
|---|---:|---:|---|
| D: contract, retention/error argument and hostile cases | 4 h | 6 h | Precisely stated preservation guarantee or a scoped obstruction |
| L: closest combined baseline and application check | 1 h | 2 h | Reuse decision and a revised distinctiveness assessment |
| E: small producer, separate reference and revision comparisons | 5 h | 12 h | Reproducible correctness, size, precision and total-cost measurements |
| O: evidence records, reviewable integration and write-up | 2 h | 4 h | One coherent result another session can reconstruct |
| **Total** | **12 h** | **24 h** | **Useful positive or negative answer for the declared workload** |

The first implementation should bound dimension, row count, case count and
the finite query family before optimizing. U11's existing guarantee does not
cover continuously changing objective directions for free (C10). It need not solve general parametric LP or
enumerate every hidden-unit subset. Use exact acceptance of certificates;
report unsupported cases and timeouts explicitly. Match evidence access across
baselines. Include an ordinary full-information semantic baseline separately
if the unit policy itself is being evaluated.
The current receiver validates a context containing all case rows and admitted
witnesses. Count that context as well as the retained proofs; pruning a proof
does not establish that its underlying source data can be discarded. If fresh
source access is unavailable, say so for every method and disable the same
fallbacks. Compression of the receiving context would be a separate contract.

Measure initial construction plus all updates, peak retained storage, proof
checking, source reads, achieved bound and decision changes. Include cases
where reuse loses and report the update count at which any initial construction
cost is recovered. A lower checking time alone is not a total-cost improvement.
Pruning must not silently turn an unavailable certificate into a countermodel.

At matched target-reduct access, an exact semantic reference and a complete
native procedure must agree on derivability by U1. The proposed practical gain
therefore concerns the cost of obtaining and receiving that answer, or a
declared precision/resource tradeoff. It cannot be a sharper valid bound than
the exact reference on the same model. A scalar-summary baseline can lose
information, but repeating that established separation alone would not answer
the proposed application question.

**A more thoroughly defended result: 24 / 48 hours total**, conditional on the
first checkpoint being informative. The extra 12 / 24 hours cover a second
application or workload family, sensitivity to degeneracy and revision-region
choice, stronger baseline tuning, adversarial reconstruction and a tighter
literature comparison. This may support a modest research claim; it is not a
forecast of acceptance at a venue or guaranteed positive performance.

Confidence is **moderate** that the first package yields a useful bounded
result; **low-to-medium** that its final question/result will prove sufficiently
distinct from close prior work; performance advantage is unknown. Reassess at
3 hours and again at 12. If the reference and producer disagree, repair before
benchmarking. If the ordinary combined baseline already does the job cleanly,
retain that useful implementation and stop selling a new pruning method.
If cost growth prevents even the frozen small comparison, report that boundary
and narrow the next attempt explicitly.

### B. An ordinary-training neural probe — required track, separate uncertainty

**First useful pilot: 6 / 12 hours total**, roughly D 1.5/3, L 0.5/1,
E 3/6 and O 1/2. This covers freezing the existing F04 hypothesis in F14,
ordinary training, a bounded development search, held-out intervention tests,
matched controls and a reproducible report. Compute waiting needs a separate
forecast after a hardware/runtime check; published GPU times are not this
host's budget. Preserve the supplied bounded-retry policy for native crashes.

At 2 / 4 hours, check that the task is learned well enough and that the
intervention/control pipeline behaves correctly. Failure there is a training
or measurement result, not a refutation of value representations. At 6 hours,
report the frozen pilot even if the result is null. Failure of the chosen
coordinate search is evidence about that search family only.

**A defended limited neural interpretation: 20 / 40 hours total**, conditional
on a promising or diagnostic pilot. Additional effort buys replication,
matched high-level alternatives, checks of apparent successes and possibly an
established distributed alignment method. A distributed extension requires its
own prospective intervention family and controls; it must not be tuned on the
pilot's held-out data. Confidence in an informative pilot is moderate;
confidence in a positive learned-cost interpretation is currently low.
The project can contribute a useful negative or identifiability result without
claiming that the network learned a unique utility or a general logic.
One concrete competing description is already visible in the target logit:
`log c_FN - log c_FP + log(eta/(1-eta))` predicts the same ordinary task
outputs without specifying separate internal J0 and J1 variables. F04's
interventions and competing-scale controls must do the discriminating work;
better ordinary predictive accuracy alone will not resolve this uncertainty.

### Relationship to the queue

A overlaps F11–F13 and the non-neural part of F14–F16; B covers an additional,
required F14/F15 track. Shared work must be counted once when tasks are actually
forecast. Neither package replaces Gate B, fresh F16 reconstruction, Gates C/D
or F17. A alone is **not a forecast for completing v2**. The existing small S8
compiler opportunity remains useful infrastructure if needed, but is not the
main novelty bet and does not warrant a separate research programme merely
because its implementation is straightforward.

## 4. Floors, usage budgets and recurrence

### What the measured work does and does not tell us

[F08's record](../work_logs/F08_2026-09-30_S1.md) credits D 90.589724 and
E 16.632667 minutes. Its overhead occupancy was not separated reliably into
engaged and unmeasured parts, so zero credited O does not mean zero overhead.
[F09's record](../work_logs/F09_2026-09-30_S1.md) credits D 60.091745,
E 13.773221 and O 10.118475, with 1.369596 minutes of tool wait and 10.661453
unmeasured, across a 96.014489-minute clock span. These are useful execution
anchors, but both stopped under protected-floor rules and included optional
extensions. They are not unbiased estimates of the minimum time needed for
their required results, and they do not establish a rate of novel discoveries
per hour. F10's final actuals belong in its linked work record.

The forecasts above are therefore broad priors based on existing infrastructure,
the checked antecedents and explicit work decomposition. In particular, the
high estimate for E in A allows for the current lack of integrated search and
an independent reference. B's high estimate allows for failures in task learning,
alignment selection and controls; extra training does not guarantee a positive
interpretation. Neither forecast is obtained by multiplying a published solver
speedup or an earlier theorem count.

### Assessment of protected minima

**L45 is a reasonable protected block for this audit and its optional ambition
calibration.** The core comparisons were drafted before the floor; the closer
retention, approximation and neural-method comparisons give the remaining
block a purpose. It would be too high as a minimum for every small source
lookup, and too low as a budget for establishing research priority across all
these areas. More literature time should be driven by the next concrete claim,
rather than a larger general bibliography.

The existing D60/D90 floors also look reasonable as protected exploration and
hostile-review blocks. The present evidence does not justify increasing every
floor. Their main risk is repeatedly generating elementary variants after the
useful boundary is clear. Use the remainder for a stronger alternative,
assumption challenge or discriminating application. A floor is not the budget
for a publishable result, and reaching it is not a novelty test. These are
recommendations; current task and gate minima are unchanged.

For future calibration, record a **core-ready checkpoint** when required
evidence first appears, then identify what the remaining protected block buys.
Keep the original central/high forecast and record which uncertainty caused an
overrun. Three to five comparable blocks will be more informative than treating
these few floor-constrained tasks as a stable productivity rate.

### Converting a weekly allowance into a useful work plan

Usage percentages have not been measured for F08–F10. Do not reconstruct them
from clock time or assume a constant minutes-per-percent conversion. For future
work, pair available account-usage readings around representative D, L and E
blocks, recording model/settings, reset boundaries and other concurrent account
use. A reset or confounded interval cannot be assigned to this task cleanly.
Use a small range of observed costs per **completed milestone**, alongside
engaged hours and waiting, rather than a single tokens-to-research formula.

Keep the protocol's existing two axes: D/L/E by research mode and R/X by
reliability of gain. The current cycle-II allocation remains D/L/E 60/10/30
through Gate B. The gate should prospectively budget cycle III's implementation
and neural work; an empirical-heavy cycle can be justified explicitly instead
of relabeling implementation as derivation. Preserve the reliable/exploratory
balance and roughly 25% recurrence reserve. No new permanent quota is proposed.

For illustration, **20 available engaged hours** is a planning assumption,
not an estimate of a week's account allowance. Set aside about 5 for recurrence
and commit at most 15 initially. Plan the 4-hour and then cumulative 8-hour
milestones, keeping room for prerequisites, integration and the next scope
increment. Fifteen initially committed hours cannot promise the 16-hour rung
plus gates. If the measured allowance supports only 6–8 hours, aim for a sound
first checkpoint and a bounded scope extension with its evidence. With more
allowance, advance both the result set and its support along the ladder;
replication alone is not the default use of every larger budget.

Use the high estimate as a replanning boundary, not a promise to keep spending
until success. A full budget is best used when the next block can change a
decision: confirm a useful result, expose its boundary, or reject an expensive
direction. More tokens or elapsed time without such a discriminator is not
automatically greater ambition.

### v2 recurrence versus v3

Finish the existing v2 evidence route before selecting a new carrier merely
because its ingredients are familiar. A successful scoped result can combine
standard methods. Recur within v2 for an incorrect certificate, an inadequate
baseline, a failed useful-derivation criterion, or a better bounded revision
test; follow the named-repair and gate rules when claims become stale.

Consider v3 when a concrete result makes a materially broader contract worth
the cost: changing row directions or learned model weights rather than only
RHS values; richer statistical evidence and utility calibration; or genuine
cyclic self-assessment rather than the current staged fragment. First request
a 3 / 6-hour feasibility comparison against the closest established method,
then forecast the larger programme from that evidence. These are options, not
verified open problems or commitments. If A reveals no special advantage over
a straightforward existing combination, that should lower the next ambition
or redirect the application, not trigger a cosmetic new version.

## 5. Planning checks derived during F10

These are local arguments used to delimit the proposed work, not new core
theorems, independent reviews, or claims of priority.

### P1. All-RHS exactness can make every affine dual vertex necessary

For the single affine query `sup{a^T x : A x <= eta}`, let
`D={lambda>=0 : A^T lambda=a}` and take a vertex `lambda` with positive
support S. The supported columns of `A^T` are independent: otherwise a small
move in both signs of a supported kernel vector contradicts extremality.
Choose `eta_i=0` on S and `eta_i=1` elsewhere. The source is feasible at
`x=0`. This certificate has budget zero and is optimal by weak duality.
Any distinct point of D must have a positive coordinate outside S, since the
equation restricted to S has a unique solution. Its budget is therefore
strictly positive. Thus deleting this vertex from a **finite explicit
catalogue of dual certificates** loses exactness at this admitted RHS.

This is a standard polyhedral argument reconstructed here. It does not prove
a memory lower bound for all representations: a compact program may factor or
reconstruct certificates. Nor does it show that every full CPWA-clause vertex
is necessary, since fixed leaf offsets and outer extrema can hide pieces.
It does show why a blanket promise to prune an arbitrary affine catalogue
while preserving every feasible RHS is a poor research target. Declare a
restricted revision family, tolerate a certified precision cost, exploit
structure, or allow new search. Those choices are the early discriminator in A.

### P2. Transporting a distributed patch may require an oblique projection

For an orthogonal hidden-space projector P, a donor patch is
`h*=(I-P)h_base+P h_donor`. Under an invertible positive diagonal neuron gauge
`h'=D h`, the same intervention is represented by `P'=D P D^-1`.
It is idempotent but need not be symmetric. For example,

    P = [[1/2,1/2],[1/2,1/2]], D = diag(2,1)
    P' = [[1/2,1],[1/4,1/2]].

Refitting an orthogonal projector onto the transformed direction would change
the intervention. Coordinate-subset projectors commute with diagonal D and
therefore avoid this issue; permutations simply relabel them. C01's general
invertible-map definition accommodates transport, while its implemented
orthogonal search family need not be closed under this gauge. This is an
adaptation cost for B's optional distributed extension, not a defect in the
existing F04 coordinate-subset design or a refutation of DAS. Preserve the
intervention itself when testing gauge invariance, with numerical tolerances
handled separately.

### P3. A last-layer cost patch naturally acts on log cost

In F04's architecture, write the logit as `f(z)=b+w^T h(z)` and the
contribution of a selected hidden-coordinate subset S as `g_S(z)=w_S^T h_S(z)`.
Patching a donor d into a base r changes the logit by `g_S(d)-g_S(r)`.
The ideal weighted-loss logit is `f*(z)=log J0(z)-log J1(z)`. Thus an exact
J0-only interchange requires

    g_S(d)-g_S(r) = log J0(d)-log J0(r).

If all pairs in a domain are tested, this makes `g_S=log J0+constant` there.
For a restricted pair family, the constant need only agree within its connected
components. More practically, if base task logit error is at most e_T and
patched logit error at most e_I on a pair, subtracting those two errors bounds
the discrepancy in this displayed equation by `e_T+e_I`.

A one-coordinate representation with an affine raw-J0 decoder cannot satisfy
both exact conditions over a nontrivial interval: it would make log J0 affine
in J0. Larger subsets and approximate conditions are different questions.
Finite ReLU models also only approximate the ideal smooth logit; the experiment
must use frozen tolerances, not require impossible exact continuum equality.
Probability and logit error are different metrics, especially near 0 or 1.

This is a diagnostic for F14, not a new training objective or an executed
experiment. A predeclared log-cost decoder, with the corresponding inverse
link when reporting cost, is a reasonable comparison to the existing affine
raw-cost decoder. It still needs matched controls and causal intervention
agreement. P3 makes the pilot more informative by separating a restrictive
measurement choice from failure to learn the proposed task structure.

### P4. Whole-certificate coverage is simpler than fragment retention

Fix a finite development workload of revision/query pairs d, nonnegative
weights w_d, and a finite candidate set of complete replayable proof schemes.
Let c_dp be 1 when scheme p independently yields an accepted proof of d's
specified threshold after replay, and 0 otherwise. Acceptance includes current
source versions, units, cases and the literal request. These values must be
fixed independently of the selected set S. Define

    F(S) = sum_d w_d max({0} union {c_dp : p in S}).

This is C11's established coverage form. The marginal gain from adding p at
d is zero if S already covers d, and w_d*c_dp otherwise. Adding other schemes
can only reduce that marginal gain. Summing proves monotonicity and
submodularity; F(empty)=0. Under a positive integer limit k of whole schemes,
C11's greedy
guarantee applies to this finite objective. It says nothing about unseen
revision frequencies, total runtime, or an optimum over all possible proofs.
Construction of the candidate set and evaluation of c_dp must be charged.

Two small obstructions delimit the adaptation:

* If fragments p and q are jointly needed to complete one proof, its coverage
  can be 0 for empty, {p}, and {q}, but 1 for {p,q}. This violates
  `F({p})+F({q}) >= F({p,q})+F(empty)`. The score concerns reuse without new
  search; freely regenerating missing fragments would change that contract.
* Even with whole schemes, protecting the worst covered demand can have the
  same table: p covers only d1 and q only d2. Taking minimum coverage over the
  two demands introduces complementarity. An average-coverage guarantee must
  not be presented as preservation of every admissible query.

Variable proof sizes and shared DAG nodes also make cardinality different
from retained bytes. A whole-scheme baseline can still be useful, with its
actual storage and checking costs reported; optimizing shared fragments under
a byte budget is a separate problem. This is a scoped reuse of established
optimization, with local counterexamples to overextension. It supports A's
small first attempt and does not claim a new greedy theorem, select the final
F14 metric, or implement a portfolio optimizer.
