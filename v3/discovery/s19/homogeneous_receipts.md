# A direct shortcut for many exchangeable configurations

Codex (GPT-6), October26,2026. DEVELOPMENT; derived strong ordinary control.
This materially narrows when the general AR1 subset algorithm is useful.

Assume every configuration has the same compact convex region B, every old
response uses the same affine g_j, and the new response uses the same affine
f. The unknown configuration vectors remain independently variable, not
equal to one another. Let

    Q(T) = B intersect all {g_j>=a_j} intersect {g_j<=b_j : j in T}.
    ell(T)=min_(Q(T)) f; u(T)=max_(Q(T)) f.

Suppose n>=k>=1. The old receipts are consistent exactly when every
singleton Q({j}) is nonempty: necessity is immediate, and sufficiency
assigns a separate configuration to each receipt. Put

    U = min_j u({j}); L_single = min_j ell({j}); L_empty=ell(empty).

Then the entire new-value set is one closed interval [L,U], where

    L = L_empty, if n>=k+1 or any Q({a,b}) is nonempty for distinct a,b;
        L_single, otherwise (n=k and all pairs are infeasible).

For k=0, the answer is simply [ell(empty),u(empty)] for any n>=1.
If a required slice is empty, return inconsistency before taking extrema.

## Proof and witnesses

Any source attaining an old upper receipt j has at least one configuration
in Q({j}); hence its new minimum cannot exceed u({j}). Assigning one
configuration to a maximizer in each singleton slice, and remaining
configurations to maximizers in Q(empty), attains U.

If n>=k+1, put one free configuration at an f-minimizer in Q(empty) and
use k others for the singleton receipts, attaining L_empty. For every
q in [L_empty,U], interpolate the free configuration within Q(empty) to
f=q and use singleton maximizers for the others. This constructs the full
interval, including when some singleton intervals are disjoint.

Now let n=k. Every q in [L_single,U] is attainable by anchoring at a
singleton slice with minimum ell and putting the other k-1 configurations
at their singleton maxima. If no pair slice is feasible, a configuration
cannot witness two old upper receipts. All k configurations must witness
one each, so no value below L_single is possible.

If a pair slice Q({a,b}) is feasible, put both receipts on one configuration
and leave one configuration free. Its maximum u({a,b}) is at least
ell({a,b})>=L_single. Consequently every q in [L_empty,L_single] can be
attained by putting the free configuration at f=q, the pair configuration
at its maximum, and all other receipt configurations at singleton maxima.
All these other values are at least q. Combining the two intervals proves
the claim. This argument does not require a topological connectivity theorem.

At most2k+2 local extremum LPs and binom(k,2) pair-feasibility LPs suffice;
the pair search stops at its first success and is unnecessary if n>k or
L_empty=L_single. A pair maximizer for a requested witness adds one LP.
This is polynomial in k, independent of n except for writing the source.
It is a derived ordinary shortcut, not a measured speedup or novelty claim.

## What the shortcut excludes

The common-profile assumptions are substantive. With k=n=2 and
B=conv{(0,1),(1,0)}, exact coordinate-minimum receipts0 force opposite
endpoints. If the new affine response is configuration-specific, choose
f_1 to take endpoint values1 and2, and f_2 to take3 and4. The two possible
new minima are1 and2, so the range has a gap. Thus common B and common old
responses alone do not imply the scalar conclusion at n=k.

For heterogeneous regions, adding arbitrarily many configurations that
cannot attain any old receipt and whose new costs are high preserves a
two-configuration gap. A large n/k ratio alone therefore does not remove
AR1's assignment problem. Nonetheless a natural use case must explain
why configuration-specific bounds or responses are warranted: homogeneous
scalar-only inference with sufficiently many configurations is already easy.

## Repeated profile types

A related easy regime has h profile types, each containing at least k+1
configurations with identical B, old responses and new response within its
type. Every empty slice must be feasible. Provided each receipt has some
feasible singleton type, the range is

    [ min_type ell_type(empty),
      min( min_type u_type(empty), min_j max_type u_type({j}) ) ].

Use one free anchor in a type achieving the lower endpoint. Assign each
receipt separately to a type whose singleton maximum is at least the upper
endpoint, and put every remaining configuration at its empty-slice maximum.
At most k+1 copies of any type are needed for that construction. The same
interpolation proves all intermediate values. Local extrema need only
O(h*k) LPs; the output source itself still has n vectors. This extension
again exploits redundant independent configurations, not identical hidden
vectors or unpriced recovery of full optimizer data.

## Development check

The frozen menu_range_probe.py checked180 seeded homogeneous coverage-menu
polytopes against AR1, with no mismatch. The larger288-case panel also made
239 direct assignment crosschecks. These exact integer-extremum examples
exercise inconsistent, pair-feasible and pair-infeasible cases. They are
finite development checks, not independent confirmation or runtime evidence.
