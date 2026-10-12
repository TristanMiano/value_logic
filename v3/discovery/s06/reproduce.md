# Reconstruct or extend the s06 repair service

Prepared by **ChatGPT (GPT-6 Astra Pro)** as handoff administration after the
s06 principal clock closed at **60.07154650425 effective research minutes**.
Preparing this guide made no new solver, proof-provider, LP or cost-audit calls
and adds no research credit. The artifacts remain DEVELOPMENT evidence.

This guide gives entrypoints into the executed mechanisms and their admission
chains. Start with [the source-anchor result](source_anchor.md) and its
[focused mathematical qualifications](source_anchor_review.md) for the next
constructive direction. Read [native findings](native_findings.md),
[RUP findings](rup_findings.md), [joint findings](joint_findings.md),
[complete-service findings](complete_findings.md) and
[hull findings](hull_findings.md) for the corresponding scope and invoices.

## Environment and preservation

Run commands from the **actual repository root**, with the `s05` and `s06`
directories in their committed relative locations. The modules resolve their
scientific dependencies from `__file__`; copying a single executable elsewhere
does not reproduce that source context. Install into an appropriate Python
environment, using the newly collected
[full requirements](research_requirements.txt):

```sh
python -m pip install -r v3/discovery/s06/research_requirements.txt
```

The observed interpreter was Python 3.12.14. The full pins include
`python-sat==1.8.dev24`, `highspy==1.11.0`, `numpy==2.3.5`,
`scipy==1.17.0` and `six==1.17.0`. SciPy supports the additional
`mix_repair.py` construction. The earlier
[native requirements](native_requirements.txt) are frozen evidence and have
not been changed. The RUP bridge constructs its own bounded CNF and does not
require `pypblib`. Glucose3 and MiniSat22 are provided by the installed PySAT
build; there is no external DRAT checker invocation.

Package versions identify the requested software release. They do not promise
identical binaries, backend tie choices, process IDs or timings on another
platform. Exact executed source/binary hashes and capabilities are retained
in [the native stream](native_stream_results.json) and
[the proof capability record](proof_cap_note.md). Admit receipts against their
recorded sources; a matching checksum alone does not check a proof.

Create a new, short output directory before a reconstruction. The following
commands deliberately fail if this directory already exists:

```sh
python -c "from pathlib import Path; Path('repro_s06').mkdir(exist_ok=False)"
```

Always supply a fresh output path. Several entrypoints otherwise default to
the historical result filename. Keep the raw archives, failed versions,
dependency hashes, identities, observations and invoices intact. A new output
on these exposed development duties is a reproduction, not fresh validation.

## Zero-acquisition entrypoints

These commands **read and check existing paid evidence**. They incur new
replay/admission/compilation work, recorded as such, while making zero new
native search, bounded proof-provider, LP or cost-observation calls:

```sh
python v3/discovery/s06/rup_replay.py v3/discovery/s06/rup_stream_results.json repro_s06/rup_replay.json
python v3/discovery/s06/hull_replay.py repro_s06/hull_replay.json
python v3/discovery/s06/source_anchor_probe.py repro_s06/source_anchor.json
```

| Entrypoint | What it reconstructs | Principal admitted inputs |
|---|---|---|
| `rup_replay.run(path, output)` | Both saved stream arms: original-source witnesses, raw RUP exports, newly derived cuts, paid mask projections, resident-state links and all 160 action gates. | Explicit trace path plus the original s05 raw/cache chain and frozen s06 bridge/stream code. |
| `hull_replay.run(output)` | The four joint-v2 histories at their recorded evidence prefixes, comparing the existing certificate with stitched hull certificates. It does not change the purchases. | `joint_source.json`, `joint_v2_results.json`, original raw admission, checked observations and branching receipts. |
| `source_anchor_probe.run(output)` | Each logical arm's own final cut bank, saved rational LP multipliers, scalar anchors and the same 14 historical audit-first observations at prefixes 0, 4, 8, 12 and 14. | `rup_stream_results.json`, `dual_hull_results.json`, `joint_v2_results.json`, `joint_source.json`, original raw admission. |

The hull and scalar-anchor entrypoints read these **saved files beside the
original module**. Supplying a new output does not redirect their inputs to a
newly generated stream. The scalar-anchor query is a retrospective combination
of final logical banks with earlier cost observations, not a newly executed
controller that acquired both. It reconstructs rational multipliers without
rerunning their LP proposals and does not enumerate a new objective-mask
projection or uncertainty hull.

### Replaying checkers with fixed output paths

`joint_check.main()` and `complete_check.execute()` intentionally refuse to
overwrite their archived outputs. They do not take an output argument. The
following wrapper imports the **original modules**, copies only the input
bytes each checker expects into separate fresh directories, redirects each
checker's local `HERE`, and invokes its original full checking function.
All source, receipt and dependency checks remain enabled. Modules resolving
s05 evidence and code-admission dependencies continue to use the original
checkout.

Run this as a **separate Python process**. The complete checker installs
process-local refusal sentinels on acquisition methods; it is deliberately
last, and the process then exits.

```sh
python - <<'PY'
import importlib
from pathlib import Path
import shutil
import sys
import tempfile

source_dir = (Path.cwd() / 'v3/discovery/s06').resolve()
output_root = (Path.cwd() / 'repro_s06').resolve()
if not source_dir.is_dir() or not output_root.is_dir():
    raise ValueError('Run from the checkout root after creating repro_s06')
sys.path.insert(0, str(source_dir))

jobs = [
    ('joint_check', 'main', 'joint_check_results.json', [
        'joint_v2_results.json', 'joint_source.json',
        'joint_repair_v2.py', 'joint_repair.py',
        'native_repair.py', 'native_stream.py', 'joint_check.py',
    ]),
    ('complete_check', 'execute', 'complete_check_results.json', [
        'joint_source.json', 'complete_service_results.json',
        'complete_service.py',
    ]),
]
for module_name, function_name, result_name, input_names in jobs:
    checker = importlib.import_module(module_name)
    fresh_dir = Path(tempfile.mkdtemp(prefix=module_name + '_', dir=output_root))
    for name in input_names:
        shutil.copy2(source_dir / name, fresh_dir / name)
    original_here = checker.HERE
    try:
        checker.HERE = fresh_dir
        getattr(checker, function_name)()
    finally:
        checker.HERE = original_here
    print(fresh_dir / result_name)
PY
```

This is zero acquisition, not zero work. `joint_check` re-admits the initial
raw bank and rechecks the four arms' observation chronology, new witnesses,
raw branching proofs and request gates. `complete_check` additionally
re-admits the finite procedure's code contract, reconstructs all recorded
audits and completed calls, and prevents an accidental new acquisition.
The copied bytes support each original checker; they are not an independent
new validation population or a substitute trust root. Preserve any failed
reconstruction and diagnose its mismatch before claiming admission.

## Entrypoints that make new paid work

The following are **new executions**, listed for the next authorized research
increment. They were not run while preparing this guide. Choose a useful
entrypoint instead of rerunning the entire list. The fresh paths preserve
the archived evidence:

```sh
python v3/discovery/s06/native_stream.py repro_s06/native_stream.json
python v3/discovery/s06/rup_stream.py repro_s06/rup_stream.json
python v3/discovery/s06/joint_repair_v2.py v3/discovery/s06/joint_source.json repro_s06/joint_v2.json
python v3/discovery/s06/complete_service.py v3/discovery/s06/joint_source.json repro_s06/complete_service.json
python v3/discovery/s06/vertex_probe.py repro_s06/vertex.json
python v3/discovery/s06/dual_hull_probe.py repro_s06/dual_hull.json
```

| Entrypoint | New acquisition/computation | Interpretation |
|---|---|---|
| `native_stream.main(output)` | Persistent native IHS/MaxSAT work and separately paid finite branching proof calls. | Two arms on the same exposed 80 requests, retaining each arm's own paid state. |
| `rup_stream.main(output)` | Persistent native IHS/MaxSAT work, fresh proof-enabled Glucose3 bounded calls, strict proof checking and Boolean projection. | The same duty, with the supported RUP bridge replacing the finite branching bridge. |
| `joint_repair_v2.execute(input, output)` | Actual simulated source audits, native IHS and finite branching proof purchases, paid acquisition quotations and cost/certificate updates. | Four explicit controllers on the committed eight-row finite cohort. The current implementation uses the base branching adapter, not `native_rup`. |
| `complete_service.execute(input, output)` | Actual simulated cost audits and complete finite branching calls, including retained code admission and operation-cap accounting. | A finite completion contract enabling a full service; no native SAT/IHS or LP call. |
| `vertex_probe.run(output)` | Two fresh Glucose3 proof calls plus exact finite construction and replay. | A transparent tiny logical example and public one-row planning menu; no actual new cohort audit. |
| `dual_hull_probe.run(output)` | New continuous HiGHS LP proposals on independently re-admitted saved cuts. | The archived run made 126 LP proposals. No new SAT/IHS, proof or cost-audit call; this is retrospective representation work on final banks. |

Names ending in `check` are not necessarily zero acquisition.
`native_check.py NEW_OUTPUT` combines historical receipt checking with two
fresh cap probes: the zero-round probe performs no solve, while the
zero-proof-budget probe performs native work and records an unresolved proof
attempt. `rup_checks_v2.py NEW_OUTPUT` includes four fresh Glucose3 calls.
`cut_dual_probe.py NEW_OUTPUT` makes new LP proposals (105 in the archived
run), despite reusing already acquired logical cuts. Keep those calls separate
from the zero-acquisition replays above.

## Callable interfaces and admission map

Both native adapters are safe to import without executing a fixture. In a
long-lived consumer, retain the engine for the same structural logical source:

```python
from native_repair import PersistentIHS
# Or: from native_rup import PersistentIHS

engine = PersistentIHS(instance_with_identity)
try:
    response = engine.purchase(integer_weights, integer_budget,
                               limits=spending_caps, exact=False)
    # Admit/check the returned evidence before changing the certificate bank.
finally:
    engine.close()
```

Use nonnegative integral objectives for this bounded-call interface. The
response separates checked feasible witnesses, native guidance, checked lower
receipts, unresolved outcomes, each work invoice and timings. Preserve
`UNRESOLVED` and no-progress results. A native optimum status or raw core does
not itself enter the independent lower bank. The native stream translates a
requested repair/replacement tolerance into a budget duty using its existing
checked bounds; the returned action must still pass the checked service gate.

| Component | Retained state / usable receipt | Required admission and limits |
|---|---|---|
| Original s05 bank via `native_stream.admit_existing_cache()` | Checked witness profiles and reusable lower-proof masks. | Rechecks original raw witnesses and branching proofs, source/objective identities and the compact cache. The 8,037-byte cache is not self-authenticating. This adapter uses its pointwise mask projection; it does not consume the optional region cells. |
| `native_repair.PersistentIHS` | One MiniSat22 oracle with ordinary learned clauses; one HiGHS core model, direct objective-cost changes and prior hitting-set solution. | Check feasible models against the original formula. The optional MiniSat warm-start mode remains disabled after the preserved failure. Native core/model reuse is real; retention of a HiGHS MIP search tree is not claimed. Fresh finite branching calls supply separately checked negative receipts. |
| `rup_bridge_v2` and `native_rup` | Source-bound raw Glucose3 export, newly checked integral cut, and separately compiled reusable mask supports. | Rebuild the exact hard/violation/budget CNF, strictly check every RUP step, derive `q·z >= b+1`, then pay to project admitted cuts. Constructor tracing starts before clauses are appended. An empty export may need a proposed empty clause, which must itself pass RUP. This is a strict RUP subset, not a general RAT/DRAT checker. Projection currently caps the soft-feature count at 16. |
| Joint v2 cost state | Compatible modes per paid source row; exact supports and compiled action/proof templates. | `joint_source.json` commits the finite source. Public modes are available; `hidden_modes` belong to the observation provider. Controllers may use only actual audits. A completed-run checker can verify saved observations against that commitment without supplying free observations to a controller. No population law is inferred. |
| Complete service via `contract_guard` | Admitted finite search procedure, prospective operation quotation and checked witness or branching proof. | Code hashes and operation guard support the complete-call premise. Do not substitute a capped native call for this premise merely because its backend often finishes. |
| `vertex_repair` / `cohort_hull` | Scalar objective anchors from independently valid lower receipts, checked fixed actions, finite hull generators. | All anchors refer to the same feasible logical source. The true optimum is concave in its objective. Hull size caps are explicit; an incomplete generator set is unresolved, not a certificate for omitted regions. |
| `cut_dual` / `source_anchor` | Rational multipliers over freshly admitted cuts; scalar anchors at full-cohort mode objectives; rowwise transport through surviving source modes. | Raw saved multipliers are re-evaluated exactly against admitted cuts. **The clamped `point_lower` evaluator is warranted only for nonnegative weights.** Source-anchor transport uses concavity of the true optimum; the clamped dual lower function need not be concave. See [the binding review](source_anchor_review.md). |

The RUP receipt is initially an objective-specific cut. Repricing it uses a
paid mask projection or a separately constructed rational dual certificate.
It does not export the leaf masks of a branching proof. Likewise, a dual LP
optimum label is only guidance for choosing multipliers: the reusable lower
comes from exact reconstruction of the rational certificate. Source transport
then needs valid scalar anchor values, not a globally concave surrogate lower
function. These distinctions are the portable scientific interfaces.

## Costs and expected differences

Preserve distinct columns for historical acquisition, current admission and
replay, newly acquired evidence, operation tariffs, native calls and measured
CPU/wall time. For `native_rup`, the composite adapter invoice includes the
inherited base adapter work **plus** its cut-projection work; reporting only
the base part drops a real cost. The full decomposition is in
[RUP findings](rup_findings.md).

The recorded common raw/cache admission is 92,969 named units, separate from
the retained 77,646-unit historical acquisition. Replays may also charge
current raw receipt reads, checking, compilation and evaluation. A new
consumer must establish its own admission chain. Counts and times from an
earlier run do not pay for that work, and native CPU seconds have no supplied
conversion into the software operation tariff or an external audit price.
Serialization, allocation, storage and native memory have the limitations
recorded in each result; there is no established robust total-cost advantage.

Keep output comparison semantic: checked actions, regret bounds, admitted
receipts, source identity, unresolved attempts and the full cost vector.
Fresh timestamps, runtime object IDs and measured time are expected to differ.
The next controller construction should integrate source-anchor logical
quotations with actual cost-audit alternatives under an explicit completion
or no-progress contract. Reusing this evidence does not supply free weights,
an unknown source law or a calibrated proof-production price.
