# Cohort hulls make retained proof stitching callable

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT; same-model auxiliary synthesis. No helper time enters the
principal clock. This note records the completed
[cohort hull constructor](cohort_hull.py), [chronological replay](hull_replay.py),
[hull result](hull_results.json), and separate [vertex probe](vertex_results.json).
The derivation and historical result files remain unchanged.

The constructive result is a small exact hull for every observed cost state
in the executed four-arm trace, together with a stronger fixed-action
certificate on three recorded prefixes. It establishes usable certificate
arithmetic on admitted evidence. It does not establish a controller or
total-cost advantage.

## 1. Six initial generators cover the eight-row source

The declared common cost source has eight fixed rows, each initially allowed
one of the same six public eight-coordinate modes. Target costs in these
implementations are **cohort sums**. Replacement price 48 and tolerance 4
correspond to mean price 6 and mean tolerance 1/2.

For each row i let `Q_i` be the mode set still compatible with its checked
audit receipts. The convex hull of all compatible cost sums is
`W=sum_i conv(Q_i)`. Group rows with identical allowed-mode sets into types g
with counts `n_g`. Then

```text
W = sum_g n_g*conv(Q_g)
  = conv{sum_g n_g*m_g : m_g in Q_g}.
```

The initial state has one type with count eight, so the six public modes
scaled by eight generate its exact hull. Enumerating the 6^8 possible row
configurations is unnecessary. This is an algebraic consequence of the
declared rowwise admissibility constraints, with no stochastic independence
or population assumption.

`cohort_hull.generators(modes, possible, meter, max_generators=256)` constructs
the group product, removes duplicate generated vectors and retains their
mode-choice provenance. It makes no claim that every retained point is an
extreme vertex. Row IDs and their actual observation histories remain
distinct: grouping is a certificate computation, not a license to merge
future cell-audit outcomes.

Across all observed states, the largest group product was 144 and the largest
distinct generating set was 72. These are observed limits, not general
complexity guarantees. The construction quotes the product before allocating
its generators and returns unresolved if the declared cap is exceeded. The
focused cap check set the initial cap to five: its six-point product correctly
returned unresolved with no partial hull certificate.

## 2. Reconstruct the bank available at each actual prefix

The replay begins with an actual raw-checker admission of the original cache:
29 witnesses and 18 lower-proof trees, bound exactly to the compact projection
and historical source archives. It then walks each executed arm in order,
rechecks that arm's recorded cost observations and logical receipts, and adds
each checked result only when it originally became available. It re-admits
21 later witness receipts and 47 later branching lower proofs and rechecks
59 historical audit receipts across the four arms. It checks the final
observed source states and retained banks against the executed trace.

There are **191 request/event certificate states**: 64 request starts plus
127 already recorded events. At each state the replay evaluates the same
admitted candidates and proof bank over the exact generated cost hull.
The single-proof hull calculation reproduces the recorded direct-support
certificate bound. The stitched calculation can select a different checked
lower proof for each generator, while retaining one fixed output action over
the whole hull. Its bound never increases.

| Historical arm | Request/event states | Hull states within arm | Largest group product | Most distinct generators | Strict prefix improvements |
|---|---:|---:|---:|---:|---:|
| `shared_deficit` | 46 | 17 | 48 | 48 | 0 |
| `audit_first` | 43 | 15 | 18 | 18 | 0 |
| `logic_first` | 48 | 15 | 18 | 18 | 1 |
| `certificate_directed` | 54 | 16 | 144 | 72 | 2 |
| Total / maximum | 191 | 63 arm-local states | 144 | 72 | 3 |

All observed hull constructions completed under the 256-product cap.
The 63 count sums the separate arm-local caches; it does not assert 63
globally distinct cost states.

The three strict cases are narrowly identified in the saved result:

| Arm and recorded event | Logical row/request | Distinct generators | Single-proof bound | Stitched bound |
|---|---:|---:|---:|---:|
| `logic_first`, after event 29 | 13 | 3 | 6 | 4 |
| `certificate_directed`, after event 34 | 13 | 5 | 6 | 4 |
| `certificate_directed`, after event 35 | 13 | 3 | 6 | 4 |

These are zero-based saved identifiers. All three retain the same checked
repair, model/mask 132, and reach the sum-scale tolerance four. In mean units,
the bound changes from 0.75 to 0.5. Each uses two distinct admitted proof
receipts across its generators.

These are three prefix comparisons concerning one logical row across two
arms; they are not three newly answered requests. Two are successive states
of the same request. No historical acquisition decision was rerun under the
stronger gate, and no recorded purchase was canceled. Continuing from an
earlier stop would change later cost observations, proof banks and controller
state, so savings cannot be inferred by deleting later receipts from the
historical invoice. The exposed trace provides a useful development case,
not fresh validation.

## 3. The scalar-anchor bridge is a separate usable route

As proved in [the vertex derivation](vertex_derivation.md), the true clipped
optimum `Cbar(w)=min(p,min_z z dot w)` is concave. If `W subseteq conv{v_h}`
and a checked scalar `ell_h<=C*(v_h)` exists at every generator, one fixed
admitted action a has uniform regret at most

```text
max_h [action_cost_a(v_h)-min(p,ell_h)].
```

Every anchor may use a different independently checked proof. The same
action must cover every anchor; the certificate cannot choose the repair
using the unobserved true cost vector. Hull containment and the common
logical source are essential premises.

The chronological hull replay uses existing repricable tree profiles; it
does not purchase scalar RUP bounds at the cohort generators. The separate
vertex probe demonstrates the scalar route with two actual bounded RUP
calls: hard clauses force `z=(1,1)`, `p=2`, and the cost hull is generated by
`(1,0)` and `(0,1)`. Each anchor has checked lower bound one. A single weak
repricable proof leaves bound one, whereas the two scalar anchors certify
zero regret over the entire segment. This anchor certificate requires no
full Boolean-objective-mask projection.

The source, variable/objective ordering, anchor weights, integer scaling,
bounded-query meaning and raw proof/checker dependencies must be admitted.
A checksum or native optimum/UNSAT status alone supplies none of these
obligations. A missing anchor, a failed checker or an unestablished hull
containment leaves that certificate unresolved. The tiny anchor source and
the eight-row historical source are separate evidence scopes.

The one-row six-mode audit-planning rehearsal in `vertex_results.json` is
also separate. On its 16 original cache banks, all 1,008 nonempty-subset
comparisons had equal stitched and single-proof bounds, and every request
had an uncovered singleton mode. Pure auditing therefore could not guarantee
completion with that bank. The later chronological hull replay adds each
arm's actual newly checked proofs and cost observations, which explains why
it can expose strict prefix cases absent from the initial-bank rehearsal.

## 4. Costs, timing and scope

The hull replay made **zero new provider, native or audit calls**. Previously
acquired results were read and checked again, not billed as new acquisitions.
The executed operation invoice is:

| Current replay work | Declared units |
|---|---:|
| Initial raw admission and compact-cache binding | 92,969 |
| Replay input reading and hashing | 441,779 |
| Hull state lookup, grouping, product quote and construction | 99,583 |
| Vertex/proof arithmetic, compilation and region queries | 556,839 |
| Historical cost and logical receipt admission/checking/retention | 18,433 |
| **Total current replay** | **1,209,603** |

The result records **0.207500820 seconds wall time** and **0.756272177 seconds
process time** for this replay. These measured values and operation tariffs
describe different quantities; neither is a runtime model inferred from an
optimum value. The 768,544-byte result preserves hashes, hulls, source states,
chosen actions, anchor proof IDs, prefix comparisons and detailed invoices.
Serialization, allocation and native memory are not fully economically
priced, and the transcript's historical acquisition invoices remain intact.

The separate tiny vertex experiment made two new bounded RUP calls. Their
encoding/checking subtotal is 963 declared units **excluding native search**,
whose operation tariff is unresolved; the vertex result separately records
its admission, arithmetic and measured times. Those calls are not part of
the zero-call hull replay, and their subtotal is not a complete economic
quote.

Reconstruction commands are recorded here for portability; these result
writers refuse to overwrite an existing output:

```text
python v3/discovery/s06/vertex_probe.py NEW_VERTEX_OUTPUT.json
python v3/discovery/s06/hull_replay.py NEW_HULL_OUTPUT.json
```

The first command would make new bounded proof calls. The second purchases
no new source observations or logical search, but performs paid re-admission
and arithmetic. This synthesis only read the existing executed evidence.
The useful next integration is a common controller gate that can invoke this
hull certificate at a stated compilation cost, retaining the same evidence
and purchase opportunities for every comparison arm. This hour's results
support that construction without asserting net savings or readiness.
