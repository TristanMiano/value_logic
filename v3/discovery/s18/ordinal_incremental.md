# Lower update cost using ordinary dynamic strongest paths

Codex (GPT-6), s18 DEVELOPMENT. This is an implementation refinement of
the raw-count adapter, not a new dynamic graph algorithm or an added
requirement for O18-M/v1.

Keep the raw-count strongest-path matrix p, with p_ii=+infinity as the
zero-length path convention. If only edge a->b increases to capacity w,
then for all i,j,

    p'_ij = max(p_ij, min(p_ia, w, p_bj)).                (I1)

Use the old column p_ia and old row p_bj. A new optimal simple path either
does not use that edge or uses it once, proving the upper bound. Conversely
the concatenation of old prefix, new edge and old suffix is a valid walk;
removing cycles cannot reduce its bottleneck, proving attainability. If
w<=p_ab already, no path entry needs to change. This ordinary edge-increase
formula takes O(d^2) elementary operations. Topological extension also
takes O(d^2), so the pair-only named-alternative method needs quadratic,
not cubic, path-and-ranking work per round.

Do not apply (I1) unchanged to winning-edge capacities: an increased reverse
count can delete a previous winning edge. Raw counts are monotone and have
the same proved mistake guarantee, so they are the appropriate variant here.

For matroids, it suffices to update only the pairs of the ordered matching
between A\B and B\A in matroid_feedback.md. Every such comparison is true
on a good round, and at least one is strict on a mistaken good round.
Find that matching using the at most r^2 candidate exchanges between the
two basis differences, where r=|A\B|. The Hall proof ensures it exists
even when the reported feasible basis A is corrupted. Use ordinary
bipartite matching, then perform r raw edge increases by (I1).

With a basic augmenting-path matcher this gives O(r*d^2+r^3+d^2)
elementary graph work, at most r^2 exchange-oracle calls, and at most d
greedy independence queries. Since r<=d, this retains the original cubic
worst-case bound and can be smaller for low-rank or small-difference duties.
Recording the full exchange set remains a valid stronger-information option.
This is an algorithmic bound, not measured total CPU savings; acquiring
feedback, representing bases and exact integer costs remain payable.

Prospective small check: compare (I1) after each of25 edge increases on
20 deterministic random traces for each dimension2..8 with full max-min
Floyd closure. This checks the implementation identity, not the universal
mistake proof or contribution novelty. Preserve the source and output.

The frozen [checker](path_update_check.py) passed all3,500 updates on140
traces, performing101,500 incremental matrix-entry updates. Python3.12.14;
elapsed139,546,900ns; source SHA256
cd44bc69b8062394951c198ad0ad8978242cb37007e91c040f105d5700dc2e67.
The [result](path_update_result.json) is a crosscheck against full closure,
not a measured comparison of complete decision costs.
