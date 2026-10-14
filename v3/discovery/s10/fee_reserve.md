# A physical-fee reserve under an incorrect response law

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

The exact prefix expectation assumes the declared score distribution. Correct
source certificates do not make that probability law true. Endpoint-heavy or
correlated latent costs can destroy the predicted acquisition savings.

Use an ordinary conservative-baseline reserve. For request t let the executable
fallback have known physical fee at most C_t. Start with a declared allowance
B_0>=0 and, before any optional query of fee f, require cumulative optional
spending s+f<=B_{t-1}. Retain any independent per-request spending guard too.
If no certified action closes, execute fallback. Let actual total fee be A_t,
including every query and fallback, and update

```math
B_t=B_{t-1}+C_t-A_t.
```

If the request closes early, A_t=s<=B_{t-1}. Otherwise A_t<=s+C_t<=B_{t-1}+C_t.
Either way B_t>=0, by induction. Therefore, simultaneously at every completed
request n,

```math
\sum_{t=1}^{n}A_t\le\sum_{t=1}^{n}C_t+B_0.
```

This is pathwise: no independence, stationarity, correct proposal distribution,
or probability estimate is needed. It requires truthful known query fees,
an actually executable fallback within C_t, and append-only payment accounting.
An interrupted request's paid prefix must be retained and charged before a
restart; resetting its reserve would invalidate the guarantee.

With constant C and B_0=C,128 completed requests spend at most129C, only0.78125%
above the full-audit reference. The allowance is explicit extra risk capacity,
not a saving or revenue. If B_0=0 and no zero-query completion earns surplus,
no exploratory query can start. A depleted reserve may permanently prevent
exploration. Thus the invariant alone gives no regret-to-best-policy or useful
learning guarantee. It can be too conservative in a changing environment.

This bounds physical fees only. To include computation, every optional unit
and fallback would need enforceable bounds in a common actual price currency,
including source setup, failed prefixes, storage, and checking. Our counted
units and unknown tariffs do not supply those hypotheses. Do not label the
physical invariant a complete-cost guarantee.

Relation to ordinary methods: Wu et al., Conservative Bandits (2016), sections
2.1,3.1--3.3 and4, already use a budget relative to a default policy to permit
or block exploration. Their stochastic result concerns mean rewards with
confidence bounds; their adversarial wrapper uses a fixed default reward.
This simpler invoice identity exploits known charges and a reserved fallback.
It imports neither their learning rates nor their novelty claim. Ordinary
mirrors must match it. The contribution here is integration with paid source
certificates and a falsifiable cost-law stress test.
