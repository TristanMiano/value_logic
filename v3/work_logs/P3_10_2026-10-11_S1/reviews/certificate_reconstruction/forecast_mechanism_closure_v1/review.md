# Closure of forecast mechanism exposition findings

Signed: **ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction**  
UTC: 2026-10-11T15:54:36.862446+00:00  
Disposition: **R1 and R2 CLOSED.**

The additive note SHA-256 `43d0560694855eb769e87873313169359f943ad4cb3609f697691427d7b1b7ae` fully addresses the two wording findings in the signed review SHA-256 `fa2b4e872cfcaf5747d9fc270640994766673bc1b34e6945e41280b53c3acc65`. The numerical/source PASS from that review is unchanged.

R1 now says that w uses already rounded fixed-mass weights and bounds only the final forecast projection, with no accumulated-update or hypothetical real-weight conclusion. The exact practical-threshold lower bound is `1/100 − 5/196608 = 49027/4915200`.

R2 now states the pointwise sign restriction explicitly and confines reversals to aggregation. Its two-position example gives mean Brier improvement `3/32`, binary-functional improvement `−1/8`, and variance difference `−7/32`, with `3/32 = −1/8 − (−7/32)` exactly. These are illustrative arithmetic, not additional data.

The original derivation and result bindings remain intact; no observer, paid method, scorer or analysis was rerun. This additive closure contributes zero principal research-clock credit. Source snapshots and exact rational checks are recorded in `closure.json`.
