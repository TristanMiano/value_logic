# Partial flow certificates: sound, but the first cheap-advice proposal loses

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

The [sequential-bound derivation](sequential_bounds.md) permits any feasible
partial allocation, checked by row demands, column capacities and prerequisite
membership. [flow_advice.py](flow_advice.py) implements a conventional greedy
allocator and a stronger integer Dinic exact control. Integer scaling, graph
construction and independent exact rational allocation checking are timed.
The older Fraction/augmenting-path implementation is retained and used only
as a small correctness comparison, not the strong speed baseline.

[flow01.json](flow01.json) preserves 80 small inputs and three supplied
128-primitive, 384-term workloads. The integer control matches all 80 older
exact optima. Greedy leaves a worse residual upper bound in 13 cases.

| Workload | Greedy residual | Exact residual | Greedy + check | Exact + check |
|---|---:|---:|---:|---:|
| Ample capacities | 0 | 0 | 5.102 ms | 4.676 ms |
| Balanced capacities | 18.375 | 17.75 | 5.136 ms | 6.638 ms |
| Shared core | 176.125 | 176.125 | 4.538 ms | 4.223 ms |

The ample workload's no-gain certificate is sound, but greedy is slower than
the stronger ordinary control. In the balanced and shared-core cases, blindly
trying greedy then falling back to exact costs 11.774 and 8.761 ms, respectively.
No beneficial two-stage economy is established. The greedy prototype computes
its pressure array by repeatedly scanning supports, so its advertised intent
to be cheap is not yet an achieved asymptotic implementation property. A new
version can fix that construction cost; current source and exposure stay intact.

Useful surviving mechanism: proof checking needs only a feasible allocation;
it need not trust or execute the advice algorithm. New prices preserve a
witness exactly when all capacities still hold. The current negative result
rejects this implementation as an economic improvement, not the certificate.
Any revised allocator must keep the integer control and account for fallback
costs. Prices, forecasts and graph inputs are still supplied; no external
deployment benefit or confirmed positive result is claimed.

## Versioned sparse-incidence repair

[flow_v2.py](flow_v2.py) replaces dense mask and pressure scans with incidence
loops for both the greedy method and integer exact control. The 80 old inputs
are explicitly replayed in [flow02.json](flow02.json), preserving every bound.
On the exposed ample workload, greedy plus check now takes 2.006 ms versus
3.311 ms for exact; a new 1,024-primitive, 3,072-term ample workload gives
17.285 versus 34.025 ms. These single cold-call savings are developmental
kernel evidence. The balanced and shared-core fallback pipelines still lose
to direct exact flow (7.455 versus 5.409 ms and 4.095 versus 2.595 ms).
The representation repair benefits both methods and does not support an
unconditional greedy-first policy or an external positive-result claim.
