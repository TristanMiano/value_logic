# F15 independent audit of saved retention outputs

Contributor: **delegated ChatGPT (GPT-6 Astra Pro), F15 saved-output audit**.
This is F15 post-exposure numerical verification, not F16, a fresh proof, or a
priority assessment. Delegated work overlapped the principal session and must
not be added to the principal's engaged-time ledger.

## Result

The independent rational audit passed **203,311 checks with zero numerical
mismatches** across all **160 cases, 1,920 method/access rows, and 11,520 scalar
intervals**. The run used only Python's standard library and the saved JSON
files. It did not import any experiment module, run a generator, prepare or
evaluate a model, acquire a new source observation, or edit a frozen file.

The detailed record is [`retention_output_audit.json`](retention_output_audit.json).
The independent executable is [`retention_output_audit.py`](retention_output_audit.py).

| Verified saved outcome | Count |
|---|---:|
| Exact scalar answers | 8,624 |
| Admitted approximate scalar answers | 616 |
| Refused scalar answers | 2,280 |
| Certified orders | 1,220 |
| Certified fallback decisions | 368 |
| Refusals followed by actual fallback execution | 332 |
| Rows performing adaptive repair | 412 |
| Rows using the prescribed two-current-mean repair | 60 |

Every scalar interval contains the same-case adaptive `fresh` point mean.
Every admitted midpoint and recorded absolute error agrees exactly with that
reference. The largest admitted numerical error is **35/1488**, approximately
0.02352 declared cost units, below the frozen 1/20 tolerance. Every useful
decision satisfies the frozen realized-regret tolerance. The largest realized
regret **including refusals** is **7/5**; refusal-to-fallback remains a distinct
outcome and receives no useful-decision credit.

## Independent calculation

For each world, the audit computes the cost of an ordered program directly as

\[
C_{(i_1,\ldots,i_k)}(w)
=\sum_{t=1}^{k} c_{i_t}\prod_{j<t}w_{i_j}
+ L\prod_{j=1}^{k}w_{i_j}.
\]

This is a closed prefix-product formula rather than a call to the frozen path
interpreter. It handles the two-attempt program edit as well as every declared
price and penalty change.

For each of the 16 seeds, six saved old means, the two saved large-price means
for orders `(0,2,1)` and `(0,1,2)`, and normalization uniquely determine the
eight-world initial law. Exact forward elimination and back substitution
give rank 8, a normalized nonnegative law, and agreement with the other four
large-price means. No generator seed is used to recover discarded information.
These reconstructed laws independently reproduce all **144** non-drift case
profiles from the prefix formula, including unchanged-law withdrawal cases.

The audit then rebuilds the protocol-declared information fibers from those
saved measurements. It enumerates nonnegative supports and solves the full
original equality system on each support, without using the experiment's RREF,
matrix inverses, dual certificates, or `Fiber` implementation. It verifies
the exact interval endpoints, equation ranks, and vertex counts. For each
vertex, it computes each action's cost minus the cheapest action under that
same vertex, and only then takes the maximum over vertices. This verifies the
same-law worst regret, selection tie breaks, certification/refusal, executed
fallback, and realized scoring.

The native comparison's exact upper bound must equal the corresponding
candidate cost interval's upper endpoint minus fallback cost. The audit checks
that identity, the candidate order and role, the recorded semantic-validity
flag, and the numerical condition for receipt or insufficiency. It also checks
the frozen useful-derivation flag against those recorded quantities. Native
proof objects are not present in these result rows, so this is an independent
check of numerical targets and receipt dispositions, not a second kernel proof
check.

Adaptive acquisition is checked against the independently reconstructed
pre-repair refusals. The two-scalar path is permitted only for the declared
stable one-price selective-summary repair; every other required repair is
checked as a full eight-field source response. Exact scalar charges, API calls,
path-execution counts, and every reported acquisition-price/horizon arithmetic
entry agree with that policy.

## Authority loss and missing drift information

After withdrawal or drift, every no-reacquisition method has the whole current
probability simplex as its admissible source, including methods that retained
the full old table. Those simplex bounds and coherent regrets are reconstructed
directly; old numerical facts are not silently reused as current authority.

The 16 drift laws are not identified by their six saved point means. The audit
does **not** infer them. It can nevertheless verify every drift interval
against the saved current reference profile, exactly reconstruct the
no-reacquisition simplex bounds and decisions, and compute every repaired
point-query cost and regret from the six recorded current means plus fallback.
The scope is the recorded query profile, not recovery of an unrecorded source.

## Aggregate anomaly and audit attempts

The first audit invocation stopped during initial JSON loading, before doing
the numerical checks: the original
`F15_v1_run1/evaluation_attempt_1/retention_results.json` was observed to contain
**zero bytes**, while its sidecar retained the original nonempty digest. The
evaluation-complete marker was already present. The mechanism of truncation
is undetermined. This contributor issued no command writing to that file;
the audit's only access was `Path.read_bytes()` followed by `json.loads()`.

The aborted audit version and failure are preserved as
[`retention_output_audit_attempt1.py`](retention_output_audit_attempt1.py) and
[`retention_output_audit_attempt1.json`](retention_output_audit_attempt1.json).
The optional audit reader was then changed to read the **160 original
individually hash-checked case files**, in the frozen seed/variant order. The
original empty aggregate was preserved. No experimental stage was retried.

Canonical JSON assembly of those intact units has SHA256

`0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691`,

which exactly matches the original aggregate sidecar. The audit checks that
equality without writing an aggregate. Its result explicitly records the
original aggregate's failed integrity check separately from the successful
per-unit numerical audit; it does not label the original aggregate intact.

The second audit invocation completed in **1.627919 wall seconds**, with
**1.626041 process seconds**. These are script resource measurements, not
additional engaged research minutes. It used CPython 3.12.14 and the prescribed
single-thread environment, with no NumPy or PyTorch dependency.

## Reproduction

From the repository root, use a new optional-audit output filename to preserve
the existing record:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python v2/work_logs/F15_2026-10-04_S1/retention_output_audit.py \
  --out v2/work_logs/F15_2026-10-04_S1/retention_output_audit_rerun.json
```

The script requires the completed-evaluation marker, hash-checks each original
case and the completion record, and records the input and script hashes. Its
output writer is exclusive, so it will not overwrite an earlier audit record.

## Interpretation limits

This supports exact numerical consistency of the saved finite challenge and
its stated admission and repair rules. The fiber reconstruction assumes the
protocol-declared retained measurements; it does not independently retest
payload isolation or the transient source interface. It does not establish a
new theorem, causal neural use, unique utility representation, worldwide
priority, or Gate C/D passage. Those remain separate questions from this
successful finite numerical audit.
