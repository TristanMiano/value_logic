# F16 core review — comparison after saved reconstruction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated distinct reconstruction.
Base commit: `6ef27f20e3ac0920953a27dd84d6c91a021ba58f`.
Date: 2026-10-05 UTC.

**Result:** no new mathematical defect was identified in the reconstructed
native soundness theorem or the unit-directed completeness dependencies examined
here. The necessary request, source, unit, case and operational qualifications
are present in the existing statements. One false syntactic dependency claim
in **my initial reconstruction** is corrected below; the project's existing
proof already states the correct denotational lemma.

This is a scoped F16 contribution, not principal acceptance, a gate decision,
external formal verification, or an assertion that every optional theorem in
the surrounding project has been reconstructed. Gates C/D and F17 remain
unattempted. Concurrent delegated work adds **zero principal minutes**. No old
source, experiment, frozen evidence, timing record, clock, or root report was
edited.

## 1. Reconstruction order and evidence inventory

The preserved [initial reconstruction](core_initial.md) was saved before opening
the derivation proofs. Its SHA-256, checked both before and after comparison,
is:

`e27d628497e93a77827b013e1341b1fa2e4037567a94c32489368c521fe5623a`

The initial note lists the precise information seen beforehand: F05 semantics,
F06 native checker, project specification, and notation. The last two contain
theorem summaries, so this was definitions-first work with disclosed project
context, **not a fully blinded external review**. The initial note remains
unchanged, including its later-corrected sentence.

After that save, I read these four requested documents in full:

- `v2/derivations/03_soundness.md`;
- `v2/derivations/03f_soundness_acceptance.md`;
- `v2/derivations/04_characterization.md`;
- `v2/derivations/04g_characterization_acceptance.md`.

I followed these relevant dependencies, reading the indicated portions rather
than treating an entire referenced file as reviewed:

| File | Inspected portion and purpose |
|---|---|
| `v2/checks/f07_soundness.py` | Lines 1–165: independent evaluator and actual `Request`, `request`, `receive` implementation. |
| `v2/derivations/04a_characterization_reconstruction.md` | A3–A4, B–B2, C–C4: rational consequence, lexical dependence, local extension, and joint-domain separators. |
| `v2/derivations/04b_uniform_revision_characterization.md` | Sections 3–6: native max-min equality, dual certificate construction, finite vertices, and preservation of replay alternatives. |
| `v2/derivations/02c_derived_cases_and_completion.md` | Sections 2–3 and 16.1–16.2: guard discharge/envelope, disjoint-hinge use, and fixed generic positive-min lemma. Headings/reference searches also exposed its outline. |
| `v2/derivations/02b_source_transport_and_withdrawal.md` | Sections 14–17 and the immediately preceding retained-proof example: constructor-level discharge and the independent disjoint-hinge proof. |
| `v2/checks/f06_derived_cases.py` | Module setup, bounded-result helper, and `_positive_min_lemma`/`positive_min`; searches located its relevant call sites. |
| `v2/checks/f06_residual_discharge.py` | Imports and `disjoint_hinges`, including the preceding result check and following observation-table helper. |
| `v2/checks/f06_source_transport.py` | Lines 1–235: pruning, localization, typed substitution, current leaf reconstruction and the beginning of row restriction. |

A function-name search also inspected the names in
`v2/checks/f07_acceptance_audit.py`; its full implementation was **not** audited.
An attempted search for `f07_soundness_audit.py` found no such file, after which
the actual receiver module above was used. No gate review, new F16 root report,
or other agent's review was opened. Imports executed by the bounded probe are
limited to the named F05/F06/F07 modules and their standard-library dependencies.

The reproducible supplemental work consists of
[adversarial_probes.py](core/adversarial_probes.py) and
[adversarial_results.json](core/adversarial_results.json). It ran nine bounded
families successfully, including one fixed generic macro. No test discovery,
broad suite, neural run, or performance comparison was performed.

Invocation from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import runpy
runpy.run_path('v2/work_logs/F16_2026-10-05_S1/reviews/core/adversarial_probes.py', run_name='__main__')
PY
```

## 2. Objections, minimal witnesses, dependencies and disposition

| ID | Exact challenge / minimal witness | Earliest dependency | Status and repair assessment |
|---|---|---|---|
| CORE-01 | In a free x:U context, `0 <=[0] 0` checks although the different requested `x <=[0] 0` fails at x=1. | F07 current-request receiving, after native root soundness. | **Closed by the existing receiver.** It checks current context, case, literal pair, unit and sufficient strength. No core repair. Callers must use that contract. |
| CORE-02 | U->V only, source x:U, row `convert(x)<=0_V`; full semantics entails `x<=0_U`, but the U-reduct admits x=1. | F08's original unrestricted completeness conjecture. | **Known obstruction correctly scoped by U1.** This refutes full-source completeness, not native soundness. A stronger interface would need an explicit added bridge/rule or a context criterion; it cannot be silently assumed. |
| CORE-03 | `let dead=src(v:V) in 0_U` is well typed with no V->U edge and denotes 0. | Initial reconstruction §6's syntactic-leaf sentence. | **Reviewer correction only.** Existing 04 §4 and 04a B correctly use denotational dependency and unused-binding erasure. Preserve the initial record; no project edit required. |
| CORE-04 | h0 has x<=0; an added h1 admits x=1. A h0 proof remains local, while a global x<=0 request is false. | Domain indexing in F07 S6/S10 and F08 local-extension step. | **Defended.** Same-case extension checks; global receipt and an `all_cases` node missing h1 reject. Existing 04 §14 and 04a B2 keep the proof local until exhaustive aggregation. |
| CORE-05 | A factor-2 conversion of min does not generally have the same opaque normal form as min of the converted terms. Treating semantic equality as a bare rewrite would leave a construction gap. | F08 U2/U3 and the native normal-form stage of U11. | **Defended by explicit native proofs.** The independent fourteen-node path/min witness checks. The generic distributivity dependency is separately discharged below, without using U1. |
| CORE-06 | Replace shared theta in the two component rows by t1=1,t2=0, with N1=N2=1/4 and O1=O2=0. Rows hold, combined gap is +1/2, not the proposed -1/2. | F05 shared-source interpretation; F06 add/rewrite. | **Defended.** Distinct source atoms prevent the cancellation; the attempted rewrite rejects. A compressed input that forgets joint information would need a separate adequacy proof. |
| CORE-07 | Empty case list, or live rows x<=0 and 1<=x with witness x=0. | F05 context admission and F07 nonvacuity. | **Defended.** Both are rejected. Temporary empty sign children instead require a strict infeasibility ray and do not become live contexts. |
| CORE-08 | Unit cycle U->V of factor 2 and V->U of factor 3 sends x=1 to 6. Cancelling the cycle to x would be false. | F05 conversion meanings and F08 retyping ratios. | **Defended.** The false identity is rejected. U3 retains actual factors and does not assume reciprocal or coherent cycles. |

No entry in this table requires reopening an accepted native soundness premise.
The first, second, fourth and fifth challenges are substantive obligations;
their resolution depends on the stated wrapper or construction, rather than
on a generic assertion that the system is sound.

## 3. Native soundness comparison

The initial reconstruction independently defined finite-real denotation,
case domains and signed difference validity, then proved the collection
invariant and all sixteen rule families. These match 03 S1–S6 and the combined
theorem in 03f §§1–2.

The critical normalization invariant is captured-environment evaluation. An
opaque min/max atom contains already normalized children, so the same lexical
node under two different bindings cannot be merged merely by node/name identity.
At a let, the RHS is processed in the old environment. Source and local names
remain separate. Recursive typing precedes zero-coefficient erasure, preventing
an ill-typed or unbound discarded child from becoming an accepted expression.
Numerical form equality is used only after compatible outer units are checked.
The soundness proof does not assert that this collection procedure recognizes
all true equalities.

The rule proof is pointwise in one assignment, which preserves all stated
source dependence. Addition does not need probabilistic independence; it does
need both premises at that assignment. Shared parent references count twice
when added twice. Min/max congruence preserves negative budgets because those
operations commute with a common additive shift. Residual congruence has a
different bound, `max(beta+gamma,0)`, because its zero arm is unchanged. The
initial saturation witness shows exactly why the zero cannot be removed.

Proof induction is over backward references. For non-case constructors, the
parents have the same local/global scope. For aggregation, the local domains
cover the union; no assignment is presumed to satisfy every case's rows at
once. The same literal pair is required across cases. This numerical condition
is a sufficient syntactic safeguard, while the identification of that pair
with one observation-legal program remains an explicit operational premise.

The checker validates every stored instruction, including unused ones. Its
soundness for the actual supplied context does not rest on an injective-hash
theorem: rows and their current budgets are checked against that context.
Fingerprinting supplies a stale-input guard, not physical provenance. The
existing proof explicitly excludes mutable/adversarial Python objects,
infinite syntax, runtime correctness and resource availability from its
algorithm-level theorem. Those limits agree with the code reviewed here.

The expected conclusion is therefore source-relative numerical validity of
the actual checked root, not correctness of uninspected external actions,
empirical source rows, probability calibration or intended utility.

## 4. Current request: exact closure of the initial witness

`f07_soundness.receive` first checks the independently supplied request against
the current context, validates its case and typed terms, invokes the native
checker, and compares the returned literal root pair and case to the request.
Finally it requires the root budget to be at most the requested inclusive
budget. This implements exactly the strengthening-to-weakening argument in
03 S10.

The bounded probes establish four specific rejections and a positive control:
the valid constant root is accepted for its actual request, and rejected for
the x-versus-zero request; an x<=1 root is rejected for x<=0; a foreign unit
is rejected; a request retained across the changed context revision is
rejected. The local-extension probe adds a fifth domain-specific rejection:
a still-valid local h0 root is insufficient for the global request when h1
admits a violating point.

The interface is inclusive. A proof at exactly threshold B establishes
`Delta<=B`, not `Delta<B`. A strict caller needs a strictly smaller certified
budget or another strict argument. 03 S10 and 03f §2 state this explicitly;
the low-level receiver's inclusive contract does not silently change it.

Producer fields are a separate layer. 03f's combined theorem requires either
the relevant producer theorem and input contract or independent receipt of
each field used. A K-valid root alone does not authenticate arbitrary attached
`penalty`, baseline or program-identity metadata. The broader collection of
producer postconditions was not independently re-audited here; this review
confirms that the soundness statement preserves the distinction.

## 5. Unit reduct, lexical correction and joint domains

The initial note's sentence claiming every *syntactic* source occurrence of a
u-term reaches u is false. The saved post-comparison probe is a concrete
counterexample: `let dead=v in 0_U`, with v:V and no conversions, is typed U,
evaluates to zero at v=41, and has a checked zero-budget equality to `0_U`.
This correction does not weaken the proof-ancestry argument: all *premise
units* of a target root still follow unit-preserving edges or declared
conversion paths. An unused foreign RHS is not a premise carrying an
inequality into another unit.

The correct semantic lemma is proved with a typed local environment. For a
term of output unit u, agreement on source/local values whose units reach u
implies equal denotation. In the let case, either the RHS unit reaches u,
in which case its value agrees by induction, or the new local's value is
irrelevant to the body's u-denotation. This uses total, pure finite terms.
It would need revision for an effectful language where unused evaluation has
an observable side effect or exception; that is outside F05.

With that correction, the reduct necessity proof is direct: inspect only
the checked root's ancestors, retain rows whose units reach u, and repeat
the soundness induction with local reduct domains and their union. No source
feasibility check itself generates an inequality. Reusing the old serialized
trace after removing rows would still require new indices/fingerprint; the
mathematical proof does not claim that such unchanged replay works.

The source-union characterization also preserves joint information. After
projecting to the relevant coordinates, a finite union Q has the explicit
nonnegative CPWA probe

`V_Q(x) = min_h max(0, max_j(a_hj.x-b_hj))`.

It vanishes exactly on Q. At a point outside Q, each member contributes a
positive violation, so the finite minimum is positive. This proves the
separation step in 04a C without replacing a nonconvex union by its convex
hull. The example `(-infinity,-1] union [1,infinity)` versus the entire line
has identical affine upper-bound answers but is separated by
`min(max(x+1,0),max(1-x,0))`. Thus an affine-only answer summary would lose
information used by this language. U9/U10 correctly compare projected joint
domains, and local queries retain their named-case qualification.

## 6. Construction and circularity check

Two completeness ingredients deserve separate treatment: ordinary numerical
representation, and an actual native proof of that representation. The
initial note's geometric max-min route supplies the former; it is not by
itself a license to rewrite opaque nonlinear atoms. The post-save comparison
checked the latter rather than silently treating the initial outline as a
completed native equality proof.

### 6.1 Forward conversion through lattice operations

The independent factor-2 min construction uses projections, positive scaling,
`min_common`, conversion and checked arithmetic rewrites. It proves both
directions in fourteen native nodes, without a reverse edge. The source's
chosen numeric scale can be inverted by a rational coefficient without
reflecting an arbitrary target-unit premise back to the source unit. The
existing U2 proof uses the same mechanism, and U3 explicitly accounts for
different path factors. This resolves the opaque-atom conversion issue and
the incoherent-cycle attack without adding an inference rule.

### 6.2 The source-free hinge chain has no completeness dependency

The key primitive algebra can be reconstructed directly. Put
`a=max(g,0)`, `c=max(-g,0)`, `m=min(a,c)`. From the max injections derive
`c<=a-g`. The two min projections then give `0<=a-m` and `g<=a-m`.
Max-common yields `a<=a-m`, hence `m<=0`. All these are existing rules and
exact affine rearrangements. Positive weights follow by dividing by their
positive maximum, using nonnegativity, then scaling back. This proves the
disjoint-hinge lemma without sign cases or distributivity.

Guard discharge reconstructs a fixed proof's monotone budget program with
the removed row replaced by its explicit violation allowance. Its finite
gain is certified by another native envelope; it is not merely attached
metadata. Opposite guard allowances then vanish by the disjoint-hinge lemma.
The generic positive-min identity needs only the fixed affine split on the
two formal variables a-b. Once discharged, the result has no source-row
assumptions and can be instantiated by closed same-unit terms.

The bounded post-comparison probe instantiated the second argument by the
nonlinear term `max(y,0)`. Its returned proof had **192 nodes**, only native
tags, **zero row reads**, and budget **zero**. This is a finite checked witness
for the generic lemma's existence. It does not ask the sign compiler to
pretend the substituted nonlinear guard is affine, and it does not invoke U1.

Translation, positive homogeneity, negation and elementary lattice
associativity/commutativity are likewise derivable from projections,
injections and common-bound rules. The positive-min identity supplies
distributivity after translation. Iterating these identities gives native
max-min normal-form equality, which can then be used in U1/U11. This ordering
is the noncircular chain stated in 04b §3 and 04g §3.

### 6.3 Rational clause certificates and finite attainment

For a clause `min_j(a_j.x+c_j)` over nonempty `Ax<=eta`, introducing a
mathematical hypograph coordinate gives a feasible linear program. Its dual
has nonnegative lambda and alpha, with `sum(alpha)=1` and
`A^T lambda=sum_j alpha_j a_j`. Weighted native minimum projections put the
clause below the alpha-weighted affine sum; weighted source rows bound that
sum. Constants and exact affine rewrites remove the mathematical auxiliary
coordinate. No unsupported new source is added to the native proof.

04a A3 reconstructs the exact multiplier using rational elimination and the
attained projected endpoint. It does not require a vertex of the original
source or compactness. The finite CPWA cover then makes a bounded overall
maximum rational and attained. This is why strict validity has a uniform
strict rational budget in the declared finite closed fragment; it would
fail for the sequence -1/n against threshold zero or for arbitrary open
domains.

The optional uniform replay construction examined in 04b fixes the dual
feasible sets independently of RHS values. A minimizing dual point of least
positive support is a rational vertex: a supported kernel direction would
either improve the objective or remove a support coordinate. Finitely many
supports yield finitely many alternatives. Retaining all of them allows
native minima of proof budgets to recompute the correct optimum under each
admitted RHS revision. The existing text expressly warns that a transport
adapter choosing one current minimum parent can lose this property. The
current-request theorem and uniform-replay theorem are not conflated.

## 7. Limits of this contribution and handoff

The core rules, request receiver, target-reduct necessity, forward retyping,
case-local extension, native normal-form dependency chain and rational clause
construction were examined substantively. I did not independently reconstruct
all optional U12–U18 results, the complete producer library, the integrated
F11+ pipeline, empirical interpretations, current task scheduling, or novelty.
Reading those topics in 04g's summary is not recorded as a full audit.

The bounded probe command exited successfully; all intended rejections and
the positive controls behaved as reported. The initial reconstruction's hash
remained unchanged. The review artifacts are the only files written by this
delegated task. No new repair is proposed for the accepted mathematical core
on this evidence. The principal should preserve the existing scope restrictions
when integrating this contribution and handle the overall F16 decision under
the independently maintained task process.
