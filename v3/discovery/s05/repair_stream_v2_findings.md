# Dynamic repair stream: corrected scalar adapter and exact paid-receipt replay

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), 2026-10-12 UTC.** This is a
routine cost correction on the already exposed 80-request stream. It is not a
new cohort, a new source acquisition, or a persistent native IHS comparison.
The original `repair_stream.py` and `repair_stream_results.json` are preserved.

## Correction and result

The original scalar adapter independently checked each new negative proof,
then compiled and stored its soft-leaf masks, although subsequent scalar queries
used only its budget cut. The corrected adapter preserves the proof check,
complete proof receipt, cut, witness bank and controller. It omits just that
unused new compilation. The tree adapter is unchanged.

| Same 80-request stream, per representation | Tree profile | Scalar cuts |
|---|---:|---:|
| Requests closed by retained bounds | 61 | 57 |
| Historical new source calls replayed | 19 | 23 |
| Historical source tariff | 43,415 | 50,052 |
| Corrected adapter tariff | 20,529 | 14,821 |
| Common initial profile setup retained from v1 | 7,975 | 7,975 |
| Corrected tariff including that common setup | **71,919** | **72,848** |
| Original v1 tariff on the same convention | 71,919 | 73,965 |
| Sum of realized request action costs | 223 | 223 |

The scalar correction removes **1,117 units**: 975 for tree compilation and
142 for compiled-mask storage. Every request still meets its one-unit regret
tolerance. All request outcomes, including source identities, bounds, status,
chosen action and witness, are identical to v1. The complete returned provider
receipts are byte-equivalent after canonical JSON decoding.

On the retained common-setup convention, tree saves **929 units**. Its four
fewer source calls save 6,637 provider units while its additional adapter work
costs 5,708. This is a narrow representation tradeoff on this exposed stream.

## Important setup sensitivity

The 7,975-unit initial profile setup is inherited as a common supplied artifact
for both representations. It includes 1,319 units of old tree-mask compilation
and storage: 1,154 + 165. The independent old proof checks cost a further 2,282
and remain necessary to use their scalar lower claims.

A standalone scalar consumer could also omit that *initial* 1,319-unit mask
compilation while retaining and checking every old proof. Its invoice-adjusted
standalone total would then be **71,529**, 390 below tree's 71,919. This second
number is an explicit invoice adjustment, not another executed controller
variant. The v2 code implements only the requested new-receipt correction and
keeps v1's shared initial artifact. Accordingly, **the 929-unit margin does not
establish a general end-to-end cost advantage**. The positive concrete capability
is that retained leaf information closes four additional requests without new
source search; the current small raw implementation does not yet justify an
unqualified total-cost claim under independently optimized setup.

## Replay and evidence boundary

`repair_stream_v2.py` checks the recorded hashes of the original stream code,
provider, repricer and original receipt bundle. For each arm separately, it
consumes paid receipts in their original order. A requested purchase must match
its event index, row, recipe, complete source identity, weights, budget and
pre-query interval. The cap must equal the constant in the hash-verified v1
caller/provider. V1 did not include a separate cap field in each event; this
provenance limitation is recorded explicitly.

The replay checks archived invoice sums and the cap. It then returns the saved
model or complete negative tree. The corrected adapter independently repeats
all witness/objective and negative-proof checks under the current source and
budget before updating its retained bounds. An unresolved answer would leave
the requested action unresolved and stop that request; none occurs in this
stream. All 42 historical receipts are consumed, and all 160 per-arm request
outcomes are compared with v1. The native provider is temporarily replaced by
an unconditional refusal guard throughout this execution.

All old and new complete proof bytes remain in the immutable input archives
and replay receipt lists. Scalar mode retains 18 initial compiled trees but
compiles no new tree masks; the original complete new proofs remain available
for a later, explicitly paid representation change.

## Historical work versus actual work now

The 93,467 source units in the two stream arms were paid in v1. They are copied
as historical invoices, not claimed as new work or independently reconstructed
search costs. The still earlier common source acquisition was 77,646 units;
it remains separate and common to both corrected stream totals.

This replay makes **zero new source calls** and **zero exact diagnostic calls**.
Its actual newly performed declared work is:

- 7,975 units to rebuild and check the common initial profile once;
- 35,350 units for the two corrected adapters, including repeated proof checks;
- 10,095 units for extra replay scope, invoice and payload checks;
- **53,420 units total** for this execution, without historical search units.

The one warm replay took approximately 37.6 ms before final serialization and
read 910,476 archive-bundle bytes. JSON loading, hashing and serialization are
additional to the declared operation tariff. This runtime is not a fresh-solve
speed measurement. Extra replay-only checks are recorded separately from the
hypothetical corrected controller tariff; they are work required to validate
this development replay.

Verification confirmed every preserved input hash and the v2 source hash. Small
scope checks rejected changed budget, cap, row/order and source identity, and
confirmed the native-provider refusal guard. No solver or source truth was
used for those checks.

## Files

- `repair_stream_v2.py`: runnable corrected adapter with strictly matched replay.
- `repair_stream_v2_results.json`: complete repeated receipts, actions, invoices,
  source hashes and separated historical/current work.
- `repair_stream.py` / `repair_stream_results.json`: unchanged historical v1.

The result supports continuing compact profile and ordinary-control engineering.
It is not a reason to freeze this tiny stream as a final performance benchmark.
