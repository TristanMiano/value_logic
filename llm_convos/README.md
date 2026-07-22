# LLM Conversation and Audit Manifest

This directory stores source conversations and external audits that influenced the project. They are provenance artifacts and idea sources, not authoritative evidence. Mathematical, empirical, and literature claims extracted from them are independently adjudicated in [`../notes/claim_ledger.md`](../notes/claim_ledger.md).

| File | Producer/context | Project role |
|---|---|---|
| [`chatgpt.txt`](chatgpt.txt) | Earlier ChatGPT conversation supplied by the project author | Source of initial adequacy, tolerance, representation, and nested-model proposals. |
| [`claude.txt`](claude.txt) | Earlier Claude/Fable conversation supplied by the project author | Source of agent-indexed licensing, closure, retention, atlas, and open-endedness proposals. Several strong claims were later narrowed or falsified. |
| [`claude_audit_2026-07-11.md`](claude_audit_2026-07-11.md) | Claude Fable 5 external audit requested by the project author; audit target commit recorded inside the file | Independent critique of Tasks 0–11A. Its findings are adjudicated in [`../notes/checkpoints/A1_external_audit_response.md`](../notes/checkpoints/A1_external_audit_response.md), not accepted automatically. |
| [`claude_audit_2026-07-12.md`](claude_audit_2026-07-12.md) | Claude Fable 5 external audit requested by the project author; audit target commit `a26ccdf` | Independent pre-Checkpoint-B critique of Tasks 11B–14A and the repaired earlier corpus. Its findings are independently adjudicated in [`../notes/checkpoints/B_core_metatheory.md`](../notes/checkpoints/B_core_metatheory.md). |
| [`claude_audit_2026-07-14.md`](claude_audit_2026-07-14.md) | Claude Fable 5 external audit requested by the project author; audit target commit `b05aee1` | Independent pre-Checkpoint-C critique of the repaired formal core and neural blueprint. Its findings are adjudicated in [`../notes/checkpoints/C_neural_blueprint.md`](../notes/checkpoints/C_neural_blueprint.md). |
| [`claude_audit_2026-07-17.md`](claude_audit_2026-07-17.md) | Claude Fable 5 external audit requested by the project author; audit target commit `93e3ce8` | Independent pre-Checkpoint-C1 critique of the frozen experiment and its public reproducibility. Its findings are adjudicated in [`../notes/checkpoints/C1_empirical_adjudication.md`](../notes/checkpoints/C1_empirical_adjudication.md). |
| [`claude_audit_2026-07-21.md`](claude_audit_2026-07-21.md) | Claude Fable 5 external audit requested by the project author; audit target commit `59ae3cc` | Independent pre-Checkpoint-D critique of Tasks 22–25, the policy/value bridge, and publication readiness. Its findings are adjudicated in [`../notes/checkpoints/D_predraft.md`](../notes/checkpoints/D_predraft.md). |

Future incoming artifacts should use a model-and-date filename and state the producer, date, audited revision or prompt context, and intended review status.
