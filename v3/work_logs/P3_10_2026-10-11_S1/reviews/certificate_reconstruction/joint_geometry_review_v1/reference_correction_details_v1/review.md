# Addendum: exact snapshot-to-live reference corrections

Signed: **ChatGPT (GPT-6 Astra Pro), `/root/certificate_reconstruction`**  
UTC: 2026-10-11T16:06:23.920208+00:00  
Disposition: **PASS, all six reference-center exceptions explained exactly.**

This additive detail accompanies the signed geometry review SHA-256
`76841babb5faa4851f9ca0cab7375d15b6b554da52af365a600fd1678b6f525b`.
It preserves the existing review, observer and results. Delta F and Delta V
below are specifically the reporter's **reference corrections** from its
predictable block-start snapshot to the live issued path. They are not the
larger full base-to-live correction totals, whose raw encodings are separately
retained in the accompanying JSON.

| Unit ID | Reference Delta F | Reference Delta V | Delta F minus Delta V |
|---|---:|---:|---:|
| `broker_cheap_null_p01__value_uniform_cold__seed3091002` | 38551681/1073741824 | 6209/32768 | -164904831/1073741824 |
| `broker_cheap_null_p01__value_uniform_cold__seed3091003` | 119311929/4294967296 | 10923/65536 | -596537799/4294967296 |
| `broker_cheap_null_p01__value_uniform_cached_hashed__seed3091002` | 38551681/1073741824 | 6209/32768 | -164904831/1073741824 |
| `broker_cheap_null_p01__value_uniform_cached_hashed__seed3091003` | 119311929/4294967296 | 10923/65536 | -596537799/4294967296 |
| `broker_cheap_null_p01__ordinary_kernel_mirror__seed3091002` | 38551681/1073741824 | 6209/32768 | -164904831/1073741824 |
| `broker_cheap_null_p01__ordinary_kernel_mirror__seed3091003` | 119311929/4294967296 | 10923/65536 | -596537799/4294967296 |

Every row has exactly one within-block change: zero-based position **15** in
block **3**, after a matching selected receipt at position(s) **13**.
The changed position is unselected. The receipt says y=1, and the live issued
forecast is exactly 1. The block-start snapshot did not yet possess this
receipt, so its reference forecast still uses the base dyadic. For seed
3091002 that base is `53118/65536`; for seed 3091003 it is `54613/65536`.
Consequently `Delta F=(1-base)^2` and `Delta V=1-base` at this position.

The corresponding reference-center difference is exactly
`C + Delta F - Delta V`; the corrected live centers and both delivered
interval endpoints still differ by C. These are two coupled seed-path cases
represented in three configurations each, not six independent mechanisms.
Full claim keys, paid receipt/query identities, the original unreduced
encodings, reduced exact fractions and input hashes remain in `results.json`
and `source_hashes.json`.

This is read-only JSON arithmetic using already paid labels. No new truth,
paid method, principal observer, scorer or analysis was executed. Principal
research-clock credit is zero.
