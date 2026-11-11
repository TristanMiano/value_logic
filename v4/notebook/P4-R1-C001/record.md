# P4-R1-C001: recursive judgment and task recovery

**Contributor:** Claude (Fable 5.2). **Opened:** November 9, 2026.
**Authorization:** Tristan Miano, November 9: "You can now begin P4-R1-C001
with the 240 minute floor." **Module:** P4-R1 / W1. **Theses:** C1, C2 (C5 later).
**Example:** the abstract judgment core, exhibited in the physics-task instance
([M0.2 decision](../../decisions/2026-11-09_running_example.md)).
**Floor:** 240 engaged research minutes, no override. Observed clock:
[timing.jsonl](timing.jsonl), tool [clock.py](../clock.py). Exploratory notebook
record; stated results go to [results](../../results/).

## Thesis in the author's terms

"Judgment is itself a task. A judge can be judged." A good judge predicts that
a performer who did well at T will do well at T again, and that requires
knowing what T is: "a judge who cannot tell the difference between T, U, and V
will make bad predictions." So judging judges forces recovery of the real
boundaries between task types (C1), and delineating tasks and judging judgments
are one operation, T = J² (C2). "Yes" means "I expect it to reappear."

## Kernel hypothesis

A judgment is a forecast of recurrence. Judging the judge scores that forecast
against the later outcome. A forecast must generalize from past instances to a
future one, and the judge's task delineation is exactly its rule for which past
instances bear on which future ones. Hence the second-order score is a function
of the delineation, and the delineations it rewards are the ones that respect
real differences in how skill transfers. The mechanism needs the performer to
*reappear*; without recurrence there is nothing to generalize.

## Candidate readings (faithfulness / defensibility)

| | Reading | Faithful? | Provable? |
|---|---|---|---|
| R0 | T = J∘J as functions | Literal | No common type; refuted as stated in phase one. Boundary marker only. |
| R1 | **T = argmax J²**: rank delineations by the best second-order score they support; the optimal ones are exactly those that separate every pair of task types with different skill transfer | High: keeps direction (judging judges ⇒ delineation), objects and the surprising part (facts recovered from value) | Credible: sufficiency plus a strictness argument |
| R2 | **T = symmetry of the J²-optimal judge**: every judge implicitly delineates tasks by what it treats as interchangeable; for the optimal judge that relation is the factual one; partition ↦ judge ↦ partition has the factual partition as its unique optimal fixed point | Higher: gives the mutual determination C2 asks for | Credible given R1 |
| R3 | Judges weighted by other judges, no outcome oracle; coupled fixed point of weighting and delineation; grounded versus self-confirming equilibria | Highest: this is the essay's society of judgers | Open; needs R1/R2 first, then independence or anchoring conditions |
| R4 | "Sufficiently good judges carry some task information" (phase one F.4) | Low: weaker conclusion, already proved | Done |

Start with R1 and R2, which sit strictly above R4 and have a path to proof;
R3 is the named obligation they leave. Spending: R1/R2 assume an evaluator
with outcome access and score the *best* forecast a delineation supports.

## Declared model, quantifiers, comparison

Performers with latent skill θ ~ P; task instances x with type z(x), drawn
independently of skill; outcome Y ~ f(· | θ, z); conditional independence
across performances. A judge with delineation c sees a performer's n past
(cell, outcome) pairs and the target's cell, and forecasts the target outcome.
J² is expected log score. Quantifiers: all delineations c, all n ≥ 0, all
finite outcome sets, arbitrary skill law. Comparison: (a) no recurrence
(n = 0, or performer identity unlinked), the "first-order" baseline given the
same outcomes; (b) equally informed non-recursive methods (latent-class and
co-clustering identifiability). Constructive targets: exact recovery
statement, the threshold n at which it starts, an instance in the physics
world. Limiting targets with repairs: no skill variation, unlinked identity,
skill-dependent task selection, suboptimal judges, duplicated labels.

## Forecast and directions

Rough forecast: 240 to 300 research minutes over several sessions; overhead
30 to 45 minutes. No result is promised. Directions, revisable:
1. Type the core; prove or break R1; find the recurrence threshold.
2. R2 fixed point. 3. Exact numerical check on small worlds, including a
   tolerance-dependent physics instance. 4. Literature: latent block /
   exchangeable-array identifiability, Dawid–Skene, peer prediction.
5. Stability (near-optimal judges recover approximately), then R3.

## Session log

### S1, 2026-11-09 (Claude, Fable 5.2)

**Alignment first.** C1 moved forward at a restricted scope: with an outcome
evaluator, judging judges recovers exactly the transfer facts that judging
performances without reappearance cannot. C2 moved forward: a typed
judge/delineation correspondence with the factual partition as its unique
optimal fixed point. C5 did not move. The headline cannot be stated without
judgment and value, and no thesis was weakened or renamed.

**Done.** Typed the core model. Proved R1 (Theorem 1), a stability bound
(Theorem 2) and R2 (Theorem 3); proved the no-reappearance limit and the
identifiable-assignment repair for skill-dependent task choice. Exact checks
on designed, physics and random worlds. Bounded literature comparison. Stated
in [R1.1](../../results/R1_recurrent_recovery.md).

**Raw findings worth keeping.** (1) The whole gain from difficulty to
transfer happens at the first reappearance; nothing in the statement needs
long histories. (2) Merge deficits are not monotone in history length
(22 of 1,200 cases). (3) With skill-dependent task choice, specialists who
never leave their niche make distinct tasks indistinguishable; 1% random
assignment already restores a deficit. (4) In the physics instance the
recovered task partition changes with the tolerance of judgment.

**Interpretive choice the author should confirm.** "First-order judgment
cannot" is read here as "judgment without reappearance of the performer,
given the same outcomes." A first-order table of approvals with performer
identities does contain the transfer facts; extracting them means scoring
which judgments predict which later ones, which is the second-order score.

**Self-review (aim balance).** Readings R0 to R4 were laid out before work
and the two most faithful provable ones were pursued; conditions added (an
outcome evaluator, tasks met independently of skill, best forecast per
delineation) are named in the result with their repairs or open status.
Construction and limits both received work: three theorems, two limiting
propositions, and probes that produced unwelcome facts (non-monotone
deficits, failure under specialist selection). Identified risks: the core of
Theorem 1 is close to known sufficiency results, so its novelty may be
overstated, which section 7 of the result tries to bound without a full
literature reconstruction; the model was chosen where the construction
works, which the selection probe only partly offsets; proofs and checks come
from one model in one session. Possible risk: the reading of "first-order"
above is the one under which the thesis holds cleanly. This is a
self-review and does not guarantee impartiality.

**Observed time.** 302,977,203,168 ns of D+L+E, which is 5.05 minutes
(D 3.87, L 0.21, E 0.97), plus 1.58 minutes of administration, across 11
observations in one runtime. Derivation done before the first observation
is unobserved and uncredited. **Floor remaining: 234.95 minutes.** At this
rate of work per observed minute the floor corresponds to several dozen
sessions of this size; the author has been asked how to treat it. The cycle
stays open and unfinished.

**Next move on resume.** R3: judges weighted only by other judges. Use
conditional independence of judges given outcomes (Kong and Schoenebeck's
mutual-information results; three-view latent-class identifiability) to seek
conditions under which every fixed point of the coupled weighting and
delineation is grounded, and construct the self-confirming fixed points that
correlated conventions allow. Then: judges who learn outcome laws from
finite data (does a needless split now cost score?), a stability bound for
general n, and whether unflagged random assignment suffices.

### S2, 2026-11-09 (Claude, Fable 5.2)

Author direction on resuming: "Keep working ... just keep updating your
branch periodically." The literal 240-minute floor stands.

**Alignment first.** C1 moved forward: the outcome evaluator of S1 is
removed when approvals are honest garblings of what happened, and a single
better-than-chance judge checked against its own later approvals suffices.
C2 moved forward: the mutual determination is now between the set of
credited judges and the delineation, with a lattice of fixed points and a
bootstrap, which is closer to the essay's society of judgers than S1's
single optimal judge. C5 first contact only (judging is an instance of the
same core). No thesis was weakened.

**Done.** [R1.2](../../results/R1_judges_without_oracle.md): Theorem 4
(approvals as their own outcomes), Proposition 6 (agreement is not
vindication), Theorem 5 (support/delineation fixed points; largest fixed
point; bootstrap; exploration), constructed self-confirming states,
Theorem 6 (bounded judges select the transfer partition itself; resolution
grows with experience), Proposition 8 (self-application). Scripts
`judge_society.py`, `local_judges.py`.

**Unwelcome facts kept.** A society that starts with no distinctions can
settle on reputation alone (world F). Vindication certifies tracking of
persistent traits, not of skill. An informative judge's task-dependent bias
enters the fixed-point delineation. Under pure specialisation, ignorance is
self-consistent.

**Self-review (aim balance).** The reading pursued (R3) is the most faithful
one listed at the start; its conditions (B1, B2, mediation for the link to
fact, history length one for vindication, supports instead of weights) are
named. Constructions and limits were built together: the worlds were chosen
before running to include a fashion pair, a pure convention, a biased
informative judge and reputation, and three of them produced fixed points I
would have preferred not to exist. Identified risk: Theorem 5 is light
mathematics (monotone maps on a finite lattice) and its weight rests on
whether the two maps are the right formalisation of the essay's J² and T,
which is an interpretive judgment for the author. Identified risk: "largest
fixed point" could be read as "the true one"; the result says explicitly
that it is not, in general. Possible risk: worlds are small and designed by
the same model that proved the statements. Self-review only.

**Next move on resume.** (1) Separate fact from shared stable bias:
communities with different biases (what all distinguish), and an anchor in
consequences, which hands off to W6/W7. (2) Excellence centroids (W1.5):
judges with different criteria over multi-attribute objects; which objects
are ever chosen, what the chosen set reveals, what nonlinear criteria add.
(3) Graded weights and update dynamics; vindication with longer histories.
(4) From S1: stability bound for general n; unflagged assignment.

**S2, continued.** [R1.3](../../results/R1_excellence_exemplars.md) takes up
the tree argument (W1.5): the set of objects ever picked as best is the same
for every diverse population of judges; with shared causes it depends on the
criteria only through the cone of the transfer kernel; an explicit count for
planar Gaussian causes; linear versus min-type judges. Mostly standard
ingredients, assembled as the kernel of the tree argument and tied to R1.1.
Two defects in the first simulation run (memory, and a reused loop variable
that silently disabled one comparison) were found and fixed before any
number was recorded. C1 moved slightly; the "great judge" who recovers why
the dimensions are connected is still open. Self-review: the exact
low-rank assumption does most of the work, and the result says so; the
unwelcome column (idiosyncratic components enlarge the set) is reported
beside the favourable one.

**Observed time, cumulative after S2.** 1,142,371,825,989 ns of D+L+E, which
is 19.04 minutes (D 17.75, L 0.21, E 1.08). **Correction applied:** three E
intervals totalling 1,673,922,558,208 ns (27.90 minutes) were spent waiting
on the exemplar simulation and are removed in full by an appended exclusion
record; they are not engaged research under the recurrence procedure. Long
computations will run under mode O from now on. One interval is uncredited
because it spans the pause between sessions and a change of runtime.
**Floor remaining: 220.96 minutes.** The cycle stays open.

### S3, 2026-11-10 (Claude, Fable 5.2)

Author direction: "The latest work has been merged. You can continue working."

**Alignment first.** C1 moved forward on the point where S2 stopped: among
judges who respond to performances, the part of their judgments that does
not depend on their conventions is identified exactly. It is the transfer
geometry of tasks; difficulty is the part confounded with convention. The
"great judge" of the tree argument gets a precise object (the matrix of
transfer correlations) and R1.3's open item on recovering the causes is
closed up to rotation. C2 and C5 did not move this session.

**Done.** [R1.4](../../results/R1_transfer_geometry.md): Theorem 9 (binary:
identification, invariance, sharpness), Theorem 10 (general grades:
canonical correlations between skill spaces), Corollary 11 (tree world).
Script `transfer_geometry.py`.

**Unwelcome facts kept.** The central identity is Spearman's correction for
attenuation, so the mathematics is classical. Difficulty cannot be
recovered from approvals under free task conventions. A first estimator for
two raters with different scales was wrong by up to 0.52 and was replaced.

**Self-review (aim balance).** The question was posed by S2's limit
("vindication is not validity") and answered with a positive
characterisation and its exact boundary, not with the non-identifiability
alone. The positive result needs performance mediation and
better-than-chance raters; both are stated, and reputation is outside it.
Identified risk: presenting a classical identity as a contribution; the
result file names the source and claims only the reading and the sharpness
statement. Possible risk: "difficulty is convention-confounded" may read as
"difficulty is not a fact"; it is a fact that needs an anchor outside
approvals, which is the stated handoff to W6 and W7. Self-review only.

**Observed time, cumulative at this checkpoint.** 1362763369497 ns, 22.71 minutes;
floor remaining 217.29 minutes. The simulations ran in seconds under E; no
exclusion needed.

**Next move on resume.** (1) Graded judge weights and their update
dynamics over the fixed-point lattice of R1.2. (2) A stability bound for
general history length and unflagged assignment, from S1. (3) State the M1
assessment inputs for W1: what is established, at which scope, for the
handoff to W6 and W7.

**S3, continued.** [R1.5](../../results/R1_weight_dynamics.md): graded
weights reinforced by weighted vindication converge (Perron-Frobenius on the
vindication matrix); the limit keeps every trait-tracking judge exactly when
the vindication graph is connected, and otherwise concentrates on the most
mutually predictable family. **Alignment:** C5 moved forward at a restricted
scope (convergence of one linear rule of recursive valuation, with the
condition separating pluralism from concentration); C2 gained the graded
version of R1.2's supports. **Unwelcome facts kept:** accurate judges of an
independent domain are driven to zero; a consistent reputation judge takes
all the weight. **Self-review:** the positive statement (no chaos; pluralism
under connectedness) and the limiting one (concentration; predictability is
not validity) come from the same theorem and are given equal prominence;
the update rule is one choice among several and the file says which
conclusions depend on it; mathematics is standard and attributed. Self-review
only.

**Observed time, cumulative after S3.** 1495520152661 ns, 24.93 minutes (D 23.52, L 0.21,
E 1.19). **Floor remaining: 215.07 minutes.** The cycle stays open.

**Next move on resume.** (1) Coupled dynamics of weights and delineation.
(2) From S1: stability bound for general history length; unflagged
assignment. (3) Draft the W1 inputs to milestone M1 and the handoff
statement to W6 and W7: what the environment must supply that judges
cannot (the scale of difficulty; a test of validity beyond predictability).

### S4, 2026-11-10 (Claude, Fable 5.2)

**Author input, November 10** (quoted in full in
[R1.6](../../results/R1_reappearance.md)): J is a prediction that what is
rated will be seen again; tasks divide into types and sub-types; judging
well requires recognising sub-types well enough for ever more granular
predictions; more capable judges have more refined conceptualisations.
"You can continue working on this recurrence."

**Effect on the readings.** S1 to S3 took J to forecast a performer's later
result. The author's J forecasts reappearance of the thing rated. R1.6
adopts the author's reading as the general one and shows the earlier
results are its restriction to "instance labelled, result forecast." This
also bears on the open question from S1 about "first-order judgment": on
the author's reading, reappearance is part of what J means, so judgment
without reappearance is not a weaker J but no J at all.

**Alignment first.** C1 and C2 moved forward in the author's own terms: the
kinds a good judge must have are fixed by the world (Theorem 13), and
refinement tracks capability in two precise senses (Corollary 14;
experience, by simulation). No thesis weakened.

**Done.** Theorem 13, Corollary 14, the ladder of gains, the unification
with Theorem 1 and with the skill-dependent-choice observation of S1, and a
simulation of judges who learn. Script `reappearance.py`.

**Self-review (aim balance).** The author's statement was taken at its
strongest precise reading and proved; the limit that the statement itself
invites (is finer always better?) is answered both ways: never worse for an
ideal judge, worse for a learner with little experience, and idle past the
world's own distinctions. Identified risk: the mathematics is the theory of
sufficient statistics, so the contribution is the identification, not the
theorem; the result says so. Identified risk of over-agreement with the
author: the reading was adopted because it is more general and repairs an
unproved observation from S1, and the file states what it does not cover
(ratings that cause recurrence). Self-review only.

**Observed time, cumulative after S4.** 1607053814328 ns, 26.78 minutes. **Floor
remaining: 213.22 minutes.** The cycle stays open.

**Next move on resume.** (1) Rating as a cause of recurrence: the selection
dynamic that the author's wording points to, as W1's handoff to W7.
(2) An explicit bound for Corollary 14. (3) Coupled dynamics of weights and
delineation; leftover bounds from S1.

### S5, 2026-11-10 (Claude, Fable 5.2)

**Author input, November 10:** the general definition of J is better
"because something has to determine 'success'. That could either be the same
agent, another agent, or something in the environment that requires it."
The author also said the work will next be handed to GPT-6 Astra.

**Alignment first.** C1 gained its missing condition in dynamic form: the
environment's share of what determines reappearance is what turns
vindication into contact with fact. C3 first contact: a factual limit that
is reached under self-revising judgment with any environmental share, and
can be blocked under mere redistribution of influence. C5: a second
convergence statement for recursive valuation. No thesis weakened.

**Done.** [R1.7](../../results/R1_who_determines_reappearance.md), Theorem
15, with simulations matching in every case run; [HANDOFF.md](HANDOFF.md).

**Self-review (aim balance).** The model is deliberately minimal and the
result file says it is a first model. Both directions are in one theorem:
convergence to the environment's ordering under adaptation, and lock-in of
conventions, including one opposed to the environment, under fixed raters.
Identified risk: the favourable case (b) depends on the unit-norm
normalisation, which makes the self-fulfilling term exactly neutral; with
another normalisation it could favour or oppose particular ratings, and
this is not explored. Identified risk: adopting the author's three sources
as the organising frame without testing an alternative taxonomy. Self-review
only.

**Observed time, cumulative after S5.** 1697189080848 ns, 28.29 minutes. **Floor
remaining: 211.71 minutes.** The cycle stays open; see the handoff.

### S6, resumed 2026-11-10 (Codex, GPT-6)

**Authorization and carried balance.** The author requested review of Fable's
work and continuous completion of this cycle's 240-minute floor. The existing
50 observations recompute to **1,697,189,080,848 ns** of research; the remaining
obligation is **12,702,810,919,152 ns** (211.7135153192 minutes). Earlier model
attributions and raw observations are preserved. This is the same cycle.

**Prospective aim.** Advance C1/C2 by checking whether good forecasts of
reappearance select the world's predictive distinctions, and by constructing
a coupled selection of conceptual kinds and judgments. C3/C5 connections are
secondary consequences requiring their own assumptions. The author's general
reading of J in R1.6/R1.7 governs; forecasting a performer's result is one
instance, and removing recurrence is not the definition of a competing J.

**Plan and readings.** First re-derive Theorems 1, 5 and 13 from their declared
models, checking enabling literature as well as counterexamples. Review the
remaining results and numerical evidence at stated scopes. Seek repairs and
stronger useful formulations wherever a proof needs them. Then investigate
jointly selected kinds and forecasts with environmental feedback, comparing
grounded recovery and self-confirming cases under the same model assumptions.
Explicit quantitative recovery and longer-history bounds are useful alternate
directions. No theorem or positive novelty finding is promised in advance.

**Forecast and execution.** About 212–240 additional research minutes, plus
30–60 minutes of excluded preparation, test waits and publication. Use the
existing clock and at most fifteen-minute observation gaps; pause for waits.
Work is in a clean worktree at main `87d21941`, on `codex/p4-r1-c001`, preserving
475 pre-existing unrelated local changes in the original checkout. This setup
and the handoff intake earn no research credit.

**S6 first checkpoint (cycle still open).** Central proof reconstruction and
the targeted repairs are recorded in [review_s6.md](review_s6.md). R1.8 adds
uniform-history and diagnostic merge bounds. R1.9 couples forecasts,
conceptual partitions and self-influenced recurrence, with a persistent
learning condition realizable under a fixed learning budget. The independent
rational checker passed, and population ODE checks retained a slow near-twin
transient as well as the later convergence. No finite-data convergence or
strategic honesty theorem is claimed by that ODE result.

**Continuation within S6.** The author explicitly allowed broader W1 work
after the handoff priorities. The next constructive question is whether
known agent-caused recurrence can be separated from environmental evidence
using finite observations, and at what cost. Compare calibration with
strategic reporting, and successful correction with the failures caused by
unknown or misspecified feedback. Retain the other W1 directions. This is
the same unfinished cycle, not a new authorization or clock.
