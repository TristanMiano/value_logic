# P3-02 hostile review: global affine scalar recovery

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated internal reviewer,
October 7, 2026 UTC. Direct mathematical reconstruction and adversarial
boundary checks; development status, no independent time credit. Only this
review is added. No new numerical test, learner, gate or later task is run.

Context: `v3/derivations/02_probability_information.md` §12 (PI-13 and the
three-outcome conditioning case); `reviews/noise_conditioning_case.md`
§§1–6; `reviews/noise_bridge_review.md` §§2–5. Primary optimal-recovery
source attribution is being checked by the principal; this review supplies
a self-contained proof and does not assert priority for the theorem.

## 1. Verdict and the necessary correction to the proposed caveat

The proposed polytope theorem and its LP dual proof are correct. A fixed
scalar linear target, a known compact convex source, and exact linear
observations admit a **globally optimal affine decoder**, even when their
pointwise fiber midpoints are not affine. No central symmetry is needed.
Bounded additive errors can be included among the unknown coordinates.

There is one important strengthening: **finite-vector unrestricted
sup-norm recovery also has a globally optimal affine decoder**, by applying
the scalar theorem separately to its coordinates. Vector-valuedness alone
does not break the claim in the present sup-norm scope. A requirement that
the output come from a compatible source point can break equality with the
unrestricted optimum. Other target norms need a separate argument.

The three proposed affine decoders for the current `L_delta` example have
exactly the stated worst errors. Choosing the best known regime therefore
attains its previously derived sharp global radius. A nonlinear fiber LP
or midpoint construction is not necessary merely to attain that global
worst-case scalar number in this example.

## 2. Exact statement and finite LP proof

Let

\[
K=\operatorname{conv}\{x_1,\ldots,x_s\}\subset\mathbb R^d
\]

be a nonempty compact convex polytope. Let `N` be a fixed known linear
observation map to `R^m`, and let `c` be a fixed known scalar linear target.
The decoder sees `z=Nx` and may return any real number. Values at impossible
observations outside `NK` do not affect this service. Define

\[
R_*:=\inf_g\sup_{x\in K}|cx-g(Nx)|,
\qquad
D:=\max_{\substack{x^+,x^-\in K\\Nx^+=Nx^-}}
       c(x^+-x^-).
\tag{A1}
\]

The ordered pair may be swapped, so the maximum in D equals the maximum
absolute target difference. Its feasible set is nonempty and compact.
Then

\[
\boxed{
R_*=\frac D2
=\min_{\alpha\in\mathbb R,\,\beta\in(\mathbb R^m)^*}
  \sup_{x\in K}|cx-\alpha-\beta Nx|.}
\tag{A2}
\]

Both the unrestricted and affine optima are attained. A prescribed output
range, source coherence, extra computational restrictions or a changing
target are not included in the affine decoder class in (A2).

### Unrestricted radius

Every indistinguishable pair forces any decoder's error to be at least
half the pair's target separation. Conversely, on each nonempty fiber,
the minimum and maximum of `cx` exist. Their midpoint has error half that
fiber's width. These observations prove `R_*=D/2`. This step itself does
not require convexity, only the stated compactness and scalar service.

### Affine primal

Write `z_i=Nx_i` and `t_i=cx_i`. An affine decoder has error at most r
on K if and only if it does at the listed generators. Indeed its signed
error is affine in x, and its absolute value at a convex combination is
at most the corresponding convex combination of endpoint errors. Its
optimal radius is therefore the finite LP

\[
\begin{array}{ll}
\text{minimize}&r\\
\text{subject to}&t_i-\alpha-\beta z_i\le r,\\
&\alpha+\beta z_i-t_i\le r\quad(i=1,\ldots,s).
\end{array}
\tag{A3}
\]

Here r, alpha and beta are free real variables. The paired inequalities
already force `r>=0`, so an explicit nonnegativity restriction on r is
redundant. Keeping r free gives the clean equality form of the dual below.
The primal is feasible, for example with `alpha=beta=0` and
`r=max_i |t_i|`, and its objective is bounded below.

### Dual and convex barycenters

Assign nonnegative dual weights `mu_i` and `nu_i` respectively to the first
and second inequalities. Taking the infimum of the Lagrangian over the
free primal variables gives

\[
\begin{array}{ll}
\text{maximize}&\displaystyle\sum_i(\mu_i-\nu_i)t_i\\
\text{subject to}&\displaystyle\sum_i\mu_i=\sum_i\nu_i=\frac12,\\
&\displaystyle\sum_i\mu_i z_i=\sum_i\nu_i z_i,\\
&\mu_i,\nu_i\ge0.
\end{array}
\tag{A4}
\]

For clarity, the free r coefficient requires
`sum(mu)+sum(nu)=1`; the free alpha coefficient requires equal totals.
The beta coefficients require equality of observation barycenters.

Every feasible dual point defines

\[
x^+=2\sum_i\mu_i x_i,\qquad
x^-=2\sum_i\nu_i x_i.
\]

Each is in K because its coefficients are nonnegative and sum to one;
their observations agree. The dual objective is exactly
`c(x^+-x^-)/2`, hence is at most `D/2`.

Conversely, represent any pair in (A1) as convex combinations of the
generators and divide each set of convex weights by two. This gives a
feasible dual point with objective half that pair's target difference.
Thus the dual optimum is `D/2`. Finite LP strong duality and attainment
give (A2). This also explains precisely where convexity enters: it turns
dual barycenters into admissible objects.

For rational generators and rational N and c, the finite LP has rational
optimal data available. This is an existence and verification statement;
enumerating a large vertex set and obtaining the coefficients may have
substantial costs. It grants no free computation or undeclared unit map.

### Additive noise as exact information about an enlarged object

For known compact convex `P` and `E`, take

\[
x=(p,e)\in K=P\times E,\qquad
N=[L\ I],\qquad c'=(c,0).
\]

The exact observation of x is the noisy record `z=Lp+e`. Formula (A2)
therefore applies to the original scalar target. More generally it applies
to a declared compact convex joint mechanism `K subseteq P times E`.
Independence, a probability distribution for e, and central symmetry of E
are not needed. If the allowed mechanism is nonconvex or the target becomes
nonlinear after a parameterization change, those premises need separate
checking. An unknown scale normalized by a ratio is not automatically a
linear target on a convex enlarged source.

## 3. Optional extension beyond polytopes

The same conclusion holds for any nonempty compact convex K in a
finite-dimensional space. A finite-intersection proof avoids an unproved
infinite LP duality assertion.

Let `R=D/2`, and put `S=NK`. Select observations
`z_0,...,z_k` affinely spanning S, with preimages `x_0,...,x_k in K`,
where `k=dim(aff S)`. An affine function on `aff S` is uniquely specified
by its values `v_j` at these observations. Restrict them to the compact box

\[
v_j\in[cx_j-R,cx_j+R],\qquad j=0,\ldots,k.
\]

For any finite collection F of further source points, the polytope
`conv(F union {x_0,...,x_k})` is contained in K. Its indistinguishable-pair
radius is at most R. The finite theorem therefore supplies affine values
in that box satisfying all constraints indexed by F. Each additional
constraint `|cx-g(Nx)|<=R` is closed in the finite vector of values v.
The resulting family of closed subsets of the compact box has the finite
intersection property, so a single v satisfies every constraint for K.
Extend the resulting affine function from `aff S` to the ambient observation
space. This supplies an attained affine error at most R; the pair lower
bound supplies equality.

The extension is mathematical existence. For a nonpolyhedral source it does
not turn an unavailable representation or optimization oracle into a finite
implementation.

## 4. What the theorem does not identify with affine recovery

### One rational triangle separates global, local and coherent optimality

Take objects `x=(z,t)` in

\[
K=\operatorname{conv}\{(0,0),(1,0),(2,1)\},
\qquad N(z,t)=z,\qquad c(z,t)=t.
\tag{A5}
\]

This is also a direct finite-law example: take `p in Delta_3`, observe the
known expected loss `z=p_2+2p_3`, and request `t=p_3`. The attainable
observation-target pairs are exactly this triangle.

For `0<=z<=2`, the target interval is

\[
[a(z),b(z)]=[\max(0,z-1),\ z/2].
\]

Its maximum width is `1/2`, attained at z=1, so `R_*=1/4`. The affine
decoder `g(z)=z/2-1/4` has residuals `1/4,-1/4,1/4` at the three source
vertices and attains that global optimum. It is not pointwise optimal:
the singleton fibers at z=0 and z=2 have true targets 0 and 1, while g
returns `-1/4` and `3/4`.

The pointwise midpoint is the nonaffine piecewise function

\[
m(z)=
\begin{cases}
z/4,&0\le z\le1,\\
3z/4-1/2,&1\le z\le2.
\end{cases}
\]

It is source-compatible on every fiber and also has global radius `1/4`.
In contrast, any **affine** decoder constrained to return a compatible
target at every observation must pass through the two singleton endpoints,
so it must be `g(z)=z/2`. Its error at `(1,0)` is `1/2`. Thus requiring
both affinity and scalar source compatibility can double the best global
radius even for this compact convex polytope.

For general convex scalar fibers, projecting a globally optimal affine
output onto the attainable interval cannot increase any target error. It
therefore produces an optimal compatible scalar output, but may destroy
affinity. Choosing the fiber midpoint is another compatible optimum.

### Removing convexity defeats unrestricted affine optimality

Keep only the three points in (A5), without their convex hull. Their
observations are distinct, so an unrestricted decoder recovers each target
exactly and has radius zero. An affine decoder still has best radius
`1/4`. To see the lower bound, error at most r implies
`g(0)>=-r`, `g(2)>=1-r`, and `g(1)<=r`. Affinity gives
`g(1)=(g(0)+g(2))/2>=1/2-r`, forcing `r>=1/4`.
The same `z/2-1/4` decoder attains it. Convexifying the source added the
indistinguishable pairs which made the positive theorem true.

### The finite-vector sup-norm extension is positive

For a fixed finite target matrix C and unrestricted vector output,

\[
\inf_g\sup_{x\in K}\|Cx-g(Nx)\|_\infty
=\max_j R_j,
\]

where `R_j` is the scalar radius for row j. Every vector decoder is bounded
below by each scalar optimum. Conversely choose an optimal affine decoder
for each row; stacking them gives one affine vector decoder with error
`max_j R_j`. Equivalently this radius is

\[
\frac12\max_{\substack{x,x'\in K\\Nx=Nx'}}
                \|C(x-x')\|_\infty.
\]

This makes no guarantee that the vector lies in `C(K intersect N^{-1}{z})`.
The inherited example `K=Delta_3, N=0, C=I` still has unrestricted radius
`1/2` and compatible-law radius `2/3`. Other norms are outside this
coordinatewise proof. Similarly, eliminating alpha and permitting only
strictly linear decoders changes the theorem: with `N=0` and target range
`[0,1]`, output zero has radius one, whereas the affine constant `1/2`
has radius `1/2`.

## 5. Three affine decoders attain the exact L_delta radius

Retain the existing assumptions exactly:

\[
p\in\Delta_3,\quad \delta>0,\quad\epsilon\ge0,\qquad
z=L_\delta p+e,\quad |e_1|,|e_2|\le\epsilon,
\quad
L_\delta=\begin{bmatrix}0&1&1\\0&1&1+\delta\end{bmatrix}.
\]

The entire product of laws and box errors is admissible. The target is
`p_3`, the loss of the decoder is scalar absolute error, and delta and
epsilon are known when selecting the decoder.

| Decoder | Exact error expression | Exact global worst error |
|---|---|---|
| `g_0(z)=1/2` | `1/2-p_3` | `R_0=1/2` |
| `g_1(z)=(z_2-z_1)/delta` | `(e_2-e_1)/delta` | `R_1=2 epsilon/delta` |
| `g_2(z)=(z_2-1/2)/(1+delta)` | `(p_2-1/2+e_2)/(1+delta)` | `R_2=(1/2+epsilon)/(1+delta)` |

All bounds are attained. For `g_0`, use `p_3=0` or 1. For `g_1`, use
oppositely signed extreme errors, with any law. For `g_2`, use `p_2=1`
and `e_2=epsilon`, or `p_2=0` and `e_2=-epsilon`. These are permitted
closed-simplex laws and box errors. In particular, the third bound uses
the actual restriction `0<=p_2<=1`; it is an ordinary affine recovery
construction exploiting the known source constraints.

Select one decoder using the known parameter regime:

| Range | Globally optimal choice | Radius |
|---|---|---|
| `0 <= epsilon <= delta/[2(delta+2)]` | `g_1` | `2 epsilon/delta` |
| `delta/[2(delta+2)] <= epsilon <= delta/2` | `g_2` | `(1/2+epsilon)/(1+delta)` |
| `epsilon >= delta/2` | `g_0` | `1/2` |

At a boundary either neighboring decoder is optimal. The selection is made
from delta and epsilon, rather than by taking a pointwise minimum of decoder
outputs. The resulting fixed decoder for that experiment is affine.

The best of the three bounds is

\[
\min(R_0,R_1,R_2)
=\frac12\min\left\{1,\frac{4\epsilon}{\delta},
                         \frac{1+2\epsilon}{1+\delta}\right\}.
\tag{A6}
\]

### Explicit matching lower bound, including probability positivity

For completeness, put `a=2 epsilon` and

\[
D=\min\{1,2a/\delta,(1+a)/(1+\delta)\},\qquad
t=\min(0,a-\delta D),
\]

and choose

\[
q=(0,1,0),\qquad p=(-t,1-D+t,D).
\]

If `delta D<=a`, then `t=0` and all probabilities are nonnegative.
Otherwise `t=a-delta D`; the bound `(1+delta)D<=1+a` ensures the
second probability is nonnegative, and `delta D<=2a` ensures `t>=-a`.
In both cases `|t|<=a` and `|t+delta D|<=a`. Their common observation

\[
z=\frac{L_\delta p+L_\delta q}{2}
 =\left(1+\frac t2,\ 1+\frac{t+\delta D}{2}\right)
\]

uses opposite box errors of size at most epsilon for the two laws. Their
target separation is D, so every decoder incurs worst error at least
`D/2`. This matches (A6), and is the same reconstruction already documented
in `noise_conditioning_case.md` §3. All points are rational when delta and
epsilon are rational.

For example, `delta=2`, `epsilon=2/5` selects
`g_2(z)=(z_2-1/2)/3` with radius `3/10`. The laws
`q=(0,1,0)` and `p=(2/5,0,3/5)` share observation `(4/5,7/5)`;
the decoder returns `3/10`, the midpoint of their target values. This
attains the stronger ordinary baseline than the difference-inversion bound
`2 epsilon/delta=2/5`.

### Global optimality still does not make this decoder a fiber midpoint

With the same `delta=2`, `epsilon=2/5`, the feasible observation `z=(0,0)`
has target interval `[0,2/15]`. Its pointwise optimal output and radius
are both `1/15`. Yet the globally optimal affine `g_2` returns `-1/6`.
Its worst error on that fiber is `2/15+1/6=3/10`, the correct global
radius, but larger than the pointwise optimum. Clipping its output merely
to `[0,1]` returns zero here and improves that error to `2/15`, which
still is not pointwise optimal.

All targets lie in `[0,1]`, so clipping any of these affine decoders to
that interval cannot increase its errors; this recovers the same best
global radius if a valid probability output is required. The clipped
function need not be affine. Requiring compatibility with the complete
observed fiber instead calls for its attainable interval, as in §4.

At epsilon zero, `g_1` is exact. At delta zero, `g_1` and (A6) are
undefined; the two distinct laws `e_2,e_3` have the same exact observation
and force radius `1/2`, attained by `g_0`, even with zero error. If only
strictly positive laws are admitted, the same positive-delta radii hold
as suprema by approaching the boundary witnesses; closed-source attainment
must then not be claimed. Unknown parameters or a different admissible
error mechanism require a new source contract before using the regime table.

## 6. Comparison and integration judgment

The sharp radius calculation should be compared with the **best affine
recovery using the known convex probability and error constraints**. In this
case that baseline attains the same global number. Comparing only with the
raw difference inverse plus a constant cap is too weak: it omits `g_2`,
which exactly achieves the middle regime.

Pointwise intervals and compatible-source certificates remain useful. They
can give a smaller error for the realized observation, exhibit infeasible
records, preserve a requested physical interpretation, or support multiple
services under an explicit contract. Their usefulness does not establish a
strictly better global unrestricted scalar minimax radius than optimal
ordinary affine recovery under these premises.

The LP proof, the compact-convex extension, and the three explicit decoders
are classified here as ordinary reconstruction and illustrative adaptation.
No worldwide priority, new optimal-recovery theory, new computational-rate
claim, or automatic support for P3-N01 follows. Native admissibility,
coefficient access and cost must still be checked under their own contracts.
