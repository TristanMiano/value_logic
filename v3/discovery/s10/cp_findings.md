# Capped-state planning: paid comparison and limits

**Codex (GPT-6), October 14, 2026. DEVELOPMENT.**

cp01 compiled exact prefix values and ordinary depth-1/2/3 fallback policies
on all 16 exposed external-source duties without hitting the state caps.
The active residual vector has 0--8 entries despite 20 source variables.
Prefix planning used 130--54,945 named units per case; depth-three planning
used 4--979,564. A short adaptive horizon can lose to a longer fixed order.

cp02 bought fresh cost outcomes on these exposed sources: 24,576 outputs and
4,096 per arm. All 96 arm/stream executions completed first attempt. A corrected
independent checker verifies exhaustive source models, every output's exact box
regret, purchases, the ordinary mirror and all 32 compiled prefix/adaptive
expectations by an independent explicit policy traversal. Its first version
mistook ascending-model order for the compiler's model order when indexing
residuals; preserve that failed checker and log. This was a checker defect,
not a changed service or free reacquisition.

| Arm | Audit fees | Counted units incl. setup | Setup units | Fallbacks |
| --- | ---: | ---: | ---: | ---: |
| Prefix / ordinary mirror (each) | 7,599 | 17,962,040 | 11,861,585 | 980 |
| Adaptive depth 3 | 7,755 | 20,269,909 | 14,113,626 | 1,000 |
| Simple threshold order | 7,601 | 17,547,216 | 11,760,154 | 355 |
| One-query marginal | 15,574 | 20,167,033 | 11,738,834 | 1,520 |
| Relevance-aware full audit | 32,256 | 18,099,956 | 9,913,076 | 4,096 |

Prefix saves 76.44% fees and 0.76% counted units against full audit on this
declared 256-request horizon per stream. Threshold saves 76.44% fees and 3.05%
counted units. Prefix's two-fee-unit gain over threshold costs 414,824 extra
named units. For an illustrative scalar tariff fee + lambda*named_units, that
gain matters only when lambda < 2/414824, about 0.0000048213 fee units per
named unit, before any unknown costs. This is a retrospective component-price
comparison, not an external price claim or a complete economic benefit region.

The ordinary prefix implementation ties exactly. All arms received shared
incremental residual updates, so the comparison does not rely on repeatedly
recomputing a weaker competitor's certificates. The prefix's expected-fee bound
is constructive but conditional on the declared independent cost law. These
results support trying response-conditioned actions and cheaper reuse; they do
not justify promotion to P3-11 or improvement of the unrelated F01 event.
