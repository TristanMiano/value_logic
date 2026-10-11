# Independent source review of joint report geometry

Signed: **ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction**  
UTC: 2026-10-11T15:54:36.862446+00:00  
Reviewed draft SHA-256: `207b74d3554f0bb297bf8d25aecf673c5264b98a1bb97d34e90df798c6e3e93d`  
Disposition: **The affine and convex-geometric claims pass on the stated binary-key relaxation. Clarify the polygon direction convention and degenerate vertex bound before implementation.**

This is a source and mathematical review of the principal's draft, frozen reporter, frozen metric implementation and frozen protocol. Exact source snapshots and hashes accompany it. No official worker or observer was executed, no final payload was reread, and no new CNF truth was generated. This review adds zero principal research-clock credit.

## Exact targets and the public shift

The frozen `_metrics` uses `emitted_q` for issued Brier loss and `terminal_action` for realized binary error. The reporter admits a completed parent, validates exactly one selected row per block against its successful checked invoice, preserves the issued dyadic, and requires the selected terminal action to equal the purchased label. Those definitions support the draft's F, V and Z.

The identity `(q−y)^2 = q+(1−2q)y−q(1−q)` for binary y proves the stated public shift exactly. In its notation, **S means the current selected-and-successfully-completed purchase positions**, not every position whose key has a known receipt by episode end. An unselected repeated key remains outside S, even when an earlier receipt makes its contribution known; this does not prevent substituting its known label later. An issued forecast is not rewritten when a receipt arrives. No fair-bit assumption is needed for the identity as arithmetic; interpreting V as a conditional expected terminal count retains the original independent-action-bit premise.

The exact feasible sets for F and V are translates by C, so their sharp key-relaxation marginal widths agree. This alone does not force arbitrary separately produced confidence intervals to have equal widths: differing clipping or conservatism can change their widths. Preserve any equality of the frozen intervals as its separately checked observation, not as a theorem about every interval construction. A nontrivial rectangular display permits impossible F–V pairs unless the relation F=V+C is enforced.

## Binary-key relaxation, support, and corners

For a fixed recorded binary terminal action a, the per-position coefficients are

- F: constant `q²`, label coefficient `1−2q`;
- Z: constant `a`, label coefficient `1−2a`.

Grouping complete canonical semantic/source/content keys within the validated episode and substituting all its sound paid labels gives the stated rational A and b vectors. In particular, the end-of-episode known-key set must be built from that parent's checked receipts with full identity/scope validation; it is distinct from the chronological hard-before mask. The full-key cube is an outer relaxation of actual mathematical truth consistency. Different CNFs can impose relations absent from this abstraction, and the record's fixed forecasts/actions are not counterfactual reexecutions under alternate labels.

The convex-hull identity follows because the cube is the convex hull of its binary vertices and affine maps commute with convex hulls. For each direction, independently choosing a label at the appropriate endpoint proves both support formulas and attainment by a binary relaxed assignment. Consequently every stronger excluded linear bound would remove some point allowed by this abstraction. It is not a lower bound on what additional public logical reasoning could establish or on the price of doing that reasoning.

The coordinate-corner sign criterion is necessary and sufficient **within this same relaxation**. To reach a coordinate's extremum, each nonzero summand must attain its own corresponding extremum; one cannot compensate for another summand falling short. Reversing coefficient signs handles minima, and zeros impose no constraint. Logical consistency may remove even a compatible relaxed corner. The draft's one-key example, `(1/16,1)` versus `(9/16,0)`, is exact.

## Required polygon specification

**G1 — specify one horizontal boundary ray.** “Closed upper half-plane” alone includes both `(1,0)` and `(−1,0)`. Cross products then cannot distinguish their angular order, and blindly combining parallel vectors can collapse their nontrivial segment to zero. Use the canonical half-plane

`dy > 0 or (dy == 0 and dx > 0)`.

Discard zero vectors first. When the condition fails, replace b by −b and shift A by the original b; the equality `[0,b] = b + [0,−b]` proves preservation. All remaining parallel generators are codirected. Exact cross-product ordering on this half-plane, combining zero-cross-product ties, then following the sorted edges followed by their negatives in the same order gives the convex boundary. No floating-angle tolerance is required.

**G2 — specify degeneracy and vertex counting.** Let m be the number of nonzero canonical directions after merging. For m≥1 the hull has at most 2m distinct vertices, excluding a duplicated closing vertex. For m=0 it is one point, so the unqualified bound “at most twice as many” needs that explicit exception. For rank one retain the two segment endpoints and zero polygon area. Detect affine rank independently of bounding-rectangle area: a slanted segment has positive rectangle area but is still one-dimensional; an axis-aligned segment has zero rectangle area. Report any area ratio with a zero denominator as unavailable, not infinity or an invented value. Coincident rectangle corners must not be counted as distinct geometric points.

After those conventions, the construction and every vertex's binary attainability are correct. A sufficient implementation audit compares its exact support against the direct formula in every distinct polygon-edge normal, along the coordinate axes, and in additional fixed diagnostic directions; verifies orientation/closure and the degenerate branches; and retains full source bindings. A few arbitrary directional checks alone are useful diagnostics but are not a proof of polygon equality. Later containment should read the already independently checked targets only after saving the public construction, as the draft states.

## Confidence and economic boundaries

The proposed region is deterministic for the chosen abstraction and assumes sound, correctly bound receipts. It does not make an MT cohort a fair-bit experiment. Intersecting it with an already valid joint confidence region preserves that region's original confidence event and assumptions because the deterministic region contains the true point on every admitted path; it requires no independence between the two regions. Merely combining several marginal levels does not create a simultaneous level without the original joint theorem or a justified multiplicity rule. The frozen protocol already states its joint fixed-end theorem's fair-bit, propensity and all-path funding premises; keep those premises explicit.

The draft correctly distinguishes this post-outcome public-information calculation from the paid reporting worker and its frozen A5 result. A smaller relaxed region, better containment visualization or sharper algebraic interval supplies neither a newly purchased receipt nor a demonstrated economic improvement. Representation construction, storage and verification would have to be paid in any deployed alternative. The unknown-prefix global economic gate remains unchanged. No new empirical coverage, feedback-policy or prospective-selection claim follows.

## Conclusion and closure condition

The load-bearing algebra, relaxed sharpness, corner criterion and interpretation boundaries are sound. G1 and G2 are small specification corrections to make before coding; the selected-position definition and scope of equal-width wording are useful explicit qualifications. An additive correction can close this source review while preserving the original draft hash. No result or official execution needs modification.
