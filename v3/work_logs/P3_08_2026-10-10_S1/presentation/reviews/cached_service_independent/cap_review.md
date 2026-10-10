> **Portable display copy — notation only.**
>
> Original: [v3/work_logs/P3_08_2026-10-10_S1/reviews/cached_service_independent/cap_review.md](../../../reviews/cached_service_independent/cap_review.md)  
> Original SHA-256: `1bdf64e3810c6610a38aa81275a61fe10d17cd7762afbdc21660f6ec7d67eab3`.
>
> Generated with the unchanged math guard's `transform(protect=True)`,
> plus relocation of relative links to their original destinations.
> The original scientific document remains unchanged. This is a source-notation
> check, with no live-render or new mathematical validation claim.

# Independent static review: selected-receipt reuse cap and coupling

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Same-model, nonblind DEVELOPMENT review; zero principal time credit.

**The 131,072-unit additional cap is conservative for the inspected finite
service, and the stated mathematical-path coupling is valid under its declared
premises.** This review reconstructs source arithmetic and coupling only. The
integration reviewer owns focused service executions; none are duplicated here.
No private labels/scores are read, and this review makes no unconditional claim
about report coverage after conditioning on completed underfunded paths.

## Source binding and closure

The inspected adapter is `v3/experiments/p308_cached_service.py`, version
`p308-selected-receipt-cache-v1`, SHA-256
`6a7c5f28d2930d6b888638fddc86b486d95978f6e5da4823cb61dbf9c728bd1b`.
The initially reviewed derivation `08_selected_receipt_reuse.md` has SHA-256
`7d2a21c9267b718646aa50f6e3b7f77219a9cb5bca64d75bab32f811025550a1`.
They match the integration review's `../cached_service_initial/source_snapshot`.

The cost derivation reads the actual cache and metering implementations:

| File | SHA-256 |
| --- | --- |
| `p308_cnf.py` | `46fd3e82505b9b6af9805836a562f2f78a3436384e0b3476c4f85cec355817a2` |
| `p308_hashcache.py` | `a668abfff6c4dd6c7d18cb186ed99bbb9c794713ce9f93e8a27470320b07a914` |
| `p308_common.py` | `4928a5b9c80e05b497bd93116957139252c65f393e6e12ea4c7ad4727f300a29` |
| `p308_broker.py` | `248642e00333f0939f2e0e41020c69879b2d5bcedacf7979f980583630ba3653` |
| `07_selective_feedback.py` | `f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48` |
| `07_selective_feedback_service.py` | `68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32` |
| `07_computation_adapter.py` | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |

The new core source procurement must include the adapter and its transitive
CNF/hash/common/selective-feedback dependencies, even when a particular branch
does not use hashing. The broker, runner and optional reporter have their
separate declared closure obligations. This per-purchase overhead allowance is
not payment for historical source creation or a replacement for installed
source procurement.

## Independent conservative arithmetic

Let $`Q`$ bound every retained and requested key's words, and $`K\leq64`$ bound
retained entries. Use $`Q=512`$, although admitted CNF keys actually have at most
343 words. Request identity has at most 16 words; there are at most 256 literals
and 64 clauses. A complete CNF admission therefore costs at most

```math
A(Q)=17+Q+16+4(256)+5(64)=Q+1377.
```

The paid key-digest/bucket helper costs at most $`H(Q)=4Q+16`$; this includes key
reads, encoding/temporary storage, digest blocks, argument checks and indexing.
Every full digest collision still pays and performs a complete-key comparison.

The adapter's non-cache, non-child work on a miss is at most $`200+3Q`$: initial
48 units; final local receipt, call-state and counter bundle $`104+2Q`$; cold-cap
reservation control 8; child binding $`32+Q`$; and answer release 8. The miss then
pays two cache admissions, a lookup and an insertion. Reserving the cold child's
cap is not a second debit; the actual child invoice is absorbed once.

For the linear cache, include initialization 6, at most $`K(Q+2)`$ lookup work,
$`16+Q`$ receipt binding, at most $`K(Q+1)`$ insertion scan, entry write $`8+Q`$,
and full FIFO shift $`2+K`$. This gives the cache-only miss allowance

```math
L(Q,K)=32+2A(Q)+K(2Q+4)+2Q.
```

For the hashed cache, initialization is at most 204 (128 heads, 64 slots and
12 configuration/header units). Each of the two complete all-collision scans
costs at most $`1+K(Q+13)`$. Include two capacity branches, two hashes, insertion
binding $`16+Q`$, and at most $`47+Q`$ for planning and committing a full replacement.
This gives

```math
G(Q,K)=271+2A(Q)+2H(Q)+2K(Q+13)+2Q.
```

These bounds conservatively include maximal initialization and a full cache
simultaneously, although a fresh initialization cannot already contain 64
entries. Cache hits omit the child/insertion and are cheaper even after their
rebound receipt and binding charges. Capacity zero also remains below the bounds.

| Maximum key bound | Linear non-child units | Hashed non-child units |
| --- | ---: | ---: |
| $`Q=343`$, $`K=64`$ | 49,547 | 53,970 |
| $`Q=512`$, $`K=64`$ | 72,362 | 78,137 |

Thus both are below 131,072. The derivation's initial wording “below sixty
thousand” is valid with the actual 343-word bound; with its stated conservative
512-word substitution, say “below eighty thousand.” This arithmetic distinction
does not change the advertised 131,072 allowance.

Let the child cap be $`S`$. At every prefix before the child starts, adapter
spending is at most its non-child allowance. A parent account $`S+131072`$ can
therefore reserve $`S`$ without relying on the truth or a likely hit. The trusted
child completes within $`S`$; redeeming the reservation absorbs its actual debit,
and the remaining non-child work is still funded. The broker's block envelope
uses the adapter's advertised cap at every possible selected position, so
choosing a favorable seed is not part of this proof.

## Coupling and receipt meaning

Fix the exogenous query tape, contract, hard mode and full fair selector/action
bit string, with all paths funded. Both service instances start empty. The
adapter retains only successful current checked CNF receipts. A cache hit binds
the current request ID to the same full semantic/source key and thus returns
the same deterministic bit as the cold provider. A miss uses that same cold
provider and separately binds its reply. Hash collisions and FIFO eviction can
change costs or hit status but cannot change a successfully checked bit.

The broker receives the same selected bit at the same selected position. Its
expert and cost-proxy functions are unchanged aliases of the CNF service, and
provider fees do not enter its selection or expert update rule. By induction,
base forecasts, numerical updates, hard masks, actual propensities, bit
consumption and terminal answers agree. A fresh owned adapter is required per
episode so withdrawal/restart cannot reuse another episode's authority.

The adapter uses its own provider name/version; the broker checks that actual
identity. Full receipt objects, resource records, balances and failure paths
are not coupled. A selected cache hit is one checked service receipt, not a new
cold computation or an independent new mathematical observation. This
substitution does not join the structural counterpossible arm to the learner.

## Remaining admission/failure wording question

The cap above covers the fully funded admitted service. The integration
reviewer was also asked to classify a direct low-budget boundary: if the first
48-unit bundle is paid but the next final-receipt bundle is denied, the method
still returns a typed failure receipt although that explicit output prepayment
was not admitted. If this object is external denial/invoice instrumentation,
the contract should state that; a claim of paid deployed failure readout for
every direct budget would require another admission/reserve arrangement. This
question does not undermine the successful-call cap or the conditional
coupling, and is not silently resolved by this static review.

## Prospective v1.1 admission resolution

Addendum, 2026-10-10 UTC. The previous section records the original v1 boundary
without alteration. The current adapter and the integration review's v1.1
snapshot both have SHA-256
`0d7c9de91bf043916d1825feb9ae7f99e34839f5286abe16c0247a32173aedb2`
(6,924 bytes), version `p308-selected-receipt-cache-v1.1`.

I inspected the changed source. A direct account below 576 units is rejected
externally before paid work; no deployed receipt is promised below that
admission threshold. The first operation of every admitted call prepays 576
output units, before the 48-unit contract/call-state bundle or any later work.
Every caught admitted denial therefore returns its paid prefix and a separately
prepaid bounded response. At the minimum 576-unit account the output debit
succeeds and the next bundle fails; its returned spent invoice is 576. The
key/request identity remains the explicit rejection placeholder until its
admission stage. The old `64+Q` output debit is removed.

For every successful corresponding call the changed debit is consequently
exactly `576-(64+Q)=512-Q`. Adding it to the preceding non-child envelopes gives

```math
L_{1.1}(Q)=134Q+3754,\qquad G_{1.1}(Q)=142Q+5433
\quad(K=64).
```

| Maximum key bound | Linear non-child units | Hashed non-child units |
| --- | ---: | ---: |
| $`Q=343`$ | 49,716 | 54,139 |
| $`Q=512`$ | 72,362 | 78,137 |

The 131,072 additional allowance remains conservative. The source change does
not alter the successful selected-label coupling under its original fresh
owner, fixed exogenous tape/bit string and all-path funding premises. It does
change successful invoices and the admitted-failure API prospectively.

Execution evidence belongs to the **integration reviewer**, not this static
review: `../cached_service_v1_1/results.json`, SHA-256
`73a673c2e95fdb5c3dc5d7752004715c8d10d4eaf84fcc828bf3d64c5521b7fb`,
records four passing groups covering minimum-account/paid-denial boundaries,
the exact version/debit delta, broker failure footers and paid failed-child
responses. I read that result and verified its hash; I did not rerun the
service. The original v1 complete-call evidence remains preserved, and its
unfunded direct-response gap is classified as repaired prospectively rather
than retrospectively erased. This addendum adds zero principal time credit.
