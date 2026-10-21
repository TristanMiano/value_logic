# A quick screen of logically related invoice facts

Codex (GPT-6), DEVELOPMENT, October21,2026. The full-cube n*beta bound does
not automatically price a source with known logical relations. Consider
four independent latent fair bits and seven queryable facts with forms
1,2,4,8,9,10,12 (bit masks for linear forms over F2). The target is form7.
Its shortest expression as an XOR of queryable facts has length3. Exact
answer acquisition must query at least that many facts on every full
answer path, but this alone does not prove a3*beta invoice lower bound.
The structured edge packing from structured_edges.md can be weaker than
the shortest support, so replacing n by that support is a new conjecture,
not an imported theorem.

Prospective screen: enumerate every distinct cap-three query-count map on
this16-world source, then solve the exact public-state Bellman recurrence.
At depth3 the final private answer cannot change the invoice, so each
root-answer branch either stops at1, always ends at2 or3, or tests one
other fact to choose2 versus3. These finitely many branch maps exhaust the
allowed count maps; dummy queries have paid unit cost. Ignore no-op public
partitions, which only add positive fees. For a uniform residual world set W,
store the integer total fee over W, with recurrence

    C(W)=min_maps [sum_k k*|W_k| + sum_k C(W_k)].

Parity-homogeneous W have C0. This is an exact finite ordinary oracle,
not an efficient general method. Initial budget: under60seconds and one
source at zero reset fee. Compare against3*beta(3,0)=7/2 only as a
conjecture screen. Preserve any failure or timeout; do not expand a search
merely to obtain a favorable number.

The first execution completed in16.9454862s:669 count maps,19887 public
states and3908282 distinct examined splits. Its exact expected optimum
was60/16=15/4, above the conjectural7/2 lower bound. It neither refutes
nor proves the source-general conjecture. In this particular source the
three latent coordinate directions already give a feasible weight-three
packing in structured_edges.md: each queried form contains at most one
of those coordinates. Thus7/2 is in fact certified for this panel by the
existing packing argument. This makes the panel less informative about a
possible packing/integral-support gap than the initial motivation suggested.
Retain that selection weakness rather than presenting the run as evidence
for a new general theorem. No further expensive oracle expansion is selected.
