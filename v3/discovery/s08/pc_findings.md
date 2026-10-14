# Proposed path-policy certificates: checked scope

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The [prospective certificate](path_policy_certs.md) was executed with
`python v3/discovery/s08/path_policy_certs.py v3/discovery/s08/pc01`.
[Design](pc01/design.json), [frozen code](pc01/impl.py) and
[results](pc01/results.json) retain all policies and upper tables.

All 72 small supplied policies (24 sources, three proposal rules) passed the
local upper-inequality checker and matched an independent full-history
rectangular adversary, with 3,624 adversary states. Six larger policies at
n=32/128 were produced and checked without full-history enumeration. Four
controls rejected a wrong source, out-of-interval root, negative bound and
underestimated continuation. These are conditional computations, with **zero
new physical source audits**.

The proposed shortcut of checking only lower extreme probabilities is unsafe
for an arbitrary heuristic. A four-node case with fees (10,1,1,1) gives a
correct worst-case bound **13**, while that shortcut gives **3**. Its
ordinary subinterval policy costs 11 but the forced-right alternative costs
1; increasing the chance of entering the ordinary branch raises the invoice.
This does not contradict the earlier monotonicity proof for an optimal
lower-probability policy, whose forced bounds dominate ordinary optima.

For n=128, production uses 247,552 named units and checking 345,984, shared
across the three root rules. Left and middle proposals use 8,128/16,256 named
units; the direct ratio scan uses 1,788,160. The latter proposer unnecessarily
rescans each interval, so the implementation does not demonstrate quadratic
**proposal** cost. A precomputed range-maximum representation could remove
that overhead; production/checking are already quadratic arithmetic counts.
Retained rational bit sizes, host work and all source acquisition remain
separate cost duties.

This establishes a checked compact upper-bill route for supplied policies,
including untrusted heuristic proposals, at the stated conditional-probability
interface. It does not yet execute a paid path service or establish novelty
over ordinary Bellman certificates and robust control.
