# The sharp lower bound available from partial action receipts

**DEVELOPMENT derivation — Codex (GPT-6), October 14, 2026 UTC.**

For any receipt state let J be the neighbors of observed M vertices. Every
compatible world's sufficient query set must include J and must cover the
remaining graph. Conversely, complete every unobserved vertex to E. Its only
M vertices are the observed ones, so its exact optimum certificate cost is

```math
B^*(r)=c(J)+\mathrm{VC}_c(G[V\setminus J]).
```

Therefore this is the greatest lower bound on the realized optimum that can
be justified uniformly from the current receipts alone. The dual certificate
in graph_audits.md is a tractable lower approximation. The gap has two distinct
sources: a suboptimal dual on the residual graph and unavoidable uncertainty
about the hidden world's mandatory vertices. No computational improvement can
eliminate the second gap while preserving the same compatible set.

For general graphs computing this sharp bound is NP-hard: choose an all-E
receipt state (or no receipts), giving J empty and ordinary weighted vertex
cover. For bipartite graphs, a minimum cut provides the exact answer; its
matching flow is a compact independently checkable lower certificate. A
max-flow producer must be executed and billed. A static graph dual is reusable
across requests; a residual optimum depends on the receipt state, though a
state-keyed cache may reuse exact J values.

Buying an extra audit solely to enlarge J can strengthen a retrospective
performance claim while making actual service cost worse. Such acquisition
needs its own request duty and value calculation. An action already checked
to have zero regret does not need further physical observations merely because
its cost-ratio certificate is loose. Keep original-action correctness,
certificate cost optimality and total service cost as separate quantities.

The current paid graph service uses the cheap static dual. It pays the same
lower-bound interface for its ordinary controls. Its naive greedy comparator
rescans the entire graph after each query; that is not the strongest practical
ordinary implementation. Before interpreting named compute prices, replace
those repeated scans with incremental degrees, a forced-query queue and an
instrumented heap. Reconstruct the same query order on existing traces, then
execute that improved service separately. No earlier measured bill is edited.
