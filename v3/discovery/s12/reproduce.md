# Reproduce s12 without replacing evidence

Codex (GPT-6). All runs are same-model DEVELOPMENT screens. Python3.12.14 on
Windows was used through the bundled runtime; probes use the Python standard
library. Sources record seeds, scopes, arithmetic choices and dependencies.
The fixed outputs and their hashes are evidence, not an independent review.

Run from this checkout using a compatible Python interpreter. Select a new
output directory and redirect stdout/stderr there. Inspect each source before
execution: most write their named JSON output beside the source; for those,
copy the source and its declared local dependencies to an isolated replay
directory first. Do not rerun into s12 or overwrite a saved output. Copying
source bytes preserves their hash; changing a filename can affect imports.

The [manifest](manifest.json) binds the session's scientific sources, outputs,
notes and clock records. In addition, outputs with source_sha256, hashes or
dependency hashes bind their execution inputs. Read [failures](failures.md)
before interpreting COMPLETED as a positive mathematical finding. The two
potential screens deliberately return counterexamples; the early five-bit
probe reaches a cap. [prefix_complete_disposition.md](prefix_complete_disposition.md)
corrects only descriptive metadata, not an optimization result.

The principal probes cover permissions/maps/lineage, affine edits, hard prices,
cap-two recursions, variable/shared-coin protocols, quantized readout, noise,
reliability/calibration, source reachability, repair margins, task/joint adequacy
and interval/temporal updates. Their individual JSON files retain finite
counts and limitations. The full scoped service has no end-to-end probe.
Expensive panel reruns are unnecessary for checking a documentation handoff.

Clock reconstruction is administrative and idempotent:

```text
python v3/discovery/s12/reconcile.py
```

It checks matched boundaries and dispositions, recreates effective_actuals.json
and appends missing replacement-ledger rows only once. Never execute start.py,
mark.py or the resident clock's serve/init commands to reproduce historical
time. close_records.py is a guarded one-time reporting mutation, not a replay.

Repository gates, after staging intended changes, are:

```text
python -m verification
python v3/checks/math_markdown.py
python tools/check_repo_paths.py
python tools/evidence_paths.py verify
```

See [publication](publication.md) for actual commands, outcomes and remote head.
These checks verify repository integrity and finite software properties; they
do not promote the candidate or independently prove the new mathematical notes.
