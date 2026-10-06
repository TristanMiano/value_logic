# F16 exact check — additional-source coherence gap

**Signed: ChatGPT (GPT-6 Astra Pro), delegated mathematical reviewer.**
2026-10-05 UTC. Principal time credit: **zero**.

**Disposition: verified.** The new §10 of
`v2/derivations/10_f16_coherent_recovery.md` gives an exact reset-model
counterexample under its stated additional convex source restriction. The
three laws, common old mean, moment directions, two radii, and realization
by one edited procedure are correct. No repair is needed for those claims.

Scope: unit old attempt prices, k=4, M=1, the stated exchangeable source,
and a decoded law required to satisfy the **augmented** source. I inspected
§10 and its following review-status paragraph only; I did not re-review
the separate upper/lower theorem. This check uses exact algebra, with no
experiment, search, execution of saved checks, or source/principal edit.

## 1. Verify the laws and old profile

For level masses q0,...,q4, the proper moments are

`m1=(q1+2q2+3q3+4q4)/4`,
`m2=(q2+3q3+6q4)/6`,
`m3=(q3+4q4)/4`, and `m4=q4`.

The uniform level law has moments `(1/2,1/3,1/4,1/5)`. Every old order has
mean `1+m1+m2+m3+m4=137/60`. Its level-cost vector is
`g=(1,5/4,5/3,5/2,5)`.

The displayed q_A,q_B,q_C have positive entries and numerator sums 200.
Direct substitution gives:

| Law | m1 | m2 | m3 | m4 |
|---|---:|---:|---:|---:|
| q_A | 101/200 | 203/600 | 1/4 | 19/100 |
| q_B | 101/200 | 1/3 | 51/200 | 19/100 |
| q_C | 1/2 | 203/600 | 51/200 | 19/100 |

These are exactly the stated proper-moment vectors with delta=1/200.
For each law, the sum of proper-moment increments is 2delta, offset by
the terminal decrease 2delta. Hence every old order still has mean 137/60.
As a separate arithmetic check, the g-weighted numerator of each law is
1370/3, which divided by 200 is 137/60.

The quoted Boolean inversion formulas also check directly. They map the
displayed moments back to the three stated level-mass vectors. Convex
combinations remain normalized nonnegative laws with the same full old
numeric profile.

## 2. Exact unrestricted and compatible-law radii

Subtract the baseline proper-moment vector and divide by delta. The image
of the additional source is exactly

`T=conv{(1,1,0),(1,0,1),(0,1,1)}`.

Every coordinate has attained endpoints zero and one. Any unrestricted
prediction therefore has worst coordinate error at least delta/2, while
the three coordinate midpoints attain that bound simultaneously. Thus

`R_free=delta/2=1/400`.

A law compatible with the additional source has normalized proper moments
z in T. Its exact worst sup-norm error is

`delta * max_i max(z_i,1-z_i)`.

Indeed each endpoint in each coordinate is attained by a source vertex,
and all other coordinate values lie between the endpoints. No common
vertex attaining all coordinate extremes at once is needed for this maximum.
Since sum(z_i)=2, some z_i>=2/3, giving radius at least 2delta/3.
The centroid `(2/3,2/3,2/3)` attains it. Its actual level law is

`q_star=(55,76,36,76,57)/300`,

the average of the three source vertices. It is a compatible probability
law, with proper moments `(151/300,101/300,76/300)` and terminal moment
57/300=19/100. Therefore

`R_compatible=2delta/3=1/300`,

and the ratio to the unrestricted radius is exactly 4/3.

## 3. One attempt-price edit observes every direction

Edit procedure 4's price by epsilon, keeping the outcomes, old prices and
M fixed. The following actual orders expose the indicated increments:

| Order | Revised mean minus its known old mean |
|---|---|
| (4,1,2,3) | epsilon |
| (1,4,2,3) | epsilon m1 |
| (1,2,4,3) | epsilon m2 |
| (1,2,3,4) | epsilon m3 |

Exchangeability makes the reached-prefix moment depend only on its size.
All 24 orders therefore introduce only these constants/three directions,
and all three directions really occur. Their old means are all 137/60.
The sharp radii for the complete revised-order vector are consequently
`|epsilon|/400` and `|epsilon|/300`. A strict gap requires epsilon!=0;
choose an edit with 1+epsilon>0 to remain in the intended price model.

## 4. Necessary meaning of compatibility

The gap requires that a law-valued answer satisfy the **new triangle
restriction**, not merely be some probability law in the original old
fiber. This condition is present in §10 and should remain explicit.

In fact the unrestricted midpoint proper moments are realized by the law

`q_free=(75,96,56,96,77)/400`.

It has old mean 137/60 and proper moments
`(1/2+1/400,1/3+1/400,1/4+1/400)`. Its terminal moment is 77/400,
whereas every law in the triangle has terminal moment 76/400. Thus it
belongs to the original old-summary fiber but violates the additional
source restriction. This explicitly demonstrates why there is no
contradiction with a no-penalty theorem for the unrestricted old fiber.

If exchangeability were dropped and only level-count information plus
one old order mean were retained, the three-dimensional query image would
not follow automatically. Here the specified exchangeable source suffices;
equivalently, retaining the full unit-price profile with all old order
means equal enforces the same within-level symmetry of moments.

The earliest dependency examined is the new §10 source-relative output
claim. No earlier radius, frozen finite result, or native soundness premise
is changed by this successful check.
