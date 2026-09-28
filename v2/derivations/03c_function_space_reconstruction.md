# F07 S1 — a second algebraic reconstruction and the expectation boundary

Status: **same-assistant alternative derivation**, not independent review.
This uses the same F05 semantics and F06 rules, without choosing a new carrier,
adding an expectation operator, or invoking an external completeness result.
It is a cross-check on [the pointwise soundness argument](03_soundness.md).

## 1. Put the denotations in an ordered function space

Fix any nonempty set D of admitted finite source assignments. Let F(D) be the
real-valued functions on D, ordered pointwise. Addition, rational scaling, min
and max are also pointwise. An expression t denotes one particular function
[t] in this space; finite syntax does not give the agent an oracle for arbitrary
functions in F(D).

For each unit use its separate coordinate copy. A literal b denotes b*1_D,
and a named conversion is the stated positive scalar map between unit copies.
The assertion t <=[b] s becomes

    [t] <= [s] + b*1_D.

Because D is nonempty, the constant embedding distinguishes 0 from -1. An empty
D would collapse all constant functions and validate every universal comparison
vacuously; the supplied-source-witness admission requirement rules that out.

The function space is an ordered rational vector lattice. The finite argument
needs only the following elementary identities, all verified pointwise:

    f<=g implies f+h<=g+h,
    f<=g and k>=0 imply kf<=kg,
    (f+h) min (g+h) = (f min g)+h,
    (f+h) max (g+h) = (f max g)+h.

No completeness of this space for arbitrary infinite joins is assumed. All
functions are finite-valued pointwise but may be unbounded on D. A metalevel
supremum can be infinite without becoming a native term value.

## 2. Recover the rule families from these identities

For transitivity, [t]<=[m]+p and [m]<=[s]+q give [t]<=[s]+(p+q).
For addition, add the inequalities. For negative comparison transport, use
`-s <= -t+b`, which is the SAME difference, rather than reversing a bound
without reversing its operands. Positive unit conversion transports the whole
ordered inequality. Nonnegative slack enlarges its right-hand side.

For min/max congruence, put d=max(p,q). Both inputs are bounded by the respective
old inputs plus d, then use monotonicity and the common-shift identity. For
combining two proofs of the same numerical query, the right constants have
meet min(p,q). These are different uses of a minimum: one operates on loss
functions, the other on two established bounds for an identical loss difference.

For residuals, [res(a,b)]=([b]-[a]) max 0. An increase in b and a decrease in a
increase this function. Applying max congruence to the changed difference and
the unchanged zero function gives the mandatory max(p+q,0) budget. The argument
is valid at nondifferentiable boundaries and requires no gradient convention.

A source row inserts its declared function inequality. Exact normalization
preserves the function represented by a term. Thus these identities reconstruct
all local rules without using optimization, random sampling or a choice of the
actually hidden source assignment.

## 3. Case restriction and union

For D_h subset D, restriction f -> f|_(D_h) preserves all finite pointwise
operations. If the D_h cover D, then f<=g on D exactly when that inequality
holds on every D_h. Different local constant budgets b_h can be weakened to
their common maximum before applying this coverage equivalence.

By contrast, after numerical assumptions have been discharged, each branch
bound B_h is a function inequality on the SAME common domain. Then f<=B_h
for every h implies f<=min_h B_h. The maximum in exhaustive conditional cases
and the minimum in globally applicable alternative proofs are reconciled by
which domain each assertion actually covers.

No independence or convexity of the cases is used in this reconstruction.
Rational polyhedra matter to the current input format, feasible witnesses and
rational-countermodel lemma; the pointwise arithmetic rules themselves preserve
inequalities on any supplied domain where their premises hold.

## 4. Function-valued allowances explain residual discharge

The preceding ordered identities remain valid when a budget is an arbitrary
finite-valued allowance function rather than a constant. For example,

    f1<=g1+e1, f2<=g2+e2

imply

    max(f1,f2)<=max(g1,g2)+max(e1,e2).

At each point let e=max(e1,e2), enlarge both allowances to e, and use common
translation. The same works for min. Combining two proofs of the SAME f-g gives
f-g<=min(e1,e2), while addition sums the allowances. This is the algebraic
cross-check of the graded bound-program construction in
[the discharge reconstruction](03b_graded_soundness_reconstruction.md).

A withdrawn row is replaced by the pointwise identity

    a <= eta + max(a-eta,0).

Its allowance is a modeled violation cost, not a confidence. Propagating such
allowances through a finite proof is justified by the same ordered operations,
not by assuming the withdrawn proposition true at a lower degree.

## 5. Expectation does not preserve all of these operations

Integration is order-preserving and linear on an appropriate integrable domain.
It is NOT generally a homomorphism for min and max. This prevents an important
misreading of the soundness theorem.

Take two equally likely outcomes and nonnegative quantities

    a=(0,2), b=(2,0).

Then E[a]=E[b]=1, but E[max(a,b)]=2 and E[min(a,b)]=0. A native proof about
max(E[a],E[b]) concerns the number 1; it does not establish the same bound on
E[max(a,b)]. The two expressions describe different consumers of information.

The distinction can be arbitrarily large for signed costs. With

    a=(M,-M), b=(-M,M),

the means are zero and E[max(a,b)]=M. No fixed finite bound on the latter follows
from the two zero means alone. Both examples involve finite quantities and
simple finite probability laws; no tail pathology is needed.

### 5.1 A precise rejected extension

Replacing every native assertion by

    E[t-s]<=b

while keeping every native rule unchanged is UNSOUND. In the first example,
`max_common` would combine E[a]<=1 and E[b]<=1 into E[max(a,b)]<=1, which is
false. This does not refute K: K's native premises in that rule are pointwise
upper bounds on the quantities supplied to max.

If source coordinates themselves denote expected costs, K validly reasons
about arithmetic/min/max OF THOSE expected costs. To claim those terms equal
expected costs of a composed program requires a separate program interpretation.
A scalar unit name alone cannot move an expectation through a nonlinear
constructor. In the SELF-MIX example the expected failure formula is an explicit
linear mixture under a fixed report, so that particular interpretation has a
specified justification.

### 5.2 Constructive safe alternatives

A uniform pointwise comparison can be integrated under the conditions in the
scope note. For nonnegative integrable a,b, the weaker inequality
max(a,b)<=a+b gives E[max(a,b)]<=E[a]+E[b]. For signed quantities that particular
sum bound need not hold, so nonnegativity is load-bearing.

The exact identity

    max(a,b)=(a+b+|a-b|)/2

also shows what additional joint information suffices: an integrable bound on
E[|a-b|]. This is not supplied by the individual means. A consumer choosing one
fixed action using its expected cost and a consumer that sees the realized
outcome before choosing an action are different policies, not two notations
for the same minimum.

No new expected-value rule set is adopted here. This is a soundness boundary
and a positive interpretation obligation for later case studies, preserving
the current ordinary real-valued proof semantics.

## 6. Relationship to a machine-checked result

This alternative argument establishes the same mathematical preservation
property as the pointwise proof. It is useful self-review because it makes
translation, domains and aggregation explicit in a different presentation.
It is not an independent reviewer, a formal proof-assistant artifact or a
replacement for exact code-to-rule correspondence. The original checker and
its earlier regression cases remain unchanged.

## 7. Minimal algebraic assumptions used by the argument

The preceding proof uses neither a largest finite loss nor the least-upper-bound
property of the real numbers. To locate the actual metatheoretic assumptions,
consider a nonzero ordered rational vector lattice V with a distinguished
positive nonzero element e. Interpret each unit as a copy of V, each rational
literal q as q e, each positive unit conversion as its positive rational scalar
map, and residual by (b-a) join 0. Source premises use this order.

The native inference pattern remains sound in this interpretation. Addition is
order-preserving, nonnegative rational multiplication is order-preserving, and
translation is an order isomorphism, hence preserves finite meets and joins.
For scalar budgets p,q, their literal bounds are comparable along e and

    (p e) join (q e) = max(p,q)e.

The proof of every local rule in section 2 therefore repeats unchanged, and
finite-DAG induction plus actual case coverage supplies the global result.
The normalizer proof uses only rational vector-space identities and the retained
meet/join nodes, so it also remains valid. A nonempty source and e>0 rule out
a negative-budget self-comparison.

This is a check of the proof's assumption strength, NOT adoption or implementation
of a new vector-valued calculus. In particular, the current Python interface
accepts scalar rational samples and the current source format is specified over
finite real coordinates. Extending the implementation would require explicit
vector orders, witnesses, conversions, query meanings and revised interfaces.
The real rational-countermodel and probability corollaries do not transfer merely
from the lattice argument. No blanket theorem about arbitrary partially ordered
values, non-lattice orders, infinite values or uncertain arithmetic axioms follows.

The point of this algebraic reconstruction is modest: order, addition and finite
lattice operations explain the proof, rather than interpreting each number as a
degree of metaphysical truth. Whether these operations model the intended
pragmatic costs is a separate semantic choice with explicit premises.

## 8. Adversarial guard audit

The following witnesses audit the preservation argument, not merely the
surface syntax of a parser. All numerical values are finite and rational.

| Guard or premise removed | Valid parent information | Invalid proposed conclusion / witness |
|---|---|---|
| acyclic proof dependencies | a statement cites only itself by rewrite | x-x<=-1 would acquire an unsupported circular "proof"; no finite induction base exists |
| actual current source bounds | old row x<=0, current row x<=2 | reusing old bound 0 fails at current x=2 |
| lexical capture in nonlinear keys | let h=1 in max(h,0) and let h=0 in max(h,0) | treating both opaque atoms as max(local h,0) incorrectly equates 1 and 0 |
| transitivity middle identity | x-y<=0 and z-w<=0 | x-w<=0 fails at (x,y,z,w)=(1,1,0,0) |
| multiplicity under addition | x<=1 | two citations cannot prove 2x<=1; x=1 refutes it |
| nonnegative scaling | x<=0 at x=-1 | multiplying both sides by -1 without reversing order would say 1<=0 |
| negation swaps operands | x-0<=0 at x=-1 | (-x)-0<=0 is false; 0-(-x)<=0 is the valid swapped-pair conclusion |
| common query for proof minimum | x<=1 and y<=-1 | choosing the smaller bound for x fails at x=1,y=-1 |
| common right side for max | 1-1<=0 and 2-2<=0 | max(1,2)-1<=0 is false |
| maximum budget for min-common | 2-1<=1 and 2-3<=-1 | 2-min(1,3)<=min(1,-1) is false |
| correct residual polarity | a_new-a_old=-1 and b_new-b_old=0 | at (a_new,a_old,b_new,b_old)=(-1,0,0,0), the residual INCREASES by 1 |
| zero floor for residual budget | preactivation decreases from -1 to -2 | both positive parts are zero, so their difference is not <=-1 |
| exhaustive cases and maximum budget | cases x=-1 and x=1 have local budgets -1,+1 | selecting only the first or averaging budgets does not prove global x<=0 |
| nonempty source admission | x<=-1 and -x<=0 | addition derives 0<=-1 vacuously; no feasible witness supports deployment |
| conversion transports budget | x<=1 with conversion factor 100 | converted x<=1 is false at x=1; the correct converted budget is 100 |
| bind returned root to request | an accepted proof of x<=1 | it does not establish the request x<=0 |

The last two distinctions concern what a caller may conclude. A resource limit
or an exception must be reported as failure to obtain an accepted proof, not
converted to acceptance of a cached result. The new audit receiver returns the
actual checked root only after binding it to an explicit request; it does not
implement evidence calibration, proof search or an action registry.

Some guards are conservative implementation choices rather than mathematically
necessary conditions. Literal equality of a case query is stricter than proved
extensional equality; exact matching of a source interpretation identifier is
stricter than a separately proved semantics-preserving transport. Weakening
those guards requires the corresponding proof, not an assumption that every
syntactically different input has different meaning.
