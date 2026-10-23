# Useful path models can remain wrong about every edge cost

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass22.
Graph potentials and reward shaping are the immediate ordinary comparators.

## Decision relevance without resolving the nuisance values

Fix a finite oriented graph with incidence matrix B (vertices by edges).
Let true edge costs be a and model costs b. If

    a-b = B^T*phi,

then every flow x with boundary B*x=d satisfies
a^T*x=b^T*x+phi^T*d. Hence all comparisons between flows with the same
boundary are exact under b. In particular, shortest-path choices for fixed
endpoints agree whenever the optimization problem is well defined. The
individual potentials and edge errors may remain unresolved, large, or
mathematically expensive. A proof of this structural relation can suffice
without computing their values.

This does not identify absolute route cost. Nor does it preserve comparisons
between different endpoints: phi^T*d then varies with the action. Two
one-edge routes to different targets already refute that extension. Negative
cycles and feasibility retain their ordinary optimization duties; the
potential relation itself preserves cycle cost exactly.

Equivalently, e=a-b is orthogonal to the cycle space ker(B). A cycle basis
provides m-n+c independent linear checks, where c is the number of connected
components of the underlying undirected graph. Potential representation is
necessary and sufficient for preserving EVERY signed-flow comparison with
fixed boundary. For a restricted directed route menu it is sufficient, but
need not be necessary. Do not silently strengthen that menu's requirement.

## Editing a few costs changes fewer independent obligations

Suppose the old potential-error relation is warranted, and a counterfactual
change to source and/or model alters their error vector by delta supported
on an edge set D. The new relation holds precisely when delta is orthogonal
to the projection of ker(B) onto coordinates D. The dimension of that
projected cycle space is

    k_D = |D| + c(G) - c(G without D).                         (1)

Proof: the kernel of the cycle-space projection consists exactly of cycles
of G without D. Subtract cycle-space dimensions:
(m-n+c(G)) - (m-|D|-n+c(G without D)). Thus a basis of k_D projected cycle
vectors gives k_D independent linear equality obligations for the edit.
When the graph remains connected after removing D, k_D=|D|. If D consists
of bridges, k_D=0: arbitrary error changes on those bridges are absorbable
in potentials and cannot alter same-boundary comparisons.

For a connected10-by10 grid, m=180,n=100 and the original cycle dimension
is81. Editing four edges whose deletion leaves it connected creates four
independent obligations instead of rechecking81 old basis cycles. This is
a reduction in equality count, not necessarily in source evaluations or
CPU time. Projecting the basis, acquiring delta and checking the inherited
certificate are paid. Ordinary incremental graph linear algebra matches
the result; a full recheck is not the strongest conventional control.

Under an exact linear-measurement oracle for otherwise arbitrary delta_D,
k_D independent scalar measurements are necessary in the worst case to
certify the new potential relation. Follow the transcript for delta=0.
With fewer measurements, their common kernel cannot be contained in the
kernel of the rank-k_D constraint map; another delta gives the same zero
transcript but violates the relation. This is an access-model lower bound,
not a lower bound against symbolic proofs or structured edit descriptions.

Deleting edges preserves the old relation by restriction. Adding edges can
be treated by extending potentials componentwise and checking the newly
created cycle constraints; an edge joining two formerly separate components
creates no such constraint. The edge semantics and endpoint duty must still
match the counterfactual request. Merely retaining the same graph identifier
does not establish this bridge.

## Contribution screen

The organizing lesson is useful fallibility: learn or prove the part of the
model error that cannot change the decision, instead of insisting on full
model correctness. This directly connects unresolved mathematical values,
fallible models and changed objectives. Graph reweighting already embodies
the basic idea. Retain the explicit edit obligation count and access-contract
distinctions as a possible application synthesis; do not claim potential
cancellation or incremental linear algebra as new mechanisms.
