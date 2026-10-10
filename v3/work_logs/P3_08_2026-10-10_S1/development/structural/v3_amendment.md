# Structural DEVELOPMENT v3 — current-warrant read and readout accounting

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.

The complete v1 and v2 runs remain preserved. Both completed every declared
mathematical comparison; v2 corrected unequal transport readout obligations.
The closure review identified two precise remaining improvements:

1. Transport's `max_serialized_object_bytes` metric tracked retained objects but
   omitted the terminal payload. Its byte charges and hard readout-size check
   were already correct. v3 includes that payload in the recorded maximum.
2. The old response's full-record mismatch was displayed before new transport,
   and only a current checked result was returned. v3 additionally performs an
   actual attempt to read the prior checked warrant, rejects that read on each
   changed scope, then proceeds through the same explicit transport/fresh-check
   path. Both methods receive the same guard and terminal status field.

No mathematical input, rank, action rule, solver, comparator, resource tariff,
budget allowance or acceptance bound changes. v3 receives a new source manifest
and fresh `run_v3/` directory. Its changed code-byte setup and guard costs are
charged; neither earlier invoice is rewritten. After source/hash, invoice,
scope-read rejection and equal-payload checks, optional verification stops.
This remains DEVELOPMENT, with zero concurrent principal time credit.
