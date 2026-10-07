# P3-02 — calibrated finite-decision information

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**, October 7, 2026 UTC. Direct mathematical
development review. No source search, project code execution, principal
edit, clock credit or gate determination accompanies this note.

## 1. Finding and exact scope

**The proposed extension is correct.** It concerns a finite nonempty
original action menu with known finite loss rows, the full simplex,
fixed exact linear measurements and the service **return some original
action that is Bayes-optimal at the actual law**. Scale is common and
strictly positive; an unknown offset is common and unrestricted.

Merge duplicate action rows. Let $`E`$ be the actions uniquely optimal
at some interior simplex law. Choose $`a_0\in E`$, and let $`D`$ have
rows $`c_a-c_{a_0}`$, $`a\in E`$. The choice of reference does not
change its row span. The existing finite essential-envelope argument
ensures $`E\ne\varnothing`$ and preserves at least one original optimum
at every law, including the boundary.

Let $`M`$ be the differences of the raw measurement rows from one
retained reference:
```math
M_j=L_j-L_0\qquad(j\ne0).
```
For an empty or single-row menu, take its effective difference matrix
to have no rows. Then the global criteria are:

| Observation contract | Necessary and sufficient condition for some optimal action |
|---|---|
| $`v=Lp`$ | $`\mathrm{row}D\subseteq\mathrm{row}[\mathbf1^\top;L]`$ |
| $`v=Lp+b\mathbf1,\ b\in\mathbb R`$ | $`\mathrm{row}D\subseteq\mathrm{row}[\mathbf1^\top;M]`$ |
| $`v=sLp,\ s>0`$ | $`\mathrm{row}D\subseteq\mathrm{row}L`$ |
| $`v=sLp+b\mathbf1,\ s>0,\ b\in\mathbb R`$ | $`\mathrm{row}D\subseteq\mathrm{row}M`$ |

With one essential action the conditions are vacuous and that action
works without observations.

## 2. Positive-cone proof

Put $`x=sp`$. As $`p`$ ranges over the full simplex and $`s>0`$,
```math
K=\{x\geq0:\mathbf1^\top x>0\}
```
is exactly the source of possible $`x`$. It is convex, its interior
is the strictly positive orthant, and its affine direction space is
$`\mathbb R^n`$. Conversely $`s=\mathbf1^\top x`$ and
$`p=x/s`$. Positive scaling preserves every original action's
optimality, so the essential actions are unchanged.

**Sufficiency.** If $`D=BL`$, the observation $`v=Lx`$ gives
```math
Bv=Dx=sDp.
```
Minimizing these essential-action differences from $`a_0`$ gives an
optimal original action. Neither the common baseline $`c_{a_0}p`$
nor the scale itself must be recovered.

**Necessity.** Write $`f(x)=\min_a c_ax`$. The finite arrangement of
strict essential-action cells in the positive orthant has connected
adjacency through interior facets: a generic polygonal path between
strict-cell points avoids intersections of codimension at least two.
At a generic facet between adjacent essential actions $`a,b`$, only
those two essential affine pieces are active locally. If a third
distinct essential piece agreed on that entire facet, one of the
three would be between the other two as a linear function and could
never be uniquely minimal.

Suppose an invisible direction $`h\in\ker L`$ satisfies
$`(c_a-c_b)h>0`$. At a generic positive facet point $`x^0`$, choose
small $`t>0`$ so that $`x^\pm=x^0\pm th`$ remain positive and lie
in the two neighboring strict cells. They have identical observations,
while
```math
\frac{f(x^+)+f(x^-)}2
=f(x^0)-\frac t2(c_a-c_b)h<f(x^0).
```
If any original action were optimal at both endpoints, linearity would
make its cost at the midpoint equal the left side, contradicting the
definition of $`f(x^0)`$. This excludes a common optimum even when
the purported common action is a discarded boundary-tie action.

Thus every adjacent essential difference annihilates $`\ker L`$.
Connectivity gives the same conclusion for every row of $`D`$, and
the rowspace/nullspace identity yields
$`\mathrm{row}D\subseteq\mathrm{row}L`$.
Normalizing $`x^\pm`$ gives admissible law/positive-scale witnesses
for the original contract. The differing strict optima ensure these
are genuinely different law cases.

This is the existing PI-9 geometry on a different convex source.
There is no known-normalization row for $`x`$: its total mass is
the unknown scale. The one-state case has one essential action after
duplicates are merged and needs no facet argument.

## 3. An unrestricted common offset

Subtracting the observed reference gives $`Mx`$. This reduction loses
no law information under an unrestricted common offset. If
$`Mx=Mx'`$, every component of $`Lx-Lx'`$ equals
$`L_0x-L_0x'`$. Choosing
```math
b'=b+L_0x-L_0x'
```
therefore makes $`Lx+b\mathbf1=Lx'+b'\mathbf1`$.
An empty menu has no information to match; with one raw row, its
unrestricted offset can match any value.

The exact action criterion consequently uses $`M`$ in place of $`L`$.
For known scale, the same argument is applied to normalized $`p`$,
so normalization remains available and the known-scale PI-9 criterion
uses $`[\mathbf1^\top;M]`$.

Bounded offsets, report-dependent offsets or constrained scales are
different sources. This reduction and its necessity statement do not
silently cover those contracts.

## 4. Minimum freely selected queries from scratch

Assume at least two essential actions, and define
```math
d=\mathrm{rank}[\mathbf1^\top;D]-1,\qquad
r=\mathrm{rank}D.
```
Both are positive. For freely selected fixed signed linear measurement
rows, the sharp raw-query counts are:

| Calibration information | Minimum raw queries |
|---|---:|
| Scale and offset known | $`d`$ |
| Scale known, unrestricted offset unknown | $`d+1`$ |
| Positive scale unknown, offset known | $`r`$ |
| Positive scale and unrestricted offset unknown | $`r+1`$ |

For known scale, normalization supplies the constant direction and
$`m`$ rows supply at most $`m`$ further quotient dimensions. A basis
of the required differences modulo constants attains $`d`$.
For unknown scale, $`m`$ rows span at most $`m`$ required ordinary
dimensions; a basis of $`\mathrm{row}D`$ attains $`r`$.

An unrestricted unknown offset leaves at most $`m-1`$ effective
differences from $`m\geq1`$ raw queries. This gives each additional
one-query lower bound. A zero-payoff reference plus the corresponding
basis queries attains it. **All four counts are zero if one essential
action suffices**; an otherwise unnecessary reference must not be charged.

These upper constructions presume the basis rows are admissible.
They apply to freely chosen known real rows, and to rational rows
when the action table is rational. A restricted menu, nonnegative-row
requirement, precision limit or acquisition cost needs its own analysis.
For arbitrary real action rows, restricting queries to rational rows
can change these minima even though the stated row-space criteria remain
valid for each chosen observation matrix.
The formulas concern construction from scratch; an existing reference
changes the accounting for subsequent repair.

The difference between $`d`$ and $`r`$ can matter. For binary states
and actions $`(0,3),(1,1),(3,0)`$, all three are essential. Their
differences span $`\mathbb R^2`$, so $`d=1`$ and $`r=2`$.
A single known-unit probability coordinate locates the three decision
regions; one unknown-scale linear measurement cannot do so globally.

## 5. Signed versus nonnegative queries

For binary actions
```math
c_1=(1,0),\qquad c_2=(0,1),
```
one signed query $`\ell=(1,-1)`$ suffices under unknown positive
scale and known zero offset. Its value
```math
v=s(p_1-p_2)
```
is negative exactly when action 1 is strictly preferable, positive
exactly when action 2 is strictly preferable, and zero at a tie.

No single nonnegative row can supply this service globally. If
$`\ell\geq0`$ is nonzero, it has positive expectation at every interior
law. For any prescribed $`v>0`$, every such law can produce $`v`$ by
choosing $`s=v/(\ell p)`$. In particular
$`(1/4,3/4)`$ and $`(3/4,1/4)`$ have opposite unique optima and
can produce the same record. The zero row is also uninformative;
it is the exception to the literal “every interior value is positive”
wording.

Two nonnegative indicator queries suffice: compare $`sp_1`$ with
$`sp_2`$. If a common offset is also unknown, comparing
$`b+sp_1`$ with $`b+sp_2`$ still selects an optimal action, even
though those two values do not generally identify the law under that
larger calibration contract.

Finally, this service returns **some** optimal original action.
For example, losses $`(0,0)`$ and $`(0,1)`$ admit the first action
without any information, although the full set of optimal actions
changes at a boundary law. Complete tie sets, prescribed tie breaking,
absolute costs and all preferences therefore retain their separate
information requirements. No learning or resource advantage follows
from the calibrated decision characterization.
