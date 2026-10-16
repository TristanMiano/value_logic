# Reproduce s11 without overwriting evidence

Codex (GPT-6). All scientific versions and their failed outputs are retained.
Use a separate output directory; run_probe.ps1 refuses existing attempts.
Do not rerun completed probes merely to earn research credit. All commands
below are administrative reproduction guidance, not a new acquisition event.

The first environment was Python 3.13. Native/interpreter failures prompted an
explicit move for affected work to bundled Python 3.12.14, NumPy 2.2.6 and
SciPy 1.15.3 in ignored dist/s11py. Native SAT extensions use Python-SAT
1.8.dev24 and six 1.17.0 in ignored dist/s11sat312 for the two repaired-runtime
cases. Those local paths are conveniences, not portable scientific inputs.
Install the recorded versions in a compatible isolated runtime when needed.

From the s11 directory, a typical finite probe command is:

```powershell
./run_probe.ps1 -Script offpath_probe.py -OutDir replay_op01 -First 0 -Last 1 -Python 'PATH_TO_PYTHON'
```

For SciPy scripts set PYTHONPATH to the compatible package location before
running. Inspect each source's argument parser and declaration. The runner
uses --case and --out and allows at most three total unchanged attempts.
Original outputs include exact fractions, source hashes, seeds, counts and
attempt ledgers. A successful retry does not establish the cause of a failure.

| Source / declaration | Original outputs | Reconstruction scope |
| --- | --- | --- |
| [Direct solver](direct_lp.py), direct_screen.py, regrid_direct.py | dl01, dl02, dl01_grid.json | Rational primal/dual regret enclosures; same-case regridding is not new acquisition. |
| [Certified repair](repair_lp.py), repair_core.py, safe_lp_plan.md | rp01 | Seven declared cases; separate full-world small comparison and compact chain paths. |
| [CNF menu](cnf_repair.py), cnf_select.py, cnf_decision.py | cr01, cr02, cd01 | Six inherited s10 sources; direct incremental SAT versus reuse; preserve all failed missing cases. |
| cnf_select_312.py, cnf_decision_312.py | cr03, cd02 | Only cases 4--5 under amended runtime/input path; original source bytes and in-memory amendment hashes recorded. |
| cnf_summary.py | cnf_results.json | Read-only aggregation of existing outputs; no SAT or optimizer rerun. |
| local_service.py, free_service.py, path_service.py | ls01, fs01, ps01 | Four exposed streams, fixed seeds/tuning and strong ordinary fee controls; ps01 has one extra mechanical case. |
| free_probe.py, baseline_probe.py, model_probe.py | ff01, bp01, ms01 | Exact estimator identities plus a separately scoped floating combined learner screen. |
| invoice_probe.py, support_probe.py | ip01, sp01 | Finite polynomial/rank checks and exact indistinguishable-law witnesses; not population data acquisition. |
| offpath_probe.py, star_probe.py | op01, st01 | Two finite geometry cases and one exact fourteen-policy primal/dual witness. |

Other original per-case folders and their sources remain available for the
earlier exploratory screens. Read [failures.md](failures.md) before selecting a
replay. In particular, invoice_flow.py case 13 has a deterministic primal
certificate failure; flow_failure.py checks an upper certificate only.

Clock reconstruction from the repository root is:

```text
python v3/discovery/s11/reconcile.py
```

It preserves the first dead runtime's raw active record, includes only closed
matched intervals, applies each disposition once and checks the fresh four-hour
floor. Never run start.py or recover_clock.py to reproduce historical time.
The closing manifest binds scientific code, outputs, logs and clock records;
source identity is not independent scientific confirmation.
