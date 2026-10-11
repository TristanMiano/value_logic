# P3-10 numeric observer: independent source review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, `/root/certificate_reconstruction`.
Date: October 11, 2026 UTC. Principal research credit: **zero**.

**Disposition: the numerical reconstruction matches the frozen algorithms by
source inspection. Strengthen the scope checks before describing its output as
a full scope-and-chronology reconstruction.** This is a separate same-model,
source-aware review. I did not run the observer or read final inputs, public
outputs, private evaluations, or analysis results.

The reviewed observer has SHA-256
`087f750c30cb46d7f31bd328d633177f93ff629dd2d65b2fd3226b7abd33a958`.
The exact observer and supporting sources are preserved under `source/`; the
complete read identities are in [source_hashes.json](source_hashes.json).

## Numerical checks

| Component | Source comparison and conclusion |
| --- | --- |
| Random words | `BitTape.seeded` draws successive 64-bit words. `take` reads the least significant remaining bits of the current word before crossing into the next. Summing each generated word shifted by `64*i`, then shifting by the consumed position, is exactly the same finite bit string. |
| Consumption order | Each block consumes its selector bits first, followed by one action draw per issued request. The observer retains the same order and verifies the exact total consumption. |
| Selector favorite | Maximizing the exact fraction `q*(D-q)/proxy` gives the same order as the worker's cross-products. Python's first maximum matches the worker's strict-improvement tie rule. The public proxy reproduces `key_words`, including the admitted ASCII version strings. |
| Ticket selection | The low half of tickets names a position; the upper half names the favorite. The favorite consequently has multiplicity `B+1`, and every other position has multiplicity one. Recorded propensities and selected multiplicity are checked. |
| Weight updates | Uniform factors use `K-loss`. Ticket factors use `multiplicity*K*K-(2*B-multiplicity)*loss`, where `K=2*B-1`. The observer reproduces both factors exactly. |
| Rounding | Fraction arithmetic computes the exact floor of each scaled positive product. Adding one per expert and assigning the remaining units to the first indices matches the inherited fixed-order rounding rule. |
| Truth and advice | Bit masks implement each variable over the complete assignment set; bounded complement, clause union and formula intersection correctly handle empty clauses, empty conjunctions, duplicates and tautologies. The six advice functions agree with the set/mask definitions in the frozen CNF service. |
| Information chronology | The base forecasts for a whole block use its initial weights. Hardening consults only labels bought before the current issue; a selected current label becomes available after issuance, including to a later duplicate inside the same block. The update occurs once at the block boundary. |

## Concrete coverage gaps in this observer version

1. **Bind the replay parameters to the scheduled configuration.** The observer
   currently trusts the episode's `contract`, `hard_enabled`, and selector. Check
   them against the immutable protocol, public horizon, and unit parameters,
   including the index configuration. Also compare the retrieved public and
   evaluation unit objects to their scheduled objects and retain the input-result
   byte links. This prevents a coherent replay of a self-reported wrong contract
   from passing the supplemental check.

2. **Check the complete semantic key and epoch at the interfaces.** The observer's
   internal key includes semantics version, source version, variable count and
   clauses, correctly excluding the request's display ID. However, it does not
   compare the recorded `claim_key` or `scope` to that key and the scheduled
   `p309-<group_id>` epoch. Check the row key, row scope, episode scope, and selected
   receipt key explicitly. Validate `hard_after` against the newly updated known
   map and the final hard-state counts and zero-withdrawal epoch. The current
   `hard_before` check alone is a narrower chronology check.

3. **Reject duplicate or extra invoice identities.** Building `by_query` directly
   can silently collapse repeated invoice IDs. Require distinct invoice IDs,
   exactly one checked invoice for each selected request, and no invoice for an
   unselected request. Bind the provider/version to the unit's cold or cached
   provider. The recorded purchase count alone does not establish that roster.

These are observer coverage gaps, not identified defects in the frozen paid
implementation or its outcomes. Several interface checks already exist in the
frozen private scorer and the separate lifecycle audit. Adding them here supports
a stronger independent reconstruction without changing any frozen experiment.
