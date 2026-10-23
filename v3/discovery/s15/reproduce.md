# Reproduce s15 without replacing evidence

Codex (GPT-6). Same-model DEVELOPMENT. [Environment](environment.json)
records the runtimes and base commit. Scientific probes use bundled Python
3.12.14 standard-library arithmetic or Python 3.13.14/SciPy where specified.
No held-out application, independent confirmation or new audit-stream run occurred.

Inspect each source before replay. Scripts write beside themselves and many
refuse an existing output. Copy the source and all referenced dependencies to
a short isolated directory, then use new stdout/stderr paths. Never replay into
s15 or replace its evidence. Source hashes and the closing manifest bind bytes;
they do not turn development probes into mathematical confirmation.

Useful small exact replays include forecast_probe.py (abstract rank laws and
an unsafe-start counterexample), feature_probe.py (finite-field correction and
anchor ambiguity), private_scope_probe.py (polynomial scope and retirement),
path_probe.py (rational value profiles), degree_probe.py (Hamming degrees),
stopping_probe.py (small symmetric stopping) and selective_probe.py (finite
confidence processes). Norm/root/capacity floating probes are numerical screens,
not outward certificates. LP discovery scripts need SciPy; their raw candidates
are not exact until the explicit rational check passes.

Preserve zero_channel and weight_channel rounding failures. zero_repair.py
uses the saved raw solution and constructs an exact rational certificate;
symmetric_probe.py checks the separate explicit stronger weight rule. The
summary_probe.json label about no exact decoder was too broad; the corrected
scope is in randomized_summary.md/zero_summary.md. A recorded zero elapsed_ns
for range_anytime_probe is retained, never used to infer independent runtime.

Administrative checks from the checkout root:

```text
python v3/discovery/s15/reconcile.py
python v3/discovery/s15/verify_evidence.py
python -m verification
python v3/checks/math_markdown.py
python tools/check_repo_paths.py
python tools/evidence_paths.py verify
```

Stage intended changes before the index path check. Reconciliation is idempotent
and appends missing replacement rows once. close_records.py is a guarded
one-time reporting mutation, not a replay. Do not restart a clock to reconstruct
historical time. See publication.md for actual local and CI outcomes.
