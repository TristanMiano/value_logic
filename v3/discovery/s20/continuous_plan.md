# Prospective continuous-loss check

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT after A1.
Freeze proof, implementation, this plan, saved inputs, runner, decision_cells.py
and lp_witness.py before execution. The first fixed input is the convex-loss
counterexample in continuous_gap.md, with exact bounds0 and13/4. Add three
three-action loss tables on knots[-2,-1,0,1,2], integer entries0..10 generated
by random.Random(2910). Use I={-1,0}, I empty, and I=[-1,0], respectively,
with O=[-2,2]. Store inputs before method exposure. No successful reruns.

For every ordered action pair on each affine piece, independently optimize
L_a(q)-w subject to w>=L_b(q), w>=l_b when known, and piece bounds on q.
Use exact primal/dual reconstruction from the existing LP witness producer.
Compare the maximum over these epigraph LP controls with the proposed
endpoint/crossing-point formula. Check every returned support witness.
The first fixture must attain B's gap at3/4; knot-only evaluation gives1,
so it is an explicit negative control for that shortcut. Reject reversed
knots, an outer interval beyond the loss domain and malformed row dimensions.
Record optimizer calls, candidate evaluations and excluded machine runtime.
