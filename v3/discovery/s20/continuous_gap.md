# Continuous-loss version of the computation-gap certificate

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT; a separate consequence.

Let I subset O be compact scalar sets, with O nonempty, and let finitely many
loss functions L_a be continuous on O. The exact but incompletely computed
range R is some nonempty compact set between them. Put l_b=max_I L_b when
I is nonempty, and l_b=-infinity otherwise. The largest possible robust
suboptimality of a fixed action a is

    Gamma_a=max(0,max_(b!=a) max_(q in O)
                   [L_a(q)-max(l_b,L_b(q))]).                 (G1)

This is the continuous version of refinement_gap.md. For any R, choose q
attaining max_R L_a; its competing worst loss is at least both l_b and
L_b(q). Conversely a maximizing pair(b,q) is realized by R=I union{q}.
Compactness and continuity ensure all maxima exist. For one action Gamma=0.
Thus the bound has a witness requiring at most one additional possible value
besides I. This witness is valid for the interval bracket, not automatically
for the original receipt geometry. With bounded discontinuous losses one can
state an analogous supremum result, but attainment is then an extra premise.

For rational continuous piecewise-affine losses on a common finite knot grid
and finite rational interval unions I,O, (G1) is exactly computable. On a
piece where L_a and L_b are affine, its inner expression is the minimum of
two affine functions. Its maximum occurs at a piece endpoint or at a point
where L_b(q)=l_b. Split also at the interval endpoints of O and the loss
knots. All these candidates are rational. When I is empty the expression is
simply L_a-L_b on each piece, requiring only endpoints. Computing l_b requires
the endpoints of I and its contained loss knots. This is ordinary exact
piecewise-linear optimization, not a new algebra or generic novelty claim.

## An endpoint-only shortcut fails even for convex individual losses

Take O=[-1,1], I={-1,0},

    L_A(q)=max(-9q,12q),   L_B(q)=10+3q.

Both losses are convex. The known worst-loss vector is(9,10), and the outer
worst vector is(12,13), so the old separate bounds are eta_A=2, eta_B=4.
For A, L_A(q)-max(10,L_B(q)) is always at most-1, giving Gamma_A=0.
For B, on[-1,0] the expression is1+3q. On[0,3/4] it is also1+3q;
on[3/4,1] it is10-9q. Consequently Gamma_B=13/4, attained at q=3/4.
The compatible range R=[-1,3/4] has worst losses(9,49/4), giving that gap.

Checking only the supplied loss knots{-1,0,1} would report at most1 for B
and be unsound. This does not contradict endpoint sufficiency for the worst
loss on a **known** fixed range. Here the uncomputed range may have a new
endpoint at3/4, where one action's possible loss meets its already witnessed
maximum. The calculation retains dependence between those extrema.

This permits the same fixed-model stopping rule with a continuous loss duty,
without first computing the entire range. It does not estimate real-world
loss probability or observation value. The incumbent-baseline qualification
for observation remains as stated in incumbent_value.md. Standalone novelty
UNASSESSED; no change to V19's fixed contribution event.
