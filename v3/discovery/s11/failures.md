# Execution failures and dispositions

Codex (GPT-6), s11 DEVELOPMENT. Causes are unknown unless established below.

The first exact compression prototype has SHA256
`e1120caf608f0741cd29d17683a8e307959f645c67c136e6d07b93b207090907`.
Its code is [potential_probe.py](potential_probe.py). No assertion or input was
changed during the following attempts:

1. Python 3.13, output pc01.json: failed during signed_flip_5 with a TypeError
   subtracting Fraction from a zip object in vector reduction. The exact failing
   model and four completed cases are retained in [pc01.failure.json](pc01.failure.json).
2. Same runtime/code/input, output pc01r.json: stopped with exit 1 after printing
   completed cases through random_12, without a traceback or final JSON. This
   attempt's output is retained in the chat tool record; no output file exists.
3. Same runtime/code/input, output pc01r2.json: TypeError inside the standard
   Fraction constructor during signed_flip_5. [Log](pc01r2.log) and
   [failure input](pc01r2.failure.json) retained.
4. Bundled Python 3.12.14, unchanged code/input, output pc01b.json: stopped with
   exit 1 after signed_flip_3, without traceback/final JSON. [Log](pc01b.log).

These are failed developmental runs, not successful complete probes or evidence
of theorem failure. Partial completed assertions remain scoped observations.
The reported unstable host motivates a bounded per-case runner as an explicit
execution amendment. It preserves the original evaluator, all 25 source cases,
seeds and assertions, and records each attempt separately. It is not described
as an unchanged full-run success. This recovery administration earns no research
credit. A later passing run would not establish the failure cause.

The explicit [per-case runner](case_run.py) subsequently completed all 25
declared cases on their first individual attempts under bundled Python 3.12.14.
[Summary](pc02/summary.json) and [attempt ledger](pc02/attempts.jsonl) retain
case indices, durations, exits and evaluator hash. This is success of the amended
execution, not retroactive success of any of the four failed full runs.
# Stopped-invoice LP reconstruction

The first `invoice_flow.py` source, SHA256
`b1abe608032930b6709a3ef6bb0ce336795599c7eafbcad681977593f49fdd5c`,
passes twelve small full-trajectory comparisons and a 24-coordinate compact
case. Case 13 (80 coordinates) fails the same exactness assertion in three
unchanged runs: `if02/c13a0.log`, `c13a1.log`, `c13a2.log`. HiGHS reports an
optimum, but denominator-limited rational reconstruction of its primal flow
does not satisfy all equalities. This is a reproducible certificate limitation,
not evidence of a stochastic hardware failure. No assertion or outcome was
changed to call the instance exact. Its repaired dual remains a candidate
upper certificate; `flow_failure.py` extracts the retained first log and checks
every arc with rational arithmetic, without rerunning the solver. Primal
attainment for that numerical instance remains unverified.

## Policy realization flow

`policy_flow.py` passed cases 0, 1 and 2 in `pf01`. The declared 31-coordinate
case failed all three attempts: two native exits -1073740791 with empty logs,
then a Python TypeError reporting a list_iterator at an assignment to the
locally created `moments` list. See `pf01/attempts.jsonl` and the three retained
logs. No source assertion or case changed. The cause is unknown; these are not
passing results or a falsification of the realization proof.

A separate Python 3.12 package preparation attempt also exited 1 while
installing SciPy/NumPy, without an explanatory traceback. It produced neither
importable target package. Runtime preparation and retries earn no research
credit. A bounded retry of that installation is authorized by the reported
unstable host; record any subsequent runtime change as an amended execution.

The package-install retry succeeded. Under Python 3.12.14 with target-directory
NumPy 2.2.6/SciPy 1.15.3, the unchanged case 3 completed in `pf02/c03a0.json`
on its first amended-runtime attempt. It still reached the declared iteration
cap and had a substantial optimization gap. Neither completion nor a changed
interpreter establishes what caused the earlier failures. `dl01` and `dl02`
use this same amended runtime. Local package files under `dist/s11py` are
untracked runtime dependencies, not scientific evidence copies.

## Conditional SAT-menu execution amendment

`cr02` completes cases 0--3, then cases 4 and 5 fail on all three unchanged
Python 3.13 attempts. The exit ledger retains access violations and stack-buffer
failures. Case 5 attempt 1 also reports `generator already executing` followed
by a directly checked SAT-witness assertion. No passing result or known hardware
cause is inferred. `cd01` cases 0--3 complete; its cases 4 and 5 fail three times
because their prerequisite JSON files do not exist. These dependent retries
were unnecessary; all logs remain evidence of what actually ran.

Prospective amendment after this exposure: keep all cases, selectors, native
solver, checks and original sources unchanged. Run only the two missing SAT
cases under bundled Python 3.12.14, with a newly installed Python-SAT 1.8.dev24
cp312 wheel and six 1.17.0 in ignored `dist/s11sat312`. Import that solver before
the original module adds its cp313 path. `cnf_select_312.py` records the runtime
and wheel-package hashes, delegates the unchanged case function and writes
separate `cr03` outputs. At most two unchanged retries remain the per-case
limit. Installation is excluded from research. Success would not establish the
cause of the earlier failures. No failed output is replaced.

If those inputs complete, `cnf_decision_312.py` changes only the input location
for cases 4--5, using an explicitly recorded in-memory version of the original
source. It records original and executed byte hashes and writes separate
`cd02` outputs under the existing Python 3.12 SciPy environment. All results
remain DEVELOPMENT; the already exposed four cases are not rerun.
