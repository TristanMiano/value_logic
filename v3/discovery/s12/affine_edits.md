# Affine sources: observations cannot help translations, but can enable erasure

Codex (GPT-6), s12. DEVELOPMENT derivation. Links S04/S19/S32 and the
[binary-clause compiler](permission_compiler.md). All arithmetic here is GF(2).

## The entire unary-map menu has a linear description

Every coordinatewise Boolean map has the form y_i=d_i*x_i+c_i. Thus d_i=1
means retain/toggle and d_i=0 means overwrite with c_i. Let the nonempty
source after receipt h be x_h+V_h, with basis v_1,...,v_k. Let the target be
A*y=b, where A has r rows. The map is universally valid exactly when

```math
A\mathrm{diag}(d)v_j=0\quad(1\le j\le k),\qquad
A\mathrm{diag}(d)x_h+A c=b.
```

Necessity follows by testing x_h and x_h+v_j. Sufficiency follows by writing
every source world as x_h plus a linear combination of those basis vectors.
For a target row a, the corresponding equations are
(a componentwise-times v_j) dot d=0 and
(a componentwise-times x_h) dot d+a dot c=b_a. They are linear in the 2n
action bits, with at most r(k+1) rows before ordinary elimination. A consistent
system reduces to at most 2n independent rows. Source/target preparation and
all elimination work must still be charged. Arbitrary operation restrictions
and nonlinear per-operation objectives can destroy this tractability.

The homogeneous part is an established **code conductor**:

```math
d\in\mathrm{Cond}(V_h,\ker A)
       =(V_h*(\ker A)^\perp)^\perp.
```

Here * is the span of coordinatewise products. The identity follows directly
by expanding a dot (d*v)=(a*v) dot d. Code conductors and stabilizing algebras
are existing coding-theory objects; this session adapts them to an observed
configuration and an operation menu. See [literature](literature.md).

For one new informative coordinate observation x_i=a, choose a basis vector
w with w_i=1. Replace x_h by x_h+(a+x_(h,i))*w and every other basis vector v
by v+v_i*w, then remove w. This supplies an explicit exact update. It may
change many displayed equations, so do not claim the binary-source compiler's
linear total update bound here. The permitted action set nevertheless expands
under consistent receipts: each new source is a subset of the old source.

## Why XOR patches are a different case

Suppose every initially possible x already satisfies the same affine target
A*x=b, and the only operation is y=x+delta. For every nonempty receipt source,

```math
\forall x\in F_h:\ A(x+\delta)=b
\quad\Longleftrightarrow\quad A\delta=0.
```

No observation can enable a previously forbidden translation. This statement
does not even require the initial source to be affine; its inclusion in the
affine target suffices. If the initial state may violate the target, observations
can instead reveal its syndrome, and this obstruction no longer applies.

## Erasure is controlled by a standard decomposition

For source and target C=ker A, erase coordinates outside S and retain those
in S. This map preserves every codeword iff C is the direct sum of its
subcodes supported on S and on its complement. One proof: if coordinate
projection preserves C, every v decomposes into its two projected codewords;
the converse is immediate. Equivalently,

```math
\mathrm{rank}(A_S)+\mathrm{rank}(A_{S^c})
       =\mathrm{rank}(A).
```

Indeed, nullity on both sides gives precisely the direct-sum dimension test.
These are separators of the column matroid. Retain/erase masks are constant
on the indecomposable support blocks; coordinates fixed to zero are irrelevant
to the actual output, though writing them may still have a charge. This is the
standard stabilizing-algebra decomposition, not a new matroid theorem.

After observing some coordinates to be zero, remove them and use the shortened
code ker A_U on the unobserved coordinates U. Its decomposition can be finer.
For nonzero receipts an offset condition also remains; decomposition of the
variation space alone is insufficient. The general equations above retain it.

## One observed bit, many selective erasures, many unresolved bits

Take m>=2 triangles arranged in a chain: triangle i has vertices
v_(i-1), w_i, v_i. Add a closing edge e from v_0 to v_m. There are 3m+1 edge
bits. A valid state is a binary circulation: an even number of selected incident
edges at every vertex. Its cycle space has dimension m+1.

An explicit parameterization uses local bits z_1,...,z_m and a coupling bit g:
both two-edge-path bits in triangle i equal z_i, its direct edge equals
z_i+g, and the closing edge equals g. These are all valid states; the displayed
independent parameters attain the cycle-space dimension.

Before observation, any universally safe retain/erase mask must be constant
on each triangle (test that triangle's circulation), and those constants must
equal the closing-edge mask (test the long circulation using the direct edges
and e). Hence only retaining everything or erasing everything is universally
safe. This describes the restricted retain/erase menu, not every unary map.

Observe e=0. The remaining m parameters z_i are still completely unresolved,
but each triangle is now a separate circulation. Any subset of whole triangles
may be erased while the rest are retained. There are **2^m distinct output
maps on the remaining source**, described using m independent choices. A
single bit observation has enabled selective transformations without learning
the values being retained. Counting writes to the already-known zero edge
as separate operational choices would artificially double this count.

A concrete duty is to clear one specified triangle and preserve all other
edge bits while keeping a valid circulation. Receipt e=0 certifies that action.
Receipt e=1 certifies that the same exact duty is impossible: clearing that
triangle removes the one unit of through-flow while the preserved incident
edges still require it. The value of the query is therefore both permission
and early rejection. A deployment claim needs a distribution or robust task
objective, real query/write costs, and a legitimate fallback.

Ordinary cycle-space analysis and code-conductor computation give the same
answer. The adapter clarifies which operation interfaces can exploit a partial
receipt; it establishes no performance advantage over those methods. No
application workload or independent confirmation is supplied yet.

The [small exact screen](affine_probe.py) ran successfully; [saved output](affine_probe.json)
records the source hash and runtime. It compared 192,936 compiled unary-map
decisions with direct execution over compatible worlds from 64 fixtures,
including 1,098 consistent receipts and 822 contradictions. Another 13,532
checks covered the translation boundary. The circulation family at m=2,3,4
passed 18,688 erasure checks: its menu went from 2 maps to 4,8,16 respectively
after the specified zero receipt, while 4,8,16 source worlds remained. The
one-receipt impossibility for clearing the first triangle was also checked.
These are finite semantic diagnostics, not measured economic improvements.
