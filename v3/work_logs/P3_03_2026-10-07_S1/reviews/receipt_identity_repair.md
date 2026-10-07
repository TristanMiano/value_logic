# Checked-receipt identity repair

Contributor: ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction agent.
October 7, 2026 UTC. **DEVELOPMENT only; zero additional concurrent research time credit.** No principal, ledger, clock or task-status files were changed by this repair.

## Finding and scope

The preserved `finite-cover-v1` core wrote accepted VM literals into the active constraint dictionary under `"vm:" + digest(q)`. A digest was consequently doing more than identifying an audit record: equality of two different queries' digest fields could cause the second accepted literal to replace the first.

If the first literal had already justified source pruning, the replacement could widen the represented finite source without rebuilding its cover. The correct VM answers alone would not establish the stronger invariant that every assignment satisfying the **current accepted constraint set** remains covered. This is a distinction between retaining the actual checked answers and covering the whole currently represented finite assessment source.

No SHA-256 collision was found or claimed. The diagnostic deliberately substitutes equal query-digest fields in two otherwise different queries. It exposes the assumption needed by the old identity scheme and checks a repair that no longer requires digest injectivity across admitted query positions.

## Preserved baseline and exact change

Before editing, the complete old core was copied to [core_before.py](../development/receipt_identity_repair/core_before.py). Its SHA-256 is `e8ac9bfda4addd9853a3b7ac174062a1152c8ec25cf6d2d09274d463c7d0419e`. The [prospective plan](../development/receipt_identity_repair/plan.md) and [baseline manifest](../development/receipt_identity_repair/baseline_manifest.json) were saved before the core change and any scientific execution for this repair.

The [current core](../../../checks/03_bounded_logic.py) now uses:

```python
rid = f"vm:{i}:{digest(q)}"
```

Its kernel version is `finite-cover-v2`. The VM remains `nat-register-v1`; the report interface remains `finite-cover-report-v2`. Only the kernel version assignment and this receipt-key expression changed, with explanatory comments added. The prior version's reports and traces remain preserved historical evidence.

The immutable admitted index is the disambiguator. The digest remains an audit suffix. For two different admitted positions $`i\ne j`$, their decimal-index fields followed by a colon differ, regardless of the digest values. Thus their active constraint keys cannot coincide. Caller assumptions cannot use the reserved `vm:` namespace. A completed job is not rescheduled until its receipt is withdrawn; withdrawal removes that job's key before the existing job reset permits reacquisition. These are the existing fixed-catalogue and supported-API conditions, not guarantees for arbitrary mutation of internal Python objects.

Under the current maximum of 12 queries, the largest index is 11. `vm:11:` followed by a 64-character digest has 70 characters, below `label`'s 128-character limit. The same identifier therefore remains admissible when passed to withdrawal.

## Counterexample and repaired invariant

The two diagnostic queries have ordinary bounded-run meanings. Query zero executes `HALT 1` in one instruction and asks for target 1, giving answer true. Query one executes seven increments and then `HALT 0`, with horizon eight and target 1, giving answer false. The delayed second job lets the first receipt be checked and used for source pruning before the second receipt arrives.

With equal query-digest fields in the preserved code:

1. The first receipt adds $`H_1=x_0`$. The source is narrowed to assignments with $`x_0=1`$.
2. The source process prunes the singleton assignments $`(0,0)`$ and $`(0,1)`$.
3. The second receipt replaces that dictionary entry with $`H_2=\neg x_1`$.
4. The current accepted source becomes $`\{(0,0),(1,0)\}`$, but the retained cover omits $`(0,0)`$.

The saved trace confirms the first acceptance at event 5, source pruning at events 9 and 11, and second acceptance at event 25. The all-current-source coverage failure occurs after the second acceptance. Both VM answers are still individually correct.

With indexed receipt keys, the second receipt adds its own entry and retains the first. The current accepted source is instead

```math
H_1\land H_2=x_0\land\neg x_1,
```

whose sole satisfying assignment is $`(1,0)`$. Earlier pruning remains sound. More generally, for this acceptance operation and a fixed immutable catalogue, adding a distinct new literal key conjoins a constraint and cannot widen the current source. The existing cover-inclusion proof therefore no longer needs a no-collision premise for this cross-query identity step.

Withdrawing the first indexed receipt removes only that receipt, restarts only its producer and retains the independent second receipt and completed job. The existing reset to the all-star cube covers the widened source $`\{(0,0),(1,0)\}`$. Source-only refinement then obtains those two singleton cells, and the reported range of $`x_0`$ becomes $`[0,1]`$ again.

## Narrow development result

The [new evaluator](../../../checks/03_receipt_identity_check.py) made one fresh [attempt](../development/receipt_identity_repair/attempt_1/summary.json): **PASS, five suites, 177 explicit assertions**. Its independent source check enumerates the four assignments directly and uses ordinary Boolean evaluation of the actual accepted constraints. It does not use the core's Strong-Kleene or interval evaluator as its reference.

| Suite | Checked result |
| --- | --- |
| Preserved-baseline obstruction | The deliberate equal-digest field surrogate reproduces one aliased constraint and missing assignment $`(0,0)`$. |
| Repaired coexistence and withdrawal | Both indexed constraints coexist; coverage holds at every recorded transaction boundary; independent withdrawal and rebuilding preserve the remaining literal. |
| Ordinary identities and exact reports | Genuine distinct digests yield the expected indexed keys; the 70-character maximum index case passes `label`; source-record substitution is rejected despite unchanged audit fields; objective revision invalidates the old report. |
| Unchanged wrapper compatibility | The existing wrapper produces current certificates under `finite-cover-v2`, retains current applicability through same-source refinement, and requires a fresh warrant after accepted evidence changes the source. |
| Exact authorized code delta | Whole parsed-source equality holds after applying only the declared kernel-version and key-expression substitutions to the preserved AST. |

All three two-query diagnostic runs reached the two accepted answers after 25 allowance-one calls, with the same acceptance/pruning event numbers. This is a result for these fixed cases, not a CPU-equivalence claim. The repaired source's longer identifiers naturally change some serialized records and boundary byte accounting.

The AST comparison identifies `Kernel._job_step` as the only changed function and records **33 unchanged function ASTs**. It also checks the entire module AST after the two permitted substitutions, covering assignments and other module structure as well as functions. Thus the VM operations, replay-checking logic apart from the final key expression, numerical interpreter, source-refinement transitions, scheduler, withdrawal/reset, report generation and exact current-warrant helper are unchanged. The wrapper file is unchanged. No generic suite or prior frontier/binding attempt was rerun.

The [manifest](../development/receipt_identity_repair/attempt_1/manifest.json) was saved before module execution. The attempt contains full repaired-core and evaluator copies, deterministic inputs, [complete traces](../development/receipt_identity_repair/attempt_1/traces.json), a [source diff](../development/receipt_identity_repair/attempt_1/core_delta.diff) and [AST/function comparison](../development/receipt_identity_repair/attempt_1/code_delta.json). Bound source files remained unchanged during the attempt. Host elapsed and process measurements in the summary are execution provenance and receive no research credit.

## Artifact hashes

| Artifact | SHA-256 |
| --- | --- |
| Preserved core | `e8ac9bfda4addd9853a3b7ac174062a1152c8ec25cf6d2d09274d463c7d0419e` |
| Repaired core | `841df6c5223844d2131642adcbb136855e054aa8833036506bb32c91aaf8afe6` |
| Narrow evaluator | `8d4d8808b2479614ea24b58f0827df6b1e9ca5428aca6cef92612de351ba380c` |
| Unchanged task wrapper | `5e7d7d669f4243dac0a0df77e429b86ac2439b7351dab70965702ccdc71b1e15` |
| Attempt manifest | `90463ddd62a6bdc687afa7b9450ba8206cec986ddca2a247ff192eb024827c29` |
| Attempt summary | `120a9ce1017643126bea4ed3e2e0ecbbdc6109fc8d2aad776dafb42fe5afe050` |
| Attempt traces | `c65731685f088794ae540cdd8321802893f03bb0a099fb82b12d2ffcde2a7df7` |
| AST comparison | `ad38185694671d0e451040e4bdcb5601417f8cfbc238648cfdc58f6065a1cba3` |

**Disposition:** the identified cross-query receipt-key alias is repaired at the immutable admitted catalogue scope. This is implementation identity work supporting the existing cover claim; it is not a new inference theorem, authentication mechanism, stronger numerical method or cryptographic collision result. Earlier results retain their original source hashes and scientific status.
