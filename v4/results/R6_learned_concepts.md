# R6.16: payoff-guided learning can select a shared factual representation

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

Agents with different fixed goals can learn which distinctions to retain
using outcomes revealed by their own actions. The mechanism evaluates a
representation by the decisions its forecasts support, then revises that
representation using subsequent payoff. With overlapping demands and
manageable representation cost, independently trained agents can retain
the same factual component. This combines the observation contract of
[R6.5](R6_payoff_judgment.md) with the representation choice of
[R6.1/R6.2](R6_observed_shared.md), serving C1/C2 and W6's link to J².
The final selective-training variant in section 6 improves realized use of
the training budget while preserving a consistency guarantee. Earlier
comparisons remain below to show both the acquisition cost and its repair.

## 1. One explicit observation and cost contract

There are finitely many raw contexts $x\in X$ and goals $j\in G$.
Opportunities $(X_t,G_t,Y_t,T_t)$ are iid, with $Y_t\in\{0,1\}$ and a
uniform price $T_t\in[0,1]$ independent of $(X_t,G_t,Y_t)$.
The conditional outcome law and context/goal frequencies are unknown.
Buying earns $Y_t-T_t$ and declining earns zero. A purchased payoff and its
known price reveal $Y_t$; a declined trade reveals no outcome.

A finite candidate class $\mathcal C$ contains partitions of the raw
contexts. A deployed model stores one forecast $q_{C,j}\in[0,1]$ for each
cell and goal, and buys when $T_t\le q_{c(X_t),G_t}$. A partition with
$k(c)$ cells costs $\kappa(k(c)-1)$ per opportunity. This is a declared
representation price, not measured hardware time or a complete coding cost.
The encoder's raw-label mapping, full-context training counts and
candidate-search computation remain explicit infrastructure. The cell price
is for the deployed representation; it does not price all retained training
storage or establish an advantage in physical memory or computation.

For a joint law $P$ on $(X,G,Y)$, the expected net deployment payoff is

$$
F_P(c,q)=\mathbb E_P\left[Yq_{c(X),G}-\frac12q_{c(X),G}^2\right]
-\kappa(k(c)-1).
\tag{1}
$$

The expectation integrates the price of the action actually taken; it is
not an extra externally supplied proper score. The best forecast in a cell
is its conditional outcome mean.

At deterministic exploration times the agent buys every offered trade,
records its decoded outcome, and pays the full $|X|$-cell training price.
From these trials it forms the empirical joint law $\widehat P_N$. It
chooses $(\widehat c,\widehat q)$ maximizing (1) for that empirical law,
using any forecast on an empirically empty cell/goal pair. During the next
exploitation block it freezes both the representation and its forecasts.
Thus unbought outcomes and evaluator-only ground truth never enter learning.

## 2. Consistency and a finite sample bound

**Proposition 1 (practical value from purchased evidence).** Let
$F_*:=\max_{c,q}F_P(c,q)$ and $d=2|X||G|$. After $N$ iid exploration
trials, for $0<\delta<1$,

$$
F_*-F_P(\widehat c,\widehat q)
\le 2\mathrm{TV}(P,\widehat P_N)
\le\sqrt{\frac{2\log((2^d-2)/\delta)}N}
\tag{2}
$$

with probability at least $1-\delta$. The first bound holds deterministically
for every empirical law.

**Proof.** For every fixed $(c,q)$, the unpriced integrand in (1) lies in
$[-1/2,1/2]$. Therefore changing its distribution changes its expectation
by at most total variation; the fixed representation charge cancels.
Compare a true maximizer with the empirical maximizer, inserting the two
empirical expectations. Empirical optimality leaves at most two TV errors.
For the second bound, TV is the maximum over subsets of the finite outcome
alphabet of $\widehat P_N(A)-P(A)$. Each nonempty proper subset has a
one-sided Hoeffding bound $\exp(-2N\epsilon^2)$. A union bound over at most
$2^d-2$ subsets bounds TV by
$\sqrt{\log((2^d-2)/\delta)/(2N)}$. $\square$

No correct forecast is assumed to be already present in a judge bank.
The model learns the cell means. Finiteness and continued purchases supply
the information; the familiar empirical optimization supplies the learner.
The bound is a conservative simultaneous guarantee, not a fitted error bar.

**Corollary 1 (eventual adequate choice for the priced task).** If exploration
supplies infinitely many iid trials, its fraction of all opportunities
tends to zero, and the per-opportunity training cost is bounded, then
the learner's time-average population regret to $F_*$ tends to zero almost
surely. Any fixed positive gap between the optimal and nonoptimal partition
values makes the selected partition eventually belong to the optimal set.

**Proof.** The finite empirical law converges almost surely, so (2)'s first
inequality makes exploitation loss vanish. Exploration's bounded loss has
vanishing average. In the finite partition class, a nonoptimal partition
cannot achieve value within the smallest positive partition gap of $F_*$,
even with its best forecast. Eventual empirical accuracy excludes all such
partitions. $\square$

For block sizes $b_n=2^{n+9}$, use $\lceil b_n^{2/3}\rceil$ exploration
trials and exploit for the remaining block. Both requirements hold,
including during the exploration portion of each block. Combining (2)
with summable block failure probabilities yields a usual
$O(T^{2/3}\sqrt{d+\log\log T+\log(1/\delta)})$ high-probability regret
bound, with constants depending on the bounded training charge. This is a
standard explore-then-commit tradeoff, not a new rate. The almost-sure
statement is about population regret conditional on the learned policies;
bounded fresh payoff noise also has vanishing realized average by the
martingale strong law.

If every optimal partition for each of several agents determines the same
feature $H(X)$, those agents eventually retain that common feature even
though their other goals differ. This conclusion needs the common-feature
property of the priced task. Agreement alone cannot substitute for it.

## 3. A declared two-agent comparison

Eight raw labels conceal the bit triples $(H,A,B)$ through a random
permutation. Each bit has outcome probability 0.2 or 0.8 according to its
value. Agent 1's opportunities concern $H$ or $A$; agent 2's concern $H$ or
$B$. Neither learner receives these semantic bit labels, the permutation,
or the probabilities. Each sees its raw context, its current goal label,
price and realized action payoff. Both can select among all 4140 partitions.

Set $\kappa=0.02$. When the common goal has probability 0.8, exhaustive
population comparison identifies the two-cell $H$ partition as the unique
best partition for each agent. Its net value is 0.141; the correctly fitted
constant representation yields 0.125, and the eight-cell representation
yields 0.03. A model storing both of an agent's relevant bits in four cells
yields 0.11. The full-model planning comparison knows these means in advance;
the observed learner must pay to discover them.

When the common goal probability is 0.4, the unique optimum is the private
bit partition: $A$ for agent 1 and $B$ for agent 2, each with net value 0.132.
The common $H$ partition then gives 0.123. This is useful diversity under
different fixed goals and a real representation charge. Both agents can
forecast the common outcome near 0.5 while discarding its context-dependent
0.2/0.8 distinction; such agreement is calibrated to their coarse information
but does not recover the fuller factual target.

The pre-execution contract specifies 32 independent replicas per environment
and both agents, blocks 512 through 65536, independent payoff observations,
and the full eight-cell price during exploration. Outcomes from declined
exploitation trades are neither decoded nor used. Population regret includes
all training purchases, their representation charge, and all exploitation
losses. Exact hidden-law evaluation is used only for reporting and the
declared oracle comparison.

## 4. Forced-purchase results and the implemented composition

The [program](../notebook/P4-R6-C001/learned_concepts.py) and
[compact output](../notebook/P4-R6-C001/learned_concepts.json) implement the
declared panel. At the final horizon of 130,560 opportunities, each run has
4287 forced-purchase exploration trials; all their costs are included.

| Common-goal probability | Final optimal representation, agent runs | Final deployment net value | Net value averaged over the whole learning run, population evaluation | Fixed constant forecast |
| ---: | --- | ---: | ---: | ---: |
| 0.8 | Shared $H$, 64/64 | 0.140916 | 0.131509 | 0.125000 |
| 0.4 | Own private bit, 64/64 | 0.131898 | 0.122723 | 0.125000 |

The high-overlap case therefore gains about 0.006509 per opportunity over
the constant forecast after the declared learning and representation costs.
This forced-purchase low-overlap case has not repaid those costs over the tested horizon,
even though its final deployed model is better. No CPU-time advantage is
claimed. The corresponding realized net returns were 0.131731 and 0.122642;
their sampling differences from population evaluation remain visible in
the output. Final common-feature mean squared errors were 0.0000894 and
0.0903098, respectively. Both agents' common-goal forecasts agree fairly
closely in the second case because both have discarded the distinction.

All 64 high-overlap runs selected $H$ after 328 accumulated exploration
trials; all low-overlap runs selected their private feature after 1637.
These are observations on the declared finite panel, not uniform sample
complexities. Independent rational enumeration checks all 4140 partitions
in each goal regime and verifies the unique optimum needed by Corollary 1.
The general TV bound is much more conservative than the observed selection
times.

This experiment implements a limited composition: purchased feedback,
forecast estimation, representation evaluation, and repeated deployment.
The first-order judge ranks actions through its forecast; the second-order
evaluation chooses the representation and forecasts that support better
decisions after costs. The goal distribution supplies the external practical
pressure selecting shared or private distinctions. This is a finite typed
instance of the instrumental/J² connection, using ordinary statistics.

The class of context partitions and the payoff interface are supplied.
Open-ended concept generation, strategically altered environments, endogenous
selection of the meta-evaluation rule, and evolutionary terminalization
remain separate directions. The author's later clarification places that
last question naturally in W7. The present result strengthens W6's factual
bridge without treating W7 as already completed.

## 5. Relevance can change while learned facts remain usable

The two agents' terminal reward rules need not change for their preferred
representations to change. A shift in which opportunities occur is enough.
Write the current context/goal distribution as $w(x,j)$ and the conditional
outcome mean as $p_{xj}$. An old observation of $Y$ in context/goal $(x,j)$
continues to inform $p_{xj}$ when that conditional law is unchanged, even
if $w$ changes. Estimate the current weights from recent context/goal
observations, which are visible whether or not a trade is purchased.

**Proposition 2 (separate factual and relevance errors).** Form a plug-in
model from any normalized weights $\widehat w$ and means
$\widehat p_{xj}\in[0,1]$. Let $(\widehat c,\widehat q)$ maximize its
version of (1), with the same representation prices. Its regret under the
current law is at most

$$
F_*-F_{w,p}(\widehat c,\widehat q)
\le2\mathrm{TV}(w,\widehat w)
+2\sum_{x,j}\widehat w(x,j)|p_{xj}-\widehat p_{xj}|.
\tag{3}
$$

**Proof.** For any fixed $(c,q)$, change $w$ to $\widehat w$ while keeping
$p$ fixed. The integrand $p_{xj}q-q^2/2$ lies in $[-1/2,1/2]$, giving a TV
bound. Next change $p$ to $\widehat p$; since $0\le q\le1$, the change is
at most the weighted absolute mean error in (3). Compare the true and
plug-in maximizers as in Proposition 1, incurring this error twice. $\square$

For a finite family with positive ongoing exposure, old and new purchased
outcomes can consistently estimate an invariant conditional law; current
weights can be learned separately. This is a familiar covariate-shift
principle. [Sugiyama, Krauledat and Müller (2007), sections 2--3](https://www.jmlr.org/papers/v8/sugiyama07a.html)
give a strong established comparison based on importance-weighted risk
evaluation. Our factorized plug-in calculation is not their cross-validation
algorithm, and does not inherit its unbiasedness claim. The value-logic
point is the separation of factual retention from changed practical weight.

**A precise switching boundary.** In the two-bit instance, let $\alpha$
be the common-goal probability. For $k=1,2,3,4$ cells, the best net values
at $\kappa=0.02$ are

$$
\frac18,\quad
0.105+0.045\max(\alpha,1-\alpha),\quad
0.13-0.0225\min(\alpha,1-\alpha),\quad0.11.
\tag{4}
$$

More cells have value at most $0.17-0.02(k-1)$ and cannot improve the
optimum. To verify the two-cell bound, standardize the two independent fair
bits to orthonormal mean-zero variables. A binary cell label spans one
mean-zero direction. Bessel's inequality bounds the sum of its squared
correlations with the bits by one, so allocating that direction to the
more frequent goal is optimal. Equality with unequal goal weights forces
the corresponding bit partition. For three cells, identical bit pairs
can be assigned to the same nearest forecast center without increasing
squared loss. Three centers for the four corners must merge a pair; merging
adjacent corners along the less weighted dimension minimizes the loss,
giving the third expression. Four cells recover both bits exactly.

Consequently the common bit is uniquely optimal for $\alpha>1/2$ and the
private bit for $\alpha<1/2$; both tie at equality. If a learner pools old
and new distributions with frequencies 0.8 and 0.4, its idealized pooled
frequency crosses this boundary only after more than three times as many
new observations as old ones. Updating current relevance separately can
avoid this delay while preserving still-valid conditional evidence.

If the outcome law changes too, the second term of (3) can remain large.
Keeping every old observation with equal weight then carries a calculable
bias. Recent evidence or a justified change detector can repair this, at a
variance and data cost. The diagnostic panel below compares both regimes;
it does not assume that an agent already knows which invariant has failed.

The [diagnostic program](../notebook/P4-R6-C001/shift_concepts.py) and
[output](../notebook/P4-R6-C001/shift_concepts.json) use 32 independent
replicas, 2048 old purchased outcomes, and 4096 current input-only
context/goal observations. All methods have access to these current inputs.
The pooled method fits the whole empirical joint law of purchased trials;
the reuse method combines all historical conditional outcome counts with
current input weights; the recent method uses those weights and only the
latest 512 purchased labels. No method receives the changed law as input.

| Current law | New purchases | Pooled joint fit | Reweighted historical conditionals | Reweighted recent conditionals |
| --- | ---: | ---: | ---: | ---: |
| Only relevance changed | 0 | 0.122591 | 0.131516 | 0.127759 |
| Only relevance changed | 512 | 0.122755 | 0.131816 | 0.131053 |
| Only relevance changed | 2048 | 0.122901 | 0.131887 | 0.130130 |
| Private outcome relation reversed too | 0 | 0.122591 | 0.024379 | 0.035787 |
| Private outcome relation reversed too | 512 | 0.122813 | 0.124893 | 0.130600 |
| Private outcome relation reversed too | 2048 | 0.122889 | 0.124943 | 0.131067 |

Entries are mean current deployment net values; the current oracle is 0.132
in both worlds. These figures omit the separately reported data-acquisition
costs and are not an end-to-end savings claim. The full output includes
standard errors, all six purchased-data budgets and representation choices.
When conditionals remain valid, reweighting selects the private distinction
in 31/32 runs before any new outcome is purchased, and 32/32 after 512.
Pooling still selects the old common distinction in all 32 runs after 2048
new outcomes. When the private relation reverses, historical reuse initially
deploys a confidently wrong forecast. After 512 new outcomes it retreats to
a constant representation in all runs; using the recent window instead
recovers the private distinction in 29/32 runs. The latter pays higher
variance in the unchanged world. These are three fixed methods; an adaptive
rule that decides when to discard historical outcomes remains an obligation.

Independent rational evaluation of all 4140 partitions at the three
endpoints $\alpha=0,1/2,1$ verifies (4). Each candidate value and each
claimed envelope segment is affine on the two intervals, so their endpoint
inequalities certify the envelope throughout those intervals. This checks
the switching claim separately from the sampled learner.

## 6. Training can make useful choices while it learns

Buying every training trade is sufficient for identification but spends
resources on predictably bad trades. Replace that rule with buying according
to the preceding block's forecast, starting at 0.5. During the same training
opportunities, retain two separate statistics: context/goal counts from
**all inputs**, and conditional outcome counts from **purchases only**.
For raw pair $(x,j)$ with $n$ purchased outcomes and sum $S$, estimate

$$
\widehat p_{xj}=\mathrm{clip}_{[\eta,1-\eta]}
\frac{S+1}{n+2},\qquad \eta=0.1.
\tag{5}
$$

Use the all-input empirical weights $\widehat w$ with these means to select
the partition and cell forecasts maximizing (1). Conditional means and
their cell averages stay within $[\eta,1-\eta]$, so each training
opportunity purchases an outcome with probability at least $\eta$.
Charge the same eight-cell price on **every training opportunity**, even
when no purchase occurs. Exploitation remains frozen and supplies no data.
Thus the comparison changes the training decisions and estimator, while
keeping the scheduled opportunities, training price and available feedback
fixed. The assumed interval contains this world's true probabilities.

**Proposition 3 (selective-training consistency).** In section 1's iid
environment, suppose every raw context/goal pair has positive probability
and every true conditional mean lies in $[\eta,1-\eta]$. With infinitely
many training opportunities, the input-weight and conditional-mean
estimates converge almost surely to their true values. The selected
partition eventually belongs to the priced optimal set whenever its gap
to the other partitions is positive. A vanishing training fraction and
bounded per-opportunity costs give vanishing time-average population regret.

**Proof.** Training purchase decisions depend on past evidence, the current
input and independent price, before the current outcome is known. For each
raw pair, its retained outcomes therefore form an iid Bernoulli sequence
with its true conditional mean. Positive raw-pair probability and the
$\eta$ purchase floor give infinitely many such outcomes almost surely.
The strong law, vanishing pseudocount contribution and valid clipping give
conditional-mean consistency. All-input frequencies obey the ordinary
strong law. Proposition 2 now makes the plug-in choice's loss vanish.
Finiteness and a positive partition gap give eventual optimal selection;
bounded training loss with vanishing frequency gives the average claim.
$\square$

This proof also gives an explicit finite guarantee. Put $d_0=|X||G|$.
For the first $n\ge1$ retained outcomes of every pair simultaneously,
with probability at least $1-\delta_y$,

$$
|\widehat p_{xj}-p_{xj}|\le r(n):=
\min\left\{1,
\sqrt{\frac{\log(\pi^2d_0n^2/(3\delta_y))}{2n}}
+\frac1{n+2}\right\},\qquad r(0):=1.
\tag{6}
$$

The union bound sums $2\exp(-2n\epsilon_n^2)$ over all pairs and all
$n$; its total is $\delta_y$. The pseudocount shifts the empirical mean
by at most $1/(n+2)$, and valid clipping cannot increase error. This bound
therefore holds at the adaptively obtained purchase counts. At a fixed
training prefix of $M$ opportunities, the input-frequency TV bound is
$a_M=\sqrt{\log((2^{d_0}-2)/\delta_w)/(2M)}$. Proposition 2 gives
regret at most $2a_M+2\sum_{x,j}\widehat w(x,j)r(n_{xj})$ with
probability at least $1-\delta_w-\delta_y$. As before, this conservative
bound is not used as a fitted certificate for the observed selection times.

Using purchased frequencies as if they were all-input frequencies instead
can distort the practical objective. For two equally frequent contexts
with probabilities 0.2 and 0.8, purchase rates 0.2 and 0.8 make the purchased
input frequencies 0.2 and 0.8. Their pooled outcome mean is 0.68, whereas
the correct forecast for a context-blind future decision is 0.5. Under
uniform prices, deploying 0.68 instead of 0.5 loses $0.18^2/2=0.0162$
per opportunity. Raw conditional means remain valid; the weights need repair.

The [selective-training program](../notebook/P4-R6-C001/selective_concepts.py)
and [output](../notebook/P4-R6-C001/selective_concepts.json) implement this
comparison on the original paired random streams, 32 replicas and two
agents per replica. Every run has 130,560 total opportunities and 4287
training opportunities. The selective method purchases about half of those
training outcomes; the full training price is still charged on all 4287.

| Common-goal probability | Forced purchases: whole-run net value | Selective purchases, correct input weights | Selective purchases, purchased-input weights | Correct-weight final optimal representations |
| ---: | ---: | ---: | ---: | --- |
| 0.8 | 0.131509 | **0.136466** | 0.136335 | Shared $H$, 64/64 |
| 0.4 | 0.122723 | **0.127174** | 0.124871 | Private bit, 64/64 |

These are population-evaluated returns including all declared training and
representation charges. The correct-weight learner now exceeds the fixed
0.125 constant forecast in both environments: by 0.011466 and 0.002174 per
opportunity. Its paired gains over forced purchases are 0.004957 and
0.004451; their standard errors across the 32 paired replica means are
0.0000326 and 0.0000899. Realized whole-run returns are 0.136675 and
0.127101. Mean purchased training counts are 2143.625 and 2145.625.

Final deployment values, 0.140807 and 0.131779, are slightly below the
forced-purchase learner's final values because fewer outcomes were bought.
The gain is in the whole learning episode: useful choices during training
more than repay this finite estimation cost. With purchased-input weights,
the low-overlap panel selects its correct private partition in only 54/64
runs and has whole-run value just below the constant baseline. This is a
finite comparison, not a claim of permanent failure of that learner.

Both improved mechanisms are ordinary statistics applied to the declared
feedback. The contribution is the implemented judgment-to-representation
connection and the exposed costs and coverage conditions. The learner still
uses a supplied finite vocabulary, a valid probability range and scheduled
training access. Choosing its own training schedule, generating new concepts
and acquiring the external evaluator remain distinct research directions.

## 7. Relation to decision-directed representation learning

[Poupart and Boutilier (2002)](https://papers.nips.cc/paper_files/paper/2002/file/14ea0d5b0cf49525d1866cb1e95ada5d-Paper.pdf)
already study compression according to decision quality, including sufficient
conditions for preserving reward predictions through compressed dynamics.
[Li, Walsh and Littman (2006)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/camera-ready-9.pdf)
distinguish preserving models, values and optimal actions, and show why the
choice matters for learning. [Grimm et al. (2020)](https://proceedings.neurips.cc/paper/2020/file/3bb585ea00014b0e3ebe4c6dd165a358-Paper.pdf)
formalize model equivalence relative to intended policies and continuation
functions. These are substantial predecessors of task-directed representation;
R6.16 does not originate that principle.

The specific synthesis here makes overlapping private purposes, purchased
feedback, representation prices and common factual content explicit in one
checked construction. Its distinguishing conclusion is the conditional
shared/private recovery statement, rather than a claim that preserving
decision quality always preserves the whole world. The supplied vocabulary
and the declared cost interface remain part of that conclusion. Sequential
abstractions and model equivalences from those papers are stronger in other
directions; their learning guarantees are not imported into this iid example.

A [direct comparison with newer judgment-to-model results](../notebook/P4-R6-C001/comparison.md)
further locates this synthesis. In particular, probability recovery through
decisions and convergence of minimal representations already have close
primary predecessors. The paid shared/private construction is the claim
assessed here; the general principle is not claimed as new.


## 8. Finite agreement near the shared/private boundary

The same selective learner was evaluated at common-goal frequencies
0.45, 0.49, 0.50, 0.51 and 0.55, with 32 new replicas and two agents.
The original checkpoint has 130,560 opportunities and 4287 training inputs;
an extended continuation has 2,096,640 opportunities and 27,788 training
inputs. This is one continuous learning run per agent, not independent
samples at its two checkpoints. Costs and the 4140-partition vocabulary
are unchanged. The [contract](../notebook/P4-R6-C001/explore.md),
[program](../notebook/P4-R6-C001/boundary_concepts.py) and
[output](../notebook/P4-R6-C001/boundary_concepts.json) record the panel.

| Common-goal frequency | Best representation | Correct at original checkpoint | Correct at extended checkpoint | Extended mean deployment regret | Extended whole-run net value |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.45 | Private | 61/64 | 64/64 | 0.000029 | 0.128040 |
| 0.49 | Private | 42/64 | 46/64 | 0.000287 | 0.125980 |
| 0.50 | Either | 64/64 | 64/64 | 0.000032 | 0.125822 |
| 0.51 | Common | 41/64 | 52/64 | 0.000197 | 0.126052 |
| 0.55 | Common | 61/64 | 64/64 | 0.000031 | 0.128047 |

At 0.51, both agents retain the common fact in 14/32 original pairs and
20/32 extended pairs. At 0.49, both retain their own private facts in
12/32 and 17/32 pairs; those are different facts, not common agreement.
At the exact tie, 17/32 pairs choose a common/private combination at each
checkpoint. Both choices are optimal, although their estimated forecasts
still have small errors. No unique-representation convergence follows
at a tie.

The exact common/private objective gap is

$$
\Delta(\alpha)=0.045|2\alpha-1|.
$$

On the displayed interval away from 0.50, this is also the gap to the
best alternative partition. It is only 0.0009 at 0.49 or 0.51. An
elementary selection guarantee makes
the role of this gap explicit: if every candidate's optimized value is
estimated to error at most $e$, and its unique optimum has gap
$\Delta>2e$, empirical maximization selects that optimum. This follows by
subtracting the two possible estimation errors from the true gap. Without
a positive gap, the same argument gives near-optimal value rather than
one particular representation. Proposition 3 gives eventual unique-optimum
selection in this finite class, not a uniform finite time near indifference.

For any selected partition $c$ and cell/goal forecast $q$, there is also
an exact decomposition. Write $q^c=\mathbb E[Y\mid c(X),G]$ under the true
opportunity law. Expanding the square in the decision objective gives

$$
F^*-F(c,q)=\bigl[F^*-F(c,q^c)\bigr]
+\frac12\mathbb E\bigl[(q(c(X),G)-q^c(c(X),G))^2\bigr].
$$

Thus a different representation and an inaccurate forecast are separate
sources of regret. At the extended 0.49 checkpoint, the 18 agents choosing
the common representation contribute $18(0.0009)/64=0.000253125$ to mean
regret; the remaining 0.000034146 comes from forecast estimation. At 0.51,
the corresponding terms are 0.000168750 and 0.000028622. Small practical
loss can therefore coexist with visibly different retained facts.

All five extended whole-run means exceed the known constant forecast's
0.125, including training costs. At the original checkpoint they are all
below it. This is a further cost boundary: weak pressure near indifference
can take longer to repay evidence acquisition. The panel supports a finite
construction and its limits, not universal agreement or a prevalence claim
about real agents.


## 9. Reuse can make the common fact worth keeping under every positive overlap

The implemented panels charge representation use on every opportunity.
A persistent representation with a one-time setup cost gives a different,
constructive convergence condition. Keep the same known outcome law and
positive price $\kappa>0$ per extra cell, but pay that price once and use the code for
$T$ iid opportunities. Let $m=\min(\alpha,1-\alpha)$.

The maximum **gross value per use**, before representation cost, among
codes with $k$ cells is

$$
G_1=0.125,\qquad
G_2=0.125+0.045\max(\alpha,1-\alpha),\qquad
G_3=0.17-0.0225m,\qquad
G_k=0.17\quad(4\le k\le8).
$$

**Proof of the envelope.** Each raw context has one of four payoff profiles,
indexed by $(H,A)$ for the first agent (or $(H,B)$ for the second).
Splitting identical profiles among cells cannot improve the maximum:
the optimized cell score is a sum of convex perspectives
$(\sum_x w_xp_{xg})^2/(2\sum_x w_x)$; maximizing over fractional
assignments of a profile to cells has a deterministic extreme-point
maximizer. Empty cells may be discarded. It is therefore enough to
partition the four profiles. One cell forecasts 0.5. Two cells optimally
separate the more frequent goal's bit: a diagonal split has gross value
0.125, and a one-versus-three split has 0.14, both no better. With three
cells, merge one pair differing only on the less frequent bit; the induced
loss is $0.0225m$. Merging on the other bit or both bits loses at least
as much. Four cells distinguish both bits and attain 0.17. Extra cells
cannot improve the true conditional forecasts. $\square$

Compare $TG_k-\kappa(k-1)$. If both goals recur, $m>0$, a four-cell code
is uniquely optimal in factual content whenever

$$
T>\frac{\kappa}{0.0225m}.
$$

It retains both the common and private bit, so **both agents retain the
common fact even when their private purposes occur more often**. To prove
the threshold, subtract the two- and three-cell objectives from the
four-cell objective: the differences are $0.045mT-2\kappa$ and
$0.0225mT-\kappa$. The same condition also beats one cell, since $m\le1/2$.
Extra cells cost more without improving gross value. At equality, the
corresponding two-, three- and four-cell maxima tie.

For setup price 0.02, five uses suffice at common-goal frequency 0.8,
three at 0.4, and two at 0.5. These are **known-law use counts**, not claims
that those few observations learn the law. The
[exact checker](../notebook/P4-R6-C001/reuse_concepts.py) and
[output](../notebook/P4-R6-C001/reuse_concepts.json) verify 248,400 partition
comparisons over six goal frequencies and ten integer reuse counts.

This is a mathematical comparison under a different cost contract, not a
second interpretation of the executed constant-price learner. A recurring
operation cost does not vanish through reuse; a nonrecurring goal with
$m=0$ supplies no pressure to preserve its missing distinction. Learning
the law and maintaining a reusable encoder still have their own costs.
The positive lesson is that durability and repeated use can expand which
factual distinctions become common instrumental priorities. It connects
the representation example with R6.3's reusable observation without claiming
that their learning and provision mechanisms have already been combined.
