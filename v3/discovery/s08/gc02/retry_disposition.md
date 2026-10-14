# n32 clique scan failure and fresh physical retry

Codex (GPT-6), DEVELOPMENT. The first scan process fails inside score() with
TypeError: a list_iterator is not subscriptable, where the unchanged source
support list is expected. This is consistent with the machine instability
reported by the author, but its cause is not proven. The exact failure log,
source, diagnostics and paid trace prefix remain in n32_clique_scan.

The retry uses the identical frozen service and source, with distinct request
prefix n32_clique_retry2 and output directory n32_clique_scan_retry2. It
replays all64 rows as **new physical acquisitions**. The original incomplete
attempt is not erased, declared free, or counted as a completed64-output
unit. Its known physical fee is tallied separately; incomplete computation,
native runtime and unassigned costs remain unknown. The design is exposed
development data, not a fresh confirmation attempt.
