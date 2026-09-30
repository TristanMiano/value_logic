# F09 optional extension — constructive affine certificate transport

Research contributor: **Codex (GPT-6)**. September 30, 2026 UTC.
Status: paper construction and same-assistant rule audit. The general compiler
described here is **not implemented or machine-checked**. The executable
`uniform_scale_proof` retains its common-positive-scale contract.

## S8. Statement and boundary

Let H be the positive rational, unit-specific affine presentation of S2:
`h_v(x)=a_v*x+c_v`, with `a_v>0`. Change sources, rows, witnesses, literals and
operation macros as specified there, retaining every source case and conversion
edge and setting each conversion factor to `k'=a_w*k/a_v`.

Given a checked F06 native proof in C with literal root

    t <=[b] s : u,

there is a finite, explicit reconstruction using the existing native rules in
H(C), with literal root

    H_u(t) <=[a_u*b] H_u(s) : u.

The construction below needs only that supplied proof, finite forward paths in
the existing conversion graph, rational arithmetic and syntax manipulation.
It does not search for a new semantic proof, introduce source cases, discard
infeasible cases, add a reverse conversion, or invoke REF. Proof size and
execution efficiency are not bounded here. The converse follows by using the
inverse positive affine presentation. This strengthens S2's consequence
isomorphism with a paper certificate-construction argument; it does not enlarge
the implemented compiler's tested contract.

The obstacle is real: the native normalizer does not itself distribute unit
conversions, scaling or translations through arbitrary lattice nodes. S1/S2's
failed blind trace maps remain counterexamples to that simpler algorithm.

## 1. Scope and forward paths

First check the entire supplied proof, then keep the root's ancestors. Every
ancestor comparison's unit v has a forward path to root unit u. All rule
dependencies preserve units except the named forward conversion rule; tracing
dependencies to the root therefore supplies such a path. `all_cases` changes
case scope, not the comparison unit.

Every source occurring in the collected normal form of a closed v-term has a
forward path to v. One may first expand its finite lexical lets with
capture-avoiding substitution. Unused bindings disappear from the normal form;
their types were nevertheless checked in the original term. No path is needed
for a foreign source that occurs only in such an unused binding. Do not infer
unit reachability from all raw source occurrences before this distinction.

Choose one forward path for every source/unit pair used below. Choices are
fixed for the whole reconstruction, independently of case. For an old path p
from v to w with positive gain K, its new gain telescopes to
`K'=(a_w/a_v)*K`. This equation does not assume that different paths or cycles
have equal gains. Paths may be empty, in which case K=1.

Define a numerical retyping macro in the new signature:

    E_vw(z) = (1/K)*P'_p(z) + c_w - (a_w/a_v)*c_v.

Its order multiplier is `a_w/a_v`: a proof `z <=[d] z'` in v can be passed
forward along p, scaled by 1/K and translated by the displayed common constant
to give `E_vw(z) <=[(a_w/a_v)*d] E_vw(z')` in w. This uses only positive native
proof scaling. Multiplication by 1/K is an ordinary scalar in w, not a unit
conversion in reverse.

## 2. A canonical root-unit form

The actual `_form` normalizer collects a rational linear combination of source
atoms and recursively nested min/max atoms, plus a constant. It expands
`res(A,B)` to `max(B-A,0)` and instantiates lexical lets. This is a syntactic
collected form, not a complete semantic normal form.

For a source x declared in w and a chosen old path w->v of gain K, put

    Y_x^v = (1/K)*P'_p(src(x)) + c_v - (a_v/a_w)*c_w.

On the changed source coordinate `y_x=a_w*x+c_w`, this has value `a_v*x+c_v`.
Different path choices give the same collected affine form after the displayed
normalization of the path gain. Each leaf is well typed in v.

Reify an old form F as a new, residual-free term C_v(F):

* A source atom x becomes Y_x^v.
* An atom `min(F,G)` or `max(F,G)` becomes the same lattice operation applied
  to C_v(F) and C_v(G).
* For a collected form `F=sum_i r_i*A_i+q`, use

      C_v(F)=sum_i r_i*C_v(A_i)+a_v*q+(1-sum_i r_i)*c_v.

Use fixed ordering and parenthesization, including an explicit convention for
the empty sum. All coefficients and constants are rational. A negative term
coefficient is allowed by the existing term grammar.

The native normalizer recognizes the following affine collection identities:

    C_v(F+G) = C_v(F)+C_v(G)-c_v,
    C_v(r*F) = r*C_v(F)+(1-r)*c_v,
    C_v(q)   = a_v*q+c_v.

More precisely, the collected form of `C_v(F)-C_v(G)` depends linearly on the
old form difference F-G: map each old atom A to the new collected form of
`C_v(A)-c_v`, and each old constant q to `a_v*q`. Thus every old recognized
**difference equality** remains a recognized difference equality after C_v.
This matters because F06 permits a rewritten expression pair on every rule
step, not only on a step explicitly named `rewrite`.

This preservation argument needs no injectivity of the atom map. If new atoms
happen to collect together, equal old differences still give equal new ones.
When old min/max children are both constants, the old normalizer folds them;
positive a_v ensures that applying C_v before or after this fold gives the same
new constant. Other lattice identities need explicit proofs below.

## 3. Native affine lattice equalities

For terms A,B in one unit and `h(z)=lambda*z+q`, `lambda>0`, both directions of

    h(max(A,B)) = max(h(A),h(B))

have zero-budget native proofs. To derive the right side <= left side, lift the
two lattice injections through positive scale lambda and common addition q,
then use `max_common`. For the other direction, write
`M=max(h(A),h(B))`. Lift `h(A)<=M` and `h(B)<=M` through the same-unit affine
map `h_inverse(z)=(z-q)/lambda`. After recognized affine rewrites and
`max_common`, obtain `max(A,B)<=h_inverse(M)`; lift through h and rewrite its
composition with h_inverse. All budgets remain zero. The min proof is the
dual argument with projections and `min_common`.

The same-unit inverse here consists of a positive rational scale and a literal
translation. It adds no edge to the conversion graph. For a forward path P,
use the existing F08 `lattice_path_equivalence` construction for

    P(min/max(A,B)) = min/max(P(A),P(B)).

That construction already proves both directions without an inverse edge. In
combination with the same-unit lemma it supplies the corresponding equality
for E_vw.

Induction on F now supplies zero-budget proofs of

    E_vw(C_v(F)) = C_w(F).                         (compatibility)

The source case is a collected affine identity between the two normalized
forward-path expressions. Constants give `a_w*q+c_w`. For a lattice atom,
distribute E using the preceding proofs, then apply the child equalities by
congruence. For an outer rational linear combination, collect the constants
and use the child equalities. If a coefficient is negative, exchange the two
directions of the zero equality, negate and scale by its absolute value. This
does not use a negative proof-scaling rule. Both directions are built together.

## 4. Bridge from the actual presentation macros

For every closed original v-term t, construct two zero-budget native proofs

    H_v(t) = C_v(_form_old(t)).                    (endpoint bridge)

The finite let expansion preserves both original and translated collected
forms. Sources and literals are the definitions above (the same-unit source
path may be empty). Addition and signed term scaling use child equalities and
the collected identities of section 2. Min/max use congruence and the positive
constant-folding observation.

For residuals, the translated macro is

    c_v + max(H_v(B)-H_v(A),0).

After applying the child bridges, the same-unit translation/max lemma gives

    max(C_v(F_B)-C_v(F_A)+c_v,c_v),

which is exactly C_v of the old expanded residual form. The explicit lattice
lemma is essential: merely asserting a constant-rule equality would repeat
the offset counterexample from S2.

For an old conversion v->w of gain k, the translated term is

    P'(H_v(t)) + c_w - k'*c_v,
    k'=(a_w/a_v)*k.

Apply the child bridge, then compatibility for that single-edge path.
Multiplying `E_vw(C_v(F))=C_w(F)` by k and adding `(1-k)*c_w` yields precisely
the displayed translated conversion on one side and C_w(kF) on the other.
No unit-inverse rule is hidden in this step.

All bridge proofs must carry the case scope in which they are used. A row-free
proof can be reconstructed with that scope (or with global scope for a global
comparison); the checker forbids mixing local and global parents in an
ordinary rule. The construction does not copy a globally tagged helper into a
local proof without changing its tag and checking it.

## 5. Reconstruct the supplied proof in root unit u

For every retained old step with endpoints t,s, budget b and any unit v,
maintain a proof in u of the canonical pair

    C_u(_form_old(t)) <=[a_u*b] C_u(_form_old(s)).

All of its contributing source units reach u by section 1. Keep its original
local case or global scope. Build steps in dependency order, using the following
recipes. After every rule, use section 2's difference-preservation lemma to
rewrite to the **actual** old step's canonical pair; the old step may already
have used an implicit difference rewrite allowed by the checker.

| Old rule | Reconstruction and exact budget |
|---|---|
| constant | Old constant difference b maps to recognized difference a_u*b; emit a native constant step |
| rewrite | Recognized old difference equality is preserved by C_u |
| trans | Old middle-form equality is preserved; budgets add |
| add | Add canonical parent proofs and remove a common c_u by difference rewrite |
| scale r>=0 | Scale by r and insert the common correction `(1-r)*c_u` by rewrite |
| negate | Native negate exchanges endpoints; insert the common correction `2*c_u` |
| convert with old factor k | In root unit u, scale the canonical parent by k and use C_u(kF); budget a_u*k*b |
| slack delta | Add slack a_u*delta |
| meet_proofs | Keep both parent proofs; their canonical differences agree; `min(a_u*b,a_u*d)=a_u*min(b,d)` |
| max_common / min_common | C_u commutes with lattice formation; old common-term equality is preserved; maximum of budgets scales by a_u |
| congruence | Apply the same min/max congruence, with the positive constant-folding convention |
| lattice | Apply the corresponding injection/projection to the canonical children |
| all_cases | Retain every old case and its identical canonical literal pair; maximum of budgets scales by a_u |

Rows and residual congruence require the following expanded recipes.

**Row.** Let the original normalized row be `d<=b` in v, so the original actual
row difference is d-b. In H(C), a row leaf followed by its literal affine
offset recovers the changed actual row with budget zero, exactly as `_row_zero`
does for F09's point certificates. Add the literal `a_v*b` to its left side;
this changes the budget to `a_v*b` and its difference to `a_v*d`. A recognized
affine rewrite makes the pair `H_v(d), H_v(0)`. Use the endpoint bridge and
E_vu to obtain `C_u(_form(d)), C_u(0)` with budget a_u*b. The later difference
rewrite handles any alternative pair actually written on the old row step.
The old row's b is fixed proof data here; no claim about commutation with a
later RHS-revision replay is made.

**Residual congruence.** Suppose the two original parent comparisons are
`A<=[b0]B` and `C<=[b1]D`. Their canonical proofs imply, by negate and add,

    C_u(C)-C_u(B) <=[a_u*(b0+b1)] C_u(D)-C_u(A).

Translate both sides by c_u and use max congruence with the zero-budget identity
`c_u<=c_u`. The result is

    max(C_u(C)-C_u(B)+c_u,c_u)
        <=[a_u*max(b0+b1,0)]
    max(C_u(D)-C_u(A)+c_u,c_u).

These are C_u of `res(B,C)` and `res(A,D)`. This reproduces the exact signed
budget constructor, including a negative b0+b1 before truncation. Simply
applying the residual rule to the encoded children would miss the outer offset.

The native checker uses exact expression pairs in `all_cases`. Deterministic
canonicalization and fixed source paths give exactly the same pair for every
case, not merely semantically equivalent terms. Other rules that require
matching differences use the section 2 preservation property. Existing proof
minimum portfolios are retained; no winner is discarded by this construction.

## 6. Return the literal request; what remains optional

At the root, compose the bridge from H_u(t) to its canonical form, the rebuilt
comparison, and the reverse bridge from the canonical form of s to H_u(s).
Their zero allowances leave exactly a_u*b. Tag each step with H(C)'s fingerprint
and use the original root scope. This gives the literal translated request,
not merely a proof of an equivalent pair that a request receiver might reject.

For the converse, the inverse parameters are `a'_v=1/a_v` and
`c'_v=-c_v/a_v`, and the inverse conversion factors are the original ones.
Structural induction on the operation macros shows that H_inverse(H(t)) has
the original collected form. The outer affine corrections cancel in each
constructor; lattice children use the induction hypothesis. In particular,
the added residual origin cancels with the inverse residual origin and inverse
addition correction. Lexical scopes are retained. For rows, these are affine
identities, so the original context's row leaves supply the same normalized
directions and offsets. Use the original context identity and original row
indices when rebuilding the inverse proof, then rewrite its endpoints to the
original literal pair. One must not mistake a fresh presentation revision
string for the original context fingerprint without this reconstruction.

Every recursion above is on a finite term/form or on an earlier proof index.
Every selected path is finite. The result is consequently a finite native
proof. Let expansion and duplicated equality proofs can cause substantial
growth; there is no size, runtime, canonical-minimality or trace-replay theorem
in this note. It also does not cover decreasing affine presentations, which
have the separate pair-reversal semantics stated in S2.

The reasonable next executable boundary is a separate, checked producer for
this construction, with regressions for one-way edges, heterogeneous scales,
nonzero offsets, nested lattices/residuals, zero and negative term coefficients,
unused/shadowed lets, signed budgets, retained proof minima, and exact all-case
root pairs. It should be accepted only after the unchanged kernel and request
receiver check its output. That optional implementation is deferred; F09's
46 passing tests and eight saved certificates do not test this general recipe.

## 7. Hand reconstruction on a one-way conversion

These examples exercise the construction on paper; they are not extra saved
machine certificates. Let x have unit U and let the only conversion be
`p:U->V` with old gain 2. Set

    h_U(x)=3*x+5,       h_V(y)=2*y-7.

The new gain is 4/3 and the conversion macro's added V-literal is
`-7-(4/3)*5=-41/3`. There is no path V->U.

First take the source row x<=3. The original query

    p(res(1,x)) <=[4] 0 : V

is tight at x=3. The changed coordinate X satisfies X<=14. A native row
comparison with allowance zero rewrites to X-8<=6. Apply max congruence with
0<=0 and fold max(6,0); then compose with the constant comparison 6<=[6]0.
This gives `max(X-8,0)<=[6]0` in U. Convert forward to V, obtaining allowance
8. Add -7 to both sides. The translated literal left endpoint is

    p'(max(X-8,0)+5)-41/3,

whose collected form is `p'(max(X-8,0))-7`; the literal right endpoint is -7.
Thus the final rewrite gives exactly the requested translated pair, with
allowance 8=2*4. The changed witness X=14 attains that difference.

For a signed test, take instead x>=1 and the original query

    p(min(x,0)) <=[-2] p(x) : V.

The changed row is X>=8. The lattice projection `min(X,5)<=5`, followed by
the row-derived comparison `5<=[-3]X`, gives
`min(X,5)<=[-3]X` in U. Forward conversion and the common literal -41/3 give

    p'(min(X,5))-41/3 <=[-4] p'(X)-41/3 : V.

These are precisely the two translated endpoints, and -4=2*(-2) is attained
at X=8. The negative allowance is scaled, never clipped or replaced by a
positive tolerance. The root-unit source coordinate here is

    Y_x^V=(1/2)*p'(X)-31/3.

The canonical left endpoint is `2*min(Y_x^V,-7)+7`; compatibility and the
affine lattice lemma connect it to the displayed translated left endpoint.
This is exactly the sort of equality that the general reconstruction proves
explicitly instead of assuming the constant-rule normalizer recognizes it.
