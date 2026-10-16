# Ordinary path-control screen: no service gain

Codex (GPT-6), DEVELOPMENT. The predeclared screen in
[path_feedback.md](path_feedback.md) ran unchanged as [path_service.py](path_service.py),
with retained outputs in ps01. All five cases passed on their first attempts.

| Case | n | Bandwidth | Requests | States / arcs | Complete paths | Execution fee | Truth queries |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 0 | 16 | 1 | 2000 | 32 / 46 | 1597 | 33153 | 6675 |
| 1 | 64 | 1 | 2000 | 128 / 190 | 17167680177565 | 166499 | 34113 |
| 2 | 64 | 1 | 2000 | 128 / 190 | 17167680177565 | 147489 | 29400 |
| 3 | 64 | 1 | 2000 | 128 / 190 | 17167680177565 | 597254 | 120280 |
| 4 | 8 | 2 | 256 | 38 / 72 | 400 | 3351 | 1214 |

The first four reuse the exact exposed ls01 worlds. Their pooled fee is
944395, versus 938744 for the sparse free-feedback learner, 940053 for the
paid local-feedback learner and 937656 for the stronger scalar bandit0
control. The new path control loses to bandit0 in each of these four cases.
It incurs zero extra feedback queries. The fifth case checks implementation
extension and has no comparable service claim. Tuning was fixed from the
displayed theorem before execution; no tuning search followed this result.

No zero inclusion probabilities occurred; maximum reported flow discrepancy
was below 6.21e-14. The first four cases counted 2464000 forward/backward
log-add operations, 1232000 edge exponentials, 243374 sampling exponentials
and 190468 purchased-edge updates. These are named operations, not total
machine work and not comparable one-for-one with matrix products in the
contrast-tree learner. Source admission and prior development costs are not
included. Finite numerical conformance does not prove the real-arithmetic
regret theorem or a population service advantage.

The constructive return is the explicit ordinary comparator and its no-extra-
purchase square-root guarantee. It blocks a claim that the earlier conservative
two-thirds rate is fundamental. It does not rescue an empirical fee-gain claim
for the model-based learner. Keep the off-path layer lemma as an unimplemented
structural lead; no unbiased free off-path update has yet been derived.
