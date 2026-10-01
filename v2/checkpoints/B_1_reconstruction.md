# Gate B — fresh reconstruction of the finite core

Reviewer: **Codex (GPT-6)**. September 30, 2026 (America/Los_Angeles;
observed UTC work begins October 1). Base `d50905e`.
Status: **reconstruction complete; disposition in [B_1](B_1.md)**.
This is a fresh same-agent, non-blinded derivation from the definitions and
actual checker, followed by comparison with the F05–F10 records. It is not an
independent reviewer or a proof-assistant verification.

## R1. Begin with a model, not checker acceptance

Fix a finite signature, positive rational conversion factors, closed typed
finite terms, and a nonempty finite family of closed rational polyhedra. Each
case has its own feasible rational witness. Coordinates are finite real numbers
at each assignment, but need not be uniformly bounded over the source.
For one named case h the comparison means

    for every x in P_h, eval(new,x)-eval(old,x) <= b.

A global comparison quantifies over the union of cases. This definition does
not mention a proof, implementation or optimizer. A supplied feasible witness
establishes nonemptiness, not the empirical applicability of the rows.

Structural evaluation is total and single-valued: leaves have declared values;
arithmetic, lattice operations and positive conversions are total on finite
reals; a nonrecursive let evaluates its RHS in the old environment before
extending that environment. This last ordering handles shadowing. Memoization
by a bare syntax node without its binding environment would not implement it.
Finite min/max subdivisions give rational CPWA denotations. Hidden assignments
are available to this mathematical interpretation, not automatically to a
deployed policy.

The kernel's collected form is an affine combination of source atoms and
recursively collected nonlinear atoms. Give each atom its pointwise denotation
and extend linearly. Structural induction proves that valuation of the form
equals term evaluation. The let induction carries the local environment;
residual unfolds as max(new-old,0). Hence identical forms imply identical
denotations. The converse need not hold. In particular, distributive identities
must be proved with rules when the opaque forms differ. The implementation
calls typing before collecting away zero coefficients.

## R2. Reconstruct soundness one point and one domain at a time

Choose an arbitrary point in the domain of an instruction. Backward parent
indices permit induction on instruction order. For ordinary rules all parents
have this same local/global domain; an all-cases instruction is treated
separately. Let d_i denote a parent's new-minus-old difference.

| Rule family | Pointwise implication |
|---|---|
| Constant and row | A constant form has that value; an affine source row, with its intercept retained in the budget, holds by membership in the selected case. |
| Rewrite | Equal collected differences have equal denotations. |
| Add and transitivity | Sum inequalities. Transitivity additionally identifies the common middle denotation. |
| Nonnegative scale and named conversion | Multiplication preserves the inequality and multiplies its budget. |
| Negation | The pair becomes (-old,-new), whose difference is still new-old; the budget is unchanged. |
| Slack | Adding a nonnegative constant to an upper bound is valid. |
| Proof minimum | Two bounds on the same difference imply their minimum, within the same domain. |
| Lattice injections/projections | min(a,b) is below each argument; max(a,b) is above each argument. |
| Common max/min and congruence | With d=max(b1,b2), monotonicity and F(a+d,b+d)=F(a,b)+d give the claimed bound, even when d is negative. |
| Residual congruence | The inner change is (new_second-old_second)+(old_first-new_first); max with the unchanged zero branch gives max(b1+b2,0). |
| All cases | At a point in case h use its own local proof. The maximum local budget covers the union; no point need satisfy every case simultaneously. |

The actual checker inspects every stored instruction, checks the context
fingerprint, equal units, earlier parents and the exact calculated budget, then
checks its recorded difference against the constructor's result. All-cases
requires each live case exactly once and the same literal expression pair.
Thus induction proves the actual designated root, including when it is not
the last instruction. Checking unused instructions is stricter than needed
for this mathematical induction; an invalid unused node is still rejected.

An independently supplied receiving request then fixes context, domain, unit,
literal new/old pair and threshold. An accepted root with b_out<=B meets an
inclusive request. A strict request needs b_out<B. A local proof cannot be
silently promoted to the union, nor can a valid root for a different request
be accepted just because its numeric bound is attractive.

This proves successful-return correctness for the supported immutable standard
data and exact arithmetic. It does not prove termination of search, trust in
empirical premises, physical program identity, runtime correctness or resource
bounds. Evaluating the purported comparison 0<=-1 at a feasible case witness
also rules out vacuous inconsistency of the admitted fragment.

## R3. Three composite conclusions reconstructed from their premises

### M1. Shared-source composition

Suppose the component rows are

    N1-O1-theta <= -3/4,
    N2-O2+theta <=  1/4.

Adding them and collecting the shared coordinate yields
`(N1+N2)-(O1+O2)<=-1/2`. The source is nonempty, for example
`N1=N2=3/4, O1=O2=1, theta=1/2`. The final composite score was not a premise.
With theta restricted to [0,1], separate marginal bounds are 1/4 and 1/4,
so their sum loses the improvement. If the two theta occurrences instead name
independent coordinates, theta1=1 and theta2=0 allows total deterioration 1/2.
The useful premise is shared identity, not an unproved independence assumption.

### M2. A nonlinear component enclosure followed by case aggregation

Take four intervals [a,c] of width 1/8 partitioning [1/4,3/4]. In each case
assume `a<=theta<=c`, `q<=(a+c)theta-ac`, and `q,z>=0`. The component upper
bound is affine. The witness `theta=a,q=a*a,z=0` makes the case nonempty.
The same query in every case is `(q+z)-(theta+z)`.

Write k=a+c-1. The rows imply `q-theta<=k*theta-ac`. If k<=0, multiply
`-theta<=-a` by -k; otherwise multiply `theta<=c` by k. Add the enclosure row.
The four resulting budgets are `-3/16,-15/64,-15/64,-3/16`, so all-cases
gives `-3/16`. Taking the minimum would be false at theta=1/4, q=1/16.
No choice of hidden case is supplied to the policy.

For the motivating component q=theta², the chord error is
`(theta-a)(c-theta)`, between zero and `(c-a)^2/4=1/256`. This proves why that
particular component fits the supplied upper enclosure; the native proof
itself uses the enclosure contract and does not gain variable multiplication.
Any other component satisfying the same rows receives the same comparison.

### M3. A report changes the evaluator's own deployment

Under the declared controller law let `p=s+1/2`, `0<=s<=1/4`,
`h(r)=(1-r)p+r*s`, and `ell(r)=z+h(r)+r/4`. The common report r is fixed before
the hidden source is known. Then

    h(r) = s+1/2-r/2,
    ell(r) = z+s+1/2-r/4.

Both r=1/2 and r=3/4 satisfy h(r)<=r uniformly. Their proxy-cost difference
is -1/16. With the separate paired discrepancy `-1/32<=e<=beta` and a common
baseline w, set `J_new=ell(3/4)+w+e`, `J_old=ell(1/2)+w`. The intended-cost
bound is `beta-1/16`, hence -1/32 at beta=1/32. The proof requires the report
law, the arithmetic composition and the discrepancy premise; a favorable
report alone cannot supply this conclusion.

The executable upper-bound certificate only needs `e<=beta`, so it also holds
on the wider source without the lower row. The displayed bounded interval is
an explicit nonempty uncertainty model; the sign witnesses lie in both models.

Relax beta to 3/32. The new bound is 1/32, attained at e=3/32, while e=-1/32
still gives -3/32. The sign of the actual change is now unresolved by the
source. The old certificate cannot be received under the new revision; replay
must recompute its bound. This is uncertainty with a quantitative update rule.

Changing the controller law is a different update. Under
`h_rev(r)=r*p+(1-r)*s` and charge `(1-r)/4`, the same reports remain valid but
the modeled cost change becomes +1/16 before e. The interpretation scope must
change; old-law RHS replay is insufficient. Thus self-assessment concerns the
evaluator's versioned behavior and influences later use, without concluding
its own soundness or implementing unrestricted cyclic proof reflection.

## R4. Reconstruct the nontrivial completeness result

Fix target unit u. A(u) contains units with a directed conversion path to u,
including u itself. In each case retain precisely rows in those units; call
the resulting union C|u. Original witnesses remain feasible after dropping
rows. Native consequence means existence of a finite accepted proof with
budget at most the requested rational bound, not success of a search routine.

### Necessity: a domain invariant

Trace the designated root's ancestors. Every parent edge preserves its unit
or follows a named conversion edge, so every used source row has unit in A(u).
Repeat R2's induction over the reduct case domains. Each used row still holds
in its case, and all-cases still covers their union. The root holds on C|u.
This is not an assertion that old serialized row indices or fingerprints are
valid in a new context.

An unused foreign-unit let can contain syntactically inaccessible sources.
Therefore the auxiliary term lemma must concern denotational dependence, with
a simultaneous typed-local-environment induction, not every syntactic leaf.
The checker obtains no new inequality from the numerical admission witness.

For the strict separation take U->V with factor one, x:U, and the sole V-row
`convert(x)<=-1:V`, witnessed by x=-1. The full source implies x<=-1:U.
Its U-reduct has no rows and admits x=0. Necessity therefore forbids a native
U-proof. This reduct point is intentionally not a full-source countermodel.

### Sufficiency: explicit finite certificates

First move accessible coordinates and rows into u using fixed positive paths.
For a path factor k, the numerical coordinate is X=k*x. An affine occurrence
of x is represented by X/k, with rational coefficients. Different paths need
not be coherent: use their explicit positive factor ratios. No reverse edge
is introduced. Positivity makes converted source inequalities equivalent.

Lattice operations also require certified conversion identities. Convert the
two injections/projections for one direction; for the reverse, divide the
same-unit inequalities by k, apply the common-bound rule in the original unit,
then convert forward. This proves both directions without accepting a
semantically true but unrecognized nonlinear rewrite.

In that one-unit language normalize the query difference to

    f = max_i min_j (a_ij*x+c_ij).

Syntax gives a finite rational expansion. Translation, positive homogeneity,
negation and distributivity need zero-budget native equality proofs. To check
the noncircular dependency, put a=max(v,0), b=max(-v,0), m=min(a,b). Lattice
rules give b<=a-v; projections then imply 0<=a-m and v<=a-m. Max-common gives
a<=a-m, hence m<=0. Nonnegativity supplies the reverse. Scaling gives the
weighted disjoint-hinge lemma. The existing fixed two-variable affine guard
construction uses this lemma to prove positive-min; closed substitution then
gives distributivity for arbitrary typed terms. It does not invoke the
completeness theorem being reconstructed or split an arbitrary nonlinear guard
as though it were an affine row.

For a clause g=min_j(a_j*x+c_j) on a nonempty polyhedron Ax<=eta, introduce
only mathematically an auxiliary z and maximize z subject to
`z<=a_j*x+c_j`. The lifted polyhedron is nonempty. If g<=B, the LP has a
finite optimum. Rational elimination gives an attained rational optimum and
nonnegative rational multipliers satisfying

    sum_j alpha_j=1,
    A^T lambda=sum_j alpha_j*a_j,
    V=lambda^T eta+sum_j alpha_j*c_j <= B.

Here is why this is not an oracle premise. Fourier–Motzkin elimination pairs
positive and negative coefficients using nonnegative rational weights, keeping
the weight vector of each resulting row. Back-substitution reconstructs a
feasible rational point whenever the projected system is feasible. Projecting
the objective equality onto its one-dimensional objective coordinate yields
its closed rational upper endpoint. The retained weights of that upper row
give the displayed certificate after dividing by its positive objective
coefficient. This covers lower-dimensional and unbounded sources; no original
source vertex is assumed.

Native min projections, scaled by alpha and added, prove
`g<=sum_j alpha_j(a_j*x+c_j)`. Weighted source rows bound this sum by V;
transitivity and slack yield B. Zero weights require no premise, and the
auxiliary LP variable never appears in the returned native context. Join
clauses by max-common, compose the proved normalization equality, and finally
join the original cases using the identical literal query pair. This constructs
a finite native proof. Necessity and sufficiency establish exactly U1.

## R5. What uniform replay adds, and what it does not

With fixed row directions, query leaves, unit graph, cases and interpretations,
the clause dual feasible set depends on none of the RHS parameters. It is an
equality slice of a nonnegative orthant and is pointed. A finite optimum has
a minimum-positive-support optimizer. A nonzero kernel direction on its
support permits both small signs; optimality makes its objective increment
zero. Move until a coordinate vanishes, contradicting minimal support.
Thus the supported columns are independent and the optimizer is a vertex.
There are finitely many supports and hence finitely many such vertices.

Retaining every vertex certificate gives a clause minimum of affine RHS
budgets; maxima combine clauses and cases. The finite trace can therefore
remain optimal under every admitted RHS revision, with each budget recomputed.
This is an existence result, not an implemented complete enumerator or an
efficiency guarantee. If a clause has no dual certificate, primal feasibility
implies unboundedness; absence from an arbitrary supplied list says much less.

Withdrawal restricts removed-row multipliers to zero, a face of the old dual
polyhedron. The surviving vertices suffice, provided the catalogue really was
complete and cases/queries obey the declared contract. Selecting one currently
best proof is a different operation and can lose future optimality. Changed
row directions, extra information or an evaluator change require new work.

## R6. Exact comparisons without overextending their interfaces

For Boolean v assign x_i=1-v(p_i). Negation becomes 1-L, conjunction becomes
max and disjunction min. Induction on formulas proves complemented truth.
With P=max of premise losses (zero for no premises), `L(B)<=P` fails exactly
when all premises are true and B false. Finite Boolean point cases are feasible
and all rows are in the target unit, so U1 supplies the native equivalence.
Inconsistent logical premises make P=1 everywhere; they do not require an
empty source. This is a finite Boolean fragment, not a claim that all signed
loss expressions are truth values.

Phase-one numerical support/refutation margins can be reproduced at their
specified inclusive/strict thresholds. The old metadata and well-formedness
conditions remain additional inputs. Joint failure does not imply that one
fixed marginal fails everywhere: `for all x, exists i` cannot be exchanged
with `exists i, for all x`. No full old evaluator is thereby embedded.

For positive affine presentations x'_u=a_u*x_u+c_u, matching conversion
factors are k'=a_u*k/a_v, with offset c_u-k'*c_v. Same-unit differences and
budgets scale by a_u; the directed access graph is preserved. Matching reduct
images plus U1 establish equivalence of consequence. This semantic theorem
does not turn blind trace relabeling into a compiler: the checked compiler
currently supports the narrower common-positive-scale case; general affine
compilation remains paper-only.

## R7. Producer guarantees are separate proof obligations

Fix the target request before asking any producer for a certificate. A source
map replaces old source variables simultaneously by closed same-unit target
terms; inserted terms are not recursively substituted again. At a target point,
interpret each old coordinate by its replacement's value. Structural induction,
including the old lexical environment at each let, commutes this interpretation
with term evaluation and collection. Closedness prevents local-name capture.
The conversion interpretation must remain fixed.

For each target case choose its declared old case, localize the old proof, and
replace each used row by a checked target proof of that row's substituted
difference. A row index or old budget alone is not such evidence. The budget
used at the replacement is its current localized budget. Grafting earlier
finite traces with index offsets preserves backward references. Recompute every
parent budget; induction then proves the transformed pair on that target case.
An all-cases assembly covers every current target case once. This need not
transport unused old rows, but does require a replacement for every used leaf
unless a separately sound simplification removes that dependence.

For withdrawal, a meet can retain an available alternative. A normalized
constant can be proved without the old leaves. These operations prove a
successful returned root; their failure proves neither semantic falsehood nor
native nonderivability. Pruning initially checks the entire input, including
unused instructions. A compiler that selects today's best meet branch preserves
today's result but need not preserve tomorrow's optimal replay. The capped-tent
fixture below gives a strict counterexample to that stronger compiler contract.

Quantitative premise discharge has another independently checkable contract.
At a removed row `a_i<=eta_i`, replace its budget by the term

    E_i = eta_i + max(a_i-eta_i,0).

Lattice injection proves `a_i<=E_i`; a retained row uses constant eta_i.
Internalize the rest of the local budget program with additions, nonnegative
scalings, minima, maxima and residual clipping. Each constructor admits its
native zero-budget allowance proof. If E_P is the resulting term and b_h the
original localized bound, the advertised penalty must equal `E_P-b_h` and the
returned trace must prove `new<=old+E_P`. It is insufficient to check a valid
trace while trusting an unrelated field named penalty. Every leaf allowance is
at least its original budget; the budget operations are monotone, so
`E_P-b_h>=0`. On points satisfying all original used rows every leaf equals its
old budget, hence the penalty vanishes. Negative b_h is preserved.

Two tempting stronger conclusions fail. First, proof-local discharge need not
give the best possible bound after withdrawal. Second, applying a nonlinear
budget program to mean violations need not bound its expectation: for equally
likely (v1,v2)=(1,0),(0,1), mean max is 1 while max of means is 1/2. A linear
nonnegative majorant can be integrated under an explicit law and finite moment
conditions. Integrate the paired difference; two individually infinite expected
losses cannot be subtracted. None of these operational premises comes from a
fingerprint, a feasible source witness, or an accepted native trace.

## R8. Fresh falsification targets and downstream boundary

On 0<=x<=c, c>=0, the query `min(x,2-x)` has exact supremum min(c,1),
attained at x=min(c,1). Projection to x and the upper source row prove c.
Half of each min projection, added, proves the source-free bound 1.
Meeting the two proves min(c,1). At c=1/2 a compiler may select the row proof;
replaying that selected proof at c=2 gives 2, although the retained portfolio
still proves 1. Withdrawing the cap leaves the source-free proof available;
the row-only strategy has no proof. This separates current validity, future
optimality, and strategy availability without relying on a semantic solver.

The new fixture checks 13 rational caps and 221 rational points, plus 19 tests
covering hostile receiving requests, disjoint cases, binding, inaccessible
units, withdrawal and report/controller revision. Its independent point
calculations do not prove universal soundness or completeness. R1–R7 provide
the mathematical arguments; the fixture checks their correspondence on a
declared finite family through the unchanged native checker and receiver.

F11 may rely on R1–R4's core and U1 theorem, the explicitly contracted producer
operations above, and R6's scoped comparisons. R5 explains the stronger fixed
revision-family existence result, not an already implemented enumeration
algorithm. Neither a supplied portfolio nor failed search automatically yields
an optimum, unboundedness result, or countermodel. A reduct countermodel must
be labeled as such and checked against the full source before making any
full-source claim. No fresh reproof of every optional F08/F09 theorem is claimed
or needed as a premise of the minimal F11 reasoner.

F10's literature audit is reused with its established-ingredient/adaptation/
contribution-candidate distinctions. No new literature search or priority claim
is made by this reconstruction. The gate record supplies the timing audit,
current test limitations and prospective allocation.
