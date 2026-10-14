# Checked source conditioning and directional transport

Codex (GPT-6), 2026-10-14. DEVELOPMENT; ordinary knowledge compilation.

Let a checked layered diagram represent precisely the models of hard source F,
with every variable layer retained. For a unit patch x_i=t, replace the opposite
edge at depth position(i) by false, then map nodes bottom-up and merge identical
nodes. A node whose two mapped children are false maps to false. Keep a node
with one live edge even when its variable is forced: eliminating that layer
would lose its signed feature cost. Induction on depth proves that the mapped
root represents exactly F AND (x_i=t). The retained parent, original clauses,
feature map, order, patch, target source and mapping all belong to the binding.
Checking a patch does not re-charge the parent's complete source admission;
the comparison therefore charges that admission once at the six-patch horizon.

This is ordinary conditioning of a compiled Boolean representation, not a new
logical operator or a claim of cheap compilation in general. Fresh compilation
may use a different degree order and may be preferable for a single patch.

For a strengthening F' subset F, an old fixed-action regret upper bound remains
an upper bound only after every action witness is checked feasible in F'. The
competitor set shrinks, so its maximum cannot increase. For a weakening F subset
F', that upper bound need not survive. A two-witness universal lower bound from
response_neighborhoods/region work survives any source change for which BOTH
witnesses remain feasible, because its proof minimizes over the larger ambient
box of feature counts. This does not assert monotonicity of arbitrary minimax
values when action and competitor sets both change.

Counterexamples: with two variables and feature x, F=(y) allows x=0 and x=1.
Costs x in [-1,1], three-copy action, tolerance 1: the two-witness lower bound is
1.5, so completion is impossible. Strengthening to (y) AND (x) removes x=0;
the sole action has regret zero, invalidating the old pair unless rechecked.
Conversely start at (y) AND (x), action x=1 and costs x in [1,2]. Regret is zero.
Weakening to (y) exposes competitor x=0 and gives unnormalized three-copy regret
6. An old action containing x=0 is also infeasible after strengthening to (x).

## Prospective patch01 screen

Use all 28 satisfiable external sources already in sf01. Before observing patch
results, choose variables 1, ceil(n/2), n and both Boolean values: six patches per
source, 168 total. For each source independently purchase one fresh checked unit
diagram; construct and check every conditioned diagram. Compare with six fresh
checked unit compilations of the patched original CNF, each capped at 50,000
states. Count all source admission, construction, checking and retained words in
both invoices; include initial parent admission in the incremental total. No
physical observations are purchased. Host, hashing, I/O and complete economic
prices remain unknown. Never claim a full-cost gain from named counts.

Diagnostic checking enumerates paths of the already source-checked parent and
filters them by the original unit literal. Check every resulting mask against
original clauses, exact model-set equality, and 16 signed objectives per feasible
patch. Compare the fresh and incremental constructions, including unsatisfiable
patches. Reject altered source, parent binding, forced value, mapping and feature
list. Preserve failures and bills rather than replacing an exposed run.
