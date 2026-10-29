# Partial evidence: first development result

Codex (GPT-6), October29,2026 UTC. Separate DEVELOPMENT after A1.
The frozen [panel](partial_plan.md) passed on its first execution:
[a01](partial_runs/a01/result.json). No successful panel was rerun.

Six exposed control problems,20 local cells and538 query answers preserve the
inner/exact/outer sandwich at every tested update. All86 attainable answers
have rational original-source witnesses checked directly. Seventeen invalid
operations were rejected without changing evidence state. Separate controls
check one-receipt upper support, two-receipt strict Farkas support and opposite
directions for bound versus point reuse. Seven transformed inputs are rejected
because this prototype requires explicit coordinate bounds; general compact
polytope support is not claimed for its constructor.

The noisy-envelope query[-5/4,-6/5] changes from UNRESOLVED to EXCLUDED after
box propagation and before any local complete certificate is delivered.
This takes134 row visits and28 coordinate-bound updates across eight cells,
with **zero optimizer calls**. Its outer range is already the exact two-piece
image, but the service correctly declines to label the range exact until an
inner source construction also covers it. Under the fixed block/mask order,
seven of eight supplied complete certificates suffice for global equality.
The panel deliberately supplies the eighth too to check monotonicity.

For the other cases, first global equality occurs after1/1,1/2,1/1,0/4 and3/4
delivered certificates, respectively. The0/4 case is an inconsistent constant
observation proved by box checking, not an unattained nonempty range. These
counts are quantities of **reused existing certificates**, not measurements
of new LP work, audit fees, or deployment savings.

The cost record includes1172 interval-table compilations,231 row visits,
30 coordinate updates and6199 retained evidence bytes across the six cases.
The many compilations include the diagnostic
query panel and are not a proposed efficient calling policy. The entire panel
took61,632,400ns in this execution; that is excluded machine time, not a
comparative speed result. The ordinary same-algorithm implementation ties.

Records SHA256:
`5dce23f4b31644a76257f1f9fd8fa31bd2eac48e5f5151f64269740996aa62c3`.
Freeze SHA256:
`1d4f108e86c4f6b7b14fc5a90d59c8a9422f04632a34fb92f43056f762190c18`.

## Why the zero-LP exclusion works here

Write the two blocks as(x_i,y_i) in[0,1]^2 with sums in[1.19,1.21] and
[1.79,1.81]. The receipts require max_i x_i>=.99 and max_i y_i>=.99.
Neither block can witness both: its sum would be at least1.98. Thus only the
two split assignments survive. In the first block, assigning x gives
x in[.99,1], y in[.19,.22]; assigning y gives x in[.19,.22], y in[.99,1].
In the second block the corresponding free coordinate lies in[.79,.82].

For f_i=.5*x_i-1.5*y_i, the first-block assigned-x image bounds are[.165,.215]
and its assigned-y bounds are[-1.405,-1.375]. The second-block bounds are
[-.735,-.685] and[-1.105,-1.075], respectively. Each endpoint is attained
by the compatible corner of the appropriate sum strip. The split-product
minimum therefore has the two components

    [-281/200,-11/8] union [-221/200,-43/40].

The query[-1.25,-1.2] lies strictly in the gap. Bounds propagation plus the
receipt partition structure already excludes it. This example consequently
supports a useful incomplete-evidence interface, **not a necessity claim for
LP optimization**. A conventional tailored calculation has the same zero-LP
answer, and a single-band task may be cheaper still.

## Scope and next uncertainty

The general sandwich proof, strict unknown/empty distinction and rational
witness construction are in[partial_ranges.md](partial_ranges.md). The finite
panel supports the implementation only at its enumerated scope. It does not
prove arbitrary-input code correctness, producer completeness, optimal query
selection or standalone novelty. Failure recovery preserves the last sound
state but does not guarantee progress. This extension is available for a
later contribution assessment and does not change the completed V19 event.
