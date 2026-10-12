# Reconstruct or extend the s07 discovery work

Prepared by **ChatGPT (GPT-6 Astra Pro)** as handoff administration on
October 12, 2026. Preparing this guide makes no new acquisition and earns
**zero research credit**. The commands below are instructions, not a receipt
that they were executed during this preparation. All s07 scientific outputs
remain DEVELOPMENT evidence.

Run commands from the **actual checkout root**, at a revision containing s07.
Keep the committed `s05`, `s06` and `s07` relative layout: imports, source
admission and some saved-input paths are resolved from the modules' locations.
For the scientific interpretation, use [bundle theory](bundle_theory.md),
[the verification review](verification_review.md), [the witness review](witness_review.md),
[population findings](population_findings.md), and the corresponding source
records. [The forecast record](forecast_design.md) and
[its final assessment](forecast_final.md) define F01; a successful reconstruction alone
does not raise its probability or establish a complete-cost saving.

## 1. Environments and fresh outputs

The [s06 research requirements](../s06/research_requirements.txt) supply the
scientific import chain used by s07:

```sh
python -m pip install -r v3/discovery/s06/research_requirements.txt
```

Those pins are `python-sat==1.8.dev24`, `highspy==1.11.0`, `numpy==2.3.5`,
`scipy==1.17.0` and `six==1.17.0`. The
[s06 environment record](../s06/reproduce.md) documents Python 3.12.14;
[the s07 robust-witness receipt](robust_witness_results.json) records HiGHS
1.11.0. Use an appropriate Python 3.12 research environment for these
entrypoints. Package pins do not establish identical binaries, solver tie
choices or timings on a different machine. The pure
[progress extractor](progress_report.py) uses only the Python standard library;
other receipt checkers import the wider scientific dependency chain even when
they make no solver call.

The repository-wide verification environment is separate: current CI uses
Python **3.13**, NumPy **2.2.5**, Matplotlib **3.10.8**, and Torch **2.8.0 CPU**.
Its installation commands are in section 6. Do not replace the research
environment's NumPy pin merely to run the repository suite.

For each selected reconstruction or probe, create a fresh short output
directory. This command fails if that directory already exists:

```sh
python -c "from pathlib import Path; Path('repro_s07').mkdir(exist_ok=False)"
```

Every command below supplies a new output filename. Some entrypoints otherwise
default to an existing scientific result path; shell redirection can overwrite
a file even when a Python entrypoint refuses to. Use a new directory for a
repeat. Preserve failed outputs and their actual disposition. New execution on
these exposed development sources is reproduction, not fresh confirmation.

## 2. Reconstruct saved evidence without new purchases

These commands read saved records and may perform substantial new checking,
enumeration, compilation and accounting work. They do not invoke new s07
native search, complete proof-provider solves or cost-provider audits.
For a quick byte-identity check of the handoff and retained prior sources, run
`python v3/discovery/s07/integrity.py`; its [inventory](manifest.json) is separate
from proof validity and the acquisition histories.

```sh
python v3/discovery/s07/progress_report.py v3/discovery/s07/a01/results.json v3/discovery/s07/a02/results.json v3/discovery/s07/a03/results.json > repro_s07/progress.json
python v3/discovery/s07/trace_check.py repro_s07/trace_check.json v3/discovery/s07/a01/results.json v3/discovery/s07/a02/results.json v3/discovery/s07/a03/results.json
python v3/discovery/s07/witness_check.py repro_s07/witness_check.json v3/discovery/s07/witness_service_results.json
python v3/discovery/s07/population_check.py repro_s07/population_check.json v3/discovery/s07/population_results.json v3/discovery/s07/population_v2_results.json
```

| Entrypoint | Reconstructed evidence and limits |
|---|---|
| `progress_report.py RESULTS...` | Source-bound output/purchase/plan counts, complete quotation meter deltas, invoice components and symbolic economic comparisons. Checks archived controller hashes; it is not an independent raw-proof checker. Version v3 distinguishes source-proven absence of control quotation payloads from unknown older candidate payloads. |
| `trace_check.py OUTPUT RESULTS...` | Re-admits the original raw bank, checks recorded audits, positive models, complete/native negative receipts and final action bounds in order. Enumerates finite feasible models only for diagnostic regret checks; these models and hidden outcomes are not supplied to a controller. |
| `witness_check.py OUTPUT RESULTS` | Reconstructs both expanded-menu schedules, original-source witnesses, raw proofs, cache updates and named tariffs from saved responses. It constructs no HiGHS model. Saved native statuses and timings remain recorded observations; missing full native primal arrays are not retrospectively reconstructed. |
| `population_check.py OUTPUT RESULTS...` | Rechecks the common raw logical proof, saved cut observations and CDF support certificates. Its deterministic-cohort prefix alternative uses already paid observations and is a replay, not an independently executed arm with measured saved purchases. |

The trace and witness checkers also read the original
[`s06/joint_source.json`](../s06/joint_source.json) and s05 admission chain.
The witness checker validates the current frozen s07 controller/dependency
bytes against its acquisition receipt. A changed implementation requires the
corresponding preserved source context; do not bypass a hash failure or change
the saved receipt to fit new code. Giving a checker a new output path does not
redirect these fixed input dependencies to a newly executed acquisition.

## 3. Finite development checks and analytical replays

These also make **zero new acquisition calls**, but they calculate new finite
examples or analytical results rather than merely extract existing totals.
Select the construction relevant to the change; none is a mandatory full
research rerun for a documentation update.

```sh
python v3/discovery/s07/repair_interface_check.py repro_s07/repair_interface.json
python v3/discovery/s07/compiled_quotes_check.py repro_s07/compiled_quotes.json
python v3/discovery/s07/row_margin_check.py repro_s07/row_margins.json
python v3/discovery/s07/ambiguity_probe.py repro_s07/ambiguity.json
python v3/discovery/s07/discrete_ambiguity_probe.py repro_s07/discrete_ambiguity.json
python v3/discovery/s07/quotient_plan.py repro_s07/quotient_plan.json
python v3/discovery/s07/quotient_closed_form.py repro_s07/quotient_closed_form.json
python v3/discovery/s07/random_order.py repro_s07/random_order.json
```

| Group | Scope |
|---|---|
| Repair interface | Hand-constructed raw proof and witnesses, all declared tiny price/refinement cases, admission rejection cases and optional-method fallback. Finite source/price coverage does not establish economic superiority. |
| Compiled quotations and row margins | Exact finite comparisons against direct calculations, cache reuse and rejection boundaries; quotations retain their own work costs. |
| Ambiguity probes | Reconstruct saved states from `witness_service_results.json` and an opposing family using the already acquired `bundle_example_results.json` proof. They do not execute a controller that skips the retrospectively identified work. |
| Quotient planning and closed form | Conditional public finite planning constructions checked against enumerated or dynamic-programming alternatives. They acquire no hidden source outcome and do not turn an unpriced planning component into an established full-service saving. |
| Random-order tariff | Exact hypergeometric, stopping-distribution and literal finite comparisons for an internally randomized policy on a fixed unknown source. No source prior or acquisition call. |

The supporting modules `repair_interface.py`, `lattice_quotes.py`,
`compiled_quotes.py`, `row_margins.py`, `robust_witness.py`,
`ambiguity_floor.py` and `discrete_ambiguity.py` expose callable components;
they are not standalone acquisition commands. Do not invoke `clock_source.py`
to reproduce scientific outputs: it belongs to the observed session clock.

## 4. Commands that acquire new evidence

The following are available for a subsequent authorized scientific execution.
They were **not run while preparing this guide**. Choose the relevant command
and retain its new source, receipts, failures and complete invoice. A name
ending in `check` is not a guarantee of zero acquisition.

```sh
python v3/discovery/s07/bundle_example.py repro_s07/bundle_example.json
python v3/discovery/s07/s29_affine.py repro_s07/s29_affine.json
python v3/discovery/s07/signed_geometry.py repro_s07/signed_geometry.json
python v3/discovery/s07/robust_witness_check.py repro_s07/robust_witness.json
python v3/discovery/s07/witness_service.py repro_s07/witness_service.json
python v3/discovery/s07/population_service.py repro_s07/population_v2.json
```

| Entrypoint | New work in the declared construction |
|---|---|
| `bundle_example.py` | Two complete finite logical calls, including the initial lower proof, and one cost audit; tests a complementary audit/proof bundle. |
| `s29_affine.py` | One complete finite negative-proof call; source-geometry transport is then checked without cost audits. The ordinary full-tree comparator reaches the same bound. |
| `signed_geometry.py` | Three new complete negative-proof calls on exactly defined transformed sources and one coordinate audit. The original-source signed inequalities are checked before the final gate. |
| `robust_witness_check.py` | Five capped HiGHS MIP proposals and one cost audit on two constructed sources, plus raw-proof/model checks. This is an acquisition probe. |
| `witness_service.py` | Two actual schedules on the saved sixteen-request source, with each arm's own robust-witness proposals, audits, complete calls and retained state. Its expanded purchase menu is a separate comparison scope from a01–a03. |
| `population_service.py` | The v2 fixed synthetic population/sample construction, actual complete logical calls and cost-cut observations for three policies. The preserved `population_service_v1.py` and `population_v1_manifest.json` retain the earlier implementation and its disposition. |

For a new **v3 bundle execution with all four configured policies**, the direct
CLI is:

```sh
python v3/discovery/s07/bundle_service.py v3/discovery/s06/joint_source.json repro_s07/bundle_v3_four_policies.json 1
```

This executes `bundle`, `audit_first`, `logic_first` and `native_logic` at depth
1. The original a03 acquisition executed **only `bundle`** and compared with
the saved a01 controls. The next section reproduces the exact recorded policy
selection instead of implying that those controls were acquired again in a03.
New timings and runtime identifiers are expected to differ. Evaluate checked
outputs, receipts, source identity and the full cost vector; do not require
byte-identical timestamps or silently omit unresolved attempts.

## 5. Re-execute an exact frozen bundle version

| Saved attempt | Frozen version | Actual policy selection | Record |
|---|---|---|---|
| a01 | `s07-complete-bundle-v1` | Four policies listed above | [Manifest](a01/manifest.json), [results](a01/results.json) |
| a02 | `s07-complete-bundle-v2` | `bundle` only; a01 controls retained | [Manifest](a02/manifest.json), [results](a02/results.json) |
| a03 | `s07-complete-bundle-v3` | `bundle` only; a01 controls retained | [Manifest](a03/manifest.json), [results](a03/results.json) |

The archived source files retain their **original** relative import layout.
In particular, their `HERE.parent / 's06'` expression is valid at the original
`s07` path, not inside `s07/a01`, `s07/a02` or `s07/a03`. Do not execute an
archived script in place or edit it to make its hash match a new path.

After checking out the published revision containing s07, create a disposable
worktree. The example chooses **a03**; choose `a01` or `a02` instead when that
is the intended historical version. These commands restore working source
files only in that separate checkout and write a new acquisition result.

```sh
git worktree add --detach ../vl_s07_repro HEAD
cd ../vl_s07_repro
python - a03 <<'PY'
import hashlib
import json
from pathlib import Path
import sys

root = Path.cwd()
s07 = root / 'v3/discovery/s07'
attempt = sys.argv[1]
if attempt not in {'a01', 'a02', 'a03'}:
    raise ValueError('Choose one preserved bundle attempt')
manifest = json.loads((s07 / attempt / 'manifest.json').read_text())
saved = json.loads((s07 / attempt / 'results.json').read_text())
for item in manifest['files']:
    data = (s07 / item['snapshot']).read_bytes()
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        raise ValueError('Changed frozen snapshot: ' + item['snapshot'])
    (root / item['path']).write_bytes(data)
source = s07.parent / 's06/joint_source.json'
if hashlib.sha256(source.read_bytes()).hexdigest() != saved['source_sha256']:
    raise ValueError('Changed fixed source')
for name, expected in saved['dependencies'].items():
    path = s07 / name
    if not path.is_file():
        path = s07.parent / 's06' / name
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError('Changed executed dependency: ' + name)
output_dir = root / 'repro_s07'
output_dir.mkdir(exist_ok=False)
sys.path.insert(0, str(s07))
import bundle_service
bundle_service.execute(source, output_dir / (attempt + '_new.json'),
    policies=tuple(saved['configuration']['policies']),
    depth=saved['configuration']['depth'])
PY
```

Use a fresh Python process and disposable checkout for each selected historical
version. The wrapper preserves the original manifest and acquisition records;
the provider still performs the raw logical-bank and complete-code admission.
It does not grant the new run the earlier acquisition cost or research time.
Do not run the latest expanded-witness checker against a restored v1/v2 working
controller: that checker intentionally binds the executed v3 dependency bytes.

## 6. Repository publication gates

The [October 12 maintenance report](../../../docs/checks_20261012.md) and
[machine receipt](../../../docs/checks_20261012.json) describe **earlier executed
checks**, not passes for the new s07 revision. Read the
[archive-link guide](../../../docs/archive_links.md) and
[mathematical-Markdown guide](../../../docs/math_markdown.md) before resolving
publication findings. Current workflows are
[verification](../../../.github/workflows/verify.yml),
[portability](../../../.github/workflows/portability.yml) and
[mathematical Markdown](../../../.github/workflows/math-markdown.yml).

In a separate **Python 3.13 verification environment**, install CI's pins:

```sh
python -m pip install numpy==2.2.5 matplotlib==3.10.8
python -m pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu
```

Provide CMake and a working native C++ build toolchain before the full run if
both native-kernel tests are to execute there. The previous maintenance used
CMake 4.4.4. The actual test code skips those two tests when `cmake` is absent;
report skips and complete those tests after providing the dependency, rather
than describing a skipped case as a pass.

Stage the intended publication files before the path and whitespace checks;
the path checker inspects the **Git index**. Run these gates from the actual
checkout root and retain current command results:

```sh
python -m verification
python v3/checks/math_markdown.py --receipt repro_s07/math_publish.json
python tools/check_repo_paths.py --checkout-root 'C:\Users\trist\projects\value_logic'
python tools/evidence_paths.py verify
python -m unittest verification.test_repo_paths verification.test_evidence_paths verification.test_relocated_links
git diff --cached --check
```

The path gate covers every tracked path **and ancestor attribute lookup**,
with a maximum of 200 relative UTF-16 code units; the explicit Windows checkout
root also exercises the full-path bound. Evidence verification checks relocated
historical object bytes. The math receipt filename must be fresh: the checker
refuses to overwrite an existing receipt. Plain
`python v3/checks/math_markdown.py` is the equivalent CI gate without a saved
receipt. No acquisition program in section 4 or 5 is required merely to publish
documentation or accounting changes.

Repository-wide links are included in `python -m verification`. For a focused
link report or a change to archival/view machinery, use the corresponding
commands below; these are targeted diagnostics/regressions, not substitutes
for the full suite:

```sh
python -m verification.check_links
python -m unittest verification.test_links verification.test_archive_origins verification.test_math_markdown verification.test_math_views
python verification/math_views.py verify
```

If the full run skipped the native cases, the exact completion command is:

```sh
python -m unittest verification.test_experiment_repair.NativeKernelTests -v
```

Repair ordinary active Markdown directly when appropriate. Scientifically
bound old sources require preserved bytes and an independently bound portable
view; changing a manifest hash alone cannot admit altered scientific content.
The link checker uses explicit source-context provenance, not blanket archive
exemptions. Registered portable views are mechanically derived and checked;
`python verification/math_views.py generate` is a reconstruction operation for
missing admitted views, not a routine command to overwrite a conflicting view.

Passing these repository gates establishes their declared software,
formatting, link and preservation checks. It supplies neither a new promotion
forecast nor a complete-cost economic result. Record the new revision's actual
gate results and remote CI status separately from the historical maintenance
receipt and from the closed principal research clock.
