# P3-02 — exact projection of independently bounded payoffs

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**. Same-model internal, nonblind derivation check.
This note owns no clock, ledger, status, gate or principal-file decision.
Concurrent reviewer effort is not additional principal research credit.
Its examples and constructions remain development material.

## 1. Result and quantified uncertainty

The proposed positive case is correct. Let $`p\in\Delta_n`$, and let an
unknown semantic payoff/loss matrix $`L\in\mathbb R^{m\times n}`$ belong to
the known entrywise box
```math
\mathcal B=\{L:\underline L_{ji}\leq L_{ji}\leq\overline L_{ji}
\text{ for all }j,i\},
```
where all endpoints are finite and
$`\underline L_{ji}\leq\overline L_{ji}`$. All entries can be chosen
independently within these intervals. Given an exact observation $`y=Lp`$,
the compatible law set is exactly
```math
\boxed{
\{p\in\Delta_n:\exists L\in\mathcal B,\ Lp=y\}
=
\{p\in\Delta_n:\underline Lp\leq y\leq\overline Lp\}.}
\tag{U1}
```

The right-hand side is a polytope, possibly empty. Thus the original
bilinear expression in the joint unknowns $`L,p`$ admits an exact affine
projection in this case. The claim is an elementary reconstruction under
the stated uncertainty model; no general elimination theorem, novelty
claim or external source survey is needed.

The existential quantifier matters. A different matrix may witness
compatibility for each candidate law. Equation (U1) does not say that one
matrix simultaneously makes every candidate law produce $`y`$, or that
every admissible matrix does so.

## 2. Direct proof and constructive witness

Fix any candidate $`p\in\Delta_n`$. Nonnegative probability weights imply,
for every admissible matrix and each row $`j`$,
```math
a_j:=\underline L_jp
\ \leq\ L_jp\ \leq\
b_j:=\overline L_jp.
```
This proves necessity. The loss entries themselves may be negative; it is
the nonnegativity of the weights $`p_i`$ that gives these endpoints.

Conversely, suppose $`a_j\leq y_j\leq b_j`$ for every row.
If $`b_j>a_j`$, choose
```math
\theta_j=\frac{y_j-a_j}{b_j-a_j}\in[0,1],
\qquad
L_{ji}=\underline L_{ji}
+\theta_j(\overline L_{ji}-\underline L_{ji})
\quad\text{for every }i.
\tag{U2}
```
All row entries are admissible, and
```math
L_jp=a_j+\theta_j(b_j-a_j)=y_j.
```
If $`b_j=a_j`$, compatibility forces $`y_j=a_j`$, and the lower row is
a valid witness. In particular, a zero-width weighted interval causes no
division problem. Entries at outcomes with $`p_i=0`$ can remain arbitrary
within their declared intervals.

The rows can be selected independently, so their witnesses assemble into
one admissible matrix. This proves sufficiency and (U1).

### What independence can be weakened to

Full entry independence is sufficient but stronger than this proof needs.
For each row, it suffices that:

1. Every admissible row lies componentwise between its declared lower and
   upper vectors.
2. The entire segment
   $`\{\underline L_j+\theta(\overline L_j-\underline L_j):
   0\leq\theta\leq1\}`$ is available.
3. Any selected admissible rows can be assembled together; there is no
   additional shared constraint coupling the rows.

The construction uses only that row segment. Mere coordinatewise marginal
intervals, or rowwise attainable ranges without joint row availability, do
not establish sufficiency.

## 3. An exact affine lift

One can also introduce $`x_{ji}=L_{ji}p_i`$. Under this particular box
uncertainty model, the following finite affine constraints give an exact
lift:
```math
p\geq0,\quad \mathbf1^\top p=1,\qquad
\underline L_{ji}p_i\leq x_{ji}\leq\overline L_{ji}p_i,\qquad
\sum_i x_{ji}=y_j.
\tag{U3}
```
Every joint state $`(p,L)`$ gives such an $`x`$. Conversely, if $`p_i>0`$,
set $`L_{ji}=x_{ji}/p_i`$. If $`p_i=0`$, both bounds force $`x_{ji}=0`$,
and any value in the corresponding payoff interval works. Entry
independence permits all these choices at once.

Eliminating $`x`$ row by row gives (U1), because the sum of independently
selectable real intervals is the interval between their endpoint sums.
This lift supplies a second check on the quantifiers and the zero-probability
case. It ceases to encode the intended joint uncertainty when unknown
matrix entries obey additional correlations that the lift omits.

## 4. Rational counterexample: one shared stake

Take two exhaustive indicator losses and one common unknown positive stake:
```math
L(s)=sI_2,\qquad 1\leq s\leq2,\qquad
y=(2/3,2/3).
```
The exact equations are
```math
sp_1=2/3,\qquad sp_2=2/3,\qquad p_1+p_2=1.
```
Adding them recovers $`s=4/3`$, so the only compatible law is
```math
p=(1/2,1/2).
\tag{U4}
```

The componentwise matrix bounds are still
$`\underline L=I_2`$ and $`\overline L=2I_2`$. Applying only the rowwise
bands gives
```math
p_i\leq2/3\leq2p_i\quad(i=1,2),
```
or
```math
p=(u,1-u),\qquad 1/3\leq u\leq2/3.
\tag{U5}
```
This is strictly larger than (U4). Its endpoint $`p=(1/3,2/3)`$ is
attained by the independently chosen matrix
```math
L=\begin{bmatrix}2&0\\0&1\end{bmatrix},
```
which produces $`y=(2/3,2/3)`$ but is not $`sI_2`$ for any common $`s`$.
The other endpoint reverses the two stakes.

Indeed, every law in (U5) is feasible under independent row stakes:
choose $`s_1=(2/3)/p_1`$ and $`s_2=(2/3)/p_2`$, both in $`[1,2]`$.
Thus (U5) is the exact law polytope for the box model and a strict outer
approximation for the shared-stake model. The shared-stake example itself
has a singleton exact law set; it isolates the need to preserve cross-row
correlation.

### Correlation within one row can also matter

Let one unknown row be
```math
L(s)=(s,1-s),\qquad 0\leq s\leq1.
```
Its coordinatewise bounds are $`(0,0)`$ and $`(1,1)`$. For the candidate
law $`p=(1/2,1/2)`$, those bounds allow any value in $`[0,1]`$.
But every actual admissible row has expectation exactly $`1/2`$, so,
for example, $`y=1/4`$ is impossible at that candidate law.
The whole diagonal segment between the declared coordinatewise lower and
upper vectors is not present in this row uncertainty set.

## 5. Independent observation-error extension

If the observation is instead
```math
y=Lp+e,\qquad |e_j|\leq\epsilon_j,
```
with these error coordinates independently available and independent of
the payoff-box choices, then the projected law set remains exactly
```math
\{p\in\Delta_n:
\underline L_jp-\epsilon_j\leq y_j
\leq\overline L_jp+\epsilon_j\ \text{for every }j\}.
\tag{U6}
```
For a fixed $`p`$, row $`j`$ can produce any semantic expectation in
$`[a_j,b_j]`$ and independently add any error in
$`[-\epsilon_j,\epsilon_j]`$. Their sum is precisely the interval
$`[a_j-\epsilon_j,b_j+\epsilon_j]`$. Equivalently, choose an expectation
from
$`[a_j,b_j]\cap[y_j-\epsilon_j,y_j+\epsilon_j]`$, use (U2) to realize it,
and take the remaining difference as the error.

Correlated errors or correlations between errors and payoff parameters must
be retained separately. The componentwise inequalities then remain necessary
under valid marginal bounds but need not be sufficient.

## 6. Scope and use in the P3-02 artifact

For a target $`Cp`$ with known coefficients, exact ranges over (U1) or
(U6) are ordinary linear programs. Full-law recovery is the special case
where the compatible law polytope is a singleton. A target expectation may
be uniquely recovered even when that polytope contains multiple laws.
No necessity of full-law recovery follows from this construction.

The interval endpoints and observation are semantic inputs to this
conditional result. The proof does not establish that learned endpoint
estimates are valid bounds or that arbitrary value numbers are expectations.
If the desired target depends on the unknown payoff matrix, projecting only
to $`p`$ may discard information needed for that target; the joint lift
or additional target variables should then be retained.

A single unknown matrix shared across several different unknown laws and
their observations also adds couplings. Applying (U1) separately to each
law allows different witnessing matrices and therefore need not characterize
their joint compatibility under the one shared matrix.

For fixed rational endpoints, (U1), (U3) and (U6) use only known rational
coefficients and affine inequalities. They therefore provide an exact
special-purpose elimination compatible with the phase-two representation
boundary. The witness formulas use division, but computing a witness matrix
is unnecessary when the required service is projected-law feasibility or a
linear target range. This gives a concrete positive case without admitting
arbitrary products of jointly uncertain quantities into the native language.

Recommended attribution: **direct finite reconstruction for independently
bounded payoff uncertainty, with an explicit exact projection and correlated
parameter counterexamples**. The result is useful as a scoped mathematical
adaptation and ordinary-comparison case; it does not by itself determine
a contribution-gate disposition.
