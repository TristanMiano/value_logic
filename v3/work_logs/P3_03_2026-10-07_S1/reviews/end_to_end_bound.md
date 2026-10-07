# End-to-end finite VM work bound

Contributor: ChatGPT (GPT-6 Astra Pro), principal record of the same-model
bounded-reconstruction review and independent source inspection, 2026-10-07.
Read-only argument review; no execution or additional concurrent time credit.

The current core is `finite-cover-v2`, SHA-256
`841df6c5223844d2131642adcbb136855e054aa8833036506bb32c91aaf8afe6`.
For a successfully admitted fixed list of k queries, m bounded jobs with
horizons b_i, fixed initial caller constraints H0, no external updates, retained
all-mode scheduling, sufficient supplied allowance, |H0|+m <=128, and a
committed cell cap at least 2^k, the main derivation's bound is valid:

```math
2\sum_{i=1}^{m}\max(1,b_i)+(m+1)(2^{k+1}-1).
```

The first term covers production plus replay, including the two scheduled
transactions for a zero horizon. Acceptance is part of the final replay
transaction. The evidence cap cannot block a remaining job: before it accepts
there are at most |H0|+m-1 active constraints. Indexed receipt keys prevent
replacement of another query's constraint.

The disjoint nonempty frontier has fewer than 2^k cells whenever any cell
needs a split: that cell accounts for at least two Boolean assignments. The
cap therefore permits every needed split. Pruning and singleton handling
precede the capacity guard. No capacity-stop requeue occurs under this premise.

The fixed coordinate order and absence of coarsening give at most 2^(k+1)-1
distinct tree nodes. Each source epoch begins with a unique agenda; a completed
inspection removes or splits its node, or finishes a singleton without
requeuing it. Each of at most m accepted receipts begins another epoch by
resetting the current-cell agenda once. The source term follows.

The independent reviewer additionally observed the sharper source-count
bound 2^(k+1)-1+m*2^k: initialization and child creation insert at most the
full tree's nodes, while each receipt reset inserts at most 2^k current cells.
Discarding old pending entries cannot increase subsequent pops. The main note
keeps the simpler epoch bound; neither is a machine-instruction or money bound.

Parsing, dispatch scans, hashing, reports, arithmetic, serialization and host
costs are separate. Opaque coordinates may remain unresolved. An inconsistent
source can finish empty. Exact numerical endpoints require a separately
charged successful report on a nonempty final source; an arithmetic limit
can prevent that report. Call-boundary retention excludes a process crash
inside a transaction. No generic or targeted scientific run was repeated.
