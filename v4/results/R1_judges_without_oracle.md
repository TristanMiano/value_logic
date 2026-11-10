# R1.2 Judges vindicated by later judgments: recovery without an outcome evaluator

**Author:** Claude (Fable 5.2). **Date:** November 9, 2026. **Cycle:**
[P4-R1-C001](../notebook/P4-R1-C001/record.md), session 2 (cycle unfinished).
**Theses:** C1, C2. **Builds on:** [R1.1](R1_recurrent_recovery.md).
**Status:** stated results with proofs and exact checks on small worlds,
written and checked by one model. Not independently reviewed.

## What this shows

R1.1 needed an evaluator who sees later outcomes. Here nobody sees outcomes.
The only data are approvals, and a judgment is credited when it is borne out
by later judgments of the same performer's *new* performances.

- **Approvals can be their own outcomes.** If judges' approvals depend on a
  task only through how the performance turns out, and are not at chance,
  then the delineations that best predict later approvals are exactly the
  refinements of the true transfer partition. One better-than-chance judge
  checked against its own later approvals is enough (Theorem 4).
- **Crediting across reappearance filters shared fashion.** Two judges who
  follow the same occasion-level fashion agree perfectly on each performance
  and earn no credit across performances (Proposition 6).
- **The credited judges and the task delineation determine each other**
  (Theorem 5). "Who is vindicated under this delineation" and "what do the
  vindicated judges jointly distinguish" are monotone maps. Their fixed points
  form a lattice. The largest one contains exactly the judges whose approvals
  track some persistent trait of performers; random judges, fashion followers
  and judges applying a pure convention about tasks belong to no fixed point,
  and distinctions drawn only by them belong to no fixed-point delineation.
- **There are self-confirming fixed points, and conditions for escaping
  them.** "Nobody can judge and there is one task" and "only reputation is
  predictable" are both self-consistent. A general factor of skill, or any
  outside delineation that vindicates one more judge, starts a monotone climb
  toward the largest fixed point (Theorem 5(iii)-(iv)).
- **Bounded judges select the true delineation itself** (Theorem 6). A judge
  who uses only a performer's past results on the same task is strictly hurt
  by needless splits, so with enough history the transfer partition is the
  unique optimum, and with little history coarser delineations win: task
  resolution grows with experience.

What this does not show: that vindication certifies tracking of *skill*. It
certifies tracking of persistent traits as the panel sees them, and these
include reputation. Informative judges with a shared task-dependent bias
also carry their bias into the fixed-point delineation.

## 1. Setting

A panel $`J`$ of judges approves performances. For a performer with
persistent traits $`\theta\sim P`$ and an instance $`x`$, the panel's approval
vector on one performance has law $`k_J(\cdot\mid\theta,x)`$ on a finite set;
$`k_S`$ is its marginal for $`S\subseteq J`$ and $`k_j`$ for one judge. No
outcome variable is needed for the definitions. $`\theta`$ collects every
persistent trait of the performer that affects any judge: ability, and also
reputation if judges respond to it.

- **B1.** Instances are i.i.d. from $`q`$, independently of traits.
- **B2.** Given traits and instances, the panel's approval vectors on
  distinct performances are independent.

Signals shared by judges on a single occasion and renewed at each performance
("fashion") are allowed: they are integrated into $`k_J`$ and respect B2.

**What a set of judges distinguishes.** $`\pi(S)`$ is the twin partition of
instances under $`k_S`$: $`x`$ and $`x'`$ are merged when
$`k_S(\cdot\mid\theta,x)=k_S(\cdot\mid\theta,x')`$ for almost every
$`\theta`$. $`\pi(\emptyset)`$ has one cell.

**Who is vindicated.** For a delineation $`c`$, judge $`j`$ is *vindicated
under* $`c`$, written $`j\in\Sigma(c)`$, when its approval of one performance
and the panel's approvals of another performance of the same performer are
dependent given the two cell labels:
$`I(A_{j,1};A_{J,0}\mid c_1,c_0)>0`$. Equivalently, with cell kernels
$`\tilde k_{\cdot,\kappa}=\sum_x q(x\mid\kappa)k_\cdot(\cdot\mid\theta,x)`$,
some covariance over traits is nonzero:

```math
\mathrm{Cov}_\theta\bigl(\tilde k_{j,\kappa}(a\mid\theta),\,
\tilde k_{J,\kappa'}(a_J\mid\theta)\bigr)\ne0
\quad\text{for some cells }\kappa,\kappa'\text{ and approvals }a,a_J .
```

By symmetry of covariance this is the same whether $`j`$'s approval comes
first (its judgment is borne out later) or second (it bears out earlier
judgments). $`\Phi(S)=\Sigma(\pi(S))`$.

## 2. Approvals as their own outcomes

**Theorem 4. Evidence: proved (corollary of Theorem 1); checked exactly.**
Assume B1 and B2 and $`n\ge1`$. Score a delineation by how well a performer's
$`n`$ past labelled panel approvals predict the panel's approvals of a new
performance. The optimal delineations are exactly the refinements of
$`\pi(J)`$.

Suppose moreover that approvals are *performance-mediated*:
$`k_J(a\mid\theta,x)=\sum_y f(y\mid\theta,z(x))\,G(a\mid y)`$ for a hidden
outcome with kernel $`f`$ as in R1.1 and a channel $`G`$ that does not depend
on the instance or the performer. Then $`\pi(J)`$ is coarser than or equal to
the transfer partition $`\bar z`$, with equality exactly when $`G`$ separates
the outcome laws of distinct classes, and in particular when $`G`$ has full
column rank. For a binary outcome and a single binary judge this says: the
judge is not at chance.

*Proof.* Apply Theorem 1 of R1.1 with the panel's approval vector as the
outcome; B1 and B2 are its assumptions A1 and A2. Under mediation, two types
are twins for $`k_J`$ exactly when $`G(f_A(\theta)-f_B(\theta))=0`$ almost
surely. $`\square`$

A judge whose channel is not injective recovers a coarser partition: it
cannot delineate what it cannot see. A panel can see more than its members:
$`\pi(S\cup S')`$ refines the common refinement of $`\pi(S)`$ and
$`\pi(S')`$, and strictly so when the judges' approvals are informative only
jointly (world G in the checks: each of two judges reads one bit of a two-bit
outcome, the types differ only in whether the bits agree).

**Proposition 6 (agreement is not vindication). Evidence: exact example.**
In world A below, two judges who copy an occasion-level fashion signal share
$`\log 2`$ nats of information on each performance and zero across
performances. Two judges who track the outcome with 20% error share 0.066
nats on the same performance and 0.027 across performances. Weighting judges
by agreement on the same performance ranks fashion first; crediting across
reappearance gives it nothing. This is the role of "yes means I expect it to
reappear": a judgment is tested on a performance that did not exist when the
judgment was made.

## 3. The credited judges and the delineation determine each other

Let $`J_{\mathrm{tr}}`$ be the judges whose approvals depend on traits:
$`k_j(\cdot\mid\theta,x)`$ is not almost surely constant in $`\theta`$ for
almost every $`x`$. Let $`J_{\mathrm{gen}}\subseteq J_{\mathrm{tr}}`$ be those
whose instance-averaged kernel $`\sum_x q(x)k_j(\cdot\mid\theta,x)`$ depends
on $`\theta`$: they respond to a trait that shows without any task labels.

**Theorem 5. Evidence: proved; fixed points enumerated in seven worlds.**
Assume B1 and B2.

- **(i) Lattice.** $`\pi`$ and $`\Sigma`$ are monotone (more judges
  distinguish more; finer labels vindicate more), so $`\Phi`$ is monotone and
  its fixed points form a complete lattice. A fixed point $`S`$ with its
  delineation $`\pi(S)`$ is a state in which the credited judges are exactly
  those vindicated under what the credited judges distinguish.
- **(ii) The largest fixed point is $`J_{\mathrm{tr}}`$** with delineation
  $`\pi(J_{\mathrm{tr}})`$, and every fixed point is contained in it. A judge
  whose approvals do not depend on any persistent trait of performers is in
  no fixed point, whatever it distinguishes among tasks.
- **(iii) Bootstrap.** Starting from no credited judges and one task, the
  iteration of $`\Phi`$ increases to the least fixed point, which contains
  $`J_{\mathrm{gen}}`$. If $`J_{\mathrm{gen}}=J_{\mathrm{tr}}`$ the fixed
  point is unique.
- **(iv) Exploration.** For any delineation $`c_0`$, the iteration started
  from $`\Sigma(c_0)`$ increases to the least fixed point containing
  $`\Sigma(c_0)`$. A delineation proposed from outside helps exactly when it
  vindicates a judge the current fixed point does not contain.

*Proof.* (i) Twins for $`k_{S'}`$ are twins for every marginal $`k_S`$,
$`S\subseteq S'`$. For $`\Sigma`$: cell kernels of a coarser delineation are
mixtures of those of a finer one, and covariance is bilinear, so a nonzero
covariance between coarse cells forces one between some pair of fine cells.
Monotone maps on a finite lattice have a lattice of fixed points, with the
extreme ones reached by iteration from the bottom and the top.

(ii) If $`k_j`$ does not depend on $`\theta`$, every cell kernel of $`j`$ is
constant in $`\theta`$ and all covariances vanish, so
$`\Sigma(c)\subseteq J_{\mathrm{tr}}`$ for all $`c`$. Conversely let
$`j\in S\cap J_{\mathrm{tr}}`$. $`\pi(S)`$ refines $`\pi(\{j\})`$, so on each
cell $`\kappa`$ of $`\pi(S)`$ the cell kernel of $`j`$ is its own kernel, and
for some $`\kappa`$ of positive probability and some $`a`$ it has positive
variance in $`\theta`$. Summing the covariances of
$`\tilde k_{j,\kappa}(a)`$ with $`\tilde k_{J,\kappa}(a_J)`$ over the
$`a_J`$ whose $`j`$-th coordinate is $`a`$ gives that variance, so one of
them is nonzero and $`j\in\Phi(S)`$. Hence $`\Phi(J)=J_{\mathrm{tr}}`$ and
$`\Phi(J_{\mathrm{tr}})=J_{\mathrm{tr}}`$.

(iii) Under the one-cell delineation the cell kernel of $`j`$ is its
instance average, and the same variance argument gives
$`\Sigma(\pi(\emptyset))=J_{\mathrm{gen}}`$. (iv) By (ii),
$`\Sigma(c_0)\subseteq J_{\mathrm{tr}}`$ and $`\Phi(S)\supseteq S`$ for every
$`S\subseteq J_{\mathrm{tr}}`$, so the chain increases; by monotonicity its
limit lies below every fixed point containing $`\Sigma(c_0)`$. $`\square`$

**Reading for C2.** J², "judgments vindicated by later judgments," is the
map $`\Sigma`$. T, "what the vindicated judges tell apart," is the map
$`\pi`$. Neither is primary: the stable states are the fixed points of their
composition, and the essay's bootstrap, in which approvals are "not
initially correlated with future approvals" and delineation and judgment
improve together, is the iteration in (iii)-(iv).

**When is the largest fixed point the factual one?** Its delineation
$`\pi(J_{\mathrm{tr}})`$ equals $`\bar z`$ when the trait-tracking judges are
performance-mediated with a separating joint channel (Theorem 4). It is
finer than $`\bar z`$ when a trait-tracking judge also has a task-dependent
bias (world D2). It is unaffected by judges who respond to reputation
without regard to the task (world F), although those judges are credited.

**Proposition 8 (judging is a task in the same sense). Evidence: argued
from Theorem 1; not separately checked.** Take judges as the performers,
judging occasions as the instances, typed by what is being judged, and as
outcome whether the judgment was borne out by later approvals. If occasions
involve independently drawn performers, so that a judge's outcomes on
distinct occasions are independent given the judge's traits and the
occasions, and occasions are met independently of those traits, then A1 and
A2 hold for this triple and Theorems 1 to 3 apply to it verbatim. The
delineation they recover is the partition of *kinds of judging* by how
judging skill transfers: judging two kinds of work is one task exactly when
no judge's reliability differs between them in a trait-dependent way.

So applying judgment to judgment does not open a new level with new rules.
Evaluating judges is an instance of the same typed core as evaluating
performers, and evaluating those evaluations is another instance. This is a
first, modest point of contact with C5: values assigned to values stay
well-typed and are disciplined by the same reappearance test at every level.
It says nothing yet about convergence of value updates or about self-trust.

## 4. Self-confirming fixed points, constructed

| World | Fixed points (credited judges; delineation) | Reached from nothing |
|---|---|---|
| A. Two task types on opposite skills; two outcome trackers, two fashion followers, one random judge | (none; one task) and (the two trackers; the true two tasks) | (none; one task) |
| B. As A with a general factor of skill | (trackers; true tasks) only | the true one |
| C. Domain 1 has a general factor, domain 2 is pure specialisation; two judges per domain | (domain-1 judges; domain 2 undivided) and (all four; all four tasks) | the first |
| D1. Outcome twins plus a third type; trackers and a judge with a pure task convention | (trackers; the true partition) only. The convention's distinction is absent although the full panel's kernel has it | the true one |
| D2. As D1 with a biased but informative judge | (all three; the true partition refined by the bias) | that one |
| F. As A plus a judge who approves by reputation alone | (reputation judge; one task) and (all three; true tasks) | the reputation one |

Three kinds of self-confirming state appear. **Ignorance** (A): with no task
distinctions, even accurate judges look random, as in the example of R1.1,
so nobody is credited and nothing recommends a distinction. **Partial
grounding** (C): the reachable fixed point is correct about one domain and
blind to another. **Reputation** (F): a society that starts with no
distinctions credits exactly the judge who tracks reputation and sees one
task. In A, C and F an outside delineation that weakly matches the missing
distinction leads to the largest fixed point (checked for A, C and F).

## 5. Bounded judges select the transfer partition itself

In R1.1 a Bayes judge loses nothing from needless splits, so optimality
gives only refinements of $`\bar z`$. A bounded judge changes this. Return to
the outcome setting of R1.1 and call a judge **cell-local** when its forecast
uses only the performer's past results in the target's own cell, optimally.
Its value is
$`V^{\mathrm{loc}}_n(c)=-H(Y_0\mid\text{same-cell part of the history},c_0)`$.

**Theorem 6. Evidence: proved; checked exactly on three worlds.** Assume A1
and A2, a finite type set, and that every twin class has an outcome law that
depends on skill. Among delineations that are functions of the type:

- **(a)** every strict refinement $`c`$ of $`\bar z`$ has
  $`V^{\mathrm{loc}}_n(c)<V^{\mathrm{loc}}_n(\bar z)`$ for all $`n\ge1`$;
- **(b)** every $`c`$ that does not refine $`\bar z`$ has
  $`\lim_n V^{\mathrm{loc}}_n(c)<\lim_n V^{\mathrm{loc}}_n(\bar z)`$;
- **(c)** hence for all sufficiently large $`n`$ the transfer partition is
  the unique optimal delineation.

*Proof.* (a) Splitting a class replaces the same-class history by a strict
sub-history with positive probability. A sub-history cannot help. It
strictly hurts on the event, of positive probability, that the sub-history
is empty while the class history is not: a single same-class result changes
the Bayes forecast with positive probability when the class kernel has
positive variance in $`\theta`$ (the second-moment identity of R1.1). (b) As
$`n\to\infty`$ the same-cell results reveal the cell kernel
$`\tilde f_\kappa(\cdot\mid\theta)`$, so the limit is
$`-\mathbb E\,H(\tilde f_{c_0}(\cdot\mid\theta))`$. If a cell mixes classes
$`A\ne B`$, strict concavity of entropy makes this smaller than the value
for the common refinement, which by (a) and the limit is at most that of
$`\bar z`$. (c) There are finitely many delineations. $`\square`$

**Resolution grows with experience.** With little history a coarser
delineation can win, because pooling near-twins buys data at a small bias.
In a world with a twin pair, a third type whose success rates differ from
theirs by 0.05, and a fourth type on the opposite skill, the unique optimum
merges the near-twin with the twins up to about a hundred past results and
is the transfer partition from $`n=128`$ on; with a difference of 0.02 the
change comes between $`n=128`$ and $`192`$, and with 0.15 the transfer
partition is optimal from $`n=1`$. So for bounded judges the optimal
delineation is single-valued, it is $`\bar z`$ once experience suffices, and
before that it is $`\bar z`$ seen at a coarser resolution. No crossover rate
is claimed.

## 6. Checks

[judge_society.py](../notebook/P4-R1-C001/judge_society.py) builds each world's
exact panel kernel, enumerates every subset of judges, and reports all fixed
points, the bootstrap from nothing, the iteration from the top, and the
single-judge and full-panel partitions. In all seven worlds the approval-
prediction optimum at $`n=1`$ equalled the refinements of $`\pi(J)`$
(Theorem 4), the iteration from the top ended at the trait-tracking judges
(Theorem 5(ii)), and the table in section 4 is its output.
[local_judges.py](../notebook/P4-R1-C001/local_judges.py) computes
$`V^{\mathrm{loc}}_n`$ exactly for all 15 partitions of four types and
$`n\le64`$, with larger $`n`$ in
[local_judges_crossover.json](../notebook/P4-R1-C001/local_judges_crossover.json).
These are small designed worlds, not a sample of worlds.

## 7. Limits and named obligations

- **Vindication is not validity.** The largest fixed point credits every
  judge who tracks a persistent trait, reputation included, and its
  delineation carries any task-dependent bias of an informative judge.
  Nothing inside the approval data separates a shared stable bias from a
  fact about performances. One repair is immediate: if judges see only the
  performance and not who performed it, approvals can depend on a performer's
  traits only through the performance, so a judge of reputation alone is a
  random judge and world F has the fixed points of world A. Candidate
  repairs not yet worked out: independent communities whose biases differ, taking
  what all of them distinguish; an anchor in consequences that no judge
  controls, which is where the environment modules W6 and W7 enter.
- **History length one.** Vindication is defined with one past performance.
  Dependence that appears only with longer histories is not captured.
- **Supports, not weights.** The fixed points are sets of credited judges.
  Graded weights and the dynamics of an actual society updating them are
  open.
- **Performance-mediated approvals** are an assumption about judges, not a
  property verified from approvals.
- **Bounded judges.** Theorem 6 treats one kind of bounded judge, who knows
  each cell's law. Judges who must also learn that law, and rates, are open.

## 8. Closest established work

Consulted at the level of abstracts and stated theorems.
[Kong and Schoenebeck](https://arxiv.org/abs/1605.01021) reward agents by
information-monotone dependence between reports, and in
[later work](https://arxiv.org/abs/1802.08887) show that under independence
conditional on the ground truth the Bayes posterior predictors maximize the
mutual-information gain; that is the same-occasion counterpart of Theorem 4
with an explicit independence assumption, where the present result instead
uses reappearance and tolerates same-occasion dependence. Latent-class
models with several raters in the tradition of Dawid and Skene estimate
rater reliabilities and latent classes jointly; Theorem 5 is not an
estimation procedure and its fixed points are structural. The lattice
argument is Knaster and Tarski's. What is added is the pair of maps, the
identification of the largest fixed point, the constructed self-confirming
states with their escape conditions, and the reading as C2.
