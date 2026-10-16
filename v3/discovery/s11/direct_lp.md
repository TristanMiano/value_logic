# Direct linear formulation of the restricted minimax-regret problem

Codex (GPT-6), DEVELOPMENT derivation. This is a proposed compact synthesis of
the realization polytope and the common-source regret oracle. It is not a new
general minimax principle. All assumptions of `policy_flow.md` and
`robust_flip.md` apply: known query-cell masses, independent intervals for
conditional first moments, fixed nonnegative query/flip fees, and a pathwise
operation cap. The source is selected before private policy randomization.

## Epigraph of the exact oracle

The realization vector x determines affine cell rows C_z(x), s_zi(x).
For each cell z, coordinate i, and comparator coefficient a in {-1,0,1}, introduce
an unrestricted-real variable d_zia with the two inequalities

```math
d_{zia}\ge w_i(s_{zi}(x)-a)\ell_{zi},\qquad
d_{zia}\ge w_i(s_{zi}(x)-a)u_{zi}.
```

For queried coordinates take both endpoints equal to the observed sign z_i.
Define W_hi(a)=sum_{z extending h} p_z d_zia and
C_h=sum_{z extending h} p_z C_z(x), P_h=sum_{z extending h}p_z.
These are affine expressions. Define k_h=H-|h| and introduce B_h.
For every history impose the terminal-zero constraint

```math
B_h\ge C_h+\sum_i W_{hi}(0).
```

For terminal one, use the ordinary dual representation of the sum of the
k_h largest positive gains. Introduce t_h>=0 and e_hi>=0 and impose

```math
e_{hi}+t_h\ge W_{hi}(-1)-W_{hi}(1)-f_iP_h,
\qquad
B_h\ge C_h+\sum_i W_{hi}(1)+k_ht_h+\sum_i e_{hi}.
```

This remains valid for k_h=0 and k_h>=m. At k_h=0 choose t_h at least every
positive gain and all e=0; for k_h>=m choose t=0. Finally, for every available
query j impose

```math
B_h\ge-a_jP_h+B_{h,j=-1}+B_{h,j=1}.
```

Minimize B_empty over these inequalities and the realization polytope. All
expressions are linear. With explicit cell-row variables and their defining
equalities, the formulation uses O(m 4^r) nonzero coefficients from cell/history
incidences, and O((m+r)3^r) variables and
constraints, independent of the number of unobserved joint truth assignments.
This is polynomial for fixed r, not polynomial in unrestricted r. The first
prototype substitutes cell expressions directly; its common-fee expansions
can instead use O(m 7^r) nonzeros. Do not attribute the more economical explicit
row implementation to that executed code.

## Why the epigraph is exact

Fix a feasible controller x. Set each d to its true endpoint maximum. Choose
each (t,e) to realize the exact top-k expression, and B by the exact backward
oracle recursion. This is feasible and attains the actual worst-case regret.

Conversely any feasible d dominates that endpoint support. Although the top-k
formula contains differences W(-1)-W(1), its resulting value is monotone in
*both* W(-1) and W(1): equivalently it is the maximum over legal subsets of
the sum of W(-1) on selected coordinates and W(1) on unselected coordinates,
minus the selected fees. Each existential (t,e) gives an upper bound on that
maximum. Terminal-zero and query expressions are monotone too. Backward
induction therefore gives B_empty at least the actual oracle value for x.
Taking the minimum over x proves the asserted exact formulation.

The proof uses the separately derived common-source oracle, whose independence
across mean coordinates and disjoint leaf cell sets is load-bearing. Replacing
the mean box with arbitrary coupled constraints does not inherit exactness.

## Why this is worth an inexpensive screen

The earlier double oracle had a nonzero gap at its 40-iteration limit on the
31-coordinate example. The direct LP removes policy-column and source-corner
generation for this particular menu. That is a concrete algorithmic capability
to check, not yet an observed speed or cost advantage. A strong ordinary
implementation of the same reduction will tie it. Comparison work must decide
whether the restricted synthesis and its proof offer a worthwhile delta.

Prospective screen: the same four declared sources, then a few varied small
instances if those pass. Check the repaired admissible policy with the exact
regret oracle. Check a rational lower certificate independently of numerical
LP status. Preserve all failures; do not reinterpret a floating optimum as an
exact result. Stop widening this branch after the cheap screen and return to
the broader portfolio.

## Bounded-variable lower certificate

The first prototype places finite bounds on all variables. Realization entries
are in [0,1] because each compatible full cell has a unit path flow. Support
variables have absolute value <=2|w_i| at the exact endpoint supports. Set
M=H max(all fees)+2 sum_i |w_i|. The exact backward values lie in [-M,M].
Each top-k threshold can be chosen in [0,4 max_i |w_i|], and each excess in
[0,4|w_i|]. These loose bounds preserve at least one exact epigraph realization
for every feasible controller, hence preserve the minimax optimum.

For a minimization LP c.x with Ax<=b, Ex=d and l<=x<=u, any rational
lambda<=0 and unrestricted rational nu give the lower bound

```math
\lambda^T b+\nu^T d+
\sum_j\min\{r_j\ell_j,r_j u_j\},
\qquad r=c-A^T\lambda-E^T\nu.
```

Indeed lambda.Ax>=lambda.b and nu.Ex=nu.d, and the remaining linear form is
bounded by its coordinatewise box infimum. No numerical dual feasibility is
assumed. Round proposed multipliers, check the formula with rational arithmetic,
and combine with the exact regret of an admissible repaired controller.
The first denominator-limited multipliers create an unnecessarily large common
denominator; this is a representation cost, not a soundness defect. A separate
common-grid reconstruction can reduce it without rerunning the LP.

## First observed screen

`dl01` completed the four declared cases on their first attempts under Python
3.12.14, NumPy 2.2.6 and SciPy 1.15.3. Cases 0 and 1 have zero exact gap.
Case 2's exact gap is 3667/5846859776. The 31-coordinate case uses 2553
variables, 3198 inequalities and 56958 nonzeros. Its checked upper is
5.196596539839095 and lower is 5.19659371304027 (displayed decimals); exact
rationals are retained. Gap <0.000002827, versus 0.361465 in the previous
40-iteration grid double oracle. Its certified upper is 34.77075% below the
named interval-midpoint policy's 239/30 regret. This is one exposed development
example, not a fresh benchmark or a comparison against all ordinary methods.

The intermediate realization-flow cutting-plane version also completed under
the amended runtime (`pf02`), but its 40-iteration upper 5.52172 and gap
0.43270 were worse than the earlier double oracle. That adverse result remains
part of the record. The direct LP is a mathematically different next development,
not a relabelled successful retry of the cutting-plane version.

`dl02` adds six prospective small boundary cases (zero horizon, no query,
zero fees/weights, zero-mass cells and horizons above the number of coordinates).
All six completed on their first attempts. Their exact oracle uppers matched
all 228 interval corners; 44 corner planners also matched unrestricted
interleaved planning. The largest gap is below 0.000001181. This checks the
declared finite cases, not arbitrary constraints or independent confirmation.

`dl01_grid.json` reuses existing numerical advice without a new LP run. Its
common-grid 31-coordinate lower is 5.196593716194002, with a 43-bit numerator/
denominator maximum and gap below 0.000002824. The original large-denominator
certificate is preserved. The probability grid in executable local rules and
the multiplier grid in the lower proof have different meanings.
