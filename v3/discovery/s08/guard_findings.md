# Joint-guard development result

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The [prospective construction](joint_guard.md) was executed by
`python v3/discovery/s08/joint_guard.py v3/discovery/s08/guard01`.
The [frozen source](guard01/impl.py), [design](guard01/design.json) and
[complete results](guard01/results.json) retain the inputs and certificates.
All 32 initial small trees and 112 compatible single-node refinements agreed
with exhaustive source enumeration. These refinements are conditional
calculations: **zero physical cost audits** were performed.

The exact joint bound was smaller than the sum of separate edge bounds on
4/32 initial cases, and smaller than the sum of separate oriented-component
bounds on 11/32. This is a representation benefit over those two relaxations,
not a new maximum-sum algorithm or a full-cost comparison.

| Tree nodes | Exact guard | Edgewise bound | Oriented bound | Producer units | Checker units |
|---:|---:|---:|---:|---:|---:|
| 32 | 56 | 60 | 80 | 825 | 954 |
| 128 | 246 | 270 | 316 | 3,209 | 3,690 |
| 512 | 863 | 969 | 1,087 | 12,557 | 14,500 |

The large cases used checked local upper inequalities plus a compatible
attaining assignment. They were not exhaustively enumerated. Named units
include graph/support admission and the indicated arithmetic; general host,
serialization and retained-byte costs are not claimed to be completely priced.
Four controls rejected an underestimated message, a nonattaining witness,
a certificate for another source and a cyclic graph.

The unit triangle has bounds 6, 3 and 2 at the oriented, edgewise and full
joint scopes. A source-dependent guard can thus benefit from retaining
correlation, but computing it on an arbitrary graph contains weighted maximum
cut. The next constructive question is how **changing the selected action**
after an audit differs from retaining a fixed map and recomputing its guard.

No new readiness event or promotion follows from these finite checks.
