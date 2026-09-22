# F02 continuation: what each candidate can forget

Research date: September 22, 2026. Base: `ba551afe7f4c026c075a49b09b341eec446caf1a`
plus the uncommitted, hash-verified F02 S1 package. This note supplements
[the four-candidate comparison](02_candidate_semantics.md); it does not select
one candidate, start F03/F06, or establish the eventual calculus's soundness.

The review is same-agent and non-blinded. Each result below has an operational
question, stated information and quantifiers, a finite or explicitly specified
mathematical argument, and a limitation. New calculations are development
fixtures, not a held-out empirical evaluation or evidence of novelty.

The [S2 completion record](../work_logs/F02_2026-09-22_S2.md) links observed
clocks, tests and acceptance evidence. Focused external checks are recorded
in the [source note](../work_logs/F02_2026-09-22_S2_sources.md); they do not
complete F03. F02 totals 61.118295 credited D minutes and 124 passing dedicated
checks across its two sessions. No new core or gate is selected.

## A. What all scalar tradeoffs preserve, exactly

### A.1 Reconstructing the deterministic guarantee question

Let a nonempty finite menu have cost vectors $A\subset\mathbb R^d$ in declared
component units, with smaller components better. Candidate G retains

$$
\Gamma_A=A+\mathbb R_+^d
=\{b:\exists a\in A,\ a\leq b\}.
$$

Candidate S, when used to summarize the *optimal* scalarized costs over that
menu, can retain the complete function

$$
f_A(w)=\min_{a\in A}w\cdot a,
\qquad w\geq0,\quad \sum_jw_j=1.
$$

These weights are declared conversions/tradeoffs, not an untyped sum of unlike
units. Once coordinates have been normalized, the following comparison is exact:

> Two nonempty finite menus have the same $f_A$ for every such weight exactly
> when their convex upper hulls $\operatorname{conv}(A)+\mathbb R_+^d$ agree.

This identifies the lost information more specifically than one counterexample.
It does **not** say that a family of arbitrary numerical codes cannot retain a
menu, or that scalarization cannot be useful for its own declared query.

**Forward calculation on one hull.** Write $C_A=\operatorname{conv}(A)+\mathbb R_+^d$.
For any nonnegative $w$, adding nonnegative slack cannot lower $w\cdot a$, and
a convex average cannot lie below the smallest component scalar score. Thus

$$
\inf_{x\in C_A}w\cdot x=\min_{a\in A}w\cdot a=f_A(w).
$$

The reverse inequality follows because every $a\in A$ lies in $C_A$; the
infimum is attained at a minimizing menu member. Equal hulls therefore give
equal optimum functions.

**Recovering the hull from those questions.** The set $C_B$ is nonempty, closed,
and convex. For closedness, if $b_n+s_n\to z$, with $b_n\in\operatorname{conv}(B)$
and $s_n\geq0$, compactness of the finite convex hull gives a subsequence
$b_n\to b$ and then $s_n\to z-b\geq0$. Convexity follows from the definitions.
For any $x\notin C_B$, choose a nearest point $y\in C_B$. Existence follows by
restricting a minimizing sequence to a sufficiently large closed ball and using
finite-dimensional compactness. Set $w=y-x\ne0$. For every $z\in C_B$, the
segment $y+t(z-y)$ stays in $C_B$. Expanding its squared distance to $x$ and
taking the right derivative at $t=0$ gives

$$
w\cdot(z-y)\geq0.
$$

Since $y+t e_j\in C_B$ for every $t\geq0$, this inequality also gives $w_j\geq0$.
Consequently $w\cdot x=w\cdot y-\|w\|^2<w\cdot y=\inf_{z\in C_B}w\cdot z$.
Normalize $w$ by its positive coordinate sum. If $x\in C_A$, then
$f_A(w)\leq w\cdot x<f_B(w)$. Thus equal optimum functions rule out a point
of either convex upper hull outside the other. This proves the stated equivalence
without assuming the full deterministic upper sets are convex.

### A.2 Why the menu example changes when mixing is admitted

For $A=\{(0,2),(2,0)\}$ and $B=A\cup\{(3/2,3/2)\}$, the convex upper hulls are
the same: $(3/2,3/2)$ lies above the mixture $(1,1)$. Their deterministic upper
sets differ, since the budget $(3/2,3/2)$ is met by B alone. This reconstructs
the S1 example and identifies its exact source: convex upper closure.

If an agent may freely choose an independent lottery over the menu and the
requirements bound **expected** component costs, the attainable mean vectors
are exactly $\operatorname{conv}(A)$. In that changed operational problem,
$C_A$ is the correct guarantee set and all scalar tradeoffs preserve it. The
previous separation disappears for a substantive reason, not through a repair
of faulty arithmetic.

If instead every realized use must meet the coordinate budget, randomization
does not help this existence question. A lottery succeeds almost surely only
if every positive-probability menu member meets the budget; choosing any one
such member already works. This statement concerns a deterministic known menu
and one joint coordinate-cap event, not arbitrary chance constraints or unknown
models.

### A.3 Randomization and uncertainty cannot be collapsed in the opposite order

With one cost coordinate, consider two actions and two possible fixed models:

| action | model 0 | model 1 |
|---|---:|---:|
| a | 0 | 2 |
| b | 2 | 0 |

A fixed pure action has worst-model cost two. Replacing each action by that
robust scalar and then mixing still gives two. But a lottery choosing a with
probability $t$, drawn independently of the fixed hidden model, has model-wise
expected costs $2(1-t)$ and $2t$. Its worst expected cost is

$$
2\max\{t,1-t\}=1+2|t-1/2|,
$$

minimized at one by $t=1/2$. Thus the pre-lottery robust-coordinate compression
that was exact for fixed-action universal caps is no longer exact for robust
*expected* costs of a controllable lottery. It remains a conservative upper
bound. Keeping the model-action table through averaging recovers the result.

If nature observes the realized action before selecting its model, or if costs
must satisfy the bound for every random draw, the worst cost is instead two.
No claim of improvement survives that changed information/aggregation contract.
Candidate G can admit this explicitly richer randomized robust variant, but it
is not obtained for free from an already compressed pure-action frontier.

## B. Candidate T: which choices can depend on which inputs?

### B.1 Pointwise maximum chooses after the input is available

Let a finite menu of transformers be $T_i:\mathbb R^B\to\mathbb R^A$. Its
pointwise envelope is $D(h)(a)=\max_i T_i(h)(a)$. For an observed input a and an
already specified continuation h, this value is attained by an appropriate
branch. That does not give one input-independent branch attaining the envelope.

For input law $\mu$ and a branch chosen **before** an unobserved input is known,
the best expected value is

$$
V_{\rm blind}(h)=\max_i\sum_a\mu_a T_i(h)(a).
$$

When a is observed before branch selection, it is

$$
V_{\rm observed}(h)=\sum_a\mu_a\max_i T_i(h)(a).
$$

For each i the latter minus its expectation is a sum of nonnegative gaps.
Therefore $V_{\rm blind}\leq V_{\rm observed}$, with equality exactly when some
single branch maximizes at every input with positive $\mu_a$. A finite menu
ensures a blind optimum is attained. This is an explicit quantifier test, not
a theorem giving an unobserved input to an agent.

### B.2 An equal-map separation survives despite knowing every continuation

There are two inputs 0,1 and two outputs L,R. The first menu contains identity
and swap transitions:

$$
f_I=(L,R),\qquad f_S=(R,L).
$$

A second menu also contains the constant-output transitions $(L,L)$ and $(R,R)$.
All immediate rewards are zero. Pointwise maximization gives the same complete
transformer for both menus:

$$
D(h)=(\max(h_L,h_R),\max(h_L,h_R)).
$$

Yet under a uniform *unobserved* input and $h=(1,0)$, the first menu can obtain
only $1/2$, while the second obtains one by committing to constant L. A mixture
of identity and swap still gives $1/2$, so allowing input-independent randomization
does not remove this separation. Allowing input observation does remove it.

The extensional optimized T map has retained the row-wise envelope, not which
rows belong to the same available global branch. The candidate must either
restrict composition to its observed-input contract, retain a family of kernels
with shared policy labels, or admit that the blind precommitment question lies
outside its compressed interface. A branch name used to retrieve the forgotten
kernel family is additional input.

This is distinct from S1's one-input lottery/menu separation. There, scalar
optimization lost a multi-constraint capability. Here, scalar expected payoff
is still the objective, but the *timing of one shared choice* changes what the
map must preserve.

## C. A tighter task-family interface for affine T steps

### C.1 Exact propagation of a relative-stakes allowance

Write $\operatorname{osc}(h)=\max h-\min h$ on a finite nonempty interface.
For a primitive $U(h)=r+Ph$, with stochastic rows $p_a$, define

$$
B_U(M)=\max_{a,b}\left[r_a-r_b+M\,\operatorname{TV}(p_a,p_b)\right],
\qquad \operatorname{TV}(p,q)=\frac12\sum_j|p_j-q_j|.
$$

Then for every $M\geq0$,

$$
\sup_{\operatorname{osc}(h)\leq M}\operatorname{osc}(U(h))=B_U(M).
$$

**Proof.** A constant shift of h cancels between two output coordinates because
the two rows each sum to one. Shift h into $[0,M]^B$. For a fixed pair a,b,

$$
U(h)_a-U(h)_b=r_a-r_b+(p_a-p_b)\cdot h.
$$

Its maximum sets $h_j=M$ where $p_{aj}>p_{bj}$ and $h_j=0$ where the inequality
is reversed. Since the row difference sums to zero, its positive mass is its
total variation. Thus the maximum is the bracketed quantity. Oscillation is the
maximum of these differences over finitely many pairs; maximizing over h and
this finite pair set can be interchanged. The maximizing pair and its endpoint
assignment attain the result. The cases $M=0$ and a singleton input also follow;
including a=b ensures the answer is nonnegative.

Consequently the earlier sufficient allowance
$\operatorname{osc}(r)+M$ can be sharpened to $B_U(M)$. For zero r this is
$M\max_{a,b}\operatorname{TV}(p_a,p_b)$, and for identical rows it is exactly
$\operatorname{osc}(r)$, independent of M. In general the maxima of reward
difference and row variation need not occur at the same pair, so even replacing
M by a largest row-variation coefficient can still be conservative.

This calculation checks closure of a span-bounded continuation family through
one finite affine suffix. It does not assert the same formula for arbitrary
nonlinear min/max transformers; those still have the broader monotonicity/shift
bound or require a separately justified sharper analysis.

### C.2 Worked allowance and a complete cancellation example

Take $r=(0,1)$ and rows $(3/4,1/4)$ and $(1/4,3/4)$. For terminal span two,
$B_U(2)=1+2(1/2)=2$, rather than the generic bound three. Terminal values
$(0,2)$ attain output values $(1/2,5/2)$ and span two. For a prefix whose
approximation guarantee is known only on intermediate span at most two, this
suffix satisfies the premise. A three-unit generic upper bound would fail to
certify that premise but would not show the actual closure false.

There is also a useful case with no finite global terminal-span restriction.
Let one-input prefix steps be $T(h)=r+p\cdot h$ and $S(h)=s+q\cdot h$, and a
shared suffix be $U(h)=t+Qh$. Their composed difference is

$$
(T;U)(h)-(S;U)(h)=r-s+(p-q)\cdot t+(p-q)Qh.
$$

They are uniformly within a fixed one-sided allowance $\epsilon$ over **all**
finite real terminal h precisely when

$$
(p-q)Q=0,
\qquad r-s+(p-q)\cdot t+\epsilon\geq0.
$$

If the coefficient vector is nonzero, choosing h opposite to it with growing
magnitude violates any finite allowance; if it is zero only the constant remains.
For example, different deterministic prefixes select L and R, but a zero-reward
suffix has the same row $(1/3,2/3)$ from both. The composed maps agree on every
h although the prefixes do not agree on arbitrary intermediate continuations.
A suffix that erases the difference can therefore justify substitution without
bounding absolute value or pretending the two prefixes are universally equal.

**Candidate consequence.** T can make downstream task dependence explicit and
sometimes compress it through a checked map. It does not need every conceivable
continuation at every intermediate interface. These examples do not choose a
universal rule for selecting that test family; they give F03/F04 concrete
assumptions and queries to audit.

## D. P compression depends on which future comparisons remain available

### D.1 All aligned bottleneck tests can recover the original profile

Fix positive weights $p_i$ on a finite supported set, a common payoff unit,
and a supplied range $L\leq x_i\leq U$ with $L<U$. Suppose a summary of x must
answer every aligned query

$$
q_y(x)=\sum_jp_j\min(x_j,y_j),\qquad y\in[L,U]^n.
$$

For each i choose the known comparison profile $y^{(i)}$ with coordinate i
set to U and every other coordinate set to L. Then

$$
q_{y^{(i)}}(x)=p_i x_i+(1-p_i)L,
\qquad
x_i=\frac{q_{y^{(i)}}(x)-(1-p_i)L}{p_i}.
$$

Thus two different supported profiles cannot have the same exact answers to
all these queries. A summary sufficient for this *whole aligned comparison
family* must distinguish those profiles. This is not a lower bound of n real
storage slots: a nonstandard lossless scalar encoding remains possible, and
zero-weight coordinates remain invisible to these tests.

The range premise is supplied, not discovered by the summary. Nor does this
make bounded values a foundation: an arbitrary finite range can be chosen for
a particular finite example, with no common range over all uses.

For an approximate decoder giving absolute error at most $\epsilon$ on every
query, a shared summary for x and x' requires

$$
p_i|x_i-x_i'|\leq2\epsilon\quad\hbox{for each supported i}.
$$

The triangle inequality proves this necessary condition from the same decoder
answer to $y^{(i)}$. It is not sufficient for the whole query family; errors
at several coordinates can combine. Rare coordinates may be less important
for these weighted tolerances without being negligible for a later subdomain
or different weighting request.

### D.2 Means are nevertheless sufficient for a different closed fragment

For fixed p, all expressions formed from x by scalar addition of known constants,
known scaling, and summing separately supplied profiles under the same linear
evaluation can be evaluated from the corresponding means. The finite-sum
identity proves that preservation without needing a joint law. Replacing the
allowed operations by aligned bottlenecks changes the query family and the
information requirement; it does not refute the additive fragment.

This is why the candidate table distinguishes retained information from admitted
operators. A richer P object need not be used everywhere. S may be an adequate
projection for one consumer, while a caller intending later aligned comparisons
must retain the extra distinctions or accept a proven loss allowance.

## E. Two tempting G extensions need different meanings

### E.1 Separate requirement intersection does not distribute through composition

Let the known deterministic menus be

$$
A=\{(0,2)\},\quad B=\{(2,0)\},\quad C=\{(0,2),(2,0)\}.
$$

Using G's own upper-set operations,

$$
(\Gamma_A\cap\Gamma_B)\otimes\Gamma_C
=\Gamma_{\{(2,4),(4,2)\}},
$$

but

$$
(\Gamma_A\otimes\Gamma_C)\cap(\Gamma_B\otimes\Gamma_C)
=\Gamma_{\{(2,2)\}}.
$$

The latter contains budget $(2,2)$ and the former does not. On the latter side,
the witness from C is $(2,0)$ for the A composite and $(0,2)$ for the B composite.
Intersecting before adding one C option instead requires a common adequate
residual budget for A and B. The different witnesses explain the strict gap.

There is a valid inclusion from left to right: if a budget is obtained from a
common residual adequate for A and B plus one C choice, that same choice works
for both separate composites. Equality is the unjustified strengthening. G's
independent addition does distribute over menu union, as S1 showed; intersection
is a different operation with different quantifiers, not another spelling of
choice or a cost-free logical conjunction.

### E.2 Bounded values do not ensure an attainable optimum

Basic G uses finite menus. Extending its pruning rule to arbitrary infinite
menus is not automatic. Consider

$$
A_\infty=\{(1/n,0):n=1,2,\ldots\}.
$$

Its attainable budget set is exactly

$$
\Gamma_{A_\infty}=\{(b_1,b_2):b_1>0,\ b_2\geq0\}.
$$

Every menu vector is dominated by another, so retaining only *attained minimal
vectors* produces an empty representation and loses all these capabilities.
Taking the closure instead adds the unattainable budget $(0,0)$. All the given
cost vectors lie in a bounded box: the problem is the infinite menu and lack of
attainment, not unbounded value magnitudes.

At every positive tolerance an appropriate finite n supplies a witness. At zero,
none does. A lottery over these positive costs also has strictly positive
expectation: at least one positive-probability term makes its nonnegative sum
positive. Thus changing deterministic choice to a lottery does not attain zero.

T has a parallel extension boundary. The finite maps $T_n(h)=h-1/n$ have pointwise
supremum $h$, the same numerical response as an actually available zero-cost
step. But if only the $T_n$ are legal, no member attains that supremum. Replacing
finite controlled maximum by arbitrary supremum can preserve the best limiting
value while losing an exact implementation. A witness-sensitive or approximate
attainability contract must say which question it answers.

These counterexamples do not invalidate the finite candidates. They show why
unbounded scalar carriers, infinite menus, completion by limits, and bounded
encodings are separate design choices, each with its own closure obligations.

## F. Shared-model sequencing: when early reduction is actually exact

### F.1 Conditional finite model, not an inference from observed frequencies

Fix one current input a, a finite nonempty hidden-model family $\Theta$, a finite
intermediate interface B, and a terminal continuation h. In model $\theta$, the
first step has reward $r_\theta$ and stochastic row $p_\theta$; the suffix has
value vector $s_\theta(h)$. The *same* hidden model applies to both steps. No
control choice in this example may inspect that hidden model.

The correctly coupled lower value is

$$
R(h)=\min_\theta\left[r_\theta+\sum_b p_\theta(b)s_\theta(h)_b\right].
$$

Reducing the suffix statewise first gives $k_b=\min_\phi s_\phi(h)_b$ and the
composed stagewise lower value

$$
L(h)=\min_\theta\left[r_\theta+\sum_b p_\theta(b)k_b\right].
$$

For every theta, replacing its suffix by k can only lower its value because
$p_\theta$ is nonnegative. Therefore $L(h)\leq R(h)$. The reduced expression
is conservative under these exact premises, not necessarily equal.

### F.2 An exact equality test, including unreachable states

Define

$$
c_\theta=r_\theta+p_\theta\cdot k,
\qquad
g_\theta=\sum_b p_\theta(b)[s_\theta(h)_b-k_b]\geq0.
$$

Then $L=\min c_\theta$ and $R=\min(c_\theta+g_\theta)$. Because Theta is finite,

$$
L=R
\quad\Longleftrightarrow\quad
\exists\theta:\ c_\theta=L\ \hbox{and}\ g_\theta=0.
$$

For sufficiency, that theta gives $R\leq L$ while the prior inequality gives
$R\geq L$. For necessity, take a theta attaining R. Both $c_\theta\geq L$ and
$g_\theta\geq0$; their sum can equal L only when both equalities hold. Finally,
$g_\theta=0$ holds exactly when the same theta attains the suffix minimum at
every b with $p_\theta(b)>0$. States that this prefix never reaches impose no
extra equality condition.

Thus "all stages must have one globally minimizing model at every state" is
unnecessarily strong. What matters for this query is a compatible minimizing
prefix and suffix choices on its positive-weight reachable states. The criterion
is h-dependent and must not be promoted to equality for all continuations without
checking that stronger quantifier.

### F.3 Worked strict gap and worked exact case

With a singleton intermediate state, rewards $r_0=0,r_1=1$ and suffix values
$s_0=1,s_1=0$ give $k=0$, $c=(0,1)$, $g=(1,0)$. Hence $L=0$ and $R=1$.
There is no theta simultaneously attaining the minimum c and zero gap. This
reconstructs S1's anti-correlated-reward witness.

For a two-state exact case, let

$$
p_0=(1,0),\ r_0=0,\ s_0=(0,100),
\qquad
p_1=(0,1),\ r_1=10,\ s_1=(100,0).
$$

Then $k=(0,0)$ and $c=(0,10)$. Model zero attains the prefix minimum and its
own suffix is minimal on its sole reachable state, giving $g_0=0$ and $L=R=0$.
Its suffix is not minimal on the other state, which is irrelevant to this
particular prefix and query. A test demanding agreement at every intermediate
state would reject an exact case for the wrong reason.

### F.4 Forgetting two different relations has opposite consequences

The modeling roles of nondeterminism cannot be inferred from the shape of a
set alone. With a fixed payoff function:

* Enlarging an *uncontrolled model set* lowers its infimum, so a lower guarantee
  remains conservative but may cease to be sharp.
* Enlarging a *controlled legal-plan set* raises its supremum, so claiming the
  new value achievable can become optimistic and false for the original plans.

For costs the inequality direction reverses with the smaller-is-better convention,
but the operational distinction survives. G's incompatible-prefix/suffix example
wrongly enlarges a controlled menu and predicts an unavailable cheap plan. T's
stagewise lower reduction enlarges the adversary's allowed switching and can
understate the correct robust value. Neither failure is repaired merely by
keeping a sign or changing a scalar to a set: the set's role and its permitted
coupling have to be specified.

These are monotonicity comparisons between explicitly nested sets. Arbitrary
model misspecification is not guaranteed conservative, and an optimistic and a
pessimistic mistake need not cancel in a justified way.

## G. A constructive connection between G and T, not a fifth chosen core

### G.1 Backward propagation can carry budgets instead of real scores

Use G's finite typed controlled relation $R\subset X\times\mathbb R^d\times Y$.
An edge $(x,c,y)$ is a legally selectable step of cost c ending at the observable
interface y. All required shared compatibility information is included in that
interface or in the admissible edge relation, as in S1. Costs add in fixed
component units. A downstream capability map assigns an upward-closed finite-
generated budget set $B(y)$ to each y. Define

$$
(W_R B)(x)=\bigcup_{(x,c,y)\in R}\big(c+B(y)\big).
$$

The meaning is direct: a total budget b works exactly when a permitted prefix
edge is selected and the remaining vector $b-c$ lies in the downstream set at
its endpoint. An empty edge set or empty downstream set supplies no witness.
This expression is a set-valued continuation map, but it is a presentation of
G's declared controlled relation, not a claim that G was secretly the scalar T
carrier all along.

For compatible finite relations R and S, and any such terminal map B,

$$
W_{R;S}(B)=W_R(W_S(B)).
$$

**Proof.** Membership on either side supplies exactly an edge $(x,c,y)$ in R,
an edge $(y,d,z)$ in S, and a terminal budget $v\in B(z)$ such that
$b=c+d+v$. The same witnesses give both directions. Additive associativity and
matching intermediate endpoints are doing the work; erasing the endpoint before
composition would invalidate the witness correspondence. Pointwise union of
capability maps is also preserved because unions distribute over this finite
edge union and translation by c. No uncontrolled outcome is reclassified as
an agent's choice.

### G.2 Fixed scalarization commutes with the admitted composition

Fix nonnegative w in normalized cost coordinates. For a nonempty finite-front
capability set B(y), let

$$
\alpha_w B(y)=\min_{b\in B(y)}w\cdot b.
$$

The minimum is attained at a generating vector, though zero weights can make
other minimizers possible. For empty B(y), use $+\infty$ only as an explicit
infeasibility sentinel in this *cost* presentation, not as a finite member of
S or the original total finite-real T carrier. Then

$$
\alpha_w(W_RB)(x)
=\min_{(x,c,y)\in R}\big[w\cdot c+\alpha_wB(y)\big].
$$

For a nonempty union the minimizing edge and its generating suffix vector
attain the right side; shifting a budget adds exactly $w\cdot c$. Empty cases
have no feasible witness and both sides have the declared sentinel. This is the
deterministic min-cost counterpart of an affine/min T expression. It shows an
exact fixed-task projection for choice and compatible additive sequencing.
It does not preserve all nonlinear hard-cap tests, as section A demonstrates.

**Worked endpoint check.** A prefix reaches L at cost $(0,0)$ or R at $(1,0)$.
The suffix from L costs $(100,0)$ and from R $(0,0)$. The propagated total budget
set is generated by $(100,0)$ and $(1,0)$, hence by $(1,0)$ alone. For weight
$(1,0)$ the scalarized recurrence gives $\min\{0+100,1+0\}=1$, agreeing exactly.
Erasing endpoints from the two separate menus first would permit the invalid
zero-cost pairing. The proof therefore demonstrates a useful compressed query
only after compatibility has been retained through composition.

### G.3 Scalar T can also answer a hard-budget query with richer terminal states

For a finite deterministic cost menu A, take the distinct cost vectors themselves
as output-interface labels and allow a branch that reaches each available vector.
Use zero immediate reward and terminal *test* function

$$
h_b(c)=\mathbf1\{c\leq b\}.
$$

The optimized T response is one exactly when some menu vector meets the budget:

$$
\max_{c\in A}h_b(c)=1
\quad\Longleftrightarrow\quad b\in\Gamma_A.
$$

This is a supplied finite indicator test about an operational requirement, not
metaphysical truth as a new primitive. It explicitly retains the cost-vector
output and admits a nonlinear terminal query. In the menus of section A.2,
$h_{(3/2,3/2)}$ distinguishes A from B even though all linear weighted cost
queries fail to do so.

There is therefore no established absolute expressive ranking "G beats every T"
or "T already contains every capability for free." G makes this budget structure
and its composition native. T can recover the particular query by enriching its
output interface and test family. Once the cost vector has been projected to a
weighted optimum, however, this terminal predicate cannot be evaluated from that
number alone. A label that retrieves a hidden full cost record also counts as
retained information, not an exception to the separation.

For stochastic outputs, the same indicator expectation concerns the probability
of meeting the joint budget, not componentwise expected costs. The deterministic
embedding must not be reused under that different interpretation without saying
so. Cost accumulation over unbounded horizons can also require larger state
interfaces; this finite example establishes no efficiency theorem.


### G.4 A smaller fixed-task representation can be exact for all later scalar continuations

For one fixed nonnegative cost tradeoff w, define a kernel indexed by the exact
input and output endpoints:

$$
K^w_{xy}=\min_{(x,c,y)\in R}w\cdot c.
$$

An absent edge is kept as a separate unavailable entry (or an explicitly
extended-cost positive-infinity sentinel). For a scalar downstream cost h,

$$
C_R^w(h)_x=\min_y\{K^w_{xy}+h_y\}.
$$

This is exact because h depends only on the retained output endpoint. Within
one x,y fiber, choosing a nonminimal weighted immediate cost cannot improve the
sum. Matching-endpoint composition therefore gives the finite kernel law

$$
K^{w,R;S}_{xz}=\min_y\{K^{w,R}_{xy}+K^{w,S}_{yz}\}.
$$

The two sides minimize the same finite family of compatible pairs. Thus a
fixed scalar task can support all its admitted downstream continuations and
finite sequences using a small endpoint-indexed kernel, rather than retaining
every multiobjective path front. With payoff sign reversed,
$h\mapsto-C_R^w(-h)$ is a max of deterministic affine T primitives.

This useful compression retains endpoints and the fixed weight. It does not
license forgetting endpoints, changing the weight without new information,
or deciding arbitrary hard vector caps from the kernel alone. Even storing
such kernels for *every* w recovers only the convex upper hull in each endpoint
fiber, not necessarily its deterministic front, by section A. Two edges with
the same endpoint but costs (0,2) and (2,0), versus those plus (3/2,3/2), give the
same kernels for every w yet differ on the hard budget. Conversely, storing each
individual action's value at every coordinate weight, with its identity, would
retain its vector and escape that particular compression restriction.

The composition argument assumes compatibility is determined by the represented
endpoints and that the stated scalar costs add. Hidden shared-policy constraints
or unrepresented state invalidate that premise. All sequences here are finite;
negative edge costs do not silently authorize an unrestricted repeat/loop
operator or a claim of a finite optimal value for an infinite-horizon problem.

## H. What this reconstruction changes in the comparison

The four candidate carriers remain as in S1. The continuation has not added a
new mandatory mathematical primitive. It supplies more exact comparison tests:

| query being retained | sufficient object in the stated fragment | information not supplied by that fact |
|---|---|---|
| one fixed additive score | S, with task/units and the stated linear law | arbitrary future aligned bottleneck queries or hard budgets |
| every nonnegative optimal scalar tradeoff | convex upper hull of a finite cost menu | nonconvex deterministic budget attainability |
| finite aligned bottleneck queries with all range masks admitted | information distinguishing all supported profile coordinates | a lower bound on the number of real storage slots or acquisition cost |
| sequential task comparison after an affine suffix | T response on the suffix's image; exact span bound or cancellation criterion | universal interchangeability before every possible suffix |
| observed-input controlled choice | pointwise optimized T map | one globally shared blind branch and its row coupling |
| one fixed action satisfying every model/coordinate cap | robust coordinate vector used by G | later robust expected costs of a lottery over actions |
| compatible additive budget sequencing | G relation or its budget-continuation presentation | independent reuse of incompatible local witnesses |
| optimum over an infinite menu | limiting numerical value, when it exists | an attaining plan or exact zero-tolerance feasibility |

For each use, retained structure can be reduced when its future consumers are
restricted appropriately. Every such reduction has a precise boundary above.
A proposed implementation that returns answers to more questions must expose
its additional data, operations, or approximations rather than claim those
answers come from an identical smaller semantic object.

**F03/F04 handoff, not gate decisions.** The finite scalar and aligned-profile
fragments remain useful controls. The candidate questions needing the most
external audit and hostile testing are T's observed-state/continuation contract
and G's witness-preserving resource composition. The limited source comparison
should check existing expectation-transformer, ordered-set/constraint, and
abstraction results with their actual assumptions. No candidate is permanently
selected by this note and no novelty has been established.

## I. The exact finite transformer class, and two useful boundaries

This section tests what candidate T actually contains. It does not turn that
candidate into the phase's selected calculus. In particular, its generator
library below is allowed to contain **arbitrary** finite stochastic affine
primitives, not just the models that happen to be operationally available.

### I.1 Three properties characterize the extensional class

Let the input and output interfaces be finite and nonempty. Consider maps
$F:\mathbb R^B\to\mathbb R^A$ generated from primitives

$$
h\longmapsto r+Ph,
\qquad P_{ab}\geq0,\qquad\sum_bP_{ab}=1,
$$

using finitely many pointwise minima, maxima, and well-typed compositions.
These are precisely the maps with all three properties:

1. global continuity and a finite piecewise-affine presentation;
2. coordinatewise monotonicity;
3. common-shift equivariance $F(h+c\mathbf1)=F(h)+c\mathbf1$ for every real $c$.

Here "piecewise affine" means that a finite polyhedral cover of the whole
finite-dimensional input space supports affine formulas agreeing on overlaps.
The result concerns equality of maps on all inputs, not equality of process
implementations, computational costs, or permissible observation schedules.

**Forward argument.** A stochastic affine primitive has the three properties.
Minimum and maximum preserve monotonicity and shift equivariance, and a finite
hyperplane refinement gives their finite continuous piecewise-affine form.
Composition preserves the two order/shift properties. For the affine property,
intersect a cell of the inner map with inverse images, under its affine formula,
of the finitely many cells of the outer map. These are polyhedra; on each one the
composite is affine. Continuity is preserved as well.

**Converse, slopes first.** Work with one output coordinate $f$. On the interior
of any full-dimensional affine cell write $f(h)=r+p\cdot h$. Small positive
coordinate perturbations stay in that cell, so monotonicity implies $p_b\geq0$
for every coordinate. Small common shifts stay there too, so shift equivariance
implies $\sum_b p_b=1$. By continuity, affine pieces that occur only on a
lower-dimensional boundary are unnecessary: neighboring full-dimensional
pieces already determine those values. Every needed piece is therefore an
allowed stochastic affine primitive.

**Converse, reconstructing from the pieces.** A continuous finite piecewise-
affine scalar function on a convex domain is a finite maximum of finite minima
of its affine pieces. This is an existing lattice-representation result, not a
novelty claim: see Ovchinnikov, *Max-Min Representation of Piecewise Linear
Functions*, Theorem 4.1, with affine components as defined in Section 2. The
following segment argument reconstructs the needed whole-space case explicitly.

Remove duplicate affine functions and partition the space by all nontrivial
hyperplanes on which two pieces agree. On each full-dimensional open region
$R$, the pieces have a fixed strict ordering. Continuity implies that $f$ uses
one fixed piece there: a switch would require equality of the two pieces.
Choose $y_R\in R$, and put

$$
S_R=\{j:\ell_j(y_R)\geq f(y_R)\},
\qquad m_R(h)=\min_{j\in S_R}\ell_j(h).
$$

The active piece belongs to $S_R$, so $m_R=f$ throughout $R$. We claim $m_R\leq f$
everywhere. Otherwise follow the segment from $y_R$ to a point of strict
violation. The difference $m_R-f$ is zero on an initial segment, continuous,
and piecewise affine. At the beginning $t_*>0$ of a positive interval, choose
a sufficiently short right interval on which $m_R=\ell_j$ and $f=\ell_k$.
Here $j\in S_R$ and $k\notin S_R$; if $k$ belonged, a minimum could not exceed it.
At $t_*$ their difference is zero. But at $y_R$ it is strictly positive because
$\ell_j(y_R)\geq f(y_R)>\ell_k(y_R)$. An affine function of segment parameter
that is positive at zero and zero at $t_*>0$ is negative immediately after
$t_*$. This contradicts the positive interval. Thus the claim holds.

It follows that $\max_R m_R\leq f$ everywhere, with equality on every open
region. Those regions are dense, and both sides are continuous, so equality
holds on their boundaries as well. There are only finitely many regions and
pieces, giving the required finite maximum-of-minima expression.

Apply this separately to every output coordinate. Different clause lengths and
numbers of clauses can be padded by repeating clauses or terms, which does not
change minima or maxima. Assemble the selected affine pieces row by row into
stochastic matrices. A common finite vector expression then yields $F$.

**What follows, and what does not.** Composition does not enlarge this
*extensional* class beyond finite min/max expressions of stochastic affine maps.
It can still be a much more compact or operationally meaningful presentation.
The normal-form proof does not preserve an externally restricted generator
library, policy witnesses, inspection costs, or when intermediate state is
observed. In particular, it does not repair the blind-choice information loss
from section B. Its pointwise choices are allowed to depend on the input state,
exactly as candidate T's original carrier stipulated.

The proof also assumes the whole real input space. Merely checking monotonicity
and shifts on a finite test set or a restricted continuation family does not
license conclusions about all local slopes on the whole space. The later
literature audit should check both this finite characterization and which
operational interpretations warrant its hypotheses.

### I.2 An explicit map that is neither convex nor concave

Set $d=h_1-h_2$, and define $F(h)=h_2+g(d)$, where

$$
g(d)=
\begin{cases}
d/4,&d\leq0,\\
3d/4,&0\leq d\leq1,\\
d/4+1/2,&1\leq d\leq2,\\
d/2,&d\geq2.
\end{cases}
$$

The breakpoints agree. Each segment has slope between zero and one, so the
corresponding two-coordinate affine slopes are nonnegative and sum to one.
The function is therefore monotone and common-shift equivariant. Its four
stochastic affine pieces are

$$
\ell_0=\tfrac14h_1+\tfrac34h_2,\quad
\ell_1=\tfrac34h_1+\tfrac14h_2,\quad
\ell_2=\tfrac14h_1+\tfrac34h_2+\tfrac12,\quad
\ell_3=\tfrac12h_1+\tfrac12h_2.
$$

A directly checkable normal form is

$$
F(h)=\max\{\ell_0(h),\min(\ell_1(h),\ell_2(h)),
                         \min(\ell_1(h),\ell_3(h))\}.
$$

For $d<0$ the first term wins; for $0<d<1$ the second gives $\ell_1$;
for $1<d<2$ it gives $\ell_2$; for $d>2$ the third gives $\ell_3$.
Boundary equality follows by continuity. This verifies the displayed
representation independently of the general proof.

Neither a convex nor a concave restriction describes all of T. On the slice
$h_2=0$, concavity fails because $g(0)=0$ is smaller than
$[g(-1)+g(1)]/2=1/4$. Convexity fails because $g(1)=3/4$ is larger than
$[g(1/2)+g(3/2)]/2=5/8$. Both failures arise within a four-piece valid map.
Positive homogeneity is also not required; the immediate-reward offsets are
real data rather than universally zero.

### I.3 Nonexpansiveness is a real modeling restriction

Monotonicity and common-shift equivariance imply

$$
\|F(h)-F(k)\|_\infty\leq\|h-k\|_\infty.
$$

Indeed, if the right side is $\delta$, then $k-\delta\mathbf1\leq h\leq
k+\delta\mathbf1$. Apply the two properties and obtain the coordinatewise
output sandwich. This needs no piecewise-affine assumption.

Consequently, the one-dimensional duplicator $D(h)=2h$ is not a map of the
present T carrier. Nor can any such map approximate it with a finite uniform
absolute error on the whole real line: shift equivariance forces
$F(h)=F(0)+h$, so $|F(h)-2h|=|F(0)-h|$ is unbounded. Similarly, pointwise
addition of two nonempty T maps has shift response $2c$, not $c$, and is not
generally a T operation.

This does not mean that duplication of payoffs is illegitimate. It means this
candidate encodes one unit of terminal payoff mass through stochastic rows.
A model that consumes two terminal payoffs, permits subprobability termination,
or amplifies a numerical measurement needs an appropriate different interface
or a documented extension. For example, a joint output state can be tested by
$h'(b_1,b_2)=h(b_1)+h(b_2)$, but constructing that terminal test is additional
structure, not ordinary one-slot T addition. The earlier physical error
amplification example is likewise not a claim that raw measurements themselves
are continuation payoffs. This limitation should be compared against intended
operations rather than hidden by a convenient reinterpretation.

### I.4 A smooth map is outside the exact carrier, but can have a global finite approximation

For an explicit contrast, consider the entirely stipulated two-coordinate map

$$
F_*(h_1,h_2)=\log\frac{e^{h_1}+e^{h_2}}2
           =h_2+g_*(h_1-h_2),
\qquad g_*(d)=\log\frac{1+e^d}2.
$$

It is monotone and common-shift equivariant. On every interval,
$g_*''(d)=e^d/(1+e^d)^2$ is strictly positive. It cannot have a finite affine
presentation on the line, and hence is not an exact finite T map. This is not
an assertion that this smooth aggregation ought to be an operation of Value
Logic; it tests the boundary of the three-property characterization.

Nevertheless, finite T approximations need not require a cap on absolute
values, or even on the difference between these two inputs. Let

$$
\sigma(t)=\frac{e^t}{1+e^t},\qquad
L_t(d)=g_*(t)+\sigma(t)(d-t).
$$

Convexity makes each tangent $L_t$ a lower bound. Its slope is in $(0,1)$,
so $h_2+L_t(h_1-h_2)$ is an allowed stochastic affine primitive. The asymptotic
lines $-\log2$ and $d-\log2$ are also lower bounds and correspond to slopes
zero and one. For a finite grid on $[-R,R]$ with maximum spacing $\Delta$,
include its tangents and both asymptotic lines, and take their maximum
$\widehat g$. Because $0<g_*''\leq1/4$, a tangent at distance at most
$\Delta/2$ has gap at most $\Delta^2/32$. Outside the grid range the appropriate
asymptotic line has gap

$$
\log(1+e^{-|d|})\leq e^{-|d|}\leq e^{-R}.
$$

Thus the finite T map $\widehat F(h)=h_2+\widehat g(h_1-h_2)$ satisfies on the
entire, unbounded input space

$$
0\leq F_*(h)-\widehat F(h)
\leq\max\{\Delta^2/32,e^{-R}\}.
$$

For a concrete instance, use tangents at the nine integers from -4 through 4
plus the two asymptotes: **eleven affine primitives**. Here $\Delta=1$ and
$e^{-4}<1/32$, since the first five nonnegative terms of the exponential series
give $e^4>1+4+8+64/6+256/24=103/3>32$. The global error is therefore at most
$1/32$. Arbitrary precision follows by increasing R and refining the grid.

This is a proved approximation for this displayed function, not a universal
approximation result for every monotone shift-equivariant map. It uses exact
real coefficients. Numerical evaluation of exponentials and logarithms provides
only a development check; a finite-precision implementation requires a separate
coefficient/error argument before inheriting the unrestricted bound. Exact
representability, useful approximation, and implementation accuracy must remain
different entries in the candidate comparison.


### I.5 Rational coefficients can give a certified global approximation too

The preceding coefficient qualification has a constructive repair. Use the
65 rational slopes $p=k/64$, k=0,...,64, and write

$$
b(p)=-\log2-p\log p-(1-p)\log(1-p),
$$

with $0\log0=0$. The affine function $pd+b(p)$ lies below $g_*(d)$. To check this
without treating a softmax identity as an unexplained oracle, set
$q=e^d/(1+e^d)$. Direct substitution gives the gap

$$
p\log\frac pq+(1-p)\log\frac{1-p}{1-q}.
$$

The scalar inequality $-\log t\geq1-t$, applied to the two terms, proves this
quantity nonnegative. Applying $\log t\leq t-1$ instead gives its upper bound
$(p-q)^2/[q(1-q)]$. Endpoint p values follow by continuity.

On $|d|\leq4$, the inverse denominator is
$e^d+2+e^{-d}<84$: $e<3$ follows by bounding the factorial-series tail with a
geometric series, and thus $e^4<81$. A nearest grid p is within $1/128$ of q,
so one of these exact-slope lines has gap at most $84/128^2=21/4096$ there.
Outside this range the endpoint slopes give the prior gap less than $1/32$.

It remains to bound intercepts using rational arithmetic. For a rational
$x\in[1/64,1]$, write $x=2^m u$ with integer $-6\leq m\leq0$ and
$1\leq u<2$. For $t=(u-1)/(u+1)\in[0,1/3]$, integration of the finite geometric
series gives

$$
\log u=2\sum_{j=0}^{N-1}\frac{t^{2j+1}}{2j+1}+R_N,
\qquad
0\leq R_N\leq\frac{2t^{2N+1}}{(2N+1)(1-t^2)}.
$$

The same formula with t=1/3 bounds log 2. For N=3 its remainder is at most
$1/6804$. Multiplying the log-2 interval by the possibly negative m with the
correct endpoint reversal and adding the log-u interval gives rational bounds
on log x of width at most $7/6804$. Combining these bounds with the negative
coefficients in b(p) gives rational $b^-(p)\leq b(p)$ with
$b(p)-b^-(p)\leq8/6804=2/1701$. At p=0 or 1 only the log-2 interval is needed.
No rounding of a nonrational **slope** is involved.

The resulting explicit rational finite T map is

$$
\widehat F_{\rm rat}(h)
=\max_{k=0,\ldots,64}\left\{
\frac{k}{64}h_1+\left(1-\frac{k}{64}\right)h_2+b^-(k/64)\right\}.
$$

Every primitive has nonnegative rational coefficients summing exactly to one.
The preceding lower-bound and coverage arguments give, on the entire unbounded
real input space,

$$
0\leq F_*(h)-\widehat F_{\rm rat}(h)
\leq\frac1{32}+\frac2{1701}<\frac1{16}.
$$

This supplies a finite exact-arithmetic implementation contract for this
specific smooth target, rather than merely asserting that irrational tangent
coefficients can be rounded harmlessly at unbounded stakes. It is not claimed
minimal in number of primitives. Rational-input evaluation can be performed
with exact fractions; floating-point evaluation would require its own arithmetic
error allowance. The general uniform statement follows from the displayed
bounds, not from a finite numerical grid or a claim of a new approximation
theory.

## J. Tolerated substitution for guarantee fronts

Candidate G need not demand exact resource vectors to support useful inference.
This section supplies a tolerance comparison specific to its admitted finite,
freely composable budget fragment. It is not a universal metric on value.

### J.1 A directed, unit-aware slack

Let A and B be finite nonempty menus in $\mathbb R^d$, and fix a positive vector
$s$ of component scales. Each $s_i$ has the unit of cost component i, so the
following comparison is dimensionless:

$$
d_s(A,B)=\max_{a\in A}\min_{b\in B}
              \max_i\left(\frac{b_i-a_i}{s_i}\right)_+.
$$

This asks how much extra budget is sufficient to replace every use from A by
some use from B. It is directed: making B better can make the distance zero
without making A and B equal. The finite extrema are attained; this is not an
unjustified use of an infimum as an available witness.

For every $\varepsilon\geq0$, the following statements are equivalent:

$$
\begin{aligned}
d_s(A,B)\leq\varepsilon
&\quad\Longleftrightarrow\quad
\forall a\in A\ \exists b\in B:\ b\leq a+\varepsilon s\\
&\quad\Longleftrightarrow\quad
\Gamma_A+\varepsilon s\subseteq\Gamma_B.
\end{aligned}
$$

The first equivalence follows coordinate by coordinate from the positive part.
For the second, if $u\in\Gamma_A$, choose $a\leq u$ and its matching b; then
$b\leq u+\varepsilon s$. Conversely, apply the set inclusion to each budget
$a\in\Gamma_A$ itself. Thus this slack has an exact budget-query interpretation:
every A-feasible budget becomes B-feasible after the specified relaxation.

At zero, the comparison is precisely capability inclusion, not an assertion
that the implementation witnesses are identical. Removing dominated vectors
from either finite menu leaves this quantity unchanged, by the equivalent
upward-set formulation. A positive diagonal unit change applied to both costs
and scales also leaves it unchanged. Arbitrary scalarization of cost coordinates
does not have that property.

For empty menus the underlying inclusion still has a meaning: replacing an
empty source asks for nothing, while no finite slack creates an available use
from an empty target and nonempty source. One may encode those exceptional
comparisons as zero and positive infinity respectively, but the availability
states remain explicit. No infinite scalar is required as a basic value object.

### J.2 Composition laws, with their real operational hypotheses

If $d_s(A,B)\leq\varepsilon$ and $d_s(B,C)\leq\delta$, matching each a first
to b and then to c gives $c\leq a+(\varepsilon+\delta)s$. Therefore

$$
d_s(A,C)\leq d_s(A,B)+d_s(B,C).
$$

Similarly, let A',B' be two additional finite nonempty menus. Write plus for
freely composable additive costs, union for controlled alternative availability,
and $A\mathbin{\vee_c}A'=\{\max(a,a'):a\in A,a'\in A'\}$ for the generators
of the intersection of their budget sets. The same elementary witness matching
gives

$$
\begin{aligned}
d_s(A+A',B+B')&\leq d_s(A,B)+d_s(A',B'),\\
d_s(A\cup A',B\cup B')&\leq\max\{d_s(A,B),d_s(A',B')\},\\
d_s(A\mathbin{\vee_c}A',B\mathbin{\vee_c}B')
&\leq\max\{d_s(A,B),d_s(A',B')\}.
\end{aligned}
$$

For the last inequality use
$\max(b,b')\leq\max(a+\varepsilon s,a'+\delta s)
\leq\max(a,a')+\max(\varepsilon,\delta)s$.
It concerns separate witnesses for the two menu requirements, as in G's original
intersection definition. It does not assert existence of one shared policy.

Likewise, the sum inequality requires freely compatible pairs. If a zero-cost
prefix reaching state u is replaced by a zero-cost prefix reaching state v,
their endpoint-erased fronts have zero slack. A suffix costing zero from u and
M from v produces composite slack M. Nothing in the cost-only comparison ruled
that out. A sufficient typed repair requires the matching edge to have the same
input and output interfaces/endpoints; the cost inequality can then be added
to a compatible suffix. More permissive endpoint simulations require a separate
declared relation and proof, not an assumption that all low-cost uses compose.

### J.3 Why scalar optimum agreement does not control this tolerance

Return to $A=\{(0,2),(2,0)\}$ and
$B=A\cup\{(3/2,3/2)\}$, with $s=(1,1)$. Their nonnegative weighted optima agree
for every weight, but

$$
d_s(A,B)=0,\qquad d_s(B,A)=1/2.
$$

The two original vectors match exactly. The extra B vector can match either
A extreme only by increasing one component from $3/2$ to two. Consequently a
budget relaxation smaller than $1/2$ cannot transfer that particular feasible
request to A. Multiplying all menu costs by a positive M while holding the
request's scales fixed makes the latter slack $M/2$, although the two scalar
optimum functions still agree exactly. This is not merely a difference in exact
zero-tolerance answers: a proposed inference from those scalar optima alone
cannot supply any universal finite hard-budget slack on this scaled class.

The positive implication goes the other way. If $d_s(A,B)\leq\varepsilon$, then
for any nonnegative weight w,

$$
\min_{b\in B}w\cdot b
\leq\min_{a\in A}w\cdot a+\varepsilon\,w\cdot s.
$$

Choose an A optimizer and its matching B witness, then multiply the component
inequalities by the nonnegative weights. Weighted scores can therefore inherit
a stated guarantee-front approximation, but equality of all weighted optima
need not recover that approximation under the deterministic budget contract.
Expected-budget lotteries replace the relevant fronts by convex upper hulls,
as in section A; that change of query is substantive.

This gives F02 a second concrete answer to F01's tolerance-relative question.
T can restrict its downstream test family and propagate scalar payoff error;
G can propagate component budget slack without first selecting a tradeoff.
Neither is a general solution to evidence acquisition, incompatible sequencing,
or hidden policy coupling. Their operations and guarantees remain different
objects to compare in the next research tasks.

### J.4 A constructive finite compression that retains hard-budget meaning

The negative scalarization result need not force an implementation to retain
arbitrarily fine distinctions in a finite front. Fix a positive slack quantum
$\varepsilon$ and component scales s as above. For a nonempty finite menu set
$\alpha_i=\min_{a\in A}a_i$, and round each vector upward by

$$
a_i^+=\alpha_i+\varepsilon s_i
       \left\lceil\frac{a_i-\alpha_i}{\varepsilon s_i}\right\rceil.
$$

Then $a\leq a^+\leq a+\varepsilon s$. Retain the rounded vectors with labels
identifying their original uses, and optionally prune dominated rounded vectors.
For the rounded menu $A^+$,

$$
\Gamma_{A^+}\subseteq\Gamma_A,
\qquad
\Gamma_A+\varepsilon s\subseteq\Gamma_{A^+}.
$$

The first inclusion means any budget accepted using a rounded witness is
actually met by its associated original use. The second means every originally
feasible budget is accepted after the specified slack. These follow directly
from the two coordinate inequalities, and survive finite dominated-vector
pruning. This is an approximation of capability with explicit direction and
error, not convexification or an unexplained smooth score.

If $L_i=(\max_a a_i-\min_a a_i)/s_i$, the number of distinct rounded vectors is
at most

$$
\prod_{i=1}^d\left(1+\lceil L_i/\varepsilon\rceil\right).
$$

That is a finite combinatorial representation bound, not a claim of favorable
complexity in large dimension or a bound on bit-level arithmetic. Every finite
input instance has finite spreads $L_i$; no universal upper bound on all possible
value magnitudes has been assumed. The offset $\alpha$ remains stored and
budget queries are interpreted in the original coordinates. It is not a free
change of the zero of physical cost; offsets from successive stages must be
added, not discarded.

Rounding must also respect any retained compatibility type. A cost front for
edges from x to y can be compressed within that interface, but merging distinct
endpoints and retaining only a cheaper rounded vector can still invalidate
sequencing. Similarly, a confidence-free point estimate of cost does not become
a certified upper bound merely because it was rounded upward. The construction
preserves the exact or already-certified interpretation supplied to it.

**Example.** For $A=\{(0,2),(2,0),(3/2,3/2)\}$, $s=(1,1)$, and
$\varepsilon=1$, the rounded middle point is $(2,2)$ and can be pruned. The two
extremes suffice at this coarse slack: the discarded middle use's budget
$(3/2,3/2)$ plus $(1,1)$ is met. At $\varepsilon=1/4$, all three points are
already on the grid, the middle point remains nondominated, and its exact
budget is preserved. The tolerance, rather than a demand to retain every raw
record or to convexify every front, controls this compression choice.


### J.5 Scalar tolerances do recover the relaxed convex-budget comparison

The earlier negative result has a quantitative positive counterpart under the
changed expected-lottery budget contract. Let $C_A=\operatorname{conv}(A)+
\mathbb R_+^d$ and similarly for B. For every $\varepsilon\geq0$,

$$
C_A+\varepsilon s\subseteq C_B
\quad\Longleftrightarrow\quad
f_B(w)\leq f_A(w)+\varepsilon\,w\cdot s
\quad\text{for every }w\geq0.
$$

The forward implication follows by minimizing each linear functional over the
two sets. For the reverse, suppose a point x of the shifted source hull lies
outside $C_B$. The nearest-point argument of A.1 gives a nonnegative nonzero w
with $w\cdot x<f_B(w)$. But $x\in C_A+\varepsilon s$ gives
$f_A(w)+\varepsilon w\cdot s\leq w\cdot x$, contradicting the proposed
inequality. The zero weight adds no restriction. Since s is strictly positive,
every nonzero nonnegative weight can be normalized by $w\cdot s=1$.
Consequently the least permitted convex-budget slack is exactly

$$
\varepsilon_{\rm convex}(A,B)
=\max_{w\geq0,\,w\cdot s=1}[f_B(w)-f_A(w)]_+.
$$

This maximum exists: the normalized weight set is compact and each finite-menu
optimum function is continuous. Equivalently, it is the least slack that lets
each source-menu vector be met by a convex combination of target-menu vectors.
Finite convexity then covers all source mixtures and upward budget slack.

Thus all weighted optimum queries can preserve **approximate**, not just exact,
mean-budget capability after the interpretation has actually been convexified.
For B equal to A shifted by a nonnegative vector e, the expression is
$\max_i e_i/s_i$. For the unsupported-option example of J.3 it is zero in both
directions even though the deterministic reverse slack is one-half. The two
answers are about different feasible uses, not contradictory evaluations.

Checking only coordinate weights does not generally recover the convex answer.
The menus $\{(0,2),(2,0)\}$ and the same menu augmented by $(1,1/2)$ have equal
coordinatewise optimum costs, but their half/half optimum costs are one and
three-quarters. Individual action vectors are determined by their coordinate
values; *menu optima* at those same coordinates are not. The control quantifier
has already merged the identities of the choices attaining each coordinate.

## K. Nonlinear continuation comparisons need more than vertex tests

### K.1 A counterexample using only admissible finite T maps

Affine comparisons on a span-bounded continuation family have the simple
extremal formulas in section C. Extending their vertex test to arbitrary
min/max expressions would be false.

With two terminal coordinates define

$$
T(h)=\max\{h_1,h_2-1/2\},\qquad
U(h)=(h_1+h_2)/2.
$$

Both are legitimate finite T maps. At the four vertices of $[0,1]^2$,
$T-U$ is respectively zero, zero, $1/2$, and zero. A vertex-only test would
therefore report $T\geq U$. But at $(h_1,h_2)=(0,1/2)$,

$$
T(h)=0,\qquad U(h)=1/4.
$$

Indeed, anchor the second coordinate at zero by common-shift invariance and
write $d=h_1-h_2\in[-1,1]$. The difference becomes
$\max\{d,-1/2\}-d/2$, whose minimum is $-1/4$ at the **internal** breakpoint
$d=-1/2$. An affine test would examine only the endpoints; the maximum in T
created a new relevant point. This establishes an exact one-quarter tolerated
comparison, not the false zero-error comparison.

### K.2 Even agreement on every Boolean terminal test is insufficient

Let $U$ be the same average, and define another finite T map

$$
F(h)=\min\left\{U(h),\max\left(
\tfrac14h_1+\tfrac34h_2,
\tfrac34h_1+\tfrac14h_2-\tfrac14\right)\right\}.
$$

The maps F and U agree at every $h\in\{0,1\}^2$. Nevertheless,
$F(1/2,0)=1/8$ while $U(1/2,0)=1/4$. With $h_2=0$, F's slopes on the successive
intervals cut by $d=0,1/2,1$ are $1/2,1/4,3/4,1/2$, all admissible.
The largest gap $U-F$ is $1/8$, at $d=1/2$.

Thus agreement on the Boolean-valued fragment of these terminal queries does
not specify how a nonlinear map treats other stakes. This is about evaluated
indicator queries in a stipulated numerical model, not a claim that Boolean
logic is invalid or that the final calculus must use fuzzy truth degrees.
A positive restricted control is important: for an **affine** primitive,
$T(0)=r$ and $T(e_j)-T(0)$ give every column of P, so those tests really do
identify that smaller carrier. The missing hypothesis is affinity, not an
absence of numerical information in all indicator tests.

### K.3 A finite repair when the affine pieces are explicitly available

For continuous piecewise-affine T and U, and a finite nonempty terminal
interface of size n, the difference $T_a(h)-U_a(h)$ is invariant under common
shifts. The family $\operatorname{osc}(h)\leq M$ can therefore be represented
without losing any comparison by the compact polytope

$$
H_M^0=\{h:h_n=0,\ h_i-h_j\leq M\text{ for every }i,j\}.
$$

In particular, every coordinate lies between -M and M. The pairwise constraints
matter: the whole box $[-M,M]^{n-1}$ would include inadmissible spans when n>2.
For M=0 or n=1 the domain is a singleton.

Refine this polytope by the finitely many boundaries of affine pieces of both
maps. On each resulting closed cell, the difference is affine. Its extremum
occurs at a cell vertex. One elementary justification is to take a minimizer,
which exists by compactness. If it lies on a positive-dimensional minimal face,
move in a direction tangent to that face. Both small signs remain feasible, so
affinity and minimality require zero slope. Move until a further constraint is
met, preserving the value; repeat until reaching a vertex. Apply the argument
to each output coordinate and each cell. The newly introduced vertices, not
just the original domain's vertices, give the exact comparison.

In the two-terminal case this procedure is particularly transparent. Anchor
$h_2=0$, list the crossings of affine pieces that lie in $[-M,M]$, add the two
endpoints, and evaluate the difference at those finitely many points. Between
consecutive crossings its active pieces are fixed, so its difference is affine
and cannot have a stricter extremum in the open interval. Extra crossings of
inactive pieces are harmless; omitted active crossings are not.

For supplied rational affine pieces, the crossings and values can be computed
exactly with rational arithmetic. Higher-dimensional implementations can use
exact rational linear systems and polyhedral feasibility, but this note makes
no efficiency claim: the number of pieces or refinement vertices can be large,
and expanding a compact composed expression can itself be expensive. Arbitrary
unspecified real coefficients do not automatically provide an effective exact
algorithm. Numerical code must state its coefficient and decision-precision
contract.

This gives another practical boundary for comparing S and T. An affine scalar
summary or stochastic primitive can admit very small complete test families;
nonlinear continuation structure can preserve useful additional distinctions
while requiring a richer finite comparison. The initial choice of a carrier
therefore changes both the inferences available and the work needed to justify
them. It does not entitle a test suite to treat a handful of vertices as a proof
of every generated map's comparison.

## L. Bounded encodings, unbounded values, and a positive precision repair

This is a comparison of implementation contracts for the candidate carriers,
not a decision to require bounded or unbounded values. Write
$\phi(x)=x/(1+|x|)$ and apply it coordinatewise, as in F01. Arguments are numerical coordinates in
a declared fixed payoff unit; a change of unit must change the recoding contract
accordingly. Its inverse is
$\phi^{-1}(z)=z/(1-|z|)$ on the **open** interval $(-1,1)$.

### L.1 Even bounded relative stakes can be lost by quantizing absolute codes

Compare $h_C=(C,C+1)$ and $k_C=(C+1,C)$ for $C\geq0$. Both have span one.
The two available actions select the first or second terminal coordinate.
Their correct rankings are opposite, each with payoff gap one. Yet the
corresponding coordinate codes differ only by

$$
\phi(C+1)-\phi(C)=\frac1{(C+1)(C+2)}.
$$

For any fixed positive code-error allowance, choose C large enough that the
half-gap fits inside it. The same reported pair of midpoint codes is then
compatible with both continuations. A deterministic choice based only on that
report incurs regret one in one of the two cases. A randomized choice has worst
expected regret at least one-half; equal mixing attains that bound. Thus a
fixed absolute code precision does not uniformly resolve even a one-unit
relative comparison as the common level grows.

This sharpens, rather than contradicts, T's span-based guarantees. The relevant
relative information exists in the exact values but has been lost by a specific
quantization of their absolute encodings. Reconstructing a centered vector
*after* that lossy observation cannot restore it.

### L.2 Exact recoding does not preserve ordinary numerical smoothness

For the fixed, perfectly nonexpansive transformer
$T(h_1,h_2)=(h_1+h_2)/2$, its exact bounded presentation is

$$
\widetilde T(a,b)
=\phi\left(\frac{\phi^{-1}(a)+\phi^{-1}(b)}2\right),
\qquad (a,b)\in(-1,1)^2.
$$

It preserves the mathematical meaning through conjugation. It need not remain
nonexpansive in ordinary distance between the codes. Encoded inputs for
$(C,-C)$ and $(C+1,-C)$ differ by only $1/[(C+1)(C+2)]$, whereas their encoded
outputs are zero and $1/3$. The ratio grows without bound. A transported metric
would preserve the original estimate; ordinary code distance is a different
quantity.

There is a stronger, precisely scoped obstruction. Every pair of paths
$(\phi(C+k),\phi(-C))$, for any fixed real k, approaches the same closed-box
corner $(1,-1)$ as $C\to\infty$. Its target output is constantly $\phi(k/2)$.
If a function g is continuous on the **closed** box $[-1,1]^2$ and its value at
that corner is v, then its uniform error against $\widetilde T$ on the open box
must be at least

$$
\sup_{k\in\mathbb R}|v-\phi(k/2)|=1+|v|\geq1.
$$

Take the limit along each path for the first inequality; the range of
$\phi(k/2)$ is $(-1,1)$ for the equality. The constant zero function has uniform
error supremum exactly one, so the lower bound is sharp. Consequently, a globally
continuous finite piecewise-affine map restricted to that closed code box cannot
approximate this target uniformly to error smaller than one on **all** open-box
inputs. Continuity on the open domain alone would not imply this obstruction:
$\widetilde T$ itself is continuous there, but has no such continuous extension.

The reason is cancellation between arbitrarily large opposite-signed decoded
values near a missing boundary point, not the mere word "bounded." The argument
does not apply unchanged to a restricted nonnegative-value domain or to a
compact encoded subdomain away from the boundary. It establishes no failure of
learning on a specified distribution or finite task population. Architecture
experiments remain a later branch; here the result prevents an unjustified
inference from exact invertibility to uniformly easy numerical approximation.

### L.3 Center before encoding when the admitted query permits it

A constructive alternative preserves unbounded absolute values while using
bounded coordinates for the task distinctions actually needed. Suppose the
request guarantees $\operatorname{osc}(h)\leq M$. Set

$$
c=h_n,\qquad d=h-c\mathbf1,
\qquad d_n=0,\quad |d_i|\leq M.
$$

For every candidate T map,

$$
T(h)=T(d)+c\mathbf1.
$$

Comparing available maps at the same input and continuation therefore needs
only their evaluations on d; the common c cancels between their values. Their
immediate rewards and costs remain inside each map and are **not** independently
recentered. For example, the maps $h\mapsto h$ and $h\mapsto h-1$ remain one
unit apart after the terminal input is centered. Quotienting each output by an
unrelated additive constant would wrongly erase that difference.

The relative coordinates can now be encoded in
$[-M/(1+M),M/(1+M)]$. Given a deterministic uniform error bound $\eta$ on those
codes, clip them to this known interval before decoding. Clipping cannot
increase their distance to the true in-range codes. For decoded values staying
in $[-M,M]$, the inverse has Lipschitz coefficient at most $(1+M)^2$; on one
sign branch this follows from

$$
\left|\frac a{1-a}-\frac b{1-b}\right|
=\frac{|a-b|}{(1-a)(1-b)},
$$

and across zero it follows by splitting the interval at zero. Thus the decoded
relative vector $\widehat d$ obeys

$$
\|d-\widehat d\|_\infty\leq(1+M)^2\eta=\delta.
$$

Nonexpansiveness gives $|T_j(d)_a-T_j(\widehat d)_a|\leq\delta$ **simultaneously
for every available exact T map** and every specified current input a. If an
agent chooses a maximizer of the approximate evaluations, its regret under the
actual h is at most $2\delta$. Subtract and add the two corresponding evaluations
at $\widehat d$: the approximate-choice difference is nonpositive, and the two
remaining errors are each at most delta. This is a shared deterministic input
certificate, not an inference from separate marginal coverage probabilities.

Centering must occur before the relevant quantization, or the relative vector
must be supplied with its own valid accuracy guarantee. Absolute value or
absolute adequacy questions still need c, or the correspondingly shifted
threshold. The method is not a lossless representation of every query after c
is discarded. It is a concrete finite-precision repair for this comparison
family, leaving the common absolute level unbounded.

### L.4 The shift/normalization premise cannot be silently weakened

If an approximate affine row has mass $1+\zeta$ rather than one, a common input
level c contributes an extra $\zeta c$. A small row-sum error can therefore
cause arbitrarily large error over the unbounded-level family. Normalizing a
learned row or adding the common offset outside a relative-coordinate model may
be a useful repair, but it changes or constrains the approximating map; it is
not a theorem about arbitrary nearly normalized coefficients.

Similarly, the two maps $T_1(h)=h$ and $T_2(h)=2h-1$ prefer different actions on
opposite sides of $h=1$. If their sole terminal value were discarded as a
"common offset," both would instead be evaluated at zero and the change would
be missed. The second map lies outside unit-mass T, exactly as section I.3
showed. A common known multiplier shared by all compared maps permits an
appropriately modified argument; different multipliers do not automatically
cancel. Context, units, continuation multiplicity, and retained precision thus
remain part of the same operational contract.

### L.5 A bounded-coordinate presentation can still be well behaved on the declared family

The cancellation obstruction is not a verdict against all bounded encodings.
The preceding change of coordinates supplies a positive contrast. Retain the
relative vector d in its supplied finite range, and let $z=\phi(c)$ encode the
common level. An encoded output coordinate can be written

$$
\Psi(z,d)=\phi\bigl(\phi^{-1}(z)+T(d)_a\bigr).
$$

On the allowed relative domain, nonexpansiveness gives
$|T(d)_a|\leq|T(0)_a|+M\leq B$ for a known finite B. For fixed $|v|\leq B$,
define $\psi_v(z)=\phi(\phi^{-1}(z)+v)$ on $(-1,1)$ and extend its endpoint
values by $\psi_v(1)=1$, $\psi_v(-1)=-1$. The extension is continuous, uniformly
for bounded v. Moreover,

$$
|\psi_v(z)-\psi_v(z')|\leq(1+B)^2|z-z'|,
\qquad
|\psi_v(z)-\psi_{v'}(z)|\leq|v-v'|.
$$

For the first inequality, write $x=\phi^{-1}(z)$. On the interior the derivative
is $(1+|x|)^2/(1+|x+v|)^2$, at most $(1+|v|)^2$ by the triangle inequality.
Integration and continuity include the endpoints. For the second, $\phi$ is
one-Lipschitz on real inputs, and endpoint limits agree independently of v.
Combining these inequalities with T's bound yields, for allowed d and d',

$$
|\Psi(z,d)-\Psi(z',d')|
\leq(1+B)^2|z-z'|+\|d-d'\|_\infty.
$$

The relative coordinates may themselves be bounded-encoded and decoded with
the estimate in L.3. This supplies a finite uniform **encoded-output** error
contract while the common real level remains unbounded. It does not supply a
uniform real-unit error after an arbitrarily near-boundary output is decoded;
that would again require accuracy information about c. Decision comparisons
that cancel c use the different, real-payoff regret guarantee in L.3.

The two presentations retain different numerical information before rounding:
independent absolute codes can lose a small relative difference, whereas a
common level plus explicitly retained relative coordinates need not. Exact
invertibility alone did not reveal that distinction. A proposed implementation
should therefore specify the coordinates it measures or stores, the consumer's
error units, and the permitted family of tasks—not declare one bounded or
unbounded format sufficient in the abstract.

## M. Final comparison audit: what has and has not been established

The S1 common-example table remains the primary comparison. Its G entry for
E04 has been clarified in this continuation: additive resource-relation
composition does not by itself prove physical-error propagation through an
amplifying stage. The relevant sensitivity and error-aggregation premise must
also be supplied. This is a correction to the table's scope, not a new theorem
that arbitrary error bounds add.

Four distinct closure questions should survive the next handoff:

| kind of closure | concrete positive evidence here | failure not excluded by that evidence |
|---|---|---|
| Algebraic | Finite T expressions remain in the monotone, shift-equivariant CPWA class; finite G operations have their stated generator rules. | A normal-form branch may not be an available physical program or preserve its witness/cost. |
| Operational | Matching-endpoint G sequencing and correctly observed-input T choice have explicit witnesses. | Hidden policy coupling, unobserved inputs, or shared unknown models may forbid the combined choices. |
| Approximation/task-family | Affine T has an exact propagated span allowance; G has a directed budget-slack composition bound. | A suffix may leave the admitted task family, or erased endpoints may invalidate slack transfer. |
| Numerical/representation | Relative-coordinate recoding and upward front rounding have stated error contracts. | Naive absolute-code quantization, unbounded cancellation, and a large refinement/front can defeat accuracy or resource expectations. |

The following distinctions also prevent an exaggerated candidate ranking.

**A scalar-family counterexample has a specified decoder.** The claim that all
weighted optimum values miss a deterministic budget option concerns optima
*after* action identity and nonoptimal vectors have been discarded. It is not
a claim about a table retaining every action's score at every coordinate weight.
Such a table reconstructs the cost vectors directly. That is additional
retained information, and should be counted as such rather than excluded by a
label like "scalar."

**Finite carriers are not infinite theories in disguise.** Finite P profiles,
finite T interfaces, and finite G fronts allow arbitrarily large finite real
coordinates. They do not thereby contain F01's entire countable payoff function
or an arbitrary infinite menu. A compact symbolic formula may represent some
countable cases, but its evaluation, tail, and closure premises are an explicit
extension. The nonattainment and cancellation examples show why the word
"unbounded" alone cannot decide those questions.

**The toy axiom example is still interpreted operationally.** A retained residue
interface and a declared decoder menu can determine the example's performance.
No candidate here has acquired a proof system for arbitrary theoremhood, an
oracle for consistency, or direct access to metaphysical truth. The initial
commitments remain motivation for useful conditional reasoning, not claims
proved by these finite constructions.

**No candidate has won by refusing every difficult query.** Each has worked
positive uses and explicit compositional laws in its admitted fragment. S is
sufficient for fixed linear evaluation; P for aligned operations; T for
specified sequential continuation questions; G for controlled budget
attainability. The richer information contracts and tolerance repairs above
clarify their scope rather than make one construction mandatory.

F03's external audit and F04's hostile comparisons remain separate unstarted
tasks. The known lattice-representation literature informs the finite T result;
no new-core soundness, completeness, independent review, or novelty status is
claimed. The next task pointer depends on F02's actual completion and timing
record, not on the number of pages or passing tests in this note.

## N. One common operational calculation across the four candidates

A small shared calculation makes the comparison concrete without scoring a
candidate on information another was not given. The following probabilities
and costs are stipulated model inputs, not empirical accuracy claims.

A hidden bit W is uniform. The legal uses are: choose a fixed uninformed answer
without acquiring a signal; acquire a cheap signal correct with probability
$3/4$ and follow it; or acquire a perfect signal and follow it. Their work costs
are zero, one, and three. Signal-dependent answers may use only the acquired
signal. A correct answer earns three payoff units and an incorrect one loses
one. A request supplies error cap epsilon, work cap b, and a conversion lambda
from work to payoff cost.

Let e be each use's error probability and c its work cost. Its expected net
payoff is $3-4e-\lambda c$. Directly from the supplied laws,

| legal use | error e | work c | net payoff at lambda=1/4 |
|---|---:|---:|---:|
| uninformed fixed answer | 1/2 | 0 | 1 |
| cheap signal, followed | 1/4 | 1 | 7/4 |
| perfect signal, followed | 0 | 3 | 9/4 |

At $(\epsilon,b)=(1/4,1)$, only the cheap use meets both requirements. At
$(1/10,1)$ none does. At $(1/2,3)$ all meet the requirements and the perfect
use has the largest displayed net payoff. If instead lambda is one, under
those same loose caps, uninformed and cheap uses tie at one while perfect has
net payoff zero. Changing the task does not contradict any earlier comparison.

**S's part.** Once the three net payoffs and the admissible menu for this
request have been supplied, comparing them is enough. Computing missing error
caps from an unexplained net score is not justified. If the construction
$3-4e-\lambda c$ and c are also supplied, e can of course be recovered; those
are additional inputs, not a failure of the counterexample principle.

**P's part.** A common four-scenario reference uses $(W,S_C)$ equal to
$(0,0),(0,1),(1,0),(1,1)$, with weights $(3,1,1,3)/8$. The perfect signal equals
W on each scenario. The cheap answer's gross payoff profile is $(3,-1,-1,3)$;
the fixed-zero answer's is $(3,3,-1,-1)$; the perfect profile is constantly
three. Their weighted means are respectively two, one, and three. Weighted
error-indicator profiles give the error column. Work remains its own declared
quantity before conversion or a hard-cap test. A pointwise choice after seeing
W would be a different information contract.

**T's part.** The cheap observation reaches each observed signal with probability
one-half and contributes immediate reward $-\lambda$. At a signal state the
posterior correctness probabilities are $3/4$ for following and $1/4$ for
opposing. Applying the terminal payoff $(3,-1)$ gives conditional action values
two and zero, so controlled choice at that *observed* interface yields
$2-\lambda=7/4$. The perfect observation similarly yields $3-3\lambda=9/4$;
the no-observation action yields one. This derives the values from a sequential
interface rather than treating them as final-score premises. It requires the
joint/posterior signal model, not just marginal signal frequencies. Legal work
budgets and separate expected-error eligibility must also be supplied or
represented; subtracting work in the reward does not itself enforce either cap.

**G's part.** Once the legally evaluated error/work pairs have been supplied,
its deterministic front is generated by $(1/2,0),(1/4,1),(0,3)$, all nondominated.
The three budget queries above are direct membership questions with concrete
use witnesses. Scalar net payoff can be compared afterward on the admissible
uses. G does not derive the signal's error probability from a bare resource
vector; that calculation came from the same supplied model used by P and T.

This example shows a legitimate division of work, not an instruction to package
all four objects into every judgment. A fixed request can use a scalar result;
a later budget change needs the retained performance distinctions; deriving
signal-dependent values needs the legal observation model. F02 has made those
candidate roles explicit so that the later core can choose and justify a small
set of primitives rather than claim that all of these queries were already
contained in one discarded score.
