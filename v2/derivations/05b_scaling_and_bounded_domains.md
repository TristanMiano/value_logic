# F09 reconstruction B — scaling, offsets and bounded presentations

Research contributor: **Codex (GPT-6)**. September 30, 2026 UTC.
Companion to [F09](05_fragments_and_comparisons.md). These are elementary
reconstructions for the adopted calculus, not novelty claims. F02's
[recoding analysis](../foundations/02a_candidate_reconstruction.md#l-bounded-encodings-unbounded-values-and-a-positive-precision-repair)
already distinguishes exact bounded codes from finite precision and ordinary
code arithmetic. Here the native signed-budget and unit interfaces are fixed.

## 1. Positive unit scaling is an exact native isomorphism

For each unit u choose a positive rational a_u. A source x:u receives coordinate
y_x=a_u*x. Transform literals q:u to a_u*q:u and leave scalar coefficients
unchanged. For each named conversion c:v->u with old factor k_c, set

    k'_c=(a_u/a_v) k_c.

Keep source and conversion identities under an explicitly declared presentation
map. Transform every term recursively, retaining its constructors, let names
and lexical binding structure. Call the result T_a(t). Transform every source
row by applying T_a to both sides, and every witness by x->y. Keep the case
schema and observation; use a fresh revision/fingerprint and declared scope.
This is a coordinate presentation, not new evidence for a different task loss.

**S1 (typed scaling).** For every closed term t:u,

    [[T_a(t)]]_(a*x) = a_u [[t]]_x.

Structural proof: literals and source leaves establish the claim; addition,
rational scaling, min, max and residual are positively homogeneous. At a let,
extend the induction to a local environment whose v-valued bindings are scaled
by a_v. At a conversion, k'_c*a_v=a_u*k_c is the necessary commuting equation.
This also covers unused bindings and shadowing; all children remain typed.

The source coordinate map is an invertible rational linear map. Each transformed
case is exactly the image of its original rational polyhedron and has the
transformed feasible witness. The conversion graph is unchanged, so unit-reduct
formation commutes with the map. Therefore, for any rational b and target unit u,

    K_C(t,s;b) iff K_(T_a C)(T_a t,T_a s; a_u*b).

Apply F08 U1 on both sides and cancel the positive factor pointwise. Optimal
finite native budgets scale by a_u, as does an attaining source model; +infinity
remains +infinity. Full-source completeness conditions do not improve just
because the conversion factors changed: the directed access graph is the same.

For a **single common factor a across all units**, there is also a direct native
proof transformation. Recursively transform each step's terms and lattice data;
multiply its budget and slack data by a; retain nonnegative scale-rule
coefficients, parent references and case labels; replace context fingerprints.
Every rule's budget constructor is positive-homogeneous: sums, finite min/max,
and max(b_1+b_2,0). Conversion factors are unchanged. In the normalizer, source
coefficients are unchanged and literal offsets scale by a, recursively inside
each min/max atom. Recognized difference equalities and row normalization are
therefore preserved. The inverse scaling reconstructs the original terms and
budgets (with a fresh context record). This includes negative improvement budgets.

The corresponding **blind instruction map is false for different unit factors**.
With U->V->U factors both 1, the normalizer recognizes
`min(x,0_U) = back(min(out(x),0_V))` as a constant difference. Scale U by 1 and
V by 2, with new conversion factors 2 and 1/2. The two values are still equal,
but their normalized forms are now `min(x,0)` and `(1/2)*min(2*x,0)`, whose
equality the affine collector does not recognize without a lattice proof.
The saved F09 fixture checks this rejection and supplies the missing positive
path/min homomorphism proof using existing F08 macros. S1's general native
isomorphism is the U1 consequence argument above, not an unchanged serialized
instruction claim. The initial stronger compiler draft was narrowed on this
counterexample; no kernel rule was changed.

If conversion factors are left unchanged while a_v and a_u differ, the equation
fails. For example k=2, a_v=3, a_u=5, x=1: the expected encoded output is 10;
the unadjusted conversion applied to encoded input gives 6. The required factor
is 10/3. A new weighting of task costs is not justified as a change of units
unless its scope, rows and conversions satisfy the stated presentation contract.

## 2. Affine offsets require transported operations

Let h_u(x)=a_u*x+c_u with a_u>0 rational and c_u rational. The comparison of two
already evaluated outputs obeys

    h_u(t)−h_u(s)=a_u(t−s),

so a common offset disappears from a paired judgment. This does not mean that
one may translate every input/literal and keep the old arithmetic unchanged.
With y=h_u(x), z=h_u(w), conjugated operations are

    encoded(q)          = a_u*q+c_u
    y plus_h z          = y+z−c_u
    r times_h y         = r*y+(1−r)*c_u
    min_h(y,z)          = min(y,z)
    max_h(y,z)          = max(y,z)
    res_h(y,z)          = res(y,z)+c_u.

For conversion c:v->u, with k'_c=(a_u/a_v)k_c, use

    convert_h(y)=convert_(c,k'_c)(y)+c_u−k'_c*c_v.

Each displayed operation is a finite rational native macro. The encoded zero
is c_u; an encoded residual is >=c_u, not necessarily >=ordinary numerical zero.
Let/local bindings carry their unit-specific encoded environments as in S1.

**S2 (affine presentation).** Recursively applying these macros yields H(t)
with [[H(t)]]_(h*x)=h_u([[t]]_x). The proof substitutes the displayed identities
at each constructor. Transformed affine source rows stay affine, witnesses and
reducts correspond bijectively, and U1 yields the same budget equivalence as S1,
with a_u*b. Its proof-existence conclusion does not assert that naively relabeling
every native instruction is already the necessary macro-expanded proof.

There is an additional normalizer trap even for one common nonzero offset.
The old syntax `res(x,0)` and `max(−x,0)` has the same collected form. Under
h(x)=x+1, the displayed macro translations are `max(1−y,0)+1` and
`max(2−y,1)`. They are equal functions, but the normalizer does not distribute
the common translation through max. Choosing a different residual macro can
move this obligation to the residual-congruence instruction rather than remove
it. An affine lattice-homomorphism proof discharges the identity; a direct
trace relabeling has not been proved or implemented for arbitrary offsets.

Without corrections, addition alone forces c_u=0: h(x+y)=h(x)+h(y) would give
a(x+y)+c=a(x+y)+2c. Standard residual also forces h(0)=0 by evaluating it on
equal inputs. An unchanged linear conversion requires the additional equation
c_u=k'_c*c_v. Standard convex mixtures with weights summing to one, in contrast,
commute with an affine h: sum_i w_i h(x_i)=h(sum_i w_i x_i). The operation and
its coefficient mass matter; “affine invariance” without naming them is vague.

Simple witness: h(x)=x+1. Encoding 1+1 gives 3, while adding the two encoded
inputs gives 4. Encoding res(1,1)=0 gives 1, while the standard residual of
the encoded inputs gives 0. Final paired offsets cancel, but these compound
meanings do not.

### 2.1 Decreasing affine maps and degenerate maps

The positive sign is an order assumption, not a convention that may be dropped.
If h(x)=a*x+c with a<0, then the exact upper-bound translation is

    t−s<=b iff h(s)−h(t)<=|a|*b.

The expression pair must be reversed. Equivalently, the unreversed encoded
difference receives a **lower** bound a*b. This is an order dual, appropriate
only with an explicit change from smaller-is-better loss to the opposite value
orientation. The native negate rule already reverses the pair without changing
the budget, and positive scaling by |a| gives the displayed general law.

A decreasing h interchanges min and max. Its transported residual is
`c+min(h(b)−h(a),0)`, equivalently `c−res(h(b),h(a))`; it is not the unchanged
nonnegative residual. Named conversions themselves still require positive
factors in F05. An orientation reversal is not permission to put a negative
factor into that table. The implemented Presentation audit deliberately accepts
positive factors only; the duality law is a separate comparison statement.

For a=0 all values collapse to c. For example the false old inequality 1<=0
becomes c<=c, so reflection fails. More generally a nondecreasing but noninjective
map can preserve order without reflecting it: ReLU maps both −1 and −2 to zero.
Strictly increasing, decreasing, and merely nondecreasing transformations
therefore have different contracts.

All presentation coefficients here are fixed rational parameters, not unknown
source-dependent multipliers. Multiplication by a varying source is generally
outside finite CPWA syntax. A common source-dependent additive offset can
cancel from a paired query when it is itself a valid term, but that cancellation
does not establish an arbitrary state-dependent change-of-scale theorem.

## 3. What monotonicity alone preserves

Every nondecreasing h preserves finite min and max. If h is strictly increasing,
it also reflects order and equality, so t<=s and h(t)<=h(s) are equivalent at
each assignment and universally over a fixed domain. Such a map preserves a
zero-budget **output comparison**, even when h itself is not a native term.
It need not preserve additive composition, numerical differences, uniform
negative margins, rational CPWA syntax, source-case representation or the
native availability of a certificate.

For h(x)=x/(1+x) on nonnegative inputs, compare component losses

    A=(0,4), total 4;       B=(1,2), total 3.

Ordinary total loss prefers B. Summing the separately recoded components gives
4/5 for A and 1/2+2/3=7/6 for B, reversing the preference. Applying h once to
the totals would preserve their order. These are different operations.

**S3 (rigidity for the actual rational-budget interface).** Let h:R->R be
finite-valued. If there is a finite-valued function g:Q->R such that for all
real x,y and rational b,

    x−y<=b iff h(x)−h(y)<=g(b),

then h(x)=a*x+c with a>0, and g(b)=a*b. Conversely these functions satisfy the
equivalence. No continuity or monotonicity hypothesis is needed: the full
comparison contract forces both. Rational budgets already suffice.

Proof. At b=0 and x=y, g(0)>=0. At x>y, reflection gives
h(x)−h(y)>g(0)>=0, so h is strictly increasing. Write M=h(1)−h(0)>0. Partition
[0,1] into N equal subintervals. Each positive increment exceeds g(0), so
M>N*g(0) for every N; hence g(0)=0.

For n>=2 let m=floor(n/2). The m consecutive increments of length 2/n starting
at zero each exceed g(1/n), because 2/n>1/n. Thus

    0<=g(1/n)<M/m ->0.

Every positive increment of length at most 1/n is at most g(1/n) by the forward
comparison. Exchanging endpoints handles negative increments. This proves
uniform continuity of h directly, without a regularity theorem about monotone
functions.

Now put x=y+b to obtain h(y+b)−h(y)<=g(b). Put x=y+b+epsilon for epsilon>0;
the left side is false, so h(y+b+epsilon)−h(y)>g(b). Let epsilon decrease to
zero and use the just-proved continuity. The increment h(y+b)−h(y) equals g(b),
independently of y, for every rational b. At y=0, g(b)=h(b)−h(0). Two successive
rational increments give g(b+d)=g(b)+g(d), hence g(q)=q*g(1) on Q. Continuity
and rational approximation give h(x)=h(0)+x*g(1) on all of R. Strict increase
gives a=g(1)>0. The converse is cancellation of the common c.

If ordinary addition must also be preserved, c=0. If transformed budgets must
remain rational, a=g(1) is rational; preserving rational literals also requires
c=h(0) rational. The theorem
concerns **one common transformation of numerical budgets** over arbitrary
baselines, not a prohibition on domain-specific nonlinear error contracts or
encodings that preserve only selected tests. The first draft assumed continuity;
the self-review removed that unnecessary hypothesis by the partition argument.

### 3.1 A single nonzero threshold is rigid in the finite CPWA class

The all-rational-budget hypothesis in S3 can be weakened when h is already
known to be finite CPWA on the whole real line. Suppose there is just one
fixed nonzero d and one finite g for which, for every real x,y,

    x-y<=d  iff  h(x)-h(y)<=g.

At x=y+d the right inequality holds. At x=y+d+epsilon it fails for every
epsilon>0. Continuity therefore gives `h(y+d)-h(y)=g` for every y. Reversing
the increment if d<0, write e=abs(d)>0 and obtain a fixed positive-step
increment G. On the right affine tail of a finite CPWA h, this increment is
`G=a*e`, where a is the tail slope. For any x, choose an integer N large
enough that x+N*e is on that tail. Repeated increments then give

    h(x)=h(x+N*e)-N*G=a*x+c.

Substitution into the assumed equivalence forces a>0 (a=0 makes the right
test constant, and a<0 reverses the threshold). Thus one exact nonzero
threshold test over **all baselines** already forces a positive affine map in
this finite class. No monotonicity assumption was needed separately. If h is
rational CPWA and d is nonzero rational, g and the resulting affine parameters
are rational as well.

In fact the argument only needs continuity and an eventual affine right tail;
finite CPWA is the native fragment's sufficient hypothesis for those properties.

Both qualifications matter. At d=0, any strictly increasing finite CPWA map
preserves the order test, including the nonlinear `x+clip(x,0,1)`. Outside the
finite class, a nonlinear increasing map can preserve a single nonzero test.
For example, write x=n+r with n integer and 0<=r<1, and set

    h(x)=n+q(r),
    q(r)=3*r/2                    for 0<=r<=1/2,
         r/2+1/2                 for 1/2<=r<=1.

This continuous function has positive alternating slopes and
`h(x+1)=h(x)+1`. Hence x-y<=1 iff h(x)-h(y)<=1, but it is not affine and has
infinitely many affine pieces. Restricting source baselines to a bounded
interval also invalidates the step-to-an-unbounded-tail argument. The corollary
is an exact global finite-CPWA result, not a claim that a single experimental
threshold identifies an affine calibration.

A nonvacuous bounded-domain example makes the last qualification concrete.
Interpolate linearly through

    (0,0), (1/2,3/4), (1,1), (3/2,7/4), (2,2),

and set h(x)=x outside [0,2]. This is globally strictly increasing, rational,
finite CPWA and non-affine. For every pair x,y in [0,2], it nevertheless gives
`x-y<=1 iff h(x)-h(y)<=1`. If y<=1, use h(y+1)=h(y)+1 and strict increase.
If y>1, every possible x satisfies both inequalities, since
`h(x)-h(y)<=2-h(y)<1`. The test is nonvacuous on this domain: x=2,y=0 fails
both sides. The corresponding -1 test also holds, by applying the same
threshold equality to the reversed pair with its weak/strict boundaries.
Outside the stated domain the equivalence fails: y=5/4 and x=19/8 have
`x-y=9/8>1`, but `h(x)-h(y)=19/8-11/8=1`. Thus a bounded native source can
support exact selected-budget tests under a nonlinear finite recoding without
contradicting either global rigidity theorem.

### 3.2 Sound nonlinear bounds must respect the sign

Assume on the relevant output range that every secant slope of h lies in
[m,L], with 0<=m<=L<infinity. For t−s<=b one has

    h(t)−h(s) <= L*max(b,0)+m*min(b,0).

For b>=0, if t<=s the difference is nonpositive; otherwise upper-Lipschitzness
gives at most Lb. For b<0, t<s and the lower secant bound gives
h(t)−h(s)<=m(t−s)<=mb. This is S4. Multiplying a negative improvement budget
by an upper Lipschitz constant reverses the relevant reasoning and is invalid.
For h(x)=max(x,2x), global slopes lie in [1,2]; t=−2,s=−1,b=−1 gives encoded
difference −1, violating the naive claimed upper bound −2.

## 4. Bounded code is not bounded additive value

An exact order encoding of R into (−1,1) is h(x)=x/(1+|x|), with inverse
h^{-1}(y)=y/(1−|y|). Exact arithmetic can be transported by

    y plus_h z = h(h^{-1}(y)+h^{-1}(z)),

and similarly for all other operations. The old budgeted comparison is
h^{-1}(y)−h^{-1}(z)<=b, equivalently y<=h(h^{-1}(z)+b). It is not in general
the ordinary code-difference test y−z<=h(b). This is the same recoding principle
already established in F02, now applied to signed native comparisons.

**S5 (finite-CPWA bounded-code obstruction).** No bounded, finite CPWA function
R->R can be injective. Its far-right affine tail has slope zero, because every
nonzero affine slope is unbounded on that ray. Thus the function is constant on
an entire tail. The same argument on [0,infinity) suffices for nonnegative
unbounded values. Therefore no exact injective global bounded recoding is itself
an F05 term of one freely varying unbounded source. This does not prohibit
bounded domains, approximate encodings with explicit scope, or transported
operations outside the selected finite CPWA language.

Restricting an old unbounded source to a bounded interval is also different from
encoding every old state: it can add new valid conclusions. The query x<=1 is
invalid on R and valid on [0,1]. Faithful representation needs the appropriate
image/reduct correspondence, not simply a finite numerical range. Conversely,
clipping is a native bounded map but generally loses distinctions: for z>=1,
clipping z and z+1 to [0,1] makes their strict original improvement disappear.

Also no bounded carrier containing a positive number is closed under ordinary
unrestricted addition: repeated addition exceeds every finite upper bound. A
bounded interpretation must restrict its operations or change them. The source
domain can nevertheless be a compact rational polytope in the present calculus;
each fixed continuous term then has a bounded range. That fact does not impose
one common bound on all terms or on all contexts.

The obstruction is not repaired merely by using several bounded native
coordinates. Let P be an unbounded finite union of closed polyhedra and
F:P->R^m the restriction of a finite CPWA map with bounded image. Refine P by
all affine cells of F. Some nonempty cell Q must be unbounded, since a finite
union of bounded cells is bounded. Such a polyhedron contains a nonconstant
ray x_0+t*v. To reconstruct the ray, normalize an unbounded sequence relative
to x_0 in the maximum norm and take a convergent subsequence of directions.
Its nonzero limit satisfies every homogeneous recession inequality A*v<=0.
Rational feasibility can supply a rational direction after fixing one nonzero
coordinate to 1 or −1. On Q, F(x)=M*x+c; boundedness along the ray forces
M*v=0. Thus F collapses an entire ray and cannot be injective. This is still
a finite-CPWA claim, not a prohibition on arbitrary discontinuous encodings.

There is a complementary decoder statement directly in F08's substitution
interface. If **all relevant new source coordinates on the target reduct** are
bounded, every finite CPWA substituted old coordinate has bounded range there.
The image cannot equal an unbounded old projected reduct. U16 therefore rules
out all-query faithfulness through such a native decoder. A bounded full source
whose bounds are inaccessible to the target does not meet this hypothesis:
its native reduct can still be unbounded. Retaining an unbounded common offset,
or asking only queries insensitive to that offset, is a different contract
and remains the positive alternative already analyzed in F02.

### 4.1 A strict-improvement boundary specific to the native theorem

Let z>=0, new loss z, old loss z+1. There is a row-free native budget −1 by
constant difference, despite the unbounded baseline. Squashing the two outputs
with h(x)=x/(1+x) gives

    h(z)−h(z+1)=−1/((1+z)(2+z)).

Every point still strictly improves. But the supremum of the encoded difference
over z>=0 is 0, unattained; no uniform negative budget exists. This does not
contradict F08's strict-validity/attainment characterization: the squashed
function is not finite CPWA. It shows exactly why its hypotheses matter.

More generally, for every increasing function bounded above on a positive ray
and every fixed d>0,

    inf_{x on the ray} (h(x+d)−h(x))=0.

If the infimum were e>0, summing n increments from any starting x would give
h(x+nd)>=h(x)+n*e, contradicting boundedness. This is S6. Thus no such bounded
monotone presentation preserves a nonzero baseline-independent improvement
margin for all unbounded baselines, even though a strictly increasing encoding
preserves pointwise strict order. With t and s in a bounded range, a positive
lower secant constant can restore a quantitative guarantee as in S4.

For a sharp restricted example, take 0<=t,s<=M and h(x)=x/(1+x). For
0<=b<=M the largest encoded difference subject to t−s<=b is b/(1+b), attained
at (t,s)=(b,0). For b=−d with 0<=d<=M it is

    −d/((1+M−d)(1+M)),

attained at (t,s)=(M−d,M). To check both, use
h(t)−h(s)=(t−s)/((1+t)(1+s)); for a fixed positive gap the denominator increases
with the baseline, while for a negative gap the largest value is at the largest
baseline and the smallest allowed gap. Differentiation is unnecessary: these
monotonicities follow by comparing the positive rational factors. If b<−M
there are no feasible pairs, so do not present that case as an attaining model.
