# P3-10-A1 principal lineage reader: source-only review

Signed by **ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction**, 2026-10-11. This is an external P3-10 saved-result observer review with **zero principal clock credit**. No reader or reporting observer was executed, and no final scientific input/result payload was read for this review. The sealed amendment manifest was read as provenance metadata only.

## Reviewed bindings

- `amended_lineage_reader.py`: SHA-256 `d3e5d1ff4a5fc4c03fea4d07d1f205c763d1cf52476c63a3c6c6c27cb55c6f8e`.
- Current A1-adapted `retrospective_report_observer.py`: SHA-256 `de5b9a46c15eba52bc6e3476425199d0034c179c23de60e3cf02d4f89a67610c`.
- Sealed A1 `continue.py`: SHA-256 `0e6fa551fe78561026972e5ba7e83e810927b8778c65bfa8c88e607c85b49cca`.
- Announced A1 manifest: SHA-256 `36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359`.

## Findings

**The private/public computation boundary is correct in the reviewed source.** The constructor requires original input completion, absence of original public completion/private stages, and all three amended completion markers before reading unit payloads. Its result-file operations compute byte hashes; JSON parsing is confined to lifecycle and reference metadata. It validates the fixed original schedule against the pinned original manifest. The reporter requests only broker/mirror public records while constructing bounds. The optional numeric observer data and evaluation records are parsed only after `public_bounds.json` and its containing directory have been fsynced. Reading private result bytes for digest validation is distinct from parsing truth or scores; the recorded zero private score payloads parsed by the barrier is accurate.

**Finding A1-L1: pin the sealed amendment trust root.** The reader compares the current A1 manifest hash with its adjacent amendment binding, while pinning only the original freeze/protocol values externally. Thus a jointly changed A1 manifest and binding can satisfy the A1 identity comparison. Add the now-announced fixed A1 manifest hash as a required constant (or an equally external immutable expected argument). This is an independent identity-check gap, not evidence that the sealed manifest or continuation has changed.

**Finding A1-L2: compare the remaining-unit metadata directly to the frozen conformance slice.** The reader's amended public stage takes unit metadata from `manifest['remaining_public_units']`; composition later checks the original 60 IDs but does not independently equate each amended unit's remaining fields to the frozen unit. Require exact list equality with `[u for u in schedule['units'] if u['arm']=='conformance']`, and verify the reused-ID list against the complementary 440 units. The sealed continuation driver already enforces both equalities. Adding them to the independent reader states and verifies the unchanged conformance obligation at that boundary, instead of relying on the producer for it.

The flat amended binding and exact full row reference handling agree with the producer schema. The separation of original 440 records, amended 60 records, original 12 inputs, and 500 amended score identities is correctly expressed. The original failure and unknown unsealed prefix cost are retained. The reader establishes byte identity and completed lineage; it does not itself establish scientific correctness, full paid-prefix accounting, prospective timing from a status string alone, or any economic advantage.

## Own observer follow-through

The same root-pinning improvement is preserved as the unexecuted `observer_v4.py`, following unexecuted v1–v3. It pins all three announced root digests and retains v3's existing exact remaining/reused roster checks. Mathematical checks are unchanged. Execution remains pending explicit principal release after all amended stages complete.
