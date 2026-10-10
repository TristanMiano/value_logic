# Authoritative scope clarification for STRUCTURAL-VM-v1 at v4.1

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Additive disposition after the principal's independent diff and reserve review.

**The measured computation primitive is a worker `opcode` trace event, not
every bytecode word or every interpreter operation.** One such event costs one
unit; each worker `c_call` profile event costs one additional bounded native-call
unit. The existing explicit source-admission, input, retention and terminal-byte
charges are added to those event charges. The same definition applies to both
matched implementations and all retained v4.1 invoices.

This statement is authoritative where the source docstring or earlier notes say
“every executed Python opcode.” That older wording is preserved as history but
is too broad. The implementation has always used the event callbacks as its
operational counter; this clarification changes no code, invoice or comparison.
It does not silently add frame-entry charges or claim a physical runtime bound.

In the audited CPython 3.12.14 run, the first-call probe's expected offsets
exclude `RESUME`, which performs interpreter tracing/debugging/optimization
bookkeeping before the observed worker body. `CACHE` positions are interpreter
data attached to other instructions, not additional worker instructions. Other
frame/bootstrap bookkeeping, interpreter specialization, GC, measurement hooks,
and operating-system costs remain outside this abstract unit model. Inline
arithmetic, equality, hashing and container work performed within a charged
event is the declared bounded native primitive under the finite operand/object
caps; it is not claimed to take one physical instruction.

The official Python 3.12 references are
[`sys.settrace`](https://docs.python.org/3.12/library/sys.html#sys.settrace),
[`RESUME`](https://docs.python.org/3.12/library/dis.html#opcode-RESUME), and
[`CACHE`](https://docs.python.org/3.12/library/dis.html#opcode-CACHE).
These document the tracing initialization requirement and distinguish the
interpreter bookkeeping/data just described. The empirical event offsets and
exact runtime are preserved in `v4_boundary/run_v2/checks.json` and `summary.json`.

No additional per-frame RESUME tariff is needed for the currently authorized
abstract event comparison: frame/bootstrap bookkeeping is explicitly outside
its resource unit, as is other interpreter machinery. A future claim about
every interpreter operation, actual CPU time, or another Python release would
require a separately declared and validated tariff. The present claim is
complete billing of the declared worker events and byte obligations for the
nine exact finite fixtures, including admitted failure prefixes.

The worker source remains `p308-structural-v4.1`, SHA-256
`84da8203ef7292623183212f7daf38c0a9e83bb6390ffdd0b0667c174975e026`.
The fixed failure receipt has two observed worker opcode events and 140 bytes,
costing 142 units within its protected 1,024-unit tranche. No rerun accompanies
this scope clarification, and all old evidence is preserved.
