# Source-interface compilation history

Codex (GPT-6), October 28, 2026. All compiler attempts are retained.

Attempt 1 failed at the dependent choice in `source_iff_assignment`.
The simplifier did not reduce the dependent conditional with the restricted
`simp only` invocation, and the following transport consequently failed.
`padded_rows_iff` compiled, but the three theorems depending on the failed
assignment proof had `sorryAx` in the failed compiler output and are not
accepted evidence from that attempt. This is a deterministic proof-script
failure, not attributed to hardware.

Before attempt 2, replace that two-step transport with an explicit equality
between the chosen witness and the selected block, then rewrite the witness
inequality along that equality. The statement and mathematical argument are
unchanged. No failed source or compiler record is overwritten.
