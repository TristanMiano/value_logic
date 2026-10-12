# Marginal-profile comparison repair

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

The original probe exits 1 at its explicit example's product-model value
assertion. The 32 generated-case loops had returned but the full result was
not written; retain the failed source/log/exit and do not claim a completed
record. Original probe SHA256:
`3492c4e7df00dd1a5f83731d0fef001be9f1da6ee4143ae633c6ce7534796e81`.

Inspection found the comparison field called the marginal-profile `value`
function on a product profile at argument one; that function correctly returns
zero at error budget one, but the product profile needs magnitude one.
[Separate diagnostic](hinge_debug01.json) evaluates the product profile with
its own function and enumerates all eight query sets: the expected value is
1/27 with no queries. Neither profile algorithm requires a change.

Prospective repair: copy the probe to `hinge_probe_v2.mjs`, replace that one
comparison call with the already imported `productValue`, bind both probe
versions, and run the same seed, cases and checks to `hinge02.json`. This is
a deterministic comparison-code repair, not an independent confirmation or
an unchanged retry. The failure and diagnostic remain preserved.
