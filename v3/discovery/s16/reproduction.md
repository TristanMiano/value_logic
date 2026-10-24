# s16 evidence and reproduction

Codex (GPT-6), October24,2026 UTC. Administration; zero research credit.

The [manifest](manifest.json) binds research notes, probe sources, outputs and
clock records. [verify_evidence.py](verify_evidence.py) checks execution hashes,
the original and repaired minimum-column sources, helper dependencies, exact
clock totals, all25 prior recurrence objects/bytes and the prior ledger prefix.
With `--index` it also checks that staged Git blobs equal working evidence.
These are integrity checks, not an independent mathematical review.

Two local Python environments were used. Rational probes used Python3.12.14
at `C:/Users/trist/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
Floating numerical probes used `C:/Python313/python.exe`, Python3.13.14,
NumPy2.2.5 and, where needed, SciPy1.15.3. Each JSON output records the actual
versions, source digest and measured runtime. Exact Fraction assertions are
finite checks; optimizer convergence and tolerance comparisons are exploratory.
In particular some local optimizer starts failed to converge while another
start supplied the reported comparison; inspect the stored flags.

Run read-only closing checks from the actual repository root:

```text
python -X utf8 v3/discovery/s16/verify_evidence.py
python -X utf8 tools/check_repo_paths.py
python -X utf8 tools/evidence_paths.py verify
python -X utf8 v3/checks/math_markdown.py
python -X utf8 -m verification
```

Reconciliation is idempotent but writes closing actuals and appends missing
ledger dispositions; it is not a research clock. The resident clock is closed.
Do not run start.py or mark.py merely to reproduce evidence. close_records.py
is the administrative construction script, not a general maintenance command;
do not rerun it over later edits. The final publication may include subsequent
format-preserving repairs and corrected scalar metadata described in failures.md.

To rerun a mathematical probe, use a separate checkout of the published commit,
copy its original output aside, inspect the script's output paths, then run the
named probe with its recorded Python environment. Some probes write JSON beside
their source, so running them in the evidence checkout would overwrite history.
Keep new stdout, stderr and outputs separately. The original failed scale run
and minimum-column reporting run retain their v0 sources and dispositions;
the corrected scale and minimum-column outputs are separate evidence.

The bounded checker can be invoked on the existing block_receipt.json input
with the output redirected to a NEW filename; block_probe.py checks its finite
valid and invalid cases. Source identity, truthful scalar/matrix brackets,
target basis and actual edit norm are premises of its receipt contract, not
facts that parsing a JSON input establishes.

No aggregate probe runtime is presented as a service speedup. Probe execution
already lies inside the observed research intervals and earns no extra credit.
Local full-suite limitations and exact-head remote CI belong in publication.md.
