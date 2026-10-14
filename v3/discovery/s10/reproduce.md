# Reproduce and inspect s10

Codex (GPT-6), October14,2026. Research is closed; reconstruction adds no new
acquisitions or historical research time.

Start with [findings](findings.md), [checkpoint](checkpoint.md),
[run inventory](run_inventory.json), [failure inventory](failures.json),
[exact actuals](effective_actuals.json) and [F01](forecast_final.md).
Root scripts are development working versions. Each executed experiment's
design binds its own copied modules and declarations. Restore those exact files
at the original import paths in a separate short checkout before replaying an
older experiment; do not substitute a later root module with the same name.

Fresh acquisitions use exclusive output directories. Never rerun a driver into
an existing evidence directory or overwrite failed logs. A new run needs a new
prospective record and separate output location. Read-only checkers reconstruct
stored receipts and outputs; their diagnostic units are separate from service
invoices. Full repository verification is `python -m verification`.

Node.js runs the `.cjs` finite kernels and stream checkers; Python runs exact
clock reconciliation, rational analyses and native comparison. No dependency
installation is required for the basic research checkers. up50's independent
native check used Python3.13.14, python-sat1.8.dev24 and six1.17.0 in a temporary
isolated target; its native/runtime tariffs remain unknown. Install that optional
dependency separately if repeating the native comparison, preserving new logs.

Useful read-only entry points include check_scalar.cjs, check_reserve.cjs,
check_learning.cjs, check_witness.cjs, check_regions.cjs and check_budget.cjs.
They currently write their checked summary paths, so run them in an isolated
copy to preserve original diagnostics. patch01 preserves gzip source/proof
objects; validate decompressed bytes and original source bindings, not just the
compressed container. dep01/dep02/dep03 retain exact primal/dual probability
certificates; three_score_checked.json binds the versioned source snapshots in
ts01 before the later correlated-learning elaboration.

The ds01 binding anomaly is preserved in ds01/bindings_manifest.json. One filename
does not match its canonical body digest, while the body has a valid internal
seal and also exists under its correct name. Follow the explicit mapping; do not
silently rename the historical reference or discard either object. Its cause is
unproven. Failed checker prefixes, the empty br01 check log with unknown status,
wrong archive-member extraction, and all eight up50 baseline cap bills remain
visible. An unchanged retry after an unexplained host failure is authorized by
the user, but does not erase the failed attempt or establish a hardware cause.

`python -B v3/discovery/s10/reconcile.py` recomputes effective closed actuals and
checks the exact floor. Its ledger correction append is idempotent. The clock
itself must never be resumed: a future session needs a fresh resident runtime.
The scripts update_progress.cjs and close_live.py are one-time administrative
updates with guards; do not rerun them against the current live table.
