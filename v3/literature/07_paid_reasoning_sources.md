# P3-07 — paid reasoning: primary sources and comparison scope

Contributor: **ChatGPT (GPT-6 Astra Pro), same-model internal literature
reviewer**, October 9, 2026 UTC. Starting repository base:
`c7386f115bf60a9eb3a419515c844b81fc6ba073`.

Status: **selected primary-source verification and prospective import
contract**. This is a targeted comparison for P3-07, not a systematic review
or a worldwide-priority finding. The principal derivation, implementation
verification and task disposition have their own records. Agent time supplies
no principal Research90 credit. All executable P3-07 evidence is development.

Read with [the problem contract, §6](../foundations/01_problem_contract.md),
[the existing source contracts](01_source_contracts.md), and the
[internal review](../work_logs/P3_07_2026-10-09_S1/reviews/literature_review.md).
The [retrieval manifest](../work_logs/P3_07_2026-10-09_S1/sources/literature_agent/source_manifest.json)
records exact URLs, locators, retrieval references and local source hashes.

## 1. The comparison this task needs

P3-07 asks for a bounded choice among acting, using a fallback, and buying
specified further computation. The interesting implementation question is how
the reasoner obtains useful estimates of the consequences of those choices,
including its own procedure, under the declared resource account. A known
conditional law can define an ideal decision problem; it does not pay for
learning, evaluating or validating that law.

The proposed restricted route is a finite catalogue of complete policies fixed
before profile sampling. Each policy contains its permitted computations and
terminal behavior, so a beneficial sequence can be represented even when its
first step alone would not change the terminal action. IID draws of bounded
mathematical-query tasks supply paid, complete observations of paired raw
loss/resource features. Simultaneous coordinate bounds then support selection
and linear repricing within that catalogue. A newly assembled controller is
assessed on a separate cohort after its whole relevant state has been fixed.
These are the principal's prospective assumptions, not conclusions already
established by the literature review.

The closest ordinary comparator combines metareasoning, empirical procedure
profiles, concentration bounds and a fixed-procedure audit. Its empirical law
can be represented by observed profile rows or by the sufficient means and
intervals used by the proposed method. It need not first infer the truth
probability of every current arithmetic sentence. The cost-oriented and
probability-oriented implementations must receive the same initial information,
acquisition opportunities, policy catalogue and resource terms. Each pays for
its own acquisitions; a conditional replay of a common paid history answers a
different question from an end-to-end acquisition comparison.

## 2. Inspected primary interfaces

### PR07-1 / S03 — the supplied-law metalevel decision problem

Nicholas Hay, Stuart Russell, David Tolpin and Solomon Eyal Shimony,
[*Selecting Computations: Theory and Applications*](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf),
UAI 2012, 10-page author PDF. Inspected **§2, Definitions 1–3, Theorems 4–5,
Definition 6, Theorems 7 and 9, Example 3 and Theorem 10; §3, Example 4**.
PDF pages 2–5 contain these passages; named locators control. The
[2012 archival record](https://arxiv.org/abs/1207.5879) was checked.

Definitions 1–3 use jointly distributed utilities and computational results,
history-dependent permitted computations, priced continuation, and a terminal
choice. The text explicitly allows adding time or expenditure to the state.
Theorem 5, under bounded utility and positive constant per-computation cost,
bounds expected computation and establishes almost-sure stopping. Example 3
permits arbitrarily long finite runs; it does not give positive probability of
endless computation under those assumptions. Theorem 7 supplies only the
one-way implication from myopic continuation to optimal continuation; Theorem
9 needs a transition-closed stopping region. Theorem 10 is specialized to its
one-armed Bernoulli model. Example 4 blocks a general independent-arm index rule.

**Import:** the decision-model interface and these stopping boundaries. Latent
profile parameters and evidence about them can be included in a supplied joint
model. Learning that model efficiently remains an additional implementation
obligation. No specialized sampling bound is imported for bounded proof search.

### PR07-2 — learning and assessing one's own computations already have a history

Stuart Russell and Eric Wefald,
[*Principles of Metareasoning*](https://people.eecs.berkeley.edu/~russell/papers/aij-principles.ps),
author-hosted PostScript linked from the
[author's publication page](https://people.eecs.berkeley.edu/~russell/research-bo.html)
as Artificial Intelligence 49 (1991). Inspected the **32-page author
manuscript: §3, p. 6; §§3.1–3.2, pp. 7–8; §5.1.1, pp. 14–15;
§§5.4.1–5.4.2, pp. 19–21; §7, pp. 27–28**. The source was downloaded,
converted locally and its pp. 20–21 visually checked; these are manuscript
pages, not journal pagination.

The paper already addresses metareasoning regress, statistical evaluation of
computations, and probabilistic self-modelling. Section 5.4.1 observes that
learning new control knowledge changes the agent whose behavior generated the
data. Its possible adaptive convergence is discussed prospectively. Section
5.4.2 supplies a probabilistic description of future choices, and explicitly
states that its proposed probability/conditional-utility estimation was not yet
implemented there. Section 3's footnote holds the actual utility function fixed.

**Import:** the conceptual antecedents and the distinction between a procedure
and estimates of it. A fresh bounded audit of a named version needs its own
statistical premises. This reading supplies no convergence or unrestricted
self-trust theorem. P3-07's external repricing contract must be stated directly.

### PR07-3 / S20 — conditional performance profiles and their acquisition

Shlomo Zilberstein and Stuart Russell,
[*Optimal Composition of Real-Time Systems*](https://people.eecs.berkeley.edu/~russell/papers/aij-anytime.pdf),
Artificial Intelligence 82, 181–213 (1996), 38-page author manuscript.
Reopened **Definitions 2.1–2.6; §§2.2.1–2.2.3; §4's setup;
§4.2, Theorems 4.6–4.7**. Relevant PDF pages are 5–9, 20 and 24–27.

Definition 2.5 conditions an output-quality distribution on input quality and
allocated time. Section 2.2.3 permits analytical acquisition or statistics from
sampled instances, discusses matching the deployment population, and exposes
representation/approximation choices. Section 2.2.1 warns that component
expectations do not in general determine an expected composite quality.
Section 4 assumes fixed profiles for by-value, side-effect-free functions.
Theorem 4.6's local composition result uses tree structure and input
monotonicity. Theorem 4.7 adds bounded degree and measures complexity against a
discrete time horizon; it is not polynomial in that horizon's encoded bit length.

**Import:** procedure-specific acquired profiles are a strong ordinary
comparator. The static composition theorems do not establish a learned
controller's calibration or survival after an arbitrary change. Conditioning
on inaccessible true input quality would also violate P3-07's observation
contract. The earlier [profile/access review](../work_logs/P3_01_2026-10-07_S1/reviews/acquisition_and_profile_boundary.md)
retains its separate reuse and repeated-subexpression boundaries.

### PR07-4 — a learned metalevel policy with explicit deployment overhead

Frederick Callaway, Sayan Gul, Paul Krueger, Thomas L. Griffiths and Falk Lieder,
[*Learning to select computations*](https://auai.org/uai2018/proceedings/papers/269.pdf),
UAI 2018, 10-page proceedings PDF. Inspected **§§2.1–2.3;
§3, equations (2)–(5); §§5.1–5.2**, PDF pages 2–4 and 8–9.

Bayesian metalevel policy search learns weights in a value-of-information
feature approximation through policy search. Its state and transition model
describe how computation changes beliefs. The feature construction uses
myopic information value, perfect information and a designed relevance
function. Section 5.1 explicitly divides a finite deadline between object-level
simulation and online metareasoning. It excludes offline training from that
deadline equation. Section 5.2 then identifies repeated use as an opportunity to
amortize training. Its reported empirical comparisons are not reproduced here.

**Import:** learned computation selection, controller overhead and training
amortization are existing ideas. The supplied-model feature calculations and
empirical demonstrations do not establish P3-07's simultaneous certificate for
paid mathematical-query profiles. A fixed complete-policy catalogue also need
not equal the much larger class of metalevel policies considered in that model.

### PR07-5 — online prediction of an anytime procedure's performance

Justin Svegliato, Kyle Hollins Wray and Shlomo Zilberstein,
[*Meta-Level Control of Anytime Algorithms with Online Performance Prediction*](https://justinsvegliato.com/s/SWZijcai18.pdf),
IJCAI 2018; [proceedings record](https://www.ijcai.org/proceedings/2018/208).
Inspected **§§2–4, Definitions 1–9 and Algorithm 1; §5's predictor;
§5.1's quality observation**, PDF pages 2–5.

The procedure predicts future quality from an observed history within one
instance and stops according to myopic or nonmyopic projected improvement.
Algorithm 1 explicitly reads current solution quality. Its experiments employ
a nonlinear regression predictor; where optimal solution cost is unavailable,
§5.1 estimates quality using a problem-dependent lower bound. The projections
are estimates used for control. The inspected definitions and algorithm do not
provide a simultaneous finite-sample coverage theorem for arbitrary profiles.

**Import:** adaptively estimating how much further computation will help is
already an implemented ordinary strategy. A proof-search timeout or a fallible
logical answer is not automatically an observable graded-quality signal. Any
P3-07 use must define how profile quality is obtained, what is only a proxy,
and what computation and checking are charged.

### PR07-6 — the concentration inequality actually needed

Wassily Hoeffding,
[*Probability Inequalities for Sums of Bounded Random Variables*](https://www.csee.umbc.edu/~lomonaco/f08/643/hwk643/Hoeffding.pdf),
JASA 58(301), 13–30 (1963), institutional mirror of the original 18-page scan.
**Theorem 2, equation (2.6), printed p. 16 / PDF page 4**, was visually
verified after local rendering. The theorem concerns independent bounded
summands and need not assume that they have identical distributions.

For the paired design, apply this theorem directly to the per-task difference.
The adjacent equation (2.7) concerns two independent samples; it is not the
justification for correlated evaluations of two policies on the same task.
Both signs and the finite family of coordinates require their stated error
allocation. This is a fixed-sample theorem; adaptive continuation of data
collection requires additional coverage control. No new concentration result
or arbitrary dependent-sample guarantee is imported.

### PR07-7 — a selected policy and a separate assessment cohort

Philip S. Thomas, Georgios Theocharous and Mohammad Ghavamzadeh,
[*High Confidence Policy Improvement*](https://proceedings.mlr.press/v37/thomas15.pdf),
ICML/PMLR 37, 2380–2388 (2015). Inspected **§2's bounded-return setting;
§4's multiple-comparison discussion and Algorithm 4**, PDF pages 2 and 5.

The method separates candidate-policy search on training data from one
acceptance assessment on held-out data. Algorithm 4 returns its candidate
only if the assessment's lower bound clears a specified threshold. The paper
distinguishes its concentration-inequality variant from variants using a
t-test or bootstrap approximation. This distinction matters when importing a
finite-sample guarantee.

**Import:** separating selection from final assessment is an established
comparison for the proposed frozen-controller audit. This paper uses an
off-policy trajectory setting. P3-07 can instead evaluate the fixed controller
directly on fresh complete tasks and reconstruct its own bound. Neither reuse
of the audit for unrestricted retuning nor a new procedure version is covered
by a guarantee for the first selected candidate.

### PR07-8 — a boundary comparator for selectively observed profiles

Nikos Karampatziakis, Paul Mineiro and Aaditya Ramdas,
[*Off-Policy Confidence Sequences*](https://proceedings.mlr.press/v139/karampatziakis21a/karampatziakis21a.pdf),
ICML/PMLR 139, 5301–5310 (2021). Inspected **§1, equation (1);
§2's bounded weights/rewards; §3, Definition 1 and Theorem 1**, PDF pages 1–3.

The selected setup uses contextual-bandit observations, a target policy
absolutely continuous with respect to the behavior policy, and known
importance ratios. Predictable nonnegative betting processes produce
confidence sets uniform over sampling time. Such guarantees address optional
stopping that an unadjusted fixed-sample interval does not.

**Import:** a stronger ordinary alternative exists if P3-07 later changes to
selected-action observations or repeated testing. Its overlap, observation,
boundedness and conditional-moment premises would have to be established in
that new experiment. A log containing only chosen computations and their
successes does not acquire those premises automatically. The present
complete-policy, fixed-sample profiling design does not need importance
weighting. No off-policy theorem is claimed for it by analogy.

### S21 — inherited probabilistic-numerics boundary

Hennig, Osborne and Girolami's
[*Probabilistic Numerics and Uncertainty in Computations*](https://arxiv.org/pdf/1506.01326v1)
remains an inherited comparator through the existing
[primary-source note](../work_logs/P3_01_2026-10-07_S1/reviews/probabilistic_numerics_boundary.md):
PDF **§§2(a)–2(c), equation (2.5), §§3(a)–3(d)**. P3-07 reuses the
distinction among a point estimate, model-conditional uncertainty, an analytic
bound and population coverage. Fresh arXiv/royal-society opens failed and PMC
returned a browser-check page in this review. Accordingly, no new S21 primary
reading or extra theorem import is claimed, and P3-01's inspected normalization
caveat is preserved without redoing it.

## 3. A bounded contract that these sources make worth checking

The following are applications to the principal's proposed design. They should
be proved or checked in the P3-07 derivation and executable evidence; their
listing here does not certify an implementation.

### 3.1 Complete policies, rather than a free optimal continuation

A catalogue item specifies what happens after every permitted observation,
including failure, refusal and timeout. The terminal action is chosen using
only the resulting visible history. Its initial action may buy an entire
bounded contingent procedure. Thus its value can include multiple useful
steps without evaluating an unspecified optimal future policy.

This restricts the comparator class. A lower bound on one catalogue item's
advantage warrants that item relative to the stated baseline under its task
distribution. It does not establish that the first computation is best among
every possible reasoning strategy. A computation with nonpositive immediate
benefit can still be a useful prefix of a complete plan. Conversely, a failed
certificate says the available evidence does not establish the required
advantage; it does not prove further reasoning has zero value.

An ordinary implementation can execute exactly the same finite policies.
When its empirical cost is computed from the same feature means, algebraic
equality of the two selectors is an appropriate result. Extra syntax or a
different name for the common score does not by itself distinguish behavior.

### 3.2 Simultaneous paired features support a precise repricing service

Let `K` complete policies and `d` feature definitions be fixed before `n`
sampled tasks, with sample size and failure budget `delta` predeclared. For
each policy `pi` and coordinate `j`, set
`D_(i,pi,j) = z_stop,j(X_i) - z_pi,j(X_i)` with deterministic bounds
`a_(pi,j) <= D_(i,pi,j) <= b_(pi,j)`. All quantities needed to observe these
features must actually be obtained under the paid contract.

With IID rows from the declared population, a direct two-sided application
of PR07-6 followed by a union bound gives the common event

```math
\left|\widehat\mu_{\pi j}-\mu_{\pi j}\right|\leq\epsilon_{\pi j},\qquad
\epsilon_{\pi j}=(b_{\pi j}-a_{\pi j})
\sqrt{\frac{\log(2Kd/\delta)}{2n}}
```

with probability at least `1-delta`. On that event, elementary linear algebra
gives, simultaneously for every price vector in the same feature contract,

```math
\lambda\cdot\mu_\pi\geq
\lambda\cdot\widehat\mu_\pi
-\sum_j|\lambda_j|\epsilon_{\pi j}.
```

This is a standard concentration-plus-linear-readout adaptation. Dependence
among policies or coordinates **within** one sampled row is allowed. If a
difference lies in `[-R,R]`, its interval width is `2R`. Row independence is
the relevant assumption, not independence of the two paired evaluations.

The same event permits selecting a catalogue member or a price vector after
seeing the profile. It does not permit silently changing the catalogue,
query population, feature meaning or computational state. In particular,
if prices change a policy's internal behavior, its induced feature vector
has changed: all such behavior maps need to be in the certified class, or the
new policy needs new evidence. A population mean bound also does not become
a guarantee conditional on an arbitrary newly selected individual query.

### 3.3 A procedure identifier is part of the statistical target

For the proposed audit, fix the whole controller before drawing an independent
audit cohort. Relevant identity includes executable code, learned profiles,
configuration, feature extractor, checker, scheduler, accessible advice and
cache/reset state. A code hash alone may omit part of that target.

Conditioned on this frozen construction history, the audit can treat the
controller as a fixed function and apply an appropriate bounded-sample result.
The interpretation remains performance on the declared task distribution and
budget. It does not certify the answer to each unresolved mathematical
sentence, all future versions, or the controller's claims about itself.

IID task draws do not suffice if a shared mutable cache or learner changes the
feature-generating mechanism across audit rows. Supply an episode reset or a
separate dependence-valid argument. After a failed audit, using that same
cohort to tune and repeatedly re-test new versions also changes the selection
problem. A fixed catalogue with simultaneous coverage, fresh samples, or an
appropriate sequential method would define different admissible remedies.

### 3.4 Setup, deployment and feasibility answer different questions

Record the full costs of obtaining profile labels, running every evaluated
policy, checking outputs, constructing features, fitting or aggregating the
profile, storing it and selecting a policy. Computational actions that construct
a dependency model or search a repair catalogue belong in this account when
used. A claimed reuse right must identify the retained object and the cost of
its access and checking.

A conditional deployment comparison may treat an already acquired profile as
sunk; an end-to-end comparison includes its acquisition. A declared horizon
`H` can amortize setup, but the horizon is an assumption of that comparison.
Show the setup amount as well as the amortized term. Each policy's hard
resource feasibility remains a separate requirement even when its expected
priced gain is favorable. Neither a mean resource estimate nor an average
performance audit establishes a worst-case execution cap.

If a task remains unresolved at the permitted horizon, record that outcome
honestly. A fixed-horizon bounded-program decision can have a fully checkable
label when its prescribed execution is completed; a prematurely interrupted
run cannot be relabeled as a refutation. Removing difficult unresolved tasks
from the profile silently changes the certified population.

## 4. Result classification

| Component | Appropriate classification for this task |
|---|---|
| Act, fallback, or buy with a modeled terminal payoff | Ordinary metareasoning interface; a fallback is an ordinary terminal action. |
| Learned quality or utility profiles for computations | Established procedure-selection idea. |
| Multi-step value represented by a fixed complete procedure | Restricted policy evaluation; expressiveness is limited by the declared catalogue. |
| Finite simultaneous mean bounds and linear repricing | Standard statistical and algebraic adaptation, with a checkable event and explicit class. |
| Assessment of the controller's own named version | Empirical procedure assessment; the freeze, sampling and reset contract define what it covers. |
| Checked links among these estimates, paid mathematical evidence and version changes | A specific integration to derive and test; any claimed advantage needs matched ordinary controls. |

The review supports using these sources as the closest comparators and
building a finite conditional result around them. It does not establish a new
general metareasoning principle, a universal optimal policy, a logical-truth
learner, or global novelty. The existing P3-N01 disposition is unchanged by
this source review.
