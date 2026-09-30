# F08 — unit-directed completeness of finite signed-loss reasoning

Research contributor: **Codex (GPT-6)**, local research session 2026-09-30 UTC.
Status: **accepted at F08 characterization scope**. The work record accounts for
**90.589724 engaged derivation minutes**, satisfying D90 after exclusions.
Base: `9e600f4`. The F05 semantics and F06/F07 kernel are unchanged.

The [acceptance reconstruction](04g_characterization_acceptance.md) consolidates
the proof and its limits. Supporting notes cover [rational reconstruction and
information](04a_characterization_reconstruction.md), [uniform replay](04b_uniform_revision_characterization.md),
[withdrawal](04c_information_and_withdrawal.md), [fixed report laws](04d_warranted_report_characterization.md),
[conversion obstructions](04e_conversion_and_boundary_audit.md),
[substitution/penalties](04f_source_substitution_and_penalties.md), and
[source geometry](04h_geometry_and_transfer.md). These are same-assistant
mathematical constructions; no global novelty or integrated search is claimed.

## 1. Initial conjecture and its failure test

The initial conjecture was full finite completeness: for every admitted F05
context C and rational budget b, semantic validity of t-s<=b implies existence
of a finite native K proof with the same context, scope, expression pair and
adequate budget. F07 establishes the forward implication, not this converse.

Test a signature with units U,V, one source x:U, and one named conversion
`c:U->V` of factor 1. The single source case has the row `convert_c(x)<=-1_V`
and feasible witness x=-1. The request is `x <=[-1] 0_U`.

The request is valid in the independent real semantics: its source is x<=-1.
However, the native rules cannot carry a V-valued premise back to a U-valued
conclusion. The nonderivability argument below is structural, not a failed
bounded proof search. This falsifies the initial conjecture without refuting
F07 or changing any earlier sound rule.

The revised target is an exact characterization of the source information
available to a target-unit proof, followed by a constructive completeness
theorem for that information. An explicit graph criterion then identifies
when this also supplies full semantic completeness.

## 2. Fixed fragment and definitions

Use precisely finite, closed, well-typed F05 terms, finite rational literals
and coefficients, positive rational named conversions, lexical nonrecursive
lets, and nonempty finite unions of rational closed polyhedral source cases.
Every retained case has a supplied rational feasible witness. Values at each
assignment are finite reals; a source need not be bounded. A query has one
fixed literal expression pair t,s of unit u across all cases. The program,
criterion, observation and source meanings are fixed as in F07.

The **unit graph** G has the declared units as vertices and one directed edge
v->w for every named conversion from v to w. A path acts by a strictly positive
rational factor, the product of its edge factors. A length-zero path is allowed.
Let A(u) be the set of units with a directed path to u.

For each case h, form the **u-reduct** C|u by retaining exactly the source rows
whose common unit belongs to A(u). Keep the signature, observation, case names,
and witnesses; use a new revision/fingerprint for the changed context. An
original witness remains feasible after rows are removed. No live case is lost.
This reduct is a syntactic, computable operation on the given source rows; it
is not defined by agreement of all possible observations.

Write B_C(t,s)=sup_{h,x in C_h}(t(x)-s(x)), with +infinity permitted. Let
K_C(t,s;b) mean that a finite native proof has exactly the requested global
root pair and a root budget at most b. Local statements restrict to one h.
Producer size limits and execution resource bounds are not part of this
mathematical existence predicate.

## 3. Characterization

**Theorem U1 (unit-directed consequence).** For every admitted input
above and rational b,

    K_C(t,s;b)  iff  C|u |= t-s<=b.

The forward direction says that inaccessible rows cannot influence a native
root. The converse requires actual proof construction: positive conversion
transport, certified retyping, finite affine sign cells, rational affine
certificates, and elimination of all temporary sign assumptions into K.
Neither a stored semantic supremum nor a lossless serialization is a proof.

When B_(C|u) is finite, the stronger result supplies a rational attaining model and a
native proof at that exact optimal budget, proved below. If it is +infinity, no finite native
budget is possible. A countermodel of C|u need not be a countermodel of C.

## 4. Why inaccessible premises cannot influence the root

Trace the ancestors of the designated root, discarding unreachable instructions
only after the original proof has been checked. Every native rule other than
`convert` preserves the common unit of its inequality premises. A conversion
has exactly the declared edge from the parent's unit to the child's. The same
holds for case aggregation: its parents have the literal same pair and unit.
Consequently every used row has a unit in A(u).

Repeat F07's **domain-indexed** induction on the root's ancestors, interpreting
each local step in its own reduct case and each global step in the reduct's
union. A used source row is true in its own case. The `all_cases` rule assembles
those separate local conclusions; it does not require one assignment to satisfy
the rows of every hidden case simultaneously. All other constructors preserve
their stated local/global domain. The root therefore holds on C|u. Unused
checked instructions do not supply premises to that induction. Context admission
is not a rule extracting an inequality from the numerical feasibility witness.

This is a semantic induction on the original checked instructions, not a claim
that the unchanged serialized proof passes `check(C|u, proof)`. Removing rows
changes indices and the fingerprint. A concrete reduct proof would have to
discard unused steps, reindex surviving rows and revalidate its current data.

In the initial counterexample, C|U has no rows. The rational assignment x=0
violates the requested bound -1, so U1's forward half already proves native
nonderivability. That assignment is deliberately outside the original source.

### A lexical detail that must not be omitted

A term of unit u can contain an unused let binding of a foreign unit. Thus
"every syntactic source leaf has a path to u" is false. The correct dependency
lemma says that the *denotation* depends only on source coordinates in A(u).
Prove it simultaneously for typed local environments: two environments agreeing
on locals whose units reach u give the same value to a term of unit u. At an
unused foreign binding, the body's induction hypothesis ignores the differing
bound value. Conversion uses A(v) subset A(u); the other live operations stay
in one unit. Alternatively, first unfold closed lets capture-avoidantly and
erase unused bindings using the exact collected-form equality audited in F07.

## 5. Constructive converse: the proof obligations

Sections 9–14 discharge the following obligations. The independent max-min
route in 04b provides a second construction with the dependencies in 04g.

1. Retype each relevant source coordinate in unit u using a chosen path.
   Establish universal *native* equalities between the original query and a
   u-only arithmetic expression over those converted coordinates. In particular,
   distributing a conversion through min/max cannot be assumed to be an exact
   `_form` rewrite: the normalizer retains nonlinear atoms.
2. Convert each retained affine row into unit u by a positive path. Its models
   are unchanged, and its row inequality has an ordinary K proof from C.
3. Expand the retyped finite query by a bottom-up binary min/max sign tree.
   Each guard is affine after prior choices. Overlapping equality faces are
   intentional. Obtain rational witnesses for nonempty closed cells and strict
   rational infeasibility rays for empty branches.
4. On a live cell, emit both zero-budget directions from each term to its
   selected affine form. Use rational affine consequence to construct a native
   leaf proof of the requested bound. A failed bound has a rational countermodel.
5. Eliminate temporary sign rows using the F06 discharge/hinge construction;
   never admit an empty live context. Lift converted source premises back to
   proofs of their actual original rows, cover all original cases, and bind the
   returned root to the current request.

## 6. Graph criterion

The stronger graph statement is: for a fixed unit graph, completeness
for all source declarations/contexts and all queries in unit u holds exactly
when A(u) has no outgoing edge to its complement. Incoming closure holds by
definition. Equivalently every unit in u's weakly connected component reaches u.
Disconnected units should not be required to have arbitrary artificial bridges.

If an edge a->v leaves A(u), a source x:a can be bounded only in v while its
query is transported along a->u. This generalizes the first counterexample.
If no edge leaves A(u), foreign rows cannot constrain relevant source coordinates;
an original feasible witness supplies the foreign coordinates for every feasible
relevant assignment. The full source and its reduct then have the same possible
query values. Section 15 proves this and distinguishes fixed source declarations.

## 7. Operational significance and boundaries

For a conventional proxy-to-intended-loss interface with `P->U`, proxy rows
and U-valued discrepancy rows are accessible to an intended-loss U query.
The reverse question need not work: a U-valued cost constraint can imply a
P-valued probability bound semantically while remaining inaccessible to a
native P proof. A new inverse bridge, an order-reflection rule, or a differently
typed request is an explicit interface decision, not an automatic inference.

The comparison keeps the same policy in all hidden sign cells. Choosing a
different affine proof in each cell does not provide the policy with hidden
information. Source applicability and the proxy/task relationship remain
external premises. No neural training, causal interpretation, global novelty,
or unrestricted reflective theorem is claimed.

## 8. Evidence status

The raw clocks, exclusions, successful runs and later native interpreter failures
are in [the F08 work record](../work_logs/F08_2026-09-30_S1.md). Acceptance combines
the detailed reconstruction, hostile examples, bounded source check, finite
native certificates and completed D90. F09/F10 and Gate B remain unattempted;
the finite tests do not formally verify Python or establish empirical meaning.

## 9. Certified retyping, without inverse conversions

Fix a target u and choose one finite path Phi_v:v->u for each v in A(u), with
positive rational product k_v. Choose the empty path and k_u=1 at u. For every
relevant source x:v, put X_x=Phi_v(src(x)). These are typed U expressions, not
new independent sources. Their joint assignments retain the original x values
and all correlations. Numerically X_x=k_v*x, so any rational affine function
of the relevant original coordinates can be expressed in unit u using these
terms and rational scaling by 1/k_v.

**Lemma U2 (native path homomorphism).** For any closed terms a,b:v, K has
source-free, zero-budget proofs in both directions between

    Phi_v(max(a,b))  and  max(Phi_v(a),Phi_v(b)),
    Phi_v(min(a,b))  and  min(Phi_v(a),Phi_v(b)).

Here source-free means no source *rows* are used; the expressions can contain
source coordinates. The proof can be instantiated locally in any admitted case.

For max, converting the two lattice injections a<=max(a,b), b<=max(a,b) and
applying max_common proves max(Phi_v(a),Phi_v(b))<=Phi_v(max(a,b)). For the
other direction form M=max(k_v*a,k_v*b), still in unit v. Lattice injection,
scaling by 1/k_v, and max_common prove

    max(a,b) <= (1/k_v)*M.

Apply the path to this inequality. Exact collected-form equality identifies
Phi_v((1/k_v)*M) with max(Phi_v(a),Phi_v(b)): both forms are the max atom with
children k_v*form(a), k_v*form(b). Thus one actual native rewrite finishes it.
For min, converting the two projections and applying min_common proves
Phi_v(min(a,b))<=min(Phi_v(a),Phi_v(b)). The reverse uses
M=min(k_v*a,k_v*b), its two projections, scaling by 1/k_v, min_common, and the
same path/rewrite argument. Every budget is zero. Division is a rational scalar
in the proof construction, not a new variable-division operation.

Path distribution over addition/scaling and literal conversion are exact
collected-form identities. Residual first expands its checked definition
max(b-a,0), then uses the max result. None of these identities gives a rule
that reflects an arbitrary U premise back into V; the one-way obstruction in
section 1 survives.

**Lemma U3 (native retyping).** Every closed t:u has a finite u-only expression
T over the converted leaves X_x and ordinary rational arithmetic/min/max, with
native zero-budget proofs t<=T and T<=t that use no source rows.

First unfold finite nonrecursive lets with capture-avoiding lexical substitution.
The original and unfolded terms have identical collected forms; K checks the
whole original term before recognizing this equality. Erasure does not admit
an originally malformed child. Remove unused bindings. Every remaining source
occurrence has a path to the output unit along its typed expression ancestry.

More generally translate Phi_v(r_v) by structural induction. Literals become
k_v*q in u, sources become X_x, and addition/scaling/min/max use U2 and the
existing congruence rules. For a conversion c:w->v of factor f, the key exact
identity is

    Phi_v(convert_c(r)) = (k_v*f/k_w) * Phi_w(r).

Both sides have the same collected form. The induction applies to Phi_w(r),
and the displayed multiplier is positive rational. A negative scalar in r
transports both equality directions using reversed negation followed by positive
scaling. No coherent-cycle assumption is needed: every actual path factor is
kept, and ratios account for different chosen paths. This is numerical typed
algebra, not a claim that every valuation bridge is physically reversible.

## 10. All usable affine premises can be brought to the target unit

For each retained row l<=r:v in C|u replace it by Phi_v(l)<=Phi_v(r):u. Call
the resulting context C^u. Positive path factors give exactly the same models
as C|u, not an approximation. Keep the original feasible witnesses. All its
rows are explicitly affine, because conversion and let expansion preserve
affineness. Multiple converted copies do not assert statistical independence.

There is an ordinary native proof of each normalized C^u row from its original
row in C: introduce the original row, apply each named conversion, and rewrite
the resulting affine difference. Normalization transports the intercept and
the budget by the same path factor. The proof does not simply rename the unit.

Thus any proof constructed using C^u rows can later be grafted into C. This
is the exact-equal-budget special case of F06's checked source-leaf transport,
with identity source mapping and unchanged operation/observation meanings.
Proofs generated under the changed context do not retain its old fingerprint.

## 11. Finite affine cells with native branch equalities

Let T,S be U3's retyped query. Expand residuals and process their finitely many
min/max occurrences in a children-before-parent order. At a current tree node,
all earlier nonlinear choices have affine representatives. For the next node
op(a,b), its child representatives a',b' are affine in the original coordinates.
Use the affine guard g=a'-b', with two closed children g<=0 and -g<=0.

In a nonempty child, the guard row proves the selected ordering. For example,
on a'<=b', min(a',b')=a' follows from its min-left projection and min_common
applied to a'<=a' and a'<=b'. Similarly max(a',b')=b' follows from max-right
injection and max_common applied to a'<=b' and b'<=b'. The positive branch is
symmetric. Lift already proved child equalities through native congruence;
addition and signed scaling transport both zero-budget directions as in U3.

Induction therefore produces actual native proofs, in each live leaf, of

    T <=[0] T_aff, T_aff <=[0] T,
    S <=[0] S_aff, S_aff <=[0] S.

The tree has at most 2^N leaves for N processed binary nonlinear occurrences
in this chosen finite expansion. This is a finiteness bound, not a practical
complexity claim or a bound in compressed input size. Equality faces belong to
both children and give the same affine value. No discontinuous branch selector
is introduced into the deployed policy.

Each leaf domain is a closed rational polyhedron. Exact rational linear
feasibility distinguishes live leaves, which have rational witnesses, from
empty ones. The supplied point witnessing the original source is not assumed
to witness every branch. No empty leaf becomes an admitted Context.

## 12. Affine consequence gives a native leaf certificate

Write a nonempty leaf P as A*x<=eta and its query difference as c+v*x. The
finite affine consequence lemma used in F04 states

    forall x in P: c+v*x<=b
      iff exists lambda>=0: A^T*lambda=v, c+lambda^T*eta<=b.

This is ordinary finite linear consequence, not a novel imported completeness
claim for Value Logic. Rational input and rational b permit rational lambda.
One way to see the rational qualification is to apply rational Gaussian
elimination to the active equalities of a feasible multiplier vector, then
approximate its free coordinates within the remaining strict slacks. The
result remains in the rational nonnegative solution polyhedron.

The native certificate is explicit. Introduce each normalized source row,
multiply by its nonnegative lambda_i, and add. Add the constant comparison
c <=[c] 0, rewrite the resulting affine difference to T_aff-S_aff, and add
nonnegative slack to reach b if necessary. Zero multipliers require no row
read; an all-zero vector starts from 0<=[0]0. Compose with the branch equalities
from section 11 to prove the SAME literal pair T <=[b] S at every live leaf.
Negative b is retained throughout; it is not clipped to a residual.

The finite-linear lemma also explains why a leaf may be unbounded in nuisance
directions while its query has a finite bound. Neither enumeration of only
vertices nor a compact source assumption is sufficient for this argument.

## 13. Eliminate sign hypotheses, including empty children

At a live parent, F06's quantitative row discharge reconstructs a live child's
proof under its parent as

    T-S <= b_minus + k_minus*max(g,0),
    T-S <= b_plus  + k_plus *max(-g,0),

respectively, with finite rational nonnegative gains. Its bound program is
monotone in the relaxed guard row. The separately emitted envelope certifies
the gain; attaching an unchecked sensitivity number would not suffice.
Min-common followed by the native disjoint-hinge identity gives a parent proof
at max(b_minus,b_plus). In particular, a common negative b remains negative.

If one child is empty, rational infeasibility provides nonnegative weights
lambda for the parent rows and a guard weight k satisfying, for g=a*x+c,

    sum_i lambda_i*a_i + k*a = 0,
    sum_i lambda_i*eta_i - k*c < 0.

The parent is nonempty, so k>0: k=0 would already contradict its witness.
In the parent, the same weighted row proof gives

    -g <= (sum_i lambda_i*eta_i)/k - c < 0.

This proves the surviving guard, with a stronger bound than its nonstrict
zero threshold. Graft it into the surviving proof. Every native budget
constructor is monotone in its row allowances, so the rebuilt root budget is
no larger. This is a strict exclusion certificate, not vacuous truth under an
inconsistent source. Both children cannot be empty at a live parent.

Eliminate guards from the bottom upward. The final proof uses only C^u rows.
The entire argument uses the already reconstructed F06/F07 transformations;
there is no added trusted `case_split`, optimizer, equality oracle or inverse
conversion tag. For any particular finite construction, finite expansion limits
can be chosen large enough in principle. A fixed default cap can still reject
it; completeness is not a guarantee about every bounded producer call.

## 14. Constructive proof of U1 and exact-bound consequences

Assume C|u semantically bounds t-s by rational b. Convert its rows to C^u and
retype t,s to T,S as in sections 9–10. For each original hidden case h, use its
single-case context for the finite tree in sections 11–13. It supplies a local
native proof T<=b S. Graft the converted rows into the corresponding original
single-case context, and localize the result to h. This preserves or strengthens
the bound. Extend this local trace to the full C by changing its fingerprint:
its signature, observation, case name and exact local rows are unchanged, every
step is local to h, and no `all_cases` remains after localization. Each constructor
therefore still checks. Other cases supply no premises to this local extension.
Append the source-free equalities relating t,T and S,s in that same local scope.
Aggregate all original cases using `all_cases`, with the literal same t,s.
If desired, apply fixed slack to obtain exactly b. This is a finite K proof
with the current request's context, expressions, unit and scope.

Together with section 4, this proves U1 for the specified finite fragment.
The construction is effective using exact rational linear feasibility and
consequence certificates; no sampled test serves as a validity oracle. The
present task specifies and audits this construction, not a complete integrated
implementation of automatic search. F11 remains a separate work item.

**Corollary U4 (optimal native bound).** B_(C|u)(t,s) belongs to Q union
{+infinity}. If finite, it is attained by a rational model and by a finite
native proof at that exact budget. Otherwise no finite native bound exists.

For each nonempty affine cell, project its rational polyhedron by the affine
query map onto the real line. Fourier–Motzkin elimination gives a rational
polyhedron on that line. If bounded above, its rational upper endpoint belongs
to it. Its nonempty rational preimage has a rational point. There are finitely
many cells and cases, so a finite largest endpoint is attained in one. U1
supplies a native proof at that rational endpoint. This avoids an unwarranted
assumption that the source has a vertex or is bounded.

**Corollary U5 (strict current requests).** For rational B, strict validity
`t-s<B` throughout C|u holds iff some native root has budget b<B. If strict
validity holds, U4's attained maximum is strictly below B. The reverse follows
from soundness. An open source or an infinite family can break this uniform-
margin conclusion: values -1/n are all strictly below zero but have supremum
zero. Such a family is outside the present finite closed fragment.

**Corollary U6 (finite proof or rational obstruction).** For a rational b,
either a requested native proof exists or a rational model of C|u violates it.
This is an exact alternative for native derivability. The latter is a genuine
modeled counterexample to the original query only if it also satisfies C.
Neither a bounded search failure nor a producer resource refusal supplies it.

## 15. When this is completeness for the full source semantics

For a fixed signature and target u, let X_u be its declared source keys whose
units reach u. Consider the following **source closure condition**:

    for every x in X_u and every unit v reachable from unit(x), v is in A(u).
                                                               (UC)

**Theorem U7 (fixed-signature characterization).** Native completeness for
every admitted context over this signature and every common-pair query of unit
u holds iff (UC). "Completeness" here means full C semantics, not only C|u.

If (UC) holds, a row whose unit is outside A(u) cannot depend semantically on
any coordinate in X_u: such dependence would require a path from its source
unit to the row's unit, contradicting (UC). Retained rows and unit-u queries
depend only on X_u by the lexical dependency lemma. Therefore, case by case,
take any model of the retained rows on X_u and fill all other coordinates from
the case's original feasible witness. It satisfies both retained and foreign
rows. Hence C and C|u have exactly the same query values. Apply U1.

Conversely, suppose x:a reaches u by a path of product p>0 and reaches a unit
v outside A(u) by a path of product q>0. Use a single source row

    Phi_(a->v)(x) <= -q_v

and a witness with x=-1 (set all other coordinates to zero). The query
Phi_(a->u)(x) <=[-p] 0_u is valid in C. The row is removed in C|u, where x=0
violates it. Section 4 proves native nonderivability. This uses an existing
declared source, and so proves necessity for the fixed signature rather than
quietly adding a variable of a convenient unit.

**Corollary U8 (graph-only criterion).** Uniformly over all choices of source
declarations using a fixed unit graph, full completeness for target u holds iff
A(u) has no edge to its complement. Equivalently, all units in u's weakly
connected component reach u. For all target units simultaneously, the criterion
is that each weakly connected component is strongly connected.

Incoming closure of A(u) is automatic. If it also has outgoing closure, it is
exactly u's weak component, and (UC) holds for every source declaration. If an
edge a->v leaves it, choose a source in a and apply U7's counterexample. The
fixed-signature result can hold under a weaker graph because an offending unit
may have no declared source feeding it. Empty-source signatures illustrate why
this distinction is necessary. No arbitrary conversion between disconnected
units is needed.

## 16. Information preservation under source revision

U1 has a precise selective-revision implication. Keeping the signature,
conversions, observation and hidden cases fixed, a change only to rows outside
A(u) cannot change the set of derivable unit-u bounds, even when it changes the
full semantic optimum. This follows from equal reducts, not from unconditional
reuse of an old proof object. Fingerprints still change; a retained trace must
be revalidated or transported with the correct current row identities.

The lost semantic precision can be arbitrarily large. With x:U, a one-way
factor-one U->V conversion, the accessible row x<=M_U and inaccessible row
convert(x)<=-1_V give full optimum -1 but native optimum M, for rational M>=-1.
Dropping the accessible bound altogether makes the native optimum +infinity.
This distinguishes unavailability of supporting inference from refutation of
the full source model, and makes the cost of the missing interface explicit.

For P->U event-price conversion in the existing reflective loss examples,
P probability rows and U discrepancy/cost rows are accessible to U loss queries.
They therefore lie in the complete side of this result. A P report query may
be on the other side if a U cost row constrains its probability. The result
identifies the exact additional transport obligation instead of assuming that
a good cost certificate automatically supplies the requested probability proof.
