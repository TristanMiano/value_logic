# Cost-region guards for improving maps and value quotients

**DEVELOPMENT derivation — Codex (GPT-6), October 13, 2026 UTC.**
S29 continuation after [G01's ordinary-policy tie](g01_findings.md).
The witness-substitution idea is inherited from certified dominance and
redundance; [source notes](source_notes.md) distinguish that import from the
cost-uncertainty interface developed here. No claim of a new general proof
system, new dominance theorem or solver superiority is made.

## 1. Preserve an optimum, without asserting a global equality

Let F be a nonempty finite set of source-feasible assignments, with ordered
violation vector $`z(x)\in\{0,1\}^m`$. Let G be a nonempty subset of F.
A checked map $`T:F\to G`$ has a public, source-bound objective guard:

```math
w^\top z(Tx)\leq w^\top z(x)+\epsilon(w)
\quad\text{for every }x\in F,\ w\in W,
\qquad\epsilon(w)\geq0.
```

Write $`C_F(w)=\min_{x\in F}w^\top z(x)`$ and define $`C_G`$
analogously. Then, pointwise throughout W,

```math
C_G(w)-\epsilon(w)\leq C_F(w)\leq C_G(w).
```

The right inequality follows from set inclusion. For the left, apply T to an
attaining minimizer in F: its image is a candidate in G of cost at most the
minimum plus epsilon. T need not be injective and need not preserve every
optimum. When epsilon is zero the optimum values agree, including at zero
weights where additional unreduced optima may exist.

Suppose a separately checked range certificate proves $`Az(x)=b`$ for x in G.
If $`w-q=A^\top\lambda(w)`$, every retained representative has the common
shift $`\kappa(w)=b^\top\lambda(w)`$, and
$`C_G(w)=C_G(q)+\kappa(w)`$. This permits S29's quotient construction on G
even if the full feasible source F has no affine equality at all. A raw lower
proof on the reduced source alone lower-bounds $`C_G`$, not automatically
$`C_F`$; subtract the admitted epsilon before making the latter inference.

## 2. Regret and replacement retain different terms

Take a checked representative u, nominal cost U, and an admitted reduced-source
lower $`L\leq C_G(q)`$. Suppose cost-source bounds give shift interval
$`[\kappa_-,\kappa_+]`$ and $`\epsilon(w)\leq e`$. At fixed replacement
price p, the following are sufficient uniform bounds:

```math
B_{\mathrm{repair}}=
\max\{0,\ U-L+e,\ U+\kappa_+-p\},
```

```math
B_{\mathrm{replace}}=
\max\{0,\ p-\max(0,L+\kappa_- -e)\}.
```

The repair-to-repair comparison consumes e; comparison with replacement does
not change the repair's physical cost by e. The zero clamp assumes nonnegative
original weights. If original costs can be signed, omit that clamp or prove a
separate valid lower. Tolerance tau must cover the full logical gap plus the
map error; a small observation interval cannot erase either obligation.

Keeping correlations may be stronger than separate extrema. With affine
transport and a pointwise epsilon envelope, replacement uses the minimum of
$`L+\kappa(w)-\epsilon(w)`$ on the same source W. Do not combine the most
favorable shift and error from incompatible outcomes.

## 3. Objective guards are reusable evidence, not permanent facts

Structural feasibility and range certificates bind the original and reduced
source, variable/feature maps and assumptions. The objective guard separately
binds the allowed cost region W and its support calculation. If a truthful
paid observation refines W to a subset, the guard remains sound. A later
reprice that expands or changes W needs its own guard evaluation; source-byte
identity alone does not authorize it.

For a finite set of possible changes $`d=z(Tx)-z(x)`$, a sufficient objective
guard is $`\max_d\sup_{w\in W}w^\top d\leq e`$. The difference set must
be proved to cover every feasible x; observed examples alone do not establish
that. A compact overapproximation is allowed, with its resulting weaker e.
For product cost rows, each support maximum is a sum of per-row maxima and
does not enumerate their Cartesian product. A guessed invariance or a free
membership oracle is not an admitted guard.

Successive maps must preserve the current reduced source. If
$`F=F_0\supseteq F_1\supseteq\cdots\supseteq F_k`$ and each map sends
$`F_{j-1}`$ into $`F_j`$ with pointwise error e_j, composition has error at
most their sum. Independently applying maps that undo each other's constraints
does not satisfy this premise. Directly bounding the composed displacement
can be tighter than summing separate maxima.

## 4. A full-dimensional source with a one-dimensional useful quotient

Let Boolean variables be s and y_1,...,y_n, with hard clauses
$`s\lor y_i`$. Soft violations are those variables themselves. Define
$`T(s,y)=(s,1-s,\ldots,1-s)`$. If s=0, feasibility already forces every
y_i=1, so the map changes nothing. If s=1, the map sets every y_i to zero;
all hard clauses stay true and all nonnegative y costs weakly decrease.
The reduced source has equations $`y_i+s=1`$.

For n at least one, F is full-dimensional in its n+1 feature coordinates:
the s=1 cube spans the n y directions, and the s=0/all-one point adds the s
direction. Thus these equations are **false as global feasible-source facts**.
They are valid on the certified representative set. There need not be any
nontrivial original-source affine quotient, yet the reduced set has dimension
one and exactly preserves the optimum for all nonnegative costs.

To make a concrete paid cost target, let independent hidden
$`\theta_i\in\{1,100\}`$ contribute theta_i to y_i and s. Add fixed cost
2 to y_1 and an independent hidden cost $`d\in\{0,4\}`$ to s. The two
representative repair costs are

```math
\sum_i\theta_i+2\quad(s=0),\qquad
\sum_i\theta_i+d\quad(s=1).
```

A physical audit of the d row selects an exact optimum, leaving all n theta
rows unresolved. At p=100n+5, replacement is irrelevant to regret, although
the common absolute cost remains unknown. No fixed repair is uniformly
zero-regret before the d audit. Ordinary weighted star vertex-cover
simplification makes the same reduction and takes the same audit; that is a
mandatory strongest comparison. The construction broadens the admitted
capability, not its demonstrated comparative resource advantage.

## 5. Prospective development check

Execute n=1,3,5 with every hidden theta/d outcome. Save the public source,
map, structural checks and nonnegative objective guard before observations.
Charge the map/range compilation and witness checks; execute a coordinate
audit provider. Independently enumerate original feasible models only after
each output. Include negative controls: an extra hard unit y_1 invalidates
the map on s=1, and negative y weight invalidates the nonincrease guard.
Also check the epsilon correction on finite signed-cost examples without the
nonnegative clamp. Do not present this prototype as running VeriPB or as
displacing its dominance-preprocessing capabilities.
