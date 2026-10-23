# Nonuniform prices in the all-target graph warrant

Codex (GPT-6), DEVELOPMENT, October 22, 2026. Constructive derivation;
uses ordinary cycle-basis support-vector machinery.

For an undirected simple graph with nonnegative edge prices, define the
price of a simple cycle C by w(C)=sum c_e-max c_e. Every edge may be a
prediction target. A basis minimizing the SUM of these cycle prices has
the threshold property: its cycles of price <=B span every such cycle.
The exchange proof in budget_warrants.md works for any fixed cycle weight.

Here is a polynomial oracle for finding a cheapest cycle with odd inner
product against a supplied edge-label vector z. Enumerate an edge e as a
possible maximum-price edge of that cycle. In G-e discard edges with
price greater than c_e. Find a cheapest endpoint-to-endpoint walk with
z-parity 1-z_e, using the ordinary two-layer parity cover and nonnegative
shortest paths. Join it to e. A finite shortest path in the cover need
not be simple in the original graph, but the resulting closed walk has
odd z-parity. Decompose it into simple cycles; at least one has odd parity.
Choose an odd component of minimum w.

Every returned component has w at most the path cost. If it contains e,
subtracting its largest price removes at least c_e; if it does not, its
entire edge cost is at most the walk's non-e cost. Multiplicities can be
removed by the usual closed-walk cycle decomposition. Conversely an
optimal odd simple cycle appears when one of its maximum-price edges
is enumerated, giving a path cost exactly w(C). Therefore the least
returned component is an optimal odd cycle. Zero prices and equal
maxima cause no change; the cover's path routine must return a finite
simple path in cover-state space, not cycle forever on zero edges.

## From the oracle to one basis for every budget

Let q be cycle-space dimension. Maintain a basis of linear functionals
on that space annihilating the already selected cycles. Pick a nonzero
one z, use the oracle to select a cheapest cycle C with z*C=1, and
eliminate z*C' from the remaining functionals by ordinary binary row
operations. Repeat q times.

Exchange proof: assume an optimal basis contains all earlier selections.
Expand the new C in that basis. Since z*C=1 and z vanishes on earlier
selections, some unselected basis element D with nonzero coefficient
has z*D=1. Replacing D by C preserves a basis and cannot raise its price,
because the oracle chose a cheapest z-odd cycle. Induction preserves an
optimal basis containing every new selection. This is the standard
support-vector proof, with our nonadditive cycle-price oracle substituted.

An elementary implementation uses q*m shortest-path calls on covers with
2n vertices and O(m) edges, plus cycle extraction and binary elimination.
This is a polynomial construction, not a new asymptotically optimized
cycle-basis algorithm. It prepares all receipt-price budgets at once.
Actual edge-value receipts and source/version checks are still paid.

This easy oracle is justified only when ALL edges may be targets.
For restricted targets, an odd walk can decompose into a non-target odd
cycle, invalidating the same extraction step. See target_warrants.md.

## Positive validation still has an observation lower bound

Let U be the union of supports of the equations generating a warrant W.
On a world x in W, a deterministic exact coordinate-query algorithm
that accepts membership must observe every coordinate in U. Otherwise
flip an unqueried coordinate i occurring in a generating equation. The
transcript is identical and the changed world is outside W. Randomness
does not avoid this requirement for each zero-error accepting transcript.
Conversely, observing U suffices, followed by parity checks.

A basis can reduce algebra and duplicate work but not the total distinct
coordinate receipts needed to positively validate this exact event.
Partial calibration savings therefore need U to be substantially smaller
than the complete model's support, or a different priced measurement
interface. Early rejection may be cheap. Do not infer cheap all-pass
calibration solely from having few basis equations.
