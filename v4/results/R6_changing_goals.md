# R6.11: common priorities under goals that sometimes oppose them

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

A priority can become a stable practical orientation even when some recurring
goals oppose it. The relevant condition depends on how agents encounter those
goals. Shared sequences select by cumulative log advantage; independently
distributed opportunities in a reproducing or retaining population select by
a matrix growth rate. With continuing revision, shared experience can erase
initial differences while priorities continue to fluctuate. This supplies a
more faithful C5 reading of an attractor than a permanently fixed scalar value.

Evidence: self-contained arguments below and a finite checker. The model is
an extension of [plastic priorities](R6_plastic_priorities.md), not an account
of all human motivation. A priority's external retention advantage and its
represented desirability remain different objects.

## 1. A shared changing environment

Let $q_t\in(0,1)$ be the retained fraction or normalized weight of programs
with a particular internal priority. When goal $g_t$ is encountered, this
priority has multiplier $R_t=R(g_t)>0$ relative to programs without it. After
selection, either priority flips to the other with probability
$\mu\in[0,1/2)$. The update is

$$
q_{t+1}=F_{R_t,\mu}(q_t)
=\frac{(1-\mu)R_tq_t+\mu(1-q_t)}{R_tq_t+1-q_t}.
\tag{1}
$$

The same $g_t$ applies to all programs in this model. In a single bounded
agent, the weights could instead be an explicit multiplicative retention
rule over competing routines. That implementation assumes this update rule;
it does not derive the rule from an initially complete absence of asymmetry.

**Proposition 1 (mixed favorable and unfavorable goals).** Suppose $\mu=0$
and the realized sequence satisfies

$$
\frac1t\sum_{s<t}\log R_s\longrightarrow L.
\tag{2}
$$

Then $L>0$ implies $q_t\to1$, and $L<0$ implies $q_t\to0$. For an irreducible
finite-state stationary Markov goal process with stationary law $\rho$,
$L=\sum_g\rho_g\log R(g)$ almost surely. Stationarity can be replaced by any
initial law for such an irreducible finite chain.

**Proof.** The odds satisfy $q_{t+1}/(1-q_{t+1})=R_tq_t/(1-q_t)$.
Their logarithm is the initial log odds plus the sum in (2). The Markov case
uses its empirical occupation frequencies. Neither independence nor
aperiodicity is required for those frequencies. At $L=0$ this argument leaves
the outcome open: alternating $R=2,1/2$ gives a nonconstant two-cycle from
every interior starting weight. $\square$

Thus “usually helpful” has an explicit repair: positive cumulative log
advantage. Counting favorable contexts alone ignores the magnitudes of gains
and losses. The nine-favorable-one-catastrophic example in R6.4 demonstrates
the distinction.

## 2. Continuing revision synchronizes a changing priority

Let $\ell=\log(q/(1-q))$, $c=1-2\mu$, and
$B=\log((1-\mu)/\mu)$, now with $0<\mu<1/2$. Equation (1) becomes

$$
\ell_{t+1}=\varphi_\mu(\ell_t+\log R_t),\qquad
\varphi_\mu(x)=\log\frac{(1-\mu)e^x+\mu}{\mu e^x+1-\mu}.
\tag{3}
$$

**Theorem 2 (shared-experience agreement and its tolerance).** For every
positive sequence $R_t$, two trajectories with the same revision rate and
same sequence satisfy

$$
|\ell_t-\tilde\ell_t|\le c^t|\ell_0-\tilde\ell_0|.
\tag{4}
$$

After their first update both log odds lie in $[-B,B]$, including trajectories
started at $q_0=0$ or $1$. If the log advantages of two agents instead differ
by at most $d$ at each step, then

$$
|\ell_t-\tilde\ell_t|
\le c^t|\ell_0-\tilde\ell_0|+
\frac{cd(1-c^t)}{1-c}.
\tag{5}
$$

In particular, a stable discrepancy between their clamped final goals can
leave a bounded discrepancy in their shared subgoal's priority.

**Proof.** With $s=(1+e^{-x})^{-1}$, the output probability is $\mu+cs$.
Differentiation gives

$$
\varphi_\mu'(x)=\frac{c\,s(1-s)}{(\mu+cs)(1-\mu-cs)}\le c,
\tag{6}
$$

because the denominator minus $s(1-s)$ equals
$\mu(1-\mu)(2s-1)^2\ge0$. It is positive, so the map is increasing.
The mean-value theorem proves the one-step contraction, which iterates to
(4); the triangle inequality adds $cd$ per step and proves (5).
The endpoint limits of (3) are $\pm B$. $\square$

For a two-sided stationary sequence of goals, iterating (3) from time $-n$
gives a Cauchy sequence at time zero: changes in the starting value after its
first update are bounded by $2Bc^{n-1}$. Its limit defines a unique stationary
priority process driven by those goals. Every other starting value approaches
that process along the same goal realization. For iid goals this also proves
uniqueness and convergence in distribution of the invariant law of (1), by
coupling trajectories using the same future draws. For Markov goals, apply
the statement to the joint goal/priority process with the stationary goal
law; convergence of an arbitrarily initialized goal's law may require
aperiodicity, even though pathwise forgetting of priority does not.

This is convergence to a **changing trajectory**, not a claim that $q_t$
converges to one number. Independent streams can produce different current
priorities despite the same invariant law. Conversely, identical initial
values can diverge under different evidence. Continuing revision supports
forgetting of initial conditions; reducing revision supports persistence but
slows this particular route to agreement.

**Corollary 3 (a broad but imperfectly useful priority).** For iid goals with
$R_t=r$ with probability $p$ and $R_t=1/r$ otherwise, $r>1$, the unique
invariant law has mean $1/2$ at $p=1/2$, mean above $1/2$ at $p>1/2$, and
mean below $1/2$ at $p<1/2$.

**Proof.** Reflection $q\mapsto1-q$ exchanges $R$ and $1/R$, so uniqueness
makes the $p=1/2$ law reflection-symmetric. Couple all goal draws by one
uniform random variable. Increasing $p$ increases each multiplier, and
$F$ is strictly increasing in both its multiplier and its interior input.
Pullback limits preserve the resulting stochastic order. For $p>1/2$, the
most recent draw lies in the interval $(1/2,p)$ with positive probability;
on that event the two updates differ strictly, even if their previous values
coincide. This yields strictly ordered means. Reflection gives $p<1/2$.
$\square$

The corollary is a distributional sense in which a more broadly useful
priority becomes more persistent without becoming literally clamped.
Asymmetric gains, asymmetric revision and goal-dependent feedback require
their own conditions; the number of favorable goals is sufficient here
because their two magnitudes were specified as reciprocals.

## 3. Independently distributed opportunities: another selection law

Now many lineages or retained routines occupy different goals at the same
time. There is no priority mutation initially. Both types change goals by
the same strictly positive row-stochastic matrix $K$. Type $i$ has positive
multiplier $f_i(g)$ at goal $g$, and its row vector of unnormalized masses
evolves by

$$
z_{i,t+1}=z_{i,t}M_i,\qquad M_i=\mathrm{diag}(f_i)K.
\tag{7}
$$

**Proposition 4 (growth-rate selection).** Let $\lambda_i$ be the Perron
eigenvalue of $M_i$, and start with positive mass of both types. If
$\lambda_1>\lambda_0$, then the normalized fraction of type 1 converges to
one both overall and conditional on each goal. Some goals may nevertheless
have $f_1(g)<f_0(g)$.

**Proof.** Strict positivity gives positive left Perron vectors $v_i$ and
$z_{i,t}=a_i\lambda_i^t v_i+o(\lambda_i^t)$, with $a_i>0$.
Their ratio at each goal tends to zero for type 0 relative to type 1.
$\square$

If symmetric priority mutation $\mu>0$ follows each update, the joint
goal/type matrix is positive and has a unique normalized Perron vector.
As $\mu\downarrow0$, that vector converges to the winning type's Perron
vector with zero mass on the losing type, provided the strict eigenvalue gap
holds. To see this, take any convergent subsequence of normalized positive
eigenvectors. Continuity of eigenvalues makes its limit an eigenvector of
the block diagonal matrix at $\mu=0$ for eigenvalue $\lambda_1$.
The gap forces its type-0 component to vanish; positivity and normalization
uniquely determine the type-1 component. Compactness then gives convergence
of the whole sequence. This proves high retention for sufficiently small
continuing revision without demanding advantage at every goal.

When every row of $K$ is $\rho$, $\lambda_i=\sum_g\rho_gf_i(g)$.
For $f_0=1$, $f_1=(2,1/2)$ and $\rho=(2/5,3/5)$, this population law favors
type 1 with growth $11/10>1$. The synchronous model in section 1 instead
has log advantage $-(1/5)\log2<0$ and loses type 1. Neither calculation
overturns the other: correlated exposure and distributed exposure are
different environments. Equation (7) is a deterministic mass model;
finite-population extinction and stochastic realized lineage growth are
separate obligations.

## 4. Reproducible finite checks

The [checker](../notebook/P4-R6-C001/changing_goals.py) and
[output](../notebook/P4-R6-C001/changing_goals.json) contain 3200 rational
identity/inequality checks, 9000 bounded-discrepancy steps, and a comparison
of matrix eigenvectors with normalized population iteration. All passed.
For the reciprocal-goal experiment, 32 replicas each use 2000 burn-in and
24000 recorded steps. At $p=0.6$:

| Revision probability $\mu$ | Mean priority | Fraction of time above $1/2$ | Mean absolute difference between independent streams |
|---:|---:|---:|---:|
| 0.005 | 0.840697 | 0.904203 | 0.198657 |
| 0.02 | 0.725308 | 0.821563 | 0.243516 |
| 0.1 | 0.586790 | 0.693324 | 0.188739 |

These are finite simulation summaries, not exact stationary expectations.
The corresponding replicate-mean standard errors are 0.001549, 0.001151 and
0.000507. Shared-uniform coupling across $p=0.4,0.5,0.6$ preserved the proved
order at every checked step. The substantial independent-stream differences
show why distributional convergence should not be reported as identical
current values. Under the distributed-opportunity example with $p=0.4$,
stationary priority rises from 0.591271 at $\mu=0.1$ to 0.998901 at
$\mu=0.0001$, although the synchronous zero-revision priority loses.

## 5. Relation to established work and the project

The contraction is an elementary two-type instance of positive-map
contraction in log-ratio/Hilbert distance, associated with
[Birkhoff (1957)](https://doi.org/10.2307/1992971). We provide the complete
derivative argument rather than claim a new general contraction theorem.
[Kussell and Leibler (2005)](https://doi.org/10.1126/science.1114383) study
population growth, phenotype switching and information in fluctuating
environments; their abstract already identifies a setting where switching
rates track environmental statistics. That broader biological mechanism is
established work. The source's full technical argument has not been used to
justify the specific formulas here.

The useful synthesis is to separate four questions about “terminal-like”
values: which values are selected, whether initial differences disappear,
whether the resulting priority is constant or moving, and whether its
persistence survives removal of its benefit. R6.4 handles the last question;
this result handles the first three under mixed favorable and unfavorable
goals. Together they advance C5's constrained recursive revision and explain
which kind of agreement can connect instrumental convergence to J².

The next constructive target is judgment that learns its own environmental
advantages while retaining coverage of informative tasks. The paired limit
is endogenous loss of that coverage or selection of a self-confirming
convention. Neither the present retention equation nor its convergence
settles whether the retained value is factual or normatively justified.
