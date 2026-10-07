# P3-03 checked-receipt identity — prospective narrow repair

Contributor: ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction agent.
October 7, 2026 UTC. **DEVELOPMENT only; zero additional concurrent research time credit.** This plan precedes the implementation change and the single planned scientific attempt.

## Question and preserved state

The current `Kernel._job_step` writes accepted literals under `"vm:" + digest(q)`. Two different admitted query positions with equal digest fields would overwrite one active constraint. If the earlier constraint had already justified pruning, this replacement could widen the currently represented source without rebuilding the cover. Does adding the immutable admitted query index make accepted receipt identities unconditionally distinct, while leaving numerical, VM, source-refinement, report-binding and scheduling algorithms unchanged?

The complete pre-edit core has been preserved as `core_before.py`, SHA-256 `e8ac9bfda4addd9853a3b7ac174062a1152c8ec25cf6d2d09274d463c7d0419e`. A baseline manifest will bind that file and this plan before the core is edited. Earlier attempt directories and their source hashes remain historical evidence and will not be changed.

## Authorized change

Use `f"vm:{i}:{digest(q)}"` for the internally accepted receipt identifier, where `i` is the immutable admitted query position. Bump `KERNEL_VERSION` from `finite-cover-v1` to `finite-cover-v2` because active-source identity semantics change. Keep the VM version and report schema/version unchanged. Do not alter the literal admitted for an answer, VM execution/replay, source splitting/pruning, numerical interpreter, scheduler or withdrawal closure/reset.

The index is the exact disambiguator; the digest is an audit suffix. Under the current maximum 12 queries, an identifier has at most 70 characters and fits `label`'s 128-character cap, including when supplied to withdrawal. Caller assumptions cannot occupy the reserved `vm:` namespace.

## Fixed diagnostic inputs and one-attempt scope

Use two different bounded VM queries and four explicitly enumerated Boolean assignments. The first query halts with output 1 in one instruction and asks for target 1, so its answer is true. The second executes seven `INC` instructions followed by `HALT 0`, with horizon eight and target 1, so its answer is false. Query versions and identifiers differ. Run in the existing round-robin schedule with allowance-one calls, capped by a fixed 128-call diagnostic limit. The delayed second query leaves time for the first checked positive literal to justify source pruning before the second receipt is accepted.

For the synthetic equality diagnostic, replace only the query-digest return field for these two query records with the same fixed 64-character hexadecimal string. Retain genuine digest computations for terminal states and other values. This is an explicit **forced-equal-digest field surrogate, not an actual SHA-256 collision**. Save all configurations, the substitution rule and expected answers before importing or running either core revision.

The single fresh `attempt_1` will contain these narrowly related checks:

1. **Preserved-baseline obstruction:** under the surrogate, demonstrate that the second receipt replaces the first literal and that the retained cover omits an assignment admitted by the now-current literal set. This is an expected counterexample to the preserved code, not a passing claim for that version.
2. **Repaired coexistence and coverage:** the same delayed sequence retains two different receipt identifiers and both true/false checked answers. Independently enumerate the four assignments satisfying the actual current accepted literals and verify cover inclusion at every recorded transaction boundary. Verify that first-receipt pruning occurred before second-receipt acceptance. Refinement after both receipts must retain coverage.
3. **Independent withdrawal and ordinary identities:** withdraw the first receipt after both were accepted. The independent second receipt, checked answer and completed job remain; reset restores coverage of the widened current source. Source-only refinement must remain sound. A separate run with genuine unique query digests must yield exactly the indexed identifiers expected from the immutable catalogue. Check the maximum admitted index's identifier length against `label`.
4. **Narrow report and wrapper compatibility:** a genuine current report is accepted, further refinement on the same source preserves its warrant, and withdrawal/objective changes reject obsolete reports. Exact source-record substitution with matching retained audit fields is rejected. One unchanged task-wrapper request must still produce a current certificate across source-only refinement under the new core version. These checks do not claim numeric JSON authentication.
5. **Exact implementation delta:** compare parsed pre/post source. After changing only the `KERNEL_VERSION` assignment and the receipt-ID expression in the preserved AST, the entire resulting AST must equal the new core AST. Also save the source diff and function hashes, identifying only `_job_step` as a changed function. This explicitly binds all unchanged VM, numerical, source-refinement, scheduler and report-binding code.

The diagnostic will save a manifest binding inputs, evaluator, plan, preserved core, repaired core and unchanged wrapper before module execution. Save complete traces, results, relevant hashes and host runtime observations. These runtime observations are execution provenance, not research time credit. Do not run generic suites, repeat historical attempts, or start a second attempt without retaining the first result and a specific new authorization or necessary correction.

## Interpretation

For distinct immutable positions $`i\ne j`$, the prefixes `vm:i:` and `vm:j:` differ regardless of digest values. Thus an accepted receipt for one query cannot replace another query's active literal merely because their fingerprints agree. The existing replay checker still determines answers using each actual original query. The repair removes this source-widening alias; it does not authenticate arbitrary records, create execution-lineage proofs, make hashes injective, or change the finite fragment's mathematical scope.
