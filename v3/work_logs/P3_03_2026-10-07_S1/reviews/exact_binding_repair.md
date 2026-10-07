# P3-03 exact current-warrant records — repair and narrow evidence

Contributor: **ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction
implementer**. October 7, 2026 UTC. **DEVELOPMENT**, with zero additional
concurrent research time credit. This is the implementer's record, not an
independent review of their own edits.

## 1. Reason for the repair

The prior current-warrant helpers compared active-source, loss and catalogue
fingerprints. SHA-256 is an audit fingerprint, not a mathematically injective
encoding of every admitted record. Exact record identity therefore required
an explicit collision premise or an exact representation comparison. The
principal selected full records and exact canonical-byte comparison.

The repair concerns **current represented-premise and target identity**. It
does not decide equivalence between differently written theories, programs or
loss expressions. It does not authenticate arbitrary JSON, verify a reported
number, or establish exact execution-lineage identity. These are distinct
services even when a report contains the same request fingerprints.

## 2. Actual interface changes

The core now declares `REPORT_VERSION = "finite-cover-report-v2"`. Its VM
version `nat-register-v1` and mathematical kernel version `finite-cover-v1`
are unchanged. Genuine core reports carry:

- `source_record`: VM version, complete current query records and exact active
  constraints, including their kinds and dependencies;
- `loss_record`: the queried expression, unit and version;
- the report interface version, alongside the existing audit fingerprints.

`report_is_current` compares canonical bytes of the reported source and loss
records with the current records, retaining explicit scope/version/epoch
checks. The fingerprints remain available for auditing but no longer decide
current represented applicability. The original-input fingerprint does not
become a claim of exact execution lineage. Older fingerprint-only report
interfaces are rejected by the new helper rather than silently reconstructed.

The wrapper advances to `named-action-regret-v2`, with output schema
`value_logic.P3-03.task_certificate.v2`. It carries a full `task_binding`:
wrapper version, original supplied catalogue, selected action, tolerance and
common unit. Its stored original binding is immutable canonical bytes;
`certificate_is_current` compares the returned task record against those
bytes before using the repaired core helper. The existing live catalogue,
compiled-loss and query guards remain in place.

Reported records are historical copies. Subsequent live revisions cannot
rewrite them, and editing a caller's returned record cannot mutate the live
kernel. They remain ordinary editable JSON objects; historical-copy behavior
does not make a client's arbitrary edit authenticated evidence.

Canonical encoding/comparison and the additional record serialization are
charged as boundary work or recorded output bytes under the existing
accounting convention. No equal-CPU-cost or unchanged physical-runtime claim
is made for the expanded interface.

## 3. Mathematical computation preserved

The [pre-edit AST record](../development/binding_baseline_ast.json) was saved
before changing the two source files. The narrow check compares that record
with the repaired source, ignoring line-position metadata.

| Module | Interface changes | Preserved computational code |
|---|---|---|
| Core | `source_identity`, `report`, `report_is_current`, `snapshot`; adds `source_record` | 29 other function ASTs are unchanged, including admission, Boolean and interval evaluation, arithmetic limits, VM steps/receipts, scheduling, cube refinement, source updates and withdrawal. The mathematical `report` prefix through exact-source determination is unchanged. |
| Wrapper | Constructor binding metadata, certificate output, current-certificate helper; adds `_task_record` | Eight other function ASTs are unchanged. The compiler block from regret-piece construction through core creation is unchanged, as is the certificate's mathematical prefix through threshold determination. |

This is precise source-delta evidence, not an assertion that the entire program
or every observable resource count is unchanged. It supports reusing the
earlier numerical/VM/refinement diagnostics at their recorded source scopes,
while the new attempt targets the changed binding interface directly.

## 4. Prospective narrow attempt

The [binding plan](../development/binding_plan.md) and baseline AST were saved
before the first repair execution. The dedicated
[checker](../../../checks/03_exact_binding_check.py) saved its fixed inputs
and manifest before importing the changed modules. It used a fresh
`development/binding_attempt_1` directory. Earlier development attempts and
their source hashes were preserved; neither broad earlier suite was rerun.

The saved [summary](../development/binding_attempt_1/summary.json) reports
**PASS: seven suites, 35 explicit assertions**:

| Check | Result |
|---|---|
| Same original input and equal counters, different active source | Exact source records differ; cross-source reports are rejected. |
| Forced equal audit fields, unequal source/loss records | Exact comparisons reject the substitutions despite matching visible fingerprints. |
| Full task binding | A different catalogue or selected action is rejected. Splicing a genuinely current core report into another task's output still fails the complete task-record check. |
| Historical copies and revisions | Returned source, loss and task records remain unchanged by later live edits; withdrawal and objective changes reject old warrants. |
| Same-source refinement | A looser core warrant and a genuine task certificate remain current after further processing of the unchanged source. |
| Explicit non-authentication | Altering only numeric bound fields can leave the identity helper true. This demonstrates that the helper does not verify the altered numbers. |
| AST scope | The declared unchanged functions and mathematical report/compiler fragments match their pre-edit AST hashes. |

The forced-fingerprint cases are **deliberate field substitutions**, not
discovered SHA-256 collisions. Their purpose is to ensure that full records
actually determine the repaired predicate rather than merely accompanying
the old hash comparison. The numeric-edit cases are deliberately not valid
certificates; passing that diagnostic means the helper's limited identity
scope is visible and is not being misreported as proof verification.

## 5. Artifact bindings and observed execution

| Artifact | SHA-256 |
|---|---|
| Repaired core | `e8ac9bfda4addd9853a3b7ac174062a1152c8ec25cf6d2d09274d463c7d0419e` |
| Repaired wrapper | `5e7d7d669f4243dac0a0df77e429b86ac2439b7351dab70965702ccdc71b1e15` |
| Narrow evaluator | `b5ecd179546c94173bc237fef12039340071642a6590f8229e2cc8f731e870f3` |
| Pre-edit AST record | `4a66031372b375bbce5346015ed4bf8af035ad7aad3670658c2b083de10d3ea7` |
| Inputs | `052226f2888b3ab61a6f0e92906bfe3f0d710073ade84fd743016568e989c7f4` |
| Traces | `de534417f20f1ab10685757f10e37adfdd9c15cfa8effd1973820c705ee380e8` |
| Manifest | `e097f192dbb747953c2436b298051ba135743f8beea8ac957c6294ee19b069a1` |
| Summary | `655608dbebf0bdcf603f109ebea737179b64e6c654630924699d0e050421a5a8` |

Read-only checks confirmed every manifest dependency, input/trace hash and
assertion sum. The observed execution ran from
`2026-10-07T16:16:30.645578+00:00` to
`2026-10-07T16:16:30.698902+00:00`, with host elapsed time
**53,323,377 ns** and process time **51,879,551 ns**. Both manifest and summary
record additional concurrent research credit as zero.

## 6. Disposition

The exact-record repair is complete at the stated interface scope. It removes
the need for a hash-collision premise from the positive current-record identity
claim. Historical report correctness still comes from its original computation
and evidence; matching records alone cannot supply those proofs. No forecast,
learning, computation-selection or counterfactual algorithm was added, and
P3-N01 is not supported merely by this interface repair.
