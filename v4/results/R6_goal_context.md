# R6.14: shared factual pressure with context-dependent goals

**Codex (GPT-6), November 12, 2026. P4-R6-C001; cycle complete; module available to recur.**

Different agents can be pushed toward the same factual distinctions even
when their goals and the situations they encounter are correlated. The
positive condition is overlapping practical exposure: a distinction must
matter for a goal that can occur on both sides of it. When the goal itself
supplies information, the right recovery target includes that information.
This extends [R6.1](R6_goal_judgment.md), serves C1/C2, and explains a precise
way for clamped goals to coexist with converging or diverse factual subgoals.

## 1. The downstream goal is also side information

Let $X$ be a finite context with $\mu(x)>0$, $G\in\{1,\ldots,m\}$ a
goal, and $Y$ an outcome. Write

$$
\pi_j(x)=\mathbb P(G=j\mid X=x),\qquad
z_j(x)=\mathbb E[v_j(Y)\mid X=x],\quad 0\le v_j\le1.
\tag{1}
$$

Assume $Y\perp G\mid X$. A representation $c(X)$ is formed before the
goal is disclosed. The decision rule sees $(c(X),G,T)$, where the price
$T\in[0,1]$ is independent of $(X,Y)$ given $G=j$ and has density $f_j$.
Buying pays $v_j(Y)-T$; declining pays zero. The fully informed rule buys
at $T\le z_j(X)$. The best rule using the representation buys at

$$
T\le q_j(c),\qquad
q_j(C)=\frac{\sum_{x\in C}\mu(x)\pi_j(x)z_j(x)}
{\sum_{x\in C}\mu(x)\pi_j(x)}.
\tag{2}
$$

The value on a cell with zero denominator is irrelevant. Let $\Delta(c)$
be the fully informed expected payoff minus this representation's best
expected payoff. Both rules see the same goal and price. The richer rule
additionally sees $X$; no goal information is silently given to only one
side of the comparison.

**Proposition 1 (weighted factual pressure).** If $f_j(t)\ge\rho_j>0$
on $[0,1]$, then

$$
\Delta(c)\ge\frac12\sum_j\rho_j
\mathbb E\!\left[\pi_j(X)(z_j(X)-q_j(c(X)))^2\right].
\tag{3}
$$

For uniform prices equality holds with every $\rho_j=1$. More generally,
if every nonempty open price interval has positive probability, zero loss
holds exactly when $z_j$ is constant on each cell intersected with
$\{x:\pi_j(x)>0\}$, for every goal $j$.

**Proof.** At a context with true expectation $z$ and report $q$, the
conditional payoff regret is

$$
d_j(z,q)=\int_q^z(z-t)f_j(t)\,dt
\ge\frac{\rho_j}2(z-q)^2.
\tag{4}
$$

The oriented integral is nonnegative in either order of $z,q$. Average it
with weights $\mu(x)\pi_j(x)$ and use the payoff-optimal conditional mean
(2). Uniform density gives equality. Under qualitative full price support,
the integral is strictly positive whenever $z\ne q$, which proves the
zero-loss characterization. $\square$

**Corollary 1 (an exposure floor replaces independence).** If additionally
$\pi_j(x)\ge a_j>0$ for every $x,j$, then

$$
\Delta(c)\ge\frac12\sum_j a_j\rho_j
\mathbb E\mathrm{Var}(z_j(X)\mid c(X)).
\tag{5}
$$

For each cell, its weighted squared error is at least $a_j$ times the
unweighted squared error evaluated at that same $q_j$, which is at least
$a_j$ times the error at the unweighted conditional mean. This proves (5).
If $Y$ is finite and $p(X)=\mathbb P(Y=\cdot\mid X)$, put
$A=\sum_j a_j\rho_jv_jv_j^\top$. If $A$ has minimum eigenvalue
$\lambda>0$ on the zero-sum tangent space, then

$$
\mathbb E\|p(X)-\mathbb E[p(X)\mid c(X)]\|^2
\le\frac{2\Delta(c)}\lambda.
\tag{6}
$$

Thus contextual correlations need not defeat the judgment-to-fact bridge.
They enter its quantitative coverage condition. A small positive exposure
floor gives qualitative identification but potentially weak practical
pressure; the cost example below makes that difference explicit.

## 2. When there is a single coarsest factual representation

Make an incompatibility graph on contexts. Distinct $x,x'$ are adjacent iff
some goal $j$ satisfies

$$
\pi_j(x)\pi_j(x')>0\quad\text{and}\quad z_j(x)\ne z_j(x').
\tag{7}
$$

**Proposition 2 (adequacy and its typing).** Under full price support,
$\Delta(c)=0$ iff each representation cell is an independent set of this
graph: equivalently, $c$ is a proper coloring. A single coarsest adequate
partition, refined by every other adequate partition, exists iff the graph
is complete multipartite.

**Proof.** A cell violates (7) exactly when its two contexts need different
expectations for the same possible downstream goal. Proposition 1 proves
the coloring characterization. Include equality in the nonadjacency
relation. If it is transitive, its equivalence classes are independent sets
and all cross-class pairs are adjacent: these classes form the unique
coarsest adequate partition. Conversely, if nonadjacency is not transitive,
there are $x,y,z$ with $x$ compatible with $y$, $y$ compatible with $z$, and
$x$ adjacent to $z$. The partition merging only $x,y$ and the one merging
only $y,z$ are both adequate. Any common coarsening merges $x,z$ and is
inadequate. A coarsest adequate partition therefore cannot exist. $\square$

With full goal support, nonadjacency means equality of the whole vector
$(z_1(x),\ldots,z_m(x))$, an equivalence relation. R6.1's shared quotient is
recovered without requiring independence. With missing support, the typed
task target is instead $(G,z_G(X))$, and adequacy means that this target is
recoverable from $(c(X),G)$. Distinct encodings can meet the same practical
obligation. This is a constructive repair of an overly simple single-task-
partition reading of T = J², not evidence that the coupling has no content.

The graph is an instance of the established characteristic graph for
zero-error function computation with decoder side information. See
[Charpenay, Le Treust and Roumy (2024), definition 4](https://www.mdpi.com/1099-4300/26/4/338).
Here the function to recover is $f(x,j)=z_j(x)$ and the encoder has no
additional side information. Graph coloring is imported structure. The
specific contribution is the practical-regret derivation, the distinction
between a factual quotient and a side-information code, and their role in
the typed judgment/convergence claim. No new general coding theorem is
claimed.

## 3. More exposure can make a factual distinction worth its cost

Take three equally likely contexts $0,1,2$, with
$z_A=(0,1/2,1)$ and $z_B=0$. Initially goal $A$ occurs at contexts $0,2$
and goal $B$ at context 1. The only graph edge is $0$--$2$. Both partitions
$\{0,1\}\mid\{2\}$ and $\{0\}\mid\{1,2\}$ are adequate. Their
labels alone differ in the distinctions retained, but combining either with
the goal actually identifies the context. This is informative agreement at
the level needed for action, not agreement on one isolated representation.

Mix the initial assignment with probability $\epsilon$ of uniform random
goal choice, so

$$
\pi_A=(1-\epsilon/2,\epsilon/2,1-\epsilon/2),\qquad
\pi_B=1-\pi_A.
\tag{8}
$$

For every $\epsilon>0$, only the full three-cell representation has zero
loss. With uniform prices, the minimum regret for one, two and three cells
is, respectively,

$$
\Delta_1=\frac{1-\epsilon/2}{12},\qquad
\Delta_2=\frac{\epsilon(1-\epsilon/2)}{48},\qquad
\Delta_3=0.
\tag{9}
$$

The two optimal two-cell choices merge adjacent contexts; merging $0,2$
has regret $\Delta_1$. These formulas follow directly from weighted
conditional variances in (3). With cost $\kappa(k-1)$ for $k$ cells, the
three-cell representation is optimal when $\kappa<\Delta_2$, two cells
when $\Delta_2<\kappa<\Delta_1-\Delta_2$, and one cell when
$\kappa>\Delta_1-\Delta_2$. Equalities give the corresponding ties.
The middle interval is nonempty for $0\le\epsilon\le1$.

At $\kappa=0.005$, full retention becomes worthwhile precisely above
$\epsilon=1-\sqrt{0.52}\approx0.27889$. At lower positive exposure,
the extra distinction is identifiable in principle yet not worth its cost
in this declared task. Increasing recurrence of that goal can change the
optimal representation while terminal preferences stay clamped.

## 4. Evidence and remaining extension

The proof is finite and explicit. The [rational checker](../notebook/P4-R6-C001/goal_context.py)
passed 54,253 graph/partition comparisons on every graph with at most five
vertices, 5862 regret/coloring/bound checks across 120 declared random
finite instances, and 44 exact exposure/cost settings. The counts of graphs
admitting a coarsest adequate partition were 1, 2, 5, 15 and 52 for one
through five vertices, matching the complete-multipartite characterization.
Uniform and nonuniform full-support prices were both checked.
The construction assumes the goal-conditional outcome expectations are
known when defining the optimal representation. Learning the changing
support and expectations from bounded feedback is a separate extension;
[R6.5](R6_payoff_judgment.md) supplies a compatible exploration ingredient,
not an already executed integration with this graph model.
