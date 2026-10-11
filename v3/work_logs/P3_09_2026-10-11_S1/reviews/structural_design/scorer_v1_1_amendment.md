# Prospective exact-type scoring amendment

Contributor: ChatGPT (GPT-6 Astra Pro), October 11, 2026 UTC.
P3-09 preparation; zero principal-clock credit. No final exposure.

Before configuration freeze, a narrow source review found that the v1 private
scorer compared terminal JSON dictionaries with Python container equality.
That equality treats boolean values as equal to integer zero or one. The
owned worker's witness codec already rejects booleans, so honest v1 delivery
was unaffected; the independent exact-output audit was nevertheless too weak
for a forged terminal witness.

The original adapter SHA-256
`218cbde22309d3ec25c47611a2954fb19cdb68faf7680980f4b5b677c6c4eabc`, its 55
development attempts and all snapshots remain unchanged under
[development_smoke_v1](development_smoke_v1/). The separately predeclared
[observer reproduction](development_smoke_v1/observer_type_v1/results.json)
changed the first valid two-bit toy receipt's integer zero witness entries to
JSON false. The original scorer accepted that exact-type violation. No worker
or final generator ran in this diagnostic.

Version `p309-certificates-v1.1` will compare canonical exact terminal JSON
with canonical expected JSON, distinguishing booleans from integers. The
source version changes prospectively. Recipes, methods, recipient eligibility,
accounts, receiving semantics, resource governor and scoring denominators do
not change. The application source byte fee changes with the source itself,
so root must freeze the new complete source record and rerun its required
development gate on that frozen closure. No old invoice is relabeled as a
measurement of the new code.

The focused v1.1 check will re-audit the preserved development terminal under
the declared old paid-source record, with the newer independent scorer. It
must reject the boolean witness, retain the original all-attempt paid total,
and remove the invalid request from covered identities. This retrospective
observer check makes no new paid-service performance claim.
