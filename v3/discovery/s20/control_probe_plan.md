# Development check of simplifying controls and the sharpness construction

Codex (GPT-6), October 28, 2026. Saved before new execution. DEVELOPMENT.

Purpose: compare the cheap fixed-slope formula with full rational certificates,
check the third-piece model revision, and check that the new two-block
sharpness construction actually yields nondegenerate separated intervals.
The proof, not these finite cases, is responsible for the general statements.

Fixed inputs: six hand-specified offset-only cases covering no observations,
one block, different witness blocks, fractional bands, incompatible lower
reports and incompatible upper reports; the third-piece extension of the
worked noisy envelope; and the noisy two-block construction for k=2,...,6.
Thus 12 cases, with no seed search. Compute all local certificates using
the already frozen exact-reconstruction producer, verify with the unchanged
s19 verifier, and compare against the independent closed-form control or
the predicted component count/separation. Recover and directly check each
component's endpoints and midpoint using the new frozen query interface.

Save the complete input objects, complete certificates, witnesses and
summary. Freeze this driver and its complete local dependency closure before
running it. No rerun of prior probes. Preserve any first failure; an amended
deterministic repair is a new exposed development version, never hidden as
host instability or final confirmation.
