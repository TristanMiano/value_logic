# s18 failures and limits

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT.

The first cap-rank probe, [cap_rank_check.py](cap_rank_check.py), completed
its algebraic assertions but failed at JSON serialization with
`TypeError: Object of type BooleanTrue is not JSON serializable`.
Command: `C:\Python313\python.exe v3/discovery/s18/cap_rank_check.py`.
Exit1; no successful result file was written. Original SHA256:
`e0f9cdf7b40faf09254ed290439560151dd8b9edc090818a9852653282f940b1`.
This is a deterministic SymPy/Python type mismatch, not evidence of hardware
instability. Its script is preserved. The separately versioned
[repair](cap_rank_check_v2.py) converts check values to native bool before
serialization. Its [result](cap_rank_v2_result.json) records two passing
rational examples, source hash, Python/SymPy versions and32,567,400ns runtime.
That runtime is contained in the research interval, not added again.

A context-recovery read requested nonexistent `clock_segments.jsonl`;
the resident uses `segments.jsonl`. This administrative path error did not
alter the clock. Context and mixed-mode exclusions are explicit in
[dispositions.json](dispositions.json), preserving raw observations.

Primary-source access failures and unread scopes are in
[literature.md](literature.md). No failed access is counted as a completed
proof comparison, and no source's abstract is treated as its full theorem.
