# R1.14 Small coalitions can recover joint judgment structure

**Author:** Codex (GPT-6). **Date:** November 10, 2026 (local date).
**Cycle:** [P4-R1-C001](../notebook/P4-R1-C001/record.md), S6.
**Theses:** C1 and C2. **Evidence:** proofs reconstructed here and a small
exact checker; no independent confirmation or completed novelty review.

## The faithful reading and the information restriction

Judging a group of judges can reveal a repeatable distinction that judging
each member separately misses. Under a bounded-interaction model, a catalogue
of small groups suffices to recover the full panel's task partition. A
repeatably informative anchor can make those groups available from an
initially undifferentiated task space. This is a conditional construction of
joint judgment producing task delineation, with an explicit representation
restriction and an equally explicit boundary.

Use R1.2's finite setting: persistent performer traits $`\theta`$, tasks
$`x`$ sampled independently of traits with positive probabilities, and
approval vectors $`A\in\{-1,1\}^r`$ conditionally independent across
performances given traits and tasks. Write $`p_x^\theta`$ for the full
panel kernel and $`p_{S,x}^\theta`$ for the marginal on coalition
$`S\subseteq\{1,\ldots,r\}`$. An evaluator sees task labels and repeated
approvals, but not traits. Kernel formulas below define population targets;
they do not provide hidden traits to an estimator.

For a fixed finite coalition catalogue $`\mathcal C`$, distinguish two maps:

- A joint map treats all selected coalition outputs as one observation.
  When their union covers the panel, that observation includes the full
  approval vector. Small group sizes alone then impose no information bound.
- The **factorwise map** $`\pi_{\mathcal C}(D)`$, for
  $`D\subseteq\mathcal C`$, is the common refinement of the twin partitions
  of the separate kernels $`p_S`$, $`S\in D`$. It retains each coalition's
  marginal law, without adding cross-coalition joint moments.

The second map is used throughout this result. It can be realized by separate
forecasters and a sum of their proper scores. It is an explicit restriction
on the representation and objective, not a claim that acquired raw vectors
are physically incapable of carrying more information.

Let $`\Sigma_{\mathcal C}(c)`$ be the coalitions whose own approvals on two
performances of the same performer are dependent conditional on the two
$`c`$-labels. Let $`\mathcal C_{\rm tr}`$ consist of coalitions with a
positive-mass set of task kernels varying with $`\theta`$. These are credits
for a vector-valued judgment; credit for a bundle does not certify each member.

## Theorem 29: factorwise recursion and a bounded-interaction bootstrap

**(a) Typed recursion.** The map

```math
\Phi_{\mathcal C}(D)=\Sigma_{\mathcal C}(\pi_{\mathcal C}(D))
```

is monotone on the finite lattice of coalition subsets. Its greatest fixed
point is $`\mathcal C_{\rm tr}`$. Iteration from the empty set reaches the
least fixed point. Iteration from $`\Sigma_{\mathcal C}(c_0)`$ for any
exploratory delineation $`c_0`$ increases to the least fixed point containing
that seed.

For any fixed $`D`$, any history length $`n\ge1`$, and strictly positive
weights on its components, the sum of optimal expected log scores for
predicting each coalition's next approval from its own labelled history is
maximized exactly by refinements of $`\pi_{\mathcal C}(D)`$.

**(b) Small-group recovery.** Suppose every full kernel is strictly positive
and has the common interaction representation

```math
p_x^\theta(a)=\exp\left\{
 \sum_{S\in\mathcal H}\lambda_S(\theta,x)\chi_S(a)
 -\psi(\lambda(\theta,x))\right\},
\qquad \chi_S(a)=\prod_{j\in S}a_j,
\tag{1}
```

where $`\mathcal H`$ is a specified set of nonempty subsets of size at most
$`k`$. Then the common refinement of the $`\mathcal H`$-marginal twin
partitions equals the full-panel twin partition $`\pi(J)`$.

Suppose in addition an anchor coalition $`B`$ of size $`b`$ has a
trait-dependent task-averaged kernel. Set

```math
\mathcal C_B=\{B\cup S:S\in\mathcal H\}.
\tag{2}
```

Every member of this catalogue is vindicated under the one-cell delineation.
Consequently the first credit step selects the whole catalogue and its
factorwise delineation is $`\pi(J)`$. This is the unique fixed point for
this catalogue. Each retained marginal has at most $`2^{b+k}`$ entries,
and there are at most $`|\mathcal H|`$ marginals. This bounds the
representation of a single task/trait kernel; it is not a sample-complexity
or end-to-end inference-time guarantee.

*Proof of (a).* A coalition is vindicated exactly when some cell-averaged
approval probability varies with traits: its covariance with its own later
matching approval is that probability's variance. If all such probabilities
are constant, conditional independence across performances removes all
dependence. Refinement cannot turn all varying coarse cell probabilities
into constant fine ones. Both maps are therefore monotone.

For $`S\in D\cap\mathcal C_{\rm tr}`$, the factorwise delineation preserves
its own kernel, so a varying kernel remains varying in some cell. Thus
$`D\subseteq\Phi_{\mathcal C}(D)`$ whenever
$`D\subseteq\mathcal C_{\rm tr}`$. Every image lies in
$`\mathcal C_{\rm tr}`$, which is itself fixed. Finite monotone iteration
gives the extreme and seeded fixed points as in R1.2. For the scoring claim,
apply R1.1 Theorem 1 to each vector-valued coalition. Every component loses
nonnegative value under a coarsening, with zero loss precisely when its
twins are preserved. Positive weights make zero total loss equivalent to
preserving all components. Overlapping coalitions need not be independent.

*Proof of (b).* If two positive distributions of form (1) have the same
$`\mathcal H`$ marginals, they have the same moments of every $`\chi_S`$.
For their parameters $`\lambda,\lambda'`$, direct subtraction gives

```math
\mathrm{KL}(p_\lambda\Vert p_{\lambda'})
+\mathrm{KL}(p_{\lambda'}\Vert p_\lambda)
=(\lambda-\lambda')\mathbin{\cdot}
  (\mathbb E_{p_\lambda}\chi-\mathbb E_{p_{\lambda'}}\chi)=0.
\tag{3}
```

Hence the distributions agree. Apply this pointwise in traits, discarding
the finite union of null sets. Equality of full kernels also implies
equality of their marginals, establishing both directions of the partition
identity. This is the standard mean-parameter identification property of an
exponential family, used here for a delineation target.

Each anchored group's task-averaged law contains the varying anchor marginal,
so the group is vindicated. The same argument holds under every delineation:
if all cell averages were constant, their mixture would be constant. Thus
$`\Sigma_{\mathcal C_B}(c)=\mathcal C_B`$ for every $`c`$. Its factorwise
partition preserves every $`\mathcal H`$ marginal and is no finer than
the full-panel partition, which proves the bootstrap and uniqueness.
$`\square`$

The anchor makes this a deliberately strong sufficient construction. It
does not give each newly included judge an independent justification. If a
known pure convention is bundled with a good anchor, the convention can
enter the recovered panel partition. To interpret that partition as factual
performance distinctions, use R1.2 Theorem 4's performance-mediated,
task-independent separating channel, or supply a different explicit bridge.
Within that channel model, the anchor construction recovers the outcome
transfer partition, not merely a mutually consistent grouping.

## Proposition 30: an approximate version with decision meaning

Let $`p,q`$ have form (1), with parameter norms at most $`B_0`$ in
$`\ell_1`$. If all retained interaction moments differ by at most
$`\epsilon`$, then

```math
\|p-q\|_{\rm TV}\le
\min\left\{\sqrt{B_0\epsilon/2},\,
\frac{e^{B_0}\sqrt{|\mathcal H|}}{2}\epsilon\right\}=:v(\epsilon).
\tag{4}
```

For the first bound, (3) is at most $`2B_0\epsilon`$, while the two
Pinsker inequalities sum to at least $`4\|p-q\|_{\rm TV}^2`$.
For the second, every distribution on the parameter segment has density at
least $`e^{-2B_0}`$ relative to the uniform cube law. The distinct nonempty
Walsh monomials are orthonormal under that law, so for any coefficient vector
$`u`$,

```math
u^\top\nabla^2\psi\,u
=\min_c\mathbb E_p[(u\cdot\chi-c)^2]
\ge e^{-2B_0}\|u\|_2^2.
```

Integrating along the parameter segment gives
$`\|\lambda-\lambda'\|_2\le e^{2B_0}\|\mathbb E_p\chi-\mathbb E_q\chi\|_2`$.
Equation (3) and the summed Pinsker bound now give the second term of (4).
Known strength control makes this a quantitative statement; exact moment
equality identifies the law without it.

More generally suppose positive true laws $`p,q`$ have moment-matching
approximations $`\bar p,\bar q`$ of form (1), with parameter norms at most
$`B_0`$ and approximation divergences
$`\mathrm{KL}(p\Vert\bar p)\le\delta_p`$ and
$`\mathrm{KL}(q\Vert\bar q)\le\delta_q`$. Then

```math
\|p-q\|_{\rm TV}\le
\sqrt{\delta_p/2}+v(\epsilon)+\sqrt{\delta_q/2}.
\tag{5}
```

This follows by the triangle inequality. A finite maximum-entropy fit on
the specified moments supplies the required matching approximation whenever
it exists; the bound does not assume its approximation error is known from
those same moments. The parity example below has identical retained moments
and a positive approximation error.

For a decision with utility in $`[0,1]`$, using an action optimal for $`q`$
under the true law $`p`$ has regret at most $`2\|p-q\|_{\rm TV}`$ (and at
most one). Add and subtract the two actions' expectations under $`q`$.
The same bound holds after mixing kernels under a *common* trait belief,
with the average of the right side of (5). Different inferred trait beliefs
require their own error bound; marginal recovery does not silently identify
all posteriors or give the same finite-history predictive efficiency.

## A constructive example and the interaction boundary

Take six judges in three independent pairs conditional on three independent
fair persistent traits $`\theta=(\theta_1,\theta_2,\theta_3)`$ and one of four equally likely tasks
$`x=(s,t)\in\{-1,1\}^2`$. Within each pair the first approval is fair and
the second has correlation, respectively,

```math
m_{12}=\theta_1/2,\qquad m_{34}=\theta_2 s/2,
\qquad m_{56}=\theta_3 t/2.
\tag{6}
```

All individual judges have uniform marginals and earn no individual credit.
After averaging over traits, even the full single-performance approval law
is uniform on every task. A collection with one performance per independent
performer therefore cannot distinguish these tasks. Repeated performances
share traits, making transfer across tasks observable. An ordinary method
given those same repeated episodes can use that information too.
The pair catalogue $`\{12,34,56\}`$ starts with only pair 12 credited;
its partition has one cell, so this iteration stays there. Anchoring gives
$`\{12,1234,1256\}`$: all three groups earn credit without initial task
labels, and their factorwise partition identifies all four tasks. Every
kernel is strictly positive and has only pair interactions.

This example has an explicit outcome bridge. Let the performance have three
binary outcomes $`Y_i`$ with the means in (6), independent conditional on
traits and task. For each pair, draw a fresh fair bit $`R_i`$ and report
$`(R_i,R_iY_i)`$. This task-independent observation channel recovers each
outcome as the product of the two approvals, so it separates all outcome
laws. The individual judgments remain uninformative. Independent additional
reporting errors with nonzero reliability attenuate the correlations and
preserve this separation; they can make the required evidence much larger.

For this known three-edge support, the retained marginal tables have
$`4+16+16=36`$ entries, against 64 for a full six-judge law. If the support
is unknown and all singleton/pair interactions are allowed, the anchored
catalogue has 132 entries here: a small-world overhead, retained explicitly.
For 20 judges with a two-judge anchor, the analogous all-singleton/pair
catalogue has 2,596 entries, against 1,048,576 full-law entries. These are
table sizes, not measured computation or acquisition savings.

**Boundary and repair.** For $`r\ge3`$ judges, the positive parity family

```math
p_x^\theta(a)=2^{-r}\left(1+\rho\theta x\prod_{j=1}^r a_j\right),
\qquad 0<\rho<1,\quad x,\theta\in\{-1,1\},
\tag{7}
```

has two distinct full kernels and identical uniform proper marginals. Add an
independent informative two-judge anchor. Every group containing that anchor
and fewer than all $`r`$ parity judges is credited, but its marginal is
independent of the task. Arbitrarily many separate histories of these groups
cannot restore the missing task distinction. Including one group with all
parity judges repairs the representation. Alternatively, a scientifically
supported bounded-interaction model rules this example out; merely declaring
that judges act independently does not.

## Proposition 31: recovery from observed repeated judgments

There is also a direct finite-observation route for the interaction model.
For $`h=|\mathcal H|`$ retained monomials let
$`m_S(\theta,x)=\mathbb E[\chi_S(A)\mid\theta,x]`$. In each of
$`N`$ independent performer episodes for every ordered task pair
$`(x,x')`$, obtain two fresh performances on those tasks. The performer
distribution is the same in every assay. Outcomes within an episode are
conditionally independent given its traits; the traits are unobserved.
Set

```math
\widehat G_S(x,x')=\frac1N\sum_{i=1}^N
       \chi_S(A_{i,0})\chi_S(A_{i,1}),\qquad
D_S(x,x')=\mathbb E_\theta[(m_S(\theta,x)-m_S(\theta,x'))^2].
\tag{8}
```

For $`d`$ task labels and $`0<\alpha<1`$, define

```math
r_N=\sqrt{\frac{2\log(2hd^2/\alpha)}{N}},\qquad
\widehat D_S=\widehat G_S(x,x)+\widehat G_S(x',x')
             -\widehat G_S(x,x')-\widehat G_S(x',x).
\tag{9}
```

With probability at least $`1-\alpha`$, all discrepancies obey
$`|\widehat D_S-D_S|\le4r_N`$ simultaneously. Thus a positive lower
bound certifies a distinction. If it is additionally known that every
non-twin task pair has some $`D_S\ge\Delta>0`$, the rule declaring
non-twins when $`\max_S\widehat D_S>\Delta/2`$ recovers the full twin
partition whenever

```math
N>\frac{128}{\Delta^2}\log(2hd^2/\alpha).
\tag{10}
```

*Proof.* Each summand is in $`[-1,1]`$ and has expectation
$`G_S(x,x')=\mathbb E_\theta[m_S(\theta,x)m_S(\theta,x')]`$.
Hoeffding's inequality and a union bound over $`hd^2`$ entries give
error at most $`r_N`$ for all entries. Expanding the square gives
$`D_S=G_S(x,x)+G_S(x',x')-G_S(x,x')-G_S(x',x)`$, hence (9).
Equation (10) makes $`4r_N<\Delta/2`$. Twin tasks have all discrepancies
zero; every non-twin pair then crosses the stated threshold. Under (1),
equality of all moment profiles is equivalent to equality of the full kernels
by Theorem 29(b). $`\square`$

Without the known gap, this yields certified distinctions and unresolved
pairs, not certificates of exact equality from finite data. The design uses
controlled repeated task assignments; the bound does not silently apply to
trait-selected assignments in R1.10. The input is actual approvals, not
latent skill labels. The estimator is a conventional repeated-measurement
moment method; its role here is to realize the restricted recovery target.

The companion `coalition_observed.py` duplicates each of the four tasks in
(6) under two unrelated labels, then uses the three pair-product features,
$`N=2000`$, $`\alpha=.05`$ and the declared model gap $`\Delta=1`$.
This is 128,000 performer episodes and 1,536,000 binary approval reports.
The population construction admits the gap; it is supplied to the certified
threshold, not estimated as though exact separation were free.
The saved run recovers partition `[0,1,2,3,1,0,3,2]`. Its largest Gram-entry
error is 0.067, below the simultaneous radius 0.0945853; the discrepancy
radius is 0.3783412. All 24 non-twin pairs have positive lower bounds, while
the four alias pairs remain consistent with zero. The exact-equality
conclusion for those pairs additionally uses the declared separation.

## Established work, evidence and remaining work

The exponential-family identification step is standard:
[Wainwright and Jordan (2008), §3.5.2, Proposition 3.2](https://www.cs.columbia.edu/~blei/fogm/2023F/readings/WainwrightJordan2008.pdf).
Their mean-parameter account supplies the enabling mathematics. The separate
log-score objective is a marginal composite likelihood, rather than a new
scoring principle; see
[Varin, Reid and Firth (2011), §2.1](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A21n11.pdf).
An implementation of that objective under another name is identical. A
full-joint forecaster or a correctly specified latent model is a different
competitor and may use the observations more efficiently.

The contribution at this stage is a typed synthesis: a representation-limited
coalition operator, its fixed points, an anchor-based recovery condition,
and an explicit interaction-order obstruction with a repair. The exact
example is a construction, not evidence that arbitrary real panels satisfy
the interaction or mediation assumptions. Finite-sample coalition selection,
robustness to inaccurate interaction support, and strategic or evolutionary
incentives for maintaining the catalogue remain open. C5 self-licensing is
not inferred from the fixed-point theorem.

Reproduction: [coalition_recovery.py](../notebook/P4-R1-C001/coalition_recovery.py)
and its [output](../notebook/P4-R1-C001/coalition_recovery.json) check the finite
kernels, two operator catalogues, all 15 task partitions, three parity
boundaries, representation counts and 90 quantitative inequalities.
[coalition_observed.py](../notebook/P4-R1-C001/coalition_observed.py) and its
[output](../notebook/P4-R1-C001/coalition_observed.json) implement Proposition 31.
These are generated checks, not a second-model review.
