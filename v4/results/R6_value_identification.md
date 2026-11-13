# R6.8 supplement: separating uses can identify the action model

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

Values can recover more than a preferred action: sufficiently varied,
accurately evaluated uses identify the physical consequences of actions.
This is a finite bridge from C7's policy/value duality to C1's recovery of
factual distinctions. It extends [R6.8](R6_policy_values.md) by making the
policy known and the environment unknown. The argument uses established
Bellman and linear-identification machinery; no new algorithmic priority
is claimed. Evaluation of actual uses is essential: mutually consistent
predictions alone do not supply the data assumed below.

## 1. Which value judgments determine a world?

There are $n$ labelled states, $A$ labelled actions and a known discount
$0<\gamma<1$. The unknown row-stochastic action kernels are $T_a$.
Query $\ell$ supplies a known stationary policy $\pi_\ell$, a known
state reward $r_\ell$, and its true state-conditional value vector
$v_\ell$. Different queries may use different rewards or the same reward.
These are values of specified policies, including possible counterfactual
policies, rather than only the best value obtainable for each reward.

For a fixed state $i$, stack its unknown action rows into
$U_i\in\mathbb R^{A\times n}$. Construct a matrix $B_i$ with $An$
columns indexed by $(a,j)$. Include the $A$ row-normalization constraints
and, for each value query, the row

$$
B_i[\ell,(a,j)]=\pi_\ell(a\mid i)v_\ell(j),\qquad
b_i[\ell]=\frac{v_\ell(i)-r_\ell(i)}\gamma.
\tag{1}
$$

Normalization rows have entry $\mathbf1\{a=a_0\}$ and right side one.
Every environment compatible with the supplied values satisfies
$B_i\mathrm{vec}(U_i)=b_i$ at each state, together with
nonnegativity.

**Proposition 1 (joint policy/value separation).** If every $B_i$ has
column rank $An$, the supplied judgments uniquely identify every action
kernel. If the true action kernels are strictly positive, this rank
condition is also necessary for uniqueness in the unrestricted class of
row-stochastic action kernels.

**Proof.** Full column rank makes each linear system have at most one
solution, and the true kernel is a solution. Conversely, if $B_i$ is rank
deficient, take a nonzero null vector and reshape it as $Z_i$. Its action
rows sum to zero. Strict positivity allows sufficiently small positive
and negative multiples of $Z_i$ to be added to $U_i$ while preserving
nonnegativity and row sums. Leave all other state rows unchanged.
Equation (1) says that every supplied $v_\ell$ still satisfies its
policy's Bellman equation in the changed environment. Discounted Bellman
contraction makes that fixed point unique. Thus both changed environments
produce exactly the same supplied values. At boundary kernels,
nonnegativity can sometimes identify a unique solution despite deficient
rank; the necessity claim explicitly excludes that case. $\square$

This condition concerns the **joint** variety of policies and their values.
A long list of near-duplicate goals need not be informative; several
policies under one nonconstant reward can be. It is also conditional on
the labelled state vocabulary and known reward functions, rather than a
construction of those primitives from nothing.

## 2. A constructive coverage condition and its precision cost

Here is a simpler sufficient design. Let the reward columns of
$R\in\mathbb R^{n\times d}$ span $\mathbb R^n$, and choose a right
inverse $C$ with $RC=I$. Evaluate all these rewards under each of $K$
known policies, keeping the same policy across a reward block. Write the
value columns as $V_k$. At each state, let $\Pi_i\in\mathbb R^{K\times A}$
contain those policies' action probabilities and suppose it has a left
inverse $L_i$, so $L_i\Pi_i=I$.

Then

$$
M_k=V_kC,\qquad P_k=\frac{I-M_k^{-1}}\gamma,\qquad
U_i=L_iD_i,
\tag{2}
$$

where row $k$ of $D_i$ is $P_k(i,\cdot)$.

Indeed $V_k=(I-\gamma P_k)^{-1}R$, so the first two identities follow
from R6.8; the third inverts $D_i=\Pi_iU_i$. One policy always choosing
each action gives $K=A$ and $\Pi_i=I$. Reward indicators give $R=I$.
Strictly positive rewards can also span the same space: the columns of
$R_\theta=\theta I+(1-\theta)\mathbf1\mathbf1^\top/n$ do so for
$0<\theta<1$.

Let $\|\cdot\|_\infty$ denote maximum absolute row sum and suppose
$\|\widehat V_kC-M_k\|_\infty\le e$ for all $k$, with
$(1+\gamma)e<1$. The inverse perturbation identity and Neumann series give

$$
\|\widehat U_i-U_i\|_\infty
\le\|L_i\|_\infty
\frac{(1+\gamma)^2e}{\gamma[1-(1+\gamma)e]}.
\tag{3}
$$

For the proof, $\|M_k^{-1}\|_\infty=\|I-\gamma P_k\|_\infty
\le1+\gamma$. Hence the inverse error is at most
$(1+\gamma)^2e/[1-(1+\gamma)e]$; divide by $\gamma$ and multiply
by $L_i$. The raw reconstructed rows can fall outside the stochastic
simplex at finite precision; (3) is a bound for that raw reconstruction.
Projection requires its own norm accounting and is not silently assumed.
If each value entry has error at most $\epsilon$, one sufficient choice
is $e=d\epsilon\|C\|_\infty$. Nearly redundant goals or policies
can therefore make factual reconstruction expensive even when exact
identification holds.

For a concrete boundary, consider a two-state chain that flips with
probability $\rho$, discount $1/2$, and rewards $R_\theta$ above.
The chains with $\rho=1/5$ and $\rho=2/5$ remain distance $2/5$ apart
in maximum row-sum norm, while their value matrices differ in each
entry by only $10\theta/63$. As $\theta$ tends to zero, nominally
different positive goals become hard to distinguish in use. At zero,
all rewards are constant and the models are unidentifiable. Increasing
the separating component or evaluation precision repairs that failure.

## 3. Four uses of one fixed reward can be enough

The rank criterion does not require one reward per state. Consider three
states, two actions, $\gamma=3/4$, state reward $(0,1,3)$, and four
deterministic policies whose action-one vectors are
$(0,0,0),(1,1,1),(0,1,1),(1,0,0)$. The following strictly positive environment is an exact
witness for full rank at all three states:

$$
T_0=\frac1{15}\begin{pmatrix}1&13&1\\1&1&13\\13&1&1\end{pmatrix},
\qquad
T_1=\frac1{15}\begin{pmatrix}1&1&13\\13&1&1\\1&13&1\end{pmatrix}.
\tag{4}
$$

The corresponding value vectors and determinants are rational:

| Policy | Value vector |
| --- | --- |
| $(0,0,0)$ | $(29/7,39/7,44/7)$ |
| $(1,1,1)$ | $(233/49,228/49,323/49)$ |
| $(0,1,1)$ | $(89/40,57/20,209/40)$ |
| $(1,0,0)$ | $(203/40,243/40,139/20)$ |

Using the normalization rows first and these queries in the displayed order,
$\det B_0=131175/21952$ and
$\det B_1=\det B_2=-4275/5488$. Substitution verifies each value's
Bellman equation, and ordinary elimination verifies the determinants.

**Corollary 2 (generic finite instance).** For this fixed reward, discount
and four-policy query design, almost every strictly positive three-state,
two-action environment is identified by its state-conditional values.
Here “almost every” means outside a Lebesgue-null algebraic subset of the
row-stochastic parameter space, not a distribution over real agents.

**Proof.** The exact checker supplies a nonzero $6\times6$ minor of each
$B_i$ at (4). Every value entry is a rational function of the transition
parameters, with nonzero denominator throughout the stochastic parameter
space because $\gamma<1$. Clear the denominators of each chosen minor.
Its numerator is a polynomial that is nonzero at (4), so its zero set
has Lebesgue measure zero and empty interior. Outside the union of these
three sets all matrices have full rank; apply Proposition 1. $\square$

Four is also the minimum number of full state-conditional value queries
that can identify an interior kernel in this observation model. With
fewer than four, each state's matrix has at most $2+3<6$ rows, and
Proposition 1 supplies an indistinguishable alternative. The lower bound
concerns this query interface, not arbitrary observations of transitions.

The witness and its minors are part of the evidence obligation, not a
Monte Carlo claim that a rank check proves genericity. The construction
does not show that evaluating the four policies is economical or that an
agent with one current goal will choose to perform those evaluations.

**Finite precision.** Construct the square matrices $\widehat B_i$ and
right sides from approximate values with simultaneous entry error at most
$\epsilon$. When $\widehat B_i$ is invertible, put
$\widehat u_i=\widehat B_i^{-1}\widehat b_i$. Then

$$
\|\widehat u_i-u_i\|_\infty
\le\|\widehat B_i^{-1}\|_\infty(1+1/\gamma)\epsilon,
\tag{5}
$$

where the vector norm is maximum absolute entry. To prove it, subtract
the true Bellman equations. Each value-query residual is
$e_\ell(i)/\gamma-\sum_{a,j}\pi_\ell(a\mid i)T_a(i,j)e_\ell(j)$,
of magnitude at most $(1+1/\gamma)\epsilon$; the normalization residuals
are zero. Multiplication by the observed inverse gives (5). An unstable
inverse therefore advertises its own precision requirement in this bound.
The bound concerns raw reconstruction, without an unproved projection step.

The required values can themselves be estimated from independent reset
rollouts. In this example rewards lie in $[0,3]$. Choose horizon $H$ with
$12(3/4)^H\le\epsilon/2$ and, for each of the 12 policy/start-state
pairs, use

$$
N\ge\frac{288}{\epsilon^2}\log\frac{24}{\delta}
\tag{6}
$$

rollouts. Truncation plus Hoeffding's inequality gives simultaneous value
error at most $\epsilon$ with probability at least $1-\delta$.
Combining with (5) gives a finite, explicitly priced sufficient route:
$12N$ resets and at most $12NH$ transitions. These conservative bounds
are not an efficient-sampling claim or an executed rollout experiment.

### 3.1 A minimal six-query design in four states

The positive result also survives at the state count where single-reward
ambiguity examples are available. Set $n=4$, $A=2$, $\gamma=3/4$,
$r=(0,1,3,7)$ and use the six action-one vectors

$$
0000,\quad1111,\quad0011,\quad1100,\quad0101,\quad1010.
$$

For an exact witness, use indices modulo four and

$$
T_0(i,j)=\tfrac45\mathbf1\{j=i+1\}+\tfrac1{20},\qquad
T_1(i,j)=\tfrac45\mathbf1\{j=i+2\}+\tfrac1{20}.
$$

The four $8\times8$ system determinants, with normalization rows first,
are respectively

$$
\frac{298944675}{487424},\quad
-\frac{70366725}{746368},\quad
\frac{19118025}{11941888},\quad
-\frac{62493525}{213248}.
$$

The checker reconstructs all four pairs of action rows exactly and stores
all six value vectors. The same nonzero-polynomial proof as Corollary 2
therefore establishes generic identification on the strictly positive
four-state/two-action parameter space for this fixed query design. Six is
minimal: five queries plus two normalization rows cannot have rank eight.
Equation (5) applies to this square design as well; the three-state rollout
budget in (6) is not asserted for its larger reward range and query count.

This is still a generic result. It coexists with structured environments
whose dynamics remain ambiguous under one reward, even after many policy
queries. The [direct source comparison](../notebook/P4-R6-C001/comparison.md)
keeps those quantifiers and observation interfaces separate. A generic
witness does not guarantee good conditioning, economical acquisition or
self-generated exploration by a single-purpose agent.

**A positive-kernel ambiguity and its repair.** Generic identification
is compatible with failure in an everywhere-positive, fully mixing world.
For three states and $r=(0,1,3)$, let every action row initially be
$(1/3,1/3,1/3)$. Change just action 0 at state 0 to $(8,13,9)/30$.
Every row of both worlds still has reward expectation $c=4/3$.
For every stationary policy and every $0<\gamma<1$, both worlds therefore
have the same current-reward value

$$
v=r+\frac{\gamma c}{1-\gamma}\mathbf1.
$$

Substitution in the Bellman equation proves this: each row sends $r$ to
$c$ and sends $\mathbf1$ to one. Even all action-values coincide. The
checker verifies 162 exact evaluations across 27 policies and three
discounts; the displayed identity proves the unrestricted parameter claim.
Changing the goal can break this ambiguity: the spanning reward design in
section 2 recovers either world. Thus the paired characterization is that
policy variety can suffice generically, while reward variety supplies the
stated guarantee over all stochastic kernels. The example does not affect
the minimal-query witnesses, whose determinants are nonzero.

## 4. Optimal value alone describes a different object

At a root state, action $A$ reaches absorbing state 0, $B$ reaches
absorbing state 1, and $C$ reaches them with probabilities $(p,1-p)$.
Let the root reward be zero and the absorbing rewards be arbitrary
$(u_0,u_1)$. For every such reward the optimal root value is
$\gamma\max(u_0,u_1)/(1-\gamma)$, independent of $p$.
All goals therefore identify the same attainable frontier while leaving
the named action $C$'s physical effect unresolved. Evaluating the known
policy that chooses $C$, using either separating reward, recovers $p$.

This complements [R6.7's capability geometry](R6_capability_geometry.md):
optimal values recover the convex attainable set; conditional values for
specified interventions can recover more of the process producing it.
It gives a concrete additional obligation for turning agreement in
successful choice into agreement about the environment.

## 5. Evidence and established comparisons

The [checker](../notebook/P4-R6-C001/value_queries.py) and
[output](../notebook/P4-R6-C001/value_queries.json) preserve exact witness
minors, reconstruction checks, deficient-coverage pairs and the
nearly-constant-reward example. These test the supplied-value mathematics;
they do not implement a new learner acquiring all the required judgments.
With directly observed transitions, ordinary transition-frequency estimation
is the natural competing route and may be much cheaper.

All 1240 exact coverage/reconstruction checks and 960 finite-precision
certificate checks passed. At value-entry errors $10^{-4}$ and $10^{-3}$,
the largest observed reconstructed entry errors were 0.001653 and 0.016651.
At error 0.01, 51/240 raw state reconstructions were nonstochastic; at
0.05, 192/240 were. These are deliberately adverse bounded perturbations,
not sampled rollout error rates. A constructive finite-precision repair is
to choose, for each action, a closest stochastic row in maximum-entry norm.
If (5) bounds the raw error by $b$, the true row is feasible within $b$,
so this projection is within $2b$ of the true row by the triangle
inequality. This elementary repair is mathematical, not an additional
executed planning comparison.

[Grimm et al. (2020)](https://proceedings.neurips.cc/paper/2020/file/3bb585ea00014b0e3ebe4c6dd165a358-Paper.pdf)
make intended policies and continuation functions determine which model
distinctions matter. Their known-reward linear analysis is a close
comparison. [Proper value equivalence (2021)](https://proceedings.neurips.cc/paper_files/paper/2021/file/400e5e6a7ce0c754f281525fae75a873-Paper.pdf)
shows how policy values can suffice for planning while allowing different
models. Our rank condition asks when the supplied values additionally
identify the dynamics, keeping rewards fixed and known. Neither the
existence of useful model equivalences nor this separating case should
be substituted for the other. The contribution here is a precise synthesis
of the project's value-to-fact and policy/value questions, with its
information and precision requirements exposed.

The [closing comparison](../notebook/P4-R6-C001/comparison.md) adds the
strongest direct inverse-Bellman predecessors and distinguishes their
action-value interface from this state-value-only design. This supplement
claims a checked finite construction and synthesis, not priority for
recovering dynamics from values. The generic finite-instance results and
single-reward ambiguity in structured classes are compatible.
