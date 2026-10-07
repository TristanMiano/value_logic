# P3-01: growing-stakes criterion check

Reviewer: **GPT-6 Astra Pro**, October 7, 2026 UTC. Same-model internal,
nonblind mathematical check of criterion probes §5 only. No canonical edits,
experiment, executable test, later-task execution or clock credit.

**Disposition: correct as scoped; no mathematical correction required.**
For positive integers `n`, the forecast is a valid probability and
`(p_n-0)^2=1/n^2`. For every `N>=1`,

```math
\sum_{n=1}^{N}\frac1{n^2}
\le 1+\int_1^\infty x^{-2}\,dx=2.
```

The two estimated action costs are exactly `1` and `1/2`, so the estimated
minimizer always selects the fallback without a tie. Actual costs are `0`
and `1/2`. Regret against the same available action chosen always is therefore
`1/2` per request and `N/2` cumulatively; average regret stays `1/2`.

There is no contradiction with prediction convergence: the forecast error
`1/n` vanishes while its task-cost amplification `n(1/n)=1` does not. The
known request-specific integer coefficient remains within the native rational
scaling interface. The claim needs no product of two uncertain coordinates.

The stated limitation is essential and sufficient: this numerical sequence
is not asserted to satisfy U04, be an LI, or describe a procedure that ignores
legitimately available resolution evidence. It refutes only an implication
from normalized prediction quality alone to this unbounded-stakes decision
guarantee. The text correctly excludes the calculation from the earlier
eleven-group numerical run and leaves P3-06 unstarted. P3-N01 remains
NOT YET SUPPORTED; no gate status changes.
