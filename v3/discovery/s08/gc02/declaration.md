# gc02: general-graph cover with paid certificates and efficient selection

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

gc01 finishes20 declared graphs with496 cut checks and80 invalid-certificate
controls. Small graphs cover4,032 partial states,843,840 action classes,
2,052,900 corner comparisons and3,568 terminal actions; larger cases check
66,996 actual-world actions. Eight clique decompositions improve the trivial
cut bound; two sparse cases remain loose (17 vs16 and23 vs22). No physical
cost query was acquired;20 original mandatory-unit resolution steps were
executed and retained. No complete SAT call occurred.

For an unobserved vertex i and possible observation v, maintain

```math
M_i(v)=2\sum_{j:ij\in E}w_{ij}\max(0,H-v-d_j).
```

This is its uncapped increment in cover score. Initially every d_j=0.
When a neighbor j is first queried with score d_j, subtract
2w_ij min(H-v,d_j) from each M_i(v). Other neighbors' contributions are
unchanged. Also update the achieved edge-max score using only incident
edges. Given remaining quota r, the exact expected marginal is the public
probability-weighted mean of min(r,M_i(v)). The anchor's marginal is r.
Both r and each unobserved vertex's marginal table only decrease, so cached
benefit/fee scores remain upper bounds. Ordinary lazy greedy repeatedly
refreshes the heap's top until its score was computed at the current state;
then no stale upper bound exceeds it. Tie-breaking uses coordinate order.
It therefore selects exactly the same query as a full current-score scan.

This is standard incremental/lazy greedy machinery, not a new optimization
principle. The intended saving is the actual selection work on the admitted
original graph. All arms receive the same clique bound, mandatory resolution,
source compilation and action checking capabilities.

**Prospective paid gc02:** n8,16,32 crossed with path,cycle,unit clique and
seeded sparse weighted graph (seed8141700). Sparse graphs contain their path
and each other edge with probability0.2, weights1..5. Query fees are1..7;
anchor fee2n+9. H=4, source alphabet{0,2,4}, common anchor0/A with A=10HW,
priceA, toleranceHK for the acquired clique certificate. Execute64 fresh
independent uniform requests per case, seeds8141710..21. Arms: lazy cover,
ordinary lazy mirror, adjacency-based current-score scan, and anchor-only.
All physical query caps are n+1. Freeze implementations and design before
cost-provider calls; acquire/check12 actual mandatory resolution and clique
certificates, preserving their invoices. No complete SAT provider is assumed.

Original exactly-one source geometry is admitted once per arm. The fixed
balanced original bitmask is compiled and checked once; later uses compare
the exact admitted bitmask and source identity. For an upper-cost repair,
construct the complete original bitmask from the smaller compatible upper
endpoint on each edge and check that recipe against the admitted source.
Every service still exports the complete bitmask, and export/read word costs
are charged. This uses explicit persistent source facts, not a changed action
duty. Post-run reconstruction independently rechecks every original clause,
receipt, marginal/controller choice and returned bound. For n8 evaluate all
compatible box corners; larger cases use the proved bound and actual hidden
world, with separate exhaustive small geometry evidence. Raw model/runtime
failures retain physical prefixes and never become free successful trials.
