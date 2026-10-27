# Anchored reconstruction of the complete attainable value set

Codex (GPT-6), October 26, 2026. DEVELOPMENT; new derivation within s19.
This improves the interval-union recurrence in [value_sets.md](value_sets.md).
The old executed source and outcomes remain unchanged.

## Input and proposed bounded claim

There are n >= 1 independently uncertain vectors x_i in nonempty compact
rational polytopes B_i. Dimensions may differ. For each retained observation
j in K={1,...,k}, affine rational functions g_ji describe the response of
configuration i. The observation says

    a_j <= min_i g_ji(x_i) <= b_j, with a_j <= b_j.

Exact old optimum values are the special case a_j=b_j. For a new objective,
let f_i be affine rational functions and V(x)=min_i f_i(x_i). The desired
output is the entire set of possible V, including every gap, and a source
witness for every requested attainable rational value. No distribution over
x is assumed. The unknown vectors must be the same across observations.

Define the compact convex local slice

    Q_i(T) = B_i intersect {g_ji >= a_j for every j}
                    intersect {g_ji <= b_j for j in T}.

For each nonempty Q_i(T), two LPs give ell_i(T)=min f_i and u_i(T)=max f_i,
with extremizers. Empty slices are unavailable. At most 2*n*2^k LP calls
are needed, including infeasibility detection. These are ordinary rational
linear programs; their bit complexity and storage are not unit-cost freebies.

**Proposed claim:** after these local LPs, an exact union of at most n*2^k
closed intervals can be constructed with

    O(n*3^k + n*2^k*log(n*2^k)) rational comparisons

and O(n*2^k) scalar table storage, in addition to the input and retained LP
witnesses. The algorithm detects inconsistent observations and recovers a
consistent source for every value it returns. This replaces the earlier
conservative O(n^2*4^k*(log(n+1)+k)) interval-propagation bound. It is a
worst-case algorithmic bound, not an observed wall-clock speedup.

## Outside-generator bottlenecks

For any index set of generators I and observation subset S, define

    U_I(S) = max over disjoint partitions (T_i : i in I) of S
                 min_(i in I) u_i(T_i).

Only partitions with all slices nonempty are permitted. Use -infinity for
no feasible partition. For no generators, U_empty(empty)=+infinity and
U_empty(S)=-infinity otherwise. Nonempty generator sets have finite feasible
bottlenecks because their polytopes are compact.

Compute prefix tables P_i(S)=U_{1,...,i}(S) and suffix tables H_i(S)=U_{i,...,n}(S).
The prefix recurrence is

    P_i(S) = max_(T subset S) min(P_(i-1)(S minus T), u_i(T)),

with unavailable terms omitted; the suffix recurrence is analogous. Store
an attaining split for every finite entry. Across all subsets, a layer has
3^k split candidates. Then for each anchor i compute

    U^(-i)(S) = max_(A subset S) min(P_(i-1)(A), H_(i+1)(S minus A)).

This is another n*3^k split scan. An attaining split and the prefix/suffix
backpointers recover the outside partition and its local maximum witnesses.

## The interval formula and proof

For each available anchor slice (i,T), form

    J_iT = [ell_i(T), min(u_i(T), U^(-i)(K minus T))],

omitting the interval when its upper endpoint is smaller than its lower
endpoint or the outside partition is infeasible. The exact attainable set is

    V(X) = union_(i,T) J_iT.                         (AR1)

First take any consistent source x. For each old observation choose one
configuration whose response is at most b_j, and assign j to it. This gives
a partition T_1,...,T_n with x_i in Q_i(T_i). Choose an anchor i attaining
the new minimum q=V(x). Then ell_i(T_i)<=q<=u_i(T_i). Every outside
configuration has f_l(x_l)>=q, so its local maximum is at least q and the
outside partition has bottleneck at least q. Hence q belongs to J_i,T_i.

Conversely, suppose q belongs to J_iT. Recover an outside partition attaining
U^(-i)(K minus T), and set every outside x_l to a local maximizer. Their
new responses are all at least q. In the anchor slice, interpolate its
minimizer and maximizer to attain exactly q. Convexity keeps this point in
Q_i(T). All old lower inequalities hold; each old upper inequality has an
assigned witness. Thus the source is consistent and its new minimum is q.
For a singleton anchor range no interpolation is needed. The n=1 and k=0
cases are covered by the explicit empty-set conventions.

Every interval endpoint is selected from a local LP optimum. Sorting and
merging the at most n*2^k intervals proves the stated comparison bound.
Rational source recovery uses affine interpolation and therefore retains
polynomial bit length in the LP certificates and requested rational q.
The claim makes no strongly-polynomial LP or uncharged solver assertion.

## Why gaps and source independence still matter

The two-segment example still returns {1,2}; its interval hull would contain
the unattainable value 3/2. The two-hypersimplex construction still gives
binom(k,k/2)/2 isolated values for even k. Those are not artifacts of the
old recurrence. AR1 gives a near-matching exponential-in-k output bound,
up to polynomial factors when n=2.

The outside maximum combines independently chosen local witnesses. Coupled
unknown generators invalidate that step; receipt_coupling.md gives a precise
hardness reduction. A joint vector of future minima also does not follow
from AR1. See joint_values.md for a valid LP fallback and a separate barrier.
Noisy observation intervals do fit AR1 directly, but statistical coverage
of those intervals remains an external premise, not a consequence of this
exact geometric computation.

## Cheap development check and comparison still required

The planned probe will compare AR1 with exhaustive observation assignments
and the earlier interval-union recurrence on small rational polytopes, and
will check recovered source points against the original inequalities. It
will preserve exact gaps and inconsistent cases. Generic max-affine fitting,
set-cover regression and disjunctive LP are close ordinary comparisons; the
specific full-range parameter bound and useful retention duty still require
an honest novelty assessment. No promotion or readiness number is asserted
by this derivation alone.

## Executed development check

[Source](anchor_range_check.py) was hashed before generation and execution:
0b52864e3bf5d46585e330b2fcff4135ee67e7e0e51bb777bf88bd870446a3c8.
It imports the frozen earlier interval recurrence with hash
4a8d5cd8b46afa9d96735ff1939fa211e9c6a333bf713af27cf1eb8ba4f81715.
[Plan](anchor_range_plan.json), [inputs](anchor_range_inputs.json),
[result](anchor_range_result.json). Seed191928; input hash
8fc273eeb93f66903aa76476e6444f7ce84f3f204c05547883d566d40fb9760c.

PASS on180 rational polygon cases against both exhaustive assignments and
the earlier interval-union recurrence;472 recovered source checks;17
inconsistent cases and3 disconnected cases. Five noisy versions of the
two-segment gap agree with the analytic formula, including gap closure at
epsilon2/3. Five hypersimplex cases through k=10 give1,3,10,35,126 components.
Runtime918,426,500ns on this host is a development invoice, not a theorem.

The polygon panel uses98,280 anchored split scans versus34,224 exhaustive
assignment scans. These units do not include the same operations and do not
establish a practical speed advantage. At small n,k the stronger worst-case
parameter bound can have larger constants. The check validates this finite
implementation and witnesses; it does not independently verify generic LP
certificates, the asymptotic proof, novelty or application-level savings.
