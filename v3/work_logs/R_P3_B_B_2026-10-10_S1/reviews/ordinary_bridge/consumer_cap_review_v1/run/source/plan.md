# Completed consumer-cap record review

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls agent, October 10,
2026 UTC. This is a same-model, nonblind DEVELOPMENT review. It earns zero
principal or agent research-clock credit.

## Selection and inputs

The parent requested an independent reconstruction of the completed
`development/actual_consumer_cap_v1` records, followed by comparison with
`development/actual_consumer_cap_analysis_v1`. Before this plan, the parent
reported 288 attempts, 239 deliveries and 49 failures. The reviewer read the
completed summary, manifest and revised analyzer source. The reviewer has not
yet read the raw attempt records or the analyzer's numerical output.

The fixed run has consumer budget 1,048,576, total budget 134,217,728 and a
1,024-unit failure reserve. It contains the original four streams, two recipient
modes, six methods and six sequential requests per session. The input unit-log
SHA-256 is
`01e88137a200c02385f1039fb146083780bf66a76900dee62f67d655460ccd4f`;
the run manifest SHA-256 is
`453cdb9baee2ad312d564c82029fddc92b4af45174c729b2797a47641784b072`.
The revised parent analyzer SHA-256 is
`2d40060d04a4c019b61a537cc1b19bca0586a27e953451f05a9fbc83e8c8a5fa`.

## Fixed reconstruction

Use a new standard-library-only reader in this directory. It will not import
or execute any worker, checker, fixture or parent analyzer. It will first
require the complete passing summary and exact seals, then verify captured
sources, the original worker-source record, primary input/reference binding,
the 288 exact attempt keys and their declared order. Every delivered output
must equal the matched primary output bytes. Failure outputs, source/cache
observations, packet byte bills and total/consumer invoice arithmetic will be
checked for every attempt.

For each of the 48 sessions and each prefix, independently sum all attempt
costs and form a six-bit mask of delivered request positions. Compute both
primary predicates directly from the matched original invoices. Keep exact
IDs for every disagreement, and distinguish prior failure from no prior
failure. Record source enrollment persistence, source-charge attempts,
reported scientific-cache eviction, subsequent recovery and failure stages.
An invoice does not disclose the rejected charge or identify which budget
branch raised; no missing trigger will be invented.

Enumerate pairwise prefix comparisons using delivered-mask inclusion and
complete cumulative total cost. Keep any empty-set raw relation explicitly
separate from a successful-service winner. Include failed costs even when
comparing identical delivered sets; neither success-conditioned costs nor
coverage counts alone define the comparison.

Only after the independent reconstruction is saved, read the parent's sealed
analysis output. Check its source/file seals and compare every request,
prefix, aggregate, discrepancy and coverage/cost relation. Save differences
before asserting agreement. Preserve any failed reader/check attempt; do not
change policies or rerun the underlying experiment.

## Execution and scope

One bounded pass over the 288 completed records and their referenced immutable
packets, one pass over the 317 sealed primary records, and one comparison pass
over the observer output are authorized. Reading, hashing, integer arithmetic
and JSON/CSV decoding are observer apparatus. This review adds no scientific
worker executions, new fixtures, threshold selection, retry or fallback.
All preexisting workers, sources, contracts and results remain immutable.
