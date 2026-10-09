# P3-B implementation and retained-evidence reconstruction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent implementation reviewer.
October 9, 2026 UTC. Same-model, targeted, nonblind review. Agent time receives
**zero principal research credit**.

**Verdict: PASS at the P3-B implementation/evidence subreview scope.** The
current restricted modules have usable input, state, dependency and resource
contracts; the accepted downstream implementation premises examined here have
no unresolved current defect. This is evidence for the principal's technical
gate decision, not a separate decision on P3-N01 or phase completion.

The pass supports proceeding to design an integrated candidate when P3-08 is
separately selected. **A single end-to-end reasoner joining P3-03's uncertainty
state, P3-05's counterfactual reuse, P3-06's forecast updates and P3-07's paid
selection has not been implemented or validated.** Local readiness and that
remaining integration obligation must remain separate.

## 1. Review basis and limits

The review uses base commit
`c7e2967d18475bda54a327864601c245c8a29062`, the
[phase-three protocol](../../../../RESEARCH_PROTOCOL.md),
[P3-B forecast](../../forecast.json), current source, and the P3-03–07 task
audits and retained final evidence. [manifest.json](manifest.json) records the
review command, environment and all current P3-03–07 Python source hashes.
[check_results.json](check_results.json) records 389 source/evidence inputs,
508 passing first-pass checks and two preserved literal-location failures.
The separate [final disposition](final_check_result.json) resolves those two
historical bindings and records the subreview PASS.

The only new scientific-module execution was three selector admission calls
using one already acquired P3-07 profile. No query population, rollout, solver,
original experiment or whole development suite was rerun. Most checks concern
exact retained bytes and whether a historical result is being attributed to
the correct current or historical implementation. Their count is not an
independent proof of all possible executions. The substantive reconstruction
also inspects the receiving definitions and control flow described below.

## 2. The actual dependency and interface contract

| Layer | Current executable service and binding | Required boundary for downstream use |
|---|---|---|
| P3-03 | `03_bounded_logic.py`, `finite-cover-v2`, and `03_task_certificate.py` represent bounded VM claims and a finite Boolean outer cover. Full source/loss records and epochs determine current applicability. | At most 12 atoms and 4,096 cells; admitted rational/input/VM limits apply. Heterogeneous work counters and transaction allowances are not a uniform physical CPU/RAM or acquisition tariff. An applicability check does not authenticate arbitrary supplied numeric report fields. |
| P3-04 | `04_counterfactual_repair.py`, reconstructed v1, gives finite hard/soft ranked selection and the declared paired-support semantics. Its current S2 sources match both replacement-run closures. | This is new replacement evidence, not recovered S1 code. Conditioning, override, program replacement and counterpossible support retain different input interpretations. Dependency graphs, ranks, exceptions and rule policy are supplied. |
| P3-05 | `05_counterfactual_transport.py` imports the exact P3-04 request implementation. The portfolio v3 receiver is shared by dependency v2 and counterpossible-bridge v2. Its source closure matches the latest full runs and the shared-front-end run. | The receiver handles at most ten bits and one rank tier. Old/current records, a feasible incumbent, Boolean maps, positive scaling, common units and the fixed receiving difference are checked. It does not infer dependencies or compile arbitrary native phase-two proofs. |
| P3-06 | The scalar learner is v2.1, the modular evidence harness is v3, capital comparison is v1.1 and price replay is v2. All six modules listed in the final evidence audit match their current hashes. | The scalar report is not P3-03's joint Boolean state. Version-matched checked labels, an immutable issued tape, selected feature/weight duties and explicit delayed-feedback ownership are needed. Fixed-tape transport does not identify a changed learner's trajectory. |
| P3-07 | Controller v3, modular adapter v1.1 and driver v3 are jointly bound. Whole-audit v2 also binds its own generator/driver source. Analytic-profile v2 and acquisition-planner v1.1 have their distinct closures. | The main selector chooses among six complete policies for a fresh cohort under its law, initial state and price contract. The arithmetic adapter's exact residue cache is not a P3-05 transport theorem. The known-prior acquisition planner is a separate supplied-model service. |

These are genuinely different interfaces, rather than one common object
called a value. The P3-04→P3-05 bridge is an executable import and compilation
bridge. The P3-06→P3-07 four-action connection imports the potential argument
mathematically and has its own source and evidence; no runtime import of the
P3-06 learner is falsely omitted from that manifest. The P3-07 dependency-cost
diagnostic does execute the actual P3-05 compiler/portfolio closure, and its
saved v2 hashes match those unchanged earlier sources.

The Python modules use shared nominal module identities to compose their
trusted local types. The reviewed closure is a coherent source set in a fresh
process. Mixing unrelated archived modules in one prepopulated import registry
is not an authenticated source-loading service supplied by this work. Future
integration must preserve the selected closure and its input/state contract.

## 3. Independent reconstruction of load-bearing boundaries

### 3.1 A retained comparison does not silently become a different decision

I inspected [PortfolioCache](../../../../checks/05_portfolio_transport.py)
`_prepare`, `verify` and `admit_portfolio`, together with the
[program receiver](../../../../checks/05_dependency_frontend.py) and
[counterpossible receiver](../../../../checks/05_counterpossible_bridge.py).

The current proof first binds the independently supplied full receiving
record. `_prepare` checks an actual feasible incumbent, then computes its
rank cutoff. Every actual minimizer lies below or at that cutoff. A split
must verify both children, and a rank exclusion requires strict inequality;
an equal-rank case cannot be discarded as a tie. A reuse leaf checks the
mapped old premises and old cutoff before checking the loss correction.

For an admitted old bound, the receiving identity is

```math
D_{\mathrm{new}}(x)
=\alpha D_{\mathrm{old}}(\psi(x))+
  \bigl(D_{\mathrm{new}}(x)-\alpha D_{\mathrm{old}}(\psi(x))\bigr),
\qquad \alpha>0.
```

The code forms that correction from the single `current.difference`. It
checks its upper bound against `bound - alpha * old.bound`. Consequently a
branch may choose a different old proof but cannot choose a different action
comparison. Full sublevel coverage and the feasible incumbent give the
nonempty all-minimizer claim. Admission stores a new domain only after
verification, preventing circular use of a not-yet-admitted result.

The program receiver recompiles both exact programs and the coefficient
table. The counterpossible receiver recompiles the quoted antecedent,
baseline, exceptions, frame and background through P3-04's paired-support
rules before accepting the numerical proof. The current shared import name
is the same in both wrappers. The retained shared-front-end v3 record binds
these exact wrappers; the earlier nominal-type failure stays historical.

P3-03 withdrawal is consistent with this treatment of old evidence. Its
`withdraw` removes dependent constraints, restarts affected jobs, restores
the full cover and advances the source epoch. Old current applicability
does not survive withdrawal merely because an old numerical interval still
looks plausible. The earlier conditional theorem remains a historical
statement about its old source.

### 3.2 Incomplete source admission cannot choose an unchecked policy

The narrow execution in [check_contract.py](check_contract.py) reconstructs
the saved 1,024-row profile as the current immutable type and independently
rebuilds its expected scope from all three current source hashes.

| New boundary call | Result |
|---|---|
| Swap the first two generic profile names; assessment cap 321 | Fixed `fallback`; no profile identity; `profile_scope_validated` false; conditional lower gain 0; 321 units charged. |
| Keep the acquired profile but change only the expected generator hash; cap 321 | The same unprofiled fallback, with all-in gain `-321/1000` at the supplied prices. |
| Keep that changed generator scope; cap 20,000 | Rejects with `Exact current catalogue, feature ranges and whole scope required.` |

The original profile record is unchanged after these calls. This directly
checks the conjunction that matters at the gate: a saved profile cannot
acquire current source validity through an incomplete check, and low-budget
fallback does not read the first name of an unvalidated catalogue. The v2
implementation review's `guess0` counterexample is a real retained failure
of its reviewed source; it is not a defect of the current v3 path.

### 3.3 Cleanup and output are bounded parts of the complete policy

I also reconstructed the cancellation reserve from
[run_policy](../../../../checks/07_paid_reasoning.py) and the
[adapter](../../../../checks/07_computation_adapter.py). A valid maximum-length
source label gives `key_words <= 24`. Cancellation pays eight handle-check
units, at most 24 identity-comparison units and one release unit, hence at
most 33 units. The complete policy reserves 65 cleanup units before opening
a job and one separate terminal-output unit. At the full 1,024-unit policy
cap, optional work therefore receives at most 958 units.

Denied operations retain their earlier paid cost. Pending jobs pass through
the public cancel path; successful acquisition funds the returned answer and
release together before publishing it. Tiny budgets cannot start a job with
no cleanup reserve. This is a concrete bounded primitive-accounting argument,
not a CPU-time claim. The adapter's `complete` convenience helper is explicitly
a producer/checker smoke interface; its arbitrary timeout behavior must not
be promoted to the complete policy's cleanup contract.

## 4. Nonvacuous predictions and the interpretation of development evidence

The modules expose operationally different outcomes: unresolved versus
checked answers, feasible incumbent versus unresolved feasibility, accepted
versus stale transported comparison, issued versus admitted feedback, and
fallback versus paid continuation. The retained final runs contain cases
where those outcomes differ. The results are not satisfied solely by returning
an empty set or declining every computation.

P3-07's [current selections](../../../P3_07_2026-10-09_S1/development/run_v3/selections.json)
include positive continuation certificates and the storage-expensive change
from fallback at earlier checkpoints to full computation at 1,024 samples.
The [whole-procedure result](../../../P3_07_2026-10-09_S1/development/whole_procedure_run_v2/result.json)
records a positive lower expected gain of `1211017049/4096000` against its
fallback comparator, while charging its acquisition and assessment. Its
outer procurement is a further bill, and the charged exact solver is cheaper.
Thus implementable decision changes and a conditional positive comparison
are supported; broad practical superiority is not.

The [P3-05 resource comparison](../../../P3_05_2026-10-08_S3/reviews/scientific_self_review.md)
retains the stronger ordinary ADD result, which was faster in all six saved
families. The current [P3-06 acceptance audit](../../../P3_06_2026-10-09_S1/readiness_audit.md)
likewise retains exact-arithmetic and ordinary-aggregator advantages on its
cheap domain. The four-action paid full-feedback example and actual
dependency construction/search diagnostic also retain negative total-cost
findings. Local executable readiness does not depend on reinterpreting these
comparisons as wins.

**IID and confidence scope.** The current
[P3-07 main derivation](../../../../derivations/07_paid_reasoning.md), section 6,
explicitly says a pseudorandom seed does not demonstrate IID sampling.
Section 4 requires independent profile/future requests, the stated law and
initial state; a selected deterministic query or an outcome-selected stopping
time is outside that immediate conclusion. The driver docstring,
`Scope.sampler_contract`, returned selector boundary and
[whole-audit closure](../../../P3_07_2026-10-09_S1/development/whole_procedure_run_v2/closure.json)
all preserve the same distinction. The four-action driver separately requires
independent fair bits for its sampling theorem. I found no current claim in
the examined sources that treats a passing fixed-seed replay as empirical
validation of nominal confidence coverage.

## 5. Evidence versions, original notation and exact preservation

The initial script deliberately kept literal hash failures visible. Two
needed interpretation of their already recorded history:

1. The P3-03 receipt-repair plan's manifest names its pre-format hash. The
   [formatting receipt](../../../P3_03_2026-10-07_S1/rendering/final_math_repair.json)
   records the later one-span code protection. Removing only those two
   protection backticks in memory reproduces the exact original SHA-256
   `edd73ab13640bbd8f067732902eb93f2f429f5ce43b8ce705b463a6ffc1c3894`;
   the current bytes match the recorded after-hash. No plan was rewritten.
2. The P3-06 recovery inventory records its entry ledger, not a promise that
   later append operations never occur. Its exact 120,635-byte prefix has
   SHA-256 `8bfb7af2a22551ee18e35b144661dd2e1bf27713027336c4bda6d6ab17a8df4c`.
   The prefix also equals the full ledger at the recorded accounting-base
   commit. No ledger or historical hash was changed.

The [resolution script](resolve_historical_bindings.py) reads the original
check output and checks only these bindings; it does not rerun the selector
or any experiment. The original `BLOCKED` literal-check result remains
unchanged, with its SHA-256 bound by the final disposition.

For P3-07, the selected whole-audit and analytic-profile review manifests
refer to exact originals retained as `.md.original.txt` sidecars. Both original
hashes match; their current display hashes are separately recorded in the
check output. The other selected review artifacts match directly. These
formatting differences do not invalidate current source or result closures.

P3-06's documented missing complete historical CF-7 draft remains missing.
Its preserved section, current argument and current code are not relabelled
as that full original file. P3-04's lost S1 source/run history and P3-05's
failed or superseded attempts similarly remain attached to their actual
versions. Neither the current-source check nor this verdict repairs history
by overwriting a manifest.

Git comparison to the stated base found no changes to prior `v2/`, current
P3-03–07 scientific source, derivations, literature, or prior task work logs.
All 389 first-pass input files were unchanged during that check. All writes
by this reviewer are confined to this new review directory. No status,
ledger, plan, publication or recurrence action was performed.

## 6. Implication for the gate

The evidence supports **local implementation readiness**, with the supplied
semantics, trusted local evidence/state, source versions, finite input caps
and declared resource models as premises. It does not establish a common
cost measure across all prior modules, arbitrary external report
authentication, universal logical uncertainty, uniquely determined
counterpossible semantics, useful selective-feedback learning, or an
integrated model-retention/computation-purchase policy.

The next implementation design must explicitly choose those connections and
compare the combined procedure with the strongest ordinary controls. That is
the missing end-to-end integration obligation, rather than an unresolved
error in the restricted accepted modules examined here. P3-N01 remains
unsupported; this subreview neither executes P3-08 nor selects recurrence.
