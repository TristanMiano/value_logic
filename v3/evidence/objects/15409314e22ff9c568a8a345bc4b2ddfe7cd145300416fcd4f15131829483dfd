# Readable certificates for the forecast/action price sensitivity

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.

The initial [exact region reconstruction](../forecast_action_price_observation_A1/results.json)
already found three nonempty and nine empty regions for `K=W+lambda*C+mu*B`.
These subsequently selected small-rational examples make its conclusion
readable. They are exact checked certificates, not additional experiments,
a new practical threshold or a changed acquisition policy. Every comparison
uses all 19 distinct ordinary configurations at the same symmetric stakes.

## Three strict illustrative points

| Family | Candidate | lambda | mu | Candidate K | Best ordinary K | Strict gap | Best ordinary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mixed | value_uniform_cold | 1/10000 | 33 | 6.9261420076 | 6.9379139779 | 0.0117719703 | finite_uniform_cold |
| gate_transfer | value_tickets_cached_hashed | 1/100000 | 40 | 10.2139468582 | 10.3636404297 | 0.1496935714 | proof_dpll_fallback1 |
| gate_transfer | value_tickets_cold | 1/100000 | 40 | 10.2075857515 | 10.3636404297 | 0.1560546782 | proof_dpll_fallback1 |

The exact rational scores and all ordinary ties are in [results.json](results.json).
A small positive gap here is a descriptive strict inequality; the frozen
0.01 practical convention is not reassigned to this newly weighted score.

## Nine empty regions have simple convex certificates

| Family | Candidate | Mathematical combination of ordinary records | W gap | C gap | B gap |
| --- | --- | --- | --- | --- | --- |
| cheap_null | value_tickets_cached_hashed | 1 exact_cache_hashed | 0.2421875000 | 439.4869791667 | 0.0014398097 |
| cheap_null | value_tickets_cold | 1 exact_cache_hashed | 0.2421875000 | 202.1822916667 | 0.0014398097 |
| cheap_null | value_uniform_cached_hashed | 1 ordinary_combo_hashed_p1_1000 | 0.1666666667 | 208.3437500000 | 0.0370473397 |
| cheap_null | value_uniform_cold | 1/2 probability_cost + 1/2 ordinary_combo_hashed_p1_10000 | 0.1445312500 | 84.2513020833 | 0.0194657034 |
| mixed | value_tickets_cached_hashed | 1 finite_uniform_cold | 0.0208333333 | 5546.2421875000 | 0.0308349393 |
| mixed | value_tickets_cold | 1 finite_uniform_cold | 0.0208333333 | 4927.3411458333 | 0.0308349393 |
| mixed | value_uniform_cached_hashed | 9/10 finite_uniform_cold + 1/10 ordinary_combo_hashed_p1_10000 | 0.0117187500 | 220.3002604167 | 0.0002844172 |
| gate_transfer | value_uniform_cached_hashed | 2/3 proof_dpll_fallback1 + 1/3 probability_cost | 0.0004340278 | 34231.2421875000 | 0.0037568714 |
| gate_transfer | value_uniform_cold | 2/3 proof_dpll_fallback1 + 1/3 probability_cost | 0.0004340278 | 33541.6380208333 | 0.0037568714 |

Every displayed gap is candidate minus combination and is **strictly positive**.
For any fixed nonnegative lambda and mu, the best component of a combination
has score no greater than its weighted mean, which is strictly lower than
the candidate. This certifies an ordinary-catalogue winner for every price
pair. It does not deploy a randomized meta-controller or claim that such a
controller, with unmeasured selection and interface costs, was run for free.

## What the new scalarization changes

The frozen objective assigns no extra price to issued Brier quality; its
mu=0 boundary still rejects every candidate. A positive mu values an
additional feature of the existing public service. It can expose a
tradeoff that the original terminal objective does not price, but cannot
repair that original endpoint or its unknown outer-attempt cost gate.

The two gate ticketed candidates have identical W and B; cold has lower C.
Thus at positive lambda the cold candidate beats its cached counterpart,
even where both beat the distinct ordinary catalogue. The recorded mirror
and the ordinary identical-kernel interpretation also remain separate:
no strict advantage over an unrestricted ordinary realization follows.

Optional paid report fees are excluded because the report is a further
unequal service. The issued forecast was already produced within the
terminal episode. Changing either score weight in a deployed controller
could change the entire trajectory; this calculation does not do so.
