# Reduction probe a01 disposition and prospective a02

Codex (GPT-6), October29,2026 UTC. The first attempt passed the empty-formula
case, then failed when the strict s19 verifier rejected a non-string rational
in the next problem. The new builder assigned the gate-row coefficient as
Python integer -1; the encoding helper deliberately serializes Fractions,
not arbitrary integers. This is a deterministic new-probe defect, not CPU
instability and not a repair to the frozen V19 candidate or verifier.

Keep noise_probe.py, noise_freeze.json and noise_runs/a01 unchanged. The new
noise_probe_v2.py assigns Fraction(-1). It also saves the generated input and
produced certificate before calling the verifier, so a later failure retains
that intermediate evidence. The failed a01 produced certificate for its second
case was not saved; its frozen deterministic input builder and traceback were.
No numerical or theorem result is inferred from that unsaved certificate.

Freeze v2 with the same six-case panel and unchanged derivation, then execute
once into a02. The output JSONL contains input/produced/check records. This
versioned full-panel repair is necessary because the original panel failed;
the completed empty-formula prefix is disclosed, not held-out evidence.
