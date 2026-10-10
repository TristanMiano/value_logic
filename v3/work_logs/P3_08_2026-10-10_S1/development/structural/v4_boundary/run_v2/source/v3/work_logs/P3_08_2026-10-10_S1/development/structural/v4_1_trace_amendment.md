# Structural DEVELOPMENT v4.1 — cold opcode-tracing initialization

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.

The first v4 boundary probe failed before any structural performance rerun.
Preserve its source, plan, helper and failure traceback in
`v4_boundary/run_v1`. Its worker source was SHA-256
`75533585c6815b63cb35ecf792a7da575abf42ed64e36a501786a65f353dba09`.
The measured fixed failure receipt cost 140 bytes and zero recorded opcodes
when it was the first tracing session in the process. A later fresh tracing
session recorded the literal function's two actual opcode events. The expected
142-unit assertion therefore correctly stopped the probe; this is not an
unchanged unexplained retry.

## Diagnosis and scope

The observed interpreter is CPython 3.12.14. The official Python 3.12
[`sys.settrace` documentation](https://docs.python.org/3.12/library/sys.html#sys.settrace)
states that opcode events require a frame's `f_trace_opcodes` flag to be enabled
before installing the trace. Setting it only in the later call-event callback
does not satisfy this initialization requirement. The linked primary
[CPython issue 114480](https://github.com/python/cpython/issues/114480) and
[issue 103615](https://github.com/python/cpython/issues/103615) discuss this
behavior. This explanation is consistent with the independent local cold-run
diagnostic. No source text is quoted here.

This was a preexisting measuring-apparatus defect: initial opcode events could
be omitted until a nested or later trace installation. The old mathematical
output comparisons remain recorded, but v1-v3 invoices cannot support the
unqualified claim that every initial worker opcode was charged. They are not
retroactively rewritten. New source-bound v4.1 invoices replace that accounting
claim for the published finite fixtures.

## Repair and prospective verification

Before installing tracing, `_meter_run` sets `f_trace_opcodes=True` on its own
excluded instrumentation frame. It restores the prior flag on exit, along with
the existing trace/profile state. This activates opcode events before any
worker code executes; it does not obtain free worker results or prime the same
function once for an unrecorded answer. Instrumentation is excluded under the
existing tariff. Meter admission is explicitly restricted to CPython 3.12.14;
other runtimes need their own prospective tariff validation.

Version the worker `p308-structural-v4.1` and the focused helper revision v2.
In a fresh process, before any metered worker call, observe a new caller and
new leaf function and compare all traced opcode offsets with their disassembly.
Then check the separately called literal function's first execution costs two
opcode units plus 140 bytes. Continue the previously planned source/input and
success-output budget-denial probes. Store this amended attempt in
`v4_boundary/run_v2`, preserving the failed first attempt. Only after these
checks pass run the nine matched cases and transport once in `run_v4_1`.

This remains DEVELOPMENT with zero concurrent principal time credit and no
final evaluation or freeze. It changes instrumentation initialization and the
explicit runtime admission boundary, not any structural input or decision rule.
