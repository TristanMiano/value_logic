# F06 S3 — derived numerical cases and coverage-aware proof reuse

Status: F06 completed at rule-development scope; F07 unstarted. September 27, 2026 (UTC).
Base: `cc1bb10e794f13567c4a1715d6b707cf1beda387`.
Dependencies: [F05 semantics](../foundations/03_provisional_core.md),
[S1 rules](02_inference_rules.md), [S2 discharge](02b_source_transport_and_withdrawal.md).
This note develops proof transformations, not F07's independent general soundness
review, a full proof searcher, or a theorem of empirical calibration.
All quantities are finite reals at each valuation; sources may be unbounded.

## 1. The problem being solved

Fix one nonempty, versioned source case C and one fixed comparison t-s, with
unit U and the policy/observation interpretation already fixed. An ordinary
numeric guard u has the same unit after any named conversion. Two local proofs
may establish the SAME comparison under u<=0 and -u<=0 respectively. These are
hypothetical arithmetic cases: the policy is not told the sign of u. In
particular, a proof of an available policy is not obtained by selecting one
policy in the first case and a different policy in the second.

The S1 `all_cases` tag joins the cases already declared in C. It neither proves
that a new partition covers C nor resolves infeasible pieces. The new task is
to eliminate an affine sign partition into S1 local arithmetic instructions.
The final trace should not retain the temporary row, a new trusted `split`
tag, or an infeasible source with a fabricated witness.

Use q<= [b] r to mean q-r<=b. A zero-budget proof can put an explicit term on
the right; a negative numerical budget retains improvement. A case proof may
have b<0, and case elimination must not silently replace b by max(b,0).

## 2. Budget programs of local proofs

For a fixed local proof P, its numerical bound is a finite expression B_P(eta)
in the bounds of its source rows. A row coefficient and the source meaning are
NOT variables of this program. The constructors of B_P are constants, row
coordinates, nonnegative scaling/conversion, addition, minimum, maximum and
max(b1+b2,0). The latter represents residual congruence. Rewriting and negation
leave the budget unchanged. Fixed slack is added. `all_cases` is first localized.

Thus B_P is monotone in each numerical source bound, even when its value is
negative. This is proved by induction over the local construction, not by
assuming that a proof's premises remain true after a revision. The program can
be evaluated for relaxed premises only after those premises have been separately
justified in the target context.

### 2.1 Sensitivity to one removed row

Temporarily append the row u=a(x)+c<=0, normalized as a(x)<=-c. Remove it again
and write h=ReLU(u). The elementary unconditional inequality

    a <= -c + ReLU(a+c)

is a lattice injection after affine rearrangement. Substituting its proof for
each use of the temporary row gives, by the S2 construction, an ordinary proof

    t <=[0] s + A_P(x),
    A_P(x)=B_P(eta + h e_guard).

The retained rows are still assumptions of C. The equality denotes the budget
expression construction, not an extra oracle call. At h=0 its value is b_P,
the original local proof bound.

A finite rational k_P>=0 satisfies

    0 <= B_P(eta+h e_guard)-B_P(eta) <= k_P h,  h>=0.

An explicit sufficient recurrence is:

| Constructor | k |
|---|---:|
| constant or lattice law | 0 |
| retained source row | 0 |
| temporary guard row | 1 |
| rewrite, negation, fixed slack | k_parent |
| add or transitivity | k_1+k_2 |
| nonnegative scale a | a k_parent |
| positive unit conversion a | a k_parent, in converted units |
| minimum of two proof bounds | max(k_1,k_2) |
| max-common, min-common or min/max congruence | max(k_1,k_2) |
| residual congruence | k_1+k_2 |

For minimum/maximum, put K=max(k1,k2). Each changed child lies between its
original value and that value+K h. Monotonicity and common-translation
invariance of min/max bound their output between its baseline and baseline+K h.
The residual case first adds the changes and then applies max(_,0), which is
nondecreasing and 1-Lipschitz. This argument does not assume positive baselines.

The recurrence is conservative, not a claim of the least slope. A currently
inactive alternative proof can make the exact response much smaller. A reused
DAG parent contributes at EACH arithmetic occurrence: sharing the computation
does not license dropping a multiplicity in an additive bound.

### 2.2 A certificate for the sensitivity envelope

It is not enough to calculate k and attach an unchecked claim to A_P. We can
emit a local S1 proof of

    A_P <=[0] b_P + E_P,

where E_P is a typed nonnegative expression numerically equal to k_P ReLU(u).
For fixed units E_P can simply be k_P ReLU(u). Named positive conversion paths
remain explicit on intermediate expressions. The final guard is converted into
the conclusion unit before applying the sign eliminator.

The construction proves both A<=b+E and 0<=E recursively.

* A constant has E=0 and an exact constant-difference proof.
* The recognized guard hinge has b=0 and E=ReLU(u). Its nonnegativity is a
  max injection, and the upper comparison is identity.
* Addition, nonnegative scaling and named conversion apply the corresponding
  existing rule to both certificates.
* At a minimum or maximum node, choose a child error term E with the larger
  numerical gain. The other error term is bounded by E: their difference is a
  nonnegative rational multiple of E, so scale the certificate 0<=E and use
  affine rearrangement. If both gains are zero, use the typed zero instead.
* For a minimum, select the child with the smaller baseline b. Min projection
  followed by that child's upper bound proves min(A1,A2)<=min(b1,b2)+E.
* For a maximum, raise both child bounds to max(b1,b2)+E and apply max-common.

The selected child is a PROOF construction; it need not be an available action.
Every comparison used here is at zero budget after internalizing its constants.
The coefficient-to-error-expression identity is checked by S1's exact affine
normalization, which retains nonlinear hinge identity rather than sampling it.

This supplies an ordinary trace for

    t <=[b_P] s + k_P ReLU(u).

Moving b_P out of a right-hand expression is done by adding the exact constant
comparison b_P<= [b_P]0 and rewriting. It is not done by changing a stored budget
without a rule. The same reconstruction will therefore fail if a coefficient,
polarity, context fingerprint or claimed budget is altered incorrectly.

## 3. Eliminating two live sign branches

Let P_minus prove t<= [b_minus]s under C,u<=0, and let P_plus prove the SAME
syntactic t,s under C,-u<=0. Supply a rational feasible witness for each branch.
The branches overlap at u=0; the overlap is intentional, not double probability
mass or duplicated execution. Every real valuation is in at least one branch.

After discharge and the preceding bound construction we have proofs in C of

    t-s <= b_minus+k_minus ReLU(u),
    t-s <= b_plus +k_plus  ReLU(-u).

The S1 min-common rule yields

    t-s <= max(b_minus,b_plus)
           +min(k_minus ReLU(u), k_plus ReLU(-u)).

More literally, the trace first derives a common left comparison against the
two hinge terms with budgets b_minus and b_plus, and then uses min-common.
The S2 `disjoint_hinges` trace proves

    min(k_minus ReLU(u), k_plus ReLU(-u)) <= 0

for nonnegative rational k_minus,k_plus. It uses only lattice, additive and
nonnegative scaling instructions; it reads no source rows. A final transitivity
step gives the target bound B=max(b_minus,b_plus).

### 3.1 What has and has not been eliminated

The temporary numeric guard disappears from the final CONTEXT. Its expression
may occur in intermediate proof terms; the final pair is t,s and its bound is B.
The source context and interpretation are unchanged, and the final trace can
be validated by the original S1 checker. There is no appeal to a numerical
optimizer deciding the conclusion. A compiler may refuse unsupported or
resource-exhausting input without invalidating this transformation.

This is an admissible rule for the specified finite local proof language. It is
not unrestricted logical reflection, arbitrary quantifier elimination, or a
complete semantic decision procedure. It concerns finite numerical values;
there is no cancellation of +infinity and -infinity.

### 3.2 Sharp budget and invalid alternatives

The maximum of branch bounds is the best conclusion obtainable from just two
arbitrary uniform branch bounds: a query may attain the larger bound inside
that branch. Taking min(b_minus,b_plus) or an unweighted average is unsound.
If additional global comparison evidence is available, an independent proof
may improve B; the sign rule does not assert optimality against all evidence.

The guard conditions must be opposites (or have independently checked coverage).
Two proofs valid respectively on u<=-1 and u>=1 say nothing about -1<u<1.
Likewise two copies of the same branch do not provide coverage. A proof compiler
must check the literal normalized guard relationship, not just labels such as
'negative' and 'positive'. A later section gives a quantitative way to retain
coverage gaps rather than silently discarding them.

## 4. Empty branches: prove exclusion, do not exploit vacuity

The F05 source interface rejects an empty live case: its witness must satisfy
all rows. A sign partition can nevertheless create an empty hypothetical piece.
Such a piece is not made into a live Context, and an arbitrary conclusion is
not accepted from a fabricated point.

Let the parent rows be A_i(x)<=eta_i, with coefficient-only A_i; let u=a(x)+c.
A finite infeasibility certificate for the branch u<=0 consists of lambda_i>=0
and k>0 satisfying

    sum_i lambda_i A_i + k a = 0,
    b = sum_i lambda_i eta_i - k c < 0.

Rows of unlike units cannot be added: positive declared conversions are required
before using them in this certificate. Zero coefficients may ignore irrelevant
rows. The parent is nonempty, so a certificate with k=0 cannot satisfy b<0;
its current feasible witness would contradict that supposed negative sum.

From the PARENT rows alone, addition/scaling derive

    -a <= (sum lambda_i eta_i)/k,
    -u <= b/k < 0.

Hence the other branch's condition -u<=0 is derivable in C, with an explicit
strict margin. Graft that proof into the live branch's ordinary trace, retain
its other parent rows, and recompute its bound. Since the replacement guard
bound is no worse than the original, the recomputed root bound is no worse
than the live branch bound. Weakening can recover the displayed live bound.

The final trace thus uses neither an empty-context rule nor a trusted
infeasibility oracle. A malformed ray fails exact coefficient/strictness checks;
a purported ray for a feasible or boundary-only branch cannot pass. The
published finite Farkas alternative explains why such rays exist for an
infeasible finite rational polyhedron, but the implementation only CHECKS supplied
rays. It does not discover them or import a general conic feasibility theorem.

If BOTH sides are claimed empty, at least one supplied ray is invalid because
every parent valuation has a real sign. The interface refuses this input.
If the parent itself is empty, it refuses the parent before considering a split.

### 4.1 Example

Parent evidence x>=1 is -x<=-1. The hypothetical x<=0 branch has the ray
lambda=1,k=1 and b=-1. The parent proves -x<=-1 and hence -x<=0. A proof from
the surviving x>=0 branch that ReLU(x)<=x therefore transports to the parent.
At x=0, by contrast, BOTH non-strict branches are feasible; a strict-negative
ray cannot be supplied merely because one branch has empty interior.

## 5. Known antecedents and scope

Rational Lawvere Logic, section 4 and Theorem 8, distinguishes arithmetic
reasoning from its Booleanized deduction theorem; the affine language does not
have that same theorem. Our finite, proof-dependent violation allowance is not
claimed to overturn that boundary: it is a quantitative reconstruction of a
given trace, not a fixed formula internalizing arbitrary consequence. Its
prelinearity and ordered arithmetic are relevant antecedents, not automatic
soundness theorems for versioned empirical sources or deployed policies.

MOSEK Modeling Cookbook section 2.3.1 states a finite Farkas alternative and
checks infeasibility by a separating linear combination. The inequality-row
orientation and nonempty-parent argument above are reconstructed explicitly.
No new priority claim is attached to Farkas certificates or ordinary sign cases.

Primary text inspected September 27, 2026 (HTML; no PDF figure inspection):

- https://drops.dagstuhl.de/storage/00lipics/lipics-vol363-csl2026/html/LIPIcs.CSL.2026.3/LIPIcs.CSL.2026.3.html
- https://docs.mosek.com/modeling-cookbook/linear.html#farkas-lemma

The project-specific question is whether these constructions make loss-valued
reasoning compositional, revisable and inspectable with its actual source and
policy conditions retained. A successful emitted trace is evidence about that
finite construction, not about the empirical adequacy of its premises.

## 6. More than a yes/no coverage check

### 6.1 Several guards and a proof-dependent cover loss

Suppose branch j adds a finite list g_jk<=0. Its proof uses the common target
Delta=t-s and obtains b_j. Discharge all temporary numeric guards. The result
is a GLOBAL proof in the parent context of Delta<=A_j, not a statement that
holds only when j happens to be the true branch. This distinction permits
combining alternative proofs without observing j.

Let h_jk=ReLU(g_jk). Nonnegative finite gains k_jk from the preceding recurrence
supply a conservative error envelope

    E_j=sum_k k_jk h_jk,
    Delta <= b_j+E_j.

The fixed proof determines which guards contribute and their multiplicities.
Let B=max_j b_j. Repeated min-common and checked translations establish

    Delta <= B + Gamma,
    Gamma=min_j E_j >=0.

No coverage assumption is needed for THIS quantitative conclusion. Exact
coverage is the additional premise Gamma<=0, which can be discharged by the
opposite-sign construction for a sign tree, or supplied as a separately checked
proof for another declared cover. A scalar allowance Gamma<=epsilon yields
Delta<=B+epsilon. It must not be inferred from finite sampled coverage.

If each coefficient for every branch guard is strictly positive, E_j=0 iff
all branch-j guards hold; hence Gamma=0 iff the finite union covers the current
valuation. If some coefficient is zero, that equivalence FAILS: the proof may
not need that guard. Its bound can validly extend outside the stated branch.
Thus a proof-dependent loss measures loss of the argument's support, not an
intrinsic degree of truth of every condition written in the source context.

The stronger retained function is min_j A_j. Replacing it by B+Gamma is a
convenient upper envelope, not an identity when branch baselines differ. Both
are finite min/plus/ReLU expressions. Neither is automatically an executable
policy that selects the best hidden alternative.

### 6.2 A gap has a magnitude

Take two cases u<=-a and u>=a, with a>0 and a common gain k>=0. Their guard
violations are ReLU(u+a) and ReLU(a-u). Therefore

    Gamma(u)=k min(ReLU(u+a),ReLU(a-u))
            =k ReLU(a-|u|).

Proof of the identity: for u>=a or u<=-a one hinge is zero. For 0<=u<=a the
smaller hinge is a-u; for -a<=u<=0 it is a+u. These cases cover the real line,
including endpoints, and give the displayed tent. This simplification is an
analytic explanation; an emitted certificate may keep the explicit min of
hinges and avoid adding an unchecked rewriting identity to the kernel.

At a=1, the common query Delta=Gamma-1/2 has bound -1/2 in BOTH outer cases
and value +1/2 at u=0. This is a sharp counterexample to treating an incomplete
cover as exhaustive. The valid parent statement retains the tent penalty.
For a=0 the gap vanishes and the ordinary opposite-sign identity is recovered.

### 6.3 Distributional version, with a separately named law

For a probability law supported on the parent source and integrable quantities,
pointwise Delta<=B+Gamma implies

    E[Delta] <= B+E[Gamma].

There is no independence requirement and no need to learn which proof is active.
The root policy is unchanged. Conversely, small E[Gamma] is not a uniform bound
on Gamma, and is not a conditional guarantee on a rare subdomain selected later.

For the preceding a=1 tent, a law assigning probability epsilon to u=0 and the
rest to u=2 has E[Gamma]=k epsilon, while its largest value is k. Taking k=1
and epsilon=1/8 gives expected Delta=-3/8, although Delta=+1/2 on the gap event.
This is a specified finite-law calculation, not an empirical coverage estimate.

The order of operations matters:

    E[min_j E_j] <= min_j E[E_j].

The left may be strictly smaller. For example E_1=(0,2), E_2=(2,0) on two equally
weighted cases gives left 0 and right 1. Both soft inequalities must hold at
each point before invoking this comparison; ordinary branch-local assertions
alone would not justify the minimum.

## 7. Exact sign coverage is not classical Boolean negation

The numeric cases u<=0 and -u<=0 overlap when u=0. Both corresponding violation
losses are zero there. The second is the opposite NON-STRICT halfspace, not the
classical negation of the first. Their coverage suffices for the derived rule;
disjointness of truth conditions is unnecessary. The *positive hinge values*
are disjoint, which is a different statement.

A continuous real-valued violation function has a closed zero set. Therefore
no continuous finite CPWA function has zero set exactly {u:u>0}. This elementary
topological observation prevents pretending that all strict Boolean negations
have already been represented by continuous zero-loss conditions. Strict
countermodels and negative improvement budgets remain meaningful in the
metatheory; no full Boolean-fragment theorem is claimed here. F09 retains that
comparison obligation.

This also clarifies how loss is being used: min and max may express alternatives
and conjunctions at their zero sets, while their actual positive magnitudes
retain task/proof sensitivity that Boolean conditions discard. No unrestricted
identification of cost with metaphysical falsehood is made.

## 8. Units and the price of weakening an assumption

An unweighted hinge depends on the units of its row. Replacing a<=eta by
k a<=k eta for k>0 changes its violation to k ReLU(a-eta). In a linear proof
with coefficient lambda, replace the coefficient by lambda/k. Then both

    (lambda/k)(k eta)=lambda eta,
    (lambda/k)ReLU(k(a-eta))=lambda ReLU(a-eta)

are unchanged. The relevant penalty is the weighted contribution, not the
raw multiplier or raw residual in isolation.

For a general local proof, first reconstruct each old row by scaling its
rescaled current row by 1/k, then apply discharge. This gives the same semantic
allowance. A syntactically different conservative gain calculation may be
larger; that is a compiler precision issue, not an intrinsic difference in
loss. Negative row scaling reverses the inequality and is not admissible as
this transformation; zero scaling destroys information.

Guard conversion for the sign compiler is explicit. Its public finite interface
requires a guard expressed in the conclusion unit, possibly using a named
positive conversion. Intermediate proof steps may use other units. A normalized
coefficient identity does not license adding time, failure probability and cost
without the conversions already declared in F05.

## 9. Conservative gains versus the best bound for one proof

The recurrence in section 2 is finite and easy to check, but it is not generally
optimal. There are at least three different quantities:

1. a recursively supplied global Lipschitz gain;
2. the maximum slope of the one-variable budget program along a relaxation ray;
3. the smallest k such that B(eta+h e)-B(eta)<=k h for all h>=0.

For f(h)=min(2 ReLU(h-1),1), h>=0, the baseline is f(0)=0. The maximum local
slope is 2, whereas the smallest baseline-relative coefficient is 2/3: the ratio
f(h)/h peaks at h=3/2 and is then 1/h. The interval [0,1] has zero response.
A proof can therefore be globally sensitive somewhere without needing that
same coefficient when relaxed from its current evidence.

For a finite rational CPWA ray program with known rational breakpoints, the
best coefficient is determined by endpoint ratios and the final ray slope.
On a positive segment where f(h)=alpha h+beta,

    (f(h)-f(0))/h = alpha+(beta-f(0))/h,

which is monotone or constant in h. Its supremum on that segment lies at an
endpoint, the right limit at zero, or the limit at infinity. The argument is
finite and uses no numerical sampling. It does NOT automatically emit an S1
proof of the sharper bound. Such a proof can use the new checked sign compiler
on a supplied segment decomposition, but automatic ray optimization is outside
this session's implemented interface.

The ordinary gain recurrence is retained as the reliable compiler route. A
smaller exact gain is an optional future proof-quality optimization, not needed
for sound sign elimination because opposite hinge penalties still have minimum
zero for any finite nonnegative gains.

## 10. A full loss comparison compiled through hypothetical cases

Let the fixed old predictor return 0 and the fixed new predictor return 1.
For an unknown target x, declared common use-cost baseline z and extra cost c,

    Old=|x|+z,
    New=|x-1|+c+z.

The parent evidence is x>=3/4, 0<=c<=1/4 and z>=0. These are a nonempty finite
affine source with witness (x,c,z)=(3/4,0,0). Neither absolute cost is bounded
above. The policy does not observe x's sign or change the two predictions.

Split on u=x-1. The negative branch is witnessed at x=3/4; the positive branch
is witnessed at x=1. All source parameters and meanings remain fixed.

### 10.1 Negative branch

The guard gives u<=0. Double it and rearrange to get u<=-u. Identity supplies
-u<=-u; max-common therefore gives |u|<=-u. Independently the parent lower
bound on x gives -2x<=-3/2, and c<=1/4. Add the constant 1 to obtain

    1-2x+c <= -1/4.

Rearrange it as -u+c<=x. Its numerical budget is -1/4, not zero. Add the
common z and compose |u|<=-u and x<=|x|. The resulting local trace proves

    New <=[-1/4] Old.

The guard enters the proof with gain at most 2: outside this branch, its
use to conclude u<=-u acquires 2 ReLU(u). The old source's x and c constraints
are retained, not softened.

### 10.2 Positive branch

Now -u<=0, so -u<=u and |u|<=u. The source row c<=1/4 and the exact constant
-1 give

    u+c-x = c-1 <= -3/4.

Again add z and use x<=|x|. This trace proves New<= [-3/4]Old. Its guard
sensitivity is at most 2. Both traces have exactly the same final expressions.

### 10.3 Parent proof

Discharging the two guards gives parent-context proofs

    New-Old <= -1/4+2 ReLU(x-1),
    New-Old <= -3/4+2 ReLU(1-x).

Min-common and the disjoint-hinge certificate remove the guard allowances,
leaving New-Old<=-1/4. At (x,c)=(3/4,1/4) equality holds, confirming sharpness
for these parent constraints. This equality is a reference calculation, not
the rule used by the checker. The old direct S1 proof supplies another route;
its agreement with the compiled trace is a regression check, not new novelty.

## 11. Iterated numerical cases and a finite shared policy

The single-split adapter can be used recursively. First compile the children
of a deeper split into a proof in their parent source, then use that proof as
a child of the next outer split. Induction on the finite tree supplies a final
ordinary proof in the initial context. The induction concerns a transformation
of supplied proofs, not a completeness theorem or an automatic search strategy.

Every live node needs a feasible witness; every claimed empty child needs a
checked exclusion certificate. The two children must preserve the common query,
source meanings and policy observation. If a branch's parent rows are missing,
reordered or strengthened without matching their exact context, its old trace
is not silently reused. Source transport is a separate checked reconstruction.

A useful four-cell example is

    h(x)=min(ReLU(x),ReLU(1-x)).

The cells x<=0, 0<=x<=1/2, 1/2<=x<=1, and x>=1 respectively give bounds
0, 1/2, 1/2, 0. For example, on x<=0, max-common proves ReLU(x)<=0 and min
projection bounds h. On 0<=x<=1/2, max-common bounds ReLU(x) by 1/2. The other
two cells use ReLU(1-x) instead. These are local algebraic proofs, not a sampled
maximizer. Recursive sign elimination gives h<=1/2 on the whole real line.
Consequently the fixed costs New=z+h(x), Old=z+3/4 satisfy New-Old<=-1/4 for
arbitrary z; a nonnegative unbounded z gives unbounded nonnegative costs.

The numeric case boundaries do not equip New with a selector that sees x:
New is already a single prescribed expression. Replacing its loss by the
minimum of TWO AVAILABLE ACTION costs would need the additional observation-
legal selection argument that F05 expressly requires. The arithmetic adapter
checks the expression pair, not the empirical interpretation of an executable
plan supplied under a name.

### 11.1 Why tree size must be reported honestly

A split is compiled into an expanded local trace using discharge, envelope
certificates and the disjoint-hinge proof. The number of original branch nodes
is not its final proof size. Reusing a DAG premise can also duplicate occurrences
inside a serialized expression even when the proof node is shared. A finite
branch tree can be exponentially larger than its depth.

A checker/emitter should therefore retain explicit resource limits and refuse
exhaustion rather than drop a case, sample the missing region, or reinterpret a
partial tree as exhaustive. No polynomial complexity guarantee is made here.
Measuring node counts and serialized-term visits is an implementation accounting
question, distinct from the logical assertion that a supplied finite expansion
is valid. The later reasoner task must decide how to share expression DAGs.

## 12. Empty-cell margins and changes in evidence

Suppose an exclusion certificate for u<=0 has margin

    delta=-(sum lambda_i eta_i-k c)/k >0.

If only the parent row bounds change by d_i, the SAME numerical combination
has updated contradiction budget

    b'=b+sum lambda_i d_i.

When b'<0 the empty branch remains excluded and the opposite guard still has
a derived strict margin. At b'=0, exclusion is not established: the boundary
u=0 may now be feasible. If b'>0, the ray no longer certifies emptiness. Neither
case justifies continuing to omit the branch merely because it was empty under
the older evidence.

This is a particularly concrete source-sensitive revision rule. For parent
-x<=-1, the x<=0 branch is empty. Relaxing the bound to 0 admits x=0; relaxing
it further to 1 admits x=-1. The saved negative-ray certificate must be checked
against the current bounds. An old branch-pruned proof may still be repairable
by another argument, but branch availability and target-bound validity are
separate claims.

By contrast, a fully compiled sign proof has no new trusted split instruction
to revisit. Its ordinary source rows can be replayed using the existing S1/S2
mechanisms, with a newly computed bound. Even after the old source restricts
neither sign, an arithmetic proof reconstructed from its CURRENT premises is
valid at its current budget. Copying its historical scalar budget would be a
mistake. The semantics and code version must remain fixed for RHS-only replay.

The difference is between (a) rerunning a branch-pruning algorithm with a stale
exclusion certificate, which must fail, and (b) replaying the already emitted
ordinary proof with all used source leaves refreshed, which may yield a weaker
but justified conclusion. This preserves useful quantitative information without
claiming an old impossibility remains true.

## 13. Small uncovered probability does not bound an unbounded loss

A binary coverage claim alone is not sufficient for expected loss improvement.
Let the one supplied case be u<=0 and the common cost difference be Delta=u-1.
Inside the case, Delta<=-1. A law assigning probability epsilon>0 to u=M and
the rest to u=0 has

    Pr[uncovered]=epsilon,
    E[Delta]=epsilon M-1.

For any small epsilon, taking M=2/epsilon gives E[Delta]=1. Increasing M makes
expected deterioration arbitrarily large. Therefore a claim that the cases
cover 'almost all' inputs cannot replace a magnitude or tail condition.

The discharged inequality Delta<=-1+ReLU(u) is valid everywhere. Its expected
version states exactly the missing obligation E[ReLU(u)]<=epsilon_loss. The
probability of violation and the expected violation magnitude are different
parameters, with different units. A bounded-loss assumption would give a
bridge, but no universal loss cap is part of this project's semantics.

This is a direct reason to retain quantitative premise-violation losses rather
than convert every failed premise into an unweighted confidence label. It does
not remove the need to validate the declared probability model or to account
for later selection of a subdomain.

## 14. Sharp offset-case synthesis without another trusted case rule

A more useful construction avoids recursively partitioning the allowance merely
to bound it. Suppose the SAME fixed comparison Delta has two parent-context
proofs

    Delta <= A + alpha ReLU(u-a),
    Delta <= B + beta  ReLU(b-u),

where a,b,A,B are finite rationals, alpha,beta>=0, and the units have already
been aligned. These may be the results of discharging cases u<=a and u>=b.
No claim that those two cases cover the source is being made.

For alpha,beta>0 define

    Cstar=(beta A+alpha B+alpha beta(b-a))/(alpha+beta),
    M=max(A,B,Cstar).

Then the following source-free arithmetic bound is sharp over all real u:

    min(A+alpha ReLU(u-a), B+beta ReLU(b-u)) <= M.

On a restricted parent domain M is still an upper bound, but need not be the
sharpest bound available from that domain. No arbitrary optimization oracle is
needed to construct M; it is arithmetic on the supplied rational constants.

### 14.1 A direct derivation using hinge shifts

For any k>=0 and any finite r,

    ReLU(r) <= k+ReLU(r-k).

An emitted S1 proof is small. The max injection r-k<=ReLU(r-k), rewritten,
gives r<=k+ReLU(r-k). Nonnegativity of ReLU(r-k) and the exact constant
0<= [-k] k give 0<=k+ReLU(r-k) at a nonpositive budget. Max-common combines
these into the displayed zero-budget inequality. No sign test on r is used.

Set

    k=(M-A)/alpha >=0,
    l=(M-B)/beta  >=0,
    a'=a+k,
    b'=b-l.

Because M>=Cstar,

    a'-b' = (alpha+beta)(M-Cstar)/(alpha beta) >=0.

The hinge-shift inequalities therefore give

    A+alpha ReLU(u-a) <= M+alpha ReLU(u-a'),
    B+beta ReLU(b-u)  <= M+beta ReLU(b'-u)
                         <= M+beta ReLU(a'-u).

The second comparison uses b'-u <= a'-u, with a NONPOSITIVE constant difference;
max congruence with zero retains budget zero. Let v=u-a'. Min projection bounds
the common minimum F by each original allowance. Transitivity and subtraction
of the common M give two zero-budget proofs

    F-M <= alpha ReLU(v),
    F-M <= beta ReLU(-v).

Min-common and the already-emitted disjoint-hinge proof give F-M<=0. Moving the
literal M into the numerical budget gives F<= [M]0.

Consequently the entire sharp offset-case bound is itself an ordinary S1 proof.
There is no new `piecewise maximum` oracle, trusted inference tag, or need to
instantiate infeasible hypothetical regions while proving this arithmetic lemma.
The sign compiler can use it after branch discharge; arbitrary parent-context
proofs of its two allowances can use it directly.

### 14.2 Sharpness and finite witnesses

As u becomes sufficiently negative, the first allowance is A and the second
can exceed A, so F attains A. A concrete witness is

    u_left=min(a, b-max((A-B)/beta,0)).

Similarly F attains B at

    u_right=max(b, a+max((B-A)/alpha,0)).

If Cstar is greater than both baselines, the two active affine pieces intersect at

    u_star=(B-A+alpha a+beta b)/(alpha+beta).

Cstar>=A and Cstar>=B imply a<=u_star<=b. Both hinges are active there and
both allowances equal Cstar. Thus M is attained by u_left, u_right or u_star.
The proof of sharpness is analytical; the returned rational witness is a
separately checked illustration, not the inference checker for the upper bound.

### 14.3 Zero gains are separate cases

If alpha=0<beta, the first allowance is the constant A and the sharp bound is A.
If beta=0<alpha, it is B. If both gains vanish, it is min(A,B). Min projection
and an exact constant comparison prove these results without dividing by zero.
A zero gain can express that a branch proof never needed the guard it was given.
The usual maximum of branch bounds would be conservative but unnecessarily weak.

The positive-gain formula must not be applied by continuity at zero. For example

    F_alpha(u)=min(alpha ReLU(u), 1+ReLU(-u))

has supremum 1 for every alpha>0 and supremum 0 at alpha=0. It converges
pointwise to zero as alpha decreases to zero, but not uniformly over the
unbounded source. Rounding a tiny positive gain to zero can therefore change a
claimed uniform guarantee by one full unit. This is another reason to separate
exact rational checking from approximate numeric coefficients.

### 14.4 Useful improvement despite a genuine coverage gap

Take A=B=-1/2, alpha=beta=1, a=-1/4 and b=1/4. The two original cases miss
(-1/4,1/4). Nevertheless their GLOBAL softened arguments yield

    Delta <= -1/2+min(ReLU(u+1/4),ReLU(1/4-u)) <= -1/4.

The finite half-unit gap costs one quarter-unit of guarantee, not complete loss
of the conclusion. At a=-1,b=1 with the same other parameters, M=+1/2, so the
same construction correctly refuses to claim improvement. This is not using
case coverage by assumption: the possible violation is priced explicitly.

More generally when A=B=B0 and both gains are positive,

    M=B0 + [alpha beta/(alpha+beta)] max(b-a,0).

This is the exact price of the offset gap for these two envelopes. It does not
supply empirical estimates of alpha, beta or the probability law, and it does
not automatically minimize the loss of an agent's available policy family.

## 15. Several one-dimensional arguments: when a pair suffices

Suppose all increasing allowances have form

    L_i(u)=A_i+alpha_i ReLU(u-a_i), alpha_i>0,

and all decreasing allowances have form

    R_j(u)=B_j+beta_j ReLU(b_j-u), beta_j>0.

Assume each family is finite and nonempty, and u ranges over the WHOLE real line.
Then

    sup_u min(min_i L_i(u), min_j R_j(u))
      = min_(i,j) sup_u min(L_i(u),R_j(u)).

The upper-bound direction is immediate: the full minimum is no larger than
any selected pair. For the other direction take a number m strictly smaller
than every pair bound. For an increasing allowance, {u:L_i(u)>m} is either the
whole line or an open upper ray. For a decreasing allowance, {u:R_j(u)>m} is
either the whole line or an open lower ray. Every upper/lower pair intersects,
since its pair supremum is greater than m. Finiteness makes the largest lower
endpoint smaller than the smallest upper endpoint whenever both exist. Thus
all these sets have a common point, where the full minimum exceeds m. Let m
increase to the finite minimum of pair bounds. This proves the equality.

This is a one-dimensional interval-intersection argument, not a general
interchange law for sup and min. Constant allowances can be included by taking
the minimum with their values. If only one positive-gain orientation exists
and there is no constant cap, the supremum is infinite. The useful finite rule
selects a pair, but a withdrawn member can require selecting a different pair.
The implementation in this checkpoint need not materialize every possible pair
or assert that this is a general proof-frontier algorithm.

### 15.1 Higher-dimensional failure of pair sufficiency

Let g1=x, g2=y, g3=-x-y. Then

    min(ReLU(g1),ReLU(g2),ReLU(g3))=0

at every (x,y), because all three raw affine values cannot be strictly positive.
But each pair of hinge functions has unbounded minimum along a suitable ray.
For (g1,g2) use x=y=T. For (g1,g3) use x=T,y=-2T. For (g2,g3) swap coordinates.
No pair supplies the finite zero bound established by the three together.

The numerical dimensionality and shared affine relations therefore matter to
how many arguments a reusable certificate must retain. A scalar-gain or
one-dimensional envelope result is not automatically a statement about every
multivariate model. The next section supplies a positive multi-guard rule.

## 16. A derived weighted coverage rule

Let g_i be same-unit finite native expressions, and suppose ordinary parent-
context proofs establish

    Delta <= A_i + k_i ReLU(g_i),   i=1,...,n,
    sum_i w_i g_i <= eta,

with the SAME Delta, finite n>=1, k_i>0, w_i>0, and rational constants. Zero
weights can be omitted. A zero-gain allowance already gives Delta<=A_i and is
handled as a separate competing proof. Set

    H=sum_i w_i/k_i >0,
    C=(eta+sum_i w_i A_i/k_i)/H,
    M=max(max_i A_i,C).

Then Delta<=M. Here eta is obtained from a checked proof, not assumed because
a branch list is labelled exhaustive. It may be positive: the rule is about
quantitative cover loss, not only perfect coverage.

### 16.1 Fully stated derivation

Let s_i=(M-A_i)/k_i>=0 and h_i=g_i-s_i. Hinge shifting from section 14 gives

    A_i+k_i ReLU(g_i) <= M+k_i ReLU(h_i).

Consequently Delta-M is bounded above by EVERY k_i ReLU(h_i), hence by their
minimum. The finite lattice identity

    min_i ReLU(z_i)=ReLU(min_i z_i)

and positive homogeneity of ReLU give

    Delta-M <= ReLU(min_i k_i h_i).

Min projection yields min_j k_j h_j <= k_i h_i for each i. Multiply the i-th
comparison by w_i/k_i, add, and divide by the positive literal H:

    min_i k_i h_i <= (sum_i w_i h_i)/H.

Finally the source proof and the choice of M imply

    sum_i w_i h_i <= eta - sum_i w_i(M-A_i)/k_i <=0.

Monotonicity of ReLU bounds the preceding positive part by zero. All comparisons
can be expanded with the existing scaling, addition, min/max and rewrite rules.
The only lattice identity that needs a nontrivial expansion is supplied next.

### 16.2 Deriving rather than assuming positive-part/min commutation

For two formal finite variables a,b, the easy direction

    ReLU(min(a,b)) <= min(ReLU(a),ReLU(b))

comes from the two min projections, max congruence with zero, and min-common.
For the reverse direction split on a-b. In the a<=b branch, identity and the
guard give a<=min(a,b) by min-common. Max congruence gives
ReLU(a)<=ReLU(min(a,b)), while min projection bounds the target
min(ReLU(a),ReLU(b)) by ReLU(a). The other branch is symmetric. Both branches
are nonempty in the free two-variable context and have zero budgets. The new
sign compiler eliminates that guard into an ordinary S1 proof.

Typed source substitution instantiates this source-free lemma at arbitrary
same-unit native expressions. Repeating the binary lemma handles finite n.
Likewise k ReLU(h)=ReLU(kh) for k>0 has a short existing-rule expansion:
max injections show both kh and 0 below k ReLU(h); conversely scale injections
for max(kh,0) by 1/k, apply max-common, then scale back by k. For k=0 both
sides are the typed zero. These are not new primitive equality oracles.

The rule is thus a finite proof macro once the supplied source and allowance
proofs exist. It is not a statement that all possible case-cover proofs have
this form, nor a complete search algorithm for weights. General derivation-level
soundness remains the later F07 audit, not a theorem imported from this note.

### 16.3 A three-argument improvement with shared sources

Let d=N-O be a fixed policy's intended cost change. The parent source supplies
only three partial numerical contracts:

    d-x <= -1/2,
    d-y <= -1/2,
    d+x+y <= 1/4.

N,O may additionally be nonnegative. A feasible witness is
N=0,O=1/4,x=y=1/4. Adding a common nonnegative baseline to N and O leaves
all comparisons unchanged and makes their absolute costs unbounded.

Put g1=x, g2=y and g3=3/4-x-y. Each row is d-g_i<=-1/2. Under the hypothetical
guard g_i<=0 its corresponding row proves d<=-1/2. These three branch contexts
are feasible; for the first two choose x=y=0,N=0,O=1/2, and for the third
choose x=3/4,y=0,N=0,O=1/2. Their union DOES NOT cover all valuations: at
x=y=1/4 every g_i equals 1/4.

Discharging the guards nevertheless gives three parent proofs

    d <= -1/2+ReLU(g_i).

The exact shared-source identity g1+g2+g3=3/4 supplies eta=3/4 with w_i=k_i=1.
The weighted rule yields H=3 and

    M=max(-1/2, (3/4-3/2)/3)=-1/4.

Thus a quarter-unit improvement survives the genuine uncovered central region.
At the supplied witness equality holds. A direct independent route adds the
three ORIGINAL signed contracts with weights 1/3; it produces the same bound.
Agreement identifies the linear arithmetic antecedent and checks the new route;
it is not evidence that linear-combination reasoning has been newly invented.

Each pair of original contracts alone permits d arbitrarily large. If the third
row is removed, choose d=T,x=y=T+1/2. If the first is removed, choose
d=T,y=T+1/2,x=-2T-1/4. The case without the second is symmetric. Taking N=T,
O=0 for T>=0 keeps the losses nonnegative. Therefore all three source arguments
matter here: retaining only any two is insufficient for any finite uniform
bound. A saved proof may not keep its three-argument conclusion after withdrawal.

### 16.4 Residuals are useful, but can discard helpful signed information

Relax only the first original contract by epsilon>=0. Direct signed addition
then proves

    d <= -1/4+epsilon/3.

The branch baselines become A1=-1/2+epsilon and A2=A3=-1/2. The coverage macro
supplies

    d <= max(-1/2+epsilon, -1/4+epsilon/3).

For epsilon<=3/8 this equals the direct result. Beyond that it can be weaker.
At epsilon=1 it gives 1/2, whereas signed addition gives 1/12. The dropped
negative parts of some g_i supplied useful information in the original source.
This is a controlled precision loss, not unsoundness. Retain the direct signed
argument and take the better currently justified proof when available.

This example supports the existing decision to keep signed comparisons primary
and nonnegative residuals as derived loss objects. It would be a mistake to
replace every signed relationship by its positive part merely because ReLU or
nonnegative loss is convenient. No gate is invalidated: the macro claims an
upper bound, not general optimality over all source information.

## 17. Fresh reconstruction of the checking boundary

The emitted trace is the evidence for a macro application. Its compiler is not
part of the trusted rule set: change a sign, omit a coefficient or attach the
wrong context fingerprint and the old checker must reject the trace. This does
not establish that the checker itself has received F07's general soundness
review; that remains the next task.

### 17.1 Exact rehoming after removing a hypothetical row

Discharge returns a source with the old branch's feasible witness and a new
revision label. Before copying its trace into the original parent, check that
both signatures and observations agree, that each has the same single named
case, and that the entire remaining row tuple equals the parent's row tuple.
Only the feasibility witness and revision/fingerprint may differ. Replace the
fingerprint, then rerun every old checking rule under the parent. Merely changing
a fingerprint without those comparisons would not be a valid transport method.

The parent witness need not satisfy the discharged temporary guard. Its role
is to establish nonemptiness of the parent, whereas the branch witness establishes
nonemptiness of the hypothetical context. Neither point supplies the universal
comparison. The compiled proof's row references name only parent rows.

### 17.2 Signed constants must move through actual proof steps

Suppose a zero-budget node proves t<=s+b+E. Add the exact constant comparison
b<=[b]0. The resulting difference is t+b-(s+b+E)=t-s-E, so an ordinary rewrite
produces t<=[b]s+E. This remains correct for b<0. Editing the original node's
budget in place, or clipping b to zero, is not this derivation.

For two branch nodes t<=[b1]s+E1 and t<=[b2]s+E2, rewrite each to the common
left difference t-s. Min-common yields t-s<=[max(b1,b2)]min(E1,E2).
This is why the negative improvement margin survives disjoint-hinge elimination.
The rule is not min of the branch budgets; min combines alternative global
arguments, while max covers different hypothetical regions.

### 17.3 Named units and the gain

All guard losses must reach the final comparison unit through declared positive
conversions. The gain is dimensionless only after this choice of numerical
coordinates. Its intermediate error term retains the named conversion path;
its final affine normal form must equal k times the final-unit guard hinge.
A source change that changes units, conversion factors or source meanings is
not the same RHS-only replay. Negative or zero changes of order cannot be
silently treated as a positive unit conversion.

### 17.4 What literal policy preservation establishes

The compiler checks one signature/observation contract and a literal common
query pair. This prevents an input proof for policy A in one hidden region and
policy B in another from being advertised as one common-policy conclusion.
It does NOT inspect a general program implementation or prove observation
legality from scratch. The F05 interpretation supplies that external obligation.
For example, a literal numerical minimum can be well typed while no deployed
controller has access to the information needed to select its minimizer.
Retaining its name in both branches does not manufacture the missing action.

The worked cases below concern one fixed query for this reason. The distinction
between proof choice and policy choice remains part of their semantic contract.

### 17.5 Numerical splitting is not arbitrary hidden-case reasoning

The current `all_cases` instruction ranges over the cases explicitly declared
by the source context. An affine sign compiler instead proves an arithmetic
cover within ONE such case. Different hidden modes may attach different source
meanings or rows to the same visible observation; those alternatives cannot be
identified by calling them opposite numerical signs. One may apply a verified
numeric derivation separately inside each declared mode, then use the existing
case instruction with its exact same-query condition. No oracle reveals a mode.

Finite closed affine cases overlap on their boundaries. The overlap is harmless
for universal inequalities and is not interpreted as duplicate probability mass.
A strict guard such as u>0 needs a different representation or an explicit
margin; it is not obtained by dropping the equality case from both branches.

## 18. A branch can be almost excluded without being impossible

The strict empty-branch test is sufficient for removing a branch, not the only
way to retain a useful bound. Suppose a proof on C,-u<=0 establishes
Delta<=b. Its discharged guard envelope gives in C

    Delta <= b+k ReLU(-u),    k>=0.

Suppose a current ordinary proof establishes -u<=q, with finite q not required
to be negative. Max congruence with the zero identity proves

    ReLU(-u) <= max(q,0).

Scaling and transitivity therefore give the graded alternative

    Delta <= b+k max(q,0).

If q<0 the omitted sign case is impossible and its cost is zero. At q=0 the
boundary may still be feasible, but the surviving nonstrict guard is valid
throughout the source; no strict-exclusion claim is needed. If q>0, a possible
uncovered region contributes an explicit allowance. This is useful even though
an empty-branch compiler must reject a nonnegative purported contradiction.

For example let Delta=-1/2+ReLU(-x). The hypothetical x>=0 region has bound
-1/2. Evidence x>=delta>0 excludes x<=0 strictly, but the revised evidence
x>=-1/8 does not. It nevertheless gives q=1/8 and the improvement guarantee
Delta<=-3/8. The query is total at all admitted finite x. If a program itself
were undefined outside the old region, this arithmetic argument would not
repair the missing program semantics.

An old finite exclusion ray has q=(sum lambda_i eta_i-k c)/k in section 4's
notation. Changing its source bounds changes q by the explicitly weighted
amount. The ray ceases to prove impossibility when its strict margin is lost,
but the same parent-row calculation can support this graded alternative.
Thus a loss of certainty about coverage need not erase all useful information.

## 19. Safe replay and sharp re-compilation are different claims

A finite trace after numeric case elimination uses only current parent rows
and the unchanged local instruction set. S1 RHS-only replay recomputes a valid
budget when row bounds change under its exact signature and row-schema guards.
It does not promise the same budget as rebuilding the entire high-level proof
transformation from the revised inputs. Historical constants inside an emitted
allowance are still historical constants, not secretly live source references.

A small exact example shows a real precision difference. The source has rows
x<=eta1 and x<=eta2. Their direct meet-proof has bound min(eta1,eta2). At
(eta1,eta2)=(0,10), discharge with no removed rows internalizes the comparisons
and produces

    x <=[0] min(0,10).

Now change the row bounds to (10,0). Replaying the two internalized arguments
gives x<=[10]0 and x<=[-10]10. The emitted min-common node takes the larger
budget, producing x<=[10]min(0,10), hence only x<=10. Rebuilding from the new
rows internalizes min(10,0) and proves x<=0. Direct replay of the ORIGINAL
meet-proof likewise returns zero. Every compared context has the feasible
witness x=0; this is not an infeasibility artifact.

The lower precision of fixed-trace replay is sound. It reflects the point at
which a snapshot numerical value became a literal term. An implementation
must therefore distinguish:

* replay the existing checked trace and report its recomputed bound;
* recompile a retained high-level certificate using refreshed applicable
  premises, then check the newly emitted trace; and
* search for a different argument, which is not supplied by either operation.

No exact future-optimality claim is made for the residual or sign compiler.
For a purely affine budget program of row bounds, ordinary arithmetic can
preserve its exact weighted update. Min/max alternatives and clipped losses
introduce snapshot-dependent bounds for which that simplification need not hold.
Retaining source references and high-level proof structure can therefore be
useful even after an expanded trace is available. This is a scoped reason to
keep both, not a demand to preserve every historical representation forever.

## 20. Finite proof trees and empty-subtree arithmetic

The binary construction can be applied repeatedly to a supplied finite affine
case tree. A child that returns a checked local proof can itself be the result
of earlier eliminations. A child that is empty instead supplies a rational
linear infeasibility ray. This is a finite certificate format, not an algorithm
that discovers the right cuts or guarantees efficient proof search.

There is a useful consistency check when both children are claimed empty.
Write the parent normalized rows as Ax<=eta and the split as u=a x+c. If the
negative and positive rays have guard weights k-,k+>0, then

    (lambda-/k- + lambda+/k+)^T A = 0,
    (lambda-/k- + lambda+/k+)^T eta = b-/k- + b+/k+ <0.

The constants c cancel. The combined ray excludes the parent itself. If a
child ray has zero guard weight, its parent-row part already does this. A
nonempty parent witness therefore rules out two valid empty children. Rejecting
such input is not losing a legitimate loss proof.

This calculation can also identify an entirely empty internal subtree without
fabricating a live Context for it. At the root, a supplied nonempty source and
ordinary generated proof remain required. The prototype's executable interface
is only a single split plus supplied local proofs/rays. A full automatic tree
search, rational feasibility solver and leaf optimizer are not implemented.

Proof size needs two separate reports. The number of emitted instructions is
not the number of serialized term occurrences: one intermediate allowance may
be shared in a DAG but duplicated in JSON or in recursive normalization. Naively
re-discharge an already-expanded child at every tree level and size can grow
much faster than the original tree. Explicit resource-limit refusal is allowed;
a silent truncation followed by a success claim is not. Neither this macro nor
the finite weighted coverage construction implies a polynomial-time general
reasoner.

These observations leave a precise later characterization question: which
families of finite native source/cell arguments admit compact certificates
without losing the conclusion needed by the consumer? This is an F08 opportunity,
not a characterization task performed or completed here.

## 21. How much information the weighted coverage rule preserves

The constant bound from section 16 is exact for a clearly delimited information
class. Fix n>=1, all k_i,w_i>0, finite A_i and eta. Regard g_i as otherwise
unrestricted real numbers with only sum_i w_i g_i<=eta. Then

    sup_g min_i(A_i+k_i ReLU(g_i))
      = max(max_i A_i, (eta+sum_i w_i A_i/k_i)/(sum_i w_i/k_i)).

The upper bound was already derived in section 16. Here is a constructive
sharpness proof, not extrapolation from finite tests. Write C for the fraction,
H for its positive denominator, and Amax=max_i A_i.

If C>=Amax, set g_i=(C-A_i)/k_i. Every g_i is nonnegative, the weighted sum is
eta by the definition of C, and every allowance is C. The bound is attained.
If C<Amax, choose j attaining Amax. For i!=j set g_i=(Amax-A_i)/k_i>=0 and set

    g_j=(eta-sum_{i!=j} w_i g_i)/w_j.

The inequality C<Amax makes g_j<0. The j-th allowance is Amax and every other
allowance is also Amax. This attains the bound. The equality case may use either
construction. No actual agent must know or select these g_i: they are semantic
witnesses that a smaller bound is impossible from the declared information alone.
For n=1 the same reasoning yields A1+k1 max(eta/w1,0).

Additional restrictions on the g_i may make the bound nonoptimal. In particular,
when they are correlated native functions of a smaller source, the attaining
vectors constructed above need not belong to that source. The rule remains
valid, but its sharpness claim is only for the aggregate-information class.
Zero weights or gains change that class and are handled by omission or a
separate constant bound; the positive-parameter formula is not extended by fiat.

### 21.1 A precise loss caused by clipping signed contracts

For the three-contract example of section 16.3 with the first RHS relaxed by
epsilon>=0, the direct signed bound C=-1/4+epsilon/3 is attained for every
finite epsilon. Set

    d=C,  x=1/4-2 epsilon/3,  y=1/4+epsilon/3.

All three original signed contracts are equalities. Choose N=max(d,0) and
O=max(-d,0), or add any common nonnegative baseline, to keep losses nonnegative.
The softened allowances have the larger tight aggregate-information bound

    M=max(-1/2+epsilon, -1/4+epsilon/3).

Their exact loss of worst-case precision in this example is therefore

    M-C=ReLU(2 epsilon/3-1/4).

At epsilon=1 the gap is 5/12. Keeping only nonnegative violation allowances
can discard a useful negative part of a signed comparison. The correct design
response is to preserve or reconstruct the signed alternative when useful,
not to assert that residuals encode all value information losslessly.

### 21.2 Coverage can itself have a residual allowance

Suppose the same branch allowances hold, but a checked parent argument gives
only sum_i w_i g_i<=eta+E(x). With E replaced by its positive part when needed,
the preceding derivation yields

    Delta <= M + ReLU(E(x))/H,

where M uses the reference eta. To see this without treating it as a new rule,
use the shifts s_i=(M-A_i)/k_i from section 16. Their weighted sum ensures
sum_i w_i(g_i-s_i)<=E. Min projection and weighted addition give
min_i k_i(g_i-s_i)<=E/H. Positive-part monotonicity and homogeneity complete
the proof. The same claim follows immediately from the displayed sharp formula
with eta replaced pointwise by eta+E and the 1/H one-sided shift bound.

In particular the elementary residual inequality always supplies

    sum_i w_i g_i <= eta + ReLU(sum_i w_i g_i-eta).

A missing coverage premise can therefore be represented by another explicit
loss rather than silently assumed true. A uniform bound on that loss gives a
uniform conclusion; an expectation bound under a specified law gives only its
corresponding expected conclusion. The calculus has not proved either bound
just by naming the residual.

This is a local quantitative rule characterization and its boundary. Its linear
and lattice ingredients are established mathematical patterns. It is not a
novel-priority claim, a general completeness theorem for the future calculus,
or an implemented learning algorithm for the weights.

## 22. Concrete derivation plans before implementation

### 22.1 Absolute prediction loss through two hypothetical regions

Keep y>=3/4, 0<=c<=1/4 and z>=0. The unchanged policy comparison is

    new=|y-1|+c+z,   old=|y|+z.

Split on u=y-1. In the u<=0 branch, the guard proves u<=-u after multiplying
its normalized comparison by two; identity proves -u<=-u. Max-common gives
|u|<=-u. The parent row -y<=-3/4, doubled and added to 1 and c<=1/4, gives
1-2y+c<=-1/4. Min/max introduction supplies y<=|y|, so transitivity and common
baseline cancellation yield new-old<=-1/4.

In the -u<=0 branch, identity and twice the opposite guard give |u|<=u.
Then c-1<=-3/4 proves new-old<=-3/4. Both branches have rational witnesses
(y,c,z)=(3/4,0,0) and (1,0,0). Their query pair is literal and unchanged.
The derived sign macro must emit the global -1/4 bound without the temporary
row. The direct S1 absolute-loss argument gives the same result independently.
Neither route assumes that the policy observes the sign used in the proof.

### 22.2 Three-source cover, with no exact union of the old regions

For section 16.3 each temporary g_i<=0 is added to its corresponding partial
row d-g_i<=-1/2, deriving d<=-1/2. Discharge removes that one temporary row.
For g3=3/4-x-y, normalization matters: its row is -x-y<=-3/4, so adding the
parent bound d+x+y<=1/4 gives -1/2, not +1/4.

At M=-1/4, every hinge is shifted by 1/4. The resulting h_i=g_i-1/4 sum to
zero. All three allowance proofs imply

    d+1/4 <= min_i ReLU(h_i) = ReLU(min_i h_i).

Min projections, addition with weights 1/3 and the exact shared-source sum
prove min_i h_i<=0. Positive-part monotonicity finishes d<=-1/4. A missing
argument destroys the coefficient cancellation and admits the unbounded rays
already given. A supplied final comparison would not be a substitute for these
intermediate proofs.

### 22.3 Exact rescaling check

For positive numbers delta_i, replace g_i by delta_i g_i, k_i by k_i/delta_i
and w_i by w_i/delta_i. Every weighted raw term, hinge allowance, ratio w_i/k_i,
H and final M is unchanged. The proof must scale source and allowance meanings
together. Negating a guard without reversing its inequality and treating it as
positive rescaling is invalid. This agrees with the earlier source-transport
boundary rather than overriding it.

### 22.4 Reconstruction targets, not a new trusted kernel

Each proposed macro ends in an ordinary S1 proof. The implementation should
report the scalar result, source rows actually retained, exact trace size and
its declared finite validation limits. It should reject bad witnesses, stale
fingerprints, changed observations, mixed-unit guards, altered query pairs,
nonpositive infeasibility margins, invalid coefficients and resource overruns.
Arithmetic test points outside a hypothetical branch are particularly important:
the final proof is about the whole parent, not just the branch witness used to
construct the input. No test count proves F07's general soundness obligation.

## 23. Conditional empirical validity is not another case-selection oracle

The numerical proof lives inside a declared source. Its statistical use needs
a separate source-validity premise. Let D denote observed data, theta a fixed
modeled parameter, C_D a data-dependent source, and pi_D an observation-legal
policy. Suppose a stated sampling model supplies

    Pr_D(theta in C_D) >= 1-alpha.

If, for every admitted dataset D, a checked derivation proves the same deployed
comparison Delta(pi_D,theta)<=b_D throughout C_D, then event inclusion gives

    Pr_D(Delta(pi_D,theta)<=b_D) >= 1-alpha.

This is a conditional semantic bridge, not a confidence claim produced by the
algebraic checker. The empirical premise must already cover the data-dependent
source and the meaning of the report-dependent policy. Old-policy calibration
alone does not supply it for a changed policy.

Choosing different arithmetic proof branches or numeric cuts after observing D
does not require an additional union bound when all of their conclusions follow
uniformly from that SAME source event. Reusing one source row twice changes its
arithmetic coefficient but does not create two independent confidence events.
Conversely, separate marginal validity guarantees for independently supplied
source claims do not establish simultaneous coverage; extra conditions or a
proper joint bound are required. The finite confidence counterexamples already
recorded in F01/F06 S2 retain their force.

A derived coverage loss Gamma has a different role. A pointwise bound
Delta<=b+Gamma, and Pr(Gamma=0)>=1-alpha, imply a probability statement but no
expected-loss bound without controlling Gamma's magnitude or integrability.
Likewise an expected Gamma bound supplies an expected conclusion, not a uniform
one. This prevents the new case macro from disguising a confidence score as a
numerical cost or a numerical cost as certainty about its empirical meaning.

These statements concern specified probability models in the metatheory. They
neither identify value with factual truth nor equip the system with access to
final metaphysical or meta-logical certainty. They make explicit which premise
would have to be supplied or revised when the calculus is used empirically.

## 24. The numerical self-model and the finite-gain limitation

The versioned two-proof bound calculator already studied in S1 emits

    B(u)=min(-3/4+u, -1/4-u).

Its source u is allowed to be unbounded. A new ordinary sign derivation splits
on u-1/4. In the lower region, min projection and u<=1/4 prove B<=-1/2;
in the upper region, the other projection and -u<=-1/4 prove the same bound.
Both hypothetical contexts have explicit feasible points. Eliminating the split
proves B<=-1/2 in the source with no numeric rows. The policy/calculator is the
same in both regions; the proof did not choose a different deployed program.

The statement concerns what the specified calculator emits. If the second
argument is no longer an applicable certificate, continuing to calculate its
numerical minimum does not restore applicability. At u=1 the first argument is
+1/4; a modified calculator returning only it does not satisfy the old negative
bound. Source/code versioning and arithmetic evaluation remain distinct.

### 24.1 Why a finite residual allowance is a restricted deduction principle

A finite proof with the chosen min/max/add/scale operations has a finite guard
gain. Its discharge therefore turns a hypothesis u<=0 into a weighted violation
loss. This is proof-dependent quantitative discharge, not a universal material
implication or a fixed formula internalizing every possible derivation. Reusing
an assumption can increase the required gain. The construction is related to
existing quantitative/lattice deduction patterns; no priority is asserted.

The finite-gain qualification is substantive. Consider the continuous function
f(u)=sqrt(ReLU(u)). Semantically u<=0 implies f(u)=0. But no finite k satisfies
f(u)<=k ReLU(u) on the real line: for every k>0, take 0<u<1/k^2. The ratio is
1/sqrt(u)>k. A discontinuous indicator 1_{u>0} gives an even simpler failure.
Neither function is a native finite CPWA expression in this fragment. Their
conditional validity alone is not a certificate of a finite quantitative gain.

This does not prohibit richer source-preserving continuations or different
moduli of continuity. It says that importing one of them requires its own
scope/approximation rule rather than claiming the finite-gain compiler already
covers it. Similarly, an empty hypothetical source cannot license an arbitrary
unbounded query merely because semantic implication there is vacuous. The
current nonempty-context interface and explicit branch exclusion avoid that
shortcut. Infinity subtraction and undefined program behavior are outside the
stated finite-value argument.

## 25. Postimplementation reconstruction from threshold feasibility

The 44-case suite first passed before this reconstruction. This is a fresh
same-assistant mathematical check, not an independent reviewer or an inference
of universal correctness from the passing examples.

### 25.1 A second proof of the exact weighted bound

Use only the aggregate-information class from section 21. Set S=sum_i w_i A_i/k_i
and H=sum_i w_i/k_i. To check whether a proposed number b is a valid upper
bound, ask whether there is a feasible vector g with

    A_i+k_i ReLU(g_i)>b for EVERY i.

If b>=Amax, this is equivalent to g_i>(b-A_i)/k_i for every i, including the
strict positivity requirement when b=A_i. A weighted sum of these inequalities
forces sum_i w_i g_i>Hb-S. It is incompatible with the source when eta<=Hb-S.
Conversely, when eta>Hb-S choose a small positive e with

    e sum_i w_i <= eta-(Hb-S),

and put g_i=(b-A_i)/k_i+e. The weighted source holds and every allowance exceeds
b. Thus a bound b>=Amax is valid exactly when b>=(eta+S)/H.

If b<Amax, choose j with A_j>b. That allowance exceeds b regardless of g_j.
Choose every other g_i sufficiently positive that its allowance exceeds b,
then choose g_j sufficiently negative to meet the weighted source. This is
possible because w_j>0. Hence no b<Amax is valid. Combining the cases recovers
M=max(Amax,(eta+S)/H), independently of the attainment construction and emitted
lattice proof.

This derivation also checks the strict hypotheses. A zero weight cannot serve
as the compensating coordinate in the second argument; it must be removed or
handled separately. A zero gain instead supplies a constant comparison. When
all weights are positive and some gains are zero, the sharp relaxed bound is
the smallest constant baseline among those zero-gain arguments: their free raw
coordinates can absorb the aggregate constraint while the other allowances are
made arbitrarily large. The current positive-gain macro deliberately does not
silently extend its division formula into this case.

### 25.2 What the clipped precision countermodel actually contradicts

At epsilon=1 the original three signed contracts imply d<=1/12. The softened
allowances alone admit the point

    d=1/2,  x=-5/4,  y=1,
    (g1,g2,g3)=(-5/4,1,1).

Their weighted sum is 3/4 and all three softened allowances equal 1/2. But the
first ORIGINAL signed row fails: d-x=7/4>1/2. Consequently this point is not a
countermodel to the original source or to its direct signed proof. It is a
countermodel to the claim that retaining only the softened inequalities keeps
all the original precision. The actual prototype retains the original rows and
the competing signed proof, so its new conservative macro does not delete that
stronger information. This distinction is necessary when reporting the result.

### 25.3 Replay can lose precision even when the feasible set stays the same

The example (eta1,eta2)=(0,10) -> (10,0) keeps the source's feasible set x<=0
unchanged. The weaker expanded-trace replay bound therefore does not reflect
new empirical uncertainty about x. It reflects a particular saved argument's
snapshot constants and common-target error propagation. Recompiling the
high-level argument restores the zero bound. A source-aware system should label
these operations distinctly, not describe a valid but weaker replay as a
semantic weakening of the whole source.

### 25.4 The criterion survives the proof, not just its numerical unit

For an ordinary absolute-error interpretation the comparison can concern the
loss at an input. For SELF-MIX the p,s coordinates instead describe modeled
failure probabilities and the compared cost is an expectation at each admitted
parameter value. Universal validity over parameter values does not turn that
expected comparison into a per-trial guarantee. Two Bernoulli failure events
with probabilities 2/5 and 1/5 have an expected improvement of 1/5; under an
independent coupling the new one nevertheless fails while the old succeeds with
probability 3/25. A monotone coupling would be a different extra assumption.

Thus the new compiler keeps the declared criterion/observation/source meaning,
not merely a matching dimension label. Shared uncertain parameters must not be
confused with a supplied coupling of random trial outcomes. These distinctions
were already part of the F05 interpretation and are not relaxed by numeric case
elimination or by a small emitted scalar bound.

### 25.5 A tolerated alternative to the finite-gain obstruction

The sqrt example in section 24 blocks an EXACT zero-intercept linear allowance,
not every useful finite approximation. For h>=0 and any epsilon>0,

    sqrt(h) <= epsilon + h/(4 epsilon).

Indeed (sqrt(h)-2 epsilon)^2>=0 gives h+4 epsilon^2>=4 epsilon sqrt(h).
With rational positive epsilon, the right side is an affine allowance in h.
An explicitly justified component enclosure can therefore recover a tolerated
comparison even though no finite k gives sqrt(h)<=k h uniformly. The cost is
the declared epsilon intercept and increasing sensitivity 1/(4 epsilon), not an
unreported change of the meaning of exact validity.

This nonlinear enclosure is mathematical orientation only in this prototype;
sqrt is not a native Term or an implemented trusted rule. It illustrates why
an obstruction for one exact representation need not end the value-oriented
program. The source-preserving continuation alternative remains available when
such enclosures are too loose for the intended task.

### 25.6 Executable and mathematical scope are not identical

Implemented here: supplied one-cut affine sign elimination, strict ray exclusion,
its graded near-exclusion alternative, symbolic finite-gain envelopes, two-hinge
constant bounds, positive-part/min instantiation and the finite positive-weight
cover macro. Every output is an ordinary proof checked by the unchanged S1 code.

Not implemented here: automatic cut discovery, general feasibility/dual search,
a recursive partition-tree optimizer, a sqrt evaluator, empirical source
calibration or program observation verification. The text's recursive-tree,
soft-coverage and sharpness arguments describe their stated mathematical scope;
they are not falsely counted as implemented algorithms. Output-size limits reject
oversized certificates but do not establish a universal time or memory bound on
all preliminary construction/normalization work.

### 25.7 Two independent constructions of the two-hinge bound

The threshold-feasibility check also applies directly to
F(u)=min(A+alpha ReLU(u-a),B+beta ReLU(c-u)), with alpha,beta>0.
For t>=max(A,B), the condition F(u)>t is equivalent to the open interval

    a+(t-A)/alpha < u < c-(t-B)/beta

being nonempty. This occurs exactly when t<Cstar. For t<max(A,B), one
allowance is already above t and moving along the appropriate unbounded ray
raises the other. This reconstructs sup F=max(A,B,Cstar) without using either
emitter's instruction sequence.

The same result is the two-argument instance of the weighted rule: choose
raw guards u-a and c-u, weights one, gains alpha and beta, and the exact
aggregate eta=c-a. Its fraction reduces algebraically to Cstar. The direct
shift/disjoint-hinge emitter and the generic weighted-cover emitter can therefore
be compared on identical inputs. Agreement is a differential construction check,
not independent verification of their common S1 checker.

### 25.8 A better bound is not automatically a cheaper reasoning process

The modeled cost criterion includes only the use costs actually declared in it.
If producing or checking the new argument incurs an additional cost K, a bound
K<=kappa in the SAME value unit gives the net comparison bound b+kappa by
ordinary addition. A negative b alone does not establish net improvement when
that cost is omitted. A proof-node count is not itself a runtime or resource
certificate, particularly with duplicated serialized terms and coefficient-bit
costs. No efficiency advantage or end-to-end resource saving is claimed by
these finite construction checks. The later empirical task must measure the
appropriate cost rather than silently assuming proof production is free.

### 25.9 Why approximate ray balance cannot be silently accepted

For any epsilon>0 consider the parent row -x+epsilon*y<=-1 and the proposed
empty guard x<=0. Unit weights leave the uncancelled coefficient epsilon*y.
Ignoring it would produce the false contradiction 0<=-1. In fact x=0,
y=-1/epsilon satisfies both inequalities. Arbitrarily small coefficient error
is therefore material on an unbounded source. The prototype's rational exact-
balance check rejects this ray rather than using a floating-point tolerance.

A corrected inference can retain the residual explicitly. If a purported ray
has sum_i lambda_i A_i+k a=r(x), its parent rows establish

    -u <= b/k-r(x)/k.

A separate source bound on -r supplies a graded repair; for example known bounds
|x_j|<=R_j give |r(x)|<=sum_j |r_j|R_j for a coefficient-only affine residual.
Without such information no universal small-error conclusion follows. This is
another use of existing arithmetic/source rules, not permission to change the
exact-ray validator or a claim that a small numerical discrepancy is harmless.

The sign of this correction can be reconstructed directly: from
-x+epsilon*y<=-1 and -y<=R, multiply the second row by epsilon and add to obtain
-x<=-1+epsilon*R. If epsilon*R<1, the x<=0 branch is strictly excluded; at equality
it may contain boundary points; above one it contributes a positive possible
violation. For Delta=-1/2+ReLU(-x), the resulting bound is
-1/2+max(-1+epsilon*R,0). At epsilon=1/100 and R=200, x=-1,y=-200 attains the
positive bound 1/2. These explicit points check both the correction's sign and
why strict exclusion, nonstrict entailment and graded applicability are distinct.


## 26. Implemented scope, validation and completion

The [emitter](../checks/f06_derived_cases.py) implements the supplied single affine
cut, strict ray, shifted-hinge and positive-weight cover constructions described
above. It also derives the positive-part/min lemma rather than adding it as a
trusted tag. The original `f06_inference_rules.py` checker is unchanged. Every
resulting proof is checked under the target context; malformed rays, wrong
queries, changed observations, unit mismatches and damaged traces are rejected.

The final new module has **49 tests**; combined F06 discovery has **171**.
The report's `F06-term-dag-v1` format is a lossless serialization of ordinary
proof terms and steps with backward references. `unpack_proof(ctx, payload)`
reconstructs and checks the trace; tests reject forward references and modified
budgets. Deduplicating storage is not a new inference rule or a claim of cheap
proof checking. Full report and test executions are in the
[S3 work record](../work_logs/F06_2026-09-27_S3.md).

All F06 acceptance conditions and its cumulative D90 are recorded as met.
F07 is next and unstarted. This is not the later independent general soundness
audit, a complete automated calculus, a neural experiment, or a priority claim.
The [source note](F06_S3_sources.md) identifies the familiar arithmetic and finite
linear antecedents rather than treating these constructions as absent from the
literature. The original source, confidence and policy limitations remain.
