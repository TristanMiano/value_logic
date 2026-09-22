# F03 — Worked mappings and import boundaries

September 22, 2026. Base: `65e91d9b46bf61566160de9dbdcb4a1a98b33f02`.
These are direct finite or explicitly specified set-theoretic calculations used
in the [literature audit](01_foundations.md). Source identifiers S01–S11 refer to
that note. They do not select a calculus or discharge F04, F07 or Gate A.

## M01. Abstraction needs a declared order and query polarity

Let `C` be the powerset of the real line, ordered by inclusion. Let `I` contain
empty and all closed real intervals, allowing infinite endpoints but not treating
infinity as a finite outcome. Set

$$
\alpha(S)=[\inf S,\sup S]\cap\mathbb R\quad(S\ne\varnothing),
\qquad \alpha(\varnothing)=\varnothing,
\qquad \gamma(I)=I.
$$

For an interval in the abstract domain,

$$
\alpha(S)\subseteq I \iff S\subseteq\gamma(I).
$$

Both implications follow because `I` is a closed interval: containment of `S`
puts its extremal limits in the same interval, and `S` is contained in its hull.
This gives a concrete example of S01's abstraction/concretization interface.
The concrete powerset and this interval domain are complete lattices; interval
joins are closed hulls of unions, not generally plain unions. In contrast, just
finite endpoints would omit the join of `[0,n]` over positive integers `n`.

For the concrete pointwise square operation, take `S={-1,1}`. Then

$$
\alpha(\{x^2:x\in S\})=\{1\},
\qquad \{x^2:x\in\alpha(S)\}=[0,1].
$$

The larger interval is sound as a possible-outcome enclosure, but is not an
exact reconstruction. No averaging or arbitrary numerical summary has been
shown to form such an adjunction by this example.

There is a separate polarity issue. Suppose `Q` is a set of possible payoff
outcomes and `Qhat` encloses it. Then

$$
Q\subseteq\widehat Q,\quad\inf\widehat Q\geq b
\quad\Longrightarrow\quad\inf Q\geq b
$$

whenever the extrema are defined as extended bounds. Nonempty support is a
separate operational premise when required. But if `G` is the set of budgets
an available implementation can actually satisfy, a membership guarantee needs

$$
\widehat G\subseteq G,\quad b\in\widehat G\quad\Longrightarrow\quad b\in G.
$$

An *outer* approximation of `G` instead supports some impossibility conclusions:
`G subset H` and `b notin H` imply `b notin G`. It does not generally support
positive feasibility. These are different queries on sets, not contradictory
notions of soundness. A claim that one should always overapproximate or always
underapproximate loses this distinction.

**Impact:** source S01 supplies a method after an explicit semantic order has
been chosen. It does not decide that order for the project. No recursive
fixed-point result is imported into the current acyclic examples.

## M02. Metric nonexpansiveness does not mean every operation preserves one error

Use ordinary absolute distance on the scalar carrier. Binary addition gives

$$
|0-1|=|0-1|=1,\qquad |(0+0)-(1+1)|=2.
$$

It therefore fails the common-error `NExp` rule for a binary operation with the
maximum input distance, as required by S02. The valid bound is instead

$$
|(x+y)-(x'+y')|\leq |x-x'|+|y-y'|.
$$

Minimum, maximum and a *fixed* convex mixture satisfy a maximum-error bound.
For example, if each input changes by at most `epsilon`, all inputs lie between
the corresponding old input minus/plus `epsilon`; monotonicity and common
translation of the minimum imply the same bracket for its result. A varying
mixture coefficient requires additional information about the coefficient and
input spread; it is not covered by that fixed-mixture assertion.

S09 provides a known generalization using operation-specific distance liftings.
Here is an elementary candidate instance, not a completeness proof. On the
unbounded set of real values define

$$
d(x,y)=\min(1,|x-y|),
\qquad D((x_1,x_2),(y_1,y_2))
 =\min(1,d(x_1,y_1)+d(x_2,y_2)).
$$

The capped sum is a metric on the product: symmetry and separation are immediate,
and its triangle inequality follows from that of the components and
`min(1,a+b) <= min(1,a)+min(1,b)` for nonnegative `a,b`. Addition is nonexpansive
from this product metric to `d`. If either component difference is at least one,
the right side is one and the conclusion is immediate; otherwise it follows
from the ordinary triangle inequality and capping.

This product construction sends a nonexpansive map to a nonexpansive product
map and preserves isometric embeddings because the displayed distances depend
only on component distances. Those are concrete checks of S09's lifting
interface for this example. They do not establish every proviso of a future
mixed signature or its deductive completeness.

The distance is bounded; the values are not. For a requested radius below one,
`d(x,y) <= epsilon` is exactly the ordinary absolute-error condition. At radius
one it loses all large-error discrimination. A different declared scale can
alter this interface, but silently capping an existing real-error claim would
change its meaning. A directed regret/slack relation is also not automatically
a symmetric metric; the selected generalized-distance axioms must match it.

**Impact:** failing S02's baseline rule is a specific signature mismatch, not a
reason to dismiss quantitative algebra or to declare values must be bounded.

## M03. Forward kernels, backward continuations, and lost probability mass

Let `P` be a finite nonnegative matrix with row sums at most one. A row
subdistribution `mu` moves forward to `mu P`. Pairing with a column continuation
`h` gives

$$
\sum_j(\mu P)_j h_j
 =\sum_i\mu_i\sum_j P_{ij}h_j
 =\mu(Ph).
$$

This elementary duality relates S03's forward linear semantics to a finite
backward expectation transformer. If a second kernel is `Q`, its backward
composition is `P(Qh)=(PQ)h`. With fixed immediate reward vectors `r,s`, the
corresponding affine composition is

$$
r+P(s+Qh)=(r+Ps)+(PQ)h.
$$

The exact common-shift calculation is

$$
(r+P(h+c\mathbf1))-(r+Ph)=cP\mathbf1.
$$

It equals `c 1` for every real `c` precisely when all row sums are one. A
one-state substochastic kernel `[1/2]` halves the shift. Its map is still
nonexpansive for absolute distance, but it is not in F02's shift-preserving
stochastic fragment. Probability of nontermination or loss cannot be ignored
by importing the normalized law from another model.

One may add an explicit cemetery state to restore stochastic rows, but the
continuation assigned to that state then has a meaning. Shifting it along with
all other states is a different query from holding its value fixed at zero.
Thus this construction requires a declared interface, not just a matrix rewrite.

**Impact:** retain F02's row-stochastic premise. No theorem about all
probabilistic programs is used to remove it, and optimization does not preserve
the linearity of the precise-kernel fragment in general.

## M04. Two different representation results for continuation maps

For a scalar map `f:R^n -> R`, assume monotonicity and
`f(x+c 1)=f(x)+c`. Put `m=max_i(x_i-y_i)`. Since `x <= y+m 1`,

$$
f(x)-f(y)\leq\max_i(x_i-y_i).
$$

Consequently every term on the right below is at least `f(x)`, and `y=x`
attains equality:

$$
f(x)=\min_{y\in\mathbb R^n}\max_{1\leq i\leq n}
       \{x_i-y_i+f(y)\}.
$$

This is the finite-coordinate specialization of the general representation
inspected in S05. Its outer index is still all of `R^n`. It does **not** give a
finite expression or a constructive way to know every `f(y)`.

A different premise supplies finiteness. Suppose `f` is globally continuous and
has finitely many affine pieces. On any full-dimensional region where
`f(x)=r+p dot x`, small coordinate increases and monotonicity imply `p_i>=0`.
Small common shifts within the region imply `sum_i p_i=1`. Lower-dimensional
boundaries inherit values by continuity. The finite max–min representation in
S04 then uses affine pieces with these stochastic slopes. For vector outputs,
apply the argument coordinatewise, retaining the finite expression data.

This checks the external step used in F02-C25 and separates it from the more
general S05 representation. It says nothing about a *fixed restricted* library
of leaf rewards/kernels, expression size, which player observes a choice, or
preservation of one implementation witness across several requirements.

Positive homogeneity is another distinct condition. The map `h -> 1+h` is
monotone and shift-preserving but fails `f(2h)=2f(h)`. Thus the zero-immediate-
payment result in S05 cannot replace its affine representation for all of T.
A scalar smooth example such as `log((exp(x)+exp(y))/2)` has the same monotonicity
and shift law without finitely many affine pieces. Its existence illustrates
why the finite-piece premise is substantive, not a technical omission.

## M05. Which semiring properties does G actually possess?

For finite `F subset R^d`, write

$$
\uparrow F=\{b:\text{some }f\in F\text{ satisfies } f\leq b\}.
$$

Include the empty set. Let alternative choice be union and free independent
combination be Minkowski sum. Finite generation is preserved by both operations:
`up F union up H = up(F union H)` and
`up F + up H = up{f+h:f in F,h in H}`. Union is idempotent; Minkowski sum is
associative, commutative and distributes over finite unions. The zero is empty,
and the multiplicative identity is `up{0}`. This establishes a useful finitary
idempotent semiring. It does not establish S06's entire c-semiring interface.

### Signed costs: the identity is not additive top

Already in one dimension let `U=[-1,infinity)` and `e=[0,infinity)`. Then
`U union e=U`, not `e`. Thus the multiplicative identity does not absorb union.
The signed finite-generated carrier has no top element: every finite menu has
a finite lower bound in each coordinate, while the union of all such menus is
the entire signed space. S06's top/identity axiom fails.

### Finite generation: infinitary union needs additional treatment

Even with nonnegative costs,

$$
\bigcup_{n\geq1}[1/n,\infty)=(0,\infty)
$$

is not a finite-generated closed upper set. Therefore the declared operation
of literal union cannot simply be applied to arbitrary families in that carrier.
This example alone is **not** proof that no alternative completion exists:
in one dimension the closed rays can use closure of union for their joins.
That would be an additional definition and would require checking the other
laws and endpoint interpretation.

In two nonnegative coordinates the finite-generated carrier even lacks some
order-theoretic suprema. Consider all `U_t=up{(t,1-t)}`, `0<=t<=1`. Their union
is

$$
K=\{(x,y)\in\mathbb R_+^2:x+y\geq1\}.
$$

It is not finite-generated: every point of its sloping boundary is a distinct
minimal element. For each positive integer `n`, the finite-generated set

$$
H_n=\uparrow\{(k/n,1-(k+1)/n):k=0,\ldots,n-1\}
$$

contains `K`. To see this, for `0<=x<1` choose `k=floor(nx)`; then
`y>=1-x>=1-(k+1)/n`. If `x>=1`, the last generator applies.
Every point of `H_n` has `x+y>=1-1/n`, so `intersection_n H_n=K`.
If the `U_t` had a least upper bound `H` in the finite-generated carrier, it
would contain `K` and be contained in every `H_n`, hence equal `K`, a contradiction.

### Nonnegative full-upper-set comparison

Taking **all** upward subsets of `R_+^d` allows arbitrary unions. Empty is bottom,
the entire orthant is both top and the Minkowski identity, and addition of sets
distributes over arbitrary unions. This gives an explicit c-semiring comparison
construction matching S06's stated axioms. It does not promise finite
representations or decidable membership for arbitrary members.

Moreover, multiplication is still not idempotent:
`[1,infinity)+[1,infinity)=[2,infinity)`. Thus the extra premise in S06's
Theorem 4.16 is not repaired by the domain completion. Repeatedly charging a
resource is different from intersecting the same constraint twice.

**Impact:** G's finitary laws survive. Importing a general local-consistency or
fixed-point result requires additional hypotheses; no such algorithm is adopted
by this audit. Different completions remain options to compare rather than
changes silently applied to the candidate.

## M06. Scalarization preserves an upper hull, not every menu

Let `F={(0,2),(2,0)}` and add `z=(3/2,3/2)` to obtain `H`. For nonnegative
weights `w=(a,b)`,

$$
\min_{f\in F}w\mathbin{\cdot} f=2\min(a,b)
\leq\tfrac32(a+b)=w\mathbin{\cdot}z.
$$

It is in fact strict for every nonzero nonnegative weight; the weak inequality
is already sufficient for the comparison. Thus `F` and `H` have the same minimum weighted scores.
The budget `z` belongs to `up H` but not `up F`. Positive feasibility has been
lost, not contradicted by the scalarization results of S07.

For a nonempty finite menu, linear minimization over
`conv(F)+R_+^d` has exactly the same values as minimization over `F` for all
nonnegative weights. Conversely, if a point lies outside this closed convex
upper image, separation supplies a strictly separating nonzero nonnegative
weight. Nonnegativity follows because the set contains every positive-coordinate
ray; a negative coefficient would make its infimum minus infinity. Hence those
weighted values characterize the convex upper image. Closedness here follows
from a finite convex hull being compact and the orthant being closed.

This is the finite specialization underlying F02's recovery claim, consistent
with S07's upper-image and scalarization discussion. It does not mean every
minimizer of a boundary-weight scalar problem is Pareto optimal. For example,
weights `(1,0)` cannot distinguish `(0,0)` from the dominated point `(0,1)`.

An admitted lottery between the two members of `F` has expected vector `(1,1)`.
It meets the expected budget `z`, but each realized member violates one
coordinate of that same hard budget. Allowing lotteries or changing from
pathwise to expected constraints is an operational change, not harmless
numerical compression.

## M07. Rectangularity is a constraint on admissible models

For a known policy, the robust value in S08 minimizes over the allowed complete
conditional models. Replacing them by arbitrary combinations of stagewise
choices is valid as an equality only under the required pasting condition.
A two-stage algebraic witness uses one unknown `theta in {0,1}` and rewards
`theta` and `1-theta`. With the same parameter at both stages,

$$
\min_{\theta\in\{0,1\}}[\theta+(1-\theta)]=1.
$$

Allowing separate adversarial choices gives

$$
\min_{\theta_1}\theta_1+\min_{\theta_2}(1-\theta_2)=0.
$$

One can realize the same expectation calculation with deterministic reward
labels on next-state outcomes and two correlated transition choices. The point
is the restricted joint model family, not a refutation of a theorem whose
rectangularity assumption it violates.

The rectangular relaxation contains the original models, so its minimum is a
valid *lower bound* on the original robust value. It need not be exact. Keeping
a common parameter, retaining sufficient history, or explicitly accepting a
conservative bound are distinct responses. Adding an unobserved parameter to
the decision maker's information would be a different problem.

**Impact:** F02's robust sequential caveat has a precise prior framework. The
next adversarial task should test the declared policy and uncertainty interfaces,
not merely whether a min/max expression evaluates to a number.

## M08. Unrestricted operations do not justify unrestricted quantitative substitution

S10 allows arbitrary interpretations of an operation symbol, but constrains a
substitution by the relation carried by its variables. Here is a direct witness
for why those are different permissions.

Use the real carrier with `d(x,y)=min(1,abs(x-y))`, and two variables `a,b`
whose directed input relation bound is `d_A(a,b)=1/10`. Put every other input
relation bound at one so it adds no constraint. Every admitted nonexpansive
interpretation `tau` then satisfies

$$
d(\tau(a),\tau(b))\leq1/10.
$$

Thus the corresponding quantitative variable judgment is valid. Now interpret
a unary symbol `g` by `g(x)=10x`, and try the substitution
`sigma(a)=g(a)`, `sigma(b)=g(b)`. With `tau(a)=0`, `tau(b)=1/10`,

$$
d(g(\tau(a)),g(\tau(b)))=d(0,1)=1>1/10.
$$

The substituted judgment is false. S10's actual substitution rule does not
make that inference: its additional premises require the substituted variable
pair to preserve the old `1/10` bound, which fails in this model. A separately
proved Lipschitz bound could supply a different, larger error allowance. Merely
admitting `g` as an operation supplies no such guarantee.

A second distinction is ordinary equality versus zero distance. On a two-element
set with the fuzzy relation constantly zero, different elements have zero
distance. Therefore `s =_0 t` need not imply `s=t` unless a separation axiom is
adopted. Such a separation condition is a semantic choice, not a theorem about
all value representations. This countermodel uses a permitted fuzzy relation;
it is not a claim that the ordinary metric on real values lacks separation.

**Impact:** generalized quantitative algebra remains a viable comparison even
for amplifying operations and directed relations. To reuse a completeness result,
the project must translate the actual variable, equality and operation contracts,
not drop a soundness side condition to make the syntax look simpler. This small
countermodel is not a proof or implementation of the entire cited system.

## Review status

The arguments above are same-agent calculations and source mappings. They have
not undergone independent review. Finite regression checks are useful for their
explicit numerical witnesses but cannot establish the infinitary completion
claims or the cited representation theorems. Source-specific hypotheses remain
in the audit and bibliography rather than being promoted to universal axioms.
