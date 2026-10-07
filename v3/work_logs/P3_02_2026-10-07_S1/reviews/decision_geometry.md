# P3-02 internal review — geometry of exact decision recovery

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **proved conditional finite lemmas; internal same-model independent
reconstruction**. This is a targeted continuation of the finite recovery
review. It claims no new scientific contribution, adds no principal-session
clock credit, and starts no learning, acquisition or later gate work.

All statements concern a known finite action menu with linear expected
losses, the full real probability simplex, an exact linear observation, and
the service of returning some minimizing action. Arbitrary summaries,
restricted domains, changing action menus and externally fixed tie policies
are different contracts.

## 1. Setup

Let
```math
X=\Delta_n,\quad X^\circ=\{p\in\Delta_n:p_j>0\text{ for every }j\},
\quad H=\{p:\mathbf1^\top p=1\}.
```
The affine dimension of $`H`$ is $`d=n-1`$. Action $`i`$ has known loss
row $`c_i\in\mathbb R^{1\times n}`$, and its expected loss is
$`f_i(p)=c_ip`$. The Bayes envelope is
```math
f(p)=\min_i c_ip.
```
Observe $`y=Lp`$, and write
```math
A=\begin{pmatrix}\mathbf1^\top\\L\end{pmatrix},\qquad N=\ker A.
```
Thus $`N`$ contains exactly the affine directions hidden by the observation.
The service requires a function $`s`$ with
```math
s(Lp)\in\mathrm{argmin}_i c_ip\qquad(p\in X).
```
It may choose any optimal action at a tie.

## 2. Sharp two-action implication

### Proposition 1

For two actions, write $`r=c_1-c_2`$. Suppose
```math
\min_j r_j<0<\max_j r_j.
```
Then the following are equivalent on the full simplex:

1. The complete weak preference, including ties, is recoverable from $`Lp`$.
2. Some Bayes-optimal action is recoverable from $`Lp`$.
3. $`r\in\mathrm{row}A`$.
4. The numerical difference $`rp`$ is recoverable from $`Lp`$.

**Existence of an interior zero law.** Choose coordinates $`j_-,j_+`$
with $`r_{j_-}<0<r_{j_+}`$, and let $`u`$ be uniform. For sufficiently
small $`\delta>0`$, both
```math
p^-=(1-\delta)e_{j_-}+\delta u,\qquad
p^+=(1-\delta)e_{j_+}+\delta u
```
lie in $`X^\circ`$ and satisfy $`rp^-<0<rp^+`$.
A strict convex combination of these two laws gives
$`p^0\in X^\circ`$ with $`rp^0=0`$.

**Proof of the nontrivial implication.** If $`r\notin\mathrm{row}A`$,
there is $`h\in N`$ with $`rh\ne0`$. Since $`p^0`$ is strictly
positive, $`p^0\pm\epsilon h\in X^\circ`$ for sufficiently small
$`\epsilon>0`$. The two observations agree, but their action differences
are $`\pm\epsilon rh`$. Each law has a different uniquely optimal action.
Thus even the weaker service in item 2 fails. Conversely, item 3 gives
$`r=\alpha\mathbf1^\top+\beta L`$, hence
$`rp=\alpha+\beta y`$, proving items 4, 1 and 2. $`\square`$

### Boundary and dominance exceptions

The strict crossing assumption cannot be omitted. If $`r\geq0`$
coordinatewise, action 2 is always optimal and needs no observation.
Recovering whether it ties can still require information; recovering the
size of its advantage can require more.

For example, with $`L=(1,0,0)`$ and $`r=(0,1,2)`$, the difference is
zero exactly when $`y=1`$, and is positive otherwise. Its sign is therefore
known everywhere, even though its value $`p_2+2p_3`$ is generally
underidentified. The zero set lies on a boundary face; there is no interior
zero law around which both perturbation signs are feasible.

With no observation, the same example still permits choosing action 2
everywhere, but does not determine the complete weak preference because
it cannot distinguish a tie from a strict inequality. If $`r=0`$, every
law is a tie and all four services are trivial.

## 3. Reduce the menu without demanding a particular tie action

First merge identical loss rows, retaining one representative. For each
remaining action define its strict interior cell
```math
U_i=\{p\in X^\circ:c_ip<c_jp\text{ for all }j\ne i\}
```
and its closed optimal cell
```math
R_i=\{p\in X:c_ip\leq c_jp\text{ for all }j\}.
```
Let $`E=\{i:U_i\ne\varnothing\}`$. These are the essential affine pieces
of the lower envelope.

### Lemma 2: essential rows preserve the envelope

The set $`E`$ is nonempty, and
```math
f(p)=\min_{i\in E}c_ip\qquad\text{for every }p\in X.
```

**Proof.** Distinct rows induce distinct affine functions on $`H`$.
Their tie sets are proper affine hyperplanes or empty sets. A finite union
of such hyperplanes cannot cover $`X^\circ`$, so a law avoiding all ties
has a unique minimizer belonging to $`E`$. For any $`p\in X`$, approach
it by tie-free laws in $`X^\circ`$. A subsequence has a fixed unique
minimizer $`i\in E`$; continuity gives $`c_ip=f(p)`$. $`\square`$

An action that is uniquely optimal at a boundary law is also uniquely
optimal at some sufficiently nearby interior law, by the strict finite
inequalities and continuity. Thus discarded actions can supply extra ties,
but cannot be the only optimal action anywhere in $`X`$.

The lemma justifies constructing a selector using $`E`$. It does not
preserve every original tie set or a tie policy that specifically demands
a discarded action.

## 4. Interior adjacency gives an exact finite characterization

Assume $`n\geq2`$. Make a graph $`G`$ on $`E`$, joining $`i,j`$ when
their full-dimensional optimal cells share a facet of dimension $`d-1`$
meeting $`X^\circ`$. Facets confined to the boundary of the probability
simplex are not edges of this graph.

### Lemma 3: the graph is connected

The cells of the finite affine lower envelope form a polyhedral subdivision
of $`X`$. Take interior points of any two strict cells. A polygonal path
between them inside the convex set $`X^\circ`$ can be chosen to avoid
intersections of distinct boundary hyperplanes of codimension at least two.
It then visits a finite sequence of full-dimensional cells and crosses only
their shared interior facets. This gives an edge path between the two cells.
In dimension one, the same argument is the ordinary ordering of intervals.

At a generic point of an interior facet there are exactly two essential
pieces in the local envelope. To see why a third cannot remain tied along
that entire facet, restrict the affine functions to $`H`$. Their differences
then vanish on the same codimension-one affine hyperplane and are
proportional. One of three distinct such affine pieces is a strict convex
combination of the other two and can never be uniquely minimal anywhere.
It therefore is not essential. Additional tie hyperplanes meeting the
facet in smaller dimension can be avoided.

### Theorem 4: globally sufficient linear summaries for some optimal action

Under the setup above, the following are equivalent:

1. A selector $`s(Lp)`$ returning some optimal action exists on all of $`X`$.
2. For every edge $`\{i,j\}`$ of $`G`$,
   

```math
   (c_i-c_j)h=0\qquad\text{for every }h\in N.
   
```
3. For all $`i,j\in E`$, $`c_i-c_j\in\mathrm{row}A`$.
4. After choosing a reference action $`i_0\in E`$, there are known affine
   functions $`q_i(y)=\alpha_i+\beta_i y`$, with $`q_{i_0}=0`$, such that
   

```math
   c_ip=c_{i_0}p+q_i(Lp)\qquad(i\in E,\ p\in X).
   
```

In particular, condition 4 constructs a valid selector:
```math
s(y)\in\mathrm{argmin}_{i\in E}q_i(y).
```
The common baseline $`c_{i_0}p`$ can remain unknown.

**Necessity at an edge.** Suppose an edge $`i,j`$ has a hidden direction
$`h\in N`$ with $`(c_i-c_j)h\ne0`$. Choose a generic point $`p^0`$
in the interior of its facet, with $`p^0\in X^\circ`$, where the local
essential envelope consists of $`i,j`$. Choose sufficiently small
$`\epsilon>0`$. Both $`p^\pm=p^0\pm\epsilon h`$ are feasible and have
the same observation. Assume, by changing the sign of $`h`$, that
$`(c_i-c_j)h>0`$. The minimizing essential action is $`j`$ at $`p^+`$
and $`i`$ at $`p^-`$. Consequently,
```math
\frac{f(p^+)+f(p^-)}2
=f(p^0)-\frac{\epsilon}{2}(c_i-c_j)h
<f(p^0).
```
If any original action were optimal at both endpoints, the affine value
of that action at their midpoint would be this smaller quantity, below
the minimum $`f(p^0)`$. This is impossible. Thus the fiber has no common
optimal action. This argument permits discarded actions to tie at special
points; it does not assume the selector must choose an essential action.

**Remaining implications.** Condition 2 and connectivity imply that every
essential difference, obtained by summing edge differences along a path,
annihilates $`N`$. Orthogonality to $`\ker A`$ gives condition 3 and
its affine factorization in condition 4. That factorization and Lemma 2
give the selector and prove condition 1. $`\square`$

For $`n=1`$, merging duplicates leaves exactly one essential minimizing
row, and the result reduces to a constant optimal action. More generally,
if $`E`$ contains one action, no observation is needed and the edge
conditions are vacuous.

### An equivalent fiber geometry

For any nonempty fiber $`F(y)`$, a common optimal action exists iff
the restriction of $`f`$ to that fiber is affine. One direction uses the
common action's affine loss. For the other, take a relative-interior law
of the fiber and an action optimal there. Its affine loss minus the assumed
affine envelope is nonnegative throughout the fiber and zero at a
relative-interior point, so it is zero throughout the fiber.

The strict midpoint inequality in the proof of Theorem 4 is precisely
the obstruction to this affine restriction.

### Minimum dimension, with the representation scope stated

Let $`D_E`$ contain the differences $`c_i-c_{i_0}`$ for $`i\in E`$.
If known linear loss measurements may be freely chosen, the minimum number
required for this global decision service is
```math
\mathrm{rank}\begin{pmatrix}\mathbf1^\top\\D_E\end{pmatrix}-1.
```
Theorem 4 gives the lower bound; a basis of the required difference rows
modulo the constant row attains it. Edge differences give the same span.
With rational loss rows, the construction and affine decoding can use
rational coefficients. Finding the essential cells, constructing the
measurements and evaluating the decoder still have computational costs.

This is a restriction on linear expectation summaries. An arbitrary
nonlinear summary could simply encode an optimal action identifier, and
is outside this dimension statement.

## 5. Nontrivial example: discard a strictly dominated action

Take three outcomes and retain $`y=p_1`$. Use the menu
```math
c_A=(0,1,1),\qquad c_B=(1,0,0),\qquad
c_D=(1/4,5/4,9/4).
```
Action $`D`$ is strictly dominated by $`A`$, since
```math
c_D-c_A=(1/4,1/4,5/4)>0
```
coordinatewise. The essential set is $`E=\{A,B\}`$, and its only
edge difference is
```math
(c_A-c_B)p=1-2y.
```
Thus choose $`A`$ for $`y>1/2`$, $`B`$ for $`y<1/2`$, and either
at equality. The chosen action depends nontrivially on the summary.

At the same observation $`y=2/3`$, consider
```math
p=(2/3,1/3,0),\qquad q=(2/3,0,1/3).
```
The cost triples $`(A,B,D)`$ are respectively
```math
(1/3,2/3,7/12),\qquad (1/3,2/3,11/12).
```
Action $`A`$ is optimal at both laws, but the ordering of $`B,D`$ reverses.
Therefore this summary recovers an optimal action while failing to recover
the complete preference order and several action differences. Demanding
all rows $`c_i-c_j`$ would reject a sufficient decision summary.

As a contrasting application, three-way zero-one classification has
$`c_i=\mathbf1^\top-e_i^\top`$. All three actions are essential;
their differences require both simplex dimensions. A single linear
expected-loss measurement cannot preserve an optimal class globally,
although two can. This conclusion concerns all mixed laws, not merely
the three pure laws.

## 6. Scope and resolved exploratory question

The proposed adjacency characterization **does hold** under the declared
full-simplex, finite-menu, exact-linear assumptions. No unresolved
geometric obstruction remains within that scope.

The fiber-intersection condition remains the appropriate general statement
for other domains. For instance, on the nonconvex domain
$`\{e_1,e_2,e_3\}`$, the one-dimensional summary $`L=(0,1,2)`$ identifies
every law and every action, even though the full-simplex dimension test
can fail. There is no connected interior cell graph on that discrete
domain to justify Theorem 4's necessity argument.

The theorem does not preserve the original complete tie set. A fixed tie
rule can demand more information: with $`c_A=(0,0)`$, $`c_B=(0,1)`$
and no observation, choosing $`A`$ is always optimal. A rule requiring
$`B`$ whenever the two tie depends on whether $`p=e_1`$, which this
summary does not retain.

These are reconstructed convex/polyhedral facts and service distinctions.
They give no update rate, resource-optimal algorithm or superiority to
ordinary decision theory.

## 7. Development cross-check

An exact rational enumeration compared two logically different predicates
for the fixed summary $`y=p_1`$ on $`\Delta_3`$:

1. Identify essential action cells by their positive two-dimensional area;
   check that every essential row has the same hidden-direction coefficient
   $`c_{i2}-c_{i3}`$.
2. Directly test that the two endpoints
   $`(y,1-y,0)`$, $`(y,0,1-y)`$ of every fiber share an optimal action.
   Endpoint action orders can change only at their rational pairwise
   crossing values of $`y`$; check all such values and interval midpoints.
   A common action at the endpoints is optimal on the whole segment.

All distinct two- and three-action menus drawn from the 27 rows with
coordinates in $`\{-1,0,1\}`$ were checked:

| Menu size | Menus | Sufficient summaries | Predicate disagreements |
|---|---:|---:|---:|
| 2 | 351 | 204 | 0 |
| 3 | 2,925 | 1,224 | 0 |

The strictly dominated-action numerical example was also checked using
exact rational arithmetic. These finite calculations are development
checks of the proof and examples, not a frozen challenge or empirical
claim about other domains.

The enumeration used the following standard-library-only calculation:

~~~python
from fractions import Fraction as F
from itertools import combinations, product

def active(rows):
    out = []
    for i, c in enumerate(rows):
        # Coordinates p=(x,z,1-x-z); each constraint is ax+bz+c0 <= 0.
        constraints = [(-1, 0, 0), (0, -1, 0), (1, 1, -1)]
        for j, b in enumerate(rows):
            if i != j:
                d = [c[t] - b[t] for t in range(3)]
                constraints.append((d[0]-d[2], d[1]-d[2], d[2]))
        vertices = set()
        for (a, b, c0), (d, e, f0) in combinations(constraints, 2):
            det = a*e-b*d
            if det:
                x, z = F(b*f0-c0*e, det), F(c0*d-a*f0, det)
                if all(u*x+v*z+w <= 0 for u, v, w in constraints):
                    vertices.add((x, z))
        vertices = list(vertices)
        if len(vertices) >= 3:
            x0, z0 = vertices[0]
            if any((x1-x0)*(z2-z0)-(z1-z0)*(x2-x0) != 0
                   for (x1,z1),(x2,z2) in combinations(vertices[1:], 2)):
                out.append(i)
    return out

def direct_fiber_service(rows):
    cuts = {F(0), F(1)}
    for col in (1, 2):
        for a, b in combinations(rows, 2):
            slope = (a[0]-a[col])-(b[0]-b[col])
            intercept = a[col]-b[col]
            if slope:
                y = F(-intercept, slope)
                if 0 <= y <= 1:
                    cuts.add(y)
    cuts = sorted(cuts)
    checks = cuts + [(a+b)/2 for a, b in zip(cuts, cuts[1:])]
    for y in checks:
        opts = []
        for col in (1, 2):
            values = [c[col]+(c[0]-c[col])*y for c in rows]
            low = min(values)
            opts.append({i for i, v in enumerate(values) if v == low})
        if not (opts[0] & opts[1]):
            return False
    return True

row_set = list(product((-1, 0, 1), repeat=3))
counts = {2: 0, 3: 0}
sufficient = {2: 0, 3: 0}
for k in (2, 3):
    for rows in combinations(row_set, k):
        E = active(rows)
        predicted = len({rows[i][1]-rows[i][2] for i in E}) == 1
        actual = direct_fiber_service(rows)
        assert predicted == actual, (rows, E, predicted, actual)
        counts[k] += 1
        sufficient[k] += actual
print(counts, sufficient)
~~~

## 8. Extracted reproducible development check

The enumeration is now available as the standard-library-only script
[02_decision_geometry_check.py](../../../checks/02_decision_geometry_check.py).
It explicitly merges duplicate rows for the geometric predicate and keeps
the endpoint oracle separate from that cell calculation. Its JSON records
the exact scope, oracle description, same-model status and script SHA-256.

The script was run once after extraction:

~~~sh
python v3/checks/02_decision_geometry_check.py --output v3/work_logs/P3_02_2026-10-07_S1/development/decision_geometry_agent.json
~~~

The [saved development result](../development/decision_geometry_agent.json)
reports **passed**, 3,276 menus and zero predicate disagreements. The
endpoint oracle examined 879 observation values for the two-action corpus
and 7,627 for the three-action corpus; negative cases stop after a witnessed
failure rather than checking the remainder of their partition.

Five focused rational checks are also saved:

- The nonconstant optimal selector with the strictly dominated third action,
  including the reversed full preference rankings at $`y=2/3`$, the tie
  at $`y=1/2`$, and the endpoint observations $`y=0,1`$.
- A common optimal action despite differing complete optimal-action sets
  within one fiber, demonstrating why a specified tie policy can fail.
- Opposite unique optima at two strictly positive laws in one fiber,
  alongside successful local recovery at a boundary singleton.
- The one-sided sign exception, with unequal positive gaps in one fiber
  and a tie only at the extreme observation.
- Explicit duplicate-row merging and retention of all duplicate actions
  in the direct oracle's tie sets.

This run supplies development evidence only. The principal's inspection
and separate rerun do not add duplicate research credit.
