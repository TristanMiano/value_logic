# F09 optional reconstruction E — optimal nonlinear budget maps

Research contributor: **Codex (GPT-6)**. September 30, 2026 UTC.
This addresses the positive alternative left by S3's affine rigidity theorem:
nonlinear recoding can have a sharp **sound** budget map even when no exact
base-independent equivalence exists. The source/typing boundary is separate.

## 1. The least sound uniform map of signed budgets

Let h:R->R be increasing. For each real b define the extended quantity

    Omega_h(b)=sup_x (h(x+b)−h(x)).

If this is finite, it is the least numerical upper bound such that

    t−s<=b implies h(t)−h(s)<=Omega_h(b)

for every pair t,s. Indeed t<=s+b, so monotonicity gives the bound, while the
pairs (s+b,s) range over every increment in the supremum. This proves both
soundness and leastness; no assertion that the supremum is attained is needed.

**S7 (signed increment modulus).** Omega_h is nondecreasing, Omega_h(0)=0,
and is subadditive wherever the displayed extended sums are defined:

    Omega_h(b+c)<=Omega_h(b)+Omega_h(c).

For the last statement, split an increment at x+c:

    h(x+b+c)−h(x)
      =[h(x+c+b)−h(x+c)]+[h(x+c)−h(x)].

Bound each bracket and take the supremum. Thus independently transformed
premise budgets can be added soundly, but the sum can be looser than transforming
the total old budget once. Exact cancellation of opposite signed budgets is
not generally preserved.

This is a statement about numerical bounds. It does **not** identify
h(t_1+t_2) with h(t_1)+h(t_2), or license an unchanged native add instruction
after nonlinear recoding. A term/presentation translation still needs the
transported operation or a separately justified comparison between those terms.

For d>0 one has

    Omega_h(−d)=−inf_x (h(x+d)−h(x)).

If h is bounded above on a positive ray, the infimum over the whole line is
zero by S6's telescoping argument and nonnegativity, hence Omega_h(−d)=0.
By contrast, a global positive lower secant bound m gives Omega_h(−d)<=−m*d.
This identifies the specific information a negative improvement certificate
needs under nonlinear recoding.

If every increment is independent of its base, Omega_h(b)=−Omega_h(−b) for all b.
Conversely this equality makes the supremum and infimum of each positive-length
increment equal, so every increment is base-independent. For strictly increasing
h, these increments give the exact comparison contract of S3, hence
h(x)=a*x+c. This is the precise sense in which an
exact signed additive budget representation is rigid. A merely sound
subadditive budget transfer has more freedom.

## 2. Finite CPWA recodings have an explicit exact modulus

Suppose h is finite rational CPWA and increasing on R, with finite breakpoints
c_1,...,c_k and left/right tail slopes a_-,a_+. For fixed b, the increment as a
function of x is piecewise affine with breakpoints among c_i and c_i−b. On
each bounded interval its maximum occurs at an endpoint; on either unbounded
tail it is the constant a_-*b or a_+*b. Therefore

    Omega_h(b)=max{
      a_-*b, a_+*b,
      h(c_i+b)−h(c_i), h(c_i)−h(c_i−b) : i=1,...,k
    }.

For k=0 the two equal tail slopes supply the affine case. This formula is valid
for positive, zero and negative b. Each displayed function of b is finite
rational CPWA, so their maximum is too. The sharp signed budget map is therefore
itself representable as a native term in a **budget source coordinate**. A
judgment's literal numerical budget is still rational; a varying budget can be
represented in the compared terms with explicit source premises instead of
silently changing that interface.

Example: h(x)=x+min(max(x,0),1), with slope 2 only on [0,1] and slope 1 elsewhere.
For b>=0, the increment equals b plus the length of overlap of [x,x+b] with
[0,1]. The largest overlap is min(b,1). For b<=0, its largest value occurs
on a slope-one tail. Hence exactly

    Omega_h(b)=b+min(max(b,0),1).

A global upper-Lipschitz bound 2*b is sharp only for 0<=b<=1; it loses an
unbounded amount as b grows. The negative budget b remains b under the optimal
map, reflecting the global lower slope 1. This recoding is unbounded and differs
substantively from a saturating bounded presentation.

### 2.1 Composition of optimal maps can still lose source alignment

For increasing g,h with finite moduli,

    Omega_(h composed g)(b) <= Omega_h(Omega_g(b)).

Use the g-increment bound inside the h-bound. Equality need not hold because
the two separate suprema may require incompatible baselines.

Let g(x)=x+clip(x,0,1) and h(y)=y+clip(y−10,0,1), where clip(z,0,1) means
min(max(z,0),1). Their steep regions are separated: g has slope 2 on [0,1],
which it maps to [0,2], while h has slope 2 on [10,11]. The composition has
slope 2 on [0,1] and [9,10], and slope 1 elsewhere. For 0<=b<=1/2 its exact
modulus is 2*b, since its slopes are at most 2 and such an interval fits in
one steep region. But Omega_h(Omega_g(b))=4*b. At b=1/4 the exact answer is
1/2 and the separately composed bound is 1. This is a recoding version of the
project's shared-source lesson: exact marginal worst cases need not align.

## 3. A positive native alternative to bounded global recoding

Every globally strictly increasing finite rational CPWA h:R->R has positive
slopes on all nondegenerate pieces, including both tails. There are finitely
many, so their minimum m is positive and maximum L is finite. Its tail limits
are −infinity and +infinity; h is onto R. Inverting each affine piece gives a
finite rational CPWA inverse, and h is globally bi-Lipschitz with constants
m,L. This statement would be false for arbitrary strictly increasing smooth
functions with vanishing tail slopes; finiteness of the affine pieces matters.

For any nonempty domain where a paired loss difference has a finite attained
optimal bound B, applying h to both losses gives an optimum B' satisfying

    min(m*B,L*B) <= B' <= max(m*B,L*B).

The upper bound is S4. For the lower bound evaluate the recoded difference at
an old attaining point, using the opposite secant inequality for its sign.
At B=0 that point gives exactly zero, so B'=0. If the old supremum is
+infinity, the lower slope m forces the new one to be +infinity too. In the
finite CPWA source fragment this therefore preserves the sign of the optimal
budget and whether it is finite, while generally changing its exact magnitude.

For a **single-unit** source calculus, such h also gives an exact nonlinear
presentation if all operations and the query decoder are transported. Replace
each source by h^{-1}(y), compose each output with h, and replace arithmetic
by h(op(h^{-1}(arguments))). Terms remain finite rational CPWA. Partition each
source case by the finitely many inverse-affine coordinate pieces; after
substitution each piece has affine rational source rows. Discard empty pieces
and choose rational witnesses for the rest. Their union is exactly the image
of the old domain under the coordinate bijection. A comparison uses decoded
differences, so U1 (all rows accessible) gives an exact native consequence
equivalence. This is a presentation theorem with potentially many new cases,
not an implemented efficient compiler or an unchanged ordinary budget rule.

### 3.1 Why that construction was not generalized blindly to typed contexts

Case refinement can change a typed native reduct even when it preserves the
full semantic source set. Let x:U, a one-way conversion c:U->V of factor 1,
and one original case with rows

    x<=10_U,        convert_c(x)<=−1_V.

Its full source is x<=−1, while its U-reduct is x<=10. Refine the case by
the U-valued guards x<=0 and x>=0, then discard the second child as infeasible
using the V-valued row. The surviving context has the same full source, but
its U-reduct now includes x<=0. Consequently a native U proof of x<=0 exists
in the refined context and did not exist in the original. The reduct witness
x=1 separates them.

Thus “expand all nonlinear rows into feasible affine cases” is not automatically
a native equivalence in an arbitrary directed-unit signature. Guard placement,
infeasible-branch evidence and which rows a target can access must be tracked.
S1/S2 avoid this issue because rational affine coordinate changes keep the
original affine rows and case schema. The single-unit nonlinear result above
is retained; a general typed nonlinear presentation compiler is **not claimed**.
This is also why the existing native guard-discharge rules cannot be replaced
by an unrestricted semantic pruning shortcut.

### 3.2 A sufficient typed condition: every unit reaches the target

The counterexample does not prohibit every typed nonlinear presentation.
Fix a query unit u and assume **every unit in the signature has a forward path
to u**. The old target sees all rows. A refinement guard written in any source
unit also reaches u, so the new target will see all refined rows and guards.
This supplies a useful sufficient condition under which the single-unit
construction does extend to a typed context.

For each unit v choose a globally strictly increasing finite rational CPWA
bijection h_v with its finite CPWA inverse. Keep the original conversion graph
and its original positive factors as the raw native conversions. Encode each
source x:v by y_x=h_v(x). Translate terms by transported operations: a binary
v-operation becomes

    h_v(op(h_v_inverse(A),h_v_inverse(B))),

and a conversion c:v->w of original gain k becomes

    h_w(convert_c(h_v_inverse(A))).

Literals become h_v(q), and source references retain their names. All these
are existing term macros: a rational univariate CPWA function can be written
as an affine term plus a finite signed sum of hinges max(x-c,0). Signed term
coefficients are allowed. This choice of raw conversion factors differs from
S1's optimized affine gauge table; the surrounding decoders and encoders now
carry the numerical change.

Partition every source coordinate by the inverse function's affine pieces.
On each common coordinate piece, substitute the corresponding affine inverse
into each original row. The new row is affine and keeps its original row unit;
its source terms still have the required forward paths. Write each piece guard
in that coordinate's source unit. Keep exactly the feasible refined cases,
with rational witnesses. All coefficients and breakpoints are rational, and
the coordinate bijection guarantees that at least one refined case survives
each admitted original case. Shared boundary pieces may overlap; a finite
union does not require a disjoint partition.

The resulting full source is exactly the image of the old source. Because all
row and guard units reach u, this is also the complete source relevant to the
old and new u-reducts. By U1, for every old u-query t<=[b]s,

    C derives t<=[b]s
      iff
    C' derives h_u_inverse(H(t))<=[b]h_u_inverse(H(s)).

The explicit decoder in this statement is essential. It preserves the old
budget test; simply comparing H(t) to H(s) with an unchanged or universal exact
nonlinear budget map would repeat the overgeneralization excluded by S3.
For a strongly connected unit graph the reachability hypothesis holds for
every target, so this gives the decoded consequence equivalence in every unit.
For a one-way U->V graph it applies to V, while the preceding counterexample
shows why it cannot automatically be asserted for U.

This is a sufficient-condition theorem, not a necessary characterization of
all allowable typed refinements. It changes the case schema and transports
the operations, and is not an implemented producer. The finite-case expansion
may be large. The general directed-unit compiler remains unclaimed, while
S8 separately reconstructs the affine case without changing any cases.
