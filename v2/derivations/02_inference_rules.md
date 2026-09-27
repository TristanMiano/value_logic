# F06 — source-aware inference for signed loss comparisons

Status: **source-transport and residual-discharge continuation; F06 partial**. September 27, 2026 (UTC).
Interpretation is fixed independently in [the F05 core](../foundations/03_provisional_core.md).
This note does not replace that semantics, finish F07's general soundness audit,
or claim a complete reasoner. The source-preserving continuation alternative
remains live. All numbers below are finite rationals in the syntax; modeled
values are finite reals pointwise and may be unbounded over the source domain.

## 1. What is being derived

Use the sequent

    C ; h |- t <=[b] s : u

for a derivation about one live case h of the exact, versioned F05 context C.
Its intended meaning is t(x)-s(x)<=b for every feasible x in that case. All
three quantities have unit u. t is the NEW loss, s the OLD loss; a negative b
retains an improvement. The union-case form `C |- t <=[b] s` requires a proof
for every live hidden case, with the same fixed deployed policy. A case-specific
interpretation table may be written explicitly; it does not change that policy.
The executable first-pass checker is restricted to a common expression pair.

`|-` is syntactic derivability by the rules below. It is not defined as the
semantic `|=` and does not consult the supremum B_C as an oracle. A failed
proof attempt is not a countermodel and is not a proof of the reverse judgment.
Source rows are conditional mathematical premises, not metaphysical truth.

Every local judgment binds the signature, units/conversions, observation,
plan/evaluator/criterion meaning, evidence revision and case identity. A
proof cannot mix contexts because their row numbers happen to agree. The
context's rational witnesses must satisfy its rows; nonempty cases are a
separate prerequisite, not a consequence of successful implication checking.

Write `t-s` for F05's addition and negative rational scaling. Exact algebraic
normalization may expand lexical bindings and declared conversions and collect
rational linear combinations. Native min/max/res subterms may be kept as
opaque, structurally identified atoms. This cancels repeated shared terms;
it does not assume that two different sources are equal or call a numerical
sample an equality proof. A linear source equality needs both inequality rows.

## 2. Small structural rule set

All displayed premises in this section have the SAME C,h and compatible units.
Every rule has a pointwise justification; the separate F07 task must assemble
and audit the eventual complete derivation-level theorem.

### R0 — exact constant difference / identity

If exact syntax normalization gives `t-s=c`, with no uncancelled source or
opaque atom, derive `t <=[c] s`. Identity is c=0. Negative c is permitted.
Reason: the difference is that literal at every finite assignment. Finite
pointwise values matter: this does not cancel infinity against infinity.

### R1 — source row

A declared affine row `a(x)<=eta` yields `a <=[eta] 0`. More generally a row
`l<=r` yields `l <=[0] r`. The coefficient-normalized form and its offset must
be retained for evidence replay. Reading a row means assuming it, not verifying
its empirical provenance or confidence. Rows can be cited more than once;
each arithmetic occurrence still contributes its coefficient to the budget.

### R2 — exact difference rewrite

From `t <=[b] s`, infer `t' <=[b] s'` when the normalized differences
`t-s` and `t'-s'` are identically equal, with the same declared source meanings.
This admits common-baseline cancellation and ordinary affine rearrangement.
It does not erase a baseline from a composition that changes its multiplicity.

A more general rewrite justified by two zero-budget derived comparisons is
possible through R3 below. Do not broaden the normalization checker into an
unreported oracle for all piecewise-affine identities.

### R3 — transitivity and budget weakening

    t <=[b] s     s <=[c] r                 t <=[b] s     b<=d
    ----------------------                 ------------------
           t <=[b+c] r                            t <=[d] s

For transitivity, `(t-r)=(t-s)+(s-r)`. For weakening, enlarge the upper bound.
For unconditional evidence replay, represent weakening by a fixed nonnegative
slack k and recompute b+k. A fixed-target d requires rechecking b_new<=d.
The middle expressions must agree under a checked exact rewrite, not merely
in their display name. Signed budgets add; replacing them by absolute values
would throw away improvement but is not required for validity.

### R4 — addition

    t1 <=[b1] s1     t2 <=[b2] s2
    --------------------------------
        t1+t2 <=[b1+b2] s1+s2

The same feasible assignment interprets both premises before they are added.
There is no independence premise. When the sum describes a program, its
component-cost interpretation must actually be additive in the specified unit.
An energy bound does not add to latency without a declared valuation bridge.

### R5 — nonnegative scaling, polarity reversal, conversion

For rational k>=0,

    t <=[b] s  =>  k t <=[k b] k s.

Negation reverses the two arguments, not the sign of the budget:

    t <=[b] s  =>  -s <=[b] -t.

Thus scaling by a<0 is represented as
`a s <=[(-a)b] a t`. The unsound alternative `a t <=[a b] a s` is not a rule.
A declared positive conversion factor k transports both expressions AND the
budget, retaining its source and target units and criterion interpretation.
A probability-to-loss weight is not automatically an invertible unit change.

### R6 — combining two proofs of one query

    t <=[b] s     t <=[c] s
    -----------------------
        t <=[min(b,c)] s

Both premises hold in the same case, so their smaller bound holds there.
This combines arguments, not alternative deployed actions. In particular it
is not the rule `min(Cost(A),Cost(B)) is an available policy`.

## 3. Order operations and the direction of approximation

### R7 — lattice introduction and comparison

The unconditional laws include

    min(a,b) <=[0] a,       min(a,b) <=[0] b,
    a <=[0] max(a,b),       b <=[0] max(a,b).

Two useful common-target rules are

    a <=[p] c     b <=[q] c  => max(a,b) <=[max(p,q)] c,
    c <=[p] a     c <=[q] b  => c <=[max(p,q)] min(a,b).

For the first, a<=c+p and b<=c+q. The second follows by choosing whichever
of a,b is the minimum at the current assignment. Both remain valid for negative
p,q. The rules do not require knowing which argument wins.

For either F=min or F=max, the congruence rule is

    a1 <=[p] b1     a2 <=[q] b2
    ------------------------------------
       F(a1,a2) <=[max(p,q)] F(b1,b2).

Indeed set d=max(p,q); monotonicity and common-translation invariance give
F(a1,a2)<=F(b1+d,b2+d)=F(b1,b2)+d. This proof does not assume independent
arguments, fixed active branches, or nonnegative modeled values.

If only one argument improves and the other remains unchanged, the guaranteed
budget is max(b,0), not b. Saturation can erase strict improvement.

### R8 — residual polarity

F05 uses `res(a,b)=max(b-a,0)`. To replace both arguments, require the reverse
comparison in the FIRST argument:

    a_old <=[p] a_new     b_new <=[q] b_old
    -----------------------------------------------------------
    res(a_new,b_new) <=[max(p+q,0)] res(a_old,b_old).

The inner difference changes by `(b_new-b_old)+(a_old-a_new)<=p+q`.
Apply max congruence with the unchanged zero argument. Using
`a_new-a_old<=p` instead is generally unsound.

For b>=0 only, the zero-reference rule is an equivalence:

    t <=[b] s    iff    res(s,t) <=[b] 0.

At a negative budget the right side is impossible in a nonempty context, even
when the signed comparison on the left proves strict improvement. The signed
judgment is therefore not replaced by its clipped shortfall.

### R9 — enclosures used in a comparison

Suppose `new <=[a] upper_new`, `upper_new <=[b] lower_old`, and
`lower_old <=[c] old`. Two applications of transitivity yield

    new <=[a+b+c] old.

Upper bounds belong on the new-cost side and lower bounds on the old-cost side.
This is an explicit three-premise argument; neither an enclosure's midpoint
nor a sampled value is silently substituted. A shared joint relation can yield
a tighter result than separately enveloping both costs.

## 4. Cases, scope, and source changes

### R10 — exhaustive hidden cases

For every live h in C, derive the corresponding fixed-policy query with budget
b_h. Then the union context derives it with budget `max_h b_h`.
A missing case is not discharged; averaging or taking the minimum is wrong.
The same observation-legal policy is held fixed in all cases. Different proof
witnesses in different cases do not give the policy access to hidden information.

Splitting a case into new polyhedra requires a coverage proof and an explicit
resolution of empty pieces. The first pass uses the already supplied F05 cases;
it does not implement unrestricted automatic case splitting.

### R11 — source restriction with explicit obligations

A proof for C can be transported to C' by a typed source map sigma and a map
from every new case into an old case. For each target row of that old case,
derive its substituted inequality in the new case. Require unchanged or
explicitly related plan/criterion meanings. The resulting assignment satisfies
all old rows, so F05's substitution lemma transfers the comparison.

For identity maps, literal row retention is a simple sufficient check. A new
revision number, invertible vector of reported bounds, or matching variable
names is not one. Joining two contexts additionally requires a witness for the
joint source; separate nonemptiness does not prove joint nonemptiness.

### R12 — paired proxy bridge

For a declared positive conversion alpha, define `E_pi=J_pi-alpha L_pi`.
From the proxy comparison `L_new <=[b] L_old` and the independently warranted
paired discrepancy `E_new <=[beta] E_old`, derive

    J_new <=[alpha*b+beta] J_old.

This is R5, R4 and an exact difference rewrite. Absolute errors need not be
bounded. A low training loss, proper scoring rule, or favorable self-report is
not a premise establishing the discrepancy comparison.

## 5. Proof records and operational boundaries

A proof record stores the rule, preceding node references, typed expression
pair, calculated budget, full context/case identity and referenced source rows.
Acyclicity is required for a finite proof trace. It does not forbid the specified
report-dependent policy from influencing the probability the proof assesses.
No rule concludes its own empirical validity from a self-reference.

Two different annotations must not be collapsed:

* arithmetic dependence records how premise bounds enter the conclusion;
* provenance records which evidence objects and assumption modes are relied on.

Repeated use of one row can multiply its arithmetic contribution while still
being only one empirical event. Formal consequence and the probability that the
source assumptions hold are separate layers. The first-pass certificates are
conditional arithmetic arguments, not a new statistical calibration procedure.

## 6. Worked derivations and current implementation

The [reconstruction](02a_rule_reconstruction.md) develops source-aware additive
composition, native absolute-error loss, reflective proxy-to-intended revision,
and a nonlinear component enclosure. Each begins with component/source premises,
not a supplied final bound. It also derives a limited proof-replay contract and
retains countermodels to tempting unsound rules.

Implementation coverage, actual tests, and remaining work are recorded after
the separately timed mathematical block. No general completeness, efficiency
advantage, new mathematical priority, trained-neural interpretation, or F07 gate
is asserted by this first pass.

## 7. Three derived interfaces used in this pass

**Deferred scalar reduction.** A component allowance `t-s<=e(x)` is written
`t <=[0] s+e`. Add these relations while retaining the common source, normalize
the summed allowance, and only then prove a finite scalar bound. Reconstruction
section 22 derives -1/2 from two partial component contracts without knowing
complete component cost functions.

**Proof-budget replay.** For unchanged row directions and source meanings,
rebuild a proof with its new finite row bounds and recalculate every budget.
The budget expression uses constants (including fixed nonnegative weakening
slack), row-bound variables, nonnegative scaling, sum, min and max. A separate structural shock expression bounds its response
to uncertain evidence changes; correlated changes may cancel. Branch-dependent
rewrites, source coefficients and missing premises need separate guards/repair.
Reconstruction sections 8–10 and 18–20 spell out the exact boundary.

**Available selection.** A minimum over known checked bounds on named available
policies can select one executable witness. A minimum over their hidden costs
cannot. Reasoning and selection overhead must be added if it belongs to the
compared use plan. The numerical deduction itself supplies no universal action
authorization or claim of target-world safety. See reconstruction section 15.


**Arithmetic consumers.** Two directed input comparisons generate a finite
replacement proof through a typed expression, by polarity-sensitive use of
R4/R5/R7/R8. For the native consumer K(x)=2x+res(0,x), one comparison with
budget b yields the signed budget 2b+max(b,0), retaining strict improvement
for b<0. This is a derived macro, not a new arbitrary Lipschitz oracle.

**Report and proof-budget self-models.** A report-transfer proof can retain a
positive allowance for an old report and still establish a nonpositive allowance
for its successor. The numerical output of a specified proof-bound calculator
can itself be modeled as a native expression. Neither construction supplies
empirical soundness from its own acceptance; exact versions, current premises
and external calibration obligations remain explicit. Reconstruction sections
31–33 give nonempty examples and countermodels.


## 8. Executable audit boundary

[`f06_inference_rules.py`](../checks/f06_inference_rules.py) checks supplied finite
proofs using exact rational normalization, row references, transitivity, addition,
nonnegative scaling, reversed negation, named conversion, fixed-slack weakening,
minimum over proofs, lattice rules, residual congruence and exhaustive cases.
It has a restricted RHS-only replay operation. Capture-free lets are expanded;
residual unfolds its definition and purely literal min/max operations are folded.
Other nonlinear atoms are kept distinct after instantiating their arguments.

The F05 point evaluator checks source-witness feasibility and supplies finite
reference checks; it is not a universal-conclusion oracle inside the proof checker. The 58 tests include
explicit proof traces, malformed/mutated proofs, source revisions, signed budgets,
lexical shadowing and finite negative controls. Discovery repeats these same
58 tests; it is not another independent suite.

The first pass does NOT implement general source-map checking (R11), automatic
case splitting or emptiness certificates, arbitrary proof search, policy synthesis,
proof-premise withdrawal monitoring, statistical calibration, or neural training.
Enclosure and proxy rules are exercised through primitive multistep derivations.
The more general mathematical interfaces in the reconstruction are not all code
features. F06 remains partial; F07's general audit has not been performed.


## 9. S2 derived proof-transport and residual-discharge interfaces

The [S2 reconstruction](02b_source_transport_and_withdrawal.md) and its two
[transport](../checks/f06_source_transport.py) and
[discharge](../checks/f06_residual_discharge.py) fixtures extend the first pass
without changing its checking kernel. The first-pass implementation exclusions
in section 8 are historical; this section states the new bounded coverage.

**R11a — proof-local transport.** Whole-context inclusion in R11 is sufficient
but stronger than needed for reusing a particular proof. After case localization
and a typed closed source substitution, replace every used row introduction by
a currently checked proof of its substituted expression. Rebuild its constructors
and recalculate their budgets. Cover every new live case with the same query.
A weaker replacement may yield a weaker conclusion; do not copy the old number.
Equal fingerprints are not required: the result has the actual NEW fingerprint.
Numerical substitution does not itself certify an observation-legal policy map.

**R13 — quantitative discharge of numerical row assumptions.** The universal
lattice consequence a<=eta+res(eta,a) replaces a removed row a<=eta. Reconstruct
a local trace with symbolic allowances, represented as ordinary zero-budget
comparisons t<=[0]s+e. Addition, nonnegative scaling, typed conversion and
min/max construct the allowance; the S2 emitter checks every resulting proof
using only S1 instructions. On retaining the original rows the allowance equals
the old localized budget; off that source it records the row-violation cost.
An additional bound or probability/integrability premise is necessary for a
scalar or expected decision. Structural probability/domain meanings are not
automatically extended by removing their numerical constraints.

**R14 — availability-sensitive reconstruction.** A lost premise can be replaced
by a surviving same-query proof or a valid unconditional constant simplification.
Otherwise the retained argument is unavailable, not numerically false. For a
fixed snapshot, store support/bound alternatives and discard (S,b) in favor of
(T,c) only when T is a subset of S and c<=b. The explicit frontier can be
exponentially larger than its compact proof DAG. Pruning by current numbers is
not guaranteed to preserve later numerical revisions.

**Derived instruction basis.** The sixteen S1 tags admit expansion into
constant, row, rewrite, add, scale, convert, lattice, max_common, min_common
and all_cases. This is a convenient ten-tag basis, not a minimality theorem.
Selecting a proof-minimum branch is snapshot-specific; retain the original
family for future evidence withdrawal or numerical reselection.

The source-free weighted identity
min(alpha res(0,u), beta res(0,-u))=0 for alpha,beta>=0 has an emitted derivation.
It supplies a prospective sign-splitting ingredient without adding a trusted
case oracle. Automatic splitting, empty-branch proof search, and general
policy synthesis remain unimplemented. F07's final soundness audit remains a
separate task; no source-calibration or learned-neural claim follows here.
