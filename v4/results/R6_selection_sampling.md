# R6.13 supplement: learning the survival criterion from finite trials

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

The exact-selection mechanism in [R6.13](R6_selection_learning.md) can be
implemented with finite survival trials per update. A sufficient schedule
increases both the trial horizon and the number of trials, so errors become
summable. The construction preserves the distinction between changing an
action and controlling its lucky consequences. It supplies an existence
bridge for learned priorities; its conservative data requirement is not a
practical efficiency claim.

## 1. Robustness of the exact convergence argument

Use R6.13's finite states and actions, with $n$ states, $A$ actions and
substochastic kernels $K_a$. Suppose every entry is at least a known
$m\in(0,1/n)$. Start with a full-support policy. At update $t$, normalize
the right Perron vector $h_t$ of $K_{\pi_t}$ by $\sum_i h_t(i)=1$ and
write $w_t(i,a)=(K_a h_t)_i$. These quantities define the target for the
proof; the learner need not know them.

**Proposition 1 (summable relative errors).** Suppose positive estimates
$\widehat w_t$ satisfy, for some common scale $c_t>0$,

$$
\left|\frac{\widehat w_t(i,a)}{c_t w_t(i,a)}-1\right|
\le\epsilon_t<\frac12,\qquad\sum_t\epsilon_t<\infty.
\tag{1}
$$

Update

$$
\pi_{t+1}(a\mid i)=
\frac{\pi_t(a\mid i)\widehat w_t(i,a)}
{\sum_b\pi_t(b\mid i)\widehat w_t(i,b)}.
\tag{2}
$$

Then $\rho(K_{\pi_t})\to\lambda_*$, $h_t\to h_*$, and all policy
cluster points are optimal, as in R6.13's Theorem 3. Individual growth
factors need not increase at every noisy step.

**Proof.** Let $\pi_t^+$ be the exact update at the current policy. Writing
$\widehat w=c_t w(1+e)$ shows that
$\pi_{t+1}/\pi_t^+=(1+e)/(1+\bar e)$ within each row, where
$|e|,|\bar e|\le\epsilon_t$. Thus the row $\ell^1$ difference is at
most $2\epsilon_t/(1-\epsilon_t)\le4\epsilon_t$.
Every sum-one right or left Perron vector of this positive policy family
has each coordinate at least $m$, and $\lambda h_i\ge m$.
For two policy kernels $L,L'$ and right/left Perron vectors $h,z'$,

$$
\rho(L')-\rho(L)=\frac{z'^{\top}(L'-L)h}{z'^{\top}h}.
\tag{3}
$$

The denominator is at least $m$, so the perturbation above changes the
growth factor by at most $4\epsilon_t/m$. The exact variance improvement
therefore gives

$$
\lambda_{t+1}-\lambda_t
\ge m\sum_i\mathrm{Var}_{a\sim\pi_t(\cdot\mid i)}w_t(i,a)
-\frac{4\epsilon_t}{m}.
\tag{4}
$$

The total possible downward movement is summable; boundedness by one
makes $\lambda_t$ converge. Summing (4) makes the action variances
summable. The exact row step is at most its action-value standard deviation
divided by $m$; adding $4\epsilon_t$ still gives vanishing row steps.
The compactness, finite-cluster-vector and uniqueness arguments of
Theorem 3 apply unchanged. Finally the actual multiplicative action factor
has the same limit as the exact one because $\epsilon_t\to0$.
An eventually greater-than-one factor for a positive action remains
impossible, excluding every omitted improving action. $\square$

## 2. A finite sampling schedule supplies the estimates

Freeze the current policy during an update. For each state and first
action, run independent reset trials: force that first action, then follow
the current policy, retaining a binary flag for survival through $H$ steps.
Its success probability is

$$
s_H(i,a)=(K_aK_\pi^{H-1}\mathbf1)_i.
\tag{5}
$$

Only these flags and the controlled state/action labels reach the learner.
No physical transition outcome is replaced with a conditioned one.

**Lemma 2 (uniform finite-horizon approximation).** Put
$\beta=1-nm^2\in(0,1)$. For every current policy there is a scale
$c_H>0$ with

$$
\max_{i,a}\left|\frac{s_H(i,a)}{c_H(K_a h)_i}-1\right|
\le\frac{\beta^{H-1}}m.
\tag{6}
$$

**Proof.** The Doob matrix $Q_{ij}=K_\pi(i,j)h_j/(\lambda h_i)$
is stochastic, with every entry at least $m^2$. Any two rows share
mass at least $nm^2$, so $Q$ contracts the oscillation of a vector by
at most $\beta$. Let $\nu$ be its invariant law and
$a=\sum_j\nu_j/h_j$. The vector $1/h$ lies in $[1,1/m]^n$;
therefore $|Q^{H-1}(1/h)-a\mathbf1|\le\beta^{H-1}/m$
coordinatewise and $a\ge1$. Conjugating back gives
$K_\pi^{H-1}\mathbf1=\lambda^{H-1}a h$ with relative coordinate
error at most $\beta^{H-1}/m$. Nonnegative action rows preserve that
relative bound. Take $c_H=\lambda^{H-1}a$. $\square$

Choose $H_t$ so that $\beta^{H_t-1}/m\le\epsilon_t/4$.
Every trial has success probability at least $p_t=(nm)^{H_t}$.
For each state/action pair take

$$
N_t\ge\frac{8}{\epsilon_t^2p_t^2}
\log\frac{2nA}{\delta_t}
\tag{7}
$$

independent trials and use their empirical success fraction, clipped below
at $p_t/2$ to keep all action probabilities positive. Hoeffding's inequality
and a union bound give simultaneous absolute error at most
$\epsilon_t p_t/4$ with conditional probability at least $1-\delta_t$.
On that event clipping is inactive, and the relative sampling error is at
most $\epsilon_t/4$. Combining it with (6) gives (1).

For example, take $\epsilon_t=1/[4(t+1)^2]$ and
$\delta_t=6\delta/[\pi^2(t+1)^2]$, for $t\ge0$. With probability
at least $1-\delta$, all updates meet Proposition 1. Moreover the failure
probabilities are summable, so almost surely only finitely many updates
fail their error bounds. Clipping keeps the policy in full support through
those failures; restarting Proposition 1 after the last failure proves
almost-sure convergence as well.

Each update is finite, with $nAN_t$ attempted episodes and at most
$nAN_tH_t$ physical transitions. The schedule has $H_t=O(\log(t+1))$
and a polynomial upper bound on $N_t$ for fixed $m,n,A,\delta$; the
exponent and constants can be enormous when $m$ is small. This is a
constructive sufficiency argument, not a proposed efficient sampler.
Known-model greedy control remains the strong planning comparator.
No new stochastic-control convergence priority is claimed.

## 3. Short-horizon and modest-sample diagnostics

The [diagnostic program](../notebook/P4-R6-C001/selection_sampling.py) and
[output](../notebook/P4-R6-C001/selection_sampling.json) use much smaller
fixed budgets than (7): 16 positive two-state/two-action models, 64 copying
rounds and add-one count smoothing. The environment generates a batch's
survival count from its exact binomial law; it does not simulate every
physical transition. The learner receives only that count. The nominal
attempted-episode budget is $256N$, with at most $256NH$ transitions if
those trials were physically executed. No acquisition-cost advantage is
inferred from this accelerated simulation.

| Horizon $H$ | Trials per state/action/round $N$ | Mean final survival factor | Models worse than their initial policy |
| ---: | ---: | ---: | ---: |
| 1 | 64 | 0.772468 | 0/16 |
| 4 | 64 | 0.772691 | 0/16 |
| 4 | 4096 | 0.773613 | 0/16 |
| 12 | 64 | 0.748266 | 1/16 |
| 12 | 512 | 0.758631 | 2/16 |
| 12 | 4096 | 0.773581 | 0/16 |

The mean initial factor is 0.676028; exhaustive planning gives mean optimum
0.773797, and 64 exact Perron updates reach 0.773576. These are averages
over the same declared models, not population prevalence estimates.
At horizon 12 with 64 trials, only about 4.98% of attempted trials survive.
Increasing the horizon is therefore useful only with enough evidence to
estimate its rarer successes. Individual sampled steps can decrease the
factor, as Proposition 1 allows. The complete output preserves all nine
settings, counts and per-model results.

A separate positive-kernel example makes the horizon error explicit:

$$
K_0=\begin{pmatrix}.79&.01\\.1&.1\end{pmatrix},\qquad
K_1=\begin{pmatrix}.01&.94\\.1&.1\end{pmatrix}.
\tag{8}
$$

From equal action probabilities the survival factor is 0.514575. Exact
one-step-success copying favors entering the dangerous second state and,
after 64 rounds, lowers the factor to 0.364882. Exact horizon-12 copying
instead reaches 0.791446, matching the exact Perron update at this precision.
This does not conflict with finite-horizon improvement in R6.13: that
theorem uses the policy appropriate to each remaining time and evaluates
the same finite terminal criterion. Reusing one short-horizon policy
stationarily for long-run survival changes the claim.

Another 100 positive models check 600 finite-horizon relative bounds and
200 policy/factor perturbation inequalities. All passed. The supplement
does not execute the conservative infinite schedule or imply a finite-sample
guarantee for the smaller panel. It closes an existence gap between exact
selection and learned selection, while leaving efficient sampling,
restricted resets and sparse-world extensions as concrete research targets.
