# Graph probe implementation amendment

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT only.

The original graph probe exited -1073741819 with no log. Its one unchanged
retry exited 1 with `TypeError: 'tuple_iterator' object is not callable` in a
nested generator expression. No result artifact or completed-unit record was
written. Both logs, exits and source hashes are preserved. No deterministic
cause has been established; the exception is not an acquisition-value result.
The unchanged retry allowance is exhausted. Do not rerun that probe.

Prospective repair: port the same mathematical recurrence, independent component
check, explicit Bellman comparison and prediction check to Node. A separate
Python input generator reproduces the **same original Python Random(64283)**
sequence, case counts, shapes and parameter draws, saving every input before
Node exposure. Scale rational data to safe integers; use a factor 2^n in small
cases to make all fair-split Bellman divisions integral. Large cases have no
Bellman enumeration and use the smaller exact scale. Assert safe integers.
No seed, output-count or scientific-method selection in response to results.

This is a versioned implementation amendment following an unresolved execution
failure, not a second unchanged retry or an independent confirmation. Results
from the amended source remain developmental and cannot erase either failure.
The source-generation and amended output have their own immutable paths and
source bindings so the implementation change can be reconstructed.
