# F07 S2 — proof producers, current requests, and operational meaning

Status: **partial F07 reconstruction**, not task completion. Input revision:
`fbdd4ac9d714aed4e39188cc71bd28ba5255f1e9`. Date: September 28, 2026 UTC
(September 27 in America/Los_Angeles).

The native soundness theorem in [03_soundness.md](03_soundness.md) is the
starting premise of this audit. The question here is different: when a routine
transforms an old proof, does its returned trace, its advertised allowance, and
its caller's current request describe the same mathematical assertion? The
answer requires postconditions on producers as well as validity of individual
rules. Nothing below promotes a producer to a new trusted inference rule.

## 1. Three levels of correctness

For a finite accepted K trace P, write its root as `(C,h,t,s,b)`, meaning
`t(x)-s(x)<=b` throughout the indicated case domain (or the union for a global
root). Distinguish:

1. **Trace soundness:** that root is true under C's mathematical assumptions.
2. **Producer correctness:** that root and any extra metadata satisfy the
   producer's contract relative to its independently fixed inputs.
3. **Use correctness:** the root concerns the actually requested program pair,
   permitted information and intended criterion, and the source interpretation
   is applicable to that use.

These are not interchangeable. A constant proof of `0<=0` is a sound trace but
is not a successful repair of a request for `x<=-1`. A correct conditional
inequality between real expressions need not denote a legal randomized program
if its probability premises have been removed. A version label binds a claim
but does not empirically establish that the label describes the world.

### P1 — request-bound acceptance, independent of producer ingenuity

Fix a current context C and a requested root R=(C,h,t,s,b) **before inspecting
the candidate output**. Let an arbitrary terminating procedure return P.
If the receiver checks P under C, checks exactly the requested term pair,
unit and local/global scope, and accepts only when `root(P).budget<=b`, then
acceptance implies the independently defined semantic assertion R.

**Proof.** The native theorem gives `t_P-s_P<=b_P` on the root's domain.
The equality checks identify its pair, unit and domain with those of R.
The checked rational inequality `b_P<=b` gives R by order transitivity. The
argument says nothing about how the procedure found P. A timeout, exception,
invalid trace, different request, or inadequate bound is not acceptance. ∎

The receiver must not derive R by copying the returned root. That would test
only (1), not whether the requested operation was accomplished. Likewise,
checking a proof of `t<=s+E` does not by itself establish that a separately
returned field called `penalty` equals E minus the original bound.

## 2. Pruning and localizing a checked proof

All parent indices in K point strictly backward. The ancestors of a root are
therefore a finite set closed under taking parents. Sorting those indices gives
a topological order; replacing them by consecutive indices is an order-preserving
bijection on the retained graph.

### P2 — pruning preserves a checked root

After first checking P, discard nonancestors and remap the retained indices.
The resulting trace checks and has the same root terms, scope and budget.

**Proof.** Every retained parent is retained and occurs earlier. Induct over
the remapped order. Its rule name, parameter values, context, expressions and
parent claims are unchanged, so the same local check succeeds. The root is
retained by definition. This operation does not salvage an initially invalid
trace with an invalid unused node: the existing routine checks its input first. ∎

### P3 — localization and the bound it actually produces

Fix a live case h. A global proof can be specialized to h by replacing every
`all_cases` node with its h-parent (and an exact rewrite to the old node's literal
pair), and relabeling source-free global operations and their selected parents
as local to h. A proof already local to h is treated similarly. A proof local
to a different case is not an admissible input.

The localized root has the original literal pair, contains no `all_cases`
node, and has budget b_h no larger than the original budget b.

**Proof.** At a case-union node its selected h-parent establishes the literal
pair on D_h, and its budget is at most the maximum used by the old global node.
Every other rule has a monotone budget operation: identity, sum, nonnegative
scaling, positive conversion, addition of fixed slack, minimum, maximum or
`max(sum,0)`. Thus replacing parent budgets by smaller ones cannot increase the
result. The strict-backward graph and recursive case selection ensure that no
foreign local row enters the specialized proof. Exact root rewrites preserve
its pair. Induction gives both validity and b_h<=b. ∎

The inequality may be strict. If two cases prove the same query with bounds
0 and 2, the global bound is 2 and localization to the first has bound 0.
A subsequent discharge must use **0 as its original local budget**, not copy
2 from the old global root. The local baseline is independently reconstructible
by the displayed budget recurrence with case-union nodes replaced by selection.

## 3. Source substitution and grafting

The [first pass](03b_graded_soundness_reconstruction.md#6-reconstructing-source-grafting-without-assuming-source-inclusion)
proved semantic substitution and proof-local grafting. Here the implementation
contract is reconstructed explicitly.

A source substitution assigns every old source coordinate a closed target term
of the same unit. It is simultaneous, not recursive rewriting of inserted terms.
Unit and conversion interpretations are fixed. For a target point x', the old
coordinate z is interpreted as `E_x'(sigma(z))`. The normalizer is compatible
with that substitution: substitute normalized target forms in old source keys,
rebuild nonlinear keys, and collect rational coefficients. Structural induction
on terms, strengthened to captured local environments, proves that this is
normalization of the substituted term. Consequently every old exact rewrite,
common-middle check, and algebraic cancellation survives the substitution.

For each target live case k, a case map selects an admissible old case h(k).
Localize first. Each used old affine row has the normalized form `a_i<=eta_i`.
A supplied target proof must establish the **substituted old expression**
`sigma(a_i)<=beta_ki`; merely citing a target row with the same integer index
is insufficient. The replacement may be weaker or stronger than eta_i. If its supplied proof is
global, beta_ki is the budget AFTER localizing that proof to target case k.
Its unlocalized global budget is conservative but need not be the value actually
used by the producer. This qualification was made explicit in the fresh S2 review.

### P4 — successful grafting has a current, not historical, bound

For the nonoptimizing reconstruction, replace each row leaf by its checked
current proof, substitute in all term-valued rule parameters, and recalculate
budgets through the old local constructors. Let B_h be the localized budget
program. The target local root has pair `(sigma(t),sigma(s))` and budget
`B_h(beta_k)`. The global union has that same literal pair and the maximum
of its new local budgets. Every target live case must occur exactly once.

**Proof.** Replacement leaves check in the target case and have the required
normalized difference. The substitution lemma preserves the algebraic shape
conditions of each parent rule. Recomputing rather than copying the budget
makes each new step satisfy its native check. Index-offsetting a finite inserted
trace preserves backward references. Induct over the localized ancestor DAG,
then apply `all_cases` to the identical pair over all target cases. ∎

The actual producer also permits two conservative optimizations:

- If a substituted difference normalizes to a constant, emit its constant
  proof without requiring the old leaves. This can recover a source-independent
  consequence after its old derivation's assumptions disappear.
- At `meet_proofs`, keep any available proof of the identical query and use the
  strongest available current bound. Failure of one alternative is not failure
  of the other.

For a precise partial-success specification, give each node either `Absent` or
`Bound(b)`. Test the constant case first; at a row consult the replacement map;
at a proof-meet take the minimum of the nonabsent entries; at other constructors
require all parents and apply their budget operation. This describes the
producer's declared salvage strategy, not all semantically valid arguments.
Successful output has the bound of this reconstruction. Failure does not prove
that the requested conclusion is false or unprovable by another method.

Nonempty target domains are important even for comparisons of bounds: a
constant-c proof and another accepted proof of the same difference must satisfy
`c<=beta` there. A supposedly stronger contradictory replacement could not be
accepted on a nonempty source. Neither optimization obtains conclusions from an
infeasible deployment context.

### Scope retained and scope not supplied by P4

P4 does **not** require target assignments to satisfy every unused old row.
It also does not show that a changed policy sees the same information, that old
probabilities still describe report-induced behavior, or that a loss has kept
its physical interpretation. The current API rejects changed scope and
observation identifiers absent a separate bridge. Equality of those identifiers
is an identity check, not independent verification of their real-world meanings.

## 4. Primitive expansion is a fixed-snapshot transformation

`compile_primitives` removes six convenience tags while keeping a ten-tag
checking basis. The replacements can be audited without treating the compiler
as an oracle:

- `trans`: add the comparisons, then cancel the common middle by rewrite;
- `negate`: rewrite the same signed difference with its terms interchanged and
  negated; do not multiply an inequality by a negative scalar without reversal;
- `slack`: add a checked source-free comparison with exactly the specified
  nonnegative budget;
- `meet_proofs`: choose a least-budget parent at this snapshot and rewrite it;
- min/max congruence: compose lattice projections/injections with the two
  premises, then use the corresponding common-side operation;
- residual congruence: rewrite its contravariant input, add, and use maximum
  congruence with the zero comparison.

### P5 — macro expansion preserves the current root

Every successfully expanded trace checks in the old context, uses only the
specified primitive tags, and has the identical root pair, scope and budget.

**Proof.** The displayed constructions have the native tag's numerical effect.
Every primitive copy preserves its old check. Induct over the finite memoized
ancestor recursion. The producer explicitly compares each expanded node budget
to the old one, and the final primitive-only checker rejects unexpanded tags. ∎

This does not assert preservation of all future sensitivities. In particular,
choosing one proof at a current minimum discards an alternative whose bound or
availability may be preferable later. A current equivalence of derivations is
not an equivalence of their possible future repairs. Retaining the higher-level
input and recompiling is a different operation from replaying a chosen expansion.

## 5. Exact metadata for numerical premise discharge

Fix old context C, selected case h, explicit withdrawal indices W, and a
caller-specified new revision identifier. Define C-W by deleting exactly those
rows in h, in their original order, retaining the other cases, signature,
observation contract and feasible witnesses. It remains nonempty: old witnesses
still satisfy the retained rows.

Independently localize the root's budget recurrence. For a retained normalized
row use the literal eta_i; for a withdrawn row use

    E_i(x) = eta_i + max(a_i(x)-eta_i,0).

At every other node apply the bound-program operation from G1. Let E_P be the
result and b_h the original localized bound. Define `Penalty_P=E_P-b_h`.

### P6 — discharge contract, including its auxiliary fields

The output contract is a K trace under C-W, local to h, with the original new
term t and old term `s+E_P`, budget zero, together with:

    allowance = E_P,
    penalty = E_P-b_h,
    old_local_budget = b_h,
    withdrawn = sorted(W).

Exact normal-form equality is an acceptable way to compare equivalent allowance
presentations, but the current context, selected rows and requested original pair
must be fixed independently of those returned fields.

**Construction proof.** At a withdrawn leaf, lattice injection proves
`a_i-eta_i<=max(a_i-eta_i,0)`; rewriting gives `a_i<=E_i` with budget zero.
At a retained leaf internalize its literal bound by adding its negative as a
constant comparison. Addition, transitivity, scaling and positive conversion
propagate the allowance algebraically. Rewrite and sign reversal preserve its
signed difference. A proof-meet combines two globally applicable bounds by
minimum. Lattice/common-side rules first raise their two allowances to a shared
maximum and then apply their zero-budget lattice derivation. Residual congruence
adds the two inner allowances and takes their maximum with zero. Fixed slack
adds its nonnegative literal allowance. Each construction ends in the original
node pair with the allowance on its right, and every emitted step is a native
K step. Induct over the localized DAG. The final root and the four fields have
exactly the stated meanings. ∎

The mathematical inequalities `Penalty_P>=0` and zero penalty on all old used
premises follow from G1–G3, **after** verifying that this is the promised E_P.
A valid trace with an unrelated extra field called `penalty` would not establish
those properties of that field. The new audit receiver therefore reconstructs
the allowance separately and checks the metadata, not just the returned trace.

Allowances can have negative baselines even though their excess over b_h is
nonnegative. The intended inequality is `Delta<=b_h+Penalty_P`. Replacing it by
`Delta<=Penalty_P` would discard a useful improvement; replacing it by
`Delta<=b_h` would silently assume the withdrawn evidence again.

## 6. Certified sign cases and imperfect coverage

A live sign branch must have exactly the parent rows plus the stated guard,
the same signature/observation interface, and its own feasible witness. This
is not permission to add whichever premises make the branch proof easiest.
Both branches must concern the same literal requested comparison.

Discharging the extra guard produces, on the common parent domain,

    Delta <= A + alpha*max(u,0),
    Delta <= B + beta*max(-u,0),

with alpha,beta>=0. The envelope construction has a separate induction invariant:
its baseline is the allowance evaluated at zero guard violation, its error is
exactly `gain*hinge`, and native traces prove both the advertised upper enclosure
and nonnegativity of that error. Its min/max step uses the larger child gain,
not an invalid sum or an arbitrarily chosen derivative at a kink.

At least one opposite hinge vanishes. Hence the two globally applicable
allowances imply `Delta<=max(A,B)`. F06 constructs an ordinary K proof of that
statement. No semantic case rule has been added to the trusted checker.

### P7 — an excluded branch requires a direction and a strict margin

Let parent normalized rows be `a_i<=eta_i` and let `g(x)=c(x)+d` be a guard.
Suppose supplied nonnegative weights w and strictly positive k satisfy

    sum_i w_i a_i + k c = 0,
    sum_i w_i eta_i - k d < 0.

Then the parent proves

    -g <= (sum_i w_i eta_i)/k - d < 0.

**Proof.** Add and scale the parent rows to bound `-c`, divide by positive k,
and add the constant -d. The displayed equality is an exact coefficient
identity, not a sampled relation or a floating-point tolerance. ∎

Thus `g<=0` is impossible in the nonempty parent and the opposite guard holds
strictly. Its current proof replaces the surviving branch's guard premise.
The resulting bound can be **stronger** than the old live-branch budget;
the correct return postcondition uses `<=`, not a claim that the two budgets
must be identical. Two empty branches cannot dispose of a nonempty parent.

A tiny omitted coefficient multiplying an unbounded source is not a small
constant error. For `epsilon*x` and arbitrary finite x, no uniform bound follows
from small epsilon alone. Exact ray checking is a soundness condition; a domain
bound or another explicit residual is needed for approximate coefficients.

### P8 — weighted imperfect coverage, reconstructed independently

Suppose k_i,w_i>0 and native proofs under one common parent establish

    Delta <= A_i+k_i*max(g_i,0)  for each i,
    sum_i w_i g_i <= eta.

Put `H=sum_i w_i/k_i` and

    M=max(max_i A_i, (eta+sum_i w_i*A_i/k_i)/H).

Then `Delta<=M`.

**Proof by contradiction.** If Delta>M, then Delta>A_i for every i. The i-th
allowance requires `max(g_i,0)>0`, hence `g_i>=(Delta-A_i)/k_i`.
Multiplying by w_i and summing gives
`sum_i w_i g_i >= Delta*H-sum_i w_i*A_i/k_i > eta`, contradiction.
All quantities are finite and H>0, so the strict comparison is legitimate. ∎

The emitted derivation instead uses shifted hinges, a minimum of globally valid
bounds, lattice projections and a checked weighted average. These two arguments
provide different reconstructions of the same contract. Zero gains are not
silently divided by: they require a separately valid constant-bound case, which
the current weighted producer deliberately leaves outside its positive-gain API.

The proofs may differ among cases; the policy must not. Native expression
minimum computes a numerical bound, not a hidden observation revealing which
program to execute.

## 7. Static support labels versus case-local proof reconstruction

A fixed proof graph has a finite **salvage grammar**: retain its constructors,
replace source leaves by available current proofs, select either child of a
same-query proof minimum, and use source-free constant/zero simplifications.
For a fixed numerical snapshot, represent a stored alternative by `(S,b)`:
S is the finite set of used row identities and b its bound. It is available
under alive set A exactly when S is contained in A.

### P9 — label pruning is sound and exact for the stated grammar

If `T subseteq S` and `c<=b`, then `(T,c)` can replace `(S,b)` for every alive
set. At a mandatory constructor, supports combine by union and budgets by the
constructor's monotone operation. At a proof minimum, combine alternative
families by union. Removing dominated labels at any step preserves the best
available root budget within this grammar. The exactness claim is conditional
on the declared finite computation finishing without its explicit work/size
limit being exceeded; a resource refusal is not an available bound.

**Proof.** Any alive set containing S also contains T, and c is at least as
strong a bound. Union with another support preserves inclusion. Every native
budget operation is nondecreasing in each parent, so replacing a parent label
by a dominating label cannot worsen any resulting label. Conversely, every
unpruned label has a finite construction from its parent labels and hence a
proof skeleton; the finite induction generates exactly the grammar's choices.
Testing each alive set shows that pruning preserves its minimum. Sharing a
premise does not turn two arithmetic uses into independent evidence events;
its numerical contribution still occurs twice where addition calls for it. ∎

An unavailable minimum may be denoted +infinity **in this external availability
calculation only**. No K term or emitted budget contains infinity. Zero scaling
can use the source-free zero proof even when its old parent is unavailable.
Failure to find an available label is not semantic refutation or full proof-
search failure.

### 7.1 A crucial scope distinction

The graph-specific `support_frontier` calculation is not automatically the
same optimization problem as `transport`, which first localizes a global proof
for each target case and only then salvages it. Localization can move
worst-case case aggregation later, preserving information about which case
made each intermediate bound large.

For an explicit example, let two cases have the rows

    case a: x<=0, x<=1,
    case b: x<=1, x<=0.

Every case has witness x=0. Build global proof P0 using row 0 in both cases,
with bound 1, and global proof P1 using row 1 in both cases, also with bound 1.
Their proof minimum is a global proof of the same literal pair `(x,0)` at 1.
Now retain only row 0 of a and row 1 of b.

Neither complete P0 nor complete P1 survives as a global stored alternative.
The unlocalized static frontier reports no available label. But after
localization, case a retains its row-0 proof at 0 and case b retains its row-1
proof at 0. Joining these current local proofs gives the GLOBAL bound x<=0.

This does not let an action see a hidden case. Both arguments prove x<=0;
only the evidence used to justify it differs. It also does not refute P9:
localization followed by reselection is a richer reconstruction grammar than
selection among the original globally aggregated skeletons.

### P10 — casewise support correctly matches the localized strategy

For a global input P, let P_h be its localization to each live case h. Compute
its local salvage optimum F_h(A), retaining only rows in A that belong to h.
If every F_h(A) is finite, local reconstruction followed by `all_cases`
produces the same literal pair with bound

    F_case(A) = max_h F_h(A).

It is the least bound for this **case-localized** salvage strategy with the
fixed supplied replacements and snapshot. If any required local optimum is
unavailable, that strategy fails rather than discarding the case.

**Proof.** P3 makes every P_h a valid local starting skeleton. P9 supplies the
least available local bound and its finite proof. Every global joining of those
local reconstructions must take their maximum, which is monotone and minimized
by choosing the least local value. The native rule then proves the global
conclusion. The converse is relative to this grammar: a missing local
reconstruction leaves its case uncovered by the prescribed procedure. ∎

The same distinction affects precision without any withdrawn rows. In case a
let x<=0,y<=2, and in case b let x<=2,y<=0. Adding the separately aggregated
global bounds yields x+y<=4. Localizing before adding and then joining yields
x+y<=2. Both proofs are sound; retaining case alignment yields the stronger one.

Where a fixed list of candidate whole proofs is under comparison, the underlying
order is the familiar finite inequality

    max_h min_i b_hi <= min_i max_h b_hi.

Unavailability can make the right-hand side infinite while the left-hand side
is finite. The legal interchange here concerns **proof witnesses of one fixed
query**, not choices of program that require hidden observations.

### 7.2 A practical audit consequence

A caller may use a static support frontier as a conservative quick rejection
of that specific stored grammar, but must not label it an exact specification
of the more capable case-localizing producer. The new tests compare both
algorithms on the separating example. The existing implementation and its
previously stated snapshot/grammar limits are retained; this audit adds the
missing cross-algorithm comparison rather than weakening an old test.

## 8. Composing transformations and preserving the source recipe

Closed simultaneous source maps compose. If sigma maps old coordinates to
intermediate terms and tau maps intermediate coordinates to final terms,
`(t[sigma])[tau]` and `t[sigma;tau]` have equal denotations, where the composed
map sends z to `sigma(z)[tau]`. Structural induction with lexical environments
proves this even when inserted terms contain nonlinearity or names also used
by binders: inserted terms are closed, and source/local namespaces are distinct.

For a nonoptimizing proof graft, the corresponding budget composition is

    B_P(B_Q1(zeta), ..., B_Qm(zeta)),

where Qi is the intermediate proof of old row i. Induction on P gives exactly
the same root budget as expanding the grafted proof and then replaying it.
An explicit typed map is indispensable; matching strings or numerically
inverting an aggregated evidence vector is not that map.

Optimization changes this statement. Suppose a proof minimum selects x<=-2
over x<=-1 at an intermediate snapshot, and the emitted trace keeps only the
first argument. At a later snapshot its corresponding row weakens to x<=1
while the alternative remains x<=-1. Replaying the selected emitted trace can
return +1, while recompiling the retained original family returns -1.
Both are correct under the new context. A receiver asking for non-deterioration
must reject the first; mathematical validity alone does not preserve the
strongest obtainable current bound.

Consequently the architecture must distinguish:

- an emitted proof of one current requested result;
- its original reusable recipe or family, when future reselection is intended;
- source meanings and observation information needed to interpret the result.

This is a contract distinction, not a requirement to retain every possible
proof or re-run all earlier computations.

## 9. Serialization, finite resource failures and the algorithm theorem

The existing term-DAG format stores each term after its children and each proof
step with backward parent indices. For an accepted proof, encoding and decoding
preserve all constructor tags, rational values, names, units, parameters,
expression pairs and parent relations. Structural induction over the term table,
then over the proof table, proves structural round-trip equality. Sharing
identical syntax under different lexical environments remains safe: each let
still supplies its own captured environment, and the normalizer/evaluator does
not memoize a local expression without that environment.

The decoder checks the returned proof under the actual current context. It does
not authenticate an external meaning merely by seeing a context fingerprint.
It can contain unused term-table entries which are not part of the returned
proof; correctness concerns the actual terms reached by its steps. Input size,
node count and term-occurrence limits may reject otherwise valid results.
Such rejection, recursion exhaustion or unavailable output is not acceptance.

### P11 — composed checked producer boundary

A pipeline may prune, localize, graft, discharge, expand macros, compile cases,
serialize and decode in any combination for which the corresponding input
contracts hold. Each successful stage must either establish the requested
postcondition from its inputs, or have its returned trace and metadata checked
by an independent receiver for that stage. If the final current receiver accepts
the original externally supplied target request, the numerical target holds
under its declared domain. No correctness of an unchecked search heuristic is
needed for that conditional conclusion.

**Proof.** Use P2–P8 and the round-trip lemma for trusted mathematical
transformations, and P1 for independently received outputs. Their contexts,
terms and budgets are the intermediate contracts, not inferred from hoped-for
behavior. Finally apply P1 to the final requested root. ∎

P11 is partial correctness of successful checked outputs, not a proof that a
resource-limited implementation always succeeds. It also does not turn a
source, policy identity, or field named `confidence` into an empirical theorem.

## 10. A quantified interpretation defect is not a vague confidence discount

The preceding results certify transformations of exact mathematical arguments.
An additional question is whether a changed or approximate interpretation can
be assessed without declaring everything either perfect or useless. The answer
is conditional: one can propagate **specified numerical discrepancies**, but not
replace missing meanings or undefined operations with an arbitrary confidence.

Fix a LOCAL accepted trace. For node j let b_j be its original checked budget
and let Phi_j be its native budget operation. At a row leaf Phi_j is its literal
row bound; at a constant it is the exact constant difference; at a lattice leaf
it is zero. Nonleaf operations are identity, sum, nonnegative scaling, positive
conversion, fixed nonnegative slack, minimum, maximum and positive part of a
sum. Each Phi_j is monotone in its parent arguments. The local restriction is
important: an `all_cases` step describes a union of domains, not simultaneously
true numerical premises in one arbitrary assignment. Localize before applying
the following statement.

Suppose d_j is a finite real interpretation of the difference at each node,
with the declared unit, and independently supplied eps_j>=0 satisfy

    d_j <= Phi_j((d_p)_(p in parents(j))) + eps_j.               (D1)

At a leaf this compares d_j to its declared literal bound. Define

    U_j = Phi_j((U_p)_p) + eps_j,
    E_j = U_j-b_j.                                              (D2)

### P12 — local-defect propagation

Under (D1), every node satisfies `d_j<=U_j=b_j+E_j` and `E_j>=0`.

**Proof.** At a leaf, (D1) is exactly the first inequality in the claim and
U_j=b_j+eps_j>=b_j. Suppose both conclusions hold at all parents. Monotonicity
and (D1) give

    d_j <= Phi_j(d_parents)+eps_j
        <= Phi_j(U_parents)+eps_j = U_j.

The native snapshot identity gives b_j=Phi_j(b_parents). Since
U_parents>=b_parents and eps_j>=0,

    E_j = eps_j+Phi_j(b_parents+E_parents)-Phi_j(b_parents) >= 0.

The strict-backward finite graph supplies the induction order. Shared parents
are evaluated once but can enter the same arithmetic constructor twice. No
independence of eps values is used. ∎

For the exact declared term interpretation, every nonleaf eps_j can be zero;
row violations then recover the earlier assumption-discharge theorem. For a
changed interpretation, small eps_j values are **additional quantitative
premises**, not consequences of the old proof or of the name of its evaluator.
Defining eps_j to be the positive part of the left-minus-right difference in
(D1) proves existence of such quantities, but gives no useful upper bound on
them. Their estimation or certification is separate work.

This is a monotone-circuit error argument, not a new trusted rule, a new proof
of the original kernel, or a claim of novel numerical analysis. Its audit role
is to state exactly what would make 'approximately preserving the rule's
meaning' sufficient for a quantitative conclusion.

### 10.1 A finite linear outer allowance

There are nonnegative coefficients C_jk, indexed by local error sites k, with

    0 <= E_j <= sum_k C_jk eps_k.                               (D3)

Construct them in topological order. At a leaf use the unit vector at j.
At every other node start with a unit coefficient for eps_j and add the
propagated parent coefficients. Identity, rewrite, negation and slack retain
the parent coefficients; scale and conversion multiply them by their positive
factor. Addition, transitivity and residual congruence add the two vectors.
For a two-parent minimum or maximum take the coordinatewise maximum of the
parent vectors before adding the j-th unit vector.

**Proof.** Identity and affine constructors follow by substitution in (D2).
For either min or max and nonnegative a_1,a_2,

    Phi(b_1+a_1,b_2+a_2)-Phi(b_1,b_2) <= max(a_1,a_2).

Since eps_k>=0, the maximum of the two parent linear allowances is at most
`sum_k max(C_p1k,C_p2k) eps_k`. For a residual positive-part operation, the
increment is at most a_1+a_2. These are precisely the stated recurrences. ∎

The exact E_j can be substantially smaller than this linear envelope. For a
same-claim proof minimum with old budgets (-1,0), increasing the first proof's
allowance by 2 and the second by 0 gives the new bound 0, not 1. The strongest
original improvement is lost, but the alternative proof prevents deterioration
of the conclusion above zero. A linear envelope can be deliberately conservative.

D3 is a statement about quantitative error magnitudes. If its errors are
random and integrable, expectation can be taken afterward. Reusing one error
site twice doubles its arithmetic influence but does not create two independent
error events. Confidence multiplication or a new per-use failure probability
would need a different argument.

### 10.2 Signed changes and correlation are not automatically errors

A known signed change delta_j can replace eps_j in (D1) and (D2); monotonicity
still proves d_j<=U_j. But E_j need not be nonnegative, and the positive-error
bound (D3) does not apply unchanged. Retaining a common signed source can be
strictly sharper than replacing its two occurrences by independent absolute
errors. Thus a modest interpretation should not erase justified dependence
merely to obtain a uniform nonnegative 'uncertainty' label.

## 11. A surviving cost comparison can coexist with a failed report

Consider the fixed two-branch controller: its emitted report r is also the
probability of selecting its second branch. Let p,s be the branch failure
probabilities. Its modeled failure is

    H_(p,s)(r)=(1-r)p+rs.

A fixed additional use cost c for the second branch gives

    J_(p,s)(r)=H_(p,s)(r)+cr+z,

where a common finite but otherwise unbounded z is permitted. Compare the
SAME two report-dependent policies r0=1/4 and r1=1/2, with c=1/8.

At the first source point (p,s)=(1/4,0),

    H(r0)=3/16, H(r1)=1/8,
    J(r1)-J(r0)=(r1-r0)(s-p+c)=-1/32.

Both reports upper-bound their own failure probabilities. Now change the source
to (p',s')=(3/4,1/2), so both branch probabilities increase by 1/2. They remain
valid probabilities and preserve the signed contrast s-p=-1/4. Consequently

    J_(p',s')(r1)-J_(p',s')(r0)=-1/32,
    H_(p',s')(r1)=5/8 > r1=1/2.

The cost-improvement guarantee survives exactly, while the new report now
understates the induced failure probability by 1/8. The old report also fails:
H_(p',s')(r0)=11/16. Preserving a comparison-relevant difference cannot certify
an absolute reporting threshold. This directly instantiates the separate
producer and deployment obligations rather than merely renaming them.

### P13 — what an operational receiver must additionally establish

To use a numerical root as a claim about these programs, retain:

1. the identity of the executed versions and the same fixed reports throughout
   the comparison;
2. the probability-domain and branch-law interpretation (0<=p,s,r<=1 here);
3. the observation contract making each policy selectable with available data;
4. the intended cost, resource units and any proxy-to-task discrepancy bridge;
5. any separate report-validity request needed by the consumer.

Conditional numerical soundness plus these bridges establishes the corresponding
operational conclusion. Numerical soundness alone does not establish the bridges.
For example p=2,s=0,r=3/4 gives the perfectly meaningful arithmetic H(r)=1/2,
but p=2 is not a failure probability for the named first branch. A small or
favorable value of H cannot repair that missing interpretation. Nor can a source
witness at some other legal point establish that every admitted point has the
required probabilistic meaning.

Observation transport retains the existing finite factor criterion: a policy
can be carried through an observation coarsening exactly when its action law is
constant on every new observation fiber. Equality of observation labels is a
version guard, not a proof of this factorization for an arbitrary program.
The new tests use explicit finite tables and rational distributions; they do
not implement a verifier for unrestricted code.

## 12. Uncertain proof alternatives: which extremum is justified?

A numerical proof minimum is sound when both arguments' assumptions hold in
the current context. A different epistemic claim is 'at least one of these
arguments has an applicable source.' Let the SAME intended difference be d,
and suppose argument i establishes d<=b_i on event or case E_i.

On the intersection of the E_i, one may conclude `d<=min_i b_i`.
On their union one can conclude `d<=max_i b_i`, but not their minimum.
The counterexample d=1, b_1=0, b_2=2 has a valid second argument and an invalid
first argument. Its minimum is false. This is not a defect of `meet_proofs`:
the latter's source contract asserts the premises jointly, not disjunctively.

### P14 — a finite fault-tolerant envelope for one fixed claim

Suppose among n same-claim arguments, at most k are inapplicable at a given
interpretation, with 0<=k<n. Order their finite bounds as
`b_(1)<=...<=b_(n)`. Then

    d <= b_(k+1).

**Proof.** The first k+1 indices cannot all be inapplicable. A valid one gives
d<=b_i<=b_(k+1). This argument does not require identifying which one is valid.
The result is sharp with no additional assumptions: let the first k arguments
be invalid, every remaining bound equal b_(k+1), and d=b_(k+1). ∎

The condition 'at most k' is itself evidence. The arithmetic order statistic
does not prove it. A finite union-of-cases model can supply it explicitly:
each case asserts the rows for one known subset of n-k applicable arguments,
and every case establishes the same bound. The policy, target loss and request
are unchanged between cases; only the proof evidence differs.

This exposes an audit interface for uncertainty about premises without pretending
that an arbitrary reliability number is a new logical truth value. The construction
is a familiar finite counting argument and is not advertised as a novel theorem.

### 12.1 Adaptively varying numerical bounds need simultaneous scope

Let the n registered procedures output random finite bounds B_i for the same
(possibly record-dependent) difference D. Let E_i imply D<=B_i and suppose
Pr(E_i^c)<=alpha_i under the same declared probability law. Neither independent
errors nor fixed numerical B_i values are assumed. Let B_(r) be the r-th order
statistic, where r=k+1 is fixed before selection. If D>B_(r), at least r of the
E_i must fail. Therefore, writing N=sum_i 1_(E_i^c),

    Pr(D>B_(r)) <= Pr(N>=r) <= min(1, sum_i alpha_i/r).

The second step follows from `r*1_(N>=r)<=N` and expectation. There is a useful
refinement: remove any t<r procedures from the count. Failure still requires
at least r-t failures among the remaining procedures. Hence an upper bound is

    min(1, min_(S:|S|<r) sum_(i notin S) alpha_i/(r-|S|)).

No independence is imported, and no claim of optimality among all possible
probability bounds is needed. The registration matters: unbounded adaptive
selection of new procedures with only individual marginal calibration is not
the finite family assumed here. These are joint-error probabilities, not a
conditional-on-issuance guarantee or an expected-utility theorem for unbounded
losses. The earlier S1 selection counterexamples remain applicable.

At r=n, failure of the maximum implies failure of every argument, so the refined
bound includes min_i alpha_i. At r=1 the bound reduces to the usual sum allowance
for selecting the minimum. These endpoints are useful independent checks on the
polarity of the interpretation.

## 13. Current comparison is not historical performance change

Source revision also creates a less obvious interpretation trap. For a fixed
versioned cost family J_theta(r), these are three distinct quantities:

    policy change at the current source:
        J_theta'(r1)-J_theta'(r0),
    source change at a fixed policy:
        J_theta'(r0)-J_theta(r0),
    simultaneous historical change:
        J_theta'(r1)-J_theta(r0).

The proof-local transport algorithm reconstructs a comparison under the CURRENT
context. Its first quantity is not automatically the third. Changing the
possible evidence about a fixed theta need not even mean that the physical
source theta changed; a declared time-varying model must say when that is the
question. The prime notation here explicitly denotes distinct source values.

### P15 — the missing term in a cross-version comparison

If separate, jointly applicable bounds establish

    J_theta'(r1)-J_theta'(r0) <= b,
    J_theta'(r0)-J_theta(r0)  <= d,

then the historical change is at most b+d.

**Proof.** Add the inequalities and cancel the identical middle quantity
J_theta'(r0). Without the second premise, that quantity's change is unrestricted
by the first. This is the existing signed transitivity argument, not a new rule. ∎

In section 11, with the common baseline unchanged, the old historical cost is
7/32 and the new historical cost is 22/32. Their difference is +15/32, even
though the present-source policy comparison is -1/32. The old policy's source
drift is +1/2, and -1/32+1/2=15/32. Thus all three assertions can simultaneously
be correct. Adding an unknown changing common baseline would require its drift
to be carried as well; cancellation within each source value does not cancel
unrelated baselines across source values.

### 13.1 Report-induced changes in branch laws

If changing the report also changes the conditional branch laws, use separate
p0,s0 and p1,s1. For fixed r0,r1 in [0,1], direct expansion gives

    H_1(r1)-H_0(r0)
      = (r1-r0)(s0-p0)
        +(1-r1)(p1-p0)+r1(s1-s0).                             (D4)

The first term is the familiar same-source policy difference. The other terms
are not erased merely because the branch names and reports have familiar
labels. Bounds delta_p,delta_s on the two law changes give an extra allowance
`(1-r1)delta_p+r1 delta_s`. The coefficients are nonnegative because r1 is a
legal mixing probability. Treating r1 as a fixed rational policy parameter
keeps the whole calculation in the selected affine comparison language.

D4 gives a constructive bridge when exact branch-law stability is too strong.
It does not supply the law-change bounds; those are uncertainty/source premises
that must be estimated or justified under their own protocol. This is a local
algebraic interface adjacent to performative prediction, not an imported
convergence result from that literature.

## 14. Exact source aliases can change the requested bound

One more producer-level counterexample sharpens P1/P4. Let the old source have
x<=0 and y>=1, with witness (0,1). It proves x-y<=-1. Now substitute BOTH old
coordinates by a target coordinate z, and remove all numerical evidence.
The substituted difference is z-z=0. The producer can correctly simplify it
and return the source-free bound 0, without requiring impossible replacement
proofs for z<=0 and z>=1.

That is a successful production of a valid CURRENT comparison, but not a
successful proof of the OLD target bound -1. A receiver fixed to the latter
must reject the output. A receiver requesting the mapped difference at 0 may
accept. Noninjective source substitutions are not universally forbidden;
what survives is the actually returned and received current claim, not a
historical budget copied by name.

A second example allows a nonlinear substitution. Old x<=1 may be mapped to
x=max(z,0), and a current proof from z<=1 plus 0<=1 establishes the substituted
row at 1. If current evidence strengthens to z<=-1, the same reconstruction
can establish max(z,0)<=0. This is typed expression substitution with a supplied
current proof, not an assumption that an affine old row stays affine as an
expression after substitution. The target **source rows** remain affine;
their derived consequence may be nonlinear.

## 15. Joint source structure determines whether a paired expectation exists

The earlier soundness pass permits an integrable cost difference even when the
two absolute expected costs are infinite. That allowance still requires an
actual joint interpretation of the pair. Marginally described losses alone do
not establish the integrability premise.

Let N have probabilities Pr(N=n)=1/(n(n+1)), n>=1. Then Pr(N>=k)=1/k.
On a shared draw, old=N+1 and new=N give a difference -1 exactly, while both
nonnegative absolute expectations diverge. On independent draws M,N with that
same law, old=N+1 and new=M have the SAME two marginal cost distributions as
before, but the difference is not integrable. Indeed, conditioning on any fixed
N=n gives

    E[(M-(n+1))_+] = sum_(k=n+2)^infinity Pr(M>=k) = infinity.

Conditioning instead on a fixed M=m gives an infinite expectation of the
opposite positive part. Hence the new-minus-old expectation is undefined in
the independent interpretation; it is not an alternative finite number.
The shared-source relation is doing essential work even though no absolute
finite-loss cap was imposed.

### P16 — finite paired expectations cannot disagree solely by coupling

There is an important complementary limit. Suppose (X,Y) and (X',Y') have the
same respective marginal laws, all four variables are finite almost surely,
and BOTH X-Y and X'-Y' are integrable. Then

    E[X-Y]=E[X'-Y'].

**Proof.** Let T_m be clipping to [-m,m]. It is 1-Lipschitz, so
`|T_m(X)-T_m(Y)|<=|X-Y|`. Its difference converges pointwise to X-Y, and dominated
convergence gives

    E[X-Y]=lim_m (E[T_m(X)]-E[T_m(Y)]).

The expectations on the right are bounded-variable quantities determined only
by the marginals. The same formula applies to X',Y', yielding equality. ∎

Thus source coupling can establish or destroy the EXISTENCE of the relevant
integrable paired expectation, and strongly affects finite risk or tail bounds.
It cannot arbitrarily change a finite expected difference when the marginal
laws are fixed and both paired differences are integrable. This prevents an
overstatement of the benefit of retaining dependence. Neither theorem silently
adds subtraction of positive and negative infinities to the native calculus.

## 16. Fresh reconstruction record and remaining audit boundary

The following checks were made from the producer's input contract, not just
from its returned numbers:

- A normalized row's offset moves into eta; substitution acts on its remaining
  expression. A target proof of a different direction or merely the same row
  number is insufficient. A supplied global replacement is localized before
  its exact current budget is substituted into the old local budget program.
- Closed source substitution preserves normal-form equalities by a recursive
  map on source keys and nonlinear child forms. It need not reflect distinctness:
  different old coordinates may become the same target expression. The latter
  can change the strongest source-free current bound.
- Zero numerical scaling does not excuse an ill-typed or unbound expression.
  The native checker types the children before normalization can cancel them.
  Source support can disappear from a *well-typed* zero conclusion, not from
  an undefined one.
- Discharge internalizes the localized bound, not a historical global maximum.
  With case bounds 0 and 2, the penalty on the first case is ReLU(x), not
  ReLU(x)-2. Both an exact allowance field and the advertised zero-baseline
  violation interpretation therefore need checks beyond root validity.
- The envelope helper produces indices into a builder, not a newly trusted
  theorem. Its returned baseline, gain and error are justified only with its
  declared hinge grammar and the final native checks of the constructed trace.
  Publicly callable helpers that raise an exception or leave an invalid builder
  have not produced an accepted certificate.
- A static frontier's exactness is relative to its fixed grammar. Localizing
  before selection changes that grammar and can improve availability as well
  as precision. This is the identified cross-algorithm distinction, not an
  invalidation of the previous restricted theorem.
- A current scalar bound, its reusable family, and its operational source
  interpretation have different persistence conditions. Pruning one selected
  proof is correct now and may still remove a useful future alternative.
- Cases and numerical approximations must retain one common intended query.
  Choosing proof witnesses under hypothetical cases supplies no hidden channel
  through which the deployed action learns those cases.

The implementation checks planned for this pass independently reconstruct the
localized allowance and request, validate metadata, and compare static versus
case-localized salvage on finite examples. They do not formalize all Python
behavior or prove arbitrary producer termination. The mathematical results
above are same-assistant reconstruction; F07 remains partial until its separate
D90 and remaining reconstruction obligations are met. No new inference tag,
F08 characterization task, neural training, or Gate B attempt is selected here.

## 17. An exclusion margin can be audited after its own premises weaken

P7's strict ray has numerical margin kappa>0 defined by

    sum_i w_i a_i + k*c = 0,
    sum_i w_i eta_i - k*d = -kappa,
    g=c+d,  w_i>=0, k>0.

Let rho_i=max(a_i-eta_i,0) at an arbitrary current finite assignment. The
source-free residual inequalities a_i<=eta_i+rho_i give

    -g <= -kappa/k + (1/k)*sum_i w_i rho_i.                    (D5)

This follows by exactly the same addition, positive scaling and constant
rewrite as the strict original exclusion. The old assertion that the parent
rows all hold has been replaced by an explicit weighted violation allowance.

If the weighted violation is STRICTLY below kappa, g>0 and the old nonpositive
branch remains excluded. If it is equal to kappa, only g>=0 follows. That still
permits use of the nonnegative branch, because both closed sign cases include
zero, but it no longer proves that the nonpositive branch is empty. If the
weighted violation can exceed kappa, its excess controls the opposite hinge:

    max(-g,0) <= max((sum_i w_i rho_i-kappa)/k,0).              (D6)

A surviving branch argument with allowance A+alpha*max(-g,0) can therefore
still be used with the corrected allowance from D6. The caller must retain
which conclusion it requests: branch impossibility, permission to use the
nonnegative-case proof, or a graded comparison are different statements.

For g=x and the old premise -x<=-1, k=w=kappa=1. At x=1/2 the old premise is
violated by 1/2 but the exclusion still holds; at x=0 the violation reaches
one and only the nonnegative guard remains justified; at x=-1/4 the additional
opposite-guard cost is 1/4. This is a direct check on the strictness and sign in
D5/D6, not an assumption that a small absolute change in a coefficient has a
uniform effect on an unbounded variable.

## 18. Proof faults and source faults are not counted interchangeably

P14 counts inapplicable **arguments**. A fault allowance for a number of source
records is different because many arguments can share one record. Repetition
is not independent support.

Let a finite stored family contain pairs (S_i,b_i), where each S_i is a set of
source identities and the associated checked proof establishes the same
numerical difference d<=b_i whenever all identities in S_i are applicable.
Let F be a set of possibly faulty source identities. Among the stored family,
the best surviving bound is

    B(F)=min_(i:S_i intersection F=empty) b_i.

When every allowed F has a survivor, a common warrant under unknown F has the
bound `max_(F allowed) B(F)`. The exactness here is relative to this stored
family and its permitted selection grammar, not arbitrary proof search. A case
without a survivor makes this family unavailable; it does not prove that d is
unbounded or false. As before, selecting a hypothetical proof witness does not
let the deployed action learn which F occurred.

**Justification.** At an actual allowed F, each disjoint support is wholly
applicable. Its proof establishes its bound; select the smallest one, then
weaken to the displayed maximum over allowed F. Conversely, no smaller bound
is obtained by this particular 'select one surviving family member' procedure
at a case attaining the maximum. Claims of semantic optimality need an actual
tightness witness, not only this algorithmic argument.

A concrete false shortcut uses three proofs with supports

    S1={a}, S2={a}, S3={b},  bounds=(0,0,1).

Suppose at most one SOURCE can fail. If a fails and b remains applicable, d=1
is permitted. Both first proofs are then inapplicable, despite only one faulty
source. The median bound 0, which would tolerate at most one faulty PROOF, is
false here. The source-aware maximum-over-fault-sets bound is 1 and is attained
by that example. Duplicating the first proof did not improve the evidence.

These are the same source identities used for proof withdrawal and dependence
tracking. Their quantitative costs can be used repeatedly in algebra, while
an empirical validity event is not multiplied merely because its source is
cited twice. An uncertain-source extension of the calculus must state which
kind of fault or probability statement it actually has.

## 19. A positive replay guarantee for primitive expansion

The loss of alternatives in section 8 does not mean primitive expansion always
obstructs future reuse. Fix the original proof syntax, its literal constants,
unit conversions, row directions and case schema. Allow only admissible changes
to source-row right-hand-side bounds, with a feasible current witness as required
by ordinary replay. Let B_j(eta) be the original numerical budget program at
node j. At a proof-minimum node the compiler picked a particular parent at the
old snapshot.

### P19 — numerical replay commutes when selected alternatives remain optimal

If every compiled proof-minimum choice remains a least-budget choice under
the new eta, then replaying the compiled primitive trace and replaying the
original recipe yield identical root pairs and budgets. In particular this
holds for every admissible RHS update when no reachable `meet_proofs` instruction
occurs in the original trace.

**Proof.** Reconstruct each macro as a function of its parent budgets, rather
than substitute only the old numbers. Expanded transitivity adds the two
budgets; reversed negation copies its budget; expanded slack adds its fixed
nonnegative constant. Expanded min/max congruence takes the maximum of the two
budgets because the inserted lattice steps have zero budget. Residual congruence
adds its correctly oriented parent budgets and takes their maximum with zero.
These identities hold for every finite signed pair of parent budgets. Primitive
copies and case joins retain their ordinary operations.

At a proof-minimum node the compiled branch has the original minimum exactly
when the specified parent is still a minimizer. Apply the induction to every
compiled ancestor; at a selected minimum its unused parent's CURRENT original
budget is used only to state the minimizing hypothesis, not silently estimated
by a stale compiled value. This proves the root equality. ∎

The premise is sufficient, not necessary for an insensitive root. For example,
a proof minimum followed by multiplication by zero retains root budget zero
even if its chosen alternative is no longer best. Equality of numerical budget
functions also does not establish equality of all future support frontiers,
source meanings, or proof explanations. Those are different observables.

For two leaf bounds eta1=-2 and eta2=-1, the old first choice survives precisely
when the changes satisfy delta1-delta2<=1. An arbitrary shared change
(delta1,delta2)=(t,t) preserves it, even with t unbounded. Changing only the first
bound by two violates the condition: replay of the selected branch gives zero,
while replay of the retained proof family gives -1. This illustrates why a
relative update certificate can be more useful than bounds on absolute changes.

## 20. Correctness of the independent discharge receiver

The new receiver reconstructs its expected object from the OLD context, proof,
selected case, explicit row-withdrawal indices and requested revision. It does
not read those decisions from the producer's returned root or metadata.

Its reconstruction walks the original DAG. At a global case join it selects
exactly the chosen case's parent. At a row, it evaluates the affine difference
at the zero coordinate vector solely to recover its intercept c; zero need not
satisfy the source. It then uses a=(lhs-rhs)-c and eta=-c. The allowance is eta
for a retained row and eta+max(a-eta,0) for a withdrawn row. Nonleaf constructors
use the independently listed symbolic and numerical budget recurrences. Memoization
is by proof node in this ONE selected case, not by a lexical local name.

Induction on that walk proves that its returned pair, local baseline and
allowance coincide with P6's mathematical specification. The implementation
shares the already audited expression datatype and uses the existing sound
normalizer only to compare equivalent returned presentations; it does not use
the producer's localizer or its allowance-generation routine as its oracle.
A separate denotation evaluates the finite regression points.

The receiver then checks the exact changed context and row identities, the
local baseline, the allowance and penalty equalities, and finally the original
requested new term versus old term plus the validated allowance at budget zero.
P1 and the equality checks give P6's full postcondition, not merely a valid
inequality about whatever fields the producer happened to return.

This receiver deliberately enforces an EXACT-reconstruction contract. A producer
may find a different, stronger valid allowance; it should submit that as a
separately named comparison and have it received on its own terms. Failure to
match P6 is not a proof that the alternative inequality is false. Likewise,
exhausting a recursion or size limit is neither success nor semantic refutation.

The finite tests include incorrect penalty, allowance, withdrawal, revision,
baseline and root fields; a wrong field is rejected even when the underlying
trace remains valid. The initial test run exposed an unpacking error in a NEW
test harness's use of the existing native catalogue. Correcting the call shape
did not alter an assertion, mathematical claim, producer or original checker.
The initial failure remains part of this session's execution record.

## 21. What a certified nonnegative penalty necessarily measures

If a current comparison has actual finite difference D and a certified
nonnegative correction R to old budget b, then

    D<=b+R and R>=0  imply  R>=max(D-b,0).                     (D7)

This follows by subtracting b and using both lower bounds on R. Conversely,
R*=max(D-b,0) is the least possible nonnegative correction when D itself is
already known. That latter formula is a semantic benchmark, not a way to
compute the missing conclusion cheaply: evaluating D can be exactly the task
that the compositional source proof was intended to avoid.

The proof-derived R_P is therefore a sufficient, potentially conservative
correction with an explicit construction from premise violations. It is not
claimed to be a unique truth degree, probability, or minimal epistemic
uncertainty. It has the same cost unit as D and b. A mere numerical conversion
from R_P to a probability-like score would need a calibrated interpretation;
the proof alone supplies no such conversion.

This is also why a strict producer receiver and an ordinary comparison receiver
serve different purposes. The former verifies the advertised construction of
R_P and all its metadata. The latter can accept any separately justified R that
meets its request. A new stronger proof is welcome, but its bound should not be
misdescribed as the old proof's particular residual decomposition.

### 21.1 Global replacement proofs carry information beyond their root numbers

Let an old single-case argument use x<=2 and y<=2 to prove x+y<=4. In the new
context, case a has x<=0,y<=2, while case b has x<=2,y<=0. A global proof of
x<=2 and a global proof of y<=2 each retain their case-specific subderivations.
If these are supplied as replacement proofs, localization yields bounds (0,2)
in a and (2,0) in b. The transported sum consequently has global bound 2.
Passing only the two root numbers (2,2) would instead retain 4. The proof
objects and their source/case structure carry useful information that those
numbers discard. This is the concrete interpretation of P4's corrected local
beta convention, not a claim that generic global bounds are themselves unsound.

### 21.2 Exact source offsets remain part of the requested expression

Old x<=1 with x replaced by z+2 requires a current proof of z+2<=beta, not
merely a current proof of z<=beta. From z<=1, the valid replacement has beta=3.
An unchanged bound of 1 would be false at z=1. The adapter's exact comparison
of the substituted old expression rejects the omitted offset; the request
receiver separately checks whether the resulting current bound 3 is strong
enough for the application. Normalizing an old source row and substituting
new coordinates are different operations with different offsets.

## 22. Audit boundary and the next reconstruction

The common invariant through the producers is the independently specified
current comparison, not the old numerical bound. In order:

1. localization changes the domain and can sharpen the bound;
2. source grafting changes the premises and recalculates that bound;
3. residual discharge changes which numerical premises are assumed and makes
   their possible violations part of the returned expression;
4. case compilation keeps one comparison while justifying it on the whole
   declared union; and
5. the final receiver compares the resulting pair, scope and strength with a
   request fixed independently of the producer's output.

Each step is conditionally mathematical. The step that changes a probability
model, observed information or deployed program has an additional interpretation
obligation, not supplied by algebraic rewriting. In particular, no sequence of
valid numerical transformations turns an unspecified 'at most k faults' belief
into proved evidence, or makes a source label authenticate itself.

For fixed bounds in P14, sharpness can be seen without changing their values:
choose d equal to their (k+1)-st order statistic and let exactly those arguments
with smaller bounds be inapplicable. There are at most k such arguments; every
other bound is at least d. Thus no universally smaller envelope follows from
the fault-count condition alone. At k=n the existence of even one applicable
argument disappears, and no finite bound follows without a different premise.
The implemented contract rejects that case rather than inventing an infinite
number in the finite-real core.

This session audits producer postconditions and their intended use relative to
the first pass's native soundness proof. It does not certify arbitrary Python
execution, floating-point substitutes, external empirical premises, or a full
neural implementation. Finite tests below exercise the declared contracts and
mutations; the universal mathematical statements depend on the written
inductions and inequalities, not their finite test counts. F07 remains partial:
the final protected block should reconstruct the combined theorem and its
explicit fragment boundaries, rather than add unrelated capabilities.

The retained-row conditions in P6 have two different roles. The inequality
`E_P>=b_P` follows from nonnegative row violations and monotonicity of the
budget constructors at every finite assignment; it does not require the
retained source rows. In contrast, `t-s<=E_P` still requires those retained
rows. Combining the two facts proves that the returned penalty is nonnegative
without accidentally deleting the assumptions needed for the conclusion.
Likewise, choosing an old proof case for each new case is an algorithmic
reconstruction choice, not evidence that the new domain is included in that
old case: the grafted row proofs discharge the used premises instead.
