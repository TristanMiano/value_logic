# Prospective certificate-transport development check

Codex (GPT-6), October 28, 2026. Separate exploratory extension. This is
not part of the frozen V19 contribution event or P3-11-A1 confirmation.

Before execution freeze this plan, the transport implementation, probe,
transport derivation, retained audit records, LP producer and old verifier.
Use a fresh output attempt directory; refuse overwrite. Preserve failures.

Questions and finite panel:

1. Reuse the existing noisy-envelope certificate on 16 deterministic changed
   models (seed 202820): receipt endpoints, receipt coefficients, and future
   readout coefficients/offsets change. Physical coordinate rows remain
   fixed. Produce and exactly verify fresh LP certificates *only* for the
   changed controls; compare their entire ranges and all nonempty local
   images to the transported outer bounds. Count new solves separately
   from the zero-LP reuse path. This establishes containment on these cases,
   not completeness or a speed advantage of the producer.
2. Old inconsistent constant receipts become consistent after changing the
   receipt from [1,2] to [-1,1]. The old empty slices must reappear. A shortcut
   retaining their old empty status must give a strictly wrong empty answer.
3. A fixed perturbation of the noisy envelope compares the residual bound
   with the unsound shortcut that discards its residual. At least one
   explicit one-dimensional control must expose the shortcut failure.
4. For receipt expansions and the excluded band [-5/4,-6/5], compute the
   first outer hit. Check before/at/after this rational boundary against
   direct interval-family evaluation and fresh exact changed LP controls.
   The first outer hit is not required to equal the exact repair radius.
5. Check the radius DP against exhaustive assignments for 120 deterministic
   artificial families, n=1..4, k=0..4, including infinite activation times,
   zero slopes, singleton intervals, and bands already admitted at zero.
   Check its finite boundary against a separate interval sweep evaluation.
6. Reject unsupported changed indexing, missing explicit finite coordinate
   bounds, negative expansion slopes, and omitted slices. These are bounded
   misuse checks, not hostile-input or security coverage.

Wall run budget: 60 seconds. Expected 2--15 seconds; mark unattended run as
wait and exclude it. Save all changed inputs/certificates, artificial inputs,
answers, control results, runtime/environment, and file hashes. First failure
is preserved and any code repair gets a new attempt and explicit explanation.
No percentage speedup, empirical economy claim, or novelty probability is
an expected output. Ordinary safe bounds plus the same recurrence tie.
