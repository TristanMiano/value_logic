# F06 S2 — proof-local source transport, withdrawal, and derived rules

Status: saved partial F06 S2 reconstruction, not the F07 general soundness audit.
Base: `77a9b400c9db58e45b78618d391ae8703850f355`.
The selected meaning is F05's finite, signed-real loss comparison. The old
S1 rule register and checked proof traces remain the starting point. All
arithmetic below is finite; no infinity is a native cost term. A missing proof
is absence of a warrant, not a degree of metaphysical falsehood.

## 1. The question and three different transport contracts

Write a local source case as C_h, its feasible assignments as X_h, and an old
proof as P of `t <=[b] s`. The conclusion means t(x)-s(x)<=b for every x in X_h.
A new context D has nonempty feasible cases Y_k. The versioned quantity meanings,
units, conversion factors, and permitted observation/policy interpretation are
part of the interface, not just coordinates of a numerical vector.

There are three distinct useful questions:

1. **Whole-context transport:** does a typed map sigma send every y in Y_k
   into an appropriate X_h? This preserves *all* old semantic consequences.
2. **Proof-local transport:** can the source leaves actually used in this
   particular derivation be established after substitution? This can preserve
   its conclusion even when sigma(Y_k) is not contained in X_h.
3. **Query rediscovery:** is there another proof of the desired new comparison,
   unrelated to the old proof's leaves? Failure of either reuse method does not
   answer this question negatively.

The distinction is operationally important. Old assumptions `x<=1, y<=0`
prove x<=1 using the first row only. New evidence `x<=1, y>=1` still proves
x<=1, although none of its assignments satisfies the entire old context.
Both contexts are nonempty. Copying the old context fingerprint is wrong;
constructing a new proof that cites the current x row is right.

Conversely, proving only that *one* witness maps into X_h is insufficient.
For old 0<=x<=1, new 0<=z<=1, and sigma(x)=2z, the new witness z=0 maps into
X_h, but z=1 refutes the transported claim 2z<=1. A witness establishes
nonemptiness; a derivation establishes a universal source obligation. They
must not be used interchangeably.

This pass develops contracts 1 and 2 for finite traces, with constructive
withdrawal/replacement. It does not implement general query discovery.

## 2. Typed source substitution, with lexical binding kept separate

A substitution assigns each old source key x_u a closed term sigma(x)_u over
the new signature. Closed here means no free lexical local: new source keys
are allowed. Units and the interpretation of every conversion are retained.
It replaces SOURCE nodes, not local variables with the same printed name.
For example, if sigma(x)=z+1, then

    (let x = src(x) in loc(x)+src(x))[sigma]
      = let x = z+1 in loc(x)+(z+1).

The inserted term has no free local x for that binder to capture. If a source
substitution with free locals were allowed, lexical renaming would be required;
this adapter instead rejects it. A zero coefficient does not excuse an
undeclared source, invalid unit, or malformed child.

Given a new assignment y, define sigma*(y)(x)=[[sigma(x)]]_y. Structural
induction on a well-typed term establishes

    [[t[sigma]]]_y = [[t]]_(sigma*(y)).                    (2.1)

For literals and sources this is immediate. Addition, rational scaling,
min/max and residual commute with the substitution because they are the same
finite real operations on both sides. A conversion uses the same positive
factor. At a let, apply the induction hypothesis to the right-hand side, then
to the body in the environment extended by that common value. Closed inserted
terms are unaffected by the local environment. This also proves unit
preservation and total finite evaluation.

Equation (2.1) is an arithmetic substitution statement. It does not prove that
two differently versioned physical programs or loss evaluators are identical.
An operational use across such scopes still needs its explicit meaning bridge.
The executable adapter is deliberately narrower: it retains the versioned
scope and observation identifier and permits a checked coordinate substitution
within them. It returns a comparison of substituted expressions, not a claim
about an unmentioned new black-box policy.

## 3. Localizing a global proof to one old case

S1 traces can end in the all-cases rule and can subsequently combine global
conclusions. To reuse such a trace in a new case k, first fix the old case h
whose local argument is to be reused. Recursively localize the root:

* a local step must have case h;
* a global source-free constant or lattice step becomes a step in h;
* a global arithmetic step localizes each of its parents to h;
* an all-cases step selects its parent for h, then localizes that parent.

The all-cases budget was the maximum of its child budgets. Localization may
therefore improve the bound. At every other constructor the budget is a
nondecreasing function of the parent budgets: sum, nonnegative multiple,
identity, minimum, maximum, or max(p+q,0). Consequently localization constructs
a local proof of the same expression pair with budget no greater than the
original global budget. It does not assume that hidden h has become visible
to the deployed policy. It is one branch of a metalevel proof.

Only root-reachable steps in the selected case need survive in the new trace.
Unreachable records remain part of historical audit data; they are not active
premises of this particular conclusion. This is syntactic proof slicing, not a
claim that the resulting support is semantically minimal.

For an arbitrary map tau from every live NEW case to an old case, localize
separately to tau(k), perform the source-leaf replacements below, then cover
EVERY live new case. Several new cases may use the same old argument. One old
case may disappear if the new source excludes it. A live new case cannot be
silently omitted. The emitted global comparison must retain the same fixed
expression pair and policy; the case map selects proofs, not actions.

## 4. Source leaves as replaceable proof obligations

An old affine source row normalizes as

    a_i(x) <= eta_i,

where a_i has zero constant offset. Let P actually use rows I after localization
and slicing. For every i in I, suppose a separately checked NEW-context proof Q_i
establishes

    a_i[sigma] <=[kappa_i] 0.

Replace each old row introduction with that finite Q_i proof, substitute sigma
in every term and term-bearing rule parameter, and rebuild the arithmetic
constructors with their current calculated budgets. This is **proof grafting**:
the result is an ordinary proof checked entirely against the new context.
There is no trusted rule whose only justification is a source-map name.

If every kappa_i<=eta_i, budget monotonicity gives a root bound no worse than
the old bound. If some replacements are weaker, grafting still constructs a
valid new proof, but its bound must be recalculated. Keeping the old final
number despite weaker leaves is not licensed.

### 4.1 Why each reconstruction step is valid locally

At a replaced leaf the new proof supplies the exact substituted expression
difference. A constant difference remains the same constant by (2.1). Exact
normalization identities are stable under closed source substitution: rational
linear collection is a homomorphism, and each structurally identified nonlinear
atom is replaced by the same instantiated nonlinear atom on both sides. A
nonlinear atom becoming constant can add simplification but cannot falsify an
old identity. Addition, scaling, lattice comparison and residual polarity then
use the same local rule justifications as S1. Recompute their budgets; do not
copy an old target-dependent weakening guard. A named conversion retains its
unit endpoints and factor. This explains the construction constructor by
constructor; F07 remains responsible for the final chosen calculus's general
derivation-level theorem and trusted-boundary audit.

A replacement proof may itself have many source rows, a different proof shape,
or a stronger bound. Repeated occurrences of the same old row can share that
proof DAG while still counting every arithmetic use. Sharing a certificate does
not remove a coefficient from an additive inequality.

### 4.2 Whole-context transport as a stronger special case

If Q_i with kappa_i<=eta_i is supplied for EVERY old row, (2.1) shows that
sigma*(Y_k) is included in X_h. This gives the earlier whole-context contract.
For one derivation, only its used leaves are required; full inclusion is a
sufficient but unnecessarily strong premise. Neither sufficient contract is
claimed necessary for the conclusion: a different proof could use other facts.

### 4.3 Stale fingerprints and row numbers

Old and new proof objects have different context fingerprints even when their
conclusions agree. The old fingerprint identifies historical source data; the
new one identifies currently admitted evidence. Each supplied replacement is
checked in the new case, for the substituted old row's actual coefficient
expression and unit. Matching row ordinal, name, or one feasible point is not
this check. Reordering rows or replacing one inequality by a short derivation
must change the references in the emitted trace. New proofs record their actual
current source dependencies, not just the old evidence labels.

## 5. A concrete reflective reuse problem

Retain SELF-MIX's same deployed controller and criterion. Failure probability
for report r is

    H(r)=(1-r)p+r s.

The report r also incurs use cost r/4. Old and new reports remain FIXED at
r0=1/2 and r1=3/4, rather than being selected using hidden p or s. The proxy
comparison is

    L1-L0 = (s-p)/4 + 1/16,

and the intended-cost comparison includes one paired discrepancy e:

    J1-J0 = (s-p)/4 + 1/16 + e.                          (5.1)

A common unbounded baseline can occur in both costs and cancels before (5.1).
The preceding context used p-s<=1/2, s-p<=-1/2, s<=1/4 and e<=1/32 among its
source rows. Its intended comparison uses only the s-p and e rows. Separate
report-validity proofs use other rows, but need not be ancestors of that root.

Now retain only the current relevant domain information

    3/4<=p<=1,     0<=s<=1/8,     e<=1/32.

It proves the replacement row s-p<=-5/8 by adding s<=1/8 and -p<=-3/4.
Grafting that proof and the current discrepancy bound into the old intended
argument yields

    J1-J0 <= -5/32 + 2/32 + 1/32 = -1/16.               (5.2)

The current source does NOT imply p-s<=1/2: p=1,s=0 is a counterexample.
Thus full old-context inclusion fails, yet the paired improvement strengthens.
No claim that the old report remains valid follows. Indeed

    sup(H(1/2)-1/2) = 1/16,
    sup(H(3/4)-3/4) = -13/32,

with both maxima attained at p=1,s=1/8. The new report is valid and the old one
is no longer uniformly valid. Report validity and policy improvement remain
different queries, even when their proofs share some evidence.

Withdraw the bound on e too. The proxy proof still gives -3/32, but the
intended-cost difference in (5.1) is unbounded above because e is unrestricted.
A finite feasible assignment with e large enough refutes any proposed finite
unconditional intended-cost bound. Calling the missing discrepancy premise
'uncertain' cannot manufacture the transfer. The new context remains nonempty;
the problem is missing evidence, not vacuity or a typing failure.

The executable examples should retain these separate roots and altered-context
witnesses. They must not silently replace the old policy with an oracle policy.

## 6. Withdrawal is a proof-availability calculation

For a fixed new source, a source replacement may be unavailable. Treat that as
an option type `no supplied proof`, not as a finite arithmetic value. A missing
row is not refuted; a present record is not thereby target-world correct.
Availability (present/current/accepted under a declared checker) and validity
of the modeled inequality are separate layers. The inference remains conditional
on its current source rows, just as it was before the update.

A constructive salvage procedure works bottom-up on a localized proof:

* an available replacement row is grafted; an unavailable row cannot be used;
* source-free constant/lattice steps survive;
* a zero-scaled comparison can be replaced by its unconditional constant proof;
* at a minimum over proofs of the SAME query, retain any surviving argument,
  selecting the smallest current bound when more than one survives;
* additive, transitive and other genuinely multipremise steps require their
  premises; a universal case conclusion requires every live case;
* whenever exact normalization already makes a node's difference constant c,
  an unconditional proof at budget c may replace its old derivation.

All inserted steps are then checked in the new context. This last check is
important: a successful availability calculation alone is not a proof.
The method does not find every true conclusion. In particular it does not
search for an unrelated derivation when the retained skeleton fails.

For example two proofs x<=-1 and x<=0 combine to x<=-1. On withdrawing the
first, x<=0 survives; on withdrawing both, neither supplies an upper warrant.
By contrast, if the two numbers are bounds in DIFFERENT hidden cases, both
cases must be discharged and withdrawing one is not repaired by keeping the
other. The identical min/max arithmetic notation does not erase this difference
in proof provenance and quantifiers.

### 6.1 Exactness relative to the stated salvage grammar

Fix a finite proof DAG and fixed current replacement proofs, one or more per
source leaf. Permit only (i) those replacements, (ii) the surviving original
constructors, (iii) either child of a same-query proof minimum, and (iv) the
constant/zero simplifications just listed. Every original budget constructor
is nondecreasing in its finite input budgets. Thus choosing the least available
parent budget is optimal at every mandatory constructor; choosing the least
available branch is optimal at a proof minimum. Topological induction therefore
computes the least root budget obtainable by THIS salvage grammar. At a node
with an unconditional constant alternative, also take its minimum.

This is a restricted reconstruction claim, not semantic completeness, global
optimality over proofs, or a claim about statistical confidence. Sharing a DAG
node creates no resource conflict between alternatives here: a proof can be
used more than once, and the budget operator still counts each use. A separate
resource-limited proof-search problem could impose additional constraints.

### 6.2 Future numeric updates need the uncompiled alternatives

At one evidence snapshot, a proof minimum can discard its weaker branch.
That is not safe as a permanent representation for all future withdrawals or
changes of numerical bounds. Old x<=1 and x<=2 select the first now; after its
withdrawal the second may be the only warrant. Replaying only a previously
selected leaf preserves at most that leaf's consequences. Retain the original
proof family when the requested consumer includes future updates.

## 7. Support-and-budget labels, and their exact dominance order

To state the information requirement more precisely, give each primitive
source assumption an immutable identifier in a finite set E. A label for a
fixed query, fixed numerical snapshot and fixed interpretation scope is

    (S,b,P),   S subseteq E,

where P is a checked proof using the assumptions S and giving bound b.
Arithmetic multiplicity and S differ: using one row three times triples its
contribution where appropriate, but does not create three independent evidence
objects. Jointly supplied rows can carry the same external evidence identifier.
The particular association of rows to evidence objects is checked metadata;
the following construction does not infer empirical reliability from it.

For an alive set A subseteq E, define the best stored bound

    F_L(A) = min { b : (S,b,P) in L, S subseteq A }.

If there is no such label, F_L(A) is *unavailable*. The optional extended-real
notation +infinity is only a shorthand for this failed minimum; no emitted
proof may contain it as a cost or budget.

A label (S,b) dominates (T,c) precisely when

    S subseteq T  and  b<=c.                              (7.1)

Sufficiency follows because every alive set admitting T admits S and receives
at least as strong a bound. Necessity for replacement by this single label
follows by evaluating the alive set T: if S is not included, the replacement
is unavailable there; if b>c, use an alive set containing both and compare the
bounds. A smaller cardinality alone is not enough: {a} and {b} survive
different withdrawals even though their sizes coincide.

### 7.1 Exact irredundancy for the full withdrawal family

For a finite label family and ALL alive subsets, deleting a label (S,b) leaves
F_L unchanged iff another retained label (T,c) has T subseteq S and c<=b.
The forward direction tests A=S: some retained proof must still give at most b
there. The reverse direction is (7.1). Equal duplicates may be merged.

After repeated such deletions, the remaining pairs (S,b) are uniquely determined
by the function F_L, up to duplicate proof witnesses with identical pairs.
To see uniqueness, take an undominated (S,b). Then F_L(S)=b. Any equivalent
family has a label (T,b) with T subseteq S realizing that value. If T were a
proper subset, equality of the functions at T would supply an old label with
support inside T and bound <=b, contradicting undominatedness of (S,b).
Hence T=S. Reversing the argument proves equality of the two irredundant pair
families. This is a concrete finite characterization, not a claim of minimum
neural width, proof-search completeness, or a new ATMS priority result.

### 7.2 How labels compose

For addition/transitivity take support unions and add budgets. Positive scaling
keeps support and scales the budget; zero scaling has the empty-support proof.
At a proof minimum take the union of the ALTERNATIVE label families: either
proof can warrant the query. At a mandatory two-premise max/min comparison,
combine each pair by support union and maximum budget. Universal cases similarly
require one supported proof per live case, then take the union and maximum.

Pruning by (7.1) commutes with these constructions because set union and the
budget operators are monotone in their respective orders. Thus finite support
frontiers can be maintained compositionally, with explicit proof witnesses.
An implementation may instead preserve the compact DAG and specialize it to
one alive set, avoiding enumeration of the full frontier.

### 7.3 The exponential boundary is real but representation-relative

For each j=1,...,n, let one subgoal have two equally strong alternative proofs,
using distinct evidence identifiers a_j or b_j. Add the n subgoals. There are
2^n minimal supports, one selection from each pair, all with the same bound.
No one support includes another, and at alive set S only its exact selection
survives. An explicit irredundant list therefore needs all 2^n supports.

Nevertheless the proof DAG 'n alternatives followed by n-1 additions' has O(n)
size and can be specialized to a given alive set in O(n) elementary choices.
The explosion concerns an explicit response table for every withdrawal pattern,
not necessarily one current proof or a compact procedure. This is the relevant
ATMS/provenance-style antecedent, now with signed quantitative bounds attached;
it is not advertised as a newly discovered combinatorial phenomenon.

### 7.4 Tolerance and restricted withdrawal patterns

If a replacement label (T,c) has T subseteq S and c<=b+delta, it preserves
availability and loses at most delta of this label's numerical strength. If
every removed label has such a retained replacement, the compressed family
satisfies F_compressed(A)<=F_original(A)+delta whenever the latter is available.
The retained bounds themselves remain valid; only strength has been lost.
For all-withdrawal support antichains in 7.3, numerical tolerance alone does not
remove the need to retain different availability possibilities.

For a restricted admissible family of alive sets Acal, the exact support test
can instead be weakened to

    for all A in Acal: S subseteq A implies T subseteq A.

This permits compression when evidence objects are contractually made available
together. Co-availability is not independence or correlation of their *validity*
events. A revised availability contract requires rechecking the compression.
Likewise current numerical dominance must be rechecked after numerical bounds
change: a label dominated at one snapshot need not be dominated forever.

## 8. A smaller checked basis without pretending all rules disappeared

S1 has sixteen implemented rule tags. Ten suffice as a CONVENIENT elaboration
basis for those finite traces:

    constant, row, rewrite, add, scale, convert, lattice,
    max_common, min_common, all_cases.

This is not a proof that ten is the smallest possible number of primitives.
It preserves explicit units and case coverage rather than hiding them inside a
larger algebraic oracle. The other six tags expand as follows.

**Transitivity.** Add t<=s[b] and s<=r[c]. Exact difference normalization gives
(t+s)-(s+r)=t-r. Rewrite to t<=r[b+c]. The middle equality is still checked.

**Reversed negation.** Rewrite t-s as (-s)-(-t), retaining budget b.
No sign change of b is licensed.

**Same-query proof minimum.** At the FIXED numerical snapshot choose the
already checked parent with smaller rational budget, then rewrite to the
requested pair. Keep the source family outside the compiled proof when later
updates matter, as section 6.2 explains.

**Nonnegative slack.** For k>=0, the lattice law

    min(0,k) <=[0] k

and constant comparison k<=[k]0 add to a zero difference with budget k,
because min(0,k)=0. Add that to the original query and normalize. This derives
b -> b+k without an unsound manipulation of exact constant equalities.
A naive attempt to add k to the left and then erase it is not a valid rewrite.

**Maximum congruence.** From a_i<=b_i[p_i], inject b_i into max(b1,b2), then
use expanded transitivity. This gives a_i<=max(b1,b2)[p_i]. The max-common
rule yields max(a1,a2)<=max(b1,b2)[max(p1,p2)].

**Minimum congruence.** Project min(a1,a2) into each a_i, then use the
corresponding a_i<=b_i[p_i]. The min-common rule gives
min(a1,a2)<=min(b1,b2)[max(p1,p2)].

**Residual congruence.** Reverse-negate a_old<=a_new[p], add
b_new<=b_old[q], and compare the resulting inner differences. Use the expanded
maximum congruence with the identical zero term. Residual unfolding then gives
its correct polarity and max(p+q,0) budget. The signed improvement can be lost
at clipping; no negative residual bound is asserted without additional evidence.

Every expansion retains the same expression pair (up to the allowed exact
normalization), unit, case and rational budget as the original constructor.
Elaboration may have a smaller active premise set at zero scaling or a proof
minimum; historical provenance can retain the original alternatives. Each
emitted trace is checked by the existing S1 checker, with a separate basis filter
rejecting any unexpanded derived tag. This is supplied-proof elaboration, not
proof search, an independent checker for all mathematics, or F07 completion.

## 9. Symbolic allowances keep dependence through a repair

Scalar replacement budgets kappa_i can themselves discard shared information.
The same core can represent a pointwise replacement allowance rho_i(y) without
changing the finite-rational BUDGET syntax:

    a_i[sigma] <=[0] rho_i(y).

Let B_P be the budget expression obtained from the old proof's constructors,
with a variable for each source-row bound, its literal constants, and operations
sum, nonnegative scale, min and max. The local symbolic reconstruction gives

    t[sigma] <=[0] s[sigma] + B_P(rho(y)).                (9.1)

One subsequently proves B_P(rho(y))<=[b]0 in the SAME new source and derives
the ordinary finite bound b. Thus no new scalar oracle or variable-product
operator is introduced. The shared dependence is kept as an ordinary native
expression until it is useful to reduce it.

The construction is not merely a semantic assertion: the following expansions
show how its local steps use S1 rules. Rewrite each parent to its difference
form d_i<=[0]rho_i. For addition/transitivity, add and normalize. For scaling,
apply the nonnegative scale and preserve its unit. Reversed negation retains
the same difference. A conversion converts the allowance too. Fixed slack adds
its constant. At a same-query proof minimum, the two parents give

    d<=[0]rho_1,  d<=[0]rho_2;

min-common gives d<=[0]min(rho_1,rho_2). At a maximum comparison, first inject
each rho_i into R=max(rho_1,rho_2), add the common reference term, and use
max-common. For a minimum comparison, obtain t<=a_i+R, subtract R from the
left by an exact difference rewrite, then use min-common and rewrite back.
Residual composition first forms the correct inner difference allowance and
then applies maximum congruence with the unchanged zero; its allowance is
max(rho_1+rho_2,0). None of these steps consults a sampled source valuation.

Global cases need separate treatment: prove the local allowance in EVERY live
case. A common upper expression dominating all local allowances may then be
used. Taking a pointwise minimum of bounds that hold in DIFFERENT cases is
not this construction. The common deployed policy is still fixed.

### 9.1 A minimal example where scalar repair loses the conclusion

Suppose an old two-row proof adds d1<=0 and d2<=0. Current replacement evidence
instead establishes

    d1<=u-3/4,   d2<=1/4-u.

Each allowance is unbounded above when u is unrestricted. Equation (9.1) gives

    d1+d2 <= (u-3/4)+(1/4-u) = -1/2.

This is a proof repair from the same two component contracts, not a supplied
final composite score. Relabeling the second occurrence as an unrelated v
invalidates the conclusion: u-v is then unbounded. Both source meanings and
expression dependence are load-bearing, even though u cancels from the result.

### 9.2 Why 'compile the best proof' has two meanings

With literal rational budgets, min-over-proofs can be compiled by choosing a
smaller parent. With source-dependent rho_1,rho_2, the better parent need not
be known uniformly. The min-common construction above supplies a valid bound
without deciding which argument is smaller at the hidden source assignment.
It chooses neither a hidden action nor a hidden evidence model. Both premises
hold jointly, so the pointwise smaller upper bound is justified.

For x<=u and x<=-u, the resulting -|u| bound retains information that either
fixed branch loses. Replacing these joint premises by alternatives valid in
different hidden cases would reverse the quantifier requirement and destroy
this argument. This is why the stored proof/program interface matters beyond
a numerical equality of min/max functions.

This symbolic construction is specified here as a derived interface with a
worked trace. The general executable adapter below uses finite supplied scalar
replacement proofs; it does not claim an automatic compiler for every symbolic
allowance or every case-dependent interpretation table.

## 10. A neural boundary: switching unbounded bounds is not a harmless gate

Consider a source-free fallback comparison with known finite bound B0 and a
conditional proof with finite but arbitrarily negative bound b. Let a in {0,1}
state whether the conditional proof is operationally available. The desired
best-available bound is

    G(0,b)=B0,    G(1,b)=min(B0,b).                       (10.1)

No globally finite ReLU network, nor any finite term of the selected CPWA
language, can represent (10.1) on both lines for every real b. Such a function
has a finite global Lipschitz constant K: each affine piece has finite slope,
and a finite min/max/add/scale composition preserves a finite bound. But the
two inputs (0,b) and (1,b) stay distance one apart, while their required outputs
differ by B0-b for b<B0. Letting b decrease contradicts K.

The obstruction does NOT rely on asking for a discontinuous value at fractional
flags: only exact Boolean endpoints are required. Nor does it forbid a network
with an external exact branch, a bounded operational domain, a richer language,
or a different representation. It is a closure limit of this particular global
finite CPWA representation of proof availability and unbounded quantitative
strength.

A useful repair needs only a lower bound b>=L, not a two-sided bound. For
L<=B0 choose M=B0-L and define

    G_L(a,b)=min(B0, b+M(1-a)).                          (10.2)

At a=0, b+M>=B0; at a=1 the desired minimum is recovered. Formula (10.2) is
native CPWA and exact on a in {0,1}, b>=L. If all b>=B0, constant B0 suffices.
The bound domain and exact-availability interface must be retained. Feeding
a fractional 'confidence' into a is not a justified half-proof: for B0=0,
L=b=-1 and a=1/2, (10.2) emits -1/2 even though no available proof has been
specified. An uncertainty model over availability must instead be reasoned
through its actual cases or calibration contract.

This connects to the neural research direction as a falsifiable representational
boundary. It is not a statement that an ordinary MLP cannot learn useful loss
comparisons, nor evidence that any network currently implements this proof
selection. Exact evidence administration and quantitative value computation
need not have identical representation contracts.

## 11. Active evidence, arithmetic multiplicity, and probability

For fixed current proof P, a set of named empirical events E_j may establish
its source rows. On their intersection, the conditional mathematical argument
has its stated meaning. Reusing the same source row multiple times does not
multiply the number of distinct validity events, even though its numerical
coefficient increases. If Pr(E_j^c)<=alpha_j, the usual union argument bounds
the failure of that FIXED support by the sum over distinct events.

A data-adaptive selection among supports does not generally inherit the error
bound of whichever support happened to be selected. S1's selection counterexample
remains in force. A simultaneous event for all eligible source procedures,
or a suitable conditional/selection-aware theorem, is needed for that inference.
The support frontier does not by itself supply one.

Likewise an operational a_j=1 (record is present, current and accepted) is not
identical to the world-level event E_j (its modeled assertion is correct).
Missing evidence does not prove E_j false, and present evidence does not prove
it true. Source/proof versioning keeps the arithmetic check honest without
claiming privileged access to final truth. The new rules remain conditional
and compatible with fallible loss estimates.

## 12. Complexity and the boundary of the claims

For one new case, a DAG-localizing/grafting pass needs at most one copy of each
reachable old node and each distinct supplied replacement proof, plus endpoint
rewrites. With explicit memoization of those structural objects, node count is
linear in that combined description. Covering K new cases multiplies the old
skeleton part by at most K. This is a structural node bound, not a bit-complexity
or runtime guarantee: rational coefficient growth, term expansion, repeated
normalization, and serialized sharing have their own costs. The prototype is
an audit fixture, not an optimized search engine.

A flat support frontier can have exponentially many entries (7.3); retaining
and specializing the original circuit avoids constructing that whole table.
Numerical optimality is only over retained proof alternatives. Source-map
availability, satisfiability witnesses, meaningful units, policy legality and
empirical calibration cannot be obtained merely by minimizing proof budgets.

F06 remains partial. This pass does not start F07's global soundness audit,
F08's principal characterization task, F11's complete reasoner, or neural training.
The finite auxiliary arguments here justify specific rule expansions and their
implementation boundaries. Their standard proof-theoretic, lattice, and ATMS
antecedents remain acknowledged; no new mathematical priority is claimed.

## 13. Quantitative assumption discharge: a lost premise becomes an obligation

The previous salvage algorithm can legitimately return 'no retained proof'.
There is also a useful symbolic alternative. A withdrawn inequality can be
replaced by a universally valid relation with an explicit violation cost.
For an affine row a(x)<=eta define

    v(x) = res(eta,a(x)) = max(a(x)-eta,0).

Then

    a(x) <= eta + v(x)                                   (13.1)

holds at every finite assignment. Its zero-budget derivation is particularly
small: inject a-eta into max(a-eta,0), then rewrite the difference to
`a <=[0] eta+res(eta,a)`. No source row is used in that derivation.

Take an old LOCAL proof P of t<=[b]s. Retain the undisputed rows at their old
bounds; replace each withdrawn row by (13.1), and use the symbolic allowance
construction of section 9. If B_P denotes the old proof's literal budget
program, the new result is

    t <=[0] s+B_P(eta+v(x)).                             (13.2)

Here v_i=0 for retained rows and is the positive violation for withdrawn rows.
The constants, operation meanings, policy and source identities in the original
proof are held fixed. Since B_P is coordinatewise nondecreasing and v>=0,

    P_P(x) = B_P(eta+v(x))-B_P(eta) >= 0,

and b=B_P(eta) for that local trace. Thus (13.2) reads

    t-s <= b+P_P(x).                                    (13.3)

This is an explicit quantitative deduction interface: a hypothesis can be
removed at the cost of a remaining expression-valued obligation. A separate
proof P_P(x)<=delta in the current source gives the finite comparison
`t<=[b+delta]s`. Without such evidence or an alternative bound, (13.3) is only
a symbolic guarantee. In particular it does not fill missing evidence with
zero or turn withdrawal into proof that the hypothesis was false.

### 13.1 Why this is more than renaming an uncertainty flag

If the old bound is -1/2, a proved total penalty at most 1/8 retains improvement
of at least 3/8. A penalty at most 1/2 retains non-deterioration; an unbounded
penalty does not yield either guarantee. The penalty has the QUERY'S loss
units and reflects how the proof uses the premise. It is not a universal
measure of how 'true' that premise is.

For q=n x and the premise x<=0, any universal inequality

    n x <= c res(0,x)

needs c>=n when n>=0: set x>0 and divide by x. Reusing the premise n times
really can multiply the consequence of its violation. It does not multiply
the number of independently calibrated empirical events.

### 13.2 A finite affine certificate gives a familiar special case

Suppose exact algebra establishes

    t-s = c + sum_i lambda_i a_i(x),    lambda_i>=0,
    b   = c + sum_i lambda_i eta_i.

Replacing every row by (13.1) and summing gives

    t-s <= b + sum_i lambda_i res(eta_i,a_i(x)).          (13.4)

The argument is an elementary nonnegative combination of inequalities, not a
new optimization theorem. The general proof-budget form (13.2) additionally
retains min/max alternatives and the typed conversions already present in a
finite proof. An ordinary ReLU computation can represent the violation terms;
that fact does not establish that a learned network has these source meanings
or uses them causally.

### 13.3 Presentation changes do not define new epistemic truth degrees

Rescale a row by k_i>0: a_i'=k_i a_i and eta_i'=k_i eta_i. Its violation becomes
v_i'=k_i v_i. In (13.4), transport the coefficient as lambda_i'=lambda_i/k_i.
Both the original bound and the weighted penalty are unchanged. A bare violation
number, by contrast, changes under this presentation. This is why source units,
normalization, and the downstream proof coefficients matter.

For a general proof, explicitly precompose the new row with the inverse scale.
The transported budget program satisfies B'_P(eta')=B_P(eta) and
B'_P(eta'+v')=B_P(eta+v). This is a construction using declared positive scales,
not invariance under arbitrary invertible row mixtures. The latter can lose
inequality information, as F04 already demonstrated.

### 13.4 Keep signed correlated changes when available

Nonnegative violation costs are conservative. They need not be the strongest
repair. For two old component bounds -3/4 and 1/4, current deviations u and -u
have zero sum. Keeping their signed common-source relation proves the old
composite -1/2 bound exactly. Replacing both deviations by their positive parts
instead gives -1/2+|u|, which has no finite bound for unrestricted u.

Thus soft discharge does not replace shared-source symbolic grafting. It is
one safe response to uncertainty about premises. The same calculus should
retain the more informative signed relation when it is actually established.

### 13.5 Alternate proofs cap the damage of a withdrawn premise

If x<=eta1 and x<=eta2 supplied two proofs, withdrawing the first while retaining
the second yields the symbolic bound

    x <= min(eta1+res(eta1,x), eta2).

The second arm always caps it at eta2, independently of the unknown first
violation. At the other extreme, with neither a cap nor a bound on the violation,
there is only a symbolic relation. Hard retention, bounded error, alternative
proofs, and complete lack of quantitative warrant are different cases of the
same explicit construction, not values on a single metaphysical truth scale.

## 14. Checking the symbolic reconstruction constructor by constructor

For a local node j retain an allowance term e_j and a checked comparison

    t_j <=[0] s_j+e_j.                                  (14.1)

Every allowance has the query unit. This invariant is more informative than
merely calculating a scalar budget alongside a proof.

**Constant difference.** If t-s=c, take e=c and use the exact constant-zero
comparison t<=[0]s+c. **Source row.** Either internalize a retained literal bound,
or use (13.1) for a withdrawn row. To internalize an ordinary proof at budget b,
add the constant comparison -b<=[-b]0 and rewrite; the new budget is exactly zero.
No change of semantic relation is hidden inside a normalization step.

**Rewrite / reversed negation.** Rewrite the parent difference while keeping
e unchanged. For negation, t-s=(-s)-(-t), so the same allowance suffices.
**Addition / transitivity.** Add the two zero-budget relations and rewrite to
the new expression pair with allowance e1+e2. **Scaling / conversion.** Apply
the same nonnegative multiplier or named positive conversion to the allowance.

**Fixed nonnegative slack.** For k>=0, 0<=[0]k is a lattice consequence. Add it
to the parent relation, obtaining allowance e+k. Merely moving a finite budget
without the matching constant comparison would be an invalid step.

**Minimum over proofs.** Rewrite both parents as t-s<=[0]e_i, use min-common,
and rewrite back. The allowance is min(e1,e2). One cannot choose an unknown
pointwise smaller branch by comparing the old literal budgets.

**Maximum common target.** Set E=max(e1,e2). Inject each e_i into E, add the
common old expression, and transit through its parent. Both new expressions
are at most old+E. Max-common gives the result at allowance E.

**Minimum common source.** First raise each allowance to E as above, obtaining
new<=old_i+E. Rewrite as new-E<=old_i, apply min-common, and rewrite back.
Again the allowance is E=max(e1,e2), not min(e1,e2).

**Lattice congruence.** For max, inject each old expression into the old maximum,
then use the preceding common-target argument. For min, project the new minimum
into each new expression, compose with its parent, raise allowances to E, and
use the common-source argument. No unproved min/max translation identity is
needed by the emitted proof.

**Residual congruence.** Reverse the first input's comparison, add the second,
and use the max construction with the unchanged zero input. The allowance is
max(e1+e2,0), with exactly the variance of R8. **Unconditional lattice rule.**
Its allowance is zero and no source leaf is needed.

An all-cases step is not an ordinary same-case two-parent constructor. Localize
first, build each local symbolic proof, and then establish an explicitly common
upper allowance before covering all live cases. Alternatively retain a
case-indexed allowance table with its declared semantics. The single-case
implementation must not be reported as automatic handling of the broader table.

The proof of this invariant is constructive: each paragraph is a finite
expansion into the stated S1 rules. A fresh F07 review still has to audit the
ultimate rule set and its full semantic preservation theorem. This local
expansion does not waive that task or claim source calibration.

## 15. A disjoint-violation lemma derivable without a trusted case oracle

For any finite term u of one unit, put

    a=max(u,0),     b=max(-u,0),     m=min(a,b).

The existing rules derive m<=[0]0 without testing the sign of u. Here is a
complete algebraic outline, with every comparison at budget zero:

1. From 0<=a rewrite -u<=a-u; from u<=a rewrite 0<=a-u.
2. Max-common gives b<=a-u.
3. Projection gives m<=a, equivalently 0<=a-m.
4. The other projection and step 2 give m<=a-u, equivalently u<=a-m.
5. Max-common on steps 3–4 gives a<=a-m, equivalently m<=0.

The reverse 0<=m follows from 0<=a, 0<=b and min-common. Thus m=0 is a proved
identity, not a sampled equality smuggled into the normalizer.

For alpha,beta>=0, let K=max(alpha,beta). If K=0 the weighted minimum is an
exact constant. If K>0, projections and nonnegativity give

    min(alpha a,beta b)/K <= a,
    min(alpha a,beta b)/K <= b.

Use min-common, the just-derived m<=0, then scale by K. Consequently

    min(alpha res(0,u), beta res(0,-u)) <=[0] 0.          (15.1)

All divisions here are by a chosen positive RATIONAL K and are ordinary scalar
coefficients, not a new variable-division operator. Both proof branches are
present simultaneously and no policy observes the sign of u.

This lemma provides the algebraic ingredient for a future derived affine case
split: after discharging opposite guards, their two nonnegative violation
costs cannot both contribute. It is worth implementing as a checked auxiliary
trace before introducing a new trusted branching constructor.

## 16. From violation losses to an expected paired-cost statement

A quantitative discharge can connect ordinary loss minimization to a meaningful
use question, but the bridge must be stated. Suppose a local proof and its
discharged hypotheses establish

    q(x) = J_new(x)-J_old(x)
         <= b + sum_i gamma_i v_i(x),    gamma_i>=0.      (16.1)

Here v_i are nonnegative residual violations in named units, converted to the
query unit by the declared coefficients/conversions. If a probability law mu
on the current source is additionally supplied, q is integrable, and the v_i
have finite means, integrating (16.1) gives

    E_mu[q] <= b + sum_i gamma_i E_mu[v_i].              (16.2)

No independence assumption is used: the pointwise inequality is integrated
once, over the shared source. Thus the weighted residual loss can serve as an
upper-bound surrogate for a particular paired use-cost question. Crossing a
negative threshold on the right establishes the corresponding expected
improvement under this declared model. Merely reducing this upper bound does
not show that the actual expected cost decreased on every training step.
The proxy-to-intended-cost premise remains necessary when q itself is only a
proxy comparison.

Three qualifications are mathematically substantive:

* A probability law on source assignments is extra information; it is not
  manufactured by the calculus or silently assumed to be metaphysically right.
* A high probability of zero violation does not bound its expected magnitude.
  A violation N on an event of probability 1/N has mean one for every finite N.
* The full nonlinear budget program generally cannot be evaluated at mean
  violations in place of taking its expectation. For equiprobable (v1,v2)
  equal to (1,0) or (0,1), E[max(v1,v2)]=1 while max(E[v1],E[v2])=1/2.
  The linear majorant in (16.1) is a safe route; a different reduction requires
  its own Jensen/structural hypotheses or joint-distribution calculation.

These are local derivations, not a new statistical calibration method. They
explain what a learned violation-loss predictor would still have to establish.
A neural activation can always be renamed 'a violation of its preactivation
being nonpositive'; that alone supplies no task-grounded interpretation.
The guard meanings, predicted consequence, coefficient relation and useful
intervention tests must be independently specified.

### 16.1 Form the paired quantity before integration

Pointwise finiteness does not imply finite absolute expected loss. Let z be a
nonnegative, finite-almost-sure random variable with infinite mean, and take
J_old=z+1 and J_new=z. Their paired difference is the integrable constant -1.
The equality E[J_new-J_old]=-1 is meaningful; subtracting the two separate
infinite expectations is not. The statement is a coupled paired improvement,
not a claim that extended-real expectations distinguish two infinities.
Using unrelated z values in the two plans would remove this cancellation.

This is another reason to preserve the shared source and the signed comparison.
A universal finite cap on every absolute value is not required for every useful
inference, but the actual operation and its integrability contract cannot be
ignored.

## 17. Toward a derived split, without changing the checking kernel here

A proof-local split on g<=0 versus -g<=0 need not eventually require an opaque
semantic oracle. Suppose the two branches give the SAME query q with bounds
b1 and b2, and quantitative discharge supplies

    q <= b1+c1 res(0,g),
    q <= b2+c2 res(0,-g),       c1,c2>=0.

Put B=max(b1,b2), weaken the two constants to B, and combine the proofs using
min-common. The result is

    q <= B + min(c1 res(0,g), c2 res(0,-g)) <= B,

where the last step is the explicit derivation (15.1). This is a constructive
route to affine sign case reasoning; it does not grant an action the ability
to observe g. Both branch arguments must concern the same deployed policy.
The finite nonnegative c_i can be conservative proof-budget gains, obtained
by sum for additive nodes, positive scaling, and componentwise maximum at
min/max nodes. Tighter gap-sensitive allowances are possible but not required
for this construction.

An empty branch is a different obligation. For parent Ax<=eta and guard
c^T x<=d, a finite Farkas certificate lambda>=0, mu>=0 satisfying

    A^T lambda+mu c=0,   lambda^T eta+mu d<0

certifies that the guarded branch is empty. Parent nonemptiness implies mu>0;
otherwise lambda would certify parent emptiness. From the parent rows one can
then derive

    -c^T x <= lambda^T eta/mu < -d.

Hence the opposite guard holds throughout the parent and only that branch's
proof needs grafting. A missing branch witness alone is not this certificate.
Neither this outline nor a finite branch enumeration changes F05's refusal to
use an empty deployment context as a warrant for arbitrary conclusions.

The split compiler and its empty-branch checker are an explicit remaining F06
question. This pass does not report them as implemented. The disjoint-hinge
trace is useful acceptance evidence for that next step, not completion of it.

## 18. Availability summaries are snapshot-relative, not universal revision caches

The finite antichain in section 7 fixes each proof's numerical budget. It is
exact for removal of available leaves at THAT evidence snapshot. It must not
be silently used as a complete cache after the numerical row bounds change.

For two rows x<=eta1 and x<=eta2, consider the retained alternative proofs

    P: x <= (eta1+3 eta2)/4,
    Q: x <= (3 eta1+eta2)/4.

Both use exactly the same two source rows. At (eta1,eta2)=(0,4), Q gives one
and P gives three, so the snapshot frontier legitimately discards P. At (4,0),
P gives one and Q gives three. Both source contexts are nonempty (x=0 works).
The pruned numeric frontier cannot recover the former alternative. Direct
single-row proofs could do better, but are deliberately not in this retained
proof-family comparison: this is about reuse, not completeness of proof search.

For reusable AFFINE budget forms B_lambda(eta)=lambda^T eta+c, dropping lambda
in favor of mu over a declared update region H is justified by BOTH

    support(mu) subseteq support(lambda),
    sup_(eta in H) [B_mu(eta)-B_lambda(eta)] <= 0.        (18.1)

Support inclusion makes the replacement available whenever the dropped proof
was available. The second clause is exactly the numerical dominance needed
at every allowed snapshot. Each condition has the direct adversarial witness:
activate only the smaller required set to test availability, or choose a bound
vector in H where the inequality reverses. For a fixed pair these conditions
are therefore necessary and sufficient when all availability subsets and all
updates in H are independently permitted. Restricted feasible combinations can
weaken the necessity statement; do not discard that quantifier qualification.

For H=R^m, affine dominance requires equal coefficient vectors and ordered
constant offsets. Otherwise the nonzero coefficient difference can be taken
arbitrarily far in its positive direction. For a rectangular finite region
l_i<=eta_i<=u_i, its exact worst difference is

    c_mu-c_lambda
    + sum_i [d_i^+ u_i + d_i^- l_i],
    d=mu-lambda, d_i^+=max(d_i,0), d_i^-=min(d_i,0).

Thus a cheap, concrete update-domain check is possible. A coupled polyhedral
update region instead admits the existing linear-certificate interface. This
is another ordinary numerical implication, not a new authority granting the
proof selector permission to declare its own source valid.

The executable `support_frontier` deliberately remains a numeric snapshot
operation. `transport` retains the original trace family, rechecks applicable
current leaves, and recalculates bounds. An emitted compiled proof may contain
only the currently chosen branch; keep the original family separately when
future reselection matters. No algorithmic guarantee of arbitrary rediscovery
is made.

## 19. Quantitative source-case extension versus hidden information

There is a useful additional distinction between cases that restrict a COMMON
arithmetic source and cases that change the meaning of the modeled quantities.
Only the first admits the following unconditional comparison.

Suppose local source cases h have rows a_hi(x)<=eta_hi, the same typed source
signature, and the SAME query q(x). Let the h-local proof have literal budget
b_h. Discharging all its numerical row assumptions gives an everywhere valid
comparison

    q(x) <= B_h(eta_h+v_h(x)),
    v_hi(x)=res(eta_hi,a_hi(x)).                         (19.1)

All these inequalities are now valid on the common arithmetic domain, not just
on their former cases. Therefore proof combination yields

    q(x) <= min_h B_h(eta_h+v_h(x)).                     (19.2)

This minimum selects proofs, never a hidden-case-dependent action. On the old
source union, some h has all v_hi=0, so the right side is at most b_h and hence
at most max_h b_h. Outside the union, (19.2) remains a quantitative statement
about violations of the former numeric premises. It does not certify that an
empirical interpretation which was only defined on that union remains valid.

A simple exact illustration uses q(x)=min(x,1-x), case x<=0, and case x>=1.
The old union proves q<=0. After discharging the two guards:

    q<=res(0,x),    q<=res(0,1-x),
    q<=min(res(0,x),res(0,1-x)).                         (19.3)

On the gap 0<x<1, the final expression is the positive triangle min(x,1-x).
At x=1/2, the previous zero bound fails by exactly 1/2. This is not evidence
that an old theorem was wrong: x=1/2 was outside its declared union. The new
penalty makes the extension's loss explicit. For opposite guards g<=0 and
-g<=0 there is no gap; section 15 proves their joint penalty is zero.

Ordinary hidden modes do NOT become interchangeable by this construction. If
h indexes different evaluator versions, conversion meanings, or genuinely
case-dependent queries q_h, every branch must retain that index or supply a
checked interpretation bridge. One may not erase such a distinction by defining
all its numerical violations as zero. The S1 all-cases rule with maximum bound
remains the direct safe operation before numerical guards are discharged.

### 19.1 Why this is a value-related quantity rather than a truth degree

For a fixed proof of q<=b, the residual expression describes how much the
SUPPORTED CONCLUSION may weaken when particular numerical premises fail. Its
units and coefficients depend on the task and the way the premises are used.
It is not an intrinsic metaphysical grade of the premise. Changing the query
or proof can change the useful penalty, and correlated signed replacements can
outperform independent nonnegative penalties.

For affine proof forms one obtains b+sum_i gamma_i v_i. With alternative proofs
having different base bounds b_j, the useful expression is

    min_j (b_j + sum_i gamma_ji v_i),

not b_min+min_j sum_i gamma_ji v_i unless all b_j agree. Equivalently its
nonnegative deterioration relative to b_min is

    min_j ((b_j-b_min) + sum_i gamma_ji v_i).

For example a conditional bound -1 with violation v>=0 and an unconditional
fallback bound 0 give min(-1+v,0)=-res(0,1-v). A small violation preserves some
improvement, and a large violation switches to non-deterioration. This exact
algebra is a possible useful meaning for a ReLU/min computation; merely
renaming an activation as such a penalty supplies none of the source, task,
or causal evidence needed to establish that interpretation.

## 20. A reflective example with a soft proxy premise

Return to the fixed reports r0=1/2 and r1=3/4. Retain s-p<=-1/2 but withdraw
the hard discrepancy premise e<=1/32. Put v_e=res(1/32,e). The checked source
arithmetic and the unconditional comparison e<=1/32+v_e give

    J1-J0 <= -1/32 + v_e.                               (20.1)

This is a useful symbolic conclusion even when v_e is not uniformly bounded.
If a separately declared source law supplies E[v_e]<=1/64 and the paired
quantity is integrable, section 16 gives E[J1-J0]<=-1/64. This expected claim
is not a pathwise guarantee that each use improves. No law or mean bound is
inferred from the controller's own confidence or training score.

For a fully explicit finite illustration, fix p=3/4,s=1/4 and let e=5/32 with
probability 1/8 and e=0 with probability 7/8. Then

    E[v_e]=(1/8)(1/8)=1/64,
    E[J1-J0]=-1/16+5/256=-11/256.

The conservative -1/64 conclusion is true. In the high-e case the realized
conditional expected-cost difference is +3/32, so the corresponding uniform
improvement assertion is false. Both fixed reports' failure-validity claims
are unchanged by this discrepancy law: it modifies the proxy-to-intended-cost
relationship, not the controller's branch probabilities.

This is the specific loss-grounded bridge: a magnitude-sensitive residual loss
can control an intended comparison under explicit assumptions. A binary flag
that e exceeded 1/32, or an uncalibrated predicted residual, cannot substitute
for E[v_e] or a warranted upper bound on it.

## 21. A derived quantitative cut and the size of a premise's influence

One row violation need not pass to the conclusion with coefficient one. Fix a
local trace P using the distinguished row a<=eta. Its budget program B_P is
built from literals, row bounds, addition, nonnegative rational scaling,
min/max, and positive declared conversions. Let v=res(eta,a). There is a finite
nonnegative gain c_P such that the discharged relation has the form

    q <= b_P+c_P v                                      (21.1)

in the common-unit case. A syntax-directed sufficient gain uses 1 for the
selected row, 0 for unaffected leaves, sum for additive/transitive nodes,
nonnegative scaling for scale, and maximum for common-target or common-source
lattice nodes. Residual congruence uses the sum of input gains followed by the
nonexpansive max-with-zero operation. At a minimum over two proofs, one may
retain whichever parent has the smaller OLD literal bound and use that
parent's gain; a tie permits either. This gives a safe majorant, not necessarily
the smallest c_P.

To check the construction, assume each parent budget under the relaxed row is
at most b_i+c_i v with v>=0. Addition and scaling are immediate. For max nodes,

    max(b1+c1 v,b2+c2 v)
      <= max(b1,b2)+max(c1,c2)v.

For a min node choose an old minimizing j; then the new minimum is at most
b_j+c_j v=b_min+c_j v. For max(B,0), its increase is at most the nonnegative
increase of B. These elementary inequalities give the claimed recursion.
The exact term B_P(eta+v), constructed in section 14, can be much tighter.
This gain estimate must not replace it without acknowledging that loss.

With several relaxed rows, carry a nonnegative gain vector. Sum and scalar
multiplication act componentwise; coordinatewise maximum is sufficient for
max nodes. At min nodes retain one old minimizing branch, or keep its whole
symbolic minimum rather than commit to a single vector. The arithmetic uses
the same shared v vector throughout; it does not create independent copies.
For mixed units, retain named conversions in the gain expression. A bare
unitless coefficient does not authorize adding a probability residual to a
monetary residual.

If current evidence proves v<=delta, (21.1) gives q<=b_P+c_P delta. Thus one
can substitute a quantitatively imperfect premise into a preexisting argument
with a justified degradation. If a second argument converts violation of
q<=b_P into degradation of another claim with gain d, then

    res(b_P,q) <= c_P v,
    r <= b_Q+d res(b_P,q) <= b_Q+d c_P v.

The gains multiply through this derived cut. This is a conditional arithmetic
construction; it is not an axiom saying that all assertions are approximately
factive. The two arguments must retain the same interpretations, units and
applicable source context, and their own independent premises must remain
warranted or themselves be discharged.

For a sharp elementary multiplicity counterexample, the row x<=0 proves
2x<=0 by using it twice. At x=1 its violation is one while the conclusion's
violation is two. A provenance SET contains only one source identifier; it
cannot replace numerical use multiplicity. Conversely min(x,x)=x does not
amplify the violation merely because its syntax mentions x twice. The
operation, not textual occurrence count alone, determines the safe grade.

### 21.1 What can and cannot be softened

Numeric row withdrawal leaves a well-defined quantity in the signature while
removing a claimed bound. It admits residual discharge. Removing the meaning
of that quantity, changing the evaluator version, or changing an observation
policy is not the same operation. The old expression may be ill-typed or refer
to a different task; assigning a large numeric residual does not repair an
undefined denotation. Those changes still need a typed interpretation bridge.

Nor is a proof's operational availability the same as its premise's actual
violation. After withdrawing a certificate, the premise might remain true but
unknown. Its modeled residual can then be zero even though the agent has no
warrant that it is zero. The calculus may derive a CONDITIONAL expression in
that residual; the consumer needs an additional bound or source law to turn it
into the relevant unconditional scalar decision. This is exactly where a
learned loss estimate can help, provided its own relation to the residual is
specified and checked rather than assumed.

## 22. Arithmetic substitution is not an observation channel

Fresh reconstruction exposes a boundary that must be retained even when the
same observation IDENTIFIER appears in two context fingerprints. The numeric
adapter substitutes typed terms and proves an inequality about them. It does
not independently verify that a transformed policy can observe every quantity
used to choose its action.

Let sigma map new arithmetic assignments Y to old assignments X. Let O and O'
be their actual observation maps, and pi the old policy. A sufficient explicit
operational bridge is a computable observation translator tau such that

    O(sigma(y)) = tau(O'(y)),
    pi'(o') = pi(tau(o')).                              (22.1)

Then pi'(O'(y))=pi(O(sigma(y))) for every admitted y. The new policy implements
the old choice using only its available observation. A separate cost/behavior
interpretation bridge still relates the chosen actions' modeled consequences.
Neither equal strings for the observation scopes nor a source inequality proves
that bridge automatically.

For a FIXED deterministic pi on finite Y, the weaker exact criterion is

    O'(y)=O'(z) implies
    pi(O(sigma(y)))=pi(O(sigma(z))).                     (22.2)

Necessity follows because one policy must choose one action for each observation.
For sufficiency define pi' on each attained observation to be that common action;
use a declared fallback on unattained observations. This finite construction
needs no omniscient choice at runtime. It can succeed even if (22.1)'s full
observation translator does not exist, because pi may ignore the lost detail.
For all old policies capable of distinguishing any two observations, (22.2)
reduces to constancy of O composed with sigma on O' fibers, which supplies tau.
For infinite observation spaces, computability/measurability of a proposed tau
or pi' is an additional obligation; the finite factorization is not silently
promoted to that broader result.

A counterexample is an old observed bit x in {-1,1}, actions {-1,1}, and
pi(x)=x with loss |pi(x)-x|=0. Substitute x=theta in a new source where theta
is hidden and O' is constant. The arithmetic expression |theta-theta| remains
zero. No observation-legal deterministic policy implements pi(theta): every
fixed action has loss two at one hidden theta. A randomized policy with fixed
probability of the two actions has worst expected loss at least one. Its two
expected losses sum to two, so their maximum cannot be below one; equal
randomization attains one. Numeric substitution did not provide an observation
of theta.

The same condition applies to a finite randomized policy by replacing actions
in (22.2) with their probability vectors. Equality of action laws is enough for
the corresponding conditional EXPECTED cost when the cost interpretation is
fixed. It does not establish identical realized actions under arbitrary random
seed couplings or a pathwise loss guarantee.

This boundary narrows what the executable transport routine claims: its result
is an ordinary checked numerical proof in the new source context, not an
executable-policy certificate. The fixed reflective examples keep the same
rational reports and controller, so their observation bridge is the identity.
No F05 theorem is retracted; its separate action/observation obligations remain
load-bearing. A future code registry must check them explicitly before using a
numeric proof as permission to deploy a transformed program.

## 23. Selected support does not by itself certify statistical confidence

Availability labels track which current source records a proof needs. A count
of the selected records is not automatically an a-posteriori failure-probability
bound, especially when the proof is selected using those records' values.

For a fixed target g=0, take two disjoint events A,B, each of probability 1/4.
A first estimated upper bound is -1 on A and +1 otherwise; a second is -1 on B
and +1 otherwise. Each separately covers g with probability 3/4. Choosing the
smaller bound covers g only with probability 1/2. At each outcome the emitted
proof can cite just one bound, but that does not restore its marginal 3/4
coverage. There is no contradiction with the arithmetic min rule: whenever
BOTH source premises hold, the minimum really is an upper bound.

A simultaneous-validity event over all potentially used source rows gives the
usual conservative bridge. Alternatively a selection-aware or conditional
coverage theorem might be supplied. Their hypotheses are additional empirical
or statistical evidence, not outputs of the proof-frontier algorithm. Numeric
use multiplicity and statistical failure-event multiplicity remain different:
using the same true inequality twice doubles its arithmetic contribution but
does not create two independent calibration events.

The analogous magnitude warning applies to softened assumptions. A row's
violation can be rare but severe; (16.2) requires the relevant mean violation
or another valid magnitude bound. This distinction is useful for a learned
loss proxy precisely because it specifies what must be estimated, rather than
pretending that a confidence number already establishes a cost guarantee.

## 24. A proof-derived lower bound can make finite ReLU availability gating possible

Section 10 rules out a finite ReLU gate for an arbitrarily negative unbounded
input budget with fixed fallback. It does not rule out every evidence-sensitive
neural computation. Softening a fixed proof gives a useful positive example.

Budget monotonicity and v>=0 imply

    B_P(eta+v) >= B_P(eta)=b0.

The lower bound b0 concerns the PROOF'S REPORTED UPPER BOUND, not the absolute
cost it bounds. Its existence does not impose a universal magnitude limit on
modeled values. For a currently available fallback proof q<=F with F>=b0, and
an exact availability indicator a in {0,1} for this optional proof, define

    G(a,v)=min(F, B_P(eta+v)+(F-b0)(1-a)).               (24.1)

If a=1 this is the stronger of the available proof and fallback. If a=0,
B_P(eta+v)>=b0 makes the second argument at least F, so G=F. All operations
are finite CPWA when B_P is; no multiplication of two unknown unbounded
quantities is needed. Thus the domain hypothesis needed by the earlier gate
can itself be a consequence of the proof construction.

For b0=-1, F=0 and B_P(eta+v)=-1+v, (24.1) simplifies to

    G(a,v)=min(0,v-a)=-res(0,a-v).

The positive ReLU output res(0,a-v) is exactly the remaining warranted
improvement in this CONSTRUCTED setup. It shrinks continuously with the
magnitude of hypothesis violation and becomes zero when the optional argument
is unavailable. This is a concrete semantics to test for, not a discovery that
ordinary trained units already implement it.

Two restrictions remain essential. First, unrestricted numerical evidence
improvement can make B_P smaller than its old b0; (24.1) is then no longer a
valid missing-proof gate with that bound. Re-establish a suitable lower bound
or use the explicit symbolic availability layer. Second, a fractional
confidence is not the Boolean a in this theorem. At v=0,a=1/2, the formula
returns -1/2, but a world with only the fallback warrant q<=0 may have q=0.
To handle uncertain availability, retain the corresponding cases or supply a
separate probabilistic consequence model. The arithmetic does not manufacture
source validity from confidence.

## 25. Fresh reconstruction notes and implementation acceptance boundaries

The following are checks of the preceding constructions, not additional
unrestricted claims.

**Local budget baseline.** If a global all-cases proof has budget max_h b_h,
localization may lower it. The nonnegative softening penalty must subtract the
LOCAL reconstructed b_h, not automatically the old global maximum. Otherwise
an unchanged strong branch could be assigned a negative 'violation penalty'.
Every returned softening result therefore identifies the localized base proof.

**Three reflective extrema occur at different source assignments.** Under
3/4<=p<=1, 0<=s<=1/8 and e<=1/32, the intended revision has worst difference
-1/16 at p=3/4,s=1/8,e=1/32. The old report's worst excess is +1/16 at
p=1,s=1/8, while the new report's worst excess is -13/32 there. This checks
uniform bounds separately; it does not merge optimizing assignments into a
purported single physical case or make policy choices depend on them.

**Removing a row is not removing its variable.** Quantitative discharge can
remove e<=1/32 from the assumption list while retaining e in res(1/32,e).
Evaluation of that penalty still needs the quantity or a justified upper
estimate. Current proof-support keys, arithmetic free-source dependencies,
and historical provenance are different interfaces, just as phase one's read
footprints were not identical to its currently cited witnesses.

**Duplicate records.** Two equal numerical rows can have distinct availability
histories. A frontier must retain both singleton supports when neither includes
the other, even when their bounds agree. A single chosen proof can be smaller,
but it is not the same future-withdrawal interface as the retained family.
Row keys are local to a context fingerprint; an index in a different context
is not the same certificate merely because its integer is equal.

**Scope of code acceptance.** New emitters must finish by running the unchanged
S1 checker against their NEW context and must keep all native term typing and
case conditions. Invalid or unresolved transport returns an explicit failure;
it does not mean semantic falsity. Finite example tests exercise off-old-source
assignments after withdrawal so that a 'successful discharge' is not tested only
where its removed assumptions already hold. A single-case symbolic compiler
is not automatically a full hidden-mode or policy-transport implementation.

**Trusted boundary.** Neither deleting derived instruction tags nor grafting
proofs proves that the remaining checker has been formally verified. F07 must
still reconstruct local semantic validity and the final rule language's
composition theorem; F11 must still build its intended reasoner. These F06
fixtures preserve auditable proof evidence without claiming those later tasks.

### 25.1 Structural domain assumptions require an additional interpretation check

The symbolic compiler is an arithmetic construction. Some source rows do more
than report fallible estimates: for example 0<=p<=1 makes p a probability in
the controller interpretation, and 0<=theta<=1 makes a proposed kernel a
probability kernel. Removing such a row yields a larger real-coordinate
context in which the emitted algebraic inequality remains valid, but it does
not automatically extend the probability or executable-domain interpretation.
A deployment adapter must retain the required structural domain or establish
an explicit replacement interpretation. The soft reflective example removes
only the discrepancy bound, retaining the probability rows.

The all-rows-withdrawn regression checks intentionally verify a broader
ARITHMETIC identity, including off-old-source points. They are not examples of
a controller having negative probability or of a theorem certifying that such
a controller can run. This is the same numerical/operational distinction as
the observation-channel counterexample, not a new truth value or a revision
of F05's interpretation contract.

### 25.2 Residual relaxation does not replace joint signed repair

For old rows d1<=-3/4 and d2<=1/4, a summed proof gives d1+d2<=-1/2. Under
new exact relations d1=u-3/4 and d2=1/4-u, signed replacement allowances retain
the exact -1/2 conclusion for every u. Independently discharging the old rows
instead yields the weaker allowance -1/2+res(0,u)+res(0,-u)=-1/2+|u|.
The new numeric source is shared in both constructions; clipping the individual
changes still discards the cancellation. Hence residual discharge is a useful
constructive fallback, not a completeness claim or a mandate to replace all
correlated evidence with separate nonnegative losses.

### 25.3 Finite proof expansion versus efficient storage

Each localized old constructor expands into a bounded number of checked S1
constructors. Reusing parent results gives a number of emitted proof nodes
linear in the old reachable DAG size, apart from explicitly grafted replacement
proofs and repeated case specializations. This is a NODE-count observation,
not a bit-complexity or runtime theorem for the Python fixture.

Allowance terms themselves can share nested min/max/sum subexpressions. A
naive tree serialization repeats shared subterms, and equality normalization
can revisit them. Thus linear proof-node expansion need not give linear JSON
size or checking time. A later implementation can intern typed subexpressions
or use explicit scoped bindings; it must not silently identify different source
or lexical environments. The current finite fixtures do not establish a general
advantage over continuation semantics.

Likewise the symbolic compiler deliberately preserves some syntactically used
retained leaves even when a later zero multiplier makes them mathematically
irrelevant. The separate constant-pruning/salvage routine can remove such a
use. A root-reachable source set is therefore a sufficient dependency interface,
not proof that every member is necessary for the semantic conclusion.

### 25.4 A useful finite alternative when exact action transport fails

Failure of exact observation factorization need not end the comparison. For a
finite new observation fiber Y_o and the old desired action a*(y), a common
new action a preserves cost within delta exactly when

    C(y,a)-C(y,a*(y)) <= delta for every y in Y_o.

Thus a deterministic repair exists iff the corresponding allowed-action sets
have nonempty intersection in each observation fiber. This criterion is both
necessary (one legal action must serve every hidden y in the fiber) and
sufficient (choose the witnessed action for that observation).

For a randomized finite policy, replace the action by ONE probability vector
p_o on actions and require

    sum_a p_o(a) C(y,a)-C(y,a*(y)) <= delta,  y in Y_o,
    p_o(a)>=0,  sum_a p_o(a)=1.

These are finite linear feasibility conditions for an explicitly common policy.
A supplied solution is a checkable expected-cost repair, not an observation of
y. In the hidden-bit example, exact transport fails, deterministic worst loss
is two and equal randomization has loss one in each hidden state. Relative to
a named fallback of cost three in both states, that randomized policy still
improves expected cost by two. The unavailable perfect-information zero-cost
policy is used only as a mathematical reference, not quietly deployed.

If an old comparison gives budget b and the new observation-legal policy has
this additional cost delta relative to the transported reference, transitivity
adds delta to b (plus any separately required baseline interpretation error).
A useful strict improvement can therefore survive information loss when its
margin exceeds the checked degradation. This is a finite minimax-style
construction, not a novel general policy-transport theorem or an implemented
policy optimizer in this pass. It records a positive next option alongside the
exact-factorization obstruction.

The residual used throughout has a simple least-repair interpretation: for
finite a,eta, res(eta,a) is the least delta>=0 for which a<=eta+delta. Any such
delta must dominate both zero and a-eta, and their maximum itself suffices.
This pointwise minimality does not imply that summing independently minimal
row repairs gives the strongest composite proof; the correlated signed repair
counterexample in 25.2 shows exactly why not.

## 26. Executed scope of this checkpoint

The [transport fixture](../checks/f06_source_transport.py) implements supplied
proof grafting, local-case specialization, numeric withdrawal salvage, finite
support frontiers, and six-rule expansion into the ten-tag checking basis.
Its 40 development tests pass. The [discharge fixture](../checks/f06_residual_discharge.py)
implements the single-case symbolic construction in section 14 for every local
S1 constructor after localization, and emits the weighted disjoint-hinge proof
from section 15 without a new trusted instruction. Its 24 tests pass.

The two modules add 64 cases; combined F06 discovery contains 122 cases. These
counts are development checks, not exhaustive validation of unrestricted
mathematics. The recorded process runs and reports are linked from
[the session record](../work_logs/F06_2026-09-27_S2.md).

The finite observation-factor helper checks a supplied complete finite table
only. It is not a checker for arbitrary programs, observation maps, or unknown
source populations. No general splitter, empty-branch search, quantitative
policy optimizer, learned neural experiment, or statistical calibration method
is implemented. Existing S1 code and earlier research are unchanged.
