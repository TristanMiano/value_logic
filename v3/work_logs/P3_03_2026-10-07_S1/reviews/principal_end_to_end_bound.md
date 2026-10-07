# End-to-end finite VM/source work bound

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Principal derivation and same-model internal read-only review. No new execution
or additional concurrent time credit.

The principal first proposed the safe epoch bound
`2 Σ max(1,b_i) + (m+1)(2^(k+1)-1)` for a fixed admitted query list,
fixed caller assumptions, no external updates, retained all-mode scheduling,
evidence capacity `|H0|+m <= 128`, and cell capacity at least `2^k`.
The bounded-reconstruction reviewer independently checked the current
`finite-cover-v2` paths and confirmed the assumptions and bound. Its review
also identified the sharper queue-entry count used in the final principal
note:

```math
B=2\sum_i\max(1,b_i)+(2^{k+1}-1)+m2^k.
```

## Load-bearing checks

- Production and deterministic replay each consume at most the horizon, or
  one transaction for a zero horizon. Acceptance happens in the final replay
  transaction. This counts used scheduled transactions, not elapsed CPU.
- Before an as-yet unaccepted job commits, at most `|H0|+m-1 <= 127`
  constraints are active. The fixed indexed receipt identity adds a distinct
  constraint. Caller assumptions cannot use the reserved `vm:` namespace.
- The frontier contains disjoint nonempty cubes. If any cube can split, its
  size is at least two, leaving fewer than `2^k` cubes. Thus the stated cap
  eliminates the only source requeue branch inside an unchanged epoch.
- Without withdrawal/coarsening, successful splitting creates at most the
  nodes of one depth-k binary tree. Initialization plus all child insertions
  add at most `2^(k+1)-1` agenda entries.
- Each of at most `m` receipt acceptances inserts at most `2^k` current cells
  into its replacement agenda. Discarded pending entries can only decrease
  later pop count. Every source transaction pops one entry.
- The persistent scheduler chooses available source or bounded-job work.
  Enough cumulative positive all-mode allowance therefore completes the
  finite workload. Call pauses do not change this operation bound.

Opaque queries need not resolve. Inconsistent conditional assumptions are
allowed and yield finite conflict after filtering. A successful separately
charged report is needed for exact numerical endpoints on a nonempty source;
its arithmetic may instead hit a declared limit. Parsing, checking node work,
dispatch scans, identity/serialization work, storage and host costs remain
separate from the heterogeneous transaction count. The guarantee covers
supported call boundaries, not arbitrary state mutation or process crashes
inside a transaction.

The reviewed current core SHA-256 is
`841df6c5223844d2131642adcbb136855e054aa8833036506bb32c91aaf8afe6`.
This direct code/queue argument strengthens the finite construction's stated
resource envelope; it is not a performance claim or an unrestricted proof
search bound.
