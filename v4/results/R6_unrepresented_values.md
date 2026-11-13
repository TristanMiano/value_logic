# R6.12: value-like structure before a represented terminal goal

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

An environmental survival filter can give initially undirected behavior a
precise value-function description. Under mixing, that description can also
be shared by populations with different fixed terminal biases, away from the
time at which those biases are evaluated. This is a constructive answer to
one reading of “agents with no terminal goals”: no internally represented
utility is required for the selection mechanism. A later learner could
internalize the resulting value, but the selection theorem itself does not
claim that internalization has happened.

This result advances C5's emergence and constraint of value, C7's
behavior/value correspondence, and W6's question about shared subgoals. It
uses established Doob conditioning and entropy-regularized control; the
contribution is their explicit interpretation and separation of mechanisms.

## 1. The environment does the filtering

Let $S$ be a finite set of live states. A baseline controller follows the
strictly positive transition matrix $P$ without computing a reward. In live
state $i$, the environment preserves the trajectory with probability
$s_i\in(0,1]$ and otherwise sends it to an absorbing dead state. If it is
preserved, the next live state follows $P_{ij}$. Thus the live transition
matrix is substochastic:

$$
K_{ij}=s_iP_{ij},\qquad h_n=K^n\mathbf 1.
\tag{1}
$$

$h_n(i)$ is exactly the probability of surviving the next $n$ transitions
from $i$. It is a property of the physical process, whether or not the
controller represents it. No future conditioning changes what the original
unconditioned controller does.

Let $u_g:S\to[0,\infty)$ be a nonzero terminal retention weight for group
$g$. For no terminal bias, use $u_g=\mathbf 1$. Otherwise, retained paths
have weights proportional to their original survival probabilities times
$u_g(X_T)$. A bounded weight can be implemented as a terminal acceptance
probability after division by its maximum. This is an external selection
rule, not an inferred intention of the original controller.

Write $h_n^g=K^n u_g$. For $n$ remaining transitions, the conditional next
state law among retained paths is

$$
Q_n^g(i,j)=\frac{K_{ij}h_{n-1}^g(j)}{h_n^g(i)}.
\tag{2}
$$

All denominators are positive for $n\ge1$. Equation (2) is Bayes' rule:
reach $j$ alive, then pass the remaining filter. It also shows why selection
can produce coherent apparent foresight without an agent computing the
future survival probability.

## 2. A common value and a common interior policy

Strict positivity gives a Perron eigenvalue $\lambda>0$, right eigenvector
$h>0$ and left eigenvector $v>0$, with $Kh=\lambda h$ and
$v^\top K=\lambda v^\top$.

**Theorem 1 (terminal-bias-independent interior behavior).** For every
nonzero $u_g\ge0$,

$$
Q_n^g(i,j)\longrightarrow Q^h(i,j)
=\frac{K_{ij}h_j}{\lambda h_i}
=\frac{P_{ij}h_j}{\sum_kP_{ik}h_k}.
\tag{3}
$$

The limiting transition rule is independent of the group's terminal weight.
It has stationary law $\nu_i=v_ih_i/(\sum_jv_jh_j)$.

**Proof.** The finite positive-matrix theorem gives

$$
K^n u_g=\lambda^n h\frac{v^\top u_g}{v^\top h}
+o(\lambda^n).
\tag{4}
$$

The positive scalar $v^\top u_g$ cancels in the ratio (2), giving (3).
Its rows sum to one by the eigenvector equation. Multiplying $\nu$ by
$Q^h$ and using the left eigenvector equation proves stationarity.
$\square$

The conclusion concerns decisions with an increasingly distant terminal
assessment. With one step remaining, $Q_1^g$ generally depends strongly on
$u_g$. Different clamped goals can therefore preserve different final choices
while exhibiting the same earlier intermediate orientation. This model has
shared transition opportunities, shared survival filtering and positive
mixing; it does not assert agreement for every pair of clamped utilities in
an arbitrary game.

There is a useful distinction within survival conditioning itself. The state
at a distant terminal time, conditioned only on survival to that time,
approaches the normalized **left** eigenvector $v$. A state far from both
the initial and terminal boundaries approaches $\nu\propto vh$. A surviving
endpoint and a typical state in a long surviving history are different
observations. These claims follow by applying (4) to the forward and
backward factors of the corresponding conditional marginal.

## 3. A value representation and an exact control comparison

Set $V_i=\log h_i$. Taking logarithms of the eigenvector equation gives

$$
\log\lambda+V_i
=\log s_i+\log\sum_jP_{ij}e^{V_j}
=\log s_i+\max_{q\in\Delta(S)}
\left\{\sum_jq_jV_j-D_{\mathrm{KL}}(q\Vert P_i)\right\}.
\tag{5}
$$

**Proof of the variational equality.** Define
$q_j^*=P_{ij}e^{V_j}/\sum_kP_{ik}e^{V_k}$. Expanding
$D_{\mathrm{KL}}(q\Vert q^*)\ge0$ gives the equality and shows that the
unique maximizing distribution is $q^*=Q_i^h$. $\square$

Thus the selected process has the same policy as an optimal controller whose
state reward is log survival and whose control cost is divergence from the
baseline dynamics. For any stationary transition rule $Q$ and stationary
law $\eta$ for it, (5), averaged under $\eta$, gives

$$
\sum_i\eta_i\left[\log s_i-D_{\mathrm{KL}}(Q_i\Vert P_i)\right]
\le\log\lambda.
\tag{6}
$$

The $V$ terms cancel by stationarity; $Q^h$ attains equality. This is a
control problem with a specified feasible set and cost, not a claim that
$Q^h$ maximizes raw survival among every physically possible controller.

There is also a finite-horizon exact statement. With a fixed initial state,
let $\mathsf P$ be the baseline path law and let
$H(\omega)=u_g(X_T)\prod_{t<T}s_{X_t}>0$, taking $u_g>0$ here.
The selected law is $\mathsf Q^*(\omega)=\mathsf P(\omega)H(\omega)/Z$,
where $Z=h_T^g(X_0)$. For every path law $\mathsf Q$,

$$
\mathbb E_{\mathsf Q}\log H-
D_{\mathrm{KL}}(\mathsf Q\Vert\mathsf P)
=\log Z-D_{\mathrm{KL}}(\mathsf Q\Vert\mathsf Q^*)\le\log Z.
\tag{7}
$$

This follows by substituting the formula for $\mathsf Q^*$ into KL.
The maximizing law has the causal, time-dependent transitions (2).
Retrospective filtering and prospective control therefore admit an exact
mathematical correspondence, given the dynamics and the divergence cost.
They are distinct physical mechanisms, and neither alone supplies a
learning algorithm for an ignorant individual.

## 4. A two-state example and a quantitative convergence bound

Use live states $A,B$ and

$$
K=\begin{pmatrix}3/5&2/5\\1/10&3/5\end{pmatrix},\quad
s=(1,7/10),\quad
P=\begin{pmatrix}3/5&2/5\\1/7&6/7\end{pmatrix}.
\tag{8}
$$

The eigenvalues are $4/5$ and $2/5$. Take $h=(2,1)$ and $v=(1,2)$.
Then

$$
Q^h=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix},\qquad
\nu=(1/2,1/2).
\tag{9}
$$

The unfiltered live-movement chain $P$ spends $5/19$ of its stationary time
in $A$. The interior of long survival-selected histories spends $1/2$ there;
the survival-selected endpoint distribution is $(1/3,2/3)$. The numbers
describe three different sampling procedures.

For $u=(a,b)\ge0$ nonzero, let $\kappa=(2b-a)/(a+2b)\in[-1,1]$.
Diagonalizing $K$ gives

$$
K^n u=\left(\frac45\right)^n\frac{a+2b}{4}
\left[(2,1)+2^{-n}\kappa(-2,1)\right].
\tag{10}
$$

Substitution into (2) yields the uniform bound

$$
\max_i\mathrm{TV}(Q_n^g(i,\cdot),Q^h(i,\cdot))
\le\frac{(3/4)2^{-n}}{1-2^{-n}},\qquad n\ge1.
\tag{11}
$$

For row $A$ the exact error is
$(3/4)|2^{-n}\kappa|/(1-2^{-n}\kappa)$; for row $B$ it is the same
numerator divided by $1+2^{-n}\kappa$. This proves (11), including terminal
weights that select only one state. Ten transitions before the terminal
assessment, the error is at most $1/1364\approx0.00073314$ for every such
terminal bias. The endpoint choices can still differ maximally.

## 5. Implemented transfer into a controller

The [checker and experiment](../notebook/P4-R6-C001/unrepresented_values.py)
implement a simple transmission step. An action selects the next live state;
survival before that action still follows $s_i$. Start with the reward-free
baseline policy $P$. Reset to each state, run it for $T$ steps, retain only
surviving trials that pass the terminal filter, and estimate each policy row
from the retained **first actions**, with add-one smoothing. The learner
receives first actions and retention flags, not $K$, $h$, or true value labels.
Its learned policy is then deployed stationarily in the same physical world.

This is actual policy cloning from externally selected experience. It is not
the original controller spontaneously rewriting its own preferences, and
it does not preserve the group's terminal policy near an endpoint. The
experiment tests whether the common early bias can be transmitted and help
future survival. Here are means across 16 training seeds, evaluated by exact
32-step survival probability from $A$:

| Training horizon | No terminal bias $(1,1)$ | Bias toward $A$, $(9,1)$ | Bias toward $B$, $(1,9)$ |
|---:|---:|---:|---:|
| 2 | 0.004916 | 0.120186 | 0.000432 |
| 4 | 0.013163 | 0.030030 | 0.007622 |
| 8 | 0.017448 | 0.018332 | 0.016891 |
| 12 | 0.018444 | 0.017713 | 0.018315 |

Baseline survival is **0.00118842**; the limiting selected controller gives
**0.01760822**, about 14.82 times the baseline. A controller with a model and
unrestricted survival optimization always chooses $A$ and achieves **1**
from $A$ (and 0.7 from $B$). Thus the transferred bias is useful, while the
model-based planner is substantially stronger on raw survival. The short
horizon and $B$-favoring filter even produce worse survival than the baseline;
longer lookahead through selection removes that particular interference.

Every setting and seed uses 65536 **attempted** trajectories from each initial
state: 25,165,824 attempts across the whole panel. No unsuccessful trial is
omitted from this cost count. At $T=12$ without terminal bias, the mean
accepted counts are 6733.625 from $A$ and 3371.0625 from $B$. The mean row-TV
estimation error is 0.007496, larger than the finite-to-limit bias 0.00006104;
increasing the horizon reduces terminal interference but makes successful
training data scarcer. The $T=12$ survival standard errors from $A$ are
0.000405, 0.000573 and 0.000387 in table order. Exact model evaluation of
learned policies is kept separate from what their training algorithm observes.

The same checker verifies 240 rational terminal-bias bounds, 1656 enumerated
path weights, and 200 finite-path KL identities. All passed. Retained counts
and per-seed policy summaries are in the
[result JSON](../notebook/P4-R6-C001/unrepresented_values.json); no path trace
is committed. The mathematical limits follow from the proofs, not this panel.

## 6. What this explains, and the constructive next step

The internal value function in (5) is reconstructed from environmental
survival and baseline behavior. It need not have existed as a represented
terminal goal in the initial controller. Nor does mere survival entail that
the controller learned it: selecting histories changes a conditional
distribution. Actual goal formation requires an inheritance, imitation or
within-agent update mechanism that transfers the useful bias into future
action. Section 5 implements one simple external imitation mechanism.
[R6.13](R6_selection_learning.md) and its [sampling supplement](R6_selection_sampling.md)
subsequently supply exact and finite-trial improvement/convergence results
under their additional conditions. Learning an explicit internal reward
and its own revision rule remains a
stronger target; R6.4/R6.6 supply separate simple mechanisms to connect.

If survival is state-independent, $s_i=s$, then $h=\mathbf 1$,
$Q^h=P$ and $V$ is constant. There is no new directional preference. If the
live process splits into isolated components, different terminal filters can
retain different components and the common-interior conclusion can fail.
Restoring communication and an effective mixing scale repairs that case;
slow communication can leave differences for a long finite time. These are
conditions governing the selection of a common orientation, not evidence
that goal formation is either automatic or impossible.

[Chetrite and Touchette (2015), section VI.3 and appendix E](https://arxiv.org/html/1405.5157v3)
give the established conditioned-process framework, including the different
endpoint and interior distributions. Their
[variational companion, appendix C](https://arxiv.org/html/1506.05291v2)
relates driven Markov chains to entropy/control optimization.
[Todorov (2006), sections 2--2.1](https://papers.nips.cc/paper_files/paper/2006/file/d806ca13ca3449af72a1ea5aedbed26a-Paper.pdf)
constructs linearly solvable control problems using precisely a divergence
cost and an exponential value transform. These are enabling results and
stronger general algorithms, not methods defeated by the example.

For the project, the useful lesson is a typed sequence: **physical filtering
can create a value-shaped pattern; a separate transmission mechanism can
internalize it; informative practical feedback can then test its judgment**.
The first step has an exact construction here; the second has the small
implemented cloning example. Reliable judgment under the transmitted rule
still requires its own evidence. This preserves a substantive reading of values emerging
without initially clamped represented goals while keeping environmental
pressure, internal evaluation and normative justification distinct.
