# F08 hostile boundary audit: what a conversion does and does not preserve

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
Status: same-assistant derivation/reconstruction. The hypothetical rule below
is studied as an optional obstruction test; it is **not** added to the kernel.

## 1. Forward conversion can gain access to evidence

Let Phi:u->v be a declared positive conversion path of factor k. Then
`A(u) subset A(v)`, so the v-reduct retains at least the u-reduct's rows.
For any fixed u-valued pair t,s,

    B_native,v(Phi(t),Phi(s)) <= k*B_native,u(t,s).

The statement includes the possibility that the right side is infinite.
When both are finite it follows directly from inclusion of the reduct model
sets and Phi's numerical scaling. Native conversion supplies the corresponding
proof-level upper bound, but extra evidence in v can improve it strictly.
This is why simply converting a numerical answer need not give the optimal
answer to the newly typed request.

If a return path Psi:v->u of factor l exists, both ancestor sets coincide.
The optimal bound then scales exactly by k. At proof level, convert a v proof
through Psi, scale by 1/(l*k), and rewrite `Psi(Phi(t))` and `Psi(Phi(s))` by
their exact collected forms. This recovers the original pair and budget.
The factors need not be reciprocal: division compensates for their declared
product, without asserting that the path's physical meaning is an identity.

**Corollary U15 (uniform native reflection through a path).** Fix a signature
and a path Phi:u->v. The implication

    K_C(Phi(t),Phi(s);k*b) => K_C(t,s;b)

holds for every admitted context and every unit-u query iff either v reaches u
or there is no declared source whose unit reaches u.

A return path gives the explicit construction above. If no source reaches u,
every closed u expression reduces to a rational constant after lexical
expansion; a valid bound has a native constant proof. Conversely, let x:a be
an existing source that reaches u by a path Theta of factor p, and suppose v
does not reach u. Put the single row `Phi(Theta(x))<=-k*p` in v and witness it
with x=-1. The v comparison has its native row proof. Its requested u inverse
has budget -p, but the u-reduct has no row and x=0 violates it. U1's necessity
direction excludes the inverse proof. Other source coordinates can be zero.

Consequently semantically equivalent full contexts can have different native
theories. Replacing an accessible row by its positive one-way converted copy
preserves its numerical models, but may remove the native evidence needed for
a lower-unit query. Keeping the original row alongside its copy avoids that
particular loss. This is a property of the present typed rules, not a failure
of their soundness.

## 2. A tempting repair is insufficient in general

One possible future rule would reflect an inequality through an existing
conversion without adding a new inverse term constructor:

    from convert_c(a) <=[b] convert_c(d)
    infer a <=[b/k_c] d.                             (REF)

REF is sound for F05's exact positive numerical conversions. The first
one-way-row counterexample would be repaired by it after an exact rewrite of
the target-unit constant. Nevertheless, merely adding REF to the current
native rules would not give full-source completeness on every unit graph.
The following example and rule invariant show why. No code change is proposed
or accepted by this note.

### 2.1 A three-row joint constraint

Use six units X,Y,Z,A,B,C and three declared sources x:X, y:Y, z:Z. There are
factor-one conversions X->A, Y->A, Y->B, Z->B, X->C and Z->C, and no others.
Subscripts below denote those explicit converted terms. In a single live
source case take

    x_A+y_A <= 0_A,
    -y_B+z_B <= 0_B,
    x_C-z_C <= -1_C.                                (J)

The joint rational assignment (x,y,z)=(-1,0,0) witnesses feasibility. In F05's
shared numerical semantics, adding the three inequalities gives `2*x<=-1`.
The exact optimum of the X query x is -1/2, attained at (-1/2,1/2,1/2).
Every x<=-1/2 has a joint lift by choosing y=z=-x.

Each row alone, however, projects onto the whole line for each of its two
source coordinates. The pairwise restrictions cannot be combined in any of
the three sink units by a conversion path.

### 2.2 An auxiliary interpretation validates the rules plus REF

This is a proof invariant for nonderivability, not a replacement for F05's
intended shared-source semantics. Give X,Y,Z the carriers of finite-valued
functions on their respective real lines. Give A,B,C the carriers of functions
on the respective domains

    D_A={(x,y):x+y<=0},
    D_B={(y,z):-y+z<=0},
    D_C={(x,z):x-z<=-1}.

Use pointwise rational arithmetic, min, max and residual, and constant
functions for literals. Interpret x,y,z as identity functions in their own
source carriers. Each conversion pulls a function back along the corresponding
coordinate projection. Every projection is surjective:

* in D_A choose the other coordinate as the negative of the given one;
* in D_B choose y=z;
* in D_C choose z=x+1, or x=z-1.

Thus each conversion preserves the pointwise operations and preserves **and
reflects** order. REF is valid, as are the native conversion and rational-scale
rules. The remaining order/lattice/affine constructors are valid pointwise.
The exact normalizer identities remain valid: a closed term in a source unit
uses its coordinate, and one in a sink unit is its collected expression in
that sink's two coordinates. Lexical substitution is ordinary typed functional
substitution; unused foreign bindings do not change a closed result. This
validates normalization rather than assuming numerical agreement from samples.

The case is single, so all_cases adds no cross-domain information. Every J
source row holds in its respective carrier by definition. The context's joint
feasibility witness remains a valid admission witness, but no inference rule
extracts additional numerical premises from that witness.

The X conclusion `x<=[-1/2]0_X` fails in the source carrier at x=0. Induction
over any finite proof therefore excludes a derivation using the native rules
plus REF, although the conclusion is valid in the intended shared-source
semantics. This demonstrates a joint-information obstruction beyond the first
one-way inversion example.

Adding actual conversion paths that make every relevant unit reach the query
unit is one sufficient solution by U7/U8. Another possible future design is a
checked rule for joint affine elimination across units. Those choices have
different semantic and implementation commitments. A future repair should
state which one it adopts and preserve this counterexample; REF alone is not
a universal completeness repair.

### 2.3 A smaller four-unit witness found during reconstruction

The same obstruction already occurs with units X,Y,A,B, sources x:X,y:Y,
factor-one conversions from each source unit to each sink, and just two rows:

    x_A+y_A<=0_A,       x_B-y_B<=-1_B.

The source is feasible at (-1,0). Its full shared-coordinate semantics implies
2*x<=-1, attained at (x,y)=(-1/2,1/2). More generally every x<=-1/2 lifts with
y=-x. Yet each individual row projects onto the whole X and whole Y line.

Use functions on R for X,Y, functions on `D_A={x+y<=0}` for A, and functions
on `D_B={x-y<=-1}` for B. Both coordinate projections from D_A are surjective
by taking the other coordinate to be its negative. For D_B, take y=x+1 when
x is fixed, or x=y-1 when y is fixed. Thus all four conversion pullbacks are
order embeddings and validate REF. Both source rows hold pointwise in their
own sink carrier, while x<=-1/2 still fails in X at x=0.

At x=0 the separate lifts use y=0 in A and y=1 in B. No common y satisfies
both rows. Individual order reflection cannot supply the missing common lift.
This gives a smaller witness to the same claim; no minimality over every
possible signature is asserted. The three-row example above remains valid.

For completeness of this rule invariant, group all sixteen native tags.
Constant and rewrite preserve equality because within each target carrier
the collected form denotes its actual pointwise expression; sink expressions
use that sink's two coordinate projections. Lexical substitution is pure and
typed, including unused foreign bindings. Row introduction uses the two
displayed valid sink inequalities. Transitivity, addition, nonnegative scale,
reversed negation and slack are pointwise real inequalities. meet_proofs uses
the minimum of two valid bounds for one difference. max_common, min_common,
lattice and min/max congruence are the pointwise lattice inequalities with
their displayed maximum budgets. Residual congruence follows from
`ReLU(a)-ReLU(b)<=max(a-b,0)` at each point and uses its specified clipped
sum of premise budgets. Conversion is a constant-preserving pullback, and
all_cases has exactly the one case. REF follows from the explicitly proved
surjectivity. This covers normalization and every rule, rather than merely
checking that the source rows are satisfiable in some unrelated structure.

## 3. Assumptions that carry real mathematical work

| Assumption | Explicit failure outside it | Consequence for F08 |
|---|---|---|
| Finitely many closed source cases | The infinite family x=-1/n has x<0 everywhere but supremum 0, unattained. The open source x<0 has the same issue. | Strict pointwise validity need not give a strict uniform rational budget; U5 uses finite closed polyhedral structure. |
| Rational coefficients | A source upper endpoint sqrt(2), if admitted in an extended language, need not have a rational attaining budget. | U4's rational optimum is not a claim about arbitrary real parameters. |
| Fixed row directions for replay | The family a*x<=1, a>0, has optimum 1/a. Changing a changes the matrix, not merely the normalized RHS. | K.replay correctly rejects that structural change; U11 does not assert a fixed CPWA budget program in a. |
| Finite CPWA query and current budget grammar | Admitting a squared query on 0<=x<=eta would give optimum eta^2. A finite min/max/affine budget program cannot equal it on an interval. | Extending the query language requires a new uniform-replay argument or richer budget operations. |
| Positive nonzero conversion factors | A zero factor destroys the source coordinate; a negative factor reverses inequality direction. | Retyping by 1/k and the current native convert rule cannot be generalized by retaining the same unit graph alone. |
| Each source case is feasible | Contradictory inaccessible rows would make full-source validity vacuous while a reduct could remain unconstrained. | The original rational witness and the live-parent condition are essential; no vacuous empty case is silently admitted. |
| Fixed report-control law | Changing a report can change the branch law or observation process, rather than just substitute a constant into R. | U14 characterizes its supplied fixed law and does not validate the new empirical interpretation. |
| All point values finite | An extended-infinite common baseline can make z-z undefined. | Cancellation and exact normalization concern finite assignments even when their supremum is infinite. |

These are boundaries of the proved claims, not permanent prohibitions on later
research. The matrix/query examples identify concrete optional continuations;
none is smuggled into the current native checker or declared solved by the
finite fixtures.
