# F07 S3 — public-source reconstruction of the checked pipeline boundary

Status: saved partial checkpoint; not F07 completion. Source revision:
`aad293c8ffa885605a39455bed61532cca18bc9a`. No prior ZIP or unpublished
conversation result supplies evidence. The source acquisition manifest records
which public files were recovered in full and checked against their Git blobs.

## 1. Reconstructed theorem layers

The assertion remains independently defined: a local root `(C,h,t,s,b,u)` means
`E_x(t)-E_x(s) <= b` at EVERY finite-real assignment in the particular case
`D_h`; a global root uses the union of live cases. A feasible rational witness
establishes nonemptiness only. It does not establish the source's empirical
applicability or make every point a probability model.

The combined statement has three different conclusions, not one overloaded
notion of 'accepted'.

* K acceptance establishes the actual returned root in the current context.
* A producer's advertised postcondition additionally needs its input contract
  and a proof of its transformation, or an independently bound receiving check.
* Operational use additionally needs the program, observation, proxy/criterion
  and probability interpretation specified for the request. None follows from
  a field name, version label or valid trace alone.

This is a conditional algorithm theorem on finite, closed, typed, immutable
supported data, exact int/Fraction operations and successful execution. It is
not a theorem that every valid mathematical input survives resource limits,
that every valid inequality is discoverable, or that an accepted bound is best.

### Native induction, reconstructed against the public implementation

`check` validates the ACTUAL context, then every stored instruction, not just
ancestors of the designated root. Parent indices must be non-Boolean integers
strictly below the current index. The context fingerprint is a stale-input
guard: the proof is rechecked against actual rows and operations, so the numeric
argument does not assume that hashing proves physical identity.

For a fixed signature, define the valuation of a collected form by the finite
rational sum of its coefficients times its source/nonlinear-atom valuations.
A nonlinear atom is a min/max of two already built forms. Induction on the
term, strengthened to the captured local environment, gives equality of this
valuation to recursive denotation. At a let, evaluate/collect the right side in
the OLD environment, then extend it. This is necessary even if a source and a
local variable share a spelling, or the same local subtree occurs under two
bindings. No node-only environment-insensitive cache is part of this proof.

Collection can erase a zero coefficient only AFTER typing the whole original
child. All operations act on finite real values, so cancellation is legitimate
even on an unbounded domain. This would not justify `infinity-infinity`.
Min/max child order need not be normalized canonically: a missed equality
causes refusal, whereas equal collected forms still entail equal denotations.
Units omitted from internal keys do not create an untyped rewrite: every
same-difference comparison independently checks its four top-level units, and
the fixed signature fixes each source coordinate and conversion factor.

The rule induction uses the same point x in the same case for every local
parent. Its numerical operations are identity, addition, nonnegative scaling,
positive named conversion, fixed nonnegative slack, min/max of justified
bounds, and the positive part of a sum for the residual. In particular:

    a1-b1 <= p, a2-b2 <= q
    => F(a1,a2)-F(b1,b2) <= max(p,q), F in {min,max},

because F is monotone and preserves a common additive shift, including a
negative shift. For `res_congruence`, the first comparison has reversed input
polarity; after adding the two preactivation bounds, maximum with the unchanged
zero branch forces `max(p+q,0)`. A strictly negative preactivation change need
not give strict residual improvement in a saturated region.

The `meet_proofs` minimum concerns one identical numerical difference, not two
alternative programs. Conversely, `all_cases` takes a MAXIMUM, covers every
live case once, and demands the literal same expression pair. These are
universal-domain quantifiers, not expected values or confidence aggregation.
The checker's final same-difference comparison transfers each constructor's
proved bound to the recorded pair. Finite ordered-DAG induction therefore
establishes every step and the designated root. Reusing a parent twice adds its
numeric contribution twice; it does not create independent evidence.

## 2. Exact source-level finding: `almost_exclusion`

Location: `almost_exclusion` in `v2/checks/f06_derived_cases.py` at the pinned
revision; its body was retrieved within the explicit 396–580 source range.
The inspection below is a derivation from that public body. The exact witness
was subsequently executed; its output is retained in the S3 evidence record.

Let its attached allowance proof have ACTUAL root `(a,c,b)`. Let the separately
checked guard proof have difference g and bound eta. Write k for the advertised
gain, d for the advertised old term, and z for its typed zero. On successful
return, the native checks enforce the following construction:

    g <=[eta] 0
    rho(g) <=[max(eta,0)] rho(0)
    k*rho(g)+d <=[k*max(eta,0)] k*rho(0)+d.

The final transitivity step requires exact normalized equality

    c = k*rho(g)+d.

Consequently the ACTUAL returned root is

    a <=[b + k*max(eta,0)] k*rho(0)+d.             (AE-actual)

This is a valid numerical result. Its right side denotes d, but generally is
not literally d. The function does not read `allowance.baseline` at all.
`allowance.new` determines a unit but is not compared to a. Thus success alone
does not authenticate those two advertised fields. The guard/gain/old fields
are constrained jointly by the actual middle-term equality; they are not all
completely unconstrained either.

This is NOT a counterexample to K soundness. Nor is it a refutation of the
correct-input mathematical transformation. It is a boundary between accepting
a proof-carrying record and proving that the record satisfies its advertised
contract. A caller must not report the advertised pair or baseline merely
because this helper returned a K-valid proof.

### Executed small exact witness

Use one nonempty case with no sources or rows; its witness is the empty tuple.
Take g=0, k=1, advertised old d=2. A constant K proof has literal pair

    new=1, old=2+rho(0), budget=-1.

Together with the constant guard proof `0 <=[0] 0`, this is an honest allowance.
Now replace only its advertised `new` field by 3 and its advertised `baseline`
by -100, retaining both proof objects. The current function's executed numeric
construction is unchanged: it returns a proof of a difference -1 with bound
-1. It does NOT establish the advertised claim `3-2 <= -100`, which is false.
A final receiver bound to that advertised request must reject it.

Even the HONEST record produces a right term containing `k*rho(0)+d` rather
than literal d. A receiver intentionally requiring literal root identity needs
a checked rewrite before accepting that honest output. This is an availability
boundary, separate from the metadata-authentication issue.

### Implemented receiving condition

Before consuming a GuardAllowance, check its attached proof against the current
parent and require its root to match the supplied current case, new term,
`old + gain*rho(guard)` and baseline; explicitly validate the rational gain and
baseline. Authenticate these relative to the caller's independently fixed
request, not by copying output metadata. After the existing arithmetic, append
an ordinary K rewrite to the requested literal `(new,old)` pair, then run the
unchanged checker. No new inference axiom or semantic operation is required.

The new `f07_near_exclusion_receiver.py` implements this receiving condition.
Its 47 tests pass in the documented public-source subset. Complete-checkout
integration remains pending; the original low-level producer is unchanged.

## Evidence boundary

Source-derived premises: F05 semantics, F06 native checker, F07 S1/S2 theorem
notes, and the public derived-case function body. The source-level dataflow and
small witness above are this session's fresh reconstruction. No external theorem,
independent reviewer, formal proof assistant, newly run full suite, novelty,
F08 work or neural experiment is claimed here.

## 3. Source transport and withdrawal: fresh dependency reconstruction

The published `_source_mapping` requires **every old source key**, exactly
once, and checks each replacement against that old key's unit. Its call to the
more permissive standalone `substitute` is therefore safe against the suspected
unmapped-source/unit loophole. This candidate objection is **excluded by the
actual wrapper**, not retained as a discovered bug. Scope and observation
identifiers must agree; conversions and the ordered unit table remain fixed.

For a closed simultaneous map sigma, define a transformation of old normal
forms by sending a source atom z to N(sigma(z)), rebuilding each min/max atom
from its transformed child forms, and collecting coefficients. It commutes
with addition and rational scaling. If an old nonlinear atom was already
constant-folded, its children are source-independent constants, so substitution
does not change that fold. Deleting zero coefficients also commutes with the
transformation. Induction strengthened to captured local environments proves
N(t[sigma]) = transform_sigma(N(t)). Thus every old source-independent exact
rewrite survives a legal substitution. This is not a claim that every true
equality is recognized by the normalizer.

`localize` first checks the entire input, selects the requested parent at
`all_cases`, and memoizes by proof-node index for one fixed target case.
Unlike caching open term evaluation by syntax alone, this memoization does not
confuse lexical environments: each retained proof node still contains its
complete closed expression. The selected budget is no greater than the old
maximum; every other native budget operation is monotone. This proves the
literal-pair invariant and the localized-baseline inequality together.

`prune` first checks all original nodes, then retains ancestors and renumbers
them in their original order. A parent index remains smaller after this
order-preserving map. `_copy_into` adds one fixed offset to every retained
reference. Neither routine purports to salvage an initially invalid unused
node. These facts suffice for the near-exclusion dependency path used here.

The published `soften_rows` does not first compile away a proof minimum. It
localizes and then recursively preserves all its native budget constructors.
At a withdrawn row a<=eta, lattice injection and rewrite produce

    a <=[0] eta + max(a-eta,0).

At a retained row, adding -eta internalizes its literal bound. At negation the
signed difference is unchanged; at transitivity/addition allowances add.
Nonnegative scaling and positive conversions transport the allowance. Slack
adds its fixed nonnegative literal. A proof minimum becomes the minimum of two
allowances on the same enlarged local domain. Common-side and lattice
congruence first raise both allowances to their maximum. Residual congruence
adds inner allowances and compares with the zero branch. A final exact rewrite
restores each original node's literal pair with its allowance on the right.
Every emitted comparison has budget zero. This establishes the advertised
expression-valued root by finite induction, independently of a sampled model.

Because eta+max(a-eta,0)>=eta for every finite assignment, monotonicity also
proves E_P>=b_h for every such assignment. The root inequality Delta<=E_P
still needs the retained source rows; nonnegativity of E_P-b_h alone does not.
The penalty vanishes when all used withdrawn rows hold. Neither property says
that an unverified returned field is the promised E_P-b_h. That is precisely
why field checking and numerical trace checking are separate obligations.

## 4. A narrow receiver theorem

Fix a current admitted single-case context C with case h and a caller-supplied
request J=(C,h,t,s,B,u). For an immutable supported GuardAllowance record, check
finite rational A and k>=0, the unit of g, and a local proof whose budget is A
and whose normalized difference is t-(s+k*max(g,0)). The receiver emits an
actual checked rewrite to the literal allowance pair

    C;h |- t <=[A] s+k*max(g,0).

The independently supplied request must name this same t and s. Check a second
local proof whose normalized difference is g and whose actual budget is eta.
Then ordinary real order gives

    g<=eta  =>  max(g,0)<=max(eta,0)
    => t-s<=A+k*max(eta,0) = M.

The original producer's budget recurrence returns M. Its right term is
k*max(0,0)+s rather than literally s. A candidate is accepted only after native
checking, matching the requested difference/scope, and verifying its actual
budget B_out<=M. A stronger valid candidate is permitted. An ordinary checked
rewrite removes the zero and yields the literal pair (t,s); this is not
permission to treat arbitrary terms as equivalent without an inference.
The existing request receiver then requires B_out<=B. A separately explicit
strict request additionally requires B_out<B. Equality supports only the
inclusive assertion.

This is partial correctness of successful returns and an explicit construction
for the stated mathematical implication. The baseline must be the input proof's
actual budget; a looser advertised baseline needs an explicit slack trace.
The theorem establishes neither strongest bounds, automatic proof discovery,
guaranteed runtime nor a statistical/empirical interpretation of the premises.
It cannot establish that a purported request genuinely originated independently
of a candidate; the conclusion concerns the request actually supplied.

## 5. Hostile reconstruction of the receiver's actual contract

Two implementation choices in section 4 are load-bearing. First, an
input proof may use a different pair with the same normalized difference;
it must be rewritten by a real K step to the advertised allowance pair before
being consumed. Second, an improved producer may return a **stronger** checked
bound B_out<=M. The adapter checks that inequality, then compares B_out—not
merely the conservative M—to the final inclusive or strict request. A valid
stronger output must not be rejected just because it differs from a nominal
formula. The original near-exclusion body currently produces exactly M.

The proof obligation is consequently:

    checked input allowance + checked guard bound
       => existence of a K proof with ceiling M;
    checked candidate with the same difference and B_out<=M
       => a checked literal root for the requested pair;
    B_out<=B (or B_out<B)
       => the requested inclusive (or strict) assertion.

The final implication does not need to trust the producer's method. The first
implication explains the advertised near-exclusion operation, not automatic
success of a particular implementation. A candidate proving an unrelated true
statement is rejected. A candidate proving this pair with a weaker-than-M bound
is also rejected even when a lax consumer request would accept that weaker
statement. Numerical validity and the producer postcondition remain distinct.

The checks authenticate numerical field consistency, not historical provenance:
a valid allowance record need not have been returned by a particular earlier
call to `discharge_branch`. Nor does the adapter establish that a caller's
request names the physically executed program. Those stronger conclusions need
independently supplied provenance/interpretation evidence.

The guard g may be any closed well-typed native expression with a checked upper
bound. It need not itself be affine. Affinity is required when a guard is
introduced as a *source row* by the sign-branch constructor, not for this final
numerical receiver. These are different API contracts. Conversely, k>=0 is
necessary for the particular formula M: with k=-1, g=0, eta=1 and A=0, the
formula would assert 0<=-1. Negative-gain expressions are not meaningless; they
simply need another bounding argument. Zero gains are admitted, although this
API still requires a guard proof and therefore is not a complete search method.

## 6. One paired-policy reconstruction, including the threshold

Let the fixed program with report r choose its second branch with probability
r. Let p,s be the two branch failure probabilities. The unit-priced failure
cost is converted explicitly from probability units to cost units. With an
additional second-branch use cost r/4 and common finite baseline z,

    J(r) = (1-r)p + r*s + r/4 + z.

The numerical coordinates above use the declared conversion factor one. Compare
r0=1/2 and r1=3/4. Let e be the *paired* proxy-to-intended discrepancy, with its
own premise e<=beta, and let g=s-p+1/2, also converted to cost units. The modeled
intended difference, computed from the branch law rather than from proof syntax,
is

    Delta = J(3/4)+e-J(1/2)
          = (s-p)/4 + 1/16 + e
          = g/4 - 1/16 + e
          <= (beta-1/16) + (1/4)*max(g,0).

This allowance follows from a lattice injection, the separate e row, constant
arithmetic and exact rewriting. No source row supplies the final composite
answer. A further checked g<=eta yields

    Delta <= beta-1/16 + (1/4)*max(eta,0).

For beta=1/32 and eta>=0, the bound is -1/32+eta/4. At eta=1/16 it is -1/64;
at eta=1/8 it is zero; at eta=1/4 it is +1/32. The first supports strict
improvement, the second only non-deterioration, and the third does not support
a zero-threshold request. These boundaries are attained: set s=0,
p=1/2-eta, e=1/32, with eta in [0,1/2]. All probabilities are valid, and z may
be any finite common baseline. Thus the threshold distinction is substantive.

An initial new test exposed a fixture error, not a kernel failure: the affine
row g<=eta normalizes to s-p<=eta-1/2. Passing that raw row root as if it already
bounded g is wrong. Adding the constant 1/2 and rewriting restores the actual
guard and its bound eta. The receiver rejected the mistaken fixture. The
initial failing run and source are retained; no assertion was weakened.

Several limits are visible in this same model. Increasing beta changes the
intended guarantee; proxy improvement alone does not fix beta. Changing the
price conversion changes the paired objective and requires new checking.
A report's own validity is a separate assertion: at p=1,s=1/4, the old report
1/2 understates its failure probability 5/8, even though the paired cost can
improve. Finally, these are comparisons at the *same current* p,s,z. A
historical comparison across changing sources needs the separate drift term
already identified in the published P15 argument.

## 7. The assumption-to-use boundary is not discharged by metadata checking

**Available observations.** Let x be hidden, A(x)=max(x,0), B(x)=max(-x,0).
The native identity min(A,B)=0 has a source-free K proof. A bound receiver may
correctly certify that numerical expression. It does not thereby implement an
action achieving it without observing x. A fixed randomization q has cost
q*A+(1-q)*B; at x=1 and x=-1 its costs are q and 1-q. They cannot both be zero.
This is a counterexample to a program interpretation, not to numerical soundness.

**Small coefficients on unbounded coordinates.** A bound on x+epsilon*z is not
a bound on x with an added constant epsilon. For epsilon>0, the finite point
x=1,z=-1/epsilon satisfies x+epsilon*z=0 but violates x<=0. Normalized guard
identity must retain that nonzero coefficient. A feasible witness with z=0
cannot justify deleting it. A bounded-domain error estimate would be a separate
premise, not an implicit rounding rule.

**Expected versus pointwise guards.** A scalar upper bound on E[g] cannot be
substituted for a pointwise bound on g in the generic positive-part allowance.
For equally likely g=-1,+1, E[g]=0 but E[max(g,0)]=1/2. With A=-1/4,k=1 and
Delta=A+max(g,0), the actual mean is +1/4, not the claimed -1/4 obtained by
clipping the mean. An outer expectation is legitimate after an actual
pointwise inequality, with measurability and appropriate moments. The specific
paired-policy difference is affine in g and can use a separate linear
expectation argument; that extra identity must not be inferred from an
arbitrary one-sided positive-part allowance.

**Unbounded common baselines.** In the paired-policy example, choose the same
random z=2^n in both programs with probability 2^(-n), n>=1. Every assignment
is finite, the probabilities sum to one, and each absolute mean baseline is
infinite because each summand in E[z] is one. The paired difference can still
be the constant -1/64. Its expectation exists, while subtraction of the two
infinite absolute expectations is undefined. A paired guarantee must not be
silently restated as that subtraction.

**Selection-aware validity.** On eight equally likely records d, let bound
procedure i for the same true difference 1 return 0 when d=i and 2 otherwise.
Each individual bound covers with probability 7/8. Selecting the minimum
returns the false bound 0 on every record. Its declared mathematical source
may still be nonempty and its K trace valid; the actual interpretation is
outside the selected source. A witness is not empirical calibration. Likewise,
Pr(accept AND false)<=alpha implies only Pr(false | accept)<=alpha/Pr(accept)
when the denominator is positive, not the same alpha conditionally on issuance.
These are explicit external probability obligations, not extra native rules.

## 8. Snapshot compilation and support-frontier contracts

A fresh source reconstruction of `compile_primitives` confirms its exact
snapshot contract. Transitivity becomes addition and an exact rewrite;
negation is a difference-preserving rewrite. Slack d>=0 is built from
min(0,d)<=d at budget zero and d<=0 at budget d, giving a reflexive comparison
with budget d. Lattice congruence uses two projections/injections followed by
`min_common`/`max_common`. Residual congruence reverses the first parent,
adds the second, and applies max congruence with zero. The compiler checks the
old numerical budget at every reconstructed node, then checks that only its
ten admitted primitive tags remain.

At a proof minimum it deliberately keeps the currently cheaper parent. This
is not evidence-update preservation. More precisely, for a *local frozen*
proof and the same row-bound coordinates, every expansion except that choice
preserves its entire bound recurrence. A selected parent is always at least
as large as the minimum of all original parents. Monotonicity therefore gives

    B_compiled(zeta) >= B_original(zeta),
    B_compiled(eta) = B_original(eta)

for the current old snapshot eta and arbitrary finite zeta, without claiming
that the changed source is empirically valid. Example: old row bounds (0,1)
on the same x select the first proof; updated bounds (2,1) give compiled budget
2 versus the retained family's budget 1. Rechecking still yields sound bounds;
the compiler need not retain the best future argument.

For the declared finite support grammar, a label (S,b) means a strategy with
numerical row support S and budget b. The code's dominance test

    T subseteq S and c<=b

preserves the best available bound for every alive-row set: whenever S is
available, T is available, and every budget consumer is monotone. Cartesian
parent combinations take unions of supports but retain arithmetic multiplicity
in the budget. A repeated shared row therefore counts once as an evidence
identifier and twice when used in an additive inequality. This does not imply
statistical independence or an optimal runtime/resource frontier.

Allowing separate recursive choices at repeated DAG occurrences does not
invalidate the numerical grammar: the finite proof can be unrolled. Moreover,
for a fixed alive set one lowest available bound at the shared node is no
worse in every monotone consumer, so inconsistent choices cannot improve the
best available value. This is not an arbitrary proof-search completeness claim.

The frontier is a *fixed-snapshot* record. Its bare Label type has no context
version; `best_label` on caller-supplied labels is not a proof receiver. A
consumer must use labels from the relevant audited computation and still obtain
and check a current root. Localizing a global proof before choosing alternatives
can additionally improve max_h min_i b_hi over min_i max_h b_hi. The static
frontier does not silently authorize that broader reconstruction grammar.

The case-producer dependency graph is noncircular at the relevant routine
level: native K -> prune/copy/localize/transport -> row softening and the direct
K disjoint-hinge lemma -> sign-case compilation -> the finite positive-min
lemma -> weighted coverage. The near-exclusion path needs only K, copy/prune,
and its input allowance; the new receiver adds no primitive. Final K checking
would protect the numerical claim even if a producer failed to produce an
answer, but it would not establish termination or metadata promises.

## 9. Fresh correspondence audit of the existing softening receiver

The published `expected_softening` / `receive_softening` pair was inspected
separately from the emitter. This is a source-level proof correspondence, not
an executed full-module regression in the rebuilt subset.

For each affine row l<=r, evaluation at the all-zero source assignment gives
its intercept c, whether or not that zero assignment satisfies the rows.
Because affine evaluation is total at every finite assignment, this computes
c without assuming feasibility at zero. Its reconstructed direction l-r-c
and budget -c are the same denotation and rational number obtained by the
emitter's affine collector. Closed lexical bindings and named conversions
preserve this equality by structural induction.

The receiver visits only the selected root's ancestors. At an `all_cases`
node it follows the unique parent for the independently requested local case.
All other budget constructors are reconstructed from their actual parent
results, rather than copying an unlocalized global bound. Hence induction
on backward references establishes that its baseline is the localized b_h,
and that its allowance is exactly the corresponding symbolic bound program
with the requested row replacements. Its literal root pair remains the old
root pair: the native case rule requires the same pair in its local parents,
and localization's other rewrites preserve the recorded pair.

For a retained row the allowance is its literal bound; for a removed row it
is eta+max(a-eta,0). Identity, sum, nonnegative scale, positive conversion,
fixed slack, proof minimum, common-side maximum and residual positive part
match the emitter's construction. In particular, softening does not first
compile away a proof minimum and thereby discard its future alternative.
The all-zero *defect* snapshot recovers b_h even when the all-zero *source*
assignment is infeasible. These are distinct uses of zero.

The receiver compares the complete revised context, the exact sorted row
indices, the localized baseline, the allowance and the penalty. It uses exact
normal-form comparison for the latter two expressions. Only after validating
the returned allowance presentation does it use that presentation in the
literal requested root t <=[0] s+allowance. Thus it admits harmless equivalent
syntax without allowing output metadata to redefine the requested numerical
function. A proof of t<=s+E alone would not authenticate the separate field
called penalty; the explicit comparison with E-b_h supplies that obligation.

The result is stronger than the new near-exclusion receiver's historical
contract: softening binds its output to a particular old proof, selected rows
and revision. Near-exclusion binds its input to a *valid current numerical
allowance*, not to an assertion that one particular earlier discharge routine
created it. A different but valid allowance proof can be accepted without
establishing that alleged history. Neither receiver authenticates empirical
provenance or the meaning of a program merely from strings or fingerprints.

## 10. Combined acceptance map and current disposition

The load-bearing implication has the following explicit premises. Let J be a
request fixed independently of the candidate output. Let C be its actual
current, nonempty context, with finite supported immutable data and the stated
finite-real interpretation. An accepted trace must satisfy the native checks
and have the requested domain, unit and comparison, with an adequate bound.
Then native derivation soundness and exact-difference replacement establish
J throughout its declared domain. Each extra producer field used to interpret
or construct J needs its own checked relation to the independently fixed
inputs. An arbitrary heuristic may propose the trace; successful checking
neither proves that it always produces one nor authenticates its narrative.

| Acceptance layer | Evidence used here | Boundary |
|---|---|---|
| Data and numeric domain | Published F05 admission and F07 S1; complete F05 module hash verified | Finite exact supported inputs; not arbitrary mutable/adversarial Python objects or infinity arithmetic |
| Normalization | Published S1 lexical proof; complete native checker hash verified; fresh substitution audit | Equal normal forms imply equal functions; not completeness of equality recognition |
| Rules and finite derivations | Published sixteen-tag pointwise and function-space reconstructions; 106 native/semantic tests rerun | Mathematical code correspondence, not proof-assistant or runtime verification |
| Current request | Published S1 receiver source; new near-exclusion receiver and hostile tests | Literal scope/unit/pair and actual bound, not producer-supplied target copying |
| Producer postconditions | Published S2 contracts; fresh softening, compilation and near-exclusion reconstruction | Near-exclusion metadata must be checked; successful return alone is insufficient |
| Concrete modeled use | Section 6 directly derives the fixed-report paired comparison and an attaining model | Explicit probability law, program identity and paired proxy premise; no learned calibration claimed |
| Deployment | Sections 7 and 9 preserve observation, empirical validity, probability and history conditions | These premises are not generated by proof checking |
| Execution and time | Actual run records and measured segments in the S3 work log | Source-subset tests are not full repository validation; no time is inferred from output size |

The older function-space argument is consistent with this map: restriction
preserves pointwise operations; a covering family of domains justifies a
maximum of local constant bounds; globally applicable allowance functions
justify their pointwise minimum. No integration homomorphism for min/max or
infinite lattice completeness is needed. Its optional ordered-vector-lattice
interpretation is an assumption-strength comparison, not a newly implemented
carrier or a replacement for the adopted finite-real source semantics.

**F07 remains partial in this delivery.** The new receiver closes a focused
input-contract obligation, but the complete producer modules and the full
published F07 suite have not been reconstructed and executed in this public-only
workspace. The measured session floor is assessed in the work log, not inferred
from this note's length. No new Gate B pass, F08 work, independent review,
formal verification, learned neural structure or novelty is claimed. The root
README, original checker/producers, old work records and master ledger bytes
are not rewritten by this additive checkpoint.
