# F16 implementation and request reception review

**Disposition: no new substantive soundness defect found in the audited finite implementation.** The attacks did not produce an accepted false current request, silently retained source dependence, or a full-source refutation drawn from an inadmissible reduct point. A documented reconstruction incompleteness was reproduced. A stale public-status passage needs editorial repair by the principal F16 lane.

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, separate concurrent implementation audit agent. Baseline: `6ef27f20e3ac0920953a27dd84d6c91a021ba58f`. Session: F16, 2026-10-05. **Zero principal D/L/E/O minutes are credited for this concurrent work.** This is a separate agent review in the same model/tool environment, not external peer review, a proof-assistant development, or independent empirical replication.

## Scope and preserved evidence

Reviewed actual code: F05 semantics; F06 native rules, source transport and the receipt codec; F07 request receiver and finite/graded helpers; F11/F12 scientific input/native/producer/reference/receipt/reuse/selected-cache/catalogue modules; all five `program*.py` modules; the scientific experiment classifier; and the F11/F12 public contract and results. The [source manifest](implementation/attempt1_source_manifest.json) records SHA-256 for **26 reviewed files**, checks each against the baseline blob, records the interpreter version, and hashes the probe. Every listed file matched the baseline at execution.

New material is confined to this review and `reviews/implementation/`. No old implementation, frozen code, existing tests, or empirical artifact was edited. The main run produced **65 journal records: 59 substantive records and 6 setup/manifest records**. All passed; 40 of the substantive records were successful expected rejections. A bounded supplement added **3 substantive records**, including one further expected rejection. Thus there are **62 substantive probe records, 41 expected rejections, and no unexpected failures**. These are probe records, not a claim of 62 independent theorem tests; some records bundle several checks.

- [Main probe source](implementation/probes.py), [complete result journal](implementation/attempt1.jsonl), [summary](implementation/attempt1_summary.json), [stdout](implementation/attempt1.stdout.log), [stderr](implementation/attempt1.stderr.log).
- [Supplement source](implementation/supplement.py), [complete supplement result](implementation/supplement1.json), [stdout](implementation/supplement1.stdout.log), [stderr](implementation/supplement1.stderr.log).
- [Commands, bounds, exclusions and failures](implementation/commands_and_bounds.md).

Both execution attempts completed on their first run. Both stderr files are empty. No F15/ND01 stage was repeated, no population was generated, and no broad existing suite or timing benchmark was run. The supplement resolved two specific untested boundaries: an active derived bound beyond the external input-size cap, and retained-premise validation in the graded withdrawal helper.

## 1. Reconstructed kernel and receiver obligations

The written theorem's relevant scope is explicit: finite, closed, typed syntax, ordinary immutable data, exact integer/Fraction arithmetic, and finite real denotations. It excludes adversarial Python methods, mutation during checking, interpreter/hardware verification, and empirical source validation. See [the theorem boundary and implementation correspondence](../../../derivations/03_soundness.md), particularly sections 1 and 6. The probes respect that boundary. Constructing a new frozen object with incorrect claim metadata is used to challenge validation; mutating an object concurrently or replacing Python operations is not used as a supposed numerical counterexample.

In [F05](../../../checks/f05_semantics.py), `infer` checks every child before arithmetic simplification, `Context.validate` checks typed affine source rows and feasible witnesses for every live case, and `evaluate` uses lexical environments with the binder's right side evaluated in the old environment. `rat` rejects floats and booleans. These checks make zero multiplication and discarded-looking bindings unable to erase a type error. The source witnesses certify nonemptiness of the supplied mathematical cases, not the empirical truth of those cases.

In [F06](../../../checks/f06_inference_rules.py), `_form` collects exact affine combinations of normalized nonlinear atoms. Equal forms justify equal differences; failure to identify an equality remains conservative. `same_difference` also requires a common unit. The checker visits all instructions, validates strictly backward parent references, requires the stated budget to equal the rule recurrence, and matches the conclusion's normalized difference against that recurrence. The request receiver is a separate boundary.

I reconstructed the important sign cases rather than assuming nonnegative budgets. Nonnegative scaling and positive conversion scale negative budgets correctly. Negation reverses and negates the sides, leaving the same difference and budget. Lattice comparison rules take the maximum of premise budgets. Residual congruence clips the sum at zero. `all_cases` requires every live hidden case exactly once, the same literal expression pair, and the maximum case budget. Local results therefore cannot silently certify the union.

The hand-built signed fixture has 25 instructions covering all **16 native tags**. It uses `x` in `[-1,-1/3]`, `y` in `[-1/2,1/2]`, and a conversion factor `3/2`. All instructions were independently evaluated by F07 at exactly three points: `(-1/3,1/2)`, `(-1,-1/2)`, and `(-5/7,2/9)`, for **75 node evaluations**. The converted negative budget was `-1/2`; a residual bound attained `1/6`; a negative residual-budget sum was correctly clipped to `0`. Nested lexical shadowing evaluated to `1` at all three points in both evaluators. This supports the inspected correspondence; finite point checks do not prove the universal theorem.

[F07 `receive`](../../../checks/f07_soundness.py) checks the independent expected context, case and units, runs the native checker, then requires the exact root pair and scope and `root.budget <= expected.budget`. Attacks separately changed the revision, observation, interpretation scope, source row while keeping the revision string, requested case, local/global scope, pair, unit, and strength. All were rejected at the appropriate boundary. A semantically equivalent but nonliteral `x+0` request was also rejected, documenting a conservative limitation rather than an unsoundness.

The two-case fixture had local bounds `0` and `1`. The global proof was accepted at `1`, rejected at `0`, rejected when its advertised root budget was forged to `0`, and rejected when one live case was omitted. Equality was accepted; a stricter budget differing by `2^-255` was rejected exactly. These results support the [documented receiver contract](../../../derivations/03a_soundness_scope_and_use.md), section 5.

## 2. Source dependence, revision and withdrawal

[Source transport](../../../checks/f06_source_transport.py) is a current-proof reconstruction procedure. It requires fixed interpretation/observation and conversion meanings, a complete typed closed source substitution when coordinates change, and a case map covering every new live case. Replacement proofs are checked in the new context and must prove the substituted old row direction. Budgets are then recomputed through `_expected`, and the output is checked again. A weaker replacement is allowed because its weaker budget propagates; the procedure does not preserve a historical numerical bound by assertion.

The source attacks established the following within the fixtures:

| Attempt | Exact outcome |
|---|---|
| Withdraw the only nonconstant source row `x <= 0` and supply no replacement | `UnavailableProof`; no output proof. |
| Replace that row by a proof of `y <= 0` without a source substitution | `ProofError`; wrong direction rejected. |
| Supply the explicit closed swap `x -> y`, `y -> x` | Output proves the substituted `y <= 0`; a request for original `x <= 0` is rejected. |
| Omit an old source key, use a free local, or change observation meaning | Rejected before successful transport. |
| Withdraw a row used only under zero scaling | A source-free constant proof survives; it is valid at `x=37,y=-11`. |
| Put mixed-unit arithmetic under zero scaling | The type error remains rejected. |
| Retain `x <= 1` after withdrawing the better alternative `x <= 0` | New proof budget is `1`; the old budget `0` is rejected. |
| Withdraw both alternatives | No reconstruction. |
| Replay the same row direction with its bound relaxed from `0` to `2` | New budget is `2`; changing the direction instead is rejected. |

The alternative fixture supplies a small concrete countermodel to an *incorrect reuse claim*: after withdrawal, `x=1` satisfies the remaining source but violates `x<=0`. The actual implementation returns the correct weaker bound and does not accept that false request.

The graded helper was also checked at this boundary. With `x<=0` withdrawn and `x<=1` retained, the point `x=1` gives actual difference, reconstructed bound, exact penalty and linear penalty all equal to `1`. At `x=2`, a retained premise fails and `grade_at` rejects the input. A penalty is therefore not used to excuse failure of a retained row.

## 3. Scientific producer and reference correspondence

The inspected native error coefficients agree with direct quadrature algebra for the frozen quartic family. For the polynomial in `reference.task_losses`, composite trapezoid error at subdivision count `n` is

`beta/n^2 + gamma/n^4`.

Thus the signed integral errors are `beta+gamma` for T1, `beta/4+gamma/16` for T2, `-gamma/4` for Richardson, and `beta/16+gamma/256` for T4. The source and native implementation use these coefficients, absolute error, and the stated evaluation counts divided by 32. This derivation is specific to the public polynomial family; it does not justify arbitrary scientific programs.

The [reference](../../../verification/reference.py) imports the public input model but not native syntax, the producer's dual solver, its coefficients or answer tables. It executes the polynomial and quadrature algorithms directly. Its planar candidate construction includes the source boundaries and the two relevant absolute-value sign boundaries. Permanent coordinate bounds make this fixed source compact; degenerate sources are handled by boundary intersections and the feasible origin. This is the inspected bounded geometric route, not a claim that arbitrary optimization has been implemented.

At four hand-selected points—origin, `(-7/13,5/17)`, `(-1,1)`, and `(2^-255,-2^-254)`—all four direct task losses exactly matched the independently interpreted native terms. One asymmetric source with a 256-bit input denominator also matched the producer and reference. Its optimum was small, so a separate active-denominator probe was necessary before making a derived-size claim.

In that supplement, `beta_cap=0`, `gamma_cap=2^-255`, action T1 and requested budget `0` produced the exact bound

`255/2^263 - 3/32`.

Its reduced denominator has **264 bits**, exceeding the external input's 256-bit cap. Current receipt validation and the internal exact-bound request both accepted it without rounding. This confirms that the documented external size limit is not incorrectly reapplied to a derived bound on this fixture. The bounded receipt format's separate derived-rational limit remains applicable.

Zero basis budget and zero proof-step budget returned `unavailable` with no proof, even where the independent semantic request was true. No search exhaustion was converted into refutation. See [producer](../../../verification/producer.py), [experiment classification](../../../verification/experiment.py), and [the public contract](../../../verification/README.md), sections “Contract and independent routes” and “Bounds and saved receipts.”

## 4. Receipts and cache reuse

[Receipt decoding](../../../verification/receipts.py) validates bounded wire data and checks the archived proof against its own source; `receive_receipt` additionally compares that source and action with separately supplied current inputs and invokes F07. Archive decoding alone is explicitly not current-request acceptance. Advertised bound metadata must equal the checked root.

The probes rejected a wrong action, a stronger exact budget, a new revision with identical bounds, withdrawn source evidence, action metadata changed while preserving the old root, and bound metadata changed from its actual value to `0`. More substantially, a genuine historical proof was relabeled with a new evidence object and all current context IDs. The native checker still rejected it because the source-row arithmetic no longer justified the old conclusions or budgets. The numerical guard therefore does not depend solely on noticing a stale hash.

The documented F12 reconstruction miss reproduced exactly. Starting with all four optional bundles at zero, then changing to `beta_cap=0`, `gamma_cap=3/32` with both joint bundles absent, gave:

| Route | Bound | Zero-budget status |
|---|---:|---|
| Fresh native producer | `-3/8192` | Certified |
| Independent full-source reference | `-3/8192` | True request |
| Retained reconstruction | `+3/8192` | Unavailable |

The maximum is attained at `(beta,gamma)=(0,3/32)`. A reconstructed receipt is accepted for budget `+3/8192` and rejected for budget `0`. This is a genuine limitation of the selected retained strategy, already stated in [F12 results](../../../verification/F12_results.md) and the public README. It is neither a newly discovered kernel failure nor a refutation of the true zero-budget request.

[Selected caching](../../../verification/selected_cache.py) and the [catalogue](../../../verification/catalogue.py) retain coefficients rather than granting validity to an old source receipt. On an unchanged direction schema relaxed from small caps to the permanent box, the original bound was `1/32`, the current full reference/catalogue bound was `471/256`, and selected replay gave the weaker safe bound `61/32`. Both successful current outputs were emitted and received in the current context. Changed row presence and action were refused. A selected numeric screen failing the requested budget returned neither an advertised bound nor a proof. An empty catalogue also returned unavailable. Relabeling T1's cached coefficients as R reached the native checker and was rejected.

## 5. Program contract and target-unit reduct

The fixed program adapter is consistent with its executable model. The zero policy's expected loss is `error+second`; the adaptive policy's is `9/40+error`; hence their mean difference is `second-9/40`. The error coordinate's cancellation in this consumer is real source-independent algebra. Risk queries instead use the finite loss thresholds and the standard exact finite-tail construction, with fractional boundary atoms handled by direct execution in the reference.

The code intentionally cannot use an audit-unit row to prove a loss-unit result when no conversion path permits that direction. For `foreign_zero=True`, the full mathematical source imposes `error=0` through the audit row, whereas the producer's accessible target-unit reduct omits that row. These are different domains, not interchangeable refutation oracles.

At the documented boundary, risk budget `-1/20` has native/reduct maximum `-1/40` and full-source maximum `-3/40`. `program_control.assess` returned **unavailable**, and the reduct attainer failed full-source feasibility. Passing that attainer to F05 as a full-source point raised `SemanticError`. The insufficient reduct proof did not pass the actual request receiver.

At the extreme admitted confidence `alpha=1-2^-255`, the same foreign-zero source gave full maximum `0` and reduct maximum `17/20`; the producer remained unavailable at budget `0`. For the mean consumer with `second_cap=9/40`, budget `0` was certified while budget `-2^-255` was correctly full-source-refuted. Equality and strict violation were not rounded or conflated. See [program producer](../../../verification/program.py), [reference](../../../verification/program_reference.py), and [decision classifier](../../../verification/program_control.py).

## 6. Public claims and remaining disposition

The substantive finite implementation claims inspected in the F11/F12 contract are appropriately bounded: the producer is purpose-built; the reference is a separate implementation route; failed search is unavailable; full-source witnesses are checked before refutation; current request binding is required; reuse is not optimal retention; and coefficient caching is available to an ordinary baseline. The numerical checks above did not contradict those claims.

**Reception finding I-01:** the baseline `v2/verification/README.md` retains present-tense statements that F15 is selected/unstarted, that no held-out evaluation has occurred, and that F15 is next. These appear near lines 19–24, 200–201 and 219 of the baseline file. The parent was notified because the baseline already includes F15 saved artifacts. The principal documentation lane should reconcile those current-status statements while preserving historical F11/F12 validation statements. This is an editorial status inconsistency, not a numerical code defect; this reviewer did not edit that file.

No source-level repair is recommended on the evidence from this audit. Broader generalization, adversarial object isolation, interpreter reliability, empirical premise truth and optimal retained-proof search remain outside these probes and outside the inspected finite code claims. The first-run finite results do not erase the older native failures recorded in F11/F12; no cause for those failures is inferred here.
