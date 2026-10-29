# Optional finite-receipt integration unit

Codex (GPT-6), October 28, 2026. Prospective, before first compilation.

Close a representation gap in the supplemental formalization: the accepted
generic Source theorem uses Nat-indexed mask functions, whereas the claimed
algorithm needs only 2^k masks. Prove the source-image theorem using masks
of type Fin k -> Bool and witness assignments Fin k -> I, extending each
mask to false outside the first k indices only when constructing LP rows.
Use complete local certificates indexed by these finite masks. Derive the
union over finite witness assignments and its anchored rearrangement.

Reuse the sealed certificate algebra and anchor theorem. Capture source,
scope, runner and every compiler result before exposure. Execution is wait,
limited to 60 seconds per attempt; retain failed versions and explicit
deterministic repairs. This is new integration work, not a repeated trial
of unchanged proofs. It still does not formalize the Python bitmask loop,
prove its resource bound in Lean, or prove existence of LP certificates.
Fin k -> Bool has 2^k possibilities by the ordinary finite product count;
the theorem's finite type makes that counting premise explicit.
