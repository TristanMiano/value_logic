# R6.13: successful-history selection can improve actual action

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

An initially reward-free controller can acquire a useful practical bias by
copying actions from successful histories. The positive condition is that
the retained histories measure the same success criterion as deployment,
with state and remaining time represented correctly. Stochastic action
outcomes do not by themselves prevent improvement. This supplies a causal
bridge from the externally selected patterns in
[R6.12](R6_unrepresented_values.md) to better future action, serving C5 and
C7 and the author's question about goals that were not initially represented.

The finite-horizon update is a special case of established reward-weighted
regression. The contribution is its explicit connection to survival filtering,
the distinction between actions and conditioned outcomes, and the survival
growth statement below. Neither component is claimed as a new general RL
algorithm.

## 1. Actions are controllable; their stochastic consequences are not

Let $S$ and $\mathcal A$ be finite. For each action $a$, $K_a(i,j)$ is the
probability of reaching live state $j$ from $i$; its row sum is at most one,
and the missing probability is absorption into failure. The baseline policy
$\pi(a\mid i)$ induces

$$
K(i,j)=\sum_a\pi(a\mid i)K_a(i,j).
\tag{1}
$$

Assume $K$ is strictly positive. This ensures useful mixing and positive
future success from every state. The controller can change $\pi$, but it
cannot replace the physical kernels $K_a$ with their outcome-conditioned
versions. A terminal retention probability $u(i)\in[0,1]$ is nonzero;
$u=\mathbf 1$ means survival alone. For $n$ remaining transitions, define

$$
h_n=K^n u,\qquad w_n(i,a)=(K_a h_{n-1})_i,
\qquad
\pi_n^+(a\mid i)=\frac{\pi(a\mid i)w_n(i,a)}{h_n(i)}.
\tag{2}
$$

These are the first-action frequencies among baseline trials that pass the
whole retention filter. Bayes' rule proves (2). They can be estimated from
first actions and a binary end-of-trial success flag; the learner need not
compute the displayed expectations. Complete observation of the modeled
state, compatible reset trials, and enough retained data are real assumptions.

## 2. Correctly timed copying improves finite-horizon success

**Theorem 1 (finite-horizon selection improvement).** Execute $\pi_n^+$
when $n$ transitions remain, using the actual kernels $K_a$. Let $V_n^+$
be its probability of passing the terminal filter. Then

$$
V_n^+(i)\ge h_n(i)\quad\text{for every }i,n.
\tag{3}
$$

**Proof.** $V_0^+=h_0=u$. If $V_{n-1}^+\ge h_{n-1}$, nonnegativity gives

$$
\begin{aligned}
V_n^+(i)
&=\sum_a\pi_n^+(a\mid i)(K_aV_{n-1}^+)_i\\
&\ge\frac{\sum_a\pi(a\mid i)w_n(i,a)^2}{h_n(i)}\\
&=h_n(i)+\frac{\mathrm{Var}_{a\sim\pi(\cdot\mid i)}w_n(i,a)}{h_n(i)}
\ge h_n(i).
\end{aligned}
\tag{4}
$$

The denominators are positive under the stated assumptions. Induction
finishes the proof. Strict action-value variance gives a strict improvement
at that time/state; earlier states can inherit the improvement. $\square$

The update can be represented as selecting for a value, but the original
controller need not contain a utility variable. The external retention rule
does supply the asymmetry. This is emergence of a behaviorally expressed
priority from variation and retention, not creation of a direction from a
fully symmetric process.

**Approximate copying.** If a learned policy satisfies
$\max_i\mathrm{TV}(\widehat\pi_n(i),\pi_n^+(i))\le\epsilon_n$,
then

$$
\widehat V_T(i)\ge V_T^+(i)-\sum_{n=1}^T\epsilon_n
\ge h_T(i)-\sum_{n=1}^T\epsilon_n.
\tag{5}
$$

Indeed each continuation value lies in $[0,1]$, so changing one action row
changes its expected continuation value by at most its TV distance.
Substochastic kernels do not amplify a sup-norm error. Backward induction
then adds the errors. This does not promise strict improvement at every
finite sample size; a positive gain must exceed the estimation allowance.

For binary actions and $N_{n,i}>0$ accepted iid reset trials, add-one
smoothed first-action counts have simultaneous errors at most

$$
\epsilon_{n,i}=\min\left\{1,
\sqrt{\frac{\log(2|S|T/\delta)}{2N_{n,i}}}
+\frac{1}{N_{n,i}+2}\right\}
\tag{6}
$$

with probability at least $1-\delta$ over all $i,n$. Conditional on the
accepted count, accepted actions have the distribution in (2); apply
Hoeffding's inequality and a union bound. Smoothing changes a binary
frequency by at most $1/(N+2)$. Use error one if no trial is accepted.
Rare survival makes this guarantee expensive, exactly as the R6.12 experiment
shows. Attempted trials and resets must be counted.

## 3. A stationary survival-growth improvement

Let $Kh=\lambda h$ be the positive Perron eigenpair of (1). Conditional
action frequencies far before a terminal filter converge to

$$
\pi^+(a\mid i)=\frac{\pi(a\mid i)(K_a h)_i}{\lambda h_i}.
\tag{7}
$$

This limit is independent of any fixed nonzero terminal $u\ge0$, by the
same positive-matrix argument as R6.12. Define the **actual** live kernel
after copying as $L(i,j)=\sum_a\pi^+(a\mid i)K_a(i,j)$.

**Theorem 2 (improved long-run survival factor).**

$$
\rho(L)\ge\lambda,
\tag{8}
$$

with strict inequality if the values $(K_a h)_i$ differ across baseline
positive-probability actions at any state. Equality holds if all such
action values tie at every state.

**Proof.** Write $w(i,a)=(K_a h)_i$. Then

$$
(Lh)_i=\lambda h_i+
\frac{\mathrm{Var}_{a\sim\pi(\cdot\mid i)}w(i,a)}{\lambda h_i}.
\tag{9}
$$

Every positive entry of $K$ is contributed by an action with positive $w$,
so $L$ is positive too. Let $z>0$ be its left Perron vector. Multiplying
(9) by $z_i$ and summing gives the exact identity

$$
\rho(L)-\lambda=
\frac{\displaystyle\sum_i z_i
\mathrm{Var}_{a\sim\pi(\cdot\mid i)}w(i,a)/(\lambda h_i)}
{z^\top h}\ge0.
\tag{10}
$$

It is strict when any variance is positive. If all variances vanish,
$Lh=\lambda h$ and positivity identifies the Perron eigenvalue. $\square$

The number $\lambda$ is the exponential survival factor of the baseline:
$\mathbb P_i(\text{survive }T)=\Theta(\lambda^T)$ for this finite positive
model. This is not the mean number of offspring or a guarantee about every
finite horizon. Iterating the exact update gives nondecreasing survival
factors, bounded by one. The following stronger assumptions also give global
convergence; finite-population loss of useful actions needs separate control.

The conditioned **state** transition from R6.12 is
$K(i,j)h_j/(\lambda h_i)$. In a general stochastic action environment it
differs from $L$. Confusing the two would give the learner control over luck.
Theorems 1--2 avoid that error by changing only action probabilities and then
evaluating the unchanged physical outcomes.

## 4. Repeated selection reaches the best survival factor

**Theorem 3 (global exact-selection convergence).** Suppose every
deterministic policy induces an irreducible live kernel with positive Perron
root, and every initial action probability is positive. Strict positivity
of every action kernel is sufficient, but sparse kernels can also satisfy
the stated condition. Repeat (7), recomputing the positive right Perron vector $h_t$
of $K_{\pi_t}$ at each step and normalizing $\sum_i h_t(i)=1$. Then

$$
\lambda_t\uparrow\lambda_*:=\max_\pi\rho(K_\pi),\qquad
h_t\longrightarrow h_*,\qquad
\max_a(K_a h_*)_i=\lambda_*h_*(i).
\tag{11}
$$

Every cluster point of the policy sequence is optimal. In particular,
its distance to the compact optimal-policy set tends to zero. If a single
action is optimal at each state, the policy converges to that deterministic
policy. Ties permit several equally successful behaviors; the theorem does
not assert convergence of the action probabilities in that case.

**Proof.** Every mixed-policy kernel contains the edges of some deterministic
policy in its support and is therefore irreducible. The policy space is
compact, and the normalized positive left and right Perron vectors and
positive Perron root vary continuously over it. Consequently there are
constants $a_0,b_0>0$ such that, for every policy and state,
$\lambda h_i\ge a_0$ and the sum-one left Perron vector satisfies
$z_i\ge b_0$. Each action has a nonzero live row, so its update factor is
positive and all finite-iteration action probabilities remain positive.
In the strictly positive case, $m=\min_{a,i,j}K_a(i,j)$ can be used for both
constants: the normalized eigenvector equations give these lower bounds
directly. Always $\lambda\le1$.

Let $\sigma_t^2(i)=\mathrm{Var}_{\pi_t(\cdot\mid i)}
(K_a h_t)_i$. Equation (10), together with
$z_{t+1}^{\top}h_t\le1$ and $\lambda_t h_t(i)\le1$, yields

$$
\lambda_{t+1}-\lambda_t\ge b_0\sum_i\sigma_t^2(i).
\tag{12}
$$

Equation (10)'s proof also holds for irreducible kernels: the needed left
and right Perron vectors are positive and copying preserves the kernel's
graph. The left side of (12) is summable. Thus every variance tends to zero. Moreover,
Cauchy--Schwarz and the update give

$$
\sum_a|\pi_{t+1}(a\mid i)-\pi_t(a\mid i)|
\le\frac{\sigma_t(i)}{\lambda_t h_t(i)}
\le\frac{\sigma_t(i)}{a_0}\longrightarrow0.
\tag{13}
$$

Let $\bar\pi$ be any policy cluster point. By continuity and (13), it is a
fixed point of (7). Each action in its support therefore has
$(K_a\bar h)_i=\bar\lambda\bar h_i$. Choose one such action per state.
The resulting deterministic policy has the same Perron eigenvector $\bar h$.
There are finitely many deterministic policies, so the cluster points of
$h_t$ belong to a finite set. Continuity and (13) also imply
$\|h_{t+1}-h_t\|\to0$. A sequence in a compact set with vanishing increments
and only finitely many cluster points has one cluster point: otherwise,
transitions between disjoint neighborhoods of two cluster points would
produce another cluster point outside those neighborhoods. Hence
$h_t\to h_\infty$; monotonicity already gives
$\lambda_t\to\lambda_\infty$.

For each state and action the multiplicative update factor consequently
converges to

$$
r(i,a)=\frac{(K_a h_\infty)_i}{\lambda_\infty h_\infty(i)}.
\tag{14}
$$

If this were greater than one, the full-support initial condition would
make the corresponding positive action probability eventually grow by a
fixed factor greater than one at every step, contradicting its upper bound
of one. Thus $K_a h_\infty\le\lambda_\infty h_\infty$ for every action.
For any policy $\pi$, multiplication by its positive left Perron vector
then gives $\rho(K_\pi)\le\lambda_\infty$. A cluster policy attains this
upper bound, proving global optimality and the max equation in (11).

For completeness, the normalized positive solution of that max equation
is unique. If two such solutions $h,g$ of the same eigenvalue were not
proportional, let $r=\max_i h_i/g_i$ and choose a maximizing state $i$.
Choose at each state an action maximizing the backup of $h$, giving an
irreducible deterministic kernel $D$. Then $Dh=\lambda_*h$ and
$Dg\le\lambda_*g$. For $d=rg-h\ge0$, we have $Dd\le\lambda_*d$.
At a state where $d_i=0$, every state reached by a positive edge of $D$
must also have zero $d$. Irreducibility propagates this to every state,
contradicting nonproportionality. Therefore $h_\infty=h_*$.
An action with $(K_a h_*)_i<\lambda_*h_*(i)$ has a limiting update factor
strictly below one and its probability eventually decays geometrically.
This proves the remaining policy statements. $\square$

The all-policy irreducibility assumption keeps every live state reachable
under every deterministic choice. It allows sparse transitions, and is
stronger than irreducibility of only the initial mixed kernel. Some useful
policies can destroy reachability; that larger class remains open here.
For the interpretation of (7) as a limit of long retained histories,
add aperiodicity of the initial full-support mixed kernel. All finite
updates preserve its graph, so this condition persists. The algebraic
convergence theorem itself does not need aperiodicity.
Full support is equally substantive: exact copying cannot invent an action
that has probability zero. Restricting the theorem to the initial support
recovers optimality within that support, while mutation or exploration can
make omitted actions available. The proof supplies no uniform finite-time
rate. The [sampling supplement](R6_selection_sampling.md) extends convergence
to summable relative evaluation errors and gives a conservative finite-trial
schedule for strictly positive kernels. Its smaller sampled panel is a
separate diagnostic, not execution of that guaranteed schedule.

## 5. Executable evidence and a necessary causal distinction

The [checker](../notebook/P4-R6-C001/selection_learning.py) verifies 480
rational finite-horizon inequalities across 60 two-state/two-action models,
including 5120 independently enumerated action/state histories. It also
checks the stationary growth identity on 300 positive stochastic models.
All passed; growth improvements in that declared panel ranged from
0.00003911 to 0.088715. These are finite model checks, not a claim about
real-world frequency or efficiency.

A one-action version of R6.12 supplies an informative boundary. Its
survival-conditioned live transition law differs from the actual live
transition law by row-TV distance as large as 0.15, while its action policy
cannot change at all. Apparent directedness among selected histories does
not by itself create a controllable capability. Adding actions that affect
the success chances, and transmitting their selected frequencies, supplies
the missing mechanism in Theorems 1--2.

On R6.12's controllable two-state example, 40 exact-model repetitions of
(7) increase the survival factor from 0.8 to 0.9999999697; the first update
gives 0.875. This repeated experiment uses eigenvectors from the known model,
unlike the one-step observed cloning panel. Its deterministic action outcomes
fall outside Theorem 3's all-policy irreducibility assumption; the numerical
example alone does not extend that theorem. Reusing the
observed panel for (6), all 384 action-row checks lie within the simultaneous
95% bound; the largest radius is 0.061706. The first checker execution reached
JSON serialization and failed on a NumPy integer count; converting that
count to a Python integer repaired it. No mathematical assertion failed.

The additional Theorem 3 panel uses 80 positive models, 2000 exact updates
per model, and exhaustive deterministic-policy comparison. All factors
increased monotonically to numerical tolerance. The median final gap was
zero to reported floating precision, while the worst gap remained
0.000276623. The maximizing-row planning comparator attained the enumerated
optimum in at most three updates in this panel. Thus copying is a successful
selection mechanism, but the evidence favors model-based planning when that
model and computation are available. With 0.02 transition tremble added to
R6.12's actions, the positive model reached its exact optimal factor 0.994;
the normalized value vector is $(1,0.7)/1.7$.

The sparse extension was checked on another 40 declared models with a
positive common-cycle edge in every action row. This verifies every policy's
irreducibility without making the matrices dense. All 2000-step trajectories
were monotone; the worst remaining factor gap was 0.0000299343. Greedy
planning attained the enumerated optimum in at most two updates. This
supports the proof extension while preserving the same adverse speed
comparison for exact-model copying.

**Persistence and revisability are different virtues.** In a one-state
model with action survival factors 0.7 and 0.9, selected action odds multiply
by $9/7$ per round. Starting the better action at probability $10^{-12}$
requires 110 rounds to make it a majority; starting at zero never discovers
it. Starting at equal odds and favoring one action for 1000 rounds requires
1001 reversed rounds before the opposite action becomes a strict majority.
Adding 0.01 symmetric revision after each selection step leaves the formerly
favored action at about 0.956588 before reversal, and changes the majority
after 11 reversed rounds. These exact/numerical model calculations connect
the acquired priority to [R6.4](R6_plastic_priorities.md): apparent
terminal-like persistence can be accumulated evidence and low revisability,
while environmental change can favor maintaining a capacity to revise.

## 6. Strong existing alternatives and the exact scientific delta

[Štrupl et al. (2022), theorems 3.1 and 4.1](https://arxiv.org/html/2107.09088v3)
give the reward-weighted update $\pi^+\propto\pi Q^\pi$ and prove monotonic
improvement using the same variance mechanism. They further prove global
convergence under their exact, unapproximated discounted-control assumptions,
with finite-case convergence rates. Those stronger results are not imported
without checking their hypotheses for the present survival-growth objective.
Theorem 1 is a finite-horizon version of that established mechanism.
Theorems 2--3 supply direct Perron-eigenvalue arguments for the survival
interpretation; a literature-priority claim for them is not made.

[Cvetković and Protasov (2020/2022)](https://doi.org/10.1007/s10107-020-01585-z)
optimize the Perron eigenvalue over independently selectable matrix rows.
That is precisely the model-based objective here when each row set is the
convex hull of its action rows. Their greedy methods choose maximizing rows;
(7) instead preserves and reweights existing action frequencies. This is a
different mechanism for the same objective, not an ordinary relabeling of
the same implementation. Their treatment of sparse matrices is also broader
than Theorem 3's all-policy irreducibility scope.

[Murthy, Moharrami and Srikant (2023)](https://proceedings.mlr.press/v211/murthy23a.html)
prove convergence of modified policy iteration for the corresponding
multiplicative, risk-sensitive control setting. Writing a live action row
as $K_a(i,j)=s(i,a)P_a(i,j)$ identifies its one-step log reward as
$\log s(i,a)$ and its asymptotic exponential reward factor as $\rho(K_\pi)$.
Their greedy improvement with partial value evaluation is another strong
planning comparison. The survival interpretation does not replace these
existing optimization results.

[Brandfonbrener et al. (2022/2023), section 3](https://arxiv.org/html/2206.01079v3)
show why conditioning on a chosen high return can select lucky trajectories
and fail to attain an optimal expected return. That comparison supports the
distinction above. Here the binary selection probability is the actual
criterion being improved, so action probabilities are weighted by expected
success. Selecting only an arbitrary extreme realization of a different
reward need not preserve its expected-value ordering. Also, one improvement
step is a different claim from optimality.

The useful bridge for value logic is now explicit: environmental retention
can evaluate a behavior without a represented final utility; copying its
successful actions can improve future success; and the resulting behavior
admits a value representation. Which facts this internalized priority forces
the agent to learn remains governed by practical coverage, as in
[R6.1](R6_goal_judgment.md) and [R6.5](R6_payoff_judgment.md).
